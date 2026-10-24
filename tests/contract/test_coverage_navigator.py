"""Fictional coverage-navigation structural contract, with no supplier input."""
import copy
import json
from pathlib import Path
import subprocess
import unittest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / 'okf-plus/schemas/coverage-navigator.schema.json'
FIXTURE = ROOT / 'examples/geography-task-experience/synthetic-coverage.cjs'

class CoverageNavigatorSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA.read_text())
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())
        cls.fixture = json.loads(subprocess.check_output(['node', str(FIXTURE)], timeout=10))

    def test_fictional_complete_payload(self):
        self.validator.validate(self.fixture)

    def test_closed_nested_shapes(self):
        for path in [(), ('basis',), ('counts',), ('rows', 0), ('rows', 0, 'gates', 0), ('rows', 0, 'evidence', 0), ('nodes', 0), ('edges', 0)]:
            with self.subTest(path=path):
                value = copy.deepcopy(self.fixture); node = value
                for part in path: node = node[part]
                node['unexpected'] = True
                self.assertTrue(list(self.validator.iter_errors(value)))

    def test_false_coverage_and_invalid_date(self):
        for key, value in [('fullCoverage', True), ('percentage', 100), ('asOf', '2026-02-29')]:
            with self.subTest(key=key):
                p = copy.deepcopy(self.fixture); p[key] = value
                self.assertTrue(list(self.validator.iter_errors(p)))

    def test_unsafe_link_and_null_text(self):
        for key, value in [('sourceUrl', 'https://example.org/x?key=fictional'), ('label', None), ('scope', ['included'])]:
            with self.subTest(key=key):
                p = copy.deepcopy(self.fixture); p['rows'][0][key] = value
                self.assertTrue(list(self.validator.iter_errors(p)))

    def test_source_caps_are_explicit(self):
        self.assertEqual(self.schema['properties']['rows']['maxItems'], 256)
        self.assertEqual(self.schema['properties']['edges']['maxItems'], 128)
        p = copy.deepcopy(self.fixture); p['rows'] = [p['rows'][0]] * 257
        self.assertTrue(list(self.validator.iter_errors(p)))

    def test_empty_supplied_basis_is_not_missing_structure(self):
        p = copy.deepcopy(self.fixture); p['rows'] = []; p['edges'] = []; p['nodes'] = []
        p['counts'] = dict.fromkeys(p['counts'], 0)
        self.validator.validate(p)

if __name__ == '__main__': unittest.main()
