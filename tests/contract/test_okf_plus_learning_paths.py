"""Check reusable learning paths against retained records and navigation limits."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import sys
import unittest
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/okf_plus"))
from model import read_markdown, safe_reference
from build import validate_record


class LearningPathRecords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = [(p, *read_markdown(p)) for p in sorted(
            (ROOT / "okf-plus/records/learning-path").glob("*.md"))]
        # Locate only referenced records. Read the identity line for indexing;
        # full definitions and source bindings are loaded for every actual link.
        cls.locations = {}
        for path in (ROOT / "okf-plus/records").rglob("*.md"):
            with path.open(encoding="utf-8") as handle:
                for _ in range(5):
                    line = handle.readline()
                    if '"@id":' in line:
                        cls.locations[json.loads("{" + line.strip().rstrip(",") + "}")["@id"]] = path
                        break
        cls.schema = json.loads((ROOT / "okf-plus/schemas/learning-path.schema.json").read_text())
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)
        cls.record_validator = Draft202012Validator(json.loads(
            (ROOT / "okf-plus/schemas/record.schema.json").read_text()))

    def test_paths_are_small_valid_authored_records_with_no_execution_claim(self):
        self.assertEqual({r[1]["nativeIdentifier"] for r in self.paths},
                         {"pavement-width", "building-heights", "road-elevation"})
        for path, row, _ in self.paths:
            with self.subTest(path=path.name):
                self.assertLess(path.stat().st_size, 16 * 1024)
                self.record_validator.validate(row)
                validate_record(row, path, {})
                self.validator.validate(row["details"]["learningPath"])
                self.assertFalse(row["okfp:machineImported"])
                self.assertFalse(row["rights"]["executionAdmitted"])
                self.assertEqual(row["type"], "Documentation")
                self.assertNotIn("programme", row["details"]["learningPath"])
                self.assertNotIn("assertions", row)

    def test_every_ordered_step_and_concept_resolves_to_retained_evidence(self):
        for path, row, body in self.paths:
            with self.subTest(path=path.name):
                learning = row["details"]["learningPath"]
                step_ids = [s["recordId"] for s in learning["steps"]]
                self.assertEqual(len(step_ids), len(set(step_ids)))
                all_ids = {x["recordId"] for x in learning["prerequisiteConcepts"]}
                all_ids.update(step_ids)
                all_ids.update(x for s in learning["steps"] for x in s["conceptRefs"])
                for identity in all_ids:
                    self.assertIn(identity, self.locations)
                    target, _ = read_markdown(self.locations[identity])
                    self.assertEqual(target["@id"], identity)
                for step in learning["steps"]:
                    target, _ = read_markdown(self.locations[step["recordId"]])
                    allowed = {target["resource"], *(s["resource"] for s in target["sources"])}
                    for source in step["sourceRefs"]:
                        self.assertIn(source, allowed)
                        safe_reference(source)
                        parsed = urlsplit(source)
                        self.assertEqual(parsed.scheme, "https")
                        self.assertFalse(parsed.username or parsed.password or parsed.query)
                for destination in re.findall(r"\]\(([^)]+)\)", body):
                    if not destination.startswith("https://"):
                        self.assertTrue((path.parent / destination).resolve().is_file(), destination)

    def test_prerequisites_are_local_paths_and_have_no_cycle(self):
        paths = {row["details"]["learningPath"]["id"]: row["details"]["learningPath"]
                 for _, row, _ in self.paths}

        def walk(identity, ancestors):
            self.assertNotIn(identity, ancestors)
            self.assertIn(identity, paths)
            for parent in paths[identity]["prerequisites"]:
                walk(parent, [*ancestors, identity])

        for identity in paths:
            walk(identity, [])

    def test_schema_refuses_unbounded_or_executable_navigation(self):
        original = self.paths[0][1]["details"]["learningPath"]
        cases = []
        value = copy.deepcopy(original); value["steps"][0]["recordId"] = "javascript:alert(1)"; cases.append(value)
        value = copy.deepcopy(original); value["steps"][0]["sourceRefs"] = ["file:///tmp/source"]; cases.append(value)
        value = copy.deepcopy(original); value["steps"] *= 25; cases.append(value)
        value = copy.deepcopy(original); value["steps"][0]["minutes"] = 481; cases.append(value)
        value = copy.deepcopy(original); value["steps"][0]["practice"] = "x" * 1201; cases.append(value)
        value = copy.deepcopy(original); value["steps"][0]["execute"] = True; cases.append(value)
        for value in cases:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    self.validator.validate(value)


if __name__ == "__main__":
    unittest.main()
