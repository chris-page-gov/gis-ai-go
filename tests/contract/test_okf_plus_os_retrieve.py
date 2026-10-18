"""Offline synthetic contracts for private OS retrieval; no provider calls."""
from __future__ import annotations

import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit, parse_qs

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/okf_plus"))
import os_retrieve as fetch
import os_credentials
import retrieval_plan

SCHEMA = b'{"$id":"trn-ntwk-synthetic-1.0","type":"object"}'
CRS = fetch.CRS3D
KEY = "synthetic-private-key-never-print"


def fixture(root):
    row = {"id": "trn-ntwk-synthetic-1", "storageCrs": CRS, "crs": [CRS, fetch.CRS84],
           "schemas": {"schema": {"id": "trn-ntwk-synthetic-1.0", "sha256": fetch.digest(SCHEMA)},
                       "queryables": {"properties": {"width": {}, "name": {}}, "sha256": "a" * 64}}}
    source = root / "okf-plus/source"
    source.mkdir(parents=True)
    (source / "os-ngd-collections.json").write_text(json.dumps({"records": [row]}))
    return {"schema": "okf-plus-os-retrieve-request.v1", "collectionId": row["id"],
            "schemaId": row["schemas"]["schema"]["id"], "schemaSha256": fetch.digest(SCHEMA),
            "bbox": [-2, 52, -1, 53], "pageSize": 2}


def page(next_url=None, count=2, start=0):
    return fetch.canonical({"type": "FeatureCollection", "numberReturned": count,
                            "features": [{"type": "Feature", "id": f"synthetic-{i}",
                                          "properties": {"width": None, "evidence": "synthetic"},
                                          "geometry": {"type": "Point", "coordinates": [400000, 250000, 82.25]}}
                                         for i in range(start, start + count)],
                            "links": [{"rel": "next", "href": next_url}] if next_url is not None else []})


def continuation(bound, offset=2, **changes):
    return fetch.BASE + bound["request"]["collectionId"] + "/items?" + urlencode({**bound["query"], "offset": offset, **changes})


class Response(io.BytesIO):
    def __init__(self, raw, url, **headers):
        super().__init__(raw)
        self.url = url
        self.headers = {"Content-Type": "application/json", "Content-Crs": "<" + CRS + ">", **headers}

    def getcode(self):
        return 200

    def geturl(self):
        return self.url


class Opener:
    def __init__(self, *replies):
        self.replies = list(replies)
        self.requests = []

    def open(self, request, **_kwargs):
        self.requests.append(request)
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        if callable(reply):
            return reply(request)
        return Response(reply, request.full_url)


class Limiter:
    def __init__(self, wait=None):
        self.attempts = 0
        self.wait = wait
        self.deferred = []

    def reserve_attempt(self, service, interval):
        assert service == "ngd-features" and interval >= 1.5
        self.attempts += 1
        return {"allowed": self.wait is None, "notBefore": self.wait, "delay": 60 if self.wait else 0}

    def defer_retry_after(self, service, value):
        self.deferred.append((service, value))
        return 9999999999


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.request = fixture(self.root)
        self.bound = fetch.prepare(self.request, self.root)
        self.environment = mock.patch.dict(os.environ, {"OS_API_KEY": KEY})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def run_fetch(self, *replies, **kwargs):
        opener = Opener(*replies)
        result = fetch.retrieve(self.request, root=self.root, opener=opener, limiter=kwargs.pop("limiter", Limiter()), **kwargs)
        return result, opener

    def directory(self):
        return self.root / "artifacts/okf-plus/os-retrieval" / fetch.digest(fetch.canonical(self.bound))

    def test_private_pages_preserve_geometry_nulls_and_header_only_key(self):
        raw = page()
        result, opener = self.run_fetch(SCHEMA, raw)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(opener.requests[0].get_header("Key"), None)
        self.assertEqual(opener.requests[1].get_header("Key"), KEY)
        self.assertNotIn(KEY, opener.requests[1].full_url)
        self.assertEqual((self.directory() / "page-00000000.geojson").read_bytes(), raw)
        for file in self.directory().iterdir():
            self.assertEqual(file.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.directory().stat().st_mode & 0o777, 0o700)
        self.assertNotIn(KEY, (self.directory() / "checkpoint.json").read_text())
        self.assertFalse((self.root / "okf-plus/source/retrieval.json").exists())
        self.assertNotIn("82.25", json.dumps(result))
        self.assertEqual(result["sourceSchemaConformance"], "not-assessed")

    def test_page_ceiling_resumes_only_verified_source_next_url(self):
        next_url = continuation(self.bound)
        first, opener = self.run_fetch(SCHEMA, page(next_url), max_pages=1)
        self.assertEqual(first["status"], "run-page-ceiling")
        self.assertEqual(len(opener.requests), 2)
        second, opener = self.run_fetch(SCHEMA, page(count=1, start=2), max_pages=1)
        self.assertEqual(second["features"], 3)
        self.assertEqual(opener.requests[1].full_url, next_url)
        with mock.patch.dict(os.environ, {}, clear=True):
            final, opener = self.run_fetch(reuse_complete=True)
        self.assertEqual(final["status"], "complete")
        self.assertFalse(opener.requests)
        self.assertTrue(final["completedCaptureReused"])
        self.assertIsNotNone(final["capturedToUnix"])

    def test_query_changes_duplicates_credentials_redirect_and_offset_skips_rejected(self):
        initial = fetch.initial_url(self.bound)
        bad_urls = [continuation(self.bound, bbox="0,0,1,1"), continuation(self.bound, offset=4),
                    continuation(self.bound, key=KEY), continuation(self.bound) + "&limit=2",
                    continuation(self.bound).replace("api.os.uk", "evil.example"),
                    continuation(self.bound).replace("/items?", "/../items?"),
                    continuation(self.bound).replace("https://api.os.uk", "https://api.os.uk@evil.example"),
                    continuation(self.bound).replace("/items?", "/%69tems?"),
                    initial.split("?", 1)[0] + "?offset=2", continuation(self.bound) + "#fragment"]
        for url in bad_urls:
            with self.subTest(url=url), self.assertRaises(fetch.RetrievalError):
                fetch.inspect_page(page(url), self.bound, 0)

    def test_wrong_queryable_rejected_and_quoted_literal_not_treated_as_field(self):
        request = {**self.request, "cql": "name = 'height AND width' AND width >= 2"}
        bound = fetch.prepare(request, self.root)
        self.assertEqual(parse_qs(urlsplit(fetch.initial_url(bound)).query)["filter"], [request["cql"]])
        for expression in ("height > 2", "width > 2;key=bad", "width > 2 /* ignore */", "1 = 1"):
            with self.subTest(expression=expression), self.assertRaises(fetch.RetrievalError):
                fetch.prepare({**request, "cql": expression}, self.root)

    def test_schema_minor_pin_and_three_dimensional_crs_cannot_be_changed(self):
        for change in ({"schemaSha256": "b" * 64}, {"schemaId": "trn-ntwk-synthetic-1.1"},
                       {"returnCrs": fetch.CRS84}, {"collectionId": "trn-ntwk-synthetic-2"}):
            with self.subTest(change=change), self.assertRaises(fetch.RetrievalError):
                fetch.prepare({**self.request, **change}, self.root)

    def test_upstream_minor_schema_change_stops_before_licensed_request(self):
        result, opener = self.run_fetch(SCHEMA + b" ")
        self.assertEqual(result["status"], "upstream-schema-changed")
        self.assertEqual(len(opener.requests), 1)
        self.assertIsNone(opener.requests[0].get_header("Key"))

    def test_response_crs_mismatch_prevents_page_commit(self):
        result, _ = self.run_fetch(SCHEMA, lambda request: Response(page(), request.full_url, **{"Content-Crs": fetch.CRS84}))
        self.assertEqual(result["status"], "response-crs-mismatch")
        self.assertEqual(result["pages"], 0)

    def test_per_run_byte_ceiling_does_not_commit_truncated_page(self):
        raw = page()
        result, _ = self.run_fetch(SCHEMA, raw, max_bytes=len(SCHEMA) + len(raw) - 1)
        self.assertEqual(result["status"], "response-byte-ceiling")
        self.assertEqual(result["pages"], 0)
        result, _ = self.run_fetch(SCHEMA, raw)
        self.assertEqual(result["status"], "complete")

    def test_corrupt_checkpoint_is_rejected_before_network(self):
        self.run_fetch(SCHEMA, page(continuation(self.bound)), max_pages=1)
        checkpoint = self.directory() / "checkpoint.json"
        wrapper = json.loads(checkpoint.read_text())
        wrapper["state"]["nextUrl"] = continuation(self.bound, offset=80)
        checkpoint.write_text(json.dumps(wrapper))
        with self.assertRaisesRegex(fetch.RetrievalError, "checkpoint-integrity"):
            self.run_fetch()

    def test_rehashed_checkpoint_still_must_match_page_chain(self):
        self.run_fetch(SCHEMA, page(continuation(self.bound)), max_pages=1)
        wrapper = json.loads((self.directory() / "checkpoint.json").read_text())
        state = wrapper["state"]
        state["nextUrl"] = continuation(self.bound, offset=80)
        fetch._save(self.directory(), state)
        with self.assertRaisesRegex(fetch.RetrievalError, "checkpoint-continuation"):
            self.run_fetch()

    def test_corrupt_committed_page_is_rejected_before_network(self):
        self.run_fetch(SCHEMA, page(continuation(self.bound)), max_pages=1)
        (self.directory() / "page-00000000.geojson").write_bytes(page(count=1))
        with self.assertRaisesRegex(fetch.RetrievalError, "page-integrity"):
            self.run_fetch()

    def test_shared_limiter_denies_before_egress(self):
        result, opener = self.run_fetch(limiter=Limiter(wait=9999999999))
        self.assertEqual(result["status"], "rate-wait")
        self.assertFalse(opener.requests)

    def test_retry_after_is_durable_and_has_no_automatic_retry(self):
        limiter = Limiter()
        failure = HTTPError("https://api.os.uk/private?key=" + KEY, 429, KEY, {"Retry-After": "120"}, io.BytesIO(KEY.encode()))
        result, opener = self.run_fetch(SCHEMA, failure, limiter=limiter)
        self.assertEqual(result["status"], "provider-rate-wait")
        self.assertEqual(limiter.deferred, [("ngd-features", "120")])
        self.assertEqual(len(opener.requests), 2)
        self.assertNotIn(KEY, json.dumps(result))
        self.assertNotIn(KEY, (self.directory() / "checkpoint.json").read_text())

    def test_provider_error_text_is_not_in_checkpoint_or_summary(self):
        result, _ = self.run_fetch(URLError(KEY + " private-account"))
        self.assertEqual(result["status"], "provider-transport-error")
        self.assertNotIn(KEY, json.dumps(result))
        self.assertNotIn("private-account", (self.directory() / "checkpoint.json").read_text())

    def test_symlink_or_public_page_is_rejected(self):
        self.run_fetch(SCHEMA, page(continuation(self.bound)), max_pages=1)
        target = self.directory() / "page-00000000.geojson"
        os.chmod(target, 0o644)
        with self.assertRaisesRegex(fetch.RetrievalError, "unsafe-private-file"):
            self.run_fetch()
        os.chmod(target, 0o600)
        checkpoint = self.directory() / "checkpoint.json"
        checkpoint.unlink()
        checkpoint.symlink_to(target)
        with self.assertRaisesRegex(fetch.RetrievalError, "unsafe-private-file"):
            self.run_fetch()

    def test_redirect_handler_does_not_follow_any_destination(self):
        outgoing = fetch.Request(fetch.initial_url(self.bound), headers={"key": KEY})
        with self.assertRaises(HTTPError):
            fetch.NoRedirect().redirect_request(outgoing, None, 302, "redirect", {}, "https://api.os.uk/other")

    def test_empty_continuation_duplicate_json_and_wrong_count_rejected(self):
        bodies = [page(continuation(self.bound), count=0), b'{"type":"FeatureCollection","type":"evil"}',
                  page().replace(b'"numberReturned":2', b'"numberReturned":3')]
        for raw in bodies:
            with self.subTest(raw=raw), self.assertRaises(fetch.RetrievalError):
                fetch.inspect_page(raw, self.bound, 0)

    def test_plan_reports_unknown_time_and_download_option_without_private_scope(self):
        bound = fetch.prepare({**self.request, "cql": "name = 'private-sensitive-location'"}, self.root)
        result = fetch._retrieval_plan(bound["request"], bound)
        self.assertIsNone(result["candidates"][0]["estimate"]["seconds"]["upper"])
        self.assertIn("download", result["downloadAlternative"])
        self.assertNotIn("private-sensitive-location", json.dumps(result))

    def test_unknown_request_fields_and_nonfinite_bbox_are_rejected(self):
        for change in ({"key": KEY}, {"bbox": [float("nan"), 1, 2, 3]}, {"wholeCollection": True}):
            with self.subTest(change=change), self.assertRaises(fetch.RetrievalError):
                fetch.prepare({**self.request, **change}, self.root)

    def test_reflected_secret_is_not_retained_even_inside_valid_feature_page(self):
        raw = page().replace(b"synthetic\"", KEY.encode() + b'"')
        result, _ = self.run_fetch(SCHEMA, raw)
        self.assertEqual(result["status"], "credential-reflected-in-response")
        self.assertEqual(result["pages"], 0)
        for file in self.directory().iterdir():
            self.assertNotIn(KEY.encode(), file.read_bytes())

    def test_repeated_feature_versions_cannot_inflate_completeness(self):
        result, _ = self.run_fetch(SCHEMA, page(continuation(self.bound)), page())
        self.assertEqual(result["status"], "repeated-feature-version")
        self.assertFalse(result["completeWithinRequestedScope"])
        self.assertEqual(result["pages"], 1)

    def test_repeated_id_with_distinct_native_version_is_preserved(self):
        raw = page().replace(b'"width":null', b'"versiondate":"2026-10-18","width":null')
        result, _ = self.run_fetch(SCHEMA, page(continuation(self.bound)), raw)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["features"], 4)

    def test_completed_capture_needs_explicit_reuse_or_new_run_identity(self):
        self.run_fetch(SCHEMA, page())
        with self.assertRaisesRegex(fetch.RetrievalError, "requires-reuse-or-new-run-id"):
            self.run_fetch()
        self.request["runId"] = "fresh-capture"
        result, opener = self.run_fetch(SCHEMA, page())
        self.assertEqual(result["status"], "complete")
        self.assertFalse(result["completedCaptureReused"])
        self.assertEqual(len(opener.requests), 2)

    def test_temporal_selection_can_scope_request_without_inventing_version_predicate(self):
        request = {key: value for key, value in self.request.items() if key != "bbox"}
        request["datetime"] = "2026-10-01T00:00:00Z/2026-10-18T00:00:00Z"
        bound = fetch.prepare(request, self.root)
        self.assertEqual(bound["query"]["datetime"], request["datetime"])
        self.assertNotIn("filter", bound["query"])

    def test_estimate_uses_actual_budget_no_retry_and_stricter_unknown_project_limit(self):
        with mock.patch.object(retrieval_plan, "plan_retrieval", wraps=retrieval_plan.plan_retrieval) as planner:
            fetch._retrieval_plan(self.request, self.bound)
        estimate = planner.call_args.args[0]
        estimate["project"].update(callerCeilingPerMinute=10, reservedTransactionsPerMinute=2)
        estimate["project"]["additionalRateLimits"] = [{"scope": "account", "transactionsPerMinute": 9,
                                                         "sourceUrl": "https://docs.os.uk/synthetic-policy"}]
        estimate["executionBudget"] = {"maxRequests": 1, "maxElapsedSeconds": 1, "maxBytes": 1}
        estimate["retryPolicy"] = {"maxRetriesPerRequest": 5, "maxWaitPerRetrySeconds": 60}
        result = fetch._retrieval_plan(self.request, self.bound, estimate, 4, 1024, 25)
        self.assertEqual(result["executorTransactionsPerMinuteCeiling"], 7)
        self.assertEqual(result["executionBudget"], {"maxRequests": 5, "maxElapsedSeconds": 25, "maxBytes": 1024})
        self.assertEqual(result["retryPolicy"]["maxRetriesPerRequest"], 0)

    def test_total_time_ceiling_stops_before_next_request(self):
        with mock.patch.object(fetch.time, "monotonic", side_effect=[0, 0, 0, 301]):
            result, opener = self.run_fetch(SCHEMA)
        self.assertEqual(result["status"], "run-time-ceiling")
        self.assertEqual(len(opener.requests), 1)

    def test_unrepresentable_retry_after_durably_stops_without_echo(self):
        limiter = Limiter()
        limiter.defer_retry_after = mock.Mock(side_effect=RuntimeError(KEY))
        error = HTTPError("https://api.os.uk", 429, KEY, {"Retry-After": "9" * 301}, io.BytesIO())
        result, _ = self.run_fetch(error, limiter=limiter)
        self.assertEqual(result["status"], "provider-rate-blocked")
        self.assertNotIn(KEY, json.dumps(result))

    def test_private_key_file_fallback_used_in_preflight_and_header_only(self):
        directory = self.root / ".secrets"
        directory.mkdir(mode=0o700)
        file = directory / "os_api_key"
        file.write_text("synthetic-fallback-key\n")
        file.chmod(0o600)
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(os_credentials.Path, "home", return_value=self.root):
            plan = fetch._retrieval_plan(self.request, self.bound)
            result, opener = self.run_fetch(SCHEMA, page())
        self.assertEqual(plan["credential"], "credential-present")
        self.assertEqual(opener.requests[1].get_header("Key"), "synthetic-fallback-key")
        self.assertNotIn("synthetic-fallback-key", json.dumps(plan) + json.dumps(result))


if __name__ == "__main__":
    unittest.main()
