#!/usr/bin/env python3
"""Independently verify and safely stage a bounded full-Explorer Pages archive.

The verifier streams tar members and retains only bounded JSON metadata and file
digests. It does not import the archive builder or execute archived source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO, Callable

REPOSITORY = "chris-page-gov/gis-ai-go"
BASE_PATH = "/gis-ai-go/"
CANONICAL_URL = "https://chris-page-gov.github.io/gis-ai-go/"
SCHEMA = "gis-ai-go.pages-archive-receipt.v2"
DISTRIBUTION = "EXPLORER-DISTRIBUTION.json"
MAX_TOTAL_BYTES = 999_999_999
MAX_ARCHIVE_BYTES = 1_060_000_000
MAX_FILE_BYTES = 32 * 1024 * 1024
MAX_FILES = 50_000
MAX_METADATA_BYTES = 32 * 1024 * 1024
MAX_RETAINED_METADATA_BYTES = 128 * 1024 * 1024
MAX_RECEIPT_BYTES = 64 * 1024
CHUNK_BYTES = 1024 * 1024
PUBLICATION_PATHS = frozenset({"publication/CHECKSUMS.sha256", "publication/manifest.json",
    "publication/provenance.json", "publication/site-receipt.json", "publication/sbom.cdx.json"})
IDENTITY_KEYS = {"repository", "sourceCommit", "version", "basePath", "canonicalUrl"}
OUTER_KEYS = {"schema", *IDENTITY_KEYS, "payloadRootSha256", "okfContentRootSha256",
    "archive", "checksum", "publication"}
SHA_RE = re.compile(r"[0-9a-f]{64}\Z")
COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
VERSION_RE = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?\Z")


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def require_keys(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{label} fields differ from the v2 contract")
    return value


def require_digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SHA_RE.fullmatch(value):
        raise ValueError(f"{label} must be a lowercase SHA-256 digest")
    return value


def safe_path(value: Any) -> str:
    if not isinstance(value, str) or not value or "\\" in value or any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError(f"unsafe v2 publication path: {value!r}")
    logical = PurePosixPath(value)
    if logical.is_absolute() or value != logical.as_posix() or any(part in {"", ".", ".."} for part in value.split("/")):
        raise ValueError(f"unsafe v2 publication path: {value!r}")
    parts = logical.parts
    if len(parts) > 16:
        raise ValueError("v2 publication path exceeds its component-depth ceiling")
    forbidden = {".git", ".github", "node_modules", "private", "research"}
    if any(part.casefold() in forbidden for part in parts) or value.casefold().endswith(".map"):
        raise ValueError(f"forbidden v2 publication path: {value}")
    hidden = any(part.startswith(".") for part in parts)
    if hidden and value not in {".nojekyll", "catalogue/.explorer-generated", "legacy/catalogue/.explorer-generated"}:
        raise ValueError(f"unexpected hidden v2 publication path: {value}")
    roots = {"index.html", "router.js", "style.css", "GIS-LICENCE", "EXPLORER-LICENSE.md", "EXPLORER-LICENSE-CODE.md", DISTRIBUTION, ".nojekyll"}
    if value not in roots and not value.startswith(("explorer/", "gis/explorer/", "legacy/", "catalogue/", "publication/")):
        raise ValueError(f"unexpected v2 distribution root: {value}")
    if value.startswith("publication/") and value not in PUBLICATION_PATHS:
        raise ValueError(f"unexpected v2 publication metadata: {value}")
    return value


def entries(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value or len(value) > MAX_FILES:
        raise ValueError(f"{label} must be a bounded non-empty array")
    paths = []
    for row in value:
        require_keys(row, {"path", "bytes", "sha256"}, label)
        paths.append(safe_path(row["path"]))
        if type(row["bytes"]) is not int or not 0 <= row["bytes"] <= MAX_FILE_BYTES:
            raise ValueError(f"{label} has an invalid byte count")
        require_digest(row["sha256"], label)
    if paths != sorted(set(paths)):
        raise ValueError(f"{label} paths must be unique and sorted")
    return value


def ledger(rows: list[dict[str, Any]]) -> bytes:
    return "".join(f"{row['sha256']}  {row['path']}\n" for row in rows).encode()


def identity(value: dict[str, Any], expected: dict[str, str], label: str) -> None:
    for key, item in expected.items():
        if value.get(key) != item:
            raise ValueError(f"{label} identity differs: {key}")


def json_bytes(raw: bytes, label: str, *, canonical: bool = True) -> Any:
    def reject_non_finite(value: str) -> None:
        raise ValueError(f"non-JSON numeric constant: {value}")
    try:
        value = json.loads(raw, parse_constant=reject_non_finite)
    except (UnicodeDecodeError, ValueError) as error:
        raise ValueError(f"{label} must be valid UTF-8 JSON") from error
    if canonical and canonical_json(value) != raw:
        raise ValueError(f"{label} must use canonical JSON")
    return value


def _regular_file(path: Path, maximum: int) -> BinaryIO:
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size > maximum:
        raise ValueError(f"input must be a bounded single-link regular file: {path.name}")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    opened = os.fstat(descriptor)
    if (opened.st_dev, opened.st_ino, opened.st_size) != (before.st_dev, before.st_ino, before.st_size):
        os.close(descriptor)
        raise ValueError(f"input changed while opened: {path.name}")
    return os.fdopen(descriptor, "rb")


def read_bounded(path: Path, maximum: int) -> bytes:
    with _regular_file(path, maximum) as handle:
        raw = handle.read(maximum + 1)
        if len(raw) > maximum:
            raise ValueError(f"input exceeds its byte ceiling: {path.name}")
        return raw


def archive_digest(path: Path) -> tuple[str, int]:
    hashed = hashlib.sha256()
    with _regular_file(path, MAX_ARCHIVE_BYTES) as handle:
        size = 0
        while chunk := handle.read(CHUNK_BYTES):
            hashed.update(chunk)
            size += len(chunk)
        if size > MAX_ARCHIVE_BYTES or size != os.fstat(handle.fileno()).st_size:
            raise ValueError("archive changed while hashed or exceeds its byte ceiling")
    return hashed.hexdigest(), size


def _read_members(archive_path: Path, consumer: Callable[[str, bytes], None] | None = None) -> tuple[list[dict[str, Any]], dict[str, bytes]]:
    rows: list[dict[str, Any]] = []
    retained: dict[str, bytes] = {}
    total = 0
    retained_bytes = 0
    last = ""
    expected_offset = 0
    seen = set()
    with _regular_file(archive_path, MAX_ARCHIVE_BYTES) as handle:
        with tarfile.open(fileobj=handle, mode="r:", format=tarfile.USTAR_FORMAT) as archive:
            for member in archive:
                if len(rows) >= MAX_FILES:
                    raise ValueError("v2 archive exceeds its file ceiling")
                if not member.name.startswith("./"):
                    raise ValueError("v2 tar members require the explicit './' root")
                path = safe_path(member.name[2:])
                if path <= last:
                    raise ValueError("v2 archive paths must be unique and sorted")
                last = path
                parts = path.split("/")
                if any("/".join(parts[:length]) in seen for length in range(1, len(parts))):
                    raise ValueError("v2 archive contains a file/directory prefix collision")
                seen.add(path)
                if (member.type != tarfile.REGTYPE or member.linkname or member.pax_headers
                    or member.mode != 0o644 or member.uid != 1000 or member.gid != 1000
                    or member.uname or member.gname or member.mtime != 0):
                    raise ValueError(f"v2 tar metadata is not normalised: {path}")
                if member.offset != expected_offset or member.offset_data != member.offset + 512:
                    raise ValueError("v2 tar must not contain extension or unlisted headers")
                normal = tarfile.TarInfo(member.name)
                normal.size = member.size
                normal.mode = 0o644
                normal.uid = normal.gid = 1000
                normal.uname = normal.gname = ""
                normal.mtime = 0
                normal.type = tarfile.REGTYPE
                handle.seek(member.offset)
                if handle.read(512) != normal.tobuf(format=tarfile.USTAR_FORMAT):
                    raise ValueError(f"v2 tar header is not canonical POSIX ustar: {path}")
                if not 0 <= member.size <= MAX_FILE_BYTES:
                    raise ValueError(f"v2 tar member exceeds its byte ceiling: {path}")
                total += member.size
                if total > MAX_TOTAL_BYTES:
                    raise ValueError("v2 served payload exceeds its byte ceiling")
                source = archive.extractfile(member)
                if source is None:
                    raise ValueError(f"v2 tar member cannot be read: {path}")
                keep = path in PUBLICATION_PATHS or path in {DISTRIBUTION, "explorer/okf-explorer-build-manifest.json", "gis/explorer/okf-explorer.json", "gis/explorer/context/manifest.json", "gis/explorer/projection-manifest.json"}
                chunks = []
                hashed = hashlib.sha256()
                count = 0
                while chunk := source.read(CHUNK_BYTES):
                    hashed.update(chunk)
                    count += len(chunk)
                    if keep:
                        chunks.append(chunk)
                    if consumer is not None:
                        consumer(path, chunk)
                if count != member.size:
                    raise ValueError(f"v2 tar member is truncated: {path}")
                if consumer is not None:
                    consumer(path, b"")
                rows.append({"path": path, "bytes": count, "sha256": hashed.hexdigest()})
                if keep:
                    retained_bytes += count
                    if retained_bytes > MAX_RETAINED_METADATA_BYTES:
                        raise ValueError("v2 retained metadata exceeds its aggregate byte ceiling")
                    retained[path] = b"".join(chunks)
                padding = (-member.size) % 512
                handle.seek(member.offset_data + member.size)
                if handle.read(padding) != b"\0" * padding:
                    raise ValueError("v2 tar member padding must be zero")
                expected_offset = member.offset_data + member.size + padding
        expected_size = ((expected_offset + 1024 + 10_239) // 10_240) * 10_240
        if os.fstat(handle.fileno()).st_size != expected_size:
            raise ValueError("v2 tar trailer length is not deterministic")
        handle.seek(expected_offset)
        if handle.read() != b"\0" * (expected_size - expected_offset):
            raise ValueError("v2 tar trailer must contain zero padding only")
    return rows, retained


def verify_distribution(distribution: dict[str, Any], rows: list[dict[str, Any]], retained: dict[str, bytes], expected: dict[str, str]) -> None:
    require_keys(distribution, {"schema", *IDENTITY_KEYS, "app", "okf", "files"}, "distribution")
    if distribution["schema"] != "gis-ai-go.explorer-distribution.v1":
        raise ValueError("distribution schema is not recognised")
    identity(distribution, expected, "distribution")
    declared = entries(distribution["files"], "distribution files")
    actual = [row for row in rows if row["path"] != DISTRIBUTION and row["path"] != ".nojekyll" and row["path"] not in PUBLICATION_PATHS]
    if declared != actual:
        raise ValueError("distribution inventory differs from its complete checked file closure")
    by_path = {row["path"]: row for row in rows}
    required = {"index.html", "router.js", "legacy/index.html", "GIS-LICENCE", "explorer/index.html", "explorer/explore/index.html", "gis/explorer/projection-manifest.json"}
    if not required.issubset(by_path):
        raise ValueError("v2 distribution is missing a required public component")
    app = require_keys(distribution["app"], {"sourceCommit", "treeSha256", "manifestSha256", "path"}, "distribution app")
    if not isinstance(app["sourceCommit"], str) or not COMMIT_RE.fullmatch(app["sourceCommit"]) or app["path"] != "explorer/okf-explorer-build-manifest.json":
        raise ValueError("distribution app source/path is invalid")
    if app["manifestSha256"] != by_path[app["path"]]["sha256"]:
        raise ValueError("distribution app manifest digest differs")
    manifest = json_bytes(retained[app["path"]], "app manifest", canonical=False)
    require_keys(manifest, {"schema", "algorithm", "file_count", "tree_sha256", "materials"}, "app manifest")
    if manifest["schema"] != "okf-explorer-app-build-manifest.v1" or manifest["algorithm"] != "sha256-canonical-json-materials-v1":
        raise ValueError("app manifest schema/algorithm is not recognised")
    materials = []
    names = []
    for item in manifest["materials"]:
        require_keys(item, {"path", "bytes", "sha256"}, "app material")
        if not isinstance(item["path"], str) or type(item["bytes"]) is not int or not 0 <= item["bytes"] <= MAX_FILE_BYTES:
            raise ValueError("app material path/byte count is invalid")
        require_digest(item["sha256"], "app material digest")
        path = safe_path("explorer/" + item["path"])
        names.append(path)
        if by_path.get(path) != {**item, "path": path}:
            raise ValueError(f"app material differs: {path}")
        materials.append({"path": item["path"], "bytes": item["bytes"], "sha256": item["sha256"]})
    if names != sorted(set(names)) or type(manifest["file_count"]) is not int or manifest["file_count"] != len(names) or "explorer/index.html" not in names or "explorer/okf-explorer-build-manifest.json" in names:
        raise ValueError("app materials must be complete, unique and sorted")
    app_tree = digest((json.dumps(materials, ensure_ascii=False, separators=(",", ":")) + "\n").encode())
    if app_tree != manifest["tree_sha256"] or app_tree != app["treeSha256"]:
        raise ValueError("app tree digest differs from its canonical materials")
    okf = require_keys(distribution["okf"], {"sourceRevision", "inputDigest", "snapshot", "descriptorPath", "contextManifestPath"}, "distribution OKF")
    if okf["sourceRevision"] != expected["sourceCommit"] or okf["descriptorPath"] != "gis/explorer/okf-explorer.json" or okf["contextManifestPath"] != "gis/explorer/context/manifest.json":
        raise ValueError("distribution OKF source/path differs")
    require_digest(okf["inputDigest"], "OKF input digest")
    descriptor = json_bytes(retained[okf["descriptorPath"]], "GIS descriptor", canonical=False)
    context = json_bytes(retained[okf["contextManifestPath"]], "GIS context", canonical=False)
    if not isinstance(descriptor, dict) or descriptor.get("schema") != "okf-explorer-large-corpus.v1" or not isinstance(context, dict) or context.get("schema") != "okf-context-corpus.v3":
        raise ValueError("GIS descriptor/context schema is not recognised")
    source = descriptor.get("source", {})
    if source.get("revision") != okf["sourceRevision"] or source.get("inputDigest") != okf["inputDigest"] or descriptor.get("snapshot") != okf["snapshot"]:
        raise ValueError("GIS descriptor identity differs from distribution")
    if context.get("bundle", {}).get("snapshot") != okf["snapshot"] or context.get("semantic_source_snapshot") != okf["snapshot"] or context.get("bundle", {}).get("source_url") != CANONICAL_URL + "gis/explorer/context/manifest.json":
        raise ValueError("GIS context is not bound to the canonical publication and snapshot")
    if context.get("extensions", {}).get("inputRevision") != okf["sourceRevision"] or context.get("extensions", {}).get("inputDigest") != okf["inputDigest"]:
        raise ValueError("GIS context producer input identity differs")
    projection = json_bytes(retained["gis/explorer/projection-manifest.json"], "Reader projection", canonical=False)
    if not isinstance(projection, dict) or projection.get("schema") != "gis-ai-go.okf-plus-explorer-projection.v1":
        raise ValueError("Reader projection schema is not recognised")
    if any(projection.get(key) != value for key, value in {"sourceRevision": okf["sourceRevision"], "inputDigest": okf["inputDigest"], "snapshot": okf["snapshot"]}.items()):
        raise ValueError("Reader projection identity differs")
    projection_rows = projection.get("outputs")
    if not isinstance(projection_rows, list) or not projection_rows:
        raise ValueError("Reader projection must bind its complete file closure")
    bound = set()
    for reference in projection_rows:
        path = safe_path("gis/explorer/" + reference["path"])
        observed = by_path.get(path)
        if observed is None or observed["bytes"] != reference.get("bytes") or observed["sha256"] != reference.get("sha256") or path in bound:
            raise ValueError(f"Reader projection reference differs: {path}")
        bound.add(path)
    if bound != {path for path in by_path if path.startswith("gis/explorer/")} - {"gis/explorer/projection-manifest.json"}:
        raise ValueError("Reader projection file closure differs")
    legacy = {path.removeprefix("legacy/"): row for path, row in by_path.items() if path.startswith("legacy/catalogue/")}
    direct = {path: row for path, row in by_path.items() if path.startswith("catalogue/")}
    if set(legacy) != set(direct) or any(legacy[path]["bytes"] != direct[path]["bytes"] or legacy[path]["sha256"] != direct[path]["sha256"] for path in direct):
        raise ValueError("legacy direct catalogue URLs differ from the retained catalogue")


def verify_archive(*, archive_path: Path, checksum_path: Path, receipt_path: Path,
    expected_source_commit: str, expected_repository: str, expected_version: str,
    expected_base_path: str, expected_archive_sha256: str | None = None) -> dict[str, Any]:
    if expected_repository != REPOSITORY or expected_base_path != BASE_PATH or not COMMIT_RE.fullmatch(expected_source_commit) or not VERSION_RE.fullmatch(expected_version):
        raise ValueError("expected v2 publication identity is invalid")
    expected = {"repository": expected_repository, "sourceCommit": expected_source_commit, "version": expected_version, "basePath": expected_base_path, "canonicalUrl": CANONICAL_URL}
    receipt = require_keys(json_bytes(read_bounded(receipt_path, MAX_RECEIPT_BYTES), "archive receipt"), OUTER_KEYS, "archive receipt")
    if receipt["schema"] != SCHEMA:
        raise ValueError("v2 archive receipt schema is not recognised")
    identity(receipt, expected, "archive receipt")
    archive_hash, archive_size = archive_digest(archive_path)
    checksum = read_bounded(checksum_path, MAX_RECEIPT_BYTES)
    if checksum != f"{archive_hash}  artifact.tar\n".encode() or (expected_archive_sha256 is not None and archive_hash != require_digest(expected_archive_sha256, "expected archive digest")):
        raise ValueError("archive does not match its accepted digest/checksum")
    if receipt["archive"] != {"path": "artifact.tar", "format": "POSIX ustar", "bytes": archive_size, "sha256": archive_hash} or receipt["checksum"] != {"path": "artifact.tar.sha256", "sha256": digest(checksum)}:
        raise ValueError("archive receipt transport identity differs")
    rows, retained = _read_members(archive_path)
    by_path = {row["path"]: row for row in rows}
    if not PUBLICATION_PATHS.issubset(retained) or DISTRIBUTION not in retained or by_path.get(".nojekyll") != {"path": ".nojekyll", "bytes": 0, "sha256": digest(b"")}:
        raise ValueError("v2 archive is missing its fixed metadata")
    payload = [row for row in rows if row["path"] not in PUBLICATION_PATHS]
    root = digest(ledger(payload))
    public = [row for row in rows if row["path"] not in {".nojekyll", "publication/CHECKSUMS.sha256"}]
    if retained["publication/CHECKSUMS.sha256"] != ledger(public):
        raise ValueError("public checksum ledger does not cover every served file exactly")
    distribution = json_bytes(retained[DISTRIBUTION], "distribution")
    verify_distribution(distribution, rows, retained, expected)
    manifest = require_keys(json_bytes(retained["publication/manifest.json"], "publication manifest"), {"schema", *IDENTITY_KEYS, "app", "okf", "okfContentRootSha256", "payload", "publicationFiles"}, "publication manifest")
    identity(manifest, expected, "publication manifest")
    supporting = [row for row in rows if row["path"] in PUBLICATION_PATHS - {"publication/manifest.json", "publication/CHECKSUMS.sha256"}]
    if manifest["schema"] != "gis-ai-go.pages-manifest.v2" or manifest["payload"] != {"fileCount": len(payload), "rootSha256": root, "files": payload} or manifest["publicationFiles"] != supporting:
        raise ValueError("publication manifest differs from the complete archived payload")
    okf_root = distribution["okf"]["inputDigest"]
    for item, label in [(manifest, "manifest"), (receipt, "receipt")]:
        if item["okfContentRootSha256"] != okf_root:
            raise ValueError(f"{label} OKF input root differs")
    if receipt["payloadRootSha256"] != root:
        raise ValueError("archive receipt payload root differs")
    provenance = require_keys(json_bytes(retained["publication/provenance.json"], "provenance"), {"schema", *IDENTITY_KEYS, "app", "okf", "builder", "source", "determinism"}, "provenance")
    site = require_keys(json_bytes(retained["publication/site-receipt.json"], "site receipt"), {"schema", *IDENTITY_KEYS, "app", "okf", "fileCount", "payloadRootSha256", "okfContentRootSha256", "okfManifestSha256", "provenanceSha256", "sbomSha256"}, "site receipt")
    for item, schema in [(provenance, "gis-ai-go.pages-provenance.v2"), (site, "gis-ai-go.pages-site-receipt.v2")]:
        identity(item, expected, schema)
        if item.get("schema") != schema or item.get("app") != distribution["app"] or item.get("okf") != distribution["okf"]:
            raise ValueError(f"{schema} component identities differ")
    if manifest["app"] != distribution["app"] or manifest["okf"] != distribution["okf"] or provenance.get("source") != {"path": "artifacts/explorer-pages-dist", "fileCount": len(payload), "payloadRootSha256": root}:
        raise ValueError("publication component/provenance identity differs")
    if provenance["builder"] != {"name": "scripts/package_explorer_pages.py", "version": "2.0.0"} or provenance["determinism"] != {"archiveFormat": "POSIX ustar", "pathOrder": "lexicographic UTF-8 publication path", "uid": 1000, "gid": 1000, "userName": "", "groupName": "", "fileMode": "0644", "modificationTime": 0, "wallClockIncluded": False}:
        raise ValueError("publication builder/determinism declaration differs from v2")
    if site.get("fileCount") != len(payload) or site.get("payloadRootSha256") != root or site.get("okfContentRootSha256") != okf_root or site.get("okfManifestSha256") != by_path[distribution["okf"]["descriptorPath"]]["sha256"] or site.get("provenanceSha256") != digest(retained["publication/provenance.json"]) or site.get("sbomSha256") != digest(retained["publication/sbom.cdx.json"]):
        raise ValueError("site receipt differs from its bound publication")
    sbom = require_keys(json_bytes(retained["publication/sbom.cdx.json"], "publication SBOM"), {"bomFormat", "specVersion", "version", "metadata", "components"}, "publication SBOM")
    components = [{"bom-ref": f"file:{row['path']}@sha256:{row['sha256']}", "type": "file", "name": row["path"], "hashes": [{"alg": "SHA-256", "content": row["sha256"]}], "properties": [{"name": "gis-ai-go:bytes", "value": str(row["bytes"])}]} for row in payload]
    if sbom.get("bomFormat") != "CycloneDX" or sbom.get("specVersion") != "1.6" or sbom.get("version") != 1 or sbom.get("components") != components:
        raise ValueError("publication SBOM differs from the complete file inventory")
    expected_sbom_metadata = {"component": {"type": "application", "name": "GIS AI GO full OKF Explorer", "version": expected_version, "hashes": [{"alg": "SHA-256", "content": root}], "licenses": [{"license": {"id": "MIT"}}]}}
    if sbom["metadata"] != expected_sbom_metadata:
        raise ValueError("publication SBOM product identity differs")
    expected_publication = {"checksumsSha256": digest(retained["publication/CHECKSUMS.sha256"]), "manifestSha256": digest(retained["publication/manifest.json"]), "provenanceSha256": digest(retained["publication/provenance.json"]), "siteReceiptSha256": digest(retained["publication/site-receipt.json"]), "sbomSha256": digest(retained["publication/sbom.cdx.json"])}
    if receipt["publication"] != expected_publication:
        raise ValueError("archive receipt publication digests differ")
    # Detect mutation between the digest pass and independent member validation.
    if archive_digest(archive_path) != (archive_hash, archive_size):
        raise ValueError("archive changed while its members were verified")
    return receipt


def stage_payload(*, archive_path: Path, checksum_path: Path, receipt_path: Path,
    output_dir: Path, expected_source_commit: str, expected_repository: str,
    expected_version: str, expected_base_path: str, expected_archive_sha256: str) -> dict[str, Any]:
    """Verify, stream and independently rehash exact bytes in a new pinned tree."""
    receipt = verify_archive(archive_path=archive_path, checksum_path=checksum_path, receipt_path=receipt_path,
        expected_source_commit=expected_source_commit, expected_repository=expected_repository,
        expected_version=expected_version, expected_base_path=expected_base_path,
        expected_archive_sha256=expected_archive_sha256)
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    read_flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    write_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    parent = output_dir.parent
    before = parent.lstat()
    if not stat.S_ISDIR(before.st_mode) or stat.S_ISLNK(before.st_mode) or output_dir.name in {"", ".", ".."}:
        raise ValueError("staging parent must be a real directory")
    parent_fd = os.open(parent, directory_flags)
    parent_identity = (before.st_dev, before.st_ino)
    output_fd: int | None = None
    active_fd: int | None = None
    active_parent: int | None = None
    active_path: str | None = None
    directories: dict[tuple[str, ...], tuple[int, int]] = {}
    files: dict[str, tuple[int, int]] = {}
    def metadata_identity(value: os.stat_result) -> tuple[int, int]:
        return value.st_dev, value.st_ino
    def child_directory(parent_descriptor: int, name: str, parts: tuple[str, ...]) -> int:
        if parts not in directories:
            if len(directories) >= MAX_FILES:
                raise ValueError("staging directory count exceeds its ceiling")
            try:
                os.mkdir(name, 0o755, dir_fd=parent_descriptor)
            except FileExistsError as error:
                raise ValueError("an unverified staging directory appeared") from error
            metadata = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
            if not stat.S_ISDIR(metadata.st_mode):
                raise ValueError("a staging directory was replaced")
            directories[parts] = metadata_identity(metadata)
        descriptor = os.open(name, directory_flags, dir_fd=parent_descriptor)
        if metadata_identity(os.fstat(descriptor)) != directories[parts]:
            os.close(descriptor)
            raise ValueError("staging directory identity differs")
        os.fchmod(descriptor, 0o755)
        return descriptor
    def consume(path: str, chunk: bytes) -> None:
        nonlocal active_fd, active_parent, active_path
        assert output_fd is not None
        if active_path is None:
            current = os.dup(output_fd)
            prefix: tuple[str, ...] = ()
            try:
                parts = tuple(path.split("/"))
                for name in parts[:-1]:
                    prefix = (*prefix, name)
                    child = child_directory(current, name, prefix)
                    os.close(current)
                    current = child
                active_fd = os.open(parts[-1], write_flags, 0o600, dir_fd=current)
                opened = os.fstat(active_fd)
                if not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1:
                    raise ValueError("staging file is not an ordinary single-link file")
                active_parent, active_path = current, path
            except Exception:
                os.close(current)
                raise
        if active_path != path or active_fd is None or active_parent is None:
            raise ValueError("staging stream changed its active file")
        if chunk:
            view = memoryview(chunk)
            while view:
                count = os.write(active_fd, view)
                if count <= 0:
                    raise ValueError("staging write made no progress")
                view = view[count:]
            return
        os.fchmod(active_fd, 0o644)
        completed = os.fstat(active_fd)
        named = os.stat(path.split("/")[-1], dir_fd=active_parent, follow_symlinks=False)
        if not stat.S_ISREG(named.st_mode) or named.st_nlink != 1 or metadata_identity(named) != metadata_identity(completed):
            raise ValueError("staging file was replaced while written")
        files[path] = metadata_identity(completed)
        os.close(active_fd)
        os.close(active_parent)
        active_fd = active_parent = None
        active_path = None
    observed: list[dict[str, Any]] = []
    def inspect(descriptor: int, parts: tuple[str, ...]) -> None:
        opened = os.fstat(descriptor)
        if metadata_identity(opened) != directories[parts] or not stat.S_ISDIR(opened.st_mode) or stat.S_IMODE(opened.st_mode) != 0o755:
            raise ValueError("staged directory metadata differs")
        with os.scandir(descriptor) as directory:
            names = sorted(entry.name for entry in directory)
        for name in names:
            child_parts = (*parts, name)
            logical = "/".join(child_parts)
            metadata = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
            if stat.S_ISDIR(metadata.st_mode):
                if child_parts not in directories:
                    raise ValueError("staging tree contains an unexpected directory")
                child = child_directory(descriptor, name, child_parts)
                try:
                    inspect(child, child_parts)
                finally:
                    os.close(child)
                continue
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1 or stat.S_IMODE(metadata.st_mode) != 0o644 or files.get(logical) != metadata_identity(metadata):
                raise ValueError("staging tree contains an unexpected or replaced file")
            child = os.open(name, read_flags, dir_fd=descriptor)
            try:
                opened = os.fstat(child)
                if metadata_identity(opened) != files[logical] or not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1:
                    raise ValueError("staging file changed while reopened")
                hashed = hashlib.sha256()
                count = 0
                while chunk := os.read(child, CHUNK_BYTES):
                    count += len(chunk)
                    if count > MAX_FILE_BYTES:
                        raise ValueError("staging file exceeds its byte ceiling")
                    hashed.update(chunk)
                observed.append({"path": logical, "bytes": count, "sha256": hashed.hexdigest()})
            finally:
                os.close(child)
    try:
        if metadata_identity(os.fstat(parent_fd)) != parent_identity:
            raise ValueError("staging parent changed while opened")
        try:
            os.mkdir(output_dir.name, 0o700, dir_fd=parent_fd)
        except FileExistsError as error:
            raise ValueError("staging output must not already exist") from error
        output_fd = os.open(output_dir.name, directory_flags, dir_fd=parent_fd)
        directories[()] = metadata_identity(os.fstat(output_fd))
        os.fchmod(output_fd, 0o755)
        copied, _ = _read_members(archive_path, consume)
        payload = [row for row in copied if row["path"] not in PUBLICATION_PATHS]
        if digest(ledger(payload)) != receipt["payloadRootSha256"]:
            raise ValueError("copied payload differs from the verified archive")
        by_path = {row["path"]: row for row in copied}
        digest_paths = {"checksumsSha256": "publication/CHECKSUMS.sha256", "manifestSha256": "publication/manifest.json", "provenanceSha256": "publication/provenance.json", "siteReceiptSha256": "publication/site-receipt.json", "sbomSha256": "publication/sbom.cdx.json"}
        if {key: by_path[path]["sha256"] for key, path in digest_paths.items()} != receipt["publication"]:
            raise ValueError("copied publication metadata differs from the verified archive")
        inspect(output_fd, ())
        if sorted(observed, key=lambda row: row["path"]) != copied:
            raise ValueError("staged inventory or bytes differ from the verified archive")
        parent_after = parent.lstat()
        named = os.stat(output_dir.name, dir_fd=parent_fd, follow_symlinks=False)
        if not stat.S_ISDIR(parent_after.st_mode) or stat.S_ISLNK(parent_after.st_mode) or metadata_identity(parent_after) != parent_identity or not stat.S_ISDIR(named.st_mode) or metadata_identity(named) != directories[()]:
            raise ValueError("named staging directory changed during verification")
        if archive_digest(archive_path)[0] != expected_archive_sha256:
            raise ValueError("archive changed while staged")
        return {"archiveSha256": expected_archive_sha256, "payloadRootSha256": receipt["payloadRootSha256"], "fileCount": len(copied), "outputDir": str(output_dir)}
    finally:
        if active_fd is not None:
            os.close(active_fd)
        if active_parent is not None:
            os.close(active_parent)
        if output_fd is not None:
            os.close(output_fd)
        os.close(parent_fd)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("archive", "checksum", "receipt"):
        parser.add_argument("--" + name, type=Path, required=True)
    for name in ("source-commit", "repository", "version", "base-path"):
        parser.add_argument("--expected-" + name, required=True)
    parser.add_argument("--expected-archive-sha256")
    args = parser.parse_args()
    receipt = verify_archive(archive_path=args.archive, checksum_path=args.checksum, receipt_path=args.receipt, expected_source_commit=args.expected_source_commit, expected_repository=args.expected_repository, expected_version=args.expected_version, expected_base_path=args.expected_base_path, expected_archive_sha256=args.expected_archive_sha256)
    print(f"Verified full Explorer Pages archive sha256={receipt['archive']['sha256']} source={receipt['sourceCommit']}.")


if __name__ == "__main__":
    main()
