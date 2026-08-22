#!/usr/bin/env python3
"""Build the blocked gateway image again and compare its canonical OCI bytes."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from gateway_image import ROOT, build_oci_archive, inspect_oci_archive, source_identity


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--allow-dirty", action="store_true")
    args = parser.parse_args()

    reference = args.reference if args.reference.is_absolute() else ROOT / args.reference
    receipt_path = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    receipt = json.loads(receipt_path.read_bytes())
    source = source_identity(allow_dirty=args.allow_dirty)
    if (
        receipt.get("source", {}).get("revision") != source.revision
        or receipt.get("source", {}).get("clean") != source.clean
    ):
        raise ValueError("reference image receipt differs from the current source state")
    expected = inspect_oci_archive(reference)
    platform = receipt.get("build", {}).get("platform")
    if not isinstance(platform, str):
        raise ValueError("reference image receipt lacks its platform")
    with tempfile.TemporaryDirectory(prefix="gis-ai-go-gateway-repro-") as temporary:
        repeated_path = Path(temporary) / "gateway-image.oci.tar"
        repeated = build_oci_archive(
            repeated_path,
            source=source,
            platform=platform,
            tag=f"gis-ai-go-gateway:deploy-207-{source.revision[:12]}",
        )
        if repeated != expected or repeated_path.read_bytes() != reference.read_bytes():
            raise AssertionError("two clean gateway OCI builds are not byte-identical")
    print(
        "Gateway OCI reproducibility passed at archive SHA-256 "
        f"{expected.archive_sha256}."
    )


if __name__ == "__main__":
    main()
