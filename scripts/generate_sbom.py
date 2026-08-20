#!/usr/bin/env python3
"""Generate a deterministic CycloneDX 1.6 manifest from installed and locked packages."""

from __future__ import annotations

import argparse
import json
import subprocess
import tomllib
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]


def npm_workspace_versions(root: Path) -> dict[str, str]:
    """Return canonical versions for the root and every pnpm workspace package."""
    manifests = [root / "package.json"]
    manifests.extend(sorted((root / "apps").glob("*/package.json")))
    manifests.extend(sorted((root / "packages").glob("*/package.json")))

    versions: dict[str, str] = {}
    for manifest in manifests:
        package = json.loads(manifest.read_text(encoding="utf-8"))
        name = package.get("name")
        version = package.get("version")
        if not isinstance(name, str) or not isinstance(version, str):
            raise AssertionError(f"Workspace manifest lacks a package name or version: {manifest}")
        if name in versions:
            raise AssertionError(f"Duplicate workspace package name: {name}")
        versions[name] = version
    return versions


def npm_components() -> Iterator[dict[str, str]]:
    result = subprocess.run(
        ["pnpm", "list", "--recursive", "--depth", "Infinity", "--json"],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    projects = json.loads(result.stdout)
    workspace_versions = npm_workspace_versions(ROOT)

    def visit(dependencies: dict[str, Any]) -> Iterator[dict[str, str]]:
        for name, detail in dependencies.items():
            version = detail.get("version")
            if version:
                if version.startswith("link:"):
                    version = workspace_versions.get(name)
                    if version is None:
                        raise AssertionError(
                            f"Workspace link has no matching checked-in package manifest: {name}"
                        )
                encoded = quote(name, safe="/")
                yield {
                    "type": "library",
                    "name": name,
                    "version": version,
                    "purl": f"pkg:npm/{encoded}@{version}",
                }
            yield from visit(detail.get("dependencies", {}))

    for project in projects:
        yield from visit(project.get("dependencies", {}))
        yield from visit(project.get("devDependencies", {}))


def python_components() -> Iterator[dict[str, str]]:
    with (ROOT / "uv.lock").open("rb") as handle:
        lock = tomllib.load(handle)
    for package in lock.get("package", []):
        version = package.get("version")
        source = package.get("source", {})
        if not version or source.get("virtual") or source.get("editable"):
            continue
        name = package["name"]
        yield {
            "type": "library",
            "name": name,
            "version": version,
            "purl": f"pkg:pypi/{quote(name, safe='')}@{version}",
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    unique: dict[tuple[str, str, str], dict[str, str]] = {}
    for component in [*npm_components(), *python_components()]:
        key = (component["purl"], component["name"], component["version"])
        unique[key] = component

    components = sorted(unique.values(), key=lambda item: item["purl"])
    if not components:
        raise AssertionError("SBOM contains no resolved dependencies")

    product_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    document = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "metadata": {
            "component": {
                "type": "application",
                "name": "gis-ai-go",
                "version": product_version,
                "copyright": "Copyright (c) 2026 Chris Page",
                "licenses": [{"license": {"id": "MIT"}}],
            },
            "properties": [
                {
                    "name": "gis-ai-go:scope",
                    "value": "resolved package dependencies; no container or runtime image",
                }
            ],
        },
        "components": components,
    }

    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Generated CycloneDX SBOM with {len(components)} components at {output}.")


if __name__ == "__main__":
    main()
