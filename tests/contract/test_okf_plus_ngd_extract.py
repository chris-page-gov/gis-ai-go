"""Synthetic private extraction contracts; no provider calls or real contents."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/okf_plus'))
import ngd_extract as module


class ExtractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        mocked = patch.object(module, 'ROOT', self.root)
        mocked.start(); self.addCleanup(mocked.stop)
        self.calls = []
        self.now = 0
        self.responses = []

    def clock(self): return self.now
    def sleep(self, value): self.now += value
    def transport(self, url, key, maximum, timeout):
        self.calls.append((url, key, maximum, timeout))
        return self.responses.pop(0)
    def feature(self, identity, value=1):
        return {'type': 'Feature', 'id': identity, 'properties': {'width': value}, 'geometry': None}
    def page(self, rows, next_offset=None, links=True):
        result = {'type': 'FeatureCollection', 'features': rows, 'numberReturned': len(rows)}
        if links:
            result['links'] = [] if next_offset is None else [{'rel': 'next', 'href': module.BASE + 'test-v1/items?offset=' + str(next_offset)}]
        return 200, json.dumps(result).encode(), {'Content-Crs': '<' + module.CRS['27700'] + '>'}
    def run_extract(self, **kwargs):
        return module.extract('test-v1', [-1, 50, 0, 51], key='PRIVATE-KEY',
                              transport=self.transport, clock=self.clock, sleep=self.sleep, **kwargs)
    def receipt_path(self): return next(self.root.rglob('receipt.json'))

    def test_complete_pages_full_records_and_header_only_key(self):
        self.responses = [self.page([self.feature('a'), self.feature('b')], 2), self.page([self.feature('c')])]
        result = self.run_extract(limit=2)
        self.assertTrue(result['complete']); self.assertEqual(result['featureCount'], 3)
        self.assertFalse(result['snapshotIsolation'])
        self.assertEqual([parse_qs(urlsplit(c[0]).query)['offset'] for c in self.calls], [['0'], ['2']])
        self.assertTrue(all('PRIVATE-KEY' not in c[0] and c[1] == 'PRIVATE-KEY' for c in self.calls))
        self.assertNotIn('PRIVATE-KEY', self.receipt_path().read_text())
        output = self.receipt_path().parent / 'features.ndjson'
        self.assertEqual(len(output.read_text().splitlines()), 3)
        self.assertTrue((output.parent / 'page-000000.json').exists())

    def test_cap_never_implies_complete_and_resume_verifies_hash(self):
        self.responses = [self.page([self.feature('a')], 1)]
        first = self.run_extract(limit=1, max_requests=1)
        self.assertFalse(first['complete']); self.assertEqual(first['reason'], 'request-budget')
        self.assertFalse((self.receipt_path().parent / 'features.ndjson').exists())
        self.responses = [self.page([])]
        second = self.run_extract(limit=1, max_requests=2)
        self.assertTrue(second['complete']); self.assertEqual(second['requests'], 2)
        (self.receipt_path().parent / 'page-000000.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            self.run_extract(limit=1, max_requests=3)

    def test_429_stops_without_retry(self):
        self.responses = [(429, b'private provider message', {})]
        result = self.run_extract()
        self.assertEqual((result['complete'], result['reason'], len(self.calls)), (False, 'rate-limited', 1))
        self.assertNotIn('private provider message', self.receipt_path().read_text())
        self.assertEqual(self.run_extract()['reason'], 'rate-limited')
        self.assertEqual(self.run_extract(refresh=True)['reason'], 'rate-limited')
        self.assertEqual(len(self.calls), 1)

    def test_missing_links_requires_empty_page(self):
        self.responses = [self.page([self.feature('a')], links=False), self.page([], links=False)]
        self.assertTrue(self.run_extract()['complete'])
        self.assertEqual(len(self.calls), 2)

    def test_duplicate_or_changed_identity_is_incomplete(self):
        for value in (1, 2):
            with self.subTest(value=value):
                self.responses = [self.page([self.feature('a')], 1), self.page([self.feature('a', value)])]
                result = self.run_extract(limit=1, max_requests=4)
                self.assertFalse(result['complete'])
                for path in self.receipt_path().parent.iterdir(): path.unlink()

    def test_untrusted_next_url_never_followed(self):
        status, raw, headers = self.page([self.feature('a')], 1)
        data = json.loads(raw); data['links'][0]['href'] = 'https://evil.example/steal?offset=1'
        self.responses = [(status, json.dumps(data).encode(), headers)]
        self.assertFalse(self.run_extract(limit=1)['complete']); self.assertEqual(len(self.calls), 1)

    def test_validation_injection_and_collection_bound_queryables(self):
        for kwargs in ({'osids': ["a') OR TRUE --"]}, {'osids': ['abc']}, {'bbox_crs': '4326'}, {'requests_per_minute': 31}, {'id_filter_operator': 'or; DROP'}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError): self.run_extract(**kwargs)
        with self.assertRaises(ValueError):
            module.extract('../items?key=x', [0, 1, 2, 3], key='key')
        with self.assertRaises(ValueError):
            module.extract('test-v1', [0, 1, float('nan'), 3], key='key')
        self.responses = [self.page([])]
        evidence = {'collectionId': 'test-v1', 'properties': {'osid': {'type': 'string'}}}
        self.assertTrue(self.run_extract(osids=['abc'], queryables=evidence)['complete'])
        query = parse_qs(urlsplit(self.calls[0][0]).query)
        self.assertEqual(query['filter'], ["(osid = 'abc')"])
        self.assertNotIn('properties', query)

    def test_safe_or_default_and_explicit_in_have_distinct_selection_receipts(self):
        evidence = {'collectionId': 'test-v1', 'properties': {'osid': {'type': 'string'}}}
        for operator, expected in (('or', "(osid = 'abc' OR osid = 'def')"),
                                   ('in', "osid IN ('abc','def')")):
            self.responses = [self.page([])]
            result = self.run_extract(osids=['def', 'abc'], queryables=evidence, id_filter_operator=operator)
            query = parse_qs(urlsplit(self.calls[-1][0]).query)
            self.assertEqual(query['filter'], [expected])
            self.assertEqual(result['selection']['idFilterOperator'], operator)
        receipts = list(self.root.rglob('receipt.json'))
        self.assertEqual(len(receipts), 2)

    def test_wall_and_byte_budgets_never_complete(self):
        self.assertEqual(self.run_extract(max_wall_seconds=1)['reason'], 'wall-budget')
        self.responses = [self.page([])]
        self.assertFalse(self.run_extract(max_bytes=1)['complete'])

    def test_no_redirect_handler(self):
        self.assertIsNone(module.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://elsewhere'))

    def test_count_contradiction_is_not_complete(self):
        status, raw, headers = self.page([self.feature('a')])
        data = json.loads(raw); data['numberMatched'] = 20
        self.responses = [(status, json.dumps(data).encode(), headers)]
        self.assertFalse(self.run_extract()['complete'])

    def test_one_writer_and_local_files_not_symlinks(self):
        def nested(*args):
            with self.assertRaisesRegex(ValueError, 'active writer'):
                self.run_extract()
            return self.page([])
        self.transport = nested
        self.assertTrue(self.run_extract()['complete'])
        receipt_path = self.receipt_path()
        receipt_path.unlink()
        receipt_path.symlink_to(self.root / 'outside')
        with self.assertRaisesRegex(ValueError, 'Symlinks'):
            self.run_extract()

    def test_content_crs_required_and_matching_registry(self):
        self.assertIn('3857', module.CRS); self.assertNotIn('4979', module.CRS)
        status, raw, headers = self.page([])
        self.responses = [(status, raw, {'Content-Crs': module.CRS['4326']})]
        result = self.run_extract()
        self.assertEqual(result['reason'], 'content-crs-mismatch')
        self.assertFalse(result['complete'])
        self.assertTrue((self.receipt_path().parent / 'page-000000.json').exists())

    def test_verified_profile_disposal_and_explicit_reacquisition_history(self):
        import transient_profile
        self.responses = [self.page([self.feature('a')])]
        result = self.run_extract()
        directory = self.receipt_path().parent
        profile_path = directory / 'profile.json'
        with patch.object(transient_profile, 'ROOT', self.root):
            profile = transient_profile.profile(directory / 'features.ndjson', profile_path,
                recipe={'selectionDigest': directory.name})
        for mutate in ('input', 'selection', 'cardinality', 'incomplete'):
            bad = json.loads(json.dumps(profile))
            if mutate == 'input': bad['inputSha256'] = 'bad'
            if mutate == 'selection': bad['retrievalRecipe']['selectionDigest'] = 'bad'
            if mutate == 'cardinality': bad['fields'][0]['cardinalityComplete'] = False
            if mutate == 'incomplete': bad['scanComplete'] = False
            profile_path.write_bytes(module.encoded(bad))
            with self.assertRaisesRegex(ValueError, 'Complete selection-bound'):
                module.discard_payloads(directory, profile_path)
            self.assertTrue((directory / 'features.ndjson').exists())
            self.assertTrue((directory / 'page-000000.json').exists())
        profile_path.write_bytes(module.encoded(profile))
        discarded = module.discard_payloads(directory, profile_path)
        self.assertTrue(discarded['payloadDiscarded'])
        self.assertEqual(discarded['profileSha256'], module.sha(profile_path.read_bytes()))
        self.assertFalse((directory / 'features.ndjson').exists())
        self.assertFalse((directory / 'page-000000.json').exists())
        self.assertTrue(profile_path.exists())
        count = len(self.calls)
        result = self.run_extract()
        self.assertEqual(result['reason'], 'needs-reacquisition'); self.assertFalse(result['complete'])
        self.assertEqual(len(self.calls), count)
        self.responses = [self.page([])]
        self.assertTrue(self.run_extract(refresh=True)['complete'])
        archive = next(path for path in (directory / 'history').glob('*.json') if '.profile.' not in path.name)
        self.assertEqual(json.loads(archive.read_bytes())['profileSha256'], discarded['profileSha256'])
        self.assertEqual(module.sha(archive.with_name(archive.stem + '.profile.json').read_bytes()), discarded['profileSha256'])

    def test_durability_failure_prevents_egress(self):
        with patch.object(module.os, 'fsync', side_effect=OSError('synthetic durability failure')):
            with self.assertRaises(OSError): self.run_extract()
        self.assertEqual(self.calls, [])

    def test_disposal_durability_failures_preserve_payloads(self):
        import transient_profile
        self.responses = [self.page([self.feature('a')])]
        self.run_extract()
        directory = self.receipt_path().parent
        profile_path = directory / 'profile.json'
        with patch.object(transient_profile, 'ROOT', self.root):
            transient_profile.profile(directory / 'features.ndjson', profile_path,
                recipe={'selectionDigest': directory.name})
        original_receipt = self.receipt_path().read_bytes()
        original_fsync = module.os.fsync
        for failure_at in range(1, 5):
            with self.subTest(failure_at=failure_at):
                self.receipt_path().write_bytes(original_receipt)
                calls = 0
                def flaky(descriptor):
                    nonlocal calls
                    calls += 1
                    if calls == failure_at: raise OSError('synthetic durability failure')
                    return original_fsync(descriptor)
                with patch.object(module.os, 'fsync', side_effect=flaky):
                    with self.assertRaises(OSError):
                        module.discard_payloads(directory, profile_path)
                self.assertTrue((directory / 'features.ndjson').exists())
                self.assertTrue((directory / 'page-000000.json').exists())
                self.assertTrue(profile_path.exists())

    def test_fixed_response_ceiling_retains_partial_payload_without_parsing(self):
        self.assertEqual(module.MAX_PAGE_BYTES, 8 * 1024 * 1024)
        self.responses = [(200, b'x' * 65, {'Content-Crs': module.CRS['27700']})]
        with patch.object(module, 'MAX_PAGE_BYTES', 64):
            result = self.run_extract(max_bytes=1000)
            self.assertEqual(result['reason'], 'response-byte-budget')
            self.assertFalse(result['complete'])
            self.assertEqual(self.calls[0][2], 64)
            self.assertEqual((self.receipt_path().parent / 'page-000000.json').read_bytes(), b'x' * 65)
            self.assertEqual(self.run_extract(max_bytes=2000)['reason'], 'response-byte-budget')
            self.assertEqual(len(self.calls), 1)


if __name__ == '__main__': unittest.main()
