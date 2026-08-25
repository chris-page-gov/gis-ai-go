#!/usr/bin/env python3
"""Verify one private two-session Claude Code QUAL-206 observation."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import math
import os
import stat
import sys
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, NoReturn

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
EVENT_SCHEMA_PATH = (
    ROOT / "schemas" / "qual-206-claude-composite-host-event-v1.schema.json"
)
CAPTURE_SCHEMA_PATH = (
    ROOT
    / "schemas"
    / "qual-206-claude-composite-host-event-capture-v1.schema.json"
)
EVENT_SCHEMA_ID = "gis-ai-go.qual-206-claude-composite-host-event.v1"
EVENT_DOMAIN = EVENT_SCHEMA_ID
DOMAIN_SEPARATION_PREFIX = b"GIS-AI-GO\0canonical-json\0sha256\0v1\0"
EXPECTED_SLOTS = ("session-1", "session-2")
EXPECTED_CAPTURE_FILES = {"events.jsonl", "manifest.json"}
EXACT_OPERATIONS = {
    "catalogue.search",
    "catalogue.describe",
    "selection.resolve",
    "data.query",
    "evidence.inspect",
}
MAX_EVENT_LOG_BYTES = 8 * 1024 * 1024
MAX_MANIFEST_BYTES = 64 * 1024
MAX_EVENT_COUNT = 512
SHA256_PATTERN = "0123456789abcdef"
COMMON_EVENT_FIELDS = {
    "schema",
    "run_id",
    "session_id",
    "slot",
    "sequence",
    "observed_at",
    "event",
    "previous_event_sha256",
    "event_sha256",
}
EVENT_FIELDS = {
    "request": {
        "direction",
        "frame_bytes",
        "frame_sha256",
        "request_ordinal",
        "request_id_sha256",
        "request_id_kind",
        "request_id_unique",
        "method",
        "operation",
        "protocol_claim",
    },
    "notification": {
        "direction",
        "frame_bytes",
        "frame_sha256",
        "notification_ordinal",
        "method",
        "protocol_claim",
        "target_request_id_sha256",
        "target_request_id_kind",
    },
    "response": {
        "direction",
        "frame_bytes",
        "frame_sha256",
        "response_ordinal",
        "request_id_sha256",
        "request_id_kind",
        "correlation",
        "request_method",
        "outcome",
        "error_code",
        "duration_ms",
        "semantic",
        "contract_valid",
    },
    "audit": {
        "direction",
        "frame_bytes",
        "frame_sha256",
        "audit_kind",
        "contract_valid",
        "ordinal",
        "guarded_api_invocation_count",
        "provider_transport_calls",
        "aborted_provider_calls",
        "ledger_event_count",
        "reported_error_count",
    },
    "anomaly": {"classification", "direction", "frame_bytes", "frame_sha256"},
    "stream": {"stream_name", "stream_phase", "bytes", "frames", "sha256", "graceful"},
}
LIFECYCLE_FIELDS = {
    "session-start": {
        "phase",
        "client",
        "source_commit",
        "protocol_target",
        "transport",
        "immediate_parent",
        "source_checkout",
        "observer_runtime",
        "capture_boundaries",
        "credential_environment_forwarded",
        "credential_environment_observed",
        "child_environment_mode",
        "host_attribution",
    },
    "child-spawned": {
        "phase",
        "fixture_arguments_match_observer_contract",
        "spawned_process_identity_verified",
    },
    "child-exit": {"phase", "exit_code", "signal"},
    "session-end": {
        "phase",
        "session_profile",
        "protocol_session_status",
        "capability_scored",
        "host_capability",
        "source_binding_ready",
        "runtime_materials_stable",
        "source_checkout_stable",
        "closure_stimulus",
        "exit_code",
        "signal",
        "request_count",
        "response_count",
        "notification_count",
        "pending_request_count",
        "stderr_event_count",
        "stderr_bytes",
        "stderr_sha256",
        "anomaly_count",
        "prior_event_count",
        "prior_event_log_bytes",
        "prior_event_log_sha256",
        "temporary_state_removed",
    },
}
NETWORK_SANDBOX_FIELDS = {
    "mcp_subtree_network_access_allowed",
    "mcp_subtree_network_sandbox",
}


class VerificationError(ValueError):
    """The private capture does not satisfy the closed replay contract."""


@dataclass(frozen=True)
class PrivateFile:
    raw: bytes
    identity: tuple[int, int]


@dataclass(frozen=True)
class SessionResult:
    run_id: str
    session_id: str
    slot: str
    profile: str
    source_commit: str
    immediate_parent: dict[str, Any]
    observer_runtime: dict[str, Any]
    client: str
    request_count: int


@dataclass(frozen=True)
class CompositeResult:
    negotiation_request_count: int
    modern_request_count: int


def fail(message: str) -> NoReturn:
    raise VerificationError(message)


def reject_duplicate_members(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail("JSON contains a duplicate object member")
        result[key] = value
    return result


def reject_non_standard_number(value: str) -> NoReturn:
    fail(f"JSON contains the non-standard number {value}")


def parse_json(raw: bytes, *, label: str) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise VerificationError(f"{label} is not strict UTF-8") from error
    if text.startswith("\ufeff"):
        fail(f"{label} must not contain a byte-order mark")
    try:
        value = json.loads(
            text,
            object_pairs_hook=reject_duplicate_members,
            parse_constant=reject_non_standard_number,
        )
    except (json.JSONDecodeError, RecursionError) as error:
        raise VerificationError(f"{label} is not one bounded JSON object") from error
    if not isinstance(value, dict):
        fail(f"{label} must contain one JSON object")
    return value


def _assert_scalar_string(value: str) -> None:
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        fail("canonical JSON cannot contain an unpaired surrogate")


def _encode_string(value: str) -> str:
    _assert_scalar_string(value)
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _ecmascript_number(value: int | float) -> str:
    if isinstance(value, int):
        return str(value)
    if not math.isfinite(value):
        fail("canonical JSON numbers must be finite")
    if value == 0:
        return "0"

    negative = value < 0
    decimal = Decimal(repr(abs(value)))
    sign, decimal_digits, exponent = decimal.as_tuple()
    if sign != 0 or not decimal_digits:
        fail("canonical JSON number conversion failed")
    digits = list(decimal_digits)
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
        exponent += 1
    rendered_digits = "".join(str(digit) for digit in digits)
    digit_count = len(rendered_digits)
    decimal_point = digit_count + exponent

    if 0 < decimal_point <= 21:
        if digit_count <= decimal_point:
            rendered = rendered_digits + ("0" * (decimal_point - digit_count))
        else:
            rendered = (
                rendered_digits[:decimal_point]
                + "."
                + rendered_digits[decimal_point:]
            )
    elif -6 < decimal_point <= 0:
        rendered = "0." + ("0" * (-decimal_point)) + rendered_digits
    else:
        coefficient = rendered_digits[0]
        if digit_count > 1:
            coefficient += "." + rendered_digits[1:]
        scientific_exponent = decimal_point - 1
        exponent_text = (
            f"+{scientific_exponent}"
            if scientific_exponent >= 0
            else str(scientific_exponent)
        )
        rendered = f"{coefficient}e{exponent_text}"
    return f"-{rendered}" if negative else rendered


def canonical_json(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return _ecmascript_number(value)
    if isinstance(value, str):
        return _encode_string(value)
    if isinstance(value, list):
        return "[" + ",".join(canonical_json(item) for item in value) + "]"
    if isinstance(value, dict):
        for key in value:
            if not isinstance(key, str):
                fail("canonical JSON object members must have string names")
            _assert_scalar_string(key)
        ordered_keys = sorted(value, key=lambda key: key.encode("utf-16-be"))
        members = (
            f"{_encode_string(key)}:{canonical_json(value[key])}"
            for key in ordered_keys
        )
        return "{" + ",".join(members) + "}"
    fail("value is outside the canonical JSON data model")


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return canonical_json(value).encode("utf-8")
    except RecursionError as error:
        raise VerificationError("canonical JSON exceeds the nesting boundary") from error


def domain_separated_sha256(value: Any) -> str:
    digest = hashlib.sha256()
    digest.update(DOMAIN_SEPARATION_PREFIX)
    digest.update(EVENT_DOMAIN.encode("utf-8"))
    digest.update(b"\0")
    digest.update(canonical_json_bytes(value))
    return digest.hexdigest()


def _file_state(metadata: os.stat_result) -> tuple[int, ...]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_uid,
        metadata.st_nlink,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _directory_state(metadata: os.stat_result) -> tuple[int, ...]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_uid,
        metadata.st_nlink,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _require_canonical_absolute_path(path: Path, *, label: str) -> None:
    if not path.is_absolute() or Path(os.path.abspath(path)) != path:
        fail(f"{label} path must be canonical and absolute")
    if "\0" in os.fspath(path):
        fail(f"{label} path is invalid")
    try:
        real = Path(os.path.realpath(path))
        parent_real = Path(os.path.realpath(path.parent))
    except OSError as error:
        raise VerificationError(f"{label} path is unavailable") from error
    if real != path or parent_real != path.parent:
        fail(f"{label} path must not traverse an alias")


def _require_private_directory(path: Path, *, label: str) -> os.stat_result:
    if not hasattr(os, "getuid"):
        fail("owner-only observation verification requires a POSIX user identity")
    try:
        metadata = path.lstat()
    except OSError as error:
        raise VerificationError(f"{label} is unavailable") from error
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISDIR(metadata.st_mode)
        or metadata.st_uid != os.getuid()
        or stat.S_IMODE(metadata.st_mode) != 0o700
    ):
        fail(f"{label} must be one current-user directory with mode 0700")
    return metadata


def _directory_names(path: Path, *, label: str) -> set[str]:
    try:
        names = set(os.listdir(path))
    except OSError as error:
        raise VerificationError(f"{label} could not be enumerated") from error
    return names


def read_private_file(path: Path, *, maximum_bytes: int, label: str) -> PrivateFile:
    """Read one stable, owner-only, single-link regular file."""
    _require_canonical_absolute_path(path, label=label)
    parent_before = _require_private_directory(path.parent, label=f"{label} parent")
    try:
        before = path.lstat()
    except OSError as error:
        raise VerificationError(f"{label} is unavailable") from error
    if (
        stat.S_ISLNK(before.st_mode)
        or not stat.S_ISREG(before.st_mode)
        or before.st_uid != os.getuid()
        or before.st_nlink != 1
        or stat.S_IMODE(before.st_mode) != 0o600
        or before.st_size < 1
        or before.st_size > maximum_bytes
    ):
        fail(f"{label} must be one bounded owner-only regular file with mode 0600")

    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise VerificationError(f"{label} could not be opened safely") from error
    try:
        opened = os.fstat(descriptor)
        if _file_state(opened) != _file_state(before):
            fail(f"{label} changed while it was opened")
        chunks: list[bytes] = []
        total = 0
        while total <= maximum_bytes:
            chunk = os.read(descriptor, min(65536, maximum_bytes + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
        after = os.fstat(descriptor)
        if (
            _file_state(after) != _file_state(opened)
            or total != opened.st_size
            or total > maximum_bytes
        ):
            fail(f"{label} changed or exceeded its byte boundary while being read")
    finally:
        os.close(descriptor)
    parent_after = _require_private_directory(path.parent, label=f"{label} parent")
    if _directory_state(parent_after) != _directory_state(parent_before):
        fail(f"{label} parent changed while being read")
    return PrivateFile(raw=b"".join(chunks), identity=(opened.st_dev, opened.st_ino))


def load_schema(path: Path, *, label: str) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise VerificationError(f"{label} is unavailable") from error
    if not raw or len(raw) > 1024 * 1024:
        fail(f"{label} is outside its repository byte boundary")
    schema = parse_json(raw, label=label)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as error:
        raise VerificationError(f"{label} is not a valid Draft 2020-12 schema") from error
    return schema


def validate_instance(
    validator: Draft202012Validator,
    value: dict[str, Any],
    *,
    label: str,
) -> None:
    try:
        errors = sorted(
            validator.iter_errors(value),
            key=lambda error: (
                tuple(str(part) for part in error.absolute_path),
                tuple(str(part) for part in error.absolute_schema_path),
            ),
        )
    except RecursionError as error:
        raise VerificationError(f"{label} exceeds the schema nesting boundary") from error
    if errors:
        error = errors[0]
        location = "$" + "".join(
            f"[{part}]" if isinstance(part, int) else f".{part}"
            for part in error.absolute_path
        )
        fail(f"{label} does not satisfy the closed schema at {location}")


def _read_event_lines(raw: bytes) -> list[bytes]:
    if not raw.endswith(b"\n") or raw.endswith(b"\r\n"):
        fail("event log must end with one canonical LF-delimited event")
    lines = raw.splitlines(keepends=True)
    if not lines or len(lines) > MAX_EVENT_COUNT:
        fail("event log has an invalid event count")
    if any(not line.endswith(b"\n") or line in {b"\n", b"\r\n"} for line in lines):
        fail("event log contains an empty or unterminated event")
    return lines


def _validate_sha256(value: str, *, label: str) -> None:
    if len(value) != 64 or any(character not in SHA256_PATTERN for character in value):
        fail(f"{label} must be a lowercase SHA-256 digest")


def _validate_uuid_v4(value: str, *, label: str) -> None:
    import uuid

    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError) as error:
        raise VerificationError(f"{label} must be a UUID") from error
    if str(parsed) != value or parsed.version != 4:
        fail(f"{label} must be one canonical UUIDv4")


def _require_boolean(mapping: dict[str, Any], name: str, expected: bool) -> None:
    if mapping.get(name) is not expected:
        fail(f"{name} has an invalid composite-observation value")


def _require_exact_event_fields(event: dict[str, Any]) -> None:
    kind = event["event"]
    if kind == "lifecycle":
        expected = COMMON_EVENT_FIELDS | LIFECYCLE_FIELDS[event["phase"]]
        if event["phase"] in {"session-start", "child-spawned"} and any(
            name in event for name in NETWORK_SANDBOX_FIELDS
        ):
            expected |= NETWORK_SANDBOX_FIELDS
    else:
        expected = COMMON_EVENT_FIELDS | EVENT_FIELDS[kind]
    if set(event) != expected:
        fail(f"{kind} event does not contain its exact closed projection")


def _require_clean_session_end(end: dict[str, Any]) -> None:
    if (
        end["protocol_session_status"] != "passed"
        or end["exit_code"] != 0
        or end["signal"] is not None
        or end["pending_request_count"] != 0
        or end["stderr_event_count"] != 0
        or end["stderr_bytes"] != 0
        or end["stderr_sha256"] is not None
        or end["anomaly_count"] != 0
        or end["runtime_materials_stable"] is not True
        or end["source_checkout_stable"] is not True
        or end["closure_stimulus"]
        not in {
            "stdin-eof",
            "sigint",
            "sigterm",
            "stdin-eof-and-sigint",
            "stdin-eof-and-sigterm",
        }
        or end["temporary_state_removed"] is not True
    ):
        fail("session-end does not describe one clean, complete observation")
    _require_boolean(end, "capability_scored", False)
    _require_boolean(end, "host_capability", False)
    _require_boolean(end, "source_binding_ready", False)


def _verify_request_response_contract(
    requests: list[dict[str, Any]],
    responses: list[dict[str, Any]],
) -> None:
    expected_semantics = {
        "server/discover": "discover-pass",
        "tools/list": "tools-list-pass",
        "resources/list": "resources-list-pass",
        "resources/templates/list": "resource-templates-pass",
        "resources/read": "resource-read-pass",
        "tools/call": "tool-call-pass",
    }
    request_by_digest: dict[str, dict[str, Any]] = {}
    for ordinal, request in enumerate(requests):
        operation_valid = (
            request["operation"] in EXACT_OPERATIONS
            if request["method"] == "tools/call"
            else request["operation"] == "not-applicable"
        )
        if (
            request["request_ordinal"] != ordinal
            or request["direction"] != "host-to-fixture"
            or request["request_id_sha256"] in request_by_digest
            or request["request_id_unique"] is not True
            or request["request_id_sha256"] is None
            or request["request_id_kind"] not in {"integer", "string"}
            or request["protocol_claim"] != "2026-07-28"
            or not operation_valid
        ):
            fail("request sequence, identity, protocol or operation projection is invalid")
        request_by_digest[request["request_id_sha256"]] = request

    if len(responses) != len(requests):
        fail("successful session must correlate one response to every request")
    seen: set[str] = set()
    for ordinal, response in enumerate(responses):
        digest = response["request_id_sha256"]
        request = request_by_digest.get(digest)
        expected_semantic = (
            expected_semantics.get(request["method"]) if request is not None else None
        )
        if (
            response["response_ordinal"] != ordinal
            or request is None
            or digest in seen
            or response["direction"] != "fixture-to-host"
            or response["request_id_kind"] != request["request_id_kind"]
            or response["request_method"] != request["method"]
            or response["correlation"] != "matched"
            or response["outcome"] != "success"
            or response["error_code"] is not None
            or response["duration_ms"] is None
            or response["contract_valid"] is not True
            or response["sequence"] <= request["sequence"]
            or expected_semantic is None
            or response["semantic"] != expected_semantic
        ):
            fail("response projection is not one contract-valid correlated success")
        seen.add(digest)


def _verify_profile(
    profile: str,
    requests: list[dict[str, Any]],
    responses: list[dict[str, Any]],
    notifications: list[dict[str, Any]],
) -> None:
    if profile == "negotiation-probe":
        if (
            len(requests) != 1
            or notifications
            or requests[0]["method"] != "server/discover"
        ):
            fail("negotiation probe must contain exactly one server/discover request")
        if (
            len(responses) != 1
            or responses[0]["semantic"] != "discover-pass"
            or responses[0]["request_method"] != "server/discover"
        ):
            fail("negotiation probe must contain one contract-valid discover success")
        return
    if profile != "modern-session":
        fail("capture contains an invalid session profile")
    if not requests:
        fail("modern session must contain at least one request")
    if any(request["method"] == "initialize" for request in requests):
        fail("modern session must not use legacy initialize")
    if any(request["protocol_claim"] != "2026-07-28" for request in requests):
        fail("every modern-session request must claim MCP 2026-07-28")
    matching = [
        response
        for response in responses
        if response["request_method"] == "tools/list"
        and response["semantic"] == "tools-list-pass"
    ]
    if not matching:
        fail("modern session must contain a contract-valid tools/list success")


def _verify_notifications(
    notifications: list[dict[str, Any]],
    requests: list[dict[str, Any]],
    responses: list[dict[str, Any]],
) -> None:
    request_by_identity = {
        request["request_id_sha256"]: request
        for request in requests
    }
    response_by_identity = {
        response["request_id_sha256"]: response
        for response in responses
    }
    cancelled: set[str] = set()
    for ordinal, notification in enumerate(notifications):
        target = notification["target_request_id_sha256"]
        request = request_by_identity.get(target)
        response = response_by_identity.get(target)
        if (
            notification["notification_ordinal"] != ordinal
            or notification["direction"] != "host-to-fixture"
            or notification["method"] != "notifications/cancelled"
            or notification["protocol_claim"] != "2026-07-28"
            or target is None
            or notification["target_request_id_kind"] not in {"integer", "string"}
            or request is None
            or response is None
            or request["request_id_kind"] != notification["target_request_id_kind"]
            or not (
                request["sequence"]
                < notification["sequence"]
                < response["sequence"]
            )
            or target in cancelled
        ):
            fail("notification sequence or protocol projection is invalid")
        cancelled.add(target)


def _verify_streams(
    streams: list[dict[str, Any]],
    *,
    requests: list[dict[str, Any]],
    responses: list[dict[str, Any]],
    notifications: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    session_end: dict[str, Any],
) -> None:
    terminal: dict[str, dict[str, Any]] = {}
    for stream in streams:
        if stream["stream_phase"] == "end":
            name = stream["stream_name"]
            if name in terminal:
                fail("session contains a duplicate terminal stream projection")
            terminal[name] = stream
    if not terminal or len(terminal) != len(streams):
        fail("session must contain only one terminal projection per captured stream")

    # The observer schemas close the names; these semantic totals bind the framed
    # streams without retaining raw client or server payloads.
    expected_by_direction = {
        "host-to-fixture": requests + notifications,
        "fixture-to-host": responses,
    }
    for direction, events in expected_by_direction.items():
        candidates = [
            stream
            for name, stream in terminal.items()
            if direction in name
            or (direction == "host-to-fixture" and name in {"stdin", "host-stdin"})
            or (
                direction == "fixture-to-host"
                and name in {"stdout", "server-stdout", "fixture-stdout"}
            )
        ]
        if candidates:
            expected_bytes = sum(event["frame_bytes"] for event in events)
            expected_frames = len(events)
            if len(candidates) != 1 or (
                candidates[0]["bytes"] != expected_bytes
                or candidates[0]["frames"] != expected_frames
            ):
                fail(f"{direction} stream projection does not match captured frames")

    audit_candidates = [
        stream
        for name, stream in terminal.items()
        if "audit" in name
    ]
    if audit_candidates and (
        len(audit_candidates) != 1
        or audit_candidates[0]["frames"] != len(audits)
        or audit_candidates[0]["bytes"]
        != sum(audit["frame_bytes"] for audit in audits)
    ):
        fail("audit stream projection does not match captured audits")
    stderr_candidates = [
        stream for name, stream in terminal.items() if "stderr" in name
    ]
    if stderr_candidates and any(
        stream["bytes"] != session_end["stderr_bytes"]
        or stream["frames"] != session_end["stderr_event_count"]
        for stream in stderr_candidates
    ):
        fail("successful composite observation must have an empty stderr stream")

    if set(terminal) != {
        "host-stdin",
        "fixture-stdout",
        "fixture-audit",
        "fixture-stderr",
    }:
        fail("session does not close exactly the four observed streams")
    if any(stream["graceful"] is not True for stream in terminal.values()):
        fail("successful composite observation contains a non-graceful stream")
    if any(stream["sha256"] is not None for stream in terminal.values()):
        fail("zero-stderr successful stream summaries must not expose a digest")


def _verify_audits(
    audits: list[dict[str, Any]],
    *,
    capability_sandbox: bool,
    requests: list[dict[str, Any]],
    responses: list[dict[str, Any]],
) -> None:
    expected = (
        "provider-egress-guard-ready",
        "provider-egress-guard-summary",
        "session-summary",
    )
    if tuple(audit["audit_kind"] for audit in audits) != expected:
        fail("session does not contain the exact zero-provider audit sequence")
    successful_response_ids = {
        response["request_id_sha256"]
        for response in responses
        if response["request_method"] == "tools/call"
        and response["outcome"] == "success"
        and response["contract_valid"] is True
    }
    expected_ledger_events = sum(
        request["operation"] == "catalogue.search"
        and request["request_id_sha256"] in successful_response_ids
        for request in requests
    ) if capability_sandbox else 0
    if expected_ledger_events not in {0, 1}:
        fail("capability session exceeds the one-call ledger boundary")
    for audit in audits:
        if (
            audit["direction"] != "fixture-audit"
            or audit["contract_valid"] is not True
        ):
            fail("session contains an invalid audit projection")
        kind = audit["audit_kind"]
        if kind == "provider-egress-guard-ready":
            expected_counts = (None, None, None, None, None)
        elif kind == "provider-egress-guard-summary":
            expected_counts = (0, None, None, None, None)
        else:
            expected_counts = (None, 0, 0, expected_ledger_events, 0)
        if (
            audit["guarded_api_invocation_count"],
            audit["provider_transport_calls"],
            audit["aborted_provider_calls"],
            audit["ledger_event_count"],
            audit["reported_error_count"],
        ) != expected_counts or audit["ordinal"] is not None:
            fail("session reports provider activity or an unsafe audit projection")


def verify_session(
    *,
    slot: str,
    event_file: PrivateFile,
    manifest_file: PrivateFile,
    event_validator: Draft202012Validator,
    capture_validator: Draft202012Validator,
    expected_run_id: str,
    expected_source_commit: str,
    expected_parent_sha256: str,
    expected_parent_bytes: int,
) -> SessionResult:
    if event_file.identity == manifest_file.identity:
        fail("event log and manifest must be distinct files")
    if not manifest_file.raw.endswith(b"\n") or manifest_file.raw.endswith(b"\r\n"):
        fail("capture manifest must be one canonical LF-terminated JSON object")
    manifest_body = manifest_file.raw[:-1]
    if b"\n" in manifest_body or b"\r" in manifest_body:
        fail("capture manifest must contain exactly one JSON object")
    manifest = parse_json(manifest_body, label=f"{slot} capture manifest")
    if canonical_json_bytes(manifest) != manifest_body:
        fail("capture manifest is not canonical JSON")
    validate_instance(capture_validator, manifest, label=f"{slot} capture manifest")

    lines = _read_event_lines(event_file.raw)
    previous_hash: str | None = None
    run_id: str | None = None
    session_id: str | None = None
    source_commit: str | None = None
    start: dict[str, Any] | None = None
    end: dict[str, Any] | None = None
    child_spawned: dict[str, Any] | None = None
    child_exit: dict[str, Any] | None = None
    requests: list[dict[str, Any]] = []
    responses: list[dict[str, Any]] = []
    notifications: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    anomalies: list[dict[str, Any]] = []
    streams: list[dict[str, Any]] = []
    lifecycle_counts: Counter[str] = Counter()
    prior_bytes = 0
    prior_digest = hashlib.sha256()

    for index, encoded_line in enumerate(lines):
        body = encoded_line[:-1]
        event = parse_json(body, label=f"{slot} event {index}")
        if canonical_json_bytes(event) != body:
            fail(f"{slot} event {index} is not canonical JSON")
        validate_instance(event_validator, event, label=f"{slot} event {index}")
        _require_exact_event_fields(event)
        if event["sequence"] != index:
            fail("event log does not have a consecutive sequence")
        if event["previous_event_sha256"] != previous_hash:
            fail("event log does not bind the preceding event")
        if event["slot"] != slot:
            fail("event slot does not match its private session directory")
        if run_id is None:
            run_id = event["run_id"]
            session_id = event["session_id"]
        elif event["run_id"] != run_id or event["session_id"] != session_id:
            fail("event log mixes run or session identities")
        core = dict(event)
        supplied_hash = core.pop("event_sha256")
        expected_hash = domain_separated_sha256(core)
        if not hmac.compare_digest(supplied_hash, expected_hash):
            fail("event log contains an invalid event identity")

        kind = event["event"]
        if kind == "lifecycle":
            phase = event["phase"]
            lifecycle_counts[phase] += 1
            if phase == "session-start":
                start = event
                source_commit = event["source_commit"]
            elif phase == "child-spawned":
                child_spawned = event
            elif phase == "child-exit":
                child_exit = event
            elif phase == "session-end":
                end = event
                if event["prior_event_count"] != index:
                    fail("session-end has an invalid prior event count")
                if event["prior_event_log_bytes"] != prior_bytes:
                    fail("session-end has an invalid prior log byte count")
                if not hmac.compare_digest(
                    event["prior_event_log_sha256"], prior_digest.hexdigest()
                ):
                    fail("session-end has an invalid prior log digest")
        elif kind == "request":
            requests.append(event)
        elif kind == "response":
            responses.append(event)
        elif kind == "notification":
            notifications.append(event)
        elif kind == "audit":
            audits.append(event)
        elif kind == "anomaly":
            anomalies.append(event)
        elif kind == "stream":
            streams.append(event)
        else:  # pragma: no cover - the closed schema rejects this first
            fail("event log contains an unknown event kind")
        if kind != "lifecycle" or event.get("phase") != "session-end":
            prior_digest.update(encoded_line)
            prior_bytes += len(encoded_line)
        previous_hash = supplied_hash

    if run_id is None or session_id is None or start is None or end is None:
        fail("event log is missing a complete session boundary")
    if lines[0][:-1] != canonical_json_bytes(start) or start["phase"] != "session-start":
        fail("event log must start with session-start")
    if lines[-1][:-1] != canonical_json_bytes(end) or end["phase"] != "session-end":
        fail("event log must end with session-end")
    if lifecycle_counts != Counter(
        {"session-start": 1, "child-spawned": 1, "child-exit": 1, "session-end": 1}
    ):
        fail("event log must contain exactly one complete child lifecycle")
    lifecycle_sequences = {
        event["phase"]: event["sequence"]
        for event in (start, child_spawned, child_exit, end)
        if event is not None
    }
    if not (
        lifecycle_sequences["session-start"]
        < lifecycle_sequences["child-spawned"]
        < lifecycle_sequences["child-exit"]
        < lifecycle_sequences["session-end"]
    ):
        fail("child lifecycle events are not in order")
    if lifecycle_sequences["child-spawned"] != 1:
        fail("passed session must spawn its only fixture before captured traffic")
    if any(
        event["sequence"] <= lifecycle_sequences["child-spawned"]
        for event in requests + responses + notifications + audits + streams
    ):
        fail("captured traffic precedes the only fixture child")
    if any(
        event["sequence"] >= lifecycle_sequences["child-exit"]
        for event in requests + notifications
    ):
        fail("host traffic is recorded after the fixture child exited")
    if child_exit is None or (
        child_exit["exit_code"] != end["exit_code"]
        or child_exit["signal"] != end["signal"]
    ):
        fail("session-end does not agree with the child exit")
    if child_spawned is None or (
        child_spawned["fixture_arguments_match_observer_contract"] is not True
        or child_spawned["spawned_process_identity_verified"] is not False
    ):
        fail("child-spawned does not preserve the observer attribution boundary")

    if run_id != expected_run_id or manifest["run_id"] != expected_run_id:
        fail("capture does not bind the expected run ID")
    if source_commit != expected_source_commit or manifest["source_commit"] != source_commit:
        fail("capture does not bind the expected source commit")
    if start["protocol_target"] != "2026-07-28":
        fail("session does not bind the final MCP protocol target")
    source_checkout = start["source_checkout"]
    if not all(
        source_checkout[name] is True
        for name in (
            "detached_head",
            "head_matches_source_commit",
            "local_origin_main_matches_source_commit",
            "working_tree_clean",
        )
    ):
        fail("session does not bind one clean detached protected-main checkout")
    parent = start["immediate_parent"]
    if (
        parent["pid"] <= 0
        or parent["sha256"] != expected_parent_sha256
        or parent["bytes"] != expected_parent_bytes
    ):
        fail("session does not bind the expected immediate parent executable")
    capability_sandbox = start["host_attribution"] == "outer-harness-spawn-executable"
    if (
        start["credential_environment_forwarded"] is not False
        or start["credential_environment_observed"] is not False
        or start["child_environment_mode"] != "closed-credential-free"
        or start["host_attribution"]
        not in {
            "immediate-parent-executable-only-unscored",
            "outer-harness-spawn-executable",
        }
    ):
        fail("session-start does not preserve its credential-free attribution boundary")
    if capability_sandbox:
        if (
            start.get("mcp_subtree_network_access_allowed") is not False
            or start.get("mcp_subtree_network_sandbox") != "macos-seatbelt-deny-network"
            or child_spawned.get("mcp_subtree_network_access_allowed") is not False
            or child_spawned.get("mcp_subtree_network_sandbox")
            != "macos-seatbelt-deny-network"
        ):
            fail("capability session does not preserve its MCP subtree network sandbox")

    if end["request_count"] != len(requests):
        fail("session-end request count does not match the event log")
    if end["response_count"] != len(responses):
        fail("session-end response count does not match the event log")
    if end["notification_count"] != len(notifications):
        fail("session-end notification count does not match the event log")
    if end["anomaly_count"] != len(anomalies):
        fail("session-end anomaly count does not match the event log")
    _require_clean_session_end(end)
    if anomalies:
        fail("successful composite observation must not contain anomalies")
    _verify_request_response_contract(requests, responses)
    _verify_notifications(notifications, requests, responses)
    _verify_profile(end["session_profile"], requests, responses, notifications)
    _verify_audits(
        audits,
        capability_sandbox=capability_sandbox,
        requests=requests,
        responses=responses,
    )
    _verify_streams(
        streams,
        requests=requests,
        responses=responses,
        notifications=notifications,
        audits=audits,
        session_end=end,
    )

    completed_log_sha256 = hashlib.sha256(event_file.raw).hexdigest()
    manifest_log = manifest["event_log"]
    manifest_bindings = {
        "client": start["client"],
        "session_id": session_id,
        "slot": slot,
        "session_profile": end["session_profile"],
        "protocol_session_status": end["protocol_session_status"],
        "capability_scored": False,
        "host_capability": False,
        "source_binding_ready": False,
    }
    for name, expected in manifest_bindings.items():
        if manifest[name] != expected:
            fail(f"capture manifest does not bind {name}")
    if manifest["status"] != "complete":
        fail("capture manifest is not complete")
    if manifest_log["bytes"] != len(event_file.raw):
        fail("capture manifest has an invalid event-log byte count")
    if manifest_log["event_count"] != len(lines):
        fail("capture manifest has an invalid event count")
    if not hmac.compare_digest(manifest_log["last_event_sha256"], previous_hash):
        fail("capture manifest does not bind the final event")
    if not hmac.compare_digest(manifest_log["sha256"], completed_log_sha256):
        fail("capture manifest has an invalid whole-log digest")

    return SessionResult(
        run_id=run_id,
        session_id=session_id,
        slot=slot,
        profile=end["session_profile"],
        source_commit=source_commit,
        immediate_parent=parent,
        observer_runtime=start["observer_runtime"],
        client=start["client"],
        request_count=len(requests),
    )


def verify_capture_root(
    capture_root: Path,
    *,
    expected_run_id: str,
    expected_source_commit: str,
    expected_parent_sha256: str,
    expected_parent_bytes: int,
) -> CompositeResult:
    """Verify exactly two stable, private session captures without writing output."""
    _validate_uuid_v4(expected_run_id, label="run ID")
    if len(expected_source_commit) != 40 or any(
        character not in SHA256_PATTERN for character in expected_source_commit
    ):
        fail("source commit must be one lowercase 40-character Git object ID")
    _validate_sha256(expected_parent_sha256, label="expected parent identity")
    if expected_parent_bytes <= 0:
        fail("expected parent byte length must be positive")

    _require_canonical_absolute_path(capture_root, label="capture root")
    root_before = _require_private_directory(capture_root, label="capture root")
    if _directory_names(capture_root, label="capture root") != set(EXPECTED_SLOTS):
        fail("capture root must contain exactly session-1 and session-2")

    event_schema = load_schema(EVENT_SCHEMA_PATH, label="composite event schema")
    capture_schema = load_schema(CAPTURE_SCHEMA_PATH, label="composite capture schema")
    event_validator = Draft202012Validator(
        event_schema,
        format_checker=FormatChecker(),
    )
    capture_validator = Draft202012Validator(
        capture_schema,
        format_checker=FormatChecker(),
    )

    results: list[SessionResult] = []
    for slot in EXPECTED_SLOTS:
        session_root = capture_root / slot
        session_before = _require_private_directory(
            session_root,
            label=f"{slot} directory",
        )
        if _directory_names(session_root, label=f"{slot} directory") != EXPECTED_CAPTURE_FILES:
            fail(f"{slot} directory must contain only events.jsonl and manifest.json")
        event_file = read_private_file(
            session_root / "events.jsonl",
            maximum_bytes=MAX_EVENT_LOG_BYTES,
            label=f"{slot} event log",
        )
        manifest_file = read_private_file(
            session_root / "manifest.json",
            maximum_bytes=MAX_MANIFEST_BYTES,
            label=f"{slot} manifest",
        )
        session_after = _require_private_directory(
            session_root,
            label=f"{slot} directory",
        )
        if _directory_state(session_after) != _directory_state(session_before):
            fail(f"{slot} directory changed during verification")
        if _directory_names(session_root, label=f"{slot} directory") != EXPECTED_CAPTURE_FILES:
            fail(f"{slot} directory changed during verification")
        results.append(
            verify_session(
                slot=slot,
                event_file=event_file,
                manifest_file=manifest_file,
                event_validator=event_validator,
                capture_validator=capture_validator,
                expected_run_id=expected_run_id,
                expected_source_commit=expected_source_commit,
                expected_parent_sha256=expected_parent_sha256,
                expected_parent_bytes=expected_parent_bytes,
            )
        )

    root_after = _require_private_directory(capture_root, label="capture root")
    if _directory_state(root_after) != _directory_state(root_before):
        fail("capture root changed during verification")
    if _directory_names(capture_root, label="capture root") != set(EXPECTED_SLOTS):
        fail("capture root changed during verification")

    first, second = results
    if first.session_id == second.session_id:
        fail("the two observations must use distinct session identities")
    if (
        first.profile != "negotiation-probe"
        or second.profile != "modern-session"
    ):
        fail("session-1 must be the negotiation probe and session-2 the modern session")
    shared = (
        first.run_id == second.run_id == expected_run_id
        and first.source_commit == second.source_commit == expected_source_commit
        and first.immediate_parent == second.immediate_parent
        and first.observer_runtime == second.observer_runtime
        and first.client == second.client
    )
    if not shared:
        fail("the two sessions do not share one source, parent and observer identity")
    if first.immediate_parent["pid"] <= 0:
        fail("the composite observation does not bind one immediate parent PID")

    by_profile = {result.profile: result for result in results}
    return CompositeResult(
        negotiation_request_count=by_profile["negotiation-probe"].request_count,
        modern_request_count=by_profile["modern-session"].request_count,
    )


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Verify one owner-only two-session QUAL-206 Claude Code observation "
            "without creating evidence."
        )
    )
    parser.add_argument("--capture-root", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--expected-parent-sha256", required=True)
    parser.add_argument("--expected-parent-bytes", required=True, type=int)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    try:
        result = verify_capture_root(
            arguments.capture_root,
            expected_run_id=arguments.run_id,
            expected_source_commit=arguments.source_commit,
            expected_parent_sha256=arguments.expected_parent_sha256,
            expected_parent_bytes=arguments.expected_parent_bytes,
        )
    except (OSError, VerificationError) as error:
        print(f"QUAL-206 Claude composite verification failed: {error}", file=sys.stderr)
        return 1
    print(
        "QUAL-206 Claude composite observation verified "
        f"(2 sessions; negotiation-probe requests: {result.negotiation_request_count}; "
        f"modern-session requests: {result.modern_request_count})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
