from __future__ import annotations
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/okf_plus'))
SPEC = importlib.util.spec_from_file_location('field_cards', ROOT / 'scripts/okf_plus/field_cards.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FieldCardTests(unittest.TestCase):
    def fixture(self, root, description='Pavement width in metres'):
        snapshot = root / 'okf-plus/source/collections.json'
        snapshot.parent.mkdir(parents=True)
        snapshot.write_text('{"records":[]}\n')
        parent = {'@context': 'https://example.org/context', '@id': 'https://example.org/collection',
                  'nativeIdentifier': 'native-collection-v1', 'resource': 'https://example.org/collection',
                  'sources': [{'normalisedSource': snapshot.relative_to(root).as_posix(),
                               'normalisedRecordSha256': 'a' * 64}],
                  'schemaEvidence': {'schema': {'resource': 'https://example.org/schema', 'responseSha256': 'b' * 64}},
                  'rights': {'retrievalAuthority': 'metadata-only'}, 'limitations': ['Synthetic evidence'],
                  'okfp:field': [{'@id': 'https://example.org/collection/field/width',
                                  'dcterms:identifier': 'width', 'okfp:queryable': False,
                                  'prov:wasDerivedFrom': {'@id': 'https://example.org/schema'},
                                  'okfp:schemaDefinition': {'@type': '@json', '@value': {'description': description}}}]}
        path = root / 'okf-plus/records/os-ngd-collections/test.md'
        path.parent.mkdir(parents=True)
        path.write_text('---\n' + json.dumps(parent) + '\n---\n\nSynthetic\n')
        return parent, path, snapshot

    def test_complete_small_card_and_deterministic_export_bind_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            parent, path, snapshot = self.fixture(root)
            cards, index = MODULE.export(root, root / 'artifacts/cards')
            self.assertEqual(len(cards), 1)
            card = cards[0]
            self.assertEqual(card['field'], parent['okfp:field'][0])
            self.assertEqual(card['parent']['@id'], parent['@id'])
            self.assertEqual(card['provenance']['sources'], parent['sources'])
            self.assertEqual(card['provenance']['schemaEvidence'], parent['schemaEvidence'])
            self.assertEqual(card['provenance']['parentSha256'], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(card['provenance']['snapshotFiles'][0]['sha256'], hashlib.sha256(snapshot.read_bytes()).hexdigest())
            self.assertEqual(card['rights'], parent['rights'])
            self.assertLess(index['cards'][0]['bytes'], MODULE.MAX_CARD_BYTES)
            self.assertEqual(MODULE.export(root, root / 'artifacts/cards'), (cards, index))
            self.assertEqual(json.loads((root / 'artifacts/cards' / index['cards'][0]['path']).read_text()), card)

    def test_native_examples_and_no_invented_alias(self):
        for description, term in [('Pavement width in metres', 'width'), ('Building height above ground', 'height'),
                                  ('Road elevation relative to datum', 'elevation')]:
            with self.subTest(term=term), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                parent, _, _ = self.fixture(root, description)
                cards = MODULE.cards_from_records(root)
                result = MODULE.search_cards(cards, term)
                self.assertEqual(result['cards'][0]['field'], parent['okfp:field'][0])
                self.assertEqual(MODULE.search_cards(cards, 'altitude')['cards'], [])
                bounded = MODULE.search_cards(cards, term, max_bytes=1024)
                self.assertEqual(bounded['cards'], [])
                self.assertEqual(bounded['omittedCandidates'], 1)
                self.assertEqual(bounded['omissions'], ['byte-limit'])
                self.assertLessEqual(len(MODULE.canonical(bounded)), 1024)

    def test_symlink_output_ancestor_rejected_without_touching_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            target = root / 'actual'
            target.mkdir()
            (root / 'artifacts').symlink_to(target, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'Symlink output path'):
                MODULE.export(root, root / 'artifacts/cards')
            self.assertEqual(list(target.iterdir()), [])

    def test_symlink_output_leaves_rejected_before_any_write(self):
        for leaf_kind in ['index', 'card']:
            with self.subTest(leaf_kind=leaf_kind), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.fixture(root)
                cards = MODULE.cards_from_records(root)
                output = root / 'artifacts/cards'
                output.mkdir(parents=True)
                target = root / 'outside.txt'
                target.write_text('retain target')
                card_name = hashlib.sha256(cards[0]['field']['@id'].encode()).hexdigest() + '.jsonld'
                leaf = 'index.json' if leaf_kind == 'index' else card_name
                (output / leaf).symlink_to(target)
                with self.assertRaisesRegex(ValueError, 'Symlink output leaf'):
                    MODULE.export(root, output)
                self.assertEqual(target.read_text(), 'retain target')
                self.assertEqual([p.name for p in output.iterdir()], [leaf])

    def test_native_compounds_match_literal_terms_without_semantic_claims(self):
        def card(parent, native):
            return {'@id': 'https://example.org/' + native,
                    'parent': {'nativeIdentifier': parent},
                    'field': {'dcterms:identifier': native}}
        cards = [card('trn-ntwk-roadlink-5', 'presenceofpavement_averagewidth_m'),
                 card('bld-fts-building-4', 'height_absolute'),
                 card('trn-ntwk-roadlink-5', 'elevationgain_againstdirection'),
                 card('other', 'width')]
        for question, expected in [('pavement width', cards[0]),
                                   ('building height', cards[1]),
                                   ('road elevation', cards[2])]:
            with self.subTest(question=question):
                result = MODULE.search_cards(cards, question, max_records=1)
                self.assertEqual(result['cards'], [expected])
                self.assertNotIn('answer', result)
        self.assertEqual(MODULE.search_cards(cards, 'altitude')['cards'], [])
        self.assertEqual(MODULE.search_cards(cards, 'sea level')['cards'], [])
        self.assertEqual(MODULE.search_cards(cards, 'ave')['cards'], [])
        # The identifier still says gain: lexical discovery cannot assert datum.
        self.assertEqual(MODULE.search_cards(cards, 'road elevation', max_records=1)['cards'][0]
                         ['field']['dcterms:identifier'], 'elevationgain_againstdirection')

    def test_record_limit_retains_stable_order_and_exact_omission_count(self):
        cards = [{'@id': 'https://example.org/' + letter, 'field': {'description': 'width'}}
                 for letter in ['z', 'a', 'b']]
        result = MODULE.search_cards(cards, 'width', max_records=1)
        self.assertEqual(result['cards'], [cards[1]])
        self.assertEqual(result['omittedCandidates'], 2)
        self.assertEqual(result['omissions'], ['record-limit'])

    def test_oversize_fails_before_writing_any_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root, 'width ' * 2000)
            output = root / 'artifacts/cards'
            with self.assertRaisesRegex(ValueError, 'exceeds byte limit'):
                MODULE.export(root, output, max_card_bytes=2048)
            self.assertFalse(output.exists())

    def test_unsafe_snapshot_and_output_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            parent, path, _ = self.fixture(root)
            parent['sources'][0]['normalisedSource'] = '../outside.json'
            path.write_text('---\n' + json.dumps(parent) + '\n---\n')
            with self.assertRaisesRegex(ValueError, 'Unsafe snapshot'):
                MODULE.cards_from_records(root)


if __name__ == '__main__':
    unittest.main()
