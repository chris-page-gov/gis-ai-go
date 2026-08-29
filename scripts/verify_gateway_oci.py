#!/usr/bin/env python3
"""Verify an unregistered gateway OCI archive, checksum, context and source receipt."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from gateway_image import (
    RECEIPT_SCHEMA,
    ROOT,
    assert_no_private_text,
    build_context_inventory,
    build_context_manifest_bytes,
    canonical_json_bytes,
    inspect_oci_archive,
    make_image_receipt,
    parse_checksum,
    parse_bounded_json_object,
    read_bounded_regular_file,
    sha256_bytes,
    source_identity,
)

MAX_RECEIPT_JSON_BYTES = 8 * 1024 * 1024
MAX_SCHEMA_JSON_BYTES = 2 * 1024 * 1024
MAX_CONTEXT_MANIFEST_BYTES = 2 * 1024 * 1024


def verify_gateway_oci(
    *,
    archive: Path,
    checksum: Path,
    receipt_path: Path,
    context_path: Path,
    expected_source_commit: str | None = None,
    require_clean: bool = False,
) -> dict[str, Any]:
    checksum_digest = parse_checksum(checksum, archive.name)
    receipt_bytes = read_bounded_regular_file(
        receipt_path,
        maximum_bytes=MAX_RECEIPT_JSON_BYTES,
        label="gateway image receipt",
    )
    assert_no_private_text(receipt_bytes, "gateway image receipt")
    receipt = parse_bounded_json_object(
        receipt_bytes,
        maximum_bytes=MAX_RECEIPT_JSON_BYTES,
        label="gateway image receipt",
    )
    schema_bytes = read_bounded_regular_file(
        RECEIPT_SCHEMA,
        maximum_bytes=MAX_SCHEMA_JSON_BYTES,
        label="gateway image receipt schema",
    )
    schema = parse_bounded_json_object(
        schema_bytes,
        maximum_bytes=MAX_SCHEMA_JSON_BYTES,
        label="gateway image receipt schema",
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(receipt)
    if canonical_json_bytes(receipt) != receipt_bytes:
        raise ValueError("gateway image receipt is outside canonical repository JSON")

    context_bytes = read_bounded_regular_file(
        context_path,
        maximum_bytes=MAX_CONTEXT_MANIFEST_BYTES,
        label="gateway build-context manifest",
    )

    current_source = source_identity(allow_dirty=True)
    if expected_source_commit is not None and current_source.revision != expected_source_commit:
        raise ValueError("current gateway source differs from the expected source commit")
    if require_clean and not current_source.clean:
        raise ValueError("current gateway source is not clean")
    inventory = build_context_inventory()
    expected_context = build_context_manifest_bytes(inventory)
    if context_bytes != expected_context:
        raise ValueError("gateway build-context manifest differs from the current source")
    inspection = inspect_oci_archive(archive)
    if checksum_digest != inspection.archive_sha256:
        raise ValueError("gateway OCI checksum differs from the canonical archive")
    expected_receipt = make_image_receipt(
        source=current_source,
        inspection=inspection,
        context_manifest_sha256=sha256_bytes(expected_context),
        context_file_count=len(inventory),
        context_bytes=sum(item[2] for item in inventory),
        archive_name=archive.name,
        realised_buildx_version=receipt["build"]["buildx_version"],
    )
    if receipt != expected_receipt:
        raise ValueError(
            "gateway image receipt differs from current source, context or OCI identity"
        )
    if require_clean and receipt["classification"] != "repository-only-unregistered-candidate":
        raise ValueError("gateway image receipt is not a publishable clean-source candidate")
    return {"inspection": inspection, "receipt": receipt, "source": current_source}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--checksum", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--context-manifest", type=Path, required=True)
    parser.add_argument("--expected-source-commit")
    parser.add_argument("--require-clean", action="store_true")
    args = parser.parse_args()

    archive = args.archive if args.archive.is_absolute() else ROOT / args.archive
    checksum = args.checksum if args.checksum.is_absolute() else ROOT / args.checksum
    receipt_path = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    context_path = (
        args.context_manifest
        if args.context_manifest.is_absolute()
        else ROOT / args.context_manifest
    )
    result = verify_gateway_oci(
        archive=archive,
        checksum=checksum,
        receipt_path=receipt_path,
        context_path=context_path,
        expected_source_commit=args.expected_source_commit,
        require_clean=args.require_clean,
    )
    inspection = result["inspection"]
    source = result["receipt"]["source"]
    print(
        "Verified unregistered gateway OCI archive "
        f"{inspection.manifest_digest} from {source['revision']}."
    )


if __name__ == "__main__":
    main()
