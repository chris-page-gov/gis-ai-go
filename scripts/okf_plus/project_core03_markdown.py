#!/usr/bin/env python3
"""Create and verify a separate Core 0.3 Markdown projection from retained sources."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile

import build
import model

ROOT = Path(__file__).resolve().parents[2]
MARKER = "gis-ai-go-okf-plus-core03-markdown.v1\n"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def project_record_text(source_text: str) -> tuple[str, dict | None]:
    """Change only generation metadata in one source Markdown file."""
    if not source_text.startswith("---\n"):
        return source_text, None
    parts = source_text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError("Unterminated Markdown front matter")
    row = model.load_json(parts[0][4:])
    if not isinstance(row, dict) or not isinstance(row.get("type"), str) or not row["type"].strip():
        return source_text, row if isinstance(row, dict) else None
    projected = build.migrate_generated(row.copy())
    body = parts[1]
    rendered = "---\n" + json.dumps(projected, ensure_ascii=False, indent=2, allow_nan=False)
    return rendered + "\n---\n" + body, projected


def _bundle_binding(bundle: Path) -> dict:
    descriptor = model.load_json((bundle / "okf.json").read_text(encoding="utf-8"))
    coverage = model.load_json((bundle / "coverage.json").read_text(encoding="utf-8"))
    lock = model.load_json((bundle / "source-lock.json").read_text(encoding="utf-8"))
    if descriptor.get("okf_version") != "0.3":
        raise ValueError("Generated Explorer descriptor does not declare Core 0.3")
    if coverage.get("recordCount") != 30876:
        raise ValueError("Unexpected retained record denominator")
    if lock.get("sha256") != coverage.get("inputDigest"):
        raise ValueError("Bundle source lock and coverage digest differ")
    with (bundle / "okf-bundle.json").open("rb") as handle:
        prefix = handle.read(16384).decode("utf-8")
    for field in ("okf_version", "okfVersion"):
        if not re.search(rf'"{field}"\s*:\s*"0\.3"', prefix):
            raise ValueError(f"Generated large bundle omits {field} Core 0.3 declaration")
    if not re.search(rf'"revision"\s*:\s*"{re.escape(coverage["revision"])}"', prefix):
        raise ValueError("Generated bundle revision differs from coverage")
    checksums = model.load_json((bundle / "checksums.json").read_text(encoding="utf-8"))
    for name, digest in checksums.items():
        if sha((bundle / name).read_bytes()) != digest:
            raise ValueError(f"Generated bundle checksum mismatch: {name}")
    for name in descriptor["entrypoints"].values():
        if name not in checksums or not (bundle / name).is_file():
            raise ValueError(f"Generated descriptor entrypoint is absent: {name}")
    return {"revision": coverage["revision"], "inputDigest": coverage["inputDigest"],
            "recordCount": coverage["recordCount"], "descriptor": descriptor}


def _write_markdown(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def project(root: Path, bundle: Path, output: Path) -> dict:
    root = root.resolve()
    bundle = bundle.resolve()
    output = output.absolute()
    if not output.parent.is_dir() or output.is_symlink():
        raise ValueError("Projection output must have an existing parent and cannot be a symlink")
    if output.resolve().is_relative_to(root):
        raise ValueError("Projection output cannot be inside the source checkout")
    if output.exists() and (not (output / ".okf-plus-core03-generated").is_file()
                            or (output / ".okf-plus-core03-generated").read_text() != MARKER):
        raise ValueError("Refusing to replace an unmarked Markdown output")
    binding = _bundle_binding(bundle)
    with tempfile.TemporaryDirectory(prefix=".gis-core03-markdown-", dir=output.parent) as temporary:
        stage = Path(temporary) / "staged"
        stage.mkdir()
        (stage / ".okf-plus-core03-generated").write_text(MARKER, encoding="utf-8")
        record_check = build.schema_validator(root, "record.schema.json")
        source_inventory = hashlib.sha256()
        projected_inventory = hashlib.sha256()
        id_inventory = hashlib.sha256()
        actor_counts = Counter()
        source_bytes = projected_bytes = record_count = markdown_files = 0
        source_records = sorted((root / "okf-plus/records").rglob("*.md"))
        identities: set[str] = set()
        for source_path in source_records:
            relative = source_path.relative_to(root / "okf-plus")
            build.source_path(root, relative)
            source_raw = source_path.read_bytes()
            source_text = source_raw.decode("utf-8")
            projected_text, projected_row = project_record_text(source_text)
            target = stage / relative
            projected_raw = projected_text.encode("utf-8")
            if projected_row is not None and isinstance(projected_row.get("type"), str):
                source_row, source_body = model.read_markdown(source_path)
                # The front-matter transformation must preserve every other field and the body.
                source_graph = {key: value for key, value in source_row.items() if key != "generated"}
                projected_graph = {key: value for key, value in projected_row.items()
                                   if key not in ("generated", build.LEGACY_GENERATED_EXTENSION)}
                if source_graph != projected_graph:
                    raise ValueError(f"Non-generation metadata changed: {relative}")
                if source_body != projected_text.split("\n---\n", 1)[1]:
                    raise ValueError(f"Authored Markdown body changed: {relative}")
                record_check.validate(projected_row)
                identifier = projected_row["@id"]
                if identifier in identities:
                    raise ValueError(f"Duplicate projected identity: {identifier}")
                identities.add(identifier)
                id_inventory.update(identifier.encode("utf-8") + b"\0")
                record_count += 1
                generated = source_row.get("generated")
                if generated is not None:
                    actor = generated["by"]
                    if actor in build.LEGACY_AUTOMATED_GENERATORS:
                        actor_counts["canonicalised-automated"] += 1
                    elif actor in build.LEGACY_UNATTRIBUTED_GENERATORS:
                        actor_counts["preserved-unattributed"] += 1
                    else:
                        actor_counts["already-conformant"] += 1
                else:
                    actor_counts["no-generated-assertion"] += 1
            _write_markdown(target, projected_raw)
            markdown_files += 1
            source_bytes += len(source_raw)
            projected_bytes += len(projected_raw)
            source_inventory.update(relative.as_posix().encode() + b"\0" + bytes.fromhex(sha(source_raw)))
            projected_inventory.update(relative.as_posix().encode() + b"\0" + bytes.fromhex(sha(projected_raw)))

        # Create a distinct generated root. The source root remains Core 0.2.
        index = {
            "okf_version": "0.3", "@context": model.CONTEXT,
            "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/catalogue",
            "@type": ["dcat:Catalog"], "type": "Knowledge Bundle",
            "title": "OS, ONS and geospatial OKF+ Core 0.3 projection",
            "description": "A source-bound Core 0.3 projection of the retained geospatial metadata records.",
            "status": "draft",
            "generated": {"by": "process:gis-ai-go-okf-plus-core03-markdown-projection"},
            "sources": [
                {"resource": "https://github.com/chris-page-gov/gis-ai-go/blob/b064a93f0675f157a93a0a8845c3c0aa8396c307/okf-plus/index.md",
                 "title": "Retained Core 0.2 source root"},
                {"resource": "../bundle/okf.json", "title": "Generated Core 0.3 bundle descriptor"}
            ],
            "dcterms:conformsTo": {"@id": "https://github.com/open-knowledge-format/open-knowledge-format/blob/527e81aff55992be21507e97004286789126f88c/SPEC.md"}
        }
        index_raw = model.markdown_text(index, "\n# OS, ONS and geospatial OKF+ Core 0.3 projection\n\n"
            "This generated root is separate from the retained Core 0.2 source root. "
            "The complete bundle and its entrypoints are in [the sibling bundle directory](../bundle/okf.json).\n"
            "The source lock in that bundle binds the source files to the candidate revision. "
            "This local candidate does not establish deployment, registration or consumer acceptance.\n").encode("utf-8")
        _write_markdown(stage / "index.md", index_raw)
        _write_markdown(stage / "context.jsonld", (root / "okf-plus/context.jsonld").read_bytes())
        _write_markdown(stage / "schemas/record.schema.json",
                        (root / "okf-plus/schemas/record.schema.json").read_bytes())
        readme = ("# OS and ONS OKF+ Core 0.3 projection\n\n"
                  "This generated Markdown projection is separate from its retained Core 0.2 sources. "
                  "Record bodies, identities, source bindings and graph fields are preserved. "
                  "Only the documented `generated` actor mapping changes.\n\n"
                  "The matching machine bundle, descriptor and entrypoints are in "
                  "[the sibling bundle output](../bundle/okf.json). Its source lock binds the exact "
                  "producer inputs and revision. This candidate is local and does not establish "
                  "publication or consumer acceptance.\n")
        _write_markdown(stage / "README.md", readme.encode("utf-8"))
        if record_count != binding["recordCount"]:
            raise ValueError("Markdown projection and generated bundle record counts differ")
        manifest = {
            "schema": "gis-ai-go.okf-plus-core03-markdown-projection.v1",
            "sourceCoreVersion": "0.2", "projectionCoreVersion": "0.3",
            "sourceRevision": binding["revision"], "inputDigest": binding["inputDigest"],
            "recordCount": record_count, "markdownFileCount": markdown_files,
            "identityCount": len(identities), "identityInventorySha256": id_inventory.hexdigest(),
            "sourceInventorySha256": source_inventory.hexdigest(),
            "projectionInventorySha256": projected_inventory.hexdigest(),
            "sourceRecordBytes": source_bytes, "projectionRecordBytes": projected_bytes,
            "actorMigrationCounts": dict(sorted(actor_counts.items())),
            "limitations": ["Source snapshots remain in the pinned producer tree and are bound by the sibling bundle source lock.",
                            "Local projection only; no deployment, registration or consumer acceptance is claimed."]
        }
        manifest_raw = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
        _write_markdown(stage / "projection-manifest.json", manifest_raw)
        if output.exists():
            previous = Path(temporary) / "previous"
            output.rename(previous)
        try:
            stage.rename(output)
        except BaseException:
            if 'previous' in locals() and previous.exists():
                previous.rename(output)
            raise
        return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(project(args.root, args.bundle, args.output), indent=2))


if __name__ == "__main__":
    main()
