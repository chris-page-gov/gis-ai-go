"""Independent digest checks and safe publication of the atomic OS projection."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
from jsonschema import ValidationError

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/okf_plus'))
import verify_semantics as VERIFY
from model import canonical, digest, markdown_text, read_markdown
import semantic


class AtomicVerifierTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source_path = self.root / 'okf-plus/source/os-synthetic.json'
        self.source_path.parent.mkdir(parents=True)
        self.schema_path = self.root / 'okf-plus/schemas/semantic-card.schema.json'
        self.schema_path.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / 'okf-plus/schemas/semantic-card.schema.json', self.schema_path)
        self.snapshot = {'schema': 'okf-plus-source-snapshot.v1', 'family': 'os-synthetic',
                         'records': [{'id': 'synthetic-measurement',
                                      'title': 'Pavement width, building heights and road height above sea level',
                                      'url': 'https://example.org/synthetic-metadata',
                                      'measurement': {'unit': 'metres', 'nullable': True}}], 'receipts': []}
        self.source_path.write_bytes(canonical(self.snapshot))
        self.output = self.root / 'artifacts/atomic'
        self.revision = 'd' * 40

    def generate(self):
        return semantic.generate_semantic(self.root, self.output, self.revision)

    def mutate_card(self, change, directory=None):
        path = next(((directory or self.output) / 'cards').glob('*/*.md'))
        card, body = read_markdown(path)
        change(card)
        path.write_text(markdown_text(card, body))
        return path

    def files(self):
        return {path.relative_to(self.output).as_posix(): path.read_bytes()
                for path in self.output.rglob('*') if path.is_file()}

    def supplement_evidence(self, definition):
        return {'snapshot': 'okf-plus/source/supplement.json', 'pointer': '/definition',
                'sha256': digest(definition), 'status': 'source-backed-curated-paraphrase-not-schema-assertion',
                'sources': [{'id': 'synthetic-source', 'url': 'https://example.org/synthetic-definition',
                             'evidenceExcerpt': definition,
                             'evidenceSha256': hashlib.sha256(definition.encode()).hexdigest(),
                             'hashScope': 'UTF-8 synthetic evidenceExcerpt only'}]}

    def test_audit_recomputes_source_values_instead_of_trusting_reported_counts(self):
        coverage = self.generate()
        audit = VERIFY.verify_cards(self.root, self.output)
        self.assertEqual(audit['recordsChecked'], 1)
        self.assertEqual(audit['recordsChecked'], coverage['cardCount'])
        self.assertEqual(audit['sourceSnapshotsChecked'], 1)
        changed = deepcopy(self.snapshot)
        changed['records'][0]['measurement']['unit'] = 'feet'
        self.source_path.write_bytes(canonical(changed))
        with self.assertRaisesRegex(ValueError, 'source value digest'):
            VERIFY.verify_cards(self.root, self.output)

    def test_containing_record_digest_is_checked_separately_from_field_value(self):
        self.generate()
        measurement = self.snapshot['records'][0]['measurement']
        def make_leaf(card):
            card['source']['pointer'] += '/measurement'
            card['source']['sha256'] = digest(measurement)
        self.mutate_card(make_leaf)
        VERIFY.verify_cards(self.root, self.output)
        changed = deepcopy(self.snapshot)
        changed['records'][0]['title'] = 'Changed containing source record'
        self.source_path.write_bytes(canonical(changed))
        with self.assertRaisesRegex(ValueError, 'source record digest'):
            VERIFY.verify_cards(self.root, self.output)

    def test_unmapped_emitted_term_is_rejected(self):
        self.generate()
        self.mutate_card(lambda card: card.update(unregisteredFieldMeaning='Unmapped semantic claim'))
        with self.assertRaises((ValueError, ValidationError)):
            VERIFY.verify_cards(self.root, self.output)

    def test_missing_reviewed_schema_fails_and_preserves_previous_build(self):
        VERIFY.verify(self.root, self.output, self.revision)
        before = self.files()
        self.schema_path.unlink()
        with self.assertRaisesRegex(ValueError, '[Rr]equired semantic card schema'):
            VERIFY.verify(self.root, self.output, self.revision)
        self.assertEqual(self.files(), before)

    def test_schema_rejects_invalid_card_types_independently_of_source_digests(self):
        self.generate()
        self.mutate_card(lambda card: card.update(gaps='Missing facts must be a list, not text'))
        with self.assertRaises(ValidationError):
            VERIFY.verify_cards(self.root, self.output)

    def test_missing_or_remapped_emitted_context_term_is_rejected(self):
        self.generate()
        context_path = self.output / 'context.jsonld'
        original = json.loads(context_path.read_text())
        for mutation in ('missing', 'remapped'):
            with self.subTest(mutation=mutation):
                changed = deepcopy(original)
                if mutation == 'missing':
                    del changed['@context']['source']
                else:
                    changed['@context']['source'] = 'https://example.org/incorrect-meaning'
                context_path.write_bytes(canonical(changed))
                with self.assertRaisesRegex(ValueError, '[Cc]ontext'):
                    VERIFY.verify_cards(self.root, self.output)

    def test_supplement_digest_is_independent_of_primary_schema_evidence(self):
        self.generate()
        supplement_path = self.source_path.parent / 'supplement.json'
        supplement = {'definition': 'Synthetic definition, not a native API value'}
        supplement_path.write_bytes(canonical(supplement))
        self.mutate_card(lambda card: card.update(semanticEvidence=self.supplement_evidence(supplement['definition'])))
        VERIFY.verify_cards(self.root, self.output)
        supplement['definition'] = 'A different meaning'
        supplement_path.write_bytes(canonical(supplement))
        with self.assertRaisesRegex(ValueError, 'Semantic evidence digest'):
            VERIFY.verify_cards(self.root, self.output)

    def test_supplement_symlink_cannot_bypass_source_path_checks(self):
        self.generate()
        other_path = self.root / 'not-an-admitted-source.json'
        other_path.write_bytes(canonical({'definition': 'Synthetic'}))
        (self.source_path.parent / 'supplement.json').symlink_to(other_path)
        self.mutate_card(lambda card: card.update(semanticEvidence=self.supplement_evidence('Synthetic')))
        with self.assertRaisesRegex(ValueError, '[Ss]emantic evidence|[Ss]upplement'):
            VERIFY.verify_cards(self.root, self.output)

    def test_failed_staged_audit_preserves_every_byte_of_previous_build(self):
        first = VERIFY.verify(self.root, self.output, self.revision)
        self.assertEqual(first['status'], 'passed')
        before = self.files()
        generate = VERIFY.generate_semantic
        def corrupt_staged(root, directory, revision):
            coverage = generate(root, directory, revision)
            self.mutate_card(lambda card: card['source'].update(sha256='0' * 64), directory)
            return coverage
        with patch.object(VERIFY, 'generate_semantic', side_effect=corrupt_staged):
            with self.assertRaisesRegex(ValueError, 'source value digest'):
                VERIFY.verify(self.root, self.output, self.revision)
        self.assertEqual(self.files(), before)
        self.assertFalse(list(self.output.parent.glob('.okf-atomic-*')))

    def test_failed_directory_replacement_restores_previous_build(self):
        VERIFY.verify(self.root, self.output, self.revision)
        before = self.files()
        rename = Path.rename
        def fail_staged(source, target):
            if source.name == 'staged' and Path(target) == self.output:
                raise OSError('Synthetic final replacement failure')
            return rename(source, target)
        with patch.object(Path, 'rename', fail_staged):
            with self.assertRaisesRegex(OSError, 'Synthetic final replacement'):
                VERIFY.verify(self.root, self.output, self.revision)
        self.assertEqual(self.files(), before)

    def test_empty_projection_unmarked_output_and_oversized_cards_are_rejected(self):
        self.output.mkdir(parents=True)
        context = self.output / 'context.jsonld'
        context.write_bytes(canonical({'@context': semantic.CONTEXT}))
        with self.assertRaisesRegex(ValueError, 'No atomic records'):
            VERIFY.verify_cards(self.root, self.output)
        marker = self.output / 'user-file.txt'
        marker.write_text('Preserve unrelated content')
        with self.assertRaisesRegex(ValueError, 'unmarked output'):
            VERIFY.verify(self.root, self.output, self.revision)
        self.assertEqual(marker.read_text(), 'Preserve unrelated content')
        marker.unlink()
        context.unlink()
        self.generate()
        path = next((self.output / 'cards').glob('*/*.md'))
        path.write_bytes(path.read_bytes() + b'x' * semantic.MAX_CARD_BYTES)
        with self.assertRaisesRegex(ValueError, 'Oversized atomic'):
            VERIFY.verify_cards(self.root, self.output)


if __name__ == '__main__':
    unittest.main()
