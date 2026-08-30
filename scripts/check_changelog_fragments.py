from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
FRAGMENT_PATTERN = re.compile(
    r"^(?P<identifier>[A-Za-z0-9][A-Za-z0-9._-]*)\."
    r"(?P<category>added|changed|deprecated|removed|fixed|security)\.md$"
)
CATEGORY_HEADINGS = (
    ("added", "Added"),
    ("changed", "Changed"),
    ("deprecated", "Deprecated"),
    ("removed", "Removed"),
    ("fixed", "Fixed"),
    ("security", "Security"),
)
MAX_FRAGMENT_BYTES = 1024


def fragment_paths(root: Path) -> tuple[Path, ...]:
    directory = root / "changelog.d"
    return tuple(
        path
        for path in sorted(directory.glob("*.md"), key=lambda item: item.name)
        if path.name != "README.md"
    )


def fragment_errors(path: Path) -> list[str]:
    """Return fail-closed formatting errors for one release fragment."""
    errors: list[str] = []
    match = FRAGMENT_PATTERN.fullmatch(path.name)
    if match is None:
        errors.append("filename must end in a supported change category")
    if path.is_symlink() or not path.is_file():
        return [*errors, "fragment must be one regular file"]

    raw = path.read_bytes()
    if len(raw) > MAX_FRAGMENT_BYTES:
        errors.append(f"fragment exceeds {MAX_FRAGMENT_BYTES} bytes")
    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError:
        return [*errors, "fragment is not UTF-8"]
    if not content.endswith("\n") or content.endswith("\n\n"):
        errors.append("fragment must end with exactly one LF")
    lines = content.splitlines()
    if not lines or not lines[0].startswith("- ") or len(lines[0]) == 2:
        errors.append("fragment must start with one non-empty Markdown bullet")
    if sum(line.startswith("- ") for line in lines) != 1:
        errors.append("fragment must contain exactly one top-level Markdown bullet")
    if any(line.lstrip().startswith("#") for line in lines):
        errors.append("fragment must not contain a heading")
    if any(not line for line in lines):
        errors.append("fragment must contain exactly one paragraph")
    if any(line.endswith((" ", "\t")) for line in lines):
        errors.append("fragment must not contain trailing whitespace")
    if any("\t" in line for line in lines):
        errors.append("fragment must not contain tabs")
    if any(line and index > 0 and not line.startswith("  ") for index, line in enumerate(lines)):
        errors.append("continuation lines must be indented by two spaces")
    return errors


def collect_fragment_errors(root: Path) -> list[str]:
    directory = root / "changelog.d"
    if not (directory / "README.md").is_file():
        return ["changelog.d/README.md is missing"]
    paths = fragment_paths(root)
    return [
        f"{path.relative_to(root).as_posix()}: {error}"
        for path in paths
        for error in fragment_errors(path)
    ]


def render_release_preview(root: Path, version: str) -> str:
    """Render fragments deterministically without mutating release metadata."""
    errors = collect_fragment_errors(root)
    if errors:
        raise ValueError("; ".join(errors))

    grouped: dict[str, list[str]] = defaultdict(list)
    for path in fragment_paths(root):
        match = FRAGMENT_PATTERN.fullmatch(path.name)
        if match is None:  # Kept explicit for type checkers after validation.
            raise ValueError(f"invalid fragment filename: {path.name}")
        grouped[match.group("category")].append(path.read_text(encoding="utf-8").rstrip())

    output = [
        f"# GIS AI GO v{version} release preview",
        "",
        "> Generated from checked changelog fragments. This is preparation, not release",
        "> evidence; the release date, deployment evidence, version change and tag remain unset.",
    ]
    for category, heading in CATEGORY_HEADINGS:
        entries = grouped.get(category)
        if not entries:
            continue
        output.extend(("", f"## {heading}", ""))
        for entry in entries:
            output.extend((entry, ""))
        output.pop()
    return "\n".join(output) + "\n"


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Validate changelog fragments and optionally render a release preview."
    )
    parser.add_argument(
        "--preview-version",
        metavar="X.Y.Z",
        help="render a deterministic, non-release preview for the supplied target version",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="write the preview to this path instead of standard output",
    )
    arguments = parser.parse_args(argv)
    if arguments.output is not None and arguments.preview_version is None:
        parser.error("--output requires --preview-version")

    errors = collect_fragment_errors(ROOT)
    if errors:
        raise SystemExit("Invalid changelog fragments:\n- " + "\n- ".join(errors))

    paths = fragment_paths(ROOT)
    if arguments.preview_version is None:
        print(f"Validated {len(paths)} changelog fragments.")
        return

    if re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", arguments.preview_version) is None:
        raise SystemExit("--preview-version must be stable Semantic Versioning X.Y.Z")
    preview = render_release_preview(ROOT, arguments.preview_version)
    if arguments.output is None:
        print(preview, end="")
        return
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(preview, encoding="utf-8")
    print(f"Wrote release preview to {arguments.output}.")


if __name__ == "__main__":
    main()
