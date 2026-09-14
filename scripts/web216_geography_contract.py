"""Pure offline WEB-216 X04 contract for synthetic point-to-area joins.

This module deliberately supports only bounded, synthetic simple polygons with
integer EPSG:27700 coordinates. Predicates use exact integer arithmetic. It is not
a general GIS engine: it does not transform, repair, simplify or find nearest
geographies, and it does not evaluate provider rights.
"""

from __future__ import annotations

import copy
import re
from typing import Any
from urllib.parse import urlsplit


INPUT_SCHEMA = "web216.synthetic-geography-join.v1"
OUTPUT_SCHEMA = "web216.synthetic-geography-join-result.v1"
CLASSIFICATION = "synthetic-only-not-ons-or-os-payload"
CRS = "EPSG:27700"
GEOGRAPHY_VINTAGE = "Census 2021"
POINT_VINTAGE = "2026 named point"
JOIN_FIELD = "MSOA21CD"
CROSS_VINTAGE_WARNING = (
    "Representative points use the declared 2026 named-point vintage while MSOA "
    "boundaries and statistics use Census 2021. The join establishes strict spatial "
    "membership only; it does not establish cross-vintage equivalence."
)

MAX_FEATURES = 64
MAX_POINTS = 64
MAX_VERTICES = 128
MAX_STATISTIC_ROWS = 2_048
MAX_CATEGORIES = 32
MAX_EVIDENCE_ITEMS = 8
MAX_LINKS = 8
MAX_ABSOLUTE_COORDINATE = 10_000_000

_IDENTIFIER = re.compile(r"[A-Z0-9][A-Z0-9-]{0,31}\Z")
_DIMENSION = re.compile(r"[a-z][a-z0-9_]{0,63}\Z")


class GeographyContractError(ValueError):
    """A stable, fail-closed X04 contract error."""

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


def _fail(code: str, detail: str) -> None:
    raise GeographyContractError(code, detail)


def _record(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        _fail("INVALID_CONTRACT", f"{label} must contain exactly {sorted(keys)}")
    return value


def _list(value: Any, label: str, *, minimum: int, maximum: int) -> list[Any]:
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        _fail("INVALID_CONTRACT", f"{label} must contain {minimum} to {maximum} items")
    return value


def _text(value: Any, label: str, *, maximum: int = 256) -> str:
    if (
        not isinstance(value, str)
        or not value
        or len(value) > maximum
        or any(ord(character) < 32 for character in value)
    ):
        _fail("INVALID_CONTRACT", f"{label} must be a bounded printable string")
    return value


def _identifier(value: Any, label: str) -> str:
    text = _text(value, label, maximum=32)
    if not _IDENTIFIER.fullmatch(text):
        _fail("INVALID_CONTRACT", f"{label} is not a bounded synthetic identifier")
    return text


def _coordinate(value: Any, label: str) -> int:
    if type(value) is not int or not -MAX_ABSOLUTE_COORDINATE <= value <= MAX_ABSOLUTE_COORDINATE:
        _fail("INVALID_CONTRACT", f"{label} must be a bounded integer coordinate; floats are unsupported")
    return value


def _point(value: Any, label: str) -> tuple[int, int]:
    values = _list(value, label, minimum=2, maximum=2)
    return (_coordinate(values[0], f"{label}[0]"), _coordinate(values[1], f"{label}[1]"))


def _cross(
    first: tuple[int, int],
    second: tuple[int, int],
    third: tuple[int, int],
) -> int:
    return ((second[0] - first[0]) * (third[1] - first[1])
            - (second[1] - first[1]) * (third[0] - first[0]))


def _on_segment(
    point: tuple[int, int],
    start: tuple[int, int],
    end: tuple[int, int],
) -> bool:
    return (
        _cross(start, end, point) == 0
        and min(start[0], end[0]) <= point[0] <= max(start[0], end[0])
        and min(start[1], end[1]) <= point[1] <= max(start[1], end[1])
    )


def _segments_intersect(
    first_start: tuple[int, int],
    first_end: tuple[int, int],
    second_start: tuple[int, int],
    second_end: tuple[int, int],
) -> bool:
    crosses = (
        _cross(first_start, first_end, second_start),
        _cross(first_start, first_end, second_end),
        _cross(second_start, second_end, first_start),
        _cross(second_start, second_end, first_end),
    )
    if ((crosses[0] > 0 > crosses[1] or crosses[0] < 0 < crosses[1])
            and (crosses[2] > 0 > crosses[3] or crosses[2] < 0 < crosses[3])):
        return True
    return (
        (crosses[0] == 0 and _on_segment(second_start, first_start, first_end))
        or (crosses[1] == 0 and _on_segment(second_end, first_start, first_end))
        or (crosses[2] == 0 and _on_segment(first_start, second_start, second_end))
        or (crosses[3] == 0 and _on_segment(first_end, second_start, second_end))
    )


def _simple_ring(geometry: Any, label: str) -> tuple[tuple[int, int], ...]:
    geometry = _record(geometry, {"type", "coordinates"}, label)
    if geometry["type"] != "Polygon":
        _fail("UNSUPPORTED_GEOMETRY", f"{label} must be a Polygon")
    rings = geometry["coordinates"]
    if not isinstance(rings, list) or len(rings) != 1:
        _fail("UNSUPPORTED_GEOMETRY", f"{label} must have one exterior ring and no holes")
    raw_ring = _list(
        rings[0], f"{label}.coordinates[0]", minimum=4, maximum=MAX_VERTICES + 1
    )
    ring = tuple(_point(value, f"{label}.coordinates[0]") for value in raw_ring)
    if ring[0] != ring[-1]:
        _fail("UNSUPPORTED_GEOMETRY", f"{label} exterior ring must be closed")
    vertices = ring[:-1]
    if len(set(vertices)) != len(vertices):
        _fail("UNSUPPORTED_GEOMETRY", f"{label} must not repeat exterior vertices")
    if any(ring[index] == ring[index + 1] for index in range(len(ring) - 1)):
        _fail("UNSUPPORTED_GEOMETRY", f"{label} must not contain zero-length edges")
    doubled_area = sum(
        start[0] * end[1] - end[0] * start[1]
        for start, end in zip(ring, ring[1:])
    )
    if doubled_area == 0:
        _fail("UNSUPPORTED_GEOMETRY", f"{label} must have non-zero area")

    edge_count = len(ring) - 1
    for first in range(edge_count):
        for second in range(first + 1, edge_count):
            adjacent = second == first + 1 or (first == 0 and second == edge_count - 1)
            if not adjacent and _segments_intersect(
                ring[first], ring[first + 1], ring[second], ring[second + 1]
            ):
                _fail("UNSUPPORTED_GEOMETRY", f"{label} must be a simple polygon")
    return ring


def _location(
    point: tuple[int, int], ring: tuple[tuple[int, int], ...]
) -> str:
    if any(_on_segment(point, start, end) for start, end in zip(ring, ring[1:])):
        return "boundary"
    inside = False
    for start, end in zip(ring, ring[1:]):
        if (start[1] > point[1]) != (end[1] > point[1]):
            # The crossing lies to the right exactly when cross / delta_y > 0.
            # Compare signs instead of dividing, preserving exactness in both directions.
            cross = _cross(start, end, point)
            if ((cross > 0 and end[1] > start[1])
                    or (cross < 0 and end[1] < start[1])):
                inside = not inside
    return "inside" if inside else "outside"


def _validate_evidence(value: Any) -> list[dict[str, Any]]:
    evidence = _list(
        value, "source_evidence", minimum=1, maximum=MAX_EVIDENCE_ITEMS
    )
    source_ids: set[str] = set()
    for index, raw_item in enumerate(evidence):
        item = _record(raw_item, {"source_id", "title", "rights", "links"},
                       f"source_evidence[{index}]")
        source_id = _identifier(item["source_id"], f"source_evidence[{index}].source_id")
        if source_id in source_ids:
            _fail("INVALID_CONTRACT", "source evidence identifiers must be unique")
        source_ids.add(source_id)
        _text(item["title"], f"source_evidence[{index}].title")
        rights = _record(item["rights"], {"label", "url"},
                         f"source_evidence[{index}].rights")
        _text(rights["label"], f"source_evidence[{index}].rights.label")
        links = _list(item["links"], f"source_evidence[{index}].links",
                      minimum=1, maximum=MAX_LINKS)
        urls = [rights["url"]]
        for link_index, raw_link in enumerate(links):
            link = _record(raw_link, {"label", "url"},
                           f"source_evidence[{index}].links[{link_index}]")
            _text(link["label"], f"source_evidence[{index}].links[{link_index}].label")
            urls.append(link["url"])
        for url in urls:
            parsed = urlsplit(_text(url, "source evidence URL", maximum=2_048))
            if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
                _fail(
                    "INVALID_CONTRACT",
                    "source evidence links must be person-verifiable HTTPS URLs",
                )
    return copy.deepcopy(evidence)


def evaluate_geography_join(payload: Any) -> dict[str, Any]:
    """Validate and execute one bounded synthetic point-in-polygon join contract."""

    root = _record(
        payload,
        {
            "schema_version", "classification", "fixture_notice", "geography",
            "representative_points", "statistics", "source_evidence",
        },
        "payload",
    )
    if root["schema_version"] != INPUT_SCHEMA or root["classification"] != CLASSIFICATION:
        _fail("INVALID_CONTRACT", "only the declared synthetic X04 contract is supported")
    _text(root["fixture_notice"], "fixture_notice", maximum=512)

    geography = _record(root["geography"], {"crs", "vintage", "identifier_field", "features"},
                        "geography")
    points = _record(root["representative_points"], {"crs", "vintage", "items"},
                     "representative_points")
    statistics = _record(
        root["statistics"],
        {
            "geography_vintage", "join_field", "category_dimension", "expected_categories",
            "fixed_dimensions", "rows",
        },
        "statistics",
    )
    if geography["crs"] != CRS or points["crs"] != CRS:
        _fail("INCOMPATIBLE_CRS", f"both geometry layers must declare {CRS}")
    if (
        geography["vintage"] != GEOGRAPHY_VINTAGE
        or statistics["geography_vintage"] != GEOGRAPHY_VINTAGE
        or points["vintage"] != POINT_VINTAGE
    ):
        _fail("INCOMPATIBLE_VINTAGE", "the declared Census 2021/2026 vintage contract is required")
    if geography["identifier_field"] != JOIN_FIELD or statistics["join_field"] != JOIN_FIELD:
        _fail("INVALID_CONTRACT", f"joins must use {JOIN_FIELD}")

    features = _list(geography["features"], "geography.features", minimum=1,
                     maximum=MAX_FEATURES)
    areas: dict[str, tuple[tuple[int, int], ...]] = {}
    for index, raw_feature in enumerate(features):
        feature = _record(raw_feature, {JOIN_FIELD, "label", "geometry"},
                          f"geography.features[{index}]")
        code = _identifier(feature[JOIN_FIELD], f"geography.features[{index}].{JOIN_FIELD}")
        if code in areas:
            _fail("DUPLICATE_GEOGRAPHY_IDENTIFIER", f"duplicate {JOIN_FIELD}")
        _text(feature["label"], f"geography.features[{index}].label")
        areas[code] = _simple_ring(feature["geometry"], f"geography.features[{index}].geometry")

    point_items = _list(points["items"], "representative_points.items", minimum=1,
                        maximum=MAX_POINTS)
    parsed_points: list[tuple[str, str, tuple[int, int]]] = []
    point_ids: set[str] = set()
    for index, raw_point in enumerate(point_items):
        item = _record(raw_point, {"id", "name", "coordinates"},
                       f"representative_points.items[{index}]")
        point_id = _identifier(item["id"], f"representative_points.items[{index}].id")
        if point_id in point_ids:
            _fail("INVALID_CONTRACT", "representative point identifiers must be unique")
        point_ids.add(point_id)
        parsed_points.append((point_id, _text(item["name"], "representative point name"),
                              _point(item["coordinates"], "representative point coordinates")))

    category_dimension = _text(statistics["category_dimension"], "category_dimension", maximum=64)
    if not _DIMENSION.fullmatch(category_dimension):
        _fail("INVALID_CONTRACT", "category_dimension must be a bounded machine name")
    expected_categories = _list(statistics["expected_categories"], "expected_categories",
                                minimum=1, maximum=MAX_CATEGORIES)
    categories = [_text(value, "expected category", maximum=64) for value in expected_categories]
    if len(set(categories)) != len(categories):
        _fail("INVALID_CONTRACT", "expected categories must be unique")

    fixed_dimensions = statistics["fixed_dimensions"]
    if not isinstance(fixed_dimensions, dict) or not 1 <= len(fixed_dimensions) <= 8:
        _fail("INVALID_CONTRACT", "fixed_dimensions must contain 1 to 8 entries")
    fixed: dict[str, str] = {}
    for raw_name, raw_value in fixed_dimensions.items():
        name = _text(raw_name, "fixed dimension name", maximum=64)
        if not _DIMENSION.fullmatch(name) or name == category_dimension:
            _fail("INVALID_CONTRACT", "fixed dimension names must be distinct machine names")
        fixed[name] = _text(raw_value, f"fixed dimension {name}", maximum=128)

    rows = _list(statistics["rows"], "statistics.rows", minimum=1,
                 maximum=MAX_STATISTIC_ROWS)
    rows_by_area: dict[str, dict[str, dict[str, Any]]] = {}
    dimension_tuples: set[tuple[str, tuple[tuple[str, str], ...]]] = set()
    expected_dimension_names = {*fixed, category_dimension}
    for index, raw_row in enumerate(rows):
        row = _record(raw_row, {JOIN_FIELD, "dimensions", "count"}, f"statistics.rows[{index}]")
        code = _identifier(row[JOIN_FIELD], f"statistics.rows[{index}].{JOIN_FIELD}")
        if code not in areas:
            _fail("UNKNOWN_GEOGRAPHY_IDENTIFIER", f"statistics row has unknown {JOIN_FIELD}")
        raw_dimensions = row["dimensions"]
        if not isinstance(raw_dimensions, dict) or set(raw_dimensions) != expected_dimension_names:
            _fail("INVALID_CONTRACT", "statistic dimensions must match the declared slice")
        dimensions = {
            _text(name, "statistic dimension name", maximum=64):
                _text(value, f"statistic dimension {name}", maximum=128)
            for name, value in raw_dimensions.items()
        }
        if any(dimensions[name] != value for name, value in fixed.items()):
            _fail("INVALID_CONTRACT", "statistic row conflicts with fixed dimensions")
        category = dimensions[category_dimension]
        if category not in categories:
            _fail("UNEXPECTED_STATISTIC_CATEGORY", "statistic row has an unexpected category")
        count = row["count"]
        if isinstance(count, bool) or not isinstance(count, int) or not 0 <= count <= 10**15:
            _fail("INVALID_CONTRACT", "statistic count must be a bounded non-negative integer")
        dimension_tuple = (code, tuple(sorted(dimensions.items())))
        if dimension_tuple in dimension_tuples:
            _fail("DUPLICATE_STATISTIC_TUPLE", "duplicate geography and dimension tuple")
        dimension_tuples.add(dimension_tuple)
        rows_by_area.setdefault(code, {})[category] = {
            "dimensions": dict(sorted(dimensions.items())), "count": count
        }
    for rows_for_area in rows_by_area.values():
        if set(rows_for_area) != set(categories):
            _fail("MISSING_EXPECTED_CATEGORY", "statistics omit an expected category")

    evidence = _validate_evidence(root["source_evidence"])
    joins = []
    for point_id, point_name, coordinates in parsed_points:
        locations = {code: _location(coordinates, ring) for code, ring in areas.items()}
        if "boundary" in locations.values() or sum(
            location == "inside" for location in locations.values()
        ) > 1:
            _fail("AMBIGUOUS_POINT_LOCATION", "point is on an edge or in overlapping polygons")
        matching = [code for code, location in locations.items() if location == "inside"]
        if not matching:
            _fail("UNSUPPORTED_POINT_LOCATION", "point is outside all supported polygons")
        code = matching[0]
        if code not in rows_by_area:
            _fail("MISSING_EXPECTED_CATEGORY", "matched geography has no complete statistic slice")
        joins.append({
            "point_id": point_id,
            "point_name": point_name,
            JOIN_FIELD: code,
            "statistics": [rows_by_area[code][category] for category in categories],
        })

    return {
        "schema_version": OUTPUT_SCHEMA,
        "classification": CLASSIFICATION,
        "crs": CRS,
        "geography_vintage": GEOGRAPHY_VINTAGE,
        "point_vintage": POINT_VINTAGE,
        "cross_vintage_warning": CROSS_VINTAGE_WARNING,
        "join_key": JOIN_FIELD,
        "join_method": "strict-point-in-single-simple-polygon",
        "nearest_fallback_used": False,
        "joins": joins,
        "source_evidence": evidence,
        "source_evidence_status": "untrusted-evidence-not-permission",
        "rights_decision": "not-evaluated",
        "limitations": [
            "Synthetic fixtures only; no ONS or OS payload is present.",
            "Geometry support is limited to one simple exterior polygon ring with bounded integer coordinates.",
            "No CRS transformation, geometry repair, nearest fallback or rights decision is "
            "performed.",
        ],
    }
