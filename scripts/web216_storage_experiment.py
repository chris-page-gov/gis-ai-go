#!/usr/bin/env python3
"""Local X05 storage comparison; no D1, Parquet, network, model or provider calls."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sqlite3
import statistics
import subprocess
import time
from typing import Any

if __package__:
    from .web216_corpus import MAX_CORPUS_BYTES, canonical, digest, identity, load_corpus
    from .web216_experiments import build, rank
else:
    from web216_corpus import MAX_CORPUS_BYTES, canonical, digest, identity, load_corpus
    from web216_experiments import build, rank


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests/fixtures/web216/development-cases.json"
CODE_FILES = ("web216_storage_experiment.py", "web216_experiments.py", "web216_corpus.py")
METADATA_FIELDS = {"sourceId", "sourceRecordId", "title"}
JOIN = "SELECT m.source_id, m.native_id, m.title, d.body_json FROM metadata m JOIN details d ON d.id=m.id"


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _write(path: Path, value: Any) -> None:
    with path.open("xb") as stream:
        stream.write(canonical(value))


def _corpus_bytes(path: Path) -> bytes:
    with path.open("rb") as stream:
        raw = stream.read(MAX_CORPUS_BYTES + 1)
    if len(raw) > MAX_CORPUS_BYTES:
        raise ValueError("Corpus exceeds the byte limit")
    return raw


def _code_hashes() -> dict[str, str]:
    return {f"scripts/{name}": hashlib.sha256((ROOT / "scripts" / name).read_bytes()).hexdigest()
            for name in CODE_FILES}


def _key(value: str) -> None:
    if not isinstance(value, str) or not 0 < len(value) <= 256:
        raise ValueError("Identifier must contain between 1 and 256 characters")


def _prefix(identifier: str) -> str:
    return hashlib.sha256(identifier.encode("utf-8")).hexdigest()[:1]


def write_layouts(records: list[dict], output: Path) -> None:
    """Only generated artefacts in a caller-created fresh experiment directory."""
    for name in ("static", "sqlite", "partitions"):
        (output / name).mkdir()
    _write(output / "static/records.json", records)
    with sqlite3.connect(output / "sqlite/records.sqlite") as connection:
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA page_size=4096")
        connection.execute("PRAGMA journal_mode=DELETE")
        connection.execute("CREATE TABLE metadata (id TEXT PRIMARY KEY, source_id TEXT NOT NULL, "
                           "native_id TEXT NOT NULL, title TEXT NOT NULL) WITHOUT ROWID")
        connection.execute("CREATE TABLE details (id TEXT PRIMARY KEY REFERENCES metadata(id), "
                           "body_json BLOB NOT NULL) WITHOUT ROWID")
        for record in records:
            key = identity(record)
            connection.execute("INSERT INTO metadata VALUES (?,?,?,?)",
                               (key, record["sourceId"], record["sourceRecordId"], record["title"]))
            rest = {field: value for field, value in record.items() if field not in METADATA_FIELDS}
            connection.execute("INSERT INTO details VALUES (?,?)", (key, canonical(rest)))
    # The context manager commits but does not close the connection itself.
    connection.close()
    partitions: dict[str, dict] = {}
    for record in records:
        key = identity(record)
        partitions.setdefault(_prefix(key), {})[key] = record
    manifest = {}
    for prefix, rows in sorted(partitions.items()):
        _write(output / "partitions" / f"{prefix}.json", rows)
        manifest[prefix] = {"records": len(rows), "sha256": hashlib.sha256(canonical(rows)).hexdigest()}
    _write(output / "partitions/manifest.json", {"version": "web216.digest-partitions.v1", "partitions": manifest})


class StaticReader:
    def __init__(self, path: Path):
        raw = (path / "records.json").read_bytes()
        self.records = {identity(record): record for record in json.loads(raw)}
        self.initial_bytes = self.bytes_read = len(raw)

    def lookup(self, key: str) -> dict | None:
        _key(key)
        return self.records.get(key)

    def all_records(self) -> list[dict]:
        return [self.records[key] for key in sorted(self.records)]

    def close(self) -> None:
        pass


class SqliteReader:
    def __init__(self, path: Path):
        self.connection = sqlite3.connect((path / "records.sqlite").resolve().as_uri() + "?mode=ro", uri=True)
        self.connection.execute("PRAGMA query_only=ON")
        self.initial_bytes = self.bytes_read = None  # sqlite3 does not expose physical page I/O here.

    @staticmethod
    def _record(row: tuple | None) -> dict | None:
        if row is None:
            return None
        source, native, title, details = row
        return {**json.loads(details), "sourceId": source, "sourceRecordId": native, "title": title}

    def lookup(self, key: str) -> dict | None:
        _key(key)
        return self._record(self.connection.execute(JOIN + " WHERE m.id=?", (key,)).fetchone())

    def all_records(self) -> list[dict]:
        return [self._record(row) for row in self.connection.execute(JOIN + " ORDER BY m.id")]

    def close(self) -> None:
        self.connection.close()


class PartitionReader:
    def __init__(self, path: Path):
        self.path, self.cache = path, {}
        raw = (path / "manifest.json").read_bytes()
        self.manifest = json.loads(raw)["partitions"]
        self.initial_bytes = self.bytes_read = len(raw)

    def _partition(self, prefix: str) -> dict:
        if prefix not in self.manifest:
            return {}
        if prefix not in self.cache:
            raw = (self.path / f"{prefix}.json").read_bytes()
            self.bytes_read += len(raw)
            if hashlib.sha256(raw).hexdigest() != self.manifest[prefix]["sha256"]:
                raise ValueError("Generated partition hash mismatch")
            self.cache[prefix] = json.loads(raw)
        return self.cache[prefix]

    def lookup(self, key: str) -> dict | None:
        _key(key)
        return self._partition(_prefix(key)).get(key)

    def all_records(self) -> list[dict]:
        records = [record for prefix in sorted(self.manifest) for record in self._partition(prefix).values()]
        return sorted(records, key=identity)

    def close(self) -> None:
        self.cache.clear()


READERS = {"static": StaticReader, "sqlite": SqliteReader, "partitions": PartitionReader}


def _queries(records: list[dict], cases: list[dict]) -> list[dict]:
    state = build(records)
    return [{"case_id": case["id"], "ranked_ids": [item["id"] for item in rank(
        state, case["query"], source_id=case.get("source_id"), concepts=case.get("concepts"))]}
        for case in cases]


def run_experiment(records: list[dict], cases: list[dict], output: Path, *, repeats: int = 3,
                   input_file_sha256: str | None = None) -> dict:
    if type(repeats) is not int or not 1 <= repeats <= 3:
        raise ValueError("Use between one and three repetitions")
    if not 1 <= len(records) <= 339 or len(cases) != 5 or len({case["id"] for case in cases}) != 5:
        raise ValueError("Use at most 339 records and exactly five distinct development cases")
    code_hashes = _code_hashes()
    ordered = sorted(records, key=identity)
    reference = _queries(ordered, cases)  # Existing build rejects duplicate source identities.
    source_hashes = {identity(record): digest(record) for record in ordered}
    sample_ids = [identity(record) for record in ordered[:5]]
    config = {"repeats": repeats, "sample_ids": sample_ids, "partition_prefix_hex_digits": 1,
              "ranking": "existing web216_experiments.build/rank with explicit case facets/concepts",
              "lookup_limit": "five identifiers times at most three cold/warm pairs per layout"}
    output = Path(output)
    output.mkdir(mode=0o700, parents=True, exist_ok=False)
    started_at, started = _utc(), time.perf_counter_ns()
    write_layouts(ordered, output)
    arms = {}
    for name, reader_class in READERS.items():
        reader = reader_class(output / name)
        try:
            reconstructed = reader.all_records()
            queries = _queries(reconstructed, cases)
            if canonical(reconstructed) != canonical(ordered) or queries != reference:
                raise ValueError("Storage layout changed logical records or ranked result identifiers")
            initial_bytes = reader.initial_bytes
        finally:
            reader.close()
        samples = []
        for repetition in range(repeats):
            for key in sample_ids:
                tick = time.perf_counter_ns()
                reader = reader_class(output / name)
                try:
                    cold = reader.lookup(key)
                    cold_ms = (time.perf_counter_ns() - tick) / 1_000_000
                    cold_bytes = reader.bytes_read
                    tick = time.perf_counter_ns()
                    warm = reader.lookup(key)
                    warm_ms = (time.perf_counter_ns() - tick) / 1_000_000
                    warm_bytes = None if cold_bytes is None else reader.bytes_read - cold_bytes
                    if (cold is None or canonical(cold) != canonical(warm) or identity(cold) != key
                            or digest(cold) != source_hashes[key]):
                        raise ValueError("Exact-detail lookup changed the selected source record")
                    samples.append({"repetition": repetition + 1, "id": key,
                                    "record_sha256": digest(cold), "cold_ms": cold_ms, "warm_ms": warm_ms,
                                    "cold_application_file_bytes": cold_bytes, "warm_application_file_bytes": warm_bytes})
                finally:
                    reader.close()
        files = [{"path": path.relative_to(output).as_posix(), "bytes": path.stat().st_size,
                  "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                 for path in sorted((output / name).iterdir()) if path.is_file()]
        arms[name] = {"persisted_bytes": sum(item["bytes"] for item in files), "files": files,
                      "initial_application_payload_bytes": initial_bytes, "logical_records_sha256": digest(reconstructed),
                      "record_count": len(reconstructed), "query_results": queries, "query_results_sha256": digest(queries),
                      "records_equal": True, "ranked_ids_equal": True, "detail_samples": samples,
                      "cold_ms_median": statistics.median(item["cold_ms"] for item in samples),
                      "warm_ms_median": statistics.median(item["warm_ms"] for item in samples)}
    revision = subprocess.run(["git", "--no-replace-objects", "-C", str(ROOT), "rev-parse", "HEAD"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=10)
    if _code_hashes() != code_hashes:
        raise ValueError("Executable source files changed during the storage experiment; no result published")
    result = {
        "schema_version": "web216.local-storage-experiment.v1", "experiment": "X05",
        "classification": "local-development-storage-comparison-not-hosting-benchmark",
        "started_at_utc": started_at, "ended_at_utc": _utc(),
        "elapsed_seconds": (time.perf_counter_ns() - started) / 1_000_000_000,
        "code_commit": revision.stdout.decode().strip(), "code_file_sha256": code_hashes,
        "config": config, "config_sha256": digest(config), "input_file_sha256": input_file_sha256,
        "input_records_sha256": digest(ordered), "cases_sha256": digest(cases), "record_count": len(ordered),
        "environment": {"python": platform.python_version(), "sqlite": sqlite3.sqlite_version,
                        "system": platform.system(), "machine": platform.machine()},
        "provider_requests": 0, "model_requests": 0, "sites_or_d1_requests": 0,
        "network_bytes": 0, "hosting_cost": None, "optimality_claimed": False,
        "limitations": [
            "Cold is a fresh application reader/connection including initialisation; OS/disk caches are uncontrolled.",
            "Warm immediately repeats the same identifier on that reader; this is not a multi-user load test.",
            "Initial bytes are eagerly read application payloads, not HTTP transfer or OS page I/O; SQLite is unknown.",
            "Persisted bytes count generated files, not filesystem allocation, RAM, remote storage or D1 billing.",
            "Local stdlib SQLite is not Sites D1; this does not test D1 limits, residency or deployment compatibility.",
            "Digest-prefix JSON partitions are a surrogate, not Parquet, columnar compression or object-store measurements.",
            "All five development queries rebuild the same existing rank state from reconstructed records; no native SQL ranking.",
            "Small fixed corpus, at most three repetitions, no unseen relevance judgements or optimality claim.",
            "Source file hashes agree at run start and end; this does not attest to earlier Python import state.",
        ], "arms": arms,
    }
    result["result_sha256"] = digest(result)
    _write(output / "result.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="Fresh experiment directory")
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    try:
        original = _corpus_bytes(args.corpus)
        records = load_corpus(args.corpus)
        if len(records) != 339 or _corpus_bytes(args.corpus) != original:
            raise ValueError("CLI requires the unchanged pinned 339-record comparison corpus")
        cases = json.loads(CASES.read_bytes())
        result = run_experiment(records, cases, args.output, repeats=args.repeats,
                                input_file_sha256=hashlib.sha256(original).hexdigest())
    except (OSError, ValueError, sqlite3.Error, subprocess.SubprocessError) as error:
        parser.exit(1, f"Storage experiment failed: {error}\n")
    print(f"Compared {result['record_count']} records across three local layouts; no hosting or optimality claim")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
