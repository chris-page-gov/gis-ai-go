from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]


def load_script(name: str) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {name}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


VERIFY = load_script("verify_pages_archive")
sys.modules["verify_pages_archive"] = VERIFY
PACKAGE = load_script("package_pages")
STAGE = load_script("stage_pages_payload")


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class PagesStagingContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.dist = self.root / "dist"
        self.package_output = self.root / "package"
        self.staging_container = self.root / "deployment-staging"
        self.staging_output = self.staging_container / "site"
        self.head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.content_root = "a" * 64
        self._make_checked_distribution()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _write_dist(self, relative: str, value: bytes) -> None:
        path = self.dist / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value)

    def _make_checked_distribution(self) -> None:
        self._write_dist(
            "index.html",
            (
                '<!doctype html><html lang="en-GB"><head>'
                '<link rel="icon" href="./favicon.svg">'
                '<link rel="stylesheet" href="./assets/app.css">'
                '<script type="module" src="./assets/app.js"></script>'
                "</head><body>GIS AI GO</body></html>\n"
            ).encode(),
        )
        self._write_dist(
            "favicon.svg",
            b'<svg xmlns="http://www.w3.org/2000/svg"></svg>\n',
        )
        self._write_dist("assets/app.css", b"body { color: #111; }\n")
        self._write_dist("assets/app.js", b"document.documentElement.className = 'js';\n")
        self._write_dist(
            "catalogue/.explorer-generated",
            b"gis-ai-go-public-explorer-data.v1\n",
        )

        catalogue_manifest = canonical_json({"files": [], "recordCount": 0, "recordIds": []})
        catalogue_files = {
            "manifest.json": catalogue_manifest,
            "okf-bundle.json": canonical_json({"recordCount": 0, "records": []}),
            "okf-bundle.jsonld": canonical_json({"@graph": []}),
            "okf-explorer.json": canonical_json({"recordCount": 0, "records": []}),
        }
        catalogue_files["build-receipt.json"] = canonical_json(
            {
                "builder": "tests/fixture",
                "builderVersion": "1.0.0",
                "contentRootSha256": self.content_root,
                "manifestSha256": sha256(catalogue_manifest),
                "revision": self.head,
                "version": self.version,
            }
        )
        for relative, value in catalogue_files.items():
            self._write_dist(f"catalogue/{relative}", value)
        self._write_dist(
            "catalogue/CHECKSUMS.sha256",
            "".join(
                f"{sha256(value)}  {relative}\n"
                for relative, value in sorted(catalogue_files.items())
            ).encode(),
        )

    def _build(self) -> dict[str, Any]:
        return PACKAGE.build_archive(
            dist=self.dist,
            output_dir=self.package_output,
            source_commit=self.head,
            repository="chris-page-gov/gis-ai-go",
            version=self.version,
            base_path="/gis-ai-go/",
        )

    def _stage(self, *, output: Path | None = None, digest: str | None = None) -> dict[str, Any]:
        receipt = json.loads((self.package_output / "archive-receipt.json").read_bytes())
        target = output or self.staging_output
        target.parent.mkdir(parents=True, exist_ok=True)
        return STAGE.stage_payload(
            archive_path=self.package_output / "artifact.tar",
            checksum_path=self.package_output / "artifact.tar.sha256",
            receipt_path=self.package_output / "archive-receipt.json",
            output_dir=target,
            expected_source_commit=self.head,
            expected_repository="chris-page-gov/gis-ai-go",
            expected_version=self.version,
            expected_base_path="/gis-ai-go/",
            expected_archive_sha256=digest or receipt["archive"]["sha256"],
        )

    def _source_files(self) -> dict[str, bytes]:
        return VERIFY.read_archive((self.package_output / "artifact.tar").read_bytes())

    def _staged_files(self, output: Path | None = None) -> dict[str, bytes]:
        target = output or self.staging_output
        return {
            path.relative_to(target).as_posix(): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }

    def test_stages_exact_regular_bytes_including_allowlisted_hidden_files(self) -> None:
        receipt = self._build()
        staged = self._stage()
        expected = self._source_files()
        self.assertEqual(self._staged_files(), expected)
        self.assertEqual(
            staged,
            {
                "archiveSha256": receipt["archive"]["sha256"],
                "payloadRootSha256": receipt["payloadRootSha256"],
                "fileCount": len(expected),
                "outputDir": str(self.staging_output),
            },
        )
        self.assertEqual((self.staging_output / ".nojekyll").read_bytes(), b"")
        self.assertIn("catalogue/.explorer-generated", expected)
        for path in self.staging_output.rglob("*"):
            metadata = path.lstat()
            self.assertFalse(stat.S_ISLNK(metadata.st_mode))
            if path.is_dir():
                self.assertEqual(stat.S_IMODE(metadata.st_mode), 0o755)
            else:
                self.assertTrue(stat.S_ISREG(metadata.st_mode))
                self.assertEqual(metadata.st_nlink, 1)
                self.assertEqual(stat.S_IMODE(metadata.st_mode), 0o644)

    def test_cli_stages_the_verified_archive_with_the_fixed_interface(self) -> None:
        receipt = self._build()
        self.staging_container.mkdir()
        completed = subprocess.run(
            [
                "python3",
                "scripts/stage_pages_payload.py",
                "--archive",
                str(self.package_output / "artifact.tar"),
                "--checksum",
                str(self.package_output / "artifact.tar.sha256"),
                "--receipt",
                str(self.package_output / "archive-receipt.json"),
                "--output-dir",
                str(self.staging_output),
                "--expected-source-commit",
                self.head,
                "--expected-repository",
                "chris-page-gov/gis-ai-go",
                "--expected-version",
                self.version,
                "--expected-base-path",
                "/gis-ai-go/",
                "--expected-archive-sha256",
                receipt["archive"]["sha256"],
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(self._staged_files(), self._source_files())
        self.assertIn(
            f"archive-sha256={receipt['archive']['sha256']} ",
            completed.stdout,
        )
        self.assertIn(
            f"payload-root-sha256={receipt['payloadRootSha256']} ",
            completed.stdout,
        )

    def test_rejects_wrong_digest_before_creating_output(self) -> None:
        self._build()
        with self.assertRaisesRegex(ValueError, "accepted artefact"):
            self._stage(digest="b" * 64)
        self.assertFalse(self.staging_output.exists())

    def test_rejects_preexisting_empty_and_nonempty_output_directories(self) -> None:
        self._build()
        for suffix, populated in (("empty", False), ("nonempty", True)):
            with self.subTest(suffix=suffix):
                output = self.root / suffix / "site"
                output.mkdir(parents=True)
                if populated:
                    (output / "untrusted.txt").write_text("untrusted\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "must not already exist"):
                    self._stage(output=output)
                if populated:
                    self.assertEqual(
                        (output / "untrusted.txt").read_text(encoding="utf-8"),
                        "untrusted\n",
                    )

    def test_rejects_output_and_parent_symbolic_links(self) -> None:
        self._build()
        real_parent = self.root / "real-parent"
        real_parent.mkdir()
        target = self.root / "target"
        target.mkdir()

        linked_output = real_parent / "linked-site"
        linked_output.symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "must not be a symbolic link"):
            self._stage(output=linked_output)
        self.assertEqual(list(target.iterdir()), [])

        linked_parent = self.root / "linked-parent"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "parent must already exist as a real directory"):
            self._stage(output=linked_parent / "site")

    def test_rejects_output_directory_replacement_race(self) -> None:
        self._build()
        self.staging_container.mkdir()
        moved = self.staging_container / "moved-site"
        decoy = self.staging_container / "decoy"
        decoy.mkdir()
        original = STAGE._write_regular_file
        replaced = False

        def replace_after_first_file(*args: Any, **kwargs: Any) -> None:
            nonlocal replaced
            original(*args, **kwargs)
            if not replaced:
                self.staging_output.rename(moved)
                self.staging_output.symlink_to(decoy, target_is_directory=True)
                replaced = True

        with mock.patch.object(STAGE, "_write_regular_file", side_effect=replace_after_first_file):
            with self.assertRaisesRegex(ValueError, "output directory changed"):
                self._stage()
        self.assertEqual(list(decoy.iterdir()), [])

    def test_rejects_staged_byte_change_before_final_inventory(self) -> None:
        self._build()
        self.staging_container.mkdir()
        original = STAGE._write_regular_file
        changed = False

        def change_index(*args: Any, **kwargs: Any) -> None:
            nonlocal changed
            original(*args, **kwargs)
            logical_path = args[1]
            if logical_path == "index.html" and not changed:
                (self.staging_output / "index.html").write_bytes(b"changed after staging\n")
                changed = True

        with mock.patch.object(STAGE, "_write_regular_file", side_effect=change_index):
            with self.assertRaisesRegex(ValueError, "inventory or bytes differ"):
                self._stage()


if __name__ == "__main__":
    unittest.main()
