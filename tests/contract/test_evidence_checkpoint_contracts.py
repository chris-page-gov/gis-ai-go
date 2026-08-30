from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIRECTORY = ROOT / "schemas"


def load_schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMA_DIRECTORY / name).read_text(encoding="utf-8"))


def schema_registry() -> Registry:
    resources = []
    for path in sorted(SCHEMA_DIRECTORY.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def validator(name: str) -> Draft202012Validator:
    return Draft202012Validator(
        load_schema(name),
        registry=schema_registry(),
        format_checker=FormatChecker(),
    )


def root_summary(
    identity: str, *, entry_count: int, file_count: int
) -> dict[str, object]:
    return {
        "root_sha256": identity * 64,
        "entry_count": entry_count,
        "file_count": file_count,
        "total_bytes": 1024,
    }


def manifest() -> dict[str, object]:
    return {
        "schema": "gis-ai-go.evidence-checkpoint-manifest.v1",
        "checkpoint_id": f"gis-ai-go:evidence-checkpoint:sha256:{'a' * 64}",
        "created_at": "2026-08-24T09:00:00.000Z",
        "quiescence": {
            "writer": "stopped-single-writer",
            "assertion": "operator-supplied",
            "source_verification": "complete-before-and-after-copy",
            "concurrent_change": "rejected",
        },
        "ledger": {
            "ledger_id": (
                f"gis-ai-go:public-evidence-ledger:sha256:{'b' * 64}"
            ),
            "retention_days": 30,
            "event_count": 1,
            "record_count": 1,
            "last_event_id": (
                f"gis-ai-go:evidence-ledger-event:sha256:{'c' * 64}"
            ),
            "root": root_summary("d", entry_count=5, file_count=3),
        },
        "reconciliation_index": {
            "index_id": (
                "gis-ai-go:evidence-reconciliation-index:sha256:"
                f"{'e' * 64}"
            ),
            "ledger_id": (
                f"gis-ai-go:public-evidence-ledger:sha256:{'b' * 64}"
            ),
            "claim_count": 1,
            "resolution_count": 1,
            "completed_count": 1,
            "pending_count": 0,
            "root": root_summary("f", entry_count=11, file_count=6),
        },
        "recovery": {
            "destination_roots": "existing-empty-private-directories",
            "verification": "complete-ledger-and-index-after-restore",
            "in_place_repair": False,
            "disposal_automation": False,
        },
        "privacy": {
            "source_path": False,
            "destination_path": False,
            "raw_query": False,
            "result_material": False,
            "credentials": False,
            "personal_data": False,
        },
    }


def external_checkpoint(source_manifest: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "gis-ai-go.evidence-external-checkpoint.v1",
        "created_at": source_manifest["created_at"],
        "checkpoint_id": source_manifest["checkpoint_id"],
        "manifest_sha256": "1" * 64,
        "storage_boundary": "external-to-backup-required",
        "ledger": copy.deepcopy(source_manifest["ledger"]),
        "reconciliation_index": copy.deepcopy(
            source_manifest["reconciliation_index"]
        ),
    }


class EvidenceCheckpointContractTests(unittest.TestCase):
    def test_manifest_and_external_checkpoint_are_closed_path_free_contracts(self) -> None:
        source_manifest = manifest()
        external = external_checkpoint(source_manifest)
        manifest_errors = list(
            validator("evidence-checkpoint-manifest.schema.json").iter_errors(
                source_manifest
            )
        )
        external_errors = list(
            validator("evidence-external-checkpoint.schema.json").iter_errors(
                external
            )
        )
        self.assertEqual([], [error.message for error in manifest_errors])
        self.assertEqual([], [error.message for error in external_errors])
        self.assertNotIn("source_directory", json.dumps(source_manifest))
        self.assertNotIn("destination_directory", json.dumps(external))

        with_path = copy.deepcopy(source_manifest)
        with_path["source_directory"] = "/private/source-ledger"
        self.assertTrue(
            list(
                validator("evidence-checkpoint-manifest.schema.json").iter_errors(
                    with_path
                )
            )
        )
        invalid_privacy = copy.deepcopy(source_manifest)
        invalid_privacy["privacy"]["source_path"] = "/private/source"
        self.assertTrue(
            list(
                validator("evidence-checkpoint-manifest.schema.json").iter_errors(
                    invalid_privacy
                )
            )
        )

    def test_external_checkpoint_requires_ledger_tail_and_both_root_digests(self) -> None:
        source_manifest = manifest()
        external = external_checkpoint(source_manifest)
        del external["ledger"]["last_event_id"]
        self.assertTrue(
            list(
                validator("evidence-external-checkpoint.schema.json").iter_errors(
                    external
                )
            )
        )

        external = external_checkpoint(source_manifest)
        del external["reconciliation_index"]["root"]["root_sha256"]
        self.assertTrue(
            list(
                validator("evidence-external-checkpoint.schema.json").iter_errors(
                    external
                )
            )
        )

    def test_role_specific_root_traversal_ceilings_are_closed(self) -> None:
        ceilings = {
            "ledger": {
                "entry_count": 2_000_003,
                "file_count": 2_000_001,
                "total_bytes": 4_259_840_016_384,
            },
            "reconciliation_index": {
                "entry_count": 20_486,
                "file_count": 20_481,
                "total_bytes": 201_342_976,
            },
        }
        checkpoint_validator = validator("evidence-checkpoint-manifest.schema.json")
        external_validator = validator("evidence-external-checkpoint.schema.json")

        for role, limits in ceilings.items():
            for field, maximum in limits.items():
                at_boundary = manifest()
                at_boundary[role]["root"][field] = maximum
                self.assertEqual(
                    [],
                    [error.message for error in checkpoint_validator.iter_errors(at_boundary)],
                )

                above_boundary = manifest()
                above_boundary[role]["root"][field] = maximum + 1
                self.assertTrue(list(checkpoint_validator.iter_errors(above_boundary)))
                self.assertTrue(
                    list(
                        external_validator.iter_errors(
                            external_checkpoint(above_boundary)
                        )
                    )
                )

    def test_check_and_reconciliation_results_distinguish_durability(self) -> None:
        source_manifest = manifest()
        check = {
            "schema": "gis-ai-go.evidence-checkpoint-check.v1",
            "status": "passed",
            "publication_durability": "not-established-by-read-only-check",
            "checkpoint_id": source_manifest["checkpoint_id"],
            "ledger": {
                "ledger_id": source_manifest["ledger"]["ledger_id"],
                "event_count": 1,
                "record_count": 1,
                "last_event_id": source_manifest["ledger"]["last_event_id"],
            },
            "reconciliation_index": {
                "index_id": source_manifest["reconciliation_index"]["index_id"],
                "ledger_id": source_manifest["ledger"]["ledger_id"],
                "claim_count": 1,
                "completed_count": 1,
                "pending_count": 0,
            },
        }
        reconciled = {
            "schema": (
                "gis-ai-go.evidence-checkpoint-publication-reconciliation.v1"
            ),
            "status": "passed",
            "publication_durability": "file-and-parent-directory-synchronised",
            "checkpoint_id": source_manifest["checkpoint_id"],
            "ledger_id": source_manifest["ledger"]["ledger_id"],
            "reconciliation_index_id": (
                source_manifest["reconciliation_index"]["index_id"]
            ),
        }
        check_validator = validator("evidence-checkpoint-check.schema.json")
        reconciliation_validator = validator(
            "evidence-checkpoint-publication-reconciliation.schema.json"
        )
        self.assertEqual([], list(check_validator.iter_errors(check)))
        self.assertEqual([], list(reconciliation_validator.iter_errors(reconciled)))

        falsely_durable = copy.deepcopy(check)
        falsely_durable["publication_durability"] = (
            "file-and-parent-directory-synchronised"
        )
        self.assertTrue(list(check_validator.iter_errors(falsely_durable)))

        read_only_reconciliation = copy.deepcopy(reconciled)
        read_only_reconciliation["publication_durability"] = (
            "not-established-by-read-only-check"
        )
        self.assertTrue(
            list(reconciliation_validator.iter_errors(read_only_reconciliation))
        )

    def test_operator_results_are_closed_path_free_and_keep_deployment_unscored(
        self,
    ) -> None:
        source_manifest = manifest()
        verification = {
            "checkpoint_id": source_manifest["checkpoint_id"],
            "ledger": {
                "ledger_id": source_manifest["ledger"]["ledger_id"],
                "event_count": 1,
                "record_count": 1,
                "last_event_id": source_manifest["ledger"]["last_event_id"],
            },
            "reconciliation_index": {
                "index_id": source_manifest["reconciliation_index"]["index_id"],
                "ledger_id": source_manifest["ledger"]["ledger_id"],
                "claim_count": 1,
                "completed_count": 1,
                "pending_count": 0,
            },
        }
        assertions = {
            "stopped_single_writer": "operator-confirmed",
            "exclusive_operation_owner": "operator-confirmed",
        }
        created = {
            "schema": "gis-ai-go.evidence-checkpoint-create-result.v1",
            "status": "passed",
            "operation": "create",
            "operator_assertions": assertions,
            "publication_durability": (
                "file-and-parent-directory-synchronised"
            ),
            **verification,
        }
        restored = {
            "schema": "gis-ai-go.evidence-checkpoint-restore-result.v1",
            "status": "passed",
            "operation": "restore",
            "operator_assertions": assertions,
            "source_checkpoint": "verified",
            "restored_pair": "verified",
            "deployment_readiness": "not-evaluated",
            **verification,
        }
        create_validator = validator(
            "evidence-checkpoint-create-result.schema.json"
        )
        restore_validator = validator(
            "evidence-checkpoint-restore-result.schema.json"
        )
        self.assertEqual([], list(create_validator.iter_errors(created)))
        self.assertEqual([], list(restore_validator.iter_errors(restored)))

        for schema_validator, document in (
            (create_validator, created),
            (restore_validator, restored),
        ):
            with self.subTest(schema=document["schema"]):
                text = json.dumps(document, sort_keys=True)
                self.assertNotIn("/Users/", text)
                self.assertNotIn("source_directory", text)
                self.assertNotIn("destination_directory", text)
                widened = copy.deepcopy(document)
                widened["checkpoint_directory"] = "/private/checkpoint"
                self.assertTrue(list(schema_validator.iter_errors(widened)))

        false_assertion = copy.deepcopy(created)
        false_assertion["operator_assertions"]["stopped_single_writer"] = False
        self.assertTrue(list(create_validator.iter_errors(false_assertion)))
        false_readiness = copy.deepcopy(restored)
        false_readiness["deployment_readiness"] = "ready"
        self.assertTrue(list(restore_validator.iter_errors(false_readiness)))

    def test_filesystem_probe_and_rehearsal_results_preserve_provider_boundary(
        self,
    ) -> None:
        source_manifest = manifest()
        filesystem = {
            "schema": "gis-ai-go.evidence-filesystem-capability-check.v1",
            "status": "passed",
            "classification": "direct-filesystem-observation",
            "scope": "one-caller-identified-filesystem",
            "observed_at": "2026-08-30T08:30:00.000Z",
            "mount_identity_sha256": "a" * 64,
            "schema_contract": {
                "path": (
                    "schemas/evidence-filesystem-capability-check.schema.json"
                ),
                "sha256": "b" * 64,
            },
            "checks": [
                "private-directory-mode-0700",
                "private-file-mode-0600",
                "exclusive-file-create",
                "sibling-hard-link",
                "atomic-no-replace-hard-link",
                "regular-file-fsync",
                "directory-fsync",
                "synchronised-clean-up",
            ],
            "limitations": {
                "same_filesystem_only": True,
                "full_hardware_flush": "not-established",
                "mount_identity_provenance": "caller-supplied-not-attested",
            },
        }
        rehearsal_filesystem = copy.deepcopy(filesystem)
        rehearsal_filesystem["classification"] = "synthetic-test-fixture"
        rehearsal = {
            "schema": "gis-ai-go.evidence-checkpoint-recovery-rehearsal.v1",
            "status": "passed",
            "mode": "deterministic-synthetic-non-live",
            "writer_lifecycle": "fixture-process-exited-before-checkpoint",
            "filesystem_observation": rehearsal_filesystem,
            "checkpoint_creation": "passed",
            "checkpoint_verification": "passed",
            "source_pair": "quarantined-without-deletion",
            "restore": "passed",
            "readiness": {
                "evidence_storage": "verified",
                "service": "not-started",
                "deployment": "not-evaluated",
            },
            "checkpoint_id": source_manifest["checkpoint_id"],
            "ledger_id": source_manifest["ledger"]["ledger_id"],
            "reconciliation_index_id": source_manifest[
                "reconciliation_index"
            ]["index_id"],
            "event_count": 1,
            "completed_claim_count": 1,
            "provider_calls": 0,
        }
        filesystem_validator = validator(
            "evidence-filesystem-capability-check.schema.json"
        )
        rehearsal_validator = validator(
            "evidence-checkpoint-recovery-rehearsal.schema.json"
        )
        self.assertEqual([], list(filesystem_validator.iter_errors(filesystem)))
        self.assertEqual([], list(rehearsal_validator.iter_errors(rehearsal)))

        omitted_fsync = copy.deepcopy(filesystem)
        omitted_fsync["checks"].remove("directory-fsync")
        self.assertTrue(list(filesystem_validator.iter_errors(omitted_fsync)))
        false_attestation = copy.deepcopy(filesystem)
        false_attestation["limitations"]["mount_identity_provenance"] = (
            "independently-attested"
        )
        self.assertTrue(list(filesystem_validator.iter_errors(false_attestation)))
        non_canonical_time = copy.deepcopy(filesystem)
        non_canonical_time["observed_at"] = "2026-08-30T08:30:00Z"
        self.assertTrue(list(filesystem_validator.iter_errors(non_canonical_time)))
        with_filesystem_path = copy.deepcopy(filesystem)
        with_filesystem_path["probe_directory"] = "/private/provider-mount"
        self.assertTrue(list(filesystem_validator.iter_errors(with_filesystem_path)))
        misclassified_rehearsal = copy.deepcopy(rehearsal)
        misclassified_rehearsal["filesystem_observation"]["classification"] = (
            "direct-filesystem-observation"
        )
        self.assertTrue(
            list(rehearsal_validator.iter_errors(misclassified_rehearsal))
        )
        promoted = copy.deepcopy(rehearsal)
        promoted["readiness"]["deployment"] = "passed"
        self.assertTrue(list(rehearsal_validator.iter_errors(promoted)))
        with_path = copy.deepcopy(rehearsal)
        with_path["rehearsal_root"] = "/private/rehearsal"
        self.assertTrue(list(rehearsal_validator.iter_errors(with_path)))


if __name__ == "__main__":
    unittest.main()
