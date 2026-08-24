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

from gateway_image import (
    NODE_BASE_DIGEST,
    NODE_BASE_NAME,
    NODE_BASE_VERSION,
    UBI_RUNTIME_BASE_DIGEST,
    UBI_RUNTIME_BASE_REFERENCE,
    UBI_RUNTIME_BASE_VERSION,
    UBI_RUNTIME_LIBRARY_DONOR_DIGEST,
    UBI_RUNTIME_LIBRARY_DONOR_REFERENCE,
    UBI_RUNTIME_LIBRARY_DONOR_VERSION,
    parse_gateway_containerfile_pins,
)

ROOT = Path(__file__).resolve().parents[1]
EXECUTION_BASE_NAME = "python"
EXECUTION_BASE_VERSION = "3.12.14-slim-bookworm"
EXECUTION_BASE_DIGEST = (
    "sha256:a116514e19457bcb7af7efe9c3dd0b9b71e85b317694e7882a1c52aa15a78134"
)
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


def execution_container_components() -> Iterator[dict[str, str]]:
    """Bind the private execution image to its reviewed multi-architecture base."""

    containerfile = (
        ROOT / "services" / "geo-execution" / "Containerfile"
    ).read_text(encoding="utf-8")
    expected = (
        f"FROM {EXECUTION_BASE_NAME}:{EXECUTION_BASE_VERSION}@{EXECUTION_BASE_DIGEST}"
    )
    if expected not in containerfile.splitlines():
        raise AssertionError("execution Containerfile differs from the SBOM base identity")
    purl = (
        f"pkg:oci/{EXECUTION_BASE_NAME}@{quote(EXECUTION_BASE_VERSION, safe='')}"
        f"?repository_url=docker.io%2Flibrary%2Fpython"
        f"&digest={quote(EXECUTION_BASE_DIGEST, safe='')}"
    )
    yield {
        "type": "container",
        "name": EXECUTION_BASE_NAME,
        "version": EXECUTION_BASE_VERSION,
        "purl": purl,
    }


def gateway_container_components() -> Iterator[dict[str, str]]:
    """Bind the blocked gateway image to its fixed builder and UBI runtime inputs."""

    containerfile = (ROOT / "apps" / "mcp-gateway" / "Containerfile").read_text(
        encoding="utf-8"
    )
    parsed = parse_gateway_containerfile_pins(containerfile)
    expected = f"{NODE_BASE_NAME}:{NODE_BASE_VERSION}@{NODE_BASE_DIGEST}"
    if parsed["node_reference"] != expected:
        raise AssertionError("gateway Containerfile differs from the SBOM base identity")
    if (
        parsed["runtime_base_reference"] != UBI_RUNTIME_BASE_REFERENCE
        or parsed["runtime_library_donor_reference"]
        != UBI_RUNTIME_LIBRARY_DONOR_REFERENCE
    ):
        raise AssertionError("gateway Containerfile differs from the UBI runtime identities")
    purl = (
        f"pkg:oci/{NODE_BASE_NAME}@{quote(NODE_BASE_VERSION, safe='')}"
        f"?repository_url=docker.io%2Flibrary%2Fnode"
        f"&digest={quote(NODE_BASE_DIGEST, safe='')}"
    )
    yield {
        "type": "container",
        "name": NODE_BASE_NAME,
        "version": NODE_BASE_VERSION,
        "purl": purl,
    }
    for name, version, repository, digest in (
        (
            "ubi10-micro",
            UBI_RUNTIME_BASE_VERSION,
            "registry.access.redhat.com%2Fubi10-micro",
            UBI_RUNTIME_BASE_DIGEST,
        ),
        (
            "ubi10-nodejs-24-minimal",
            UBI_RUNTIME_LIBRARY_DONOR_VERSION,
            "registry.access.redhat.com%2Fubi10%2Fnodejs-24-minimal",
            UBI_RUNTIME_LIBRARY_DONOR_DIGEST,
        ),
    ):
        yield {
            "type": "container",
            "name": name,
            "version": version,
            "purl": (
                f"pkg:oci/{name}@{quote(version, safe='')}"
                f"?repository_url={repository}&digest={quote(digest, safe='')}"
            ),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    unique: dict[tuple[str, str, str], dict[str, str]] = {}
    for component in [
        *npm_components(),
        *python_components(),
        *execution_container_components(),
        *gateway_container_components(),
    ]:
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
                    "value": (
                        "resolved package dependencies plus the pinned private execution image "
                        "and fixed gateway Node builder, UBI runtime root and UBI library donor; "
                        "the full realised gateway operating-system and runtime-file inventory "
                        "is emitted by the separate DEPLOY-207 image SBOM"
                    ),
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
