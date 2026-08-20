#!/usr/bin/env python3
"""Prove that two clean, locked GIS AI GO release builds are byte-identical."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REPOSITORY = "chris-page-gov/gis-ai-go"
EXPECTED_BASE_PATH = "/gis-ai-go/"
GENERATED_ROOTS = (
    PurePosixPath("apps/public-explorer/dist"),
    PurePosixPath("apps/public-explorer/public/catalogue"),
    PurePosixPath("artifacts/okf"),
)
GENERATED_MARKERS = {
    PurePosixPath("apps/public-explorer/public/catalogue"): (
        ".explorer-generated",
        b"gis-ai-go-public-explorer-data.v1\n",
    ),
    PurePosixPath("artifacts/okf"): (
        ".okf-generated",
        b"gis-ai-go-okf-builder.v1\n",
    ),
}
RELEASE_OUTPUTS = (
    "artifact.tar",
    "artifact.tar.sha256",
    "archive-receipt.json",
)
BUILD_COMMAND = ("pnpm", "run", "build:explorer")
BUILD_TIMEOUT_SECONDS = 5 * 60
PACKAGE_TIMEOUT_SECONDS = 2 * 60
MAX_GENERATED_FILES = 10_000
MAX_GENERATED_BYTES = 128 * 1024 * 1024
MAX_RELEASE_OUTPUT_BYTES = 160 * 1024 * 1024
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
VERSION_RE = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
CHECKSUM_ROW_RE = re.compile(r"([0-9a-f]{64})  (.+)\Z")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _safe_relative_path(value: str, label: str) -> str:
    logical = PurePosixPath(value)
    if (
        not value
        or value.startswith("/")
        or "\\" in value
        or "\0" in value
        or logical.is_absolute()
        or any(part in {"", ".", ".."} for part in logical.parts)
    ):
        raise ValueError(f"unsafe {label} path: {value!r}")
    return value


def _expected_directories(files: set[str]) -> set[str]:
    directories: set[str] = set()
    for value in files:
        parts = PurePosixPath(value).parts[:-1]
        for length in range(1, len(parts) + 1):
            directories.add(PurePosixPath(*parts[:length]).as_posix())
    return directories


def _inventory_regular_tree(root: Path, label: str) -> tuple[set[str], set[str]]:
    metadata = root.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError(f"{label} root must be a real directory")

    directories: set[str] = set()
    files: set[str] = set()
    total_bytes = 0

    def visit(directory: Path, prefix: PurePosixPath | None = None) -> None:
        nonlocal total_bytes
        with os.scandir(directory) as entries:
            ordered = sorted(entries, key=lambda entry: entry.name)
        for entry in ordered:
            relative = entry.name if prefix is None else f"{prefix.as_posix()}/{entry.name}"
            _safe_relative_path(relative, label)
            entry_metadata = entry.stat(follow_symlinks=False)
            if stat.S_ISLNK(entry_metadata.st_mode):
                raise ValueError(f"{label} must not contain symbolic links: {relative}")
            if stat.S_ISDIR(entry_metadata.st_mode):
                directories.add(relative)
                visit(Path(entry.path), PurePosixPath(relative))
                continue
            if not stat.S_ISREG(entry_metadata.st_mode):
                raise ValueError(f"{label} must contain regular files only: {relative}")
            if entry_metadata.st_nlink != 1:
                raise ValueError(f"{label} must not contain hard-linked files: {relative}")
            total_bytes += entry_metadata.st_size
            if total_bytes > MAX_GENERATED_BYTES:
                raise ValueError(f"{label} exceeds {MAX_GENERATED_BYTES} bytes")
            if len(files) >= MAX_GENERATED_FILES:
                raise ValueError(f"{label} exceeds {MAX_GENERATED_FILES} files")
            files.add(relative)

    visit(root)
    return directories, files


def _parse_checksum_ledger(value: bytes, label: str) -> list[tuple[str, str]]:
    try:
        text = value.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"{label} checksum ledger must be UTF-8") from error
    if not text.endswith("\n"):
        raise ValueError(f"{label} checksum ledger must end with a newline")
    rows: list[tuple[str, str]] = []
    for line in text[:-1].split("\n"):
        match = CHECKSUM_ROW_RE.fullmatch(line)
        if match is None:
            raise ValueError(f"invalid {label} checksum row: {line!r}")
        rows.append((match.group(1), _safe_relative_path(match.group(2), label)))
    paths = [path for _, path in rows]
    if not rows or paths != sorted(paths) or len(paths) != len(set(paths)):
        raise ValueError(f"{label} checksum paths must be non-empty, unique and sorted")
    return rows


def _validate_checksum_generated_root(
    target: Path,
    *,
    label: str,
    marker_name: str,
    marker_value: bytes,
    source_commit: str,
    version: str,
) -> None:
    directories, files = _inventory_regular_tree(target, label)
    marker_path = target / marker_name
    checksum_path = target / "CHECKSUMS.sha256"
    if marker_name not in files or marker_path.read_bytes() != marker_value:
        raise ValueError(f"refusing to remove {label}: generated marker is missing or invalid")
    if "CHECKSUMS.sha256" not in files:
        raise ValueError(f"refusing to remove {label}: checksum ledger is missing")
    rows = _parse_checksum_ledger(checksum_path.read_bytes(), label)
    locked_paths = [path for _, path in rows]
    if marker_name in locked_paths or "CHECKSUMS.sha256" in locked_paths:
        raise ValueError(f"refusing to remove {label}: checksum inventory is recursive")
    expected_files = {marker_name, "CHECKSUMS.sha256", *locked_paths}
    if files != expected_files or directories != _expected_directories(expected_files):
        raise ValueError(f"refusing to remove {label}: inventory is not exactly generated")
    for expected, relative in rows:
        value = (target / relative).read_bytes()
        if sha256_bytes(value) != expected:
            raise ValueError(f"refusing to remove {label}: checksum mismatch for {relative}")

    try:
        receipt = json.loads((target / "build-receipt.json").read_bytes())
    except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"refusing to remove {label}: build receipt is invalid") from error
    if not isinstance(receipt, dict):
        raise ValueError(f"refusing to remove {label}: build receipt must be an object")
    if receipt.get("revision") != source_commit or receipt.get("version") != version:
        raise ValueError(f"refusing to remove {label}: build identity differs from this checkout")


def _load_pages_packager() -> ModuleType:
    path = ROOT / "scripts/package_pages.py"
    specification = importlib.util.spec_from_file_location("gis_ai_go_package_pages", path)
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load the canonical Pages packager")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def _validate_distribution(target: Path, source_commit: str, version: str) -> None:
    label = "Explorer distribution"
    directories, files = _inventory_regular_tree(target, label)
    packager = _load_pages_packager()
    distribution = packager.inventory_regular_files(target)
    if files != set(distribution) or directories != _expected_directories(files):
        raise ValueError("refusing to remove Explorer distribution: inventory is not exact")
    packager.require_checked_distribution(distribution, version, source_commit)


def resolve_cleanup_target(root: Path, relative: PurePosixPath | str) -> Path:
    """Resolve one exact generated root without following repository symlinks."""
    logical = PurePosixPath(relative)
    if logical not in GENERATED_ROOTS:
        raise ValueError(f"cleanup target is not allowlisted: {logical.as_posix()}")
    root_metadata = root.lstat()
    if stat.S_ISLNK(root_metadata.st_mode) or not stat.S_ISDIR(root_metadata.st_mode):
        raise ValueError("repository root must be a real directory")

    current = root
    for part in logical.parts[:-1]:
        current = current / part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            return root.joinpath(*logical.parts)
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise ValueError(f"cleanup parent must be a real directory: {current}")
    return root.joinpath(*logical.parts)


def clean_generated_roots(root: Path, source_commit: str, version: str) -> list[str]:
    """Validate every present root first, then remove only the fixed generated roots."""
    if not COMMIT_RE.fullmatch(source_commit):
        raise ValueError("source commit must be a full lower-case Git commit")
    if not VERSION_RE.fullmatch(version):
        raise ValueError("version must be a stable semantic version")
    targets: list[tuple[PurePosixPath, Path]] = []
    for relative in GENERATED_ROOTS:
        target = resolve_cleanup_target(root, relative)
        if not target.exists() and not target.is_symlink():
            continue
        metadata = target.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise ValueError(f"refusing to remove non-directory generated root: {relative}")
        if relative == GENERATED_ROOTS[0]:
            _validate_distribution(target, source_commit, version)
        else:
            marker_name, marker_value = GENERATED_MARKERS[relative]
            _validate_checksum_generated_root(
                target,
                label=relative.as_posix(),
                marker_name=marker_name,
                marker_value=marker_value,
                source_commit=source_commit,
                version=version,
            )
        targets.append((relative, target))

    if targets and not shutil.rmtree.avoids_symlink_attacks:
        raise RuntimeError("secure generated-root cleanup is unavailable on this platform")
    removed: list[str] = []
    for relative, target in targets:
        metadata = target.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise ValueError(f"generated root changed before cleanup: {relative}")
        shutil.rmtree(target)
        if target.exists() or target.is_symlink():
            raise RuntimeError(f"generated root remains after cleanup: {relative}")
        removed.append(relative.as_posix())
    return removed


def _release_output_bytes(root: Path) -> dict[str, bytes]:
    metadata = root.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError("release output root must be a real directory")
    actual = {path.name for path in root.iterdir()}
    expected = set(RELEASE_OUTPUTS)
    if actual != expected:
        raise ValueError(
            "release output inventory must be exactly the three canonical files; "
            f"missing={sorted(expected - actual)}; extra={sorted(actual - expected)}"
        )
    values: dict[str, bytes] = {}
    for name in RELEASE_OUTPUTS:
        path = root / name
        file_metadata = path.lstat()
        if (
            stat.S_ISLNK(file_metadata.st_mode)
            or not stat.S_ISREG(file_metadata.st_mode)
            or file_metadata.st_nlink != 1
        ):
            raise ValueError(f"release output must be an ordinary single-link file: {name}")
        if file_metadata.st_size > MAX_RELEASE_OUTPUT_BYTES:
            raise ValueError(f"release output exceeds {MAX_RELEASE_OUTPUT_BYTES} bytes: {name}")
        values[name] = path.read_bytes()
    return values


def compare_release_outputs(first: Path, second: Path) -> dict[str, str]:
    """Require exact inventories and byte equality for all three release outputs."""
    first_values = _release_output_bytes(first)
    second_values = _release_output_bytes(second)
    differences = [
        name for name in RELEASE_OUTPUTS if first_values[name] != second_values[name]
    ]
    if differences:
        detail = ", ".join(
            f"{name} ({sha256_bytes(first_values[name])} != "
            f"{sha256_bytes(second_values[name])})"
            for name in differences
        )
        raise ValueError(f"clean release builds are not byte-identical: {detail}")
    return {name: sha256_bytes(first_values[name]) for name in RELEASE_OUTPUTS}


def _run(command: list[str] | tuple[str, ...], *, root: Path, timeout: int) -> None:
    environment = os.environ.copy()
    environment.update(
        {
            "CI": "1",
            "LANG": "C",
            "LC_ALL": "C",
            "SOURCE_DATE_EPOCH": "0",
            "TZ": "UTC",
        }
    )
    subprocess.run(command, cwd=root, check=True, env=environment, timeout=timeout)


def _git_head(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    value = result.stdout.strip()
    if not COMMIT_RE.fullmatch(value):
        raise ValueError("Git HEAD is not a full lower-case commit")
    return value


def _package(root: Path, output: Path, source_commit: str, version: str) -> None:
    _run(
        [
            sys.executable,
            "scripts/package_pages.py",
            "--dist",
            "apps/public-explorer/dist",
            "--output-dir",
            str(output),
            "--source-commit",
            source_commit,
            "--repository",
            EXPECTED_REPOSITORY,
            "--version",
            version,
            "--base-path",
            EXPECTED_BASE_PATH,
        ],
        root=root,
        timeout=PACKAGE_TIMEOUT_SECONDS,
    )


def check_release_reproducibility(root: Path = ROOT) -> dict[str, str]:
    source_commit = _git_head(root)
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not VERSION_RE.fullmatch(version):
        raise ValueError("VERSION must contain one stable semantic version")

    with tempfile.TemporaryDirectory(prefix="gis-ai-go-release-reproducibility-") as temporary:
        outputs: list[Path] = []
        for build_number in (1, 2):
            removed = clean_generated_roots(root, source_commit, version)
            print(
                f"Starting clean release build {build_number}/2; "
                f"removed={','.join(removed) if removed else 'none'}.",
                flush=True,
            )
            _run(BUILD_COMMAND, root=root, timeout=BUILD_TIMEOUT_SECONDS)
            output = Path(temporary) / f"build-{build_number}"
            _package(root, output, source_commit, version)
            outputs.append(output)
        digests = compare_release_outputs(outputs[0], outputs[1])

    print(
        "Two clean locked builds produced byte-identical release outputs: "
        + ", ".join(f"{name}=sha256:{digests[name]}" for name in RELEASE_OUTPUTS)
        + ".",
        flush=True,
    )
    return digests


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    check_release_reproducibility()


if __name__ == "__main__":
    main()
