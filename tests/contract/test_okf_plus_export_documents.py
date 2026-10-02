"""Private originals are separate, admitted, exact and credential-free."""
import importlib.util
import json
from pathlib import Path
import stat
import sys
import tarfile
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/okf_plus'))
SPEC = importlib.util.spec_from_file_location('okf_plus_private_export_tests', ROOT / 'scripts/okf_plus/export_documents.py')
PRIVATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PRIVATE)
URL = 'https://docs.os.uk/os-apis/synthetic-guide.md'


def fixture(root, raw=b'# Synthetic public guide\n', url=URL):
    scanner = root / 'scripts/scan_secrets.py'; scanner.parent.mkdir(parents=True)
    scanner.write_bytes((ROOT / 'scripts/scan_secrets.py').read_bytes())
    capture = root / 'artifacts/okf-plus/capture'; capture.mkdir(parents=True)
    checksum = PRIVATE.sha(raw); (capture / (checksum + '.body')).write_bytes(raw)
    receipt = {'url': url, 'status': 200, 'retrievedAt': '2026-10-02T00:00:00Z',
               'bytes': len(raw), 'sha256': checksum}
    excluded = {'url': 'https://api.os.uk/downloads/v1/products', 'status': 200,
                'retrievedAt': receipt['retrievedAt'], 'sha256': 'a' * 64, 'bytes': 999}
    (capture / 'ledger.json').write_text(json.dumps({'requests': [receipt, excluded]}))
    return receipt


class PrivateOriginalExportTests(unittest.TestCase):
    def test_only_docs_are_included_with_private_modes_and_relocatable_bytes(self):
        archives = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory); fixture(root); output = root / 'artifacts/okf-plus/export'
                ledger = root / 'artifacts/okf-plus/capture/ledger.json'; before = ledger.read_bytes()
                receipt = PRIVATE.export_documents(root, output)
                self.assertEqual(receipt['originalDocuments'], 1)
                self.assertEqual(ledger.read_bytes(), before)
                for path in output.iterdir():
                    self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
                path = output / receipt['archive']['path']; archives.append(path.read_bytes())
                manifest = PRIVATE.verify_archive(path, PRIVATE.SCHEMA)
                self.assertEqual(manifest['publication'], 'owner-private-no-publication')
                self.assertEqual(manifest['provenance'][0]['sourceUrl'], URL)
                with tarfile.open(path) as archive:
                    self.assertTrue(all(m.mode == 0o600 for m in archive))
        self.assertEqual(*archives)

    def test_unadmitted_document_route_and_tampered_raw_response_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); receipt = fixture(root, url='https://docs.os.uk/os-apis/private.json')
            with self.assertRaises(ValueError): PRIVATE.collect(root)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); receipt = fixture(root)
            (root / 'artifacts/okf-plus/capture' / (receipt['sha256'] + '.body')).write_bytes(b'Changed')
            with self.assertRaises(ValueError): PRIVATE.collect(root)

    def test_exact_reviewed_placeholder_allowed_but_realistic_synthetic_token_rejected(self):
        patterns = PRIVATE.public_patterns(ROOT)
        text = ('api' + 'Key = ' + json.dumps('INSERT_API_KEY_HERE')).encode()
        self.assertEqual(PRIVATE.credential_check(text, patterns), 1)
        token = ('s' + 'k-' + 'x' * 24).encode()
        with self.assertRaises(ValueError): PRIVATE.credential_check(token, patterns)
        unreviewed = ('api' + 'Key = ' + json.dumps('unreviewed-synthetic-value')).encode()
        with self.assertRaises(ValueError): PRIVATE.credential_check(unreviewed, patterns)

    def test_unpinned_specification_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); fixture(root)
            path = root / 'artifacts/okf-plus/specifications'; path.mkdir()
            (path / 'manifest.json').write_text(json.dumps({
                'schema': 'gis-ai-go.okf-plus-retained-specifications.v1', 'files': [{
                    'repository': 'https://example.org/not-official', 'commit': 'b' * 40,
                    'repositoryPath': 'swagger.yaml', 'status': 200, 'sha256': 'a' * 64}]}))
            with self.assertRaises(ValueError): PRIVATE.collect(root)

    def test_count_and_total_byte_limits_are_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); fixture(root)
            with mock.patch.object(PRIVATE, 'MAX_TOTAL_BYTES', 4), self.assertRaises(ValueError):
                PRIVATE.collect(root)
            with mock.patch.object(PRIVATE, 'MAX_DOCUMENTS', 0), self.assertRaises(ValueError):
                PRIVATE.collect(root)

    def test_a_redirected_receipt_cannot_assert_the_requested_document_origin(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); fixture(root)
            ledger_path = root / 'artifacts/okf-plus/capture/ledger.json'
            ledger = json.loads(ledger_path.read_text())
            ledger['requests'][0]['finalUrl'] = 'https://example.org/other-document'
            ledger_path.write_text(json.dumps(ledger))
            with self.assertRaises(ValueError): PRIVATE.collect(root)

    def test_public_archive_verifier_does_not_mislabel_private_originals(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); fixture(root); output = root / 'artifacts/okf-plus/export'
            receipt = PRIVATE.export_documents(root, output)
            with self.assertRaises(ValueError): PRIVATE.verify_archive(output / receipt['archive']['path'])


if __name__ == '__main__':
    unittest.main()
