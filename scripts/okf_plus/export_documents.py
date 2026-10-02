#!/usr/bin/env python3
"""Owner-private hand-off of verified official documentation originals only.

No network or capture-ledger write occurs. Statistical/catalogue/feature/account
responses and all unpinned specifications are outside this separate archive.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import tarfile
import tempfile
from urllib.parse import urlsplit

from export import MANIFEST, public_patterns, read_file, safe_path, sha, verify_archive
from harvest import allowed
from import_sources import captured_bytes
from model import canonical, load_json, safe_reference

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = 'gis-ai-go.okf-plus-private-document-export.v1'
MAX_DOCUMENTS = 3000
MAX_DOCUMENT_BYTES = 16 * 1024 * 1024
MAX_TOTAL_BYTES = 128 * 1024 * 1024
SPECIFICATIONS = {
    ('https://github.com/ONSdigital/dp-search-api', 'f634c78cc362654ddb464c4559d37202ba0034a9', 'swagger.yaml'):
        '8b897c35a7c7d98cfef5faa158c8a12d04acebabf69b6eee849f1aaf70b95029',
    ('https://github.com/ONSdigital/dp-dataset-api', 'ffe4c71027d7dd88484a408f0b19a823f312dfe6', 'swagger.yaml'):
        '269ed359fb2713734f450585027cae102585a6995559686cfe7404829a7d1f5a',
}
# Exact already-reviewed public example placeholders only. Retain original
# bytes, but do not mistake these literal instructions for real credentials.
PLACEHOLDER_HASHES = {sha(value.encode()) for value in (
    'INSERT_API_KEY_HERE', 'INSERT_YOUR_API_KEY_HERE', 'YOUR_API_KEY_HERE', 'INSERT_API_KEY')}
# The remaining reviewed source value contains only the words INSERT/API/KEY/HERE.
PLACEHOLDER_HASHES.add('3489543a5b514255afdfb3853351dfec59e3ad004f632147cc9fc3f08c1f8954')


def admitted_document_url(url):
    safe_reference(url)
    parsed = urlsplit(url)
    if (parsed.hostname != 'docs.os.uk' or parsed.query or parsed.fragment
            or not parsed.path.startswith(('/os-apis/', '/osngd/', '/os-downloads/'))
            or not (parsed.path.endswith('.md') or parsed.path.endswith('/llms.txt'))):
        raise ValueError('Original document route is outside the admitted profile')
    allowed(url)
    return url


def credential_check(raw, patterns):
    text = raw.decode('utf-8'); placeholders = 0

    def reviewed(match):
        nonlocal placeholders
        quoted = re.search(r'["\']([^"\']+)["\']$', match.group())
        if quoted and sha(quoted[1].encode()) in PLACEHOLDER_HASHES:
            placeholders += 1
            return ''
        return match.group()

    inspected = patterns['assigned secret'].sub(reviewed, text)
    if any(pattern.search(inspected) for pattern in patterns.values()):
        raise ValueError('Unreviewed credential or machine-path pattern in an original document')
    return placeholders


def specification_source(entry):
    key = (entry.get('repository'), entry.get('commit'), entry.get('repositoryPath'))
    if key not in SPECIFICATIONS or entry.get('sha256') != SPECIFICATIONS[key] or entry.get('status') != 200:
        raise ValueError('Specification does not match a reviewed official source pin')
    repository, commit, path = key
    expected = {'https://raw.githubusercontent.com/' + repository.removeprefix('https://github.com/') + '/' + commit + '/' + path,
                repository + '/blob/' + commit + '/' + path}
    if entry.get('sourceUrl') not in expected:
        raise ValueError('Specification URL does not match its official source pin')
    safe_reference(entry['sourceUrl'])


def collect(root):
    """Read one ledger snapshot; never write it or infer absent originals."""
    ledger_raw = read_file(root, 'artifacts/okf-plus/capture/ledger.json')
    ledger = load_json(ledger_raw.decode()); patterns = public_patterns(root)
    files = {}; provenance = []; total = 0; seen = set()
    for receipt in ledger['requests']:
        if receipt.get('status') != 200 or urlsplit(receipt.get('url', '')).hostname != 'docs.os.uk':
            continue
        admitted_document_url(receipt['url'])
        if receipt.get('finalUrl', receipt['url']) != receipt['url']:
            raise ValueError('Redirected original requires a separately reviewed source receipt')
        identity = (receipt['url'], receipt.get('sha256'), receipt.get('retrievedAt'))
        if identity in seen:
            continue
        seen.add(identity)
        raw = captured_bytes(root, receipt)
        if len(raw) > MAX_DOCUMENT_BYTES:
            raise ValueError('Original documentation exceeds the per-file byte ceiling')
        placeholders = credential_check(raw, patterns)
        suffix = '.txt' if urlsplit(receipt['url']).path.endswith('/llms.txt') else '.md'
        path = 'documentation/' + sha(canonical(identity)) + suffix
        total += len(raw)
        if len(files) >= MAX_DOCUMENTS or total > MAX_TOTAL_BYTES:
            raise ValueError('Original-document count or total byte ceiling exceeded')
        files[path] = raw
        provenance.append({'path': path, 'sourceUrl': receipt['url'], 'retrievedAt': receipt['retrievedAt'],
            'bytes': len(raw), 'sha256': sha(raw), 'sourceKind': 'official-documentation-original',
            'reviewedExamplePlaceholders': placeholders,
            'rights': {'status': 'source-rights-retained',
                       'note': 'Owner-private retained original; no public publication or blanket re-licensing.'}})
    specification_manifest = root / 'artifacts/okf-plus/specifications/manifest.json'
    gaps = []
    if specification_manifest.exists():
        document = load_json(read_file(root, specification_manifest.relative_to(root).as_posix()).decode())
        if document.get('schema') != 'gis-ai-go.okf-plus-retained-specifications.v1':
            raise ValueError('Unrecognised retained-specification manifest')
        gaps = document.get('gaps', [])
        for entry in document['files']:
            specification_source(entry)
            raw = read_file(root, 'artifacts/okf-plus/specifications/' + safe_path(entry['path']))
            if len(raw) > MAX_DOCUMENT_BYTES or sha(raw) != entry['sha256'] or len(raw) != entry['bytes']:
                raise ValueError('Retained specification digest or byte count mismatch')
            placeholders = credential_check(raw, patterns)
            path = 'specifications/' + sha(canonical([entry['sourceUrl'], entry['sha256']])) + '.yaml'
            if path in files:
                raise ValueError('Duplicate retained specification identity')
            total += len(raw)
            if len(files) >= MAX_DOCUMENTS or total > MAX_TOTAL_BYTES:
                raise ValueError('Original-document count or total byte ceiling exceeded')
            files[path] = raw
            provenance.append({**{key: entry[key] for key in ('sourceUrl', 'retrievedAt', 'bytes', 'sha256', 'rights', 'repository', 'commit', 'repositoryPath')},
                               'path': path, 'sourceKind': 'official-pinned-specification-original',
                               'reviewedExamplePlaceholders': placeholders})
    if not files or len(files) > MAX_DOCUMENTS or total > MAX_TOTAL_BYTES:
        raise ValueError('Empty or oversized original-document hand-off')
    return files, {'ledgerSha256': sha(ledger_raw), 'provenance': sorted(provenance, key=lambda item: item['path']),
                   'specificationGaps': gaps}


def export_documents(root, output):
    root = Path(root).resolve(); output = Path(output).resolve()
    if not output.is_relative_to(root / 'artifacts/okf-plus/export'):
        raise ValueError('Private originals must stay in the ignored export directory')
    files, evidence = collect(root)
    files['PRIVATE_README.md'] = (
        '# Private original documentation hand-off\n\n'
        'Owner-only retained originals. No public publication or upload is authorised by this archive. '
        'Source rights remain applicable. Statistical, catalogue, feature and account response payloads are excluded.\n\n'
        'Each original is bound to its successful source receipt or reviewed immutable specification pin. '
        'Public guide examples may contain reviewed literal key placeholders; actual credentials are forbidden. '
        'Missing specifications stay listed as gaps. API operations described in a guide do not grant invocation authority.\n\n'
        'Verify without extracting: `python scripts/okf_plus/export_documents.py --verify PRIVATE-original-documents.tar.gz`.\n'
    ).encode()
    entries = [{'path': path, 'bytes': len(raw), 'sha256': sha(raw)} for path, raw in sorted(files.items())]
    manifest = {'schema': SCHEMA, 'publication': 'owner-private-no-publication',
                'fileCount': len(entries), 'payloadBytes': sum(e['bytes'] for e in entries),
                'files': entries, **evidence,
                'limits': {'maxDocuments': MAX_DOCUMENTS, 'maxDocumentBytes': MAX_DOCUMENT_BYTES,
                           'maxTotalBytes': MAX_TOTAL_BYTES}}
    files[MANIFEST] = canonical(manifest)
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.private-documents-', dir=output) as directory:
        stage = Path(directory)
        archive_path = stage / 'PRIVATE-original-documents.tar.gz'
        with archive_path.open('wb') as handle, gzip.GzipFile(filename='', fileobj=handle, mode='wb', mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode='w|', format=tarfile.PAX_FORMAT) as archive:
                for path, raw in sorted(files.items()):
                    info = tarfile.TarInfo(path); info.size = len(raw); info.mode = 0o600
                    info.mtime = 0; info.uid = info.gid = 0; info.uname = info.gname = ''
                    archive.addfile(info, io.BytesIO(raw))
        verify_archive(archive_path, SCHEMA)
        with archive_path.open('rb') as handle:
            archive_hash = hashlib.file_digest(handle, 'sha256').hexdigest()
        receipt = {'schema': 'gis-ai-go.okf-plus-private-document-export-receipt.v1',
            'status': 'verified', 'publication': 'owner-private-no-publication',
            'archive': {'path': archive_path.name, 'bytes': archive_path.stat().st_size, 'sha256': archive_hash},
            'manifest': {'path': 'PRIVATE-original-documents-manifest.json', 'bytes': len(files[MANIFEST]), 'sha256': sha(files[MANIFEST])},
            'originalDocuments': len(evidence['provenance']), 'networkRequests': 0}
        (stage / receipt['manifest']['path']).write_bytes(files[MANIFEST])
        (stage / 'PRIVATE-original-documents-receipt.json').write_bytes(canonical(receipt))
        for path in stage.iterdir():
            os.chmod(path, 0o600)
            target = output / path.name
            if target.is_symlink() or (target.exists() and not target.is_file()):
                raise ValueError('Private export destination is not a regular file')
        for path in stage.iterdir():
            path.replace(output / path.name)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'artifacts/okf-plus/export')
    parser.add_argument('--verify', type=Path)
    args = parser.parse_args()
    if args.verify:
        manifest = verify_archive(args.verify, SCHEMA)
        print(json.dumps({'status': 'verified', 'publication': manifest['publication'], 'fileCount': manifest['fileCount']}))
    else:
        print(json.dumps(export_documents(ROOT, args.output)))


if __name__ == '__main__':
    main()
