"""Offline, bounded discovery and explicit traversal of atomic OKF+ cards.

SQLite is a machine index, never an AI context document. Queries read only the
selected small cards; source snapshots are not opened or fetched. Associative
query expansion helps discovery and makes no claim of semantic equivalence.
"""
from __future__ import annotations

import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
from typing import Any
from urllib.parse import quote

MAX_CARD_BYTES = 16384
MAX_RESPONSE_BYTES = 1048576
MAX_QUERY_TERMS = 64
INDEX_NAME = "semantic.sqlite3"
SCHEMA = "gis-ai-go.okf-plus-semantic-index.v1"
EXPANSION_RELATIONS = ("parent", "codeList", "related", "children", "semantic-companion",
                       "schema", "queryable-schema")
STOP_WORDS = frozenset("a an and are as at be by can do does for from how i in is it of on or our the this to us we what which with".split())
# These are discovery associations, never field mappings or answer templates.
ALIASES = {"pavement": ("footway", "sidewalk"), "sidewalk": ("footway", "pavement"),
           "height": ("elevation", "altitude"), "elevation": ("height", "altitude"),
           "width": ("widths",), "heights": ("height", "elevation"),
           "roads": ("road",), "buildings": ("building",)}


def render(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate card key")
        result[key] = value
    return result


def _flatten(value):
    if isinstance(value, dict):
        return " ".join(str(key) + " " + _flatten(item) for key, item in value.items())
    if isinstance(value, list):
        return " ".join(_flatten(item) for item in value)
    return str(value) if value is not None else ""


def _tokens(value):
    words = re.sub(r"([a-z])([A-Z])", r"\1 \2", value)
    return re.findall(r"[^\W_]+", words.casefold(), flags=re.UNICODE)


def _card_path(root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or len(path.parts) != 3 or path.parts[0] != "cards" or ".." in path.parts:
        raise ValueError("invalid indexed card path")
    candidate = root / path
    if candidate.is_symlink() or not candidate.resolve().is_relative_to(root.resolve() / "cards"):
        raise ValueError("card path escapes card directory")
    return candidate


def _read_card(path: Path, expected_hash: str | None = None):
    with path.open("rb") as stream:
        raw = stream.read(MAX_CARD_BYTES + 1)
    if len(raw) > MAX_CARD_BYTES:
        raise ValueError("card exceeds atomic byte limit")
    digest = hashlib.sha256(raw).hexdigest()
    if expected_hash is not None and digest != expected_hash:
        raise ValueError("card integrity mismatch; regenerate the index")
    text = raw.decode("utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("invalid card front matter")
    header, body = text[4:].split("\n---\n", 1)
    def reject(_):
        raise ValueError("non-finite card value")
    card = json.loads(header, object_pairs_hook=_unique, parse_constant=reject)
    if not isinstance(card, dict) or not all(isinstance(card.get(key), str) and card[key]
                                            for key in ("@id", "kind", "title")):
        raise ValueError("card identity, kind and title are required")
    if not isinstance(card.get("source"), dict) or not isinstance(card.get("gaps", []), list):
        raise ValueError("card provenance and gaps are required")
    return card, body.strip(), digest


def _reference(value):
    return value.get("@id") if isinstance(value, dict) else value if isinstance(value, str) else None


def _links(card):
    for relation in ("parent", "codeList"):
        target = _reference(card.get(relation))
        if target:
            yield relation, target
    for item in card.get("related", []):
        target = _reference(item)
        if target:
            yield str(item.get("relation", "related")) if isinstance(item, dict) else "related", target


def build_index(root: Path, revision: str | None = None) -> dict[str, Any]:
    """Build atomically from small generated cards, with no source-file reads."""
    root = Path(root)
    if revision is not None and not re.fullmatch(r"[0-9a-f]{7,64}", revision):
        raise ValueError("revision must be an immutable hexadecimal identity")
    root.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(prefix=".semantic-", suffix=".sqlite3", dir=root, delete=False)
    temporary = Path(handle.name)
    handle.close()
    digest = hashlib.sha256()
    count = 0
    try:
        with sqlite3.connect(temporary) as connection:
            connection.executescript("""
                CREATE TABLE metadata (name TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE cards (id TEXT PRIMARY KEY, path TEXT UNIQUE NOT NULL,
                    sha256 TEXT NOT NULL, native TEXT, collection_id TEXT, version TEXT,
                    kind TEXT NOT NULL, parent_id TEXT);
                CREATE INDEX cards_native ON cards(native, collection_id, version);
                CREATE INDEX cards_parent ON cards(parent_id, id);
                CREATE TABLE links (source TEXT NOT NULL, relation TEXT NOT NULL,
                    target TEXT NOT NULL, PRIMARY KEY(source, relation, target));
                CREATE VIRTUAL TABLE terms USING fts5(id UNINDEXED, words, tokenize='unicode61');
            """)
            for path in sorted((root / "cards").glob("*/*.md")):
                relative = path.relative_to(root).as_posix()
                card, body, card_digest = _read_card(_card_path(root, relative))
                connection.execute("INSERT INTO cards VALUES (?,?,?,?,?,?,?,?)", (
                    card["@id"], relative, card_digest, card.get("nativeIdentifier"),
                    card.get("collectionId"), str(card["version"]) if card.get("version") is not None else None,
                    card["kind"], _reference(card.get("parent"))))
                # Repeat identifying terms to weight them above incidental prose.
                identity = " ".join(str(card.get(key, "")) for key in
                                    ("title", "nativeIdentifier", "collectionId"))
                searchable = " ".join(_tokens(identity + " " + identity + " " +
                    _flatten({key: card.get(key) for key in
                              ("title", "description", "facts", "aliases", "gaps", "parentTitle")}) + " " + body))
                connection.execute("INSERT INTO terms VALUES (?,?)", (card["@id"], searchable))
                connection.executemany("INSERT OR IGNORE INTO links VALUES (?,?,?)",
                                       ((card["@id"], relation, target) for relation, target in _links(card)))
                digest.update(render({"id": card["@id"], "path": relative, "sha256": card_digest}))
                count += 1
            summary = {"schema": SCHEMA, "sourceRevision": revision, "cards": count,
                       "cardsSha256": digest.hexdigest(), "maxCardBytes": MAX_CARD_BYTES}
            connection.executemany("INSERT INTO metadata VALUES (?,?)",
                                   ((key, json.dumps(value)) for key, value in summary.items()))
        temporary.replace(root / INDEX_NAME)
        return summary
    finally:
        temporary.unlink(missing_ok=True)


def _connect(root):
    path = (root / INDEX_NAME).resolve()
    connection = sqlite3.connect("file:" + quote(str(path), safe="/") + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only=ON")
    connection.execute("PRAGMA trusted_schema=OFF")
    metadata = {row[0]: json.loads(row[1]) for row in connection.execute("SELECT name,value FROM metadata")}
    if metadata.get("schema") != SCHEMA:
        connection.close()
        raise ValueError("unsupported semantic index")
    return connection, metadata


def _limits(max_records, max_bytes):
    if type(max_records) is not int or not 1 <= max_records <= 100:
        raise ValueError("max_records must be an integer from 1 to 100")
    if type(max_bytes) is not int or not 1024 <= max_bytes <= MAX_RESPONSE_BYTES:
        raise ValueError("max_bytes must be an integer from 1024 to 1048576")


def _envelope(operation, metadata, max_records, max_bytes):
    return {"schema": "gis-ai-go.okf-plus-semantic-result.v1", "operation": operation,
            "status": "discovery-only", "sourceRevision": metadata["sourceRevision"],
            "cardsSha256": metadata["cardsSha256"], "results": [], "truncated": False,
            "omissions": [], "limits": {"maxRecords": max_records, "maxBytes": max_bytes},
            "integrity": "Selected card bytes verified against the local index; source hashes are retained, source snapshots are not re-read.",
            "counts": {"cardsInIndex": metadata["cards"], "returned": 0, "responseBytes": 0}}


def _measure(result):
    # The byte count includes its own representation and the final newline.
    while True:
        size = len(render(result))
        if result["counts"]["responseBytes"] == size:
            return size
        result["counts"]["responseBytes"] = size


def _finish(result, max_bytes):
    while _measure(result) > max_bytes and result["results"]:
        result["results"].pop()
        result["truncated"] = True
        if "byte-limit" not in result["omissions"]:
            result["omissions"].append("byte-limit")
        result["counts"]["returned"] = len(result["results"])
        if "matchingCandidates" in result["counts"]:
            result["counts"]["omittedCandidates"] = result["counts"]["matchingCandidates"] - len(result["results"])
    while _measure(result) > max_bytes and result.get("missingLinks"):
        result["missingLinks"].pop()
        result["omittedMissingLinks"] += 1
        result["truncated"] = True
        if "byte-limit" not in result["omissions"]:
            result["omissions"].append("byte-limit")
    if _measure(result) > max_bytes:
        raise ValueError("response envelope exceeds byte budget")
    return result


def _load(root, row):
    card, body, _ = _read_card(_card_path(root, row["path"]), row["sha256"])
    if card["@id"] != row["id"]:
        raise ValueError("indexed card identity mismatch")
    return card, body


def _summary(card):
    # Do not clip evidence strings: absent descriptions are retrieved with read.
    keys = ("@id", "kind", "title", "nativeIdentifier", "collectionId", "version", "source", "gaps")
    return {**{key: card[key] for key in keys if key in card},
            "description": card.get("description", "") if len(card.get("description", "")) <= 512 else None,
            "details": "Use read with this @id to retrieve the complete atomic card and explicit links."}


def search(root: Path, question: str, max_records: int = 10, max_bytes: int = 32768,
           collection_id: str | None = None, version: str | None = None,
           kind: str | None = None) -> dict[str, Any]:
    _limits(max_records, max_bytes)
    if not isinstance(question, str) or not question.strip() or len(question) > 2000:
        raise ValueError("question must contain 1 to 2000 characters")
    root = Path(root)
    connection, metadata = _connect(root)
    try:
        result = _envelope("search", metadata, max_records, max_bytes)
        all_terms = list(dict.fromkeys(word for word in _tokens(question) if word not in STOP_WORDS))
        terms = all_terms[:MAX_QUERY_TERMS]
        expansions = {term: list(ALIASES[term]) for term in terms if term in ALIASES}
        result.update({"queryTerms": terms, "associativeExpansions": expansions,
                       "expansionMeaning": "Discovery associations only; field meanings, units and datums require the selected evidence."})
        if len(all_terms) > len(terms):
            result["truncated"] = True
            result["omissions"].append("query-term-limit")
        result["counts"]["omittedQueryTerms"] = len(all_terms) - len(terms)
        query_terms = list(dict.fromkeys(terms + [term for values in expansions.values() for term in values]))
        filters, parameters = [], []
        for column, value in (("collection_id", collection_id), ("version", version), ("kind", kind)):
            if value is not None:
                filters.append("c." + column + "=?")
                parameters.append(str(value))
        where = " AND " + " AND ".join(filters) if filters else ""
        if query_terms:
            match = " OR ".join('"' + term.replace('"', '""') + '"' for term in query_terms)
            total = connection.execute("SELECT count(*) FROM terms JOIN cards c ON c.id=terms.id WHERE terms MATCH ?" + where,
                                       [match, *parameters]).fetchone()[0]
            # Rank breadth of the user's concepts before repetition/rarity. An
            # alias belongs to its original query group and earns no extra vote.
            # Each branch uses FTS postings; no card corpus is loaded in Python.
            groups = [' OR '.join('"' + token + '"' for token in
                                 dict.fromkeys([term, *expansions.get(term, [])])) for term in terms]
            cte = "WITH hits AS (" + " UNION ALL ".join(
                "SELECT id FROM terms WHERE terms MATCH ?" for _ in groups) + "), " + \
                "coverage AS (SELECT id,count(*) AS matched_terms FROM hits GROUP BY id) "
            rows = connection.execute(cte +
                "SELECT c.*,coverage.matched_terms,bm25(terms) AS score FROM terms " +
                "JOIN cards c ON c.id=terms.id JOIN coverage ON coverage.id=c.id WHERE terms MATCH ?" +
                where + " ORDER BY coverage.matched_terms DESC,score,c.id LIMIT ?",
                [*groups, match, *parameters, max_records]).fetchall()
        else:
            total, rows = 0, []
        result["counts"].update({"matchingCandidates": total, "omittedCandidates": total - len(rows)})
        for row in rows:
            card, _ = _load(root, row)
            result["results"].append({**_summary(card), "matchedQueryConcepts": row["matched_terms"]})
        result["counts"]["returned"] = len(result["results"])
        if total > len(rows):
            result["truncated"] = True
            result["omissions"].append("record-limit")
        return _finish(result, max_bytes)
    finally:
        connection.close()


def read_item(root: Path, identifier: str, *, collection_id: str | None = None,
              version: str | None = None, expand: tuple[str, ...] = (), depth: int = 1,
              max_records: int = 10, max_bytes: int = 65536) -> dict[str, Any]:
    """Read an exact identity or unambiguous native ID, optionally linked cards."""
    _limits(max_records, max_bytes)
    if not isinstance(identifier, str) or not 1 <= len(identifier) <= 2000:
        raise ValueError("identifier must contain 1 to 2000 characters")
    if type(depth) is not int or not 0 <= depth <= 5:
        raise ValueError("depth must be an integer from 0 to 5")
    if any(value not in EXPANSION_RELATIONS for value in expand):
        raise ValueError("unknown expansion relation")
    root = Path(root)
    connection, metadata = _connect(root)
    try:
        result = _envelope("read", metadata, max_records, max_bytes)
        result.update({"requestedIdentifier": identifier, "expansion": {"relations": list(expand), "depth": depth},
                       "missingLinks": [], "omittedMissingLinks": 0, "unvisitedLinks": 0})
        filters, params = ["(id=? OR native=?)"], [identifier, identifier]
        for column, value in (("collection_id", collection_id), ("version", version)):
            if value is not None:
                filters.append(column + "=?")
                params.append(str(value))
        where = " AND ".join(filters)
        count = connection.execute("SELECT count(*) FROM cards WHERE " + where, params).fetchone()[0]
        rows = connection.execute("SELECT * FROM cards WHERE " + where + " ORDER BY id LIMIT ?",
                                  [*params, max_records]).fetchall()
        if count != 1:
            result["status"] = "not-found" if count == 0 else "ambiguous-identifier"
            result["counts"].update({"matchingCandidates": count, "omittedCandidates": count - len(rows)})
            result["results"] = [_summary(_load(root, row)[0]) for row in rows]
            result["counts"]["returned"] = len(rows)
            if count > len(rows):
                result["truncated"] = True
                result["omissions"].append("record-limit")
            return _finish(result, max_bytes)
        queue = deque([(rows[0], 0)])
        seen = {rows[0]["id"]}
        while queue:
            row, level = queue.popleft()
            card, body = _load(root, row)
            result["results"].append({"card": card, "body": body, "depth": level})
            result["counts"]["returned"] = len(result["results"])
            if _measure(result) > max_bytes:
                result["results"].pop()
                result["counts"]["returned"] -= 1
                result["truncated"] = True
                result["omissions"].append("byte-limit")
                result["unvisitedLinks"] += 1 + len(queue)
                break
            if not expand:
                continue
            clauses, link_params = [], [row["id"]]
            for relation in expand:
                if relation == "related":
                    clauses.append("relation NOT IN ('parent','codeList')")
                elif relation != "children":
                    clauses.append("relation=?")
                    link_params.append(relation)
            targets = []
            if clauses:
                targets.extend(item[0] for item in connection.execute(
                    "SELECT target FROM links WHERE source=? AND (" + " OR ".join(clauses) + ") ORDER BY target",
                    link_params))
            if "children" in expand:
                # Only the bounded prefix is materialised even for large code lists.
                child_count = connection.execute("SELECT count(*) FROM cards WHERE parent_id=?", (row["id"],)).fetchone()[0]
                children = connection.execute("SELECT id FROM cards WHERE parent_id=? ORDER BY id LIMIT ?",
                                              (row["id"], max_records + 1)).fetchall()
                targets.extend(item[0] for item in children)
                if child_count > len(children):
                    result["unvisitedLinks"] += child_count - len(children)
            for target in dict.fromkeys(targets):
                if target in seen:
                    continue
                seen.add(target)
                if level >= depth:
                    result["unvisitedLinks"] += 1
                    if "depth-limit" not in result["omissions"]:
                        result["omissions"].append("depth-limit")
                    continue
                if len(result["results"]) + len(queue) >= max_records:
                    result["unvisitedLinks"] += 1
                    if "record-limit" not in result["omissions"]:
                        result["omissions"].append("record-limit")
                    continue
                linked = connection.execute("SELECT * FROM cards WHERE id=?", (target,)).fetchone()
                if linked is None:
                    if len(result["missingLinks"]) < max_records:
                        result["missingLinks"].append({"from": row["id"], "to": target})
                    else:
                        result["omittedMissingLinks"] += 1
                        if "missing-link-limit" not in result["omissions"]:
                            result["omissions"].append("missing-link-limit")
                else:
                    queue.append((linked, level + 1))
        result["truncated"] = bool(result["omissions"] or result["unvisitedLinks"])
        return _finish(result, max_bytes)
    finally:
        connection.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Generated semantic card directory")
    parser.add_argument("--max-records", type=int, default=10)
    parser.add_argument("--max-bytes", type=int, default=65536)
    parser.add_argument("--collection-id")
    parser.add_argument("--version")
    sub = parser.add_subparsers(dest="command", required=True)
    search_parser = sub.add_parser("search")
    search_parser.add_argument("question")
    search_parser.add_argument("--kind")
    read_parser = sub.add_parser("read")
    read_parser.add_argument("identifier")
    read_parser.add_argument("--expand", action="append", choices=EXPANSION_RELATIONS, default=[])
    read_parser.add_argument("--depth", type=int, default=1)
    sub.add_parser("index")
    args = parser.parse_args(argv)
    try:
        if args.command == "index":
            result = build_index(args.root)
        else:
            kwargs = {"max_records": args.max_records, "max_bytes": args.max_bytes,
                      "collection_id": args.collection_id, "version": args.version}
            result = search(args.root, args.question, kind=args.kind, **kwargs) if args.command == "search" else read_item(
                args.root, args.identifier, expand=tuple(args.expand), depth=args.depth, **kwargs)
        sys.stdout.buffer.write(render(result))
        return 0
    except (ValueError, OSError, sqlite3.Error, UnicodeError, KeyError, TypeError):
        print("Semantic query failed: invalid input, unavailable index or card integrity failure.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
