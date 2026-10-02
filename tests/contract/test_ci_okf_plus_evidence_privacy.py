"""Canonical CI must retain public assurance and exclude private OKF+ evidence."""
import fnmatch
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class OkfPlusCiEvidencePrivacyTests(unittest.TestCase):
    def test_ci_evidence_upload_excludes_private_okf_plus_inputs_and_diagnostics(self):
        workflow = (ROOT / '.github/workflows/ci.yml').read_text()
        block = workflow.split('      - name: Upload generated evidence\n', 1)[1].split('\n  gateway_image:', 1)[0]
        paths = block.split('          path: |\n', 1)[1].split('          if-no-files-found:', 1)[0]
        patterns = [line.strip() for line in paths.splitlines() if line.strip()]
        excluded = [value[1:] for value in patterns if value.startswith('!')]
        private = ('capture/source.body', 'specifications/manifest.json', 'ons-review-probes/0.json',
                   'ons-catalogue-probes/1.body', 'raw/source.json', 'private/account.json',
                   'private-diagnostics/importer-check.log', 'export/PRIVATE-original-documents.tar.gz',
                   'export/nested/PRIVATE-original-documents-manifest.json')
        for relative in private:
            with self.subTest(relative=relative):
                self.assertTrue(any(fnmatch.fnmatchcase('artifacts/okf-plus/' + relative, p) for p in excluded))
        self.assertIn('artifacts/', patterns)
        self.assertIn('apps/public-explorer/test-results/', patterns)
        for public in ('verification.json', 'bundle/source-lock.json', 'context/schema-validation.json',
                       'export/okf-plus-metadata.tar.gz'):
            self.assertFalse(any(fnmatch.fnmatchcase('artifacts/okf-plus/' + public, p) for p in excluded))


if __name__ == "__main__":
    unittest.main()
