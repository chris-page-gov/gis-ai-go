from __future__ import annotations

import sys
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE))

from gis_ai_go_execution import ExecutionBoundary, ExecutionService  # noqa: E402

from fixtures import FIXED_NOW, expected_result, valid_request  # noqa: E402


class ExecutionBoundaryTests(unittest.TestCase):
    def test_identity_is_current(self) -> None:
        boundary = ExecutionBoundary()
        self.assertEqual(boundary.product, "GIS AI GO")
        self.assertFalse(boundary.live_provider_calls)
        self.assertFalse(boundary.end_user_authentication)
        self.assertFalse(boundary.policy_authority)
        self.assertFalse(boundary.public_ingress)
        self.assertEqual(("fixture.features.query",), boundary.operations)

    def test_boundary_runs_only_the_typed_synthetic_operation(self) -> None:
        boundary = ExecutionBoundary(_executor=ExecutionService(clock=lambda: FIXED_NOW))
        self.assertEqual(expected_result(), boundary.execute(valid_request()))


if __name__ == "__main__":
    unittest.main()
