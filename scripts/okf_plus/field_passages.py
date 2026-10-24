#!/usr/bin/env python3
"""Private candidate links from exact native field headings to captured passages."""
from __future__ import annotations
import argparse
import hashlib
import re
import ctypes
import os
import shutil
import tempfile
from collections import Counter
from pathlib import Path
try:
    from .model import PREFIXES, canonical, load_json
    from .passages import no_symlinks
except ImportError:
    from model import PREFIXES, canonical, load_json
    from passages import no_symlinks

ROOT = Path(__file__).resolve().parents[2]
BASE = 'https://docs.os.uk/osngd/data-structure/'
BINDINGS = {'bld-fts-building-4': BASE + 'buildings/building-features/building.md',
            'trn-ntwk-roadlink-5': BASE + 'transport/transport-network/road-link.md',
            'trn-ntwk-pavementlink-1': BASE + 'transport/transport-network/pavement-link.md'}


def checked(base, relative):
    path = no_symlinks(Path(base) / relative)
    if not path.is_relative_to(Path(base).absolute()):
        raise ValueError('Path escapes evidence root')
    return path


def read(path, expected=None):
    raw = no_symlinks(path).read_bytes()
    if expected and hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('Evidence checksum mismatch')
    return load_json(raw.decode())


def heading_details(text):
    visible = text.replace('\\_', '_').replace('`', '')
    visible = re.sub(r'<a\b[^>]*>\s*</a>', '', visible).strip()
    visible = re.sub(r'^:new:\s*', '', visible)
    match = re.fullmatch(r'(.*?)\s+\(formerly\s+(.*?)\s*\)', visible)
    return (match[1].strip(), match[2].strip()) if match else (visible, None)


def heading_text(text):
    return heading_details(text)[0]


def document_sections(private, entry, url):
    directory = checked(private, entry['passageDirectory'])
    manifest_path = checked(directory, 'manifest.jsonld')
    manifest = read(manifest_path)
    source = manifest['source']
    if source['url'] != url or source['sha256'] != entry['receipt']['sha256']:
        raise ValueError('Document source binding mismatch')
    sections, former_names, heading_evidence = {}, {}, {}
    reconstructed = hashlib.sha256()
    reconstructed_bytes = 0
    for segment in manifest['segments']:
        path = checked(directory, segment['file'])
        payload = read(path, segment['sha256'])
        if path.stat().st_size != segment['bytes']:
            raise ValueError('Passage byte length mismatch')
        chunk = payload['text'].encode('utf-8')
        reconstructed.update(chunk)
        reconstructed_bytes += len(chunk)
        if payload['source'] != source or payload['position'] != segment['position']:
            raise ValueError('Passage source or position mismatch')
        for heading in payload['headingBreadcrumb']:
            name, former = heading_details(heading['text'])
            key = (heading['line'], heading['level'])
            heading_evidence[key] = heading
            if former and re.fullmatch(r'[A-Za-z0-9_]+', former):
                former_names.setdefault(former, {})[key] = {'kind': 'explicit-former-heading-annotation',
                    'sourceText': heading['text'], 'position': {'lineStart': heading['line']}}
            # A source-authored rename statement gives an exact old native name;
            # it does not make old/new fields interchangeable in a live query.
            if heading is payload['headingBreadcrumb'][-1]:
                prose = payload['text'].replace('\\_', '_')
                rename = re.match(r'^This attribute (?:was |is )?called\s+`([A-Za-z0-9_]+)`', prose)
                if rename and former:
                    former_names.setdefault(rename[1], {})[key] = {'kind': 'explicit-former-name-prose',
                        'sourceText': payload['text'], 'position': payload['position'],
                        'passageId': payload['@id'], 'sha256': segment['sha256']}
            sections.setdefault(name, {}).setdefault(key, []).append({
                '@id': payload['@id'], 'path': path.relative_to(Path(private).absolute()).as_posix(),
                'sha256': segment['sha256'], 'bytes': segment['bytes'],
                'position': segment['position'], 'headingBreadcrumb': payload['headingBreadcrumb']})
    if (reconstructed.hexdigest() != source['sha256'] or
            reconstructed_bytes != source['bytes'] or
            manifest['reconstruction']['sha256'] != reconstructed.hexdigest() or
            manifest['reconstruction']['bytes'] != reconstructed_bytes or
            ('bytes' in entry['receipt'] and entry['receipt']['bytes'] != reconstructed_bytes)):
        raise ValueError('Document reconstruction checksum or byte length mismatch')
    former_sections = {}
    for native, matches in former_names.items():
        for key, evidence in matches.items():
            current = heading_text(heading_evidence[key]['text'])
            former_sections.setdefault(native, {})[key] = {
                'passages': sections[current][key], 'evidence': evidence}
    return source, sections, hashlib.sha256(manifest_path.read_bytes()).hexdigest(), former_sections


REVIEWED_ROUTES = {
    'asu-gbpcd-postcodeunitpoint-1': BASE + 'administrative-and-statistical-units/gb-postcodes/postcode-unit-point.md',
    'trn-rami-routingstructure-1': BASE + 'transport/rami/routingstructure.md'}
BINDING_PROFILE = 'okf-plus/profile/os-collection-document-bindings.json'


def reviewed_bindings(root, native_collections):
    """Validate the bounded reviewed registry; source metadata cannot extend it."""
    path = checked(root, BINDING_PROFILE)
    raw = path.read_bytes()
    profile = load_json(raw.decode())
    if (profile.get('@type') != 'okfp:ReviewedCandidateDocumentBindings' or
            profile.get('policy', {}).get('executionAdmitted') is not False or
            not isinstance(profile.get('bindings'), list)):
        raise ValueError('Malformed reviewed binding profile')
    result, cache = {}, {}
    for index, binding in enumerate(profile['bindings']):
        native = binding.get('collectionId')
        if native not in REVIEWED_ROUTES or native in result or binding.get('documentUrl') != REVIEWED_ROUTES[native]:
            raise ValueError('Unreviewed or duplicate collection-document route')
        if binding.get('versionStatus') != 'current-document-not-independently-version-matched':
            raise ValueError('Reviewed binding cannot assert version equivalence')
        sources = binding.get('sources')
        if not isinstance(sources, list) or len(sources) < 3:
            raise ValueError('Reviewed binding lacks source evidence')
        resolved = {}
        for evidence in sources:
            source = evidence.get('snapshot')
            if source not in {'okf-plus/source/' + family + '.json' for family in
                    ['os-ngd-collections', 'osngd-documentation', 'osngd-documentation-pages', 'os-api-contracts']}:
                raise ValueError('Unreviewed source snapshot')
            if source not in cache:
                body = checked(root, source).read_bytes()
                cache[source] = (hashlib.sha256(body).hexdigest(), load_json(body.decode()))
            sha, snapshot = cache[source]
            if sha != evidence.get('snapshotSha256'):
                raise ValueError('Reviewed source snapshot checksum mismatch')
            pointer = evidence.get('pointer', '')
            if not re.fullmatch(r'/records/[0-9]+', pointer):
                raise ValueError('Invalid reviewed source pointer')
            record = snapshot['records'][int(pointer.rsplit('/', 1)[1])]
            if hashlib.sha256(canonical(record)).hexdigest() != evidence.get('normalisedRecordSha256'):
                raise ValueError('Reviewed source record checksum mismatch')
            if evidence.get('sourceSha256'):
                if record.get('sourceSha256') != evidence['sourceSha256'] or record.get('url') != evidence.get('sourceUrl'):
                    raise ValueError('Reviewed source response binding mismatch')
                if not any(r.get('sha256') == evidence['sourceSha256'] and
                        r.get('url') == evidence['sourceUrl'] and r.get('status') == 200
                        for r in snapshot['receipts']):
                    raise ValueError('Reviewed source response lacks receipt')
            resolved[source] = record
        collection = resolved.get('okf-plus/source/os-ngd-collections.json', {})
        document = resolved.get('okf-plus/source/osngd-documentation.json', {})
        if (collection.get('id') != native or collection.get('title') != binding.get('collectionTitle') or
                collection.get('description') != binding.get('nativeDefinition') or
                document.get('url') != binding['documentUrl'] or document.get('title') != binding.get('documentTitle')):
            raise ValueError('Reviewed native collection or document identity mismatch')
        if resolved.get('okf-plus/source/osngd-documentation-pages.json', {}).get('url') != binding['documentUrl']:
            raise ValueError('Reviewed document projection identity mismatch')
        if native.startswith('asu-') and resolved.get('okf-plus/source/os-api-contracts.json', {}).get('url') !=                 'https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features.md':
            raise ValueError('GB route lacks NI-exclusion review evidence')
        result[native] = {'url': binding['documentUrl'], 'evidence': {
            'profile': BINDING_PROFILE, 'profileSha256': hashlib.sha256(raw).hexdigest(),
            'pointer': '/bindings/' + str(index), 'reviewedBinding': binding}}
    if (set(REVIEWED_ROUTES) & set(native_collections)) - set(result):
        raise ValueError('Missing reviewed collection binding')
    return result


def reviewed_heading_bindings(root):
    path = checked(root, BINDING_PROFILE)
    raw = path.read_bytes()
    profile = load_json(raw.decode())
    bindings = profile.get('headingBindings', [])
    if not isinstance(bindings, list): raise ValueError('Malformed reviewed heading bindings')
    result = {}
    for number, binding in enumerate(bindings):
        if (not isinstance(binding, dict) or not isinstance(binding.get('collectionIds'), list) or
                not binding['collectionIds'] or binding.get('nativeField') not in {'osid', 'usrn'} or
                not re.fullmatch(r'[a-f0-9]{64}', binding.get('sourceSha256', '')) or
                type(binding.get('headingLine')) is not int or binding['headingLine'] < 1 or
                binding.get('headingText') != binding['nativeField'] or
                binding.get('versionStatus') != 'current-document-not-independently-version-matched' or
                not isinstance(binding.get('documentUrl'), str)):
            raise ValueError('Malformed reviewed primary heading binding')
        for native in binding['collectionIds']:
            key = (native, binding['nativeField'])
            if key in result: raise ValueError('Duplicate reviewed primary heading binding')
            result[key] = {**binding, 'profile': BINDING_PROFILE,
                'profileSha256': hashlib.sha256(raw).hexdigest(), 'pointer': '/headingBindings/' + str(number)}
    return result


def discover_bindings(root):
    """Exact frozen titles provide candidate routes, never version equivalence."""
    root = no_symlinks(root)
    paths = {'collections': 'okf-plus/source/os-ngd-collections.json',
             'documentation': 'okf-plus/source/osngd-documentation.json'}
    snapshots = {key: read(checked(root, path)) for key, path in paths.items()}
    hashes = {key: hashlib.sha256(checked(root, path).read_bytes()).hexdigest()
              for key, path in paths.items()}
    candidates = {}
    for number, document in enumerate(snapshots['documentation']['records']):
        if document['url'].startswith(BASE):
            candidates.setdefault(document['title'], []).append((number, document))
    result = {}
    for number, collection in enumerate(snapshots['collections']['records']):
        title = collection['title']
        unversioned = re.sub(r' v[0-9]+$', '', title)
        matches = candidates.get(unversioned, [])
        evidence = {'collectionTitle': title, 'matchTitle': unversioned,
            'collectionSnapshot': paths['collections'], 'collectionSnapshotSha256': hashes['collections'],
            'collectionPointer': '/records/' + str(number),
            'documentationSnapshot': paths['documentation'], 'documentationSnapshotSha256': hashes['documentation'],
            'candidates': [{'url': document['url'], 'title': document['title'],
                'pointer': '/records/' + str(index)} for index, document in matches]}
        result[collection['id']] = {'status': 'unique-route' if len(matches) == 1 else
            ('ambiguous-route' if matches else 'route-not-found'),
            'url': matches[0][1]['url'] if len(matches) == 1 else None, 'evidence': evidence}
    reviewed = reviewed_bindings(root, result)
    for native, binding in reviewed.items():
        if native not in result:
            continue
        result[native]['status'] = 'unique-route'
        result[native]['url'] = binding['url']
        result[native]['method'] = 'reviewed-route-exact-heading-candidate'
        result[native]['evidence']['reviewedCuration'] = binding['evidence']
    return result


def bounded_overlay(row, max_bytes):
    """Externalise whole ordered passage references; every file stays bounded."""
    if len(canonical(row)) <= max_bytes:
        return row, {}
    row = dict(row)
    passages = row['passages']
    if not passages:
        raise ValueError('Overlay metadata exceeds byte ceiling')
    files, entries, current = {}, [], []
    key = hashlib.sha256(row['@id'].encode()).hexdigest()
    def publish(group):
        payload = canonical({'references': group})
        name = key + '-references-' + str(len(entries) + 1) + '.json'
        files[name] = payload
        entries.append({'path': name, 'sha256': hashlib.sha256(payload).hexdigest(), 'bytes': len(payload)})
    for passage in passages:
        candidate = current + [passage]
        if len(canonical({'references': candidate})) > max_bytes:
            if not current: raise ValueError('Single passage reference exceeds byte ceiling')
            publish(current)
            current = [passage]
            if len(canonical({'references': current})) > max_bytes:
                raise ValueError('Single passage reference exceeds byte ceiling')
        else: current = candidate
    if current: publish(current)
    manifest = {'profile': 'okf-plus-passage-reference-manifest.v1',
        'sha256': hashlib.sha256(canonical(passages)).hexdigest(), 'referenceCount': len(passages),
        'reconstruction': 'Concatenate references arrays from ordered parts.', 'parts': entries}
    manifest_name = key + '-references-manifest.json'
    raw = canonical(manifest)
    if len(raw) > max_bytes: raise ValueError('Reference manifest exceeds byte ceiling')
    files[manifest_name] = raw
    row['passages'] = []
    row['passageManifest'] = {'path': manifest_name, 'sha256': hashlib.sha256(raw).hexdigest(),
                              'bytes': len(raw), 'referenceCount': len(passages)}
    if len(canonical(row)) > max_bytes: raise ValueError('Overlay metadata exceeds byte ceiling')
    return row, files


def overlays(cards_root, private, *, all_collections=False, root=ROOT):
    cards_root, private = no_symlinks(cards_root), no_symlinks(private)
    index = read(checked(cards_root, 'index.json'))
    checkpoint = read(checked(private, 'checkpoint.json'))
    registry = discover_bindings(root) if all_collections else {}
    heading_bindings = reviewed_heading_bindings(root) if all_collections else {}
    documents = {}
    collection_cache = None
    results = []
    for item in index['cards']:
        native_parent = item.get('parentNativeIdentifier', item['parent'].rsplit('/', 1)[-1])
        if not all_collections and native_parent not in BINDINGS:
            continue
        card = read(checked(cards_root, item['path']), item['sha256'])
        if card['parent']['nativeIdentifier'] != native_parent or card['field']['@id'] != item['id']:
            raise ValueError('Card identity mismatch')
        route = registry.get(native_parent, {'status': 'route-not-found', 'url': None}) if all_collections else {}
        url = route.get('url') if all_collections else BINDINGS[native_parent]
        entry = checkpoint['records'].get(url, {})
        row = {'@context': {**PREFIXES, **{k: {'@id': 'okfp:' + k, '@type': '@json'} for k in
                 ['card', 'parent', 'source', 'binding', 'passages', 'passageManifest', 'status', 'rights', 'limitations']}},
               '@id': card['@id'] + '/private-passages', '@type': 'okfp:CandidateFieldPassageOverlay',
               'card': {'@id': card['@id'], 'path': item['path'], 'sha256': item['sha256']},
               'parent': card['parent'], 'source': {'url': url},
               'binding': {'method': 'curated-route-exact-heading-match',
                           'versionStatus': 'current-document-not-independently-version-matched',
                           'nativeField': card['field']['dcterms:identifier']},
               'rights': {'audience': 'private', 'publicationAdmitted': False, 'executionAdmitted': False},
               'limitations': ['Candidate evidence links only; no inferred units, datum, methods or semantic equivalence.'],
               'passages': []}
        if all_collections:
            row['binding']['method'] = route.get('method', 'frozen-exact-title-exact-heading-candidate')
            row['binding']['routeEvidence'] = route.get('evidence', {})
        if all_collections and route['status'] != 'unique-route':
            row['status'] = route['status']
        elif entry.get('status') != 'captured':
            row['status'] = 'document-not-captured'
        else:
            if url not in documents:
                documents[url] = document_sections(private, entry, url)
            source, sections, manifest_hash, former_sections = documents[url]
            row['source'] = {**source, 'manifestSha256': manifest_hash, 'receipt': entry['receipt']}
            field = card['field']['dcterms:identifier']
            matches = sections.get(field, {})
            reviewed = heading_bindings.get((native_parent, field))
            if len(matches) > 1 and reviewed:
                if reviewed['documentUrl'] != url or reviewed['sourceSha256'] != source['sha256']:
                    raise ValueError('Reviewed primary heading source checksum mismatch')
                chosen = {key: refs for key, refs in matches.items() if key[0] == reviewed['headingLine']}
                if len(chosen) != 1: raise ValueError('Reviewed primary heading position mismatch')
                matches = chosen
                row['binding']['routeMethod'] = row['binding']['method']
                row['binding']['method'] = 'reviewed-primary-field-heading-candidate'
                row['binding']['headingEvidence'] = reviewed
            if not matches and field in former_sections:
                aliases = former_sections[field]
                matches = {key: value['passages'] for key,value in aliases.items()}
                row['binding']['routeMethod'] = row['binding']['method']
                row['binding']['method'] = 'source-explicit-former-name-heading-candidate'
                row['binding']['formerNameEvidence'] = [value['evidence'] for value in aliases.values()]
            if not matches and all_collections:
                retained = card['field'].get('okfp:schemaDefinition', {}).get('@value', {})
                if retained.get('type') == 'array' and isinstance(retained.get('items'), dict):
                    if collection_cache is None:
                        source_path = checked(root, 'okf-plus/source/os-ngd-collections.json')
                        raw = source_path.read_bytes()
                        snapshot = load_json(raw.decode())
                        collection_cache = (hashlib.sha256(raw).hexdigest(), {
                            value['id']: (number, value) for number, value in enumerate(snapshot['records'])})
                    snapshot_hash, native_sources = collection_cache
                    number, native_collection = native_sources[native_parent]
                    definition = native_collection['schemas']['schema']['properties'][field]
                    if canonical(definition) != canonical(retained):
                        raise ValueError('Native container definition checksum mismatch')
                    normalised = ''.join(field.split()).casefold()
                    label_matches = [(name, candidates) for name, candidates in sections.items()
                        if ''.join(name.split()).casefold() == normalised]
                    matches = {key: refs for _, candidates in label_matches for key, refs in candidates.items()}
                    if matches:
                        row['binding']['routeMethod'] = row['binding']['method']
                        row['binding']['method'] = 'source-container-label-heading-candidate'
                        row['binding']['containerEvidence'] = {
                            'snapshot': 'okf-plus/source/os-ngd-collections.json',
                            'snapshotSha256': snapshot_hash,
                            'pointer': '/records/' + str(number) + '/schemas/schema/properties/' +
                                field.replace('~', '~0').replace('/', '~1'),
                            'definitionSha256': hashlib.sha256(canonical(definition)).hexdigest(),
                            'schemaResponseSha256': native_collection['schemas']['schema']['sha256'],
                            'normalisation': 'Whitespace removal and casefold only; native top-level array/items required.',
                            'originalLabels': [name for name, _ in label_matches]}
            if len(matches) > 1:
                row['status'] = 'ambiguous-heading'
            elif not matches:
                row['status'] = 'heading-not-found'
            else:
                row['status'] = 'matched'
                row['passages'] = next(iter(matches.values()))
        results.append(row)
    return results


def export(root, cards_root=None, private=None, output=None, *, all_collections=False, max_overlay_bytes=16384):
    root = no_symlinks(root)
    cards_root = cards_root or root / 'artifacts/okf-plus/field-cards'
    private = private or root / 'artifacts/okf-plus/private-os-documents'
    output = no_symlinks(output or root / 'artifacts/okf-plus/field-passages')
    if not output.is_relative_to(root / 'artifacts'):
        raise ValueError('Output must be under artifacts')
    if type(max_overlay_bytes) is not int or not 1024 <= max_overlay_bytes <= 16384:
        raise ValueError('Overlay byte ceiling must be 1024..16384')
    if all_collections and output.exists():
        raise ValueError('All-collection output must be a new directory')
    rows = overlays(cards_root, private, all_collections=all_collections, root=root)
    files = {}
    for row in rows:
        bounded, references = bounded_overlay(row, max_overlay_bytes)
        files.update(references)
        files[hashlib.sha256(row['@id'].encode()).hexdigest() + '.jsonld'] = canonical(bounded)
    summary = {'schema': 'gis-ai-go.okf-plus-field-passages.v1', 'candidateOnly': True,
               'counts': dict(Counter(row['status'] for row in rows)),
               'bindings': {key: value['url'] for key,value in discover_bindings(root).items()
                            if value['status'] == 'unique-route'} if all_collections else BINDINGS,
               'allCollections': all_collections, 'maxOverlayBytes': max_overlay_bytes,
               'files': [{'path': name, 'sha256': hashlib.sha256(raw).hexdigest()} for name, raw in sorted(files.items())]}
    files['index.json'] = canonical(summary)
    for name in files:
        target = no_symlinks(output / name)
        if target.exists() and not target.is_file():
            raise ValueError('Output leaf must be a regular file')
    if all_collections:
        output.parent.mkdir(parents=True, exist_ok=True)
        stage = Path(tempfile.mkdtemp(prefix='.' + output.name + '-', dir=output.parent))
        try:
            for name, raw in files.items():
                with (stage / name).open('wb') as stream:
                    stream.write(raw); stream.flush(); os.fsync(stream.fileno())
            descriptor = os.open(stage, os.O_RDONLY | os.O_DIRECTORY)
            try: os.fsync(descriptor)
            finally: os.close(descriptor)
            rename = getattr(ctypes.CDLL(None, use_errno=True), 'renameat2', None)
            if rename is None: raise OSError('Atomic all-collection publication requires renameat2')
            rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
            rename.restype = ctypes.c_int
            no_symlinks(output)
            if rename(-100, os.fsencode(stage), -100, os.fsencode(output), 1):
                error = ctypes.get_errno()
                raise OSError(error, os.strerror(error), str(output))
        finally:
            if stage.exists(): shutil.rmtree(stage)
    else:
        output.mkdir(parents=True, exist_ok=True)
        for name, raw in files.items():
            (output / name).write_bytes(raw)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--all-collections', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    summary = export(args.root, output=args.output, all_collections=args.all_collections)
    print(canonical({'counts': summary['counts'], 'candidateOnly': True}).decode(), end='')

if __name__ == '__main__':
    main()
