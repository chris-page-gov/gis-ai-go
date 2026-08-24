#!/usr/bin/env python3
"""Closed DEPLOY-207 gateway evidence inventory and manifest helpers."""

from __future__ import annotations

import stat
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from gateway_image import (
    ROOT,
    assert_no_private_json,
    assert_no_private_text,
    canonical_json_bytes,
    parse_bounded_json_object,
    read_bounded_regular_file,
    sha256_file,
)

EVIDENCE_SCHEMA = ROOT / "schemas" / "gateway-image-evidence-manifest.schema.json"
EVIDENCE_MANIFEST_NAME = "gateway-image-evidence-manifest.json"
SUBJECTS = (
    ("build-context", "build-context.sha256"),
    ("oci-archive", "gateway-image.oci.tar"),
    ("oci-checksum", "gateway-image.oci.tar.sha256"),
    ("image-receipt", "image-receipt.json"),
    ("image-sbom", "gateway-image.sbom.cdx.json"),
    ("image-sbom-checksum", "gateway-image.sbom.cdx.json.sha256"),
    ("trivy-database", "gateway-image.trivy-db.tar.gz"),
    ("trivy-database-checksum", "gateway-image.trivy-db.tar.gz.sha256"),
    ("trivy-report", "gateway-image.trivy-report.json"),
    ("runtime-library-donor-archive", "gateway-runtime-library-donor.oci.tar"),
    (
        "runtime-library-donor-trivy-report",
        "gateway-runtime-library-donor.trivy-report.json",
    ),
    ("vulnerability-scan", "gateway-image.vulnerability-scan.json"),
    ("container-acceptance", "container-acceptance.json"),
)
ACCEPTED_FILES = frozenset({name for _, name in SUBJECTS} | {EVIDENCE_MANIFEST_NAME})
MAX_SCHEMA_JSON_BYTES = 2 * 1024 * 1024
MAX_RECEIPT_JSON_BYTES = 8 * 1024 * 1024
MAX_SBOM_JSON_BYTES = 256 * 1024 * 1024
MAX_SCAN_JSON_BYTES = 32 * 1024 * 1024
MAX_ACCEPTANCE_JSON_BYTES = 8 * 1024 * 1024
MAX_MANIFEST_JSON_BYTES = 8 * 1024 * 1024


def load_bounded_json_object(
    path: Path, *, maximum_bytes: int, label: str
) -> dict[str, Any]:
    """Load one JSON object through the bounded regular-file reader."""
    return parse_bounded_json_object(
        read_bounded_regular_file(path, maximum_bytes=maximum_bytes, label=label),
        maximum_bytes=maximum_bytes,
        label=label,
    )


def _syft_version(sbom: dict[str, Any]) -> str:
    tools = sbom.get("metadata", {}).get("tools", {}).get("components")
    if not isinstance(tools, list):
        raise ValueError("gateway image SBOM lacks its Syft tool identity")
    versions = {
        item.get("version")
        for item in tools
        if isinstance(item, dict) and item.get("name") == "syft"
    }
    if versions != {"1.42.2"}:
        raise ValueError("gateway image SBOM differs from the pinned Syft version")
    return "1.42.2"


def make_subjects(output: Path) -> list[dict[str, Any]]:
    subjects: list[dict[str, Any]] = []
    for role, name in SUBJECTS:
        path = output / name
        metadata = path.lstat()
        if (
            stat.S_ISLNK(metadata.st_mode)
            or not stat.S_ISREG(metadata.st_mode)
            or metadata.st_size < 1
        ):
            raise ValueError(f"gateway evidence subject is missing or invalid: {name}")
        subjects.append(
            {"role": role, "file": name, "sha256": sha256_file(path), "bytes": metadata.st_size}
        )
    return subjects


def make_evidence_manifest(output: Path, phases: list[dict[str, Any]]) -> dict[str, Any]:
    receipt = load_bounded_json_object(
        output / "image-receipt.json",
        maximum_bytes=MAX_RECEIPT_JSON_BYTES,
        label="gateway image receipt",
    )
    sbom = load_bounded_json_object(
        output / "gateway-image.sbom.cdx.json",
        maximum_bytes=MAX_SBOM_JSON_BYTES,
        label="gateway image SBOM",
    )
    scan = load_bounded_json_object(
        output / "gateway-image.vulnerability-scan.json",
        maximum_bytes=MAX_SCAN_JSON_BYTES,
        label="gateway vulnerability receipt",
    )
    acceptance = load_bounded_json_object(
        output / "container-acceptance.json",
        maximum_bytes=MAX_ACCEPTANCE_JSON_BYTES,
        label="gateway container acceptance receipt",
    )
    manifest = {
        "schema": "gis-ai-go.gateway-image-evidence-manifest.v1",
        "classification": receipt["classification"],
        "source": {
            "revision": receipt["source"]["revision"],
            "version": receipt["source"]["version"],
            "clean": receipt["source"]["clean"],
        },
        "image": {
            "manifest_digest": receipt["image"]["manifest_digest"],
            "platform": receipt["build"]["platform"],
        },
        "subjects": make_subjects(output),
        "tool_versions": {
            "docker_client": acceptance["engine"]["client"]["version"],
            "docker_server": acceptance["engine"]["server"]["version"],
            "compose": acceptance["engine"]["compose"]["version"],
            "buildx": receipt["build"]["buildx_version"],
            "buildkit": receipt["build"]["buildkit_version"],
            "syft": _syft_version(sbom),
            "trivy": scan["scanner"]["version"],
        },
        "phases": phases,
        "passed": True,
        "claims": {
            "public_deployment": False,
            "production_activation": False,
            "live_provider_call": False,
            "production_rollback": False,
        },
    }
    schema = load_bounded_json_object(
        EVIDENCE_SCHEMA,
        maximum_bytes=MAX_SCHEMA_JSON_BYTES,
        label="gateway evidence manifest schema",
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(manifest)
    encoded = canonical_json_bytes(manifest)
    assert_no_private_json(manifest, "gateway evidence manifest")
    assert_no_private_text(encoded, "gateway evidence manifest")
    return manifest


def write_evidence_manifest(output: Path, phases: list[dict[str, Any]]) -> Path:
    manifest = make_evidence_manifest(output, phases)
    path = output / EVIDENCE_MANIFEST_NAME
    path.write_bytes(canonical_json_bytes(manifest))
    entries = list(output.iterdir())
    if (
        {item.name for item in entries} != ACCEPTED_FILES
        or any(not item.is_file() or item.is_symlink() for item in entries)
    ):
        raise ValueError(
            "gateway accepted evidence directory is not a closed regular-file set"
        )
    return path
