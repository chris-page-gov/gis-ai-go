"""Shape checks for the public, fictional field-documentary widget fixture."""
import copy
import json
from pathlib import Path
import subprocess
import unittest

from jsonschema import Draft202012Validator, ValidationError


ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "examples" / "geography-task-experience"


class FieldDocumentaryBrowserSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(
            (COMPONENT / "field-documentary-browser.schema.json").read_text()
        )
        cls.validator = Draft202012Validator(cls.schema)
        run = subprocess.run(
            ["node", "-e", "process.stdout.write(JSON.stringify(require('./synthetic-field-links.cjs').fixture()))"],
            cwd=COMPONENT, check=True, capture_output=True, text=True, timeout=10,
        )
        cls.fixture = json.loads(run.stdout)

    def test_schema_and_complete_fictional_fixture(self):
        Draft202012Validator.check_schema(self.schema)
        self.validator.validate(self.fixture)
        self.assertEqual(len(self.fixture["documents"]), 1)
        self.assertEqual(len(self.fixture["fields"]), 12)
        self.assertFalse(self.fixture["globalComplete"])

    def test_wrapper_extras_and_missing_evidence_refused(self):
        for mutate in (
            lambda p: p.update(extra="unknown"),
            lambda p: p.pop("basis"),
            lambda p: p["fields"][0].pop("provenance"),
            lambda p: p["resources"][0].update(extra="unknown"),
        ):
            with self.subTest(mutation=mutate):
                value = copy.deepcopy(self.fixture)
                mutate(value)
                with self.assertRaises(ValidationError):
                    self.validator.validate(value)

    def test_array_limits_and_empty_selection_refused(self):
        for key, maximum in (("resources", 64), ("documents", 16),
                             ("sections", 1024), ("fields", 2048)):
            for replacement in ([], [self.fixture[key][0]] * (maximum + 1)):
                with self.subTest(key=key, length=len(replacement)):
                    value = copy.deepcopy(self.fixture)
                    value[key] = replacement
                    with self.assertRaises(ValidationError):
                        self.validator.validate(value)

    def test_native_null_empty_and_order_survive_schema_validation(self):
        value = copy.deepcopy(self.fixture)
        before = json.dumps(value, ensure_ascii=False)
        self.validator.validate(value)
        self.assertEqual(json.dumps(value, ensure_ascii=False), before)
        self.assertEqual(value["fields"][0]["native"]["nativeProperty"]["enum"],
                         ["A", None, ""])
        self.assertIsNone(value["documents"][0]["publicationDate"])


if __name__ == "__main__":
    unittest.main()
