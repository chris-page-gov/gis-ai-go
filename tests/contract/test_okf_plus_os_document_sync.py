"""Private sync recovery contracts: synthetic snapshots and mock capture only."""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/okf_plus'))
import os_document_sync as sync
import passages
from harvest import dump


class MockCapture:
    calls = []
    fail = False
    def __init__(self, root, max_requests):
        self.private = root / sync.PRIVATE
        self.path = self.private / 'ledger.json'
        self.ledger = sync.load_json(self.path.read_text()) if self.path.exists() else {'requests': []}
        self.max_requests = max_requests
    def get(self, url, kind):
        for r in self.ledger['requests']:
            if r['url'] == url and r['status'] == 200:
                return (self.private / r['rawFile']).read_bytes().decode(), r
        if len(self.ledger['requests']) >= self.max_requests:
            raise RuntimeError('Run request ceiling reached')
        self.calls.append(url)
        raw = ('# Synthetic\r\n' + url + '\n漢字😀').encode()
        digest = hashlib.sha256(raw).hexdigest()
        r = {'url': url, 'status': 404 if self.fail else 200, 'sha256': digest,
             'rawFile': digest + '.body', 'bytes': len(raw), 'retrievedAt': 'synthetic'}
        self.ledger['requests'].append(r)
        (self.private / r['rawFile']).write_bytes(raw)
        dump(self.path, self.ledger)
        return (None if self.fail else raw.decode()), r


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for family in sync.FAMILIES:
            urls = [f'https://docs.os.uk/{family}/{name}.md' for name in ('a', 'building')]
            dump(self.root / 'okf-plus/source' / (family + '-documentation.json'),
                 {'records': [{'url': url, 'id': url} for url in urls]})
        self.patch = patch.object(passages, 'ROOT', self.root)
        self.patch.start(); self.addCleanup(self.patch.stop)
        MockCapture.calls = []; MockCapture.fail = False
    def run_sync(self, **kwargs):
        return sync.run(self.root, capture_factory=MockCapture, **kwargs)
    def test_frozen_scope_priority_bounded_batch_resume_and_exact_evidence(self):
        frozen = sync.scope(self.root)
        self.assertEqual(frozen['targetCount'], 6)
        self.assertTrue(all('/building.md' in url for url in frozen['targets'][:3]))
        state = self.run_sync(max_documents=2)
        self.assertEqual(state['counts'], {'target': 6, 'captured': 2, 'failed': 0, 'unknown': 4})
        self.assertEqual(state['stopReason'], 'document-batch-ceiling')
        state = self.run_sync(max_documents=100)
        self.assertTrue(state['scopeComplete'])
        self.assertEqual(len(MockCapture.calls), 6)
        self.assertEqual(self.run_sync()['counts']['captured'], 6)
        self.assertEqual(len(MockCapture.calls), 6)
        for row in state['records'].values():
            receipt = row['receipt']
            raw = (self.root / sync.PRIVATE / receipt['rawFile']).read_bytes()
            sync.verify_passages(self.root / sync.PRIVATE / row['passageDirectory'], raw)
        path = self.root / 'okf-plus/source/osngd-documentation.json'
        path.write_bytes(path.read_bytes() + b'\n')
        with self.assertRaises(ValueError): self.run_sync()
    def test_failure_unknown_and_request_ceiling_are_distinct(self):
        MockCapture.fail = True
        state = self.run_sync(max_requests=1)
        self.assertEqual(state['counts'], {'target': 6, 'captured': 0, 'failed': 1, 'unknown': 5})
        self.assertFalse(state['scopeComplete'])
        self.assertIn('ceiling', state['stopReason'])
    def test_deadline_and_single_writer_lock(self):
        ticks = iter([0, 2])
        state = self.run_sync(deadline_seconds=1, clock=lambda: next(ticks))
        self.assertEqual(state['counts']['unknown'], 6)
        self.assertEqual(state['stopReason'], 'wall-deadline')
        with sync.writer_lock(self.root / sync.PRIVATE):
            with self.assertRaises(RuntimeError): self.run_sync()
    def test_checksum_corruption_is_retained_as_failure(self):
        state = self.run_sync(max_documents=1)
        row = next(iter(state['records'].values()))
        (self.root / sync.PRIVATE / row['receipt']['rawFile']).write_bytes(b'corrupt')
        state = self.run_sync(max_documents=1)
        self.assertEqual(state['counts']['failed'], 1)
        self.assertFalse(state['scopeComplete'])
    def test_private_capture_prior_429_refuses_before_parent_or_network(self):
        private = self.root / sync.PRIVATE
        url = 'https://docs.os.uk/osngd/synthetic.md'
        ledger = {'profile': 'okf-plus-private-os-documentation.v1',
                  'requests': [{'url': url, 'status': 429}]}
        dump(private / 'ledger.json', ledger)
        capture = sync.PrivateCapture(self.root, 10)
        before = (private / 'ledger.json').read_bytes()
        with patch.object(sync.Capture, 'get') as parent_get, \
                patch.object(capture.opener, 'open') as network:
            for _ in range(2):
                with self.assertRaisesRegex(RuntimeError, 'Prior rate-limit'):
                    capture.get(url, 'text')
            parent_get.assert_not_called()
            network.assert_not_called()
        self.assertEqual(capture.ledger, ledger)
        self.assertEqual((private / 'ledger.json').read_bytes(), before)
    def test_unsafe_source_and_budgets_fail_without_capture(self):
        for kwargs in ({'max_requests': 3001}, {'max_documents': 0}, {'deadline_seconds': 0}):
            with self.assertRaises(ValueError): self.run_sync(**kwargs)
        dump(self.root / 'okf-plus/source/osngd-documentation.json', {'records': [
            {'url': 'https://evil.invalid/a.md', 'id': 'https://evil.invalid/a.md'}]})
        with self.assertRaises(ValueError): self.run_sync()
        self.assertEqual(MockCapture.calls, [])


if __name__ == '__main__': unittest.main()
