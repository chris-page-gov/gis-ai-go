"""Synthetic route observations and unsent private OS support drafts."""
import copy
import unittest
from scripts.okf_plus.route_comparison import compare_routes, draft_markdown


class RouteComparisonTests(unittest.TestCase):
    def fixture(self):
        route = {'route_id': 'or-route', 'call': {'method': 'GET',
            'url': 'https://api.os.uk/synthetic/items',
            'params': {'filter': "osid = 'synthetic-1'"}, 'key_binding': 'OS_API_KEY'},
            'context': {'collection': 'synthetic-v1', 'version': '1', 'crs': '27700',
                        'time': '2026-10-19', 'units': 'metres'},
            'source_independence': False, 'receipt_sha256': 'a' * 64,
            'identity_path': ['id'], 'fields': {'width': ['properties', 'width']},
            'records': [{'id': 'synthetic-1', 'properties': {'width': 3.0}},
                        {'id': 'synthetic-2', 'properties': {'width': None}}]}
        other = copy.deepcopy(route)
        other['route_id'] = 'in-route'; other['receipt_sha256'] = 'b' * 64
        return {'routes': [route, other], 'requested_fields': ['width'],
                'methodology': 'Compare exact native IDs and retained full-call responses.',
                'code_reference': 'urn:synthetic:comparison-code-v1'}

    def test_same_backend_agreement_is_descriptive_not_confidence_or_ticket(self):
        result = compare_routes(self.fixture())
        row = result['observations'][0]['fields'][0]
        self.assertEqual((row['N'], row['equal'], row['concordance_fraction']), (2, 2, 1))
        self.assertEqual(row['null_observations'], 1)
        self.assertIsNone(result['support_case']); self.assertIsNone(draft_markdown(result))
        self.assertIn('not independent evidence', result['limitations'][1])
        self.assertFalse(result['execution'])

    def test_discrepancy_yields_private_candidate_case_without_values_by_default(self):
        spec = self.fixture()
        spec['routes'][1]['records'][0]['properties']['width'] = 4.0
        result = compare_routes(spec)
        row = result['observations'][0]['fields'][0]
        self.assertEqual((row['N'], row['unequal'], row['concordance_fraction']), (2, 1, .5))
        self.assertNotIn('private_differences', row)
        case = result['support_case']
        self.assertEqual(case['distribution'], 'private')
        self.assertTrue(case['candidateOnly']); self.assertFalse(case['sendingAdmitted'])
        self.assertEqual(case['calls'][0]['receipt_sha256'], 'a' * 64)
        self.assertIn('OS_API_KEY', draft_markdown(result))
        spec['include_private_values'] = True
        self.assertEqual(compare_routes(spec)['observations'][0]['fields'][0]['private_differences'][0]['right'], 4.0)

    def test_context_mismatch_requires_reviewed_aligned_input_claim(self):
        spec = self.fixture(); spec['routes'][1]['context']['version'] = '2'
        result = compare_routes(spec)
        self.assertFalse(result['observations'][0]['fields'][0]['comparable'])
        self.assertIsNone(result['support_case'])
        spec['normalization'] = {'reviewed': True, 'contexts_aligned': True,
                                 'evidence': 'urn:reviewed:version-alignment'}
        self.assertTrue(compare_routes(spec)['observations'][0]['fields'][0]['comparable'])

    def test_different_native_fields_require_explicit_mapping_evidence(self):
        spec = self.fixture(); right = spec['routes'][1]
        right['fields']['width'] = ['properties', 'other_width']
        for record in right['records']:
            record['properties']['other_width'] = record['properties'].pop('width')
        self.assertFalse(compare_routes(spec)['observations'][0]['fields'][0]['comparable'])
        spec['reviewed_mappings'] = [{'field': 'width', 'evidence': 'urn:reviewed:equivalence'}]
        self.assertEqual(compare_routes(spec)['observations'][0]['fields'][0]['equal'], 2)

    def test_tolerance_needs_explicit_same_units_crs_and_reason(self):
        spec = self.fixture(); spec['routes'][1]['records'][0]['properties']['width'] = 3.01
        self.assertIsNotNone(compare_routes(spec)['support_case'])
        spec['tolerances'] = {'width': {'absolute': .02, 'reason': 'Documented rounding',
                                      'units': 'metres', 'crs': '27700'}}
        self.assertIsNone(compare_routes(spec)['support_case'])
        spec['tolerances']['width']['units'] = 'feet'
        with self.assertRaisesRegex(ValueError, 'identical explicit units'):
            compare_routes(spec)
        spec['tolerances']['width']['units'] = 'metres'
        del spec['tolerances']['width']['reason']
        with self.assertRaises(ValueError): compare_routes(spec)

    def test_missing_records_values_and_type_observations(self):
        spec = self.fixture(); right = spec['routes'][1]
        right['records'][0]['properties']['width'] = '3.0'
        del right['records'][1]['properties']['width']
        right['records'].append({'id': 'synthetic-3', 'properties': {'width': 9}})
        row = compare_routes(spec)['observations'][0]['fields'][0]
        self.assertEqual(row['missing_left_records'], 1)
        self.assertEqual(row['missing_right_values'], 1)
        self.assertEqual(row['type_differences'], 1)
        self.assertEqual(row['N'], 1)

    def test_in500_or200_exact_selector_status_case_preserves_operator_calls(self):
        spec = self.fixture(); spec['requested_fields'] = []
        for index, route in enumerate(spec['routes']):
            route['records'] = []; route['http_status'] = 200 if index == 0 else 500
            route['selector_id'] = 'private-same-id-set'
            route['expected_behavior_refs'] = ['https://docs.os.uk/os-apis/synthetic-filter.md']
        spec['routes'][1]['call']['params']['filter'] = "osid IN ('synthetic-1')"
        result = compare_routes(spec)
        self.assertTrue(result['observations'][0]['http_status_discrepancy'])
        self.assertEqual(result['support_case']['calls'][1]['http_status'], 500)
        self.assertIn("IN ('synthetic-1')", draft_markdown(result))
        spec['routes'][0]['http_status'] = 500
        self.assertEqual(compare_routes(spec)['support_case']['discrepancies'][0]['kind'], 'http-error')

    def test_rejects_credentials_and_unbounded_or_ambiguous_inputs(self):
        for change in ['query-key', 'param-token', 'bearer', 'duplicate-id', 'many-routes', 'missing-hash']:
            spec = self.fixture()
            if change == 'query-key': spec['routes'][0]['call']['url'] += '?key=DO-NOT-RETAIN'
            if change == 'param-token': spec['routes'][0]['call']['params']['access_token'] = 'secret'
            if change == 'bearer': spec['routes'][0]['call']['params']['header'] = 'Bearer secret'
            if change == 'duplicate-id': spec['routes'][0]['records'].append(copy.deepcopy(spec['routes'][0]['records'][0]))
            if change == 'many-routes': spec['routes'] *= 5
            if change == 'missing-hash': del spec['routes'][0]['receipt_sha256']
            with self.subTest(change=change), self.assertRaises(ValueError): compare_routes(spec)
