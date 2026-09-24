#!/usr/bin/env python3
"""Package verified tracked source for the separate LOCAL-214 evaluation edition."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import re
import subprocess
import tarfile
from pathlib import Path, PurePosixPath

if __package__:
    from scripts.scan_secrets import BANNED_NAMES, PATTERNS
else:
    from scan_secrets import BANNED_NAMES, PATTERNS

ROOT = Path(__file__).resolve().parents[1]
EDITION = "v0.2.0-local.1"
IDENTITY = "local214-source-identity.json"
ARCHIVE = f"gis-ai-go-{EDITION}-source.tar.gz"
MAX_FILES = 4096
MAX_FILE_BYTES = 32 * 1024 * 1024
MAX_TOTAL_BYTES = 128 * 1024 * 1024
GENERATED = {
    ".git", ".venv", ".uv-cache", ".pnpm-store", "node_modules", "dist",
    "dist-hosted", "artifacts", "__pycache__", ".pytest_cache", ".ruff_cache",
    ".mypy_cache", "coverage", "test-results", "playwright-report",
}
LOCKFILES = ("pnpm-lock.yaml", "uv.lock")
GENERATED_PATHS = {
    "apps/public-explorer/public/catalogue", "apps/webmcp-explorer/public/catalogue",
}


def serialise(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_object(kind: str, content: bytes) -> str:
    return hashlib.sha1(f"{kind} {len(content)}\0".encode() + content).hexdigest()


def tree_identity(materials: list[dict]) -> str:
    tree: dict = {}
    for item in materials:
        parts = source_path(item["path"]).parts
        directory = tree
        for part in parts[:-1]:
            directory = directory.setdefault(part, {})
            if not isinstance(directory, dict):
                raise ValueError("Conflicting source tree paths")
        if parts[-1] in directory:
            raise ValueError("Duplicate source tree path")
        directory[parts[-1]] = (item["mode"], item["git_blob"])

    def encode(directory: dict) -> str:
        records = []
        for name, entry in directory.items():
            is_tree = isinstance(entry, dict)
            mode, identity = ("40000", encode(entry)) if is_tree else entry
            records.append((name.encode() + (b"/" if is_tree else b""),
                            mode.encode() + b" " + name.encode() + b"\0" + bytes.fromhex(identity)))
        return git_object("tree", b"".join(record for _, record in sorted(records)))

    return encode(tree)


def git(root: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=root, capture_output=True, check=True, timeout=60,
    ).stdout


def source_path(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if (path.is_absolute() or str(path) != name or not path.parts
            or any(part in {".", ".."} or part in GENERATED for part in path.parts)
            or "\\" in name or any(ord(char) < 32 for char in name)
            or path.name in BANNED_NAMES
            or (path.name.startswith(".env.") and path.name != ".env.example")):
        raise ValueError("Source contains a prohibited path")
    return path


def scan_bytes(name: str, content: bytes) -> None:
    # Match the existing baseline scanner; this is not an exhaustive disclosure audit.
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return
    for label, pattern in PATTERNS.items():
        if pattern.search(text):
            raise ValueError(f"{name}: baseline scan found possible {label}")


def capture_source(root: Path) -> tuple[dict, dict[str, bytes]]:
    if git(root, "status", "--porcelain", "--untracked-files=all"):
        raise ValueError("Package only a clean committed source checkout")
    commit = git(root, "rev-parse", "HEAD").decode().strip()
    tree = git(root, "rev-parse", "HEAD^{tree}").decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Source must use a full SHA-1 Git commit identity")
    entries = []
    for record in git(root, "ls-tree", "-rlz", "HEAD").split(b"\0"):
        if not record:
            continue
        header, raw_name = record.split(b"\t", 1)
        mode, kind, object_id, length = header.split()
        name = raw_name.decode("utf-8")
        source_path(name)
        if mode not in {b"100644", b"100755"} or kind != b"blob" or name == IDENTITY:
            raise ValueError("Only regular tracked source files may be packaged")
        size = int(length)
        if size > MAX_FILE_BYTES:
            raise ValueError("Source file exceeds the packaging bound")
        entries.append((name, mode.decode(), object_id.decode(), size))
    if not entries or len(entries) > MAX_FILES or sum(row[3] for row in entries) > MAX_TOTAL_BYTES:
        raise ValueError("Source inventory exceeds the packaging bound")
    request = "".join(f"{row[2]}\n" for row in entries).encode()
    batch = subprocess.run(
        ["git", "cat-file", "--batch"], input=request, cwd=root,
        capture_output=True, check=True, timeout=60,
    ).stdout
    stream = io.BytesIO(batch)
    files, materials = {}, []
    for name, mode, object_id, size in entries:
        if stream.readline() != f"{object_id} blob {size}\n".encode():
            raise ValueError("Git returned an inconsistent source object")
        content = stream.read(size)
        if len(content) != size or stream.read(1) != b"\n":
            raise ValueError("Git source object is incomplete")
        scan_bytes(name, content)
        files[name] = content
        materials.append({"path": name, "mode": mode, "bytes": size,
                          "sha256": digest(content), "git_blob": object_id})
    if stream.read(1):
        raise ValueError("Git returned surplus source data")
    if any(name not in files for name in (*LOCKFILES, "package.json", "scripts/start-local-candidate")):
        raise ValueError("Source is missing a required local-edition input")
    if git(root, "rev-parse", "HEAD").decode().strip() != commit or git(
        root, "status", "--porcelain", "--untracked-files=all"
    ):
        raise ValueError("Source changed during packaging")
    identity = {
        "schema": "gis-ai-go.local214-source-identity.v1", "edition": EDITION,
        "source_commit": commit, "source_tree": tree,
        "source_commit_object": git(root, "cat-file", "commit", commit).decode("utf-8"),
        "software_version": json.loads(files["package.json"])["version"],
        "materials": sorted(materials, key=lambda item: item["path"]),
        "lockfiles": {name: digest(files[name]) for name in LOCKFILES},
        "boundary": {"source_only": True, "attested": False,
                     "supported_public_release": False, "provider_calls": False},
    }
    return identity, files


def make_archive(identity: dict, files: dict[str, bytes]) -> bytes:
    contents = {**files, IDENTITY: serialise(identity)}
    modes = {row["path"]: int(row["mode"], 8) & 0o777 for row in identity["materials"]}
    output = io.BytesIO()
    # Fixed header metadata produces the same bytes for the same source and format.
    with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
            for name in sorted(contents):
                item = tarfile.TarInfo(f"gis-ai-go-{EDITION}/{name}")
                item.size, item.mode, item.mtime = len(contents[name]), modes.get(name, 0o644), 0
                archive.addfile(item, io.BytesIO(contents[name]))
    return output.getvalue()


def package(root: Path, destination: Path) -> dict:
    root = root.resolve(strict=True)
    parent = destination.parent.resolve(strict=True)
    destination = parent / destination.name
    if destination.is_relative_to(root):
        raise ValueError("Write packages outside the source checkout")
    identity, files = capture_source(root)
    archive = make_archive(identity, files)
    manifest = {
        "schema": "gis-ai-go.local214-source-package.v1",
        "edition": EDITION, "source_commit": identity["source_commit"],
        "source_tree": identity["source_tree"], "software_version": identity["software_version"],
        "archive": {"path": ARCHIVE, "bytes": len(archive), "sha256": digest(archive)},
        "source_identity_sha256": digest(serialise(identity)),
        "source_files": len(files), "lockfiles": identity["lockfiles"],
        "boundary": identity["boundary"],
    }
    destination.mkdir(mode=0o700)  # Never overwrite an existing package or symlink.
    payloads = {ARCHIVE: archive, "local214-package-manifest.json": serialise(manifest)}
    payloads["SHA256SUMS"] = "".join(
        f"{digest(data)}  {name}\n" for name, data in sorted(payloads.items())
    ).encode()
    for name, data in payloads.items():
        with (destination / name).open("xb") as output:
            output.write(data)
    return manifest


def verify(root: Path) -> dict:
    """Check extracted maintained bytes; installed/generated directories are not attested."""
    root = root.resolve(strict=True)
    identity_path = root / IDENTITY
    if (identity_path.is_symlink() or not identity_path.is_file()
            or identity_path.stat().st_size > 4 * 1024 * 1024):
        raise ValueError("Source identity must be a bounded regular file")
    identity = json.loads(identity_path.read_bytes())
    if (identity.get("schema") != "gis-ai-go.local214-source-identity.v1"
            or identity.get("edition") != EDITION
            or not re.fullmatch(r"[0-9a-f]{40}", identity.get("source_commit", ""))):
        raise ValueError("Unrecognised source identity")
    materials = identity.get("materials")
    if not isinstance(materials, list) or not 0 < len(materials) <= MAX_FILES:
        raise ValueError("Invalid source inventory")
    commit_bytes = identity.get("source_commit_object", "").encode("utf-8")
    if (git_object("commit", commit_bytes) != identity["source_commit"]
            or commit_bytes.split(b"\n", 1)[0] != f"tree {identity.get('source_tree')}".encode()
            or tree_identity(materials) != identity.get("source_tree")):
        raise ValueError("Source inventory does not reconstruct the named Git commit")
    names, total = set(), 0
    for item in materials:
        name = str(source_path(item["path"]))
        if name in names or item["mode"] not in {"100644", "100755"}:
            raise ValueError("Duplicate or unsupported source material")
        names.add(name)
        path = root / name
        component = path
        while component != root:
            if component.is_symlink():
                raise ValueError("Source material follows a symlink")
            component = component.parent
        size = path.stat().st_size
        total += size
        if size != item["bytes"] or size > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
            raise ValueError("Source byte inventory differs")
        data = path.read_bytes()
        blob = git_object("blob", data)
        if digest(data) != item["sha256"] or blob != item["git_blob"]:
            raise ValueError(f"Changed source material: {name}")
        if (path.stat().st_mode & 0o111 != 0) != (item["mode"] == "100755"):
            raise ValueError(f"Changed executable mode: {name}")
    for name in LOCKFILES:
        if name not in names or digest((root / name).read_bytes()) != identity["lockfiles"][name]:
            raise ValueError("Changed source lockfile")
    for directory, folders, filenames in os.walk(root, followlinks=False):
        base = Path(directory)
        folders[:] = [name for name in folders if name not in GENERATED
                      and (base / name).relative_to(root).as_posix() not in GENERATED_PATHS]
        for name in folders:
            if (base / name).is_symlink():
                raise ValueError("Unexpected source directory symlink")
        for name in filenames:
            relative = (base / name).relative_to(root).as_posix()
            if relative not in names | {IDENTITY} and name != ".DS_Store":
                raise ValueError(f"Unexpected source file: {relative}")
    return identity


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("package", "verify"))
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--revision-only", action="store_true")
    args = parser.parse_args()
    if args.command == "package":
        if args.revision_only:
            parser.error("--revision-only is only available for verify")
        if args.output_dir is None:
            parser.error("package requires --output-dir pointing to a new directory")
        result = package(args.root, args.output_dir)
    else:
        if args.output_dir is not None:
            parser.error("verify does not accept --output-dir")
        result = verify(args.root)
        result = {key: result[key] for key in ("schema", "edition", "source_commit", "source_tree")}
        if args.revision_only:
            print(result["source_commit"])
            return
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
