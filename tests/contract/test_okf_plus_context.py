"""Whole-corpus projection, evidence integrity and vendored pinned-engine checks."""
from copy import deepcopy
import gzip
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from scripts.okf_plus.context_projection import (
    VENDOR_ROOT, canonical, install, pinned_contract, project, sha, validate_outputs,
    vendor_files, verify_engine,
)

BASE = 'https://example.test/okf-plus/context/'
CAPTURED = '2026-10-02T12:00:00Z'


def fixture(count=41):
    records = []; parents = []
    for number in range(count):
        native = 'TAIL999' if number == count - 1 else f'ITEM{number:03d}'
        identifier = f'https://example.test/metadata/{number:05d}'
        source = {'resource': 'https://example.test/catalogue', 'responseSha256': 'a' * 64,
                  'retrievedAt': '2026-10-01T01:02:03Z', 'sourcePointer': f'/items/{number}',
                  'sourcePointerStatus': 'exact-native-id-match'}
        common = {'title': native + ' metadata', 'description': 'Clearly synthetic metadata.',
            'type': 'Concept' if number == 0 else 'Dataset', 'sourceFamily': 'synthetic',
            'nativeIdentifier': native, 'sources': [source],
            'temporal': {'status': 'source-stated', 'start': '1999-01', 'end': '2026-08', 'kind': 'native-period-options'},
            'update': {'frequency': {'status': 'source-stated', 'label': 'Monthly'},
                       'releaseCatalogue': ['https://example.test/releases'], 'releaseFeed': ['https://example.test/feed'],
                       'nextRelease': 'TBC', 'metadataModified': '2026-10-01', 'releaseVersion': '7'},
            'details': {'native': native, 'nullField': None}, 'tags': [native],
            'resource': 'https://example.test/catalogue/' + native,
            'rights': {'metadata': 'CC0 synthetic fixture', 'describedData': 'No observation entitlement.',
                       'executionAdmitted': False}, 'limitations': ['Synthetic; no observations.']}
        parents.append({'@id': identifier, 'assertionStatus': 'normalised', 'reviewStatus': 'synthetic', **deepcopy(common)})
        records.append({'id': identifier, 'route': f'records/synthetic/{native}.md',
                        'text': f'# {native}\n\nWhole synthetic metadata passage with final caveat.\n', **common})
    identity = {'revision': 'b' * 40, 'inputDigest': 'c' * 64}
    return ({'schema': 'gis-ai-go.okf-plus-search-index.v1', **identity, 'records': records},
            {'schema': 'gis-ai-go.okf-plus-bundle.v1', **identity, 'recordCount': count, 'records': parents})


class ProjectionTests(unittest.TestCase):
    def produce(self, count=41):
        search, bundle = fixture(count)
        return search, bundle, *project(search, bundle, base_url=BASE, captured_at=CAPTURED)

    def test_every_input_record_has_whole_metadata_and_verified_passage(self):
        search, bundle, outputs, review = self.produce()
        manifest = json.loads(outputs['manifest.json']); records = []
        for reference in manifest['records']['shards']:
            raw = outputs[reference['path']]; decoded = gzip.decompress(raw)
            self.assertEqual(sha(raw), reference['sha256'])
            self.assertEqual(sha(decoded), reference['decoded_sha256'])
            records.extend(json.loads(decoded)['records'])
        self.assertEqual(len(records), 41)
        self.assertEqual(review['wholeCorpus']['omittedRecordIds'], [])
        for row, parent, record in zip(search['records'], bundle['records'], records):
            self.assertTrue(record['text'].startswith(row['text']))
            self.assertIn(canonical(parent).decode(), record['text'])
            span = record['evidence_unit']['spans'][0]
            self.assertEqual(sha(record['text'].encode()), span['literal_sha256'])
            self.assertEqual(len(record['text'].encode()), span['unit_end'])
            self.assertEqual(outputs[span['source_url'].removeprefix(BASE)], record['text'].encode())
            self.assertEqual(json.loads(record['rights']), row['rights'])
        self.assertIn(search['records'][-1]['id'], review['representativeIndex']['omittedInputIds'])

    def test_snapshot_pair_mismatch_and_missing_records_fail(self):
        search, bundle = fixture()
        bundle['records'][3]['update']['nextRelease'] = 'incorrect replacement'
        with self.assertRaisesRegex(ValueError, 'field mismatch'):
            project(search, bundle, base_url=BASE, captured_at=CAPTURED)
        search, bundle = fixture()
        bundle['records'][3]['schemaEvidence'] = {'dimensions': ['TIME']}
        with self.assertRaisesRegex(ValueError, 'Schema evidence differs'):
            project(search, bundle, base_url=BASE, captured_at=CAPTURED)
        search, bundle = fixture(); bundle['records'].pop()
        with self.assertRaisesRegex(ValueError, 'identities'):
            project(search, bundle, base_url=BASE, captured_at=CAPTURED)

    def test_oversized_evidence_fails_instead_of_truncating(self):
        search, bundle = fixture(1); search['records'][0]['text'] = 'x' * 100001
        with self.assertRaisesRegex(ValueError, 'do not truncate'):
            project(search, bundle, base_url=BASE, captured_at=CAPTURED)

    def test_unbound_upstream_sources_remain_explicit_and_retained(self):
        search, bundle = fixture(1)
        for row in (search['records'][0], bundle['records'][0]):
            del row['sources'][0]['responseSha256']
        outputs, review = project(search, bundle, base_url=BASE, captured_at=CAPTURED)
        self.assertEqual(len(review['wholeCorpus']['sourceFieldBindingOmissions']), 1)
        record = json.loads(gzip.decompress(outputs['records/00000.json.gz']))['records'][0]
        self.assertIn('exact-native-id-match', record['text'])
        self.assertEqual(record['assertion_status'], 'normalized')

    def test_repeated_build_is_byte_identical_and_all_entrypoints_hash_bound(self):
        search, bundle, outputs, review = self.produce(3)
        again, _ = project(search, bundle, base_url=BASE, captured_at=CAPTURED)
        self.assertEqual(outputs, again)
        entrypoints = json.loads(outputs['descriptor-entrypoints.json'])
        for reference in entrypoints['entrypoints'].values():
            self.assertEqual(sha(outputs[reference['path']]), reference['sha256'])
        self.assertEqual(entrypoints['projectionManifest']['sha256'], sha(outputs['projection-manifest.json']))

    def test_installer_refuses_unmarked_directory(self):
        _, _, outputs, _ = self.produce(1)
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, 'unmarked'):
                install(outputs, Path(temporary))


class PinnedCompatibilityTests(unittest.TestCase):
    def test_tail_metadata_and_budget_refusal_with_actual_pinned_engine(self):
        search, bundle = fixture()
        outputs, _ = project(search, bundle, base_url=BASE, captured_at=CAPTURED)
        checks, pins = pinned_contract()
        validation = validate_outputs(outputs, checks)
        self.assertEqual(validation['allEvidenceRecordsValidated'], 41)
        self.assertGreater(len(pins), 5)
        cases = [
            {'question': 'TAIL999', 'expectedId': search['records'][-1]['id'],
             'requiredText': ['1999-01', '2026-08', 'https://example.test/feed', 'Monthly', 'TBC', 'No observation entitlement.']},
            {'question': 'ITEM000 metadata', 'expectedId': search['records'][0]['id']},
            {'question': 'unrecognised outside corpus question', 'expectInsufficient': True},
            {'question': 'ITEM000 metadata TAIL999', 'budget': {'max_nodes': 1}, 'expectOmission': True, 'expectInsufficient': True},
        ]
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'corpus'; install(outputs, path)
            report = verify_engine(path, cases)
            self.assertEqual(report['status'], 'passed')
            self.assertEqual(report['networkCalls'], 0)
            self.assertEqual(report['results'][0]['corpusRecords'], 41)

    def test_changed_vendor_bytes_fail_before_engine_execution(self):
        with tempfile.TemporaryDirectory() as temporary:
            copied = Path(temporary) / 'vendor'; shutil.copytree(VENDOR_ROOT, copied)
            source = copied / 'apps/okf-explorer/src/lib/context/index.ts'
            source.write_bytes(source.read_bytes() + b'\n// altered synthetic copy\n')
            with self.assertRaisesRegex(ValueError, 'source checksum mismatch'):
                vendor_files(copied)

    def test_changed_vendor_manifest_cannot_rebind_engine_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            copied = Path(temporary) / 'vendor'; shutil.copytree(VENDOR_ROOT, copied)
            manifest = copied / 'manifest.json'
            manifest.write_bytes(manifest.read_bytes() + b'\n')
            with self.assertRaisesRegex(ValueError, 'manifest checksum mismatch'):
                pinned_contract(copied)


if __name__ == '__main__':
    unittest.main()
