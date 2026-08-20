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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def registry() -> Registry:
    return Registry().with_resources(
        [
            (schema["$id"], Resource.from_contents(schema))
            for schema in (
                load_json(path) for path in sorted(SCHEMA_DIR.glob("*.schema.json"))
            )
        ]
    )


SCHEMA_REGISTRY = registry()


def validator(name: str) -> Draft202012Validator:
    schema = load_json(SCHEMA_DIR / name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(
        schema,
        registry=SCHEMA_REGISTRY,
        format_checker=FormatChecker(),
    )


def assert_closed(test_case: unittest.TestCase, value: object, path: str = "$") -> None:
    if isinstance(value, dict):
        if value.get("type") == "object":
            test_case.assertIs(
                value.get("additionalProperties"),
                False,
                f"{path} must reject additional properties",
            )
        for key, nested in value.items():
            assert_closed(test_case, nested, f"{path}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            assert_closed(test_case, nested, f"{path}[{index}]")


class ExecutionSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = load_json(FIXTURE_DIR / "execution-request.example.json")
        self.result = load_json(FIXTURE_DIR / "execution-result.example.json")
        self.problem = load_json(FIXTURE_DIR / "execution-problem.example.json")

    def test_schema_ids_are_versioned_and_every_object_is_closed(self) -> None:
        expected = {
            "execution-request.schema.json": "urn:gis-ai-go:schema:execution-request:1",
            "execution-result.schema.json": "urn:gis-ai-go:schema:execution-result:1",
            "execution-problem.schema.json": "urn:gis-ai-go:schema:execution-problem:1",
        }
        for name, schema_id in expected.items():
            with self.subTest(schema=name):
                schema = load_json(SCHEMA_DIR / name)
                self.assertEqual(schema_id, schema["$id"])
                assert_closed(self, schema)

    def test_gateway_python_round_trip_fixtures_validate_and_preserve_context(self) -> None:
        for schema, value in (
            ("execution-request.schema.json", self.request),
            ("execution-result.schema.json", self.result),
            ("execution-problem.schema.json", self.problem),
        ):
            with self.subTest(schema=schema):
                self.assertEqual([], list(validator(schema).iter_errors(value)))

        self.assertEqual(self.request["trace"], self.result["trace"])
        self.assertEqual(
            self.request["parameters"]["source"],
            self.result["evidence"]["source"],
        )

    def test_unknown_fields_operations_crs_axis_and_excessive_limits_fail_closed(self) -> None:
        request_validator = validator("execution-request.schema.json")
        mutations: list[dict[str, Any]] = []
        for path, value in (
            (("unexpected",), True),
            (("operation",), "provider.execute"),
            (("parameters", "unexpected"), True),
            (("parameters", "crs"), "EPSG:3857"),
            (("parameters", "axis_order"), "latitude-longitude"),
            (("parameters", "limit"), 101),
            (("limits", "max_coordinates"), 129),
        ):
            changed = copy.deepcopy(self.request)
            target = changed
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            mutations.append(changed)
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.assertTrue(list(request_validator.iter_errors(mutation)))

    def test_problem_contract_cannot_return_stack_path_or_provider_error(self) -> None:
        problem_validator = validator("execution-problem.schema.json")
        for key in ("stack", "path", "provider_error", "url", "sql"):
            changed = copy.deepcopy(self.problem)
            changed[key] = "sensitive"
            with self.subTest(key=key):
                self.assertTrue(list(problem_validator.iter_errors(changed)))


if __name__ == "__main__":
    unittest.main()
