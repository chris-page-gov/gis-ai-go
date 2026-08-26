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
from unittest.mock import patch

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import verify_qual_206_claude_capability as verifier  # noqa: E402


PUBLIC_SCHEMA_PATH = (
    ROOT / "schemas/qual-206-claude-capability-evidence-v1.schema.json"
)
PRIVATE_SCHEMA_PATH = (
    ROOT / "schemas/qual-206-claude-capability-private-run-v1.schema.json"
)
SESSION_SCHEMA_PATH = (
    ROOT / "schemas/qual-206-claude-capability-session-v1.schema.json"
)
SHA = "a" * 64
COMMIT = "b" * 40
TREE = "c" * 40
RECEIPT = f"gis-ai-go:evidence-receipt:sha256:{'d' * 64}"
TRACKED = sorted(verifier.TRACKED_CAPABILITY_MATERIALS)
BOUNDARY = (
    "One bounded Claude Code 2.1.245 model-mediated catalogue.search observation "
    "for QUAL-206-HOST-002 over local MCP 2026-07-28 STDIO. This does not "
    "prove exact-five model capability, remote HTTP interoperability, a live "
    "geospatial provider, registry publication, activation, deployment or release."
)
RECOGNISED_CREDENTIAL_VARIABLES = (
    "OPENAI_API_KEY",
    "CODEX_API_KEY",
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_SESSION_TOKEN",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "AZURE_CLIENT_SECRET",
)


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


def write_private_json(path: Path, value: dict[str, object]) -> bytes:
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


def create_fake_capture(root: Path) -> tuple[int, str]:
    node = Path(subprocess.check_output(["node", "-p", "process.execPath"], text=True).strip())
    node_raw = node.read_bytes()
    node_sha256 = hashlib.sha256(node_raw).hexdigest()
    driver = root.parent / "drive-capability-fake.mjs"
    driver.write_text(
        """
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
const [captureRoot, repositoryRoot, fakePath] = process.argv.slice(2);
const harnessPath = `${repositoryRoot}/scripts/qual_206_claude_capability_harness.mjs`;
const closurePath = `${repositoryRoot}/scripts/qual_206_claude_runtime_closure.mjs`;
const harness = await import(pathToFileURL(harnessPath));
const closure = await import(pathToFileURL(closurePath));
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
await harness.runClaudeCapability({
  authKind: "first-party-login", claudeBin: process.execPath, maxBudgetUsd: null,
  model: "claude-sonnet-5", privateRoot: captureRoot, sourceCommit: commit,
}, {
  acceptedIdentity: {bytes: nodeBytes.length, sha256: digest(nodeBytes), version: "2.1.245"},
  authStatus: () => ({
    api_provider: "firstParty", auth_method: "claude.ai",
    logged_in: true, subscription_type: "pro",
  }),
  command: [process.execPath, fakePath], environment,
  maximumMilliseconds: 30000, parentExecutable: process.execPath,
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
    fake_source = (
        ROOT / "tests/interoperability/fixtures/qual_206_fake_claude_capability_client.mjs"
    )
    fake = root.parent / "qual_206_fake_claude_capability_client.mjs"
    fake.write_text(
        fake_source.read_text(encoding="utf-8")
        .replace("2_000", "10_000")
        .replace(
            "timeout waiting for ${method}",
            "timeout waiting for ${method}; child stderr=${stderr}",
        ),
        encoding="utf-8",
    )
    completed = subprocess.run(
        [str(node), str(driver), str(root), str(ROOT), str(fake)],
        check=True,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=60,
    )
    if not (root / "observer" / "session-1" / "events.jsonl").exists():
        entries = [path.relative_to(root).as_posix() for path in root.rglob("*")]
        manifest_path = root / "run-manifest.json"
        manifest_text = (
            manifest_path.read_text(encoding="utf-8") if manifest_path.exists() else "absent"
        )
        client_stderr = (
            (root / "stderr.log").read_text(encoding="utf-8")
            if (root / "stderr.log").exists()
            else "absent"
        )
        raise AssertionError(
            f"fake harness did not create a session: {entries}; "
            f"stdout={completed.stdout!r}; stderr={completed.stderr!r}; "
            f"client_stderr={client_stderr!r}; manifest={manifest_text}"
        )
    rebind_fake_event_capture(root)
    stdout_path = root / "stdout.json"
    output = json.loads(stdout_path.read_text(encoding="utf-8"))
    output.update(
        {
            "num_turns": 3,
            "usage": {
                "input_tokens": 3,
                "cache_creation_input_tokens": 5,
                "cache_read_input_tokens": 7,
                "output_tokens": 11,
            },
            "modelUsage": {
                "claude-sonnet-5": {
                    "inputTokens": 3,
                    "cacheCreationInputTokens": 5,
                    "cacheReadInputTokens": 7,
                    "outputTokens": 11,
                }
            },
        }
    )
    stdout_raw = json.dumps(output, separators=(",", ":")).encode()
    stdout_path.write_bytes(stdout_raw)
    os.chmod(stdout_path, 0o600)
    manifest_path = root / "run-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    stdout_facts = {
        "bytes": len(stdout_raw),
        "limit_exceeded": False,
        "sha256": hashlib.sha256(stdout_raw).hexdigest(),
    }
    manifest["execution"]["stdout"] = stdout_facts
    manifest["private_files"]["stdout"] = {"name": "stdout.json", **stdout_facts}
    write_private_json(manifest_path, manifest)
    return len(node_raw), node_sha256


def public_projection() -> dict[str, object]:
    return {
        "schema": "gis-ai-go.qual-206-claude-capability-evidence.v1",
        "status": "capability_pass",
        "observed_at": "2026-08-25T18:00:00.000Z",
        "source": {
            "repository": "chris-page-gov/gis-ai-go",
            "repository_origin": "https://github.com/chris-page-gov/gis-ai-go.git",
            "commit": COMMIT,
            "tree": TREE,
            "version": "0.1.0",
            "local_origin_main_match": True,
            "protected_main_verification": "external-publication-gate",
            "production_activation": False,
        },
        "host": {
            "name": "Claude Code",
            "version": "2.1.245",
            "executable_bytes": 376109392,
            "executable_sha256": (
                "9f7c2260251765a18d0b35198669dacc1912f6e8129a3b01f6b58d93365ff1f1"
            ),
            "model_requested": "claude-sonnet-5",
            "auth_kind": "first-party-login",
            "auth_preflight": {
                "logged_in": True,
                "api_provider": "firstParty",
                "auth_method": "claude.ai",
                "subscription_type_observed": True,
            },
            "model_provider_usage_observed": True,
            "guarded_provider_api_invocations": 0,
        },
        "case": {
            "id": "QUAL-206-HOST-002",
            "capability": "catalogue_search",
            "corpus_sha256": (
                "23ac9bc1a76d524bd0e250b11b9ba321b09e66bd5921f1463f50c150001cd389"
            ),
            "prompt_sha256": SHA,
            "required_tool": "catalogue.search",
            "prompt_text_repeated_in_projection": False,
        },
        "transport": {
            "protocol": "2026-07-28",
            "kind": "operating-system-stdio-pipes",
            "session_count": 1,
            "request_count": 3,
            "response_count": 3,
            "tool_call_count": 1,
            "only_catalogue_search_advertised": True,
            "resources_advertised": 0,
            "provider_egress_guard_calls": 0,
        },
        "result": {
            "classification": "capability_pass",
            "capability": "passed",
            "record_id": "hmlr:dataset:inspire-index-polygons",
            "title": "Index polygons spatial data (INSPIRE)",
            "receipt_id": RECEIPT,
            "receipt_verification_valid": True,
            "model_output_match": True,
            "model_reported": "claude-sonnet-5",
            "model_usage_observed": True,
            "input_tokens": 12,
            "output_tokens": 7,
            "num_turns": 3,
            "client_exit_code": 0,
        },
        "isolation": {
            "built_in_tools_available": False,
            "allowed_mcp_tool_count": 1,
            "claude_permission_alias": (
                "mcp__gis-ai-go-qual-206-host-002__catalogue_search"
            ),
            "permission_mode": "dontAsk",
            "session_persistence": False,
            "maximum_turns": 2,
            "mcp_subtree_network_access_allowed": False,
            "mcp_subtree_network_sandbox": "macos-seatbelt-deny-network",
            "mcp_child_recognised_credentials_forwarded": False,
            "raw_host_output_published": False,
        },
        "runtime_binding": {
            "tracked_source_material_count": 16,
            "generated_first_party_closure": {
                "bytes": 1,
                "file_count": 1,
                "manifest_sha256": "1" * 64,
                "reference_manifest_sha256": "1" * 64,
                "reference_matches_current": True,
            },
            "installed_dependency_closure": {
                "bytes": 1,
                "entry_count": 1,
                "manifest_sha256": "2" * 64,
            },
            "node_runtime": {
                "bytes": 50320,
                "sha256": (
                    "1ef99ea25fe70c9b67e7efe768ef8ee22148d3cabc703db6131b57aeb617d040"
                ),
                "version": "26.7.0",
            },
            "network_sandbox": {
                "bytes": 102560,
                "profile_sha256": (
                    "0a5222386587bf836d30a070bd759c0194f999bf5503ba76c6c0f8cb84b19db2"
                ),
                "sha256": (
                    "8290e4be7387a0df83cd1559e86afd880464f269450573d012795761fe298f16"
                ),
            },
            "network_sandbox_probe": {
                "fsync_pass": True,
                "loopback_denied": True,
                "probe_script_sha256": (
                    "c6540fbbb22b0c3b965a6ce5dceb81eb2064e99ceb324c122db31ad6f0a8f426"
                ),
            },
            "complete_first_party_generated_closure_binding": False,
            "third_party_runtime_binding": "installed-closure-digest-plus-pnpm-lockfile",
            "complete_runtime_source_binding": False,
            "dependency_materials_stable": True,
            "runtime_materials_stable": True,
            "source_checkout_stable": True,
        },
        "claims": {
            "host_002_catalogue_search": True,
            "exact_five_model_capability": False,
            "remote_http_interoperability": False,
            "live_geospatial_provider": False,
            "registry_publication": False,
            "activation": False,
            "deployment": False,
            "release": False,
        },
        "private_capture": {
            "retained": True,
            "published": False,
            "manifest_sha256": "3" * 64,
            "stdout_sha256": "4" * 64,
            "stderr_sha256": hashlib.sha256(b"").hexdigest(),
        },
        "boundary": BOUNDARY,
    }


def session_summary() -> dict[str, object]:
    return {
        "schema": "gis-ai-go.qual-206-claude-capability-session.v1",
        "run_id": "12345678-1234-4234-8234-123456789abc",
        "session_id": "87654321-4321-4321-8321-cba987654321",
        "slot": "session-1",
        "source_commit": COMMIT,
        "case_id": "QUAL-206-HOST-002",
        "session_profile": "modern-session",
        "protocol_session_status": "passed",
        "capability_scored": False,
        "mcp_subtree_network_access_allowed": False,
        "mcp_subtree_network_sandbox": "macos-seatbelt-deny-network",
        "request": {
            "observed": True,
            "valid": True,
            "parameters_bytes": 29,
            "parameters_sha256": SHA,
            "global_claim_bytes": 194,
            "global_claim_sha256": "1" * 64,
        },
        "response": {
            "observed": True,
            "contract_valid": True,
            "case_id": "QUAL-206-HOST-002",
            "deterministic_result_valid": True,
            "expected_record_id_match": True,
            "expected_title_match": True,
            "output_contract_valid": True,
            "receipt_id": RECEIPT,
            "receipt_present": True,
            "receipt_verification_valid": True,
            "record_id": "hmlr:dataset:inspire-index-polygons",
            "structured_plain_text_parity": True,
            "title": "Index polygons spatial data (INSPIRE)",
        },
    }


class ClaudeCapabilityContractsTest(unittest.TestCase):
    def test_node_harness_regressions_are_repository_gated(self) -> None:
        environment = os.environ.copy()
        for name in RECOGNISED_CREDENTIAL_VARIABLES:
            environment.pop(name, None)
        completed = subprocess.run(
            [
                "node",
                "--test",
                "tests/interoperability/test_qual_206_claude_capability_harness.mjs",
            ],
            cwd=ROOT,
            check=False,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120,
        )
        self.assertEqual(
            completed.returncode,
            0,
            f"{completed.stdout}\n{completed.stderr}",
        )
        summary = {
            match.group(1): int(match.group(2))
            for match in re.finditer(
                r"^(?:ℹ|#)\s+(tests|pass|fail|skipped)\s+(\d+)$",
                completed.stdout,
                re.MULTILINE,
            )
        }
        expected = {
            "tests": 16,
            "pass": 16 if sys.platform == "darwin" else 4,
            "fail": 0,
            "skipped": 0 if sys.platform == "darwin" else 12,
        }
        self.assertEqual(summary, expected, completed.stdout)

    def test_public_projection_is_closed_and_pass_only(self) -> None:
        check = validator(PUBLIC_SCHEMA_PATH)
        document = public_projection()
        self.assertEqual(list(check.iter_errors(document)), [])
        mutations: list[tuple[str, dict[str, object]]] = []
        for label, path, value in (
            ("exact-five inflation", ("claims", "exact_five_model_capability"), True),
            ("remote inflation", ("claims", "remote_http_interoperability"), True),
            ("unverified receipt", ("result", "receipt_verification_valid"), False),
            ("model mismatch", ("result", "model_output_match"), False),
            ("zero model input", ("result", "input_tokens"), 0),
            ("reported-turn under-count", ("result", "num_turns"), 2),
            ("second call", ("transport", "tool_call_count"), 2),
            ("built-in tools", ("isolation", "built_in_tools_available"), True),
            ("turn ceiling drift", ("isolation", "maximum_turns"), 1),
            (
                "permission alias drift",
                ("isolation", "claude_permission_alias"),
                "mcp__gis-ai-go-qual-206-host-002__catalogue.search",
            ),
            (
                "network access inflation",
                ("isolation", "mcp_subtree_network_access_allowed"),
                True,
            ),
        ):
            changed = copy.deepcopy(document)
            changed[path[0]][path[1]] = value  # type: ignore[index]
            mutations.append((label, changed))
        unexpected = copy.deepcopy(document)
        unexpected["unexpected_private_field"] = "not-published"
        mutations.append(("unknown private field", unexpected))
        failed_probe = copy.deepcopy(document)
        failed_probe["runtime_binding"]["network_sandbox_probe"][  # type: ignore[index]
            "loopback_denied"
        ] = False
        mutations.append(("failed network sandbox probe", failed_probe))
        for label, changed in mutations:
            with self.subTest(label=label):
                self.assertTrue(list(check.iter_errors(changed)))

    def test_private_session_requires_correlated_allowlisted_facts(self) -> None:
        check = validator(SESSION_SCHEMA_PATH)
        document = session_summary()
        self.assertEqual(list(check.iter_errors(document)), [])
        no_request = copy.deepcopy(document)
        no_request["request"] = {
            "observed": False,
            "valid": None,
            "parameters_bytes": None,
            "parameters_sha256": None,
            "global_claim_bytes": None,
            "global_claim_sha256": None,
        }
        no_request["response"] = {
            name: None for name in document["response"]  # type: ignore[index]
        }
        no_request["response"]["observed"] = False  # type: ignore[index]
        self.assertEqual(list(check.iter_errors(no_request)), [])
        false_claim = copy.deepcopy(document)
        false_claim["request"]["global_claim_sha256"] = None  # type: ignore[index]
        self.assertTrue(list(check.iter_errors(false_claim)))

    def test_private_run_schema_separates_login_from_api_budget(self) -> None:
        check = validator(PRIVATE_SCHEMA_PATH)
        document = {
            "schema": "gis-ai-go.qual-206-claude-capability-private-run.v1",
            "run_id": "12345678-1234-4234-8234-123456789abc",
            "source": {
                "commit": COMMIT,
                "tree": TREE,
                "repository_origin": "https://github.com/chris-page-gov/gis-ai-go.git",
                "local_origin_main_match": True,
                "protected_main_verification": "external-publication-gate",
            },
            "case": {
                "id": "QUAL-206-HOST-002",
                "corpus_bytes": 1,
                "corpus_sha256": SHA,
                "prompt_bytes": 1,
                "prompt_sha256": SHA,
                "prompt_text_repeated_in_projection": False,
            },
            "host": {
                "name": "Claude Code",
                "version": "2.1.245",
                "executable_bytes": 376109392,
                "executable_sha256": (
                    "9f7c2260251765a18d0b35198669dacc1912f6e8129a3b01f6b58d93365ff1f1"
                ),
                "model_requested": "claude-sonnet-5",
                "auth_kind": "first-party-login",
                "api_budget_usd": None,
                "auth_preflight": {
                    "logged_in": True,
                    "api_provider": "firstParty",
                    "auth_method": "claude.ai",
                    "subscription_type": "pro",
                },
            },
            "execution": {
                "started_at": "2026-08-25T18:00:00.000Z",
                "finished_at": "2026-08-25T18:00:01.000Z",
                "command_sha256": SHA,
                "exit_code": 0,
                "signal": None,
                "interrupted_signal": None,
                "harness_classification": None,
                "stdout": {"bytes": 1, "limit_exceeded": False, "sha256": SHA},
                "stderr": {"bytes": 0, "limit_exceeded": False, "sha256": SHA},
                "output_schema_sha256": SHA,
                "built_in_tools_available": False,
                "allowed_mcp_tool": "mcp__gis-ai-go-qual-206-host-002__catalogue_search",
                "permission_mode": "dontAsk",
                "session_persistence": False,
                "maximum_turns": 2,
                "effort": "low",
                "process_group_absent": True,
                "spawned_process_executable_attested": True,
            },
            "private_files": {
                "mcp_config": {"name": "mcp.json", "bytes": 1, "sha256": SHA},
                "settings": {"name": "settings.json", "bytes": 1, "sha256": SHA},
                "stdout": {
                    "name": "stdout.json",
                    "bytes": 1,
                    "limit_exceeded": False,
                    "sha256": SHA,
                },
                "stderr": {
                    "name": "stderr.log",
                    "bytes": 0,
                    "limit_exceeded": False,
                    "sha256": SHA,
                },
                "observer_directory": "observer",
            },
            "isolation": {
                "private_root_mode": "0700",
                "private_file_mode": "0600",
                "workspace_empty": True,
                "mcp_subtree_network_access_allowed": False,
                "mcp_subtree_network_sandbox": "macos-seatbelt-deny-network",
                "mcp_child_recognised_credentials_forwarded": False,
                "raw_material_published": False,
            },
            "runtime_binding": {
                "tracked_source_materials": [
                    {"bytes": 1, "path": path, "sha256": SHA} for path in TRACKED
                ],
                "generated_first_party_closure": {
                    "bytes": 1,
                    "file_count": 1,
                    "manifest_sha256": SHA,
                    "reference_manifest_sha256": SHA,
                    "reference_matches_current": True,
                },
                "installed_dependency_closure": {
                    "bytes": 1,
                    "entry_count": 1,
                    "manifest_sha256": "2" * 64,
                },
                "node_runtime": {
                    "bytes": 50320,
                    "path": "/opt/homebrew/Cellar/node/26.7.0/bin/node",
                    "sha256": (
                        "1ef99ea25fe70c9b67e7efe768ef8ee22148d3cabc703db6131b57aeb617d040"
                    ),
                    "version": "26.7.0",
                },
                "network_sandbox": {
                    "bytes": 102560,
                    "path": "/usr/bin/sandbox-exec",
                    "profile_sha256": (
                        "0a5222386587bf836d30a070bd759c0194f999bf5503ba76c6c0f8cb84b19db2"
                    ),
                    "sha256": (
                        "8290e4be7387a0df83cd1559e86afd880464f269450573d012795761fe298f16"
                    ),
                },
                "network_sandbox_probe": {
                    "fsync_pass": True,
                    "loopback_denied": True,
                    "probe_script_sha256": (
                        "c6540fbbb22b0c3b965a6ce5dceb81eb2064e99ceb324c122db31ad6f0a8f426"
                    ),
                },
                "complete_first_party_generated_closure_binding": False,
                "third_party_runtime_binding": (
                    "installed-closure-digest-plus-pnpm-lockfile"
                ),
                "complete_runtime_source_binding": False,
                "dependency_materials_stable": True,
                "runtime_materials_stable": True,
                "source_checkout_stable": True,
            },
        }
        self.assertEqual(list(check.iter_errors(document)), [])
        for classification in (
            "stdin-stream-failed",
            "stdout-capture-write-failed",
        ):
            with self.subTest(classification=classification):
                failure = copy.deepcopy(document)
                failure_execution = cast(dict[str, Any], failure["execution"])
                failure_execution["harness_classification"] = classification
                self.assertEqual(list(check.iter_errors(failure)), [])
        unknown_failure = copy.deepcopy(document)
        unknown_execution = cast(dict[str, Any], unknown_failure["execution"])
        unknown_execution["harness_classification"] = "unclassified-harness-failure"
        self.assertTrue(list(check.iter_errors(unknown_failure)))
        changed = copy.deepcopy(document)
        changed["host"]["api_budget_usd"] = "1.00"  # type: ignore[index]
        self.assertTrue(list(check.iter_errors(changed)))
        api_key = copy.deepcopy(document)
        api_key_host = cast(dict[str, Any], api_key["host"])
        api_key_auth = cast(dict[str, Any], api_key_host["auth_preflight"])
        api_key_host["auth_kind"] = "api-key"
        api_key_host["api_budget_usd"] = "1.00"
        api_key_auth["auth_method"] = "api-key-environment"
        api_key_auth["subscription_type"] = None
        self.assertEqual(list(check.iter_errors(api_key)), [])
        zero_budget = copy.deepcopy(api_key)
        zero_budget["host"]["api_budget_usd"] = "0.00"  # type: ignore[index]
        self.assertTrue(list(check.iter_errors(zero_budget)))

    def test_model_output_must_match_the_observed_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as value:
            root = Path(value)
            os.chmod(root, 0o700)
            output = {
                "type": "result",
                "subtype": "success",
                "is_error": False,
                "permission_denials": [],
                "num_turns": 3,
                "usage": {
                    "input_tokens": 3,
                    "cache_creation_input_tokens": 5,
                    "cache_read_input_tokens": 7,
                    "output_tokens": 11,
                },
                "modelUsage": {
                    "claude-sonnet-5": {
                        "inputTokens": 3,
                        "cacheCreationInputTokens": 5,
                        "cacheReadInputTokens": 7,
                        "outputTokens": 11,
                    }
                },
                "structured_output": {
                    "record_id": "hmlr:dataset:inspire-index-polygons",
                    "title": "Index polygons spatial data (INSPIRE)",
                    "receipt_id": RECEIPT,
                },
            }
            stdout = json.dumps(output, separators=(",", ":")).encode()
            stderr = b""
            for name, raw in (("stdout.json", stdout), ("stderr.log", stderr)):
                path = root / name
                path.write_bytes(raw)
                os.chmod(path, 0o600)
            manifest = {
                "execution": {
                    "exit_code": 0,
                    "signal": None,
                    "interrupted_signal": None,
                    "process_group_absent": True,
                    "spawned_process_executable_attested": True,
                    "harness_classification": None,
                    "stdout": {
                        "bytes": len(stdout),
                        "sha256": hashlib.sha256(stdout).hexdigest(),
                        "limit_exceeded": False,
                    },
                    "stderr": {
                        "bytes": 0,
                        "sha256": hashlib.sha256(stderr).hexdigest(),
                        "limit_exceeded": False,
                    },
                }
            }
            self.assertEqual(
                verifier.verify_output(root, manifest, RECEIPT)["receipt_id"],
                RECEIPT,
            )
            for label, field, value in (
                ("interrupted launcher", "interrupted_signal", "SIGTERM"),
                ("unattested process", "spawned_process_executable_attested", False),
            ):
                with self.subTest(label=label):
                    invalid_manifest = copy.deepcopy(manifest)
                    invalid_manifest["execution"][field] = value
                    with self.assertRaisesRegex(
                        verifier.CapabilityVerificationError,
                        "bounded client run",
                    ):
                        verifier.verify_output(root, invalid_manifest, RECEIPT)
            with self.assertRaisesRegex(
                verifier.CapabilityVerificationError,
                "does not match",
            ):
                verifier.verify_output(
                    root,
                    manifest,
                    f"gis-ai-go:evidence-receipt:sha256:{'e' * 64}",
                )
            invalid_outputs = []
            wrong_model = copy.deepcopy(output)
            wrong_model["modelUsage"] = {
                "claude-sonnet-4": wrong_model["modelUsage"]["claude-sonnet-5"]
            }
            invalid_outputs.append(("pinned model", wrong_model))
            zero_input = copy.deepcopy(output)
            for name in (
                "input_tokens",
                "cache_creation_input_tokens",
                "cache_read_input_tokens",
            ):
                zero_input["usage"][name] = 0
            for name in (
                "inputTokens",
                "cacheCreationInputTokens",
                "cacheReadInputTokens",
            ):
                zero_input["modelUsage"]["claude-sonnet-5"][name] = 0
            invalid_outputs.append(("positive input usage", zero_input))
            too_few_turns = copy.deepcopy(output)
            too_few_turns["num_turns"] = 2
            invalid_outputs.append(("exact reported-turn lifecycle", too_few_turns))
            non_integer_turns = copy.deepcopy(output)
            non_integer_turns["num_turns"] = 3.0
            invalid_outputs.append(("integer reported-turn count", non_integer_turns))
            extra_turn = copy.deepcopy(output)
            extra_turn["num_turns"] = 4
            invalid_outputs.append(("extra reported turn", extra_turn))
            for label, invalid in invalid_outputs:
                with self.subTest(label=label):
                    invalid_raw = json.dumps(invalid, separators=(",", ":")).encode()
                    (root / "stdout.json").write_bytes(invalid_raw)
                    os.chmod(root / "stdout.json", 0o600)
                    manifest["execution"]["stdout"] = {
                        "bytes": len(invalid_raw),
                        "sha256": hashlib.sha256(invalid_raw).hexdigest(),
                        "limit_exceeded": False,
                    }
                    with self.assertRaisesRegex(
                        verifier.CapabilityVerificationError,
                        "Claude final.*output",
                    ):
                        verifier.verify_output(root, manifest, RECEIPT)

    @unittest.skipUnless(
        sys.platform == "darwin",
        "the accepted Claude capability runtime uses macOS Seatbelt",
    )
    def test_fake_capture_verifies_end_to_end_without_publication(self) -> None:
        before = sorted((ROOT / "tests/interoperability/evidence").iterdir())
        with tempfile.TemporaryDirectory(dir="/private/tmp") as value:
            base = Path(value)
            root = base / "capture"
            root.mkdir(mode=0o700)
            os.chmod(root, 0o700)
            executable_bytes, executable_sha256 = create_fake_capture(root)

            def test_source_boundary(manifest: dict[str, object]) -> None:
                binding = cast(dict[str, Any], manifest["runtime_binding"])
                materials = cast(
                    list[dict[str, Any]],
                    binding["tracked_source_materials"],
                )
                self.assertEqual({item["path"] for item in materials}, set(TRACKED))
                generated = cast(
                    dict[str, Any],
                    binding["generated_first_party_closure"],
                )
                self.assertTrue(generated["reference_matches_current"])
                self.assertEqual(
                    generated["manifest_sha256"],
                    generated["reference_manifest_sha256"],
                )
                self.assertEqual(
                    {
                        "bytes": generated["bytes"],
                        "file_count": generated["file_count"],
                        "manifest_sha256": generated["manifest_sha256"],
                    },
                    verifier.measure_generated_runtime_closure(),
                )
                self.assertEqual(
                    binding["installed_dependency_closure"],
                    verifier.measure_installed_dependency_closure(),
                )

            projection = verifier.verify_and_project(
                root,
                source_verifier=test_source_boundary,
                private_validator=fake_host_validator(
                    PRIVATE_SCHEMA_PATH,
                    executable_bytes=executable_bytes,
                    executable_sha256=executable_sha256,
                ),
                public_validator=fake_host_validator(
                    PUBLIC_SCHEMA_PATH,
                    executable_bytes=executable_bytes,
                    executable_sha256=executable_sha256,
                ),
            )
            self.assertEqual(projection["status"], "capability_pass")
            self.assertEqual(projection["result"]["model_reported"], "claude-sonnet-5")
            self.assertTrue(projection["result"]["model_usage_observed"])
            self.assertEqual(projection["transport"]["tool_call_count"], 1)
            self.assertFalse(projection["claims"]["deployment"])
        after = sorted((ROOT / "tests/interoperability/evidence").iterdir())
        self.assertEqual(after, before)

    def test_no_public_observation_is_added_by_the_harness_implementation(self) -> None:
        matches = sorted(
            (ROOT / "tests/interoperability/evidence").glob(
                "claude-code-2.1.245-host-002-capability-*.json"
            )
        )
        self.assertEqual(matches, [])


if __name__ == "__main__":
    unittest.main()
