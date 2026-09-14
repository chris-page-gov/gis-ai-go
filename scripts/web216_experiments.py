"""Offline WEB-216 development experiments; no provider or MCP execution.

Source metadata is data, not instructions. Ranking does not consume gold labels,
evaluation aliases, arbitrary source fields or model-written answers.
"""

from __future__ import annotations

import argparse
import copy
import json
import platform
import re
import statistics
import time
from pathlib import Path
from typing import Any

if __package__:
    from .web216_corpus import canonical, digest, identity, load_corpus
else:
    from web216_corpus import canonical, digest, identity, load_corpus


ROOT = Path(__file__).resolve().parents[1]
VIEW_VERSION = "web216.discovery-view.v1"
CONCEPT_VERSION = "web216.curated-dimension-vocabulary.v1"
# Explicit engineering mappings, not learned relevance labels or equivalence claims.
# Evidence is the exact native dimension name attached to each derived edge.
DIMENSION_CONCEPTS = {
    "C_AGE": "age",
    "GENDER": "sex",
    "GEOGRAPHY": "geography",
    "ltla": "local-authority",
    "occupancy_rating_rooms_6a": "occupancy-rooms",
}
STORY_IDS = {
    "ons-data-api:cpih01", "ons-data-api:TS001", "ons-data-api:TS053",
    "ons-data-api:TS052", "ons-data-api:TS017",
    "nomis-dataset-definitions:NM_2002_1", "nomis-dataset-definitions:NM_2006_1",
}


def tokens(text: str) -> list[str]:
    """Bounded deterministic Unicode words; do not silently truncate a query."""
    return re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE)


def project(record: dict[str, Any]) -> dict[str, Any]:
    native_dimensions = []
    for dimension in record.get("versionDimensions", []):
        native_dimensions.append(dimension.get("id", ""))
    for component in record.get("components", []):
        if component.get("kind") in {"dimension", "timedimension"}:
            native_dimensions.append(component.get("concept", ""))
    edges = [
        {"concept": DIMENSION_CONCEPTS[name], "native_dimension": name,
         "status": "curated-mapping", "vocabulary": CONCEPT_VERSION}
        for name in sorted(set(native_dimensions)) if name in DIMENSION_CONCEPTS
    ]
    # No evaluation_aliases, free-form annotations, URLs or gold-answer text here.
    return {
        "id": identity(record), "source_id": record["sourceId"],
        "title": record["title"], "description": record.get("description", ""),
        "keywords": record.get("keywords", []), "concept_edges": edges,
        "source_record_sha256": digest(record),
        "execution": "not-enabled-by-this-experiment",
    }


def build(records: list[dict[str, Any]], previous: dict | None = None) -> dict:
    """Reuse unchanged in-memory projections; regenerate all derived postings.

    The previous state must be this function's process-local output, not a supplied
    cache file. This experiment does not establish a durable cache trust boundary.
    """
    entries, reused, seen = {}, 0, set()
    contract = digest({"view_version": VIEW_VERSION, "concept_version": CONCEPT_VERSION,
                       "dimension_concepts": DIMENSION_CONCEPTS})
    previous_entries = (previous or {}).get("entries", {})
    if previous and (previous.get("version") != VIEW_VERSION or previous.get("contract_sha256") != contract):
        previous_entries = {}
    for record in records:
        key = identity(record)
        if key in seen:
            raise ValueError("Duplicate source identity")
        seen.add(key)
        source_hash = digest(record)
        prior = previous_entries.get(key)
        if prior and prior["source_sha256"] == source_hash:
            entry = copy.deepcopy(prior)
            if digest(entry["view"]) != entry["view_sha256"]:
                raise ValueError("Corrupt in-memory projection")
            reused += 1
        else:
            view = project(record)
            entry = {"source_sha256": source_hash, "view": view, "view_sha256": digest(view)}
        entries[key] = entry
    postings: dict[str, list[str]] = {}
    concepts: dict[str, list[str]] = {}
    for key in sorted(entries):
        view = entries[key]["view"]
        text = " ".join([view["title"], view["description"], *view["keywords"]])
        for token in sorted(set(tokens(text))):
            postings.setdefault(token, []).append(key)
        for concept in sorted({edge["concept"] for edge in view["concept_edges"]}):
            concepts.setdefault(concept, []).append(key)
    logical = {"version": VIEW_VERSION, "contract_sha256": contract, "entries": entries, "postings": postings,
               "concepts": concepts}
    return {**logical, "logical_sha256": digest(logical), "reused_count": reused}


def rank(state: dict, query: str, *, concepts: list[str] | None = None,
         source_id: str | None = None) -> list[dict]:
    if not isinstance(query, str) or len(query) > 256 or len(tokens(query)) > 10:
        raise ValueError("Query exceeds 256 characters or 10 normalised terms")
    requested = concepts or []
    if len(requested) > 5 or any(x not in set(DIMENSION_CONCEPTS.values()) for x in requested):
        raise ValueError("Unknown or excessive concepts")
    if source_id is not None and source_id not in {"ons-data-api", "nomis-dataset-definitions"}:
        raise ValueError("Unknown source facet")
    scores: dict[str, int] = {}
    for token in set(tokens(query)):
        for key in state["postings"].get(token, []):
            scores[key] = scores.get(key, 0) + 1
    for concept in set(requested):
        for key in state["concepts"].get(concept, []):
            scores[key] = scores.get(key, 0) + 2
    return [{"id": key, "score": score} for key, score in
            sorted(scores.items(), key=lambda item: (-item[1], item[0]))
            if not source_id or state["entries"][key]["view"]["source_id"] == source_id]


def mutation_check(records: list[dict]) -> dict:
    """Synthetic add/change/delete, never described as an actual upstream update."""
    original = build(records)
    changed = copy.deepcopy(records)
    changed[0]["title"] += " synthetic amendment marker"
    removed = changed.pop(1)
    added = copy.deepcopy(records[1])
    added["sourceRecordId"] = "WEB216-SYNTHETIC-ADDITION"
    added["title"] = "Synthetic geography test record"
    changed.append(added)
    full, incremental = build(changed), build(changed, original)
    equal = full["logical_sha256"] == incremental["logical_sha256"]
    absent = identity(removed) not in incremental["entries"] and all(
        identity(removed) not in ids for ids in
        [*incremental["postings"].values(), *incremental["concepts"].values()])
    if not equal or not absent:
        raise ValueError("Incremental build diverged from full build")
    return {"mutation_kind": "synthetic-add-change-delete", "equal_logical_output": equal,
            "deleted_identity_absent": absent, "reused_records": incremental["reused_count"],
            "full_sha256": full["logical_sha256"], "incremental_sha256": incremental["logical_sha256"]}


def evaluate(records: list[dict], cases: list[dict], *, repeats: int = 5) -> dict:
    if not 1 <= repeats <= 100:
        raise ValueError("Repeats must be between 1 and 100")
    ids = {identity(record) for record in records}
    if not STORY_IDS <= ids:
        raise ValueError("Corpus lacks required development and contrast records")
    arms = {
        "story-subset": [r for r in records if identity(r) in STORY_IDS],
        "comparison-full": records,
        "comparison-lazy-detail": records,
    }
    output = {}
    for name, arm_records in arms.items():
        arm_ids = {identity(record) for record in arm_records}
        timings = []
        for _ in range(repeats):
            start = time.perf_counter_ns()
            state = build(arm_records)
            timings.append((time.perf_counter_ns() - start) / 1_000_000)
        full_bytes = len(canonical(arm_records))
        summary = [state["entries"][key]["view"] for key in sorted(state["entries"])]
        initial_bytes = len(canonical(summary)) if name.endswith("lazy-detail") else full_bytes
        results = []
        for case in cases:
            for mode in ("keyword-facet", "keyword-facet-concepts"):
                start = time.perf_counter_ns()
                candidates = rank(state, case["query"], source_id=case.get("source_id"),
                                  concepts=case.get("concepts") if mode.endswith("concepts") else None)
                elapsed = (time.perf_counter_ns() - start) / 1_000_000
                expected = case["expected_ids"]  # scorer only, after retrieval
                top = [candidate["id"] for candidate in candidates[:5]]
                accepted_ranks = [i + 1 for i, candidate in enumerate(candidates)
                                  if candidate["id"] in expected]
                # Physical byte model, not observed browser/network performance.
                top_record = next((r for r in arm_records if candidates and
                                   identity(r) == candidates[0]["id"]), None)
                detail_bytes = len(canonical(top_record)) if top_record and name.endswith("lazy-detail") else 0
                results.append({"case_id": case["id"], "mode": mode, "top_five": top,
                                "expected_present": any(x in arm_ids for x in expected),
                                "first_relevant_rank": min(accepted_ranks, default=None),
                                "recall_at_five": len(set(expected) & set(top)) / len(expected) if expected else None,
                                "empty_result": not candidates, "ranking_ms": elapsed,
                                "first_detail_bytes": detail_bytes})
        output[name] = {"record_count": len(arm_records), "initial_json_bytes": initial_bytes,
                        "full_record_json_bytes": full_bytes, "initial_gzip_bytes": None,
                        "build_ms_samples": timings, "build_ms_median": statistics.median(timings),
                        "logical_sha256": state["logical_sha256"], "cases": results}
    return {"schema_version": "web216.offline-experiment.v1", "view_version": VIEW_VERSION,
            "concept_vocabulary": CONCEPT_VERSION, "classification": "development-not-confirmatory",
            "corpus_sha256": digest(records), "cases_sha256": digest(cases),
            "environment": {"python": platform.python_version(), "system": platform.system(),
                            "machine": platform.machine()},
            "provider_requests": 0, "model_requests": 0, "provider_charge": 0,
            "agent_token_cost": None, "actual_network_bytes": None,
            "limitations": ["Frozen metadata, not current provider observations",
                            "Development cases and curated concepts are not blinded",
                            "Concept hints are author-supplied, not automatic intent understanding",
                            "JSON bytes are an analytical model, not host measurements",
                            "No full-corpus, optimality, user-research or execution-support claim"],
            "arms": output, "incremental": mutation_check(records)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=ROOT / "tests/fixtures/web216/story-corpus.json")
    parser.add_argument("--cases", type=Path, default=ROOT / "tests/fixtures/web216/development-cases.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    records = load_corpus(args.corpus)
    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    started = time.time()
    result = evaluate(records, cases, repeats=args.repeats)
    result["started_at_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started))
    result["elapsed_seconds"] = time.time() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"status": "completed", "records": len(records),
                      "result_sha256": digest(result), "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
