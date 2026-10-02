#!/usr/bin/env python3
"""Build and verify all retained OKF+ metadata offline, with separate open gates.

No capture, browser, model or service-registration operation is performed.
Exit 0 means the declared automated checks passed; four context-required review
questions and hosted Ask OKF acceptance remain explicitly unassessed.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import gc
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import traceback
from urllib.parse import urlsplit

try:
    from .context_projection import (EXPLORER_REVISION, VENDOR_MANIFEST_SHA256, canonical,
        install, pinned_contract, project, sha, validate_outputs, verify_engine)
    from .model import load_json
    from .search import evaluate_cases, load_index
except ImportError:
    from context_projection import (EXPLORER_REVISION, VENDOR_MANIFEST_SHA256, canonical,
        install, pinned_contract, project, sha, validate_outputs, verify_engine)
    from model import load_json
    from search import evaluate_cases, load_index

ROOT = Path(__file__).resolve().parents[2]
MAX_REPORT_BYTES = 1024 * 1024
MAX_BUNDLE_BYTES = 256 * 1024 * 1024
MAX_DIAGNOSTIC_BYTES = 64 * 1024
OFFLINE_SCRIPT_WRAPPER = '''import pathlib,runpy,sys
def deny(event,args):
    if event in ('socket.connect','socket.getaddrinfo','urllib.Request'):
        raise RuntimeError('Network forbidden during offline verification')
sys.addaudithook(deny)
sys.argv=sys.argv[1:]
sys.path.insert(0,str(pathlib.Path(sys.argv[0]).resolve().parent))
runpy.run_path(sys.argv[0],run_name='__main__')
'''


def _file_ref(path, base):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        while raw := handle.read(1024 * 1024):
            digest.update(raw)
    return {'path': path.relative_to(base).as_posix(), 'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}


def _write(path, value, base=None):
    raw = canonical(value) + b'\n'
    if len(raw) > MAX_REPORT_BYTES:
        raise ValueError('Verification report exceeds its byte ceiling')
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.verification-', delete=False) as temporary:
        temporary.write(raw)
        temporary_path = Path(temporary.name)
    try:
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)
    return {'path': path.relative_to(base).as_posix() if base else path.name, 'bytes': len(raw), 'sha256': sha(raw)}


class Checkpoints:
    """Bounded, atomic stage snapshots; timing completion is not a passed gate."""

    def __init__(self, output, report):
        self.output, self.report = output, report
        self.started = self.stage_started = time.monotonic()
        self.active = None
        report['timing'] = {'basis': 'monotonic-seconds', 'elapsedSeconds': 0, 'stages': {}}

    def _finish_stage(self, now, state):
        if self.active is not None:
            seconds = round(now - self.stage_started, 3)
            self.report['timing']['stages'][self.active] = {'state': state, 'elapsedSeconds': seconds}
            print(f'OKF+ verification: {self.active} {state} ({seconds:.1f}s)', flush=True)

    def enter(self, stage):
        now = time.monotonic()
        self._finish_stage(now, 'finished')
        self.active, self.stage_started = stage, now
        self.report['activeStage'] = stage
        self.report['timing']['elapsedSeconds'] = round(now - self.started, 3)
        self.report['timing']['stages'][stage] = {'state': 'running', 'elapsedSeconds': 0}
        _write(self.output / 'verification.json', self.report)
        print(f'OKF+ verification: {stage} started', flush=True)
        return stage

    def finish(self, *, failed):
        now = time.monotonic()
        self._finish_stage(now, 'failed' if failed else 'finished')
        self.report['activeStage'] = None
        self.report['timing']['elapsedSeconds'] = round(now - self.started, 3)
        _write(self.output / 'verification.json', self.report)


def _private_diagnostic(output, stage, error, process_stderr=b''):
    """Keep bounded details locally; never add this file to export artefacts."""
    if isinstance(process_stderr, str):
        process_stderr = process_stderr.encode()
    frames = ''.join(traceback.format_tb(error.__traceback__)).encode()
    # jsonschema errors expose a concise message separately from their expanded
    # source/schema dump. No diagnostic text enters the public machine report.
    detail = getattr(error, 'message', None)
    message = str(detail if detail is not None else error).encode(errors='replace')
    raw = frames + type(error).__name__.encode() + b': ' + message + b'\n' + process_stderr
    truncated = len(raw) > MAX_DIAGNOSTIC_BYTES
    if truncated:
        marker = b'\n[private diagnostic truncated to a bounded head and tail]\n'
        half = (MAX_DIAGNOSTIC_BYTES - len(marker)) // 2
        raw = raw[:half] + marker + raw[-half:]
    directory = output / 'private-diagnostics'
    if directory.is_symlink():
        raise ValueError('Private diagnostic directory must not be a symlink')
    directory.mkdir(exist_ok=True)
    path = directory / (stage + '.log')
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, 'O_NOFOLLOW', 0)
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, 'wb') as handle:
        os.fchmod(handle.fileno(), 0o600)
        handle.write(raw)
    return {'path': path.relative_to(output).as_posix(), 'bytes': len(raw), 'sha256': sha(raw),
            'truncated': truncated, 'visibility': 'local-only-not-an-export-artefact'}


def retrieval_gate(report):
    """Do not count the four explicitly unrun semantic cases as passes."""
    counts = report['counts']
    if (counts['cases'] != 40 or counts['notEvaluatedContextRequired'] != 4
            or counts['passedRetrieval'] + counts['failedRetrieval'] != 36):
        raise ValueError('Question-suite denominator or context-review boundary changed')
    return {'status': 'passed' if counts['failedRetrieval'] == 0 else 'failed',
            'counts': counts, 'failedCaseIds': [r['id'] for r in report['cases'] if r['status'] == 'failed'],
            'unassessedContextCaseIds': [r['id'] for r in report['cases']
                                        if r['status'] == 'not-evaluated-context-required']}


def representative_cases(search, projection):
    """Choose real bound records, not synthetic replacements or retrieval seeds."""
    rows = sorted(search['records'], key=lambda row: row['id'])
    selected = set(projection['representativeIndex']['selectedInputIds'])
    candidates = [(ordinal, row) for ordinal, row in enumerate(rows)
                  if ordinal >= 16 and row['id'] not in selected and row['sourceFamily'] == 'ons-datasets'
                  and re.fullmatch(r'[A-Za-z0-9_-]{3,100}', row['nativeIdentifier'])
                  and len(re.findall(r'[A-Za-z0-9]{2,}', row['nativeIdentifier'])) <= 8]
    if not candidates:
        raise ValueError('No real ONS identifier beyond the representative shortlist')
    ordinal, tail = candidates[-1]
    cadence = next((row for row in rows if row['sourceFamily'] == 'ons-datasets'
                    and row['nativeIdentifier'] == 'cpih01'
                    and row['update']['frequency'].get('label') and row['update'].get('releaseFeed')), None)
    if cadence is None:
        raise ValueError('Bound cpih01 cadence/feed record required for the declared check')
    required = [canonical(cadence['update']['frequency']).decode(),
                canonical(cadence['update']['releaseFeed']).decode(),
                canonical(cadence['rights']).decode(), canonical(cadence['temporal']).decode()]
    return [
        {'id': 'full-corpus-tail-identifier', 'question': tail['nativeIdentifier'], 'expectedId': tail['id'],
         'requiredText': [tail['nativeIdentifier'], canonical(tail['update']).decode()],
         'selectionEvidence': {'canonicalOrdinal': ordinal, 'outsideRepresentativeIndex': True}},
        {'id': 'cadence-feed-rights', 'question': 'cpih01 metadata', 'expectedId': cadence['id'],
         'requiredText': required, 'selectionEvidence': {'sourceFamily': cadence['sourceFamily'],
                                                       'nativeIdentifier': cadence['nativeIdentifier']}},
        {'id': 'unsupported-observation-answer', 'question': "Retrieve today's actual cpih01 observation values",
         'expectInsufficient': True},
        {'id': 'unknown-question', 'question': 'quasar zygomorphic unobtainium',
         'expectInsufficient': True, 'expectEmpty': True},
    ]


def audit_complete_corpus(search, bundle, outputs):
    """Independently inspect every emitted record/card and complete source passage."""
    manifest = load_json(outputs['manifest.json'].decode())
    sources = {row['id']: row for row in search['records']}
    semantic = {row['@id']: row for row in bundle['records']}
    seen = set(); card_ids = set(); record_hashes = {}; passage_bytes = 0
    for reference in manifest['records']['shards']:
        raw = outputs[reference['path']]; decoded = gzip.decompress(raw)
        if sha(raw) != reference['sha256'] or sha(decoded) != reference['decoded_sha256']:
            raise ValueError('Record shard integrity mismatch')
        records = load_json(decoded.decode())['records']
        if len(records) != reference['count']:
            raise ValueError('Record shard denominator mismatch')
        for record in records:
            identifier = record['id']
            if identifier in seen or identifier not in sources:
                raise ValueError('Unexpected or duplicate corpus identity')
            seen.add(identifier); row = sources[identifier]
            expected = row['text'] + '\n\nOKF+ complete retained semantic metadata (JSON):\n' + canonical(semantic[identifier]).decode() + '\n'
            if record['text'] != expected:
                raise ValueError('Whole source metadata omitted or altered in context evidence')
            unit = record['evidence_unit']; span = unit['spans'][0]; raw_text = expected.encode()
            prefix = urlsplit(manifest['bundle']['source_url']); passage = urlsplit(span['source_url'])
            directory = prefix.path.rsplit('/', 1)[0] + '/'
            if (passage.scheme != prefix.scheme or passage.netloc != prefix.netloc
                    or not passage.path.startswith(directory) or passage.query or passage.fragment):
                raise ValueError('Passage escapes corpus publication binding')
            relative = passage.path.removeprefix(directory)
            if (len(unit['spans']) != 1 or span['unit_start'] != 0 or span['unit_end'] != len(raw_text)
                    or span['literal_sha256'] != sha(raw_text) or outputs.get(relative) != raw_text):
                raise ValueError('Complete passage integrity mismatch')
            passage_bytes += len(raw_text); record_hashes[identifier] = sha(canonical(record))
    for reference in manifest['discovery']['shards']:
        raw = outputs[reference['path']]; decoded = gzip.decompress(raw)
        if sha(raw) != reference['sha256'] or sha(decoded) != reference['decoded_sha256']:
            raise ValueError('Discovery shard integrity mismatch')
        cards = load_json(decoded.decode())['cards']
        if len(cards) != reference['count']:
            raise ValueError('Discovery shard denominator mismatch')
        for card in cards:
            identifier = card['evidence_id']
            if identifier in card_ids or card['evidence_sha256'] != record_hashes.get(identifier):
                raise ValueError('Missing, duplicate or stale discovery binding')
            card_ids.add(identifier)
    if (seen != set(sources) or seen != set(semantic) or card_ids != seen
            or manifest['records']['count'] != len(seen) or manifest['discovery']['count'] != len(seen)):
        raise ValueError('Whole-corpus denominator or identity mismatch')
    return {'status': 'passed-every-record-and-card', 'inputRecords': len(sources),
            'evidenceRecords': len(seen), 'discoveryCards': len(card_ids), 'completePassageBytes': passage_bytes,
            'omittedRecords': 0, 'omittedSemanticFields': 0}


def run_verification(root, output, revision, captured_at):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output == root or output.is_relative_to(root / 'okf-plus'):
        raise ValueError('Verification output must not overwrite source files')
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('A full Git source revision is required')
    output.mkdir(parents=True, exist_ok=True)
    report = {'schema': 'gis-ai-go.okf-plus-offline-verification.v1', 'status': 'running',
              'sourceRevision': revision, 'sourceState': 'working-tree-input-digest', 'capturedAt': captured_at,
              'implementationSha256': sha(Path(__file__).read_bytes()), 'explorerRevision': EXPLORER_REVISION,
              'vendorManifestSha256': VENDOR_MANIFEST_SHA256,
              'networkPolicy': 'Python network audit denial and pinned-engine fetch denial; no capture operation',
              'installedAskOkfAdmission': 'not-established', 'stages': {}}
    checkpoint = Checkpoints(output, report)
    stage = checkpoint.enter('importer-check'); exit_code = 2; diagnostic_stderr = b''
    try:
        imported = subprocess.run([sys.executable, '-c', OFFLINE_SCRIPT_WRAPPER,
                                   str(root / 'scripts/okf_plus/import_sources.py'), '--check'],
                                  cwd=root, capture_output=True, timeout=1800)
        report['stages']['importer'] = {'status': 'passed' if imported.returncode == 0 else 'failed',
            'exitCode': imported.returncode, 'stdoutSha256': sha(imported.stdout), 'stderrSha256': sha(imported.stderr)}
        if imported.returncode:
            diagnostic_stderr = imported.stderr
            raise RuntimeError('Source-to-Markdown consistency check failed')
        stage = checkpoint.enter('build')
        built = subprocess.run([sys.executable, '-c', OFFLINE_SCRIPT_WRAPPER, str(root / 'scripts/okf_plus/build.py'),
                                '--output', str(output / 'bundle'), '--revision', revision],
                               cwd=root, capture_output=True, timeout=1800)
        report['stages']['build'] = {'status': 'passed' if built.returncode == 0 else 'failed',
            'exitCode': built.returncode, 'stdoutSha256': sha(built.stdout), 'stderrSha256': sha(built.stderr)}
        if built.returncode:
            diagnostic_stderr = built.stderr
            raise RuntimeError('Source build failed')
        stage = checkpoint.enter('retrieval-evaluation')
        search_path = output / 'bundle/search-index.json'; bundle_path = output / 'bundle/okf-bundle.json'
        search = load_index(search_path)
        with bundle_path.open('rb') as handle:
            bundle_raw = handle.read(MAX_BUNDLE_BYTES + 1)
        if len(bundle_raw) > MAX_BUNDLE_BYTES:
            raise ValueError('Bundle exceeds offline verification byte ceiling')
        bundle = load_json(bundle_raw.decode()); del bundle_raw
        if search.get('revision') != revision or bundle.get('revision') != revision:
            raise ValueError('Built input revision differs from admitted source revision')
        question_path = root / 'okf-plus/evaluation/questions.json'; questions_raw = question_path.read_bytes()
        questions = load_json(questions_raw.decode()); evaluation = evaluate_cases(search, questions)
        gate = retrieval_gate(evaluation); report['stages']['retrieval'] = gate
        report['questionCorpusFileSha256'] = sha(questions_raw)
        report['inputDigest'] = search['inputDigest']; report['searchIndexSha256'] = evaluation['indexSha256']
        transferred = {key: _file_ref(path, output) for key, path in
                       (('search', search_path), ('bundle', bundle_path))}
        report['transferredInputs'] = transferred
        report['retrievalReport'] = _write(output / 'retrieval-evaluation.json', evaluation)
        gc.collect()
        stage = checkpoint.enter('whole-corpus-projection')
        outputs, projection = project(search, bundle,
            base_url='https://chris-page-gov.github.io/gis-ai-go/okf-plus/context/', captured_at=captured_at)
        stage = checkpoint.enter('all-record-schema-validation')
        checks, schema_hashes = pinned_contract(); validation = validate_outputs(outputs, checks)
        validation.update(explorerRevision=EXPLORER_REVISION, vendorManifestSha256=VENDOR_MANIFEST_SHA256,
                          schemaFileSha256=schema_hashes,
                          transferredInputSha256={key: value['sha256'] for key, value in transferred.items()})
        stage = checkpoint.enter('whole-corpus-audit')
        audit = audit_complete_corpus(search, bundle, outputs)
        if validation['allEvidenceRecordsValidated'] != audit['inputRecords']:
            raise ValueError('Schema validation denominator differs from complete corpus')
        report['stages']['wholeCorpus'] = {**audit, 'schemaEvidenceRecords': validation['allEvidenceRecordsValidated'],
            'corpusManifestSha256': sha(outputs['manifest.json']),
            'projectionManifestSha256': sha(outputs['projection-manifest.json']),
            'inputSearchSha256': projection['inputSearchSha256'], 'inputBundleSha256': projection['inputBundleSha256']}
        outputs['schema-validation.json'] = canonical(validation)
        stage = checkpoint.enter('context-installation')
        install(outputs, output / 'context')
        cases = representative_cases(search, projection)
        report['contextCases'] = _write(output / 'context-cases.json', cases)
        del outputs, search, bundle; gc.collect()
        stage = checkpoint.enter('pinned-engine-evaluation')
        engine = verify_engine(output / 'context', cases)
        report['engineReport'] = _write(output / 'context/engine-validation.json', engine, output)
        report['stages']['contextEngine'] = {'status': engine['status'], 'cases': len(engine['results']),
                                          'networkCalls': engine['networkCalls']}
        report['status'] = 'passed-automated-checks' if gate['status'] == 'passed' else 'failed-retrieval-checks'
        report['artifacts'] = {key: _file_ref(output / path, output) for key, path in (
            ('bundleChecksums', 'bundle/checksums.json'), ('sourceLock', 'bundle/source-lock.json'),
            ('retrievalReport', 'retrieval-evaluation.json'), ('contextEntrypoints', 'context/descriptor-entrypoints.json'),
            ('contextSchemaReport', 'context/schema-validation.json'), ('contextEngineReport', 'context/engine-validation.json'),
            ('contextCases', 'context-cases.json'))}
        exit_code = 0 if gate['status'] == 'passed' else 1
    except Exception as error:
        report.update(status='failed', failure={'stage': stage, 'errorType': type(error).__name__})
        # Retain diagnostic identity, never absolute paths, source bodies or
        # unbounded subprocess logs in the report.
        if isinstance(error, subprocess.CalledProcessError):
            report['failure']['stderrSha256'] = sha((error.stderr or '').encode() if isinstance(error.stderr, str) else (error.stderr or b''))
            diagnostic_stderr = error.stderr or b''
        report['failure']['message'] = 'Verification stopped during ' + stage + '; inspect the bounded private diagnostic for details.'
        try:
            report['failure']['privateDiagnostic'] = _private_diagnostic(output, stage, error, diagnostic_stderr)
        except (OSError, ValueError):
            report['failure']['privateDiagnosticStatus'] = 'could-not-write-local-diagnostic'
    report['limitations'] = ['Four context-required question-suite cases are separately unassessed, not passes.',
        'Engine probes check complete metadata retrieval and insufficiency, not generated-answer quality.',
        'No hosted publication, installed Ask OKF admission, provider access or licence entitlement is established.']
    checkpoint.finish(failed='failure' in report)
    return report, exit_code


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'artifacts/okf-plus')
    parser.add_argument('--revision')
    parser.add_argument('--captured-at')
    args = parser.parse_args(argv)
    revision = args.revision or subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    captured_at = args.captured_at or datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    def deny(event, _args):
        if event in ('socket.connect', 'socket.getaddrinfo', 'urllib.Request'):
            raise RuntimeError('Network forbidden during offline verification')
    sys.addaudithook(deny)
    report, code = run_verification(ROOT, args.output, revision, captured_at)
    print(json.dumps({'status': report['status'], 'sourceRevision': revision,
                      'failureStage': report.get('failure', {}).get('stage'),
                      'unassessedContextCases': report.get('stages', {}).get('retrieval', {}).get('unassessedContextCaseIds', [])}))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
