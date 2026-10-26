#!/usr/bin/env python3
"""Package the checked full-Explorer distribution without buffering its payload."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import stat
import subprocess
import tarfile
import tempfile
from pathlib import Path
from typing import Any, BinaryIO

try:
    import verify_explorer_pages_archive as verifier
except ModuleNotFoundError:
    from scripts import verify_explorer_pages_archive as verifier

ROOT = Path(__file__).resolve().parents[1]
PIN_PATH = ROOT / "config/explorer-publication.json"
BUILDER_VERSION = "2.0.0"
OUTPUT_NAMES = {"artifact.tar", "artifact.tar.sha256", "archive-receipt.json"}
_DIR_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
_READ_FLAGS = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
RETAIN = verifier.PUBLICATION_PATHS | {verifier.DISTRIBUTION, "explorer/okf-explorer-build-manifest.json", "gis/explorer/okf-explorer.json", "gis/explorer/context/manifest.json", "gis/explorer/projection-manifest.json"}


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _open_root(path: Path) -> int:
    before = path.lstat()
    if not stat.S_ISDIR(before.st_mode) or stat.S_ISLNK(before.st_mode):
        raise ValueError("distribution root must be a real directory")
    descriptor = os.open(path, _DIR_FLAGS)
    opened = os.fstat(descriptor)
    if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
        os.close(descriptor)
        raise ValueError("distribution root changed while opened")
    return descriptor


def inventory_distribution(root: Path) -> tuple[list[dict[str, Any]], dict[str, bytes]]:
    rows: list[dict[str, Any]] = []
    retained: dict[str, bytes] = {}
    total = retained_total = 0
    directory_count = 0
    def visit(descriptor: int, prefix: str) -> None:
        nonlocal total, retained_total, directory_count
        directory_count += 1
        if directory_count > verifier.MAX_FILES:
            raise ValueError("distribution directory count exceeds its ceiling")
        with os.scandir(descriptor) as directory:
            names = sorted(entry.name for entry in directory)
        for name in names:
            logical = prefix + name
            metadata = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
            if stat.S_ISDIR(metadata.st_mode):
                verifier.safe_path(logical + ("/explorer/file" if logical == "gis" else "/file"))
                child = os.open(name, _DIR_FLAGS, dir_fd=descriptor)
                try:
                    opened = os.fstat(child)
                    if (opened.st_dev, opened.st_ino) != (metadata.st_dev, metadata.st_ino):
                        raise ValueError("distribution directory changed while opened")
                    visit(child, logical + "/")
                finally:
                    os.close(child)
                continue
            verifier.safe_path(logical)
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1 or metadata.st_size > verifier.MAX_FILE_BYTES:
                raise ValueError(f"distribution requires bounded single-link regular files: {logical}")
            if logical.startswith("publication/") or logical == ".nojekyll":
                raise ValueError("distribution must not supply publication metadata")
            total += metadata.st_size
            if total > verifier.MAX_TOTAL_BYTES or len(rows) >= verifier.MAX_FILES - 6:
                raise ValueError("distribution exceeds its aggregate byte/file ceiling")
            child = os.open(name, _READ_FLAGS, dir_fd=descriptor)
            try:
                opened = os.fstat(child)
                if (opened.st_dev, opened.st_ino, opened.st_size) != (metadata.st_dev, metadata.st_ino, metadata.st_size) or not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1:
                    raise ValueError(f"distribution file changed while opened: {logical}")
                hashed = hashlib.sha256()
                chunks = []
                count = 0
                while chunk := os.read(child, verifier.CHUNK_BYTES):
                    count += len(chunk)
                    if count > metadata.st_size:
                        raise ValueError(f"distribution file grew while read: {logical}")
                    hashed.update(chunk)
                    if logical in RETAIN:
                        chunks.append(chunk)
                after = os.fstat(child)
                if count != metadata.st_size or (after.st_size, after.st_mtime_ns, after.st_ctime_ns) != (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns):
                    raise ValueError(f"distribution file changed while read: {logical}")
                rows.append({"path": logical, "bytes": count, "sha256": hashed.hexdigest()})
                if logical in RETAIN:
                    retained_total += count
                    if retained_total > verifier.MAX_RETAINED_METADATA_BYTES:
                        raise ValueError("distribution retained metadata exceeds its byte ceiling")
                    retained[logical] = b"".join(chunks)
            finally:
                os.close(child)
    descriptor = _open_root(root)
    try:
        visit(descriptor, "")
    finally:
        os.close(descriptor)
    if not rows:
        raise ValueError("distribution must not be empty")
    return sorted(rows, key=lambda row: row["path"]), retained


def _open_relative(root_descriptor: int, logical: str) -> BinaryIO:
    parts = logical.split("/")
    descriptor = os.dup(root_descriptor)
    try:
        for part in parts[:-1]:
            child = os.open(part, _DIR_FLAGS, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        file_descriptor = os.open(parts[-1], _READ_FLAGS, dir_fd=descriptor)
        metadata = os.fstat(file_descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            os.close(file_descriptor)
            raise ValueError(f"archive source is no longer an ordinary file: {logical}")
        return os.fdopen(file_descriptor, "rb")
    finally:
        os.close(descriptor)


class _HashingReader:
    def __init__(self, source: BinaryIO) -> None:
        self.source = source
        self.hashed = hashlib.sha256()
        self.count = 0

    def read(self, size: int = -1) -> bytes:
        value = self.source.read(size)
        self.hashed.update(value)
        self.count += len(value)
        return value


def _entry(path: str, value: bytes) -> dict[str, Any]:
    return {"path": path, "bytes": len(value), "sha256": sha256(value)}


def _descriptor_directory(descriptor: int) -> Path:
    """Use the OS descriptor namespace to keep temporary paths parent-pinned."""
    opened = os.fstat(descriptor)
    for namespace in ("/proc/self/fd", "/dev/fd"):
        candidate = Path(namespace) / str(descriptor)
        try:
            named = candidate.stat()
        except OSError:
            continue
        if stat.S_ISDIR(named.st_mode) and (named.st_dev, named.st_ino) == (opened.st_dev, opened.st_ino):
            return candidate
    raise ValueError("the full-Explorer archive builder requires a directory descriptor namespace")


def _ledger(rows: list[dict[str, Any]]) -> bytes:
    return "".join(f"{row['sha256']}  {row['path']}\n" for row in sorted(rows, key=lambda item: item["path"])).encode()


def build_archive(*, dist: Path, output_dir: Path, source_commit: str,
    repository: str, version: str, base_path: str) -> dict[str, Any]:
    if repository != verifier.REPOSITORY or base_path != verifier.BASE_PATH or not verifier.COMMIT_RE.fullmatch(source_commit) or not verifier.VERSION_RE.fullmatch(version):
        raise ValueError("full-Explorer Pages publication identity is invalid")
    if version != (ROOT / "VERSION").read_text().strip() or source_commit != subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip():
        raise ValueError("publication must bind the checked-out HEAD and VERSION")
    if output_dir.resolve() == dist.resolve() or output_dir.resolve().is_relative_to(dist.resolve()):
        raise ValueError("archive output must not be inside the distribution")
    expected_output_identity = None
    if output_dir.exists() or output_dir.is_symlink():
        metadata = output_dir.lstat()
        if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode) or any(output_dir.iterdir()):
            raise ValueError("archive output must be a new or empty real directory")
        expected_output_identity = (metadata.st_dev, metadata.st_ino)
    parent_descriptor = _open_root(output_dir.parent)
    os.close(parent_descriptor)
    rows, retained = inventory_distribution(dist)
    if verifier.DISTRIBUTION not in retained:
        raise ValueError("distribution identity manifest is missing")
    expected = {"repository": repository, "sourceCommit": source_commit, "version": version, "basePath": base_path, "canonicalUrl": verifier.CANONICAL_URL}
    distribution = verifier.json_bytes(retained[verifier.DISTRIBUTION], "distribution")
    verifier.verify_distribution(distribution, rows, retained, expected)
    pin = json.loads(PIN_PATH.read_bytes())
    if (pin.get("sourceCommit") != distribution["app"]["sourceCommit"]
        or pin.get("appTreeSha256") != distribution["app"]["treeSha256"]
        or pin.get("appManifestSha256") != distribution["app"]["manifestSha256"]
        or pin.get("canonicalUrl") != expected["canonicalUrl"]
        or pin.get("basePath") != expected["basePath"]):
        raise ValueError("distribution differs from the checked Explorer publication pin")
    payload = sorted([*rows, _entry(".nojekyll", b"")], key=lambda row: row["path"])
    payload_root = sha256(_ledger(payload))
    components = [{"bom-ref": f"file:{row['path']}@sha256:{row['sha256']}", "type": "file", "name": row["path"], "hashes": [{"alg": "SHA-256", "content": row["sha256"]}], "properties": [{"name": "gis-ai-go:bytes", "value": str(row["bytes"])}]} for row in payload]
    sbom = canonical_json({"bomFormat": "CycloneDX", "specVersion": "1.6", "version": 1,
        "metadata": {"component": {"type": "application", "name": "GIS AI GO full OKF Explorer", "version": version, "hashes": [{"alg": "SHA-256", "content": payload_root}], "licenses": [{"license": {"id": "MIT"}}]}}, "components": components})
    provenance = canonical_json({"schema": "gis-ai-go.pages-provenance.v2", **expected,
        "app": distribution["app"], "okf": distribution["okf"],
        "builder": {"name": "scripts/package_explorer_pages.py", "version": BUILDER_VERSION},
        "source": {"path": "artifacts/explorer-pages-dist", "fileCount": len(payload), "payloadRootSha256": payload_root},
        "determinism": {"archiveFormat": "POSIX ustar", "pathOrder": "lexicographic UTF-8 publication path", "uid": 1000, "gid": 1000, "userName": "", "groupName": "", "fileMode": "0644", "modificationTime": 0, "wallClockIncluded": False}})
    descriptor_digest = next(row["sha256"] for row in rows if row["path"] == distribution["okf"]["descriptorPath"])
    site = canonical_json({"schema": "gis-ai-go.pages-site-receipt.v2", **expected,
        "app": distribution["app"], "okf": distribution["okf"], "fileCount": len(payload),
        "payloadRootSha256": payload_root, "okfContentRootSha256": distribution["okf"]["inputDigest"],
        "okfManifestSha256": descriptor_digest, "provenanceSha256": sha256(provenance), "sbomSha256": sha256(sbom)})
    extra = {".nojekyll": b"", "publication/provenance.json": provenance,
        "publication/site-receipt.json": site, "publication/sbom.cdx.json": sbom}
    supporting = sorted([_entry(path, raw) for path, raw in extra.items() if path != ".nojekyll"], key=lambda row: row["path"])
    manifest = canonical_json({"schema": "gis-ai-go.pages-manifest.v2", **expected,
        "app": distribution["app"], "okf": distribution["okf"],
        "okfContentRootSha256": distribution["okf"]["inputDigest"],
        "payload": {"fileCount": len(payload), "rootSha256": payload_root, "files": payload},
        "publicationFiles": supporting})
    extra["publication/manifest.json"] = manifest
    public_rows = sorted([*rows, *[_entry(path, raw) for path, raw in extra.items() if path != ".nojekyll"]], key=lambda row: row["path"])
    checksums = _ledger(public_rows)
    extra["publication/CHECKSUMS.sha256"] = checksums
    archive_rows = sorted([*rows, *[_entry(path, raw) for path, raw in extra.items()]], key=lambda row: row["path"])
    if len(archive_rows) > verifier.MAX_FILES or sum(row["bytes"] for row in archive_rows) > verifier.MAX_TOTAL_BYTES or any(row["bytes"] > verifier.MAX_FILE_BYTES for row in archive_rows):
        raise ValueError("complete served publication exceeds its byte/file ceilings")
    root_descriptor = _open_root(dist)
    parent_descriptor = _open_root(output_dir.parent)
    parent_identity = os.fstat(parent_descriptor)
    output_descriptor = None
    try:
        with tempfile.TemporaryDirectory(prefix=".explorer-pages-archive-", dir=_descriptor_directory(parent_descriptor)) as temporary:
            stage = Path(temporary)
            archive_path = stage / "artifact.tar"
            with tarfile.open(archive_path, mode="w", format=tarfile.USTAR_FORMAT) as archive:
                for row in archive_rows:
                    member = tarfile.TarInfo("./" + row["path"])
                    member.size = row["bytes"]
                    member.uid = member.gid = 1000
                    member.uname = member.gname = ""
                    member.mode = 0o644
                    member.mtime = 0
                    member.type = tarfile.REGTYPE
                    source = io.BytesIO(extra[row["path"]]) if row["path"] in extra else _open_relative(root_descriptor, row["path"])
                    with source:
                        reader = _HashingReader(source)
                        archive.addfile(member, reader)
                        if reader.count != row["bytes"] or reader.hashed.hexdigest() != row["sha256"] or source.read(1):
                            raise ValueError(f"distribution changed while archived: {row['path']}")
            if inventory_distribution(dist)[0] != rows:
                raise ValueError("distribution inventory changed while archived")
            archive_hash, archive_size = verifier.archive_digest(archive_path)
            checksum = f"{archive_hash}  artifact.tar\n".encode()
            receipt = {"schema": verifier.SCHEMA, **expected, "payloadRootSha256": payload_root,
                "okfContentRootSha256": distribution["okf"]["inputDigest"],
                "archive": {"path": "artifact.tar", "format": "POSIX ustar", "bytes": archive_size, "sha256": archive_hash},
                "checksum": {"path": "artifact.tar.sha256", "sha256": sha256(checksum)},
                "publication": {"checksumsSha256": sha256(checksums), "manifestSha256": sha256(manifest), "provenanceSha256": sha256(provenance), "siteReceiptSha256": sha256(site), "sbomSha256": sha256(sbom)}}
            (stage / "artifact.tar.sha256").write_bytes(checksum)
            (stage / "archive-receipt.json").write_bytes(canonical_json(receipt))
            verifier.verify_archive(archive_path=archive_path, checksum_path=stage / "artifact.tar.sha256", receipt_path=stage / "archive-receipt.json", expected_source_commit=source_commit, expected_repository=repository, expected_version=version, expected_base_path=base_path, expected_archive_sha256=archive_hash)
            if expected_output_identity is None:
                os.mkdir(output_dir.name, 0o700, dir_fd=parent_descriptor)
                named = os.stat(output_dir.name, dir_fd=parent_descriptor, follow_symlinks=False)
                expected_output_identity = (named.st_dev, named.st_ino)
            output_descriptor = os.open(output_dir.name, _DIR_FLAGS, dir_fd=parent_descriptor)
            opened_output = os.fstat(output_descriptor)
            if (opened_output.st_dev, opened_output.st_ino) != expected_output_identity or os.listdir(output_descriptor):
                raise ValueError("archive output changed before publication")
            stage_descriptor = _open_root(stage)
            try:
                for name in sorted(OUTPUT_NAMES):
                    # linkat is atomic and refuses an existing name; unlike a
                    # path-based rename it cannot follow a replaced output dir
                    # or overwrite a file that appeared during publication.
                    os.link(name, name, src_dir_fd=stage_descriptor, dst_dir_fd=output_descriptor, follow_symlinks=False)
                    os.unlink(name, dir_fd=stage_descriptor)
            finally:
                os.close(stage_descriptor)
            if set(os.listdir(output_descriptor)) != OUTPUT_NAMES:
                raise ValueError("archive output inventory changed during publication")
            anchored_output = _descriptor_directory(output_descriptor)
            if verifier.archive_digest(anchored_output / "artifact.tar") != (archive_hash, archive_size) or verifier.read_bounded(anchored_output / "artifact.tar.sha256", verifier.MAX_RECEIPT_BYTES) != checksum or verifier.read_bounded(anchored_output / "archive-receipt.json", verifier.MAX_RECEIPT_BYTES) != canonical_json(receipt):
                raise ValueError("published archive bytes differ from the checked candidate")
            named_parent = output_dir.parent.lstat()
            named_output = os.stat(output_dir.name, dir_fd=parent_descriptor, follow_symlinks=False)
            if not stat.S_ISDIR(named_parent.st_mode) or stat.S_ISLNK(named_parent.st_mode) or (named_parent.st_dev, named_parent.st_ino) != (parent_identity.st_dev, parent_identity.st_ino) or not stat.S_ISDIR(named_output.st_mode) or (named_output.st_dev, named_output.st_ino) != expected_output_identity:
                raise ValueError("archive output directory changed during publication")
            os.fchmod(output_descriptor, 0o755)
    finally:
        if output_descriptor is not None:
            os.close(output_descriptor)
        os.close(parent_descriptor)
        os.close(root_descriptor)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    for name in ("source-commit", "repository", "version", "base-path"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    receipt = build_archive(dist=args.dist, output_dir=args.output_dir, source_commit=args.source_commit, repository=args.repository, version=args.version, base_path=args.base_path)
    print(f"Built full Explorer Pages archive sha256={receipt['archive']['sha256']} bytes={receipt['archive']['bytes']} source={receipt['sourceCommit']}.")


if __name__ == "__main__":
    main()
