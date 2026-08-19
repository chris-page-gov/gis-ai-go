from __future__ import annotations

import sys
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE))

from gis_ai_go_execution import ExecutionBoundary, StageZeroBoundaryError  # noqa: E402


class ExecutionBoundaryTests(unittest.TestCase):
    def test_identity_is_current(self) -> None:
        boundary = ExecutionBoundary()
        self.assertEqual(boundary.product, "GIS AI GO")
        self.assertFalse(boundary.live_provider_calls)

    def test_execution_fails_closed(self) -> None:
        with self.assertRaisesRegex(StageZeroBoundaryError, "not authorised"):
            ExecutionBoundary().execute("data.query")


if __name__ == "__main__":
    unittest.main()
