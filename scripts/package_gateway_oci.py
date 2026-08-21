#!/usr/bin/env python3
"""Build one canonical, receipt-bound blocked gateway OCI archive."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from gateway_image import (
    RECEIPT_SCHEMA,
    ROOT,
    build_context_inventory,
    build_context_manifest_bytes,
    build_oci_archive,
    buildx_version,
    canonical_json_bytes,
    make_image_receipt,
    sha256_bytes,
    source_identity,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/gateway"))
    parser.add_argument("--platform", default="linux/amd64")
    parser.add_argument("--allow-dirty", action="store_true")
    args = parser.parse_args()

    output = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    source = source_identity(allow_dirty=args.allow_dirty)
    inventory = build_context_inventory()
    manifest_bytes = build_context_manifest_bytes(inventory)
    manifest_path = output / "build-context.sha256"
    manifest_path.write_bytes(manifest_bytes)

    archive = output / "gateway-image.oci.tar"
    tag = f"gis-ai-go-gateway:deploy-207-{source.revision[:12]}"
    inspection = build_oci_archive(
        archive,
        source=source,
        platform=args.platform,
        tag=tag,
    )
    receipt = make_image_receipt(
        source=source,
        inspection=inspection,
        context_manifest_sha256=sha256_bytes(manifest_bytes),
        context_file_count=len(inventory),
        context_bytes=sum(item[2] for item in inventory),
        archive_name=archive.name,
        realised_buildx_version=buildx_version(),
    )
    schema = json.loads(RECEIPT_SCHEMA.read_bytes())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(receipt)
    (output / "image-receipt.json").write_bytes(canonical_json_bytes(receipt))
    (output / "gateway-image.oci.tar.sha256").write_text(
        f"{inspection.archive_sha256}  {archive.name}\n", encoding="utf-8"
    )
    print(
        "Packaged blocked gateway OCI archive "
        f"{inspection.manifest_digest} ({inspection.archive_sha256})."
    )


if __name__ == "__main__":
    main()
