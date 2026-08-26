#!/usr/bin/env python3
"""Verify one private Claude HOST-002 run and publish only a path-free pass."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from typing import Any, Callable, NoReturn

from jsonschema import Draft202012Validator, FormatChecker

import verify_qual_206_claude_composite_observation as composite


ROOT = Path(__file__).resolve().parents[1]
PRIVATE_SCHEMA = ROOT / "schemas/qual-206-claude-capability-private-run-v1.schema.json"
SESSION_SCHEMA = ROOT / "schemas/qual-206-claude-capability-session-v1.schema.json"
EVENT_SCHEMA = ROOT / "schemas/qual-206-claude-composite-host-event-v1.schema.json"
EVENT_CAPTURE_SCHEMA = (
    ROOT / "schemas/qual-206-claude-composite-host-event-capture-v1.schema.json"
)
PUBLIC_SCHEMA = ROOT / "schemas/qual-206-claude-capability-evidence-v1.schema.json"
EVIDENCE_DIRECTORY = ROOT / "tests/interoperability/evidence"
CORPUS = ROOT / "tests/interoperability/qual_206_cases.json"
OBSERVER = ROOT / "scripts/qual_206_claude_stdio_observer.mjs"
PINNED_MODEL = "claude-sonnet-5"
CANONICAL_REPOSITORY_ORIGIN = "https://github.com/chris-page-gov/gis-ai-go.git"
ALLOWED_REPOSITORY_ORIGINS = {
    CANONICAL_REPOSITORY_ORIGIN,
    "git@github.com:chris-page-gov/gis-ai-go.git",
}
SAFE_GIT_OPTIONS = (
    "-c",
    "core.fsmonitor=false",
    "-c",
    "core.hooksPath=/dev/null",
)
CLOSED_GIT_ENVIRONMENT = {
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_OPTIONAL_LOCKS": "0",
    "LANG": "C",
    "LC_ALL": "C",
    "PATH": "/usr/bin:/bin",
}
EXPECTED_PROMPT = (
    "Search the public catalogue for INSPIRE and return the first record with "
    "its inline evidence receipt.\n"
).encode()
EXPECTED_NODE_BYTES = 50_320
EXPECTED_NODE_SHA256 = "1ef99ea25fe70c9b67e7efe768ef8ee22148d3cabc703db6131b57aeb617d040"
NETWORK_SANDBOX = "macos-seatbelt-deny-network"
NETWORK_SANDBOX_PROFILE = "(version 1) (allow default) (deny network*)"
SANDBOX_EXEC = Path("/usr/bin/sandbox-exec")
NETWORK_SANDBOX_PROBE_SOURCE = "\n".join(
    (
        '"use strict";',
        "const { closeSync, constants, fsyncSync, openSync, readFileSync, rmSync, "
        'writeSync } = require("node:fs");',
        'const { createConnection } = require("node:net");',
        'const { join } = require("node:path");',
        "const root = process.argv[1];",
        "const port = Number(process.argv[2]);",
        'const path = join(root, "durability-probe");',
        'const value = Buffer.from("gis-ai-go-network-sandbox-probe\\n", "utf8");',
        "let descriptor = openSync(path, constants.O_WRONLY | constants.O_CREAT | "
        "constants.O_EXCL | (constants.O_NOFOLLOW || 0), 0o600);",
        "try { writeSync(descriptor, value); fsyncSync(descriptor); } finally { "
        "closeSync(descriptor); }",
        'if (!readFileSync(path).equals(value)) throw new Error("durability readback failed");',
        "descriptor = openSync(root, constants.O_RDONLY | (constants.O_DIRECTORY || 0) | "
        "(constants.O_NOFOLLOW || 0));",
        "try { fsyncSync(descriptor); rmSync(path); fsyncSync(descriptor); } finally { "
        "closeSync(descriptor); }",
        'const socket = createConnection({ host: "127.0.0.1", port });',
        "let finished = false;",
        "const timer = setTimeout(() => finish(4, { fsync_pass: true, network_error: "
        '"timeout" }), 2000);',
        "function finish(code, result) {",
        "  if (finished) return;",
        "  finished = true;",
        "  clearTimeout(timer);",
        "  socket.destroy();",
        "  process.stdout.write(`${JSON.stringify(result)}\\n`);",
        "  process.exitCode = code;",
        "}",
        "socket.once(\"connect\", () => finish(3, { fsync_pass: true, "
        "network_error: null }));",
        'socket.once("error", (error) => {',
        "  const code = error && error.code;",
        "  finish(code === \"EPERM\" || code === \"EACCES\" ? 0 : 5, { "
        'fsync_pass: true, network_error: code || "unknown" });',
        "});",
    )
)
EXPECTED_NETWORK_SANDBOX_PROBE_SHA256 = hashlib.sha256(
    NETWORK_SANDBOX_PROBE_SOURCE.encode()
).hexdigest()
EXPECTED_SANDBOX_EXEC_BYTES = 102_560
EXPECTED_SANDBOX_EXEC_SHA256 = (
    "8290e4be7387a0df83cd1559e86afd880464f269450573d012795761fe298f16"
)
EXPECTED_RECORD_ID = "hmlr:dataset:inspire-index-polygons"
EXPECTED_TITLE = "Index polygons spatial data (INSPIRE)"
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
CLAUDE_CLIENT_ONLY_MCP_VARIABLES = (
    "MCP_PROTOCOL_NEGOTIATION",
    "MCP_SDK_GENERATION",
)
TRACKED_CAPABILITY_MATERIALS = {
    "package.json",
    "pnpm-lock.yaml",
    "schemas/qual-206-claude-capability-evidence-v1.schema.json",
    "schemas/qual-206-claude-capability-private-run-v1.schema.json",
    "schemas/qual-206-claude-capability-session-v1.schema.json",
    "schemas/qual-206-claude-composite-host-event-capture-v1.schema.json",
    "schemas/qual-206-claude-composite-host-event-v1.schema.json",
    "scripts/qual_206_claude_capability_harness.mjs",
    "scripts/qual_206_claude_runtime_closure.mjs",
    "scripts/qual_206_claude_stdio_observer.mjs",
    "scripts/qual_206_exact_five_event_collector.mjs",
    "scripts/verify_qual_206_claude_capability.py",
    "scripts/verify_qual_206_claude_composite_observation.py",
    "tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs",
    "tests/interoperability/fixtures/qual_206_strict_modern_event_server.mjs",
    "tests/interoperability/qual_206_cases.json",
}
GENERATED_RUNTIME_ROOTS = (
    "apps/mcp-gateway/dist",
    "artifacts/okf",
    "packages/authority-context/dist",
    "packages/contracts/dist",
    "packages/evidence/dist",
    "packages/policy-client/dist",
    "packages/provider-adapter-sdk/dist",
    "packages/tool-registry/dist",
)
INSTALLED_DEPENDENCY_ROOTS = (
    "node_modules",
    "apps/mcp-gateway/node_modules",
    "apps/public-explorer/node_modules",
    "packages/authority-context/node_modules",
    "packages/policy-client/node_modules",
    "packages/provider-adapter-sdk/node_modules",
)
WORKSPACE_DEPENDENCY_TARGETS = {
    "apps/mcp-gateway",
    "apps/public-explorer",
    "packages/authority-context",
    "packages/contracts",
    "packages/evidence",
    "packages/policy-client",
    "packages/provider-adapter-sdk",
    "packages/tool-registry",
}
OUTPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["record_id", "title", "receipt_id"],
    "properties": {
        "record_id": {"const": EXPECTED_RECORD_ID},
        "title": {"const": EXPECTED_TITLE},
        "receipt_id": {
            "type": "string",
            "pattern": "^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$",
        },
    },
}
EXPECTED_ROOT_NAMES = {
    "mcp.json",
    "observer",
    "run-manifest.json",
    "settings.json",
    "stderr.log",
    "stdout.json",
    "workspace",
}
EXPECTED_SESSION_FILES = {"capability.json", "events.jsonl", "manifest.json"}
RECEIPT_ID = re.compile(r"^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$")
TOKEN_PATTERN = re.compile(
    rb"(?:sk-[A-Za-z0-9_-]{8,}|gh[opusr]_[A-Za-z0-9]{8,}|"
    rb"xox[baprs]-[A-Za-z0-9-]{8,}|AKIA[0-9A-Z]{16}|"
    rb"Bearer\s+[A-Za-z0-9._~-]{8,})",
    re.IGNORECASE,
)
BOUNDARY = (
    "One bounded Claude Code 2.1.245 model-mediated catalogue.search observation "
    "for QUAL-206-HOST-002 over local MCP 2026-07-28 STDIO. This does not "
    "prove exact-five model capability, remote HTTP interoperability, a live "
    "geospatial provider, registry publication, activation, deployment or release."
)


class CapabilityVerificationError(ValueError):
    """The owner-only capability run did not satisfy the pass contract."""


def fail(message: str) -> NoReturn:
    raise CapabilityVerificationError(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def strict_object(raw: bytes, *, label: str, newline: bool = False) -> dict[str, Any]:
    if newline:
        if not raw.endswith(b"\n") or raw.endswith(b"\r\n"):
            fail(f"{label} must be one LF-terminated canonical JSON object")
        raw = raw[:-1]
        if b"\n" in raw or b"\r" in raw:
            fail(f"{label} must contain exactly one JSON object")
    try:
        value = composite.parse_json(raw, label=label)
    except (OSError, composite.VerificationError) as error:
        raise CapabilityVerificationError(str(error)) from error
    return value


def canonical_line(value: dict[str, Any]) -> bytes:
    try:
        return composite.canonical_json_bytes(value) + b"\n"
    except composite.VerificationError as error:
        raise CapabilityVerificationError(str(error)) from error


def schema_validator(path: Path) -> Draft202012Validator:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate(
    validator: Draft202012Validator,
    value: dict[str, Any],
    *,
    label: str,
) -> None:
    errors = sorted(validator.iter_errors(value), key=lambda error: list(error.path))
    if errors:
        details = "; ".join(
            f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in errors[:8]
        )
        fail(f"{label} failed its closed schema: {details}")


def require_directory(path: Path, *, label: str, mode: int = 0o700) -> os.stat_result:
    try:
        if not path.is_absolute() or Path(os.path.abspath(path)) != path:
            fail(f"{label} must be canonical and absolute")
        if Path(os.path.realpath(path)) != path:
            fail(f"{label} must not traverse an alias")
        metadata = path.lstat()
    except OSError as error:
        raise CapabilityVerificationError(f"{label} is unavailable") from error
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISDIR(metadata.st_mode)
        or metadata.st_uid != os.getuid()
        or stat.S_IMODE(metadata.st_mode) != mode
    ):
        fail(f"{label} must be one owner-owned {mode:04o} directory")
    return metadata


def read_private(path: Path, *, maximum: int, label: str) -> bytes:
    try:
        before = path.lstat()
        if (
            stat.S_ISLNK(before.st_mode)
            or not stat.S_ISREG(before.st_mode)
            or before.st_uid != os.getuid()
            or before.st_nlink != 1
            or stat.S_IMODE(before.st_mode) != 0o600
            or before.st_size < 0
            or before.st_size > maximum
        ):
            fail(f"{label} must be one owner-only bounded regular file")
        descriptor = os.open(
            path,
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
        )
        try:
            opened = os.fstat(descriptor)
            if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
                fail(f"{label} changed before it was opened")
            chunks: list[bytes] = []
            remaining = opened.st_size
            while remaining:
                chunk = os.read(descriptor, min(65_536, remaining))
                if not chunk:
                    fail(f"{label} ended before its declared size")
                chunks.append(chunk)
                remaining -= len(chunk)
            raw = b"".join(chunks)
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)
    except OSError as error:
        raise CapabilityVerificationError(f"{label} could not be read safely") from error
    if (
        (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        != (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    ):
        fail(f"{label} changed while it was read")
    return raw


def git_output(*arguments: str) -> str:
    result = subprocess.run(
        ["/usr/bin/git", *SAFE_GIT_OPTIONS, *arguments],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=CLOSED_GIT_ENVIRONMENT,
        timeout=10,
    )
    if result.returncode != 0:
        fail(f"git {' '.join(arguments)} failed during source verification")
    return result.stdout.decode("utf-8", errors="strict").strip()


def read_stable_regular(
    path: Path,
    *,
    maximum: int,
    label: str,
    require_single_link: bool = True,
) -> bytes:
    try:
        if not path.is_absolute() or Path(os.path.realpath(path)) != path:
            fail(f"{label} must be canonical and must not traverse an alias")
        before = path.lstat()
        if (
            stat.S_ISLNK(before.st_mode)
            or not stat.S_ISREG(before.st_mode)
            or (require_single_link and before.st_nlink != 1)
            or before.st_size < 0
            or before.st_size > maximum
        ):
            fail(f"{label} must be one bounded singly linked regular file")
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        try:
            opened = os.fstat(descriptor)
            if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
                fail(f"{label} changed before it was opened")
            chunks: list[bytes] = []
            remaining = opened.st_size
            while remaining:
                chunk = os.read(descriptor, min(65_536, remaining))
                if not chunk:
                    fail(f"{label} ended before its declared size")
                chunks.append(chunk)
                remaining -= len(chunk)
            raw = b"".join(chunks)
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)
    except OSError as error:
        raise CapabilityVerificationError(f"{label} could not be read safely") from error
    if (
        (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        != (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    ):
        fail(f"{label} changed while it was read")
    return raw


def measure_stable_regular(
    path: Path,
    *,
    maximum: int,
    label: str,
    require_single_link: bool = True,
) -> dict[str, Any]:
    try:
        if not path.is_absolute() or Path(os.path.realpath(path)) != path:
            fail(f"{label} must be canonical and must not traverse an alias")
        before = path.lstat()
        if (
            stat.S_ISLNK(before.st_mode)
            or not stat.S_ISREG(before.st_mode)
            or (require_single_link and before.st_nlink != 1)
            or before.st_size < 0
            or before.st_size > maximum
        ):
            fail(f"{label} must be one bounded regular file")
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        try:
            opened = os.fstat(descriptor)
            if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
                fail(f"{label} changed before it was opened")
            digest = hashlib.sha256()
            measured_bytes = 0
            while True:
                chunk = os.read(descriptor, 65_536)
                if not chunk:
                    break
                digest.update(chunk)
                measured_bytes += len(chunk)
                if measured_bytes > maximum:
                    fail(f"{label} exceeded its byte boundary")
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)
    except OSError as error:
        raise CapabilityVerificationError(f"{label} could not be measured safely") from error
    if (
        (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        != (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        or measured_bytes != before.st_size
    ):
        fail(f"{label} changed while it was measured")
    return {"bytes": measured_bytes, "sha256": digest.hexdigest()}


def measure_generated_runtime_closure() -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    identities: set[tuple[int, int]] = set()
    total_bytes = 0

    def visit(directory: Path) -> None:
        try:
            state = directory.lstat()
            if (
                stat.S_ISLNK(state.st_mode)
                or not stat.S_ISDIR(state.st_mode)
                or Path(os.path.realpath(directory)) != directory
            ):
                fail("generated runtime root must be one real directory")
            children = sorted(directory.iterdir(), key=lambda child: child.name)
        except OSError as error:
            raise CapabilityVerificationError(
                "generated runtime closure is unavailable"
            ) from error
        for child in children:
            child_state = child.lstat()
            if stat.S_ISDIR(child_state.st_mode) and not stat.S_ISLNK(child_state.st_mode):
                visit(child)
                continue
            if not stat.S_ISREG(child_state.st_mode) or stat.S_ISLNK(child_state.st_mode):
                fail("generated runtime closure contains a link or special file")
            identity = (child_state.st_dev, child_state.st_ino)
            if identity in identities or child_state.st_nlink != 1:
                fail("generated runtime file must be singly linked and unique")
            identities.add(identity)
            measured = measure_stable_regular(
                child,
                maximum=536_870_912,
                label="generated runtime file",
            )
            nonlocal total_bytes
            total_bytes += measured["bytes"]
            if len(entries) >= 4_096 or total_bytes > 536_870_912:
                fail("generated runtime closure exceeds its boundary")
            entries.append(
                {
                    "bytes": measured["bytes"],
                    "path": child.relative_to(ROOT).as_posix(),
                    "sha256": measured["sha256"],
                }
            )

    for relative in GENERATED_RUNTIME_ROOTS:
        visit(ROOT / relative)
    digest = hashlib.sha256()
    digest.update(b"GIS-AI-GO\0canonical-json\0sha256\0v1\0")
    digest.update(b"gis-ai-go.qual-206-claude-runtime-closure.v1\0")
    digest.update(composite.canonical_json_bytes(entries))
    return {
        "bytes": total_bytes,
        "file_count": len(entries),
        "manifest_sha256": digest.hexdigest(),
    }


def measure_installed_dependency_closure() -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    identities: set[tuple[int, int]] = set()
    total_bytes = 0

    def visit(path: Path, depth: int) -> None:
        nonlocal total_bytes
        if depth > 32:
            fail("installed dependency closure is too deeply nested")
        try:
            state = path.lstat()
        except OSError as error:
            raise CapabilityVerificationError(
                "installed dependency closure is unavailable"
            ) from error
        relative = path.relative_to(ROOT).as_posix()
        if stat.S_ISLNK(state.st_mode):
            target = os.readlink(path)
            try:
                resolved = path.resolve(strict=True)
                after = path.lstat()
                stable_target = os.readlink(path)
            except OSError as error:
                raise CapabilityVerificationError(
                    "installed dependency link target is unavailable"
                ) from error
            dependency_roots = tuple(ROOT / value for value in INSTALLED_DEPENDENCY_ROOTS)
            workspace_targets = {ROOT / value for value in WORKSPACE_DEPENDENCY_TARGETS}
            target_is_measured = any(
                resolved == dependency_root or dependency_root in resolved.parents
                for dependency_root in dependency_roots
            ) or resolved in workspace_targets
            if (
                os.path.isabs(target)
                or "\0" in target
                or ROOT not in resolved.parents
                or not target_is_measured
                or (after.st_dev, after.st_ino, after.st_mtime_ns)
                != (state.st_dev, state.st_ino, state.st_mtime_ns)
                or stable_target != target
            ):
                fail("installed dependency closure contains an unsafe link target")
            entries.append({"kind": "symlink", "path": relative, "target": target})
        elif stat.S_ISDIR(state.st_mode):
            for child in sorted(path.iterdir(), key=lambda value: value.name):
                visit(child, depth + 1)
        elif stat.S_ISREG(state.st_mode):
            identity = (state.st_dev, state.st_ino)
            if state.st_nlink != 1 or identity in identities:
                fail("installed dependency file must be singly linked and unique")
            identities.add(identity)
            measured = measure_stable_regular(
                path,
                maximum=536_870_912,
                label="installed dependency file",
            )
            total_bytes += measured["bytes"]
            if total_bytes > 1_073_741_824:
                fail("installed dependency closure exceeds its byte boundary")
            entries.append(
                {
                    "kind": "file",
                    "path": relative,
                    "bytes": measured["bytes"],
                    "sha256": measured["sha256"],
                }
            )
        else:
            fail("installed dependency closure contains a special file")
        if len(entries) > 20_000:
            fail("installed dependency closure has too many entries")

    for relative in INSTALLED_DEPENDENCY_ROOTS:
        visit(ROOT / relative, 0)
    digest = hashlib.sha256()
    digest.update(b"GIS-AI-GO\0canonical-json\0sha256\0v1\0")
    digest.update(b"gis-ai-go.qual-206-claude-dependency-closure.v1\0")
    digest.update(composite.canonical_json_bytes(entries))
    return {
        "bytes": total_bytes,
        "entry_count": len(entries),
        "manifest_sha256": digest.hexdigest(),
    }


def verify_case(manifest: dict[str, Any]) -> None:
    raw = read_stable_regular(CORPUS, maximum=1_048_576, label="HOST-002 corpus")
    case = manifest["case"]
    if (
        len(raw) != case["corpus_bytes"]
        or sha256_bytes(raw) != case["corpus_sha256"]
        or case["corpus_sha256"]
        != "23ac9bc1a76d524bd0e250b11b9ba321b09e66bd5921f1463f50c150001cd389"
        or len(EXPECTED_PROMPT) != case["prompt_bytes"]
        or sha256_bytes(EXPECTED_PROMPT) != case["prompt_sha256"]
    ):
        fail("the private manifest does not bind the exact HOST-002 corpus and prompt")
    corpus = strict_object(raw, label="HOST-002 corpus")
    matches = [value for value in corpus.get("cases", []) if value.get("id") == case["id"]]
    if (
        len(matches) != 1
        or set(matches[0])
        != {"capability", "expected", "id", "prompt", "provenance", "required_tools"}
        or f"{matches[0]['prompt']}\n".encode() != EXPECTED_PROMPT
        or matches[0]["capability"] != "catalogue_search"
        or matches[0]["required_tools"] != ["catalogue.search"]
    ):
        fail("the HOST-002 corpus case does not match the frozen capability request")


def verify_source_and_materials(manifest: dict[str, Any]) -> None:
    source = manifest["source"]
    if (
        git_output("rev-parse", "HEAD") != source["commit"]
        or git_output("rev-parse", "refs/remotes/origin/main") != source["commit"]
        or git_output("rev-parse", f"{source['commit']}^{{tree}}") != source["tree"]
        or git_output("config", "--local", "--no-includes", "--get", "remote.origin.url")
        not in ALLOWED_REPOSITORY_ORIGINS
        or git_output("status", "--porcelain=v1", "--untracked-files=all") != ""
    ):
        fail("verification requires the unchanged clean local origin/main source checkout")
    symbolic = subprocess.run(
        ["/usr/bin/git", *SAFE_GIT_OPTIONS, "symbolic-ref", "-q", "HEAD"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=CLOSED_GIT_ENVIRONMENT,
        timeout=10,
    )
    if symbolic.returncode != 1:
        fail("verification requires a detached local origin/main checkout")
    if (
        source["repository_origin"] != CANONICAL_REPOSITORY_ORIGIN
        or source["local_origin_main_match"] is not True
        or source["protected_main_verification"] != "external-publication-gate"
    ):
        fail("source claims exceed the locally verifiable boundary")
    binding = manifest["runtime_binding"]
    materials = binding["tracked_source_materials"]
    paths = [item["path"] for item in materials]
    if len(paths) != len(set(paths)) or set(paths) != TRACKED_CAPABILITY_MATERIALS:
        fail("tracked runtime materials do not contain the exact source closure")
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
                *SAFE_GIT_OPTIONS,
                "show",
                f"{source['commit']}:{item['path']}",
            ],
            cwd=ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=CLOSED_GIT_ENVIRONMENT,
            timeout=10,
        )
        if blob.returncode != 0 or sha256_bytes(blob.stdout) != item["sha256"]:
            fail(f"runtime material is not bound to the source commit: {item['path']}")
    generated = binding["generated_first_party_closure"]
    current = measure_generated_runtime_closure()
    installed = measure_installed_dependency_closure()
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
        fail("generated or third-party runtime binding does not preserve its exact boundary")


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
        "enabledMcpjsonServers": ["gis-ai-go-qual-206-host-002"],
        "permissions": {
            "allow": ["mcp__gis-ai-go-qual-206-host-002__catalogue_search"],
            "deny": [],
            "defaultMode": "dontAsk",
        },
    }
    if settings != expected_settings:
        fail("private Claude settings widen or change the closed host profile")
    if set(mcp) != {"mcpServers"} or set(mcp["mcpServers"]) != {
        "gis-ai-go-qual-206-host-002"
    }:
        fail("private MCP configuration does not contain exactly one server")
    server = mcp["mcpServers"]["gis-ai-go-qual-206-host-002"]
    if (
        not isinstance(server, dict)
        or set(server) != {"type", "command", "args"}
        or server["type"] != "stdio"
        or server["command"] != str(SANDBOX_EXEC)
        or not isinstance(server["args"], list)
        or not all(isinstance(value, str) for value in server["args"])
    ):
        fail("private MCP server definition is not the exact STDIO projection")
    unset_arguments = [
        value
        for name in (
            *RECOGNISED_CREDENTIAL_VARIABLES,
            *CLAUDE_CLIENT_ONLY_MCP_VARIABLES,
        )
        for value in ("-u", name)
    ]
    args = server["args"]
    prefix = [
        "-p",
        NETWORK_SANDBOX_PROFILE,
        "/usr/bin/env",
        *unset_arguments,
        "GIS_AI_GO_QUAL_206_EVENT_CAPTURE=1",
        f"GIS_AI_GO_QUAL_206_MCP_NETWORK_SANDBOX={NETWORK_SANDBOX}",
        "GIS_AI_GO_QUAL_206_HOST_ATTESTATION=outer-harness-spawn-executable",
    ]
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
        SANDBOX_EXEC,
        maximum=1_048_576,
        label="macOS Seatbelt executable",
    )
    observer_root = private_root / "observer"
    expected_tail = [
        str(node_path),
        str(OBSERVER),
        "--claude-host-002-capability-observation-only",
        "--capture-root",
        str(observer_root),
        "--run-id",
        manifest["run_id"],
        "--client",
        "claude-code-2.1.245-host-002",
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
        "bytes": EXPECTED_SANDBOX_EXEC_BYTES,
        "path": str(SANDBOX_EXEC),
        "profile_sha256": sha256_bytes(NETWORK_SANDBOX_PROFILE.encode()),
        "sha256": EXPECTED_SANDBOX_EXEC_SHA256,
    }
    expected_sandbox_probe = {
        "fsync_pass": True,
        "loopback_denied": True,
        "probe_script_sha256": EXPECTED_NETWORK_SANDBOX_PROBE_SHA256,
    }
    if (
        str(node_path) != manifest["runtime_binding"]["node_runtime"]["path"]
        or node != {"bytes": EXPECTED_NODE_BYTES, "sha256": EXPECTED_NODE_SHA256}
        or manifest["runtime_binding"]["node_runtime"]
        != {
            "bytes": EXPECTED_NODE_BYTES,
            "path": str(node_path),
            "sha256": EXPECTED_NODE_SHA256,
            "version": "26.7.0",
        }
        or sandbox
        != {
            "bytes": EXPECTED_SANDBOX_EXEC_BYTES,
            "sha256": EXPECTED_SANDBOX_EXEC_SHA256,
        }
        or manifest["runtime_binding"]["network_sandbox"] != expected_sandbox
        or manifest["runtime_binding"]["network_sandbox_probe"]
        != expected_sandbox_probe
    ):
        fail("private MCP configuration does not bind the accepted runtime executables")
    expected_output_schema_sha256 = sha256_bytes(
        composite.canonical_json_bytes(OUTPUT_SCHEMA)
    )
    if manifest["execution"]["output_schema_sha256"] != expected_output_schema_sha256:
        fail("Claude output schema digest does not bind the exact pass projection")


def verify_event_log(
    raw: bytes,
    manifest: dict[str, Any],
    *,
    slot: str,
    run_manifest: dict[str, Any],
    event_validator: Draft202012Validator,
) -> tuple[list[dict[str, Any]], Counter[str], Counter[str], int]:
    if not raw or not raw.endswith(b"\n") or raw.endswith(b"\r\n"):
        fail(f"{slot} event log is not LF-terminated")
    encoded_lines = [line + b"\n" for line in raw[:-1].split(b"\n")]
    previous: str | None = None
    events: list[dict[str, Any]] = []
    methods: Counter[str] = Counter()
    operations: Counter[str] = Counter()
    provider_guard_calls = 0
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
        if value["event"] == "audit":
            if value["contract_valid"] is not True:
                fail(f"{slot} contains an invalid fixture audit")
            provider_guard_calls += value["guarded_api_invocation_count"] or 0
            provider_guard_calls += value["provider_transport_calls"] or 0
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
    ):
        fail(f"{slot} does not bind the clean source and Claude parent")
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
    audit_kinds = [
        event["audit_kind"] for event in events if event["event"] == "audit"
    ]
    if audit_kinds != [
        "provider-egress-guard-ready",
        "provider-egress-guard-summary",
        "session-summary",
    ]:
        fail(f"{slot} does not contain the exact closed fixture audit sequence")
    if provider_guard_calls != 0:
        fail(f"{slot} observed geospatial provider egress")
    if manifest["event_log"] != {
        "bytes": len(raw),
        "event_count": len(events),
        "last_event_sha256": previous,
        "sha256": sha256_bytes(raw),
    }:
        fail(f"{slot} manifest does not bind its event log")
    return events, methods, operations, provider_guard_calls


def verify_sessions(
    observer_root: Path,
    run_manifest: dict[str, Any],
) -> tuple[list[dict[str, Any]], Counter[str], Counter[str], int]:
    require_directory(observer_root, label="observer root")
    names = set(os.listdir(observer_root))
    if "catalogue-search.claim.json" not in names:
        fail("observer root has no global catalogue.search claim")
    slots = sorted(name for name in names if re.fullmatch(r"session-[123]", name))
    if names != set(slots) | {"catalogue-search.claim.json"} or not slots:
        fail("observer root contains an unexpected entry")
    claim_raw = read_private(
        observer_root / "catalogue-search.claim.json",
        maximum=1_024,
        label="global capability claim",
    )
    claim = strict_object(claim_raw, label="global capability claim", newline=True)
    if (
        set(claim) != {"schema", "case_id", "run_id", "session_id"}
        or claim["schema"] != "gis-ai-go.qual-206-claude-capability-call-claim.v1"
        or claim["case_id"] != "QUAL-206-HOST-002"
        or claim["run_id"] != run_manifest["run_id"]
    ):
        fail("global capability claim is invalid")

    event_validator = schema_validator(EVENT_SCHEMA)
    capture_validator = schema_validator(EVENT_CAPTURE_SCHEMA)
    session_validator = schema_validator(SESSION_SCHEMA)
    summaries: list[dict[str, Any]] = []
    total_methods: Counter[str] = Counter()
    total_operations: Counter[str] = Counter()
    total_guard_calls = 0
    seen_session_ids: set[str] = set()
    for slot in slots:
        path = observer_root / slot
        require_directory(path, label=slot)
        if set(os.listdir(path)) != EXPECTED_SESSION_FILES:
            fail(f"{slot} does not contain its exact three private files")
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
            path / "capability.json",
            maximum=65_536,
            label=f"{slot} capability",
        )
        event_state = (path / "events.jsonl").lstat()
        manifest_state = (path / "manifest.json").lstat()
        composite_result = composite.verify_session(
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
        )
        event_manifest = strict_object(manifest_raw, label=f"{slot} manifest", newline=True)
        summary = strict_object(summary_raw, label=f"{slot} capability", newline=True)
        if canonical_line(event_manifest) != manifest_raw or canonical_line(summary) != summary_raw:
            fail(f"{slot} contains a non-canonical manifest")
        validate(capture_validator, event_manifest, label=f"{slot} event manifest")
        validate(session_validator, summary, label=f"{slot} capability summary")
        if (
            event_manifest["slot"] != slot
            or summary["slot"] != slot
            or event_manifest["session_id"] != summary["session_id"]
            or summary["session_id"] in seen_session_ids
            or summary["run_id"] != run_manifest["run_id"]
            or summary["source_commit"] != run_manifest["source"]["commit"]
            or summary["mcp_subtree_network_access_allowed"] is not False
            or summary["mcp_subtree_network_sandbox"] != NETWORK_SANDBOX
            or composite_result.session_id != summary["session_id"]
            or composite_result.profile != summary["session_profile"]
        ):
            fail(f"{slot} has inconsistent run or session identity")
        seen_session_ids.add(summary["session_id"])
        events, methods, operations, guard_calls = verify_event_log(
            event_raw,
            event_manifest,
            slot=slot,
            run_manifest=run_manifest,
            event_validator=event_validator,
        )
        summaries.append(summary)
        total_methods.update(methods)
        total_operations.update(operations)
        total_guard_calls += guard_calls
    call_summaries = [summary for summary in summaries if summary["request"]["observed"]]
    if len(call_summaries) != 1 or claim["session_id"] != call_summaries[0]["session_id"]:
        fail("the run does not contain exactly one globally claimed tool call")
    call = call_summaries[0]
    expected_parameters = composite.canonical_json_bytes({"limit": 1, "query": "INSPIRE"})
    if (
        call["request"]["valid"] is not True
        or call["request"]["parameters_bytes"] != len(expected_parameters)
        or call["request"]["parameters_sha256"] != sha256_bytes(expected_parameters)
        or call["request"]["global_claim_bytes"] != len(claim_raw)
        or call["request"]["global_claim_sha256"] != sha256_bytes(claim_raw)
    ):
        fail("the observed HOST-002 request is invalid")
    response = call["response"]
    required_true = (
        "contract_valid",
        "deterministic_result_valid",
        "expected_record_id_match",
        "expected_title_match",
        "output_contract_valid",
        "receipt_present",
        "receipt_verification_valid",
        "structured_plain_text_parity",
    )
    if response["observed"] is not True or any(
        response[name] is not True for name in required_true
    ):
        fail("the observed HOST-002 response or inline receipt is invalid")
    if (
        response["record_id"] != EXPECTED_RECORD_ID
        or response["title"] != EXPECTED_TITLE
        or not isinstance(response["receipt_id"], str)
        or RECEIPT_ID.fullmatch(response["receipt_id"]) is None
        or total_operations != Counter({"catalogue.search": 1})
        or total_guard_calls != 0
    ):
        fail("the run widened or changed the bounded catalogue.search result")
    return summaries, total_methods, total_operations, total_guard_calls


def verify_output(
    root: Path,
    manifest: dict[str, Any],
    receipt_id: str,
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
        fail("Claude did not complete one bounded client run")
    stdout = read_private(root / "stdout.json", maximum=8 * 1_048_576, label="Claude stdout")
    stderr = read_private(root / "stderr.log", maximum=1_048_576, label="Claude stderr")
    if (
        len(stdout) != execution["stdout"]["bytes"]
        or sha256_bytes(stdout) != execution["stdout"]["sha256"]
        or len(stderr) != execution["stderr"]["bytes"]
        or sha256_bytes(stderr) != execution["stderr"]["sha256"]
    ):
        fail("Claude output files do not match the private run manifest")
    if TOKEN_PATTERN.search(stdout) or TOKEN_PATTERN.search(stderr):
        fail("Claude private output contains a recognised credential pattern")
    output = strict_object(stdout, label="Claude JSON output")
    structured = output.get("structured_output")
    model_usage = output.get("modelUsage")
    usage = output.get("usage")
    reported = model_usage.get(PINNED_MODEL) if isinstance(model_usage, dict) else None

    def token_count(mapping: Any, name: str, *, maximum: int) -> int | None:
        value = mapping.get(name) if isinstance(mapping, dict) else None
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value < 0
            or value > maximum
        ):
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
        output.get("type") != "result"
        or output.get("is_error") is not False
        or output.get("subtype") != "success"
        or output.get("permission_denials") != []
        or not isinstance(structured, dict)
        or set(structured) != {"record_id", "title", "receipt_id"}
        or structured["record_id"] != EXPECTED_RECORD_ID
        or structured["title"] != EXPECTED_TITLE
        or structured["receipt_id"] != receipt_id
        or not isinstance(model_usage, dict)
        or set(model_usage) != {PINNED_MODEL}
        or not isinstance(reported, dict)
        or bounded_aggregate != bounded_model
        or sum(bounded_aggregate[:3]) <= 0
        or sum(bounded_aggregate[:3]) > 10_000_000
        or bounded_aggregate[3] <= 0
        or isinstance(num_turns, bool)
        or num_turns != 2
    ):
        fail("Claude final structured output does not match the verified MCP result")
    return {
        **structured,
        "model_reported": PINNED_MODEL,
        "model_usage_observed": True,
        "input_tokens": sum(bounded_aggregate[:3]),
        "output_tokens": bounded_aggregate[3],
        "num_turns": num_turns,
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
        raw = read_private(private_root / facts["name"], maximum=8 * 1_048_576, label=name)
        if len(raw) != facts["bytes"] or sha256_bytes(raw) != facts["sha256"]:
            fail(f"{name} does not match the private manifest")
        private_raw[name] = raw
    verify_case(manifest)
    verify_private_configuration(
        private_root,
        manifest,
        private_raw["mcp_config"],
        private_raw["settings"],
    )
    source_check = source_verifier or verify_source_and_materials
    source_check(manifest)
    summaries, methods, operations, guard_calls = verify_sessions(
        private_root / "observer", manifest
    )
    call = next(summary for summary in summaries if summary["request"]["observed"])
    receipt_id = call["response"]["receipt_id"]
    model_result = verify_output(private_root, manifest, receipt_id)
    if methods["server/discover"] < 1 or methods["tools/list"] < 1:
        fail("Claude did not complete discovery and one-tool listing before capability use")
    source_check(manifest)
    projection = {
        "schema": "gis-ai-go.qual-206-claude-capability-evidence.v1",
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
            "guarded_provider_api_invocations": 0,
        },
        "case": {
            "id": "QUAL-206-HOST-002",
            "capability": "catalogue_search",
            "corpus_sha256": manifest["case"]["corpus_sha256"],
            "prompt_sha256": manifest["case"]["prompt_sha256"],
            "required_tool": "catalogue.search",
            "prompt_text_repeated_in_projection": False,
        },
        "transport": {
            "protocol": "2026-07-28",
            "kind": "operating-system-stdio-pipes",
            "session_count": len(summaries),
            "request_count": sum(methods.values()),
            "response_count": sum(methods.values()),
            "tool_call_count": operations["catalogue.search"],
            "only_catalogue_search_advertised": True,
            "resources_advertised": 0,
            "provider_egress_guard_calls": guard_calls,
        },
        "result": {
            "classification": "capability_pass",
            "capability": "passed",
            "record_id": call["response"]["record_id"],
            "title": call["response"]["title"],
            "receipt_id": receipt_id,
            "receipt_verification_valid": True,
            "model_output_match": True,
            "model_reported": model_result["model_reported"],
            "model_usage_observed": model_result["model_usage_observed"],
            "input_tokens": model_result["input_tokens"],
            "output_tokens": model_result["output_tokens"],
            "num_turns": model_result["num_turns"],
            "client_exit_code": manifest["execution"]["exit_code"],
        },
        "isolation": {
            "built_in_tools_available": False,
            "allowed_mcp_tool_count": 1,
            "claude_permission_alias": manifest["execution"]["allowed_mcp_tool"],
            "permission_mode": "dontAsk",
            "session_persistence": False,
            "maximum_turns": 1,
            "mcp_subtree_network_access_allowed": False,
            "mcp_subtree_network_sandbox": NETWORK_SANDBOX,
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
            "manifest_sha256": sha256_bytes(manifest_raw),
            "stdout_sha256": manifest["execution"]["stdout"]["sha256"],
            "stderr_sha256": manifest["execution"]["stderr"]["sha256"],
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
        fail("public projection may only be written to the interoperability evidence directory")
    encoded = (json.dumps(projection, ensure_ascii=False, indent=2) + "\n").encode()
    descriptor = os.open(
        output,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o644,
    )
    try:
        os.fchmod(descriptor, 0o644)
        offset = 0
        while offset < len(encoded):
            written = os.write(descriptor, encoded[offset:])
            if written <= 0:
                fail("public projection write made no progress")
            offset += written
        os.fsync(descriptor)
        opened = os.fstat(descriptor)
        named = output.lstat()
        if (
            (opened.st_dev, opened.st_ino) != (named.st_dev, named.st_ino)
            or opened.st_nlink != 1
            or stat.S_IMODE(opened.st_mode) != 0o644
            or opened.st_size != len(encoded)
        ):
            fail("public projection changed during publication")
    finally:
        os.close(descriptor)


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify one private Claude HOST-002 run and publish a pass-only projection."
    )
    parser.add_argument("--private-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    try:
        projection = verify_and_project(arguments.private_root)
        publish_projection(arguments.output, projection)
    except (OSError, CapabilityVerificationError, composite.VerificationError) as error:
        print(f"QUAL-206 Claude capability verification failed: {error}", file=sys.stderr)
        return 1
    print("QUAL-206 Claude HOST-002 capability pass verified and projected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
