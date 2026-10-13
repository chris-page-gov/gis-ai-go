from __future__ import annotations

import contextlib
import hashlib
import io
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import node_runtime_advisory as node  # noqa: E402
import run_gateway_image_assurance as assurance  # noqa: E402
import scan_gateway_image as scan  # noqa: E402
from gateway_image import NODE_ADVISORY_STAGE_EXIT_CODES  # noqa: E402
from tests.contract.test_node_runtime_advisory import (  # noqa: E402
    ASSESSED_AT,
    DATABASE_BUILT,
    DATABASE_CAPTURED,
    database_source,
    grype_cyclonedx_report,
    grype_json_report,
    node_fixture,
)


class NodeAdvisoryDiagnosticsTests(unittest.TestCase):
    @contextlib.contextmanager
    def fixture(self, output: Path):
        """Use real Node assessment and files, replacing network/container seams."""
        sbom, receipt = node_fixture()
        archive_bytes = b"synthetic database archive"
        archive_sha256 = hashlib.sha256(archive_bytes).hexdigest()
        source = {
            "schema_version": "v6.1.9", "built": DATABASE_BUILT, "valid": True,
            "source_url": database_source(archive_sha256),
            "source_sha256": archive_sha256,
        }
        behaviour = {
            "actual_ids": (), "actual_severity": "High",
            "affected_ids": tuple(sorted(node.NODE_CALIBRATION_HIGH_IDS)),
            "fixed_ids": (), "provider_captured": DATABASE_CAPTURED,
            "mutate_database": False, "disagree_reports": False,
        }

        def download(_status, destination):
            destination.write_bytes(archive_bytes)

        def import_database(cache, _archive, *, source):
            (cache / "6").mkdir()
            (cache / "6" / "import.json").write_bytes(b"{}")
            (cache / "6" / "vulnerability.db").write_bytes(b"synthetic database")
            return {**source, "load_mode": "manual-import"}

        def scan_raw(cache, input_document, *, output_format):
            version = input_document["components"][0]["version"]
            role = next(role for role, (expected, _calibration) in node.NODE_ROLES.items()
                        if expected == version)
            identifiers = behaviour[f"{role}_ids"]
            if behaviour["mutate_database"]:
                (cache / "6" / "vulnerability.db").write_bytes(b"mutated database")
            if output_format == "cyclonedx-json":
                return grype_cyclonedx_report(
                    input_document,
                    vulnerability_ids=() if behaviour["disagree_reports"] else identifiers,
                )
            report = grype_json_report(
                input_document, database_sha256=archive_sha256,
                vulnerability_ids=identifiers, manual_import=True,
            )
            report["descriptor"]["db"]["providers"]["nvd"]["captured"] = (
                behaviour["provider_captured"]
            )
            if role == "actual":
                for match in report["matches"]:
                    match["vulnerability"]["severity"] = behaviour["actual_severity"]
            return report

        seams = {
            "acquire_grype_image": mock.Mock(),
            "update_database": mock.Mock(return_value=source),
            "download_database_archive": mock.Mock(side_effect=download),
            "import_database": mock.Mock(side_effect=import_database),
            "database_inventory": mock.Mock(wraps=node.database_inventory),
            "_scan_raw": mock.Mock(side_effect=scan_raw),
            "normalise_json_report": mock.Mock(wraps=node.normalise_json_report),
            "extract_node_identity": mock.Mock(wraps=node.extract_node_identity),
        }
        with contextlib.ExitStack() as stack:
            clock = stack.enter_context(mock.patch.object(node, "datetime", wraps=datetime))
            clock.now.return_value = datetime.fromisoformat(ASSESSED_AT.replace("Z", "+00:00"))
            for name, seam in seams.items():
                stack.enter_context(mock.patch.object(node, name, seam))
            yield {"sbom": sbom, "receipt": receipt, "output": output}, seams, behaviour, clock

    def assert_detached(self, error):
        self.assertIsNone(error.__cause__)
        self.assertIsNone(error.__context__)

    def assert_no_role_files(self, root):
        for role_files in node.NODE_ROLE_FILES.values():
            for name in role_files.values():
                self.assertFalse((root / name).exists(), name)

    def test_step_does_not_stringify_or_chain_underlying_failure(self):
        class UnrenderableFailure(Exception):
            def __str__(self):
                raise AssertionError("untrusted exception must not be rendered")

        for stage in NODE_ADVISORY_STAGE_EXIT_CODES:
            with self.subTest(stage=stage), self.assertRaises(node.NodeAdvisoryFailure) as raised:
                node._node_step(stage, mock.Mock(side_effect=UnrenderableFailure()))
            self.assertEqual(raised.exception.stage, stage)
            self.assert_detached(raised.exception)

    def test_step_preserves_arguments_result_and_control_flow(self):
        result = object()
        operation = mock.Mock(return_value=result)
        self.assertIs(node._node_step("node-db-update", operation, 1, named=2), result)
        operation.assert_called_once_with(1, named=2)
        for original in (node.NodeAdvisoryFailure("node-runtime-policy"),
                         KeyboardInterrupt(), SystemExit(3)):
            with self.subTest(error=type(original).__name__), self.assertRaises(type(original)) as raised:
                node._node_step("node-db-update", mock.Mock(side_effect=original))
            self.assertIs(raised.exception, original)

    def test_unknown_stage_is_rejected_before_operation_and_not_reflected(self):
        operation = mock.Mock()
        marker = "unreviewed-stage-text"
        with self.assertRaises(ValueError) as raised:
            node._node_step(marker, operation)
        operation.assert_not_called()
        self.assertNotIn(marker, str(raised.exception))

    def test_orchestrator_stages_errors_and_stops_later_work(self):
        cases = (
            ("node-scanner-acquisition", "acquire_grype_image", "update_database"),
            ("node-db-update", "update_database", "download_database_archive"),
            ("node-db-download", "download_database_archive", "import_database"),
            ("node-db-import", "import_database", "database_inventory"),
            ("node-db-inventory", "database_inventory", "_scan_raw"),
            ("node-scan-execution", "_scan_raw", "normalise_json_report"),
            ("node-identity-binding", "extract_node_identity", "_scan_raw"),
        )
        for stage, failed, untouched in cases:
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                with self.fixture(root) as (arguments, seams, _behaviour, _clock):
                    seams[failed].side_effect = OSError("synthetic hidden detail")
                    with self.assertRaises(node.NodeAdvisoryFailure) as raised:
                        node.generate_node_advisory(**arguments)
                    self.assertEqual(raised.exception.stage, stage)
                    self.assert_detached(raised.exception)
                    seams[untouched].assert_not_called()
                    self.assert_no_role_files(root)

    def test_invalid_json_report_is_classified_without_persisting_reports(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.fixture(root) as (arguments, seams, _behaviour, _clock):
                seams["_scan_raw"].return_value = {}
                seams["_scan_raw"].side_effect = None
                with self.assertRaises(node.NodeAdvisoryFailure) as raised:
                    node.generate_node_advisory(**arguments)
                self.assertEqual(raised.exception.stage, "node-report-validation")
                self.assert_no_role_files(root)

    def test_disagreeing_json_and_cyclonedx_reports_still_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.fixture(root) as (arguments, _seams, behaviour, _clock):
                behaviour["disagree_reports"] = True
                with self.assertRaises(node.NodeAdvisoryFailure) as raised:
                    node.generate_node_advisory(**arguments)
                self.assertEqual(raised.exception.stage, "node-report-validation")
                self.assert_no_role_files(root)

    def test_missing_positive_or_ineffective_fixed_control_still_fails_calibration(self):
        for changed_role, identifiers in (
            ("affected_ids", ()), ("fixed_ids", tuple(sorted(node.NODE_CALIBRATION_HIGH_IDS)))
        ):
            with self.subTest(role=changed_role), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                with self.fixture(root) as (arguments, _seams, behaviour, _clock):
                    behaviour[changed_role] = identifiers
                    with self.assertRaises(node.NodeAdvisoryFailure) as raised:
                        node.generate_node_advisory(**arguments)
                    self.assertEqual(raised.exception.stage, "node-calibration")
                    self.assert_no_role_files(root)

    def test_real_high_and_critical_actual_runtime_findings_still_fail_policy(self):
        for severity in ("High", "Critical"):
            with self.subTest(severity=severity), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                with self.fixture(root) as (arguments, _seams, behaviour, _clock):
                    behaviour["actual_ids"] = ("CVE-2026-56846",)
                    behaviour["actual_severity"] = severity
                    with self.assertRaises(node.NodeAdvisoryFailure) as raised:
                        node.generate_node_advisory(**arguments)
                    self.assertEqual(raised.exception.stage, "node-runtime-policy")
                    self.assert_detached(raised.exception)
                    self.assert_no_role_files(root)

    def test_stale_database_still_fails_before_writing_role_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.fixture(root) as (arguments, _seams, _behaviour, clock):
                clock.now.return_value = datetime(2026, 8, 28, tzinfo=UTC)
                with self.assertRaises(node.NodeAdvisoryFailure) as raised:
                    node.generate_node_advisory(**arguments)
                self.assertEqual(raised.exception.stage, "node-db-freshness")
                self.assert_no_role_files(root)

    def test_stale_provider_in_current_database_still_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.fixture(root) as (arguments, _seams, behaviour, _clock):
                behaviour["provider_captured"] = "2026-08-20T00:00:00Z"
                with self.assertRaises(node.NodeAdvisoryFailure) as raised:
                    node.generate_node_advisory(**arguments)
                self.assertEqual(raised.exception.stage, "node-provider-freshness")
                self.assert_no_role_files(root)

    def test_changed_replay_identity_prevents_assessment(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.fixture(root) as (arguments, seams, _behaviour, _clock):
                original = seams["import_database"].side_effect

                def changed(*args, **kwargs):
                    return {**original(*args, **kwargs), "built": "2026-08-22T06:15:27Z"}

                seams["import_database"].side_effect = changed
                with self.assertRaises(node.NodeAdvisoryFailure) as raised:
                    node.generate_node_advisory(**arguments)
                self.assertEqual(raised.exception.stage, "node-db-replay-binding")
                seams["_scan_raw"].assert_not_called()
                self.assert_no_role_files(root)

    def test_real_replay_file_mutation_prevents_evidence_persistence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.fixture(root) as (arguments, _seams, behaviour, _clock):
                behaviour["mutate_database"] = True
                with self.assertRaises(node.NodeAdvisoryFailure) as raised:
                    node.generate_node_advisory(**arguments)
                self.assertEqual(raised.exception.stage, "node-db-replay-binding")
                self.assert_no_role_files(root)

    def test_role_evidence_write_failure_is_classified(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.fixture(root) as (arguments, _seams, _behaviour, _clock):
                original = Path.write_bytes

                def write(path, content):
                    if path.name == node.NODE_ROLE_FILES["actual"]["input"]:
                        raise OSError("synthetic write failure")
                    return original(path, content)

                with (mock.patch.object(Path, "write_bytes", write),
                      self.assertRaises(node.NodeAdvisoryFailure) as raised):
                    node.generate_node_advisory(**arguments)
                self.assertEqual(raised.exception.stage, "node-evidence-write")
                self.assert_detached(raised.exception)

    def test_successful_real_assessment_preserves_evidence_and_offline_contract(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.fixture(root) as (arguments, seams, _behaviour, _clock):
                evidence, findings = node.generate_node_advisory(**arguments)
                self.assertIs(evidence["calibration"]["passed"], True)
                self.assertIs(evidence["assessment"]["passed"], True)
                self.assertEqual(findings, [])
                self.assertEqual(evidence["database"]["age_seconds"], 86_400)
                self.assertEqual(evidence["replay"]["network"], "none")
                self.assertEqual(evidence["replay"]["pull"], "never")
                self.assertIs(evidence["replay"]["database_hash_validation"], True)
                self.assertEqual(seams["database_inventory"].call_count, 2)
                self.assertEqual(seams["_scan_raw"].call_count, 6)
                for files in node.NODE_ROLE_FILES.values():
                    for name in files.values():
                        self.assertTrue((root / name).is_file(), name)

    def test_outer_scan_stage_preserves_node_failure_identity(self):
        for stage in NODE_ADVISORY_STAGE_EXIT_CODES:
            original = node.NodeAdvisoryFailure(stage)
            with self.subTest(stage=stage), self.assertRaises(node.NodeAdvisoryFailure) as raised:
                with scan._scan_stage("node-advisory"):
                    raise original
            self.assertIs(raised.exception, original)

    def test_scanner_cli_silently_maps_node_failures_without_exception_chain(self):
        for stage, code in NODE_ADVISORY_STAGE_EXIT_CODES.items():
            with self.subTest(stage=stage):
                output = io.StringIO()
                with (mock.patch.object(scan, "main", side_effect=node.NodeAdvisoryFailure(stage)),
                      contextlib.redirect_stdout(output), contextlib.redirect_stderr(output),
                      self.assertRaises(SystemExit) as raised):
                    scan.cli()
                self.assertEqual(raised.exception.code, code)
                self.assertEqual(output.getvalue(), "")
                self.assert_detached(raised.exception)

    def test_real_hostile_subprocesses_expose_only_reviewed_node_stage(self):
        private_path = "/" + "home/runner/work/private"
        payload = f"Bearer SYNTHETIC-NODE-SECRET {private_path}".encode()
        cases = [("vulnerability-scan", code, stage)
                 for stage, code in NODE_ADVISORY_STAGE_EXIT_CODES.items()]
        cases += [("container-acceptance", code, None)
                  for code in NODE_ADVISORY_STAGE_EXIT_CODES.values()]
        cases += [("vulnerability-scan", 112, None)]
        for phase, code, stage in cases:
            with self.subTest(phase=phase, code=code):
                command = (f"import os,sys;os.write(1,{payload!r});"
                           f"os.write(2,{payload!r});sys.exit({code})")
                output = io.StringIO()
                with (contextlib.redirect_stdout(output), contextlib.redirect_stderr(output),
                      self.assertRaises(ValueError) as raised):
                    assurance.run_checked(phase, [sys.executable, "-c", command])
                rendered = output.getvalue() + str(raised.exception)
                self.assertNotIn("Bearer", rendered)
                self.assertNotIn("SYNTHETIC-NODE-SECRET", rendered)
                self.assertNotIn(private_path, rendered)
                self.assertNotIn(hashlib.sha256(payload).hexdigest(), rendered)
                self.assert_detached(raised.exception)
                if stage is None:
                    self.assertNotIn("failure_stage=", rendered)
                    self.assertIn("exited unsuccessfully", rendered)
                else:
                    self.assertIn(f"failure_stage={stage}", rendered)
                    self.assertEqual(rendered.count("failure_stage="), 1)


if __name__ == "__main__":
    unittest.main()
