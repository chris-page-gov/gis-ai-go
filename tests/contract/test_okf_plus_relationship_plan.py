"""Synthetic source-backed relationship planning; no provider or spatial calls."""
import copy
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator
from scripts.okf_plus import relationship_plan as m, linked_identifiers as client
from tests.contract.test_okf_plus_linked_identifiers import response, OP

ROOT = Path(__file__).resolve().parents[2]
SOURCE = {'identifier': '000000000001', 'identifierType': 'UPRN', 'featureType': 'BLPU'}
TARGET = {'identifierType': 'TOID', 'featureType': 'TopographicArea'}


def candidate(kind='linked-identifiers', cid='api'):
    value = {'id': cid, 'kind': kind, 'source': dict(SOURCE), 'targetType': dict(TARGET),
        'relationship': 'Synthetic source-declared association',
        'sourceEvidence': [{'reference': 'urn:synthetic:reviewed-source', 'sha256': '1' * 64}],
        'scopeStatus': 'supported', 'versionStatus': 'supported', 'observationStatus': 'not-observed'}
    if kind == 'linked-identifiers': value['method'] = 'BLPU_UPRN_TopographicArea_TOID_5'
    return value


def spec():
    return {'schema': 'gis-ai-go.relationship-plan-input.v1', 'source': dict(SOURCE),
        'targetType': dict(TARGET), 'purpose': 'Synthetic relationship investigation',
        'candidates': [candidate()], 'spatialFallback': {'requested': False, 'reason': 'Investigate declared relationships first', 'evidence': []}}


class RelationshipPlanTests(unittest.TestCase):
    def test_native_and_api_candidates_have_no_implicit_source_priority(self):
        value = spec(); value['candidates'] += [candidate('native-reference', 'native')]
        plan = m.plan_relationships(value)
        self.assertEqual([c['id'] for c in plan['candidates']], ['api', 'native'])
        self.assertFalse(plan['automaticExecution']); self.assertFalse(plan['joinsEstablished'])
        self.assertEqual(plan['sourceConstraints'][0]['method'], 'BLPU_UPRN_TopographicArea_TOID_5')
    def test_missing_relationship_is_not_supplied_by_native_precedence(self):
        value = spec(); other = candidate('native-reference', 'native'); other['scopeStatus'] = 'incompatible'
        value['candidates'].append(other)
        plan = m.plan_relationships(value)
        self.assertEqual([c['id'] for c in plan['candidates']], ['api'])
        self.assertIn('relationship-scope-incompatible', plan['unresolved'][0]['reasons'])
    def test_version_and_scope_unknowns_remain_unresolved(self):
        for field in ('versionStatus', 'scopeStatus'):
            value = spec(); value['candidates'][0][field] = 'unresolved'
            plan = m.plan_relationships(value)
            self.assertEqual(plan['candidates'], []); self.assertEqual(len(plan['unresolved']), 1)
    def test_denied_and_incomplete_are_not_empty_relationships(self):
        for status in ('denied', 'incomplete'):
            value = spec(); value['candidates'][0]['observationStatus'] = status
            plan = m.plan_relationships(value); self.assertEqual(plan['candidates'], [])
            self.assertFalse(plan['spatialFallback']['requested'])
    def test_empty_observation_retains_scoped_status(self):
        value = spec(); value['candidates'][0]['observationStatus'] = 'empty-response'
        plan = m.plan_relationships(value)
        self.assertEqual(plan['candidates'][0]['observationStatus'], 'empty-response')
        self.assertFalse(plan['transitiveIdentity']); self.assertFalse(plan['geographicEquivalence'])
    def test_no_spatial_execution_even_if_explicitly_requested(self):
        value = spec(); value['candidates'] = []; value['spatialFallback']['requested'] = True
        plan = m.plan_relationships(value)
        self.assertEqual(plan['spatialFallback']['status'], 'separate-review-required')
        self.assertFalse(plan['automaticExecution'])
    def test_method2_road_surface_cannot_satisfy_building_outline(self):
        value = spec(); road = {'identifier': 'osgb0000000000000002', 'identifierType': 'TOID', 'featureType': 'RoadLink'}
        value['source'] = road; value['candidates'][0]['source'] = road
        value['candidates'][0]['method'] = 'RoadLink_TOID_TopographicArea_TOID_2'; value['targetSemantics'] = 'building-outline'
        plan = m.plan_relationships(value)
        self.assertEqual(plan['candidates'], []); self.assertIn('target-semantics-unproven', plan['unresolved'][0]['reasons'])
        self.assertIn('road', plan['sourceConstraints'][0]['meaning'].lower())
    def test_method5_alone_cannot_establish_building_outline_classification(self):
        value = spec(); value['targetSemantics'] = 'building-outline'
        plan = m.plan_relationships(value)
        self.assertEqual(plan['candidates'], [])
        self.assertIn('target-semantics-unproven', plan['unresolved'][0]['reasons'])
        self.assertFalse(plan['transitiveIdentity'])
    def test_numeric_identifier_namespace_collision_is_not_same_node(self):
        value = spec(); value['candidates'][0]['source']['identifierType'] = 'USRN'
        with self.assertRaises(ValueError): m.plan_relationships(value)
    def test_unadmitted_osid_and_pathlink_types_refused(self):
        for field, invalid in (('identifierType', 'OSID'), ('featureType', 'PathLink')):
            value = spec(); value['targetType'][field] = invalid
            with self.assertRaises(ValueError): m.plan_relationships(value)
    def test_credentials_unknown_fields_and_fake_equivalence_refused(self):
        for change in ({'key': 'synthetic-secret'}, {'equivalent': True}, {'geometry': {}}):
            value = spec(); value['candidates'][0].update(change)
            with self.assertRaises(ValueError): m.plan_relationships(value)
        value = spec(); value['candidates'][0]['sourceEvidence'][0]['reference'] = 'https://example.invalid/?key=synthetic'
        with self.assertRaises(ValueError): m.plan_relationships(value)
    def test_missing_source_digest_and_duplicate_candidates_refused(self):
        value = spec(); value['candidates'][0]['sourceEvidence'][0]['sha256'] = 'unknown'
        with self.assertRaises(ValueError): m.plan_relationships(value)
        value = spec(); value['candidates'] *= 2
        with self.assertRaises(ValueError): m.plan_relationships(value)
    def test_impossible_native_node_type_pair_is_refused(self):
        value = spec(); value['candidates'] = [candidate('native-reference')]
        value['source']['identifierType'] = 'GUID'; value['candidates'][0]['source']['identifierType'] = 'GUID'
        with self.assertRaisesRegex(ValueError, 'pairing'): m.plan_relationships(value)
        value = spec(); value['targetType']['identifierType'] = 'UPRN'
        with self.assertRaisesRegex(ValueError, 'pairing'): m.plan_relationships(value)

    def test_closed_schemas_match_actual_input_output_and_refuse_extras(self):
        for name in ('relationship-plan', 'linked-identifiers'):
            schema = json.loads((ROOT / f'okf-plus/schemas/{name}.schema.json').read_text())
            Draft202012Validator.check_schema(schema)
            validator = Draft202012Validator(schema)
            if name == 'relationship-plan':
                values = [spec(), m.plan_relationships(spec())]
            else:
                values = [client.graph(OP, response(), '2' * 64, '2030-01-01T00:00:00Z')]
            for value in values:
                validator.validate(value)
                invalid = copy.deepcopy(value); invalid['unknown'] = True
                self.assertTrue(list(validator.iter_errors(invalid)))
    def test_public_profile_contains_no_private_paths_or_payload_identifiers(self):
        raw = client.PROFILE.read_bytes(); value = json.loads(raw)
        self.assertLessEqual(len(raw), 16384)
        self.assertEqual({m['correlationMethodIdentifier'] for m in value['methods']}, client.METHODS)
        self.assertNotIn(b'/Users/', raw); self.assertNotIn(b'/Volumes/', raw)
        self.assertFalse(value['authentication']['queryKeyFallback'])


if __name__ == '__main__': unittest.main()
