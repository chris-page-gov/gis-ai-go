from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
FIXED_NOW = datetime(2026, 8, 20, 12, 0, tzinfo=timezone.utc)


def load_fixture(name: str) -> dict[str, Any]:
    value = json.loads(
        (ROOT / "providers" / "fixtures" / name).read_text(encoding="utf-8")
    )
    return copy.deepcopy(value)


def valid_request() -> dict[str, Any]:
    return load_fixture("execution-request.example.json")


def expected_result() -> dict[str, Any]:
    return load_fixture("execution-result.example.json")
