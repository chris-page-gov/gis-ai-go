#!/usr/bin/env python3
"""Run a conservative, offline Stage 0 secret and machine-path scan."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {
    ".git",
    ".mypy_cache",
    ".pnpm-store",
    ".pytest_cache",
    ".ruff_cache",
    ".uv-cache",
    ".venv",
    "__pycache__",
    "artifacts",
    "dist",
    "node_modules",
}
SKIP_SUFFIXES = {".zip", ".png", ".jpg", ".jpeg", ".gif", ".ico"}
BANNED_NAMES = {".env", "id_rsa", "id_ed25519", "credentials.json"}

PATTERNS = {
    "private key": re.compile("-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"gh" + r"[pousr]_[A-Za-z0-9]{20,}"),
    "OpenAI-style token": re.compile(r"sk" + r"-(?:proj-)?[A-Za-z0-9_-]{20,}"),
    "AWS access key": re.compile(r"AK" + r"IA[0-9A-Z]{16}"),
    "Slack token": re.compile(r"xox" + r"[baprs]-[A-Za-z0-9-]{20,}"),
    "assigned secret": re.compile(
        r"(?i)(?:api[_-]?key|password|client[_-]?secret|access[_-]?token)"
        r"\s*[:=]\s*[\"'][^\"']{8,}[\"']"
    ),
    "machine-specific path": re.compile(r"/(?:Users|home|Volumes)/[A-Za-z0-9._-]+/"),
}


def main() -> None:
    findings: list[str] = []
    scanned = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or SKIP_PARTS.intersection(path.parts):
            continue
        if path.name in BANNED_NAMES:
            findings.append(f"{path.relative_to(ROOT)}: banned credential filename")
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{path.relative_to(ROOT)}: possible {label}")
    if findings:
        raise AssertionError("\n".join(findings))
    print(f"Scanned {scanned} text files; no baseline secret or machine-path match found.")


if __name__ == "__main__":
    main()
