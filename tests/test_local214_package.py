"""Source identity, deterministic packaging and hostile archive-input regressions."""

from __future__ import annotations

import io
import json
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

from scripts.local214_package import (
    ARCHIVE, EDITION, IDENTITY, capture_source, make_archive, package, scan_bytes, verify,
)


class Local214PackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sandbox = tempfile.TemporaryDirectory(prefix="local214-package-test-")
        self.addCleanup(self.sandbox.cleanup)
        self.base = Path(self.sandbox.name)
        self.root = self.base / "source"
        self.root.mkdir()
        self.git("init", "-q")
        fixtures = {
            "package.json": '{"version":"0.1.0"}\n',
            "pnpm-lock.yaml": "lockfileVersion: '9.0'\n",
            "uv.lock": "version = 1\n",
            "scripts/start-local-candidate": "#!/bin/sh\nexit 0\n",
            "src/example.ts": "export const example = 1;\n",
        }
        for name, content in fixtures.items():
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content)
        (self.root / "scripts/start-local-candidate").chmod(0o755)
        self.commit()

    def git(self, *args: str) -> str:
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout

    def commit(self) -> None:
        self.git("add", ".")
        self.git("-c", "user.name=Local edition test", "-c",
                 "user.email=local-edition@example.invalid", "commit", "-qm", "test fixture")

    def extract(self) -> tuple[dict, Path]:
        identity, files = capture_source(self.root)
        extraction = self.base / "extracted"
        extraction.mkdir()
        with tarfile.open(fileobj=io.BytesIO(make_archive(identity, files))) as archive:
            archive.extractall(extraction, filter="data")
        return identity, extraction / f"gis-ai-go-{EDITION}"

    def test_reproducible_source_package_and_extracted_identity(self) -> None:
        first = self.base / "first"
        second = self.base / "second"
        manifest = package(self.root, first)
        package(self.root, second)
        self.assertEqual((first / ARCHIVE).read_bytes(), (second / ARCHIVE).read_bytes())
        self.assertEqual((first / "SHA256SUMS").read_bytes(), (second / "SHA256SUMS").read_bytes())
        self.assertEqual(manifest["software_version"], "0.1.0")
        self.assertFalse(manifest["boundary"]["attested"])
        self.assertNotIn(str(self.root), json.dumps(manifest))
        identity, extracted = self.extract()
        self.assertEqual(verify(extracted), identity)
        self.assertTrue((extracted / "scripts/start-local-candidate").stat().st_mode & 0o111)
        self.assertFalse((extracted / ".git").exists())

    def test_dirty_source_untracked_input_and_existing_output_are_refused(self) -> None:
        output = self.base / "existing"
        output.mkdir()
        with self.assertRaises(FileExistsError):
            package(self.root, output)
        with self.assertRaisesRegex(ValueError, "outside"):
            package(self.root, self.root / "output")
        (self.root / "untracked.txt").write_text("not committed")
        with self.assertRaisesRegex(ValueError, "clean"):
            capture_source(self.root)

    def test_symlink_and_generated_tracked_inputs_are_refused(self) -> None:
        (self.root / "linked").symlink_to("src/example.ts")
        self.commit()
        with self.assertRaisesRegex(ValueError, "regular"):
            capture_source(self.root)
        (self.root / "linked").unlink()
        (self.root / "dist").mkdir()
        (self.root / "dist/generated.js").write_text("untrusted generated code")
        self.commit()
        with self.assertRaisesRegex(ValueError, "prohibited"):
            capture_source(self.root)

    def test_tampered_file_and_extra_source_are_refused(self) -> None:
        _, extracted = self.extract()
        original = (extracted / "src/example.ts").read_bytes()
        (extracted / "src/example.ts").write_bytes(original.replace(b"1", b"2"))
        with self.assertRaisesRegex(ValueError, "Changed source"):
            verify(extracted)
        (extracted / "src/example.ts").write_bytes(original)
        (extracted / "extra.mjs").write_text("export default 'unexpected';")
        with self.assertRaisesRegex(ValueError, "Unexpected source"):
            verify(extracted)

    def test_identity_cannot_rename_commit_or_drop_source_file(self) -> None:
        identity, extracted = self.extract()
        forged = {**identity, "source_commit": "1" * 40}
        (extracted / IDENTITY).write_text(json.dumps(forged))
        with self.assertRaisesRegex(ValueError, "named Git commit"):
            verify(extracted)
        forged = {**identity, "materials": identity["materials"][:-1]}
        (extracted / IDENTITY).write_text(json.dumps(forged))
        with self.assertRaisesRegex(ValueError, "named Git commit"):
            verify(extracted)

    def test_extracted_symlink_and_execution_mode_changes_are_refused(self) -> None:
        _, extracted = self.extract()
        launch = extracted / "scripts/start-local-candidate"
        launch.chmod(0o644)
        with self.assertRaisesRegex(ValueError, "executable mode"):
            verify(extracted)
        launch.chmod(0o755)
        (extracted / "src/example.ts").unlink()
        (extracted / "src/example.ts").symlink_to(self.root / "src/example.ts")
        with self.assertRaisesRegex(ValueError, "symlink"):
            verify(extracted)

    def test_installed_and_generated_files_are_explicitly_outside_source_verification(self) -> None:
        identity, extracted = self.extract()
        (extracted / "node_modules").mkdir()
        (extracted / "node_modules/installed.js").write_text("installed dependency")
        (extracted / "artifacts").mkdir()
        (extracted / "artifacts/output.json").write_text("{}")
        self.assertEqual(verify(extracted), identity)

    def test_baseline_secret_scan_rejects_without_echoing_secret(self) -> None:
        secret = "gh" + "p_" + "a" * 30
        # Exercise the package's exact scanner without persisting even a fabricated
        # credential-shaped fixture in a test repository or temporary file.
        with self.assertRaisesRegex(ValueError, "possible GitHub token") as caught:
            scan_bytes("src/example.ts", f"export const fixture = '{secret}';\n".encode())
        self.assertNotIn(secret, str(caught.exception))


if __name__ == "__main__":
    unittest.main()
