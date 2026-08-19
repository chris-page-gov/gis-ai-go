from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "docs" / "research" / "2026-08-19"


class RepositoryBoundaryTests(unittest.TestCase):
    def test_research_zip_is_immutable(self) -> None:
        digest = hashlib.sha256(
            (RESEARCH / "governed-geospatial-research-pack.zip").read_bytes()
        ).hexdigest()
        self.assertEqual(
            digest,
            "08ecb65f18f8bef8af0d79dd3c9974da5939544fdecd899e62532c3089798e34",
        )

    def test_promoted_schema_ids_use_current_namespace(self) -> None:
        for path in (ROOT / "schemas").glob("*.schema.json"):
            schema = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(schema["$id"].startswith("urn:gis-ai-go:schema:"))
            self.assertNotIn("locus-accord", schema["$id"])

    def test_root_package_is_private_and_unlicensed(self) -> None:
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertTrue(package["private"])
        self.assertEqual(package["license"], "UNLICENSED")

    def test_fixture_identity_uses_current_service_name(self) -> None:
        receipt = json.loads(
            (ROOT / "providers" / "fixtures" / "evidence-receipt.example.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(receipt["software"][0]["name"], "gis-ai-go-execution")


if __name__ == "__main__":
    unittest.main()
