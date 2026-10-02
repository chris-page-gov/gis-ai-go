#!/usr/bin/env python3
"""Freeze verified source locators before offline import or publication.

Only this explicit acquisition stage reads private response bytes. A missing or
unmatched response fails closed, preserving the previous frozen locator index.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from import_sources import original_locators
from model import canonical, load_json

ROOT = Path(__file__).resolve().parents[2]


def freeze(root: Path):
    families = {}
    for path in sorted((root / "okf-plus/source").glob("*.json")):
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("Source snapshot escapes the checkout")
        snapshot = load_json(path.read_text())
        if snapshot.get("schema") != "okf-plus-source-snapshot.v1":
            continue
        family = snapshot["family"]
        if family in families:
            raise ValueError("Duplicate source family")
        families[family] = {
            native: {"url": receipt["url"], "retrievedAt": receipt["retrievedAt"],
                     "sha256": receipt["sha256"], "pointer": pointer,
                     "status": "exact-native-id-match" if pointer is not None else "catalogue-document"}
            for native, (receipt, pointer) in original_locators(root, snapshot).items()
        }
    if not families:
        raise ValueError("No source snapshots to freeze")
    document = {
        "schema": "gis-ai-go.okf-plus-source-locators.v1",
        "generationRule": "Verified captured bytes and native JSON pointers, explicit document evidence or reviewed document-parser identity. No unrelated receipt fallback. Browser observations and failed requests retain separate evidence kinds. Offline import does not require private captures.",
        "families": families,
    }
    destination = root / "okf-plus/source/locator-index.json"
    if destination.is_symlink():
        raise ValueError("Locator output cannot be a symbolic link")
    temporary = destination.with_suffix(".json.tmp")
    if temporary.exists():
        raise ValueError("Pending locator output already exists")
    try:
        temporary.write_bytes(canonical(document))
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    return document


def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()
    document = freeze(ROOT)
    print("Persisted verified source locators", sum(map(len, document["families"].values())))


if __name__ == "__main__":
    main()
