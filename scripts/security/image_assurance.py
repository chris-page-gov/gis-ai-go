#!/usr/bin/env python3
"""Offline, fail-closed assurance of a supplied immutable OCI image archive.

This command never acquires tools or databases. Its receipt covers this image and
this vulnerability database only; it grants no source, deployment or identity
acceptance. Outputs must be outside this checkout (including its build contexts).
Each scanner is bounded to 2 CPUs, 6 GiB memory, 256 processes and a 4 GiB
temporary filesystem. Run images sequentially on constrained hosts.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import datetime as dt
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tarfile
import threading
import uuid
from typing import Any, BinaryIO


SYFT_VERSION = "1.42.2"
TRIVY_VERSION = "0.74.0"
SYFT_REFERENCE = "anchore/syft:v1.42.2@sha256:15952b4306fd990724afaaf7f1c71fcd03546b89fbf6f2d32b0be5f81e3ef431"
TRIVY_REFERENCE = "aquasec/trivy:0.74.0@sha256:62b1e65e8869bc4b4c6aa4fa2b21595256c7c2f6018a9d9ad61caf87187c1969"
DOCKER = ("docker", "--host=unix:///var/run/docker.sock")
ROOT = Path(__file__).resolve().parents[2]
MAX_ARCHIVE = 8 * 1024**3
MAX_EXPANDED = 32 * 1024**3
MAX_OUTER_FILES = 100_000
MAX_JSON = 16 * 1024**2
MAX_REPORT = 256 * 1024**2
MAX_DB = 2 * 1024**3
MAX_LAYER_ENTRIES = 1_000_000
MAX_DIAGNOSTIC = 1024**2
SCANNER_TMPFS = 4 * 1024**3
SCANNER_MEMORY = 6 * 1024**3
IMAGE_INDEX = "application/vnd.oci.image.index.v1+json"
IMAGE_MANIFEST = "application/vnd.oci.image.manifest.v1+json"
IMAGE_CONFIG = "application/vnd.oci.image.config.v1+json"
EMPTY_CONFIG = "application/vnd.oci.empty.v1+json"
DOCKER_INDEX = "application/vnd.docker.distribution.manifest.list.v2+json"
DOCKER_MANIFEST = "application/vnd.docker.distribution.manifest.v2+json"
DOCKER_CONFIG = "application/vnd.docker.container.image.v1+json"
LAYERS = {
    "application/vnd.oci.image.layer.v1.tar": False,
    "application/vnd.oci.image.layer.v1.tar+gzip": True,
    "application/vnd.docker.image.rootfs.diff.tar.gzip": True,
}
DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
SEVERITIES = ("UNKNOWN", "LOW", "MEDIUM", "HIGH", "CRITICAL")


class Blocked(Exception):
    """A safe machine-readable gate failure, without host paths or stderr."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def require(condition: bool, code: str) -> None:
    if not condition:
        raise Blocked(code)


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "duplicate_json_key")
        result[key] = value
    return result


def parse_json(raw: bytes, maximum: int = MAX_JSON) -> Any:
    require(len(raw) <= maximum, "json_size_limit")
    try:
        return json.loads(raw, object_pairs_hook=_unique_pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(Blocked("nonfinite_json")))
    except (ValueError, UnicodeError, RecursionError):
        raise Blocked("invalid_json") from None


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n").encode()


def sha256(path: Path, maximum: int) -> str:
    total = 0
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024**2):
            total += len(chunk)
            require(total <= maximum, "file_size_limit")
            digest.update(chunk)
    return digest.hexdigest()


def safe_path(path: Path) -> Path:
    """Refuse symlink components instead of silently following caller aliases."""
    absolute = path.absolute()
    for component in (absolute, *absolute.parents):
        if component.exists() or component.is_symlink():
            require(not component.is_symlink(), "symlink_path")
    require(not any(character in str(absolute) for character in ("\n", "\r", "\0", ",", ":")),
            "unsafe_mount_path")
    return absolute


def private_output(path: Path) -> Path:
    path = safe_path(path)
    require(path != ROOT and ROOT not in path.parents, "output_inside_build_context")
    if path.exists():
        metadata = path.stat()
        require(path.is_dir() and metadata.st_uid == os.getuid()
                and not metadata.st_mode & 0o077 and not any(path.iterdir()),
                "output_not_fresh_private_directory")
    else:
        path.mkdir(parents=True, mode=0o700)
        path.chmod(0o700)
    return path


def retain(path: Path, raw: bytes) -> None:
    with path.open("xb") as stream:
        os.chmod(path, 0o600)
        stream.write(raw)


def snapshot(source: Path, target: Path, maximum: int) -> dict[str, Any]:
    source = safe_path(source)
    before = source.stat()
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and 0 < before.st_size <= maximum, "input_not_bounded_regular_file")
    digest = hashlib.sha256()
    total = 0
    with source.open("rb") as incoming, target.open("xb") as outgoing:
        os.chmod(target, 0o400)
        while chunk := incoming.read(1024**2):
            total += len(chunk)
            require(total <= maximum, "file_size_limit")
            outgoing.write(chunk)
            digest.update(chunk)
    after = source.stat()
    require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns)
            == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns)
            and total == before.st_size, "input_changed_during_snapshot")
    return {"bytes": total, "sha256": digest.hexdigest()}


def logical_name(name: str) -> str:
    require(isinstance(name, str) and 0 < len(name.encode()) <= 4096, "unsafe_oci_path")
    require(not name.startswith("/") and "\\" not in name and "\0" not in name,
            "unsafe_oci_path")
    parts = name.rstrip("/").split("/")
    require(all(part not in ("", ".", "..") for part in parts), "unsafe_oci_path")
    return PurePosixPath(*parts).as_posix()


class HashedStream:
    """Bounded decompressed stream; inner layer files are never extracted."""

    def __init__(self, source: BinaryIO, budget: list[int]):
        self.source = source
        self.budget = budget
        self.digest = hashlib.sha256()

    def read(self, count: int = -1) -> bytes:
        require(count >= 0, "unbounded_layer_read")
        raw = self.source.read(count)
        self.budget[0] += len(raw)
        require(self.budget[0] <= MAX_EXPANDED, "expanded_layer_size_limit")
        self.digest.update(raw)
        return raw


def _layer_identity(stream: BinaryIO, compressed: bool, budget: list[int],
                    passwd: bytes | None, etc_link: bool, need_passwd: bool) -> tuple[str, bytes | None, bool]:
    source = gzip.GzipFile(fileobj=stream) if compressed else stream
    reader = HashedStream(source, budget)
    with tarfile.open(fileobj=reader, mode="r|") as layer:
        for count, item in enumerate(layer):
            require(count < MAX_LAYER_ENTRIES, "layer_entry_limit")
            # Linux image layers legitimately contain symlinks. They are metadata
            # here: neither the layer nor any link target is extracted onto host.
            if not need_passwd:
                continue
            name = item.name.removeprefix("./").rstrip("/")
            # A redirected /etc cannot establish the user mapping safely.
            if name == "etc":
                etc_link = not item.isdir()
            if name in (".wh.etc", ".wh..wh..opq", "etc/.wh.passwd", "etc/.wh..wh..opq"):
                passwd = None
            if name == "etc/passwd":
                require(item.isreg() and item.size <= 1024**2, "unresolved_image_user")
                handle = layer.extractfile(item)
                require(handle is not None, "unresolved_image_user")
                passwd = handle.read(1024**2 + 1)
    while reader.read(1024**2):
        pass
    return "sha256:" + reader.digest.hexdigest(), passwd, etc_link


def inspect_oci(path: Path, expected: str) -> dict[str, Any]:
    """Validate every content-addressed blob and the complete selected closure."""
    require(bool(DIGEST.fullmatch(expected)), "invalid_expected_manifest_digest")
    try:
        with tarfile.open(path, mode="r:") as archive:
            members: dict[str, tarfile.TarInfo] = {}
            total = 0
            for member in archive:
                name = logical_name(member.name)
                require(name not in members, "duplicate_oci_entry")
                require((member.type in {tarfile.REGTYPE, tarfile.AREGTYPE} and not member.issparse())
                        or member.isdir(), "oci_link_or_special_entry")
                if member.isdir():
                    require(name in {"blobs", "blobs/sha256"}, "unknown_oci_directory")
                else:
                    require(name in {"index.json", "oci-layout", "manifest.json"}
                            or re.fullmatch(r"blobs/sha256/[0-9a-f]{64}", name) is not None,
                            "unknown_oci_entry")
                    total += member.size
                    require(member.size >= 0 and total <= MAX_ARCHIVE, "oci_size_limit")
                members[name] = member
                require(len(members) <= MAX_OUTER_FILES, "oci_entry_limit")
            require({"index.json", "oci-layout"} <= members.keys(), "missing_oci_layout")

            def read(name: str) -> bytes:
                member = members.get(name)
                require(member is not None and member.isreg() and member.size <= MAX_JSON,
                        "missing_or_oversized_oci_metadata")
                stream = archive.extractfile(member)
                require(stream is not None, "missing_oci_blob")
                return stream.read(MAX_JSON + 1)

            require(parse_json(read("oci-layout")) == {"imageLayoutVersion": "1.0.0"},
                    "invalid_oci_layout")
            blobs: set[str] = set()
            for name, member in members.items():
                if not name.startswith("blobs/") or not member.isreg():
                    continue
                handle = archive.extractfile(member)
                require(handle is not None, "missing_oci_blob")
                digest = hashlib.sha256()
                while raw := handle.read(1024**2):
                    digest.update(raw)
                require(digest.hexdigest() == name.rsplit("/", 1)[-1], "oci_blob_digest_mismatch")
                blobs.add("sha256:" + digest.hexdigest())
            used: set[str] = set()
            runtime: list[dict[str, Any]] = []
            attestations: list[dict[str, str]] = []
            visited: set[str] = set()
            selected: set[str] = set()

            def descriptor(value: Any) -> tuple[str, str]:
                require(isinstance(value, dict), "invalid_oci_descriptor")
                digest = value.get("digest")
                media = value.get("mediaType")
                size = value.get("size")
                require(isinstance(digest, str) and bool(DIGEST.fullmatch(digest))
                        and isinstance(media, str) and type(size) is int and size > 0,
                        "invalid_oci_descriptor")
                require("urls" not in value, "external_oci_descriptor")
                member = members.get("blobs/sha256/" + digest[7:])
                require(member is not None and member.isreg() and member.size == size,
                        "oci_descriptor_size_or_blob_mismatch")
                if "data" in value:
                    inline = value["data"]
                    require(isinstance(inline, str) and len(inline) <= 4 * MAX_JSON // 3 + 4,
                            "invalid_inline_oci_data")
                    try:
                        raw = base64.b64decode(inline, validate=True)
                    except (ValueError, binascii.Error):
                        raise Blocked("invalid_inline_oci_data") from None
                    require(len(raw) == size and "sha256:" + hashlib.sha256(raw).hexdigest() == digest
                            and raw == read("blobs/sha256/" + digest[7:]), "inline_oci_data_mismatch")
                used.add(digest)
                return digest, media

            def visit(value: Any, chosen: bool = False, depth: int = 0) -> None:
                require(depth <= 8 and len(visited) < 256, "oci_graph_limit")
                digest, media = descriptor(value)
                require(digest not in visited, "duplicate_or_cyclic_oci_descriptor")
                visited.add(digest)
                chosen = chosen or digest == expected
                if chosen:
                    selected.add(digest)
                obj = parse_json(read("blobs/sha256/" + digest[7:]))
                require(isinstance(obj, dict) and type(obj.get("schemaVersion")) is int and obj["schemaVersion"] == 2
                        and obj.get("mediaType", media) == media, "invalid_oci_manifest")
                if media in {IMAGE_INDEX, DOCKER_INDEX}:
                    children = obj.get("manifests")
                    require(isinstance(children, list) and 0 < len(children) <= 32,
                            "invalid_oci_index")
                    for child in children:
                        visit(child, chosen, depth + 1)
                    return
                require(media in {IMAGE_MANIFEST, DOCKER_MANIFEST}, "unsupported_oci_media_type")
                annotations = value.get("annotations", {})
                require(isinstance(annotations, dict), "invalid_oci_annotations")
                attestation = annotations.get("vnd.docker.reference.type") == "attestation-manifest"
                config_digest, config_media = descriptor(obj.get("config"))
                require(config_media in {IMAGE_CONFIG, DOCKER_CONFIG}
                        or attestation and config_media == EMPTY_CONFIG, "invalid_oci_config_media_type")
                config = parse_json(read("blobs/sha256/" + config_digest[7:]))
                require(isinstance(config, dict), "invalid_oci_config")
                require(config_media != EMPTY_CONFIG or config == {}, "invalid_empty_attestation_config")
                layers = obj.get("layers")
                require(isinstance(layers, list) and 0 < len(layers) <= 128, "invalid_oci_layers")
                if attestation:
                    target = annotations.get("vnd.docker.reference.digest")
                    require(isinstance(target, str) and bool(DIGEST.fullmatch(target)),
                            "invalid_attestation_target")
                    require(value.get("platform") == {"architecture": "unknown", "os": "unknown"},
                            "invalid_attestation_platform")
                    if "subject" in obj:
                        subject_digest, subject_media = descriptor(obj["subject"])
                        require(subject_digest == target and subject_media in {IMAGE_MANIFEST, DOCKER_MANIFEST},
                                "attestation_subject_mismatch")
                    for layer in layers:
                        _, layer_media = descriptor(layer)
                        require(layer_media == "application/vnd.in-toto+json", "invalid_attestation_layer")
                        payload = parse_json(read("blobs/sha256/" + layer["digest"][7:]))
                        require(isinstance(payload, dict) and isinstance(payload.get("subject"), list),
                                "invalid_attestation_payload")
                    attestations.append({"manifest_digest": digest, "target_manifest_digest": target})
                    return
                require(config.get("os") == "linux" and config.get("architecture") in {"amd64", "arm64"},
                        "unsupported_runtime_platform")
                platform = value.get("platform")
                if platform is not None:
                    require(isinstance(platform, dict) and platform.get("os") == config["os"]
                            and platform.get("architecture") == config["architecture"],
                            "oci_platform_mismatch")
                for layer in layers:
                    _, layer_media = descriptor(layer)
                    require(layer_media in LAYERS, "unsupported_runtime_layer_media_type")
                runtime.append({"digest": digest, "config_digest": config_digest, "config": config,
                                "layers": layers, "selected": chosen})

            index = parse_json(read("index.json"))
            require(isinstance(index, dict) and type(index.get("schemaVersion")) is int and index["schemaVersion"] == 2
                    and index.get("mediaType", IMAGE_INDEX) == IMAGE_INDEX
                    and isinstance(index.get("manifests"), list) and 0 < len(index["manifests"]) <= 32,
                    "invalid_oci_index")
            for value in index["manifests"]:
                visit(value)
            require(expected in selected, "expected_manifest_not_reachable")
            require(used == blobs, "unreachable_oci_blob")
            require(len(runtime) == 1 and runtime[0]["selected"], "ambiguous_or_unselected_runtime_image")
            image = runtime[0]
            require(all(item["target_manifest_digest"] == image["digest"] for item in attestations),
                    "attestation_targets_different_image")
            config = image["config"]
            require(isinstance(config.get("config"), dict), "invalid_runtime_config")
            user = config["config"].get("User")
            require(isinstance(user, str) and len(user) <= 128 and user and user.split(":", 1)[0] != "root",
                    "image_user_not_nonroot")
            parts = user.split(":")
            require(len(parts) <= 2 and all(re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", part) is not None
                                           for part in parts), "invalid_image_user")
            username = parts[0]
            numeric = username.isascii() and username.isdecimal()
            require(numeric or re.fullmatch(r"[a-z_][a-z0-9_-]{0,63}", username) is not None,
                    "invalid_image_user")
            uid: int | None = int(username) if numeric else None
            require(uid is None or 0 < uid <= 2**32 - 2, "image_user_not_nonroot")
            rootfs = config.get("rootfs")
            require(isinstance(rootfs, dict) and rootfs.get("type") == "layers"
                    and isinstance(rootfs.get("diff_ids"), list)
                    and len(rootfs["diff_ids"]) == len(image["layers"])
                    and all(isinstance(item, str) and bool(DIGEST.fullmatch(item)) for item in rootfs["diff_ids"]),
                    "invalid_image_diff_ids")
            budget = [0]
            passwd = None
            etc_link = False
            for layer, diff_id in zip(image["layers"], rootfs["diff_ids"], strict=True):
                handle = archive.extractfile(members["blobs/sha256/" + layer["digest"][7:]])
                require(handle is not None, "missing_runtime_layer")
                observed, passwd, etc_link = _layer_identity(handle, LAYERS[layer["mediaType"]],
                                                             budget, passwd, etc_link, not numeric)
                require(observed == diff_id, "image_diff_id_mismatch")
            if uid is None:
                require(passwd is not None and not etc_link, "unresolved_image_user")
                try:
                    rows = [line.split(":") for line in passwd.decode("utf-8").splitlines()
                            if line.split(":", 1)[0] == username]
                    require(len(rows) == 1 and len(rows[0]) == 7 and rows[0][2].isascii()
                            and rows[0][2].isdecimal(), "unresolved_image_user")
                    uid = int(rows[0][2])
                except UnicodeError:
                    raise Blocked("unresolved_image_user") from None
                require(0 < uid <= 2**32 - 2, "image_user_not_nonroot")
            if "manifest.json" in members:
                # Docker's convenience index must agree with the OCI graph.
                legacy = parse_json(read("manifest.json"))
                require(isinstance(legacy, list) and len(legacy) == 1 and isinstance(legacy[0], dict)
                        and legacy[0].get("Config") == "blobs/sha256/" + image["config_digest"][7:]
                        and legacy[0].get("Layers") == ["blobs/sha256/" + item["digest"][7:] for item in image["layers"]],
                        "docker_convenience_manifest_mismatch")
            return {"requested_manifest_digest": expected, "manifest_digest": image["digest"],
                    "config_digest": image["config_digest"], "diff_ids": rootfs["diff_ids"],
                    "platform": {"os": config["os"], "architecture": config["architecture"]},
                    "user": user, "resolved_uid": uid, "layer_count": len(image["layers"]),
                    "expanded_bytes": budget[0], "attestations": attestations,
                    "attestations_verified": False, "blob_count": len(blobs),
                    "scanner_normalization_required": not (len(index["manifests"]) == 1
                        and index["manifests"][0]["digest"] == image["digest"])}
    except (tarfile.TarError, OSError, EOFError, gzip.BadGzipFile):
        raise Blocked("invalid_oci_archive_or_layer") from None


def validate_scanner_directory(root: Path, image: dict[str, Any]) -> dict[str, Any]:
    """Recheck the closed derived OCI directory without executing image content."""
    root = safe_path(root)
    require(root.is_dir(), "invalid_scanner_directory")
    inventory: list[dict[str, Any]] = []
    total = 0
    for current, directories, files in os.walk(root, followlinks=False):
        for name in directories:
            path = Path(current) / name
            require(not path.is_symlink() and path.relative_to(root).as_posix() in {"blobs", "blobs/sha256"},
                    "invalid_scanner_directory")
        for name in files:
            path = Path(current) / name
            metadata = path.lstat()
            require(stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
                    "invalid_scanner_directory")
            logical = path.relative_to(root).as_posix()
            require(logical in {"index.json", "oci-layout"}
                    or re.fullmatch(r"blobs/sha256/[0-9a-f]{64}", logical) is not None,
                    "invalid_scanner_directory")
            total += metadata.st_size
            require(len(inventory) < MAX_OUTER_FILES and 0 < metadata.st_size <= MAX_ARCHIVE
                    and total <= MAX_ARCHIVE, "oci_size_limit")
            digest = sha256(path, MAX_ARCHIVE)
            require(not logical.startswith("blobs/") or logical.rsplit("/", 1)[-1] == digest,
                    "scanner_blob_digest_mismatch")
            inventory.append({"path": logical, "bytes": metadata.st_size, "sha256": digest})
    by_name = {item["path"]: item for item in inventory}

    def read(name: str) -> Any:
        require(name in by_name and by_name[name]["bytes"] <= MAX_JSON, "invalid_scanner_directory")
        return parse_json((root / name).read_bytes())

    def descriptor(value: Any) -> tuple[str, str]:
        require(isinstance(value, dict) and isinstance(value.get("digest"), str)
                and bool(DIGEST.fullmatch(value["digest"])) and type(value.get("size")) is int
                and isinstance(value.get("mediaType"), str) and "urls" not in value,
                "invalid_scanner_directory")
        name = "blobs/sha256/" + value["digest"][7:]
        require(name in by_name and by_name[name]["bytes"] == value["size"], "invalid_scanner_directory")
        return value["digest"], value["mediaType"]

    require(read("oci-layout") == {"imageLayoutVersion": "1.0.0"}, "invalid_scanner_directory")
    index = read("index.json")
    require(isinstance(index, dict) and type(index.get("schemaVersion")) is int and index["schemaVersion"] == 2
            and index.get("mediaType") == IMAGE_INDEX and isinstance(index.get("manifests"), list)
            and len(index["manifests"]) == 1, "invalid_scanner_directory")
    manifest_digest, media = descriptor(index["manifests"][0])
    require(manifest_digest == image["manifest_digest"] and media in {IMAGE_MANIFEST, DOCKER_MANIFEST}
            and index["manifests"][0].get("platform") == image["platform"], "normalization_binding_mismatch")
    manifest_name = "blobs/sha256/" + manifest_digest[7:]
    manifest = read(manifest_name)
    require(isinstance(manifest, dict) and manifest.get("schemaVersion") == 2
            and manifest.get("mediaType", media) == media and isinstance(manifest.get("layers"), list),
            "invalid_scanner_directory")
    config_digest, config_media = descriptor(manifest.get("config"))
    require(config_digest == image["config_digest"] and config_media in {IMAGE_CONFIG, DOCKER_CONFIG},
            "normalization_binding_mismatch")
    config_name = "blobs/sha256/" + config_digest[7:]
    config = read(config_name)
    require(isinstance(config, dict) and config.get("rootfs", {}).get("diff_ids") == image["diff_ids"]
            and config.get("config", {}).get("User") == image["user"]
            and {"os": config.get("os"), "architecture": config.get("architecture")} == image["platform"],
            "normalization_binding_mismatch")
    closed = {"index.json", "oci-layout", manifest_name, config_name}
    for layer in manifest["layers"]:
        digest, layer_media = descriptor(layer)
        require(layer_media in LAYERS, "invalid_scanner_directory")
        closed.add("blobs/sha256/" + digest[7:])
    require(set(by_name) == closed, "scanner_directory_unclosed_inventory")
    inventory.sort(key=lambda item: item["path"])
    return {"bytes": total, "files": inventory,
            "inventory_sha256": hashlib.sha256(canonical(inventory)).hexdigest()}


def normalize_scanner_directory(source: Path, target: Path, image: dict[str, Any]) -> dict[str, Any]:
    """Copy only validated SHA-addressed blobs to a private single-image OCI dir.

    Syft 1.42.2 rejects nested indexes and Trivy 0.74.0 expects an OCI directory.
    No archive path is extracted: only the already validated manifest, config and
    layer names are copied with bounded reads and rechecked content hashes. The
    original archive/index and unverified attestations remain retained authority.
    """
    try:
        with tarfile.open(source, mode="r:") as incoming:
            manifest_name = "blobs/sha256/" + image["manifest_digest"][7:]
            member = incoming.getmember(manifest_name)
            require(member.isreg() and member.size <= MAX_JSON, "invalid_normalization_source")
            stream = incoming.extractfile(member)
            require(stream is not None, "invalid_normalization_source")
            manifest = parse_json(stream.read(MAX_JSON + 1))
            require(isinstance(manifest, dict) and isinstance(manifest.get("config"), dict)
                    and manifest["config"].get("digest") == image["config_digest"]
                    and isinstance(manifest.get("layers"), list), "normalization_binding_mismatch")
            names = [manifest_name, "blobs/sha256/" + image["config_digest"][7:]]
            names.extend("blobs/sha256/" + item["digest"][7:] for item in manifest["layers"])
            descriptor = {"mediaType": manifest.get("mediaType", IMAGE_MANIFEST),
                          "digest": image["manifest_digest"], "size": member.size, "platform": image["platform"]}
            metadata = {"oci-layout": canonical({"imageLayoutVersion": "1.0.0"}),
                        "index.json": canonical({"schemaVersion": 2, "mediaType": IMAGE_INDEX,
                                                 "manifests": [descriptor]})}
            total = sum(len(raw) for raw in metadata.values())
            target.mkdir(mode=0o700)
            (target / "blobs").mkdir(mode=0o700)
            (target / "blobs/sha256").mkdir(mode=0o700)
            for name, raw in metadata.items():
                retain(target / name, raw)
                (target / name).chmod(0o400)
            for name in dict.fromkeys(names):
                original = incoming.getmember(name)
                require(original.isreg() and not original.issparse(), "invalid_normalization_source")
                total += original.size
                require(total <= MAX_ARCHIVE, "oci_size_limit")
                stream = incoming.extractfile(original)
                require(stream is not None, "invalid_normalization_source")
                digest = hashlib.sha256()
                copied = 0
                with (target / name).open("xb") as output:
                    os.chmod(target / name, 0o400)
                    while raw := stream.read(1024**2):
                        copied += len(raw)
                        require(copied <= original.size, "invalid_normalization_source")
                        digest.update(raw)
                        output.write(raw)
                require(copied == original.size and digest.hexdigest() == name.rsplit("/", 1)[-1],
                        "scanner_blob_digest_mismatch")
        return validate_scanner_directory(target, image)
    except (tarfile.TarError, OSError, KeyError, TypeError):
        raise Blocked("invalid_normalization_source") from None


def _timestamp(value: Any) -> dt.datetime:
    require(isinstance(value, str) and len(value) <= 64, "invalid_db_timestamp")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise Blocked("invalid_db_timestamp") from None
    require(parsed.tzinfo is not None and parsed.utcoffset() == dt.timedelta(0), "invalid_db_timestamp")
    return parsed


def validate_db(cache: Path, now: dt.datetime) -> dict[str, Any]:
    cache = safe_path(cache)
    require(cache.is_dir(), "missing_trivy_db")
    observed: set[str] = set()
    for current, directories, files in os.walk(cache, followlinks=False):
        for name in directories + files:
            path = Path(current) / name
            require(not path.is_symlink(), "db_symlink_or_special_file")
            if path.is_file():
                observed.add(path.relative_to(cache).as_posix())
            else:
                require(path.is_dir() and path.relative_to(cache).as_posix() == "db", "db_unclosed_inventory")
    require(observed == {"db/trivy.db", "db/metadata.json"}, "db_unclosed_inventory")
    inventory = []
    for name in sorted(observed):
        path = cache / name
        metadata = path.stat()
        require(stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1
                and 0 < metadata.st_size <= MAX_DB, "db_symlink_or_special_file")
        inventory.append({"path": name, "bytes": metadata.st_size, "sha256": sha256(path, MAX_DB)})
    require((cache / "db/metadata.json").stat().st_size <= MAX_JSON, "json_size_limit")
    metadata = parse_json((cache / "db/metadata.json").read_bytes())
    require(isinstance(metadata, dict) and type(metadata.get("Version")) is int
            and metadata["Version"] == 2, "unsupported_trivy_db_schema")
    updated = _timestamp(metadata.get("UpdatedAt"))
    next_update = _timestamp(metadata.get("NextUpdate"))
    require(dt.timedelta(0) <= now - updated < dt.timedelta(hours=24), "stale_or_future_trivy_db")
    require(next_update > now and next_update > updated, "expired_trivy_db")
    return {"schema_version": 2, "updated_at": metadata["UpdatedAt"], "next_update": metadata["NextUpdate"],
            "age_seconds": int((now - updated).total_seconds()), "files": inventory,
            "inventory_sha256": hashlib.sha256(canonical(inventory)).hexdigest()}


def docker_env() -> dict[str, str]:
    environment = os.environ.copy()
    for key in ("DOCKER_HOST", "DOCKER_CONTEXT", "DOCKER_TLS", "DOCKER_TLS_VERIFY", "DOCKER_CERT_PATH"):
        environment.pop(key, None)
    return environment


def sanitized_diagnostic(raw: bytes, arguments: list[str]) -> bytes:
    """Retain bounded failure detail without host paths or credential-shaped text."""
    text = raw.decode("utf-8", errors="replace")
    text = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)
    text = "".join(character for character in text if character in "\n\t" or ord(character) >= 32)
    for argument in arguments:
        if argument.startswith("--mount=type=bind,src="):
            source = argument.split("src=", 1)[1].split(",dst=", 1)[0]
            destination = argument.split(",dst=", 1)[1].split(",", 1)[0]
            text = text.replace(source, destination)
    text = text.replace(str(ROOT), "[checkout]")
    text = re.sub(r"(?i)(https?://)[^/@\s]+:[^/@\s]+@", r"\1[redacted]@", text)
    text = re.sub(r"(?i)\bBearer\s+[^\s,;]+", "Bearer [redacted]", text)
    text = re.sub(r"(?i)\b(authorization|token|secret|password|credential|api[_-]?key)[\"']?\s*[:=]\s*[\"']?[^\s,;\"']+",
                  r"\1=[redacted]", text)
    text = re.sub(r"\b[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\b", "[redacted-jwt]", text)
    encoded = text.encode("utf-8")
    if len(encoded) > MAX_DIAGNOSTIC:
        marker = b"\n[diagnostic truncated]\n"
        return encoded[:MAX_DIAGNOSTIC - len(marker)] + marker
    return encoded


def run_docker(arguments: list[str], timeout: int = 1200, maximum: int = MAX_REPORT,
               diagnostic: Path | None = None) -> bytes:
    """Bound execution; retain sanitised private stderr on success and failure."""
    try:
        process = subprocess.Popen([*DOCKER, *arguments], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   env=docker_env(), stdin=subprocess.DEVNULL)
    except OSError:
        if diagnostic is not None:
            retain(diagnostic, b"Docker CLI unavailable; no scanner ran.\n")
        raise Blocked("docker_unavailable") from None
    stdout: list[bytes] = []
    stderr: list[bytes] = []
    exceeded = threading.Event()

    def cleanup() -> None:
        name = next((value[7:] for value in arguments if value.startswith("--name=")), None)
        if name is not None:
            try:
                subprocess.run([*DOCKER, "container", "rm", "--force", name], timeout=30,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               stdin=subprocess.DEVNULL, env=docker_env(), check=False)
            except (OSError, subprocess.TimeoutExpired):
                pass

    def drain(pipe: BinaryIO, target: list[bytes], limit: int) -> None:
        total = 0
        while raw := pipe.read(64 * 1024):
            remaining = limit - total
            target.append(raw[:max(remaining, 0)])
            total += len(raw)
            if total > limit:
                exceeded.set()
                try:
                    process.kill()
                except ProcessLookupError:
                    pass
                break
        pipe.close()

    threads = [threading.Thread(target=drain, args=(process.stdout, stdout, maximum), daemon=True),
               threading.Thread(target=drain, args=(process.stderr, stderr, MAX_DIAGNOSTIC), daemon=True)]
    for thread in threads:
        thread.start()
    timed_out = False
    try:
        code = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        cleanup()
        timed_out = True
    finally:
        for thread in threads:
            thread.join(timeout=10)
    if diagnostic is not None:
        detail = b"".join(stderr)
        if exceeded.is_set():
            detail += b"\n[scanner output exceeded bound]\n"
        if timed_out:
            detail += b"\n[scanner execution timed out]\n"
        retain(diagnostic, sanitized_diagnostic(detail, arguments))
    require(not timed_out, "scanner_timeout")
    if exceeded.is_set() or any(thread.is_alive() for thread in threads):
        cleanup()
        raise Blocked("scanner_output_limit")
    require(code == 0, "scanner_or_preloaded_tool_unavailable")
    return b"".join(stdout)


def container(reference: str, mounts: tuple[tuple[Path, str], ...] = ()) -> list[str]:
    uid, gid = os.getuid(), os.getgid()
    require(uid > 0, "scanner_host_user_is_root")
    args = ["run", "--rm", f"--name=gis-image-assurance-{uuid.uuid4().hex}",
            "--pull=never", "--network=none", "--read-only", "--cap-drop=ALL", "--pids-limit=256",
            "--cpus=2", "--memory=6g", "--memory-swap=6g",
            "--security-opt=no-new-privileges", f"--user={uid}:{gid}",
            f"--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=4g,mode=0700,uid={uid},gid={gid}",
            "--env=SYFT_CHECK_FOR_APP_UPDATE=false", "--env=XDG_CACHE_HOME=/tmp/cache",
            "--env=XDG_CONFIG_HOME=/tmp/config"]
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "all_proxy", "no_proxy"):
        args.append(f"--env={key}=")
    for source, destination in mounts:
        args.append(f"--mount=type=bind,src={source},dst={destination},readonly")
    return [*args, reference]


def inspect_tool(reference: str, diagnostic: Path | None = None) -> dict[str, str]:
    document = parse_json(run_docker(["image", "inspect", reference], timeout=30, maximum=1024**2, diagnostic=diagnostic))
    require(isinstance(document, list) and len(document) == 1 and isinstance(document[0], dict),
            "invalid_preloaded_tool_metadata")
    image = document[0]
    expected = reference.split(":", 1)[0] + "@" + reference.split("@", 1)[1]
    require(isinstance(image.get("RepoDigests"), list) and expected in image["RepoDigests"]
            and isinstance(image.get("Id"), str) and bool(DIGEST.fullmatch(image["Id"])),
            "preloaded_tool_digest_mismatch")
    return {"reference": reference, "image_config_digest": image["Id"]}


def verify_versions(output: Path) -> dict[str, Any]:
    tools = {"syft": inspect_tool(SYFT_REFERENCE, output / "syft-inspect.stderr.txt"),
             "trivy": inspect_tool(TRIVY_REFERENCE, output / "trivy-inspect.stderr.txt")}
    syft_raw = run_docker([*container(SYFT_REFERENCE), "version", "-o", "json"], timeout=30, maximum=1024**2,
                         diagnostic=output / "syft-version.stderr.txt")
    retain(output / "syft-version.json", syft_raw)
    syft = parse_json(syft_raw)
    require(isinstance(syft, dict) and syft.get("version") == SYFT_VERSION, "syft_version_mismatch")
    trivy_raw = run_docker([*container(TRIVY_REFERENCE), "--version"], timeout=30, maximum=1024**2,
                          diagnostic=output / "trivy-version.stderr.txt")
    retain(output / "trivy-version.txt", trivy_raw)
    require(re.search(rb"(?m)^Version:\s*" + re.escape(TRIVY_VERSION.encode()) + rb"\s*$", trivy_raw) is not None,
            "trivy_version_mismatch")
    tools["syft"]["version"] = SYFT_VERSION
    tools["trivy"]["version"] = TRIVY_VERSION
    return tools


def _text(value: Any, code: str = "invalid_package_inventory") -> str:
    require(isinstance(value, str) and 0 < len(value) <= 4096
            and not any(ord(char) < 32 for char in value), code)
    return value


def validate_sbom(syft: Any, spdx: Any, image: dict[str, Any]) -> dict[str, Any]:
    require(isinstance(syft, dict) and isinstance(syft.get("descriptor"), dict)
            and syft["descriptor"].get("name") == "syft" and syft["descriptor"].get("version") == SYFT_VERSION,
            "invalid_syft_report")
    source = syft.get("source")
    require(isinstance(source, dict) and source.get("type") == "image"
            and isinstance(source.get("metadata"), dict)
            and source["metadata"].get("imageID") == image["config_digest"], "syft_image_binding_mismatch")
    packages = syft.get("artifacts")
    require(isinstance(packages, list) and 0 < len(packages) <= 1_000_000, "empty_or_invalid_syft_inventory")
    types: dict[str, int] = {}
    identities: set[tuple[str, str, str]] = set()
    package_names: dict[str, list[str]] = {}
    for package in packages:
        require(isinstance(package, dict), "invalid_package_inventory")
        name, version, kind = (_text(package.get(key)) for key in ("name", "version", "type"))
        _text(package.get("id"))
        identities.add((name, version, kind))
        types[kind] = types.get(kind, 0) + 1
        package_names.setdefault(kind, []).append(name)
    require(isinstance(spdx, dict) and spdx.get("spdxVersion") in {"SPDX-2.2", "SPDX-2.3"}
            and spdx.get("SPDXID") == "SPDXRef-DOCUMENT" and isinstance(spdx.get("creationInfo"), dict)
            and any(isinstance(value, str) and "syft" in value.lower() and SYFT_VERSION in value
                    for value in spdx["creationInfo"].get("creators", [])), "invalid_spdx_report")
    spdx_packages = spdx.get("packages")
    require(isinstance(spdx_packages, list) and len(spdx_packages) >= len(identities), "empty_or_incomplete_spdx_inventory")
    spdx_names = set()
    spdx_ids = set()
    for package in spdx_packages:
        require(isinstance(package, dict), "invalid_spdx_inventory")
        identifier = _text(package.get("SPDXID"))
        require(identifier not in spdx_ids, "duplicate_spdx_package_id")
        spdx_ids.add(identifier)
        name = _text(package.get("name"))
        version = package.get("versionInfo")
        if version is not None:
            spdx_names.add((name, _text(version)))
    require({(name, version) for name, version, _ in identities} <= spdx_names, "spdx_inventory_mismatch")
    return {"syft_packages": len(packages), "spdx_packages": len(spdx_packages), "package_types": types,
            "_package_names": package_names}


def validate_trivy(report: Any, image: dict[str, Any], sbom: dict[str, Any]) -> dict[str, Any]:
    require(isinstance(report, dict) and type(report.get("SchemaVersion")) is int and report["SchemaVersion"] == 2
            and report.get("ArtifactType") == "container_image"
            and report.get("ArtifactName") == "/input/image", "invalid_trivy_report")
    require(isinstance(report.get("ArtifactID"), str) and bool(DIGEST.fullmatch(report["ArtifactID"])),
            "invalid_trivy_artifact_id")
    metadata = report.get("Metadata")
    require(isinstance(metadata, dict) and metadata.get("ImageID") == image["config_digest"]
            and metadata.get("DiffIDs") == image["diff_ids"], "trivy_image_binding_mismatch")
    os_metadata = metadata.get("OS")
    require(isinstance(os_metadata, dict), "missing_trivy_os_inventory")
    os_family = _text(os_metadata.get("Family"), "missing_trivy_os_inventory")
    os_name = _text(os_metadata.get("Name"), "missing_trivy_os_inventory")
    results = report.get("Results")
    require(isinstance(results, list) and 0 < len(results) <= 100_000, "empty_or_invalid_trivy_results")
    counts = {severity: 0 for severity in SEVERITIES}
    result_types: dict[str, int] = {}
    packages = 0
    versioned_packages = 0
    versionless_packages = 0
    invalid_versions = 0
    os_results = 0
    os_package_names: set[str] = set()
    language_package_names: dict[str, set[str]] = {}
    for result in results:
        require(isinstance(result, dict) and isinstance(result.get("Class"), str)
                and result["Class"] in {"os-pkgs", "lang-pkgs"},
                "invalid_trivy_package_class")
        kind = _text(result.get("Type"), "invalid_trivy_package_type")
        _text(result.get("Target"), "invalid_trivy_package_target")
        result_types[kind] = result_types.get(kind, 0) + 1
        if result["Class"] == "os-pkgs":
            require(kind == os_family, "trivy_os_type_mismatch")
            os_results += 1
        inventory = result.get("Packages")
        require(isinstance(inventory, list) and 0 < len(inventory) <= 1_000_000,
                "empty_or_invalid_trivy_package_inventory")
        inventory_names = set()
        for package in inventory:
            require(isinstance(package, dict), "invalid_trivy_package_inventory")
            name = _text(package.get("Name"))
            try:
                _text(package.get("Version"))
                versioned_packages += 1
            except Blocked:
                # A real Go binary can list its unversioned main/local module.
                # Preserve fully checked vulnerability counts before blocking
                # coverage; never count this entry as a versioned package.
                invalid_versions += 1
                if package.get("Version") in (None, ""):
                    versionless_packages += 1
            inventory_names.add(name)
        packages += len(inventory)
        if result["Class"] == "os-pkgs":
            os_package_names.update(inventory_names)
        else:
            language_package_names.setdefault(kind, set()).update(inventory_names)
        vulnerabilities = result.get("Vulnerabilities", [])
        require(isinstance(vulnerabilities, list) and len(vulnerabilities) <= 1_000_000,
                "invalid_trivy_vulnerabilities")
        for finding in vulnerabilities:
            require(isinstance(finding, dict), "invalid_trivy_vulnerability")
            _text(finding.get("VulnerabilityID"), "invalid_trivy_vulnerability")
            name = _text(finding.get("PkgName"), "invalid_trivy_vulnerability")
            _text(finding.get("InstalledVersion"), "invalid_trivy_vulnerability")
            severity = finding.get("Severity")
            require(isinstance(severity, str) and severity in counts and name in inventory_names,
                    "invalid_trivy_vulnerability")
            counts[severity] += 1
    require(os_results == 1, "missing_or_duplicate_trivy_os_inventory")
    os_types = {"deb", "rpm", "apk", "alpm", "portage"}
    language_types = {"npm": {"npm", "node-pkg"}, "python": {"python-pkg"},
                      "go-module": {"gomod", "gobinary"}, "java-archive": {"jar"},
                      "gem": {"gemspec", "bundler"}, "rust-crate": {"cargo"},
                      "dotnet": {"dotnet-core"}, "composer": {"composer"},
                      "swift": {"swift"}, "dart-pub": {"pub"}, "hex": {"hex"}}
    summary = {"os": {"family": os_family, "name": os_name}, "results": len(results),
               "result_types": result_types, "packages": versioned_packages,
               "inventory_entries": packages, "versioned_packages": versioned_packages,
               "versionless_packages": versionless_packages, "invalid_package_versions": invalid_versions,
               "severity_counts": counts,
               "blocking_findings": counts["HIGH"] + counts["CRITICAL"], "coverage": "admitted_package_types"}
    try:
        require(invalid_versions == 0, "invalid_package_inventory")
        require(set(sbom["package_types"]) <= os_types | language_types.keys(),
                "unassessed_syft_package_type")
        for syft_type, trivy_types in language_types.items():
            if sbom["package_types"].get(syft_type):
                require(any(result_types.get(kind, 0) > 0 for kind in trivy_types),
                        "missing_trivy_language_inventory")
        for kind, names in sbom["_package_names"].items():
            if kind in os_types:
                require(set(names) <= os_package_names, "incomplete_trivy_os_inventory")
            elif kind in {"npm", "python", "go-module"}:
                scanned_names: set[str] = set()
                for trivy_type in language_types[kind]:
                    scanned_names.update(language_package_names.get(trivy_type, set()))
                require(set(names) <= scanned_names, "incomplete_trivy_language_inventory")
    except Blocked as error:
        summary["coverage"] = "blocked"
        error.scan_summary = summary
        raise
    return summary


def assure(archive: Path, manifest_digest: str, db_cache: Path, output_dir: Path) -> int:
    output = private_output(output_dir)
    receipt: dict[str, Any] = {
        "schema": "gis-ai-go.offline-image-assurance.v1", "status": "BLOCKED",
        "observed_at": dt.datetime.now(dt.timezone.utc).isoformat(), "network": "none",
        "acceptance_scope": "supplied OCI image and retained vulnerability database only",
        "source_acceptance": "not_assessed", "hosted_authentication": "not_assessed",
        "platform_acceptance": "not_assessed", "deployment_authorised": False,
        "tool_references": {"syft": SYFT_REFERENCE, "trivy": TRIVY_REFERENCE},
        "scanner_resources": {"cpus": 2, "memory_bytes": SCANNER_MEMORY,
                              "tmpfs_bytes": SCANNER_TMPFS, "pids": 256, "swap_bytes": 0},
    }
    code = 2
    try:
        require(os.getuid() > 0, "scanner_host_user_is_root")
        require(bool(DIGEST.fullmatch(manifest_digest)), "invalid_expected_manifest_digest")
        inputs = output / "inputs"
        inputs.mkdir(mode=0o700)
        frozen_archive = inputs / "image.oci.tar"
        receipt["archive"] = snapshot(archive, frozen_archive, MAX_ARCHIVE)
        receipt["image"] = inspect_oci(frozen_archive, manifest_digest)
        scanner_directory = inputs / "scanner-image"
        scanner_identity = normalize_scanner_directory(frozen_archive, scanner_directory, receipt["image"])
        retain(output / "scanner-input-inventory.json", canonical(scanner_identity))
        receipt["scanner_input"] = {
            "normalization": "validated_runtime_manifest_closure_directory",
            "inventory_sha256": scanner_identity["inventory_sha256"], "bytes": scanner_identity["bytes"],
            "file_count": len(scanner_identity["files"]), "evidence_path": "inputs/" + scanner_directory.name,
            "original_archive_sha256": receipt["archive"]["sha256"],
            "requested_manifest_digest": manifest_digest,
            "selected_manifest_digest": receipt["image"]["manifest_digest"],
            "config_digest": receipt["image"]["config_digest"], "diff_ids": receipt["image"]["diff_ids"],
            "attestations_included": False,
        }
        now = dt.datetime.now(dt.timezone.utc)
        source_db = validate_db(db_cache, now)
        frozen_cache = inputs / "trivy-cache"
        (frozen_cache / "db").mkdir(parents=True, mode=0o700)
        frozen_cache.chmod(0o700)
        for item in source_db["files"]:
            copied = snapshot(db_cache / item["path"], frozen_cache / item["path"], MAX_DB)
            require(copied == {"bytes": item["bytes"], "sha256": item["sha256"]}, "db_changed_during_snapshot")
        receipt["database"] = validate_db(frozen_cache, now)
        retain(output / "db-inventory.json", canonical(receipt["database"]))
        receipt["tools"] = verify_versions(output)
        mounts = ((scanner_directory, "/input/image"),)
        raw_syft = run_docker([*container(SYFT_REFERENCE, mounts), "oci-dir:/input/image",
                               "--scope=squashed", "--output=syft-json"], diagnostic=output / "syft.stderr.txt")
        retain(output / "syft.json", raw_syft)
        raw_spdx = run_docker([*container(SYFT_REFERENCE, mounts), "oci-dir:/input/image",
                               "--scope=squashed", "--output=spdx-json"], diagnostic=output / "spdx.stderr.txt")
        retain(output / "sbom.spdx.json", raw_spdx)
        sbom = validate_sbom(parse_json(raw_syft, MAX_REPORT), parse_json(raw_spdx, MAX_REPORT), receipt["image"])
        receipt["sbom"] = {key: value for key, value in sbom.items() if not key.startswith("_")}
        raw_trivy = run_docker([*container(TRIVY_REFERENCE, (*mounts, (frozen_cache, "/cache"))),
                                "image", "--input=/input/image", "--cache-dir=/cache",
                                "--cache-backend=memory", "--scanners=vuln",
                                "--severity=UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL", "--format=json", "--no-progress",
                                "--list-all-pkgs", "--skip-db-update", "--skip-java-db-update", "--offline-scan"],
                               diagnostic=output / "trivy.stderr.txt")
        retain(output / "trivy.json", raw_trivy)
        receipt["scan"] = validate_trivy(parse_json(raw_trivy, MAX_REPORT), receipt["image"], sbom)
        require(sha256(frozen_archive, MAX_ARCHIVE) == receipt["archive"]["sha256"], "immutable_archive_changed")
        scanner_final = validate_scanner_directory(scanner_directory, receipt["image"])
        require(scanner_final == scanner_identity, "immutable_scanner_directory_changed")
        final_db = validate_db(frozen_cache, dt.datetime.now(dt.timezone.utc))
        require(final_db["files"] == receipt["database"]["files"], "immutable_db_changed")
        require(receipt["scan"]["blocking_findings"] == 0, "high_or_critical_vulnerabilities")
        receipt["status"] = "PASS"
        code = 0
    except Blocked as error:
        receipt["blocked_reason"] = error.code
        if hasattr(error, "scan_summary"):
            receipt["scan"] = error.scan_summary
    except (OSError, ValueError, TypeError, KeyError, OverflowError):
        receipt["blocked_reason"] = "invalid_input_or_execution_failure"
    finally:
        evidence = []
        for path in sorted(output.iterdir()):
            if path.is_file():
                evidence.append({"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path, MAX_REPORT)})
        receipt["evidence"] = evidence
        receipt["evidence_inventory_sha256"] = hashlib.sha256(canonical(evidence)).hexdigest()
        retain(output / "receipt.json", canonical(receipt))
    print(json.dumps({"status": receipt["status"], "blocked_reason": receipt.get("blocked_reason"),
                      "receipt": "receipt.json"}, sort_keys=True))
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--manifest-digest", required=True)
    parser.add_argument("--db-cache", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        return assure(args.archive, args.manifest_digest, args.db_cache, args.output_dir)
    except Blocked as error:
        print(json.dumps({"status": "BLOCKED", "blocked_reason": error.code}, sort_keys=True))
        return 2
    except OSError:
        print(json.dumps({"status": "BLOCKED", "blocked_reason": "output_unavailable"}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
