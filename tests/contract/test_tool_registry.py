from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
PROFILE_PATH = ROOT / "profiles" / "tool-registry.v1.json"
SCHEMA_PATH = ROOT / "schemas" / "tool-registry.schema.json"
RESEARCH_PATH = (
    ROOT
    / "docs"
    / "research"
    / "2026-08-19"
    / "research-pack"
    / "data"
    / "tool-catalogue.json"
)
RESEARCH_SHA256 = "851f626bae4d63e8355ff9ca4021b56041ffa7e432d41f7f682c214151b5a8c3"
CANONICAL_NAMES = [
    "catalogue.search",
    "catalogue.describe",
    "selection.resolve",
    "data.query",
    "spatial.locate",
    "spatial.analyse",
    "statistics.compare",
    "route.plan",
    "map.render",
    "artefact.export",
    "evidence.inspect",
    "workflow.execute",
]
TARGET_ACTIVE = [
    "catalogue.search",
    "catalogue.describe",
    "selection.resolve",
    "data.query",
    "evidence.inspect",
]
CURRENT_APPLICATION_METADATA = {
    "T03": {
        "providerDependencies": [
            "reviewed public selection profile",
            "public-read policy",
            "public evidence contract",
        ],
        "costPerformance": (
            "Low; deterministic closed constraints and one reviewed selection profile"
        ),
        "controlledErrors": [
            "INVALID_REQUEST",
            "AMBIGUOUS_SELECTION",
            "MISSING_DIMENSION",
            "CONTRADICTORY_CONSTRAINTS",
            "NO_COMPATIBLE_PROVIDER",
            "POLICY_DENIED",
            "EVIDENCE_UNAVAILABLE",
        ],
        "fallbackBehaviour": "Return required choices and no executable plan.",
        "fallbackState": "implemented",
    },
    "T04": {
        "providerDependencies": [
            "explicitly injected ONS Data API adapter",
            "public-read policy",
            "durable public evidence ledger",
            "receipt-only idempotency reconciliation index",
        ],
        "costPerformance": (
            "Bounded to one observation, two provider attempts and a 20 second adapter ceiling"
        ),
        "controlledErrors": [
            "INVALID_REQUEST",
            "QUERY_CANCELLED",
            "QUERY_DEADLINE_EXCEEDED",
            "POLICY_DENIED",
            "PROVIDER_SUSPENDED",
            "PROVIDER_RATE_LIMITED",
            "PROVIDER_TIMEOUT",
            "PROVIDER_UNAVAILABLE",
            "PROVIDER_CONTRACT_FAILED",
            "EVIDENCE_UNAVAILABLE",
            "IDEMPOTENCY_PENDING",
            "IDEMPOTENCY_COMPLETED",
            "IDEMPOTENCY_CONFLICT",
        ],
        "fallbackBehaviour": (
            "Fail closed; no result cache, alternate provider or result fallback is permitted."
        ),
        "fallbackState": "not-implemented",
    },
    "T11": {
        "providerDependencies": [
            "durable public evidence ledger",
            "receipt-only idempotency reconciliation index",
        ],
        "costPerformance": "Low",
        "controlledErrors": [
            "INVALID_REQUEST",
            "EVIDENCE_NOT_FOUND",
            "EVIDENCE_UNAVAILABLE",
        ],
        "fallbackBehaviour": (
            "Fail closed; no alternate receipt, result replay or challenge route is "
            "implemented."
        ),
        "fallbackState": "not-implemented",
    },
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


class ToolRegistryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = load_json(PROFILE_PATH)
        cls.schema = load_json(SCHEMA_PATH)
        cls.validator = Draft202012Validator(cls.schema)
        cls.research = load_json(RESEARCH_PATH)

    def assert_invalid(self, value: Any) -> None:
        self.assertTrue(list(self.validator.iter_errors(value)))

    def test_profile_validates_as_closed_v1_contract(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        errors = sorted(
            self.validator.iter_errors(self.profile),
            key=lambda error: list(error.absolute_path),
        )
        self.assertEqual(
            errors,
            [],
            "; ".join(
                f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
                for error in errors
            ),
        )
        self.assertEqual(self.profile["canonicalOrder"], CANONICAL_NAMES)
        self.assertEqual(
            [tool["id"] for tool in self.profile["tools"]],
            [f"T{index:02d}" for index in range(1, 13)],
        )
        self.assertEqual(
            [tool["name"] for tool in self.profile["tools"]],
            CANONICAL_NAMES,
        )

    def test_research_provenance_and_current_fields_are_exact(self) -> None:
        digest = hashlib.sha256(RESEARCH_PATH.read_bytes()).hexdigest()
        self.assertEqual(digest, RESEARCH_SHA256)
        self.assertEqual(self.profile["source"]["research"]["sha256"], digest)
        self.assertTrue(self.profile["source"]["research"]["immutable"])

        for index, (profile, research) in enumerate(
            zip(self.profile["tools"], self.research["tools"], strict=True)
        ):
            with self.subTest(tool=profile["name"]):
                self.assertEqual(profile["id"], research["id"])
                self.assertEqual(profile["name"], research["name"])
                self.assertEqual(profile["namespace"], research["namespace"])
                self.assertEqual(profile["purpose"], research["purpose"])
                self.assertEqual(profile["readOnly"], research["read_only"])
                self.assertEqual(profile["mutating"], research["mutating"])
                current_metadata = CURRENT_APPLICATION_METADATA.get(profile["id"])
                if current_metadata is None:
                    self.assertEqual(
                        profile["support"]["providerDependencies"],
                        research["provider_dependencies"],
                    )
                    self.assertEqual(profile["costPerformance"], research["cost_performance"])
                    self.assertEqual(profile["controlledErrors"], research["error_codes"])
                    self.assertEqual(
                        profile["fallback"]["behaviour"], research["fallback_behaviour"]
                    )
                else:
                    self.assertEqual(
                        profile["support"]["providerDependencies"],
                        current_metadata["providerDependencies"],
                    )
                    self.assertEqual(
                        profile["costPerformance"], current_metadata["costPerformance"]
                    )
                    self.assertEqual(
                        profile["controlledErrors"], current_metadata["controlledErrors"]
                    )
                    self.assertEqual(
                        profile["fallback"]["behaviour"],
                        current_metadata["fallbackBehaviour"],
                    )
                    self.assertEqual(
                        profile["fallback"]["state"],
                        current_metadata["fallbackState"],
                    )
                self.assertEqual(profile["accessTiers"], research["access_tiers"])
                self.assertEqual(
                    profile["policyAttributes"],
                    research["policy_relevant_attributes"],
                )
                self.assertEqual(
                    profile["provenance"]["requiredFields"],
                    research["provenance_fields"],
                )
                self.assertEqual(profile["threats"]["risks"], research["risks"])
                self.assertEqual(
                    profile["cursor"]["researchStatement"],
                    research["pagination_or_artefact"],
                )
                pointer = f"/tools/{index}"
                self.assertEqual(profile["source"]["pointer"], pointer)
                self.assertEqual(
                    profile["source"]["inputSchemaPointer"],
                    f"{pointer}/input_schema",
                )
                self.assertEqual(
                    profile["source"]["outputSchemaPointer"],
                    f"{pointer}/output_schema",
                )

    def test_current_and_target_states_are_distinct_and_honest(self) -> None:
        profiles = {tool["name"]: tool for tool in self.profile["tools"]}
        implemented = [
            name
            for name in CANONICAL_NAMES
            if profiles[name]["current"]["implementationState"] == "implemented"
        ]
        target_active = [
            name
            for name in CANONICAL_NAMES
            if profiles[name]["v02Target"]["lifecycleState"] == "active"
        ]
        self.assertEqual(
            implemented,
            TARGET_ACTIVE,
        )
        self.assertEqual(target_active, TARGET_ACTIVE)
        for name in ["selection.resolve", "data.query"]:
            self.assertEqual(profiles[name]["current"]["implementationState"], "implemented")
            self.assertEqual(profiles[name]["current"]["lifecycleState"], "suspended")
        self.assertTrue(profiles["workflow.execute"]["mutating"])
        self.assertFalse(profiles["workflow.execute"]["readOnly"])
        self.assertEqual(profiles["workflow.execute"]["releaseTarget"], "v0.3.0")

        for profile in self.profile["tools"]:
            with self.subTest(tool=profile["name"]):
                self.assertFalse(profile["current"]["discoveryEligible"])
                self.assertFalse(any(profile["current"]["activationGates"].values()))
                self.assertFalse(profile["v02Target"]["runtimeAuthority"])
        self.assertFalse(self.profile["runtimeAuthority"]["productionRegistration"])
        self.assertFalse(self.profile["runtimeAuthority"]["registryCanActivate"])
        self.assertFalse(self.profile["runtimeAuthority"]["environmentOverride"])

    def test_runtime_schema_references_are_accepted_files_or_explicitly_missing(self) -> None:
        for profile in self.profile["tools"]:
            for direction, reference in profile["runtimeSchemas"].items():
                with self.subTest(tool=profile["name"], direction=direction):
                    if reference["state"] == "missing":
                        self.assertIsNone(reference["ref"])
                        continue
                    relative = reference["ref"]
                    self.assertTrue(relative.startswith("schemas/"))
                    self.assertNotIn("docs/research", relative)
                    schema_path = ROOT / relative
                    self.assertTrue(schema_path.is_file())
                    runtime_schema = load_json(schema_path)
                    self.assertTrue(runtime_schema["$id"].startswith("urn:gis-ai-go:schema:"))

    def test_schema_rejects_duplicates_reordering_and_unknown_fields(self) -> None:
        duplicate = copy.deepcopy(self.profile)
        duplicate["tools"][1]["id"] = duplicate["tools"][0]["id"]
        self.assert_invalid(duplicate)

        reordered = copy.deepcopy(self.profile)
        reordered["tools"][0], reordered["tools"][1] = (
            reordered["tools"][1],
            reordered["tools"][0],
        )
        self.assert_invalid(reordered)

        unknown_root = copy.deepcopy(self.profile)
        unknown_root["environmentOverride"] = True
        self.assert_invalid(unknown_root)

        unknown_nested = copy.deepcopy(self.profile)
        unknown_nested["tools"][0]["current"]["advertise"] = True
        self.assert_invalid(unknown_nested)

    def test_registry_does_not_modify_gateway_activation_or_read_environment(self) -> None:
        activation = (ROOT / "apps" / "mcp-gateway" / "src" / "activation.ts").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("@gis-ai-go/tool-registry", activation)
        self.assertIn("activeTools: Object.freeze([])", activation)
        self.assertIn("activeApiOperations: Object.freeze([])", activation)

        runtime_source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((ROOT / "packages" / "tool-registry" / "src").glob("*.ts"))
        )
        self.assertNotIn("process.env", runtime_source)


if __name__ == "__main__":
    unittest.main()
