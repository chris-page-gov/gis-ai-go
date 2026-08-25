from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT / "schemas" / "qual-206-claude-composite-stdio-readiness-v2.schema.json"
)
EVIDENCE_PATH = (
    ROOT
    / "tests"
    / "interoperability"
    / "evidence"
    / "claude-code-2.1.245-modern-stdio-readiness-2026-08-25.json"
)
RUNBOOK_PATH = ROOT / "docs" / "operations" / "QUAL-206_CLAUDE_COMPOSITE_OBSERVATION.md"
EVIDENCE_README_PATH = ROOT / "tests" / "interoperability" / "evidence" / "README.md"
SOURCE_COMMIT = "e905c632724ecc9d13b13452fee37328e75cc2a4"
SOURCE_TREE = "c611ba2d86dcefb541814e5cd4ab3345dd8745b6"
SCHEMA_SHA256 = "729e8a6d5a3a2799a601a6d86588aaebef76fc6a053de254fdf2cacb77ec49aa"
EVIDENCE_SHA256 = "a588d5cfe211f0a7f571b736cb86e8ef0105999089d59e81239364fe4b804b23"
HISTORICAL_ARTIFACTS = {
    "schemas/qual-206-claude-composite-stdio-readiness.schema.json": (
        "0999efbed9c9b4267370cf9ee0b66dfe9c36824b2b6ab9d76c3af1f87bfed930"
    ),
    (
        "tests/interoperability/evidence/"
        "claude-code-2.1.241-modern-stdio-readiness-2026-08-25.json"
    ): "eecb01a605d678a0fc2a1603e6b3e3be340890b3c9d9c9b5f1a1eb6070043639",
}
EXPECTED_RUNTIME_MATERIALS = {
    "scripts/qual_206_claude_stdio_observer.mjs": (
        "86f07637913c66aeb3df62fb3a8a44aee8c47b096b82a4cf914c4cf5f44d87ae"
    ),
    "scripts/qual_206_exact_five_event_collector.mjs": (
        "be45d157c3daed81267e03be34b02eeb8fb006d8889f436ee531e315fba6bdc0"
    ),
    "tests/interoperability/fixtures/qual_206_strict_modern_event_server.mjs": (
        "04e274f89dc6abbb97b445e12a38a45588bd1273dbd318c0bdadb9cac6d97a98"
    ),
    "tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs": (
        "f34757b6c7c555adb37a2d5fffbb164a264a689fe603e12f25703fea8d46eafe"
    ),
    "scripts/verify_qual_206_claude_composite_observation.py": (
        "79fd56d43ae8b644089e205a2d8fb3b0e448232a266eb00c47693f844d7fe90d"
    ),
    "schemas/qual-206-claude-composite-host-event-v1.schema.json": (
        "3fa5d43594309ce6674da8f596ef7b55405f82a38db85458a1bbfe5b02af4dc4"
    ),
    "schemas/qual-206-claude-composite-host-event-capture-v1.schema.json": (
        "9e8df35db3910104019d2319643a37de0dc28d6d239c8532e28c08668d162082"
    ),
}
BOUNDARY = (
    "Accepted protected-main Claude Code 2.1.245 strict-modern STDIO "
    "transport-readiness evidence only. In v2 automatic negotiation, Claude "
    "completed a contract-valid MCP 2026-07-28 server/discover probe and a "
    "separate tools/list session. No model task, tool call, resource read, "
    "exact-five operation journey, provider, remote HTTP host, registration, "
    "activation, deployment or release was exercised. Capability remains "
    "unscored, and the independent-host capability and exact-five source-binding "
    "gates remain incomplete."
)
PUBLIC_EVIDENCE_FORBIDDEN = re.compile(
    r"(?:"
    r"/Users/|/home/|/Volumes/|/private/tmp/|file://|"
    r"[A-Za-z]:\\\\Users\\\\|"
    r"\bsk-[A-Za-z0-9_-]{8,}|\bgh[opusr]_[A-Za-z0-9]{8,}|"
    r"\bxox[baprs]-[A-Za-z0-9-]{8,}|\bAKIA[0-9A-Z]{16}|"
    r"\bBearer\s+[A-Za-z0-9._~-]+|"
    r"OPENAI_API_KEY|CODEX_API_KEY|ANTHROPIC_API_KEY|ANTHROPIC_AUTH_TOKEN|"
    r"CLAUDE_CODE_OAUTH_TOKEN|"
    r"https?://(?:chatgpt\.com/c/|claude\.ai/chat/)|"
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-"
    r"[0-9a-f]{12}\b"
    r")",
    re.IGNORECASE,
)
FORBIDDEN_FIELD_NAMES = {
    "arguments",
    "command_sha256",
    "environment",
    "headers",
    "immediate_parent",
    "log_path",
    "machine_id",
    "pid",
    "profile_path",
    "raw_command",
    "raw_result",
    "request_id_sha256",
    "run_id",
    "session_id",
    "user_id",
}


def reject_non_standard_number(value: str) -> None:
    raise ValueError(f"Non-standard JSON number: {value}")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=reject_non_standard_number,
    )
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain one JSON object")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_output(*arguments: str) -> bytes:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise AssertionError(f"git {' '.join(arguments)} failed: {message}")
    return result.stdout


def git_blob(commit: str, path: str) -> bytes:
    return git_output("show", f"{commit}:{path}")


def nested_field_names(node: object) -> set[str]:
    names: set[str] = set()
    if isinstance(node, dict):
        names.update(node)
        for value in node.values():
            names.update(nested_field_names(value))
    elif isinstance(node, list):
        for value in node:
            names.update(nested_field_names(value))
    return names


def assert_contract_objects_are_closed(
    test_case: unittest.TestCase,
    node: object,
    path: str = "$",
) -> None:
    if isinstance(node, dict):
        if node.get("type") == "object":
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


class Qual206ClaudeCompositeStdioReadinessV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        cls.document = load_json(EVIDENCE_PATH)
        cls.validator = Draft202012Validator(
            cls.schema,
            format_checker=FormatChecker(),
        )

    def assert_invalid(self, value: object) -> None:
        self.assertTrue(list(self.validator.iter_errors(value)))

    def test_closed_schema_accepts_exact_canonical_projection(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        assert_contract_objects_are_closed(self, self.schema)
        errors = sorted(
            self.validator.iter_errors(self.document),
            key=lambda error: list(error.absolute_path),
        )
        self.assertEqual(
            [],
            [
                f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: "
                f"{error.message}"
                for error in errors
            ],
        )
        expected_bytes = (
            json.dumps(self.document, ensure_ascii=False, indent=2) + "\n"
        ).encode()
        self.assertEqual(EVIDENCE_PATH.read_bytes(), expected_bytes)
        self.assertEqual(sha256_bytes(SCHEMA_PATH.read_bytes()), SCHEMA_SHA256)
        self.assertEqual(sha256_bytes(EVIDENCE_PATH.read_bytes()), EVIDENCE_SHA256)
        self.assertEqual(
            self.document["schema_contract"],
            {
                "path": (
                    "schemas/qual-206-claude-composite-stdio-readiness-v2.schema.json"
                ),
                "sha256": SCHEMA_SHA256,
            },
        )

    def test_projection_binds_exact_protected_main_source_and_runtime(self) -> None:
        source = self.document["source"]
        self.assertEqual(source["commit"], SOURCE_COMMIT)
        self.assertEqual(source["tree"], SOURCE_TREE)
        self.assertEqual(
            git_output("rev-parse", f"{SOURCE_COMMIT}^{{tree}}").decode().strip(),
            SOURCE_TREE,
        )
        self.assertEqual(
            git_output("merge-base", "--is-ancestor", SOURCE_COMMIT, "HEAD"),
            b"",
        )
        actual_materials = {
            item["path"]: item["sha256"]
            for item in self.document["runtime_materials"]
        }
        self.assertEqual(actual_materials, EXPECTED_RUNTIME_MATERIALS)
        for path, expected_digest in EXPECTED_RUNTIME_MATERIALS.items():
            with self.subTest(path=path):
                self.assertEqual(
                    sha256_bytes(git_blob(SOURCE_COMMIT, path)),
                    expected_digest,
                )
        assurance = source["assurance"]
        self.assertTrue(all(
            value is True
            for key, value in assurance.items()
            if key not in {"ci_run_id", "codeql_run_id"}
        ))

    def test_two_sessions_prove_transport_readiness_only(self) -> None:
        probe, modern = self.document["sessions"]
        self.assertEqual(
            (probe["profile"], probe["request"]["method"], probe["closure_stimulus"]),
            ("negotiation-probe", "server/discover", "sigterm"),
        )
        self.assertEqual(
            (modern["profile"], modern["request"]["method"], modern["closure_stimulus"]),
            ("modern-session", "tools/list", "sigint"),
        )
        for session in (probe, modern):
            self.assertEqual(session["request"]["protocol_claim"], "2026-07-28")
            self.assertEqual(session["response"]["outcome"], "success")
            self.assertTrue(session["response"]["contract_valid"])
            self.assertEqual(session["request_count"], session["response_count"])
            self.assertEqual(session["request_count"], 1)
            for key in (
                "pending_request_count",
                "anomaly_count",
                "stderr_bytes",
                "stderr_event_count",
            ):
                self.assertEqual(session[key], 0)
            self.assertTrue(session["temporary_state_removed"])
            self.assertTrue(session["runtime_materials_stable"])
            self.assertTrue(session["source_checkout_stable"])
            self.assertEqual(set(session["audit_counters"].values()), {0})
            self.assertFalse(
                session["retained_private_evidence"]["raw_content_published"]
            )
        self.assertFalse(self.document["protocol_target"]["legacy_initialize_observed"])
        self.assertEqual(self.document["host"]["transport_readiness"], "ready")
        self.assertEqual(self.document["host"]["capability"], "unscored")

    def test_isolation_verification_and_limitations_remain_fail_closed(self) -> None:
        verification = self.document["verification"]
        self.assertEqual(verification["result"], "passed")
        self.assertEqual(verification["session_count"], 2)
        self.assertEqual(verification["remaining_observer_processes"], 0)
        self.assertEqual(verification["remaining_fixture_processes"], 0)
        self.assertTrue(verification["private_archive_owner_only"])
        self.assertTrue(verification["public_projection_path_free"])

        isolation = self.document["isolation"]
        self.assertTrue(isolation["disposable_profile"])
        self.assertFalse(isolation["normal_profile_used"])
        self.assertEqual(isolation["recognised_parent_credential_variables_present"], 0)
        self.assertEqual(isolation["mcp_child_environment"], "closed-credential-free")
        self.assertFalse(isolation["raw_host_logs_published"])
        self.assertFalse(isolation["private_client_output"]["published"])

        limitations = self.document["limitations"]
        self.assertTrue(limitations["strict_modern_transport_ready"])
        self.assertFalse(any(
            value
            for key, value in limitations.items()
            if key != "strict_modern_transport_ready"
        ))
        self.assertEqual(self.document["boundary"], BOUNDARY)

    def test_historical_observation_remains_byte_exact_and_separate(self) -> None:
        lineage = self.document["historical_lineage"]
        self.assertEqual(
            lineage["relationship"],
            "preserved-prior-2.1.241-readiness-result-not-relabelled",
        )
        self.assertEqual(
            {
                item["path"]: item["sha256"]
                for item in lineage["preserved_artifacts"]
            },
            HISTORICAL_ARTIFACTS,
        )
        for path, expected_digest in HISTORICAL_ARTIFACTS.items():
            with self.subTest(path=path):
                self.assertEqual(sha256_bytes((ROOT / path).read_bytes()), expected_digest)

    def test_public_projection_is_path_free_and_minimised(self) -> None:
        rendered = EVIDENCE_PATH.read_text(encoding="utf-8")
        self.assertIsNone(PUBLIC_EVIDENCE_FORBIDDEN.search(rendered))
        self.assertFalse(nested_field_names(self.document) & FORBIDDEN_FIELD_NAMES)
        self.assertNotIn('"raw_content":', rendered)
        self.assertNotIn('"source_checkout":', rendered)
        self.assertNotIn('"observer_runtime":', rendered)
        self.assertNotIn('"credential_environment":', rendered)

    def test_schema_rejects_claim_widening_and_projection_tampering(self) -> None:
        cases: list[tuple[str, dict[str, Any]]] = []

        capability = copy.deepcopy(self.document)
        capability["host"]["capability"] = "ready"
        cases.append(("capability", capability))

        provider = copy.deepcopy(self.document)
        provider["limitations"]["live_provider_called"] = True
        cases.append(("provider", provider))

        raw = copy.deepcopy(self.document)
        raw["sessions"][0]["retained_private_evidence"]["raw_content_published"] = True
        cases.append(("raw", raw))

        method = copy.deepcopy(self.document)
        method["sessions"][1]["request"]["method"] = "initialize"
        cases.append(("method", method))

        extra = copy.deepcopy(self.document)
        extra["session_id"] = "not-allowed"
        cases.append(("extra", extra))

        for label, value in cases:
            with self.subTest(label=label):
                self.assert_invalid(value)

    def test_runbook_and_evidence_readme_state_the_accepted_boundary(self) -> None:
        filename = EVIDENCE_PATH.name
        for path in (RUNBOOK_PATH, EVIDENCE_README_PATH):
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertIn(filename, text)
                self.assertIn("capability", text.casefold())
                self.assertIn("2026-07-28", text)


if __name__ == "__main__":
    unittest.main()
