"""Candidate output metadata stays small, source-bound and non-executable."""
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]


class OutputIntentTests(unittest.TestCase):
    def test_profile_is_small_and_does_not_grant_execution_or_rendering(self):
        path = ROOT / 'okf-plus/profile/os-output-intents.json'
        self.assertLessEqual(path.stat().st_size, 16384)
        profile = json.loads(path.read_text())
        self.assertFalse(profile['policy']['executionAdmitted'])
        self.assertFalse(profile['policy']['rendererImplemented'])
        self.assertFalse(profile['policy']['routeUrlsExecutable'])
        for key in ['@id', '@context', 'owner', 'threats', 'rights', 'requiredUnderstanding']:
            self.assertTrue(profile[key])
        intents = {item['id']: item for item in profile['intents']}
        self.assertNotEqual(intents['exact-table']['candidateRoutes'], intents['contextual-map']['candidateRoutes'])
        self.assertTrue(all(item['status'] == 'recommendation' and item['requires'] and
                            item['rejectAssumption'] for item in intents.values()))

    def test_evidence_matches_committed_source_and_successful_capture_receipt(self):
        profile = json.loads((ROOT / 'okf-plus/profile/os-output-intents.json').read_text())
        for item in profile['evidence']:
            snapshot = json.loads((ROOT / item['snapshot']).read_text())
            record = snapshot['records'][int(item['pointer'].split('/')[-1])]
            self.assertEqual(record['url'], item['sourceUrl'])
            self.assertEqual(record['sourceSha256'], item['sourceSha256'])
            self.assertTrue(any(r['url'] == item['sourceUrl'] and r.get('sha256') == item['sourceSha256']
                                and r['status'] == 200 for r in snapshot['receipts']))

if __name__ == '__main__':
    unittest.main()
