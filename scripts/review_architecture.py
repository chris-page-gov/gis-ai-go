#!/usr/bin/env python3
"""Reproduce the architecture review inventory and check immutable Git line links.

This is a source/documentation check. It does not infer runtime reachability from
text matches, certify provider data, or replace the repository's assurance lanes.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote, unquote


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "docs" / "architecture"
BASELINE = "97bc45635a91064cd78f06bf0848ad7636f05439"
GIT_URL = "https://github.com/chris-page-gov/gis-ai-go/blob/"
CODE_SUFFIXES = {".py", ".ts", ".mjs", ".js", ".cjs", ".sh", ".tsx", ".jsx", ".css", ".html", ".sql"}
EXCLUDED_PREFIXES = ("docs/research/", "okf/vendor/", "okf-plus/records/")
SOURCE_LINK = re.compile(
    re.escape(GIT_URL) + r"([^/\s)]+)/(.*?)(?:#L(\d+)(?:-L(\d+))?)(?=[\s)\]>\"`]|$)"
)


def git(*arguments: str) -> bytes:
    return subprocess.check_output(["git", *arguments], cwd=ROOT)


def tracked_tree() -> dict[str, str]:
    tree: dict[str, str] = {}
    for entry in git("ls-tree", "-rz", BASELINE).split(b"\0"):
        if not entry:
            continue
        metadata, path = entry.split(b"\t", 1)
        _mode, kind, object_id = metadata.split()
        if kind == b"blob":
            tree[path.decode()] = object_id.decode()
    return tree


def read_blobs(object_ids: list[str]) -> dict[str, bytes]:
    """Read the immutable objects in one Git invocation, including binary files."""
    unique = sorted(set(object_ids))
    output = subprocess.check_output(
        ["git", "cat-file", "--batch"],
        input="".join(f"{item}\n" for item in unique).encode(), cwd=ROOT,
    )
    position = 0
    result: dict[str, bytes] = {}
    for object_id in unique:
        end = output.index(b"\n", position)
        actual_id, kind, size = output[position:end].split()
        if actual_id.decode() != object_id or kind != b"blob":
            raise ValueError(f"Unexpected Git object response for {object_id}")
        position = end + 1
        result[object_id] = output[position:position + int(size)]
        position += int(size) + 1
    return result


def is_maintained_code(path: str) -> bool:
    if path.startswith(EXCLUDED_PREFIXES):
        return False
    return (
        Path(path).suffix in CODE_SUFFIXES
        or path in {"scripts/start-local-candidate", "scripts/start-public-data-workbench"}
        or Path(path).name == "Containerfile"
        or path.startswith(".github/workflows/")
    )


def review_area(path: str) -> str:
    if path.startswith("okf-plus/vendor/"):
        return "Experimental and knowledge"
    if path.startswith(("apps/public-", "apps/webmcp-", "packages/experience-intake/")):
        return "User interfaces and intake"
    if path.startswith(("packages/", "services/")):
        return "Core packages and execution"
    if path.startswith("apps/mcp-gateway/"):
        return "Experimental and knowledge" if any(
            word in Path(path).name for word in ("sites-pilot", "web216")
        ) else "Core gateway"
    if path.startswith(("sites/", "scripts/okf_plus/")) or (
        path.startswith("scripts/") and any(word in Path(path).name for word in ("experience", "sites"))
    ):
        return "Experimental and knowledge"
    return "Build and operations"


def role(path: str) -> str:
    if path.startswith("okf-plus/vendor/"):
        return "pinned vendored dependency"
    if Path(path).suffix == ".sql":
        return "database migration and constraints"
    if path.startswith("tests/") or "/test/" in path or "/tests/" in path:
        return "test or test fixture"
    if path.startswith(("scripts/", ".github/")) or "/scripts/" in path:
        return "build, operator or assurance tooling"
    if Path(path).suffix in {".css", ".html"}:
        return "presentation"
    if Path(path).name.endswith("config.ts") or Path(path).name == "Containerfile":
        return "configuration"
    return "application or library"


def inventory(tree: dict[str, str]) -> dict:
    paths = sorted(path for path in tree if is_maintained_code(path))
    blobs = read_blobs([tree[path] for path in paths])
    rows = []
    for path in paths:
        body = blobs[tree[path]]
        rows.append({
            "path": path, "git_blob": tree[path], "lines": len(body.splitlines()),
            "bytes": len(body), "review_area": review_area(path), "role": role(path),
            "authorship": "vendored" if path.startswith("okf-plus/vendor/") else "project",
            "source": f"{GIT_URL}{BASELINE}/{quote(path, safe='/')}#L1-L{max(1, len(body.splitlines()))}",
        })
    return {
        "baseline": BASELINE,
        "scope": "All tracked paths inventoried; authored code, migrations and CI plus separately labelled pinned vendor code listed individually. Review depth is documented in REVIEW.md and the component chapters.",
        "tracked_files": len(tree),
        "top_level_counts": dict(sorted(Counter(path.split('/')[0] for path in tree).items())),
        "source_files": len(rows),
        "source_lines": sum(row["lines"] for row in rows),
        "authored_files": sum(row["authorship"] == "project" for row in rows),
        "vendor_files": sum(row["authorship"] == "vendored" for row in rows),
        "authored_lines": sum(row["lines"] for row in rows if row["authorship"] == "project"),
        "vendor_lines": sum(row["lines"] for row in rows if row["authorship"] == "vendored"),
        "files": rows,
    }


def markdown_inventory(data: dict) -> str:
    lines = [
        "# Source coverage register", "",
        f"Immutable review baseline: `{BASELINE}`.", "",
        f"The tree contains **{data['tracked_files']:,} tracked files**. The register below identifies "
        f"**{data['source_files']:,} code, presentation, migration, launcher and CI files** "
        f"(**{data['source_lines']:,} lines**): **{data['authored_files']:,} project-authored files** "
        f"and **{data['vendor_files']:,} pinned vendor files**. Vendor code is a dependency boundary, "
        "not a local refactoring target.",
        "",
        "Every listed file received inventory and structural/reference coverage. Component chapters "
        "describe the implementation and boundary traces; [the review](REVIEW.md) records depth and "
        "limitations. A row is not a claim that every line received a manual semantic audit. "
        "Generated/imported knowledge records, immutable research and third-party material remain "
        "data/evidence: their inventory does not establish semantic completeness.",
        "",
        "The inventory is derived from Git objects, so later inline comments cannot shift these references. "
        "Counts describe the baseline, not documentation added by this review. "
        "Reproduce with `python3 scripts/review_architecture.py --write`; "
        "check with `python3 scripts/review_architecture.py --check`.",
        "", "## Complete top-level inventory", "",
        "| Tree or root file | Tracked files |", "| --- | ---: |",
    ]
    lines += [f"| `{name}` | {count:,} |" for name, count in data["top_level_counts"].items()]
    for area in sorted({row["review_area"] for row in data["files"]}):
        lines += ["", f"## {area}", "", "| Source at review baseline | Lines | Role |", "| --- | ---: | --- |"]
        lines += [f"| [{row['path']}]({row['source']}) | {row['lines']:,} | {row['role']} |"
                  for row in data["files"] if row["review_area"] == area]
    return "\n".join(lines) + "\n"


def check_source_links(tree: dict[str, str]) -> int:
    matches = []
    for document in sorted(DESTINATION.glob("*.md")):
        for match in SOURCE_LINK.finditer(document.read_text()):
            revision, path, start, end = match.groups()
            path = unquote(path)
            if revision != BASELINE or path not in tree:
                raise ValueError(f"{document.name}: reference outside review baseline: {match.group()}")
            matches.append((document.name, path, int(start), int(end or start)))
    blobs = read_blobs([tree[path] for _, path, _, _ in matches])
    for name, path, start, end in matches:
        count = len(blobs[tree[path]].splitlines())
        if not 1 <= start <= end <= count:
            raise ValueError(f"{name}: invalid line range {path}#L{start}-L{end}; file has {count} lines")
    return len(matches)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    tree = tracked_tree()
    data = inventory(tree)
    outputs = {
        "source-inventory.json": json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        "SOURCE_REGISTER.md": markdown_inventory(data),
    }
    if args.write:
        DESTINATION.mkdir(parents=True, exist_ok=True)
        for name, content in outputs.items():
            (DESTINATION / name).write_text(content)
        print(f"Wrote inventory: {data['source_files']} source files ({data['authored_files']} authored, {data['vendor_files']} vendored); {data['tracked_files']} total tracked files.")
    else:
        for name, content in outputs.items():
            if (DESTINATION / name).read_text() != content:
                raise ValueError(f"{name} differs from the immutable baseline inventory")
        checked = check_source_links(tree)
        print(f"Verified complete inventory and {checked} immutable Git line references.")


if __name__ == "__main__":
    main()
