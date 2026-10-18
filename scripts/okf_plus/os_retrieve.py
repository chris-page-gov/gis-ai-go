#!/usr/bin/env python3
"""Private, resumable OS NGD retrieval, invoked only for a dataset request.

Source: OS NGD Features /technical-specification/features.md, captured SHA-256
c2b126fcbb5d412b4e0e93f6858e7258a6a511b8d313330669c1a237699a0059:
GET items, limit 1..100, offset pagination, CQL text, explicit request/return CRS.
The key header was separately observed in SITES-218_NGD_VALIDATION.md. Default
urllib TLS/proxy behaviour is preserved. No redirect, geographic conversion,
full-record schema-conformance claim, generic URL input or gateway registration.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from jsonschema import Draft202012Validator

try:
    from .harvest import deadline
    from .os_credentials import CredentialError, credential_status, load_os_key
except ImportError:
    from harvest import deadline
    from os_credentials import CredentialError, credential_status, load_os_key

ROOT = Path(__file__).resolve().parents[2]
CRS84 = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
CRS3D = "http://www.opengis.net/def/crs/EPSG/0/7405"
BASE = "https://api.os.uk/features/ngd/ofa/v1/collections/"
FEATURES_SOURCE = "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/features"
PROFILE = "okf-plus-private-os-ngd-retrieval.v1"


class RetrievalError(ValueError):
    """Only fixed, non-sensitive error codes leave this module."""


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def _json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise RetrievalError("duplicate-json-key")
            result[key] = value
        return result
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda _value: (_ for _ in ()).throw(ValueError()))
    except (ValueError, UnicodeError, RecursionError):
        raise RetrievalError("invalid-json") from None


def _private_directory(path):
    # All output is rooted in the repository's ignored artifacts/ tree. Reject
    # symlinks at every existing level before creating an owner-only directory.
    for parent in reversed((path, *path.parents)):
        if parent.is_symlink():
            raise RetrievalError("unsafe-private-path")
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path, 0o700)


def _write_private(path, raw):
    if path.is_symlink():
        raise RetrievalError("unsafe-private-path")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".pending-", delete=False) as stream:
            temporary = Path(stream.name)
            os.fchmod(stream.fileno(), 0o600)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _read_private(path, ceiling):
    if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o077:
        raise RetrievalError("unsafe-private-file")
    with path.open("rb") as stream:
        raw = stream.read(ceiling + 1)
    if len(raw) > ceiling:
        raise RetrievalError("private-file-ceiling")
    return raw


@contextmanager
def _lock(path):
    if path.is_symlink():
        raise RetrievalError("unsafe-private-path")
    descriptor = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(descriptor, "a+b") as stream:
        os.fchmod(stream.fileno(), 0o600)
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RetrievalError("retrieval-already-running") from None
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def _cql(text, queryables):
    """Admit a small scalar CQL-text vocabulary; the provider validates grammar.

    This supports comparisons, IN, LIKE, IS NULL and boolean grouping. Spatial
    predicates use the separately typed bbox. No implicit schema-to-queryable
    promotion or arbitrary functions are admitted.
    """
    pattern = re.compile(r"\s+|'(?:[^']|'')*'|-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|[A-Za-z_][A-Za-z_0-9]*|<=|>=|<>|[=<>(),]")
    keywords = {"AND", "OR", "NOT", "LIKE", "IN", "IS", "NULL", "TRUE", "FALSE"}
    position = 0
    properties = set()
    while position < len(text):
        token = pattern.match(text, position)
        if token is None:
            raise RetrievalError("unsupported-cql-token")
        value = token.group()
        if re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", value) and value.upper() not in keywords:
            if value not in queryables:
                raise RetrievalError("field-is-not-queryable")
            properties.add(value)
        position = token.end()
    if not properties:
        raise RetrievalError("cql-needs-queryable-field")


def prepare(request, root=ROOT):
    """Validate against retained metadata without network access or key reads."""
    schema = _json((Path(__file__).resolve().parents[2] / "okf-plus/schemas/os-retrieve-request.schema.json").read_bytes())
    if next(Draft202012Validator(schema).iter_errors(request), None) is not None:
        raise RetrievalError("invalid-retrieval-request")
    if request.get("wholeCollection") and any(key in request for key in ("bbox", "cql", "datetime")):
        raise RetrievalError("contradictory-collection-scope")
    catalogue = _json((root / "okf-plus/source/os-ngd-collections.json").read_bytes())
    rows = [row for row in catalogue["records"] if row.get("id") == request["collectionId"]]
    if len(rows) != 1:
        raise RetrievalError("collection-not-in-retained-catalogue")
    row = rows[0]
    source_schema = row["schemas"]["schema"]
    if (request["schemaId"] != source_schema.get("id") or
            request["schemaSha256"] != source_schema.get("sha256")):
        raise RetrievalError("collection-schema-pin-mismatch")
    returned_crs = request.get("returnCrs", row.get("storageCrs"))
    if returned_crs not in row.get("crs", []):
        raise RetrievalError("return-crs-not-advertised")
    if row.get("storageCrs") == CRS3D and returned_crs != CRS3D:
        raise RetrievalError("native-elevation-crs-required")
    params = {"limit": str(request.get("pageSize", 100)), "crs": returned_crs}
    if "bbox" in request:
        bounds = request["bbox"]
        if (not all(type(value) in (int, float) and math.isfinite(value) for value in bounds)
                or bounds[0] >= bounds[2] or bounds[1] >= bounds[3]):
            raise RetrievalError("invalid-bbox")
        bbox_crs = request.get("bboxCrs", CRS84)
        if bbox_crs == CRS84 and not (-180 <= bounds[0] < bounds[2] <= 180 and -90 <= bounds[1] < bounds[3] <= 90):
            raise RetrievalError("invalid-bbox")
        params.update({"bbox": ",".join(str(value) for value in bounds), "bbox-crs": bbox_crs})
    if "cql" in request:
        _cql(request["cql"], row["schemas"]["queryables"]["properties"])
        params.update({"filter": request["cql"], "filter-lang": "cql-text",
                       "filter-crs": request.get("filterCrs", CRS84)})
    if "datetime" in request:
        # Source-native temporal syntax is validated by OS, never interpolated
        # into a URL or promoted into arbitrary version-field predicates.
        if re.fullmatch(r"[0-9TZ:.+/\-]+", request["datetime"]) is None:
            raise RetrievalError("invalid-datetime")
        params["datetime"] = request["datetime"]
    bound = {"request": request, "query": params,
             "queryablesSha256": row["schemas"]["queryables"]["sha256"],
             "sourceSchemaConformance": "not-assessed",
             "nativeSchemaDefects": source_schema.get("requiredUndeclared", [])}
    return bound


def initial_url(bound):
    return BASE + bound["request"]["collectionId"] + "/items?" + urlencode(bound["query"])


def validate_url(url, bound, *, next_offset=None):
    """A next link can only change offset; missing scope is not reconstructed."""
    if not isinstance(url, str) or len(url) > 16384 or any(ord(char) < 33 for char in url):
        raise RetrievalError("unsafe-pagination-url")
    try:
        parsed = urlsplit(url)
        pairs = parse_qsl(parsed.query, keep_blank_values=True, strict_parsing=True)
        query = dict(pairs)
        if (parsed.scheme != "https" or parsed.netloc != "api.os.uk" or parsed.fragment
                or parsed.path != "/features/ngd/ofa/v1/collections/" + bound["request"]["collectionId"] + "/items"
                or len(pairs) != len(query) or set(query) - set(bound["query"]) - {"offset"}
                or any(query.get(key) != value for key, value in bound["query"].items())):
            raise RetrievalError("pagination-scope-mismatch")
        offset = query.pop("offset", "0")
        if re.fullmatch(r"0|[1-9][0-9]{0,17}", offset) is None:
            raise RetrievalError("invalid-pagination-offset")
        if next_offset is not None and int(offset) != next_offset:
            raise RetrievalError("pagination-offset-mismatch")
        return int(offset)
    except (ValueError, UnicodeError):
        raise RetrievalError("unsafe-pagination-url") from None


def inspect_page(raw, bound, offset):
    page = _json(raw)
    if (not isinstance(page, dict) or page.get("type") != "FeatureCollection"
            or not isinstance(page.get("features"), list) or not isinstance(page.get("links"), list)
            or len(page["features"]) > int(bound["query"]["limit"])):
        raise RetrievalError("invalid-feature-page")
    features = page["features"]
    if any(not isinstance(item, dict) or item.get("type") != "Feature" or not isinstance(item.get("id"), str) or not item["id"]
           or not isinstance(item.get("properties"), dict) or "geometry" not in item for item in features):
        raise RetrievalError("invalid-feature-wrapper")
    if "numberReturned" in page and (type(page["numberReturned"]) is not int or page["numberReturned"] != len(features)):
        raise RetrievalError("feature-count-mismatch")
    if any(not isinstance(link, dict) for link in page["links"]):
        raise RetrievalError("invalid-page-links")
    next_links = [link.get("href") for link in page["links"] if link.get("rel") == "next"]
    if len(next_links) > 1:
        raise RetrievalError("ambiguous-next-page")
    next_url = next_links[0] if next_links else None
    if next_links:
        if not features:
            raise RetrievalError("empty-page-with-continuation")
        validate_url(next_url, bound, next_offset=offset + len(features))
    return len(features), next_url


def _identities(raw):
    """Same source ID with different native versions remains a distinct record."""
    identities = []
    for feature in _json(raw)["features"]:
        properties = feature["properties"]
        identities.append(digest(canonical([feature["id"], properties.get("osid"),
                                           properties.get("versiondate"),
                                           properties.get("versionavailablefromdate"),
                                           properties.get("versionavailabletodate")])))
    if len(set(identities)) != len(identities):
        raise RetrievalError("duplicate-feature-version")
    return set(identities)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise HTTPError(req.full_url, code, "redirect-refused", headers, fp)


def _save(directory, state):
    raw = canonical(state)
    _write_private(directory / "checkpoint.json", canonical({"sha256": digest(raw), "state": state}) + b"\n")


def _load(directory, bound):
    identity = digest(canonical(bound))
    path = directory / "checkpoint.json"
    if not path.exists():
        return {"profile": PROFILE, "requestSha256": identity, "binding": bound,
                "pages": [], "nextUrl": initial_url(bound), "status": "ready", "attempts": 0}, set()
    wrapper = _json(_read_private(path, 16 * 1024 * 1024))
    state = wrapper.get("state") if isinstance(wrapper, dict) else None
    if (not isinstance(state, dict) or wrapper.get("sha256") != digest(canonical(state))
            or state.get("requestSha256") != identity or state.get("binding") != bound
            or state.get("profile") != PROFILE or not isinstance(state.get("pages"), list)
            or type(state.get("attempts")) is not int or state["attempts"] < len(state["pages"])):
        raise RetrievalError("checkpoint-integrity-failed")
    expected_url = initial_url(bound)
    seen = set()
    for index, receipt in enumerate(state["pages"]):
        if not isinstance(receipt, dict) or receipt.get("file") != f"page-{index:08d}.geojson" or expected_url is None:
            raise RetrievalError("checkpoint-page-chain-failed")
        if (type(receipt.get("retrievedAtUnix")) not in (int, float)
                or not math.isfinite(receipt["retrievedAtUnix"]) or receipt["retrievedAtUnix"] < 0):
            raise RetrievalError("checkpoint-page-time-failed")
        raw = _read_private(directory / receipt["file"], 64 * 1024 * 1024)
        if receipt.get("sha256") != digest(raw) or receipt.get("bytes") != len(raw) or receipt.get("requestSha256") != digest(expected_url.encode()):
            raise RetrievalError("checkpoint-page-integrity-failed")
        count, expected_url = inspect_page(raw, bound, validate_url(expected_url, bound))
        identities = _identities(raw)
        if seen & identities:
            raise RetrievalError("checkpoint-repeated-feature-version")
        seen.update(identities)
        if receipt.get("features") != count or receipt.get("contentCrs") != bound["query"]["crs"]:
            raise RetrievalError("checkpoint-page-evidence-failed")
    if state.get("nextUrl") != expected_url or (state.get("status") == "complete") != (expected_url is None):
        raise RetrievalError("checkpoint-continuation-failed")
    return state, seen


def summary(state, *, reused=False):
    """No locations, filters, URLs, raw errors, records or account data on stdout."""
    result = {"status": state["status"], "pages": len(state["pages"]),
              "features": sum(page["features"] for page in state["pages"]),
              "bytes": sum(page["bytes"] for page in state["pages"]),
              "completeWithinRequestedScope": state["status"] == "complete",
              "snapshotConsistency": "not-established", "sourceSchemaConformance": "not-assessed",
              "completedCaptureReused": reused,
              "capturedFromUnix": min((page["retrievedAtUnix"] for page in state["pages"]), default=None),
              "capturedToUnix": max((page["retrievedAtUnix"] for page in state["pages"]), default=None)}
    if "resumeAfter" in state:
        result["resumeAfter"] = state["resumeAfter"]
    return result


def retrieve(request, *, root=ROOT, key_env="OS_API_KEY", max_pages=100,
             max_bytes=64 * 1024 * 1024, page_bytes=16 * 1024 * 1024,
             timeout=30, interval=1.5, max_elapsed=300, reuse_complete=False, opener=None, limiter=None):
    """Fetch one bounded run. Repeating the same request resumes verified pages.

    The shared persistent limiter reserves attempts before egress. Rate waits and
    provider Retry-After stop this run with durable state; there is no hidden retry.
    """
    if (type(max_pages) is not int or not 1 <= max_pages <= 10000
            or type(max_bytes) is not int or not 1 <= max_bytes <= 1024 ** 4
            or type(page_bytes) is not int or not 1 <= page_bytes <= 64 * 1024 * 1024
            or type(timeout) not in (int, float) or not 0 < timeout <= 60
            or type(interval) not in (int, float) or not math.isfinite(interval) or interval < 1.5
            or type(max_elapsed) not in (int, float) or not 1 <= max_elapsed <= 86400
            or re.fullmatch(r"[A-Z_][A-Z_0-9]{0,99}", key_env) is None):
        raise RetrievalError("invalid-operational-control")
    bound = prepare(request, root)
    run_deadline = time.monotonic() + max_elapsed
    directory = root / "artifacts/okf-plus/os-retrieval" / digest(canonical(bound))
    _private_directory(directory)
    with _lock(directory / ".lock"):
        state, seen = _load(directory, bound)
        if state["status"] == "complete":
            if not reuse_complete:
                raise RetrievalError("completed-capture-requires-reuse-or-new-run-id")
            return summary(state, reused=True)
        try:
            key = load_os_key(key_env)
        except CredentialError as error:
            raise RetrievalError(error.code) from None
        if key.encode() in canonical(bound):
            raise RetrievalError("credential-in-retrieval-request")
        if limiter is None:
            limiter = _default_limiter(root)
        opener = opener or build_opener(NoRedirect())
        used_bytes = 0
        state.pop("resumeAfter", None)
        # A collection's major version does not pin its current minor schema.
        # Re-check the public schema once per run, before any licensed records.
        schema_url = BASE + request["collectionId"] + "/schema"
        schema_verified = False
        for _ in range(max_pages + 1):
            if time.monotonic() >= run_deadline:
                state["status"] = "run-time-ceiling"
                break
            remaining = min(page_bytes, max_bytes - used_bytes)
            if remaining <= 0:
                state["status"] = "run-byte-ceiling"
                break
            url = state["nextUrl"] if schema_verified else schema_url
            offset = validate_url(url, bound) if schema_verified else 0
            wait = _reserve(limiter, interval)
            if wait:
                state.update(status="rate-wait", resumeAfter=wait)
                break
            request_timeout = min(timeout, run_deadline - time.monotonic())
            if request_timeout <= 0:
                state["status"] = "run-time-ceiling"
                break
            state["attempts"] += 1
            state["status"] = "request-in-progress"
            _save(directory, state)
            headers = {"Accept": "application/geo+json" if schema_verified else "application/schema+json",
                       "Accept-Encoding": "identity"}
            if schema_verified:
                headers["key"] = key
            outgoing = Request(url, headers=headers)
            try:
                with deadline(request_timeout):
                    with opener.open(outgoing, timeout=request_timeout) as response:
                        if response.getcode() != 200 or response.geturl() != url:
                            raise RetrievalError("unexpected-provider-response")
                        if response.headers.get("Content-Encoding", "identity").lower() != "identity":
                            raise RetrievalError("unexpected-content-encoding")
                        content_crs = response.headers.get("Content-Crs", "").strip("<>")
                        if schema_verified and content_crs != bound["query"]["crs"]:
                            raise RetrievalError("response-crs-mismatch")
                        media_type = response.headers.get("Content-Type", "").split(";", 1)[0].lower()
                        if media_type not in ("application/geo+json", "application/json", "application/schema+json"):
                            raise RetrievalError("unexpected-content-type")
                        raw = response.read(remaining)
                        used_bytes += len(raw)
                        # At an exact ceiling EOF cannot be distinguished without
                        # consuming an extra byte; refuse instead of overrunning.
                        if len(raw) >= remaining:
                            raise RetrievalError("response-byte-ceiling")
                if key.encode() in raw or key.encode() in canonical(_json(raw)):
                    raise RetrievalError("credential-reflected-in-response")
                if not schema_verified:
                    if digest(raw) != request["schemaSha256"]:
                        raise RetrievalError("upstream-schema-changed")
                    state["schemaPreflight"] = {"sha256": digest(raw), "bytes": len(raw), "checkedAtUnix": time.time()}
                    schema_verified = True
                    _save(directory, state)
                    continue
                count, next_url = inspect_page(raw, bound, offset)
                identities = _identities(raw)
                if seen & identities:
                    raise RetrievalError("repeated-feature-version")
            except HTTPError as error:
                if error.code in (429, 503):
                    try:
                        state.update(status="provider-rate-wait", resumeAfter=_defer(limiter, error.headers.get("Retry-After")))
                    except RetrievalError:
                        state["status"] = "provider-rate-blocked"
                else:
                    state["status"] = "provider-http-error"
                error.close()
                break
            except RetrievalError as error:
                state["status"] = str(error)
                break
            except (URLError, OSError, TimeoutError):
                state["status"] = "provider-transport-error"
                break
            filename = f"page-{len(state['pages']):08d}.geojson"
            _write_private(directory / filename, raw)
            seen.update(identities)
            state["pages"].append({"file": filename, "sha256": digest(raw), "bytes": len(raw),
                                   "features": count, "contentCrs": content_crs,
                                   "requestSha256": digest(url.encode()), "retrievedAtUnix": time.time()})
            state["nextUrl"] = next_url
            state["status"] = "complete" if next_url is None else "run-page-ceiling"
            _save(directory, state)
            if next_url is None:
                return summary(state)
        _save(directory, state)
        return summary(state)


def _default_limiter(root):
    # Aggregate pacing with metadata capture; no credential/account identifier.
    try:
        from .os_rate_limit import SharedRateLimiter
    except ImportError:
        from os_rate_limit import SharedRateLimiter
    return SharedRateLimiter(root)


def _reserve(limiter, interval):
    try:
        result = limiter.reserve_attempt("ngd-features", interval)
        # Ordinary pacing can wait briefly. A durable Retry-After or another
        # consumer's longer reservation checkpoints and returns without busy retry.
        if not result["allowed"] and result["delay"] <= 2:
            time.sleep(result["delay"])
            result = limiter.reserve_attempt("ngd-features", interval)
        return None if result["allowed"] else result["notBefore"]
    except (ValueError, RuntimeError, KeyError, TypeError, OSError):
        raise RetrievalError("rate-checkpoint-unavailable") from None


def _defer(limiter, value):
    try:
        return limiter.defer_retry_after("ngd-features", value)
    except (ValueError, RuntimeError, KeyError, TypeError, OSError):
        raise RetrievalError("rate-checkpoint-unavailable") from None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    parser.add_argument("--fetch", action="store_true", help="Retrieve the explicitly requested dataset; default is offline planning only")
    parser.add_argument("--key-env", default="OS_API_KEY", help="Named key environment variable; default also falls back to the private ~/.secrets/os_api_key file")
    parser.add_argument("--max-pages", type=int, default=100)
    parser.add_argument("--max-bytes", type=int, default=64 * 1024 * 1024)
    parser.add_argument("--page-bytes", type=int, default=16 * 1024 * 1024)
    parser.add_argument("--max-seconds", type=float, default=300, help="Total per-run elapsed ceiling; interrupted runs can resume")
    parser.add_argument("--estimate-request", type=Path, help="Optional evidence-backed planner request with measurements and matching download candidates")
    parser.add_argument("--run-id", help="New capture identity; keep the same value when resuming")
    parser.add_argument("--reuse-complete", action="store_true", help="Explicitly reuse a verified completed capture; no freshness claim")
    args = parser.parse_args(argv)
    try:
        if args.request.stat().st_size > 16384:
            raise RetrievalError("request-byte-ceiling")
        request = _json(args.request.read_bytes())
        if args.run_id:
            request["runId"] = args.run_id
        bound = prepare(request)
        estimate = None
        if args.estimate_request:
            if args.estimate_request.stat().st_size > 256 * 1024:
                raise RetrievalError("estimate-request-byte-ceiling")
            estimate = _json(args.estimate_request.read_bytes())
        plan = _retrieval_plan(request, bound, estimate, args.max_pages, args.max_bytes, args.max_seconds, args.key_env)
        print(json.dumps(plan, sort_keys=True), flush=True)
        if args.fetch:
            if plan["executorTransactionsPerMinuteCeiling"] == 0:
                raise RetrievalError("no-unreserved-rate-capacity")
            result = retrieve(request, key_env=args.key_env, max_pages=args.max_pages,
                              max_bytes=args.max_bytes, page_bytes=args.page_bytes,
                              interval=60 / plan["executorTransactionsPerMinuteCeiling"],
                              max_elapsed=args.max_seconds, reuse_complete=args.reuse_complete)
            print(json.dumps(result, sort_keys=True))
            return 0 if result["status"] == "complete" else 2
        return 0
    except RetrievalError as error:
        print(json.dumps({"status": str(error)}))
        return 2
    except (OSError, ValueError, KeyError, TypeError):
        print(json.dumps({"status": "local-input-or-state-error"}))
        return 2


def _retrieval_plan(request, bound, estimate=None, max_pages=100, max_bytes=64 * 1024 * 1024, max_elapsed=300, key_env="OS_API_KEY"):
    try:
        from .retrieval_plan import plan_retrieval
    except ImportError:
        from retrieval_plan import plan_retrieval
    parameters = {key: value for key, value in bound["query"].items() if key != "limit"}
    if "bbox" in request:
        parameters["bbox"] = request["bbox"]
    selection = {"scope": "whole-collection" if request.get("wholeCollection") else "subset", "parameters": parameters}
    dataset = {"nativeIdentifier": request["collectionId"], "version": request["schemaId"],
               "sourceUrl": BASE + request["collectionId"] + "/schema", "schemaSha256": request["schemaSha256"]}
    if estimate is None:
        estimate = {"schema": "gis-ai-go.okf-plus-retrieval-request.v1", "dataset": dataset,
                    "selection": selection, "authority": {"basis": "owner-confirmed-PSGA", "reference": "urn:owner:2026-10-18"},
                    "project": {"mode": "unknown", "reservedTransactionsPerMinute": 0, "callerCeilingPerMinute": 40},
                    "initialWaitSeconds": {"lower": 0, "upper": 60, "basis": "execution-policy"},
                    "retryPolicy": {"maxRetriesPerRequest": 0, "maxWaitPerRetrySeconds": 0},
                    "executionBudget": {"maxRequests": max_pages + 1, "maxElapsedSeconds": max_elapsed, "maxBytes": max_bytes},
                    "api": {"service": "os-ngd-features", "pageSize": int(bound["query"]["limit"]), "availability": "unverified"}}
    elif (estimate.get("dataset") != dataset or estimate.get("selection") != selection
          or estimate.get("api", {}).get("service") != "os-ngd-features"
          or estimate.get("api", {}).get("pageSize") != int(bound["query"]["limit"])):
        raise RetrievalError("estimate-scope-mismatch")
    estimate = _json(canonical(estimate))
    estimate["project"]["callerCeilingPerMinute"] = min(40, estimate["project"].get("callerCeilingPerMinute", 40))
    # Measurements describe the workload, while CLI controls describe this run.
    # Bind displayed budgets and retries to the actual executor, never an
    # independently supplied hypothetical planner budget.
    estimate["executionBudget"] = {"maxRequests": max_pages + 1, "maxElapsedSeconds": max_elapsed, "maxBytes": max_bytes}
    estimate["retryPolicy"] = {"maxRetriesPerRequest": 0, "maxWaitPerRetrySeconds": 0}
    plan = plan_retrieval(estimate)
    known_ceiling = plan["ratePolicy"]["effectiveTransactionsPerMinute"]
    if known_ceiling is None:
        explicit_limits = [40, estimate["project"]["callerCeilingPerMinute"]]
        explicit_limits.extend(row["transactionsPerMinute"] for row in estimate["project"].get("additionalRateLimits", []))
        known_ceiling = max(0, min(explicit_limits) - estimate["project"]["reservedTransactionsPerMinute"])
    # Planner inputs are private and may contain addresses in filters. Display
    # only fixed messages, aggregate estimates and public policy references.
    route = next((candidate["kind"] for candidate in plan["candidates"]
                  if candidate["id"] == plan["recommendation"]["routeId"]), None)
    return {"status": "offline-plan", "credential": credential_status(key_env),
            "recommendation": {"kind": route,
                                                         "status": plan["recommendation"]["status"],
                                                         "reason": plan["recommendation"]["reason"]},
            "candidates": [{"kind": candidate["kind"], "estimate": candidate["estimate"],
                            "blockedReasons": candidate["blockedReasons"]} for candidate in plan["candidates"]],
            "downloadAlternative": "Check OS Data Hub download packages for equivalent collection, version, scope and currency before a large API extraction.",
            "rateSource": plan["ratePolicy"]["sourceUrl"],
            "executorTransactionsPerMinuteCeiling": known_ceiling,
            "executionBudget": estimate["executionBudget"], "retryPolicy": estimate["retryPolicy"],
            "executor": "NGD Features API only; bulk download transfer is not implemented by this command, even when a package is recommended.",
            "nativeCrsPreserved": bound["query"]["crs"], "paginationSource": FEATURES_SOURCE,
            "metadataPreflight": "Each run makes one additional public schema request within the same pacing and byte budget; its latency is excluded from the dataset estimate.",
            "externalTraffic": "The shared limiter covers this workspace only; reserve capacity for any other consumers of the same OS project.",
            "scopeSemantics": "Bounding boxes select intersecting whole features; no clipping or height derivation."}


if __name__ == "__main__":
    raise SystemExit(main())
