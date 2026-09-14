#!/usr/bin/env python3
"""Pure validation of captured ONS L522/MM23 monthly index data; no network."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import parse_qsl, urlsplit
from zoneinfo import ZoneInfo

if __package__:
    from . import web216_corpus as _corpus_module
    from .web216_corpus import canonical, digest
else:
    import web216_corpus as _corpus_module
    from web216_corpus import canonical, digest


ORIGIN = "https://api.beta.ons.gov.uk"
URI = "/economy/inflationandpriceindices/timeseries/l522/mm23"
TITLE = "CPIH INDEX 00: ALL ITEMS 2015=100"
UNIT = "Index, base year = 100"
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December")
MAX_BYTES = 1024 * 1024
MAX_MONTHS = 2000
ROW_FIELDS = {"date", "value", "label", "year", "month", "quarter", "sourceDataset", "updateDate"}
SOURCE_URLS = {
    "search": ORIGIN + "/v1/search?content_type=timeseries&cdids=L522",
    "data": ORIGIN + "/v1/data?uri=%2Feconomy%2Finflationandpriceindices%2Ftimeseries%2Fl522%2Fmm23",
    "public_page": "https://www.ons.gov.uk" + URI,
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any) -> dict:
    _require(isinstance(value, dict), "Expected a JSON object")
    return value


def _time(value: Any) -> datetime:
    _require(isinstance(value, str) and 1 <= len(value) <= 40, "Missing source timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    _require(parsed.tzinfo is not None, "Source timestamps must include a time zone")
    return parsed.astimezone(timezone.utc)


def _read(path: Path) -> tuple[Any, bytes]:
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    _require(len(raw) <= MAX_BYTES, "Captured file exceeds byte limit")

    def pairs(items):
        result = {}
        for key, value in items:
            _require(key not in result, "Duplicate JSON key")
            result[key] = value
        return result

    def invalid(_):
        raise ValueError("Non-finite JSON number")

    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=invalid)
    canonical(value)  # Reject numeric overflow as well as explicit NaN/Infinity.
    return value, raw


def validate_current_cpih(search: dict, data: dict, *, retrieved_at: str,
                          period: str = "latest") -> dict:
    """Validate supplied monthly rows; callers must establish their capture binding."""
    retrieved = _time(retrieved_at)
    search, data = _object(search), _object(data)
    items = search.get("items")
    _require(type(search.get("count")) is int and search["count"] == 1
             and isinstance(items, list) and len(items) == 1, "Search must return exactly one item")
    item = _object(items[0])
    _require(all(item.get(key) == value for key, value in {
        "cdid": "L522", "dataset_id": "MM23", "type": "timeseries", "uri": URI, "title": TITLE,
    }.items()), "Wrong searched series identity or title")
    _require(data.get("type") == "timeseries" and data.get("uri") == URI, "Wrong data identity")
    description = _object(data.get("description"))
    _require(all(description.get(key) == value for key, value in {
        "cdid": "L522", "datasetId": "MM23", "title": TITLE, "unit": UNIT,
    }.items()), "Wrong data series, title or index unit")
    release = description.get("releaseDate")
    _require(item.get("release_date") == release, "Search/data release mismatch: possible snapshot race")
    released = _time(release)
    _require(released <= retrieved, "Source release is after the recorded retrieval")
    released_london = released.astimezone(ZoneInfo("Europe/London"))
    next_release = description.get("nextRelease")
    _require(isinstance(next_release, str) and 0 < len(next_release) <= 80, "Missing next-release metadata")
    months = data.get("months")
    _require(isinstance(months, list) and 0 < len(months) <= MAX_MONTHS, "Missing or excessive monthly rows")
    by_period = {}
    for row in months:
        row = _object(row)
        _require(set(row) == ROW_FIELDS, "Unknown or missing monthly fields, including suppression metadata")
        _require(row["sourceDataset"] == "MM23" and row["quarter"] == "", "Wrong monthly source or time grain")
        source_date = row["date"]
        _require(isinstance(source_date, str) and re.fullmatch(r"[0-9]{4} [A-Z]{3}", source_date) is not None,
                 "Invalid source month date")
        year, abbreviation = source_date.split(" ")
        matches = [number for number, name in enumerate(MONTHS, 1) if name[:3].upper() == abbreviation]
        _require(len(matches) == 1, "Unknown month abbreviation")
        month = matches[0]
        _require(row["label"] == source_date and row["year"] == year and row["month"] == MONTHS[month - 1],
                 "Inconsistent monthly date/label/year/month")
        key = f"{year}-{month:02d}"
        _require(key not in by_period, "Duplicate monthly period")
        _require(datetime(int(year), month, 1, tzinfo=timezone.utc) <= retrieved, "Future period after retrieval")
        _require((int(year), month) <= (released_london.year, released_london.month),
                 "Monthly period is after the source release month in London")
        updated = _time(row["updateDate"])
        _require(updated <= retrieved, "Monthly update is after retrieval")
        _require(updated <= released, "Monthly update is after the source release")
        value = row["value"]
        _require(isinstance(value, str) and re.fullmatch(r"(?:0|[1-9][0-9]{0,14})(?:\.[0-9]{1,10})?", value) is not None,
                 "Unknown, blank, suppressed or non-decimal-string monthly value")
        by_period[key] = row
    ordered = sorted(by_period)
    latest = by_period[ordered[-1]]
    _require("date" in description and "number" in description, "Missing required headline observation")
    _require(description["date"] == latest["date"] and description["number"] == latest["value"],
             "Headline observation disagrees with the latest monthly row")
    _require(period == "latest" or (isinstance(period, str) and re.fullmatch(r"[0-9]{4}-(?:0[1-9]|1[0-2])", period) is not None),
             "Period must be latest or YYYY-MM")
    selected_period = ordered[-1] if period == "latest" else period
    _require(selected_period in by_period, "Requested period is not present; no substitution is permitted")
    return {
        "schema_version": "web216.validated-current-cpih.v1", "cdid": "L522", "dataset_id": "MM23",
        "uri": URI, "title": TITLE, "unit": UNIT, "measure_kind": "index-not-percentage",
        "base_year": 2015, "base_year_basis": "Exact series title, not the generic unit string",
        "requested_period": period, "selected_period": selected_period, "observation": by_period[selected_period],
        "retrieved_at": retrieved_at, "currency": "As of this recorded retrieval, not a permanent current claim",
        "release_date": release, "release_date_london": released_london.date().isoformat(),
        "next_release": next_release, "next_release_validation": "unvalidated-provider-text",
        "validated_month_count": len(months),
        "validated_period_range": {"first": ordered[0], "last": ordered[-1]}, "retained_observation_count": 1,
        "source_urls": SOURCE_URLS, "selection_authorised": False, "mcp_executed": False,
        "production_transport": False,
    }


def validate_capture(directory: Path, period: str = "latest") -> dict:
    directory = Path(directory)
    manifest, raw_manifest = _read(directory / "run-manifest.json")
    manifest = _object(manifest)
    _require(manifest.get("outcome") == "raw-responses-collected-pending-schema-validation"
             and manifest.get("mcp_executed") is False and manifest.get("production_transport") is False,
             "Unexpected source-time manifest outcome or authority boundary")
    attempts = manifest.get("attempts")
    _require(isinstance(attempts, list) and len(attempts) == 2, "Expected exactly two source-time attempts")
    captured = _time(manifest.get("completed_at"))
    previous = _time(manifest.get("started_at"))
    bodies, hashes = {}, {}
    for stage, attempt in zip(("search", "data"), attempts, strict=True):
        attempt = _object(attempt)
        _require(attempt.get("stage") == stage and type(attempt.get("status")) is int
                 and attempt["status"] == 200 and attempt.get("body_complete") is True,
                 "Expected two complete HTTP 200 responses")
        actual, expected = urlsplit(attempt.get("url", "")), urlsplit(SOURCE_URLS[stage])
        query = parse_qsl(actual.query, keep_blank_values=True)
        _require((actual.scheme, actual.netloc, actual.path, actual.fragment) ==
                 (expected.scheme, expected.netloc, expected.path, "")
                 and len(query) == len(set(key for key, _ in query))
                 and sorted(query) == sorted(parse_qsl(expected.query)), "Unexpected captured request URL")
        started, completed = _time(attempt.get("started_at")), _time(attempt.get("completed_at"))
        _require(previous <= started <= completed <= captured, "Inconsistent serial source-time bounds")
        previous = completed
        bodies[stage], raw = _read(directory / f"{stage}.body.json")
        hashes[stage] = hashlib.sha256(raw).hexdigest()
        _require(attempt.get("body_sha256") == hashes[stage]
                 and type(attempt.get("bytes_retained")) is int and attempt["bytes_retained"] == len(raw),
                 "Captured body hash or byte count differs from source-time manifest")
        _require(str(attempt.get("content_type", "")).split(";", 1)[0].lower() == "application/json",
                 "Captured response is not JSON")
    result = validate_current_cpih(bodies["search"], bodies["data"],
                                   retrieved_at=manifest["completed_at"], period=period)
    validator_sources = {
        "scripts/web216_current_cpih.py": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scripts/web216_corpus.py": hashlib.sha256(Path(_corpus_module.__file__).read_bytes()).hexdigest(),
    }
    result.update({"input_scope": "full-captured-response", "original_body_sha256": hashes,
                   "capture_manifest_sha256": hashlib.sha256(raw_manifest).hexdigest(),
                   "validator_sha256": validator_sources["scripts/web216_current_cpih.py"],
                   "validator_source_sha256": validator_sources})
    return {**result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture-directory", type=Path, required=True)
    parser.add_argument("--period", default="latest")
    parser.add_argument("--output", type=Path, required=True, help="Fresh result file; never overwritten")
    args = parser.parse_args()
    try:
        result = validate_capture(args.capture_directory, args.period)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as stream:
            stream.write(canonical(result) + b"\n")
    except (OSError, ValueError, TypeError) as error:
        parser.exit(1, f"CPIH validation failed: {error}\n")
    print(f"Validated {result['validated_month_count']} monthly rows; selected {result['selected_period']}; "
          "index, not percentage; no MCP execution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
