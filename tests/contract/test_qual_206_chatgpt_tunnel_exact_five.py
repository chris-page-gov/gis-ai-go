from __future__ import annotations

import argparse
import copy
from datetime import datetime, timedelta, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import select
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Callable
import unittest
from unittest import mock

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import finalise_qual_206_chatgpt_tunnel_exact_five as finaliser  # noqa: E402
import verify_qual_206_chatgpt_tunnel_exact_five as verifier  # noqa: E402


SCHEMAS = (
    verifier.STATUS_SCHEMA,
    verifier.EVENT_SCHEMA,
    verifier.CAPTURE_SCHEMA,
    verifier.SESSION_SCHEMA,
    verifier.PRIVATE_SCHEMA,
    verifier.PUBLIC_SCHEMA,
)
RUN_ID = "12345678-1234-4234-8234-123456789abc"
FRESH_APP_VERSION = "asdk_app_v_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
HISTORICAL_APP_VERSION = "asdk_app_v_6a873f85363081918f25a5aeaee98159"
TUNNEL_ID = "tunnel_6a873e7214308191bfe27240c1c03f68"
TUNNEL_NAME = "gis-ai-go-v0-2-interoperability"
PROFILE_NAME = "gis-ai-go-v0-2-exact-five-v1"
REMOTE_IDENTITY = {"found": True, "id": TUNNEL_ID, "name": TUNNEL_NAME}
PORTABLE_FIXTURE = (
    ROOT
    / "tests"
    / "contract"
    / "fixtures"
    / "qual-206-chatgpt-tunnel-portable-fixture.v1.json"
)


def validator(
    path: Path,
    mutation: Callable[[dict[str, Any]], None] | None = None,
) -> Draft202012Validator:
    schema = json.loads(path.read_text(encoding="utf-8"))
    if mutation is not None:
        mutation(schema)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


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


def write_private_json(path: Path, value: dict[str, Any]) -> bytes:
    raw = verifier.canonical_line(value)
    path.write_bytes(raw)
    os.chmod(path, 0o600)
    return raw


def file_facts(name: str, raw: bytes) -> dict[str, Any]:
    return {
        "name": name,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "mode": "0600",
    }


def material_facts(name: str, raw: bytes) -> dict[str, Any]:
    return {"name": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def iso_milliseconds(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


class ChatGptTunnelPortableContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(PORTABLE_FIXTURE.read_text(encoding="utf-8"))
        cls.profile = json.loads(verifier.PROFILE.read_text(encoding="utf-8"))

    def test_synthetic_fixture_exercises_all_six_canonical_schemas(self) -> None:
        self.assertEqual(
            set(self.fixture),
            {
                "schema",
                "synthetic",
                "statuses",
                "events",
                "session_captures",
                "sessions",
                "private_run",
                "public_evidence",
            },
        )
        self.assertEqual(
            self.fixture["schema"],
            "gis-ai-go.qual-206-chatgpt-tunnel-portable-fixture.v1",
        )
        self.assertIs(self.fixture["synthetic"], True)
        self.assertEqual(
            tuple(
                len(self.fixture[key])
                for key in ("statuses", "events", "session_captures", "sessions")
            ),
            (3, 37, 2, 2),
        )
        records = (
            (verifier.STATUS_SCHEMA, self.fixture["statuses"]),
            (verifier.EVENT_SCHEMA, self.fixture["events"]),
            (verifier.CAPTURE_SCHEMA, self.fixture["session_captures"]),
            (verifier.SESSION_SCHEMA, self.fixture["sessions"]),
            (verifier.PRIVATE_SCHEMA, [self.fixture["private_run"]]),
            (verifier.PUBLIC_SCHEMA, [self.fixture["public_evidence"]]),
        )
        for schema_path, instances in records:
            with self.subTest(schema=schema_path.name):
                contract = validator(schema_path)
                assert_contract_objects_are_closed(
                    self,
                    json.loads(schema_path.read_text(encoding="utf-8")),
                )
                for instance in instances:
                    self.assertEqual(list(contract.iter_errors(instance)), [])

    def test_fixture_event_chains_and_embedded_hashes_are_self_consistent(self) -> None:
        for session in self.fixture["sessions"]:
            events = [
                event
                for event in self.fixture["events"]
                if event["session_id"] == session["session_id"]
            ]
            previous: str | None = None
            encoded: list[bytes] = []
            for index, event in enumerate(events):
                self.assertEqual(event["sequence"], index)
                self.assertEqual(event["previous_event_sha256"], previous)
                core = dict(event)
                supplied = core.pop("event_sha256")
                self.assertEqual(supplied, verifier.event_digest(core))
                if event.get("phase") == "session-end":
                    prior_raw = b"".join(encoded)
                    self.assertEqual(event["prior_event_count"], index)
                    self.assertEqual(event["prior_event_log_bytes"], len(prior_raw))
                    self.assertEqual(
                        event["prior_event_log_sha256"],
                        hashlib.sha256(prior_raw).hexdigest(),
                    )
                previous = supplied
                encoded.append(verifier.canonical_line(event))
            event_raw = b"".join(encoded)
            capture = next(
                item
                for item in self.fixture["session_captures"]
                if item["session_id"] == session["session_id"]
            )
            self.assertEqual(
                capture["event_log"],
                {
                    "bytes": len(event_raw),
                    "event_count": len(events),
                    "last_event_sha256": events[-1]["event_sha256"],
                    "sha256": hashlib.sha256(event_raw).hexdigest(),
                },
            )

        private_raw = verifier.canonical_line(self.fixture["private_run"])
        self.assertEqual(
            self.fixture["public_evidence"]["private_capture"][
                "run_manifest_sha256"
            ],
            hashlib.sha256(private_raw).hexdigest(),
        )

    def test_request_ids_may_be_reused_only_after_the_response(self) -> None:
        digest = "a" * 64
        serial = [
            {"event": "request", "request_id_sha256": digest},
            {"event": "response", "request_id_sha256": digest},
            {"event": "request", "request_id_sha256": digest},
            {"event": "response", "request_id_sha256": digest},
        ]
        self.assertEqual(
            len(verifier.correlate_request_response_events(serial, "session-1")),
            2,
        )
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "in-flight request identity",
        ):
            verifier.correlate_request_response_events(
                [serial[0], serial[2]], "session-1"
            )
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "orphan or duplicate response",
        ):
            verifier.correlate_request_response_events(
                [serial[0], serial[1], serial[3]], "session-1"
            )

    def test_teardown_event_contract_distinguishes_the_two_truthful_orders(self) -> None:
        event_validator = validator(verifier.EVENT_SCHEMA)
        session = self.fixture["sessions"][0]
        common = {
            "schema": "gis-ai-go.qual-206-chatgpt-tunnel-exact-five-event.v1",
            "run_id": self.fixture["private_run"]["run_id"],
            "session_id": session["session_id"],
            "slot": session["slot"],
            "sequence": 2,
            "observed_at": self.fixture["private_run"]["execution"]["started_at"],
            "event": "lifecycle",
            "previous_event_sha256": "a" * 64,
            "event_sha256": "b" * 64,
            "phase": "parent-teardown-signal",
            "signal": "SIGTERM",
            "immediate_parent_verified": True,
        }
        eof_before_signal = {
            **common,
            "stdin_closed_before_signal": True,
            "stdin_eof_observed_within_grace": False,
        }
        signal_before_eof = {
            **common,
            "stdin_closed_before_signal": False,
            "stdin_eof_observed_within_grace": True,
        }
        for label, event in (
            ("EOF before SIGTERM", eof_before_signal),
            ("SIGTERM before EOF", signal_before_eof),
        ):
            with self.subTest(order=label):
                self.assertEqual(list(event_validator.iter_errors(event)), [])

        for label, pair in (
            ("both true", (True, True)),
            ("both false", (False, False)),
        ):
            changed = {
                **common,
                "stdin_closed_before_signal": pair[0],
                "stdin_eof_observed_within_grace": pair[1],
            }
            with self.subTest(order=label):
                self.assertTrue(list(event_validator.iter_errors(changed)))

        missing_grace_fact = dict(eof_before_signal)
        del missing_grace_fact["stdin_eof_observed_within_grace"]
        self.assertTrue(list(event_validator.iter_errors(missing_grace_fact)))

        session_end = next(
            event
            for event in self.fixture["events"]
            if event["session_id"] == session["session_id"]
            and event.get("phase") == "session-end"
        )
        signal_first_end = {**session_end, "closure_stimulus": "sigterm-then-stdin-eof"}
        self.assertEqual(list(event_validator.iter_errors(signal_first_end)), [])

    def test_developer_version_id_is_not_used_as_tool_surface_evidence(self) -> None:
        for schema_path, source in (
            (verifier.PRIVATE_SCHEMA, self.fixture["private_run"]),
            (verifier.PUBLIC_SCHEMA, self.fixture["public_evidence"]),
        ):
            observed = copy.deepcopy(source)
            observed["host"]["app_version_id"] = HISTORICAL_APP_VERSION
            with self.subTest(schema=schema_path.name):
                self.assertEqual(list(validator(schema_path).iter_errors(observed)), [])

    def test_request_arguments_bind_events_summaries_and_frozen_profile(self) -> None:
        session = self.fixture["sessions"][1]
        requests = [
            event
            for event in self.fixture["events"]
            if event["session_id"] == session["session_id"]
            and event["event"] == "request"
            and event["method"] == "tools/call"
        ]
        profile_arguments = [
            operation["arguments"] for operation in self.profile["operations"][:4]
        ]
        receipt_id = session["operations"][0]["response"]["receipt_id"]
        verifier.verify_request_argument_bindings(
            requests,
            session["operations"],
            profile_arguments,
            receipt_id,
        )

        changed_requests = copy.deepcopy(requests)
        changed_operations = copy.deepcopy(session["operations"])
        changed_arguments = verifier.canonical_bytes({"query": "OTHER", "limit": 1})
        changed_bytes = len(changed_arguments)
        changed_sha256 = hashlib.sha256(changed_arguments).hexdigest()
        changed_requests[0]["arguments_bytes"] = changed_bytes
        changed_requests[0]["arguments_sha256"] = changed_sha256
        changed_operations[0]["request"]["parameters_bytes"] = changed_bytes
        changed_operations[0]["request"]["parameters_sha256"] = changed_sha256
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "request arguments do not match the frozen profile",
        ):
            verifier.verify_request_argument_bindings(
                changed_requests,
                changed_operations,
                profile_arguments,
                receipt_id,
            )

    def test_event_times_are_monotonic_inside_the_operator_window(self) -> None:
        execution = self.fixture["private_run"]["execution"]
        started = verifier.parse_time(execution["started_at"])
        finished = verifier.parse_time(execution["finished_at"])
        sessions: list[list[dict[str, Any]]] = []
        for session in self.fixture["sessions"]:
            events = [
                event
                for event in self.fixture["events"]
                if event["session_id"] == session["session_id"]
            ]
            sessions.append(events)
            verifier.verify_event_observation_window(
                events,
                started=started,
                finished=finished,
            )

        lifecycle_outside = copy.deepcopy(sessions[1])
        lifecycle_outside[0]["observed_at"] = iso_milliseconds(
            started - timedelta(seconds=1)
        )
        verifier.verify_event_observation_window(
            lifecycle_outside,
            started=started,
            finished=finished,
        )
        outside = copy.deepcopy(sessions[1])
        last_protocol = max(
            verifier.parse_time(event["observed_at"])
            for event in outside
            if event["event"] in {"request", "response", "notification"}
        )
        non_monotonic = copy.deepcopy(sessions[1])
        non_monotonic[1]["observed_at"] = iso_milliseconds(
            verifier.parse_time(non_monotonic[0]["observed_at"])
            - timedelta(milliseconds=1)
        )
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "protocol events are outside the declared observation window",
        ):
            verifier.verify_event_observation_window(
                outside,
                started=started,
                finished=last_protocol - timedelta(milliseconds=1),
            )
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "session events are not monotonic",
        ):
            verifier.verify_event_observation_window(
                non_monotonic,
                started=started,
                finished=finished,
            )

    def test_cli_requires_explicit_node_and_pnpm_paths(self) -> None:
        verifier_arguments = [
            "--private-root",
            "/tmp/private",
            "--output",
            "/tmp/public.json",
        ]
        finaliser_arguments = [
            "--private-root",
            "/tmp/private",
            "--started-at",
            "2026-08-28T00:00:00.000Z",
            "--finished-at",
            "2026-08-28T00:01:00.000Z",
            "--displayed-model",
            "GPT-5",
            "--app-version-id",
            FRESH_APP_VERSION,
            "--conversation-id-sha256",
            "b" * 64,
        ]
        for parser, arguments in (
            (verifier.parse_arguments, verifier_arguments),
            (finaliser.parse_arguments, finaliser_arguments),
        ):
            for added in ([], ["--node", "/explicit/node"]):
                with self.subTest(parser=parser.__module__, added=added):
                    with self.assertRaises(SystemExit), mock.patch(
                        "sys.stderr", new_callable=io.StringIO
                    ):
                        parser(arguments + added)
            parsed = parser(
                arguments
                + ["--node", "/explicit/node", "--pnpm", "/explicit/pnpm"]
            )
            self.assertEqual(parsed.node, Path("/explicit/node"))
            self.assertEqual(parsed.pnpm, Path("/explicit/pnpm"))

    def test_runtime_paths_reject_relative_missing_and_symlink_inputs(self) -> None:
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "Node path must be an existing canonical absolute path",
        ):
            verifier.locate_verified_node(Path("node"))
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "pnpm path must be an existing canonical absolute path",
        ):
            verifier.require_explicit_pnpm_path(Path("pnpm"))
        with tempfile.TemporaryDirectory(prefix="qual206-runtime-paths-") as directory:
            root = Path(directory).resolve()
            missing = root / "missing"
            target = root / "target"
            target.write_bytes(b"synthetic executable")
            alias = root / "alias"
            alias.symlink_to(target)
            for path in (missing, alias):
                with self.subTest(path=path):
                    with self.assertRaises(verifier.TunnelExactFiveVerificationError):
                        verifier.locate_verified_node(path)
                    with self.assertRaises(verifier.TunnelExactFiveVerificationError):
                        verifier.require_explicit_pnpm_path(path)


class ChatGptTunnelExactFiveContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if sys.platform != "darwin":
            raise unittest.SkipTest("the closed observer requires the reviewed macOS sandbox")
        cls.temporary = Path(
            tempfile.mkdtemp(prefix="gis-ai-go-chatgpt-tunnel-verifier-test-")
        ).resolve()
        os.chmod(cls.temporary, 0o700)
        cls.capture = cls.temporary / "accepted"
        cls.capture.mkdir(mode=0o700)
        node = shutil.which("node")
        if node is None:
            raise unittest.SkipTest("the reviewed Node runtime is unavailable")
        cls.node = verifier.locate_verified_node(Path(os.path.realpath(node)))
        cls.parent_executable = Path(os.path.realpath(sys.executable))
        parent_raw = cls.parent_executable.read_bytes()
        cls.parent_identity = {
            "bytes": len(parent_raw),
            "sha256": hashlib.sha256(parent_raw).hexdigest(),
        }
        generated = verifier._host_call(verifier.host002.measure_generated_runtime_closure)
        cls.runtime = {
            "generated_first_party_closure": {
                **generated,
                "reference_manifest_sha256": generated["manifest_sha256"],
                "reference_matches_current": True,
            },
            "installed_dependency_closure": verifier._host_call(
                verifier.host002.measure_installed_dependency_closure
            ),
        }
        cls.commit = verifier._host_call(verifier.host002.git_output, "rev-parse", "HEAD")
        cls.tree = verifier._host_call(
            verifier.host002.git_output, "rev-parse", f"{cls.commit}^{{tree}}"
        )
        cls.profile = json.loads(verifier.PROFILE.read_text(encoding="utf-8"))
        cls._create_observer_capture()
        cls.fixture_command_sha256 = cls._session_start("session-1")["observer_runtime"][
            "command_sha256"
        ]
        if (
            cls._session_start("session-2")["observer_runtime"]["command_sha256"]
            != cls.fixture_command_sha256
        ):
            raise AssertionError("the fake sessions did not retain one fixture command")
        cls.outer_mcp_command_sha256 = hashlib.sha256(
            b"synthetic outer tunnel MCP command"
        ).hexdigest()
        if cls.outer_mcp_command_sha256 == cls.fixture_command_sha256:
            raise AssertionError("the fake inner and outer command digests are not distinct")
        cls._create_statuses_and_manifest()
        cls.private_validator = validator(
            verifier.PRIVATE_SCHEMA,
            lambda schema: schema["properties"]["tunnel_client"]["properties"].update(
                {
                    "binary_bytes": {"const": cls.parent_identity["bytes"]},
                    "binary_sha256": {"const": cls.parent_identity["sha256"]},
                }
            ),
        )
        cls.public_validator = validator(
            verifier.PUBLIC_SCHEMA,
            lambda schema: schema["properties"]["tunnel"]["properties"].update(
                {"client_binary_sha256": {"const": cls.parent_identity["sha256"]}}
            ),
        )
        cls.event_validator = validator(
            verifier.EVENT_SCHEMA,
            lambda schema: schema["$defs"]["immediateParent"]["properties"].update(
                {
                    "bytes": {"const": cls.parent_identity["bytes"]},
                    "sha256": {"const": cls.parent_identity["sha256"]},
                }
            ),
        )

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.temporary)

    @classmethod
    def _closed_environment(cls) -> dict[str, str]:
        environment = dict(os.environ)
        for name in verifier.host002.RECOGNISED_CREDENTIAL_VARIABLES:
            environment.pop(name, None)
        environment.update(
            {
                "GIS_AI_GO_QUAL_206_CHATGPT_TUNNEL_EXACT_FIVE": "1",
                "GIS_AI_GO_QUAL_206_EVENT_CAPTURE": "1",
                "GIS_AI_GO_QUAL_206_MCP_NETWORK_SANDBOX": verifier.NETWORK_SANDBOX,
                "GIS_AI_GO_QUAL_206_HOST_ATTESTATION": (
                    "outer-harness-bound-tunnel-client"
                ),
            }
        )
        return environment

    @classmethod
    def _observer_arguments(cls) -> list[str]:
        generated = cls.runtime["generated_first_party_closure"]
        installed = cls.runtime["installed_dependency_closure"]
        return [
            cls.node,
            str(verifier.OBSERVER),
            "--chatgpt-tunnel-exact-five-observation-only",
            "--capture-root",
            str(cls.capture),
            "--run-id",
            RUN_ID,
            "--client",
            "fake-chatgpt-tunnel-host",
            "--source-commit",
            cls.commit,
            "--expected-parent-sha256",
            cls.parent_identity["sha256"],
            "--expected-parent-bytes",
            str(cls.parent_identity["bytes"]),
            "--expected-generated-runtime-bytes",
            str(generated["bytes"]),
            "--expected-generated-runtime-file-count",
            str(generated["file_count"]),
            "--expected-generated-runtime-manifest-sha256",
            generated["manifest_sha256"],
            "--expected-generated-runtime-reference-manifest-sha256",
            generated["reference_manifest_sha256"],
            "--expected-generated-runtime-reference-matches-current",
            "true",
            "--expected-installed-dependency-bytes",
            str(installed["bytes"]),
            "--expected-installed-dependency-entry-count",
            str(installed["entry_count"]),
            "--expected-installed-dependency-manifest-sha256",
            installed["manifest_sha256"],
        ]

    @classmethod
    def _start_observer(cls) -> subprocess.Popen[str]:
        return subprocess.Popen(
            cls._observer_arguments(),
            cwd=ROOT,
            env=cls._closed_environment(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    @classmethod
    def _request(
        cls,
        process: subprocess.Popen[str],
        request_id: str | int,
        method: str,
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if process.stdin is None or process.stdout is None:
            raise AssertionError("observer pipes are unavailable")
        meta = {
            "io.modelcontextprotocol/protocolVersion": verifier.PROTOCOL,
            "io.modelcontextprotocol/clientCapabilities": {},
            "io.modelcontextprotocol/clientInfo": {
                "name": "qual-206-fake-chatgpt-tunnel",
                "version": "1.0.0",
            },
        }
        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": {**(parameters or {}), "_meta": meta},
        }
        process.stdin.write(json.dumps(request, separators=(",", ":")) + "\n")
        process.stdin.flush()
        ready, _, _ = select.select([process.stdout], [], [], 30)
        if not ready:
            process.kill()
            raise AssertionError(f"observer timed out before the {method} response")
        response = json.loads(process.stdout.readline())
        if response.get("id") != request_id or "error" in response:
            raise AssertionError(f"observer rejected {method}: {response}")
        return response["result"]

    @classmethod
    def _finish(cls, process: subprocess.Popen[str]) -> None:
        if process.stdin is None or process.stdout is None or process.stderr is None:
            raise AssertionError("observer pipes are unavailable")
        process.stdin.close()
        try:
            return_code = process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
            raise AssertionError("observer did not close after STDIN EOF")
        stderr = process.stderr.read()
        process.stdout.close()
        process.stderr.close()
        if return_code != 0 or stderr:
            raise AssertionError(
                f"observer failed with code {return_code}: {stderr.rstrip()}"
            )

    @classmethod
    def _create_observer_capture(cls) -> None:
        discovery = cls._start_observer()
        result = cls._request(discovery, "discover-1", "server/discover")
        if result.get("supportedVersions") != [verifier.PROTOCOL]:
            raise AssertionError("the fake discovery response changed")
        cls._finish(discovery)

        exact_five = cls._start_observer()
        listing = cls._request(exact_five, 0, "tools/list")
        if sorted(tool["name"] for tool in listing["tools"]) != sorted(
            verifier.OPERATIONS
        ):
            raise AssertionError("the fake canonical tool listing changed")
        search_receipt: str | None = None
        for operation in cls.profile["operations"]:
            arguments = (
                {"receipt_id": search_receipt}
                if operation["name"] == "evidence.inspect"
                else operation["arguments"]
            )
            result = cls._request(
                exact_five,
                0,
                "tools/call",
                {"name": operation["name"], "arguments": arguments},
            )
            if operation["name"] == "catalogue.search":
                search_receipt = result["structuredContent"]["evidence_receipt"][
                    "receipt_id"
                ]
        if search_receipt is None:
            raise AssertionError("the fake exact-five session did not return a receipt")
        cls._finish(exact_five)

    @classmethod
    def _session_start(cls, slot: str) -> dict[str, Any]:
        line = (cls.capture / slot / "events.jsonl").read_text(encoding="utf-8").splitlines()[
            0
        ]
        return json.loads(line)

    @classmethod
    def _status(cls, phase: str, observed_at: str) -> dict[str, Any]:
        stopped = phase == "stopped"
        return {
            "schema": "gis-ai-go.qual-206-chatgpt-tunnel-status.v1",
            "phase": phase,
            "observed_at": observed_at,
            "alias": PROFILE_NAME,
            "profile_name": PROFILE_NAME,
            "target_kind": "command",
            "mcp_command_sha256": cls.outer_mcp_command_sha256,
            "tunnel_id": TUNNEL_ID,
            "remote": {**REMOTE_IDENTITY, "found": not stopped},
            "stale": False,
            "error": None,
            "remote_error": None,
            "runtime_state": "stopped" if stopped else "ready",
            "healthy": not stopped,
            "ready": not stopped,
            "control_plane_poll_health": (
                None if stopped else {"state": "direct", "route_kind": "control_plane"}
            ),
            "remote_lookup_attempted": not stopped,
            "process_running": not stopped,
            "local": {
                "healthz_status": None if stopped else 200,
                "readyz_status": None if stopped else 200,
                "direct_healthy_poll_route": not stopped,
            },
        }

    @classmethod
    def _create_statuses_and_manifest(cls) -> None:
        events = [
            json.loads(line)
            for slot in ("session-1", "session-2")
            for line in (cls.capture / slot / "events.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        protocol_times = [
            datetime.fromisoformat(event["observed_at"].replace("Z", "+00:00"))
            for event in events
            if event["event"] in {"request", "response", "notification"}
        ]
        first = min(protocol_times)
        last = max(protocol_times)
        final_lifecycle = max(
            datetime.fromisoformat(event["observed_at"].replace("Z", "+00:00"))
            for event in events
        )
        before_raw = write_private_json(
            cls.capture / verifier.STATUS_BEFORE_NAME,
            cls._status("before", iso_milliseconds(first - timedelta(milliseconds=1))),
        )
        after_raw = write_private_json(
            cls.capture / verifier.STATUS_AFTER_NAME,
            cls._status("after", iso_milliseconds(last + timedelta(milliseconds=1))),
        )
        stopped_raw = write_private_json(
            cls.capture / verifier.STATUS_STOPPED_NAME,
            cls._status(
                "stopped",
                iso_milliseconds(final_lifecycle + timedelta(milliseconds=1)),
            ),
        )
        claim_raw = (cls.capture / verifier.CLAIM_NAME).read_bytes()
        claim = json.loads(claim_raw)
        manifest = {
            "schema": "gis-ai-go.qual-206-chatgpt-tunnel-exact-five-private-run.v1",
            "run_id": claim["run_id"],
            "scenario": verifier.SCENARIO,
            "source": {
                "commit": cls.commit,
                "tree": cls.tree,
                "repository_origin": verifier.host002.CANONICAL_REPOSITORY_ORIGIN,
                "local_origin_main_match": True,
                "clean_detached_checkout": True,
                "protected_main_verification": "external-publication-gate",
            },
            "runtime": cls.runtime,
            "tunnel_client": {
                "version": "0.0.13",
                "build_sha": "4b5267f823be0b046bb883aacb51603cfde3a0ea",
                "reported_version": verifier.TUNNEL_CLIENT_VERSION,
                "binary_bytes": cls.parent_identity["bytes"],
                "binary_sha256": cls.parent_identity["sha256"],
                "archive_sha256": (
                    "15abf165f06050af642c948ba6bd6c905191dc5420a9422dadde2b49d892e2c6"
                ),
                "sha256sums_sha256": (
                    "e6495395e8f5d952b0edc34a0b552426e38472973a7602f94b3868fbcd9aceb4"
                ),
                "release_url": (
                    "https://github.com/openai/tunnel-client/releases/tag/v0.0.13"
                ),
                "release_verified": True,
            },
            "tunnel": {
                "local_alias": PROFILE_NAME,
                "remote_name": TUNNEL_NAME,
                "remote_id": TUNNEL_ID,
                "connection_kind": "openai-secure-tunnel",
                "authenticated": True,
                "local_mcp_child_transport": "stdio",
                "direct_public_streamable_http_tls": False,
            },
            "host": {
                "name": "ChatGPT",
                "app_name": "GIS AI GO v0.2 interoperability",
                "app_id": "asdk_app_6a873f853628819184bccb4a9b961576",
                "app_version_id": FRESH_APP_VERSION,
                "displayed_model": "GPT-5",
                "displayed_model_operator_observed": True,
                "conversation_id_sha256": "b" * 64,
            },
            "execution": {
                "started_at": iso_milliseconds(first),
                "finished_at": iso_milliseconds(last),
                "exit_code": None,
                "signal": None,
                "classification": "complete",
                "session_count": 2,
            },
            "private_files": {
                "claim": file_facts(verifier.CLAIM_NAME, claim_raw),
                "status_before": file_facts(verifier.STATUS_BEFORE_NAME, before_raw),
                "status_after": file_facts(verifier.STATUS_AFTER_NAME, after_raw),
                "status_stopped": file_facts(verifier.STATUS_STOPPED_NAME, stopped_raw),
            },
            "isolation": {
                "private_root_mode": "0700",
                "private_file_mode": "0600",
                "observer_credentials_observed": False,
                "mcp_child_recognised_credentials_forwarded": False,
                "mcp_child_network_access_allowed": False,
                "mcp_child_network_sandbox": verifier.NETWORK_SANDBOX,
                "provider_egress_guard_ready": True,
                "guarded_live_provider_api_invocations": 0,
                "raw_material_published": False,
            },
            "claims": dict(verifier.EXPECTED_CLAIMS),
        }
        write_private_json(cls.capture / "run-manifest.json", manifest)

    def setUp(self) -> None:
        self.case_root = Path(
            tempfile.mkdtemp(prefix="gis-ai-go-chatgpt-tunnel-verifier-case-")
        ).resolve()
        self.addCleanup(shutil.rmtree, self.case_root)
        self.case = self.case_root / "capture"
        shutil.copytree(self.capture, self.case)
        os.chmod(self.case, 0o700)

    def verify(self, root: Path | None = None) -> dict[str, Any]:
        return verifier.verify_and_project(
            root or self.case,
            node_path=Path(self.node),
            pnpm_path=Path(self.node),
            source_verifier=lambda _manifest: None,
            private_validator=self.private_validator,
            public_validator=self.public_validator,
            event_validator=self.event_validator,
            runtime_reproducer=lambda _commit, _node, _pnpm: copy.deepcopy(self.runtime),
        )

    def test_node_and_pnpm_paths_must_be_explicit_canonical_and_absolute(self) -> None:
        self.assertEqual(
            verifier.locate_verified_node(Path(self.node)),
            self.node,
        )
        self.assertEqual(
            verifier.require_explicit_pnpm_path(Path(self.node)),
            self.node,
        )
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "canonical absolute path",
        ):
            verifier.locate_verified_node(Path("node"))
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "canonical absolute path",
        ):
            verifier.require_explicit_pnpm_path(Path("pnpm"))
        alias = self.case_root / "pnpm-alias"
        alias.symlink_to(self.node)
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "canonical absolute path",
        ):
            verifier.require_explicit_pnpm_path(alias)
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "canonical absolute path",
        ):
            verifier.locate_verified_node(alias)
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "canonical absolute path",
        ):
            verifier.require_explicit_pnpm_path(self.case_root / "missing-pnpm")
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "canonical absolute path",
        ):
            verifier.locate_verified_node(self.case_root / "missing-node")

    def test_reference_reproducer_uses_only_the_explicit_pnpm_path(self) -> None:
        generated = self.runtime["generated_first_party_closure"]
        current_generated = {
            "bytes": generated["bytes"],
            "file_count": generated["file_count"],
            "manifest_sha256": generated["manifest_sha256"],
        }
        completed = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=verifier.canonical_line(self.runtime),
            stderr=b"",
        )
        poisoned = self.case_root / "poisoned-path"
        poisoned.mkdir(mode=0o700)
        fake_pnpm = poisoned / "pnpm"
        fake_pnpm.write_text("must not be selected\n", encoding="utf-8")
        fake_pnpm.chmod(0o700)

        def host_call(function: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
            if function is verifier.host002.measure_generated_runtime_closure:
                return current_generated
            if function is verifier.host002.measure_installed_dependency_closure:
                return self.runtime["installed_dependency_closure"]
            return function(*args, **kwargs)

        with (
            mock.patch.object(
                verifier,
                "_host_call",
                side_effect=host_call,
            ),
            mock.patch.object(
                verifier.subprocess,
                "run",
                return_value=completed,
            ) as run,
            mock.patch.dict(os.environ, {"PATH": str(poisoned)}),
        ):
            reproduced = verifier.independently_reproduce_runtime_closure(
                "a" * 40,
                node_path=self.node,
                pnpm_path=Path(self.node),
            )
        self.assertEqual(reproduced, self.runtime)
        command = run.call_args.args[0]
        environment = run.call_args.kwargs["env"]
        self.assertEqual(command[-1], self.node)
        self.assertEqual(
            environment["PATH"],
            os.pathsep.join((str(Path(self.node).parent), "/usr/bin", "/bin")),
        )
        self.assertNotIn(str(poisoned), environment["PATH"])

    def test_finaliser_and_verifier_cli_require_node_and_pnpm(self) -> None:
        with mock.patch("sys.stderr", new=io.StringIO()):
            with self.assertRaises(SystemExit):
                verifier.parse_arguments([
                    "--private-root", str(self.case),
                    "--pnpm", self.node,
                    "--output", str(self.case_root / "output.json"),
                ])
            with self.assertRaises(SystemExit):
                verifier.parse_arguments([
                    "--private-root", str(self.case),
                    "--node", self.node,
                    "--output", str(self.case_root / "output.json"),
                ])
            with self.assertRaises(SystemExit):
                finaliser.parse_arguments([
                    "--private-root", str(self.case),
                    "--pnpm", self.node,
                    "--started-at", "2026-08-27T12:00:00.000Z",
                    "--finished-at", "2026-08-27T12:01:00.000Z",
                    "--displayed-model", "GPT-5",
                    "--app-version-id", FRESH_APP_VERSION,
                    "--conversation-id-sha256", "b" * 64,
                ])
            with self.assertRaises(SystemExit):
                finaliser.parse_arguments([
                    "--private-root", str(self.case),
                    "--node", self.node,
                    "--started-at", "2026-08-27T12:00:00.000Z",
                    "--finished-at", "2026-08-27T12:01:00.000Z",
                    "--displayed-model", "GPT-5",
                    "--app-version-id", FRESH_APP_VERSION,
                    "--conversation-id-sha256", "b" * 64,
                ])

    def rebind_root_file(self, name: str, value: dict[str, Any], fact: str) -> None:
        raw = write_private_json(self.case / name, value)
        manifest_path = self.case / "run-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["private_files"][fact] = file_facts(name, raw)
        write_private_json(manifest_path, manifest)

    def rebind_session_events(
        self,
        slot: str,
        events: list[dict[str, Any]],
    ) -> None:
        previous: str | None = None
        encoded: list[bytes] = []
        for index, event in enumerate(events):
            event["sequence"] = index
            event["previous_event_sha256"] = previous
            if event.get("event") == "lifecycle" and event.get("phase") == "session-end":
                prior_raw = b"".join(encoded)
                event["prior_event_count"] = index
                event["prior_event_log_bytes"] = len(prior_raw)
                event["prior_event_log_sha256"] = hashlib.sha256(prior_raw).hexdigest()
            core = dict(event)
            core.pop("event_sha256", None)
            event["event_sha256"] = verifier.event_digest(core)
            previous = event["event_sha256"]
            encoded.append(verifier.canonical_line(event))
        raw = b"".join(encoded)
        event_path = self.case / slot / "events.jsonl"
        event_path.write_bytes(raw)
        os.chmod(event_path, 0o600)
        capture_path = self.case / slot / "manifest.json"
        capture = json.loads(capture_path.read_text(encoding="utf-8"))
        capture["event_log"] = {
            "bytes": len(raw),
            "event_count": len(events),
            "last_event_sha256": events[-1]["event_sha256"],
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
        write_private_json(capture_path, capture)

    def add_parent_teardown(
        self,
        slot: str,
        *,
        after_child_exit: bool,
        stdin_closed_before_signal: bool,
        stdin_eof_observed_within_grace: bool,
        closure_stimulus: str,
    ) -> None:
        event_path = self.case / slot / "events.jsonl"
        events = [
            json.loads(line)
            for line in event_path.read_text(encoding="utf-8").splitlines()
        ]
        child_index = next(
            index
            for index, event in enumerate(events)
            if event.get("event") == "lifecycle"
            and event.get("phase") == "child-exit"
        )
        child_exit = events[child_index]
        teardown = {
            "schema": child_exit["schema"],
            "run_id": child_exit["run_id"],
            "session_id": child_exit["session_id"],
            "slot": child_exit["slot"],
            "sequence": 0,
            "observed_at": child_exit["observed_at"],
            "event": "lifecycle",
            "previous_event_sha256": None,
            "event_sha256": "0" * 64,
            "phase": "parent-teardown-signal",
            "signal": "SIGTERM",
            "stdin_closed_before_signal": stdin_closed_before_signal,
            "stdin_eof_observed_within_grace": stdin_eof_observed_within_grace,
            "immediate_parent_verified": True,
        }
        events.insert(child_index + int(after_child_exit), teardown)
        end = next(
            event
            for event in events
            if event.get("event") == "lifecycle"
            and event.get("phase") == "session-end"
        )
        end["closure_stimulus"] = closure_stimulus
        self.rebind_session_events(slot, events)

    def rebind_session_summary(self, slot: str, summary: dict[str, Any]) -> None:
        summary_raw = write_private_json(
            self.case / slot / "exact-five-session.json",
            summary,
        )
        capture_path = self.case / slot / "manifest.json"
        capture = json.loads(capture_path.read_text(encoding="utf-8"))
        capture["session_summary"] = material_facts(
            "exact-five-session.json",
            summary_raw,
        )
        write_private_json(capture_path, capture)

    def test_all_new_contract_objects_are_closed(self) -> None:
        for path in SCHEMAS:
            with self.subTest(schema=path.name):
                schema = json.loads(path.read_text(encoding="utf-8"))
                Draft202012Validator.check_schema(schema)
                assert_contract_objects_are_closed(self, schema)

    def test_real_observer_capture_projects_only_the_narrow_pass(self) -> None:
        projection = self.verify()
        self.assertEqual(projection["status"], "capability_pass")
        self.assertEqual(projection["runtime"], self.runtime)
        self.assertEqual(projection["transport"]["request_count"], 7)
        self.assertEqual(projection["transport"]["response_count"], 7)
        self.assertEqual(projection["transport"]["tool_call_count"], 5)
        self.assertEqual(projection["transport"]["provider_transport_calls"], 1)
        self.assertTrue(projection["tunnel"]["teardown_verified"])
        self.assertEqual(
            projection["tunnel"]["mcp_command_sha256"], self.outer_mcp_command_sha256
        )
        receipts = projection["result"]["operation_receipts"]
        self.assertEqual(len(receipts), 5)
        self.assertEqual(len({item["receipt_id"] for item in receipts}), 5)
        self.assertTrue(projection["result"]["inspection_relationship"]["valid"])
        self.assertEqual(projection["claims"], verifier.EXPECTED_CLAIMS)
        rendered = json.dumps(projection, separators=(",", ":"))
        self.assertIsNone(verifier.FORBIDDEN_PUBLIC_TEXT.search(rendered))
        self.assertFalse(
            verifier.nested_field_names(projection) & verifier.FORBIDDEN_PUBLIC_FIELDS
        )

    def test_verifier_accepts_eof_before_sigterm_teardown(self) -> None:
        self.add_parent_teardown(
            "session-2",
            after_child_exit=False,
            stdin_closed_before_signal=True,
            stdin_eof_observed_within_grace=False,
            closure_stimulus="stdin-eof-and-sigterm",
        )
        self.assertEqual(self.verify()["status"], "capability_pass")

    def test_verifier_accepts_sigterm_then_eof_teardown_before_child_exit(self) -> None:
        self.add_parent_teardown(
            "session-2",
            after_child_exit=False,
            stdin_closed_before_signal=False,
            stdin_eof_observed_within_grace=True,
            closure_stimulus="sigterm-then-stdin-eof",
        )
        self.assertEqual(self.verify()["status"], "capability_pass")

    def test_verifier_rejects_mismatched_teardown_closure(self) -> None:
        self.add_parent_teardown(
            "session-2",
            after_child_exit=False,
            stdin_closed_before_signal=False,
            stdin_eof_observed_within_grace=True,
            closure_stimulus="stdin-eof-and-sigterm",
        )
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "parent teardown closure is inconsistent",
        ):
            self.verify()

    def test_verifier_rejects_child_exit_before_any_parent_teardown(self) -> None:
        self.add_parent_teardown(
            "session-2",
            after_child_exit=True,
            stdin_closed_before_signal=False,
            stdin_eof_observed_within_grace=True,
            closure_stimulus="sigterm-then-stdin-eof",
        )
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "lifecycle is not the exact closed sequence",
        ):
            self.verify()

    def test_status_contract_rejects_leakage_and_false_teardown(self) -> None:
        status_validator = validator(verifier.STATUS_SCHEMA)
        accepted = json.loads(
            (self.case / verifier.STATUS_BEFORE_NAME).read_text(encoding="utf-8")
        )
        stopped = json.loads(
            (self.case / verifier.STATUS_STOPPED_NAME).read_text(encoding="utf-8")
        )
        mutations: list[tuple[str, dict[str, Any]]] = []
        for name, value in (
            ("endpoint", "https://example.invalid:443/mcp"),
            ("port", 443),
            ("local_path", "private-local-material"),
        ):
            changed = copy.deepcopy(accepted)
            changed[name] = value
            mutations.append((name, changed))
        running_stop = copy.deepcopy(stopped)
        running_stop["process_running"] = True
        mutations.append(("running stop", running_stop))
        looked_up_stop = copy.deepcopy(stopped)
        looked_up_stop["remote_lookup_attempted"] = True
        mutations.append(("remote lookup after stop", looked_up_stop))
        for label, changed in mutations:
            with self.subTest(mutation=label):
                self.assertTrue(list(status_validator.iter_errors(changed)))

    def test_actual_harness_ready_and_stopped_projections_match_schema(self) -> None:
        source = r"""
import { createHash } from "node:crypto";
import {
  projectStoppedTunnelStatus,
  projectTunnelStatus,
} from "./scripts/qual_206_chatgpt_tunnel_exact_five_harness.mjs";
const alias = "gis-ai-go-v0-2-exact-five-v1";
const tunnelId = "tunnel_6a873e7214308191bfe27240c1c03f68";
const tunnelName = "gis-ai-go-v0-2-interoperability";
const command = "/usr/bin/env -i synthetic-observer-command";
const commandSha256 = createHash("sha256").update(command, "utf8").digest("hex");
const healthUrlFile =
  "/private/tmp/operator/tunnel-state/health/gis-ai-go-v0-2-exact-five-v1.url";
const healthBaseUrl = "http://127.0.0.1:61234";
const raw = {
  alias,
  tunnel_id: tunnelId,
  profile_name: alias,
  remote: { id: tunnelId, name: tunnelName },
  stale: false,
  error: "",
  remote_error: "",
  runtime_state: "ready",
  healthy: true,
  ready: true,
  control_plane_poll_health: {
    state: "unknown",
    reason: "no live admin UI system snapshot",
  },
  remote_lookup_attempted: true,
  process_running: true,
  health_url_file: healthUrlFile,
  process: {
    alias,
    tunnel_id: tunnelId,
    profile_name: alias,
    mode: "process",
    pid: 12345,
    target_kind: "command",
    target_value: command,
  },
  local: {
    effective_health: {
      base_url: healthBaseUrl,
      healthz: { ok: true, status: 200, url: "private-and-not-projected" },
      readyz: { ok: true, status: 200, url: "private-and-not-projected" },
    },
    live_admin_ui: { base_url: "private-and-not-projected" },
  },
  pid: 12345,
};
const pollHealth = {
  locator: {
    kind: "url_file",
    url_file: healthUrlFile,
    resolved_base_url: healthBaseUrl,
  },
  process: { pid: 12345, running: true },
  base_url: healthBaseUrl,
  ui_url: `${healthBaseUrl}/ui`,
  healthz: {
    url: `${healthBaseUrl}/healthz`, ok: true, status: 200, body: "live",
  },
  readyz: {
    url: `${healthBaseUrl}/readyz`, ok: true, status: 200, body: "ready",
  },
  control_plane_poll: {
    url: `${healthBaseUrl}/metrics`, value: Math.floor(Date.now() / 1000), ok: true,
  },
  result: "ok",
};
const ready = projectTunnelStatus(
  raw,
  pollHealth,
  "before",
  commandSha256,
  healthUrlFile,
  "2026-08-27T12:00:00.000Z",
);
const stoppedRaw = {
  ...raw,
  remote: null,
  runtime_state: "stopped",
  healthy: false,
  ready: false,
  remote_lookup_attempted: false,
  process_running: false,
  stopped: true,
  stop_error: "",
  control_plane_poll_health: {
    state: "unknown",
    reason: "no live admin UI system snapshot",
  },
  process: {
    ...raw.process,
    mode: "stopped",
    pid: undefined,
  },
  local: {
    effective_health: {
      healthz: { ok: false, status: 0 },
      readyz: { ok: false, status: 0 },
    },
    live_admin_ui: { found: false },
  },
  pid: undefined,
};
delete stoppedRaw.pid;
delete stoppedRaw.process.pid;
const stopped = projectStoppedTunnelStatus(
  stoppedRaw, commandSha256, "2026-08-27T12:30:00.000Z",
);
process.stdout.write(`${JSON.stringify([ready, stopped])}\n`);
"""
        result = subprocess.run(
            [self.node, "--input-type=module", "--eval", source],
            cwd=ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        ready, stopped = json.loads(result.stdout)
        status_validator = validator(verifier.STATUS_SCHEMA)
        status_validator.validate(ready)
        status_validator.validate(stopped)
        self.assertEqual(
            ready["control_plane_poll_health"],
            {"state": "healthy", "route_kind": "control_plane"},
        )
        self.assertTrue(ready["local"]["direct_healthy_poll_route"])
        self.assertIsNone(stopped["control_plane_poll_health"])
        self.assertFalse(stopped["local"]["direct_healthy_poll_route"])
        rendered = json.dumps([ready, stopped], separators=(",", ":"))
        self.assertNotIn("private-and-not-projected", rendered)

    def test_status_identity_and_command_drift_are_rejected(self) -> None:
        after = json.loads(
            (self.case / verifier.STATUS_AFTER_NAME).read_text(encoding="utf-8")
        )
        after["mcp_command_sha256"] = "c" * 64
        self.rebind_root_file(verifier.STATUS_AFTER_NAME, after, "status_after")
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "identities drifted",
        ):
            self.verify()

    def test_private_contract_rejects_claim_and_host_inflation(self) -> None:
        private_validator = validator(verifier.PRIVATE_SCHEMA)
        manifest = json.loads(
            (self.case / "run-manifest.json").read_text(encoding="utf-8")
        )
        mutations: list[tuple[str, dict[str, Any]]] = []
        malformed_version = copy.deepcopy(manifest)
        malformed_version["host"]["app_version_id"] = "asdk_app_v_invalid"
        mutations.append(("malformed app version", malformed_version))
        direct_http = copy.deepcopy(manifest)
        direct_http["claims"]["direct_public_streamable_http_tls"] = True
        mutations.append(("direct public HTTP", direct_http))
        client_exit = copy.deepcopy(manifest)
        client_exit["execution"]["exit_code"] = 0
        mutations.append(("unproved client exit", client_exit))
        closure = copy.deepcopy(manifest)
        closure["runtime"]["generated_first_party_closure"][
            "reference_matches_current"
        ] = False
        mutations.append(("unbound generated closure", closure))
        local_path = copy.deepcopy(manifest)
        local_path["source"]["local_path"] = "/private/tmp/source"
        mutations.append(("local path", local_path))
        for label, changed in mutations:
            with self.subTest(mutation=label):
                self.assertTrue(list(private_validator.iter_errors(changed)))

    def test_public_contract_rejects_leakage_and_boundary_inflation(self) -> None:
        public_validator = validator(verifier.PUBLIC_SCHEMA)
        projection = self.verify()
        mutations: list[tuple[str, dict[str, Any]]] = []
        endpoint = copy.deepcopy(projection)
        endpoint["tunnel"]["endpoint"] = "https://example.invalid/mcp"
        mutations.append(("endpoint", endpoint))
        malformed_version = copy.deepcopy(projection)
        malformed_version["host"]["app_version_id"] = "asdk_app_v_invalid"
        mutations.append(("malformed app version", malformed_version))
        direct_http = copy.deepcopy(projection)
        direct_http["claims"]["direct_public_streamable_http_tls"] = True
        mutations.append(("direct public HTTP", direct_http))
        no_teardown = copy.deepcopy(projection)
        no_teardown["tunnel"]["teardown_verified"] = False
        mutations.append(("missing teardown", no_teardown))
        for label, changed in mutations:
            with self.subTest(mutation=label):
                self.assertTrue(list(public_validator.iter_errors(changed)))

    def test_independent_result_verifier_rejects_coordinated_raw_mutation(self) -> None:
        session_root = self.case / "session-2"
        result_path = session_root / "exact-five-results.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        result["results"][1]["result"]["structuredContent"]["trace_id"] = "mutated"
        result_raw = write_private_json(result_path, result)
        material = material_facts("exact-five-results.json", result_raw)

        summary_path = session_root / "exact-five-session.json"
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        summary["result_material"] = material
        summary_raw = write_private_json(summary_path, summary)

        capture_path = session_root / "manifest.json"
        capture = json.loads(capture_path.read_text(encoding="utf-8"))
        capture["result_material"] = material
        capture["session_summary"] = material_facts(
            "exact-five-session.json", summary_raw
        )
        write_private_json(capture_path, capture)
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "independent secure-tunnel exact-five result verification failed",
        ):
            self.verify()

    def test_request_event_and_summary_cannot_coordinate_away_from_profile(self) -> None:
        slot = "session-2"
        event_path = self.case / slot / "events.jsonl"
        events = [
            json.loads(line)
            for line in event_path.read_text(encoding="utf-8").splitlines()
        ]
        request = next(
            event
            for event in events
            if event["event"] == "request" and event["method"] == "tools/call"
        )
        changed_arguments = verifier.canonical_bytes({"query": "OTHER", "limit": 1})
        request["arguments_bytes"] = len(changed_arguments)
        request["arguments_sha256"] = hashlib.sha256(changed_arguments).hexdigest()
        self.rebind_session_events(slot, events)

        summary_path = self.case / slot / "exact-five-session.json"
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        summary["operations"][0]["request"]["parameters_bytes"] = len(changed_arguments)
        summary["operations"][0]["request"]["parameters_sha256"] = hashlib.sha256(
            changed_arguments
        ).hexdigest()
        self.rebind_session_summary(slot, summary)
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "request arguments do not match the frozen profile",
        ):
            self.verify()

    def test_event_times_must_remain_inside_the_declared_window(self) -> None:
        slot = "session-2"
        event_path = self.case / slot / "events.jsonl"
        events = [
            json.loads(line)
            for line in event_path.read_text(encoding="utf-8").splitlines()
        ]
        for event in events:
            event["observed_at"] = iso_milliseconds(
                verifier.parse_time(event["observed_at"]) + timedelta(days=1)
            )
        self.rebind_session_events(slot, events)
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "protocol events are outside the declared observation window",
        ):
            self.verify()

    def test_inner_fixture_command_digest_is_independently_bound(self) -> None:
        slot = "session-2"
        event_path = self.case / slot / "events.jsonl"
        events = [
            json.loads(line)
            for line in event_path.read_text(encoding="utf-8").splitlines()
        ]
        events[0]["observer_runtime"]["command_sha256"] = "d" * 64
        self.rebind_session_events(slot, events)
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "runtime or source binding changed",
        ):
            self.verify()

    def test_event_chain_and_global_claim_mutations_are_rejected(self) -> None:
        event_path = self.case / "session-1" / "events.jsonl"
        lines = event_path.read_text(encoding="utf-8").splitlines()
        event = json.loads(lines[2])
        event["client_attribution_valid"] = False
        lines[2] = json.dumps(event, sort_keys=True, separators=(",", ":"))
        event_raw = ("\n".join(lines) + "\n").encode()
        event_path.write_bytes(event_raw)
        os.chmod(event_path, 0o600)
        capture_path = self.case / "session-1" / "manifest.json"
        capture = json.loads(capture_path.read_text(encoding="utf-8"))
        capture["event_log"]["bytes"] = len(event_raw)
        capture["event_log"]["sha256"] = hashlib.sha256(event_raw).hexdigest()
        write_private_json(capture_path, capture)
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "invalid content address",
        ):
            self.verify()

        shutil.rmtree(self.case)
        shutil.copytree(self.capture, self.case)
        claim_path = self.case / verifier.CLAIM_NAME
        claim = json.loads(claim_path.read_text(encoding="utf-8"))
        claim["operation_order"] = list(reversed(claim["operation_order"]))
        self.rebind_root_file(verifier.CLAIM_NAME, claim, "claim")
        with self.assertRaisesRegex(
            verifier.TunnelExactFiveVerificationError,
            "global exact-five claim is invalid",
        ):
            self.verify()

    def test_runtime_closure_comparison_rejects_each_mutation_family(self) -> None:
        generated = self.runtime["generated_first_party_closure"]
        current_generated = {
            "bytes": generated["bytes"],
            "file_count": generated["file_count"],
            "manifest_sha256": generated["manifest_sha256"],
        }
        installed = self.runtime["installed_dependency_closure"]
        verifier.verify_runtime_closure_facts(
            self.runtime,
            current_generated=current_generated,
            current_installed=installed,
            independently_built=self.runtime,
        )
        mutations = []
        wrong_reference = copy.deepcopy(self.runtime)
        wrong_reference["generated_first_party_closure"][
            "reference_manifest_sha256"
        ] = "d" * 64
        mutations.append((wrong_reference, current_generated, installed, wrong_reference))
        wrong_current = copy.deepcopy(current_generated)
        wrong_current["manifest_sha256"] = "d" * 64
        mutations.append((self.runtime, wrong_current, installed, self.runtime))
        wrong_installed = copy.deepcopy(installed)
        wrong_installed["manifest_sha256"] = "d" * 64
        mutations.append((self.runtime, current_generated, wrong_installed, self.runtime))
        wrong_build = copy.deepcopy(self.runtime)
        wrong_build["installed_dependency_closure"]["manifest_sha256"] = "d" * 64
        mutations.append((self.runtime, current_generated, installed, wrong_build))
        for expected, current, dependencies, built in mutations:
            with self.subTest(mutation=built):
                with self.assertRaises(verifier.TunnelExactFiveVerificationError):
                    verifier.verify_runtime_closure_facts(
                        expected,
                        current_generated=current,
                        current_installed=dependencies,
                        independently_built=built,
                    )

    def test_finaliser_writes_once_with_owner_only_mode(self) -> None:
        root = self.case_root / "finaliser"
        root.mkdir(mode=0o700)
        finaliser.write_manifest(root, {"schema": "synthetic-test"})
        output = root / "run-manifest.json"
        self.assertEqual(output.stat().st_mode & 0o777, 0o600)
        self.assertEqual(
            output.read_bytes(),
            verifier.canonical_line({"schema": "synthetic-test"}),
        )
        with self.assertRaises(FileExistsError):
            finaliser.write_manifest(root, {"schema": "second-write"})

    def test_finaliser_builds_runtime_and_stopped_status_into_manifest(self) -> None:
        root = self.case_root / "finaliser-capture"
        shutil.copytree(self.capture, root)
        base = json.loads((root / "run-manifest.json").read_text(encoding="utf-8"))
        (root / "run-manifest.json").unlink()
        arguments = argparse.Namespace(
            private_root=root,
            started_at=base["execution"]["started_at"],
            finished_at=base["execution"]["finished_at"],
            displayed_model="GPT-5",
            app_version_id=FRESH_APP_VERSION,
            conversation_id_sha256="b" * 64,
            node=Path(self.node),
            pnpm=Path(self.node),
        )
        with (
            mock.patch.object(finaliser.verifier, "verify_source"),
            mock.patch.object(
                finaliser.verifier,
                "locate_verified_node",
                return_value=self.node,
            ),
            mock.patch.object(
                finaliser.verifier,
                "independently_reproduce_runtime_closure",
                return_value=copy.deepcopy(self.runtime),
            ) as runtime_reproducer,
        ):
            manifest = finaliser.build_manifest(arguments)
        runtime_reproducer.assert_called_once_with(
            base["source"]["commit"],
            node_path=self.node,
            pnpm_path=Path(self.node),
        )
        self.assertEqual(manifest["runtime"], self.runtime)
        self.assertEqual(manifest["execution"]["exit_code"], None)
        self.assertEqual(manifest["execution"]["signal"], None)
        self.assertEqual(
            manifest["private_files"]["status_stopped"]["name"],
            verifier.STATUS_STOPPED_NAME,
        )


if __name__ == "__main__":
    unittest.main()
