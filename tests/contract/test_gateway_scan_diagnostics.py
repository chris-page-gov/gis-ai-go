from __future__ import annotations

import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import run_gateway_image_assurance as assurance  # noqa: E402
import scan_gateway_image as scan  # noqa: E402
from gateway_image import VULNERABILITY_SCAN_STAGE_EXIT_CODES  # noqa: E402
from tests.contract.test_gateway_image_contract import coverage_fixture  # noqa: E402


class GatewayScanDiagnosticsTests(unittest.TestCase):
    @contextlib.contextmanager
    def fixture(self, root: Path):
        """Exercise orchestration with real files, coverage and finding policy.

        Acquisition and image binding have their own contract tests. This fixture
        supplies those seams and a small schema for synthetic evidence; privacy,
        serialisation, schema validation and policy execution remain real.
        """
        report, donor_report, sbom, receipt, donor = coverage_fixture()
        receipt["source"] = {"clean": True, "revision": "a" * 40}
        receipt["image"]["manifest_digest"] = "sha256:" + "b" * 64
        paths = {
            "archive": root / "gateway-image.oci.tar",
            "sbom": root / "gateway-image.sbom.cdx.json",
            "receipt_path": root / "image-receipt.json",
            "output": root / "gateway-image.vulnerability-scan.json",
        }
        paths["archive"].write_bytes(b"synthetic image")
        paths["sbom"].write_text(json.dumps(sbom), encoding="utf-8")
        paths["receipt_path"].write_text(json.dumps(receipt), encoding="utf-8")
        schema = root / "synthetic-scan.schema.json"
        schema.write_text(
            json.dumps({"type": "object", "required": ["passed"],
                        "properties": {"passed": {"type": "boolean"}}}),
            encoding="utf-8",
        )

        def acquire(destination: Path):
            destination.write_bytes(b"synthetic donor")
            return {**donor, "file": destination.name}

        def package(_cache: Path, destination: Path):
            destination.write_bytes(b"synthetic database")
            return []

        seams = {
            "bind_gateway_archive": mock.Mock(return_value={}),
            "_acquire_scan_images": mock.Mock(side_effect=acquire),
            "_download_trivy_database": mock.Mock(return_value=root),
            "package_database": mock.Mock(side_effect=package),
            "inspect_database_archive": mock.Mock(return_value=[]),
            "_docker_scan": mock.Mock(side_effect=[report, donor_report]),
            "cache_inventory": mock.Mock(return_value=[]),
            "project_coverage": mock.Mock(wraps=scan.project_coverage),
            "generate_node_advisory": mock.Mock(return_value=({}, [])),
            "project_all_findings": mock.Mock(wraps=scan.project_all_findings),
            "evaluate_policy": mock.Mock(wraps=scan.evaluate_policy),
        }
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.object(scan, "SCAN_SCHEMA", schema))
            for name, replacement in seams.items():
                stack.enter_context(mock.patch.object(scan, name, replacement))
            yield paths, seams, report, schema

    def assert_detached(self, error: BaseException) -> None:
        self.assertIsNone(error.__cause__)
        self.assertIsNone(error.__context__)

    def test_stage_failures_do_not_stringify_or_chain_underlying_exceptions(self):
        class UnrenderableFailure(Exception):
            def __str__(self):
                raise AssertionError("untrusted exception must not be rendered")

        for stage in VULNERABILITY_SCAN_STAGE_EXIT_CODES:
            with self.subTest(stage=stage), self.assertRaises(scan.ScanStageFailure) as raised:
                with scan._scan_stage(stage):
                    raise UnrenderableFailure()
            self.assertEqual(raised.exception.stage, stage)
            self.assert_detached(raised.exception)

    def test_stage_identity_cannot_be_supplied_as_arbitrary_diagnostic_text(self):
        marker = "unreviewed-diagnostic-stage"
        with self.assertRaises(ValueError) as raised:
            with scan._scan_stage(marker):
                self.fail("unrecognised stage entered")
        self.assertNotIn(marker, str(raised.exception))

    def test_nested_stage_identity_and_control_flow_are_preserved(self):
        failures = [scan.ScanStageFailure("trivy-gateway-assessment"),
                    KeyboardInterrupt(), SystemExit(12)]
        for failure in failures:
            with self.subTest(error=type(failure).__name__), self.assertRaises(type(failure)) as raised:
                with scan._scan_stage("trivy-db-retention"):
                    raise failure
            self.assertIs(raised.exception, failure)
        with self.assertRaises(scan.ScanStageFailure) as raised:
            with scan._scan_stage("trivy-db-retention"):
                with scan._scan_stage("trivy-gateway-assessment"):
                    raise ValueError("synthetic private detail")
        self.assertEqual(raised.exception.stage, "trivy-gateway-assessment")
        self.assert_detached(raised.exception)

    def test_orchestrator_classifies_failed_seams_and_stops_later_work(self):
        cases = (
            ("input-binding", "bind_gateway_archive", "_acquire_scan_images"),
            ("scanner-images", "_acquire_scan_images", "_download_trivy_database"),
            ("trivy-db-retention", "package_database", "_docker_scan"),
            ("trivy-gateway-assessment", "_docker_scan", "cache_inventory"),
            ("trivy-donor-assessment", "_docker_scan", "cache_inventory"),
            ("trivy-evidence-binding", "project_coverage", "generate_node_advisory"),
            ("node-advisory", "generate_node_advisory", "project_all_findings"),
        )
        for stage, failing, untouched in cases:
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as temporary:
                with self.fixture(Path(temporary)) as (paths, seams, report, _schema):
                    error = OSError("synthetic hidden failure")
                    seams[failing].side_effect = (
                        [report, error] if stage == "trivy-donor-assessment" else error
                    )
                    with self.assertRaises(scan.ScanStageFailure) as raised:
                        scan.generate_scan_evidence(**paths)
                    self.assertEqual(raised.exception.stage, stage)
                    self.assert_detached(raised.exception)
                    seams[untouched].assert_not_called()
                    if failing == "_docker_scan":
                        self.assertEqual(seams[failing].call_count,
                                         2 if stage == "trivy-donor-assessment" else 1)
                    self.assertFalse(paths["output"].exists())

    def test_missing_input_is_classified_before_acquisition(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.fixture(Path(temporary)) as (paths, seams, _report, _schema):
                paths["receipt_path"].unlink()
                with self.assertRaises(scan.ScanStageFailure) as raised:
                    scan.generate_scan_evidence(**paths)
                self.assertEqual(raised.exception.stage, "input-binding")
                seams["_acquire_scan_images"].assert_not_called()

    def test_retained_database_mismatch_prevents_scanning(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.fixture(Path(temporary)) as (paths, seams, _report, _schema):
                seams["inspect_database_archive"].return_value = [{"bytes": 1}]
                with self.assertRaises(scan.ScanStageFailure) as raised:
                    scan.generate_scan_evidence(**paths)
                self.assertEqual(raised.exception.stage, "trivy-db-retention")
                seams["_docker_scan"].assert_not_called()

    def test_replay_database_mutation_blocks_report_persistence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.fixture(root) as (paths, seams, _report, _schema):
                seams["cache_inventory"].return_value = [{"bytes": 1}]
                with self.assertRaises(scan.ScanStageFailure) as raised:
                    scan.generate_scan_evidence(**paths)
                self.assertEqual(raised.exception.stage, "trivy-evidence-binding")
                seams["generate_node_advisory"].assert_not_called()
                self.assertFalse((root / scan.REPORT_NAME).exists())
                self.assertFalse(paths["output"].exists())

    def test_schema_failure_is_classified_before_evidence_is_written(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.fixture(root) as (paths, _seams, _report, schema):
                schema.write_text('{"type":"object","required":["absent-field"]}',
                                  encoding="utf-8")
                with self.assertRaises(scan.ScanStageFailure) as raised:
                    scan.generate_scan_evidence(**paths)
                self.assertEqual(raised.exception.stage, "final-evidence-validation")
                self.assert_detached(raised.exception)
                self.assertFalse((root / scan.REPORT_NAME).exists())
                self.assertFalse(paths["output"].exists())

    def test_fixable_high_and_critical_findings_still_fail_policy(self):
        for severity in ("HIGH", "CRITICAL"):
            with self.subTest(severity=severity), tempfile.TemporaryDirectory() as temporary:
                with self.fixture(Path(temporary)) as (paths, seams, report, _schema):
                    report["Results"][0]["Vulnerabilities"] = [{
                        "VulnerabilityID": "CVE-2026-12345", "PkgName": "glibc",
                        "InstalledVersion": "2.39-1.el10", "FixedVersion": "2.39-2.el10",
                        "Severity": severity,
                    }]
                    with self.assertRaises(scan.ScanStageFailure) as raised:
                        scan.generate_scan_evidence(**paths)
                    self.assertEqual(raised.exception.stage, "vulnerability-policy")
                    self.assert_detached(raised.exception)
                    seams["evaluate_policy"].assert_called_once()
                    evidence = json.loads(paths["output"].read_text(encoding="utf-8"))
                    self.assertIs(evidence["passed"], False)
                    self.assertEqual(len(evidence["fixable_findings"]), 1)
                    self.assertEqual(evidence["fixable_findings"][0]["severity"], severity)

    def test_success_retains_offline_arguments_and_passed_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.fixture(Path(temporary)) as (paths, seams, _report, _schema):
                evidence = scan.generate_scan_evidence(**paths)
                self.assertIs(evidence["passed"], True)
                self.assertEqual(json.loads(paths["output"].read_text()), evidence)
                self.assertEqual(seams["_docker_scan"].call_count, 2)
                for invocation in seams["_docker_scan"].call_args_list:
                    self.assertIs(invocation.kwargs["offline"], True)
                    self.assertEqual(invocation.kwargs["pull"], "never")

    def test_existing_acquisition_failures_keep_identity_and_exit_codes(self):
        cases = (
            (scan.TrivyDatabaseAcquisitionError, "_download_trivy_database", 86),
            (scan.RuntimeLibraryDonorAcquisitionError, "_acquire_scan_images", 87),
            (scan.RuntimeLibraryDonorValidationError, "_acquire_scan_images", 88),
        )
        for error_type, seam, code in cases:
            with self.subTest(code=code), tempfile.TemporaryDirectory() as temporary:
                with self.fixture(Path(temporary)) as (paths, seams, _report, _schema):
                    original = error_type("synthetic hidden failure")
                    seams[seam].side_effect = original
                    with self.assertRaises(error_type) as raised:
                        scan.generate_scan_evidence(**paths)
                    self.assertIs(raised.exception, original)
                    streams = io.StringIO()
                    with (mock.patch.object(scan, "main", side_effect=original),
                          contextlib.redirect_stdout(streams),
                          contextlib.redirect_stderr(streams),
                          self.assertRaises(SystemExit) as exited):
                        scan.cli()
                    self.assertEqual(exited.exception.code, code)
                    self.assertEqual(streams.getvalue(), "")

    def test_cli_exits_silently_without_retaining_stage_exception(self):
        for stage, code in VULNERABILITY_SCAN_STAGE_EXIT_CODES.items():
            with self.subTest(stage=stage):
                streams = io.StringIO()
                with (mock.patch.object(scan, "main", side_effect=scan.ScanStageFailure(stage)),
                      contextlib.redirect_stdout(streams), contextlib.redirect_stderr(streams),
                      self.assertRaises(SystemExit) as raised):
                    scan.cli()
                self.assertEqual(raised.exception.code, code)
                self.assertEqual(streams.getvalue(), "")
                self.assert_detached(raised.exception)

    def checked_failure(self, phase: str, code: int):
        private_path = "/" + "home/runner/work/private"
        payload = f"Bearer SYNTHETIC-DO-NOT-REPLAY {private_path}".encode()
        command = (f"import os,sys;os.write(1,{payload!r});"
                   f"os.write(2,{payload!r});sys.exit({code})")
        output = io.StringIO()
        with (contextlib.redirect_stdout(output), contextlib.redirect_stderr(output),
              self.assertRaises(ValueError) as raised):
            assurance.run_checked(phase, [sys.executable, "-c", command])
        rendered = output.getvalue() + str(raised.exception)
        self.assertNotIn("Bearer", rendered)
        self.assertNotIn(private_path, rendered)
        self.assertNotIn("SYNTHETIC-DO-NOT-REPLAY", rendered)
        self.assertNotIn(hashlib.sha256(payload).hexdigest(), rendered)
        self.assert_detached(raised.exception)
        return rendered

    def test_real_subprocess_reserved_exits_publish_only_fixed_stage(self):
        for stage, code in VULNERABILITY_SCAN_STAGE_EXIT_CODES.items():
            with self.subTest(stage=stage):
                rendered = self.checked_failure("vulnerability-scan", code)
                self.assertIn(f"failure_stage={stage}", rendered)
                self.assertEqual(rendered.count("failure_stage="), 1)

    def test_unknown_and_other_phase_exit_codes_are_generic_failures(self):
        cases = [("vulnerability-scan", 1), ("vulnerability-scan", 125)]
        cases.extend(("container-acceptance", code)
                     for code in VULNERABILITY_SCAN_STAGE_EXIT_CODES.values())
        for phase, code in cases:
            with self.subTest(phase=phase, code=code):
                rendered = self.checked_failure(phase, code)
                self.assertIn("exited unsuccessfully", rendered)
                self.assertNotIn("failure_stage=", rendered)

    def test_classified_policy_exit_cannot_promote_quarantined_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            phases = []

            def phase(name, _arguments):
                phases.append(name)
                if name == "vulnerability-scan":
                    quarantine = next((root / "artifacts").glob(".gateway-quarantine-*"))
                    (quarantine / "failed-scan.json").write_text('{"passed":false}')
                    code = VULNERABILITY_SCAN_STAGE_EXIT_CODES["vulnerability-policy"]
                    assurance.run_checked(name, [sys.executable, "-c",
                                                 f"raise SystemExit({code})"])
                return {"name": name, "passed": True}

            streams = io.StringIO()
            with (mock.patch.object(assurance, "ROOT", root),
                  mock.patch.object(sys, "argv", ["run_gateway_image_assurance.py"]),
                  mock.patch.object(assurance, "run_phase", side_effect=phase),
                  mock.patch.object(assurance, "write_evidence_manifest") as manifest,
                  contextlib.redirect_stdout(streams), contextlib.redirect_stderr(streams),
                  self.assertRaises(ValueError)):
                assurance.main()
            self.assertEqual(phases[-1], "vulnerability-scan")
            self.assertNotIn("container-acceptance", phases)
            manifest.assert_not_called()
            self.assertFalse((root / "artifacts" / "gateway").exists())
            self.assertEqual(list((root / "artifacts").glob(".gateway-quarantine-*")), [])
            self.assertIn("failure_stage=vulnerability-policy", streams.getvalue())


if __name__ == "__main__":
    unittest.main()
