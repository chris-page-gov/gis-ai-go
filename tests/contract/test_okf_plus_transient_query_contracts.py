"""Optional structural assurance using synthetic producer outputs, never network."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator, ValidationError
from scripts.okf_plus import ngd_extract, transient_profile
from scripts.okf_plus.query_planner import plan_query

ROOT = Path(__file__).resolve().parents[2]


class TransientQueryContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = ROOT / 'okf-plus/schemas/transient-query.schema.json'
        cls.schema = json.loads(cls.path.read_text())
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def outputs(self):
        identity = {'stable_id': 'urn:synthetic:width', 'native_field': 'width',
                    'collection_id': 'synthetic-v1'}
        plan = plan_query({'coverage_id': 'synthetic-selection',
            'requested_fields': [identity], 'routes': [{'route_id': 'synthetic-api',
                'coverage_id': 'synthetic-selection', 'collection_id': 'synthetic-v1',
                'fields': [identity], 'kind': 'api', 'request': {'path': '/synthetic'},
                'estimated_requests': 1}]})
        features = [{'type': 'Feature', 'id': str(i), 'geometry': None,
                     'properties': {'width': i + 1}} for i in range(2)]
        body = json.dumps({'type': 'FeatureCollection', 'features': features,
                           'numberReturned': 2, 'numberMatched': 2, 'links': []}).encode()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(ngd_extract, 'ROOT', root), patch.object(transient_profile, 'ROOT', root):
                receipt = ngd_extract.extract('synthetic-v1', [-1, 50, 0, 51],
                    key='SYNTHETIC-PRIVATE-KEY', sleep=lambda _: None,
                    transport=lambda *_: (200, body, {'Content-Crs': ngd_extract.CRS['27700']}))
                selection_dir = next((root / 'artifacts').rglob('receipt.json')).parent
                before_discard = copy.deepcopy(receipt)
                profile_path = root / 'artifacts/profile.json'
                profile = transient_profile.profile(selection_dir / 'features.ndjson', profile_path,
                    recipe={'selectionDigest': selection_dir.name},
                    schema={'type': 'object', 'properties': {'properties': {
                        'type': 'object', 'properties': {'width': {'type': 'number'}}}}})
                index = transient_profile.export_field_knowledge(profile_path, root / 'artifacts/knowledge')
                card_path = root / 'artifacts/knowledge' / index['fields'][0]['file']
                card = json.loads(card_path.read_text())
                discarded = ngd_extract.discard_payloads(selection_dir, profile_path)
                self.assertFalse((selection_dir / 'features.ndjson').exists())
        return {'query': plan, 'profile': profile, 'index': index, 'card': card,
                'receipt': before_discard, 'discarded': discarded}

    def test_real_synthetic_producer_outputs_and_compact_schema(self):
        self.assertLess(self.path.stat().st_size, 32 * 1024)
        for name, output in self.outputs().items():
            with self.subTest(producer=name):
                self.validator.validate(output)

    def test_selection_complete_and_scan_complete_do_not_claim_national_coverage(self):
        outputs = self.outputs()
        self.assertTrue(outputs['receipt']['complete'])
        self.assertTrue(outputs['profile']['scanComplete'])
        self.assertEqual(outputs['profile']['recordCount'], 2)
        self.assertEqual(outputs['card']['observedScope']['recordCount'], 2)
        self.assertFalse(outputs['card']['observedScope']['providerUniverseComplete'])
        self.assertFalse(outputs['receipt']['snapshotIsolation'])
        outputs['card']['observedScope']['providerUniverseComplete'] = True
        with self.assertRaises(ValidationError):
            self.validator.validate(outputs['card'])

    def test_authority_private_and_complete_mutations_rejected(self):
        mutations = [('query', ['execution'], True), ('query', ['candidateOnly'], False),
            ('query', ['selected', 'recipes', 0, 'execution'], True),
            ('query', ['joins'], True), ('profile', ['scanComplete'], False),
            ('profile', ['executionAdmitted'], True), ('profile', ['distribution'], 'public'),
            ('index', ['distribution'], 'public'), ('index', ['executionAdmitted'], True),
            ('card', ['rights', 'distribution'], 'public'), ('card', ['rights', 'executionAdmitted'], True),
            ('card', ['observedScope', 'scanComplete'], False), ('receipt', ['snapshotIsolation'], True)]
        outputs = self.outputs()
        for name, keys, value in mutations:
            output = copy.deepcopy(outputs[name])
            target = output
            for key in keys[:-1]: target = target[key]
            target[keys[-1]] = value
            with self.subTest(producer=name, keys=keys), self.assertRaises(ValidationError):
                self.validator.validate(output)
        for name, output in outputs.items():
            output['retrievalGranted'] = True
            with self.subTest(producer=name, grant=True), self.assertRaises(ValidationError):
                self.validator.validate(output)

    def test_required_provenance_and_disposal_binding_rejected_when_missing(self):
        outputs = self.outputs()
        for name, keys in [('profile', ['inputSha256']), ('profile', ['declaredSchemaSha256']),
                ('profile', ['retrievalRecipeSha256']), ('index', ['profileSha256']),
                ('card', ['evidenceHashes', 'profileSha256']), ('card', ['prov:wasDerivedFrom']),
                ('receipt', ['ndjsonSha256']), ('discarded', ['profilePath']),
                ('discarded', ['profileSha256'])]:
            output = copy.deepcopy(outputs[name])
            target = output
            for key in keys[:-1]: target = target[key]
            del target[keys[-1]]
            with self.subTest(producer=name, keys=keys), self.assertRaises(ValidationError):
                self.validator.validate(output)

    def test_large_schema_definition_parts_and_navigation_validate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(transient_profile, 'ROOT', root):
                source = root / 'input.ndjson'
                source.write_text(json.dumps({'type':'Feature','properties':{'width':3}})+'\n')
                profile_path = root / 'artifacts/profile.json'
                transient_profile.profile(source, profile_path, schema={'properties': {
                    'properties': {'type':'object','description':'rich definition ' * 2000,
                        'properties':{'width':{'type':'number'}}}}})
                destination = root / 'artifacts/knowledge'
                index = transient_profile.export_field_knowledge(profile_path, destination)
                self.validator.validate(index)
                self.assertTrue(index['definitionFiles'])
                for output_path in destination.iterdir():
                    self.validator.validate(json.loads(output_path.read_text()))
                parent = next(json.loads((destination / item['file']).read_text())
                    for item in index['fields'] if item['path'] == ['properties'])
                self.assertTrue(parent['childCards'])
                bad = copy.deepcopy(parent)
                del bad['declaredFieldDefinitionRef']['sha256']
                with self.assertRaises(ValidationError): self.validator.validate(bad)
