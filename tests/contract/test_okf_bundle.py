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
        with (
            tempfile.TemporaryDirectory() as first,
            tempfile.TemporaryDirectory() as second,
        ):
            first_output = Path(first) / "different" / "first"
            second_output = Path(second) / "second"
            BUILDER.build(ROOT, first_output, FIXED_REVISION)
            BUILDER.build(ROOT, second_output, FIXED_REVISION)
            self.assertEqual(file_bytes(first_output), file_bytes(second_output))

    def test_bundle_schema_and_publication_boundary(self) -> None:
        schema = load_json(ROOT / "schemas" / "okf-publication-bundle.schema.json")
        Draft202012Validator.check_schema(schema)
        errors = list(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(
                self.bundle
            )
        )
        self.assertEqual(errors, [])
        self.assertEqual(self.bundle["recordCount"], 36)
        self.assertEqual(self.bundle["recordCount"], len(self.bundle["records"]))
        counts = {
            record_type: sum(
                record["type"] == record_type for record in self.bundle["records"]
            )
            for record_type in {record["type"] for record in self.bundle["records"]}
        }
        self.assertEqual(
            counts,
            {"bundle": 1, "dataset": 3, "provider": 4, "source": 24, "workflow": 4},
        )
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
            (ROOT / "okf/vendor/okf-landregistry/v0.3.0/LICENSE.md").read_bytes(),
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
        self.assertEqual(release["tagged_at"], "2026-08-12T01:43:30+01:00")
        self.assertEqual(release["commit"], "1d708e39f2cde19610d43c5a7f5e36e4a2f947bc")
        self.assertEqual(
            release["release_root_sha256"],
            "6a29e38e7bb805aafb7f36ba8d1fa4ce976875f45997049cd4808d6ede7f75e1",
        )
        self.assertEqual(
            release["evaluation_questions_sha256"], BUILDER.HMLR_QUESTIONS_SHA256
        )
        questions = ROOT / BUILDER.HMLR_QUESTIONS
        self.assertEqual(
            hashlib.sha256(questions.read_bytes()).hexdigest(),
            BUILDER.HMLR_QUESTIONS_SHA256,
        )
        question_lock = next(
            item
            for item in source_lock["inputs"]
            if item["path"] == BUILDER.HMLR_QUESTIONS.as_posix()
        )
        self.assertEqual(question_lock["sha256"], BUILDER.HMLR_QUESTIONS_SHA256)
        locked_sha256 = {Path(item["path"]): item["sha256"] for item in source_lock["inputs"]}
        self.assertEqual(
            {
                path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                for path in BUILDER.HMLR_APPROVED_INPUT_SHA256
            },
            BUILDER.HMLR_APPROVED_INPUT_SHA256,
        )
        for path, digest in BUILDER.HMLR_APPROVED_INPUT_SHA256.items():
            with self.subTest(path=path):
                self.assertEqual(locked_sha256[path], digest)

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

    def test_selected_hmlr_journeys_are_exact_non_executing_projections(self) -> None:
        workflows = {
            record["id"]: record
            for record in self.bundle["records"]
            if record["type"] == "workflow"
        }
        expected = {
            "LR-Q003": {
                "sha256": "1ceea667a350027240418de79439ecbe83f77a7243290b7970e3847a19f84547",
                "sources": {
                    "S-OKF-HMLR-V0.3.0",
                    "hmlr-source:7177c8b621ecfc42",
                    "hmlr-source:b81206b053b276d5",
                },
                "target": "NEG-LR-Q003-BUSINESS-GATEWAY-OFFICIAL-COPY",
            },
            "LR-Q006": {
                "sha256": "3d4980bd7f63ff5c65bd519584a42c85adab907bad17d216345467d07c507ab0",
                "sources": {
                    "S-OKF-HMLR-V0.3.0",
                    "hmlr-source:7177c8b621ecfc42",
                    "hmlr-source:b81206b053b276d5",
                    "hmlr-source:c5984959cb2b5fa5",
                },
                "target": "NEG-LR-Q006-ADDRESS-SEARCH-CODE",
            },
            "LR-Q012": {
                "sha256": "84269ab3c74e31517e7fb9a2c3eb7fba71b9e9757418be5674cfe778b88d452c",
                "sources": {
                    "S-OKF-HMLR-V0.3.0",
                    "hmlr-source:638ecac167aaf6f0",
                    "hmlr-source:951ac51b5d700a95",
                },
                "target": "NEG-LR-Q012-NATIONAL-POLYGON-SERVICE",
            },
        }
        self.assertEqual(set(workflows), {"WF01", *expected})
        for identifier, expectation in expected.items():
            record = workflows[identifier]
            with self.subTest(record=identifier):
                self.assertEqual(record["access"]["state"], "planned-non-executing")
                self.assertEqual(record["status"], "candidate-non-executing")
                self.assertEqual(record["authority"]["class"], "derived")
                self.assertEqual(record["authority"]["source"], "S-OKF-HMLR-V0.3.0")
                self.assertEqual(record["rights"]["state"], "metadata-citation")
                self.assertEqual(set(record["sourceRefs"]), expectation["sources"])
                self.assertEqual(
                    record["details"]["sourceRecordSha256"], expectation["sha256"]
                )
                self.assertEqual(
                    [target["id"] for target in record["details"]["forbiddenTargets"]],
                    [expectation["target"]],
                )
                self.assertEqual(
                    set(record["details"]["forbiddenTargets"][0]), {"id", "reason"}
                )
                self.assertTrue(record["details"]["expectedPropositions"])
                self.assertTrue(record["details"]["requiredCaveatIds"])

        self.assertIn(
            "not proof of ownership",
            " ".join(workflows["LR-Q003"]["details"]["expectedPropositions"]).lower(),
        )
        self.assertIn(
            "search of the index map",
            " ".join(workflows["LR-Q006"]["details"]["expectedPropositions"]).lower(),
        )
        q12_text = " ".join(
            workflows["LR-Q012"]["details"]["expectedPropositions"]
            + workflows["LR-Q012"]["limitations"]
        ).lower()
        self.assertIn("indicative", q12_text)
        self.assertIn("not exact legal boundary", q12_text)
        source_urls = {
            record["id"]: record["details"]["url"]
            for record in self.bundle["records"]
            if record["id"].startswith("hmlr-source:")
        }
        self.assertEqual(
            {
                identifier: source_urls[identifier]
                for identifier in (
                    "hmlr-source:638ecac167aaf6f0",
                    "hmlr-source:7177c8b621ecfc42",
                    "hmlr-source:951ac51b5d700a95",
                    "hmlr-source:b81206b053b276d5",
                    "hmlr-source:c5984959cb2b5fa5",
                )
            },
            {
                "hmlr-source:638ecac167aaf6f0": (
                    "https://www.gov.uk/government/publications/"
                    "hm-land-registry-plans-boundaries-pg40s3"
                ),
                "hmlr-source:7177c8b621ecfc42": (
                    "https://www.gov.uk/guidance/"
                    "land-registry-portal-how-to-request-official-copies"
                ),
                "hmlr-source:951ac51b5d700a95": (
                    "https://use-land-property-data.service.gov.uk/datasets/llc"
                ),
                "hmlr-source:b81206b053b276d5": (
                    "https://www.gov.uk/search-property-information-land-registry"
                ),
                "hmlr-source:c5984959cb2b5fa5": (
                    "https://www.gov.uk/guidance/"
                    "land-registry-portal-request-a-search-of-the-index-map"
                ),
            },
        )

    def test_provider_examples_preserve_mixed_rights_and_date_meanings(self) -> None:
        providers = {
            record["id"]: record
            for record in self.bundle["records"]
            if record["type"] == "provider"
        }
        expected_digests = {
            "PV-HMLR-OPEN": "2c9b1712ad8995bd4e6bd37699bad6fc233462cf874f7fdba14e5e0bfb23f824",
            "PV-LANDIS": "a735efba3e6d58d533f17d438e053246f7902705881186de542f5d26043e2c2a",
            "PV-ONS-DATA": "535e6eb65fc9af4507e30700d425393a658a085a3a240689f4b37124dc8f8622",
            "PV-ONS-GEO": "75f4313b278f360c0e60a8095ffdedca16aaabc7ce7ec91448ba1a1659203c1c",
        }
        self.assertEqual(set(providers), set(expected_digests))
        for identifier, record in providers.items():
            with self.subTest(record=identifier):
                self.assertEqual(record["access"]["state"], "public-metadata")
                self.assertEqual(record["rights"]["state"], "metadata-citation")
                self.assertEqual(
                    record["details"]["sourceRecordSha256"],
                    expected_digests[identifier],
                )
                self.assertEqual(
                    record["details"]["metadataSnapshotGeneratedAt"],
                    "2026-08-19T13:30:00+01:00",
                )
                self.assertEqual(
                    record["freshness"]["observedAt"],
                    record["details"]["metadataSnapshotGeneratedAt"],
                )
                self.assertEqual(
                    record["freshness"]["reviewedAt"], "2026-08-20T00:00:00Z"
                )
                if identifier != "PV-HMLR-OPEN":
                    self.assertNotIn("hmlr", record["tags"])

        landis = providers["PV-LANDIS"]
        self.assertEqual(landis["details"]["describedAccess"], "mixed-per-record")
        self.assertEqual(
            landis["details"]["accessTiers"],
            ["open", "commercial-or-restricted where record terms require"],
        )
        self.assertIn(
            "each record", landis["rights"]["describedResourceLicence"].lower()
        )
        self.assertIn(
            "blanket licence", landis["rights"]["describedResourceLicence"].lower()
        )
        self.assertIn("mixed-access", landis["tags"])

        ons_data = providers["PV-ONS-DATA"]
        ons_geo = providers["PV-ONS-GEO"]
        self.assertEqual(set(ons_data["sourceRefs"]), {"S-ONS-API", "S-ONS-LICENCE"})
        self.assertEqual(
            set(ons_geo["sourceRefs"]),
            {"S-ONS-GEOGRAPHY", "S-ONS-LICENCE", "S-ONS-OPG"},
        )
        self.assertIn("where stated", ons_data["rights"]["describedResourceLicence"])
        self.assertIn(
            "product-specific", ons_geo["rights"]["describedResourceLicence"].lower()
        )

        records = {record["id"]: record for record in self.bundle["records"]}
        ons_source = records["S-ONS-API"]
        self.assertIsNone(ons_source["details"]["published"])
        self.assertEqual(ons_source["details"]["retrieved"], "2026-08-19")
        self.assertEqual(ons_source["freshness"]["observedAt"], "2026-08-19T00:00:00Z")
        price_paid = records["hmlr:dataset:price-paid-data"]
        self.assertEqual(price_paid["details"]["publisherLastUpdated"], "2026-07-28")
        self.assertEqual(price_paid["freshness"]["observedAt"], "2026-07-29T07:53:38Z")

    def test_hmlr_release_provenance_is_visible_and_exact(self) -> None:
        release = next(
            record
            for record in self.bundle["records"]
            if record["id"] == "S-OKF-HMLR-V0.3.0"
        )
        details = release["details"]
        self.assertEqual(release["authority"]["class"], "derived")
        self.assertEqual(details["releaseTag"], "v0.3.0")
        self.assertEqual(details["releaseTaggedAt"], "2026-08-12T01:43:30+01:00")
        self.assertEqual(details["retrievedOn"], "2026-08-19")
        self.assertEqual(details["commit"], "1d708e39f2cde19610d43c5a7f5e36e4a2f947bc")
        self.assertEqual(
            details["releaseRootSha256"],
            "6a29e38e7bb805aafb7f36ba8d1fa4ce976875f45997049cd4808d6ede7f75e1",
        )
        self.assertEqual(
            details["evaluationQuestionsSha256"], BUILDER.HMLR_QUESTIONS_SHA256
        )
        self.assertEqual(details["supersededResearchCommitPrefix"], "4580c9e")
        self.assertEqual(
            details["supersededResearchReferenceStatus"],
            "not-resolvable-in-local-clone-or-refs",
        )
        self.assertEqual(
            details["supersededResearchDecision"],
            "Use the approved immutable v0.3.0 release identity above.",
        )

    def test_hmlr_superseded_reference_identity_fails_closed(self) -> None:
        publication = load_json(ROOT / "okf" / "source" / "publication.json")
        source_lock = load_json(ROOT / "okf" / "source-lock.json")
        for field, value in (
            ("recorded_commit_prefix", "different"),
            ("status", "resolved"),
            ("status", None),
            ("decision", "Use mutable main."),
        ):
            changed = copy.deepcopy(source_lock)
            changed["supersedes_unresolved_research_reference"][field] = value
            with self.subTest(field=field, value=value), self.assertRaisesRegex(
                ValueError, "superseded research reference"
            ):
                BUILDER.hmlr_release_source_record(changed, publication)

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
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(), entry["sha256"]
            )

        checksum_bytes = (self.output / "CHECKSUMS.sha256").read_bytes()
        checksum_rows = []
        for line in checksum_bytes.decode("utf-8").splitlines():
            digest, relative = line.split("  ", 1)
            self.assertNotIn("..", Path(relative).parts)
            self.assertEqual(
                hashlib.sha256((self.output / relative).read_bytes()).hexdigest(),
                digest,
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
            ROOT / "okf/vendor/okf-landregistry/v0.3.0/source/curated-records.json"
        )["records"]
        rights = load_json(
            ROOT
            / "okf/vendor/okf-landregistry/v0.3.0/source/curated-rights-access.json"
        )["classifications"]
        record = next(
            row for row in records if row["id"] == "hmlr:dataset:price-paid-data"
        )
        classification = copy.deepcopy(
            next(row for row in rights if row["source_native_id"] == record["id"])
        )
        classification["rights_state"] = "unknown"
        publication = load_json(ROOT / "okf" / "source" / "publication.json")
        with self.assertRaisesRegex(ValueError, "publishable rights"):
            BUILDER.hmlr_dataset_record(
                record, classification, ["S-HMLR-PPD"], publication
            )
        classification["rights_state"] = "open-with-conditions"
        classification["access_state"] = "unknown"
        with self.assertRaisesRegex(ValueError, "publishable rights"):
            BUILDER.hmlr_dataset_record(
                record, classification, ["S-HMLR-PPD"], publication
            )

        missing_attribution = copy.deepcopy(publication)
        missing_attribution["attribution_by_record"].pop(record["id"])
        classification["access_state"] = "public"
        with self.assertRaisesRegex(ValueError, "explicit attribution"):
            BUILDER.hmlr_dataset_record(
                record, classification, ["S-HMLR-PPD"], missing_attribution
            )

    def test_selected_provider_digests_and_mixed_rights_fail_closed(self) -> None:
        publication = load_json(ROOT / "okf" / "source" / "publication.json")
        source_lock = load_json(ROOT / "okf" / "source-lock.json")
        changed_digest = copy.deepcopy(publication)
        changed_digest["selected"]["research_provider_sha256_by_id"]["PV-ONS-DATA"] = (
            "0" * 64
        )
        with self.assertRaisesRegex(ValueError, "selected provider digest mismatch"):
            BUILDER.build_records(ROOT, changed_digest, source_lock)

        changed_question_digest = copy.deepcopy(publication)
        changed_question_digest["selected"]["hmlr_question_sha256_by_id"]["LR-Q012"] = (
            "0" * 64
        )
        with self.assertRaisesRegex(
            ValueError, "selected HMLR question digest mismatch"
        ):
            BUILDER.build_records(ROOT, changed_question_digest, source_lock)

        changed_release = copy.deepcopy(source_lock)
        changed_release["external_release"]["commit"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "approved v0.3.0 pin"):
            BUILDER.hmlr_release_source_record(changed_release, publication)

        providers_doc = load_json(
            ROOT / "docs/research/2026-08-19/research-pack/data/providers.json"
        )
        landis = copy.deepcopy(
            next(row for row in providers_doc["providers"] if row["id"] == "PV-LANDIS")
        )
        landis["licence"] = "Open Government Licence"
        with self.assertRaisesRegex(ValueError, "per-record rights wording"):
            BUILDER.provider_record(landis, publication, providers_doc["generated_at"])
        landis["access_tier"] = []
        with self.assertRaisesRegex(ValueError, "no described access tiers"):
            BUILDER.provider_record(landis, publication, providers_doc["generated_at"])

    def test_hmlr_question_controls_fail_closed(self) -> None:
        suite = load_json(ROOT / BUILDER.HMLR_QUESTIONS)
        publication = load_json(ROOT / "okf" / "source" / "publication.json")
        caveats = {row["id"]: row["text"] for row in suite["caveat_registry"]}
        hard_failures = {row["id"] for row in suite["hard_failures"]}
        original = next(row for row in suite["questions"] if row["id"] == "LR-Q003")
        source_refs = [
            BUILDER.source_record_id(source["canonical_url"])
            for source in original["expected_sources"]
        ]

        def project(question: dict[str, Any]) -> dict[str, Any]:
            return BUILDER.hmlr_question_record(
                question,
                source_refs,
                caveats,
                hard_failures,
                suite["research_cutoff"],
                BUILDER.canonical_record_sha256(question),
                publication,
            )

        missing_caveat = copy.deepcopy(original)
        missing_caveat["required_caveat_ids"] = []
        with self.assertRaisesRegex(ValueError, "lacks mandatory caveats"):
            project(missing_caveat)

        unknown_caveat = copy.deepcopy(original)
        unknown_caveat["required_caveat_ids"] = ["CAV-NOT-REGISTERED"]
        with self.assertRaisesRegex(ValueError, "unknown mandatory caveats"):
            project(unknown_caveat)

        missing_hard_failure = copy.deepcopy(original)
        missing_hard_failure["hard_failure_ids"] = []
        with self.assertRaisesRegex(ValueError, "lacks hard-failure controls"):
            project(missing_hard_failure)

        source_mismatch = copy.deepcopy(original)
        source_mismatch["runtime_expected_source_url"] = "https://example.invalid/"
        with self.assertRaisesRegex(ValueError, "outside its positive sources"):
            project(source_mismatch)

        target_overlap = copy.deepcopy(original)
        target_overlap["must_not_retrieve"][0]["canonical_url"] = original[
            "expected_sources"
        ][0]["canonical_url"]
        with self.assertRaisesRegex(ValueError, "both required and forbidden"):
            project(target_overlap)

        no_forbidden_target = copy.deepcopy(original)
        no_forbidden_target["must_not_retrieve"] = []
        with self.assertRaisesRegex(ValueError, "requires unique forbidden targets"):
            project(no_forbidden_target)

        wrong_digest = copy.deepcopy(original)
        with self.assertRaisesRegex(ValueError, "question digest mismatch"):
            BUILDER.hmlr_question_record(
                wrong_digest,
                source_refs,
                caveats,
                hard_failures,
                suite["research_cutoff"],
                "0" * 64,
                publication,
            )

    def test_forbidden_payload_keys_and_unsafe_urls_fail_closed(self) -> None:
        profile = load_json(ROOT / "okf" / "profile" / "public-discovery-v1.json")
        forbidden = {
            BUILDER.canonical_key(key) for key in profile["forbidden_payload_keys"]
        }
        for key in (
            "address",
            "apiKey",
            "certificate",
            "cookie",
            "feature",
            "geometry",
            "logo",
            "ownership",
            "serviceResponse",
            "signedUrl",
            "titleNumber",
            "uprn",
        ):
            with (
                self.subTest(key=key),
                self.assertRaisesRegex(ValueError, "forbidden payload key"),
            ):
                BUILDER.reject_forbidden_keys({"nested": {key: "blocked"}}, forbidden)
        BUILDER.reject_forbidden_keys(self.bundle, forbidden)
        for value in ("javascript:alert(1)", "file:///tmp/data", "../escape"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                BUILDER.validate_url(value)

        output_text = b"\n".join(file_bytes(self.output).values()).decode("utf-8")
        for forbidden_url in (
            "https://businessgateway.landregistry.gov.uk/bg2/s1/v1",
            "https://github.com/LandRegistry/address-search-api",
            "https://use-land-property-data.service.gov.uk/datasets/nps",
        ):
            with self.subTest(url=forbidden_url):
                self.assertNotIn(forbidden_url, output_text)

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

    def test_coordinated_hmlr_source_and_lock_mutation_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_lock = copy_locked_inputs(root)
            records_path = root / BUILDER.HMLR_VENDOR / "source/curated-records.json"
            rights_path = (
                root / BUILDER.HMLR_VENDOR / "source/curated-rights-access.json"
            )
            records_doc = load_json(records_path)
            rights_doc = load_json(rights_path)
            record = next(
                row
                for row in records_doc["records"]
                if row["id"] == "hmlr:dataset:price-paid-data"
            )
            record["description"] = (
                "Validation mutation not present in the approved upstream release."
            )
            rights = next(
                row
                for row in rights_doc["classifications"]
                if row["source_native_id"] == record["id"]
            )
            rights["curated_record_sha256"] = BUILDER.canonical_record_sha256(record)
            records_path.write_bytes(BUILDER.canonical_json_bytes(records_doc))
            rights_path.write_bytes(BUILDER.canonical_json_bytes(rights_doc))

            lock_by_path = {item["path"]: item for item in source_lock["inputs"]}
            for path in (records_path, rights_path):
                relative = path.relative_to(root).as_posix()
                lock_by_path[relative]["sha256"] = hashlib.sha256(
                    path.read_bytes()
                ).hexdigest()

            BUILDER.verify_source_lock(root, source_lock)
            publication = load_json(root / "okf/source/publication.json")
            with self.assertRaisesRegex(
                ValueError, "approved v0.3.0 input hash mismatch"
            ):
                BUILDER.build_records(root, publication, source_lock)

    def test_coordinated_hmlr_licence_and_lock_mutation_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source_lock = copy_locked_inputs(root)
            licence_path = root / BUILDER.HMLR_VENDOR / "LICENSE.md"
            licence_path.write_bytes(licence_path.read_bytes() + b"\nAltered terms.\n")
            relative = licence_path.relative_to(root).as_posix()
            lock_entry = next(
                item for item in source_lock["inputs"] if item["path"] == relative
            )
            lock_entry["sha256"] = hashlib.sha256(licence_path.read_bytes()).hexdigest()

            BUILDER.verify_source_lock(root, source_lock)
            with self.assertRaisesRegex(
                ValueError, "approved v0.3.0 input hash mismatch"
            ):
                BUILDER.verify_approved_hmlr_inputs(root)

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
