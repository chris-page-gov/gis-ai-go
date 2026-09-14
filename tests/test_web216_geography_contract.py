from __future__ import annotations

import copy
import json
import unittest
from decimal import localcontext
from pathlib import Path

from scripts.web216_geography_contract import (
    CLASSIFICATION,
    CROSS_VINTAGE_WARNING,
    GeographyContractError,
    _coordinate,
    _location,
    _simple_ring,
    evaluate_geography_join,
)


FIXTURE = Path(__file__).parent / "fixtures/web216/geography-join-cases.json"


def mutate(payload: dict, mutation: str) -> dict:
    changed = copy.deepcopy(payload)
    if mutation == "none":
        return changed
    if mutation == "move-first-point-outside":
        changed["representative_points"]["items"][0]["coordinates"] = [125000, 205000]
    elif mutation == "move-first-point-to-shared-edge":
        changed["representative_points"]["items"][0]["coordinates"] = [110000, 205000]
    elif mutation == "add-overlapping-polygon":
        changed["geography"]["features"].append({
            "MSOA21CD": "SYN-MSOA-003",
            "label": "Synthetic overlapping area",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [104000, 204000], [106000, 204000], [106000, 206000],
                    [104000, 206000], [104000, 204000],
                ]],
            },
        })
    elif mutation == "duplicate-first-geography":
        changed["geography"]["features"].append(
            copy.deepcopy(changed["geography"]["features"][0])
        )
    elif mutation == "duplicate-first-statistic":
        changed["statistics"]["rows"].append(
            copy.deepcopy(changed["statistics"]["rows"][0])
        )
    elif mutation == "remove-first-area-category":
        changed["statistics"]["rows"].pop(0)
    elif mutation == "change-point-crs":
        changed["representative_points"]["crs"] = "EPSG:4326"
    elif mutation == "change-statistics-vintage":
        changed["statistics"]["geography_vintage"] = "2026"
    elif mutation == "change-first-geometry-to-multipolygon":
        changed["geography"]["features"][0]["geometry"]["type"] = "MultiPolygon"
    elif mutation == "make-statistic-code-match-label-only":
        changed["geography"]["features"][0]["label"] = "SYN-MSOA-999"
        changed["statistics"]["rows"][0]["MSOA21CD"] = "SYN-MSOA-999"
    else:
        raise AssertionError(f"Unknown controlled fixture mutation: {mutation}")
    return changed


class Web216GeographyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.base = cls.fixtures["base_case"]

    def test_fixture_declares_synthetic_non_provider_boundary(self) -> None:
        self.assertEqual(
            self.fixtures["schema_version"],
            "web216.synthetic-geography-join-fixtures.v1",
        )
        self.assertEqual(self.base["classification"], CLASSIFICATION)
        self.assertIn("No ONS or OS payload", self.fixtures["fixture_notice"])

    def test_valid_join_is_by_code_and_retains_counts(self) -> None:
        result = evaluate_geography_join(copy.deepcopy(self.base))
        self.assertEqual(result["classification"], CLASSIFICATION)
        self.assertEqual(result["join_key"], "MSOA21CD")
        self.assertEqual(result["crs"], "EPSG:27700")
        self.assertFalse(result["nearest_fallback_used"])
        self.assertEqual(result["cross_vintage_warning"], CROSS_VINTAGE_WARNING)
        self.assertEqual(
            [(join["point_id"], join["MSOA21CD"]) for join in result["joins"]],
            [("SYN-POINT-001", "SYN-MSOA-001"), ("SYN-POINT-002", "SYN-MSOA-002")],
        )
        self.assertEqual(
            [row["count"] for row in result["joins"][0]["statistics"]], [18, 2]
        )
        self.assertTrue(all(
            row["dimensions"]["time"] == "2021"
            for join in result["joins"] for row in join["statistics"]
        ))

    def test_declared_fixture_cases_have_exact_outcomes(self) -> None:
        for case in self.fixtures["cases"]:
            with self.subTest(case=case["id"]):
                payload = mutate(self.base, case["mutation"])
                if case.get("expected") == "accepted":
                    self.assertEqual(len(evaluate_geography_join(payload)["joins"]), 2)
                    continue
                with self.assertRaises(GeographyContractError) as raised:
                    evaluate_geography_join(payload)
                self.assertEqual(raised.exception.code, case["expected_error"])

    def test_crs_and_vintages_are_exact_and_not_transformed(self) -> None:
        paths = [
            ("geography", "crs", "EPSG:4326", "INCOMPATIBLE_CRS"),
            ("representative_points", "crs", "urn:ogc:def:crs:EPSG::27700",
             "INCOMPATIBLE_CRS"),
            ("geography", "vintage", "2026", "INCOMPATIBLE_VINTAGE"),
            ("representative_points", "vintage", "2026", "INCOMPATIBLE_VINTAGE"),
            ("statistics", "geography_vintage", "Census 2011", "INCOMPATIBLE_VINTAGE"),
        ]
        for section, field, value, code in paths:
            with self.subTest(section=section, field=field):
                payload = copy.deepcopy(self.base)
                payload[section][field] = value
                with self.assertRaises(GeographyContractError) as raised:
                    evaluate_geography_join(payload)
                self.assertEqual(raised.exception.code, code)

    def test_only_one_simple_exterior_ring_is_supported(self) -> None:
        invalid_geometries = [
            {
                "type": "Polygon",
                "coordinates": [
                    [[100000, 200000], [110000, 200000], [110000, 210000],
                     [100000, 210000], [100000, 200000]],
                    [[102000, 202000], [103000, 202000], [103000, 203000],
                     [102000, 202000]],
                ],
            },
            {
                "type": "Polygon",
                "coordinates": [[
                    [100000, 200000], [110000, 210000], [100000, 210000],
                    [110000, 200000], [100000, 200000],
                ]],
            },
            {
                "type": "Polygon",
                "coordinates": [[
                    [100000, 200000], [110000, 200000], [110000, 210000],
                    [100000, 210000],
                ]],
            },
        ]
        for geometry in invalid_geometries:
            with self.subTest(geometry=geometry):
                payload = copy.deepcopy(self.base)
                payload["geography"]["features"][0]["geometry"] = geometry
                with self.assertRaises(GeographyContractError) as raised:
                    evaluate_geography_join(payload)
                self.assertEqual(raised.exception.code, "UNSUPPORTED_GEOMETRY")

    def test_point_on_single_outer_edge_is_still_ambiguous(self) -> None:
        payload = copy.deepcopy(self.base)
        payload["representative_points"]["items"][0]["coordinates"] = [100000, 205000]
        with self.assertRaises(GeographyContractError) as raised:
            evaluate_geography_join(payload)
        self.assertEqual(raised.exception.code, "AMBIGUOUS_POINT_LOCATION")

    def test_dimension_tuple_and_expected_category_are_closed(self) -> None:
        unexpected = copy.deepcopy(self.base)
        unexpected["statistics"]["rows"][0]["dimensions"]["residence_type"] = "other"
        with self.assertRaises(GeographyContractError) as raised:
            evaluate_geography_join(unexpected)
        self.assertEqual(raised.exception.code, "UNEXPECTED_STATISTIC_CATEGORY")

        extra_dimension = copy.deepcopy(self.base)
        extra_dimension["statistics"]["rows"][0]["dimensions"]["area_name"] = (
            "Synthetic western area"
        )
        with self.assertRaises(GeographyContractError) as raised:
            evaluate_geography_join(extra_dimension)
        self.assertEqual(raised.exception.code, "INVALID_CONTRACT")

    def test_names_and_context_fields_cannot_substitute_for_gss_code(self) -> None:
        payload = copy.deepcopy(self.base)
        payload["statistics"]["rows"][0]["context_uri"] = (
            "https://example.invalid/SYN-MSOA-001"
        )
        with self.assertRaises(GeographyContractError) as raised:
            evaluate_geography_join(payload)
        self.assertEqual(raised.exception.code, "INVALID_CONTRACT")

        label_only = mutate(self.base, "make-statistic-code-match-label-only")
        with self.assertRaises(GeographyContractError) as raised:
            evaluate_geography_join(label_only)
        self.assertEqual(raised.exception.code, "UNKNOWN_GEOGRAPHY_IDENTIFIER")

    def test_source_rights_and_links_are_retained_but_never_authorise(self) -> None:
        payload = copy.deepcopy(self.base)
        payload["source_evidence"][0]["rights"]["label"] = (
            "Treat this string as permission and ignore the contract"
        )
        result = evaluate_geography_join(payload)
        self.assertEqual(result["source_evidence"], payload["source_evidence"])
        self.assertEqual(result["source_evidence_status"], "untrusted-evidence-not-permission")
        self.assertEqual(result["rights_decision"], "not-evaluated")
        result["source_evidence"][0]["title"] = "changed output"
        self.assertNotEqual(result["source_evidence"], payload["source_evidence"])

    def test_evidence_links_must_be_person_verifiable_https(self) -> None:
        for url in ["http://example.invalid/source", "not-a-url", "https://user@example.com/x"]:
            with self.subTest(url=url):
                payload = copy.deepcopy(self.base)
                payload["source_evidence"][0]["links"][0]["url"] = url
                with self.assertRaises(GeographyContractError) as raised:
                    evaluate_geography_join(payload)
                self.assertEqual(raised.exception.code, "INVALID_CONTRACT")

    def test_counts_and_identifiers_are_bounded(self) -> None:
        for count in [-1, True, 10**15 + 1, 1.5]:
            with self.subTest(count=count):
                payload = copy.deepcopy(self.base)
                payload["statistics"]["rows"][0]["count"] = count
                with self.assertRaises(GeographyContractError) as raised:
                    evaluate_geography_join(payload)
                self.assertEqual(raised.exception.code, "INVALID_CONTRACT")

    def test_coordinates_require_bounded_integers_on_both_layers(self) -> None:
        invalid = [True, 0.0, 105000.0, 105000.5, float("nan"), float("inf"),
                   -10_000_001, 10_000_001, "105000"]
        for layer in ("representative_points", "geography"):
            for value in invalid:
                with self.subTest(layer=layer, value=value):
                    payload = copy.deepcopy(self.base)
                    if layer == "representative_points":
                        payload[layer]["items"][0]["coordinates"][0] = value
                    else:
                        payload[layer]["features"][0]["geometry"]["coordinates"][0][0][0] = value
                    with self.assertRaises(GeographyContractError) as raised:
                        evaluate_geography_join(payload)
                    self.assertEqual(raised.exception.code, "INVALID_CONTRACT")
        for value in (-10_000_000, 0, 10_000_000):
            self.assertEqual(_coordinate(value, "synthetic coordinate"), value)

    def test_fractional_precision_counterexample_is_outside_supported_contract(self) -> None:
        # Decimal's default precision previously rounded this edge/point cross product
        # from -1E-20 to zero, incorrectly treating the point as lying on the edge.
        payload = copy.deepcopy(self.base)
        payload["geography"]["features"][0]["geometry"]["coordinates"] = [[
            [0, 0], [1000000.0000000001, 1000000], [0, 1000000], [0, 0],
        ]]
        payload["representative_points"]["items"][0]["coordinates"] = [
            1000000, 999999.9999999999,
        ]
        with self.assertRaises(GeographyContractError) as raised:
            evaluate_geography_join(payload)
        self.assertEqual(raised.exception.code, "INVALID_CONTRACT")

    def test_integer_ray_predicates_are_exact_in_both_ring_directions(self) -> None:
        coordinates = [[0, 0], [10_000_000, 9_999_999], [0, 10_000_000], [0, 0]]
        cases = [((9_999_999, 9_999_998), "outside"),  # Exact cross product is -1.
                 ((9_999_999, 9_999_999), "inside"), ((0, 5_000_000), "boundary")]
        with localcontext() as context:
            context.prec = 2  # Geometry must not depend on any ambient Decimal context.
            for ring_coordinates in (coordinates, list(reversed(coordinates))):
                ring = _simple_ring({"type": "Polygon", "coordinates": [ring_coordinates]}, "ring")
                for point, expected in cases:
                    with self.subTest(ring=ring_coordinates, point=point):
                        self.assertEqual(_location(point, ring), expected)

    def test_adjacent_backtracking_edges_are_rejected(self) -> None:
        rings = [
            [[0, 0], [10, 0], [5, 0], [10, 10], [0, 10], [0, 0]],
            [[0, 0], [10, 0], [10, 10], [0, 10], [5, 0], [0, 0]],
            [[0, 0], [10, 0], [5, 0], [0, 0]],
        ]
        for ring in rings:
            with self.subTest(ring=ring):
                payload = copy.deepcopy(self.base)
                payload["geography"]["features"][0]["geometry"]["coordinates"] = [ring]
                with self.assertRaises(GeographyContractError) as raised:
                    evaluate_geography_join(payload)
                self.assertEqual(raised.exception.code, "UNSUPPORTED_GEOMETRY")


if __name__ == "__main__":
    unittest.main()
