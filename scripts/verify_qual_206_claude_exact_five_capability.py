#!/usr/bin/env python3
"""Verify one private Claude exact-five run and project only a path-free pass."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Callable, NoReturn

from jsonschema import Draft202012Validator

import verify_qual_206_claude_capability as host002
import verify_qual_206_claude_composite_observation as composite


ROOT = Path(__file__).resolve().parents[1]
PRIVATE_SCHEMA = (
    ROOT / "schemas/qual-206-claude-exact-five-capability-private-run-v1.schema.json"
)
SESSION_SCHEMA = (
    ROOT / "schemas/qual-206-claude-exact-five-capability-session-v1.schema.json"
)
EVENT_SCHEMA = ROOT / "schemas/qual-206-claude-composite-host-event-v1.schema.json"
EVENT_CAPTURE_SCHEMA = (
    ROOT / "schemas/qual-206-claude-composite-host-event-capture-v1.schema.json"
)
PUBLIC_SCHEMA = (
    ROOT / "schemas/qual-206-claude-exact-five-capability-evidence-v1.schema.json"
)
PROFILE = (
    ROOT
    / "tests/interoperability/fixtures/qual_206_claude_exact_five_profile.v1.json"
)
OBSERVER = ROOT / "scripts/qual_206_claude_stdio_observer.mjs"
RESULT_VERIFIER = ROOT / "scripts/verify_qual_206_claude_exact_five_results.mjs"
EVIDENCE_DIRECTORY = ROOT / "tests/interoperability/evidence"
PINNED_MODEL = "claude-sonnet-5"
PROFILE_ID = "exact-five-v1"
CASE_ID = "QUAL-206-CLAUDE-EXACT-FIVE-V1"
SERVER_NAME = "gis-ai-go-qual-206-exact-five-v1"
PROTOCOL = "2026-07-28"
MAXIMUM_AGENTIC_TURNS = 10
MINIMUM_CLAUDE_REPORTED_TURNS = 3
MAXIMUM_CLAUDE_REPORTED_TURNS = MAXIMUM_AGENTIC_TURNS + 1
TURN_COUNT_SEMANTICS = (
    "claude-code-2.1.245-cli-configured-max-turns-ten-reported-num-turns-at-most-eleven"
)
OPERATIONS = (
    "catalogue.search",
    "catalogue.describe",
    "selection.resolve",
    "data.query",
    "evidence.inspect",
)
PERMISSION_ALIASES = (
    "mcp__gis-ai-go-qual-206-exact-five-v1__catalogue_search",
    "mcp__gis-ai-go-qual-206-exact-five-v1__catalogue_describe",
    "mcp__gis-ai-go-qual-206-exact-five-v1__selection_resolve",
    "mcp__gis-ai-go-qual-206-exact-five-v1__data_query",
    "mcp__gis-ai-go-qual-206-exact-five-v1__evidence_inspect",
)
OUTPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "profile",
        "operation_order",
        "receipt_ids",
        "inspected_search_receipt_id",
    ],
    "properties": {
        "profile": {"const": PROFILE_ID},
        "operation_order": {"const": list(OPERATIONS)},
        "receipt_ids": {
            "type": "object",
            "additionalProperties": False,
            "required": list(OPERATIONS),
            "properties": {
                operation: {
                    "type": "string",
                    "pattern": (
                        "^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$"
                    ),
                }
                for operation in OPERATIONS
            },
        },
        "inspected_search_receipt_id": {
            "type": "string",
            "pattern": "^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$",
        },
    },
}
RECEIPT_ID = re.compile(r"^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$")
EXPECTED_ROOT_NAMES = {
    "mcp.json",
    "observer",
    "run-manifest.json",
    "settings.json",
    "stderr.log",
    "stdout.json",
    "workspace",
}
EXPECTED_SESSION_FILES = {
    "events.jsonl",
    "exact-five-capability.json",
    "exact-five-results.json",
    "manifest.json",
}
TRACKED_EXACT_FIVE_CAPABILITY_MATERIALS = {
    "package.json",
    "pnpm-lock.yaml",
    "schemas/qual-206-claude-exact-five-capability-evidence-v1.schema.json",
    "schemas/qual-206-claude-exact-five-capability-private-run-v1.schema.json",
    "schemas/qual-206-claude-exact-five-capability-session-v1.schema.json",
    "schemas/qual-206-claude-composite-host-event-capture-v1.schema.json",
    "schemas/qual-206-claude-composite-host-event-v1.schema.json",
    "scripts/qual_206_claude_capability_harness.mjs",
    "scripts/qual_206_claude_exact_five_capability_harness.mjs",
    "scripts/qual_206_claude_runtime_closure.mjs",
    "scripts/qual_206_claude_stdio_observer.mjs",
    "scripts/qual_206_exact_five_event_collector.mjs",
    "scripts/verify_qual_206_claude_exact_five_capability.py",
    "scripts/verify_qual_206_claude_exact_five_results.mjs",
    "scripts/verify_qual_206_claude_composite_observation.py",
    "tests/interoperability/fixtures/qual_206_claude_exact_five_profile.v1.json",
    "tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs",
    "tests/interoperability/fixtures/qual_206_strict_modern_event_server.mjs",
}
BOUNDARY = (
    "One bounded Claude Code 2.1.245 model-mediated exact-five-v1 observation over "
    "local MCP 2026-07-28 STDIO with a deterministic synthetic provider fixture. "
    "This does not prove remote HTTP interoperability, a live geospatial provider, "
    "registry publication, activation, deployment or release."
)


class ExactFiveCapabilityVerificationError(ValueError):
    """The private exact-five run did not satisfy the pass contract."""


def fail(message: str) -> NoReturn:
    raise ExactFiveCapabilityVerificationError(message)


def _host_call(function: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    try:
        return function(*args, **kwargs)
    except (
        host002.CapabilityVerificationError,
        composite.VerificationError,
    ) as error:
        raise ExactFiveCapabilityVerificationError(str(error)) from error


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_line(value: dict[str, Any]) -> bytes:
    return _host_call(host002.canonical_line, value)


def strict_object(raw: bytes, *, label: str, newline: bool = False) -> dict[str, Any]:
    return _host_call(host002.strict_object, raw, label=label, newline=newline)


def schema_validator(path: Path) -> Draft202012Validator:
    return _host_call(host002.schema_validator, path)


def validate(
    validator: Draft202012Validator,
    value: dict[str, Any],
    *,
    label: str,
) -> None:
    _host_call(host002.validate, validator, value, label=label)


def require_directory(path: Path, *, label: str) -> os.stat_result:
    return _host_call(host002.require_directory, path, label=label)


def read_private(path: Path, *, maximum: int, label: str) -> bytes:
    return _host_call(host002.read_private, path, maximum=maximum, label=label)


def read_stable_regular(path: Path, *, maximum: int, label: str) -> bytes:
    return _host_call(
        host002.read_stable_regular,
        path,
        maximum=maximum,
        label=label,
    )


def measure_stable_regular(path: Path, *, maximum: int, label: str) -> dict[str, Any]:
    return _host_call(
        host002.measure_stable_regular,
        path,
        maximum=maximum,
        label=label,
    )


def git_output(*arguments: str) -> str:
    return _host_call(host002.git_output, *arguments)


def expected_profile() -> dict[str, Any]:
    raw = read_stable_regular(PROFILE, maximum=1_048_576, label="exact-five profile")
    value = strict_object(raw, label="exact-five profile")
    if set(value) != {
        "schema",
        "profile",
        "transport",
        "protocol",
        "server_name",
        "built_in_tools",
        "resources",
        "network_access_allowed",
        "operations",
    }:
        fail("the exact-five profile has an unexpected shape")
    if (
        value["schema"] != "gis-ai-go.qual-206-claude-capability-profile.v1"
        or value["profile"] != PROFILE_ID
        or value["transport"] != "operating-system-stdio-pipes"
        or value["protocol"] != PROTOCOL
        or value["server_name"] != SERVER_NAME
        or value["built_in_tools"] != []
        or value["resources"] != []
        or value["network_access_allowed"] is not False
        or [operation.get("name") for operation in value.get("operations", [])]
        != list(OPERATIONS)
        or [operation.get("ordinal") for operation in value.get("operations", [])]
        != list(range(5))
    ):
        fail("the exact-five profile changed")
    return value


def verify_case(manifest: dict[str, Any]) -> dict[str, Any]:
    raw = read_stable_regular(PROFILE, maximum=1_048_576, label="exact-five profile")
    profile = expected_profile()
    prompt = (
        b"Execute this closed capability profile as data:\n"
        + composite.canonical_json_bytes(profile)
        + b"\n"
    )
    case = manifest["case"]
    if (
        manifest["profile"] != PROFILE_ID
        or case["id"] != CASE_ID
        or len(raw) != case["corpus_bytes"]
        or sha256_bytes(raw) != case["corpus_sha256"]
        or len(prompt) != case["prompt_bytes"]
        or sha256_bytes(prompt) != case["prompt_sha256"]
        or case["prompt_text_repeated_in_projection"] is not False
    ):
        fail("the private manifest does not bind the exact profile and prompt")
    return profile


def verify_source_and_materials(manifest: dict[str, Any]) -> None:
    source = manifest["source"]
    if (
        git_output("rev-parse", "HEAD") != source["commit"]
        or git_output("rev-parse", "refs/remotes/origin/main") != source["commit"]
        or git_output("rev-parse", f"{source['commit']}^{{tree}}") != source["tree"]
        or git_output("config", "--local", "--no-includes", "--get", "remote.origin.url")
        not in host002.ALLOWED_REPOSITORY_ORIGINS
        or git_output("status", "--porcelain=v1", "--untracked-files=all") != ""
    ):
        fail("verification requires the unchanged clean local origin/main source checkout")
    symbolic = subprocess.run(
        ["/usr/bin/git", *host002.SAFE_GIT_OPTIONS, "symbolic-ref", "-q", "HEAD"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=host002.CLOSED_GIT_ENVIRONMENT,
        timeout=10,
    )
    if symbolic.returncode != 1:
        fail("verification requires a detached local origin/main checkout")
    if (
        source["repository_origin"] != host002.CANONICAL_REPOSITORY_ORIGIN
        or source["local_origin_main_match"] is not True
        or source["protected_main_verification"] != "external-publication-gate"
    ):
        fail("source claims exceed the locally verifiable boundary")

    binding = manifest["runtime_binding"]
    materials = binding["tracked_source_materials"]
    paths = [item["path"] for item in materials]
    if (
        len(paths) != len(set(paths))
        or set(paths) != TRACKED_EXACT_FIVE_CAPABILITY_MATERIALS
    ):
        fail("tracked runtime materials do not contain the exact verifier closure")
    for item in materials:
        path = ROOT / item["path"]
        measured = measure_stable_regular(
            path,
            maximum=536_870_912,
            label=f"runtime material {item['path']}",
        )
        if measured != {"bytes": item["bytes"], "sha256": item["sha256"]}:
            fail(f"runtime material changed: {item['path']}")
        blob = subprocess.run(
            [
                "/usr/bin/git",
                *host002.SAFE_GIT_OPTIONS,
                "show",
                f"{source['commit']}:{item['path']}",
            ],
            cwd=ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=host002.CLOSED_GIT_ENVIRONMENT,
            timeout=10,
        )
        if blob.returncode != 0 or sha256_bytes(blob.stdout) != item["sha256"]:
            fail(f"runtime material is not source-bound: {item['path']}")

    generated = binding["generated_first_party_closure"]
    current = _host_call(host002.measure_generated_runtime_closure)
    installed = _host_call(host002.measure_installed_dependency_closure)
    if (
        current
        != {
            "bytes": generated["bytes"],
            "file_count": generated["file_count"],
            "manifest_sha256": generated["manifest_sha256"],
        }
        or generated["reference_manifest_sha256"] != generated["manifest_sha256"]
        or generated["reference_matches_current"] is not True
        or installed != binding["installed_dependency_closure"]
        or binding["complete_first_party_generated_closure_binding"] is not False
        or binding["third_party_runtime_binding"]
        != "installed-closure-digest-plus-pnpm-lockfile"
        or binding["complete_runtime_source_binding"] is not False
        or binding["dependency_materials_stable"] is not True
        or binding["runtime_materials_stable"] is not True
        or binding["source_checkout_stable"] is not True
    ):
        fail("generated or dependency runtime binding changed")


def verify_private_configuration(
    private_root: Path,
    manifest: dict[str, Any],
    mcp_raw: bytes,
    settings_raw: bytes,
) -> None:
    if (
        not mcp_raw.endswith(b"\n")
        or not settings_raw.endswith(b"\n")
        or b"\n" in mcp_raw[:-1]
        or b"\n" in settings_raw[:-1]
    ):
        fail("private MCP and settings files must be canonical LF-terminated JSON")
    mcp = strict_object(mcp_raw, label="private MCP configuration", newline=True)
    settings = strict_object(settings_raw, label="private Claude settings", newline=True)
    if canonical_line(mcp) != mcp_raw or canonical_line(settings) != settings_raw:
        fail("private MCP or settings configuration is not canonical JSON")
    expected_settings = {
        "autoMemoryEnabled": False,
        "disableAllHooks": True,
        "disabledMcpjsonServers": [],
        "enableAllProjectMcpServers": False,
        "enabledMcpjsonServers": [SERVER_NAME],
        "permissions": {
            "allow": list(PERMISSION_ALIASES),
            "deny": [],
            "defaultMode": "dontAsk",
        },
    }
    if settings != expected_settings:
        fail("private Claude settings widen or change the exact-five profile")
    if set(mcp) != {"mcpServers"} or set(mcp["mcpServers"]) != {SERVER_NAME}:
        fail("private MCP configuration does not contain exactly one server")
    server = mcp["mcpServers"][SERVER_NAME]
    if (
        not isinstance(server, dict)
        or set(server) != {"type", "command", "args"}
        or server["type"] != "stdio"
        or server["command"] != str(host002.SANDBOX_EXEC)
        or not isinstance(server["args"], list)
        or not all(isinstance(value, str) for value in server["args"])
    ):
        fail("private MCP server definition is not the exact STDIO projection")
    unset_arguments = [
        value
        for name in (
            *host002.RECOGNISED_CREDENTIAL_VARIABLES,
            *host002.CLAUDE_CLIENT_ONLY_MCP_VARIABLES,
        )
        for value in ("-u", name)
    ]
    prefix = [
        "-p",
        host002.NETWORK_SANDBOX_PROFILE,
        "/usr/bin/env",
        *unset_arguments,
        "GIS_AI_GO_QUAL_206_EVENT_CAPTURE=1",
        f"GIS_AI_GO_QUAL_206_MCP_NETWORK_SANDBOX={host002.NETWORK_SANDBOX}",
        "GIS_AI_GO_QUAL_206_HOST_ATTESTATION=outer-harness-spawn-executable",
    ]
    args = server["args"]
    if args[: len(prefix)] != prefix:
        fail("private MCP child does not unset the exact closed variable set")
    tail = args[len(prefix) :]
    if len(tail) != 15:
        fail("private MCP observer command has an unexpected argument count")
    node_path = Path(tail[0])
    node = measure_stable_regular(
        node_path,
        maximum=1_048_576,
        label="Node runtime executable",
    )
    sandbox = measure_stable_regular(
        host002.SANDBOX_EXEC,
        maximum=1_048_576,
        label="macOS Seatbelt executable",
    )
    expected_tail = [
        str(node_path),
        str(OBSERVER),
        "--claude-exact-five-v1-capability-observation-only",
        "--capture-root",
        str(private_root / "observer"),
        "--run-id",
        manifest["run_id"],
        "--client",
        "claude-code-2.1.245-exact-five-v1",
        "--source-commit",
        manifest["source"]["commit"],
        "--expected-parent-sha256",
        manifest["host"]["executable_sha256"],
        "--expected-parent-bytes",
        str(manifest["host"]["executable_bytes"]),
    ]
    if tail != expected_tail:
        fail("private MCP observer command widens or changes its Seatbelt profile")
    expected_sandbox = {
        "bytes": host002.EXPECTED_SANDBOX_EXEC_BYTES,
        "path": str(host002.SANDBOX_EXEC),
        "profile_sha256": sha256_bytes(host002.NETWORK_SANDBOX_PROFILE.encode()),
        "sha256": host002.EXPECTED_SANDBOX_EXEC_SHA256,
    }
    expected_probe = {
        "fsync_pass": True,
        "loopback_denied": True,
        "probe_script_sha256": host002.EXPECTED_NETWORK_SANDBOX_PROBE_SHA256,
    }
    if (
        str(node_path) != manifest["runtime_binding"]["node_runtime"]["path"]
        or node
        != {
            "bytes": host002.EXPECTED_NODE_BYTES,
            "sha256": host002.EXPECTED_NODE_SHA256,
        }
        or manifest["runtime_binding"]["node_runtime"]
        != {
            "bytes": host002.EXPECTED_NODE_BYTES,
            "path": str(node_path),
            "sha256": host002.EXPECTED_NODE_SHA256,
            "version": "26.7.0",
        }
        or sandbox
        != {
            "bytes": host002.EXPECTED_SANDBOX_EXEC_BYTES,
            "sha256": host002.EXPECTED_SANDBOX_EXEC_SHA256,
        }
        or manifest["runtime_binding"]["network_sandbox"] != expected_sandbox
        or manifest["runtime_binding"]["network_sandbox_probe"] != expected_probe
    ):
        fail("private MCP configuration does not bind the accepted runtimes")
    output_schema_sha256 = sha256_bytes(composite.canonical_json_bytes(OUTPUT_SCHEMA))
    if manifest["execution"]["output_schema_sha256"] != output_schema_sha256:
        fail("Claude output schema digest does not bind the exact-five projection")


def verify_event_log(
    raw: bytes,
    event_manifest: dict[str, Any],
    *,
    slot: str,
    run_manifest: dict[str, Any],
    event_validator: Draft202012Validator,
) -> tuple[list[dict[str, Any]], Counter[str], Counter[str], dict[str, int]]:
    if not raw or not raw.endswith(b"\n") or raw.endswith(b"\r\n"):
        fail(f"{slot} event log is not LF-terminated")
    encoded_lines = [line + b"\n" for line in raw[:-1].split(b"\n")]
    previous: str | None = None
    events: list[dict[str, Any]] = []
    methods: Counter[str] = Counter()
    operations: Counter[str] = Counter()
    for index, encoded in enumerate(encoded_lines):
        value = strict_object(encoded[:-1], label=f"{slot} event {index}")
        if composite.canonical_json_bytes(value) != encoded[:-1]:
            fail(f"{slot} event {index} is not canonical JSON")
        validate(event_validator, value, label=f"{slot} event {index}")
        if (
            value["sequence"] != index
            or value["slot"] != slot
            or value["run_id"] != run_manifest["run_id"]
            or value["previous_event_sha256"] != previous
        ):
            fail(f"{slot} event chain context is invalid")
        core = dict(value)
        supplied = core.pop("event_sha256")
        expected = composite.domain_separated_sha256(core)
        if not hmac.compare_digest(supplied, expected):
            fail(f"{slot} event {index} has an invalid content address")
        previous = supplied
        events.append(value)
        if value["event"] == "request":
            methods[value["method"]] += 1
            if value["method"] == "tools/call":
                operations[value["operation"]] += 1

    if not events:
        fail(f"{slot} event log is empty")
    start, end = events[0], events[-1]
    if (
        start.get("event") != "lifecycle"
        or start.get("phase") != "session-start"
        or end.get("event") != "lifecycle"
        or end.get("phase") != "session-end"
        or start["source_commit"] != run_manifest["source"]["commit"]
        or start["immediate_parent"]["sha256"]
        != run_manifest["host"]["executable_sha256"]
        or start["immediate_parent"]["bytes"]
        != run_manifest["host"]["executable_bytes"]
        or not all(start["source_checkout"].values())
        or start["mcp_subtree_network_access_allowed"] is not False
        or start["mcp_subtree_network_sandbox"] != host002.NETWORK_SANDBOX
    ):
        fail(f"{slot} does not bind the clean source, host and network boundary")
    if (
        end["protocol_session_status"] != "passed"
        or end["session_profile"] == "invalid"
        or end["capability_scored"] is not False
        or end["host_capability"] is not False
        or end["source_binding_ready"] is not False
        or end["anomaly_count"] != 0
        or end["pending_request_count"] != 0
        or end["stderr_bytes"] != 0
        or end["request_count"] != sum(methods.values())
    ):
        fail(f"{slot} session did not close cleanly")
    responses = [event for event in events if event["event"] == "response"]
    requests = [event for event in events if event["event"] == "request"]
    if len(responses) != len(requests) or end["response_count"] != len(responses):
        fail(f"{slot} request and response counts differ")
    if any(
        response["correlation"] != "matched" or response["contract_valid"] is not True
        for response in responses
    ):
        fail(f"{slot} contains an invalid or uncorrelated response")
    requests_by_digest = {
        request["request_id_sha256"]: request for request in requests
    }
    presented_fields = {
        "presented_direction",
        "presented_frame_bytes",
        "presented_frame_sha256",
        "presented_result_sha256",
    }
    for response in responses:
        request = requests_by_digest.get(response["request_id_sha256"])
        has_presented_fields = bool(set(response) & presented_fields)
        if request is not None and request["method"] == "tools/list":
            if (
                not presented_fields <= set(response)
                or response["presented_direction"] != "observer-to-host"
                or response["presented_frame_sha256"] == response["frame_sha256"]
            ):
                fail(f"{slot} does not bind its host-facing tools projection")
        elif has_presented_fields:
            fail(f"{slot} projects a response other than tools/list")
    audits = [event for event in events if event["event"] == "audit"]
    audit_kinds = [event["audit_kind"] for event in audits]
    no_operation_audits = [
        "provider-egress-guard-ready",
        "provider-egress-guard-summary",
        "session-summary",
    ]
    exact_five_audits = [
        "provider-egress-guard-ready",
        "provider-transport-started",
        "provider-egress-guard-summary",
        "session-summary",
    ]
    if audit_kinds not in (no_operation_audits, exact_five_audits):
        fail(f"{slot} does not contain the exact fixed-provider audit sequence")
    if any(event["contract_valid"] is not True for event in audits):
        fail(f"{slot} contains an invalid fixture audit")
    has_provider_start = audit_kinds == exact_five_audits
    provider_start = audits[1] if has_provider_start else None
    guard_summary = audits[2] if has_provider_start else audits[1]
    session_summary = audits[3] if has_provider_start else audits[2]
    audit = {
        "guarded_provider_api_invocations": guard_summary[
            "guarded_api_invocation_count"
        ],
        "provider_transport_calls": session_summary["provider_transport_calls"],
        "aborted_provider_calls": session_summary["aborted_provider_calls"],
        "ledger_event_count": session_summary["ledger_event_count"],
    }
    if (
        (provider_start is not None and provider_start["ordinal"] != 1)
        or audit
        != (
            {
                "guarded_provider_api_invocations": 0,
                "provider_transport_calls": 1,
                "aborted_provider_calls": 0,
                "ledger_event_count": 4,
            }
            if has_provider_start
            else {
                "guarded_provider_api_invocations": 0,
                "provider_transport_calls": 0,
                "aborted_provider_calls": 0,
                "ledger_event_count": 0,
            }
        )
        or any(event["audit_kind"] == "provider-egress-guard-blocked" for event in audits)
    ):
        fail(f"{slot} widened or changed the deterministic provider boundary")
    if event_manifest["event_log"] != {
        "bytes": len(raw),
        "event_count": len(events),
        "last_event_sha256": previous,
        "sha256": sha256_bytes(raw),
    }:
        fail(f"{slot} manifest does not bind its event log")
    return events, methods, operations, audit


def independently_verify_results(
    result_raw: bytes,
    *,
    node_path: str,
) -> dict[str, Any]:
    result = subprocess.run(
        [
            str(host002.SANDBOX_EXEC),
            "-p",
            host002.NETWORK_SANDBOX_PROFILE,
            node_path,
            str(RESULT_VERIFIER),
        ],
        cwd=ROOT,
        check=False,
        input=result_raw,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=host002.CLOSED_GIT_ENVIRONMENT,
        timeout=30,
    )
    if result.returncode != 0 or result.stderr:
        fail("independent exact-five result verification failed")
    verified = strict_object(
        result.stdout,
        label="independent exact-five result verification",
        newline=True,
    )
    if canonical_line(verified) != result.stdout:
        fail("independent exact-five result verification is not canonical")
    if set(verified) != {
        "schema",
        "profile",
        "run_id",
        "session_id",
        "discovery_count",
        "tools_list_count",
        "resources_advertised",
        "tool_schema_projection",
        "presented_tools_result_sha256",
        "operation_order",
        "operations",
        "inspection_relationship",
        "result_material_sha256",
    } or verified["schema"] != (
        "gis-ai-go.qual-206-claude-exact-five-results-verification.v1"
    ):
        fail("independent exact-five result verification widened its output")
    return verified


def _expected_arguments(profile: dict[str, Any], receipt_id: str) -> list[dict[str, Any]]:
    return [
        *[operation["arguments"] for operation in profile["operations"][:4]],
        {"receipt_id": receipt_id},
    ]


def verify_sessions(
    observer_root: Path,
    run_manifest: dict[str, Any],
    profile: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    Counter[str],
    Counter[str],
    dict[str, int],
    dict[str, Any],
    dict[str, int],
]:
    require_directory(observer_root, label="observer root")
    names = set(os.listdir(observer_root))
    claim_name = "exact-five-v1.claim.json"
    if claim_name not in names:
        fail("observer root has no global exact-five claim")
    slots = sorted(name for name in names if re.fullmatch(r"session-[123]", name))
    if names != set(slots) | {claim_name} or not slots:
        fail("observer root contains an unexpected entry")
    claim_raw = read_private(
        observer_root / claim_name,
        maximum=1_024,
        label="global exact-five claim",
    )
    claim = strict_object(claim_raw, label="global exact-five claim", newline=True)
    if (
        set(claim) != {"schema", "profile", "run_id", "session_id"}
        or claim["schema"]
        != "gis-ai-go.qual-206-claude-exact-five-capability-claim.v1"
        or claim["profile"] != PROFILE_ID
        or claim["run_id"] != run_manifest["run_id"]
    ):
        fail("global exact-five claim is invalid")

    event_validator = schema_validator(EVENT_SCHEMA)
    capture_validator = schema_validator(EVENT_CAPTURE_SCHEMA)
    session_validator = schema_validator(SESSION_SCHEMA)
    summaries: list[dict[str, Any]] = []
    total_methods: Counter[str] = Counter()
    total_operations: Counter[str] = Counter()
    total_audit = Counter[str]()
    protocol_facts = Counter[str]()
    independent: dict[str, Any] | None = None
    seen_session_ids: set[str] = set()
    for slot in slots:
        path = observer_root / slot
        require_directory(path, label=slot)
        if set(os.listdir(path)) != EXPECTED_SESSION_FILES:
            fail(f"{slot} does not contain its exact four private files")
        event_raw = read_private(
            path / "events.jsonl",
            maximum=8 * 1_048_576,
            label=f"{slot} events",
        )
        manifest_raw = read_private(
            path / "manifest.json",
            maximum=65_536,
            label=f"{slot} manifest",
        )
        summary_raw = read_private(
            path / "exact-five-capability.json",
            maximum=65_536,
            label=f"{slot} exact-five summary",
        )
        result_raw = read_private(
            path / "exact-five-results.json",
            maximum=6 * 1_048_576,
            label=f"{slot} exact-five result material",
        )
        summary = strict_object(
            summary_raw,
            label=f"{slot} exact-five summary",
            newline=True,
        )
        event_state = (path / "events.jsonl").lstat()
        manifest_state = (path / "manifest.json").lstat()
        composite_result = _host_call(
            composite.verify_session,
            slot=slot,
            event_file=composite.PrivateFile(
                raw=event_raw,
                identity=(event_state.st_dev, event_state.st_ino),
            ),
            manifest_file=composite.PrivateFile(
                raw=manifest_raw,
                identity=(manifest_state.st_dev, manifest_state.st_ino),
            ),
            event_validator=event_validator,
            capture_validator=capture_validator,
            expected_run_id=run_manifest["run_id"],
            expected_source_commit=run_manifest["source"]["commit"],
            expected_parent_sha256=run_manifest["host"]["executable_sha256"],
            expected_parent_bytes=run_manifest["host"]["executable_bytes"],
            exact_five_capability=bool(summary.get("operations")),
            allow_presented_tools_projection=True,
        )
        event_manifest = strict_object(
            manifest_raw,
            label=f"{slot} manifest",
            newline=True,
        )
        if canonical_line(event_manifest) != manifest_raw or canonical_line(summary) != summary_raw:
            fail(f"{slot} contains a non-canonical manifest or summary")
        validate(capture_validator, event_manifest, label=f"{slot} event manifest")
        validate(session_validator, summary, label=f"{slot} exact-five summary")
        material = summary["result_material"]
        if (
            material
            != {
                "name": "exact-five-results.json",
                "bytes": len(result_raw),
                "sha256": sha256_bytes(result_raw),
            }
        ):
            fail(f"{slot} summary does not bind its private result material")
        if (
            event_manifest["slot"] != slot
            or summary["slot"] != slot
            or event_manifest["session_id"] != summary["session_id"]
            or summary["session_id"] in seen_session_ids
            or summary["run_id"] != run_manifest["run_id"]
            or summary["source_commit"] != run_manifest["source"]["commit"]
            or summary["profile"] != PROFILE_ID
            or summary["mcp_subtree_network_access_allowed"] is not False
            or summary["mcp_subtree_network_sandbox"] != host002.NETWORK_SANDBOX
            or composite_result.session_id != summary["session_id"]
            or composite_result.profile != summary["session_profile"]
        ):
            fail(f"{slot} has inconsistent run or session identity")
        seen_session_ids.add(summary["session_id"])
        events, methods, operations, audit = verify_event_log(
            event_raw,
            event_manifest,
            slot=slot,
            run_manifest=run_manifest,
            event_validator=event_validator,
        )
        summaries.append(summary)
        total_methods.update(methods)
        total_operations.update(operations)
        total_audit.update(audit)
        independently_verified = independently_verify_results(
            result_raw,
            node_path=run_manifest["runtime_binding"]["node_runtime"]["path"],
        )
        presented_responses = [
            event
            for event in events
            if event["event"] == "response" and "presented_result_sha256" in event
        ]
        presented_result_sha256 = independently_verified[
            "presented_tools_result_sha256"
        ]
        if (
            (independently_verified["tools_list_count"] == 0 and (
                presented_responses or presented_result_sha256 is not None
            ))
            or (independently_verified["tools_list_count"] == 1 and (
                len(presented_responses) != 1
                or presented_result_sha256 is None
                or presented_responses[0]["presented_result_sha256"]
                != presented_result_sha256
            ))
        ):
            fail(f"{slot} event trace does not bind the independently verified projection")
        if (
            independently_verified["run_id"] != run_manifest["run_id"]
            or independently_verified["session_id"] != summary["session_id"]
            or independently_verified["profile"] != PROFILE_ID
            or independently_verified["resources_advertised"] != 0
            or independently_verified["tool_schema_projection"]
            != summary["tool_schema_projection"]
        ):
            fail(f"{slot} independent listing and result context is invalid")
        protocol_facts.update(
            {
                "discovery_count": independently_verified["discovery_count"],
                "tools_list_count": independently_verified["tools_list_count"],
                "resources_advertised": independently_verified["resources_advertised"],
            }
        )
        if summary["operations"]:
            if independent is not None:
                fail("the run contains more than one exact-five result session")
            independent = independently_verified
        elif (
            independently_verified["operations"] != []
            or independently_verified["operation_order"] != []
            or summary["global_claim"] != {"bytes": None, "sha256": None}
        ):
            fail(f"{slot} auxiliary session contains capability material")

    call_summaries = [summary for summary in summaries if summary["operations"]]
    if len(call_summaries) != 1 or independent is None:
        fail("the run does not contain exactly one complete exact-five session")
    call = call_summaries[0]
    if claim["session_id"] != call["session_id"]:
        fail("the global exact-five claim does not bind the call session")
    if (
        call["global_claim"]["bytes"] != len(claim_raw)
        or call["global_claim"]["sha256"] != sha256_bytes(claim_raw)
        or independent["run_id"] != run_manifest["run_id"]
        or independent["session_id"] != call["session_id"]
        or independent["profile"] != PROFILE_ID
        or independent["operation_order"] != list(OPERATIONS)
        or independent["tool_schema_projection"] is None
        or independent["tool_schema_projection"]["canonical_tools_sha256"]
        == independent["tool_schema_projection"]["presented_tools_sha256"]
    ):
        fail("the exact-five claim or independent result context is invalid")
    operation_summaries = call["operations"]
    independent_operations = independent["operations"]
    if len(operation_summaries) != 5 or len(independent_operations) != 5:
        fail("the exact-five session is incomplete")
    search_receipt_id = independent_operations[0]["receipt_id"]
    expected_arguments = _expected_arguments(profile, search_receipt_id)
    for ordinal, operation in enumerate(OPERATIONS):
        item = operation_summaries[ordinal]
        request = item["request"]
        response = item["response"]
        independent_response = independent_operations[ordinal]
        encoded_arguments = composite.canonical_json_bytes(expected_arguments[ordinal])
        if (
            item["ordinal"] != ordinal
            or request["ordinal"] != ordinal
            or request["operation"] != operation
            or request["expected_operation"] != operation
            or request["bytes"] != len(encoded_arguments)
            or request["sha256"] != sha256_bytes(encoded_arguments)
            or request["protocol_valid"] is not True
            or request["client_attribution_valid"] is not True
            or request["evidence_request_valid"] is not True
            or request["valid"] is not True
            or response["operation"] != operation
            or response["receipt_id"] != independent_response["receipt_id"]
            or any(
                response[name] is not True
                for name in (
                    "output_contract_valid",
                    "receipt_present",
                    "receipt_verification_valid",
                    "structured_plain_text_parity",
                )
            )
            or any(
                independent_response[name] is not True
                for name in (
                    "output_contract_valid",
                    "receipt_verification_valid",
                    "structured_plain_text_parity",
                )
            )
        ):
            fail(f"the {operation} request, response or receipt is invalid")
    receipts = [item["receipt_id"] for item in independent_operations]
    relationship = call["inspection_relationship"]
    independently_verified_relationship = independent["inspection_relationship"]
    if (
        len(set(receipts)) != 5
        or relationship["valid"] is not True
        or relationship["search_receipt_id"] != receipts[0]
        or relationship["inspected_receipt_id"] != receipts[0]
        or operation_summaries[-1]["response"]["inspected_receipt_id"] != receipts[0]
        or operation_summaries[-1]["response"]["inspection_relationship_valid"] is not True
        or receipts[-1] == receipts[0]
        or independently_verified_relationship
        != {
            "search_receipt_id": receipts[0],
            "inspected_receipt_id": receipts[0],
            "inspection_receipt_id": receipts[-1],
            "valid": True,
        }
    ):
        fail("the search-to-inspection receipt relationship is invalid")
    if (
        total_operations != Counter({operation: 1 for operation in OPERATIONS})
        or total_methods["tools/call"] != 5
        or total_methods["resources/read"] != 0
        or set(total_methods) - {"server/discover", "tools/list", "tools/call"}
        or total_methods["server/discover"] != protocol_facts["discovery_count"]
        or total_methods["tools/list"] != protocol_facts["tools_list_count"]
        or protocol_facts["resources_advertised"] != 0
        or total_audit
        != Counter(
            {
                "provider_transport_calls": 1,
                "ledger_event_count": 4,
                "guarded_provider_api_invocations": 0,
                "aborted_provider_calls": 0,
            }
        )
    ):
        fail("the complete session widened its calls, resources or provider boundary")
    return (
        summaries,
        total_methods,
        total_operations,
        dict(total_audit),
        independent,
        dict(protocol_facts),
    )


def verify_output(
    private_root: Path,
    manifest: dict[str, Any],
    receipt_ids: dict[str, str],
) -> dict[str, Any]:
    execution = manifest["execution"]
    if (
        execution["exit_code"] != 0
        or execution["signal"] is not None
        or execution["interrupted_signal"] is not None
        or execution["harness_classification"] is not None
        or execution["process_group_absent"] is not True
        or execution["spawned_process_executable_attested"] is not True
        or execution["stdout"]["limit_exceeded"] is not False
        or execution["stderr"]["limit_exceeded"] is not False
    ):
        fail("Claude did not complete one bounded exact-five client run")
    stdout = read_private(
        private_root / "stdout.json",
        maximum=8 * 1_048_576,
        label="Claude stdout",
    )
    stderr = read_private(
        private_root / "stderr.log",
        maximum=1_048_576,
        label="Claude stderr",
    )
    if (
        len(stdout) != execution["stdout"]["bytes"]
        or sha256_bytes(stdout) != execution["stdout"]["sha256"]
        or len(stderr) != execution["stderr"]["bytes"]
        or sha256_bytes(stderr) != execution["stderr"]["sha256"]
    ):
        fail("Claude output files do not match the private run manifest")
    if host002.TOKEN_PATTERN.search(stdout) or host002.TOKEN_PATTERN.search(stderr):
        fail("Claude private output contains a recognised credential pattern")
    output = strict_object(stdout, label="Claude JSON output")
    structured = output.get("structured_output")
    model_usage = output.get("modelUsage")
    usage = output.get("usage")
    reported = model_usage.get(PINNED_MODEL) if isinstance(model_usage, dict) else None

    def token_count(mapping: Any, name: str, *, maximum: int) -> int | None:
        value = mapping.get(name) if isinstance(mapping, dict) else None
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= maximum:
            return None
        return value

    aggregate_names = (
        "input_tokens",
        "cache_creation_input_tokens",
        "cache_read_input_tokens",
        "output_tokens",
    )
    model_names = (
        "inputTokens",
        "cacheCreationInputTokens",
        "cacheReadInputTokens",
        "outputTokens",
    )
    token_maxima = (10_000_000, 10_000_000, 10_000_000, 1_000_000)
    aggregate_counts = [
        token_count(usage, name, maximum=maximum)
        for name, maximum in zip(aggregate_names, token_maxima, strict=True)
    ]
    model_counts = [
        token_count(reported, name, maximum=maximum)
        for name, maximum in zip(model_names, token_maxima, strict=True)
    ]
    num_turns = output.get("num_turns")
    if any(value is None for value in aggregate_counts + model_counts):
        fail("Claude final output does not contain bounded model usage")
    bounded_aggregate = [int(value) for value in aggregate_counts]
    bounded_model = [int(value) for value in model_counts]
    if (
        type(num_turns) is not int
        or num_turns < MINIMUM_CLAUDE_REPORTED_TURNS
        or num_turns > MAXIMUM_CLAUDE_REPORTED_TURNS
        or execution["maximum_turns"] != MAXIMUM_AGENTIC_TURNS
    ):
        fail("Claude CLI reported turns fall outside the bounded turn semantics")
    stop_reason = output.get("stop_reason")
    terminal_reason = output.get("terminal_reason")
    if terminal_reason != "completed":
        fail("Claude final output did not report a completed terminal reason")
    if stop_reason not in {"end_turn", "tool_use"}:
        fail(
            "Claude final output did not use an accepted end_turn or tool_use "
            "stop reason"
        )
    if "deferred_tool_use" in output:
        fail("Claude final output retained deferred tool use")
    if (
        output.get("type") != "result"
        or output.get("is_error") is not False
        or output.get("subtype") != "success"
        or output.get("permission_denials") != []
        or not isinstance(structured, dict)
        or set(structured)
        != {"profile", "operation_order", "receipt_ids", "inspected_search_receipt_id"}
        or structured["profile"] != PROFILE_ID
        or structured["operation_order"] != list(OPERATIONS)
        or structured["receipt_ids"] != receipt_ids
        or structured["inspected_search_receipt_id"] != receipt_ids["catalogue.search"]
        or not isinstance(model_usage, dict)
        or set(model_usage) != {PINNED_MODEL}
        or not isinstance(reported, dict)
        or bounded_aggregate != bounded_model
        or sum(bounded_aggregate[:3]) <= 0
        or sum(bounded_aggregate[:3]) > 10_000_000
        or bounded_aggregate[3] <= 0
    ):
        fail("Claude final structured output does not match all five verified results")
    return {
        "model_reported": PINNED_MODEL,
        "model_usage_observed": True,
        "input_tokens": sum(bounded_aggregate[:3]),
        "output_tokens": bounded_aggregate[3],
        "claude_cli_reported_turns": num_turns,
        "claude_cli_stop_reason": stop_reason,
        "claude_cli_terminal_reason": terminal_reason,
        "agentic_turn_limit": execution["maximum_turns"],
        "turn_count_semantics": TURN_COUNT_SEMANTICS,
    }


def verify_and_project(
    private_root: Path,
    *,
    source_verifier: Callable[[dict[str, Any]], None] | None = None,
    private_validator: Draft202012Validator | None = None,
    public_validator: Draft202012Validator | None = None,
) -> dict[str, Any]:
    root_state = require_directory(private_root, label="private root")
    if set(os.listdir(private_root)) != EXPECTED_ROOT_NAMES:
        fail("private root does not contain the exact harness output set")
    require_directory(private_root / "workspace", label="private workspace")
    if os.listdir(private_root / "workspace"):
        fail("the isolated Claude workspace is not empty")
    manifest_raw = read_private(
        private_root / "run-manifest.json",
        maximum=1_048_576,
        label="private run manifest",
    )
    manifest = strict_object(manifest_raw, label="private run manifest", newline=True)
    if canonical_line(manifest) != manifest_raw:
        fail("private run manifest is not canonical JSON")
    validate(
        private_validator or schema_validator(PRIVATE_SCHEMA),
        manifest,
        label="private run manifest",
    )
    private_raw: dict[str, bytes] = {}
    for name in ("mcp_config", "settings", "stdout", "stderr"):
        facts = manifest["private_files"][name]
        raw = read_private(
            private_root / facts["name"],
            maximum=8 * 1_048_576,
            label=name,
        )
        if len(raw) != facts["bytes"] or sha256_bytes(raw) != facts["sha256"]:
            fail(f"{name} does not match the private manifest")
        private_raw[name] = raw
    profile = verify_case(manifest)
    verify_private_configuration(
        private_root,
        manifest,
        private_raw["mcp_config"],
        private_raw["settings"],
    )
    source_check = source_verifier or verify_source_and_materials
    source_check(manifest)
    summaries, methods, operations, audit, independent, protocol_facts = verify_sessions(
        private_root / "observer",
        manifest,
        profile,
    )
    receipt_ids = {
        item["operation"]: item["receipt_id"] for item in independent["operations"]
    }
    model_result = verify_output(private_root, manifest, receipt_ids)
    if methods["server/discover"] < 1 or methods["tools/list"] < 1:
        fail("Claude did not complete discovery and exact-five listing before use")
    if operations != Counter({operation: 1 for operation in OPERATIONS}):
        fail("Claude did not complete the exact ordered operation set")
    source_check(manifest)
    projection = {
        "schema": "gis-ai-go.qual-206-claude-exact-five-capability-evidence.v1",
        "status": "capability_pass",
        "observed_at": manifest["execution"]["finished_at"],
        "source": {
            "repository": "chris-page-gov/gis-ai-go",
            "repository_origin": manifest["source"]["repository_origin"],
            "commit": manifest["source"]["commit"],
            "tree": manifest["source"]["tree"],
            "version": "0.1.0",
            "local_origin_main_match": manifest["source"]["local_origin_main_match"],
            "protected_main_verification": manifest["source"][
                "protected_main_verification"
            ],
            "production_activation": False,
        },
        "host": {
            "name": "Claude Code",
            "version": manifest["host"]["version"],
            "executable_bytes": manifest["host"]["executable_bytes"],
            "executable_sha256": manifest["host"]["executable_sha256"],
            "model_requested": manifest["host"]["model_requested"],
            "auth_kind": manifest["host"]["auth_kind"],
            "auth_preflight": {
                "logged_in": manifest["host"]["auth_preflight"]["logged_in"],
                "api_provider": manifest["host"]["auth_preflight"]["api_provider"],
                "auth_method": manifest["host"]["auth_preflight"]["auth_method"],
                "subscription_type_observed": isinstance(
                    manifest["host"]["auth_preflight"]["subscription_type"], str
                ),
            },
            "model_provider_usage_observed": True,
            "guarded_provider_api_invocations": audit[
                "guarded_provider_api_invocations"
            ],
        },
        "profile": {
            "id": PROFILE_ID,
            "profile_sha256": manifest["case"]["corpus_sha256"],
            "prompt_sha256": manifest["case"]["prompt_sha256"],
            "operation_order": list(OPERATIONS),
            "prompt_text_repeated_in_projection": False,
        },
        "transport": {
            "protocol": PROTOCOL,
            "kind": "operating-system-stdio-pipes",
            "session_count": len(summaries),
            "request_count": sum(methods.values()),
            "response_count": sum(methods.values()),
            "tool_call_count": 5,
            "resource_read_count": methods["resources/read"],
            "resources_advertised": protocol_facts["resources_advertised"],
            "provider_transport_calls": audit["provider_transport_calls"],
            "aborted_provider_calls": audit["aborted_provider_calls"],
            "ledger_event_count": audit["ledger_event_count"],
            "guarded_provider_api_invocations": audit[
                "guarded_provider_api_invocations"
            ],
            "tool_schema_projection": independent["tool_schema_projection"],
        },
        "result": {
            "classification": "capability_pass",
            "capability": "passed",
            "profile": PROFILE_ID,
            "operation_order": list(OPERATIONS),
            "operation_receipts": independent["operations"],
            "inspection_relationship": independent["inspection_relationship"],
            "independent_result_verification": True,
            "model_output_match": True,
            **model_result,
            "client_exit_code": manifest["execution"]["exit_code"],
        },
        "isolation": {
            "built_in_tools_available": False,
            "allowed_mcp_tool_count": 5,
            "claude_permission_aliases": list(PERMISSION_ALIASES),
            "permission_mode": "dontAsk",
            "session_persistence": False,
            "maximum_agentic_turns": MAXIMUM_AGENTIC_TURNS,
            "mcp_subtree_network_access_allowed": False,
            "mcp_subtree_network_sandbox": host002.NETWORK_SANDBOX,
            "mcp_child_recognised_credentials_forwarded": False,
            "raw_host_output_published": False,
        },
        "runtime_binding": {
            "tracked_source_material_count": len(
                manifest["runtime_binding"]["tracked_source_materials"]
            ),
            "generated_first_party_closure": manifest["runtime_binding"][
                "generated_first_party_closure"
            ],
            "installed_dependency_closure": manifest["runtime_binding"][
                "installed_dependency_closure"
            ],
            "node_runtime": {
                "bytes": manifest["runtime_binding"]["node_runtime"]["bytes"],
                "sha256": manifest["runtime_binding"]["node_runtime"]["sha256"],
                "version": manifest["runtime_binding"]["node_runtime"]["version"],
            },
            "network_sandbox": {
                "bytes": manifest["runtime_binding"]["network_sandbox"]["bytes"],
                "profile_sha256": manifest["runtime_binding"]["network_sandbox"][
                    "profile_sha256"
                ],
                "sha256": manifest["runtime_binding"]["network_sandbox"]["sha256"],
            },
            "network_sandbox_probe": manifest["runtime_binding"][
                "network_sandbox_probe"
            ],
            "complete_first_party_generated_closure_binding": manifest[
                "runtime_binding"
            ]["complete_first_party_generated_closure_binding"],
            "third_party_runtime_binding": manifest["runtime_binding"][
                "third_party_runtime_binding"
            ],
            "complete_runtime_source_binding": manifest["runtime_binding"][
                "complete_runtime_source_binding"
            ],
            "dependency_materials_stable": manifest["runtime_binding"][
                "dependency_materials_stable"
            ],
            "runtime_materials_stable": manifest["runtime_binding"][
                "runtime_materials_stable"
            ],
            "source_checkout_stable": manifest["runtime_binding"][
                "source_checkout_stable"
            ],
        },
        "claims": {
            "local_stdio_exact_five_model_capability": True,
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
            "manifest_sha256": sha256_bytes(manifest_raw),
            "stdout_sha256": manifest["execution"]["stdout"]["sha256"],
            "stderr_sha256": manifest["execution"]["stderr"]["sha256"],
            "result_material_sha256": independent["result_material_sha256"],
        },
        "boundary": BOUNDARY,
    }
    validate(
        public_validator or schema_validator(PUBLIC_SCHEMA),
        projection,
        label="public projection",
    )
    after = private_root.lstat()
    if (
        root_state.st_dev,
        root_state.st_ino,
        root_state.st_mode,
        root_state.st_uid,
    ) != (after.st_dev, after.st_ino, after.st_mode, after.st_uid):
        fail("private root changed during verification")
    return projection


def publish_projection(output: Path, projection: dict[str, Any]) -> None:
    if not output.is_absolute() or Path(os.path.abspath(output)) != output:
        fail("public output path must be canonical and absolute")
    if output.exists() or Path(os.path.realpath(output.parent)) != output.parent:
        fail("public output must be a new file in a real directory")
    if output.parent != EVIDENCE_DIRECTORY:
        fail("public output is outside the interoperability evidence directory")
    _host_call(host002.publish_projection, output, projection)


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Verify one private Claude exact-five run and publish a pass-only projection."
        )
    )
    parser.add_argument("--private-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    try:
        projection = verify_and_project(arguments.private_root)
        publish_projection(arguments.output, projection)
    except (
        OSError,
        ExactFiveCapabilityVerificationError,
        host002.CapabilityVerificationError,
        composite.VerificationError,
    ) as error:
        print(
            f"QUAL-206 Claude exact-five capability verification failed: {error}",
            file=sys.stderr,
        )
        return 1
    print("QUAL-206 Claude exact-five capability pass verified and projected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
