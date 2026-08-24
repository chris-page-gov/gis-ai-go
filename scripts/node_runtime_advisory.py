#!/usr/bin/env python3
"""Calibrated, offline-replayable advisory coverage for the standalone Node runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import ssl
import stat
import subprocess
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import parse_qs, unquote, urlsplit
from urllib.request import (
    HTTPRedirectHandler,
    HTTPSHandler,
    ProxyHandler,
    Request,
    build_opener,
)

from gateway_image import (
    NODE_BINARY_SHA256,
    NODE_RUNTIME_CPE,
    NODE_RUNTIME_PURL,
    NODE_SECURITY_ADVISORY_URL,
    NODE_UPSTREAM_ARCHIVE_SHA256,
    NODE_UPSTREAM_ARCHIVE_URL,
    ROOT,
    assert_no_private_json,
    assert_no_private_text,
    canonical_json_bytes,
    parse_bounded_json_object,
    parse_checksum,
    prohibited_text_reason,
    read_bounded_regular_file,
    sha256_file,
)

GRYPE_VERSION = "0.117.0"
GRYPE_REFERENCE = (
    "anchore/grype:v0.117.0@"
    "sha256:ab8d929faec38875a45aba74c9651549cd096756d1981773c04375f282e91075"
)
GRYPE_PLATFORM = "linux/amd64"
GRYPE_DB_ARCHIVE_NAME = "gateway-node.grype-db.tar.zst"
GRYPE_DB_CHECKSUM_NAME = f"{GRYPE_DB_ARCHIVE_NAME}.sha256"
GRYPE_INPUT_PATH = "/input/node-runtime.sbom.cdx.json"
GRYPE_DB_INPUT_PATH = f"/input/{GRYPE_DB_ARCHIVE_NAME}"
DATABASE_REQUEST_HEADERS = {
    "Accept": "application/zstd",
    "User-Agent": "gis-ai-go/0.1 vulnerability-evidence",
}
MAX_GRYPE_DB_ARCHIVE_BYTES = 256 * 1024 * 1024
MAX_GRYPE_DB_EXPANDED_BYTES = 3 * 1024 * 1024 * 1024
MAX_GRYPE_REPORT_BYTES = 32 * 1024 * 1024
MAX_GRYPE_DIAGNOSTIC_BYTES = 4 * 1024
GRYPE_TIMEOUT_SECONDS = 20 * 60
MAX_DATABASE_AGE_AT_SCAN = timedelta(days=3)
# The protected producer and provenance jobs have 50- and 30-minute timeouts.
# Two hours leaves transfer/setup headroom without treating retained history as same-run.
MAX_PROTECTED_PROVENANCE_ASSESSMENT_AGE = timedelta(hours=2)
MAX_PROTECTED_PROVENANCE_FUTURE_SKEW = timedelta(minutes=5)
NODE_CALIBRATION_AFFECTED_VERSION = "24.18.0"
NODE_CALIBRATION_FIXED_VERSION = "24.18.1"
NODE_CALIBRATION_HIGH_IDS = frozenset(
    {"CVE-2026-56846", "CVE-2026-56848", "CVE-2026-58043"}
)
NODE_ROLES: dict[str, tuple[str, str | None]] = {
    "actual": ("24.19.0", None),
    "affected": (NODE_CALIBRATION_AFFECTED_VERSION, "affected"),
    "fixed": (NODE_CALIBRATION_FIXED_VERSION, "fixed"),
}
NODE_ROLE_FILES: dict[str, dict[str, str]] = {
    role: {
        "input": f"gateway-node.{role}.input.cdx.json",
        "json_report": f"gateway-node.{role}.grype.json",
        "cyclonedx_report": f"gateway-node.{role}.grype.cdx.json",
    }
    for role in NODE_ROLES
}
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_GRYPE_SCHEMA = re.compile(r"v6\.[0-9]+\.[0-9]+\Z")
_XXH64 = re.compile(r"xxh64:[0-9a-f]{16}\Z")
_CVE = re.compile(r"CVE-[0-9]{4}-[0-9]{4,}\Z")


class _RejectRedirect(HTTPRedirectHandler):
    def redirect_request(
        self,
        req: Any,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        raise HTTPError(req.full_url, code, "Grype database redirect rejected", headers, fp)


def _bounded_text(value: Any, *, label: str, maximum: int) -> str:
    if not isinstance(value, str) or not value or len(value) > maximum:
        raise ValueError(f"Grype {label} is missing or outside its bound")
    return value


def _sanitise_diagnostic(value: object, *, label: str) -> str:
    if not isinstance(value, bytes):
        return f"{label}_status=unavailable"
    if len(value) > MAX_GRYPE_DIAGNOSTIC_BYTES:
        return f"{label}_status=withheld {label}_reason=over-bound"
    try:
        text = value.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return f"{label}_status=withheld {label}_reason=invalid-utf8"
    reason = prohibited_text_reason(text)
    if reason is not None:
        return f"{label}_status=withheld {label}_reason={reason}"
    return f"{label}_status=readable {label}_text={json.dumps(' '.join(text.split()))}"


def _run_grype(
    arguments: list[str],
    *,
    cache: Path,
    network: bool,
    input_file: Path | None = None,
    database_archive: Path | None = None,
) -> bytes:
    cache_metadata = cache.lstat()
    if stat.S_ISLNK(cache_metadata.st_mode) or not stat.S_ISDIR(cache_metadata.st_mode):
        raise ValueError("Grype cache must be one real directory")
    uid = os.getuid()
    gid = os.getgid()
    command = [
        "docker",
        "run",
        "--rm",
        "--pull=never",
        "--platform=linux/amd64",
        "--read-only",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        f"--user={uid}:{gid}",
        (
            "--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=512m,mode=0700,"
            f"uid={uid},gid={gid}"
        ),
        f"--volume={cache.resolve(strict=True)}:/cache",
        "--env=GRYPE_DB_CACHE_DIR=/cache",
        "--env=GRYPE_DB_AUTO_UPDATE=false",
        "--env=GRYPE_DB_VALIDATE_BY_HASH_ON_START=true",
        "--env=GRYPE_DB_VALIDATE_AGE=false",
        "--env=GRYPE_DB_REQUIRE_UPDATE_CHECK=false",
        "--env=GRYPE_CHECK_FOR_APP_UPDATE=false",
        "--env=GRYPE_MATCH_STOCK_USING_CPES=true",
        "--env=GRYPE_ADD_CPES_IF_NONE=false",
    ]
    if not network:
        command.append("--network=none")
    if input_file is not None:
        metadata = input_file.lstat()
        if (
            stat.S_ISLNK(metadata.st_mode)
            or not stat.S_ISREG(metadata.st_mode)
            or metadata.st_size < 1
            or metadata.st_size > MAX_GRYPE_REPORT_BYTES
        ):
            raise ValueError("Grype Node input is invalid or outside its bound")
        command.append(f"--volume={input_file.resolve(strict=True)}:{GRYPE_INPUT_PATH}:ro")
    if database_archive is not None:
        metadata = database_archive.lstat()
        if (
            stat.S_ISLNK(metadata.st_mode)
            or not stat.S_ISREG(metadata.st_mode)
            or metadata.st_size < 1
            or metadata.st_size > MAX_GRYPE_DB_ARCHIVE_BYTES
        ):
            raise ValueError("Grype database archive is invalid or outside its bound")
        command.append(
            f"--volume={database_archive.resolve(strict=True)}:{GRYPE_DB_INPUT_PATH}:ro"
        )
    command.extend([GRYPE_REFERENCE, *arguments])
    try:
        result = subprocess.run(
            tuple(command),
            cwd=ROOT,
            check=True,
            capture_output=True,
            timeout=GRYPE_TIMEOUT_SECONDS,
        )
    except subprocess.CalledProcessError as error:
        stdout = _sanitise_diagnostic(error.stdout, label="stdout")
        stderr = _sanitise_diagnostic(error.stderr, label="stderr")
        raise ValueError(
            f"pinned Grype command failed with exit code {error.returncode}; "
            f"{stdout}; {stderr}"
        ) from None
    except subprocess.TimeoutExpired as error:
        stdout = _sanitise_diagnostic(error.stdout, label="stdout")
        stderr = _sanitise_diagnostic(error.stderr, label="stderr")
        raise ValueError(
            f"pinned Grype command timed out after {GRYPE_TIMEOUT_SECONDS} seconds; "
            f"{stdout}; {stderr}"
        ) from None
    except OSError:
        raise ValueError("pinned Grype command could not be started") from None
    if len(result.stdout) > MAX_GRYPE_REPORT_BYTES:
        raise ValueError("Grype output exceeds its evidence bound")
    return result.stdout


def acquire_grype_image() -> None:
    subprocess.run(
        ("docker", "pull", "--platform=linux/amd64", GRYPE_REFERENCE),
        cwd=ROOT,
        check=True,
        timeout=GRYPE_TIMEOUT_SECONDS,
    )


def _parse_json(raw: bytes, *, label: str) -> dict[str, Any]:
    if len(raw) > MAX_GRYPE_REPORT_BYTES:
        raise ValueError(f"{label} exceeds its byte bound")
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{label} is not valid JSON") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be one JSON object")
    return value


def _normalise_database_status(
    value: Any, *, expected_source: dict[str, Any] | None = None
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Grype database status is missing")
    schema_version = _bounded_text(
        value.get("schemaVersion"), label="database schema", maximum=64
    )
    source = _bounded_text(value.get("from"), label="database source", maximum=2_048)
    built = _bounded_text(value.get("built"), label="database build time", maximum=32)
    if _GRYPE_SCHEMA.fullmatch(schema_version) is None or value.get("valid") is not True:
        raise ValueError("Grype database is not valid schema v6 evidence")
    if not built.endswith("Z"):
        raise ValueError("Grype database build time is not UTC")
    try:
        parsed = datetime.fromisoformat(built[:-1] + "+00:00")
    except ValueError as error:
        raise ValueError("Grype database build time is invalid") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise ValueError("Grype database build time is not UTC")
    status = {
        "schema_version": schema_version,
        "built": parsed.astimezone(UTC).isoformat(timespec="seconds").replace(
            "+00:00", "Z"
        ),
        "valid": True,
    }
    if source == "manual import":
        expected = _database_source_binding(expected_source)
        if any(status[key] != expected[key] for key in status):
            raise ValueError("manual Grype import differs from its acquired database")
        return {**expected, "load_mode": "manual-import"}
    if expected_source is not None:
        raise ValueError("offline Grype status did not report a manual import")
    return {
        **status,
        "source_url": source,
        "source_sha256": _database_source_sha256(source),
    }


def _database_source_sha256(source: str) -> str:
    parsed = urlsplit(source)
    query = parse_qs(parsed.query, keep_blank_values=True, strict_parsing=True)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "grype.anchore.io"
        or parsed.port is not None
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
        or not parsed.path.startswith("/databases/v6/vulnerability-db_v6.")
        or not parsed.path.endswith(".tar.zst")
        or set(query) != {"checksum"}
        or len(query["checksum"]) != 1
    ):
        raise ValueError("Grype database source URL is outside the closed origin and path")
    checksum = unquote(query["checksum"][0])
    if not checksum.startswith("sha256:") or _SHA256.fullmatch(checksum[7:]) is None:
        raise ValueError("Grype database source URL lacks an exact SHA-256 checksum")
    return checksum[7:]


def _database_source_binding(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Grype database source binding is missing")
    return _normalise_database_status(
        {
            "schemaVersion": value.get("schema_version"),
            "from": value.get("source_url"),
            "built": value.get("built"),
            "valid": value.get("valid"),
        }
    )


def read_database_status(
    cache: Path, *, expected_source: dict[str, Any] | None = None
) -> dict[str, Any]:
    raw = _run_grype(["db", "status", "-o", "json"], cache=cache, network=False)
    return _normalise_database_status(
        _parse_json(raw, label="Grype database status"),
        expected_source=expected_source,
    )


def update_database(cache: Path) -> dict[str, Any]:
    _run_grype(["db", "update"], cache=cache, network=True)
    return read_database_status(cache)


def download_database_archive(status: dict[str, Any], output: Path) -> None:
    source = status["source_url"]
    expected_sha256 = status["source_sha256"]
    if _database_source_sha256(source) != expected_sha256:
        raise ValueError("Grype database status checksum differs from its source URL")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    opener = build_opener(
        ProxyHandler({}),
        HTTPSHandler(context=ssl.create_default_context()),
        _RejectRedirect(),
    )
    digest = hashlib.sha256()
    total = 0
    try:
        request = Request(source, method="GET", headers=DATABASE_REQUEST_HEADERS)
        with opener.open(request, timeout=60) as response, temporary.open("xb") as sink:
            if response.status != 200 or response.geturl() != source:
                raise ValueError("Grype database response differs from the exact source")
            content_type = response.headers.get_content_type()
            declared = response.headers.get("Content-Length")
            if content_type != "application/zstd" or declared is None:
                raise ValueError("Grype database response lacks its closed media metadata")
            try:
                declared_bytes = int(declared)
            except ValueError as error:
                raise ValueError("Grype database response length is invalid") from error
            if declared_bytes < 1 or declared_bytes > MAX_GRYPE_DB_ARCHIVE_BYTES:
                raise ValueError("Grype database response exceeds its retained bound")
            while chunk := response.read(1024 * 1024):
                total += len(chunk)
                if total > MAX_GRYPE_DB_ARCHIVE_BYTES:
                    raise ValueError("Grype database response exceeds its retained bound")
                digest.update(chunk)
                sink.write(chunk)
        if total != declared_bytes or digest.hexdigest() != expected_sha256:
            raise ValueError("Grype database response differs from its advertised identity")
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)


def import_database(
    cache: Path, archive: Path, *, source: dict[str, Any]
) -> dict[str, Any]:
    _run_grype(
        ["db", "import", GRYPE_DB_INPUT_PATH],
        cache=cache,
        network=False,
        database_archive=archive,
    )
    return read_database_status(cache, expected_source=source)


def database_inventory(cache: Path) -> list[dict[str, Any]]:
    expected = {"6/import.json", "6/vulnerability.db"}
    result: list[dict[str, Any]] = []
    total = 0
    for relative in sorted(expected):
        path = cache / relative
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise ValueError("Grype imported database inventory is not regular")
        total += metadata.st_size
        if total > MAX_GRYPE_DB_EXPANDED_BYTES:
            raise ValueError("Grype imported database exceeds its expanded bound")
        result.append(
            {"path": relative, "sha256": sha256_file(path), "bytes": metadata.st_size}
        )
    unexpected = {
        item.relative_to(cache).as_posix()
        for item in cache.rglob("*")
        if item.is_file() or item.is_symlink()
    } - expected
    if unexpected:
        raise ValueError("Grype imported database inventory is not closed")
    return result


def extract_node_identity(sbom: dict[str, Any], receipt: dict[str, Any]) -> dict[str, str]:
    composition = receipt.get("build", {}).get("runtime_composition", {})
    node = composition.get("node_binary") if isinstance(composition, dict) else None
    rootfs = receipt.get("image", {}).get("rootfs", {})
    critical_entries = rootfs.get("critical_entries") if isinstance(rootfs, dict) else None
    if not isinstance(node, dict) or not isinstance(critical_entries, list):
        raise ValueError("gateway receipt lacks the standalone Node runtime identity")
    expected_node = {
        "name": "node",
        "version": "24.19.0",
        "purl": NODE_RUNTIME_PURL,
        "cpe": NODE_RUNTIME_CPE,
        "path": "/usr/local/bin/node",
        "file_sha256": NODE_BINARY_SHA256,
        "rootfs_inventory_sha256": rootfs.get("inventory_sha256"),
        "upstream_archive_url": NODE_UPSTREAM_ARCHIVE_URL,
        "upstream_archive_sha256": NODE_UPSTREAM_ARCHIVE_SHA256,
        "security_advisory_url": NODE_SECURITY_ADVISORY_URL,
    }
    receipt_identity = {
        "version": expected_node["version"],
        "path": expected_node["path"],
        "sha256": expected_node["file_sha256"],
        "purl": expected_node["purl"],
        "cpe": expected_node["cpe"],
        "upstream_archive_url": expected_node["upstream_archive_url"],
        "upstream_archive_sha256": expected_node["upstream_archive_sha256"],
        "security_advisory_url": expected_node["security_advisory_url"],
    }
    if any(node.get(key) != value for key, value in receipt_identity.items()):
        raise ValueError("gateway receipt Node runtime differs from its fixed identity")
    critical = [
        item
        for item in critical_entries
        if isinstance(item, dict) and item.get("path") == expected_node["path"]
    ]
    if len(critical) != 1 or critical[0].get("sha256") != NODE_BINARY_SHA256:
        raise ValueError("gateway rootfs does not bind the exact Node executable")

    components = sbom.get("components")
    if not isinstance(components, list):
        raise ValueError("gateway SBOM lacks its component inventory")
    applications = [
        item
        for item in components
        if isinstance(item, dict)
        and (
            item.get("purl") == NODE_RUNTIME_PURL
            or (
                item.get("type") == "application"
                and (
                    item.get("name") == "node"
                    or (
                        isinstance(item.get("purl"), str)
                        and item["purl"].startswith("pkg:generic/node@")
                    )
                    or (
                        isinstance(item.get("cpe"), str)
                        and item["cpe"].startswith("cpe:2.3:a:nodejs:node.js:")
                    )
                )
            )
        )
    ]
    files = [
        item
        for item in components
        if isinstance(item, dict)
        and item.get("type") == "file"
        and (
            item.get("name") == "node"
            or any(
                isinstance(prop, dict)
                and prop.get("name") == "gis-ai-go:runtime-file-path"
                and prop.get("value") == expected_node["path"]
                for prop in item.get("properties", [])
            )
        )
    ]
    if len(applications) != 1 or len(files) != 1:
        raise ValueError("gateway SBOM Node application and measured file are not unique")
    application = applications[0]
    app_properties = {
        item.get("name"): item.get("value")
        for item in application.get("properties", [])
        if isinstance(item, dict)
    }
    file_component = files[0]
    file_properties = {
        item.get("name"): item.get("value")
        for item in file_component.get("properties", [])
        if isinstance(item, dict)
    }
    file_hashes = {
        item.get("content")
        for item in file_component.get("hashes", [])
        if isinstance(item, dict) and item.get("alg") == "SHA-256"
    }
    if (
        application.get("type") != "application"
        or application.get("name") != "node"
        or application.get("version") != "24.19.0"
        or application.get("purl") != NODE_RUNTIME_PURL
        or application.get("cpe") != NODE_RUNTIME_CPE
        or app_properties.get("syft:location:0:path") != expected_node["path"]
        or file_component.get("version") != "24.19.0"
        or file_hashes != {NODE_BINARY_SHA256}
        or file_properties.get("gis-ai-go:runtime-file-path") != expected_node["path"]
        or file_properties.get("gis-ai-go:rootfs-inventory-sha256")
        != expected_node["rootfs_inventory_sha256"]
        or file_properties.get("gis-ai-go:upstream-archive")
        != NODE_UPSTREAM_ARCHIVE_URL
        or file_properties.get("gis-ai-go:upstream-archive-sha256")
        != NODE_UPSTREAM_ARCHIVE_SHA256
    ):
        raise ValueError("gateway SBOM Node identity is not bound to the measured runtime")
    return expected_node


def _node_purl(version: str) -> str:
    return f"pkg:generic/node@{version}"


def _node_cpe(version: str) -> str:
    return f"cpe:2.3:a:nodejs:node.js:{version}:*:*:*:*:*:*:*"


def make_node_input(
    identity: dict[str, str], *, version: str, calibration: str | None
) -> dict[str, Any]:
    component: dict[str, Any] = {
        "bom-ref": _node_purl(version),
        "type": "application",
        "name": "node",
        "version": version,
        "purl": _node_purl(version),
        "cpe": _node_cpe(version),
    }
    if calibration is None:
        component["hashes"] = [
            {"alg": "SHA-256", "content": identity["file_sha256"]}
        ]
        component["properties"] = [
            {"name": "gis-ai-go:runtime-file-path", "value": identity["path"]},
            {
                "name": "gis-ai-go:rootfs-inventory-sha256",
                "value": identity["rootfs_inventory_sha256"],
            },
            {
                "name": "gis-ai-go:upstream-archive",
                "value": identity["upstream_archive_url"],
            },
            {
                "name": "gis-ai-go:upstream-archive-sha256",
                "value": identity["upstream_archive_sha256"],
            },
        ]
    else:
        component["properties"] = [
            {"name": "gis-ai-go:synthetic-calibration", "value": calibration},
            {
                "name": "gis-ai-go:security-advisory",
                "value": NODE_SECURITY_ADVISORY_URL,
            },
        ]
    return {
        "$schema": "https://cyclonedx.org/schema/bom-1.6.schema.json",
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "metadata": {
            "component": {
                "bom-ref": "urn:gis-ai-go:node-runtime-advisory-input",
                "type": "application",
                "name": "gis-ai-go-node-runtime-advisory-input",
                "version": version,
            }
        },
        "components": [component],
    }


def _scan_raw(
    cache: Path, input_document: dict[str, Any], *, output_format: str
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="gis-ai-go-grype-input-") as temporary:
        input_path = Path(temporary) / "node-runtime.sbom.cdx.json"
        input_path.write_bytes(canonical_json_bytes(input_document))
        raw = _run_grype(
            [
                f"sbom:{GRYPE_INPUT_PATH}",
                "--output",
                output_format,
                "--show-suppressed",
            ],
            cache=cache,
            network=False,
            input_file=input_path,
        )
    return _parse_json(raw, label=f"Grype {output_format} report")


def _normalise_provider(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ValueError("Grype report lacks the NVD database provider")
    captured = _bounded_text(value.get("captured"), label="NVD capture", maximum=32)
    provider_input = _bounded_text(value.get("input"), label="NVD input", maximum=64)
    if not captured.endswith("Z"):
        raise ValueError("Grype NVD capture time is invalid")
    try:
        parsed = datetime.fromisoformat(captured[:-1] + "+00:00")
    except ValueError as error:
        raise ValueError("Grype NVD capture time is invalid") from error
    if parsed.utcoffset() != timedelta(0) or _XXH64.fullmatch(provider_input) is None:
        raise ValueError("Grype NVD provider identity is invalid")
    return {
        "name": "nvd",
        "captured": parsed.astimezone(UTC).isoformat(timespec="seconds").replace(
            "+00:00", "Z"
        ),
        "input": provider_input,
    }


def _validate_non_node_ignore_rules(value: Any) -> None:
    """Accept only Grype's pinned kernel-header defaults, none of which match Node."""
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError("Grype ignore rules differ from the pinned non-Node defaults")
    expected_packages = {
        ("rpm", "kernel-headers", "kernel"),
        ("deb", "linux(-.*)?-headers-.*", "linux.*"),
        ("deb", "linux-libc-dev", "linux"),
        ("deb", "linux-kbuild-.*", "linux.*"),
    }
    actual_packages: set[tuple[str, str, str]] = set()
    for rule in value:
        if not isinstance(rule, dict):
            raise ValueError("Grype ignore rule is not an object")
        package = rule.get("package")
        if (
            not isinstance(package, dict)
            or rule.get("vulnerability") != ""
            or rule.get("include-aliases") is not False
            or rule.get("reason") != ""
            or rule.get("namespace") != ""
            or rule.get("fix-state") != ""
            or rule.get("vex-status") != ""
            or rule.get("vex-justification") != ""
            or rule.get("match-type") != "exact-indirect-match"
            or package.get("version") != ""
            or package.get("language") != ""
            or package.get("location") != ""
        ):
            raise ValueError("Grype ignore rule could conceal a Node advisory match")
        actual_packages.add(
            (package.get("type"), package.get("name"), package.get("upstream-name"))
        )
    if actual_packages != expected_packages:
        raise ValueError("Grype ignore rules differ from the pinned non-Node defaults")


def normalise_json_report(
    report: dict[str, Any],
    input_document: dict[str, Any],
    *,
    database_source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    descriptor = report.get("descriptor")
    if not isinstance(descriptor, dict):
        raise ValueError("Grype JSON report lacks its descriptor")
    configuration = descriptor.get("configuration")
    db = descriptor.get("db")
    if (
        descriptor.get("name") != "grype"
        or descriptor.get("version") != GRYPE_VERSION
        or not isinstance(configuration, dict)
        or not isinstance(db, dict)
    ):
        raise ValueError("Grype JSON report lacks the pinned scanner identity")
    stock = configuration.get("match", {}).get("stock")
    db_configuration = configuration.get("db")
    external_sources = configuration.get("externalSources")
    if (
        stock != {"using-cpes": True}
        or not isinstance(db_configuration, dict)
        or db_configuration.get("auto-update") is not False
        or db_configuration.get("validate-by-hash-on-start") is not True
        or db_configuration.get("validate-age") is not False
        or db_configuration.get("require-update-check") is not False
        or configuration.get("check-for-app-update") is not False
        or configuration.get("add-cpes-if-none") is not False
        or configuration.get("show-suppressed") is not True
        or configuration.get("vex-documents") != []
        or configuration.get("ignore-wontfix") != ""
        or configuration.get("only-fixed") is not False
        or configuration.get("only-notfixed") is not False
        or configuration.get("exclude") != []
        or not isinstance(external_sources, dict)
        or external_sources.get("enable") is not False
    ):
        raise ValueError("Grype JSON report does not prove the closed offline CPE mode")
    _validate_non_node_ignore_rules(configuration.get("ignore"))
    status = _normalise_database_status(
        db.get("status"), expected_source=database_source
    )
    providers = db.get("providers")
    if not isinstance(providers, dict):
        raise ValueError("Grype JSON report lacks its database providers")
    nvd = _normalise_provider(providers.get("nvd"))
    component = input_document["components"][0]
    matches = report.get("matches")
    ignored_matches = report.get("ignoredMatches", [])
    if (
        not isinstance(matches, list)
        or len(matches) > 10_000
        or ignored_matches not in (None, [])
    ):
        raise ValueError("Grype JSON report match inventory is invalid")
    source = report.get("source")
    if source != {"type": "sbom-file", "target": GRYPE_INPUT_PATH}:
        raise ValueError("Grype JSON report is not bound to the closed Node input role")
    projected: list[dict[str, Any]] = []
    for match in matches:
        if not isinstance(match, dict):
            raise ValueError("Grype JSON report contains an invalid match")
        artifact = match.get("artifact")
        vulnerability = match.get("vulnerability")
        details = match.get("matchDetails")
        if (
            not isinstance(artifact, dict)
            or not isinstance(vulnerability, dict)
            or not isinstance(details, list)
            or not details
        ):
            raise ValueError("Grype JSON report match is incomplete")
        cpes = artifact.get("cpes")
        if (
            artifact.get("name") != "node"
            or artifact.get("version") != component["version"]
            or artifact.get("type") != "UnknownPackage"
            or artifact.get("purl") != component["purl"]
            or not isinstance(cpes, list)
            or component["cpe"] not in cpes
        ):
            raise ValueError("Grype report matched a component outside the exact Node input")
        identifier = _bounded_text(
            vulnerability.get("id"), label="vulnerability ID", maximum=64
        )
        severity = _bounded_text(
            vulnerability.get("severity"), label="vulnerability severity", maximum=16
        ).upper()
        namespace = _bounded_text(
            vulnerability.get("namespace"), label="vulnerability namespace", maximum=128
        )
        fix = vulnerability.get("fix")
        if (
            _CVE.fullmatch(identifier) is None
            or severity not in {"NEGLIGIBLE", "LOW", "MEDIUM", "HIGH", "CRITICAL"}
            or namespace != "nvd:cpe"
            or not isinstance(fix, dict)
            or fix.get("state") not in {"fixed", "not-fixed", "unknown", "wont-fix"}
            or not isinstance(fix.get("versions"), list)
            or any(
                not isinstance(item, str) or not item or len(item) > 512
                for item in fix["versions"]
            )
        ):
            raise ValueError("Grype Node advisory match is outside the closed contract")
        if len(details) != 1 or not isinstance(details[0], dict):
            raise ValueError("Grype Node advisory match is not one stock CPE assessment")
        detail = details[0]
        searched = detail.get("searchedBy")
        found = detail.get("found")
        if (
            detail.get("type") != "cpe-match"
            or detail.get("matcher") != "stock-matcher"
            or not isinstance(searched, dict)
            or searched.get("namespace") != "nvd:cpe"
            or searched.get("cpes") != [component["cpe"]]
            or searched.get("package")
            != {"name": "node", "version": component["version"]}
            or not isinstance(found, dict)
            or found.get("vulnerabilityID") != identifier
            or not isinstance(found.get("cpes"), list)
            or not found["cpes"]
            or any(
                not isinstance(item, str)
                or not item.startswith("cpe:2.3:a:nodejs:node.js:")
                for item in found["cpes"]
            )
            or len(set(found["cpes"])) != len(found["cpes"])
        ):
            raise ValueError("Grype Node advisory match did not use the exact stock CPE")
        projected.append(
            {
                "id": identifier,
                "severity": severity,
                "namespace": namespace,
                "installed_version": component["version"],
                "fixed_versions": sorted(set(fix["versions"])),
                "fix_state": fix["state"],
                "matcher": "stock-matcher",
                "match_types": ["cpe-match"],
                "searched_cpe": component["cpe"],
                "found_cpes": sorted(set(found["cpes"])),
                "version_constraint": _bounded_text(
                    found.get("versionConstraint"),
                    label="vulnerability version constraint",
                    maximum=512,
                ),
            }
        )
    if len({item["id"] for item in projected}) != len(projected):
        raise ValueError("Grype Node advisory report duplicates a vulnerability ID")
    projected.sort(
        key=lambda item: (
            item["severity"], item["id"], item["installed_version"], item["fix_state"]
        )
    )
    return {
        "scanner": {"name": "grype", "version": GRYPE_VERSION},
        "configuration": {
            "stock_cpe_matching": True,
            "database_auto_update": False,
            "database_hash_validation": True,
            "database_age_validation": False,
            "database_update_check": False,
            "external_sources": False,
            "cpe_synthesis": False,
            "suppressed_matches_reported": True,
            "node_ignore_rules": False,
            "package_or_path_exclusions": False,
            "vex_documents": False,
        },
        "database": {**status, "provider": nvd},
        "input_sha256": hashlib.sha256(canonical_json_bytes(input_document)).hexdigest(),
        "matches": projected,
    }


def normalise_cyclonedx_report(
    report: dict[str, Any], input_document: dict[str, Any]
) -> dict[str, Any]:
    metadata = report.get("metadata")
    tools = metadata.get("tools", {}).get("components") if isinstance(metadata, dict) else None
    if (
        report.get("bomFormat") != "CycloneDX"
        or report.get("specVersion") not in {"1.5", "1.6", "1.7"}
        or not isinstance(tools, list)
        or {
            (item.get("name"), item.get("version"))
            for item in tools
            if isinstance(item, dict)
        }
        != {("grype", GRYPE_VERSION)}
    ):
        raise ValueError("Grype CycloneDX report lacks its pinned tool identity")
    expected = input_document["components"][0]
    components = report.get("components")
    if not isinstance(components, list):
        raise ValueError("Grype CycloneDX report lacks its component inventory")
    matching = [
        item
        for item in components
        if isinstance(item, dict) and item.get("purl") == expected["purl"]
    ]
    metadata_components = [
        item
        for item in components
        if isinstance(item, dict)
        and item.get("bom-ref") == "urn:gis-ai-go:node-runtime-advisory-input"
    ]
    if len(components) != 2 or len(matching) != 1 or len(metadata_components) != 1:
        raise ValueError("Grype CycloneDX report does not expose one exact Node component")
    component = matching[0]
    metadata_component = metadata_components[0]
    if (
        component.get("type") != "library"
        or component.get("name") != "node"
        or component.get("version") != expected["version"]
        or component.get("cpe") != expected["cpe"]
        or not isinstance(component.get("bom-ref"), str)
        or metadata_component.get("type") != "library"
        or metadata_component.get("name") != "gis-ai-go-node-runtime-advisory-input"
        or metadata_component.get("version") != expected["version"]
    ):
        raise ValueError("Grype CycloneDX Node component differs from its input")
    vulnerabilities = report.get("vulnerabilities") or []
    if not isinstance(vulnerabilities, list):
        raise ValueError("Grype CycloneDX vulnerability inventory is invalid")
    identifiers: list[str] = []
    for vulnerability in vulnerabilities:
        if not isinstance(vulnerability, dict):
            raise ValueError("Grype CycloneDX report contains an invalid vulnerability")
        identifier = _bounded_text(
            vulnerability.get("id"), label="CycloneDX vulnerability ID", maximum=64
        )
        affects = vulnerability.get("affects")
        if (
            _CVE.fullmatch(identifier) is None
            or not isinstance(affects, list)
            or len(affects) != 1
            or not isinstance(affects[0], dict)
            or affects[0].get("ref") != component["bom-ref"]
        ):
            raise ValueError("Grype CycloneDX vulnerability lacks its Node binding")
        identifiers.append(identifier)
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("Grype CycloneDX report duplicates a vulnerability ID")
    return {
        "scanner": {"name": "grype", "version": GRYPE_VERSION},
        "input_sha256": hashlib.sha256(canonical_json_bytes(input_document)).hexdigest(),
        "component": {
            "name": "node",
            "version": expected["version"],
            "purl": expected["purl"],
            "cpe": expected["cpe"],
        },
        "vulnerability_ids": sorted(identifiers),
    }


def _assess(
    cache: Path,
    input_document: dict[str, Any],
    *,
    database_source: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    raw_json = _scan_raw(cache, input_document, output_format="json")
    raw_cdx = _scan_raw(cache, input_document, output_format="cyclonedx-json")
    projected_json = normalise_json_report(
        raw_json, input_document, database_source=database_source
    )
    projected_cdx = normalise_cyclonedx_report(raw_cdx, input_document)
    json_ids = sorted(item["id"] for item in projected_json["matches"])
    if json_ids != projected_cdx["vulnerability_ids"]:
        raise ValueError("Grype JSON and CycloneDX Node findings disagree")
    return raw_json, raw_cdx, projected_json, projected_cdx


def _project_findings(report: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for item in report["matches"]:
        if item["severity"] not in {"HIGH", "CRITICAL"}:
            continue
        fixed_version = item["fixed_versions"][0] if item["fixed_versions"] else None
        result.append(
            {
                "target": "Node.js core",
                "id": item["id"],
                "package": "node",
                "installed_version": item["installed_version"],
                "fixed_version": fixed_version,
                "severity": item["severity"],
            }
        )
    return sorted(
        result,
        key=lambda item: (
            item["severity"], item["id"], item["installed_version"],
            item["fixed_version"] or "",
        ),
    )


def _bytes_binding(name: str, content: bytes) -> dict[str, Any]:
    return {
        "file": name,
        "sha256": hashlib.sha256(content).hexdigest(),
        "bytes": len(content),
    }


def _role_evidence(
    *,
    role: str,
    version: str,
    input_bytes: bytes,
    report_bytes: bytes,
    cdx_bytes: bytes,
    projected_json: dict[str, Any],
    projected_cdx: dict[str, Any],
) -> dict[str, Any]:
    files = NODE_ROLE_FILES[role]
    matched_ids = sorted(item["id"] for item in projected_json["matches"])
    high_critical_ids = sorted(
        item["id"]
        for item in projected_json["matches"]
        if item["severity"] in {"HIGH", "CRITICAL"}
    )
    if matched_ids != projected_cdx["vulnerability_ids"]:
        raise ValueError(f"Grype {role} JSON and CycloneDX findings disagree")
    return {
        "role": role,
        "version": version,
        "input": _bytes_binding(files["input"], input_bytes),
        "json_report": _bytes_binding(files["json_report"], report_bytes),
        "cyclonedx_report": _bytes_binding(files["cyclonedx_report"], cdx_bytes),
        "matched_ids": matched_ids,
        "high_critical_ids": high_critical_ids,
        "normalised_matches_sha256": hashlib.sha256(
            canonical_json_bytes(projected_json["matches"])
        ).hexdigest(),
        "component_visible": projected_cdx["component"]["version"] == version,
    }


def _calibration_projection(roles: dict[str, dict[str, Any]]) -> dict[str, Any]:
    affected = set(roles["affected"]["matched_ids"])
    affected_high = set(roles["affected"]["high_critical_ids"])
    fixed = set(roles["fixed"]["matched_ids"])
    if (
        not NODE_CALIBRATION_HIGH_IDS.issubset(affected)
        or not NODE_CALIBRATION_HIGH_IDS.issubset(affected_high)
        or NODE_CALIBRATION_HIGH_IDS & fixed
        or not roles["affected"]["component_visible"]
        or not roles["fixed"]["component_visible"]
    ):
        raise ValueError("Grype Node CPE calibration did not cross the fixed security boundary")
    return {
        "official_advisory": NODE_SECURITY_ADVISORY_URL,
        "required_high_ids": sorted(NODE_CALIBRATION_HIGH_IDS),
        "affected_role": "affected",
        "fixed_role": "fixed",
        "passed": True,
    }


def _actual_assessment(role: dict[str, Any]) -> dict[str, Any]:
    high_critical_ids = role.get("high_critical_ids")
    if not role.get("component_visible"):
        raise ValueError("Grype actual Node component is not visible in its output")
    if not isinstance(high_critical_ids, list) or high_critical_ids:
        raise ValueError("Grype actual Node component has a High or Critical NVD CPE match")
    return {
        "role": "actual",
        "component_visible": True,
        "matched_ids": role["matched_ids"],
        "high_critical_matched_ids": [],
        "passed": True,
    }


def assess_node(
    cache: Path,
    sbom: dict[str, Any],
    receipt: dict[str, Any],
    *,
    database_source: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, bytes], list[dict[str, Any]]]:
    identity = extract_node_identity(sbom, receipt)
    roles: dict[str, dict[str, Any]] = {}
    artifacts: dict[str, bytes] = {}
    projections: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    actual_boundary: dict[str, Any] | None = None
    for role, (version, calibration) in NODE_ROLES.items():
        input_document = make_node_input(
            identity, version=version, calibration=calibration
        )
        raw_json, raw_cdx, projected_json, projected_cdx = _assess(
            cache, input_document, database_source=database_source
        )
        if actual_boundary is None:
            actual_boundary = {
                "scanner": projected_json["scanner"],
                "configuration": projected_json["configuration"],
                "database": projected_json["database"],
            }
        elif any(
            projected_json[key] != value for key, value in actual_boundary.items()
        ):
            raise ValueError("Grype roles did not use the exact assessment boundary")
        input_bytes = canonical_json_bytes(input_document)
        report_bytes = canonical_json_bytes(raw_json)
        cdx_bytes = canonical_json_bytes(raw_cdx)
        for document, encoded, label in (
            (input_document, input_bytes, "input"),
            (raw_json, report_bytes, "JSON report"),
            (raw_cdx, cdx_bytes, "CycloneDX report"),
        ):
            assert_no_private_json(document, f"Grype Node {role} {label}")
            assert_no_private_text(encoded, f"Grype Node {role} {label}")
        files = NODE_ROLE_FILES[role]
        artifacts.update(
            {
                files["input"]: input_bytes,
                files["json_report"]: report_bytes,
                files["cyclonedx_report"]: cdx_bytes,
            }
        )
        roles[role] = _role_evidence(
            role=role,
            version=version,
            input_bytes=input_bytes,
            report_bytes=report_bytes,
            cdx_bytes=cdx_bytes,
            projected_json=projected_json,
            projected_cdx=projected_cdx,
        )
        projections[role] = (projected_json, projected_cdx)
    if actual_boundary is None:
        raise ValueError("Grype Node role inventory is empty")
    calibration = _calibration_projection(roles)
    actual_json, _ = projections["actual"]
    assessment = _actual_assessment(roles["actual"])
    evidence = {
        "scanner": {
            "image": GRYPE_REFERENCE,
            "version": GRYPE_VERSION,
            "platform": GRYPE_PLATFORM,
        },
        "component": identity,
        "database": actual_boundary["database"],
        "configuration": actual_boundary["configuration"],
        "roles": roles,
        "calibration": calibration,
        "assessment": assessment,
    }
    return evidence, artifacts, _project_findings(actual_json)


def _file_binding(path: Path, *, maximum_bytes: int) -> dict[str, Any]:
    metadata = path.lstat()
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISREG(metadata.st_mode)
        or metadata.st_size < 1
        or metadata.st_size > maximum_bytes
    ):
        raise ValueError(f"Grype evidence is not one regular file: {path.name}")
    return {"file": path.name, "sha256": sha256_file(path), "bytes": metadata.st_size}


def _read_evidence(path: Path, *, maximum_bytes: int, label: str) -> bytes:
    return read_bounded_regular_file(
        path, maximum_bytes=maximum_bytes, label=label
    )


def _database_age_seconds(database: dict[str, Any], assessed_at: str) -> int:
    built_value = database.get("built")
    if (
        not isinstance(built_value, str)
        or not built_value.endswith("Z")
        or not isinstance(assessed_at, str)
        or not assessed_at.endswith("Z")
    ):
        raise ValueError("Grype database freshness timestamps are invalid")
    try:
        built = datetime.fromisoformat(built_value[:-1] + "+00:00")
        assessed = datetime.fromisoformat(assessed_at[:-1] + "+00:00")
    except ValueError as error:
        raise ValueError("Grype database freshness timestamps are invalid") from error
    age = assessed - built
    if (
        built.tzinfo is None
        or assessed.tzinfo is None
        or age < timedelta(0)
        or age > MAX_DATABASE_AGE_AT_SCAN
    ):
        raise ValueError("Grype database is not current enough for the assessment")
    return round(age.total_seconds())


def _provider_age_seconds(database: dict[str, Any], assessed_at: str) -> int:
    built_value = database.get("built")
    provider = database.get("provider")
    captured_value = provider.get("captured") if isinstance(provider, dict) else None
    if (
        not isinstance(built_value, str)
        or not built_value.endswith("Z")
        or not isinstance(captured_value, str)
        or not captured_value.endswith("Z")
        or not isinstance(assessed_at, str)
        or not assessed_at.endswith("Z")
    ):
        raise ValueError("Grype NVD provider freshness timestamps are invalid")
    try:
        captured = datetime.fromisoformat(captured_value[:-1] + "+00:00")
        built = datetime.fromisoformat(built_value[:-1] + "+00:00")
        assessed = datetime.fromisoformat(assessed_at[:-1] + "+00:00")
    except ValueError as error:
        raise ValueError("Grype NVD provider freshness timestamps are invalid") from error
    age = assessed - captured
    if (
        captured.tzinfo is None
        or built.tzinfo is None
        or assessed.tzinfo is None
        or not captured <= built <= assessed
        or age > MAX_DATABASE_AGE_AT_SCAN
    ):
        raise ValueError("Grype NVD provider is not current enough for the assessment")
    return round(age.total_seconds())


def _trusted_verification_time() -> datetime:
    """Return the verifier clock used only by explicit same-run provenance checks."""
    return datetime.now(UTC)


def _verify_protected_provenance_freshness(
    assessed: datetime, *, verified_at: datetime
) -> None:
    if verified_at.tzinfo is None or verified_at.utcoffset() != timedelta(0):
        raise ValueError("protected provenance verifier clock is not UTC")
    age = verified_at - assessed
    if age < -MAX_PROTECTED_PROVENANCE_FUTURE_SKEW:
        raise ValueError("retained Grype assessment is ahead of the verifier clock")
    if age > MAX_PROTECTED_PROVENANCE_ASSESSMENT_AGE:
        raise ValueError("retained Grype assessment is too old for protected provenance")


def generate_node_advisory(
    *, sbom: dict[str, Any], receipt: dict[str, Any], output: Path
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    acquire_grype_image()
    database_archive = output / GRYPE_DB_ARCHIVE_NAME
    database_checksum = output / GRYPE_DB_CHECKSUM_NAME
    with tempfile.TemporaryDirectory(prefix="gis-ai-go-grype-online-") as temporary:
        cache = Path(temporary) / "cache"
        cache.mkdir(mode=0o700)
        online_status = update_database(cache)
        download_database_archive(online_status, database_archive)
    database_checksum.write_text(
        f"{sha256_file(database_archive)}  {database_archive.name}\n", encoding="utf-8"
    )
    with tempfile.TemporaryDirectory(prefix="gis-ai-go-grype-replay-") as temporary:
        cache = Path(temporary) / "cache"
        cache.mkdir(mode=0o700)
        replay_status = import_database(
            cache, database_archive, source=online_status
        )
        if _database_source_binding(replay_status) != online_status:
            raise ValueError("offline Grype import differs from the acquired database status")
        inventory_before = database_inventory(cache)
        node, artifacts, findings = assess_node(
            cache, sbom, receipt, database_source=online_status
        )
        if database_inventory(cache) != inventory_before:
            raise ValueError("offline Grype assessment mutated the imported database")
    assessed_at = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    age_seconds = _database_age_seconds(node["database"], assessed_at)
    provider_age_seconds = _provider_age_seconds(node["database"], assessed_at)
    for name, content in artifacts.items():
        (output / name).write_bytes(content)
    node["database"] = {
        **node["database"],
        "assessed_at": assessed_at,
        "age_seconds": age_seconds,
        "provider_age_seconds": provider_age_seconds,
        "archive": _file_binding(
            database_archive, maximum_bytes=MAX_GRYPE_DB_ARCHIVE_BYTES
        ),
        "expanded_files": inventory_before,
    }
    node["replay"] = {
        "pull": "never",
        "network": "none",
        "database_import": True,
        "database_age_validation": False,
        "database_hash_validation": True,
        "stock_cpe_matching": True,
    }
    return node, findings


def verify_node_advisory(
    *,
    node: dict[str, Any],
    directory: Path,
    sbom: dict[str, Any],
    receipt: dict[str, Any],
    phase: dict[str, Any],
    replay: bool,
    require_current_assessment: bool = False,
) -> list[dict[str, Any]]:
    identity = extract_node_identity(sbom, receipt)
    if node.get("component") != identity:
        raise ValueError("retained Grype Node component differs from the exact runtime")
    archive = directory / GRYPE_DB_ARCHIVE_NAME
    checksum = directory / GRYPE_DB_CHECKSUM_NAME
    archive_binding = _file_binding(
        archive, maximum_bytes=MAX_GRYPE_DB_ARCHIVE_BYTES
    )
    if parse_checksum(checksum, archive.name) != archive_binding["sha256"]:
        raise ValueError("retained Grype database checksum differs")
    if node.get("database", {}).get("archive") != archive_binding:
        raise ValueError("retained Grype database binding differs")
    database = node.get("database")
    if not isinstance(database, dict) or database.get("load_mode") != "manual-import":
        raise ValueError("retained Grype Node database binding is missing")
    database_source = _database_source_binding(database)
    retained_roles = node.get("roles")
    if not isinstance(retained_roles, dict) or set(retained_roles) != set(NODE_ROLES):
        raise ValueError("retained Grype Node role inventory is not closed")
    expected_roles: dict[str, dict[str, Any]] = {}
    projections: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for role, (version, calibration) in NODE_ROLES.items():
        expected_input = make_node_input(
            identity, version=version, calibration=calibration
        )
        files = NODE_ROLE_FILES[role]
        input_bytes = _read_evidence(
            directory / files["input"],
            maximum_bytes=MAX_GRYPE_REPORT_BYTES,
            label=f"retained Grype {role} input",
        )
        if input_bytes != canonical_json_bytes(expected_input):
            raise ValueError(f"retained Grype {role} input differs from its role")
        report_bytes = _read_evidence(
            directory / files["json_report"],
            maximum_bytes=MAX_GRYPE_REPORT_BYTES,
            label=f"retained Grype {role} JSON report",
        )
        cdx_bytes = _read_evidence(
            directory / files["cyclonedx_report"],
            maximum_bytes=MAX_GRYPE_REPORT_BYTES,
            label=f"retained Grype {role} CycloneDX report",
        )
        report = _parse_json(report_bytes, label=f"retained Grype {role} JSON report")
        cdx = _parse_json(cdx_bytes, label=f"retained Grype {role} CycloneDX report")
        if (
            canonical_json_bytes(report) != report_bytes
            or canonical_json_bytes(cdx) != cdx_bytes
        ):
            raise ValueError(f"retained Grype {role} report is not canonical")
        projected_json = normalise_json_report(
            report, expected_input, database_source=database_source
        )
        projected_cdx = normalise_cyclonedx_report(cdx, expected_input)
        expected_roles[role] = _role_evidence(
            role=role,
            version=version,
            input_bytes=input_bytes,
            report_bytes=report_bytes,
            cdx_bytes=cdx_bytes,
            projected_json=projected_json,
            projected_cdx=projected_cdx,
        )
        projections[role] = (projected_json, projected_cdx)
    if retained_roles != expected_roles:
        raise ValueError("retained Grype Node role bindings differ from their evidence")
    actual_json, _ = projections["actual"]
    for role, (projected_json, _) in projections.items():
        if (
            projected_json["scanner"] != actual_json["scanner"]
            or projected_json["configuration"] != actual_json["configuration"]
            or projected_json["database"] != actual_json["database"]
        ):
            raise ValueError(f"retained Grype {role} boundary differs from actual")
    static_expected = {
        "scanner": {
            "image": GRYPE_REFERENCE,
            "version": GRYPE_VERSION,
            "platform": GRYPE_PLATFORM,
        },
        "component": identity,
        "configuration": actual_json["configuration"],
    }
    for key, value in static_expected.items():
        if node.get(key) != value:
            raise ValueError("retained Grype Node assessment differs from its reports")
    report_database = actual_json["database"]
    if any(database.get(key) != value for key, value in report_database.items()):
        raise ValueError("retained Grype report and database binding disagree")
    if database.get("source_sha256") != sha256_file(archive):
        raise ValueError("retained Grype archive differs from its published checksum")
    assessed_at = database.get("assessed_at")
    if not isinstance(assessed_at, str):
        raise ValueError("retained Grype assessment timestamp is missing")
    if database.get("age_seconds") != _database_age_seconds(database, assessed_at):
        raise ValueError("retained Grype database age projection differs")
    if database.get("provider_age_seconds") != _provider_age_seconds(
        database, assessed_at
    ):
        raise ValueError("retained Grype NVD provider age projection differs")
    if (
        not assessed_at.endswith("Z")
        or not isinstance(phase.get("started_at"), str)
        or not phase["started_at"].endswith("Z")
        or not isinstance(phase.get("completed_at"), str)
        or not phase["completed_at"].endswith("Z")
    ):
        raise ValueError("retained Grype assessment timing is invalid")
    try:
        assessed = datetime.fromisoformat(assessed_at[:-1] + "+00:00")
        phase_started = datetime.fromisoformat(
            phase["started_at"][:-1] + "+00:00"
        )
        phase_completed = datetime.fromisoformat(
            phase["completed_at"][:-1] + "+00:00"
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("retained Grype assessment timing is invalid") from error
    if not phase_started <= assessed <= phase_completed:
        raise ValueError("retained Grype assessment is outside the scan phase")
    if require_current_assessment:
        _verify_protected_provenance_freshness(
            assessed, verified_at=_trusted_verification_time()
        )
    calibration = _calibration_projection(expected_roles)
    if node.get("calibration") != calibration:
        raise ValueError("retained Grype Node calibration is incomplete")
    assessment = _actual_assessment(expected_roles["actual"])
    if node.get("assessment") != assessment:
        raise ValueError("retained Grype Node assessment projection differs")
    expected_replay = {
        "pull": "never",
        "network": "none",
        "database_import": True,
        "database_age_validation": False,
        "database_hash_validation": True,
        "stock_cpe_matching": True,
    }
    if node.get("replay") != expected_replay:
        raise ValueError("retained Grype Node replay boundary differs")
    if replay:
        with tempfile.TemporaryDirectory(prefix="gis-ai-go-grype-verify-") as temporary:
            cache = Path(temporary) / "cache"
            cache.mkdir(mode=0o700)
            status = import_database(cache, archive, source=database_source)
            if status != {**database_source, "load_mode": "manual-import"}:
                raise ValueError("verification Grype import differs from retained status")
            inventory = database_inventory(cache)
            if inventory != database.get("expanded_files"):
                raise ValueError("verification Grype database inventory differs")
            replay_node, _, replay_findings = assess_node(
                cache, sbom, receipt, database_source=database_source
            )
            if database_inventory(cache) != inventory:
                raise ValueError("verification Grype assessment mutated its database")
        replay_database = replay_node["database"]
        if (
            replay_node["component"] != identity
            or replay_node["configuration"] != actual_json["configuration"]
            or replay_database != report_database
            or replay_node["calibration"] != calibration
            or replay_node["assessment"] != assessment
            or any(
                replay_node["roles"][role][key] != expected_roles[role][key]
                for role in NODE_ROLES
                for key in (
                    "role",
                    "version",
                    "input",
                    "matched_ids",
                    "high_critical_ids",
                    "normalised_matches_sha256",
                    "component_visible",
                )
            )
        ):
            raise ValueError("offline Grype Node replay differs from retained evidence")
        return replay_findings
    return _project_findings(actual_json)


def restore_database_from_scan(*, scan_path: Path, output: Path) -> Path:
    """Rehydrate the non-published DB directly from its exact Anchore source."""
    output_metadata = output.lstat()
    if stat.S_ISLNK(output_metadata.st_mode) or not stat.S_ISDIR(output_metadata.st_mode):
        raise ValueError("Grype restore output must be one real evidence directory")
    scan_bytes = _read_evidence(
        scan_path,
        maximum_bytes=MAX_GRYPE_REPORT_BYTES,
        label="gateway vulnerability receipt for Grype restore",
    )
    scan = parse_bounded_json_object(
        scan_bytes,
        maximum_bytes=MAX_GRYPE_REPORT_BYTES,
        label="gateway vulnerability receipt for Grype restore",
    )
    if canonical_json_bytes(scan) != scan_bytes:
        raise ValueError("gateway vulnerability receipt for Grype restore is not canonical")
    if scan_path.resolve(strict=True).parent != output.resolve(strict=True):
        raise ValueError("Grype restore receipt must belong to its evidence directory")
    node = scan.get("node_runtime")
    if (
        scan.get("schema") != "gis-ai-go.gateway-image-vulnerability-scan.v3"
        or not isinstance(node, dict)
        or node.get("scanner")
        != {
            "image": GRYPE_REFERENCE,
            "version": GRYPE_VERSION,
            "platform": GRYPE_PLATFORM,
        }
    ):
        raise ValueError("gateway receipt lacks the exact Grype restore identity")
    database = node.get("database")
    if not isinstance(database, dict):
        raise ValueError("gateway receipt lacks the Grype restore database")
    source = database.get("source_url")
    source_sha256 = database.get("source_sha256")
    archive_binding = database.get("archive")
    provider = database.get("provider")
    if (
        not isinstance(source, str)
        or not isinstance(source_sha256, str)
        or _database_source_sha256(source) != source_sha256
        or database.get("valid") is not True
        or not isinstance(provider, dict)
        or provider.get("name") != "nvd"
        or not isinstance(archive_binding, dict)
        or archive_binding.get("file") != GRYPE_DB_ARCHIVE_NAME
        or archive_binding.get("sha256") != source_sha256
        or type(archive_binding.get("bytes")) is not int
        or archive_binding["bytes"] < 1
        or archive_binding["bytes"] > MAX_GRYPE_DB_ARCHIVE_BYTES
    ):
        raise ValueError("gateway receipt Grype restore database binding differs")
    archive = output / GRYPE_DB_ARCHIVE_NAME
    checksum = output / GRYPE_DB_CHECKSUM_NAME
    if archive.exists() or archive.is_symlink():
        raise ValueError("Grype restore refuses to overwrite a retained database")
    if parse_checksum(checksum, archive.name) != source_sha256:
        raise ValueError("retained Grype restore checksum differs from its source")
    download_database_archive(
        {"source_url": source, "source_sha256": source_sha256}, archive
    )
    try:
        if (
            _file_binding(
                archive, maximum_bytes=MAX_GRYPE_DB_ARCHIVE_BYTES
            )
            != archive_binding
        ):
            raise ValueError("rehydrated Grype database differs from its receipt")
    except Exception:
        archive.unlink(missing_ok=True)
        raise
    return archive


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Restore private Grype replay evidence from its exact upstream source."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    restore = subparsers.add_parser("restore-database")
    restore.add_argument("--scan", type=Path, required=True)
    restore.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "restore-database":
        restore_database_from_scan(
            scan_path=args.scan.resolve(), output=args.output_dir.resolve()
        )


if __name__ == "__main__":
    main()
