"""Lossless private evidence and boundary contracts, using synthetic source text."""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/okf_plus'))
import passages
from model import load_json

URL = 'https://docs.os.uk/osngd/synthetic.md'


class PrivatePassageTests(unittest.TestCase):
    def assert_reconstruction(self, raw, limit=4096):
        manifest, parts = passages.split_document(raw, URL, max_bytes=limit)
        decoded = [load_json(part.decode()) for part in parts]
        self.assertEqual(b''.join(p['text'].encode() for p in decoded), raw)
        self.assertEqual(manifest['source']['sha256'], hashlib.sha256(raw).hexdigest())
        self.assertTrue(manifest['reconstruction']['verified'])
        previous = 0
        for segment, encoded, part in zip(manifest['segments'], parts, decoded):
            self.assertLessEqual(len(encoded), limit)
            self.assertEqual(segment['sha256'], hashlib.sha256(encoded).hexdigest())
            pos = part['position']
            self.assertEqual(pos['byteStart'], previous)
            self.assertEqual(raw[pos['byteStart']:pos['byteEnd']], part['text'].encode())
            previous = pos['byteEnd']
            self.assertFalse(part['trust']['executionAdmitted'])
            self.assertEqual(part['distribution']['audience'], 'private')
        self.assertEqual(previous, len(raw))
        return manifest, decoded

    def test_exact_original_bytes_and_heading_ancestry(self):
        raw = b'\xef\xbb\xbfPreamble\r\n# Heading\r\n\r\n## Child\nvalue\rno-final-newline'
        _, parts = self.assert_reconstruction(raw)
        self.assertEqual(parts[-1]['headingBreadcrumb'], [
            {'level': 1, 'text': 'Heading', 'line': 2},
            {'level': 2, 'text': 'Child', 'line': 4}])
        self.assertEqual(parts[-1]['position']['lineStart'], 6)

    def test_unicode_long_line_split_offsets_and_no_truncation(self):
        text = '# Cymru\n' + '😀é漢字\\"\t' * 3000 + '\r\nlast'
        manifest, parts = self.assert_reconstruction(text.encode())
        self.assertGreater(len(parts), 10)
        chars = 0
        for part in parts:
            pos = part['position']
            self.assertEqual(pos['characterStart'], chars)
            self.assertEqual(text[pos['characterStart']:pos['characterEnd']], part['text'])
            chars = pos['characterEnd']
        self.assertEqual(chars, len(text))
        self.assertEqual(manifest, passages.split_document(text.encode(), URL, max_bytes=4096)[0])

    def test_fenced_headings_are_preserved_as_evidence_only(self):
        _, parts = self.assert_reconstruction(b'# Real\n```sh\n# Fake\nrm -rf /\n```\nlast')
        self.assertEqual(parts[-1]['headingBreadcrumb'][0]['text'], 'Real')
        self.assertIn('rm -rf /', ''.join(p['text'] for p in parts))

    def test_empty_source_is_verifiably_empty(self):
        manifest, parts = self.assert_reconstruction(b'')
        self.assertEqual(parts, [])
        self.assertEqual(manifest['segments'], [])

    def test_invalid_inputs_fail_instead_of_truncating(self):
        for url in ('https://evil.invalid/osngd/a.md', URL + '?key=secret',
                    'http://docs.os.uk/osngd/a.md', 'https://docs.os.uk/osngd/../a.md'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                passages.split_document(b'test', url)
        for limit in (0, -1, True, 100):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                passages.split_document(b'test', URL, max_bytes=limit)
        with self.assertRaises(UnicodeDecodeError):
            passages.split_document(b'\xff', URL)

    def test_private_output_refuses_symlinks_overwrites_and_public_paths(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(passages, 'ROOT', Path(directory)):
            root = Path(directory)
            source = root / 'source.md'
            source.write_bytes(b'# Synthetic\r\nExample')
            output = root / 'artifacts/private/passages'
            manifest = passages.write_document(source, URL, output)
            disk = load_json((output / 'manifest.jsonld').read_text())
            self.assertEqual(disk, manifest)
            rebuilt = b''.join(load_json((output / s['file']).read_text())['text'].encode()
                               for s in disk['segments'])
            self.assertEqual(rebuilt, source.read_bytes())
            with self.assertRaises(ValueError):
                passages.write_document(source, URL, output)
            with self.assertRaises(ValueError):
                passages.write_document(source, URL, root / 'public')
            with self.assertRaises(ValueError):
                passages.write_document(source, URL, root / 'artifacts/../public')
            alias = root / 'alias.md'
            alias.symlink_to(source)
            with self.assertRaises(ValueError):
                passages.write_document(alias, URL, root / 'artifacts/other')
            (root / 'artifacts/link').symlink_to(root, target_is_directory=True)
            with self.assertRaises(ValueError):
                passages.write_document(source, URL, root / 'artifacts/link/output')


if __name__ == '__main__':
    unittest.main()
