#!/usr/bin/env python3
"""Create and verify a deterministic, public-only OKF+ metadata hand-off."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path, PurePosixPath
import re
import tarfile
import tempfile

from model import canonical, digest, load_json
from build import source_inputs

ROOT = Path(__file__).resolve().parents[2]
MARKER = 'gis-ai-go.okf-plus-export.v1\n'
MAX_FILE = 256 * 1024 * 1024
MAX_TOTAL = 2 * 1024 * 1024 * 1024
MAX_FILES = 100_000
MANIFEST = 'EXPORT_MANIFEST.json'
FIXED = ('LICENSE', '.nvmrc', 'pyproject.toml', 'uv.lock', 'package.json', 'pnpm-lock.yaml',
         'services/geo-execution/pyproject.toml', 'scripts/scan_secrets.py')
DIRECTORIES = ('okf-plus', 'scripts/okf_plus')
SUFFIXES = {'.md', '.json', '.jsonld', '.yamlld', '.yaml', '.yml', '.ttl', '.py', '.ts', '.toml', '.txt'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def safe_path(value):
    if (not isinstance(value, str) or not value or '\\' in value
            or any(ord(c) < 32 or ord(c) == 127 for c in value)):
        raise ValueError('Invalid export path')
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in ('', '.', '..') for p in value.split('/')) or ':' in value:
        raise ValueError('Export paths must be safe relative paths')
    return value


def read_file(root, relative):
    relative = safe_path(relative)
    path = root / relative
    if (not path.resolve().is_relative_to(root.resolve())
            or any(p.is_symlink() for p in [path, *path.parents] if p != root and p.is_relative_to(root))):
        raise ValueError('Export input contains a symbolic link or escapes the root')
    if not path.is_file() or path.stat().st_size > MAX_FILE:
        raise ValueError('Missing or oversized export input')
    with path.open('rb') as handle:
        raw = handle.read(MAX_FILE + 1)
    if len(raw) > MAX_FILE:
        raise ValueError('Export input exceeds byte ceiling')
    return raw


def source_paths(root):
    paths = set(FIXED)
    for directory in DIRECTORIES:
        base = root / directory
        if not base.is_dir() or base.is_symlink():
            raise ValueError('Required source directory is missing or symbolic')
        for path in base.rglob('*'):
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                raise ValueError('Symbolic source path is forbidden')
            if '__pycache__' in path.parts:
                continue
            if path.is_file():
                if path.suffix not in SUFFIXES:
                    raise ValueError('Unexpected source file type; review before export')
                paths.add(relative)
    paths.update(p.relative_to(root).as_posix() for p in (root / 'docs/implementation').glob('OKF-220*.md'))
    paths.update(p.relative_to(root).as_posix() for p in (root / 'tests/contract').glob('test_okf_plus*.py'))
    paths.update(p.relative_to(root).as_posix() for p in (root / 'tests').glob('test_okf_plus*.py'))
    for relative in paths:
        if any(p in ('.git', '.env', 'capture', 'secrets', 'node_modules') for p in PurePosixPath(relative).parts):
            raise ValueError('Private or unrelated input is forbidden')
    return sorted(paths)


def check_reference(root, reference):
    raw = read_file(root, reference['path'])
    if sha(raw) != reference['sha256'] or len(raw) != reference['bytes']:
        raise ValueError('Verified artefact reference no longer matches its bytes')
    return raw


def verified_generated(root, generated, included_sources):
    """Verify the final report and all source/bundle/context digest chains."""
    report = load_json(read_file(generated, 'verification.json').decode())
    if (report.get('schema') != 'gis-ai-go.okf-plus-offline-verification.v1'
            or report.get('status') != 'passed-automated-checks'):
        raise ValueError('Generated export requires passed automated verification')
    stages = report['stages']; counts = stages['retrieval']['counts']
    if (stages['importer']['status'] != 'passed' or stages['build']['status'] != 'passed' or stages['retrieval']['status'] != 'passed'
            or counts != {'cases': 40, 'passedRetrieval': 36, 'failedRetrieval': 0,
                          'notEvaluatedContextRequired': 4}
            or stages['contextEngine'] != {'status': 'passed', 'cases': 4, 'networkCalls': 0}):
        raise ValueError('Generated verification gate is incomplete')
    whole = stages['wholeCorpus']
    if (whole['status'] != 'passed-every-record-and-card' or whole['omittedRecords'] != 0
            or whole['omittedSemanticFields'] != 0 or whole['inputRecords'] < 1
            or any(whole[k] != whole['inputRecords'] for k in ('evidenceRecords', 'discoveryCards', 'schemaEvidenceRecords'))):
        raise ValueError('Whole-corpus verification is incomplete')
    required = {'bundle/checksums.json', 'bundle/source-lock.json', 'retrieval-evaluation.json',
                'context/descriptor-entrypoints.json', 'context/schema-validation.json',
                'context/engine-validation.json', 'context-cases.json'}
    references = report.get('artifacts', {})
    if not isinstance(references, dict) or {r['path'] for r in references.values()} != required or len(references) != len(required):
        raise ValueError('Final verification artefact inventory is incomplete')
    for reference in references.values():
        check_reference(generated, reference)
    transferred = report.get('transferredInputs', {})
    if (set(transferred) != {'search', 'bundle'} or transferred['search']['path'] != 'bundle/search-index.json'
            or transferred['bundle']['path'] != 'bundle/okf-bundle.json'):
        raise ValueError('Verified bundle/search input references are incomplete')
    for reference in transferred.values():
        check_reference(generated, reference)
    if report['implementationSha256'] != sha(read_file(root, 'scripts/okf_plus/verify.py')):
        raise ValueError('Verification implementation has changed')
    if report['questionCorpusFileSha256'] != sha(read_file(root, 'okf-plus/evaluation/questions.json')):
        raise ValueError('Evaluation questions have changed')
    checksums = load_json(read_file(generated, 'bundle/checksums.json').decode())
    bundle_paths = {'bundle/' + safe_path(p) for p in checksums} | {'bundle/checksums.json'}
    actual = {p.relative_to(generated).as_posix() for p in (generated / 'bundle').rglob('*') if p.is_file()}
    if actual != bundle_paths:
        raise ValueError('Generated bundle file inventory differs')
    for path, checksum in checksums.items():
        if sha(read_file(generated, 'bundle/' + path)) != checksum:
            raise ValueError('Generated bundle checksum mismatch')
    lock = load_json(read_file(generated, 'bundle/source-lock.json').decode())
    if (lock['revision'] != report['sourceRevision'] or lock['sha256'] != report['inputDigest']
            or digest(lock['inputs']) != lock['sha256']):
        raise ValueError('Generated source identity differs')
    if lock['inputs'] != source_inputs(root):
        raise ValueError('Current build input inventory differs from verified source lock')
    for entry in lock['inputs']:
        if entry['path'] not in included_sources or sha(read_file(root, entry['path'])) != entry['sha256']:
            raise ValueError('Generated source lock is stale or not included in the hand-off')
    descriptor = load_json(read_file(generated, 'context/descriptor-entrypoints.json').decode())
    context = generated / 'context'
    for reference in [*descriptor['entrypoints'].values(), descriptor['projectionManifest']]:
        check_reference(context, reference)
    projection_raw = read_file(context, 'projection-manifest.json')
    projection = load_json(projection_raw.decode())
    if (sha(projection_raw) != whole['projectionManifestSha256']
            or sha(read_file(context, 'manifest.json')) != whole['corpusManifestSha256']
            or projection['inputDigest'] != report['inputDigest']
            or projection['sourceRevision'] != report['sourceRevision']):
        raise ValueError('Context projection identity differs')
    for reference in projection['outputs']:
        check_reference(context, reference)
    context_paths = {'context/' + r['path'] for r in projection['outputs']} | {
        'context/projection-manifest.json', 'context/descriptor-entrypoints.json',
        'context/schema-validation.json', 'context/engine-validation.json'}
    paths = bundle_paths | context_paths | {'verification.json', 'retrieval-evaluation.json', 'context-cases.json'}
    return sorted(paths), report


def public_patterns(root):
    spec = importlib.util.spec_from_file_location('okf_plus_export_secret_patterns', root / 'scripts/scan_secrets.py')
    if spec is None or spec.loader is None:
        raise ValueError('Public export scanner is unavailable')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module.PATTERNS


def check_public(raw, relative, patterns):
    if relative.endswith('.gz'):
        with gzip.GzipFile(fileobj=io.BytesIO(raw)) as handle:
            raw = handle.read(MAX_FILE + 1)
        if len(raw) > MAX_FILE:
            raise ValueError('Decoded export input exceeds byte ceiling')
    text = raw.decode('utf-8')
    if any(pattern.search(text) for pattern in patterns.values()):
        raise ValueError('Secret or machine-path pattern in export input; review locally')


def readme(revision, generated):
    return (f'# OKF+ metadata hand-off\n\nSource revision: `{revision}`.\n\n'
        'This archive contains public metadata and source code. It contains no private capture cache. '
        'Native source rights and limitations remain in the records. Metadata discovery does not grant data access.\n\n'
        'Verify with `python scripts/okf_plus/export.py --verify path-to-archive.tar.gz`. '
        'The manifest lists each payload file; its own digest and the archive digest are in the adjacent export receipt.\n\n'
        'Python 3.12 or later, uv and the Node version in `.nvmrc` are prerequisites. '
        'The minimal service pyproject is included only to resolve the pinned uv workspace. '
        'The package manifests record source dependencies; unrelated repository commands are outside this hand-off.\n\n'
        f'Offline verification: `uv run --locked python scripts/okf_plus/verify.py --revision {revision}`. '
        'Initial dependency provisioning may need network access; the verifier denies provider network requests. '
        'Do not run harvest or locator-freeze commands to reproduce the frozen source build.\n\n'
        f'Generated artefacts included: {"yes; exact passing report and digest chains checked" if generated else "no; source-only hand-off"}. '
        'Four context-required evaluation cases remain unassessed. Installed Ask OKF admission, publication and live-provider authority are not established by this export.\n').encode()


def verify_archive(path, expected_schema='gis-ai-go.okf-plus-export-manifest.v1'):
    """Inspect and hash regular files without extracting an archive."""
    if Path(path).stat().st_size > MAX_TOTAL:
        raise ValueError('Compressed archive exceeds byte ceiling')
    found = {}; total = 0; manifest = None
    with tarfile.open(path, 'r:gz') as archive:
        for member in archive:
            name = safe_path(member.name)
            if (not member.isfile() or member.issym() or member.islnk() or name in found
                    or not 0 <= member.size <= MAX_FILE or len(found) >= MAX_FILES):
                raise ValueError('Unsafe or oversized archive member')
            total += member.size
            if total > MAX_TOTAL:
                raise ValueError('Archive exceeds total byte ceiling')
            handle = archive.extractfile(member)
            if handle is None:
                raise ValueError('Archive member has no data')
            raw = handle.read(MAX_FILE + 1)
            if len(raw) != member.size:
                raise ValueError('Archive member size mismatch')
            found[name] = {'path': name, 'bytes': len(raw), 'sha256': sha(raw)}
            if name == MANIFEST:
                manifest = load_json(raw.decode())
    if not manifest or manifest.get('schema') != expected_schema:
        raise ValueError('Export manifest is missing or unsupported')
    expected = {item['path']: item for item in manifest['files']}
    if len(expected) != len(manifest['files']) or set(found) != set(expected) | {MANIFEST}:
        raise ValueError('Archive and manifest inventories differ')
    if any(found[name] != item for name, item in expected.items()):
        raise ValueError('Archive payload checksum mismatch')
    if manifest.get('fileCount') != len(expected) or manifest.get('payloadBytes') != sum(e['bytes'] for e in expected.values()):
        raise ValueError('Manifest file or byte count mismatch')
    return manifest


def export(root, output, revision, generated=None):
    root = Path(root).resolve(); output = Path(output).resolve()
    if not re.fullmatch('[0-9a-f]{40}', revision):
        raise ValueError('A full source revision is required')
    if not output.is_relative_to(root / 'artifacts/okf-plus') or output == root / 'artifacts/okf-plus':
        raise ValueError('Export output must be a child of the ignored OKF+ artefact directory')
    if output.exists() and (not (output / '.okf-plus-export').is_file()
                            or (output / '.okf-plus-export').read_text() != MARKER):
        raise ValueError('Refusing to replace an unmarked export output')
    sources = source_paths(root); candidates = {p: (root, p) for p in sources}
    report = None
    if generated is not None:
        generated = Path(generated).resolve()
        paths, report = verified_generated(root, generated, set(sources))
        if report['sourceRevision'] != revision:
            raise ValueError('Requested revision differs from verified output')
        candidates.update({'generated/' + p: (generated, p) for p in paths})
    if len(candidates) + 2 > MAX_FILES:
        raise ValueError('Export file-count ceiling exceeded')
    patterns = public_patterns(root); entries = []; total = 0
    extra = {'EXPORT_README.md': readme(revision, report is not None)}
    for relative in sorted([*candidates, *extra]):
        raw = extra[relative] if relative in extra else read_file(*candidates[relative])
        check_public(raw, relative, patterns)
        total += len(raw)
        if total > MAX_TOTAL:
            raise ValueError('Export payload exceeds total byte ceiling')
        entries.append({'path': relative, 'bytes': len(raw), 'sha256': sha(raw)})
    manifest = {'schema': 'gis-ai-go.okf-plus-export-manifest.v1', 'sourceRevision': revision,
        'generatedStatus': 'verified-automated-checks' if report else 'not-included',
        'verificationSha256': sha(read_file(Path(generated), 'verification.json')) if report else None,
        'fileCount': len(entries), 'payloadBytes': total, 'files': entries,
        'manifestSelfHash': 'Excluded to avoid self-reference; bound by adjacent export receipt.',
        'limits': {'maxFiles': MAX_FILES, 'maxFileBytes': MAX_FILE, 'maxTotalBytes': MAX_TOTAL}}
    extra[MANIFEST] = canonical(manifest)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.okf-plus-export-', dir=output.parent) as directory:
        stage = Path(directory) / 'stage'; stage.mkdir()
        archive_path = stage / 'okf-plus-metadata.tar.gz'
        expected = {e['path']: e for e in entries}
        with archive_path.open('wb') as handle, gzip.GzipFile(filename='', fileobj=handle, mode='wb', mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode='w|', format=tarfile.PAX_FORMAT) as archive:
                for relative in sorted([*candidates, *extra]):
                    raw = extra[relative] if relative in extra else read_file(*candidates[relative])
                    if relative in expected and (sha(raw) != expected[relative]['sha256'] or len(raw) != expected[relative]['bytes']):
                        raise ValueError('Export inputs changed while packaging')
                    info = tarfile.TarInfo(relative); info.size = len(raw); info.mode = 0o644
                    info.mtime = 0; info.uid = info.gid = 0; info.uname = info.gname = ''
                    archive.addfile(info, io.BytesIO(raw))
        verify_archive(archive_path)
        (stage / MANIFEST).write_bytes(extra[MANIFEST])
        with archive_path.open('rb') as handle:
            checksum = hashlib.file_digest(handle, 'sha256').hexdigest()
        receipt = {'schema': 'gis-ai-go.okf-plus-export-receipt.v1', 'status': 'verified',
            'archive': {'path': archive_path.name, 'bytes': archive_path.stat().st_size, 'sha256': checksum},
            'manifest': {'path': MANIFEST, 'bytes': len(extra[MANIFEST]), 'sha256': sha(extra[MANIFEST])},
            'sourceRevision': revision, 'generatedStatus': manifest['generatedStatus']}
        (stage / 'export-receipt.json').write_bytes(canonical(receipt))
        (stage / '.okf-plus-export').write_text(MARKER)
        previous = Path(directory) / 'previous'
        if output.exists():
            output.rename(previous)
        try:
            stage.rename(output)
        except BaseException:
            if previous.exists(): previous.rename(output)
            raise
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'artifacts/okf-plus/export')
    parser.add_argument('--revision')
    parser.add_argument('--generated', type=Path)
    parser.add_argument('--verify', type=Path)
    args = parser.parse_args()
    if args.verify:
        result = verify_archive(args.verify)
        print(json.dumps({'status': 'verified', 'fileCount': result['fileCount'], 'sourceRevision': result['sourceRevision']}))
    else:
        if not args.revision: parser.error('--revision is required for export')
        print(json.dumps(export(ROOT, args.output, args.revision, args.generated)))


if __name__ == '__main__':
    main()
