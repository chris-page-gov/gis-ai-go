#!/usr/bin/env python3
"""Build the deterministic GIS AI GO public-discovery OKF publication."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker

BUILDER_VERSION = "1.0.0"
GENERATED_MARKER = "gis-ai-go-okf-builder.v1\n"
PUBLIC_BASE = "https://chris-page-gov.github.io/gis-ai-go/"
HMLR_VENDOR = Path("okf/vendor/okf-landregistry/v0.3.0")
MAX_INPUT_FILE_BYTES = 16 * 1024 * 1024
MAX_INPUT_BYTES = 64 * 1024 * 1024
MAX_RECORDS = 10_000


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def canonical_record_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode() + b"\n"
    return hashlib.sha256(payload).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalise_datetime(value: str) -> str:
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return f"{value}T00:00:00Z"
    return value


def locked_path(root: Path, relative: str) -> Path:
    logical = PurePosixPath(relative)
    if logical.is_absolute() or ".." in logical.parts or not logical.parts:
        raise ValueError(f"unsafe locked path: {relative}")
    path = root.joinpath(*logical.parts)
    cursor = path
    while cursor != root:
        if cursor.is_symlink():
            raise ValueError(f"locked input must not be a symbolic link: {relative}")
        cursor = cursor.parent
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"locked path escapes repository: {relative}")
    if not path.is_file():
        raise ValueError(f"locked input is missing or not a file: {relative}")
    return path


def verify_source_lock(root: Path, source_lock: dict[str, Any]) -> list[dict[str, Any]]:
    if source_lock.get("algorithm") != "sha256":
        raise ValueError("source lock must use sha256")
    inputs = source_lock.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        raise ValueError("source lock must contain inputs")
    paths = [item.get("path") for item in inputs]
    if not all(isinstance(path, str) for path in paths):
        raise ValueError("source lock paths must be strings")
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise ValueError("source lock paths must be unique and lexicographically sorted")

    verified: list[dict[str, Any]] = []
    total_bytes = 0
    for item in inputs:
        relative = item.get("path")
        expected = item.get("sha256")
        role = item.get("role")
        if not isinstance(relative, str) or not isinstance(role, str):
            raise ValueError("source lock entries require path and role strings")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ValueError(f"invalid sha256 for locked input: {relative}")
        path = locked_path(root, relative)
        size = path.stat().st_size
        if size > MAX_INPUT_FILE_BYTES:
            raise ValueError(
                f"locked input exceeds {MAX_INPUT_FILE_BYTES} bytes: {relative}"
            )
        total_bytes += size
        if total_bytes > MAX_INPUT_BYTES:
            raise ValueError(f"locked inputs exceed {MAX_INPUT_BYTES} bytes in total")
        actual = sha256_file(path)
        if actual != expected:
            raise ValueError(
                f"locked input hash mismatch for {relative}: expected {expected}, found {actual}"
            )
        verified.append(
            {
                "path": relative,
                "role": role,
                "sha256": actual,
                "bytes": size,
            }
        )

    for controlled_root in (Path("okf/profile"), Path("okf/source"), HMLR_VENDOR):
        input_root = root / controlled_root
        if not input_root.is_dir() or input_root.is_symlink():
            raise ValueError(
                f"controlled input root is missing or is a symbolic link: {controlled_root}"
            )
        actual_paths: set[str] = set()
        for path in input_root.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"controlled inputs must not contain symbolic links: {path}")
            if path.is_file():
                actual_paths.add(path.relative_to(root).as_posix())
        locked_paths = {
            item["path"]
            for item in inputs
            if item["path"].startswith(f"{controlled_root}/")
        }
        if actual_paths != locked_paths:
            missing = sorted(locked_paths - actual_paths)
            extra = sorted(actual_paths - locked_paths)
            raise ValueError(
                f"controlled input inventory differs from the source lock for "
                f"{controlled_root}; missing={missing}, extra={extra}"
            )
    return verified


def validate_url(value: str) -> None:
    parsed = urlparse(value)
    if parsed.scheme:
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError(f"URL must use HTTPS: {value}")
        return
    logical = PurePosixPath(value)
    if logical.is_absolute() or ".." in logical.parts:
        raise ValueError(f"relative URL is unsafe: {value}")


def canonical_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def reject_forbidden_keys(value: Any, forbidden: set[str], path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if canonical_key(str(key)) in forbidden:
                raise ValueError(f"forbidden payload key at {path}.{key}")
            reject_forbidden_keys(child, forbidden, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_forbidden_keys(child, forbidden, f"{path}[{index}]")


def freshness(publication: dict[str, Any], observed_at: str) -> dict[str, str]:
    return {
        "observedAt": normalise_datetime(observed_at),
        "reviewedAt": publication["reviewed_at"],
        "staleAfter": publication["stale_after"],
        "status": "current",
    }


def publication_envelope() -> dict[str, Any]:
    return {
        "classification": "public",
        "containsPersonalData": False,
        "containsProtectedData": False,
    }


def research_source_record(
    source: dict[str, Any], publication: dict[str, Any]
) -> dict[str, Any]:
    url = source["url"]
    validate_url(url)
    notes = source.get("notes") or "Citation metadata only; consult the source for scope."
    return {
        "schema": "gis-ai-go-okf-concept.v1",
        "id": source["id"],
        "type": "source",
        "title": source["title"],
        "description": notes,
        "authority": {
            "class": "source-authoritative"
            if source.get("authority") == "primary"
            else "derived",
            "statement": (
                f"{source.get('authority', 'unclassified')} source recorded at "
                f"{source.get('maturity', 'unknown')} maturity."
            ),
            "source": url,
        },
        "publication": publication_envelope(),
        "access": {
            "tier": "open",
            "state": "public-metadata",
            "authentication": "None for the cited public evidence page.",
        },
        "rights": {
            "state": "metadata-citation",
            "recordLicence": "MIT",
            "describedResourceLicence": (
                "Source-specific; the source is cited, not relicensed."
            ),
            "attribution": source.get("organisation") or "Consult the named publisher.",
        },
        "freshness": freshness(publication, source["retrieved"]),
        "status": "external-source",
        "sourceRefs": [source["id"]],
        "limitations": [notes],
        "tags": sorted({source["source_type"], source["maturity"], "source"}),
        "details": {
            "url": url,
            "organisation": source.get("organisation"),
            "sourceType": source["source_type"],
            "maturity": source["maturity"],
            "published": source.get("published"),
            "retrieved": source["retrieved"],
            "commitSha": source.get("commit_sha"),
        },
    }


def provider_record(
    provider: dict[str, Any], publication: dict[str, Any]
) -> dict[str, Any]:
    source_refs = sorted(provider["source_ids"])
    return {
        "schema": "gis-ai-go-okf-concept.v1",
        "id": provider["id"],
        "type": "provider",
        "title": provider["name"],
        "description": provider["recommended_integration"],
        "authority": {
            "class": "derived",
            "statement": provider["authority"],
            "source": source_refs[0],
        },
        "publication": publication_envelope(),
        "access": {
            "tier": "open",
            "state": "public-metadata",
            "authentication": "No provider connection is made by this candidate bundle.",
        },
        "rights": {
            "state": "metadata-citation",
            "recordLicence": "MIT",
            "describedResourceLicence": provider["licence"],
            "attribution": provider["attribution"],
        },
        "freshness": freshness(publication, publication["reviewed_at"]),
        "status": "candidate-metadata",
        "sourceRefs": source_refs,
        "limitations": [
            provider["known_changes"],
            provider["quality_limitations"],
            "No live provider call, data distribution or service response is included.",
        ],
        "tags": ["hmlr", "open", "provider"],
        "details": {
            "geographicScope": provider["geographic_scope"],
            "datasetsServices": provider["datasets_services"],
            "identifiers": provider["identifiers"],
            "updateFrequency": provider["update_frequency"],
            "mechanisms": provider["mechanisms"],
            "formats": provider["formats"],
            "cost": provider["cost"],
            "recommendedIntegration": provider["recommended_integration"],
        },
    }


def workflow_record(
    workflow: dict[str, Any], publication: dict[str, Any]
) -> dict[str, Any]:
    source_refs = sorted(workflow["source_ids"])
    return {
        "schema": "gis-ai-go-okf-concept.v1",
        "id": workflow["id"],
        "type": "workflow",
        "title": workflow["name"],
        "description": workflow["purpose"],
        "authority": {
            "class": "project-authoritative",
            "statement": workflow["definition_authority"],
            "source": source_refs[0],
        },
        "publication": publication_envelope(),
        "access": {
            "tier": "open",
            "state": "planned-non-executing",
            "authentication": "Not applicable: this is a non-executing description.",
        },
        "rights": {
            "state": "project-mit",
            "recordLicence": "MIT",
            "describedResourceLicence": "Not applicable; this is a non-executing description.",
            "attribution": "Copyright © 2026 Chris Page.",
        },
        "freshness": freshness(publication, publication["reviewed_at"]),
        "status": "candidate-non-executing",
        "sourceRefs": source_refs,
        "limitations": [
            "Description only; no workflow runtime or provider execution exists in this release.",
        ],
        "tags": ["discovery", "open", "workflow"],
        "details": {
            "steps": workflow["steps"],
            "humanApproval": workflow["human_approval"],
            "entryCriteria": workflow["entry_criteria"],
            "exitCriteria": workflow["exit_criteria"],
            "rollback": workflow["rollback"],
        },
    }


def source_record_id(url: str) -> str:
    return f"hmlr-source:{sha256_bytes(url.encode())[:16]}"


def hmlr_source_record(
    source_id: str,
    url: str,
    referenced_by: Iterable[str],
    publication: dict[str, Any],
) -> dict[str, Any]:
    validate_url(url)
    parsed = urlparse(url)
    label = f"{parsed.netloc}{parsed.path}".rstrip("/")
    return {
        "schema": "gis-ai-go-okf-concept.v1",
        "id": source_id,
        "type": "source",
        "title": f"Official HMLR source: {label}",
        "description": "Public evidence page cited by the selected upstream metadata record.",
        "authority": {
            "class": "source-authoritative",
            "statement": (
                "Official publisher evidence remains authoritative for current scope "
                "and terms."
            ),
            "source": url,
        },
        "publication": publication_envelope(),
        "access": {
            "tier": "open",
            "state": "public-metadata",
            "authentication": "None for the cited public evidence page.",
        },
        "rights": {
            "state": "metadata-citation",
            "recordLicence": "CC BY 4.0 for upstream metadata; GIS AI GO additions are MIT.",
            "describedResourceLicence": (
                "Source-specific; the source is cited, not relicensed."
            ),
            "attribution": "Consult HM Land Registry and any named third-party terms.",
        },
        "freshness": freshness(publication, publication["observed_at"]),
        "status": "external-source",
        "sourceRefs": [source_id],
        "limitations": [
            "A public evidence page does not imply that linked data, services or "
            "attachments are open."
        ],
        "tags": ["hmlr", "official-source", "source"],
        "details": {
            "url": url,
            "referencedBy": sorted(referenced_by),
        },
    }


def hmlr_dataset_record(
    record: dict[str, Any],
    rights: dict[str, Any],
    source_refs: list[str],
    publication: dict[str, Any],
) -> dict[str, Any]:
    if rights["access_state"] != "public" or rights["rights_state"] != "open-with-conditions":
        raise ValueError(f"selected HMLR record does not have publishable rights: {record['id']}")
    actual = canonical_record_sha256(record)
    if actual != rights["curated_record_sha256"]:
        raise ValueError(f"selected HMLR record digest mismatch: {record['id']}")
    attribution = publication["attribution_by_record"].get(record["id"])
    if not attribution:
        raise ValueError(f"selected HMLR record lacks explicit attribution: {record['id']}")
    if "inspire" in record["id"].lower():
        caveats = " ".join(record["caveats"]).lower()
        if "indicative" not in caveats or not any(
            term in caveats for term in ("legal", "definitive")
        ):
            raise ValueError(f"selected INSPIRE record lacks a non-legal caveat: {record['id']}")

    return {
        "schema": "gis-ai-go-okf-concept.v1",
        "id": record["id"],
        "type": "dataset",
        "title": record["title"],
        "description": record["description"],
        "authority": {
            "class": "source-authoritative",
            "statement": (
                "Source metadata is publisher-authored; GIS AI GO provides only a "
                "deterministic, metadata-only projection."
            ),
            "source": rights["evidence_url"],
        },
        "publication": publication_envelope(),
        "access": {
            "tier": "open",
            "state": "public",
            "authentication": record["authentication"],
        },
        "rights": {
            "state": rights["rights_state"],
            "recordLicence": "CC BY 4.0 for upstream metadata; GIS AI GO additions are MIT.",
            "describedResourceLicence": record["licence"],
            "attribution": attribution,
        },
        "freshness": freshness(publication, record["observed_at"]),
        "status": "candidate-metadata",
        "sourceRefs": sorted(source_refs),
        "limitations": sorted(
            set(record["caveats"])
            | {"Metadata only; no provider distribution or feature payload is included."}
        ),
        "tags": sorted(set(record["topics"]) | {"hmlr", "metadata-only"}),
        "details": {
            "sourceNativeId": record["id"],
            "publisher": record["publisher"],
            "recordType": record["record_type"],
            "jurisdiction": record["jurisdiction"],
            "audience": record["audience"],
            "accessModel": record["access_model"],
            "cadence": record["cadence"],
            "formats": record["formats"],
            "publisherLastUpdated": record["publisher_last_updated"],
            "rightsRef": rights["rights_ref"],
            "classificationStatus": rights["classification_status"],
            "recordSha256": actual,
        },
    }


def product_record(publication: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "gis-ai-go-okf-concept.v1",
        "id": publication["id"],
        "type": "bundle",
        "title": publication["title"],
        "description": publication["description"],
        "authority": {
            "class": "project-authoritative",
            "statement": "GIS AI GO is authoritative only for this normalised publication.",
            "source": "S-OKF-SPEC",
        },
        "publication": publication_envelope(),
        "access": {
            "tier": "open",
            "state": "public-metadata",
            "authentication": "None.",
        },
        "rights": {
            "state": "project-mit",
            "recordLicence": "MIT",
            "describedResourceLicence": (
                "MIT for GIS AI GO original material; third-party records retain their terms."
            ),
            "attribution": "Copyright © 2026 Chris Page; see THIRD_PARTY.md.",
        },
        "freshness": freshness(publication, publication["observed_at"]),
        "status": "candidate",
        "sourceRefs": ["S-OKF-SPEC"],
        "limitations": publication["limitations"],
        "tags": ["geospatial", "governance", "metadata-only", "okf"],
        "details": {
            "okfVersion": publication["okf_version"],
            "profile": publication["profile"],
            "compatibilityProfile": publication["compatibility_profile"],
        },
    }


def select_unique(rows: list[dict[str, Any]], ids: list[str], label: str) -> list[dict[str, Any]]:
    by_id = {row["id"]: row for row in rows}
    if len(by_id) != len(rows):
        raise ValueError(f"duplicate IDs in {label}")
    missing = sorted(set(ids) - set(by_id))
    if missing:
        raise ValueError(f"missing selected IDs in {label}: {missing}")
    return [by_id[identifier] for identifier in ids]


def validate_reference_closure(records: list[dict[str, Any]]) -> None:
    identifiers = [record["id"] for record in records]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("generated record IDs are not unique")
    known = set(identifiers)
    for record in records:
        missing = sorted(set(record["sourceRefs"]) - known)
        if missing:
            raise ValueError(f"unresolved source references for {record['id']}: {missing}")


def build_records(root: Path, publication: dict[str, Any]) -> list[dict[str, Any]]:
    research_data = root / "docs/research/2026-08-19/research-pack/data"
    providers_doc = load_json(research_data / "providers.json")
    workflows_doc = load_json(research_data / "workflows.json")
    sources_doc = load_json(research_data / "sources.json")
    hmlr_records_doc = load_json(root / HMLR_VENDOR / "source/curated-records.json")
    hmlr_rights_doc = load_json(root / HMLR_VENDOR / "source/curated-rights-access.json")

    selected = publication["selected"]
    providers = select_unique(
        providers_doc["providers"], selected["research_provider_ids"], "providers"
    )
    workflows = select_unique(
        workflows_doc["workflows"], selected["research_workflow_ids"], "workflows"
    )
    hmlr_records = select_unique(
        hmlr_records_doc["records"], selected["hmlr_record_ids"], "HMLR records"
    )
    rights_rows = hmlr_rights_doc["classifications"]
    rights_by_id = {row["source_native_id"]: row for row in rights_rows}
    if len(rights_by_id) != len(rights_rows):
        raise ValueError("duplicate source-native IDs in HMLR rights classifications")

    referenced_research_sources = {
        source_id
        for row in providers + workflows
        for source_id in row.get("source_ids", [])
    } | {"S-OKF-SPEC"}
    selected_sources = select_unique(
        sources_doc["sources"], sorted(referenced_research_sources), "sources"
    )
    research_source_ids_by_url = {
        row["url"]: row["id"] for row in selected_sources if row["url"].startswith("https://")
    }

    url_references: dict[str, set[str]] = {}
    hmlr_source_refs: dict[str, list[str]] = {}
    for row in hmlr_records:
        refs: list[str] = []
        for url in row["source_urls"]:
            validate_url(url)
            source_id = research_source_ids_by_url.get(url, source_record_id(url))
            refs.append(source_id)
            if source_id.startswith("hmlr-source:"):
                url_references.setdefault(url, set()).add(row["id"])
        hmlr_source_refs[row["id"]] = refs

    records: list[dict[str, Any]] = [product_record(publication)]
    records.extend(provider_record(row, publication) for row in providers)
    records.extend(workflow_record(row, publication) for row in workflows)
    records.extend(research_source_record(row, publication) for row in selected_sources)
    for row in hmlr_records:
        rights = rights_by_id.get(row["id"])
        if not rights:
            raise ValueError(f"missing rights classification: {row['id']}")
        records.append(
            hmlr_dataset_record(
                row,
                rights,
                hmlr_source_refs[row["id"]],
                publication,
            )
        )
    for url, referenced_by in sorted(url_references.items()):
        records.append(
            hmlr_source_record(
                source_record_id(url),
                url,
                referenced_by,
                publication,
            )
        )

    records.sort(key=lambda record: (record["type"], record["id"]))
    if len(records) > MAX_RECORDS:
        raise ValueError(f"generated record count exceeds {MAX_RECORDS}")
    validate_reference_closure(records)
    return records


def validate_records(
    records: list[dict[str, Any]], profile: dict[str, Any], schema: dict[str, Any]
) -> None:
    required = set(profile["required_record_fields"])
    allowed_types = set(profile["record_types"])
    forbidden = {canonical_key(key) for key in profile["forbidden_payload_keys"]}
    concept_validator = Draft202012Validator(
        schema["$defs"]["concept"], format_checker=FormatChecker()
    )
    for record in records:
        missing = sorted(required - set(record))
        if missing:
            raise ValueError(f"record {record.get('id')} lacks fields: {missing}")
        if record["type"] not in allowed_types:
            raise ValueError(f"record type is not allowed: {record['type']}")
        reject_forbidden_keys(record, forbidden)
        for value in walk_urls(record):
            validate_url(value)
        errors = sorted(concept_validator.iter_errors(record), key=lambda error: list(error.path))
        if errors:
            detail = "; ".join(
                f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
                for error in errors
            )
            raise ValueError(f"record {record['id']} failed schema validation: {detail}")


def walk_urls(value: Any, key: str = "") -> Iterable[str]:
    if isinstance(value, dict):
        for child_key, child in value.items():
            if isinstance(child, str) and canonical_key(child_key) in {
                "profile",
                "source",
                "url",
            }:
                yield child
            else:
                yield from walk_urls(child, str(child_key))
    elif isinstance(value, list):
        for child in value:
            yield from walk_urls(child, key)


def record_iri(record: dict[str, Any]) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", record["id"].lower()).strip("-")[:64]
    suffix = sha256_bytes(record["id"].encode())[:10]
    return f"{PUBLIC_BASE}id/{record['type']}/{slug}-{suffix}"


def jsonld_document(bundle: dict[str, Any]) -> dict[str, Any]:
    iris = {record["id"]: record_iri(record) for record in bundle["records"]}
    graph = []
    for record in bundle["records"]:
        graph.append(
            {
                "@id": iris[record["id"]],
                "@type": f"okf:{record['type'].title()}",
                "recordSchema": record["schema"],
                "identifier": record["id"],
                "title": record["title"],
                "description": record["description"],
                "status": record["status"],
                "authority": record["authority"],
                "publication": record["publication"],
                "access": record["access"],
                "rights": record["rights"],
                "freshness": record["freshness"],
                "sourceIdentifier": record["sourceRefs"],
                "source": [{"@id": iris[source]} for source in record["sourceRefs"]],
                "limitations": record["limitations"],
                "tags": record["tags"],
                "details": record["details"],
            }
        )
    return {
        "@context": {
            "@version": 1.1,
            "@vocab": "https://chris-page-gov.github.io/okf-explorer/ns#",
            "okf": "https://chris-page-gov.github.io/okf-explorer/ns#",
            "dcterms": "http://purl.org/dc/terms/",
            "schema": "https://schema.org/",
            "identifier": "dcterms:identifier",
            "recordSchema": "okf:recordSchema",
            "title": "dcterms:title",
            "description": "dcterms:description",
            "status": "schema:creativeWorkStatus",
            "source": {"@id": "dcterms:source", "@type": "@id", "@container": "@set"},
            "sourceIdentifier": {"@id": "okf:sourceIdentifier", "@container": "@set"},
            "limitations": {"@id": "okf:limitation", "@container": "@set"},
            "tags": {"@id": "schema:keywords", "@container": "@set"},
            "authority": "okf:authority",
            "publication": "okf:publication",
            "access": "okf:access",
            "rights": "okf:rights",
            "freshness": "okf:freshness",
            "details": "okf:details",
        },
        "@id": f"{PUBLIC_BASE}id/bundle/public-discovery",
        "@type": "okf:Bundle",
        "title": bundle["title"],
        "description": bundle["description"],
        "version": bundle["version"],
        "okfVersion": bundle["okfVersion"],
        "@graph": graph,
    }


def markdown_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def markdown_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def record_output_path(record: dict[str, Any]) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", record["id"].lower()).strip("-")
    if not slug:
        raise ValueError(f"record ID cannot produce a safe output path: {record['id']}")
    return f"records/{record['type']}/{slug}.md"


def validate_output_paths(records: list[dict[str, Any]]) -> None:
    paths = [record_output_path(record) for record in records]
    if len(paths) != len(set(paths)):
        raise ValueError("record IDs produce colliding output paths")


def record_markdown(record: dict[str, Any]) -> bytes:
    lines = [
        "---",
        f"schema: {markdown_scalar(record['schema'])}",
        f"id: {markdown_scalar(record['id'])}",
        f"type: {markdown_scalar(record['type'])}",
        f"title: {markdown_scalar(record['title'])}",
        f"description: {markdown_scalar(record['description'])}",
        f"status: {markdown_scalar(record['status'])}",
        f"authority: {markdown_json(record['authority'])}",
        f"publication: {markdown_json(record['publication'])}",
        f"access: {markdown_json(record['access'])}",
        f"rights: {markdown_json(record['rights'])}",
        f"freshness: {markdown_json(record['freshness'])}",
        f"sourceRefs: {markdown_json(record['sourceRefs'])}",
        f"limitations: {markdown_json(record['limitations'])}",
        f"tags: {markdown_json(record['tags'])}",
        f"details: {markdown_json(record['details'])}",
        "---",
        "",
        f"# {record['title']}",
        "",
        record["description"],
        "",
        "## Publication boundary",
        "",
        f"- Classification: {record['publication']['classification']}",
        (
            "- Contains personal data: "
            f"{'yes' if record['publication']['containsPersonalData'] else 'no'}"
        ),
        (
            "- Contains protected data: "
            f"{'yes' if record['publication']['containsProtectedData'] else 'no'}"
        ),
        "",
        "## Authority",
        "",
        record["authority"]["statement"],
        f"- Authority source: `{record['authority']['source']}`",
        "",
        "## Access and rights",
        "",
        f"- Access: {record['access']['state']} ({record['access']['tier']})",
        f"- Authentication: {record['access']['authentication']}",
        f"- Rights state: {record['rights']['state']}",
        f"- Record licence: {record['rights']['recordLicence']}",
        f"- Described resource licence: {record['rights']['describedResourceLicence']}",
        f"- Attribution: {record['rights']['attribution']}",
        "",
        "## Freshness",
        "",
        f"- Observed: {record['freshness']['observedAt']}",
        f"- Reviewed: {record['freshness']['reviewedAt']}",
        f"- Stale after: {record['freshness']['staleAfter']}",
        "",
        "## Sources",
        "",
        *[f"- `{source}`" for source in record["sourceRefs"]],
        "",
        "## Limitations",
        "",
        *[f"- {limitation}" for limitation in record["limitations"]],
        "",
    ]
    return "\n".join(lines).encode()


def index_markdown(bundle: dict[str, Any]) -> bytes:
    lines = [
        "---",
        'type: "Knowledge Bundle"',
        f"title: {markdown_scalar(bundle['title'])}",
        f"status: {markdown_scalar(bundle['status'])}",
        f"okf_version: {markdown_scalar(bundle['okfVersion'])}",
        f"version: {markdown_scalar(bundle['version'])}",
        "---",
        "",
        "# GIS AI GO public discovery bundle",
        "",
        bundle["description"],
        "",
        "This is a metadata-only candidate. It does not execute provider services or",
        "establish property ownership, title extent or legal boundaries.",
        "",
        "## Records",
        "",
    ]
    for record in bundle["records"]:
        lines.append(f"- [{record['title']}]({record_output_path(record)})")
    lines.extend(
        [
            "",
            "## Machine-readable forms",
            "",
            "- [OKF bundle](okf-bundle.json)",
            "- [JSON-LD](okf-bundle.jsonld)",
            "- [Explorer descriptor](okf-explorer.json)",
            "- [Build receipt](build-receipt.json)",
            "",
        ]
    )
    return "\n".join(lines).encode()


def write_file(root: Path, relative: str, content: bytes) -> None:
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)


def prepare_output(output: Path) -> None:
    if output.is_symlink():
        raise ValueError(f"output directory must not be a symbolic link: {output}")
    if output.exists():
        marker = output / ".okf-generated"
        if not marker.is_file() or marker.read_text(encoding="utf-8") != GENERATED_MARKER:
            raise ValueError(f"refusing to replace unmarked output directory: {output}")
        shutil.rmtree(output)
    output.mkdir(parents=True)
    (output / ".okf-generated").write_text(GENERATED_MARKER, encoding="utf-8")


def existing_payloads(output: Path, excluded: set[str]) -> list[str]:
    return sorted(
        path.relative_to(output).as_posix()
        for path in output.rglob("*")
        if path.is_file()
        and path.relative_to(output).as_posix() not in excluded
        and path.name != ".okf-generated"
    )


def build(root: Path, output: Path, revision: str) -> dict[str, Any]:
    root = root.resolve()
    if output.is_symlink():
        raise ValueError(f"output directory must not be a symbolic link: {output}")
    output = output.resolve()
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("revision must be a 40-character lowercase Git SHA")

    source_lock_path = root / "okf/source-lock.json"
    source_lock = load_json(source_lock_path)
    verified_inputs = verify_source_lock(root, source_lock)
    publication = load_json(root / "okf/source/publication.json")
    profile = load_json(root / "okf/profile/public-discovery-v1.json")
    schema = load_json(root / "schemas/okf-publication-bundle.schema.json")
    version = (root / "VERSION").read_text(encoding="utf-8").strip()

    records = build_records(root, publication)
    validate_records(records, profile, schema)
    validate_output_paths(records)
    bundle = {
        "schema": "gis-ai-go-okf-bundle.v1",
        "id": f"{PUBLIC_BASE}id/bundle/public-discovery",
        "title": publication["title"],
        "description": publication["description"],
        "okfVersion": publication["okf_version"],
        "profile": publication["profile"],
        "profileStatus": profile["status"],
        "version": version,
        "revision": revision,
        "status": publication["status"],
        "authority": {
            "bundleAuthority": "Metadata normalisation and this publication only.",
            "officialSourceAuthority": "External live publisher sources.",
            "legalAdvice": False,
            "notEndorsedBySource": True,
        },
        "scope": {
            "kind": "bounded-public-metadata-discovery",
            "metadataOnly": True,
            "containsProtectedData": False,
            "excludes": [
                "authenticated, paid or user-submitted service content",
                "provider distributions and response bodies",
                "property, ownership, address and transaction rows",
                "real geometry and legal boundary determinations",
            ],
        },
        "rights": {
            "statement": (
                "GIS AI GO original material is MIT; each third-party record retains "
                "its recorded rights and conditions."
            ),
            "thirdPartyNotices": "THIRD_PARTY.md",
        },
        "observedAt": publication["observed_at"],
        "reviewedAt": publication["reviewed_at"],
        "staleAfter": publication["stale_after"],
        "recordCount": len(records),
        "records": records,
    }
    bundle_errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(bundle),
        key=lambda error: list(error.path),
    )
    if bundle_errors:
        detail = "; ".join(
            f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in bundle_errors
        )
        raise ValueError(f"generated bundle failed schema validation: {detail}")

    prepare_output(output)
    write_file(output, "THIRD_PARTY.md", (root / "THIRD_PARTY.md").read_bytes())
    write_file(
        output,
        "third-party/okf-landregistry-LICENSE.md",
        (root / HMLR_VENDOR / "LICENSE.md").read_bytes(),
    )
    write_file(output, "okf-bundle.json", canonical_json_bytes(bundle))
    jsonld = jsonld_document(bundle)
    write_file(output, "okf-bundle.jsonld", canonical_json_bytes(jsonld))
    write_file(output, "context.jsonld", canonical_json_bytes({"@context": jsonld["@context"]}))
    write_file(output, "index.md", index_markdown(bundle))
    for record in records:
        write_file(output, record_output_path(record), record_markdown(record))

    descriptor = {
        "schema": "gis-ai-go-okf-explorer.v1",
        "id": f"{PUBLIC_BASE}okf-explorer.json",
        "title": bundle["title"],
        "description": bundle["description"],
        "okfVersion": bundle["okfVersion"],
        "profile": bundle["profile"],
        "profileStatus": bundle["profileStatus"],
        "version": version,
        "revision": revision,
        "publicationState": "candidate",
        "counts": {
            "records": len(records),
            "types": {
                kind: sum(record["type"] == kind for record in records)
                for kind in sorted({record["type"] for record in records})
            },
        },
        "scope": bundle["scope"],
        "rights": bundle["rights"],
        "entrypoints": {
            "human": "index.md",
            "json": "okf-bundle.json",
            "jsonLd": "okf-bundle.jsonld",
            "checksums": "CHECKSUMS.sha256",
            "receipt": "build-receipt.json",
        },
    }
    write_file(output, "okf-explorer.json", canonical_json_bytes(descriptor))

    initial_files = existing_payloads(
        output, {"CHECKSUMS.sha256", "build-receipt.json", "manifest.json"}
    )
    manifest = {
        "schema": "gis-ai-go-okf-manifest.v1",
        "version": version,
        "revision": revision,
        "recordCount": len(records),
        "recordIds": [record["id"] for record in records],
        "files": [
            {
                "path": path,
                "bytes": (output / path).stat().st_size,
                "sha256": sha256_file(output / path),
            }
            for path in initial_files
        ],
    }
    write_file(output, "manifest.json", canonical_json_bytes(manifest))

    content_files = existing_payloads(output, {"CHECKSUMS.sha256", "build-receipt.json"})
    content_checksums = "".join(
        f"{sha256_file(output / path)}  {path}\n" for path in content_files
    ).encode()
    content_root = sha256_bytes(content_checksums)
    input_root = sha256_bytes(
        "".join(
            f"{item['sha256']}  {item['path']}\n" for item in verified_inputs
        ).encode()
    )
    receipt = {
        "schema": "gis-ai-go-okf-build-receipt.v1",
        "builder": "scripts/build_okf.py",
        "builderVersion": BUILDER_VERSION,
        "version": version,
        "revision": revision,
        "profile": profile["id"],
        "profileStatus": profile["status"],
        "sourceLockSha256": sha256_file(source_lock_path),
        "inputRootSha256": input_root,
        "inputs": verified_inputs,
        "recordCount": len(records),
        "outputCount": len(content_files) + 1,
        "checksumScope": (
            "All generated files except .okf-generated and CHECKSUMS.sha256, "
            "including build-receipt.json."
        ),
        "contentRootScope": (
            "All generated payload files except .okf-generated, CHECKSUMS.sha256 and "
            "build-receipt.json."
        ),
        "contentRootSha256": content_root,
        "manifestSha256": sha256_file(output / "manifest.json"),
        "determinism": {
            "canonicalJson": "sorted-key UTF-8 JSON with two-space indent and final newline",
            "pathOrder": "lexicographic",
            "wallClockIncluded": False,
            "checkoutPathIncluded": False,
        },
    }
    write_file(output, "build-receipt.json", canonical_json_bytes(receipt))
    checksum_files = existing_payloads(output, {"CHECKSUMS.sha256"})
    checksums = "".join(
        f"{sha256_file(output / path)}  {path}\n" for path in checksum_files
    ).encode()
    write_file(output, "CHECKSUMS.sha256", checksums)
    return receipt


def git_revision(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--revision")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    revision = args.revision or git_revision(root)
    receipt = build(root, output, revision)
    print(
        f"Built {receipt['recordCount']} OKF records into {output}; "
        f"content root {receipt['contentRootSha256']}."
    )


if __name__ == "__main__":
    main()
