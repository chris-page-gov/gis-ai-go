from __future__ import annotations
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
NAMES = ['os-ngd', 'os-wfs', 'os-download']


def pointer(document, path):
    for part in path.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        document = document[int(part)] if isinstance(document, list) else document[part]
    return document


def evidence_nodes(value):
    if isinstance(value, dict):
        if {'snapshot', 'pointer', 'sourceSha256', 'sourceUrl'} <= value.keys():
            yield value
        for item in value.values():
            yield from evidence_nodes(item)
    elif isinstance(value, list):
        for item in value:
            yield from evidence_nodes(item)


class QueryCapabilitiesTests(unittest.TestCase):
    def load(self, name):
        return json.loads((ROOT / f'okf-plus/profile/{name}-query-capabilities.json').read_text())

    def test_small_linked_profiles_carry_rights_policy_and_no_execution_grant(self):
        for name in NAMES:
            with self.subTest(name=name):
                path = ROOT / f'okf-plus/profile/{name}-query-capabilities.json'
                self.assertLessEqual(path.stat().st_size, 16384)
                profile = self.load(name)
                self.assertTrue(profile['@id'].startswith('https://'))
                self.assertIn('@context', profile)
                self.assertFalse(profile['policy']['executionAdmitted'])
                for key in ['owner', 'rights', 'threats', 'status', 'retentionIntent', 'unverified']:
                    self.assertTrue(profile[key])

    def test_all_evidence_pointers_and_original_capture_hash_receipts_match(self):
        for name in NAMES:
            for evidence in evidence_nodes(self.load(name)):
                with self.subTest(name=name, pointer=evidence['pointer']):
                    snapshot = json.loads((ROOT / evidence['snapshot']).read_text())
                    self.assertIsNotNone(pointer(snapshot, evidence['pointer']))
                    record_path = '/'.join(evidence['pointer'].split('/')[:3])
                    record = pointer(snapshot, record_path)
                    self.assertEqual(record['sourceSha256'], evidence['sourceSha256'])
                    self.assertEqual(record['url'], evidence['sourceUrl'])
                    self.assertTrue(any(r.get('sha256') == evidence['sourceSha256'] and
                        r['url'] == evidence['sourceUrl'] and r['status'] == 200 and
                        r['retrievedAt'] == evidence['retrievedAt'] for r in snapshot['receipts']))

    def resolve(self, evidence):
        return pointer(json.loads((ROOT / evidence['snapshot']).read_text()), evidence['pointer'])

    def test_ngd_parameter_language_and_limit_claims_match_native_contract(self):
        capabilities = self.load('os-ngd')['capabilities']
        params = self.resolve(capabilities['items']['evidence'])
        self.assertEqual(capabilities['items']['parameters'], [p['name'] for p in params])
        self.assertFalse({'properties', 'select', 'propertyName'} & {p['name'] for p in params})
        language = self.resolve(capabilities['filter']['evidence'])
        self.assertEqual(capabilities['filter']['languages'], language['schema']['enum'])
        limit = self.resolve(capabilities['limits']['evidence'])
        self.assertEqual(capabilities['limits']['maxFeatures'], limit['schema']['maximum'])
        self.assertEqual(capabilities['limits']['minFeatures'], limit['schema']['minimum'])
        self.assertEqual(params[0]['schema']['type'], 'string')
        self.assertTrue(params[0]['schema']['enum'])

    def test_wfs_projection_and_download_supply_types_are_source_native(self):
        wfs = self.load('os-wfs')['capabilities']
        self.assertEqual(self.resolve(wfs['projection']['evidence'])['name'], 'propertyName')
        self.assertEqual(self.resolve(wfs['paging']['evidence'])['schema']['maximum'], wfs['paging']['countMaximum'])
        self.assertEqual(self.resolve(wfs['counts']['evidence'])['schema']['enum'], wfs['counts']['values'])
        downloads = self.load('os-download')['capabilities']
        self.assertEqual(self.resolve(downloads['supplyTypes']['evidence']), downloads['supplyTypes']['values'])
        for operation in downloads['operations']:
            native = self.resolve(operation['evidence'])
            self.assertEqual(native['path'], operation['path'])
            self.assertEqual(native['method'], operation['method'])

if __name__ == '__main__':
    unittest.main()
