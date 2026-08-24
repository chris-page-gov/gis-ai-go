#!/usr/bin/env python3
"""Verify the complete closed DEPLOY-207 gateway evidence directory."""

from __future__ import annotations

import argparse
import json
import stat
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from gateway_evidence import (
    ACCEPTED_FILES,
    EVIDENCE_MANIFEST_NAME,
    EVIDENCE_SCHEMA,
    MAX_ACCEPTANCE_JSON_BYTES,
    MAX_MANIFEST_JSON_BYTES,
    MAX_RECEIPT_JSON_BYTES,
    MAX_SBOM_JSON_BYTES,
    MAX_SCAN_JSON_BYTES,
    MAX_SCHEMA_JSON_BYTES,
    load_bounded_json_object,
    make_subjects,
    parse_bounded_json_object,
    read_bounded_regular_file,
)
from gateway_image import (
    MAX_PRIVACY_TEXT_BYTES,
    ROOT,
    SYFT_REFERENCE,
    assert_no_private_json,
    assert_no_private_text,
    canonical_json_bytes,
    make_runtime_sbom_components,
    parse_checksum,
    sha256_bytes,
    sha256_file,
)
from scan_gateway_image import verify_scan_evidence
from verify_gateway_oci import verify_gateway_oci

ACCEPTANCE_SCHEMA = ROOT / "schemas" / "gateway-container-acceptance.schema.json"
COMPOSE_FILE = ROOT / "deploy" / "gateway" / "compose.candidate.yaml"
PHASE_ORDER = [
    "okf",
    "package",
    "verify",
    "reproducibility",
    "sbom",
    "vulnerability-scan",
    "container-acceptance",
]
TEXT_EVIDENCE = ACCEPTED_FILES - {
    "gateway-image.oci.tar",
    "gateway-image.trivy-db.tar.gz",
    "gateway-runtime-library-donor.oci.tar",
}
ACCEPTANCE_PHASE_ORDER = [
    "engine-identity",
    "exact-oci-load",
    "compose-render",
    "compose-start-and-probe",
    "restart-and-persistence",
    "service-suspension",
    "exact-image-restore",
]
TIMING_TOLERANCE_MS = 2_000
MAX_CHECKSUM_OR_CONTEXT_BYTES = 2 * 1024 * 1024
TEXT_FILE_LIMITS = {
    "build-context.sha256": MAX_CHECKSUM_OR_CONTEXT_BYTES,
    "gateway-image.oci.tar.sha256": MAX_CHECKSUM_OR_CONTEXT_BYTES,
    "image-receipt.json": MAX_RECEIPT_JSON_BYTES,
    "gateway-image.sbom.cdx.json": MAX_SBOM_JSON_BYTES,
    "gateway-image.sbom.cdx.json.sha256": MAX_CHECKSUM_OR_CONTEXT_BYTES,
    "gateway-image.trivy-db.tar.gz.sha256": MAX_CHECKSUM_OR_CONTEXT_BYTES,
    "gateway-image.trivy-report.json": MAX_SCAN_JSON_BYTES,
    "gateway-runtime-library-donor.trivy-report.json": MAX_SCAN_JSON_BYTES,
    "gateway-image.vulnerability-scan.json": MAX_SCAN_JSON_BYTES,
    "container-acceptance.json": MAX_ACCEPTANCE_JSON_BYTES,
    EVIDENCE_MANIFEST_NAME: MAX_MANIFEST_JSON_BYTES,
}


def _load_canonical(
    path: Path,
    schema_path: Path | None = None,
    *,
    maximum_bytes: int,
) -> dict[str, Any]:
    raw = read_bounded_regular_file(
        path,
        maximum_bytes=maximum_bytes,
        label=f"gateway evidence JSON {path.name}",
    )
    value = parse_bounded_json_object(
        raw,
        maximum_bytes=maximum_bytes,
        label=f"gateway evidence JSON {path.name}",
    )
    if canonical_json_bytes(value) != raw:
        raise ValueError(f"gateway evidence JSON is not canonical: {path.name}")
    if schema_path is not None:
        schema = load_bounded_json_object(
            schema_path,
            maximum_bytes=MAX_SCHEMA_JSON_BYTES,
            label=f"gateway evidence schema {schema_path.name}",
        )
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(value)
    return value


def _verify_sbom(output: Path, receipt: dict[str, Any]) -> dict[str, Any]:
    path = output / "gateway-image.sbom.cdx.json"
    checksum = output / "gateway-image.sbom.cdx.json.sha256"
    sbom = _load_canonical(path, maximum_bytes=MAX_SBOM_JSON_BYTES)
    sbom_bytes = canonical_json_bytes(sbom)
    if parse_checksum(checksum, path.name) != sha256_bytes(sbom_bytes):
        raise ValueError("gateway image SBOM checksum differs")
    metadata = sbom.get("metadata")
    component = metadata.get("component") if isinstance(metadata, dict) else None
    if (
        sbom.get("bomFormat") != "CycloneDX"
        or sbom.get("specVersion") not in {"1.5", "1.6"}
        or not isinstance(sbom.get("components"), list)
        or not sbom["components"]
        or not isinstance(component, dict)
        or component.get("bom-ref") != receipt["image"]["manifest_digest"]
        or component.get("name") != "gis-ai-go-gateway"
        or component.get("version") != receipt["source"]["version"]
        or component.get("licenses")
        != [
            {
                "expression": (
                    "MIT AND LicenseRef-Red-Hat-UBI-EULA AND "
                    "LicenseRef-Third-Party-Notices"
                )
            }
        ]
        or metadata.get("timestamp") != receipt["source"]["created"]
    ):
        raise ValueError("gateway image SBOM identity differs from its image receipt")
    expected_properties = {
        "gis-ai-go:image-manifest-digest": receipt["image"]["manifest_digest"],
        "gis-ai-go:image-receipt-sha256": sha256_file(
            output / "image-receipt.json"
        ),
        "gis-ai-go:source-revision": receipt["source"]["revision"],
        "gis-ai-go:scanner-image": SYFT_REFERENCE,
        "gis-ai-go:rootfs-inventory-sha256": receipt["image"]["rootfs"][
            "inventory_sha256"
        ],
        "gis-ai-go:runtime-base-reference": receipt["build"]["runtime_composition"][
            "runtime_base"
        ]["reference"],
        "gis-ai-go:runtime-base-source-reference": receipt["build"][
            "runtime_composition"
        ]["runtime_base"]["source_reference"],
        "gis-ai-go:runtime-library-donor-reference": receipt["build"][
            "runtime_composition"
        ]["runtime_library_donor"]["reference"],
        "gis-ai-go:runtime-library-source-reference": receipt["build"][
            "runtime_composition"
        ]["runtime_library_donor"]["source_reference"],
        "gis-ai-go:ubi-eula-sha256": receipt["build"]["runtime_composition"][
            "licence_material"
        ]["ubi_eula"]["sha256"],
        "gis-ai-go:support-boundary": receipt["build"]["runtime_composition"][
            "support_boundary"
        ],
    }
    properties = component.get("properties")
    if not isinstance(properties, list) or {
        item.get("name"): item.get("value")
        for item in properties
        if isinstance(item, dict)
    } != expected_properties:
        raise ValueError("gateway image SBOM properties differ from the exact source")
    tools = metadata.get("tools", {}).get("components")
    if not isinstance(tools, list) or {
        item.get("version")
        for item in tools
        if isinstance(item, dict) and item.get("name") == "syft"
    } != {"1.42.2"}:
        raise ValueError("gateway image SBOM lacks the exact Syft identity")
    components_by_reference: dict[str, dict[str, Any]] = {}
    for item in sbom["components"]:
        if not isinstance(item, dict) or not isinstance(item.get("bom-ref"), str):
            continue
        reference = item["bom-ref"]
        if reference in components_by_reference:
            raise ValueError("gateway image SBOM contains a duplicate component identity")
        components_by_reference[reference] = item
    for expected in make_runtime_sbom_components(receipt):
        actual = components_by_reference.get(expected["bom-ref"])
        normalised_expected = _normalise_sbom_value(expected)
        if actual != normalised_expected:
            raise ValueError(
                "gateway image SBOM lacks an exact runtime donor-file component"
            )
    return sbom


def _normalise_sbom_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _normalise_sbom_value(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        items = [_normalise_sbom_value(item) for item in value]
        return sorted(
            items,
            key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":")),
        )
    return value


def _parse_utc_timestamp(value: Any, *, label: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"{label} is not an explicit UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise ValueError(f"{label} is not a valid timestamp") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise ValueError(f"{label} is not UTC")
    return parsed.astimezone(UTC)


def _phase_duration(value: Any, *, label: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{label} is not a non-negative integer duration")
    return value


def _verify_phases(phases: Any) -> None:
    if (
        not isinstance(phases, list)
        or any(not isinstance(item, dict) for item in phases)
        or [item.get("name") for item in phases] != PHASE_ORDER
    ):
        raise ValueError("gateway evidence phase order is not closed")
    previous_end: datetime | None = None
    for phase in phases:
        name = phase["name"]
        started = _parse_utc_timestamp(
            phase.get("started_at"), label=f"gateway evidence {name} start"
        )
        completed = _parse_utc_timestamp(
            phase.get("completed_at"), label=f"gateway evidence {name} completion"
        )
        duration_ms = _phase_duration(
            phase.get("duration_ms"), label=f"gateway evidence {name} duration"
        )
        if completed < started or duration_ms <= 0:
            raise ValueError("gateway evidence phase times are not sequential")
        if previous_end is not None:
            gap_ms = round((started - previous_end).total_seconds() * 1000)
            if gap_ms < 0:
                raise ValueError("gateway evidence phase times are not sequential")
        elapsed_ms = round((completed - started).total_seconds() * 1000)
        if abs(duration_ms - elapsed_ms) > TIMING_TOLERANCE_MS:
            raise ValueError("gateway evidence phase duration differs from its timestamps")
        previous_end = completed


def _verify_acceptance_phase_timings(phases: Any) -> tuple[str, str, int]:
    """Validate the closed acceptance sequence and return its aggregate timing."""
    if (
        not isinstance(phases, list)
        or any(not isinstance(item, dict) for item in phases)
        or [item.get("name") for item in phases] != ACCEPTANCE_PHASE_ORDER
    ):
        raise ValueError("gateway container acceptance phase order is not closed")
    previous_end: datetime | None = None
    first_started: datetime | None = None
    for phase in phases:
        name = phase["name"]
        started = _parse_utc_timestamp(
            phase.get("started_at"), label=f"gateway acceptance {name} start"
        )
        ended = _parse_utc_timestamp(
            phase.get("ended_at"), label=f"gateway acceptance {name} end"
        )
        duration_ms = _phase_duration(
            phase.get("duration_ms"), label=f"gateway acceptance {name} duration"
        )
        if ended < started:
            raise ValueError("gateway container acceptance phase timing is inconsistent")
        if previous_end is not None:
            gap_ms = round((started - previous_end).total_seconds() * 1000)
            if gap_ms < 0:
                raise ValueError(
                    "gateway container acceptance phase timing is not sequential"
                )
        elapsed_ms = round((ended - started).total_seconds() * 1000)
        if abs(duration_ms - elapsed_ms) > TIMING_TOLERANCE_MS:
            raise ValueError(
                "gateway container acceptance phase duration differs from its timestamps"
            )
        if first_started is None:
            first_started = started
        previous_end = ended
    assert first_started is not None and previous_end is not None
    aggregate_duration_ms = round(
        (previous_end - first_started).total_seconds() * 1000
    )
    if aggregate_duration_ms <= 0:
        raise ValueError("gateway container acceptance aggregate timing is not positive")
    return phases[0]["started_at"], phases[-1]["ended_at"], aggregate_duration_ms


def _verify_outer_phase_containment(
    outer_phase: dict[str, Any],
    *,
    inner_started_at: str,
    inner_completed_at: str,
    inner_duration_ms: int,
    label: str,
) -> None:
    """Require one verified inner operation to fit its manifest phase."""
    outer_started = _parse_utc_timestamp(
        outer_phase.get("started_at"), label=f"{label} outer start"
    )
    outer_completed = _parse_utc_timestamp(
        outer_phase.get("completed_at"), label=f"{label} outer completion"
    )
    outer_duration_ms = _phase_duration(
        outer_phase.get("duration_ms"), label=f"{label} outer duration"
    )
    inner_started = _parse_utc_timestamp(inner_started_at, label=f"{label} inner start")
    inner_completed = _parse_utc_timestamp(
        inner_completed_at, label=f"{label} inner completion"
    )
    inner_duration = _phase_duration(inner_duration_ms, label=f"{label} inner duration")
    tolerance = timedelta(milliseconds=TIMING_TOLERANCE_MS)
    outer_elapsed_ms = round((outer_completed - outer_started).total_seconds() * 1000)
    inner_elapsed_ms = round((inner_completed - inner_started).total_seconds() * 1000)
    if (
        outer_elapsed_ms <= 0
        or inner_elapsed_ms <= 0
        or outer_duration_ms <= 0
        or inner_duration <= 0
        or abs(outer_duration_ms - outer_elapsed_ms) > TIMING_TOLERANCE_MS
        or abs(inner_duration - inner_elapsed_ms) > TIMING_TOLERANCE_MS
        or inner_started < outer_started - tolerance
        or inner_completed > outer_completed + tolerance
        or inner_duration > outer_duration_ms + TIMING_TOLERANCE_MS
    ):
        raise ValueError(f"{label} timing is not contained by its evidence phase")


def _verify_acceptance_bindings(
    acceptance: dict[str, Any], receipt: dict[str, Any]
) -> None:
    source = receipt["source"]
    accepted_source = {
        "repository": source["repository"],
        "revision": source["revision"],
        "version": source["version"],
        "created": source["created"],
        "source_date_epoch": source["source_date_epoch"],
        "tree_clean": source["clean"],
    }
    accepted_image = acceptance["image"]
    runtime_container = acceptance["runtime"]["container"]
    compose_version = acceptance["engine"]["compose"]["version"].removeprefix("v")
    runtime_versions = {
        runtime_container["labels"]["version"],
        acceptance["runtime"]["network"]["labels"]["version"],
        *(item["labels"]["version"] for item in acceptance["runtime"]["volumes"]),
    }
    health_catalogue = acceptance["boundary"]["health"]["catalogue"]
    loaded_descriptor = accepted_image["loaded_image_descriptor"]
    if loaded_descriptor is None:
        expected_loaded_image_id = receipt["image"]["config_digest"]
    else:
        if loaded_descriptor["digest"] != receipt["image"]["manifest_digest"]:
            raise ValueError("gateway container descriptor differs from the OCI manifest")
        expected_loaded_image_id = receipt["image"]["manifest_digest"]
    if (
        acceptance["classification"] != "local-mechanism-rehearsal"
        or acceptance["source"] != accepted_source
        or accepted_image["archive_sha256"] != receipt["image"]["archive_sha256"]
        or accepted_image["manifest_digest"] != receipt["image"]["manifest_digest"]
        or accepted_image["config_digest"] != receipt["image"]["config_digest"]
        or accepted_image["platform"] != receipt["build"]["platform"]
        or accepted_image["tag"]
        != f"gis-ai-go-gateway:deploy-207-{source['revision'][:12]}"
        or accepted_image["loaded_image_id"] != accepted_image["restored_image_id"]
        or accepted_image["loaded_image_id"] != expected_loaded_image_id
        or runtime_container["image_id"] != accepted_image["loaded_image_id"]
        or runtime_container["labels"]["image"] != accepted_image["loaded_image_id"]
        or runtime_versions != {compose_version}
        or health_catalogue["revision"] != source["revision"]
        or health_catalogue["version"] != source["version"]
        or acceptance["compose"]["file"] != "deploy/gateway/compose.candidate.yaml"
        or acceptance["compose"]["file_sha256"] != sha256_file(COMPOSE_FILE)
        or any(acceptance["claims"].values())
    ):
        raise ValueError("gateway container acceptance differs from source, image or claims")

    okf_receipt_path = ROOT / "artifacts" / "okf" / "build-receipt.json"
    try:
        okf_receipt = load_bounded_json_object(
            okf_receipt_path,
            maximum_bytes=MAX_RECEIPT_JSON_BYTES,
            label="canonical OKF build receipt",
        )
    except (OSError, ValueError) as error:
        raise ValueError(
            "canonical OKF evidence is unavailable for acceptance verification"
        ) from error
    if (
        okf_receipt.get("revision") != source["revision"]
        or okf_receipt.get("version") != source["version"]
        or okf_receipt.get("contentRootSha256")
        != health_catalogue["content_root_sha256"]
        or okf_receipt.get("recordCount") != health_catalogue["record_count"]
    ):
        raise ValueError("gateway health catalogue differs from canonical OKF evidence")


def _verify_tool_version_bindings(
    manifest: dict[str, Any],
    receipt: dict[str, Any],
    scan: dict[str, Any],
    acceptance: dict[str, Any],
) -> None:
    expected = {
        "docker_client": acceptance["engine"]["client"]["version"],
        "docker_server": acceptance["engine"]["server"]["version"],
        "compose": acceptance["engine"]["compose"]["version"],
        "buildx": receipt["build"]["buildx_version"],
        "buildkit": receipt["build"]["buildkit_version"],
        "syft": "1.42.2",
        "trivy": scan["scanner"]["version"],
    }
    if manifest["tool_versions"] != expected:
        raise ValueError("gateway evidence tool identities differ from producing evidence")


def _verify_text_evidence_privacy(output: Path) -> None:
    """Reject private paths and credential-shaped values before parsing evidence."""
    for name in sorted(TEXT_EVIDENCE):
        maximum_bytes = TEXT_FILE_LIMITS.get(name)
        if maximum_bytes is None:
            raise ValueError(f"gateway textual evidence lacks a byte bound: {name}")
        raw = read_bounded_regular_file(
            output / name,
            maximum_bytes=min(maximum_bytes, MAX_PRIVACY_TEXT_BYTES),
            label=f"gateway textual evidence {name}",
        )
        assert_no_private_text(raw, f"gateway textual evidence {name}")
        if name.endswith(".json"):
            document = parse_bounded_json_object(
                raw,
                maximum_bytes=maximum_bytes,
                label=f"gateway textual evidence {name}",
            )
            assert_no_private_json(document, f"gateway textual evidence {name}")


def verify_gateway_image_evidence(
    *,
    output: Path,
    expected_source_commit: str | None,
    require_clean: bool,
    replay_trivy: bool,
) -> dict[str, Any]:
    output_metadata = output.lstat()
    if stat.S_ISLNK(output_metadata.st_mode) or not stat.S_ISDIR(output_metadata.st_mode):
        raise ValueError("gateway evidence path is not a regular directory")
    entries = list(output.iterdir())
    if (
        {item.name for item in entries} != ACCEPTED_FILES
        or any(
            stat.S_ISLNK(item.lstat().st_mode)
            or not stat.S_ISREG(item.lstat().st_mode)
            for item in entries
        )
    ):
        raise ValueError("gateway accepted evidence directory is not a closed regular-file set")
    _verify_text_evidence_privacy(output)
    _load_canonical(
        output / "image-receipt.json",
        maximum_bytes=MAX_RECEIPT_JSON_BYTES,
    )
    oci_result = verify_gateway_oci(
        archive=output / "gateway-image.oci.tar",
        checksum=output / "gateway-image.oci.tar.sha256",
        receipt_path=output / "image-receipt.json",
        context_path=output / "build-context.sha256",
        expected_source_commit=expected_source_commit,
        require_clean=require_clean,
    )
    receipt = oci_result["receipt"]
    sbom = _verify_sbom(output, receipt)
    scan = verify_scan_evidence(
        scan_path=output / "gateway-image.vulnerability-scan.json",
        archive=output / "gateway-image.oci.tar",
        sbom=output / "gateway-image.sbom.cdx.json",
        receipt_path=output / "image-receipt.json",
        replay=replay_trivy,
    )
    acceptance = _load_canonical(
        output / "container-acceptance.json",
        ACCEPTANCE_SCHEMA,
        maximum_bytes=MAX_ACCEPTANCE_JSON_BYTES,
    )
    acceptance_timing = _verify_acceptance_phase_timings(acceptance["phases"])
    _verify_acceptance_bindings(acceptance, receipt)
    manifest = _load_canonical(
        output / EVIDENCE_MANIFEST_NAME,
        EVIDENCE_SCHEMA,
        maximum_bytes=MAX_MANIFEST_JSON_BYTES,
    )
    expected_subjects = make_subjects(output)
    if (
        manifest["classification"] != receipt["classification"]
        or manifest["source"]
        != {
            "revision": receipt["source"]["revision"],
            "version": receipt["source"]["version"],
            "clean": receipt["source"]["clean"],
        }
        or manifest["image"]
        != {
            "manifest_digest": receipt["image"]["manifest_digest"],
            "platform": receipt["build"]["platform"],
        }
        or manifest["subjects"] != expected_subjects
    ):
        raise ValueError("gateway evidence manifest does not transitively bind its subjects")
    _verify_tool_version_bindings(manifest, receipt, scan, acceptance)
    _verify_phases(manifest["phases"])
    phases_by_name = {phase["name"]: phase for phase in manifest["phases"]}
    scan_phase = scan["phase"]
    _verify_outer_phase_containment(
        phases_by_name["vulnerability-scan"],
        inner_started_at=scan_phase["started_at"],
        inner_completed_at=scan_phase["completed_at"],
        inner_duration_ms=scan_phase["duration_ms"],
        label="gateway vulnerability scan",
    )
    _verify_outer_phase_containment(
        phases_by_name["container-acceptance"],
        inner_started_at=acceptance_timing[0],
        inner_completed_at=acceptance_timing[1],
        inner_duration_ms=acceptance_timing[2],
        label="gateway container acceptance",
    )
    return {
        "receipt": receipt,
        "sbom": sbom,
        "scan": scan,
        "acceptance": acceptance,
        "manifest": manifest,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--expected-source-commit")
    parser.add_argument("--require-clean", action="store_true")
    parser.add_argument("--skip-trivy-replay", action="store_true")
    args = parser.parse_args()
    output = args.directory if args.directory.is_absolute() else ROOT / args.directory
    result = verify_gateway_image_evidence(
        output=output,
        expected_source_commit=args.expected_source_commit,
        require_clean=args.require_clean,
        replay_trivy=not args.skip_trivy_replay,
    )
    print(
        "Verified complete blocked gateway evidence for "
        f"{result['receipt']['image']['manifest_digest']}."
    )


if __name__ == "__main__":
    main()
