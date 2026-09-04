#!/usr/bin/env python3
"""Capture delivery evidence into a private, content-addressed local store.

The store is deliberately independent of the product evidence ledger.  It keeps
source bytes for a future, separately authorised retrospective; it does not count
attempts, infer causes, calculate costs or publish material.
"""

from __future__ import annotations

import argparse
import contextlib
import ctypes
import errno
import fcntl
import gzip
import hashlib
import io
import json
import math
import mmap
import os
import plistlib
import re
import selectors
import shutil
import stat
import subprocess
import sys
import time
import unicodedata
import uuid
import zipfile
import zlib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence
from urllib.parse import quote, urlsplit, urlunsplit
from zoneinfo import ZoneInfo


# Reuse this module instance when the CLI lazily loads the candidate-scoped
# verifier; otherwise Python would load a second copy under the import name.
if __name__ == "__main__":
    sys.modules.setdefault("capture_delivery_evidence", sys.modules[__name__])


ROOT = Path(__file__).resolve().parents[1]
STORE_SCHEMA = "gis-ai-go.delivery-evidence-store.v1"
EVENT_SCHEMA = "gis-ai-go.delivery-evidence-journal-event.v1"
LEDGER_SCHEMA = "gis-ai-go.delivery-evidence-expiry-ledger.v1"
PENDING_EVENT_SCHEMA = "gis-ai-go.delivery-evidence-pending-event.v1"
PENDING_EVENT_NAME = ".pending-event.json"
JOURNAL_DOMAIN = b"gis-ai-go.delivery-evidence-journal-event.v1\0"
IDENTITY_DOMAIN = b"gis-ai-go.delivery-evidence-source-identity.v1\0"
LONDON = ZoneInfo("Europe/London")
OVERLAP = timedelta(hours=48)
WARNING_WINDOW = timedelta(days=14)
MAX_METADATA_BYTES = 16 * 1024 * 1024
MAX_LOG_BYTES = 512 * 1024 * 1024
MAX_OBJECT_BYTES = 2 * 1024 * 1024 * 1024
DEFAULT_ARTIFACT_MAX_BYTES = 16 * 1024 * 1024
DEFAULT_CAPTURE_MAX_BYTES = 8 * 1024 * 1024 * 1024
MAX_CAPTURE_MAX_BYTES = 64 * 1024 * 1024 * 1024
MIN_STORE_FREE_BYTES = 5 * 1024 * 1024 * 1024
MAX_ARCHIVE_SCAN_UNCOMPRESSED_BYTES = 2 * 1024 * 1024 * 1024
MAX_ARCHIVE_SCAN_ENTRIES = 100_000
MAX_ARCHIVE_SCAN_METADATA_BYTES = 64 * 1024 * 1024
MAX_PNG_METADATA_BYTES = 16 * 1024 * 1024
MAX_JPEG_BYTES = 64 * 1024 * 1024
UNINSPECTABLE_ARCHIVE_SUFFIXES = {
    ".7z",
    ".bz2",
    ".gz",
    ".lz",
    ".rar",
    ".tar",
    ".tgz",
    ".xz",
    ".zst",
}
PRIVATE_KEY_CONTAINER_SUFFIXES = {
    ".der",
    ".jks",
    ".key",
    ".keystore",
    ".p12",
    ".p8",
    ".pfx",
    ".pk8",
}
GITHUB_METADATA_TIMEOUT_SECONDS = 60
GITHUB_METADATA_MAX_ATTEMPTS = 3
GITHUB_METADATA_RETRY_DELAY_SECONDS = 0.1
GITHUB_DOWNLOAD_TIMEOUT_SECONDS = 300
MAX_GITHUB_API_INVOCATIONS = 10_000
MAX_GITHUB_METADATA_TRANSFER_BYTES = 512 * 1024 * 1024
MAX_GITHUB_CAPTURE_SECONDS = 60 * 60
GITHUB_MAX_WORKFLOW_RUN_DURATION = timedelta(days=35)
GITHUB_MAX_RETENTION_DAYS = 400
MAX_CAPTURE_EVENTS = 25_000
MAX_CAPTURE_METADATA_BYTES = 512 * 1024 * 1024
MAX_STORE_EVENTS = 100_000
MAX_STORE_JOURNAL_BYTES = 128 * 1024 * 1024
MAX_STORE_LEDGER_BYTES = 64 * 1024 * 1024
MAX_CODEX_LINE_BYTES = 64 * 1024 * 1024
MAX_CODEX_PREFIX_BYTES = 64 * 1024
MAX_CODEX_TEXT_BYTES = 16 * 1024
MAX_CODEX_CONTAINER_ITEMS = 64
MAX_CODEX_PROJECTED_LINE_BYTES = 8 * 1024 * 1024
LEGACY_CODEX_PROJECTION_SCHEMA = "gis-ai-go.codex-user-visible-delivery-projection.v1"
INTERMEDIATE_CODEX_PROJECTION_SCHEMA = (
    "gis-ai-go.codex-user-visible-delivery-projection.v2"
)
CODEX_PROJECTION_SCHEMA = "gis-ai-go.codex-user-visible-delivery-projection.v3"
CODEX_GENERATION_SCHEMA = "gis-ai-go.codex-thread-closure-generation.v1"
CODEX_OUTSIDE_LINEAGE_STUB = "session_meta:outside-selected-lineage"
CODEX_FORK_ID_DIGEST_DOMAIN = b"gis-ai-go.codex-forked-from-id.v1\0"
CODEX_GENERATION_FILE_KEYS = {
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
TEXT_SUFFIXES = {
    ".csv",
    ".json",
    ".jsonl",
    ".log",
    ".md",
    ".ndjson",
    ".text",
    ".toml",
    ".tsv",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
TRIGGER_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9._-]{0,62}[a-z0-9])?$")
REPOSITORY_PATTERN = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9_.-]{0,98}[A-Za-z0-9])?/"
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]{0,98}[A-Za-z0-9])?$"
)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
BOUNDARIES: dict[str, bool] = {
    "retrospective_analysis_started": False,
    "attempts_counted": False,
    "causal_findings_produced": False,
    "costs_calculated": False,
    "publication_authorised": False,
}
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "private-key",
        re.compile(
            r"(?:-----BEGIN (?:(?:[A-Z0-9][A-Z0-9 -]{0,62} )?PRIVATE KEY|"
            r"PGP PRIVATE KEY BLOCK)-----|"
            r"---- BEGIN SSH2 ENCRYPTED PRIVATE KEY ----|"
            r"PuTTY-User-Key-File-[123]:\s*[A-Za-z0-9._+-]+)"
        ),
    ),
    (
        "github-stateless-installation-token",
        re.compile(
            r"ghs_[A-Za-z0-9]+_[A-Za-z0-9_-]+\."
            r"[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"
        ),
    ),
    ("github-token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}")),
    ("github-fine-grained-token", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("openai-token", re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}")),
    ("anthropic-token", re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}")),
    ("npm-granular-token", re.compile(r"npm_[A-Za-z0-9]{36,}")),
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("aws-temporary-access-key", re.compile(r"ASIA[0-9A-Z]{16}")),
    ("google-api-key", re.compile(r"AIza[A-Za-z0-9_-]{35}")),
    ("google-oauth-client-secret", re.compile(r"GOCSPX-[A-Za-z0-9_-]{28}")),
    ("gitlab-token", re.compile(r"glpat-[A-Za-z0-9_-]{20,}")),
    (
        "pypi-token",
        re.compile(r"pypi-AgEIcHlwaS5vcmc[A-Za-z0-9_-]{30,}"),
    ),
    ("slack-token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}")),
    ("slack-app-token", re.compile(r"xapp-1-[A-Za-z0-9-]{40,}")),
    ("hugging-face-token", re.compile(r"hf_[A-Za-z0-9]{34,}")),
    ("stripe-live-secret", re.compile(r"(?:sk|rk)_live_[A-Za-z0-9]{24,}")),
    (
        "sendgrid-api-key",
        re.compile(r"SG\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{32,}"),
    ),
    ("docker-access-token", re.compile(r"dckr_pat_[A-Za-z0-9_-]{20,}")),
    (
        "slack-webhook",
        re.compile(
            r"https://hooks\.slack\.com/services/"
            r"[A-Za-z0-9_-]{8,}/[A-Za-z0-9_-]{8,}/[A-Za-z0-9_-]{16,}"
        ),
    ),
    (
        "bearer-token",
        re.compile(r"(?i)authorization\s*:\s*bearer\s+[A-Za-z0-9._~+/-]{16,}={0,2}"),
    ),
    (
        "basic-authorization",
        re.compile(
            r"(?i)(?:proxy-)?authorization\s*:\s*basic\s+"
            r"[A-Za-z0-9+/]{12,}={0,2}"
        ),
    ),
    (
        "session-cookie",
        re.compile(
            r"(?i)(?:set-cookie|cookie)\s*:\s*[^\r\n]{0,4096}?"
            r"(?<![A-Za-z0-9_.-])(?:__Host-|__Secure-)?"
            r"(?:jsessionid|phpsessid|asp\.net_sessionid|sessionid|session|"
            r"connect\.sid|sid|auth|token)\s*=\s*"
            r"[\"']?[A-Za-z0-9._~+/%-]{1,}[\"']?"
        ),
    ),
    (
        "oauth-callback-code",
        re.compile(
            r"(?i)(?:[?&]|\b)(?:code|access_token|refresh_token|id_token)="
            r"[A-Za-z0-9._~+/%-]{12,}"
        ),
    ),
    (
        "database-credential-url",
        re.compile(
            r"(?i)(?<![A-Za-z0-9_-])(?:database[_-]?url|connection[_-]?string)"
            r"(?:\\?[\"'])?\s*[:=]\s*"
            r"[\"']?(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://"
            r"[^\s:@/\"']+:[^\s@\"']+@"
        ),
    ),
    (
        "userinfo-credential-url",
        re.compile(
            r"(?i)(?:https?|postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqps?)://"
            r"[^\s:@/\"']+:[^\s@/\"']+@"
        ),
    ),
    (
        "assigned-secret",
        re.compile(
            r"(?i)(?<![A-Za-z0-9_-])(?:aws[_-]?secret[_-]?access[_-]?key|"
            r"aws[_-]?session[_-]?token|node[_-]?auth[_-]?token|"
            r"session[_-]?token|auth[_-]?token|_auth[_-]?token|npm[_-]?token|"
            r"refresh[_-]?token|id[_-]?token|api[_-]?key|password|"
            r"client[_-]?secret|access[_-]?token|token|secret)"
            r"(?:\\?[\"'])?\s*[:=]\s*[\"'][^\"'\r\n]{1,}[\"']"
        ),
    ),
    (
        "assigned-secret-unquoted",
        re.compile(
            r"(?i)(?<![A-Za-z0-9_-])(?:aws[_-]?secret[_-]?access[_-]?key|"
            r"aws[_-]?session[_-]?token|node[_-]?auth[_-]?token|"
            r"session[_-]?token|auth[_-]?token|_auth[_-]?token|npm[_-]?token|"
            r"refresh[_-]?token|id[_-]?token|api[_-]?key|password|"
            r"client[_-]?secret|access[_-]?token|token|secret)"
            r"(?:\\?[\"'])?\s*[:=]\s*[A-Za-z0-9._~+/%-]{1,}"
        ),
    ),
    (
        "signed-url",
        re.compile(
            r"(?i)[?&](?:x-amz-signature|sig|signature)="
            r"[A-Za-z0-9._~+/%-]{16,}"
        ),
    ),
)
UNREDACTABLE_SECRET_PATTERN = re.compile(
    rb"(?:-----BEGIN (?:(?:[A-Z0-9][A-Z0-9 -]{0,62} )?PRIVATE KEY|"
    rb"PGP PRIVATE KEY BLOCK)-----|"
    rb"---- BEGIN SSH2 ENCRYPTED PRIVATE KEY ----|"
    rb"PuTTY-User-Key-File-[123]:\s*[A-Za-z0-9._+-]+)"
)
FIXED_LENGTH_REDACTION_PATTERNS: tuple[tuple[str, re.Pattern[bytes]], ...] = (
    (
        "github-stateless-installation-token",
        re.compile(
            rb"(ghs_[A-Za-z0-9]+_[A-Za-z0-9_-]+\."
            rb"[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)"
        ),
    ),
    ("github-token", re.compile(rb"(gh[pousr]_[A-Za-z0-9_]{20,})")),
    (
        "github-fine-grained-token",
        re.compile(rb"(github_pat_[A-Za-z0-9_]{20,})"),
    ),
    ("openai-token", re.compile(rb"(sk-(?:proj-)?[A-Za-z0-9_-]{20,})")),
    ("anthropic-token", re.compile(rb"(sk-ant-[A-Za-z0-9_-]{20,})")),
    ("npm-granular-token", re.compile(rb"(npm_[A-Za-z0-9]{36,})")),
    ("aws-access-key", re.compile(rb"(AKIA[0-9A-Z]{16})")),
    ("aws-temporary-access-key", re.compile(rb"(ASIA[0-9A-Z]{16})")),
    ("google-api-key", re.compile(rb"(AIza[A-Za-z0-9_-]{35})")),
    (
        "google-oauth-client-secret",
        re.compile(rb"(GOCSPX-[A-Za-z0-9_-]{28})"),
    ),
    ("gitlab-token", re.compile(rb"(glpat-[A-Za-z0-9_-]{20,})")),
    (
        "pypi-token",
        re.compile(rb"(pypi-AgEIcHlwaS5vcmc[A-Za-z0-9_-]{30,})"),
    ),
    ("slack-token", re.compile(rb"(xox[baprs]-[A-Za-z0-9-]{20,})")),
    ("slack-app-token", re.compile(rb"(xapp-1-[A-Za-z0-9-]{40,})")),
    ("hugging-face-token", re.compile(rb"(hf_[A-Za-z0-9]{34,})")),
    ("stripe-live-secret", re.compile(rb"((?:sk|rk)_live_[A-Za-z0-9]{24,})")),
    (
        "sendgrid-api-key",
        re.compile(rb"(SG\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{32,})"),
    ),
    ("docker-access-token", re.compile(rb"(dckr_pat_[A-Za-z0-9_-]{20,})")),
    (
        "slack-webhook",
        re.compile(
            rb"https://hooks\.slack\.com/services/"
            rb"([A-Za-z0-9_-]{8,}/[A-Za-z0-9_-]{8,}/[A-Za-z0-9_-]{16,})"
        ),
    ),
    (
        "bearer-token",
        re.compile(rb"(?i)authorization\s*:\s*bearer\s+([A-Za-z0-9._~+/-]{16,}={0,2})"),
    ),
    (
        "basic-authorization",
        re.compile(
            rb"(?i)(?:proxy-)?authorization\s*:\s*basic\s+"
            rb"([A-Za-z0-9+/]{12,}={0,2})"
        ),
    ),
    (
        "session-cookie",
        re.compile(
            rb"(?i)(?:set-cookie|cookie)\s*:\s*[^\r\n]{0,4096}?"
            rb"(?<![A-Za-z0-9_.-])(?:__Host-|__Secure-)?"
            rb"(?:jsessionid|phpsessid|asp\.net_sessionid|sessionid|session|"
            rb"connect\.sid|sid|auth|token)\s*=\s*[\"']?"
            rb"([A-Za-z0-9._~+/%-]{1,})[\"']?"
        ),
    ),
    (
        "oauth-callback-code",
        re.compile(
            rb"(?i)(?:[?&]|\b)(?:code|access_token|refresh_token|id_token)="
            rb"([A-Za-z0-9._~+/%-]{12,})"
        ),
    ),
    (
        "database-credential-url",
        re.compile(
            rb"(?i)(?<![A-Za-z0-9_-])(?:database[_-]?url|connection[_-]?string)"
            rb"(?:\\?[\"'])?\s*[:=]\s*"
            rb"[\"']?((?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://"
            rb"[^\s:@/\"']+:[^\s@\"']+@[^\s\"']*)"
        ),
    ),
    (
        "userinfo-credential-url",
        re.compile(
            rb"(?i)(?:https?|postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqps?)://"
            rb"[^\s:@/\"']+:([^\s@/\"']+)@"
        ),
    ),
    (
        "assigned-secret",
        re.compile(
            rb"(?i)(?<![A-Za-z0-9_-])(?:aws[_-]?secret[_-]?access[_-]?key|"
            rb"aws[_-]?session[_-]?token|node[_-]?auth[_-]?token|"
            rb"session[_-]?token|auth[_-]?token|_auth[_-]?token|"
            rb"npm[_-]?token|"
            rb"refresh[_-]?token|id[_-]?token|api[_-]?key|password|"
            rb"client[_-]?secret|access[_-]?token|token|secret)"
            rb"(?:\\?[\"'])?\s*[:=]\s*[\"']([^\"'\r\n]{1,})[\"']"
        ),
    ),
    (
        "assigned-secret-unquoted",
        re.compile(
            rb"(?i)(?<![A-Za-z0-9_-])(?:aws[_-]?secret[_-]?access[_-]?key|"
            rb"aws[_-]?session[_-]?token|node[_-]?auth[_-]?token|"
            rb"session[_-]?token|auth[_-]?token|_auth[_-]?token|"
            rb"npm[_-]?token|"
            rb"refresh[_-]?token|id[_-]?token|api[_-]?key|password|"
            rb"client[_-]?secret|access[_-]?token|token|secret)"
            rb"(?:\\?[\"'])?\s*[:=]\s*([A-Za-z0-9._~+/%-]{1,})"
        ),
    ),
    (
        "signed-url",
        re.compile(
            rb"(?i)[?&](?:x-amz-signature|sig|signature)="
            rb"([A-Za-z0-9._~+/%-]{16,})"
        ),
    ),
)

# Some redaction patterns deliberately capture a complete value so they can mask
# it in place. A streaming safety scan must not wait for an unbounded closing
# quote or ``@`` before deciding that the same credential structure is present.
# These bounded prefix detectors recognise the credential-bearing structure as
# soon as the first value byte is available. Excessive structural whitespace or
# user-info components fail closed rather than growing the overlap without bound.
SECRET_SCAN_STRUCTURAL_LIMIT = 4096
SECRET_SCAN_OVERLAP_CHARACTERS = 16 * 1024
SECRET_SCAN_OVERLAP_BYTES = 64 * 1024
_STREAMING_ASSIGNED_SECRET_KEY = (
    r"(?<![A-Za-z0-9_-])(?:aws[_-]?secret[_-]?access[_-]?key|"
    r"aws[_-]?session[_-]?token|node[_-]?auth[_-]?token|"
    r"session[_-]?token|auth[_-]?token|_auth[_-]?token|npm[_-]?token|"
    r"refresh[_-]?token|id[_-]?token|api[_-]?key|password|"
    r"client[_-]?secret|access[_-]?token|token|secret)"
)
_STREAMING_USERINFO_SCHEME = (
    r"(?:https?|postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqps?)"
)
_STREAMING_SECRET_DETECTION_PATTERN_SOURCES: tuple[tuple[str, str], ...] = (
    (
        "assigned-secret",
        rf"(?i){_STREAMING_ASSIGNED_SECRET_KEY}(?:\\?[\"'])?"
        rf"\s{{0,{SECRET_SCAN_STRUCTURAL_LIMIT}}}[:=]"
        rf"\s{{0,{SECRET_SCAN_STRUCTURAL_LIMIT}}}[\"'][^\"'\r\n]",
    ),
    (
        "assigned-secret-unquoted",
        rf"(?i){_STREAMING_ASSIGNED_SECRET_KEY}(?:\\?[\"'])?"
        rf"\s{{0,{SECRET_SCAN_STRUCTURAL_LIMIT}}}[:=]"
        rf"\s{{0,{SECRET_SCAN_STRUCTURAL_LIMIT}}}[A-Za-z0-9._~+/%-]",
    ),
    (
        "assigned-secret",
        rf"(?i){_STREAMING_ASSIGNED_SECRET_KEY}(?:\\?[\"'])?"
        rf"\s{{{SECRET_SCAN_STRUCTURAL_LIMIT + 1}}}",
    ),
    (
        "assigned-secret",
        rf"(?i){_STREAMING_ASSIGNED_SECRET_KEY}(?:\\?[\"'])?"
        rf"\s{{0,{SECRET_SCAN_STRUCTURAL_LIMIT}}}[:=]"
        rf"\s{{{SECRET_SCAN_STRUCTURAL_LIMIT + 1}}}",
    ),
    (
        "userinfo-credential-url",
        rf"(?i){_STREAMING_USERINFO_SCHEME}://"
        rf"[^\s:@/\"']{{1,{SECRET_SCAN_STRUCTURAL_LIMIT}}}:"
        rf"[^\s@/\"']{{1,{SECRET_SCAN_STRUCTURAL_LIMIT}}}@",
    ),
    (
        "userinfo-credential-url",
        rf"(?i){_STREAMING_USERINFO_SCHEME}://"
        rf"[^\s:@/\"']{{{SECRET_SCAN_STRUCTURAL_LIMIT + 1}}}",
    ),
    (
        "userinfo-credential-url",
        rf"(?i){_STREAMING_USERINFO_SCHEME}://"
        rf"[^\s:@/\"']{{1,{SECRET_SCAN_STRUCTURAL_LIMIT}}}:"
        rf"[^\s@/\"']{{{SECRET_SCAN_STRUCTURAL_LIMIT + 1}}}",
    ),
)
STREAMING_SECRET_DETECTION_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (category, re.compile(source))
    for category, source in _STREAMING_SECRET_DETECTION_PATTERN_SOURCES
)
STREAMING_SECRET_DETECTION_BYTE_PATTERNS: tuple[
    tuple[str, re.Pattern[bytes]], ...
] = tuple(
    (category, re.compile(source.encode("ascii")))
    for category, source in _STREAMING_SECRET_DETECTION_PATTERN_SOURCES
)


class EvidenceCaptureError(RuntimeError):
    """Raised when evidence cannot be captured without weakening the boundary."""


class GitHubProviderUnavailableError(EvidenceCaptureError):
    """Raised only when GitHub transport cannot supply a requested source."""


class SecretDetectedError(EvidenceCaptureError):
    """Raised when a high-confidence credential pattern is present."""

    def __init__(self, category: str) -> None:
        super().__init__(f"source contains excluded secret category: {category}")
        self.category = category


class UnredactableSecretError(EvidenceCaptureError):
    """Raised when preserving JSONL shape cannot safely remove a secret."""


class _CodexProjectionRedactionNotStable(EvidenceCaptureError):
    """Internal signal that one redaction pass would not produce a fixed point."""

    def __init__(self, categories: Sequence[str]) -> None:
        super().__init__("Codex projection redaction did not reach a fixed point")
        self.categories = tuple(categories)


def _reject_json_constant(value: str) -> object:
    raise EvidenceCaptureError(f"non-standard JSON constant: {value}")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise EvidenceCaptureError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def parse_json(raw: bytes, label: str) -> Any:
    try:
        return json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise EvidenceCaptureError(f"{label} is not valid UTF-8 JSON") from error


def canonical_json(value: object, *, pretty: bool = False) -> bytes:
    if pretty:
        return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
            "utf-8"
        )
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n"
    ).encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def source_identity_sha256(identity: str) -> str:
    return hashlib.sha256(IDENTITY_DOMAIN + identity.encode("utf-8")).hexdigest()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def format_time(value: datetime) -> str:
    normalised = value.astimezone(timezone.utc)
    return normalised.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def format_london_time(value: datetime) -> str:
    return value.astimezone(LONDON).isoformat(timespec="milliseconds")


def parse_time(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise EvidenceCaptureError(f"{label} is not a valid ISO 8601 date-time") from error
    if parsed.tzinfo is None:
        raise EvidenceCaptureError(f"{label} must include an offset")
    return parsed.astimezone(timezone.utc)


@contextlib.contextmanager
def private_umask() -> Iterator[None]:
    previous = os.umask(0o077)
    try:
        yield
    finally:
        os.umask(previous)


def _mode(path: Path) -> int:
    return stat.S_IMODE(path.lstat().st_mode)


def _extended_attributes(path: Path) -> tuple[str, ...]:
    list_attributes = getattr(os, "listxattr", None)
    if list_attributes is not None:
        try:
            return tuple(sorted(list_attributes(path, follow_symlinks=False)))
        except NotImplementedError:
            pass
    if sys.platform == "darwin":
        libc = ctypes.CDLL(None, use_errno=True)
        list_attributes = libc.listxattr
        list_attributes.argtypes = (
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_size_t,
            ctypes.c_int,
        )
        list_attributes.restype = ctypes.c_ssize_t
        encoded_path = os.fsencode(path)
        required = list_attributes(encoded_path, None, 0, 0x0001)
        if required < 0 or required > 1024 * 1024:
            raise EvidenceCaptureError("could not inspect extended attributes")
        if required == 0:
            return ()
        buffer = ctypes.create_string_buffer(required)
        written = list_attributes(encoded_path, buffer, required, 0x0001)
        if written != required:
            raise EvidenceCaptureError("extended attributes changed while inspected")
        try:
            names = buffer.raw[:written].rstrip(b"\0").split(b"\0")
            return tuple(sorted(name.decode("utf-8") for name in names if name))
        except UnicodeDecodeError as error:
            raise EvidenceCaptureError("extended-attribute names are not UTF-8") from error
    raise EvidenceCaptureError("extended-attribute inspection is unavailable")


def _remove_extended_attribute(path: Path, name: str) -> None:
    remove_attribute = getattr(os, "removexattr", None)
    if remove_attribute is not None:
        try:
            remove_attribute(path, name, follow_symlinks=False)
            return
        except NotImplementedError:
            pass
    if sys.platform == "darwin":
        libc = ctypes.CDLL(None, use_errno=True)
        remove_attribute = libc.removexattr
        remove_attribute.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
        remove_attribute.restype = ctypes.c_int
        if remove_attribute(os.fsencode(path), name.encode("utf-8"), 0x0001) == 0:
            return
    raise EvidenceCaptureError("could not remove an extended attribute")


def _is_system_provenance_attribute(path: Path, name: str) -> bool:
    """Recognise the SIP-managed macOS provenance marker, not user data forks."""

    if sys.platform != "darwin" or name != "com.apple.provenance":
        return False
    libc = ctypes.CDLL(None, use_errno=True)
    get_attribute = libc.getxattr
    get_attribute.argtypes = (
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_void_p,
        ctypes.c_size_t,
        ctypes.c_uint32,
        ctypes.c_int,
    )
    get_attribute.restype = ctypes.c_ssize_t
    encoded_path = os.fsencode(path)
    encoded_name = name.encode("utf-8")
    required = get_attribute(encoded_path, encoded_name, None, 0, 0, 0x0001)
    if required != 11:
        return False
    buffer = ctypes.create_string_buffer(required)
    written = get_attribute(
        encoded_path,
        encoded_name,
        buffer,
        required,
        0,
        0x0001,
    )
    if written != required:
        return False
    value = buffer.raw[:written]
    return len(value) == 11 and value.startswith(b"\x01\x02")


def _unindexed_extended_attributes(path: Path) -> tuple[str, ...]:
    return tuple(
        name
        for name in _extended_attributes(path)
        if not _is_system_provenance_attribute(path, name)
    )


def _has_extended_acl(path: Path) -> bool:
    if sys.platform != "darwin":
        return False
    libc = ctypes.CDLL(None, use_errno=True)
    get_acl = libc.acl_get_file
    get_acl.argtypes = (ctypes.c_char_p, ctypes.c_int)
    get_acl.restype = ctypes.c_void_p
    acl = get_acl(os.fsencode(path), 0x00000100)
    if not acl:
        if ctypes.get_errno() == errno.ENOENT:
            return False
        raise EvidenceCaptureError("could not inspect extended ACLs")
    free_acl = libc.acl_free
    free_acl.argtypes = (ctypes.c_void_p,)
    free_acl.restype = ctypes.c_int
    if free_acl(acl) != 0:
        raise EvidenceCaptureError("could not release extended ACL metadata")
    return True


def _strip_unindexed_metadata(path: Path) -> None:
    """Remove OS-added xattrs and ACLs from a newly created store entry."""

    for name in _unindexed_extended_attributes(path):
        _remove_extended_attribute(path, name)
    if _has_extended_acl(path):
        result = subprocess.run(
            ["/bin/chmod", "-N", str(path)],
            check=False,
            capture_output=True,
            timeout=10,
        )
        if result.returncode != 0:
            raise EvidenceCaptureError("could not remove an inherited extended ACL")
    if _unindexed_extended_attributes(path) or _has_extended_acl(path):
        raise EvidenceCaptureError("store entry retains unindexed extended metadata")


def _require_no_unindexed_metadata(path: Path, label: str) -> None:
    if _unindexed_extended_attributes(path):
        raise EvidenceCaptureError(f"{label} has unindexed extended attributes")
    if _has_extended_acl(path):
        raise EvidenceCaptureError(f"{label} has an unindexed extended ACL")


def _require_private_directory(path: Path, label: str) -> None:
    metadata = path.lstat()
    if path.is_symlink() or not stat.S_ISDIR(metadata.st_mode):
        raise EvidenceCaptureError(f"{label} must be a real directory")
    if stat.S_IMODE(metadata.st_mode) != 0o700:
        raise EvidenceCaptureError(f"{label} must have mode 0700")
    if metadata.st_uid != os.getuid():
        raise EvidenceCaptureError(f"{label} must be owned by the current user")
    _require_no_unindexed_metadata(path, label)


def _require_private_regular_file(path: Path, label: str) -> None:
    metadata = path.lstat()
    if path.is_symlink() or not stat.S_ISREG(metadata.st_mode):
        raise EvidenceCaptureError(f"{label} must be a regular file")
    if metadata.st_nlink != 1:
        raise EvidenceCaptureError(f"{label} must not be hard linked")
    if stat.S_IMODE(metadata.st_mode) != 0o600:
        raise EvidenceCaptureError(f"{label} must have mode 0600")
    if metadata.st_uid != os.getuid():
        raise EvidenceCaptureError(f"{label} must be owned by the current user")
    _require_no_unindexed_metadata(path, label)


def _read_private_file_bounded(path: Path, label: str, max_bytes: int) -> bytes:
    """Read one private file only after descriptor-bound size checks."""

    _require_private_regular_file(path, label)
    path_before = path.lstat()
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        if (
            opened.st_dev != path_before.st_dev
            or opened.st_ino != path_before.st_ino
            or opened.st_size > max_bytes
        ):
            raise EvidenceCaptureError(f"{label} exceeds its byte boundary or changed")
        chunks: list[bytes] = []
        total = 0
        while chunk := os.read(descriptor, min(1024 * 1024, max_bytes + 1 - total)):
            chunks.append(chunk)
            total += len(chunk)
            if total > max_bytes:
                raise EvidenceCaptureError(f"{label} exceeds its byte boundary")
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    path_after = path.lstat()
    if (
        _source_signature(opened) != _source_signature(after)
        or _source_signature(opened) != _source_signature(path_after)
        or total != opened.st_size
    ):
        raise EvidenceCaptureError(f"{label} changed while it was read")
    return b"".join(chunks)


def _macos_mount_metadata(path: Path) -> tuple[str, str, set[str]]:
    """Return the backing device, mount point and flags for a local path."""

    try:
        disk = subprocess.run(
            ["/bin/df", "-P", str(path)],
            check=False,
            capture_output=True,
            timeout=10,
        )
        mounts = subprocess.run(
            ["/sbin/mount"],
            check=False,
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise EvidenceCaptureError("could not inspect private-store mount ownership") from error
    if disk.returncode != 0 or mounts.returncode != 0:
        raise EvidenceCaptureError("could not inspect private-store mount ownership")
    try:
        disk_lines = disk.stdout.decode("utf-8").splitlines()
        mount_lines = mounts.stdout.decode("utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise EvidenceCaptureError("private-store mount metadata is not UTF-8") from error
    if len(disk_lines) < 2 or not disk_lines[-1].split():
        raise EvidenceCaptureError("private-store filesystem identity is unavailable")
    filesystem = disk_lines[-1].split()[0]
    matches = [line for line in mount_lines if line.startswith(f"{filesystem} on ")]
    if len(matches) != 1:
        raise EvidenceCaptureError("private-store mount identity is ambiguous")
    match = re.fullmatch(r".+ on (.+) \(([^()]*)\)", matches[0])
    if match is None:
        raise EvidenceCaptureError("private-store mount flags are unavailable")
    mount_point = match.group(1)
    flags = {item.strip().lower() for item in match.group(2).split(",")}
    return filesystem, mount_point, flags


def _macos_diskutil_info(filesystem: str, mount_point: str) -> dict[str, object]:
    try:
        result = subprocess.run(
            ["/usr/sbin/diskutil", "info", "-plist", mount_point],
            check=False,
            capture_output=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise EvidenceCaptureError("could not attest private-store volume metadata") from error
    if result.returncode != 0:
        raise EvidenceCaptureError("could not attest private-store volume metadata")
    try:
        value = plistlib.loads(result.stdout)
    except (plistlib.InvalidFileException, ValueError) as error:
        raise EvidenceCaptureError("private-store volume metadata is invalid") from error
    if not isinstance(value, dict):
        raise EvidenceCaptureError("private-store volume metadata is invalid")
    if value.get("MountPoint") != mount_point:
        raise EvidenceCaptureError("private-store volume mount identity differs")
    device_node = value.get("DeviceNode")
    device_identifier = value.get("DeviceIdentifier")
    if device_node != filesystem and device_identifier != Path(filesystem).name:
        raise EvidenceCaptureError("private-store volume device identity differs")
    return value


def _require_enforced_volume_ownership(path: Path) -> None:
    """Require an internal, FileVault-protected macOS ownership boundary."""

    if sys.platform != "darwin":
        return
    filesystem, mount_point, flags = _macos_mount_metadata(path)
    if flags.intersection({"noowners", "unknownpermissions"}):
        raise EvidenceCaptureError("private-store volume does not enforce ownership")
    value = _macos_diskutil_info(filesystem, mount_point)
    if value.get("GlobalPermissionsEnabled") is not True:
        raise EvidenceCaptureError("private-store volume does not enforce ownership")
    if (
        value.get("Internal") is not True
        or value.get("RemovableMediaOrExternalDevice") is not False
        or value.get("Ejectable") is not False
    ):
        raise EvidenceCaptureError(
            "private-store volume is not an attested internal device"
        )
    if value.get("Encryption") is not True or value.get("FileVault") is not True:
        raise EvidenceCaptureError("private-store volume is not FileVault protected")


def _make_directory(path: Path) -> None:
    path.mkdir(mode=0o700, parents=True, exist_ok=False)
    _strip_unindexed_metadata(path)


def _exclusive_file(path: Path, raw: bytes = b"") -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            view = view[written:]
        _strip_unindexed_metadata(path)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def initialise_store(store: Path) -> None:
    if not store.is_absolute():
        raise EvidenceCaptureError("the private store path must be absolute")
    resolved = store.resolve(strict=False)
    repository = ROOT.resolve()
    if resolved == repository or repository in resolved.parents:
        raise EvidenceCaptureError("the private store must be outside the repository")
    ownership_probe = resolved
    while not ownership_probe.exists() and ownership_probe != ownership_probe.parent:
        ownership_probe = ownership_probe.parent
    _require_enforced_volume_ownership(ownership_probe)
    if store.exists() or store.is_symlink():
        _require_private_directory(store, "private store")
    else:
        store.mkdir(mode=0o700, parents=True)
        os.chmod(store, 0o700)
        _strip_unindexed_metadata(store)
    directories = (
        store / "objects",
        store / "objects" / "sha256",
        store / ".incoming",
    )
    for directory in directories:
        if directory.exists() or directory.is_symlink():
            _require_private_directory(directory, str(directory.relative_to(store)))
        else:
            _make_directory(directory)
    marker = store / "format.json"
    marker_value = {"schema": STORE_SCHEMA, "boundaries": BOUNDARIES}
    if marker.exists() or marker.is_symlink():
        if _read_private_file_bounded(
            marker,
            "store format marker",
            MAX_METADATA_BYTES,
        ) != canonical_json(marker_value, pretty=True):
            raise EvidenceCaptureError("private store format marker does not match")
    else:
        _exclusive_file(marker, canonical_json(marker_value, pretty=True))
    for name in ("journal.jsonl", ".lock", ".metadata_never_index"):
        path = store / name
        if path.exists() or path.is_symlink():
            _require_private_regular_file(path, name)
        else:
            _exclusive_file(path)
    ledger = store / "expiry-ledger.json"
    if not ledger.exists() and not ledger.is_symlink():
        _exclusive_file(ledger, canonical_json(empty_expiry_ledger(), pretty=True))
    else:
        _require_private_regular_file(ledger, "expiry ledger")
    pending = store / PENDING_EVENT_NAME
    if pending.exists() or pending.is_symlink():
        _require_private_regular_file(pending, "pending event transaction")


def empty_expiry_ledger() -> dict[str, object]:
    return {
        "schema": LEDGER_SCHEMA,
        "journal_sha256": sha256_bytes(b""),
        "entries": [],
        "boundaries": BOUNDARIES,
    }


def _strict_event_keys(event: Mapping[str, object]) -> None:
    expected = {
        "schema",
        "sequence",
        "captured_at_utc",
        "captured_at_europe_london",
        "time_source",
        "trigger",
        "repository",
        "source",
        "objects",
        "disposition",
        "boundaries",
        "previous_event_sha256",
        "event_sha256",
    }
    if set(event) != expected:
        raise EvidenceCaptureError("journal event has unknown or missing fields")


def read_journal(path: Path) -> list[dict[str, Any]]:
    _require_private_regular_file(path, "journal")
    if path.stat().st_size > MAX_STORE_JOURNAL_BYTES:
        raise EvidenceCaptureError("journal exceeds the lifetime byte boundary")
    events: list[dict[str, Any]] = []
    previous: str | None = None
    with path.open("rb") as stream:
        for sequence, raw in enumerate(stream):
            if sequence >= MAX_STORE_EVENTS:
                raise EvidenceCaptureError("journal exceeds the lifetime event boundary")
            if len(raw) > MAX_METADATA_BYTES:
                raise EvidenceCaptureError("journal event exceeds the byte boundary")
            if not raw.endswith(b"\n"):
                raise EvidenceCaptureError("journal event is not newline terminated")
            value = parse_json(raw, f"journal event {sequence}")
            if not isinstance(value, dict):
                raise EvidenceCaptureError("journal event root must be an object")
            _strict_event_keys(value)
            if value["schema"] != EVENT_SCHEMA or value["sequence"] != sequence:
                raise EvidenceCaptureError("journal event schema or sequence is invalid")
            if value["previous_event_sha256"] != previous:
                raise EvidenceCaptureError("journal hash chain is discontinuous")
            core = dict(value)
            supplied = core.pop("event_sha256")
            expected = hashlib.sha256(JOURNAL_DOMAIN + canonical_json(core)[:-1]).hexdigest()
            if supplied != expected:
                raise EvidenceCaptureError("journal event digest does not match")
            if raw != canonical_json(value):
                raise EvidenceCaptureError("journal event is not canonical JSON")
            if value["boundaries"] != BOUNDARIES:
                raise EvidenceCaptureError("journal event crosses the preservation boundary")
            previous = supplied
            events.append(value)
    return events


def build_expiry_ledger(events: Sequence[Mapping[str, Any]], journal_raw: bytes) -> dict[str, object]:
    entries: list[dict[str, object]] = []
    for event in events:
        source = event["source"]
        if source["expires_at_utc"] is None:
            continue
        expiry = parse_time(source["expires_at_utc"], "source expiry")
        warning = expiry - WARNING_WINDOW
        entries.append(
            {
                "source_identity_sha256": source["identity_sha256"],
                "source_kind": source["kind"],
                "expires_at_utc": format_time(expiry),
                "warning_at_utc": format_time(warning),
                "expiry_basis": source["expiry_basis"],
                "disposition": event["disposition"]["status"],
                "captured": bool(event["objects"]),
            }
        )
    entries.sort(key=lambda item: (item["expires_at_utc"], item["source_identity_sha256"]))
    return {
        "schema": LEDGER_SCHEMA,
        "journal_sha256": sha256_bytes(journal_raw),
        "entries": entries,
        "boundaries": BOUNDARIES,
    }


def atomic_replace(path: Path, raw: bytes) -> None:
    parent = path.parent
    temporary = parent / f".{path.name}.{uuid.uuid4().hex}.tmp"
    _exclusive_file(temporary, raw)
    try:
        os.replace(temporary, path)
        descriptor = os.open(parent, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def _scan_secret_text(path: Path) -> None:
    decoder_tail = ""
    try:
        with path.open("r", encoding="utf-8") as stream:
            while True:
                chunk = stream.read(1024 * 1024)
                if not chunk:
                    break
                candidate = decoder_tail + chunk
                _scan_secret_string(candidate)
                decoder_tail = candidate[-SECRET_SCAN_OVERLAP_CHARACTERS:]
    except UnicodeDecodeError as error:
        raise EvidenceCaptureError("declared text source is not valid UTF-8") from error


def _scan_secret_string(value: str) -> None:
    for category, pattern in SECRET_PATTERNS:
        if pattern.search(value):
            raise SecretDetectedError(category)
    for category, pattern in STREAMING_SECRET_DETECTION_PATTERNS:
        if pattern.search(value):
            raise SecretDetectedError(category)


def _scan_utf16_secret_bytes(candidate: bytes) -> None:
    """Scan BOM-marked or strongly NUL-interleaved UTF-16 text."""

    for marker, encoding in ((b"\xff\xfe", "utf-16-le"), (b"\xfe\xff", "utf-16-be")):
        start = candidate.find(marker)
        if start >= 0:
            raw = candidate[start + len(marker) :]
            raw = raw[: len(raw) - len(raw) % 2]
            _scan_secret_string(raw.decode(encoding, errors="ignore"))

    for offset in (0, 1):
        raw = candidate[offset:]
        raw = raw[: len(raw) - len(raw) % 2]
        if len(raw) < 24:
            continue
        for encoding in ("utf-16-le", "utf-16-be"):
            _scan_secret_string(raw.decode(encoding, errors="ignore"))


def _scan_utf32_secret_bytes(candidate: bytes) -> None:
    """Scan unambiguously BOM-marked UTF-32 text."""

    for marker, encoding in (
        (b"\xff\xfe\x00\x00", "utf-32-le"),
        (b"\x00\x00\xfe\xff", "utf-32-be"),
    ):
        start = candidate.find(marker)
        if start < 0:
            continue
        raw = candidate[start + len(marker) :]
        raw = raw[: len(raw) - len(raw) % 4]
        _scan_secret_string(raw.decode(encoding, errors="ignore"))


def _scan_secret_binary_stream(stream: Any, *, prefix: bytes = b"") -> None:
    tail = b""
    chunk = prefix or stream.read(1024 * 1024)
    while chunk:
        candidate = tail + chunk
        if UNREDACTABLE_SECRET_PATTERN.search(candidate):
            raise SecretDetectedError("private-key")
        for category, pattern in FIXED_LENGTH_REDACTION_PATTERNS:
            if pattern.search(candidate):
                raise SecretDetectedError(category)
        for category, pattern in STREAMING_SECRET_DETECTION_BYTE_PATTERNS:
            if pattern.search(candidate):
                raise SecretDetectedError(category)
        _scan_utf32_secret_bytes(candidate)
        _scan_utf16_secret_bytes(candidate)
        tail = candidate[-SECRET_SCAN_OVERLAP_BYTES:]
        chunk = stream.read(1024 * 1024)


def _scan_zip_archive(path: Path) -> None:
    """Scan bounded ZIP members without extracting them to the filesystem."""

    try:
        with path.open("rb") as raw_stream:
            _scan_secret_binary_stream(raw_stream)
        with zipfile.ZipFile(path) as archive:
            entries = archive.infolist()
            if len(entries) > MAX_ARCHIVE_SCAN_ENTRIES:
                raise EvidenceCaptureError("ZIP archive exceeds the entry boundary")
            uncompressed = sum(item.file_size for item in entries)
            if uncompressed > MAX_ARCHIVE_SCAN_UNCOMPRESSED_BYTES:
                raise EvidenceCaptureError("ZIP archive exceeds the scan byte boundary")
            metadata_bytes = len(archive.comment)
            _scan_secret_binary_stream(io.BytesIO(archive.comment))
            for item in entries:
                encoded_name = item.filename.encode("utf-8", errors="surrogatepass")
                metadata_bytes += (
                    len(encoded_name) + len(item.comment) + len(item.extra)
                )
                if metadata_bytes > MAX_ARCHIVE_SCAN_METADATA_BYTES:
                    raise EvidenceCaptureError("ZIP archive exceeds the metadata boundary")
                _scan_secret_string(item.filename)
                _scan_secret_binary_stream(io.BytesIO(item.comment))
                _scan_secret_binary_stream(io.BytesIO(item.extra))
                if item.is_dir() and (item.file_size != 0 or item.compress_size != 0):
                    raise EvidenceCaptureError(
                        "ZIP directory entries cannot contain a compressed payload"
                    )
                if item.is_dir():
                    continue
                if item.flag_bits & 0x1:
                    raise EvidenceCaptureError("encrypted ZIP members cannot be inspected")
                with archive.open(item, "r") as stream:
                    prefix = stream.read(512)
                    suffix = Path(item.filename).suffix.lower()
                    nested_zip = zipfile.is_zipfile(stream)
                    if (
                        suffix in PRIVATE_KEY_CONTAINER_SUFFIXES
                        or _looks_like_der_container(prefix, item.file_size)
                        or prefix.startswith((b"\xfe\xed\xfe\xed", b"\xce\xce\xce\xce"))
                    ):
                        raise SecretDetectedError("private-key-container")
                    if (
                        suffix == ".zip"
                        or suffix in UNINSPECTABLE_ARCHIVE_SUFFIXES
                        or _archive_format_from_header(prefix) is not None
                        or nested_zip
                    ):
                        raise EvidenceCaptureError(
                            "nested archive or compressed members are not permitted"
                        )
                    stream.seek(0)
                    if _embedded_archive_format_from_stream(stream) is not None:
                        raise EvidenceCaptureError(
                            "nested archive or compressed members are not permitted"
                        )
                    stream.seek(len(prefix))
                    _scan_secret_binary_stream(stream, prefix=prefix)
    except SecretDetectedError:
        raise
    except EvidenceCaptureError:
        raise
    except (zipfile.BadZipFile, zipfile.LargeZipFile, RuntimeError) as error:
        raise EvidenceCaptureError("ZIP archive cannot be inspected safely") from error


def _archive_format_from_header(header: bytes) -> str | None:
    if header[:4] in {b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08"}:
        return "zip"
    if header.startswith(b"\x1f\x8b"):
        return "gzip"
    if header.startswith(b"BZh"):
        return "bzip2"
    if header.startswith(b"\xfd7zXZ\x00"):
        return "xz"
    if header.startswith(b"7z\xbc\xaf'\x1c"):
        return "7z"
    if header.startswith(b"Rar!\x1a\x07"):
        return "rar"
    if header.startswith(b"\x28\xb5\x2f\xfd"):
        return "zstd"
    if _looks_like_pkcs12(header):
        return "pkcs12"
    if len(header) >= 262 and header[257:262] == b"ustar":
        return "tar"
    return None


def _archive_format_from_magic(path: Path) -> str | None:
    with path.open("rb") as stream:
        return _archive_format_from_header(stream.read(512))


def _der_content_offset(raw: bytes, offset: int) -> int | None:
    """Return the content offset for one bounded DER item, or ``None``."""

    if offset + 2 > len(raw):
        return None
    length = raw[offset + 1]
    if length < 0x80:
        return offset + 2
    length_bytes = length & 0x7F
    if length_bytes < 1 or length_bytes > 4 or offset + 2 + length_bytes > len(raw):
        return None
    return offset + 2 + length_bytes


def _looks_like_der_container(header: bytes, total_bytes: int) -> bool:
    """Conservatively recognise a complete DER SEQUENCE container."""

    if len(header) < 2 or header[0] != 0x30 or total_bytes < 2:
        return False
    first_length = header[1]
    if first_length < 0x80:
        content_length = first_length
        header_length = 2
    else:
        length_bytes = first_length & 0x7F
        if length_bytes < 1 or length_bytes > 4 or len(header) < 2 + length_bytes:
            return False
        content_length = int.from_bytes(header[2 : 2 + length_bytes], "big")
        header_length = 2 + length_bytes
    return header_length + content_length == total_bytes


def _looks_like_pkcs12(header: bytes) -> bool:
    """Recognise the closed PFX envelope without parsing or decrypting its key bags."""

    if not header or header[0] != 0x30:
        return False
    pfx_content = _der_content_offset(header, 0)
    if pfx_content is None or header[pfx_content : pfx_content + 3] != b"\x02\x01\x03":
        return False
    content_info = pfx_content + 3
    if content_info >= len(header) or header[content_info] != 0x30:
        return False
    content_offset = _der_content_offset(header, content_info)
    if content_offset is None:
        return False
    # PKCS #7 data or encryptedData content type inside the PFX authSafe.
    return header[content_offset : content_offset + 11] in {
        b"\x06\x09\x2a\x86\x48\x86\xf7\x0d\x01\x07\x01",
        b"\x06\x09\x2a\x86\x48\x86\xf7\x0d\x01\x07\x06",
    }


_EMBEDDED_ARCHIVE_PATTERNS: tuple[tuple[str, re.Pattern[bytes]], ...] = (
    ("embedded-zip", re.compile(rb"PK\x03\x04")),
    (
        "pkcs12",
        re.compile(
            rb"\x02\x01\x03\x30(?:[\x00-\x7f]|\x81[\s\S]|\x82[\s\S]{2}|"
            rb"\x83[\s\S]{3}|\x84[\s\S]{4})"
            rb"\x06\x09\x2a\x86\x48\x86\xf7\x0d\x01\x07(?:\x01|\x06)"
        ),
    ),
    (
        "gzip",
        re.compile(
            rb"\x1f\x8b\x08[\x00-\x1f][\s\S]{4}[\x00\x02\x04](?:[\x00-\x0d]|\xff)"
        ),
    ),
    ("bzip2", re.compile(rb"BZh[1-9]1AY&SY")),
    ("xz", re.compile(rb"\xfd7zXZ\x00")),
    ("7z", re.compile(rb"7z\xbc\xaf\x27\x1c")),
    ("rar", re.compile(rb"Rar!\x1a\x07(?:\x00|\x01\x00)")),
    ("zstd", re.compile(rb"\x28\xb5\x2f\xfd")),
)


def _embedded_archive_format_from_stream(stream: Any) -> str | None:
    """Detect strong archive signatures anywhere in an already bounded stream."""

    tail = b""
    while chunk := stream.read(1024 * 1024):
        candidate = tail + chunk
        for archive_format, pattern in _EMBEDDED_ARCHIVE_PATTERNS:
            if pattern.search(candidate):
                return archive_format
        tail = candidate[-32:]
    return None


def _embedded_archive_format(path: Path) -> str | None:
    with path.open("rb") as stream:
        return _embedded_archive_format_from_stream(stream)


def _validate_redacted_jsonl(path: Path) -> None:
    _scan_secret_text(path)
    with path.open("rb") as stream:
        for line_number, raw in enumerate(stream, start=1):
            if len(raw) > 1024 * 1024:
                raise EvidenceCaptureError("redacted JSONL line exceeds 1 MiB")
            if not raw.strip():
                continue
            value = parse_json(raw, f"redacted JSONL line {line_number}")
            if not isinstance(value, dict):
                raise EvidenceCaptureError("each redacted JSONL line must be an object")


def redact_projection_bytes(raw: bytes) -> tuple[bytes, list[str], int]:
    """Redact one canonical projection record before it reaches the filesystem."""

    if UNREDACTABLE_SECRET_PATTERN.search(raw):
        raise UnredactableSecretError("private-key-block")
    mutable = bytearray(raw)
    spans: list[tuple[int, int, str]] = []
    for category, pattern in FIXED_LENGTH_REDACTION_PATTERNS:
        for match in pattern.finditer(raw):
            start, end = match.span(1)
            spans.append((start, end, category))
    spans.sort(key=lambda item: (item[0], -(item[1] - item[0])))
    categories: dict[str, int] = {}
    previous_end = -1
    for start, end, category in spans:
        if start < previous_end:
            continue
        mutable[start:end] = b"X" * (end - start)
        categories[category] = categories.get(category, 0) + 1
        previous_end = end
    return bytes(mutable), sorted(categories), sum(categories.values())


def redact_clone_in_place(path: Path) -> tuple[list[str], int]:
    """Redact high-confidence ASCII values without changing file length."""

    descriptor = os.open(path, os.O_RDWR | getattr(os, "O_NOFOLLOW", 0))
    categories: dict[str, int] = {}
    try:
        size = os.fstat(descriptor).st_size
        if size == 0:
            return [], 0
        with mmap.mmap(descriptor, 0, access=mmap.ACCESS_WRITE) as content:
            if UNREDACTABLE_SECRET_PATTERN.search(content):
                raise UnredactableSecretError("private-key-block")
            spans: list[tuple[int, int, str]] = []
            for category, pattern in FIXED_LENGTH_REDACTION_PATTERNS:
                for match in pattern.finditer(content):
                    start, end = match.span(1)
                    spans.append((start, end, category))
            spans.sort(key=lambda item: (item[0], -(item[1] - item[0])))
            previous_end = -1
            for start, end, category in spans:
                if start < previous_end:
                    continue
                content[start:end] = b"X" * (end - start)
                categories[category] = categories.get(category, 0) + 1
                previous_end = end
            content.flush()
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return sorted(categories), sum(categories.values())


def rehash_staged(path: Path) -> StagedObject:
    metadata = path.lstat()
    if path.is_symlink() or not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
        raise EvidenceCaptureError("redacted clone is not one regular file")
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
            total += len(chunk)
    return StagedObject(path, digest.hexdigest(), total)


@dataclass(frozen=True)
class StagedObject:
    path: Path
    sha256: str
    bytes: int
    source_stat_before: dict[str, int] | None = None
    source_stat_after: dict[str, int] | None = None
    source_changed_during_copy: bool | None = None


@dataclass(frozen=True)
class CloneSnapshot:
    staged: StagedObject
    source_stat_before: dict[str, int]
    source_stat_after: dict[str, int]
    source_changed_after_snapshot: bool


@dataclass(frozen=True)
class TransientClone:
    descriptor: int
    source_stat_before: dict[str, int]
    source_stat_after: dict[str, int]
    source_changed_after_snapshot: bool


def _source_signature(
    metadata: os.stat_result,
) -> tuple[int, int, int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_nlink,
        metadata.st_uid,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _source_identity_signature(metadata: os.stat_result) -> tuple[int, int, int, int, int]:
    """Fields which must not change when an active rollout merely appends."""

    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_nlink,
        metadata.st_uid,
    )


def _recorded_source_stat(metadata: os.stat_result) -> dict[str, int]:
    return {
        "device": metadata.st_dev,
        "inode": metadata.st_ino,
        "mode": stat.S_IMODE(metadata.st_mode),
        "links": metadata.st_nlink,
        "owner_uid": metadata.st_uid,
        "bytes": metadata.st_size,
        "mtime_ns": metadata.st_mtime_ns,
        "ctime_ns": metadata.st_ctime_ns,
    }


def _validate_local_source_metadata(path: Path, metadata: os.stat_result) -> None:
    if path.is_symlink() or not stat.S_ISREG(metadata.st_mode):
        raise EvidenceCaptureError("source must be a regular file, not a link or special file")
    if metadata.st_nlink != 1:
        raise EvidenceCaptureError("source must not be hard linked")


def _filesystem_type(path: Path) -> str:
    """Return the macOS filesystem personality without evaluating shell text."""

    if sys.platform != "darwin":
        raise EvidenceCaptureError("APFS filesystem inspection is available only on macOS")
    filesystem, mount_point, _ = _macos_mount_metadata(path)
    value = _macos_diskutil_info(filesystem, mount_point)
    personality = value.get("FilesystemType") or value.get("FilesystemName")
    if not isinstance(personality, str):
        raise EvidenceCaptureError("filesystem identity does not name its type")
    return personality.lower()


def _macos_clonefile(source: Path, destination: Path) -> None:
    """Call fclonefileat(2) with CLONE_NOOWNERCOPY and no copy fallback."""

    if sys.platform != "darwin":
        raise EvidenceCaptureError("APFS clone capture is available only on macOS")
    libc = ctypes.CDLL(None, use_errno=True)
    try:
        clonefile = libc.fclonefileat
    except AttributeError as error:
        raise EvidenceCaptureError("fclonefileat(2) is unavailable") from error
    clonefile.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
    clonefile.restype = ctypes.c_int
    clone_noownercopy = 0x0002
    source_descriptor = os.open(source, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    directory_descriptor = os.open(destination.parent, os.O_RDONLY)
    try:
        result = clonefile(
            source_descriptor,
            directory_descriptor,
            os.fsencode(destination.name),
            clone_noownercopy,
        )
        if result != 0:
            error_number = ctypes.get_errno()
            message = os.strerror(error_number) if error_number else "unknown clonefile error"
            raise EvidenceCaptureError(f"APFS fclonefileat capture failed: {message}")
    finally:
        os.close(directory_descriptor)
        os.close(source_descriptor)


def stage_apfs_clone(
    source: Path,
    incoming: Path,
    *,
    clone_function: Callable[[Path, Path], None] | None = None,
    filesystem_type_function: Callable[[Path], str] | None = None,
    after_clone_hook: Callable[[], None] | None = None,
) -> CloneSnapshot:
    """Create and hash one same-device, owner-only APFS clone snapshot.

    Test callers may inject the two platform operations. Production never falls
    back to a byte copy when APFS or clonefile is unavailable.
    """

    before = source.lstat()
    _validate_local_source_metadata(source, before)
    if before.st_uid != os.getuid() or stat.S_IMODE(before.st_mode) & 0o022:
        raise EvidenceCaptureError(
            "APFS clone source must be owned by the current user and not group/other writable"
        )
    incoming_metadata = incoming.lstat()
    if before.st_dev != incoming_metadata.st_dev:
        raise EvidenceCaptureError("APFS clone source and private store must share one device")
    identify = filesystem_type_function or _filesystem_type
    if identify(source).lower() != "apfs" or identify(incoming).lower() != "apfs":
        raise EvidenceCaptureError("APFS clone capture requires APFS on source and store")
    destination = incoming / f"{uuid.uuid4().hex}.clone"
    clone = clone_function or _macos_clonefile
    try:
        clone(source, destination)
        cloned = destination.lstat()
        if destination.is_symlink() or not stat.S_ISREG(cloned.st_mode) or cloned.st_nlink != 1:
            raise EvidenceCaptureError("clonefile did not create one regular private snapshot")
        if cloned.st_size != before.st_size:
            raise EvidenceCaptureError("clonefile snapshot size does not match the source snapshot")
        os.chmod(destination, 0o600, follow_symlinks=False)
        if after_clone_hook is not None:
            after_clone_hook()
        after = source.lstat()
        digest = hashlib.sha256()
        total = 0
        descriptor = os.open(destination, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        try:
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_OBJECT_BYTES:
                    raise EvidenceCaptureError("APFS clone snapshot exceeds the byte boundary")
                digest.update(chunk)
        finally:
            os.close(descriptor)
        return CloneSnapshot(
            staged=StagedObject(destination, digest.hexdigest(), total),
            source_stat_before=_recorded_source_stat(before),
            source_stat_after=_recorded_source_stat(after),
            source_changed_after_snapshot=_source_signature(before) != _source_signature(after),
        )
    except Exception:
        destination.unlink(missing_ok=True)
        raise


def create_transient_apfs_clone(
    source: Path,
    incoming: Path,
    *,
    clone_function: Callable[[Path, Path], None] | None = None,
    filesystem_type_function: Callable[[Path], str] | None = None,
    expected_source_metadata: os.stat_result | None = None,
) -> TransientClone:
    """Create a private APFS COW read source without retaining or byte-copying it."""

    before = source.lstat()
    _validate_local_source_metadata(source, before)
    if expected_source_metadata is not None:
        if _source_identity_signature(before) != _source_identity_signature(
            expected_source_metadata
        ):
            raise EvidenceCaptureError("Codex source identity changed after inventory")
        if before.st_size < expected_source_metadata.st_size:
            raise EvidenceCaptureError("Codex source was truncated after inventory")
    if before.st_uid != os.getuid() or stat.S_IMODE(before.st_mode) & 0o022:
        raise EvidenceCaptureError(
            "Codex source must be owned by the current user and not group/other writable"
        )
    incoming_metadata = incoming.lstat()
    if before.st_dev != incoming_metadata.st_dev:
        raise EvidenceCaptureError("Codex source and private store must share one device")
    identify = filesystem_type_function or _filesystem_type
    if identify(source).lower() != "apfs" or identify(incoming).lower() != "apfs":
        raise EvidenceCaptureError("Codex projection requires APFS COW cloning")
    destination = incoming / f"{uuid.uuid4().hex}.transient-clone"
    clone = clone_function or _macos_clonefile
    clone_descriptor: int | None = None
    try:
        clone(source, destination)
        cloned = destination.lstat()
        if destination.is_symlink() or not stat.S_ISREG(cloned.st_mode) or cloned.st_nlink != 1:
            raise EvidenceCaptureError("clonefile did not create one regular transient clone")
        if cloned.st_size != before.st_size:
            raise EvidenceCaptureError("transient clone size does not match the source snapshot")
        os.chmod(destination, 0o600, follow_symlinks=False)
        clone_descriptor = os.open(
            destination, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        )
        opened = os.fstat(clone_descriptor)
        if not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1:
            raise EvidenceCaptureError("transient clone descriptor is not one regular file")
        destination.unlink()
        after = source.lstat()
        if _source_identity_signature(after) != _source_identity_signature(before):
            raise EvidenceCaptureError("Codex source identity changed while cloning")
        return TransientClone(
            descriptor=clone_descriptor,
            source_stat_before=_recorded_source_stat(before),
            source_stat_after=_recorded_source_stat(after),
            source_changed_after_snapshot=_source_signature(before) != _source_signature(after),
        )
    except Exception:
        if clone_descriptor is not None:
            os.close(clone_descriptor)
        destination.unlink(missing_ok=True)
        raise


def stage_regular_file(
    source: Path,
    incoming: Path,
    *,
    max_bytes: int = MAX_OBJECT_BYTES,
    after_read_hook: Callable[[], None] | None = None,
) -> StagedObject:
    before = source.lstat()
    _validate_local_source_metadata(source, before)
    if before.st_size > max_bytes:
        raise EvidenceCaptureError("source exceeds the configured byte boundary")
    descriptor = os.open(source, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    temporary = incoming / uuid.uuid4().hex
    target = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    digest = hashlib.sha256()
    total = 0
    try:
        opened = os.fstat(descriptor)
        if _source_signature(opened) != _source_signature(before):
            raise EvidenceCaptureError("source identity changed before capture")
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise EvidenceCaptureError("source exceeds the configured byte boundary")
            digest.update(chunk)
            view = memoryview(chunk)
            while view:
                written = os.write(target, view)
                view = view[written:]
        os.fsync(target)
        if after_read_hook is not None:
            after_read_hook()
        after_fd = os.fstat(descriptor)
        after_path = source.lstat()
        if (
            _source_signature(before) != _source_signature(after_fd)
            or _source_signature(before) != _source_signature(after_path)
        ):
            raise EvidenceCaptureError("source changed while it was being captured")
    except Exception:
        os.close(target)
        os.close(descriptor)
        temporary.unlink(missing_ok=True)
        raise
    os.close(target)
    os.close(descriptor)
    return StagedObject(
        temporary,
        digest.hexdigest(),
        total,
        _recorded_source_stat(before),
        _recorded_source_stat(after_path),
        False,
    )


def stage_bytes(raw: bytes, incoming: Path, *, max_bytes: int) -> StagedObject:
    if len(raw) > max_bytes:
        raise EvidenceCaptureError("source exceeds the configured byte boundary")
    temporary = incoming / uuid.uuid4().hex
    _exclusive_file(temporary, raw)
    return StagedObject(temporary, sha256_bytes(raw), len(raw))


def detect_media_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".json", ".jsonl", ".ndjson"}:
        return "application/json" if suffix == ".json" else "application/x-ndjson"
    if suffix == ".zip":
        return "application/zip"
    if suffix == ".png":
        return "image/png"
    if suffix in TEXT_SUFFIXES:
        return "text/plain; charset=utf-8"
    return "application/octet-stream"


def _bounded_zlib_metadata(raw: bytes, label: str) -> bytes:
    decompressor = zlib.decompressobj()
    output = decompressor.decompress(raw, MAX_PNG_METADATA_BYTES + 1)
    if len(output) > MAX_PNG_METADATA_BYTES or decompressor.unconsumed_tail:
        raise EvidenceCaptureError(f"PNG {label} exceeds the metadata boundary")
    output += decompressor.flush(MAX_PNG_METADATA_BYTES + 1 - len(output))
    if (
        len(output) > MAX_PNG_METADATA_BYTES
        or not decompressor.eof
        or decompressor.unused_data
    ):
        raise EvidenceCaptureError(f"PNG {label} is not one bounded zlib stream")
    return output


def _scan_png_metadata(chunk_type: bytes, content: bytes) -> None:
    _scan_secret_binary_stream(io.BytesIO(content))
    compressed: bytes | None = None
    label = chunk_type.decode("ascii")
    if chunk_type in {b"zTXt", b"iCCP"}:
        _prefix, separator, remainder = content.partition(b"\x00")
        if not separator or not remainder or remainder[0] != 0:
            raise EvidenceCaptureError(f"PNG {label} metadata is invalid")
        compressed = remainder[1:]
    elif chunk_type == b"iTXt":
        _keyword, separator, remainder = content.partition(b"\x00")
        if not separator or len(remainder) < 2:
            raise EvidenceCaptureError("PNG iTXt metadata is invalid")
        compression_flag, compression_method = remainder[0], remainder[1]
        _language, separator, remainder = remainder[2:].partition(b"\x00")
        _translated, translated_separator, text_value = remainder.partition(b"\x00")
        if not separator or not translated_separator:
            raise EvidenceCaptureError("PNG iTXt metadata is invalid")
        if compression_flag == 1 and compression_method == 0:
            compressed = text_value
        elif compression_flag != 0 or compression_method != 0:
            raise EvidenceCaptureError("PNG iTXt compression marker is invalid")
    if compressed is not None:
        expanded = _bounded_zlib_metadata(compressed, label)
        _scan_secret_binary_stream(io.BytesIO(expanded))


def _validate_png(path: Path) -> None:
    """Stream-validate one PNG and scan its bounded metadata containers."""

    metadata = path.stat()
    if metadata.st_size > MAX_OBJECT_BYTES:
        raise EvidenceCaptureError("PNG source exceeds the byte boundary")
    with path.open("rb") as stream:
        if stream.read(8) != b"\x89PNG\r\n\x1a\n":
            raise EvidenceCaptureError("PNG source has an invalid signature")
        chunks = 0
        saw_header = False
        saw_image_data = False
        saw_end = False
        while True:
            header = stream.read(8)
            if not header:
                break
            if len(header) != 8:
                raise EvidenceCaptureError("PNG source is truncated")
            length = int.from_bytes(header[:4], "big")
            chunk_type = header[4:]
            if not re.fullmatch(rb"[A-Za-z]{4}", chunk_type):
                raise EvidenceCaptureError("PNG source has an invalid chunk")
            chunks += 1
            if chunks > MAX_ARCHIVE_SCAN_ENTRIES:
                raise EvidenceCaptureError("PNG source exceeds the chunk boundary")
            if chunks == 1:
                if chunk_type != b"IHDR" or length != 13:
                    raise EvidenceCaptureError("PNG source has no canonical header")
                saw_header = True
            if chunk_type != b"IDAT" and length > MAX_PNG_METADATA_BYTES:
                raise EvidenceCaptureError("PNG metadata exceeds the byte boundary")
            retained = bytearray() if chunk_type != b"IDAT" else None
            checksum = zlib.crc32(chunk_type)
            remaining = length
            while remaining:
                block = stream.read(min(1024 * 1024, remaining))
                if not block:
                    raise EvidenceCaptureError("PNG source is truncated")
                checksum = zlib.crc32(block, checksum)
                if retained is not None:
                    retained.extend(block)
                remaining -= len(block)
            expected_crc = stream.read(4)
            if len(expected_crc) != 4:
                raise EvidenceCaptureError("PNG source is truncated")
            if checksum & 0xFFFFFFFF != int.from_bytes(expected_crc, "big"):
                raise EvidenceCaptureError("PNG source has an invalid chunk checksum")
            if chunk_type == b"IDAT":
                saw_image_data = True
            elif retained is not None:
                _scan_png_metadata(chunk_type, bytes(retained))
            if chunk_type == b"IEND":
                if length != 0 or stream.read(1):
                    raise EvidenceCaptureError("PNG source has invalid trailing content")
                saw_end = True
                break
        if not saw_header or not saw_image_data or not saw_end:
            raise EvidenceCaptureError("PNG source is incomplete")


def _validate_jpeg(path: Path) -> None:
    """Validate a bounded JPEG container and scan all non-pixel segments."""

    metadata = path.stat()
    if metadata.st_size > MAX_JPEG_BYTES:
        raise EvidenceCaptureError("JPEG source exceeds the byte boundary")
    with path.open("rb") as stream:
        if stream.read(2) != b"\xff\xd8":
            raise EvidenceCaptureError("JPEG source has an invalid signature")
        in_scan = False
        pending_marker: int | None = None
        saw_scan = False
        segments = 0
        while True:
            if in_scan:
                while True:
                    value = stream.read(1)
                    if not value:
                        raise EvidenceCaptureError("JPEG source is incomplete")
                    if value != b"\xff":
                        continue
                    marker = stream.read(1)
                    while marker == b"\xff":
                        marker = stream.read(1)
                    if not marker:
                        raise EvidenceCaptureError("JPEG source is incomplete")
                    marker_value = marker[0]
                    if marker_value == 0 or 0xD0 <= marker_value <= 0xD7:
                        continue
                    pending_marker = marker_value
                    in_scan = False
                    break
            if pending_marker is None:
                prefix = stream.read(1)
                if prefix != b"\xff":
                    raise EvidenceCaptureError("JPEG source has an invalid marker")
                marker = stream.read(1)
                while marker == b"\xff":
                    marker = stream.read(1)
                if not marker or marker == b"\x00":
                    raise EvidenceCaptureError("JPEG source has an invalid marker")
                marker_value = marker[0]
            else:
                marker_value = pending_marker
                pending_marker = None
            segments += 1
            if segments > MAX_ARCHIVE_SCAN_ENTRIES:
                raise EvidenceCaptureError("JPEG source exceeds the segment boundary")
            if marker_value == 0xD9:
                if not saw_scan or stream.read(1):
                    raise EvidenceCaptureError("JPEG source has invalid trailing content")
                return
            if marker_value == 0xD8:
                raise EvidenceCaptureError("JPEG source contains a nested start marker")
            if marker_value == 0x01 or 0xD0 <= marker_value <= 0xD7:
                continue
            length_raw = stream.read(2)
            if len(length_raw) != 2:
                raise EvidenceCaptureError("JPEG source is truncated")
            length = int.from_bytes(length_raw, "big")
            if length < 2:
                raise EvidenceCaptureError("JPEG source has an invalid segment")
            content = stream.read(length - 2)
            if len(content) != length - 2:
                raise EvidenceCaptureError("JPEG source is truncated")
            _scan_secret_binary_stream(io.BytesIO(content))
            if marker_value == 0xDA:
                saw_scan = True
                in_scan = True


def _sanitise_journal_label(value: str) -> tuple[str, list[str], int]:
    """Remove high-confidence secrets from source labels before journalling."""

    sanitised = value
    categories: list[str] = []
    count = 0
    for category, pattern in SECRET_PATTERNS:
        def replacement(match: re.Match[str], *, category: str = category) -> str:
            raw = match.group(0).encode("utf-8")
            return f"[redacted-{category}-sha256:{sha256_bytes(raw)}]"

        sanitised, occurrences = pattern.subn(replacement, sanitised)
        if occurrences:
            categories.extend([f"journal-label:{category}"] * occurrences)
            count += occurrences
    return sanitised, sorted(set(categories)), count


def _source_value(
    *,
    kind: str,
    identity: str,
    label: str,
    occurred_at_utc: str | None,
    expires_at_utc: str | None,
    expiry_basis: str,
    commit_sha: str | None,
    tree_sha: str | None,
    redaction_mode: str,
    snapshot_method: str,
    source_stat_before: dict[str, int] | None,
    source_stat_after: dict[str, int] | None,
    source_changed_after_snapshot: bool | None,
    collection_generation_sha256: str | None,
    collection_window: dict[str, object] | None,
    redaction_categories: list[str],
    redaction_count: int,
) -> dict[str, object]:
    label, label_categories, label_count = _sanitise_journal_label(label)
    return {
        "kind": kind,
        "identity": identity,
        "identity_sha256": source_identity_sha256(identity),
        "immutability": "strict-immutable",
        "label": label,
        "occurred_at_utc": occurred_at_utc,
        "expires_at_utc": expires_at_utc,
        "expiry_basis": expiry_basis,
        "commit_sha": commit_sha,
        "tree_sha": tree_sha,
        "redaction_mode": redaction_mode,
        "snapshot_method": snapshot_method,
        "source_stat_before": source_stat_before,
        "source_stat_after": source_stat_after,
        "source_changed_after_snapshot": source_changed_after_snapshot,
        "collection_generation_sha256": collection_generation_sha256,
        "collection_window": collection_window,
        "redaction_categories": sorted(set(redaction_categories + label_categories)),
        "redaction_count": redaction_count + label_count,
    }


def _event_fingerprint(event: Mapping[str, Any]) -> tuple[object, ...]:
    return (
        event["source"],
        event["objects"],
        event["disposition"],
        event["repository"],
    )


_INCOMING_TOOL_FILE = re.compile(
    r"^[0-9a-f]{32}(?:\.(?:clone|transient-clone|projection\.jsonl|jsonl\.gz|download))?$"
)


def _clean_stale_incoming(
    incoming: Path,
    *,
    preserve_names: set[str] | None = None,
) -> None:
    """Remove only recognisable interrupted-capture files under the store lock."""

    for candidate in incoming.iterdir():
        metadata = candidate.lstat()
        if not _INCOMING_TOOL_FILE.fullmatch(candidate.name):
            raise EvidenceCaptureError("private store contains an unknown incoming file")
        if preserve_names is not None and candidate.name in preserve_names:
            continue
        if (
            candidate.is_symlink()
            or not stat.S_ISREG(metadata.st_mode)
            or metadata.st_nlink != 1
            or metadata.st_uid != os.getuid()
        ):
            raise EvidenceCaptureError("private store contains an unsafe stale incoming file")
        os.chmod(candidate, 0o600, follow_symlinks=False)
        candidate.unlink()


def _pending_regular_metadata(
    path: Path,
    label: str,
    *,
    allowed_links: set[int],
) -> os.stat_result:
    metadata = path.lstat()
    if path.is_symlink() or not stat.S_ISREG(metadata.st_mode):
        raise EvidenceCaptureError(f"{label} must be a regular file")
    if metadata.st_nlink not in allowed_links:
        raise EvidenceCaptureError(f"{label} has an unexpected hard-link topology")
    if stat.S_IMODE(metadata.st_mode) != 0o600:
        raise EvidenceCaptureError(f"{label} must have mode 0600")
    if metadata.st_uid != os.getuid():
        raise EvidenceCaptureError(f"{label} must be owned by the current user")
    _require_no_unindexed_metadata(path, label)
    return metadata


def _validate_bound_object_file(
    path: Path,
    label: str,
    *,
    expected_device: int,
    expected_inode: int,
    expected_sha256: str,
    expected_bytes: int,
    allowed_links: set[int],
) -> os.stat_result:
    metadata = _pending_regular_metadata(path, label, allowed_links=allowed_links)
    if metadata.st_dev != expected_device or metadata.st_ino != expected_inode:
        raise EvidenceCaptureError(f"{label} does not match the pending inode binding")
    if metadata.st_size != expected_bytes:
        raise EvidenceCaptureError(f"{label} does not match the pending byte count")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    digest = hashlib.sha256()
    try:
        opened = os.fstat(descriptor)
        if (
            opened.st_dev != metadata.st_dev
            or opened.st_ino != metadata.st_ino
            or opened.st_uid != metadata.st_uid
            or _source_signature(opened) != _source_signature(metadata)
        ):
            raise EvidenceCaptureError(f"{label} changed while it was opened")
        total = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > expected_bytes:
                raise EvidenceCaptureError(f"{label} exceeds the pending byte count")
            digest.update(chunk)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = path.lstat()
    if (
        current.st_uid != metadata.st_uid
        or _source_signature(current) != _source_signature(metadata)
        or _source_signature(after) != _source_signature(metadata)
    ):
        raise EvidenceCaptureError(f"{label} changed while it was verified")
    if total != expected_bytes or digest.hexdigest() != expected_sha256:
        raise EvidenceCaptureError(f"{label} does not match the pending content binding")
    _require_no_unindexed_metadata(path, label)
    return metadata


def _validated_journal_prefix(raw: bytes) -> list[dict[str, Any]]:
    """Validate the complete journal prefix named by a pending transaction."""

    if len(raw) > MAX_STORE_JOURNAL_BYTES:
        raise EvidenceCaptureError("journal exceeds the lifetime byte boundary")
    if raw and not raw.endswith(b"\n"):
        raise EvidenceCaptureError("pending transaction journal prefix is incomplete")
    events: list[dict[str, Any]] = []
    previous: str | None = None
    for sequence, line in enumerate(raw.splitlines(keepends=True)):
        if sequence >= MAX_STORE_EVENTS:
            raise EvidenceCaptureError("journal exceeds the lifetime event boundary")
        if len(line) > MAX_METADATA_BYTES:
            raise EvidenceCaptureError("journal event exceeds the byte boundary")
        value = parse_json(line, f"journal event {sequence}")
        if not isinstance(value, dict):
            raise EvidenceCaptureError("journal event root must be an object")
        _strict_event_keys(value)
        if value["schema"] != EVENT_SCHEMA or value["sequence"] != sequence:
            raise EvidenceCaptureError("journal event schema or sequence is invalid")
        if value["previous_event_sha256"] != previous:
            raise EvidenceCaptureError("journal hash chain is discontinuous")
        core = dict(value)
        supplied = core.pop("event_sha256")
        expected = hashlib.sha256(JOURNAL_DOMAIN + canonical_json(core)[:-1]).hexdigest()
        if supplied != expected:
            raise EvidenceCaptureError("journal event digest does not match")
        if line != canonical_json(value):
            raise EvidenceCaptureError("journal event is not canonical JSON")
        if value["boundaries"] != BOUNDARIES:
            raise EvidenceCaptureError("journal event crosses the preservation boundary")
        previous = supplied
        events.append(value)
    return events


@dataclass(frozen=True)
class StagedCapture:
    """One already-staged captured event in an ordered store transaction."""

    staged: StagedObject
    trigger: str
    repository: str | None
    source: dict[str, object]
    role: str
    media_type: str
    opaque: bool
    secret_scan: str
    secret_scan_performed: bool
    sensitivity: str
    captured_at: datetime | None = None


@dataclass(frozen=True)
class ObjectlessCapture:
    """One excluded or unavailable event in an ordered store transaction."""

    trigger: str
    repository: str | None
    source: dict[str, object]
    status_value: str
    reason: str
    captured_at: datetime | None = None


class EvidenceStore:
    """Locked writer for the private delivery-evidence store."""

    def __init__(
        self,
        root: Path,
        *,
        max_capture_bytes: int = DEFAULT_CAPTURE_MAX_BYTES,
        fault_injector: Callable[[str], None] | None = None,
    ) -> None:
        self.root = root
        self.max_capture_bytes = max_capture_bytes
        self.lock_stream: Any = None
        self.events: list[dict[str, Any]] = []
        self.identities: dict[str, dict[str, Any]] = {}
        self.captured = 0
        self.no_op = 0
        self.excluded = 0
        self.unavailable = 0
        self.captured_bytes = 0
        self.transferred_bytes = 0
        self.github_api_invocations = 0
        self.github_metadata_bytes = 0
        self.capture_events = 0
        self.capture_metadata_bytes = 0
        self.github_capture_started = time.monotonic()
        self.fault_injector = fault_injector

    def __enter__(self) -> "EvidenceStore":
        initialise_store(self.root)
        self.lock_stream = (self.root / ".lock").open("r+b")
        fcntl.flock(self.lock_stream.fileno(), fcntl.LOCK_EX)
        try:
            pending = self._read_pending_transaction()
            preserve_names: set[str] = set()
            if pending is not None:
                preserve_names = {
                    str(binding["staged_name"])
                    for binding in pending["objects"]
                    if binding is not None
                }
            _clean_stale_incoming(
                self.root / ".incoming",
                preserve_names=preserve_names,
            )
            if pending is not None:
                self._complete_pending_transaction(pending)
            _clean_stale_incoming(self.root / ".incoming")
            self.events = read_journal(self.root / "journal.jsonl")
            for event in self.events:
                identity = event["source"]["identity"]
                if identity in self.identities:
                    raise EvidenceCaptureError(
                        "journal contains a duplicate immutable source identity"
                    )
                self.identities[identity] = event
            self._refresh_ledger()
        except Exception:
            self._close_lock()
            raise
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self._close_lock()

    def _close_lock(self) -> None:
        if self.lock_stream is not None:
            fcntl.flock(self.lock_stream.fileno(), fcntl.LOCK_UN)
            self.lock_stream.close()
            self.lock_stream = None

    @property
    def incoming(self) -> Path:
        return self.root / ".incoming"

    def already_captured(self, identity: str) -> bool:
        existing = self.identities.get(identity)
        if existing is None or existing["disposition"]["status"] != "captured":
            return False
        self.no_op += 1
        return True

    @property
    def remaining_transfer_bytes(self) -> int:
        retained_budget = max(
            0,
            self.max_capture_bytes
            - self.captured_bytes
            - self.capture_metadata_bytes,
        )
        transfer_budget = max(0, self.max_capture_bytes - self.transferred_bytes)
        return min(retained_budget, transfer_budget)

    def require_staging_capacity(self, planned_bytes: int) -> None:
        if (
            not isinstance(planned_bytes, int)
            or isinstance(planned_bytes, bool)
            or planned_bytes < 0
        ):
            raise EvidenceCaptureError("planned staging size is invalid")
        if (
            self.captured_bytes
            + self.capture_metadata_bytes
            + planned_bytes
            > self.max_capture_bytes
        ):
            raise EvidenceCaptureError("capture exceeds the per-invocation byte boundary")
        if shutil.disk_usage(self.root).free < MIN_STORE_FREE_BYTES + planned_bytes:
            raise EvidenceCaptureError(
                "private store lacks free-space reserve for the planned staging operation"
            )

    def note_transfer(self, byte_count: int) -> None:
        if (
            not isinstance(byte_count, int)
            or isinstance(byte_count, bool)
            or byte_count < 0
        ):
            raise EvidenceCaptureError("transfer byte count is invalid")
        if self.transferred_bytes + byte_count > self.max_capture_bytes:
            self.transferred_bytes = self.max_capture_bytes
            raise EvidenceCaptureError("GitHub transfers exceed the invocation byte boundary")
        if shutil.disk_usage(self.root).free < MIN_STORE_FREE_BYTES + byte_count:
            raise EvidenceCaptureError(
                "private store lacks free-space reserve for GitHub transfer"
            )
        self.transferred_bytes += byte_count

    def begin_github_api_request(self) -> float:
        remaining = MAX_GITHUB_CAPTURE_SECONDS - (
            time.monotonic() - self.github_capture_started
        )
        if remaining <= 0:
            raise EvidenceCaptureError("GitHub capture exceeds the wall-clock boundary")
        if self.github_api_invocations >= MAX_GITHUB_API_INVOCATIONS:
            raise EvidenceCaptureError("GitHub capture exceeds the API invocation boundary")
        self.github_api_invocations += 1
        return remaining

    def note_github_metadata(self, byte_count: int) -> None:
        if (
            not isinstance(byte_count, int)
            or isinstance(byte_count, bool)
            or byte_count < 0
        ):
            raise EvidenceCaptureError("GitHub metadata byte count is invalid")
        boundary = min(self.max_capture_bytes, MAX_GITHUB_METADATA_TRANSFER_BYTES)
        if self.github_metadata_bytes + byte_count > boundary:
            self.github_metadata_bytes = boundary
            raise EvidenceCaptureError("GitHub metadata exceeds the invocation byte boundary")
        self.github_metadata_bytes += byte_count

    def _inject_fault(self, point: str) -> None:
        if self.fault_injector is not None:
            self.fault_injector(point)

    def _build_events(
        self,
        cores: Sequence[dict[str, object]],
    ) -> list[dict[str, Any]]:
        previous = self.events[-1]["event_sha256"] if self.events else None
        events: list[dict[str, Any]] = []
        for offset, core in enumerate(cores):
            value = {
                "schema": EVENT_SCHEMA,
                "sequence": len(self.events) + offset,
                **core,
                "boundaries": BOUNDARIES,
                "previous_event_sha256": previous,
            }
            digest = hashlib.sha256(
                JOURNAL_DOMAIN + canonical_json(value)[:-1]
            ).hexdigest()
            event = {**value, "event_sha256": digest}
            events.append(event)
            previous = digest
        return events

    def _build_event(self, core: dict[str, object]) -> dict[str, Any]:
        return self._build_events([core])[0]

    def _prepare_pending_object(
        self,
        staged: StagedObject,
        event: Mapping[str, Any],
        *,
        reserved_finals: dict[str, tuple[int, int]] | None = None,
    ) -> dict[str, object]:
        if (
            staged.path.parent != self.incoming
            or not _INCOMING_TOOL_FILE.fullmatch(staged.path.name)
        ):
            raise EvidenceCaptureError("staged object is outside the recognised incoming topology")
        if not SHA256_PATTERN.fullmatch(staged.sha256):
            raise EvidenceCaptureError("staged object digest is invalid")
        if (
            not isinstance(staged.bytes, int)
            or isinstance(staged.bytes, bool)
            or staged.bytes < 0
            or staged.bytes > MAX_OBJECT_BYTES
        ):
            raise EvidenceCaptureError("staged object byte count is invalid")
        _strip_unindexed_metadata(staged.path)
        staged_metadata = _pending_regular_metadata(
            staged.path,
            "staged content object",
            allowed_links={1},
        )
        _validate_bound_object_file(
            staged.path,
            "staged content object",
            expected_device=staged_metadata.st_dev,
            expected_inode=staged_metadata.st_ino,
            expected_sha256=staged.sha256,
            expected_bytes=staged.bytes,
            allowed_links={1},
        )
        staged_descriptor = os.open(
            staged.path,
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
        )
        try:
            os.fsync(staged_descriptor)
        finally:
            os.close(staged_descriptor)
        _fsync_directory(self.incoming)

        parent = self.root / "objects" / "sha256" / staged.sha256[:2]
        if parent.exists() or parent.is_symlink():
            _require_private_directory(parent, "object shard")
        else:
            _make_directory(parent)
            _fsync_directory(parent.parent)
        destination = parent / staged.sha256
        reserved = reserved_finals if reserved_finals is not None else {}
        final_preexisting = (
            staged.sha256 in reserved
            or destination.exists()
            or destination.is_symlink()
        )
        final_metadata: os.stat_result
        if staged.sha256 in reserved:
            final_device, final_inode = reserved[staged.sha256]
            if destination.exists() or destination.is_symlink():
                _validate_bound_object_file(
                    destination,
                    "reserved content object",
                    expected_device=final_device,
                    expected_inode=final_inode,
                    expected_sha256=staged.sha256,
                    expected_bytes=staged.bytes,
                    allowed_links={1},
                )
        elif final_preexisting:
            final_metadata = _pending_regular_metadata(
                destination,
                "existing content object",
                allowed_links={1},
            )
            _validate_bound_object_file(
                destination,
                "existing content object",
                expected_device=final_metadata.st_dev,
                expected_inode=final_metadata.st_ino,
                expected_sha256=staged.sha256,
                expected_bytes=staged.bytes,
                allowed_links={1},
            )
            final_device = final_metadata.st_dev
            final_inode = final_metadata.st_ino
        else:
            final_device = staged_metadata.st_dev
            final_inode = staged_metadata.st_ino
        reserved[staged.sha256] = (final_device, final_inode)
        object_value = event["objects"]
        if (
            not isinstance(object_value, list)
            or len(object_value) != 1
            or not isinstance(object_value[0], dict)
            or object_value[0].get("sha256") != staged.sha256
            or object_value[0].get("bytes") != staged.bytes
        ):
            raise EvidenceCaptureError("pending event does not match the staged object")
        return {
            "staged_name": staged.path.name,
            "staged_device": staged_metadata.st_dev,
            "staged_inode": staged_metadata.st_ino,
            "final_relative_path": destination.relative_to(self.root).as_posix(),
            "final_preexisting": final_preexisting,
            "final_device": final_device,
            "final_inode": final_inode,
            "sha256": staged.sha256,
            "bytes": staged.bytes,
        }

    def _write_pending_transaction(
        self,
        events: Sequence[Mapping[str, Any]],
        object_bindings: Sequence[Mapping[str, object] | None],
    ) -> None:
        if not events or len(events) != len(object_bindings):
            raise EvidenceCaptureError("pending transaction batch is empty or misaligned")
        pending_path = self.root / PENDING_EVENT_NAME
        if pending_path.exists() or pending_path.is_symlink():
            raise EvidenceCaptureError("private store already contains a pending transaction")
        journal_path = self.root / "journal.jsonl"
        _require_private_regular_file(journal_path, "journal")
        if journal_path.stat().st_size > MAX_STORE_JOURNAL_BYTES:
            raise EvidenceCaptureError("journal exceeds the lifetime byte boundary")
        journal_raw = _read_private_file_bounded(
            journal_path,
            "journal",
            MAX_STORE_JOURNAL_BYTES,
        )
        value = {
            "schema": PENDING_EVENT_SCHEMA,
            "journal_before": {
                "bytes": len(journal_raw),
                "sha256": sha256_bytes(journal_raw),
            },
            "events": [dict(event) for event in events],
            "objects": [
                dict(binding) if binding is not None else None
                for binding in object_bindings
            ],
        }
        raw = canonical_json(value)
        if len(raw) > MAX_METADATA_BYTES:
            raise EvidenceCaptureError("pending event transaction exceeds the byte boundary")
        event_bytes = sum(len(canonical_json(event)) for event in events)
        if len(self.events) + len(events) > MAX_STORE_EVENTS:
            raise EvidenceCaptureError("journal exceeds the lifetime event boundary")
        if len(journal_raw) + event_bytes > MAX_STORE_JOURNAL_BYTES:
            raise EvidenceCaptureError("journal exceeds the lifetime byte boundary")
        if shutil.disk_usage(self.root).free < MIN_STORE_FREE_BYTES + len(raw):
            raise EvidenceCaptureError(
                "private store lacks free-space reserve for the pending transaction"
            )
        temporary = self.incoming / uuid.uuid4().hex
        try:
            _exclusive_file(temporary, raw)
            _fsync_directory(self.incoming)
            os.replace(temporary, pending_path)
            _fsync_directory(self.incoming)
            _fsync_directory(self.root)
        finally:
            temporary.unlink(missing_ok=True)
        self._inject_fault("after-pending-event")

    def _read_pending_transaction(self) -> dict[str, Any] | None:
        path = self.root / PENDING_EVENT_NAME
        if not path.exists() and not path.is_symlink():
            return None
        raw = _read_private_file_bounded(
            path,
            "pending event transaction",
            MAX_METADATA_BYTES,
        )
        value = parse_json(raw, "pending event transaction")
        if not isinstance(value, dict) or set(value) != {
            "schema",
            "journal_before",
            "events",
            "objects",
        }:
            raise EvidenceCaptureError("pending event transaction has unknown or missing fields")
        if value["schema"] != PENDING_EVENT_SCHEMA or raw != canonical_json(value):
            raise EvidenceCaptureError("pending event transaction is not canonical")
        journal_before = value["journal_before"]
        if not isinstance(journal_before, dict) or set(journal_before) != {"bytes", "sha256"}:
            raise EvidenceCaptureError("pending event journal binding is invalid")
        before_bytes = journal_before["bytes"]
        if (
            not isinstance(before_bytes, int)
            or isinstance(before_bytes, bool)
            or before_bytes < 0
            or before_bytes > MAX_STORE_JOURNAL_BYTES
            or not isinstance(journal_before["sha256"], str)
            or not SHA256_PATTERN.fullmatch(journal_before["sha256"])
        ):
            raise EvidenceCaptureError("pending event journal binding is invalid")
        events = value["events"]
        object_bindings = value["objects"]
        if (
            not isinstance(events, list)
            or not events
            or not isinstance(object_bindings, list)
            or len(events) != len(object_bindings)
        ):
            raise EvidenceCaptureError("pending transaction batch is empty or misaligned")
        staged_names: set[str] = set()
        for event, object_binding in zip(events, object_bindings, strict=True):
            if not isinstance(event, dict):
                raise EvidenceCaptureError("pending event is not an object")
            _strict_event_keys(event)
            if event["schema"] != EVENT_SCHEMA or event["boundaries"] != BOUNDARIES:
                raise EvidenceCaptureError("pending event schema or boundary is invalid")
            if (
                not isinstance(event["sequence"], int)
                or isinstance(event["sequence"], bool)
                or event["sequence"] < 0
                or not isinstance(event["source"], dict)
                or not isinstance(event["source"].get("identity"), str)
                or not event["source"]["identity"]
                or not isinstance(event["disposition"], dict)
            ):
                raise EvidenceCaptureError("pending event sequence or identity is invalid")
            core = dict(event)
            supplied = core.pop("event_sha256")
            expected = hashlib.sha256(
                JOURNAL_DOMAIN + canonical_json(core)[:-1]
            ).hexdigest()
            if supplied != expected:
                raise EvidenceCaptureError("pending event digest does not match")

            event_objects = event["objects"]
            if object_binding is None:
                if event_objects != [] or event["disposition"].get("status") not in {
                    "excluded",
                    "unavailable",
                }:
                    raise EvidenceCaptureError("object-free pending event is inconsistent")
                continue
            expected_keys = {
                "staged_name",
                "staged_device",
                "staged_inode",
                "final_relative_path",
                "final_preexisting",
                "final_device",
                "final_inode",
                "sha256",
                "bytes",
            }
            if not isinstance(object_binding, dict) or set(object_binding) != expected_keys:
                raise EvidenceCaptureError(
                    "pending object binding has unknown or missing fields"
                )
            integer_keys = (
                "staged_device",
                "staged_inode",
                "final_device",
                "final_inode",
                "bytes",
            )
            if any(
                not isinstance(object_binding[key], int)
                or isinstance(object_binding[key], bool)
                or object_binding[key] < 0
                for key in integer_keys
            ):
                raise EvidenceCaptureError("pending object integer binding is invalid")
            digest = object_binding["sha256"]
            staged_name = object_binding["staged_name"]
            expected_relative = f"objects/sha256/{str(digest)[:2]}/{digest}"
            if (
                not isinstance(digest, str)
                or not SHA256_PATTERN.fullmatch(digest)
                or not isinstance(staged_name, str)
                or not _INCOMING_TOOL_FILE.fullmatch(staged_name)
                or object_binding["final_relative_path"] != expected_relative
                or not isinstance(object_binding["final_preexisting"], bool)
                or object_binding["bytes"] > MAX_OBJECT_BYTES
                or not isinstance(event_objects, list)
                or len(event_objects) != 1
                or not isinstance(event_objects[0], dict)
                or event_objects[0].get("sha256") != digest
                or event_objects[0].get("bytes") != object_binding["bytes"]
                or event["disposition"].get("status") != "captured"
            ):
                raise EvidenceCaptureError("pending object binding is inconsistent")
            if not object_binding["final_preexisting"] and (
                object_binding["final_device"] != object_binding["staged_device"]
                or object_binding["final_inode"] != object_binding["staged_inode"]
            ):
                raise EvidenceCaptureError("new pending object inode binding is inconsistent")
            if staged_name in staged_names:
                raise EvidenceCaptureError("pending transaction repeats a staged object path")
            staged_names.add(staged_name)
        return value

    def _pending_journal_state(
        self,
        pending: Mapping[str, Any],
    ) -> tuple[int, bool, list[bytes]]:
        journal_path = self.root / "journal.jsonl"
        _require_private_regular_file(journal_path, "journal")
        if journal_path.stat().st_size > MAX_STORE_JOURNAL_BYTES:
            raise EvidenceCaptureError("journal exceeds the lifetime byte boundary")
        journal_raw = _read_private_file_bounded(
            journal_path,
            "journal",
            MAX_STORE_JOURNAL_BYTES,
        )
        before = pending["journal_before"]
        offset = before["bytes"]
        if len(journal_raw) < offset:
            raise EvidenceCaptureError("journal is shorter than the pending transaction prefix")
        prefix = journal_raw[:offset]
        suffix = journal_raw[offset:]
        if sha256_bytes(prefix) != before["sha256"]:
            raise EvidenceCaptureError("journal does not match the pending transaction prefix")
        prefix_events = _validated_journal_prefix(prefix)
        if len(prefix_events) + len(pending["events"]) > MAX_STORE_EVENTS:
            raise EvidenceCaptureError("journal exceeds the lifetime event boundary")
        previous = prefix_events[-1]["event_sha256"] if prefix_events else None
        identities: set[str] = set()
        for existing in prefix_events:
            identity = existing["source"]["identity"]
            if identity in identities:
                raise EvidenceCaptureError("journal contains a duplicate immutable source identity")
            identities.add(identity)
        event_raws: list[bytes] = []
        for index, event in enumerate(pending["events"]):
            if (
                event["sequence"] != len(prefix_events) + index
                or event["previous_event_sha256"] != previous
            ):
                raise EvidenceCaptureError("pending event does not extend the journal prefix")
            identity = event["source"]["identity"]
            if identity in identities:
                raise EvidenceCaptureError("pending event duplicates an immutable source identity")
            identities.add(identity)
            previous = event["event_sha256"]
            event_raws.append(canonical_json(event))

        completed = 0
        remainder = suffix
        while completed < len(event_raws) and len(remainder) >= len(event_raws[completed]):
            expected = event_raws[completed]
            if remainder[: len(expected)] != expected:
                raise EvidenceCaptureError("journal has an unprovable pending event suffix")
            remainder = remainder[len(expected) :]
            completed += 1
        if completed == len(event_raws):
            if remainder:
                raise EvidenceCaptureError("journal extends beyond the pending transaction")
            return completed, False, event_raws
        if not event_raws[completed].startswith(remainder):
            raise EvidenceCaptureError("journal has an unprovable partial pending event")
        return completed, bool(remainder), event_raws

    def _complete_pending_object(
        self,
        binding: Mapping[str, Any],
        *,
        journal_state: str,
    ) -> None:
        staged = self.incoming / binding["staged_name"]
        final = self.root / binding["final_relative_path"]
        parent = final.parent
        _require_private_directory(parent, "object shard")
        staged_exists = staged.exists() or staged.is_symlink()
        final_exists = final.exists() or final.is_symlink()
        digest = binding["sha256"]
        byte_count = binding["bytes"]

        if binding["final_preexisting"]:
            if not final_exists:
                raise EvidenceCaptureError("pre-existing pending content object is missing")
            _validate_bound_object_file(
                final,
                "pending final content object",
                expected_device=binding["final_device"],
                expected_inode=binding["final_inode"],
                expected_sha256=digest,
                expected_bytes=byte_count,
                allowed_links={1},
            )
            if staged_exists:
                if journal_state != "absent":
                    raise EvidenceCaptureError(
                        "pending journal advanced before staged object removal"
                    )
                _validate_bound_object_file(
                    staged,
                    "pending staged content object",
                    expected_device=binding["staged_device"],
                    expected_inode=binding["staged_inode"],
                    expected_sha256=digest,
                    expected_bytes=byte_count,
                    allowed_links={1},
                )
                staged.unlink()
                _fsync_directory(self.incoming)
                self._inject_fault("after-staged-unlink")
            return

        if staged_exists and final_exists:
            if journal_state != "absent":
                raise EvidenceCaptureError("pending journal advanced before staged object removal")
            staged_metadata = _validate_bound_object_file(
                staged,
                "pending staged content object",
                expected_device=binding["staged_device"],
                expected_inode=binding["staged_inode"],
                expected_sha256=digest,
                expected_bytes=byte_count,
                allowed_links={2},
            )
            final_metadata = _validate_bound_object_file(
                final,
                "pending final content object",
                expected_device=binding["final_device"],
                expected_inode=binding["final_inode"],
                expected_sha256=digest,
                expected_bytes=byte_count,
                allowed_links={2},
            )
            if (
                staged_metadata.st_dev != final_metadata.st_dev
                or staged_metadata.st_ino != final_metadata.st_ino
            ):
                raise EvidenceCaptureError("pending hard links do not share the bound inode")
            staged.unlink()
            _fsync_directory(self.incoming)
            self._inject_fault("after-staged-unlink")
        elif staged_exists:
            if journal_state != "absent":
                raise EvidenceCaptureError("pending journal advanced before object installation")
            _validate_bound_object_file(
                staged,
                "pending staged content object",
                expected_device=binding["staged_device"],
                expected_inode=binding["staged_inode"],
                expected_sha256=digest,
                expected_bytes=byte_count,
                allowed_links={1},
            )
            os.link(staged, final, follow_symlinks=False)
            _fsync_directory(parent)
            self._inject_fault("after-object-link")
            staged.unlink()
            _fsync_directory(self.incoming)
            self._inject_fault("after-staged-unlink")
        elif not final_exists:
            raise EvidenceCaptureError("pending content object has neither staged nor final bytes")

        _validate_bound_object_file(
            final,
            "pending final content object",
            expected_device=binding["final_device"],
            expected_inode=binding["final_inode"],
            expected_sha256=digest,
            expected_bytes=byte_count,
            allowed_links={1},
        )

    def _write_pending_events(
        self,
        completed: int,
        has_partial: bool,
        event_raws: Sequence[bytes],
        offset: int,
    ) -> None:
        if completed == len(event_raws):
            descriptor = os.open(self.root / "journal.jsonl", os.O_WRONLY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            return
        remaining_bytes = sum(len(raw) for raw in event_raws[completed:])
        if shutil.disk_usage(self.root).free < MIN_STORE_FREE_BYTES + remaining_bytes:
            raise EvidenceCaptureError(
                "private store lacks free-space reserve for the journal append"
            )
        journal_path = self.root / "journal.jsonl"
        descriptor = os.open(journal_path, os.O_WRONLY)
        try:
            replay_offset = offset + sum(len(raw) for raw in event_raws[:completed])
            if has_partial:
                os.ftruncate(descriptor, replay_offset)
                os.fsync(descriptor)
            os.lseek(descriptor, replay_offset, os.SEEK_SET)
            first = event_raws[completed]
            split = max(1, len(first) // 2)
            for index, part in enumerate((first[:split], first[split:])):
                view = memoryview(part)
                while view:
                    written = os.write(descriptor, view)
                    if written <= 0:
                        raise EvidenceCaptureError("journal write made no progress")
                    view = view[written:]
                if index == 0:
                    os.fsync(descriptor)
                    self._inject_fault("after-journal-prefix")
            for event_raw in event_raws[completed + 1 :]:
                view = memoryview(event_raw)
                while view:
                    written = os.write(descriptor, view)
                    if written <= 0:
                        raise EvidenceCaptureError("journal write made no progress")
                    view = view[written:]
            os.fsync(descriptor)
            self._inject_fault("after-journal-append")
        finally:
            os.close(descriptor)

    def _complete_pending_transaction(self, pending: Mapping[str, Any]) -> None:
        completed, has_partial, event_raws = self._pending_journal_state(pending)
        journal_state = "advanced" if completed or has_partial else "absent"
        for object_binding in pending["objects"]:
            if object_binding is not None:
                self._complete_pending_object(
                    object_binding,
                    journal_state=journal_state,
                )
        self._write_pending_events(
            completed,
            has_partial,
            event_raws,
            pending["journal_before"]["bytes"],
        )
        marker = self.root / PENDING_EVENT_NAME
        if _read_private_file_bounded(
            marker,
            "pending event transaction",
            MAX_METADATA_BYTES,
        ) != canonical_json(pending):
            raise EvidenceCaptureError("pending event transaction changed during recovery")
        marker.unlink()
        _fsync_directory(self.root)

    def _commit_pending_events(
        self,
        events: Sequence[dict[str, Any]],
        object_bindings: Sequence[Mapping[str, object] | None],
    ) -> list[dict[str, Any]]:
        event_raws = [canonical_json(event) for event in events]
        event_bytes = sum(len(raw) for raw in event_raws)
        if self.capture_events + len(events) > MAX_CAPTURE_EVENTS:
            raise EvidenceCaptureError("capture exceeds the per-invocation event boundary")
        metadata_boundary = min(self.max_capture_bytes, MAX_CAPTURE_METADATA_BYTES)
        if self.capture_metadata_bytes + event_bytes > metadata_boundary:
            raise EvidenceCaptureError(
                "capture exceeds the per-invocation metadata byte boundary"
            )
        if (
            self.captured_bytes
            + self.capture_metadata_bytes
            + event_bytes
            > self.max_capture_bytes
        ):
            raise EvidenceCaptureError("capture exceeds the per-invocation byte boundary")
        self._write_pending_transaction(events, object_bindings)
        pending = self._read_pending_transaction()
        if pending is None:
            raise EvidenceCaptureError("pending event transaction was not installed")
        self._complete_pending_transaction(pending)
        self.events.extend(events)
        self.capture_events += len(events)
        self.capture_metadata_bytes += event_bytes
        for event in events:
            self.identities[event["source"]["identity"]] = event
        self._refresh_ledger()
        return list(events)

    def _append_event(self, core: dict[str, object]) -> dict[str, Any]:
        event = self._build_event(core)
        self._commit_pending_events([event], [None])
        return event

    def _refresh_ledger(self) -> None:
        journal_path = self.root / "journal.jsonl"
        if journal_path.stat().st_size > MAX_STORE_JOURNAL_BYTES:
            raise EvidenceCaptureError("journal exceeds the lifetime byte boundary")
        journal_raw = _read_private_file_bounded(
            journal_path,
            "journal",
            MAX_STORE_JOURNAL_BYTES,
        )
        ledger = build_expiry_ledger(self.events, journal_raw)
        expected = canonical_json(ledger, pretty=True)
        if len(expected) > MAX_STORE_LEDGER_BYTES:
            raise EvidenceCaptureError("expiry ledger exceeds the lifetime byte boundary")
        path = self.root / "expiry-ledger.json"
        if _read_private_file_bounded(
            path,
            "expiry ledger",
            MAX_STORE_LEDGER_BYTES,
        ) != expected:
            if shutil.disk_usage(self.root).free < MIN_STORE_FREE_BYTES + len(expected):
                raise EvidenceCaptureError(
                    "private store lacks free-space reserve for the expiry ledger"
                )
            atomic_replace(path, expected)

    def commit_staged(
        self,
        staged: StagedObject,
        *,
        trigger: str,
        repository: str | None,
        source: dict[str, object],
        role: str,
        media_type: str,
        opaque: bool,
        secret_scan: str,
        secret_scan_performed: bool,
        sensitivity: str,
        captured_at: datetime | None = None,
    ) -> bool:
        item = StagedCapture(
            staged=staged,
            trigger=trigger,
            repository=repository,
            source=source,
            role=role,
            media_type=media_type,
            opaque=opaque,
            secret_scan=secret_scan,
            secret_scan_performed=secret_scan_performed,
            sensitivity=sensitivity,
            captured_at=captured_at,
        )
        return self.commit_staged_batch([item]) == 1

    def _staged_capture_core(self, item: StagedCapture) -> dict[str, object]:
        object_value = {
            "role": item.role,
            "sha256": item.staged.sha256,
            "bytes": item.staged.bytes,
            "media_type": item.media_type,
            "opaque": item.opaque,
            "secret_scan": item.secret_scan,
            "secret_scan_performed": item.secret_scan_performed,
            "sensitivity": item.sensitivity,
            "public_projection_eligible": False,
        }
        moment = item.captured_at or utc_now()
        return {
            "captured_at_utc": format_time(moment),
            "captured_at_europe_london": format_london_time(moment),
            "time_source": "local-system-clock-unattested",
            "trigger": item.trigger,
            "repository": item.repository,
            "source": item.source,
            "objects": [object_value],
            "disposition": {"status": "captured", "reason": None},
        }

    @staticmethod
    def _discard_staged_captures(
        items: Sequence[StagedCapture | ObjectlessCapture],
    ) -> None:
        for item in items:
            if isinstance(item, StagedCapture):
                item.staged.path.unlink(missing_ok=True)

    def commit_staged_batch(self, captures: Sequence[StagedCapture]) -> int:
        """Commit an ordered group of staged objects and events as one WAL unit."""

        return self.commit_capture_batch(captures)

    def commit_capture_batch(
        self,
        captures: Sequence[StagedCapture | ObjectlessCapture],
    ) -> int:
        """Commit captured and object-free events as one ordered WAL unit."""

        items = list(captures)
        if not items:
            raise EvidenceCaptureError("capture batch must not be empty")
        staged_items = [item for item in items if isinstance(item, StagedCapture)]
        if len({item.staged.path for item in staged_items}) != len(staged_items):
            self._discard_staged_captures(items)
            raise EvidenceCaptureError("staged capture batch contains a repeated incoming path")
        raw_identities = [item.source.get("identity") for item in items]
        if any(not isinstance(identity, str) or not identity for identity in raw_identities):
            self._discard_staged_captures(items)
            raise EvidenceCaptureError("staged capture batch has an invalid source identity")
        identities = [str(identity) for identity in raw_identities]
        if len(set(identities)) != len(identities):
            self._discard_staged_captures(items)
            raise EvidenceCaptureError("staged capture batch contains a duplicate source identity")
        cores: list[dict[str, object]] = []
        for item in items:
            if isinstance(item, StagedCapture):
                cores.append(self._staged_capture_core(item))
                continue
            if item.status_value not in {"excluded", "unavailable"}:
                self._discard_staged_captures(items)
                raise EvidenceCaptureError("invalid object-free disposition")
            if not item.reason:
                self._discard_staged_captures(items)
                raise EvidenceCaptureError("object-free disposition requires a reason")
            moment = item.captured_at or utc_now()
            cores.append(
                {
                    "captured_at_utc": format_time(moment),
                    "captured_at_europe_london": format_london_time(moment),
                    "time_source": "local-system-clock-unattested",
                    "trigger": item.trigger,
                    "repository": item.repository,
                    "source": item.source,
                    "objects": [],
                    "disposition": {
                        "status": item.status_value,
                        "reason": item.reason,
                    },
                }
            )
        existing_matches = 0
        for item, core in zip(items, cores, strict=True):
            existing = self.identities.get(str(item.source["identity"]))
            if existing is None:
                continue
            candidate = {
                "source": item.source,
                "objects": core["objects"],
                "disposition": core["disposition"],
                "repository": item.repository,
            }
            if _event_fingerprint(existing) != _event_fingerprint(candidate):
                self._discard_staged_captures(items)
                raise EvidenceCaptureError(
                    "immutable source identity has conflicting evidence"
                )
            existing_matches += 1
        if existing_matches:
            self._discard_staged_captures(items)
            if existing_matches != len(items):
                raise EvidenceCaptureError(
                    "staged capture batch mixes existing and new source identities"
                )
            self.no_op += len(items)
            return 0
        if any(
            not isinstance(item.staged.bytes, int)
            or isinstance(item.staged.bytes, bool)
            or item.staged.bytes < 0
            for item in staged_items
        ):
            self._discard_staged_captures(items)
            raise EvidenceCaptureError("staged capture batch has an invalid byte count")
        byte_count = sum(item.staged.bytes for item in staged_items)
        if (
            self.captured_bytes
            + self.capture_metadata_bytes
            + byte_count
            > self.max_capture_bytes
        ):
            self._discard_staged_captures(items)
            raise EvidenceCaptureError("capture exceeds the per-invocation byte boundary")
        if shutil.disk_usage(self.root).free < MIN_STORE_FREE_BYTES:
            self._discard_staged_captures(items)
            raise EvidenceCaptureError(
                "private store has less than the required free-space reserve"
            )
        events = self._build_events(cores)
        event_bytes = sum(len(canonical_json(event)) for event in events)
        if (
            self.captured_bytes
            + self.capture_metadata_bytes
            + byte_count
            + event_bytes
            > self.max_capture_bytes
        ):
            self._discard_staged_captures(items)
            raise EvidenceCaptureError("capture exceeds the per-invocation byte boundary")
        reserved_finals: dict[str, tuple[int, int]] = {}
        try:
            object_bindings = [
                (
                    self._prepare_pending_object(
                        item.staged,
                        event,
                        reserved_finals=reserved_finals,
                    )
                    if isinstance(item, StagedCapture)
                    else None
                )
                for item, event in zip(items, events, strict=True)
            ]
        except Exception:
            self._discard_staged_captures(items)
            raise
        self._commit_pending_events(events, object_bindings)
        self.captured += len(staged_items)
        self.excluded += sum(
            isinstance(item, ObjectlessCapture) and item.status_value == "excluded"
            for item in items
        )
        self.unavailable += sum(
            isinstance(item, ObjectlessCapture) and item.status_value == "unavailable"
            for item in items
        )
        self.captured_bytes += byte_count
        return len(items)

    def record_without_object(
        self,
        *,
        trigger: str,
        repository: str | None,
        source: dict[str, object],
        status_value: str,
        reason: str,
        captured_at: datetime | None = None,
    ) -> bool:
        item = ObjectlessCapture(
            trigger=trigger,
            repository=repository,
            source=source,
            status_value=status_value,
            reason=reason,
            captured_at=captured_at,
        )
        return self.commit_capture_batch([item]) == 1

    def summary(self) -> dict[str, object]:
        ledger = parse_json(
            _read_private_file_bounded(
                self.root / "expiry-ledger.json",
                "expiry ledger",
                MAX_STORE_LEDGER_BYTES,
            ),
            "expiry ledger",
        )
        now = utc_now()
        warnings = sum(
            1
            for item in ledger["entries"]
            if parse_time(item["warning_at_utc"], "warning") <= now
        )
        return {
            "captured": self.captured,
            "captured_bytes": self.captured_bytes,
            "transferred_bytes": self.transferred_bytes,
            "github_api_invocations": self.github_api_invocations,
            "github_metadata_bytes": self.github_metadata_bytes,
            "capture_events": self.capture_events,
            "capture_metadata_bytes": self.capture_metadata_bytes,
            "no_op": self.no_op,
            "excluded": self.excluded,
            "unavailable": self.unavailable,
            "expiry_warnings": warnings,
            "journal_events": len(self.events),
            "journal_head_sha256": self.events[-1]["event_sha256"] if self.events else None,
            "boundaries": BOUNDARIES,
        }


def _local_identity(
    path: Path,
    metadata: Mapping[str, int],
    kind: str,
    content_sha256: str,
) -> str:
    path_digest = sha256_bytes(os.fsencode(str(path.resolve(strict=True))))
    return (
        f"{kind}:path-sha256:{path_digest}:device:{metadata['device']}:inode:{metadata['inode']}:"
        f"mtime-ns:{metadata['mtime_ns']}:ctime-ns:{metadata['ctime_ns']}:"
        f"bytes:{metadata['bytes']}:content-sha256:{content_sha256}"
    )


def capture_local_file(
    store: EvidenceStore,
    path: Path,
    *,
    trigger: str,
    repository: str | None,
    redacted_jsonl: bool = False,
    apfs_clone: bool = False,
) -> bool:
    metadata = path.lstat()
    _validate_local_source_metadata(path, metadata)
    store.require_staging_capacity(metadata.st_size)
    resolved = path.resolve(strict=True)
    if resolved == store.root.resolve() or store.root.resolve() in resolved.parents:
        raise EvidenceCaptureError("source and private store paths overlap")
    kind = (
        "local-apfs-clone"
        if apfs_clone
        else "local-redacted-jsonl"
        if redacted_jsonl
        else "local-file"
    )
    clone_snapshot = stage_apfs_clone(path, store.incoming) if apfs_clone else None
    staged = (
        clone_snapshot.staged
        if clone_snapshot is not None
        else stage_regular_file(path, store.incoming)
    )
    before_stat = (
        clone_snapshot.source_stat_before
        if clone_snapshot is not None
        else staged.source_stat_before
    )
    after_stat = (
        clone_snapshot.source_stat_after
        if clone_snapshot is not None
        else staged.source_stat_after
    )
    if before_stat is None or after_stat is None:
        staged.path.unlink(missing_ok=True)
        raise EvidenceCaptureError("local capture did not bind source stat evidence")
    identity = _local_identity(path, before_stat, kind, staged.sha256)
    source = _source_value(
        kind=kind,
        identity=identity,
        label=path.name,
        occurred_at_utc=None,
        expires_at_utc=None,
        expiry_basis="unknown",
        commit_sha=None,
        tree_sha=None,
        redaction_mode=(
            "operator-supplied-redacted-jsonl-not-attested" if redacted_jsonl else "none"
        ),
        snapshot_method="apfs-clonefile" if apfs_clone else "stable-byte-copy",
        source_stat_before=before_stat,
        source_stat_after=after_stat,
        source_changed_after_snapshot=(
            clone_snapshot.source_changed_after_snapshot if clone_snapshot is not None else False
        ),
        collection_generation_sha256=None,
        collection_window=None,
        redaction_categories=[],
        redaction_count=0,
    )
    media_type = "application/x-ndjson" if redacted_jsonl else detect_media_type(path)
    with staged.path.open("rb") as staged_stream:
        staged_header = staged_stream.read(16)
    if staged_header.startswith(b"\xff\xd8\xff"):
        media_type = "image/jpeg"
    archive_format = _archive_format_from_magic(staged.path)
    if archive_format is None and zipfile.is_zipfile(staged.path):
        archive_format = "zip"
    if archive_format is None:
        archive_format = _embedded_archive_format(staged.path)
    if archive_format == "zip":
        media_type = "application/zip"
    opaque = media_type in {"application/zip", "application/octet-stream"}
    secret_scan = "opaque-binary-not-inspected"
    try:
        if redacted_jsonl:
            _validate_redacted_jsonl(staged.path)
            secret_scan = "operator-redacted-jsonl-high-confidence-scan-passed"
            opaque = False
        elif archive_format == "zip" or media_type == "application/zip":
            _scan_zip_archive(staged.path)
            secret_scan = "zip-entry-high-confidence-scan-passed"
            opaque = True
        elif (
            archive_format is not None
            or path.suffix.lower() in UNINSPECTABLE_ARCHIVE_SUFFIXES
            or path.suffix.lower() in PRIVATE_KEY_CONTAINER_SUFFIXES
        ):
            staged.path.unlink(missing_ok=True)
            return store.record_without_object(
                trigger=trigger,
                repository=repository,
                source=source,
                status_value="unavailable",
                reason="unsupported-compressed-or-archive-format",
            )
        elif not apfs_clone and path.suffix.lower() in TEXT_SUFFIXES:
            _scan_secret_text(staged.path)
            secret_scan = "high-confidence-text-scan-passed"
            opaque = False
        elif media_type in {"image/png", "image/jpeg"}:
            if media_type == "image/png":
                _validate_png(staged.path)
            else:
                _validate_jpeg(staged.path)
            with staged.path.open("rb") as stream:
                _scan_secret_binary_stream(stream)
            secret_scan = (
                "validated-png-high-confidence-byte-scan-passed"
                if media_type == "image/png"
                else "validated-jpeg-high-confidence-metadata-scan-passed"
            )
            opaque = True
        else:
            with staged.path.open("rb") as stream:
                _scan_secret_binary_stream(stream)
            staged.path.unlink(missing_ok=True)
            return store.record_without_object(
                trigger=trigger,
                repository=repository,
                source=source,
                status_value="unavailable",
                reason="unsupported-opaque-binary-format",
            )
    except SecretDetectedError as error:
        staged.path.unlink(missing_ok=True)
        return store.record_without_object(
            trigger=trigger,
            repository=repository,
            source=source,
            status_value="excluded",
            reason=f"secret-category:{error.category}",
        )
    except EvidenceCaptureError:
        staged.path.unlink(missing_ok=True)
        raise
    return store.commit_staged(
        staged,
        trigger=trigger,
        repository=repository,
        source=source,
        role="redacted-jsonl" if redacted_jsonl else "local-source",
        media_type=media_type,
        opaque=opaque,
        secret_scan=secret_scan,
        secret_scan_performed=secret_scan != "opaque-binary-not-inspected",
        sensitivity="owner-only-redacted" if redacted_jsonl else "owner-only-raw",
    )


def _paths_have_ancestry_overlap(left: Path, right: Path) -> bool:
    left_value = left.resolve(strict=True)
    right_value = right.resolve(strict=True)
    return (
        left_value == right_value
        or left_value in right_value.parents
        or right_value in left_value.parents
    )


def iter_local_directory(directory: Path, *, store_root: Path | None = None) -> Iterator[Path]:
    metadata = directory.lstat()
    if directory.is_symlink() or not stat.S_ISDIR(metadata.st_mode):
        raise EvidenceCaptureError("local directory source must be a real directory")
    if store_root is not None and _paths_have_ancestry_overlap(directory, store_root):
        raise EvidenceCaptureError("source directory and private store paths overlap")
    for root, directory_names, file_names in os.walk(directory, followlinks=False):
        root_path = Path(root)
        for name in sorted(directory_names):
            candidate = root_path / name
            item = candidate.lstat()
            if candidate.is_symlink() or not stat.S_ISDIR(item.st_mode):
                raise EvidenceCaptureError("local directory contains a linked or special directory")
        for name in sorted(file_names):
            candidate = root_path / name
            item = candidate.lstat()
            if candidate.is_symlink() or not stat.S_ISREG(item.st_mode) or item.st_nlink != 1:
                raise EvidenceCaptureError("local directory contains a linked or special file")
            yield candidate


@dataclass(frozen=True)
class CodexSessionRecord:
    path: Path
    thread_id: str
    session_id: str
    parent_thread_id: str | None
    timestamp: str
    metadata: os.stat_result


@dataclass(frozen=True)
class CodexProjection:
    record: CodexSessionRecord
    staged: StagedObject | None
    identity: str
    source: dict[str, object]
    disposition: str
    reason: str | None
    raw_source_sha256: str
    uncompressed_sha256: str | None
    uncompressed_bytes: int | None
    skipped_record_types: dict[str, int]
    retained_records: int
    object_sha256: str | None
    object_bytes: int | None
    reused: bool


_CODEX_HIDDEN_KEYS = {
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
_CODEX_OMITTED_KEY_NORMALISATIONS = {
    "absolutepath",
    "attachment",
    "attachmentid",
    "attachments",
    "clientid",
    "clientidentifier",
    "filepath",
    "localpath",
    "meta",
    "path",
    "sourcepath",
}
_CODEX_SENSITIVE_KEY_NORMALISATIONS = {
    "accesstoken",
    "apikey",
    "authorization",
    "bearer",
    "clientsecret",
    "cookie",
    "credential",
    "idtoken",
    "jwt",
    "passphrase",
    "password",
    "privatekey",
    "refreshtoken",
    "secret",
    "session",
    "token",
}
_CODEX_URL_PATTERN = re.compile(r"(?i)\bhttps?://[^\s<>{}\[\]\"']+")
_CODEX_ALLOWED_EVENT_TYPES = {
    "agent_message",
    "item_completed",
    "mcp_tool_call_end",
    "patch_apply_end",
    "sub_agent_activity",
    "task_complete",
    "task_started",
    "token_count",
    "turn_aborted",
    "user_message",
    "web_search_end",
}
_CODEX_EXCLUDED_EVENT_TYPES = {
    "agent_reasoning",
    "context_compacted",
    "thread_settings",
    "thread_settings_applied",
}
_CODEX_USAGE_FIELDS = {
    "cached_input_tokens",
    "input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
}
_CODEX_RATE_LIMIT_CONTAINER_FIELDS = {"credits", "primary", "secondary"}
_CODEX_RATE_LIMIT_VALUE_FIELDS = {
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
_CODEX_IMAGE_KEY_NORMALISATIONS = {"image", "images", "imageurl", "inputimage"}
_CODEX_RESPONSE_CALL_TYPES = {"custom_tool_call", "function_call"}
_CODEX_RESPONSE_OUTPUT_TYPES = {"custom_tool_call_output", "function_call_output"}


def _normalise_codex_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


_CODEX_HIDDEN_KEY_NORMALISATIONS = {
    _normalise_codex_key(key) for key in _CODEX_HIDDEN_KEYS
}
_CODEX_JSON_KEY_FRAGMENT_LIMIT = 512
_CODEX_ASSIGNMENT_KEY_FRAGMENT_LIMIT = 128
_CODEX_JSON_KEY_FRAGMENT_PATTERN = re.compile(
    rf'("(?:\\(?:["\\/bfnrt]|u[0-9A-Fa-f]{{4}})|[^"\\])'
    rf'{{1,{_CODEX_JSON_KEY_FRAGMENT_LIMIT}}}")\s*:'
)
_CODEX_ASSIGNMENT_KEY_FRAGMENT_PATTERN = re.compile(
    rf"(?i)(?<![A-Za-z0-9])([A-Za-z][A-Za-z0-9_.-]"
    rf"{{0,{_CODEX_ASSIGNMENT_KEY_FRAGMENT_LIMIT - 1}}})\s*[:=]\s*"
)


def _strip_codex_leading_ignorables(value: str) -> str:
    index = 0
    while index < len(value):
        character = value[index]
        if not character.isspace() and unicodedata.category(character) != "Cf":
            break
        index += 1
    return value[index:]


def _codex_assignment_delimiter_is_padding(
    value: str, start: int, end: int, delimiter: int
) -> bool:
    """Distinguish terminal padding syntax with no value from an assignment."""

    if end != delimiter or value[delimiter] != "=":
        return False
    padding_end = delimiter
    while padding_end < len(value) and value[padding_end] == "=":
        padding_end += 1
        if padding_end - delimiter > 2:
            return False
    whole_text = start == 0 and padding_end == len(value)
    quoted_token = (
        start > 0
        and padding_end < len(value)
        and value[start - 1] == '"'
        and value[padding_end] == '"'
        and (start < 2 or value[start - 2] != "\\")
    )
    if not whole_text and not quoted_token:
        return False
    if quoted_token:
        following = padding_end + 1
        while following < len(value) and value[following].isspace():
            following += 1
        if following < len(value) and value[following] in ":=":
            return False
    size = padding_end - start
    if size > MAX_CODEX_TEXT_BYTES:
        return False
    token = value[start:padding_end]
    # This identifies a delimiter, not an encoding or safe content. Masking may
    # have changed the token's length or padding bits; neither establishes an RHS.
    return re.fullmatch(r"[A-Za-z0-9_-]+={1,2}", token) is not None


def _classify_codex_oversized_text_key_fragments(value: str) -> tuple[bool, bool]:
    """Fail closed on structural keys beyond the bounded regex classifiers."""

    if ":" not in value and "=" not in value:
        return False, False
    hidden = False
    sensitive = False

    # Adjacent unescaped quotes form every possible free-form key candidate,
    # including a valid key after an unmatched quote. Their interiors are
    # disjoint, so validating all candidates remains linear in the input size.
    previous_quote: int | None = None
    consecutive_backslashes = 0
    for position, character in enumerate(value):
        if character == "\\":
            consecutive_backslashes += 1
            continue
        unescaped_quote = character == '"' and consecutive_backslashes % 2 == 0
        consecutive_backslashes = 0
        if not unescaped_quote:
            continue
        if previous_quote is not None:
            after = position + 1
            while after < len(value) and value[after].isspace():
                after += 1
            if after < len(value) and value[after] == ":":
                units = 0
                valid = True
                cursor = previous_quote + 1
                while cursor < position:
                    item = value[cursor]
                    if item != "\\":
                        valid = valid and ord(item) >= 0x20
                        units += 1
                        cursor += 1
                        continue
                    units += 1
                    if cursor + 1 >= position:
                        valid = False
                        break
                    escape = value[cursor + 1]
                    if escape in '"\\/bfnrt':
                        cursor += 2
                    elif (
                        escape == "u"
                        and cursor + 5 < position
                        and all(
                            digit in "0123456789abcdefABCDEF"
                            for digit in value[cursor + 2 : cursor + 6]
                        )
                    ):
                        cursor += 6
                    else:
                        valid = False
                        cursor += 2
                if units > _CODEX_JSON_KEY_FRAGMENT_LIMIT:
                    if not valid:
                        return True, True
                    try:
                        key = json.loads(value[previous_quote : position + 1])
                    except json.JSONDecodeError:
                        return True, True
                    if not isinstance(key, str):
                        return True, True
                    if _codex_key_is_sensitive(key):
                        sensitive = True
                    else:
                        hidden = True
                    if hidden and sensitive:
                        return True, True
        previous_quote = position

    # Assignment keys are ASCII by contract. Scan their complete run once and
    # decide only when a real assignment delimiter follows it.
    index = 0
    while index < len(value):
        character = value[index]
        if not character.isascii() or not character.isalpha() or (
            index > 0 and value[index - 1].isascii() and value[index - 1].isalnum()
        ):
            index += 1
            continue
        end = index + 1
        while end < len(value):
            item = value[end]
            if not item.isascii() or not (item.isalnum() or item in "_.-"):
                break
            end += 1
        after = end
        while after < len(value) and value[after].isspace():
            after += 1
        if (
            end - index > _CODEX_ASSIGNMENT_KEY_FRAGMENT_LIMIT
            and after < len(value)
            and value[after] in ":="
        ):
            key = value[index:end]
            if _codex_key_is_sensitive(key):
                sensitive = True
            elif _normalise_codex_key(key) in _CODEX_HIDDEN_KEY_NORMALISATIONS:
                hidden = True
            elif _codex_assignment_delimiter_is_padding(value, index, end, after):
                # Only this delimiter is padding. The ordinary key and secret
                # classifiers still inspect the complete text independently.
                pass
            else:
                hidden = True
            if hidden and sensitive:
                return True, True
        index = max(end, index + 1)
    return hidden, sensitive


def _classify_codex_text_key_fragments(value: str) -> tuple[bool, bool]:
    """Classify hidden and sensitive key fragments in one shared pass."""

    has_colon = ":" in value
    has_assignment = has_colon or "=" in value
    if not has_assignment:
        return False, False
    hidden, sensitive = _classify_codex_oversized_text_key_fragments(value)
    if hidden and sensitive:
        return True, True
    if has_colon:
        for match in _CODEX_JSON_KEY_FRAGMENT_PATTERN.finditer(value):
            try:
                key = json.loads(match.group(1))
            except json.JSONDecodeError:
                return True, True
            if not isinstance(key, str):
                return True, True
            normalised = _normalise_codex_key(key)
            hidden = hidden or normalised in _CODEX_HIDDEN_KEY_NORMALISATIONS
            sensitive = sensitive or _codex_key_is_sensitive(key)
            if hidden and sensitive:
                return True, True
    for match in _CODEX_ASSIGNMENT_KEY_FRAGMENT_PATTERN.finditer(value):
        key = match.group(1)
        hidden = hidden or _normalise_codex_key(key) in _CODEX_HIDDEN_KEY_NORMALISATIONS
        sensitive = sensitive or _codex_key_is_sensitive(key)
        if hidden and sensitive:
            return True, True
    return hidden, sensitive


def _codex_text_contains_hidden_json_key(value: str) -> bool:
    hidden, _ = _classify_codex_text_key_fragments(value)
    return hidden


def _codex_key_is_sensitive(key: str) -> bool:
    normalised = _normalise_codex_key(key)
    if any(
        normalised == sensitive or normalised.endswith(sensitive)
        for sensitive in _CODEX_SENSITIVE_KEY_NORMALISATIONS
    ):
        return True
    words = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", key)
    words = re.sub(r"[^A-Za-z0-9]+", " ", words).lower().split()
    for index, word in enumerate(words):
        if word not in _CODEX_SENSITIVE_KEY_NORMALISATIONS:
            continue
        following = words[index + 1] if index + 1 < len(words) else ""
        if word == "session" and following in {"id", "name", "type"}:
            continue
        if word == "token" and following in {"count", "name", "type", "usage"}:
            continue
        return True
    return False


def _codex_text_contains_sensitive_key_fragment(value: str) -> bool:
    _, sensitive = _classify_codex_text_key_fragments(value)
    return sensitive


def _codex_key_is_omitted(key: str) -> bool:
    if key.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:[\\/]", key):
        return True
    return _normalise_codex_key(key) in _CODEX_OMITTED_KEY_NORMALISATIONS


def _sanitise_codex_url(value: str) -> str:
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError:
        return "[invalid URL omitted]"
    if parsed.scheme.lower() not in {"http", "https"} or hostname is None:
        return value
    host = f"[{hostname}]" if ":" in hostname else hostname
    if port is not None:
        host = f"{host}:{port}"
    return urlunsplit((parsed.scheme.lower(), host, parsed.path, "", ""))


def _sanitise_codex_urls_in_text(value: str) -> str:
    return _CODEX_URL_PATTERN.sub(lambda match: _sanitise_codex_url(match.group(0)), value)


_CODEX_LOCAL_PATH_PATTERN = re.compile(
    r"(?i)(?:"
    r"file:///(?:[^\r\n\"'<>/]+/)+[^\r\n\"'<>\s]+"
    r"|(?<![A-Za-z0-9:/.])/(?!/)(?:[^\r\n\"'<>/]+/)+[^\r\n\"'<>\s]+"
    r"|(?<![A-Za-z0-9])~(?:/[^\r\n\"'<>]+)+"
    r"|(?<![A-Za-z0-9])(?:[A-Z]:\\|\\\\[^\\\r\n\"'<>]+\\)"
    r"(?:[^\\\r\n\"'<>]+\\)+[^\\\r\n\"'<>\s]+)"
)


def _sanitise_codex_local_paths_in_text(value: str) -> tuple[str, int]:
    return _CODEX_LOCAL_PATH_PATTERN.subn("[local-path-omitted]", value)


def _fixed_length_codex_mask(value: object) -> str:
    if isinstance(value, str):
        size = len(value.encode("utf-8"))
    else:
        raw = json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        size = len(raw)
    return "X" * size


def _codex_value_exceeds_depth(value: object, *, maximum_depth: int = 8) -> bool:
    """Measure JSON container depth iteratively so hostile input cannot exhaust Python."""

    stack: list[tuple[object, int]] = [(value, 0)]
    visited = 0
    while stack:
        item, depth = stack.pop()
        visited += 1
        if visited > 100_000:
            return True
        if isinstance(item, list):
            if depth >= maximum_depth:
                return True
            stack.extend((child, depth + 1) for child in item)
        elif isinstance(item, dict):
            if depth >= maximum_depth:
                return True
            stack.extend((child, depth + 1) for child in item.values())
    return False


def _codex_maximum_depth_text_stub(value: str) -> dict[str, object]:
    raw = value.encode("utf-8")
    return {
        "text_omitted": True,
        "reason": "maximum-depth",
        "original_utf8_bytes": len(raw),
        "original_sha256": sha256_bytes(raw),
    }


def _codex_nested_json_string_has_sensitive_structure(value: str) -> bool:
    candidate = value
    for _ in range(4):
        structured = _strip_codex_leading_ignorables(candidate)
        if not structured.startswith('"'):
            return False
        try:
            decoded = json.loads(structured)
        except (json.JSONDecodeError, RecursionError):
            return True
        if not isinstance(decoded, str):
            return False
        hidden, sensitive = _classify_codex_text_key_fragments(decoded)
        if hidden or sensitive:
            return True
        candidate = decoded
    return _strip_codex_leading_ignorables(candidate).startswith('"')


def _redact_codex_projection_value(
    value: object,
) -> tuple[object, list[str], int]:
    """Mask sensitive keyed values before canonical JSON serialisation."""

    if _codex_value_exceeds_depth(value):
        return (
            {"projection_omitted": True, "reason": "maximum-depth"},
            ["maximum-depth"],
            1,
        )

    count = 0
    categories: set[str] = set()

    def visit(
        item: object,
        *,
        allow_hidden_count_keys: bool = False,
        depth: int = 0,
    ) -> object:
        nonlocal count
        if isinstance(item, list):
            if depth >= 8:
                count += 1
                categories.add("maximum-depth")
                return {"projection_omitted": True, "reason": "maximum-depth"}
            return [visit(child, depth=depth + 1) for child in item]
        if isinstance(item, str):
            if item == CODEX_OUTSIDE_LINEAGE_STUB:
                return item
            if item.lower().startswith("data:image/"):
                return {"image_summary": _codex_image_summary(item)}
            sanitised = _sanitise_codex_urls_in_text(item)
            sanitised, path_count = _sanitise_codex_local_paths_in_text(sanitised)
            count += path_count
            if path_count:
                categories.add("local-path")
            if _codex_nested_json_string_has_sensitive_structure(sanitised):
                count += 1
                categories.add("sensitive-key")
                raw = sanitised.encode("utf-8")
                return {
                    "text_omitted": True,
                    "reason": "nested-sensitive-structured-text",
                    "original_utf8_bytes": len(raw),
                    "original_sha256": sha256_bytes(raw),
                }
            structured = _strip_codex_leading_ignorables(sanitised)
            if structured.startswith(("{", "[")):
                oversized_hidden, oversized_sensitive = (
                    _classify_codex_oversized_text_key_fragments(sanitised)
                )
                if oversized_hidden or oversized_sensitive:
                    raw = sanitised.encode("utf-8")
                    if oversized_sensitive:
                        count += 1
                        categories.add("sensitive-key")
                    return {
                        "text_omitted": True,
                        "reason": (
                            "sensitive-structured-field"
                            if oversized_sensitive and not oversized_hidden
                            else "hidden-structured-field"
                        ),
                        "original_utf8_bytes": len(raw),
                        "original_sha256": sha256_bytes(raw),
                    }
                try:
                    embedded = json.loads(structured)
                except RecursionError:
                    count += 1
                    categories.add("maximum-depth")
                    return _codex_maximum_depth_text_stub(sanitised)
                except json.JSONDecodeError:
                    raw = sanitised.encode("utf-8")
                    return {
                        "text_omitted": True,
                        "reason": "invalid-structured-text",
                        "original_utf8_bytes": len(raw),
                        "original_sha256": sha256_bytes(raw),
                    }
                if isinstance(embedded, (dict, list)):
                    if _codex_value_exceeds_depth(embedded):
                        count += 1
                        categories.add("maximum-depth")
                        return _codex_maximum_depth_text_stub(sanitised)
                    return json.dumps(
                        # The embedded JSON is an independently bounded document.
                        # Its intrinsic depth was checked immediately above, so do
                        # not add the surrounding projection-wrapper depth again.
                        visit(embedded, depth=0),
                        ensure_ascii=False,
                        separators=(",", ":"),
                        sort_keys=True,
                    )
            hidden, sensitive = _classify_codex_text_key_fragments(sanitised)
            if hidden:
                raw = sanitised.encode("utf-8")
                return {
                    "text_omitted": True,
                    "reason": "hidden-structured-field",
                    "original_utf8_bytes": len(raw),
                    "original_sha256": sha256_bytes(raw),
                }
            if sensitive:
                count += 1
                categories.add("sensitive-key")
                raw = sanitised.encode("utf-8")
                return {
                    "text_omitted": True,
                    "reason": "sensitive-structured-field",
                    "original_utf8_bytes": len(raw),
                    "original_sha256": sha256_bytes(raw),
                }
            return sanitised
        if not isinstance(item, dict):
            return item
        if depth >= 8:
            count += 1
            categories.add("maximum-depth")
            return {"projection_omitted": True, "reason": "maximum-depth"}
        redacted: dict[str, object] = {}
        for key, child in item.items():
            if not isinstance(key, str):
                continue
            normalised = _normalise_codex_key(key)
            if (
                (
                    normalised in _CODEX_HIDDEN_KEY_NORMALISATIONS
                    and not allow_hidden_count_keys
                )
                or _codex_key_is_omitted(key)
            ):
                continue
            if _codex_key_is_sensitive(key) and not (
                allow_hidden_count_keys and key == CODEX_OUTSIDE_LINEAGE_STUB
            ):
                redacted[key] = _fixed_length_codex_mask(child)
                count += 1
                categories.add("sensitive-key")
            elif normalised in _CODEX_IMAGE_KEY_NORMALISATIONS or (
                isinstance(child, str) and child.lower().startswith("data:image/")
            ):
                redacted[f"{key}_summary"] = _codex_image_summary(child)
            elif normalised in {
                "aggregateskippedrecordtypes",
                "skippedrecordtypes",
            }:
                redacted[key] = visit(
                    child,
                    allow_hidden_count_keys=True,
                    depth=depth + 1,
                )
            else:
                redacted[key] = visit(child, depth=depth + 1)
        return redacted

    projected = visit(value)
    return projected, sorted(categories), count


def _redact_codex_projection_fixed_point(
    value: object,
) -> tuple[object, list[str], int]:
    """Return one-pass output only when a second pass proves it is stable."""

    projected, categories, count = _redact_codex_projection_value(value)
    repeated, repeated_categories, _ = _redact_codex_projection_value(projected)
    if repeated != projected:
        raise _CodexProjectionRedactionNotStable(
            sorted(set(categories) | set(repeated_categories))
        )
    return projected, categories, count


def _require_codex_projection_final_fixed_point(
    raw: bytes, categories: Sequence[str]
) -> None:
    """Require the actual byte-masked record to remain canonical and sanitised."""

    try:
        value = parse_json(raw, "byte-redacted Codex projection")
    except (EvidenceCaptureError, RecursionError):
        raise _CodexProjectionRedactionNotStable(sorted(set(categories))) from None
    normalised, final_categories, _ = _redact_codex_projection_fixed_point(value)
    if normalised != value or canonical_json(value) != raw:
        raise _CodexProjectionRedactionNotStable(
            sorted(set(categories) | set(final_categories))
        )


def _bounded_codex_text(value: str) -> object:
    sanitised = _sanitise_codex_urls_in_text(value)
    raw = sanitised.encode("utf-8")
    hidden, _ = _classify_codex_text_key_fragments(sanitised)
    if hidden:
        return {
            "text_omitted": True,
            "reason": "hidden-structured-field",
            "original_utf8_bytes": len(raw),
            "original_sha256": sha256_bytes(raw),
        }
    if len(raw) <= MAX_CODEX_TEXT_BYTES:
        return sanitised
    if _strip_codex_leading_ignorables(sanitised).startswith(("{", "[")):
        return {
            "text_omitted": True,
            "reason": "oversized-structured-text",
            "original_utf8_bytes": len(raw),
            "original_sha256": sha256_bytes(raw),
        }
    prefix = raw[:MAX_CODEX_TEXT_BYTES]
    while True:
        try:
            text = prefix.decode("utf-8")
            break
        except UnicodeDecodeError:
            prefix = prefix[:-1]
    return {
        "text": text,
        "truncated": True,
        "original_utf8_bytes": len(raw),
        "original_sha256": sha256_bytes(raw),
    }


def _codex_image_summary(value: object) -> dict[str, object]:
    values = value if isinstance(value, list) else [value]
    summaries: list[dict[str, object]] = []
    for item in values[:MAX_CODEX_CONTAINER_ITEMS]:
        if isinstance(item, str):
            raw = item.encode("utf-8")
            item_type: object | None = None
        else:
            raw = json.dumps(
                item,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
            item_type = item.get("type") if isinstance(item, dict) else None
        summary: dict[str, object] = {
            "bytes": len(raw),
            "sha256": sha256_bytes(raw),
        }
        if isinstance(item_type, str):
            summary["type"] = _bounded_codex_text(item_type)
        summaries.append(summary)
    projected: dict[str, object] = {"count": len(values), "items": summaries}
    if len(values) > MAX_CODEX_CONTAINER_ITEMS:
        projected["summarised_items"] = MAX_CODEX_CONTAINER_ITEMS
    return projected


def _bounded_codex_value(value: object, *, depth: int = 0) -> object:
    """Project bounded audit data while dropping internal-state field names."""

    if depth >= 8:
        raw = canonical_json(value)
        return {
            "truncated": True,
            "reason": "maximum-depth",
            "canonical_sha256": sha256_bytes(raw),
            "canonical_bytes": len(raw),
        }
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        if value.lower().startswith("data:image/"):
            return {"image_summary": _codex_image_summary(value)}
        return _bounded_codex_text(value)
    if isinstance(value, list):
        items = [
            _bounded_codex_value(item, depth=depth + 1)
            for item in value[:MAX_CODEX_CONTAINER_ITEMS]
        ]
        if len(value) > MAX_CODEX_CONTAINER_ITEMS:
            items.append(
                {
                    "truncated": True,
                    "reason": "maximum-list-items",
                    "original_items": len(value),
                }
            )
        return items
    if isinstance(value, dict):
        projected: dict[str, object] = {}
        visible_items = [
            (key, item)
            for key, item in sorted(value.items())
            if (
                isinstance(key, str)
                and _normalise_codex_key(key) not in _CODEX_HIDDEN_KEY_NORMALISATIONS
                and not _codex_key_is_omitted(key)
            )
        ]
        for key, item in visible_items[:MAX_CODEX_CONTAINER_ITEMS]:
            normalised = _normalise_codex_key(key)
            if normalised in _CODEX_IMAGE_KEY_NORMALISATIONS or (
                isinstance(item, str) and item.lower().startswith("data:image/")
            ):
                projected[f"{key}_summary"] = _codex_image_summary(item)
            else:
                projected[key] = _bounded_codex_value(item, depth=depth + 1)
        if len(visible_items) > MAX_CODEX_CONTAINER_ITEMS:
            projected["_projection_truncated"] = {
                "reason": "maximum-object-fields",
                "original_visible_fields": len(visible_items),
            }
        return projected
    return _bounded_codex_text(str(value))


def _codex_session_meta_projection(payload: Mapping[str, object]) -> dict[str, object]:
    projected: dict[str, object] = _codex_text_fields(payload, (
        "id",
        "session_id",
        "parent_thread_id",
        "agent_nickname",
        "agent_role",
        "timestamp",
        "cli_version",
        "originator",
        "thread_source",
        "model_provider",
    ))
    forked_from_id = payload.get("forked_from_id")
    if isinstance(forked_from_id, str) and forked_from_id:
        bounded_fork_id = _bounded_codex_text(forked_from_id)
        if isinstance(bounded_fork_id, str):
            projected["forked_from_id"] = bounded_fork_id
        projected["forked_from_id_sha256"] = _codex_forked_from_id_sha256(
            forked_from_id
        )
    agent_path = _codex_path_value(payload.get("agent_path"))
    if agent_path is not None:
        projected["agent_path"] = agent_path
    source = payload.get("source")
    if isinstance(source, dict):
        subagent = source.get("subagent")
        if isinstance(subagent, dict):
            spawn = subagent.get("thread_spawn")
            if isinstance(spawn, dict):
                allowed = _codex_text_fields(
                    spawn,
                    ("parent_thread_id", "agent_nickname", "agent_role"),
                )
                depth = spawn.get("depth")
                if isinstance(depth, int) and not isinstance(depth, bool) and depth >= 0:
                    allowed["depth"] = depth
                parent_path = _codex_path_value(spawn.get("agent_path"))
                if parent_path is not None:
                    allowed["agent_path"] = parent_path
                if allowed:
                    projected["agent_parent_path"] = allowed
    git = payload.get("git")
    if isinstance(git, dict):
        allowed_git = _codex_text_fields(
            git, ("commit_hash", "branch", "repository_url")
        )
        if allowed_git:
            projected["git"] = _bounded_codex_value(allowed_git)
    return projected


def _codex_forked_from_id_sha256(value: str) -> str:
    """Bind exact raw fork provenance without retaining its private value."""

    return sha256_bytes(CODEX_FORK_ID_DIGEST_DOMAIN + value.encode("utf-8"))


def _raw_codex_session_meta_identity(
    payload: Mapping[str, object],
) -> tuple[str, str, tuple[str, ...], str | None] | None:
    """Extract exact lineage fields before the user-visible lossy projection."""

    thread_id = payload.get("id")
    if not isinstance(thread_id, str) or not thread_id:
        return None
    if "session_id" in payload:
        session_id = payload["session_id"]
        if not isinstance(session_id, str) or not session_id:
            return None
    else:
        session_id = thread_id

    parent_references: list[str] = []

    def add_parent(value: object) -> bool:
        if value is None:
            return True
        if not isinstance(value, str) or not value:
            return False
        parent_references.append(value)
        return True

    if "parent_thread_id" in payload and not add_parent(payload["parent_thread_id"]):
        return None
    source = payload.get("source")
    if isinstance(source, Mapping):
        subagent = source.get("subagent")
        if isinstance(subagent, Mapping):
            spawn = subagent.get("thread_spawn")
            if (
                isinstance(spawn, Mapping)
                and "parent_thread_id" in spawn
                and not add_parent(spawn["parent_thread_id"])
            ):
                return None

    if len(set(parent_references)) > 1:
        return None
    fork_digest: str | None = None
    if "forked_from_id" in payload:
        forked_from_id = payload["forked_from_id"]
        if not isinstance(forked_from_id, str) or not forked_from_id:
            return None
        fork_digest = _codex_forked_from_id_sha256(forked_from_id)
    return thread_id, session_id, tuple(parent_references), fork_digest


def _codex_session_meta_within_lineage(
    payload: Mapping[str, object],
    record: CodexSessionRecord,
    allowed_thread_ids: set[str] | frozenset[str],
    *,
    raw_payload: Mapping[str, object] | None = None,
    lineage_metadata: Mapping[str, tuple[str, str | None]] | None = None,
    authoritative_forked_from_id_sha256: str | None = None,
    authoritative: bool,
) -> bool:
    """Return whether raw and projected session metadata stay in exact lineage."""

    raw_identity = _raw_codex_session_meta_identity(
        payload if raw_payload is None else raw_payload
    )
    if raw_identity is None:
        return False
    raw_thread_id, raw_session_id, raw_parent_references, raw_fork_digest = raw_identity

    thread_id = payload.get("id")
    if thread_id != raw_thread_id:
        return False
    if authoritative:
        if thread_id != record.thread_id:
            return False

    session_id = payload.get("session_id")
    effective_session_id = session_id if isinstance(session_id, str) else thread_id
    if effective_session_id != raw_session_id:
        return False

    parent_references: list[object] = []
    if "parent_thread_id" in payload:
        parent_references.append(payload["parent_thread_id"])
    parent_path = payload.get("agent_parent_path")
    if isinstance(parent_path, Mapping) and "parent_thread_id" in parent_path:
        parent_references.append(parent_path["parent_thread_id"])
    if tuple(parent_references) != raw_parent_references:
        return False
    projected_fork_digest = payload.get("forked_from_id_sha256")
    if raw_fork_digest is None:
        if projected_fork_digest is not None or "forked_from_id" in payload:
            return False
    elif projected_fork_digest != raw_fork_digest:
        return False
    if not authoritative and raw_fork_digest is not None:
        if (
            authoritative_forked_from_id_sha256 is None
            or raw_fork_digest != authoritative_forked_from_id_sha256
        ):
            return False

    if authoritative:
        if raw_session_id != record.session_id:
            return False
        if record.parent_thread_id is None:
            return not raw_parent_references
        return bool(raw_parent_references) and all(
            parent == record.parent_thread_id for parent in raw_parent_references
        )

    known_metadata = (
        lineage_metadata.get(raw_thread_id)
        if lineage_metadata is not None
        else None
    )
    if raw_thread_id in allowed_thread_ids:
        if known_metadata is None:
            if raw_thread_id != record.thread_id:
                return False
        else:
            known_session_id, known_parent_thread_id = known_metadata
            if known_session_id != record.session_id or raw_session_id != known_session_id:
                return False
            if known_parent_thread_id is None:
                if raw_parent_references:
                    return False
            elif not raw_parent_references or any(
                parent != known_parent_thread_id for parent in raw_parent_references
            ):
                return False
        return raw_session_id == record.session_id

    # A shared session alias is distinct from thread ancestry. It is admissible
    # only when no selected thread owns that identity; a sibling collision fails.
    return (
        raw_thread_id == record.session_id
        and raw_session_id == record.session_id
        and not raw_parent_references
        and (lineage_metadata is None or raw_thread_id not in lineage_metadata)
    )


def _codex_allowed_fields(
    payload: Mapping[str, object], fields: Sequence[str]
) -> dict[str, object]:
    return {
        key: _bounded_codex_value(payload[key])
        for key in fields
        if key in payload
    }


def _codex_text_fields(
    payload: Mapping[str, object], fields: Sequence[str]
) -> dict[str, object]:
    return {
        key: _bounded_codex_text(payload[key])
        for key in fields
        if isinstance(payload.get(key), str)
    }


def _codex_number_fields(
    payload: Mapping[str, object], fields: Sequence[str]
) -> dict[str, object]:
    def is_bounded_number(value: object) -> bool:
        if isinstance(value, bool):
            return False
        if isinstance(value, int):
            return 0 <= value <= 2**63 - 1
        return (
            isinstance(value, float)
            and math.isfinite(value)
            and 0 <= value <= 2**63 - 1
        )

    return {
        key: payload[key]
        for key in fields
        if is_bounded_number(payload.get(key))
    }


def _codex_path_value(value: object) -> object | None:
    if isinstance(value, str):
        return _bounded_codex_text(value)
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return [
            _bounded_codex_text(item)
            for item in value[:MAX_CODEX_CONTAINER_ITEMS]
        ]
    return None


def _codex_attachment_summary(value: object) -> dict[str, object]:
    attachments = value if isinstance(value, list) else [value]
    summary: dict[str, object] = {"count": len(attachments)}
    items: list[dict[str, object]] = []
    for attachment in attachments[:MAX_CODEX_CONTAINER_ITEMS]:
        if not isinstance(attachment, Mapping):
            continue
        item: dict[str, object] = {}
        attachment_type = attachment.get("type")
        if isinstance(attachment_type, str):
            item["type"] = _bounded_codex_text(attachment_type)
        byte_count = attachment.get("bytes", attachment.get("size_bytes"))
        if isinstance(byte_count, int) and not isinstance(byte_count, bool) and byte_count >= 0:
            item["bytes"] = byte_count
        digest = attachment.get("sha256", attachment.get("digest"))
        if isinstance(digest, str) and re.fullmatch(r"(?:sha256:)?[0-9A-Fa-f]{64}", digest):
            item["sha256"] = digest.removeprefix("sha256:").lower()
        if item:
            items.append(item)
    if items:
        summary["items"] = items
    if len(attachments) > MAX_CODEX_CONTAINER_ITEMS:
        summary["summarised_items"] = MAX_CODEX_CONTAINER_ITEMS
    return summary


def _codex_user_message_projection(payload: Mapping[str, object]) -> dict[str, object]:
    projected: dict[str, object] = {"type": "user_message"}
    message = payload.get("message")
    if isinstance(message, str):
        projected["message"] = _bounded_codex_text(message)
    summaries = {
        key: _codex_attachment_summary(payload[key])
        for key in ("images", "local_images", "audio", "local_audio", "text_elements")
        if key in payload
    }
    if summaries:
        projected["attachment_summary"] = summaries
    return projected


def _codex_memory_citation_projection(value: object) -> dict[str, object]:
    if not isinstance(value, Mapping):
        return {}
    projected: dict[str, object] = {}
    entries = value.get("entries")
    if isinstance(entries, list):
        projected_entries: list[dict[str, object]] = []
        for entry in entries[:MAX_CODEX_CONTAINER_ITEMS]:
            if not isinstance(entry, Mapping):
                continue
            projected_entry = _codex_text_fields(entry, ("note",))
            for line_key in ("lineStart", "lineEnd"):
                line = entry.get(line_key)
                if isinstance(line, int) and not isinstance(line, bool) and line >= 0:
                    projected_entry[line_key] = line
            path = entry.get("path")
            if isinstance(path, str):
                projected_entry["path_basename"] = re.split(r"[\\/]", path)[-1]
                projected_entry["path_sha256"] = sha256_bytes(path.encode("utf-8"))
            projected_entries.append(projected_entry)
        projected["entries"] = projected_entries
    rollout_ids = value.get("rolloutIds")
    if isinstance(rollout_ids, list):
        projected["rolloutIds"] = [
            _bounded_codex_text(item)
            for item in rollout_ids[:MAX_CODEX_CONTAINER_ITEMS]
            if isinstance(item, str)
        ]
    return projected


def _normalise_codex_error(value: object) -> dict[str, object]:
    normalised: dict[str, object] = {"present": bool(value)}
    if isinstance(value, Mapping):
        for key in ("code", "type", "status"):
            item = value.get(key)
            if isinstance(item, (str, int)) and not isinstance(item, bool):
                normalised[key] = _bounded_codex_value(item)
    return normalised


def _normalise_codex_reason(value: object) -> object:
    if isinstance(value, str):
        return _bounded_codex_text(value)
    if isinstance(value, Mapping):
        return _codex_text_fields(value, ("code", "kind", "type"))
    return _bounded_codex_text(type(value).__name__)


def _codex_item_completed_projection(payload: Mapping[str, object]) -> dict[str, object]:
    projected: dict[str, object] = {"type": "item_completed"}
    projected.update(_codex_text_fields(payload, ("thread_id", "turn_id")))
    projected.update(_codex_number_fields(payload, ("started_at_ms", "completed_at_ms")))
    item = payload.get("item")
    if isinstance(item, Mapping):
        descriptor = _codex_text_fields(
            item, ("agent_thread_id", "id", "kind", "type")
        )
        item_path = _codex_path_value(item.get("agent_path"))
        if item_path is not None:
            descriptor["agent_path"] = item_path
        if descriptor:
            projected["item"] = descriptor
    return projected


def _codex_mcp_tool_projection(payload: Mapping[str, object]) -> dict[str, object]:
    projected: dict[str, object] = {"type": "mcp_tool_call_end"}
    projected.update(_codex_text_fields(
        payload,
        (
            "call_id",
            "plugin_id",
            "action_name",
            "app_name",
            "connector_id",
            "link_id",
        ),
    ))
    projected.update(_codex_number_fields(payload, ("duration",)))
    if isinstance(payload.get("read_only_hint"), bool):
        projected["read_only_hint"] = payload["read_only_hint"]
    invocation = payload.get("invocation")
    if isinstance(invocation, Mapping):
        projected_invocation = _codex_text_fields(invocation, ("server", "tool"))
        if "arguments" in invocation:
            projected_invocation["arguments"] = _bounded_codex_value(
                invocation["arguments"]
            )
        if projected_invocation:
            projected["invocation"] = projected_invocation
    if "result" in payload:
        projected["result"] = _bounded_codex_value(payload["result"])
    return projected


def _codex_web_result_projection(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    results: list[dict[str, object]] = []
    for result in value[:MAX_CODEX_CONTAINER_ITEMS]:
        if not isinstance(result, Mapping):
            continue
        projected = _codex_text_fields(
            result, ("type", "ref_id", "domain", "title", "snippet")
        )
        for key in ("url", "thumbnail_url"):
            url = result.get(key)
            if isinstance(url, str) and re.match(r"(?i)^https?://", url):
                projected[key] = _sanitise_codex_url(url)
        results.append(projected)
    return results


def _codex_usage_projection(value: object) -> dict[str, int | float]:
    if not isinstance(value, Mapping):
        return {}
    return {
        key: item
        for key, item in value.items()
        if key in _CODEX_USAGE_FIELDS
        and isinstance(item, (int, float))
        and not isinstance(item, bool)
    }


def _codex_rate_limits_projection(value: object, *, depth: int = 0) -> object:
    if depth >= 4 or not isinstance(value, Mapping):
        return {}
    projected: dict[str, object] = {}
    for key, item in value.items():
        if key == "limit_id":
            continue
        if key in _CODEX_RATE_LIMIT_CONTAINER_FIELDS:
            if isinstance(item, Mapping):
                projected[key] = _codex_rate_limits_projection(item, depth=depth + 1)
            elif key == "credits" and isinstance(item, (bool, int, float)):
                projected[key] = item
        elif key in _CODEX_RATE_LIMIT_VALUE_FIELDS and isinstance(
            item, (str, bool, int, float)
        ):
            projected[key] = _bounded_codex_value(item)
    return projected


def _codex_token_count_projection(payload: Mapping[str, object]) -> dict[str, object]:
    projected: dict[str, object] = {"type": "token_count", "info": {}}
    info = payload.get("info")
    if isinstance(info, Mapping):
        projected_info: dict[str, object] = {}
        for key in ("last_token_usage", "total_token_usage"):
            if key in info:
                projected_info[key] = _codex_usage_projection(info[key])
        window = info.get("model_context_window")
        if isinstance(window, (int, float)) and not isinstance(window, bool):
            projected_info["model_context_window"] = window
        projected["info"] = projected_info
    if "rate_limits" in payload:
        projected["rate_limits"] = _codex_rate_limits_projection(payload["rate_limits"])
    return projected


def _unknown_codex_type(namespace: str, value: object) -> str:
    if not isinstance(value, str):
        return f"{namespace}:unknown"
    digest = sha256_bytes(value.encode("utf-8"))
    return f"{namespace}:unknown-sha256:{digest}"


def _parse_codex_json_container(value: object) -> object:
    if not isinstance(value, str) or not value.lstrip().startswith(("{", "[")):
        return value
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return value
    return parsed if isinstance(parsed, (dict, list)) else value


def _codex_image_descriptor(item: Mapping[str, object]) -> dict[str, object] | None:
    descriptor = _codex_allowed_fields(item, ("type", "detail", "media_type"))
    source: object | None = None
    for key in ("image_url", "url", "data", "image"):
        if key in item:
            source = item[key]
            break
    if isinstance(source, str) and re.match(r"(?i)^https?://", source):
        descriptor["url"] = _sanitise_codex_url(source)
    elif source is not None:
        if isinstance(source, str):
            raw = source.encode("utf-8")
        else:
            raw = json.dumps(
                source,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        descriptor["encoded_bytes"] = len(raw)
        descriptor["sha256"] = sha256_bytes(raw)
    else:
        encoded_bytes = item.get("encoded_bytes")
        digest = item.get("sha256")
        if isinstance(encoded_bytes, int) and encoded_bytes >= 0:
            descriptor["encoded_bytes"] = encoded_bytes
        if isinstance(digest, str) and SHA256_PATTERN.fullmatch(digest.lower()):
            descriptor["sha256"] = digest.lower()
    has_embedded_binding = "encoded_bytes" in descriptor and "sha256" in descriptor
    has_link_binding = "url" in descriptor
    if not has_embedded_binding and not has_link_binding:
        # A type/detail-only image item carries no safe, verifiable provenance.
        # Omitting it is preferable to retaining a descriptor which falsely
        # appears to bind an image that the projection does not preserve.
        return None
    return descriptor


def _codex_response_output_items(value: object) -> list[dict[str, object]]:
    if isinstance(value, str):
        return [{"type": "text", "text": _bounded_codex_text(value)}]
    if isinstance(value, list):
        candidates = value
    elif isinstance(value, Mapping):
        content = value.get("content")
        if isinstance(content, list):
            candidates = content
        else:
            candidates = [value]
    else:
        return []
    projected: list[dict[str, object]] = []
    for item in candidates[:MAX_CODEX_CONTAINER_ITEMS]:
        if isinstance(item, str):
            projected.append({"type": "text", "text": _bounded_codex_text(item)})
            continue
        if not isinstance(item, Mapping):
            continue
        item_type = item.get("type")
        text = item.get("text")
        if item_type in {"input_text", "text"} and isinstance(text, str):
            projected.append({"type": item_type, "text": _bounded_codex_text(text)})
            continue
        normalised_type = (
            _normalise_codex_key(item_type) if isinstance(item_type, str) else ""
        )
        if normalised_type in _CODEX_IMAGE_KEY_NORMALISATIONS or any(
            key in item for key in ("image_url", "image", "data")
        ):
            descriptor = _codex_image_descriptor(item)
            if descriptor is not None:
                projected.append(descriptor)
    return projected


def _codex_response_projection(
    payload: Mapping[str, object],
) -> tuple[dict[str, object] | None, str]:
    response_type = payload.get("type")
    if response_type == "reasoning":
        return None, "response_item:reasoning"
    if response_type == "compaction":
        return None, "response_item:compaction"
    if response_type == "message":
        return None, "response_item:message"
    if response_type == "agent_message":
        projected: dict[str, object] = {"type": "agent_message"}
        projected.update(
            _codex_text_fields(payload, ("author", "recipient", "status", "call_id"))
        )
        input_text: list[dict[str, object]] = []
        content = payload.get("content")
        if isinstance(content, list):
            for item in content[:MAX_CODEX_CONTAINER_ITEMS]:
                if (
                    isinstance(item, Mapping)
                    and item.get("type") == "input_text"
                    and isinstance(item.get("text"), str)
                ):
                    input_text.append(
                        {
                            "type": "input_text",
                            "text": _bounded_codex_text(item["text"]),
                        }
                    )
        projected["content"] = input_text
        return projected, ""
    if response_type in _CODEX_RESPONSE_CALL_TYPES:
        name = payload.get("name")
        if not isinstance(name, str) or not name:
            return None, "response_item:invalid-tool-call"
        projected = {"type": response_type, "name": _bounded_codex_text(name)}
        projected.update(
            _codex_text_fields(
                payload, ("namespace", "server", "call_id", "status")
            )
        )
        for key in ("input", "arguments"):
            if key in payload:
                parsed = _parse_codex_json_container(payload[key])
                projected[key] = _bounded_codex_value(parsed)
        return projected, ""
    if response_type in _CODEX_RESPONSE_OUTPUT_TYPES:
        projected = {"type": response_type}
        projected.update(_codex_text_fields(payload, ("call_id", "status")))
        output = payload.get("output")
        projected["output"] = _codex_response_output_items(output)
        return projected, ""
    return None, _unknown_codex_type("response_item", response_type)


def _codex_event_projection(payload: Mapping[str, object]) -> tuple[dict[str, object] | None, str]:
    event_type = payload.get("type")
    if event_type in _CODEX_EXCLUDED_EVENT_TYPES:
        return None, f"event_msg:{event_type}"
    if not isinstance(event_type, str) or event_type not in _CODEX_ALLOWED_EVENT_TYPES:
        return None, _unknown_codex_type("event_msg", event_type)
    if event_type == "user_message":
        return _codex_user_message_projection(payload), ""
    if event_type == "agent_message":
        projected: dict[str, object] = {"type": "agent_message"}
        projected.update(_codex_text_fields(payload, ("message", "phase")))
        if "memory_citation" in payload:
            projected["memory_citation"] = _codex_memory_citation_projection(
                payload["memory_citation"]
            )
        return projected, ""
    if event_type == "task_started":
        projected = {"type": "task_started"}
        projected.update(
            _codex_text_fields(
                payload, ("turn_id", "started_at", "collaboration_mode_kind")
            )
        )
        projected.update(_codex_number_fields(payload, ("model_context_window",)))
        return projected, ""
    if event_type == "task_complete":
        projected = {"type": "task_complete"}
        projected.update(
            _codex_text_fields(payload, ("turn_id", "started_at", "completed_at"))
        )
        projected.update(_codex_number_fields(payload, ("duration_ms",)))
        latency = _codex_number_fields(payload, ("time_to_first_token_ms",))
        if "time_to_first_token_ms" in latency:
            # Preserve this event-specific metric without granting a generic
            # exception to credential-shaped `token` keys in tool arguments.
            projected["first_output_latency_ms"] = latency["time_to_first_token_ms"]
        if "error" in payload:
            projected["error"] = _normalise_codex_error(payload["error"])
        return projected, ""
    if event_type == "sub_agent_activity":
        projected = {"type": "sub_agent_activity"}
        projected.update(
            _codex_text_fields(payload, ("agent_thread_id", "event_id", "kind"))
        )
        projected.update(_codex_number_fields(payload, ("occurred_at_ms",)))
        agent_path = _codex_path_value(payload.get("agent_path"))
        if agent_path is not None:
            projected["agent_path"] = agent_path
        return projected, ""
    if event_type == "item_completed":
        return _codex_item_completed_projection(payload), ""
    if event_type == "mcp_tool_call_end":
        return _codex_mcp_tool_projection(payload), ""
    if event_type == "patch_apply_end":
        projected = {"type": "patch_apply_end"}
        projected.update(
            _codex_text_fields(
                payload, ("call_id", "turn_id", "status", "stdout", "stderr")
            )
        )
        if isinstance(payload.get("success"), bool):
            projected["success"] = payload["success"]
        if "changes" in payload:
            changes = payload["changes"]
            if isinstance(changes, (Mapping, list)):
                projected["changes_omitted_count"] = len(changes)
            elif changes is not None:
                projected["changes_omitted_count"] = 1
            else:
                projected["changes_omitted_count"] = 0
        return projected, ""
    if event_type == "web_search_end":
        projected = {"type": "web_search_end"}
        projected.update(_codex_text_fields(payload, ("call_id", "action", "query")))
        projected["results"] = _codex_web_result_projection(payload.get("results"))
        return projected, ""
    if event_type == "token_count":
        return _codex_token_count_projection(payload), ""
    projected = {"type": "turn_aborted"}
    projected.update(
        _codex_text_fields(payload, ("turn_id", "started_at", "completed_at"))
    )
    projected.update(_codex_number_fields(payload, ("duration_ms",)))
    if "reason" in payload:
        projected["reason"] = _normalise_codex_reason(payload["reason"])
    return projected, ""


def _project_codex_record(value: object) -> tuple[dict[str, object] | None, str]:
    if not isinstance(value, dict):
        return None, "invalid:non-object"
    record_type = value.get("type")
    timestamp = value.get("timestamp")
    payload = value.get("payload")
    if record_type in {"compacted", "world_state", "turn_context"}:
        return None, str(record_type)
    if record_type == "session_meta" and isinstance(payload, dict):
        projected_payload = _codex_session_meta_projection(payload)
    elif record_type == "response_item" and isinstance(payload, dict):
        projected_payload, reason = _codex_response_projection(payload)
        if projected_payload is None:
            return None, reason
    elif record_type == "event_msg" and isinstance(payload, dict):
        projected_payload, reason = _codex_event_projection(payload)
        if projected_payload is None:
            return None, reason
    elif record_type == "inter_agent_communication_metadata" and isinstance(payload, dict):
        trigger_turn = payload.get("trigger_turn")
        projected_payload = {}
        if isinstance(trigger_turn, str):
            projected_payload["trigger_turn"] = _bounded_codex_text(trigger_turn)
        elif (
            isinstance(trigger_turn, int)
            and not isinstance(trigger_turn, bool)
            and trigger_turn >= 0
        ):
            projected_payload["trigger_turn"] = trigger_turn
    else:
        return None, _unknown_codex_type("top", record_type)
    projected: dict[str, object] = {
        "source_type": record_type,
        "payload": projected_payload,
    }
    if isinstance(timestamp, str):
        projected["timestamp"] = _bounded_codex_text(timestamp)
    return projected, ""


def _write_all(descriptor: int, raw: bytes) -> None:
    view = memoryview(raw)
    while view:
        written = os.write(descriptor, view)
        view = view[written:]


def _top_level_json_type_from_prefix(raw: bytes) -> str | None:
    """Read a top-level JSON `type` string without entering a large payload."""

    depth = 0
    index = 0
    size = len(raw)
    while index < size:
        byte = raw[index]
        if byte == 0x7B:  # {
            depth += 1
            index += 1
            continue
        if byte == 0x7D:  # }
            depth -= 1
            index += 1
            continue
        if byte != 0x22:  # "
            index += 1
            continue
        start = index
        index += 1
        escaped = False
        while index < size:
            current = raw[index]
            if escaped:
                escaped = False
            elif current == 0x5C:
                escaped = True
            elif current == 0x22:
                break
            index += 1
        if index >= size:
            return None
        end = index + 1
        if depth != 1:
            index = end
            continue
        cursor = end
        while cursor < size and raw[cursor] in b" \t\r\n":
            cursor += 1
        if cursor >= size or raw[cursor] != 0x3A:  # :
            index = end
            continue
        try:
            key = json.loads(raw[start:end].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None
        if key != "type":
            index = end
            continue
        cursor += 1
        while cursor < size and raw[cursor] in b" \t\r\n":
            cursor += 1
        if cursor >= size or raw[cursor] != 0x22:
            return None
        value_start = cursor
        cursor += 1
        escaped = False
        while cursor < size:
            current = raw[cursor]
            if escaped:
                escaped = False
            elif current == 0x5C:
                escaped = True
            elif current == 0x22:
                try:
                    value = json.loads(raw[value_start : cursor + 1].decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    return None
                return value if isinstance(value, str) else None
            cursor += 1
        return None
    return None


def _codex_stub_kind(skipped_type: str) -> str:
    if (
        skipped_type in {"compacted", "world_state", "turn_context"}
        or skipped_type == "response_item:reasoning"
        or skipped_type == "response_item:compaction"
        or skipped_type == "response_item:message"
        or skipped_type.startswith("response_item:message:")
        or skipped_type in {
            "event_msg:agent_reasoning",
            "event_msg:context_compacted",
            "event_msg:thread_settings",
            "event_msg:thread_settings_applied",
        }
    ):
        return "excluded-rollout-record"
    return "unsupported-rollout-record"


def _gzip_projection(source: Path, incoming: Path) -> tuple[StagedObject, str, int]:
    source_bytes = source.stat().st_size
    if shutil.disk_usage(incoming).free < MIN_STORE_FREE_BYTES + source_bytes + 1024 * 1024:
        raise EvidenceCaptureError(
            "private store lacks free-space reserve for projection compression"
        )
    uncompressed_digest = hashlib.sha256()
    uncompressed_bytes = 0
    compressed_path = incoming / f"{uuid.uuid4().hex}.jsonl.gz"
    descriptor = os.open(compressed_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with source.open("rb") as input_stream, os.fdopen(
            descriptor, "wb", closefd=False
        ) as output_stream:
            with gzip.GzipFile(
                filename="",
                mode="wb",
                compresslevel=9,
                fileobj=output_stream,
                mtime=0,
            ) as compressed:
                while chunk := input_stream.read(1024 * 1024):
                    uncompressed_digest.update(chunk)
                    uncompressed_bytes += len(chunk)
                    compressed.write(chunk)
            output_stream.flush()
            os.fsync(output_stream.fileno())
    except Exception:
        os.close(descriptor)
        compressed_path.unlink(missing_ok=True)
        raise
    os.close(descriptor)
    return rehash_staged(compressed_path), uncompressed_digest.hexdigest(), uncompressed_bytes


def _codex_projection_identity(
    record: CodexSessionRecord,
    *,
    path_digest: str,
    raw_source_sha256: str,
    source_stat_before: Mapping[str, int],
    object_sha256: str,
) -> str:
    stat_digest = sha256_bytes(canonical_json(source_stat_before))
    return (
        f"codex-user-visible-projection:thread:{record.thread_id}:session:{record.session_id}:"
        f"path-sha256:{path_digest}:source-sha256:{raw_source_sha256}:"
        f"source-stat-sha256:{stat_digest}:projection-sha256:{object_sha256}"
    )


def stage_codex_user_visible_projection(
    record: CodexSessionRecord,
    incoming: Path,
    *,
    allowed_session_thread_ids: set[str] | frozenset[str] | None = None,
    session_lineage_metadata: Mapping[str, tuple[str, str | None]] | None = None,
    read_path: Path | None = None,
    read_descriptor: int | None = None,
    provenance_stat_before: dict[str, int] | None = None,
    provenance_stat_after: dict[str, int] | None = None,
    source_changed_after_snapshot: bool = False,
    max_projection_bytes: int = MAX_OBJECT_BYTES,
) -> CodexProjection:
    """Stream one rollout into a redacted, deterministic, user-visible projection."""

    if read_path is not None and read_descriptor is not None:
        raise EvidenceCaptureError("Codex projection read source is ambiguous")
    if max_projection_bytes < 1 or max_projection_bytes > MAX_OBJECT_BYTES:
        raise EvidenceCaptureError("Codex projection byte boundary is invalid")
    allowed_lineage = set(
        (
            {
                record.thread_id,
                *(
                    (record.parent_thread_id,)
                    if record.parent_thread_id is not None
                    else ()
                ),
            }
            if allowed_session_thread_ids is None
            else allowed_session_thread_ids
        )
    )
    if record.thread_id not in allowed_lineage:
        raise EvidenceCaptureError("Codex projection lineage is incomplete")
    if shutil.disk_usage(incoming).free < MIN_STORE_FREE_BYTES:
        raise EvidenceCaptureError("private store has less than the required free-space reserve")
    projection_source = read_path or record.path
    if read_descriptor is None:
        before = projection_source.lstat()
        _validate_local_source_metadata(projection_source, before)
        source_descriptor = os.open(
            projection_source, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        )
    else:
        source_descriptor = os.dup(read_descriptor)
        before = os.fstat(source_descriptor)
        if not stat.S_ISREG(before.st_mode):
            os.close(source_descriptor)
            raise EvidenceCaptureError("Codex projection descriptor is not a regular file")
    if before.st_uid != os.getuid() or stat.S_IMODE(before.st_mode) & 0o022:
        os.close(source_descriptor)
        raise EvidenceCaptureError("Codex session file is not safely owned by the current user")
    source_stat_before = provenance_stat_before or _recorded_source_stat(before)
    path_digest = sha256_bytes(os.fsencode(str(record.path.resolve(strict=True))))
    projection_path = incoming / f"{uuid.uuid4().hex}.projection.jsonl"
    projection_descriptor = os.open(
        projection_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
    )
    raw_digest = hashlib.sha256()
    skipped: dict[str, int] = {}
    retained = 0
    line_number = 0
    projection_bytes = 0
    next_free_space_check = 0
    redaction_totals: dict[str, int] = {}
    unredactable_categories: set[str] = set()
    authoritative_forked_from_id_sha256: str | None = None

    def emit_projection_line(
        value: object,
        *,
        fallback: object | None = None,
    ) -> bool:
        nonlocal next_free_space_check, projection_bytes
        value, structured_categories, structured_count = (
            _redact_codex_projection_fixed_point(value)
        )
        raw_value = canonical_json(value)
        if len(raw_value) > MAX_CODEX_PROJECTED_LINE_BYTES:
            raise EvidenceCaptureError("projected Codex record exceeds the byte boundary")
        try:
            redacted, categories, count = redact_projection_bytes(raw_value)
        except UnredactableSecretError as error:
            if fallback is None:
                raise
            unredactable_categories.add(str(error))
            redacted, categories, count = redact_projection_bytes(canonical_json(fallback))
            emitted = False
        else:
            emitted = True
        _require_codex_projection_final_fixed_point(
            redacted, structured_categories + categories
        )
        all_categories = structured_categories + categories
        all_count = structured_count + count
        for category in all_categories:
            redaction_totals[category] = redaction_totals.get(category, 0) + 1
        if all_count != len(all_categories):
            # Preserve an exact occurrence count even when one category occurs repeatedly.
            repeated = all_count - len(all_categories)
            if repeated:
                redaction_totals["_additional_occurrences"] = (
                    redaction_totals.get("_additional_occurrences", 0) + repeated
                )
        projection_bytes += len(redacted)
        if projection_bytes > max_projection_bytes:
            raise EvidenceCaptureError("uncompressed Codex projection exceeds the byte boundary")
        _write_all(projection_descriptor, redacted)
        if projection_bytes >= next_free_space_check:
            if shutil.disk_usage(incoming).free < MIN_STORE_FREE_BYTES:
                raise EvidenceCaptureError(
                    "private store has less than the required free-space reserve"
                )
            next_free_space_check = projection_bytes + 64 * 1024 * 1024
        return emitted

    try:
        opened = os.fstat(source_descriptor)
        if _source_signature(opened) != _source_signature(before):
            raise EvidenceCaptureError("Codex session identity changed before projection")
        header = {
            "schema": CODEX_PROJECTION_SCHEMA,
            "record": "projection-header",
            "thread_id": record.thread_id,
            "session_id": record.session_id,
            "parent_thread_id": record.parent_thread_id,
            "source_path_sha256": path_digest,
            "boundaries": BOUNDARIES,
        }
        emit_projection_line(header)
        with os.fdopen(source_descriptor, "rb", closefd=False) as source_stream:
            while True:
                prefix = source_stream.readline(MAX_CODEX_PREFIX_BYTES + 1)
                if not prefix:
                    break
                line_number += 1
                if prefix.endswith(b"\n"):
                    raw = prefix
                else:
                    top_level_type = _top_level_json_type_from_prefix(prefix)
                    if top_level_type in {"compacted", "world_state", "turn_context"}:
                        line_digest = hashlib.sha256(prefix)
                        raw_digest.update(prefix)
                        consumed = len(prefix)
                        final_chunk = prefix
                        while final_chunk and not final_chunk.endswith(b"\n"):
                            final_chunk = source_stream.readline(1024 * 1024)
                            if not final_chunk:
                                break
                            consumed += len(final_chunk)
                            raw_digest.update(final_chunk)
                            line_digest.update(final_chunk)
                        skipped_type = str(top_level_type)
                        skipped[skipped_type] = skipped.get(skipped_type, 0) + 1
                        stub = {
                            "record": "excluded-rollout-record",
                            "source_line": line_number,
                            "source_line_sha256": line_digest.hexdigest(),
                            "source_bytes": consumed,
                            "source_type": skipped_type,
                        }
                        emit_projection_line(stub)
                        continue
                    chunks = [prefix]
                    total = len(prefix)
                    final_chunk = prefix
                    while final_chunk and not final_chunk.endswith(b"\n"):
                        final_chunk = source_stream.readline(1024 * 1024)
                        if not final_chunk:
                            break
                        total += len(final_chunk)
                        if total > MAX_CODEX_LINE_BYTES:
                            raise EvidenceCaptureError(
                                "allowed or unknown Codex record exceeds the line boundary"
                            )
                        chunks.append(final_chunk)
                    raw = b"".join(chunks)
                raw_digest.update(raw)
                line_sha256 = sha256_bytes(raw)
                if not raw.strip():
                    skipped["blank"] = skipped.get("blank", 0) + 1
                    stub = {
                        "record": "unsupported-rollout-record",
                        "source_line": line_number,
                        "source_line_sha256": line_sha256,
                        "source_bytes": len(raw),
                        "source_type": "blank",
                    }
                    emit_projection_line(stub)
                    continue
                value = parse_json(raw, f"Codex session record {line_number}")
                projected, skipped_type = _project_codex_record(value)
                if projected is None:
                    skipped[skipped_type] = skipped.get(skipped_type, 0) + 1
                    stub = {
                        "record": _codex_stub_kind(skipped_type),
                        "source_line": line_number,
                        "source_line_sha256": line_sha256,
                        "source_bytes": len(raw),
                        "source_type": skipped_type,
                    }
                    emit_projection_line(stub)
                    continue
                if projected.get("source_type") == "session_meta":
                    projected_payload = projected.get("payload")
                    raw_payload = (
                        value.get("payload") if isinstance(value, Mapping) else None
                    )
                    authoritative = line_number == 1
                    if authoritative and isinstance(raw_payload, Mapping):
                        raw_identity = _raw_codex_session_meta_identity(raw_payload)
                        if raw_identity is not None:
                            authoritative_forked_from_id_sha256 = raw_identity[3]
                    if not isinstance(projected_payload, Mapping) or not (
                        _codex_session_meta_within_lineage(
                            projected_payload,
                            record,
                            allowed_lineage,
                            raw_payload=(
                                raw_payload if isinstance(raw_payload, Mapping) else None
                            ),
                            lineage_metadata=session_lineage_metadata,
                            authoritative_forked_from_id_sha256=(
                                authoritative_forked_from_id_sha256
                            ),
                            authoritative=authoritative,
                        )
                    ):
                        if authoritative:
                            raise EvidenceCaptureError(
                                "Codex first session metadata differs from its inventory"
                            )
                        skipped_type = CODEX_OUTSIDE_LINEAGE_STUB
                        skipped[skipped_type] = skipped.get(skipped_type, 0) + 1
                        stub = {
                            "record": "excluded-rollout-record",
                            "source_line": line_number,
                            "source_line_sha256": line_sha256,
                            "source_bytes": len(raw),
                            "source_type": skipped_type,
                        }
                        emit_projection_line(stub)
                        continue
                projected_line = {
                    "record": "projected-rollout-record",
                    "source_line": line_number,
                    "source_line_sha256": line_sha256,
                    "source_bytes": len(raw),
                    **projected,
                }
                if _codex_value_exceeds_depth(projected_line):
                    skipped_type = "projection:maximum-depth"
                    skipped[skipped_type] = skipped.get(skipped_type, 0) + 1
                    emit_projection_line(
                        {
                            "record": "excluded-rollout-record",
                            "source_line": line_number,
                            "source_line_sha256": line_sha256,
                            "source_bytes": len(raw),
                            "source_type": skipped_type,
                        }
                    )
                    continue
                line = canonical_json(projected_line)
                if len(line) > MAX_CODEX_PROJECTED_LINE_BYTES:
                    raise EvidenceCaptureError("projected Codex record exceeds the byte boundary")
                secret_stub = {
                    "record": "excluded-rollout-record",
                    "source_line": line_number,
                    "source_line_sha256": line_sha256,
                    "source_bytes": len(raw),
                    "source_type": "unredactable-secret:private-key-block",
                }
                try:
                    emitted = emit_projection_line(projected_line, fallback=secret_stub)
                except _CodexProjectionRedactionNotStable as error:
                    suffix = (
                        "maximum-depth"
                        if "maximum-depth" in error.categories
                        else "fixed-point"
                    )
                    skipped_type = f"projection:redaction-{suffix}"
                    skipped[skipped_type] = skipped.get(skipped_type, 0) + 1
                    emit_projection_line(
                        {
                            "record": "excluded-rollout-record",
                            "source_line": line_number,
                            "source_line_sha256": line_sha256,
                            "source_bytes": len(raw),
                            "source_type": skipped_type,
                        }
                    )
                    continue
                if emitted:
                    retained += 1
                else:
                    skipped_type = "unredactable-secret:private-key-block"
                    skipped[skipped_type] = skipped.get(skipped_type, 0) + 1
        after_fd = os.fstat(source_descriptor)
        after_path = (
            projection_source.lstat() if read_descriptor is None else after_fd
        )
        path_changed = (
            read_descriptor is None
            and _source_signature(before) != _source_signature(after_path)
        )
        if _source_signature(before) != _source_signature(after_fd) or path_changed:
            raise EvidenceCaptureError("Codex session changed while it was projected")
        footer = {
            "schema": CODEX_PROJECTION_SCHEMA,
            "record": "projection-footer",
            "source_sha256": raw_digest.hexdigest(),
            "source_bytes": after_fd.st_size,
            "source_stat_before": source_stat_before,
            "source_stat_after": provenance_stat_after or _recorded_source_stat(after_path),
            "source_records": line_number,
            "retained_records": retained,
            "skipped_record_types": dict(sorted(skipped.items())),
        }
        emit_projection_line(footer)
        os.fsync(projection_descriptor)
    except Exception:
        os.close(source_descriptor)
        os.close(projection_descriptor)
        projection_path.unlink(missing_ok=True)
        raise
    os.close(source_descriptor)
    os.close(projection_descriptor)

    redaction_categories = sorted(
        category for category in redaction_totals if category != "_additional_occurrences"
    )
    redaction_count = sum(
        count
        for category, count in redaction_totals.items()
        if category != "_additional_occurrences"
    ) + redaction_totals.get("_additional_occurrences", 0)
    if unredactable_categories:
        uncompressed_before = rehash_staged(projection_path)
        projection_path.unlink(missing_ok=True)
        source_stat_after = provenance_stat_after or _recorded_source_stat(after_path)
        category = sorted(unredactable_categories)[0]
        identity = (
            f"codex-user-visible-projection:thread:{record.thread_id}:"
            f"session:{record.session_id}:path-sha256:{path_digest}:"
            f"source-sha256:{raw_digest.hexdigest()}:excluded:{category}"
        )
        source = _source_value(
            kind="codex-user-visible-projection",
            identity=identity,
            label=record.path.name,
            occurred_at_utc=record.timestamp,
            expires_at_utc=None,
            expiry_basis="unknown",
            commit_sha=None,
            tree_sha=None,
            redaction_mode="fixed-length-high-confidence-projection-redaction",
            snapshot_method="streamed-user-visible-projection",
            source_stat_before=source_stat_before,
            source_stat_after=source_stat_after,
            source_changed_after_snapshot=source_changed_after_snapshot,
            collection_generation_sha256=None,
            collection_window=None,
            redaction_categories=sorted(unredactable_categories),
            redaction_count=len(unredactable_categories),
        )
        return CodexProjection(
            record=record,
            staged=None,
            identity=identity,
            source=source,
            disposition="excluded",
            reason=f"unredactable-secret-category:{category}",
            raw_source_sha256=raw_digest.hexdigest(),
            uncompressed_sha256=uncompressed_before.sha256,
            uncompressed_bytes=uncompressed_before.bytes,
            skipped_record_types=dict(sorted(skipped.items())),
            retained_records=retained,
            object_sha256=None,
            object_bytes=None,
            reused=False,
        )

    staged, uncompressed_sha256, uncompressed_bytes = _gzip_projection(
        projection_path, incoming
    )
    projection_path.unlink(missing_ok=True)
    source_stat_after = provenance_stat_after or _recorded_source_stat(after_path)
    identity = _codex_projection_identity(
        record,
        path_digest=path_digest,
        raw_source_sha256=raw_digest.hexdigest(),
        source_stat_before=source_stat_before,
        object_sha256=staged.sha256,
    )
    source = _source_value(
        kind="codex-user-visible-projection",
        identity=identity,
        label=record.path.name,
        occurred_at_utc=record.timestamp,
        expires_at_utc=None,
        expiry_basis="unknown",
        commit_sha=None,
        tree_sha=None,
        redaction_mode="fixed-length-high-confidence-projection-redaction",
        snapshot_method="streamed-user-visible-projection",
        source_stat_before=source_stat_before,
        source_stat_after=source_stat_after,
        source_changed_after_snapshot=source_changed_after_snapshot,
        collection_generation_sha256=None,
        collection_window=None,
        redaction_categories=redaction_categories,
        redaction_count=redaction_count,
    )
    return CodexProjection(
        record=record,
        staged=staged,
        identity=identity,
        source=source,
        disposition="captured",
        reason=None,
        raw_source_sha256=raw_digest.hexdigest(),
        uncompressed_sha256=uncompressed_sha256,
        uncompressed_bytes=uncompressed_bytes,
        skipped_record_types=dict(sorted(skipped.items())),
        retained_records=retained,
        object_sha256=staged.sha256,
        object_bytes=staged.bytes,
        reused=False,
    )


def _parse_codex_session_meta(
    first: bytes,
    *,
    label: str,
) -> tuple[str, str, str | None, str]:
    if not first or len(first) > MAX_METADATA_BYTES:
        raise EvidenceCaptureError("Codex session first record is missing or oversized")
    value = parse_json(first, label)
    if (
        not isinstance(value, dict)
        or value.get("type") != "session_meta"
        or not isinstance(value.get("payload"), dict)
    ):
        raise EvidenceCaptureError("Codex session does not start with a session_meta record")
    payload = value["payload"]
    identity = _raw_codex_session_meta_identity(payload)
    if identity is None:
        raise EvidenceCaptureError("Codex session lineage metadata is invalid")
    thread_id, session_id, parent_references, _fork_digest = identity
    parent = parent_references[0] if parent_references else None
    timestamp = payload.get("timestamp") or value.get("timestamp")
    if not isinstance(timestamp, str):
        raise EvidenceCaptureError("Codex session metadata has no timestamp")
    timestamp = format_time(parse_time(timestamp, "Codex session timestamp"))
    return thread_id, session_id, parent, timestamp


def _read_codex_session_record(path: Path) -> CodexSessionRecord:
    metadata = path.lstat()
    _validate_local_source_metadata(path, metadata)
    if metadata.st_uid != os.getuid() or stat.S_IMODE(metadata.st_mode) & 0o022:
        raise EvidenceCaptureError("Codex session file is not safely owned by the current user")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            first = stream.readline(MAX_METADATA_BYTES + 1)
    finally:
        os.close(descriptor)
    thread_id, session_id, parent, timestamp = _parse_codex_session_meta(
        first,
        label="Codex session first record",
    )
    after = path.lstat()
    if (
        after.st_dev != metadata.st_dev
        or after.st_ino != metadata.st_ino
        or not stat.S_ISREG(after.st_mode)
    ):
        raise EvidenceCaptureError("Codex session path changed during metadata inventory")
    return CodexSessionRecord(path, thread_id, session_id, parent, timestamp, after)


def _verify_cloned_codex_session_record(
    descriptor: int,
    record: CodexSessionRecord,
) -> None:
    prefix = os.pread(descriptor, MAX_METADATA_BYTES + 1, 0)
    newline = prefix.find(b"\n")
    first = prefix[: newline + 1] if newline >= 0 else prefix
    observed = _parse_codex_session_meta(
        first,
        label="cloned Codex session first record",
    )
    expected = (
        record.thread_id,
        record.session_id,
        record.parent_thread_id,
        record.timestamp,
    )
    if observed != expected:
        raise EvidenceCaptureError("cloned Codex session metadata differs from inventory")


def _iter_explicit_codex_records(roots: Sequence[Path]) -> list[CodexSessionRecord]:
    records: list[CodexSessionRecord] = []
    seen_paths: set[Path] = set()
    for root in roots:
        root_metadata = root.lstat()
        if root.is_symlink() or not stat.S_ISDIR(root_metadata.st_mode):
            raise EvidenceCaptureError("Codex session root must be an explicit real directory")
        for current, directory_names, file_names in os.walk(root, followlinks=False):
            current_path = Path(current)
            for name in sorted(directory_names):
                child = current_path / name
                child_metadata = child.lstat()
                if child.is_symlink() or not stat.S_ISDIR(child_metadata.st_mode):
                    raise EvidenceCaptureError("Codex session root contains a linked directory")
            for name in sorted(file_names):
                if not name.endswith(".jsonl"):
                    continue
                path = current_path / name
                resolved = path.resolve(strict=True)
                if resolved in seen_paths:
                    continue
                seen_paths.add(resolved)
                records.append(_read_codex_session_record(path))
    return records


def _select_codex_thread_closure(
    inventory: Sequence[CodexSessionRecord],
    thread_id: str,
) -> list[CodexSessionRecord]:
    selected_ids = {
        record.thread_id
        for record in inventory
        if record.thread_id == thread_id
    }
    if not selected_ids:
        session_roots = {
            record.thread_id
            for record in inventory
            if record.session_id == thread_id and record.parent_thread_id is None
        }
        if len(session_roots) != 1:
            raise EvidenceCaptureError(
                "Codex thread id was not found uniquely in the explicit session roots"
            )
        selected_ids = session_roots
    changed = True
    while changed:
        before_count = len(selected_ids)
        selected_ids.update(
            record.thread_id
            for record in inventory
            if record.parent_thread_id in selected_ids
        )
        changed = len(selected_ids) != before_count
    return sorted(
        (record for record in inventory if record.thread_id in selected_ids),
        key=lambda item: (item.timestamp, item.thread_id, str(item.path)),
    )


def _require_unique_codex_thread_identities(
    records: Sequence[CodexSessionRecord],
) -> None:
    thread_ids: set[str] = set()
    for record in records:
        if record.thread_id in thread_ids:
            raise EvidenceCaptureError(
                "Codex thread closure contains a duplicate thread identity"
            )
        thread_ids.add(record.thread_id)


def _require_acyclic_codex_thread_graph(
    records: Sequence[CodexSessionRecord],
) -> None:
    """Reject self-parenting and cycles wholly inside the selected closure."""

    parents = {record.thread_id: record.parent_thread_id for record in records}
    for thread_id, parent_thread_id in parents.items():
        if parent_thread_id == thread_id:
            raise EvidenceCaptureError("Codex thread closure contains a self-parent edge")
        visited: set[str] = set()
        current: str | None = thread_id
        while current is not None and current in parents:
            if current in visited:
                raise EvidenceCaptureError("Codex thread closure contains a parent cycle")
            visited.add(current)
            current = parents[current]


def _codex_session_lineages(
    records: Sequence[CodexSessionRecord],
) -> dict[str, frozenset[str]]:
    """Build each selected thread's exact current-and-ancestor thread set."""

    parents = {record.thread_id: record.parent_thread_id for record in records}
    sessions = {record.thread_id: record.session_id for record in records}
    selected_thread_ids = set(parents)
    lineages: dict[str, frozenset[str]] = {}
    for thread_id, session_id in sessions.items():
        allowed = {thread_id}
        visited: set[str] = set()
        current = thread_id
        while current in parents:
            if current in visited:
                raise EvidenceCaptureError("Codex thread closure contains a parent cycle")
            visited.add(current)
            parent = parents[current]
            if parent is None:
                break
            allowed.add(parent)
            current = parent
        if session_id in selected_thread_ids and session_id not in allowed:
            raise EvidenceCaptureError(
                "Codex session alias collides with a selected non-ancestor thread"
            )
        lineages[thread_id] = frozenset(allowed)
    return lineages


def _codex_manifest_lineage_context(
    files: Sequence[Mapping[str, object]],
) -> tuple[
    dict[str, frozenset[str]],
    dict[str, tuple[str, str | None]],
]:
    """Build the per-thread lineage sets and metadata bound by one manifest."""

    parents = {
        str(item["thread_id"]): item["parent_thread_id"]
        for item in files
    }
    metadata = {
        str(item["thread_id"]): (
            str(item["session_id"]),
            item["parent_thread_id"],
        )
        for item in files
    }
    lineages: dict[str, frozenset[str]] = {}
    selected_thread_ids = set(parents)
    for thread_id, (session_id, _parent_thread_id) in metadata.items():
        allowed = {thread_id}
        visited: set[str] = set()
        current = thread_id
        while current in parents:
            if current in visited:
                raise EvidenceCaptureError("Codex generation contains a parent cycle")
            visited.add(current)
            parent = parents[current]
            if parent is None:
                break
            if not isinstance(parent, str) or not parent:
                raise EvidenceCaptureError("Codex generation parent metadata is invalid")
            allowed.add(parent)
            current = parent
        if session_id in selected_thread_ids and session_id not in allowed:
            raise EvidenceCaptureError(
                "Codex generation session alias collides with a non-ancestor thread"
            )
        lineages[thread_id] = frozenset(allowed)
    return lineages, metadata


def _reusable_codex_projections(
    store: EvidenceStore,
    records: Sequence[CodexSessionRecord],
) -> dict[str, CodexProjection]:
    """Find completed projections matching an exact current path/stat snapshot."""

    current_lineages = _codex_session_lineages(records)
    current_metadata = {
        record.thread_id: (record.session_id, record.parent_thread_id)
        for record in records
    }
    wanted: dict[tuple[str, str], CodexSessionRecord] = {}
    for record in records:
        current = record.path.lstat()
        _validate_local_source_metadata(record.path, current)
        if _source_signature(current) != _source_signature(record.metadata):
            continue
        path_digest = sha256_bytes(os.fsencode(str(record.path.resolve(strict=True))))
        stat_digest = sha256_bytes(canonical_json(_recorded_source_stat(current)))
        wanted[(path_digest, stat_digest)] = record
    reusable: dict[str, CodexProjection] = {}
    considered_paths: set[str] = set()
    wanted_paths = {path_digest for path_digest, _stat_digest in wanted}
    for event in reversed(store.events):
        if event["source"]["kind"] != "codex-thread-closure-generation-manifest":
            continue
        if event["disposition"]["status"] != "captured" or len(event["objects"]) != 1:
            continue
        try:
            from verify_delivery_evidence import validate_reusable_codex_generation

            manifest = validate_reusable_codex_generation(
                store.root,
                store.events,
                str(event["source"]["identity"]),
                required_projection_schema=CODEX_PROJECTION_SCHEMA,
            )
            if manifest is None:
                continue
        except (
            EvidenceCaptureError,
            ImportError,
            KeyError,
            OSError,
            TypeError,
            ValueError,
        ):
            raise EvidenceCaptureError(
                "prior Codex generation failed semantic validation"
            ) from None
        prior_lineages, prior_metadata = _codex_manifest_lineage_context(
            manifest["files"]
        )
        for item in manifest["files"]:
            if not isinstance(item, dict) or set(item) != CODEX_GENERATION_FILE_KEYS:
                raise EvidenceCaptureError("prior Codex generation file entry is invalid")
            path_digest = item.get("source_path_sha256")
            identity = item.get("source_identity")
            if not isinstance(path_digest, str) or not isinstance(identity, str):
                raise EvidenceCaptureError("prior Codex generation identity is invalid")
            if path_digest in considered_paths:
                continue
            considered_paths.add(path_digest)
            source_event = store.identities.get(identity)
            if source_event is None or source_event["source"]["kind"] != "codex-user-visible-projection":
                raise EvidenceCaptureError("prior Codex generation projection is missing")
            source = source_event["source"]
            if source["source_changed_after_snapshot"] is not False:
                continue
            source_stat = source["source_stat_before"]
            if source_stat != source["source_stat_after"] or not isinstance(source_stat, dict):
                continue
            final_stat = item["source_stat_final_observation"]
            final_changed = item["source_changed_by_final_observation"]
            if (
                not isinstance(final_stat, dict)
                or set(final_stat) != {
                    "device",
                    "inode",
                    "mode",
                    "links",
                    "owner_uid",
                    "bytes",
                    "mtime_ns",
                    "ctime_ns",
                }
                or not isinstance(final_changed, bool)
                or final_changed is not (source["source_stat_after"] != final_stat)
            ):
                raise EvidenceCaptureError("prior Codex final source observation is invalid")
            if final_changed or final_stat != source_stat:
                continue
            stat_digest = sha256_bytes(canonical_json(source_stat))
            record = wanted.get((path_digest, stat_digest))
            if record is None or path_digest in reusable:
                continue
            current_lineage = current_lineages[record.thread_id]
            if prior_lineages.get(record.thread_id) != current_lineage:
                continue
            prior_alias_collision = (
                record.session_id in prior_metadata
                and record.session_id not in prior_lineages[record.thread_id]
            )
            current_alias_collision = (
                record.session_id in current_metadata
                and record.session_id not in current_lineage
            )
            if prior_alias_collision != current_alias_collision:
                continue
            prior_lineage_metadata = {
                lineage_thread: prior_metadata[lineage_thread]
                for lineage_thread in current_lineage
                if lineage_thread in prior_metadata
            }
            current_lineage_metadata = {
                lineage_thread: current_metadata[lineage_thread]
                for lineage_thread in current_lineage
                if lineage_thread in current_metadata
            }
            if prior_lineage_metadata != current_lineage_metadata:
                continue
            disposition = source_event["disposition"]["status"]
            if disposition not in {"captured", "excluded"}:
                continue
            object_sha256 = item.get("object_sha256")
            object_bytes = item.get("object_bytes")
            if disposition == "captured":
                if (
                    len(source_event["objects"]) != 1
                    or source_event["objects"][0]["sha256"] != object_sha256
                    or source_event["objects"][0]["bytes"] != object_bytes
                ):
                    raise EvidenceCaptureError("prior Codex projection object binding differs")
            reusable[path_digest] = CodexProjection(
                record=record,
                staged=None,
                identity=identity,
                source=dict(source),
                disposition=disposition,
                reason=source_event["disposition"]["reason"],
                raw_source_sha256=str(item.get("raw_source_sha256")),
                uncompressed_sha256=item.get("uncompressed_sha256"),
                uncompressed_bytes=item.get("uncompressed_bytes"),
                skipped_record_types=dict(item.get("skipped_record_types") or {}),
                retained_records=int(item.get("retained_records") or 0),
                object_sha256=object_sha256,
                object_bytes=object_bytes,
                reused=True,
            )
        if wanted_paths <= considered_paths:
            break
    return reusable


def capture_codex_thread_closure(
    store: EvidenceStore,
    *,
    thread_id: str,
    session_roots: Sequence[Path],
    trigger: str,
    clone_function: Callable[[Path, Path], None] | None = None,
    filesystem_type_function: Callable[[Path], str] | None = None,
    progress_function: Callable[[Mapping[str, object]], None] | None = None,
) -> int:
    """Capture a user-visible projection for a target and its child agents.

    The raw rollout files are never installed in the store.  Hidden reasoning,
    compacted context and system/developer instruction bodies are excluded.
    """

    if not thread_id or not session_roots:
        raise EvidenceCaptureError("Codex closure needs a thread id and explicit session roots")
    collection_start = utc_now()
    progress_started = time.monotonic()

    def report_progress(
        stage: str,
        *,
        completed_files: int,
        total_files: int,
        completed_source_bytes: int,
        total_source_bytes: int,
        staged_projection_bytes: int,
        reused_files: int,
    ) -> None:
        if progress_function is None:
            return
        progress_function(
            {
                "stage": stage,
                "completed_files": completed_files,
                "total_files": total_files,
                "completed_source_bytes": completed_source_bytes,
                "total_source_bytes": total_source_bytes,
                "staged_projection_bytes": staged_projection_bytes,
                "reused_files": reused_files,
                "elapsed_seconds": round(time.monotonic() - progress_started, 3),
            }
        )

    for root in session_roots:
        if _paths_have_ancestry_overlap(root, store.root):
            raise EvidenceCaptureError("Codex session root and private store paths overlap")
    inventory = _iter_explicit_codex_records(session_roots)
    selected = _select_codex_thread_closure(inventory, thread_id)
    _require_unique_codex_thread_identities(selected)
    _require_acyclic_codex_thread_graph(selected)
    session_lineages = _codex_session_lineages(selected)
    session_metadata = {
        record.thread_id: (record.session_id, record.parent_thread_id)
        for record in selected
    }
    total_files = len(selected)
    total_source_bytes = sum(record.metadata.st_size for record in selected)
    report_progress(
        "inventory-complete",
        completed_files=0,
        total_files=total_files,
        completed_source_bytes=0,
        total_source_bytes=total_source_bytes,
        staged_projection_bytes=0,
        reused_files=0,
    )
    report_progress(
        "reuse-validation-start",
        completed_files=0,
        total_files=total_files,
        completed_source_bytes=0,
        total_source_bytes=total_source_bytes,
        staged_projection_bytes=0,
        reused_files=0,
    )
    reusable = _reusable_codex_projections(store, selected)
    reusable_paths = set(reusable)
    reused_source_bytes = sum(
        record.metadata.st_size
        for record in selected
        if sha256_bytes(os.fsencode(str(record.path.resolve(strict=True))))
        in reusable_paths
    )
    report_progress(
        "reuse-validation-complete",
        completed_files=len(reusable),
        total_files=total_files,
        completed_source_bytes=reused_source_bytes,
        total_source_bytes=total_source_bytes,
        staged_projection_bytes=0,
        reused_files=len(reusable),
    )
    projections: list[CodexProjection] = []
    staged_projection_bytes = 0
    completed_files = 0
    completed_source_bytes = 0
    reused_files = 0
    last_progress_files = 0
    last_progress_at = time.monotonic()
    try:
        for record in selected:
            path_digest = sha256_bytes(
                os.fsencode(str(record.path.resolve(strict=True)))
            )
            if path_digest in reusable:
                projections.append(reusable[path_digest])
                reused_files += 1
            else:
                remaining_projection_bytes = (
                    store.max_capture_bytes
                    - store.captured_bytes
                    - staged_projection_bytes
                    - MAX_METADATA_BYTES
                )
                if remaining_projection_bytes < 1:
                    raise EvidenceCaptureError(
                        "Codex closure exceeds the per-invocation byte boundary"
                    )
                if shutil.disk_usage(store.root).free < MIN_STORE_FREE_BYTES:
                    raise EvidenceCaptureError(
                        "private store has less than the required free-space reserve"
                    )
                transient = create_transient_apfs_clone(
                    record.path,
                    store.incoming,
                    clone_function=clone_function,
                    filesystem_type_function=filesystem_type_function,
                    expected_source_metadata=record.metadata,
                )
                try:
                    _verify_cloned_codex_session_record(transient.descriptor, record)
                    projection = stage_codex_user_visible_projection(
                        record,
                        store.incoming,
                        allowed_session_thread_ids=session_lineages[record.thread_id],
                        session_lineage_metadata=session_metadata,
                        read_descriptor=transient.descriptor,
                        provenance_stat_before=transient.source_stat_before,
                        provenance_stat_after=transient.source_stat_after,
                        source_changed_after_snapshot=(
                            transient.source_changed_after_snapshot
                        ),
                        max_projection_bytes=min(
                            remaining_projection_bytes,
                            MAX_OBJECT_BYTES,
                        ),
                    )
                    if (
                        projection.staged is not None
                        and projection.staged.bytes > remaining_projection_bytes
                    ):
                        projection.staged.path.unlink(missing_ok=True)
                        raise EvidenceCaptureError(
                            "Codex closure exceeds the per-invocation byte boundary"
                        )
                    projections.append(projection)
                    if projection.staged is not None:
                        staged_projection_bytes += projection.staged.bytes
                finally:
                    os.close(transient.descriptor)

            completed_files += 1
            completed_source_bytes += record.metadata.st_size
            progress_now = time.monotonic()
            if (
                completed_files == total_files
                or completed_files - last_progress_files >= 25
                or progress_now - last_progress_at >= 30
            ):
                report_progress(
                    "projection-progress",
                    completed_files=completed_files,
                    total_files=total_files,
                    completed_source_bytes=completed_source_bytes,
                    total_source_bytes=total_source_bytes,
                    staged_projection_bytes=staged_projection_bytes,
                    reused_files=reused_files,
                )
                last_progress_files = completed_files
                last_progress_at = progress_now

        report_progress(
            "final-topology-start",
            completed_files=completed_files,
            total_files=total_files,
            completed_source_bytes=completed_source_bytes,
            total_source_bytes=total_source_bytes,
            staged_projection_bytes=staged_projection_bytes,
            reused_files=reused_files,
        )
        final_inventory = _iter_explicit_codex_records(session_roots)
        final_selected = _select_codex_thread_closure(final_inventory, thread_id)
        _require_unique_codex_thread_identities(final_selected)
        _require_acyclic_codex_thread_graph(final_selected)
        projections_by_path = {
            sha256_bytes(os.fsencode(str(item.record.path.resolve(strict=True)))): item
            for item in projections
        }
        final_by_path = {
            sha256_bytes(os.fsencode(str(item.path.resolve(strict=True)))): item
            for item in final_selected
        }
        if set(final_by_path) != set(projections_by_path):
            raise EvidenceCaptureError("Codex thread closure topology changed during capture")
        final_observations: dict[str, tuple[dict[str, int], bool]] = {}
        for path_digest, final_record in final_by_path.items():
            projection = projections_by_path[path_digest]
            if (
                final_record.thread_id != projection.record.thread_id
                or final_record.session_id != projection.record.session_id
                or final_record.parent_thread_id != projection.record.parent_thread_id
            ):
                raise EvidenceCaptureError("Codex thread closure changed during capture")
            if _source_identity_signature(final_record.metadata) != _source_identity_signature(
                projection.record.metadata
            ):
                raise EvidenceCaptureError("Codex thread source identity changed during capture")
            snapshot_stat = projection.source["source_stat_before"]
            if (
                not isinstance(snapshot_stat, dict)
                or final_record.metadata.st_size < snapshot_stat["bytes"]
            ):
                raise EvidenceCaptureError("Codex thread source was truncated during capture")
            source_stat_after = projection.source["source_stat_after"]
            if not isinstance(source_stat_after, dict):
                raise EvidenceCaptureError("Codex projection lacks post-snapshot stat evidence")
            final_stat = _recorded_source_stat(final_record.metadata)
            final_observations[path_digest] = (
                final_stat,
                source_stat_after != final_stat,
            )
        final_projection_bytes = sum(
            projection.staged.bytes
            for projection in projections
            if projection.staged is not None
        )
        if (
            store.captured_bytes
            + final_projection_bytes
            + MAX_METADATA_BYTES
            > store.max_capture_bytes
        ):
            raise EvidenceCaptureError(
                "Codex closure exceeds the per-invocation byte boundary"
            )
        report_progress(
            "final-topology-complete",
            completed_files=completed_files,
            total_files=total_files,
            completed_source_bytes=completed_source_bytes,
            total_source_bytes=total_source_bytes,
            staged_projection_bytes=staged_projection_bytes,
            reused_files=reused_files,
        )
    except Exception:
        for projection in projections:
            if projection.staged is not None:
                projection.staged.path.unlink(missing_ok=True)
        raise

    manifest_files: list[dict[str, object]] = []
    aggregate_skipped: dict[str, int] = {}
    for projection in projections:
        path_digest = sha256_bytes(
            os.fsencode(str(projection.record.path.resolve(strict=True)))
        )
        for skipped_type, count in projection.skipped_record_types.items():
            aggregate_skipped[skipped_type] = aggregate_skipped.get(skipped_type, 0) + count
        manifest_files.append(
            {
                "thread_id": projection.record.thread_id,
                "session_id": projection.record.session_id,
                "parent_thread_id": projection.record.parent_thread_id,
                "source_path_sha256": path_digest,
                "source_identity": projection.identity,
                "source_identity_sha256": source_identity_sha256(projection.identity),
                "raw_source_sha256": projection.raw_source_sha256,
                "disposition": projection.disposition,
                "reason": projection.reason,
                "object_sha256": (
                    projection.staged.sha256
                    if projection.staged is not None
                    else projection.object_sha256
                ),
                "object_bytes": (
                    projection.staged.bytes
                    if projection.staged is not None
                    else projection.object_bytes
                ),
                "uncompressed_sha256": projection.uncompressed_sha256,
                "uncompressed_bytes": projection.uncompressed_bytes,
                "retained_records": projection.retained_records,
                "skipped_record_types": projection.skipped_record_types,
                "redaction_categories": projection.source["redaction_categories"],
                "redaction_count": projection.source["redaction_count"],
                "source_stat_final_observation": final_observations[path_digest][0],
                "source_changed_by_final_observation": final_observations[path_digest][1],
            }
        )
    generation_material = {
        "schema": CODEX_GENERATION_SCHEMA,
        "thread_id": thread_id,
        "selection_rule": "target-and-transitive-descendants-by-parent-thread-id",
        "files": manifest_files,
        "boundaries": BOUNDARIES,
    }
    generation = sha256_bytes(canonical_json(generation_material))
    collection_end = utc_now()
    window: dict[str, object] = {
        "start_utc": format_time(collection_start),
        "end_utc": format_time(collection_end),
        "selected_files": len(selected),
        "selection_rule": "target-and-transitive-descendants-by-parent-thread-id",
    }

    manifest = {
        **generation_material,
        "collection_generation_sha256": generation,
        "collection_window": window,
        "selected_file_count": len(selected),
        "aggregate_skipped_record_types": dict(sorted(aggregate_skipped.items())),
    }
    manifest_identity = f"codex-thread-closure:generation:{generation}:manifest"
    manifest_staged: StagedObject | None = None
    manifest_source: dict[str, object] | None = None
    manifest_reused = store.already_captured(manifest_identity)
    if not manifest_reused:
        manifest_raw = canonical_json(manifest, pretty=True)
        manifest_staged = stage_bytes(
            manifest_raw, store.incoming, max_bytes=MAX_METADATA_BYTES
        )
        try:
            _scan_secret_text(manifest_staged.path)
        except Exception:
            manifest_staged.path.unlink(missing_ok=True)
            raise
        manifest_source = _source_value(
            kind="codex-thread-closure-generation-manifest",
            identity=manifest_identity,
            label=f"Codex thread closure generation {generation}",
            occurred_at_utc=None,
            expires_at_utc=None,
            expiry_basis="unknown",
            commit_sha=None,
            tree_sha=None,
            redaction_mode="generated-from-owner-only-redacted-projections",
            snapshot_method="derived-generation-manifest",
            source_stat_before=None,
            source_stat_after=None,
            source_changed_after_snapshot=None,
            collection_generation_sha256=generation,
            collection_window=window,
            redaction_categories=[],
            redaction_count=0,
        )
    try:
        captures: list[StagedCapture | ObjectlessCapture] = []
        for projection in projections:
            if projection.reused:
                store.no_op += 1
            elif projection.staged is not None:
                captures.append(
                    StagedCapture(
                        staged=projection.staged,
                        trigger=trigger,
                        repository=None,
                        source=projection.source,
                        role="codex-user-visible-projection-gzip",
                        media_type="application/gzip",
                        opaque=False,
                        secret_scan=(
                            "fixed-length-high-confidence-redaction-completed"
                        ),
                        secret_scan_performed=True,
                        sensitivity="owner-only-redacted",
                    )
                )
            else:
                reason = (
                    projection.reason
                    or "unredactable-secret-category:unknown"
                )
                existing = store.identities.get(projection.identity)
                if existing is not None:
                    candidate = {
                        "source": projection.source,
                        "objects": [],
                        "disposition": {
                            "status": "excluded",
                            "reason": reason,
                        },
                        "repository": None,
                    }
                    if _event_fingerprint(existing) != _event_fingerprint(candidate):
                        raise EvidenceCaptureError(
                            "immutable source identity has conflicting evidence"
                        )
                    store.no_op += 1
                    reused_files += 1
                    continue
                captures.append(
                    ObjectlessCapture(
                        trigger=trigger,
                        repository=None,
                        source=projection.source,
                        status_value="excluded",
                        reason=reason,
                    )
                )
        if manifest_staged is not None and manifest_source is not None:
            captures.append(
                StagedCapture(
                    staged=manifest_staged,
                    trigger=trigger,
                    repository=None,
                    source=manifest_source,
                    role="codex-thread-closure-generation-manifest",
                    media_type="application/json",
                    opaque=False,
                    secret_scan="high-confidence-text-scan-passed",
                    secret_scan_performed=True,
                    sensitivity="owner-only-redacted",
                )
            )
        if manifest_reused and captures:
            raise EvidenceCaptureError(
                "prior Codex generation manifest has an incomplete projection set"
            )
        report_progress(
            "commit-start",
            completed_files=completed_files,
            total_files=total_files,
            completed_source_bytes=completed_source_bytes,
            total_source_bytes=total_source_bytes,
            staged_projection_bytes=staged_projection_bytes,
            reused_files=reused_files,
        )
        if captures:
            store.commit_capture_batch(captures)
        report_progress(
            "commit-complete",
            completed_files=completed_files,
            total_files=total_files,
            completed_source_bytes=completed_source_bytes,
            total_source_bytes=total_source_bytes,
            staged_projection_bytes=staged_projection_bytes,
            reused_files=reused_files,
        )
    except Exception:
        if not (store.root / PENDING_EVENT_NAME).exists():
            for projection in projections:
                if projection.staged is not None:
                    projection.staged.path.unlink(missing_ok=True)
            if manifest_staged is not None:
                manifest_staged.path.unlink(missing_ok=True)
        raise
    return len(selected)


class GhClient:
    """Small `gh api` adapter which never invokes a shell."""

    def __init__(self, executable: str = "gh") -> None:
        self.executable = executable
        self.last_response_bytes = 0

    def json(
        self,
        endpoint: str,
        *,
        paginate: bool = False,
        timeout_seconds: float | None = None,
    ) -> Any:
        self.last_response_bytes = 0
        arguments = [self.executable, "api"]
        if paginate:
            arguments.extend(("--paginate", "--slurp"))
        arguments.append(endpoint)
        process = subprocess.Popen(
            arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        if process.stdout is None:
            process.kill()
            process.wait()
            raise EvidenceCaptureError("GitHub metadata request did not expose stdout")
        selector = selectors.DefaultSelector()
        deadline = time.monotonic() + (
            GITHUB_METADATA_TIMEOUT_SECONDS
            if timeout_seconds is None
            else min(GITHUB_METADATA_TIMEOUT_SECONDS, max(0.001, timeout_seconds))
        )
        output = bytearray()
        try:
            os.set_blocking(process.stdout.fileno(), False)
            selector.register(process.stdout, selectors.EVENT_READ)
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise GitHubProviderUnavailableError(
                        "GitHub metadata request timed out"
                    )
                ready = selector.select(timeout=min(1.0, remaining))
                if not ready:
                    if process.poll() is None:
                        continue
                    try:
                        chunk = os.read(process.stdout.fileno(), 1024 * 1024)
                    except BlockingIOError:
                        continue
                else:
                    try:
                        chunk = os.read(process.stdout.fileno(), 1024 * 1024)
                    except BlockingIOError:
                        continue
                if not chunk:
                    break
                output.extend(chunk)
                if len(output) > MAX_METADATA_BYTES:
                    raise EvidenceCaptureError("GitHub metadata exceeds the byte boundary")
            try:
                return_code = process.wait(timeout=max(0.1, deadline - time.monotonic()))
            except subprocess.TimeoutExpired as error:
                raise GitHubProviderUnavailableError(
                    "GitHub metadata request timed out"
                ) from error
            if return_code != 0:
                raise GitHubProviderUnavailableError("GitHub metadata request failed")
        except Exception:
            if process.poll() is None:
                process.kill()
                process.wait()
            raise
        finally:
            self.last_response_bytes = len(output)
            selector.close()
            process.stdout.close()
        return parse_json(bytes(output), "GitHub response")

    def download_to(
        self,
        endpoint: str,
        incoming: Path,
        *,
        max_bytes: int,
        byte_observer: Callable[[int], None] | None = None,
        timeout_seconds: float | None = None,
    ) -> StagedObject:
        temporary = incoming / f"{uuid.uuid4().hex}.download"
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        process = subprocess.Popen(
            [self.executable, "api", endpoint],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        if process.stdout is None:
            process.kill()
            os.close(descriptor)
            temporary.unlink(missing_ok=True)
            raise EvidenceCaptureError("GitHub download did not expose stdout")
        digest = hashlib.sha256()
        total = 0
        selector = selectors.DefaultSelector()
        deadline = time.monotonic() + (
            GITHUB_DOWNLOAD_TIMEOUT_SECONDS
            if timeout_seconds is None
            else min(GITHUB_DOWNLOAD_TIMEOUT_SECONDS, max(0.001, timeout_seconds))
        )
        try:
            os.set_blocking(process.stdout.fileno(), False)
            selector.register(process.stdout, selectors.EVENT_READ)
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise GitHubProviderUnavailableError("GitHub download timed out")
                ready = selector.select(timeout=min(1.0, remaining))
                if not ready:
                    if process.poll() is None:
                        continue
                    try:
                        chunk = os.read(process.stdout.fileno(), 1024 * 1024)
                    except BlockingIOError:
                        continue
                    if chunk:
                        pass
                    else:
                        break
                else:
                    try:
                        chunk = os.read(process.stdout.fileno(), 1024 * 1024)
                    except BlockingIOError:
                        continue
                if not chunk:
                    break
                if byte_observer is not None:
                    byte_observer(len(chunk))
                total += len(chunk)
                if total > max_bytes:
                    process.kill()
                    process.wait()
                    raise EvidenceCaptureError("GitHub download exceeds the byte boundary")
                digest.update(chunk)
                view = memoryview(chunk)
                while view:
                    written = os.write(descriptor, view)
                    view = view[written:]
            try:
                return_code = process.wait(timeout=max(0.1, deadline - time.monotonic()))
            except subprocess.TimeoutExpired as error:
                raise GitHubProviderUnavailableError("GitHub download timed out") from error
            if return_code != 0:
                # Deliberately do not retain stderr: it can contain signed redirect URLs.
                raise GitHubProviderUnavailableError("GitHub download failed")
            os.fsync(descriptor)
        except Exception:
            if process.poll() is None:
                process.kill()
                process.wait()
            os.close(descriptor)
            temporary.unlink(missing_ok=True)
            raise
        finally:
            selector.close()
            process.stdout.close()
        os.close(descriptor)
        return StagedObject(temporary, digest.hexdigest(), total)


def _download_to_stage(
    client: Any,
    endpoint: str,
    incoming: Path,
    *,
    max_bytes: int,
    store: EvidenceStore,
) -> StagedObject:
    remaining_seconds = store.begin_github_api_request()
    effective_max = min(max_bytes, store.remaining_transfer_bytes)
    if effective_max < 1:
        raise EvidenceCaptureError("GitHub transfer byte boundary is exhausted")
    store.require_staging_capacity(effective_max)
    if hasattr(client, "download_to"):
        if isinstance(client, GhClient):
            return client.download_to(
                endpoint,
                incoming,
                max_bytes=effective_max,
                byte_observer=store.note_transfer,
                timeout_seconds=remaining_seconds,
            )
        return client.download_to(
            endpoint,
            incoming,
            max_bytes=effective_max,
            byte_observer=store.note_transfer,
        )
    # The compatibility seam exists only for bounded synthetic test clients.
    raw = client.download(endpoint, max_bytes=effective_max)
    store.note_transfer(len(raw))
    return stage_bytes(raw, incoming, max_bytes=effective_max)


def _github_json(
    store: EvidenceStore,
    client: Any,
    endpoint: str,
    *,
    paginate: bool = False,
    retry_sleep: Callable[[float], None] = time.sleep,
) -> Any:
    """Fetch bounded JSON, retrying only transient transport failures from `GhClient`."""

    missing = object()

    def note_response_bytes(value: Any = missing) -> None:
        observed_bytes = getattr(client, "last_response_bytes", None)
        if not isinstance(observed_bytes, int) or isinstance(observed_bytes, bool):
            observed_bytes = 0 if value is missing else len(canonical_json(value))
        store.note_github_metadata(observed_bytes)

    if not isinstance(client, GhClient):
        store.begin_github_api_request()
        value = client.json(endpoint, paginate=paginate)
        note_response_bytes(value)
        return value

    for attempt in range(1, GITHUB_METADATA_MAX_ATTEMPTS + 1):
        remaining_seconds = store.begin_github_api_request()
        try:
            value = client.json(
                endpoint,
                paginate=paginate,
                timeout_seconds=remaining_seconds,
            )
        except GitHubProviderUnavailableError:
            note_response_bytes()
            if attempt >= GITHUB_METADATA_MAX_ATTEMPTS:
                raise
            if store.github_api_invocations >= MAX_GITHUB_API_INVOCATIONS:
                continue
            remaining_after_attempt = MAX_GITHUB_CAPTURE_SECONDS - (
                time.monotonic() - store.github_capture_started
            )
            delay = min(
                GITHUB_METADATA_RETRY_DELAY_SECONDS,
                max(0.0, remaining_after_attempt),
            )
            if delay > 0:
                retry_sleep(delay)
        except Exception:
            note_response_bytes()
            raise
        else:
            note_response_bytes(value)
            return value
    raise EvidenceCaptureError("GitHub metadata retry loop ended unexpectedly")


def _flatten_pages(value: Any, key: str) -> list[dict[str, Any]]:
    pages = value if isinstance(value, list) else [value]
    items: list[dict[str, Any]] = []
    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get(key), list):
            raise EvidenceCaptureError(f"GitHub response does not contain {key}")
        for item in page[key]:
            if not isinstance(item, dict):
                raise EvidenceCaptureError(f"GitHub {key} item is not an object")
            items.append(item)
    return items


def _validate_github_artifact_rows(
    artifacts: list[dict[str, Any]],
    *,
    run_id: int,
    repository_id: int,
    head_sha: str | None,
    occurred_at: str,
) -> list[dict[str, Any]]:
    """Validate a complete provider snapshot before it enters the journal."""

    if head_sha is None:
        raise EvidenceCaptureError("GitHub artefact run commit identity is unavailable")
    seen_ids: set[int] = set()
    for artifact in artifacts:
        artifact_id = artifact.get("id")
        size = artifact.get("size_in_bytes")
        workflow_run = artifact.get("workflow_run")
        provider_digest = artifact.get("digest")
        expired = artifact.get("expired")
        expires_at = artifact.get("expires_at")
        created_at = artifact.get("created_at") or occurred_at
        if (
            not isinstance(artifact_id, int)
            or isinstance(artifact_id, bool)
            or artifact_id <= 0
        ):
            raise EvidenceCaptureError("GitHub artefact id is invalid")
        if artifact_id in seen_ids:
            raise EvidenceCaptureError("GitHub artefact id is duplicated")
        seen_ids.add(artifact_id)
        if (
            not isinstance(size, int)
            or isinstance(size, bool)
            or size < 0
        ):
            raise EvidenceCaptureError("GitHub artefact size is invalid")
        if (
            not isinstance(workflow_run, Mapping)
            or not isinstance(workflow_run.get("id"), int)
            or isinstance(workflow_run.get("id"), bool)
            or workflow_run.get("id") != run_id
            or not isinstance(workflow_run.get("repository_id"), int)
            or isinstance(workflow_run.get("repository_id"), bool)
            or workflow_run.get("repository_id") != repository_id
            or not isinstance(workflow_run.get("head_sha"), str)
            or str(workflow_run.get("head_sha")).lower() != head_sha
        ):
            raise EvidenceCaptureError("GitHub artefact workflow identity is inconsistent")
        if provider_digest is not None and (
            not isinstance(provider_digest, str)
            or re.fullmatch(r"sha256:[0-9a-fA-F]{64}", provider_digest) is None
        ):
            raise EvidenceCaptureError("GitHub artefact digest is invalid")
        if not isinstance(expired, bool):
            raise EvidenceCaptureError("GitHub artefact expiry marker is invalid")
        if expires_at is not None:
            if not isinstance(expires_at, str):
                raise EvidenceCaptureError("GitHub artefact expiry time is invalid")
            parse_time(expires_at, "GitHub artefact expiry")
        if not isinstance(created_at, str):
            raise EvidenceCaptureError("GitHub artefact creation time is invalid")
        parse_time(created_at, "GitHub artefact creation time")
    return sorted(artifacts, key=lambda item: int(item["id"]))


def _github_source(
    kind: str,
    identity: str,
    label: str,
    *,
    occurred_at: str | None,
    expires_at: str | None,
    expiry_basis: str,
    commit_sha: str | None,
    tree_sha: str | None = None,
    collection_generation_sha256: str | None = None,
) -> dict[str, object]:
    if occurred_at is not None:
        occurred_at = format_time(parse_time(occurred_at, "GitHub source time"))
    if expires_at is not None:
        expires_at = format_time(parse_time(expires_at, "GitHub expiry"))
    return _source_value(
        kind=kind,
        identity=identity,
        label=label,
        occurred_at_utc=occurred_at,
        expires_at_utc=expires_at,
        expiry_basis=expiry_basis,
        commit_sha=commit_sha,
        tree_sha=tree_sha,
        redaction_mode="none",
        snapshot_method="github-api-download",
        source_stat_before=None,
        source_stat_after=None,
        source_changed_after_snapshot=None,
        collection_generation_sha256=collection_generation_sha256,
        collection_window=None,
        redaction_categories=[],
        redaction_count=0,
    )


def _github_run_tree_sha(run: Mapping[str, object]) -> str | None:
    head_commit = run.get("head_commit")
    if head_commit is None:
        raise EvidenceCaptureError("GitHub run head commit identity is unavailable")
    if not isinstance(head_commit, Mapping):
        raise EvidenceCaptureError("GitHub run head commit is not an object")
    head_sha = run.get("head_sha")
    commit_id = head_commit.get("id")
    if (
        not isinstance(head_sha, str)
        or re.fullmatch(r"[0-9a-fA-F]{40}", head_sha) is None
        or not isinstance(commit_id, str)
        or re.fullmatch(r"[0-9a-fA-F]{40}", commit_id) is None
        or commit_id.lower() != head_sha.lower()
    ):
        raise EvidenceCaptureError("GitHub run head commit identity is inconsistent")
    tree_sha = head_commit.get("tree_id")
    if tree_sha is None:
        raise EvidenceCaptureError("GitHub run tree identity is unavailable")
    if not isinstance(tree_sha, str) or re.fullmatch(r"[0-9a-fA-F]{40}", tree_sha) is None:
        raise EvidenceCaptureError("GitHub run tree identity is invalid")
    return tree_sha.lower()


def _github_observation_source(
    source: Mapping[str, object],
    *,
    outcome: str,
) -> dict[str, object]:
    """Version a bounded observation without occupying the canonical source identity.

    A transport failure or policy skip is evidence about one capture attempt, not
    immutable proof that the provider object can never be obtained.  Keeping the
    canonical identity free allows a later unattended sweep to preserve the real
    object when it becomes available.
    """

    if not TRIGGER_PATTERN.fullmatch(outcome):
        raise EvidenceCaptureError("GitHub observation outcome is invalid")
    observed = dict(source)
    source_digest = sha256_bytes(canonical_json(source))
    identity = (
        f"{source['identity']}:observation:{outcome}:"
        f"source-sha256:{source_digest}"
    )
    observed["identity"] = identity
    observed["identity_sha256"] = source_identity_sha256(identity)
    return observed


def _capture_github_json(
    store: EvidenceStore,
    value: object,
    *,
    trigger: str,
    repository: str,
    source: dict[str, object],
    role: str,
) -> bool:
    raw = canonical_json(value, pretty=True)
    store.require_staging_capacity(len(raw))
    staged = stage_bytes(raw, store.incoming, max_bytes=MAX_METADATA_BYTES)
    try:
        _scan_secret_text(staged.path)
    except SecretDetectedError as error:
        staged.path.unlink(missing_ok=True)
        store.record_without_object(
            trigger=trigger,
            repository=repository,
            source=source,
            status_value="excluded",
            reason=f"secret-category:{error.category}",
        )
        return False
    store.commit_staged(
        staged,
        trigger=trigger,
        repository=repository,
        source=source,
        role=role,
        media_type="application/json",
        opaque=False,
        secret_scan="high-confidence-text-scan-passed",
        secret_scan_performed=True,
        sensitivity="owner-only-raw",
    )
    return True


def _capture_github_zip(
    store: EvidenceStore,
    staged: StagedObject,
    *,
    trigger: str,
    repository: str,
    source: dict[str, object],
    role: str,
) -> None:
    try:
        _scan_zip_archive(staged.path)
    except SecretDetectedError as error:
        staged.path.unlink(missing_ok=True)
        store.record_without_object(
            trigger=trigger,
            repository=repository,
            source=source,
            status_value="excluded",
            reason=f"secret-category:{error.category}",
        )
        return
    except EvidenceCaptureError:
        staged.path.unlink(missing_ok=True)
        store.record_without_object(
            trigger=trigger,
            repository=repository,
            source=_github_observation_source(
                source,
                outcome="archive-validation-failed",
            ),
            status_value="unavailable",
            reason="github-archive-validation-failed",
        )
        return
    store.commit_staged(
        staged,
        trigger=trigger,
        repository=repository,
        source=source,
        role=role,
        media_type="application/zip",
        opaque=True,
        secret_scan="zip-entry-high-confidence-scan-passed",
        secret_scan_performed=True,
        sensitivity="owner-only-raw",
    )


def _capture_github_repository_snapshot(
    store: EvidenceStore,
    *,
    repository: str,
    trigger: str,
    client: Any,
) -> str:
    """Capture a closed repository identity snapshot and return its stable prefix."""

    value = _github_json(store, client, f"repos/{repository}")
    if not isinstance(value, dict) or not isinstance(value.get("id"), int):
        raise EvidenceCaptureError("GitHub repository response has no numeric id")
    full_name = value.get("full_name")
    if not isinstance(full_name, str) or not REPOSITORY_PATTERN.fullmatch(full_name):
        raise EvidenceCaptureError("GitHub repository response has no canonical full name")
    if full_name != repository:
        raise EvidenceCaptureError("GitHub repository identity differs from the request")
    selected = {
        key: value[key]
        for key in (
            "id",
            "node_id",
            "full_name",
            "html_url",
            "private",
            "visibility",
            "archived",
            "default_branch",
            "created_at",
            "updated_at",
            "pushed_at",
        )
        if key in value
    }
    raw = canonical_json(selected, pretty=True)
    digest = sha256_bytes(raw)
    prefix = f"github:repository:{value['id']}"
    source = _github_source(
        "github-repository-identity-snapshot",
        f"{prefix}:metadata:snapshot:{digest}",
        f"GitHub repository {full_name}",
        occurred_at=None,
        expires_at=None,
        expiry_basis="unknown",
        commit_sha=None,
    )
    captured = _capture_github_json(
        store,
        selected,
        trigger=trigger,
        repository=repository,
        source=source,
        role="github-repository-identity",
    )
    if not captured:
        raise EvidenceCaptureError("GitHub repository identity was excluded by capture policy")
    return prefix


def capture_github(
    store: EvidenceStore,
    *,
    repository: str,
    since: datetime,
    trigger: str,
    download_run_logs: bool,
    artifact_max_bytes: int,
    client: GhClient,
) -> None:
    discovery_since = since.astimezone(timezone.utc) - OVERLAP
    repository_prefix = _capture_github_repository_snapshot(
        store,
        repository=repository,
        trigger=trigger,
        client=client,
    )
    retention_lookup_source = _github_source(
        "github-actions-retention-policy-snapshot",
        f"{repository_prefix}:actions-retention",
        "GitHub Actions artefact and log retention policy lookup",
        occurred_at=None,
        expires_at=None,
        expiry_basis="unknown",
        commit_sha=None,
    )
    try:
        retention = _github_json(
            store,
            client,
            f"repos/{repository}/actions/permissions/artifact-and-log-retention"
        )
    except GitHubProviderUnavailableError:
        retention = None
        store.record_without_object(
            trigger=trigger,
            repository=repository,
            source=_github_observation_source(
                retention_lookup_source,
                outcome="lookup-unavailable",
            ),
            status_value="unavailable",
            reason="github-metadata-unavailable",
        )
    if retention is not None:
        if (
            not isinstance(retention, dict)
            or not isinstance(retention.get("days"), int)
            or isinstance(retention.get("days"), bool)
            or retention["days"] <= 0
            or retention["days"] > GITHUB_MAX_RETENTION_DAYS
        ):
            raise EvidenceCaptureError("GitHub retention policy is invalid")
        retention_raw = canonical_json(retention, pretty=True)
        retention_digest = sha256_bytes(retention_raw)
        retention_source = _github_source(
            "github-actions-retention-policy-snapshot",
            f"{repository_prefix}:actions-retention:snapshot:{retention_digest}",
            "GitHub Actions artefact and log retention policy",
            occurred_at=None,
            expires_at=None,
            expiry_basis="unknown",
            commit_sha=None,
        )
        _capture_github_json(
            store,
            retention,
            trigger=trigger,
            repository=repository,
            source=retention_source,
            role="github-actions-retention-policy",
        )
    creation_floor = discovery_since - GITHUB_MAX_WORKFLOW_RUN_DURATION
    discovery_filter = format_time(creation_floor).replace(".000Z", "Z")
    encoded_created = quote(f">={discovery_filter}", safe="")
    response = _github_json(
        store,
        client,
        f"repos/{repository}/actions/runs?status=completed&created={encoded_created}&per_page=100",
        paginate=True,
    )
    run_pages = response if isinstance(response, list) else [response]
    if not run_pages or any(
        not isinstance(page, dict)
        or not isinstance(page.get("total_count"), int)
        or isinstance(page.get("total_count"), bool)
        for page in run_pages
    ):
        raise EvidenceCaptureError("GitHub workflow-run discovery count is unavailable")
    total_counts = {int(page["total_count"]) for page in run_pages}
    if len(total_counts) != 1:
        raise EvidenceCaptureError("GitHub workflow-run discovery count changed while paging")
    runs = _flatten_pages(response, "workflow_runs")
    if next(iter(total_counts)) > len(runs):
        raise EvidenceCaptureError("GitHub workflow-run discovery is truncated")
    selected: list[dict[str, Any]] = []
    for run in runs:
        if run.get("status") != "completed":
            continue
        source_time = run.get("updated_at") or run.get("run_started_at")
        if not isinstance(source_time, str):
            raise EvidenceCaptureError("completed GitHub run has no source time")
        if parse_time(source_time, "GitHub run time") < discovery_since:
            continue
        selected.append(run)
    expanded: list[dict[str, Any]] = []
    blocked_artifact_runs: set[int] = set()
    for run in selected:
        run_id = int(run["id"])
        latest_attempt = int(run.get("run_attempt", 1))
        if latest_attempt < 1:
            raise EvidenceCaptureError("completed GitHub run has an invalid attempt number")
        for attempt_number in range(1, latest_attempt):
            previous = _github_json(
                store,
                client,
                f"repos/{repository}/actions/runs/{run_id}/attempts/{attempt_number}"
            )
            if (
                not isinstance(previous, dict)
                or int(previous.get("id", -1)) != run_id
                or int(previous.get("run_attempt", -1)) != attempt_number
                or previous.get("status") != "completed"
            ):
                raise EvidenceCaptureError("GitHub run attempt metadata is inconsistent")
            expanded.append(previous)
        expanded.append(run)
    selected = expanded
    selected.sort(key=lambda item: (int(item["id"]), int(item.get("run_attempt", 1))))

    run_bindings: dict[int, tuple[str | None, str | None]] = {}
    for run in selected:
        run_id = int(run["id"])
        head_sha = str(run.get("head_sha") or "").lower() or None
        if head_sha is not None and re.fullmatch(r"[0-9a-f]{40}", head_sha) is None:
            raise EvidenceCaptureError("GitHub run commit identity is invalid")
        tree_sha = _github_run_tree_sha(run)
        binding = (head_sha, tree_sha)
        previous_binding = run_bindings.get(run_id)
        if previous_binding is not None and previous_binding != binding:
            raise EvidenceCaptureError("GitHub run attempts have inconsistent source identities")
        run_bindings[run_id] = binding

    for run in selected:
        run_id = int(run["id"])
        attempt = int(run.get("run_attempt", 1))
        head_sha, tree_sha = run_bindings[run_id]
        occurred_at = str(run.get("run_started_at") or run.get("created_at"))
        prefix = f"{repository_prefix}:run:{run_id}:attempt:{attempt}"
        run_digest = sha256_bytes(canonical_json(run, pretty=True))
        run_source = _github_source(
            "github-actions-run-metadata",
            f"{prefix}:metadata:snapshot:{run_digest}",
            f"workflow run {run_id} attempt {attempt}",
            occurred_at=occurred_at,
            expires_at=None,
            expiry_basis="unknown",
            commit_sha=head_sha,
            tree_sha=tree_sha,
        )
        run_metadata_captured = _capture_github_json(
            store,
            run,
            trigger=trigger,
            repository=repository,
            source=run_source,
            role="github-run-metadata",
        )
        if not run_metadata_captured:
            blocked_artifact_runs.add(run_id)
            continue

        jobs_response = _github_json(
            store,
            client,
            f"repos/{repository}/actions/runs/{run_id}/attempts/{attempt}/jobs?per_page=100",
            paginate=True,
        )
        jobs = _flatten_pages(jobs_response, "jobs")
        jobs.sort(key=lambda item: int(item["id"]))
        for job in jobs:
            job_run_id = job.get("run_id")
            job_attempt = job.get("run_attempt")
            job_head_sha = job.get("head_sha")
            if (
                not isinstance(job_run_id, int)
                or isinstance(job_run_id, bool)
                or job_run_id != run_id
                or not isinstance(job_attempt, int)
                or isinstance(job_attempt, bool)
                or job_attempt != attempt
                or not isinstance(job_head_sha, str)
                or head_sha is None
                or job_head_sha.lower() != head_sha
            ):
                raise EvidenceCaptureError("GitHub job identity is inconsistent")
        jobs_value = {"jobs": jobs}
        jobs_digest = sha256_bytes(canonical_json(jobs_value, pretty=True))
        jobs_source = _github_source(
            "github-actions-run-jobs",
            f"{prefix}:jobs:snapshot:{jobs_digest}",
            f"workflow run {run_id} attempt {attempt} jobs",
            occurred_at=occurred_at,
            expires_at=None,
            expiry_basis="unknown",
            commit_sha=head_sha,
            tree_sha=tree_sha,
        )
        _capture_github_json(
            store,
            jobs_value,
            trigger=trigger,
            repository=repository,
            source=jobs_source,
            role="github-run-jobs",
        )

        if download_run_logs:
            logs_source = _github_source(
                "github-actions-run-logs",
                f"{prefix}:logs",
                f"workflow run {run_id} attempt {attempt} logs",
                occurred_at=occurred_at,
                # Repository retention settings are mutable and GitHub applies
                # changes only to newly created logs.  A current setting does
                # not attest the creation-time policy for this historical run.
                expires_at=None,
                expiry_basis="unknown",
                commit_sha=head_sha,
                tree_sha=tree_sha,
            )
            if store.already_captured(str(logs_source["identity"])):
                continue_logs = False
            else:
                continue_logs = True
            if not continue_logs:
                pass
            else:
                try:
                    staged = _download_to_stage(
                        client,
                        f"repos/{repository}/actions/runs/{run_id}/attempts/{attempt}/logs",
                        store.incoming,
                        max_bytes=MAX_LOG_BYTES,
                        store=store,
                    )
                except GitHubProviderUnavailableError:
                    store.record_without_object(
                        trigger=trigger,
                        repository=repository,
                        source=_github_observation_source(
                            logs_source,
                            outcome="download-unavailable",
                        ),
                        status_value="unavailable",
                        reason="github-download-unavailable",
                    )
                else:
                    _capture_github_zip(
                        store,
                        staged,
                        trigger=trigger,
                        repository=repository,
                        source=logs_source,
                        role="github-run-logs-archive",
                    )

    # GitHub exposes artefacts at run scope, not attempt scope. Preserve the
    # run-level snapshot exactly once, using the latest completed attempt only
    # for the run's commit/tree and occurrence-time bindings.
    artifact_runs: dict[int, dict[str, Any]] = {}
    for run in selected:
        if int(run["id"]) not in blocked_artifact_runs:
            artifact_runs[int(run["id"])] = run
    for run_id, run in sorted(artifact_runs.items()):
        head_sha, tree_sha = run_bindings[run_id]
        occurred_at = str(run.get("run_started_at") or run.get("created_at"))
        run_prefix = f"{repository_prefix}:run:{run_id}"
        repository_id = int(repository_prefix.rsplit(":", 1)[1])
        artifacts_response = _github_json(
            store,
            client,
            f"repos/{repository}/actions/runs/{run_id}/artifacts?per_page=100",
            paginate=True,
        )
        artifacts = _flatten_pages(artifacts_response, "artifacts")
        artifacts = _validate_github_artifact_rows(
            artifacts,
            run_id=run_id,
            repository_id=repository_id,
            head_sha=head_sha,
            occurred_at=occurred_at,
        )
        artifacts_value = {"artifacts": artifacts}
        artifacts_digest = sha256_bytes(canonical_json(artifacts_value, pretty=True))
        artifacts_source = _github_source(
            "github-actions-artifact-metadata",
            f"{run_prefix}:artifacts-metadata:snapshot:{artifacts_digest}",
            f"workflow run {run_id} artefact metadata",
            occurred_at=occurred_at,
            expires_at=None,
            expiry_basis="unknown",
            commit_sha=head_sha,
            tree_sha=tree_sha,
        )
        artifacts_metadata_captured = _capture_github_json(
            store,
            artifacts_value,
            trigger=trigger,
            repository=repository,
            source=artifacts_source,
            role="github-artifact-metadata",
        )
        if not artifacts_metadata_captured:
            continue
        for artifact in artifacts:
            artifact_id = int(artifact["id"])
            workflow_run = artifact.get("workflow_run")
            if not isinstance(workflow_run, Mapping):
                raise EvidenceCaptureError("GitHub artefact workflow identity is unavailable")
            artefact_run_id = workflow_run.get("id")
            artefact_repository_id = workflow_run.get("repository_id")
            artefact_head_sha = workflow_run.get("head_sha")
            if (
                not isinstance(artefact_run_id, int)
                or isinstance(artefact_run_id, bool)
                or artefact_run_id != run_id
                or not isinstance(artefact_repository_id, int)
                or isinstance(artefact_repository_id, bool)
                or artefact_repository_id != repository_id
                or not isinstance(artefact_head_sha, str)
                or head_sha is None
                or artefact_head_sha.lower() != head_sha
            ):
                raise EvidenceCaptureError("GitHub artefact workflow identity is inconsistent")
            name = str(artifact.get("name") or f"artifact-{artifact_id}")
            size_value = artifact.get("size_in_bytes")
            if (
                not isinstance(size_value, int)
                or isinstance(size_value, bool)
                or size_value < 0
            ):
                raise EvidenceCaptureError("GitHub artefact size is invalid")
            size = size_value
            expires_at = artifact.get("expires_at")
            provider_digest = artifact.get("digest")
            if provider_digest is not None and (
                not isinstance(provider_digest, str)
                or re.fullmatch(r"sha256:[0-9a-fA-F]{64}", provider_digest) is None
            ):
                raise EvidenceCaptureError("GitHub artefact digest is invalid")
            artifact_source = _github_source(
                "github-actions-artifact",
                f"{run_prefix}:artifact:{artifact_id}:zip",
                f"artefact {artifact_id}: {name}",
                occurred_at=str(artifact.get("created_at") or occurred_at),
                expires_at=str(expires_at) if expires_at else None,
                expiry_basis="provider-observed" if expires_at else "unknown",
                commit_sha=head_sha,
                tree_sha=tree_sha,
                collection_generation_sha256=artifacts_digest,
            )
            if store.already_captured(str(artifact_source["identity"])):
                continue
            expired = artifact.get("expired")
            if not isinstance(expired, bool):
                raise EvidenceCaptureError("GitHub artefact expiry marker is invalid")
            if expired:
                store.record_without_object(
                    trigger=trigger,
                    repository=repository,
                    source=_github_observation_source(
                        artifact_source,
                        outcome="expired",
                    ),
                    status_value="unavailable",
                    reason="github-artifact-expired",
                )
                continue
            impact = name.startswith("ci-impact-plan-")
            if not impact and size > artifact_max_bytes:
                store.record_without_object(
                    trigger=trigger,
                    repository=repository,
                    source=_github_observation_source(
                        artifact_source,
                        outcome=f"policy-skip-max-bytes-{artifact_max_bytes}",
                    ),
                    status_value="unavailable",
                    reason="selective-large-artifact-not-captured",
                )
                continue
            hard_limit = (
                max(artifact_max_bytes, 64 * 1024 * 1024)
                if impact
                else artifact_max_bytes
            )
            try:
                staged = _download_to_stage(
                    client,
                    f"repos/{repository}/actions/artifacts/{artifact_id}/zip",
                    store.incoming,
                    max_bytes=min(hard_limit, MAX_OBJECT_BYTES),
                    store=store,
                )
            except GitHubProviderUnavailableError:
                store.record_without_object(
                    trigger=trigger,
                    repository=repository,
                    source=_github_observation_source(
                        artifact_source,
                        outcome="download-unavailable",
                    ),
                    status_value="unavailable",
                    reason="github-download-unavailable",
                )
            else:
                if staged.bytes != size:
                    staged.path.unlink(missing_ok=True)
                    store.record_without_object(
                        trigger=trigger,
                        repository=repository,
                        source=_github_observation_source(
                            artifact_source,
                            outcome="provider-size-mismatch",
                        ),
                        status_value="unavailable",
                        reason="github-artifact-provider-size-mismatch",
                    )
                    continue
                if (
                    isinstance(provider_digest, str)
                    and staged.sha256 != provider_digest.removeprefix("sha256:").lower()
                ):
                    staged.path.unlink(missing_ok=True)
                    store.record_without_object(
                        trigger=trigger,
                        repository=repository,
                        source=_github_observation_source(
                            artifact_source,
                            outcome="provider-digest-mismatch",
                        ),
                        status_value="unavailable",
                        reason="github-artifact-provider-digest-mismatch",
                    )
                    continue
                _capture_github_zip(
                    store,
                    staged,
                    trigger=trigger,
                    repository=repository,
                    source=artifact_source,
                    role="github-artifact-archive",
                )


def _flatten_github_array_pages(value: object, label: str) -> list[Mapping[str, object]]:
    if not isinstance(value, list):
        raise EvidenceCaptureError(f"GitHub {label} response is not an array")
    candidates: list[object]
    if all(isinstance(page, list) for page in value):
        candidates = [item for page in value for item in page]
    else:
        candidates = list(value)
    if not all(isinstance(item, Mapping) for item in candidates):
        raise EvidenceCaptureError(f"GitHub {label} response contains a non-object")
    return [item for item in candidates if isinstance(item, Mapping)]


def _require_github_parent_url(
    value: Mapping[str, object],
    *,
    field: str,
    expected: str,
    label: str,
) -> None:
    if value.get(field) != expected:
        raise EvidenceCaptureError(f"GitHub {label} parent identity is inconsistent")


def capture_github_discussion(
    store: EvidenceStore,
    *,
    repository: str,
    number: int,
    trigger: str,
    client: GhClient,
) -> None:
    if number < 1:
        raise EvidenceCaptureError("discussion number must be positive")
    repository_prefix = _capture_github_repository_snapshot(
        store,
        repository=repository,
        trigger=trigger,
        client=client,
    )
    issue = _github_json(store, client, f"repos/{repository}/issues/{number}")
    if not isinstance(issue, dict):
        raise EvidenceCaptureError("GitHub discussion response is not an object")
    repository_api_url = f"https://api.github.com/repos/{repository}"
    issue_api_url = f"{repository_api_url}/issues/{number}"
    pull_api_url = f"{repository_api_url}/pulls/{number}"
    if issue.get("number") != number:
        raise EvidenceCaptureError("GitHub discussion number differs from the request")
    _require_github_parent_url(
        issue,
        field="repository_url",
        expected=repository_api_url,
        label="discussion",
    )
    _require_github_parent_url(
        issue,
        field="url",
        expected=issue_api_url,
        label="discussion",
    )
    sources: list[tuple[str, object]] = [("issue-or-pull-request", issue)]
    issue_comments = _github_json(
        store,
        client,
        f"repos/{repository}/issues/{number}/comments?per_page=100", paginate=True
    )
    for comment in _flatten_github_array_pages(issue_comments, "issue comments"):
        _require_github_parent_url(
            comment,
            field="issue_url",
            expected=issue_api_url,
            label="issue-comment",
        )
    sources.append(("issue-comments", issue_comments))
    if "pull_request" in issue:
        pull_link = issue.get("pull_request")
        if not isinstance(pull_link, Mapping):
            raise EvidenceCaptureError("GitHub pull-request link is not an object")
        _require_github_parent_url(
            pull_link,
            field="url",
            expected=pull_api_url,
            label="pull-request link",
        )
        pull = _github_json(store, client, f"repos/{repository}/pulls/{number}")
        if not isinstance(pull, Mapping) or pull.get("number") != number:
            raise EvidenceCaptureError("GitHub pull-request number differs from the request")
        _require_github_parent_url(
            pull,
            field="url",
            expected=pull_api_url,
            label="pull-request",
        )
        repository_id = int(repository_prefix.rsplit(":", 1)[1])
        base = pull.get("base")
        base_repository = base.get("repo") if isinstance(base, Mapping) else None
        if (
            not isinstance(base_repository, Mapping)
            or base_repository.get("id") != repository_id
            or not isinstance(base_repository.get("full_name"), str)
            or str(base_repository["full_name"]).casefold() != repository.casefold()
        ):
            raise EvidenceCaptureError("GitHub pull-request repository identity is inconsistent")
        reviews = _github_json(
            store,
            client,
            f"repos/{repository}/pulls/{number}/reviews?per_page=100",
            paginate=True,
        )
        for review in _flatten_github_array_pages(reviews, "pull-request reviews"):
            _require_github_parent_url(
                review,
                field="pull_request_url",
                expected=pull_api_url,
                label="pull-request review",
            )
        review_comments = _github_json(
            store,
            client,
            f"repos/{repository}/pulls/{number}/comments?per_page=100",
            paginate=True,
        )
        for comment in _flatten_github_array_pages(
            review_comments, "pull-request review comments"
        ):
            _require_github_parent_url(
                comment,
                field="pull_request_url",
                expected=pull_api_url,
                label="pull-request review comment",
            )
        sources.extend(
            (
                ("pull-request", pull),
                ("pull-request-reviews", reviews),
                ("pull-request-review-comments", review_comments),
            )
        )
    for role, value in sources:
        raw = canonical_json(value, pretty=True)
        digest = sha256_bytes(raw)
        identity = f"{repository_prefix}:discussion:{number}:{role}:snapshot:{digest}"
        source = _github_source(
            "github-discussion-snapshot",
            identity,
            f"GitHub discussion {number} {role}",
            occurred_at=None,
            expires_at=None,
            expiry_basis="unknown",
            commit_sha=None,
        )
        _capture_github_json(
            store,
            value,
            trigger=trigger,
            repository=repository,
            source=source,
            role=f"github-{role}",
        )


def validate_arguments(arguments: argparse.Namespace) -> None:
    if not TRIGGER_PATTERN.fullmatch(arguments.trigger):
        raise EvidenceCaptureError("trigger must be a short lowercase slug")
    if arguments.repository is not None and not REPOSITORY_PATTERN.fullmatch(
        arguments.repository
    ):
        raise EvidenceCaptureError("repository must use owner/name form")
    if arguments.artifact_max_bytes < 0 or arguments.artifact_max_bytes > MAX_OBJECT_BYTES:
        raise EvidenceCaptureError("artifact byte boundary is invalid")
    if (
        arguments.max_capture_bytes < 1
        or arguments.max_capture_bytes > MAX_CAPTURE_MAX_BYTES
    ):
        raise EvidenceCaptureError("capture byte boundary is invalid")
    if (
        arguments.repository is not None
        and arguments.since is None
        and not arguments.discussion_number
    ):
        raise EvidenceCaptureError("GitHub capture requires --since")
    if arguments.repository is None and arguments.download_run_logs:
        raise EvidenceCaptureError("--download-run-logs requires --repository")
    if bool(arguments.codex_thread_id) != bool(arguments.codex_session_root):
        raise EvidenceCaptureError(
            "--codex-thread-id and at least one --codex-session-root are required together"
        )


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--store", type=Path, required=True)
    value.add_argument("--repository")
    value.add_argument("--since")
    value.add_argument("--trigger", required=True)
    value.add_argument("--local-file", type=Path, action="append", default=[])
    value.add_argument("--local-clone-file", type=Path, action="append", default=[])
    value.add_argument("--local-directory", type=Path, action="append", default=[])
    value.add_argument("--redacted-local-jsonl", type=Path, action="append", default=[])
    value.add_argument("--codex-thread-id")
    value.add_argument("--codex-session-root", type=Path, action="append", default=[])
    value.add_argument("--download-run-logs", action="store_true")
    value.add_argument("--discussion-number", type=int, action="append", default=[])
    value.add_argument(
        "--artifact-max-bytes", type=int, default=DEFAULT_ARTIFACT_MAX_BYTES
    )
    value.add_argument(
        "--max-capture-bytes", type=int, default=DEFAULT_CAPTURE_MAX_BYTES
    )
    return value


def _print_codex_capture_progress(value: Mapping[str, object]) -> None:
    """Write one path-free aggregate progress record for unattended capture."""

    try:
        print(
            json.dumps({"evidence_capture_progress": dict(value)}, sort_keys=True),
            file=sys.stderr,
            flush=True,
        )
    except BrokenPipeError:
        # Progress is advisory; a closed observer must not invalidate the capture.
        return


def run(arguments: argparse.Namespace, *, client: GhClient | None = None) -> dict[str, object]:
    validate_arguments(arguments)
    since = parse_time(arguments.since, "--since") if arguments.since else None
    with private_umask(), EvidenceStore(
        arguments.store,
        max_capture_bytes=arguments.max_capture_bytes,
    ) as store:
        if arguments.repository is not None and since is not None:
            capture_github(
                store,
                repository=arguments.repository,
                since=since,
                trigger=arguments.trigger,
                download_run_logs=arguments.download_run_logs,
                artifact_max_bytes=arguments.artifact_max_bytes,
                client=client or GhClient(),
            )
        for number in arguments.discussion_number:
            if arguments.repository is None:
                raise EvidenceCaptureError("--discussion-number requires --repository")
            capture_github_discussion(
                store,
                repository=arguments.repository,
                number=number,
                trigger=arguments.trigger,
                client=client or GhClient(),
            )
        for path in arguments.local_file:
            capture_local_file(
                store,
                path,
                trigger=arguments.trigger,
                repository=arguments.repository,
            )
        for directory in arguments.local_directory:
            for path in iter_local_directory(directory, store_root=store.root):
                capture_local_file(
                    store,
                    path,
                    trigger=arguments.trigger,
                    repository=arguments.repository,
                )
        for path in arguments.local_clone_file:
            capture_local_file(
                store,
                path,
                trigger=arguments.trigger,
                repository=arguments.repository,
                apfs_clone=True,
            )
        for path in arguments.redacted_local_jsonl:
            capture_local_file(
                store,
                path,
                trigger=arguments.trigger,
                repository=arguments.repository,
                redacted_jsonl=True,
            )
        if arguments.codex_thread_id:
            capture_codex_thread_closure(
                store,
                thread_id=arguments.codex_thread_id,
                session_roots=arguments.codex_session_root,
                trigger=arguments.trigger,
                progress_function=_print_codex_capture_progress,
            )
        return store.summary()


def main(argv: Sequence[str] | None = None) -> int:
    try:
        arguments = parser().parse_args(argv)
        summary = run(arguments)
    except (EvidenceCaptureError, OSError) as error:
        message = (
            "required local material is unavailable or inaccessible"
            if isinstance(error, OSError)
            else str(error)
        )
        print(
            json.dumps({"error": message, "boundaries": BOUNDARIES}, sort_keys=True),
            file=sys.stderr,
        )
        return 1
    print(json.dumps(summary, sort_keys=True))
    return 2 if summary["excluded"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
