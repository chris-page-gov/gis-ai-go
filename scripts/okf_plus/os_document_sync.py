"""Bounded private OS documentation capture from frozen committed indexes only.

CLI: python scripts/okf_plus/os_document_sync.py --max-requests 3000
     --deadline-seconds 1800
No discovered links are followed. Documentation pacing is Capture's 0.75 seconds;
this is independent of any OS API key or API rate allowance.
"""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import os
import time
from contextlib import contextmanager
from pathlib import Path

try:
    from .harvest import Capture, dump
    from .documentation import document_url
    from .model import load_json
    from .passages import write_document, no_symlinks, DEFAULT_MAX_BYTES
except ImportError:
    from harvest import Capture, dump
    from documentation import document_url
    from model import load_json
    from passages import write_document, no_symlinks, DEFAULT_MAX_BYTES

ROOT = Path(__file__).resolve().parents[2]
FAMILIES = ('os-apis', 'osngd', 'os-downloads')
PREFIXES = tuple('/' + family + '/' for family in FAMILIES)
PRIVATE = Path('artifacts/okf-plus/private-os-documents')


def scope(root):
    sources, targets = [], []
    for family in FAMILIES:
        path = no_symlinks(root / 'okf-plus/source' / (family + '-documentation.json'))
        raw = path.read_bytes()
        snapshot = load_json(raw.decode())
        rows = snapshot['records']
        if not isinstance(rows, list):
            raise ValueError('Source index requires a record list')
        urls = []
        for row in rows:
            if not isinstance(row, dict) or row.get('id') != row.get('url'):
                raise ValueError('Source identity mismatch')
            url = document_url(row['url'], prefix='/' + family + '/')
            urls.append(url)
        if len(set(urls)) != len(urls):
            raise ValueError('Duplicate source URL')
        sources.append({'file': path.name, 'sha256': hashlib.sha256(raw).hexdigest(), 'count': len(urls)})
        targets.extend(urls)
    if len(set(targets)) != len(targets):
        raise ValueError('Duplicate cross-index URL')
    targets.sort(key=lambda url: (not any(token in url for token in
        ('pavement', 'road-link', '/building.md', 'heightingmethod', 'building-height')), url))
    return {'sources': sources, 'targetCount': len(targets), 'targets': targets,
            'discoveredLinksFollowed': False}


@contextmanager
def writer_lock(private):
    no_symlinks(private)
    private.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(private, 0o700)
    lock = no_symlinks(private / 'writer.lock')
    with lock.open('a') as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError('A private documentation writer is already active') from error
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


class PrivateCapture(Capture):
    def __init__(self, root, max_requests):
        private = no_symlinks(root / PRIVATE)
        # Initialisation at an unused private root avoids reading the public lane's ledger.
        super().__init__(private, max_requests)
        self.private = private
        self.path = no_symlinks(private / 'ledger.json')
        self.ledger = load_json(self.path.read_text()) if self.path.exists() else {
            'profile': 'okf-plus-private-os-documentation.v1', 'requests': []}
        for receipt in self.ledger['requests']:
            document_url(receipt['url'], prefix=PREFIXES)
            if receipt.get('rawFile'):
                name = receipt['rawFile']
                if name != receipt.get('sha256', '') + '.body' or Path(name).name != name:
                    raise ValueError('Unsafe raw evidence filename')
                no_symlinks(private / name)

    def get(self, url, kind='json'):
        if any(row.get('status') == 429 for row in self.ledger['requests']):
            raise RuntimeError('Prior rate-limit stop requires a separately reviewed capture')
        return super().get(url, kind)


def verify_passages(output, raw):
    manifest_path = no_symlinks(output / 'manifest.jsonld')
    manifest = load_json(manifest_path.read_text())
    chunks = []
    for number, segment in enumerate(manifest['segments'], 1):
        if segment['file'] != f'part-{number:08d}.jsonld':
            raise ValueError('Unexpected passage filename or order')
        payload = no_symlinks(output / segment['file']).read_bytes()
        if hashlib.sha256(payload).hexdigest() != segment['sha256'] or len(payload) != segment['bytes']:
            raise ValueError('Passage checksum mismatch')
        chunks.append(load_json(payload.decode())['text'].encode())
    if b''.join(chunks) != raw or manifest['source']['sha256'] != hashlib.sha256(raw).hexdigest():
        raise ValueError('Passage reconstruction mismatch')
    return manifest


def run(root=ROOT, *, max_requests=3000, deadline_seconds=1800, max_passage_bytes=DEFAULT_MAX_BYTES,
        capture_factory=PrivateCapture, clock=time.monotonic, max_documents=100):
    if type(max_requests) is not int or not 1 <= max_requests <= 3000:
        raise ValueError('Request ceiling must be 1..3000')
    if type(deadline_seconds) is not int or not 1 <= deadline_seconds <= 86400:
        raise ValueError('Deadline must be 1..86400 seconds')
    if type(max_documents) is not int or not 1 <= max_documents <= 3000:
        raise ValueError('Document batch must be 1..3000')
    private = no_symlinks(root / PRIVATE)
    frozen = scope(root)
    started = clock()
    with writer_lock(private):
        checkpoint = no_symlinks(private / 'checkpoint.json')
        state = load_json(checkpoint.read_text()) if checkpoint.exists() else {
            'profile': 'okf-plus-private-os-document-sync.v1', 'scope': frozen, 'records': {},
            'distribution': 'private', 'executionAdmitted': False}
        if state['scope'] != frozen:
            raise ValueError('Frozen source scope changed; preserve this run and choose a new recovery path')
        cap = capture_factory(root, max_requests)
        state['stopReason'] = None
        def save():
            rows = state['records'].values()
            captured = sum(row['status'] == 'captured' for row in rows)
            failed = sum(row['status'] == 'failed' for row in rows)
            state['counts'] = {'target': len(frozen['targets']), 'captured': captured,
                'failed': failed, 'unknown': len(frozen['targets']) - captured - failed}
            state['requestCount'] = len(cap.ledger['requests'])
            state['scopeComplete'] = captured == len(frozen['targets'])
            dump(checkpoint, state)
        save()
        attempted = 0
        for url in frozen['targets']:
            if clock() - started >= deadline_seconds:
                state['stopReason'] = 'wall-deadline'; break
            previous = state['records'].get(url, {})
            if previous.get('status') != 'captured':
                if attempted >= max_documents:
                    state['stopReason'] = 'document-batch-ceiling'; break
                attempted += 1
            try:
                text, receipt = cap.get(url, 'text')
                if text is None:
                    state['records'][url] = {'status': 'failed', 'receipt': dict(receipt)}
                    save(); continue
                path = no_symlinks(private / receipt['rawFile'])
                raw = path.read_bytes()
                if hashlib.sha256(raw).hexdigest() != receipt['sha256']:
                    raise ValueError('Raw checksum mismatch')
                key = hashlib.sha256((url + '\0' + receipt['sha256']).encode()).hexdigest()
                output = no_symlinks(private / 'passages' / key)
                manifest = verify_passages(output, raw) if output.exists() else write_document(
                    path, url, output, max_bytes=max_passage_bytes)
                state['records'][url] = {'status': 'captured', 'receipt': dict(receipt),
                    'passageDirectory': 'passages/' + key, 'passageCount': len(manifest['segments'])}
            except RuntimeError as error:
                state['stopReason'] = str(error)
                save(); break
            except (ValueError, OSError, UnicodeError) as error:
                state['records'][url] = {'status': 'failed', 'error': type(error).__name__,
                    'receipts': [dict(r) for r in cap.ledger['requests'] if r['url'] == url]}
            save()
        save()
        return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-requests', type=int, required=True)
    parser.add_argument('--deadline-seconds', type=int, default=1800)
    parser.add_argument('--max-documents', type=int, default=100)
    parser.add_argument('--max-passage-bytes', type=int, default=DEFAULT_MAX_BYTES)
    args = parser.parse_args()
    state = run(max_requests=args.max_requests, deadline_seconds=args.deadline_seconds,
                max_passage_bytes=args.max_passage_bytes, max_documents=args.max_documents)
    print(state['counts'], 'stop:', state['stopReason'], flush=True)


if __name__ == '__main__':
    main()
