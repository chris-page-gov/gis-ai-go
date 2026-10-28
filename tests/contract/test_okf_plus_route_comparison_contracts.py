"""Output schemas against real synthetic offline comparison producers."""
import copy
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError
from scripts.okf_plus.route_comparison import compare_routes


class RouteComparisonContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[2] / 'okf-plus/schemas/route-comparison.schema.json'
        cls.schema = json.loads(path.read_text())
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def fixture(self):
        route = {'route_id': 'synthetic-left',
            'call': {'method': 'GET', 'url': 'https://api.os.uk/synthetic/items',
                     'params': {'count': 1}, 'key_binding': 'OS_API_KEY'},
            'context': {'collection': 'synthetic-v1', 'version': '1', 'crs': '27700',
                        'time': 'synthetic-window', 'units': 'metres'},
            'source_independence': False, 'receipt_sha256': 'a' * 64,
            'identity_path': ['id'], 'fields': {'width': ['properties', 'width']},
            'records': [{'id': 'synthetic-1', 'properties': {'width': 3.0}}]}
        right = copy.deepcopy(route); right['route_id'] = 'synthetic-right'
        right['receipt_sha256'] = 'b' * 64
        return {'routes': [route, right], 'requested_fields': ['width'],
                'methodology': 'Exact synthetic native field comparison',
                'code_reference': 'urn:synthetic:method-v1'}

    def produced(self):
        spec = self.fixture()
        agreement = compare_routes(spec)
        spec['routes'][1]['records'][0]['properties']['width'] = 4.0
        spec['include_private_values'] = True
        different = compare_routes(spec)
        spec['routes'][1]['context']['version'] = '2'
        unassessed = compare_routes(spec)
        spec = self.fixture()
        for i, route in enumerate(spec['routes']):
            route.update(http_status=200 if i == 0 else 500, selector_id='same-selector',
                         expected_behavior_refs=['https://docs.os.uk/os-apis/synthetic.md'])
        http = compare_routes(spec)
        return {'agreement': agreement, 'different': different, 'unassessed': unassessed,
                'http': http, 'standalone_case': different['support_case']}

    def test_actual_agreement_difference_unassessed_http_and_case_outputs(self):
        for name, output in self.produced().items():
            with self.subTest(output=name): self.validator.validate(output)

    def test_missing_hash_and_authority_changes_rejected(self):
        source = self.produced()['different']
        mutations = [(['execution'], True), (['distribution'], 'public'),
                     (['candidateOnly'], False), (['support_case', 'sendingAdmitted'], True),
                     (['support_case', 'execution'], True),
                     (['support_case', 'calls', 0, 'receipt_sha256'], None)]
        for keys, value in mutations:
            output = copy.deepcopy(source); target = output
            for key in keys[:-1]: target = target[key]
            if value is None: del target[keys[-1]]
            else: target[keys[-1]] = value
            with self.subTest(keys=keys), self.assertRaises(ValidationError):
                self.validator.validate(output)

    def test_non_comparable_observations_cannot_claim_comparisons(self):
        source = self.produced()['unassessed']
        for keys, value in [(['observations', 0, 'comparable'], True),
                            (['observations', 0, 'fields', 0, 'comparable'], True),
                            (['observations', 0, 'fields', 0, 'N'], 1),
                            (['observations', 0, 'fields', 0, 'concordance_fraction'], 1.0)]:
            output = copy.deepcopy(source); target = output
            for key in keys[:-1]: target = target[key]
            target[keys[-1]] = value
            with self.subTest(keys=keys), self.assertRaises(ValidationError):
                self.validator.validate(output)

    def test_invented_confidence_and_sending_grants_rejected(self):
        for name, output in self.produced().items():
            output['statistical_confidence'] = .99
            with self.subTest(output=name), self.assertRaises(ValidationError):
                self.validator.validate(output)
