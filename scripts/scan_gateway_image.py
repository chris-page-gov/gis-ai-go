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
from urllib.parse import parse_qs, unquote

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
    LIBSTDCXX_PATH,
    LIBSTDCXX_RPM_NAME,
    LIBSTDCXX_RPM_PURL,
    LIBSTDCXX_RPM_VERSION,
    LIBSTDCXX_SHA256,
    MAX_LAYER_PATH_BYTES,
    MAX_LAYER_PATH_COMPONENTS,
    MAX_LAYER_PATH_COMPONENT_BYTES,
    MAX_OCI_BYTES,
    ROOT,
    TRIVY_REFERENCE,
    UBI_RUNTIME_LIBRARY_DONOR_DIGEST,
    UBI_RUNTIME_LIBRARY_DONOR_REFERENCE,
    assert_no_private_json,
    assert_no_private_text,
    canonical_json_bytes,
    contains_diagnostic_private_path,
    parse_checksum,
    prohibited_text_reason,
    sha256_file,
)
from node_runtime_advisory import generate_node_advisory, verify_node_advisory

BLOCKED_SEVERITIES = frozenset({"HIGH", "CRITICAL"})
TRIVY_VERSION = "0.74.0"
SCAN_SCHEMA = ROOT / "schemas" / "gateway-image-vulnerability-scan.schema.json"
DB_ARCHIVE_NAME = "gateway-image.trivy-db.tar.gz"
DB_CHECKSUM_NAME = f"{DB_ARCHIVE_NAME}.sha256"
REPORT_NAME = "gateway-image.trivy-report.json"
DONOR_ARCHIVE_NAME = "gateway-runtime-library-donor.oci.tar"
DONOR_REPORT_NAME = "gateway-runtime-library-donor.trivy-report.json"
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
TRIVY_OCI_PATH = "/input/gateway-image.oci.tar"
TRIVY_DONOR_PATH = "/input/gateway-runtime-library-donor.oci.tar"
MAX_OCI_FILES = 20_000
MAX_JSON_BYTES = 4 * 1024 * 1024
OCI_INDEX_MEDIA_TYPE = "application/vnd.oci.image.index.v1+json"
OCI_MANIFEST_MEDIA_TYPE = "application/vnd.oci.image.manifest.v1+json"
OCI_CONFIG_MEDIA_TYPE = "application/vnd.oci.image.config.v1+json"
OCI_LAYER_MEDIA_TYPE = "application/vnd.oci.image.layer.v1.tar+gzip"
_SHA256_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
_RPM_PURL = re.compile(r"pkg:rpm/redhat/([^@?]+)@([^?]+)\?(.+)\Z")
_NPM_PURL = re.compile(r"pkg:npm/(.+)@([^@?]+)(?:\?.*)?\Z")

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
    try:
        encoded = value.encode("utf-8", errors="strict")
    except UnicodeEncodeError as error:
        raise ValueError(f"non-UTF-8 Trivy evidence path: {value!r}") from error
    if len(encoded) > MAX_LAYER_PATH_BYTES:
        raise ValueError(f"Trivy evidence path exceeds its byte bound: {value!r}")
    logical = PurePosixPath(value)
    if (
        not value
        or value.startswith("/")
        or "\\" in value
        or "\0" in value
        or logical.is_absolute()
        or any(part in {"", ".", ".."} for part in logical.parts)
        or len(logical.parts) > MAX_LAYER_PATH_COMPONENTS
        or any(
            len(part.encode("utf-8")) > MAX_LAYER_PATH_COMPONENT_BYTES
            for part in logical.parts
        )
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


def _archive_json_member(
    archive: tarfile.TarFile,
    members: dict[str, tarfile.TarInfo],
    name: str,
) -> dict[str, Any]:
    member = members.get(name)
    if member is None or not member.isreg() or member.size > MAX_JSON_BYTES:
        raise ValueError(f"donor OCI JSON member is missing or over its bound: {name}")
    source = archive.extractfile(member)
    if source is None:
        raise ValueError(f"donor OCI JSON member is unavailable: {name}")
    try:
        document = json.loads(source.read(MAX_JSON_BYTES + 1))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"donor OCI JSON member is invalid: {name}") from error
    if not isinstance(document, dict):
        raise ValueError(f"donor OCI JSON member must be an object: {name}")
    return document


def _verify_donor_blob(
    archive: tarfile.TarFile,
    members: dict[str, tarfile.TarInfo],
    descriptor: Any,
    *,
    media_type: str,
    maximum: int,
    optional_keys: frozenset[str] = frozenset(),
) -> tuple[str, str]:
    if (
        not isinstance(descriptor, dict)
        or not {"mediaType", "digest", "size"}.issubset(descriptor)
        or not set(descriptor).issubset(
            {"mediaType", "digest", "size"} | optional_keys
        )
        or descriptor.get("mediaType") != media_type
    ):
        raise ValueError("donor OCI descriptor differs from the closed contract")
    digest = descriptor.get("digest")
    size = descriptor.get("size")
    if (
        not isinstance(digest, str)
        or _SHA256_DIGEST.fullmatch(digest) is None
        or type(size) is not int
        or size < 1
        or size > maximum
    ):
        raise ValueError("donor OCI descriptor digest or size is invalid")
    name = f"blobs/sha256/{digest.removeprefix('sha256:')}"
    member = members.get(name)
    if member is None or not member.isreg() or member.size != size:
        raise ValueError("donor OCI descriptor blob is missing or has a different size")
    source = archive.extractfile(member)
    if source is None:
        raise ValueError("donor OCI descriptor blob is unavailable")
    realised = hashlib.sha256()
    while chunk := source.read(1024 * 1024):
        realised.update(chunk)
    if realised.hexdigest() != digest.removeprefix("sha256:"):
        raise ValueError("donor OCI descriptor blob digest differs")
    return digest, name


def inspect_donor_archive(path: Path) -> dict[str, Any]:
    """Verify and bind the retained Docker-save archive for the pinned donor."""
    metadata = path.lstat()
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISREG(metadata.st_mode)
        or metadata.st_size < 1
        or metadata.st_size > MAX_OCI_BYTES
    ):
        raise ValueError("runtime-library donor archive is invalid or over its bound")
    with tarfile.open(path, "r:") as archive:
        members: dict[str, tarfile.TarInfo] = {}
        total = 0
        for member in archive:
            if len(members) >= MAX_OCI_FILES:
                raise ValueError("runtime-library donor archive exceeds its file bound")
            name = _safe_relative_path(member.name)
            if name != member.name or name in members:
                raise ValueError("runtime-library donor archive path inventory is ambiguous")
            if not (member.isdir() or member.isreg()):
                raise ValueError("runtime-library donor archive contains a special member")
            if (
                member.uid != 0
                or member.gid != 0
                or member.uname != ""
                or member.gname != ""
                or member.mtime != 0
                or member.pax_headers
            ):
                raise ValueError("runtime-library donor archive metadata is not canonical")
            expected_mode = 0o755 if member.isdir() else (
                0o644 if name in {"index.json", "manifest.json"} else 0o444
            )
            if member.mode != expected_mode:
                raise ValueError("runtime-library donor archive mode is not canonical")
            if member.isreg():
                total += member.size
                if total > MAX_OCI_BYTES:
                    raise ValueError("runtime-library donor archive exceeds its byte bound")
            members[name] = member
        directories = {name for name, member in members.items() if member.isdir()}
        files = {name for name, member in members.items() if member.isreg()}
        if directories != {"blobs", "blobs/sha256"}:
            raise ValueError("runtime-library donor directory inventory is not closed")
        if not {"index.json", "manifest.json", "oci-layout"}.issubset(files):
            raise ValueError("runtime-library donor archive is incomplete")
        layout = _archive_json_member(archive, members, "oci-layout")
        if layout != {"imageLayoutVersion": "1.0.0"}:
            raise ValueError("runtime-library donor OCI layout is invalid")
        index = _archive_json_member(archive, members, "index.json")
        descriptors = index.get("manifests")
        if (
            set(index) != {"schemaVersion", "mediaType", "manifests"}
            or index.get("schemaVersion") != 2
            or index.get("mediaType") != OCI_INDEX_MEDIA_TYPE
            or not isinstance(descriptors, list)
            or len(descriptors) != 1
        ):
            raise ValueError("runtime-library donor index is outside the closed contract")
        descriptor = descriptors[0]
        manifest_digest, manifest_name = _verify_donor_blob(
            archive,
            members,
            descriptor,
            media_type=OCI_MANIFEST_MEDIA_TYPE,
            maximum=MAX_JSON_BYTES,
            optional_keys=frozenset({"annotations"}),
        )
        if (
            manifest_digest != UBI_RUNTIME_LIBRARY_DONOR_DIGEST
            or descriptor.get("annotations")
            != {
                "containerd.io/distribution.source.registry.access.redhat.com":
                    "ubi10/nodejs-24-minimal"
            }
        ):
            raise ValueError("runtime-library donor archive differs from the pinned image")
        manifest = _archive_json_member(archive, members, manifest_name)
        layers = manifest.get("layers")
        if (
            manifest.get("schemaVersion") != 2
            or manifest.get("mediaType") != OCI_MANIFEST_MEDIA_TYPE
            or not isinstance(layers, list)
            or not layers
            or len(layers) > 64
            or not set(manifest).issubset(
                {"schemaVersion", "mediaType", "config", "layers", "annotations"}
            )
        ):
            raise ValueError("runtime-library donor manifest is invalid")
        config_digest, config_name = _verify_donor_blob(
            archive,
            members,
            manifest.get("config"),
            media_type=OCI_CONFIG_MEDIA_TYPE,
            maximum=MAX_JSON_BYTES,
        )
        layer_digests: list[str] = []
        layer_names: list[str] = []
        for layer in layers:
            digest, name = _verify_donor_blob(
                archive,
                members,
                layer,
                media_type=OCI_LAYER_MEDIA_TYPE,
                maximum=MAX_OCI_BYTES,
            )
            layer_digests.append(digest)
            layer_names.append(name)
        config = _archive_json_member(archive, members, config_name)
        rootfs = config.get("rootfs")
        diff_ids = rootfs.get("diff_ids") if isinstance(rootfs, dict) else None
        if (
            config.get("architecture") != "amd64"
            or config.get("os") != "linux"
            or not isinstance(rootfs, dict)
            or set(rootfs) != {"type", "diff_ids"}
            or rootfs.get("type") != "layers"
            or not isinstance(diff_ids, list)
            or len(diff_ids) != len(layer_digests)
            or any(
                not isinstance(item, str) or _SHA256_DIGEST.fullmatch(item) is None
                for item in diff_ids
            )
            or len(set(diff_ids)) != len(diff_ids)
        ):
            raise ValueError("runtime-library donor configuration identity is invalid")
        manifest_member = members["manifest.json"]
        source = archive.extractfile(manifest_member)
        if source is None or manifest_member.size > MAX_JSON_BYTES:
            raise ValueError("runtime-library donor Docker manifest is unavailable")
        try:
            docker_manifest = json.loads(source.read(MAX_JSON_BYTES + 1))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("runtime-library donor Docker manifest is invalid") from error
        if docker_manifest != [
            {"Config": config_name, "RepoTags": None, "Layers": layer_names}
        ]:
            raise ValueError("runtime-library donor Docker manifest differs from its OCI graph")
        reachable = {manifest_name, config_name, *layer_names}
        if files != {"index.json", "manifest.json", "oci-layout"} | reachable:
            raise ValueError("runtime-library donor archive has unreachable content")
        return {
            "file": path.name,
            "sha256": sha256_file(path),
            "bytes": metadata.st_size,
            "reference": UBI_RUNTIME_LIBRARY_DONOR_REFERENCE,
            "manifest_digest": manifest_digest,
            "config_digest": config_digest,
            "layer_digests": layer_digests,
            "rootfs_diff_ids": diff_ids,
            "platform": "linux/amd64",
        }


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


def _normalise_trivy_package(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Trivy report contains an invalid package inventory entry")
    name = _bounded_text(value.get("Name"), label="package name", maximum=512)
    version = _bounded_text(value.get("Version"), label="package version", maximum=512)
    identifier = value.get("Identifier")
    if not isinstance(identifier, dict):
        raise ValueError("Trivy report package lacks its package URL identity")
    purl = _bounded_text(identifier.get("PURL"), label="package URL", maximum=2_048)
    package: dict[str, Any] = {
        "Name": name,
        "Version": version,
        "Identifier": {"PURL": purl},
    }
    for key in ("Release", "Arch"):
        item = value.get(key)
        if item is not None:
            package[key] = _bounded_text(
                item, label=f"package {key.lower()}", maximum=512
            )
    return package


def _normalise_trivy_vulnerability(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Trivy report contains an invalid vulnerability")
    severity = value.get("Severity")
    if severity not in BLOCKED_SEVERITIES:
        raise ValueError("Trivy report contains a finding outside the requested severities")
    fixed = value.get("FixedVersion")
    if fixed is None or fixed == "":
        fixed_version = ""
    else:
        fixed_version = _bounded_text(
            fixed, label="fixed version", maximum=1_024
        )
    return {
        "VulnerabilityID": _bounded_text(
            value.get("VulnerabilityID"), label="vulnerability ID", maximum=256
        ),
        "PkgName": _bounded_text(
            value.get("PkgName"), label="vulnerability package", maximum=512
        ),
        "InstalledVersion": _bounded_text(
            value.get("InstalledVersion"),
            label="installed version",
            maximum=512,
        ),
        "FixedVersion": fixed_version,
        "Severity": severity,
    }


def normalise_trivy_report(
    document: dict[str, Any], *, artifact_path: str = TRIVY_OCI_PATH
) -> dict[str, Any]:
    """Retain one deterministic, privacy-safe projection of an exact OCI scan."""
    validate_trivy_report(document)
    artifact_id = document.get("ArtifactID")
    metadata = document.get("Metadata")
    if (
        document.get("SchemaVersion") != 2
        or not isinstance(artifact_id, str)
        or re.fullmatch(r"sha256:[0-9a-f]{64}", artifact_id) is None
        or document.get("ArtifactName") != artifact_path
        or document.get("ArtifactType") != "container_image"
        or not isinstance(metadata, dict)
    ):
        raise ValueError("Trivy report is not bound to the exact OCI archive input")
    image_id = metadata.get("ImageID")
    diff_ids = metadata.get("DiffIDs")
    operating_system = metadata.get("OS")
    if (
        not isinstance(image_id, str)
        or re.fullmatch(r"sha256:[0-9a-f]{64}", image_id) is None
        or not isinstance(diff_ids, list)
        or not diff_ids
        or len(diff_ids) > 64
        or any(
            not isinstance(item, str)
            or re.fullmatch(r"sha256:[0-9a-f]{64}", item) is None
            for item in diff_ids
        )
        or len(set(diff_ids)) != len(diff_ids)
        or operating_system != {"Family": "redhat", "Name": "10.2"}
    ):
        raise ValueError("Trivy report OCI metadata differs from the reviewed image")
    results: list[dict[str, Any]] = []
    for result in document["Results"]:
        if not isinstance(result, dict):
            raise ValueError("Trivy report contains an invalid result target")
        packages = result.get("Packages")
        if not isinstance(packages, list) or not packages:
            raise ValueError("Trivy report result lacks its package inventory")
        vulnerabilities = result.get("Vulnerabilities") or []
        if not isinstance(vulnerabilities, list):
            raise ValueError("Trivy report result has an invalid vulnerability list")
        results.append(
            {
                "Target": _bounded_text(
                    result.get("Target"), label="target", maximum=1_024
                ),
                "Class": _bounded_text(
                    result.get("Class"), label="target class", maximum=128
                ),
                "Type": _bounded_text(
                    result.get("Type"), label="target type", maximum=128
                ),
                "Packages": sorted(
                    (_normalise_trivy_package(item) for item in packages),
                    key=lambda item: (
                        item["Name"],
                        item["Version"],
                        item.get("Release", ""),
                        item.get("Arch", ""),
                        item["Identifier"]["PURL"],
                    ),
                ),
                "Vulnerabilities": sorted(
                    (_normalise_trivy_vulnerability(item) for item in vulnerabilities),
                    key=lambda item: (
                        item["Severity"],
                        item["VulnerabilityID"],
                        item["PkgName"],
                        item["InstalledVersion"],
                        item["FixedVersion"],
                    ),
                ),
            }
        )
    return {
        "SchemaVersion": 2,
        "Trivy": {"Version": TRIVY_VERSION},
        "ArtifactID": artifact_id,
        "ArtifactName": artifact_path,
        "ArtifactType": "container_image",
        "Metadata": {
            "OS": operating_system,
            "ImageID": image_id,
            "DiffIDs": diff_ids,
        },
        "Results": sorted(
            results,
            key=lambda item: (item["Class"], item["Type"], item["Target"]),
        ),
    }


def _parse_rpm_purl(value: str, *, expected_distro: str) -> tuple[str, str, str | None]:
    match = _RPM_PURL.fullmatch(value)
    if match is None:
        raise ValueError("RPM package inventory contains an invalid Red Hat package URL")
    query = parse_qs(match.group(3), keep_blank_values=True, strict_parsing=True)
    if query.get("distro") != [expected_distro] or any(
        len(items) != 1 for items in query.values()
    ):
        raise ValueError("RPM package URL differs from the expected Red Hat distribution")
    arch = query.get("arch", [None])[0]
    return unquote(match.group(1)), unquote(match.group(2)), arch


def _parse_npm_purl(value: str) -> tuple[str, str]:
    match = _NPM_PURL.fullmatch(value)
    if match is None:
        raise ValueError("Node package inventory contains an invalid package URL")
    return unquote(match.group(1)), unquote(match.group(2))


def project_coverage(
    document: dict[str, Any],
    donor_document: dict[str, Any],
    sbom: dict[str, Any],
    receipt: dict[str, Any],
    donor: dict[str, Any],
) -> dict[str, Any]:
    """Fail closed unless Trivy covers the exact SBOM OS and language inventories."""
    report = normalise_trivy_report(document)
    metadata = report["Metadata"]
    if (
        metadata["ImageID"] != receipt["image"]["config_digest"]
        or metadata["DiffIDs"] != receipt["image"]["rootfs_diff_ids"]
    ):
        raise ValueError("Trivy report differs from the exact OCI configuration or layers")
    results = report["Results"]
    os_results = [item for item in results if item["Class"] == "os-pkgs"]
    language_results = [item for item in results if item["Class"] == "lang-pkgs"]
    if (
        len(results) != 2
        or len(os_results) != 1
        or len(language_results) != 1
        or os_results[0]["Type"] != "redhat"
        or os_results[0]["Target"] != f"{TRIVY_OCI_PATH} (redhat 10.2)"
        or language_results[0]["Type"] != "node-pkg"
        or language_results[0]["Target"] != "Node.js"
    ):
        raise ValueError("Trivy report OS and language target inventory is not closed")

    components = sbom.get("components")
    if not isinstance(components, list) or not components:
        raise ValueError("gateway SBOM lacks its package inventory")
    expected_os: dict[tuple[str, str, str], str] = {}
    expected_metadata_rpms: dict[tuple[str, str], str] = {}
    expected_language: dict[str, tuple[str, str]] = {}
    donor_component: dict[str, Any] | None = None
    for component in components:
        if not isinstance(component, dict):
            continue
        purl = component.get("purl")
        if not isinstance(purl, str):
            continue
        if purl.startswith("pkg:rpm/redhat/"):
            name, version, arch = _parse_rpm_purl(purl, expected_distro="rhel-10.2")
            if component.get("name") != name or component.get("version") != version:
                raise ValueError("gateway SBOM RPM identity fields disagree")
            if purl == LIBSTDCXX_RPM_PURL:
                if donor_component is not None:
                    raise ValueError("gateway SBOM duplicates the donor libstdc++ identity")
                donor_component = component
            elif name == "gpg-pubkey":
                if arch is not None:
                    raise ValueError("gateway SBOM signing-key metadata has an unexpected arch")
                identity = (name, version)
                if identity in expected_metadata_rpms:
                    raise ValueError("gateway SBOM duplicates signing-key RPM metadata")
                expected_metadata_rpms[identity] = purl
            else:
                if arch is None:
                    raise ValueError("gateway SBOM runtime RPM lacks its architecture")
                identity = (name, version, arch)
                if identity in expected_os:
                    raise ValueError("gateway SBOM duplicates one runtime RPM identity")
                expected_os[identity] = purl
        elif purl.startswith("pkg:npm/"):
            name, version = _parse_npm_purl(purl)
            if component.get("name") != name or component.get("version") != version:
                raise ValueError("gateway SBOM Node package identity fields disagree")
            if purl in expected_language:
                raise ValueError("gateway SBOM duplicates one Node package identity")
            expected_language[purl] = (name, version)

    if donor_component is None:
        raise ValueError("gateway SBOM lacks the exact donor libstdc++ RPM identity")
    receipt_donor = receipt["build"]["runtime_composition"]["runtime_library_donor"]
    if receipt_donor.get("package") != {
        "name": LIBSTDCXX_RPM_NAME,
        "version": LIBSTDCXX_RPM_VERSION,
        "purl": LIBSTDCXX_RPM_PURL,
    }:
        raise ValueError("gateway receipt lacks the exact donor libstdc++ RPM identity")
    donor_hashes = donor_component.get("hashes")
    donor_properties = donor_component.get("properties")
    if (
        not isinstance(donor_hashes, list)
        or {item.get("content") for item in donor_hashes if isinstance(item, dict)}
        != {LIBSTDCXX_SHA256}
        or not isinstance(donor_properties, list)
        or {
            item.get("name"): item.get("value")
            for item in donor_properties
            if isinstance(item, dict)
        }.get("gis-ai-go:runtime-file-path")
        != LIBSTDCXX_PATH
    ):
        raise ValueError("gateway SBOM donor libstdc++ file binding differs")
    critical = {
        item["path"]: item for item in receipt["image"]["rootfs"]["critical_entries"]
    }
    if critical.get(LIBSTDCXX_PATH, {}).get("sha256") != LIBSTDCXX_SHA256:
        raise ValueError("gateway root filesystem donor libstdc++ binding differs")

    scanned_os: dict[tuple[str, str, str], str] = {}
    scanned_metadata_rpms: dict[tuple[str, str], str] = {}
    for package in os_results[0]["Packages"]:
        purl = package["Identifier"]["PURL"]
        name, purl_version, arch = _parse_rpm_purl(
            purl, expected_distro="redhat-10.2"
        )
        release = package.get("Release")
        combined_version = (
            f"{package['Version']}-{release}" if release else package["Version"]
        )
        if package["Name"] != name or combined_version != purl_version:
            raise ValueError("Trivy OS package fields disagree with their package URL")
        if name == "gpg-pubkey":
            if arch != "None" or package.get("Arch") != "None":
                raise ValueError("Trivy signing-key RPM metadata has an unexpected arch")
            metadata_identity = (name, combined_version)
            if metadata_identity in scanned_metadata_rpms:
                raise ValueError("Trivy report duplicates signing-key RPM metadata")
            scanned_metadata_rpms[metadata_identity] = purl
            continue
        if arch is None or package.get("Arch") != arch:
            raise ValueError("Trivy OS package architecture fields disagree")
        identity = (name, combined_version, arch)
        if identity in scanned_os:
            raise ValueError("Trivy report duplicates one OS package identity")
        scanned_os[identity] = purl
    if set(scanned_os) != set(expected_os):
        raise ValueError("Trivy report does not cover the exact SBOM OS package inventory")
    if set(scanned_metadata_rpms) != set(expected_metadata_rpms):
        raise ValueError("Trivy report does not cover the exact SBOM RPM metadata inventory")

    scanned_language: dict[str, tuple[str, str]] = {}
    for package in language_results[0]["Packages"]:
        purl = package["Identifier"]["PURL"]
        name, version = _parse_npm_purl(purl)
        if package["Name"] != name or package["Version"] != version:
            raise ValueError("Trivy Node package fields disagree with their package URL")
        if purl in scanned_language:
            raise ValueError("Trivy report duplicates one Node package identity")
        scanned_language[purl] = (name, version)
    if scanned_language != expected_language:
        raise ValueError("Trivy report does not cover the exact SBOM Node package inventory")

    donor_report = normalise_trivy_report(
        donor_document, artifact_path=TRIVY_DONOR_PATH
    )
    donor_metadata = donor_report["Metadata"]
    if (
        donor_metadata["ImageID"] != donor["config_digest"]
        or donor_metadata["DiffIDs"] != donor["rootfs_diff_ids"]
    ):
        raise ValueError("Trivy donor report differs from the pinned donor OCI graph")
    donor_results = donor_report["Results"]
    if (
        len(donor_results) != 1
        or donor_results[0]["Class"] != "os-pkgs"
        or donor_results[0]["Type"] != "redhat"
        or donor_results[0]["Target"]
        != f"{TRIVY_DONOR_PATH} (redhat 10.2)"
    ):
        raise ValueError("Trivy donor report package target inventory is not closed")
    donor_packages: dict[tuple[str, str, str], str] = {}
    for package in donor_results[0]["Packages"]:
        purl = package["Identifier"]["PURL"]
        name, purl_version, arch = _parse_rpm_purl(
            purl, expected_distro="redhat-10.2"
        )
        release = package.get("Release")
        combined_version = (
            f"{package['Version']}-{release}" if isinstance(release, str) else ""
        )
        if (
            not isinstance(release, str)
            or arch is None
            or package.get("Arch") != arch
            or package["Name"] != name
            or combined_version != purl_version
        ):
            raise ValueError("Trivy donor package lacks release or architecture identity")
        identity = (name, combined_version, arch)
        if identity in donor_packages:
            raise ValueError("Trivy donor report duplicates an RPM identity")
        donor_packages[identity] = purl
    donor_identity = (
        LIBSTDCXX_RPM_NAME,
        LIBSTDCXX_RPM_VERSION,
        "x86_64",
    )
    donor_report_purl = donor_packages.get(donor_identity)
    if donor_report_purl is None:
        raise ValueError("Trivy donor report omits the exact copied libstdc++ RPM")

    return {
        "mode": "exact-oci-archive-plus-pinned-donor",
        "operating_system": {
            "family": "redhat",
            "version": "10.2",
            "class": "os-pkgs",
            "type": "redhat",
            "scanned_packages": [
                {
                    "name": name,
                    "version": version,
                    "arch": arch,
                    "report_purl": scanned_os[(name, version, arch)],
                    "sbom_purl": expected_os[(name, version, arch)],
                }
                for name, version, arch in sorted(expected_os)
            ],
            "scanned_metadata_packages": [
                {
                    "name": name,
                    "version": version,
                    "report_purl": scanned_metadata_rpms[(name, version)],
                    "sbom_purl": expected_metadata_rpms[(name, version)],
                }
                for name, version in sorted(expected_metadata_rpms)
            ],
        },
        "language": {
            "class": "lang-pkgs",
            "type": "node-pkg",
            "scanned_purls": sorted(expected_language),
        },
        "external_runtime_package": {
            "name": LIBSTDCXX_RPM_NAME,
            "version": LIBSTDCXX_RPM_VERSION,
            "sbom_purl": LIBSTDCXX_RPM_PURL,
            "report_purl": donor_report_purl,
            "file_path": LIBSTDCXX_PATH,
            "file_sha256": LIBSTDCXX_SHA256,
            "donor_reference": donor["reference"],
            "donor_manifest_digest": donor["manifest_digest"],
            "donor_config_digest": donor["config_digest"],
            "donor_rootfs_diff_ids": donor["rootfs_diff_ids"],
            "donor_scanned_rpm_count": len(donor_packages),
        },
        "passed": True,
    }


def project_findings(
    document: dict[str, Any], *, package_allowlist: frozenset[str] | None = None
) -> list[dict[str, Any]]:
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
            if package_allowlist is not None and package not in package_allowlist:
                continue
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
        key=_finding_sort_key,
    )


def _finding_sort_key(item: dict[str, Any]) -> tuple[str, ...]:
    return (
        item["severity"],
        item["id"],
        item["target"],
        item["package"],
        item["installed_version"],
        item["fixed_version"] or "",
    )


def project_all_findings(
    report: dict[str, Any], donor_report: dict[str, Any]
) -> list[dict[str, Any]]:
    findings = [
        *project_findings(report),
        *project_findings(
            donor_report, package_allowlist=frozenset({LIBSTDCXX_RPM_NAME})
        ),
    ]
    if len(findings) > MAX_FINDINGS:
        raise ValueError("combined Trivy reports exceed the retained finding-count bound")
    return sorted(findings, key=_finding_sort_key)


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


def _acquire_scan_images(donor_archive: Path) -> dict[str, Any]:
    _acquire_trivy_image()
    subprocess.run(
        ("docker", "pull", UBI_RUNTIME_LIBRARY_DONOR_REFERENCE),
        cwd=ROOT,
        check=True,
        timeout=20 * 60,
    )
    temporary = donor_archive.with_suffix(donor_archive.suffix + ".tmp")
    try:
        subprocess.run(
            (
                "docker",
                "image",
                "save",
                f"--output={temporary}",
                UBI_RUNTIME_LIBRARY_DONOR_REFERENCE,
            ),
            cwd=ROOT,
            check=True,
            timeout=20 * 60,
        )
        identity = inspect_donor_archive(temporary)
        temporary.replace(donor_archive)
        return {**identity, "file": donor_archive.name}
    finally:
        temporary.unlink(missing_ok=True)


def _docker_scan(
    *,
    cache: Path,
    archive: Path,
    artifact_path: str,
    offline: bool,
    pull: str,
) -> dict[str, Any]:
    if offline and pull != "never":
        raise ValueError("offline Trivy replay must use Docker pull=never")
    archive_metadata = archive.lstat()
    if (
        stat.S_ISLNK(archive_metadata.st_mode)
        or not stat.S_ISREG(archive_metadata.st_mode)
        or archive_metadata.st_size < 1
        or archive_metadata.st_size > MAX_OCI_BYTES
        or artifact_path not in {TRIVY_OCI_PATH, TRIVY_DONOR_PATH}
    ):
        raise ValueError("Trivy OCI input archive is invalid or outside its bound")
    mounted_archive = archive.resolve(strict=True)
    mounted_cache = cache.resolve(strict=True)
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
        f"--volume={mounted_archive}:{artifact_path}:ro",
        f"--volume={mounted_cache}:/cache",
    ]
    if offline:
        arguments.append("--network=none")
    arguments.extend(
        [
            TRIVY_REFERENCE,
            "image",
            f"--input={artifact_path}",
            "--cache-dir=/cache",
            "--cache-backend=memory",
            "--scanners=vuln",
            "--severity=HIGH,CRITICAL", "--format=json", "--no-progress",
            "--list-all-pkgs",
        ]
    )
    if offline:
        arguments.extend(["--skip-db-update", "--offline-scan"])
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
    return normalise_trivy_report(report, artifact_path=artifact_path)


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


def _file_binding(path: Path) -> dict[str, Any]:
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise ValueError(f"retained evidence file is not one regular file: {path.name}")
    return {
        "file": path.name,
        "sha256": sha256_file(path),
        "bytes": metadata.st_size,
    }


def bind_gateway_archive(archive: Path, receipt: dict[str, Any]) -> dict[str, Any]:
    """Bind the scan input to the exact archive already measured by the image receipt."""
    image = receipt.get("image")
    if not isinstance(image, dict):
        raise ValueError("gateway image receipt lacks its exact OCI identity")
    file_binding = _file_binding(archive)
    if file_binding != {
        "file": image.get("archive"),
        "sha256": image.get("archive_sha256"),
        "bytes": image.get("archive_bytes"),
    }:
        raise ValueError("gateway vulnerability scan input differs from the exact OCI receipt")
    config_digest = image.get("config_digest")
    rootfs_diff_ids = image.get("rootfs_diff_ids")
    rootfs = image.get("rootfs")
    if (
        not isinstance(config_digest, str)
        or _SHA256_DIGEST.fullmatch(config_digest) is None
        or not isinstance(rootfs_diff_ids, list)
        or not rootfs_diff_ids
        or len(rootfs_diff_ids) > 64
        or any(
            not isinstance(item, str) or _SHA256_DIGEST.fullmatch(item) is None
            for item in rootfs_diff_ids
        )
        or len(set(rootfs_diff_ids)) != len(rootfs_diff_ids)
        or not isinstance(rootfs, dict)
        or not isinstance(rootfs.get("inventory_sha256"), str)
        or re.fullmatch(r"[0-9a-f]{64}", rootfs["inventory_sha256"]) is None
    ):
        raise ValueError("gateway image receipt lacks its measured OCI configuration")
    return {
        **file_binding,
        "config_digest": config_digest,
        "rootfs_diff_ids": rootfs_diff_ids,
        "rootfs_inventory_sha256": rootfs["inventory_sha256"],
    }


def generate_scan_evidence(
    *, archive: Path, sbom: Path, receipt_path: Path, output: Path
) -> dict[str, Any]:
    receipt = load_bounded_json_object(
        receipt_path,
        maximum_bytes=MAX_RECEIPT_JSON_BYTES,
        label="gateway image receipt",
    )
    image_binding = bind_gateway_archive(archive, receipt)
    started_at = utc_timestamp()
    started = time.monotonic()
    output.parent.mkdir(parents=True, exist_ok=True)
    archive_path = output.parent / DB_ARCHIVE_NAME
    checksum_path = output.parent / DB_CHECKSUM_NAME
    report_path = output.parent / REPORT_NAME
    donor_archive_path = output.parent / DONOR_ARCHIVE_NAME
    donor_report_path = output.parent / DONOR_REPORT_NAME
    donor = _acquire_scan_images(donor_archive_path)
    with tempfile.TemporaryDirectory(prefix="gis-ai-go-trivy-online-") as online_temporary:
        online_cache = Path(online_temporary) / "cache"
        online_cache.mkdir(mode=0o700)
        _docker_scan(
            cache=online_cache,
            archive=archive,
            artifact_path=TRIVY_OCI_PATH,
            offline=False,
            pull="never",
        )
        _docker_scan(
            cache=online_cache,
            archive=donor_archive_path,
            artifact_path=TRIVY_DONOR_PATH,
            offline=False,
            pull="never",
        )
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
        report = _docker_scan(
            cache=replay_cache,
            archive=archive,
            artifact_path=TRIVY_OCI_PATH,
            offline=True,
            pull="never",
        )
        donor_report = _docker_scan(
            cache=replay_cache,
            archive=donor_archive_path,
            artifact_path=TRIVY_DONOR_PATH,
            offline=True,
            pull="never",
        )
        if cache_inventory(replay_cache) != inventory:
            raise ValueError("offline Trivy replay mutated the retained database")
    report_bytes = canonical_json_bytes(report)
    donor_report_bytes = canonical_json_bytes(donor_report)
    assert_no_private_json(report, "gateway Trivy report")
    assert_no_private_text(report_bytes, "gateway Trivy report")
    assert_no_private_json(donor_report, "gateway donor Trivy report")
    assert_no_private_text(donor_report_bytes, "gateway donor Trivy report")
    sbom_document = load_bounded_json_object(
        sbom,
        maximum_bytes=MAX_SBOM_JSON_BYTES,
        label="gateway image SBOM",
    )
    coverage = project_coverage(
        report, donor_report, sbom_document, receipt, donor
    )
    node_runtime, node_findings = generate_node_advisory(
        sbom=sbom_document,
        receipt=receipt,
        output=output.parent,
    )
    findings = sorted(
        [*project_all_findings(report, donor_report), *node_findings],
        key=_finding_sort_key,
    )
    fixable, passed = evaluate_policy(findings)
    evidence = {
        "schema": "gis-ai-go.gateway-image-vulnerability-scan.v3",
        "classification": (
            "repository-only-blocked-candidate"
            if receipt["source"]["clean"] else "non-publishable-development-build"
        ),
        "source_revision": receipt["source"]["revision"],
        "image_manifest_digest": receipt["image"]["manifest_digest"],
        "image": image_binding,
        "donor_image": donor,
        "scanner": {"image": TRIVY_REFERENCE, "version": TRIVY_VERSION},
        "sbom": {"file": sbom.name, "sha256": sha256_file(sbom), "bytes": sbom.stat().st_size},
        "database": {
            "archive": archive_path.name, "archive_sha256": sha256_file(archive_path),
            "archive_bytes": archive_path.stat().st_size,
            "expanded_bytes": sum(item["bytes"] for item in inventory),
            "file_count": len(inventory), "files": inventory,
        },
        "reports": {
            "gateway": {
                "file": report_path.name,
                "sha256": hashlib.sha256(report_bytes).hexdigest(),
                "bytes": len(report_bytes),
            },
            "runtime_library_donor": {
                "file": donor_report_path.name,
                "sha256": hashlib.sha256(donor_report_bytes).hexdigest(),
                "bytes": len(donor_report_bytes),
            },
        },
        "replay": {
            "pull": "never",
            "network": "none",
            "skip_db_update": True,
            "offline_scan": True,
            "list_all_packages": True,
            "inputs": [archive.name, donor_archive_path.name],
        },
        "node_runtime": node_runtime,
        "coverage": coverage,
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
    donor_report_path.write_bytes(donor_report_bytes)
    output.write_bytes(output_bytes)
    if not passed:
        raise AssertionError(
            f"gateway image has {len(fixable)} fixable high or critical vulnerabilities"
        )
    return evidence


def verify_scan_evidence(
    *,
    scan_path: Path,
    archive: Path,
    sbom: Path,
    receipt_path: Path,
    replay: bool,
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
    image_binding = bind_gateway_archive(archive, receipt)
    donor_archive = scan_path.parent / DONOR_ARCHIVE_NAME
    donor = inspect_donor_archive(donor_archive)
    if (
        scan["classification"] != expected_classification
        or scan["source_revision"] != receipt["source"]["revision"]
        or scan["image_manifest_digest"] != receipt["image"]["manifest_digest"]
        or scan["image"] != image_binding
        or scan["donor_image"] != donor
        or scan["sbom"]
        != {
            "file": sbom.name,
            "sha256": hashlib.sha256(sbom_bytes).hexdigest(),
            "bytes": len(sbom_bytes),
        }
    ):
        raise ValueError("gateway vulnerability receipt differs from source, image or SBOM")
    database_archive = scan_path.parent / scan["database"]["archive"]
    checksum = scan_path.parent / DB_CHECKSUM_NAME
    if (
        parse_checksum(checksum, database_archive.name)
        != sha256_file(database_archive)
    ):
        raise ValueError("retained Trivy database checksum differs")
    archive_metadata = database_archive.lstat()
    with tempfile.TemporaryDirectory(prefix="gis-ai-go-trivy-verify-") as temporary:
        cache = Path(temporary) / "cache"
        cache.mkdir(mode=0o700)
        inventory = inspect_database_archive(database_archive, extract_to=cache)
        expected_database = {
            "archive": database_archive.name,
            "archive_sha256": sha256_file(database_archive),
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
                archive=archive,
                artifact_path=TRIVY_OCI_PATH,
                offline=True,
                pull="never",
            )
            replay_donor_report = _docker_scan(
                cache=cache,
                archive=donor_archive,
                artifact_path=TRIVY_DONOR_PATH,
                offline=True,
                pull="never",
            )
            if cache_inventory(cache) != inventory:
                raise ValueError("verification replay mutated the retained Trivy database")
    report_path = scan_path.parent / scan["reports"]["gateway"]["file"]
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
    report = normalise_trivy_report(report)
    expected_report = {
        "file": report_path.name,
        "sha256": hashlib.sha256(report_bytes).hexdigest(),
        "bytes": len(report_bytes),
    }
    if (
        canonical_json_bytes(report) != report_bytes
        or scan["reports"]["gateway"] != expected_report
    ):
        raise ValueError("gateway vulnerability receipt report binding differs")
    donor_report_path = scan_path.parent / scan["reports"][
        "runtime_library_donor"
    ]["file"]
    donor_report_bytes = read_bounded_regular_file(
        donor_report_path,
        maximum_bytes=MAX_REPORT_BYTES,
        label="retained donor Trivy scan report",
    )
    donor_report = parse_bounded_json_object(
        donor_report_bytes,
        maximum_bytes=MAX_REPORT_BYTES,
        label="retained donor Trivy scan report",
    )
    donor_report = normalise_trivy_report(
        donor_report, artifact_path=TRIVY_DONOR_PATH
    )
    expected_donor_report = {
        "file": donor_report_path.name,
        "sha256": hashlib.sha256(donor_report_bytes).hexdigest(),
        "bytes": len(donor_report_bytes),
    }
    if (
        canonical_json_bytes(donor_report) != donor_report_bytes
        or scan["reports"]["runtime_library_donor"] != expected_donor_report
    ):
        raise ValueError("gateway donor vulnerability report binding differs")
    sbom_document = parse_bounded_json_object(
        sbom_bytes,
        maximum_bytes=MAX_SBOM_JSON_BYTES,
        label="gateway image SBOM",
    )
    coverage = project_coverage(
        report, donor_report, sbom_document, receipt, donor
    )
    node_findings = verify_node_advisory(
        node=scan["node_runtime"],
        directory=scan_path.parent,
        sbom=sbom_document,
        receipt=receipt,
        phase=scan["phase"],
        replay=replay,
    )
    findings = sorted(
        [*project_all_findings(report, donor_report), *node_findings],
        key=_finding_sort_key,
    )
    fixable, passed = evaluate_policy(findings)
    if (
        scan["coverage"] != coverage
        or scan["findings"] != findings
        or scan["fixable_findings"] != fixable
        or scan["passed"] != passed or not passed
    ):
        raise ValueError("gateway vulnerability policy projection differs from its report")
    verify_phase_timing(scan["phase"])
    if replay:
        if replay_projection(replay_report) != replay_projection(report):
            raise ValueError("offline Trivy replay differs from the retained report")
        if replay_projection(replay_donor_report) != replay_projection(donor_report):
            raise ValueError("offline donor Trivy replay differs from the retained report")
    return scan


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--sbom", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sbom = args.sbom if args.sbom.is_absolute() else ROOT / args.sbom
    receipt = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    if args.archive is None:
        archive = receipt.parent / "gateway-image.oci.tar"
    else:
        archive = args.archive if args.archive.is_absolute() else ROOT / args.archive
    output = args.output if args.output.is_absolute() else ROOT / args.output
    generate_scan_evidence(
        archive=archive, sbom=sbom, receipt_path=receipt, output=output
    )
    print("Gateway image vulnerability scan and retained offline replay passed.")


if __name__ == "__main__":
    main()
