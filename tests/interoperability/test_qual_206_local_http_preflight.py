from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "qual_206_verify_local_http_preflight.py"
SPEC = importlib.util.spec_from_file_location("qual_206_local_http_verifier", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


class LocalHttpPreflightVerifierTest(unittest.TestCase):
    @staticmethod
    def openapi_fixture() -> tuple[dict[str, object], list[dict[str, object]]]:
        paths: dict[str, object] = {}
        schemas: dict[str, object] = {
            "Health": {"type": "object", "title": "Health"},
            "Readiness": {"type": "object", "title": "Readiness"},
        }
        tools: list[dict[str, object]] = []
        for name in VERIFIER.EXACT_OPERATIONS:
            contract = VERIFIER.OPENAPI_OPERATION_CONTRACTS[name]
            input_schema = (
                {"oneOf": [{"type": "object"}], "title": f"{name} input"}
                if name == "evidence.inspect"
                else {"type": "object", "title": f"{name} input"}
            )
            advertised_input_schema = (
                {**input_schema, "type": "object"}
                if name == "evidence.inspect"
                else input_schema
            )
            output_schema = {"type": "object", "title": f"{name} output"}
            tools.append(
                {
                    "name": name,
                    "inputSchema": advertised_input_schema,
                    "outputSchema": output_schema,
                }
            )
            schemas[contract["input_component"]] = input_schema
            schemas[contract["output_component"]] = output_schema
            paths[contract["path"]] = {
                "post": {
                    "operationId": contract["operation_id"],
                    "x-gis-ai-go-operation": name,
                    "x-gis-ai-go-lifecycle": "candidate-conformance-only",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": (
                                        "#/components/schemas/"
                                        f"{contract['input_component']}"
                                    )
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": (
                                            "#/components/schemas/"
                                            f"{contract['output_component']}"
                                        )
                                    }
                                }
                            }
                        }
                    },
                }
            }
        paths["/healthz"] = {
            "get": {
                "operationId": "healthCheck",
                "responses": {
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Health"}
                            }
                        }
                    }
                },
            }
        }
        readiness_response = {
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Readiness"}
                }
            }
        }
        paths["/readyz"] = {
            "get": {
                "operationId": "readinessCheck",
                "responses": {
                    "200": deepcopy(readiness_response),
                    "503": deepcopy(readiness_response),
                },
            }
        }
        paths["/openapi.json"] = {
            "get": {
                "operationId": "openApiContract",
                "responses": {
                    "200": {
                        "content": {
                            "application/json": {"schema": {"type": "object"}}
                        }
                    }
                },
            }
        }
        return {"paths": paths, "components": {"schemas": schemas}}, tools

    @staticmethod
    def schema_digest_manifest_fixture(
        tools: list[dict[str, object]],
    ) -> dict[str, object]:
        by_operation = {tool["name"]: tool for tool in tools}
        return {
            "schema": VERIFIER.CANONICAL_SCHEMA_DIGEST_MANIFEST_ID,
            "algorithm": VERIFIER.CANONICAL_SCHEMA_DIGEST_ALGORITHM,
            "domain": VERIFIER.CANONICAL_SCHEMA_DIGEST_DOMAIN,
            "operations": [
                {
                    "operation": operation,
                    "input_schema_sha256": VERIFIER.canonical_tool_schema_sha256(
                        operation,
                        "input",
                        by_operation[operation]["inputSchema"],
                    ),
                    "output_schema_sha256": VERIFIER.canonical_tool_schema_sha256(
                        operation,
                        "output",
                        by_operation[operation]["outputSchema"],
                    ),
                }
                for operation in VERIFIER.EXACT_OPERATIONS
            ],
        }

    @staticmethod
    def idempotency_evidence_fixture() -> tuple[
        tuple[dict[str, object], dict[str, object]],
        dict[str, str],
        dict[str, str],
        str,
    ]:
        successful_key = f"gis-ai-go:ik:v1:{'9' * 64}"
        aborted_key = f"gis-ai-go:ik:v1:{'8' * 64}"
        receipt = f"gis-ai-go:evidence-receipt:sha256:{'1' * 64}"
        common = {
            "schema": "gis-ai-go.qual-206-exact-five-http-audit.v1",
            "event": "idempotency-evidence-state",
        }
        successful = {
            **common,
            "role": "successful",
            "idempotency_key_sha256": VERIFIER.public_idempotency_key_sha256(
                successful_key
            ),
            "reconciliation_status": "completed",
            "claim_id": f"gis-ai-go:evidence-reconciliation-claim:sha256:{'2' * 64}",
            "resolution_id": (
                "gis-ai-go:evidence-reconciliation-resolution:sha256:"
                f"{'3' * 64}"
            ),
            "receipt_id": receipt,
            "record_id": f"gis-ai-go:public-evidence-record:sha256:{'4' * 64}",
            "ledger_event_id": f"gis-ai-go:evidence-ledger-event:sha256:{'5' * 64}",
            "ledger_event_sequence": 4,
            "completed_evidence_created": True,
        }
        aborted = {
            **common,
            "role": "aborted",
            "idempotency_key_sha256": VERIFIER.public_idempotency_key_sha256(aborted_key),
            "reconciliation_status": "pending",
            "claim_id": f"gis-ai-go:evidence-reconciliation-claim:sha256:{'6' * 64}",
            "resolution_id": None,
            "receipt_id": None,
            "record_id": None,
            "ledger_event_id": None,
            "ledger_event_sequence": None,
            "completed_evidence_created": False,
        }
        return (
            (successful, aborted),
            {"idempotency_key": successful_key},
            {"idempotency_key": aborted_key},
            receipt,
        )

    @classmethod
    def audit_capture_fixture(
        cls,
    ) -> tuple[dict[str, object], dict[str, str], dict[str, str], str]:
        evidence, successful, aborted, receipt = cls.idempotency_evidence_fixture()
        guarded_apis = list(VERIFIER.EXACT_GUARDED_APIS)
        events = [
            {
                "schema": VERIFIER.PROVIDER_EGRESS_GUARD_SCHEMA_ID,
                "event": "provider-egress-guard-ready",
                "guarded_apis": guarded_apis,
            },
            {
                "schema": VERIFIER.AUDIT_SCHEMA_ID,
                "event": "server-listening",
                "scenario": "capability-pack",
                "source_commit": "a" * 40,
                "transport": "operating-system-loopback-http",
                "host": "127.0.0.1",
                "port": 49152,
                "state": "candidate-unregistered",
                "production_registration": False,
            },
            *(
                {
                    "schema": VERIFIER.AUDIT_SCHEMA_ID,
                    "event": event,
                    "scenario": "capability-pack",
                    "ordinal": ordinal,
                }
                for event, ordinal in (
                    ("provider-transport-started", 1),
                    ("provider-transport-started", 2),
                    ("provider-transport-aborted", 2),
                )
            ),
            {
                "schema": VERIFIER.PROVIDER_EGRESS_GUARD_SCHEMA_ID,
                "event": "provider-egress-guard-summary",
                "guarded_apis": guarded_apis,
                "guarded_api_invocation_count": 0,
            },
            *evidence,
            {
                "schema": VERIFIER.AUDIT_SCHEMA_ID,
                "event": "session-summary",
                "scenario": "capability-pack",
                "source_commit": "a" * 40,
                "transport": "operating-system-loopback-http",
                "host": "127.0.0.1",
                "state": "candidate-unregistered",
                "production_registration": False,
                "operations": list(VERIFIER.EXACT_OPERATIONS),
                "resources": list(VERIFIER.EXACT_RESOURCES),
                "suspensions": [],
                "provider_transport_calls": 2,
                "aborted_provider_calls": 1,
                "ledger_event_count": 4,
                "reported_error_count": 0,
                "private_state_root_mode": "0700",
                "guarded_api_invocation_count": 0,
            },
        ]
        capture = {
            "source": {"commit": "a" * 40},
            "fixture": {"host": "127.0.0.1", "port": 49152},
            "audit_lines": [json.dumps(event) for event in events],
        }
        return capture, successful, aborted, receipt

    def test_public_contract_closes_every_wider_claim(self) -> None:
        schema = json.loads(VERIFIER.PUBLIC_SCHEMA_PATH.read_text())
        properties = schema["properties"]
        self.assertEqual(
            properties["evidence_classification"]["const"],
            "local-http-transport-preflight",
        )
        source = properties["source"]["properties"]
        self.assertIs(source["working_tree_clean"]["const"], True)
        self.assertIs(source["complete_runtime_source_binding"]["const"], False)
        claims = properties["claims"]["properties"]
        self.assertEqual(claims["claude_code_capability"]["const"], "unscored")
        self.assertEqual(claims["model_capability"]["const"], "unscored")
        self.assertIs(claims["remote_host_acceptance"]["const"], False)
        for name in (
            "registration_performed",
            "activation_performed",
            "deployment_performed",
            "release_performed",
        ):
            self.assertIs(claims[name]["const"], False)
        execution = properties["execution"]["properties"]
        self.assertEqual(execution["provider_transport_calls"]["const"], 2)
        self.assertEqual(execution["aborted_provider_calls"]["const"], 1)
        self.assertEqual(execution["ledger_events"]["const"], 4)
        material_contracts = properties["verification"]["properties"]["source_materials"]
        material_paths = tuple(
            item["allOf"][1]["properties"]["path"]["const"]
            for item in material_contracts["prefixItems"]
        )
        self.assertEqual(material_contracts["minItems"], len(material_paths))
        self.assertEqual(material_contracts["maxItems"], len(material_paths))
        self.assertEqual(material_paths, VERIFIER.SOURCE_MATERIAL_PATHS)
        self.assertIn(
            "schemas/qual-206-exact-five-tool-schema-digests.v1.json",
            material_paths,
        )

    def test_path_free_projection_rejects_location_disclosure(self) -> None:
        with self.assertRaisesRegex(VERIFIER.VerificationError, "forbidden location"):
            VERIFIER.validate_path_free({"host": "redacted.invalid"})
        with self.assertRaisesRegex(VERIFIER.VerificationError, "not path-free"):
            VERIFIER.validate_path_free({"material": "/private/tmp/capture.json"})
        with self.assertRaisesRegex(VERIFIER.VerificationError, "not path-free"):
            VERIFIER.validate_path_free({"address": "127.0.0.1"})

    def test_private_schema_failure_does_not_reflect_instance_values(self) -> None:
        marker = "SYNTHETIC-PRIVATE-MARKER-QUAL-206"
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {"value": {"type": "string"}},
        }
        value = {"value": {"secret": marker}, f"unexpected-{marker}": True}
        with self.assertRaises(VERIFIER.VerificationError) as raised:
            VERIFIER.validate_with_schema(
                value,
                VERIFIER.Draft202012Validator(schema),
                "Private capture",
            )
        self.assertEqual(
            str(raised.exception),
            "Private capture failed its closed schema contract",
        )
        self.assertNotIn(marker, str(raised.exception))

    def test_private_capture_reader_rejects_non_private_and_hard_linked_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "capture.json"
            path.write_text("{}\n")
            path.chmod(0o600)
            self.assertEqual(
                VERIFIER.bounded_regular_file(path, 1024, "capture", owner_only=True),
                b"{}\n",
            )
            path.chmod(0o640)
            with self.assertRaisesRegex(VERIFIER.VerificationError, "owner-owned"):
                VERIFIER.bounded_regular_file(path, 1024, "capture", owner_only=True)
            path.chmod(0o600)
            link = root / "capture-link.json"
            os.link(path, link)
            with self.assertRaisesRegex(VERIFIER.VerificationError, "singly linked"):
                VERIFIER.bounded_regular_file(path, 1024, "capture", owner_only=True)

    def test_verifier_rejects_private_capture_copied_inside_ignored_repository(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="qual-206-private-capture-", dir=ROOT / "artifacts"
        ) as directory:
            root = Path(directory)
            root.chmod(0o700)
            path = root / "capture.json"
            path.write_text("{}\n")
            path.chmod(0o600)
            with self.assertRaisesRegex(VERIFIER.VerificationError, "outside the repository"):
                VERIFIER.verify_and_project(path, verify_current_source=False)

    def test_verifier_requires_owner_only_canonical_capture_parent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "capture.json"
            path.write_text("{}\n")
            path.chmod(0o600)
            root.chmod(0o755)
            try:
                with self.assertRaisesRegex(VERIFIER.VerificationError, "owner-owned 0700"):
                    VERIFIER.exact_private_capture_path(path)
            finally:
                root.chmod(0o700)

    def test_verifier_rejects_symbolic_capture_parent(self) -> None:
        with (
            tempfile.TemporaryDirectory() as target_directory,
            tempfile.TemporaryDirectory() as alias_directory,
        ):
            target = Path(target_directory)
            target.chmod(0o700)
            path = target / "capture.json"
            path.write_text("{}\n")
            path.chmod(0o600)
            alias = Path(alias_directory) / "capture-parent"
            alias.symlink_to(target, target_is_directory=True)
            with self.assertRaisesRegex(VERIFIER.VerificationError, "symbolic link"):
                VERIFIER.exact_private_capture_path(alias / "capture.json")

    def test_observation_identity_binds_all_projected_facts(self) -> None:
        projection = {
            "schema": "example",
            "claims": {"remote_host_acceptance": False},
            "verification": {"observation_sha256": None},
        }
        first = VERIFIER.observation_sha256(projection)
        projection["claims"]["remote_host_acceptance"] = True
        second = VERIFIER.observation_sha256(projection)
        self.assertNotEqual(first, second)
        self.assertRegex(first, r"^[0-9a-f]{64}$")

    def test_openapi_callable_contract_rejects_path_method_identity_and_schema_drift(
        self,
    ) -> None:
        openapi, tools = self.openapi_fixture()
        VERIFIER.validate_openapi_callable_contract(openapi, tools)
        mutations = (
            (
                "extra path",
                lambda value: value["paths"].__setitem__(
                    "/unexpected", {"post": {}}
                ),
                "exact closed path set",
            ),
            (
                "extra method",
                lambda value: value["paths"]["/data/query"].__setitem__(
                    "get", {}
                ),
                "exact closed members",
            ),
            (
                "operation identity",
                lambda value: value["paths"]["/data/query"]["post"].__setitem__(
                    "operationId", "unexpectedDataQuery"
                ),
                "operation identity",
            ),
            (
                "request schema reference",
                lambda value: value["paths"]["/data/query"]["post"][
                    "requestBody"
                ]["content"]["application/json"].__setitem__(
                    "schema", {"$ref": "#/components/schemas/CatalogueSearchRequest"}
                ),
                "schema reference",
            ),
            (
                "component schema",
                lambda value: value["components"]["schemas"].__setitem__(
                    "DataQueryResult", {"type": "object", "additionalProperties": True}
                ),
                "differ from MCP",
            ),
        )
        for label, mutate, failure in mutations:
            with self.subTest(label=label):
                tampered = deepcopy(openapi)
                mutate(tampered)
                with self.assertRaisesRegex(VERIFIER.VerificationError, failure):
                    VERIFIER.validate_openapi_callable_contract(tampered, tools)
        tampered_tools = deepcopy(tools)
        evidence_tool = next(
            tool for tool in tampered_tools if tool["name"] == "evidence.inspect"
        )
        evidence_tool["inputSchema"]["unexpected"] = True
        with self.assertRaisesRegex(VERIFIER.VerificationError, "differ from MCP"):
            VERIFIER.validate_openapi_callable_contract(openapi, tampered_tools)

    def test_cancellation_replay_rejects_completed_or_ledger_evidence_for_aborted_key(
        self,
    ) -> None:
        events, successful, aborted, receipt = self.idempotency_evidence_fixture()
        VERIFIER.validate_idempotency_evidence(events, successful, aborted, receipt)

        completed_mutations = (
            ("reconciliation_status", "completed"),
            ("completed_evidence_created", True),
            (
                "resolution_id",
                "gis-ai-go:evidence-reconciliation-resolution:sha256:"
                f"{'7' * 64}",
            ),
            ("receipt_id", f"gis-ai-go:evidence-receipt:sha256:{'7' * 64}"),
            ("record_id", f"gis-ai-go:public-evidence-record:sha256:{'7' * 64}"),
            (
                "ledger_event_id",
                f"gis-ai-go:evidence-ledger-event:sha256:{'7' * 64}",
            ),
            ("ledger_event_sequence", 5),
        )
        for member, value in completed_mutations:
            with self.subTest(aborted_completion_member=member):
                tampered = deepcopy(events)
                tampered[1][member] = value
                with self.assertRaisesRegex(
                    VERIFIER.VerificationError, "aborted.*acquired"
                ):
                    VERIFIER.validate_idempotency_evidence(
                        tampered, successful, aborted, receipt
                    )

        swapped = deepcopy(events)
        swapped[1]["idempotency_key_sha256"] = events[0]["idempotency_key_sha256"]
        with self.assertRaisesRegex(VERIFIER.VerificationError, "captured requests"):
            VERIFIER.validate_idempotency_evidence(swapped, successful, aborted, receipt)

    def test_audit_requires_canonical_ordered_egress_guard_contracts(self) -> None:
        capture, successful, aborted, receipt = self.audit_capture_fixture()
        VERIFIER.validate_audit(capture, successful, aborted, receipt)
        mutations = (
            (0, "schema", "wrong.guard.v1"),
            (0, "guarded_apis", list(reversed(VERIFIER.EXACT_GUARDED_APIS))),
            (1, "transport", "https"),
            (1, "state", "active"),
            (1, "production_registration", True),
            (5, "schema", "wrong.guard.v1"),
            (5, "guarded_apis", list(reversed(VERIFIER.EXACT_GUARDED_APIS))),
            (8, "schema", "wrong.audit.v1"),
        )
        for event_index, member, replacement in mutations:
            with self.subTest(event_index=event_index, member=member):
                tampered = deepcopy(capture)
                event = json.loads(tampered["audit_lines"][event_index])
                event[member] = replacement
                tampered["audit_lines"][event_index] = json.dumps(event)
                with self.assertRaises(VERIFIER.VerificationError):
                    VERIFIER.validate_audit(tampered, successful, aborted, receipt)

    def test_public_projection_writer_completes_short_writes_and_reads_back(self) -> None:
        projection = {
            "schema": "test.public.v1",
            "padding": "x" * 4096,
            "verification": {"observation_sha256": "0" * 64},
        }
        real_write = VERIFIER.os.write

        def short_write(descriptor: int, raw: bytes) -> int:
            return real_write(descriptor, raw[: max(1, len(raw) // 3)])

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory).resolve() / "projection.json"
            with mock.patch.object(VERIFIER.os, "write", side_effect=short_write):
                VERIFIER.write_new_public_projection(output, projection)
            expected = (json.dumps(projection, indent=2, ensure_ascii=False) + "\n").encode()
            self.assertEqual(output.read_bytes(), expected)

    def test_public_projection_writer_rejects_corrupt_readback(self) -> None:
        projection = {"schema": "test.public.v1", "value": "synthetic"}
        real_read = VERIFIER.os.read
        corrupted = False

        def corrupt_read(descriptor: int, size: int) -> bytes:
            nonlocal corrupted
            chunk = real_read(descriptor, size)
            if chunk and not corrupted:
                corrupted = True
                return bytes((chunk[0] ^ 1,)) + chunk[1:]
            return chunk

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory).resolve() / "projection.json"
            with (
                mock.patch.object(VERIFIER.os, "read", side_effect=corrupt_read),
                self.assertRaisesRegex(VERIFIER.VerificationError, "readback"),
            ):
                VERIFIER.write_new_public_projection(output, projection)
            self.assertFalse(output.exists())
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_public_projection_writer_rejects_parent_rename(self) -> None:
        projection = {"schema": "test.public.v1", "value": "synthetic"}
        real_fsync = VERIFIER.os.fsync

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            parent = root / "publication"
            renamed_parent = root / "renamed-publication"
            parent.mkdir()
            output = parent / "projection.json"

            def rename_parent(descriptor: int) -> None:
                real_fsync(descriptor)
                parent.rename(renamed_parent)

            with (
                mock.patch.object(VERIFIER.os, "fsync", side_effect=rename_parent),
                self.assertRaisesRegex(VERIFIER.VerificationError, "finalisation|parent"),
            ):
                VERIFIER.write_new_public_projection(output, projection)
            self.assertFalse(output.exists())
            self.assertEqual(list(renamed_parent.iterdir()), [])

    def test_public_projection_writer_removes_final_name_when_directory_sync_fails(
        self,
    ) -> None:
        projection = {"schema": "test.public.v1", "value": "synthetic"}
        real_fsync = VERIFIER.os.fsync
        calls = 0

        def fail_directory_sync(descriptor: int) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("synthetic directory sync failure")
            real_fsync(descriptor)

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory).resolve() / "projection.json"
            with (
                mock.patch.object(VERIFIER.os, "fsync", side_effect=fail_directory_sync),
                self.assertRaisesRegex(VERIFIER.VerificationError, "finalisation"),
            ):
                VERIFIER.write_new_public_projection(output, projection)
            self.assertFalse(output.exists())
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_git_invocation_uses_fixed_executable_and_sanitised_environment(self) -> None:
        completed = subprocess_result = mock.Mock(stdout=b"value\n", stderr=b"")
        with (
            mock.patch.dict(os.environ, {"GIT_DIR": "/attacker", "PATH": str(ROOT)}),
            mock.patch.object(VERIFIER.subprocess, "run", return_value=completed) as run,
        ):
            self.assertEqual(VERIFIER.git_text("rev-parse", "HEAD"), "value")
        command = run.call_args.args[0]
        environment = run.call_args.kwargs["env"]
        self.assertEqual(command[0], "/usr/bin/git")
        self.assertEqual(command[1], "--no-replace-objects")
        self.assertNotIn("GIT_DIR", environment)
        self.assertEqual(environment["PATH"], "/usr/bin:/bin")
        self.assertIs(subprocess_result, completed)

    def test_clean_source_rejects_hidden_index_state_and_tree_blob_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory).resolve()

            def git(*arguments: str) -> str:
                completed = subprocess.run(
                    ["/usr/bin/git", *arguments],
                    cwd=repository,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                return completed.stdout.strip()

            git("init", "--quiet")
            material = repository / "material.txt"
            material.write_text("recorded\n", encoding="utf-8")
            git("add", "material.txt")
            git(
                "-c",
                "user.name=QUAL-206 test",
                "-c",
                "user.email=qual-206@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "test fixture",
            )
            source = {
                "commit": git("rev-parse", "HEAD"),
                "tree": git("rev-parse", "HEAD^{tree}"),
                "working_tree_clean": True,
            }
            git("update-index", "--assume-unchanged", "material.txt")
            material.write_text("modified but hidden\n", encoding="utf-8")
            current = [
                {
                    "path": "material.txt",
                    "sha256": VERIFIER.sha256(material.read_bytes()),
                }
            ]
            with mock.patch.object(VERIFIER, "ROOT", repository):
                with self.assertRaisesRegex(VERIFIER.VerificationError, "index state"):
                    VERIFIER.verify_clean_current_source(source)
                with self.assertRaisesRegex(VERIFIER.VerificationError, "tree blob"):
                    VERIFIER.verify_named_materials_match_tree(source, current)

    def test_git_source_resolution_ignores_replacement_refs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory).resolve()

            def git(*arguments: str) -> str:
                completed = subprocess.run(
                    ["/usr/bin/git", *arguments],
                    cwd=repository,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                return completed.stdout.strip()

            git("init", "--quiet")
            material = repository / "material.txt"
            material.write_text("recorded\n", encoding="utf-8")
            git("add", "material.txt")
            git(
                "-c",
                "user.name=QUAL-206 test",
                "-c",
                "user.email=qual-206@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "recorded fixture",
            )
            recorded_commit = git("rev-parse", "HEAD")
            recorded_tree = git("rev-parse", "HEAD^{tree}")
            material.write_text("replacement\n", encoding="utf-8")
            git("add", "material.txt")
            git(
                "-c",
                "user.name=QUAL-206 test",
                "-c",
                "user.email=qual-206@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "replacement fixture",
            )
            replacement_commit = git("rev-parse", "HEAD")
            git("checkout", "--quiet", "--detach", recorded_commit)
            git("replace", recorded_commit, replacement_commit)
            with mock.patch.object(VERIFIER, "ROOT", repository):
                self.assertEqual(
                    VERIFIER.git_text("rev-parse", "HEAD^{tree}"),
                    recorded_tree,
                )

    def test_canonical_schema_validation_uses_manifest_without_node_process(
        self,
    ) -> None:
        _, tools = self.openapi_fixture()
        manifest = self.schema_digest_manifest_fixture(tools)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema-digests.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            with (
                mock.patch.object(
                    VERIFIER,
                    "CANONICAL_SCHEMA_DIGEST_MANIFEST_PATH",
                    path,
                ),
                mock.patch.dict(os.environ, {"PATH": ""}),
                mock.patch.object(
                    VERIFIER.subprocess,
                    "run",
                    side_effect=AssertionError("unexpected child process"),
                ) as run,
            ):
                VERIFIER.validate_canonical_tool_schemas(tools)
            run.assert_not_called()

    def test_canonical_schema_validation_rejects_input_and_output_drift(self) -> None:
        _, tools = self.openapi_fixture()
        manifest = self.schema_digest_manifest_fixture(tools)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema-digests.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            for member in ("inputSchema", "outputSchema"):
                changed = deepcopy(tools)
                changed[0][member]["description"] = f"changed {member}"
                with (
                    self.subTest(member=member),
                    mock.patch.object(
                        VERIFIER,
                        "CANONICAL_SCHEMA_DIGEST_MANIFEST_PATH",
                        path,
                    ),
                    self.assertRaisesRegex(
                        VERIFIER.VerificationError,
                        "differ from the canonical exact-five schemas",
                    ),
                ):
                    VERIFIER.validate_canonical_tool_schemas(changed)

    def test_canonical_schema_manifest_is_closed_and_ordered(self) -> None:
        _, tools = self.openapi_fixture()
        original = self.schema_digest_manifest_fixture(tools)
        mutations = {
            "extra member": lambda value: value.__setitem__("unexpected", True),
            "wrong domain": lambda value: value.__setitem__("domain", "wrong"),
            "wrong order": lambda value: value["operations"].reverse(),
            "invalid digest": lambda value: value["operations"][0].__setitem__(
                "input_schema_sha256",
                "A" * 64,
            ),
            "missing operation": lambda value: value["operations"].pop(),
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema-digests.json"
            for label, mutate in mutations.items():
                changed = deepcopy(original)
                mutate(changed)
                path.write_text(json.dumps(changed), encoding="utf-8")
                with (
                    self.subTest(mutation=label),
                    mock.patch.object(
                        VERIFIER,
                        "CANONICAL_SCHEMA_DIGEST_MANIFEST_PATH",
                        path,
                    ),
                    self.assertRaises(VERIFIER.VerificationError),
                ):
                    VERIFIER.validate_canonical_tool_schemas(tools)

    def test_canonical_schema_digest_ignores_object_member_order(self) -> None:
        _, tools = self.openapi_fixture()
        manifest = self.schema_digest_manifest_fixture(tools)
        reordered = deepcopy(tools)
        schema = reordered[0]["inputSchema"]
        reordered[0]["inputSchema"] = dict(reversed(tuple(schema.items())))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema-digests.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            with mock.patch.object(
                VERIFIER,
                "CANONICAL_SCHEMA_DIGEST_MANIFEST_PATH",
                path,
            ):
                VERIFIER.validate_canonical_tool_schemas(reordered)

    def test_source_material_binding_rejects_execution_mutation(self) -> None:
        captured = [
            {
                "path": path,
                "sha256_before_execution": "a" * 64,
                "sha256_after_execution": "a" * 64,
            }
            for path in VERIFIER.SOURCE_MATERIAL_PATHS
        ]
        captured[10]["sha256_after_execution"] = "b" * 64
        current = [
            {"path": path, "sha256": "a" * 64}
            for path in VERIFIER.SOURCE_MATERIAL_PATHS
        ]
        with self.assertRaisesRegex(VERIFIER.VerificationError, "observed execution"):
            VERIFIER.validate_captured_source_materials(captured, current)

    def test_source_material_binding_rejects_change_before_replay(self) -> None:
        captured = [
            {
                "path": path,
                "sha256_before_execution": "a" * 64,
                "sha256_after_execution": "a" * 64,
            }
            for path in VERIFIER.SOURCE_MATERIAL_PATHS
        ]
        current = [
            {"path": path, "sha256": "a" * 64}
            for path in VERIFIER.SOURCE_MATERIAL_PATHS
        ]
        current[10]["sha256"] = "b" * 64
        with self.assertRaisesRegex(VERIFIER.VerificationError, "execution and replay"):
            VERIFIER.validate_captured_source_materials(captured, current)


if __name__ == "__main__":
    unittest.main()
