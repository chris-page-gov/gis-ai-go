"""Source-fidelity and semantic-boundary checks for small OS knowledge cards."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/okf_plus'))
import semantic
import semantic_search
from model import canonical, digest


class SemanticCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards = list(semantic.generate_cards(ROOT))
        cls.fields = {(card['collectionId'], card['nativeIdentifier']): card
                      for card in cls.cards if card['kind'] == 'field'}

    @classmethod
    def tearDownClass(cls):
        del cls.cards
        del cls.fields

    def test_every_retained_schema_field_and_queryable_has_its_own_card(self):
        snapshot = json.loads((ROOT / 'okf-plus/source/os-ngd-collections.json').read_text())
        expected = {(item['id'], name) for item in snapshot['records']
                    for name in set(item['schemas']['schema']['properties']) | set(item['schemas']['queryables']['properties'])}
        self.assertEqual(set(self.fields), expected)
        self.assertEqual(len({card['@id'] for card in self.cards}), len(self.cards))

    def test_every_card_has_bounded_size_and_exact_source_pointer_digest(self):
        snapshots = {}
        for card in self.cards:
            self.assertLessEqual(len(semantic.card_text(card).encode()), semantic.MAX_CARD_BYTES)
            source = card['source']
            if source['snapshot'] not in snapshots:
                snapshots[source['snapshot']] = json.loads((ROOT / source['snapshot']).read_text())
            snapshot = snapshots[source['snapshot']]
            self.assertEqual(source['sha256'], digest(semantic.resolve_pointer(snapshot, source['pointer'])))
            self.assertEqual(source['recordSha256'], digest(semantic.resolve_pointer(snapshot, source['recordPointer'])))
            if source['responseBinding'] == 'matched-capture-receipt':
                self.assertTrue(any(receipt.get('status') == 200 and
                                    receipt.get('sha256') == source['responseSha256'] and
                                    receipt.get('retrievedAt') == source['retrievedAt'] and
                                    receipt.get('url') == source['resource']
                                    for receipt in snapshot['receipts']))

    def test_pavement_scope_preserves_both_sides_and_per_side_subsection_distinction(self):
        name = 'presenceofpavement_minimumwidth_m'
        road = self.fields['trn-ntwk-roadlink-5', name]
        pavement = self.fields['trn-ntwk-pavementlink-1', name]
        self.assertIn('both sides', road['definition'])
        self.assertIn('subsection', pavement['definition'])
        self.assertNotEqual(road['@id'], pavement['@id'])
        self.assertEqual(road['unit'], 'm')
        self.assertIn('Algorithmic', road['derivationMethod'])
        self.assertFalse(road['facts']['nullable'])
        self.assertTrue(road['facts']['required'])
        # Current reviewed documentation never silently enriches all old versions.
        old = self.fields['trn-ntwk-roadlink-2', name]
        self.assertNotIn('definition', old)
        self.assertIn('definition-not-evidenced', old['gaps'])

    def test_schema_level_defects_are_preserved_without_repairing_case(self):
        schemas = [card for card in self.cards if card['kind'] == 'schema-definition']
        self.assertEqual(len(schemas), 188)
        snapshot = json.loads((ROOT / 'okf-plus/source/os-ngd-collections.json').read_text())
        for card in schemas:
            original = semantic.resolve_pointer(snapshot, card['source']['pointer'])
            self.assertEqual(card['facts'], {key: value for key, value in original.items() if key != 'properties'})
        road = next(card for card in schemas if card['nativeIdentifier'] == 'trn-ntwk-roadlink-5/schema')
        self.assertIn('presenceOfstreetlight_coverage', road['facts']['required'])
        self.assertIn('presenceOfstreetlight_coverage', road['facts']['requiredUndeclared'])
        self.assertIn('required-property-not-declared:presenceOfstreetlight_coverage', road['gaps'])
        self.assertIn('required-property-not-declared:presenceofcyclelane_overallPercentage', road['gaps'])
        self.assertIn('additionalProperties', road['facts'])
        self.assertIn('dialect', road['facts'])
        self.assertNotIn(('trn-ntwk-roadlink-5', 'presenceOfstreetlight_coverage'), self.fields)
        declared = self.fields['trn-ntwk-roadlink-5', 'presenceofstreetlight_coverage']
        self.assertFalse(declared['facts']['required'])
        self.assertIn({'@id': road['@id'], 'relation': 'schema', 'status': 'source-stated'}, declared['related'])

    def test_all_cards_conform_to_strict_semantic_contract(self):
        schema = json.loads((ROOT / 'okf-plus/schemas/semantic-card.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        for card in self.cards:
            validator.validate(card)
        field = deepcopy(self.fields['trn-ntwk-roadlink-5', 'geometry'])
        field['facts'] = []
        self.assertFalse(validator.is_valid(field))
        field['facts'] = {}
        field['source']['sha256'] = 'unbound'
        self.assertFalse(validator.is_valid(field))

    def test_companion_links_are_explicit_same_version_reading_dependencies(self):
        indexed = {card['@id']: card for card in self.cards}
        supplement = json.loads((ROOT / 'okf-plus/source/os-field-semantics.json').read_text())
        expected_count = sum(len(fact.get('relatedFieldIdentifiers', [])) for fact in supplement['facts'])
        count = 0
        for card in self.fields.values():
            links = [link for link in card['related'] if link['relation'] == 'semantic-companion']
            count += len(links)
            for link in links:
                target = indexed[link['@id']]
                self.assertEqual(target['kind'], 'field')
                self.assertEqual(target['collectionId'], card['collectionId'])
                self.assertEqual(target['version'], card['version'])
                self.assertEqual(link['status'], 'author-curated-reading-dependencies')
                self.assertIn(target['nativeIdentifier'], card['facts']['semantics']['relatedFieldIdentifiers'])
                self.assertIn('Partial excerpts', card['facts']['semantics']['retainedEvidenceScope'])
        self.assertEqual(count, expected_count)
        self.assertGreater(count, 0)

    def test_rich_linked_read_is_bounded_and_avoids_unrequested_schema_and_versions(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            for card in self.fields.values():
                if card['collectionId'] not in ('trn-ntwk-roadlink-4', 'trn-ntwk-roadlink-5'):
                    continue
                path = output / semantic.card_path(card)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(semantic.card_text(card))
            semantic_search.build_index(output, revision='e' * 40)
            result = semantic_search.read_item(output, 'geometry', collection_id='trn-ntwk-roadlink-5',
                                               expand=('semantic-companion',), depth=2,
                                               max_records=4, max_bytes=60000)
            cards = [entry['card'] for entry in result['results']]
            self.assertEqual({card['nativeIdentifier'] for card in cards},
                             {'geometry', 'heightingmethod', 'startgradeseparation', 'endgradeseparation'})
            self.assertTrue(all(card['collectionId'] == 'trn-ntwk-roadlink-5' for card in cards))
            self.assertTrue(all(card['kind'] == 'field' for card in cards))
            self.assertLessEqual(len(semantic_search.render(result)), 60000)
            limited = semantic_search.read_item(output, 'geometry', collection_id='trn-ntwk-roadlink-5',
                                                expand=('semantic-companion',), depth=2,
                                                max_records=2, max_bytes=30000)
            self.assertLessEqual(len(limited['results']), 2)
            self.assertLessEqual(len(semantic_search.render(limited)), 30000)
            self.assertTrue(limited['truncated'])

    def test_building_absolute_relative_nullability_and_datum_are_separate(self):
        absolute = self.fields['bld-fts-building-4', 'height_absolutemax_m']
        relative = self.fields['bld-fts-building-4', 'height_relativemax_m']
        ground = self.fields['bld-fts-building-4', 'height_absolutemin_m']
        self.assertEqual(absolute['facts']['semantics']['semanticRole'], 'absolute-top-elevation')
        self.assertIn('ground', ground['definition'])
        self.assertNotEqual(absolute['definition'], relative['definition'])
        self.assertTrue(absolute['facts']['nullable'])
        self.assertTrue(absolute['facts']['required'])
        self.assertIn('vertical-datum-not-evidenced', absolute['gaps'])
        self.assertNotIn('verticalDatum', absolute)
        self.assertNotEqual(self.fields['bld-fts-buildingpart-1', 'absoluteheightmaximum']['@id'],
                            self.fields['bld-fts-buildingpart-2', 'height_absolutemax_m']['@id'])

    def test_road_3d_geometry_is_distinct_from_ascent_and_grade_separation(self):
        geometry = self.fields['trn-ntwk-roadlink-5', 'geometry']
        gain = self.fields['trn-ntwk-roadlink-5', 'elevationgain_indirection']
        separation = self.fields['trn-ntwk-roadlink-5', 'startgradeseparation']
        self.assertIn('Three-dimensional', geometry['definition'])
        self.assertIn('7405', geometry['facts']['semantics']['retrievalGuidance'])
        self.assertIn('ascent', gain['definition'].casefold())
        self.assertNotEqual(gain['facts']['semantics']['semanticRole'], geometry['facts']['semantics']['semanticRole'])
        self.assertIn('relative', separation['definition'].casefold())
        self.assertTrue(any('not present-day sea level' in value for value in geometry['facts']['semantics']['limitations']))

    def test_enum_values_remain_field_scoped_and_have_real_graph_links(self):
        field = self.fields['bld-fts-building-4', 'height_confidencelevel']
        values = [card for card in self.cards if card['kind'] == 'code-value' and card.get('parent') == field['codeList']]
        self.assertEqual({card['facts']['value'] for card in values}, {'High', 'Incomplete', 'Low', 'Moderate', 'Not Assessed'})
        self.assertTrue(all(card['codeList'] == field['codeList'] for card in values))
        self.assertTrue(all(card.get('definition') for card in values))
        self.assertTrue(all(card.get('semanticEvidence') for card in values))
        self.assertEqual(semantic.CONTEXT['parent']['@id'], 'dcterms:isPartOf')
        self.assertEqual(semantic.CONTEXT['codeList']['@id'], 'skos:inScheme')
        self.assertEqual(semantic.CONTEXT['definition'], 'skos:definition')

    def test_all_current_card_terms_have_local_json_ld_definitions(self):
        for card in self.cards:
            self.assertFalse(set(card) - set(semantic.CONTEXT) - {'@id', '@context', '@type'})

    def test_documentation_labels_do_not_become_definitions_or_api_enums(self):
        docs = [card for card in self.cards if card['kind'] == 'code-value' and card['sourceFamily'] == 'osngd-documentation-pages']
        self.assertEqual(len(docs), 6067)
        self.assertTrue(all('definition' not in card and card['collectionId'] is None for card in docs))
        self.assertTrue(all('definition-not-evidenced' in card['gaps'] for card in docs))
        sections = [card for card in self.cards if card['kind'] == 'documentation-section']
        self.assertTrue(all('section-body-not-evidenced' in card['gaps'] for card in sections))

    def test_api_fragments_operations_security_and_native_constraints_are_preserved(self):
        snapshot = json.loads((ROOT / 'okf-plus/source/os-api-contracts.json').read_text())
        expected = sum(len(contract['operations']) for record in snapshot['records'] for contract in record['contracts'])
        operations = [card for card in self.cards if card['kind'] == 'api-operation']
        self.assertEqual(len(operations), expected)
        for card in operations:
            native = semantic.resolve_pointer(snapshot, card['source']['pointer'])
            self.assertEqual(card['facts']['documentedSecurity'], native['documentedSecurity'])
            self.assertEqual(card['facts']['httpMethodSemantics'], native['httpMethodSemantics'])
            self.assertFalse(card['facts']['callable'])
            self.assertEqual(card['nativeIdentifier'], native['method'] + ' ' + native['path'])

    def test_paginated_catalogue_receipts_use_frozen_native_locator(self):
        locators = json.loads((ROOT / 'okf-plus/source/locator-index.json').read_text())['families']
        for card in self.cards:
            if card['sourceFamily'] != 'os-gemini-metadata':
                continue
            locator = locators['os-gemini-metadata'][card['nativeIdentifier']]
            self.assertEqual(card['source']['resource'], locator['url'])
            self.assertEqual(card['source']['responseSha256'], locator['sha256'])
            self.assertEqual(card['source']['responsePointer'], locator['pointer'])
        synthetic = {'family': 'os-synthetic', 'records': [{'id': 'later-page'}],
                     'receipts': [{'url': 'https://example.org/first', 'status': 200,
                                   'sha256': 'a' * 64, 'retrievedAt': '2026-10-18T00:00:00Z'}]}
        source = semantic.Source(ROOT / 'okf-plus/source/os-synthetic.json', ROOT, synthetic, 0)
        self.assertEqual(source.evidence('')['responseBinding'], 'not-evidenced')
        self.assertIsNone(source.evidence('')['responseSha256'])

    def test_large_facts_split_losslessly_with_character_offsets(self):
        card = deepcopy(next(iter(self.fields.values())))
        value = 'Synthetic 🗺 evidence. ' * 3000
        card['facts'] = {'largeValue': value, 'empty': []}
        cards = list(semantic._bounded(card))
        self.assertGreater(len(cards), 2)
        self.assertEqual(cards[0]['facts']['sha256'], digest(card['facts']))
        parts = sorted((part['facts'] for part in cards[1:] if part['facts']['factPointer'] == '/largeValue'),
                       key=lambda part: part['characterOffset'])
        self.assertEqual(''.join(part['value'] for part in parts), value)
        self.assertTrue(all(len(semantic.card_text(part).encode()) <= semantic.MAX_CARD_BYTES for part in cards))
        self.assertTrue(any(part['facts']['value'] == [] for part in cards[1:]))

    def test_card_ids_and_output_paths_are_stable_and_version_scoped(self):
        field = self.fields['trn-ntwk-roadlink-5', 'geometry']
        self.assertEqual(field['@id'], semantic.semantic_id('field', 'os-ngd-collections',
                         'trn-ntwk-roadlink-5', '/schemas/schema/properties/geometry'))
        self.assertNotEqual(field['@id'], self.fields['trn-ntwk-roadlink-4', 'geometry']['@id'])
        self.assertEqual(len(semantic.card_path(field).parts), 3)
        self.assertNotIn('trn-ntwk', semantic.card_path(field).name)

    def test_supplement_rejects_stale_snapshot_nonexistent_field_and_changed_excerpt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'okf-plus/source'
            source.mkdir(parents=True)
            for name in ('os-ngd-collections.json', 'os-field-semantics.json'):
                shutil.copyfile(ROOT / 'okf-plus/source' / name, source / name)
            original = json.loads((source / 'os-field-semantics.json').read_text())
            for mutate, error in (
                (lambda value: value.update(sourceSnapshotSha256='0' * 64), 'snapshot checksum'),
                (lambda value: value['facts'][0].update(collectionId='trn-ntwk-roadlink-999'), 'version-scoped schema field'),
                (lambda value: value['sources'][0].update(evidenceExcerpt='Changed'), 'excerpt checksum'),
                (lambda value: value['facts'][0].update(relatedFieldIdentifiers=['height_absolutemax_m']), 'same-collection schema field'),
            ):
                value = deepcopy(original)
                mutate(value)
                (source / 'os-field-semantics.json').write_bytes(canonical(value))
                with self.assertRaisesRegex(ValueError, error):
                    semantic._supplements(root)


if __name__ == '__main__':
    unittest.main()
