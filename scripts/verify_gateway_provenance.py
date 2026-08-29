#!/usr/bin/env python3
"""Verify an independent gateway rebuild and dependency-free attestation inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, BinaryIO, Iterator


ARCHIVE_NAME = "gateway-image.oci.tar"
ARCHIVE_CHECKSUM_NAME = f"{ARCHIVE_NAME}.sha256"
SBOM_NAME = "gateway-image.sbom.cdx.json"
SCAN_NAME = "gateway-image.vulnerability-scan.json"
EVIDENCE_MANIFEST_NAME = "gateway-image-evidence-manifest.json"
MANIFEST_SUBJECTS = (
    ("build-context", "build-context.sha256"),
    ("oci-archive", ARCHIVE_NAME),
    ("oci-checksum", ARCHIVE_CHECKSUM_NAME),
    ("image-receipt", "image-receipt.json"),
    ("image-sbom", SBOM_NAME),
    ("image-sbom-checksum", "gateway-image.sbom.cdx.json.sha256"),
    ("trivy-database", "gateway-image.trivy-db.tar.gz"),
    ("trivy-database-checksum", "gateway-image.trivy-db.tar.gz.sha256"),
    ("trivy-report", "gateway-image.trivy-report.json"),
    ("grype-database", "gateway-node.grype-db.tar.zst"),
    ("grype-database-checksum", "gateway-node.grype-db.tar.zst.sha256"),
    ("node-actual-input", "gateway-node.actual.input.cdx.json"),
    ("node-actual-grype-report", "gateway-node.actual.grype.json"),
    ("node-actual-grype-cyclonedx-report", "gateway-node.actual.grype.cdx.json"),
    ("node-affected-input", "gateway-node.affected.input.cdx.json"),
    ("node-affected-grype-report", "gateway-node.affected.grype.json"),
    (
        "node-affected-grype-cyclonedx-report",
        "gateway-node.affected.grype.cdx.json",
    ),
    ("node-fixed-input", "gateway-node.fixed.input.cdx.json"),
    ("node-fixed-grype-report", "gateway-node.fixed.grype.json"),
    ("node-fixed-grype-cyclonedx-report", "gateway-node.fixed.grype.cdx.json"),
    ("runtime-library-donor-archive", "gateway-runtime-library-donor.oci.tar"),
    (
        "runtime-library-donor-trivy-report",
        "gateway-runtime-library-donor.trivy-report.json",
    ),
    ("vulnerability-scan", SCAN_NAME),
    ("container-acceptance", "container-acceptance.json"),
)
EXCLUDED_PRIVATE_GRYPE_DB = "gateway-node.grype-db.tar.zst"
PRODUCER_TRANSPORT_FILES = frozenset(
    {
        filename
        for _role, filename in MANIFEST_SUBJECTS
        if filename != EXCLUDED_PRIVATE_GRYPE_DB
    }
    | {EVIDENCE_MANIFEST_NAME}
)
MAX_ARCHIVE_BYTES = 768 * 1024 * 1024
MAX_SBOM_BYTES = 256 * 1024 * 1024
MAX_SCAN_BYTES = 32 * 1024 * 1024
MAX_MANIFEST_BYTES = 8 * 1024 * 1024
MAX_CHECKSUM_BYTES = 256
STREAM_CHUNK_BYTES = 1024 * 1024
COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
MANIFEST_DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")
UTC_TIMESTAMP_RE = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z\Z"
)
VERSION_RE = re.compile(
    r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z"
)
MAX_DATABASE_AGE_AT_SCAN = timedelta(days=3)
MAX_PROVENANCE_ASSESSMENT_AGE = timedelta(hours=2)
MAX_PROVENANCE_FUTURE_SKEW = timedelta(minutes=5)
SBOM_PROPERTY_NAMES = frozenset(
    {
        "gis-ai-go:image-manifest-digest",
        "gis-ai-go:image-receipt-sha256",
        "gis-ai-go:rootfs-inventory-sha256",
        "gis-ai-go:runtime-base-reference",
        "gis-ai-go:runtime-base-source-reference",
        "gis-ai-go:runtime-library-donor-reference",
        "gis-ai-go:runtime-library-source-reference",
        "gis-ai-go:scanner-image",
        "gis-ai-go:source-revision",
        "gis-ai-go:support-boundary",
        "gis-ai-go:ubi-eula-sha256",
    }
)


@dataclass(frozen=True)
class FileMeasurement:
    sha256: str
    bytes: int


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    ).encode()


def _strict_property_map(value: Any, *, label: str) -> dict[str, str]:
    if not isinstance(value, list):
        raise ValueError(f"{label} is not a list")
    properties: dict[str, str] = {}
    for item in value:
        if (
            not isinstance(item, dict)
            or set(item) != {"name", "value"}
            or not isinstance(item["name"], str)
            or not item["name"]
            or not isinstance(item["value"], str)
            or item["name"] in properties
        ):
            raise ValueError(f"{label} contains an invalid or duplicate property")
        properties[item["name"]] = item["value"]
    return properties


def _file_identity(metadata: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_nlink,
    )


@contextmanager
def opened_regular_file(
    path: Path, *, maximum_bytes: int, label: str
) -> Iterator[tuple[BinaryIO, os.stat_result]]:
    """Open one bounded, unlinked regular file without following symbolic links."""
    try:
        initial = path.lstat()
    except OSError as error:
        raise ValueError(f"{label} is unavailable") from error
    if (
        stat.S_ISLNK(initial.st_mode)
        or not stat.S_ISREG(initial.st_mode)
        or initial.st_nlink != 1
        or initial.st_size < 1
        or initial.st_size > maximum_bytes
    ):
        raise ValueError(f"{label} is not one bounded regular file")
    no_follow = getattr(os, "O_NOFOLLOW", None)
    if no_follow is None:
        raise ValueError(f"{label} cannot be opened without following links")
    descriptor = os.open(path, os.O_RDONLY | no_follow)
    stream: BinaryIO | None = None
    try:
        opened = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened.st_mode)
            or opened.st_nlink != 1
            or _file_identity(opened) != _file_identity(initial)
        ):
            raise ValueError(f"{label} changed while it was opened")
        stream = os.fdopen(descriptor, "rb", closefd=True)
        descriptor = -1
        yield stream, opened
        closed = os.fstat(stream.fileno())
        if _file_identity(closed) != _file_identity(opened):
            raise ValueError(f"{label} changed while it was read")
    finally:
        if stream is not None:
            stream.close()
        elif descriptor >= 0:
            os.close(descriptor)


def read_regular_file(path: Path, *, maximum_bytes: int, label: str) -> bytes:
    with opened_regular_file(path, maximum_bytes=maximum_bytes, label=label) as (
        stream,
        opened,
    ):
        raw = stream.read(maximum_bytes + 1)
        if len(raw) != opened.st_size or len(raw) > maximum_bytes:
            raise ValueError(f"{label} changed or exceeded its byte bound while reading")
        return raw


def measure_regular_file(
    path: Path, *, maximum_bytes: int, label: str
) -> FileMeasurement:
    digest = hashlib.sha256()
    size = 0
    with opened_regular_file(path, maximum_bytes=maximum_bytes, label=label) as (
        stream,
        opened,
    ):
        while True:
            chunk = stream.read(STREAM_CHUNK_BYTES)
            if not chunk:
                break
            size += len(chunk)
            if size > maximum_bytes:
                raise ValueError(f"{label} exceeded its byte bound while reading")
            digest.update(chunk)
        if size != opened.st_size:
            raise ValueError(f"{label} changed while it was measured")
    return FileMeasurement(digest.hexdigest(), size)


def compare_regular_files(
    first: Path,
    second: Path,
    *,
    maximum_bytes: int,
    first_label: str,
    second_label: str,
) -> tuple[FileMeasurement, FileMeasurement, bool]:
    first_digest = hashlib.sha256()
    second_digest = hashlib.sha256()
    first_size = 0
    second_size = 0
    identical = True
    with opened_regular_file(
        first, maximum_bytes=maximum_bytes, label=first_label
    ) as (first_stream, first_opened), opened_regular_file(
        second, maximum_bytes=maximum_bytes, label=second_label
    ) as (second_stream, second_opened):
        while True:
            first_chunk = first_stream.read(STREAM_CHUNK_BYTES)
            second_chunk = second_stream.read(STREAM_CHUNK_BYTES)
            if not first_chunk and not second_chunk:
                break
            first_size += len(first_chunk)
            second_size += len(second_chunk)
            if first_size > maximum_bytes or second_size > maximum_bytes:
                raise ValueError("gateway rebuild comparison exceeded its byte bound")
            first_digest.update(first_chunk)
            second_digest.update(second_chunk)
            if first_chunk != second_chunk:
                identical = False
        if first_size != first_opened.st_size or second_size != second_opened.st_size:
            raise ValueError("gateway rebuild input changed while it was compared")
    return (
        FileMeasurement(first_digest.hexdigest(), first_size),
        FileMeasurement(second_digest.hexdigest(), second_size),
        identical,
    )


def parse_checksum(path: Path, *, filename: str, label: str) -> str:
    raw = read_regular_file(
        path, maximum_bytes=MAX_CHECKSUM_BYTES, label=label
    )
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise ValueError(f"{label} is not ASCII") from error
    match = re.fullmatch(rf"([0-9a-f]{{64}})  {re.escape(filename)}\n", text)
    if match is None:
        raise ValueError(f"{label} is not one canonical SHA-256 record")
    return match.group(1)


def verify_rebuild(
    *,
    accepted_archive: Path,
    accepted_checksum: Path,
    independent_archive: Path,
    independent_checksum: Path,
) -> FileMeasurement:
    """Require two separately produced canonical archives to be byte-identical."""
    accepted, independent, identical = compare_regular_files(
        accepted_archive,
        independent_archive,
        maximum_bytes=MAX_ARCHIVE_BYTES,
        first_label="accepted gateway OCI archive",
        second_label="independently rebuilt gateway OCI archive",
    )
    accepted_declared = parse_checksum(
        accepted_checksum,
        filename=accepted_archive.name,
        label="accepted gateway OCI checksum",
    )
    independent_declared = parse_checksum(
        independent_checksum,
        filename=independent_archive.name,
        label="independent gateway OCI checksum",
    )
    if accepted_declared != accepted.sha256:
        raise ValueError("accepted gateway OCI checksum differs from its archive")
    if independent_declared != independent.sha256:
        raise ValueError("independent gateway OCI checksum differs from its archive")
    if (
        not identical
        or accepted.bytes != independent.bytes
        or accepted.sha256 != independent.sha256
    ):
        raise ValueError("independent gateway OCI rebuild differs from accepted bytes")
    return accepted


def load_canonical_json_object(
    path: Path, *, maximum_bytes: int, label: str
) -> dict[str, Any]:
    raw = read_regular_file(path, maximum_bytes=maximum_bytes, label=label)

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{label} contains a duplicate member: {key}")
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
    if not isinstance(value, dict) or canonical_json_bytes(value) != raw:
        raise ValueError(f"{label} is not one canonical JSON object")
    return value


def _subject_by_file(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    subjects = manifest.get("subjects")
    if not isinstance(subjects, list) or not subjects:
        raise ValueError("gateway evidence manifest lacks its subject inventory")
    by_file: dict[str, dict[str, Any]] = {}
    identities: list[tuple[str, str]] = []
    for subject in subjects:
        if not isinstance(subject, dict) or set(subject) != {
            "role",
            "file",
            "sha256",
            "bytes",
        }:
            raise ValueError("gateway evidence manifest contains an invalid subject")
        filename = subject.get("file")
        if not isinstance(filename, str) or filename in by_file:
            raise ValueError("gateway evidence manifest repeats a subject file")
        role = subject.get("role")
        if not isinstance(role, str):
            raise ValueError("gateway evidence manifest has an invalid subject role")
        identities.append((role, filename))
        by_file[filename] = subject
    if tuple(identities) != MANIFEST_SUBJECTS:
        raise ValueError("gateway evidence manifest subject contract differs")
    return by_file


def parse_utc_timestamp(value: Any, *, label: str) -> datetime:
    if not isinstance(value, str) or UTC_TIMESTAMP_RE.fullmatch(value) is None:
        raise ValueError(f"{label} is not one canonical UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise ValueError(f"{label} is not a valid UTC timestamp") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise ValueError(f"{label} is not UTC")
    return parsed.astimezone(UTC)


def _project_age_seconds(later: datetime, earlier: datetime, *, label: str) -> int:
    age = later - earlier
    if age < timedelta(0) or age > MAX_DATABASE_AGE_AT_SCAN:
        raise ValueError(f"{label} is outside the current database window")
    return round(age.total_seconds())


def _verify_scan_freshness(
    scan: dict[str, Any],
    *,
    manifest: dict[str, Any],
    archive: FileMeasurement,
    sbom: FileMeasurement,
    expected_source_commit: str,
    verified_at: datetime,
) -> None:
    """Use only the privileged runner clock to enforce the retained scan window."""
    image = scan.get("image")
    scan_sbom = scan.get("sbom")
    node_runtime = scan.get("node_runtime")
    database = node_runtime.get("database") if isinstance(node_runtime, dict) else None
    provider = database.get("provider") if isinstance(database, dict) else None
    phase = scan.get("phase")
    if (
        scan.get("schema") != "gis-ai-go.gateway-image-vulnerability-scan.v3"
        or scan.get("classification") != "repository-only-unregistered-candidate"
        or scan.get("source_revision") != expected_source_commit
        or scan.get("image_manifest_digest")
        != manifest["image"]["manifest_digest"]
        or scan.get("passed") is not True
        or scan.get("claims")
        != {
            "public_deployment": False,
            "production_activation": False,
            "live_provider_call": False,
        }
        or not isinstance(image, dict)
        or image.get("file") != ARCHIVE_NAME
        or image.get("sha256") != archive.sha256
        or image.get("bytes") != archive.bytes
        or scan_sbom
        != {
            "file": SBOM_NAME,
            "sha256": sbom.sha256,
            "bytes": sbom.bytes,
        }
        or not isinstance(database, dict)
        or database.get("valid") is not True
        or database.get("load_mode") != "manual-import"
        or not isinstance(provider, dict)
        or provider.get("name") != "nvd"
        or not isinstance(phase, dict)
    ):
        raise ValueError("gateway vulnerability scan has an invalid attestation identity")

    if verified_at.tzinfo is None or verified_at.utcoffset() != timedelta(0):
        raise ValueError("gateway provenance verifier clock is not UTC")
    verified_at = verified_at.astimezone(UTC)
    built = parse_utc_timestamp(
        database.get("built"), label="gateway Grype database build"
    )
    captured = parse_utc_timestamp(
        provider.get("captured"), label="gateway NVD provider capture"
    )
    assessed = parse_utc_timestamp(
        database.get("assessed_at"), label="gateway Grype assessment"
    )
    phase_started = parse_utc_timestamp(
        phase.get("started_at"), label="gateway vulnerability phase start"
    )
    phase_completed = parse_utc_timestamp(
        phase.get("completed_at"), label="gateway vulnerability phase completion"
    )
    if not captured <= built <= assessed or not phase_started <= assessed <= phase_completed:
        raise ValueError("gateway vulnerability freshness timestamps are not ordered")
    database_age = _project_age_seconds(
        assessed, built, label="gateway Grype database"
    )
    provider_age = _project_age_seconds(
        assessed, captured, label="gateway NVD provider"
    )
    if (
        type(database.get("age_seconds")) is not int
        or database["age_seconds"] != database_age
        or type(database.get("provider_age_seconds")) is not int
        or database["provider_age_seconds"] != provider_age
    ):
        raise ValueError("gateway vulnerability freshness projections differ")
    assessment_age = verified_at - assessed
    if assessment_age < -MAX_PROVENANCE_FUTURE_SKEW:
        raise ValueError("gateway Grype assessment is ahead of the verifier clock")
    if assessment_age > MAX_PROVENANCE_ASSESSMENT_AGE:
        raise ValueError("gateway Grype assessment is too old for OIDC provenance")


def verify_attestation_inputs(
    *,
    directory: Path,
    expected_source_commit: str,
    verified_at: datetime | None = None,
) -> dict[str, FileMeasurement]:
    """Verify the dependency-free hand-off consumed by the OIDC attestation job."""
    if COMMIT_RE.fullmatch(expected_source_commit) is None:
        raise ValueError("expected gateway source commit is invalid")
    metadata = directory.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError("gateway attestation input is not one real directory")
    entries = list(directory.iterdir())
    names = {entry.name for entry in entries}
    if names != PRODUCER_TRANSPORT_FILES:
        raise ValueError("gateway attestation input file set is not closed")
    for entry in entries:
        entry_metadata = entry.lstat()
        if (
            stat.S_ISLNK(entry_metadata.st_mode)
            or not stat.S_ISREG(entry_metadata.st_mode)
            or entry_metadata.st_nlink != 1
            or entry_metadata.st_size < 1
            or entry_metadata.st_size > MAX_ARCHIVE_BYTES
        ):
            raise ValueError("gateway attestation input contains an invalid file")

    manifest = load_canonical_json_object(
        directory / EVIDENCE_MANIFEST_NAME,
        maximum_bytes=MAX_MANIFEST_BYTES,
        label="gateway evidence manifest",
    )
    source = manifest.get("source")
    image = manifest.get("image")
    if (
        manifest.get("schema") != "gis-ai-go.gateway-image-evidence-manifest.v2"
        or manifest.get("classification") != "repository-only-unregistered-candidate"
        or manifest.get("passed") is not True
        or not isinstance(source, dict)
        or set(source) != {"revision", "version", "clean"}
        or source.get("revision") != expected_source_commit
        or VERSION_RE.fullmatch(str(source.get("version"))) is None
        or source.get("clean") is not True
        or not isinstance(image, dict)
        or set(image) != {"manifest_digest", "platform"}
        or MANIFEST_DIGEST_RE.fullmatch(str(image.get("manifest_digest"))) is None
        or image.get("platform") != "linux/amd64"
    ):
        raise ValueError("gateway evidence manifest has an invalid attestation identity")

    subjects = _subject_by_file(manifest)
    measurements: dict[str, FileMeasurement] = {}
    for filename, role, maximum in (
        (ARCHIVE_NAME, "oci-archive", MAX_ARCHIVE_BYTES),
        (SBOM_NAME, "image-sbom", MAX_SBOM_BYTES),
        (SCAN_NAME, "vulnerability-scan", MAX_SCAN_BYTES),
    ):
        measurement = measure_regular_file(
            directory / filename,
            maximum_bytes=maximum,
            label=f"gateway attestation subject {filename}",
        )
        subject = subjects.get(filename)
        if subject != {
            "role": role,
            "file": filename,
            "sha256": measurement.sha256,
            "bytes": measurement.bytes,
        }:
            raise ValueError(f"gateway attestation subject differs from manifest: {filename}")
        measurements[filename] = measurement

    archive_checksum = parse_checksum(
        directory / ARCHIVE_CHECKSUM_NAME,
        filename=ARCHIVE_NAME,
        label="gateway attestation OCI checksum",
    )
    if archive_checksum != measurements[ARCHIVE_NAME].sha256:
        raise ValueError("gateway attestation OCI checksum differs from its archive")

    sbom = load_canonical_json_object(
        directory / SBOM_NAME,
        maximum_bytes=MAX_SBOM_BYTES,
        label="gateway image SBOM",
    )
    metadata_document = sbom.get("metadata")
    component = (
        metadata_document.get("component")
        if isinstance(metadata_document, dict)
        else None
    )
    property_map = _strict_property_map(
        component.get("properties") if isinstance(component, dict) else None,
        label="gateway image SBOM properties",
    )
    if (
        sbom.get("bomFormat") != "CycloneDX"
        or not isinstance(component, dict)
        or component.get("bom-ref") != image["manifest_digest"]
        or set(property_map) != SBOM_PROPERTY_NAMES
        or property_map.get("gis-ai-go:source-revision") != expected_source_commit
        or property_map.get("gis-ai-go:image-manifest-digest")
        != image["manifest_digest"]
    ):
        raise ValueError("gateway image SBOM differs from the attestation identity")
    scan = load_canonical_json_object(
        directory / SCAN_NAME,
        maximum_bytes=MAX_SCAN_BYTES,
        label="gateway vulnerability scan",
    )
    _verify_scan_freshness(
        scan,
        manifest=manifest,
        archive=measurements[ARCHIVE_NAME],
        sbom=measurements[SBOM_NAME],
        expected_source_commit=expected_source_commit,
        verified_at=verified_at or datetime.now(UTC),
    )
    checksum_measurement = measure_regular_file(
        directory / ARCHIVE_CHECKSUM_NAME,
        maximum_bytes=MAX_CHECKSUM_BYTES,
        label="gateway attestation OCI checksum",
    )
    if subjects.get(ARCHIVE_CHECKSUM_NAME) != {
        "role": "oci-checksum",
        "file": ARCHIVE_CHECKSUM_NAME,
        "sha256": checksum_measurement.sha256,
        "bytes": checksum_measurement.bytes,
    }:
        raise ValueError("gateway attestation OCI checksum differs from manifest")
    measurements[ARCHIVE_CHECKSUM_NAME] = checksum_measurement
    measurements[EVIDENCE_MANIFEST_NAME] = measure_regular_file(
        directory / EVIDENCE_MANIFEST_NAME,
        maximum_bytes=MAX_MANIFEST_BYTES,
        label="gateway evidence manifest",
    )
    return measurements


def main() -> None:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    compare = commands.add_parser("compare-rebuild")
    compare.add_argument("--accepted-archive", type=Path, required=True)
    compare.add_argument("--accepted-checksum", type=Path, required=True)
    compare.add_argument("--independent-archive", type=Path, required=True)
    compare.add_argument("--independent-checksum", type=Path, required=True)
    attestation = commands.add_parser("verify-attestation-inputs")
    attestation.add_argument("--directory", type=Path, required=True)
    attestation.add_argument("--expected-source-commit", required=True)
    args = parser.parse_args()

    if args.command == "compare-rebuild":
        measurement = verify_rebuild(
            accepted_archive=args.accepted_archive,
            accepted_checksum=args.accepted_checksum,
            independent_archive=args.independent_archive,
            independent_checksum=args.independent_checksum,
        )
        print(
            "Independent gateway OCI rebuild is byte-identical at SHA-256 "
            f"{measurement.sha256}."
        )
        return
    measurements = verify_attestation_inputs(
        directory=args.directory,
        expected_source_commit=args.expected_source_commit,
    )
    print(
        "Verified dependency-free gateway attestation inputs for "
        f"{args.expected_source_commit} ({len(measurements)} subjects)."
    )


if __name__ == "__main__":
    main()
