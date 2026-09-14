#!/usr/bin/env python3
"""Import a pinned, metadata-only OKF-ONS experiment corpus without network access.

Source code is never imported or executed. The committed derivative manifest is
the offline trust anchor, not a signature or permission to retrieve observations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any


SOURCE_COMMIT = "4aa41c71dd570ceccb661768af95c4d69f49162b"
SNAPSHOT = "metadata-enrichment-2026-07-21-r6"
TRANSFORMATION_VERSION = "web216-exact-source-subset.v1"
SCHEMA_VERSION = "web216.offline-corpus.v1"
MANIFEST_SCHEMA = "web216.source-manifest.v1"
MANIFEST_PATH = Path(__file__).resolve().parents[1] / "tests/fixtures/web216/source-manifest.json"
MAX_CORPUS_BYTES = 5_000_000
SOURCES = {
    "ons-data-api": {
        "path": f"source/{SNAPSHOT}/ons-data-api.json",
        "blob_sha256": "68ac8e0f59c47d0eba6fadaf172721f0190daa0e390487e181f039ceb9deeb9a",
        "blob_bytes": 1_180_917,
        "record_count": 337,
    },
    "nomis-dataset-definitions": {
        "path": f"source/{SNAPSHOT}/nomis-dataset-definitions.json",
        "blob_sha256": "ef7968bce990d1031ff12b4b0ce9168e08d6052e2073a8fcb1742e4e516c9ce1",
        "blob_bytes": 14_658_828,
        "record_count": 1617,
    },
}
STORY_IDS = frozenset({
    "ons-data-api:cpih01", "ons-data-api:TS001", "ons-data-api:TS017",
    "ons-data-api:TS052", "ons-data-api:TS053",
    "nomis-dataset-definitions:NM_2002_1", "nomis-dataset-definitions:NM_2006_1",
})
RIGHTS = {
    "basis_checked_on": "2026-09-14",
    "basis_check_scope": "General ONS/Nomis terms pages checked 14 September 2026; "
    "not a record-specific legal audit.",
    "attribution": "Contains public metadata attributed to the Office for National Statistics "
    "and Nomis. Source attribution does not imply endorsement.",
    "general_terms_urls": [
        "https://www.ons.gov.uk/help/terms-conditions",
        "https://www.nomisweb.co.uk/home/copyright.asp",
        "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
    ],
    "licence_basis": "General ONS/Nomis Open Government Licence metadata basis; preserve "
    "source-specific qualifications. A missing record-level licence remains missing.",
    "limitations": "Metadata only; no blanket source-data licence, observation retrieval "
    "authority, ELS rights assessment or OS product licence is asserted.",
}


def canonical(value: Any) -> bytes:
    """Stable UTF-8 JSON, without a trailing newline or non-finite numbers."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def _source_digest(value: Any) -> str:
    # The upstream acquisition contract escapes non-ASCII characters; the new
    # derivative contract above intentionally uses literal UTF-8 instead.
    encoded = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"),
                         allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def identity(record: dict[str, Any]) -> str:
    """Preserve the acquisition source ID, without adding a dataset namespace."""
    if not isinstance(record, dict) or record.get("sourceId") not in SOURCES:
        raise ValueError("Unsupported metadata source identity")
    native = record.get("sourceRecordId")
    if not isinstance(native, str) or not re.fullmatch(r"[A-Za-z0-9._-]{1,200}", native):
        raise ValueError("Invalid source-native record identity")
    return f"{record['sourceId']}:{native}"


def _json(data: bytes) -> Any:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in rows:
            if key in result:
                raise ValueError("Duplicate JSON object key")
            result[key] = value
        return result

    def constant(_: str) -> Any:
        raise ValueError("Non-finite JSON number")

    return json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)


def _read(path: Path) -> Any:
    with path.open("rb") as stream:
        data = stream.read(MAX_CORPUS_BYTES + 1)
    if len(data) > MAX_CORPUS_BYTES:
        raise ValueError("Corpus or manifest exceeds the byte limit")
    return _json(data)


def _git_blob(source_repo: Path, source: dict[str, Any]) -> bytes:
    # Disable replacement objects, text conversion, external diffs and promisor
    # lazy fetching. Reading a dirty checkout never reads its working-tree files.
    environment = dict(os.environ, GIT_NO_LAZY_FETCH="1", GIT_TERMINAL_PROMPT="0")
    result = subprocess.run(
        ["git", "--no-pager", "--no-replace-objects", "-C", str(source_repo), "show",
         "--no-ext-diff", "--no-textconv", f"{SOURCE_COMMIT}:{source['path']}"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30,
        env=environment,
    )
    data = result.stdout
    if len(data) != source["blob_bytes"] or hashlib.sha256(data).hexdigest() != source["blob_sha256"]:
        raise ValueError("Pinned source blob length or SHA-256 mismatch")
    return data


def _source_projection(source_id: str, envelope: dict[str, Any]) -> dict[str, Any]:
    source = SOURCES[source_id]
    provenance = envelope.get("provenance", {})
    records = envelope.get("records")
    if (envelope.get("schemaVersion") != "okf-ons.source-acquisition.v1"
            or not isinstance(provenance, dict) or not isinstance(records, list)
            or provenance.get("source", {}).get("id") != source_id
            or len(records) != source["record_count"]
            or provenance.get("recordCount") != len(records)
            or provenance.get("recordSetSha256") != _source_digest(records)):
        raise ValueError("Pinned acquisition envelope or record-set binding is invalid")
    assurance = provenance.get("assurance", {})
    if assurance.get("metadataOnly") is not True or assurance.get("observationsFetched") is not False:
        raise ValueError("Acquisition is not explicitly metadata-only")
    pages = provenance.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError("Source-envelope page provenance is missing")
    receipt_bindings = []
    for page in pages:
        if (not isinstance(page, dict) or not isinstance(page.get("requestUrl"), str)
                or not isinstance(page.get("contentSha256"), str)):
            raise ValueError("Malformed upstream acquisition receipt")
        receipt_bindings.append({"requestUrl": page["requestUrl"],
                                 "contentSha256": page["contentSha256"]})
    if provenance.get("snapshotSetSha256") != _source_digest(receipt_bindings):
        raise ValueError("Source-envelope receipt-set binding mismatch")
    seen: set[str] = set()
    for record in records:
        key = identity(record)
        if key in seen or record["sourceId"] != source_id:
            raise ValueError("Duplicate or cross-source record in acquisition")
        seen.add(key)
    return {
        "source_id": source_id,
        **source,
        "record_set_sha256": provenance["recordSetSha256"],
        "source_description": provenance["source"],
        "page_provenance": {
            "scope": "upstream-source-envelope; not a per-record acquisition receipt",
            "receipt_count": len(pages),
            "receipts_sha256": digest(pages),
            "snapshot_set_sha256": provenance["snapshotSetSha256"],
            "receipt_objects_copied": 0,
            "note": "The full pinned source blob retains the original receipts. This "
            "subset does not invent a page-to-record binding or copy unrelated receipts.",
        },
    }


def _assemble(sources: list[dict[str, Any]], records: list[dict[str, Any]], scope: str) -> dict[str, Any]:
    if scope not in {"story", "comparison"}:
        raise ValueError("Scope must be story or comparison")
    selected = [record for record in records if scope == "comparison" or identity(record) in STORY_IDS]
    selected.sort(key=identity)
    keys = [identity(record) for record in selected]
    expected_count = 7 if scope == "story" else 339
    if len(keys) != expected_count or len(set(keys)) != len(keys) or not STORY_IDS.issubset(keys):
        raise ValueError("The pinned scope has missing or duplicate records")
    body = {
        "schema_version": SCHEMA_VERSION,
        "transformation_version": TRANSFORMATION_VERSION,
        "source_commit": SOURCE_COMMIT,
        "source_snapshot": SNAPSHOT,
        "scope": scope,
        "scope_statement": "Seven explicitly selected story records" if scope == "story" else
        "All 337 dataset-level ONS Data API records and two fixed Nomis supplements; "
        "not the complete ONS/Nomis or four-lane upstream catalogue",
        "metadata_only": True,
        "observations_included": False,
        "upstream_snapshot_completeness_claimed": False,
        "rights": RIGHTS,
        "sources": sources,
        "records": selected,
    }
    return {**body, "corpus_sha256": digest(body)}


def import_pinned(source_repo: Path, scope: str) -> dict[str, Any]:
    """Read only two immutable Git blobs; no source execution or provider access."""
    if scope not in {"story", "comparison"}:
        raise ValueError("Scope must be story or comparison")
    records: list[dict[str, Any]] = []
    sources = []
    for source_id, source in sorted(SOURCES.items()):
        envelope = _json(_git_blob(source_repo, source))
        sources.append(_source_projection(source_id, envelope))
        records.extend(record for record in envelope["records"]
                       if source_id == "ons-data-api" or identity(record) in STORY_IDS)
    return _assemble(sources, records, scope)


def _manifest(comparison: dict[str, Any]) -> dict[str, Any]:
    story = _assemble(comparison["sources"], comparison["records"], "story")
    body = {
        "schema_version": MANIFEST_SCHEMA,
        "transformation_version": TRANSFORMATION_VERSION,
        "source_commit": SOURCE_COMMIT,
        "source_snapshot": SNAPSHOT,
        "sources": comparison["sources"],
        "rights": RIGHTS,
        "record_sha256": {identity(record): digest(record) for record in comparison["records"]},
        "scopes": {
            scope: {"record_ids": [identity(record) for record in corpus["records"]],
                    "corpus_sha256": corpus["corpus_sha256"]}
            for scope, corpus in (("story", story), ("comparison", comparison))
        },
        "trust_boundary": "A committed derivative manifest is the offline integrity anchor. "
        "Hashes do not authenticate a publisher, establish statistical accuracy or authorise execution.",
    }
    return {**body, "manifest_sha256": digest(body)}


def load_corpus(path: Path) -> list[dict[str, Any]]:
    """Validate a derivative against its wrapper and the committed source manifest."""
    manifest = _read(MANIFEST_PATH)
    corpus = _read(Path(path))
    if not isinstance(manifest, dict) or not isinstance(corpus, dict):
        raise ValueError("Corpus and manifest must be objects")
    for item, field in ((manifest, "manifest_sha256"), (corpus, "corpus_sha256")):
        body = {key: value for key, value in item.items() if key != field}
        if item.get(field) != digest(body):
            raise ValueError(f"Invalid {field} binding")
    if (manifest.get("schema_version") != MANIFEST_SCHEMA
            or corpus.get("schema_version") != SCHEMA_VERSION
            or any(item.get("source_commit") != SOURCE_COMMIT
                   or item.get("source_snapshot") != SNAPSHOT
                   or item.get("transformation_version") != TRANSFORMATION_VERSION
                   for item in (manifest, corpus))):
        raise ValueError("Unsupported corpus or manifest version")
    scope = corpus.get("scope")
    if scope not in {"story", "comparison"}:
        raise ValueError("Invalid corpus scope")
    sources = corpus.get("sources")
    if sources != manifest.get("sources") or not isinstance(sources, list) or len(sources) != 2:
        raise ValueError("Source manifest binding mismatch")
    for source in sources:
        pin = SOURCES.get(source.get("source_id"))
        if pin is None or any(source.get(key) != value for key, value in pin.items()):
            raise ValueError("Unpinned source metadata")
    if (corpus.get("metadata_only") is not True or corpus.get("observations_included") is not False
            or corpus.get("upstream_snapshot_completeness_claimed") is not False
            or corpus.get("rights") != RIGHTS or manifest.get("rights") != RIGHTS):
        raise ValueError("Corpus boundary or rights metadata changed")
    records = corpus.get("records")
    if not isinstance(records, list):
        raise ValueError("Corpus records must be an array")
    keys = [identity(record) for record in records]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate corpus record identity")
    scope_manifest = manifest.get("scopes", {}).get(scope, {})
    if keys != scope_manifest.get("record_ids") or len(keys) != (7 if scope == "story" else 339):
        raise ValueError("Corpus identity set or order differs from its pinned scope")
    for record in records:
        if digest(record) != manifest.get("record_sha256", {}).get(identity(record)):
            raise ValueError("Exact source record SHA-256 mismatch")
    if corpus["corpus_sha256"] != scope_manifest.get("corpus_sha256"):
        raise ValueError("Corpus differs from the committed derivative manifest")
    return records


def _write(path: Path, value: dict[str, Any], replace: bool) -> None:
    data = canonical(value) + b"\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as stream:
            stream.write(data)
    except FileExistsError:
        if not replace or path.read_bytes() != data:
            raise ValueError("Output exists; --replace permits only byte-identical regeneration") from None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--scope", choices=("story", "comparison"), default="story")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path,
                        help="Also generate the pinned 339-record digest manifest")
    parser.add_argument("--replace", action="store_true",
                        help="Accept an existing output only if already byte-identical")
    args = parser.parse_args()
    try:
        for path in (args.output, args.manifest_output):
            if path is not None and path.resolve().is_relative_to(args.source_repo.resolve()):
                raise ValueError("Outputs must be outside the read-only source repository")
        comparison = import_pinned(args.source_repo, "comparison")
        corpus = _assemble(comparison["sources"], comparison["records"], args.scope)
        _write(args.output, corpus, args.replace)
        if args.manifest_output is not None:
            _write(args.manifest_output, _manifest(comparison), args.replace)
        print(f"Imported {len(corpus['records'])} metadata records; no network or source execution")
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        parser.exit(1, f"Import failed: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
