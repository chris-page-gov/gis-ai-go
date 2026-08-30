#!/usr/bin/env python3
"""Verify provider-neutral deployment, HTTPS and live-provider evidence.

The verifier is deliberately offline. It validates closed contracts and their
cross-document identities; it does not make DNS, TLS, provider or deployment calls.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIRECTORY = ROOT / "schemas"
PLAN_SCHEMA = "deployment-admission-plan.schema.json"
TRANSPORT_SCHEMA = "remote-https-acceptance.schema.json"
LIVE_SCHEMA = "deployed-live-provider-evidence.schema.json"
FILESYSTEM_SCHEMA = "evidence-filesystem-capability-check.schema.json"
MAX_DOCUMENT_BYTES = 2 * 1024 * 1024
EXACT_OPERATIONS = (
    "catalogue.search",
    "catalogue.describe",
    "selection.resolve",
    "data.query",
    "evidence.inspect",
)
EXACT_RESOURCES = (
    "catalogue.public",
    "catalogue.record",
    "evidence.receipt",
)
SYNTHETIC_CLASSIFICATION = "synthetic-test-fixture"
RESERVED_TEST_HOSTNAMES = frozenset({"example.com", "example.net", "example.org"})
RESERVED_TEST_SUFFIXES = (".example", ".invalid", ".localhost", ".test")


class AdmissionVerificationError(ValueError):
    """Raised when an admission document fails closed verification."""


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise AdmissionVerificationError(f"document contains duplicate JSON key: {key}")
        value[key] = item
    return value


def _reject_json_constant(value: str) -> object:
    raise AdmissionVerificationError(f"document contains non-standard JSON value: {value}")


def _read_bounded_regular_file(path: Path, label: str) -> bytes:
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise AdmissionVerificationError(f"{label} is missing") from error
    if path.is_symlink() or not stat.S_ISREG(metadata.st_mode):
        raise AdmissionVerificationError(f"{label} must be a regular file, not a link")
    if metadata.st_size <= 0 or metadata.st_size > MAX_DOCUMENT_BYTES:
        raise AdmissionVerificationError(f"{label} exceeds the closed byte boundary")
    return path.read_bytes()


def _parse_document(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_json_object,
            parse_constant=_reject_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AdmissionVerificationError(f"{label} is not valid UTF-8 JSON") from error
    if not isinstance(value, dict):
        raise AdmissionVerificationError(f"{label} root must be an object")
    expected = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
    if raw != expected:
        raise AdmissionVerificationError(
            f"{label} must use the deterministic two-space JSON projection"
        )
    return value


def _schema_registry() -> Registry:
    resources = []
    for path in sorted(SCHEMA_DIRECTORY.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        resources.append((schema["$id"], Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def _validate_schema(document: dict[str, Any], schema_name: str, label: str) -> None:
    schema_path = SCHEMA_DIRECTORY / schema_name
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(
        schema,
        registry=_schema_registry(),
        format_checker=FormatChecker(),
    )
    errors = sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    if errors:
        details = "; ".join(
            f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in errors[:8]
        )
        raise AdmissionVerificationError(f"{label} failed schema validation: {details}")

    contract = document["schema_contract"]
    expected_path = f"schemas/{schema_name}"
    expected_digest = hashlib.sha256(schema_path.read_bytes()).hexdigest()
    if contract != {"path": expected_path, "sha256": expected_digest}:
        raise AdmissionVerificationError(f"{label} does not bind the exact schema bytes")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _parse_time(value: str, label: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise AdmissionVerificationError(f"{label} is not a valid date-time") from error


def _origin_hostname(origin: str, label: str) -> str:
    parsed = urlsplit(origin)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port is not None
        or parsed.path
        or parsed.query
        or parsed.fragment
        or parsed.hostname != parsed.hostname.lower()
    ):
        raise AdmissionVerificationError(f"{label} is not one canonical HTTPS origin")
    if parsed.geturl() != origin:
        raise AdmissionVerificationError(f"{label} is not canonically serialised")
    return parsed.hostname


def _expect_equal(left: object, right: object, label: str) -> None:
    if left != right:
        raise AdmissionVerificationError(f"{label} does not match")


def _expect_sorted_unique(values: Iterable[str], label: str) -> None:
    observed = tuple(values)
    if observed != tuple(sorted(set(observed))):
        raise AdmissionVerificationError(f"{label} must be sorted and unique")


def _verify_plan(plan: dict[str, Any]) -> None:
    origin = plan["ingress"]["public_origin"]
    hostname = _origin_hostname(origin, "plan public origin")
    _expect_equal(plan["ingress"]["hostname"], hostname, "plan ingress hostname")
    _expect_equal(
        plan["ingress"]["accepted_hosts"],
        [hostname, f"{hostname}:443"],
        "plan accepted Host list",
    )
    _expect_equal(plan["ingress"]["accepted_origins"], [origin], "plan Origin list")
    _expect_equal(plan["ingress"]["health_probe_host"], hostname, "plan health Host")
    _expect_equal(tuple(plan["service"]["operations"]), EXACT_OPERATIONS, "plan operations")
    _expect_equal(tuple(plan["service"]["resources"]), EXACT_RESOURCES, "plan resources")
    _expect_sorted_unique(
        plan["controls"]["egress"]["allowed_path_prefixes"],
        "plan egress path prefixes",
    )
    synthetic = plan["classification"] == SYNTHETIC_CLASSIFICATION
    if not synthetic and (
        any(
            hostname == reserved or hostname.endswith(f".{reserved}")
            for reserved in RESERVED_TEST_HOSTNAMES
        )
        or any(hostname.endswith(suffix) for suffix in RESERVED_TEST_SUFFIXES)
    ):
        raise AdmissionVerificationError("a real plan cannot use a reserved test hostname")
    if (
        not synthetic
        and plan["controls"]["workload_identity"]["mechanism"] == "synthetic-fixture"
    ):
        raise AdmissionVerificationError("a real plan cannot use a synthetic workload identity")

    spend = plan["spend"]
    authorised = plan["status"] == "authorised-pending-deployment-evidence"
    if authorised != spend["authority_confirmed"]:
        raise AdmissionVerificationError("plan status and spend authority diverge")
    if authorised:
        controls = plan["controls"]
        if not all(
            (
                controls["single_writer"]["rollout_overlap_fenced"],
                controls["single_writer"]["maintenance_overlap_fenced"],
                controls["storage"]["rpo_defined"],
                controls["storage"]["rto_defined"],
                controls["storage"]["disposal_defined"],
                controls["observability"]["retention_defined"],
                plan["operator"]["all_assigned"],
            )
        ):
            raise AdmissionVerificationError(
                "an authorised plan must close fencing, recovery, retention and operator fields"
            )


def _verify_transport(plan: dict[str, Any], transport: dict[str, Any]) -> None:
    _expect_equal(transport["source"], plan["source"], "transport source identity")
    _expect_equal(transport["image"], plan["image"], "transport image identity")
    target = transport["target"]
    origin = plan["ingress"]["public_origin"]
    hostname = plan["ingress"]["hostname"]
    _expect_equal(target["public_origin"], origin, "transport public origin")
    _expect_equal(target["hostname"], hostname, "transport hostname")
    _expect_equal(
        target["deployed_manifest_digest"],
        plan["image"]["manifest_digest"],
        "deployed image manifest",
    )

    dns_tls = transport["dns_tls"]
    for key in ("dns_hostname", "sni_hostname"):
        _expect_equal(dns_tls[key], hostname, f"transport {key}")
    started = _parse_time(transport["observed_at"]["started"], "transport start")
    completed = _parse_time(transport["observed_at"]["completed"], "transport completion")
    not_before = _parse_time(dns_tls["certificate_not_before"], "certificate not-before")
    not_after = _parse_time(dns_tls["certificate_not_after"], "certificate not-after")
    if not (not_before <= started <= completed < not_after):
        raise AdmissionVerificationError(
            "transport observation is outside the certificate validity window"
        )

    plaintext = transport["plaintext"]
    if plaintext["outcome"] == "redirected-to-canonical-https":
        _expect_equal(plaintext["redirect_origin"], origin, "plaintext redirect origin")
    authority = transport["authority"]
    if authority["accepted_host"] not in plan["ingress"]["accepted_hosts"]:
        raise AdmissionVerificationError("transport accepted Host was not admitted by the plan")
    _expect_equal(authority["accepted_origin"], origin, "transport accepted Origin")
    _expect_equal(
        transport["endpoints"]["openapi"]["server_origin"],
        origin,
        "OpenAPI public origin",
    )
    _expect_equal(
        tuple(transport["capability"]["operations"]),
        EXACT_OPERATIONS,
        "transport operations",
    )
    _expect_equal(
        tuple(transport["capability"]["resources"]),
        EXACT_RESOURCES,
        "transport resources",
    )

    controls = transport["runtime_controls"]
    if (
        transport["classification"] != SYNTHETIC_CLASSIFICATION
        and controls["workload_identity"]["mechanism"] == "synthetic-fixture"
    ):
        raise AdmissionVerificationError(
            "real transport evidence cannot use a synthetic workload identity"
        )
    storage = controls["storage"]
    if storage["ledger_volume_id_sha256"] == storage["reconciliation_volume_id_sha256"]:
        raise AdmissionVerificationError("transport storage volumes are not distinct")
    recovery = controls["suspension_recovery"]
    _expect_equal(
        recovery["restored_manifest_digest"],
        plan["image"]["manifest_digest"],
        "restored image manifest",
    )
    rollback = controls["rollback"]
    _expect_equal(
        rollback["candidate_manifest_digest"],
        plan["image"]["manifest_digest"],
        "rollback candidate image manifest",
    )
    if rollback["previous_manifest_digest"] == rollback["candidate_manifest_digest"]:
        raise AdmissionVerificationError("rollback did not select a distinct previous image")


def _verify_live(
    transport_raw: bytes,
    transport: dict[str, Any],
    live: dict[str, Any],
) -> None:
    _expect_equal(live["source"], transport["source"], "live-provider source identity")
    _expect_equal(live["image"], transport["image"], "live-provider image identity")
    transport_target = transport["target"]
    live_target = live["target"]
    for key in (
        "provider",
        "deployment_id",
        "public_origin",
        "hostname",
        "deployed_manifest_digest",
    ):
        _expect_equal(live_target[key], transport_target[key], f"live-provider target {key}")
    _expect_equal(
        live["transport_binding"]["document_sha256"],
        _sha256(transport_raw),
        "live-provider transport document digest",
    )
    transport_completed = _parse_time(
        transport["observed_at"]["completed"], "transport completion"
    )
    live_started = _parse_time(live["observed_at"]["started"], "live-provider start")
    live_completed = _parse_time(live["observed_at"]["completed"], "live-provider completion")
    if not (transport_completed <= live_started <= live_completed):
        raise AdmissionVerificationError(
            "live-provider observation did not follow accepted transport evidence"
        )


def _verify_filesystem_check(
    raw: bytes,
    document: dict[str, Any],
    *,
    expected_document_sha256: str,
    expected_mount_identity_sha256: str,
    expected_classification: str,
    transport_started: datetime,
    label: str,
) -> None:
    _validate_schema(document, FILESYSTEM_SCHEMA, label)
    if document["status"] != "passed":
        raise AdmissionVerificationError(f"{label} did not pass")
    _expect_equal(_sha256(raw), expected_document_sha256, f"{label} document digest")
    _expect_equal(
        document["mount_identity_sha256"],
        expected_mount_identity_sha256,
        f"{label} mount identity",
    )
    _expect_equal(
        document["classification"],
        expected_classification,
        f"{label} classification",
    )
    observed_at = _parse_time(document["observed_at"], f"{label} observation time")
    if observed_at > transport_started:
        raise AdmissionVerificationError(f"{label} was observed after transport acceptance began")


def verify_documents(
    plan_path: Path,
    transport_path: Path | None = None,
    live_path: Path | None = None,
    ledger_filesystem_path: Path | None = None,
    reconciliation_filesystem_path: Path | None = None,
    *,
    expected_source_commit: str | None = None,
    expected_source_tree: str | None = None,
    expected_image_manifest: str | None = None,
    require_non_synthetic_contracts: bool = False,
) -> dict[str, object]:
    if live_path is not None and transport_path is None:
        raise AdmissionVerificationError("live-provider evidence requires transport evidence")
    filesystem_paths = (ledger_filesystem_path, reconciliation_filesystem_path)
    if transport_path is None and any(path is not None for path in filesystem_paths):
        raise AdmissionVerificationError("filesystem checks require transport evidence")
    if transport_path is not None and any(path is None for path in filesystem_paths):
        raise AdmissionVerificationError(
            "transport evidence requires both exact filesystem capability checks"
        )

    plan_raw = _read_bounded_regular_file(plan_path, "admission plan")
    plan = _parse_document(plan_raw, "admission plan")
    _validate_schema(plan, PLAN_SCHEMA, "admission plan")
    _verify_plan(plan)

    transport_raw: bytes | None = None
    transport: dict[str, Any] | None = None
    if transport_path is not None:
        transport_raw = _read_bounded_regular_file(transport_path, "transport evidence")
        transport = _parse_document(transport_raw, "transport evidence")
        _validate_schema(transport, TRANSPORT_SCHEMA, "transport evidence")
        _verify_transport(plan, transport)

    filesystem_documents: list[dict[str, Any]] = []
    if transport is not None:
        assert ledger_filesystem_path is not None
        assert reconciliation_filesystem_path is not None
        storage = transport["runtime_controls"]["storage"]
        expected_classification = (
            SYNTHETIC_CLASSIFICATION
            if transport["classification"] == SYNTHETIC_CLASSIFICATION
            else "direct-filesystem-observation"
        )
        transport_started = _parse_time(
            transport["observed_at"]["started"], "transport start"
        )
        for label, path, digest_key, identity_key in (
            (
                "ledger filesystem check",
                ledger_filesystem_path,
                "ledger_filesystem_check_sha256",
                "ledger_volume_id_sha256",
            ),
            (
                "reconciliation filesystem check",
                reconciliation_filesystem_path,
                "reconciliation_filesystem_check_sha256",
                "reconciliation_volume_id_sha256",
            ),
        ):
            raw = _read_bounded_regular_file(path, label)
            document = _parse_document(raw, label)
            _verify_filesystem_check(
                raw,
                document,
                expected_document_sha256=storage[digest_key],
                expected_mount_identity_sha256=storage[identity_key],
                expected_classification=expected_classification,
                transport_started=transport_started,
                label=label,
            )
            filesystem_documents.append(document)

    live_raw: bytes | None = None
    live: dict[str, Any] | None = None
    if live_path is not None:
        assert transport_raw is not None and transport is not None
        live_raw = _read_bounded_regular_file(live_path, "live-provider evidence")
        live = _parse_document(live_raw, "live-provider evidence")
        _validate_schema(live, LIVE_SCHEMA, "live-provider evidence")
        _verify_live(transport_raw, transport, live)

    documents = [
        plan,
        *(value for value in (transport, live) if value is not None),
        *filesystem_documents,
    ]
    classifications = {value["classification"] for value in documents}
    synthetic = SYNTHETIC_CLASSIFICATION in classifications
    if synthetic and classifications != {SYNTHETIC_CLASSIFICATION}:
        raise AdmissionVerificationError("synthetic and real admission evidence cannot be mixed")
    if transport is not None and not synthetic:
        if plan["status"] != "authorised-pending-deployment-evidence":
            raise AdmissionVerificationError(
                "real transport evidence requires an authorised admission plan"
            )
    if require_non_synthetic_contracts and synthetic:
        raise AdmissionVerificationError(
            "synthetic fixtures cannot satisfy non-synthetic contract mode"
        )
    if (
        require_non_synthetic_contracts
        and plan["status"] != "authorised-pending-deployment-evidence"
    ):
        raise AdmissionVerificationError(
            "non-synthetic deployment contracts require an authorised plan"
        )
    if require_non_synthetic_contracts and any(
        value is None
        for value in (
            expected_source_commit,
            expected_source_tree,
            expected_image_manifest,
        )
    ):
        raise AdmissionVerificationError(
            "non-synthetic contract mode requires independent source, tree and image expectations"
        )

    source = plan["source"]
    image = plan["image"]
    if expected_source_commit is not None:
        _expect_equal(source["commit"], expected_source_commit, "expected source commit")
    if expected_source_tree is not None:
        _expect_equal(source["tree"], expected_source_tree, "expected source tree")
    if expected_image_manifest is not None:
        _expect_equal(
            image["manifest_digest"], expected_image_manifest, "expected image manifest"
        )

    scope = "plan-only"
    if transport is not None:
        scope = "transport-only"
    if live is not None:
        scope = "transport-and-live-provider"
    return {
        "schema": "gis-ai-go.deployment-admission-verification.v1",
        "status": "passed",
        "evidence_scope": scope,
        "synthetic": synthetic,
        "admission_plan_contract_valid": True,
        "transport_evidence_contract_valid": transport is not None,
        "live_provider_evidence_contract_valid": live is not None,
        "filesystem_evidence_contracts_valid": len(filesystem_documents) == 2,
        "observation_provenance_attested": False,
        "release_ready": False,
        "source_commit": source["commit"],
        "source_tree": source["tree"],
        "image_manifest_digest": image["manifest_digest"],
        "plan_sha256": _sha256(plan_raw),
        "transport_sha256": None if transport_raw is None else _sha256(transport_raw),
        "live_provider_sha256": None if live_raw is None else _sha256(live_raw),
    }


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--transport", type=Path)
    parser.add_argument("--live-provider", type=Path)
    parser.add_argument("--ledger-filesystem-check", type=Path)
    parser.add_argument("--reconciliation-filesystem-check", type=Path)
    parser.add_argument("--expected-source-commit")
    parser.add_argument("--expected-source-tree")
    parser.add_argument("--expected-image-manifest")
    parser.add_argument("--require-non-synthetic-contracts", action="store_true")
    return parser.parse_args()


def main() -> None:
    arguments = _arguments()
    try:
        result = verify_documents(
            arguments.plan,
            arguments.transport,
            arguments.live_provider,
            arguments.ledger_filesystem_check,
            arguments.reconciliation_filesystem_check,
            expected_source_commit=arguments.expected_source_commit,
            expected_source_tree=arguments.expected_source_tree,
            expected_image_manifest=arguments.expected_image_manifest,
            require_non_synthetic_contracts=arguments.require_non_synthetic_contracts,
        )
    except AdmissionVerificationError as error:
        raise SystemExit(f"deployment admission failed: {error}") from error
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
