from __future__ import annotations

import builtins
import copy
import os
import sqlite3
import subprocess
import sys
import threading
import unittest
import urllib.request
from datetime import timedelta
from pathlib import Path
from unittest import mock

SOURCE = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE))

from gis_ai_go_execution import (  # noqa: E402
    EXECUTION_PARAMETERS_DOMAIN,
    EXECUTION_RESULT_DATA_DOMAIN,
    ExecutionFailure,
    ExecutionService,
    canonical_json_bytes,
    sha256_identity,
    strict_json_loads,
)

from fixtures import FIXED_NOW, expected_result, valid_request  # noqa: E402


class ExecutionServiceTests(unittest.TestCase):
    def service(self, **options: object) -> ExecutionService:
        return ExecutionService(clock=lambda: FIXED_NOW, **options)

    def assert_failure(self, request: object, code: str, **options: object) -> None:
        with self.assertRaises(ExecutionFailure) as raised:
            self.service().execute(request, **options)
        self.assertEqual(code, raised.exception.code)

    def test_identical_inputs_produce_byte_identical_canonical_results_and_evidence(self) -> None:
        request = valid_request()
        first = self.service().execute(copy.deepcopy(request))
        second = self.service().execute(copy.deepcopy(request))
        self.assertEqual(expected_result(), first)
        self.assertEqual(canonical_json_bytes(first), canonical_json_bytes(second))
        self.assertEqual(first["evidence"], second["evidence"])

    def test_domain_separated_rfc8785_digests_match_the_gateway_vectors(self) -> None:
        value = {
            "negative_zero": -0.0,
            "fixed_small": 1e-6,
            "exponent_small": 1e-7,
            "exponent_large": 1e30,
            "decimal": 333333333.33333329,
            "integer": 9_007_199_254_740_991,
            "unicode": "Café 😀",
        }
        self.assertEqual(
            (
                b'{"decimal":333333333.3333333,"exponent_large":1e+30,'
                b'"exponent_small":1e-7,"fixed_small":0.000001,'
                b'"integer":9007199254740991,"negative_zero":0,'
                b'"unicode":"Caf\xc3\xa9 \xf0\x9f\x98\x80"}'
            ),
            canonical_json_bytes(value),
        )
        self.assertEqual(
            "sha256:4afb2bfe5ee293d98a8525f34418c79011251e30f94a8dfecac0fb93e3841a48",
            sha256_identity(EXECUTION_PARAMETERS_DOMAIN, value),
        )
        self.assertEqual(
            "sha256:f89af91ec033f5d1c6e04dfbf66ac8af8624b7dcc43c33290ef48ef040b70502",
            sha256_identity(EXECUTION_RESULT_DATA_DOMAIN, dict(reversed(value.items()))),
        )

    def test_trace_and_provider_native_source_rights_survive_the_round_trip(self) -> None:
        request = valid_request()
        result = self.service().execute(request)
        self.assertEqual(request["trace"], result["trace"])
        self.assertEqual(request["parameters"]["source"], result["evidence"]["source"])
        self.assertEqual("none", result["evidence"]["transformation"]["geometry_repair"])
        self.assertEqual(
            "none",
            result["evidence"]["transformation"]["geometry_simplification"],
        )

    def test_unknown_operations_parameters_and_fields_fail_closed_without_reflection(self) -> None:
        malicious = "provider.execute /tmp/private.db SELECT secret FROM users"
        for mutation, code in (
            (("operation", malicious), "UNKNOWN_OPERATION"),
            (("unexpected", malicious), "INVALID_REQUEST"),
            (("parameters", "unexpected", malicious), "INVALID_REQUEST"),
            (("gateway_authorisation", "unexpected", malicious), "INVALID_REQUEST"),
        ):
            request = valid_request()
            target = request
            for key in mutation[:-2]:
                target = target[key]
            target[mutation[-2]] = mutation[-1]
            with self.subTest(mutation=mutation):
                with self.assertRaises(ExecutionFailure) as raised:
                    self.service().execute(request)
                problem = raised.exception.as_problem()
                self.assertEqual(code, problem["code"])
                self.assertNotIn(malicious, canonical_json_bytes(problem).decode("utf-8"))

    def test_source_crs_and_axis_order_are_exact_allowlists(self) -> None:
        for path, value, code in (
            (("parameters", "fixture_id"), "other", "SOURCE_MISMATCH"),
            (("parameters", "source", "version"), "2.0.0", "SOURCE_MISMATCH"),
            (("parameters", "crs"), "EPSG:3857", "INVALID_CRS"),
            (("parameters", "axis_order"), "latitude-longitude", "INVALID_AXIS_ORDER"),
        ):
            request = valid_request()
            target = request
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            with self.subTest(path=path):
                self.assert_failure(request, code)

    def test_malformed_and_self_intersecting_geometry_fail_without_repair(self) -> None:
        mutations = (
            {"type": "Point", "coordinates": [-1, 52]},
            {"type": "Polygon", "coordinates": [[[-4, 50], [0, 50], [0, 54], [-4, 54]]]},
            {
                "type": "Polygon",
                "coordinates": [[[-4, 50], [0, 54], [-4, 54], [0, 50], [-4, 50]]],
            },
            {
                "type": "Polygon",
                "coordinates": [[[-4, 50], [-4, 50], [0, 54], [-4, 54], [-4, 50]]],
            },
        )
        for geometry in mutations:
            request = valid_request()
            request["parameters"]["geometry"] = geometry
            with self.subTest(geometry=geometry):
                self.assert_failure(request, "INVALID_GEOMETRY")

    def test_coordinate_feature_byte_complexity_and_output_limits_are_enforced(self) -> None:
        excessive_coordinates = valid_request()
        excessive_coordinates["parameters"]["geometry"]["coordinates"] = [
            [[-4 + index / 1000, 50] for index in range(128)] + [[-4, 50]]
        ]
        self.assert_failure(excessive_coordinates, "LIMIT_EXCEEDED")

        excessive_features = valid_request()
        excessive_features["parameters"]["limit"] = 11
        self.assert_failure(excessive_features, "LIMIT_EXCEEDED")

        excessive_complexity = valid_request()
        excessive_complexity["limits"]["max_complexity"] = 16
        self.assert_failure(excessive_complexity, "LIMIT_EXCEEDED")

        excessive_raw_bytes = valid_request()
        excessive_raw_bytes["limits"]["max_input_bytes"] = 1024
        self.assert_failure(excessive_raw_bytes, "LIMIT_EXCEEDED", raw_size=1025)

        small_output = valid_request()
        small_output["limits"]["max_output_bytes"] = 1024
        self.assert_failure(small_output, "OUTPUT_LIMIT_EXCEEDED")

    def test_expired_and_excessive_deadlines_are_bounded(self) -> None:
        expired = valid_request()
        expired["deadline"] = (FIXED_NOW - timedelta(seconds=1)).isoformat()
        self.assert_failure(expired, "DEADLINE_EXCEEDED")

        excessive = valid_request()
        excessive["deadline"] = (FIXED_NOW + timedelta(seconds=31)).isoformat()
        self.assert_failure(excessive, "LIMIT_EXCEEDED")

        non_canonical = valid_request()
        non_canonical["deadline"] = "2026-08-20 12:00:10+00:00"
        self.assert_failure(non_canonical, "INVALID_REQUEST")

        times = iter((FIXED_NOW, FIXED_NOW + timedelta(seconds=11)))
        service = ExecutionService(clock=lambda: next(times))
        with self.assertRaises(ExecutionFailure) as raised:
            service.execute(valid_request())
        self.assertEqual("DEADLINE_EXCEEDED", raised.exception.code)

    def test_cooperative_cancellation_interrupts_an_active_execution(self) -> None:
        started = threading.Event()
        resume = threading.Event()

        def checkpoint(_request_id: str, index: int) -> None:
            if index == 0:
                started.set()
                self.assertTrue(resume.wait(timeout=2))

        service = self.service(checkpoint=checkpoint)
        failures: list[ExecutionFailure] = []

        def execute() -> None:
            try:
                service.execute(valid_request())
            except ExecutionFailure as failure:
                failures.append(failure)

        worker = threading.Thread(target=execute)
        worker.start()
        self.assertTrue(started.wait(timeout=2))
        self.assertTrue(service.cancel("exec-202-example"))
        resume.set()
        worker.join(timeout=2)
        self.assertFalse(worker.is_alive())
        self.assertEqual(["EXECUTION_CANCELLED"], [failure.code for failure in failures])
        self.assertFalse(service.cancel("exec-202-example"))

    def test_execution_reaches_no_url_path_sql_shell_eval_or_dynamic_code_surface(self) -> None:
        forbidden = AssertionError("forbidden capability reached")
        with (
            mock.patch.object(builtins, "open", side_effect=forbidden),
            mock.patch.object(builtins, "eval", side_effect=forbidden),
            mock.patch.object(builtins, "exec", side_effect=forbidden),
            mock.patch.object(os, "system", side_effect=forbidden),
            mock.patch.object(sqlite3, "connect", side_effect=forbidden),
            mock.patch.object(subprocess, "run", side_effect=forbidden),
            mock.patch.object(urllib.request, "urlopen", side_effect=forbidden),
        ):
            self.assertEqual(expected_result(), self.service().execute(valid_request()))

    def test_strict_json_rejects_duplicates_nonfinite_values_and_bad_unicode(self) -> None:
        for payload in (
            b'{"a":1,"a":2}',
            b'{"value":NaN}',
            b'\xff',
            b'{"value":"\\ud800"}',
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    strict_json_loads(payload)


if __name__ == "__main__":
    unittest.main()
