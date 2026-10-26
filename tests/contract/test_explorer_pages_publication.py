from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import package_explorer_pages as package

# Discovery imports some existing CLI tests with scripts/ on sys.path. The
# builder then loads its verifier by the standalone CLI name; focused package
# tests use scripts.verify_explorer_pages_archive instead. Patch the actual
# builder dependency in either context rather than a second imported copy.
verify = package.verifier

ROOT = Path(__file__).resolve().parents[2]


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_script(name):
    specification = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class FullExplorerPagesTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.dist = self.root / "dist"
        self.dist.mkdir()
        self.source = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        self.version = (ROOT / "VERSION").read_text().strip()
        self.identity = {"repository": verify.REPOSITORY, "sourceCommit": self.source,
            "version": self.version, "basePath": verify.BASE_PATH, "canonicalUrl": verify.CANONICAL_URL}
        self.raw = {"index.html": b"<!doctype html><a href='explorer/explore/'>Explorer</a>\n",
            "router.js": b"// synthetic bounded route fixture\n", "GIS-LICENCE": b"MIT\n",
            "explorer/index.html": b"<!doctype html><title>Synthetic Explorer home</title>\n",
            "explorer/explore/index.html": b"<!doctype html><title>Synthetic Explorer reader</title>\n",
            "legacy/index.html": b"<!doctype html><title>Synthetic legacy catalogue</title>\n",
            "catalogue/.explorer-generated": b"gis-ai-go-public-explorer-data.v1\n",
            "catalogue/record.json": b'{"id":"synthetic"}\n',
            "legacy/catalogue/.explorer-generated": b"gis-ai-go-public-explorer-data.v1\n",
            "legacy/catalogue/record.json": b'{"id":"synthetic"}\n'}
        materials = [{"path": path.removeprefix("explorer/"), "bytes": len(raw), "sha256": sha(raw)}
            for path, raw in sorted(self.raw.items()) if path.startswith("explorer/")]
        tree = sha((json.dumps(materials, separators=(",", ":")) + "\n").encode())
        app_manifest = {"schema": "okf-explorer-app-build-manifest.v1", "algorithm": "sha256-canonical-json-materials-v1",
            "file_count": len(materials), "tree_sha256": tree, "materials": materials}
        self.raw["explorer/okf-explorer-build-manifest.json"] = (json.dumps(app_manifest, indent=2) + "\n").encode()
        self.raw["gis/explorer/context/manifest.json"] = canonical({"schema": "okf-context-corpus.v3", "semantic_source_snapshot": "synthetic-1", "extensions": {"inputRevision": self.source, "inputDigest": "c" * 64}, "bundle": {"snapshot": "synthetic-1", "source_url": verify.CANONICAL_URL + "gis/explorer/context/manifest.json"}})
        self.raw["gis/explorer/okf-explorer.json"] = canonical({"schema": "okf-explorer-large-corpus.v1", "snapshot": "synthetic-1", "source": {"revision": self.source, "inputDigest": "c" * 64}})
        projection = {"schema": "gis-ai-go.okf-plus-explorer-projection.v1", "sourceRevision": self.source, "inputDigest": "c" * 64, "snapshot": "synthetic-1",
            "outputs": [{"path": path.removeprefix("gis/explorer/"), "bytes": len(raw), "sha256": sha(raw)}
                for path, raw in sorted(self.raw.items()) if path.startswith("gis/explorer/")]}
        self.raw["gis/explorer/projection-manifest.json"] = canonical(projection)
        self.app = {"sourceCommit": "b" * 40, "treeSha256": tree,
            "manifestSha256": sha(self.raw["explorer/okf-explorer-build-manifest.json"]),
            "path": "explorer/okf-explorer-build-manifest.json"}
        self.okf = {"sourceRevision": self.source, "inputDigest": "c" * 64, "snapshot": "synthetic-1",
            "descriptorPath": "gis/explorer/okf-explorer.json", "contextManifestPath": "gis/explorer/context/manifest.json"}
        self.pin = self.root / "publication-pin.json"
        self.pin.write_bytes(canonical({"sourceCommit": self.app["sourceCommit"], "appTreeSha256": tree,
            "appManifestSha256": self.app["manifestSha256"], "canonicalUrl": verify.CANONICAL_URL, "basePath": verify.BASE_PATH}))
        self.pin_patch = mock.patch.object(package, "PIN_PATH", self.pin)
        self.pin_patch.start()
        self.write_distribution()

    def tearDown(self):
        self.pin_patch.stop()
        self.temporary.cleanup()

    def write_distribution(self):
        for path, raw in self.raw.items():
            target = self.dist / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        distribution = {"schema": "gis-ai-go.explorer-distribution.v1", **self.identity,
            "app": self.app, "okf": self.okf,
            "files": [{"path": path, "bytes": len(raw), "sha256": sha(raw)} for path, raw in sorted(self.raw.items())]}
        (self.dist / verify.DISTRIBUTION).write_bytes(canonical(distribution))

    def build(self, name="archive"):
        output = self.root / name
        receipt = package.build_archive(dist=self.dist, output_dir=output, source_commit=self.source,
            repository=verify.REPOSITORY, version=self.version, base_path=verify.BASE_PATH)
        return output, receipt

    def verify_arguments(self, output, receipt):
        return {"archive_path": output / "artifact.tar", "checksum_path": output / "artifact.tar.sha256",
            "receipt_path": output / "archive-receipt.json", "expected_source_commit": self.source,
            "expected_repository": verify.REPOSITORY, "expected_version": self.version,
            "expected_base_path": verify.BASE_PATH, "expected_archive_sha256": receipt["archive"]["sha256"]}

    def rebind_transport(self, output, receipt, raw):
        """Authenticate malformed bytes so tests exercise the independent parser."""
        (output / "artifact.tar").write_bytes(raw)
        receipt["archive"]["sha256"] = sha(raw)
        receipt["archive"]["bytes"] = len(raw)
        checksum = f"{sha(raw)}  artifact.tar\n".encode()
        (output / "artifact.tar.sha256").write_bytes(checksum)
        receipt["checksum"]["sha256"] = sha(checksum)
        (output / "archive-receipt.json").write_bytes(canonical(receipt))

    def test_deterministic_archive_independent_verification_and_exact_streamed_staging(self):
        first, receipt = self.build()
        second, other = self.build("second")
        self.assertEqual(receipt, other)
        self.assertEqual((first / "artifact.tar").read_bytes(), (second / "artifact.tar").read_bytes())
        self.assertEqual(verify.verify_archive(**self.verify_arguments(first, receipt)), receipt)
        result = verify.stage_payload(**self.verify_arguments(first, receipt), output_dir=self.root / "staged")
        self.assertEqual(result["payloadRootSha256"], receipt["payloadRootSha256"])
        for path, raw in self.raw.items():
            self.assertEqual((self.root / "staged" / path).read_bytes(), raw)
        self.assertEqual((self.root / "staged" / ".nojekyll").read_bytes(), b"")
        self.assertFalse((self.root / "staged" / "archive-receipt.json").exists())

    def test_existing_wrappers_dispatch_v2_before_the_legacy_archive_ceiling(self):
        output, receipt = self.build()
        legacy_verify = load_script("verify_pages_archive")
        with mock.patch.object(legacy_verify, "MAX_ARCHIVE_BYTES", 1):
            self.assertEqual(legacy_verify.verify_archive(**self.verify_arguments(output, receipt)), receipt)
        with mock.patch.dict(sys.modules, {"verify_pages_archive": legacy_verify}):
            legacy_stage = load_script("stage_pages_payload")
        with mock.patch.object(legacy_verify, "MAX_ARCHIVE_BYTES", 1):
            result = legacy_stage.stage_payload(**self.verify_arguments(output, receipt), output_dir=self.root / "staged")
        self.assertGreater(result["fileCount"], 1)

    def test_unlisted_or_modified_payload_fails_before_output_is_published(self):
        for relative in ("explorer/index.html", "explorer/unlisted.js"):
            with self.subTest(relative=relative):
                target = self.dist / relative
                original = target.read_bytes() if target.exists() else None
                target.write_bytes(b"changed")
                with self.assertRaisesRegex(ValueError, "inventory"):
                    self.build()
                self.assertFalse((self.root / "archive").exists())
                if original is None:
                    target.unlink()
                else:
                    target.write_bytes(original)

    def test_rehashed_distribution_cannot_hide_modified_app_or_incomplete_projection(self):
        self.raw["explorer/index.html"] = b"changed app"
        self.write_distribution()
        with self.assertRaisesRegex(ValueError, "app material"):
            self.build()
        self.raw["explorer/index.html"] = b"<!doctype html><title>Synthetic Explorer home</title>\n"
        self.raw["gis/explorer/unbound.json"] = b"{}\n"
        self.write_distribution()
        with self.assertRaisesRegex(ValueError, "projection file closure"):
            self.build()

    def test_wrong_context_origin_and_legacy_direct_bytes_are_rejected(self):
        original = self.raw["gis/explorer/context/manifest.json"]
        invalid_context = json.loads(original)
        invalid_context["bundle"]["source_url"] = "http://127.0.0.1:8130/gis/explorer/context/manifest.json"
        self.raw["gis/explorer/context/manifest.json"] = canonical(invalid_context)
        self.write_distribution()
        with self.assertRaisesRegex(ValueError, "canonical publication"):
            self.build()
        self.raw["gis/explorer/context/manifest.json"] = original
        self.raw["catalogue/record.json"] = b"different direct bytes"
        self.write_distribution()
        with self.assertRaisesRegex(ValueError, "legacy direct"):
            self.build()

    def test_links_special_files_and_unsafe_paths_are_rejected(self):
        target = self.dist / "router.js"
        target.unlink()
        target.symlink_to(self.dist / "index.html")
        with self.assertRaisesRegex(ValueError, "single-link"):
            self.build()
        target.unlink()
        os.link(self.dist / "index.html", target)
        with self.assertRaisesRegex(ValueError, "single-link"):
            self.build()
        target.unlink()
        for value in ("../escape", "explorer/../private/key", "explorer/.env", "explorer/node_modules/a", "explorer/research/a", "publication/unexpected.json", "explorer/a\nb", "explorer/a\rb", "explorer/a\tb", "explorer/a\x7fb"):
            with self.subTest(path=value), self.assertRaises(ValueError):
                verify.safe_path(value)

    def test_file_total_and_metadata_budgets_are_enforced(self):
        for name, ceiling in (("MAX_FILE_BYTES", 4), ("MAX_TOTAL_BYTES", 100), ("MAX_RETAINED_METADATA_BYTES", 10)):
            with self.subTest(name=name), mock.patch.object(verify, name, ceiling), self.assertRaises(ValueError):
                self.build()

    def test_archive_or_receipt_tampering_is_rejected(self):
        output, receipt = self.build()
        archive = output / "artifact.tar"
        original = archive.read_bytes()
        archive.write_bytes(original + b"unverified trailer")
        with self.assertRaisesRegex(ValueError, "digest/checksum"):
            verify.verify_archive(**self.verify_arguments(output, receipt))
        archive.write_bytes(original)
        altered = dict(receipt)
        altered["payloadRootSha256"] = "d" * 64
        (output / "archive-receipt.json").write_bytes(canonical(altered))
        with self.assertRaisesRegex(ValueError, "payload root"):
            verify.verify_archive(**self.verify_arguments(output, receipt))

    def test_canonical_tar_headers_and_trailer_are_checked_independently(self):
        output, receipt = self.build()
        original = (output / "artifact.tar").read_bytes()
        # Recompute outer identity to show header validation is independent of it.
        modified = bytearray(original)
        modified[265] = ord("x")
        modified[148:156] = b"        "
        modified[148:156] = f"{sum(modified[:512]):06o}\0 ".encode()
        (output / "artifact.tar").write_bytes(modified)
        receipt["archive"]["sha256"] = sha(modified)
        checksum = f"{sha(modified)}  artifact.tar\n".encode()
        (output / "artifact.tar.sha256").write_bytes(checksum)
        receipt["checksum"]["sha256"] = sha(checksum)
        (output / "archive-receipt.json").write_bytes(canonical(receipt))
        with self.assertRaisesRegex(ValueError, "normalised|canonical"):
            verify.verify_archive(**self.verify_arguments(output, receipt))

    def test_trailing_bytes_zero_records_and_truncated_trailers_fail_even_with_new_outer_digests(self):
        output, receipt = self.build()
        original = (output / "artifact.tar").read_bytes()
        cases = (original + b"unverified", original + b"\0" * 10_240, original[:-512], original[:-1] + b"x")
        for raw in cases:
            with self.subTest(bytes=len(raw)):
                self.rebind_transport(output, receipt, raw)
                with self.assertRaisesRegex(ValueError, "trailer"):
                    verify.verify_archive(**self.verify_arguments(output, receipt))

    def test_gnu_extension_and_symbolic_members_cannot_hide_behind_regular_payload(self):
        output, receipt = self.build()
        for symbolic in (False, True):
            with self.subTest(symbolic=symbolic):
                buffer = io.BytesIO()
                with tarfile.open(fileobj=buffer, mode="w", format=tarfile.GNU_FORMAT) as archive:
                    member = tarfile.TarInfo("./explorer/" + "a" * 120)
                    member.uid = member.gid = 1000
                    member.mode = 0o644
                    if symbolic:
                        member.type = tarfile.SYMTYPE
                        member.linkname = "../../private"
                        archive.addfile(member)
                    else:
                        member.size = 1
                        archive.addfile(member, io.BytesIO(b"x"))
                self.rebind_transport(output, receipt, buffer.getvalue())
                with self.assertRaisesRegex(ValueError, "extension|normalised|canonical"):
                    verify.verify_archive(**self.verify_arguments(output, receipt))

    def test_staging_rechecks_bytes_after_copy(self):
        output, receipt = self.build()
        destination = self.root / "staged"
        original_reader = verify._read_members
        def corrupt_after_copy(path, consumer=None):
            result = original_reader(path, consumer)
            if consumer is not None:
                (destination / "router.js").write_bytes(b"changed during staging")
            return result
        with mock.patch.object(verify, "_read_members", side_effect=corrupt_after_copy), self.assertRaisesRegex(ValueError, "staged inventory|replaced file"):
            verify.stage_payload(**self.verify_arguments(output, receipt), output_dir=destination)

    def test_pin_and_archive_member_count_are_bounded(self):
        pin = json.loads(self.pin.read_bytes())
        pin["sourceCommit"] = "e" * 40
        self.pin.write_bytes(canonical(pin))
        with self.assertRaisesRegex(ValueError, "publication pin"):
            self.build()
        pin["sourceCommit"] = self.app["sourceCommit"]
        self.pin.write_bytes(canonical(pin))
        with mock.patch.object(verify, "MAX_FILES", 5), self.assertRaises(ValueError):
            self.build()

    def test_member_ceiling_includes_the_six_fixed_publication_files(self):
        self.assertEqual(verify.MAX_FILES, 50_000)
        expected_members = len(self.raw) + 1 + 6  # Distribution manifest, then fixed files.
        with mock.patch.object(verify, "MAX_FILES", expected_members):
            output, receipt = self.build("at-boundary")
            rows, _ = verify._read_members(output / "artifact.tar")
            self.assertEqual(len(rows), expected_members)
            self.assertEqual(verify.verify_archive(**self.verify_arguments(output, receipt)), receipt)
        with mock.patch.object(verify, "MAX_FILES", expected_members - 1), self.assertRaises(ValueError):
            self.build("over-boundary")

    def test_component_schemas_and_context_producer_identity_are_required(self):
        cases = (("gis/explorer/okf-explorer.json", "schema", "unknown"),
            ("gis/explorer/context/manifest.json", "schema", "unknown"),
            ("gis/explorer/projection-manifest.json", "schema", "unknown"),
            ("gis/explorer/context/manifest.json", "semantic_source_snapshot", "different"),
            ("gis/explorer/context/manifest.json", "extensions", {"inputRevision": "e" * 40, "inputDigest": "c" * 64}))
        for path, key, value in cases:
            with self.subTest(path=path, key=key):
                original = self.raw[path]
                altered = json.loads(original)
                altered[key] = value
                self.raw[path] = canonical(altered)
                self.write_distribution()
                with self.assertRaisesRegex(ValueError, "schema|snapshot|producer input identity"):
                    self.build()
                self.raw[path] = original

    def test_json_rejects_non_standard_numbers_like_the_browser_parser(self):
        for value in (b'{"value":NaN}', b'{"value":Infinity}', b'{"value":-Infinity}'):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "valid UTF-8 JSON"):
                verify.json_bytes(value, "public metadata", canonical=False)

    def test_archive_publication_cannot_follow_a_replaced_output_directory(self):
        output = self.root / "archive"
        victim = self.root / "victim"
        victim.mkdir()
        (victim / "artifact.tar").write_bytes(b"personal file must survive")
        original_link = os.link
        triggered = False
        def replace_output(*args, **kwargs):
            nonlocal triggered
            if not triggered:
                triggered = True
                output.rmdir()
                output.symlink_to(victim, target_is_directory=True)
            return original_link(*args, **kwargs)
        with mock.patch.object(package.os, "link", side_effect=replace_output), self.assertRaises((ValueError, OSError)):
            self.build()
        self.assertTrue(triggered)
        self.assertEqual((victim / "artifact.tar").read_bytes(), b"personal file must survive")
        self.assertEqual(sorted(path.name for path in victim.iterdir()), ["artifact.tar"])

    def test_archive_publication_refuses_a_file_that_appears_in_the_pinned_output(self):
        output = self.root / "archive"
        original_link = os.link
        triggered = False
        def inject_file(*args, **kwargs):
            nonlocal triggered
            if not triggered:
                triggered = True
                (output / "artifact.tar").write_bytes(b"new personal file")
            return original_link(*args, **kwargs)
        with mock.patch.object(package.os, "link", side_effect=inject_file), self.assertRaises(FileExistsError):
            self.build()
        self.assertEqual((output / "artifact.tar").read_bytes(), b"new personal file")

    def test_archive_publication_detects_a_replaced_output_parent(self):
        parent = self.root / "publication-parent"
        parent.mkdir()
        victim = self.root / "victim-parent"
        victim.mkdir()
        moved = self.root / "original-parent"
        output = parent / "archive"
        original_link = os.link
        triggered = False
        def replace_parent(*args, **kwargs):
            nonlocal triggered
            if not triggered:
                triggered = True
                parent.rename(moved)
                parent.symlink_to(victim, target_is_directory=True)
            return original_link(*args, **kwargs)
        try:
            with mock.patch.object(package.os, "link", side_effect=replace_parent), self.assertRaisesRegex(ValueError, "directory changed"):
                package.build_archive(dist=self.dist, output_dir=output, source_commit=self.source, repository=verify.REPOSITORY, version=self.version, base_path=verify.BASE_PATH)
            self.assertEqual(list(victim.iterdir()), [])
        finally:
            if triggered:
                parent.unlink()
                moved.rename(parent)

    def test_staging_refuses_existing_directory_and_symbolic_parent(self):
        output, receipt = self.build()
        existing = self.root / "existing"
        existing.mkdir()
        (existing / "personal-note").write_text("retain")
        with self.assertRaisesRegex(ValueError, "must not already exist"):
            verify.stage_payload(**self.verify_arguments(output, receipt), output_dir=existing)
        self.assertEqual((existing / "personal-note").read_text(), "retain")
        linked = self.root / "linked"
        linked.symlink_to(existing, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "real directory"):
            verify.stage_payload(**self.verify_arguments(output, receipt), output_dir=linked / "site")


if __name__ == "__main__":
    unittest.main()
