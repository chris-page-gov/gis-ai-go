#!/usr/bin/env python3
"""Replay a private QUAL-206 local HTTP capture into a path-free projection."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import secrets
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, NoReturn
from urllib.parse import quote

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
PRIVATE_SCHEMA_RELATIVE = Path("schemas/qual-206-local-http-private-capture-v1.schema.json")
PUBLIC_SCHEMA_RELATIVE = Path("schemas/qual-206-local-http-transport-preflight.schema.json")
PRIVATE_SCHEMA_PATH = ROOT / PRIVATE_SCHEMA_RELATIVE
PUBLIC_SCHEMA_PATH = ROOT / PUBLIC_SCHEMA_RELATIVE
PRIVATE_SCHEMA_ID = "gis-ai-go.qual-206-local-http-private-capture.v1"
PUBLIC_SCHEMA_ID = "gis-ai-go.qual-206-local-http-transport-preflight.v1"
AUDIT_SCHEMA_ID = "gis-ai-go.qual-206-exact-five-http-audit.v1"
PROVIDER_EGRESS_GUARD_SCHEMA_ID = "gis-ai-go.qual-206-provider-egress-guard.v1"
EXACT_GUARDED_APIS = (
    "dns.Resolver.resolve4",
    "dns.Resolver.resolve6",
    "https.request",
)
OBSERVATION_DOMAIN = "gis-ai-go.qual-206-local-http-transport-preflight.observation.v1"
DOMAIN_PREFIX = f"GIS-AI-GO\0{OBSERVATION_DOMAIN}\0v1\0".encode()
CANONICAL_SCHEMA_VALIDATOR_RELATIVE = Path(
    "scripts/qual_206_validate_local_http_schemas.mjs"
)
CANONICAL_SCHEMA_VALIDATION_ID = "gis-ai-go.qual-206-local-http-schema-validation.v1"
GIT_EXECUTABLE = Path("/usr/bin/git")
MAX_CAPTURE_BYTES = 16 * 1_048_576
MAX_SCHEMA_BYTES = 1_048_576
MAX_SCHEMA_VALIDATOR_OUTPUT_BYTES = 4_096
MAX_MATERIAL_BYTES = 16 * 1_048_576
MAX_PUBLIC_BYTES = 1_048_576
FULL_GIT_OBJECT = re.compile(r"^[0-9a-f]{40}$")
RECEIPT_ID = re.compile(r"^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$")
RECORD_ID = re.compile(r"^gis-ai-go:public-evidence-record:sha256:[0-9a-f]{64}$")
LEDGER_EVENT_ID = re.compile(r"^gis-ai-go:evidence-ledger-event:sha256:[0-9a-f]{64}$")
RECONCILIATION_CLAIM_ID = re.compile(
    r"^gis-ai-go:evidence-reconciliation-claim:sha256:[0-9a-f]{64}$"
)
RECONCILIATION_RESOLUTION_ID = re.compile(
    r"^gis-ai-go:evidence-reconciliation-resolution:sha256:[0-9a-f]{64}$"
)
PUBLIC_IDEMPOTENCY_KEY = re.compile(r"^gis-ai-go:ik:v1:[0-9a-f]{64}$")
ABSOLUTE_WINDOWS_PATH = re.compile(r"^[A-Za-z]:[\\/]")
FORBIDDEN_PUBLIC_MEMBERS = frozenset({"host", "hostname", "port", "url", "endpoint"})
EXACT_OPERATIONS = (
    "catalogue.search",
    "catalogue.describe",
    "selection.resolve",
    "data.query",
    "evidence.inspect",
)
EXACT_RESOURCES = ("catalogue.public", "catalogue.record", "evidence.receipt")
EXACT_METHODS = (
    "server/discover",
    "tools/list",
    "resources/list",
    "resources/templates/list",
    "resources/read",
    "resources/read",
    "tools/call",
    "tools/call",
    "tools/call",
    "tools/call",
    "tools/call",
    "resources/read",
    "tools/call",
    "prompts/list",
)
EXACT_SUBJECTS = (
    "not-applicable",
    "not-applicable",
    "not-applicable",
    "not-applicable",
    "catalogue.public",
    "catalogue.record",
    "catalogue.search",
    "catalogue.describe",
    "selection.resolve",
    "data.query",
    "evidence.inspect",
    "evidence.receipt",
    "data.query",
    "not-applicable",
)
EXACT_SEMANTICS = (
    "discover-pass",
    "tools-list-pass",
    "resources-list-pass",
    "resource-templates-pass",
    "resource-read-pass",
    "resource-read-pass",
    "tool-success-pass",
    "tool-success-pass",
    "tool-success-pass",
    "tool-success-pass",
    "tool-success-pass",
    "resource-read-pass",
    "client-aborted-no-completed-evidence",
    "expected-method-not-found",
)
OPERATION_PATHS = {
    "catalogue.search": "/catalogue/search",
    "catalogue.describe": "/catalogue/describe",
    "selection.resolve": "/selection/resolve",
    "data.query": "/data/query",
    "evidence.inspect": "/evidence/inspect",
}
OPENAPI_OPERATION_CONTRACTS = {
    "catalogue.search": {
        "path": "/catalogue/search",
        "operation_id": "catalogueSearch",
        "input_component": "CatalogueSearchRequest",
        "output_component": "CatalogueSearchResult",
    },
    "catalogue.describe": {
        "path": "/catalogue/describe",
        "operation_id": "catalogueDescribe",
        "input_component": "CatalogueDescribeRequest",
        "output_component": "CatalogueDescribeResult",
    },
    "selection.resolve": {
        "path": "/selection/resolve",
        "operation_id": "selectionResolve",
        "input_component": "SelectionResolveRequest",
        "output_component": "SelectionResolveResult",
    },
    "data.query": {
        "path": "/data/query",
        "operation_id": "dataQuery",
        "input_component": "DataQueryRequest",
        "output_component": "DataQueryResult",
    },
    "evidence.inspect": {
        "path": "/evidence/inspect",
        "operation_id": "evidenceInspect",
        "input_component": "EvidenceInspectRequest",
        "output_component": "EvidenceInspectResult",
    },
}
OPENAPI_INFRASTRUCTURE_CONTRACTS = {
    "/healthz": {"operation_id": "healthCheck", "component": "Health"},
    "/readyz": {"operation_id": "readinessCheck", "component": "Readiness"},
    "/openapi.json": {"operation_id": "openApiContract", "component": None},
}
EXACT_OPENAPI_PATHS = frozenset(
    {
        *(contract["path"] for contract in OPENAPI_OPERATION_CONTRACTS.values()),
        *OPENAPI_INFRASTRUCTURE_CONTRACTS,
    }
)
IDEMPOTENCY_KEY_DOMAIN = "gis-ai-go.idempotency-key.v1"
CANONICAL_DIGEST_PREFIX = b"GIS-AI-GO\0canonical-json\0sha256\0v1\0"
SOURCE_MATERIAL_PATHS = (
    "scripts/qual_206_local_http_preflight.mjs",
    "scripts/qual_206_verify_local_http_preflight.py",
    str(CANONICAL_SCHEMA_VALIDATOR_RELATIVE),
    str(PUBLIC_SCHEMA_RELATIVE),
    str(PRIVATE_SCHEMA_RELATIVE),
    "artifacts/okf/manifest.json",
    "artifacts/okf/okf-bundle.json",
    "scripts/qual_206_exact_five_event_collector.mjs",
    "tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs",
    "apps/mcp-gateway/test/fixtures/qual-206-exact-five-http-server.mjs",
    "apps/mcp-gateway/dist/src/mcp-http.js",
    "apps/mcp-gateway/dist/src/mcp-server.js",
)
EXPECTED_DERIVED_UNTRACKED_MATERIALS = frozenset(
    {
        "artifacts/okf/manifest.json",
        "artifacts/okf/okf-bundle.json",
        "apps/mcp-gateway/dist/src/mcp-http.js",
        "apps/mcp-gateway/dist/src/mcp-server.js",
    }
)


class VerificationError(ValueError):
    """Private capture or derived projection failed its closed contract."""


def fail(message: str) -> NoReturn:
    raise VerificationError(message)


def reject_duplicate_members(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, member in pairs:
        if key in value:
            fail("JSON contains a duplicate object member")
        value[key] = member
    return value


def reject_non_standard_number(value: str) -> NoReturn:
    fail(f"JSON contains the non-standard number {value}")


def parse_json_text(text: str, label: str) -> dict[str, Any]:
    if text.startswith("\ufeff"):
        fail(f"{label} must not contain a byte-order mark")
    try:
        value = json.loads(
            text,
            object_pairs_hook=reject_duplicate_members,
            parse_constant=reject_non_standard_number,
        )
    except (json.JSONDecodeError, RecursionError) as error:
        raise VerificationError(f"{label} is not one strict JSON object") from error
    if not isinstance(value, dict):
        fail(f"{label} must contain one JSON object")
    return value


def parse_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise VerificationError(f"{label} is not strict UTF-8") from error
    return parse_json_text(text, label)


def bounded_regular_file(
    path: Path,
    maximum: int,
    label: str,
    *,
    owner_only: bool = False,
) -> bytes:
    try:
        before = path.stat(follow_symlinks=False)
    except OSError as error:
        raise VerificationError(f"{label} cannot be read") from error
    if not stat.S_ISREG(before.st_mode) or path.is_symlink():
        fail(f"{label} must be one regular non-symbolic-link file")
    if owner_only and (
        before.st_uid != os.getuid()
        or before.st_nlink != 1
        or (before.st_mode & 0o777) != 0o600
    ):
        fail(f"{label} must be one owner-owned, singly linked 0600 file")
    if before.st_size < 1 or before.st_size > maximum:
        fail(f"{label} is outside its byte bound")
    raw = path.read_bytes()
    after = path.stat(follow_symlinks=False)
    if (
        len(raw) != before.st_size
        or before.st_dev != after.st_dev
        or before.st_ino != after.st_ino
        or before.st_mode != after.st_mode
        or before.st_uid != after.st_uid
        or before.st_nlink != after.st_nlink
        or before.st_size != after.st_size
        or before.st_mtime_ns != after.st_mtime_ns
    ):
        fail(f"{label} changed while it was read")
    return raw


def exact_private_capture_path(path: Path) -> Path:
    if not path.is_absolute():
        fail("Private capture path must be canonical and absolute")
    try:
        canonical_path = path.resolve(strict=True)
        canonical_parent = path.parent.resolve(strict=True)
        named = path.stat(follow_symlinks=False)
        parent = path.parent.stat(follow_symlinks=False)
    except OSError as error:
        raise VerificationError("Private capture path cannot be resolved") from error
    if (
        canonical_path != path
        or canonical_parent != path.parent
        or stat.S_ISLNK(named.st_mode)
        or stat.S_ISLNK(parent.st_mode)
    ):
        fail("Private capture path and parent must not traverse a symbolic link")
    try:
        canonical_path.relative_to(ROOT)
    except ValueError:
        pass
    else:
        fail("Private capture must be outside the repository")
    if (
        not stat.S_ISDIR(parent.st_mode)
        or parent.st_uid != os.getuid()
        or parent.st_nlink < 2
        or (parent.st_mode & 0o777) != 0o700
    ):
        fail("Private capture parent must be one owner-owned 0700 directory")
    return path


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def exact_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        fail(f"{label} does not have its exact closed members")
    return value


def canonical_json(value: Any) -> str:
    if value is None or isinstance(value, (bool, str)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value) or not value.is_integer():
            fail("Canonical projection numbers must be finite integers")
        return str(int(value))
    if isinstance(value, list):
        return "[" + ",".join(canonical_json(member) for member in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(
            f"{canonical_json(key)}:{canonical_json(value[key])}"
            for key in sorted(value)
        ) + "}"
    fail("Canonical projection contains an unsupported value")


def public_idempotency_key_sha256(value: Any) -> str:
    if (
        not isinstance(value, str)
        or not PUBLIC_IDEMPOTENCY_KEY.fullmatch(value)
        or value == f"gis-ai-go:ik:v1:{'0' * 64}"
    ):
        fail("Private data-query request has an invalid idempotency key")
    material = canonical_json({"operation": "data.query", "key": value}).encode()
    return sha256(
        CANONICAL_DIGEST_PREFIX
        + IDEMPOTENCY_KEY_DOMAIN.encode()
        + b"\0"
        + material
    )


def observation_sha256(projection: dict[str, Any]) -> str:
    verification = projection["verification"]
    normalised = {
        **projection,
        "verification": {**verification, "observation_sha256": None},
    }
    return sha256(DOMAIN_PREFIX + canonical_json(normalised).encode())


def schema_validator(path: Path, label: str) -> tuple[bytes, Draft202012Validator]:
    raw = bounded_regular_file(path, MAX_SCHEMA_BYTES, label)
    schema = parse_json_bytes(raw, label)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as error:
        raise VerificationError(f"{label} is not valid Draft 2020-12 JSON Schema") from error
    return raw, Draft202012Validator(schema, format_checker=FormatChecker())


def validate_with_schema(
    value: dict[str, Any],
    validator: Draft202012Validator,
    label: str,
) -> None:
    if next(validator.iter_errors(value), None) is not None:
        # jsonschema messages and instance paths can reproduce private instance
        # values. Keep the CLI failure useful without reflecting either surface.
        fail(f"{label} failed its closed schema contract")


def executable_state(path: Path) -> tuple[int, int, int, int, int, int, int]:
    metadata = path.stat(follow_symlinks=False)
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_uid,
        metadata.st_nlink,
        metadata.st_size,
        metadata.st_mtime_ns,
    )


def trusted_node_executable() -> tuple[Path, tuple[int, int, int, int, int, int, int]]:
    selected = shutil.which("node")
    if selected is None:
        fail("Canonical exact-five schema validator requires Node.js")
    try:
        executable = Path(selected).resolve(strict=True)
        metadata = executable.stat(follow_symlinks=False)
    except OSError as error:
        raise VerificationError("Node.js executable identity could not be verified") from error
    try:
        executable.relative_to(ROOT)
    except ValueError:
        pass
    else:
        fail("Node.js executable must be outside the repository")
    if (
        not executable.is_absolute()
        or not stat.S_ISREG(metadata.st_mode)
        or metadata.st_nlink < 1
        or metadata.st_mode & 0o022
        or not os.access(executable, os.X_OK)
    ):
        fail("Node.js executable is not a trusted regular executable")
    return executable, executable_state(executable)


def validate_canonical_tool_schemas(tools: list[Any]) -> None:
    """Compare advertised schemas with the canonical exact-five schema material."""
    try:
        tool_bytes = json.dumps(
            tools,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode()
    except (TypeError, ValueError, RecursionError) as error:
        raise VerificationError("Advertised tool schemas are not bounded JSON") from error
    if len(tool_bytes) < 1 or len(tool_bytes) > MAX_SCHEMA_BYTES:
        fail("Advertised tool schemas are outside the canonical validator byte bound")
    validator = ROOT / CANONICAL_SCHEMA_VALIDATOR_RELATIVE
    node, node_before = trusted_node_executable()
    environment = {
        "CI": "1",
        "LANG": "C",
        "LC_ALL": "C",
        "NO_COLOR": "1",
        "TZ": "UTC",
    }
    try:
        completed = subprocess.run(
            [str(node), str(validator), "--stdin-tools-list-only"],
            cwd=ROOT,
            check=False,
            input=tool_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=environment,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise VerificationError(
            "Canonical exact-five schema validator could not be executed"
        ) from error
    try:
        node_after = executable_state(node)
    except OSError as error:
        raise VerificationError("Node.js executable identity could not be rechecked") from error
    if node_after != node_before:
        fail("Node.js executable changed during canonical schema validation")
    if (
        len(completed.stdout) > MAX_SCHEMA_VALIDATOR_OUTPUT_BYTES
        or len(completed.stderr) > MAX_SCHEMA_VALIDATOR_OUTPUT_BYTES
    ):
        fail("Canonical exact-five schema validator exceeded its output bound")
    if completed.stderr != b"":
        fail("Canonical exact-five schema validator wrote to stderr")
    result = parse_json_bytes(completed.stdout, "Canonical exact-five schema validation")
    exact_keys(
        result,
        {"schema", "valid"},
        "Canonical exact-five schema validation",
    )
    if (
        result["schema"] != CANONICAL_SCHEMA_VALIDATION_ID
        or result["valid"] is not True
        or completed.returncode != 0
    ):
        fail("Advertised input or output schemas differ from the canonical exact-five schemas")


def object_member(value: Any, key: str, label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not isinstance(value.get(key), dict):
        fail(f"{label} is not one JSON object")
    return value[key]


def response_schema(
    operation: dict[str, Any],
    status: str,
    media_type: str,
    label: str,
) -> dict[str, Any]:
    responses = object_member(operation, "responses", f"{label} responses")
    response = object_member(responses, status, f"{label} {status} response")
    content = object_member(response, "content", f"{label} {status} content")
    media = object_member(content, media_type, f"{label} {status} media type")
    return object_member(media, "schema", f"{label} {status} schema")


def openapi_component_matches_mcp(
    operation: str,
    direction: str,
    component: Any,
    advertised: Any,
) -> bool:
    if component == advertised:
        return True
    if (
        operation == "evidence.inspect"
        and direction == "input"
        and isinstance(component, dict)
        and "type" not in component
        and isinstance(advertised, dict)
    ):
        # The pinned MCP SDK adds this one redundant object type to a oneOf
        # dispatcher. The canonical tool-schema bridge proves that exact SDK
        # normalisation separately; no other OpenAPI/MCP divergence is accepted.
        return advertised == {**component, "type": "object"}
    return False


def validate_openapi_callable_contract(
    openapi: dict[str, Any],
    tools: list[Any],
) -> None:
    """Prove the exact advertised direct-call surface and its MCP schema bindings."""
    paths = openapi.get("paths")
    if not isinstance(paths, dict) or set(paths) != EXACT_OPENAPI_PATHS:
        fail("OpenAPI does not advertise its exact closed path set")
    components = object_member(openapi, "components", "OpenAPI components")
    schemas = object_member(components, "schemas", "OpenAPI component schemas")
    tool_by_name = {
        tool.get("name"): tool
        for tool in tools
        if isinstance(tool, dict) and isinstance(tool.get("name"), str)
    }
    if set(tool_by_name) != set(EXACT_OPERATIONS):
        fail("OpenAPI schema binding did not receive the exact-five tool set")

    operation_ids: list[str] = []
    for name in EXACT_OPERATIONS:
        contract = OPENAPI_OPERATION_CONTRACTS[name]
        path = contract["path"]
        path_item = exact_keys(paths[path], {"post"}, f"OpenAPI path {path}")
        operation = object_member(path_item, "post", f"OpenAPI operation {path}")
        operation_id = operation.get("operationId")
        if (
            operation_id != contract["operation_id"]
            or operation.get("x-gis-ai-go-operation") != name
            or operation.get("x-gis-ai-go-lifecycle") != "candidate-conformance-only"
        ):
            fail(f"OpenAPI operation identity for {name} changed")
        operation_ids.append(operation_id)

        request_body = object_member(
            operation,
            "requestBody",
            f"OpenAPI {name} request body",
        )
        request_content = object_member(
            request_body,
            "content",
            f"OpenAPI {name} request content",
        )
        request_media = object_member(
            request_content,
            "application/json",
            f"OpenAPI {name} request media type",
        )
        request_schema = object_member(
            request_media,
            "schema",
            f"OpenAPI {name} request schema",
        )
        input_component = contract["input_component"]
        output_component = contract["output_component"]
        if (
            request_body.get("required") is not True
            or request_schema != {"$ref": f"#/components/schemas/{input_component}"}
            or response_schema(operation, "200", "application/json", name)
            != {"$ref": f"#/components/schemas/{output_component}"}
        ):
            fail(f"OpenAPI request or success schema reference for {name} changed")
        tool = tool_by_name[name]
        if (
            not openapi_component_matches_mcp(
                name,
                "input",
                schemas.get(input_component),
                tool.get("inputSchema"),
            )
            or not openapi_component_matches_mcp(
                name,
                "output",
                schemas.get(output_component),
                tool.get("outputSchema"),
            )
        ):
            fail(f"OpenAPI component schemas for {name} differ from MCP")

    for path, contract in OPENAPI_INFRASTRUCTURE_CONTRACTS.items():
        path_item = exact_keys(paths[path], {"get"}, f"OpenAPI path {path}")
        operation = object_member(path_item, "get", f"OpenAPI operation {path}")
        operation_id = operation.get("operationId")
        if operation_id != contract["operation_id"]:
            fail(f"OpenAPI operation identity for {path} changed")
        operation_ids.append(operation_id)
        component = contract["component"]
        if component is None:
            if response_schema(operation, "200", "application/json", path) != {
                "type": "object"
            }:
                fail("OpenAPI contract-reader success schema changed")
            continue
        statuses = ("200", "503") if path == "/readyz" else ("200",)
        for status in statuses:
            if response_schema(operation, status, "application/json", path) != {
                "$ref": f"#/components/schemas/{component}"
            }:
                fail(f"OpenAPI infrastructure schema binding for {path} changed")
        if not isinstance(schemas.get(component), dict):
            fail(f"OpenAPI infrastructure component {component} is absent")

    if len(set(operation_ids)) != len(operation_ids):
        fail("OpenAPI operation identities are not unique")


def git_bytes(*arguments: str) -> bytes:
    environment = {
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": "/usr/bin:/bin",
    }
    try:
        completed = subprocess.run(
            [
                str(GIT_EXECUTABLE),
                "--no-replace-objects",
                "-c",
                "core.fsmonitor=false",
                "-c",
                "core.untrackedCache=false",
                *arguments,
            ],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=environment,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise VerificationError("Current Git source identity could not be verified") from error
    if len(completed.stdout) > 20 * 1_048_576 or len(completed.stderr) > 1_048_576:
        fail("Current Git source identity exceeded its output bound")
    return completed.stdout


def git_text(*arguments: str) -> str:
    try:
        return git_bytes(*arguments).decode("utf-8", errors="strict").strip()
    except UnicodeDecodeError as error:
        raise VerificationError("Current Git source identity is not UTF-8") from error


def verify_safe_clean_index() -> None:
    for flag in ("-v", "-f"):
        rows = git_bytes("ls-files", flag, "-z").split(b"\0")
        for row in rows:
            if row and not row.startswith(b"H "):
                fail(
                    "A passing clean source must not use assume-unchanged, "
                    "skip-worktree or filesystem-monitor index state"
                )


def verify_named_materials_match_tree(
    source: dict[str, Any], materials: list[dict[str, str]]
) -> None:
    if source["working_tree_clean"] is not True:
        return
    for material in materials:
        relative = material["path"]
        entry = git_text("ls-tree", "--full-tree", source["tree"], "--", relative)
        if entry == "":
            if relative not in EXPECTED_DERIVED_UNTRACKED_MATERIALS:
                fail(f"Clean source material {relative} is absent from the Git tree")
            continue
        match = re.fullmatch(
            r"(?:100644|100755) blob ([0-9a-f]{40})\t(.+)",
            entry,
        )
        if match is None or match.group(2) != relative:
            fail(f"Git tree entry for source material {relative} is not one regular blob")
        tree_bytes = git_bytes("cat-file", "blob", match.group(1))
        if len(tree_bytes) < 1 or len(tree_bytes) > MAX_MATERIAL_BYTES:
            fail(f"Git tree blob for source material {relative} is outside its byte bound")
        if sha256(tree_bytes) != material["sha256"]:
            fail(f"Clean source material {relative} differs from its recorded Git tree blob")


def verify_clean_current_source(source: dict[str, Any]) -> None:
    try:
        repository_root = Path(git_text("rev-parse", "--show-toplevel")).resolve(
            strict=True
        )
    except OSError as error:
        raise VerificationError("Current Git repository root could not be verified") from error
    if repository_root != ROOT:
        fail("Current Git repository root does not match the verifier repository")
    commit = git_text("rev-parse", "HEAD")
    tree = git_text("rev-parse", "HEAD^{tree}")
    status = git_text("status", "--porcelain=v1", "--untracked-files=all")
    if not FULL_GIT_OBJECT.fullmatch(commit) or not FULL_GIT_OBJECT.fullmatch(tree):
        fail("Current Git source identity is malformed")
    if source["commit"] != commit or source["tree"] != tree:
        fail("Private capture does not match the current Git commit and tree")
    if source["working_tree_clean"] is not True or status != "":
        fail("A passing durable projection requires one clean current worktree")
    verify_safe_clean_index()


def raw_exchange(
    captured: dict[str, Any], ordinal: int
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    if captured["ordinal"] != ordinal:
        fail("Private request ordinals are not exact and contiguous")
    request_raw = captured["request_json"].encode()
    if len(request_raw) != captured["request_bytes"]:
        fail(f"Request {ordinal} byte count does not match raw JSON")
    request = parse_json_bytes(request_raw, f"Request {ordinal}")
    response_text = captured["response_json"]
    if response_text is None:
        if captured["response_bytes"] != 0 or captured["transport_outcome"] != "client-aborted":
            fail(f"Request {ordinal} has an invalid absent response")
        return request, None
    response_raw = response_text.encode()
    if len(response_raw) != captured["response_bytes"]:
        fail(f"Response {ordinal} byte count does not match raw JSON")
    if captured["transport_outcome"] != "response":
        fail(f"Request {ordinal} has an invalid transport outcome")
    return request, parse_json_bytes(response_raw, f"Response {ordinal}")


def validate_meta(params: dict[str, Any], label: str) -> None:
    meta = exact_keys(
        params.get("_meta"),
        {
            "io.modelcontextprotocol/protocolVersion",
            "io.modelcontextprotocol/clientCapabilities",
            "io.modelcontextprotocol/clientInfo",
        },
        f"{label} metadata",
    )
    client = exact_keys(
        meta["io.modelcontextprotocol/clientInfo"],
        {"name", "version"},
        f"{label} client identity",
    )
    if (
        meta["io.modelcontextprotocol/protocolVersion"] != "2026-07-28"
        or meta["io.modelcontextprotocol/clientCapabilities"] != {}
        or client != {"name": "gis-ai-go-local-http-preflight", "version": "1.0.0"}
    ):
        fail(f"{label} modern-protocol metadata changed")


def result_of(message: Any, request_id: Any, label: str) -> dict[str, Any]:
    exact_keys(message, {"jsonrpc", "id", "result"}, label)
    if message["jsonrpc"] != "2.0" or message["id"] != request_id:
        fail(f"{label} is not correlated to its request")
    if not isinstance(message["result"], dict):
        fail(f"{label} result is not an object")
    return message["result"]


def catalogue_expectations() -> dict[str, Any]:
    manifest = parse_json_bytes(
        bounded_regular_file(
            ROOT / "artifacts/okf/manifest.json", MAX_MATERIAL_BYTES, "OKF manifest"
        ),
        "OKF manifest",
    )
    bundle = parse_json_bytes(
        bounded_regular_file(
            ROOT / "artifacts/okf/okf-bundle.json", MAX_MATERIAL_BYTES, "OKF bundle"
        ),
        "OKF bundle",
    )
    revision = manifest.get("revision")
    if not isinstance(revision, str) or not FULL_GIT_OBJECT.fullmatch(revision):
        fail("OKF manifest revision is invalid")
    if bundle.get("revision") != revision or bundle.get("recordCount") != len(
        bundle.get("records", [])
    ):
        fail("OKF bundle does not match its manifest")
    records = [record for record in bundle["records"] if record.get("id") == "LR-Q003"]
    if len(records) != 1:
        fail("OKF bundle does not contain exactly one LR-Q003 record")
    return {"bundle": bundle, "record": records[0], "revision": revision}


def validate_tool_result(
    operation: str,
    result: dict[str, Any],
    output_schema: dict[str, Any],
    expected_catalogue: dict[str, Any],
    search_receipt: str | None,
) -> tuple[dict[str, Any], str]:
    exact_keys(result, {"_meta", "content", "resultType", "structuredContent"}, operation)
    structured = result["structuredContent"]
    contents = result["content"]
    expected_text = json.dumps(structured, ensure_ascii=False, separators=(",", ":"))
    if (
        result["resultType"] != "complete"
        or not isinstance(structured, dict)
        or not isinstance(contents, list)
        or len(contents) != 1
        or contents[0] != {"type": "text", "text": expected_text}
    ):
        fail(f"{operation} structured and plain-text representations differ")
    try:
        errors = list(Draft202012Validator(output_schema).iter_errors(structured))
    except Exception as error:
        raise VerificationError(f"{operation} output schema could not be replayed") from error
    if errors:
        fail(f"{operation} result violates its advertised output schema")
    receipt = structured.get("evidence_receipt", {}).get("receipt_id")
    if not isinstance(receipt, str) or not RECEIPT_ID.fullmatch(receipt):
        fail(f"{operation} has no valid evidence receipt")
    if operation == "catalogue.search":
        records = structured.get("data", {}).get("records", [])
        passed = (
            structured.get("schema") == "gis-ai-go.catalogue-result.v1"
            and structured.get("catalogue", {}).get("record_count") == 36
            and structured.get("catalogue", {}).get("revision") == expected_catalogue["revision"]
            and len(records) == 1
            and records[0].get("id") == "hmlr:dataset:inspire-index-polygons"
        )
    elif operation == "catalogue.describe":
        record = structured.get("data", {}).get("record", {})
        passed = record.get("id") == "LR-Q003" and record.get("status") == "candidate-non-executing"
    elif operation == "selection.resolve":
        data = structured.get("data", {})
        passed = (
            data.get("status") == "resolved"
            and data.get("ambiguity") is None
            and data.get("ranking", {}).get("selected_candidate_id")
            == "PV-ONS-DATA:weekly-deaths-region:time-series:121"
        )
    elif operation == "data.query":
        observations = structured.get("data", {}).get("observations", [])
        passed = (
            structured.get("schema") == "gis-ai-go.data-query-result.v1"
            and structured.get("data", {}).get("status") == "succeeded"
            and len(observations) == 1
            and observations[0].get("value") == "10471"
        )
    else:
        passed = (
            search_receipt is not None
            and structured.get("schema") == "gis-ai-go.evidence-inspect-result.v3"
            and structured.get("verification", {}).get("status") == "passed"
            and structured.get("verification", {}).get("ledger") == "restart-verified"
            and structured.get("data", {}).get("record", {}).get("receipt", {}).get("receipt_id")
            == search_receipt
        )
    if not passed:
        fail(f"{operation} deterministic result facts did not replay")
    return structured, receipt


def validate_idempotency_evidence(
    events: tuple[dict[str, Any], dict[str, Any]],
    successful_arguments: dict[str, Any],
    aborted_arguments: dict[str, Any],
    successful_receipt: str,
) -> None:
    event_keys = {
        "schema",
        "event",
        "role",
        "idempotency_key_sha256",
        "reconciliation_status",
        "claim_id",
        "resolution_id",
        "receipt_id",
        "record_id",
        "ledger_event_id",
        "ledger_event_sequence",
        "completed_evidence_created",
    }
    successful, aborted = events
    for event, role in ((successful, "successful"), (aborted, "aborted")):
        exact_keys(event, event_keys, f"{role.title()} idempotency evidence event")
        if (
            event["schema"] != "gis-ai-go.qual-206-exact-five-http-audit.v1"
            or event["event"] != "idempotency-evidence-state"
            or event["role"] != role
        ):
            fail(f"{role.title()} idempotency evidence identity changed")

    successful_key = successful_arguments.get("idempotency_key")
    aborted_key = aborted_arguments.get("idempotency_key")
    successful_digest = public_idempotency_key_sha256(successful_key)
    aborted_digest = public_idempotency_key_sha256(aborted_key)
    if successful_key == aborted_key or successful_digest == aborted_digest:
        fail("Successful and aborted data-query idempotency identities are not distinct")
    if (
        successful["idempotency_key_sha256"] != successful_digest
        or aborted["idempotency_key_sha256"] != aborted_digest
    ):
        fail("Private idempotency evidence is not bound to the captured requests")

    if (
        successful["reconciliation_status"] != "completed"
        or successful["completed_evidence_created"] is not True
        or not isinstance(successful["claim_id"], str)
        or not RECONCILIATION_CLAIM_ID.fullmatch(successful["claim_id"])
        or not isinstance(successful["resolution_id"], str)
        or not RECONCILIATION_RESOLUTION_ID.fullmatch(successful["resolution_id"])
        or successful["receipt_id"] != successful_receipt
        or not isinstance(successful["record_id"], str)
        or not RECORD_ID.fullmatch(successful["record_id"])
        or not isinstance(successful["ledger_event_id"], str)
        or not LEDGER_EVENT_ID.fullmatch(successful["ledger_event_id"])
        or successful["ledger_event_sequence"] != 4
    ):
        fail("The successful data-query key is not bound to its completed ledger evidence")
    if (
        aborted["reconciliation_status"] != "pending"
        or aborted["completed_evidence_created"] is not False
        or not isinstance(aborted["claim_id"], str)
        or not RECONCILIATION_CLAIM_ID.fullmatch(aborted["claim_id"])
        or aborted["resolution_id"] is not None
        or aborted["receipt_id"] is not None
        or aborted["record_id"] is not None
        or aborted["ledger_event_id"] is not None
        or aborted["ledger_event_sequence"] is not None
    ):
        fail("The aborted data-query key acquired completed evidence")


def validate_audit(
    capture: dict[str, Any],
    successful_arguments: dict[str, Any],
    aborted_arguments: dict[str, Any],
    successful_receipt: str,
) -> None:
    events = [
        parse_json_text(line, f"Audit event {index}")
        for index, line in enumerate(capture["audit_lines"], 1)
    ]
    names = tuple(event.get("event") for event in events)
    expected_names = (
        "provider-egress-guard-ready",
        "server-listening",
        "provider-transport-started",
        "provider-transport-started",
        "provider-transport-aborted",
        "provider-egress-guard-summary",
        "idempotency-evidence-state",
        "idempotency-evidence-state",
        "session-summary",
    )
    if names != expected_names:
        fail("Private audit event order or cardinality changed")
    (
        guard_ready,
        listening,
        started_one,
        started_two,
        aborted_two,
        guard_summary,
        successful_evidence,
        aborted_evidence,
        summary,
    ) = events
    exact_keys(guard_ready, {"schema", "event", "guarded_apis"}, "Guard ready event")
    canonical_guarded_apis = list(EXACT_GUARDED_APIS)
    if (
        guard_ready["schema"] != PROVIDER_EGRESS_GUARD_SCHEMA_ID
        or guard_ready["guarded_apis"] != canonical_guarded_apis
    ):
        fail("Provider egress guard ready contract changed")
    exact_keys(
        listening,
        {
            "schema",
            "event",
            "scenario",
            "source_commit",
            "transport",
            "host",
            "port",
            "state",
            "production_registration",
        },
        "Server listening event",
    )
    if (
        listening["schema"] != AUDIT_SCHEMA_ID
        or listening["scenario"] != "capability-pack"
        or listening["source_commit"] != capture["source"]["commit"]
        or listening["transport"] != "operating-system-loopback-http"
        or listening["host"] != capture["fixture"]["host"]
        or listening["port"] != capture["fixture"]["port"]
        or listening["state"] != "candidate-unregistered"
        or listening["production_registration"] is not False
    ):
        fail("Server listening event does not bind the private capture")
    for event, ordinal in ((started_one, 1), (started_two, 2), (aborted_two, 2)):
        exact_keys(event, {"schema", "event", "scenario", "ordinal"}, "Provider audit event")
        if (
            event["schema"] != AUDIT_SCHEMA_ID
            or event["scenario"] != "capability-pack"
            or event["ordinal"] != ordinal
        ):
            fail("Provider audit event sequence changed")
    exact_keys(
        guard_summary,
        {"schema", "event", "guarded_apis", "guarded_api_invocation_count"},
        "Guard summary",
    )
    if (
        guard_summary["schema"] != PROVIDER_EGRESS_GUARD_SCHEMA_ID
        or guard_summary["guarded_apis"] != canonical_guarded_apis
        or guard_summary["guarded_apis"] != guard_ready["guarded_apis"]
        or guard_summary["guarded_api_invocation_count"] != 0
    ):
        fail("Provider egress guard observed an external invocation")
    validate_idempotency_evidence(
        (successful_evidence, aborted_evidence),
        successful_arguments,
        aborted_arguments,
        successful_receipt,
    )
    exact_keys(
        summary,
        {
            "schema", "event", "scenario", "source_commit", "transport", "host", "state",
            "production_registration", "operations", "resources", "suspensions",
            "provider_transport_calls", "aborted_provider_calls", "ledger_event_count",
            "reported_error_count", "private_state_root_mode", "guarded_api_invocation_count",
        },
        "Fixture summary",
    )
    expected = {
        "schema": AUDIT_SCHEMA_ID,
        "event": "session-summary",
        "scenario": "capability-pack",
        "source_commit": capture["source"]["commit"],
        "transport": "operating-system-loopback-http",
        "host": "127.0.0.1",
        "state": "candidate-unregistered",
        "production_registration": False,
        "operations": list(EXACT_OPERATIONS),
        "resources": list(EXACT_RESOURCES),
        "suspensions": [],
        "provider_transport_calls": 2,
        "aborted_provider_calls": 1,
        "ledger_event_count": 4,
        "reported_error_count": 0,
        "private_state_root_mode": "0700",
        "guarded_api_invocation_count": 0,
    }
    for key, value in expected.items():
        if summary[key] != value:
            fail(f"Fixture summary field {key} changed")
    if summary["guarded_api_invocation_count"] != guard_summary[
        "guarded_api_invocation_count"
    ]:
        fail("Fixture summary does not agree with the provider egress guard summary")


def replay_capture(capture: dict[str, Any]) -> dict[str, Any]:
    expected_catalogue = catalogue_expectations()
    requests: list[dict[str, Any]] = []
    responses: list[dict[str, Any] | None] = []
    ids: set[Any] = set()
    for ordinal, captured in enumerate(capture["requests"], 1):
        request, response = raw_exchange(captured, ordinal)
        exact_keys(request, {"jsonrpc", "id", "method", "params"}, f"Request {ordinal}")
        if request["jsonrpc"] != "2.0" or request["method"] != EXACT_METHODS[ordinal - 1]:
            fail(f"Request {ordinal} does not match the canonical method sequence")
        if not isinstance(request["id"], (str, int)) or request["id"] in ids:
            fail("JSON-RPC request IDs are not unique bounded scalars")
        ids.add(request["id"])
        if not isinstance(request["params"], dict):
            fail(f"Request {ordinal} parameters are not an object")
        validate_meta(request["params"], f"Request {ordinal}")
        requests.append(request)
        responses.append(response)

    discover = result_of(responses[0], requests[0]["id"], "Discovery response")
    if discover.get("supportedVersions") != ["2026-07-28"]:
        fail("Discovery did not return the exact protocol target")
    listed = result_of(responses[1], requests[1]["id"], "Tool listing response")
    tools = listed.get("tools")
    tool_names = [tool.get("name") for tool in tools] if isinstance(tools, list) else []
    if len(set(tool_names)) != 5 or sorted(tool_names) != sorted(EXACT_OPERATIONS):
        fail("Tool listing is not the unique exact-five set")
    validate_canonical_tool_schemas(tools)
    output_schemas: dict[str, dict[str, Any]] = {}
    for tool in tools:
        if (
            not isinstance(tool, dict)
            or not isinstance(tool.get("inputSchema"), dict)
            or not isinstance(tool.get("outputSchema"), dict)
        ):
            fail("Advertised tool schemas are not objects")
        output_schemas[tool["name"]] = tool["outputSchema"]
    resources = result_of(responses[2], requests[2]["id"], "Resource listing response")
    if [item.get("uri") for item in resources.get("resources", [])] != [
        "gis-ai-go://catalogue/public"
    ]:
        fail("Resource listing is not the exact fixed catalogue resource")
    templates = result_of(responses[3], requests[3]["id"], "Resource template response")
    if [item.get("uriTemplate") for item in templates.get("resourceTemplates", [])] != [
        "gis-ai-go://catalogue/records/{record_id}",
        "gis-ai-go://evidence/receipts/{receipt_id}",
    ]:
        fail("Resource templates are not the exact fixed pair")

    openapi_raw = capture["openapi"]["response_json"].encode()
    if len(openapi_raw) != capture["openapi"]["response_bytes"]:
        fail("OpenAPI response byte count does not match raw JSON")
    openapi = parse_json_bytes(openapi_raw, "OpenAPI response")
    if (
        openapi.get("x-gis-ai-go-lifecycle") != "candidate-unregistered"
        or openapi.get("x-gis-ai-go-production-registration") is not False
        or openapi.get("x-gis-ai-go-candidate-operations") != list(EXACT_OPERATIONS)
        or openapi.get("x-gis-ai-go-mounted-candidate-operations")
        != [
            "catalogue.describe",
            "catalogue.search",
            "evidence.inspect",
            "selection.resolve",
            "data.query",
        ]
        or openapi.get("x-gis-ai-go-mounted-candidate-catalogue-operations")
        != ["catalogue.describe", "catalogue.search"]
    ):
        fail("OpenAPI direct-operation projection differs from MCP")
    validate_openapi_callable_contract(openapi, tools)
    paths = openapi["paths"]
    readiness_raw = capture["readiness"]["response_json"].encode()
    if len(readiness_raw) != capture["readiness"]["response_bytes"]:
        fail("Readiness response byte count does not match raw JSON")
    readiness = parse_json_bytes(readiness_raw, "Readiness response")
    if (
        capture["readiness"]["http_status"] != 200
        or capture["readiness"]["content_type"] != "application/json"
        or readiness.get("status") != "ready"
        or readiness.get("reason") != "candidate-assembly-verified"
        or readiness.get("production_registration") is not False
        or sorted(readiness.get("active_tools", [])) != sorted(EXACT_OPERATIONS)
        or sorted(readiness.get("active_api_operations", [])) != sorted(EXACT_OPERATIONS)
    ):
        fail("Readiness direct-operation projection differs from MCP")

    tool_checks: list[dict[str, Any]] = []
    structured_by_operation: dict[str, dict[str, Any]] = {}
    search_receipt: str | None = None
    for index, operation in enumerate(EXACT_OPERATIONS, 6):
        params = requests[index]["params"]
        if params.get("name") != operation or not isinstance(params.get("arguments"), dict):
            fail(f"{operation} call request does not match its operation")
        structured, receipt = validate_tool_result(
            operation,
            result_of(responses[index], requests[index]["id"], f"{operation} response"),
            output_schemas[operation],
            expected_catalogue,
            search_receipt,
        )
        if operation == "catalogue.search":
            search_receipt = receipt
        structured_by_operation[operation] = structured
        tool_checks.append(
            {
                "operation": operation,
                "output_contract_valid": True,
                "structured_plain_text_parity": True,
                "direct_api_operation_parity": OPERATION_PATHS[operation] in paths,
                "deterministic_result_valid": True,
                "receipt_present": True,
            }
        )

    evidence_uri = f"gis-ai-go://evidence/receipts/{quote(str(search_receipt), safe='')}"
    resource_expectations = (
        (4, "catalogue.public", "gis-ai-go://catalogue/public", expected_catalogue["bundle"]),
        (
            5,
            "catalogue.record",
            "gis-ai-go://catalogue/records/LR-Q003",
            expected_catalogue["record"],
        ),
        (11, "evidence.receipt", evidence_uri, structured_by_operation["evidence.inspect"]),
    )
    resource_checks = []
    for index, resource, uri, expected in resource_expectations:
        if requests[index]["params"].get("uri") != uri:
            fail(f"{resource} request URI changed")
        response_result = result_of(responses[index], requests[index]["id"], f"{resource} response")
        contents = response_result.get("contents")
        if not isinstance(contents, list) or len(contents) != 1:
            fail(f"{resource} did not return one content item")
        item = contents[0]
        if item.get("uri") != uri or item.get("mimeType") != "application/json":
            fail(f"{resource} returned the wrong reference")
        if parse_json_text(item.get("text", ""), f"{resource} content") != expected:
            fail(f"{resource} content did not replay against canonical material")
        resource_checks.append(
            {
                "resource": resource,
                "content_contract_valid": True,
                "deterministic_result_valid": True,
            }
        )

    cancel_args = requests[12]["params"].get("arguments")
    first_args = requests[9]["params"].get("arguments")
    if (
        requests[12]["params"].get("name") != "data.query"
        or not isinstance(cancel_args, dict)
        or not isinstance(first_args, dict)
        or cancel_args.get("idempotency_key") == first_args.get("idempotency_key")
        or responses[12] is not None
    ):
        fail("The second data.query is not one distinct client-aborted request")
    unsupported = exact_keys(responses[13], {"jsonrpc", "id", "error"}, "Unsupported response")
    if unsupported["id"] != requests[13]["id"] or unsupported["error"] != {
        "code": -32601,
        "message": "Method not found",
    }:
        fail("prompts/list did not return exact method-not-found")
    successful_data_receipt = structured_by_operation["data.query"].get(
        "evidence_receipt", {}
    ).get("receipt_id")
    if not isinstance(successful_data_receipt, str):
        fail("The successful data query has no receipt for cancellation attribution")
    validate_audit(
        capture,
        first_args,
        cancel_args,
        successful_data_receipt,
    )

    request_checks = []
    for index, captured in enumerate(capture["requests"]):
        request_checks.append(
            {
                "ordinal": index + 1,
                "method": EXACT_METHODS[index],
                "subject": EXACT_SUBJECTS[index],
                "semantic": EXACT_SEMANTICS[index],
                "request_bytes": captured["request_bytes"],
                "request_sha256": sha256(captured["request_json"].encode()),
                "response_bytes": captured["response_bytes"],
                "response_sha256": (
                    None
                    if captured["response_json"] is None
                    else sha256(captured["response_json"].encode())
                ),
                "contract_valid": True,
            }
        )
    return {
        "requests": request_checks,
        "tool_checks": tool_checks,
        "resource_checks": resource_checks,
        "cancellation": {
            "mechanism": "http-request-abort-signal",
            "provider_started": True,
            "provider_aborted": True,
            "response_observed": False,
            "successful_request_completed_evidence_created": True,
            "completed_evidence_created": False,
            "private_idempotency_attribution_replayed": True,
        },
        "unsupported_method": {
            "method": "prompts/list",
            "error_code": -32601,
            "error_message": "Method not found",
            "contract_valid": True,
        },
    }


def source_materials() -> list[dict[str, str]]:
    materials = []
    root = ROOT.resolve(strict=True)
    for relative in SOURCE_MATERIAL_PATHS:
        lexical_path = root / relative
        path = lexical_path.resolve(strict=True)
        try:
            path.relative_to(root)
        except ValueError as error:
            raise VerificationError("Source material escaped the repository root") from error
        if path != lexical_path:
            fail(f"Source material {relative} must not traverse a symbolic link")
        raw = bounded_regular_file(path, MAX_MATERIAL_BYTES, f"Source material {relative}")
        materials.append({"path": relative, "sha256": sha256(raw)})
    return materials


def validate_captured_source_materials(
    captured: Any,
    current: list[dict[str, str]],
) -> list[dict[str, str]]:
    if not isinstance(captured, list) or len(captured) != len(SOURCE_MATERIAL_PATHS):
        fail("Private capture does not bind the exact source-material set")
    if len(current) != len(SOURCE_MATERIAL_PATHS):
        fail("Current source-material set is not exact")
    projected: list[dict[str, str]] = []
    for index, relative in enumerate(SOURCE_MATERIAL_PATHS):
        binding = exact_keys(
            captured[index],
            {"path", "sha256_before_execution", "sha256_after_execution"},
            f"Private source material {index + 1}",
        )
        observed_before = binding["sha256_before_execution"]
        observed_after = binding["sha256_after_execution"]
        if binding["path"] != relative:
            fail("Private capture source-material order changed")
        if observed_before != observed_after:
            fail(f"Source material {relative} changed during observed execution")
        if current[index] != {"path": relative, "sha256": observed_before}:
            fail(f"Source material {relative} changed between execution and replay")
        projected.append({"path": relative, "sha256": observed_before})
    return projected


def validate_path_free(value: Any, trail: tuple[str, ...] = ()) -> None:
    if isinstance(value, dict):
        for key, member in value.items():
            if key in FORBIDDEN_PUBLIC_MEMBERS:
                location = "/".join((*trail, key))
                fail(f"Public projection contains forbidden location member {location}")
            validate_path_free(member, (*trail, key))
        return
    if isinstance(value, list):
        for index, member in enumerate(value):
            validate_path_free(member, (*trail, str(index)))
        return
    if not isinstance(value, str):
        return
    lowered = value.lower()
    if (
        value.startswith(("/", "~/", "file:"))
        or ABSOLUTE_WINDOWS_PATH.match(value)
        or "127.0.0.1" in value
        or "localhost" in lowered
        or "/private/tmp/" in value
        or "/var/folders/" in value
        or "\\users\\" in lowered
    ):
        fail(f"Public projection is not path-free at {'/'.join(trail)}")


def build_projection(
    capture: dict[str, Any],
    capture_raw: bytes,
    *,
    verify_current_source: bool = True,
) -> dict[str, Any]:
    if capture.get("schema") != PRIVATE_SCHEMA_ID:
        fail("Private capture schema identity changed")
    if capture["source"]["working_tree_clean"] is not True:
        fail("A passing durable projection requires a clean capture source")
    if verify_current_source:
        verify_clean_current_source(capture["source"])
    current_materials_before = source_materials()
    if verify_current_source:
        verify_named_materials_match_tree(capture["source"], current_materials_before)
    projected_materials = validate_captured_source_materials(
        capture["source_materials"], current_materials_before
    )
    journey = replay_capture(capture)
    public_schema_raw, public_validator = schema_validator(PUBLIC_SCHEMA_PATH, "Public schema")
    projection: dict[str, Any] = {
        "schema": PUBLIC_SCHEMA_ID,
        "schema_contract": {
            "path": str(PUBLIC_SCHEMA_RELATIVE),
            "sha256": sha256(public_schema_raw),
        },
        "evidence_classification": "local-http-transport-preflight",
        "status": "loopback-http-transport-pass-capability-unscored",
        "observed_at": capture["observed_at"],
        "source": {
            "repository": capture["source"]["repository"],
            "commit": capture["source"]["commit"],
            "tree": capture["source"]["tree"],
            "checkout_scope": "local-worktree",
            "working_tree_clean": True,
            "complete_runtime_source_binding": False,
        },
        "runtime": {
            "node_version": capture["runtime"]["node_version"],
            "mcp_server_version": capture["runtime"]["mcp_server_version"],
            "fixture_process": "direct-child",
        },
        "transport": {
            "kind": "operating-system-loopback-http",
            "protocol": "http",
            "protocol_version": "2026-07-28",
            "address_class": "ipv4-loopback",
            "ephemeral_port": True,
            "listener_created": True,
            "listener_closed": True,
            "tls_exercised": False,
            "endpoint_published": False,
            "request_count": 14,
            "response_count": 13,
            "remote_host_acceptance": False,
        },
        "candidate": {
            "state": "candidate-unregistered",
            "production_registration": False,
            "operations": list(EXACT_OPERATIONS),
            "resources": list(EXACT_RESOURCES),
        },
        "journey": journey,
        "validation": {
            "canonical_tool_schema_validator": (
                "scripts/qual_206_exact_five_event_collector.mjs"
                "#advertisedToolSchemasExact"
            ),
            "protocol_discovery_exact": True,
            "operation_set_exact": True,
            "tool_schemas_exact": True,
            "resource_set_exact": True,
            "resource_template_set_exact": True,
            "openapi_callable_contract_exact": True,
            "readiness_operation_parity": True,
            "all_tool_results_contract_valid": True,
            "all_tool_results_structured_plain_text_parity": True,
            "all_tools_direct_api_operation_parity": True,
            "all_resource_results_contract_valid": True,
            "guarded_provider_egress_invocations": 0,
            "unexpected_audit_events": 0,
            "stdout_bytes": 0,
            "stderr_bytes": 0,
        },
        "execution": {
            "tool_calls": 6,
            "resource_reads": 3,
            "provider_transport_calls": 2,
            "aborted_provider_calls": 1,
            "ledger_events": 4,
            "reported_errors": 0,
        },
        "claims": {
            "transport_preflight": True,
            "claude_code_capability": "unscored",
            "model_capability": "unscored",
            "live_provider_readiness": "not-exercised",
            "remote_host_acceptance": False,
            "registration_performed": False,
            "activation_performed": False,
            "deployment_performed": False,
            "release_performed": False,
        },
        "verification": {
            "offline_verifier_path": "scripts/qual_206_verify_local_http_preflight.py",
            "source_materials": projected_materials,
            "private_capture_schema_path": str(PRIVATE_SCHEMA_RELATIVE),
            "private_capture_sha256": sha256(capture_raw),
            "private_capture_replayed": True,
            "private_capture_published": False,
            "observation_sha256": None,
            "schema_verified": True,
            "public_projection_path_free": True,
        },
        "limitations": [
            "The listener accepted requests only on the local IPv4 loopback interface.",
            "No TLS, secure tunnel, public hostname or independent remote host was exercised.",
            (
                "The client was a deterministic synthetic harness; no model client or "
                "Claude Code task was exercised."
            ),
            (
                "Only the deterministic fixture provider was used; no live provider, "
                "external network or provider credential was exercised."
            ),
            (
                "This preflight does not authorise or prove registration, activation, "
                "deployment or release."
            ),
        ],
        "boundary": (
            "Local operating-system loopback HTTP transport preflight only. A deterministic "
            "synthetic client completed the exact-five MCP 2026-07-28 discovery, listing, "
            "resource, tool, cancellation and unsupported-method journey over one ephemeral "
            "local socket. Remote-host acceptance is false; Claude Code and model capability "
            "remain unscored; no live provider was exercised; and no registration, activation, "
            "deployment or release was performed."
        ),
    }
    projection["verification"]["observation_sha256"] = observation_sha256(projection)
    validate_path_free(projection)
    validate_with_schema(projection, public_validator, "Public projection")
    if len((json.dumps(projection, indent=2) + "\n").encode()) > MAX_PUBLIC_BYTES:
        fail("Derived public projection exceeds its byte bound")
    current_materials_after = source_materials()
    if current_materials_after != current_materials_before:
        fail("Source material changed during private-capture replay")
    if verify_current_source:
        verify_clean_current_source(capture["source"])
        verify_named_materials_match_tree(capture["source"], current_materials_after)
    return projection


def write_new_public_projection(path: Path, projection: dict[str, Any]) -> None:
    if not path.is_absolute() or path != path.resolve():
        fail("Public output must be one canonical absolute new file")
    if path.parent.resolve(strict=True) != path.parent:
        fail("Public output parent must not traverse a symbolic link")
    raw = (json.dumps(projection, indent=2, ensure_ascii=False) + "\n").encode()
    if len(raw) < 1 or len(raw) > MAX_PUBLIC_BYTES:
        fail("Public output is outside its byte bound")
    expected_sha256 = sha256(raw)
    directory_flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        directory_flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        directory_flags |= os.O_NOFOLLOW
    try:
        parent_descriptor = os.open(path.parent, directory_flags)
    except OSError as error:
        raise VerificationError("Public output parent could not be opened") from error
    flags = os.O_RDWR | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    temporary_name = f".qual-206-public-{secrets.token_hex(16)}.tmp"
    descriptor: int | None = None
    opened: os.stat_result | None = None
    temporary_created = False
    final_created = False
    try:
        parent_before = os.fstat(parent_descriptor)
        named_parent = path.parent.stat(follow_symlinks=False)
        if (
            not stat.S_ISDIR(parent_before.st_mode)
            or parent_before.st_dev != named_parent.st_dev
            or parent_before.st_ino != named_parent.st_ino
            or parent_before.st_mode != named_parent.st_mode
            or parent_before.st_uid != named_parent.st_uid
            or parent_before.st_nlink != named_parent.st_nlink
        ):
            fail("Public output parent identity changed")
        try:
            os.stat(path.name, dir_fd=parent_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            fail("Public output must be a new file")
        descriptor = os.open(
            temporary_name,
            flags,
            0o600,
            dir_fd=parent_descriptor,
        )
        temporary_created = True
        os.fchmod(descriptor, 0o644)
        opened = os.fstat(descriptor)
        named_temporary = os.stat(
            temporary_name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        if (
            not stat.S_ISREG(opened.st_mode)
            or opened.st_dev != named_temporary.st_dev
            or opened.st_ino != named_temporary.st_ino
            or opened.st_mode != named_temporary.st_mode
            or opened.st_uid != os.getuid()
            or opened.st_uid != named_temporary.st_uid
            or opened.st_nlink != 1
            or named_temporary.st_nlink != 1
            or opened.st_size != 0
            or named_temporary.st_size != 0
        ):
            fail("Public output temporary descriptor and path do not agree")
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written < 1 or written > len(raw) - offset:
                fail("Public output write did not make bounded progress")
            offset += written
        os.fsync(descriptor)
        written_state = os.fstat(descriptor)
        named_written_state = os.stat(
            temporary_name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        if (
            written_state.st_dev != opened.st_dev
            or written_state.st_ino != opened.st_ino
            or written_state.st_mode != opened.st_mode
            or written_state.st_uid != opened.st_uid
            or written_state.st_nlink != 1
            or written_state.st_size != len(raw)
            or named_written_state.st_dev != written_state.st_dev
            or named_written_state.st_ino != written_state.st_ino
            or named_written_state.st_mode != written_state.st_mode
            or named_written_state.st_uid != written_state.st_uid
            or named_written_state.st_nlink != 1
            or named_written_state.st_size != len(raw)
        ):
            fail("Public output temporary identity or size changed while it was written")
        os.lseek(descriptor, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        read_count = 0
        while read_count <= len(raw):
            chunk = os.read(descriptor, min(65_536, len(raw) + 1 - read_count))
            if chunk == b"":
                break
            chunks.append(chunk)
            read_count += len(chunk)
        readback = b"".join(chunks)
        if readback != raw or sha256(readback) != expected_sha256:
            fail("Public output exact-byte and digest readback failed")
        if parse_json_bytes(readback, "Public output readback") != projection:
            fail("Public output parsed readback differs from the projection")

        parent_before_publication = os.fstat(parent_descriptor)
        absolute_parent_before_publication = path.parent.stat(follow_symlinks=False)
        if (
            parent_before_publication.st_dev != parent_before.st_dev
            or parent_before_publication.st_ino != parent_before.st_ino
            or parent_before_publication.st_mode != parent_before.st_mode
            or parent_before_publication.st_uid != parent_before.st_uid
            or absolute_parent_before_publication.st_dev
            != parent_before_publication.st_dev
            or absolute_parent_before_publication.st_ino
            != parent_before_publication.st_ino
            or absolute_parent_before_publication.st_mode
            != parent_before_publication.st_mode
            or absolute_parent_before_publication.st_uid
            != parent_before_publication.st_uid
            or absolute_parent_before_publication.st_nlink
            != parent_before_publication.st_nlink
        ):
            fail("Public output parent identity changed before publication")
        try:
            os.link(
                temporary_name,
                path.name,
                src_dir_fd=parent_descriptor,
                dst_dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except OSError as error:
            raise VerificationError("Public output must be a new file") from error
        final_created = True
        linked_state = os.stat(
            path.name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        if (
            linked_state.st_dev != written_state.st_dev
            or linked_state.st_ino != written_state.st_ino
            or linked_state.st_mode != written_state.st_mode
            or linked_state.st_uid != written_state.st_uid
            or linked_state.st_nlink != 2
            or linked_state.st_size != written_state.st_size
        ):
            fail("Public output hard-link publication identity changed")
        os.unlink(temporary_name, dir_fd=parent_descriptor)
        temporary_created = False
        os.fsync(parent_descriptor)

        final_state = os.fstat(descriptor)
        final_named_state = os.stat(
            path.name,
            dir_fd=parent_descriptor,
            follow_symlinks=False,
        )
        absolute_final_state = path.stat(follow_symlinks=False)
        parent_after = os.fstat(parent_descriptor)
        absolute_parent_after = path.parent.stat(follow_symlinks=False)
        if (
            final_state.st_dev != written_state.st_dev
            or final_state.st_ino != written_state.st_ino
            or final_state.st_mode != written_state.st_mode
            or final_state.st_uid != written_state.st_uid
            or final_state.st_nlink != 1
            or final_state.st_size != written_state.st_size
            or final_named_state.st_dev != final_state.st_dev
            or final_named_state.st_ino != final_state.st_ino
            or final_named_state.st_mode != final_state.st_mode
            or final_named_state.st_uid != final_state.st_uid
            or final_named_state.st_nlink != final_state.st_nlink
            or final_named_state.st_size != final_state.st_size
            or absolute_final_state.st_dev != final_state.st_dev
            or absolute_final_state.st_ino != final_state.st_ino
            or absolute_final_state.st_mode != final_state.st_mode
            or absolute_final_state.st_uid != final_state.st_uid
            or absolute_final_state.st_nlink != final_state.st_nlink
            or absolute_final_state.st_size != final_state.st_size
        ):
            fail("Public output identity changed after publication")
        if (
            parent_after.st_dev != parent_before.st_dev
            or parent_after.st_ino != parent_before.st_ino
            or parent_after.st_mode != parent_before.st_mode
            or parent_after.st_uid != parent_before.st_uid
            or parent_after.st_nlink < 2
            or absolute_parent_after.st_dev != parent_after.st_dev
            or absolute_parent_after.st_ino != parent_after.st_ino
            or absolute_parent_after.st_mode != parent_after.st_mode
            or absolute_parent_after.st_uid != parent_after.st_uid
            or absolute_parent_after.st_nlink != parent_after.st_nlink
        ):
            fail("Public output parent identity changed after publication")
    except OSError as error:
        raise VerificationError("Public output finalisation failed") from error
    finally:
        if final_created and opened is not None:
            try:
                current_final = os.stat(
                    path.name,
                    dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
                if (
                    sys.exc_info()[0] is not None
                    and current_final.st_dev == opened.st_dev
                    and current_final.st_ino == opened.st_ino
                ):
                    os.unlink(path.name, dir_fd=parent_descriptor)
                    final_created = False
            except OSError:
                pass
        if temporary_created:
            try:
                os.unlink(temporary_name, dir_fd=parent_descriptor)
            except OSError:
                pass
        if sys.exc_info()[0] is not None:
            try:
                os.fsync(parent_descriptor)
            except OSError:
                pass
        if descriptor is not None:
            os.close(descriptor)
        os.close(parent_descriptor)


def verify_and_project(
    capture_path: Path,
    *,
    verify_current_source: bool = True,
) -> tuple[dict[str, Any], bytes]:
    capture_path = exact_private_capture_path(capture_path)
    capture_raw = bounded_regular_file(
        capture_path, MAX_CAPTURE_BYTES, "Private capture", owner_only=True
    )
    exact_private_capture_path(capture_path)
    capture = parse_json_bytes(capture_raw, "Private capture")
    _schema_raw, private_validator = schema_validator(PRIVATE_SCHEMA_PATH, "Private schema")
    validate_with_schema(capture, private_validator, "Private capture")
    return (
        build_projection(capture, capture_raw, verify_current_source=verify_current_source),
        capture_raw,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Independently replay one owner-only QUAL-206 local HTTP raw/audit capture "
            "and write a path-free public projection without network, provider or model calls."
        )
    )
    parser.add_argument("--capture", required=True, type=Path)
    parser.add_argument("--public-output", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        projection, _raw = verify_and_project(arguments.capture)
        write_new_public_projection(arguments.public_output, projection)
    except (VerificationError, OSError) as error:
        print(f"QUAL-206 local HTTP preflight verification failed: {error}", file=sys.stderr)
        return 1
    except Exception:
        print(
            "QUAL-206 local HTTP preflight verification failed: "
            "unexpected bounded replay failure",
            file=sys.stderr,
        )
        return 1
    print(
        "QUAL-206 local HTTP transport preflight replayed and projected; "
        "remote host acceptance remains false."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
