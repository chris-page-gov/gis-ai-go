from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_gateway_container as container_check  # noqa: E402


class GatewayContainerCliDiagnosticTests(unittest.TestCase):
    def test_exception_arguments_are_not_converted_to_text(self) -> None:
        class Argument:
            def __str__(self):
                raise RuntimeError("sensitive exception argument must not be inspected")

        self.assertEqual(
            container_check._acceptance_failure_reason(AssertionError(Argument())),
            "assertion_failed",
        )

    def test_unhashable_stage_uses_the_unknown_code(self) -> None:
        self.assertEqual(
            container_check._acceptance_failure_line([], ValueError("private data")),
            "gateway-container-acceptance-failure stage=unknown reason=validation_failed",
        )

    def test_known_assertion_emits_only_fixed_stage_and_reason_codes(self) -> None:
        output = io.StringIO()
        failure = AssertionError("/runner/private/work/provider-token=do-not-print")

        def fail_in_probe(*, _diagnostic_stage: list[str], _cli: bool) -> None:
            _diagnostic_stage[0] = "compose_start_probe"
            raise failure

        with (
            mock.patch.object(container_check, "main", side_effect=fail_in_probe),
            contextlib.redirect_stderr(output),
        ):
            status = container_check.cli_main()

        self.assertEqual(status, 1)
        self.assertEqual(
            output.getvalue(),
            "gateway-container-acceptance-failure "
            "stage=compose_start_probe reason=assertion_failed\n",
        )
        self.assertNotIn("private", output.getvalue())
        self.assertNotIn("provider", output.getvalue())

    def test_unknown_exception_data_is_never_echoed(self) -> None:
        class UnclassifiedFailure(RuntimeError):
            pass

        output = io.StringIO()
        failure = UnclassifiedFailure(
            "Bearer secret /Users/runner/work/private-provider-data"
        )
        with (
            mock.patch.object(container_check, "main", side_effect=failure),
            contextlib.redirect_stderr(output),
        ):
            status = container_check.cli_main()

        self.assertEqual(status, 1)
        self.assertEqual(
            output.getvalue(),
            "gateway-container-acceptance-failure "
            "stage=arguments reason=unknown\n",
        )

    def test_invalid_stage_is_reduced_to_unknown(self) -> None:
        line = container_check._acceptance_failure_line(
            "private/path", RuntimeError("provider data")
        )
        self.assertEqual(
            line,
            "gateway-container-acceptance-failure stage=unknown reason=unknown",
        )

    def test_known_health_timeout_message_maps_to_fixed_code(self) -> None:
        self.assertEqual(
            container_check._acceptance_failure_line(
                "compose_start_probe",
                AssertionError("Docker did not report the gateway container healthy"),
            ),
            "gateway-container-acceptance-failure "
            "stage=compose_start_probe reason=container_health_timeout",
        )

    def test_real_cli_argument_failure_is_sanitised(self) -> None:
        output = io.StringIO()
        argv = ["check_gateway_container.py", "--archive", "/private/provider-token"]
        with (
            mock.patch.object(sys, "argv", argv),
            contextlib.redirect_stderr(output),
        ):
            status = container_check.cli_main()

        self.assertEqual(status, 1)
        self.assertEqual(
            output.getvalue(),
            "gateway-container-acceptance-failure "
            "stage=arguments reason=validation_failed\n",
        )

    def test_real_input_validation_failure_reports_input_stage(self) -> None:
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing-private-image.tar"
            argv = [
                "check_gateway_container.py", "--archive", str(missing),
                "--receipt", str(Path(temporary) / "missing-receipt.json"),
            ]
            with (
                mock.patch.object(sys, "argv", argv),
                contextlib.redirect_stderr(output),
            ):
                status = container_check.cli_main()

        self.assertEqual(status, 1)
        self.assertEqual(
            output.getvalue(),
            "gateway-container-acceptance-failure "
            "stage=input_validation reason=system_call_failed\n",
        )

    def test_library_argument_errors_keep_argparse_system_exit(self) -> None:
        with mock.patch.object(sys, "argv", ["check_gateway_container.py"]):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    container_check.main()
    def test_successful_cli_control_has_no_diagnostic(self) -> None:
        output = io.StringIO()
        with (
            mock.patch.object(container_check, "main", return_value=None),
            contextlib.redirect_stderr(output),
            contextlib.redirect_stdout(output),
        ):
            status = container_check.cli_main()

        self.assertEqual(status, 0)
        self.assertEqual(output.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
