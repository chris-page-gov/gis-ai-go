from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.check_versions import (
    is_valid_product_version,
    release_metadata_errors,
    release_readiness_errors,
)


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

    def test_bootstrap_version_does_not_claim_release_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.assertEqual(release_metadata_errors(root, "0.0.0"), [])

    def test_release_readiness_is_an_explicit_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "changelog.d").mkdir()
            (root / "changelog.d" / "NEXT.feature.md").write_text(
                "- Continue feature delivery.\n",
                encoding="utf-8",
            )

            self.assertEqual(
                release_readiness_errors(root, "0.1.0", release_ready=False),
                [],
                "ordinary post-release feature branches must allow changelog fragments",
            )
            self.assertIn(
                "VERSION 0.0.0 is the bootstrap candidate and cannot be released",
                release_readiness_errors(root, "0.0.0", release_ready=True),
            )
            self.assertIn(
                "CHANGELOG.md is missing",
                release_readiness_errors(root, "0.1.0", release_ready=True),
            )

            (root / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
            (root / "changelog.d" / "README.md").write_text(
                "Instructions\n",
                encoding="utf-8",
            )
            errors = release_readiness_errors(root, "0.1.0", release_ready=True)
            self.assertIn("unconsumed changelog fragments: NEXT.feature.md", errors)
            self.assertIn("RELEASE_NOTES/0.1.0.md is missing", errors)

    def test_supported_version_requires_complete_release_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "changelog.d").mkdir()
            (root / "changelog.d" / "README.md").write_text("Instructions\n", encoding="utf-8")
            (root / "RELEASE_NOTES").mkdir()
            (root / "RELEASE_NOTES" / "0.1.0.md").write_text(
                "# GIS AI GO v0.1.0\n",
                encoding="utf-8",
            )
            (root / "CHANGELOG.md").write_text(
                "# Changelog\n\n"
                "## [Unreleased]\n\n"
                "## [0.1.0] - 2026-08-20\n\n"
                "[0.1.0]: https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0\n",
                encoding="utf-8",
            )

            self.assertEqual(release_metadata_errors(root, "0.1.0"), [])

            (root / "changelog.d" / "QUAL-105.security.md").write_text(
                "- Release gate.\n",
                encoding="utf-8",
            )
            (root / "RELEASE_NOTES" / "0.1.0.md").unlink()
            errors = release_metadata_errors(root, "0.1.0")
            self.assertIn("RELEASE_NOTES/0.1.0.md is missing", errors)
            self.assertIn("unconsumed changelog fragments: QUAL-105.security.md", errors)

            (root / "RELEASE_NOTES" / "0.1.0.md").write_text("\n", encoding="utf-8")
            self.assertIn(
                "RELEASE_NOTES/0.1.0.md is empty",
                release_metadata_errors(root, "0.1.0"),
            )

            (root / "changelog.d" / "README.md").unlink()
            self.assertIn(
                "changelog.d/README.md is missing",
                release_metadata_errors(root, "0.1.0"),
            )

    def test_supported_version_rejects_undated_or_wrong_release_link(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "changelog.d").mkdir()
            (root / "RELEASE_NOTES").mkdir()
            (root / "RELEASE_NOTES" / "0.1.0.md").write_text("Notes\n", encoding="utf-8")
            (root / "CHANGELOG.md").write_text(
                "## [0.1.0]\n\n"
                "[0.1.0]: https://github.com/chris-page-gov/gis-ai-go/commits/main\n",
                encoding="utf-8",
            )

            errors = release_metadata_errors(root, "0.1.0")
            self.assertIn("CHANGELOG.md has no dated [0.1.0] release section", errors)
            self.assertIn("CHANGELOG.md has no exact [0.1.0] release link", errors)


if __name__ == "__main__":
    unittest.main()
