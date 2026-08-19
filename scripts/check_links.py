#!/usr/bin/env python3
"""Check local Markdown links, research checksums and source identifiers."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs" / "research" / "2026-08-19"
PACK = RESEARCH / "research-pack"
VENDORED_OKF = ROOT / "okf" / "vendor"
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
SOURCE_ID = re.compile(r"^S-[A-Z0-9-]+$")
SKIP_PARTS = {".git", ".venv", "node_modules", "artifacts", "dist"}


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def walk_strings(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)


def check_markdown_links() -> tuple[int, list[str]]:
    checked = 0
    failures: list[str] = []
    for path in ROOT.rglob("*.md"):
        # Exact vendored Markdown may contain upstream-relative links to files outside
        # the selected input set. Its bytes and complete local inventory are enforced
        # by the OKF source lock instead of rewriting those links.
        if SKIP_PARTS.intersection(path.parts) or path.is_relative_to(VENDORED_OKF):
            continue
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).strip().strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            checked += 1
            candidate = (path.parent / target).resolve()
            if not candidate.is_relative_to(ROOT.resolve()):
                failures.append(f"{path.relative_to(ROOT)}: link escapes repository: {target}")
            elif not candidate.exists():
                failures.append(f"{path.relative_to(ROOT)}: missing target: {target}")
    return checked, failures


def check_pack_hashes() -> int:
    expected_zip = "08ecb65f18f8bef8af0d79dd3c9974da5939544fdecd899e62532c3089798e34"
    zip_path = RESEARCH / "governed-geospatial-research-pack.zip"
    actual_zip = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    if actual_zip != expected_zip:
        raise AssertionError(f"research ZIP hash mismatch: {actual_zip}")

    expected_files: set[str] = set()
    for line in (PACK / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        if relative in expected_files:
            raise AssertionError(f"duplicate research checksum path: {relative}")
        target = (PACK / relative).resolve()
        if not target.is_relative_to(PACK.resolve()):
            raise AssertionError(f"research checksum path escapes pack: {relative}")
        expected_files.add(relative)
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != digest:
            raise AssertionError(f"research checksum mismatch: {relative}")

    actual_files = {
        path.relative_to(PACK).as_posix()
        for path in PACK.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS.txt"
    }
    if expected_files != actual_files:
        missing = sorted(expected_files - actual_files)
        extra = sorted(actual_files - expected_files)
        raise AssertionError(f"research inventory mismatch; missing={missing}, extra={extra}")
    if any(path.is_symlink() for path in PACK.rglob("*")):
        raise AssertionError("research pack contains a symbolic link")
    return len(expected_files)


def check_ledger_snapshots() -> int:
    for filename in ("sources.json", "repositories.json"):
        live = ROOT / "docs" / "source-ledger" / filename
        research = PACK / "data" / filename
        if live.read_bytes() != research.read_bytes():
            raise AssertionError(f"source-ledger snapshot differs from research: {filename}")
    return 2


def check_source_ids() -> int:
    ledger = load_json(ROOT / "docs" / "source-ledger" / "sources.json")
    known = {source["id"] for source in ledger["sources"]}
    referenced: set[str] = set()
    for path in (PACK / "data").glob("*.json"):
        for value in walk_strings(load_json(path)):
            if SOURCE_ID.fullmatch(value):
                referenced.add(value)
    missing = sorted(referenced - known)
    if missing:
        raise AssertionError(f"unresolved research source identifiers: {missing}")
    return len(referenced)


def main() -> None:
    link_count, failures = check_markdown_links()
    if failures:
        raise AssertionError("\n".join(failures))
    checksum_count = check_pack_hashes()
    snapshot_count = check_ledger_snapshots()
    source_count = check_source_ids()
    print(
        f"Checked {link_count} local Markdown links, {checksum_count} research hashes "
        f"and {snapshot_count} ledger snapshots; resolved {source_count} source identifiers."
    )


if __name__ == "__main__":
    main()
