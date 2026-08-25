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
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
VERIFIER_PATH = ROOT / "scripts" / "verify_qual_206_claude_composite_observation.py"
EVENT_SCHEMA_PATH = (
    ROOT / "schemas" / "qual-206-claude-composite-host-event-v1.schema.json"
)
CAPTURE_SCHEMA_PATH = (
    ROOT
    / "schemas"
    / "qual-206-claude-composite-host-event-capture-v1.schema.json"
)
NODE_TEST_PATH = "tests/interoperability/test_qual_206_claude_stdio_observer.mjs"
RUN_ID = "12345678-1234-4123-8123-123456789abc"
OTHER_RUN_ID = "87654321-4321-4321-8321-cba987654321"
SESSION_IDS = (
    "11111111-1111-4111-8111-111111111111",
    "22222222-2222-4222-8222-222222222222",
)
SOURCE_COMMIT = "0" * 40
OTHER_SOURCE_COMMIT = "1" * 40
PARENT_SHA256 = "a" * 64
PARENT_BYTES = 325_055_632


def load_verifier() -> Any:
    specification = importlib.util.spec_from_file_location(
        "qual_206_claude_composite_observation_verifier",
        VERIFIER_PATH,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load the Claude composite verifier")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


VERIFIER = load_verifier()


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


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


def observer_runtime(marker: str = "accepted") -> dict[str, Any]:
    return {
        "node_version": "v24.0.0",
        "node_executable_bytes": 1,
        "node_executable_sha256": digest(f"node-{marker}"),
        "observer_source_sha256": digest(f"observer-{marker}"),
        "exact_collector_source_sha256": digest(f"collector-{marker}"),
        "fixture_source_sha256": digest(f"fixture-{marker}"),
        "provider_egress_guard_source_sha256": digest(f"guard-{marker}"),
        "command_sha256": digest(f"command-{marker}"),
    }


def start_fields(
    *,
    source_commit: str,
    parent_pid: int,
    runtime: dict[str, Any],
    source_checkout: dict[str, bool] | None = None,
) -> dict[str, Any]:
    return {
        "phase": "session-start",
        "client": "claude-code-2.1.241",
        "source_commit": source_commit,
        "protocol_target": "2026-07-28",
        "transport": "operating-system-stdio-pipes",
        "immediate_parent": {
            "pid": parent_pid,
            "bytes": PARENT_BYTES,
            "sha256": PARENT_SHA256,
        },
        "source_checkout": source_checkout
        or {
            "detached_head": True,
            "head_matches_source_commit": True,
            "local_origin_main_matches_source_commit": True,
            "working_tree_clean": True,
        },
        "observer_runtime": copy.deepcopy(runtime),
        "capture_boundaries": {
            "maximum_event_count": 512,
            "maximum_event_log_bytes": 8_388_608,
            "maximum_frame_bytes": 1_048_576,
            "maximum_idle_milliseconds": 30_000,
            "maximum_session_milliseconds": 120_000,
            "maximum_stderr_bytes": 65_536,
        },
        "credential_environment_observed": False,
        "credential_environment_forwarded": False,
        "child_environment_mode": "closed-credential-free",
        "host_attribution": "immediate-parent-executable-only-unscored",
    }


def audit_fields(kind: str, ordinal: int) -> dict[str, Any]:
    values: dict[str, tuple[int | None, int | None, int | None, int | None, int | None]] = {
        "provider-egress-guard-ready": (None, None, None, None, None),
        "provider-egress-guard-summary": (0, None, None, None, None),
        "session-summary": (None, 0, 0, 0, 0),
    }
    guarded, provider, aborted, ledger, errors = values[kind]
    return {
        "direction": "fixture-audit",
        "frame_bytes": 20 + ordinal,
        "frame_sha256": digest(f"audit-{kind}"),
        "audit_kind": kind,
        "contract_valid": True,
        "ordinal": None,
        "guarded_api_invocation_count": guarded,
        "provider_transport_calls": provider,
        "aborted_provider_calls": aborted,
        "ledger_event_count": ledger,
        "reported_error_count": errors,
    }


def event_core(
    *,
    run_id: str,
    session_id: str,
    slot: str,
    sequence: int,
    event: str,
    previous: str | None,
) -> dict[str, Any]:
    return {
        "schema": "gis-ai-go.qual-206-claude-composite-host-event.v1",
        "run_id": run_id,
        "session_id": session_id,
        "slot": slot,
        "sequence": sequence,
        "observed_at": f"2026-08-25T05:00:{sequence:02d}.000Z",
        "event": event,
        "previous_event_sha256": previous,
    }


def encode_event(core: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    value = copy.deepcopy(core)
    value["event_sha256"] = VERIFIER.domain_separated_sha256(value)
    return value, VERIFIER.canonical_json_bytes(value) + b"\n"


def make_session(
    *,
    slot: str,
    session_id: str,
    profile: str,
    run_id: str = RUN_ID,
    source_commit: str = SOURCE_COMMIT,
    parent_pid: int = 4242,
    runtime: dict[str, Any] | None = None,
    modern_method: str = "tools/list",
    modern_semantic: str = "tools-list-pass",
    response_contract_valid: bool = True,
    anomaly: bool = False,
    request_extra: dict[str, Any] | None = None,
    source_checkout: dict[str, bool] | None = None,
    closure_stimulus: str = "stdin-eof",
    notification_method: str | None = None,
    notification_position: str = "between",
    traffic_after_exit: bool = False,
) -> tuple[bytes, bytes]:
    selected_runtime = runtime or observer_runtime()
    method = "server/discover" if profile == "negotiation-probe" else modern_method
    semantic = "discover-pass" if profile == "negotiation-probe" else modern_semantic
    request_id_sha256 = digest(f"request-{slot}")
    request_frame_bytes = 41
    response_frame_bytes = 51
    notification_frame_bytes = 31
    audit_values = [
        audit_fields("provider-egress-guard-ready", 0),
        audit_fields("provider-egress-guard-summary", 1),
        audit_fields("session-summary", 2),
    ]
    request = {
        "direction": "host-to-fixture",
        "frame_bytes": request_frame_bytes,
        "frame_sha256": digest(f"request-frame-{slot}"),
        "request_ordinal": 0,
        "request_id_sha256": request_id_sha256,
        "request_id_kind": "string",
        "request_id_unique": True,
        "method": method,
        "operation": "not-applicable",
        "protocol_claim": "2026-07-28",
    }
    if request_extra:
        request.update(request_extra)
    specifications: list[tuple[str, dict[str, Any]]] = [
        (
            "lifecycle",
            start_fields(
                source_commit=source_commit,
                parent_pid=parent_pid,
                runtime=selected_runtime,
                source_checkout=source_checkout,
            ),
        ),
        (
            "lifecycle",
            {
                "phase": "child-spawned",
                "fixture_arguments_match_observer_contract": True,
                "spawned_process_identity_verified": False,
            },
        ),
        ("request", request),
    ]
    if notification_method is not None:
        notification_specification = (
            "notification",
            {
                "direction": "host-to-fixture",
                "frame_bytes": notification_frame_bytes,
                "frame_sha256": digest(f"notification-frame-{slot}"),
                "notification_ordinal": 0,
                "method": notification_method,
                "protocol_claim": "2026-07-28",
                "target_request_id_sha256": request_id_sha256,
                "target_request_id_kind": "string",
            },
        )
        if notification_position == "before-request":
            specifications.insert(2, notification_specification)
        else:
            specifications.append(notification_specification)
    specifications.append(
        (
            "response",
            {
                "direction": "fixture-to-host",
                "frame_bytes": response_frame_bytes,
                "frame_sha256": digest(f"response-frame-{slot}"),
                "response_ordinal": 0,
                "request_id_sha256": request_id_sha256,
                "request_id_kind": "string",
                "correlation": "matched",
                "request_method": method,
                "outcome": "success",
                "error_code": None,
                "duration_ms": 1,
                "semantic": semantic,
                "contract_valid": response_contract_valid,
            },
        )
    )
    if notification_method is not None and notification_position == "after-response":
        notification = specifications.pop(-2)
        specifications.append(notification)
    if anomaly:
        specifications.append(
            (
                "anomaly",
                {
                    "classification": "synthetic-anomaly",
                    "direction": "observer",
                    "frame_bytes": 0,
                    "frame_sha256": digest("empty-frame"),
                },
            )
        )
    specifications.extend(("audit", value) for value in audit_values)
    specifications.extend(
        [
            (
                "stream",
                {
                    "stream_name": "host-stdin",
                    "stream_phase": "end",
                    "bytes": request_frame_bytes
                    + (notification_frame_bytes if notification_method is not None else 0),
                    "frames": 1 + (1 if notification_method is not None else 0),
                    "sha256": None,
                    "graceful": True,
                },
            ),
            (
                "stream",
                {
                    "stream_name": "fixture-stdout",
                    "stream_phase": "end",
                    "bytes": response_frame_bytes,
                    "frames": 1,
                    "sha256": None,
                    "graceful": True,
                },
            ),
            (
                "stream",
                {
                    "stream_name": "fixture-audit",
                    "stream_phase": "end",
                    "bytes": sum(value["frame_bytes"] for value in audit_values),
                    "frames": len(audit_values),
                    "sha256": None,
                    "graceful": True,
                },
            ),
            (
                "stream",
                {
                    "stream_name": "fixture-stderr",
                    "stream_phase": "end",
                    "bytes": 0,
                    "frames": 0,
                    "sha256": None,
                    "graceful": True,
                },
            ),
            ("lifecycle", {"phase": "child-exit", "exit_code": 0, "signal": None}),
        ]
    )
    if traffic_after_exit:
        child_exit = specifications.pop()
        specifications.insert(2, child_exit)

    encoded: list[bytes] = []
    previous: str | None = None
    for sequence, (kind, fields) in enumerate(specifications):
        core = event_core(
            run_id=run_id,
            session_id=session_id,
            slot=slot,
            sequence=sequence,
            event=kind,
            previous=previous,
        )
        core.update(fields)
        value, line = encode_event(core)
        encoded.append(line)
        previous = value["event_sha256"]

    prior = b"".join(encoded)
    end_core = event_core(
        run_id=run_id,
        session_id=session_id,
        slot=slot,
        sequence=len(encoded),
        event="lifecycle",
        previous=previous,
    )
    end_core.update(
        {
            "phase": "session-end",
            "session_profile": profile,
            "protocol_session_status": "passed",
            "capability_scored": False,
            "host_capability": False,
            "source_binding_ready": False,
            "runtime_materials_stable": True,
            "source_checkout_stable": True,
            "closure_stimulus": closure_stimulus,
            "exit_code": 0,
            "signal": None,
            "request_count": 1,
            "response_count": 1,
            "notification_count": 1 if notification_method is not None else 0,
            "pending_request_count": 0,
            "stderr_event_count": 0,
            "stderr_bytes": 0,
            "stderr_sha256": None,
            "anomaly_count": 1 if anomaly else 0,
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
        "schema": "gis-ai-go.qual-206-claude-composite-host-event-capture.v1",
        "event_schema": "gis-ai-go.qual-206-claude-composite-host-event.v1",
        "run_id": run_id,
        "client": "claude-code-2.1.241",
        "source_commit": source_commit,
        "session_id": session_id,
        "slot": slot,
        "status": "complete",
        "session_profile": profile,
        "protocol_session_status": "passed",
        "capability_scored": False,
        "host_capability": False,
        "source_binding_ready": False,
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
    final_event = json.loads(log.splitlines()[-1])
    manifest["event_log"] = {
        "bytes": len(log),
        "event_count": len(log.splitlines()),
        "last_event_sha256": final_event["event_sha256"],
        "sha256": hashlib.sha256(log).hexdigest(),
    }
    return VERIFIER.canonical_json_bytes(manifest) + b"\n"


class Qual206ClaudeCompositeObservationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT)
        self.temporary_root = Path(self.temporary.name).resolve()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_root(
        self,
        *,
        first: dict[str, Any] | None = None,
        second: dict[str, Any] | None = None,
    ) -> Path:
        root = self.temporary_root / "capture"
        root.mkdir(mode=0o700)
        root.chmod(0o700)
        parameters = [
            {
                "slot": "session-1",
                "session_id": SESSION_IDS[0],
                "profile": "negotiation-probe",
                **(first or {}),
            },
            {
                "slot": "session-2",
                "session_id": SESSION_IDS[1],
                "profile": "modern-session",
                **(second or {}),
            },
        ]
        for values in parameters:
            directory = root / values["slot"]
            directory.mkdir(mode=0o700)
            directory.chmod(0o700)
            log, manifest = make_session(**values)
            event_path = directory / "events.jsonl"
            manifest_path = directory / "manifest.json"
            event_path.write_bytes(log)
            manifest_path.write_bytes(manifest)
            event_path.chmod(0o600)
            manifest_path.chmod(0o600)
        return root

    def verify(self, root: Path) -> Any:
        return VERIFIER.verify_capture_root(
            root,
            expected_run_id=RUN_ID,
            expected_source_commit=SOURCE_COMMIT,
            expected_parent_sha256=PARENT_SHA256,
            expected_parent_bytes=PARENT_BYTES,
        )

    def test_schemas_are_valid_and_every_data_object_is_closed(self) -> None:
        for path in (EVENT_SCHEMA_PATH, CAPTURE_SCHEMA_PATH):
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            assert_contract_objects_are_closed(self, schema)

    def test_node_observer_suite_is_included_in_python_assurance(self) -> None:
        completed = subprocess.run(
            ["node", "--test", NODE_TEST_PATH],
            cwd=ROOT,
            check=False,
            capture_output=True,
            encoding="utf-8",
            env={**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
            timeout=60,
        )
        diagnostics = f"{completed.stdout}\n{completed.stderr}"[-16_384:]
        self.assertEqual(completed.returncode, 0, diagnostics)

    def test_accepts_exact_two_session_composite_and_cli_is_path_free(self) -> None:
        root = self.write_root()
        before = {
            path.relative_to(root): path.read_bytes()
            for path in root.rglob("*")
            if path.is_file()
        }
        result = self.verify(root)
        self.assertEqual(result.negotiation_request_count, 1)
        self.assertEqual(result.modern_request_count, 1)
        completed = subprocess.run(
            [
                sys.executable,
                str(VERIFIER_PATH),
                "--capture-root",
                str(root),
                "--run-id",
                RUN_ID,
                "--source-commit",
                SOURCE_COMMIT,
                "--expected-parent-sha256",
                PARENT_SHA256,
                "--expected-parent-bytes",
                str(PARENT_BYTES),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            encoding="utf-8",
            timeout=30,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(
            completed.stdout,
            "QUAL-206 Claude composite observation verified "
            "(2 sessions; negotiation-probe requests: 1; modern-session requests: 1).\n",
        )
        for forbidden in (str(root), RUN_ID, SOURCE_COMMIT, PARENT_SHA256):
            self.assertNotIn(forbidden, completed.stdout)
        after = {
            path.relative_to(root): path.read_bytes()
            for path in root.rglob("*")
            if path.is_file()
        }
        self.assertEqual(after, before)

    def test_rejects_duplicate_session_and_role(self) -> None:
        with self.subTest("session"):
            root = self.write_root(second={"session_id": SESSION_IDS[0]})
            with self.assertRaisesRegex(VERIFIER.VerificationError, "distinct session"):
                self.verify(root)
        self.temporary.cleanup()
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT)
        self.temporary_root = Path(self.temporary.name).resolve()
        with self.subTest("role"):
            root = self.write_root(second={"profile": "negotiation-probe"})
            with self.assertRaisesRegex(VERIFIER.VerificationError, "session-1"):
                self.verify(root)

    def test_rejects_run_parent_runtime_and_source_drift(self) -> None:
        cases = {
            "run": {"run_id": OTHER_RUN_ID},
            "parent": {"parent_pid": 4243},
            "runtime": {"runtime": observer_runtime("changed")},
            "source": {"source_commit": OTHER_SOURCE_COMMIT},
        }
        for name, changes in cases.items():
            with self.subTest(name):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    original_root = self.temporary_root
                    self.temporary_root = Path(temporary).resolve()
                    try:
                        root = self.write_root(second=changes)
                        with self.assertRaises(VERIFIER.VerificationError):
                            self.verify(root)
                    finally:
                        self.temporary_root = original_root

    def test_rejects_pagination_semantic_initialize_and_missing_tools_list(self) -> None:
        cases = {
            "pagination": {
                "modern_semantic": "other-success",
                "response_contract_valid": False,
            },
            "initialize": {
                "modern_method": "initialize",
                "modern_semantic": "other-success",
            },
            "missing tools list": {
                "modern_method": "resources/list",
                "modern_semantic": "resources-list-pass",
            },
        }
        for name, changes in cases.items():
            with self.subTest(name):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    original_root = self.temporary_root
                    self.temporary_root = Path(temporary).resolve()
                    try:
                        root = self.write_root(second=changes)
                        with self.assertRaises(VERIFIER.VerificationError):
                            self.verify(root)
                    finally:
                        self.temporary_root = original_root

    def test_rejects_anomaly_and_cross_variant_known_field(self) -> None:
        with self.subTest("anomaly"):
            root = self.write_root(second={"anomaly": True})
            with self.assertRaisesRegex(VERIFIER.VerificationError, "clean, complete"):
                self.verify(root)
        self.temporary.cleanup()
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT)
        self.temporary_root = Path(self.temporary.name).resolve()
        with self.subTest("cross variant"):
            log, _manifest = make_session(
                slot="session-2",
                session_id=SESSION_IDS[1],
                profile="modern-session",
                request_extra={"request_count": 1},
            )
            forged_request = json.loads(log.splitlines()[2])
            with self.assertRaisesRegex(
                VERIFIER.VerificationError,
                "exact closed projection",
            ):
                VERIFIER._require_exact_event_fields(forged_request)
            root = self.write_root(second={"request_extra": {"request_count": 1}})
            with self.assertRaises(VERIFIER.VerificationError):
                self.verify(root)

    def test_rejects_unsafe_permissions_and_unexpected_entries(self) -> None:
        mutations = {
            "root mode": lambda root: root.chmod(0o755),
            "event mode": lambda root: (root / "session-1" / "events.jsonl").chmod(0o640),
            "extra file": lambda root: (root / "session-2" / "extra.txt").write_text("x"),
            "third process": lambda root: (root / "session-3").mkdir(mode=0o700),
        }
        for name, mutate in mutations.items():
            with self.subTest(name):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    original_root = self.temporary_root
                    self.temporary_root = Path(temporary).resolve()
                    try:
                        root = self.write_root()
                        mutate(root)
                        with self.assertRaises(VERIFIER.VerificationError):
                            self.verify(root)
                    finally:
                        self.temporary_root = original_root

    def test_rejects_hash_manifest_and_noncanonical_corruption(self) -> None:
        mutations = ("hash", "manifest", "event canonical", "manifest canonical")
        for name in mutations:
            with self.subTest(name):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    original_root = self.temporary_root
                    self.temporary_root = Path(temporary).resolve()
                    try:
                        root = self.write_root()
                        directory = root / "session-2"
                        event_path = directory / "events.jsonl"
                        manifest_path = directory / "manifest.json"
                        if name == "hash":
                            lines = event_path.read_bytes().splitlines(keepends=True)
                            event = json.loads(lines[2])
                            event["event_sha256"] = "f" * 64
                            lines[2] = VERIFIER.canonical_json_bytes(event) + b"\n"
                            changed = b"".join(lines)
                            event_path.write_bytes(changed)
                            manifest_path.write_bytes(
                                refresh_manifest(changed, manifest_path.read_bytes())
                            )
                        elif name == "manifest":
                            manifest = json.loads(manifest_path.read_bytes())
                            manifest["event_log"]["sha256"] = "f" * 64
                            manifest_path.write_bytes(
                                VERIFIER.canonical_json_bytes(manifest) + b"\n"
                            )
                        elif name == "event canonical":
                            lines = event_path.read_bytes().splitlines(keepends=True)
                            event = json.loads(lines[0])
                            reordered = dict(reversed(list(event.items())))
                            lines[0] = json.dumps(
                                reordered,
                                ensure_ascii=False,
                                separators=(",", ":"),
                            ).encode() + b"\n"
                            changed = b"".join(lines)
                            event_path.write_bytes(changed)
                            manifest_path.write_bytes(
                                refresh_manifest(changed, manifest_path.read_bytes())
                            )
                        else:
                            manifest = json.loads(manifest_path.read_bytes())
                            manifest_path.write_bytes(
                                (json.dumps(manifest, indent=2) + "\n").encode()
                            )
                        event_path.chmod(0o600)
                        manifest_path.chmod(0o600)
                        with self.assertRaises(VERIFIER.VerificationError):
                            self.verify(root)
                    finally:
                        self.temporary_root = original_root

    def test_rejects_duplicate_json_members(self) -> None:
        root = self.write_root()
        manifest_path = root / "session-2" / "manifest.json"
        raw = manifest_path.read_bytes()
        self.assertIn(b'"status":"complete"', raw)
        manifest_path.write_bytes(
            raw.replace(
                b'"status":"complete"',
                b'"status":"complete","status":"complete"',
            )
        )
        manifest_path.chmod(0o600)
        with self.assertRaisesRegex(VERIFIER.VerificationError, "duplicate object member"):
            self.verify(root)

    def test_rejects_non_clean_source_checkout(self) -> None:
        checkout = {
            "detached_head": False,
            "head_matches_source_commit": True,
            "local_origin_main_matches_source_commit": True,
            "working_tree_clean": True,
        }
        root = self.write_root(second={"source_checkout": checkout})
        with self.assertRaisesRegex(VERIFIER.VerificationError, "clean detached"):
            self.verify(root)

    def test_accepts_safe_sigterm_close_and_rejects_missing_close_stimulus(self) -> None:
        root = self.write_root(second={"closure_stimulus": "sigterm"})
        self.verify(root)
        self.temporary.cleanup()
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT)
        self.temporary_root = Path(self.temporary.name).resolve()
        root = self.write_root(second={"closure_stimulus": "none"})
        with self.assertRaisesRegex(VERIFIER.VerificationError, "clean, complete"):
            self.verify(root)

    def test_accepts_safe_sigint_close(self) -> None:
        root = self.write_root(second={"closure_stimulus": "sigint"})
        self.verify(root)

    def test_accepts_safe_stdin_eof_and_sigint_close(self) -> None:
        root = self.write_root(second={"closure_stimulus": "stdin-eof-and-sigint"})
        self.verify(root)

    def test_rejects_legacy_notification_and_host_traffic_after_child_exit(self) -> None:
        cases = {
            "legacy notification": {
                "notification_method": "notifications/initialized",
            },
            "cancellation before request": {
                "notification_method": "notifications/cancelled",
                "notification_position": "before-request",
            },
            "cancellation after response": {
                "notification_method": "notifications/cancelled",
                "notification_position": "after-response",
            },
            "traffic after exit": {"traffic_after_exit": True},
        }
        for name, changes in cases.items():
            with self.subTest(name):
                with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
                    original_root = self.temporary_root
                    self.temporary_root = Path(temporary).resolve()
                    try:
                        root = self.write_root(second=changes)
                        with self.assertRaises(VERIFIER.VerificationError):
                            self.verify(root)
                    finally:
                        self.temporary_root = original_root

    def test_rejects_operation_mismatch_and_swapped_composite_chronology(self) -> None:
        with self.subTest("operation"):
            root = self.write_root(
                second={"request_extra": {"operation": "data.query"}}
            )
            with self.assertRaisesRegex(VERIFIER.VerificationError, "operation"):
                self.verify(root)
        self.temporary.cleanup()
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT)
        self.temporary_root = Path(self.temporary.name).resolve()
        with self.subTest("chronology"):
            root = self.write_root(
                first={"profile": "modern-session"},
                second={"profile": "negotiation-probe"},
            )
            with self.assertRaisesRegex(VERIFIER.VerificationError, "session-1"):
                self.verify(root)

    def test_number_canonicalisation_matches_ecmascript_boundaries(self) -> None:
        self.assertEqual(VERIFIER.canonical_json(1e-6), "0.000001")
        self.assertEqual(VERIFIER.canonical_json(1e-7), "1e-7")
        self.assertEqual(VERIFIER.canonical_json(1e20), "100000000000000000000")
        self.assertEqual(VERIFIER.canonical_json(1e21), "1e+21")
        self.assertEqual(VERIFIER.canonical_json(-0.0), "0")


if __name__ == "__main__":
    unittest.main()
