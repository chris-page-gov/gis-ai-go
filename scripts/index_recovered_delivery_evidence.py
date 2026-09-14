#!/usr/bin/env python3
"""Build an owner-only index from a verified EVID-211 projection generation.

The utility never reads raw Codex rollouts. It verifies the complete evidence store
offline, selects the newest captured Codex closure manifest, then reads only the
manifest and its captured user-visible projection objects. Output is a new private
directory outside the repository; an existing destination is never replaced.
"""

from __future__ import annotations

import argparse
import contextlib
import gzip
import hashlib
import json
import math
import os
import re
import shutil
import sqlite3
import stat
import sys
import tempfile
from collections.abc import Callable, Iterator, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, BinaryIO

from capture_delivery_evidence import (
    BOUNDARIES,
    CODEX_GENERATION_SCHEMA,
    CODEX_PROJECTION_SCHEMA,
    EvidenceCaptureError,
    INTERMEDIATE_CODEX_PROJECTION_SCHEMA,
    LEGACY_CODEX_GENERATION_SCHEMA,
    LEGACY_CODEX_PROJECTION_SCHEMA,
    MAX_CODEX_PROJECTED_LINE_BYTES,
    MAX_METADATA_BYTES,
    _has_extended_acl,
    _require_enforced_volume_ownership,
    canonical_json,
    private_umask,
)
from verify_delivery_evidence import EvidenceVerificationError, verify_store


INDEX_SCHEMA = "gis-ai-go.private-recovered-delivery-index.v1"
JOURNAL_KIND = "codex-thread-closure-generation-manifest"
PROJECTION_KIND = "codex-user-visible-projection"
ALLOWED_GENERATION_SCHEMAS = {
    LEGACY_CODEX_GENERATION_SCHEMA,
    CODEX_GENERATION_SCHEMA,
}
ALLOWED_PROJECTION_SCHEMAS = {
    LEGACY_CODEX_PROJECTION_SCHEMA,
    INTERMEDIATE_CODEX_PROJECTION_SCHEMA,
    CODEX_PROJECTION_SCHEMA,
}
CLAUDE_PATTERN = re.compile(
    r"(?:\bclaude\b|anthropic|qual[-_ ]?206[^\n]{0,120}claude|host[-_ ]?002)",
    re.IGNORECASE,
)
AUTHENTICATION_PATTERN = re.compile(
    r"(?:claude\s+auth|auth(?:entication)?\s+status|oauth|log\s*in|login|keychain)",
    re.IGNORECASE,
)
ACTIVATION_PATTERN = re.compile(
    r"GIS_AI_GO_QUAL_206_CLAUDE[^\s=]*\s*=\s*(?:1|true)", re.IGNORECASE
)
HARNESS_PATTERN = re.compile(
    r"qual_206_claude(?:_exact_five)?_capability_harness\.mjs", re.IGNORECASE
)
READINESS_PATTERN = re.compile(
    r"(?:mcp\s+list|stdio[_ -]?(?:observer|readiness)|transport[_ -]?readiness|"
    r"server/discover|modern[_ -]?stdio)",
    re.IGNORECASE,
)
VERIFIER_PATTERN = re.compile(
    r"(?:verify_qual_206_claude|test_qual_206_claude|"
    r"(?:pytest|unittest|pnpm\s+(?:run\s+)?test)[^\n]{0,160}claude)",
    re.IGNORECASE,
)
SDK_COST_KEYS = {"costusd", "totalcostusd"}
TOKEN_KEYS = {
    "cached_input_tokens",
    "input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
}
ASSIGNMENT_TOOLS = {
    "spawn_agent": "spawn",
    "followup_task": "follow-up",
    "send_message": "inter-agent-message",
    "create_thread": "new-thread",
    "send_message_to_thread": "thread-message",
}
OUTPUT_FILES = (
    "messages.jsonl",
    "agent-assignments.jsonl",
    "claude-ledger.jsonl",
    "process-sessions.jsonl",
    "sdk-costs.jsonl",
    "token-usage.jsonl",
    "turn-activity.jsonl",
    "README.md",
)


class RecoveryIndexError(RuntimeError):
    """A safe, path-free recovery-index failure."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class _DigestingReader:
    """Hash a compressed projection while `gzip` consumes it once."""

    def __init__(self, stream: BinaryIO) -> None:
        self.stream = stream
        self.hasher = hashlib.sha256()
        self.bytes_read = 0

    def read(self, size: int = -1) -> bytes:
        value = self.stream.read(size)
        self.hasher.update(value)
        self.bytes_read += len(value)
        return value

    def seek(self, offset: int, whence: int = os.SEEK_SET) -> int:
        return self.stream.seek(offset, whence)

    def tell(self) -> int:
        return self.stream.tell()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _normalised_tool_name(value: object) -> str:
    if not isinstance(value, str):
        return ""
    tail = re.split(r"[.:/]", value)[-1]
    return re.sub(r"[^a-z0-9_]+", "_", tail.lower()).strip("_")


def _json_text(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _safe_text(value: object) -> str:
    if isinstance(value, str):
        return value
    return _json_text(value)


def is_claude_related(*values: object) -> bool:
    """Return whether retained, already-redacted values mention the Claude lane."""

    return bool(CLAUDE_PATTERN.search("\n".join(_safe_text(value) for value in values)))


def classify_claude_candidate(*values: object) -> str:
    """Classify a candidate without asserting that it was an actual model attempt."""

    text = "\n".join(_safe_text(value) for value in values)
    if AUTHENTICATION_PATTERN.search(text):
        return "authentication"
    if ACTIVATION_PATTERN.search(text) and HARNESS_PATTERN.search(text):
        return "live-observation-candidate"
    if READINESS_PATTERN.search(text):
        return "readiness"
    if VERIFIER_PATTERN.search(text):
        return "verifier-or-test"
    return "implementation-or-research"


def _walk_json_documents(value: object, *, depth: int = 0) -> Iterator[tuple[str, object]]:
    """Yield bounded structured values and exact JSON strings contained within them."""

    if depth > 12:
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            yield str(key), item
            yield from _walk_json_documents(item, depth=depth + 1)
        return
    if isinstance(value, list):
        for item in value:
            yield from _walk_json_documents(item, depth=depth + 1)
        return
    if not isinstance(value, str) or len(value) > 1024 * 1024:
        return
    stripped = value.strip()
    if not stripped.startswith(("{", "[")):
        return
    try:
        parsed = json.loads(stripped)
    except (ValueError, TypeError):
        return
    if isinstance(parsed, (dict, list)):
        yield from _walk_json_documents(parsed, depth=depth + 1)


def extract_sdk_costs(value: object) -> list[dict[str, object]]:
    """Extract finite non-negative reported USD cost-field candidates."""

    found: list[dict[str, object]] = []
    for key, item in _walk_json_documents(value):
        normalised = re.sub(r"[^a-z0-9]", "", key.lower())
        if normalised not in SDK_COST_KEYS:
            continue
        if (
            isinstance(item, (int, float))
            and not isinstance(item, bool)
            and math.isfinite(float(item))
            and float(item) >= 0
        ):
            found.append(
                {
                    "field": key,
                    "value": item,
                    "currency": "USD",
                    "classification": "reported-cost-field-candidate",
                    "provider_usage_proven": False,
                    "actual_billed_cost": "unknown",
                }
            )
    return found


def _session_values(value: object, *, depth: int = 0) -> set[str]:
    """Return session values used only for private, unambiguous process linkage."""

    if depth > 12:
        return set()
    found: set[str] = set()
    if isinstance(value, Mapping):
        for key, item in value.items():
            normalised = re.sub(r"[^a-z0-9]", "", str(key).lower())
            if (
                normalised == "sessionid"
                and isinstance(item, (str, int))
                and not isinstance(item, bool)
            ):
                found.add(str(item))
            found.update(_session_values(item, depth=depth + 1))
        return found
    if isinstance(value, list):
        for item in value:
            found.update(_session_values(item, depth=depth + 1))
        return found
    if isinstance(value, str) and len(value) <= 1024 * 1024:
        stripped = value.strip()
        if stripped.startswith(("{", "[")):
            with contextlib.suppress(ValueError, TypeError):
                parsed = json.loads(stripped)
                found.update(_session_values(parsed, depth=depth + 1))
        # Outer orchestration calls can retain JavaScript rather than direct JSON.
        for match in re.finditer(
            r"(?:session_id|sessionId)\s*[\"']?\s*:\s*[\"']?([A-Za-z0-9._-]{1,128})",
            value,
        ):
            found.add(match.group(1))
    return found


def _is_exec_call(tool_name: str, arguments: object) -> bool:
    normalised = _normalised_tool_name(tool_name)
    return normalised == "exec_command" or (
        normalised == "exec" and "exec_command" in _safe_text(arguments)
    )


def _is_write_stdin_call(tool_name: str, arguments: object) -> bool:
    normalised = _normalised_tool_name(tool_name)
    return normalised == "write_stdin" or (
        normalised == "exec" and "write_stdin" in _safe_text(arguments)
    )


def _continuation_kind(arguments: object) -> str:
    if isinstance(arguments, Mapping):
        chars = arguments.get("chars")
        return "stdin" if isinstance(chars, str) and bool(chars) else "poll"
    text = _safe_text(arguments)
    match = re.search(r"chars\s*[\"']?\s*:\s*[\"']([^\"']*)[\"']", text)
    return "stdin" if match is not None and bool(match.group(1)) else "poll"


def _assignment_kind(tool_name: object, namespace: object) -> str | None:
    normalised = _normalised_tool_name(tool_name)
    if normalised not in ASSIGNMENT_TOOLS:
        return None
    namespace_text = str(namespace or "").lower()
    full_name = str(tool_name or "").lower()
    if normalised in {"send_message", "spawn_agent", "followup_task"} and not (
        "collaboration" in namespace_text
        or "collaboration" in full_name
        or full_name == normalised
    ):
        return None
    return ASSIGNMENT_TOOLS[normalised]


def _object_path(store: Path, digest: str) -> Path:
    return store / "objects" / "sha256" / digest[:2] / digest


def _open_regular(path: Path) -> tuple[int, os.stat_result]:
    try:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    except OSError as error:
        raise RecoveryIndexError("verified-object-unavailable") from error
    metadata = os.fstat(descriptor)
    if (
        not stat.S_ISREG(metadata.st_mode)
        or metadata.st_uid != os.getuid()
        or metadata.st_nlink != 1
    ):
        os.close(descriptor)
        raise RecoveryIndexError("verified-object-shape-changed")
    return descriptor, metadata


def _read_bound_object(store: Path, digest: str, expected_bytes: int) -> bytes:
    path = _object_path(store, digest)
    descriptor, before = _open_regular(path)
    try:
        if before.st_size != expected_bytes:
            raise RecoveryIndexError("verified-object-size-changed")
        chunks: list[bytes] = []
        total = 0
        hasher = hashlib.sha256()
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_METADATA_BYTES:
                raise RecoveryIndexError("verified-manifest-is-oversized")
            hasher.update(chunk)
            chunks.append(chunk)
        after = os.fstat(descriptor)
        current = path.lstat()
        if (
            total != expected_bytes
            or hasher.hexdigest() != digest
            or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            or (after.st_dev, after.st_ino) != (current.st_dev, current.st_ino)
        ):
            raise RecoveryIndexError("verified-manifest-binding-changed")
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _journal_pass(
    descriptor: int,
    *,
    select_manifest: bool = False,
    wanted_projection_identities: set[str] | None = None,
) -> tuple[dict[str, object], dict[str, Any] | None, dict[str, dict[str, Any]]]:
    os.lseek(descriptor, 0, os.SEEK_SET)
    hasher = hashlib.sha256()
    count = 0
    head_event_sha256: str | None = None
    latest_manifest: dict[str, Any] | None = None
    projection_events: dict[str, dict[str, Any]] = {}
    with os.fdopen(os.dup(descriptor), "rb") as stream:
        while True:
            raw = stream.readline(MAX_METADATA_BYTES + 1)
            if not raw:
                break
            if len(raw) > MAX_METADATA_BYTES or not raw.endswith(b"\n"):
                raise RecoveryIndexError("verified-journal-shape-changed")
            hasher.update(raw)
            count += 1
            try:
                event = json.loads(raw)
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise RecoveryIndexError("verified-journal-shape-changed") from error
            if not isinstance(event, dict):
                raise RecoveryIndexError("verified-journal-shape-changed")
            event_sha256 = event.get("event_sha256")
            if isinstance(event_sha256, str):
                head_event_sha256 = event_sha256
            source = event.get("source")
            disposition = event.get("disposition")
            if not isinstance(source, dict) or not isinstance(disposition, dict):
                continue
            if (
                select_manifest
                and source.get("kind") == JOURNAL_KIND
                and disposition.get("status") == "captured"
            ):
                latest_manifest = event
            identity = source.get("identity")
            if (
                wanted_projection_identities is not None
                and isinstance(identity, str)
                and identity in wanted_projection_identities
                and source.get("kind") == PROJECTION_KIND
            ):
                projection_events[identity] = event
    return (
        {
            "bytes": os.fstat(descriptor).st_size,
            "events": count,
            "sha256": hasher.hexdigest(),
            "head_event_sha256": head_event_sha256,
        },
        latest_manifest,
        projection_events,
    )


def _verify_journal_snapshot(
    scan: Mapping[str, object], verified: Mapping[str, object]
) -> None:
    if (
        scan.get("events") != verified.get("journal_events")
        or scan.get("head_event_sha256") != verified.get("journal_head_sha256")
        or scan.get("sha256") != verified.get("journal_sha256")
        or verified.get("verified") is not True
    ):
        raise RecoveryIndexError("journal-changed-after-verification")


def _parse_manifest(raw: bytes) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RecoveryIndexError("verified-manifest-is-invalid") from error
    if (
        not isinstance(value, dict)
        or value.get("schema") not in ALLOWED_GENERATION_SCHEMAS
        or raw != canonical_json(value, pretty=True)
        or not isinstance(value.get("files"), list)
        or not value["files"]
    ):
        raise RecoveryIndexError("verified-manifest-is-invalid")
    if any(
        not isinstance(item, dict) or item.get("disposition") != "captured"
        for item in value["files"]
    ):
        raise RecoveryIndexError("selected-generation-is-not-fully-projected")
    return value


def _payload_arguments(payload: Mapping[str, object]) -> object:
    if "arguments" in payload:
        return payload["arguments"]
    return payload.get("input")


def _source_binding(
    context: Mapping[str, object], raw: bytes, value: Mapping[str, object]
) -> dict[str, object]:
    return {
        "thread_ref": context["thread_ref"],
        "manifest_event_sequence": context["manifest_event_sequence"],
        "manifest_event_sha256": context["manifest_event_sha256"],
        "manifest_object_sha256": context["manifest_object_sha256"],
        "projection_event_sequence": context["projection_event_sequence"],
        "projection_event_sha256": context["projection_event_sha256"],
        "projection_object_sha256": context["projection_object_sha256"],
        "projection_uncompressed_sha256": context[
            "projection_uncompressed_sha256"
        ],
        "source_line": value.get("source_line"),
        "source_line_sha256": value.get("source_line_sha256"),
        "source_bytes": value.get("source_bytes"),
        "projected_line_sha256": _sha256_bytes(raw),
    }


def _iter_projection(
    store: Path,
    item: Mapping[str, object],
    context: Mapping[str, object],
) -> Iterator[tuple[bytes, dict[str, Any], dict[str, object]]]:
    digest = item.get("object_sha256")
    expected_bytes = item.get("object_bytes")
    if not isinstance(digest, str) or not isinstance(expected_bytes, int):
        raise RecoveryIndexError("verified-projection-binding-is-invalid")
    path = _object_path(store, digest)
    descriptor, before = _open_regular(path)
    try:
        if before.st_size != expected_bytes:
            raise RecoveryIndexError("verified-projection-size-changed")
        uncompressed = hashlib.sha256()
        uncompressed_bytes = 0
        header_seen = False
        footer_seen = False
        with os.fdopen(os.dup(descriptor), "rb") as compressed_stream:
            digesting_stream = _DigestingReader(compressed_stream)
            with gzip.GzipFile(fileobj=digesting_stream, mode="rb") as stream:
                while True:
                    raw = stream.readline(MAX_CODEX_PROJECTED_LINE_BYTES + 1)
                    if not raw:
                        break
                    if len(raw) > MAX_CODEX_PROJECTED_LINE_BYTES or not raw.endswith(b"\n"):
                        raise RecoveryIndexError("verified-projection-shape-changed")
                    uncompressed.update(raw)
                    uncompressed_bytes += len(raw)
                    try:
                        value = json.loads(raw)
                    except (UnicodeDecodeError, json.JSONDecodeError) as error:
                        raise RecoveryIndexError("verified-projection-shape-changed") from error
                    if not isinstance(value, dict) or raw != canonical_json(value):
                        raise RecoveryIndexError("verified-projection-shape-changed")
                    record = value.get("record")
                    if record == "projection-header":
                        if header_seen or value.get("schema") not in ALLOWED_PROJECTION_SCHEMAS:
                            raise RecoveryIndexError("verified-projection-shape-changed")
                        header_seen = True
                    elif record == "projection-footer":
                        footer_seen = True
                    elif record == "projected-rollout-record":
                        if not header_seen or footer_seen:
                            raise RecoveryIndexError("verified-projection-shape-changed")
                        yield raw, value, _source_binding(context, raw, value)
            if (
                digesting_stream.bytes_read != expected_bytes
                or digesting_stream.hasher.hexdigest() != digest
            ):
                raise RecoveryIndexError("verified-projection-digest-changed")
        if not header_seen or not footer_seen:
            raise RecoveryIndexError("verified-projection-shape-changed")
        if (
            uncompressed.hexdigest() != item.get("uncompressed_sha256")
            or uncompressed_bytes != item.get("uncompressed_bytes")
        ):
            raise RecoveryIndexError("verified-projection-uncompressed-binding-changed")
        after = os.fstat(descriptor)
        current = path.lstat()
        if (
            (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            or (after.st_dev, after.st_ino) != (current.st_dev, current.st_ino)
        ):
            raise RecoveryIndexError("verified-projection-path-changed")
    finally:
        os.close(descriptor)


def _write_jsonl(stream: BinaryIO, value: object) -> None:
    stream.write(canonical_json(value))


def _open_private_output(path: Path) -> BinaryIO:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    return os.fdopen(descriptor, "wb")


def _is_inside_git_checkout(path: Path) -> bool:
    """Return whether a path is at or below any Git checkout or worktree."""

    return any(os.path.lexists(candidate / ".git") for candidate in (path, *path.parents))


def _prepare_output(output: Path, store: Path) -> tuple[Path, Path]:
    if os.path.lexists(output):
        raise RecoveryIndexError("output-already-exists")
    if output.name in {"", ".", ".."}:
        raise RecoveryIndexError("output-path-is-invalid")
    try:
        parent = output.parent.resolve(strict=True)
    except OSError as error:
        raise RecoveryIndexError("output-parent-is-unavailable") from error
    parent_metadata = parent.stat()
    if (
        not stat.S_ISDIR(parent_metadata.st_mode)
        or parent_metadata.st_uid != os.getuid()
        or stat.S_IMODE(parent_metadata.st_mode) & 0o022
    ):
        raise RecoveryIndexError("output-parent-is-not-owner-controlled")
    canonical_output = parent / output.name
    repository = Path(__file__).resolve().parents[1]
    canonical_store = store.resolve(strict=True)
    if canonical_output.is_relative_to(repository) or canonical_output.is_relative_to(
        canonical_store
    ):
        raise RecoveryIndexError("output-must-be-outside-repository-and-store")
    if _is_inside_git_checkout(canonical_output):
        raise RecoveryIndexError("output-must-be-outside-any-git-checkout")
    try:
        _require_enforced_volume_ownership(parent)
    except EvidenceCaptureError as error:
        raise RecoveryIndexError("output-volume-is-not-admitted") from error
    staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.incoming-", dir=parent))
    try:
        os.chmod(staging, 0o700)
        if _has_extended_acl(staging):
            raise RecoveryIndexError("private-output-inherits-extended-acl")
    except Exception:
        shutil.rmtree(staging)
        raise
    return canonical_output, staging


def _database(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    os.chmod(path, 0o600)
    connection.executescript(
        """
        PRAGMA journal_mode=DELETE;
        PRAGMA synchronous=FULL;
        CREATE TABLE calls (
            id INTEGER PRIMARY KEY,
            thread_ref TEXT NOT NULL,
            call_id TEXT,
            tool_name TEXT NOT NULL,
            namespace TEXT,
            server TEXT,
            timestamp TEXT,
            arguments_json TEXT NOT NULL,
            source_json TEXT NOT NULL,
            assignment_kind TEXT,
            direct_claude INTEGER NOT NULL DEFAULT 0,
            classification TEXT,
            paired_output_count INTEGER NOT NULL DEFAULT 0,
            process_ref TEXT,
            process_event TEXT
        );
        CREATE TABLE outputs (
            id INTEGER PRIMARY KEY,
            thread_ref TEXT NOT NULL,
            call_id TEXT,
            timestamp TEXT,
            output_json TEXT NOT NULL,
            source_json TEXT NOT NULL,
            direct_claude INTEGER NOT NULL DEFAULT 0,
            paired_call_id INTEGER,
            process_ref TEXT
        );
        CREATE INDEX calls_by_correlation ON calls(thread_ref, call_id);
        CREATE INDEX calls_by_process ON calls(process_ref, process_event, id);
        CREATE INDEX outputs_by_correlation ON outputs(thread_ref, call_id);
        CREATE INDEX outputs_by_paired_call_id ON outputs(paired_call_id, id);
        CREATE INDEX outputs_by_process ON outputs(process_ref, id);
        """
    )
    return connection


def _first_projection_pass(
    store: Path,
    manifest: Mapping[str, object],
    contexts: Mapping[str, Mapping[str, object]],
    connection: sqlite3.Connection,
) -> dict[str, int]:
    counts = {
        "projected_records": 0,
        "tool_calls": 0,
        "tool_outputs": 0,
    }
    for item in manifest["files"]:  # type: ignore[index]
        identity = str(item["source_identity"])
        context = contexts[identity]
        for _raw, value, source in _iter_projection(store, item, context):
            counts["projected_records"] += 1
            payload = value.get("payload")
            if value.get("source_type") != "response_item" or not isinstance(payload, dict):
                continue
            event_type = payload.get("type")
            if event_type in {"custom_tool_call", "function_call"}:
                name = payload.get("name")
                if not isinstance(name, str) or not name:
                    continue
                arguments = _payload_arguments(payload)
                assignment_kind = _assignment_kind(name, payload.get("namespace"))
                connection.execute(
                    """
                    INSERT INTO calls(
                        thread_ref, call_id, tool_name, namespace, server, timestamp,
                        arguments_json, source_json, assignment_kind, direct_claude
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        context["thread_ref"],
                        payload.get("call_id"),
                        name,
                        payload.get("namespace"),
                        payload.get("server"),
                        value.get("timestamp"),
                        _json_text(arguments),
                        _json_text(source),
                        assignment_kind,
                        int(is_claude_related(name, arguments)),
                    ),
                )
                counts["tool_calls"] += 1
            elif event_type in {"custom_tool_call_output", "function_call_output"}:
                output = payload.get("output")
                connection.execute(
                    """
                    INSERT INTO outputs(
                        thread_ref, call_id, timestamp, output_json, source_json,
                        direct_claude
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        context["thread_ref"],
                        payload.get("call_id"),
                        value.get("timestamp"),
                        _json_text(output),
                        _json_text(source),
                        int(is_claude_related(output)),
                    ),
                )
                counts["tool_outputs"] += 1
    connection.commit()
    return counts


def _correlate_calls_and_outputs(connection: sqlite3.Connection) -> dict[str, int]:
    """Correlate exact call IDs and private async process sessions."""

    counts = {
        "ambiguous_call_output_correlations": 0,
        "linked_process_sessions": 0,
        "ambiguous_process_sessions": 0,
    }
    correlations = connection.execute(
        """
        SELECT thread_ref, call_id, COUNT(*)
        FROM calls
        WHERE call_id IS NOT NULL
        GROUP BY thread_ref, call_id
        """
    ).fetchall()
    for thread_ref, call_id, call_count in correlations:
        outputs = connection.execute(
            "SELECT id FROM outputs WHERE thread_ref = ? AND call_id = ? ORDER BY id",
            (thread_ref, call_id),
        ).fetchall()
        if call_count == 1:
            call_pk = connection.execute(
                "SELECT id FROM calls WHERE thread_ref = ? AND call_id = ?",
                (thread_ref, call_id),
            ).fetchone()[0]
            connection.execute(
                "UPDATE calls SET paired_output_count = ? WHERE id = ?",
                (len(outputs), call_pk),
            )
            connection.executemany(
                "UPDATE outputs SET paired_call_id = ? WHERE id = ?",
                [(call_pk, output[0]) for output in outputs],
            )
        elif outputs:
            counts["ambiguous_call_output_correlations"] += len(outputs)

    starts: dict[str, list[int]] = {}
    followers: dict[str, list[tuple[int, str]]] = {}
    call_rows = connection.execute(
        "SELECT id, tool_name, arguments_json FROM calls ORDER BY id"
    )
    for call_pk, tool_name, arguments_json in call_rows:
        arguments = json.loads(arguments_json)
        if _is_exec_call(tool_name, arguments):
            outputs = [
                json.loads(row[0])
                for row in connection.execute(
                    "SELECT output_json FROM outputs WHERE paired_call_id = ? ORDER BY id",
                    (call_pk,),
                )
            ]
            session_ids: set[str] = set()
            for output in outputs:
                session_ids.update(_session_values(output))
            if len(session_ids) == 1:
                starts.setdefault(next(iter(session_ids)), []).append(call_pk)
            elif len(session_ids) > 1:
                counts["ambiguous_process_sessions"] += 1
        elif _is_write_stdin_call(tool_name, arguments):
            session_ids = _session_values(arguments)
            if len(session_ids) == 1:
                followers.setdefault(next(iter(session_ids)), []).append(
                    (call_pk, _continuation_kind(arguments))
                )
            elif len(session_ids) > 1:
                counts["ambiguous_process_sessions"] += 1

    process_ordinal = 0
    for session_id in sorted(starts):
        start_calls = starts[session_id]
        if len(start_calls) != 1:
            counts["ambiguous_process_sessions"] += 1
            continue
        process_ordinal += 1
        process_ref = f"process-{process_ordinal:04d}"
        start_pk = start_calls[0]
        connection.execute(
            "UPDATE calls SET process_ref = ?, process_event = 'start' WHERE id = ?",
            (process_ref, start_pk),
        )
        connection.execute(
            "UPDATE outputs SET process_ref = ? WHERE paired_call_id = ?",
            (process_ref, start_pk),
        )
        for follower_pk, kind in followers.get(session_id, []):
            connection.execute(
                "UPDATE calls SET process_ref = ?, process_event = ? WHERE id = ?",
                (process_ref, kind, follower_pk),
            )
            connection.execute(
                "UPDATE outputs SET process_ref = ? WHERE paired_call_id = ?",
                (process_ref, follower_pk),
            )
        counts["linked_process_sessions"] += 1

    # Classify with paired output included. A process is Claude-related if any
    # directly linked event is; all its continuation polls then inherit the lane.
    for call_pk, name, arguments_json in connection.execute(
        "SELECT id, tool_name, arguments_json FROM calls ORDER BY id"
    ):
        arguments = json.loads(arguments_json)
        outputs = [
            json.loads(row[0])
            for row in connection.execute(
                "SELECT output_json FROM outputs WHERE paired_call_id = ? ORDER BY id",
                (call_pk,),
            )
        ]
        combined = [name, arguments, *outputs]
        direct = is_claude_related(*combined)
        classification = classify_claude_candidate(*combined) if direct else None
        connection.execute(
            "UPDATE calls SET direct_claude = ?, classification = ? WHERE id = ?",
            (int(direct), classification, call_pk),
        )
        if direct:
            connection.execute(
                "UPDATE outputs SET direct_claude = 1 WHERE paired_call_id = ?",
                (call_pk,),
            )
    for process_ref, related in connection.execute(
        """
        SELECT process_ref, MAX(direct_claude)
        FROM calls
        WHERE process_ref IS NOT NULL
        GROUP BY process_ref
        """
    ):
        if not related:
            continue
        start_classification = connection.execute(
            """
            SELECT classification FROM calls
            WHERE process_ref = ? AND process_event = 'start'
            """,
            (process_ref,),
        ).fetchone()
        inherited = (
            start_classification[0]
            if start_classification is not None and start_classification[0]
            else "implementation-or-research"
        )
        connection.execute(
            """
            UPDATE calls SET direct_claude = 1,
                classification = COALESCE(classification, ?)
            WHERE process_ref = ?
            """,
            (inherited, process_ref),
        )
        connection.execute(
            "UPDATE outputs SET direct_claude = 1 WHERE process_ref = ?",
            (process_ref,),
        )
    connection.commit()
    return counts


def _second_projection_pass(
    store: Path,
    manifest: Mapping[str, object],
    contexts: Mapping[str, Mapping[str, object]],
    staging: Path,
) -> dict[str, int]:
    counts = {
        "message_records": 0,
        "token_usage_snapshots": 0,
        "turn_activity_records": 0,
    }
    with (
        _open_private_output(staging / "messages.jsonl") as messages,
        _open_private_output(staging / "token-usage.jsonl") as tokens,
        _open_private_output(staging / "turn-activity.jsonl") as turns,
    ):
        for item in manifest["files"]:  # type: ignore[index]
            identity = str(item["source_identity"])
            context = contexts[identity]
            for _raw, value, source in _iter_projection(store, item, context):
                payload = value.get("payload")
                if not isinstance(payload, dict):
                    continue
                source_type = value.get("source_type")
                event_type = payload.get("type")
                if source_type == "event_msg" and event_type in {
                    "user_message",
                    "agent_message",
                }:
                    record = {
                        "schema": f"{INDEX_SCHEMA}.message.v1",
                        "record_kind": str(event_type).replace("_", "-"),
                        "scope": "user-visible-event",
                        "timestamp": value.get("timestamp"),
                        "source": source,
                    }
                    for key in (
                        "message",
                        "phase",
                        "attachment_summary",
                        "memory_citation",
                    ):
                        if key in payload:
                            record[key] = payload[key]
                    _write_jsonl(messages, record)
                    counts["message_records"] += 1
                elif source_type == "response_item" and event_type == "agent_message":
                    content = payload.get("content")
                    if isinstance(content, list):
                        text_items = [
                            item.get("text")
                            for item in content
                            if isinstance(item, dict)
                            and item.get("type") == "input_text"
                            and isinstance(item.get("text"), str)
                        ]
                        _write_jsonl(
                            messages,
                            {
                                "schema": f"{INDEX_SCHEMA}.message.v1",
                                "record_kind": "agent-message",
                                "scope": "projected-agent-communication",
                                "timestamp": value.get("timestamp"),
                                "author": payload.get("author"),
                                "recipient": payload.get("recipient"),
                                "status": payload.get("status"),
                                "content": text_items,
                                "source": source,
                            },
                        )
                        counts["message_records"] += 1
                if source_type == "event_msg" and event_type == "token_count":
                    info = payload.get("info")
                    usage: dict[str, dict[str, int]] = {}
                    if isinstance(info, dict):
                        for usage_kind in ("last_token_usage", "total_token_usage"):
                            values = info.get(usage_kind)
                            if isinstance(values, dict):
                                selected = {
                                    key: item
                                    for key, item in values.items()
                                    if key in TOKEN_KEYS
                                    and isinstance(item, int)
                                    and not isinstance(item, bool)
                                    and item >= 0
                                }
                                if selected:
                                    usage[usage_kind] = selected
                    if usage:
                        _write_jsonl(
                            tokens,
                            {
                                "schema": f"{INDEX_SCHEMA}.token-usage.v1",
                                "classification": "token-counts-not-money",
                                "timestamp": value.get("timestamp"),
                                "usage": usage,
                                "source": source,
                            },
                        )
                        counts["token_usage_snapshots"] += 1
                if source_type == "event_msg" and event_type in {
                    "task_started",
                    "task_complete",
                    "turn_aborted",
                }:
                    activity = {
                        key: payload[key]
                        for key in (
                            "type",
                            "turn_id",
                            "started_at",
                            "completed_at",
                            "duration_ms",
                            "first_output_latency_ms",
                            "error",
                            "reason",
                        )
                        if key in payload
                    }
                    _write_jsonl(
                        turns,
                        {
                            "schema": f"{INDEX_SCHEMA}.turn-activity.v1",
                            "classification": "retained-turn-marker-not-total-work",
                            "timestamp": value.get("timestamp"),
                            "activity": activity,
                            "source": source,
                        },
                    )
                    counts["turn_activity_records"] += 1
    return counts


def _emit_call_indexes(
    connection: sqlite3.Connection, staging: Path
) -> dict[str, int]:
    counts = {
        "agent_assignment_calls": 0,
        "claude_call_records": 0,
        "claude_output_records": 0,
        "sdk_cost_values": 0,
        "process_session_records": 0,
        "process_poll_calls": 0,
    }
    with (
        _open_private_output(staging / "agent-assignments.jsonl") as assignments,
        _open_private_output(staging / "claude-ledger.jsonl") as claude,
        _open_private_output(staging / "sdk-costs.jsonl") as costs,
        _open_private_output(staging / "process-sessions.jsonl") as processes,
    ):
        for row in connection.execute(
            """
            SELECT id, thread_ref, call_id, tool_name, namespace, server, timestamp,
                   arguments_json, source_json, assignment_kind,
                   direct_claude, classification, paired_output_count,
                   process_ref, process_event
            FROM calls ORDER BY id
            """
        ):
            (
                call_pk,
                thread_ref,
                call_id,
                tool_name,
                namespace,
                server,
                timestamp,
                arguments_json,
                source_json,
                assignment_kind,
                claude_related,
                classification,
                paired_output_count,
                process_ref,
                process_event,
            ) = row
            call_ref = f"call-{call_pk:06d}"
            arguments = json.loads(arguments_json)
            source = json.loads(source_json)
            if assignment_kind:
                _write_jsonl(
                    assignments,
                    {
                        "schema": f"{INDEX_SCHEMA}.agent-assignment-call.v1",
                        "call_ref": call_ref,
                        "assignment_kind": assignment_kind,
                        "tool_name": tool_name,
                        "namespace": namespace,
                        "server": server,
                        "timestamp": timestamp,
                        "arguments": arguments,
                        "output_correlation": (
                            "unambiguous"
                            if paired_output_count
                            else "no-retained-output"
                        ),
                        "source": source,
                    },
                )
                counts["agent_assignment_calls"] += 1
            if not claude_related:
                continue
            attempt_status = "candidate-not-established-as-model-attempt"
            if process_event == "poll":
                attempt_status = "orchestration-poll-not-a-model-attempt"
                counts["process_poll_calls"] += 1
            _write_jsonl(
                claude,
                {
                    "schema": f"{INDEX_SCHEMA}.claude-ledger.v1",
                    "record_kind": "tool-call",
                    "call_ref": call_ref,
                    "candidate_classification": classification,
                    "model_attempt_status": attempt_status,
                    "process_ref": process_ref,
                    "process_event": process_event,
                    "tool_name": tool_name,
                    "namespace": namespace,
                    "server": server,
                    "timestamp": timestamp,
                    "arguments": arguments,
                    "paired_output_count": paired_output_count,
                    "source": source,
                },
            )
            counts["claude_call_records"] += 1

        for row in connection.execute(
            """
            SELECT outputs.id, outputs.thread_ref, outputs.call_id,
                   outputs.timestamp, outputs.output_json, outputs.source_json,
                   outputs.direct_claude, outputs.paired_call_id,
                   outputs.process_ref, calls.classification, calls.process_event
            FROM outputs
            LEFT JOIN calls ON calls.id = outputs.paired_call_id
            ORDER BY outputs.id
            """
        ):
            (
                output_pk,
                _thread_ref,
                _call_id,
                timestamp,
                output_json,
                source_json,
                claude_related,
                paired_call_pk,
                process_ref,
                classification,
                process_event,
            ) = row
            if not claude_related:
                continue
            output = json.loads(output_json)
            source = json.loads(source_json)
            output_ref = f"output-{output_pk:06d}"
            paired_call_ref = (
                f"call-{paired_call_pk:06d}" if paired_call_pk is not None else None
            )
            _write_jsonl(
                claude,
                {
                    "schema": f"{INDEX_SCHEMA}.claude-ledger.v1",
                    "record_kind": "tool-output",
                    "output_ref": output_ref,
                    "paired_call_ref": paired_call_ref,
                    "output_correlation": (
                        "unambiguous" if paired_call_ref else "unresolved"
                    ),
                    "candidate_classification": (
                        classification or classify_claude_candidate(output)
                    ),
                    "model_attempt_status": (
                        "orchestration-poll-output-not-a-model-attempt"
                        if process_event == "poll"
                        else "candidate-output-not-proof-of-model-attempt"
                    ),
                    "process_ref": process_ref,
                    "timestamp": timestamp,
                    "output": output,
                    "source": source,
                },
            )
            counts["claude_output_records"] += 1
            for ordinal, cost in enumerate(extract_sdk_costs(output), 1):
                _write_jsonl(
                    costs,
                    {
                        "schema": f"{INDEX_SCHEMA}.sdk-cost.v1",
                        "cost_ref": f"{output_ref}-cost-{ordinal:02d}",
                        "paired_call_ref": paired_call_ref,
                        "candidate_classification": (
                            classification or classify_claude_candidate(output)
                        ),
                        **cost,
                        "source": source,
                    },
                )
                counts["sdk_cost_values"] += 1

        for process_ref, start_call, continuations, polls, stdin_calls in connection.execute(
            """
            SELECT process_ref,
                   SUM(CASE WHEN process_event = 'start' THEN 1 ELSE 0 END),
                   SUM(CASE WHEN process_event IN ('poll', 'stdin') THEN 1 ELSE 0 END),
                   SUM(CASE WHEN process_event = 'poll' THEN 1 ELSE 0 END),
                   SUM(CASE WHEN process_event = 'stdin' THEN 1 ELSE 0 END)
            FROM calls
            WHERE process_ref IS NOT NULL AND direct_claude = 1
            GROUP BY process_ref ORDER BY process_ref
            """
        ):
            _write_jsonl(
                processes,
                {
                    "schema": f"{INDEX_SCHEMA}.process-session.v1",
                    "process_ref": process_ref,
                    "linkage": "unambiguous-retained-session-value",
                    "start_call_count": start_call,
                    "continuation_call_count": continuations,
                    "poll_call_count": polls,
                    "stdin_call_count": stdin_calls,
                    "session_identifier_published": False,
                    "polls_count_as_model_attempts": False,
                },
            )
            counts["process_session_records"] += 1
    return counts


def _output_binding(path: Path, records: int | None = None) -> dict[str, object]:
    hasher = hashlib.sha256()
    byte_count = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            hasher.update(chunk)
            byte_count += len(chunk)
    binding: dict[str, object] = {
        "name": path.name,
        "bytes": byte_count,
        "sha256": hasher.hexdigest(),
    }
    if records is not None:
        binding["records"] = records
    return binding


def _readme(counts: Mapping[str, int]) -> bytes:
    return f"""# Recovered delivery evidence index

Status: owner-only derived index; do not publish.

The complete evidence store passed offline verification before this index was
built. The index then selected the newest captured EVID-211 closure manifest and
read only its verified user-visible projection objects. It did not read raw Codex
rollouts, hidden reasoning, client credentials or another extraction archive.

## Contents

- `messages.jsonl`: {counts['message_records']:,} projected user and agent message
  records, each bound to its journal event, generation manifest, projection object
  and projected source line.
- `agent-assignments.jsonl`: {counts['agent_assignment_calls']:,} retained agent
  assignment or follow-up tool calls. These are source records, not evidence that
  the assigned work was accepted.
- `claude-ledger.jsonl`: {counts['claude_call_records']:,} Claude-related candidate
  calls and {counts['claude_output_records']:,} related outputs. A candidate is not
  automatically an actual model observation or provider request.
- `process-sessions.jsonl`: {counts['process_session_records']:,} unambiguous private
  links between asynchronous execution starts and later `write_stdin` calls. Polls
  are orchestration events and never count as model attempts.
- `sdk-costs.jsonl`: {counts['sdk_cost_values']:,} finite, non-negative USD
  cost-field candidates found in retained output. The filename and
  `sdk_cost_values` count remain for compatibility. Candidates may come from code
  or test examples; they do not prove SDK or provider usage and actual billed cost
  remains unknown.
- `token-usage.jsonl`: {counts['token_usage_snapshots']:,} retained token-count
  snapshots. Tokens are counts, not money.
- `turn-activity.jsonl`: {counts['turn_activity_records']:,} retained start,
  completion and abort markers.
- `manifest.json`: exact input and output bindings, aggregate counts and limits.

## Interpretation limits

The index is complete only for user-visible records admitted to the selected
projection generation. EVID-211 intentionally excludes hidden reasoning and some
unsafe or unsupported records. A message timestamp records an event, not necessarily
the start or end of work. A retained `duration_ms` belongs to that reported turn;
concurrent turns can overlap and their sum is not total elapsed time. Command wait
time, CI wait, human authorisation time, model execution and total project time are
different measures.

Tool-call correlation uses exact retained call identifiers within a projected
thread. Process linkage is emitted only when one execution start exposes one
session value; the raw session value is not repeated in the derived index. Missing
or ambiguous links remain unknown. The index does not claim that every Claude
candidate was run, reached a provider, succeeded or incurred a charge.
""".encode("utf-8")


def _write_private_bytes(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)


def _fsync_file(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def build_index(
    store: Path,
    output: Path,
    *,
    verify_function: Callable[[Path], Mapping[str, object]] = verify_store,
) -> dict[str, int]:
    """Verify one store and atomically create a new owner-only recovery index."""

    with private_umask():
        canonical_output, staging = _prepare_output(output, store)
        completed = False
        journal_descriptor: int | None = None
        database_connection: sqlite3.Connection | None = None
        try:
            try:
                verified = verify_function(store)
            except EvidenceVerificationError as error:
                raise RecoveryIndexError("private-store-verification-failed") from error
            if verified.get("verified") is not True:
                raise RecoveryIndexError("private-store-verification-failed")

            journal_path = store / "journal.jsonl"
            journal_descriptor, journal_metadata = _open_regular(journal_path)
            first_scan, manifest_event, _unused = _journal_pass(
                journal_descriptor, select_manifest=True
            )
            _verify_journal_snapshot(first_scan, verified)
            if manifest_event is None:
                raise RecoveryIndexError("verified-store-has-no-captured-generation")
            manifest_objects = manifest_event.get("objects")
            if not isinstance(manifest_objects, list) or len(manifest_objects) != 1:
                raise RecoveryIndexError("verified-manifest-binding-is-invalid")
            manifest_object = manifest_objects[0]
            if not isinstance(manifest_object, dict):
                raise RecoveryIndexError("verified-manifest-binding-is-invalid")
            manifest_digest = manifest_object.get("sha256")
            manifest_bytes = manifest_object.get("bytes")
            if not isinstance(manifest_digest, str) or not isinstance(manifest_bytes, int):
                raise RecoveryIndexError("verified-manifest-binding-is-invalid")
            manifest_raw = _read_bound_object(store, manifest_digest, manifest_bytes)
            manifest = _parse_manifest(manifest_raw)
            wanted = {
                str(item["source_identity"])
                for item in manifest["files"]
            }
            second_scan, _latest, projection_events = _journal_pass(
                journal_descriptor, wanted_projection_identities=wanted
            )
            if second_scan != first_scan or set(projection_events) != wanted:
                raise RecoveryIndexError("journal-changed-during-indexing")

            manifest_sequence = manifest_event.get("sequence")
            manifest_event_sha = manifest_event.get("event_sha256")
            contexts: dict[str, dict[str, object]] = {}
            projection_bindings: list[dict[str, object]] = []
            for ordinal, item in enumerate(manifest["files"], 1):
                identity = str(item["source_identity"])
                event = projection_events[identity]
                event_objects = event.get("objects")
                if (
                    not isinstance(event_objects, list)
                    or len(event_objects) != 1
                    or not isinstance(event_objects[0], dict)
                    or event_objects[0].get("sha256") != item.get("object_sha256")
                ):
                    raise RecoveryIndexError("projection-event-binding-differs")
                thread_ref = f"thread-{ordinal:04d}"
                context = {
                    "thread_ref": thread_ref,
                    "manifest_event_sequence": manifest_sequence,
                    "manifest_event_sha256": manifest_event_sha,
                    "manifest_object_sha256": manifest_digest,
                    "projection_event_sequence": event.get("sequence"),
                    "projection_event_sha256": event.get("event_sha256"),
                    "projection_object_sha256": item.get("object_sha256"),
                    "projection_uncompressed_sha256": item.get(
                        "uncompressed_sha256"
                    ),
                }
                contexts[identity] = context
                projection_bindings.append(
                    {
                        **context,
                        "source_identity_sha256": item.get("source_identity_sha256"),
                        "source_path_sha256": item.get("source_path_sha256"),
                        "parent_thread_ref": None,
                        "object_bytes": item.get("object_bytes"),
                        "uncompressed_bytes": item.get("uncompressed_bytes"),
                        "retained_records": item.get("retained_records"),
                        "skipped_record_types": item.get("skipped_record_types"),
                    }
                )
            thread_refs = {
                str(item["thread_id"]): contexts[str(item["source_identity"])][
                    "thread_ref"
                ]
                for item in manifest["files"]
            }
            for item, binding in zip(manifest["files"], projection_bindings, strict=True):
                binding["parent_thread_ref"] = thread_refs.get(item.get("parent_thread_id"))

            database_path = staging / ".working.sqlite3"
            database_connection = _database(database_path)
            counts = _first_projection_pass(
                store, manifest, contexts, database_connection
            )
            counts.update(_correlate_calls_and_outputs(database_connection))
            counts.update(
                _second_projection_pass(store, manifest, contexts, staging)
            )
            counts.update(_emit_call_indexes(database_connection, staging))
            counts["selected_threads"] = len(manifest["files"])

            database_connection.close()
            database_connection = None
            database_path.unlink()
            readme_raw = _readme(counts)
            _write_private_bytes(staging / "README.md", readme_raw)

            output_record_counts = {
                "messages.jsonl": counts["message_records"],
                "agent-assignments.jsonl": counts["agent_assignment_calls"],
                "claude-ledger.jsonl": (
                    counts["claude_call_records"] + counts["claude_output_records"]
                ),
                "process-sessions.jsonl": counts["process_session_records"],
                "sdk-costs.jsonl": counts["sdk_cost_values"],
                "token-usage.jsonl": counts["token_usage_snapshots"],
                "turn-activity.jsonl": counts["turn_activity_records"],
            }
            output_bindings = [
                _output_binding(
                    staging / name,
                    output_record_counts.get(name),
                )
                for name in OUTPUT_FILES
            ]
            final_scan, _latest, _events = _journal_pass(journal_descriptor)
            if final_scan != first_scan:
                raise RecoveryIndexError("journal-changed-during-indexing")
            final_journal_metadata = os.fstat(journal_descriptor)
            if (
                journal_metadata.st_dev,
                journal_metadata.st_ino,
                journal_metadata.st_size,
                journal_metadata.st_mtime_ns,
            ) != (
                final_journal_metadata.st_dev,
                final_journal_metadata.st_ino,
                final_journal_metadata.st_size,
                final_journal_metadata.st_mtime_ns,
            ):
                raise RecoveryIndexError("journal-changed-during-indexing")

            manifest_document = {
                "schema": INDEX_SCHEMA,
                "status": "complete-private-derived-index",
                "created_at_utc": datetime.now(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
                "boundaries": {
                    "owner_only": True,
                    "publishable": False,
                    "raw_rollouts_read": False,
                    "hidden_reasoning_read": False,
                    "client_credentials_read": False,
                    "verified_store_before_indexing": True,
                    "selected_files_have_projection_objects": True,
                    "exhaustive_transcript_attested": False,
                    "actual_model_attempts_attested": False,
                    "provider_usage_proven": False,
                    "actual_billed_cost": "unknown",
                    "token_counts_are_money": False,
                    "polls_count_as_model_attempts": False,
                },
                "input_bindings": {
                    "journal": {
                        "events": first_scan["events"],
                        "bytes": first_scan["bytes"],
                        "sha256": first_scan["sha256"],
                        "head_event_sha256": first_scan["head_event_sha256"],
                    },
                    "generation_manifest": {
                        "event_sequence": manifest_sequence,
                        "event_sha256": manifest_event_sha,
                        "object_sha256": manifest_digest,
                        "object_bytes": manifest_bytes,
                        "collection_generation_sha256": manifest.get(
                            "collection_generation_sha256"
                        ),
                        "collection_window": manifest.get("collection_window"),
                        "selected_file_count": manifest.get("selected_file_count"),
                    },
                    "projections": projection_bindings,
                },
                "counts": dict(sorted(counts.items())),
                "outputs": output_bindings,
                "limitations": [
                    "The index covers admitted user-visible projection records, "
                    "not raw transcripts.",
                    "A Claude-related candidate is not automatically an actual "
                    "model or provider attempt.",
                    "Reported cost-field candidates may occur in code or test "
                    "examples; they do not prove SDK or provider usage, and "
                    "actual billed cost remains unknown.",
                    "Token usage is recorded as counts and is not converted into money.",
                    "Retained durations are event-local and must not be summed "
                    "as total project time.",
                    "Ambiguous call, output or process-session relationships remain unlinked.",
                ],
            }
            _write_private_bytes(
                staging / "manifest.json",
                canonical_json(manifest_document, pretty=True),
            )
            expected_files = {*OUTPUT_FILES, "manifest.json"}
            observed_files = {path.name for path in staging.iterdir() if path.is_file()}
            if observed_files != expected_files or any(
                not path.is_file() or path.is_symlink() for path in staging.iterdir()
            ):
                raise RecoveryIndexError("private-output-shape-is-invalid")
            for path in staging.iterdir():
                os.chmod(path, 0o600)
                _fsync_file(path)
            _fsync_directory(staging)
            if os.path.lexists(canonical_output):
                raise RecoveryIndexError("output-already-exists")
            os.rename(staging, canonical_output)
            _fsync_directory(canonical_output.parent)
            completed = True
            return counts
        finally:
            if database_connection is not None:
                database_connection.close()
            if journal_descriptor is not None:
                os.close(journal_descriptor)
            if not completed and staging.exists():
                shutil.rmtree(staging)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--store", type=Path, required=True)
    value.add_argument("--output", type=Path, required=True)
    return value


SAFE_SUMMARY_KEYS = (
    "selected_threads",
    "projected_records",
    "message_records",
    "agent_assignment_calls",
    "claude_call_records",
    "claude_output_records",
    "linked_process_sessions",
    "process_poll_calls",
    "sdk_cost_values",
    "token_usage_snapshots",
    "turn_activity_records",
)


def main(
    argv: Sequence[str] | None = None,
    *,
    verify_function: Callable[[Path], Mapping[str, object]] = verify_store,
) -> int:
    arguments = parser().parse_args(argv)
    try:
        counts = build_index(
            arguments.store,
            arguments.output,
            verify_function=verify_function,
        )
    except RecoveryIndexError as error:
        print(
            json.dumps({"indexed": False, "error": error.code}, sort_keys=True),
            file=sys.stderr,
        )
        return 1
    except Exception:
        # Never reflect a retained value, private path, digest or session identifier
        # through an unexpected exception at the command boundary.
        print(
            json.dumps({"indexed": False, "error": "private-indexing-failed"}, sort_keys=True),
            file=sys.stderr,
        )
        return 1
    print(
        json.dumps(
            {
                "indexed": True,
                **{key: int(counts.get(key, 0)) for key in SAFE_SUMMARY_KEYS},
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
