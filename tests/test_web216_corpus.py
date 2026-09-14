"""Portable offline checks: no source checkout or network is needed."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts import web216_corpus as corpus


FIXTURES = Path(__file__).parent / "fixtures/web216"


class Web216CorpusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "corpus.json"
        self.story = json.loads((FIXTURES / "story-corpus.json").read_bytes())

    def write(self, value: object, *, rehash: bool = False) -> Path:
        if rehash and isinstance(value, dict):
            value["corpus_sha256"] = corpus.digest(
                {key: item for key, item in value.items() if key != "corpus_sha256"}
            )
        self.path.write_bytes(corpus.canonical(value))
        return self.path

    def test_canonical_utf8_order_and_no_nan(self) -> None:
        self.assertEqual(corpus.canonical({"z": 2, "a": "café"}), b'{"a":"caf\xc3\xa9","z":2}')
        self.assertEqual(corpus.digest({"z": 2, "a": "café"}),
                         hashlib.sha256(b'{"a":"caf\xc3\xa9","z":2}').hexdigest())
        for number in (float("nan"), float("inf"), -float("inf")):
            with self.subTest(number=number), self.assertRaises(ValueError):
                corpus.canonical({"number": number})

    def test_story_has_exact_seven_native_identities(self) -> None:
        records = corpus.load_corpus(FIXTURES / "story-corpus.json")
        self.assertEqual([corpus.identity(record) for record in records], sorted({
            "ons-data-api:cpih01", "ons-data-api:TS001", "ons-data-api:TS017",
            "ons-data-api:TS052", "ons-data-api:TS053",
            "nomis-dataset-definitions:NM_2002_1", "nomis-dataset-definitions:NM_2006_1",
        }))
        self.assertEqual(self.story["source_commit"], "4aa41c71dd570ceccb661768af95c4d69f49162b")
        self.assertTrue(self.story["metadata_only"])
        self.assertFalse(self.story["upstream_snapshot_completeness_claimed"])
        rooms = next(record for record in records if record["sourceRecordId"] == "TS053")
        dimensions = {item["id"]: item for item in rooms["versionDimensions"]}
        self.assertTrue(dimensions["ltla"]["isAreaType"])
        self.assertIn("inappropriate to measure change", dimensions["occupancy_rating_rooms_6a"]
                      ["qualityStatementText"])

    def test_manifest_pins_339_records_and_two_source_blobs(self) -> None:
        manifest = json.loads((FIXTURES / "source-manifest.json").read_bytes())
        keys = manifest["scopes"]["comparison"]["record_ids"]
        self.assertEqual(len(keys), 339)
        self.assertEqual(sum(key.startswith("ons-data-api:") for key in keys), 337)
        self.assertEqual(set(keys), set(manifest["record_sha256"]))
        self.assertEqual(len(manifest["sources"]), 2)
        self.assertEqual({source["blob_sha256"] for source in manifest["sources"]},
                         {source["blob_sha256"] for source in corpus.SOURCES.values()})
        self.assertEqual(manifest["scopes"]["story"]["corpus_sha256"], self.story["corpus_sha256"])
        for source in manifest["sources"]:
            self.assertEqual(source["page_provenance"]["receipt_objects_copied"], 0)
            self.assertIn("not a per-record", source["page_provenance"]["scope"])

    def test_changed_record_rejected_before_and_after_wrapper_rehash(self) -> None:
        self.story["records"][0]["title"] += " altered"
        with self.assertRaisesRegex(ValueError, "corpus_sha256"):
            corpus.load_corpus(self.write(self.story))
        with self.assertRaisesRegex(ValueError, "source record SHA-256"):
            corpus.load_corpus(self.write(self.story, rehash=True))

    def test_duplicate_identity_rejected_even_with_fresh_wrapper_hash(self) -> None:
        self.story["records"][1] = copy.deepcopy(self.story["records"][0])
        with self.assertRaisesRegex(ValueError, "Duplicate corpus"):
            corpus.load_corpus(self.write(self.story, rehash=True))

    def test_record_order_and_missing_record_rejected(self) -> None:
        self.story["records"].reverse()
        with self.assertRaisesRegex(ValueError, "identity set or order"):
            corpus.load_corpus(self.write(self.story, rehash=True))
        self.story["records"].pop()
        with self.assertRaisesRegex(ValueError, "identity set or order"):
            corpus.load_corpus(self.write(self.story, rehash=True))

    def test_unsafe_sources_and_native_ids_rejected(self) -> None:
        for source in ("ons-explore-local-statistics", "ons-open-geography", "os", "nomis", "../ons"):
            with self.subTest(source=source), self.assertRaises(ValueError):
                corpus.identity({"sourceId": source, "sourceRecordId": "safe"})
        for native in (None, "../name", "a:b", "a/b", "", "x" * 201):
            with self.subTest(native=native), self.assertRaises(ValueError):
                corpus.identity({"sourceId": "ons-data-api", "sourceRecordId": native})
        self.story["records"][0]["sourceId"] = "os"
        with self.assertRaisesRegex(ValueError, "Unsupported metadata source"):
            corpus.load_corpus(self.write(self.story, rehash=True))

    def test_boundary_and_rights_tampering_rejected(self) -> None:
        for field, value in (("metadata_only", False), ("observations_included", True),
                             ("upstream_snapshot_completeness_claimed", True), ("rights", {})):
            changed = copy.deepcopy(self.story)
            changed[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "boundary or rights"):
                corpus.load_corpus(self.write(changed, rehash=True))

    def test_source_hash_and_wrapper_extensions_rejected(self) -> None:
        changed = copy.deepcopy(self.story)
        changed["sources"][0]["blob_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "Source manifest binding"):
            corpus.load_corpus(self.write(changed, rehash=True))
        self.story["unexpected"] = "not permitted by pinned derivative"
        with self.assertRaisesRegex(ValueError, "committed derivative manifest"):
            corpus.load_corpus(self.write(self.story, rehash=True))

    def test_json_duplicate_keys_nonfinite_numbers_and_large_input_rejected(self) -> None:
        for data in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}'):
            self.path.write_bytes(data)
            with self.subTest(data=data), self.assertRaises(ValueError):
                corpus.load_corpus(self.path)
        self.path.write_bytes(b" " * (corpus.MAX_CORPUS_BYTES + 1))
        with self.assertRaisesRegex(ValueError, "byte limit"):
            corpus.load_corpus(self.path)

    def test_manifest_digest_tampering_rejected(self) -> None:
        manifest = json.loads((FIXTURES / "source-manifest.json").read_bytes())
        manifest["source_commit"] = "0" * 40
        path = self.path.parent / "manifest.json"
        path.write_bytes(corpus.canonical(manifest))
        with patch.object(corpus, "MANIFEST_PATH", path), self.assertRaisesRegex(ValueError, "manifest_sha256"):
            corpus.load_corpus(FIXTURES / "story-corpus.json")

    def test_git_reads_exact_commit_and_disables_fetch_and_source_conversion(self) -> None:
        source = {"path": "source/pinned.json", "blob_bytes": 2,
                  "blob_sha256": hashlib.sha256(b"{}").hexdigest()}
        result = subprocess.CompletedProcess([], 0, stdout=b"{}", stderr=b"")
        with patch.object(corpus.subprocess, "run", return_value=result) as run:
            self.assertEqual(corpus._git_blob(Path("example-source"), source), b"{}")
        arguments = run.call_args.args[0]
        self.assertEqual(arguments[-1], f"{corpus.SOURCE_COMMIT}:source/pinned.json")
        for flag in ("--no-replace-objects", "--no-ext-diff", "--no-textconv"):
            self.assertIn(flag, arguments)
        self.assertEqual(run.call_args.kwargs["env"]["GIT_NO_LAZY_FETCH"], "1")
        self.assertEqual(run.call_args.kwargs["timeout"], 30)
        result.stdout = b"[]"
        with patch.object(corpus.subprocess, "run", return_value=result), self.assertRaisesRegex(ValueError, "SHA-256"):
            corpus._git_blob(Path("example-source"), source)

    def test_upstream_acquisition_digest_profile_is_distinct_from_derivative(self) -> None:
        value = {"label": "café"}
        self.assertNotEqual(corpus.digest(value), corpus._source_digest(value))
        expected = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()
        self.assertEqual(corpus._source_digest(value), hashlib.sha256(expected).hexdigest())

    def test_source_projection_validates_records_and_receipts_independently(self) -> None:
        records = [{"sourceId": "ons-data-api", "sourceRecordId": f"test-{index}", "title": "café"}
                   for index in range(337)]
        pages = [{"requestUrl": "https://example.org/public-metadata", "contentSha256": "1" * 64}]
        envelope = {
            "schemaVersion": "okf-ons.source-acquisition.v1", "records": records,
            "provenance": {"source": {"id": "ons-data-api"}, "recordCount": 337,
                           "recordSetSha256": corpus._source_digest(records), "pages": pages,
                           "snapshotSetSha256": corpus._source_digest(pages),
                           "assurance": {"metadataOnly": True, "observationsFetched": False}},
        }
        projection = corpus._source_projection("ons-data-api", envelope)
        self.assertEqual(projection["page_provenance"]["receipt_count"], 1)
        changed = copy.deepcopy(envelope)
        changed["records"][0]["title"] = "changed"
        with self.assertRaisesRegex(ValueError, "record-set binding"):
            corpus._source_projection("ons-data-api", changed)
        changed = copy.deepcopy(envelope)
        changed["provenance"]["pages"][0]["requestUrl"] += "?changed=true"
        with self.assertRaisesRegex(ValueError, "receipt-set binding"):
            corpus._source_projection("ons-data-api", changed)
        changed = copy.deepcopy(envelope)
        changed["records"][1] = copy.deepcopy(changed["records"][0])
        changed["provenance"]["recordSetSha256"] = corpus._source_digest(changed["records"])
        with self.assertRaisesRegex(ValueError, "Duplicate or cross-source"):
            corpus._source_projection("ons-data-api", changed)

    def test_fixture_contains_no_observation_or_geometry_payload_keys(self) -> None:
        forbidden = {"observations", "geometry", "valuedomain", "access_token", "password"}

        def check(value: object) -> None:
            if isinstance(value, dict):
                self.assertFalse(forbidden.intersection(key.casefold() for key in value))
                for child in value.values():
                    check(child)
            elif isinstance(value, list):
                for child in value:
                    check(child)

        check(self.story["records"])

    def test_write_never_overwrites_different_existing_bytes(self) -> None:
        corpus._write(self.path, self.story, False)
        original = self.path.read_bytes()
        with self.assertRaisesRegex(ValueError, "Output exists"):
            corpus._write(self.path, self.story, False)
        corpus._write(self.path, self.story, True)
        with self.assertRaisesRegex(ValueError, "byte-identical"):
            corpus._write(self.path, {"different": True}, True)
        self.assertEqual(self.path.read_bytes(), original)

    def test_invalid_scope_does_not_read_source(self) -> None:
        with patch.object(corpus, "_git_blob") as read, self.assertRaises(ValueError):
            corpus.import_pinned(Path("source"), "all")
        read.assert_not_called()

    def test_cli_refuses_any_output_in_the_read_only_source_repository(self) -> None:
        arguments = ["web216_corpus.py", "--source-repo", self.directory.name,
                     "--output", str(self.path)]
        with patch("sys.argv", arguments), patch.object(corpus, "import_pinned") as read:
            with self.assertRaises(SystemExit) as error:
                corpus.main()
        self.assertEqual(error.exception.code, 1)
        read.assert_not_called()
        self.assertFalse(self.path.exists())


if __name__ == "__main__":
    unittest.main()
