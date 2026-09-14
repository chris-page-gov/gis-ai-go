"""Small fixture tests for local storage mechanics, not benchmark results."""

from __future__ import annotations

import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import web216_storage_experiment as storage
from scripts.web216_corpus import canonical, digest, identity, load_corpus
from scripts.web216_experiments import build, rank


class StorageExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = load_corpus(storage.ROOT / "tests/fixtures/web216/story-corpus.json")
        cls.cases = json.loads(storage.CASES.read_bytes())

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_layouts_reconstruct_exact_records_and_identical_five_query_ids(self):
        original = digest(self.records)
        result = storage.run_experiment(self.records, self.cases, self.root / "run", repeats=1)
        self.assertEqual(digest(self.records), original)
        self.assertEqual(result["record_count"], 7)
        self.assertFalse(result["optimality_claimed"])
        self.assertEqual(result["provider_requests"], 0)
        self.assertEqual(result["sites_or_d1_requests"], 0)
        self.assertIsNone(result["hosting_cost"])
        expected = [{"case_id": case["id"], "ranked_ids": [row["id"] for row in rank(
            build(self.records), case["query"], concepts=case.get("concepts"), source_id=case.get("source_id"))]}
            for case in self.cases]
        for name, arm in result["arms"].items():
            with self.subTest(layout=name):
                self.assertTrue(arm["records_equal"])
                self.assertEqual(arm["query_results"], expected)
                self.assertEqual(arm["logical_records_sha256"], digest(sorted(self.records, key=identity)))
                self.assertEqual(len(arm["detail_samples"]), 5)
                self.assertEqual(arm["persisted_bytes"], sum(row["bytes"] for row in arm["files"]))
                for row in arm["files"]:
                    raw = (self.root / "run" / row["path"]).read_bytes()
                    self.assertEqual(len(raw), row["bytes"])
                    self.assertEqual(hashlib.sha256(raw).hexdigest(), row["sha256"])
        self.assertIsNone(result["arms"]["sqlite"]["initial_application_payload_bytes"])
        self.assertLess(result["arms"]["partitions"]["initial_application_payload_bytes"],
                        result["arms"]["static"]["initial_application_payload_bytes"])
        self.assertEqual(result["result_sha256"], digest(
            {key: value for key, value in result.items() if key != "result_sha256"}))
        self.assertEqual(result["code_file_sha256"], {
            f"scripts/{name}": hashlib.sha256((storage.ROOT / "scripts" / name).read_bytes()).hexdigest()
            for name in ("web216_storage_experiment.py", "web216_experiments.py", "web216_corpus.py")})
        self.assertEqual(json.loads((self.root / "run/result.json").read_bytes()), result)

    def test_indexed_detail_lookup_and_unknown_identifier(self):
        ordered = sorted(self.records, key=identity)
        storage.write_layouts(ordered, self.root)
        for name, reader_class in storage.READERS.items():
            reader = reader_class(self.root / name)
            try:
                for record in ordered:
                    self.assertEqual(canonical(reader.lookup(identity(record))), canonical(record))
                self.assertIsNone(reader.lookup("ons-data-api:UNKNOWN"))
                self.assertIsNone(reader.lookup("'; DROP TABLE metadata; --"))
                with self.assertRaises(ValueError):
                    reader.lookup("x" * 257)
                if name == "sqlite":
                    plan = reader.connection.execute("EXPLAIN QUERY PLAN " + storage.JOIN + " WHERE m.id=?",
                                                     (identity(ordered[0]),)).fetchall()
                    self.assertTrue(all("SEARCH" in row[3] and "PRIMARY KEY" in row[3] for row in plan))
                if name == "partitions":
                    count = reader.bytes_read
                    reader.lookup(identity(ordered[0]))
                    self.assertEqual(reader.bytes_read, count)
            finally:
                reader.close()

    def test_missing_optional_source_fields_are_preserved_in_sqlite_roundtrip(self):
        records = copy.deepcopy(self.records)
        records[0].pop("keywords", None)
        records[0].pop("description", None)
        storage.write_layouts(records, self.root)
        reader = storage.SqliteReader(self.root / "sqlite")
        try:
            reconstructed = reader.lookup(identity(records[0]))
            self.assertEqual(reconstructed, records[0])
            self.assertNotIn("keywords", reconstructed)
            self.assertNotIn("description", reconstructed)
        finally:
            reader.close()

    def test_partitions_are_deterministic_and_tampering_is_detected(self):
        left, right = self.root / "left", self.root / "right"
        left.mkdir()
        right.mkdir()
        storage.write_layouts(self.records, left)
        storage.write_layouts(list(reversed(self.records)), right)
        for path in (left / "partitions").iterdir():
            self.assertEqual(path.read_bytes(), (right / "partitions" / path.name).read_bytes())
        key = identity(self.records[0])
        path = left / "partitions" / f"{storage._prefix(key)}.json"
        path.write_bytes(path.read_bytes() + b" ")
        reader = storage.PartitionReader(left / "partitions")
        try:
            with self.assertRaisesRegex(ValueError, "partition hash"):
                reader.lookup(key)
        finally:
            reader.close()

    def test_duplicate_ids_and_excessive_repetitions_fail_before_output(self):
        output = self.root / "run"
        with self.assertRaisesRegex(ValueError, "Duplicate source"):
            storage.run_experiment([*self.records, self.records[0]], self.cases, output, repeats=1)
        self.assertFalse(output.exists())
        for repeats in (0, 4, True):
            with self.subTest(repeats=repeats), self.assertRaisesRegex(ValueError, "repetitions"):
                storage.run_experiment(self.records, self.cases, output, repeats=repeats)
        self.assertFalse(output.exists())

    def test_existing_output_and_wrong_cli_corpus_are_never_overwritten(self):
        self.root.joinpath("sentinel").write_text("preserved")
        with self.assertRaises(FileExistsError):
            storage.run_experiment(self.records, self.cases, self.root, repeats=1)
        self.assertEqual((self.root / "sentinel").read_text(), "preserved")
        output = self.root / "cli-output"
        args = ["web216_storage_experiment.py", "--corpus",
                str(storage.ROOT / "tests/fixtures/web216/story-corpus.json"), "--output", str(output)]
        with patch("sys.argv", args), patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit):
            storage.main()
        self.assertFalse(output.exists())

    def test_corpus_reads_are_bounded_before_validation(self):
        class CountingStream(io.BytesIO):
            requested = []

            def read(self, size=-1):
                self.requested.append(size)
                return super().read(size)

        raw = CountingStream(b"x" * (storage.MAX_CORPUS_BYTES + 2))
        output = self.root / "oversized-run"
        args = ["web216_storage_experiment.py", "--corpus", "oversized.json", "--output", str(output)]
        with patch("sys.argv", args), patch.object(Path, "open", return_value=raw), \
                patch.object(storage, "load_corpus") as loader, \
                patch("sys.stderr", new_callable=io.StringIO) as error, self.assertRaises(SystemExit):
            storage.main()
        self.assertIn("byte limit", error.getvalue())
        self.assertEqual(raw.requested, [storage.MAX_CORPUS_BYTES + 1])
        loader.assert_not_called()
        self.assertFalse(output.exists())
        with patch.object(storage, "MAX_CORPUS_BYTES", 3), \
                patch.object(Path, "open", return_value=io.BytesIO(b"abc")):
            self.assertEqual(storage._corpus_bytes(Path("small.json")), b"abc")

    def test_each_changed_source_hash_aborts_without_a_success_result(self):
        before = storage._code_hashes()
        for index, source in enumerate(before):
            after = {**before, source: "0" * 64}
            output = self.root / f"changed-source-{index}"
            with self.subTest(source=source), \
                    patch.object(storage, "_code_hashes", side_effect=[before, after]), \
                    self.assertRaisesRegex(ValueError, "source files changed"):
                storage.run_experiment(self.records, self.cases, output, repeats=1)
            self.assertTrue((output / "static/records.json").is_file())
            self.assertTrue((output / "sqlite/records.sqlite").is_file())
            self.assertTrue((output / "partitions/manifest.json").is_file())
            self.assertFalse((output / "result.json").exists())

    def test_layout_failure_preserves_partial_evidence_and_no_success_result(self):
        output = self.root / "failed-run"

        def fail_after_static(records, destination):
            (destination / "static").mkdir()
            storage._write(destination / "static/records.json", records)
            raise OSError("Synthetic layout failure")

        with patch.object(storage, "write_layouts", side_effect=fail_after_static), \
                self.assertRaisesRegex(OSError, "Synthetic layout failure"):
            storage.run_experiment(self.records, self.cases, output, repeats=1)
        retained = (output / "static/records.json").read_bytes()
        self.assertEqual(retained, canonical(sorted(self.records, key=identity)))
        self.assertFalse((output / "result.json").exists())
        with self.assertRaises(FileExistsError):
            storage.run_experiment(self.records, self.cases, output, repeats=1)
        self.assertEqual((output / "static/records.json").read_bytes(), retained)


if __name__ == "__main__":
    unittest.main()
