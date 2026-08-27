from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, cast
import unittest

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import verify_qual_206_claude_exact_five_capability as verifier  # noqa: E402


PRIVATE_SCHEMA = (
    ROOT / "schemas/qual-206-claude-exact-five-capability-private-run-v1.schema.json"
)
SESSION_SCHEMA = (
    ROOT / "schemas/qual-206-claude-exact-five-capability-session-v1.schema.json"
)
PUBLIC_SCHEMA = (
    ROOT / "schemas/qual-206-claude-exact-five-capability-evidence-v1.schema.json"
)
OPERATIONS = list(verifier.OPERATIONS)
FORBIDDEN_PUBLIC = re.compile(
    r"(?:/Users/|/home/|/Volumes/|/private/tmp/|/tmp/|/var/folders/|"
    r"/opt/homebrew/|/usr/bin/|file://|"
    r"https?://(?:chatgpt\.com|chat\.openai\.com)/share/|"
    r"[A-Za-z]:\\\\Users\\\\|"
    r"\bsk-[A-Za-z0-9_-]{8,}|\bgh[opusr]_[A-Za-z0-9]{8,}|"
    r"\bxox[baprs]-[A-Za-z0-9-]{8,}|\bAKIA[0-9A-Z]{16}|"
    r"\bBearer\s+[A-Za-z0-9._~-]+|"
    r"OPENAI_API_KEY|ANTHROPIC_API_KEY|ANTHROPIC_AUTH_TOKEN|"
    r"CLAUDE_CODE_OAUTH_TOKEN|"
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-"
    r"[0-9a-f]{12}\b)",
    re.IGNORECASE,
)
FORBIDDEN_FIELDS = {
    "api_budget_usd",
    "arguments",
    "cost",
    "environment",
    "local_path",
    "mcp_config",
    "pid",
    "prompt",
    "prompt_text",
    "raw_content",
    "request_id",
    "response_body",
    "result_material",
    "run_id",
    "session_id",
    "settings",
    "subscription_type",
    "total_cost_usd",
    "user_identity",
}


def validator(path: Path) -> Draft202012Validator:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def fake_host_validator(
    path: Path,
    *,
    executable_bytes: int,
    executable_sha256: str,
) -> Draft202012Validator:
    schema = json.loads(path.read_text(encoding="utf-8"))
    host = schema["properties"]["host"]["properties"]
    host["executable_bytes"] = {"const": executable_bytes}
    host["executable_sha256"] = {"const": executable_sha256}
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def nested_field_names(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {
            name for child in value.values() for name in nested_field_names(child)
        }
    if isinstance(value, list):
        return {name for child in value for name in nested_field_names(child)}
    return set()


def write_private_json(path: Path, value: dict[str, Any]) -> bytes:
    raw = verifier.canonical_line(value)
    path.write_bytes(raw)
    os.chmod(path, 0o600)
    return raw


def rebind_fake_event_capture(root: Path) -> None:
    sessions = sorted((root / "observer").glob("session-*"))
    if not sessions:
        raise AssertionError("fake harness did not create an observer session")
    for session in sessions:
        event_path = session / "events.jsonl"
        events = [
            json.loads(line)
            for line in event_path.read_text(encoding="utf-8").splitlines()
        ]
        prior = b""
        previous: str | None = None
        encoded: list[bytes] = []
        for index, event in enumerate(events):
            if event["event"] == "lifecycle" and event["phase"] == "session-start":
                event["source_checkout"] = {
                    "detached_head": True,
                    "head_matches_source_commit": True,
                    "local_origin_main_matches_source_commit": True,
                    "working_tree_clean": True,
                }
            if event["event"] == "lifecycle" and event["phase"] == "session-end":
                event["prior_event_count"] = index
                event["prior_event_log_bytes"] = len(prior)
                event["prior_event_log_sha256"] = hashlib.sha256(prior).hexdigest()
            event["previous_event_sha256"] = previous
            core = dict(event)
            core.pop("event_sha256", None)
            event["event_sha256"] = verifier.composite.domain_separated_sha256(core)
            line = verifier.canonical_line(event)
            encoded.append(line)
            if event["event"] != "lifecycle" or event.get("phase") != "session-end":
                prior += line
            previous = event["event_sha256"]
        event_raw = b"".join(encoded)
        event_path.write_bytes(event_raw)
        os.chmod(event_path, 0o600)
        manifest_path = session / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["event_log"] = {
            "bytes": len(event_raw),
            "event_count": len(events),
            "last_event_sha256": previous,
            "sha256": hashlib.sha256(event_raw).hexdigest(),
        }
        write_private_json(manifest_path, manifest)


def create_fake_capture(root: Path, *, scenario: str = "positive") -> tuple[int, str]:
    node = Path(
        subprocess.check_output(["node", "-p", "process.execPath"], text=True).strip()
    )
    node_raw = node.read_bytes()
    driver = root.parent / "drive-exact-five-fake.mjs"
    driver.write_text(
        """
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
const [captureRoot, repositoryRoot, fakePath, scenario] = process.argv.slice(2);
const launcher = await import(pathToFileURL(
  `${repositoryRoot}/scripts/qual_206_claude_exact_five_capability_harness.mjs`,
));
const harness = await import(pathToFileURL(
  `${repositoryRoot}/scripts/qual_206_claude_capability_harness.mjs`,
));
const closure = await import(pathToFileURL(
  `${repositoryRoot}/scripts/qual_206_claude_runtime_closure.mjs`,
));
const digest = (value) => createHash("sha256").update(value).digest("hex");
const commit = execFileSync(
  "git", ["-C", repositoryRoot, "rev-parse", "HEAD"], {encoding:"utf8"},
).trim();
const tree = execFileSync(
  "git", ["-C", repositoryRoot, "rev-parse", "HEAD^{tree}"], {encoding:"utf8"},
).trim();
const nodeBytes = readFileSync(process.execPath);
const generated = closure.measureGeneratedRuntimeClosure(repositoryRoot);
const installed = closure.measureInstalledDependencyClosure(repositoryRoot);
const environment = {...process.env};
for (const name of [
  "OPENAI_API_KEY", "CODEX_API_KEY", "ANTHROPIC_API_KEY",
  "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_BASE_URL",
  "CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX",
  "CLAUDE_CODE_USE_FOUNDRY", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY",
  "AWS_SESSION_TOKEN", "GOOGLE_APPLICATION_CREDENTIALS", "AZURE_CLIENT_SECRET",
]) delete environment[name];
await launcher.runClaudeExactFiveCapability({
  authKind: "first-party-login", claudeBin: process.execPath, maxBudgetUsd: null,
  model: "claude-sonnet-5", privateRoot: captureRoot, sourceCommit: commit,
}, {
  acceptedIdentity: {
    bytes: nodeBytes.length, sha256: digest(nodeBytes), version: "2.1.245",
  },
  authStatus: () => ({
    api_provider: "firstParty", auth_method: "claude.ai",
    logged_in: true, subscription_type: "test-profile",
  }),
  command: [process.execPath, fakePath], environment,
  extraEnvironment: {QUAL_206_FAKE_CLAUDE_EXACT_FIVE_SCENARIO: scenario},
  maximumMilliseconds: 30000,
  networkSandboxProbe: harness.expectedNetworkSandboxProbeEvidence(),
  parentExecutable: process.execPath,
  runId: "12345678-1234-4234-8234-123456789abc",
  runtimeClosureBinding: {
    generated_first_party_closure: {
      ...generated,
      reference_manifest_sha256: generated.manifest_sha256,
      reference_matches_current: true,
    },
    installed_dependency_closure: installed,
  },
  sourceFacts: (value) => ({
    commit: value,
    tree,
    repository_origin: "https://github.com/chris-page-gov/gis-ai-go.git",
    local_origin_main_match: true,
    protected_main_verification: "external-publication-gate",
  }),
  version: "2.1.245 (Claude Code)",
});
""",
        encoding="utf-8",
    )
    fake = (
        ROOT
        / "tests/interoperability/fixtures/qual_206_fake_claude_exact_five_client.mjs"
    )
    completed = subprocess.run(
        [str(node), str(driver), str(root), str(ROOT), str(fake), scenario],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=60,
    )
    if completed.returncode != 0:
        client_stderr = (root / "stderr.log").read_text(encoding="utf-8")
        raise AssertionError(
            f"fake exact-five harness failed: {completed.stdout}\n{completed.stderr}\n"
            f"client stderr: {client_stderr}"
        )
    rebind_fake_event_capture(root)
    return len(node_raw), hashlib.sha256(node_raw).hexdigest()


def fake_source_boundary(manifest: dict[str, Any]) -> None:
    binding = manifest["runtime_binding"]
    materials = binding["tracked_source_materials"]
    if {item["path"] for item in materials} != verifier.TRACKED_EXACT_FIVE_CAPABILITY_MATERIALS:
        raise AssertionError("fake capture did not bind the exact verifier source closure")
    generated = binding["generated_first_party_closure"]
    if generated["manifest_sha256"] != generated["reference_manifest_sha256"]:
        raise AssertionError("generated closure reference changed")
    if {
        "bytes": generated["bytes"],
        "file_count": generated["file_count"],
        "manifest_sha256": generated["manifest_sha256"],
    } != verifier.host002.measure_generated_runtime_closure():
        raise AssertionError("generated closure changed")
    if binding["installed_dependency_closure"] != (
        verifier.host002.measure_installed_dependency_closure()
    ):
        raise AssertionError("installed dependency closure changed")


def rebind_result_material(root: Path) -> None:
    session = root / "observer/session-1"
    result_path = session / "exact-five-results.json"
    raw = result_path.read_bytes()
    summary_path = session / "exact-five-capability.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["result_material"] = {
        "name": "exact-five-results.json",
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
    write_private_json(summary_path, summary)


def rebind_stdout(root: Path) -> None:
    raw = (root / "stdout.json").read_bytes()
    facts = {
        "bytes": len(raw),
        "limit_exceeded": False,
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
    manifest_path = root / "run-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["execution"]["stdout"] = facts
    manifest["private_files"]["stdout"] = {"name": "stdout.json", **facts}
    write_private_json(manifest_path, manifest)


class ClaudeExactFiveCapabilityContractsTest(unittest.TestCase):
    @unittest.skipUnless(
        sys.platform == "darwin",
        "the accepted Claude exact-five runtime uses macOS Seatbelt",
    )
    def test_fake_capture_projects_only_a_minimised_independently_verified_pass(
        self,
    ) -> None:
        evidence_before = sorted((ROOT / "tests/interoperability/evidence").iterdir())
        with tempfile.TemporaryDirectory(dir="/private/tmp") as value:
            base = Path(value)
            capture = base / "capture"
            capture.mkdir(mode=0o700)
            os.chmod(capture, 0o700)
            executable_bytes, executable_sha256 = create_fake_capture(capture)
            private_check = fake_host_validator(
                PRIVATE_SCHEMA,
                executable_bytes=executable_bytes,
                executable_sha256=executable_sha256,
            )
            public_check = fake_host_validator(
                PUBLIC_SCHEMA,
                executable_bytes=executable_bytes,
                executable_sha256=executable_sha256,
            )
            projection = verifier.verify_and_project(
                capture,
                source_verifier=fake_source_boundary,
                private_validator=private_check,
                public_validator=public_check,
            )
            self.assertEqual(projection["status"], "capability_pass")
            self.assertEqual(projection["profile"]["operation_order"], OPERATIONS)
            self.assertEqual(projection["transport"]["tool_call_count"], 5)
            self.assertEqual(projection["transport"]["resources_advertised"], 0)
            self.assertEqual(projection["transport"]["resource_read_count"], 0)
            self.assertEqual(projection["transport"]["provider_transport_calls"], 1)
            self.assertEqual(
                projection["transport"]["guarded_provider_api_invocations"], 0
            )
            self.assertEqual(projection["result"]["claude_cli_reported_turns"], 9)
            self.assertEqual(projection["result"]["agentic_turn_limit"], 8)
            receipts = [
                item["receipt_id"] for item in projection["result"]["operation_receipts"]
            ]
            self.assertEqual(len(set(receipts)), 5)
            self.assertEqual(
                projection["result"]["inspection_relationship"],
                {
                    "search_receipt_id": receipts[0],
                    "inspected_receipt_id": receipts[0],
                    "inspection_receipt_id": receipts[-1],
                    "valid": True,
                },
            )
            self.assertTrue(projection["result"]["independent_result_verification"])
            self.assertEqual(
                projection["claims"],
                {
                    "local_stdio_exact_five_model_capability": True,
                    "remote_http_interoperability": False,
                    "live_geospatial_provider": False,
                    "registry_publication": False,
                    "activation": False,
                    "deployment": False,
                    "release": False,
                },
            )
            rendered = json.dumps(projection, separators=(",", ":"))
            self.assertIsNone(FORBIDDEN_PUBLIC.search(rendered))
            self.assertFalse(nested_field_names(projection) & FORBIDDEN_FIELDS)

            session = json.loads(
                (capture / "observer/session-1/exact-five-capability.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(list(validator(SESSION_SCHEMA).iter_errors(session)), [])
            manifest = json.loads((capture / "run-manifest.json").read_text())
            self.assertEqual(list(private_check.iter_errors(manifest)), [])
            self.assertEqual(list(public_check.iter_errors(projection)), [])

            complete_material = json.loads(
                (capture / "observer/session-1/exact-five-results.json").read_text(
                    encoding="utf-8"
                )
            )
            split_results = (
                (complete_material["results"][:1], 1, 0, 0),
                (complete_material["results"][1:], 0, 1, 5),
            )
            for entries, discoveries, listings, calls in split_results:
                split = {
                    **complete_material,
                    "results": [
                        {**entry, "ordinal": ordinal}
                        for ordinal, entry in enumerate(entries)
                    ],
                }
                verified_split = verifier.independently_verify_results(
                    verifier.canonical_line(split),
                    node_path=manifest["runtime_binding"]["node_runtime"]["path"],
                )
                self.assertEqual(verified_split["discovery_count"], discoveries)
                self.assertEqual(verified_split["tools_list_count"], listings)
                self.assertEqual(len(verified_split["operations"]), calls)

            independent_mutations: list[tuple[str, dict[str, Any]]] = []
            result_reorder = copy.deepcopy(complete_material)
            result_reorder["results"][2]["result"], result_reorder["results"][3][
                "result"
            ] = (
                result_reorder["results"][3]["result"],
                result_reorder["results"][2]["result"],
            )
            independent_mutations.append(("result reordering", result_reorder))
            duplicate_result = copy.deepcopy(complete_material)
            duplicate_result["results"][3] = {
                **copy.deepcopy(duplicate_result["results"][2]),
                "ordinal": 3,
            }
            independent_mutations.append(("duplicate result", duplicate_result))
            broken_parity = copy.deepcopy(complete_material)
            broken_parity["results"][2]["result"]["content"][0]["text"] = "{}"
            independent_mutations.append(("body parity", broken_parity))
            wrong_relationship = copy.deepcopy(complete_material)
            inspection = wrong_relationship["results"][-1]["result"][
                "structuredContent"
            ]
            inspection["data"]["record"]["receipt"]["receipt_id"] = (
                wrong_relationship["results"][3]["result"]["structuredContent"]
                ["evidence_receipt"]["receipt_id"]
            )
            wrong_relationship["results"][-1]["result"]["content"][0]["text"] = (
                json.dumps(inspection, ensure_ascii=False, separators=(",", ":"))
            )
            independent_mutations.append(
                ("inspection relationship", wrong_relationship)
            )
            extra_method = copy.deepcopy(complete_material)
            extra_method["results"][0]["method"] = "resources/list"
            independent_mutations.append(("extra allowed method", extra_method))
            for label, changed in independent_mutations:
                with self.subTest(independent_result_mutation=label):
                    with self.assertRaisesRegex(
                        verifier.ExactFiveCapabilityVerificationError,
                        "independent exact-five result verification failed",
                    ):
                        verifier.independently_verify_results(
                            verifier.canonical_line(changed),
                            node_path=manifest["runtime_binding"]["node_runtime"][
                                "path"
                            ],
                        )

            mutations: list[tuple[str, dict[str, Any]]] = []
            remote = copy.deepcopy(projection)
            remote["claims"]["remote_http_interoperability"] = True
            mutations.append(("remote HTTP inflation", remote))
            turns = copy.deepcopy(projection)
            turns["result"]["claude_cli_reported_turns"] = 10
            mutations.append(("reported turn bound inflation", turns))
            too_few_turns = copy.deepcopy(projection)
            too_few_turns["result"]["claude_cli_reported_turns"] = 2
            mutations.append(("reported turn bound deflation", too_few_turns))
            order = copy.deepcopy(projection)
            order["result"]["operation_order"][0:2] = reversed(
                order["result"]["operation_order"][0:2]
            )
            mutations.append(("operation reordering", order))
            receipt_boolean = copy.deepcopy(projection)
            receipt_boolean["result"]["operation_receipts"][2][
                "receipt_verification_valid"
            ] = False
            mutations.append(("receipt verification downgrade", receipt_boolean))
            leaked = copy.deepcopy(projection)
            leaked["private_capture"]["local_path"] = "/private/tmp/capture"
            mutations.append(("private path", leaked))
            for label, changed in mutations:
                with self.subTest(public_mutation=label):
                    self.assertTrue(list(public_check.iter_errors(changed)))

            result_path = capture / "observer/session-1/exact-five-results.json"
            summary_path = capture / "observer/session-1/exact-five-capability.json"
            original_result = result_path.read_bytes()
            original_summary = summary_path.read_bytes()
            try:
                result_material = json.loads(original_result)
                structured = result_material["results"][3]["result"][
                    "structuredContent"
                ]
                structured["evidence_receipt"]["receipt_id"] = (
                    f"gis-ai-go:evidence-receipt:sha256:{'0' * 64}"
                )
                result_material["results"][3]["result"]["content"][0]["text"] = (
                    json.dumps(structured, ensure_ascii=False, separators=(",", ":"))
                )
                write_private_json(result_path, result_material)
                rebind_result_material(capture)
                with self.assertRaisesRegex(
                    verifier.ExactFiveCapabilityVerificationError,
                    "independent exact-five result verification failed",
                ):
                    verifier.verify_and_project(
                        capture,
                        source_verifier=fake_source_boundary,
                        private_validator=private_check,
                        public_validator=public_check,
                    )
            finally:
                result_path.write_bytes(original_result)
                summary_path.write_bytes(original_summary)
                os.chmod(result_path, 0o600)
                os.chmod(summary_path, 0o600)

            original_summary = summary_path.read_bytes()
            try:
                summary = json.loads(original_summary)
                summary["operations"][1]["request"]["sha256"] = "0" * 64
                write_private_json(summary_path, summary)
                with self.assertRaisesRegex(
                    verifier.ExactFiveCapabilityVerificationError,
                    "catalogue.describe request",
                ):
                    verifier.verify_and_project(
                        capture,
                        source_verifier=fake_source_boundary,
                        private_validator=private_check,
                        public_validator=public_check,
                    )
            finally:
                summary_path.write_bytes(original_summary)
                os.chmod(summary_path, 0o600)

            output_path = capture / "stdout.json"
            manifest_path = capture / "run-manifest.json"
            original_output = output_path.read_bytes()
            original_manifest = manifest_path.read_bytes()
            try:
                output = json.loads(original_output)
                output["num_turns"] = 10
                output_path.write_bytes(
                    json.dumps(output, separators=(",", ":")).encode()
                )
                os.chmod(output_path, 0o600)
                rebind_stdout(capture)
                with self.assertRaisesRegex(
                    verifier.ExactFiveCapabilityVerificationError,
                    "reported turns",
                ):
                    verifier.verify_and_project(
                        capture,
                        source_verifier=fake_source_boundary,
                        private_validator=private_check,
                        public_validator=public_check,
                    )
            finally:
                output_path.write_bytes(original_output)
                manifest_path.write_bytes(original_manifest)
                os.chmod(output_path, 0o600)
                os.chmod(manifest_path, 0o600)

            try:
                output = json.loads(original_output)
                output["num_turns"] = 2
                output_path.write_bytes(
                    json.dumps(output, separators=(",", ":")).encode()
                )
                os.chmod(output_path, 0o600)
                rebind_stdout(capture)
                with self.assertRaisesRegex(
                    verifier.ExactFiveCapabilityVerificationError,
                    "reported turns",
                ):
                    verifier.verify_and_project(
                        capture,
                        source_verifier=fake_source_boundary,
                        private_validator=private_check,
                        public_validator=public_check,
                    )
            finally:
                output_path.write_bytes(original_output)
                manifest_path.write_bytes(original_manifest)
                os.chmod(output_path, 0o600)
                os.chmod(manifest_path, 0o600)

            try:
                output = json.loads(original_output)
                output["stop_reason"] = "tool_use"
                output_path.write_bytes(
                    json.dumps(output, separators=(",", ":")).encode()
                )
                os.chmod(output_path, 0o600)
                rebind_stdout(capture)
                with self.assertRaisesRegex(
                    verifier.ExactFiveCapabilityVerificationError,
                    "end_turn terminal state",
                ):
                    verifier.verify_and_project(
                        capture,
                        source_verifier=fake_source_boundary,
                        private_validator=private_check,
                        public_validator=public_check,
                    )
            finally:
                output_path.write_bytes(original_output)
                manifest_path.write_bytes(original_manifest)
                os.chmod(output_path, 0o600)
                os.chmod(manifest_path, 0o600)
        evidence_after = sorted((ROOT / "tests/interoperability/evidence").iterdir())
        self.assertEqual(evidence_after, evidence_before)

    @unittest.skipUnless(
        sys.platform == "darwin",
        "the accepted Claude exact-five runtime uses macOS Seatbelt",
    )
    def test_four_call_tool_use_terminal_is_rejected(self) -> None:
        evidence_before = sorted((ROOT / "tests/interoperability/evidence").iterdir())
        with tempfile.TemporaryDirectory(dir="/private/tmp") as value:
            capture = Path(value) / "capture"
            capture.mkdir(mode=0o700)
            os.chmod(capture, 0o700)
            executable_bytes, executable_sha256 = create_fake_capture(
                capture,
                scenario="premature-tool-use",
            )
            output = json.loads((capture / "stdout.json").read_text(encoding="utf-8"))
            self.assertEqual(output["subtype"], "success")
            self.assertIs(output["is_error"], False)
            self.assertEqual(output["stop_reason"], "tool_use")
            self.assertEqual(output["num_turns"], 7)
            self.assertEqual(output["structured_output"]["operation_order"], OPERATIONS)
            summary = json.loads(
                (
                    capture
                    / "observer/session-2/exact-five-capability.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(len(summary["operations"]), 4)
            self.assertEqual(
                [item["request"]["operation"] for item in summary["operations"]],
                OPERATIONS[:4],
            )
            self.assertEqual(summary["protocol_session_status"], "failed")
            with self.assertRaisesRegex(
                verifier.ExactFiveCapabilityVerificationError,
                "session-end does not describe one clean, complete observation",
            ):
                verifier.verify_and_project(
                    capture,
                    source_verifier=fake_source_boundary,
                    private_validator=fake_host_validator(
                        PRIVATE_SCHEMA,
                        executable_bytes=executable_bytes,
                        executable_sha256=executable_sha256,
                    ),
                    public_validator=fake_host_validator(
                        PUBLIC_SCHEMA,
                        executable_bytes=executable_bytes,
                        executable_sha256=executable_sha256,
                    ),
                )
        evidence_after = sorted((ROOT / "tests/interoperability/evidence").iterdir())
        self.assertEqual(evidence_after, evidence_before)

    def test_no_exact_five_public_evidence_is_registered_before_a_live_run(self) -> None:
        matches = sorted(
            (ROOT / "tests/interoperability/evidence").glob(
                "claude-code-2.1.245-exact-five-capability-*.json"
            )
        )
        self.assertEqual(matches, [])

    @unittest.skipUnless(
        sys.platform == "darwin",
        "the accepted Claude exact-five runtime uses macOS Seatbelt",
    )
    def test_accepted_two_session_negotiation_and_call_shape_projects(self) -> None:
        with tempfile.TemporaryDirectory(dir="/private/tmp") as value:
            capture = Path(value) / "capture"
            capture.mkdir(mode=0o700)
            os.chmod(capture, 0o700)
            executable_bytes, executable_sha256 = create_fake_capture(
                capture,
                scenario="split-sessions",
            )
            projection = verifier.verify_and_project(
                capture,
                source_verifier=fake_source_boundary,
                private_validator=fake_host_validator(
                    PRIVATE_SCHEMA,
                    executable_bytes=executable_bytes,
                    executable_sha256=executable_sha256,
                ),
                public_validator=fake_host_validator(
                    PUBLIC_SCHEMA,
                    executable_bytes=executable_bytes,
                    executable_sha256=executable_sha256,
                ),
            )
            self.assertEqual(projection["status"], "capability_pass")
            self.assertEqual(projection["transport"]["session_count"], 2)
            self.assertEqual(projection["transport"]["request_count"], 7)
            self.assertEqual(projection["transport"]["tool_call_count"], 5)
            self.assertEqual(projection["transport"]["resources_advertised"], 0)


if __name__ == "__main__":
    unittest.main()
