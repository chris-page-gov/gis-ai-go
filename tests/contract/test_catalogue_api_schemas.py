from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas"

SCHEMA_IDS = {
    "catalogue-search-request.schema.json": (
        "urn:gis-ai-go:schema:catalogue-search-request:v1"
    ),
    "catalogue-describe-request.schema.json": (
        "urn:gis-ai-go:schema:catalogue-describe-request:v1"
    ),
    "catalogue-result.schema.json": "urn:gis-ai-go:schema:catalogue-result:v1",
    "catalogue-problem.schema.json": "urn:gis-ai-go:schema:catalogue-problem:v1",
}


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def validator(name: str) -> Draft202012Validator:
    schema = load_schema(name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def assert_valid(
    test_case: unittest.TestCase,
    schema_validator: Draft202012Validator,
    instance: object,
) -> None:
    errors = sorted(schema_validator.iter_errors(instance), key=lambda error: list(error.path))
    test_case.assertEqual([], [error.message for error in errors])


def assert_invalid(
    test_case: unittest.TestCase,
    schema_validator: Draft202012Validator,
    instance: object,
) -> None:
    test_case.assertTrue(list(schema_validator.iter_errors(instance)))


def assert_objects_are_closed(test_case: unittest.TestCase, node: object, path: str = "$") -> None:
    if isinstance(node, dict):
        if node.get("type") == "object":
            if path == "$.$defs.source_native_object":
                test_case.assertIsInstance(
                    node.get("additionalProperties"),
                    dict,
                    "source-native fields must use the bounded recursive value schema",
                )
            else:
                test_case.assertIs(
                    node.get("additionalProperties"),
                    False,
                    f"{path} must reject unknown properties",
                )
        for key, value in node.items():
            assert_objects_are_closed(test_case, value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            assert_objects_are_closed(test_case, value, f"{path}[{index}]")


CATALOGUE = {
    "id": "gis-ai-go:bundle:public-discovery",
    "version": "0.1.0",
    "revision": "a" * 40,
    "content_root_sha256": "c" * 64,
    "record_count": 36,
    "reviewed_at": "2026-08-20T00:00:00Z",
    "stale_after": "2027-02-20T00:00:00Z",
}
SEARCH_RECORD = {
    "id": "hmlr:dataset:inspire-index-polygons",
    "type": "dataset",
    "title": "HM Land Registry INSPIRE index polygons",
    "description": "Public discovery metadata with a non-legal boundary caveat.",
    "authority": "source-authoritative",
    "access": "public-metadata",
    "rights": "open-with-conditions",
    "freshness": "current",
    "status": "candidate-metadata",
    "tags": ["hmlr", "boundaries"],
}


class CatalogueApiSchemaTests(unittest.TestCase):
    def test_schema_ids_are_stable_and_every_object_is_closed(self) -> None:
        for name, expected_id in SCHEMA_IDS.items():
            with self.subTest(schema=name):
                schema = load_schema(name)
                Draft202012Validator.check_schema(schema)
                self.assertEqual(expected_id, schema["$id"])
                assert_objects_are_closed(self, schema)

    def test_search_request_accepts_only_bounded_controlled_filters(self) -> None:
        schema_validator = validator("catalogue-search-request.schema.json")
        request = {
            "query": "open boundary statistics",
            "facets": {
                "types": ["dataset"],
                "authority": ["source-authoritative"],
                "access": ["public-metadata"],
                "rights": ["open-with-conditions"],
                "freshness": ["current"],
                "tags": ["hmlr"],
            },
            "limit": 20,
            "cursor": "opaque-cursor",
        }
        assert_valid(self, schema_validator, request)
        assert_valid(self, schema_validator, {})

        schema = load_schema("catalogue-search-request.schema.json")
        self.assertEqual(20, schema["properties"]["limit"]["default"])
        self.assertIn(
            "10 normalised terms",
            schema["properties"]["query"]["$comment"],
        )

        invalid_requests = [
            {**request, "query": "q" * 257},
            {**request, "limit": 0},
            {**request, "limit": 101},
            {**request, "cursor": "c" * 1025},
            {**request, "unexpected": True},
            {**request, "facets": {"provider": ["hmlr"]}},
            {**request, "facets": {"types": ["collection"]}},
            {**request, "facets": {"types": ["dataset", "dataset"]}},
        ]
        for invalid in invalid_requests:
            with self.subTest(invalid=invalid):
                assert_invalid(self, schema_validator, invalid)

    def test_describe_request_requires_a_bounded_id_and_allowlisted_includes(self) -> None:
        schema_validator = validator("catalogue-describe-request.schema.json")
        request = {
            "record_id": "hmlr:dataset:inspire-index-polygons",
            "include": ["relationships", "sources"],
        }
        assert_valid(self, schema_validator, request)
        assert_valid(self, schema_validator, {"record_id": request["record_id"]})

        invalid_requests = [
            {},
            {"record_id": ""},
            {"record_id": "r" * 513},
            {**request, "include": []},
            {**request, "include": ["sources", "sources"]},
            {**request, "include": ["rights"]},
            {**request, "include": ["details"]},
            {**request, "unexpected": True},
        ]
        for invalid in invalid_requests:
            with self.subTest(invalid=invalid):
                assert_invalid(self, schema_validator, invalid)

    def test_search_success_envelope_is_bounded(self) -> None:
        schema_validator = validator("catalogue-result.schema.json")
        result = {
            "schema": "gis-ai-go.catalogue-result.v1",
            "operation": "catalogue.search",
            "request_id": "request-001",
            "trace_id": "0" * 32,
            "catalogue": CATALOGUE,
            "warnings": [],
            "data": {
                "records": [SEARCH_RECORD],
                "facets": {
                    "types": [{"value": "dataset", "count": 1}],
                    "authority": [{"value": "source-authoritative", "count": 1}],
                    "access": [{"value": "public-metadata", "count": 1}],
                    "rights": [{"value": "open-with-conditions", "count": 1}],
                    "freshness": [{"value": "current", "count": 1}],
                    "tags": [{"value": "hmlr", "count": 1}],
                },
                "page": {
                    "limit": 20,
                    "returned": 1,
                    "matched": 1,
                    "next_cursor": None,
                },
            },
        }
        assert_valid(self, schema_validator, result)

        unsupported_evidence = copy.deepcopy(result)
        unsupported_evidence["evidence"] = {
            "receipt_id": "receipt_catalogue_001",
            "receipt_digest": f"sha256:{'b' * 64}",
        }
        assert_invalid(self, schema_validator, unsupported_evidence)

        unknown = copy.deepcopy(result)
        unknown["data"]["records"][0]["details"] = {"arbitrary": True}
        assert_invalid(self, schema_validator, unknown)

        too_many_records = copy.deepcopy(result)
        too_many_records["data"]["records"] = [
            {**SEARCH_RECORD, "id": f"record:{index}"} for index in range(101)
        ]
        assert_invalid(self, schema_validator, too_many_records)

        uncontrolled_facet = copy.deepcopy(result)
        uncontrolled_facet["data"]["facets"]["types"] = [
            {"value": "collection", "count": 1}
        ]
        assert_invalid(self, schema_validator, uncontrolled_facet)

    def test_describe_success_envelope_has_bounded_optional_expansions(self) -> None:
        schema_validator = validator("catalogue-result.schema.json")
        result = {
            "schema": "gis-ai-go.catalogue-result.v1",
            "operation": "catalogue.describe",
            "request_id": "request-002",
            "trace_id": "1" * 32,
            "catalogue": CATALOGUE,
            "warnings": [
                "This catalogue contains public metadata and does not execute providers."
            ],
            "data": {
                "record": {
                    "id": SEARCH_RECORD["id"],
                    "type": "dataset",
                    "title": SEARCH_RECORD["title"],
                    "description": SEARCH_RECORD["description"],
                    "authority": {
                        "class": "source-authoritative",
                        "statement": "HM Land Registry is the source authority.",
                        "source": "S-HMLR-INSPIRE",
                    },
                    "publication": {
                        "classification": "public",
                        "contains_personal_data": False,
                        "contains_protected_data": False,
                    },
                    "access": {
                        "tier": "open",
                        "state": "public-metadata",
                        "authentication": "none",
                    },
                    "rights": {
                        "state": "open-with-conditions",
                        "record_licence": "MIT",
                        "described_resource_licence": "Open Government Licence",
                        "attribution": (
                            "Contains HM Land Registry public sector information."
                        ),
                    },
                    "freshness": {
                        "observed_at": "2026-08-19T12:00:00Z",
                        "reviewed_at": "2026-08-20T12:00:00Z",
                        "stale_after": "2027-02-20T12:00:00Z",
                        "status": "current",
                    },
                    "status": "candidate-metadata",
                    "source_refs": ["S-HMLR-INSPIRE"],
                    "limitations": [
                        "Indicative geometry does not establish an exact legal boundary."
                    ],
                    "tags": ["hmlr", "boundaries"],
                    "details": {
                        "publisher": "HM Land Registry",
                        "publisherLastUpdated": "2026-07-28",
                        "sourceNativeId": "hmlr-inspire-index-polygons",
                        "formats": ["GML"],
                        "recordSha256": "a" * 64,
                    },
                },
                "included": {
                    "relationships": [
                        {"relation": "source", "record_id": "S-HMLR-INSPIRE"}
                    ],
                    "sources": [
                        {
                            "id": "S-HMLR-INSPIRE",
                            "title": "HM Land Registry INSPIRE guidance",
                            "authority": "source-authoritative",
                            "access": "public",
                            "rights": "metadata-citation",
                            "freshness": "current",
                        }
                    ],
                },
            },
        }
        assert_valid(self, schema_validator, result)

        duplicate = copy.deepcopy(result)
        duplicate["data"]["included"]["relationships"] *= 2
        assert_invalid(self, schema_validator, duplicate)

        disallowed = copy.deepcopy(result)
        disallowed["data"]["included"]["details"] = []
        assert_invalid(self, schema_validator, disallowed)

        unsafe_details = copy.deepcopy(result)
        unsafe_details["data"]["record"]["details"] = {
            "publisher": "trusted\u202eevil"
        }
        assert_invalid(self, schema_validator, unsafe_details)

        dangerous_details = copy.deepcopy(result)
        dangerous_details["data"]["record"]["details"] = {
            "__proto__": {"polluted": True}
        }
        assert_invalid(self, schema_validator, dangerous_details)

        unsafe_key = copy.deepcopy(result)
        unsafe_key["data"]["record"]["details"] = {"trusted\u202eevil": True}
        assert_invalid(self, schema_validator, unsafe_key)

    def test_problem_envelope_rejects_unbounded_or_unknown_data(self) -> None:
        schema_validator = validator("catalogue-problem.schema.json")
        problem = {
            "schema": "gis-ai-go.catalogue-problem.v1",
            "type": "urn:gis-ai-go:problem:invalid-request",
            "title": "Invalid request",
            "status": 400,
            "code": "invalid_request",
            "detail": "The limit must be between 1 and 100.",
            "instance": "/requests/request-003",
            "request_id": "request-003",
            "trace_id": "2" * 32,
            "errors": [
                {
                    "path": "$.limit",
                    "code": "out_of_range",
                    "message": "Use an integer from 1 to 100.",
                }
            ],
        }
        assert_valid(self, schema_validator, problem)

        for change in (
            {"status": 200},
            {"code": "database_error"},
            {"detail": "d" * 1025},
            {"debug": {"stack": "secret"}},
        ):
            invalid = {**problem, **change}
            with self.subTest(change=change):
                assert_invalid(self, schema_validator, invalid)


if __name__ == "__main__":
    unittest.main()
