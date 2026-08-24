from __future__ import annotations

import copy
import hashlib
import json
import math
import re
import subprocess
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schemas" / "qual-206-claude-code-stdio-observation.schema.json"
EVIDENCE_PATH = (
    ROOT
    / "tests"
    / "interoperability"
    / "evidence"
    / "claude-code-2.1.241-stdio-observation-2026-08-24.json"
)
RUNBOOK_PATH = ROOT / "docs" / "operations" / "QUAL-206_INTEROPERABILITY.md"
HISTORICAL_SCHEMA_PATH = ROOT / "schemas" / "qual-206-legacy-stdio-readiness.schema.json"
HISTORICAL_EVIDENCE_PATH = (
    ROOT
    / "tests"
    / "interoperability"
    / "evidence"
    / "claude-code-legacy-stdio-readiness-2026-08-23.json"
)
SOURCE_COMMIT = "dda0eb9f776e64bcd45069e77b4acbcd4d495e01"
SOURCE_TREE = "258e6f3b3f62abccf04795e015f6961e06740fcf"
SCHEMA_SHA256 = "78b9a8071a6954028576f397c98dd0fc4b87dddbaf72654f6459407b280e2a9b"
EVIDENCE_SHA256 = "d2cd72b7f16a0bafd8a7190b87b14f150b7fa975f6d70f5e779eb9ddf5f92478"
HISTORICAL_SCHEMA_SHA256 = (
    "5ce73d3d45c762112ac932407000b4379d07d92a9e54808227cd72e6050fd02a"
)
HISTORICAL_EVIDENCE_SHA256 = (
    "a3d40e2013095baf977bad336366c0fb429a05b6a5a267c3e069595e4cdb1a6b"
)
LOCKFILE_SHA256 = "640208aa66d26241514025b33dbde50bc14be7bbd33641eec9977e87699bb4ec"
EXPECTED_RUNTIME_FILES = [
    (
        "apps/mcp-gateway/src/mcp-server.ts",
        "e2c5cec027f3049d0a501b885a0ab6336d7e6059690df54ac7b257945807b454",
    ),
    (
        "apps/mcp-gateway/src/mcp-stdio.ts",
        "5e8d87020d1efe34b2b83940f60d2df5926f466c12473fffc156463c9a6cef30",
    ),
    (
        "scripts/qual_206_conformance_server.mjs",
        "aba0f4415bc9f94443be8b79eee06b03bdd275ca9854218dee30102c20a6778f",
    ),
    (
        "scripts/qual_206_legacy_conformance_server.mjs",
        "bf87bec24357d5fd6d419bd8b4374642ab46a2f3dfa6d9baebde46f7498edb9c",
    ),
    (
        "scripts/qual_206_telemetry_proxy.mjs",
        "3800e4458932ee1324ad03d64007f23f76f49682a6eabdc191ecf6eaccb501d5",
    ),
]
EXPECTED_COMPILED_ENTRYPOINTS = [
    (
        "apps/mcp-gateway/dist/src/mcp-server.js",
        "71fdde3b45363d366b62e7c4219c2cc77efbfbfe9d9e5d110f656e76ee9d2ab1",
    ),
    (
        "apps/mcp-gateway/dist/src/mcp-stdio.js",
        "17a04b0b1f0a5549157c8e07119ac1d7a895b86d9a73312aaaa2561fd1e092e3",
    ),
]
BOUNDARY = (
    "Accepted protected-main Claude Code protocol observation only. Claude Code "
    "2.1.241 offered MCP 2025-11-25, so the strict 2026-07-28 STDIO surface "
    "correctly rejected it while the constructor-only fallback completed "
    "initialisation and tools/list. No model, tool call, resource read, exact-five "
    "production assembly, provider, remote HTTP host, registration, activation, "
    "deployment or release was exercised. Capability and the independent-host gate "
    "remain unscored and incomplete."
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
    "command_sha256",
    "environment",
    "headers",
    "log_path",
    "profile_path",
    "prompt",
    "raw_command",
    "raw_result",
    "session_id",
    "session_id_sha256",
}


def reject_non_standard_number(value: str) -> None:
    raise ValueError(f"Non-standard JSON number: {value}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=reject_non_standard_number,
    )


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


class Qual206ClaudeCodeStdioObservationTests(unittest.TestCase):
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

    def test_closed_schema_accepts_exact_canonical_evidence(self) -> None:
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
                "path": "schemas/qual-206-claude-code-stdio-observation.schema.json",
                "sha256": SCHEMA_SHA256,
            },
        )

    def test_record_binds_exact_protected_main_source_materials(self) -> None:
        source = self.document["source"]
        self.assertEqual(source["commit"], SOURCE_COMMIT)
        self.assertEqual(source["tree"], SOURCE_TREE)
        self.assertEqual(
            git_output("rev-parse", f"{SOURCE_COMMIT}^{{tree}}").decode().strip(),
            SOURCE_TREE,
        )
        runtime = [(item["path"], item["sha256"]) for item in source["runtime_files"]]
        self.assertEqual(runtime, EXPECTED_RUNTIME_FILES)
        for path, expected_digest in EXPECTED_RUNTIME_FILES:
            with self.subTest(path=path):
                self.assertEqual(sha256_bytes(git_blob(SOURCE_COMMIT, path)), expected_digest)
        build = source["build"]
        self.assertEqual(build["lockfile"]["sha256"], LOCKFILE_SHA256)
        self.assertEqual(
            sha256_bytes(git_blob(SOURCE_COMMIT, "pnpm-lock.yaml")),
            LOCKFILE_SHA256,
        )
        self.assertEqual(
            [
                (item["path"], item["sha256"])
                for item in build["compiled_entrypoints"]
            ],
            EXPECTED_COMPILED_ENTRYPOINTS,
        )
        self.assertTrue(build["preflight_passed"])
        self.assertTrue(build["loopback_permission_required"])

    def test_historical_observation_remains_byte_exact_and_separate(self) -> None:
        self.assertEqual(
            sha256_bytes(HISTORICAL_SCHEMA_PATH.read_bytes()),
            HISTORICAL_SCHEMA_SHA256,
        )
        self.assertEqual(
            sha256_bytes(HISTORICAL_EVIDENCE_PATH.read_bytes()),
            HISTORICAL_EVIDENCE_SHA256,
        )
        self.assertEqual(
            self.document["historical_lineage"],
            {
                "schema_sha256": HISTORICAL_SCHEMA_SHA256,
                "evidence_sha256": HISTORICAL_EVIDENCE_SHA256,
                "relationship": "preserved-separate-not-superseded",
            },
        )

    def test_attempts_distinguish_modern_failure_from_fallback_readiness(self) -> None:
        modern, fallback = self.document["attempts"]
        self.assertEqual((modern["kind"], fallback["kind"]), (
            "strict-modern",
            "constructor-only-fallback",
        ))
        self.assertEqual(modern["client_requested_protocol"], "2025-11-25")
        self.assertEqual(fallback["client_requested_protocol"], "2025-11-25")
        self.assertEqual(modern["server_protocol"], "2026-07-28")
        self.assertEqual(fallback["negotiated_protocol"], "2025-06-18")
        self.assertEqual((modern["transport_readiness"], fallback["transport_readiness"]), (
            "not-ready",
            "ready",
        ))
        self.assertEqual((modern["capability"], fallback["capability"]), (
            "unscored",
            "unscored",
        ))
        self.assertEqual(modern["error_code"], -32022)
        self.assertFalse(modern["initialize_success"])
        self.assertFalse(modern["tools_list_success"])
        self.assertTrue(fallback["initialize_success"])
        self.assertTrue(fallback["tools_list_success"])
        self.assertEqual(
            modern["telemetry"]["initialize_request"],
            fallback["telemetry"]["initialize_request"],
        )
        historical = load_json(HISTORICAL_EVIDENCE_PATH)["telemetry"]
        self.assertEqual(
            fallback["telemetry"]["initialize_response"]["frame_sha256"],
            historical["initialize_response"]["frame_sha256"],
        )
        self.assertEqual(
            fallback["telemetry"]["tools_list_response"]["frame_sha256"],
            historical["tools_list_response"]["frame_sha256"],
        )
        self.assertNotIn("tools_list_request", modern["telemetry"])
        self.assertNotIn("tools_list_response", modern["telemetry"])

        for attempt in (modern, fallback):
            telemetry = attempt["telemetry"]
            self.assertEqual(
                telemetry["event_count"],
                sum(telemetry["event_counts"].values()),
            )
            for response_name in (
                "initialize_response",
                *(("tools_list_response",) if attempt is fallback else ()),
            ):
                duration = telemetry[response_name]["duration_ms"]
                self.assertTrue(math.isfinite(duration))
                self.assertGreaterEqual(duration, 0)
            for count_name in (
                "invalid_frame_count",
                "non_json_frame_count",
                "truncated_frame_count",
                "server_stderr_event_count",
                "pending_request_count",
            ):
                self.assertEqual(telemetry[count_name], 0)
            self.assertEqual(telemetry["exit_code"], 0)
            self.assertFalse(telemetry["raw_content_published"])
            self.assertFalse(attempt["tool_call_observed"])
            self.assertFalse(attempt["resource_read_observed"])

        limitations = self.document["limitations"]
        self.assertFalse(limitations["modern_transport_ready"])
        self.assertTrue(limitations["legacy_transport_ready"])
        self.assertFalse(limitations["capability_result_claimed"])
        self.assertFalse(limitations["independent_host_gate_completed"])
        self.assertFalse(limitations["exact_five_assembly_exercised"])
        self.assertFalse(limitations["model_task_requested"])
        self.assertFalse(limitations["live_provider_called"])
        self.assertFalse(limitations["remote_http_observed"])
        self.assertFalse(limitations["activation_or_release_claimed"])
        self.assertEqual(self.document["boundary"], BOUNDARY)

        self.assertEqual(
            self.document["isolation"],
            {
                "temporary_profiles": 2,
                "profile_root_mode": "0700",
                "backup_directory_mode": "0755",
                "primary_configuration_mode": "0600",
                "generated_backup_modes": ["0644", "0600"],
                "normal_profile_used": False,
                "credential_variables_removed": 5,
                "mcp_child_environment_allowlisted": True,
                "retained_private_logs": 2,
                "credential_value_pattern_matches": 0,
                "remaining_isolated_processes_after_cleanup": 0,
                "raw_host_logs_published": False,
            },
        )

    def test_protocol_target_is_the_source_ledger_release(self) -> None:
        source_ledger = load_json(ROOT / "docs" / "source-ledger" / "sources.json")
        sources = source_ledger["sources"]
        source = next(item for item in sources if item["id"] == "S-MCP-SPEC")
        self.assertEqual(source["published"], "2026-07-28")
        self.assertEqual(source["maturity"], "final-general-availability")
        self.assertEqual(
            self.document["protocol_target"],
            {
                "version": "2026-07-28",
                "status_at_observation": "latest-published",
                "source_id": "S-MCP-SPEC",
            },
        )

    def test_public_record_contains_no_path_secret_session_or_raw_payload(self) -> None:
        public_text = EVIDENCE_PATH.read_text(encoding="utf-8")
        self.assertIsNone(PUBLIC_EVIDENCE_FORBIDDEN.search(public_text))
        self.assertTrue(FORBIDDEN_FIELD_NAMES.isdisjoint(nested_field_names(self.document)))

    def test_repeat_procedure_strips_all_five_provider_credentials(self) -> None:
        runbook = RUNBOOK_PATH.read_text(encoding="utf-8")
        compact_runbook = re.sub(r"\s+", "", runbook)
        mcp_sequence = (
            '"-u","OPENAI_API_KEY","-u","CODEX_API_KEY",'
            '"-u","ANTHROPIC_API_KEY","-u","ANTHROPIC_AUTH_TOKEN",'
            '"-u","CLAUDE_CODE_OAUTH_TOKEN"'
        )
        self.assertIn(mcp_sequence, compact_runbook)

        stripped_parent_sequence = "\n".join(
            (
                "/usr/bin/env -u OPENAI_API_KEY -u CODEX_API_KEY \\",
                "  -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN \\",
                "  -u CLAUDE_CODE_OAUTH_TOKEN",
            )
        )
        self.assertGreaterEqual(runbook.count(stripped_parent_sequence), 4)

    def test_hostile_or_inflated_mutations_are_rejected(self) -> None:
        mutations: list[tuple[str, Any]] = []

        for label, path, value in (
            ("wrong source commit", ("source", "commit"), "0" * 40),
            ("production registration", ("source", "production_registration"), True),
            ("modern readiness inflation", ("attempts", 0, "transport_readiness"), "ready"),
            ("modern capability inflation", ("attempts", 0, "capability"), "passed"),
            ("fallback capability inflation", ("attempts", 1, "capability"), "passed"),
            ("independent host claim", ("limitations", "independent_host_gate_completed"), True),
            ("exact-five claim", ("limitations", "exact_five_assembly_exercised"), True),
            ("provider claim", ("limitations", "live_provider_called"), True),
            ("remote HTTP claim", ("limitations", "remote_http_observed"), True),
            ("release claim", ("limitations", "activation_or_release_claimed"), True),
        ):
            mutation = copy.deepcopy(self.document)
            target: Any = mutation
            for part in path[:-1]:
                target = target[part]
            target[path[-1]] = value
            mutations.append((label, mutation))

        swapped_attempts = copy.deepcopy(self.document)
        swapped_attempts["attempts"] = list(reversed(swapped_attempts["attempts"]))
        mutations.append(("attempt order", swapped_attempts))

        modern_list = copy.deepcopy(self.document)
        modern_list["attempts"][0]["telemetry"]["tools_list_request"] = copy.deepcopy(
            self.document["attempts"][1]["telemetry"]["tools_list_request"]
        )
        mutations.append(("modern tools/list inflation", modern_list))

        missing_fallback_list = copy.deepcopy(self.document)
        del missing_fallback_list["attempts"][1]["telemetry"]["tools_list_response"]
        mutations.append(("missing fallback tools/list", missing_fallback_list))

        successful_error = copy.deepcopy(self.document)
        successful_error["attempts"][1]["telemetry"]["initialize_response"][
            "error_code"
        ] = -32022
        mutations.append(("error on success response", successful_error))

        missing_error = copy.deepcopy(self.document)
        del missing_error["attempts"][0]["telemetry"]["initialize_response"][
            "error_code"
        ]
        mutations.append(("missing error code", missing_error))

        modern_success = copy.deepcopy(self.document)
        modern_success["attempts"][0]["telemetry"]["initialize_response"][
            "outcome"
        ] = "success"
        del modern_success["attempts"][0]["telemetry"]["initialize_response"][
            "error_code"
        ]
        mutations.append(("modern success contradiction", modern_success))

        fallback_initialize_error = copy.deepcopy(self.document)
        fallback_initialize_error["attempts"][1]["telemetry"]["initialize_response"].update(
            {"outcome": "error", "error_code": -32022}
        )
        mutations.append(("fallback initialize error", fallback_initialize_error))

        fallback_list_error = copy.deepcopy(self.document)
        fallback_list_error["attempts"][1]["telemetry"]["tools_list_response"].update(
            {"outcome": "error", "error_code": -32603}
        )
        mutations.append(("fallback tools/list error", fallback_list_error))

        divergent_error = copy.deepcopy(self.document)
        divergent_error["attempts"][0]["telemetry"]["initialize_response"][
            "error_code"
        ] = -32603
        mutations.append(("divergent inner error", divergent_error))

        wrong_list_method = copy.deepcopy(self.document)
        wrong_list_method["attempts"][1]["telemetry"]["tools_list_request"][
            "method_label"
        ] = "other"
        mutations.append(("wrong tools/list method", wrong_list_method))

        inconsistent_event_count = copy.deepcopy(self.document)
        inconsistent_event_count["attempts"][1]["telemetry"]["event_count"] = 1
        mutations.append(("inconsistent event count", inconsistent_event_count))

        duplicate_runtime = copy.deepcopy(self.document)
        duplicate_runtime["source"]["runtime_files"] = [
            copy.deepcopy(self.document["source"]["runtime_files"][0])
            for _ in range(5)
        ]
        mutations.append(("duplicate runtime bindings", duplicate_runtime))

        absolute_path = copy.deepcopy(self.document)
        absolute_path["source"]["runtime_files"][0]["path"] = (
            "/" + "Users" + "/example/runtime.ts"
        )
        mutations.append(("absolute path", absolute_path))

        for label, path in (
            (
                "parent traversal",
                "apps/../../" + "Users" + "/example/private.log",
            ),
            ("current-directory segment", "scripts/./runtime.mjs"),
            ("empty path segment", "apps//runtime.ts"),
        ):
            traversal = copy.deepcopy(self.document)
            traversal["source"]["runtime_files"][0]["path"] = path
            mutations.append((label, traversal))

        session = copy.deepcopy(self.document)
        session["attempts"][0]["telemetry"]["session_id_sha256"] = "0" * 64
        mutations.append(("session identifier", session))

        unknown = copy.deepcopy(self.document)
        unknown["unexpected"] = True
        mutations.append(("unknown root field", unknown))

        for label, mutation in mutations:
            with self.subTest(label=label):
                self.assert_invalid(mutation)

    def test_non_standard_json_numbers_are_rejected_at_load_boundary(self) -> None:
        with self.assertRaises(ValueError):
            json.loads('{"duration_ms": NaN}', parse_constant=reject_non_standard_number)


if __name__ == "__main__":
    unittest.main()
