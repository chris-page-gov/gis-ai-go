"""Bounded deterministic geometry validation and point selection."""

from __future__ import annotations

import math
from typing import Any, Sequence

from .errors import INVALID_GEOMETRY, LIMIT_EXCEEDED, ExecutionFailure

Position = tuple[float, float]


def _position(value: Any) -> Position:
    if not isinstance(value, list) or len(value) != 2:
        raise INVALID_GEOMETRY
    longitude, latitude = value
    if (
        isinstance(longitude, bool)
        or isinstance(latitude, bool)
        or not isinstance(longitude, (int, float))
        or not isinstance(latitude, (int, float))
    ):
        raise INVALID_GEOMETRY
    longitude = float(longitude)
    latitude = float(latitude)
    if (
        not math.isfinite(longitude)
        or not math.isfinite(latitude)
        or not -180 <= longitude <= 180
        or not -90 <= latitude <= 90
    ):
        raise INVALID_GEOMETRY
    return (0.0 if longitude == 0 else longitude, 0.0 if latitude == 0 else latitude)


def _orientation(a: Position, b: Position, c: Position) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _on_segment(a: Position, b: Position, point: Position) -> bool:
    epsilon = 1e-12
    return (
        abs(_orientation(a, b, point)) <= epsilon
        and min(a[0], b[0]) - epsilon <= point[0] <= max(a[0], b[0]) + epsilon
        and min(a[1], b[1]) - epsilon <= point[1] <= max(a[1], b[1]) + epsilon
    )


def _segments_intersect(a: Position, b: Position, c: Position, d: Position) -> bool:
    first = _orientation(a, b, c)
    second = _orientation(a, b, d)
    third = _orientation(c, d, a)
    fourth = _orientation(c, d, b)
    if ((first > 0 > second) or (second > 0 > first)) and (
        (third > 0 > fourth) or (fourth > 0 > third)
    ):
        return True
    return any(
        (
            abs(first) <= 1e-12 and _on_segment(a, b, c),
            abs(second) <= 1e-12 and _on_segment(a, b, d),
            abs(third) <= 1e-12 and _on_segment(c, d, a),
            abs(fourth) <= 1e-12 and _on_segment(c, d, b),
        )
    )


def validate_polygon(value: Any, *, max_coordinates: int) -> tuple[Position, ...]:
    """Return a validated simple outer ring without modifying it."""

    if not isinstance(value, dict) or set(value) != {"type", "coordinates"}:
        raise INVALID_GEOMETRY
    if value.get("type") != "Polygon":
        raise INVALID_GEOMETRY
    coordinates = value.get("coordinates")
    if not isinstance(coordinates, list) or len(coordinates) != 1:
        raise INVALID_GEOMETRY
    raw_ring = coordinates[0]
    if not isinstance(raw_ring, list) or len(raw_ring) < 4:
        raise INVALID_GEOMETRY
    if len(raw_ring) > max_coordinates:
        raise LIMIT_EXCEEDED
    ring = tuple(_position(item) for item in raw_ring)
    if ring[0] != ring[-1]:
        raise INVALID_GEOMETRY
    if any(ring[index] == ring[index + 1] for index in range(len(ring) - 1)):
        raise INVALID_GEOMETRY
    if len(set(ring[:-1])) < 3:
        raise INVALID_GEOMETRY

    twice_area = sum(
        ring[index][0] * ring[index + 1][1]
        - ring[index + 1][0] * ring[index][1]
        for index in range(len(ring) - 1)
    )
    if abs(twice_area) <= 1e-12:
        raise INVALID_GEOMETRY

    segment_count = len(ring) - 1
    for first in range(segment_count):
        for second in range(first + 1, segment_count):
            if second in {first, first + 1}:
                continue
            if first == 0 and second == segment_count - 1:
                continue
            if _segments_intersect(
                ring[first],
                ring[first + 1],
                ring[second],
                ring[second + 1],
            ):
                raise INVALID_GEOMETRY
    return ring


def point_in_polygon(point: Position, ring: Sequence[Position]) -> bool:
    """Return whether a point is inside or on the boundary of a simple polygon."""

    inside = False
    for index in range(len(ring) - 1):
        first = ring[index]
        second = ring[index + 1]
        if _on_segment(first, second, point):
            return True
        if (first[1] > point[1]) == (second[1] > point[1]):
            continue
        intersection = (second[0] - first[0]) * (point[1] - first[1]) / (
            second[1] - first[1]
        ) + first[0]
        if point[0] < intersection:
            inside = not inside
    return inside
