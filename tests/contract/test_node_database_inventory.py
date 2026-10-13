from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import node_runtime_advisory as node  # noqa: E402
from gateway_image import MAX_GRYPE_DB_EXPANDED_BYTES  # noqa: E402


class NodeDatabaseInventoryTests(unittest.TestCase):
    def make_cache(self, root: Path) -> Path:
        cache = root / "cache"
        (cache / "6").mkdir(parents=True)
        (cache / "6/import.json").write_bytes(b"{}")
        (cache / "6/vulnerability.db").write_bytes(b"synthetic database")
        return cache

    def assert_rejected_before_hashing(self, cache: Path, stage: str):
        with (mock.patch.object(node, "sha256_file") as digest,
              self.assertRaises(node.NodeAdvisoryFailure) as raised):
            node.database_inventory(cache)
        self.assertEqual(raised.exception.stage, stage)
        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)
        digest.assert_not_called()
        return raised.exception

    def test_exact_inventory_retains_sorted_paths_sizes_and_real_hashes(self):
        with tempfile.TemporaryDirectory() as temporary:
            cache = self.make_cache(Path(temporary))
            expected = [
                {"path": path, "bytes": len(content),
                 "sha256": hashlib.sha256(content).hexdigest()}
                for path, content in (
                    ("6/import.json", b"{}"),
                    ("6/vulnerability.db", b"synthetic database"),
                )
            ]
            inventory = node.database_inventory(cache)
            self.assertEqual(inventory, expected)
            self.assertEqual(
                node._database_inventory_shape(inventory, label="synthetic inventory"),
                [{"path": item["path"], "bytes": item["bytes"]} for item in expected],
            )

    def test_missing_root_directory_or_required_file_is_classified(self):
        for relative in ("", "6", "6/import.json", "6/vulnerability.db"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temporary:
                cache = self.make_cache(Path(temporary))
                missing = cache / relative
                if missing.is_dir():
                    shutil.rmtree(missing)
                else:
                    missing.unlink()
                self.assert_rejected_before_hashing(cache, "node-db-inventory-missing")

    def test_required_directories_must_be_real_directories(self):
        for relative in ("", "6"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temporary:
                cache = self.make_cache(Path(temporary))
                path = cache / relative
                shutil.rmtree(path)
                path.write_bytes(b"synthetic wrong type")
                self.assert_rejected_before_hashing(cache, "node-db-inventory-type")

    def test_required_files_cannot_be_directories(self):
        for relative in ("6/import.json", "6/vulnerability.db"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temporary:
                cache = self.make_cache(Path(temporary))
                path = cache / relative
                path.unlink()
                path.mkdir()
                self.assert_rejected_before_hashing(cache, "node-db-inventory-type")

    def test_root_version_directory_and_files_cannot_be_symlinks(self):
        for relative in ("", "6", "6/import.json", "6/vulnerability.db"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                cache = self.make_cache(root)
                path = cache / relative
                target = root / "preserved-target"
                path.rename(target)
                path.symlink_to(target, target_is_directory=target.is_dir())
                self.assert_rejected_before_hashing(cache, "node-db-inventory-type")
                self.assertTrue(target.exists())

    def test_broken_required_symlink_is_a_type_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            cache = self.make_cache(Path(temporary))
            path = cache / "6/vulnerability.db"
            path.unlink()
            path.symlink_to("missing-target")
            self.assert_rejected_before_hashing(cache, "node-db-inventory-type")

    def test_required_fifo_is_rejected_without_reading_or_hashing(self):
        for relative in ("6/import.json", "6/vulnerability.db"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temporary:
                cache = self.make_cache(Path(temporary))
                path = cache / relative
                path.unlink()
                os.mkfifo(path)
                self.assert_rejected_before_hashing(cache, "node-db-inventory-type")

    def test_required_socket_is_rejected_without_reading_or_hashing(self):
        with tempfile.TemporaryDirectory() as temporary:
            cache = self.make_cache(Path(temporary))
            path = cache / "6/vulnerability.db"
            path.unlink()
            # A socket inode exercises file-type validation without opening a listener.
            os.mknod(path, stat.S_IFSOCK | 0o600)
            self.assert_rejected_before_hashing(cache, "node-db-inventory-type")

    def test_zero_length_required_files_are_rejected_before_any_hash(self):
        for relative in ("6/import.json", "6/vulnerability.db"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temporary:
                cache = self.make_cache(Path(temporary))
                (cache / relative).write_bytes(b"")
                self.assert_rejected_before_hashing(cache, "node-db-inventory-zero-length")

    def test_unexpected_regular_files_and_empty_directories_are_rejected(self):
        for relative in ("unexpected", "6/unexpected"):
            for kind in ("file", "directory"):
                with self.subTest(relative=relative, kind=kind), tempfile.TemporaryDirectory() as temporary:
                    cache = self.make_cache(Path(temporary))
                    path = cache / relative
                    if kind == "directory":
                        path.mkdir()
                    else:
                        path.write_bytes(b"synthetic extra file")
                    self.assert_rejected_before_hashing(cache, "node-db-inventory-unexpected-entry")

    def test_unexpected_fifo_socket_and_symlink_are_rejected_before_hashing(self):
        for kind in ("fifo", "socket", "symlink"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                cache = self.make_cache(Path(temporary))
                path = cache / "6/unexpected"
                if kind == "fifo":
                    os.mkfifo(path)
                elif kind == "socket":
                    os.mknod(path, stat.S_IFSOCK | 0o600)
                else:
                    path.symlink_to("vulnerability.db")
                self.assert_rejected_before_hashing(cache, "node-db-inventory-type")

    def test_untrusted_extra_filename_does_not_reach_the_diagnostic(self):
        with tempfile.TemporaryDirectory() as temporary:
            cache = self.make_cache(Path(temporary))
            marker = "Bearer SYNTHETIC-DO-NOT-EXPOSE"
            (cache / "6" / marker).write_bytes(b"synthetic extra file")
            error = self.assert_rejected_before_hashing(cache, "node-db-inventory-unexpected-entry")
            self.assertNotIn(marker, str(error))
            self.assertNotIn(temporary, str(error))

    def test_exact_aggregate_bound_is_accepted_without_reading_sparse_database(self):
        with tempfile.TemporaryDirectory() as temporary:
            cache = self.make_cache(Path(temporary))
            database_bytes = node.MAX_GRYPE_DB_EXPANDED_BYTES - 2
            with (cache / "6/vulnerability.db").open("wb") as stream:
                stream.truncate(database_bytes)
            with mock.patch.object(node, "sha256_file", side_effect=["a" * 64, "b" * 64]) as digest:
                inventory = node.database_inventory(cache)
            self.assertEqual([item["bytes"] for item in inventory], [2, database_bytes])
            self.assertEqual(digest.call_args_list,
                             [mock.call(cache / "6/import.json"),
                              mock.call(cache / "6/vulnerability.db")])
            node._database_inventory_shape(inventory, label="synthetic exact-bound inventory")

    def test_observed_database_size_passes_inventory_shape_and_real_schema(self):
        schema = json.loads(
            (ROOT / "schemas/gateway-image-vulnerability-scan.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(MAX_GRYPE_DB_EXPANDED_BYTES, 4 * 1024 * 1024 * 1024)
        self.assertEqual(node.MAX_GRYPE_DB_EXPANDED_BYTES, MAX_GRYPE_DB_EXPANDED_BYTES)
        self.assertEqual(
            schema["$defs"]["grypeDatabaseFile"]["properties"]["bytes"]["maximum"],
            MAX_GRYPE_DB_EXPANDED_BYTES,
        )
        # Retain the schema's local SHA-256 reference without a remote resolver.
        validator = Draft202012Validator({
            "$ref": "#/$defs/grypeDatabaseFile", "$defs": schema["$defs"],
        })
        with tempfile.TemporaryDirectory() as temporary:
            cache = self.make_cache(Path(temporary))
            (cache / "6/import.json").write_bytes(b"m" * 97)
            with (cache / "6/vulnerability.db").open("wb") as stream:
                stream.truncate(3_239_141_376)
            with mock.patch.object(node, "sha256_file", side_effect=["a" * 64, "b" * 64]):
                inventory = node.database_inventory(cache)
            self.assertEqual(sum(item["bytes"] for item in inventory), 3_239_141_473)
            self.assertEqual(
                node._database_inventory_shape(inventory, label="observed-size fixture"),
                [{"path": "6/import.json", "bytes": 97},
                 {"path": "6/vulnerability.db", "bytes": 3_239_141_376}],
            )
            for item in inventory:
                validator.validate(item)
            oversized_item = {
                **inventory[1], "bytes": MAX_GRYPE_DB_EXPANDED_BYTES + 1,
            }
            with self.assertRaises(ValidationError):
                validator.validate(oversized_item)

    def test_one_byte_over_aggregate_bound_fails_before_hash_and_reports_only_sizes(self):
        with tempfile.TemporaryDirectory() as temporary:
            cache = self.make_cache(Path(temporary))
            database_bytes = node.MAX_GRYPE_DB_EXPANDED_BYTES - 1
            with (cache / "6/vulnerability.db").open("wb") as stream:
                stream.truncate(database_bytes)
            error = self.assert_rejected_before_hashing(cache, "node-db-inventory-expanded-bound")
            self.assertEqual(error.inventory_sizes, {
                "metadata_bytes": 2,
                "database_bytes": database_bytes,
                "expanded_bytes": node.MAX_GRYPE_DB_EXPANDED_BYTES + 1,
                "maximum_bytes": 4 * 1024 * 1024 * 1024,
            })
            for value in error.inventory_sizes.values():
                self.assertIs(type(value), int)
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 2**63 - 1)
            self.assertNotIn(temporary, str(error))
            retained_inventory = [
                {"path": "6/import.json", "sha256": "a" * 64, "bytes": 2},
                {"path": "6/vulnerability.db", "sha256": "b" * 64,
                 "bytes": database_bytes},
            ]
            for item in retained_inventory:
                self.assertLessEqual(item["bytes"], MAX_GRYPE_DB_EXPANDED_BYTES)
            with self.assertRaisesRegex(ValueError, "exceeds its expanded bound"):
                node._database_inventory_shape(
                    retained_inventory, label="synthetic aggregate-overflow inventory"
                )

    def test_oversized_metadata_is_included_in_aggregate_before_hashing(self):
        with tempfile.TemporaryDirectory() as temporary:
            cache = self.make_cache(Path(temporary))
            with (cache / "6/import.json").open("wb") as stream:
                stream.truncate(node.MAX_GRYPE_DB_EXPANDED_BYTES)
            error = self.assert_rejected_before_hashing(cache, "node-db-inventory-expanded-bound")
            self.assertEqual(error.inventory_sizes["metadata_bytes"], node.MAX_GRYPE_DB_EXPANDED_BYTES)
            self.assertEqual(error.inventory_sizes["database_bytes"], len(b"synthetic database"))
            self.assertEqual(error.inventory_sizes["expanded_bytes"],
                             node.MAX_GRYPE_DB_EXPANDED_BYTES + len(b"synthetic database"))

    def test_lstat_read_failures_are_detached_and_never_stringified(self):
        class UnrenderableReadFailure(OSError):
            def __str__(self):
                raise AssertionError("untrusted read failure must not be rendered")

        original = Path.lstat
        for relative in ("", "6", "6/import.json", "6/vulnerability.db"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temporary:
                cache = self.make_cache(Path(temporary))
                failed = cache / relative

                def lstat(path, *args, **kwargs):
                    if path == failed:
                        raise UnrenderableReadFailure()
                    return original(path, *args, **kwargs)

                with mock.patch.object(Path, "lstat", lstat):
                    self.assert_rejected_before_hashing(cache, "node-db-inventory-read")

    def test_hash_read_failures_are_detached_and_do_not_expose_paths(self):
        marker = "Bearer SYNTHETIC-HASH-FAILURE"
        for failed_call in (0, 1):
            with self.subTest(failed_call=failed_call), tempfile.TemporaryDirectory() as temporary:
                cache = self.make_cache(Path(temporary))
                outcomes = ["a" * 64, "b" * 64]
                outcomes[failed_call] = OSError(marker + " " + temporary)
                with (mock.patch.object(node, "sha256_file", side_effect=outcomes) as digest,
                      self.assertRaises(node.NodeAdvisoryFailure) as raised):
                    node.database_inventory(cache)
                self.assertEqual(raised.exception.stage, "node-db-inventory-read")
                self.assertEqual(digest.call_count, failed_call + 1)
                self.assertIsNone(raised.exception.__cause__)
                self.assertIsNone(raised.exception.__context__)
                self.assertNotIn(marker, str(raised.exception))
                self.assertNotIn(temporary, str(raised.exception))


if __name__ == "__main__":
    unittest.main()
