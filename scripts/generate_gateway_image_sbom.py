#!/usr/bin/env python3
"""Generate a deterministic full-image CycloneDX SBOM with pinned Syft."""

from __future__ import annotations

import argparse
import json
import subprocess
import uuid
from pathlib import Path
from typing import Any

from gateway_image import (
    ROOT,
    SYFT_REFERENCE,
    assert_no_private_json,
    assert_no_private_text,
    canonical_json_bytes,
    inspect_oci_archive,
    sha256_file,
)


def normalise(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: normalise(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        items = [normalise(item) for item in value]
        return sorted(items, key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")))
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    archive = args.archive if args.archive.is_absolute() else ROOT / args.archive
    receipt_path = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    output = args.output if args.output.is_absolute() else ROOT / args.output
    inspection = inspect_oci_archive(archive)
    receipt = json.loads(receipt_path.read_bytes())
    source = receipt.get("source")
    if not isinstance(source, dict) or receipt.get("image", {}).get(
        "manifest_digest"
    ) != inspection.manifest_digest:
        raise ValueError("gateway SBOM input differs from the image receipt")

    result = subprocess.run(
        (
            "docker",
            "run",
            "--rm",
            "--pull=always",
            "--read-only",
            "--network=none",
            "--cap-drop=ALL",
            "--security-opt=no-new-privileges",
            "--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=512m,mode=0700",
            "--env=HOME=/tmp",
            "--env=SYFT_CHECK_FOR_APP_UPDATE=false",
            f"--volume={archive}:/input/gateway-image.oci.tar:ro",
            SYFT_REFERENCE,
            "oci-archive:/input/gateway-image.oci.tar",
            "--output=cyclonedx-json",
        ),
        cwd=ROOT,
        check=True,
        capture_output=True,
        timeout=10 * 60,
    )
    try:
        document = json.loads(result.stdout)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("pinned Syft returned an invalid CycloneDX document") from error
    if (
        not isinstance(document, dict)
        or document.get("bomFormat") != "CycloneDX"
        or not isinstance(document.get("components"), list)
        or not document["components"]
    ):
        raise ValueError("pinned Syft returned an empty or unsupported image SBOM")
    metadata = document.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError("pinned Syft image SBOM lacks metadata")
    metadata["timestamp"] = source["created"]
    metadata["component"] = {
        "bom-ref": inspection.manifest_digest,
        "type": "container",
        "name": "gis-ai-go-gateway",
        "version": source["version"],
        "properties": [
            {"name": "gis-ai-go:image-manifest-digest", "value": inspection.manifest_digest},
            {"name": "gis-ai-go:source-revision", "value": source["revision"]},
            {"name": "gis-ai-go:scanner-image", "value": SYFT_REFERENCE},
        ],
    }
    document["serialNumber"] = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, inspection.manifest_digest)}"
    normalised = normalise(document)
    output_bytes = canonical_json_bytes(normalised)
    assert_no_private_json(normalised, "gateway image SBOM")
    assert_no_private_text(output_bytes, "gateway image SBOM")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(output_bytes)
    output.with_suffix(output.suffix + ".sha256").write_text(
        f"{sha256_file(output)}  {output.name}\n", encoding="utf-8"
    )
    print(
        f"Generated full gateway image SBOM with {len(document['components'])} components."
    )


if __name__ == "__main__":
    main()
