#!/usr/bin/env python3
"""Verify one private QUAL-206 strict-modern event capture without rewriting it."""

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
    ROOT / "schemas" / "qual-206-strict-modern-host-event-v1.schema.json"
)
CAPTURE_SCHEMA_PATH = (
    ROOT / "schemas" / "qual-206-strict-modern-host-event-capture-v1.schema.json"
)
EVENT_SCHEMA_ID = "gis-ai-go.qual-206-strict-modern-host-event.v1"
EVENT_DOMAIN = "gis-ai-go.qual-206-strict-modern-host-event.v1"
DOMAIN_SEPARATION_PREFIX = b"GIS-AI-GO\0canonical-json\0sha256\0v1\0"
MAX_EVENT_LOG_BYTES = 8 * 1024 * 1024
MAX_MANIFEST_BYTES = 64 * 1024
MAX_EVENT_COUNT = 512
EXPECTED_STREAMS = {
    "host-stdin",
    "server-stdout",
    "server-stderr",
    "server-audit",
}
EXPECTED_AUDIT_ORDER = (
    "provider-egress-guard-ready",
    "provider-transport-started:1",
    "provider-transport-started:2",
    "provider-transport-aborted:2",
    "provider-egress-guard-summary",
    "session-summary",
)
EXPECTED_AUDIT_INDEX = {
    identity: index for index, identity in enumerate(EXPECTED_AUDIT_ORDER)
}
EXPECTED_REQUESTS = (
    ("server/discover", "not-applicable", "not-applicable"),
    ("tools/list", "not-applicable", "not-applicable"),
    ("resources/list", "not-applicable", "not-applicable"),
    ("resources/templates/list", "not-applicable", "not-applicable"),
    ("resources/read", "not-applicable", "catalogue.public"),
    ("resources/read", "not-applicable", "catalogue.record"),
    ("tools/call", "catalogue.search", "not-applicable"),
    ("tools/call", "catalogue.describe", "not-applicable"),
    ("tools/call", "selection.resolve", "not-applicable"),
    ("tools/call", "data.query", "not-applicable"),
    ("tools/call", "evidence.inspect", "not-applicable"),
    ("resources/read", "not-applicable", "evidence.receipt"),
    ("tools/call", "data.query", "not-applicable"),
    ("prompts/list", "not-applicable", "not-applicable"),
)
EXPECTED_RESPONSE_ORDINALS = tuple(range(12)) + (13,)
AUDIT_FIELD_NAMES = (
    "audit_kind",
    "contract_valid",
    "scenario",
    "ordinal",
    "guarded_apis_exact",
    "guarded_api_invocation_count",
    "source_commit_match",
    "state",
    "production_registration",
    "operations_exact",
    "resources_exact",
    "suspensions_empty",
    "provider_transport_calls",
    "aborted_provider_calls",
    "ledger_event_count",
    "reported_error_count",
)


class VerificationError(ValueError):
    """The private capture does not satisfy the closed verification contract."""


@dataclass(frozen=True)
class VerificationResult:
    """A process-local result, not a new evidence artefact."""

    session_id: str
    event_count: int
    protocol_session_status: str


@dataclass(frozen=True)
class PrivateFile:
    raw: bytes
    identity: tuple[int, int]


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
    )


def _require_canonical_absolute_path(path: Path, *, label: str) -> None:
    if not path.is_absolute() or Path(os.path.abspath(path)) != path:
        fail(f"{label} path must be canonical and absolute")
    if "\0" in os.fspath(path):
        fail(f"{label} path is invalid")
    try:
        parent_real = Path(os.path.realpath(path.parent))
    except OSError as error:
        raise VerificationError(f"{label} parent is unavailable") from error
    if parent_real != path.parent:
        fail(f"{label} parent must not traverse an alias")


def read_private_file(path: Path, *, maximum_bytes: int, label: str) -> PrivateFile:
    """Read one stable owner-only file under one stable owner-only directory."""
    if not hasattr(os, "getuid"):
        fail("owner-only event verification requires a POSIX user identity")
    _require_canonical_absolute_path(path, label=label)
    uid = os.getuid()
    try:
        parent_before = path.parent.lstat()
        before = path.lstat()
    except OSError as error:
        raise VerificationError(f"{label} is unavailable") from error
    if (
        not stat.S_ISDIR(parent_before.st_mode)
        or parent_before.st_uid != uid
        or stat.S_IMODE(parent_before.st_mode) != 0o700
    ):
        fail(f"{label} parent must be one current-user directory with mode 0700")
    if (
        stat.S_ISLNK(before.st_mode)
        or not stat.S_ISREG(before.st_mode)
        or before.st_uid != uid
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
    try:
        parent_after = path.parent.lstat()
    except OSError as error:
        raise VerificationError(f"{label} parent changed while being read") from error
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


def _audit_identity(event: dict[str, Any]) -> str:
    kind = event["audit_kind"]
    if kind in {"provider-transport-started", "provider-transport-aborted"}:
        return f"{kind}:{event['ordinal']}"
    return kind


def _empty_response_facts() -> dict[str, Any]:
    return {
        "advertised_operations_exact": None,
        "advertised_resources_exact": None,
        "advertised_templates_exact": None,
        "advertised_tool_schemas_valid": None,
        "deterministic_result_valid": None,
        "expected_method_not_found": None,
        "receipt_reference_match": None,
        "receipt_present": None,
        "reported_operation": "not-applicable",
        "resource_content_valid": None,
        "returned_resource": "not-applicable",
        "structured_plain_text_parity": None,
        "supported_versions_exact": None,
        "tool_result": "not-applicable",
    }


def _expected_response_projection(
    ordinal: int,
) -> tuple[str, str, int | None, dict[str, Any]]:
    facts = _empty_response_facts()
    if ordinal == 0:
        facts["supported_versions_exact"] = True
        facts["deterministic_result_valid"] = True
        return "discover-pass", "success", None, facts
    if ordinal == 1:
        facts["advertised_operations_exact"] = True
        facts["advertised_tool_schemas_valid"] = True
        return "tools-list-pass", "success", None, facts
    if ordinal == 2:
        facts["advertised_resources_exact"] = True
        return "resources-list-pass", "success", None, facts
    if ordinal == 3:
        facts["advertised_templates_exact"] = True
        return "resource-templates-pass", "success", None, facts
    if ordinal in {4, 5, 11}:
        facts["deterministic_result_valid"] = True
        facts["resource_content_valid"] = True
        facts["returned_resource"] = EXPECTED_REQUESTS[ordinal][2]
        if ordinal == 11:
            facts["receipt_reference_match"] = True
        return "resource-read-pass", "success", None, facts
    if 6 <= ordinal <= 10:
        operation = EXPECTED_REQUESTS[ordinal][1]
        facts.update(
            {
                "deterministic_result_valid": True,
                "receipt_present": True,
                "reported_operation": operation,
                "structured_plain_text_parity": True,
                "tool_result": "success",
            }
        )
        if ordinal == 10:
            facts["receipt_reference_match"] = True
        return "tool-success-pass", "success", None, facts
    if ordinal == 13:
        facts["expected_method_not_found"] = True
        return "expected-method-not-found", "error", -32601, facts
    fail("response projection refers to the cancelled request")


def _expected_audit_projection(identity: str) -> dict[str, Any]:
    projection: dict[str, Any] = {
        "audit_kind": identity.split(":", 1)[0],
        "contract_valid": True,
        "scenario": "not-applicable",
        "ordinal": None,
        "guarded_apis_exact": None,
        "guarded_api_invocation_count": None,
        "source_commit_match": None,
        "state": "not-applicable",
        "production_registration": None,
        "operations_exact": None,
        "resources_exact": None,
        "suspensions_empty": None,
        "provider_transport_calls": None,
        "aborted_provider_calls": None,
        "ledger_event_count": None,
        "reported_error_count": None,
    }
    if identity == "provider-egress-guard-ready":
        projection["guarded_apis_exact"] = True
    elif identity in {
        "provider-transport-started:1",
        "provider-transport-started:2",
        "provider-transport-aborted:2",
    }:
        projection["scenario"] = "independent-host"
        projection["ordinal"] = int(identity.rsplit(":", 1)[1])
    elif identity == "provider-egress-guard-summary":
        projection["guarded_apis_exact"] = True
        projection["guarded_api_invocation_count"] = 0
    elif identity == "session-summary":
        projection.update(
            {
                "scenario": "independent-host",
                "source_commit_match": True,
                "state": "candidate-unregistered",
                "production_registration": False,
                "operations_exact": True,
                "resources_exact": True,
                "suspensions_empty": True,
                "provider_transport_calls": 2,
                "aborted_provider_calls": 1,
                "ledger_event_count": 4,
                "reported_error_count": 0,
            }
        )
    else:
        fail("passed session contains an unexpected server-audit identity")
    return projection


def _verify_passed_journey(
    *,
    session_start: dict[str, Any],
    child_spawned: dict[str, Any],
    requests: list[dict[str, Any]],
    notifications: list[dict[str, Any]],
    responses: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    stderr_events: list[dict[str, Any]],
    streams: dict[str, dict[str, Any]],
    session_end: dict[str, Any],
) -> None:
    if (
        session_start["scenario"] != "independent-host"
        or session_start["protocol_target"] != "2026-07-28"
        or session_start["transport"] != "operating-system-stdio-pipes"
        or session_start["credential_environment_forwarded"] is not False
        or session_start["host_attribution"]
        != "immediate-parent-executable-only-unscored"
    ):
        fail("passed session has an invalid session-start projection")
    if (
        child_spawned["spawn_arguments_match_collector_contract"] is not True
        or child_spawned["spawned_process_identity_verified"] is not False
    ):
        fail("passed session has an invalid child-spawn projection")

    if len(requests) != len(EXPECTED_REQUESTS):
        fail("passed session does not contain the exact client-request journey")
    request_by_digest: dict[str, tuple[int, dict[str, Any]]] = {}
    for ordinal, (request, expected) in enumerate(zip(requests, EXPECTED_REQUESTS)):
        method, operation, resource = expected
        if (
            request["journey_ordinal"] != ordinal
            or request["method"] != method
            or request["operation"] != operation
            or request["resource"] != resource
            or request["protocol_claim"] != "2026-07-28"
            or request["journey_semantic_valid"] is not True
            or request["request_id_unique"] is not True
            or request["request_id_kind"] not in {"string", "integer"}
            or request["request_id_sha256"] is None
        ):
            fail(f"passed session has an invalid client-request projection at {ordinal}")
        digest = request["request_id_sha256"]
        if digest in request_by_digest:
            fail("passed session reuses a projected request identity")
        request_by_digest[digest] = (ordinal, request)

    if len(notifications) != 1:
        fail("passed session does not contain one cancellation notification")
    notification = notifications[0]
    cancelled_request = requests[12]
    if (
        notification["method"] != "notifications/cancelled"
        or notification["protocol_claim"] != "2026-07-28"
        or notification["target_matched_pending_data_query"] is not True
        or notification["target_request_id_sha256"]
        != cancelled_request["request_id_sha256"]
        or notification["target_request_id_kind"]
        != cancelled_request["request_id_kind"]
        or not (
            cancelled_request["sequence"]
            < notification["sequence"]
            < requests[13]["sequence"]
        )
    ):
        fail("passed session has an invalid cancellation projection")

    if len(responses) != len(EXPECTED_RESPONSE_ORDINALS):
        fail("passed session does not contain the exact response journey")
    observed_response_ordinals: list[int] = []
    seen_response_digests: set[str] = set()
    for response in responses:
        digest = response["request_id_sha256"]
        request_context = request_by_digest.get(digest)
        if request_context is None or digest in seen_response_digests:
            fail("passed session has an orphaned or duplicate response projection")
        seen_response_digests.add(digest)
        ordinal, request = request_context
        observed_response_ordinals.append(ordinal)
        semantic, outcome, error_code, facts = _expected_response_projection(ordinal)
        if (
            response["correlation"] != "matched"
            or response["request_id_kind"] != request["request_id_kind"]
            or response["request_method"] != request["method"]
            or response["operation"] != request["operation"]
            or response["resource"] != request["resource"]
            or response["outcome"] != outcome
            or response["error_code"] != error_code
            or response["semantic"] != semantic
            or response["facts"] != facts
            or response["duration_ms"] is None
            or response["sequence"] <= request["sequence"]
        ):
            fail(f"passed session has an invalid response projection at {ordinal}")
    if tuple(observed_response_ordinals) != EXPECTED_RESPONSE_ORDINALS:
        fail("passed session has reordered response projections")
    if cancelled_request["request_id_sha256"] in seen_response_digests:
        fail("passed session includes a response after cancellation")

    if len(audits) != len(EXPECTED_AUDIT_ORDER):
        fail("passed session does not contain the exact server-audit journey")
    audit_by_identity = {_audit_identity(audit): audit for audit in audits}
    for identity in EXPECTED_AUDIT_ORDER:
        audit = audit_by_identity.get(identity)
        if audit is None:
            fail("passed session is missing an expected server-audit projection")
        projected = {name: audit[name] for name in AUDIT_FIELD_NAMES}
        if projected != _expected_audit_projection(identity):
            fail(f"passed session has an invalid server-audit projection: {identity}")
    expected_frame_counts = {
        "host-stdin": len(requests) + len(notifications),
        "server-stdout": len(responses),
        "server-audit": len(audits),
        "server-stderr": len(stderr_events),
    }
    expected_stream_bytes = {
        "host-stdin": sum(event["frame_bytes"] for event in requests + notifications),
        "server-stdout": sum(event["frame_bytes"] for event in responses),
        "server-stderr": sum(event["bytes"] for event in stderr_events),
    }
    for name, expected_frames in expected_frame_counts.items():
        stream = streams[name]
        if stream["graceful"] is not True or stream["frame_count"] != expected_frames:
            fail(f"passed session has an invalid {name} stream-end projection")
        if name in expected_stream_bytes and stream["bytes"] != expected_stream_bytes[name]:
            fail(f"passed session has an invalid {name} byte total")
        if name != "server-stderr" and stream["bytes"] <= 0:
            fail(f"passed session reports no captured bytes for {name}")
    if session_end["stderr_bytes"] != expected_stream_bytes["server-stderr"]:
        fail("passed session has an invalid stderr byte total")


def verify_capture(event_log_path: Path, manifest_path: Path) -> VerificationResult:
    """Verify an immutable snapshot of one log and its closed sibling manifest."""
    if event_log_path.parent != manifest_path.parent or event_log_path == manifest_path:
        fail("event log and manifest must be distinct siblings")
    event_file = read_private_file(
        event_log_path,
        maximum_bytes=MAX_EVENT_LOG_BYTES,
        label="event log",
    )
    manifest_file = read_private_file(
        manifest_path,
        maximum_bytes=MAX_MANIFEST_BYTES,
        label="capture manifest",
    )
    if event_file.identity == manifest_file.identity:
        fail("event log and manifest must not be the same file")

    event_schema = load_schema(EVENT_SCHEMA_PATH, label="event schema")
    capture_schema = load_schema(CAPTURE_SCHEMA_PATH, label="capture schema")
    event_validator = Draft202012Validator(
        event_schema,
        format_checker=FormatChecker(),
    )
    capture_validator = Draft202012Validator(
        capture_schema,
        format_checker=FormatChecker(),
    )

    if not manifest_file.raw.endswith(b"\n") or manifest_file.raw.endswith(b"\r\n"):
        fail("capture manifest must be one canonical LF-terminated JSON object")
    manifest_body = manifest_file.raw[:-1]
    if b"\n" in manifest_body or b"\r" in manifest_body:
        fail("capture manifest must contain exactly one JSON object")
    manifest = parse_json(manifest_body, label="capture manifest")
    if canonical_json_bytes(manifest) != manifest_body:
        fail("capture manifest is not canonical JSON")
    validate_instance(capture_validator, manifest, label="capture manifest")

    lines = _read_event_lines(event_file.raw)
    previous_hash: str | None = None
    session_id: str | None = None
    source_commit: str | None = None
    event_counts: Counter[str] = Counter()
    stream_names: set[str] = set()
    stream_events: dict[str, dict[str, Any]] = {}
    child_exit: dict[str, Any] | None = None
    child_spawned: dict[str, Any] | None = None
    session_start: dict[str, Any] | None = None
    session_end: dict[str, Any] | None = None
    request_events: list[dict[str, Any]] = []
    notification_events: list[dict[str, Any]] = []
    response_events: list[dict[str, Any]] = []
    audit_events: list[dict[str, Any]] = []
    stderr_events: list[dict[str, Any]] = []
    audit_identities: list[str] = []
    audit_contract_validity: list[bool] = []
    seen_audit_identities: set[str] = set()
    previous_expected_audit_index = -1
    ended = False
    prior_bytes = 0
    prior_digest = hashlib.sha256()

    for index, encoded_line in enumerate(lines):
        if ended:
            fail("event log contains an event after session_end")
        body = encoded_line[:-1]
        event = parse_json(body, label=f"event {index}")
        if canonical_json_bytes(event) != body:
            fail(f"event {index} is not canonical JSON")
        validate_instance(event_validator, event, label=f"event {index}")
        if event["sequence"] != index:
            fail(f"event {index} does not have the consecutive sequence")
        if event["previous_event_sha256"] != previous_hash:
            fail(f"event {index} does not bind the preceding event")
        current_session = event["session_id"]
        if session_id is None:
            session_id = current_session
        elif current_session != session_id:
            fail("event log mixes more than one session")
        core = dict(event)
        supplied_hash = core.pop("event_sha256")
        expected_hash = domain_separated_sha256(core)
        if not hmac.compare_digest(supplied_hash, expected_hash):
            fail(f"event {index} has an invalid event identity")

        event_name = event["event"]
        event_counts[event_name] += 1
        if index == 0 and event_name != "session_start":
            fail("event log does not start with session_start")
        if index > 0 and event_name == "session_start":
            fail("event log contains more than one session_start")
        if event_name == "session_start":
            session_start = event
            source_commit = event["source_commit"]
        elif event_name == "child_spawned":
            child_spawned = event
        elif event_name == "client_request":
            request_events.append(event)
        elif event_name == "client_notification":
            notification_events.append(event)
        elif event_name == "server_response":
            response_events.append(event)
        elif event_name == "stream_end":
            stream = event["stream"]
            if stream in stream_names:
                fail("event log contains a duplicate stream_end")
            stream_names.add(stream)
            stream_events[stream] = event
        elif event_name == "server_audit":
            audit_events.append(event)
            audit_identity = _audit_identity(event)
            audit_contract_validity.append(event["contract_valid"])
            if audit_identity in seen_audit_identities:
                fail("event log contains a duplicate server-audit identity")
            seen_audit_identities.add(audit_identity)
            if event["audit_kind"] == "provider-egress-guard-blocked":
                if event["contract_valid"] is not False:
                    fail("blocked provider egress cannot be a valid audit contract")
            else:
                expected_index = EXPECTED_AUDIT_INDEX.get(audit_identity)
                if expected_index is None:
                    fail("event log contains an unexpected server-audit identity")
                if expected_index <= previous_expected_audit_index:
                    fail("event log contains reordered server-audit identities")
                previous_expected_audit_index = expected_index
                audit_identities.append(audit_identity)
        elif event_name == "server_stderr":
            stderr_events.append(event)
        elif event_name == "child_exit":
            if child_exit is not None:
                fail("event log contains more than one child_exit")
            child_exit = event
        elif event_name == "session_end":
            session_end = event
            ended = True
            if event["prior_event_count"] != index:
                fail("session_end has an invalid prior event count")
            if event["prior_event_log_bytes"] != prior_bytes:
                fail("session_end has an invalid prior log byte count")
            if not hmac.compare_digest(
                event["prior_event_log_sha256"], prior_digest.hexdigest()
            ):
                fail("session_end has an invalid prior log digest")
        if event_name != "session_end":
            prior_digest.update(encoded_line)
            prior_bytes += len(encoded_line)
        previous_hash = supplied_hash

    if (
        not ended
        or session_start is None
        or session_end is None
        or child_spawned is None
    ):
        fail("event log is incomplete")
    if lines[-1][:-1] != canonical_json_bytes(session_end):
        fail("session_end is not the final event")
    if event_counts["session_start"] != 1 or event_counts["session_end"] != 1:
        fail("event log does not contain exactly one session boundary")
    if event_counts["child_spawned"] != 1 or event_counts["child_exit"] != 1:
        fail("event log does not contain one complete child process lifecycle")
    if stream_names != EXPECTED_STREAMS or event_counts["stream_end"] != 4:
        fail("event log does not contain one end event for every captured stream")
    if child_exit is None:
        fail("event log does not contain a child exit")
    if (
        child_exit["exit_code"] != session_end["exit_code"]
        or child_exit["signal"] != session_end["signal"]
    ):
        fail("session_end does not agree with the child exit")
    if session_end["request_count"] != event_counts["client_request"]:
        fail("session_end request count does not agree with the event log")
    if session_end["response_count"] != event_counts["server_response"]:
        fail("session_end response count does not agree with the event log")
    if session_end["notification_count"] != event_counts["client_notification"]:
        fail("session_end notification count does not agree with the event log")
    if session_end["stderr_event_count"] != event_counts["server_stderr"]:
        fail("session_end stderr count does not agree with the event log")
    if session_end["anomaly_count"] != event_counts["capture_anomaly"]:
        fail("session_end anomaly count does not agree with the event log")
    expected_local_checkout_candidate = (
        session_start["source_checkout"]["detached_head"]
        and session_start["source_checkout"]["head_matches_source_commit"]
        and session_start["source_checkout"][
            "local_origin_main_matches_source_commit"
        ]
        and session_start["source_checkout"]["working_tree_clean"]
        and session_end["runtime_materials_stable"]
    )
    if session_end["source_binding_ready"] is not False:
        fail("session_end must keep host source binding unready")
    if (
        session_end["local_checkout_candidate_ready"]
        is not expected_local_checkout_candidate
    ):
        fail("session_end local-checkout candidate state is inconsistent")

    if session_end["protocol_session_status"] == "passed":
        passed_contract = (
            not session_end["source_binding_ready"]
            and session_end["runtime_materials_stable"]
            and session_end["exit_code"] == 0
            and session_end["signal"] is None
            and session_end["request_count"] == 14
            and session_end["response_count"] == 13
            and session_end["notification_count"] == 1
            and session_end["pending_request_count"] == 0
            and session_end["cancelled_request_count"] == 1
            and session_end["stderr_event_count"] == 0
            and session_end["stderr_bytes"] == 0
            and session_end["stderr_sha256"] is None
            and session_end["anomaly_count"] == 0
            and session_end["temporary_state_removed"]
            and tuple(audit_identities) == EXPECTED_AUDIT_ORDER
            and event_counts["server_audit"] == len(EXPECTED_AUDIT_ORDER)
        )
        if not passed_contract:
            fail("passed session does not satisfy the closed collector outcome")
        if not all(audit_contract_validity):
            fail("passed session contains an invalid server-audit contract")
        _verify_passed_journey(
            session_start=session_start,
            child_spawned=child_spawned,
            requests=request_events,
            notifications=notification_events,
            responses=response_events,
            audits=audit_events,
            stderr_events=stderr_events,
            streams=stream_events,
            session_end=session_end,
        )

    completed_log_sha256 = hashlib.sha256(event_file.raw).hexdigest()
    manifest_log = manifest["event_log"]
    if manifest["event_schema"] != EVENT_SCHEMA_ID:
        fail("capture manifest names an unexpected event schema")
    if manifest["session_id"] != session_id:
        fail("capture manifest does not bind the event session")
    if manifest["source_commit"] != source_commit:
        fail("capture manifest does not bind the event source commit")
    if manifest["protocol_session_status"] != session_end["protocol_session_status"]:
        fail("capture manifest does not bind the session outcome")
    if manifest["source_binding_ready"] is not session_end["source_binding_ready"]:
        fail("capture manifest does not bind the source readiness state")
    if (
        manifest["local_checkout_candidate_ready"]
        is not session_end["local_checkout_candidate_ready"]
    ):
        fail("capture manifest does not bind the local-checkout candidate state")
    if manifest_log["bytes"] != len(event_file.raw):
        fail("capture manifest has an invalid event-log byte count")
    if manifest_log["event_count"] != len(lines):
        fail("capture manifest has an invalid event count")
    if not hmac.compare_digest(manifest_log["last_event_sha256"], previous_hash):
        fail("capture manifest does not bind the last event")
    if not hmac.compare_digest(manifest_log["sha256"], completed_log_sha256):
        fail("capture manifest has an invalid whole-log digest")

    return VerificationResult(
        session_id=session_id,
        event_count=len(lines),
        protocol_session_status=session_end["protocol_session_status"],
    )


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Verify one owner-only QUAL-206 strict-modern event log and its "
            "closed manifest without creating evidence."
        )
    )
    parser.add_argument("--event-log", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    try:
        result = verify_capture(arguments.event_log, arguments.manifest)
    except (OSError, VerificationError) as error:
        print(f"QUAL-206 event verification failed: {error}", file=sys.stderr)
        return 1
    print(
        "QUAL-206 private event capture verified "
        f"({result.event_count} events; {result.protocol_session_status})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
