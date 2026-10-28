"""Retained-record graph coverage, evidence and semantic-boundary checks."""
from copy import deepcopy
from pathlib import Path
import unittest

from jsonschema import ValidationError

from scripts.okf_plus.context_projection import canonical, sha
from scripts.okf_plus.explorer_relationships import project_relationships, validate_relationships
from scripts.okf_plus.model import read_markdown
from tests.contract.test_okf_plus_context import fixture, CAPTURED


ROOT = Path(__file__).resolve().parents[2]
SKOS_RELATED = 'http://www.w3.org/2004/02/skos/core#related'
REVISION = 'b' * 40


def records(count=3):
    search, bundle = fixture(count)
    return search['records'], {row['@id']: row for row in bundle['records']}


class ExplorerRelationshipTests(unittest.TestCase):
    def test_explicit_links_keep_predicate_routes_and_source_governance(self):
        rows, semantic = records()
        source, target = rows[0]['id'], rows[1]['id']
        semantic[source]['skos:related'] = [{'@id': target}]
        original = deepcopy(semantic)
        relationships, coverage = project_relationships(rows, semantic, captured_at=CAPTURED, source_revision=REVISION)
        self.assertEqual(semantic, original)
        self.assertEqual(len(relationships), 1)
        edge = relationships[0]
        self.assertEqual((edge['source'], edge['target']), (rows[0]['route'], rows[1]['route']))
        self.assertEqual((edge['source_iri'], edge['target_iri'], edge['predicate']), (source, target, SKOS_RELATED))
        self.assertEqual(edge['kind'], 'related')
        self.assertEqual(edge['inverse_label'], 'related concept')
        self.assertEqual(edge['assertion_status'], 'normalized')
        self.assertEqual(edge['source_assertion_status'], 'normalised')
        self.assertEqual(edge['authority']['class'], 'synthetic')
        self.assertEqual(edge['assertion_scope'], 'synthetic-fixture')
        self.assertIn('does not establish geographic feature topology', edge['scope'])
        self.assertEqual(edge['rights']['inherited_record_rights'], semantic[source]['rights'])
        self.assertTrue(edge['rights']['no_rights_expansion'])
        self.assertEqual(edge['observed_at'], CAPTURED)
        self.assertEqual(edge['freshness'], 'unknown')
        evidence = edge['evidence'][0]
        self.assertEqual(evidence['locator'], '/skos:related/0')
        self.assertEqual(evidence['source_value'], semantic[source]['skos:related'][0])
        self.assertEqual(evidence['source_sha256'], sha(canonical(semantic[source])))
        self.assertEqual(evidence['source_value_sha256'], sha(canonical(evidence['source_value'])))
        self.assertEqual(evidence['url'], f'https://github.com/chris-page-gov/gis-ai-go/blob/{REVISION}/okf-plus/{rows[0]["route"]}')
        self.assertEqual(coverage['projected_assertions'], 1)
        self.assertEqual(coverage['all_projected_assertions_schema_validated'], 1)
        self.assertTrue(coverage['all_internal_record_references_projected'])

    def test_navigation_and_json_literal_fields_do_not_create_relationships(self):
        rows, semantic = records()
        for row in semantic.values():
            row['tags'] = ['related', 'same as', rows[1]['id']]
            row['details']['learningPath'] = {'steps': [{'recordId': rows[1]['id']}]}
            row['details']['nestedLink'] = {'@id': rows[1]['id']}
        rows[0]['text'] += '[Related record](' + rows[1]['route'] + ')'
        relationships, coverage = project_relationships(rows, semantic, captured_at=CAPTURED)
        self.assertEqual(relationships, [])
        self.assertEqual(coverage['explicit_top_level_reference_occurrences'], 0)

    def test_external_and_nested_targets_remain_counted_as_unprojected(self):
        rows, semantic = records()
        parent = semantic[rows[0]['id']]
        parent['skos:related'] = [{'@id': rows[1]['id']}]
        parent['skos:relatedMatch'] = [{'@id': f'https://example.test/external/{n}'} for n in range(9)]
        parent['qb:structure'] = {'@id': rows[0]['id'] + '#nested-structure'}
        parent['dcterms:conformsTo'] = {'@id': 'https://example.test/profile'}
        relationships, coverage = project_relationships(rows, semantic, captured_at=CAPTURED)
        self.assertEqual(len(relationships), 1)
        self.assertEqual(coverage['explicit_top_level_reference_occurrences'], 12)
        self.assertEqual(coverage['retained_record_reference_occurrences'], 1)
        self.assertEqual(coverage['unprojected_reference_occurrences'], 11)
        self.assertEqual(sum(row['count'] for row in coverage['unprojected_groups']), 11)
        matched = next(row for row in coverage['unprojected_groups'] if row['predicate'].endswith('relatedMatch'))
        self.assertEqual(matched['count'], 9)
        self.assertEqual(len(matched['examples']), 4)
        self.assertEqual(matched['examples_omitted'], 5)
        self.assertRegex(matched['occurrence_ids_sha256'], r'^[0-9a-f]{64}$')
        self.assertIn('nested semantic entities remain', coverage['scope'])
        self.assertEqual(project_relationships(rows, semantic, captured_at=CAPTURED), (relationships, coverage))

    def test_assertion_ids_survive_source_order_changes_and_do_not_add_reverse_edges(self):
        rows, semantic = records()
        semantic[rows[0]['id']]['skos:related'] = [{'@id': rows[1]['id']}, {'@id': rows[2]['id']}]
        first, _ = project_relationships(rows, semantic, captured_at=CAPTURED)
        semantic[rows[0]['id']]['skos:related'].reverse()
        second, _ = project_relationships(list(reversed(rows)), semantic, captured_at=CAPTURED)
        self.assertEqual([row['id'] for row in first], [row['id'] for row in second])
        self.assertEqual(len(first), 2)
        self.assertEqual({row['source_iri'] for row in first}, {rows[0]['id']})
        self.assertFalse(any(row['predicate'].endswith('sameAs') for row in first))

    def test_duplicate_triples_keep_every_source_occurrence_as_evidence(self):
        rows, semantic = records()
        semantic[rows[0]['id']]['skos:related'] = [{'@id': rows[1]['id']}, {'@id': rows[1]['id']}]
        relationships, coverage = project_relationships(rows, semantic, captured_at=CAPTURED)
        self.assertEqual(len(relationships), 1)
        self.assertEqual([row['locator'] for row in relationships[0]['evidence']], ['/skos:related/0', '/skos:related/1'])
        self.assertEqual(coverage['retained_record_reference_occurrences'], 2)
        self.assertEqual(coverage['projected_assertions'], 1)
        self.assertEqual(coverage['duplicate_reference_occurrences'], 1)

    def test_different_declared_predicates_and_statuses_are_not_collapsed(self):
        rows, semantic = records()
        parent = semantic[rows[0]['id']]
        parent['reviewStatus'] = 'source-reviewed'
        parent['assertionStatus'] = 'official'
        parent['skos:broader'] = {'@id': rows[1]['id']}
        parent['dcterms:isPartOf'] = {'@id': rows[2]['id']}
        relationships, _ = project_relationships(rows, semantic, captured_at=CAPTURED)
        self.assertEqual({row['predicate'] for row in relationships}, {
            'http://www.w3.org/2004/02/skos/core#broader', 'http://purl.org/dc/terms/isPartOf'})
        self.assertEqual({row['assertion_status'] for row in relationships}, {'official'})
        # Projector authority never becomes official merely because a source
        # record carries the official assertion-status value.
        self.assertEqual({row['authority']['class'] for row in relationships}, {'derived'})
        self.assertEqual({row['assertion_scope'] for row in relationships}, {'real-world'})

    def test_unknown_internal_predicate_fails_instead_of_disappearing(self):
        rows, semantic = records()
        semantic[rows[0]['id']]['skos:unsupported'] = {'@id': rows[1]['id']}
        with self.assertRaisesRegex(ValueError, 'Unsupported internal record relationship predicate'):
            project_relationships(rows, semantic, captured_at=CAPTURED)

    def test_every_row_is_validated_and_evidence_is_bound_to_actual_source(self):
        rows, semantic = records()
        semantic[rows[0]['id']]['skos:related'] = [{'@id': rows[1]['id']}, {'@id': rows[2]['id']}]
        relationships, _ = project_relationships(rows, semantic, captured_at=CAPTURED)
        routes = {row['id']: row['route'] for row in rows}
        wrong = deepcopy(relationships); del wrong[-1]['rights']
        with self.assertRaises(ValidationError):
            validate_relationships(wrong, routes, semantic)
        wrong = deepcopy(relationships); wrong[-1]['evidence'][0]['locator'] = '/skos:related/0'
        with self.assertRaisesRegex(ValueError, 'differs from its source pointer'):
            validate_relationships(wrong, routes, semantic)
        wrong = deepcopy(relationships); wrong[-1]['target'] = rows[1]['route']
        with self.assertRaisesRegex(ValueError, 'retained record route'):
            validate_relationships(wrong, routes, semantic)
        wrong = deepcopy(relationships); wrong[-1]['evidence'][0]['source_value_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            validate_relationships(wrong, routes, semantic)

    def test_invalid_identifiers_credentials_dates_and_route_collisions_fail(self):
        rows, semantic = records()
        for target in ('javascript:alert(1)', 'https://user:secret@example.test/',
                       'https://example.test/?api_key=private', 'https://example.test/bad%xy'):
            bad = deepcopy(semantic)
            bad[rows[0]['id']]['skos:related'] = {'@id': target}
            with self.assertRaises(ValueError):
                project_relationships(rows, bad, captured_at=CAPTURED)
        for date in ('2026-10-02', '2026-02-31T00:00:00Z', '2026-10-02T00:00:00+01:00', None):
            with self.assertRaises(ValueError):
                project_relationships(rows, semantic, captured_at=date)
        wrong = deepcopy(rows); wrong[1]['route'] = wrong[0]['route']
        with self.assertRaisesRegex(ValueError, 'identities or Reader routes'):
            project_relationships(wrong, semantic, captured_at=CAPTURED)

    def test_access_rights_source_links_reach_real_retained_concept_routes(self):
        names = ['access-rights', 'open-government-licence', 'data-service']
        semantic = {}; rows = []
        for name in names:
            route = f'records/geospatial-concepts/{name}.md'
            parent, _ = read_markdown(ROOT / 'okf-plus' / route)
            semantic[parent['@id']] = parent
            rows.append({'id': parent['@id'], 'route': route})
        relationships, coverage = project_relationships(rows, semantic, captured_at=CAPTURED)
        access = [row for row in relationships if row['source'] == 'records/geospatial-concepts/access-rights.md']
        self.assertEqual(len(access), 2)
        self.assertEqual({row['target'] for row in access}, {
            'records/geospatial-concepts/open-government-licence.md', 'records/geospatial-concepts/data-service.md'})
        self.assertEqual({row['predicate'] for row in access}, {SKOS_RELATED})
        self.assertEqual({row['assertion_status'] for row in access}, {'normalized'})
        self.assertTrue(coverage['all_internal_record_references_projected'])

    def test_complete_authored_concept_graph_matches_every_explicit_source_link(self):
        semantic = {}; rows = []
        for path in sorted((ROOT / 'okf-plus/records/geospatial-concepts').glob('*.md')):
            parent, _ = read_markdown(path)
            semantic[parent['@id']] = parent
            rows.append({'id': parent['@id'], 'route': path.relative_to(ROOT / 'okf-plus').as_posix()})
        # Independent source-side denominator: no producer registry or exported
        # counts participate in deciding which explicit links must survive.
        expected = {(identifier, SKOS_RELATED, reference['@id'])
                    for identifier, parent in semantic.items()
                    for reference in parent.get('skos:related', [])
                    if reference['@id'] in semantic}
        self.assertGreaterEqual(len(expected), 137)
        relationships, coverage = project_relationships(rows, semantic, captured_at=CAPTURED)
        self.assertEqual({(edge['source_iri'], edge['predicate'], edge['target_iri']) for edge in relationships}, expected)
        self.assertEqual(coverage['projected_assertions'], len(expected))
        self.assertEqual(coverage['all_projected_assertions_schema_validated'], len(expected))


if __name__ == '__main__':
    unittest.main()
