from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from verify_gateway_provenance import (  # noqa: E402
    ARCHIVE_NAME,
    ARCHIVE_CHECKSUM_NAME,
    EVIDENCE_MANIFEST_NAME,
    EXCLUDED_PRIVATE_GRYPE_DB,
    MANIFEST_SUBJECTS,
    PRODUCER_TRANSPORT_FILES,
    SCAN_NAME,
    SBOM_PROPERTY_NAMES,
    SBOM_NAME,
    canonical_json_bytes,
    verify_attestation_inputs,
    verify_rebuild,
)
from gateway_evidence import ACCEPTED_FILES, SUBJECTS  # noqa: E402
from gateway_image import canonical_json_bytes as gateway_canonical_json_bytes  # noqa: E402


SOURCE_COMMIT = "5" * 40
IMAGE_DIGEST = "sha256:" + "a" * 64
ASSESSED_AT = datetime(2026, 8, 24, 12, 0, tzinfo=UTC)
VERIFIED_AT = ASSESSED_AT + timedelta(minutes=1)


def timestamp(value: datetime) -> str:
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_archive(directory: Path, payload: bytes) -> tuple[Path, Path]:
    directory.mkdir()
    archive = directory / ARCHIVE_NAME
    archive.write_bytes(payload)
    checksum = directory / f"{ARCHIVE_NAME}.sha256"
    checksum.write_text(f"{sha256(payload)}  {ARCHIVE_NAME}\n", encoding="ascii")
    return archive, checksum


def write_attestation_inputs(directory: Path) -> None:
    directory.mkdir()
    archive = b"canonical gateway OCI"
    property_values = {
        "gis-ai-go:image-manifest-digest": IMAGE_DIGEST,
        "gis-ai-go:image-receipt-sha256": "b" * 64,
        "gis-ai-go:rootfs-inventory-sha256": "c" * 64,
        "gis-ai-go:runtime-base-reference": (
            "registry.example/base@sha256:" + "d" * 64
        ),
        "gis-ai-go:runtime-base-source-reference": "registry.example/base-source",
        "gis-ai-go:runtime-library-donor-reference": (
            "registry.example/donor@sha256:" + "e" * 64
        ),
        "gis-ai-go:runtime-library-source-reference": "registry.example/donor-source",
        "gis-ai-go:scanner-image": "registry.example/syft@sha256:" + "f" * 64,
        "gis-ai-go:source-revision": SOURCE_COMMIT,
        "gis-ai-go:support-boundary": "repository-only blocked candidate",
        "gis-ai-go:ubi-eula-sha256": "1" * 64,
    }
    if set(property_values) != SBOM_PROPERTY_NAMES:
        raise AssertionError("attestation fixture SBOM property inventory differs")
    sbom = gateway_canonical_json_bytes(
        {
            "bomFormat": "CycloneDX",
            "metadata": {
                "component": {
                    "bom-ref": IMAGE_DIGEST,
                    "description": "Governed gateway evidence — exact image",
                    "properties": [
                        {"name": name, "value": property_values[name]}
                        for name in sorted(property_values)
                    ],
                }
            },
        }
    )
    (directory / ARCHIVE_NAME).write_bytes(archive)
    archive_checksum = f"{sha256(archive)}  {ARCHIVE_NAME}\n".encode("ascii")
    (directory / ARCHIVE_CHECKSUM_NAME).write_bytes(archive_checksum)
    (directory / SBOM_NAME).write_bytes(sbom)
    scan = canonical_json_bytes(
        {
            "claims": {
                "live_provider_call": False,
                "production_activation": False,
                "public_deployment": False,
            },
            "classification": "repository-only-blocked-candidate",
            "image": {
                "bytes": len(archive),
                "file": ARCHIVE_NAME,
                "sha256": sha256(archive),
            },
            "image_manifest_digest": IMAGE_DIGEST,
            "node_runtime": {
                "database": {
                    "age_seconds": 24 * 60 * 60,
                    "assessed_at": timestamp(ASSESSED_AT),
                    "built": timestamp(ASSESSED_AT - timedelta(days=1)),
                    "load_mode": "manual-import",
                    "provider": {
                        "captured": timestamp(ASSESSED_AT - timedelta(days=2)),
                        "name": "nvd",
                    },
                    "provider_age_seconds": 2 * 24 * 60 * 60,
                    "valid": True,
                }
            },
            "passed": True,
            "phase": {
                "completed_at": timestamp(ASSESSED_AT + timedelta(seconds=30)),
                "started_at": timestamp(ASSESSED_AT - timedelta(seconds=30)),
            },
            "sbom": {
                "bytes": len(sbom),
                "file": SBOM_NAME,
                "sha256": sha256(sbom),
            },
            "schema": "gis-ai-go.gateway-image-vulnerability-scan.v3",
            "source_revision": SOURCE_COMMIT,
        }
    )
    (directory / SCAN_NAME).write_bytes(scan)
    for filename in PRODUCER_TRANSPORT_FILES - {
        entry.name for entry in directory.iterdir()
    } - {EVIDENCE_MANIFEST_NAME}:
        (directory / filename).write_bytes(
            f"retained producer evidence: {filename}\n".encode()
        )
    private_grype_database = b"private retained Grype database"
    subjects = []
    for role, filename in MANIFEST_SUBJECTS:
        content = (
            private_grype_database
            if filename == EXCLUDED_PRIVATE_GRYPE_DB
            else (directory / filename).read_bytes()
        )
        subjects.append(
            {
                "bytes": len(content),
                "file": filename,
                "role": role,
                "sha256": sha256(content),
            }
        )
    manifest = {
        "classification": "repository-only-blocked-candidate",
        "image": {
            "manifest_digest": IMAGE_DIGEST,
            "platform": "linux/amd64",
        },
        "passed": True,
        "schema": "gis-ai-go.gateway-image-evidence-manifest.v2",
        "source": {
            "clean": True,
            "revision": SOURCE_COMMIT,
            "version": "0.1.0",
        },
        "subjects": subjects,
    }
    (directory / EVIDENCE_MANIFEST_NAME).write_bytes(canonical_json_bytes(manifest))


def write_rebound_sbom(directory: Path, sbom: dict[str, object]) -> None:
    sbom_bytes = canonical_json_bytes(sbom)
    (directory / SBOM_NAME).write_bytes(sbom_bytes)
    checksum_bytes = f"{sha256(sbom_bytes)}  {SBOM_NAME}\n".encode("ascii")
    checksum_name = f"{SBOM_NAME}.sha256"
    (directory / checksum_name).write_bytes(checksum_bytes)

    scan_path = directory / SCAN_NAME
    scan = json.loads(scan_path.read_bytes())
    scan["sbom"]["bytes"] = len(sbom_bytes)
    scan["sbom"]["sha256"] = sha256(sbom_bytes)
    scan_bytes = canonical_json_bytes(scan)
    scan_path.write_bytes(scan_bytes)

    manifest_path = directory / EVIDENCE_MANIFEST_NAME
    manifest = json.loads(manifest_path.read_bytes())
    updated = {
        SBOM_NAME: sbom_bytes,
        checksum_name: checksum_bytes,
        SCAN_NAME: scan_bytes,
    }
    for subject in manifest["subjects"]:
        content = updated.get(subject["file"])
        if content is not None:
            subject["bytes"] = len(content)
            subject["sha256"] = sha256(content)
    manifest_path.write_bytes(canonical_json_bytes(manifest))


class GatewayProvenanceTests(unittest.TestCase):
    def test_oidc_canonical_json_matches_gateway_evidence_encoding(self) -> None:
        value = {"description": "Governed gateway evidence — exact image"}
        self.assertEqual(canonical_json_bytes(value), gateway_canonical_json_bytes(value))

    def test_original_producer_transport_inventory_matches_the_evidence_contract(
        self,
    ) -> None:
        self.assertEqual(
            PRODUCER_TRANSPORT_FILES,
            ACCEPTED_FILES - {"gateway-node.grype-db.tar.zst"},
        )
        self.assertEqual(MANIFEST_SUBJECTS, SUBJECTS)

    def test_independent_rebuild_must_be_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            accepted_archive, accepted_checksum = write_archive(
                root / "accepted", b"reviewed bytes"
            )
            independent_archive, independent_checksum = write_archive(
                root / "independent", b"reviewed bytes"
            )
            measurement = verify_rebuild(
                accepted_archive=accepted_archive,
                accepted_checksum=accepted_checksum,
                independent_archive=independent_archive,
                independent_checksum=independent_checksum,
            )
            self.assertEqual(measurement.sha256, sha256(b"reviewed bytes"))
            self.assertEqual(measurement.bytes, len(b"reviewed bytes"))

    def test_self_consistent_substituted_archive_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            accepted_archive, accepted_checksum = write_archive(
                root / "accepted", b"reviewed application bytes"
            )
            independent_archive, independent_checksum = write_archive(
                root / "independent", b"substituted application bytes"
            )
            with self.assertRaisesRegex(ValueError, "differs from accepted bytes"):
                verify_rebuild(
                    accepted_archive=accepted_archive,
                    accepted_checksum=accepted_checksum,
                    independent_archive=independent_archive,
                    independent_checksum=independent_checksum,
                )

    def test_archive_checksum_and_real_file_controls_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            accepted_archive, accepted_checksum = write_archive(
                root / "accepted", b"reviewed bytes"
            )
            independent_archive, independent_checksum = write_archive(
                root / "independent", b"reviewed bytes"
            )
            independent_checksum.write_text(
                f"{'0' * 64}  {ARCHIVE_NAME}\n", encoding="ascii"
            )
            with self.assertRaisesRegex(ValueError, "checksum differs"):
                verify_rebuild(
                    accepted_archive=accepted_archive,
                    accepted_checksum=accepted_checksum,
                    independent_archive=independent_archive,
                    independent_checksum=independent_checksum,
                )

            independent_checksum.write_text(
                f"{sha256(b'reviewed bytes')}  {ARCHIVE_NAME}\n", encoding="ascii"
            )
            independent_archive.unlink()
            independent_archive.symlink_to(accepted_archive)
            with self.assertRaisesRegex(ValueError, "not one bounded regular file"):
                verify_rebuild(
                    accepted_archive=accepted_archive,
                    accepted_checksum=accepted_checksum,
                    independent_archive=independent_archive,
                    independent_checksum=independent_checksum,
                )

            independent_archive.unlink()
            os.link(accepted_archive, independent_archive)
            with self.assertRaisesRegex(ValueError, "not one bounded regular file"):
                verify_rebuild(
                    accepted_archive=accepted_archive,
                    accepted_checksum=accepted_checksum,
                    independent_archive=independent_archive,
                    independent_checksum=independent_checksum,
                )

    def test_oidc_attestation_inputs_are_source_and_subject_bound(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "attestation"
            write_attestation_inputs(root)
            measurements = verify_attestation_inputs(
                directory=root,
                expected_source_commit=SOURCE_COMMIT,
                verified_at=VERIFIED_AT,
            )
            self.assertEqual(
                set(measurements),
                {
                    ARCHIVE_NAME,
                    ARCHIVE_CHECKSUM_NAME,
                    SBOM_NAME,
                    SCAN_NAME,
                    EVIDENCE_MANIFEST_NAME,
                },
            )

            with self.subTest("changed OCI bytes"):
                archive = root / ARCHIVE_NAME
                original = archive.read_bytes()
                archive.write_bytes(original + b"changed")
                with self.assertRaisesRegex(ValueError, "differs from manifest"):
                    verify_attestation_inputs(
                        directory=root,
                        expected_source_commit=SOURCE_COMMIT,
                        verified_at=VERIFIED_AT,
                    )
                archive.write_bytes(original)

            with self.subTest("wrong source commit"):
                with self.assertRaisesRegex(ValueError, "invalid attestation identity"):
                    verify_attestation_inputs(
                        directory=root,
                        expected_source_commit="6" * 40,
                        verified_at=VERIFIED_AT,
                    )

            with self.subTest("extra transported file"):
                extra = root / "unexpected"
                extra.write_bytes(b"x")
                with self.assertRaisesRegex(ValueError, "file set is not closed"):
                    verify_attestation_inputs(
                        directory=root,
                        expected_source_commit=SOURCE_COMMIT,
                        verified_at=VERIFIED_AT,
                    )

    def test_oidc_attestation_accepts_the_closed_original_producer_superset(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "attestation"
            write_attestation_inputs(root)
            self.assertEqual(
                {entry.name for entry in root.iterdir()}, PRODUCER_TRANSPORT_FILES
            )
            measurements = verify_attestation_inputs(
                directory=root,
                expected_source_commit=SOURCE_COMMIT,
                verified_at=VERIFIED_AT,
            )
            self.assertEqual(
                set(measurements),
                {
                    ARCHIVE_NAME,
                    ARCHIVE_CHECKSUM_NAME,
                    SBOM_NAME,
                    SCAN_NAME,
                    EVIDENCE_MANIFEST_NAME,
                },
            )

    def test_oidc_attestation_rejects_a_reduced_manifest_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "attestation"
            write_attestation_inputs(root)
            manifest_path = root / EVIDENCE_MANIFEST_NAME
            manifest = json.loads(manifest_path.read_bytes())
            manifest["subjects"] = manifest["subjects"][:-1]
            manifest_path.write_bytes(canonical_json_bytes(manifest))
            with self.assertRaisesRegex(ValueError, "subject contract differs"):
                verify_attestation_inputs(
                    directory=root,
                    expected_source_commit=SOURCE_COMMIT,
                    verified_at=VERIFIED_AT,
                )

    def test_oidc_attestation_rejects_a_rebound_sbom(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "attestation"
            write_attestation_inputs(root)
            sbom_path = root / SBOM_NAME
            sbom = json.loads(sbom_path.read_bytes())
            source_property = next(
                item
                for item in sbom["metadata"]["component"]["properties"]
                if item["name"] == "gis-ai-go:source-revision"
            )
            source_property["value"] = "6" * 40
            sbom_bytes = canonical_json_bytes(sbom)
            sbom_path.write_bytes(sbom_bytes)
            manifest_path = root / EVIDENCE_MANIFEST_NAME
            manifest = json.loads(manifest_path.read_bytes())
            subject = next(
                item for item in manifest["subjects"] if item["file"] == SBOM_NAME
            )
            subject["bytes"] = len(sbom_bytes)
            subject["sha256"] = sha256(sbom_bytes)
            manifest_path.write_bytes(canonical_json_bytes(manifest))
            with self.assertRaisesRegex(ValueError, "SBOM differs"):
                verify_attestation_inputs(
                    directory=root,
                    expected_source_commit=SOURCE_COMMIT,
                    verified_at=VERIFIED_AT,
                )

    def test_oidc_attestation_rejects_ambiguous_sbom_properties(self) -> None:
        for case in (
            "duplicate source",
            "duplicate scanner",
            "scalar item",
            "extra field",
            "non-string value",
        ):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / "attestation"
                write_attestation_inputs(root)
                sbom = json.loads((root / SBOM_NAME).read_bytes())
                properties = sbom["metadata"]["component"]["properties"]
                if case == "duplicate source":
                    properties.insert(
                        0,
                        {
                            "name": "gis-ai-go:source-revision",
                            "value": "6" * 40,
                        },
                    )
                elif case == "duplicate scanner":
                    scanner = next(
                        item
                        for item in properties
                        if item["name"] == "gis-ai-go:scanner-image"
                    )
                    properties.insert(0, dict(scanner))
                elif case == "scalar item":
                    properties.insert(0, "ignored")
                elif case == "extra field":
                    properties[0]["unexpected"] = True
                else:
                    properties[0]["value"] = 1
                write_rebound_sbom(root, sbom)
                with self.assertRaisesRegex(
                    ValueError,
                    "invalid or duplicate property",
                ):
                    verify_attestation_inputs(
                        directory=root,
                        expected_source_commit=SOURCE_COMMIT,
                        verified_at=VERIFIED_AT,
                    )

    def test_oidc_attestation_uses_its_clock_for_scan_freshness(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "attestation"
            write_attestation_inputs(root)
            scan_path = root / SCAN_NAME
            manifest_path = root / EVIDENCE_MANIFEST_NAME
            scan = json.loads(scan_path.read_bytes())
            stale_assessment = ASSESSED_AT - timedelta(hours=3)
            database = scan["node_runtime"]["database"]
            database["assessed_at"] = timestamp(stale_assessment)
            database["built"] = timestamp(stale_assessment - timedelta(days=1))
            database["provider"]["captured"] = timestamp(
                stale_assessment - timedelta(days=2)
            )
            scan["phase"]["started_at"] = timestamp(
                stale_assessment - timedelta(seconds=30)
            )
            scan["phase"]["completed_at"] = timestamp(
                stale_assessment + timedelta(seconds=30)
            )
            scan_bytes = canonical_json_bytes(scan)
            scan_path.write_bytes(scan_bytes)
            manifest = json.loads(manifest_path.read_bytes())
            subject = next(
                item for item in manifest["subjects"] if item["file"] == SCAN_NAME
            )
            subject["bytes"] = len(scan_bytes)
            subject["sha256"] = sha256(scan_bytes)
            manifest_path.write_bytes(canonical_json_bytes(manifest))
            with self.assertRaisesRegex(ValueError, "too old for OIDC provenance"):
                verify_attestation_inputs(
                    directory=root,
                    expected_source_commit=SOURCE_COMMIT,
                    verified_at=VERIFIED_AT,
                )

    def test_oidc_attestation_rejects_stale_provider_data(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "attestation"
            write_attestation_inputs(root)
            scan_path = root / SCAN_NAME
            manifest_path = root / EVIDENCE_MANIFEST_NAME
            scan = json.loads(scan_path.read_bytes())
            database = scan["node_runtime"]["database"]
            database["provider"]["captured"] = timestamp(
                ASSESSED_AT - timedelta(days=4)
            )
            database["provider_age_seconds"] = 4 * 24 * 60 * 60
            scan_bytes = canonical_json_bytes(scan)
            scan_path.write_bytes(scan_bytes)
            manifest = json.loads(manifest_path.read_bytes())
            subject = next(
                item for item in manifest["subjects"] if item["file"] == SCAN_NAME
            )
            subject["bytes"] = len(scan_bytes)
            subject["sha256"] = sha256(scan_bytes)
            manifest_path.write_bytes(canonical_json_bytes(manifest))
            with self.assertRaisesRegex(ValueError, "outside the current database window"):
                verify_attestation_inputs(
                    directory=root,
                    expected_source_commit=SOURCE_COMMIT,
                    verified_at=VERIFIED_AT,
                )


if __name__ == "__main__":
    unittest.main()
