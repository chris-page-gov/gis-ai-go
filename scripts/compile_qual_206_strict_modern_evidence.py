#!/usr/bin/env python3
"""Compile one private QUAL-206 host capture into bounded public evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
CAPTURE_SCHEMA_PATH = ROOT / "schemas" / "qual-206-strict-modern-host-capture.schema.json"
EVIDENCE_SCHEMA_PATH = ROOT / "schemas" / "qual-206-strict-modern-host-evidence.schema.json"
IDENTITY_HELPER_PATH = ROOT / "scripts" / "qual_206_strict_modern_identity.mjs"
MAX_CAPTURE_BYTES = 1_048_576
MAX_PRIVATE_TELEMETRY_BYTES = 8_388_608
EXACT_OPERATIONS = [
    "catalogue.search",
    "catalogue.describe",
    "selection.resolve",
    "data.query",
    "evidence.inspect",
]
EXACT_RESOURCES = [
    "catalogue.public",
    "catalogue.record",
    "evidence.receipt",
]
REQUIRED_CAPABILITY_CASES = {
    f"QUAL-206-HOST-{index:03d}" for index in range(1, 11)
}
BOUNDARY = (
    "Pre-activation, summary-level host capture only. It is not event-level "
    "capability evidence and does not authorise or prove registration, activation, "
    "deployment, release or completion of QUAL-206."
)
IDENTITY_PREFIX = "gis-ai-go:qual-206-strict-modern-host-evidence:sha256:"
IDENTITY_DOMAIN = "gis-ai-go.qual-206-strict-modern-host-evidence.v2"
GIT_BOUND_ROLES = {
    "source",
    "launcher",
    "telemetry-wrapper",
    "lockfile",
    "provider-egress-guard",
    "manifest",
    "compiler",
    "identity-helper",
    "capture-schema",
    "evidence-schema",
    "build-receipt",
}
REQUIRED_OBSERVED_MATERIALS = {
    ("compiler", "scripts/compile_qual_206_strict_modern_evidence.py"),
    ("identity-helper", "scripts/qual_206_strict_modern_identity.mjs"),
    ("capture-schema", "schemas/qual-206-strict-modern-host-capture.schema.json"),
    ("evidence-schema", "schemas/qual-206-strict-modern-host-evidence.schema.json"),
    ("launcher", "tests/interoperability/fixtures/qual_206_exact_five_stdio_server.mjs"),
    ("telemetry-wrapper", "scripts/qual_206_telemetry_proxy.mjs"),
    (
        "provider-egress-guard",
        "tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs",
    ),
    ("manifest", "package.json"),
    ("lockfile", "pnpm-lock.yaml"),
    ("source", "packages/evidence/src/canonical-json.ts"),
    ("source", "packages/evidence/src/digest.ts"),
    ("source", "packages/evidence/src/index.ts"),
    ("compiled", "packages/evidence/dist/src/canonical-json.js"),
    ("compiled", "packages/evidence/dist/src/digest.js"),
    ("compiled", "packages/evidence/dist/src/index.js"),
    ("build-receipt", "evaluation/qual-206-local-evaluation-receipts.v1.json"),
}
PINNED_IDENTITY_RUNTIME_SHA256 = {
    "packages/evidence/dist/src/canonical-json.js": (
        "0b898e4597f5f4f90d5feda5ef9d80c9ea14409f531c2378ff2c9e0a3529c624"
    ),
    "packages/evidence/dist/src/digest.js": (
        "295226181b1a5441b075b47efa9d00a36b664dd91b090daff9bfb046300fd81f"
    ),
    "packages/evidence/dist/src/index.js": (
        "51129a84578ed1cf46fa5bdf2f6afe32fa875874acd99c55e7416889c68070dd"
    ),
}
HISTORICAL_LINEAGE = [
    {
        "path": "schemas/qual-206-claude-code-stdio-observation.schema.json",
        "sha256": "78b9a8071a6954028576f397c98dd0fc4b87dddbaf72654f6459407b280e2a9b",
    },
    {
        "path": (
            "tests/interoperability/evidence/"
            "claude-code-2.1.241-stdio-observation-2026-08-24.json"
        ),
        "sha256": "d2cd72b7f16a0bafd8a7190b87b14f150b7fa975f6d70f5e779eb9ddf5f92478",
    },
    {
        "path": "schemas/qual-206-legacy-stdio-readiness.schema.json",
        "sha256": "5ce73d3d45c762112ac932407000b4379d07d92a9e54808227cd72e6050fd02a",
    },
    {
        "path": (
            "tests/interoperability/evidence/"
            "claude-code-legacy-stdio-readiness-2026-08-23.json"
        ),
        "sha256": "a3d40e2013095baf977bad336366c0fb429a05b6a5a267c3e069595e4cdb1a6b",
    },
    {
        "path": "tests/interoperability/qual_206_cases.json",
        "sha256": "23ac9bc1a76d524bd0e250b11b9ba321b09e66bd5921f1463f50c150001cd389",
    },
]
CAPTURE_FORBIDDEN_KEYS = {
    "arguments",
    "boundary",
    "capability",
    "claims",
    "command_sha256",
    "environment",
    "evidence_id",
    "headers",
    "prompt",
    "raw_command",
    "raw_payload",
    "raw_result",
    "readiness",
    "result_content",
    "session_id",
    "session_id_sha256",
    "status",
}
PUBLIC_FORBIDDEN_KEYS = {
    "arguments",
    "command_sha256",
    "device_id",
    "environment",
    "headers",
    "hostname",
    "prompt",
    "raw_command",
    "raw_payload",
    "raw_result",
    "result_content",
    "session_id",
    "session_id_sha256",
    "username",
}
PUBLIC_FORBIDDEN_PATTERN = re.compile(
    r"(?:"
    r"/Users/|/home/|/Volumes/|/private/tmp/|file://|"
    r"[A-Za-z]:\\\\Users\\\\|"
    r"\bsk-[A-Za-z0-9_-]{8,}|\bgh[opusr]_[A-Za-z0-9]{8,}|"
    r"\bxox[baprs]-[A-Za-z0-9-]{8,}|\bAKIA[0-9A-Z]{16}|"
    r"\bBearer\s+[A-Za-z0-9._~-]+|"
    r"OPENAI_API_KEY|CODEX_API_KEY|ANTHROPIC_API_KEY|"
    r"ANTHROPIC_AUTH_TOKEN|CLAUDE_CODE_OAUTH_TOKEN|"
    r"https?://(?:chatgpt\.com/c/|claude\.ai/chat/)|"
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|"
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-"
    r"[0-9a-f]{12}\b"
    r")",
    re.IGNORECASE,
)


class EvidenceError(ValueError):
    """A fail-closed evidence compilation error."""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def reject_non_standard_number(value: str) -> None:
    raise EvidenceError(f"non-standard JSON number: {value}")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise EvidenceError(f"duplicate JSON object key: {key}")
        value[key] = item
    return value


def assert_no_surrogate_code_points(value: object, path: str = "$") -> None:
    if isinstance(value, str):
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise EvidenceError(f"{path} contains a surrogate code point")
    elif isinstance(value, dict):
        for key, item in value.items():
            assert_no_surrogate_code_points(key, f"{path}.<key>")
            assert_no_surrogate_code_points(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            assert_no_surrogate_code_points(item, f"{path}[{index}]")


def parse_json_bytes(value: bytes, label: str) -> dict[str, Any]:
    try:
        parsed = json.loads(
            value.decode("utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_non_standard_number,
        )
    except UnicodeDecodeError as error:
        raise EvidenceError(f"{label} is not UTF-8") from error
    except json.JSONDecodeError as error:
        raise EvidenceError(f"{label} is not valid JSON: {error.msg}") from error
    if not isinstance(parsed, dict):
        raise EvidenceError(f"{label} must contain one JSON object")
    assert_no_surrogate_code_points(parsed)
    return parsed


def load_schema(path: Path) -> dict[str, Any]:
    schema = parse_json_bytes(path.read_bytes(), str(path.relative_to(ROOT)))
    Draft202012Validator.check_schema(schema)
    return schema


def format_errors(
    validator: Draft202012Validator,
    value: object,
) -> list[str]:
    errors = sorted(
        validator.iter_errors(value),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    return [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in errors
    ]


def validate(validator: Draft202012Validator, value: object, label: str) -> None:
    errors = format_errors(validator, value)
    if errors:
        raise EvidenceError(f"{label} failed schema validation: {'; '.join(errors)}")


def require_mode(path: Path, expected: int, label: str) -> os.stat_result:
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode):
        raise EvidenceError(f"{label} must not be a symbolic link")
    if not stat.S_ISREG(metadata.st_mode) and label != "capture root":
        raise EvidenceError(f"{label} must be a regular file")
    if label == "capture root" and not stat.S_ISDIR(metadata.st_mode):
        raise EvidenceError("capture root must be a directory")
    if metadata.st_uid != os.getuid():
        raise EvidenceError(f"{label} must be owned by the current user")
    if stat.S_ISREG(metadata.st_mode) and metadata.st_nlink != 1:
        raise EvidenceError(f"{label} must have exactly one hard link")
    mode = stat.S_IMODE(metadata.st_mode)
    if mode != expected:
        raise EvidenceError(f"{label} must have mode {expected:04o}, found {mode:04o}")
    return metadata


def normalise_capture_root(value: str) -> Path:
    supplied = Path(value)
    if not supplied.is_absolute():
        raise EvidenceError("capture root must be absolute")
    require_mode(supplied, 0o700, "capture root")
    resolved = supplied.resolve(strict=True)
    if resolved != supplied:
        raise EvidenceError("capture root must not resolve through an alias")
    return resolved


def ensure_no_symlink_components(root: Path, path: Path, label: str) -> None:
    try:
        relative = path.relative_to(root)
    except ValueError as error:
        raise EvidenceError(f"{label} must remain beneath the capture root") from error
    current = root
    for part in relative.parts:
        current = current / part
        if stat.S_ISLNK(current.lstat().st_mode):
            raise EvidenceError(f"{label} must not traverse a symbolic link")


def private_relative_path(root: Path, value: str | Path, label: str) -> PurePosixPath:
    supplied = Path(value)
    if supplied.is_absolute():
        try:
            supplied = supplied.relative_to(root)
        except ValueError as error:
            raise EvidenceError(f"{label} must remain beneath the capture root") from error
    logical = PurePosixPath(supplied.as_posix())
    if (
        not logical.parts
        or logical.is_absolute()
        or any(part in {"", ".", ".."} for part in logical.parts)
        or "\\" in logical.as_posix()
        or "\x00" in logical.as_posix()
    ):
        raise EvidenceError(f"{label} has an unsafe private path")
    return logical


def same_file_state(left: os.stat_result, right: os.stat_result) -> bool:
    return (
        left.st_dev,
        left.st_ino,
        left.st_mode,
        left.st_uid,
        left.st_nlink,
        left.st_size,
        left.st_mtime_ns,
    ) == (
        right.st_dev,
        right.st_ino,
        right.st_mode,
        right.st_uid,
        right.st_nlink,
        right.st_size,
        right.st_mtime_ns,
    )


def read_private_file(
    root: Path,
    value: str | Path,
    label: str,
    maximum: int,
) -> bytes:
    """Read a private file through directory descriptors without following links."""

    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise EvidenceError("secure private capture reads are unsupported on this platform")
    logical = private_relative_path(root, value, label)
    initial_root = require_mode(root, 0o700, "capture root")
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    file_flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    root_descriptor = os.open(root, directory_flags)
    descriptors = [root_descriptor]
    file_descriptor: int | None = None
    try:
        if not same_file_state(initial_root, os.fstat(root_descriptor)):
            raise EvidenceError("capture root changed while it was opened")
        directory_descriptor = root_descriptor
        for part in logical.parts[:-1]:
            child_descriptor = os.open(part, directory_flags, dir_fd=directory_descriptor)
            descriptors.append(child_descriptor)
            child = os.fstat(child_descriptor)
            if not stat.S_ISDIR(child.st_mode) or child.st_uid != os.getuid():
                raise EvidenceError(f"{label} traverses an unsafe private directory")
            if stat.S_IMODE(child.st_mode) != 0o700:
                raise EvidenceError(f"{label} private directories must have mode 0700")
            directory_descriptor = child_descriptor

        file_descriptor = os.open(logical.parts[-1], file_flags, dir_fd=directory_descriptor)
        before = os.fstat(file_descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise EvidenceError(f"{label} must be a regular file")
        if before.st_uid != os.getuid() or stat.S_IMODE(before.st_mode) != 0o600:
            raise EvidenceError(f"{label} must be owner-only mode 0600")
        if before.st_nlink != 1:
            raise EvidenceError(f"{label} must have exactly one hard link")
        if before.st_size <= 0 or before.st_size > maximum:
            raise EvidenceError(f"{label} size is outside the accepted boundary")

        chunks: list[bytes] = []
        remaining = maximum + 1
        while remaining:
            chunk = os.read(file_descriptor, min(65_536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        content = b"".join(chunks)
        after = os.fstat(file_descriptor)
        if len(content) > maximum or len(content) != before.st_size:
            raise EvidenceError(f"{label} grew, shrank or exceeded its size boundary")
        if not same_file_state(before, after):
            raise EvidenceError(f"{label} changed while it was read")
        current_root = root.lstat()
        if not same_file_state(initial_root, current_root):
            raise EvidenceError("capture root changed while private input was read")
        return content
    finally:
        if file_descriptor is not None:
            os.close(file_descriptor)
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def safe_repository_path(value: str) -> str:
    if not value or "\\" in value or "\x00" in value:
        raise EvidenceError(f"unsafe repository path: {value!r}")
    logical = PurePosixPath(value)
    if logical.is_absolute() or any(part in {"", ".", ".."} for part in logical.parts):
        raise EvidenceError(f"unsafe repository path: {value!r}")
    if logical.as_posix() != value:
        raise EvidenceError(f"non-canonical repository path: {value!r}")
    return value


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


def assert_capture_has_no_claim_fields(capture: dict[str, Any]) -> None:
    forbidden = CAPTURE_FORBIDDEN_KEYS.intersection(nested_field_names(capture))
    if forbidden:
        raise EvidenceError(
            "private capture contains compiler-owned or unsafe fields: "
            + ", ".join(sorted(forbidden))
        )


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
        raise EvidenceError(f"git {' '.join(arguments)} failed: {message}")
    return result.stdout


def read_repository_material(path: str) -> bytes:
    target = ROOT / safe_repository_path(path)
    if target.resolve(strict=True) != target:
        raise EvidenceError(f"repository material must not traverse a link: {path}")
    before = target.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise EvidenceError(f"repository material must be a single-link regular file: {path}")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(target, flags)
    try:
        opened = os.fstat(descriptor)
        if not same_file_state(before, opened):
            raise EvidenceError(f"repository material changed while it was opened: {path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 65_536)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        if not same_file_state(opened, after):
            raise EvidenceError(f"repository material changed while it was read: {path}")
        content = b"".join(chunks)
        if len(content) != opened.st_size:
            raise EvidenceError(f"repository material was not read completely: {path}")
        return content
    finally:
        os.close(descriptor)


def verify_observed_source(capture: dict[str, Any]) -> None:
    source = capture["source"]
    for field in ("protected_main", "detached_checkout", "worktree_clean"):
        if source[field] is not True:
            raise EvidenceError(f"observed host source requires {field}=true")

    commit = source["commit"]
    expected_tree = source["tree"]
    actual_tree = git_output("rev-parse", f"{commit}^{{tree}}").decode().strip()
    if actual_tree != expected_tree:
        raise EvidenceError("source tree does not match the captured commit")

    remote_main = git_output("rev-parse", "--verify", "refs/remotes/origin/main").decode().strip()
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, remote_main],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if ancestor.returncode != 0:
        raise EvidenceError("observed source commit is not accepted protected-main history")

    seen_materials: set[tuple[str, str]] = set()
    for material in source["materials"]:
        role = material["role"]
        path = safe_repository_path(material["path"])
        identity = (role, path)
        if identity in seen_materials:
            raise EvidenceError(f"duplicate source material: {role}:{path}")
        seen_materials.add(identity)
        if role in GIT_BOUND_ROLES:
            blob = git_output("show", f"{commit}:{path}")
            if sha256_bytes(blob) != material["sha256"]:
                raise EvidenceError(f"source material digest mismatch: {path}")
        elif role == "compiled":
            if sha256_bytes(read_repository_material(path)) != material["sha256"]:
                raise EvidenceError(f"compiled material digest mismatch: {path}")
        else:
            raise EvidenceError(f"unrecognised source material role: {role}")

    if seen_materials != REQUIRED_OBSERVED_MATERIALS:
        missing = sorted(REQUIRED_OBSERVED_MATERIALS - seen_materials)
        extra = sorted(seen_materials - REQUIRED_OBSERVED_MATERIALS)
        raise EvidenceError(
            "observed source material inventory is not closed; "
            f"missing={missing!r}; extra={extra!r}"
        )

    for reference in (capture["corpus"]["base"], capture["corpus"]["expansion"]):
        path = safe_repository_path(reference["path"])
        blob = git_output("show", f"{commit}:{path}")
        if sha256_bytes(blob) != reference["sha256"]:
            raise EvidenceError(f"corpus digest mismatch at source commit: {path}")


def verify_telemetry_file(root: Path, capture: dict[str, Any]) -> None:
    retained = capture["telemetry"]["retained_private"]
    value = read_private_file(
        root,
        retained["path"],
        "private telemetry",
        MAX_PRIVATE_TELEMETRY_BYTES,
    )
    if len(value) != retained["bytes"]:
        raise EvidenceError("private telemetry byte count does not match")
    if sha256_bytes(value) != retained["sha256"]:
        raise EvidenceError("private telemetry digest does not match")


def verify_telemetry_counts(capture: dict[str, Any]) -> None:
    telemetry = capture["telemetry"]
    count_fields = (
        "session_start_count",
        "request_count",
        "notification_count",
        "response_count",
        "session_end_count",
        "anomaly_count",
        "malformed_frame_count",
        "non_json_frame_count",
        "truncated_frame_count",
        "server_stderr_count",
    )
    if telemetry["event_count"] != sum(telemetry[field] for field in count_fields):
        raise EvidenceError("telemetry event_count does not match its closed counters")
    if telemetry["session_start_count"] != 1 or telemetry["session_end_count"] != 1:
        raise EvidenceError("telemetry must contain exactly one session start and end")
    observation = capture["observation"]
    minimum_round_trips = sum(
        1
        for stage in (
            observation["initialize"],
            observation["tools_list"],
            observation["resources_list"],
        )
        if stage["observed"]
    ) + len(observation["tool_results"]) + len(observation["resource_results"])
    if telemetry["request_count"] < minimum_round_trips:
        raise EvidenceError("telemetry request_count cannot support the observed stages")
    if telemetry["response_count"] < minimum_round_trips:
        raise EvidenceError("telemetry response_count cannot support the observed stages")
    if (
        observation["initialized_notification_observed"]
        and telemetry["notification_count"] < 1
    ):
        raise EvidenceError("telemetry lacks the observed initialized notification")
    if clean_transport(capture) and telemetry["request_count"] != telemetry["response_count"]:
        raise EvidenceError("clean telemetry must close every request with one response")


def verify_stage(stage: dict[str, Any], label: str) -> None:
    outcome = stage["outcome"]
    observed = stage["observed"]
    error_code = stage["error_code"]
    if outcome == "success" and (not observed or error_code is not None):
        raise EvidenceError(f"{label} success is internally inconsistent")
    if outcome == "error" and (not observed or not isinstance(error_code, int)):
        raise EvidenceError(f"{label} error is internally inconsistent")
    if outcome == "not-observed" and (observed or error_code is not None):
        raise EvidenceError(f"{label} not-observed state is internally inconsistent")


def verify_observation(capture: dict[str, Any]) -> None:
    observation = capture["observation"]
    verify_stage(observation["initialize"], "initialize")
    verify_stage(observation["tools_list"], "tools/list")
    verify_stage(observation["resources_list"], "resources/list")
    for key, item_key in (("tools_list", "operations"), ("resources_list", "resources")):
        stage = observation[key]
        if stage["outcome"] != "success" and stage[item_key]:
            raise EvidenceError(f"{key} cannot publish discovery values without success")

    tool_names = [item["operation"] for item in observation["tool_results"]]
    if len(tool_names) != len(set(tool_names)):
        raise EvidenceError("tool results contain a duplicate operation")
    resource_names = [item["resource"] for item in observation["resource_results"]]
    if len(resource_names) != len(set(resource_names)):
        raise EvidenceError("resource results contain a duplicate resource")
    if (
        observation["initialized_notification_observed"]
        and observation["initialize"]["outcome"] != "success"
    ):
        raise EvidenceError("initialized notification requires successful initialisation")
    if observation["tool_results"] and observation["tools_list"]["outcome"] != "success":
        raise EvidenceError("tool results require successful tools/list discovery")
    if (
        observation["resource_results"]
        and observation["resources_list"]["outcome"] != "success"
    ):
        raise EvidenceError("resource results require successful resources/list discovery")


def verify_protocol(capture: dict[str, Any]) -> None:
    protocol = capture["protocol"]
    negotiated = protocol["negotiated_version"]
    if negotiated is not None and protocol["client_requested_version"] != negotiated:
        raise EvidenceError("negotiated protocol must equal the client-requested version")


def verify_capture_kind(capture: dict[str, Any]) -> None:
    synthetic = capture["capture_kind"] == "synthetic-test-fixture"
    synthetic_host = capture["host"]["name"] == "synthetic-test-host"
    if synthetic != synthetic_host:
        raise EvidenceError("capture kind and allowlisted host identity are inconsistent")
    identities = [
        (material["role"], material["path"])
        for material in capture["source"]["materials"]
    ]
    if len(identities) != len(set(identities)):
        raise EvidenceError("source materials contain a duplicate role and path")


def clean_transport(capture: dict[str, Any]) -> bool:
    telemetry = capture["telemetry"]
    return (
        telemetry["exit_code"] == 0
        and telemetry["pending_request_count"] == 0
        and telemetry["anomaly_count"] == 0
        and telemetry["malformed_frame_count"] == 0
        and telemetry["non_json_frame_count"] == 0
        and telemetry["truncated_frame_count"] == 0
        and telemetry["server_stderr_count"] == 0
    )


def derive_readiness(capture: dict[str, Any]) -> tuple[bool, str, int | None]:
    observation = capture["observation"]
    initialize = observation["initialize"]
    tools_list = observation["tools_list"]
    ready = (
        capture["protocol"]["negotiated_version"] == "2026-07-28"
        and capture["protocol"]["client_requested_version"] == "2026-07-28"
        and observation["host_report"] == "connected"
        and initialize["outcome"] == "success"
        and observation["initialized_notification_observed"] is True
        and tools_list["outcome"] == "success"
        and clean_transport(capture)
    )
    if ready:
        return True, "protocol-negotiation-pass", None
    if initialize["outcome"] == "error":
        return False, "protocol-negotiation-failure", initialize["error_code"]
    if tools_list["outcome"] == "error":
        return False, "tools-list-failure", tools_list["error_code"]
    host_report = observation["host_report"]
    classification = {
        "process-failed": "host-launch-failure",
        "configuration-failed": "configuration-failure",
        "authentication-failed": "authentication-failure",
        "failed-to-connect": "transport-failure",
    }.get(host_report, "transport-failure")
    return False, classification, None


def derive_capability(capture: dict[str, Any], ready: bool) -> tuple[bool, bool, bool]:
    observation = capture["observation"]
    exact_discovery = (
        ready
        and observation["tools_list"]["operations"] == EXACT_OPERATIONS
        and observation["resources_list"]["outcome"] == "success"
        and observation["resources_list"]["resources"] == EXACT_RESOURCES
    )
    tools = observation["tool_results"]
    tool_pass = (
        [item["operation"] for item in tools] == EXACT_OPERATIONS
        and all(item["outcome"] == "success" for item in tools)
        and all(item["structured_plain_text_parity"] == "passed" for item in tools)
        and all(item["receipt_present"] is True for item in tools)
    )
    resources = observation["resource_results"]
    resource_pass = (
        [item["resource"] for item in resources] == EXACT_RESOURCES
        and all(item["outcome"] == "success" for item in resources)
    )
    cases_pass = REQUIRED_CAPABILITY_CASES.issubset(set(capture["corpus"]["case_ids"]))
    host = capture["host"]
    capability_pass = (
        exact_discovery
        and host["probe"] == "model-task"
        and host["model_authentication_supplied"] is True
        and host["model_task_requested"] is True
        and tool_pass
        and resource_pass
        and observation["cancellation"] == {"observed": True, "outcome": "passed"}
        and observation["unsupported_traffic"]
        == {"observed": True, "outcome": "passed"}
    )
    parity_pass = len(tools) == len(EXACT_OPERATIONS) and all(
        item["structured_plain_text_parity"] == "passed" for item in tools
    )
    return exact_discovery, capability_pass and cases_pass, parity_pass


def public_telemetry(capture: dict[str, Any]) -> dict[str, Any]:
    telemetry = capture["telemetry"]
    return {
        "schema": telemetry["schema"],
        "retained_private": {
            "retention": "operator-controlled-local",
            "raw_content_published": False,
            "digest_published": False,
            "byte_count_published": False,
        },
        "event_count": telemetry["event_count"],
        "event_counts": {
            "session_start": telemetry["session_start_count"],
            "request": telemetry["request_count"],
            "notification": telemetry["notification_count"],
            "response": telemetry["response_count"],
            "session_end": telemetry["session_end_count"],
            "anomaly": telemetry["anomaly_count"],
            "malformed_frame": telemetry["malformed_frame_count"],
            "non_json_frame": telemetry["non_json_frame_count"],
            "truncated_frame": telemetry["truncated_frame_count"],
            "server_stderr": telemetry["server_stderr_count"],
        },
        "exit_code": telemetry["exit_code"],
        "pending_request_count": telemetry["pending_request_count"],
    }


def compiler_contract(capture_bytes: bytes) -> dict[str, Any]:
    paths = [
        ("compiler", "scripts/compile_qual_206_strict_modern_evidence.py"),
        ("identity-helper", "scripts/qual_206_strict_modern_identity.mjs"),
        ("capture-schema", "schemas/qual-206-strict-modern-host-capture.schema.json"),
        ("evidence-schema", "schemas/qual-206-strict-modern-host-evidence.schema.json"),
        ("canonical-source", "packages/evidence/src/canonical-json.ts"),
        ("digest-source", "packages/evidence/src/digest.ts"),
        ("canonical-runtime", "packages/evidence/dist/src/canonical-json.js"),
        ("digest-runtime", "packages/evidence/dist/src/digest.js"),
        ("identity-runtime", "packages/evidence/dist/src/index.js"),
    ]
    materials = []
    for role, path in paths:
        digest = sha256_bytes(read_repository_material(path))
        pinned = PINNED_IDENTITY_RUNTIME_SHA256.get(path)
        if pinned is not None and digest != pinned:
            raise EvidenceError(f"shared canonical identity runtime drifted: {path}")
        materials.append({"role": role, "path": path, "sha256": digest})
    return {
        "identity_domain": IDENTITY_DOMAIN,
        "materials": materials,
        "private_capture": {
            "bytes": len(capture_bytes),
            "sha256": sha256_bytes(capture_bytes),
            "retention": "operator-controlled-local",
            "raw_content_published": False,
        },
    }


def shared_content_address(value: dict[str, Any]) -> str:
    for path, expected in PINNED_IDENTITY_RUNTIME_SHA256.items():
        if sha256_bytes(read_repository_material(path)) != expected:
            raise EvidenceError(f"shared canonical identity runtime drifted: {path}")
    node = shutil.which("node")
    if node is None:
        raise EvidenceError("Node.js is required for shared canonical evidence identity")
    input_bytes = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    result = subprocess.run(
        [node, str(IDENTITY_HELPER_PATH)],
        cwd=ROOT,
        check=False,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={"PATH": os.environ.get("PATH", os.defpath)},
        timeout=10,
    )
    stdout = result.stdout.decode("utf-8", errors="strict")
    stderr = result.stderr.decode("utf-8", errors="replace")
    if result.returncode != 0 or stderr or not stdout.endswith("\n"):
        raise EvidenceError(
            "shared canonical identity helper failed closed"
            + (f": {stderr.strip()}" if stderr.strip() else "")
        )
    identity = stdout.removesuffix("\n")
    if not re.fullmatch(re.escape(IDENTITY_PREFIX) + r"[0-9a-f]{64}", identity):
        raise EvidenceError("shared canonical identity helper returned an invalid identity")
    return identity


def compile_evidence(capture: dict[str, Any], capture_bytes: bytes) -> dict[str, Any]:
    ready, readiness_classification, error_code = derive_readiness(capture)
    exact_discovery, reported_capability_pass, parity_pass = derive_capability(capture, ready)
    synthetic = capture["capture_kind"] == "synthetic-test-fixture"
    capability_pass = synthetic and reported_capability_pass
    status = "capability_pass" if capability_pass else "ready_unscored" if ready else "not_ready"
    observation = capture["observation"]
    visible_results = observation["tool_results"] if synthetic and ready else []
    visible_resources = observation["resource_results"] if synthetic and ready else []
    if synthetic and parity_pass:
        parity = "passed"
    elif synthetic and any(
        item["structured_plain_text_parity"] == "failed" for item in visible_results
    ):
        parity = "failed"
    else:
        parity = "not-tested"

    source = dict(capture["source"])
    source.update(
        {
            "protected_main": False if synthetic else source["protected_main"],
            "detached_checkout": False if synthetic else source["detached_checkout"],
            "worktree_clean": False if synthetic else source["worktree_clean"],
            "production_registration": False,
            "production_activation": False,
            "public_endpoint_created": False,
        }
    )
    surface = dict(capture["surface"])
    surface["production_registration"] = False
    limitations = (
        [
            "Synthetic fixture: this record tests the compiler and is not host evidence.",
            "A synthetic capability pass makes no claim about a real client or provider.",
        ]
        if synthetic
        else [
            "This projection compiles a closed capture summary, not an event-level transcript.",
            "Real host capability remains unscored until a versioned exact-five "
            "event collector exists.",
            "Protected-main ancestry is checked against the local origin/main ref, "
            "not the network.",
            "This single capture does not complete the independent-host gate.",
        ]
    )

    evidence: dict[str, Any] = {
        "schema": "gis-ai-go.qual-206-strict-modern-host-evidence.v2",
        "evidence_id": "",
        "classification": (
            "synthetic-test-only"
            if synthetic
            else "pre-activation-strict-modern-host-summary"
        ),
        "status": status,
        "observed_at": capture["observed_at"],
        "schema_contract": {
            "path": "schemas/qual-206-strict-modern-host-evidence.schema.json",
            "sha256": sha256_bytes(EVIDENCE_SCHEMA_PATH.read_bytes()),
        },
        "compiler_contract": compiler_contract(capture_bytes),
        "lineage": {
            "relationship": "preserved-separate-not-superseded",
            "historical_artifacts": [dict(item) for item in HISTORICAL_LINEAGE],
        },
        "source": source,
        "host": capture["host"],
        "protocol": capture["protocol"],
        "surface": surface,
        "readiness": {
            "outcome": "ready" if ready else "not_ready",
            "classification": readiness_classification,
            "initialize_observed": observation["initialize"]["observed"],
            "initialize_success": observation["initialize"]["outcome"] == "success",
            "initialized_notification_observed": observation[
                "initialized_notification_observed"
            ],
            "tools_list_observed": observation["tools_list"]["observed"],
            "tools_list_success": observation["tools_list"]["outcome"] == "success",
            "host_report": observation["host_report"],
            "error_code": error_code,
        },
        "capability": {
            "outcome": "passed" if capability_pass else "unscored",
            "corpus": capture["corpus"],
            "exact_five_surface_discovered": synthetic and exact_discovery,
            "exact_five_capability_exercised": capability_pass,
            "discovered_operations": (
                observation["tools_list"]["operations"] if synthetic and ready else []
            ),
            "discovered_resources": (
                observation["resources_list"]["resources"] if synthetic and ready else []
            ),
            "tool_results": visible_results,
            "resource_results": visible_resources,
            "structured_plain_text_parity": parity,
            "cancellation": (
                observation["cancellation"]["outcome"] if synthetic else "not-tested"
            ),
            "unsupported_traffic": (
                observation["unsupported_traffic"]["outcome"]
                if synthetic
                else "not-tested"
            ),
            "model_task_requested": capture["host"]["model_task_requested"],
        },
        "telemetry": public_telemetry(capture),
        "isolation": capture["isolation"],
        "claims": {
            "live_host_session": False,
            "strict_modern_transport_ready": False,
            "capability_scored": False,
            "exact_five_host_capability": False,
            "live_provider_call": False,
            "remote_http_host": False,
            "independent_host_gate_completed": False,
            "production_registration": False,
            "production_activation": False,
            "public_deployment": False,
            "registry_publication": False,
            "release_acceptance": False,
            "complete_qual_206": False,
        },
        "limitations": limitations,
        "boundary": BOUNDARY,
    }
    identity_core = dict(evidence)
    del identity_core["evidence_id"]
    evidence["evidence_id"] = shared_content_address(identity_core)
    return evidence


def assert_public_safe(evidence: dict[str, Any]) -> None:
    def visit(node: object, parent: str | None = None) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key in PUBLIC_FORBIDDEN_KEYS:
                    raise EvidenceError(f"public evidence contains forbidden field: {key}")
                visit(value, key)
        elif isinstance(node, list):
            for value in node:
                visit(value, parent)

    visit(evidence)
    encoded = json.dumps(evidence, ensure_ascii=False, allow_nan=False)
    match = PUBLIC_FORBIDDEN_PATTERN.search(encoded)
    if match:
        raise EvidenceError("public evidence contains a private path, secret or session value")


def canonical_output(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode(
        "utf-8"
    )


def write_exclusive_atomic(path: Path, value: bytes) -> None:
    if not path.is_absolute():
        raise EvidenceError("output path must be absolute")
    parent = path.parent
    if not parent.exists() or not parent.is_dir():
        raise EvidenceError("output parent directory must already exist")
    if parent.resolve(strict=True) != parent:
        raise EvidenceError("output parent must not traverse a symbolic link")
    parent_metadata = parent.lstat()
    if (
        not stat.S_ISDIR(parent_metadata.st_mode)
        or parent_metadata.st_uid != os.getuid()
        or stat.S_IMODE(parent_metadata.st_mode) & 0o022
    ):
        raise EvidenceError("output parent must be owned by the user and not group/world writable")
    if path.exists() or path.is_symlink():
        raise EvidenceError("output already exists; historical evidence is never overwritten")
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(
        os, "O_NOFOLLOW", 0
    )
    parent_descriptor = os.open(parent, directory_flags)
    temporary_name = f".qual-206-host-evidence-{os.getpid()}-{secrets.token_hex(12)}"
    temporary_descriptor: int | None = None
    try:
        if not same_file_state(parent_metadata, os.fstat(parent_descriptor)):
            raise EvidenceError("output parent changed while it was opened")
        temporary_descriptor = os.open(
            temporary_name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            0o600,
            dir_fd=parent_descriptor,
        )
        offset = 0
        while offset < len(value):
            written = os.write(temporary_descriptor, value[offset:])
            if written <= 0:
                raise EvidenceError("output write made no progress")
            offset += written
        os.fchmod(temporary_descriptor, 0o644)
        os.fsync(temporary_descriptor)
        os.close(temporary_descriptor)
        temporary_descriptor = None
        os.link(
            temporary_name,
            path.name,
            src_dir_fd=parent_descriptor,
            dst_dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        os.fsync(parent_descriptor)
    except FileExistsError as error:
        raise EvidenceError(
            "output already exists; historical evidence is never overwritten"
        ) from error
    finally:
        if temporary_descriptor is not None:
            os.close(temporary_descriptor)
        try:
            os.unlink(temporary_name, dir_fd=parent_descriptor)
        except FileNotFoundError:
            pass
        os.close(parent_descriptor)


def compile_capture(capture_root: Path, capture_path: Path, output: Path) -> dict[str, Any]:
    capture_schema = load_schema(CAPTURE_SCHEMA_PATH)
    evidence_schema = load_schema(EVIDENCE_SCHEMA_PATH)
    capture_validator = Draft202012Validator(
        capture_schema,
        format_checker=FormatChecker(),
    )
    evidence_validator = Draft202012Validator(
        evidence_schema,
        format_checker=FormatChecker(),
    )
    capture_bytes = read_private_file(
        capture_root,
        capture_path,
        "capture manifest",
        MAX_CAPTURE_BYTES,
    )
    capture = parse_json_bytes(capture_bytes, "capture manifest")
    assert_capture_has_no_claim_fields(capture)
    validate(capture_validator, capture, "capture manifest")
    verify_telemetry_file(capture_root, capture)
    verify_telemetry_counts(capture)
    verify_observation(capture)
    verify_protocol(capture)
    verify_capture_kind(capture)
    if capture["capture_kind"] == "observed-host-session":
        verify_observed_source(capture)
    evidence = compile_evidence(capture, capture_bytes)
    assert_public_safe(evidence)
    validate(evidence_validator, evidence, "compiled public evidence")
    write_exclusive_atomic(output, canonical_output(evidence))
    return evidence


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        description=(
            "Compile a private strict MCP 2026-07-28 host capture into bounded, "
            "deterministic public evidence with a shared RFC 8785 identity."
        )
    )
    value.add_argument("--capture-root", required=True)
    value.add_argument("--capture", required=True)
    value.add_argument("--output", required=True)
    return value


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        root = normalise_capture_root(arguments.capture_root)
        output = Path(arguments.output)
        if not output.is_absolute():
            output = (Path.cwd() / output).absolute()
        evidence = compile_capture(root, Path(arguments.capture), output)
    except (EvidenceError, OSError, subprocess.SubprocessError) as error:
        print(f"QUAL-206 evidence compilation failed: {error}", file=sys.stderr)
        return 2
    print(
        f"Wrote {evidence['classification']} {evidence['status']} evidence to {output}.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
