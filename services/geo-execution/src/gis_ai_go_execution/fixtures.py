"""Small public synthetic fixtures for deterministic execution acceptance."""

from __future__ import annotations

from types import MappingProxyType
from typing import Any

FIXTURE_ID = "synthetic-gb-places-v1"
SOURCE = MappingProxyType(
    {
        "provider_id": "gis-ai-go.synthetic-fixture",
        "dataset_id": "synthetic-gb-places",
        "version": "1.0.0",
        "rights": "CC0-1.0",
        "source_uri": "urn:gis-ai-go:fixture:synthetic-gb-places:1",
    }
)

# These deliberately fictional records exist only to verify contracts. Their
# coordinates are test values and carry no assertion about a real person or place.
FEATURES: tuple[dict[str, Any], ...] = (
    {
        "type": "Feature",
        "id": "SYN-001",
        "geometry": {"type": "Point", "coordinates": [-1.50, 52.40]},
        "properties": {
            "native_id": "SYN-001",
            "name": "Synthetic Alpha",
            "category": "synthetic-place",
        },
    },
    {
        "type": "Feature",
        "id": "SYN-002",
        "geometry": {"type": "Point", "coordinates": [-1.90, 52.48]},
        "properties": {
            "native_id": "SYN-002",
            "name": "Synthetic Bravo",
            "category": "synthetic-place",
        },
    },
    {
        "type": "Feature",
        "id": "SYN-003",
        "geometry": {"type": "Point", "coordinates": [-3.18, 51.48]},
        "properties": {
            "native_id": "SYN-003",
            "name": "Synthetic Charlie",
            "category": "synthetic-place",
        },
    },
    {
        "type": "Feature",
        "id": "SYN-004",
        "geometry": {"type": "Point", "coordinates": [-0.12, 51.50]},
        "properties": {
            "native_id": "SYN-004",
            "name": "Synthetic Delta",
            "category": "synthetic-place",
        },
    },
    {
        "type": "Feature",
        "id": "SYN-005",
        "geometry": {"type": "Point", "coordinates": [-3.19, 55.95]},
        "properties": {
            "native_id": "SYN-005",
            "name": "Synthetic Echo",
            "category": "synthetic-place",
        },
    },
)
