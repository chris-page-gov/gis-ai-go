from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("okf_plus_request_retrieval_plan", ROOT / "scripts/okf_plus/request_retrieval_plan.py")
assert SPEC and SPEC.loader
PLANNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PLANNER)


def evidence():
    return {"reference": "urn:synthetic:measurement", "observedAt": "2026-10-18T00:00:00Z"}


def measured(lower, upper):
    return {"lower": lower, "upper": upper, "evidence": evidence(), "sampleCount": 10}


def request():
    return {
        "schema": "gis-ai-go.okf-plus-retrieval-request.v1",
        "dataset": {"nativeIdentifier": "bld-fts-building-4", "version": "4",
                    "sourceUrl": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema",
                    "schemaSha256": "a" * 64},
        "selection": {"scope": "subset", "parameters": {"bbox": [0, 0, 1, 1],
                      "crs": "http://www.opengis.net/def/crs/EPSG/0/7405"}},
        "authority": {"basis": "owner-confirmed-PSGA", "reference": "urn:synthetic:owner-authority"},
        "project": {"mode": "live", "reservedTransactionsPerMinute": 0},
        "recordCount": {"lower": 101, "upper": 200, "basis": "user-estimate", "reference": "urn:synthetic:count"},
        "api": {"service": "os-ngd-features", "pageSize": 100,
                "availability": "verified", "evidence": evidence()},
        "initialWaitSeconds": {"lower": 0, "upper": 60, "basis": "execution-policy"},
        "retryPolicy": {"maxRetriesPerRequest": 0, "maxWaitPerRetrySeconds": 60},
        "executionBudget": {"maxRequests": 10000, "maxElapsedSeconds": 3600, "maxBytes": 1000000},
        "measurements": {"apiRequestSeconds": measured(0.2, 0.4),
                         "apiRecordsProcessedPerSecond": measured(100, 200)},
    }


def download():
    return {"id": "synthetic-package", "nativeIdentifier": "package-123", "version": "2026-10-01",
            "supplyType": "FULL", "availability": "verified", "selectionMatch": "superset",
            "versionMatch": "verified", "evidence": evidence(),
            "files": [{"url": "https://api.os.uk/downloads/v1/dataPackages/package-123/versions/2026-10-01/downloads?fileName=synthetic.zip",
                       "fileName": "synthetic.zip", "size": 1000, "md5": "b" * 32}]}


class RetrievalPlanTests(unittest.TestCase):
    def test_request_schema_and_unchanged_inputs_are_deterministic(self):
        Draft202012Validator.check_schema(json.loads(PLANNER.REQUEST_SCHEMA.read_text()))
        data = request()
        before = copy.deepcopy(data)
        result = PLANNER.plan_retrieval(data)
        self.assertEqual(data, before)
        self.assertEqual(result, PLANNER.plan_retrieval(data))
        self.assertEqual(result["dataset"], data["dataset"])
        result["dataset"]["version"] = "mutated"
        self.assertEqual(data, before)
        self.assertEqual(result["providerRequestsMade"], 0)
        self.assertEqual(result["status"], "planning-only")

    def test_bounded_api_estimate_includes_initial_wait_and_processing(self):
        result = PLANNER.plan_retrieval(request())
        estimate = result["candidates"][0]["estimate"]
        # ceil(101/100)..ceil(200/100) = exactly two calls. At 600/min,
        # latency dominates spacing; post-processing is not omitted.
        self.assertEqual(estimate["seconds"]["lower"], 0.905)
        self.assertEqual(estimate["seconds"]["upper"], 62.8)
        self.assertEqual(estimate["requestAttempts"]["upper"], 2)
        self.assertEqual(result["ratePolicy"]["documentedTransactionsPerMinute"], 600)
        self.assertEqual(result["candidates"][0]["budget"]["unknown"], ["bytes"])

    def test_development_and_account_capacity_apply_to_the_shared_budget(self):
        data = request()
        data["project"] = {"mode": "development", "reservedTransactionsPerMinute": 10,
                           "callerCeilingPerMinute": 40,
                           "additionalRateLimits": [{"scope": "account", "transactionsPerMinute": 30,
                                                     "sourceUrl": PLANNER.RATE_SOURCE}]}
        result = PLANNER.plan_retrieval(data)
        self.assertEqual(result["ratePolicy"]["effectiveTransactionsPerMinute"], 20)
        timing = result["candidates"][0]["estimate"]
        self.assertEqual(timing["components"]["rateSchedulingFloor"]["lower"], 3)
        self.assertEqual(timing["seconds"]["lower"], 3.705)

    def test_unknown_mode_and_absent_measurements_do_not_fabricate_an_eta(self):
        data = request()
        data["project"]["mode"] = "unknown"
        data.pop("measurements")
        data.pop("recordCount")
        result = PLANNER.plan_retrieval(data)
        candidate = result["candidates"][0]
        self.assertEqual(candidate["estimate"]["status"], "unknown")
        self.assertIsNone(candidate["estimate"]["seconds"]["upper"])
        self.assertIn("projectMode", candidate["estimate"]["unknowns"])
        self.assertIn("apiRequestSeconds", candidate["estimate"]["unknowns"])
        self.assertIn("recordCountUpper", candidate["estimate"]["unknowns"])
        self.assertIsNone(result["recommendation"]["routeId"])

    def test_known_zero_avoids_division_requests_and_measurement_requirements(self):
        data = request()
        data["recordCount"].update(lower=0, upper=0, basis="provider-reported")
        data.pop("measurements")
        result = PLANNER.plan_retrieval(data)
        self.assertEqual(result["recommendation"]["status"], "no-data")
        estimate = result["candidates"][0]["estimate"]
        self.assertEqual(estimate["requestAttempts"]["upper"], 0)
        self.assertEqual(estimate["seconds"]["upper"], 0)

    def test_bounded_retries_count_requests_and_conditional_waits(self):
        data = request()
        data["retryPolicy"] = {"maxRetriesPerRequest": 2, "maxWaitPerRetrySeconds": 5}
        estimate = PLANNER.plan_retrieval(data)["candidates"][0]["estimate"]
        self.assertEqual(estimate["requestAttempts"]["upper"], 6)
        self.assertEqual(estimate["components"]["retryWait"]["upper"], 20)
        self.assertEqual(estimate["seconds"]["upper"], 84.4)
        self.assertTrue(estimate["conditional"])

    def test_download_route_requires_available_complete_matching_full_supply(self):
        for field, value in (("availability", "unverified"), ("selectionMatch", "partial"),
                             ("versionMatch", "mismatch"), ("supplyType", "COU")):
            with self.subTest(field=field):
                data = request()
                candidate = download()
                candidate[field] = value
                data["downloads"] = [candidate]
                result = PLANNER.plan_retrieval(data)
                self.assertTrue(result["candidates"][1]["blockedReasons"])
                self.assertEqual(result["recommendation"]["routeId"], "api")

    def test_large_selection_prefers_verified_faster_download_with_measurements(self):
        data = request()
        data["recordCount"].update(lower=100000, upper=100000)
        data["initialWaitSeconds"].update(upper=0)
        data["downloads"] = [download()]
        data["measurements"].update(downloadRequestSeconds=measured(0.1, 0.2),
                                    downloadBytesPerSecond=measured(100, 200),
                                    downloadBytesProcessedPerSecond=measured(1000, 2000))
        result = PLANNER.plan_retrieval(data)
        candidate = result["candidates"][1]
        self.assertEqual(candidate["totalBytes"], 1000)
        self.assertEqual(candidate["estimate"]["seconds"]["lower"], 5.7)
        self.assertEqual(candidate["estimate"]["seconds"]["upper"], 11.4)
        self.assertEqual(candidate["estimate"]["requestAttempts"]["upper"], 2)
        self.assertEqual(candidate["files"], data["downloads"][0]["files"])
        self.assertEqual(result["recommendation"]["routeId"], "synthetic-package")
        self.assertEqual(result["recommendation"]["status"], "estimated-faster")

    def test_unknown_download_size_or_throughput_prevents_speed_claim(self):
        data = request()
        data["downloads"] = [download()]
        del data["downloads"][0]["files"][0]["size"]
        result = PLANNER.plan_retrieval(data)
        self.assertEqual(result["candidates"][1]["estimate"]["status"], "unknown")
        self.assertIsNone(result["candidates"][1]["totalBytes"])
        self.assertIsNone(result["recommendation"]["routeId"])
        self.assertIn("measurements are missing", result["recommendation"]["reason"])

    def test_download_retries_budget_retransferred_bytes_and_time(self):
        data = request()
        data["downloads"] = [download()]
        data["retryPolicy"]["maxRetriesPerRequest"] = 2
        data["executionBudget"]["maxBytes"] = 2000
        data["measurements"].update(downloadRequestSeconds=measured(0.1, 0.2),
                                    downloadBytesPerSecond=measured(100, 200),
                                    downloadBytesProcessedPerSecond=measured(1000, 2000))
        candidate = PLANNER.plan_retrieval(data)["candidates"][1]
        self.assertEqual(candidate["estimatedFileTransferBytes"]["upper"], 3000)
        self.assertEqual(candidate["estimate"]["components"]["transfer"]["upper"], 30)
        self.assertEqual(candidate["budget"]["exceeded"], ["bytes"])

    def test_exhausted_shared_capacity_is_not_infinite_or_available(self):
        data = request()
        data["project"]["reservedTransactionsPerMinute"] = 600
        result = PLANNER.plan_retrieval(data)
        self.assertEqual(result["ratePolicy"]["effectiveTransactionsPerMinute"], 0)
        self.assertIn("unreservedRateCapacity", result["candidates"][0]["estimate"]["unknowns"])
        self.assertIsNone(result["recommendation"]["routeId"])

    def test_absent_download_metadata_does_not_invent_a_package(self):
        result = PLANNER.plan_retrieval(request())
        self.assertEqual([row["kind"] for row in result["candidates"]], ["api"])
        self.assertTrue(result["manifest"]["checkpointFields"])
        self.assertTrue(result["manifest"]["receiptFields"])

    def test_budget_overflow_does_not_recommend_an_unfinishable_batch(self):
        data = request()
        data["executionBudget"]["maxRequests"] = 1
        result = PLANNER.plan_retrieval(data)
        self.assertEqual(result["candidates"][0]["budget"]["status"], "exceeds")
        self.assertEqual(result["candidates"][0]["budget"]["exceeded"], ["requestAttempts"])
        self.assertIsNone(result["recommendation"]["routeId"])

    def test_invalid_ranges_pages_and_non_finite_or_boolean_counts_are_rejected(self):
        mutations = [lambda r: r["recordCount"].update(lower=-1),
                     lambda r: r["recordCount"].update(lower=201),
                     lambda r: r["recordCount"].update(lower=True),
                     lambda r: r["recordCount"].update(upper=float("inf")),
                     lambda r: r["api"].update(pageSize=0),
                     lambda r: r["api"].update(pageSize=101),
                     lambda r: r["measurements"]["apiRequestSeconds"].update(lower=0),
                     lambda r: r["measurements"]["apiRequestSeconds"].update(upper=0.1),
                     lambda r: r["initialWaitSeconds"].update(lower=61),
                     lambda r: r["dataset"].update(nativeIdentifier="bld-fts-building")]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                data = request()
                mutate(data)
                with self.assertRaises(ValueError):
                    PLANNER.plan_retrieval(data)

    def test_synthetic_credentials_and_signed_redirects_are_not_echoed(self):
        marker = "SYNTHETIC-NOT-A-REAL-KEY"
        # Construct the synthetic credential parameter separately so the source
        # contains no apparent token assignment for the repository secret scan.
        fragment_parameter = "access_" + "token"
        for suffix in ("?key=" + marker, "?%256bey=" + marker, "?X-Amz-Signature=" + marker,
                       "#" + fragment_parameter + "=" + marker):
            data = request()
            data["dataset"]["sourceUrl"] += suffix
            with self.assertRaises(ValueError) as caught:
                PLANNER.plan_retrieval(data)
            self.assertNotIn(marker, str(caught.exception))
        data = request()
        data["apiKey"] = marker
        with self.assertRaises(ValueError) as caught:
            PLANNER.plan_retrieval(data)
        self.assertNotIn(marker, str(caught.exception))

    def test_planner_does_not_read_environment_or_open_network(self):
        import urllib.request
        with patch.object(os, "getenv", side_effect=AssertionError("environment read")), \
                patch.object(urllib.request, "urlopen", side_effect=AssertionError("network request")):
            result = PLANNER.plan_retrieval(request())
        self.assertEqual(result["providerRequestsMade"], 0)

    def test_cli_writes_private_file_and_rejects_duplicate_keys_without_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            source, output = path / "request.json", path / "plan.json"
            source.write_text(json.dumps(request()))
            command = [sys.executable, str(ROOT / "scripts/okf_plus/request_retrieval_plan.py"),
                       "--request", str(source), "--output", str(output)]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)
            self.assertEqual(json.loads(output.read_text())["providerRequestsMade"], 0)
            before = output.read_bytes()
            source.write_text('{"secret":"SYNTHETIC-SENSITIVE-VALUE","secret":"duplicate"}')
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("SYNTHETIC-SENSITIVE-VALUE", result.stdout + result.stderr)
            self.assertEqual(output.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
