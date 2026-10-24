"""Synthetic, offline checks for owner-private OS metadata inventory."""
import hashlib
import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.error import HTTPError

from scripts.okf_plus import os_private_inventory as inventory


class PrivateInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / 'private'
        self.key = patch.dict(os.environ, {'OS_API_KEY': 'synthetic-secret-never-persist'})
        self.key.start()
        self.addCleanup(self.key.stop)
        self.opener_patch = patch.object(inventory, 'build_opener')
        self.opener = self.opener_patch.start().return_value
        self.addCleanup(self.opener_patch.stop)
        sleep = patch.object(inventory.time, 'sleep')
        sleep.start()
        self.addCleanup(sleep.stop)

    def make(self, **kwargs):
        return inventory.Inventory(self.output, **kwargs)

    def response(self, raw=b'[]', status=200):
        response = Mock()
        response.read.return_value = raw
        response.status = status
        self.opener.open.return_value.__enter__.return_value = response
        return response

    def test_only_fixed_metadata_routes_admitted(self):
        allowed = [inventory.PACKAGE, '/features/ngd/ofa/v1/collections',
                   '/downloads/v1/products', inventory.PACKAGE + '/pkg-1/versions/v_2']
        for route in allowed:
            self.assertEqual(inventory.admitted(route), inventory.BASE + route)
        for route in ['https://evil.invalid/', inventory.PACKAGE + '?key=secret',
                      inventory.PACKAGE + '/pkg/versions/v/files',
                      inventory.PACKAGE + '/../files', '//evil.invalid',
                      '/features/ngd/ofa/v1/collections/building/items']:
            with self.subTest(route=route), self.assertRaises(ValueError):
                inventory.admitted(route)
        self.opener.open.assert_not_called()

    def test_budget_validation_rejects_boolean_and_outside_bounds(self):
        for kwargs in [{'max_requests': True}, {'max_requests': 0},
                       {'max_requests': 1001}, {'max_requests': 1.5},
                       {'wall_seconds': False}, {'wall_seconds': 0},
                       {'wall_seconds': 3601}, {'wall_seconds': float('inf')}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.make(**kwargs)
        self.opener.open.assert_not_called()

    def test_private_modes_and_successful_receipt_contain_no_key(self):
        self.response()
        worker = self.make()
        worker.get(inventory.PACKAGE)
        self.assertEqual(stat.S_IMODE(self.output.stat().st_mode), 0o700)
        for path in self.output.iterdir():
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertNotIn(os.environ['OS_API_KEY'], path.read_text())
        row = json.loads(worker.path.read_text())['requests'][0]
        self.assertEqual(row['status'], 200)
        self.assertEqual(row['bytes'], 2)
        self.assertEqual(row['sha256'], hashlib.sha256(b'[]').hexdigest())

    def test_replay_checks_checksum_without_network(self):
        self.response(b'{"synthetic":true}')
        worker = self.make()
        expected = worker.get(inventory.PACKAGE)
        self.opener.open.reset_mock()
        resumed = self.make()
        self.assertEqual(resumed.get(inventory.PACKAGE), expected)
        self.opener.open.assert_not_called()
        digest = resumed.ledger['requests'][0]['sha256']
        (self.output / (digest + '.json')).write_bytes(b'{}')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            resumed.get(inventory.PACKAGE)
        self.opener.open.assert_not_called()

    def test_previous_429_stops_new_requests(self):
        worker = self.make()
        worker.ledger['requests'].append({'route': inventory.PACKAGE, 'status': 429})
        inventory.save(worker.path, worker.ledger)
        with self.assertRaisesRegex(RuntimeError, 'Prior rate-limit'):
            self.make().get('/downloads/v1/products')
        self.opener.open.assert_not_called()

    def test_cumulative_request_and_byte_budgets_stop_before_network(self):
        for row, message in [({'status': 'failed', 'route': inventory.PACKAGE}, 'request ceiling'),
                             ({'status': 'failed', 'route': inventory.PACKAGE,
                               'bytes': inventory.MAX_TOTAL}, 'byte ceiling')]:
            with self.subTest(message=message):
                worker = self.make(max_requests=1 if 'request' in message else 2)
                worker.ledger['requests'] = [row]
                with self.assertRaisesRegex(RuntimeError, message):
                    worker.get('/downloads/v1/products')
        self.opener.open.assert_not_called()

    def test_wall_budget_stops_before_network(self):
        worker = self.make(wall_seconds=1)
        with self.assertRaisesRegex(RuntimeError, 'Wall budget'):
            worker.get(inventory.PACKAGE)
        self.opener.open.assert_not_called()

    def test_oversized_response_persists_bounded_failure(self):
        response = self.response(b'12345')
        worker = self.make()
        with patch.object(inventory, 'MAX_BODY', 4):
            with self.assertRaisesRegex(RuntimeError, 'Inventory request failed'):
                worker.get(inventory.PACKAGE)
        response.read.assert_called_once_with(5)
        row = json.loads(worker.path.read_text())['requests'][0]
        self.assertEqual(row['status'], 'failed')
        self.assertEqual(row['bytes'], 5)
        self.assertNotIn('sha256', row)

    def test_request_failure_persisted_without_credential_or_exception_text(self):
        self.opener.open.side_effect = HTTPError(
            'https://example.invalid/?key=synthetic-secret-never-persist', 429,
            'synthetic-secret-never-persist', {'Retry-After': '30'}, None)
        worker = self.make()
        with self.assertRaises(RuntimeError) as caught:
            worker.get(inventory.PACKAGE)
        self.assertNotIn(os.environ['OS_API_KEY'], str(caught.exception))
        content = worker.path.read_text()
        self.assertNotIn(os.environ['OS_API_KEY'], content)
        row = json.loads(content)['requests'][0]
        self.assertEqual(row['status'], 429)
        self.assertEqual(row['errorType'], 'HTTPError')
        self.assertEqual(row['retryAfter'], '30')
        self.assertIn('elapsedSeconds', row)

    def test_catalogue_constructs_version_routes_from_native_identifiers(self):
        worker = self.make()
        responses = {inventory.PACKAGE: [{'id': 'native-package',
            'url': 'https://evil.invalid/package', 'versions': [
                {'id': 'version-1', 'url': 'https://evil.invalid/payload'}]}],
            '/features/ngd/ofa/v1/collections': {'collections': [{'id': 'synthetic'}]},
            '/downloads/v1/products': [{'id': 'synthetic-product'}],
            inventory.PACKAGE + '/native-package/versions/version-1': {'files': []}}
        with patch.object(worker, 'get', side_effect=responses.__getitem__) as get:
            result = worker.run()
        self.assertEqual([call.args[0] for call in get.call_args_list], list(responses))
        self.assertEqual(result['versionCount'], 1)
        self.assertFalse(result['featureDataDownloaded'])
        self.assertEqual(result['globalEntitlementCompleteness'], 'not-established')
        self.assertNotIn('versions', result)
        self.opener.open.assert_not_called()

    def test_invalid_native_identifier_cannot_supply_a_route(self):
        worker = self.make()
        with patch.object(worker, 'get', side_effect=[
            [{'id': '../escape', 'versions': [{'id': 'v1'}]}], {'collections': []}, []]) as get:
            with self.assertRaises(ValueError):
                worker.run()
        self.assertEqual(get.call_count, 3)
        self.opener.open.assert_not_called()
