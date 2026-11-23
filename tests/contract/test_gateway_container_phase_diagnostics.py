from __future__ import annotations

import contextlib
import io
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import run_gateway_image_assurance as assurance

LINE = "gateway-container-acceptance-failure stage=compose_start_probe reason=container_health_timeout"


class ContainerPhaseDiagnosticTests(unittest.TestCase):
    def test_only_one_closed_diagnostic_line_is_parsed(self):
        self.assertEqual(assurance._container_acceptance_diagnostic(LINE), LINE)
        for value in (LINE + " private/path", LINE + "\n" + LINE,
                      LINE.replace("compose_start_probe", "private_path"),
                      LINE.replace("container_health_timeout", "private_reason"),
                      LINE.replace("stage=", "stage=/private/")):
            self.assertIsNone(assurance._container_acceptance_diagnostic(value))

    def invoke_failure(self, phase, stderr, stdout=""):
        command = "import sys;sys.stdout.write(" + repr(stdout) + ");sys.stderr.write(" + repr(stderr) + ");sys.exit(1)"
        captured = io.StringIO()
        with (contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured),
              self.assertRaises(ValueError)):
            assurance.run_checked(phase, [sys.executable, "-c", command])
        return captured.getvalue()

    def test_real_failed_subprocess_retains_failure_and_exposes_the_closed_code(self):
        output = self.invoke_failure("container-acceptance", LINE + "\n")
        self.assertEqual(output.count(LINE), 1)
        self.assertIn("output withheld", output)

    def test_private_or_ambiguous_streams_do_not_forward_diagnostics(self):
        for phase, stderr, stdout in (
            ("foreign-phase", LINE + "\n", ""),
            ("container-acceptance", LINE + "\nBearer SYNTHETIC-PRIVATE-VALUE", ""),
            ("container-acceptance", LINE + "\n" + LINE, ""),
            ("container-acceptance", LINE + "\n", LINE + "\n"),
        ):
            output = self.invoke_failure(phase, stderr, stdout)
            self.assertNotIn(LINE, output)
            self.assertNotIn("SYNTHETIC-PRIVATE-VALUE", output)


if __name__ == "__main__":
    unittest.main()
