"""Bounded private recovery supervisor; no workspace-lifetime guarantee.

Owner: repository owner. Policy: only existing frozen documentation capture,
local verification and metadata exporters are invoked; source text is untrusted
and never executed. No credentials are read by this supervisor. Private outputs
are local ignored artefacts, not GitHub publication or proof of runtime survival.
"""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import json
import os
import subprocess
import tempfile
import time
import uuid
from pathlib import Path

from . import os_document_sync as sync, field_cards, field_passages
from .passages import no_symlinks

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = Path('artifacts/okf-plus/private-recovery-supervisor')
RESUMABLE = {None, 'wall-deadline', 'document-batch-ceiling'}


def atomic(path, value):
    path = no_symlinks(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    descriptor, name = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name)
    try:
        with os.fdopen(descriptor, 'w') as stream:
            json.dump(value, stream, indent=2, allow_nan=False)
            stream.flush(); os.fsync(stream.fileno())
        os.replace(name, path)
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try: os.fsync(directory_fd)
        finally: os.close(directory_fd)
    finally:
        Path(name).unlink(missing_ok=True)


def source_head(root):
    result = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root,
                            capture_output=True, text=True, check=True)
    return result.stdout.strip()


def counts(state):
    targets = state['scope']['targets']
    if len(targets) > 3000 or len(set(targets)) != len(targets):
        raise ValueError('Invalid frozen target scope')
    rows = state['records']
    captured = sum(rows.get(url, {}).get('status') == 'captured' for url in targets)
    failed = sum(rows.get(url, {}).get('status') == 'failed' for url in targets)
    return {'requested': len(targets), 'processed': captured + failed,
            'captured': captured, 'failed': failed, 'unresolved': len(targets) - captured - failed}


def audit_captured(root, state):
    private = no_symlinks(root / sync.PRIVATE)
    verified = 0
    for url in state['scope']['targets']:
        row = state['records'].get(url, {})
        if row.get('status') != 'captured': continue
        receipt = row['receipt']
        digest = receipt['sha256']
        if (not isinstance(digest, str) or len(digest) != 64
                or any(c not in 'abcdef0123456789' for c in digest)
                or receipt['rawFile'] != digest + '.body' or receipt.get('url') != url):
            raise ValueError('Captured receipt binding mismatch')
        raw = no_symlinks(private / receipt['rawFile']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError('Captured raw checksum mismatch')
        passage = no_symlinks(private / row['passageDirectory'])
        if not passage.is_relative_to(private): raise ValueError('Passage root escapes private evidence')
        manifest = sync.verify_passages(passage, raw)
        if manifest['source']['url'] != url: raise ValueError('Passage URL binding mismatch')
        verified += 1
    return {'verifiedCaptured': verified, 'rawChecksumsVerified': True,
            'passageReconstructionVerified': True}


class NoFailedRetryCapture(sync.PrivateCapture):
    """Reuse known failure receipts, without another provider attempt."""
    def get(self, url, kind='json'):
        if any(row.get('status') == 429 for row in self.ledger['requests']):
            raise RuntimeError('Prior rate-limit stop requires a separately reviewed capture')
        for row in reversed(self.ledger['requests']):
            if row.get('url') == url:
                # An interrupted request cannot supersede a known terminal outcome.
                if row.get('status') in ('pending', None): continue
                if row.get('status') != 200: return None, row
                break
        return super().get(url, kind)


def run(root=ROOT, *, max_wall_seconds=28800, poll_seconds=30,
        clock=time.monotonic, sleep=time.sleep, sync_runner=sync.run,
        auditor=audit_captured, card_export=field_cards.export,
        passage_export=field_passages.export, head_reader=source_head, scope_reader=sync.scope):
    if type(max_wall_seconds) is not int or not 1 <= max_wall_seconds <= 86400:
        raise ValueError('Wall ceiling must be 1..86400 seconds')
    if type(poll_seconds) is not int or not 1 <= poll_seconds <= 60:
        raise ValueError('Poll interval must be 1..60 seconds')
    root = no_symlinks(root)
    private = no_symlinks(root / PRIVATE)
    private.mkdir(parents=True, exist_ok=True, mode=0o700); private.chmod(0o700)
    lock = no_symlinks(private / 'supervisor.lock')
    with lock.open('a') as stream:
        try: fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise RuntimeError('A recovery supervisor is already active') from None
        started = clock(); ends = started + max_wall_seconds
        output = no_symlinks(private / ('run-' + uuid.uuid4().hex))
        output.mkdir(mode=0o700)
        result = {'profile': 'okf-plus-private-recovery-supervisor.v1',
            'distribution': 'private', 'execution': 'fixed-documentation-recovery-only',
            'sourceHEAD': head_reader(root), 'status': 'starting', 'counts': None,
            'phases': [], 'outputDirectory': output.relative_to(root).as_posix(),
            'maxWallSeconds': max_wall_seconds, 'workspaceSurvivalGuaranteed': False}
        def save(status, **extra):
            result.update(status=status, **extra)
            result['elapsedSeconds'] = max(0, clock() - started)
            atomic(output / 'receipt.json', result)
            atomic(private / 'checkpoint.json', result)
        def phase(name, details):
            result['phases'].append({'phase': name, 'sourceHEAD': head_reader(root), **details})
            save(name)
        def remaining(): return ends - clock()
        def load_state():
            path = no_symlinks(root / sync.PRIVATE / 'checkpoint.json')
            if path.exists():
                with path.open('rb') as source: raw = source.read(16 * 1024 * 1024 + 1)
                if len(raw) > 16 * 1024 * 1024: raise ValueError('Documentation checkpoint byte ceiling')
                return json.loads(raw)
            return {'scope': scope_reader(root), 'records': {}, 'stopReason': None}
        save('starting')
        previous_unknown = None
        try:
            while True:
                if remaining() <= 0: save('wall_budget'); return result
                # Observe the current writer without taking over or removing its lock.
                try:
                    with sync.writer_lock(root / sync.PRIVATE):
                        state = load_state()
                        if state['scope'] != scope_reader(root):
                            raise ValueError('Frozen documentation source scope changed')
                        result['counts'] = counts(state)
                        unknown = result['counts']['unresolved']
                        ledger_path = no_symlinks(root / sync.PRIVATE / 'ledger.json')
                        ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {'requests': []}
                        if unknown > 0 and any(row.get('status') == 429 for row in ledger['requests']):
                            save('blocked', stopReason='prior-rate-limit'); return result
                        if unknown == 0:
                            if remaining() <= 0: save('wall_budget'); return result
                            save('auditing')
                            verified = auditor(root, state)
                            phase('audit', verified)
                            if remaining() <= 0: save('wall_budget'); return result
                            cards_dir = output / 'field-cards'
                            save('exporting_field_cards')
                            cards, index = card_export(root, cards_dir)
                            phase('field_cards', {'cards': len(cards), 'indexSha256': hashlib.sha256((cards_dir / 'index.json').read_bytes()).hexdigest()})
                            if remaining() <= 0: save('wall_budget'); return result
                            overlay_dir = output / 'field-passages-final'
                            save('exporting_field_passages')
                            summary = passage_export(root, cards_root=cards_dir, private=root / sync.PRIVATE,
                                output=overlay_dir, all_collections=True)
                            phase('field_passages', {'indexSha256': hashlib.sha256((overlay_dir / 'index.json').read_bytes()).hexdigest(),
                                'candidateOnly': summary['candidateOnly'], 'allCollections': summary['allCollections']})
                            save('finished_partial' if result['counts']['failed'] else 'finished_complete',
                                 sourceScopeComplete=state.get('scopeComplete') is True)
                            return result
                        if state.get('stopReason') not in RESUMABLE:
                            save('blocked', stopReason='non-resumable-documentation-stop'); return result
                except RuntimeError as error:
                    if str(error) != 'A private documentation writer is already active': raise
                    save('waiting_writer')
                    sleep(min(poll_seconds, max(0, remaining())))
                    continue
                if previous_unknown is not None and unknown >= previous_unknown:
                    save('blocked', stopReason='no-unresolved-progress'); return result
                budget = min(3600, int(remaining()))
                if budget < 1: save('wall_budget'); return result
                save('capturing')
                try:
                    state = sync_runner(root, max_requests=3000, max_documents=2303,
                        deadline_seconds=budget, capture_factory=NoFailedRetryCapture)
                except RuntimeError as error:
                    if str(error) != 'A private documentation writer is already active': raise
                    save('waiting_writer'); sleep(min(poll_seconds, max(0, remaining()))); continue
                previous_unknown = unknown
                result['counts'] = counts(state)
                phase('capture', {'counts': result['counts'], 'stopReason': state.get('stopReason')})
        except Exception as error:
            save('failed', errorType=type(error).__name__)
            return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-wall-seconds', type=int, default=28800)
    parser.add_argument('--poll-seconds', type=int, default=30)
    args = parser.parse_args(argv)
    result = run(max_wall_seconds=args.max_wall_seconds, poll_seconds=args.poll_seconds)
    print(json.dumps({'status': result['status'], 'counts': result['counts'], 'outputDirectory': result['outputDirectory']}))
    return 0 if result['status'] in {'finished_partial','finished_complete'} else 2


if __name__ == '__main__': raise SystemExit(main())
