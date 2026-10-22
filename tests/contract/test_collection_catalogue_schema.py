"""Fictional catalogue/schema checks; no source acquisition or new dependencies."""
import copy
import json
from pathlib import Path
import subprocess
import unittest

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2] / 'examples/geography-task-experience'


class CatalogueSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / 'collection-catalogue.schema.json').read_text())
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)
        text = subprocess.check_output(
            ['node', '-e', 'process.stdout.write(JSON.stringify(require("./synthetic-collections.cjs").catalogue()))'],
            cwd=ROOT, text=True, timeout=10,
        )
        cls.fixture = json.loads(text)

    def test_complete_fictional_five_collection_fixture(self):
        self.validator.validate(self.fixture)
        self.assertEqual(len(self.fixture['collections']), 5)
        self.assertTrue(all(x['schemeCount'] == 2 and x['entryCount'] == 26 for x in self.fixture['collections']))

    def test_closed_catalogue_and_collection_fields(self):
        for path in [(), ('collections', 0)]:
            value = copy.deepcopy(self.fixture)
            target = value
            for part in path:
                target = target[part]
            target['url'] = 'https://example.invalid/arbitrary'
            with self.assertRaises(ValidationError):
                self.validator.validate(value)

    def test_bounds_and_global_coverage_are_not_widened(self):
        for key, value in [('schemeCount', 65), ('schemeCount', 0), ('entryCount', -1), ('entryCount', True), ('coverage', 'complete')]:
            fixture = copy.deepcopy(self.fixture)
            fixture['collections'][0][key] = value
            with self.assertRaises(ValidationError):
                self.validator.validate(fixture)
        fixture = copy.deepcopy(self.fixture)
        fixture['globalComplete'] = True
        with self.assertRaises(ValidationError):
            self.validator.validate(fixture)


if __name__ == '__main__':
    unittest.main(verbosity=2)
