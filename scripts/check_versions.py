from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def main() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        raise SystemExit(f"VERSION is not valid Semantic Versioning: {version!r}")

    observed: dict[str, str] = {}
    for relative in (
        "package.json",
        "apps/mcp-gateway/package.json",
        "packages/contracts/package.json",
    ):
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

    print(f"Validated product version {version} across {len(observed)} manifests and locks.")


if __name__ == "__main__":
    main()
