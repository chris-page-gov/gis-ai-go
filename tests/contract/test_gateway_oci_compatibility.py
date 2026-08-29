from __future__ import annotations

import copy
import gzip
import hashlib
import io
import json
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from gateway_image import (  # noqa: E402
    DOCKER_SAVE_MANIFEST,
    EXPECTED_ENVIRONMENT,
    EXPECTED_ENTRYPOINT,
    EXPECTED_HEALTH_CONFIGURATION,
    EXPECTED_REGISTRY_ID,
    UBI_RUNTIME_BASE_DIGEST,
    UBI_RUNTIME_BASE_REFERENCE,
    UBI_RUNTIME_LIBRARY_DONOR_REFERENCE,
    canonical_json_bytes,
    canonicalise_oci_archive,
    inspect_oci_archive,
)


def compact(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def blob_name(value: bytes) -> str:
    return f"blobs/sha256/{digest(value).removeprefix('sha256:')}"


def compressed_layer(name: str, payload: bytes) -> tuple[bytes, str]:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.USTAR_FORMAT) as archive:
        member = tarfile.TarInfo(name)
        member.mode = 0o644
        member.size = len(payload)
        archive.addfile(member, io.BytesIO(payload))
    raw = buffer.getvalue()
    return gzip.compress(raw, mtime=0), digest(raw)


def hybrid_files() -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    created = "2026-08-21T00:00:00Z"
    revision = "a" * 40
    tag = f"deploy-207-{revision[:12]}"
    labels = {
        "org.opencontainers.image.title": (
            "GIS AI GO local unregistered gateway candidate"
        ),
        "org.opencontainers.image.description": (
            "Repository-only exact-five unregistered gateway container"
        ),
        "org.opencontainers.image.source": "https://github.com/chris-page-gov/gis-ai-go",
        "org.opencontainers.image.licenses": (
            "MIT AND LicenseRef-Red-Hat-UBI-EULA AND "
            "LicenseRef-Third-Party-Notices"
        ),
        "org.opencontainers.image.base.name": UBI_RUNTIME_BASE_REFERENCE,
        "org.opencontainers.image.base.digest": UBI_RUNTIME_BASE_DIGEST,
        "org.opencontainers.image.version": "0.1.0",
        "org.opencontainers.image.revision": revision,
        "org.opencontainers.image.created": created,
        "io.gis-ai-go.registry-id": EXPECTED_REGISTRY_ID,
        "io.gis-ai-go.lifecycle": "candidate-unregistered",
        "io.gis-ai-go.red-hat-support": "not-supported-or-endorsed",
        "io.gis-ai-go.runtime-library-donor": UBI_RUNTIME_LIBRARY_DONOR_REFERENCE,
        "io.gis-ai-go.source-tree-clean": "true",
        "io.gis-ai-go.live-provider-calls": "true",
        "io.gis-ai-go.active-tools": (
            '["catalogue.search","catalogue.describe","selection.resolve",'
            '"data.query","evidence.inspect"]'
        ),
        "io.gis-ai-go.active-api-operations": (
            '["catalogue.search","catalogue.describe","selection.resolve",'
            '"data.query","evidence.inspect"]'
        ),
    }
    first_layer, first_diff_id = compressed_layer("first.txt", b"first layer\n")
    second_layer, second_diff_id = compressed_layer("second.txt", b"second layer\n")
    layers = [first_layer, second_layer]
    config_value = {
        "architecture": "amd64",
        "os": "linux",
        "created": created,
        "config": {
            "User": "65532:65532",
            "Entrypoint": EXPECTED_ENTRYPOINT,
            "WorkingDir": "/app/apps/mcp-gateway",
            "ExposedPorts": {"8787/tcp": {}},
            "Healthcheck": {
                **EXPECTED_HEALTH_CONFIGURATION,
                "Test": list(EXPECTED_HEALTH_CONFIGURATION["Test"]),
            },
            "Env": list(EXPECTED_ENVIRONMENT),
            "Labels": labels,
            "StopSignal": "SIGTERM",
        },
        "rootfs": {"type": "layers", "diff_ids": [first_diff_id, second_diff_id]},
        "history": [],
    }
    config = compact(config_value)
    manifest_value = {
        "schemaVersion": 2,
        "mediaType": "application/vnd.oci.image.manifest.v1+json",
        "config": {
            "mediaType": "application/vnd.oci.image.config.v1+json",
            "digest": digest(config),
            "size": len(config),
        },
        "layers": [
            {
                "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
                "digest": digest(layer),
                "size": len(layer),
            }
            for layer in layers
        ],
    }
    manifest = compact(manifest_value)
    index = compact(
        {
            "schemaVersion": 2,
            "mediaType": "application/vnd.oci.image.index.v1+json",
            "manifests": [
                {
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "digest": digest(manifest),
                    "size": len(manifest),
                    "annotations": {
                        "io.containerd.image.name": (
                            f"docker.io/library/gis-ai-go-gateway:{tag}"
                        ),
                        "org.opencontainers.image.created": created,
                        "org.opencontainers.image.ref.name": tag,
                    },
                    "platform": {"architecture": "amd64", "os": "linux"},
                }
            ],
        }
    )
    config_name = blob_name(config)
    layer_names = [blob_name(layer) for layer in layers]
    files = {
        "oci-layout": compact({"imageLayoutVersion": "1.0.0"}),
        "index.json": index,
        config_name: config,
        blob_name(manifest): manifest,
        **{name: layer for name, layer in zip(layer_names, layers, strict=True)},
    }
    docker_manifest = [
        {
            "Config": config_name,
            "RepoTags": [f"gis-ai-go-gateway:{tag}"],
            "Layers": layer_names,
        }
    ]
    return files, docker_manifest


def write_archive(
    path: Path,
    files: dict[str, bytes],
    *,
    docker_manifest: bytes | None = None,
    extra_file: bool = False,
    outer_attack: str | None = None,
) -> None:
    members: list[tuple[str, bytes | None, bytes, str]] = [
        ("blobs", None, tarfile.DIRTYPE, ""),
        ("blobs/sha256", None, tarfile.DIRTYPE, ""),
        *((name, value, tarfile.REGTYPE, "") for name, value in files.items()),
    ]
    if docker_manifest is not None:
        members.append((DOCKER_SAVE_MANIFEST, docker_manifest, tarfile.REGTYPE, ""))
    if extra_file:
        members.append(
            ("unexpected.txt", b"outside the closed inventory\n", tarfile.REGTYPE, "")
        )
    if outer_attack == "absolute":
        members.append(("/absolute.txt", b"outside\n", tarfile.REGTYPE, ""))
    elif outer_attack == "traversal":
        members.append(("../escape.txt", b"outside\n", tarfile.REGTYPE, ""))
    elif outer_attack == "normalisation-collision":
        members.append(("./index.json", files["index.json"], tarfile.REGTYPE, ""))
    elif outer_attack == "duplicate":
        members.append(("index.json", files["index.json"], tarfile.REGTYPE, ""))
    elif outer_attack == "symlink":
        members.append(("linked-index.json", None, tarfile.SYMTYPE, "index.json"))
    elif outer_attack == "hardlink":
        members.append(("hard-index.json", None, tarfile.LNKTYPE, "index.json"))
    elif outer_attack is not None:
        raise AssertionError(f"unknown outer archive attack: {outer_attack}")
    with tarfile.open(path, "w", format=tarfile.USTAR_FORMAT) as archive:
        for name, value, member_type, link_name in sorted(
            members, key=lambda item: (item[0].count("/"), item[0])
        ):
            member = tarfile.TarInfo(name)
            member.uid = 65532
            member.gid = 65532
            member.uname = ""
            member.gname = ""
            member.mtime = 0
            member.type = member_type
            member.linkname = link_name
            if member_type == tarfile.DIRTYPE:
                member.mode = 0o755
                archive.addfile(member)
            elif member_type in (tarfile.SYMTYPE, tarfile.LNKTYPE):
                member.mode = 0o777
                archive.addfile(member)
            else:
                assert value is not None
                member.type = tarfile.REGTYPE
                member.mode = 0o644
                member.size = len(value)
                archive.addfile(member, io.BytesIO(value))


class GatewayOciCompatibilityTests(unittest.TestCase):
    def test_valid_hybrid_is_derived_canonical_and_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw = root / "raw.oci.tar"
            first = root / "first.oci.tar"
            second = root / "second.oci.tar"
            rebuilt = root / "rebuilt.oci.tar"
            files, expected = hybrid_files()
            write_archive(raw, files)

            canonicalise_oci_archive(raw, first)
            canonicalise_oci_archive(raw, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            inspection = inspect_oci_archive(first)
            self.assertEqual(inspection.config_digest, digest(files[expected[0]["Config"]]))
            self.assertEqual(
                list(inspection.layer_digests),
                [
                    "sha256:" + path.rsplit("/", 1)[1]
                    for path in expected[0]["Layers"]
                ],
            )
            with tarfile.open(first, "r:") as archive:
                member = archive.getmember(DOCKER_SAVE_MANIFEST)
                handle = archive.extractfile(member)
                self.assertIsNotNone(handle)
                assert handle is not None
                self.assertEqual(handle.read(), canonical_json_bytes(expected))

            canonicalise_oci_archive(
                first,
                rebuilt,
                allow_existing_docker_manifest=True,
            )
            self.assertEqual(first.read_bytes(), rebuilt.read_bytes())

    def test_strict_inspection_rejects_hostile_docker_save_projections(self) -> None:
        files, valid = hybrid_files()
        cases: dict[str, tuple[bytes | None, bool]] = {}
        cases["missing"] = (None, False)
        cases["noncanonical"] = (
            json.dumps(valid, sort_keys=True, separators=(",", ":")).encode("utf-8"),
            False,
        )
        multiple = copy.deepcopy(valid)
        multiple.append(copy.deepcopy(valid[0]))
        cases["multiple"] = (canonical_json_bytes(multiple), False)
        extra_key = copy.deepcopy(valid)
        extra_key[0]["Parent"] = "sha256:" + "0" * 64
        cases["extra-key"] = (canonical_json_bytes(extra_key), False)
        wrong_config = copy.deepcopy(valid)
        wrong_config[0]["Config"] = wrong_config[0]["Layers"][0]
        cases["wrong-config"] = (canonical_json_bytes(wrong_config), False)
        wrong_tag = copy.deepcopy(valid)
        wrong_tag[0]["RepoTags"] = ["gis-ai-go-gateway:latest"]
        cases["wrong-tag"] = (canonical_json_bytes(wrong_tag), False)
        additional_tag = copy.deepcopy(valid)
        additional_tag[0]["RepoTags"].append("gis-ai-go-gateway:latest")
        cases["additional-tag"] = (canonical_json_bytes(additional_tag), False)
        duplicate_tag = copy.deepcopy(valid)
        duplicate_tag[0]["RepoTags"].append(duplicate_tag[0]["RepoTags"][0])
        cases["duplicate-tag"] = (canonical_json_bytes(duplicate_tag), False)
        missing_tag = copy.deepcopy(valid)
        missing_tag[0]["RepoTags"] = []
        cases["missing-tag"] = (canonical_json_bytes(missing_tag), False)
        wrong_layer_order = copy.deepcopy(valid)
        wrong_layer_order[0]["Layers"].reverse()
        cases["wrong-layer-order"] = (canonical_json_bytes(wrong_layer_order), False)
        additional_layer = copy.deepcopy(valid)
        additional_layer[0]["Layers"].append(additional_layer[0]["Config"])
        cases["additional-layer"] = (canonical_json_bytes(additional_layer), False)
        duplicate_layer = copy.deepcopy(valid)
        duplicate_layer[0]["Layers"].insert(0, duplicate_layer[0]["Layers"][0])
        cases["duplicate-layer"] = (canonical_json_bytes(duplicate_layer), False)
        missing_layer = copy.deepcopy(valid)
        missing_layer[0]["Layers"].pop()
        cases["missing-layer"] = (canonical_json_bytes(missing_layer), False)
        cases["extra-file"] = (canonical_json_bytes(valid), True)
        path_escape = copy.deepcopy(valid)
        path_escape[0]["Config"] = "../config.json"
        cases["path-escape"] = (canonical_json_bytes(path_escape), False)

        for name, (docker_manifest, extra_file) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                archive = Path(temporary) / "hostile.oci.tar"
                write_archive(
                    archive,
                    files,
                    docker_manifest=docker_manifest,
                    extra_file=extra_file,
                )
                with self.assertRaises(ValueError):
                    inspect_oci_archive(archive)

    def test_strict_inspection_rejects_outer_archive_aliasing_and_links(self) -> None:
        files, valid = hybrid_files()
        for attack in (
            "absolute",
            "traversal",
            "normalisation-collision",
            "duplicate",
            "symlink",
            "hardlink",
        ):
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as temporary:
                archive = Path(temporary) / "hostile.oci.tar"
                write_archive(
                    archive,
                    files,
                    docker_manifest=canonical_json_bytes(valid),
                    outer_attack=attack,
                )
                with self.assertRaises(ValueError):
                    inspect_oci_archive(archive)

    def test_raw_buildkit_manifest_is_rejected_even_when_it_matches(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw = root / "raw.oci.tar"
            output = root / "output.oci.tar"
            files, valid = hybrid_files()
            write_archive(raw, files, docker_manifest=canonical_json_bytes(valid))
            with self.assertRaisesRegex(
                ValueError,
                "raw OCI archive must not supply Docker manifest",
            ):
                canonicalise_oci_archive(raw, output)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
