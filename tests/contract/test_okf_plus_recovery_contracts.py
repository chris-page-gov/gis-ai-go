"""Optional structural contracts against synthetic outputs of actual producers.

These checks do not grant provider authority or verify upstream truth/checksums.
"""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from jsonschema import Draft202012Validator, ValidationError
from scripts.okf_plus import field_cards, field_passages, os_document_sync, os_private_inventory
from scripts.okf_plus.passages import split_document
from scripts.okf_plus.retrieval_plan import plan_retrieval

ROOT = Path(__file__).resolve().parents[2]


class RecoveryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / 'okf-plus/schemas/recovery-operations.schema.json').read_text())
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def outputs(self):
        manifest, _ = split_document(b'# Synthetic\nPavement evidence.\n',
                                    'https://docs.os.uk/osngd/synthetic.md')
        planner = plan_retrieval({'api': {'count': 1}})
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent_path = root / 'okf-plus/records/os-ngd-collections/synthetic.md'
            parent_path.parent.mkdir(parents=True)
            parent_path.write_text('Synthetic parent bytes\n')
            parent = {'@context': {}, '@id': 'urn:synthetic:collection',
                      'nativeIdentifier': 'synthetic-v1', 'resource': 'urn:synthetic:resource',
                      'sources': [], 'rights': {'retrievalAuthority': 'metadata-only'},
                      'okfp:field': [{'@id': 'urn:synthetic:field:width'}]}
            with patch.object(field_cards, 'read_markdown', return_value=(parent, '')):
                cards, index = field_cards.export(root, root / 'artifacts/cards')
            with patch.object(os_private_inventory, 'build_opener'):
                inventory = os_private_inventory.Inventory(root / 'private')
            with patch.object(inventory, 'get', side_effect=[[], {'collections': []}, []]):
                summary = inventory.run()
            coverage = json.loads((root / 'private/coverage.json').read_text())
            source_dir = root / 'okf-plus/source'
            source_dir.mkdir(parents=True)
            for family in os_document_sync.FAMILIES:
                (source_dir / (family + '-documentation.json')).write_text('{"records":[]}')
            capture = Mock()
            capture.ledger = {'requests': []}
            checkpoint = os_document_sync.run(root, max_requests=1,
                capture_factory=lambda *_: capture)
            capture.get.assert_not_called()
            overlay_card = copy.deepcopy(cards[0])
            overlay_card['parent']['nativeIdentifier'] = 'bld-fts-building-4'
            overlay_card['field']['dcterms:identifier'] = 'width'
            item = {'id': overlay_card['field']['@id'], 'parent': overlay_card['parent']['@id'],
                    'parentNativeIdentifier': 'bld-fts-building-4', 'path': 'synthetic.jsonld',
                    'sha256': 'a' * 64}
            with patch.object(field_passages, 'read', side_effect=[
                    {'cards': [item]}, {'records': {}}, overlay_card]):
                overlay_rows = field_passages.overlays(root / 'cards', root / 'private-docs')
            with patch.object(field_passages, 'overlays', return_value=overlay_rows):
                overlay_index = field_passages.export(root)

        return {'fieldCard': cards[0], 'fieldIndex': index, 'privateManifest': manifest,
                'retrievalPlan': planner, 'inventoryCoverage': coverage,
                'inventorySummary': summary, 'documentCheckpoint': checkpoint, 'candidateFieldOverlay': overlay_rows[0],
                'candidateFieldIndex': overlay_index}

    def test_actual_producer_outputs_validate(self):
        for name, output in self.outputs().items():
            with self.subTest(producer=name):
                self.validator.validate(output)

    def test_missing_native_discriminators_rejected(self):
        for name, output in self.outputs().items():
            discriminator = next(key for key in ('schema', 'profile', '@type', 'metadata_only')
                                 if key in output)
            del output[discriminator]
            with self.subTest(producer=name), self.assertRaises(ValidationError):
                self.validator.validate(output)

    def test_authority_and_distribution_mutations_rejected(self):
        outputs = self.outputs()
        mutations = [('candidateFieldIndex', ['candidateOnly'], False),
                     ('candidateFieldOverlay', ['rights', 'executionAdmitted'], True),
                     ('candidateFieldOverlay', ['rights', 'publicationAdmitted'], True),
                     ('retrievalPlan', ['execution'], True),
                     ('retrievalPlan', ['metadata_only'], False),
                     ('privateManifest', ['trust', 'executionAdmitted'], True),
                     ('privateManifest', ['distribution', 'publicationAdmitted'], True),
                     ('privateManifest', ['distribution', 'audience'], 'public'),
                     ('inventoryCoverage', ['featureDataDownloaded'], True),
                     ('inventoryCoverage', ['distribution'], 'public'),
                     ('documentCheckpoint', ['executionAdmitted'], True),
                     ('documentCheckpoint', ['distribution'], 'public'),
                     ('documentCheckpoint', ['scope', 'discoveredLinksFollowed'], True)]
        for name, keys, value in mutations:
            output = copy.deepcopy(outputs[name])
            target = output
            for key in keys[:-1]:
                target = target[key]
            target[keys[-1]] = value
            with self.subTest(producer=name, keys=keys), self.assertRaises(ValidationError):
                self.validator.validate(output)

    def test_missing_evidence_identifiers_rejected(self):
        outputs = self.outputs()
        for name, keys in [('fieldCard', ['provenance', 'parentSha256']),
                           ('fieldIndex', ['cards', 0, 'sha256']),
                           ('privateManifest', ['source', 'sha256']),
                           ('documentCheckpoint', ['scope', 'sources', 0, 'sha256'])]:
            output = copy.deepcopy(outputs[name])
            target = output
            for key in keys[:-1]:
                target = target[key]
            del target[keys[-1]]
            with self.subTest(producer=name), self.assertRaises(ValidationError):
                self.validator.validate(output)
