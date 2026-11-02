from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import gateway_image as image  # noqa: E402
import node_runtime_advisory as node  # noqa: E402
from tests.contract import test_node_advisory_diagnostics as diagnostics  # noqa: E402

FIXTURE = ROOT / "tests/fixtures/node-runtime-advisory/CVE-2026-105482.json"


class ReviewedPublicAdvisoryDescriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record_bytes = FIXTURE.read_bytes()
        cls.record = json.loads(cls.record_bytes)
        cls.description = next(
            item["value"] for item in cls.record["containers"]["cna"]["descriptions"]
            if item["lang"] == "en"
        )

    def advisory(self):
        return {"id": "CVE-2026-105482", "description": self.description}

    def assert_rejected(self, document):
        self.assertEqual(image.prohibited_json_reason(document), "sensitive")
        with self.assertRaises(ValueError):
            image.assert_no_private_json(document, "synthetic report")
        with self.assertRaises(ValueError):
            image.assert_no_private_text(image.canonical_json_bytes(document), "synthetic report")

    def test_immutable_public_source_and_description_identity(self):
        self.assertEqual(hashlib.sha256(self.record_bytes).hexdigest(),
                         "4741deb16926e3245564d15c2a47929fb1a31fafe85dbab9d81f9081b5262d17")
        self.assertEqual(self.record["cveMetadata"]["cveId"], "CVE-2026-105482")
        self.assertEqual(len(self.description.encode("utf-8")), 670)
        self.assertEqual(hashlib.sha256(self.description.encode("utf-8")).hexdigest(),
                         "4860b19ad9d60392ad2fb11103fc786e634469d26db9ecc7692591ac06967f01")
        self.assertNotIn(chr(0), self.description)
        self.assertIn("\\0", self.description)
        self.assertEqual(image.prohibited_text_reason(self.description), "sensitive")

    def test_exact_description_passes_json_and_canonical_text_without_mutating_raw_evidence(self):
        for report in (self.advisory(), {"matches": [{"vulnerability": self.advisory()}]},
                       {"vulnerabilities": [self.advisory()]}):
            original = copy.deepcopy(report)
            encoded = image.canonical_json_bytes(report)
            self.assertIsNone(image.prohibited_json_reason(report))
            image.assert_no_private_json(report, "public report")
            image.assert_no_private_text(encoded, "public report")
            self.assertEqual(report, original)
            self.assertEqual(image.canonical_json_bytes(report), encoded)

    def test_other_keys_ids_standalone_and_embedded_prose_keep_original_checks(self):
        for document in (
            self.description,
            [self.description],
            {"description": self.description},
            {"id": "CVE-2026-105483", "description": self.description},
            {"id": "CVE-2026-105482", "Description": self.description},
            {"id": "CVE-2026-105482", "value": self.description},
            {"id": "CVE-2026-105482", "description": [self.description]},
        ):
            with self.subTest(document_type=type(document).__name__):
                self.assert_rejected(document)

    def test_changed_appended_embedded_and_actual_control_values_still_refuse(self):
        variants = (
            "prefix " + self.description,
            self.description + " suffix",
            self.description.replace("DNS", "dns", 1),
            self.description.replace("\\0", chr(0)),
            self.description + " Bearer SYNTHETIC-PRIVATE-VALUE",
            self.description + "/" + "home/private/source",
        )
        for value in variants:
            with self.subTest(length=len(value)):
                self.assert_rejected({"id": "CVE-2026-105482", "description": value})

    def test_enclosing_credential_and_sibling_guards_remain_active(self):
        for document in (
            {"password": self.advisory()},
            {"authorization": self.advisory()},
            {"name": "password", "value": self.advisory()},
            {**self.advisory(), "authorization": "Bearer SYNTHETIC-PRIVATE-VALUE"},
            {"advisory": self.advisory(), "source": "/" + "home/private/source"},
        ):
            with self.subTest(keys=list(document)):
                self.assert_rejected(document)

    def with_public_description(self, scan_operation):
        def scan(*args, **kwargs):
            report = scan_operation(*args, **kwargs)
            if kwargs["output_format"] == "json":
                vulnerabilities = [match["vulnerability"] for match in report["matches"]]
            else:
                vulnerabilities = report.get("vulnerabilities", [])
            for vulnerability in vulnerabilities:
                if vulnerability["id"] == "CVE-2026-105482":
                    vulnerability["description"] = self.description
            return report
        return scan

    def test_raw_calibration_reports_retain_exact_public_description(self):
        fixture = diagnostics.NodeAdvisoryDiagnosticsTests()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with fixture.fixture(root) as (arguments, seams, behaviour, _clock):
                behaviour["affected_ids"] += ("CVE-2026-105482",)
                behaviour["fixed_ids"] = ("CVE-2026-105482",)
                seams["_scan_raw"].side_effect = self.with_public_description(seams["_scan_raw"].side_effect)
                evidence, findings = node.generate_node_advisory(**arguments)
                self.assertEqual(findings, [])
                self.assertIs(evidence["calibration"]["passed"], True)
                for role in ("affected", "fixed"):
                    for kind in ("json_report", "cyclonedx_report"):
                        document = json.loads((root / node.NODE_ROLE_FILES[role][kind]).read_bytes())
                        vulnerabilities = ([match["vulnerability"] for match in document["matches"]]
                                           if kind == "json_report" else document["vulnerabilities"])
                        retained = next(item["description"] for item in vulnerabilities
                                        if item["id"] == "CVE-2026-105482")
                        self.assertEqual(retained.encode("utf-8"), self.description.encode("utf-8"))

    def test_admitted_public_description_never_waives_high_or_critical_actual_findings(self):
        fixture = diagnostics.NodeAdvisoryDiagnosticsTests()
        for severity in ("High", "Critical"):
            with self.subTest(severity=severity), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                with fixture.fixture(root) as (arguments, seams, behaviour, _clock):
                    behaviour["actual_ids"] = ("CVE-2026-105482",)
                    behaviour["actual_severity"] = severity
                    seams["_scan_raw"].side_effect = self.with_public_description(seams["_scan_raw"].side_effect)
                    with self.assertRaises(node.NodeAdvisoryFailure) as raised:
                        node.generate_node_advisory(**arguments)
                    self.assertEqual(raised.exception.stage, "node-runtime-policy")
                    fixture.assert_no_role_files(root)

    def test_admitted_value_still_counts_towards_all_existing_bounds(self):
        for name, limit in (("MAX_PRIVACY_TEXT_BYTES", 669),
                            ("MAX_PRIVACY_JSON_NODES", 2),
                            ("MAX_PRIVACY_JSON_DEPTH", 0)):
            with self.subTest(bound=name), mock.patch.object(image, name, limit):
                self.assertEqual(image.prohibited_json_reason(self.advisory()), "sensitive")
