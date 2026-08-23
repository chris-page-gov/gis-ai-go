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
SCHEMA_PATH = ROOT / "schemas" / "qual-206-legacy-stdio-readiness.schema.json"
EVIDENCE_PATH = (
    ROOT
    / "tests"
    / "interoperability"
    / "evidence"
    / "claude-code-legacy-stdio-readiness-2026-08-23.json"
)
SOURCE_COMMIT = "30b575beb27ff805745a2864c1acf44392774046"
SOURCE_TREE = "bb84c13d618984304d5db300be775275b8037ea8"
SCHEMA_SHA256 = "5ce73d3d45c762112ac932407000b4379d07d92a9e54808227cd72e6050fd02a"
EVIDENCE_SHA256 = "a3d40e2013095baf977bad336366c0fb429a05b6a5a267c3e069595e4cdb1a6b"
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
    "Accepted protected-main Claude Code transport-readiness evidence only. The "
    "constructor-only local conformance launcher passed legacy STDIO initialisation "
    "and tools/list; no tool, resource, exact-five production assembly, model, "
    "provider, remote HTTP host, registration, activation, deployment or release "
    "was exercised. Capability remains unscored."
)
PUBLIC_EVIDENCE_FORBIDDEN = re.compile(
    r"(?:"
    r"/Users/|/home/|/Volumes/|/private/tmp/|file://|"
    r"[A-Za-z]:\\\\Users\\\\|"
    r"\bsk-[A-Za-z0-9_-]{8,}|\bgh[opusr]_[A-Za-z0-9]{8,}|"
    r"\bxox[baprs]-[A-Za-z0-9-]{8,}|\bAKIA[0-9A-Z]{16}|"
    r"\bBearer\s+[A-Za-z0-9._~-]+|"
    r"OPENAI_API_KEY|CODEX_API_KEY|ANTHROPIC_API_KEY|"
    r"https?://(?:chatgpt\.com/c/|claude\.ai/chat/)|"
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
    r")",
    re.IGNORECASE,
)
FORBIDDEN_FIELD_NAMES = {
    "credential",
    "device_id",
    "environment",
    "headers",
    "host_profile_path",
    "log",
    "prompt",
    "raw_command",
    "result",
    "telemetry_path",
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


class Qual206LegacyStdioReadinessTests(unittest.TestCase):
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
                "path": "schemas/qual-206-legacy-stdio-readiness.schema.json",
                "sha256": SCHEMA_SHA256,
            },
        )

    def test_record_binds_the_exact_protected_main_source_materials(self) -> None:
        source = self.document["source"]
        self.assertEqual(source["commit"], SOURCE_COMMIT)
        self.assertEqual(source["tree"], SOURCE_TREE)
        actual_tree = git_output("rev-parse", f"{SOURCE_COMMIT}^{{tree}}").decode().strip()
        self.assertEqual(actual_tree, SOURCE_TREE)
        self.assertEqual(
            [(item["path"], item["sha256"]) for item in source["runtime_files"]],
            EXPECTED_RUNTIME_FILES,
        )
        for path, expected_digest in EXPECTED_RUNTIME_FILES:
            with self.subTest(path=path):
                self.assertEqual(sha256_bytes(git_blob(SOURCE_COMMIT, path)), expected_digest)
        build = source["build"]
        self.assertEqual(
            build["lockfile"],
            {"path": "pnpm-lock.yaml", "sha256": LOCKFILE_SHA256},
        )
        self.assertEqual(
            sha256_bytes(git_blob(SOURCE_COMMIT, "pnpm-lock.yaml")),
            LOCKFILE_SHA256,
        )
        self.assertEqual(build["command"], "pnpm run test:interoperability")
        self.assertTrue(build["dependencies_installed_with_frozen_lockfile"])
        self.assertTrue(build["preflight_passed"])
        self.assertEqual(
            [
                (item["source_path"], item["sha256"])
                for item in build["compiled_entrypoints"]
            ],
            EXPECTED_COMPILED_ENTRYPOINTS,
        )
        # These are immutable observed entrypoint bytes, not a claim about a later
        # branch build. The exact historical tree and frozen lockfile are verified
        # above so ordinary future runtime work cannot relabel this observation.

    def test_transport_readiness_is_not_inflated_into_capability(self) -> None:
        source = self.document["source"]
        host = self.document["host"]
        telemetry = self.document["telemetry"]
        isolation = self.document["isolation"]
        limitations = self.document["limitations"]

        self.assertEqual(telemetry["source_commit"], source["commit"])
        self.assertEqual(telemetry["event_count"], sum(telemetry["event_counts"].values()))
        self.assertEqual(host["transport_readiness"], "ready")
        self.assertEqual(host["capability"], "unscored")
        self.assertEqual((host["platform"], host["architecture"]), ("darwin", "arm64"))
        self.assertTrue(host["initialize_success"])
        self.assertTrue(host["tools_list_success"])
        self.assertFalse(host["model_authentication_supplied"])
        self.assertFalse(host["model_task_requested"])
        self.assertFalse(host["tool_call_observed"])
        self.assertFalse(host["resource_read_observed"])
        self.assertEqual(telemetry["initialize_response"]["outcome"], "success")
        self.assertEqual(telemetry["tools_list_response"]["outcome"], "success")
        for response_name in ("initialize_response", "tools_list_response"):
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
        self.assertEqual(isolation["token_pattern_matches"], 0)
        self.assertEqual(isolation["remaining_isolated_processes_after_cleanup"], 0)
        self.assertFalse(isolation["normal_profile_mutation_observed"])
        self.assertFalse(isolation["raw_host_logs_published"])
        self.assertTrue(isolation["parent_openai_key_variables_removed"])
        self.assertTrue(isolation["mcp_child_environment_allowlisted"])
        self.assertTrue(isolation["mcp_child_openai_key_variables_removed"])
        self.assertEqual(set(limitations.values()), {False})
        self.assertEqual(self.document["boundary"], BOUNDARY)

    def test_public_record_contains_no_path_secret_or_raw_payload_fields(self) -> None:
        public_text = EVIDENCE_PATH.read_text(encoding="utf-8")
        self.assertIsNone(PUBLIC_EVIDENCE_FORBIDDEN.search(public_text))
        self.assertTrue(
            FORBIDDEN_FIELD_NAMES.isdisjoint(nested_field_names(self.document))
        )

    def test_hostile_or_inflated_mutations_are_rejected(self) -> None:
        mutations: list[tuple[str, Any]] = []

        absolute_path = copy.deepcopy(self.document)
        absolute_path["source"]["runtime_files"][0]["path"] = (
            "/" + "Users" + "/example/runtime.ts"
        )
        mutations.append(("absolute path", absolute_path))

        parent_path = copy.deepcopy(self.document)
        parent_path["source"]["runtime_files"][0]["path"] = "../runtime.ts"
        mutations.append(("parent-relative path", parent_path))

        raw_command = copy.deepcopy(self.document)
        raw_command["host"]["raw_command"] = "unexpected"
        mutations.append(("raw command", raw_command))

        prompt = copy.deepcopy(self.document)
        prompt["telemetry"]["prompt"] = "unexpected"
        mutations.append(("prompt", prompt))

        raw_result = copy.deepcopy(self.document)
        raw_result["telemetry"]["result"] = {"unexpected": True}
        mutations.append(("result", raw_result))

        environment = copy.deepcopy(self.document)
        environment["isolation"]["environment"] = {"unexpected": True}
        mutations.append(("environment", environment))

        log = copy.deepcopy(self.document)
        log["telemetry"]["log"] = "unexpected"
        mutations.append(("log", log))

        wrong_commit = copy.deepcopy(self.document)
        wrong_commit["source"]["commit"] = "0" * 40
        mutations.append(("wrong source commit", wrong_commit))

        activation = copy.deepcopy(self.document)
        activation["source"]["production_activation"] = True
        mutations.append(("production activation", activation))

        capability = copy.deepcopy(self.document)
        capability["host"]["capability"] = "passed"
        mutations.append(("capability inflation", capability))

        tool_call = copy.deepcopy(self.document)
        tool_call["host"]["tool_call_observed"] = True
        mutations.append(("tool call", tool_call))

        resource_read = copy.deepcopy(self.document)
        resource_read["host"]["resource_read_observed"] = True
        mutations.append(("resource read", resource_read))

        pending = copy.deepcopy(self.document)
        pending["telemetry"]["pending_request_count"] = 1
        mutations.append(("pending request", pending))

        token_match = copy.deepcopy(self.document)
        token_match["isolation"]["token_pattern_matches"] = 1
        mutations.append(("credential pattern", token_match))

        completed_gate = copy.deepcopy(self.document)
        completed_gate["limitations"]["independent_host_gate_completed"] = True
        mutations.append(("completed host gate", completed_gate))

        exact_five = copy.deepcopy(self.document)
        exact_five["limitations"]["exact_five_assembly_exercised"] = True
        mutations.append(("exact-five claim", exact_five))

        raw_content = copy.deepcopy(self.document)
        raw_content["telemetry"]["raw_content_published"] = True
        mutations.append(("raw content", raw_content))

        swapped_runtime = copy.deepcopy(self.document)
        swapped_runtime["source"]["runtime_files"][0:2] = reversed(
            swapped_runtime["source"]["runtime_files"][0:2]
        )
        mutations.append(("runtime order", swapped_runtime))

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
