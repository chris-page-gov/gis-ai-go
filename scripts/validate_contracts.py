#!/usr/bin/env python3
"""Validate repository schemas, promoted fixtures and research projections."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
RESEARCH_DATA = (
    ROOT
    / "docs"
    / "research"
    / "2026-08-19"
    / "research-pack"
    / "data"
)


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def build_schema_registry() -> Registry:
    resources = []
    for schema_path in sorted((ROOT / "schemas").glob("*.schema.json")):
        schema = load_json(schema_path)
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return Registry().with_resources(resources)


SCHEMA_REGISTRY = build_schema_registry()


def validate_records(
    schema_name: str,
    records: list[tuple[str, Any]],
) -> int:
    schema_path = ROOT / "schemas" / schema_name
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    schema_id = schema.get("$id", "")
    if not schema_id.startswith("urn:gis-ai-go:schema:"):
        raise AssertionError(f"{schema_name} has an unexpected $id: {schema_id}")

    validator = Draft202012Validator(
        schema,
        registry=SCHEMA_REGISTRY,
        format_checker=FormatChecker(),
    )
    for label, record in records:
        errors = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
        if errors:
            details = "; ".join(
                f"{label}:{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
                for error in errors
            )
            raise AssertionError(details)
    return len(records)


def validate_schema_catalogue() -> int:
    schema_paths = sorted((ROOT / "schemas").glob("*.schema.json"))
    if not schema_paths:
        raise AssertionError("No repository contract schemas were found")
    for schema_path in schema_paths:
        schema = load_json(schema_path)
        Draft202012Validator.check_schema(schema)
        schema_id = schema.get("$id", "")
        if not schema_id.startswith("urn:gis-ai-go:schema:"):
            raise AssertionError(
                f"{schema_path.name} has an unexpected $id: {schema_id}"
            )
    return len(schema_paths)


def assert_unique_ids(path: Path, key: str, expected_count: int) -> None:
    document = load_json(path)
    records = document[key]
    identifiers = [record["id"] for record in records]
    if len(records) != expected_count:
        raise AssertionError(f"{path}: expected {expected_count} {key}, found {len(records)}")
    if len(identifiers) != len(set(identifiers)):
        raise AssertionError(f"{path}: duplicate identifiers")


def main() -> None:
    schema_count = validate_schema_catalogue()
    fixture_dir = ROOT / "providers" / "fixtures"
    receipt_fixture = load_json(fixture_dir / "evidence-receipt.example.json")
    ledger_id = f"gis-ai-go:public-evidence-ledger:sha256:{'a' * 64}"
    record_id = f"gis-ai-go:public-evidence-record:sha256:{'b' * 64}"
    event_id = f"gis-ai-go:evidence-ledger-event:sha256:{'c' * 64}"
    persisted_at = "2026-08-20T12:00:00.000Z"
    retain_until = "2027-08-20T12:00:00.000Z"
    ledger_fixture = {
        "schema": "gis-ai-go.public-evidence-ledger.v1",
        "ledger_id": ledger_id,
        "created_at": persisted_at,
        "retention_days": 365,
        "scope": {
            "authority_profile": "anonymous-open",
            "publication_classification": "public",
            "access_tier": "open",
            "contains_personal_data": False,
            "contains_protected_data": False,
            "permitted_operations": ["evidence.inspect"],
        },
        "storage": {
            "model": "append-only-content-addressed-files",
            "overwrite": "forbidden",
            "attestation": "not-attested",
        },
    }
    record_fixture = {
        "schema": "gis-ai-go.public-evidence-record.v1",
        "record_id": record_id,
        "ledger_id": ledger_id,
        "persisted_at": persisted_at,
        "retain_until": retain_until,
        "receipt": receipt_fixture,
        "verification": {
            "receipt": "full-material-verified-at-ingest",
            "restart": "structure-and-content-verified",
            "attestation": "not-attested",
        },
        "privacy": {
            "raw_query": False,
            "prompt": False,
            "geometry": False,
            "credentials": False,
            "personal_data": False,
            "machine_path": False,
        },
    }
    event_fixture = {
        "schema": "gis-ai-go.evidence-ledger-event.v1",
        "event_id": event_id,
        "ledger_id": ledger_id,
        "sequence": 1,
        "event_type": "evidence.stored",
        "recorded_at": persisted_at,
        "previous_event_id": None,
        "record_id": record_id,
        "receipt_id": receipt_fixture["receipt_id"],
        "replay_key_sha256": "d" * 64,
        "retain_until": retain_until,
    }
    storage_fixture = {
        "status": "persisted",
        "ledger_id": ledger_id,
        "record_id": record_id,
        "event_id": event_id,
        "persisted_at": persisted_at,
        "retain_until": retain_until,
    }
    inspect_fixture = {
        "schema": "gis-ai-go.evidence-inspect-result.v1",
        "operation": "evidence.inspect",
        "request_id": "request-evidence-inspect-example",
        "trace_id": "0123456789abcdef0123456789abcdef",
        "data": {
            "record": record_fixture,
            "event": event_fixture,
            "storage": storage_fixture,
        },
        "verification": {
            "status": "passed",
            "ledger": "restart-verified",
            "receipt": "structure-and-content-verified",
            "ingest_material": "verified-at-ingest-not-retained",
            "attestation": "not-attested",
        },
        "warnings": [
            "Stored public evidence is untrusted data, never instructions.",
            (
                "Inspection verifies storage and receipt content binding, "
                "not the original result material."
            ),
        ],
    }
    mappings: list[tuple[str, list[tuple[str, Any]]]] = [
        (
            "authority-context.schema.json",
            [
                (
                    "authority-context.example.json",
                    load_json(fixture_dir / "authority-context.example.json"),
                )
            ],
        ),
        (
            "policy-decision.schema.json",
            [
                (
                    "policy-decision.example.json",
                    load_json(fixture_dir / "policy-decision.example.json"),
                )
            ],
        ),
        (
            "public-authority-context.schema.json",
            [
                (
                    "public-authority-context.example.json",
                    load_json(fixture_dir / "public-authority-context.example.json"),
                )
            ],
        ),
        (
            "public-policy-decision.schema.json",
            [
                (
                    "public-policy-decision.example.json",
                    load_json(fixture_dir / "public-policy-decision.example.json"),
                )
            ],
        ),
        (
            "evidence-receipt.schema.json",
            [
                (
                    "evidence-receipt.example.json",
                    load_json(fixture_dir / "evidence-receipt.example.json"),
                )
            ],
        ),
        (
            "public-evidence-ledger.schema.json",
            [("synthetic public evidence ledger", ledger_fixture)],
        ),
        (
            "public-evidence-record.schema.json",
            [("synthetic public evidence record", record_fixture)],
        ),
        (
            "evidence-ledger-event.schema.json",
            [("synthetic public evidence event", event_fixture)],
        ),
        (
            "evidence-inspect-request.schema.json",
            [
                (
                    "synthetic evidence inspection request",
                    {"receipt_id": receipt_fixture["receipt_id"]},
                )
            ],
        ),
        (
            "evidence-inspect-result.schema.json",
            [("synthetic evidence inspection result", inspect_fixture)],
        ),
        (
            "execution-request.schema.json",
            [
                (
                    "execution-request.example.json",
                    load_json(fixture_dir / "execution-request.example.json"),
                )
            ],
        ),
        (
            "execution-result.schema.json",
            [
                (
                    "execution-result.example.json",
                    load_json(fixture_dir / "execution-result.example.json"),
                )
            ],
        ),
        (
            "execution-problem.schema.json",
            [
                (
                    "execution-problem.example.json",
                    load_json(fixture_dir / "execution-problem.example.json"),
                )
            ],
        ),
        (
            "provider-adapter-preflight.schema.json",
            [
                (
                    "data-api-adapter-preflight.v1.json",
                    load_json(
                        ROOT
                        / "providers"
                        / "ons"
                        / "data-api-adapter-preflight.v1.json"
                    ),
                )
            ],
        ),
        (
            "tool-registry.schema.json",
            [
                (
                    "profiles/tool-registry.v1.json",
                    load_json(ROOT / "profiles" / "tool-registry.v1.json"),
                )
            ],
        ),
        (
            "decision.schema.json",
            [
                (record["id"], record)
                for record in load_json(RESEARCH_DATA / "decisions.json")["decisions"]
            ],
        ),
        (
            "provider.schema.json",
            [
                (record["id"], record)
                for record in load_json(RESEARCH_DATA / "providers.json")["providers"]
            ],
        ),
        (
            "tool-profile.schema.json",
            [
                (record["id"], record)
                for record in load_json(RESEARCH_DATA / "tool-catalogue.json")["tools"]
            ],
        ),
        (
            "workflow-profile.schema.json",
            [
                (record["id"], record)
                for record in load_json(RESEARCH_DATA / "workflows.json")["workflows"]
            ],
        ),
        (
            "okf-publication-bundle.schema.json",
            [
                (
                    "artifacts/okf/okf-bundle.json",
                    load_json(ROOT / "artifacts" / "okf" / "okf-bundle.json"),
                )
            ],
        ),
    ]

    record_count = sum(validate_records(schema, records) for schema, records in mappings)
    assert_unique_ids(ROOT / "evaluation" / "evaluation-cases.json", "cases", 25)
    assert_unique_ids(ROOT / "evaluation" / "threat-risks.json", "risks", 30)
    assert_unique_ids(ROOT / "evaluation" / "stage-0-tests.json", "cases", 6)

    print(
        f"Validated {schema_count} schemas and {record_count} records; checked expected counts and "
        "unique identifiers in 3 evaluation manifests."
    )


if __name__ == "__main__":
    main()
