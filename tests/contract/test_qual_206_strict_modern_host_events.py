from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
VERIFIER_PATH = ROOT / "scripts" / "verify_qual_206_strict_modern_host_events.py"
EVENT_SCHEMA_PATH = (
    ROOT / "schemas" / "qual-206-strict-modern-host-event-v1.schema.json"
)
CAPTURE_SCHEMA_PATH = (
    ROOT / "schemas" / "qual-206-strict-modern-host-event-capture-v1.schema.json"
)
SESSION_ID = "12345678-1234-4123-8123-123456789abc"
SOURCE_COMMIT = "0" * 40


def load_verifier() -> Any:
    specification = importlib.util.spec_from_file_location(
        "qual_206_strict_modern_host_event_verifier",
        VERIFIER_PATH,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load the QUAL-206 event verifier")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


VERIFIER = load_verifier()


def assert_contract_objects_are_closed(
    test_case: unittest.TestCase,
    node: object,
    path: str = "$",
) -> None:
    if isinstance(node, dict):
        if node.get("type") == "object":
            test_case.assertIs(
                node.get("additionalProperties"),
                False,
                f"{path} must reject unknown properties",
            )
        for key, value in node.items():
            assert_contract_objects_are_closed(test_case, value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            assert_contract_objects_are_closed(test_case, value, f"{path}[{index}]")


def session_start_fields() -> dict[str, Any]:
    digest = "a" * 64
    return {
        "client": "synthetic-test-host",
        "scenario": "independent-host",
        "source_commit": SOURCE_COMMIT,
        "catalogue_revision": "1" * 40,
        "protocol_target": "2026-07-28",
        "transport": "operating-system-stdio-pipes",
        "immediate_parent": {"bytes": 1, "sha256": digest},
        "source_checkout": {
            "detached_head": False,
            "head_matches_source_commit": False,
            "local_origin_main_matches_source_commit": False,
            "working_tree_clean": False,
        },
        "runtime_materials": {
            "bytes": 1,
            "file_count": 1,
            "manifest_sha256": "b" * 64,
        },
        "capture_boundaries": {
            "maximum_event_count": 512,
            "maximum_event_log_bytes": 8388608,
            "maximum_frame_bytes": 1048576,
            "maximum_idle_milliseconds": 30000,
            "maximum_session_milliseconds": 120000,
            "maximum_stderr_bytes": 65536,
        },
        "server_runtime": {
            "node_version": "v24.0.0",
            "executable_bytes": 1,
            "executable_sha256": digest,
            "collector_source_sha256": "c" * 64,
            "fixture_source_sha256": "d" * 64,
            "provider_egress_guard_source_sha256": "e" * 64,
            "command_sha256": "f" * 64,
        },
        "credential_environment_forwarded": False,
        "host_attribution": "immediate-parent-executable-only-unscored",
    }


def event_core(sequence: int, event: str, previous: str | None) -> dict[str, Any]:
    return {
        "schema": "gis-ai-go.qual-206-strict-modern-host-event.v1",
        "session_id": SESSION_ID,
        "sequence": sequence,
        "observed_at": f"2026-08-25T03:00:{sequence:02d}.000Z",
        "event": event,
        "previous_event_sha256": previous,
    }


def audit_fields(
    kind: str,
    *,
    ordinal: int | None = None,
    scenario: str = "not-applicable",
) -> dict[str, Any]:
    return {
        "audit_kind": kind,
        "contract_valid": True,
        "scenario": scenario,
        "ordinal": ordinal,
        "guarded_apis_exact": True if kind == "provider-egress-guard-ready" else None,
        "guarded_api_invocation_count": None,
        "source_commit_match": None,
        "state": "not-applicable",
        "production_registration": None,
        "operations_exact": None,
        "resources_exact": None,
        "suspensions_empty": None,
        "provider_transport_calls": None,
        "aborted_provider_calls": None,
        "ledger_event_count": None,
        "reported_error_count": None,
    }


def encode_event(core: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    value = copy.deepcopy(core)
    value["event_sha256"] = VERIFIER.domain_separated_sha256(value)
    return value, VERIFIER.canonical_json_bytes(value) + b"\n"


def make_capture(
    mutate_events: Callable[[list[dict[str, Any]]], None] | None = None,
) -> tuple[bytes, bytes]:
    specifications: list[dict[str, Any]] = [
        {"event": "session_start", **session_start_fields()},
        {
            "event": "child_spawned",
            "spawn_arguments_match_collector_contract": True,
            "spawned_process_identity_verified": False,
        },
        {"event": "stream_end", "stream": "host-stdin", "bytes": 0,
         "frame_count": 0, "graceful": True},
        {"event": "stream_end", "stream": "server-stdout", "bytes": 0,
         "frame_count": 0, "graceful": True},
        {"event": "stream_end", "stream": "server-stderr", "bytes": 0,
         "frame_count": 0, "graceful": True},
        {"event": "stream_end", "stream": "server-audit", "bytes": 0,
         "frame_count": 0, "graceful": True},
        {"event": "child_exit", "exit_code": 1, "signal": None},
    ]
    if mutate_events is not None:
        mutate_events(specifications)

    encoded: list[bytes] = []
    previous: str | None = None
    values: list[dict[str, Any]] = []
    for sequence, specification in enumerate(specifications):
        core = event_core(sequence, specification["event"], previous)
        core.update({key: value for key, value in specification.items() if key != "event"})
        value, line = encode_event(core)
        encoded.append(line)
        values.append(value)
        previous = value["event_sha256"]

    prior = b"".join(encoded)
    end_core = event_core(len(encoded), "session_end", previous)
    end_core.update(
        {
            "protocol_session_status": "failed",
            "capability_scored": False,
            "exact_five_host_capability": False,
            "source_binding_ready": False,
            "local_checkout_candidate_ready": False,
            "runtime_materials_stable": True,
            "exit_code": 1,
            "signal": None,
            "request_count": 0,
            "response_count": 0,
            "notification_count": 0,
            "pending_request_count": 0,
            "cancelled_request_count": 0,
            "stderr_event_count": 0,
            "stderr_bytes": 0,
            "stderr_sha256": None,
            "anomaly_count": 0,
            "prior_event_count": len(encoded),
            "prior_event_log_bytes": len(prior),
            "prior_event_log_sha256": hashlib.sha256(prior).hexdigest(),
            "temporary_state_removed": True,
        }
    )
    end, end_line = encode_event(end_core)
    encoded.append(end_line)
    values.append(end)
    log = b"".join(encoded)
    manifest = {
        "schema": "gis-ai-go.qual-206-strict-modern-host-event-capture.v1",
        "event_schema": "gis-ai-go.qual-206-strict-modern-host-event.v1",
        "source_commit": SOURCE_COMMIT,
        "session_id": SESSION_ID,
        "status": "complete",
        "protocol_session_status": "failed",
        "capability_scored": False,
        "exact_five_host_capability": False,
        "source_binding_ready": False,
        "local_checkout_candidate_ready": False,
        "event_log": {
            "bytes": len(log),
            "event_count": len(encoded),
            "last_event_sha256": end["event_sha256"],
            "sha256": hashlib.sha256(log).hexdigest(),
        },
    }
    return log, VERIFIER.canonical_json_bytes(manifest) + b"\n"


def make_passed_capture(
    mutate_events: Callable[[list[dict[str, Any]]], None] | None = None,
) -> tuple[bytes, bytes]:
    specifications: list[dict[str, Any]] = [
        {"event": "session_start", **session_start_fields()},
        {
            "event": "child_spawned",
            "spawn_arguments_match_collector_contract": True,
            "spawned_process_identity_verified": False,
        },
    ]
    request_frame_bytes: list[int] = []
    response_frame_bytes: list[int] = []
    notification_frame_bytes = 19
    for ordinal, (method, operation, resource) in enumerate(VERIFIER.EXPECTED_REQUESTS):
        request_digest = hashlib.sha256(f"request-{ordinal}".encode()).hexdigest()
        request_kind = "integer" if ordinal % 2 == 0 else "string"
        frame_bytes = 31 + ordinal
        request_frame_bytes.append(frame_bytes)
        specifications.append(
            {
                "event": "client_request",
                "direction": "client-to-server",
                "frame_bytes": frame_bytes,
                "frame_sha256": hashlib.sha256(
                    f"request-frame-{ordinal}".encode()
                ).hexdigest(),
                "request_id_sha256": request_digest,
                "request_id_kind": request_kind,
                "request_id_unique": True,
                "method": method,
                "operation": operation,
                "resource": resource,
                "protocol_claim": "2026-07-28",
                "journey_ordinal": ordinal,
                "journey_semantic_valid": True,
                "parameters_bytes": ordinal,
                "parameters_sha256": hashlib.sha256(
                    f"parameters-{ordinal}".encode()
                ).hexdigest(),
            }
        )
        if ordinal == 12:
            specifications.append(
                {
                    "event": "client_notification",
                    "direction": "client-to-server",
                    "frame_bytes": notification_frame_bytes,
                    "frame_sha256": hashlib.sha256(b"notification-frame").hexdigest(),
                    "method": "notifications/cancelled",
                    "protocol_claim": "2026-07-28",
                    "target_request_id_sha256": request_digest,
                    "target_request_id_kind": request_kind,
                    "target_matched_pending_data_query": True,
                    "parameters_bytes": 1,
                    "parameters_sha256": hashlib.sha256(
                        b"notification-parameters"
                    ).hexdigest(),
                }
            )
            continue
        semantic, outcome, error_code, facts = VERIFIER._expected_response_projection(
            ordinal
        )
        response_bytes = 61 + ordinal
        response_frame_bytes.append(response_bytes)
        specifications.append(
            {
                "event": "server_response",
                "direction": "server-to-client",
                "frame_bytes": response_bytes,
                "frame_sha256": hashlib.sha256(
                    f"response-frame-{ordinal}".encode()
                ).hexdigest(),
                "request_id_sha256": request_digest,
                "request_id_kind": request_kind,
                "correlation": "matched",
                "request_method": method,
                "operation": operation,
                "resource": resource,
                "outcome": outcome,
                "error_code": error_code,
                "duration_ms": 1,
                "semantic": semantic,
                "facts": facts,
            }
        )

    for identity in VERIFIER.EXPECTED_AUDIT_ORDER:
        specifications.append(
            {
                "event": "server_audit",
                **VERIFIER._expected_audit_projection(identity),
            }
        )
    specifications.extend(
        [
            {
                "event": "stream_end",
                "stream": "host-stdin",
                "bytes": sum(request_frame_bytes) + notification_frame_bytes,
                "frame_count": 15,
                "graceful": True,
            },
            {
                "event": "stream_end",
                "stream": "server-stdout",
                "bytes": sum(response_frame_bytes),
                "frame_count": 13,
                "graceful": True,
            },
            {
                "event": "stream_end",
                "stream": "server-stderr",
                "bytes": 0,
                "frame_count": 0,
                "graceful": True,
            },
            {
                "event": "stream_end",
                "stream": "server-audit",
                "bytes": 6,
                "frame_count": 6,
                "graceful": True,
            },
            {"event": "child_exit", "exit_code": 0, "signal": None},
        ]
    )
    if mutate_events is not None:
        mutate_events(specifications)

    encoded: list[bytes] = []
    previous: str | None = None
    for sequence, specification in enumerate(specifications):
        core = event_core(sequence, specification["event"], previous)
        core.update({key: value for key, value in specification.items() if key != "event"})
        value, line = encode_event(core)
        encoded.append(line)
        previous = value["event_sha256"]

    prior = b"".join(encoded)
    end_core = event_core(len(encoded), "session_end", previous)
    end_core.update(
        {
            "protocol_session_status": "passed",
            "capability_scored": False,
            "exact_five_host_capability": False,
            "source_binding_ready": False,
            "local_checkout_candidate_ready": False,
            "runtime_materials_stable": True,
            "exit_code": 0,
            "signal": None,
            "request_count": 14,
            "response_count": 13,
            "notification_count": 1,
            "pending_request_count": 0,
            "cancelled_request_count": 1,
            "stderr_event_count": 0,
            "stderr_bytes": 0,
            "stderr_sha256": None,
            "anomaly_count": 0,
            "prior_event_count": len(encoded),
            "prior_event_log_bytes": len(prior),
            "prior_event_log_sha256": hashlib.sha256(prior).hexdigest(),
            "temporary_state_removed": True,
        }
    )
    end, end_line = encode_event(end_core)
    encoded.append(end_line)
    log = b"".join(encoded)
    manifest = {
        "schema": "gis-ai-go.qual-206-strict-modern-host-event-capture.v1",
        "event_schema": "gis-ai-go.qual-206-strict-modern-host-event.v1",
        "source_commit": SOURCE_COMMIT,
        "session_id": SESSION_ID,
        "status": "complete",
        "protocol_session_status": "passed",
        "capability_scored": False,
        "exact_five_host_capability": False,
        "source_binding_ready": False,
        "local_checkout_candidate_ready": False,
        "event_log": {
            "bytes": len(log),
            "event_count": len(encoded),
            "last_event_sha256": end["event_sha256"],
            "sha256": hashlib.sha256(log).hexdigest(),
        },
    }
    return log, VERIFIER.canonical_json_bytes(manifest) + b"\n"


def refresh_manifest(log: bytes, manifest_raw: bytes) -> bytes:
    manifest = json.loads(manifest_raw)
    lines = log.splitlines()
    last = json.loads(lines[-1])
    manifest["event_log"].update(
        {
            "bytes": len(log),
            "event_count": len(lines),
            "last_event_sha256": last["event_sha256"],
            "sha256": hashlib.sha256(log).hexdigest(),
        }
    )
    return VERIFIER.canonical_json_bytes(manifest) + b"\n"


class Qual206StrictModernHostEventContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT)
        self.root = Path(self.temporary.name).resolve()
        self.root.chmod(0o700)
        self.event_log = self.root / "events.jsonl"
        self.manifest = self.root / "capture.json"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_capture(self, log: bytes, manifest: bytes) -> None:
        self.event_log.write_bytes(log)
        self.manifest.write_bytes(manifest)
        self.event_log.chmod(0o600)
        self.manifest.chmod(0o600)

    def test_schemas_are_valid_and_every_object_is_closed(self) -> None:
        for path in (EVENT_SCHEMA_PATH, CAPTURE_SCHEMA_PATH):
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            assert_contract_objects_are_closed(self, schema)

    def test_real_collector_journey_passes_the_independent_replay(self) -> None:
        completed = subprocess.run(
            [
                "node",
                "--test",
                "tests/interoperability/test_qual_206_event_collector.mjs",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            encoding="utf-8",
            env={**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
            timeout=60,
        )
        diagnostics = f"{completed.stdout}\n{completed.stderr}"[-16_384:]
        self.assertEqual(completed.returncode, 0, diagnostics)

    def test_verifier_accepts_one_complete_unscored_capture(self) -> None:
        log, manifest = make_capture()
        self.write_capture(log, manifest)
        result = VERIFIER.verify_capture(self.event_log, self.manifest)
        self.assertEqual(result.event_count, 8)
        self.assertEqual(result.protocol_session_status, "failed")

    def test_verifier_accepts_one_exact_replayed_passed_capture(self) -> None:
        log, manifest = make_passed_capture()
        self.write_capture(log, manifest)
        result = VERIFIER.verify_capture(self.event_log, self.manifest)
        self.assertEqual(result.event_count, 42)
        self.assertEqual(result.protocol_session_status, "passed")

    def test_verifier_rejects_a_rehashed_forged_passed_request_projection(self) -> None:
        def forge_projection(specifications: list[dict[str, Any]]) -> None:
            request = next(
                event
                for event in specifications
                if event["event"] == "client_request"
                and event["journey_ordinal"] == 6
            )
            request["journey_semantic_valid"] = False

        log, manifest = make_passed_capture(forge_projection)
        self.write_capture(log, manifest)
        with self.assertRaisesRegex(VERIFIER.VerificationError, "request projection"):
            VERIFIER.verify_capture(self.event_log, self.manifest)

    def test_verifier_rejects_rehashed_forged_passed_response_facts(self) -> None:
        def forge_projection(specifications: list[dict[str, Any]]) -> None:
            response = next(
                event
                for event in specifications
                if event["event"] == "server_response"
                and event["operation"] == "catalogue.search"
            )
            response["facts"]["deterministic_result_valid"] = False

        log, manifest = make_passed_capture(forge_projection)
        self.write_capture(log, manifest)
        with self.assertRaisesRegex(VERIFIER.VerificationError, "response projection"):
            VERIFIER.verify_capture(self.event_log, self.manifest)

    def test_verifier_rejects_a_rehashed_forged_passed_stream_total(self) -> None:
        def forge_stream_total(specifications: list[dict[str, Any]]) -> None:
            stream = next(
                event
                for event in specifications
                if event["event"] == "stream_end" and event["stream"] == "host-stdin"
            )
            stream["bytes"] += 1

        log, manifest = make_passed_capture(forge_stream_total)
        self.write_capture(log, manifest)
        with self.assertRaisesRegex(VERIFIER.VerificationError, "host-stdin byte total"):
            VERIFIER.verify_capture(self.event_log, self.manifest)

    def test_verifier_rejects_a_recomputed_manifest_over_a_bad_event_hash(self) -> None:
        log, manifest = make_capture()
        lines = log.splitlines(keepends=True)
        end = json.loads(lines[-1])
        end["event_sha256"] = "9" * 64
        lines[-1] = VERIFIER.canonical_json_bytes(end) + b"\n"
        changed_log = b"".join(lines)
        self.write_capture(changed_log, refresh_manifest(changed_log, manifest))
        with self.assertRaisesRegex(VERIFIER.VerificationError, "event identity"):
            VERIFIER.verify_capture(self.event_log, self.manifest)

    def test_verifier_rejects_duplicate_json_members(self) -> None:
        log, manifest = make_capture()
        lines = log.splitlines(keepends=True)
        self.assertIn(b'"sequence":0', lines[0])
        lines[0] = lines[0].replace(b'"sequence":0', b'"sequence":0,"sequence":0')
        changed_log = b"".join(lines)
        self.write_capture(changed_log, refresh_manifest(changed_log, manifest))
        with self.assertRaisesRegex(VERIFIER.VerificationError, "duplicate object member"):
            VERIFIER.verify_capture(self.event_log, self.manifest)

    def test_verifier_rejects_a_mixed_session_even_with_a_rebuilt_chain(self) -> None:
        def change_session(specifications: list[dict[str, Any]]) -> None:
            specifications[1]["session_id_override"] = (
                "87654321-4321-4321-8321-cba987654321"
            )

        log, manifest = make_capture(change_session)
        lines = log.splitlines(keepends=True)
        child = json.loads(lines[1])
        child["session_id"] = child.pop("session_id_override")
        child_core = dict(child)
        child_core.pop("event_sha256")
        child["event_sha256"] = VERIFIER.domain_separated_sha256(child_core)
        lines[1] = VERIFIER.canonical_json_bytes(child) + b"\n"
        changed_log = b"".join(lines)
        self.write_capture(changed_log, refresh_manifest(changed_log, manifest))
        with self.assertRaisesRegex(VERIFIER.VerificationError, "mixes more than one session"):
            VERIFIER.verify_capture(self.event_log, self.manifest)

    def test_verifier_rejects_an_event_after_session_end(self) -> None:
        log, manifest = make_capture()
        end = json.loads(log.splitlines()[-1])
        extra_core = event_core(end["sequence"] + 1, "child_spawned", end["event_sha256"])
        extra_core.update(
            {
                "spawn_arguments_match_collector_contract": True,
                "spawned_process_identity_verified": False,
            }
        )
        _extra, extra_line = encode_event(extra_core)
        changed_log = log + extra_line
        self.write_capture(changed_log, refresh_manifest(changed_log, manifest))
        with self.assertRaisesRegex(VERIFIER.VerificationError, "after session_end"):
            VERIFIER.verify_capture(self.event_log, self.manifest)

    def test_verifier_rejects_an_incomplete_but_rehashed_log(self) -> None:
        log, manifest = make_capture()
        incomplete_log = b"".join(log.splitlines(keepends=True)[:-1])
        self.write_capture(incomplete_log, refresh_manifest(incomplete_log, manifest))
        with self.assertRaisesRegex(VERIFIER.VerificationError, "incomplete"):
            VERIFIER.verify_capture(self.event_log, self.manifest)

    def test_verifier_rejects_a_wrong_whole_log_digest(self) -> None:
        log, manifest_raw = make_capture()
        manifest = json.loads(manifest_raw)
        manifest["event_log"]["sha256"] = "7" * 64
        changed_manifest = VERIFIER.canonical_json_bytes(manifest) + b"\n"
        self.write_capture(log, changed_manifest)
        with self.assertRaisesRegex(VERIFIER.VerificationError, "whole-log digest"):
            VERIFIER.verify_capture(self.event_log, self.manifest)

    def test_verifier_rejects_duplicate_server_audit_identities(self) -> None:
        def duplicate_audit(specifications: list[dict[str, Any]]) -> None:
            audit = {"event": "server_audit", **audit_fields(
                "provider-egress-guard-ready"
            )}
            specifications[2:2] = [audit, copy.deepcopy(audit)]

        log, manifest = make_capture(duplicate_audit)
        self.write_capture(log, manifest)
        with self.assertRaisesRegex(VERIFIER.VerificationError, "duplicate server-audit"):
            VERIFIER.verify_capture(self.event_log, self.manifest)

    def test_verifier_rejects_reordered_server_audit_identities(self) -> None:
        def reorder_audit(specifications: list[dict[str, Any]]) -> None:
            specifications[2:2] = [
                {
                    "event": "server_audit",
                    **audit_fields(
                        "provider-transport-started",
                        ordinal=1,
                        scenario="independent-host",
                    ),
                },
                {
                    "event": "server_audit",
                    **audit_fields("provider-egress-guard-ready"),
                },
            ]

        log, manifest = make_capture(reorder_audit)
        self.write_capture(log, manifest)
        with self.assertRaisesRegex(VERIFIER.VerificationError, "reordered server-audit"):
            VERIFIER.verify_capture(self.event_log, self.manifest)

    def test_verifier_rejects_a_group_readable_capture(self) -> None:
        log, manifest = make_capture()
        self.write_capture(log, manifest)
        self.event_log.chmod(0o640)
        with self.assertRaisesRegex(VERIFIER.VerificationError, "mode 0600"):
            VERIFIER.verify_capture(self.event_log, self.manifest)

    def test_number_canonicalisation_matches_ecmascript_boundaries(self) -> None:
        self.assertEqual(VERIFIER.canonical_json(1e-6), "0.000001")
        self.assertEqual(VERIFIER.canonical_json(1e-7), "1e-7")
        self.assertEqual(VERIFIER.canonical_json(1e20), "100000000000000000000")
        self.assertEqual(VERIFIER.canonical_json(1e21), "1e+21")
        self.assertEqual(VERIFIER.canonical_json(-0.0), "0")


if __name__ == "__main__":
    unittest.main()
