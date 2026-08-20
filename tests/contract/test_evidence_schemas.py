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

SCHEMA_IDS = {
    "public-authority-context.schema.json": (
        "urn:gis-ai-go:schema:public-authority-context:v1"
    ),
    "public-policy.schema.json": "urn:gis-ai-go:schema:public-policy:v1",
    "public-policy-decision.schema.json": (
        "urn:gis-ai-go:schema:public-policy-decision:v1"
    ),
    "evidence-receipt.schema.json": "urn:gis-ai-go:schema:evidence-receipt:v1",
}

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


PUBLIC_POLICY = load_json(
    ROOT / "packages" / "policy-client" / "src" / "public-catalogue-v1.json"
)


def build_schema_registry() -> Registry:
    resources = []
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        schema = load_json(path)
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return Registry().with_resources(resources)


SCHEMA_REGISTRY = build_schema_registry()


def validator(name: str) -> Draft202012Validator:
    schema = load_json(SCHEMA_DIR / name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(
        schema,
        registry=SCHEMA_REGISTRY,
        format_checker=FormatChecker(),
    )


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


def assert_contract_objects_are_closed(
    test_case: unittest.TestCase,
    node: object,
    path: str = "$",
) -> None:
    if isinstance(node, dict):
        if node.get("type") == "object" and ".contains" not in path:
            test_case.assertIs(
                node.get("additionalProperties"),
                False,
                f"{path} must reject unknown properties",
            )
        for key, value in node.items():
            assert_contract_objects_are_closed(test_case, value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            assert_contract_objects_are_closed(test_case, value, f"{path}[{index}]")


def keys_in(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value).union(*(keys_in(item) for item in value.values()))
    if isinstance(value, list):
        return set().union(*(keys_in(item) for item in value))
    return set()


class EvidenceSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.authority_context = load_json(
            FIXTURE_DIR / "public-authority-context.example.json"
        )
        self.policy_decision = load_json(
            FIXTURE_DIR / "public-policy-decision.example.json"
        )
        self.receipt = load_json(FIXTURE_DIR / "evidence-receipt.example.json")

    def test_v1_schema_ids_are_stable_and_contract_objects_are_closed(self) -> None:
        for name, expected_id in SCHEMA_IDS.items():
            with self.subTest(schema=name):
                schema = load_json(SCHEMA_DIR / name)
                Draft202012Validator.check_schema(schema)
                self.assertEqual(expected_id, schema["$id"])
                assert_contract_objects_are_closed(self, schema)

    def test_anonymous_open_context_is_server_constructed_and_contains_no_identity(self) -> None:
        schema_validator = validator("public-authority-context.schema.json")
        assert_valid(self, schema_validator, self.authority_context)

        self.assertEqual("server", self.authority_context["construction"]["source"])
        self.assertEqual(
            "anonymous-open",
            self.authority_context["construction"]["profile"],
        )
        self.assertEqual("none", self.authority_context["access"]["authentication"])
        self.assertEqual(
            {"catalogue.search", "catalogue.describe"},
            set(self.authority_context["permitted_operations"]),
        )
        forbidden = {
            "actor",
            "subject",
            "user_id",
            "organisation",
            "role",
            "client",
            "device",
            "workload",
            "credential",
            "token",
        }
        self.assertTrue(forbidden.isdisjoint(keys_in(self.authority_context)))

        protected = copy.deepcopy(self.authority_context)
        protected["access"]["contains_protected_data"] = True
        assert_invalid(self, schema_validator, protected)

        identified = copy.deepcopy(self.authority_context)
        identified["actor"] = {"id": "unexpected"}
        assert_invalid(self, schema_validator, identified)

        incomplete = copy.deepcopy(self.authority_context)
        incomplete["permitted_operations"] = ["catalogue.search"]
        assert_invalid(self, schema_validator, incomplete)

    def test_compiled_public_policy_is_an_exact_allow_list_with_default_deny(self) -> None:
        schema_validator = validator("public-policy.schema.json")
        assert_valid(self, schema_validator, PUBLIC_POLICY)
        self.assertEqual("deny", PUBLIC_POLICY["default_effect"])
        self.assertEqual(
            {"catalogue.search", "catalogue.describe"},
            {rule["operation"] for rule in PUBLIC_POLICY["rules"]},
        )

        for mutation in (
            {"default_effect": "allow"},
            {"rules": PUBLIC_POLICY["rules"][:1]},
            {"rules": [PUBLIC_POLICY["rules"][0], PUBLIC_POLICY["rules"][0]]},
            {"unexpected": True},
        ):
            invalid = copy.deepcopy(PUBLIC_POLICY)
            invalid.update(mutation)
            with self.subTest(mutation=mutation):
                assert_invalid(self, schema_validator, invalid)

        wrong_effect = copy.deepcopy(PUBLIC_POLICY)
        wrong_effect["rules"][0]["effect"] = "allow"
        assert_invalid(self, schema_validator, wrong_effect)

    def test_public_policy_decision_supports_allow_and_default_deny_without_raw_input(self) -> None:
        schema_validator = validator("public-policy-decision.schema.json")
        assert_valid(self, schema_validator, self.policy_decision)
        self.assertEqual(PUBLIC_POLICY["policy_id"], self.policy_decision["policy_id"])
        self.assertEqual("rfc8785-jcs", self.policy_decision["canonicalisation"])
        self.assertEqual("deny", self.policy_decision["policy_default_effect"])

        denied = copy.deepcopy(self.policy_decision)
        denied["operation"] = "data.query"
        denied["effect"] = "deny"
        denied["reason_code"] = "operation-not-allowed"
        denied["obligations"] = []
        assert_valid(self, schema_validator, denied)

        denied_with_obligations = copy.deepcopy(denied)
        denied_with_obligations["obligations"] = ["not-persisted"]
        assert_invalid(self, schema_validator, denied_with_obligations)

        unsupported_allow = copy.deepcopy(self.policy_decision)
        unsupported_allow["operation"] = "data.query"
        assert_invalid(self, schema_validator, unsupported_allow)

        raw_input = copy.deepcopy(self.policy_decision)
        raw_input["raw_query"] = "unnecessary input"
        assert_invalid(self, schema_validator, raw_input)

    def test_inline_receipt_is_self_contained_not_persisted_and_not_attested(self) -> None:
        schema_validator = validator("evidence-receipt.schema.json")
        assert_valid(self, schema_validator, self.receipt)

        self.assertEqual(self.authority_context, self.receipt["authority_context"])
        self.assertEqual(self.policy_decision, self.receipt["policy_decision"])
        self.assertEqual(
            {
                "delivery": "inline-only",
                "persistence": "not-persisted",
                "attestation": "not-attested",
            },
            self.receipt["evidence_handling"],
        )
        self.assertEqual(
            sorted(
                self.receipt["licence_obligations"],
                key=lambda obligation: obligation["record_id"],
            ),
            self.receipt["licence_obligations"],
        )
        forbidden = {
            "uri",
            "store_uri",
            "receipt_uri",
            "raw_query",
            "query",
            "machine_path",
            "prompt",
            "token",
            "credential",
        }
        self.assertTrue(forbidden.isdisjoint(keys_in(self.receipt)))

        for handling_key, unsupported_value in (
            ("delivery", "reference"),
            ("persistence", "persisted"),
            ("attestation", "attested"),
        ):
            invalid = copy.deepcopy(self.receipt)
            invalid["evidence_handling"][handling_key] = unsupported_value
            with self.subTest(handling_key=handling_key):
                assert_invalid(self, schema_validator, invalid)

        external_reference = copy.deepcopy(self.receipt)
        external_reference["store_uri"] = "urn:unexpected:evidence"
        assert_invalid(self, schema_validator, external_reference)

        raw_input = copy.deepcopy(self.receipt)
        raw_input["operation"]["raw_query"] = "public boundary"
        assert_invalid(self, schema_validator, raw_input)

        incomplete_rights = copy.deepcopy(self.receipt)
        incomplete_rights["licence_obligations"][0].pop("attribution")
        assert_invalid(self, schema_validator, incomplete_rights)

        duplicate_rights = copy.deepcopy(self.receipt)
        duplicate_rights["licence_obligations"].append(
            copy.deepcopy(duplicate_rights["licence_obligations"][0])
        )
        assert_invalid(self, schema_validator, duplicate_rights)

        unbounded_result = copy.deepcopy(self.receipt)
        unbounded_result["result"]["returned_record_count"] = 101
        assert_invalid(self, schema_validator, unbounded_result)

        incomplete_pipeline = copy.deepcopy(self.receipt)
        incomplete_pipeline["transformations"].pop()
        assert_invalid(self, schema_validator, incomplete_pipeline)

        reordered_pipeline = copy.deepcopy(self.receipt)
        reordered_pipeline["transformations"][0:2] = reversed(
            reordered_pipeline["transformations"][0:2]
        )
        assert_invalid(self, schema_validator, reordered_pipeline)

        denied_success = copy.deepcopy(self.receipt)
        denied_success["policy_decision"]["effect"] = "deny"
        denied_success["policy_decision"]["reason_code"] = "operation-not-allowed"
        denied_success["policy_decision"]["obligations"] = []
        assert_invalid(self, schema_validator, denied_success)

        mismatched_operation = copy.deepcopy(self.receipt)
        mismatched_operation["policy_decision"]["operation"] = "catalogue.describe"
        assert_invalid(self, schema_validator, mismatched_operation)

    def test_content_id_and_digest_domains_are_explicit_and_distinct(self) -> None:
        self.assertTrue(
            self.authority_context["context_id"].startswith(
                "gis-ai-go:public-authority-context:sha256:"
            )
        )
        self.assertTrue(
            PUBLIC_POLICY["policy_id"].startswith("gis-ai-go:public-policy:sha256:")
        )
        self.assertTrue(
            self.policy_decision["decision_id"].startswith(
                "gis-ai-go:public-policy-decision:sha256:"
            )
        )
        self.assertTrue(
            self.receipt["receipt_id"].startswith(
                "gis-ai-go:evidence-receipt:sha256:"
            )
        )
        self.assertNotEqual(
            self.receipt["operation"]["normalised_parameters"]["domain"],
            self.receipt["result"]["domain"],
        )


if __name__ == "__main__":
    unittest.main()
