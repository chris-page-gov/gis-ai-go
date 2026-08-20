from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def load_script(name: str) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {name}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


PACKAGE = load_script("package_pages")
VERIFY = load_script("verify_pages_archive")


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class PagesPublicationContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.dist = self.root / "dist"
        self.output = self.root / "output"
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

    def _write(self, relative: str, value: bytes) -> None:
        path = self.dist / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value)

    def _make_checked_distribution(self) -> None:
        self._write(
            "index.html",
            (
                '<!doctype html><html lang="en-GB"><head>'
                '<link rel="icon" href="./favicon.svg">'
                '<link rel="stylesheet" href="./assets/app.css">'
                '<script type="module" src="./assets/app.js"></script>'
                "</head><body>GIS AI GO</body></html>\n"
            ).encode(),
        )
        self._write("favicon.svg", b"<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>\n")
        self._write("assets/app.css", b"body { color: #111; }\n")
        self._write("assets/app.js", b"document.documentElement.className = 'js';\n")
        self._write("catalogue/.explorer-generated", b"gis-ai-go-public-explorer-data.v1\n")

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
            self._write(f"catalogue/{relative}", value)
        ledger = "".join(
            f"{sha256(value)}  {relative}\n"
            for relative, value in sorted(catalogue_files.items())
        ).encode()
        self._write("catalogue/CHECKSUMS.sha256", ledger)

    def _build(self, output: Path | None = None) -> dict[str, Any]:
        return PACKAGE.build_archive(
            dist=self.dist,
            output_dir=output or self.output,
            source_commit=self.head,
            repository="chris-page-gov/gis-ai-go",
            version=self.version,
            base_path="/gis-ai-go/",
        )

    def _verify(
        self,
        output: Path | None = None,
        *,
        source_commit: str | None = None,
        expected_digest: str | None = None,
    ) -> dict[str, Any]:
        target = output or self.output
        return VERIFY.verify_archive(
            archive_path=target / "artifact.tar",
            checksum_path=target / "artifact.tar.sha256",
            receipt_path=target / "archive-receipt.json",
            expected_source_commit=source_commit or self.head,
            expected_repository="chris-page-gov/gis-ai-go",
            expected_version=self.version,
            expected_base_path="/gis-ai-go/",
            expected_archive_sha256=expected_digest,
        )

    def _archive_files(self, output: Path | None = None) -> dict[str, bytes]:
        target = output or self.output
        with tarfile.open(target / "artifact.tar", mode="r:") as archive:
            return {
                member.name: archive.extractfile(member).read()  # type: ignore[union-attr]
                for member in archive.getmembers()
            }

    def test_builds_and_verifies_exact_deterministic_outputs(self) -> None:
        first = self._build()
        second_output = self.root / "second"
        second = self._build(second_output)
        self.assertEqual(set(path.name for path in self.output.iterdir()), PACKAGE.OUTPUT_NAMES)
        for name in sorted(PACKAGE.OUTPUT_NAMES):
            self.assertEqual((self.output / name).read_bytes(), (second_output / name).read_bytes())
        self.assertEqual(first, second)
        verified = self._verify(expected_digest=first["archive"]["sha256"])
        self.assertEqual(verified, first)
        self.assertEqual(first["okfContentRootSha256"], self.content_root)

    def test_archive_preserves_distribution_bytes_and_normalises_tar_metadata(self) -> None:
        self._build()
        source = PACKAGE.inventory_regular_files(self.dist)
        archive_files = self._archive_files()
        for path, value in source.items():
            self.assertEqual(archive_files[path], value)
        self.assertEqual(archive_files[".nojekyll"], b"")
        with tarfile.open(self.output / "artifact.tar", mode="r:") as archive:
            members = archive.getmembers()
        self.assertEqual(
            [member.name for member in members], sorted(member.name for member in members)
        )
        for member in members:
            self.assertTrue(member.isfile())
            self.assertEqual(member.type, tarfile.REGTYPE)
            self.assertEqual((member.uid, member.gid, member.uname, member.gname), (0, 0, "", ""))
            self.assertEqual((member.mode, member.mtime, member.pax_headers), (0o644, 0, {}))

    def test_public_checksum_ledger_is_complete_fetchable_and_acyclic(self) -> None:
        self._build()
        files = self._archive_files()
        rows = VERIFY.parse_checksum_ledger(
            files["publication/CHECKSUMS.sha256"], "publication checksums"
        )
        ledger_paths = [row["path"] for row in rows]
        self.assertNotIn(".nojekyll", ledger_paths)
        self.assertNotIn("publication/CHECKSUMS.sha256", ledger_paths)
        self.assertEqual(
            ledger_paths,
            sorted(set(files) - {".nojekyll", "publication/CHECKSUMS.sha256"}),
        )
        manifest = json.loads(files["publication/manifest.json"])
        payload_paths = [item["path"] for item in manifest["payload"]["files"]]
        self.assertIn(".nojekyll", payload_paths)
        supporting_paths = [item["path"] for item in manifest["publicationFiles"]]
        self.assertEqual(
            supporting_paths,
            [
                "publication/provenance.json",
                "publication/sbom.cdx.json",
                "publication/site-receipt.json",
            ],
        )

    def test_metadata_has_fixed_schemas_identity_and_no_wall_clock(self) -> None:
        receipt = self._build()
        files = self._archive_files()
        manifest = json.loads(files["publication/manifest.json"])
        provenance = json.loads(files["publication/provenance.json"])
        site_receipt = json.loads(files["publication/site-receipt.json"])
        sbom = json.loads(files["publication/sbom.cdx.json"])
        self.assertEqual(receipt["schema"], "gis-ai-go.pages-archive-receipt.v1")
        self.assertEqual(manifest["schema"], "gis-ai-go.pages-manifest.v1")
        self.assertEqual(provenance["schema"], "gis-ai-go.pages-provenance.v1")
        self.assertEqual(site_receipt["schema"], "gis-ai-go.pages-site-receipt.v1")
        self.assertEqual((sbom["bomFormat"], sbom["specVersion"]), ("CycloneDX", "1.6"))
        for document in (receipt, manifest, provenance, site_receipt):
            self.assertEqual(document["repository"], "chris-page-gov/gis-ai-go")
            self.assertEqual(document["sourceCommit"], self.head)
            self.assertEqual(document["version"], self.version)
            self.assertEqual(document["basePath"], "/gis-ai-go/")
            self.assertEqual(
                document["canonicalUrl"],
                "https://chris-page-gov.github.io/gis-ai-go/",
            )
            serialised = json.dumps(document)
            for forbidden in ("createdAt", "generatedAt", "publishedAt", "timestamp"):
                self.assertNotIn(forbidden, serialised)
        self.assertFalse(provenance["determinism"]["wallClockIncluded"])

    def test_rejects_symbolic_link_in_distribution(self) -> None:
        (self.dist / "assets" / "linked.js").symlink_to(self.dist / "assets" / "app.js")
        with self.assertRaisesRegex(ValueError, "symbolic links"):
            self._build()

    def test_rejects_hard_link_in_distribution(self) -> None:
        os.link(self.dist / "assets" / "app.js", self.dist / "assets" / "hard.js")
        with self.assertRaisesRegex(ValueError, "hard-linked"):
            self._build()

    @unittest.skipUnless(hasattr(os, "mkfifo"), "requires POSIX FIFO support")
    def test_rejects_special_file_in_distribution(self) -> None:
        os.mkfifo(self.dist / "assets" / "pipe")
        with self.assertRaisesRegex(ValueError, "regular files only"):
            self._build()

    def test_rejects_historical_research_and_unexpected_files(self) -> None:
        self._write("research/notes.txt", b"not for publication\n")
        with self.assertRaisesRegex(ValueError, "forbidden"):
            self._build()
        (self.dist / "research" / "notes.txt").unlink()
        (self.dist / "research").rmdir()
        self._write("notes.txt", b"unexpected\n")
        with self.assertRaisesRegex(ValueError, "inventory is not exact"):
            self._build()

    def test_rejects_catalogue_byte_change(self) -> None:
        path = self.dist / "catalogue" / "okf-bundle.json"
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "catalogue checksum mismatch"):
            self._build()

    def test_rejects_catalogue_revision_different_from_publication_source(self) -> None:
        receipt_path = self.dist / "catalogue" / "build-receipt.json"
        receipt = json.loads(receipt_path.read_bytes())
        receipt["revision"] = "b" * 40
        receipt_bytes = canonical_json(receipt)
        receipt_path.write_bytes(receipt_bytes)
        ledger_path = self.dist / "catalogue" / "CHECKSUMS.sha256"
        rows = VERIFY.parse_checksum_ledger(ledger_path.read_bytes(), "catalogue checksums")
        ledger_path.write_bytes(
            "".join(
                f"{sha256(receipt_bytes) if row['path'] == 'build-receipt.json' else row['sha256']}"
                f"  {row['path']}\n"
                for row in rows
            ).encode()
        )
        with self.assertRaisesRegex(ValueError, "revision differs"):
            self._build()

    def test_rejects_output_directory_symlink(self) -> None:
        target = self.root / "target"
        target.mkdir()
        self.output.symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "output directory must be a real directory"):
            self._build()
        self.assertEqual(list(target.iterdir()), [])

    def test_rejects_preexisting_output_symlink(self) -> None:
        self.output.mkdir()
        target = self.root / "outside.txt"
        target.write_text("do not replace\n", encoding="utf-8")
        (self.output / "artifact.tar").symlink_to(target)
        with self.assertRaisesRegex(ValueError, "ordinary single-link file"):
            self._build()
        self.assertEqual(target.read_text(encoding="utf-8"), "do not replace\n")

    def test_verifier_rejects_outer_file_symlink(self) -> None:
        self._build()
        real_checksum = self.root / "real-checksum"
        (self.output / "artifact.tar.sha256").replace(real_checksum)
        (self.output / "artifact.tar.sha256").symlink_to(real_checksum)
        with self.assertRaisesRegex(ValueError, "ordinary single-link"):
            self._verify()

    def test_rejects_wrong_source_commit_and_digest(self) -> None:
        receipt = self._build()
        with self.assertRaisesRegex(ValueError, "sourceCommit"):
            self._verify(source_commit="b" * 40)
        with self.assertRaisesRegex(ValueError, "accepted artefact"):
            self._verify(expected_digest="b" * 64)
        self.assertNotEqual(receipt["archive"]["sha256"], "b" * 64)

    def test_rejects_noncanonical_archive_even_with_coordinated_outer_files(self) -> None:
        receipt = self._build()
        archive_path = self.output / "artifact.tar"
        archive_path.write_bytes(archive_path.read_bytes() + (b"\0" * 512))
        altered = archive_path.read_bytes()
        digest = sha256(altered)
        checksum = f"{digest}  artifact.tar\n".encode()
        (self.output / "artifact.tar.sha256").write_bytes(checksum)
        receipt["archive"]["bytes"] = len(altered)
        receipt["archive"]["sha256"] = digest
        receipt["checksum"]["sha256"] = sha256(checksum)
        (self.output / "archive-receipt.json").write_bytes(canonical_json(receipt))
        with self.assertRaisesRegex(ValueError, "canonical deterministic"):
            self._verify(expected_digest=digest)

    def test_rejects_hard_link_tar_member(self) -> None:
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w", format=tarfile.USTAR_FORMAT) as archive:
            regular = tarfile.TarInfo("index.html")
            regular.size = 1
            regular.mode = 0o644
            regular.mtime = 0
            archive.addfile(regular, io.BytesIO(b"x"))
            linked = tarfile.TarInfo("linked.html")
            linked.type = tarfile.LNKTYPE
            linked.linkname = "index.html"
            linked.mode = 0o644
            linked.mtime = 0
            archive.addfile(linked)
        with self.assertRaisesRegex(ValueError, "regular files only"):
            VERIFY.read_archive(buffer.getvalue())

    def test_cli_contract_builds_then_verifies(self) -> None:
        package = subprocess.run(
            [
                "python3", "scripts/package_pages.py",
                "--dist", str(self.dist),
                "--output-dir", str(self.output),
                "--source-commit", self.head,
                "--repository", "chris-page-gov/gis-ai-go",
                "--version", self.version,
                "--base-path", "/gis-ai-go/",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        receipt = json.loads((self.output / "archive-receipt.json").read_bytes())
        verify = subprocess.run(
            [
                "python3", "scripts/verify_pages_archive.py",
                "--archive", str(self.output / "artifact.tar"),
                "--checksum", str(self.output / "artifact.tar.sha256"),
                "--receipt", str(self.output / "archive-receipt.json"),
                "--expected-source-commit", self.head,
                "--expected-repository", "chris-page-gov/gis-ai-go",
                "--expected-version", self.version,
                "--expected-base-path", "/gis-ai-go/",
                "--expected-archive-sha256", receipt["archive"]["sha256"],
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("Built deterministic Pages archive sha256=", package.stdout)
        self.assertIn("Verified Pages archive sha256=", verify.stdout)


if __name__ == "__main__":
    unittest.main()
