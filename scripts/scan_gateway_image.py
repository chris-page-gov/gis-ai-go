#!/usr/bin/env python3
"""Generate and verify retained, offline-replayable gateway vulnerability evidence."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import stat
import subprocess
import tarfile
import tempfile
import time
import unicodedata
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO

from jsonschema import Draft202012Validator, FormatChecker

from gateway_evidence import (
    MAX_RECEIPT_JSON_BYTES,
    MAX_SBOM_JSON_BYTES,
    MAX_SCAN_JSON_BYTES,
    MAX_SCHEMA_JSON_BYTES,
    load_bounded_json_object,
    parse_bounded_json_object,
    read_bounded_regular_file,
)
from gateway_image import (
    ROOT,
    TRIVY_REFERENCE,
    assert_no_private_json,
    assert_no_private_text,
    canonical_json_bytes,
    contains_diagnostic_private_path,
    parse_checksum,
    prohibited_text_reason,
    sha256_file,
)

BLOCKED_SEVERITIES = frozenset({"HIGH", "CRITICAL"})
TRIVY_VERSION = "0.74.0"
SCAN_SCHEMA = ROOT / "schemas" / "gateway-image-vulnerability-scan.schema.json"
DB_ARCHIVE_NAME = "gateway-image.trivy-db.tar.gz"
DB_CHECKSUM_NAME = f"{DB_ARCHIVE_NAME}.sha256"
REPORT_NAME = "gateway-image.trivy-report.json"
EXPECTED_DB_FILES = frozenset({"db/metadata.json", "db/trivy.db"})
MAX_DB_FILES = 8
MAX_DB_EXPANDED_BYTES = 2 * 1024 * 1024 * 1024
MAX_DB_ARCHIVE_BYTES = 768 * 1024 * 1024
MAX_REPORT_BYTES = 32 * 1024 * 1024
MAX_FINDINGS = 10_000
TIMING_TOLERANCE_MS = 2_000
MAX_TRIVY_DIAGNOSTIC_BYTES = 4 * 1024
MAX_TRIVY_DIAGNOSTIC_RENDERED_BYTES = 4 * MAX_TRIVY_DIAGNOSTIC_BYTES + 2
TRIVY_SCAN_TIMEOUT_SECONDS = 20 * 60

_DIAGNOSTIC_SENSITIVE = re.compile(
    r"(?i)(?:"
    r"bearer|auth|oauth|credentials?|api[ _-]?keys?|"
    r"(?:access|refresh)[ _-]?tokens?|tokens?|"
    r"passwords?|passwd|pwd|client[ _-]?secrets?|secrets?"
    r")"
)


def utc_timestamp() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _sanitise_trivy_diagnostic(value: object, *, label: str) -> str:
    """Return one closed stream projection without reflecting unsafe text."""
    if not isinstance(value, bytes):
        return f"{label}_status=unavailable"
    if len(value) > MAX_TRIVY_DIAGNOSTIC_BYTES:
        return (
            f"{label}_status=withheld "
            f"{label}_reason=over-bound {label}_truncated=true"
        )
    try:
        text = value.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return f"{label}_status=withheld {label}_reason=invalid-utf8"
    if any(
        unicodedata.category(character).startswith("C")
        and character not in "\t\n\r"
        for character in text
    ):
        return f"{label}_status=withheld {label}_reason=unsafe-control"
    prohibited_reason = prohibited_text_reason(text)
    normalised = " ".join(text.split())
    if prohibited_reason is None:
        prohibited_reason = prohibited_text_reason(normalised)
    if prohibited_reason is not None:
        return f"{label}_status=withheld {label}_reason={prohibited_reason}"
    if contains_diagnostic_private_path(normalised):
        return f"{label}_status=withheld {label}_reason=private-path"
    if _DIAGNOSTIC_SENSITIVE.search(normalised):
        return f"{label}_status=withheld {label}_reason=sensitive"
    rendered = json.dumps(normalised or "[empty]", ensure_ascii=True)
    if len(rendered.encode("ascii")) > MAX_TRIVY_DIAGNOSTIC_RENDERED_BYTES:
        return f"{label}_status=withheld {label}_reason=encoded-bound"
    metadata = (
        f"{label}_bytes={len(value)} "
        f"{label}_sha256={hashlib.sha256(value).hexdigest()}"
    )
    return f"{metadata} {label}_status=readable {label}_text={rendered}"


def _safe_relative_path(value: str) -> str:
    logical = PurePosixPath(value)
    if (
        not value
        or value.startswith("/")
        or "\\" in value
        or "\0" in value
        or logical.is_absolute()
        or any(part in {"", ".", ".."} for part in logical.parts)
    ):
        raise ValueError(f"unsafe Trivy database path: {value!r}")
    return logical.as_posix()


def cache_inventory(root: Path) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []
    total = 0
    for current, directories, names in os.walk(root, followlinks=False):
        directories.sort()
        names.sort()
        current_path = Path(current)
        for directory in directories:
            if stat.S_ISLNK((current_path / directory).lstat().st_mode):
                raise ValueError("Trivy cache contains a symbolic-link directory")
        for name in names:
            path = current_path / name
            metadata = path.lstat()
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
                raise ValueError("Trivy cache contains a link or special file")
            logical = path.relative_to(root).as_posix()
            total += metadata.st_size
            if len(files) >= MAX_DB_FILES or total > MAX_DB_EXPANDED_BYTES:
                raise ValueError("Trivy database exceeds its retained evidence bound")
            files.append(
                {"path": logical, "sha256": sha256_file(path), "bytes": metadata.st_size}
            )
    if {item["path"] for item in files} != EXPECTED_DB_FILES:
        raise ValueError("Trivy database cache inventory is not closed")
    return files


def _copy_stream(source: BinaryIO, destination: BinaryIO, maximum: int) -> tuple[str, int]:
    digest = hashlib.sha256()
    total = 0
    while chunk := source.read(1024 * 1024):
        total += len(chunk)
        if total > maximum:
            raise ValueError("retained Trivy database member exceeds its bound")
        digest.update(chunk)
        destination.write(chunk)
    return digest.hexdigest(), total


def package_database(cache: Path, archive_path: Path) -> list[dict[str, Any]]:
    inventory = cache_inventory(cache)
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = archive_path.with_suffix(archive_path.suffix + ".tmp")
    with temporary.open("wb") as raw:
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=raw, compresslevel=6, mtime=0
        ) as compressed:
            with tarfile.open(
                fileobj=compressed, mode="w|", format=tarfile.USTAR_FORMAT
            ) as archive:
                directory = tarfile.TarInfo("db")
                directory.type = tarfile.DIRTYPE
                directory.mode = 0o755
                directory.uid = 65532
                directory.gid = 65532
                directory.mtime = 0
                archive.addfile(directory)
                for item in inventory:
                    member = tarfile.TarInfo(item["path"])
                    member.type = tarfile.REGTYPE
                    member.mode = 0o644
                    member.uid = 65532
                    member.gid = 65532
                    member.mtime = 0
                    member.size = item["bytes"]
                    with (cache / item["path"]).open("rb") as source:
                        archive.addfile(member, source)
    if temporary.stat().st_size > MAX_DB_ARCHIVE_BYTES:
        temporary.unlink(missing_ok=True)
        raise ValueError("compressed Trivy database exceeds its evidence bound")
    temporary.replace(archive_path)
    return inventory


def _bounded_files_equal(left: Path, right: Path, *, maximum_bytes: int) -> bool:
    left_metadata = left.lstat()
    right_metadata = right.lstat()
    if (
        stat.S_ISLNK(left_metadata.st_mode)
        or stat.S_ISLNK(right_metadata.st_mode)
        or not stat.S_ISREG(left_metadata.st_mode)
        or not stat.S_ISREG(right_metadata.st_mode)
        or left_metadata.st_size != right_metadata.st_size
        or left_metadata.st_size > maximum_bytes
    ):
        return False
    with left.open("rb") as left_source, right.open("rb") as right_source:
        while True:
            left_chunk = left_source.read(1024 * 1024)
            right_chunk = right_source.read(1024 * 1024)
            if left_chunk != right_chunk:
                return False
            if not left_chunk:
                return True


def inspect_database_archive(
    archive_path: Path, *, extract_to: Path | None = None
) -> list[dict[str, Any]]:
    metadata = archive_path.lstat()
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISREG(metadata.st_mode)
        or metadata.st_size > MAX_DB_ARCHIVE_BYTES
    ):
        raise ValueError("retained Trivy database archive is invalid or over its bound")
    temporary: tempfile.TemporaryDirectory[str] | None = None
    if extract_to is None:
        temporary = tempfile.TemporaryDirectory(prefix="gis-ai-go-trivy-inspect-")
        extraction_root = Path(temporary.name) / "cache"
        extraction_root.mkdir(mode=0o700)
    else:
        extraction_root = extract_to
        extraction_metadata = extraction_root.lstat()
        if (
            stat.S_ISLNK(extraction_metadata.st_mode)
            or not stat.S_ISDIR(extraction_metadata.st_mode)
            or any(extraction_root.iterdir())
        ):
            raise ValueError("Trivy database extraction root is not an empty regular directory")

    try:
        inventory: list[dict[str, Any]] = []
        total = 0
        with tarfile.open(archive_path, "r:gz") as archive:
            expected_names = ["db", "db/metadata.json", "db/trivy.db"]
            member_count = 0
            for member in archive:
                if (
                    member_count >= len(expected_names)
                    or member.name != expected_names[member_count]
                ):
                    raise ValueError(
                        "retained Trivy database archive inventory is not canonical"
                    )
                member_count += 1
                name = _safe_relative_path(member.name)
                expected_mode = 0o755 if member.isdir() else 0o644
                if (
                    member.uid != 65532
                    or member.gid != 65532
                    or member.uname != ""
                    or member.gname != ""
                    or member.mtime != 0
                    or member.mode != expected_mode
                    or member.pax_headers
                ):
                    raise ValueError("retained Trivy database metadata is not canonical")
                if member.isdir():
                    if name != "db":
                        raise ValueError(
                            "retained Trivy database has an unexpected directory"
                        )
                    (extraction_root / name).mkdir(
                        mode=0o755, parents=True, exist_ok=False
                    )
                    continue
                if not member.isreg():
                    raise ValueError(
                        "retained Trivy database contains a link or special member"
                    )
                total += member.size
                if total > MAX_DB_EXPANDED_BYTES:
                    raise ValueError(
                        "retained Trivy database exceeds its expanded bound"
                    )
                extracted = archive.extractfile(member)
                if extracted is None:
                    raise ValueError("retained Trivy database member is unavailable")
                target = extraction_root / name
                target.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
                with target.open("xb") as sink:
                    digest, size = _copy_stream(extracted, sink, member.size)
                target.chmod(0o600)
                if size != member.size:
                    raise ValueError(
                        "retained Trivy database member size changed while reading"
                    )
                inventory.append({"path": name, "sha256": digest, "bytes": size})
            if member_count != len(expected_names):
                raise ValueError("retained Trivy database archive is incomplete")
        if {item["path"] for item in inventory} != EXPECTED_DB_FILES:
            raise ValueError("retained Trivy database file inventory is not closed")

        with tempfile.TemporaryDirectory(
            prefix="gis-ai-go-trivy-canonical-"
        ) as canonical_temporary:
            canonical_archive = Path(canonical_temporary) / DB_ARCHIVE_NAME
            canonical_inventory = package_database(extraction_root, canonical_archive)
            if canonical_inventory != inventory or not _bounded_files_equal(
                archive_path,
                canonical_archive,
                maximum_bytes=MAX_DB_ARCHIVE_BYTES,
            ):
                raise ValueError(
                    "retained Trivy database is not the canonical gzip and USTAR encoding"
                )
        return inventory
    finally:
        if temporary is not None:
            temporary.cleanup()


def _bounded_text(value: Any, *, label: str, maximum: int) -> str:
    if not isinstance(value, str) or not value or len(value) > maximum:
        raise ValueError(f"Trivy report {label} is missing or outside its bound")
    return value


def validate_trivy_report(document: dict[str, Any]) -> None:
    if (
        not isinstance(document, dict)
        or document.get("Trivy") != {"Version": TRIVY_VERSION}
        or not isinstance(document.get("Results"), list)
    ):
        raise ValueError("retained report lacks the exact Trivy identity or result shape")


def project_findings(document: dict[str, Any]) -> list[dict[str, Any]]:
    validate_trivy_report(document)
    projected: list[dict[str, Any]] = []
    results = document.get("Results")
    assert isinstance(results, list)
    for result in results:
        if not isinstance(result, dict):
            raise ValueError("Trivy report contains an invalid target")
        target = _bounded_text(result.get("Target"), label="target", maximum=1_024)
        findings = result.get("Vulnerabilities") or []
        if not isinstance(findings, list):
            raise ValueError("Trivy report target or vulnerability list is invalid")
        for finding in findings:
            if not isinstance(finding, dict):
                raise ValueError("Trivy report contains an invalid vulnerability")
            severity = finding.get("Severity")
            if severity not in BLOCKED_SEVERITIES:
                raise ValueError("Trivy report contains a finding outside the requested severities")
            identifier = _bounded_text(
                finding.get("VulnerabilityID"), label="vulnerability ID", maximum=256
            )
            package = _bounded_text(
                finding.get("PkgName"), label="package name", maximum=512
            )
            installed = _bounded_text(
                finding.get("InstalledVersion"),
                label="installed version",
                maximum=512,
            )
            fixed = finding.get("FixedVersion")
            if fixed is None or fixed == "":
                fixed_version = None
            elif isinstance(fixed, str) and len(fixed) <= 1_024:
                fixed_version = fixed
            else:
                raise ValueError("Trivy report fixed version has an invalid type or length")
            projected.append(
                {
                    "target": target,
                    "id": identifier,
                    "package": package,
                    "installed_version": installed,
                    "fixed_version": fixed_version,
                    "severity": severity,
                }
            )
            if len(projected) > MAX_FINDINGS:
                raise ValueError("Trivy report exceeds the retained finding-count bound")
    return sorted(
        projected,
        key=lambda item: (
            item["severity"], item["id"], item["target"], item["package"],
            item["installed_version"], item["fixed_version"] or "",
        ),
    )


def evaluate_policy(findings: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], bool]:
    fixable = [item for item in findings if item["fixed_version"] is not None]
    return fixable, not fixable


def _acquire_trivy_image() -> None:
    subprocess.run(
        ("docker", "pull", TRIVY_REFERENCE),
        cwd=ROOT,
        check=True,
        timeout=20 * 60,
    )


def _docker_scan(*, cache: Path, sbom: Path, offline: bool, pull: str) -> dict[str, Any]:
    if offline and pull != "never":
        raise ValueError("offline Trivy replay must use Docker pull=never")
    scanner_uid = os.getuid()
    scanner_gid = os.getgid()
    arguments = [
        "docker", "run", "--rm", f"--pull={pull}", "--read-only", "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        f"--user={scanner_uid}:{scanner_gid}",
        (
            "--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=512m,mode=0700,"
            f"uid={scanner_uid},gid={scanner_gid}"
        ),
        f"--volume={sbom}:/input/gateway-image.sbom.cdx.json:ro",
        f"--volume={cache}:/cache",
    ]
    if offline:
        arguments.append("--network=none")
    arguments.extend(
        [
            TRIVY_REFERENCE, "sbom", "--cache-dir=/cache", "--scanners=vuln",
            "--severity=HIGH,CRITICAL", "--format=json", "--no-progress",
        ]
    )
    if offline:
        arguments.extend(["--skip-db-update", "--offline-scan"])
    arguments.append("/input/gateway-image.sbom.cdx.json")
    result: subprocess.CompletedProcess[bytes] | None = None
    failure: ValueError | None = None
    try:
        result = subprocess.run(
            tuple(arguments),
            cwd=ROOT,
            check=True,
            capture_output=True,
            timeout=TRIVY_SCAN_TIMEOUT_SECONDS,
        )
    except subprocess.CalledProcessError as error:
        return_code = error.returncode if type(error.returncode) is int else "unknown"
        stdout = _sanitise_trivy_diagnostic(error.stdout, label="stdout")
        stderr = _sanitise_trivy_diagnostic(error.stderr, label="stderr")
        failure = ValueError(
            f"pinned Trivy scan failed with exit code {return_code}; "
            f"{stdout}; {stderr}"
        )
    except subprocess.TimeoutExpired as error:
        stdout = _sanitise_trivy_diagnostic(error.stdout, label="stdout")
        stderr = _sanitise_trivy_diagnostic(error.stderr, label="stderr")
        failure = ValueError(
            f"pinned Trivy scan timed out after {TRIVY_SCAN_TIMEOUT_SECONDS} seconds; "
            f"{stdout}; {stderr}"
        )
    except OSError:
        failure = ValueError("pinned Trivy scan could not be started")
    if failure is not None:
        raise failure
    if result is None:
        raise ValueError("pinned Trivy scan completed without a process result")
    if len(result.stdout) > MAX_REPORT_BYTES:
        raise ValueError("Trivy report exceeds its evidence bound")
    report = parse_bounded_json_object(
        result.stdout,
        maximum_bytes=MAX_REPORT_BYTES,
        label="pinned Trivy scan report",
    )
    validate_trivy_report(report)
    return report


def replay_projection(document: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in document.items() if key not in {"CreatedAt", "ReportID"}}


def verify_phase_timing(phase: dict[str, Any]) -> None:
    if not isinstance(phase, dict) or type(phase.get("duration_ms")) is not int:
        raise ValueError("gateway vulnerability scan timing has an invalid shape")
    started_at = phase.get("started_at")
    completed_at = phase.get("completed_at")
    if (
        not isinstance(started_at, str)
        or not started_at.endswith("Z")
        or not isinstance(completed_at, str)
        or not completed_at.endswith("Z")
    ):
        raise ValueError("gateway vulnerability scan timestamps must be explicit UTC")
    try:
        started = datetime.fromisoformat(started_at[:-1] + "+00:00")
        completed = datetime.fromisoformat(completed_at[:-1] + "+00:00")
    except ValueError as error:
        raise ValueError("gateway vulnerability scan timestamps are invalid") from error
    elapsed_ms = round((completed - started).total_seconds() * 1000)
    if (
        elapsed_ms <= 0
        or phase["duration_ms"] <= 0
        or abs(phase["duration_ms"] - elapsed_ms) > TIMING_TOLERANCE_MS
    ):
        raise ValueError("gateway vulnerability scan timing is inconsistent")


def generate_scan_evidence(*, sbom: Path, receipt_path: Path, output: Path) -> dict[str, Any]:
    receipt = load_bounded_json_object(
        receipt_path,
        maximum_bytes=MAX_RECEIPT_JSON_BYTES,
        label="gateway image receipt",
    )
    started_at = utc_timestamp()
    started = time.monotonic()
    output.parent.mkdir(parents=True, exist_ok=True)
    archive_path = output.parent / DB_ARCHIVE_NAME
    checksum_path = output.parent / DB_CHECKSUM_NAME
    report_path = output.parent / REPORT_NAME
    _acquire_trivy_image()
    with tempfile.TemporaryDirectory(prefix="gis-ai-go-trivy-online-") as online_temporary:
        online_cache = Path(online_temporary) / "cache"
        online_cache.mkdir(mode=0o700)
        _docker_scan(cache=online_cache, sbom=sbom, offline=False, pull="never")
        inventory = package_database(online_cache, archive_path)
    checksum_path.write_text(
        f"{sha256_file(archive_path)}  {archive_path.name}\n", encoding="utf-8"
    )
    with tempfile.TemporaryDirectory(prefix="gis-ai-go-trivy-replay-") as replay_temporary:
        replay_cache = Path(replay_temporary) / "cache"
        replay_cache.mkdir(mode=0o700)
        extracted_inventory = inspect_database_archive(archive_path, extract_to=replay_cache)
        if extracted_inventory != inventory:
            raise ValueError("retained Trivy database differs after canonical extraction")
        report = _docker_scan(cache=replay_cache, sbom=sbom, offline=True, pull="never")
        if cache_inventory(replay_cache) != inventory:
            raise ValueError("offline Trivy replay mutated the retained database")
    report_bytes = canonical_json_bytes(report)
    assert_no_private_json(report, "gateway Trivy report")
    assert_no_private_text(report_bytes, "gateway Trivy report")
    findings = project_findings(report)
    fixable, passed = evaluate_policy(findings)
    evidence = {
        "schema": "gis-ai-go.gateway-image-vulnerability-scan.v1",
        "classification": (
            "repository-only-blocked-candidate"
            if receipt["source"]["clean"] else "non-publishable-development-build"
        ),
        "source_revision": receipt["source"]["revision"],
        "image_manifest_digest": receipt["image"]["manifest_digest"],
        "scanner": {"image": TRIVY_REFERENCE, "version": TRIVY_VERSION},
        "sbom": {"file": sbom.name, "sha256": sha256_file(sbom), "bytes": sbom.stat().st_size},
        "database": {
            "archive": archive_path.name, "archive_sha256": sha256_file(archive_path),
            "archive_bytes": archive_path.stat().st_size,
            "expanded_bytes": sum(item["bytes"] for item in inventory),
            "file_count": len(inventory), "files": inventory,
        },
        "report": {
            "file": report_path.name, "sha256": hashlib.sha256(report_bytes).hexdigest(),
            "bytes": len(report_bytes),
        },
        "replay": {
            "pull": "never",
            "network": "none",
            "skip_db_update": True,
            "offline_scan": True,
        },
        "policy": {
            "severities": sorted(BLOCKED_SEVERITIES), "block_fixable_only": True,
            "maximum_fixable_findings": 0,
        },
        "findings": findings,
        "fixable_findings": fixable,
        "passed": passed,
        "phase": {
            "started_at": started_at, "completed_at": utc_timestamp(),
            "duration_ms": round((time.monotonic() - started) * 1000),
        },
        "claims": {
            "public_deployment": False, "production_activation": False,
            "live_provider_call": False,
        },
    }
    schema = load_bounded_json_object(
        SCAN_SCHEMA,
        maximum_bytes=MAX_SCHEMA_JSON_BYTES,
        label="gateway vulnerability receipt schema",
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(evidence)
    output_bytes = canonical_json_bytes(evidence)
    assert_no_private_json(evidence, "gateway vulnerability evidence")
    assert_no_private_text(output_bytes, "gateway vulnerability evidence")
    report_path.write_bytes(report_bytes)
    output.write_bytes(output_bytes)
    if not passed:
        raise AssertionError(
            f"gateway image has {len(fixable)} fixable high or critical vulnerabilities"
        )
    return evidence


def verify_scan_evidence(
    *, scan_path: Path, sbom: Path, receipt_path: Path, replay: bool
) -> dict[str, Any]:
    scan_bytes = read_bounded_regular_file(
        scan_path,
        maximum_bytes=MAX_SCAN_JSON_BYTES,
        label="gateway vulnerability receipt",
    )
    scan = parse_bounded_json_object(
        scan_bytes,
        maximum_bytes=MAX_SCAN_JSON_BYTES,
        label="gateway vulnerability receipt",
    )
    schema = load_bounded_json_object(
        SCAN_SCHEMA,
        maximum_bytes=MAX_SCHEMA_JSON_BYTES,
        label="gateway vulnerability receipt schema",
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(scan)
    if canonical_json_bytes(scan) != scan_bytes:
        raise ValueError("gateway vulnerability receipt is not canonical JSON")
    receipt = load_bounded_json_object(
        receipt_path,
        maximum_bytes=MAX_RECEIPT_JSON_BYTES,
        label="gateway image receipt",
    )
    sbom_bytes = read_bounded_regular_file(
        sbom,
        maximum_bytes=MAX_SBOM_JSON_BYTES,
        label="gateway image SBOM",
    )
    expected_classification = (
        "repository-only-blocked-candidate"
        if receipt["source"]["clean"]
        else "non-publishable-development-build"
    )
    if (
        scan["classification"] != expected_classification
        or scan["source_revision"] != receipt["source"]["revision"]
        or scan["image_manifest_digest"] != receipt["image"]["manifest_digest"]
        or scan["sbom"]
        != {
            "file": sbom.name,
            "sha256": hashlib.sha256(sbom_bytes).hexdigest(),
            "bytes": len(sbom_bytes),
        }
    ):
        raise ValueError("gateway vulnerability receipt differs from source, image or SBOM")
    archive = scan_path.parent / scan["database"]["archive"]
    checksum = scan_path.parent / DB_CHECKSUM_NAME
    if parse_checksum(checksum, archive.name) != sha256_file(archive):
        raise ValueError("retained Trivy database checksum differs")
    archive_metadata = archive.lstat()
    with tempfile.TemporaryDirectory(prefix="gis-ai-go-trivy-verify-") as temporary:
        cache = Path(temporary) / "cache"
        cache.mkdir(mode=0o700)
        inventory = inspect_database_archive(archive, extract_to=cache)
        expected_database = {
            "archive": archive.name,
            "archive_sha256": sha256_file(archive),
            "archive_bytes": archive_metadata.st_size,
            "expanded_bytes": sum(item["bytes"] for item in inventory),
            "file_count": len(inventory),
            "files": inventory,
        }
        if scan["database"] != expected_database:
            raise ValueError("gateway vulnerability receipt database binding differs")
        if replay:
            replay_report = _docker_scan(
                cache=cache,
                sbom=sbom,
                offline=True,
                pull="never",
            )
            if cache_inventory(cache) != inventory:
                raise ValueError("verification replay mutated the retained Trivy database")
    report_path = scan_path.parent / scan["report"]["file"]
    report_bytes = read_bounded_regular_file(
        report_path,
        maximum_bytes=MAX_REPORT_BYTES,
        label="retained Trivy scan report",
    )
    report = parse_bounded_json_object(
        report_bytes,
        maximum_bytes=MAX_REPORT_BYTES,
        label="retained Trivy scan report",
    )
    validate_trivy_report(report)
    expected_report = {
        "file": report_path.name,
        "sha256": hashlib.sha256(report_bytes).hexdigest(),
        "bytes": len(report_bytes),
    }
    if canonical_json_bytes(report) != report_bytes or scan["report"] != expected_report:
        raise ValueError("gateway vulnerability receipt report binding differs")
    findings = project_findings(report)
    fixable, passed = evaluate_policy(findings)
    if (
        scan["findings"] != findings or scan["fixable_findings"] != fixable
        or scan["passed"] != passed or not passed
    ):
        raise ValueError("gateway vulnerability policy projection differs from its report")
    verify_phase_timing(scan["phase"])
    if replay:
        if replay_projection(replay_report) != replay_projection(report):
            raise ValueError("offline Trivy replay differs from the retained report")
    return scan


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sbom", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sbom = args.sbom if args.sbom.is_absolute() else ROOT / args.sbom
    receipt = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    output = args.output if args.output.is_absolute() else ROOT / args.output
    generate_scan_evidence(sbom=sbom, receipt_path=receipt, output=output)
    print("Gateway image vulnerability scan and retained offline replay passed.")


if __name__ == "__main__":
    main()
