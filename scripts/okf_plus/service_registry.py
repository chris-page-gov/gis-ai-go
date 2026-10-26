#!/usr/bin/env python3
"""Offline, bounded OS service/route cards; this module never executes a route.

Implementation means the named local profile contains code, not that credentials,
entitlement, service availability or a successful test run have been established.
Native contracts remain evidence, including unresolved servers and callable=false.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, SchemaError, ValidationError

try:
    from .model import BASE, canonical, digest, load_json, markdown_text, read_markdown, safe_reference
    from .semantic import semantic_id
except ImportError:
    from model import BASE, canonical, digest, load_json, markdown_text, read_markdown, safe_reference
    from semantic import semantic_id

ROOT = Path(__file__).resolve().parents[2]
SOURCE = 'okf-plus/source/os-api-contracts.json'
SCHEMA = 'okf-plus/schemas/service-registry-card.schema.json'
MAX_CARD_BYTES = 16 * 1024
PROFILE = 'private-ngd-extract-with-transient-profile'
VERSION = 'gis-ai-go.okf-plus-service-registry.v2'
CONTEXT_URL = BASE + 'service-registry/context.jsonld'
CONTEXT = {'@version': 1.1, 'okfp': BASE + 'vocab/',
           'dcterms': 'http://purl.org/dc/terms/', 'dcat': 'http://www.w3.org/ns/dcat#',
           'prov': 'http://www.w3.org/ns/prov#',
           'schemaVersion': 'okfp:cardSchema', 'kind': 'okfp:recordType',
           'title': 'dcterms:title', 'service': 'okfp:serviceIdentifier',
           'parent': {'@id': 'dcterms:isPartOf', '@type': '@id'},
           'atomicOperation': {'@id': 'dcterms:relation', '@type': '@id'},
           **{k: {'@id': 'okfp:' + k, '@type': '@json'} for k in
              ('source', 'native', 'role', 'statuses', 'implementationEvidence', 'gaps',
               'operationCounts', 'links', 'scope')}}

# These are reviewed summaries of the retained route types, not quotations or
# claims of current access. Each card binds the overview and its operation cohort.
ROLES = {
    'os-ngd-api-features': ('data', 'Discover NGD collections and schemas, query features and retrieve individual features.'),
    'os-ngd-api-tiles': ('data', 'Discover NGD tile collections, tile matrices and styles, and retrieve vector tiles.'),
    'os-features-api': ('data', 'Query feature data and archive features through WFS capabilities, schema and feature requests.'),
    'os-vector-tile-api': ('data', 'Retrieve vector map tiles, service metadata and styles.'),
    'os-maps-api': ('data', 'Retrieve raster map tiles through ZXY or WMTS requests.'),
    'os-places-api': ('data', 'Find address records by search text, postcode, UPRN and spatial searches.'),
    'os-names-api': ('data', 'Find named places by text or nearest-location searches.'),
    'os-linked-identifiers-api': ('data', 'Follow relationships between identifiers, feature types and product versions.'),
    'os-downloads-api': ('data', 'Discover products and data packages, inspect versions and request downloadable files.'),
    'os-net-api': ('data', 'Inspect positioning stations and their health, and discover or retrieve RINEX observations and prepared ZIP downloads.'),
    'oauth-2-api': ('authentication', 'Authentication support; no executable OpenAPI operation was retained in this documentation cohort.'),
    'os-match-and-cleanse-api': ('data', 'Address matching and cleansing; the retained service title explicitly marks this API withdrawn.'),
}
NGD_SERVER = 'https://api.os.uk/features/ngd/ofa/v1'
DOWNLOAD_SERVER = 'https://api.os.uk/downloads/v1/'
DEFERRED_METADATA_SOURCE = (
    'https://github.com/chris-page-gov/gis-ai-go/blob/'
    '35318abcce5e23c1509ed6ce131d81f5dfd0d38c/scripts/okf_plus/metadata_refresh.py'
)
METADATA_PATHS = {
    'os-ngd-api-features': {'/collections', '/collections/{collectionId}/schema', '/collections/{collectionId}/queryables'},
    'os-downloads-api': {'/products', '/products/{productId}', '/products/{productId}/downloads',
                         '/dataPackages', '/dataPackages/{dataPackageId}',
                         '/dataPackages/{dataPackageId}/versions',
                         '/dataPackages/{dataPackageId}/versions/{versionId}'},
}
EVIDENCE_FILES = {
    # The separate metadata-capture extension remains on its immutable
    # reconciliation branch. No local implementation is claimed for it here.
    'metadata': (),
    'data': (('implementation', 'scripts/okf_plus/ngd_extract.py'),
             ('implementation', 'scripts/okf_plus/transient_profile.py'),
             ('synthetic-test-contract', 'tests/contract/test_okf_plus_ngd_extract.py'),
             ('synthetic-test-contract', 'tests/contract/test_okf_plus_transient_profile.py')),
}


def _file(root, relative):
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()) or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('Source and bundle paths must be local, contained and not symlinks')
    return path


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _service(row):
    path = urlsplit(row['url']).path.strip('/').split('/')
    if len(path) >= 3 and path[:2] == ['os-apis', 'accessing-os-apis']:
        return path[2].removesuffix('.md')
    return None


def service_id(slug):
    return BASE + 'service-registry/id/service/' + slug


def _path(card_id, kind):
    return 'cards/' + kind + '/' + _sha(card_id.encode()) + '.md'


def _evidence(root, category):
    return [{'path': p, 'sha256': _sha(_file(root, p).read_bytes()),
             'kind': kind} for kind, p in EVIDENCE_FILES[category]]


def _source(snapshot, snapshot_hash, index, suffix=''):
    row = snapshot['records'][index]
    value = row
    for part in suffix.strip('/').split('/') if suffix else []:
        value = value[int(part)] if isinstance(value, list) else value[part]
    receipts = [r for r in snapshot.get('receipts', []) if r.get('status') == 200
                and r.get('url') == row['url'] and r.get('sha256') == row.get('sourceSha256')]
    return {'snapshot': SOURCE, 'snapshotSha256': snapshot_hash,
            'pointer': '/records/' + str(index) + suffix, 'valueSha256': digest(value),
            'recordPointer': '/records/' + str(index), 'recordSha256': digest(row),
            'documentUrl': safe_reference(row['url']), 'documentSha256': row.get('sourceSha256'),
            'captureReceipt': deepcopy(receipts[0]) if receipts else None,
            'binding': 'matched-capture-receipt' if receipts else 'normalised-source-only'}


def _statuses(lifecycle, metadata=False, data=False):
    return {'documented': 'retained-documentation', 'lifecycle': lifecycle,
            'metadataCaptureImplemented': 'implemented-subset' if metadata else 'not-implemented-in-profile',
            'dataExecutorImplemented': 'implemented-subset' if data else 'not-implemented-in-profile',
            'syntheticValidation': 'test-contracts-present-not-executed-by-registry' if metadata or data else 'not-evidenced',
            'liveAccess': 'not-tested'}


def _support(slug, operation, servers, lifecycle):
    valid = operation['method'] == 'GET' and lifecycle == 'current-in-retained-documentation'
    data = (valid and slug == 'os-ngd-api-features' and servers == [NGD_SERVER]
            and operation['path'] == '/collections/{collectionId}/items'
            and operation.get('operationId') == 'getItems')
    return False, bool(data)


def _base(slug, title, kind, source, lifecycle):
    return {'@context': CONTEXT_URL, '@type': ['okfp:ServiceCapabilityCard', 'dcat:DataService'],
            'schemaVersion': VERSION, 'kind': kind, 'service': slug, 'title': title,
            'source': source, 'statuses': _statuses(lifecycle), 'implementationEvidence': [],
            'gaps': [], 'scope': {'executionProfile': PROFILE,
                'metadataProfile': 'closed-os-metadata-refresh', 'providerRequestsMade': 0,
                'authority': 'documentation-and-code-inventory-only',
                'otherImplementations': (
                    'Other executors and experimental Sites adapters are outside the named NGD extraction and transient profiling profile; '
                    'these statuses are not whole-repository claims. Broader metadata capture remains a separate extension on the '
                    'reconciliation branch, absent from this checkout: ' + DEFERRED_METADATA_SOURCE)}}


def project(root=ROOT, *, snapshot=None):
    """Return source-bound cards and coverage without touching network or secrets."""
    root = Path(root).resolve()
    raw = _file(root, SOURCE).read_bytes()
    loaded = load_json(raw.decode())
    if snapshot is None:
        snapshot = loaded
    elif snapshot != loaded:
        raise ValueError('The projection must bind the exact source snapshot on disk')
    if snapshot.get('family') != 'os-api-contracts':
        raise ValueError('Unexpected source family')
    snapshot_hash = _sha(raw)
    grouped, unassigned = {}, []
    for index, row in enumerate(snapshot['records']):
        slug = _service(row)
        if slug is None:
            # Core and supporting documents are explicitly counted, never lost.
            if row.get('contracts'):
                slug = 'unmapped-' + _sha(row['url'].encode())[:16]
            else:
                unassigned.append(index)
                continue
        grouped.setdefault(slug, []).append((index, row))
    cards = []
    for slug, rows in sorted(grouped.items()):
        overview_index, overview = next(((i, r) for i, r in rows if r['url'].endswith('/' + slug + '.md')), rows[0])
        lifecycle = ('withdrawn-in-retained-documentation' if 'withdrawn' in overview['title'].lower()
                     else 'current-in-retained-documentation' if slug in ROLES else 'unknown')
        service = _base(slug, overview['title'], 'service', _source(snapshot, snapshot_hash, overview_index), lifecycle)
        service['@id'] = service_id(slug)
        service['native'] = {'sourceCallable': overview.get('callable'), 'documentationCount': len(rows)}
        category, summary = ROLES.get(slug, ('unknown', 'Unmapped retained API documentation; service role needs review.'))
        service['role'] = {'category': category, 'summary': summary, 'basis': 'reviewed-summary-of-retained-title-and-route-types',
                           'evidence': 'source overview plus operation cards selected by service identifier'}
        service['links'] = {'operations': {'relation': 'indexed-children', 'command': 'routes', 'service': slug},
                            'atomicBundle': {'relation': 'separate-semantic-index', 'command': 'semantic_search.py read',
                                             'note': 'Pass the separately generated semantic bundle; this registry does not resolve its cards.'}}
        operations = []
        for index, row in rows:
            for ci, contract in enumerate(row.get('contracts', [])):
                for oi, operation in enumerate(contract.get('operations', [])):
                    suffix = f'/contracts/{ci}/operations/{oi}'
                    atomic = semantic_id('api-operation', 'os-api-contracts', row['id'], suffix)
                    card = _base(slug, operation['method'] + ' ' + operation['path'], 'operation', _source(snapshot, snapshot_hash, index, suffix), lifecycle)
                    card.update({'@id': BASE + 'service-registry/id/operation/' + _sha(atomic.encode()),
                                 'parent': service['@id'], 'atomicOperation': atomic,
                                 'role': {'category': category, 'summary': card['title'], 'basis': 'native-operation',
                                          'evidence': card['source']['pointer']},
                                 'native': {'operation': deepcopy(operation), 'servers': deepcopy(contract['servers']),
                                            'openapi': contract.get('openapi'), 'contractVersion': contract.get('version'),
                                            'fragmentSha256': contract.get('fragmentSha256'),
                                            'contractSha256': digest(contract), 'sourceCallable': row.get('callable'),
                                            'unresolvedComponentClasses': deepcopy(contract.get('unresolvedComponentClasses', []))},
                                 'links': {'atomicContract': {'relation': 'separate-semantic-index',
                                                             '@id': semantic_id('api-contract', 'os-api-contracts', row['id'], f'/contracts/{ci}'),
                                                             'note': 'Component schemas, parameters and security schemes are separate children of this contract in the semantic bundle.'}}})
                    metadata, data = _support(slug, operation, contract['servers'], lifecycle)
                    card['statuses'] = _statuses(lifecycle, metadata, data)
                    if metadata:
                        card['implementationEvidence'] += _evidence(root, 'metadata')
                        card['scope']['supportedMetadata'] = 'GET with substituted native identifiers and no query; downloads lists metadata only, with no fileName or redirect parameters.'
                    if data:
                        card['implementationEvidence'] += _evidence(root, 'data')
                        card['scope']['supportedData'] = (
                            'ngd_extract.py requires a collection identifier and bbox in CRS84 or EPSG:27700; '
                            'output CRS is EPSG:27700, EPSG:7405, EPSG:4326 or EPSG:3857. '
                            'Optional native osid selection uses OR or IN with collection-bound queryables evidence. '
                            'Requests, bytes, elapsed time and rate are bounded; private pages, NDJSON and receipts support resumption. '
                            'transient_profile.py creates a separate local profile; ngd_extract.discard_payloads requires '
                            'complete selection-bound profiling, matching payload hashes and complete field cardinalities before disposal.')
                        card['gaps'].append(
                            'The named executor requires bbox; arbitrary CQL, datetime, a whole-collection option and '
                            'returned-schema validation are outside its implemented selection contract.')
                    if not data:
                        card['gaps'].append('No geographic-data executor in the named NGD extraction and transient profiling profile for this operation.')
                    if any('${' in server for server in contract['servers']):
                        card['gaps'].append('Retained server contains an unresolved variable; no endpoint has been invented.')
                    if contract.get('unresolvedComponentClasses'):
                        card['gaps'].append('Retained contract has unresolved component classes; preserve and inspect the linked contract evidence.')
                    if operation['path'] in {'/prepareRinexZipDownload', '/startRinexZipDownload'}:
                        card['gaps'].append('GET may initiate remote preparation work; HTTP method alone does not admit this operation.')
                    operations.append(card)
        metadata_count = sum(c['statuses']['metadataCaptureImplemented'] == 'implemented-subset' for c in operations)
        data_count = sum(c['statuses']['dataExecutorImplemented'] == 'implemented-subset' for c in operations)
        service['operationCounts'] = {'retained': len(operations), 'metadataCaptureImplemented': metadata_count, 'dataExecutorImplemented': data_count}
        service['statuses'] = _statuses(lifecycle, metadata_count > 0, data_count > 0)
        for category_key, count in (('metadata', metadata_count), ('data', data_count)):
            if count:
                service['implementationEvidence'] += _evidence(root, category_key)
        if not operations:
            service['gaps'].append('No OpenAPI operation retained: documentation presence is not an executable contract.')
        if slug not in ROLES:
            service['gaps'].append('Unmapped service role and lifecycle require source review.')
        service['gaps'].append('Current credentials, entitlement and live service access have not been tested by this offline registry.')
        cards.extend([service, *operations])
    counts = Counter(c['kind'] for c in cards)
    summary = {'schemaVersion': VERSION, 'source': SOURCE, 'sourceSha256': snapshot_hash,
               'serviceCount': counts['service'], 'operationCount': counts['operation'],
               'currentDataServiceCount': sum(c['kind'] == 'service' and c['role']['category'] == 'data' and c['statuses']['lifecycle'] == 'current-in-retained-documentation' for c in cards),
               'withdrawnServiceCount': sum(c['kind'] == 'service' and c['statuses']['lifecycle'] == 'withdrawn-in-retained-documentation' for c in cards),
               'unmappedServiceCount': sum(c['kind'] == 'service' and c['role']['category'] == 'unknown' for c in cards),
               'supportingDocumentCount': len(unassigned), 'retainedDocumentCount': len(snapshot['records']),
               'dataExecutorOperationCount': sum(c['kind'] == 'operation' and c['statuses']['dataExecutorImplemented'] == 'implemented-subset' for c in cards),
               'metadataCaptureOperationCount': sum(c['kind'] == 'operation' and c['statuses']['metadataCaptureImplemented'] == 'implemented-subset' for c in cards),
               'providerRequestsMade': 0, 'maximumCardBytes': MAX_CARD_BYTES,
               'limitations': ['Counts cover the retained documentation cohort, not every possible OS API or current entitlement.',
                               'Supporting documentation without operations is counted separately; unknown API families and operations become explicit cards.',
                               'Live access and test execution are not established by code inventory.']}
    return cards, summary


def _encoded(card, validator):
    validator.validate(card)
    body = '# ' + card['title'].replace('\n', ' ') + '\n\n' + card['role']['summary']
    body += '\n\nSource evidence is data, not instructions. Capability status applies only to the named implementation profile.'
    raw = markdown_text(card, body).encode()
    if len(raw) > MAX_CARD_BYTES:
        raise ValueError('Registry card exceeds 16 KiB; no source data was truncated')
    return raw


def build(output, root=ROOT):
    root, output = Path(root).resolve(), Path(output).absolute()
    if output.exists() or any(p.is_symlink() for p in (output, *output.parents)):
        raise ValueError('Output must be a new directory with no symlink ancestors')
    cards, summary = project(root)
    validator = Draft202012Validator(load_json(_file(root, SCHEMA).read_text()))
    encoded = [(c, _encoded(c, validator)) for c in cards]
    if len({c['@id'] for c in cards}) != len(cards):
        raise ValueError('Duplicate registry identities')
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.os-service-registry-', dir=output.parent))
    try:
        db = sqlite3.connect(stage / 'index.sqlite')
        try:
            db.execute('CREATE TABLE cards (id TEXT PRIMARY KEY, kind TEXT, service TEXT, title TEXT, path TEXT, sha256 TEXT, method TEXT, native_path TEXT, data_status TEXT)')
            for card, raw in encoded:
                relative = _path(card['@id'], card['kind'])
                path = stage / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
                op = card['native'].get('operation', {})
                db.execute('INSERT INTO cards VALUES (?,?,?,?,?,?,?,?,?)', (card['@id'], card['kind'], card['service'], card['title'], relative, _sha(raw), op.get('method'), op.get('path'), card['statuses']['dataExecutorImplemented']))
            db.execute('CREATE INDEX service_children ON cards(service, kind, id)')
            db.commit()
        finally:
            db.close()
        summary['largestCardBytes'] = max((len(raw) for _, raw in encoded), default=0)
        summary['indexSha256'] = _sha((stage / 'index.sqlite').read_bytes())
        (stage / 'summary.json').write_bytes(canonical(summary))
        (stage / 'context.jsonld').write_bytes(canonical({'@context': CONTEXT}))
        (stage / 'card.schema.json').write_bytes(_file(root, SCHEMA).read_bytes())
        stage.rename(output)
    except BaseException:
        shutil.rmtree(stage)
        raise
    return summary


def query(bundle, *, service=None, key=None, max_records=12, max_bytes=64 * 1024):
    """Read bounded cards or route summaries through a local, read-only index."""
    if type(max_records) is not int or not 1 <= max_records <= 100 or type(max_bytes) is not int or not 1024 <= max_bytes <= 1024 * 1024:
        raise ValueError('Reader bounds must be 1..100 records and 1024..1048576 bytes')
    bundle = Path(bundle).absolute()
    index = _file(bundle, 'index.sqlite')
    if index.stat().st_size > 8 * 1024 * 1024:
        raise ValueError('Registry index exceeds the bounded local profile')
    summary_path = _file(bundle, 'summary.json')
    if summary_path.stat().st_size > MAX_CARD_BYTES:
        raise ValueError('Oversized registry summary')
    summary = load_json(summary_path.read_text())
    if summary.get('schemaVersion') != VERSION:
        raise ValueError('Registry bundle version is unsupported; rebuild for the current execution profile')
    if _sha(index.read_bytes()) != summary['indexSha256']:
        raise ValueError('Registry index integrity mismatch')
    db = sqlite3.connect(index.as_uri() + '?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    try:
        if key:
            where, values = 'id = ? OR (kind = ? AND service = ?)', (key, 'service', key)
        elif service:
            where, values = 'kind = ? AND service = ?', ('operation', service)
        else:
            where, values = 'kind = ?', ('service',)
        total = db.execute('SELECT COUNT(*) FROM cards WHERE ' + where, values).fetchone()[0]
        if key and total != 1:
            raise ValueError('Read requires one exact card ID or service identifier')
        rows = db.execute('SELECT * FROM cards WHERE ' + where + ' ORDER BY service,id LIMIT ?', (*values, max_records)).fetchall()
        results = []
        validator = Draft202012Validator(load_json(_file(ROOT, SCHEMA).read_text()))
        for row in rows:
            if key:
                if row['path'] != _path(row['id'], row['kind']):
                    raise ValueError('Invalid indexed card path')
                path = _file(bundle, row['path'])
                if path.stat().st_size > MAX_CARD_BYTES or _sha(path.read_bytes()) != row['sha256']:
                    raise ValueError('Registry card size or integrity mismatch')
                card, _ = read_markdown(path)
                validator.validate(card)
                if (card['@id'], card['kind'], card['service']) != (row['id'], row['kind'], row['service']):
                    raise ValueError('Registry card identity mismatch')
                result = card
            else:
                result = {k: row[k] for k in ('id', 'kind', 'service', 'title', 'method', 'native_path', 'data_status')}
            candidate = {'total': total, 'returned': len(results) + 1, 'truncated': total > len(results) + 1, 'records': [*results, result]}
            if len(canonical(candidate)) > max_bytes:
                break
            results.append(result)
        return {'total': total, 'returned': len(results), 'truncated': total > len(results), 'records': results}
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    producer = sub.add_parser('build')
    producer.add_argument('--repo', type=Path, default=ROOT)
    producer.add_argument('--output', type=Path, required=True)
    for name in ('list', 'routes', 'read'):
        reader = sub.add_parser(name)
        reader.add_argument('--bundle', type=Path, required=True)
        reader.add_argument('--max-records', type=int, default=12)
        reader.add_argument('--max-bytes', type=int, default=64 * 1024)
        if name != 'list':
            reader.add_argument('identifier')
    args = parser.parse_args()
    try:
        if args.command == 'build':
            result = build(args.output, args.repo)
        else:
            result = query(args.bundle, key=args.identifier if args.command == 'read' else None,
                           service=args.identifier if args.command == 'routes' else None,
                           max_records=args.max_records, max_bytes=args.max_bytes)
        print(canonical(result).decode(), end='')
    except (ValueError, OSError, sqlite3.Error, SchemaError, ValidationError, KeyError, TypeError) as exc:
        message = exc.message if isinstance(exc, (SchemaError, ValidationError)) else str(exc)
        parser.exit(2, 'Service registry error: ' + message.replace('\n', ' ')[:300] + '\n')


if __name__ == '__main__':
    main()
