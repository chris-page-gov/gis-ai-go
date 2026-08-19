#!/usr/bin/env python3
"""Render live DOT sources without modifying the immutable research pack."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    dot = shutil.which("dot")
    if dot is None:
        raise SystemExit("Graphviz 'dot' is required to render architecture diagrams")

    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.mkdir(parents=True, exist_ok=True)
    sources = sorted((ROOT / "architecture" / "source" / "dot").glob("*.dot"))
    if len(sources) != 9:
        raise AssertionError(f"expected 9 DOT sources, found {len(sources)}")

    for source in sources:
        destination = output / f"{source.stem}.svg"
        subprocess.run([dot, "-Tsvg", str(source), "-o", str(destination)], check=True)
        if "<svg" not in destination.read_text(encoding="utf-8"):
            raise AssertionError(f"Graphviz did not create an SVG: {destination}")

    version = subprocess.run([dot, "-V"], capture_output=True, check=True, text=True)
    detail = (version.stderr or version.stdout).strip()
    print(f"Rendered {len(sources)} diagrams with {detail}.")


if __name__ == "__main__":
    main()
