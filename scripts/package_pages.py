#!/usr/bin/env python3
"""Build the deterministic, immutable GIS AI GO GitHub Pages archive."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import stat
import subprocess
import tarfile
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REPOSITORY = "chris-page-gov/gis-ai-go"
EXPECTED_BASE_PATH = "/gis-ai-go/"
CANONICAL_URL = "https://chris-page-gov.github.io/gis-ai-go/"
BUILDER_VERSION = "1.0.0"
MAX_FILE_BYTES = 32 * 1024 * 1024
MAX_TOTAL_BYTES = 128 * 1024 * 1024
MAX_FILES = 10_000
OUTPUT_NAMES = {"artifact.tar", "artifact.tar.sha256", "archive-receipt.json"}
PUBLICATION_PATHS = {
    "publication/CHECKSUMS.sha256",
    "publication/manifest.json",
    "publication/provenance.json",
    "publication/site-receipt.json",
    "publication/sbom.cdx.json",
}
REQUIRED_CATALOGUE_PATHS = {
    "build-receipt.json",
    "manifest.json",
    "okf-bundle.json",
    "okf-bundle.jsonld",
    "okf-explorer.json",
}
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
VERSION_RE = re.compile(
    r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?\Z"
)


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_entry(path: str, value: bytes) -> dict[str, Any]:
    return {"path": path, "bytes": len(value), "sha256": sha256_bytes(value)}


def safe_relative_path(value: str) -> str:
    logical = PurePosixPath(value)
    if (
        not value
        or value.startswith("/")
        or "\\" in value
        or "\0" in value
        or logical.is_absolute()
        or any(part in {"", ".", ".."} for part in logical.parts)
    ):
        raise ValueError(f"unsafe publication path: {value!r}")
    lowered = value.casefold()
    forbidden_parts = {".git", "docs", "node_modules", "publication", "research"}
    if (
        any(part.casefold() in forbidden_parts for part in logical.parts)
        or "research-pack" in lowered
        or lowered.endswith(".map")
    ):
        raise ValueError(f"forbidden or non-public distribution path: {value}")
    hidden = [part for part in logical.parts if part.startswith(".")]
    if hidden and value != "catalogue/.explorer-generated":
        raise ValueError(f"unexpected hidden distribution path: {value}")
    return value


def inventory_regular_files(root: Path) -> dict[str, bytes]:
    try:
        root_metadata = root.lstat()
    except FileNotFoundError as error:
        raise ValueError(f"distribution does not exist: {root}") from error
    if stat.S_ISLNK(root_metadata.st_mode) or not stat.S_ISDIR(root_metadata.st_mode):
        raise ValueError("distribution root must be a real directory")

    files: dict[str, bytes] = {}
    total_bytes = 0

    def visit(directory: Path, prefix: PurePosixPath | None = None) -> None:
        nonlocal total_bytes
        with os.scandir(directory) as entries:
            ordered = sorted(entries, key=lambda entry: entry.name)
        for entry in ordered:
            relative = entry.name if prefix is None else f"{prefix.as_posix()}/{entry.name}"
            safe_relative_path(relative)
            metadata = entry.stat(follow_symlinks=False)
            if stat.S_ISLNK(metadata.st_mode):
                raise ValueError(f"distribution must not contain symbolic links: {relative}")
            if stat.S_ISDIR(metadata.st_mode):
                visit(Path(entry.path), PurePosixPath(relative))
                continue
            if not stat.S_ISREG(metadata.st_mode):
                raise ValueError(f"distribution must contain regular files only: {relative}")
            if metadata.st_nlink != 1:
                raise ValueError(f"distribution must not contain hard-linked files: {relative}")
            if metadata.st_size > MAX_FILE_BYTES:
                raise ValueError(f"distribution file exceeds {MAX_FILE_BYTES} bytes: {relative}")
            total_bytes += metadata.st_size
            if total_bytes > MAX_TOTAL_BYTES:
                raise ValueError(f"distribution exceeds {MAX_TOTAL_BYTES} bytes")
            if len(files) >= MAX_FILES:
                raise ValueError(f"distribution exceeds {MAX_FILES} files")
            files[relative] = Path(entry.path).read_bytes()

    visit(root)
    if not files:
        raise ValueError("distribution must not be empty")
    return files


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
        rows.append({"sha256": match.group(1), "path": safe_relative_path(match.group(2))})
    paths = [row["path"] for row in rows]
    if not rows or paths != sorted(paths) or len(paths) != len(set(paths)):
        raise ValueError(f"{label} paths must be non-empty, unique and sorted")
    return rows


class _References(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.values: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name.casefold() in {"href", "src"} and value and not value.startswith("#"):
                self.values.append(value)


def html_references(value: bytes) -> set[str]:
    try:
        text = value.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("Explorer index must be UTF-8") from error
    parser = _References()
    parser.feed(text)
    references: set[str] = set()
    for raw in parser.values:
        split = urlsplit(raw)
        if split.scheme or split.netloc or raw.startswith("/") or raw.startswith("//"):
            raise ValueError(f"Explorer index contains a non-relative reference: {raw}")
        path = unquote(split.path)
        if path.startswith("./"):
            path = path[2:]
        if not path:
            continue
        references.add(safe_relative_path(path))
    return references


def require_checked_distribution(
    files: dict[str, bytes], version: str, source_commit: str
) -> dict[str, Any]:
    for required in {
        "index.html",
        "favicon.svg",
        "catalogue/.explorer-generated",
        "catalogue/CHECKSUMS.sha256",
    }:
        if required not in files:
            raise ValueError(f"checked distribution is missing {required}")
    if files["catalogue/.explorer-generated"] != b"gis-ai-go-public-explorer-data.v1\n":
        raise ValueError("Explorer catalogue marker is not recognised")

    catalogue_rows = parse_checksum_ledger(
        files["catalogue/CHECKSUMS.sha256"], "catalogue checksum ledger"
    )
    catalogue_paths = {
        path.removeprefix("catalogue/")
        for path in files
        if path.startswith("catalogue/")
    }
    expected_catalogue = {
        ".explorer-generated",
        "CHECKSUMS.sha256",
        *(row["path"] for row in catalogue_rows),
    }
    if catalogue_paths != expected_catalogue:
        raise ValueError("distributed catalogue inventory differs from its checksum ledger")
    for row in catalogue_rows:
        path = f"catalogue/{row['path']}"
        if sha256_bytes(files[path]) != row["sha256"]:
            raise ValueError(f"distributed catalogue checksum mismatch: {row['path']}")
    if not REQUIRED_CATALOGUE_PATHS.issubset({row["path"] for row in catalogue_rows}):
        missing = sorted(REQUIRED_CATALOGUE_PATHS - {row["path"] for row in catalogue_rows})
        raise ValueError(f"distributed catalogue is missing required files: {missing}")

    references = html_references(files["index.html"])
    expected_files = {
        "index.html",
        *(path for path in files if path.startswith("catalogue/")),
        *references,
    }
    if "favicon.svg" not in references:
        raise ValueError("Explorer index must reference favicon.svg")
    if set(files) != expected_files:
        missing = sorted(expected_files - set(files))
        extra = sorted(set(files) - expected_files)
        raise ValueError(f"distribution inventory is not exact; missing={missing}; extra={extra}")

    try:
        receipt = json.loads(files["catalogue/build-receipt.json"])
        catalogue_manifest = json.loads(files["catalogue/manifest.json"])
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("catalogue receipt and manifest must be valid UTF-8 JSON") from error
    if not isinstance(receipt, dict) or not isinstance(catalogue_manifest, dict):
        raise ValueError("catalogue receipt and manifest must be JSON objects")
    for field in (
        "builder",
        "builderVersion",
        "revision",
        "contentRootSha256",
        "manifestSha256",
        "version",
    ):
        if not isinstance(receipt.get(field), str) or not receipt[field]:
            raise ValueError(f"catalogue build receipt requires string field {field}")
    if not COMMIT_RE.fullmatch(receipt["revision"]):
        raise ValueError("catalogue build receipt revision must be a full commit")
    if receipt["revision"] != source_commit:
        raise ValueError(
            "catalogue build receipt revision differs from the publication source commit"
        )
    if not SHA256_RE.fullmatch(receipt["contentRootSha256"]):
        raise ValueError("catalogue build receipt content root is invalid")
    actual_manifest_sha = sha256_bytes(files["catalogue/manifest.json"])
    if receipt["manifestSha256"] != actual_manifest_sha:
        raise ValueError("catalogue build receipt does not bind catalogue/manifest.json")
    if receipt["version"] != version:
        raise ValueError("catalogue build receipt version differs from the publication version")
    return {
        "builder": receipt["builder"],
        "builderVersion": receipt["builderVersion"],
        "revision": receipt["revision"],
        "contentRootSha256": receipt["contentRootSha256"],
        "manifestSha256": actual_manifest_sha,
    }


def validate_identity(repository: str, source_commit: str, version: str, base_path: str) -> None:
    if repository != EXPECTED_REPOSITORY:
        raise ValueError(f"repository must be exactly {EXPECTED_REPOSITORY}")
    if base_path != EXPECTED_BASE_PATH:
        raise ValueError(f"base path must be exactly {EXPECTED_BASE_PATH}")
    if not COMMIT_RE.fullmatch(source_commit):
        raise ValueError("source commit must be a 40-character lowercase hexadecimal commit")
    if not VERSION_RE.fullmatch(version):
        raise ValueError("version must be a semantic version")
    expected_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != expected_version:
        raise ValueError(
            f"version differs from VERSION: expected {expected_version}, found {version}"
        )
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    )
    if result.stdout.strip() != source_commit:
        raise ValueError("source commit must equal the checked-out HEAD")


def checksum_ledger(entries: list[dict[str, Any]]) -> bytes:
    ordered = sorted(entries, key=lambda item: item["path"])
    return "".join(f"{item['sha256']}  {item['path']}\n" for item in ordered).encode()


def payload_root(entries: list[dict[str, Any]]) -> str:
    return sha256_bytes(checksum_ledger(entries))


def publication_sbom(
    identity: dict[str, str], payload_entries: list[dict[str, Any]], root_sha256: str
) -> bytes:
    components = []
    for item in sorted(payload_entries, key=lambda entry: entry["path"]):
        components.append(
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
    return canonical_json(
        {
            "bomFormat": "CycloneDX",
            "specVersion": "1.6",
            "version": 1,
            "metadata": {
                "component": {
                    "bom-ref": f"git:{identity['repository']}@{identity['sourceCommit']}",
                    "type": "application",
                    "name": "GIS AI GO public Explorer",
                    "version": identity["version"],
                    "hashes": [{"alg": "SHA-256", "content": root_sha256}],
                    "licenses": [{"license": {"id": "MIT"}}],
                },
                "properties": [
                    {"name": "gis-ai-go:base-path", "value": identity["basePath"]},
                    {"name": "gis-ai-go:repository", "value": identity["repository"]},
                    {"name": "gis-ai-go:source-commit", "value": identity["sourceCommit"]},
                ],
            },
            "components": components,
        }
    )


def deterministic_tar(files: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.USTAR_FORMAT) as archive:
        for path in sorted(files):
            if path != ".nojekyll" and not path.startswith("publication/"):
                safe_relative_path(path)
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


def build_archive(
    *,
    dist: Path,
    output_dir: Path,
    source_commit: str,
    repository: str,
    version: str,
    base_path: str,
) -> dict[str, Any]:
    validate_identity(repository, source_commit, version, base_path)
    dist_resolved = dist.resolve()
    output_resolved = output_dir.resolve()
    if output_resolved == dist_resolved or output_resolved.is_relative_to(dist_resolved):
        raise ValueError("output directory must not be inside the checked distribution")

    dist_files = inventory_regular_files(dist)
    okf = require_checked_distribution(dist_files, version, source_commit)
    identity = {
        "repository": repository,
        "sourceCommit": source_commit,
        "version": version,
        "basePath": base_path,
        "canonicalUrl": CANONICAL_URL,
    }
    payload_files = {**dist_files, ".nojekyll": b""}
    payload_entries = [file_entry(path, value) for path, value in sorted(payload_files.items())]
    root_sha256 = payload_root(payload_entries)

    sbom = publication_sbom(identity, payload_entries, root_sha256)
    provenance = canonical_json(
        {
            "schema": "gis-ai-go.pages-provenance.v1",
            **identity,
            "builder": {"name": "scripts/package_pages.py", "version": BUILDER_VERSION},
            "source": {
                "path": "apps/public-explorer/dist",
                "fileCount": len(payload_entries),
                "payloadRootSha256": root_sha256,
            },
            "okf": {
                "buildReceiptPath": "catalogue/build-receipt.json",
                **okf,
            },
            "determinism": {
                "archiveFormat": "POSIX ustar",
                "pathOrder": "lexicographic UTF-8 publication path",
                "uid": 0,
                "gid": 0,
                "userName": "",
                "groupName": "",
                "fileMode": "0644",
                "modificationTime": 0,
                "wallClockIncluded": False,
            },
        }
    )
    site_receipt = canonical_json(
        {
            "schema": "gis-ai-go.pages-site-receipt.v1",
            **identity,
            "fileCount": len(payload_entries),
            "payloadRootSha256": root_sha256,
            "okfContentRootSha256": okf["contentRootSha256"],
            "okfManifestSha256": okf["manifestSha256"],
            "provenanceSha256": sha256_bytes(provenance),
            "sbomSha256": sha256_bytes(sbom),
        }
    )
    supporting = {
        "publication/provenance.json": provenance,
        "publication/site-receipt.json": site_receipt,
        "publication/sbom.cdx.json": sbom,
    }
    supporting_entries = [file_entry(path, value) for path, value in sorted(supporting.items())]
    manifest = canonical_json(
        {
            "schema": "gis-ai-go.pages-manifest.v1",
            **identity,
            "okfContentRootSha256": okf["contentRootSha256"],
            "payload": {
                "fileCount": len(payload_entries),
                "rootSha256": root_sha256,
                "files": payload_entries,
            },
            "publicationFiles": supporting_entries,
        }
    )
    archive_files = {
        **payload_files,
        **supporting,
        "publication/manifest.json": manifest,
    }
    publicly_fetchable = [
        file_entry(path, value)
        for path, value in sorted(archive_files.items())
        if path != ".nojekyll"
    ]
    checksums = checksum_ledger(publicly_fetchable)
    archive_files["publication/CHECKSUMS.sha256"] = checksums
    if set(archive_files) != set(payload_files) | PUBLICATION_PATHS:
        raise AssertionError("internal publication inventory differs from the fixed contract")

    archive_bytes = deterministic_tar(archive_files)
    archive_sha256 = sha256_bytes(archive_bytes)
    archive_checksum = f"{archive_sha256}  artifact.tar\n".encode()
    receipt = {
        "schema": "gis-ai-go.pages-archive-receipt.v1",
        **identity,
        "payloadRootSha256": root_sha256,
        "okfContentRootSha256": okf["contentRootSha256"],
        "archive": {
            "path": "artifact.tar",
            "format": "POSIX ustar",
            "bytes": len(archive_bytes),
            "sha256": archive_sha256,
        },
        "checksum": {
            "path": "artifact.tar.sha256",
            "sha256": sha256_bytes(archive_checksum),
        },
        "publication": {
            "checksumsSha256": sha256_bytes(checksums),
            "manifestSha256": sha256_bytes(manifest),
            "provenanceSha256": sha256_bytes(provenance),
            "siteReceiptSha256": sha256_bytes(site_receipt),
            "sbomSha256": sha256_bytes(sbom),
        },
    }

    if output_dir.exists() or output_dir.is_symlink():
        output_metadata = output_dir.lstat()
        if stat.S_ISLNK(output_metadata.st_mode) or not stat.S_ISDIR(output_metadata.st_mode):
            raise ValueError("output directory must be a real directory")
    else:
        output_dir.mkdir(parents=True, exist_ok=False)
    unexpected = {path.name for path in output_dir.iterdir()} - OUTPUT_NAMES
    if unexpected:
        raise ValueError(f"output directory contains unexpected entries: {sorted(unexpected)}")
    for name in sorted(OUTPUT_NAMES):
        candidate = output_dir / name
        if not candidate.exists() and not candidate.is_symlink():
            continue
        metadata = candidate.lstat()
        if (
            stat.S_ISLNK(metadata.st_mode)
            or not stat.S_ISREG(metadata.st_mode)
            or metadata.st_nlink != 1
        ):
            raise ValueError(f"existing output must be an ordinary single-link file: {name}")
    (output_dir / "artifact.tar").write_bytes(archive_bytes)
    (output_dir / "artifact.tar.sha256").write_bytes(archive_checksum)
    (output_dir / "archive-receipt.json").write_bytes(canonical_json(receipt))
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--base-path", required=True)
    args = parser.parse_args()
    receipt = build_archive(
        dist=args.dist,
        output_dir=args.output_dir,
        source_commit=args.source_commit,
        repository=args.repository,
        version=args.version,
        base_path=args.base_path,
    )
    print(
        "Built deterministic Pages archive "
        f"sha256={receipt['archive']['sha256']} bytes={receipt['archive']['bytes']} "
        f"source={receipt['sourceCommit']}."
    )


if __name__ == "__main__":
    main()
