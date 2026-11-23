from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import gateway_image as image


class NovemberPublicAdvisoryDescriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = (ROOT / "tests/fixtures/node-runtime-advisory/CVE-2026-123864.json").read_bytes()
        assert hashlib.sha256(raw).hexdigest() == "8191afa44fd10504ad7b00387ebc0eeda501de91b775883e62d7b1ef290d2fef"
        record = json.loads(raw)
        assert record["cveMetadata"]["cveId"] == "CVE-2026-123864"
        cls.description = next(x["value"] for x in record["containers"]["cna"]["descriptions"] if x["lang"] == "en")

    def advisory(self):
        return {"id": "CVE-2026-123864", "description": self.description}

    def reject(self, document):
        self.assertIsNotNone(image.prohibited_json_reason(document))
        with self.assertRaises(ValueError):
            image.assert_no_private_json(document, "synthetic report")
        with self.assertRaises(ValueError):
            image.assert_no_private_text(image.canonical_json_bytes(document), "synthetic report")

    def test_exact_public_source_passes_both_report_formats_without_mutation(self):
        self.assertEqual(len(self.description.encode()), 929)
        self.assertEqual(hashlib.sha256(self.description.encode()).hexdigest(),
                         "97b94971e6c46a1c75d0e6b3a6f1334391574030f715be10c6b39ce40c059601")
        self.assertEqual(image.prohibited_text_reason(self.description), "sensitive")
        for report in (self.advisory(), {"matches": [{"vulnerability": self.advisory()}]},
                       {"vulnerabilities": [self.advisory()]}):
            original = copy.deepcopy(report)
            image.assert_no_private_json(report, "public advisory")
            image.assert_no_private_text(image.canonical_json_bytes(report), "public advisory")
            self.assertEqual(report, original)

    def test_other_contexts_and_mutated_prose_remain_rejected(self):
        for value in (self.description, [self.description], {"description": self.description},
                      {"id": "CVE-2026-123865", "description": self.description},
                      {"id": "CVE-2026-123864", "Description": self.description},
                      {"id": "CVE-2026-123864", "value": self.description}):
            with self.subTest(kind=type(value).__name__):
                self.reject(value)
        for value in ("prefix " + self.description, self.description + " suffix",
                      self.description.replace("HTTPS", "https", 1),
                      self.description + " Bearer SYNTHETIC-PRIVATE-VALUE",
                      self.description + chr(0)):
            self.reject({"id": "CVE-2026-123864", "description": value})

    def test_enclosing_credentials_and_sibling_guards_remain_active(self):
        for value in ({"password": self.advisory()}, {"authorization": self.advisory()},
                      {"name": "password", "value": self.advisory()},
                      {**self.advisory(), "authorization": "Bearer SYNTHETIC-PRIVATE-VALUE"},
                      {"advisory": self.advisory(), "source": "/" + "home/private/source"}):
            self.reject(value)


if __name__ == "__main__":
    unittest.main()
