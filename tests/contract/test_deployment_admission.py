from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIRECTORY = ROOT / "schemas"
FIXTURE_DIRECTORY = ROOT / "tests" / "contract" / "fixtures"
PLAN_FIXTURE = FIXTURE_DIRECTORY / "deployment-admission-plan.synthetic.v1.json"
TRANSPORT_FIXTURE = FIXTURE_DIRECTORY / "remote-https-acceptance.synthetic.v1.json"
LIVE_FIXTURE = FIXTURE_DIRECTORY / "deployed-live-provider-evidence.synthetic.v1.json"
LEDGER_FILESYSTEM_FIXTURE = (
    FIXTURE_DIRECTORY / "evidence-filesystem-capability-check-ledger.synthetic.v1.json"
)
RECONCILIATION_FILESYSTEM_FIXTURE = (
    FIXTURE_DIRECTORY
    / "evidence-filesystem-capability-check-reconciliation.synthetic.v1.json"
)
sys.path.insert(0, str(ROOT / "scripts"))

from verify_deployment_admission import (  # noqa: E402
    AdmissionVerificationError,
    verify_documents,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def assert_closed_objects(test_case: unittest.TestCase, value: object, path: str) -> None:
    if isinstance(value, dict):
        if value.get("type") == "object":
            test_case.assertIs(
                value.get("additionalProperties"),
                False,
                f"{path} must reject unknown properties",
            )
        for key, item in value.items():
            assert_closed_objects(test_case, item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            assert_closed_objects(test_case, item, f"{path}[{index}]")


class DeploymentAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = load_json(PLAN_FIXTURE)
        self.transport = load_json(TRANSPORT_FIXTURE)
        self.live = load_json(LIVE_FIXTURE)
        self.ledger_filesystem = load_json(LEDGER_FILESYSTEM_FIXTURE)
        self.reconciliation_filesystem = load_json(RECONCILIATION_FILESYSTEM_FIXTURE)

    def run_mutation(
        self,
        target: str,
        mutation: Callable[[dict[str, Any]], None],
        *,
        include_live: bool = False,
    ) -> None:
        plan = copy.deepcopy(self.plan)
        transport = copy.deepcopy(self.transport)
        live = copy.deepcopy(self.live)
        mutation({"plan": plan, "transport": transport, "live": live}[target])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path = root / "plan.json"
            transport_path = root / "transport.json"
            live_path = root / "live.json"
            ledger_filesystem_path = root / "ledger-filesystem.json"
            reconciliation_filesystem_path = root / "reconciliation-filesystem.json"
            write_json(plan_path, plan)
            write_json(transport_path, transport)
            write_json(live_path, live)
            write_json(ledger_filesystem_path, self.ledger_filesystem)
            write_json(reconciliation_filesystem_path, self.reconciliation_filesystem)
            with self.assertRaises(AdmissionVerificationError):
                verify_documents(
                    plan_path,
                    transport_path,
                    live_path if include_live else None,
                    ledger_filesystem_path,
                    reconciliation_filesystem_path,
                )

    def test_schemas_are_valid_and_every_typed_object_is_closed(self) -> None:
        for name in (
            "deployment-admission-plan.schema.json",
            "remote-https-acceptance.schema.json",
            "deployed-live-provider-evidence.schema.json",
        ):
            schema = load_json(SCHEMA_DIRECTORY / name)
            Draft202012Validator.check_schema(schema)
            assert_closed_objects(self, schema, name)

    def test_synthetic_fixture_chain_is_valid_but_never_promoted(self) -> None:
        result = verify_documents(
            PLAN_FIXTURE,
            TRANSPORT_FIXTURE,
            LIVE_FIXTURE,
            LEDGER_FILESYSTEM_FIXTURE,
            RECONCILIATION_FILESYSTEM_FIXTURE,
        )
        self.assertEqual("transport-and-live-provider", result["evidence_scope"])
        self.assertIs(result["synthetic"], True)
        self.assertIs(result["transport_evidence_contract_valid"], True)
        self.assertIs(result["live_provider_evidence_contract_valid"], True)
        self.assertIs(result["filesystem_evidence_contracts_valid"], True)
        self.assertIs(result["observation_provenance_attested"], False)
        self.assertIs(result["release_ready"], False)

    def test_plan_and_transport_phases_remain_distinct(self) -> None:
        plan = verify_documents(PLAN_FIXTURE)
        transport = verify_documents(
            PLAN_FIXTURE,
            TRANSPORT_FIXTURE,
            ledger_filesystem_path=LEDGER_FILESYSTEM_FIXTURE,
            reconciliation_filesystem_path=RECONCILIATION_FILESYSTEM_FIXTURE,
        )
        self.assertEqual("plan-only", plan["evidence_scope"])
        self.assertEqual("transport-only", transport["evidence_scope"])
        self.assertIs(transport["live_provider_evidence_contract_valid"], False)

    def test_transport_requires_two_exact_filesystem_checks(self) -> None:
        with self.assertRaisesRegex(
            AdmissionVerificationError,
            "requires both exact filesystem capability checks",
        ):
            verify_documents(PLAN_FIXTURE, TRANSPORT_FIXTURE)
        with self.assertRaisesRegex(AdmissionVerificationError, "document digest"):
            verify_documents(
                PLAN_FIXTURE,
                TRANSPORT_FIXTURE,
                ledger_filesystem_path=RECONCILIATION_FILESYSTEM_FIXTURE,
                reconciliation_filesystem_path=LEDGER_FILESYSTEM_FIXTURE,
            )

    def test_synthetic_documents_cannot_satisfy_real_evidence_mode(self) -> None:
        with self.assertRaisesRegex(
            AdmissionVerificationError,
            "synthetic fixtures cannot satisfy non-synthetic contract mode",
        ):
            verify_documents(
                PLAN_FIXTURE,
                TRANSPORT_FIXTURE,
                LIVE_FIXTURE,
                LEDGER_FILESYSTEM_FIXTURE,
                RECONCILIATION_FILESYSTEM_FIXTURE,
                expected_source_commit=self.plan["source"]["commit"],
                expected_source_tree=self.plan["source"]["tree"],
                expected_image_manifest=self.plan["image"]["manifest_digest"],
                require_non_synthetic_contracts=True,
            )

    def test_non_synthetic_labels_remain_contract_valid_not_attested(self) -> None:
        plan = copy.deepcopy(self.plan)
        transport = copy.deepcopy(self.transport)
        live = copy.deepcopy(self.live)
        ledger_filesystem = copy.deepcopy(self.ledger_filesystem)
        reconciliation_filesystem = copy.deepcopy(self.reconciliation_filesystem)

        origin = "https://gateway.service.gov.uk"
        hostname = "gateway.service.gov.uk"
        plan["classification"] = "provider-neutral-pre-deployment-plan"
        plan["status"] = "authorised-pending-deployment-evidence"
        plan["ingress"].update(
            {
                "public_origin": origin,
                "hostname": hostname,
                "accepted_hosts": [hostname, f"{hostname}:443"],
                "accepted_origins": [origin],
                "health_probe_host": hostname,
            }
        )
        plan["controls"]["single_writer"].update(
            {"rollout_overlap_fenced": True, "maintenance_overlap_fenced": True}
        )
        plan["controls"]["workload_identity"].update(
            {
                "mechanism": "provider-managed-identity",
                "identity_subject": "fixture-subject",
            }
        )
        plan["controls"]["storage"].update(
            {"rpo_defined": True, "rto_defined": True, "disposal_defined": True}
        )
        plan["controls"]["observability"]["retention_defined"] = True
        plan["operator"].update(
            {
                "owner": "fixture-owner",
                "suspension_procedure": "docs/operations/suspend.md",
                "checkpoint_procedure": "docs/operations/checkpoint.md",
                "restore_procedure": "docs/operations/restore.md",
                "rollback_procedure": "docs/operations/rollback.md",
                "incident_route": "fixture-incident-route",
                "all_assigned": True,
            }
        )
        plan["spend"].update(
            {
                "authority_confirmed": True,
                "currency": "GBP",
                "monthly_limit": 1.0,
                "hard_stop_mechanism": "fixture-hard-stop",
                "cost_owner": "fixture-cost-owner",
            }
        )

        transport["classification"] = "direct-public-https-observation"
        transport["target"].update(
            {
                "provider": "azure-container-apps",
                "deployment_id": "gateway-candidate-01",
                "public_origin": origin,
                "hostname": hostname,
            }
        )
        transport["dns_tls"].update(
            {"dns_hostname": hostname, "sni_hostname": hostname}
        )
        transport["authority"].update(
            {"accepted_host": hostname, "accepted_origin": origin}
        )
        transport["plaintext"]["redirect_origin"] = origin
        transport["endpoints"]["openapi"]["server_origin"] = origin
        transport["runtime_controls"]["workload_identity"]["mechanism"] = (
            "provider-managed-identity"
        )
        ledger_filesystem["classification"] = "direct-filesystem-observation"
        reconciliation_filesystem["classification"] = "direct-filesystem-observation"

        live["classification"] = "deployed-bounded-live-provider-observation"
        live["target"].update(
            {
                key: transport["target"][key]
                for key in (
                    "provider",
                    "deployment_id",
                    "public_origin",
                    "hostname",
                    "deployed_manifest_digest",
                )
            }
        )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path = root / "plan.json"
            transport_path = root / "transport.json"
            live_path = root / "live.json"
            ledger_path = root / "ledger-filesystem.json"
            reconciliation_path = root / "reconciliation-filesystem.json"
            write_json(plan_path, plan)
            write_json(ledger_path, ledger_filesystem)
            write_json(reconciliation_path, reconciliation_filesystem)
            storage = transport["runtime_controls"]["storage"]
            storage["ledger_filesystem_check_sha256"] = hashlib.sha256(
                ledger_path.read_bytes()
            ).hexdigest()
            storage["reconciliation_filesystem_check_sha256"] = hashlib.sha256(
                reconciliation_path.read_bytes()
            ).hexdigest()
            write_json(transport_path, transport)
            live["transport_binding"]["document_sha256"] = hashlib.sha256(
                transport_path.read_bytes()
            ).hexdigest()
            write_json(live_path, live)

            with self.assertRaisesRegex(
                AdmissionVerificationError,
                "requires independent source, tree and image expectations",
            ):
                verify_documents(
                    plan_path,
                    transport_path,
                    live_path,
                    ledger_path,
                    reconciliation_path,
                    require_non_synthetic_contracts=True,
                )
            result = verify_documents(
                plan_path,
                transport_path,
                live_path,
                ledger_path,
                reconciliation_path,
                expected_source_commit=plan["source"]["commit"],
                expected_source_tree=plan["source"]["tree"],
                expected_image_manifest=plan["image"]["manifest_digest"],
                require_non_synthetic_contracts=True,
            )

        self.assertIs(result["synthetic"], False)
        self.assertIs(result["transport_evidence_contract_valid"], True)
        self.assertIs(result["live_provider_evidence_contract_valid"], True)
        self.assertIs(result["observation_provenance_attested"], False)
        self.assertIs(result["release_ready"], False)
        self.assertNotIn("public_deployment_verified", result)
        self.assertNotIn("live_provider_verified", result)

    def test_expected_source_tree_and_image_are_bound(self) -> None:
        result = verify_documents(
            PLAN_FIXTURE,
            TRANSPORT_FIXTURE,
            ledger_filesystem_path=LEDGER_FILESYSTEM_FIXTURE,
            reconciliation_filesystem_path=RECONCILIATION_FILESYSTEM_FIXTURE,
            expected_source_commit=self.plan["source"]["commit"],
            expected_source_tree=self.plan["source"]["tree"],
            expected_image_manifest=self.plan["image"]["manifest_digest"],
        )
        self.assertEqual(self.plan["source"]["tree"], result["source_tree"])
        with self.assertRaises(AdmissionVerificationError):
            verify_documents(
                PLAN_FIXTURE,
                TRANSPORT_FIXTURE,
                ledger_filesystem_path=LEDGER_FILESYSTEM_FIXTURE,
                reconciliation_filesystem_path=RECONCILIATION_FILESYSTEM_FIXTURE,
                expected_source_tree="0" * 40,
            )

    def test_contracts_reject_unknown_fields_and_operation_or_resource_drift(self) -> None:
        mutations: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
            ("unknown root", lambda value: value.__setitem__("unexpected", True)),
            (
                "operation reordering",
                lambda value: value["service"]["operations"].reverse(),
            ),
            (
                "resource replacement",
                lambda value: value["service"]["resources"].__setitem__(
                    2, "workflow.execute"
                ),
            ),
        )
        for label, mutation in mutations:
            with self.subTest(label=label):
                self.run_mutation("plan", mutation)

    def test_plan_rejects_authority_and_spend_shortcuts(self) -> None:
        mutations: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
            (
                "forwarded headers as authority",
                lambda value: value["ingress"].__setitem__(
                    "forwarded_headers_are_authority", True
                ),
            ),
            (
                "budget alert as hard stop",
                lambda value: value["spend"].__setitem__(
                    "budget_alert_is_hard_stop", True
                ),
            ),
            (
                "static workload credentials",
                lambda value: value["controls"]["workload_identity"].__setitem__(
                    "static_credentials", True
                ),
            ),
            (
                "direct IP egress",
                lambda value: value["controls"]["egress"].__setitem__(
                    "direct_ip_egress_allowed", True
                ),
            ),
            (
                "missing hard-link semantics",
                lambda value: value["controls"]["storage"].__setitem__(
                    "hard_links", False
                ),
            ),
        )
        for label, mutation in mutations:
            with self.subTest(label=label):
                self.run_mutation("plan", mutation)

    def test_plan_rejects_origin_host_and_probe_divergence(self) -> None:
        mutations: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
            (
                "origin with port",
                lambda value: value["ingress"].__setitem__(
                    "public_origin", "https://gateway.example.com:443"
                ),
            ),
            (
                "host list widening",
                lambda value: value["ingress"]["accepted_hosts"].__setitem__(
                    1, "attacker.example.com"
                ),
            ),
            (
                "health probe divergence",
                lambda value: value["ingress"].__setitem__(
                    "health_probe_host", "probe.example.com"
                ),
            ),
        )
        for label, mutation in mutations:
            with self.subTest(label=label):
                self.run_mutation("plan", mutation)

    def test_transport_rejects_source_image_and_target_drift(self) -> None:
        mutations: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
            (
                "source tree drift",
                lambda value: value["source"].__setitem__("tree", "0" * 40),
            ),
            (
                "image drift",
                lambda value: value["image"].__setitem__(
                    "manifest_digest", "sha256:" + "0" * 64
                ),
            ),
            (
                "deployed digest drift",
                lambda value: value["target"].__setitem__(
                    "deployed_manifest_digest", "sha256:" + "0" * 64
                ),
            ),
            (
                "target hostname drift",
                lambda value: value["target"].__setitem__(
                    "hostname", "attacker.example.com"
                ),
            ),
        )
        for label, mutation in mutations:
            with self.subTest(label=label):
                self.run_mutation("transport", mutation)

    def test_transport_rejects_tls_and_plaintext_downgrade(self) -> None:
        mutations: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
            (
                "TLS 1.0 accepted",
                lambda value: value["dns_tls"].__setitem__(
                    "tls_1_0_rejected", False
                ),
            ),
            (
                "expired certificate",
                lambda value: value["dns_tls"].__setitem__(
                    "certificate_not_after", "2026-08-30T10:04:59Z"
                ),
            ),
            (
                "plaintext reaches gateway",
                lambda value: value["plaintext"].__setitem__(
                    "gateway_body_observed", True
                ),
            ),
            (
                "redirect to different authority",
                lambda value: value["plaintext"].__setitem__(
                    "redirect_origin", "https://attacker.example.com"
                ),
            ),
        )
        for label, mutation in mutations:
            with self.subTest(label=label):
                self.run_mutation("transport", mutation)

    def test_transport_rejects_authority_and_parity_failures(self) -> None:
        mutations: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
            (
                "forwarded Host substitutes",
                lambda value: value["authority"].__setitem__(
                    "forwarded_host_cannot_substitute", False
                ),
            ),
            (
                "wrong Origin accepted",
                lambda value: value["authority"].__setitem__("wrong_origin_status", 200),
            ),
            (
                "plain-text parity false",
                lambda value: value["capability"]["tool_checks"][3].__setitem__(
                    "structured_plain_text_parity", False
                ),
            ),
            (
                "receipt missing",
                lambda value: value["capability"]["tool_checks"][4].__setitem__(
                    "receipt_present", False
                ),
            ),
        )
        for label, mutation in mutations:
            with self.subTest(label=label):
                self.run_mutation("transport", mutation)

    def test_transport_rejects_runtime_control_failures(self) -> None:
        mutations: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
            (
                "overlapping writer admitted",
                lambda value: value["runtime_controls"]["single_writer_fencing"].__setitem__(
                    "maximum_observed_writers", 2
                ),
            ),
            (
                "static workload credential",
                lambda value: value["runtime_controls"]["workload_identity"].__setitem__(
                    "static_credentials", True
                ),
            ),
            (
                "unexpected egress not blocked",
                lambda value: value["runtime_controls"]["egress"].__setitem__(
                    "unexpected_domain_blocked", False
                ),
            ),
            (
                "hard links not verified",
                lambda value: value["runtime_controls"]["storage"].__setitem__(
                    "hard_links_verified", False
                ),
            ),
            (
                "secrets present in logs",
                lambda value: value["runtime_controls"]["logs"].__setitem__(
                    "secrets_absent", False
                ),
            ),
            (
                "restore image drift",
                lambda value: value["runtime_controls"]["suspension_recovery"].__setitem__(
                    "restored_manifest_digest", "sha256:" + "0" * 64
                ),
            ),
            (
                "rollback rebuilt",
                lambda value: value["runtime_controls"]["rollback"].__setitem__(
                    "selected_without_rebuild", False
                ),
            ),
            (
                "rollback uses candidate as previous",
                lambda value: value["runtime_controls"]["rollback"].__setitem__(
                    "previous_manifest_digest", value["image"]["manifest_digest"]
                ),
            ),
        )
        for label, mutation in mutations:
            with self.subTest(label=label):
                self.run_mutation("transport", mutation)

    def test_live_evidence_requires_exact_transport_source_image_and_target(self) -> None:
        mutations: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
            (
                "transport digest drift",
                lambda value: value["transport_binding"].__setitem__(
                    "document_sha256", "0" * 64
                ),
            ),
            (
                "source drift",
                lambda value: value["source"].__setitem__("commit", "0" * 40),
            ),
            (
                "target drift",
                lambda value: value["target"].__setitem__(
                    "deployment_id", "different-deployment"
                ),
            ),
            (
                "multiple provider executions",
                lambda value: value["call"].__setitem__(
                    "provider_execution_count", 2
                ),
            ),
            (
                "payload retained",
                lambda value: value["evidence_handling"].__setitem__(
                    "provider_payload_stored", True
                ),
            ),
        )
        for label, mutation in mutations:
            with self.subTest(label=label):
                self.run_mutation("live", mutation, include_live=True)

    def test_live_evidence_cannot_exist_without_transport(self) -> None:
        with self.assertRaisesRegex(
            AdmissionVerificationError, "requires transport evidence"
        ):
            verify_documents(PLAN_FIXTURE, live_path=LIVE_FIXTURE)

    def test_synthetic_and_real_classifications_cannot_be_mixed(self) -> None:
        self.run_mutation(
            "transport",
            lambda value: value.__setitem__(
                "classification", "direct-public-https-observation"
            ),
        )

    def test_real_plan_rejects_reserved_host_and_synthetic_identity(self) -> None:
        reserved = copy.deepcopy(self.plan)
        reserved["classification"] = "provider-neutral-pre-deployment-plan"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reserved.json"
            write_json(path, reserved)
            with self.assertRaisesRegex(AdmissionVerificationError, "reserved test hostname"):
                verify_documents(path)

        synthetic_identity = copy.deepcopy(reserved)
        synthetic_identity["ingress"].update(
            {
                "public_origin": "https://gateway.service.gov.uk",
                "hostname": "gateway.service.gov.uk",
                "accepted_hosts": [
                    "gateway.service.gov.uk",
                    "gateway.service.gov.uk:443",
                ],
                "accepted_origins": ["https://gateway.service.gov.uk"],
                "health_probe_host": "gateway.service.gov.uk",
            }
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic-identity.json"
            write_json(path, synthetic_identity)
            with self.assertRaisesRegex(AdmissionVerificationError, "synthetic workload identity"):
                verify_documents(path)

    def test_duplicate_noncanonical_and_linked_documents_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            duplicate = root / "duplicate.json"
            raw = PLAN_FIXTURE.read_text(encoding="utf-8")
            duplicate.write_text(
                raw.replace(
                    '  "schema": "gis-ai-go.deployment-admission-plan.v1",',
                    '  "schema": "gis-ai-go.deployment-admission-plan.v1",\n'
                    '  "schema": "gis-ai-go.deployment-admission-plan.v1",',
                    1,
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(AdmissionVerificationError, "duplicate JSON key"):
                verify_documents(duplicate)

            noncanonical = root / "noncanonical.json"
            noncanonical.write_text(json.dumps(self.plan), encoding="utf-8")
            with self.assertRaisesRegex(AdmissionVerificationError, "two-space JSON projection"):
                verify_documents(noncanonical)

            linked = root / "linked.json"
            linked.symlink_to(PLAN_FIXTURE)
            with self.assertRaisesRegex(AdmissionVerificationError, "regular file, not a link"):
                verify_documents(linked)


if __name__ == "__main__":
    unittest.main()
