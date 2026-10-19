"""Synthetic capability-evidence planning, with no provider calls."""
import copy
import unittest
from scripts.okf_plus.query_planner import plan_query


def field(name, collection='ngd-v1'):
    return {'stable_id': 'urn:field:' + name, 'native_field': name,
            'collection_id': collection}


def route(name, fields, **extra):
    return {'route_id': name, 'coverage_id': 'selection-1',
            'collection_id': fields[0]['collection_id'], 'fields': fields,
            'kind': 'api', 'request': {'path': '/synthetic/collection'},
            'estimated_requests': 1, **extra}


class QueryPlannerTests(unittest.TestCase):
    def fixture(self):
        fields = [field(name) for name in ('a3', 'z2', 'b26')]
        routes = [route(f['native_field'], [f]) for f in fields]
        routes.append(route('ngd-documented', fields,
            projection={'supported': True, 'parameter': 'synthetic-native-properties',
                        'evidence': 'urn:synthetic:documented-projection'}))
        return {'coverage_id': 'selection-1', 'requested_fields': fields, 'routes': routes}

    def test_one_explicit_ngd_cover_beats_three_calls_and_preserves_alternatives(self):
        spec = self.fixture()
        before = copy.deepcopy(spec)
        result = plan_query(spec)
        self.assertEqual(spec, before)
        self.assertFalse(result['execution'])
        self.assertTrue(result['candidateOnly'])
        recipes = result['selected']['recipes']
        self.assertEqual([r['route_id'] for r in recipes], ['ngd-documented'])
        self.assertEqual(recipes[0]['serverProjection']['values'], ['a3', 'b26', 'z2'])
        self.assertEqual(recipes[0]['serverProjection']['parameter'], 'synthetic-native-properties')
        self.assertIn('timing evidence is incomplete', result['rationale'])
        self.assertTrue(any(len(a['recipes']) == 3 for a in result['alternatives']))
        self.assertEqual(result['missing_fields'], [])

    def test_unknown_projection_never_fabricates_native_parameter(self):
        spec = self.fixture()
        spec['routes'] = [route('full', spec['requested_fields'],
            projection={'supported': False, 'parameter': 'must-not-be-inferred'})]
        recipe = plan_query(spec)['selected']['recipes'][0]
        self.assertIsNone(recipe['serverProjection'])
        self.assertEqual(recipe['mode'], 'full-record-local-projection')
        self.assertEqual(recipe['localProjection'], ['a3', 'b26', 'z2'])
        self.assertFalse(recipe['execution'])

    def test_download_and_full_record_candidates_remain_available(self):
        spec = self.fixture()
        spec['routes'] += [route('full', spec['requested_fields']),
                           route('download', spec['requested_fields'], kind='download', estimated_requests=2)]
        result = plan_query(spec)
        modes = {recipe['mode'] for alternative in result['alternatives']
                 for recipe in alternative['recipes']}
        self.assertTrue({'full-record-local-projection', 'server-projection',
                         'download-local-projection'} <= modes)

    def test_coverage_mismatch_and_missing_fields_are_explicit(self):
        spec = self.fixture()
        spec['routes'] = [route('wrong', spec['requested_fields'], coverage_id='different')]
        result = plan_query(spec)
        self.assertIsNone(result['selected'])
        self.assertEqual(len(result['missing_fields']), 3)
        self.assertEqual(result['rejected_routes'][0]['reason'], 'coverage-mismatch')
        spec['routes'] = [route('partial', spec['requested_fields'][:1])]
        self.assertEqual(len(plan_query(spec)['missing_fields']), 2)

    def test_exact_identity_requires_native_field_and_collection(self):
        wanted = field('width')
        different = {**wanted, 'native_field': 'height'}
        result = plan_query({'coverage_id': 'selection-1', 'requested_fields': [wanted],
                             'routes': [route('different', [different])]})
        self.assertIsNone(result['selected'])
        self.assertEqual(result['missing_fields'], [wanted])

    def test_independent_cross_collection_requests_need_no_join(self):
        fields = [field('a3', 'collection-a'), field('z2', 'collection-z'),
                  field('b26', 'collection-b')]
        spec = {'coverage_id': 'selection-1', 'requested_fields': fields,
                'routes': [route(str(i), [value]) for i, value in enumerate(fields)]}
        result = plan_query(spec)
        self.assertEqual(len(result['selected']['recipes']), 3)
        self.assertFalse(result['selected']['joins'])
        self.assertEqual(result['selected']['result_mode'], 'bundled-independent-results')

    def test_single_route_cross_collection_claim_needs_documented_capability(self):
        fields = [field('a', 'collection-a'), field('b', 'collection-b')]
        spec = {'coverage_id': 'selection-1', 'requested_fields': fields,
                'routes': [route('unsupported-single', fields)]}
        result = plan_query(spec)
        self.assertIsNone(result['selected'])
        self.assertEqual(result['rejected_routes'][0]['reason'],
                         'single-route-cross-collection-capability-unproven')
        spec['routes'][0]['cross_collection_capability'] = {
            'supported': True, 'evidence': 'urn:synthetic:single-route-spec'}
        self.assertEqual(len(plan_query(spec)['selected']['recipes']), 1)

    def test_reviewed_equivalence_allows_one_physical_route_to_cover_three_concepts(self):
        wanted = [field('a3', 'a'), field('z2', 'z'), field('b26', 'b')]
        physical = [field('native-' + value['native_field'], 'ngd') for value in wanted]
        combined = route('ngd-combined', physical, field_mappings=[
            {'requested_stable_id': concept['stable_id'], 'route_field': native,
             'equivalent': True, 'evidence': 'urn:reviewed:mapping:' + str(i)}
            for i, (concept, native) in enumerate(zip(wanted, physical))],
            projection={'supported': True, 'parameter': 'synthetic-properties',
                        'evidence': 'urn:synthetic:projection'})
        spec = {'coverage_id': 'selection-1', 'requested_fields': wanted,
                'routes': [route(str(i), [value]) for i, value in enumerate(wanted)] + [combined]}
        result = plan_query(spec)
        self.assertEqual([r['route_id'] for r in result['selected']['recipes']], ['ngd-combined'])
        mapping = result['selected']['recipes'][0]['field_mapping']
        self.assertTrue(all(item['method'] == 'reviewed-equivalence' and item['evidence'] for item in mapping))
        self.assertEqual(result['selected']['recipes'][0]['serverProjection']['values'],
                         ['native-a3', 'native-b26', 'native-z2'])
        del combined['field_mappings']
        result = plan_query(spec)
        self.assertEqual(len(result['selected']['recipes']), 3)
        self.assertIn({'route_id': 'ngd-combined', 'reason': 'no-exact-field-identity'},
                      result['rejected_routes'])

    def test_ambiguous_or_unsupported_mappings_rejected(self):
        concept = field('concept', 'source')
        physical = field('physical', 'ngd')
        mapping = {'requested_stable_id': concept['stable_id'], 'route_field': physical,
                   'equivalent': True, 'evidence': 'urn:reviewed:mapping'}
        base = {'coverage_id': 'selection-1', 'requested_fields': [concept],
                'routes': [route('mapped', [physical], field_mappings=[mapping])]}
        for change in ['duplicate', 'no-evidence', 'not-equivalent', 'unknown-native']:
            spec = copy.deepcopy(base)
            mappings = spec['routes'][0]['field_mappings']
            if change == 'duplicate': mappings.append(copy.deepcopy(mapping))
            if change == 'no-evidence': mappings[0]['evidence'] = ''
            if change == 'not-equivalent': mappings[0]['equivalent'] = False
            if change == 'unknown-native': mappings[0]['route_field'] = {**physical, 'native_field': 'other'}
            with self.subTest(change=change), self.assertRaises(ValueError):
                plan_query(spec)

    def test_complete_timing_evidence_changes_optimisation(self):
        spec = self.fixture()
        for candidate in spec['routes']:
            candidate['acquisition_seconds'] = {'min': 1, 'max': 2}
            candidate['processing_seconds'] = {'min': 0, 'max': 0}
        spec['routes'][-1]['processing_seconds'] = {'min': 20, 'max': 30}
        result = plan_query(spec)
        self.assertEqual(len(result['selected']['recipes']), 3)
        self.assertEqual(result['selected']['total_seconds'], {'min': 3, 'max': 6})

    def test_bounded_routes_fields_types_and_costs(self):
        for mutate in [lambda s: s.update(routes=s['routes'] * 5),
                       lambda s: s.update(requested_fields=[]),
                       lambda s: s['routes'][0].update(estimated_requests=True),
                       lambda s: s['routes'][0].update(estimated_bytes=-1),
                       lambda s: s['routes'][0].update(estimated_requests=10**1000),
                       lambda s: s['routes'][0].update(estimated_requests=float('inf')),
                       lambda s: s['routes'][0].update(acquisition_seconds={'min': 2, 'max': 1}),
                       lambda s: s['routes'][0].update(request='arbitrary URL')]:
            spec = self.fixture()
            mutate(spec)
            with self.subTest(spec=spec), self.assertRaises(ValueError):
                plan_query(spec)


    def test_output_requirements_exclude_cheaper_portrayal_for_native_table(self):
        spec = self.fixture(); fields = spec['requested_fields']
        spec['output_requirement'] = {'kind':'table','required_capabilities':['native-values']}
        spec['routes'] = [route('tiles', fields, estimated_requests=0,
            output_capabilities={'portrayal': {'supported':True,'evidence':'urn:synthetic:tile-style'}}),
            route('features', fields, estimated_requests=2,
            output_capabilities={'native-values': {'supported':True,'evidence':'urn:synthetic:native'}})]
        result = plan_query(spec)
        self.assertEqual(result['selected']['recipes'][0]['route_id'], 'features')
        self.assertTrue(result['outputFitEstablished'])
        self.assertEqual(result['rejected_routes'][0]['reason'], 'output-capability-unproven')
        self.assertEqual(result['rejected_routes'][0]['required_capabilities'], ['native-values'])
        self.assertEqual(result['selected']['recipes'][0]['outputCapabilityEvidence'],
                         {'native-values':'urn:synthetic:native'})

    def test_analytical_map_requires_explicit_geometry_and_values_evidence(self):
        spec = self.fixture(); fields = spec['requested_fields']
        spec['output_requirement'] = {'kind':'map','required_capabilities':['native-values','geometry']}
        spec['routes'] = [route('features', fields, output_capabilities={
            'native-values': {'supported':True,'evidence':'urn:synthetic:attributes'},
            'geometry': {'supported':True,'evidence':'urn:synthetic:geometry'}})]
        self.assertTrue(plan_query(spec)['outputFitEstablished'])
        del spec['routes'][0]['output_capabilities']['geometry']['evidence']
        result = plan_query(spec)
        self.assertFalse(result['outputFitEstablished'])
        self.assertIsNone(result['selected'])
        self.assertEqual(result['rejected_routes'][0]['required_capabilities'], ['geometry'])

    def test_map_kind_does_not_infer_renderer_or_native_attributes(self):
        spec = self.fixture(); fields = spec['requested_fields']
        spec['output_requirement'] = {'kind':'map','required_capabilities':['portrayal']}
        spec['routes'] = [route('context', fields, output_capabilities={
            'portrayal': {'supported':True,'evidence':'urn:synthetic:portrayal'}})]
        result = plan_query(spec)
        self.assertTrue(result['outputFitEstablished'])
        self.assertEqual(set(result['selected']['recipes'][0]['outputCapabilityEvidence']), {'portrayal'})
        spec['output_requirement'] = {'kind':'analysis','required_capabilities':['native-values']}
        self.assertIsNone(plan_query(spec)['selected'])

    def test_unknown_or_ambiguous_output_capabilities_are_rejected(self):
        for requirement in [{'kind':'map','required_capabilities':[]},
                            {'kind':'map','required_capabilities':['geometry','geometry']},
                            {'kind':'map','required_capabilities':['measure-from-pixels']},
                            {'kind':'table'}]:
            spec = self.fixture(); spec['output_requirement'] = requirement
            with self.subTest(requirement=requirement), self.assertRaises(ValueError): plan_query(spec)
        spec = self.fixture(); spec['routes'][0]['output_capabilities']={'invented':{}}
        with self.assertRaises(ValueError): plan_query(spec)


    def test_request_and_evidence_credentials_are_rejected_without_echoing_values(self):
        secret = 'SYNTHETIC-CREDENTIAL-NOT-A-REAL-KEY'
        cases = [({'headers':{'key':secret}}, None),
                 ({'headers':{'Authorization':'Bearer '+secret}}, None),
                 ({'url':'https://api.os.uk/synthetic?key='+secret}, None),
                 ({'url':'https://user:'+secret+'@api.os.uk/synthetic'}, None),
                 ({'path':'/synthetic'}, 'https://evidence.invalid/?client_secret='+secret)]
        for request, evidence in cases:
            spec = self.fixture(); spec['routes'][0]['request'] = request
            if evidence:
                spec['routes'][0]['output_capabilities'] = {
                    'native-values': {'supported':True,'evidence':evidence}}
            with self.subTest(request=request), self.assertRaises(ValueError) as raised:
                plan_query(spec)
            self.assertNotIn(secret,str(raised.exception))
        spec = self.fixture(); spec['routes'][0]['request'] = {'key_binding':'OS_API_KEY'}
        self.assertFalse(plan_query(spec)['execution'])
