#!/usr/bin/env python3
"""Verify a private delivery-evidence store without network access."""

from __future__ import annotations

import argparse
import concurrent.futures
import fcntl
import gzip
import hashlib
import io
import json
import math
import multiprocessing
import os
import queue
import re
import stat
import sys
import time
import unicodedata
import zipfile
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence
from urllib.parse import urlsplit

from capture_delivery_evidence import (
    BOUNDARIES,
    CODEX_GENERATION_SCHEMA,
    CODEX_PROJECTION_SCHEMA,
    INTERMEDIATE_CODEX_PROJECTION_SCHEMA,
    LEGACY_CODEX_PROJECTION_SCHEMA,
    EVENT_SCHEMA,
    FIXED_LENGTH_REDACTION_PATTERNS,
    GITHUB_MAX_RETENTION_DAYS,
    LEDGER_SCHEMA,
    MAX_CODEX_LINE_BYTES,
    MAX_METADATA_BYTES,
    MAX_OBJECT_BYTES,
    MAX_STORE_LEDGER_BYTES,
    MAX_STORE_JOURNAL_BYTES,
    PRIVATE_KEY_CONTAINER_SUFFIXES,
    REPOSITORY_PATTERN,
    SECRET_PATTERNS,
    SHA256_PATTERN,
    UNREDACTABLE_SECRET_PATTERN,
    STORE_SCHEMA,
    TRIGGER_PATTERN,
    EvidenceCaptureError,
    SecretDetectedError,
    _archive_format_from_magic,
    _classify_codex_oversized_text_key_fragments,
    _codex_value_exceeds_depth,
    _embedded_archive_format,
    _read_private_file_bounded,
    _redact_codex_projection_value,
    build_expiry_ledger,
    canonical_json,
    format_time,
    parse_json,
    parse_time,
    private_umask,
    read_journal,
    source_identity_sha256,
    utc_now,
    _require_enforced_volume_ownership,
    _scan_secret_binary_stream,
    _scan_zip_archive,
    _validate_jpeg,
    _validate_png,
    _sanitise_codex_local_paths_in_text,
    _unindexed_extended_attributes,
    _has_extended_acl,
)


class EvidenceVerificationError(EvidenceCaptureError):
    """Raised when an owner-only evidence store fails closed verification."""


class _CodexProjectionSchemaMismatch(EvidenceVerificationError):
    """Internal signal for a valid projection using an obsolete schema."""


_FIXED_LENGTH_REDACTION_MANDATORY_MARKERS: dict[str, tuple[bytes, ...]] = {
    "github-stateless-installation-token": (b"ghs_",),
    "github-token": (b"ghp_", b"gho_", b"ghu_", b"ghs_", b"ghr_"),
    "github-fine-grained-token": (b"github_pat_",),
    "openai-token": (b"sk-",),
    "anthropic-token": (b"sk-ant-",),
    "npm-granular-token": (b"npm_",),
    "aws-access-key": (b"akia",),
    "aws-temporary-access-key": (b"asia",),
    "google-api-key": (b"aiza",),
    "google-oauth-client-secret": (b"gocspx-",),
    "gitlab-token": (b"glpat-",),
    "pypi-token": (b"pypi-ageichlwas5vcmc",),
    "slack-token": (b"xox",),
    "slack-app-token": (b"xapp-1-",),
    "hugging-face-token": (b"hf_",),
    "stripe-live-secret": (b"_live_",),
    "sendgrid-api-key": (b"sg.",),
    "docker-access-token": (b"dckr_pat_",),
    "slack-webhook": (b"https://hooks.slack.com/services/",),
    "bearer-token": (b"authorization",),
    "basic-authorization": (b"authorization",),
    "session-cookie": (b"cookie",),
    "oauth-callback-code": (
        b"code=",
        b"access_" + b"token=",
        b"refresh_token=",
        b"id_token=",
    ),
    "database-credential-url": (b"database", b"connection"),
    "userinfo-credential-url": (b"://",),
    "assigned-secret": (b"token", b"secret", b"key", b"password"),
    "assigned-secret-unquoted": (b"token", b"secret", b"key", b"password"),
    "signed-url": (b"sig",),
}
CODEX_VERIFICATION_PROGRESS_INTERVAL = 25
STORE_INTEGRITY_PROGRESS_OBJECT_INTERVAL = 250
CODEX_VERIFICATION_PROGRESS_BYTES = 64 * 1024 * 1024
CODEX_VERIFICATION_PROGRESS_SECONDS = 30.0
MIN_CODEX_VERIFICATION_WORKERS = 1
MAX_CODEX_VERIFICATION_WORKERS = 4


_CODEX_WORKER_PROGRESS_QUEUE: Any = None


def _initialise_codex_projection_worker(progress_queue: Any) -> None:
    """Install the bounded parent progress channel in a projection worker."""

    global _CODEX_WORKER_PROGRESS_QUEUE
    _CODEX_WORKER_PROGRESS_QUEUE = progress_queue


def _verify_codex_projection_worker(
    path: Path,
    manifest_item: Mapping[str, Any],
    source_event: Mapping[str, Any],
    allowed_session_thread_ids: set[str] | frozenset[str],
    session_lineage_metadata: Mapping[str, tuple[str, str | None]],
    progress_byte_interval: int,
) -> None:
    """Fully verify one projection in an isolated bounded-memory process."""

    pending_bytes = 0
    last_progress_at = time.monotonic()

    def report_bytes(count: int) -> None:
        nonlocal pending_bytes, last_progress_at
        pending_bytes += count
        current = time.monotonic()
        if (
            pending_bytes >= progress_byte_interval
            or current - last_progress_at >= CODEX_VERIFICATION_PROGRESS_SECONDS
        ):
            _CODEX_WORKER_PROGRESS_QUEUE.put(pending_bytes)
            pending_bytes = 0
            last_progress_at = current

    _verify_codex_projection(
        path,
        manifest_item,
        source_event,
        allowed_session_thread_ids=allowed_session_thread_ids,
        session_lineage_metadata=session_lineage_metadata,
        progress_bytes_function=report_bytes,
    )
    if pending_bytes:
        _CODEX_WORKER_PROGRESS_QUEUE.put(pending_bytes)


def _verify_fixed_length_projection_redactions(raw: bytes) -> None:
    """Reject unredacted credentials without rescanning safe lines 28 times."""

    lowered = raw.lower()
    for category, pattern in FIXED_LENGTH_REDACTION_PATTERNS:
        markers = _FIXED_LENGTH_REDACTION_MANDATORY_MARKERS.get(category)
        if markers is not None and not any(marker in lowered for marker in markers):
            continue
        # A newly configured category without reviewed mandatory markers takes the
        # original full-scan path so a stale optimisation can never skip it.
        for match in pattern.finditer(raw):
            captured = match.group(1)
            redacted = captured and all(byte == ord("X") for byte in captured)
            _expect(
                redacted,
                f"Codex projection contains unredacted secret category {category}",
            )


SOURCE_KEYS = {
    "kind",
    "identity",
    "identity_sha256",
    "immutability",
    "label",
    "occurred_at_utc",
    "expires_at_utc",
    "expiry_basis",
    "commit_sha",
    "tree_sha",
    "redaction_mode",
    "snapshot_method",
    "source_stat_before",
    "source_stat_after",
    "source_changed_after_snapshot",
    "collection_generation_sha256",
    "collection_window",
    "redaction_categories",
    "redaction_count",
}
OBJECT_KEYS = {
    "role",
    "sha256",
    "bytes",
    "media_type",
    "opaque",
    "secret_scan",
    "secret_scan_performed",
    "sensitivity",
    "public_projection_eligible",
}
DISPOSITION_KEYS = {"status", "reason"}
ALLOWED_TOP_LEVEL_FILES = {
    "format.json",
    "journal.jsonl",
    "expiry-ledger.json",
    ".lock",
    ".metadata_never_index",
}
ALLOWED_TOP_LEVEL_DIRECTORIES = {"objects", ".incoming"}
SOURCE_STAT_KEYS = {
    "device",
    "inode",
    "mode",
    "links",
    "owner_uid",
    "bytes",
    "mtime_ns",
    "ctime_ns",
}
CODEX_MANIFEST_FILE_KEYS = {
    "thread_id",
    "session_id",
    "parent_thread_id",
    "source_path_sha256",
    "source_identity",
    "source_identity_sha256",
    "raw_source_sha256",
    "disposition",
    "reason",
    "object_sha256",
    "object_bytes",
    "uncompressed_sha256",
    "uncompressed_bytes",
    "retained_records",
    "skipped_record_types",
    "redaction_categories",
    "redaction_count",
    "source_stat_final_observation",
    "source_changed_by_final_observation",
}
CODEX_MANIFEST_KEYS = {
    "schema",
    "thread_id",
    "selection_rule",
    "files",
    "boundaries",
    "collection_generation_sha256",
    "collection_window",
    "selected_file_count",
    "aggregate_skipped_record_types",
}
CODEX_EXCLUDED_KEYS = {
    "analysis",
    "base_instructions",
    "chain_of_thought",
    "compacted",
    "developer_instructions",
    "developer_message",
    "dynamic_tools",
    "encrypted_content",
    "instructions",
    "reasoning",
    "system_message",
    "thought",
    "turn_context",
    "world_state",
}
CODEX_EXCLUDED_KEY_NORMALISATIONS = {
    re.sub(r"[^a-z0-9]", "", key.lower()) for key in CODEX_EXCLUDED_KEYS
}
CODEX_JSON_KEY_FRAGMENT_PATTERN = re.compile(
    r'("(?:\\(?:["\\/bfnrt]|u[0-9A-Fa-f]{4})|[^"\\]){1,512}")\s*:'
)
CODEX_SESSION_PAYLOAD_KEYS = {
    "id",
    "session_id",
    "parent_thread_id",
    "forked_from_id",
    "forked_from_id_sha256",
    "agent_path",
    "agent_nickname",
    "agent_role",
    "timestamp",
    "cli_version",
    "originator",
    "thread_source",
    "model_provider",
    "agent_parent_path",
    "git",
}
LEGACY_CODEX_FORK_ID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)
CODEX_RESPONSE_CALL_TYPES = {"custom_tool_call", "function_call"}
CODEX_RESPONSE_OUTPUT_TYPES = {"custom_tool_call_output", "function_call_output"}
CODEX_RESPONSE_CALL_KEYS = {
    "type",
    "name",
    "namespace",
    "server",
    "call_id",
    "status",
    "input",
    "arguments",
}
CODEX_RESPONSE_OUTPUT_KEYS = {"type", "call_id", "status", "output"}
GITHUB_SOURCE_KINDS = {
    "github-actions-artifact",
    "github-actions-artifact-metadata",
    "github-actions-retention-policy-snapshot",
    "github-actions-run-jobs",
    "github-actions-run-logs",
    "github-actions-run-metadata",
    "github-discussion-snapshot",
    "github-repository-identity-snapshot",
}
LOCAL_SOURCE_KINDS = {"local-file", "local-apfs-clone", "local-redacted-jsonl"}
CODEX_SOURCE_KINDS = {
    "codex-user-visible-projection",
    "codex-thread-closure-generation-manifest",
}
SOURCE_KINDS = LOCAL_SOURCE_KINDS | GITHUB_SOURCE_KINDS | CODEX_SOURCE_KINDS
LOCAL_SECRET_CATEGORIES = {category for category, _ in SECRET_PATTERNS} | {
    "private-key-container"
}
CODEX_EVENT_PAYLOAD_KEYS = {
    "user_message": {"type", "message", "attachment_summary"},
    "agent_message": {"type", "message", "phase", "memory_citation"},
    "task_started": {
        "type",
        "turn_id",
        "started_at",
        "model_context_window",
        "collaboration_mode_kind",
    },
    "task_complete": {
        "type",
        "turn_id",
        "started_at",
        "completed_at",
        "duration_ms",
        "first_output_latency_ms",
        "time_to_first_token_ms",
        "error",
    },
    "sub_agent_activity": {
        "type",
        "agent_path",
        "agent_thread_id",
        "event_id",
        "kind",
        "occurred_at_ms",
    },
    "item_completed": {
        "type",
        "thread_id",
        "turn_id",
        "started_at_ms",
        "completed_at_ms",
        "item",
    },
    "mcp_tool_call_end": {
        "type",
        "call_id",
        "duration",
        "read_only_hint",
        "plugin_id",
        "action_name",
        "app_name",
        "connector_id",
        "link_id",
        "invocation",
        "result",
    },
    "patch_apply_end": {
        "type",
        "call_id",
        "turn_id",
        "status",
        "success",
        "stdout",
        "stderr",
        "changes_omitted_count",
    },
    "web_search_end": {"type", "call_id", "action", "query", "results"},
    "token_count": {"type", "info", "rate_limits"},
    "turn_aborted": {
        "type",
        "turn_id",
        "started_at",
        "completed_at",
        "duration_ms",
        "reason",
    },
}


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceVerificationError(message)


def _is_non_negative_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _is_positive_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _verify_count_mapping(value: object, label: str) -> None:
    _expect(
        isinstance(value, dict)
        and all(
            isinstance(key, str) and key and _is_positive_int(count)
            for key, count in value.items()
        ),
        f"{label} is invalid",
    )


def _is_number(value: object) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return 0 <= value <= 2**63 - 1
    return (
        isinstance(value, float)
        and math.isfinite(value)
        and 0 <= value <= 2**63 - 1
    )


def _is_legacy_redacted_number(value: object) -> bool:
    """Recognise the exact fixed-length mask emitted by the initial capture."""

    return isinstance(value, str) and 1 <= len(value) <= 64 and set(value) == {"X"}


def _is_text_omission_descriptor(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    keys = set(value)
    return keys == {
        "text_omitted",
        "reason",
        "original_utf8_bytes",
        "original_sha256",
    } and (
        value["text_omitted"] is True
        and value["reason"]
        in {
            "hidden-structured-field",
            "invalid-structured-text",
            "maximum-depth",
            "nested-sensitive-structured-text",
            "oversized-structured-text",
            "sensitive-structured-field",
        }
        and _is_non_negative_int(value["original_utf8_bytes"])
        and isinstance(value["original_sha256"], str)
        and bool(SHA256_PATTERN.fullmatch(value["original_sha256"]))
    )


def _is_bounded_text(value: object) -> bool:
    if isinstance(value, str):
        return True
    if not isinstance(value, dict):
        return False
    keys = set(value)
    if keys == {"text", "truncated", "original_utf8_bytes", "original_sha256"}:
        return (
            (
                isinstance(value["text"], str)
                or _is_text_omission_descriptor(value["text"])
            )
            and value["truncated"] is True
            and _is_non_negative_int(value["original_utf8_bytes"])
            and isinstance(value["original_sha256"], str)
            and bool(SHA256_PATTERN.fullmatch(value["original_sha256"]))
        )
    return _is_text_omission_descriptor(value)


def _is_bounded_json(value: object) -> bool:
    stack: list[tuple[object, int]] = [(value, 0)]
    visited = 0
    while stack:
        item, depth = stack.pop()
        visited += 1
        if visited > 100_000 or depth > 10:
            return False
        if item is None or isinstance(item, (str, bool)) or _is_number(item):
            continue
        if isinstance(item, list):
            if len(item) > 65:
                return False
            stack.extend((child, depth + 1) for child in item)
            continue
        if isinstance(item, dict):
            if len(item) > 65 or not all(isinstance(key, str) for key in item):
                return False
            stack.extend((child, depth + 1) for child in item.values())
            continue
        return False
    return True


def _is_safe_http_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    return (
        parsed.scheme.lower() in {"http", "https"}
        and parsed.hostname is not None
        and parsed.username is None
        and parsed.password is None
        and not parsed.query
        and not parsed.fragment
    )


def _is_codex_path_value(value: object) -> bool:
    return _is_bounded_text(value) or (
        isinstance(value, list)
        and len(value) <= 64
        and all(_is_bounded_text(item) for item in value)
    )


def _expect_bounded_text_fields(
    value: Mapping[str, Any], fields: Sequence[str], label: str
) -> None:
    for field in fields:
        if field in value:
            _expect(_is_bounded_text(value[field]), f"{label} {field} is invalid")


def _verify_attachment_summary(value: object) -> None:
    _expect(isinstance(value, dict), "Codex attachment summary is not an object")
    if not isinstance(value, dict):
        return
    _expect(
        set(value)
        <= {
            "images_summary",
            "local_images",
            "audio",
            "local_audio",
            "text_elements",
        },
        "Codex attachment summary is not closed",
    )
    for summary in value.values():
        _expect(isinstance(summary, dict), "Codex attachment class is not an object")
        if not isinstance(summary, dict):
            continue
        _expect(
            set(summary) <= {"count", "items", "summarised_items"}
            and _is_non_negative_int(summary.get("count")),
            "Codex attachment class is invalid",
        )
        if "summarised_items" in summary:
            _expect(
                _is_non_negative_int(summary["summarised_items"]),
                "Codex attachment summary count is invalid",
            )
        if "items" in summary:
            items = summary["items"]
            _expect(isinstance(items, list) and len(items) <= 64, "Codex attachments are invalid")
            if not isinstance(items, list):
                continue
            for item in items:
                _expect(
                    isinstance(item, dict) and set(item) <= {"type", "bytes", "sha256"},
                    "Codex attachment descriptor is not closed",
                )
                if not isinstance(item, dict):
                    continue
                if "type" in item:
                    _expect(_is_bounded_text(item["type"]), "Codex attachment type is invalid")
                if "bytes" in item:
                    _expect(_is_non_negative_int(item["bytes"]), "Codex attachment size is invalid")
                if "sha256" in item:
                    _expect(
                        isinstance(item["sha256"], str)
                        and bool(SHA256_PATTERN.fullmatch(item["sha256"])),
                        "Codex attachment digest is invalid",
                    )


def _verify_rate_limit_projection(value: object, *, depth: int = 0) -> None:
    _expect(isinstance(value, dict) and depth < 4, "Codex rate-limit projection is invalid")
    if not isinstance(value, dict):
        return
    containers = {"credits", "primary", "secondary"}
    scalars = {
        "balance",
        "has_credits",
        "plan",
        "plan_type",
        "remaining_percent",
        "reset_after_seconds",
        "reset_at",
        "resets_at",
        "unlimited",
        "used_percent",
        "window_minutes",
    }
    _expect(set(value) <= containers | scalars, "Codex rate-limit projection is not closed")
    for key, item in value.items():
        if key in containers:
            if key == "credits" and isinstance(item, (bool, int, float)):
                continue
            _verify_rate_limit_projection(item, depth=depth + 1)
        else:
            _expect(
                isinstance(item, (str, bool, int, float)),
                "Codex rate-limit value is invalid",
            )


def _verify_modes_and_shape(root: Path) -> None:
    _expect(root.is_absolute(), "private store path must be absolute")
    _require_enforced_volume_ownership(root)
    root_metadata = root.lstat()
    _expect(not root.is_symlink() and stat.S_ISDIR(root_metadata.st_mode), "store is not a directory")
    _expect(stat.S_IMODE(root_metadata.st_mode) == 0o700, "store mode is not 0700")
    _expect(root_metadata.st_uid == os.getuid(), "store is not owned by the current user")
    _expect(not _unindexed_extended_attributes(root), "store has unindexed extended attributes")
    _expect(not _has_extended_acl(root), "store has an unindexed extended ACL")
    for current, directory_names, file_names in os.walk(root, followlinks=False):
        current_path = Path(current)
        metadata = current_path.lstat()
        _expect(not current_path.is_symlink(), "store contains a symbolic-link directory")
        _expect(stat.S_ISDIR(metadata.st_mode), "store contains a special directory")
        _expect(stat.S_IMODE(metadata.st_mode) == 0o700, "store directory mode is not 0700")
        _expect(metadata.st_uid == os.getuid(), "store directory has an unexpected owner")
        _expect(
            not _unindexed_extended_attributes(current_path),
            "store directory has unindexed extended attributes",
        )
        _expect(
            not _has_extended_acl(current_path),
            "store directory has an unindexed extended ACL",
        )
        for name in directory_names:
            candidate = current_path / name
            item = candidate.lstat()
            _expect(not candidate.is_symlink(), "store contains a symbolic-link directory")
            _expect(stat.S_ISDIR(item.st_mode), "store contains a special directory entry")
            _expect(item.st_uid == os.getuid(), "store directory has an unexpected owner")
            _expect(
                not _unindexed_extended_attributes(candidate),
                "store directory has unindexed extended attributes",
            )
            _expect(
                not _has_extended_acl(candidate),
                "store directory has an unindexed extended ACL",
            )
        for name in file_names:
            candidate = current_path / name
            item = candidate.lstat()
            _expect(not candidate.is_symlink(), "store contains a symbolic-link file")
            _expect(stat.S_ISREG(item.st_mode), "store contains a special file")
            _expect(item.st_nlink == 1, "store contains a hard-linked file")
            _expect(stat.S_IMODE(item.st_mode) == 0o600, "store file mode is not 0600")
            _expect(item.st_uid == os.getuid(), "store file has an unexpected owner")
            _expect(
                not _unindexed_extended_attributes(candidate),
                "store file has unindexed extended attributes",
            )
            _expect(
                not _has_extended_acl(candidate),
                "store file has an unindexed extended ACL",
            )


def _verify_topology(root: Path) -> None:
    top_level = list(root.iterdir())
    top_names = {item.name for item in top_level if item.is_file()}
    _expect(top_names == ALLOWED_TOP_LEVEL_FILES, "store contains an unexpected top-level file")
    top_directories = {item.name for item in top_level if item.is_dir()}
    _expect(
        top_directories == ALLOWED_TOP_LEVEL_DIRECTORIES,
        "store contains an unexpected top-level directory",
    )
    _expect(
        {item.name for item in (root / "objects").iterdir()} == {"sha256"},
        "objects directory topology is invalid",
    )


def _verify_format(root: Path) -> None:
    raw = _read_private_file_bounded(
        root / "format.json",
        "format marker",
        MAX_METADATA_BYTES,
    )
    value = parse_json(raw, "format marker")
    expected = {"schema": STORE_SCHEMA, "boundaries": BOUNDARIES}
    _expect(value == expected, "format marker is invalid")
    _expect(raw == canonical_json(expected, pretty=True), "format marker is not canonical")


def _journal_label_redaction_count(source: Mapping[str, Any]) -> int:
    markers = re.findall(
        r"\[redacted-([a-z0-9-]+)-sha256:([0-9a-f]{64})\]",
        source["label"],
    )
    _expect(
        all(category in LOCAL_SECRET_CATEGORIES for category, _ in markers),
        "source label has an unknown redaction category",
    )
    expected_categories = sorted(
        {f"journal-label:{category}" for category, _ in markers}
    )
    observed_categories = sorted(
        category
        for category in source["redaction_categories"]
        if category.startswith("journal-label:")
    )
    _expect(
        observed_categories == expected_categories,
        "source label redaction metadata differs",
    )
    _expect(
        source["redaction_count"] >= len(markers),
        "source label redaction count differs",
    )
    return len(markers)


def _verify_source(source: Mapping[str, Any]) -> None:
    _expect(set(source) == SOURCE_KEYS, "source has unknown or missing fields")
    _expect(
        isinstance(source["kind"], str) and source["kind"] in SOURCE_KINDS,
        "source kind is outside the closed capture contract",
    )
    _expect(
        isinstance(source["label"], str)
        and 0 < len(source["label"].encode("utf-8")) <= 4096
        and _sanitise_codex_local_paths_in_text(source["label"])[1] == 0,
        "source label is invalid",
    )
    _expect(isinstance(source["redaction_mode"], str), "source redaction mode is invalid")
    _expect(isinstance(source["identity"], str) and source["identity"], "source identity is empty")
    _expect(
        source["identity_sha256"] == source_identity_sha256(source["identity"]),
        "source identity digest does not match",
    )
    _expect(source["immutability"] == "strict-immutable", "source is not immutable")
    _expect(
        source["snapshot_method"]
        in {
            "stable-byte-copy",
            "apfs-clonefile",
            "github-api-download",
            "streamed-user-visible-projection",
            "derived-generation-manifest",
        },
        "source snapshot method is invalid",
    )
    _expect(
        source["expiry_basis"] in {"provider-observed", "policy-snapshot-derived", "unknown"},
        "source expiry basis is invalid",
    )
    for key in ("occurred_at_utc", "expires_at_utc"):
        if source[key] is not None:
            parsed = parse_time(source[key], key)
            _expect(parsed.utcoffset().total_seconds() == 0, f"{key} is not UTC")
    for key in ("commit_sha", "tree_sha"):
        if source[key] is not None:
            _expect(bool(re.fullmatch(r"[0-9a-f]{40}", source[key])), f"{key} is invalid")
    for key in ("source_stat_before", "source_stat_after"):
        if source[key] is not None:
            _expect(
                isinstance(source[key], dict) and set(source[key]) == SOURCE_STAT_KEYS,
                f"{key} is invalid",
            )
            _expect(
                all(isinstance(item, int) and not isinstance(item, bool) for item in source[key].values()),
                f"{key} is invalid",
            )
    if source["snapshot_method"] in {"github-api-download", "derived-generation-manifest"}:
        _expect(source["source_stat_before"] is None, "GitHub source has local stat evidence")
        _expect(source["source_stat_after"] is None, "GitHub source has local stat evidence")
        _expect(source["source_changed_after_snapshot"] is None, "GitHub source has local mutation claim")
    else:
        _expect(source["source_stat_before"] is not None, "local source lacks pre-snapshot stat")
        _expect(source["source_stat_after"] is not None, "local source lacks post-snapshot stat")
        _expect(
            isinstance(source["source_changed_after_snapshot"], bool),
            "local source mutation marker is invalid",
        )
        signature_keys = (
            "device",
            "inode",
            "mode",
            "links",
            "owner_uid",
            "bytes",
            "mtime_ns",
            "ctime_ns",
        )
        changed = any(
            source["source_stat_before"][key] != source["source_stat_after"][key]
            for key in signature_keys
        )
        _expect(
            source["source_changed_after_snapshot"] is changed,
            "local source mutation marker differs from its stats",
        )
    _expect(
        isinstance(source["redaction_categories"], list)
        and all(isinstance(item, str) and item for item in source["redaction_categories"]),
        "redaction categories are invalid",
    )
    _expect(
        source["redaction_categories"] == sorted(set(source["redaction_categories"])),
        "redaction categories are invalid",
    )
    _expect(
        _is_non_negative_int(source["redaction_count"]),
        "redaction count is invalid",
    )
    _journal_label_redaction_count(source)
    if source["collection_generation_sha256"] is not None:
        _expect(
            bool(SHA256_PATTERN.fullmatch(source["collection_generation_sha256"])),
            "collection generation digest is invalid",
        )
    if source["collection_window"] is not None:
        window = source["collection_window"]
        _expect(
            isinstance(window, dict)
            and set(window) == {"start_utc", "end_utc", "selected_files", "selection_rule"},
            "collection window is invalid",
        )
        _expect(
            window["selection_rule"]
            == "target-and-transitive-descendants-by-parent-thread-id",
            "collection selection rule is invalid",
        )
        _expect(
            _is_positive_int(window["selected_files"]),
            "collection selected-file count is invalid",
        )
        _expect(
            isinstance(window["start_utc"], str) and isinstance(window["end_utc"], str),
            "collection window times are invalid",
        )
        _expect(
            parse_time(window["start_utc"], "collection start")
            <= parse_time(window["end_utc"], "collection end"),
            "collection window is reversed",
        )


def _verify_event_semantics(event: Mapping[str, Any]) -> None:
    _expect(event["schema"] == EVENT_SCHEMA, "event schema is invalid")
    _expect(event["time_source"] == "local-system-clock-unattested", "time source overclaims")
    _expect(event["boundaries"] == BOUNDARIES, "event crosses the preservation boundary")
    _verify_source(event["source"])
    _expect(
        isinstance(event["trigger"], str)
        and TRIGGER_PATTERN.fullmatch(event["trigger"]) is not None,
        "event trigger is invalid",
    )
    _expect(
        event["repository"] is None
        or isinstance(event["repository"], str)
        and REPOSITORY_PATTERN.fullmatch(event["repository"]) is not None,
        "event repository is invalid",
    )
    _expect(isinstance(event["objects"], list), "event objects are not an array")
    _expect(set(event["disposition"]) == DISPOSITION_KEYS, "disposition is not closed")
    status_value = event["disposition"]["status"]
    _expect(status_value in {"captured", "excluded", "unavailable"}, "disposition status is invalid")
    if status_value == "captured":
        _expect(len(event["objects"]) == 1, "captured source must bind one object")
        _expect(event["disposition"]["reason"] is None, "captured source has an unavailable reason")
        source_label = event["source"]["label"].casefold()
        _expect(
            not any(source_label.endswith(suffix) for suffix in PRIVATE_KEY_CONTAINER_SUFFIXES),
            "captured source is a private-key container",
        )
    else:
        _expect(not event["objects"], "unavailable or excluded source binds an object")
        _expect(
            isinstance(event["disposition"]["reason"], str) and event["disposition"]["reason"],
            "unavailable or excluded source has no reason",
        )
    for item in event["objects"]:
        _expect(isinstance(item, dict) and set(item) == OBJECT_KEYS, "object record is not closed")
        _expect(bool(SHA256_PATTERN.fullmatch(item["sha256"])), "object digest is invalid")
        _expect(_is_non_negative_int(item["bytes"]), "object size is invalid")
        _expect(isinstance(item["opaque"], bool), "object opacity marker is invalid")
        _expect(
            isinstance(item["secret_scan_performed"], bool),
            "object secret-scan marker is invalid",
        )
        _expect(
            item["sensitivity"] in {"owner-only-raw", "owner-only-redacted", "public-source"},
            "object sensitivity is invalid",
        )
        _expect(
            item["public_projection_eligible"] is False,
            "captured source cannot be public-projection eligible",
        )
        if item["media_type"] == "application/zip":
            _expect(item["opaque"] is True, "ZIP evidence must remain opaque")
    utc_time = parse_time(event["captured_at_utc"], "captured_at_utc")
    london = parse_time(event["captured_at_europe_london"], "captured_at_europe_london")
    _expect(utc_time == london, "UTC and Europe/London capture times differ")
    _verify_local_semantics(event)


def _verify_local_semantics(event: Mapping[str, Any]) -> None:
    source = event["source"]
    kind = source["kind"]
    if kind not in LOCAL_SOURCE_KINDS:
        return
    _expect(
        source["occurred_at_utc"] is None
        and source["expires_at_utc"] is None
        and source["expiry_basis"] == "unknown"
        and source["commit_sha"] is None
        and source["tree_sha"] is None
        and source["collection_generation_sha256"] is None
        and source["collection_window"] is None
        and all(
            category.startswith("journal-label:")
            for category in source["redaction_categories"]
        )
        and source["redaction_count"] == _journal_label_redaction_count(source),
        "local source metadata is outside the closed capture contract",
    )
    expected_snapshot = "apfs-clonefile" if kind == "local-apfs-clone" else "stable-byte-copy"
    expected_redaction = (
        "operator-supplied-redacted-jsonl-not-attested"
        if kind == "local-redacted-jsonl"
        else "none"
    )
    _expect(
        source["snapshot_method"] == expected_snapshot
        and source["redaction_mode"] == expected_redaction,
        "local source capture mode differs",
    )
    identity = re.fullmatch(
        re.escape(kind)
        + r":path-sha256:([0-9a-f]{64}):device:([0-9]+):inode:([0-9]+):"
        + r"mtime-ns:([0-9]+):ctime-ns:([0-9]+):bytes:([0-9]+):"
        + r"content-sha256:([0-9a-f]{64})",
        source["identity"],
    )
    _expect(identity is not None, "local source identity differs")
    if identity is None:
        return
    before = source["source_stat_before"]
    _expect(isinstance(before, dict), "local source lacks acquisition stat evidence")
    if not isinstance(before, dict):
        return
    for group, key in zip(
        identity.groups()[1:6],
        ("device", "inode", "mtime_ns", "ctime_ns", "bytes"),
        strict=True,
    ):
        _expect(int(group) == before[key], f"local source {key} identity differs")
    if kind != "local-apfs-clone":
        _expect(
            source["source_changed_after_snapshot"] is False
            and source["source_stat_before"] == source["source_stat_after"],
            "stable local source changed during capture",
        )

    status_value = event["disposition"]["status"]
    reason = event["disposition"]["reason"]
    if status_value == "excluded":
        match = re.fullmatch(r"secret-category:([a-z0-9-]+)", str(reason))
        _expect(
            match is not None and match.group(1) in LOCAL_SECRET_CATEGORIES,
            "local exclusion reason is outside the closed capture contract",
        )
        return
    if status_value == "unavailable":
        _expect(
            reason
            in {
                "unsupported-compressed-or-archive-format",
                "unsupported-opaque-binary-format",
            },
            "local unavailable reason is outside the closed capture contract",
        )
        return
    _expect(status_value == "captured", "local source disposition is invalid")
    item = event["objects"][0]
    _expect(item["sha256"] == identity.group(7), "local object digest differs from identity")
    _expect(item["bytes"] == int(identity.group(6)), "local object size differs from identity")
    _expect(item["secret_scan_performed"] is True, "local object lacks its required secret scan")
    if kind == "local-redacted-jsonl":
        _expect(
            item["role"] == "redacted-jsonl"
            and item["media_type"] == "application/x-ndjson"
            and item["opaque"] is False
            and item["secret_scan"]
            == "operator-redacted-jsonl-high-confidence-scan-passed"
            and item["sensitivity"] == "owner-only-redacted",
            "redacted JSONL object metadata differs",
        )
        return
    _expect(
        item["role"] == "local-source" and item["sensitivity"] == "owner-only-raw",
        "local raw object metadata differs",
    )
    object_domains = {
        "application/json": (False, "high-confidence-text-scan-passed"),
        "application/x-ndjson": (False, "high-confidence-text-scan-passed"),
        "text/plain; charset=utf-8": (False, "high-confidence-text-scan-passed"),
        "image/png": (True, "validated-png-high-confidence-byte-scan-passed"),
        "image/jpeg": (True, "validated-jpeg-high-confidence-metadata-scan-passed"),
        "application/zip": (True, "zip-entry-high-confidence-scan-passed"),
    }
    _expect(item["media_type"] in object_domains, "local object media type is invalid")
    if item["media_type"] not in object_domains:
        return
    expected_opaque, expected_scan = object_domains[item["media_type"]]
    _expect(
        item["opaque"] is expected_opaque and item["secret_scan"] == expected_scan,
        "local object scan metadata differs",
    )
    if kind == "local-apfs-clone":
        _expect(
            item["media_type"] in {"image/png", "image/jpeg", "application/zip"},
            "APFS clone object media type is invalid",
        )


def _object_paths(root: Path) -> dict[str, Path]:
    object_root = root / "objects" / "sha256"
    observed: dict[str, Path] = {}
    for shard in sorted(object_root.iterdir()):
        _expect(shard.is_dir() and not shard.is_symlink(), "object shard is invalid")
        _expect(re.fullmatch(r"[0-9a-f]{2}", shard.name) is not None, "object shard name is invalid")
        for path in sorted(shard.iterdir()):
            _expect(path.is_file() and not path.is_symlink(), "content object is invalid")
            _expect(bool(SHA256_PATTERN.fullmatch(path.name)), "content-object name is invalid")
            _expect(path.name.startswith(shard.name), "content object is in the wrong shard")
            _expect(path.name not in observed, "duplicate content object")
            observed[path.name] = path
    return observed


def _github_event_value(
    event: Mapping[str, Any], observed: Mapping[str, Path], label: str
) -> Any:
    _expect(
        event["disposition"]["status"] == "captured" and len(event["objects"]) == 1,
        f"{label} object is unavailable",
    )
    item = event["objects"][0]
    _expect(item["media_type"] == "application/json", f"{label} is not JSON")
    path = observed.get(item["sha256"])
    _expect(path is not None, f"{label} object is missing")
    if path is None:  # pragma: no cover - narrowed by the fail-closed check
        raise EvidenceVerificationError(f"{label} object is missing")
    raw = _read_private_file_bounded(path, label, MAX_METADATA_BYTES)
    value = parse_json(raw, label)
    _expect(raw == canonical_json(value, pretty=True), f"{label} is not canonical")
    return value


def _github_event_json(
    event: Mapping[str, Any], observed: Mapping[str, Path], label: str
) -> Mapping[str, Any]:
    value = _github_event_value(event, observed, label)
    _expect(isinstance(value, dict), f"{label} is not an object")
    return value if isinstance(value, dict) else {}


def _flatten_github_pages_for_verification(value: object, label: str) -> list[Mapping[str, Any]]:
    _expect(isinstance(value, list), f"{label} is not an array")
    if not isinstance(value, list):
        return []
    candidates: list[object]
    if all(isinstance(page, list) for page in value):
        candidates = [item for page in value for item in page]
    else:
        candidates = list(value)
    _expect(all(isinstance(item, dict) for item in candidates), f"{label} contains a non-object")
    return [item for item in candidates if isinstance(item, dict)]


def _verify_github_observation_source_digest(
    source: Mapping[str, Any],
    *,
    base_identity: str,
    expected_digest: str,
) -> None:
    base_source = dict(source)
    base_source["identity"] = base_identity
    base_source["identity_sha256"] = source_identity_sha256(base_identity)
    _expect(
        hashlib.sha256(canonical_json(base_source)).hexdigest() == expected_digest,
        "GitHub observation source digest differs",
    )


def _verify_github_semantics(
    events: Sequence[Mapping[str, Any]], observed: Mapping[str, Path]
) -> None:
    github_events = [
        event
        for event in events
        if isinstance(event["source"].get("kind"), str)
        and event["source"]["kind"].startswith("github-")
    ]
    _expect(
        all(event["source"]["kind"] in GITHUB_SOURCE_KINDS for event in github_events),
        "GitHub source kind is outside the closed capture contract",
    )
    repositories: dict[int, tuple[str, bool]] = {}
    captured_repository_ids: set[int] = set()
    for event in github_events:
        if event["source"]["kind"] != "github-repository-identity-snapshot":
            continue
        identity_match = re.fullmatch(
            r"github:repository:([1-9][0-9]*):metadata:snapshot:([0-9a-f]{64})",
            event["source"]["identity"],
        )
        _expect(identity_match is not None, "GitHub repository source identity differs")
        if identity_match is None:
            continue
        repository_id = int(identity_match.group(1))
        if event["disposition"]["status"] != "captured":
            _expect(
                event["disposition"]["status"] == "excluded",
                "GitHub repository identity is neither captured nor policy-excluded",
            )
            full_name = event["repository"]
            _expect(
                isinstance(full_name, str)
                and REPOSITORY_PATTERN.fullmatch(full_name) is not None,
                "GitHub excluded repository identity is invalid",
            )
            if not isinstance(full_name, str):
                continue
            prior = repositories.get(repository_id)
            _expect(
                prior is None or prior[0] == full_name,
                "GitHub repository snapshots disagree on canonical identity",
            )
            repositories.setdefault(repository_id, (full_name, False))
            continue
        value = _github_event_json(event, observed, "GitHub repository identity")
        _expect(
            identity_match.group(2)
            == hashlib.sha256(canonical_json(value, pretty=True)).hexdigest(),
            "GitHub repository snapshot digest differs",
        )
        value_repository_id = value.get("id")
        full_name = value.get("full_name")
        _expect(
            _is_positive_int(value_repository_id)
            and isinstance(full_name, str)
            and REPOSITORY_PATTERN.fullmatch(full_name) is not None,
            "GitHub repository identity is invalid",
        )
        if not _is_positive_int(value_repository_id) or not isinstance(full_name, str):
            continue
        _expect(
            repository_id == value_repository_id,
            "GitHub repository snapshot id differs",
        )
        _expect(event["repository"] == full_name, "GitHub repository event binding differs")
        private = value.get("private") is True or value.get("visibility") == "private"
        prior = repositories.get(repository_id)
        _expect(
            prior is None or prior[0] == full_name,
            "GitHub repository snapshots disagree on canonical identity",
        )
        repositories[repository_id] = (full_name, private)
        captured_repository_ids.add(repository_id)

    for event in github_events:
        match = re.match(r"^github:repository:([1-9][0-9]*)(?::|$)", event["source"]["identity"])
        _expect(match is not None, "GitHub source identity has no repository binding")
        if match is None:
            continue
        repository_id = int(match.group(1))
        _expect(repository_id in repositories, "GitHub source has no repository identity snapshot")
        if repository_id not in repositories:
            continue
        _expect(
            repository_id in captured_repository_ids
            or event["source"]["kind"] == "github-repository-identity-snapshot",
            "GitHub policy-excluded repository identity has child evidence",
        )
        full_name, _private = repositories[repository_id]
        _expect(event["repository"] == full_name, "GitHub event repository differs from its source")
        _expect(
            event["source"]["snapshot_method"] == "github-api-download"
            and event["source"]["redaction_mode"] == "none"
            and all(
                category.startswith("journal-label:")
                for category in event["source"]["redaction_categories"]
            )
            and event["source"]["redaction_count"]
            == _journal_label_redaction_count(event["source"])
            and (
                event["source"]["kind"] == "github-actions-artifact"
                and isinstance(
                    event["source"]["collection_generation_sha256"], str
                )
                or event["source"]["kind"] != "github-actions-artifact"
                and event["source"]["collection_generation_sha256"] is None
            )
            and event["source"]["collection_window"] is None,
            "GitHub source metadata is outside the closed capture contract",
        )
        if event["source"]["kind"] in {
            "github-repository-identity-snapshot",
            "github-actions-retention-policy-snapshot",
            "github-discussion-snapshot",
        }:
            _expect(
                event["source"]["commit_sha"] is None
                and event["source"]["tree_sha"] is None
                and event["source"]["occurred_at_utc"] is None
                and event["source"]["expires_at_utc"] is None
                and event["source"]["expiry_basis"] == "unknown",
                "GitHub non-run source has commit provenance",
            )
        elif event["source"]["kind"] in {
            "github-actions-run-metadata",
            "github-actions-run-jobs",
            "github-actions-artifact-metadata",
        }:
            _expect(
                event["source"]["expires_at_utc"] is None
                and event["source"]["expiry_basis"] == "unknown",
                "GitHub run metadata has an unsupported expiry claim",
            )
        for item in event["objects"]:
            _expect(
                item["sensitivity"] == "owner-only-raw",
                "GitHub evidence sensitivity differs from capture policy",
            )

    github_json_roles = {
        "github-repository-identity-snapshot": "github-repository-identity",
        "github-actions-retention-policy-snapshot": "github-actions-retention-policy",
        "github-actions-run-metadata": "github-run-metadata",
        "github-actions-run-jobs": "github-run-jobs",
        "github-actions-artifact-metadata": "github-artifact-metadata",
    }
    for event in github_events:
        if event["disposition"]["status"] != "captured":
            continue
        kind = event["source"]["kind"]
        item = event["objects"][0]
        if kind in github_json_roles:
            _expect(
                item["role"] == github_json_roles[kind]
                and item["media_type"] == "application/json"
                and item["opaque"] is False
                and item["secret_scan"] == "high-confidence-text-scan-passed"
                and item["secret_scan_performed"] is True,
                "GitHub JSON object metadata is outside the closed capture contract",
            )
        elif kind in {"github-actions-run-logs", "github-actions-artifact"}:
            expected_role = (
                "github-run-logs-archive"
                if kind == "github-actions-run-logs"
                else "github-artifact-archive"
            )
            _expect(
                item["role"] == expected_role
                and item["media_type"] == "application/zip"
                and item["opaque"] is True
                and item["secret_scan"] == "zip-entry-high-confidence-scan-passed"
                and item["secret_scan_performed"] is True,
                "GitHub archive object metadata is outside the closed capture contract",
            )

    for event in github_events:
        if event["source"]["kind"] != "github-actions-retention-policy-snapshot":
            continue
        unavailable_match = re.fullmatch(
            r"github:repository:([1-9][0-9]*):actions-retention:"
            r"observation:lookup-unavailable:source-sha256:([0-9a-f]{64})",
            event["source"]["identity"],
        )
        if unavailable_match is not None:
            _verify_github_observation_source_digest(
                event["source"],
                base_identity=(
                    f"github:repository:{unavailable_match.group(1)}:actions-retention"
                ),
                expected_digest=unavailable_match.group(2),
            )
            _expect(
                event["disposition"]["status"] == "unavailable"
                and event["disposition"]["reason"] == "github-metadata-unavailable"
                and event["objects"] == [],
                "GitHub retention lookup observation is invalid",
            )
            continue
        match = re.fullmatch(
            r"github:repository:([1-9][0-9]*):actions-retention:snapshot:"
            r"([0-9a-f]{64})",
            event["source"]["identity"],
        )
        _expect(match is not None, "GitHub retention source identity is invalid")
        if match is None:
            continue
        if event["disposition"]["status"] != "captured":
            _expect(
                event["disposition"]["status"] == "excluded",
                "GitHub retention snapshot is neither captured nor policy-excluded",
            )
            continue
        value = _github_event_json(event, observed, "GitHub retention policy")
        _expect(
            match.group(2)
            == hashlib.sha256(canonical_json(value, pretty=True)).hexdigest(),
            "GitHub retention snapshot digest differs",
        )
        _expect(
            _is_positive_int(value.get("days"))
            and int(value["days"]) <= GITHUB_MAX_RETENTION_DAYS,
            "GitHub retention policy is invalid",
        )

    for event in github_events:
        if event["source"]["kind"] != "github-discussion-snapshot":
            continue
        match = re.fullmatch(
            r"github:repository:([1-9][0-9]*):discussion:([1-9][0-9]*):"
            r"(issue-or-pull-request|issue-comments|pull-request|pull-request-reviews|"
            r"pull-request-review-comments):snapshot:([0-9a-f]{64})",
            event["source"]["identity"],
        )
        _expect(match is not None, "GitHub discussion source identity is invalid")
        if match is None:
            continue
        repository_id = int(match.group(1))
        number = int(match.group(2))
        role = match.group(3)
        if event["disposition"]["status"] != "captured":
            _expect(
                event["disposition"]["status"] == "excluded",
                "GitHub discussion snapshot is neither captured nor policy-excluded",
            )
            continue
        discussion_item = event["objects"][0]
        _expect(
            discussion_item["role"] == f"github-{role}"
            and discussion_item["media_type"] == "application/json"
            and discussion_item["opaque"] is False
            and discussion_item["secret_scan"] == "high-confidence-text-scan-passed"
            and discussion_item["secret_scan_performed"] is True,
            "GitHub discussion object metadata is outside the closed capture contract",
        )
        value = _github_event_value(event, observed, f"GitHub discussion {role}")
        _expect(
            match.group(4) == hashlib.sha256(canonical_json(value, pretty=True)).hexdigest(),
            "GitHub discussion snapshot digest differs",
        )
        repository, _private = repositories[repository_id]
        repository_url = f"https://api.github.com/repos/{repository}"
        issue_url = f"{repository_url}/issues/{number}"
        pull_url = f"{repository_url}/pulls/{number}"
        if role == "issue-or-pull-request":
            _expect(
                isinstance(value, dict)
                and value.get("number") == number
                and value.get("repository_url") == repository_url
                and value.get("url") == issue_url,
                "GitHub discussion issue binding differs",
            )
            if isinstance(value, dict) and "pull_request" in value:
                pull_link = value.get("pull_request")
                _expect(
                    isinstance(pull_link, dict) and pull_link.get("url") == pull_url,
                    "GitHub discussion pull-request link differs",
                )
        elif role == "issue-comments":
            for comment in _flatten_github_pages_for_verification(value, role):
                _expect(
                    comment.get("issue_url") == issue_url,
                    "GitHub issue-comment parent differs",
                )
        elif role == "pull-request":
            base = value.get("base") if isinstance(value, dict) else None
            base_repository = base.get("repo") if isinstance(base, dict) else None
            _expect(
                isinstance(value, dict)
                and value.get("number") == number
                and value.get("url") == pull_url
                and isinstance(base_repository, dict)
                and base_repository.get("id") == repository_id
                and isinstance(base_repository.get("full_name"), str)
                and base_repository["full_name"].casefold() == repository.casefold(),
                "GitHub pull-request repository binding differs",
            )
        else:
            for item in _flatten_github_pages_for_verification(value, role):
                _expect(
                    item.get("pull_request_url") == pull_url,
                    "GitHub pull-request child parent differs",
                )

    run_bindings: dict[tuple[int, int, int], tuple[str, str]] = {}
    excluded_run_bindings: dict[tuple[int, int, int], tuple[str, str]] = {}
    run_level_bindings: dict[tuple[int, int], tuple[str, str]] = {}
    run_occurrences: dict[tuple[int, int, int], str] = {}
    run_level_occurrences: dict[tuple[int, int], tuple[int, str]] = {}
    for event in github_events:
        if event["source"]["kind"] != "github-actions-run-metadata":
            continue
        identity_match = re.fullmatch(
            r"github:repository:([1-9][0-9]*):run:([1-9][0-9]*):attempt:"
            r"([1-9][0-9]*):metadata:snapshot:([0-9a-f]{64})",
            event["source"]["identity"],
        )
        _expect(identity_match is not None, "GitHub run identity differs")
        if identity_match is None:
            continue
        repository_id = int(identity_match.group(1))
        run_id = int(identity_match.group(2))
        attempt = int(identity_match.group(3))
        key = (repository_id, run_id, attempt)
        if event["disposition"]["status"] != "captured":
            _expect(
                event["disposition"]["status"] == "excluded",
                "GitHub run snapshot is neither captured nor policy-excluded",
            )
            commit_sha = event["source"]["commit_sha"]
            tree_sha = event["source"]["tree_sha"]
            _expect(
                repository_id in repositories
                and isinstance(commit_sha, str)
                and re.fullmatch(r"[0-9a-f]{40}", commit_sha) is not None
                and isinstance(tree_sha, str)
                and re.fullmatch(r"[0-9a-f]{40}", tree_sha) is not None,
                "GitHub excluded run provenance is invalid",
            )
            if isinstance(commit_sha, str) and isinstance(tree_sha, str):
                binding = (commit_sha, tree_sha)
                prior = excluded_run_bindings.get(key)
                _expect(
                    prior is None or prior == binding,
                    "GitHub excluded run observations have inconsistent provenance",
                )
                excluded_run_bindings[key] = binding
            continue
        value = _github_event_json(event, observed, "GitHub run metadata")
        _expect(
            identity_match.group(4)
            == hashlib.sha256(canonical_json(value, pretty=True)).hexdigest(),
            "GitHub run snapshot digest differs",
        )
        run_id = value.get("id")
        attempt = value.get("run_attempt")
        head_sha = value.get("head_sha")
        head_commit = value.get("head_commit")
        tree_sha = head_commit.get("tree_id") if isinstance(head_commit, dict) else None
        commit_id = head_commit.get("id") if isinstance(head_commit, dict) else None
        completion_time = value.get("updated_at") or value.get("run_started_at")
        occurrence_time = value.get("run_started_at") or value.get("created_at")
        _expect(
            _is_positive_int(run_id)
            and _is_positive_int(attempt)
            and isinstance(head_sha, str)
            and re.fullmatch(r"[0-9a-fA-F]{40}", head_sha) is not None
            and isinstance(commit_id, str)
            and commit_id.lower() == head_sha.lower()
            and isinstance(tree_sha, str)
            and re.fullmatch(r"[0-9a-fA-F]{40}", tree_sha) is not None,
            "GitHub run source identity is invalid",
        )
        _expect(
            isinstance(completion_time, str),
            "GitHub run completion time is invalid",
        )
        _expect(
            isinstance(occurrence_time, str),
            "GitHub run occurrence time is invalid",
        )
        if not (_is_positive_int(run_id) and _is_positive_int(attempt)):
            continue
        binding = (str(head_sha).lower(), str(tree_sha).lower())
        _expect(
            (int(identity_match.group(2)), int(identity_match.group(3))) == (run_id, attempt),
            "GitHub run source identity differs from its metadata",
        )
        _expect(
            (event["source"]["commit_sha"], event["source"]["tree_sha"]) == binding,
            "GitHub run event source differs from its metadata",
        )
        key = (repository_id, int(run_id), int(attempt))
        if isinstance(completion_time, str):
            parse_time(completion_time, "GitHub run completion")
        normalised_occurrence = (
            format_time(parse_time(occurrence_time, "GitHub run occurrence"))
            if isinstance(occurrence_time, str)
            else ""
        )
        _expect(
            event["source"]["occurred_at_utc"] == normalised_occurrence,
            "GitHub run occurrence differs from retained provider metadata",
        )
        prior_occurrence = run_occurrences.get(key)
        _expect(
            prior_occurrence is None or prior_occurrence == normalised_occurrence,
            "GitHub run snapshots have inconsistent occurrence times",
        )
        run_occurrences[key] = normalised_occurrence
        excluded_binding = excluded_run_bindings.get(key)
        _expect(
            excluded_binding is None or excluded_binding == binding,
            "GitHub captured and excluded run observations disagree on provenance",
        )
        run_bindings[key] = binding
        run_key = (repository_id, int(run_id))
        prior = run_level_bindings.get(run_key)
        _expect(prior is None or prior == binding, "GitHub run attempts have inconsistent provenance")
        run_level_bindings[run_key] = binding
        prior_level_occurrence = run_level_occurrences.get(run_key)
        if prior_level_occurrence is None or int(attempt) > prior_level_occurrence[0]:
            run_level_occurrences[run_key] = (int(attempt), normalised_occurrence)
        elif int(attempt) == prior_level_occurrence[0]:
            _expect(
                prior_level_occurrence[1] == normalised_occurrence,
                "GitHub latest run attempt has inconsistent occurrence times",
            )

    artifact_bindings: dict[
        tuple[int, int, int, str],
        tuple[int, str | None, str, bool, str | None, str],
    ] = {}
    artifact_immutable_bindings: dict[
        tuple[int, int, int], tuple[int, str | None, str]
    ] = {}
    artifact_metadata_snapshots: dict[tuple[int, int], list[tuple[int, str]]] = {}
    artifact_metadata_keys: set[tuple[int, int, int]] = set()
    for event in github_events:
        if event["source"]["kind"] != "github-actions-artifact-metadata":
            continue
        match = re.fullmatch(
            r"github:repository:([1-9][0-9]*):run:([1-9][0-9]*):"
            r"artifacts-metadata:snapshot:([0-9a-f]{64})",
            event["source"]["identity"],
        )
        _expect(match is not None, "GitHub artefact metadata identity is invalid")
        if match is None:
            continue
        repository_id, run_id = int(match.group(1)), int(match.group(2))
        run_key = (repository_id, run_id)
        _expect(run_key in run_level_bindings, "GitHub artefact metadata has no run binding")
        _expect(
            run_key in run_level_occurrences
            and event["source"]["occurred_at_utc"]
            == run_level_occurrences[run_key][1],
            "GitHub artefact metadata occurrence differs from its latest run attempt",
        )
        if event["disposition"]["status"] != "captured":
            _expect(
                event["disposition"]["status"] == "excluded",
                "GitHub artefact metadata is neither captured nor policy-excluded",
            )
            if run_key in run_level_bindings:
                _expect(
                    (event["source"]["commit_sha"], event["source"]["tree_sha"])
                    == run_level_bindings[run_key],
                    "GitHub excluded artefact metadata provenance differs",
                )
            continue
        value = _github_event_json(event, observed, "GitHub artefact metadata")
        _expect(
            match.group(3)
            == hashlib.sha256(canonical_json(value, pretty=True)).hexdigest(),
            "GitHub artefact metadata snapshot digest differs",
        )
        metadata_digest = match.group(3)
        artifact_metadata_snapshots.setdefault(run_key, []).append(
            (int(event["sequence"]), metadata_digest)
        )
        artifacts = value.get("artifacts")
        _expect(isinstance(artifacts, list), "GitHub artefact metadata is invalid")
        if not isinstance(artifacts, list) or run_key not in run_level_bindings:
            continue
        expected_head, expected_tree = run_level_bindings[run_key]
        _expect(
            (event["source"]["commit_sha"], event["source"]["tree_sha"])
            == (expected_head, expected_tree),
            "GitHub artefact metadata provenance differs",
        )
        snapshot_ids: set[int] = set()
        for artifact in artifacts:
            _expect(isinstance(artifact, dict), "GitHub artefact row is invalid")
            if not isinstance(artifact, dict):
                continue
            artifact_id = artifact.get("id")
            size = artifact.get("size_in_bytes")
            workflow = artifact.get("workflow_run")
            provider_digest = artifact.get("digest")
            expired = artifact.get("expired")
            expires_at = artifact.get("expires_at")
            _expect(
                _is_positive_int(artifact_id)
                and _is_non_negative_int(size)
                and isinstance(workflow, dict)
                and workflow.get("id") == run_id
                and workflow.get("repository_id") == repository_id
                and isinstance(workflow.get("head_sha"), str)
                and workflow["head_sha"].lower() == expected_head,
                "GitHub artefact workflow binding differs",
            )
            _expect(
                provider_digest is None
                or isinstance(provider_digest, str)
                and re.fullmatch(r"sha256:[0-9a-fA-F]{64}", provider_digest) is not None,
                "GitHub artefact provider digest is invalid",
            )
            _expect(
                isinstance(expired, bool),
                "GitHub artefact expiry marker is invalid",
            )
            _expect(
                expires_at is None or isinstance(expires_at, str),
                "GitHub artefact expiry time is invalid",
            )
            if not (
                _is_positive_int(artifact_id)
                and _is_non_negative_int(size)
                and isinstance(workflow, dict)
                and isinstance(workflow.get("head_sha"), str)
                and isinstance(expired, bool)
                and (expires_at is None or isinstance(expires_at, str))
            ):
                continue
            _expect(artifact_id not in snapshot_ids, "GitHub artefact id is duplicated")
            snapshot_ids.add(artifact_id)
            artifact_key = (repository_id, run_id, int(artifact_id))
            binding_key = (*artifact_key, metadata_digest)
            normalised_digest = (
                provider_digest.removeprefix("sha256:").lower()
                if isinstance(provider_digest, str)
                else None
            )
            normalised_expiry = (
                format_time(parse_time(expires_at, "GitHub artefact expiry"))
                if isinstance(expires_at, str)
                else None
            )
            created_at = artifact.get("created_at") or run_level_occurrences[run_key][1]
            normalised_occurrence = (
                format_time(parse_time(created_at, "GitHub artefact creation"))
                if isinstance(created_at, str)
                else ""
            )
            binding = (
                int(size),
                normalised_digest,
                expected_head,
                expired,
                normalised_expiry,
                normalised_occurrence,
            )
            immutable_binding = (int(size), normalised_digest, expected_head)
            immutable_prior = artifact_immutable_bindings.get(artifact_key)
            if immutable_prior is not None:
                _expect(
                    immutable_prior[0] == immutable_binding[0]
                    and immutable_prior[2] == immutable_binding[2]
                    and (
                        immutable_prior[1] is None
                        or immutable_binding[1] is None
                        or immutable_prior[1] == immutable_binding[1]
                    ),
                    "GitHub artefact metadata changed immutable provider bindings",
                )
                immutable_binding = (
                    immutable_binding[0],
                    immutable_prior[1]
                    if immutable_prior[1] is not None
                    else immutable_binding[1],
                    immutable_binding[2],
                )
            artifact_immutable_bindings[artifact_key] = immutable_binding
            prior = artifact_bindings.get(binding_key)
            _expect(
                prior is None or prior == binding,
                "GitHub artefact metadata snapshot has inconsistent provider bindings",
            )
            artifact_bindings[binding_key] = binding
            artifact_metadata_keys.add(artifact_key)

    seen_artifact_keys: set[tuple[int, int, int]] = set()
    for event in github_events:
        kind = event["source"]["kind"]
        identity = event["source"]["identity"]
        attempt_match = re.match(
            r"^github:repository:([1-9][0-9]*):run:([1-9][0-9]*):attempt:([1-9][0-9]*):",
            identity,
        )
        run_match = re.match(
            r"^github:repository:([1-9][0-9]*):run:([1-9][0-9]*):",
            identity,
        )
        if kind in {"github-actions-run-jobs", "github-actions-run-logs"}:
            _expect(attempt_match is not None, "GitHub attempt source identity is invalid")
            if attempt_match is None:
                continue
            key = tuple(int(value) for value in attempt_match.groups())
            _expect(
                key not in excluded_run_bindings or key in run_bindings,
                "GitHub policy-excluded run attempt has child evidence",
            )
            _expect(key in run_bindings, "GitHub attempt has no run metadata binding")
            if key in run_bindings:
                _expect(
                    (event["source"]["commit_sha"], event["source"]["tree_sha"])
                    == run_bindings[key],
                    "GitHub attempt source provenance differs",
                )
                _expect(
                    event["source"]["occurred_at_utc"] == run_occurrences[key],
                    "GitHub attempt occurrence differs from its run metadata",
                )
            if kind == "github-actions-run-logs":
                logs_match = re.fullmatch(
                    r"github:repository:([1-9][0-9]*):run:([1-9][0-9]*):attempt:"
                    r"([1-9][0-9]*):logs(?::observation:(download-unavailable|"
                    r"archive-validation-failed):source-sha256:([0-9a-f]{64}))?",
                    identity,
                )
                _expect(logs_match is not None, "GitHub logs source identity is invalid")
                suffix = logs_match.group(4) if logs_match is not None else None
                if logs_match is not None and suffix is not None:
                    _verify_github_observation_source_digest(
                        event["source"],
                        base_identity=(
                            f"github:repository:{key[0]}:run:{key[1]}:attempt:"
                            f"{key[2]}:logs"
                        ),
                        expected_digest=logs_match.group(5),
                    )
                status_value = event["disposition"]["status"]
                _expect(
                    (status_value in {"captured", "excluded"} and suffix is None)
                    or (status_value == "unavailable" and suffix is not None),
                    "GitHub logs observation status differs from its identity",
                )
                if suffix is not None:
                    _expect(
                        event["disposition"]["reason"]
                        == {
                            "download-unavailable": "github-download-unavailable",
                            "archive-validation-failed": "github-archive-validation-failed",
                        }[suffix],
                        "GitHub logs observation reason differs from its identity",
                    )
                source = event["source"]
                _expect(
                    source["expiry_basis"] == "unknown"
                    and source["expires_at_utc"] is None,
                    "GitHub historical log expiry is not independently evidenced",
                )
            if kind == "github-actions-run-jobs":
                jobs_match = re.fullmatch(
                    r"github:repository:([1-9][0-9]*):run:([1-9][0-9]*):attempt:"
                    r"([1-9][0-9]*):jobs:snapshot:([0-9a-f]{64})",
                    identity,
                )
                _expect(jobs_match is not None, "GitHub jobs source identity is invalid")
            if kind == "github-actions-run-jobs" and event["objects"]:
                jobs_value = _github_event_json(event, observed, "GitHub run jobs")
                if jobs_match is not None:
                    _expect(
                        jobs_match.group(4)
                        == hashlib.sha256(canonical_json(jobs_value, pretty=True)).hexdigest(),
                        "GitHub jobs snapshot digest differs",
                    )
                jobs = jobs_value.get("jobs")
                _expect(isinstance(jobs, list), "GitHub run jobs are invalid")
                if isinstance(jobs, list):
                    for job in jobs:
                        _expect(
                            isinstance(job, dict)
                            and job.get("run_id") == key[1]
                            and job.get("run_attempt") == key[2]
                            and isinstance(job.get("head_sha"), str)
                            and job["head_sha"].lower() == run_bindings[key][0],
                            "GitHub job source provenance differs",
                        )
        elif kind == "github-actions-artifact-metadata":
            _expect(run_match is not None, "GitHub artefact source identity is invalid")
            if run_match is None:
                continue
            key = tuple(int(value) for value in run_match.groups())
            _expect(key in run_level_bindings, "GitHub artefact has no run metadata binding")
            if key in run_level_bindings:
                _expect(
                    (event["source"]["commit_sha"], event["source"]["tree_sha"])
                    == run_level_bindings[key],
                    "GitHub artefact source provenance differs",
                )
        elif kind == "github-actions-artifact":
            artifact_match = re.fullmatch(
                r"github:repository:([1-9][0-9]*):run:([1-9][0-9]*):artifact:"
                r"([1-9][0-9]*):zip(?::observation:(expired|"
                r"policy-skip-max-bytes-[0-9]+|download-unavailable|"
                r"provider-size-mismatch|provider-digest-mismatch|"
                r"archive-validation-failed):source-sha256:([0-9a-f]{64}))?",
                identity,
            )
            _expect(artifact_match is not None, "GitHub artefact source identity is invalid")
            if artifact_match is None:
                continue
            key = tuple(int(value) for value in artifact_match.groups()[:3])
            suffix = artifact_match.group(4)
            if suffix is not None:
                _verify_github_observation_source_digest(
                    event["source"],
                    base_identity=(
                        f"github:repository:{key[0]}:run:{key[1]}:"
                        f"artifact:{key[2]}:zip"
                    ),
                    expected_digest=artifact_match.group(5),
                )
            generation = event["source"]["collection_generation_sha256"]
            _expect(
                isinstance(generation, str),
                "GitHub artefact has no exact metadata snapshot binding",
            )
            run_key = key[:2]
            preceding_snapshots = [
                (sequence, digest)
                for sequence, digest in artifact_metadata_snapshots.get(run_key, [])
                if sequence < int(event["sequence"])
            ]
            latest_preceding = (
                max(preceding_snapshots, key=lambda item: item[0])
                if preceding_snapshots
                else None
            )
            _expect(
                latest_preceding is not None and generation == latest_preceding[1],
                "GitHub artefact does not bind its exact preceding metadata snapshot",
            )
            binding_key = (*key, str(generation))
            _expect(
                binding_key in artifact_bindings,
                "GitHub artefact has no exact metadata row binding",
            )
            if binding_key not in artifact_bindings:
                continue
            seen_artifact_keys.add(key)
            binding = artifact_bindings[binding_key]
            _expect(
                (event["source"]["commit_sha"], event["source"]["tree_sha"])
                == run_level_bindings[key[:2]],
                "GitHub artefact source provenance differs",
            )
            status_value = event["disposition"]["status"]
            _expect(
                (status_value in {"captured", "excluded"} and suffix is None)
                or (status_value == "unavailable" and suffix is not None),
                "GitHub artefact observation status differs from its identity",
            )
            source_expiry = event["source"]["expires_at_utc"]
            _expect(
                (
                    source_expiry is None
                    and event["source"]["expiry_basis"] == "unknown"
                )
                or (
                    isinstance(source_expiry, str)
                    and event["source"]["expiry_basis"] == "provider-observed"
                ),
                "GitHub artefact expiry basis differs from provider metadata",
            )
            required_expired = suffix == "expired"
            _expect(
                (required_expired, source_expiry) == (binding[3], binding[4]),
                "GitHub artefact expiry differs from provider metadata",
            )
            _expect(
                event["source"]["occurred_at_utc"] == binding[5],
                "GitHub artefact occurrence differs from provider metadata",
            )
            if status_value == "captured":
                item = event["objects"][0]
                _expect(item["media_type"] == "application/zip", "GitHub artefact is not ZIP")
                _expect(item["bytes"] == binding[0], "GitHub artefact provider size differs")
                if binding[1] is not None:
                    _expect(
                        item["sha256"] == binding[1],
                        "GitHub artefact provider digest differs",
                    )
            elif suffix is not None:
                expected_reason = (
                    "selective-large-artifact-not-captured"
                    if suffix.startswith("policy-skip-max-bytes-")
                    else {
                        "expired": "github-artifact-expired",
                        "download-unavailable": "github-download-unavailable",
                        "provider-size-mismatch": (
                            "github-artifact-provider-size-mismatch"
                        ),
                        "provider-digest-mismatch": (
                            "github-artifact-provider-digest-mismatch"
                        ),
                        "archive-validation-failed": (
                            "github-archive-validation-failed"
                        ),
                    }.get(suffix)
                )
                _expect(
                    expected_reason is not None
                    and event["disposition"]["reason"] == expected_reason,
                    "GitHub artefact observation reason differs from its identity",
                )

    _expect(
        artifact_metadata_keys <= seen_artifact_keys,
        "GitHub artefact metadata has no capture or bounded observation",
    )


def _contains_excluded_projection_key(value: object) -> bool:
    if isinstance(value, dict):
        return any(
            re.sub(r"[^a-z0-9]", "", key.lower())
            in CODEX_EXCLUDED_KEY_NORMALISATIONS
            or _contains_excluded_projection_key(item)
            for key, item in value.items()
        )
    if isinstance(value, list):
        return any(_contains_excluded_projection_key(item) for item in value)
    if isinstance(value, str):
        oversized_hidden, oversized_sensitive = (
            _classify_codex_oversized_text_key_fragments(value)
        )
        if oversized_hidden or oversized_sensitive:
            return True
        for match in CODEX_JSON_KEY_FRAGMENT_PATTERN.finditer(value):
            try:
                key = json.loads(match.group(1))
            except json.JSONDecodeError:
                return True
            if (
                not isinstance(key, str)
                or re.sub(r"[^a-z0-9]", "", key.lower())
                in CODEX_EXCLUDED_KEY_NORMALISATIONS
            ):
                return True
        index = 0
        while index < len(value):
            character = value[index]
            if not character.isspace() and unicodedata.category(character) != "Cf":
                break
            index += 1
        structured = value[index:]
        if not structured.startswith(("{", "[")):
            return False
        try:
            embedded = json.loads(structured)
        except json.JSONDecodeError:
            return True
        if isinstance(embedded, (dict, list)):
            return _contains_excluded_projection_key(embedded)
    return False


def _verify_codex_event_payload_domains(payload: Mapping[str, Any]) -> None:
    event_type = payload["type"]
    _expect(isinstance(event_type, str), "Codex event type is invalid")
    if event_type == "user_message":
        if "message" in payload:
            _expect(_is_bounded_text(payload["message"]), "Codex user message is invalid")
        if "attachment_summary" in payload:
            _verify_attachment_summary(payload["attachment_summary"])
        return
    if event_type == "agent_message":
        _expect_bounded_text_fields(payload, ("message", "phase"), "Codex agent message")
        citation = payload.get("memory_citation")
        if citation is not None:
            _expect(isinstance(citation, dict), "Codex memory citation is not an object")
            if isinstance(citation, dict):
                _expect(set(citation) <= {"entries", "rolloutIds"}, "Codex citation is not closed")
                entries = citation.get("entries", [])
                _expect(isinstance(entries, list) and len(entries) <= 64, "Codex citations are invalid")
                if isinstance(entries, list):
                    for entry in entries:
                        _expect(
                            isinstance(entry, dict)
                            and set(entry)
                            <= {"lineStart", "lineEnd", "note", "path_basename", "path_sha256"},
                            "Codex citation entry is not closed",
                        )
                        if not isinstance(entry, dict):
                            continue
                        for key in ("lineStart", "lineEnd"):
                            if key in entry:
                                _expect(_is_non_negative_int(entry[key]), "Codex citation line is invalid")
                        for key in ("note", "path_basename"):
                            if key in entry:
                                _expect(_is_bounded_text(entry[key]), "Codex citation text is invalid")
                        if "path_sha256" in entry:
                            _expect(
                                isinstance(entry["path_sha256"], str)
                                and bool(SHA256_PATTERN.fullmatch(entry["path_sha256"])),
                                "Codex citation path digest is invalid",
                            )
                rollout_ids = citation.get("rolloutIds", [])
                _expect(
                    isinstance(rollout_ids, list)
                    and len(rollout_ids) <= 64
                    and all(_is_bounded_text(item) for item in rollout_ids),
                    "Codex citation rollout ids are invalid",
                )
        return
    if event_type == "task_started":
        _expect_bounded_text_fields(
            payload,
            ("turn_id", "started_at", "collaboration_mode_kind"),
            "Codex task start",
        )
        if "model_context_window" in payload:
            _expect(_is_number(payload["model_context_window"]), "Codex context window is invalid")
        return
    if event_type == "task_complete":
        _expect_bounded_text_fields(
            payload,
            ("turn_id", "started_at", "completed_at"),
            "Codex task completion",
        )
        for key in ("duration_ms", "first_output_latency_ms"):
            if key in payload:
                _expect(_is_number(payload[key]), f"Codex {key} is invalid")
        if "time_to_first_token_ms" in payload:
            # The first immutable capture conservatively masked this
            # credential-shaped name. Later projections use the safe alias.
            _expect(
                _is_legacy_redacted_number(payload["time_to_first_token_ms"]),
                "Codex time_to_first_token_ms is invalid",
            )
            _expect(
                "first_output_latency_ms" not in payload,
                "Codex task completion mixes legacy and current latency fields",
            )
        if "error" in payload:
            error = payload["error"]
            _expect(
                isinstance(error, dict)
                and set(error) <= {"present", "code", "type", "status"}
                and isinstance(error.get("present"), bool),
                "Codex task error is invalid",
            )
            if isinstance(error, dict):
                for key in ("code", "type", "status"):
                    if key in error:
                        _expect(
                            _is_bounded_text(error[key])
                            or isinstance(error[key], int) and not isinstance(error[key], bool),
                            "Codex task error field is invalid",
                        )
        return
    if event_type == "sub_agent_activity":
        _expect_bounded_text_fields(
            payload,
            ("agent_thread_id", "event_id", "kind"),
            "Codex sub-agent activity",
        )
        if "agent_path" in payload:
            _expect(_is_codex_path_value(payload["agent_path"]), "Codex agent path is invalid")
        if "occurred_at_ms" in payload:
            _expect(_is_number(payload["occurred_at_ms"]), "Codex sub-agent time is invalid")
        return
    if event_type == "item_completed":
        _expect_bounded_text_fields(
            payload, ("thread_id", "turn_id"), "Codex completed item"
        )
        for key in ("started_at_ms", "completed_at_ms"):
            if key in payload:
                _expect(_is_number(payload[key]), f"Codex item {key} is invalid")
        if "item" in payload:
            item = payload["item"]
            _expect(
                isinstance(item, dict)
                and set(item) <= {"agent_path", "agent_thread_id", "id", "kind", "type"},
                "Codex completed item descriptor is invalid",
            )
            if isinstance(item, dict):
                _expect_bounded_text_fields(
                    item,
                    tuple(key for key in item if key != "agent_path"),
                    "Codex completed item",
                )
                if "agent_path" in item:
                    _expect(_is_codex_path_value(item["agent_path"]), "Codex item path is invalid")
        return
    if event_type == "mcp_tool_call_end":
        _expect_bounded_text_fields(
            payload,
            (
                "call_id",
                "plugin_id",
                "action_name",
                "app_name",
                "connector_id",
                "link_id",
            ),
            "Codex MCP call",
        )
        if "duration" in payload:
            _expect(_is_number(payload["duration"]), "Codex MCP duration is invalid")
        if "read_only_hint" in payload:
            _expect(isinstance(payload["read_only_hint"], bool), "Codex MCP hint is invalid")
        if "invocation" in payload:
            invocation = payload["invocation"]
            _expect(
                isinstance(invocation, dict)
                and set(invocation) <= {"arguments", "server", "tool"},
                "Codex MCP invocation is invalid",
            )
            if isinstance(invocation, dict):
                _expect_bounded_text_fields(
                    invocation, ("server", "tool"), "Codex MCP invocation"
                )
                if "arguments" in invocation:
                    _expect(_is_bounded_json(invocation["arguments"]), "Codex MCP arguments are invalid")
        if "result" in payload:
            _expect(_is_bounded_json(payload["result"]), "Codex MCP result is invalid")
        return
    if event_type == "patch_apply_end":
        _expect_bounded_text_fields(
            payload,
            ("call_id", "turn_id", "status", "stdout", "stderr"),
            "Codex patch result",
        )
        if "success" in payload:
            _expect(isinstance(payload["success"], bool), "Codex patch success is invalid")
        if "changes_omitted_count" in payload:
            _expect(
                _is_non_negative_int(payload["changes_omitted_count"]),
                "Codex patch change count is invalid",
            )
        return
    if event_type == "web_search_end":
        _expect_bounded_text_fields(
            payload, ("call_id", "action", "query"), "Codex web result"
        )
        results = payload.get("results")
        _expect(isinstance(results, list) and len(results) <= 64, "Codex web results are invalid")
        if isinstance(results, list):
            for result in results:
                _expect(
                    isinstance(result, dict)
                    and set(result)
                    <= {"type", "ref_id", "domain", "url", "title", "snippet", "thumbnail_url"},
                    "Codex web result is not closed",
                )
                if not isinstance(result, dict):
                    continue
                _expect_bounded_text_fields(
                    result,
                    ("type", "ref_id", "domain", "title", "snippet"),
                    "Codex web result",
                )
                for key in ("url", "thumbnail_url"):
                    if key in result:
                        _expect(_is_safe_http_url(result[key]), "Codex web URL is invalid")
        return
    if event_type == "token_count":
        info = payload.get("info")
        _expect(isinstance(info, dict), "Codex token information is invalid")
        if isinstance(info, dict):
            _expect(
                set(info) <= {"last_token_usage", "total_token_usage", "model_context_window"},
                "Codex token information is not closed",
            )
            for key in ("last_token_usage", "total_token_usage"):
                if key in info:
                    usage = info[key]
                    _expect(
                        isinstance(usage, dict)
                        and set(usage)
                        <= {
                            "cached_input_tokens",
                            "input_tokens",
                            "output_tokens",
                            "reasoning_output_tokens",
                            "total_tokens",
                        }
                        and all(_is_number(item) for item in usage.values()),
                        "Codex token usage is invalid",
                    )
            if "model_context_window" in info:
                _expect(_is_number(info["model_context_window"]), "Codex context window is invalid")
        if "rate_limits" in payload:
            _verify_rate_limit_projection(payload["rate_limits"])
        return
    _expect(event_type == "turn_aborted", "Codex event type is invalid")
    _expect_bounded_text_fields(
        payload, ("turn_id", "started_at", "completed_at"), "Codex aborted turn"
    )
    if "duration_ms" in payload:
        _expect(_is_number(payload["duration_ms"]), "Codex aborted duration is invalid")
    if "reason" in payload:
        reason = payload["reason"]
        _expect(
            _is_bounded_text(reason)
            or isinstance(reason, dict)
            and set(reason) <= {"code", "kind", "type"}
            and all(_is_bounded_text(item) for item in reason.values()),
            "Codex aborted reason is invalid",
        )


def _verify_codex_projected_payload(
    source_type: str,
    payload: Mapping[str, Any],
    header: Mapping[str, Any],
    *,
    allowed_session_thread_ids: set[str] | frozenset[str] | None = None,
    session_lineage_metadata: Mapping[str, tuple[str, str | None]] | None = None,
    authoritative_forked_from_id_sha256: str | None = None,
    authoritative_session_meta: bool = False,
    projection_schema: str = CODEX_PROJECTION_SCHEMA,
) -> None:
    if source_type == "session_meta":
        _expect(set(payload) <= CODEX_SESSION_PAYLOAD_KEYS, "Codex session payload is not closed")
        allowed_lineage = set(
            {
                header["thread_id"],
                *(
                    (header.get("parent_thread_id"),)
                    if header.get("parent_thread_id") is not None
                    else ()
                ),
            }
            if allowed_session_thread_ids is None
            else allowed_session_thread_ids
        )
        _expect(
            header["thread_id"] in allowed_lineage,
            "Codex session lineage is incomplete",
        )
        thread_id = payload.get("id")
        _expect(isinstance(thread_id, str) and thread_id, "Codex session thread is invalid")
        if authoritative_session_meta:
            _expect(thread_id == header["thread_id"], "Codex session payload thread differs")
        effective_session_id = payload.get("session_id", thread_id)
        _expect(
            isinstance(effective_session_id, str)
            and effective_session_id == header["session_id"],
            "Codex session payload session differs",
        )
        parent_references: list[object] = []
        if "parent_thread_id" in payload:
            parent_references.append(payload["parent_thread_id"])
        parent_path = payload.get("agent_parent_path")
        if isinstance(parent_path, dict) and "parent_thread_id" in parent_path:
            parent_references.append(parent_path["parent_thread_id"])
        _expect(
            all(isinstance(parent, str) for parent in parent_references),
            "Codex session parent is invalid",
        )
        if authoritative_session_meta:
            expected_parent = header.get("parent_thread_id")
            if expected_parent is None:
                _expect(not parent_references, "Codex session payload parent differs")
            else:
                _expect(
                    bool(parent_references)
                    and all(parent == expected_parent for parent in parent_references),
                    "Codex session payload parent differs",
                )
        else:
            known_metadata = (
                session_lineage_metadata.get(thread_id)
                if session_lineage_metadata is not None
                else None
            )
            if thread_id in allowed_lineage:
                if known_metadata is None and thread_id == header["thread_id"]:
                    known_metadata = (
                        header["session_id"],
                        header.get("parent_thread_id"),
                    )
                _expect(
                    known_metadata is not None,
                    "Codex session restatement has no proven lineage metadata",
                )
                if known_metadata is not None:
                    known_session_id, known_parent_thread_id = known_metadata
                    _expect(
                        known_session_id == header["session_id"]
                        and effective_session_id == known_session_id,
                        "Codex session restatement has a different lineage session",
                    )
                    if known_parent_thread_id is None:
                        _expect(
                            not parent_references,
                            "Codex session restatement parent differs from its lineage",
                        )
                    else:
                        _expect(
                            bool(parent_references)
                            and all(
                                parent == known_parent_thread_id
                                for parent in parent_references
                            ),
                            "Codex session restatement parent differs from its lineage",
                        )
            else:
                _expect(
                    thread_id == header["session_id"]
                    and effective_session_id == header["session_id"]
                    and not parent_references
                    and (
                        session_lineage_metadata is None
                        or thread_id not in session_lineage_metadata
                    ),
                    "Codex session payload is outside the selected lineage",
                )

        forked_from_id = payload.get("forked_from_id")
        fork_digest = payload.get("forked_from_id_sha256")
        if projection_schema in {
            INTERMEDIATE_CODEX_PROJECTION_SCHEMA,
            CODEX_PROJECTION_SCHEMA,
        }:
            if forked_from_id is not None or fork_digest is not None:
                _expect(
                    isinstance(fork_digest, str)
                    and bool(SHA256_PATTERN.fullmatch(fork_digest)),
                    "Codex fork source digest is invalid",
                )
                if not authoritative_session_meta:
                    _expect(
                        authoritative_forked_from_id_sha256 is not None
                        and fork_digest == authoritative_forked_from_id_sha256,
                        "Codex fork source differs from the authoritative session record",
                    )
        else:
            _expect(
                projection_schema == LEGACY_CODEX_PROJECTION_SCHEMA,
                "Codex projection schema is invalid",
            )
            _expect(fork_digest is None, "legacy Codex projection has a fork digest")
            if forked_from_id is not None:
                _expect(
                    isinstance(forked_from_id, str)
                    and LEGACY_CODEX_FORK_ID_PATTERN.fullmatch(forked_from_id)
                    is not None,
                    "legacy Codex fork source is not provably lossless",
                )
        for key in (
            "id",
            "session_id",
            "parent_thread_id",
            "forked_from_id",
            "agent_nickname",
            "agent_role",
            "timestamp",
            "cli_version",
            "originator",
            "thread_source",
            "model_provider",
        ):
            if key in payload:
                _expect(
                    payload[key] is None or _is_bounded_text(payload[key]),
                    f"Codex session {key} is invalid",
                )
        if "agent_path" in payload:
            _expect(_is_codex_path_value(payload["agent_path"]), "Codex session agent path is invalid")
        if "agent_parent_path" in payload:
            parent_path = payload["agent_parent_path"]
            _expect(
                isinstance(parent_path, dict)
                and set(parent_path)
                <= {"parent_thread_id", "depth", "agent_path", "agent_nickname", "agent_role"},
                "Codex session parent path is invalid",
            )
            if isinstance(parent_path, dict):
                for key in ("parent_thread_id", "agent_nickname", "agent_role"):
                    if key in parent_path:
                        _expect(_is_bounded_text(parent_path[key]), "Codex parent field is invalid")
                if "depth" in parent_path:
                    _expect(_is_non_negative_int(parent_path["depth"]), "Codex parent depth is invalid")
                if "agent_path" in parent_path:
                    _expect(_is_codex_path_value(parent_path["agent_path"]), "Codex parent path is invalid")
        if "git" in payload:
            git = payload["git"]
            _expect(
                isinstance(git, dict)
                and set(git) <= {"commit_hash", "branch", "repository_url"},
                "Codex session Git metadata is invalid",
            )
            if isinstance(git, dict):
                _expect_bounded_text_fields(git, tuple(git), "Codex session Git")
        return
    if source_type == "response_item":
        response_type = payload.get("type")
        if response_type == "agent_message":
            _expect(
                set(payload)
                <= {"type", "author", "recipient", "status", "call_id", "content"},
                "Codex agent-message payload is not closed",
            )
            content = payload.get("content")
            _expect(isinstance(content, list), "Codex response content is not an array")
            _expect(
                all(
                    isinstance(item, dict)
                    and set(item) == {"type", "text"}
                    and item["type"] == "input_text"
                    for item in content
                ),
                "Codex response content is invalid",
            )
            _expect_bounded_text_fields(
                payload,
                ("author", "recipient", "status", "call_id"),
                "Codex response",
            )
            for item in content:
                _expect(_is_bounded_text(item["text"]), "Codex response text is invalid")
            return
        if response_type in CODEX_RESPONSE_CALL_TYPES:
            _expect(set(payload) <= CODEX_RESPONSE_CALL_KEYS, "Codex tool-call payload is not closed")
            _expect(
                isinstance(payload.get("name"), str) and payload["name"],
                "Codex tool-call name is invalid",
            )
            _expect_bounded_text_fields(
                payload,
                ("name", "namespace", "server", "call_id", "status"),
                "Codex tool call",
            )
            for key in ("input", "arguments"):
                if key in payload:
                    _expect(_is_bounded_json(payload[key]), f"Codex tool {key} is invalid")
            return
        if response_type in CODEX_RESPONSE_OUTPUT_TYPES:
            _expect(
                set(payload) <= CODEX_RESPONSE_OUTPUT_KEYS,
                "Codex tool-output payload is not closed",
            )
            output = payload.get("output")
            _expect(isinstance(output, list), "Codex tool output is not an array")
            for item in output:
                _expect(isinstance(item, dict), "Codex tool-output item is not an object")
                item_type = item.get("type")
                if item_type in {"input_text", "text"}:
                    _expect(
                        set(item) == {"type", "text"} and isinstance(item["text"], (str, dict)),
                        "Codex tool-output text item is invalid",
                    )
                    _expect(_is_bounded_text(item["text"]), "Codex tool-output text is invalid")
                    continue
                _expect(
                    set(item)
                    <= {"type", "detail", "media_type", "encoded_bytes", "sha256", "url"},
                    "Codex tool-output image descriptor is not closed",
                )
                encoded = item.get("encoded_bytes")
                object_digest = item.get("sha256")
                url = item.get("url")
                embedded = _is_non_negative_int(encoded) and isinstance(
                    object_digest, str
                ) and bool(SHA256_PATTERN.fullmatch(object_digest))
                linked = isinstance(url, str) and bool(url)
                _expect(embedded is not linked, "Codex tool-output image descriptor is invalid")
                if linked:
                    _expect(_is_safe_http_url(url), "Codex tool-output image URL is invalid")
                for key in ("type", "detail", "media_type"):
                    if key in item:
                        _expect(_is_bounded_text(item[key]), "Codex image descriptor is invalid")
            return
        _expect(False, "response message or reasoning leaked into the projection")
        return
    if source_type == "event_msg":
        event_type = payload.get("type")
        _expect(
            isinstance(event_type, str) and event_type in CODEX_EVENT_PAYLOAD_KEYS,
            "excluded or unknown Codex event leaked into the projection",
        )
        _expect(
            set(payload) <= CODEX_EVENT_PAYLOAD_KEYS[event_type],
            "Codex event payload is not closed",
        )
        _verify_codex_event_payload_domains(payload)
        return
    _expect(
        source_type == "inter_agent_communication_metadata"
        and set(payload) <= {"trigger_turn"},
        "Codex inter-agent payload is not closed",
    )
    if "trigger_turn" in payload:
        _expect(
            _is_bounded_text(payload["trigger_turn"])
            or _is_non_negative_int(payload["trigger_turn"]),
            "Codex inter-agent trigger is invalid",
        )


def _verify_codex_object_metadata(
    item: Mapping[str, Any],
    *,
    role: str,
    media_type: str,
    secret_scan: str,
    label: str,
) -> None:
    _expect(
        isinstance(item, Mapping) and set(item) == OBJECT_KEYS,
        f"{label} object record is not closed",
    )
    _expect(item["role"] == role, f"{label} object role is invalid")
    _expect(item["media_type"] == media_type, f"{label} object media type is invalid")
    _expect(item["opaque"] is False, f"{label} object opacity is invalid")
    _expect(item["secret_scan"] == secret_scan, f"{label} object secret scan is invalid")
    _expect(item["secret_scan_performed"] is True, f"{label} object was not secret-scanned")
    _expect(item["sensitivity"] == "owner-only-redacted", f"{label} object is not redacted")
    _expect(
        item["public_projection_eligible"] is False,
        f"{label} object cannot be public-projection eligible",
    )


def _is_bound_codex_projection_gzip(
    archive_format: str | None,
    claims: Sequence[tuple[Mapping[str, Any], str]],
) -> bool:
    """Identify only gzip objects committed to full projection verification."""

    if archive_format != "gzip" or not claims:
        return False
    if not all(
        item["role"] == "codex-user-visible-projection-gzip"
        and source_kind == "codex-user-visible-projection"
        for item, source_kind in claims
    ):
        return False
    for item, _ in claims:
        _verify_codex_object_metadata(
            item,
            role="codex-user-visible-projection-gzip",
            media_type="application/gzip",
            secret_scan="fixed-length-high-confidence-redaction-completed",
            label="Codex projection",
        )
    return True


def _verify_codex_manifest_item(item: Mapping[str, Any]) -> None:
    _expect(
        isinstance(item, dict) and set(item) == CODEX_MANIFEST_FILE_KEYS,
        "manifest file is not closed",
    )
    for key in ("thread_id", "session_id", "source_identity"):
        _expect(isinstance(item[key], str) and item[key], f"manifest {key} is invalid")
    _expect(
        item["parent_thread_id"] is None
        or isinstance(item["parent_thread_id"], str) and item["parent_thread_id"],
        "manifest parent thread id is invalid",
    )
    for key in (
        "source_path_sha256",
        "source_identity_sha256",
        "raw_source_sha256",
        "uncompressed_sha256",
    ):
        _expect(
            isinstance(item[key], str) and bool(SHA256_PATTERN.fullmatch(item[key])),
            f"manifest {key} is invalid",
        )
    _expect(item["disposition"] in {"captured", "excluded"}, "manifest disposition is invalid")
    if item["disposition"] == "captured":
        _expect(item["reason"] is None, "captured manifest file has an exclusion reason")
        _expect(
            isinstance(item["object_sha256"], str)
            and bool(SHA256_PATTERN.fullmatch(item["object_sha256"])),
            "captured manifest object digest is invalid",
        )
        _expect(_is_positive_int(item["object_bytes"]), "captured manifest object size is invalid")
    else:
        _expect(
            isinstance(item["reason"], str) and item["reason"],
            "excluded manifest file has no reason",
        )
        _expect(
            item["object_sha256"] is None and item["object_bytes"] is None,
            "excluded projection binds an object",
        )
    _expect(_is_positive_int(item["uncompressed_bytes"]), "manifest uncompressed size is invalid")
    _expect(_is_non_negative_int(item["retained_records"]), "manifest retained count is invalid")
    _verify_count_mapping(item["skipped_record_types"], "manifest skipped-record counts")
    _expect(
        isinstance(item["redaction_categories"], list)
        and all(
            isinstance(category, str) and category
            for category in item["redaction_categories"]
        ),
        "manifest redaction categories are invalid",
    )
    _expect(
        item["redaction_categories"] == sorted(set(item["redaction_categories"])),
        "manifest redaction categories are invalid",
    )
    _expect(_is_non_negative_int(item["redaction_count"]), "manifest redaction count is invalid")


def _verify_codex_final_observation(
    item: Mapping[str, Any],
    source_event: Mapping[str, Any],
) -> None:
    final_stat = item["source_stat_final_observation"]
    _expect(
        isinstance(final_stat, dict) and set(final_stat) == SOURCE_STAT_KEYS,
        "Codex final source observation is invalid",
    )
    _expect(
        all(
            isinstance(value, int) and not isinstance(value, bool)
            for value in final_stat.values()
        ),
        "Codex final source observation is invalid",
    )
    changed = item["source_changed_by_final_observation"]
    _expect(isinstance(changed, bool), "Codex final source mutation marker is invalid")
    source = source_event["source"]
    source_stat_before = source["source_stat_before"]
    source_stat_after = source["source_stat_after"]
    _expect(
        isinstance(source_stat_before, dict) and isinstance(source_stat_after, dict),
        "Codex projection lacks source stat evidence",
    )
    _expect(
        changed is (source_stat_after != final_stat),
        "Codex final source mutation marker differs from its stats",
    )
    for key in ("device", "inode", "mode", "links", "owner_uid"):
        _expect(
            source_stat_after[key] == source_stat_before[key],
            "Codex snapshot source identity changed during acquisition",
        )
        _expect(
            final_stat[key] == source_stat_after[key],
            "Codex final source identity differs from its snapshot",
        )
    _expect(
        final_stat["bytes"] >= source_stat_before["bytes"],
        "Codex final source observation is truncated",
    )


def _verify_codex_manifest_event_metadata(event: Mapping[str, Any]) -> Mapping[str, Any]:
    _expect(event["disposition"]["status"] == "captured", "Codex generation manifest is unavailable")
    _expect(len(event["objects"]) == 1, "Codex generation manifest must bind one object")
    manifest_source = event["source"]
    _expect(
        manifest_source["snapshot_method"] == "derived-generation-manifest",
        "Codex generation snapshot method differs",
    )
    _expect(
        manifest_source["redaction_mode"]
        == "generated-from-owner-only-redacted-projections",
        "Codex generation redaction mode differs",
    )
    manifest_object = event["objects"][0]
    _verify_codex_object_metadata(
        manifest_object,
        role="codex-thread-closure-generation-manifest",
        media_type="application/json",
        secret_scan="high-confidence-text-scan-passed",
        label="Codex generation manifest",
    )
    _expect(
        _is_positive_int(manifest_object["bytes"])
        and manifest_object["bytes"] <= MAX_METADATA_BYTES,
        "Codex generation manifest exceeds the byte boundary",
    )
    return manifest_object


def _codex_value_has_only_depth_overflow(
    value: object,
    *,
    maximum_depth: int = 8,
    maximum_nodes: int = 100_000,
) -> bool:
    """Prove that depth, not the aggregate node safety cap, caused omission."""

    stack: list[tuple[object, int]] = [(value, 0)]
    visited = 0
    depth_exceeded = False
    while stack:
        item, depth = stack.pop()
        visited += 1
        if visited > maximum_nodes:
            return False
        if isinstance(item, list):
            if depth >= maximum_depth:
                depth_exceeded = True
            stack.extend((child, depth + 1) for child in item)
        elif isinstance(item, dict):
            if depth >= maximum_depth:
                depth_exceeded = True
            stack.extend((child, depth + 1) for child in item.values())
    return depth_exceeded


def _codex_projection_record_has_only_wrapper_depth_drift(
    value: Mapping[str, object],
    normalised_record: object,
) -> bool:
    """Recognise historical wrapper-depth drift without bypassing child redaction."""

    if (
        value.get("record") != "projected-rollout-record"
        or normalised_record
        != {"projection_omitted": True, "reason": "maximum-depth"}
        or not _codex_value_has_only_depth_overflow(value)
    ):
        return False
    for child in value.values():
        if _codex_value_exceeds_depth(child):
            return False
        normalised_child, _, _ = _redact_codex_projection_value(child)
        if normalised_child != child:
            return False
    return True


def _historical_codex_projection_record_has_only_local_path_drift(
    value: Mapping[str, object],
    normalised_record: object,
    redaction_categories: Sequence[str],
    redaction_count: int,
) -> bool:
    """Bound the owner-only v1/v2 message-path gap superseded by v3 capture."""

    if (
        value.get("record") != "projected-rollout-record"
        or value.get("source_type") != "event_msg"
        or redaction_categories != ["local-path"]
        or redaction_count < 1
        or not isinstance(normalised_record, dict)
        or set(normalised_record) != set(value)
    ):
        return False
    payload = value.get("payload")
    normalised_payload = normalised_record.get("payload")
    if (
        not isinstance(payload, dict)
        or not isinstance(normalised_payload, dict)
        or payload.get("type") != "user_message"
        or set(payload) != set(normalised_payload)
        or not isinstance(payload.get("message"), str)
        or not isinstance(normalised_payload.get("message"), str)
    ):
        return False
    expected_message, path_count = _sanitise_codex_local_paths_in_text(
        payload["message"]
    )
    if (
        path_count != redaction_count
        or expected_message != normalised_payload["message"]
    ):
        return False
    if any(
        value[key] != normalised_record[key]
        for key in value
        if key != "payload"
    ):
        return False
    return all(
        payload[key] == normalised_payload[key]
        for key in payload
        if key != "message"
    )


def _legacy_codex_omission_residual_is_bounded(
    residual_source_bytes: int,
    omitted_records: int,
) -> bool:
    """Require every unbound legacy source record to occupy at least one byte."""

    return (
        omitted_records > 0
        and omitted_records <= residual_source_bytes
        <= MAX_CODEX_LINE_BYTES * omitted_records
    )


def _verify_codex_projection(
    path: Path,
    manifest_item: Mapping[str, Any],
    source_event: Mapping[str, Any],
    *,
    allowed_session_thread_ids: set[str] | frozenset[str] | None = None,
    session_lineage_metadata: Mapping[str, tuple[str, str | None]] | None = None,
    required_projection_schema: str | None = None,
    read_descriptor: int | None = None,
    progress_bytes_function: Callable[[int], None] | None = None,
) -> None:
    source = source_event["source"]
    _expect(source["kind"] == "codex-user-visible-projection", "Codex source kind differs")
    _expect(
        source["snapshot_method"] == "streamed-user-visible-projection",
        "Codex projection snapshot method differs",
    )
    _expect(
        source["redaction_mode"] == "fixed-length-high-confidence-projection-redaction",
        "Codex projection redaction mode differs",
    )
    _expect(
        source["collection_generation_sha256"] is None and source["collection_window"] is None,
        "Codex projection carries generation metadata",
    )
    source_stat_before = source["source_stat_before"]
    source_stat_after = source["source_stat_after"]
    stat_digest = hashlib.sha256(canonical_json(source_stat_before)).hexdigest()
    expected_identity = (
        f"codex-user-visible-projection:thread:{manifest_item['thread_id']}:"
        f"session:{manifest_item['session_id']}:"
        f"path-sha256:{manifest_item['source_path_sha256']}:"
        f"source-sha256:{manifest_item['raw_source_sha256']}:"
        f"source-stat-sha256:{stat_digest}:"
        f"projection-sha256:{manifest_item['object_sha256']}"
    )
    _expect(source["identity"] == expected_identity, "Codex projection identity differs")
    digest = hashlib.sha256()
    total = 0
    header: dict[str, Any] | None = None
    footer: dict[str, Any] | None = None
    skipped: dict[str, int] = {}
    retained = 0
    source_line = 0
    source_bytes = 0
    session_meta_records = 0
    legacy_unbound_maximum_depth_records = 0
    authoritative_forked_from_id_sha256: str | None = None
    try:
        if read_descriptor is None:
            compressed_stream = path.open("rb")
        else:
            os.lseek(read_descriptor, 0, os.SEEK_SET)
            compressed_stream = os.fdopen(os.dup(read_descriptor), "rb")
        with compressed_stream:
            with gzip.GzipFile(fileobj=compressed_stream, mode="rb") as stream:
                line_number = 0
                while True:
                    raw = stream.readline(16 * 1024 * 1024 + 1)
                    if not raw:
                        break
                    line_number += 1
                    _expect(len(raw) <= 16 * 1024 * 1024, "Codex projection line is oversized")
                    total += len(raw)
                    _expect(total <= 2 * 1024 * 1024 * 1024, "Codex projection is oversized")
                    digest.update(raw)
                    value = parse_json(raw, f"Codex projection line {line_number}")
                    _expect(isinstance(value, dict), "Codex projection line is not an object")
                    _expect(raw == canonical_json(value), "Codex projection line is not canonical")
                    (
                        normalised_record,
                        record_redaction_categories,
                        record_redaction_count,
                    ) = _redact_codex_projection_value(value)
                    historical_wrapper_depth_artefact = bool(
                        header is not None
                        and header.get("schema")
                        in {
                            LEGACY_CODEX_PROJECTION_SCHEMA,
                            INTERMEDIATE_CODEX_PROJECTION_SCHEMA,
                        }
                        and _codex_projection_record_has_only_wrapper_depth_drift(
                            value,
                            normalised_record,
                        )
                    )
                    historical_local_path_drift = bool(
                        header is not None
                        and header.get("schema")
                        in {
                            LEGACY_CODEX_PROJECTION_SCHEMA,
                            INTERMEDIATE_CODEX_PROJECTION_SCHEMA,
                        }
                        and _historical_codex_projection_record_has_only_local_path_drift(
                            value,
                            normalised_record,
                            record_redaction_categories,
                            record_redaction_count,
                        )
                    )
                    _expect(
                        normalised_record == value
                        or historical_wrapper_depth_artefact
                        or historical_local_path_drift,
                        "Codex projection record bypasses capture redaction",
                    )
                    try:
                        raw.decode("utf-8")
                    except UnicodeDecodeError as error:
                        raise EvidenceVerificationError("Codex projection is not UTF-8") from error
                    _expect(
                        UNREDACTABLE_SECRET_PATTERN.search(raw) is None,
                        "Codex projection contains an unredactable private key marker",
                    )
                    _verify_fixed_length_projection_redactions(raw)
                    record_type = value.get("record")
                    if record_type == "projection-header":
                        _expect(header is None and line_number == 1, "Codex projection header is misplaced")
                        _expect(
                            set(value)
                            == {
                                "schema",
                                "record",
                                "thread_id",
                                "session_id",
                                "parent_thread_id",
                                "source_path_sha256",
                                "boundaries",
                            },
                            "Codex projection header is not closed",
                        )
                        _expect(
                            value["schema"]
                            in {
                                LEGACY_CODEX_PROJECTION_SCHEMA,
                                INTERMEDIATE_CODEX_PROJECTION_SCHEMA,
                                CODEX_PROJECTION_SCHEMA,
                            },
                            "Codex projection schema is invalid",
                        )
                        _expect(value["boundaries"] == BOUNDARIES, "Codex projection crosses its boundary")
                        _expect(value["thread_id"] == manifest_item["thread_id"], "Codex thread id differs")
                        _expect(value["session_id"] == manifest_item["session_id"], "Codex session id differs")
                        _expect(
                            value["parent_thread_id"] == manifest_item["parent_thread_id"],
                            "Codex parent thread id differs",
                        )
                        _expect(
                            value["source_path_sha256"] == manifest_item["source_path_sha256"],
                            "Codex source path digest differs",
                        )
                        if (
                            required_projection_schema is not None
                            and value["schema"] != required_projection_schema
                        ):
                            raise _CodexProjectionSchemaMismatch(
                                "prior Codex projection schema is incompatible"
                            )
                        header = value
                        if progress_bytes_function is not None:
                            progress_bytes_function(len(raw))
                        continue
                    _expect(header is not None, "Codex projection has no leading header")
                    _expect(footer is None, "Codex projection has records after its footer")
                    if value == {
                        "projection_omitted": True,
                        "reason": "maximum-depth",
                    }:
                        _expect(
                            header["schema"] == LEGACY_CODEX_PROJECTION_SCHEMA,
                            "current Codex projection has an unbound omission",
                        )
                        source_line += 1
                        retained += 1
                        legacy_unbound_maximum_depth_records += 1
                        if progress_bytes_function is not None:
                            progress_bytes_function(len(raw))
                        continue
                    if record_type == "projection-footer":
                        _expect(
                            set(value)
                            == {
                                "schema",
                                "record",
                                "source_sha256",
                                "source_bytes",
                                "source_stat_before",
                                "source_stat_after",
                                "source_records",
                                "retained_records",
                                "skipped_record_types",
                            },
                            "Codex projection footer is not closed",
                        )
                        _expect(
                            value["schema"] == header["schema"],
                            "Codex footer schema is invalid",
                        )
                        _expect(
                            isinstance(value["source_sha256"], str)
                            and bool(SHA256_PATTERN.fullmatch(value["source_sha256"])),
                            "Codex footer source digest is invalid",
                        )
                        _expect(
                            value["source_sha256"] == manifest_item["raw_source_sha256"],
                            "Codex raw-source digest differs",
                        )
                        _expect(_is_non_negative_int(value["source_bytes"]), "Codex source size is invalid")
                        _expect(
                            value["source_stat_before"] == source_stat_before
                            and value["source_stat_after"] == source_stat_after,
                            "Codex footer source stats differ",
                        )
                        _expect(
                            value["source_bytes"] == source_stat_before["bytes"],
                            "Codex footer source size differs from its snapshot stat",
                        )
                        _expect(
                            _is_non_negative_int(value["source_records"]),
                            "Codex source-record count is invalid",
                        )
                        _expect(
                            _is_non_negative_int(value["retained_records"]),
                            "Codex retained-record count is invalid",
                        )
                        _verify_count_mapping(
                            value["skipped_record_types"],
                            "Codex footer skipped-record counts",
                        )
                        _expect(value["retained_records"] == retained, "Codex retained-record count differs")
                        _expect(value["skipped_record_types"] == skipped, "Codex skipped-record count differs")
                        _expect(value["source_records"] == source_line, "Codex source-record count differs")
                        _expect(
                            value["source_records"] == retained + sum(skipped.values()),
                            "Codex footer record accounting differs",
                        )
                        if legacy_unbound_maximum_depth_records:
                            residual_source_bytes = value["source_bytes"] - source_bytes
                            _expect(
                                _legacy_codex_omission_residual_is_bounded(
                                    residual_source_bytes,
                                    legacy_unbound_maximum_depth_records,
                                ),
                                "legacy Codex omitted source-byte residual is invalid",
                            )
                        else:
                            _expect(
                                value["source_bytes"] == source_bytes,
                                "Codex footer source-byte total differs",
                            )
                        _expect(session_meta_records >= 1, "Codex projection has no session record")
                        footer = value
                        if progress_bytes_function is not None:
                            progress_bytes_function(len(raw))
                        continue
                    _expect(
                        record_type
                        in {
                            "projected-rollout-record",
                            "excluded-rollout-record",
                            "unsupported-rollout-record",
                        },
                        "Codex projection record type is invalid",
                    )
                    source_line += 1
                    _expect(
                        _is_positive_int(value.get("source_line"))
                        and value["source_line"] == source_line,
                        "Codex source-line sequence differs",
                    )
                    _expect(
                        isinstance(value.get("source_line_sha256"), str)
                        and bool(SHA256_PATTERN.fullmatch(value["source_line_sha256"])),
                        "Codex source-line digest is invalid",
                    )
                    _expect(_is_positive_int(value.get("source_bytes")), "Codex source-line size is invalid")
                    source_bytes += value["source_bytes"]
                    if record_type == "projected-rollout-record":
                        _expect(
                            set(value)
                            in (
                                {
                                    "record",
                                    "source_line",
                                    "source_line_sha256",
                                    "source_bytes",
                                    "source_type",
                                    "payload",
                                },
                                {
                                    "record",
                                    "source_line",
                                    "source_line_sha256",
                                    "source_bytes",
                                    "source_type",
                                    "payload",
                                    "timestamp",
                                },
                            ),
                            "projected Codex record is not closed",
                        )
                        _expect(isinstance(value["payload"], dict), "projected Codex payload is not an object")
                        if (
                            isinstance(normalised_record, dict)
                            and "payload" in normalised_record
                        ):
                            normalised_payload = normalised_record["payload"]
                        elif historical_wrapper_depth_artefact:
                            # The wrapper compatibility proof independently
                            # normalises and checks every direct child.
                            normalised_payload = value["payload"]
                        else:
                            normalised_payload = None
                        _expect(
                            normalised_payload == value["payload"]
                            or historical_local_path_drift,
                            "Codex projection payload bypasses capture redaction",
                        )
                        _expect(
                            not _contains_excluded_projection_key(value["payload"]),
                            "Codex projection contains an excluded internal-state field",
                        )
                        _expect(
                            value["source_type"]
                            in {
                                "session_meta",
                                "response_item",
                                "event_msg",
                                "inter_agent_communication_metadata",
                            },
                            "projected Codex source type is invalid",
                        )
                        if "timestamp" in value:
                            _expect(
                                _is_bounded_text(value["timestamp"]),
                                "Codex projected timestamp is invalid",
                            )
                        if value["source_type"] == "session_meta":
                            session_meta_records += 1
                            if session_meta_records == 1:
                                _expect(source_line == 1, "first Codex session record is misplaced")
                                fork_digest = value["payload"].get(
                                    "forked_from_id_sha256"
                                )
                                if isinstance(fork_digest, str):
                                    authoritative_forked_from_id_sha256 = fork_digest
                        _verify_codex_projected_payload(
                            value["source_type"],
                            value["payload"],
                            header,
                            allowed_session_thread_ids=allowed_session_thread_ids,
                            session_lineage_metadata=session_lineage_metadata,
                            authoritative_forked_from_id_sha256=(
                                authoritative_forked_from_id_sha256
                            ),
                            authoritative_session_meta=(
                                value["source_type"] == "session_meta"
                                and session_meta_records == 1
                            ),
                            projection_schema=header["schema"],
                        )
                        retained += 1
                    else:
                        _expect(
                            set(value)
                            == {
                                "record",
                                "source_line",
                                "source_line_sha256",
                                "source_bytes",
                                "source_type",
                            },
                            "Codex excluded/unsupported stub is not closed",
                        )
                        skipped_type = value["source_type"]
                        _expect(isinstance(skipped_type, str) and skipped_type, "Codex stub type is invalid")
                        skipped[skipped_type] = skipped.get(skipped_type, 0) + 1
                    if progress_bytes_function is not None:
                        progress_bytes_function(len(raw))
    except (OSError, EOFError) as error:
        raise EvidenceVerificationError("Codex projection gzip is invalid") from error
    _expect(header is not None and footer is not None, "Codex projection is incomplete")
    _expect(digest.hexdigest() == manifest_item["uncompressed_sha256"], "uncompressed digest differs")
    _expect(total == manifest_item["uncompressed_bytes"], "uncompressed byte count differs")
    _expect(retained == manifest_item["retained_records"], "manifest retained-record count differs")
    _expect(skipped == manifest_item["skipped_record_types"], "manifest skipped-record count differs")


def _read_codex_manifest(
    path: Path,
    expected_bytes: object,
    *,
    read_descriptor: int | None = None,
) -> bytes:
    _expect(
        _is_positive_int(expected_bytes) and expected_bytes <= MAX_METADATA_BYTES,
        "Codex generation manifest exceeds the byte boundary",
    )
    if read_descriptor is None:
        metadata = path.stat()
        _expect(metadata.st_size == expected_bytes, "Codex manifest object size differs")
        _expect(metadata.st_size <= MAX_METADATA_BYTES, "Codex manifest object is oversized")
        with path.open("rb") as stream:
            raw = stream.read(MAX_METADATA_BYTES + 1)
    else:
        metadata = os.fstat(read_descriptor)
        _expect(metadata.st_size == expected_bytes, "Codex manifest object size differs")
        _expect(metadata.st_size <= MAX_METADATA_BYTES, "Codex manifest object is oversized")
        os.lseek(read_descriptor, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        total = 0
        while chunk := os.read(
            read_descriptor,
            min(1024 * 1024, MAX_METADATA_BYTES + 1 - total),
        ):
            chunks.append(chunk)
            total += len(chunk)
            _expect(total <= MAX_METADATA_BYTES, "Codex manifest object is oversized")
        raw = b"".join(chunks)
    _expect(len(raw) <= MAX_METADATA_BYTES, "Codex manifest object grew while being read")
    _expect(len(raw) == expected_bytes, "Codex manifest object size differs")
    return raw


def _verify_codex_projections_parallel(
    tasks: Sequence[
        tuple[
            str,
            Path,
            Mapping[str, Any],
            Mapping[str, Any],
            set[str] | frozenset[str],
            Mapping[str, tuple[str, str | None]],
        ]
    ],
    *,
    workers: int,
    progress_bytes_function: Callable[[int], None] | None,
    completed_function: Callable[[str], None],
) -> None:
    """Verify independent projections concurrently and raise errors in input order."""

    if not tasks:
        return
    context = multiprocessing.get_context("spawn")
    progress_queue = context.Queue(maxsize=workers * 2)
    futures: dict[concurrent.futures.Future[None], tuple[int, str]] = {}
    errors: list[tuple[int, Exception]] = []
    callback_error: Exception | None = None

    def drain_progress() -> None:
        nonlocal callback_error
        while True:
            try:
                count = progress_queue.get_nowait()
            except queue.Empty:
                break
            if progress_bytes_function is not None and callback_error is None:
                try:
                    progress_bytes_function(count)
                except Exception as error:
                    callback_error = error

    try:
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=workers,
            mp_context=context,
            initializer=_initialise_codex_projection_worker,
            initargs=(progress_queue,),
        ) as executor:
            next_index = 0
            pending: set[concurrent.futures.Future[None]] = set()

            def submit_available() -> None:
                nonlocal next_index
                maximum_in_flight = workers * 2
                while len(pending) < maximum_in_flight and next_index < len(tasks):
                    task = tasks[next_index]
                    identity, path, item, source_event, lineage, session_metadata = task
                    future = executor.submit(
                        _verify_codex_projection_worker,
                        path,
                        item,
                        source_event,
                        lineage,
                        session_metadata,
                        CODEX_VERIFICATION_PROGRESS_BYTES,
                    )
                    futures[future] = (next_index, identity)
                    pending.add(future)
                    next_index += 1

            submit_available()
            while pending:
                done, remaining = concurrent.futures.wait(
                    pending,
                    timeout=0.25,
                    return_when=concurrent.futures.FIRST_COMPLETED,
                )
                pending = set(remaining)
                drain_progress()
                for future in done:
                    index, identity = futures.pop(future)
                    try:
                        future.result()
                    except Exception as error:  # re-raised deterministically below
                        errors.append((index, error))
                    else:
                        if callback_error is not None:
                            continue
                        try:
                            completed_function(identity)
                        except Exception as error:
                            callback_error = error
                submit_available()
        drain_progress()
    except (OSError, RuntimeError) as error:
        raise EvidenceVerificationError(
            "Codex projection worker pool failed closed"
        ) from error
    finally:
        progress_queue.close()
        progress_queue.join_thread()
    if callback_error is not None:
        raise EvidenceVerificationError(
            "Codex projection progress reporting failed closed"
        ) from None
    if errors:
        error = min(errors, key=lambda item: item[0])[1]
        if isinstance(error, EvidenceVerificationError):
            raise error
        raise EvidenceVerificationError("Codex projection worker failed closed") from error


def _verify_codex_generations(
    events: Sequence[Mapping[str, Any]],
    observed: Mapping[str, Path],
    *,
    required_projection_schema: str | None = None,
    observed_descriptors: Mapping[str, int] | None = None,
    progress_function: Callable[[Mapping[str, object]], None] | None = None,
    workers: int = 1,
) -> bool:
    _expect(
        isinstance(workers, int)
        and not isinstance(workers, bool)
        and MIN_CODEX_VERIFICATION_WORKERS
        <= workers
        <= MAX_CODEX_VERIFICATION_WORKERS,
        "Codex verification worker count is invalid",
    )
    parallel_projection_verification = bool(
        workers > 1
        and required_projection_schema is None
        and observed_descriptors is None
    )
    by_identity = {event["source"]["identity"]: event for event in events}
    projection_events = {
        identity: event
        for identity, event in by_identity.items()
        if event["source"]["kind"] == "codex-user-visible-projection"
    }
    manifest_events = [
        event
        for event in events
        if event["source"]["kind"] == "codex-thread-closure-generation-manifest"
    ]
    referenced: set[str] = set()
    projection_schema_compatible = True
    captured_projection_seen = False
    completed_projection_identities: set[str] = set()
    total_projections = len(projection_events)

    started_at = time.monotonic()
    last_progress_at = started_at
    completed_projection_bytes = 0
    last_progress_bytes = 0
    parallel_tasks: list[
        tuple[
            str,
            Path,
            Mapping[str, Any],
            Mapping[str, Any],
            set[str] | frozenset[str],
            Mapping[str, tuple[str, str | None]],
        ]
    ] = []

    def report_progress(stage: str, *, observed_at: float | None = None) -> None:
        if progress_function is None:
            return
        current = time.monotonic() if observed_at is None else observed_at
        progress_function(
            {
                "stage": stage,
                "completed_projections": len(completed_projection_identities),
                "total_projections": total_projections,
                "completed_projection_bytes": completed_projection_bytes,
                "elapsed_seconds": round(max(0.0, current - started_at), 3),
            }
        )

    def advance_projection_bytes(count: int) -> None:
        nonlocal completed_projection_bytes, last_progress_at, last_progress_bytes
        completed_projection_bytes += count
        current = time.monotonic()
        if (
            completed_projection_bytes - last_progress_bytes
            >= CODEX_VERIFICATION_PROGRESS_BYTES
            or current - last_progress_at >= CODEX_VERIFICATION_PROGRESS_SECONDS
        ):
            report_progress("codex-verification-progress", observed_at=current)
            last_progress_bytes = completed_projection_bytes
            last_progress_at = current

    def complete_projection(identity: str) -> None:
        nonlocal last_progress_at, last_progress_bytes
        completed_projection_identities.add(identity)
        completed_projections = len(completed_projection_identities)
        if (
            progress_function is not None
            and completed_projections < total_projections
            and completed_projections % CODEX_VERIFICATION_PROGRESS_INTERVAL == 0
        ):
            current = time.monotonic()
            report_progress("codex-verification-progress", observed_at=current)
            last_progress_bytes = completed_projection_bytes
            last_progress_at = current

    if progress_function is not None and total_projections:
        report_progress("codex-verification-start", observed_at=started_at)
    for event in manifest_events:
        manifest_object = _verify_codex_manifest_event_metadata(event)
        manifest_path = observed.get(manifest_object["sha256"])
        _expect(manifest_path is not None, "Codex generation manifest object is missing")
        if manifest_path is None:  # pragma: no cover - narrowed by the fail-closed check
            raise EvidenceVerificationError("Codex generation manifest object is missing")
        raw = _read_codex_manifest(
            manifest_path,
            manifest_object["bytes"],
            read_descriptor=(
                observed_descriptors[manifest_object["sha256"]]
                if observed_descriptors is not None
                else None
            ),
        )
        manifest = parse_json(raw, "Codex generation manifest")
        _expect(isinstance(manifest, dict), "Codex generation manifest is not an object")
        _expect(set(manifest) == CODEX_MANIFEST_KEYS, "Codex generation manifest is not closed")
        _expect(raw == canonical_json(manifest, pretty=True), "Codex generation manifest is not canonical")
        _expect(manifest["schema"] == CODEX_GENERATION_SCHEMA, "Codex generation schema is invalid")
        _expect(manifest["boundaries"] == BOUNDARIES, "Codex generation crosses its boundary")
        _expect(
            manifest["selection_rule"]
            == "target-and-transitive-descendants-by-parent-thread-id",
            "Codex generation selection rule is invalid",
        )
        _expect(
            isinstance(manifest["thread_id"], str) and manifest["thread_id"],
            "Codex generation thread id is invalid",
        )
        files = manifest["files"]
        _expect(isinstance(files, list) and files, "Codex generation has no files")
        _expect(
            _is_positive_int(manifest["selected_file_count"])
            and manifest["selected_file_count"] == len(files),
            "Codex selected-file count differs",
        )
        parents: dict[str, str | None] = {}
        session_metadata: dict[str, tuple[str, str | None]] = {}
        session_lineages: dict[str, frozenset[str]] = {}
        for item in files:
            _verify_codex_manifest_item(item)
            item_thread = item["thread_id"]
            _expect(
                item_thread not in parents,
                "Codex generation repeats a thread",
            )
            parents[item_thread] = item["parent_thread_id"]
            session_metadata[item_thread] = (
                item["session_id"],
                item["parent_thread_id"],
            )
        for item in files:
            item_thread = item["thread_id"]
            allowed = {item_thread}
            visited: set[str] = set()
            current = item_thread
            while current in parents:
                _expect(
                    current not in visited,
                    "Codex generation contains a parent cycle",
                )
                visited.add(current)
                parent = parents[current]
                _expect(parent != current, "Codex generation contains a self-parent edge")
                if parent is None:
                    break
                allowed.add(parent)
                current = parent
            _expect(
                item["session_id"] not in parents
                or item["session_id"] in allowed,
                "Codex session alias collides with a selected non-ancestor thread",
            )
            session_lineages[item_thread] = frozenset(allowed)
        window = manifest["collection_window"]
        _expect(
            isinstance(window, dict)
            and set(window) == {"start_utc", "end_utc", "selected_files", "selection_rule"},
            "Codex collection window is invalid",
        )
        _expect(
            window["selection_rule"] == manifest["selection_rule"],
            "Codex collection-window selection rule differs",
        )
        _expect(
            _is_positive_int(window["selected_files"])
            and window["selected_files"] == len(files),
            "Codex collection-window selected-file count differs",
        )
        _expect(
            isinstance(window["start_utc"], str) and isinstance(window["end_utc"], str),
            "Codex collection-window times are invalid",
        )
        _expect(
            parse_time(window["start_utc"], "Codex collection start")
            <= parse_time(window["end_utc"], "Codex collection end"),
            "Codex collection window is reversed",
        )
        _verify_count_mapping(
            manifest["aggregate_skipped_record_types"],
            "Codex aggregate skipped-record counts",
        )
        generation_material = {
            "schema": CODEX_GENERATION_SCHEMA,
            "thread_id": manifest["thread_id"],
            "selection_rule": manifest["selection_rule"],
            "files": files,
            "boundaries": BOUNDARIES,
        }
        generation = hashlib.sha256(canonical_json(generation_material)).hexdigest()
        _expect(
            generation == manifest["collection_generation_sha256"],
            "Codex collection generation digest differs",
        )
        _expect(
            event["source"]["collection_generation_sha256"] == generation,
            "Codex manifest source generation differs",
        )
        _expect(
            event["source"]["collection_window"] == manifest["collection_window"],
            "Codex manifest collection window differs",
        )
        _expect(
            event["source"]["identity"]
            == f"codex-thread-closure:generation:{generation}:manifest",
            "Codex manifest identity differs",
        )
        aggregate: dict[str, int] = {}
        generation_identities: set[str] = set()
        generation_paths: set[str] = set()
        generation_threads: set[str] = set()
        parent_edges: list[tuple[str, str | None]] = []
        for item in files:
            _verify_codex_manifest_item(item)
            identity = item["source_identity"]
            _expect(identity not in generation_identities, "Codex generation repeats a source")
            generation_identities.add(identity)
            _expect(
                item["source_path_sha256"] not in generation_paths,
                "Codex generation repeats a source path",
            )
            generation_paths.add(item["source_path_sha256"])
            _expect(
                item["thread_id"] not in generation_threads,
                "Codex generation repeats a thread",
            )
            generation_threads.add(item["thread_id"])
            parent_edges.append((item["thread_id"], item["parent_thread_id"]))
            referenced.add(identity)
            _expect(
                item["source_identity_sha256"] == source_identity_sha256(identity),
                "manifest source-identity digest differs",
            )
            source_event = projection_events.get(identity)
            _expect(source_event is not None, "Codex generation references a missing projection")
            if source_event is None:  # pragma: no cover - narrowed by the fail-closed check
                raise EvidenceVerificationError("Codex generation references a missing projection")
            _verify_codex_final_observation(item, source_event)
            _expect(
                source_event["disposition"]["status"] == item["disposition"],
                "Codex projection disposition differs",
            )
            _expect(source_event["disposition"]["reason"] == item["reason"], "Codex reason differs")
            _expect(
                source_event["source"]["redaction_categories"] == item["redaction_categories"]
                and source_event["source"]["redaction_count"] == item["redaction_count"],
                "Codex redaction metadata differs",
            )
            if item["disposition"] == "captured":
                captured_projection_seen = True
                _expect(len(source_event["objects"]) == 1, "captured Codex projection has no object")
                source_object = source_event["objects"][0]
                _expect(source_object["sha256"] == item["object_sha256"], "Codex object digest differs")
                _expect(source_object["bytes"] == item["object_bytes"], "Codex object size differs")
                _verify_codex_object_metadata(
                    source_object,
                    role="codex-user-visible-projection-gzip",
                    media_type="application/gzip",
                    secret_scan="fixed-length-high-confidence-redaction-completed",
                    label="Codex projection",
                )
                projection_path = observed.get(source_object["sha256"])
                _expect(projection_path is not None, "Codex projection object is missing")
                if projection_path is None:  # pragma: no cover - narrowed above
                    raise EvidenceVerificationError("Codex projection object is missing")
                if parallel_projection_verification:
                    lineage = session_lineages[item["thread_id"]]
                    lineage_metadata = {
                        thread_id: session_metadata[thread_id]
                        for thread_id in lineage
                        if thread_id in session_metadata
                    }
                    parallel_tasks.append(
                        (
                            identity,
                            projection_path,
                            item,
                            source_event,
                            lineage,
                            lineage_metadata,
                        )
                    )
                else:
                    try:
                        _verify_codex_projection(
                            projection_path,
                            item,
                            source_event,
                            allowed_session_thread_ids=session_lineages[item["thread_id"]],
                            session_lineage_metadata=session_metadata,
                            required_projection_schema=required_projection_schema,
                            read_descriptor=(
                                observed_descriptors[source_object["sha256"]]
                                if observed_descriptors is not None
                                else None
                            ),
                            progress_bytes_function=(
                                advance_projection_bytes
                                if progress_function is not None
                                else None
                            ),
                        )
                    except _CodexProjectionSchemaMismatch:
                        projection_schema_compatible = False
            else:
                source = source_event["source"]
                _expect(
                    source["snapshot_method"] == "streamed-user-visible-projection"
                    and source["redaction_mode"]
                    == "fixed-length-high-confidence-projection-redaction",
                    "excluded Codex projection metadata differs",
                )
                reason_prefix = "unredactable-secret-category:"
                _expect(item["reason"].startswith(reason_prefix), "excluded Codex reason is invalid")
                category = item["reason"][len(reason_prefix) :]
                _expect(bool(category), "excluded Codex secret category is empty")
                expected_identity = (
                    f"codex-user-visible-projection:thread:{item['thread_id']}:"
                    f"session:{item['session_id']}:"
                    f"path-sha256:{item['source_path_sha256']}:"
                    f"source-sha256:{item['raw_source_sha256']}:excluded:{category}"
                )
                _expect(source["identity"] == expected_identity, "excluded Codex identity differs")
            if not (parallel_projection_verification and item["disposition"] == "captured"):
                complete_projection(identity)
            for skipped_type, count in item["skipped_record_types"].items():
                aggregate[skipped_type] = aggregate.get(skipped_type, 0) + count
        reachable = {
            item["thread_id"]
            for item in files
            if item["thread_id"] == manifest["thread_id"]
        }
        if not reachable:
            reachable = {
                item["thread_id"]
                for item in files
                if item["session_id"] == manifest["thread_id"]
                and item["parent_thread_id"] is None
            }
        _expect(
            len(reachable) == 1,
            "Codex generation does not contain one unique target thread",
        )
        parents = dict(parent_edges)
        for thread, parent in parent_edges:
            _expect(parent != thread, "Codex generation contains a self-parent edge")
            visited: set[str] = set()
            current: str | None = thread
            while current is not None and current in parents:
                _expect(
                    current not in visited,
                    "Codex generation contains a parent cycle",
                )
                visited.add(current)
                current = parents[current]
        while True:
            expanded = reachable | {
                thread
                for thread, parent in parent_edges
                if parent in reachable
            }
            if expanded == reachable:
                break
            reachable = expanded
        _expect(
            reachable == generation_threads,
            "Codex generation is not a target-and-transitive-descendant closure",
        )
        _expect(
            dict(sorted(aggregate.items())) == manifest["aggregate_skipped_record_types"],
            "Codex aggregate skipped-record count differs",
        )
    if parallel_projection_verification:
        parallel_start_bytes = completed_projection_bytes
        _verify_codex_projections_parallel(
            parallel_tasks,
            workers=workers,
            progress_bytes_function=(
                advance_projection_bytes if progress_function is not None else None
            ),
            completed_function=complete_projection,
        )
        if progress_function is not None:
            expected_parallel_bytes = sum(
                int(task[2]["uncompressed_bytes"])
                for task in parallel_tasks
            )
            accounted_parallel_bytes = completed_projection_bytes - parallel_start_bytes
            _expect(
                accounted_parallel_bytes <= expected_parallel_bytes,
                "Codex projection worker progress exceeds its byte binding",
            )
            if accounted_parallel_bytes < expected_parallel_bytes:
                advance_projection_bytes(
                    expected_parallel_bytes - accounted_parallel_bytes
                )
    _expect(
        set(projection_events) == referenced,
        "Codex projection set is partial or lacks a completion manifest",
    )
    if required_projection_schema is not None and not captured_projection_seen:
        projection_schema_compatible = False
    if progress_function is not None and total_projections:
        report_progress("codex-verification-complete")
    return projection_schema_compatible


def validate_reusable_codex_generation(
    root: Path,
    events: Sequence[Mapping[str, Any]],
    manifest_identity: str,
    *,
    required_projection_schema: str | None = None,
) -> Mapping[str, Any] | None:
    """Deep-validate one prior generation before the capture path reuses it."""

    try:
        journal_events = read_journal(root / "journal.jsonl")
    except EvidenceCaptureError as error:
        raise EvidenceVerificationError(
            "prior Codex generation journal validation failed"
        ) from error
    _expect(
        list(events) == journal_events,
        "prior Codex generation differs from the durable journal",
    )
    by_identity = {
        event["source"]["identity"]: event
        for event in events
    }
    _expect(
        len(by_identity) == len(events),
        "prior Codex generation journal repeats an identity",
    )
    manifest_event = by_identity.get(manifest_identity)
    _expect(
        manifest_event is not None
        and manifest_event["source"]["kind"]
        == "codex-thread-closure-generation-manifest",
        "prior Codex generation manifest is missing",
    )
    if manifest_event is None:  # pragma: no cover - narrowed above
        raise EvidenceVerificationError("prior Codex generation manifest is missing")
    _verify_event_semantics(manifest_event)
    manifest_object = _verify_codex_manifest_event_metadata(manifest_event)
    manifest_digest = manifest_object["sha256"]
    manifest_path = root / "objects" / "sha256" / manifest_digest[:2] / manifest_digest
    _expect(
        manifest_path.is_file() and not manifest_path.is_symlink(),
        "prior Codex generation manifest object is missing",
    )
    raw = _read_codex_manifest(manifest_path, manifest_object["bytes"])
    _expect(
        hashlib.sha256(raw).hexdigest() == manifest_digest,
        "prior Codex generation manifest object digest differs",
    )
    manifest = parse_json(raw, "prior Codex generation manifest")
    _expect(
        isinstance(manifest, dict)
        and set(manifest) == CODEX_MANIFEST_KEYS
        and isinstance(manifest.get("files"), list)
        and bool(manifest["files"]),
        "prior Codex generation manifest is invalid",
    )
    subset: list[Mapping[str, Any]] = [manifest_event]
    observed: dict[str, Path] = {manifest_digest: manifest_path}
    claims: dict[str, int] = {manifest_digest: manifest_object["bytes"]}
    for item in manifest["files"]:
        _expect(
            isinstance(item, dict)
            and isinstance(item.get("source_identity"), str),
            "prior Codex generation file entry is invalid",
        )
        source_event = by_identity.get(item["source_identity"])
        _expect(
            source_event is not None
            and source_event["source"]["kind"] == "codex-user-visible-projection",
            "prior Codex generation projection is missing",
        )
        if source_event is None:  # pragma: no cover - narrowed above
            raise EvidenceVerificationError("prior Codex generation projection is missing")
        _verify_event_semantics(source_event)
        subset.append(source_event)
        for object_item in source_event["objects"]:
            digest = object_item["sha256"]
            prior_bytes = claims.get(digest)
            _expect(
                prior_bytes is None or prior_bytes == object_item["bytes"],
                "prior Codex generation object size conflicts",
            )
            claims[digest] = object_item["bytes"]
            observed[digest] = root / "objects" / "sha256" / digest[:2] / digest
    descriptors: dict[str, int] = {}
    signatures: dict[str, tuple[int, ...]] = {}
    try:
        for digest, path in observed.items():
            metadata = path.lstat()
            _expect(
                not path.is_symlink()
                and stat.S_ISREG(metadata.st_mode)
                and metadata.st_nlink == 1
                and stat.S_IMODE(metadata.st_mode) == 0o600
                and metadata.st_uid == os.getuid()
                and not _has_extended_acl(path)
                and not _unindexed_extended_attributes(path),
                "prior Codex generation object is not a private regular file",
            )
            _expect(
                metadata.st_size == claims[digest],
                "prior Codex generation object size differs",
            )
            descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            descriptors[digest] = descriptor
            opened = os.fstat(descriptor)
            signature = (
                opened.st_dev,
                opened.st_ino,
                opened.st_mode,
                opened.st_nlink,
                opened.st_uid,
                opened.st_size,
                opened.st_mtime_ns,
                opened.st_ctime_ns,
            )
            _expect(
                signature
                == (
                    metadata.st_dev,
                    metadata.st_ino,
                    metadata.st_mode,
                    metadata.st_nlink,
                    metadata.st_uid,
                    metadata.st_size,
                    metadata.st_mtime_ns,
                    metadata.st_ctime_ns,
                ),
                "prior Codex generation object changed while it was opened",
            )
            signatures[digest] = signature
            computed = hashlib.sha256()
            total = 0
            while chunk := os.read(descriptor, 1024 * 1024):
                total += len(chunk)
                _expect(
                    total <= claims[digest],
                    "prior Codex generation object exceeds its byte binding",
                )
                computed.update(chunk)
            _expect(
                total == claims[digest] and computed.hexdigest() == digest,
                "prior Codex generation object digest differs",
            )
        compatible = _verify_codex_generations(
            subset,
            observed,
            required_projection_schema=required_projection_schema,
            observed_descriptors=descriptors,
        )
        for digest, path in observed.items():
            after = os.fstat(descriptors[digest])
            current = path.lstat()
            _expect(
                signatures[digest]
                == (
                    after.st_dev,
                    after.st_ino,
                    after.st_mode,
                    after.st_nlink,
                    after.st_uid,
                    after.st_size,
                    after.st_mtime_ns,
                    after.st_ctime_ns,
                )
                == (
                    current.st_dev,
                    current.st_ino,
                    current.st_mode,
                    current.st_nlink,
                    current.st_uid,
                    current.st_size,
                    current.st_mtime_ns,
                    current.st_ctime_ns,
                ),
                "prior Codex generation object changed during semantic validation",
            )
        return manifest if compatible else None
    finally:
        for descriptor in descriptors.values():
            os.close(descriptor)




def _verify_store_locked(
    root: Path,
    *,
    progress_function: Callable[[Mapping[str, object]], None] | None = None,
    workers: int = 1,
) -> dict[str, object]:
    try:
        _verify_modes_and_shape(root)
        _verify_topology(root)
        _verify_format(root)
        incoming = root / ".incoming"
        _expect(not any(incoming.iterdir()), "store contains an incomplete incoming object")
        journal_raw = _read_private_file_bounded(
            root / "journal.jsonl",
            "journal",
            MAX_STORE_JOURNAL_BYTES,
        )
        try:
            _scan_secret_binary_stream(io.BytesIO(journal_raw))
        except SecretDetectedError as error:
            raise EvidenceVerificationError(
                f"journal contains unredacted secret category {error.category}"
            ) from error
        events = read_journal(root / "journal.jsonl")
        identities: set[str] = set()
        referenced: dict[str, int] = {}
        object_claims: dict[str, list[tuple[Mapping[str, Any], str]]] = {}
        for event in events:
            _verify_event_semantics(event)
            if event["source"]["kind"] == "codex-thread-closure-generation-manifest":
                _verify_codex_manifest_event_metadata(event)
            identity = event["source"]["identity"]
            _expect(identity not in identities, "immutable source identity is duplicated")
            identities.add(identity)
            for item in event["objects"]:
                digest = item["sha256"]
                if digest in referenced:
                    _expect(referenced[digest] == item["bytes"], "object size conflicts across events")
                referenced[digest] = item["bytes"]
                object_claims.setdefault(digest, []).append(
                    (item, event["source"]["kind"])
                )
        observed = _object_paths(root)
        _expect(set(observed) == set(referenced), "indexed and stored content objects differ")
        integrity_started_at = time.monotonic()
        integrity_last_progress_at = integrity_started_at
        integrity_completed_objects = 0
        integrity_completed_bytes = 0
        integrity_last_progress_bytes = 0
        integrity_total_objects = len(observed)
        integrity_total_bytes = sum(referenced.values())

        def report_integrity_progress(
            stage: str,
            *,
            observed_at: float | None = None,
        ) -> None:
            if progress_function is None:
                return
            current = time.monotonic() if observed_at is None else observed_at
            progress_function(
                {
                    "stage": stage,
                    "completed_objects": integrity_completed_objects,
                    "total_objects": integrity_total_objects,
                    "completed_object_bytes": integrity_completed_bytes,
                    "total_object_bytes": integrity_total_bytes,
                    "elapsed_seconds": round(
                        max(0.0, current - integrity_started_at),
                        3,
                    ),
                }
            )

        if progress_function is not None:
            report_integrity_progress(
                "store-integrity-start",
                observed_at=integrity_started_at,
            )
        for digest, path in observed.items():
            metadata = path.stat()
            _expect(metadata.st_size <= MAX_OBJECT_BYTES, "content object exceeds byte boundary")
            _expect(metadata.st_size == referenced[digest], "content-object size differs")
            computed = hashlib.sha256()
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    computed.update(chunk)
                    if progress_function is not None:
                        integrity_completed_bytes += len(chunk)
                        current = time.monotonic()
                        if (
                            integrity_completed_bytes - integrity_last_progress_bytes
                            >= CODEX_VERIFICATION_PROGRESS_BYTES
                            or current - integrity_last_progress_at
                            >= CODEX_VERIFICATION_PROGRESS_SECONDS
                        ):
                            report_integrity_progress(
                                "store-integrity-progress",
                                observed_at=current,
                            )
                            integrity_last_progress_bytes = integrity_completed_bytes
                            integrity_last_progress_at = current
            _expect(computed.hexdigest() == digest, "content-object digest differs")
            archive_format = _archive_format_from_magic(path)
            media_types = {item["media_type"] for item, _ in object_claims[digest]}
            _expect(
                "application/octet-stream" not in media_types,
                "content object uses an unsupported opaque binary format",
            )
            try:
                if archive_format == "zip" or zipfile.is_zipfile(path):
                    _scan_zip_archive(path)
                elif media_types == {"image/png"}:
                    _validate_png(path)
                    with path.open("rb") as stream:
                        _scan_secret_binary_stream(stream)
                elif media_types == {"image/jpeg"}:
                    _validate_jpeg(path)
                    with path.open("rb") as stream:
                        _scan_secret_binary_stream(stream)
                else:
                    if archive_format is None:
                        archive_format = _embedded_archive_format(path)
                    gzip_projection = _is_bound_codex_projection_gzip(
                        archive_format,
                        object_claims[digest],
                    )
                    _expect(
                        archive_format is None or gzip_projection,
                        "content object is an unsupported compressed or archive format",
                    )
                    if not gzip_projection:
                        with path.open("rb") as stream:
                            _scan_secret_binary_stream(stream)
            except SecretDetectedError as error:
                raise EvidenceVerificationError(
                    f"content object contains unredacted secret category {error.category}"
                ) from error
            integrity_completed_objects += 1
            if (
                progress_function is not None
                and integrity_completed_objects < integrity_total_objects
                and (
                    integrity_completed_objects
                    % STORE_INTEGRITY_PROGRESS_OBJECT_INTERVAL
                    == 0
                    or time.monotonic() - integrity_last_progress_at
                    >= CODEX_VERIFICATION_PROGRESS_SECONDS
                )
            ):
                current = time.monotonic()
                report_integrity_progress(
                    "store-integrity-progress",
                    observed_at=current,
                )
                integrity_last_progress_bytes = integrity_completed_bytes
                integrity_last_progress_at = current
        if progress_function is not None:
            report_integrity_progress("store-integrity-complete")
        _verify_github_semantics(events, observed)
        _verify_codex_generations(
            events,
            observed,
            progress_function=progress_function,
            workers=workers,
        )
        expected_ledger = build_expiry_ledger(events, journal_raw)
        ledger_path = root / "expiry-ledger.json"
        ledger_raw = _read_private_file_bounded(
            ledger_path,
            "expiry ledger",
            MAX_STORE_LEDGER_BYTES,
        )
        ledger = parse_json(ledger_raw, "expiry ledger")
        _expect(ledger == expected_ledger, "expiry ledger does not match the journal")
        _expect(ledger_raw == canonical_json(expected_ledger, pretty=True), "expiry ledger is not canonical")
    except (EvidenceCaptureError, FileNotFoundError, OSError, TypeError, ValueError) as error:
        if isinstance(error, EvidenceVerificationError):
            raise
        if isinstance(error, OSError):
            raise EvidenceVerificationError(
                "private evidence store is unavailable or inaccessible"
            ) from error
        raise EvidenceVerificationError(str(error)) from error

    now = utc_now()
    warning_count = sum(
        1
        for item in expected_ledger["entries"]
        if parse_time(item["warning_at_utc"], "warning") <= now
    )
    return {
        "verified": True,
        "journal_events": len(events),
        "journal_head_sha256": events[-1]["event_sha256"] if events else None,
        "objects": len(observed),
        "bytes": sum(referenced.values()),
        "expiry_warnings": warning_count,
        "boundaries": BOUNDARIES,
        "limitations": {
            "source_truth_attested": False,
            "timestamp_attested": False,
            "whole_store_rewrite_detectable_without_independent_anchor": False,
        },
    }


def verify_store(
    root: Path,
    *,
    progress_function: Callable[[Mapping[str, object]], None] | None = None,
    workers: int = 1,
) -> dict[str, object]:
    _expect(
        isinstance(workers, int)
        and not isinstance(workers, bool)
        and MIN_CODEX_VERIFICATION_WORKERS
        <= workers
        <= MAX_CODEX_VERIFICATION_WORKERS,
        "Codex verification worker count is invalid",
    )
    try:
        lock_path = root / ".lock"
        lock_metadata = lock_path.lstat()
        _expect(
            not lock_path.is_symlink()
            and stat.S_ISREG(lock_metadata.st_mode)
            and lock_metadata.st_nlink == 1
            and stat.S_IMODE(lock_metadata.st_mode) == 0o600
            and lock_metadata.st_uid == os.getuid(),
            "store lock is not one private regular file",
        )
        with lock_path.open("rb") as lock_stream:
            fcntl.flock(lock_stream.fileno(), fcntl.LOCK_SH)
            try:
                return _verify_store_locked(
                    root,
                    progress_function=progress_function,
                    workers=workers,
                )
            finally:
                fcntl.flock(lock_stream.fileno(), fcntl.LOCK_UN)
    except (EvidenceCaptureError, FileNotFoundError, OSError, TypeError, ValueError) as error:
        if isinstance(error, EvidenceVerificationError):
            raise
        if isinstance(error, OSError):
            raise EvidenceVerificationError(
                "private evidence store is unavailable or inaccessible"
            ) from error
        raise EvidenceVerificationError(str(error)) from error


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--store", type=Path, required=True)
    value.add_argument(
        "--progress",
        action="store_true",
        help="write bounded path-free Codex verification progress to standard error",
    )
    value.add_argument(
        "--workers",
        type=int,
        choices=range(
            MIN_CODEX_VERIFICATION_WORKERS,
            MAX_CODEX_VERIFICATION_WORKERS + 1,
        ),
        default=1,
        help="verify independent Codex projections with 1 to 4 processes (default: 1)",
    )
    return value


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    progress_function = None
    if arguments.progress:
        progress_function = lambda value: print(  # noqa: E731
            json.dumps({"progress": value}, sort_keys=True),
            file=sys.stderr,
        )
    try:
        with private_umask():
            result = verify_store(
                arguments.store,
                progress_function=progress_function,
                workers=arguments.workers,
            )
    except EvidenceVerificationError as error:
        print(json.dumps({"verified": False, "error": str(error), "boundaries": BOUNDARIES}, sort_keys=True), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
