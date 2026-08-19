from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
FIXED_REVISION = "0" * 40


def load_builder() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "gis_ai_go_build_okf", ROOT / "scripts" / "build_okf.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load OKF builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILDER = load_builder()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def file_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def parse_json_frontmatter(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise AssertionError(f"missing frontmatter: {path}")
    result: dict[str, Any] = {}
    for line in lines[1:]:
        if line == "---":
            return result
        key, value = line.split(": ", 1)
        if key in result:
            raise AssertionError(f"duplicate frontmatter key: {key}")
        result[key] = json.loads(value)
    raise AssertionError(f"unterminated frontmatter: {path}")


def copy_locked_inputs(destination: Path) -> dict[str, Any]:
    source_lock = load_json(ROOT / "okf" / "source-lock.json")
    for item in source_lock["inputs"]:
        source = ROOT / item["path"]
        target = destination / item["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return source_lock


class OkfBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_directory = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temporary_directory.name) / "bundle"
        BUILDER.build(ROOT, cls.output, FIXED_REVISION)
        cls.bundle = load_json(cls.output / "okf-bundle.json")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary_directory.cleanup()

    def test_build_is_byte_for_byte_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_output = Path(first) / "different" / "first"
            second_output = Path(second) / "second"
            BUILDER.build(ROOT, first_output, FIXED_REVISION)
            BUILDER.build(ROOT, second_output, FIXED_REVISION)
            self.assertEqual(file_bytes(first_output), file_bytes(second_output))

    def test_bundle_schema_and_publication_boundary(self) -> None:
        schema = load_json(ROOT / "schemas" / "okf-publication-bundle.schema.json")
        Draft202012Validator.check_schema(schema)
        errors = list(
            Draft202012Validator(
                schema, format_checker=FormatChecker()
            ).iter_errors(self.bundle)
        )
        self.assertEqual(errors, [])
        self.assertEqual(self.bundle["recordCount"], 18)
        self.assertEqual(self.bundle["recordCount"], len(self.bundle["records"]))
        self.assertEqual(
            self.bundle["profile"],
            "https://chris-page-gov.github.io/gis-ai-go/profile/public-discovery/v1/",
        )
        self.assertTrue(self.bundle["scope"]["metadataOnly"])
        self.assertFalse(self.bundle["scope"]["containsProtectedData"])
        self.assertEqual(self.bundle["rights"]["thirdPartyNotices"], "THIRD_PARTY.md")
        self.assertEqual(
            (self.output / "THIRD_PARTY.md").read_bytes(),
            (ROOT / "THIRD_PARTY.md").read_bytes(),
        )
        self.assertEqual(
            (self.output / "third-party" / "okf-landregistry-LICENSE.md").read_bytes(),
            (
                ROOT
                / "okf/vendor/okf-landregistry/v0.3.0/LICENSE.md"
            ).read_bytes(),
        )
        for record in self.bundle["records"]:
            with self.subTest(record=record["id"]):
                self.assertEqual(record["publication"]["classification"], "public")
                self.assertFalse(record["publication"]["containsPersonalData"])
                self.assertFalse(record["publication"]["containsProtectedData"])
                self.assertIn("recordLicence", record["rights"])
                self.assertIn("describedResourceLicence", record["rights"])

    def test_source_lock_pins_the_approved_release(self) -> None:
        source_lock = load_json(ROOT / "okf" / "source-lock.json")
        paths = [item["path"] for item in source_lock["inputs"]]
        self.assertEqual(paths, sorted(set(paths)))
        release = source_lock["external_release"]
        self.assertEqual(release["retrieved_on"], "2026-08-19")
        self.assertEqual(release["tag"], "v0.3.0")
        self.assertEqual(
            release["commit"], "1d708e39f2cde19610d43c5a7f5e36e4a2f947bc"
        )
        self.assertEqual(
            release["release_root_sha256"],
            "6a29e38e7bb805aafb7f36ba8d1fa4ce976875f45997049cd4808d6ede7f75e1",
        )

    def test_selected_hmlr_records_have_known_rights_and_legal_caveats(self) -> None:
        datasets = {
            record["id"]: record
            for record in self.bundle["records"]
            if record["type"] == "dataset"
        }
        self.assertEqual(
            set(datasets),
            {
                "hmlr:dataset:inspire-index-polygons",
                "hmlr:dataset:local-land-charges-inspire",
                "hmlr:dataset:price-paid-data",
            },
        )
        for identifier, record in datasets.items():
            with self.subTest(record=identifier):
                self.assertEqual(record["access"]["state"], "public")
                self.assertEqual(record["rights"]["state"], "open-with-conditions")
                self.assertTrue(record["rights"]["attribution"])
        for identifier in (
            "hmlr:dataset:inspire-index-polygons",
            "hmlr:dataset:local-land-charges-inspire",
        ):
            caveats = " ".join(datasets[identifier]["limitations"]).lower()
            self.assertIn("indicative", caveats)
            self.assertTrue("legal" in caveats or "definitive" in caveats)

    def test_json_and_jsonld_project_the_same_identifiers(self) -> None:
        jsonld = load_json(self.output / "okf-bundle.jsonld")
        json_ids = {record["id"] for record in self.bundle["records"]}
        jsonld_ids = {record["identifier"] for record in jsonld["@graph"]}
        self.assertEqual(json_ids, jsonld_ids)
        self.assertEqual(len(jsonld["@graph"]), self.bundle["recordCount"])
        self.assertEqual(
            load_json(self.output / "context.jsonld"), {"@context": jsonld["@context"]}
        )
        for record in self.bundle["records"]:
            self.assertLessEqual(set(record["sourceRefs"]), json_ids)
        jsonld_by_id = {record["identifier"]: record for record in jsonld["@graph"]}
        for record in self.bundle["records"]:
            projection = jsonld_by_id[record["id"]]
            with self.subTest(record=record["id"]):
                self.assertEqual(projection["recordSchema"], record["schema"])
                self.assertEqual(projection["@type"], f"okf:{record['type'].title()}")
                for field in (
                    "title",
                    "description",
                    "status",
                    "authority",
                    "publication",
                    "access",
                    "rights",
                    "freshness",
                    "limitations",
                    "tags",
                    "details",
                ):
                    self.assertEqual(projection[field], record[field])
                self.assertEqual(projection["sourceIdentifier"], record["sourceRefs"])

    def test_markdown_frontmatter_projects_every_record_field(self) -> None:
        for record in self.bundle["records"]:
            path = self.output / BUILDER.record_output_path(record)
            with self.subTest(record=record["id"]):
                self.assertEqual(parse_json_frontmatter(path), record)

    def test_manifest_checksums_and_content_root_are_complete(self) -> None:
        manifest = load_json(self.output / "manifest.json")
        for entry in manifest["files"]:
            path = self.output / entry["path"]
            self.assertTrue(path.is_file())
            self.assertEqual(path.stat().st_size, entry["bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), entry["sha256"])

        checksum_bytes = (self.output / "CHECKSUMS.sha256").read_bytes()
        checksum_rows = []
        for line in checksum_bytes.decode("utf-8").splitlines():
            digest, relative = line.split("  ", 1)
            self.assertNotIn("..", Path(relative).parts)
            self.assertEqual(
                hashlib.sha256((self.output / relative).read_bytes()).hexdigest(), digest
            )
            checksum_rows.append(relative)
        self.assertEqual(checksum_rows, sorted(checksum_rows))
        self.assertIn("build-receipt.json", checksum_rows)
        self.assertNotIn("CHECKSUMS.sha256", checksum_rows)

        receipt = load_json(self.output / "build-receipt.json")
        self.assertEqual(receipt["outputCount"], len(checksum_rows))
        content_checksums = "".join(
            line + "\n"
            for line in checksum_bytes.decode("utf-8").splitlines()
            if not line.endswith("  build-receipt.json")
        ).encode()
        self.assertEqual(
            receipt["contentRootSha256"], hashlib.sha256(content_checksums).hexdigest()
        )
        expected_input_root = hashlib.sha256(
            "".join(
                f"{item['sha256']}  {item['path']}\n" for item in receipt["inputs"]
            ).encode()
        ).hexdigest()
        self.assertEqual(receipt["inputRootSha256"], expected_input_root)
        self.assertEqual(
            receipt["manifestSha256"],
            hashlib.sha256((self.output / "manifest.json").read_bytes()).hexdigest(),
        )
        self.assertFalse(receipt["determinism"]["wallClockIncluded"])
        self.assertFalse(receipt["determinism"]["checkoutPathIncluded"])

    def test_output_contains_no_historical_identity_or_machine_path(self) -> None:
        text = b"\n".join(file_bytes(self.output).values()).decode("utf-8")
        self.assertNotIn("Locus Accord", text)
        self.assertNotIn("/Users/", text)
        self.assertNotIn('"publicationState": "released"', text)
        self.assertNotIn('"status": "released"', text)

    def test_bad_rights_for_selected_record_fail_closed(self) -> None:
        records = load_json(
            ROOT
            / "okf/vendor/okf-landregistry/v0.3.0/source/curated-records.json"
        )["records"]
        rights = load_json(
            ROOT
            / "okf/vendor/okf-landregistry/v0.3.0/source/curated-rights-access.json"
        )["classifications"]
        record = next(row for row in records if row["id"] == "hmlr:dataset:price-paid-data")
        classification = copy.deepcopy(
            next(row for row in rights if row["source_native_id"] == record["id"])
        )
        classification["rights_state"] = "unknown"
        publication = load_json(ROOT / "okf" / "source" / "publication.json")
        with self.assertRaisesRegex(ValueError, "publishable rights"):
            BUILDER.hmlr_dataset_record(record, classification, ["S-HMLR-PPD"], publication)

    def test_forbidden_payload_keys_and_unsafe_urls_fail_closed(self) -> None:
        profile = load_json(ROOT / "okf" / "profile" / "public-discovery-v1.json")
        forbidden = {BUILDER.canonical_key(key) for key in profile["forbidden_payload_keys"]}
        with self.assertRaisesRegex(ValueError, "forbidden payload key"):
            BUILDER.reject_forbidden_keys({"nested": {"geometry": {}}}, forbidden)
        for value in ("javascript:alert(1)", "file:///tmp/data", "../escape"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                BUILDER.validate_url(value)

    def test_unknown_access_and_unresolved_references_fail_closed(self) -> None:
        records = copy.deepcopy(self.bundle["records"])
        records[0]["sourceRefs"].append("missing:source")
        with self.assertRaisesRegex(ValueError, "unresolved source references"):
            BUILDER.validate_reference_closure(records)

        invalid = copy.deepcopy(self.bundle["records"])
        invalid[0]["access"]["state"] = "unknown"
        profile = load_json(ROOT / "okf" / "profile" / "public-discovery-v1.json")
        schema = load_json(ROOT / "schemas" / "okf-publication-bundle.schema.json")
        with self.assertRaisesRegex(ValueError, "failed schema validation"):
            BUILDER.validate_records(invalid, profile, schema)

    def test_changed_locked_input_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_lock = copy_locked_inputs(root)
            relative = source_lock["inputs"][0]["path"]
            target = root / relative
            target.write_bytes(target.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                BUILDER.verify_source_lock(root, source_lock)

    def test_vendored_input_inventory_is_exact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_lock = copy_locked_inputs(root)
            extra = root / BUILDER.HMLR_VENDOR / "unexpected.json"
            extra.write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "inventory differs"):
                BUILDER.verify_source_lock(root, source_lock)

    def test_symbolic_linked_input_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_lock = copy_locked_inputs(root)
            relative = "okf/vendor/okf-landregistry/v0.3.0/LICENSE.md"
            target = root / relative
            target.unlink()
            target.symlink_to(ROOT / relative)
            with self.assertRaisesRegex(ValueError, "symbolic link"):
                BUILDER.verify_source_lock(root, source_lock)

    def test_traversal_path_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsafe locked path"):
            BUILDER.locked_path(ROOT, "../outside.json")

    def test_colliding_output_paths_fail_closed(self) -> None:
        records = [
            {"id": "example:a/b", "type": "source"},
            {"id": "example:a-b", "type": "source"},
        ]
        with self.assertRaisesRegex(ValueError, "colliding output paths"):
            BUILDER.validate_output_paths(records)


if __name__ == "__main__":
    unittest.main()
