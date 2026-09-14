"""Portable current-CPIH validation tests using only a redacted local projection."""

from __future__ import annotations

import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import web216_current_cpih as cpih


FIXTURE = Path(__file__).parent / "fixtures/web216/current-cpih-projection.json"


class CurrentCpihTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = json.loads(FIXTURE.read_bytes())
        self.search, self.data = self.fixture["search"], self.fixture["data"]
        self.retrieved = self.fixture["retrieved_at"]
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def validate(self, period="latest") -> dict:
        return cpih.validate_current_cpih(self.search, self.data, retrieved_at=self.retrieved, period=period)

    def capture(self) -> tuple[Path, dict]:
        """A synthetic two-row capture, never presented as the original full body."""
        directory = self.root / "synthetic-capture"
        directory.mkdir()
        attempts = []
        for stage, body in (("search", self.search), ("data", self.data)):
            raw = cpih.canonical(body)
            (directory / f"{stage}.body.json").write_bytes(raw)
            attempts.append({
                "stage": stage, "status": 200, "body_complete": True,
                "body_sha256": hashlib.sha256(raw).hexdigest(), "bytes_retained": len(raw),
                "url": cpih.SOURCE_URLS[stage], "content_type": "application/json",
                "started_at": self.retrieved, "completed_at": self.retrieved,
            })
        manifest = {"outcome": "raw-responses-collected-pending-schema-validation",
                    "mcp_executed": False, "production_transport": False,
                    "started_at": self.retrieved, "completed_at": self.retrieved, "attempts": attempts}
        (directory / "run-manifest.json").write_bytes(cpih.canonical(manifest))
        return directory, manifest

    def test_fixture_is_hash_bound_redacted_projection_not_whole_response(self) -> None:
        self.assertEqual(self.fixture["projection_sha256"], cpih.digest(
            {key: value for key, value in self.fixture.items() if key != "projection_sha256"}))
        self.assertIn("not a whole-response fixture", self.fixture["projection_scope"])
        self.assertEqual(self.fixture["projected_month_count"], 2)
        self.assertEqual(self.fixture["full_captured_month_count"], 463)
        self.assertEqual(self.fixture["full_captured_period_range"], {"first": "1988-01", "last": "2026-07"})
        self.assertEqual(self.fixture["original_body_sha256"]["data"],
                         "7f9af141727981a21d040febcb8a71db9299455e910583ed3eefad446a50a3b9")
        self.assertNotEqual(cpih.digest(self.data), self.fixture["original_body_sha256"]["data"])
        self.assertNotIn("contact", self.data["description"])
        self.assertNotIn("@", FIXTURE.read_text())

    def test_latest_and_requested_month_preserve_index_strings(self) -> None:
        latest = self.validate()
        self.assertEqual(latest["selected_period"], "2026-07")
        self.assertEqual(latest["observation"]["value"], "142.7")
        self.assertEqual(latest["validated_month_count"], 2)
        self.assertEqual(latest["retained_observation_count"], 1)
        self.assertEqual(latest["measure_kind"], "index-not-percentage")
        self.assertEqual(latest["base_year"], 2015)
        self.assertIn("series title", latest["base_year_basis"])
        self.assertFalse(latest["selection_authorised"])
        self.assertFalse(latest["mcp_executed"])
        january = self.validate("2026-01")
        self.assertEqual(january["observation"]["value"], "139.4")
        self.assertEqual(january["observation"]["updateDate"], "2026-02-18T00:00:00.000Z")

    def test_latest_uses_actual_chronology_not_array_order(self) -> None:
        self.data["months"].reverse()
        self.assertEqual(self.validate()["selected_period"], "2026-07")

    def test_release_time_is_preserved_and_london_date_is_correct(self) -> None:
        result = self.validate()
        self.assertEqual(result["release_date"], "2026-08-18T23:00:00.000Z")
        self.assertEqual(result["release_date_london"], "2026-08-19")
        self.assertEqual(result["next_release"], "16 September 2026")
        self.assertEqual(result["next_release_validation"], "unvalidated-provider-text")
        self.assertEqual(result["retrieved_at"], self.retrieved)

    def test_next_release_is_preserved_as_unvalidated_provider_text(self) -> None:
        self.data["description"]["nextRelease"] = "To be announced"
        result = self.validate()
        self.assertEqual(result["next_release"], "To be announced")
        self.assertEqual(result["next_release_validation"], "unvalidated-provider-text")

    def test_wrong_search_identity_or_multiple_candidates_rejected(self) -> None:
        for key, value in (("cdid", "D7G7"), ("dataset_id", "OTHER"), ("type", "dataset"),
                           ("uri", "/different"), ("title", "CPI INDEX")):
            original = self.search["items"][0][key]
            self.search["items"][0][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "searched series"):
                self.validate()
            self.search["items"][0][key] = original
        self.search["items"].append(copy.deepcopy(self.search["items"][0]))
        with self.assertRaisesRegex(ValueError, "exactly one"):
            self.validate()

    def test_wrong_data_series_base_or_unit_rejected(self) -> None:
        for key, value in (("cdid", "D7BT"), ("datasetId", "OTHER"), ("unit", "Percent"),
                           ("title", "CPIH INDEX 00: ALL ITEMS 2016=100")):
            original = self.data["description"][key]
            self.data["description"][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "series, title or index unit"):
                self.validate()
            self.data["description"][key] = original

    def test_search_data_snapshot_race_rejected(self) -> None:
        self.search["items"][0]["release_date"] = "2026-07-15T00:00:00.000Z"
        with self.assertRaisesRegex(ValueError, "snapshot race"):
            self.validate()

    def test_duplicate_period_and_inconsistent_date_parts_rejected(self) -> None:
        self.data["months"].append(copy.deepcopy(self.data["months"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate monthly"):
            self.validate()
        self.data["months"].pop()
        self.data["months"][0]["month"] = "February"
        with self.assertRaisesRegex(ValueError, "Inconsistent monthly"):
            self.validate()

    def test_future_period_release_or_update_rejected(self) -> None:
        january = self.data["months"][0]
        january.update(date="2026 OCT", label="2026 OCT", month="October")
        with self.assertRaisesRegex(ValueError, "Future period"):
            self.validate()
        self.data = copy.deepcopy(self.fixture["data"])
        # self.fixture shares self.data before this reset; restore the known row.
        self.data["months"][0].update(date="2026 JAN", label="2026 JAN", month="January")
        self.data["months"][0]["updateDate"] = "2026-10-01T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "update is after"):
            self.validate()
        self.data["months"][0]["updateDate"] = "2026-02-18T00:00:00Z"
        self.data["description"]["releaseDate"] = "2026-10-01T00:00:00Z"
        self.search["items"][0]["release_date"] = "2026-10-01T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "release is after"):
            self.validate()

    def test_blanks_suppression_numbers_and_wrong_source_are_rejected(self) -> None:
        row = self.data["months"][-1]
        for value in ("", "[c]", "NaN", " 142.7", "+142.7", "0142.7", 142.7, 142, None):
            row["value"] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "monthly value"):
                self.validate()
        row["value"] = "142.7"
        row["suppressed"] = True
        with self.assertRaisesRegex(ValueError, "suppression metadata"):
            self.validate()
        del row["suppressed"]
        row["sourceDataset"] = "OTHER"
        with self.assertRaisesRegex(ValueError, "monthly source"):
            self.validate()

    def test_month_after_release_before_retrieval_is_rejected(self) -> None:
        self.data["months"][-1].update(date="2026 SEP", label="2026 SEP", month="September")
        self.data["description"]["date"] = "2026 SEP"
        with self.assertRaisesRegex(ValueError, "period is after the source release month"):
            self.validate()

    def test_update_after_release_before_retrieval_is_rejected(self) -> None:
        self.data["months"][-1]["updateDate"] = "2026-08-20T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "update is after the source release"):
            self.validate()

    def test_release_month_uses_london_not_utc_calendar(self) -> None:
        release = "2026-07-31T23:00:00Z"
        self.data["description"].update(releaseDate=release, date="2026 AUG")
        self.search["items"][0]["release_date"] = release
        self.data["months"][-1].update(date="2026 AUG", label="2026 AUG", month="August",
                                       updateDate=release)
        self.assertEqual(self.validate()["selected_period"], "2026-08")

    def test_missing_requested_period_is_not_silently_replaced(self) -> None:
        for period in ("2026-02", "2026-13", "2026-1", "current", ""):
            with self.subTest(period=period), self.assertRaises(ValueError):
                self.validate(period)

    def test_bound_row_count_and_headline_consistency(self) -> None:
        self.data["description"]["number"] = "999.9"
        with self.assertRaisesRegex(ValueError, "Headline observation"):
            self.validate()
        self.data["months"] *= cpih.MAX_MONTHS
        with self.assertRaisesRegex(ValueError, "excessive monthly"):
            self.validate()

    def test_missing_headline_fields_cannot_make_an_older_month_latest(self) -> None:
        for missing in (("date",), ("number",), ("date", "number")):
            data = copy.deepcopy(self.data)
            data["months"].pop()
            for key in missing:
                del data["description"][key]
            with self.subTest(missing=missing), self.assertRaisesRegex(ValueError, "Missing required headline"):
                cpih.validate_current_cpih(self.search, data, retrieved_at=self.retrieved)

    def test_capture_requires_two_hash_bound_successful_serial_attempts(self) -> None:
        directory, manifest = self.capture()
        result = cpih.validate_capture(directory)
        self.assertEqual(result["input_scope"], "full-captured-response")
        self.assertEqual(result["validated_month_count"], 2)
        for field, value in (("status", 429), ("body_complete", False), ("body_sha256", "0" * 64),
                             ("bytes_retained", 0), ("url", "https://example.org/data")):
            changed = copy.deepcopy(manifest)
            changed["attempts"][1][field] = value
            (directory / "run-manifest.json").write_bytes(cpih.canonical(changed))
            with self.subTest(field=field), self.assertRaises(ValueError):
                cpih.validate_capture(directory)
        manifest["outcome"] = "claimed-success"
        (directory / "run-manifest.json").write_bytes(cpih.canonical(manifest))
        with self.assertRaisesRegex(ValueError, "manifest outcome"):
            cpih.validate_capture(directory)

    def test_changed_raw_bytes_duplicate_json_and_nan_fail_closed(self) -> None:
        directory, _ = self.capture()
        path = directory / "data.body.json"
        for raw in (cpih.canonical(self.data) + b" ", b'{"x":1,"x":2}', b'{"x":NaN}',
                    b'{"x":1e999}', b" " * (cpih.MAX_BYTES + 1)):
            path.write_bytes(raw)
            with self.subTest(size=len(raw)), self.assertRaises(ValueError):
                cpih.validate_capture(directory)

    def test_capture_binds_validator_and_imported_source_dependency(self) -> None:
        directory, _ = self.capture()
        result = cpih.validate_capture(directory)
        paths = {"scripts/web216_current_cpih.py": Path(cpih.__file__),
                 "scripts/web216_corpus.py": Path(cpih._corpus_module.__file__)}
        expected = {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()}
        self.assertEqual(result["validator_source_sha256"], expected)
        self.assertEqual(result["validator_sha256"], expected["scripts/web216_current_cpih.py"])
        original_read = Path.read_bytes
        for name, changed_path in paths.items():
            def mutated_read(path: Path) -> bytes:
                raw = original_read(path)
                return raw + b"\n# Synthetic source mutation\n" if path == changed_path else raw

            with self.subTest(source=name), patch.object(Path, "read_bytes", mutated_read):
                changed = cpih.validate_capture(directory)
            self.assertNotEqual(changed["validator_source_sha256"][name], expected[name])
            self.assertNotEqual(changed["result_sha256"], result["result_sha256"])
            self.assertEqual(changed["original_body_sha256"], result["original_body_sha256"])

    def test_cli_output_is_fresh_and_does_not_overwrite(self) -> None:
        directory, _ = self.capture()
        output = self.root / "result.json"
        args = ["web216_current_cpih.py", "--capture-directory", str(directory),
                "--period", "2026-01", "--output", str(output)]
        with patch("sys.argv", args), patch("sys.stdout", new_callable=io.StringIO):
            self.assertEqual(cpih.main(), 0)
        original = output.read_bytes()
        self.assertEqual(json.loads(original)["observation"]["value"], "139.4")
        with (patch("sys.argv", args), patch("sys.stderr", new_callable=io.StringIO),
              self.assertRaises(SystemExit)):
            cpih.main()
        self.assertEqual(output.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
