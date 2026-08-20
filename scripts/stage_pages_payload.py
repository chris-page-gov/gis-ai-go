#!/usr/bin/env python3
"""Safely stage the exact logical files from a verified Pages source archive."""

from __future__ import annotations

import argparse
import os
import stat
from pathlib import Path
from typing import Any

import verify_pages_archive as verifier


_DIRECTORY_FLAGS = (
    os.O_RDONLY
    | getattr(os, "O_CLOEXEC", 0)
    | getattr(os, "O_DIRECTORY", 0)
    | getattr(os, "O_NOFOLLOW", 0)
)
_READ_FLAGS = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
_WRITE_FLAGS = (
    os.O_WRONLY
    | os.O_CREAT
    | os.O_EXCL
    | getattr(os, "O_CLOEXEC", 0)
    | getattr(os, "O_NOFOLLOW", 0)
)
_FILE_MODE = 0o644
_DIRECTORY_MODE = 0o755

Identity = tuple[int, int]


def _identity(metadata: os.stat_result) -> Identity:
    return metadata.st_dev, metadata.st_ino


def _require_same_identity(
    metadata: os.stat_result,
    expected: Identity,
    label: str,
) -> None:
    if _identity(metadata) != expected:
        raise ValueError(f"{label} changed while the Pages payload was staged")


def _open_real_directory(path: Path, label: str) -> tuple[int, Identity]:
    try:
        before = path.lstat()
    except FileNotFoundError as error:
        raise ValueError(f"{label} must already exist as a real directory") from error
    if stat.S_ISLNK(before.st_mode) or not stat.S_ISDIR(before.st_mode):
        raise ValueError(f"{label} must already exist as a real directory")
    try:
        descriptor = os.open(path, _DIRECTORY_FLAGS)
    except OSError as error:
        raise ValueError(f"{label} could not be opened safely") from error
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISDIR(opened.st_mode):
            raise ValueError(f"{label} must be a real directory")
        _require_same_identity(opened, _identity(before), label)
        return descriptor, _identity(opened)
    except Exception:
        os.close(descriptor)
        raise


def _existing_output_error(parent_descriptor: int, name: str) -> ValueError:
    try:
        metadata = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
    except FileNotFoundError:
        return ValueError("output directory changed while it was created")
    if stat.S_ISLNK(metadata.st_mode):
        return ValueError("output directory must not be a symbolic link")
    return ValueError("output directory must not already exist")


def _create_output_directory(
    output_dir: Path,
) -> tuple[int, Identity, int, Identity, str]:
    name = output_dir.name
    if not name or name in {".", ".."}:
        raise ValueError("output directory must name a new child directory")
    parent = output_dir.parent
    parent_descriptor, parent_identity = _open_real_directory(
        parent, "output directory parent"
    )
    try:
        try:
            os.mkdir(name, 0o700, dir_fd=parent_descriptor)
        except FileExistsError as error:
            raise _existing_output_error(parent_descriptor, name) from error
        try:
            created = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
            if not stat.S_ISDIR(created.st_mode) or stat.S_ISLNK(created.st_mode):
                raise ValueError("new output directory is not a real directory")
            output_descriptor = os.open(name, _DIRECTORY_FLAGS, dir_fd=parent_descriptor)
        except Exception:
            raise
        try:
            opened = os.fstat(output_descriptor)
            if not stat.S_ISDIR(opened.st_mode):
                raise ValueError("new output directory is not a real directory")
            _require_same_identity(opened, _identity(created), "output directory")
            os.fchmod(output_descriptor, _DIRECTORY_MODE)
            return (
                parent_descriptor,
                parent_identity,
                output_descriptor,
                _identity(opened),
                name,
            )
        except Exception:
            os.close(output_descriptor)
            raise
    except Exception:
        os.close(parent_descriptor)
        raise


def _open_child_directory(
    parent_descriptor: int,
    name: str,
    logical_parts: tuple[str, ...],
    directory_identities: dict[tuple[str, ...], Identity],
) -> int:
    expected = directory_identities.get(logical_parts)
    if expected is None:
        try:
            os.mkdir(name, _DIRECTORY_MODE, dir_fd=parent_descriptor)
        except FileExistsError as error:
            logical = "/".join(logical_parts)
            raise ValueError(f"staging directory appeared unexpectedly: {logical}") from error
        created = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
        if not stat.S_ISDIR(created.st_mode) or stat.S_ISLNK(created.st_mode):
            logical = "/".join(logical_parts)
            raise ValueError(f"staging path is not a real directory: {logical}")
        expected = _identity(created)
        directory_identities[logical_parts] = expected
    try:
        descriptor = os.open(name, _DIRECTORY_FLAGS, dir_fd=parent_descriptor)
    except OSError as error:
        logical = "/".join(logical_parts)
        raise ValueError(f"staging directory could not be opened safely: {logical}") from error
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISDIR(opened.st_mode):
            raise ValueError(f"staging path is not a directory: {'/'.join(logical_parts)}")
        _require_same_identity(opened, expected, f"staging directory {'/'.join(logical_parts)}")
        if stat.S_IMODE(opened.st_mode) != _DIRECTORY_MODE:
            os.fchmod(descriptor, _DIRECTORY_MODE)
        return descriptor
    except Exception:
        os.close(descriptor)
        raise


def _write_all(descriptor: int, value: bytes) -> None:
    view = memoryview(value)
    while view:
        written = os.write(descriptor, view)
        if written <= 0:
            raise OSError("write returned no progress")
        view = view[written:]


def _write_regular_file(
    root_descriptor: int,
    logical_path: str,
    value: bytes,
    directory_identities: dict[tuple[str, ...], Identity],
    file_identities: dict[str, Identity],
) -> None:
    parts = tuple(logical_path.split("/"))
    current_descriptor = os.dup(root_descriptor)
    try:
        prefix: tuple[str, ...] = ()
        for part in parts[:-1]:
            prefix = (*prefix, part)
            child_descriptor = _open_child_directory(
                current_descriptor,
                part,
                prefix,
                directory_identities,
            )
            os.close(current_descriptor)
            current_descriptor = child_descriptor

        name = parts[-1]
        try:
            file_descriptor = os.open(
                name,
                _WRITE_FLAGS,
                0o600,
                dir_fd=current_descriptor,
            )
        except FileExistsError as error:
            raise ValueError(f"staging file appeared unexpectedly: {logical_path}") from error
        except OSError as error:
            raise ValueError(f"staging file could not be created safely: {logical_path}") from error
        try:
            opened = os.fstat(file_descriptor)
            if not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1:
                raise ValueError(f"staging file is not a single-link regular file: {logical_path}")
            os.fchmod(file_descriptor, _FILE_MODE)
            _write_all(file_descriptor, value)
            completed = os.fstat(file_descriptor)
            if completed.st_size != len(value):
                raise ValueError(f"staging file byte count differs: {logical_path}")
            file_identity = _identity(completed)
        finally:
            os.close(file_descriptor)

        named = os.stat(name, dir_fd=current_descriptor, follow_symlinks=False)
        if (
            not stat.S_ISREG(named.st_mode)
            or named.st_nlink != 1
            or stat.S_IMODE(named.st_mode) != _FILE_MODE
        ):
            raise ValueError(f"staging file metadata differs: {logical_path}")
        _require_same_identity(named, file_identity, f"staging file {logical_path}")
        file_identities[logical_path] = file_identity
    finally:
        os.close(current_descriptor)


def _read_all(descriptor: int) -> bytes:
    chunks: list[bytes] = []
    while True:
        chunk = os.read(descriptor, 1024 * 1024)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


def _inventory_directory(
    descriptor: int,
    logical_parts: tuple[str, ...],
    directory_identities: dict[tuple[str, ...], Identity],
    file_identities: dict[str, Identity],
    observed_directories: set[tuple[str, ...]],
    observed_files: dict[str, bytes],
) -> None:
    opened = os.fstat(descriptor)
    expected_directory = directory_identities.get(logical_parts)
    if expected_directory is None:
        raise ValueError(f"unexpected staging directory: {'/'.join(logical_parts)}")
    _require_same_identity(
        opened,
        expected_directory,
        f"staging directory {'/'.join(logical_parts) or '.'}",
    )
    if not stat.S_ISDIR(opened.st_mode) or stat.S_IMODE(opened.st_mode) != _DIRECTORY_MODE:
        raise ValueError(f"staging directory metadata differs: {'/'.join(logical_parts) or '.'}")
    observed_directories.add(logical_parts)

    with os.scandir(descriptor) as entries:
        ordered = sorted(entries, key=lambda entry: os.fsencode(entry.name))
    for entry in ordered:
        name = entry.name
        if name in {"", ".", ".."} or "/" in name or "\0" in name:
            raise ValueError(f"unsafe staged entry name: {name!r}")
        child_parts = (*logical_parts, name)
        metadata = entry.stat(follow_symlinks=False)
        if stat.S_ISDIR(metadata.st_mode):
            expected = directory_identities.get(child_parts)
            if expected is None:
                raise ValueError(f"unexpected staging directory: {'/'.join(child_parts)}")
            _require_same_identity(
                metadata,
                expected,
                f"staging directory {'/'.join(child_parts)}",
            )
            child_descriptor = _open_child_directory(
                descriptor,
                name,
                child_parts,
                directory_identities,
            )
            try:
                _inventory_directory(
                    child_descriptor,
                    child_parts,
                    directory_identities,
                    file_identities,
                    observed_directories,
                    observed_files,
                )
            finally:
                os.close(child_descriptor)
            continue
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            logical_path = "/".join(child_parts)
            raise ValueError(f"staging tree contains a link or special file: {logical_path}")
        logical_path = "/".join(child_parts)
        expected_file = file_identities.get(logical_path)
        if expected_file is None:
            raise ValueError(f"unexpected staging file: {logical_path}")
        _require_same_identity(metadata, expected_file, f"staging file {logical_path}")
        if stat.S_IMODE(metadata.st_mode) != _FILE_MODE:
            raise ValueError(f"staging file mode differs: {logical_path}")
        try:
            file_descriptor = os.open(name, _READ_FLAGS, dir_fd=descriptor)
        except OSError as error:
            raise ValueError(
                f"staging file could not be reopened safely: {logical_path}"
            ) from error
        try:
            reopened = os.fstat(file_descriptor)
            if not stat.S_ISREG(reopened.st_mode) or reopened.st_nlink != 1:
                raise ValueError(f"staging file is not a regular file: {logical_path}")
            _require_same_identity(reopened, expected_file, f"staging file {logical_path}")
            observed_files[logical_path] = _read_all(file_descriptor)
        finally:
            os.close(file_descriptor)


def _assert_named_output_identity(
    output_dir: Path,
    parent_descriptor: int,
    parent_identity: Identity,
    output_name: str,
    output_identity: Identity,
) -> None:
    parent_metadata = output_dir.parent.lstat()
    if stat.S_ISLNK(parent_metadata.st_mode) or not stat.S_ISDIR(parent_metadata.st_mode):
        raise ValueError("output directory parent changed while the Pages payload was staged")
    _require_same_identity(parent_metadata, parent_identity, "output directory parent")
    named = os.stat(output_name, dir_fd=parent_descriptor, follow_symlinks=False)
    if stat.S_ISLNK(named.st_mode) or not stat.S_ISDIR(named.st_mode):
        raise ValueError("output directory changed while the Pages payload was staged")
    _require_same_identity(named, output_identity, "output directory")


def materialise_files(files: dict[str, bytes], output_dir: Path) -> dict[str, bytes]:
    """Write verified logical files to a newly created, descriptor-pinned directory."""
    if not files:
        raise ValueError("verified Pages payload must contain at least one file")
    for logical_path in files:
        verifier.safe_archive_path(logical_path)

    (
        parent_descriptor,
        parent_identity,
        output_descriptor,
        output_identity,
        output_name,
    ) = _create_output_directory(output_dir)
    directory_identities: dict[tuple[str, ...], Identity] = {(): output_identity}
    file_identities: dict[str, Identity] = {}
    try:
        for logical_path in sorted(files, key=os.fsencode):
            _write_regular_file(
                output_descriptor,
                logical_path,
                files[logical_path],
                directory_identities,
                file_identities,
            )

        observed_directories: set[tuple[str, ...]] = set()
        observed_files: dict[str, bytes] = {}
        _inventory_directory(
            output_descriptor,
            (),
            directory_identities,
            file_identities,
            observed_directories,
            observed_files,
        )
        if observed_directories != set(directory_identities):
            raise ValueError("staged directory inventory differs from the verified payload")
        if observed_files != files:
            raise ValueError("staged file inventory or bytes differ from the verified payload")
        _assert_named_output_identity(
            output_dir,
            parent_descriptor,
            parent_identity,
            output_name,
            output_identity,
        )
        return observed_files
    finally:
        os.close(output_descriptor)
        os.close(parent_descriptor)


def stage_payload(
    *,
    archive_path: Path,
    checksum_path: Path,
    receipt_path: Path,
    output_dir: Path,
    expected_source_commit: str,
    expected_repository: str,
    expected_version: str,
    expected_base_path: str,
    expected_archive_sha256: str,
) -> dict[str, Any]:
    """Verify an accepted source archive, then stage its exact logical bytes."""
    receipt = verifier.verify_archive(
        archive_path=archive_path,
        checksum_path=checksum_path,
        receipt_path=receipt_path,
        expected_source_commit=expected_source_commit,
        expected_repository=expected_repository,
        expected_version=expected_version,
        expected_base_path=expected_base_path,
        expected_archive_sha256=expected_archive_sha256,
    )
    archive_bytes = verifier.read_outer_file(
        archive_path,
        "Pages archive",
        verifier.MAX_ARCHIVE_BYTES,
    )
    archive_sha256 = verifier.sha256_bytes(archive_bytes)
    if (
        archive_sha256 != expected_archive_sha256
        or archive_sha256 != receipt["archive"]["sha256"]
    ):
        raise ValueError("Pages archive changed after verification")
    files = verifier.read_archive(archive_bytes)
    observed = materialise_files(files, output_dir)
    return {
        "archiveSha256": archive_sha256,
        "payloadRootSha256": receipt["payloadRootSha256"],
        "fileCount": len(observed),
        "outputDir": str(output_dir),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--checksum", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-source-commit", required=True)
    parser.add_argument("--expected-repository", required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--expected-base-path", required=True)
    parser.add_argument("--expected-archive-sha256", required=True)
    args = parser.parse_args()
    staged = stage_payload(
        archive_path=args.archive,
        checksum_path=args.checksum,
        receipt_path=args.receipt,
        output_dir=args.output_dir,
        expected_source_commit=args.expected_source_commit,
        expected_repository=args.expected_repository,
        expected_version=args.expected_version,
        expected_base_path=args.expected_base_path,
        expected_archive_sha256=args.expected_archive_sha256,
    )
    print(
        "Staged verified Pages payload "
        f"archive-sha256={staged['archiveSha256']} "
        f"payload-root-sha256={staged['payloadRootSha256']} "
        f"files={staged['fileCount']} output={staged['outputDir']}."
    )


if __name__ == "__main__":
    main()
