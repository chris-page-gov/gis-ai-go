#!/usr/bin/env python3
"""Deterministic, local metadata discovery. No model calls or live retrieval."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

MAX_INDEX_BYTES = 256 * 1024 * 1024
MAX_RECORDS = 100_000
MAX_QUERY_TERMS = 64
MAX_RESPONSE_BYTES = 1024 * 1024
IMPLEMENTATION_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
FIELDS = (
    "id", "title", "description", "text", "type", "sourceFamily",
    "nativeIdentifier", "sources", "temporal", "update", "details", "tags",
    "resource", "route", "rights", "limitations", "schemaEvidence",
    "assertionStatus", "reviewStatus", "status",
)
WEIGHTS = {
    "id": 20, "nativeIdentifier": 25, "title": 12, "description": 5,
    "text": 2, "type": 3, "sourceFamily": 6, "tags": 7,
    "temporal": 4, "update": 4, "details": 3, "rights": 1,
    "limitations": 1, "schemaEvidence": 2,
}
# Qualifying words such as not, before, after and without deliberately survive.
STOP_WORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "can", "data", "dataset",
    "datasets", "do", "does", "for", "from", "have", "how", "i", "in",
    "is", "it", "me", "of", "on", "or", "please", "show", "tell", "that",
    "the", "their", "these", "this", "to", "us", "what", "when", "where",
    "which", "with",
})


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def render(result: dict[str, Any]) -> bytes:
    """The CLI's exact output, including its one final newline."""
    return canonical_bytes(result) + b"\n"


def _normalise(value: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", value.casefold())
                   if not unicodedata.combining(c))


def _flatten(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        # Field names help distinguish source-native date and frequency roles.
        return " ".join(f"{k} {_flatten(v)}" for k, v in sorted(value.items()))
    if isinstance(value, list):
        return " ".join(_flatten(v) for v in value)
    return "" if value is None else str(value)


def _tokens(value: str) -> set[str]:
    # Split camelCase keys without conflating their semantic roles.
    value = re.sub(r"([a-z])([A-Z])", r"\1 \2", value)
    return set(re.findall(r"[a-z0-9]+", _normalise(value)))


def _count_bytes(result: dict[str, Any]) -> int:
    # The byte count includes its own decimal representation and the envelope.
    for _ in range(8):
        size = len(render(result))
        if result["counts"]["responseBytes"] == size:
            return size
        result["counts"]["responseBytes"] = size
    raise ValueError("Could not stabilise response byte count")


def _query_plan(question: str) -> dict[str, Any]:
    tokens = _tokens(question)
    frequency = next((label for label, terms in (
        ("monthly", {"monthly"}), ("quarterly", {"quarterly"}),
        ("annual", {"annual", "annually", "yearly"}),
        ("weekly", {"weekly"}), ("daily", {"daily"}),
    ) if tokens & terms), None)
    return {
        "publicationFrequency": bool(tokens & {"update", "updated", "updates", "release", "releases", "released", "publication", "cadence", "often"})
        and not bool(tokens & {"observation", "observations", "statistical"}),
        "frequencyLabel": frequency,
        "releaseFeed": bool(tokens & {"feed", "feeds", "rss", "atom"}),
        "temporalCoverage": bool(tokens & {"coverage", "period", "periods", "range", "years", "extent"}),
    }


def _structured_matches(record: dict[str, Any], plan: dict[str, Any]) -> list[str]:
    """Rank only explicitly named field roles; never infer values from titles."""
    matches = []
    update = record.get("update") or {}
    temporal = record.get("temporal") or {}
    if not isinstance(update, dict) or not isinstance(temporal, dict):
        raise ValueError("temporal and update must be objects")
    frequency = update.get("frequency") or {}
    if not isinstance(frequency, dict):
        raise ValueError("update frequency must be an object")
    label = _normalise(str(frequency.get("label") or ""))
    label = {"annually": "annual", "yearly": "annual"}.get(label, label)
    if (plan["publicationFrequency"] and frequency.get("status") == "source-stated"
            and frequency.get("sourceField") == "release_frequency"
            and label and (not plan["frequencyLabel"] or label == plan["frequencyLabel"])):
        matches.append("update.frequency:source-release-frequency")
    if plan["releaseFeed"] and isinstance(update.get("releaseFeed"), list) and update["releaseFeed"]:
        matches.append("update.releaseFeed:advertised-route")
    if (plan["temporalCoverage"] and temporal.get("status") == "source-stated"
            and temporal.get("sourceField") and (temporal.get("start") or temporal.get("end"))):
        matches.append("temporal:source-stated-extent")
    if (plan["temporalCoverage"] and temporal.get("status") == "normalised-source-options"
            and temporal.get("kind") == "available-native-period-options"
            and temporal.get("sourceField") and temporal.get("derivation")
            and temporal.get("start") is not None and temporal.get("end") is not None):
        matches.append("temporal:complete-native-option-extrema")
    return matches


class PreparedIndex:
    """Immutable-by-ownership, bounded local snapshot with weighted postings.

    Preparation takes a private copy. Later caller mutations of either the input
    or a returned result cannot invalidate the retained digest and token index.
    """

    def __init__(self, index: dict[str, Any]):
        if not isinstance(index, dict) or not isinstance(index.get("records"), list):
            raise ValueError("index must contain a records array")
        if len(index["records"]) > MAX_RECORDS:
            raise ValueError("index record limit exceeded")
        encoded = canonical_bytes(index)
        if len(encoded) > MAX_INDEX_BYTES:
            raise ValueError("index byte limit exceeded")
        self.index_sha256 = hashlib.sha256(encoded).hexdigest()
        frozen = json.loads(encoded)
        self.revision = frozen.get("sourceRevision", frozen.get("revision"))
        if self.revision is not None and (not isinstance(self.revision, str)
                                         or not re.fullmatch(r"[a-f0-9]{40,64}", self.revision)):
            raise ValueError("source revision must be an immutable hexadecimal identity")
        self._records = frozen["records"]
        self._postings: dict[str, list[tuple[int, int]]] = {}
        self._identifiers: dict[str, list[tuple[int, bool]]] = {}
        seen = set()
        for ordinal, record in enumerate(self._records):
            if not isinstance(record, dict) or not isinstance(record.get("id"), str) or not record["id"]:
                raise ValueError("each record requires a non-empty string id")
            if record["id"] in seen:
                raise ValueError("duplicate record identity")
            seen.add(record["id"])
            _structured_matches(record, {"publicationFrequency": False, "releaseFeed": False,
                                         "temporalCoverage": False})
            terms: dict[str, int] = {}
            for field, weight in WEIGHTS.items():
                for token in _tokens(_flatten(record.get(field))):
                    terms[token] = terms.get(token, 0) + weight
            for token, weight in terms.items():
                self._postings.setdefault(token, []).append((ordinal, weight))
            for field in ("id", "nativeIdentifier"):
                identifier = record.get(field)
                if isinstance(identifier, str) and identifier:
                    shaped = bool(re.search(r"[0-9_:./-]|[A-Z].*[A-Z]", identifier))
                    self._identifiers.setdefault(_normalise(identifier), []).append((ordinal, shaped))

    def _rank(self, question: str, terms: list[str], plan: dict[str, Any]) -> list[tuple[int, int, bool, list[str]]]:
        scores: dict[int, int] = {}
        for term in terms:
            for ordinal, weight in self._postings.get(term, ()):
                scores[ordinal] = scores.get(ordinal, 0) + weight
        query = _normalise(question)
        exact = set()
        for needle, entries in self._identifiers.items():
            if len(needle) > len(query) or needle not in query:
                continue
            whole = query.strip() == needle
            if not whole and (len(needle) < 3 or not re.search(r"(?<![\w])" + re.escape(needle) + r"(?![\w])", query)):
                continue
            for ordinal, shaped in entries:
                if whole or shaped:
                    exact.add(ordinal)
        for ordinal in exact:
            scores[ordinal] = scores.get(ordinal, 0) + 10000
        ranked = []
        for ordinal, record in enumerate(self._records):
            structured = _structured_matches(record, plan)
            if ordinal not in scores and not structured:
                continue
            score = scores.get(ordinal, 0)
            ranked.append((ordinal, score + 100 * len(structured), ordinal in exact, structured))
        return sorted(ranked, key=lambda row: (-row[1], self._records[row[0]]["id"]))

    def _result(self, rank: tuple[int, int, bool, list[str]], terms: list[str]) -> dict[str, Any]:
        ordinal, score, exact, structured = rank
        record = self._records[ordinal]
        matches = {}
        for field in WEIGHTS:
            matched = sorted(set(terms) & _tokens(_flatten(record.get(field))))
            if matched:
                matches[field] = matched
        return {"record": copy.deepcopy({k: record[k] for k in FIELDS if k in record}),
                "score": score, "identifierMatch": exact, "matchedFields": matches,
                "structuredMatches": structured}


def search(index: dict[str, Any] | PreparedIndex, question: str, max_records: int = 10,
           max_bytes: int = 65536) -> dict[str, Any]:
    """Rank all local records, retaining whole evidence and explicit omissions.

    The digest binds canonical index content. The CLI separately adds an exact
    file-byte digest before applying the response byte ceiling.
    """
    return _search(index, question, max_records, max_bytes)


def _search(index: dict[str, Any] | PreparedIndex, question: str, max_records: int,
            max_bytes: int, file_digest: str | None = None) -> dict[str, Any]:
    if type(max_records) is not int or not 1 <= max_records <= 100:
        raise ValueError("max_records must be an integer from 1 to 100")
    if type(max_bytes) is not int or not 1024 <= max_bytes <= MAX_RESPONSE_BYTES:
        raise ValueError("max_bytes must be an integer from 1024 to 1048576")
    if not isinstance(question, str) or not question.strip() or len(question) > 2000:
        raise ValueError("question must contain 1 to 2000 characters")
    prepared = index if isinstance(index, PreparedIndex) else PreparedIndex(index)
    terms = sorted(_tokens(question) - STOP_WORDS)
    wanted = terms[:MAX_QUERY_TERMS]
    plan = _query_plan(question)
    ranked = prepared._rank(question, wanted, plan)
    result = {
        "schema": "gis-ai-go.okf-plus-search-result.v1",
        "algorithm": "gis-ai-go.okf-plus-lexical.v1",
        "implementationSha256": IMPLEMENTATION_SHA256,
        "status": "discovery-only",
        "sourceRevision": prepared.revision,
        "indexSha256": prepared.index_sha256,
        "indexDigestBasis": "UTF-8 sorted compact JSON; no final newline",
        "question": question,
        "queryTerms": wanted,
        "queryPlan": plan,
        "limits": {"maxRecords": max_records, "maxBytes": max_bytes,
                   "maxQueryTerms": MAX_QUERY_TERMS},
        "counts": {"recordsInIndex": len(prepared._records),
                   "matchingCandidates": len(ranked), "returned": 0,
                   "omittedCandidates": len(ranked),
                   "omittedQueryTerms": max(0, len(terms) - len(wanted)),
                   "responseBytes": 0},
        "truncated": False,
        "omissions": [],
        "results": [prepared._result(row, wanted) for row in ranked[:max_records]],
        "limitations": [
            "Metadata discovery only; ranking does not establish evidence sufficiency or current live availability.",
            "Statistical frequency, publication cadence, geography vintage and observation coverage retain their separate source meanings.",
        ],
    }
    if file_digest:
        result["indexFileSha256"] = file_digest
    byte_limited = False
    while True:
        result["counts"]["returned"] = len(result["results"])
        result["counts"]["omittedCandidates"] = len(ranked) - len(result["results"])
        result["omissions"] = (
            (["record-limit"] if len(ranked) > max_records else [])
            + (["byte-limit"] if byte_limited else [])
            + (["query-term-limit"] if len(terms) > len(wanted) else [])
        )
        result["truncated"] = bool(result["omissions"])
        if _count_bytes(result) <= max_bytes:
            return result
        if not result["results"]:
            raise ValueError("max_bytes cannot accommodate the discovery envelope")
        # Preserve rank order; never silently shorten evidence or fill its place
        # with a lower-ranked item after dropping a larger, higher-ranked one.
        result["results"].pop()
        byte_limited = True


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _invalid_constant(_value: str) -> None:
    raise ValueError("non-finite JSON number")


def _load_index_bytes(path: Path) -> tuple[dict[str, Any], bytes]:
    with Path(path).open("rb") as handle:
        raw = handle.read(MAX_INDEX_BYTES + 1)
    if len(raw) > MAX_INDEX_BYTES:
        raise ValueError("index byte limit exceeded")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object,
                       parse_constant=_invalid_constant)
    if not isinstance(value, dict) or not isinstance(value.get("records"), list):
        raise ValueError("index must contain a records array")
    return value, raw


def load_index(path: Path) -> dict[str, Any]:
    """Read a bounded local JSON index, rejecting duplicate/non-finite JSON."""
    return _load_index_bytes(path)[0]


def evaluate_cases(index: dict[str, Any] | PreparedIndex, corpus: dict[str, Any]) -> dict[str, Any]:
    """Evaluate declared metadata retrieval only, never semantic sufficiency."""
    if corpus.get("schema") != "gis-ai-go.okf-plus-question-corpus.v1":
        raise ValueError("unsupported question corpus")
    cases = corpus.get("cases")
    if not isinstance(cases, list) or len(cases) > 200:
        raise ValueError("invalid or excessive question cases")
    seen = set()
    outcomes = []
    defaults = corpus.get("defaults", {})
    prepared = index if isinstance(index, PreparedIndex) else PreparedIndex(index)
    for case in cases:
        if not isinstance(case.get("id"), str) or case["id"] in seen:
            raise ValueError("question cases require unique identities")
        seen.add(case["id"])
        if case.get("mode") == "context-required":
            outcomes.append({"id": case["id"], "status": "not-evaluated-context-required"})
            continue
        if case.get("mode") != "retrieval":
            raise ValueError("unsupported question evaluation mode")
        result = search(prepared, case["question"],
                        case.get("maxRecords", defaults.get("maxRecords", 10)),
                        case.get("maxBytes", defaults.get("maxBytes", 65536)))
        records = [row["record"] for row in result["results"]]
        failures = []
        ranks = []
        for target in case.get("targets", []):
            rank = next((i + 1 for i, row in enumerate(records)
                         if all(row.get(k) == v for k, v in target.items())), None)
            ranks.append({"target": target, "rank": rank})
            if rank is None:
                failures.append("expected-record-not-retained")
        for check in case.get("fieldChecks", []):
            matched = [r for r in records if r.get("nativeIdentifier") == check["nativeIdentifier"]
                       and (not check.get("sourceFamily") or r.get("sourceFamily") == check["sourceFamily"])]
            value = matched[0] if len(matched) == 1 else None
            present = len(matched) == 1
            for key in check["path"]:
                if not isinstance(value, dict) or key not in value:
                    present = False
                    break
                value = value[key]
            if not present or canonical_bytes(value) != canonical_bytes(check["equals"]):
                failures.append("source-field-mismatch")
        if ("expectedCandidateCount" in case
                and result["counts"]["matchingCandidates"] != case["expectedCandidateCount"]):
            failures.append("candidate-count-mismatch")
        outcomes.append({"id": case["id"], "status": "failed" if failures else "passed-retrieval",
                         "failures": failures, "targetRanks": ranks, "counts": result["counts"],
                         "truncated": result["truncated"], "omissions": result["omissions"]})
    return {
        "schema": "gis-ai-go.okf-plus-retrieval-evaluation.v1",
        "sourceRevision": prepared.revision,
        "indexSha256": prepared.index_sha256,
        "questionCorpusSha256": hashlib.sha256(canonical_bytes(corpus)).hexdigest(),
        "implementationSha256": IMPLEMENTATION_SHA256,
        "counts": {"cases": len(outcomes),
                   "passedRetrieval": sum(r["status"] == "passed-retrieval" for r in outcomes),
                   "failedRetrieval": sum(r["status"] == "failed" for r in outcomes),
                   "notEvaluatedContextRequired": sum(r["status"] == "not-evaluated-context-required" for r in outcomes)},
        "cases": outcomes,
        "limitations": ["Retrieval and literal field checks only; manual review boundaries are not automatically passed.",
                        "No live data, semantic sufficiency, model answer, MCP deployment or installed Ask OKF acceptance is established."],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--max-records", type=int, default=10)
    parser.add_argument("--max-bytes", type=int, default=65536)
    args = parser.parse_args(argv)
    try:
        index, raw = _load_index_bytes(args.index)
        result = _search(index, args.question, args.max_records, args.max_bytes,
                         hashlib.sha256(raw).hexdigest())
    except (OSError, UnicodeError, ValueError, TypeError, RecursionError):
        # Do not disclose local paths or source content through error messages.
        print("Could not validate the local index, question or output budget.", file=sys.stderr)
        return 2
    sys.stdout.buffer.write(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
