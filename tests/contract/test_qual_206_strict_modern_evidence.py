from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest import mock

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
COMPILER_PATH = ROOT / "scripts" / "compile_qual_206_strict_modern_evidence.py"
CAPTURE_SCHEMA_PATH = (
    ROOT / "schemas" / "qual-206-strict-modern-host-capture.schema.json"
)
EVIDENCE_SCHEMA_PATH = (
    ROOT / "schemas" / "qual-206-strict-modern-host-evidence.schema.json"
)
EXACT_OPERATIONS = [
    "catalogue.search",
    "catalogue.describe",
    "selection.resolve",
    "data.query",
    "evidence.inspect",
]
EXACT_RESOURCES = [
    "catalogue.public",
    "catalogue.record",
    "evidence.receipt",
]
HISTORICAL_V1_SHA256 = {
    "evaluation/qual-206-local-evaluation-receipts.v1.json": (
        "de94f097c6bbd6a9b1cb7f4eddff38933835233254f262f664cddfeaca048088"
    ),
    "evaluation/qual-206-local-protocol-evidence-matrix.v1.json": (
        "ef2ce33b55b7250c00edc0b61067c048d23f374c1ba6fe07af332975cd48c541"
    ),
    "tests/interoperability/qual_206_cases.json": (
        "23ac9bc1a76d524bd0e250b11b9ba321b09e66bd5921f1463f50c150001cd389"
    ),
    "tests/interoperability/qual_206_cases_expansion.json": (
        "e70c21b371593c2dae863999745f1fecf2152ff80f0b025a1ccbec135b47f4af"
    ),
    "tests/interoperability/evidence/chatgpt-tunnel-2026-08-20.json": (
        "5194129281837f85fef65f3d975522140570a3ecdd85bd836bc03037d434b568"
    ),
    "tests/interoperability/evidence/codex-cli-2026-08-20.json": (
        "1507e1889423444867353adf520308be10bb502d07a8c0cb4c6bf70d20dae127"
    ),
    "tests/interoperability/evidence/independent-host-readiness-2026-08-20.json": (
        "9cb4e569d7a1be9399a700f5d628ae7ace22318be9c7fc3cd055de326c5f7fbe"
    ),
    "tests/interoperability/evidence/legacy-fallback-exploratory-2026-08-20.json": (
        "5d2c22c17b7a0c65bd3957f9d23057ab7a5d522d223ed432642250b997823537"
    ),
    (
        "tests/interoperability/evidence/"
        "claude-code-legacy-stdio-readiness-2026-08-23.json"
    ): "a3d40e2013095baf977bad336366c0fb429a05b6a5a267c3e069595e4cdb1a6b",
    (
        "tests/interoperability/evidence/"
        "claude-code-2.1.241-stdio-observation-2026-08-24.json"
    ): "d2cd72b7f16a0bafd8a7190b87b14f150b7fa975f6d70f5e779eb9ddf5f92478",
    "schemas/qual-206-local-evaluation-receipt-set.schema.json": (
        "9584de9fe7531457b7b83eb7f9102ee897e2cae61a5fe1f5f68b0f6b775232d9"
    ),
    "schemas/qual-206-local-protocol-evidence-matrix.schema.json": (
        "baa856f4c0d28a497360c9af0526e6e0b3aa6698f19e1857549e988f48f4931a"
    ),
    "schemas/qual-206-evaluation-expansion.schema.json": (
        "1843351626b6f96cb118e575388606daa0d6f60b22b28b92d9655a14873caf8b"
    ),
    "schemas/qual-206-legacy-stdio-readiness.schema.json": (
        "5ce73d3d45c762112ac932407000b4379d07d92a9e54808227cd72e6050fd02a"
    ),
    "schemas/qual-206-claude-code-stdio-observation.schema.json": (
        "78b9a8071a6954028576f397c98dd0fc4b87dddbaf72654f6459407b280e2a9b"
    ),
}


def load_compiler() -> Any:
    specification = importlib.util.spec_from_file_location(
        "qual_206_strict_modern_evidence_compiler",
        COMPILER_PATH,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load the QUAL-206 evidence compiler")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain one JSON object")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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


def nested_field_names(node: object) -> set[str]:
    names: set[str] = set()
    if isinstance(node, dict):
        names.update(node)
        for value in node.values():
            names.update(nested_field_names(value))
    elif isinstance(node, list):
        for value in node:
            names.update(nested_field_names(value))
    return names


def make_capture(state: str = "capability_pass") -> dict[str, Any]:
    if state not in {"not_ready", "ready_unscored", "capability_pass"}:
        raise ValueError(f"unknown fixture state: {state}")
    ready = state != "not_ready"
    capability = state == "capability_pass"
    digest = "1" * 64
    capture: dict[str, Any] = {
        "schema": "gis-ai-go.qual-206-strict-modern-host-capture.v1",
        "capture_kind": "synthetic-test-fixture",
        "observed_at": "2026-08-25T09:00:00Z",
        "source": {
            "repository": "chris-page-gov/gis-ai-go",
            "commit": "0" * 40,
            "tree": "0" * 40,
            "protected_main": False,
            "detached_checkout": False,
            "worktree_clean": False,
            "product_version": "0.2.0",
            "materials": [
                {
                    "role": "source",
                    "path": "packages/evidence/src/index.ts",
                    "sha256": digest,
                }
            ],
        },
        "host": {
            "name": "synthetic-test-host",
            "version": "1.0.0",
            "platform": "darwin",
            "architecture": "arm64",
            "identity": {
                "kind": "package",
                "name": "synthetic-test-host",
                "version": "1.0.0",
                "sha256": "2" * 64,
            },
            "probe": "model-task" if capability else "mcp-list",
            "model_authentication_supplied": capability,
            "model_task_requested": capability,
        },
        "protocol": {
            "target_version": "2026-07-28",
            "target_source_id": "S-MCP-SPEC",
            "client_requested_version": "2026-07-28",
            "server_supported_versions": ["2026-07-28"],
            "negotiated_version": "2026-07-28" if ready else None,
        },
        "surface": {
            "assembly": "candidate-unregistered-exact-five",
            "transport": "stdio",
            "operations": EXACT_OPERATIONS,
            "resources": EXACT_RESOURCES,
        },
        "corpus": {
            "base": {
                "path": "tests/interoperability/qual_206_cases.json",
                "sha256": HISTORICAL_V1_SHA256[
                    "tests/interoperability/qual_206_cases.json"
                ],
            },
            "expansion": {
                "path": "tests/interoperability/qual_206_cases_expansion.json",
                "sha256": HISTORICAL_V1_SHA256[
                    "tests/interoperability/qual_206_cases_expansion.json"
                ],
            },
            "case_ids": [f"QUAL-206-HOST-{index:03d}" for index in range(1, 11)],
        },
        "isolation": {
            "temporary_profile": True,
            "profile_root_mode": "0700",
            "primary_configuration_mode": "0600",
            "normal_profile_used": False,
            "normal_profile_mutation_observed": False,
            "credential_variables_removed_count": 5,
            "mcp_child_environment_allowlisted": True,
            "credential_value_pattern_matches": 0,
            "remaining_processes_after_cleanup": 0,
            "raw_host_logs_published": False,
            "os_network_isolation_enforced": True,
            "provider_egress_guard_exercised": True,
        },
        "telemetry": {
            "schema": "gis-ai-go.qual-206-host-capture-summary.v1",
            "retained_private": {
                "path": "telemetry.json",
                "bytes": 1,
                "sha256": "0" * 64,
                "mode": "0600",
            },
            "event_count": 25 if capability else 9 if ready else 4,
            "session_start_count": 1,
            "request_count": 11 if capability else 3 if ready else 1,
            "notification_count": 1 if ready else 0,
            "response_count": 11 if capability else 3 if ready else 1,
            "session_end_count": 1,
            "anomaly_count": 0,
            "malformed_frame_count": 0,
            "non_json_frame_count": 0,
            "truncated_frame_count": 0,
            "server_stderr_count": 0,
            "pending_request_count": 0,
            "exit_code": 0 if ready else 1,
            "raw_content_published": False,
        },
        "observation": {
            "host_report": "connected" if ready else "failed-to-connect",
            "initialize": {
                "observed": True,
                "outcome": "success" if ready else "error",
                "error_code": None if ready else -32000,
            },
            "initialized_notification_observed": ready,
            "tools_list": {
                "observed": ready,
                "outcome": "success" if ready else "not-observed",
                "operations": EXACT_OPERATIONS if ready else [],
                "error_code": None,
            },
            "resources_list": {
                "observed": ready,
                "outcome": "success" if ready else "not-observed",
                "resources": EXACT_RESOURCES if ready else [],
                "error_code": None,
            },
            "tool_results": [],
            "resource_results": [],
            "cancellation": {"observed": False, "outcome": "not-tested"},
            "unsupported_traffic": {"observed": False, "outcome": "not-tested"},
        },
    }
    if capability:
        capture["observation"]["tool_results"] = [
            {
                "operation": operation,
                "outcome": "success",
                "structured_plain_text_parity": "passed",
                "receipt_present": True,
                "request_sha256": f"{index:x}" * 64,
                "response_sha256": f"{index + 5:x}" * 64,
            }
            for index, operation in enumerate(EXACT_OPERATIONS, start=1)
        ]
        capture["observation"]["resource_results"] = [
            {
                "resource": resource,
                "outcome": "success",
                "response_sha256": f"{index + 10:x}" * 64,
            }
            for index, resource in enumerate(EXACT_RESOURCES, start=1)
        ]
        capture["observation"]["cancellation"] = {
            "observed": True,
            "outcome": "passed",
        }
        capture["observation"]["unsupported_traffic"] = {
            "observed": True,
            "outcome": "passed",
        }
    return capture


def make_observed_source_capture() -> tuple[dict[str, Any], dict[str, bytes]]:
    capture = make_capture("ready_unscored")
    capture["capture_kind"] = "observed-host-session"
    capture["host"].update(
        {
            "name": "claude-code",
            "identity": {
                "kind": "package",
                "name": "@anthropic-ai/claude-code",
                "version": "2.1.241",
                "sha256": "3" * 64,
            },
        }
    )
    blobs: dict[str, bytes] = {}
    materials = []
    for role, path in sorted(COMPILER.REQUIRED_OBSERVED_MATERIALS):
        content = f"{role}:{path}\n".encode()
        blobs[path] = content
        materials.append({"role": role, "path": path, "sha256": sha256_bytes(content)})
    for reference in (capture["corpus"]["base"], capture["corpus"]["expansion"]):
        blobs[reference["path"]] = (ROOT / reference["path"]).read_bytes()
    capture["source"].update(
        {
            "commit": "a" * 40,
            "tree": "b" * 40,
            "protected_main": True,
            "detached_checkout": True,
            "worktree_clean": True,
            "materials": materials,
        }
    )
    return capture, blobs


class PrivateCapture:
    def __init__(self, test_case: unittest.TestCase, state: str = "capability_pass"):
        self.test_case = test_case
        self.temporary = tempfile.TemporaryDirectory(prefix="qual-206-strict-test-")
        self.root = Path(self.temporary.name)
        self.root.chmod(0o700)
        self.capture_path = self.root / "capture.json"
        self.telemetry_path = self.root / "telemetry.json"
        self.output_path = self.root / "public-evidence.json"
        self.capture = make_capture(state)
        self.write_telemetry(b'{"private":"telemetry"}\n')
        self.write_capture()

    def write_telemetry(self, value: bytes) -> None:
        self.telemetry_path.write_bytes(value)
        self.telemetry_path.chmod(0o600)
        retained = self.capture["telemetry"]["retained_private"]
        retained["bytes"] = len(value)
        retained["sha256"] = sha256_bytes(value)

    def write_capture(self, raw: bytes | None = None) -> None:
        value = (
            raw
            if raw is not None
            else (json.dumps(self.capture, ensure_ascii=False, indent=2) + "\n").encode()
        )
        self.capture_path.write_bytes(value)
        self.capture_path.chmod(0o600)

    def compile(self) -> dict[str, Any]:
        return COMPILER.compile_capture(self.root, self.capture_path, self.output_path)

    def close(self) -> None:
        self.temporary.cleanup()


COMPILER = load_compiler()


class Qual206StrictModernEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.capture_schema = load_json(CAPTURE_SCHEMA_PATH)
        cls.evidence_schema = load_json(EVIDENCE_SCHEMA_PATH)
        cls.capture_validator = Draft202012Validator(
            cls.capture_schema,
            format_checker=FormatChecker(),
        )
        cls.evidence_validator = Draft202012Validator(
            cls.evidence_schema,
            format_checker=FormatChecker(),
        )

    def fixture(self, state: str = "capability_pass") -> PrivateCapture:
        fixture = PrivateCapture(self, state)
        self.addCleanup(fixture.close)
        return fixture

    def assert_valid_public_evidence(self, evidence: dict[str, Any]) -> None:
        errors = sorted(
            self.evidence_validator.iter_errors(evidence),
            key=lambda error: [str(part) for part in error.absolute_path],
        )
        self.assertEqual(
            [],
            [
                f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
                for error in errors
            ],
        )

    def assert_compile_rejected(self, fixture: PrivateCapture, pattern: str) -> None:
        with self.assertRaisesRegex((COMPILER.EvidenceError, OSError), pattern):
            fixture.compile()

    def verify_mocked_observed_source(
        self,
        capture: dict[str, Any],
        blobs: dict[str, bytes],
        *,
        ancestor_returncode: int = 0,
    ) -> None:
        commit = capture["source"]["commit"]

        def fake_git_output(*arguments: str) -> bytes:
            if arguments == ("rev-parse", f"{commit}^{{tree}}"):
                return b"b" * 40 + b"\n"
            if arguments == ("rev-parse", "--verify", "refs/remotes/origin/main"):
                return b"c" * 40 + b"\n"
            if len(arguments) == 2 and arguments[0] == "show":
                prefix = f"{commit}:"
                self.assertTrue(arguments[1].startswith(prefix))
                return blobs[arguments[1][len(prefix) :]]
            raise AssertionError(f"unexpected git call: {arguments!r}")

        with (
            mock.patch.object(COMPILER, "git_output", side_effect=fake_git_output),
            mock.patch.object(
                COMPILER.subprocess,
                "run",
                return_value=SimpleNamespace(returncode=ancestor_returncode),
            ),
            mock.patch.object(
                COMPILER,
                "read_repository_material",
                side_effect=lambda path: blobs[path],
            ),
        ):
            COMPILER.verify_observed_source(capture)

    def test_schemas_are_valid_and_all_object_contracts_are_closed(self) -> None:
        for schema in (self.capture_schema, self.evidence_schema):
            Draft202012Validator.check_schema(schema)
            assert_contract_objects_are_closed(self, schema)

    def test_synthetic_not_ready_compiles_fail_closed_public_evidence(self) -> None:
        fixture = self.fixture("not_ready")
        evidence = fixture.compile()
        self.assertEqual(evidence["status"], "not_ready")
        self.assertEqual(evidence["readiness"]["outcome"], "not_ready")
        self.assertEqual(evidence["capability"]["outcome"], "unscored")
        self.assert_valid_public_evidence(evidence)

    def test_synthetic_ready_unscored_compiles_without_capability_claim(self) -> None:
        fixture = self.fixture("ready_unscored")
        evidence = fixture.compile()
        self.assertEqual(evidence["status"], "ready_unscored")
        self.assertEqual(evidence["readiness"]["outcome"], "ready")
        self.assertEqual(evidence["capability"]["outcome"], "unscored")
        self.assertFalse(evidence["claims"]["strict_modern_transport_ready"])
        self.assert_valid_public_evidence(evidence)

    def test_synthetic_capability_pass_exercises_compiler_without_real_claims(self) -> None:
        fixture = self.fixture("capability_pass")
        evidence = fixture.compile()
        self.assertEqual(evidence["classification"], "synthetic-test-only")
        self.assertEqual(evidence["status"], "capability_pass")
        self.assertEqual(evidence["capability"]["outcome"], "passed")
        self.assertTrue(evidence["capability"]["exact_five_capability_exercised"])
        self.assertFalse(any(evidence["claims"].values()))
        self.assert_valid_public_evidence(evidence)

    def test_observed_summary_is_capped_at_ready_unscored_and_all_host_claims_false(self) -> None:
        capture = make_capture("capability_pass")
        capture["capture_kind"] = "observed-host-session"
        capture["host"].update(
            {
                "name": "claude-code",
                "identity": {
                    "kind": "package",
                    "name": "@anthropic-ai/claude-code",
                    "version": "2.1.241",
                    "sha256": "3" * 64,
                },
            }
        )
        capture_bytes = (json.dumps(capture, separators=(",", ":")) + "\n").encode()
        evidence = COMPILER.compile_evidence(capture, capture_bytes)
        self.assertEqual(
            evidence["classification"],
            "pre-activation-strict-modern-host-summary",
        )
        self.assertEqual(evidence["status"], "ready_unscored")
        self.assertEqual(evidence["capability"]["outcome"], "unscored")
        for claim in (
            "live_host_session",
            "strict_modern_transport_ready",
            "capability_scored",
            "exact_five_host_capability",
            "remote_http_host",
        ):
            self.assertFalse(evidence["claims"][claim], claim)
        self.assert_valid_public_evidence(evidence)

    def test_observed_source_binding_accepts_only_the_closed_verified_inventory(self) -> None:
        capture, blobs = make_observed_source_capture()
        self.verify_mocked_observed_source(capture, blobs)

        mutations: list[tuple[str, Any, str, int]] = [
            (
                "tree",
                lambda value, _: value["source"].update({"tree": "d" * 40}),
                "source tree does not match",
                0,
            ),
            (
                "ancestry",
                lambda _value, _blobs: None,
                "not accepted protected-main history",
                1,
            ),
            (
                "missing",
                lambda value, _: value["source"]["materials"].pop(),
                "inventory is not closed",
                0,
            ),
            (
                "duplicate",
                lambda value, _: value["source"]["materials"].append(
                    copy.deepcopy(value["source"]["materials"][0])
                ),
                "duplicate source material",
                0,
            ),
            (
                "tracked-digest",
                lambda value, _: value["source"]["materials"][0].update(
                    {"sha256": "0" * 64}
                ),
                "source material digest mismatch",
                0,
            ),
            (
                "compiled-digest",
                lambda value, _: next(
                    item
                    for item in value["source"]["materials"]
                    if item["role"] == "compiled"
                ).update({"sha256": "0" * 64}),
                "compiled material digest mismatch",
                0,
            ),
            (
                "corpus",
                lambda value, _: value["corpus"]["base"].update(
                    {"sha256": "0" * 64}
                ),
                "corpus digest mismatch",
                0,
            ),
        ]
        for label, mutate, pattern, ancestor_returncode in mutations:
            with self.subTest(label=label):
                changed, changed_blobs = make_observed_source_capture()
                mutate(changed, changed_blobs)
                with self.assertRaisesRegex(COMPILER.EvidenceError, pattern):
                    self.verify_mocked_observed_source(
                        changed,
                        changed_blobs,
                        ancestor_returncode=ancestor_returncode,
                    )

    def test_shared_rfc8785_identity_is_deterministic_and_materially_bound(self) -> None:
        expected_vector = (
            "gis-ai-go:qual-206-strict-modern-host-evidence:sha256:"
            "7651a65e4c2ce6e019c2916850adc012cf5b7748c7139a5ac5776f7ffe67831d"
        )
        self.assertEqual(
            COMPILER.shared_content_address({"z": 1, "a": "é"}),
            expected_vector,
        )
        self.assertEqual(
            COMPILER.shared_content_address({"a": "é", "z": 1}),
            expected_vector,
        )
        for unsafe_integer in (9007199254740992, 9007199254740993):
            with self.subTest(unsafe_integer=unsafe_integer):
                with self.assertRaisesRegex(
                    COMPILER.EvidenceError,
                    "shared canonical identity helper failed closed",
                ):
                    COMPILER.shared_content_address({"error_code": unsafe_integer})
        capture = make_capture("ready_unscored")
        capture_bytes = (json.dumps(capture, separators=(",", ":")) + "\n").encode()
        first = COMPILER.compile_evidence(copy.deepcopy(capture), capture_bytes)
        second = COMPILER.compile_evidence(copy.deepcopy(capture), capture_bytes)
        self.assertEqual(first["evidence_id"], second["evidence_id"])
        changed = copy.deepcopy(capture)
        changed["observed_at"] = "2026-08-25T09:00:01Z"
        changed_bytes = (json.dumps(changed, separators=(",", ":")) + "\n").encode()
        third = COMPILER.compile_evidence(changed, changed_bytes)
        self.assertNotEqual(first["evidence_id"], third["evidence_id"])

    def test_public_projection_excludes_private_paths_and_telemetry_identity(self) -> None:
        fixture = self.fixture("capability_pass")
        private_digest = fixture.capture["telemetry"]["retained_private"]["sha256"]
        evidence = fixture.compile()
        public = json.dumps(evidence, ensure_ascii=False, sort_keys=True)
        retained = evidence["telemetry"]["retained_private"]
        self.assertEqual(
            set(retained),
            {
                "retention",
                "raw_content_published",
                "digest_published",
                "byte_count_published",
            },
        )
        self.assertNotIn(str(fixture.root), public)
        self.assertNotIn("telemetry.json", public)
        self.assertNotIn(private_digest, public)
        self.assertFalse(
            {"arguments", "environment", "headers", "raw_payload", "raw_result"}
            & nested_field_names(evidence)
        )
        self.assert_valid_public_evidence(evidence)

    def test_existing_output_is_never_overwritten(self) -> None:
        fixture = self.fixture("ready_unscored")
        first = fixture.compile()
        first_bytes = fixture.output_path.read_bytes()
        self.assertEqual(first["status"], "ready_unscored")
        self.assert_compile_rejected(fixture, "already exists|never overwritten")
        self.assertEqual(fixture.output_path.read_bytes(), first_bytes)

    def test_output_parent_symlink_is_rejected(self) -> None:
        fixture = self.fixture("ready_unscored")
        actual = fixture.root / "actual-output"
        actual.mkdir(mode=0o700)
        link = fixture.root / "linked-output"
        link.symlink_to(actual.name, target_is_directory=True)
        fixture.output_path = link / "public-evidence.json"
        self.assert_compile_rejected(fixture, "must not traverse a symbolic link")

    def test_final_capture_symlink_is_rejected(self) -> None:
        fixture = self.fixture()
        target = fixture.root / "capture-target.json"
        fixture.capture_path.rename(target)
        fixture.capture_path.symlink_to(target.name)
        self.assert_compile_rejected(
            fixture,
            "symbolic link|Too many levels|Not a directory",
        )

    def test_parent_symlink_in_capture_path_is_rejected(self) -> None:
        fixture = self.fixture()
        actual = fixture.root / "actual"
        actual.mkdir(mode=0o700)
        nested_capture = actual / "capture.json"
        nested_capture.write_bytes(fixture.capture_path.read_bytes())
        nested_capture.chmod(0o600)
        link = fixture.root / "linked"
        link.symlink_to(actual.name, target_is_directory=True)
        fixture.capture_path = link / "capture.json"
        self.assert_compile_rejected(
            fixture,
            "symbolic link|Too many levels|Not a directory",
        )

    def test_hardlinked_capture_is_rejected(self) -> None:
        fixture = self.fixture()
        os.link(fixture.capture_path, fixture.root / "capture-backup.json")
        self.assert_compile_rejected(fixture, "exactly one hard link")

    def test_non_owner_only_capture_mode_is_rejected(self) -> None:
        fixture = self.fixture()
        fixture.capture_path.chmod(0o640)
        self.assert_compile_rejected(fixture, "owner-only mode 0600")

    def test_fifo_capture_is_rejected_without_blocking(self) -> None:
        fixture = self.fixture()
        fixture.capture_path.unlink()
        os.mkfifo(fixture.capture_path, mode=0o600)
        self.assert_compile_rejected(fixture, "must be a regular file")

    def test_oversized_capture_is_rejected_before_parsing(self) -> None:
        fixture = self.fixture()
        fixture.capture_path.write_bytes(b"x" * (COMPILER.MAX_CAPTURE_BYTES + 1))
        self.assert_compile_rejected(fixture, "size is outside the accepted boundary")

    def test_duplicate_json_object_key_is_rejected(self) -> None:
        fixture = self.fixture()
        fixture.write_capture(b'{"schema":"first","schema":"second"}\n')
        self.assert_compile_rejected(fixture, "duplicate JSON object key: schema")

    def test_non_standard_json_number_is_rejected(self) -> None:
        fixture = self.fixture()
        fixture.write_capture(b'{"schema":"first","event_count":NaN}\n')
        self.assert_compile_rejected(fixture, "non-standard JSON number: NaN")

    def test_malformed_utf8_is_rejected(self) -> None:
        fixture = self.fixture()
        fixture.write_capture(b"\xff\n")
        self.assert_compile_rejected(fixture, "is not UTF-8")

    def test_escaped_surrogate_is_rejected_before_canonical_identity(self) -> None:
        fixture = self.fixture()
        fixture.write_capture(b'{"schema":"\\ud800"}\n')
        self.assert_compile_rejected(fixture, "surrogate code point")

    def test_public_privacy_guard_and_real_capability_schema_fail_closed(self) -> None:
        fixture = self.fixture("capability_pass")
        evidence = fixture.compile()
        leaked = copy.deepcopy(evidence)
        leaked["host"]["version"] = "ghp_abcdefgh12345678"
        with self.assertRaisesRegex(COMPILER.EvidenceError, "private path, secret"):
            COMPILER.assert_public_safe(leaked)

        forged = copy.deepcopy(evidence)
        forged["classification"] = "pre-activation-strict-modern-host-summary"
        errors = list(self.evidence_validator.iter_errors(forged))
        self.assertTrue(errors, "real-host capability_pass must be schema-invalid")

    def test_private_telemetry_digest_and_count_mismatches_are_rejected(self) -> None:
        with self.subTest("digest"):
            fixture = self.fixture()
            fixture.capture["telemetry"]["retained_private"]["sha256"] = "f" * 64
            fixture.write_capture()
            self.assert_compile_rejected(fixture, "telemetry digest does not match")
        with self.subTest("closed counters"):
            fixture = self.fixture()
            fixture.capture["telemetry"]["event_count"] += 1
            fixture.write_capture()
            self.assert_compile_rejected(fixture, "event_count does not match")

    def test_ready_summary_requires_matching_protocol_host_and_supporting_events(self) -> None:
        with self.subTest("protocol"):
            fixture = self.fixture("ready_unscored")
            fixture.capture["protocol"]["client_requested_version"] = "2025-11-25"
            fixture.write_capture()
            self.assert_compile_rejected(
                fixture,
                "negotiated protocol must equal the client-requested version",
            )
        with self.subTest("host"):
            fixture = self.fixture("ready_unscored")
            fixture.capture["observation"]["host_report"] = "failed-to-connect"
            fixture.write_capture()
            evidence = fixture.compile()
            self.assertEqual(evidence["status"], "not_ready")
            self.assertEqual(evidence["readiness"]["outcome"], "not_ready")
        with self.subTest("counters"):
            fixture = self.fixture("ready_unscored")
            telemetry = fixture.capture["telemetry"]
            telemetry["request_count"] = 0
            telemetry["response_count"] = 0
            telemetry["event_count"] = 3
            fixture.write_capture()
            self.assert_compile_rejected(
                fixture,
                "request_count cannot support the observed stages",
            )

    def test_historical_v1_artifacts_remain_byte_exact(self) -> None:
        self.assertEqual(
            COMPILER.HISTORICAL_LINEAGE,
            [
                {"path": path, "sha256": HISTORICAL_V1_SHA256[path]}
                for path in (
                    "schemas/qual-206-claude-code-stdio-observation.schema.json",
                    (
                        "tests/interoperability/evidence/"
                        "claude-code-2.1.241-stdio-observation-2026-08-24.json"
                    ),
                    "schemas/qual-206-legacy-stdio-readiness.schema.json",
                    (
                        "tests/interoperability/evidence/"
                        "claude-code-legacy-stdio-readiness-2026-08-23.json"
                    ),
                    "tests/interoperability/qual_206_cases.json",
                )
            ],
        )
        for relative_path, expected in HISTORICAL_V1_SHA256.items():
            with self.subTest(path=relative_path):
                self.assertEqual(
                    sha256_bytes((ROOT / relative_path).read_bytes()),
                    expected,
                )


if __name__ == "__main__":
    unittest.main()
