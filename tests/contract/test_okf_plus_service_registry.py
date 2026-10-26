from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator, ValidationError

from scripts.okf_plus import service_registry as registry
from scripts.okf_plus.model import canonical, digest, load_json, read_markdown
from scripts.okf_plus.semantic import semantic_id

ROOT = Path(__file__).resolve().parents[2]


class ServiceRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.bundle = Path(cls.temp.name) / 'bundle'
        cls.summary = registry.build(cls.bundle)
        cls.cards, _ = registry.project()
        cls.source = json.loads((ROOT / registry.SOURCE).read_text())
        cls.validator = Draft202012Validator(json.loads((ROOT / registry.SCHEMA).read_text()))

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def _operation(self, service, path):
        return next(c for c in self.cards if c['kind'] == 'operation' and c['service'] == service and c['native']['operation']['path'] == path)

    def _repository(self, path):
        for relative in [registry.SOURCE, registry.SCHEMA, *[p for entries in registry.EVIDENCE_FILES.values() for _, p in entries]]:
            target = path / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)

    def test_every_retained_operation_preserves_native_contract_and_exact_semantic_identity(self):
        expected = {}
        for ri, row in enumerate(self.source['records']):
            for ci, contract in enumerate(row['contracts']):
                for oi, operation in enumerate(contract['operations']):
                    suffix = f'/contracts/{ci}/operations/{oi}'
                    atomic = semantic_id('api-operation', self.source['family'], row['id'], suffix)
                    expected[atomic] = (ri, row, contract, operation, suffix)
        actual = {c['atomicOperation']: c for c in self.cards if c['kind'] == 'operation'}
        self.assertEqual(set(actual), set(expected))
        self.assertEqual(len(actual), 60)
        for atomic, (ri, row, contract, operation, suffix) in expected.items():
            card = actual[atomic]
            self.assertEqual(card['native']['operation'], operation)
            self.assertEqual(card['native']['servers'], contract['servers'])
            self.assertEqual(card['native']['sourceCallable'], row['callable'])
            self.assertEqual(card['native']['fragmentSha256'], contract['fragmentSha256'])
            self.assertEqual(card['native']['contractSha256'], digest(contract))
            self.assertEqual(card['source']['pointer'], f'/records/{ri}' + suffix)
            self.assertEqual(card['source']['valueSha256'], digest(operation))
            self.assertEqual(card['source']['recordSha256'], digest(row))
            self.assertEqual(card['source']['documentSha256'], row['sourceSha256'])

    def test_source_capture_and_implementation_hashes_are_exact(self):
        snapshot_hash = hashlib.sha256((ROOT / registry.SOURCE).read_bytes()).hexdigest()
        for card in self.cards:
            self.assertEqual(card['source']['snapshotSha256'], snapshot_hash)
            receipt = card['source']['captureReceipt']
            self.assertEqual(receipt['url'], card['source']['documentUrl'])
            self.assertEqual(receipt['sha256'], card['source']['documentSha256'])
            self.assertIn(receipt, self.source['receipts'])
            for evidence in card['implementationEvidence']:
                self.assertEqual(evidence['sha256'], hashlib.sha256((ROOT / evidence['path']).read_bytes()).hexdigest())

    def test_ten_current_data_families_with_withdrawn_and_oauth_gaps(self):
        self.assertEqual(self.summary['serviceCount'], 12)
        self.assertEqual(self.summary['currentDataServiceCount'], 10)
        self.assertEqual(self.summary['withdrawnServiceCount'], 1)
        self.assertEqual(self.summary['retainedDocumentCount'], 152)
        services = {c['service']: c for c in self.cards if c['kind'] == 'service'}
        self.assertEqual(services['oauth-2-api']['operationCounts']['retained'], 0)
        self.assertTrue(any('No OpenAPI' in gap for gap in services['oauth-2-api']['gaps']))
        withdrawn = services['os-match-and-cleanse-api']
        self.assertEqual(withdrawn['statuses']['lifecycle'], 'withdrawn-in-retained-documentation')
        self.assertIn('withdrawn', withdrawn['title'])
        self.assertEqual(sum(c['native']['documentationCount'] for c in services.values()) + self.summary['supportingDocumentCount'], 152)

    def test_only_exact_ngd_items_route_is_supported_for_local_private_data(self):
        supported = [c for c in self.cards if c['kind'] == 'operation' and c['statuses']['dataExecutorImplemented'] == 'implemented-subset']
        self.assertEqual(len(supported), 1)
        card = supported[0]
        self.assertEqual(card['native']['operation']['path'], '/collections/{collectionId}/items')
        self.assertEqual(card['native']['servers'], [registry.NGD_SERVER])
        self.assertFalse(self._operation('os-ngd-api-features', '/collections/{collectionId}/items/{featureId}')['statuses']['dataExecutorImplemented'] == 'implemented-subset')
        lifecycle = 'current-in-retained-documentation'
        op = card['native']['operation']
        for slug, change, servers, state in [
            ('os-names-api', {}, [registry.NGD_SERVER], lifecycle),
            ('os-ngd-api-features', {'method': 'POST'}, [registry.NGD_SERVER], lifecycle),
            ('os-ngd-api-features', {'operationId': 'other'}, [registry.NGD_SERVER], lifecycle),
            ('os-ngd-api-features', {}, ['https://example.invalid'], lifecycle),
            ('os-ngd-api-features', {}, [registry.NGD_SERVER, 'https://example.invalid'], lifecycle),
            ('os-ngd-api-features', {}, [registry.NGD_SERVER], 'withdrawn-in-retained-documentation'),
        ]:
            self.assertFalse(registry._support(slug, {**op, **change}, servers, state)[1])

    def test_metadata_capture_is_deferred_without_losing_native_documented_routes(self):
        supported = [c for c in self.cards if c['kind'] == 'operation' and c['statuses']['metadataCaptureImplemented'] == 'implemented-subset']
        self.assertEqual(supported, [])
        self.assertEqual(self.summary['metadataCaptureOperationCount'], 0)
        self.assertEqual(registry.EVIDENCE_FILES['metadata'], ())
        documented = [c for c in self.cards if c['kind'] == 'operation'
                      and c['native']['operation']['path'] in registry.METADATA_PATHS.get(c['service'], set())]
        self.assertEqual(len(documented), 10)
        for card in documented:
            self.assertEqual(card['statuses']['metadataCaptureImplemented'], 'not-implemented-in-profile')
            self.assertEqual(card['implementationEvidence'], [])
            self.assertNotIn('supportedMetadata', card['scope'])
            self.assertIn('absent from this checkout', card['scope']['otherImplementations'])
            self.assertIn(registry.DEFERRED_METADATA_SOURCE, card['scope']['otherImplementations'])
        download = self._operation('os-downloads-api', '/dataPackages/{dataPackageId}/versions/{versionId}/downloads')
        self.assertEqual(download['statuses']['metadataCaptureImplemented'], 'not-implemented-in-profile')
        self.assertEqual(download['statuses']['dataExecutorImplemented'], 'not-implemented-in-profile')

    def test_data_support_binds_canonical_extraction_and_verified_profiling_contracts(self):
        from scripts.okf_plus import ngd_extract
        card = self._operation('os-ngd-api-features', '/collections/{collectionId}/items')
        self.assertEqual({(row['kind'], row['path']) for row in card['implementationEvidence']}, {
            ('implementation', 'scripts/okf_plus/ngd_extract.py'),
            ('implementation', 'scripts/okf_plus/transient_profile.py'),
            ('synthetic-test-contract', 'tests/contract/test_okf_plus_ngd_extract.py'),
            ('synthetic-test-contract', 'tests/contract/test_okf_plus_transient_profile.py'),
        })
        self.assertEqual(card['scope']['executionProfile'], 'private-ngd-extract-with-transient-profile')
        self.assertIn('requires a collection identifier and bbox', card['scope']['supportedData'])
        self.assertIn('complete selection-bound profiling', card['scope']['supportedData'])
        self.assertTrue(any('arbitrary CQL, datetime, a whole-collection option' in gap for gap in card['gaps']))
        self.assertNotIn('os_retrieve', json.dumps(card))
        # The advertised identifier subset requires matching collection evidence;
        # documentation of a wider API filter does not authorise it in this executor.
        queryables = {'collectionId': 'synthetic-1', 'properties': {'osid': {'type': 'string'}}}
        for operator in ('or', 'in'):
            selected = ngd_extract.selection('synthetic-1', [0, 0, 1, 1], 'CRS84', '7405',
                                             ['synthetic-id'], queryables, operator)
            self.assertEqual(selected['idFilterOperator'], operator)
            self.assertIsNotNone(selected['queryablesSha256'])
        with self.assertRaisesRegex(ValueError, 'Collection-bound queryables'):
            ngd_extract.selection('different-1', [0, 0, 1, 1], 'CRS84', '7405',
                                  ['synthetic-id'], queryables)

    def test_no_false_live_or_synthetic_execution_claims_and_no_secret_access(self):
        with patch('socket.socket', side_effect=AssertionError('offline registry used network')), patch('os.getenv', side_effect=AssertionError('registry read a credential environment')):
            cards, summary = registry.project()
        self.assertEqual(summary['providerRequestsMade'], 0)
        for card in cards:
            self.assertEqual(card['statuses']['liveAccess'], 'not-tested')
            self.assertEqual(card['scope']['executionProfile'], 'private-ngd-extract-with-transient-profile')
            self.assertIn('outside', card['scope']['otherImplementations'])
            self.assertIn(card['statuses']['syntheticValidation'], ['not-evidenced', 'test-contracts-present-not-executed-by-registry'])

    def test_unresolved_servers_post_query_and_remote_work_are_preserved(self):
        linked = self._operation('os-linked-identifiers-api', '/identifiers/{id}')
        self.assertEqual(linked['native']['servers'], ['${lids.api.server}/search/links/v1'])
        self.assertTrue(any('unresolved variable' in gap for gap in linked['gaps']))
        self.assertEqual(self._operation('os-places-api', '/polygon')['native']['operation']['method'], 'POST')
        for path in ('/prepareRinexZipDownload', '/startRinexZipDownload'):
            card = self._operation('os-net-api', path)
            self.assertTrue(any('remote preparation' in gap for gap in card['gaps']))
            self.assertEqual(card['statuses']['metadataCaptureImplemented'], 'not-implemented-in-profile')

    def test_schema_is_closed_and_all_cards_fit_without_truncation(self):
        Draft202012Validator.check_schema(self.validator.schema)
        for card in self.cards:
            self.validator.validate(card)
            self.assertLessEqual(len(registry._encoded(card, self.validator)), 16384)
            for field in ('statuses', 'source', 'scope'):
                changed = deepcopy(card)
                changed[field]['invented'] = True
                with self.assertRaises(ValidationError):
                    self.validator.validate(changed)
        changed = deepcopy(self.cards[0])
        changed['unreviewedStatus'] = True
        with self.assertRaises(ValidationError):
            self.validator.validate(changed)

    def test_oversize_card_fails_before_output_and_existing_output_is_not_replaced(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'new-bundle'
            huge = deepcopy(self.cards)
            huge[0]['role']['summary'] = 'synthetic ' * 10000
            with patch.object(registry, 'project', return_value=(huge, self.summary)):
                with self.assertRaisesRegex(ValueError, 'exceeds 16 KiB'):
                    registry.build(output)
            self.assertFalse(output.exists())
            output.mkdir()
            marker = output / 'preserve.txt'
            marker.write_text('user data')
            with self.assertRaisesRegex(ValueError, 'new directory'):
                registry.build(output)
            self.assertEqual(marker.read_text(), 'user data')

    def test_new_unknown_service_and_outside_document_operation_are_not_discarded(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self._repository(repo)
            source = deepcopy(self.source)
            row = deepcopy(source['records'][31])
            row['url'] = row['id'] = 'https://docs.os.uk/os-apis/accessing-os-apis/os-synthetic-api/route.md'
            row['title'] = 'Synthetic service'
            source['records'].append(row)
            outside = deepcopy(row)
            outside['url'] = outside['id'] = 'https://docs.os.uk/os-apis/core-concepts/synthetic.md'
            source['records'].append(outside)
            (repo / registry.SOURCE).write_bytes(canonical(source))
            cards, summary = registry.project(repo)
            self.assertEqual(summary['operationCount'], 62)
            self.assertEqual(summary['unmappedServiceCount'], 2)
            unknown = [c for c in cards if c['role']['category'] == 'unknown']
            self.assertEqual(len(unknown), 4)
            self.assertTrue(all(c['statuses']['lifecycle'] == 'unknown' for c in unknown))
            self.assertTrue(all(c['statuses']['dataExecutorImplemented'] == 'not-implemented-in-profile' for c in unknown))

    def test_reader_is_bounded_and_reads_one_card_without_large_source_input(self):
        listed = registry.query(self.bundle, max_records=3)
        self.assertEqual((listed['total'], listed['returned'], listed['truncated']), (12, 3, True))
        routes = registry.query(self.bundle, service='os-net-api', max_records=5)
        self.assertEqual((routes['total'], routes['returned']), (13, 5))
        read = registry.query(self.bundle, key='oauth-2-api')
        self.assertEqual(read['records'][0]['operationCounts']['retained'], 0)
        limited = registry.query(self.bundle, key='oauth-2-api', max_bytes=1024)
        self.assertEqual(limited['returned'], 0)
        self.assertTrue(limited['truncated'])
        self.assertLessEqual(len(canonical(limited)), 1024)
        with self.assertRaisesRegex(ValueError, 'one exact'):
            registry.query(self.bundle, key='missing')
        with self.assertRaises(ValueError):
            registry.query(self.bundle, max_records=0)

    def test_reader_rejects_modified_cards_index_and_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / 'bundle'
            shutil.copytree(self.bundle, bundle)
            card = next(c for c in self.cards if c['kind'] == 'service')
            card_path = bundle / registry._path(card['@id'], card['kind'])
            card_path.write_text(card_path.read_text() + '\nmodified\n')
            with self.assertRaisesRegex(ValueError, 'integrity mismatch'):
                registry.query(bundle, key=card['@id'])
            index = bundle / 'index.sqlite'
            with sqlite3.connect(index) as db:
                db.execute("UPDATE cards SET title='untrusted changed value'")
            with self.assertRaisesRegex(ValueError, 'index integrity'):
                registry.query(bundle)
            linked = Path(directory) / 'linked'
            linked.symlink_to(self.bundle, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'symlinks'):
                registry.query(linked)

    def test_old_execution_profile_requires_explicit_bundle_regeneration(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / 'bundle'
            shutil.copytree(self.bundle, bundle)
            summary_path = bundle / 'summary.json'
            summary = json.loads(summary_path.read_text())
            summary['schemaVersion'] = 'gis-ai-go.okf-plus-service-registry.v1'
            summary_path.write_bytes(canonical(summary))
            for query in ({}, {'service': 'os-ngd-api-features'}, {'key': 'os-ngd-api-features'}):
                with self.subTest(query=query), self.assertRaisesRegex(ValueError, 'rebuild for the current execution profile'):
                    registry.query(bundle, **query)

    def test_cli_build_list_routes_and_read(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / 'cli'
            script = ROOT / 'scripts/okf_plus/service_registry.py'
            def cli(*args):
                run = subprocess.run([sys.executable, str(script), *args], cwd=ROOT, capture_output=True, text=True, check=True)
                return load_json(run.stdout)
            self.assertEqual(cli('build', '--output', str(bundle))['operationCount'], 60)
            self.assertEqual(cli('list', '--bundle', str(bundle))['total'], 12)
            self.assertEqual(cli('routes', '--bundle', str(bundle), 'os-ngd-api-features')['total'], 8)
            self.assertEqual(cli('read', '--bundle', str(bundle), 'os-names-api')['records'][0]['kind'], 'service')


if __name__ == '__main__':
    unittest.main()
