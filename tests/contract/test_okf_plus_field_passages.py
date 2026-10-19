from __future__ import annotations
import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/okf_plus'))
SPEC = importlib.util.spec_from_file_location('field_passages', ROOT / 'scripts/okf_plus/field_passages.py')
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
from passages import split_document


class FieldPassageTests(unittest.TestCase):
    def fixture(self, root, body, native='height_m', captured=True):
        cards = root / 'artifacts/cards'
        private = root / 'artifacts/docs'
        cards.mkdir(parents=True)
        private.mkdir(parents=True)
        parent = 'bld-fts-building-4'
        url = M.BINDINGS[parent]
        card = {'@id': 'https://example.org/card', 'parent': {'@id': 'https://example.org/' + parent,
                'nativeIdentifier': parent}, 'field': {'@id': 'https://example.org/field',
                'dcterms:identifier': native}}
        raw = M.canonical(card)
        (cards / 'card.jsonld').write_bytes(raw)
        (cards / 'index.json').write_bytes(M.canonical({'cards': [{'parent': card['parent']['@id'],
            'path': 'card.jsonld', 'id': card['field']['@id'], 'sha256': hashlib.sha256(raw).hexdigest()}]}))
        records = {}
        if captured:
            source = root / 'source.md'
            source.write_bytes(body.encode())
            manifest, parts = split_document(source.read_bytes(), url)
            destination = private / 'passages/doc'
            destination.mkdir(parents=True)
            (destination / 'manifest.jsonld').write_bytes(M.canonical(manifest))
            for segment, payload in zip(manifest['segments'], parts):
                (destination / segment['file']).write_bytes(payload)
            records[url] = {'status': 'captured', 'passageDirectory': 'passages/doc',
                            'receipt': {'sha256': manifest['source']['sha256']}}
        (private / 'checkpoint.json').write_bytes(M.canonical({'records': records}))
        return cards, private, url

    def test_exact_escaped_heading_includes_descendant_section_and_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cards, private, url = self.fixture(root, '# Building\n## `height\\_m`\nDefinition\n### Detail\nMore\n## Other\nExcluded\n')
            row = M.overlays(cards, private)[0]
            self.assertEqual(row['status'], 'matched')
            self.assertEqual(len(row['passages']), 4)
            self.assertEqual(row['source']['url'], url)
            self.assertEqual(row['source']['sha256'], hashlib.sha256((root/'source.md').read_bytes()).hexdigest())
            self.assertEqual(row['binding']['versionStatus'], 'current-document-not-independently-version-matched')
            self.assertTrue(all('text' not in p for p in row['passages']))
            self.assertTrue(all(p['sha256'] and p['position'] and p['@id'] for p in row['passages']))
            self.assertFalse(row['rights']['publicationAdmitted'])

    def test_unicode_exact_match_and_substring_refusal(self):
        for native, expected in [('hauteur_é', 'matched'), ('hauteur', 'heading-not-found'),
                                 ('HAUTEUR_É', 'heading-not-found')]:
            with self.subTest(native=native), tempfile.TemporaryDirectory() as tmp:
                cards, private, _ = self.fixture(Path(tmp), '# Building\n## hauteur\\_é\nDéfinition\n', native)
                self.assertEqual(M.overlays(cards, private)[0]['status'], expected)

    def test_duplicate_heading_is_ambiguous_without_selecting_passages(self):
        with tempfile.TemporaryDirectory() as tmp:
            cards, private, _ = self.fixture(Path(tmp), '# Building\n## height_m\nOne\n## height_m\nTwo\n')
            row = M.overlays(cards, private)[0]
            self.assertEqual(row['status'], 'ambiguous-heading')
            self.assertEqual(row['passages'], [])

    def test_missing_document_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            cards, private, _ = self.fixture(Path(tmp), '', captured=False)
            row = M.overlays(cards, private)[0]
            self.assertEqual(row['status'], 'document-not-captured')
            self.assertEqual(row['passages'], [])

    def test_rehashed_modified_passage_cannot_keep_original_source_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            cards, private, _ = self.fixture(Path(tmp), '# Building\n## height_m\nDefinition\n')
            manifest_path = private / 'passages/doc/manifest.jsonld'
            manifest = M.read(manifest_path)
            segment = manifest['segments'][-1]
            path = private / 'passages/doc' / segment['file']
            payload = M.read(path)
            payload['text'] = 'Altered definition\n'
            raw = M.canonical(payload)
            path.write_bytes(raw)
            segment['sha256'] = hashlib.sha256(raw).hexdigest()
            segment['bytes'] = len(raw)
            manifest_path.write_bytes(M.canonical(manifest))
            with self.assertRaisesRegex(ValueError, 'reconstruction checksum'):
                M.overlays(cards, private)

    def test_tampered_passage_and_symlink_output_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cards, private, _ = self.fixture(root, '# Building\n## height_m\nDefinition\n')
            output = root / 'artifacts/overlays'
            summary = M.export(root, cards, private, output)
            leaf = output / summary['files'][0]['path']
            leaf.unlink()
            target = root / 'outside'
            target.write_text('retain')
            leaf.symlink_to(target)
            with self.assertRaisesRegex(ValueError, 'Symbolic link'):
                M.export(root, cards, private, output)
            self.assertEqual(target.read_text(), 'retain')
            part = next((private/'passages/doc').glob('part-*.jsonld'))
            part.write_text('{}')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                M.overlays(cards, private)

if __name__ == '__main__':
    unittest.main()
