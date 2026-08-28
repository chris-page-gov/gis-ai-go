#!/usr/bin/env python3
"""Verify one private ChatGPT secure-tunnel run and project only a path-free pass."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
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
    ROOT / "schemas/qual-206-chatgpt-tunnel-exact-five-private-run-v1.schema.json"
)
STATUS_SCHEMA = ROOT / "schemas/qual-206-chatgpt-tunnel-status-v1.schema.json"
CAPTURE_SCHEMA = (
    ROOT
    / "schemas/qual-206-chatgpt-tunnel-exact-five-session-capture-v1.schema.json"
)
SESSION_SCHEMA = (
    ROOT / "schemas/qual-206-chatgpt-tunnel-exact-five-session-v1.schema.json"
)
EVENT_SCHEMA = ROOT / "schemas/qual-206-chatgpt-tunnel-exact-five-event-v1.schema.json"
PUBLIC_SCHEMA = (
    ROOT / "schemas/qual-206-chatgpt-tunnel-exact-five-evidence-v1.schema.json"
)
PROFILE = (
    ROOT
    / "tests/interoperability/fixtures/qual_206_chatgpt_tunnel_exact_five_profile.v1.json"
)
OBSERVER = ROOT / "scripts/qual_206_chatgpt_tunnel_exact_five_observer.mjs"
EXACT_VALIDATOR = ROOT / "scripts/qual_206_claude_stdio_observer.mjs"
FIXTURE = (
    ROOT / "tests/interoperability/fixtures/qual_206_strict_modern_event_server.mjs"
)
PROVIDER_GUARD = (
    ROOT / "tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs"
)
RESULT_VERIFIER = ROOT / "scripts/verify_qual_206_chatgpt_tunnel_exact_five_results.mjs"
EVIDENCE_DIRECTORY = ROOT / "tests/interoperability/evidence"

EVENT_SCHEMA_ID = "gis-ai-go.qual-206-chatgpt-tunnel-exact-five-event.v1"
EVENT_DIGEST_PREFIX = b"GIS-AI-GO\0canonical-json\0sha256\0v1\0"
PROFILE_ID = "exact-five-v1"
SCENARIO = "chatgpt-tunnel-exact-five-v1"
PROTOCOL = "2026-07-28"
NETWORK_SANDBOX = "macos-seatbelt-deny-network"
NETWORK_SANDBOX_PROFILE_SHA256 = (
    "0a5222386587bf836d30a070bd759c0194f999bf5503ba76c6c0f8cb84b19db2"
)
OPERATIONS = (
    "catalogue.search",
    "catalogue.describe",
    "selection.resolve",
    "data.query",
    "evidence.inspect",
)
TUNNEL_CLIENT_VERSION = (
    "0.0.13+4b5267f823be0b046bb883aacb51603cfde3a0ea "
    "(git sha: 4b5267f823be0b046bb883aacb51603cfde3a0ea)"
)
TUNNEL_CLIENT_BYTES = 20_336_818
TUNNEL_CLIENT_SHA256 = (
    "814b5e7ad378e6dfeb7eeebf12df37ff879cfe58fd504769cabfc3e3b4cf99f6"
)
EXPECTED_NODE_BYTES = host002.EXPECTED_NODE_BYTES
EXPECTED_NODE_SHA256 = host002.EXPECTED_NODE_SHA256
SOURCE_RUNTIME_PATHS = {
    "observer_source_sha256": OBSERVER,
    "exact_validator_source_sha256": EXACT_VALIDATOR,
    "fixture_source_sha256": FIXTURE,
    "provider_egress_guard_source_sha256": PROVIDER_GUARD,
    "profile_sha256": PROFILE,
}
RUNTIME_BINDING_SOURCE = """
import { buildAndBindGeneratedRuntime } from
  './scripts/qual_206_claude_capability_harness.mjs';
const binding = buildAndBindGeneratedRuntime(process.argv[1], process.argv[2]);
process.stdout.write(`${JSON.stringify(binding)}\\n`);
""".strip()
CLAIM_NAME = "exact-five-v1.claim.json"
STATUS_BEFORE_NAME = "tunnel-status-before.json"
STATUS_AFTER_NAME = "tunnel-status-after.json"
STATUS_STOPPED_NAME = "tunnel-status-stopped.json"
SESSION_CORE_FILES = {"events.jsonl", "exact-five-session.json", "manifest.json"}
EXPECTED_CLAIMS = {
    "remote_host_via_openai_secure_tunnel": True,
    "local_mcp_child_transport": "stdio",
    "direct_public_streamable_http_tls": False,
    "live_geospatial_provider": False,
    "registry_publication": False,
    "activation": False,
    "deployment": False,
    "release": False,
}
BOUNDARY = (
    "One bounded ChatGPT exact-five-v1 remote-host observation through the reviewed "
    "OpenAI secure tunnel to a byte-bound local STDIO observer, which proxied the "
    "calls to a separate network-denied deterministic MCP 2026-07-28 fixture/server. "
    "This proves neither direct public Streamable HTTP over TLS nor a live geospatial "
    "provider, registry publication, activation, deployment or release."
)
FORBIDDEN_PUBLIC_TEXT = re.compile(
    r"(?:/Users/|/home/|/Volumes/|/private/tmp/|/tmp/|/var/folders/|"
    r"/opt/homebrew/|/usr/bin/|file://|localhost|127\.0\.0\.1|"
    r"\b(?:OPENAI|CODEX|ANTHROPIC|CLAUDE)_[A-Z0-9_]*KEY\b|"
    r"\bBearer\s+[A-Za-z0-9._~-]+|"
    r"\bsk-[A-Za-z0-9_-]{8,}|[A-Za-z]:\\\\Users\\\\)",
    re.IGNORECASE,
)
FORBIDDEN_PUBLIC_FIELDS = {
    "arguments",
    "command",
    "endpoint",
    "environment",
    "local_path",
    "pid",
    "port",
    "prompt",
    "raw_content",
    "request_id",
    "result_material",
    "route",
    "run_id",
    "session_id",
    "url",
}


class TunnelExactFiveVerificationError(ValueError):
    """The private secure-tunnel run did not satisfy the closed pass contract."""


def fail(message: str) -> NoReturn:
    raise TunnelExactFiveVerificationError(message)


def correlate_request_response_events(
    events: list[dict[str, Any]], slot: str
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Correlate responses while allowing an ID to be reused after completion."""

    pending: dict[str, dict[str, Any]] = {}
    pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for event in events:
        if event["event"] == "request":
            digest = event["request_id_sha256"]
            if digest in pending:
                fail(f"{slot} reuses an in-flight request identity")
            pending[digest] = event
        elif event["event"] == "response":
            digest = event["request_id_sha256"]
            request = pending.pop(digest, None)
            if request is None:
                fail(f"{slot} contains an orphan or duplicate response")
            pairs.append((request, event))
    if pending:
        fail(f"{slot} contains an unanswered request")
    return pairs


def _host_call(function: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    try:
        return function(*args, **kwargs)
    except (host002.CapabilityVerificationError, composite.VerificationError) as error:
        raise TunnelExactFiveVerificationError(str(error)) from error


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return _host_call(composite.canonical_json_bytes, value)


def canonical_line(value: dict[str, Any]) -> bytes:
    return canonical_bytes(value) + b"\n"


def event_digest(value: dict[str, Any]) -> str:
    digest = hashlib.sha256()
    digest.update(EVENT_DIGEST_PREFIX)
    digest.update(EVENT_SCHEMA_ID.encode("utf-8"))
    digest.update(b"\0")
    digest.update(canonical_bytes(value))
    return digest.hexdigest()


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
    return _host_call(host002.read_stable_regular, path, maximum=maximum, label=label)


def strict_canonical_object(
    raw: bytes,
    *,
    label: str,
    maximum_single_line: bool = True,
) -> dict[str, Any]:
    if not raw.endswith(b"\n") or raw.endswith(b"\r\n"):
        fail(f"{label} is not LF-terminated")
    if maximum_single_line and b"\n" in raw[:-1]:
        fail(f"{label} is not one canonical JSON object")
    value = _host_call(host002.strict_object, raw[:-1], label=label)
    if canonical_line(value) != raw:
        fail(f"{label} is not canonical JSON")
    return value


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def nested_field_names(value: Any) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {
            name for child in value.values() for name in nested_field_names(child)
        }
    if isinstance(value, list):
        return {name for child in value for name in nested_field_names(child)}
    return set()


def verify_source(manifest: dict[str, Any]) -> None:
    source = manifest["source"]
    if (
        _host_call(host002.git_output, "rev-parse", "HEAD") != source["commit"]
        or _host_call(host002.git_output, "rev-parse", "refs/remotes/origin/main")
        != source["commit"]
        or _host_call(host002.git_output, "rev-parse", f"{source['commit']}^{{tree}}")
        != source["tree"]
        or _host_call(
            host002.git_output,
            "config",
            "--local",
            "--no-includes",
            "--get",
            "remote.origin.url",
        )
        not in host002.ALLOWED_REPOSITORY_ORIGINS
        or _host_call(
            host002.git_output, "status", "--porcelain=v1", "--untracked-files=all"
        )
        != ""
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


def verify_bound_file(
    private_root: Path,
    facts: dict[str, Any],
    *,
    maximum: int,
    label: str,
) -> bytes:
    raw = read_private(private_root / facts["name"], maximum=maximum, label=label)
    if (
        facts["mode"] != "0600"
        or len(raw) != facts["bytes"]
        or not hmac.compare_digest(sha256_bytes(raw), facts["sha256"])
    ):
        fail(f"{label} does not match the private run manifest")
    return raw


def verify_statuses(
    before_raw: bytes,
    after_raw: bytes,
    stopped_raw: bytes,
    manifest: dict[str, Any],
    status_validator: Draft202012Validator,
) -> str:
    before = strict_canonical_object(before_raw, label="tunnel status before")
    after = strict_canonical_object(after_raw, label="tunnel status after")
    stopped = strict_canonical_object(stopped_raw, label="tunnel status stopped")
    validate(status_validator, before, label="tunnel status before")
    validate(status_validator, after, label="tunnel status after")
    validate(status_validator, stopped, label="tunnel status stopped")
    if (
        before["phase"] != "before"
        or after["phase"] != "after"
        or stopped["phase"] != "stopped"
    ):
        fail("tunnel status phases are not the exact preflight, postflight and stop set")
    tunnel = manifest["tunnel"]
    expected_running_identity = {
        "alias": tunnel["local_alias"],
        "tunnel_id": tunnel["remote_id"],
        "remote": {
            "found": True,
            "id": tunnel["remote_id"],
            "name": tunnel["remote_name"],
        },
    }
    expected_stopped_identity = {
        **expected_running_identity,
        "remote": {**expected_running_identity["remote"], "found": False},
    }
    for value, expected in (
        (before, expected_running_identity),
        (after, expected_running_identity),
        (stopped, expected_stopped_identity),
    ):
        identity = {key: value[key] for key in ("alias", "tunnel_id", "remote")}
        if identity != expected:
            fail("preflight, postflight or stopped tunnel identity drifted")
    command_hashes = {value["mcp_command_sha256"] for value in (before, after, stopped)}
    if (
        len(command_hashes) != 1
        or any(
            value["profile_name"] != tunnel["local_alias"]
            or value["target_kind"] != "command"
            for value in (before, after, stopped)
        )
    ):
        fail("preflight and postflight tunnel identities drifted")
    started = parse_time(manifest["execution"]["started_at"])
    finished = parse_time(manifest["execution"]["finished_at"])
    if not (
        parse_time(before["observed_at"])
        <= started
        <= finished
        <= parse_time(after["observed_at"])
        <= parse_time(stopped["observed_at"])
    ):
        fail("tunnel status, execution and teardown timestamps are not ordered")
    return command_hashes.pop()


def load_profile() -> tuple[dict[str, Any], list[dict[str, Any]], str]:
    raw = read_stable_regular(PROFILE, maximum=1_048_576, label="secure-tunnel profile")
    value = _host_call(host002.strict_object, raw, label="secure-tunnel profile")
    operations = value.get("operations")
    if (
        value.get("schema") != "gis-ai-go.qual-206-host-capability-profile.v1"
        or value.get("profile") != PROFILE_ID
        or not isinstance(operations, list)
        or [item.get("name") for item in operations] != list(OPERATIONS)
        or [item.get("ordinal") for item in operations] != list(range(5))
        or any(not isinstance(item.get("arguments"), dict) for item in operations[:4])
        or operations[-1].get("arguments_from")
        != "catalogue.search.evidence_receipt.receipt_id"
    ):
        fail("the secure-tunnel exact-five profile changed")
    return value, [item["arguments"] for item in operations[:4]], sha256_bytes(raw)


def source_runtime_digests(profile_sha256: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for field, path in SOURCE_RUNTIME_PATHS.items():
        raw = read_stable_regular(path, maximum=536_870_912, label=field)
        values[field] = sha256_bytes(raw)
    if values["profile_sha256"] != profile_sha256:
        fail("profile digest changed during verification")
    return values


def locate_verified_node(path: Path) -> str:
    if not path.is_absolute():
        fail("Node path must be an existing canonical absolute path")
    try:
        resolved = path.resolve(strict=True)
    except OSError:
        fail("Node path must be an existing canonical absolute path")
    if resolved != path:
        fail("Node path must be an existing canonical absolute path")
    node = str(resolved)
    raw = read_stable_regular(Path(node), maximum=1_048_576, label="Node runtime")
    if len(raw) != EXPECTED_NODE_BYTES or sha256_bytes(raw) != EXPECTED_NODE_SHA256:
        fail("the Node runtime does not match the accepted verifier runtime")
    result = subprocess.run(
        [node, "--version"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={"LANG": "C", "LC_ALL": "C", "PATH": "/usr/bin:/bin"},
        timeout=10,
        text=True,
    )
    if result.returncode != 0 or result.stderr or result.stdout.strip() != "v26.7.0":
        fail("the Node runtime version changed")
    return node


def require_explicit_pnpm_path(path: Path) -> str:
    if not path.is_absolute():
        fail("pnpm path must be an existing canonical absolute path")
    try:
        resolved = path.resolve(strict=True)
    except OSError:
        fail("pnpm path must be an existing canonical absolute path")
    if resolved != path:
        fail("pnpm path must be an existing canonical absolute path")
    return str(resolved)


def verify_runtime_closure_facts(
    expected: dict[str, Any],
    *,
    current_generated: dict[str, Any],
    current_installed: dict[str, Any],
    independently_built: dict[str, Any],
) -> None:
    generated = expected["generated_first_party_closure"]
    if (
        set(expected)
        != {"generated_first_party_closure", "installed_dependency_closure"}
        or generated["reference_manifest_sha256"] != generated["manifest_sha256"]
        or generated["reference_matches_current"] is not True
        or current_generated
        != {
            "bytes": generated["bytes"],
            "file_count": generated["file_count"],
            "manifest_sha256": generated["manifest_sha256"],
        }
        or current_installed != expected["installed_dependency_closure"]
        or independently_built != expected
    ):
        fail("generated or installed runtime closure is not independently source-bound")


def independently_reproduce_runtime_closure(
    source_commit: str,
    *,
    node_path: str,
    pnpm_path: Path,
) -> dict[str, Any]:
    current_generated = _host_call(host002.measure_generated_runtime_closure)
    current_installed = _host_call(host002.measure_installed_dependency_closure)
    explicit_pnpm_path = require_explicit_pnpm_path(pnpm_path)
    build_environment = dict(host002.CLOSED_GIT_ENVIRONMENT)
    build_environment["PATH"] = os.pathsep.join(
        (str(Path(node_path).parent), "/usr/bin", "/bin")
    )
    result = subprocess.run(
        [
            str(host002.SANDBOX_EXEC),
            "-p",
            host002.NETWORK_SANDBOX_PROFILE,
            node_path,
            "--input-type=module",
            "--eval",
            RUNTIME_BINDING_SOURCE,
            source_commit,
            explicit_pnpm_path,
        ],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=build_environment,
        timeout=300,
    )
    if result.returncode != 0 or result.stderr:
        fail("independent source reference build for the runtime closure failed")
    independently_built = strict_canonical_object(
        result.stdout,
        label="independent runtime closure",
        maximum_single_line=True,
    )
    verify_runtime_closure_facts(
        independently_built,
        current_generated=current_generated,
        current_installed=current_installed,
        independently_built=independently_built,
    )
    return independently_built


def independently_verify_results(result_raw: bytes, *, node_path: str) -> dict[str, Any]:
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
        fail("independent secure-tunnel exact-five result verification failed")
    verified = strict_canonical_object(
        result.stdout,
        label="independent secure-tunnel result verification",
    )
    expected_keys = {
        "schema", "profile", "run_id", "session_id", "discovery_count",
        "tools_list_count", "resources_list_count", "resource_templates_list_count",
        "resources_advertised", "canonical_tools_sha256",
        "tool_schema_projection_applied", "operation_order", "operations",
        "inspection_relationship", "result_material_sha256",
    }
    if (
        set(verified) != expected_keys
        or verified["schema"]
        != "gis-ai-go.qual-206-chatgpt-tunnel-exact-five-results-verification.v1"
    ):
        fail("independent result verifier widened its output")
    return verified


def verify_event_log(
    raw: bytes,
    *,
    slot: str,
    run_id: str,
    session_id: str,
    source_commit: str,
    parent_identity: dict[str, Any],
    runtime_digests: dict[str, str],
    runtime_closure: dict[str, Any],
    mcp_command_sha256: str,
    event_validator: Draft202012Validator,
) -> tuple[list[dict[str, Any]], Counter[str], Counter[str], dict[str, int]]:
    if not raw or not raw.endswith(b"\n") or raw.endswith(b"\r\n"):
        fail(f"{slot} event log is not LF-terminated")
    encoded_lines = [line + b"\n" for line in raw[:-1].split(b"\n")]
    events: list[dict[str, Any]] = []
    previous: str | None = None
    for index, encoded in enumerate(encoded_lines):
        event = strict_canonical_object(encoded, label=f"{slot} event {index}")
        validate(event_validator, event, label=f"{slot} event {index}")
        if (
            event["sequence"] != index
            or event["slot"] != slot
            or event["run_id"] != run_id
            or event["session_id"] != session_id
            or event["previous_event_sha256"] != previous
        ):
            fail(f"{slot} event {index} has invalid chain context")
        core = dict(event)
        supplied = core.pop("event_sha256")
        if not hmac.compare_digest(supplied, event_digest(core)):
            fail(f"{slot} event {index} has an invalid content address")
        previous = supplied
        events.append(event)
    if not events:
        fail(f"{slot} event log is empty")
    lifecycle = [event for event in events if event["event"] == "lifecycle"]
    phases = [event["phase"] for event in lifecycle]
    accepted_phases = (
        ["session-start", "child-spawned", "child-exit", "session-end"],
        [
            "session-start", "child-spawned", "parent-teardown-signal",
            "child-exit", "session-end",
        ],
    )
    if phases not in accepted_phases:
        fail(f"{slot} lifecycle is not the exact closed sequence")
    start = lifecycle[0]
    child_exit = next(event for event in lifecycle if event["phase"] == "child-exit")
    end = lifecycle[-1]
    teardown = next(
        (event for event in lifecycle if event["phase"] == "parent-teardown-signal"),
        None,
    )
    expected_closure_stimulus = "stdin-eof"
    if teardown is not None:
        teardown_pair = (
            teardown["stdin_closed_before_signal"],
            teardown["stdin_eof_observed_within_grace"],
        )
        expected_closure_stimulus = {
            (True, False): "stdin-eof-and-sigterm",
            (False, True): "sigterm-then-stdin-eof",
        }.get(teardown_pair, "")
        if (
            not expected_closure_stimulus
            or teardown["signal"] != "SIGTERM"
            or teardown["immediate_parent_verified"] is not True
        ):
            fail(f"{slot} parent teardown evidence is inconsistent")
    if end["closure_stimulus"] != expected_closure_stimulus:
        fail(f"{slot} parent teardown closure is inconsistent")
    if (
        events[0] is not start
        or events[-1] is not end
        or start["source_commit"] != source_commit
        or start["protocol_target"] != PROTOCOL
        or start["transport"] != "operating-system-stdio-pipes"
        or start["immediate_parent"]
        != {"pid": start["immediate_parent"]["pid"], **parent_identity}
        or start["observer_runtime"]["node_version"] != "v26.7.0"
        or start["observer_runtime"]["node_executable_bytes"] != EXPECTED_NODE_BYTES
        or start["observer_runtime"]["node_executable_sha256"] != EXPECTED_NODE_SHA256
        or start["observer_runtime"]["network_sandbox_executable_bytes"]
        != host002.EXPECTED_SANDBOX_EXEC_BYTES
        or start["observer_runtime"]["network_sandbox_executable_sha256"]
        != host002.EXPECTED_SANDBOX_EXEC_SHA256
        or start["observer_runtime"]["network_sandbox_profile_sha256"]
        != NETWORK_SANDBOX_PROFILE_SHA256
        or any(
            start["observer_runtime"][field] != digest
            for field, digest in runtime_digests.items()
        )
        or start["runtime_closure"] != runtime_closure
        or start["observer_runtime"]["command_sha256"] != mcp_command_sha256
        or start["credential_environment_observed"] is not False
        or start["credential_environment_forwarded"] is not False
        or start["mcp_child_network_access_allowed"] is not False
        or child_exit["exit_code"] != 0
        or child_exit["signal"] is not None
    ):
        fail(f"{slot} runtime or source binding changed")
    prior_raw = b"".join(encoded_lines[:-1])
    if (
        end["runtime_materials_stable"] is not True
        or end["runtime_closures_stable"] is not True
        or end["exit_code"] != 0
        or end["signal"] is not None
        or end["pending_request_count"] != 0
        or end["stderr_event_count"] != 0
        or end["stderr_bytes"] != 0
        or end["anomaly_count"] != 0
        or end["temporary_state_removed"] is not True
        or end["prior_event_count"] != len(events) - 1
        or end["prior_event_log_bytes"] != len(prior_raw)
        or end["prior_event_log_sha256"] != sha256_bytes(prior_raw)
    ):
        fail(f"{slot} did not close cleanly")
    requests = [event for event in events if event["event"] == "request"]
    responses = [event for event in events if event["event"] == "response"]
    if (
        len(requests) != len(responses)
        or end["request_count"] != len(requests)
        or end["response_count"] != len(responses)
    ):
        fail(f"{slot} request and response counts differ")
    correlated = correlate_request_response_events(events, slot)
    if len(correlated) != len(requests):
        fail(f"{slot} request and response correlation is incomplete")
    methods: Counter[str] = Counter()
    operations: Counter[str] = Counter()
    for request in requests:
        methods[request["method"]] += 1
        if request["method"] == "tools/call":
            operations[request["operation"]] += 1
        if (
            request["request_id_unique"] is not True
            or request["client_attribution_valid"] is not True
            or request["semantic_valid"] is not True
            or request["protocol_claim"] != PROTOCOL
            or (
                request["method"] == "tools/call"
                and (
                    request["arguments_bytes"] is None
                    or request["arguments_sha256"] is None
                )
            )
            or (
                request["method"] != "tools/call"
                and (
                    request["arguments_bytes"] is not None
                    or request["arguments_sha256"] is not None
                )
            )
        ):
            fail(f"{slot} contains an invalid request")
    for request, response in correlated:
        if (
            response["request_id_kind"] != request["request_id_kind"]
            or response["request_method"] != request["method"]
            or response["operation"] != request["operation"]
            or response["correlation"] != "matched"
            or response["outcome"] != "success"
            or response["error_code"] is not None
            or response["contract_valid"] is not True
        ):
            fail(f"{slot} contains an invalid or uncorrelated response")
    if any(event["event"] == "anomaly" for event in events):
        fail(f"{slot} contains an anomaly")
    streams = [event for event in events if event["event"] == "stream"]
    if (
        {event["stream_name"] for event in streams}
        != {"host-stdin", "fixture-stdout", "fixture-audit", "fixture-stderr"}
        or any(event["graceful"] is not True for event in streams)
    ):
        fail(f"{slot} stream closure is incomplete")
    stderr_stream = next(event for event in streams if event["stream_name"] == "fixture-stderr")
    if stderr_stream["bytes"] != 0 or stderr_stream["frames"] != 0:
        fail(f"{slot} fixture stderr is not empty")
    audits = [event for event in events if event["event"] == "audit"]
    audit_kinds = [event["audit_kind"] for event in audits]
    no_call = [
        "provider-egress-guard-ready", "provider-egress-guard-summary", "session-summary"
    ]
    exact_five = [
        "provider-egress-guard-ready", "provider-transport-started",
        "provider-egress-guard-summary", "session-summary",
    ]
    if audit_kinds not in (no_call, exact_five) or any(
        event["contract_valid"] is not True for event in audits
    ):
        fail(f"{slot} audit sequence widened or changed")
    has_call = audit_kinds == exact_five
    guard = audits[2] if has_call else audits[1]
    summary = audits[3] if has_call else audits[2]
    audit = {
        "guarded_api_invocations": guard["guarded_api_invocation_count"],
        "provider_transport_calls": summary["provider_transport_calls"],
        "aborted_provider_calls": summary["aborted_provider_calls"],
        "ledger_event_count": summary["ledger_event_count"],
        "reported_error_count": summary["reported_error_count"],
    }
    expected_audit = (
        {
            "guarded_api_invocations": 0,
            "provider_transport_calls": 1,
            "aborted_provider_calls": 0,
            "ledger_event_count": 4,
            "reported_error_count": 0,
        }
        if has_call
        else {
            "guarded_api_invocations": 0,
            "provider_transport_calls": 0,
            "aborted_provider_calls": 0,
            "ledger_event_count": 0,
            "reported_error_count": 0,
        }
    )
    if audit != expected_audit:
        fail(f"{slot} changed the deterministic provider boundary")
    return events, methods, operations, audit


def expected_arguments(
    profile_arguments: list[dict[str, Any]], receipt_id: str
) -> list[dict[str, Any]]:
    return [*profile_arguments[:4], {"receipt_id": receipt_id}]


def verify_event_observation_window(
    events: list[dict[str, Any]],
    *,
    started: datetime,
    finished: datetime,
) -> None:
    if not events:
        fail("the session event window is empty")
    observed = [parse_time(event["observed_at"]) for event in events]
    if (
        any(value < started or value > finished for value in observed)
        or any(left > right for left, right in zip(observed, observed[1:]))
    ):
        fail("session events are not monotonic within the declared observation window")


def verify_request_argument_bindings(
    requests: list[dict[str, Any]],
    operation_summaries: list[dict[str, Any]],
    profile_arguments: list[dict[str, Any]],
    search_receipt: str,
) -> None:
    if len(requests) != 5 or len(operation_summaries) != 5:
        fail("the exact-five request argument set is incomplete")
    arguments = expected_arguments(profile_arguments, search_receipt)
    for ordinal, operation in enumerate(OPERATIONS):
        encoded = canonical_bytes(arguments[ordinal])
        expected = {
            "operation": operation,
            "valid": True,
            "parameters_bytes": len(encoded),
            "parameters_sha256": sha256_bytes(encoded),
        }
        event = requests[ordinal]
        summary = operation_summaries[ordinal]
        if (
            summary["ordinal"] != ordinal
            or summary["request"] != expected
            or event["operation"] != operation
            or event["arguments_bytes"] != expected["parameters_bytes"]
            or event["arguments_sha256"] != expected["parameters_sha256"]
        ):
            fail(f"the {operation} request arguments do not match the frozen profile")


def verify_sessions(
    private_root: Path,
    manifest: dict[str, Any],
    claim_raw: bytes,
    profile_arguments: list[dict[str, Any]],
    runtime_digests: dict[str, str],
    node_path: str,
    parent_identity: dict[str, Any],
    runtime_closure: dict[str, Any],
    mcp_command_sha256: str,
    event_validator: Draft202012Validator | None = None,
) -> tuple[dict[str, Any], Counter[str], Counter[str], Counter[str], int]:
    session_names = sorted(
        name for name in os.listdir(private_root) if re.fullmatch(r"session-[1-8]", name)
    )
    expected_names = [f"session-{index}" for index in range(1, len(session_names) + 1)]
    if (
        session_names != expected_names
        or len(session_names) != manifest["execution"]["session_count"]
    ):
        fail("private capture does not contain contiguous session-1 to session-8 slots")
    event_check = event_validator or schema_validator(EVENT_SCHEMA)
    capture_validator = schema_validator(CAPTURE_SCHEMA)
    session_validator = schema_validator(SESSION_SCHEMA)
    claim = strict_canonical_object(claim_raw, label="global exact-five claim")
    if (
        set(claim) != {
            "schema", "profile", "run_id", "session_id", "source_commit", "operation_order"
        }
        or claim["schema"] != "gis-ai-go.qual-206-chatgpt-tunnel-exact-five-claim.v1"
        or claim["profile"] != PROFILE_ID
        or claim["run_id"] != manifest["run_id"]
        or claim["source_commit"] != manifest["source"]["commit"]
        or claim["operation_order"] != list(OPERATIONS)
    ):
        fail("global exact-five claim is invalid")
    all_methods: Counter[str] = Counter()
    all_operations: Counter[str] = Counter()
    all_audit: Counter[str] = Counter()
    notification_count = 0
    exact_verified: dict[str, Any] | None = None
    seen_session_ids: set[str] = set()
    execution_started = parse_time(manifest["execution"]["started_at"])
    execution_finished = parse_time(manifest["execution"]["finished_at"])
    for slot in session_names:
        session_root = private_root / slot
        require_directory(session_root, label=slot)
        names = set(os.listdir(session_root))
        if names not in (SESSION_CORE_FILES, SESSION_CORE_FILES | {"exact-five-results.json"}):
            fail(f"{slot} contains an unexpected private file")
        event_raw = read_private(
            session_root / "events.jsonl", maximum=8 * 1_048_576, label=f"{slot} events"
        )
        capture_raw = read_private(
            session_root / "manifest.json", maximum=65_536, label=f"{slot} manifest"
        )
        session_raw = read_private(
            session_root / "exact-five-session.json",
            maximum=65_536,
            label=f"{slot} summary",
        )
        capture = strict_canonical_object(capture_raw, label=f"{slot} manifest")
        session = strict_canonical_object(session_raw, label=f"{slot} summary")
        validate(capture_validator, capture, label=f"{slot} manifest")
        validate(session_validator, session, label=f"{slot} summary")
        if (
            capture["slot"] != slot
            or session["slot"] != slot
            or capture["run_id"] != manifest["run_id"]
            or session["run_id"] != manifest["run_id"]
            or capture["source_commit"] != manifest["source"]["commit"]
            or session["source_commit"] != manifest["source"]["commit"]
            or capture["session_id"] != session["session_id"]
            or session["session_id"] in seen_session_ids
            or capture["session_profile"] != session["session_profile"]
            or capture["protocol_session_status"] != session["protocol_session_status"]
        ):
            fail(f"{slot} has inconsistent run or session identity")
        seen_session_ids.add(session["session_id"])
        if capture["event_log"] != {
            "bytes": len(event_raw),
            "event_count": len(event_raw[:-1].split(b"\n")),
            "last_event_sha256": json.loads(event_raw.splitlines()[-1])["event_sha256"],
            "sha256": sha256_bytes(event_raw),
        }:
            fail(f"{slot} manifest does not bind its event log")
        if capture["session_summary"] != {
            "name": "exact-five-session.json",
            "bytes": len(session_raw),
            "sha256": sha256_bytes(session_raw),
        }:
            fail(f"{slot} manifest does not bind its session summary")
        events, methods, operations, audit = verify_event_log(
            event_raw,
            slot=slot,
            run_id=manifest["run_id"],
            session_id=session["session_id"],
            source_commit=manifest["source"]["commit"],
            parent_identity=parent_identity,
            runtime_digests=runtime_digests,
            runtime_closure=runtime_closure,
            mcp_command_sha256=mcp_command_sha256,
            event_validator=event_check,
        )
        verify_event_observation_window(
            events,
            started=execution_started,
            finished=execution_finished,
        )
        start = events[0]
        end = events[-1]
        if (
            start["client"] != capture["client"]
            or end["session_profile"] != session["session_profile"]
            or end["protocol_session_status"] != session["protocol_session_status"]
            or session["protocol_session_status"] != "passed"
            or session["session_profile"] == "invalid"
            or session["counts"]
            != {
                "request_count": sum(methods.values()),
                "response_count": sum(methods.values()),
                "notification_count": end["notification_count"],
                "tool_call_count": operations.total(),
            }
            or session["audit"]
            != {
                "contract_valid": True,
                "guard_ready": True,
                "guard_summary": True,
                **audit,
            }
        ):
            fail(f"{slot} summary does not match its event trace")
        material = capture["result_material"]
        if material != session["result_material"]:
            fail(f"{slot} result-material bindings differ")
        if material is None:
            if "exact-five-results.json" in names or session["operations"]:
                fail(f"{slot} negotiation session retained capability material")
            if session["global_claim"] is not None:
                fail(f"{slot} negotiation session retained the global claim")
        else:
            if "exact-five-results.json" not in names:
                fail(f"{slot} call-bearing session omitted result material")
            result_raw = read_private(
                session_root / "exact-five-results.json",
                maximum=6 * 1_048_576,
                label=f"{slot} result material",
            )
            if material != {
                "name": "exact-five-results.json",
                "bytes": len(result_raw),
                "sha256": sha256_bytes(result_raw),
            }:
                fail(f"{slot} result material is not content-bound")
            independent = independently_verify_results(result_raw, node_path=node_path)
            if exact_verified is not None:
                fail("the run contains more than one call-bearing session")
            exact_verified = independent
            if (
                independent["run_id"] != manifest["run_id"]
                or independent["session_id"] != session["session_id"]
                or independent["profile"] != PROFILE_ID
                or independent["resources_advertised"] != 0
                or independent["tool_schema_projection_applied"] is not False
                or session["canonical_tool_schema"]
                != {
                    "observed": True,
                    "exact": True,
                    "tools_sha256": independent["canonical_tools_sha256"],
                    "projection_applied": False,
                }
            ):
                fail(f"{slot} canonical tool or result context is invalid")
            if session["global_claim"] != {
                "bytes": len(claim_raw),
                "sha256": sha256_bytes(claim_raw),
            } or claim["session_id"] != session["session_id"]:
                fail("global exact-five claim does not bind the call session")
            operation_summaries = session["operations"]
            independent_operations = independent["operations"]
            if len(operation_summaries) != 5 or len(independent_operations) != 5:
                fail("the exact-five session is incomplete")
            search_receipt = independent_operations[0]["receipt_id"]
            requests = [
                event for event in events
                if event["event"] == "request" and event["method"] == "tools/call"
            ]
            responses = [
                event for event in events
                if event["event"] == "response" and event["request_method"] == "tools/call"
            ]
            verify_request_argument_bindings(
                requests,
                operation_summaries,
                profile_arguments,
                search_receipt,
            )
            for ordinal, operation in enumerate(OPERATIONS):
                item = operation_summaries[ordinal]
                independent_item = independent_operations[ordinal]
                response = item["response"]
                if (
                    response["operation"] != operation
                    or response["receipt_id"] != independent_item["receipt_id"]
                    or responses[ordinal]["operation"] != operation
                    or responses[ordinal]["receipt_id"] != independent_item["receipt_id"]
                    or any(
                        response[name] is not True
                        for name in (
                            "receipt_present", "receipt_verification_valid",
                            "output_contract_valid", "structured_plain_text_parity",
                        )
                    )
                ):
                    fail(f"the {operation} request, response or receipt is invalid")
            if (
                session["inspection_relationship"] != independent["inspection_relationship"]
                or session["inspection_relationship"]["valid"] is not True
                or operation_summaries[-1]["response"]["inspected_receipt_id"]
                != search_receipt
                or operation_summaries[-1]["response"]["inspection_relationship_valid"]
                is not True
            ):
                fail("the search-to-inspection relationship is invalid")
        all_methods.update(methods)
        all_operations.update(operations)
        all_audit.update(audit)
        notification_count += end["notification_count"]
    if exact_verified is None:
        fail("the run has no complete exact-five result session")
    if all_operations != Counter({operation: 1 for operation in OPERATIONS}):
        fail("the run did not complete each exact-five operation once")
    if all_methods["tools/list"] < 1 or all_methods["tools/call"] != 5:
        fail("the run did not complete discovery and exact-five invocation")
    if all_audit != Counter(
        {
            "guarded_api_invocations": 0,
            "provider_transport_calls": 1,
            "aborted_provider_calls": 0,
            "ledger_event_count": 4,
            "reported_error_count": 0,
        }
    ):
        fail("the aggregate deterministic provider boundary changed")
    return exact_verified, all_methods, all_operations, all_audit, notification_count


def verify_and_project(
    private_root: Path,
    *,
    node_path: Path,
    pnpm_path: Path,
    source_verifier: Callable[[dict[str, Any]], None] | None = None,
    private_validator: Draft202012Validator | None = None,
    public_validator: Draft202012Validator | None = None,
    event_validator: Draft202012Validator | None = None,
    runtime_reproducer: Callable[[str, str, Path], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    explicit_node_path = locate_verified_node(node_path)
    explicit_pnpm_path = Path(require_explicit_pnpm_path(pnpm_path))
    root_state = require_directory(private_root, label="private root")
    manifest_raw = read_private(
        private_root / "run-manifest.json",
        maximum=1_048_576,
        label="private run manifest",
    )
    manifest = strict_canonical_object(manifest_raw, label="private run manifest")
    validate(
        private_validator or schema_validator(PRIVATE_SCHEMA),
        manifest,
        label="private run manifest",
    )
    expected_root_names = {
        "run-manifest.json", CLAIM_NAME, STATUS_BEFORE_NAME, STATUS_AFTER_NAME,
        STATUS_STOPPED_NAME,
        *{f"session-{index}" for index in range(1, manifest["execution"]["session_count"] + 1)},
    }
    if set(os.listdir(private_root)) != expected_root_names:
        fail("private root does not contain the exact finalised capture set")
    claim_raw = verify_bound_file(
        private_root,
        manifest["private_files"]["claim"],
        maximum=2_048,
        label="global exact-five claim",
    )
    before_raw = verify_bound_file(
        private_root,
        manifest["private_files"]["status_before"],
        maximum=65_536,
        label="tunnel status before",
    )
    after_raw = verify_bound_file(
        private_root,
        manifest["private_files"]["status_after"],
        maximum=65_536,
        label="tunnel status after",
    )
    stopped_raw = verify_bound_file(
        private_root,
        manifest["private_files"]["status_stopped"],
        maximum=65_536,
        label="tunnel status stopped",
    )
    mcp_command_sha256 = verify_statuses(
        before_raw,
        after_raw,
        stopped_raw,
        manifest,
        schema_validator(STATUS_SCHEMA),
    )
    (source_verifier or verify_source)(manifest)
    _profile, profile_arguments, profile_sha256 = load_profile()
    runtime_digests = source_runtime_digests(profile_sha256)
    runtime_closure = (
        runtime_reproducer(
            manifest["source"]["commit"],
            explicit_node_path,
            explicit_pnpm_path,
        )
        if runtime_reproducer is not None
        else independently_reproduce_runtime_closure(
            manifest["source"]["commit"],
            node_path=explicit_node_path,
            pnpm_path=explicit_pnpm_path,
        )
    )
    if runtime_closure != manifest["runtime"]:
        fail("private runtime closure differs from the independent source reference build")
    independent, methods, _operations, audit, notification_count = verify_sessions(
        private_root,
        manifest,
        claim_raw,
        profile_arguments,
        runtime_digests,
        explicit_node_path,
        {
            "bytes": manifest["tunnel_client"]["binary_bytes"],
            "sha256": manifest["tunnel_client"]["binary_sha256"],
        },
        runtime_closure,
        mcp_command_sha256,
        event_validator,
    )
    if (
        manifest["execution"]["classification"] != "complete"
        or manifest["execution"]["exit_code"] is not None
        or manifest["execution"]["signal"] is not None
        or manifest["claims"] != EXPECTED_CLAIMS
        or manifest["isolation"]["guarded_live_provider_api_invocations"] != 0
    ):
        fail("private run did not complete within the accepted claim boundary")
    projection = {
        "schema": "gis-ai-go.qual-206-chatgpt-tunnel-exact-five-evidence.v1",
        "status": "capability_pass",
        "observed_at": manifest["execution"]["finished_at"],
        "source": {
            "repository": "chris-page-gov/gis-ai-go",
            "repository_origin": manifest["source"]["repository_origin"],
            "commit": manifest["source"]["commit"],
            "tree": manifest["source"]["tree"],
            "version": "0.1.0",
            "local_origin_main_match": True,
            "protected_main_verification": "external-publication-gate",
            "production_activation": False,
        },
        "runtime": runtime_closure,
        "host": dict(manifest["host"]),
        "tunnel": {
            "local_alias": manifest["tunnel"]["local_alias"],
            "remote_name": manifest["tunnel"]["remote_name"],
            "remote_id": manifest["tunnel"]["remote_id"],
            "connection_kind": manifest["tunnel"]["connection_kind"],
            "client_version": manifest["tunnel_client"]["reported_version"],
            "client_binary_sha256": manifest["tunnel_client"]["binary_sha256"],
            "client_archive_sha256": manifest["tunnel_client"]["archive_sha256"],
            "profile_name": manifest["tunnel"]["local_alias"],
            "target_kind": "command",
            "mcp_command_sha256": mcp_command_sha256,
            "preflight_healthy": True,
            "postflight_healthy": True,
            "teardown_verified": True,
            "local_mcp_child_transport": "stdio",
            "direct_public_streamable_http_tls": False,
        },
        "profile": {
            "id": PROFILE_ID,
            "profile_sha256": profile_sha256,
            "operation_order": list(OPERATIONS),
        },
        "transport": {
            "protocol": PROTOCOL,
            "remote_host_kind": "openai-secure-tunnel",
            "local_child_kind": "operating-system-stdio-pipes",
            "session_count": manifest["execution"]["session_count"],
            "request_count": sum(methods.values()),
            "response_count": sum(methods.values()),
            "notification_count": notification_count,
            "tool_call_count": 5,
            "resource_read_count": 0,
            "resources_advertised": independent["resources_advertised"],
            "canonical_tools_sha256": independent["canonical_tools_sha256"],
            "tool_schema_projection_applied": False,
            "provider_transport_calls": audit["provider_transport_calls"],
            "aborted_provider_calls": audit["aborted_provider_calls"],
            "ledger_event_count": audit["ledger_event_count"],
            "guarded_provider_api_invocations": audit["guarded_api_invocations"],
        },
        "result": {
            "classification": "capability_pass",
            "capability": "passed",
            "profile": PROFILE_ID,
            "operation_order": list(OPERATIONS),
            "operation_receipts": independent["operations"],
            "inspection_relationship": independent["inspection_relationship"],
            "independent_result_verification": True,
        },
        "isolation": {
            "observer_credentials_observed": False,
            "mcp_child_recognised_credentials_forwarded": False,
            "mcp_child_network_access_allowed": False,
            "mcp_child_network_sandbox": NETWORK_SANDBOX,
            "provider_egress_guard_ready": True,
            "raw_host_material_published": False,
        },
        "claims": dict(EXPECTED_CLAIMS),
        "private_capture": {
            "retained_local": True,
            "published": False,
            "run_manifest_sha256": sha256_bytes(manifest_raw),
            "claim_sha256": sha256_bytes(claim_raw),
            "result_material_sha256": independent["result_material_sha256"],
        },
        "boundary": BOUNDARY,
    }
    validate(
        public_validator or schema_validator(PUBLIC_SCHEMA),
        projection,
        label="public projection",
    )
    rendered = json.dumps(projection, ensure_ascii=False, separators=(",", ":"))
    if FORBIDDEN_PUBLIC_TEXT.search(rendered):
        fail("public projection contains a forbidden local, credential or endpoint value")
    if nested_field_names(projection) & FORBIDDEN_PUBLIC_FIELDS:
        fail("public projection contains a forbidden private field")
    after = private_root.lstat()
    if (root_state.st_dev, root_state.st_ino, root_state.st_mode, root_state.st_uid) != (
        after.st_dev,
        after.st_ino,
        after.st_mode,
        after.st_uid,
    ):
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
            "Verify one private ChatGPT secure-tunnel exact-five run and publish a "
            "pass-only path-free projection."
        )
    )
    parser.add_argument("--private-root", required=True, type=Path)
    parser.add_argument("--node", required=True, type=Path)
    parser.add_argument("--pnpm", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    try:
        projection = verify_and_project(
            arguments.private_root,
            node_path=arguments.node,
            pnpm_path=arguments.pnpm,
        )
        publish_projection(arguments.output, projection)
    except (
        OSError,
        TunnelExactFiveVerificationError,
        host002.CapabilityVerificationError,
        composite.VerificationError,
    ) as error:
        print(
            f"QUAL-206 ChatGPT tunnel exact-five verification failed: {error}",
            file=sys.stderr,
        )
        return 1
    print("QUAL-206 ChatGPT tunnel exact-five pass verified and projected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
