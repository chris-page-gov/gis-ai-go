#!/usr/bin/env python3
"""Verify a GIS AI GO Pages archive without extracting or rebuilding the site."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import stat
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any

EXPECTED_REPOSITORY = "chris-page-gov/gis-ai-go"
EXPECTED_BASE_PATH = "/gis-ai-go/"
EXPECTED_CANONICAL_URL = "https://chris-page-gov.github.io/gis-ai-go/"
PUBLICATION_PATHS = {
    "publication/CHECKSUMS.sha256",
    "publication/manifest.json",
    "publication/provenance.json",
    "publication/site-receipt.json",
    "publication/sbom.cdx.json",
}
MAX_ARCHIVE_BYTES = 160 * 1024 * 1024
MAX_FILE_BYTES = 32 * 1024 * 1024
MAX_FILES = 10_010
MAX_METADATA_BYTES = 2 * 1024 * 1024
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def require_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{label} fields differ from the contract; "
            f"missing={sorted(expected - actual)}; extra={sorted(actual - expected)}"
        )
    return value


def require_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise ValueError(f"{label} must be a lowercase SHA-256 digest")
    return value


def safe_archive_path(value: str) -> str:
    logical = PurePosixPath(value)
    if (
        not value
        or value.startswith("/")
        or "\\" in value
        or "\0" in value
        or logical.is_absolute()
        or any(part in {"", ".", ".."} for part in logical.parts)
    ):
        raise ValueError(f"unsafe archive path: {value!r}")
    lowered = value.casefold()
    if (
        any(
            part.casefold() in {".git", "docs", "node_modules", "research"}
            for part in logical.parts
        )
        or ("publication" in logical.parts and logical.parts[0] != "publication")
        or "research-pack" in lowered
        or lowered.endswith(".map")
    ):
        raise ValueError(f"forbidden archive path: {value}")
    hidden = [part for part in logical.parts if part.startswith(".")]
    if hidden and value not in {".nojekyll", "catalogue/.explorer-generated"}:
        raise ValueError(f"unexpected hidden archive path: {value}")
    return value


def parse_checksum_ledger(value: bytes, label: str) -> list[dict[str, str]]:
    try:
        text = value.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"{label} must be UTF-8") from error
    if not text.endswith("\n"):
        raise ValueError(f"{label} must end with a newline")
    rows: list[dict[str, str]] = []
    for line in text[:-1].split("\n"):
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            raise ValueError(f"invalid {label} row: {line!r}")
        rows.append({"sha256": match.group(1), "path": safe_archive_path(match.group(2))})
    paths = [row["path"] for row in rows]
    if not rows or paths != sorted(paths) or len(paths) != len(set(paths)):
        raise ValueError(f"{label} paths must be non-empty, unique and sorted")
    return rows


def checksum_ledger(entries: list[dict[str, Any]]) -> bytes:
    ordered = sorted(entries, key=lambda item: item["path"])
    return "".join(f"{item['sha256']}  {item['path']}\n" for item in ordered).encode()


def file_entry(path: str, value: bytes) -> dict[str, Any]:
    return {"path": path, "bytes": len(value), "sha256": sha256_bytes(value)}


def read_outer_file(path: Path, label: str, maximum_bytes: int) -> bytes:
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise ValueError(f"{label} does not exist") from error
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISREG(metadata.st_mode)
        or metadata.st_nlink != 1
    ):
        raise ValueError(f"{label} must be an ordinary single-link regular file")
    if metadata.st_size > maximum_bytes:
        raise ValueError(f"{label} exceeds {maximum_bytes} bytes")
    return path.read_bytes()


def deterministic_tar(files: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.USTAR_FORMAT) as archive:
        for path in sorted(files):
            value = files[path]
            member = tarfile.TarInfo(path)
            member.size = len(value)
            member.mode = 0o644
            member.uid = 0
            member.gid = 0
            member.uname = ""
            member.gname = ""
            member.mtime = 0
            member.type = tarfile.REGTYPE
            archive.addfile(member, io.BytesIO(value))
    return buffer.getvalue()


def read_archive(value: bytes) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    try:
        with tarfile.open(fileobj=io.BytesIO(value), mode="r:") as archive:
            members = archive.getmembers()
            if len(members) > MAX_FILES:
                raise ValueError(f"archive exceeds {MAX_FILES} members")
            paths = [member.name for member in members]
            if paths != sorted(paths) or len(paths) != len(set(paths)):
                raise ValueError("archive paths must be unique and sorted")
            for member in members:
                path = safe_archive_path(member.name)
                if member.type != tarfile.REGTYPE or not member.isfile():
                    raise ValueError(f"archive must contain regular files only: {path}")
                if member.linkname:
                    raise ValueError(f"archive member must not link elsewhere: {path}")
                if member.pax_headers:
                    raise ValueError(f"archive must not contain PAX metadata: {path}")
                if (
                    member.uid != 0
                    or member.gid != 0
                    or member.uname != ""
                    or member.gname != ""
                    or member.mode != 0o644
                    or member.mtime != 0
                ):
                    raise ValueError(f"archive member metadata is not normalised: {path}")
                if member.size > MAX_FILE_BYTES:
                    raise ValueError(f"archive member exceeds {MAX_FILE_BYTES} bytes: {path}")
                handle = archive.extractfile(member)
                if handle is None:
                    raise ValueError(f"archive member cannot be read: {path}")
                files[path] = handle.read()
    except tarfile.TarError as error:
        raise ValueError("artifact.tar is not a valid uncompressed POSIX tar archive") from error
    if deterministic_tar(files) != value:
        raise ValueError("archive bytes are not the canonical deterministic POSIX ustar encoding")
    return files


def parse_json_file(files: dict[str, bytes], path: str) -> Any:
    try:
        value = json.loads(files[path])
    except (KeyError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{path} must be valid UTF-8 JSON") from error
    if canonical_json(value) != files[path]:
        raise ValueError(f"{path} must use canonical sorted two-space JSON with a final newline")
    return value


def require_identity(
    value: dict[str, Any],
    *,
    repository: str,
    source_commit: str,
    version: str,
    base_path: str,
    label: str,
) -> None:
    expected = {
        "repository": repository,
        "sourceCommit": source_commit,
        "version": version,
        "basePath": base_path,
        "canonicalUrl": EXPECTED_CANONICAL_URL,
    }
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            raise ValueError(f"{label} {key} differs from the expected identity")


def require_file_entries(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a non-empty array")
    paths: list[str] = []
    for index, raw in enumerate(value):
        item = require_keys(raw, {"path", "bytes", "sha256"}, f"{label}[{index}]")
        if not isinstance(item["path"], str):
            raise ValueError(f"{label}[{index}].path must be a string")
        safe_archive_path(item["path"])
        if (
            not isinstance(item["bytes"], int)
            or isinstance(item["bytes"], bool)
            or item["bytes"] < 0
        ):
            raise ValueError(f"{label}[{index}].bytes must be a non-negative integer")
        require_sha256(item["sha256"], f"{label}[{index}].sha256")
        paths.append(item["path"])
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise ValueError(f"{label} paths must be unique and sorted")
    return value


def verify_catalogue(files: dict[str, bytes], manifest: dict[str, Any], version: str) -> None:
    catalogue_rows = parse_checksum_ledger(
        files["catalogue/CHECKSUMS.sha256"], "catalogue checksums"
    )
    catalogue_paths = {
        path.removeprefix("catalogue/")
        for path in files
        if path.startswith("catalogue/")
    }
    expected_paths = {
        ".explorer-generated",
        "CHECKSUMS.sha256",
        *(row["path"] for row in catalogue_rows),
    }
    if catalogue_paths != expected_paths:
        raise ValueError("archived catalogue inventory differs from catalogue checksums")
    for row in catalogue_rows:
        if sha256_bytes(files[f"catalogue/{row['path']}"]) != row["sha256"]:
            raise ValueError(f"archived catalogue checksum mismatch: {row['path']}")
    receipt = parse_json_file(files, "catalogue/build-receipt.json")
    if not isinstance(receipt, dict):
        raise ValueError("catalogue build receipt must be an object")
    if receipt.get("version") != version:
        raise ValueError("catalogue build receipt version differs from publication version")
    okf = manifest["okf"]
    expected = {
        "builder": receipt.get("builder"),
        "builderVersion": receipt.get("builderVersion"),
        "revision": receipt.get("revision"),
        "contentRootSha256": receipt.get("contentRootSha256"),
        "manifestSha256": sha256_bytes(files["catalogue/manifest.json"]),
    }
    for key, expected_value in expected.items():
        if okf[key] != expected_value:
            raise ValueError(f"publication provenance differs from catalogue receipt: {key}")
    if receipt.get("manifestSha256") != expected["manifestSha256"]:
        raise ValueError("catalogue receipt does not bind catalogue/manifest.json")


def verify_sbom(
    sbom: Any,
    *,
    payload_entries: list[dict[str, Any]],
    payload_root: str,
    repository: str,
    source_commit: str,
    version: str,
    base_path: str,
) -> None:
    document = require_keys(
        sbom,
        {"bomFormat", "specVersion", "version", "metadata", "components"},
        "SBOM",
    )
    if (
        document["bomFormat"] != "CycloneDX"
        or document["specVersion"] != "1.6"
        or document["version"] != 1
    ):
        raise ValueError("SBOM must be CycloneDX 1.6 document version 1")
    metadata = require_keys(document["metadata"], {"component", "properties"}, "SBOM metadata")
    component = require_keys(
        metadata["component"],
        {"bom-ref", "type", "name", "version", "hashes", "licenses"},
        "SBOM product",
    )
    if (
        component["bom-ref"] != f"git:{repository}@{source_commit}"
        or component["type"] != "application"
        or component["name"] != "GIS AI GO public Explorer"
        or component["version"] != version
        or component["hashes"] != [{"alg": "SHA-256", "content": payload_root}]
        or component["licenses"] != [{"license": {"id": "MIT"}}]
    ):
        raise ValueError("SBOM product identity differs from the publication")
    expected_properties = [
        {"name": "gis-ai-go:base-path", "value": base_path},
        {"name": "gis-ai-go:repository", "value": repository},
        {"name": "gis-ai-go:source-commit", "value": source_commit},
    ]
    if metadata["properties"] != expected_properties:
        raise ValueError("SBOM publication properties differ from the publication")
    expected_components = []
    for item in payload_entries:
        expected_components.append(
            {
                "bom-ref": f"file:{item['path']}@sha256:{item['sha256']}",
                "type": "file",
                "name": item["path"],
                "hashes": [{"alg": "SHA-256", "content": item["sha256"]}],
                "properties": [
                    {"name": "gis-ai-go:bytes", "value": str(item["bytes"])},
                    {"name": "gis-ai-go:publication-path", "value": item["path"]},
                ],
            }
        )
    if document["components"] != expected_components:
        raise ValueError("SBOM file components differ from the complete payload inventory")


def verify_archive(
    *,
    archive_path: Path,
    checksum_path: Path,
    receipt_path: Path,
    expected_source_commit: str,
    expected_repository: str,
    expected_version: str,
    expected_base_path: str,
    expected_archive_sha256: str | None = None,
) -> dict[str, Any]:
    if expected_repository != EXPECTED_REPOSITORY or expected_base_path != EXPECTED_BASE_PATH:
        raise ValueError(
            "expected repository and base path must name the GIS AI GO Pages publication"
        )
    if not COMMIT_RE.fullmatch(expected_source_commit):
        raise ValueError("expected source commit must be a full lowercase commit")
    if expected_archive_sha256 is not None:
        require_sha256(expected_archive_sha256, "expected archive digest")

    archive_bytes = read_outer_file(archive_path, "Pages archive", MAX_ARCHIVE_BYTES)
    digest = sha256_bytes(archive_bytes)
    expected_checksum = f"{digest}  artifact.tar\n".encode()
    checksum_bytes = read_outer_file(checksum_path, "Pages archive checksum", MAX_METADATA_BYTES)
    if checksum_bytes != expected_checksum:
        raise ValueError("artifact.tar.sha256 does not exactly bind artifact.tar")
    if expected_archive_sha256 is not None and digest != expected_archive_sha256:
        raise ValueError("archive digest differs from the expected accepted artefact")

    try:
        receipt_bytes = read_outer_file(receipt_path, "Pages archive receipt", MAX_METADATA_BYTES)
        receipt_value = json.loads(receipt_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("archive receipt must be valid UTF-8 JSON") from error
    if canonical_json(receipt_value) != receipt_bytes:
        raise ValueError("archive receipt must use canonical JSON")
    receipt = require_keys(
        receipt_value,
        {
            "schema", "repository", "sourceCommit", "version", "basePath", "canonicalUrl",
            "payloadRootSha256", "okfContentRootSha256", "archive", "checksum", "publication",
        },
        "archive receipt",
    )
    if receipt["schema"] != "gis-ai-go.pages-archive-receipt.v1":
        raise ValueError("archive receipt schema is not recognised")
    require_identity(
        receipt,
        repository=expected_repository,
        source_commit=expected_source_commit,
        version=expected_version,
        base_path=expected_base_path,
        label="archive receipt",
    )
    require_sha256(receipt["payloadRootSha256"], "archive receipt payload root")
    require_sha256(receipt["okfContentRootSha256"], "archive receipt OKF root")
    archive = require_keys(
        receipt["archive"],
        {"path", "format", "bytes", "sha256"},
        "archive receipt archive",
    )
    expected_archive = {
        "path": "artifact.tar",
        "format": "POSIX ustar",
        "bytes": len(archive_bytes),
        "sha256": digest,
    }
    if archive != expected_archive:
        raise ValueError("archive receipt archive identity differs from artifact.tar")
    checksum = require_keys(receipt["checksum"], {"path", "sha256"}, "archive receipt checksum")
    if checksum != {"path": "artifact.tar.sha256", "sha256": sha256_bytes(checksum_bytes)}:
        raise ValueError("archive receipt checksum identity differs from artifact.tar.sha256")
    publication = require_keys(
        receipt["publication"],
        {
            "checksumsSha256",
            "manifestSha256",
            "provenanceSha256",
            "siteReceiptSha256",
            "sbomSha256",
        },
        "archive receipt publication",
    )
    for key, value in publication.items():
        require_sha256(value, f"archive receipt publication {key}")

    files = read_archive(archive_bytes)
    if not PUBLICATION_PATHS.issubset(files) or ".nojekyll" not in files:
        raise ValueError("archive is missing the fixed Pages publication files")
    if files[".nojekyll"] != b"":
        raise ValueError(".nojekyll must be an empty regular file")
    if any(path.startswith("publication/") and path not in PUBLICATION_PATHS for path in files):
        raise ValueError("archive contains an unexpected publication metadata file")

    public_rows = parse_checksum_ledger(
        files["publication/CHECKSUMS.sha256"], "publication checksums"
    )
    expected_public_paths = sorted(set(files) - {".nojekyll", "publication/CHECKSUMS.sha256"})
    if [row["path"] for row in public_rows] != expected_public_paths:
        raise ValueError("publication checksums must cover every publicly fetchable archive file")
    for row in public_rows:
        if sha256_bytes(files[row["path"]]) != row["sha256"]:
            raise ValueError(f"publication checksum mismatch: {row['path']}")

    manifest = require_keys(
        parse_json_file(files, "publication/manifest.json"),
        {
            "schema", "repository", "sourceCommit", "version", "basePath", "canonicalUrl",
            "okfContentRootSha256", "payload", "publicationFiles",
        },
        "publication manifest",
    )
    if manifest["schema"] != "gis-ai-go.pages-manifest.v1":
        raise ValueError("publication manifest schema is not recognised")
    require_identity(
        manifest,
        repository=expected_repository,
        source_commit=expected_source_commit,
        version=expected_version,
        base_path=expected_base_path,
        label="publication manifest",
    )
    payload = require_keys(
        manifest["payload"],
        {"fileCount", "rootSha256", "files"},
        "manifest payload",
    )
    payload_entries = require_file_entries(payload["files"], "manifest payload files")
    expected_payload_paths = sorted(path for path in files if not path.startswith("publication/"))
    if [item["path"] for item in payload_entries] != expected_payload_paths:
        raise ValueError("manifest payload inventory differs from archived site files")
    for item in payload_entries:
        if item != file_entry(item["path"], files[item["path"]]):
            raise ValueError(f"manifest payload metadata differs from bytes: {item['path']}")
    root_sha256 = sha256_bytes(checksum_ledger(payload_entries))
    if payload["fileCount"] != len(payload_entries) or payload["rootSha256"] != root_sha256:
        raise ValueError("manifest payload count or content root differs from the inventory")
    supporting_entries = require_file_entries(
        manifest["publicationFiles"], "manifest publication files"
    )
    expected_supporting_paths = [
        "publication/provenance.json", "publication/sbom.cdx.json", "publication/site-receipt.json"
    ]
    if [item["path"] for item in supporting_entries] != expected_supporting_paths:
        raise ValueError("manifest publication files differ from the acyclic supporting set")
    for item in supporting_entries:
        if item != file_entry(item["path"], files[item["path"]]):
            raise ValueError(f"manifest supporting metadata differs from bytes: {item['path']}")

    provenance = require_keys(
        parse_json_file(files, "publication/provenance.json"),
        {
            "schema", "repository", "sourceCommit", "version", "basePath", "canonicalUrl",
            "builder", "source", "okf", "determinism",
        },
        "publication provenance",
    )
    if provenance["schema"] != "gis-ai-go.pages-provenance.v1":
        raise ValueError("publication provenance schema is not recognised")
    require_identity(
        provenance,
        repository=expected_repository,
        source_commit=expected_source_commit,
        version=expected_version,
        base_path=expected_base_path,
        label="publication provenance",
    )
    if require_keys(provenance["builder"], {"name", "version"}, "provenance builder") != {
        "name": "scripts/package_pages.py", "version": "1.0.0"
    }:
        raise ValueError("publication provenance builder is not recognised")
    source = require_keys(
        provenance["source"],
        {"path", "fileCount", "payloadRootSha256"},
        "provenance source",
    )
    expected_source = {
        "path": "apps/public-explorer/dist",
        "fileCount": len(payload_entries),
        "payloadRootSha256": root_sha256,
    }
    if source != expected_source:
        raise ValueError("publication provenance source differs from the payload")
    okf = require_keys(
        provenance["okf"],
        {
            "buildReceiptPath",
            "builder",
            "builderVersion",
            "revision",
            "contentRootSha256",
            "manifestSha256",
        },
        "provenance OKF",
    )
    if (
        okf["buildReceiptPath"] != "catalogue/build-receipt.json"
        or not COMMIT_RE.fullmatch(okf["revision"])
        or okf["revision"] != expected_source_commit
    ):
        raise ValueError("publication provenance OKF identity is invalid")
    require_sha256(okf["contentRootSha256"], "provenance OKF content root")
    require_sha256(okf["manifestSha256"], "provenance OKF manifest")
    determinism = require_keys(
        provenance["determinism"],
        {
            "archiveFormat",
            "pathOrder",
            "uid",
            "gid",
            "userName",
            "groupName",
            "fileMode",
            "modificationTime",
            "wallClockIncluded",
        },
        "provenance determinism",
    )
    if determinism != {
        "archiveFormat": "POSIX ustar", "pathOrder": "lexicographic UTF-8 publication path",
        "uid": 0, "gid": 0, "userName": "", "groupName": "", "fileMode": "0644",
        "modificationTime": 0, "wallClockIncluded": False,
    }:
        raise ValueError("publication provenance determinism contract differs")

    site_receipt = require_keys(
        parse_json_file(files, "publication/site-receipt.json"),
        {
            "schema", "repository", "sourceCommit", "version", "basePath", "canonicalUrl",
            "fileCount", "payloadRootSha256", "okfContentRootSha256", "okfManifestSha256",
            "provenanceSha256", "sbomSha256",
        },
        "site receipt",
    )
    if site_receipt["schema"] != "gis-ai-go.pages-site-receipt.v1":
        raise ValueError("site receipt schema is not recognised")
    require_identity(
        site_receipt,
        repository=expected_repository,
        source_commit=expected_source_commit,
        version=expected_version,
        base_path=expected_base_path,
        label="site receipt",
    )
    expected_site_values = {
        "fileCount": len(payload_entries),
        "payloadRootSha256": root_sha256,
        "okfContentRootSha256": okf["contentRootSha256"],
        "okfManifestSha256": okf["manifestSha256"],
        "provenanceSha256": sha256_bytes(files["publication/provenance.json"]),
        "sbomSha256": sha256_bytes(files["publication/sbom.cdx.json"]),
    }
    for key, value in expected_site_values.items():
        if site_receipt[key] != value:
            raise ValueError(f"site receipt differs from the archived publication: {key}")

    verify_sbom(
        parse_json_file(files, "publication/sbom.cdx.json"),
        payload_entries=payload_entries,
        payload_root=root_sha256,
        repository=expected_repository,
        source_commit=expected_source_commit,
        version=expected_version,
        base_path=expected_base_path,
    )
    verify_catalogue(files, provenance, expected_version)

    if manifest["okfContentRootSha256"] != okf["contentRootSha256"]:
        raise ValueError("publication manifest OKF root differs from provenance")
    expected_outer = {
        "payloadRootSha256": root_sha256,
        "okfContentRootSha256": okf["contentRootSha256"],
    }
    for key, value in expected_outer.items():
        if receipt[key] != value:
            raise ValueError(f"archive receipt differs from the publication: {key}")
    expected_publication_digests = {
        "checksumsSha256": sha256_bytes(files["publication/CHECKSUMS.sha256"]),
        "manifestSha256": sha256_bytes(files["publication/manifest.json"]),
        "provenanceSha256": sha256_bytes(files["publication/provenance.json"]),
        "siteReceiptSha256": sha256_bytes(files["publication/site-receipt.json"]),
        "sbomSha256": sha256_bytes(files["publication/sbom.cdx.json"]),
    }
    if publication != expected_publication_digests:
        raise ValueError("archive receipt publication digests differ from artifact.tar")
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--checksum", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--expected-source-commit", required=True)
    parser.add_argument("--expected-repository", required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--expected-base-path", required=True)
    parser.add_argument("--expected-archive-sha256")
    args = parser.parse_args()
    receipt = verify_archive(
        archive_path=args.archive,
        checksum_path=args.checksum,
        receipt_path=args.receipt,
        expected_source_commit=args.expected_source_commit,
        expected_repository=args.expected_repository,
        expected_version=args.expected_version,
        expected_base_path=args.expected_base_path,
        expected_archive_sha256=args.expected_archive_sha256,
    )
    print(
        "Verified Pages archive "
        f"sha256={receipt['archive']['sha256']} files-bound={receipt['payloadRootSha256']} "
        f"source={receipt['sourceCommit']}."
    )


if __name__ == "__main__":
    main()
