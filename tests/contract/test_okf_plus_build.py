"""Independent offline producer and capture-boundary regression tests."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError
from urllib.request import Request

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/okf_plus"))
import model
import harvest
import import_sources
import freeze_locators

SPEC = importlib.util.spec_from_file_location("okf_plus_build_assurance", ROOT / "scripts/okf_plus/build.py")
assert SPEC and SPEC.loader
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)

REVISION = "c" * 40
SOURCE_URL = "https://example.org/synthetic-catalogue"
CAPTURE_TIME = "2026-10-02T00:00:00Z"


def fixture(root: Path):
    native = {"id": "synthetic-1", "title": "Synthetic public metadata"}
    receipt = {"status": 200, "url": SOURCE_URL, "retrievedAt": CAPTURE_TIME,
               "sha256": "a" * 64, "bytes": 100}
    snapshot = {
        "schema": "okf-plus-source-snapshot.v1", "family": "synthetic",
        "records": [native], "receipts": [receipt],
        "coverage": {"unit": "synthetic metadata record", "retrievedUnique": 1,
                     "reportedTotal": 1, "catalogueComplete": True,
                     "limitations": ["Synthetic test only."]},
    }
    source = {"resource": SOURCE_URL, "retrievedAt": CAPTURE_TIME,
              "responseSha256": receipt["sha256"], "sourcePointer": "/items/0",
              "normalisedSource": "okf-plus/source/synthetic.json",
              "normalisedPointer": "/records/0", "normalisedRecordSha256": model.digest(native),
              "sourcePointerStatus": "exact-native-id-match", "evidenceKind": "captured-public-metadata"}
    row = model.record("synthetic", "synthetic-1", native["title"],
                       "Synthetic fixture; no provider data or credentials.",
                       "https://example.org/synthetic-record", source)
    source_path = root / source["normalisedSource"]
    source_path.parent.mkdir(parents=True)
    source_path.write_bytes(model.canonical(snapshot))
    (source_path.parent / "locator-index.json").write_bytes(model.canonical({
        "families": {"synthetic": {"synthetic-1": {
            "url": SOURCE_URL, "retrievedAt": CAPTURE_TIME, "sha256": receipt["sha256"],
            "pointer": source["sourcePointer"], "status": source["sourcePointerStatus"],
        }}},
    }))
    record_path = root / "okf-plus/records/synthetic/one.md"
    model.write_markdown(record_path, row, "# Synthetic metadata\n\nNo live observation is present.")
    return row, record_path, snapshot


def generated_bytes(output):
    return {p.relative_to(output).as_posix(): p.read_bytes()
            for p in sorted(output.rglob("*")) if p.is_file()}


class FakeResponse:
    status = 200
    headers = {}
    url = "https://api.os.uk/downloads/v1/products"

    def __init__(self, body=b"[]"):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self, limit):
        return self.body[:limit]


def capture_fixture(root, document, url=SOURCE_URL):
    raw = document.encode() if isinstance(document, str) else model.canonical(document)
    checksum = hashlib.sha256(raw).hexdigest()
    directory = root / "artifacts/okf-plus/capture"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / (checksum + ".body")).write_bytes(raw)
    return {"url": url, "retrievedAt": CAPTURE_TIME, "sha256": checksum,
            "status": 200, "bytes": len(raw)}


class OkfPlusLocatorTests(unittest.TestCase):
    def test_exact_native_identifier_is_bound_to_its_page(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = capture_fixture(root, {"items": [{"id": "first"}]})
            second = capture_fixture(root, {"items": [{"id": "second"}]}, SOURCE_URL + "?page=2")
            snapshot = {"family": "synthetic", "records": [{"id": "second"}], "receipts": [first, second]}
            actual = import_sources.original_locators(root, snapshot)
            self.assertEqual(actual["second"], (second, "/items/0"))
            snapshot["records"] = [{"id": "absent"}]
            with self.assertRaises(ValueError):
                import_sources.original_locators(root, snapshot)

    def test_explicit_native_uri_or_name_pointer_is_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for field in ("uri", "name"):
                receipt = capture_fixture(root, {"items": [{field: "native-value"}]})
                item = {"id": "native-value", "nativeIdentityField": field,
                        "sourceEvidence": {**receipt, "pointer": "/items/0"}}
                snapshot = {"family": "synthetic", "records": [item], "receipts": [receipt]}
                self.assertEqual(import_sources.original_locators(root, snapshot)["native-value"],
                                 (receipt, "/items/0"))
                for pointer in ("/items/1", "/items/-1", "/items/01", "/it~2ems/0"):
                    item["sourceEvidence"]["pointer"] = pointer
                    with self.subTest(pointer=pointer), self.assertRaises(ValueError):
                        import_sources.original_locators(root, snapshot)
                item["sourceEvidence"]["pointer"] = "/items/0"
                item["id"] = "wrong-native-id"
                with self.assertRaises(ValueError):
                    import_sources.original_locators(root, snapshot)

    def test_private_raw_tampering_or_missing_response_stops_freezing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = capture_fixture(root, {"id": "a"})
            snapshot = {"family": "synthetic", "records": [{"id": "a"}], "receipts": [receipt]}
            raw = root / "artifacts/okf-plus/capture" / (receipt["sha256"] + ".body")
            raw.write_bytes(b"{}")
            with self.assertRaises(ValueError):
                import_sources.original_locators(root, snapshot)
            raw.unlink()
            with self.assertRaises(FileNotFoundError):
                import_sources.original_locators(root, snapshot)

    def test_reviewed_nested_code_list_identity_is_resolved_from_the_raw_item(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = capture_fixture(root, {"items": [{"links": {"self": {"id": "native-code-list"}}}]})
            item = {"id": "native-code-list", "nativeIdentityField": "/links/self/id",
                    "sourceEvidence": {**receipt, "pointer": "/items/0"}}
            snapshot = {"family": "synthetic", "records": [item], "receipts": [receipt]}
            self.assertEqual(import_sources.original_locators(root, snapshot)[item['id']], (receipt, "/items/0"))
            item['nativeIdentityField'] = '/links/self/missing'
            with self.assertRaises(ValueError):
                import_sources.original_locators(root, snapshot)

    def test_document_binding_needs_explicit_matching_url_and_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = capture_fixture(root, "# Public synthetic guide\n")
            item = {"id": SOURCE_URL, "url": SOURCE_URL, "sourceSha256": receipt["sha256"]}
            snapshot = {"family": "synthetic", "records": [item], "receipts": [receipt]}
            self.assertEqual(import_sources.original_locators(root, snapshot)[SOURCE_URL], (receipt, None))
            item["url"] = SOURCE_URL + "/wrong"
            with self.assertRaises(ValueError):
                import_sources.original_locators(root, snapshot)

    def test_navigation_document_must_contain_the_native_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            link = "https://example.org/guide"
            receipt = capture_fixture(root, "- [Guide](" + link + ")\n")
            snapshot = {"family": "synthetic-documentation", "records": [{"id": link}], "receipts": [receipt]}
            self.assertEqual(import_sources.original_locators(root, snapshot)[link], (receipt, None))
            snapshot["records"] = [{"id": link + "/absent"}]
            with self.assertRaises(ValueError):
                import_sources.original_locators(root, snapshot)

    def test_failed_metadata_is_never_rebound_to_successful_capture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            success = capture_fixture(root, {"id": "other"})
            failed = {"url": SOURCE_URL + "/failed", "retrievedAt": CAPTURE_TIME, "status": 500}
            item = {"id": "failed-id", "metadataStatus": "request-failed", "metadataEvidence": failed}
            snapshot = {"family": "synthetic", "records": [item], "receipts": [success, failed]}
            self.assertEqual(import_sources.original_locators(root, snapshot), {})
            evidence = import_sources.source_evidence(snapshot, Path("okf-plus/source/synthetic.json"), 0, item, {})
            self.assertEqual(evidence["evidenceKind"], "failed-metadata-request")
            self.assertEqual(evidence["requestStatus"], 500)
            self.assertNotIn("responseSha256", evidence)
            self.assertNotIn("sourcePointer", evidence)
            item["metadataEvidence"] = {**failed, "url": SOURCE_URL + "/unrecorded"}
            with self.assertRaises(ValueError):
                import_sources.original_locators(root, snapshot)

    def test_metadata_document_requires_the_exact_receipt_tuple(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            receipt = capture_fixture(root, {"version": 1, "title": "Synthetic metadata"})
            item = {"id": "dataset", "metadataEvidence": copy.deepcopy(receipt)}
            snapshot = {"family": "synthetic", "records": [item], "receipts": [receipt]}
            self.assertEqual(import_sources.original_locators(root, snapshot)["dataset"], (receipt, None))
            for field, value in (("url", SOURCE_URL + "/unrelated"),
                                 ("retrievedAt", "2025-01-01T00:00:00Z")):
                item["metadataEvidence"] = {**receipt, field: value}
                with self.subTest(field=field), self.assertRaises(ValueError):
                    import_sources.original_locators(root, snapshot)

    def test_browser_observation_has_no_invented_http_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            item = {"id": "browser-only", "sourceObservation": {
                "status": "browser-observed", "sourceUrl": SOURCE_URL, "observedOn": "2026-10-02"}}
            snapshot = {"family": "synthetic", "records": [item], "receipts": []}
            self.assertEqual(import_sources.original_locators(root, snapshot), {})
            evidence = import_sources.source_evidence(snapshot, Path("okf-plus/source/synthetic.json"), 0, item, {})
            self.assertEqual(evidence["evidenceKind"], "rendered-public-catalogue")
            for field in ("responseSha256", "retrievedAt", "sourcePointer"):
                self.assertNotIn(field, evidence)

    def test_failed_freeze_preserves_the_previous_public_locator_index(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            path = root / "okf-plus/source/locator-index.json"
            before = path.read_bytes()
            with self.assertRaises(FileNotFoundError):
                freeze_locators.freeze(root)
            self.assertEqual(path.read_bytes(), before)

    def test_verified_freeze_is_deterministic_and_import_is_cache_independent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _row, _path, snapshot = fixture(root)
            receipt = capture_fixture(root, {"items": snapshot["records"]})
            snapshot["receipts"] = [receipt]
            source_path = root / "okf-plus/source/synthetic.json"
            source_path.write_bytes(model.canonical(snapshot))
            first = freeze_locators.freeze(root)
            index_path = source_path.parent / "locator-index.json"
            frozen_bytes = index_path.read_bytes()
            self.assertEqual(freeze_locators.freeze(root), first)
            self.assertEqual(index_path.read_bytes(), frozen_bytes)
            raw = root / "artifacts/okf-plus/capture" / (receipt["sha256"] + ".body")
            raw.unlink()
            evidence = import_sources.source_evidence(snapshot, Path("okf-plus/source/synthetic.json"),
                0, snapshot["records"][0], first["families"]["synthetic"])
            self.assertEqual(evidence["responseSha256"], receipt["sha256"])
            self.assertEqual(evidence["sourcePointer"], "/items/0")


class OkfPlusBuildTests(unittest.TestCase):
    def validate(self, root, row, path, snapshot):
        with mock.patch.object(BUILD, "ROOT", root):
            BUILD.validate_record(row, path, {"okf-plus/source/synthetic.json": snapshot})

    def test_relocated_builds_are_byte_identical_and_checksums_cover_outputs(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            outputs = []
            for directory in (a, b):
                root = Path(directory)
                fixture(root)
                output = root / "generated"
                with mock.patch.object(BUILD, "ROOT", root):
                    coverage = BUILD.build(root, output, REVISION)
                self.assertEqual(coverage["recordCount"], 1)
                self.assertEqual(coverage["globalCompleteness"], "not-established")
                checksums = json.loads((output / "checksums.json").read_text())
                self.assertEqual(set(checksums), {p.name for p in output.iterdir()
                                                if p.is_file() and p.name != "checksums.json"})
                for relative, digest in checksums.items():
                    self.assertEqual(hashlib.sha256((output / relative).read_bytes()).hexdigest(), digest)
                outputs.append(generated_bytes(output))
                self.assertNotIn(directory.encode(), b"".join(outputs[-1].values()))
            self.assertEqual(*outputs)

    def test_changed_source_bytes_fail_the_existing_record_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row, path, snapshot = fixture(root)
            snapshot["records"][0]["title"] = "Changed source metadata"
            with self.assertRaises(ValueError):
                self.validate(root, row, path, snapshot)

    def test_import_uses_frozen_locator_without_private_capture_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row, _path, snapshot = fixture(root)
            locators = model.load_json((root / "okf-plus/source/locator-index.json").read_text())
            self.assertFalse((root / "artifacts").exists())
            imported = import_sources.source_evidence(
                snapshot, Path("okf-plus/source/synthetic.json"), 0,
                snapshot["records"][0], locators["families"]["synthetic"])
            self.assertEqual(imported, row["sources"][0])
            with self.assertRaises(ValueError):
                import_sources.source_evidence(snapshot, Path("okf-plus/source/synthetic.json"),
                                               0, snapshot["records"][0], {})

    def test_provenance_url_and_time_must_match_the_digest_bound_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row, path, snapshot = fixture(root)
            for field, value in (("resource", "https://example.org/wrong-source"),
                                 ("retrievedAt", "1900-01-01T00:00:00Z")):
                mutated = copy.deepcopy(row)
                mutated["sources"][0][field] = value
                with self.subTest(field=field), self.assertRaises(ValueError):
                    self.validate(root, mutated, path, snapshot)

    def test_native_identifier_and_family_cannot_drift_from_normalised_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row, path, snapshot = fixture(root)
            for field, value in (("nativeIdentifier", "other-id"), ("sourceFamily", "other-family")):
                mutated = copy.deepcopy(row)
                mutated[field] = value
                with self.subTest(field=field), self.assertRaises(ValueError):
                    self.validate(root, mutated, path, snapshot)

    def test_provenance_and_reference_urls_reject_credentials_and_control_bytes(self):
        unsafe = ("https://example.org/data?%74oken=synthetic", "https://example.org/data?key=synthetic",
                  "https://example.org:99999/data", "https://example.org/data\n#outside",
                  "https://example.org/data with spaces", "https://user:synthetic@example.org/data")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row, path, snapshot = fixture(root)
            for url in unsafe:
                mutated = copy.deepcopy(row)
                mutated["resource"] = url
                with self.subTest(url=url), self.assertRaises(ValueError):
                    self.validate(root, mutated, path, snapshot)

    def test_unknown_temporal_bounds_and_execution_authority_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row, path, snapshot = fixture(root)
            mutated = copy.deepcopy(row)
            mutated["temporal"]["start"] = "2024-01-01"
            with self.assertRaises(ValueError):
                self.validate(root, mutated, path, snapshot)
            mutated = copy.deepcopy(row)
            mutated["rights"]["executionAdmitted"] = True
            with self.assertRaises(ValueError):
                self.validate(root, mutated, path, snapshot)

    def test_invalid_typed_dates_and_reversed_extent_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row, path, snapshot = fixture(root)
            for start, end in (("2024-13-99", None), ("2025-01-01", "2024-01-01")):
                mutated = copy.deepcopy(row)
                with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                    model.apply_temporal(mutated, start, end, "dataset-reference-period", "synthetic")
                    self.validate(root, mutated, path, snapshot)

    def test_duplicate_identity_and_record_symlinks_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row, path, _snapshot = fixture(root)
            other = path.with_name("two.md")
            model.write_markdown(other, row, "# Duplicate synthetic identity")
            with self.assertRaises(ValueError):
                BUILD.build(root, root / "generated-one", REVISION)
            other.unlink()
            other.symlink_to(path)
            with self.assertRaises(ValueError):
                BUILD.build(root, root / "generated-two", REVISION)

    def test_normalised_source_symlink_cannot_escape_the_checkout(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as external:
            root = Path(directory)
            _row, _path, snapshot = fixture(root)
            target = Path(external) / "source.json"
            target.write_bytes(model.canonical(snapshot))
            source = root / "okf-plus/source/synthetic.json"
            source.unlink()
            source.symlink_to(target)
            with self.assertRaises(ValueError):
                BUILD.build(root, root / "generated", REVISION)

    def test_unmarked_output_and_source_directories_are_never_replaced(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root)
            output = root / "unrelated"
            output.mkdir()
            (output / "keep.txt").write_text("Keep this user file.")
            with self.assertRaises(ValueError):
                BUILD.build(root, output, REVISION)
            self.assertEqual((output / "keep.txt").read_text(), "Keep this user file.")
            for candidate in (root, root / "okf-plus", root / "okf-plus/records"):
                with self.subTest(candidate=candidate), self.assertRaises(ValueError):
                    BUILD.build(root, candidate, REVISION)

    def test_failed_rebuild_preserves_every_previous_bundle_byte(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            row, path, _snapshot = fixture(root)
            output = root / "generated"
            BUILD.build(root, output, REVISION)
            before = generated_bytes(output)
            row["rights"]["executionAdmitted"] = True
            model.write_markdown(path, row, "# Invalid synthetic input")
            with self.assertRaises(ValueError):
                BUILD.build(root, output, REVISION)
            self.assertEqual(generated_bytes(output), before)
            self.assertEqual(list(root.glob(".okf-plus-build-*")), [])

    def test_capture_rejects_encoded_credentials_and_noncanonical_paths(self):
        for url in ("https://api.os.uk/downloads/v1/products?%74oken=synthetic",
                    "https://api.os.uk/downloads/v1/products?key",
                    "https://docs.os.uk/../private.md",
                    "https://docs.os.uk/a/../private.md",
                    "https://docs.os.uk/a%2f..%2fprivate.md"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                harvest.allowed(url)

    def test_redirect_does_not_bypass_request_accounting(self):
        handler = harvest.Redirect()
        url = "https://api.os.uk/downloads/v1/products"
        with self.assertRaises((HTTPError, ValueError)):
            handler.redirect_request(Request(url), None, 302, "Found", {}, url + "/OpenNames")

    def test_wall_deadline_interrupts_work_and_restores_signal_handler(self):
        previous = object()
        with mock.patch.object(harvest.signal, "getsignal", return_value=previous), \
             mock.patch.object(harvest.signal, "getitimer", return_value=(0, 0)), \
             mock.patch.object(harvest.signal, "signal") as install, \
             mock.patch.object(harvest.signal, "setitimer") as timer:
            with self.assertRaises(TimeoutError):
                with harvest.deadline():
                    handler = install.call_args.args[1]
                    handler(None, None)
            self.assertEqual(timer.call_args_list, [
                mock.call(harvest.signal.ITIMER_REAL, 30),
                mock.call(harvest.signal.ITIMER_REAL, 0),
            ])
            self.assertEqual(install.call_args, mock.call(harvest.signal.SIGALRM, previous))

    def test_wall_deadline_does_not_replace_an_existing_alarm(self):
        with mock.patch.object(harvest.signal, "getsignal"), \
             mock.patch.object(harvest.signal, "getitimer", return_value=(10, 0)), \
             mock.patch.object(harvest.signal, "signal") as install:
            with self.assertRaises(RuntimeError):
                with harvest.deadline():
                    self.fail("An existing alarm must block this capture.")
            install.assert_not_called()

    def test_request_ceiling_prevents_the_next_network_attempt(self):
        with tempfile.TemporaryDirectory() as directory:
            cap = harvest.Capture(Path(directory), max_requests=1)
            cap.ledger["requests"] = [{"url": "https://example.org/previous", "status": "failed"}]
            cap.opener = mock.Mock()
            with self.assertRaises(RuntimeError):
                cap.get("https://api.os.uk/downloads/v1/products")
            cap.opener.open.assert_not_called()

    def test_response_byte_overflow_is_recorded_and_not_published(self):
        with tempfile.TemporaryDirectory() as directory:
            cap = harvest.Capture(Path(directory), max_requests=1)
            cap.opener = mock.Mock()
            cap.opener.open.return_value = FakeResponse(b"x" * 33)
            with mock.patch.object(harvest, "MAX_BYTES", 32), mock.patch.object(harvest.time, "sleep"):
                data, receipt = cap.get("https://api.os.uk/downloads/v1/products")
            self.assertIsNone(data)
            self.assertEqual(receipt["status"], "failed")
            self.assertEqual(receipt["bytes"], 33)
            self.assertFalse(list(cap.public.glob("*.json")))

    def test_verified_cache_avoids_a_second_request_and_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            cap = harvest.Capture(Path(directory), max_requests=1)
            cap.opener = mock.Mock()
            cap.opener.open.return_value = FakeResponse()
            with mock.patch.object(harvest.time, "sleep"):
                value, receipt = cap.get("https://api.os.uk/downloads/v1/products")
                replay, _ = cap.get("https://api.os.uk/downloads/v1/products")
            self.assertEqual(value, replay)
            self.assertEqual(cap.opener.open.call_count, 1)
            (cap.private / receipt["rawFile"]).write_bytes(b"[1]")
            with self.assertRaises(ValueError):
                cap.get("https://api.os.uk/downloads/v1/products")
            self.assertEqual(cap.opener.open.call_count, 1)


if __name__ == "__main__":
    unittest.main()
