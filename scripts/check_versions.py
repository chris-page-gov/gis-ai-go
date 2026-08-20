from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
STABLE_SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
RELEASE_DATE = r"\d{4}-\d{2}-\d{2}"


def npm_package_manifests(root: Path) -> tuple[str, ...]:
    """Return every root and pnpm-workspace package manifest deterministically."""
    manifests = [root / "package.json"]
    manifests.extend(sorted((root / "apps").glob("*/package.json")))
    manifests.extend(sorted((root / "packages").glob("*/package.json")))
    return tuple(path.relative_to(root).as_posix() for path in manifests)


def is_valid_product_version(value: str) -> bool:
    """Return whether a version is stable SemVer and valid unchanged in Python metadata."""
    return STABLE_SEMVER.fullmatch(value) is not None


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def release_metadata_errors(root: Path, version: str) -> list[str]:
    """Return release metadata errors for a supported, non-bootstrap version."""
    if version == "0.0.0":
        return []

    errors: list[str] = []
    changelog_path = root / "CHANGELOG.md"
    if changelog_path.is_file():
        changelog = changelog_path.read_text(encoding="utf-8")
    else:
        changelog = ""
        errors.append("CHANGELOG.md is missing")
    release_header = re.compile(
        rf"^## \[{re.escape(version)}\] - {RELEASE_DATE}$",
        re.MULTILINE,
    )
    if release_header.search(changelog) is None:
        errors.append(f"CHANGELOG.md has no dated [{version}] release section")

    release_link = (
        f"[{version}]: https://github.com/chris-page-gov/gis-ai-go/releases/tag/v{version}"
    )
    if release_link not in changelog.splitlines():
        errors.append(f"CHANGELOG.md has no exact [{version}] release link")

    release_notes = root / "RELEASE_NOTES" / f"{version}.md"
    if not release_notes.is_file():
        errors.append(f"{release_notes.relative_to(root).as_posix()} is missing")
    elif not release_notes.read_text(encoding="utf-8").strip():
        errors.append(f"{release_notes.relative_to(root).as_posix()} is empty")

    fragment_directory = root / "changelog.d"
    if not (fragment_directory / "README.md").is_file():
        errors.append("changelog.d/README.md is missing")
    fragments = sorted(
        path.name
        for path in fragment_directory.glob("*.md")
        if path.name != "README.md"
    )
    if fragments:
        errors.append(f"unconsumed changelog fragments: {', '.join(fragments)}")

    return errors


def release_readiness_errors(
    root: Path,
    version: str,
    *,
    release_ready: bool,
) -> list[str]:
    """Return release-only errors when an explicit release gate is requested."""
    if not release_ready:
        return []
    if version == "0.0.0":
        return ["VERSION 0.0.0 is the bootstrap candidate and cannot be released"]
    return release_metadata_errors(root, version)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Validate product-version synchronisation and optional release metadata."
    )
    parser.add_argument(
        "--release-ready",
        action="store_true",
        help="also require complete release notes, changelog metadata and consumed fragments",
    )
    arguments = parser.parse_args(argv)

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not is_valid_product_version(version):
        raise SystemExit(f"VERSION must be stable Semantic Versioning X.Y.Z: {version!r}")

    observed: dict[str, str] = {}
    for relative in npm_package_manifests(ROOT):
        value = load_json(ROOT / relative).get("version")
        observed[relative] = str(value)

    for relative in ("pyproject.toml", "services/geo-execution/pyproject.toml"):
        project = load_toml(ROOT / relative).get("project")
        if not isinstance(project, dict):
            raise SystemExit(f"{relative} has no [project] table")
        observed[relative] = str(project.get("version"))

    lock = load_toml(ROOT / "uv.lock")
    packages = lock.get("package")
    if not isinstance(packages, list):
        raise SystemExit("uv.lock has no package list")
    workspace_names = {"gis-ai-go", "gis-ai-go-execution"}
    for package in packages:
        if not isinstance(package, dict) or package.get("name") not in workspace_names:
            continue
        observed[f"uv.lock:{package['name']}"] = str(package.get("version"))

    missing = sorted(
        f"uv.lock:{name}" for name in workspace_names if f"uv.lock:{name}" not in observed
    )
    mismatches = sorted(
        f"{source}={value}" for source, value in observed.items() if value != version
    )
    if missing or mismatches:
        details = "; ".join([*missing, *mismatches])
        raise SystemExit(f"Product versions do not match VERSION {version}: {details}")

    release_errors = release_readiness_errors(
        ROOT,
        version,
        release_ready=arguments.release_ready,
    )
    if release_errors:
        raise SystemExit("Release metadata is incomplete: " + "; ".join(release_errors))

    suffix = " Release metadata is complete." if arguments.release_ready else ""
    print(
        f"Validated product version {version} across {len(observed)} manifests and locks."
        f"{suffix}"
    )


if __name__ == "__main__":
    main()
