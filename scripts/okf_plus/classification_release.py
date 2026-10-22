"""Validate reviewed classification lists and export private, source-bound cards.

Offline only. A complete selected list is not a complete domain, a semantic
mapping, or proof that a supplier currently uses that release in every product.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator

try:
    from .model import canonical, digest, identifier, load_json, markdown_text, record, safe_reference
    from .term_discovery import build_discovery
    from .native_search import validate_native_search, qualified_form
    from .label_origin import validate_label_origin, label_assertions
except ImportError:
    from model import canonical, digest, identifier, load_json, markdown_text, record, safe_reference
    from term_discovery import build_discovery
    from native_search import validate_native_search, qualified_form
    from label_origin import validate_label_origin, label_assertions

SCHEMA = 'gis-ai-go.classification-browser.v1'
MAX_BYTES = 16 * 1024 * 1024
MAX_CARD_BYTES = 16 * 1024
ROOT = Path(__file__).resolve().parents[2]


def read_payload(path):
    """Bound the actual read and refuse links, special files and concurrent edits."""
    path = Path(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_BYTES:
            raise ValueError('Classification input must be a bounded regular file')
        raw = stream.read(MAX_BYTES + 1)
        after = os.fstat(stream.fileno())
    identity = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    if (len(raw) > MAX_BYTES or len(raw) != before.st_size
            or identity(before) != identity(after) or identity(after) != identity(path.lstat())):
        raise ValueError('Classification input changed during its bounded read')
    return load_json(raw.decode('utf-8')), hashlib.sha256(raw).hexdigest()


def validate(payload):
    schema = load_json((ROOT / 'okf-plus/schemas/classification-browser.schema.json').read_text())
    Draft202012Validator(schema).validate(payload)
    seen = set()
    for scheme in payload['schemes']:
        if scheme['id'] in seen:
            raise ValueError('Duplicate scheme identity')
        seen.add(scheme['id'])
        sources = {s['id']: s for s in scheme['sources']}
        if len(sources) != len(scheme['sources']):
            raise ValueError('Duplicate source identity within scheme')
        for source in sources.values():
            safe_reference(source['url'])
            url = urlsplit(source['url'])
            if url.scheme != 'https' or url.username or url.password:
                raise ValueError('Source links must be credential-free HTTPS references')
        entries = scheme['entries']
        coverage = scheme['coverage']
        if coverage['retainedEntries'] != len(entries):
            raise ValueError('Retained entry count disagrees with payload')
        if (coverage['status'] == 'complete-selected-list'
                and coverage['expectedEntries'] != len(entries)):
            raise ValueError('Complete selected lists require a matching explicit denominator')
        if len({e['id'] for e in entries}) != len(entries):
            raise ValueError('Duplicate entry identity within scheme')
        definitions = sum(e['definition'] is not None and bool(e['definition'].strip()) for e in entries)
        if coverage['definitionsStatus'] == 'source-definitions-retained' and definitions != len(entries):
            raise ValueError('Definition coverage claim disagrees with retained text')
        if coverage['definitionsStatus'] == 'labels-only' and definitions:
            raise ValueError('Labels-only coverage cannot conceal retained definitions')
        for entry in entries:
            if entry['sourceId'] not in sources:
                raise ValueError('Unresolved entry source')
            validate_native_search(entry, sources)
            validate_label_origin(entry, sources)
            for alias in entry['aliases']:
                if alias['sourceId'] not in sources:
                    raise ValueError('Unresolved lexical-form source')
        # Native code collisions are valid evidence, never an identity key.
    return payload


def concept_record(scheme, entry, payload_digest):
    source = next(s for s in scheme['sources'] if s['id'] == entry['sourceId'])
    # Unknown supplier editions must not collapse successive observed snapshots.
    snapshot = digest({'edition': scheme['edition'], 'sources': [
        {'url': s['url'], 'sha256': s['sha256']} for s in scheme['sources']]})
    scheme_identity = scheme['id'] + '/' + snapshot
    native_id = scheme_identity + '/' + entry['id']
    definition = entry['definition']
    description = definition if definition is not None else 'No separate source definition retained; consult the source label and scheme context.'
    coded = entry['code'] is not None and bool(entry['code'].strip())
    row = record('classification-release', native_id, entry['label'], description,
                 source['url'], {'resource': source['url'], 'sourceArtifactSha256': source['sha256'],
                                 'sourceArtifactTitle': source['title'],
                                 'sourceLocator': entry['sourceLocator'],
                                 'reviewedPayloadSha256': payload_digest}, kind='Concept' if coded else 'Documentation',
                 details={'scheme': {k: deepcopy(v) for k, v in scheme.items() if k != 'entries'},
                          'entry': deepcopy(entry)})
    row['reviewStatus'] = 'source-bound-projection; semantic-review-separate'
    row['rights'] = {'metadata': 'Source rights retained; private export is not redistribution permission.',
                     'describedData': 'Classification metadata only; no feature or statistical observations.',
                     'retrievalAuthority': 'offline-reviewed-input-only', 'executionAdmitted': False}
    row['limitations'] = list(scheme['gaps']) + [
        'The exporter validates structure, counts and source bindings, not the truth of source interpretations.',
        'Source code equality does not establish equivalence or a join across schemes or editions.',
        'Native parent/level values are retained; no inferred SKOS hierarchy is emitted.']
    row.update(label_assertions(entry,
        {s['id']: s for s in scheme['sources']}, coded))
    if coded:
        row['skos:notation'] = entry['code']
    if coded and definition is not None:
        row['skos:definition'] = definition
    row['skos:inScheme' if coded else 'dcterms:isPartOf'] = {'@id': identifier('classification-scheme', scheme_identity)}
    row['update']['releaseVersion'] = scheme['edition']
    row['temporal']['note'] = 'Release, reference and retrieval dates remain separately labelled in details.scheme; no validity interval inferred.'
    if entry['aliases']:
        by_id = {s['id']: s for s in scheme['sources']}
        row['okfp:lexicalForm'] = [
            {'@id': row['@id'] + '/lexical-form/' + str(i), '@type': 'okfp:LexicalForm',
             'rdf:value': {'@value': alias['text']}, 'okfp:formKind': alias['kind'],
             'okfp:authority': alias['authority'],
             'prov:wasDerivedFrom': [{'@id': by_id[alias['sourceId']]['url']}]}
            for i, alias in enumerate(entry['aliases'])]
    native_forms = validate_native_search(entry, {s['id']: s for s in scheme['sources']})
    if native_forms:
        row.setdefault('okfp:lexicalForm', []).extend(
            qualified_form(row['@id'], form, source['url']) for form in native_forms)
    return row


def export(payload, output, raw_digest, *, source_revision):
    # This is the reviewed producer source commit, not a truncated payload hash.
    if not isinstance(source_revision, str) or not re.fullmatch('[a-f0-9]{40}', source_revision):
        raise ValueError('Reviewed producer source revision must be 40 lowercase hexadecimal characters')
    validate(payload)
    if not re.fullmatch('[a-f0-9]{64}', raw_digest):
        raise ValueError('Input SHA-256 required')
    output = Path(output)
    if output.exists() or output.is_symlink():
        raise ValueError('Export requires a new output directory')
    if not output.parent.is_dir() or output.parent.is_symlink():
        raise ValueError('Export parent must be an existing directory, not a symlink')
    payload_digest = digest(payload)
    rows = [concept_record(scheme, entry, payload_digest)
            for scheme in payload['schemes'] for entry in scheme['entries']]
    record_schema = load_json((ROOT / 'okf-plus/schemas/record.schema.json').read_text())
    Draft202012Validator.check_schema(record_schema)
    record_validator = Draft202012Validator(record_schema)
    for row in rows:
        record_validator.validate(row)
    files = {}
    for row in rows:
        name = 'cards/' + hashlib.sha256(row['@id'].encode()).hexdigest() + '.md'
        # Supplier strings remain in JSON front matter, not interpreted as Markdown.
        raw = markdown_text(row, 'Source-bound classification metadata. Read the labelled source, dates and coverage limits in the front matter.').encode()
        if len(raw) > MAX_CARD_BYTES:
            raise ValueError('Classification card exceeds the small-knowledge ceiling')
        files[name] = raw
    index = build_discovery(rows, {'namespaces': []}, source_revision, payload_digest)
    index_schema = load_json((ROOT / 'okf-plus/schemas/term-discovery.schema.json').read_text())
    Draft202012Validator.check_schema(index_schema)
    Draft202012Validator(index_schema).validate(index)
    files['term-discovery.json'] = canonical(index)
    files['classification-browser.json'] = canonical(payload)
    manifest = {'schema': 'gis-ai-go.classification-export.v1', 'inputSha256': raw_digest,
                'producerSourceRevision': source_revision,
                'canonicalPayloadSha256': payload_digest, 'schemes': len(payload['schemes']),
                'records': len(rows), 'conceptRecords': sum(r['type'] == 'Concept' for r in rows),
                'uncodedSourceRecords': sum(r['type'] != 'Concept' for r in rows),
                'globalComplete': False, 'providerCalls': 0,
                'files': [{'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
            for name, raw in sorted(files.items())]}
    if any('labelOrigin' in entry for scheme in payload['schemes'] for entry in scheme['entries']):
        manifest['labelOrigins'] = {kind: sum(
            entry.get('labelOrigin', {}).get('kind', 'legacy-unqualified') == kind
            for scheme in payload['schemes'] for entry in scheme['entries'])
            for kind in ('source-native', 'project-display-fallback', 'legacy-unqualified')}
    # Exclusive creation preserves previous outputs. A failed write leaves an
    # incomplete directory without COMPLETE.json, never a false success receipt.
    output.mkdir(mode=0o700)
    (output / 'cards').mkdir(mode=0o700)
    for name, raw in files.items():
        with (output / name).open('xb') as stream:
            os.chmod(output / name, 0o600)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    pending = output / '.COMPLETE.pending'
    with pending.open('xb') as stream:
        os.chmod(pending, 0o600)
        stream.write(canonical(manifest))
        stream.flush()
        os.fsync(stream.fileno())
    pending.rename(output / 'COMPLETE.json')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--source-revision', required=True,
                        help='Exact reviewed producer source commit; not a payload hash')
    args = parser.parse_args()
    payload, sha = read_payload(args.input)
    result = export(payload, args.output, sha, source_revision=args.source_revision)
    print(json.dumps({'schemes': result['schemes'], 'records': result['records'],
                      'conceptRecords': result['conceptRecords'], 'uncodedSourceRecords': result['uncodedSourceRecords'],
                      'globalComplete': False, 'providerCalls': 0}))


if __name__ == '__main__':
    main()
