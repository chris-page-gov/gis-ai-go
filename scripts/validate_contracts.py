#!/usr/bin/env python3
"""Validate Stage 0 schemas, promoted fixtures and research-record projections."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

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

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for label, record in records:
        errors = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
        if errors:
            details = "; ".join(
                f"{label}:{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
                for error in errors
            )
            raise AssertionError(details)
    return len(records)


def assert_unique_ids(path: Path, key: str, expected_count: int) -> None:
    document = load_json(path)
    records = document[key]
    identifiers = [record["id"] for record in records]
    if len(records) != expected_count:
        raise AssertionError(f"{path}: expected {expected_count} {key}, found {len(records)}")
    if len(identifiers) != len(set(identifiers)):
        raise AssertionError(f"{path}: duplicate identifiers")


def main() -> None:
    fixture_dir = ROOT / "providers" / "fixtures"
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
            "evidence-receipt.schema.json",
            [
                (
                    "evidence-receipt.example.json",
                    load_json(fixture_dir / "evidence-receipt.example.json"),
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
        f"Validated 8 schemas and {record_count} records; checked expected counts and "
        "unique identifiers in 3 evaluation manifests."
    )


if __name__ == "__main__":
    main()
