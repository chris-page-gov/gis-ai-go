#!/usr/bin/env python3
"""Shared deterministic gateway-image construction and verification helpers."""

from __future__ import annotations

import base64
import binascii
import gzip
import hashlib
import io
import json
import os
import re
import shutil
import stat
import string
import subprocess
import tarfile
import tempfile
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO, Iterable

ROOT = Path(__file__).resolve().parents[1]
CONTAINERFILE = ROOT / "apps" / "mcp-gateway" / "Containerfile"
DOCKERIGNORE = ROOT / "apps" / "mcp-gateway" / "Containerfile.dockerignore"
RECEIPT_SCHEMA = ROOT / "schemas" / "gateway-image-receipt.schema.json"

NODE_BASE_NAME = "node"
NODE_BASE_VERSION = "24.19.0-bookworm-slim"
NODE_BASE_DIGEST = "sha256:3638d9a6fe4030bd716be989438248074489337ba3275657f93595428be4fc03"
NODE_BASE_REFERENCE = f"{NODE_BASE_NAME}:{NODE_BASE_VERSION}@{NODE_BASE_DIGEST}"
PNPM_VERSION = "10.33.2"
PNPM_SHA512 = (
    "a90faf6feeab71ad6c6e57f94e0fe1a12f5dcc22cd754db40ae9593eb6a3e0b6"
    "b12e3540218bb37ae083404b1f2ce6db2a4121e979829b4aff94b99f49da1cf8"
)
BUILDKIT_REFERENCE = (
    "moby/buildkit:buildx-stable-1@"
    "sha256:28a898719c18a33f4e8000685287fa36fd0dd9560c6440227d3a732d79bb41d8"
)
BUILDKIT_DIGEST = BUILDKIT_REFERENCE.rsplit("@", 1)[1]
BUILDKIT_REPOSITORY = BUILDKIT_REFERENCE.rsplit("@", 1)[0].rsplit(":", 1)[0]
BUILDKIT_REPOSITORY_DIGEST = f"{BUILDKIT_REPOSITORY}@{BUILDKIT_DIGEST}"
BUILDKIT_CLASSIC_AMD64_MANIFEST_DIGEST = (
    "sha256:040d34121c27906c4ff9ac152a30d52bf2c5d328d3bb748916bb3d2743c02528"
)
BUILDKIT_CLASSIC_AMD64_CONFIG_ID = (
    "sha256:260cc297a47c57183fe53fb963885068c30e976060fabc90e32af04919dbd0bf"
)
BUILDKIT_CLASSIC_AMD64_REPOSITORY_DIGEST = (
    f"{BUILDKIT_REPOSITORY}@{BUILDKIT_CLASSIC_AMD64_MANIFEST_DIGEST}"
)
BUILDKIT_VERSION = "v0.32.2"
BUILDER_NAME = "gis-ai-go-gateway"
SYFT_REFERENCE = (
    "anchore/syft:v1.42.2@"
    "sha256:15952b4306fd990724afaaf7f1c71fcd03546b89fbf6f2d32b0be5f81e3ef431"
)
TRIVY_REFERENCE = (
    "aquasec/trivy:0.74.0@"
    "sha256:62b1e65e8869bc4b4c6aa4fa2b21595256c7c2f6018a9d9ad61caf87187c1969"
)

EXPECTED_REPOSITORY = "chris-page-gov/gis-ai-go"
EXPECTED_REGISTRY_ID = "io.github.chris-page-gov/gis-ai-go"
EXPECTED_ENTRYPOINT = ["node", "dist/src/container-main.js"]
EXPECTED_HEALTHCHECK = ["CMD", "node", "dist/src/container-healthcheck.js"]
EXPECTED_HEALTH_CONFIGURATION = {
    "Test": EXPECTED_HEALTHCHECK,
    "Interval": 10_000_000_000,
    "Timeout": 3_000_000_000,
    "StartPeriod": 5_000_000_000,
    "Retries": 3,
}
EXPECTED_WORKING_DIRECTORY = "/app/apps/mcp-gateway"
EXPECTED_USER = "65532:65532"
EXPECTED_PORT = "8787/tcp"
EXPECTED_ENVIRONMENT = [
    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "NODE_VERSION=24.19.0",
    "YARN_VERSION=1.22.22",
    "HOME=/nonexistent",
    "NODE_ENV=production",
    "TZ=UTC",
]
LEDGER_ROOT = "/var/lib/gis-ai-go/ledger"
RECONCILIATION_ROOT = "/var/lib/gis-ai-go/reconciliation"

OCI_INDEX_MEDIA_TYPE = "application/vnd.oci.image.index.v1+json"
OCI_MANIFEST_MEDIA_TYPE = "application/vnd.oci.image.manifest.v1+json"
OCI_CONFIG_MEDIA_TYPE = "application/vnd.oci.image.config.v1+json"
OCI_LAYER_MEDIA_TYPE = "application/vnd.oci.image.layer.v1.tar+gzip"
DOCKER_SAVE_MANIFEST = "manifest.json"

COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
SHA256_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")
VERSION_RE = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
PLATFORM_RE = re.compile(r"linux/(?:amd64|arm64)\Z")
_PATH_TOKEN_BOUNDARY = r"(?<![A-Za-z0-9._~/%-])"
_DRIVE_TOKEN_BOUNDARY = r"(?<![A-Za-z0-9._~/%-])"
_FORWARD_UNC_BOUNDARY = (
    r"(?<![A-Za-z0-9._~/%:-])"
)
CPE_URI_DRIVE_PATH_TEXT = re.compile(
    r"(?<![A-Za-z0-9._~/%-])cpe:(?:2\.3:|/)[A-Z]:(?:\\+|/)",
    re.IGNORECASE,
)
CPE_PATH_PREFIX_TEXT = re.compile(
    r"(?<![A-Za-z0-9._~/%-])cpe:(?:2\.3:|/)",
    re.IGNORECASE,
)
_PATH_SEGMENT = r"[^\\/\s\x00-\x1f:?#\"'{}\[\]]{1,255}"
_PATH_END = r"(?=[\\/?#\s\"',;)}\]]|$)"
PRIVATE_PATH_TEXT = re.compile(
    r"(?:"
    r"\bfile:/+|"
    + _PATH_TOKEN_BOUNDARY
    + r"/(?:Users|home|Volumes|workspace)/+[^/\\\s\x00-\x1f]{1,255}"
    + _PATH_END
    + r"|"
    + _PATH_TOKEN_BOUNDARY
    + r"/(?:private/tmp|private/var/folders|var/folders|root|runner|"
    r"github/workspace|__w|__t)(?=/|[?#\s\"',;)}\]]|$)|"
    + _PATH_TOKEN_BOUNDARY
    + r"/tmp/|"
    + _PATH_TOKEN_BOUNDARY
    + r"/mnt/[a-z]/(?:Users|home)/[^/\\\s\x00-\x1f]{1,255}"
    + _PATH_END
    + r"|"
    + _PATH_TOKEN_BOUNDARY
    + r"/opt/(?:actions-runner|hostedtoolcache)(?=/|[?#\s\"',;)}\]]|$)|"
    + _DRIVE_TOKEN_BOUNDARY
    + r"[A-Z]:(?:\\+|/)[^/\\\s\x00-\x1f]{0,255}"
    + _PATH_END
    + r"|"
    + _PATH_TOKEN_BOUNDARY
    + r"\\{2}\?\\+UNC\\+"
    + _PATH_SEGMENT
    + r"\\+"
    + _PATH_SEGMENT
    + _PATH_END
    + r"|"
    + _DRIVE_TOKEN_BOUNDARY
    + r"\\{2}[?.]\\+"
    + r"|"
    + _DRIVE_TOKEN_BOUNDARY
    + r"\\{2}[?.]\\+[A-Z]:\\+[^/\\\s\x00-\x1f]{0,255}"
    + _PATH_END
    + r"|"
    + _PATH_TOKEN_BOUNDARY
    + r"\\{2}"
    + _PATH_SEGMENT
    + r"(?:\\+|/)"
    + _PATH_SEGMENT
    + _PATH_END
    + r"|"
    + _FORWARD_UNC_BOUNDARY
    + r"//[?.]/"
    + r"|"
    + _FORWARD_UNC_BOUNDARY
    + r"//"
    + _PATH_SEGMENT
    + r"(?:/|\\+)"
    + _PATH_SEGMENT
    + _PATH_END
    + r"|\b(?:RUNNER_TEMP|RUNNER_WORKSPACE|GITHUB_WORKSPACE)\s*="
    r")",
    re.IGNORECASE,
)
DIAGNOSTIC_PRIVATE_PATH_TEXT = re.compile(
    r"(?:"
    r"\bfile:/+|"
    r"/(?:Users|home|Volumes|workspace)(?:/|$)|"
    r"/(?:private/tmp|private/var/folders|tmp|var/folders|root|runner|"
    r"github/workspace|__w|__t)(?:/|$)|"
    r"/opt/(?:hostedtoolcache|actions-runner)(?:/|$)|"
    r"/mnt/[a-z]/(?:Users|home)(?:/|$)|"
    + _PATH_TOKEN_BOUNDARY
    + r"[A-Z]:(?:\\+|/)|"
    + _PATH_TOKEN_BOUNDARY
    + r"\\{2}"
    + _PATH_SEGMENT
    + r"(?:\\+|/)"
    + _PATH_SEGMENT
    + _PATH_END
    + r"|"
    + _FORWARD_UNC_BOUNDARY
    + r"//[^/\s]+/[^/\s]+|"
    r"\b(?:RUNNER_TEMP|RUNNER_WORKSPACE|GITHUB_WORKSPACE)\s*="
    r")",
    re.IGNORECASE,
)
SENSITIVE_TOKEN_TEXT = re.compile(
    r"(?:"
    r"\bAuthorization[\"']?\s*[:=]\s*[\"']?Bearer(?:\s+|%20|\+)"
    r"(?!authentication\b|authori[sz]ation\b|redacted\b|unavailable\b)"
    r"[A-Za-z0-9._~+/=-]{1,}|"
    r"\bBearer(?:\s+|%20|\+)"
    r"(?!authentication\b|authori[sz]ation\b|redacted\b|unavailable\b)"
    r"[A-Za-z0-9._~+/=-]{7,}|"
    r"\bAuthorization[\"']?\s*[:=]\s*[\"']?Basic(?:\s+|%20|\+)"
    r"(?!authentication\b|authori[sz]ation\b|redacted\b|unavailable\b)"
    r"[A-Za-z0-9+/=]{1,}|"
    r"[A-Za-z][A-Za-z0-9+.-]{1,31}://[^/\s:@]*:[^@\s/]+@|"
    r"(?<!:)//[^/\s:@]*:[^@\s/]+@|"
    r"-----BEGIN[ \t\r\n\v\f\x85\u2028\u2029]+"
    r"[^-\r\n\v\f\x85\u2028\u2029]{0,64}PRIVATE"
    r"[ \t\r\n\v\f\x85\u2028\u2029]+KEY"
    r"(?:[ \t\r\n\v\f\x85\u2028\u2029]+BLOCK)?-----|"
    r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}|"
    r"glpat-[A-Za-z0-9_-]{20,}|npm_[A-Za-z0-9]{20,}|"
    r"pypi-AgEI[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{35}|"
    r"(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}|"
    r"whsec_[A-Za-z0-9]{16,}|xox[baprsce]-[A-Za-z0-9-]{20,}|"
    r"xapp-[0-9]+-[A-Za-z0-9-]{20,}|"
    r"(?:AKIA|ASIA)[0-9A-Z]{16}|"
    r"gh[pousr](?:_|%5f)[A-Za-z0-9]{20,}|"
    r"github(?:_|%5f)pat(?:_|%5f)[A-Za-z0-9_]{20,}|"
    r"sk(?:-|%2d)(?:proj(?:-|%2d))?[A-Za-z0-9_-]{20,}|"
    r"(?:AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN)\s*[:=]\s*[\"']?"
    r"[A-Za-z0-9/+=]{16,}(?=[\"'\s,}&]|$)|"
    r"gis-ai-go:ik:v1:[0-9a-f]{64}"
    r")",
    re.IGNORECASE,
)
BASIC_CREDENTIAL_PREFIX_TEXT = re.compile(
    r"(?<![A-Za-z0-9])Basic(?:"
    r"[ \t\r\n\v\f\x85\u2028\u2029]+|"
    r"\\?(?:\r\n|[\r\n\v\f\x85\u2028\u2029])[ \t]*|"
    r"%20|\+)",
    re.IGNORECASE,
)
PROJECTED_AUTHORIZATION_TEXT = re.compile(
    r"(?<![A-Za-z0-9])Authorization[\"']?\s*\]?"
    r"(?:\[[^\]\r\n]{0,159}\]){0,16}\s*[:=]\s*"
    r"(?P<authorization_value>\"(?:\\.|[^\"\\\r\n]){0,256}\"|"
    r"'(?:\\.|[^'\\\r\n]){0,256}'|[^\r\n,;}&\]]{1,256})",
    re.IGNORECASE,
)
OVERLONG_PROJECTED_AUTHORIZATION_TEXT = re.compile(
    r"(?<![A-Za-z0-9._~-])(?:[A-Za-z_][A-Za-z0-9_.-]{160,})"
    r"(?:_|\[\s*[\"']?)Authorization",
    re.IGNORECASE,
)
SENSITIVE_ASSIGNMENT_TEXT = re.compile(
    r"(?=(?<![A-Za-z0-9._~%-])"
    r"(?:--?)?(?P<quote>[\"']?)(?P<key>[:_]{0,2}"
    r"[A-Za-z_][A-Za-z0-9_.-]{0,159}"
    r"(?:\[[^\]\r\n]{0,159}\]){0,16})"
    r"(?P=quote)\]?\s*(?P<delimiter>[:=])(?P<spacing>\s*)"
    r"(?P<value>\"(?:\\.|[^\"\\\r\n]){0,256}\"|"
    r"'(?:\\.|[^'\\\r\n]){0,256}'|"
    r"\$\{\{\s*[A-Za-z_][A-Za-z0-9_.-]*\s*\}\}|"
    r"\$\{[A-Za-z_][A-Za-z0-9_]*\}|"
    r"\{\{\s*[A-Za-z_][A-Za-z0-9_.-]*\s*\}\}|"
    r"\[redacted\]|\[\]|\{\}|not[ _-](?:set|provided|applicable)|n/a|"
    r"[^\s\r\n,;)&>`}&\]]{0,256}))",
    re.IGNORECASE,
)
MALFORMED_SPACED_ASSIGNMENT_TEXT = re.compile(
    r"(?=(?<![A-Za-z0-9._~%/\\-])"
    r"(?P<key>[A-Za-z_][A-Za-z0-9_.-]{0,79}"
    r"(?:[ \t]+[A-Za-z_][A-Za-z0-9_.-]{0,79}){0,3})"
    r"[ \t]*(?P<delimiter>[:=])(?P<spacing>[ \t]*)"
    r"(?P<value>\"(?:\\.|[^\"\\\r\n]){0,256}\"|"
    r"'(?:\\.|[^'\\\r\n]){0,256}'|"
    r"\$\{\{\s*[A-Za-z_][A-Za-z0-9_.-]*\s*\}\}|"
    r"\$\{[A-Za-z_][A-Za-z0-9_]*\}|"
    r"\{\{\s*[A-Za-z_][A-Za-z0-9_.-]*\s*\}\}|"
    r"\[redacted\]|\[\]|\{\}|not[ _-](?:set|provided|applicable)|n/a|"
    r"[^\r\n,}\]]{1,256}))",
    re.IGNORECASE,
)
MALFORMED_RAW_ASSIGNMENT_TEXT = re.compile(
    r"(?=(?<![A-Za-z0-9._~%/\\-])"
    r"(?P<key>\"(?:\\.|[^\"\\\r\n]){1,160}\"|"
    r"'(?:\\.|[^'\\\r\n]){1,160}'|"
    r"[A-Za-z_$][^:=,\r\n{}\[\]]{0,159}?)"
    r"\s*(?P<delimiter>[:=])\s*"
    r"(?P<value>\"(?:\\.|[^\"\\\r\n]){0,256}\"|"
    r"'(?:\\.|[^'\\\r\n]){0,256}'|"
    r"\$\{\{\s*[A-Za-z_][A-Za-z0-9_.-]*\s*\}\}|"
    r"\$\{[A-Za-z_][A-Za-z0-9_]*\}|"
    r"\{\{\s*[A-Za-z_][A-Za-z0-9_.-]*\s*\}\}|"
    r"\[redacted\]|\[\]|\{\}|not[ _-](?:set|provided|applicable)|n/a|"
    r"[^\r\n,)>`}&\]]{0,256}))",
    re.IGNORECASE,
)
MALFORMED_STRUCTURAL_ASSIGNMENT_TEXT = re.compile(
    r"(?=(?<![A-Za-z0-9._~%/\\-])"
    r"(?P<key>\"(?:\\.|[^\"\\\r\n]){1,160}\"|"
    r"'(?:\\.|[^'\\\r\n]){1,160}'|"
    r"[A-Za-z_$][^:=,\r\n{}\[\]]{0,159}?)"
    r"(?:\s*[\[\]{}]){1,16}\s*(?P<delimiter>[:=])\s*"
    r"(?P<value>\"(?:\\.|[^\"\\\r\n]){0,256}\"|"
    r"'(?:\\.|[^'\\\r\n]){0,256}'|"
    r"\$\{\{\s*[A-Za-z_][A-Za-z0-9_.-]*\s*\}\}|"
    r"\$\{[A-Za-z_][A-Za-z0-9_]*\}|"
    r"\{\{\s*[A-Za-z_][A-Za-z0-9_.-]*\s*\}\}|"
    r"\[redacted\]|\[\]|\{\}|not[ _-](?:set|provided|applicable)|n/a|"
    r"[^\r\n,)>`}&\]]{0,256}))",
    re.IGNORECASE,
)
OVERLONG_MALFORMED_STRUCTURAL_KEY_TEXT = re.compile(
    r"(?=(?<![A-Za-z0-9._~%/\\-])"
    r"(?P<key>\"(?:\\.|[^\"\\\r\n]){1,160}\"|"
    r"'(?:\\.|[^'\\\r\n]){1,160}'|"
    r"[A-Za-z_$][^:=,\r\n{}\[\]]{0,159}?)"
    r"(?:\s*[\[\]{}]){17})",
    re.IGNORECASE,
)
COMMENTED_VALUE_PROPERTY_TEXT = re.compile(
    r"\A\s*(?P<key>\"(?:\\.|[^\"\\\r\n]){1,160}\"|"
    r"'(?:\\.|[^'\\\r\n]){1,160}'|[A-Za-z_$][A-Za-z0-9_$.-]{0,159})"
    r"\s*[:=]\s*"
    r"(?P<value>\"(?:\\.|[^\"\\\r\n]){0,256}\"|"
    r"'(?:\\.|[^'\\\r\n]){0,256}'|[^\r\n,}]{1,256})"
    r"\s*,?\s*\Z",
    re.IGNORECASE,
)
OVERLONG_ASSIGNMENT_KEY_TEXT = re.compile(
    r"(?=(?<![A-Za-z0-9._~%-])"
    r"(?:(?:[A-Za-z_][A-Za-z0-9_.]{0,63})\s*\[\s*)?"
    r"(?:--?)?(?P<over_quote>[\"']?)[A-Za-z_][A-Za-z0-9_.-]{160,}"
    r"(?P=over_quote)\s*\]?\s*[:=])",
    re.IGNORECASE,
)
OVERLONG_BRACKETED_KEY_TEXT = re.compile(
    r"(?<![A-Za-z0-9._~%-])(?:--?)?"
    r"[A-Za-z_][A-Za-z0-9_.-]{0,159}"
    r"(?:\[[^\]\r\n]{0,159}\]){0,16}\[[^\]\r\n]{160,}\]",
    re.IGNORECASE,
)
OVERLONG_BRACKETED_KEY_DEPTH_TEXT = re.compile(
    r"(?<![A-Za-z0-9._~%-])(?:--?)?"
    r"[A-Za-z_][A-Za-z0-9_.-]{0,159}"
    r"(?:\[[^\]\r\n]{0,159}\]){17}(?=\[|\s*[:=])",
    re.IGNORECASE,
)
SENSITIVE_QUERY_TEXT = re.compile(
    r"[?&](?P<query_key>[A-Za-z_][A-Za-z0-9_.-]{0,159}"
    r"(?:\[[^\]\r\n&#\s]{0,159}\]){0,16})="
    r"(?P<query_value>[^&#\s\"'`,;)>}\]]{1,256})",
    re.IGNORECASE,
)
OVERLONG_SENSITIVE_QUERY_TEXT = re.compile(
    r"[?&][A-Za-z_][A-Za-z0-9_.-]{0,159}"
    r"(?:\[[^\]\r\n&#\s]{0,159}\]){17}(?=\[|=)",
    re.IGNORECASE,
)
OVERLONG_QUERY_COMPONENT_TEXT = re.compile(
    r"[?&][A-Za-z_][A-Za-z0-9_.-]{0,159}"
    r"(?:\[[^\]\r\n&#\s\"']{0,159}\]){0,16}"
    r"\[[^\]\r\n&#\s\"']{160,}\]",
    re.IGNORECASE,
)
OVERLONG_QUERY_KEY_TEXT = re.compile(
    r"[?&][A-Za-z_][A-Za-z0-9_.-]{160,}(?:\[|=)",
    re.IGNORECASE,
)
CLI_CREDENTIAL_TEXT = re.compile(
    r"(?=(?<![A-Za-z0-9._~%-])--?"
    r"(?P<cli_key>[A-Za-z_][A-Za-z0-9_.-]{0,159})\s+"
    r"(?P<cli_value>\"(?:\\.|[^\"\\\r\n]){0,256}\"|"
    r"'(?:\\.|[^'\\\r\n]){0,256}'|[^\s\r\n,;}&\]]{1,256}))",
    re.IGNORECASE,
)
OVERLONG_CLI_KEY_TEXT = re.compile(
    r"(?<![A-Za-z0-9._~%-])--?[A-Za-z_][A-Za-z0-9_.-]{160,}\s+",
    re.IGNORECASE,
)
OVERLONG_BRACKETED_BASE_TEXT = re.compile(
    r"(?<![A-Za-z0-9._~%-])(?:--?)?[\"']?"
    r"[A-Za-z_][A-Za-z0-9_.-]{160,}\[",
    re.IGNORECASE,
)
PRIVACY_JSON_UNICODE_ESCAPE = re.compile(r"\\u([0-9a-f]{4})", re.IGNORECASE)
PRIVACY_JS_UNICODE_ESCAPE = re.compile(
    r"\\u\{([0-9a-f]{1,6})\}", re.IGNORECASE
)
PRIVACY_PYTHON_HEX_ESCAPE = re.compile(r"\\x([0-9a-f]{2})", re.IGNORECASE)
PRIVACY_OCTAL_ESCAPE = re.compile(r"\\([0-7]{1,3})")
PRIVACY_JSON_LINE_ESCAPE = re.compile(r"\\(?:r\\n|[abfnrtv0])")
PRIVACY_JSON_SLASH_ESCAPE = re.compile(r"\\/")
PRIVACY_JSON_QUOTE_ESCAPE = re.compile(r'\\"')
PRIVACY_JSON_BACKSLASH_ESCAPE = re.compile(r"\\\\(?!:)")
PRIVACY_LINE_FOLD = re.compile(
    r"\\?(?:\r\n|[\t\r\n\v\f\x85\u2028\u2029])[ \t]*"
)
UNSAFE_ASCII_PRIVACY_CONTROL_TEXT = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]"
)
PRIVACY_LINE_TERMINATORS = "\r\n\u2028\u2029"
MAX_PRIVACY_DECODE_PASSES = 3
MAX_PRIVACY_BACKSLASH_RUN = 64
MAX_PRIVACY_PERCENT_RUN_BYTES = 4096
SAFE_CREDENTIAL_PLACEHOLDERS = frozenset(
    {
        "",
        "null",
        "none",
        "empty",
        "redacted",
        "[redacted]",
        "<redacted>",
        "not set",
        "not-set",
        "not_set",
        "unavailable",
        "n/a",
        "not applicable",
        "not-applicable",
        "not_applicable",
        "not provided",
        "not-provided",
        "not_provided",
        "false",
        "true",
        "********",
        "[]",
        "{}",
    }
)
SAFE_JSONC_CREDENTIAL_ANNOTATIONS = frozenset(
    {
        "c",
        "comment",
        "config",
        "configuration",
        "documentation",
        "docs",
        "example",
        "note",
        "ok",
        "placeholder",
        "todo",
    }
)
SAFE_JSONC_CREDENTIAL_ANNOTATION_CUES = frozenset(
    {
        "configuration",
        "deployment",
        "docs",
        "environment",
        "example",
        "injected",
        "loaded",
        "provided",
        "requirements",
        "runtime",
        "stored",
        "supplied",
        "variable",
    }
)
CREDENTIAL_MATERIAL_SUFFIXES = (
    "accesskey",
    "material",
    "encoding",
    "base64",
    "content",
    "payload",
    "digest",
    "encoded",
    "string",
    "bytes",
    "value",
    "base",
    "data",
    "b64",
    "pem",
    "der",
    "jwk",
    "json",
    "hex",
    "hash",
    "raw",
    "blob",
    "body",
    "text",
    "pkcs1",
    "pkcs8",
    "openssh",
    "ed25519",
    "ecdsa",
    "seed",
    "rsa",
    "ec",
)
MALFORMED_SPACED_SENSITIVE_KEY_SUFFIXES = (
    "apikey",
    "secretkey",
    "privatekey",
    "signingkey",
    "encryptionkey",
    "hmackey",
    "fernetkey",
    "jwtkey",
    "clientsecret",
    "accesstoken",
    "refreshtoken",
    "authtoken",
    "authorizationtoken",
    "githubtoken",
    "apitoken",
    "secretaccesskey",
)
MAX_CREDENTIAL_MATERIAL_SUFFIXES = 16
MAX_PRIVACY_INLINE_JSON_CHARS = 8 * 1024 * 1024
MAX_PRIVACY_TEXT_BYTES = 8 * 1024 * 1024
MAX_PRIVACY_JSON_DEPTH = 128
MAX_PRIVACY_JSON_NODES = 1_000_000
MAX_PRIVACY_JSON_ALIASES = 16
MAX_PRIVACY_EMBEDDED_JSON_CANDIDATES = 4096
MAX_PRIVACY_MALFORMED_TOKEN_CHARS = 4096
MAX_PRIVACY_MALFORMED_TOKENS = 4096
MAX_PRIVACY_MALFORMED_CHARS = 1024 * 1024
MAX_PRIVACY_JSON_NUMBER_CHARS = 4096
MAX_JOSE_HEADER_PROBE_CHARS = 4096
PRIVACY_PHASE_OUTPUT_BOUNDARY = "[gateway-phase-output-boundary]"
MALFORMED_COMMENT_STRUCTURE_TRANSLATION = str.maketrans("{}[]", "    ")
_JOSE_CHARS = frozenset(string.ascii_letters + string.digits + "_-")
_BASIC_TOKEN_CHARS = frozenset(string.ascii_letters + string.digits + "+/=")
_PATH_BOUNDARY_CHARS = frozenset(string.ascii_letters + string.digits + "._~/%-")
_PATH_SCAN_TERMINATOR_TEXT = re.compile(r"[\s?#\"']")
CREDENTIAL_METADATA_SUFFIXES = frozenset(
    {
        "algorithm",
        "count",
        "description",
        "enabled",
        "field",
        "format",
        "header",
        "id",
        "length",
        "name",
        "policy",
        "provider",
        "required",
        "route",
        "schema",
        "type",
        "version",
    }
)
REVIEWED_CPE_BASE_IDENTITIES = frozenset(
    {("base", "base-passwd"), ("base-passwd", "base-passwd")}
)


def _decode_privacy_escapes_once(value: str) -> str:
    """Decode one bounded layer of printable ASCII percent/JSON escapes."""

    def decode_json_unicode(match: re.Match[str]) -> str:
        decoded = int(match.group(1), 16)
        character = chr(decoded)
        return (
            character
            if 0x20 <= decoded <= 0x7E
            or decoded in {0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x85, 0x2028, 0x2029}
            or unicodedata.category(character) in {"Cc", "Cf"}
            else match.group(0)
        )

    def decode_js_unicode(match: re.Match[str]) -> str:
        decoded = int(match.group(1), 16)
        if decoded > 0x10FFFF:
            return "\0"
        character = chr(decoded)
        return (
            character
            if 0x20 <= decoded <= 0x7E
            or decoded in {0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x85, 0x2028, 0x2029}
            or unicodedata.category(character) in {"Cc", "Cf"}
            else match.group(0)
        )

    def decode_octal(match: re.Match[str]) -> str:
        decoded = int(match.group(1), 8)
        return chr(decoded) if decoded <= 0xFF else "\0"

    def decode_json_line(match: re.Match[str]) -> str:
        return "\r\n" if match.group(0).lower() == "\\r\\n" else "\n"

    def decode_python_hex(match: re.Match[str]) -> str:
        decoded = int(match.group(1), 16)
        character = chr(decoded)
        return (
            character
            if 0x20 <= decoded <= 0x7E
            or unicodedata.category(character) in {"Cc", "Cf"}
            else match.group(0)
        )

    decoded = _decode_percent_privacy_escapes(value)
    decoded = PRIVACY_JS_UNICODE_ESCAPE.sub(decode_js_unicode, decoded)
    decoded = PRIVACY_JSON_UNICODE_ESCAPE.sub(decode_json_unicode, decoded)
    decoded = PRIVACY_PYTHON_HEX_ESCAPE.sub(decode_python_hex, decoded)
    decoded = PRIVACY_OCTAL_ESCAPE.sub(decode_octal, decoded)
    decoded = PRIVACY_JSON_LINE_ESCAPE.sub(decode_json_line, decoded)
    decoded = PRIVACY_JSON_QUOTE_ESCAPE.sub('"', decoded)
    decoded = PRIVACY_JSON_BACKSLASH_ESCAPE.sub(lambda _match: "\\", decoded)
    return PRIVACY_JSON_SLASH_ESCAPE.sub("/", decoded)


def _decode_percent_privacy_escapes(value: str) -> str:
    """Decode bounded percent-octet runs without regex repetition storage."""
    if "%" not in value:
        return value
    output: list[str] = []
    position = 0
    while position < len(value):
        start = value.find("%", position)
        if start < 0:
            output.append(value[position:])
            break
        if (
            start + 2 >= len(value)
            or value[start + 1] not in string.hexdigits
            or value[start + 2] not in string.hexdigits
        ):
            output.append(value[position : start + 1])
            position = start + 1
            continue
        output.append(value[position:start])
        octets = bytearray()
        cursor = start
        while (
            cursor + 2 < len(value)
            and value[cursor] == "%"
            and value[cursor + 1] in string.hexdigits
            and value[cursor + 2] in string.hexdigits
        ):
            if len(octets) >= MAX_PRIVACY_PERCENT_RUN_BYTES:
                return "\0"
            octets.append(int(value[cursor + 1 : cursor + 3], 16))
            cursor += 3
        try:
            output.append(bytes(octets).decode("utf-8", errors="strict"))
        except UnicodeDecodeError:
            # Malformed encoded octets must not shield a valid credential suffix.
            return "\0"
        position = cursor
    return "".join(output)


def _decoded_privacy_projection(value: str) -> str | None:
    """Decode the bounded privacy projection or fail on deeper encoding."""
    candidate = value
    for _ in range(MAX_PRIVACY_DECODE_PASSES + 1):
        decoded = _decode_privacy_escapes_once(candidate)
        if decoded == candidate:
            return candidate
        candidate = decoded
    return candidate if _decode_privacy_escapes_once(candidate) == candidate else None


def _fold_privacy_lines(value: str) -> str:
    """Join physical or escaped line continuations with bounded C-level storage."""
    return PRIVACY_LINE_FOLD.sub("", value)


def _contains_unsafe_privacy_control(value: str) -> bool:
    """Reject invisible/control text except ordinary tab and line endings."""
    if UNSAFE_ASCII_PRIVACY_CONTROL_TEXT.search(value):
        return True
    if value.isascii():
        return False
    return any(
        unicodedata.category(character).startswith("C")
        and character not in "\t\n\r"
        for character in value
        if not character.isascii()
    )


def _utf8_length_exceeds(value: str, maximum_bytes: int) -> bool:
    """Check a UTF-8 byte bound without allocating one full encoded copy."""
    if len(value) > maximum_bytes:
        return True
    if value.isascii():
        return False
    byte_count = 0
    for offset in range(0, len(value), 64 * 1024):
        try:
            byte_count += len(value[offset : offset + 64 * 1024].encode("utf-8"))
        except UnicodeEncodeError:
            return True
        if byte_count > maximum_bytes:
            return True
    return False


def _bounded_utf8_length(value: str, maximum_bytes: int) -> int | None:
    """Return one UTF-8 byte length, or ``None`` once the bound is exceeded."""
    if len(value) > maximum_bytes:
        return None
    if value.isascii():
        return len(value)
    byte_count = 0
    for offset in range(0, len(value), 64 * 1024):
        try:
            byte_count += len(value[offset : offset + 64 * 1024].encode("utf-8"))
        except UnicodeEncodeError:
            return None
        if byte_count > maximum_bytes:
            return None
    return byte_count


def _contains_basic_credential(value: str) -> bool:
    """Recognise a bounded RFC Basic token only when it decodes to user:password."""
    for prefix in BASIC_CREDENTIAL_PREFIX_TEXT.finditer(value):
        position = prefix.end()
        end = position
        while end < len(value) and value[end] in _BASIC_TOKEN_CHARS:
            end += 1
        if end == position:
            continue
        if end - position > 4096:
            return True
        token = value[position:end]
        if "=" in token[:-2]:
            continue
        try:
            decoded = base64.b64decode(
                token + "=" * (-len(token) % 4), validate=True
            )
        except (binascii.Error, ValueError):
            continue
        _username, separator, password = decoded.partition(b":")
        if not separator or not password:
            continue
        has_explicit_base64_cue = any(
            character in string.digits + "+/=" for character in token
        )
        if has_explicit_base64_cue:
            return True
        try:
            decoded_text = decoded.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            has_c0_control = any(byte < 0x20 for byte in decoded)
            has_c1_control = any(0x7F <= byte <= 0x9F for byte in decoded)
            if has_c1_control or (has_c0_control and bool(_username)):
                return True
            continue
        text_username, text_separator, text_password = decoded_text.partition(":")
        has_control = any(
            unicodedata.category(character).startswith("C")
            for character in decoded_text
        ) or any(character in PRIVACY_LINE_TERMINATORS for character in decoded_text)
        if text_separator and text_password and has_control:
            return True
        if (
            text_separator
            and text_password
            and not has_control
            and (text_username or has_explicit_base64_cue)
        ):
            return True
    return False


def _is_safe_credential_placeholder(value: str) -> bool:
    if value.lower() in SAFE_CREDENTIAL_PLACEHOLDERS:
        return True
    if re.fullmatch(
        r"(?:\$\{[A-Za-z_][A-Za-z0-9_]*\}|\$[A-Za-z_][A-Za-z0-9_]*|"
        r"\$?\{\{\s*[A-Za-z_][A-Za-z0-9_.-]*\s*\}\}|"
        r"sha256:[0-9a-f]{64})",
        value,
        re.IGNORECASE,
    ):
        return True
    return re.fullmatch(r"\*{8,}", value) is not None


def _jsonc_comment_value_is_sensitive(key: str, body: str) -> bool:
    """Classify a value-slot comment without treating ordinary prose as data."""
    stripped = body.strip()
    projected = _decoded_privacy_projection(stripped)
    if projected is None:
        return True
    normalised = _normalise_matched_credential_value(projected)
    if not normalised or _is_safe_credential_placeholder(normalised):
        return False
    if stripped[:1] in {"\"", "'"} or projected != stripped:
        return _credential_key_value_is_sensitive(key, normalised)
    if any(
        marker in projected
        for marker in ("//", "/*", "*/", "{", "}", "[", "]", ":", "=")
    ):
        return True
    if (
        SENSITIVE_TOKEN_TEXT.search(projected)
        or _contains_basic_credential(projected)
        or _contains_compact_jose_token(projected)
    ):
        return True
    folded = normalised.casefold()
    if folded in SAFE_JSONC_CREDENTIAL_ANNOTATIONS:
        return False
    prose_words = re.fullmatch(r"[A-Za-z]+(?:[ \t]+[A-Za-z]+)*", normalised)
    if prose_words is not None and SAFE_JSONC_CREDENTIAL_ANNOTATION_CUES.intersection(
        folded.split()
    ):
        return False
    return _credential_key_value_is_sensitive(key, normalised)


def _safe_placeholder_has_clean_termination(match: re.Match[str]) -> bool:
    position = match.end("value")
    text = match.string
    spaces = 0
    while position < len(text) and text[position] in " \t" and spaces < 256:
        position += 1
        spaces += 1
    comment_bytes = 0
    key = match.group("key").lstrip(":_")
    for _ in range(16):
        if text.startswith("/*", position):
            end = text.find("*/", position + 2, min(len(text), position + 1024))
            if end < 0:
                return False
            if _jsonc_comment_value_is_sensitive(
                key, text[position + 2 : end]
            ):
                return False
            comment_bytes += end + 2 - position
            position = end + 2
        elif text.startswith("//", position):
            end = position + 2
            limit = min(len(text), position + 1024)
            while end < limit and text[end] not in PRIVACY_LINE_TERMINATORS:
                end += 1
            if end == len(text):
                return not _jsonc_comment_value_is_sensitive(
                    key, text[position + 2 : end]
                )
            if end == limit:
                return False
            if _jsonc_comment_value_is_sensitive(
                key, text[position + 2 : end]
            ):
                return False
            comment_bytes += end + 1 - position
            position = end + 1
        else:
            break
        while position < len(text) and text[position].isspace():
            position += 1
            comment_bytes += 1
            if comment_bytes > 1024:
                return False
    if position == len(text) or text[position] in "\r\n,;}&]\"'":
        return True
    if spaces == 256 and position < len(text) and text[position] in " \t":
        return False
    return spaces > 0 and SENSITIVE_ASSIGNMENT_TEXT.match(text, position) is not None


def _strip_credential_material_suffixes(value: str) -> str:
    stripped = value
    for _ in range(MAX_CREDENTIAL_MATERIAL_SUFFIXES):
        suffix = next(
            (
                candidate
                for candidate in CREDENTIAL_MATERIAL_SUFFIXES
                if stripped.endswith(candidate) and len(stripped) > len(candidate)
            ),
            None,
        )
        if suffix is None:
            break
        stripped = stripped[: -len(suffix)]
    return stripped


def _credential_component_parts(value: str) -> tuple[tuple[str, ...], str]:
    component = value.strip()
    if (
        len(component) >= 2
        and component[0] == component[-1]
        and component[0] in {"\"", "'"}
    ):
        component = component[1:-1].strip()
    expanded = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", component.lstrip(":_"))
    words = tuple(
        part.lower()
        for part in re.split(r"[^A-Za-z0-9]+", expanded)
        if part
    )
    suffix_words = frozenset(CREDENTIAL_MATERIAL_SUFFIXES)
    retained = list(words)
    for _ in range(MAX_CREDENTIAL_MATERIAL_SUFFIXES):
        if not retained or retained[-1] not in suffix_words:
            break
        retained.pop()
    compact = _strip_credential_material_suffixes("".join(retained))
    return tuple(retained), compact


def _credential_key_components(value: str) -> tuple[tuple[tuple[str, ...], str], ...]:
    base, _, suffix = value.partition("[")
    components = [base]
    if suffix:
        components.extend(
            match.group(1)
            for match in re.finditer(r"\[([^\]\r\n]{0,159})\]", "[" + suffix)
        )
    candidates = [
        parts
        for component in components
        if (parts := _credential_component_parts(component))[0]
    ]
    if suffix:
        joined_key = re.sub(r"\[(?:[0-9]*)\]", "", value)
        joined_key = joined_key.replace("[", "").replace("]", "")
        joined = _credential_component_parts(joined_key)
        joined_kind = _credential_key_kind(*joined)
        if joined[0] and (
            joined_kind == "sensitive"
            or joined[1]
            in {
                "token",
                "tokens",
                "accesstoken",
                "refreshtoken",
                "authtoken",
                "authenticationtoken",
                "authorizationtoken",
                "githubtoken",
                "apitoken",
            }
            or joined[0][-1] == "authorization"
        ):
            candidates.append(joined)
    return tuple(dict.fromkeys(candidates))


def _credential_key_kind(words: tuple[str, ...], compact: str) -> str | None:
    if not words or not compact:
        return None
    if words[-1] in CREDENTIAL_METADATA_SUFFIXES:
        return None
    if compact == "compassword" and "password" not in words:
        return None
    if any(
        word in {
            "password",
            "passwords",
            "passwd",
            "pwd",
            "credential",
            "credentials",
            "secret",
            "secrets",
        }
        for word in words
    ):
        return "sensitive"
    sensitive_pairs = {
        ("api", "key"),
        ("api", "keys"),
        ("secret", "key"),
        ("secret", "keys"),
        ("private", "key"),
        ("private", "keys"),
        ("signing", "key"),
        ("signing", "keys"),
        ("encryption", "key"),
        ("encryption", "keys"),
        ("hmac", "key"),
        ("hmac", "keys"),
        ("fernet", "key"),
        ("fernet", "keys"),
        ("jwt", "key"),
        ("jwt", "keys"),
        ("client", "secret"),
        ("access", "token"),
        ("refresh", "token"),
        ("auth", "token"),
        ("authentication", "token"),
        ("authorization", "token"),
        ("github", "token"),
        ("api", "token"),
    }
    if any(tuple(words[index : index + 2]) in sensitive_pairs for index in range(len(words) - 1)):
        return "sensitive"
    sensitive_triples = {
        ("secret", "access", "key"),
        ("secret", "access", "keys"),
    }
    if any(
        tuple(words[index : index + 3]) in sensitive_triples
        for index in range(len(words) - 2)
    ):
        return "sensitive"
    compact_sensitive_suffixes = (
        "password",
        "passwd",
        "apikey",
        "apikeys",
        "secretkey",
        "secretkeys",
        "privatekey",
        "privatekeys",
        "signingkey",
        "signingkeys",
        "encryptionkey",
        "encryptionkeys",
        "hmackey",
        "hmackeys",
        "fernetkey",
        "fernetkeys",
        "jwtkey",
        "jwtkeys",
        "clientsecret",
        "accesstoken",
        "refreshtoken",
        "authtoken",
        "authenticationtoken",
        "authorizationtoken",
        "githubtoken",
        "apitoken",
        "secretaccesskey",
        "secretaccesskeys",
    )
    if compact in {"pwd", "secret", "secrets", "credential", "credentials"}:
        return "sensitive"
    if any(suffix in compact for suffix in compact_sensitive_suffixes):
        return "sensitive"
    if (
        any(word in {"token", "tokens"} for word in words)
        or compact.endswith(("token", "tokens"))
    ):
        return "token"
    return None


def _cpe_prefix(match: re.Match[str]) -> str | None:
    prefix = match.string[max(0, match.start() - 512) : match.start()]
    found = re.search(
        r"(?<![A-Za-z0-9._~/%-])(?P<cpe>"
        r"(?:cpe:2\.3:[aho]:|cpe:/[aho]:)"
        r"(?:\\[^\r\n]|[A-Za-z0-9._~*?@!$()+:-]){0,384})\Z",
        prefix,
        re.IGNORECASE,
    )
    return found.group("cpe") if found is not None else None


def _split_cpe_fields(value: str) -> tuple[str, ...]:
    fields: list[str] = []
    current: list[str] = []
    backslashes = 0
    for character in value:
        if character == ":" and backslashes % 2 == 0:
            fields.append("".join(current))
            current = []
        else:
            current.append(character)
        backslashes = backslashes + 1 if character == "\\" else 0
    fields.append("".join(current))
    return tuple(fields)


def _bounded_cpe_path_token(value: str, start: int) -> tuple[str, int] | None:
    token_match = re.match(
        r"(?:\\[^\r\n]|[A-Za-z0-9._~*?@!$()+:/-]){1,1024}",
        value[start:],
    )
    if token_match is None:
        return None
    raw_token = token_match.group(0)
    end = start + len(raw_token)
    if end < len(value) and value[end] not in "\t\r\n \"',;)}]":
        return None
    if len(raw_token) == 1024 and end < len(value):
        return None
    return raw_token, end


def _valid_complete_cpe_path_token(value: str, start: int) -> int | None:
    """Return the end of one complete CPE whose part only resembles a drive."""
    bounded = _bounded_cpe_path_token(value, start)
    if bounded is None:
        return None
    raw_token, end = bounded
    token = raw_token
    for _ in range(MAX_PRIVACY_DECODE_PASSES):
        decoded = token.replace("\\\\", "\\")
        if decoded == token:
            break
        token = decoded
    else:
        if token.replace("\\\\", "\\") != token:
            return None
    lowered_token = token.lower()
    if lowered_token.startswith("cpe:2.3:"):
        component_start = len("cpe:2.3:")
    elif lowered_token.startswith("cpe:/"):
        component_start = len("cpe:/")
    else:
        return None
    position = component_start
    while position < len(token):
        character = token[position]
        if character == "\\":
            if position + 1 >= len(token):
                return None
            escaped = token[position + 1]
            if escaped.isalnum() or escaped == "_":
                return None
            position += 2
            continue
        if character == "/":
            return None
        position += 1
    fields = _split_cpe_fields(token)
    lowered = tuple(field.lower() for field in fields)
    valid = (
        len(fields) == 13
        and lowered[:2] == ("cpe", "2.3")
        and lowered[2] in {"a", "h", "o"}
    ) or (
        len(fields) == 8
        and lowered[0] == "cpe"
        and lowered[1] in {"/a", "/h", "/o"}
    )
    return end if valid else None


def _trusted_complete_cpe_path_tokens(value: str) -> frozenset[str] | None:
    tokens: set[str] = set()
    occurrences = 0
    for prefix in CPE_PATH_PREFIX_TEXT.finditer(value):
        occurrences += 1
        if occurrences > MAX_PRIVACY_EMBEDDED_JSON_CANDIDATES:
            return None
        start = prefix.start()
        end = _valid_complete_cpe_path_token(value, start)
        if end is None:
            continue
        token = value[start:end]
        tokens.add(token)
        for _ in range(MAX_PRIVACY_DECODE_PASSES):
            decoded = _decode_privacy_escapes_once(token)
            if decoded == token:
                break
            token = decoded
            tokens.add(token)
    return frozenset(tokens)


def _valid_cpe_path_spans(
    value: str, *, trusted_cpe_tokens: frozenset[str] = frozenset()
) -> tuple[tuple[int, int], ...] | None:
    valid_cpe_spans: list[tuple[int, int]] = []
    for prefix in CPE_PATH_PREFIX_TEXT.finditer(value):
        if len(valid_cpe_spans) >= MAX_PRIVACY_EMBEDDED_JSON_CANDIDATES:
            return None
        start = prefix.start()
        bounded = _bounded_cpe_path_token(value, start)
        if bounded is None:
            continue
        token, bounded_end = bounded
        end = _valid_complete_cpe_path_token(value, start)
        if end is not None or token in trusted_cpe_tokens:
            valid_cpe_spans.append((start, bounded_end if end is None else end))
    return tuple(valid_cpe_spans)


def _has_unexempted_path_match(
    matches: Iterable[re.Match[str]], valid_cpe_spans: tuple[tuple[int, int], ...]
) -> bool:
    span_index = 0
    for match in matches:
        position = match.start()
        while (
            span_index < len(valid_cpe_spans)
            and valid_cpe_spans[span_index][1] <= position
        ):
            span_index += 1
        if not (
            span_index < len(valid_cpe_spans)
            and valid_cpe_spans[span_index][0]
            <= position
            < valid_cpe_spans[span_index][1]
        ):
            return True
    return False


def _contains_private_path(
    value: str, *, trusted_cpe_tokens: frozenset[str] = frozenset()
) -> bool:
    valid_cpe_spans = _valid_cpe_path_spans(
        value, trusted_cpe_tokens=trusted_cpe_tokens
    )
    if valid_cpe_spans is None:
        return True
    return _has_unexempted_path_match(
        CPE_URI_DRIVE_PATH_TEXT.finditer(value), valid_cpe_spans
    ) or _has_unexempted_path_match(
        PRIVATE_PATH_TEXT.finditer(value), valid_cpe_spans
    )


def contains_diagnostic_private_path(value: str) -> bool:
    """Apply the broader diagnostic path gate without rejecting a valid CPE."""
    trusted_cpe_tokens = _trusted_complete_cpe_path_tokens(value)
    if trusted_cpe_tokens is None:
        return True
    valid_cpe_spans = _valid_cpe_path_spans(
        value, trusted_cpe_tokens=trusted_cpe_tokens
    )
    if valid_cpe_spans is None:
        return True
    return _has_unexempted_path_match(
        DIAGNOSTIC_PRIVATE_PATH_TEXT.finditer(value), valid_cpe_spans
    )


def _normalise_cpe_component(value: str) -> str:
    unescaped = re.sub(r"\\([:+])", r"\1", value)
    return unescaped.lower().replace("_", "-")


def _is_reviewed_sensitive_cpe_fields(fields: tuple[str, ...]) -> bool:
    if len(fields) == 13 and fields[:3] == ("cpe", "2.3", "a"):
        vendor, product, version = fields[3:6]
        trailing = fields[6:]
    elif len(fields) == 8 and fields[:2] == ("cpe", "/a"):
        vendor, product, version = fields[2:5]
        trailing = fields[5:]
    else:
        return False
    if any(field != "*" for field in trailing):
        return False
    identity = (_normalise_cpe_component(vendor), _normalise_cpe_component(product))
    normalised_version = _normalise_cpe_component(version)
    if identity in REVIEWED_CPE_BASE_IDENTITIES:
        return normalised_version == "3.6.1"
    return (
        identity == ("passwd", "passwd")
        and normalised_version == "1:4.13+dfsg1-1+deb12u2"
    )


def _is_complete_cpe_assignment(match: re.Match[str], value: str) -> bool:
    prefix = _cpe_prefix(match)
    if prefix is None or len(value) > 512:
        return False
    between = match.string[match.start("key") : match.start("value")]
    candidate = prefix + between + value
    variants = [candidate]
    for _ in range(MAX_PRIVACY_DECODE_PASSES):
        decoded = variants[-1].replace("\\\\", "\\")
        if decoded == variants[-1]:
            break
        variants.append(decoded)
    for variant in variants:
        if re.fullmatch(
            r"(?:\\[^\r\n]|[A-Za-z0-9._~*?@!$()+:/-]){1,1024}",
            variant,
        ) is None:
            continue
        fields = _split_cpe_fields(variant)
        if _is_reviewed_sensitive_cpe_fields(fields):
            return True
    return False


def _credential_assignment_is_sensitive(match: re.Match[str]) -> bool:
    key = match.group("key").lstrip(":_")
    classifications = tuple(
        (words, compact, _credential_key_kind(words, compact))
        for words, compact in _credential_key_components(key)
    )
    if not any(
        kind is not None or (words and words[-1] == "authorization")
        for words, _compact, kind in classifications
    ):
        return False
    raw_value = match.group("value")
    extended_comment_value = raw_value.lstrip().startswith(("//", "/*"))
    value_projection = (
        match.string[
            match.start("value") : min(
                len(match.string), match.start("value") + 1024
            )
        ]
        if extended_comment_value
        else raw_value
    )
    comment_bodies, uncommented_value = _leading_jsonc_comments(value_projection)
    if uncommented_value is None:
        return True
    if extended_comment_value:
        key = match.group("key").lstrip(":_")
        for body in comment_bodies:
            if _jsonc_comment_value_is_sensitive(key, body):
                return True
    value = uncommented_value.strip()
    if extended_comment_value and value[:1] in {"\"", "'"}:
        quote = value[0]
        escaped = False
        end = 1
        while end < len(value):
            character = value[end]
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == quote:
                value = value[: end + 1]
                break
            end += 1
        else:
            return True
    projected_value = _decoded_privacy_projection(value)
    if projected_value is None:
        return True
    value = projected_value
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"\"", "'"}:
        value = value[1:-1].strip()
    if _is_safe_credential_placeholder(value):
        return (
            False
            if extended_comment_value
            else not _safe_placeholder_has_clean_termination(match)
        )
    compact_colon = (
        match.group("delimiter") == ":"
        and not match.group("quote")
        and not match.group("spacing")
    )
    package_value = (
        value[:-1] if compact_colon and value.endswith(('"', "'")) else value
    )
    cpe_context = _is_complete_cpe_assignment(match, package_value)
    if compact_colon and cpe_context:
        return False
    if (
        compact_colon
        and value.lower() in {"change", "reset"}
        and match.start() > 0
        and match.string[match.start() - 1] == "/"
    ):
        return False
    if (
        match.group("delimiter") == ":"
        and bool(match.group("spacing"))
        and value.lower() in {"policy", "requirements", "rules"}
    ):
        return False
    if any(kind == "sensitive" for _words, _compact, kind in classifications):
        return bool(value)
    return any(
        kind == "token" and _token_key_value_is_sensitive(compact, value)
        for _words, compact, kind in classifications
    )


def _token_key_value_is_sensitive(classification_key: str, value: str) -> bool:
    token_key = classification_key.removesuffix("s")
    prefix = token_key.removesuffix("token")
    sensitive_prefixes = {
        "access",
        "api",
        "auth",
        "authentication",
        "authorization",
        "azure",
        "client",
        "csrf",
        "gh",
        "github",
        "id",
        "jwt",
        "npm",
        "oauth",
        "openai",
        "refresh",
        "session",
    }
    if prefix in sensitive_prefixes:
        return bool(value)
    if not prefix:
        return value.lower() not in {"cursor", "page", "pagination"}
    if prefix == "page" and re.fullmatch(
        r"(?:cursor|page|pagination)(?:-[0-9]{1,20})?",
        value,
        re.IGNORECASE,
    ):
        return False
    if prefix == "design" and value.lower() == "primary-colour":
        return False
    if prefix == "theme" and value.lower() == "primary":
        return False
    return bool(value)


def _normalise_matched_credential_value(value: str) -> str:
    normalised = value.strip()
    if (
        len(normalised) >= 2
        and normalised[0] == normalised[-1]
        and normalised[0] in {"\"", "'"}
    ):
        normalised = normalised[1:-1].strip()
    return normalised


def _credential_key_value_is_sensitive(key: str, value: str) -> bool:
    normalised = _normalise_matched_credential_value(value)
    if _is_safe_credential_placeholder(normalised):
        return False
    classifications = tuple(
        (words, compact, _credential_key_kind(words, compact))
        for words, compact in _credential_key_components(key)
    )
    if any(
        words and words[-1] == "authorization"
        for words, _compact, _kind in classifications
    ):
        return _authorization_text_is_sensitive(normalised)
    if any(compact == "auth" for _words, compact, _kind in classifications):
        return bool(normalised)
    if any(kind == "sensitive" for _words, _compact, kind in classifications):
        return bool(normalised)
    return any(
        kind == "token" and _token_key_value_is_sensitive(compact, normalised)
        for _words, compact, kind in classifications
    )


def _authorization_text_is_sensitive(value: str) -> bool:
    value = _normalise_matched_credential_value(value)
    if _is_safe_credential_placeholder(value):
        return False
    parts = re.split(r"(?:\s+|\+)", value, maxsplit=1)
    if len(parts) == 2 and parts[0].lower() in {"basic", "bearer"}:
        remainder = parts[1]
        return remainder.lower() not in {
            "authentication",
            "authorization",
            "redacted",
            "unavailable",
        }
    return bool(value)


def _authorization_value_is_sensitive(match: re.Match[str]) -> bool:
    return _authorization_text_is_sensitive(match.group("authorization_value"))


def _sensitive_query_value(match: re.Match[str]) -> bool:
    return _credential_key_value_is_sensitive(
        match.group("query_key"), match.group("query_value")
    )


def _sensitive_cli_value(match: re.Match[str]) -> bool:
    return _credential_key_value_is_sensitive(
        match.group("cli_key"), match.group("cli_value")
    )


def _json_value_is_sensitive_for_key(key: str, value: Any) -> bool:
    if value is None or isinstance(value, bool):
        return False
    if isinstance(value, (list, dict)):
        if not value:
            return False
        return any(
            _credential_key_kind(words, compact) in {"sensitive", "token"}
            or compact == "auth"
            or (words and words[-1] == "authorization")
            for words, compact in _credential_key_components(key)
        )
    if isinstance(value, str):
        return _credential_key_value_is_sensitive(key, value)
    return _credential_key_value_is_sensitive(key, str(value))


def _json_field_name(value: str) -> str:
    expanded = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    return re.sub(r"[^A-Za-z0-9]", "", expanded).lower()


def prohibited_json_reason(document: Any) -> str | None:
    """Inspect one parsed JSON value with explicit depth and node bounds."""
    stack: list[tuple[Any, int]] = [(document, 0)]
    nodes = 0
    textual_bytes = 0

    def count_text(value: str) -> bool:
        nonlocal textual_bytes
        length = _bounded_utf8_length(
            value, MAX_PRIVACY_TEXT_BYTES - textual_bytes
        )
        if length is None:
            return False
        textual_bytes += length
        return True

    while stack:
        node, depth = stack.pop()
        nodes += 1
        if nodes > MAX_PRIVACY_JSON_NODES or depth > MAX_PRIVACY_JSON_DEPTH:
            return "sensitive"
        if isinstance(node, dict):
            declarations: list[Any] = []
            property_values: list[Any] = []
            for key, value in node.items():
                if isinstance(key, str):
                    if not count_text(key):
                        return "sensitive"
                    if prohibited_text_reason(key) is not None:
                        return "sensitive"
                    projected_key = _decoded_privacy_projection(key)
                    if projected_key is None:
                        return "sensitive"
                    projected_value = value
                    if isinstance(value, str):
                        nodes += 1
                        if (
                            nodes > MAX_PRIVACY_JSON_NODES
                            or depth + 1 > MAX_PRIVACY_JSON_DEPTH
                            or not count_text(value)
                        ):
                            return "sensitive"
                        if prohibited_text_reason(value) is not None:
                            return "sensitive"
                        projected_value = _decoded_privacy_projection(value)
                        if projected_value is None:
                            return "sensitive"
                    field = _json_field_name(projected_key)
                    if field in {"name", "key", "variable", "envname"}:
                        declarations.append(projected_value)
                        if len(declarations) > MAX_PRIVACY_JSON_ALIASES:
                            return "sensitive"
                    elif field == "value":
                        property_values.append(projected_value)
                        if len(property_values) > MAX_PRIVACY_JSON_ALIASES:
                            return "sensitive"
                    if _json_value_is_sensitive_for_key(
                        projected_key, projected_value
                    ):
                        return "sensitive"
                if not isinstance(value, str):
                    stack.append((value, depth + 1))
            for declared_key in declarations:
                if not isinstance(declared_key, str):
                    continue
                if any(
                    _json_value_is_sensitive_for_key(declared_key, property_value)
                    for property_value in property_values
                ):
                    return "sensitive"
        elif isinstance(node, list):
            stack.extend((value, depth + 1) for value in node)
        elif isinstance(node, str):
            if not count_text(node):
                return "sensitive"
            if prohibited_text_reason(node) is not None:
                return "sensitive"
    return None


def _scan_json_quoted_token(
    value: str, start: int, quote: str, maximum_chars: int
) -> tuple[str | None, int]:
    """Read one bounded quoted token without regex backtracking."""
    position = start + 1
    escaped = False
    while position < len(value):
        character = value[position]
        if escaped:
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == quote:
            if position - start - 1 > maximum_chars:
                return None, position + 1
            return value[start + 1 : position], position + 1
        elif character in PRIVACY_LINE_TERMINATORS:
            return None, position + 1
        if position - start - 1 > maximum_chars:
            return None, position + 1
        position += 1
    return None, len(value)


def _lexical_json_reason(value: str) -> str | None:
    """Inspect double-quoted key/value pairs in one monotonic bounded pass."""
    position = 0
    while position < len(value):
        start = value.find('"', position)
        if start < 0:
            return None
        raw_key, after_key = _scan_json_quoted_token(value, start, '"', 512)
        if raw_key is None:
            closing = value.find('"', after_key, min(len(value), start + 1025))
            cursor = closing + 1 if closing >= 0 else after_key
            while cursor < len(value) and value[cursor].isspace():
                cursor += 1
            if cursor < len(value) and value[cursor] in ":=":
                return "sensitive"
            position = after_key
            continue
        position = after_key
        while position < len(value) and value[position].isspace():
            position += 1
        if position >= len(value) or value[position] != ":":
            continue
        position += 1
        while position < len(value) and value[position].isspace():
            position += 1
        while position < len(value):
            if value.startswith("/*", position):
                end = value.find("*/", position + 2)
                if end < 0:
                    return "sensitive"
                position = end + 2
            elif value.startswith("//", position):
                end = position + 2
                while (
                    end < len(value)
                    and value[end] not in PRIVACY_LINE_TERMINATORS
                ):
                    end += 1
                position = end
            else:
                break
            while position < len(value) and value[position].isspace():
                position += 1
        if position >= len(value):
            return None
        value_start = position
        placeholder = re.match(
            r"(?:\$\{\{\s*[A-Za-z_][A-Za-z0-9_.-]*\s*\}\}|"
            r"\$\{[A-Za-z_][A-Za-z0-9_]*\}|"
            r"\{\{\s*[A-Za-z_][A-Za-z0-9_.-]*\s*\}\}|"
            r"\[redacted\]|\[\]|\{\})",
            value[position:],
            re.IGNORECASE,
        )
        if placeholder is not None:
            position += placeholder.end()
            raw_value = value[value_start:position]
        elif value[position] in {'"', "'"}:
            quote = value[position]
            _inner_value, after_value = _scan_json_quoted_token(
                value, position, quote, 512
            )
            if _inner_value is None:
                position = after_value
                continue
            position = after_value
            raw_value = value[value_start:position]
        else:
            while (
                position < len(value)
                and not value[position].isspace()
                and value[position] not in ",}]"
                and position - value_start <= 512
            ):
                position += 1
            if position == value_start or position - value_start > 512:
                continue
            raw_value = value[value_start:position]
        try:
            key = json.loads('"' + raw_key + '"')
        except (json.JSONDecodeError, UnicodeDecodeError):
            key = raw_key
        projected_key = _decoded_privacy_projection(key)
        projected_value = _decoded_privacy_projection(raw_value)
        if projected_key is None or projected_value is None:
            return "sensitive"
        if _credential_key_value_is_sensitive(projected_key, projected_value):
            return "sensitive"
    return None


class _PrivacyJsonRejected(ValueError):
    pass


def _leading_jsonc_comments(value: str) -> tuple[tuple[str, ...], str | None]:
    """Return bounded leading JSONC comment bodies and the remaining scalar."""
    position = 0
    bodies: list[str] = []
    while True:
        while position < len(value) and value[position].isspace():
            position += 1
        if value.startswith("/*", position):
            end = value.find("*/", position + 2)
            if end < 0:
                return tuple(bodies), None
            bodies.append(value[position + 2 : end])
            position = end + 2
            continue
        if value.startswith("//", position):
            end = position + 2
            while end < len(value) and value[end] not in PRIVACY_LINE_TERMINATORS:
                end += 1
            if end >= len(value):
                return tuple(bodies), None
            bodies.append(value[position + 2 : end])
            position = end + 1
            continue
        return tuple(bodies), value[position:]


def _strip_leading_jsonc_comments(value: str) -> str | None:
    """Remove bounded leading JSONC comments from one matched scalar value."""
    _bodies, remainder = _leading_jsonc_comments(value)
    return remainder


def _load_privacy_json(value: str) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, item in pairs:
            if key in result:
                raise _PrivacyJsonRejected
            result[key] = item
        return result

    def reject_constant(_value: str) -> None:
        raise _PrivacyJsonRejected

    def parse_integer(number: str) -> int:
        if len(number) > MAX_PRIVACY_JSON_NUMBER_CHARS:
            raise _PrivacyJsonRejected
        return int(number)

    def parse_float(number: str) -> float:
        if len(number) > MAX_PRIVACY_JSON_NUMBER_CHARS:
            raise _PrivacyJsonRejected
        return float(number)

    return json.loads(
        value,
        object_pairs_hook=reject_duplicates,
        parse_constant=reject_constant,
        parse_int=parse_integer,
        parse_float=parse_float,
    )


def _top_level_json_string_reason(value: str) -> tuple[bool, str | None]:
    """Unwrap at most three complete JSON strings before text classification."""
    current = value.strip()
    if not current.startswith('"'):
        return False, None
    unwrapped = False
    for _ in range(MAX_PRIVACY_DECODE_PASSES):
        try:
            document = _load_privacy_json(current)
        except (_PrivacyJsonRejected, json.JSONDecodeError, RecursionError, ValueError):
            break
        if not isinstance(document, str):
            return (True, prohibited_json_reason(document)) if unwrapped else (False, None)
        unwrapped = True
        current = document
        if _utf8_length_exceeds(current, MAX_PRIVACY_TEXT_BYTES):
            return True, "sensitive"
        if not current.strip().startswith('"'):
            break
    if not unwrapped:
        return False, None
    if current.strip().startswith('"'):
        try:
            if isinstance(_load_privacy_json(current.strip()), str):
                return True, "sensitive"
        except (_PrivacyJsonRejected, json.JSONDecodeError, RecursionError, ValueError):
            pass
    return True, prohibited_text_reason(current)


def _json_preparse_reason(value: str) -> str | None:
    """Enforce structural and numeric budgets before allocating a JSON graph."""
    structural_tokens = 0
    number_chars = 0
    in_string = False
    escaped = False
    for character in value:
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
            number_chars = 0
            continue
        if character in "{}[],:":
            structural_tokens += 1
            number_chars = 0
            if structural_tokens > MAX_PRIVACY_JSON_NODES:
                return "sensitive"
            continue
        if character in "+-.0123456789Ee":
            number_chars += 1
            if number_chars > MAX_PRIVACY_JSON_NUMBER_CHARS:
                return "sensitive"
        elif not character.isspace():
            number_chars = 0
    return None


def _complete_json_reason(value: str) -> tuple[bool, str | None]:
    stripped = value.strip()
    if (
        not stripped
        or stripped[0] not in "[{"
    ):
        return False, None
    preparse_reason = _json_preparse_reason(stripped)
    if preparse_reason is not None:
        return True, preparse_reason
    try:
        document = _load_privacy_json(stripped)
    except _PrivacyJsonRejected:
        return True, "sensitive"
    except (json.JSONDecodeError, RecursionError, ValueError):
        return False, None
    return True, prohibited_json_reason(document)


def _dequote_malformed_projection(value: str) -> tuple[str, int]:
    """Collapse malformed key punctuation without discarding field content."""
    output: list[str] = []
    escaped_quotes = 0
    position = 0
    delimiter: str | None = None
    while position < len(value):
        character = value[position]
        if (
            character == "\\"
            and position + 1 < len(value)
            and value[position + 1] in {'"', "'"}
        ):
            escaped_quotes += 1
            position += 2
            continue
        if (
            character == "\\"
            and position + 1 < len(value)
            and (
                value[position + 1].isascii()
                and (value[position + 1].isalnum() or value[position + 1] == "_")
            )
        ):
            position += 1
            continue
        if delimiter is not None:
            if value.startswith(delimiter, position):
                position += len(delimiter)
                delimiter = None
                continue
            if character in {'"', "'"} and character != delimiter[0]:
                run = 1
                while (
                    run < 3
                    and position + run < len(value)
                    and value[position + run] == character
                ):
                    run += 1
                following = position + run
                while following < len(value) and value[following].isspace():
                    following += 1
                if following == len(value) or value[following] in ":=,}]":
                    delimiter = None
                    position += run
                    continue
            if character == "!":
                position += 1
                continue
            if (
                character == "/"
                and position > 0
                and position + 1 < len(value)
                and value[position - 1].isalnum()
                and value[position + 1].isalnum()
            ):
                position += 1
                continue
            if character.isspace():
                output.append("_")
                position += 1
                continue
            output.append(" " if character in "{}[]" else character)
            position += 1
            continue
        if character in {'"', "'"}:
            run = 1
            while (
                run < 3
                and position + run < len(value)
                and value[position + run] == character
            ):
                run += 1
            if run == 1:
                inner, after = _scan_json_quoted_token(
                    value,
                    position,
                    character,
                    MAX_PRIVACY_MALFORMED_TOKEN_CHARS,
                )
                if inner is not None and _is_safe_credential_placeholder(
                    inner.strip()
                ):
                    output.append(value[position:after])
                    position = after
                    continue
            delimiter = character * (3 if run >= 3 else run)
            position += len(delimiter)
            continue
        if character == "!":
            position += 1
            continue
        if (
            character == "/"
            and position > 0
            and position + 1 < len(value)
            and value[position - 1].isalnum()
            and value[position + 1].isalnum()
        ):
            position += 1
            continue
        output.append(character)
        position += 1
    return "".join(output), escaped_quotes


def _is_uri_double_slash(value: str, position: int) -> bool:
    """Return whether ``//`` starts a URI rather than a JSONC comment."""
    if position < 2 or value[position - 1] != ":":
        return False
    scheme_end = position - 1
    scheme_start = scheme_end
    while scheme_start > 0 and value[scheme_start - 1] in (
        string.ascii_letters + string.digits + "+.-"
    ):
        scheme_start -= 1
    scheme = value[scheme_start:scheme_end]
    if not scheme or not scheme[0].isalpha() or len(scheme) > 32:
        return False
    context = scheme_start - 1
    while context >= 0 and value[context].isspace():
        context -= 1
    return context < 0 or value[context] not in "{[,"


def _has_malformed_quote_signal(value: str) -> bool:
    """Recognise bounded quote damage that needs a dequoted recovery lane."""
    if value.count('"') % 2 or value.count("'") % 2:
        return True
    if re.search(r"([\"'])\1", value) is not None:
        return True
    if re.search(r"[A-Za-z0-9][\"'][A-Za-z0-9]", value) is not None:
        return True
    for delimiter in (":", "="):
        position = value.find(delimiter)
        while position >= 0:
            start = max(
                value.rfind("{", 0, position),
                value.rfind("[", 0, position),
                value.rfind(",", 0, position),
            )
            token = value[start + 1 : position].strip()
            if (
                len(token) >= 2
                and token[0] in {"\"", "'"}
                and token[-1] in {"\"", "'"}
                and token[0] != token[-1]
            ):
                return True
            position = value.find(delimiter, position + 1)
    return False


def _match_is_uri_scheme(match: re.Match[str]) -> bool:
    value_start = match.start("value")
    return (
        match.group("delimiter") == ":"
        and not match.groupdict().get("spacing", "")
        and match.string.startswith("//", value_start)
        and _is_uri_double_slash(match.string, value_start)
    )


def _malformed_json_projections(value: str) -> tuple[str, str, tuple[str, ...]]:
    """Strip JSONC comments and retain adjacent comment bodies as own lanes."""
    preserved: list[str] = []
    flattened: list[str] = []
    comment_groups: list[list[str]] = []
    previous_comment_end: int | None = None
    position = 0
    delimiter: str | None = None
    escaped = False
    last_nonspace: str | None = None
    trailing_alias_comment = False
    trailing_alias_comment_starts: set[int] = set()
    for match in SENSITIVE_ASSIGNMENT_TEXT.finditer(value):
        if _json_field_name(match.group("key")) != "value" or not _is_safe_credential_placeholder(
            _normalise_matched_credential_value(match.group("value"))
        ):
            continue
        comment_start = match.end("value")
        while comment_start < len(value) and value[comment_start] in " \t":
            comment_start += 1
        if value.startswith(("/*", "//"), comment_start):
            trailing_alias_comment_starts.add(comment_start)

    def record_comment(body: str, start: int, end: int) -> None:
        nonlocal previous_comment_end
        if (
            previous_comment_end is None
            or value[previous_comment_end:start].strip()
        ):
            comment_groups.append([])
        comment_groups[-1].append(body)
        previous_comment_end = end

    def flattened_comment_body(
        body: str, *, value_slot: bool, trailing_alias_value: bool
    ) -> str:
        if value_slot:
            projection = _decoded_privacy_projection(body.strip())
            if projection is None:
                return body + ","
            normalised = _normalise_matched_credential_value(projection)
            if _jsonc_comment_value_is_sensitive("password", body):
                return json.dumps(normalised, ensure_ascii=False) + ","
        if trailing_alias_value:
            projection = _decoded_privacy_projection(body.strip())
            if projection is None:
                return ',"value":"invalid",'
            normalised = _normalise_matched_credential_value(projection)
            if _jsonc_comment_value_is_sensitive("password", body):
                return ',"value":' + json.dumps(normalised, ensure_ascii=False) + ","
        match = COMMENTED_VALUE_PROPERTY_TEXT.fullmatch(body)
        if match is not None and _json_field_name(match.group("key")) == "value":
            return "," + body + ","
        if any(marker in body for marker in "{}[]"):
            return "," + body.translate(MALFORMED_COMMENT_STRUCTURE_TRANSLATION) + ","
        return ",,"

    while position < len(value):
        character = value[position]
        if delimiter is not None:
            if value.startswith(delimiter, position) and not escaped:
                preserved.append(delimiter)
                flattened.append(delimiter)
                position += len(delimiter)
                delimiter = None
                continue
            preserved.append(character)
            flattened.append(character)
            if not character.isspace():
                last_nonspace = character
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            position += 1
            continue
        if character in {'"', "'"}:
            run = 1
            while (
                run < 3
                and position + run < len(value)
                and value[position + run] == character
            ):
                run += 1
            delimiter = character * (3 if run >= 3 else 1)
            preserved.append(delimiter)
            flattened.append(delimiter)
            last_nonspace = character
            trailing_alias_comment = False
            position += len(delimiter)
            continue
        if value.startswith("/*", position):
            trailing_alias_comment = (
                trailing_alias_comment or position in trailing_alias_comment_starts
            )
            end = value.find("*/", position + 2)
            if end < 0:
                record_comment(value[position + 2 :], position, len(value))
                preserved.append(" ")
                body = value[position + 2 :]
                flattened.append(
                    flattened_comment_body(
                        body,
                        value_slot=last_nonspace in {":", "="},
                        trailing_alias_value=trailing_alias_comment,
                    )
                )
                break
            record_comment(value[position + 2 : end], position, end + 2)
            preserved.append(" ")
            body = value[position + 2 : end]
            flattened.append(
                flattened_comment_body(
                    body,
                    value_slot=last_nonspace in {":", "="},
                    trailing_alias_value=trailing_alias_comment,
                )
            )
            position = end + 2
            continue
        if value.startswith("//", position) and not _is_uri_double_slash(
            value, position
        ):
            trailing_alias_comment = (
                trailing_alias_comment or position in trailing_alias_comment_starts
            )
            end = position + 2
            while end < len(value) and value[end] not in PRIVACY_LINE_TERMINATORS:
                end += 1
            record_comment(value[position + 2 : end], position, end)
            preserved.append(" ")
            body = value[position + 2 : end]
            flattened.append(
                flattened_comment_body(
                    body,
                    value_slot=last_nonspace in {":", "="},
                    trailing_alias_value=trailing_alias_comment,
                )
            )
            if end < len(value):
                preserved.append(value[end])
                flattened.append(value[end])
                end += 1
            position = end
            continue
        preserved.append(character)
        flattened.append(character)
        if not character.isspace():
            last_nonspace = character
            trailing_alias_comment = False
        position += 1
    # Adjacent comment bodies are one disjoint lane. Joining without inserted
    # punctuation preserves credentials split across adjacent comments while
    # never correlating a comment field with an outer field.
    lanes = tuple("".join(group) for group in comment_groups if group)
    return "".join(preserved), "".join(flattened), lanes


def _malformed_projection_reason(value: str) -> str | None:
    """Classify actual malformed key/value events with per-frame aliases."""
    events: list[tuple[int, str, str]] = []
    event_set: set[tuple[int, str, str]] = set()

    def add_event(start: int, key: str, value_text: str) -> str | None:
        event = (start, key, value_text)
        if event in event_set:
            return None
        event_set.add(event)
        events.append(event)
        return (
            "sensitive"
            if len(events) > MAX_PRIVACY_MALFORMED_TOKENS
            else None
        )

    for match in OVERLONG_MALFORMED_STRUCTURAL_KEY_TEXT.finditer(value):
        key = match.group("key")
        field = _json_field_name(key)
        if field in {"name", "key", "variable", "envname", "value"} or any(
            _credential_key_kind(words, compact) is not None
            for words, compact in _credential_key_components(key)
        ):
            return "sensitive"

    for match in SENSITIVE_ASSIGNMENT_TEXT.finditer(value):
        if _match_is_uri_scheme(match) or _assignment_is_folded_uri_metadata(match):
            continue
        key = match.group("key")
        matched_value = match.group("value")
        if matched_value.lstrip().startswith(("/*", "//")):
            continue
        if add_event(match.start(), key, matched_value) is not None:
            return "sensitive"
        if _credential_assignment_is_sensitive(match):
            return "sensitive"
        field = _json_field_name(key)
        normalised_value = _normalise_matched_credential_value(matched_value)
        if (
            field in {"name", "key", "variable", "envname", "value"}
            and _is_safe_credential_placeholder(normalised_value)
            and not _safe_placeholder_has_clean_termination(match)
        ):
            return "sensitive"

    for match in MALFORMED_SPACED_ASSIGNMENT_TEXT.finditer(value):
        if _match_is_uri_scheme(match) or _assignment_is_folded_uri_metadata(match):
            continue
        key = match.group("key")
        matched_value = match.group("value")
        key_has_space = any(character.isspace() for character in key.strip())
        value_has_space = any(
            character.isspace() for character in matched_value.strip()
        )
        if not (key_has_space or value_has_space):
            continue
        if add_event(match.start(), key, matched_value) is not None:
            return "sensitive"
        if key_has_space and any(
            compact.endswith(MALFORMED_SPACED_SENSITIVE_KEY_SUFFIXES)
            and _credential_key_value_is_sensitive(key, matched_value)
            for _words, compact in _credential_key_components(key)
        ):
            return "sensitive"

    standard_key = re.compile(r"[\"']?[A-Za-z_][A-Za-z0-9_.-]{0,159}[\"']?\Z")
    for match in MALFORMED_STRUCTURAL_ASSIGNMENT_TEXT.finditer(value):
        if _match_is_uri_scheme(match) or _assignment_is_folded_uri_metadata(match):
            continue
        key = match.group("key").strip()
        matched_value = match.group("value").strip()
        if add_event(match.start(), key, matched_value) is not None:
            return "sensitive"
        if _credential_key_value_is_sensitive(key, matched_value):
            return "sensitive"

    for match in MALFORMED_RAW_ASSIGNMENT_TEXT.finditer(value):
        if _match_is_uri_scheme(match) or _assignment_is_folded_uri_metadata(match):
            continue
        key = match.group("key").strip()
        matched_value = match.group("value").strip()
        if (
            any(marker in key for marker in ("/*", "*/", "//"))
            or any(marker in matched_value for marker in ("/*", "*/", "//"))
            or (
                any(quote in key for quote in ("\"", "'"))
                and key[:1] not in {"\"", "'"}
            )
        ):
            continue
        if add_event(match.start(), key, matched_value) is not None:
            return "sensitive"
        if standard_key.fullmatch(key) is None and _credential_key_value_is_sensitive(
            key, matched_value
        ):
            return "sensitive"

    events.sort(key=lambda event: event[0])

    frames: dict[int, tuple[list[str], list[str]]] = {0: ([], [])}
    frame_parents: dict[int, int] = {}
    frame_kinds: dict[int, str] = {}
    stack: list[tuple[int, str]] = [(0, "")]
    next_frame = 1
    event_index = 0
    delimiter: str | None = None
    comment: str | None = None
    escaped = False
    skip_until = 0

    def new_frame(kind: str) -> str | None:
        nonlocal next_frame
        if next_frame > MAX_PRIVACY_MALFORMED_TOKENS:
            return "sensitive"
        frames[next_frame] = ([], [])
        frame_parents[next_frame] = stack[-1][0]
        frame_kinds[next_frame] = kind
        stack.append((next_frame, kind))
        next_frame += 1
        return "sensitive" if len(stack) > MAX_PRIVACY_JSON_DEPTH else None

    def record(key: str, value_text: str, frame: int) -> str | None:
        key = key.lstrip(":_")
        field = _json_field_name(key)
        normalised_value = _normalise_matched_credential_value(value_text)
        declarations, property_values = frames[frame]
        if field in {"name", "key", "variable", "envname"}:
            declarations.append(normalised_value)
            if len(declarations) > MAX_PRIVACY_JSON_ALIASES:
                return "sensitive"
        elif field == "value":
            property_values.append(normalised_value)
            if len(property_values) > MAX_PRIVACY_JSON_ALIASES:
                return "sensitive"
        return None

    for position, character in enumerate(value):
        if position < skip_until:
            continue
        while event_index < len(events) and events[event_index][0] == position:
            _start, key, value_text = events[event_index]
            reason = record(key, value_text, stack[-1][0])
            if reason is not None:
                return reason
            event_index += 1
        if comment == "line":
            if character in PRIVACY_LINE_TERMINATORS:
                comment = None
                stack.pop()
            continue
        if comment == "block":
            if value.startswith("*/", position):
                comment = None
                stack.pop()
                skip_until = position + 2
            continue
        if delimiter is not None:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif value.startswith(delimiter, position):
                skip_until = position + len(delimiter)
                delimiter = None
                stack.pop()
            continue
        if value.startswith("//", position) and not _is_uri_double_slash(
            value, position
        ):
            if new_frame("//") is not None:
                return "sensitive"
            comment = "line"
            skip_until = position + 2
            continue
        if value.startswith("/*", position):
            if new_frame("/*") is not None:
                return "sensitive"
            comment = "block"
            skip_until = position + 2
            continue
        if character in {'"', "'"}:
            run = 1
            while (
                run < 3
                and position + run < len(value)
                and value[position + run] == character
            ):
                run += 1
            delimiter = character * (3 if run >= 3 else 1)
            if new_frame(delimiter) is not None:
                return "sensitive"
            skip_until = position + len(delimiter)
            continue
        if character in "[{":
            if new_frame(character) is not None:
                return "sensitive"
        if (
            character in "]}"
            and len(stack) > 1
            and (
                (stack[-1][1] == "[" and character == "]")
                or (stack[-1][1] == "{" and character == "}")
            )
        ):
            stack.pop()
    while event_index < len(events):
        _start, key, value_text = events[event_index]
        reason = record(key, value_text, stack[-1][0])
        if reason is not None:
            return reason
        event_index += 1

    # A structural opener that remains unfinished is malformed rather than a
    # trustworthy scope boundary. Collapse its structural subtree into the
    # parent, including a closed child opened beneath that unfinished frame.
    # Properly closed sibling objects and arrays remain isolated.
    unfinished_structural = {
        frame for frame, kind in stack if kind in {"[", "{"}
    }
    merge_frames: set[int] = set()
    for frame, kind in frame_kinds.items():
        if kind not in {"[", "{"}:
            continue
        ancestor = frame
        while ancestor in frame_parents:
            if ancestor in unfinished_structural:
                merge_frames.add(frame)
                break
            ancestor = frame_parents[ancestor]
    for child_frame in sorted(merge_frames, reverse=True):
        parent_frame = frame_parents[child_frame]
        child_declarations, child_values = frames[child_frame]
        parent_declarations, parent_values = frames[parent_frame]
        parent_declarations.extend(child_declarations)
        parent_values.extend(child_values)
        if (
            len(parent_declarations) > MAX_PRIVACY_JSON_ALIASES
            or len(parent_values) > MAX_PRIVACY_JSON_ALIASES
        ):
            return "sensitive"

    for declarations, property_values in frames.values():
        for declared_key in declarations:
            if any(
                _json_value_is_sensitive_for_key(declared_key, property_value)
                for property_value in property_values
            ):
                return "sensitive"
    return None


def _malformed_json_reason(value: str) -> str | None:
    """Inspect malformed structured text with bounded pair-aware projections."""
    if not (
        "{" in value
        or "[" in value
        or "/*" in value
        or "//" in value
        or ((('"' in value) or ("'" in value)) and ((":" in value) or ("=" in value)))
    ):
        return None
    if len(value) > MAX_PRIVACY_MALFORMED_CHARS:
        return "sensitive"
    decoded_value = _decoded_privacy_projection(value)
    if decoded_value is None:
        return "sensitive"
    if decoded_value != value:
        decoded_reason = _malformed_json_reason(decoded_value)
        if decoded_reason is not None:
            return decoded_reason
        identity_projection = re.sub(
            r"\\(?!x[0-9A-Fa-f]{2}|u(?:[0-9A-Fa-f]{4}|"
            r"\{[0-9A-Fa-f]{1,6}\})|[0-7]{1,3})(?=[A-Za-z_])",
            "",
            value,
        )
        if identity_projection != value:
            identity_reason = _malformed_json_reason(identity_projection)
            if identity_reason is not None:
                return identity_reason
        return None
    tokens = 0
    in_token = False
    for character in value:
        token_character = character.isalnum() or character in "_-"
        if token_character and not in_token:
            tokens += 1
            if tokens > MAX_PRIVACY_MALFORMED_TOKENS:
                return "sensitive"
        in_token = token_character
    unwrapped = value.strip()
    for _ in range(MAX_PRIVACY_DECODE_PASSES + 1):
        if not unwrapped or unwrapped[0] != '"':
            break
        try:
            document = _load_privacy_json(unwrapped)
        except (_PrivacyJsonRejected, json.JSONDecodeError, RecursionError, ValueError):
            break
        if not isinstance(document, str):
            return prohibited_json_reason(document)
        if _utf8_length_exceeds(document, MAX_PRIVACY_TEXT_BYTES):
            return "sensitive"
        unwrapped = document
    else:
        if unwrapped.startswith('"'):
            return "sensitive"
    if unwrapped != value.strip():
        return prohibited_text_reason(unwrapped)

    for match in SENSITIVE_ASSIGNMENT_TEXT.finditer(value):
        key = match.group("key")
        field = _json_field_name(key)
        relevant = field in {"name", "key", "variable", "envname", "value"} or any(
            _credential_key_kind(words, compact) is not None
            for words, compact in _credential_key_components(key)
        )
        if (
            relevant
            and _is_safe_credential_placeholder(
                _normalise_matched_credential_value(match.group("value"))
            )
            and not _safe_placeholder_has_clean_termination(match)
        ):
            return "sensitive"

    preserved, flattened, comment_lanes = _malformed_json_projections(value)
    projections: tuple[str, ...] = (preserved, flattened, *comment_lanes)
    if _has_malformed_quote_signal(preserved):
        dequoted, _escaped_quotes = _dequote_malformed_projection(preserved)
        projections += (dequoted,)
    for projection in projections:
        folded = _fold_privacy_lines(projection)
        if (
            SENSITIVE_TOKEN_TEXT.search(projection)
            or SENSITIVE_TOKEN_TEXT.search(folded)
            or _contains_basic_credential(projection)
            or _contains_compact_jose_token(projection)
        ):
            return "sensitive"
        reason = _malformed_projection_reason(projection)
        if reason is not None:
            return reason
    return None


def _embedded_json_reason(value: str) -> str | None:
    """Inspect disjoint, balanced JSON candidates embedded in ordinary text."""
    start: int | None = None
    stack: list[str] = []
    string_quote: str | None = None
    comment: str | None = None
    escaped = False
    candidates = 0
    ignored_until = 0

    for position, character in enumerate(value):
        if position < ignored_until:
            continue
        if start is None:
            if character == "[":
                if position > 0 and (
                    value[position - 1].isalnum()
                    or value[position - 1] in "_]"
                ):
                    continue
            elif character != "{":
                continue
            if character == "{" and position > 0 and value[position - 1] == "$":
                placeholder = re.match(
                    r"\{[A-Za-z_][A-Za-z0-9_]*\}", value[position:]
                )
                if placeholder is not None:
                    ignored_until = position + placeholder.end()
                    continue
            if character == "{" and value.startswith("{{", position):
                placeholder = re.match(
                    r"\{\{\s*[A-Za-z_][A-Za-z0-9_.-]*\s*\}\}",
                    value[position:],
                )
                if placeholder is not None:
                    ignored_until = position + placeholder.end()
                    continue
            start = position
            stack = [character]
            string_quote = None
            comment = None
            escaped = False
            continue
        if string_quote is not None:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == string_quote:
                string_quote = None
            continue
        if comment == "line":
            if character in PRIVACY_LINE_TERMINATORS:
                comment = None
            continue
        if comment == "block":
            if character == "/" and position > 0 and value[position - 1] == "*":
                comment = None
            continue
        if character == "/" and position + 1 < len(value):
            following = value[position + 1]
            if following == "/" and not _is_uri_double_slash(value, position):
                comment = "line"
                continue
            if following == "*":
                comment = "block"
                continue
        if character in {'"', "'"}:
            string_quote = character
            continue
        if character in "[{":
            stack.append(character)
            if len(stack) > MAX_PRIVACY_JSON_DEPTH:
                return "sensitive"
            continue
        if character not in "]}":
            continue
        if not stack or (stack[-1] == "[" and character != "]") or (
            stack[-1] == "{" and character != "}"
        ):
            # Keep the outer candidate intact. A mismatched closer is ordinary
            # malformed content; resetting here can split a declaration from
            # its later value field and make the privacy check fail open.
            continue
        stack.pop()
        if stack:
            continue
        candidates += 1
        candidate = value[start : position + 1]
        start = None
        comment = None
        if candidates > MAX_PRIVACY_EMBEDDED_JSON_CANDIDATES:
            return "sensitive"
        if len(candidate) > MAX_PRIVACY_INLINE_JSON_CHARS:
            reason = _malformed_json_reason(candidate)
            if reason is not None:
                return reason
            continue
        preparse_reason = _json_preparse_reason(candidate)
        if preparse_reason is not None:
            return preparse_reason
        try:
            document = _load_privacy_json(candidate)
        except _PrivacyJsonRejected:
            return "sensitive"
        except (json.JSONDecodeError, RecursionError, ValueError):
            decoded_candidate = candidate
            for _ in range(MAX_PRIVACY_DECODE_PASSES + 1):
                decoded = _decode_privacy_escapes_once(decoded_candidate)
                if decoded == decoded_candidate:
                    break
                decoded_candidate = decoded
            if decoded_candidate != candidate:
                decoded_complete, decoded_reason = _complete_json_reason(
                    decoded_candidate
                )
                if decoded_reason is not None:
                    return decoded_reason
                if decoded_complete:
                    continue
            reason = _malformed_json_reason(candidate)
            if reason is not None:
                return reason
            continue
        reason = prohibited_json_reason(document)
        if reason is not None:
            return reason

    if start is not None:
        candidate = value[start:]
        decoded_candidate = candidate
        for _ in range(MAX_PRIVACY_DECODE_PASSES + 1):
            decoded = _decode_privacy_escapes_once(decoded_candidate)
            if decoded == decoded_candidate:
                break
            decoded_candidate = decoded
        if decoded_candidate != candidate:
            decoded_complete, decoded_reason = _complete_json_reason(decoded_candidate)
            if decoded_reason is not None:
                return decoded_reason
            if decoded_complete:
                return None
            if decoded_candidate.endswith(('"', "'")):
                decoded_complete, decoded_reason = _complete_json_reason(
                    decoded_candidate[:-1]
                )
                if decoded_reason is not None:
                    return decoded_reason
                if decoded_complete:
                    return None
        reason = _malformed_json_reason(candidate)
        if reason is not None:
            return reason
    return None


def _scan_jose_segment(value: str, start: int) -> int:
    position = start
    while position < len(value) and value[position] in _JOSE_CHARS:
        position += 1
    return position


def _jose_header_is_json_object(value: str, start: int, end: int) -> bool:
    length = end - start
    if length < 3:
        return False
    if length >= 13 and value.startswith("eyJ", start, end):
        return True
    if length > MAX_JOSE_HEADER_PROBE_CHARS:
        probe_length = MAX_JOSE_HEADER_PROBE_CHARS - (
            MAX_JOSE_HEADER_PROBE_CHARS % 4
        )
        encoded = value[start : start + probe_length]
        try:
            decoded = base64.b64decode(encoded, altchars=b"-_", validate=True)
        except (binascii.Error, ValueError):
            return False
        stripped = decoded.lstrip(b" \t\r\n")
        return not stripped or stripped.startswith(b"{")
    encoded = value[start:end]
    padded = encoded + "=" * (-length % 4)
    try:
        decoded = base64.b64decode(padded, altchars=b"-_", validate=True)
        document = json.loads(decoded.decode("utf-8"))
    except (binascii.Error, UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return False
    return isinstance(document, dict)


def _contains_compact_jose_token(value: str) -> bool:
    """Recognise compact JOSE tokens with a JSON object header in linear time."""
    if "." not in value:
        return False
    position = 0
    while position < len(value):
        while position < len(value) and value[position] not in _JOSE_CHARS:
            position += 1
        header_start = position
        header_end = _scan_jose_segment(value, header_start)
        if header_end == header_start or header_end >= len(value) or value[header_end] != ".":
            position = max(header_end, header_start + 1)
            continue
        payload_start = header_end + 1
        payload_end = _scan_jose_segment(value, payload_start)
        if payload_end >= len(value) or value[payload_end] != ".":
            position = payload_start
            continue
        if _jose_header_is_json_object(value, header_start, header_end):
            return True
        position = payload_start
    return False


def _contains_absolute_parent_traversal(value: str) -> bool:
    """Recognise an absolute path with a parent component in one forward scan."""
    position = 0
    while position < len(value):
        root = value.find("/", position)
        if root < 0:
            return False
        previous = value[root - 1] if root else ""
        prefix = value[max(0, root - 6) : root].lower()
        if previous in _PATH_BOUNDARY_CHARS or prefix.endswith(("http:", "https:")):
            position = root + 1
            continue
        terminator = _PATH_SCAN_TERMINATOR_TEXT.search(value, root + 1)
        end = terminator.start() if terminator is not None else len(value)
        parent = value.find("/..", root, end)
        while parent >= 0:
            after = parent + 3
            if after == end or value[after] == "/":
                return True
            parent = value.find("/..", parent + 3, end)
        position = end + 1
    return False


def _assignment_starts_in_uri(value: str, start: int) -> bool:
    """Return whether an assignment-looking key starts inside one URI token."""
    token_start = start
    while (
        token_start > 0
        and not value[token_start - 1].isspace()
        and value[token_start - 1] not in "\"'`,;{}[]()<>"
    ):
        token_start -= 1
    scheme = value.find("://", token_start, start)
    return scheme >= 0 and not any(
        character.isspace() for character in value[scheme:start]
    )


def _assignment_is_folded_uri_metadata(match: re.Match[str]) -> bool:
    """Ignore only URI path keys formed by folding a later ``value`` field."""
    if not _assignment_starts_in_uri(match.string, match.start("key")):
        return False
    compact = re.sub(r"[^A-Za-z0-9]", "", match.group("key")).lower()
    return compact.endswith("value")


SENSITIVE_SYNTAX_HINT_TEXT = re.compile(
    r"[=:/?&\[\]{}@.+\-]|Authorization", re.IGNORECASE
)


def _contains_sensitive_structured_text(
    candidate: str, *, complete_json: bool
) -> bool:
    return bool(
        _lexical_json_reason(candidate)
        or (not complete_json and _embedded_json_reason(candidate))
        or _malformed_json_reason(candidate)
        or OVERLONG_ASSIGNMENT_KEY_TEXT.search(candidate)
        or OVERLONG_BRACKETED_KEY_TEXT.search(candidate)
        or OVERLONG_BRACKETED_KEY_DEPTH_TEXT.search(candidate)
        or OVERLONG_BRACKETED_BASE_TEXT.search(candidate)
        or OVERLONG_PROJECTED_AUTHORIZATION_TEXT.search(candidate)
        or OVERLONG_SENSITIVE_QUERY_TEXT.search(candidate)
        or OVERLONG_QUERY_COMPONENT_TEXT.search(candidate)
        or OVERLONG_QUERY_KEY_TEXT.search(candidate)
        or OVERLONG_CLI_KEY_TEXT.search(candidate)
        or any(
            _authorization_value_is_sensitive(match)
            for match in PROJECTED_AUTHORIZATION_TEXT.finditer(candidate)
        )
        or any(
            not _assignment_is_folded_uri_metadata(match)
            and _credential_assignment_is_sensitive(match)
            for match in SENSITIVE_ASSIGNMENT_TEXT.finditer(candidate)
        )
        or any(
            _sensitive_query_value(match)
            for match in SENSITIVE_QUERY_TEXT.finditer(candidate)
        )
        or any(
            _sensitive_cli_value(match)
            for match in CLI_CREDENTIAL_TEXT.finditer(candidate)
        )
    )


def prohibited_text_reason(value: str) -> str | None:
    """Classify high-specificity private paths and credential-shaped values."""
    if _utf8_length_exceeds(value, MAX_PRIVACY_TEXT_BYTES):
        return "sensitive"
    if _contains_unsafe_privacy_control(value):
        return "sensitive"
    if "\\" * (MAX_PRIVACY_BACKSLASH_RUN + 1) in value:
        return "sensitive"
    wrapped_json_string, wrapped_json_reason = _top_level_json_string_reason(value)
    if wrapped_json_string:
        return wrapped_json_reason
    complete_json, complete_json_reason = _complete_json_reason(value)
    if complete_json_reason is not None:
        return "sensitive"
    if complete_json:
        return None
    initial_trusted_cpe_tokens = _trusted_complete_cpe_path_tokens(value)
    if initial_trusted_cpe_tokens is None:
        return "sensitive"
    trusted_cpe_tokens = set(initial_trusted_cpe_tokens)
    if _contains_private_path(
        value, trusted_cpe_tokens=frozenset(trusted_cpe_tokens)
    ) or _contains_absolute_parent_traversal(value):
        return "private-path"
    if _lexical_json_reason(value) or (
        not complete_json and _embedded_json_reason(value)
    ):
        return "sensitive"
    candidate = value
    for pass_index in range(MAX_PRIVACY_DECODE_PASSES + 1):
        if pass_index:
            candidate_trusted_cpe_tokens = _trusted_complete_cpe_path_tokens(candidate)
            if candidate_trusted_cpe_tokens is None:
                return "sensitive"
            trusted_cpe_tokens.update(candidate_trusted_cpe_tokens)
        decoded = _decode_privacy_escapes_once(candidate)
        if decoded == candidate:
            break
        candidate = decoded
    else:
        if _decode_privacy_escapes_once(candidate) != candidate:
            return "sensitive"
    if candidate != value:
        if _contains_unsafe_privacy_control(candidate):
            return "sensitive"
        if _contains_private_path(
            candidate, trusted_cpe_tokens=frozenset(trusted_cpe_tokens)
        ) or _contains_absolute_parent_traversal(candidate):
            return "private-path"
    if (
        SENSITIVE_TOKEN_TEXT.search(candidate)
        or _contains_basic_credential(candidate)
        or _contains_compact_jose_token(candidate)
    ):
        return "sensitive"
    if SENSITIVE_SYNTAX_HINT_TEXT.search(
        candidate
    ) and _contains_sensitive_structured_text(candidate, complete_json=complete_json):
        return "sensitive"
    unfolded = _fold_privacy_lines(candidate)
    if unfolded != candidate:
        path_projection = candidate
        if "//" in candidate or "/*" in candidate:
            path_projection, _flattened, _comment_lanes = _malformed_json_projections(
                candidate
            )
        unfolded_path = _fold_privacy_lines(path_projection)
        if _contains_private_path(
            unfolded_path, trusted_cpe_tokens=frozenset(trusted_cpe_tokens)
        ) or _contains_absolute_parent_traversal(unfolded_path):
            return "private-path"
        preserved = candidate
        if "//" in candidate:
            preserved, _flattened, _comment_lanes = _malformed_json_projections(
                candidate
            )
        if (
            preserved == candidate
            and SENSITIVE_SYNTAX_HINT_TEXT.search(unfolded)
            and _contains_sensitive_structured_text(
                unfolded, complete_json=complete_json
            )
        ):
            return "sensitive"
        if (
            SENSITIVE_TOKEN_TEXT.search(unfolded)
            or _contains_basic_credential(unfolded)
            or _contains_compact_jose_token(unfolded)
        ):
            return "sensitive"
    return None

MAX_CONTEXT_FILES = 20_000
MAX_CONTEXT_BYTES = 256 * 1024 * 1024
MAX_OCI_FILES = 20_000
MAX_OCI_BYTES = 768 * 1024 * 1024
MAX_LAYER_EXPANDED_BYTES = 512 * 1024 * 1024
MAX_ROOTFS_EXPANDED_BYTES = 2 * 1024 * 1024 * 1024
MAX_LAYER_MEMBERS = 200_000
MAX_JSON_BYTES = 4 * 1024 * 1024
MAX_CHECKSUM_BYTES = 4 * 1024

CONTEXT_FILES = (
    "LICENSE",
    "VERSION",
    "package.json",
    "pnpm-lock.yaml",
    "pnpm-workspace.yaml",
    "tsconfig.base.json",
    "apps/mcp-gateway/Containerfile",
    "apps/mcp-gateway/Containerfile.dockerignore",
    "packages/tool-registry/package.json",
)
CONTEXT_ROOTS = (
    "apps/mcp-gateway",
    "packages/authority-context",
    "packages/contracts",
    "packages/evidence",
    "packages/policy-client",
    "packages/provider-adapter-sdk",
    "schemas",
)
ADMITTED_PACKAGE_MANIFESTS = (
    "package.json",
    "apps/mcp-gateway/package.json",
    "packages/authority-context/package.json",
    "packages/contracts/package.json",
    "packages/evidence/package.json",
    "packages/policy-client/package.json",
    "packages/provider-adapter-sdk/package.json",
    "packages/tool-registry/package.json",
)
FORBIDDEN_PACKAGE_LIFECYCLE_SCRIPTS = frozenset(
    {
        "preinstall",
        "install",
        "postinstall",
        "preprepare",
        "prepare",
        "postprepare",
        "prepublish",
        "prepublishOnly",
        "publish",
        "postpublish",
        "prepack",
        "postpack",
        "dependencies",
    }
)
BUILDER_MANIFEST_COPY_INSTRUCTIONS = (
    "COPY package.json pnpm-lock.yaml pnpm-workspace.yaml tsconfig.base.json VERSION LICENSE ./",
    "COPY apps/mcp-gateway/package.json apps/mcp-gateway/package.json",
    "COPY packages/authority-context/package.json packages/authority-context/package.json",
    "COPY packages/contracts/package.json packages/contracts/package.json",
    "COPY packages/evidence/package.json packages/evidence/package.json",
    "COPY packages/policy-client/package.json packages/policy-client/package.json",
    (
        "COPY packages/provider-adapter-sdk/package.json "
        "packages/provider-adapter-sdk/package.json"
    ),
    "COPY packages/tool-registry/package.json packages/tool-registry/package.json",
)
BUILDER_SOURCE_COPY_INSTRUCTIONS = (
    "COPY apps/mcp-gateway/ apps/mcp-gateway/",
    "COPY packages/authority-context/ packages/authority-context/",
    "COPY packages/contracts/ packages/contracts/",
    "COPY packages/evidence/ packages/evidence/",
    "COPY packages/policy-client/ packages/policy-client/",
    "COPY packages/provider-adapter-sdk/ packages/provider-adapter-sdk/",
    "COPY schemas/ schemas/",
    "COPY artifacts/okf/ artifacts/okf/",
)
BUILDER_COPY_INSTRUCTIONS = (
    *BUILDER_MANIFEST_COPY_INSTRUCTIONS,
    *BUILDER_SOURCE_COPY_INSTRUCTIONS,
)
IGNORED_DIRECTORY_NAMES = frozenset({"dist", "node_modules"})
IGNORED_FILE_NAMES = frozenset({".DS_Store"})
OKF_ROOT = ROOT / "artifacts" / "okf"
OKF_ALWAYS_FILES = frozenset({".okf-generated", "CHECKSUMS.sha256"})


@dataclass(frozen=True)
class SourceIdentity:
    revision: str
    version: str
    source_date_epoch: int
    created: str
    clean: bool


@dataclass(frozen=True)
class OciInspection:
    archive_sha256: str
    archive_size: int
    index_sha256: str
    manifest_digest: str
    config_digest: str
    layer_digests: tuple[str, ...]
    rootfs_diff_ids: tuple[str, ...]
    platform: str
    labels: dict[str, str]


def run(
    arguments: Iterable[str],
    *,
    capture: bool = False,
    discard_output: bool = False,
    timeout: int = 30 * 60,
) -> subprocess.CompletedProcess[str]:
    if capture and discard_output:
        raise ValueError("command output cannot be captured and discarded")
    return subprocess.run(
        tuple(arguments),
        cwd=ROOT,
        check=True,
        capture_output=capture,
        stdout=subprocess.DEVNULL if discard_output else None,
        stderr=subprocess.DEVNULL if discard_output else None,
        text=True,
        timeout=timeout,
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def read_bounded_regular_file(
    path: Path, *, maximum_bytes: int, label: str
) -> bytes:
    """Read one bounded regular file without following a symbolic link."""
    if maximum_bytes < 1:
        raise ValueError(f"{label} has an invalid byte bound")
    try:
        metadata = path.lstat()
    except OSError as error:
        raise ValueError(f"{label} is unavailable") from error
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISREG(metadata.st_mode)
        or metadata.st_size < 1
        or metadata.st_size > maximum_bytes
    ):
        raise ValueError(f"{label} is not a bounded regular file")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError(f"{label} could not be opened safely") from error
    try:
        opened = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened.st_mode)
            or opened.st_dev != metadata.st_dev
            or opened.st_ino != metadata.st_ino
            or opened.st_size != metadata.st_size
        ):
            raise ValueError(f"{label} changed while it was opened")
        raw = bytearray()
        while len(raw) <= maximum_bytes:
            chunk = os.read(descriptor, min(1024 * 1024, maximum_bytes + 1 - len(raw)))
            if not chunk:
                break
            raw.extend(chunk)
        closed = os.fstat(descriptor)
        if (
            closed.st_dev != opened.st_dev
            or closed.st_ino != opened.st_ino
            or closed.st_size != opened.st_size
            or len(raw) != opened.st_size
            or len(raw) > maximum_bytes
        ):
            raise ValueError(f"{label} changed or exceeded its byte bound while reading")
        return bytes(raw)
    finally:
        os.close(descriptor)


def parse_bounded_json_object(
    raw: bytes, *, maximum_bytes: int, label: str
) -> dict[str, Any]:
    """Parse one bounded UTF-8 JSON object and reject ambiguous JSON forms."""
    if not raw or len(raw) > maximum_bytes:
        raise ValueError(f"{label} is empty or exceeds its JSON byte bound")

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{label} contains a duplicate JSON member: {key}")
            result[key] = value
        return result

    def reject_constant(value: str) -> None:
        raise ValueError(f"{label} contains a non-JSON numeric constant: {value}")

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=reject_duplicates,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as error:
        raise ValueError(f"{label} is not bounded UTF-8 JSON") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} is not a JSON object")
    return value


def source_identity(*, allow_dirty: bool = False) -> SourceIdentity:
    revision = run(("git", "rev-parse", "HEAD"), capture=True).stdout.strip()
    if COMMIT_RE.fullmatch(revision) is None:
        raise ValueError("gateway image source revision must be a full lower-case Git commit")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if VERSION_RE.fullmatch(version) is None:
        raise ValueError("gateway image product version must be stable semantic version text")
    epoch_text = run(("git", "show", "-s", "--format=%ct", revision), capture=True).stdout.strip()
    if not epoch_text.isascii() or not epoch_text.isdigit():
        raise ValueError("gateway image source commit time is invalid")
    epoch = int(epoch_text)
    created = datetime.fromtimestamp(epoch, UTC).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )
    status = run(
        ("git", "status", "--porcelain=v1", "--untracked-files=all"), capture=True
    ).stdout
    clean = status == ""
    if not clean and not allow_dirty:
        raise ValueError("exact-source gateway image construction requires a clean worktree")
    return SourceIdentity(revision, version, epoch, created, clean)


def _safe_context_file(path: Path, logical: str) -> tuple[str, str, int]:
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise ValueError(f"gateway build context must contain regular files only: {logical}")
    if metadata.st_nlink != 1:
        raise ValueError(f"gateway build context must not contain hard links: {logical}")
    return logical, sha256_file(path), metadata.st_size


def _is_context_path(logical: str) -> bool:
    return logical in CONTEXT_FILES or any(
        logical == root or logical.startswith(f"{root}/") for root in CONTEXT_ROOTS
    )


def _git_tracked_context_paths() -> set[str]:
    result = subprocess.run(
        (
            "git",
            "ls-files",
            "--cached",
            "-z",
            "--",
            *CONTEXT_FILES,
            *CONTEXT_ROOTS,
        ),
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    paths: set[str] = set()
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        try:
            logical = raw.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("gateway tracked context path is not UTF-8") from error
        if not _is_context_path(logical):
            raise ValueError(f"Git returned a path outside the gateway context: {logical}")
        if logical in paths:
            raise ValueError(f"gateway tracked context contains a duplicate path: {logical}")
        paths.add(logical)
    missing = sorted(set(CONTEXT_FILES) - paths)
    if missing:
        raise ValueError(
            "gateway build inputs must be Git tracked before construction: "
            + ", ".join(missing)
        )
    return paths


def _okf_projection_paths() -> set[str]:
    checksum_path = OKF_ROOT / "CHECKSUMS.sha256"
    try:
        checksum_text = checksum_path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError) as error:
        raise ValueError("the canonical OKF projection must exist before image construction") from error
    relative_paths: set[str] = set(OKF_ALWAYS_FILES)
    for line in checksum_text.splitlines(keepends=True):
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)\n", line)
        if match is None:
            raise ValueError("the OKF projection checksum ledger is invalid")
        relative = _safe_tar_path(match.group(2))
        if relative in relative_paths:
            raise ValueError(f"the OKF projection repeats an output: {relative}")
        output = OKF_ROOT / relative
        if sha256_file(output) != match.group(1):
            raise ValueError(f"the OKF projection output differs from its checksum: {relative}")
        relative_paths.add(relative)
    realised: set[str] = set()
    for current, directories, names in os.walk(OKF_ROOT, followlinks=False):
        directories.sort()
        names.sort()
        current_path = Path(current)
        for directory in directories:
            if stat.S_ISLNK((current_path / directory).lstat().st_mode):
                raise ValueError("the OKF projection contains a symbolic-link directory")
        for name in names:
            path = current_path / name
            relative = path.relative_to(OKF_ROOT).as_posix()
            _safe_context_file(path, f"artifacts/okf/{relative}")
            realised.add(relative)
    if realised != relative_paths:
        missing = sorted(relative_paths - realised)
        extra = sorted(realised - relative_paths)
        raise ValueError(
            f"the OKF projection inventory is not closed (missing={missing}, extra={extra})"
        )
    return {f"artifacts/okf/{relative}" for relative in relative_paths}


def select_build_context_paths(
    tracked_paths: set[str], generated_paths: set[str]
) -> list[str]:
    admitted = tracked_paths | generated_paths
    for logical in admitted:
        name = PurePosixPath(logical).name
        if name == ".env" or name.startswith(".env."):
            raise ValueError(f"gateway build context rejects environment file: {logical}")
    return sorted(admitted)


def build_context_inventory() -> list[tuple[str, str, int]]:
    inventory: list[tuple[str, str, int]] = []
    paths = select_build_context_paths(
        _git_tracked_context_paths(), _okf_projection_paths()
    )
    for logical in paths:
        name = PurePosixPath(logical).name
        if name in IGNORED_FILE_NAMES or name.endswith(".tsbuildinfo"):
            raise ValueError(f"gateway tracked context contains a forbidden generated file: {logical}")
        if any(part in IGNORED_DIRECTORY_NAMES for part in PurePosixPath(logical).parts):
            raise ValueError(f"gateway tracked context contains a forbidden directory: {logical}")
        inventory.append(_safe_context_file(ROOT / logical, logical))
        if len(inventory) > MAX_CONTEXT_FILES:
            raise ValueError("gateway build context exceeds its file bound")
    inventory.sort(key=lambda item: item[0])
    if len({item[0] for item in inventory}) != len(inventory):
        raise ValueError("gateway build context contains duplicate paths")
    if sum(item[2] for item in inventory) > MAX_CONTEXT_BYTES:
        raise ValueError("gateway build context exceeds its byte bound")
    return inventory


def build_context_manifest_bytes(inventory: Iterable[tuple[str, str, int]]) -> bytes:
    rows = [f"{digest}  {path}\n" for path, digest, _ in inventory]
    return "".join(rows).encode("utf-8")


def materialise_build_context(
    inventory: Iterable[tuple[str, str, int]], destination: Path
) -> None:
    destination.mkdir(mode=0o700, parents=True, exist_ok=False)
    for logical, expected_digest, expected_size in inventory:
        source = ROOT / logical
        target = destination / logical
        target.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        target.chmod(0o644)
        if target.stat().st_size != expected_size or sha256_file(target) != expected_digest:
            raise ValueError(f"materialised gateway context differs from inventory: {logical}")


def _logical_containerfile_instructions(text: str) -> list[str]:
    instructions: list[str] = []
    pending = ""
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not pending and (not stripped or stripped.startswith("#")):
            continue
        if not pending and not re.match(r"^[A-Z]+(?:\s|$)", stripped):
            raise ValueError(f"gateway Containerfile has an unparseable instruction: {raw_line}")
        continued = stripped.endswith("\\")
        piece = stripped[:-1].rstrip() if continued else stripped
        pending = f"{pending} {piece}".strip()
        if not continued:
            instructions.append(re.sub(r"\s+", " ", pending))
            pending = ""
    if pending:
        raise ValueError("gateway Containerfile ends with an incomplete instruction")
    return instructions


def parse_gateway_containerfile_pins(text: str) -> dict[str, str]:
    instructions = _logical_containerfile_instructions(text)
    node_args = [item for item in instructions if item.startswith("ARG NODE_BASE")]
    expected_arg = f'ARG NODE_BASE="{NODE_BASE_REFERENCE}"'
    if node_args != [expected_arg]:
        raise ValueError("gateway Containerfile must declare one exact active Node base ARG")
    from_instructions = [item for item in instructions if item.startswith("FROM ")]
    if from_instructions != [
        "FROM ${NODE_BASE} AS builder",
        "FROM ${NODE_BASE} AS runtime",
    ]:
        raise ValueError("gateway Containerfile FROM instructions differ from the fixed Node base")
    if any(item.startswith("ADD ") for item in instructions):
        raise ValueError("gateway Containerfile must not admit local or remote ADD inputs")
    builder_end = instructions.index("FROM ${NODE_BASE} AS runtime")
    builder_instructions = instructions[:builder_end]
    builder_copies = tuple(
        item for item in builder_instructions if item.startswith("COPY ")
    )
    if builder_copies != BUILDER_COPY_INSTRUCTIONS:
        raise ValueError(
            "gateway builder COPY inventory or order differs from the closed contract"
        )
    active = "\n".join(instructions)
    pack_operands = re.findall(r"\bnpm pack ([^ ]+)", active)
    if pack_operands != [f"pnpm@{PNPM_VERSION}"]:
        raise ValueError("gateway Containerfile must fetch one exact pnpm package")
    if active.count(PNPM_SHA512) != 1:
        raise ValueError("gateway Containerfile must contain one exact pnpm checksum operand")
    tarball = f"/tmp/pnpm/pnpm-{PNPM_VERSION}.tgz"
    if active.count(tarball) != 2:
        raise ValueError("gateway Containerfile pnpm tarball operands are not closed")
    if f"npm install --global --ignore-scripts {tarball}" not in active:
        raise ValueError("gateway Containerfile pnpm installation operand differs")
    if f"test \"$(pnpm --version)\" = '{PNPM_VERSION}'" not in active:
        raise ValueError("gateway Containerfile does not verify the exact pnpm version")
    fetch_instruction = "RUN pnpm fetch --frozen-lockfile"
    deploy_instruction = (
        "RUN pnpm --filter @gis-ai-go/mcp-gateway deploy --prod --legacy --ignore-scripts "
        "/runtime/apps/mcp-gateway"
    )
    bootstrap_instruction = (
        "RUN mkdir -p /opt/pnpm/bin /tmp/pnpm "
        f"&& npm pack pnpm@{PNPM_VERSION} --ignore-scripts --pack-destination /tmp/pnpm "
        "&& printf '%s %s\\n' "
        f"'{PNPM_SHA512}' '/tmp/pnpm/pnpm-{PNPM_VERSION}.tgz' "
        "| sha512sum --check --strict "
        f"&& npm install --global --ignore-scripts /tmp/pnpm/pnpm-{PNPM_VERSION}.tgz "
        f"&& test \"$(pnpm --version)\" = '{PNPM_VERSION}' && rm -rf /tmp/pnpm"
    )
    manifest_copies = set(BUILDER_MANIFEST_COPY_INSTRUCTIONS)
    non_manifest_source_copy_indexes = [
        index
        for index, item in enumerate(builder_instructions)
        if item.startswith("COPY ") and item not in manifest_copies
    ]
    if not non_manifest_source_copy_indexes:
        raise ValueError("gateway Containerfile lacks its broad source COPY inventory")
    source_copy_cutoff = min(non_manifest_source_copy_indexes)
    deploy_indexes = [
        index for index, item in enumerate(builder_instructions) if item == deploy_instruction
    ]
    fetch_indexes = [
        index for index, item in enumerate(builder_instructions) if item == fetch_instruction
    ]
    if (
        len(fetch_indexes) != 1
        or len(deploy_indexes) != 1
        or fetch_indexes[0] >= deploy_indexes[0]
        or deploy_indexes[0] >= source_copy_cutoff
    ):
        raise ValueError(
            "gateway dependency fetch and deploy must precede broad source copies"
        )
    networked_before_source = tuple(
        item
        for item in builder_instructions[:source_copy_cutoff]
        if item.startswith("RUN ") and not item.startswith("RUN --network=none ")
    )
    if networked_before_source != (
        bootstrap_instruction,
        fetch_instruction,
        deploy_instruction,
    ):
        raise ValueError(
            "gateway pre-source networked RUN inventory differs from the closed contract"
        )
    bootstrap_index = builder_instructions.index(bootstrap_instruction)
    manifest_copy_indexes = [
        builder_instructions.index(item) for item in BUILDER_MANIFEST_COPY_INSTRUCTIONS
    ]
    if max(manifest_copy_indexes) >= bootstrap_index:
        raise ValueError(
            "gateway package and lock manifests must precede dependency networking"
        )
    post_copy = instructions[source_copy_cutoff + 1 :]
    if any(
        item.startswith("RUN ") and not item.startswith("RUN --network=none ")
        for item in post_copy
    ):
        raise ValueError("every gateway RUN after broad source copy must disable networking")
    build_runs = [item for item in post_copy if "pnpm install" in item]
    if len(build_runs) != 1 or not build_runs[0].startswith("RUN --network=none "):
        raise ValueError("gateway install/build must run with networking disabled")
    if "pnpm install --offline --frozen-lockfile --ignore-scripts" not in build_runs[0]:
        raise ValueError("gateway production install must be offline and ignore scripts")
    required_workspace_copies = (
        "cp -a apps/mcp-gateway/dist /runtime/apps/mcp-gateway/dist",
        "cp -a packages/authority-context/dist /runtime/apps/mcp-gateway/"
        "node_modules/@gis-ai-go/authority-context/dist",
        "cp -a packages/contracts/dist /runtime/apps/mcp-gateway/"
        "node_modules/@gis-ai-go/contracts/dist",
        "cp -a packages/evidence/dist /runtime/apps/mcp-gateway/"
        "node_modules/@gis-ai-go/evidence/dist",
        "cp -a packages/policy-client/dist /runtime/apps/mcp-gateway/"
        "node_modules/@gis-ai-go/policy-client/dist",
        "cp -a packages/provider-adapter-sdk/dist /runtime/apps/mcp-gateway/"
        "node_modules/@gis-ai-go/provider-adapter-sdk/dist",
    )
    if any(value not in build_runs[0] for value in required_workspace_copies):
        raise ValueError("gateway runtime lacks a reviewed workspace build output")
    runtime_runs = [item for item in instructions if "mkdir -p /nonexistent" in item]
    if len(runtime_runs) != 1 or not runtime_runs[0].startswith("RUN --network=none "):
        raise ValueError("gateway runtime mutation must run with networking disabled")
    return {
        "node_reference": NODE_BASE_REFERENCE,
        "pnpm_version": PNPM_VERSION,
        "pnpm_sha512": PNPM_SHA512,
    }


def verify_gateway_dockerignore(text: str) -> None:
    rules = [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    if not rules or rules[0] != "**":
        raise ValueError("gateway Dockerignore must begin from a deny-all rule")
    if rules[-2:] != ["**/.env", "**/.env.*"]:
        raise ValueError("gateway Dockerignore must end with closed environment-file exclusions")
    for required in ("**/dist/", "**/node_modules/", "**/*.tsbuildinfo"):
        if required not in rules:
            raise ValueError(f"gateway Dockerignore lacks required exclusion: {required}")


def verify_root_package_manager(package: Any) -> None:
    if not isinstance(package, dict) or package.get("packageManager") != f"pnpm@{PNPM_VERSION}":
        raise ValueError("root packageManager differs from the reviewed pnpm identity")


def verify_package_manifest_lifecycle_policy(
    package: Any, *, logical_path: str
) -> None:
    """Reject install, packing and publication hooks in an admitted manifest."""
    if not isinstance(package, dict):
        raise ValueError(f"admitted package manifest must be an object: {logical_path}")
    scripts = package.get("scripts")
    if scripts is None:
        return
    if not isinstance(scripts, dict) or not all(
        isinstance(name, str) and isinstance(command, str)
        for name, command in scripts.items()
    ):
        raise ValueError(f"admitted package scripts must be string pairs: {logical_path}")
    lifecycle_hooks = sorted(FORBIDDEN_PACKAGE_LIFECYCLE_SCRIPTS.intersection(scripts))
    if lifecycle_hooks:
        raise ValueError(
            f"admitted package manifest contains lifecycle hooks: {logical_path}: "
            + ", ".join(lifecycle_hooks)
        )


def _admitted_package_manifest_paths() -> tuple[str, ...]:
    paths = tuple(
        sorted(
            logical
            for logical in _git_tracked_context_paths()
            if PurePosixPath(logical).name == "package.json"
        )
    )
    missing = sorted(set(ADMITTED_PACKAGE_MANIFESTS) - set(paths))
    if missing:
        raise ValueError(
            "gateway build context lacks required package manifests: "
            + ", ".join(missing)
        )
    return paths


def verify_checked_inputs(source: SourceIdentity) -> None:
    containerfile = CONTAINERFILE.read_text(encoding="utf-8")
    parse_gateway_containerfile_pins(containerfile)
    packages: dict[str, Any] = {}
    for logical_path in _admitted_package_manifest_paths():
        try:
            package = json.loads((ROOT / logical_path).read_bytes())
        except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError(f"admitted package manifest is invalid: {logical_path}") from error
        verify_package_manifest_lifecycle_policy(package, logical_path=logical_path)
        packages[logical_path] = package
    verify_root_package_manager(packages["package.json"])
    try:
        verify_gateway_dockerignore(DOCKERIGNORE.read_text(encoding="utf-8"))
    except (FileNotFoundError, UnicodeDecodeError) as error:
        raise ValueError("gateway-specific Docker build-context policy is missing") from error
    receipt_path = ROOT / "artifacts" / "okf" / "build-receipt.json"
    try:
        receipt = json.loads(receipt_path.read_bytes())
    except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("the checked OKF build must exist before image construction") from error
    if (
        not isinstance(receipt, dict)
        or receipt.get("revision") != source.revision
        or receipt.get("version") != source.version
    ):
        raise ValueError("the checked OKF build identity differs from the image source")


def verify_pinned_builder() -> None:
    try:
        details = run(
            ("docker", "buildx", "inspect", BUILDER_NAME), capture=True
        ).stdout
        container = json.loads(
            run(
                ("docker", "inspect", f"buildx_buildkit_{BUILDER_NAME}0"),
                capture=True,
            ).stdout
        )
        image = json.loads(
            run(
                ("docker", "image", "inspect", BUILDKIT_REFERENCE),
                capture=True,
            ).stdout
        )
    except (subprocess.CalledProcessError, json.JSONDecodeError) as error:
        raise ValueError(
            "the exact pinned GIS AI GO BuildKit builder is unavailable"
        ) from error
    required = (
        rf"^Name:\s+{re.escape(BUILDER_NAME)}\s*$",
        r"^Driver:\s+docker-container\s*$",
        rf'^Driver Options:\s+image="{re.escape(BUILDKIT_REFERENCE)}"\s*$',
        r"^Status:\s+running\s*$",
        rf"^BuildKit version:\s+{re.escape(BUILDKIT_VERSION)}\s*$",
    )
    if any(re.search(pattern, details, re.MULTILINE) is None for pattern in required):
        raise ValueError("the active gateway builder differs from the pinned identity")

    if (
        not isinstance(container, list)
        or len(container) != 1
        or not isinstance(container[0], dict)
        or not isinstance(image, list)
        or len(image) != 1
        or not isinstance(image[0], dict)
    ):
        raise ValueError("the gateway BuildKit image inspection is malformed")
    container_record = container[0]
    image_record = image[0]
    container_config = container_record.get("Config")
    image_id = image_record.get("Id")
    if (
        not isinstance(container_config, dict)
        or container_config.get("Image") != BUILDKIT_REFERENCE
        or not isinstance(image_id, str)
        or SHA256_RE.fullmatch(image_id) is None
        or container_record.get("Image") != image_id
    ):
        raise ValueError("the gateway BuildKit container differs from the pinned image")

    repo_digests = image_record.get("RepoDigests")
    repository_prefix = f"{BUILDKIT_REPOSITORY}@"
    if (
        not isinstance(repo_digests, list)
        or not repo_digests
        or any(
            not isinstance(value, str)
            or not value.startswith(repository_prefix)
            or SHA256_RE.fullmatch(value.removeprefix(repository_prefix)) is None
            for value in repo_digests
        )
        or len(repo_digests) != len(set(repo_digests))
    ):
        raise ValueError("the gateway BuildKit repository digest differs from the pin")

    missing = object()
    descriptor = image_record.get("Descriptor", missing)
    if descriptor is missing:
        allowed_classic_repo_digests = {
            BUILDKIT_REPOSITORY_DIGEST,
            BUILDKIT_CLASSIC_AMD64_REPOSITORY_DIGEST,
        }
        if (
            image_record.get("Os") != "linux"
            or image_record.get("Architecture") != "amd64"
            or image_id != BUILDKIT_CLASSIC_AMD64_CONFIG_ID
            or not set(repo_digests).issubset(allowed_classic_repo_digests)
        ):
            raise ValueError(
                "the classic Docker BuildKit image differs from the pinned amd64 child"
            )
        return
    if (
        not isinstance(descriptor, dict)
        or descriptor.get("mediaType") != OCI_INDEX_MEDIA_TYPE
        or descriptor.get("digest") != BUILDKIT_DIGEST
        or not isinstance(descriptor.get("size"), int)
        or isinstance(descriptor.get("size"), bool)
        or descriptor["size"] <= 0
        or descriptor["size"] > MAX_JSON_BYTES
        or image_id != BUILDKIT_DIGEST
        or repo_digests != [BUILDKIT_REPOSITORY_DIGEST]
    ):
        raise ValueError("the gateway BuildKit OCI descriptor differs from the pin")


def buildx_version() -> str:
    result = run(("docker", "buildx", "version"), capture=True, timeout=30)
    match = re.search(r"\bv?(\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?)\b", result.stdout)
    if match is None:
        raise ValueError("Docker Buildx did not report a bounded semantic version")
    return f"v{match.group(1)}"


def _safe_tar_path(value: str) -> str:
    candidate = value[2:] if value.startswith("./") else value
    logical = PurePosixPath(candidate)
    if (
        not candidate
        or candidate.startswith("/")
        or "\\" in candidate
        or "\0" in candidate
        or logical.is_absolute()
        or any(part in {"", ".", ".."} for part in logical.parts)
    ):
        raise ValueError(f"unsafe OCI archive path: {value!r}")
    return logical.as_posix()


def canonicalise_oci_archive(
    source: Path,
    destination: Path,
    *,
    allow_existing_docker_manifest: bool = False,
) -> None:
    """Write a canonical hybrid OCI and Docker-save archive.

    BuildKit output must not supply ``manifest.json``. The Docker-save projection is
    instead derived from the digest-verified OCI graph. The narrowly scoped opt-in is
    used only when rebuilding an already canonical archive for byte verification; even
    then, the supplied bytes must exactly match the independently derived projection.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(source, "r:") as archive:
        members: list[tarfile.TarInfo] = []
        for member in archive:
            members.append(member)
            if len(members) > MAX_OCI_FILES:
                raise ValueError("OCI archive exceeds its file bound")
        normalised: dict[str, tarfile.TarInfo] = {}
        total_bytes = 0
        for member in members:
            name = _safe_tar_path(member.name)
            if name in normalised:
                raise ValueError(f"OCI archive contains a duplicate path: {name}")
            if not (member.isdir() or member.isreg()):
                raise ValueError(f"OCI archive contains a link or special member: {name}")
            if member.isreg():
                total_bytes += member.size
                if total_bytes > MAX_OCI_BYTES:
                    raise ValueError("OCI archive exceeds its byte bound")
            normalised[name] = member

        supplied_docker_manifest = normalised.get(DOCKER_SAVE_MANIFEST)
        if supplied_docker_manifest is not None and not allow_existing_docker_manifest:
            raise ValueError("raw OCI archive must not supply Docker manifest.json")
        docker_manifest = _docker_save_manifest_bytes_from_oci(archive, normalised)
        if supplied_docker_manifest is not None:
            supplied_bytes = _member_bytes(
                archive,
                normalised,
                DOCKER_SAVE_MANIFEST,
                maximum=MAX_JSON_BYTES,
            )
            if supplied_bytes != docker_manifest:
                raise ValueError(
                    "supplied Docker manifest differs from the derived OCI projection"
                )
            output_bytes = total_bytes
        else:
            if len(normalised) + 1 > MAX_OCI_FILES:
                raise ValueError("OCI archive exceeds its file bound")
            output_bytes = total_bytes + len(docker_manifest)
        if output_bytes > MAX_OCI_BYTES:
            raise ValueError("OCI archive exceeds its byte bound")

        temporary = destination.with_suffix(destination.suffix + ".tmp")
        with tarfile.open(temporary, "w", format=tarfile.USTAR_FORMAT) as output:
            output_names = {*normalised, DOCKER_SAVE_MANIFEST}
            for name in sorted(output_names, key=lambda item: (item.count("/"), item)):
                if name == DOCKER_SAVE_MANIFEST:
                    info = tarfile.TarInfo(name)
                    info.uid = 65532
                    info.gid = 65532
                    info.uname = ""
                    info.gname = ""
                    info.mtime = 0
                    info.type = tarfile.REGTYPE
                    info.mode = 0o644
                    info.size = len(docker_manifest)
                    output.addfile(info, io.BytesIO(docker_manifest))
                    continue
                member = normalised[name]
                info = tarfile.TarInfo(name)
                info.uid = 65532
                info.gid = 65532
                info.uname = ""
                info.gname = ""
                info.mtime = 0
                if member.isdir():
                    info.type = tarfile.DIRTYPE
                    info.mode = 0o755
                    output.addfile(info)
                    continue
                info.type = tarfile.REGTYPE
                info.mode = 0o644
                info.size = member.size
                extracted = archive.extractfile(member)
                if extracted is None:
                    raise ValueError(f"OCI archive file is unavailable: {name}")
                output.addfile(info, extracted)
        temporary.replace(destination)


def _json_member(
    archive: tarfile.TarFile, members: dict[str, tarfile.TarInfo], name: str
) -> dict[str, Any]:
    member = members.get(name)
    if member is None or not member.isreg() or member.size > MAX_JSON_BYTES:
        raise ValueError(f"OCI archive JSON member is missing or over its bound: {name}")
    extracted = archive.extractfile(member)
    if extracted is None:
        raise ValueError(f"OCI archive JSON member is unavailable: {name}")
    try:
        value = json.loads(extracted.read())
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"OCI archive JSON member is invalid: {name}") from error
    if not isinstance(value, dict):
        raise ValueError(f"OCI archive JSON member must be an object: {name}")
    return value


def _member_bytes(
    archive: tarfile.TarFile,
    members: dict[str, tarfile.TarInfo],
    name: str,
    *,
    maximum: int,
) -> bytes:
    member = members.get(name)
    if member is None or not member.isreg() or member.size > maximum:
        raise ValueError(f"OCI archive member is missing or over its bound: {name}")
    extracted = archive.extractfile(member)
    if extracted is None:
        raise ValueError(f"OCI archive member is unavailable: {name}")
    value = extracted.read(maximum + 1)
    if len(value) != member.size:
        raise ValueError(f"OCI archive member changed while it was read: {name}")
    return value


def _digest_member(
    archive: tarfile.TarFile, members: dict[str, tarfile.TarInfo], digest: str
) -> str:
    if SHA256_RE.fullmatch(digest) is None:
        raise ValueError("OCI descriptor digest is invalid")
    name = f"blobs/sha256/{digest.removeprefix('sha256:')}"
    member = members.get(name)
    if member is None or not member.isreg():
        raise ValueError(f"OCI descriptor blob is missing: {digest}")
    extracted = archive.extractfile(member)
    if extracted is None:
        raise ValueError(f"OCI descriptor blob is unavailable: {digest}")
    actual = hashlib.sha256()
    while chunk := extracted.read(1024 * 1024):
        actual.update(chunk)
    if actual.hexdigest() != digest.removeprefix("sha256:"):
        raise ValueError(f"OCI descriptor blob digest differs: {digest}")
    return name


def _descriptor_blob(
    archive: tarfile.TarFile,
    members: dict[str, tarfile.TarInfo],
    descriptor: Any,
    *,
    expected_media_type: str,
    maximum: int,
    allowed_optional_keys: frozenset[str] = frozenset(),
) -> tuple[str, str]:
    if not isinstance(descriptor, dict):
        raise ValueError("OCI descriptor must be an object")
    required = {"mediaType", "digest", "size"}
    if not required.issubset(descriptor) or not set(descriptor).issubset(
        required | allowed_optional_keys
    ):
        raise ValueError("OCI descriptor keys are outside the closed contract")
    if descriptor.get("mediaType") != expected_media_type:
        raise ValueError("OCI descriptor media type differs from the closed contract")
    digest = descriptor.get("digest")
    size = descriptor.get("size")
    if not isinstance(digest, str) or not isinstance(size, int) or isinstance(size, bool):
        raise ValueError("OCI descriptor digest or size is invalid")
    if size < 1 or size > maximum:
        raise ValueError("OCI descriptor size is outside its bound")
    name = _digest_member(archive, members, digest)
    if members[name].size != size:
        raise ValueError("OCI descriptor size differs from the referenced blob")
    return digest, name


def _uncompressed_layer_digest(
    archive: tarfile.TarFile,
    member: tarfile.TarInfo,
) -> tuple[str, int]:
    extracted = archive.extractfile(member)
    if extracted is None:
        raise ValueError("OCI layer blob is unavailable")
    digest = hashlib.sha256()
    expanded = 0
    try:
        with tempfile.TemporaryFile() as expanded_layer:
            with gzip.GzipFile(fileobj=extracted, mode="rb") as decompressed:
                while chunk := decompressed.read(1024 * 1024):
                    expanded += len(chunk)
                    if expanded > MAX_LAYER_EXPANDED_BYTES:
                        raise ValueError("OCI layer exceeds its expanded byte bound")
                    digest.update(chunk)
                    expanded_layer.write(chunk)
            expanded_layer.seek(0)
            _validate_layer_tar(expanded_layer)
    except (EOFError, gzip.BadGzipFile, OSError) as error:
        raise ValueError("OCI layer is not a valid bounded gzip stream") from error
    if expanded == 0:
        raise ValueError("OCI layer expands to no bytes")
    return f"sha256:{digest.hexdigest()}", expanded


def _validate_layer_link(member_name: str, value: str, *, symbolic: bool) -> None:
    if not value or "\\" in value or "\0" in value:
        raise ValueError("OCI layer contains an unsafe link target")
    if value.startswith("/") or not symbolic:
        parts = PurePosixPath(value.lstrip("/")).parts
    else:
        parts = (*PurePosixPath(member_name).parent.parts, *PurePosixPath(value).parts)
    resolved: list[str] = []
    for part in parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if not resolved:
                raise ValueError("OCI layer link target escapes the image root")
            resolved.pop()
        else:
            resolved.append(part)
    if not resolved:
        raise ValueError("OCI layer link target resolves to no path")


def _validate_layer_tar(fileobj: BinaryIO) -> None:
    names: set[str] = set()
    try:
        with tarfile.open(fileobj=fileobj, mode="r:") as layer:
            for member in layer:
                if len(names) >= MAX_LAYER_MEMBERS:
                    raise ValueError("OCI layer exceeds its member-count bound")
                name = _safe_tar_path(member.name)
                if name in names:
                    raise ValueError("OCI layer contains a duplicate path")
                names.add(name)
                if not (member.isdir() or member.isreg() or member.issym() or member.islnk()):
                    raise ValueError("OCI layer contains an unsupported special member")
                if member.size < 0 or member.size > MAX_LAYER_EXPANDED_BYTES:
                    raise ValueError("OCI layer member exceeds its byte bound")
                if member.issym() or member.islnk():
                    _validate_layer_link(
                        name, member.linkname, symbolic=member.issym()
                    )
    except tarfile.TarError as error:
        raise ValueError("OCI layer does not expand to a valid tar archive") from error


def _validate_image_labels(labels: dict[str, str]) -> None:
    static = {
        "org.opencontainers.image.title": "GIS AI GO blocked gateway candidate",
        "org.opencontainers.image.description": (
            "Repository-only zero-capability gateway container"
        ),
        "org.opencontainers.image.source": "https://github.com/chris-page-gov/gis-ai-go",
        "org.opencontainers.image.licenses": "MIT",
        "io.gis-ai-go.registry-id": EXPECTED_REGISTRY_ID,
        "io.gis-ai-go.lifecycle": "candidate-blocked",
        "io.gis-ai-go.live-provider-calls": "false",
        "io.gis-ai-go.active-tools": "[]",
        "io.gis-ai-go.active-api-operations": "[]",
    }
    dynamic = {
        "org.opencontainers.image.version",
        "org.opencontainers.image.revision",
        "org.opencontainers.image.created",
        "io.gis-ai-go.source-tree-clean",
    }
    if set(labels) != set(static) | dynamic:
        raise ValueError("OCI image label keys differ from the closed gateway contract")
    if any(labels.get(key) != value for key, value in static.items()):
        raise ValueError("OCI image labels weaken the blocked gateway boundary")
    if VERSION_RE.fullmatch(labels["org.opencontainers.image.version"]) is None:
        raise ValueError("OCI image version label is invalid")
    if COMMIT_RE.fullmatch(labels["org.opencontainers.image.revision"]) is None:
        raise ValueError("OCI image revision label is invalid")
    try:
        created = datetime.strptime(
            labels["org.opencontainers.image.created"], "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=UTC)
    except ValueError as error:
        raise ValueError("OCI image created label is invalid") from error
    if created.timestamp() < 0:
        raise ValueError("OCI image created label predates the supported epoch")
    if labels["io.gis-ai-go.source-tree-clean"] not in {"true", "false"}:
        raise ValueError("OCI image source cleanliness label is invalid")


def _docker_save_manifest_bytes_from_oci(
    archive: tarfile.TarFile,
    members: dict[str, tarfile.TarInfo],
) -> bytes:
    """Derive Docker's load index from the digest-verified OCI descriptor graph."""
    index = _json_member(archive, members, "index.json")
    descriptors = index.get("manifests")
    if (
        set(index) != {"schemaVersion", "mediaType", "manifests"}
        or index.get("schemaVersion") != 2
        or index.get("mediaType") != OCI_INDEX_MEDIA_TYPE
        or not isinstance(descriptors, list)
        or len(descriptors) != 1
    ):
        raise ValueError("OCI archive must contain exactly one image manifest")
    _, manifest_name = _descriptor_blob(
        archive,
        members,
        descriptors[0],
        expected_media_type=OCI_MANIFEST_MEDIA_TYPE,
        maximum=MAX_JSON_BYTES,
        allowed_optional_keys=frozenset({"annotations", "platform"}),
    )
    manifest = _json_member(archive, members, manifest_name)
    config_descriptor = manifest.get("config")
    layers = manifest.get("layers")
    if (
        set(manifest) != {"schemaVersion", "mediaType", "config", "layers"}
        or manifest.get("schemaVersion") != 2
        or manifest.get("mediaType") != OCI_MANIFEST_MEDIA_TYPE
        or not isinstance(config_descriptor, dict)
        or not isinstance(layers, list)
        or not layers
        or len(layers) > 64
    ):
        raise ValueError("OCI image manifest is invalid")
    _, config_name = _descriptor_blob(
        archive,
        members,
        config_descriptor,
        expected_media_type=OCI_CONFIG_MEDIA_TYPE,
        maximum=MAX_JSON_BYTES,
    )
    layer_names: list[str] = []
    for layer in layers:
        _, layer_name = _descriptor_blob(
            archive,
            members,
            layer,
            expected_media_type=OCI_LAYER_MEDIA_TYPE,
            maximum=MAX_OCI_BYTES,
            allowed_optional_keys=frozenset({"annotations"}),
        )
        layer_names.append(layer_name)
    config = _json_member(archive, members, config_name)
    runtime = config.get("config")
    labels = runtime.get("Labels") if isinstance(runtime, dict) else None
    revision = labels.get("org.opencontainers.image.revision") if isinstance(labels, dict) else None
    if not isinstance(revision, str) or COMMIT_RE.fullmatch(revision) is None:
        raise ValueError("OCI image revision label cannot bind the Docker tag")
    tag = f"deploy-207-{revision[:12]}"
    return canonical_json_bytes(
        [
            {
                "Config": config_name,
                "RepoTags": [f"gis-ai-go-gateway:{tag}"],
                "Layers": layer_names,
            }
        ]
    )


def _validate_docker_save_manifest(
    manifest_bytes: bytes,
    *,
    config_name: str,
    layer_names: list[str],
    tag: str,
) -> None:
    try:
        value = json.loads(manifest_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("Docker save manifest is invalid JSON") from error
    if manifest_bytes != canonical_json_bytes(value):
        raise ValueError("Docker save manifest is not canonical JSON")
    if not isinstance(value, list) or len(value) != 1 or not isinstance(value[0], dict):
        raise ValueError("Docker save manifest must contain exactly one image")
    image = value[0]
    if set(image) != {"Config", "RepoTags", "Layers"}:
        raise ValueError("Docker save manifest image keys are outside the closed contract")
    supplied_config = image.get("Config")
    supplied_layers = image.get("Layers")
    if not isinstance(supplied_config, str) or not isinstance(supplied_layers, list):
        raise ValueError("Docker save manifest paths are invalid")
    paths = [supplied_config, *supplied_layers]
    if not all(isinstance(path, str) for path in paths):
        raise ValueError("Docker save manifest paths are invalid")
    try:
        canonical_paths = [_safe_tar_path(path) for path in paths]
    except ValueError as error:
        raise ValueError("Docker save manifest contains an unsafe path") from error
    if canonical_paths != paths:
        raise ValueError("Docker save manifest paths are not canonical")
    expected = {
        "Config": config_name,
        "RepoTags": [tag],
        "Layers": layer_names,
    }
    if image != expected:
        raise ValueError("Docker save manifest differs from the exact OCI image")


def _assert_canonical_oci_archive(path: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="gis-ai-go-oci-canonical-") as temporary:
        rebuilt = Path(temporary) / "rebuilt.oci.tar"
        canonicalise_oci_archive(
            path,
            rebuilt,
            allow_existing_docker_manifest=True,
        )
        if (
            rebuilt.stat().st_size != path.stat().st_size
            or sha256_file(rebuilt) != sha256_file(path)
        ):
            raise ValueError("OCI archive bytes are outside canonical USTAR form")


def inspect_oci_archive(path: Path) -> OciInspection:
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise ValueError("OCI archive must be one real regular file")
    if metadata.st_size > MAX_OCI_BYTES:
        raise ValueError("OCI archive exceeds its byte bound")
    _assert_canonical_oci_archive(path)
    with tarfile.open(path, "r:") as archive:
        members: dict[str, tarfile.TarInfo] = {}
        ordered_names: list[str] = []
        total_bytes = 0
        for member in archive:
            if len(members) >= MAX_OCI_FILES:
                raise ValueError("OCI archive exceeds its member-count bound")
            name = _safe_tar_path(member.name)
            if name != member.name:
                raise ValueError("OCI archive member path is not canonical")
            if name in members:
                raise ValueError(f"OCI archive contains a duplicate path: {name}")
            if not (member.isdir() or member.isreg()):
                raise ValueError(f"OCI archive contains a link or special member: {name}")
            if (
                member.uid != 65532
                or member.gid != 65532
                or member.uname != ""
                or member.gname != ""
                or member.mtime != 0
                or member.pax_headers
            ):
                raise ValueError("OCI archive member metadata is not canonical")
            expected_mode = 0o755 if member.isdir() else 0o644
            if member.mode != expected_mode:
                raise ValueError("OCI archive member mode is not canonical")
            if member.isreg():
                total_bytes += member.size
                if total_bytes > MAX_OCI_BYTES:
                    raise ValueError("OCI archive exceeds its declared byte bound")
            members[name] = member
            ordered_names.append(name)
        if ordered_names != sorted(ordered_names, key=lambda item: (item.count("/"), item)):
            raise ValueError("OCI archive member order is not canonical")
        directories = {name for name, member in members.items() if member.isdir()}
        if directories != {"blobs", "blobs/sha256"}:
            raise ValueError("OCI archive directory inventory is not closed")
        files = {name for name, member in members.items() if member.isreg()}
        if not {"index.json", "manifest.json", "oci-layout"}.issubset(files):
            raise ValueError("OCI archive lacks its required layout files")
        if any(
            name not in {"index.json", "manifest.json", "oci-layout"}
            and not name.startswith("blobs/sha256/")
            for name in files
        ):
            raise ValueError("OCI archive contains a file outside its closed inventory")
        layout = _json_member(archive, members, "oci-layout")
        if layout != {"imageLayoutVersion": "1.0.0"}:
            raise ValueError("OCI archive layout version is invalid")
        index_bytes = _member_bytes(
            archive, members, "index.json", maximum=MAX_JSON_BYTES
        )
        try:
            index = json.loads(index_bytes)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("OCI archive index is invalid") from error
        if not isinstance(index, dict):
            raise ValueError("OCI archive index must be an object")
        descriptors = index.get("manifests")
        if (
            set(index) != {"schemaVersion", "mediaType", "manifests"}
            or index.get("schemaVersion") != 2
            or index.get("mediaType") != OCI_INDEX_MEDIA_TYPE
            or not isinstance(descriptors, list)
            or len(descriptors) != 1
        ):
            raise ValueError("OCI archive must contain exactly one image manifest")
        descriptor = descriptors[0]
        manifest_digest, manifest_name = _descriptor_blob(
            archive,
            members,
            descriptor,
            expected_media_type=OCI_MANIFEST_MEDIA_TYPE,
            maximum=MAX_JSON_BYTES,
            allowed_optional_keys=frozenset({"annotations", "platform"}),
        )
        manifest = _json_member(archive, members, manifest_name)
        config_descriptor = manifest.get("config")
        layers = manifest.get("layers")
        if (
            set(manifest) != {"schemaVersion", "mediaType", "config", "layers"}
            or manifest.get("schemaVersion") != 2
            or manifest.get("mediaType") != OCI_MANIFEST_MEDIA_TYPE
            or not isinstance(config_descriptor, dict)
            or not isinstance(layers, list)
            or not layers
            or len(layers) > 64
        ):
            raise ValueError("OCI image manifest is invalid")
        config_digest, config_name = _descriptor_blob(
            archive,
            members,
            config_descriptor,
            expected_media_type=OCI_CONFIG_MEDIA_TYPE,
            maximum=MAX_JSON_BYTES,
        )
        layer_digests: list[str] = []
        realised_diff_ids: list[str] = []
        expanded_rootfs = 0
        for layer in layers:
            layer_digest, layer_name = _descriptor_blob(
                archive,
                members,
                layer,
                expected_media_type=OCI_LAYER_MEDIA_TYPE,
                maximum=MAX_OCI_BYTES,
                allowed_optional_keys=frozenset({"annotations"}),
            )
            realised_diff_id, expanded = _uncompressed_layer_digest(
                archive, members[layer_name]
            )
            expanded_rootfs += expanded
            if expanded_rootfs > MAX_ROOTFS_EXPANDED_BYTES:
                raise ValueError("OCI root filesystem exceeds its expanded byte bound")
            layer_digests.append(layer_digest)
            realised_diff_ids.append(realised_diff_id)
        config = _json_member(archive, members, config_name)
        runtime = config.get("config")
        if not isinstance(runtime, dict):
            raise ValueError("OCI runtime configuration is invalid")
        labels = runtime.get("Labels")
        if not isinstance(labels, dict) or not all(
            isinstance(key, str) and isinstance(value, str) for key, value in labels.items()
        ):
            raise ValueError("OCI image labels are invalid")
        _validate_image_labels(labels)
        if set(runtime) != {
            "User",
            "ExposedPorts",
            "Env",
            "Entrypoint",
            "WorkingDir",
            "Labels",
            "StopSignal",
            "Healthcheck",
        }:
            raise ValueError("OCI runtime configuration keys are not closed")
        if runtime.get("User") != EXPECTED_USER:
            raise ValueError("OCI image must use the fixed non-root identity")
        if runtime.get("Entrypoint") != EXPECTED_ENTRYPOINT:
            raise ValueError("OCI image entry point differs from the blocked candidate")
        if runtime.get("WorkingDir") != EXPECTED_WORKING_DIRECTORY:
            raise ValueError("OCI image working directory differs from the blocked candidate")
        if runtime.get("ExposedPorts") != {EXPECTED_PORT: {}}:
            raise ValueError("OCI image must expose only the gateway port")
        health = runtime.get("Healthcheck")
        if health != EXPECTED_HEALTH_CONFIGURATION:
            raise ValueError("OCI image health check differs from the fixed probe")
        environment = runtime.get("Env")
        if environment != EXPECTED_ENVIRONMENT:
            raise ValueError("OCI image environment differs from the closed runtime contract")
        if runtime.get("StopSignal") != "SIGTERM":
            raise ValueError("OCI image stop signal differs from the closed runtime contract")
        architecture = config.get("architecture")
        operating_system = config.get("os")
        if architecture not in {"amd64", "arm64"} or operating_system != "linux":
            raise ValueError("OCI image platform is outside the reviewed candidate")
        platform = f"{operating_system}/{architecture}"
        if descriptor.get("platform") != {
            "architecture": architecture,
            "os": operating_system,
        }:
            raise ValueError("OCI index platform differs from the image configuration")
        created = labels["org.opencontainers.image.created"]
        revision = labels["org.opencontainers.image.revision"]
        tag = f"deploy-207-{revision[:12]}"
        if descriptor.get("annotations") != {
            "io.containerd.image.name": f"docker.io/library/gis-ai-go-gateway:{tag}",
            "org.opencontainers.image.created": created,
            "org.opencontainers.image.ref.name": tag,
        }:
            raise ValueError("OCI index annotations differ from the exact image identity")
        if config.get("created") != created:
            raise ValueError("OCI configuration creation time differs from its source label")
        rootfs = config.get("rootfs")
        if not isinstance(rootfs, dict) or set(rootfs) != {"type", "diff_ids"}:
            raise ValueError("OCI root filesystem descriptor is invalid")
        diff_ids = rootfs.get("diff_ids")
        if (
            rootfs.get("type") != "layers"
            or not isinstance(diff_ids, list)
            or len(diff_ids) != len(layer_digests)
            or not all(isinstance(value, str) and SHA256_RE.fullmatch(value) for value in diff_ids)
            or len(set(diff_ids)) != len(diff_ids)
        ):
            raise ValueError("OCI root filesystem diff IDs are invalid")
        if diff_ids != realised_diff_ids:
            raise ValueError("OCI root filesystem diff IDs differ from expanded layer bytes")
        docker_manifest_bytes = _member_bytes(
            archive,
            members,
            DOCKER_SAVE_MANIFEST,
            maximum=MAX_JSON_BYTES,
        )
        layer_names = [
            f"blobs/sha256/{value.removeprefix('sha256:')}"
            for value in layer_digests
        ]
        _validate_docker_save_manifest(
            docker_manifest_bytes,
            config_name=config_name,
            layer_names=layer_names,
            tag=f"gis-ai-go-gateway:{tag}",
        )
        reachable = {
            manifest_name,
            config_name,
            *layer_names,
        }
        if files != {"index.json", "manifest.json", "oci-layout"} | reachable:
            raise ValueError("OCI archive contains an unreachable or missing blob")
        return OciInspection(
            archive_sha256=sha256_file(path),
            archive_size=metadata.st_size,
            index_sha256=sha256_bytes(index_bytes),
            manifest_digest=manifest_digest,
            config_digest=config_digest,
            layer_digests=tuple(layer_digests),
            rootfs_diff_ids=tuple(diff_ids),
            platform=platform,
            labels=dict(labels),
        )


def build_oci_archive(
    output: Path,
    *,
    source: SourceIdentity,
    platform: str,
    tag: str,
    no_cache: bool = True,
) -> OciInspection:
    if PLATFORM_RE.fullmatch(platform) is None:
        raise ValueError("gateway image platform must be linux/amd64 or linux/arm64")
    verify_checked_inputs(source)
    verify_pinned_builder()
    inventory = build_context_inventory()
    output.parent.mkdir(parents=True, exist_ok=True)
    raw = output.with_suffix(output.suffix + ".raw")
    with tempfile.TemporaryDirectory(prefix="gis-ai-go-gateway-context-") as temporary:
        context = Path(temporary) / "context"
        materialise_build_context(inventory, context)
        arguments = [
            "docker",
            "buildx",
            "build",
            "--builder",
            BUILDER_NAME,
            "--file",
            str(context / CONTAINERFILE.relative_to(ROOT)),
            "--platform",
            platform,
            "--tag",
            tag,
            "--provenance=false",
            "--sbom=false",
            "--build-arg",
            f"PRODUCT_VERSION={source.version}",
            "--build-arg",
            f"SOURCE_CREATED={source.created}",
            "--build-arg",
            f"SOURCE_DATE_EPOCH={source.source_date_epoch}",
            "--build-arg",
            f"SOURCE_REVISION={source.revision}",
            "--build-arg",
            f"SOURCE_TREE_CLEAN={str(source.clean).lower()}",
            "--output",
            f"type=oci,dest={raw},rewrite-timestamp=true",
        ]
        if no_cache:
            arguments.append("--no-cache")
        arguments.append(str(context))
        try:
            run(arguments, discard_output=True, timeout=30 * 60)
            canonicalise_oci_archive(raw, output)
        finally:
            raw.unlink(missing_ok=True)
    inspection = inspect_oci_archive(output)
    if inspection.platform != platform:
        raise ValueError("built OCI platform differs from the requested platform")
    return inspection


def make_image_receipt(
    *,
    source: SourceIdentity,
    inspection: OciInspection,
    context_manifest_sha256: str,
    context_file_count: int,
    context_bytes: int,
    archive_name: str,
    realised_buildx_version: str,
) -> dict[str, Any]:
    labels = inspection.labels
    if (
        labels.get("org.opencontainers.image.version") != source.version
        or labels.get("org.opencontainers.image.revision") != source.revision
        or labels.get("org.opencontainers.image.created") != source.created
        or labels.get("io.gis-ai-go.source-tree-clean") != str(source.clean).lower()
    ):
        raise ValueError("OCI labels do not bind the supplied source identity")
    return {
        "schema": "gis-ai-go.gateway-image-receipt.v1",
        "classification": (
            "repository-only-blocked-candidate"
            if source.clean
            else "non-publishable-development-build"
        ),
        "source": {
            "repository": EXPECTED_REPOSITORY,
            "revision": source.revision,
            "version": source.version,
            "created": source.created,
            "source_date_epoch": source.source_date_epoch,
            "clean": source.clean,
        },
        "build": {
            "platform": inspection.platform,
            "node_base": {
                "reference": NODE_BASE_REFERENCE,
                "digest": NODE_BASE_DIGEST,
            },
            "package_manager": {
                "name": "pnpm",
                "version": PNPM_VERSION,
                "sha512": PNPM_SHA512,
            },
            "buildkit": BUILDKIT_REFERENCE,
            "buildkit_version": BUILDKIT_VERSION,
            "buildx_version": realised_buildx_version,
            "context": {
                "manifest": "build-context.sha256",
                "manifest_sha256": context_manifest_sha256,
                "file_count": context_file_count,
                "bytes": context_bytes,
            },
        },
        "image": {
            "archive": archive_name,
            "archive_sha256": inspection.archive_sha256,
            "archive_bytes": inspection.archive_size,
            "index_sha256": inspection.index_sha256,
            "manifest_digest": inspection.manifest_digest,
            "config_digest": inspection.config_digest,
            "layer_digests": list(inspection.layer_digests),
            "rootfs_diff_ids": list(inspection.rootfs_diff_ids),
            "entrypoint": EXPECTED_ENTRYPOINT,
            "user": EXPECTED_USER,
        },
        "runtime_boundary": {
            "lifecycle": "candidate-blocked",
            "readiness_status": 503,
            "active_tools": [],
            "active_api_operations": [],
            "active_resources": [],
            "live_provider_calls": False,
            "public_deployment": False,
            "ledger_root": LEDGER_ROOT,
            "reconciliation_root": RECONCILIATION_ROOT,
        },
        "assurance_tools": {
            "sbom": SYFT_REFERENCE,
            "vulnerability_scan": TRIVY_REFERENCE,
        },
    }


def parse_checksum(path: Path, expected_name: str) -> str:
    raw = read_bounded_regular_file(
        path,
        maximum_bytes=MAX_CHECKSUM_BYTES,
        label="gateway checksum ledger",
    )
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("gateway checksum ledger must be UTF-8") from error
    match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)\n", text)
    if match is None or match.group(2) != expected_name:
        raise ValueError("gateway OCI checksum ledger is invalid")
    return match.group(1)


def assert_no_private_text(value: bytes | str, label: str) -> None:
    if isinstance(value, bytes):
        if len(value) > MAX_PRIVACY_TEXT_BYTES:
            raise ValueError(f"{label} contains prohibited sensitive")
        try:
            text = value.decode("utf-8")
        except UnicodeDecodeError:
            text = None
        if text is None:
            raise ValueError(f"{label} must be UTF-8")
    elif isinstance(value, str):
        text = value
    else:
        raise TypeError("private-text input must be bytes or str")
    reason = prohibited_text_reason(text)
    if reason is not None:
        raise ValueError(f"{label} contains prohibited {reason}")


def assert_no_private_json(value: Any, label: str) -> None:
    reason = prohibited_json_reason(value)
    if reason is not None:
        raise ValueError(f"{label} contains prohibited {reason}")


def stream_copy(source: BinaryIO, destination: BinaryIO) -> None:
    while chunk := source.read(1024 * 1024):
        destination.write(chunk)
