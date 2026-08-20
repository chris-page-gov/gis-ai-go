"""Deterministic bounded JSON helpers used by execution evidence."""

from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any

MAX_SAFE_INTEGER = 9_007_199_254_740_991
DOMAIN_SEPARATION_PREFIX = b"GIS-AI-GO\0canonical-json\0sha256\0v1\0"
EXECUTION_PARAMETERS_DOMAIN = "gis-ai-go.execution-parameters.v1"
EXECUTION_RESULT_DATA_DOMAIN = "gis-ai-go.execution-result-data.v1"
DOMAIN_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9.-]{0,126}[a-z0-9])?\.v[1-9][0-9]*$")


class StrictJsonError(ValueError):
    """Raised for JSON outside the accepted deterministic subset."""


def _normalise(value: Any, *, depth: int = 0) -> Any:
    if depth > 32:
        raise StrictJsonError("JSON nesting exceeds the execution limit")
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise StrictJsonError("integer is outside the interoperable JSON range")
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise StrictJsonError("number must be finite")
        return 0.0 if value == 0.0 else value
    if isinstance(value, str):
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise StrictJsonError("unpaired Unicode surrogate is not permitted")
        return value
    if isinstance(value, list):
        return [_normalise(item, depth=depth + 1) for item in value]
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise StrictJsonError("object keys must be strings")
        return {
            key: _normalise(item, depth=depth + 1)
            for key, item in value.items()
        }
    raise StrictJsonError("value is outside the JSON data model")


def _serialise_float(value: float) -> str:
    """Serialise one finite IEEE 754 value using RFC 8785 number rules."""

    if not math.isfinite(value):
        raise StrictJsonError("number must be finite")
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    coefficient, exponent_marker, exponent_text = repr(abs(value)).partition("e")
    if not exponent_marker:
        return sign + coefficient.removesuffix(".0")

    exponent = int(exponent_text)
    digits = coefficient.replace(".", "")
    if -6 <= exponent < 21:
        decimal_position = exponent + 1
        if decimal_position <= 0:
            rendered = "0." + ("0" * -decimal_position) + digits
        elif decimal_position >= len(digits):
            rendered = digits + ("0" * (decimal_position - len(digits)))
        else:
            rendered = f"{digits[:decimal_position]}.{digits[decimal_position:]}"
        return sign + rendered

    significand = digits[0] + (f".{digits[1:]}" if len(digits) > 1 else "")
    labelled_exponent = f"+{exponent}" if exponent >= 0 else str(exponent)
    return f"{sign}{significand}e{labelled_exponent}"


def _serialise_canonical(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return _serialise_float(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, list):
        return f"[{','.join(_serialise_canonical(item) for item in value)}]"
    if isinstance(value, dict):
        items = sorted(value.items(), key=lambda item: item[0].encode("utf-16be"))
        return "{" + ",".join(
            f"{_serialise_canonical(key)}:{_serialise_canonical(item)}"
            for key, item in items
        ) + "}"
    raise StrictJsonError("value is outside the JSON data model")


def canonical_json_bytes(value: Any) -> bytes:
    """Return RFC 8785 canonical UTF-8 for the supported bounded JSON subset."""

    return _serialise_canonical(_normalise(value)).encode("utf-8")


def sha256_identity(domain: str, value: Any) -> str:
    """Return a domain-separated labelled SHA-256 identity over canonical JSON."""

    if DOMAIN_PATTERN.fullmatch(domain) is None:
        raise StrictJsonError("canonical digest domain is invalid")
    digest = hashlib.sha256()
    digest.update(DOMAIN_SEPARATION_PREFIX)
    digest.update(domain.encode("utf-8"))
    digest.update(b"\0")
    digest.update(canonical_json_bytes(value))
    return f"sha256:{digest.hexdigest()}"


def strict_json_loads(payload: bytes) -> Any:
    """Decode UTF-8 JSON while rejecting duplicate keys and non-finite numbers."""

    def object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise StrictJsonError("duplicate object key")
            result[key] = value
        return result

    def reject_constant(_value: str) -> None:
        raise StrictJsonError("non-finite number")

    try:
        decoded = payload.decode("utf-8", errors="strict")
        value = json.loads(
            decoded,
            object_pairs_hook=object_pairs,
            parse_constant=reject_constant,
        )
        return _normalise(value)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as error:
        raise StrictJsonError("invalid JSON") from error
