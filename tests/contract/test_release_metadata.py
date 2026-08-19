from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.check_versions import is_valid_product_version


ROOT = Path(__file__).resolve().parents[2]


class ReleaseMetadataTests(unittest.TestCase):
    def test_product_version_is_stable_semver(self) -> None:
        for value in ("0.0.0", "0.1.0", "1.0.0", "10.23.456"):
            with self.subTest(value=value):
                self.assertTrue(is_valid_product_version(value))

        for value in (
            "01.0.0",
            "1.00.0",
            "1.0.00",
            "1.0",
            "v1.0.0",
            "1.0.0-01",
            "1.0.0-alpha",
            "1.0.0+build",
        ):
            with self.subTest(value=value):
                self.assertFalse(is_valid_product_version(value))

    def test_sbom_uses_canonical_product_version(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "sbom.cdx.json"
            subprocess.run(
                [sys.executable, "scripts/generate_sbom.py", "--output", str(output)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            sbom = json.loads(output.read_text(encoding="utf-8"))

        expected = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(sbom["metadata"]["component"]["version"], expected)
        self.assertNotIn("Stage 0", sbom["metadata"]["properties"][0]["value"])


if __name__ == "__main__":
    unittest.main()
