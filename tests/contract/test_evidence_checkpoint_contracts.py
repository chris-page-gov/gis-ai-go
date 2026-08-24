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


if __name__ == "__main__":
    unittest.main()
