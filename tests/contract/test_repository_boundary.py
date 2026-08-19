from __future__ import annotations

import hashlib
import json
import re
import tomllib
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

    def test_repository_uses_mit_licence_metadata(self) -> None:
        for relative in (
            "package.json",
            "apps/mcp-gateway/package.json",
            "apps/public-explorer/package.json",
            "packages/contracts/package.json",
        ):
            package = json.loads((ROOT / relative).read_text(encoding="utf-8"))
            self.assertTrue(package["private"])
            self.assertEqual(package["license"], "MIT")

        for relative in ("pyproject.toml", "services/geo-execution/pyproject.toml"):
            with (ROOT / relative).open("rb") as handle:
                project = tomllib.load(handle)["project"]
            self.assertEqual(project["license"], "MIT")

        licence = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", licence)
        self.assertIn("Copyright (c) 2026 Chris Page", licence)

    def test_fixture_identity_uses_current_service_name(self) -> None:
        receipt = json.loads(
            (ROOT / "providers" / "fixtures" / "evidence-receipt.example.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(receipt["software"][0]["name"], "gis-ai-go-execution")

    def test_package_uv_run_commands_are_lock_strict(self) -> None:
        excluded_parts = {".git", "artifacts", "dist", "node_modules"}
        uv_run = re.compile(r"(?<![\w-])uv\s+run(?=\s)")
        locked_option = re.compile(r"^\s+--locked(?:\s|$)")

        for path in sorted(ROOT.rglob("package.json")):
            relative = path.relative_to(ROOT)
            if excluded_parts.intersection(relative.parts):
                continue
            package = json.loads(path.read_text(encoding="utf-8"))
            scripts = package.get("scripts", {})
            self.assertIsInstance(scripts, dict)
            for script_name, command in scripts.items():
                if not isinstance(command, str):
                    continue
                for invocation, match in enumerate(uv_run.finditer(command), start=1):
                    with self.subTest(
                        package=relative.as_posix(),
                        script=script_name,
                        invocation=invocation,
                    ):
                        self.assertRegex(
                            command[match.end() :],
                            locked_option,
                            "repository package scripts must start every uv run with --locked",
                        )


if __name__ == "__main__":
    unittest.main()
