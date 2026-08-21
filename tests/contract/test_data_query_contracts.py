from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas"
FIXTURE_DIR = ROOT / "providers" / "fixtures"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def registry() -> Registry:
    resources = []
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        schema = load(path)
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def validator(name: str) -> Draft202012Validator:
    schema = load(SCHEMA_DIR / name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(
        schema,
        registry=registry(),
        format_checker=FormatChecker(),
    )


def assert_closed(test_case: unittest.TestCase, node: object, path: str = "$") -> None:
    if isinstance(node, dict):
        if node.get("type") == "object":
            test_case.assertIs(
                node.get("additionalProperties"),
                False,
                f"{path} must reject unknown properties",
            )
        for key, value in node.items():
            assert_closed(test_case, value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            assert_closed(test_case, value, f"{path}[{index}]")


class DataQueryContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parameters = load(FIXTURE_DIR / "data-query-parameters.example.json")
        self.result = load(FIXTURE_DIR / "data-query-result.example.json")
        self.problem = load(FIXTURE_DIR / "data-query-problem.example.json")
        self.cancelled_problem = load(
            FIXTURE_DIR / "data-query-cancelled-problem.example.json"
        )
        self.deadline_problem = load(
            FIXTURE_DIR / "data-query-deadline-exceeded-problem.example.json"
        )

    def test_schema_ids_are_stable_and_every_object_is_closed(self) -> None:
        expected = {
            "data-query-parameters.schema.json": (
                "urn:gis-ai-go:schema:data-query-parameters:v1"
            ),
            "data-query-result.schema.json": (
                "urn:gis-ai-go:schema:data-query-result:v1"
            ),
            "data-query-problem.schema.json": (
                "urn:gis-ai-go:schema:data-query-problem:v1"
            ),
        }
        for name, schema_id in expected.items():
            with self.subTest(schema=name):
                schema = load(SCHEMA_DIR / name)
                Draft202012Validator.check_schema(schema)
                self.assertEqual(schema_id, schema["$id"])
                assert_closed(self, schema)
        self.assertEqual(
            10,
            len(load(SCHEMA_DIR / "data-query-problem.schema.json")["oneOf"]),
        )

    def test_exact_parameters_and_success_fixture_validate(self) -> None:
        parameters = validator("data-query-parameters.schema.json")
        result = validator("data-query-result.schema.json")
        self.assertTrue(parameters.is_valid(self.parameters))
        self.assertTrue(result.is_valid(self.result))
        self.assertEqual(5, len(self.parameters))
        self.assertEqual(1, self.parameters["limit"])
        self.assertEqual(
            ["time", "geography", "week", "causeofdeath"],
            [entry["dimension"] for entry in self.parameters["selections"]],
        )
        self.assertEqual("10471", self.result["data"]["observations"][0]["value"])
        self.assertIsNone(self.result["data"]["observations"][0]["unit"])
        selection_plan_path = SCHEMA_DIR / "selection-plan.schema.json"
        if selection_plan_path.exists():
            self.assertEqual(
                self.parameters,
                load(selection_plan_path)["const"]["data_query"],
                "the independently validated query must equal selection plan output",
            )

    def test_parameter_and_result_drift_fail_closed(self) -> None:
        parameters = validator("data-query-parameters.schema.json")
        result = validator("data-query-result.schema.json")
        mutations: list[tuple[str, dict[str, Any], Draft202012Validator]] = []
        for label, path, value in [
            ("latest version", ["dataset", "version"], "latest"),
            ("second item", ["limit"], 2),
            ("caller URL", ["url"], "https://example.invalid"),
        ]:
            candidate = copy.deepcopy(self.parameters)
            target = candidate
            for member in path[:-1]:
                target = target[member]
            target[path[-1]] = value
            mutations.append((label, candidate, parameters))

        reordered = copy.deepcopy(self.parameters)
        reordered["selections"].reverse()
        mutations.append(("selection order", reordered, parameters))

        for label, path, value in [
            ("decimal observation", ["data", "observations", 0, "value"], "10.5"),
            ("invented unit", ["data", "observations", 0, "unit"], "deaths"),
            ("wrong provider", ["evidence_binding", "provider_id"], "other"),
            ("wrong operation", ["operation"], "selection.resolve"),
        ]:
            candidate = copy.deepcopy(self.result)
            target: Any = candidate
            for member in path[:-1]:
                target = target[member]
            target[path[-1]] = value
            mutations.append((label, candidate, result))

        for label, candidate, checked_by in mutations:
            with self.subTest(mutation=label):
                self.assertFalse(checked_by.is_valid(candidate))

    def test_problems_are_closed_receipt_free_and_non_reflective(self) -> None:
        problem = validator("data-query-problem.schema.json")
        for fixture in [
            self.problem,
            self.cancelled_problem,
            self.deadline_problem,
        ]:
            with self.subTest(code=fixture["code"]):
                self.assertTrue(problem.is_valid(fixture))
        forbidden = {
            "abort_reason",
            "adapter_code",
            "credential",
            "deadline",
            "evidence_receipt",
            "provider_status",
            "raw_error",
            "reason",
            "stack",
            "token",
        }
        for fixture in [
            self.problem,
            self.cancelled_problem,
            self.deadline_problem,
        ]:
            self.assertTrue(forbidden.isdisjoint(fixture))
            for key in forbidden:
                candidate = copy.deepcopy(fixture)
                candidate[key] = "secret"
                with self.subTest(code=fixture["code"], extra=key):
                    self.assertFalse(problem.is_valid(candidate))


if __name__ == "__main__":
    unittest.main()
