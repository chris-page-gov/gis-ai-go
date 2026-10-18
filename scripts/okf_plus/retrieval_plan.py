#!/usr/bin/env python3
"""Offline, source-backed OS retrieval estimates and private request manifests.

Owner: GIS AI GO OKF+ metadata tooling. This module never reads credentials,
opens a provider connection or interprets a plan as proof of access. Estimates
model one sequential worker and require measurements of the requested workload.
The closed input contract excludes headers, credentials and arbitrary endpoints.
Run with the repository's pinned development environment (jsonschema required).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
REQUEST_SCHEMA = ROOT / "okf-plus/schemas/retrieval-request.schema.json"
MAX_REQUEST_BYTES = 256 * 1024
RATE_SOURCE = "https://docs.os.uk/os-apis/core-concepts/rate-limiting-policy"
PAGE_SOURCES = {
    "os-ngd-features": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/features",
    "os-features": "https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/technical-specification/paging",
}
DOWNLOAD_SOURCE = "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/data-package-version-id"
POLICY_REVIEWED = "2026-10-18"


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode()


def _safe_reference(value):
    # Reference text is never printed in a validation error. Signed download
    # redirects are credentials too: retain the clean catalogue download URL.
    if value.startswith("urn:"):
        if not re.fullmatch(r"urn:[A-Za-z0-9:._-]+", value):
            raise ValueError("Invalid evidence reference")
        return
    try:
        parts = urlsplit(value)
        crs_identifier = (parts.scheme == "http" and parts.hostname == "www.opengis.net"
                          and parts.path.startswith("/def/crs/") and not parts.query and not parts.fragment)
        if ((parts.scheme != "https" and not crs_identifier) or not parts.hostname or parts.username
                or parts.password or parts.port not in (None, 443)
                or any(ord(c) <= 32 or ord(c) == 127 for c in value)):
            raise ValueError
        credential_fields = parts.query + ("&" + parts.fragment if "=" in parts.fragment else "")
        for key, _ in parse_qsl(credential_fields, keep_blank_values=True):
            decoded = key
            for _ in range(16):
                changed = unquote(decoded)
                if changed == decoded:
                    break
                decoded = changed
            else:
                raise ValueError
            normal = re.sub(r"[^a-z0-9]", "", decoded.casefold())
            if (normal in {"key", "apikey", "token", "accesstoken", "password",
                           "authorization", "clientsecret", "signature", "sig",
                           "secret", "credential", "sas"}
                    or normal.startswith(("xamz", "xgoog"))):
                raise ValueError
    except (ValueError, UnicodeError):
        raise ValueError("Credential-bearing or invalid reference URL") from None


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate request key")
        result[key] = value
    return result


def validate_request(request):
    """Validate shape, ranges and credential-free references without echoing input."""
    try:
        encoded = canonical(request)
    except (ValueError, TypeError, RecursionError):
        raise ValueError("Request must be finite JSON") from None
    if len(encoded) > MAX_REQUEST_BYTES:
        raise ValueError("Request byte limit exceeded")
    schema = json.loads(REQUEST_SCHEMA.read_text(encoding="utf-8"))
    if next(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(request), None):
        raise ValueError("Request does not conform to retrieval-request.schema.json")

    def visit(value):
        if isinstance(value, dict):
            if "lower" in value and "upper" in value and value["upper"] is not None:
                if value["lower"] > value["upper"]:
                    raise ValueError("Reversed range")
            for key, item in value.items():
                if key in {"url", "reference", "sourceUrl", "bbox-crs", "crs", "filter-crs"}:
                    _safe_reference(item)
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)
    visit(request)
    parameters = request["selection"]["parameters"]
    if request["selection"]["scope"] == "subset" and not any(
            name in parameters for name in ("bbox", "filter", "datetime", "resourceId")):
        raise ValueError("A subset requires an explicit selection")
    if request["selection"]["scope"] == "whole-collection" and any(
            name in parameters for name in ("bbox", "filter", "datetime", "resourceId")):
        raise ValueError("A whole-collection request cannot contain a selection filter")
    if "bbox" in parameters:
        box = parameters["bbox"]
        if box[0] > box[2] or box[1] > box[3]:
            raise ValueError("Bounding box minima exceed maxima; split antimeridian selections")
    api = request.get("api")
    if api and api["service"] == "os-ngd-features":
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*-[1-9][0-9]*", request["dataset"]["nativeIdentifier"]):
            raise ValueError("NGD requires the source-native versioned collection identifier")
        if "resourceId" in parameters:
            raise ValueError("NGD item listing does not accept the WFS resourceId parameter")
    ids = [item["id"] for item in request.get("downloads", [])]
    if len(ids) != len(set(ids)):
        raise ValueError("Download candidate identifiers must be unique")
    for item in request.get("downloads", []):
        if item["id"] == "api":
            raise ValueError("Download identifiers cannot collide with the API route")
        urls = [file["url"] for file in item["files"]]
        if len(urls) != len(set(urls)):
            raise ValueError("Download files must be unique within each candidate")
        for url in urls:
            parts = urlsplit(url)
            if parts.hostname != "api.os.uk" or not parts.path.startswith("/downloads/v1/"):
                raise ValueError("Use an OS Downloads catalogue URL, not a signed redirect")
    return json.loads(encoded)


def _rate(project):
    mode = project["mode"]
    documented = {"live": 600, "development": 50}.get(mode)
    limits = [{"scope": "api-and-project", "transactionsPerMinute": documented,
               "sourceUrl": RATE_SOURCE}] if documented is not None else []
    limits += project.get("additionalRateLimits", [])
    ceilings = [row["transactionsPerMinute"] for row in limits]
    if project.get("callerCeilingPerMinute") is not None:
        ceilings.append(project["callerCeilingPerMinute"])
    # An arbitrary caller ceiling cannot establish the provider's project mode.
    available = (max(0, min(ceilings) - project["reservedTransactionsPerMinute"])
                 if documented is not None else None)
    return {"projectMode": mode, "documentedTransactionsPerMinute": documented,
            "effectiveTransactionsPerMinute": available,
            "reservedTransactionsPerMinute": project["reservedTransactionsPerMinute"],
            "constraints": limits,
            "callerCeilingPerMinute": project.get("callerCeilingPerMinute"),
            "scheduling": "sequential; evenly spaced starts; coordinate all workers sharing the limiting scope",
            "policyReviewedOn": POLICY_REVIEWED,
            "sourceUrl": RATE_SOURCE}


def _component(lower=None, upper=None, *, unit="seconds", reason=None):
    result = {"lower": lower, "upper": upper, "unit": unit}
    if reason:
        result["unknownReason"] = reason
    return result


def _pages(count, size):
    # A known empty selection requires no feature requests. This assumes a
    # trustworthy prior count, not that an unqueried selection is empty.
    return math.ceil(count / size) if count is not None else None


def _estimate(request, requests, processing, *, download_bytes=None):
    measurements = request.get("measurements", {})
    rate = _rate(request["project"])["effectiveTransactionsPerMinute"]
    retry = request["retryPolicy"]
    lower_calls, upper_calls = requests["lower"], requests["upper"]
    attempts = None if upper_calls is None else upper_calls * (1 + retry["maxRetriesPerRequest"])
    wait = request["initialWaitSeconds"]
    if upper_calls == 0:
        return {"status": "estimated", "seconds": _component(0, 0),
                "requestAttempts": _component(0, 0, unit="requests"),
                "components": {}, "unknowns": [], "conditional": True}
    unknowns = []
    latency_name = "downloadRequestSeconds" if download_bytes is not None else "apiRequestSeconds"
    latency = measurements.get(latency_name)
    if latency is None:
        unknowns.append(latency_name)
    if rate is None:
        unknowns.append("projectMode")
    elif rate == 0:
        unknowns.append("unreservedRateCapacity")
    if upper_calls is None:
        unknowns.append("recordCountUpper")
    interval = 60 / rate if rate else None

    def wire(calls, edge):
        if calls == 0:
            return 0
        if calls is None or latency is None or interval is None:
            return None
        # Latency already includes API response transfer. Spacing and latency
        # overlap; do not add both once for each request and double-count them.
        return (calls - 1) * max(interval, latency[edge]) + latency[edge]

    wire_range = _component(wire(lower_calls, "lower"), wire(attempts, "upper"))
    # This is only a scheduling floor; it is not an end-to-end estimate.
    rate_floor = _component(max(0, lower_calls - 1) * interval if interval else None,
                            max(0, upper_calls - 1) * interval if interval and upper_calls is not None else None)
    retry_wait = 0 if attempts is None else (attempts - upper_calls) * retry["maxWaitPerRetrySeconds"]
    parts = {"requestAndSpacing": wire_range, "rateSchedulingFloor": rate_floor,
             "initialWait": _component(wait["lower"], wait["upper"]),
             "retryWait": _component(0, retry_wait if attempts is not None else None),
             "processing": processing}
    if processing["lower"] is None or processing["upper"] is None:
        unknowns.append(processing.get("unknownReason", "processingMeasurement"))
    if download_bytes is not None:
        throughput = measurements.get("downloadBytesPerSecond")
        if download_bytes == 0:
            transfer = _component(0, 0)
        elif throughput is None or download_bytes is None or download_bytes < 0:
            transfer = _component(reason="downloadSizeOrThroughput")
            unknowns.append("downloadSizeOrThroughput")
        else:
            transfer = _component(download_bytes / throughput["upper"],
                                  download_bytes * (1 + retry["maxRetriesPerRequest"]) / throughput["lower"])
        parts["transfer"] = transfer
    if unknowns:
        total = _component(reason="; ".join(sorted(set(unknowns))))
    else:
        summed = [v for k, v in parts.items() if k != "rateSchedulingFloor"]
        total = _component(round(sum(v["lower"] for v in summed), 6),
                           round(sum(v["upper"] for v in summed), 6))
    return {"status": "unknown" if unknowns else "estimated", "seconds": total,
            "requestAttempts": _component(lower_calls, attempts, unit="requests"),
            "components": parts, "unknowns": sorted(set(unknowns)), "conditional": True}


def _processing(counts, measurement, reason):
    if counts["upper"] == 0:
        return _component(0, 0)
    if not measurement:
        return _component(reason=reason)
    return _component(counts["lower"] / measurement["upper"],
                      counts["upper"] / measurement["lower"] if counts["upper"] is not None else None,
                      reason="recordCountUpper" if counts["upper"] is None else None)


def _budget_status(estimate, budget, bytes_required=None):
    reasons, unknown = [], []
    checks = (("requestAttempts", estimate["requestAttempts"]["upper"], budget["maxRequests"]),
              ("elapsedSeconds", estimate["seconds"]["upper"], budget["maxElapsedSeconds"]),
              ("bytes", bytes_required, budget["maxBytes"]))
    for name, required, ceiling in checks:
        if required is None:
            unknown.append(name)
        elif required > ceiling:
            reasons.append(name)
    return {"status": "exceeds" if reasons else "unknown" if unknown else "within",
            "exceeded": reasons, "unknown": unknown}


def plan_retrieval(request):
    """Return a deterministic plan. Neither estimated time nor rights prove execution."""
    request = validate_request(request)
    count = request.get("recordCount", {"lower": 0, "upper": None, "basis": "unknown"})
    measurements = request.get("measurements", {})
    rate = _rate(request["project"])
    candidates = []
    api = request.get("api")
    if api:
        pages = _component(_pages(count["lower"], api["pageSize"]),
                           _pages(count["upper"], api["pageSize"]), unit="requests")
        estimate = _estimate(request, pages, _processing(count, measurements.get("apiRecordsProcessedPerSecond"),
                                                        "apiRecordsProcessedPerSecond"))
        block = []
        if api["availability"] != "verified":
            block.append("API availability is not verified for this project and collection")
        if rate["effectiveTransactionsPerMinute"] in (0, None):
            block.append("Project rate capacity is not established")
        identifier = request["dataset"]["nativeIdentifier"]
        endpoint = ("https://api.os.uk/features/ngd/ofa/v1/collections/" + identifier + "/items"
                    if api["service"] == "os-ngd-features" else "https://api.os.uk/features/v1/wfs")
        candidates.append({"id": "api", "kind": "api", "service": api["service"],
                           "endpoint": endpoint, "pageSize": api["pageSize"],
                           "documentedMaximumPageSize": 100, "pageLimitSource": PAGE_SOURCES[api["service"]],
                           "availability": api["availability"], "availabilityEvidence": api.get("evidence"),
                           "estimate": estimate, "blockedReasons": block,
                           "budget": _budget_status(estimate, request["executionBudget"], 0 if count["upper"] == 0 else None)})
    for download in request.get("downloads", []):
        files = download["files"]
        size = sum(file["size"] for file in files) if all("size" in file for file in files) else None
        byte_count = {"lower": size or 0, "upper": size}
        transfer_ceiling = size * (1 + request["retryPolicy"]["maxRetriesPerRequest"]) if size is not None else None
        processing = _processing(byte_count, measurements.get("downloadBytesProcessedPerSecond"),
                                 "downloadSizeOrProcessingMeasurement")
        # The advertised OS URL redirects to the file: account for both wire
        # requests. Applying the OS spacing to both is deliberately conservative.
        calls = _component(2 * len(files), 2 * len(files), unit="requests")
        estimate = _estimate(request, calls, processing, download_bytes=size if size is not None else -1)
        block = []
        if download["availability"] != "verified":
            block.append("Download availability is not verified for this project")
        if download["selectionMatch"] not in {"exact", "superset"}:
            block.append("Download does not establish complete coverage of the requested selection")
        if download["versionMatch"] != "verified":
            block.append("Download does not establish the requested data/schema version")
        if download["supplyType"] != "FULL":
            block.append("Change-only supply cannot replace a full dataset without a verified base")
        if rate["effectiveTransactionsPerMinute"] in (0, None):
            block.append("Project rate capacity is not established")
        candidates.append({**download, "kind": "download", "totalBytes": size,
                           "estimatedFileTransferBytes": _component(size, transfer_ceiling, unit="bytes"),
                           "estimate": estimate, "blockedReasons": block,
                           "budget": _budget_status(estimate, request["executionBudget"], transfer_ceiling),
                           "requestCountAssumption": "one OS catalogue redirect and one file request per file; additional redirects require a new plan",
                           "metadataContractSource": DOWNLOAD_SOURCE})

    eligible = [row for row in candidates if not row["blockedReasons"] and row["budget"]["status"] != "exceeds"]
    recommendation = {"routeId": None, "reason": "No verified complete route fits the known execution budgets",
                      "status": "unresolved"}
    if count["upper"] == 0:
        recommendation = {"routeId": None, "status": "no-data", "reason": "The supplied count is zero; conditional on that count, no geographic records need retrieval"}
    elif len(eligible) == 1:
        recommendation = {"routeId": eligible[0]["id"], "status": "provisional",
                          "reason": "Only one verified complete route is supplied; missing estimates remain unknown"}
    elif eligible:
        # A faster midpoint is not a proof of a faster route. Only separated
        # estimate intervals justify the definite timing recommendation.
        faster = [row for row in eligible if row["estimate"]["status"] == "estimated" and all(
            other is row or (other["estimate"]["status"] == "estimated" and
                             row["estimate"]["seconds"]["upper"] < other["estimate"]["seconds"]["lower"])
            for other in eligible)]
        if faster:
            recommendation = {"routeId": faster[0]["id"], "status": "estimated-faster",
                              "reason": "Its estimated upper duration is below every other eligible route's lower duration"}
        else:
            recommendation["reason"] = "Estimate ranges overlap or measurements are missing; efficiency is unresolved"
    digest = hashlib.sha256(canonical(request)).hexdigest()
    return {"schema": "gis-ai-go.okf-plus-retrieval-plan.v1", "planId": "sha256:" + digest,
            "status": "planning-only", "providerRequestsMade": 0, "owner": "GIS AI GO OKF+ metadata tooling",
            "dataset": request["dataset"], "selection": request["selection"], "recordCount": count,
            "authority": request["authority"], "ratePolicy": rate, "candidates": candidates,
            "recommendation": recommendation, "measurements": measurements,
            "manifest": {"trigger": "geographic-data-request", "acquisitionMode": "on-demand",
                         "requestSha256": digest, "executionBudget": request["executionBudget"],
                         "retryPolicy": request["retryPolicy"], "initialWaitSeconds": request["initialWaitSeconds"],
                         "credentialDelivery": "executor-only; never in request, plan, URLs or receipt",
                         "outputPolicy": "private geographic payloads; metadata-only public evidence",
                         "preflight": ["Confirm current project/API access, collection/schema version and policy sources",
                                       "Coordinate rate budget with other consumers of this project/API/account",
                                       "Verify selection fields against queryables and bind the source-native CRS",
                                       "Resolve download metadata, supply type, version and coverage before transfer",
                                       "Count discovery/redirect/retry requests inside a separate explicit execution budget"],
                         "stopConditions": ["request, byte or wall-clock budget reached", "401 or 403; do not retry",
                                            "429 Retry-After exceeds the remaining wait/deadline budget",
                                            "retry allowance exhausted", "repeated page, duplicate cursor or changed version",
                                            "redirect destination has not been independently admitted"],
                         "checkpointFields": ["planId", "sourceVersion", "selectionSha256", "pageCursorWithoutCredentials",
                                              "receivedRecordIdsDigest", "requestsAttempted", "bytesReceived", "elapsedSeconds",
                                              "lastCommittedOutputDigest", "nextAllowedRequestAt"],
                         "receiptFields": ["planId", "startedAt", "endedAt", "sourceNativeIdentifier", "sourceVersion",
                                           "redactedRequestIdentity", "httpStatuses", "requestCountIncludingRetries",
                                           "responseBytes", "responseDigests", "outputDigests", "receivedUniqueRecords",
                                           "completeness", "rateWaitSeconds", "actualProcessingSeconds", "failures"]},
            "assumptions": ["All durations are conditional estimates, not completion guarantees",
                            "One sequential worker; measurements must match query complexity, format, network and processing",
                            "Retrieval and processing are modelled as separate serial phases; pipelining can reduce elapsed time",
                            "API latency includes response transfer; download request latency excludes file transfer",
                            "Download processing includes decompression and any filtering/joining of a superset",
                            "Download byte estimates include bounded retransfer of files but exclude unmeasured error-response bodies",
                            "Counts describe the requested selection and remain stable during paging",
                            "Request estimates exclude metadata preflight; the executor must budget and receipt it separately",
                            "The bounded retry maximum estimates attempted effort; a longer Retry-After requires checkpoint and stop",
                            "PSGA authority does not prove that an API is enabled or a matching package has been created"],
            "limitations": ["Supports NGD Features, WFS Features and supplied OS Downloads metadata; other API planners are not implemented",
                            "No live request, data processing, access verification or complete-catalogue claim",
                            "API response byte requirements remain unknown without a measured size model",
                            "Metadata and plans are untrusted evidence, not executable instructions"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="Private JSON plan destination; stdout if omitted")
    args = parser.parse_args()
    try:
        with args.request.open("rb") as stream:
            raw = stream.read(MAX_REQUEST_BYTES + 1)
        if len(raw) > MAX_REQUEST_BYTES:
            raise ValueError("Request byte limit exceeded")
        request = json.loads(raw, object_pairs_hook=_reject_duplicate_keys,
                             parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Non-finite request number")))
        payload = canonical(plan_retrieval(request))
        if args.output:
            if args.output.is_symlink():
                raise ValueError("Output must not be a symbolic link")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(dir=args.output.parent, prefix=".retrieval-plan-", delete=False) as stream:
                    temporary = Path(stream.name)
                    stream.write(payload)
                    stream.flush()
                    os.fsync(stream.fileno())
                temporary.replace(args.output)
            finally:
                if temporary:
                    temporary.unlink(missing_ok=True)
        else:
            sys.stdout.buffer.write(payload)
    except (ValueError, OSError, RecursionError):
        # A parser/OS exception can contain caller input or a sensitive path.
        print("Retrieval plan rejected: invalid request or inaccessible file; input values omitted", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
