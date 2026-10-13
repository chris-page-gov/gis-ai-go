from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import gateway_image as image  # noqa: E402
import node_runtime_advisory as node  # noqa: E402
import run_gateway_image_assurance as assurance  # noqa: E402
import scan_gateway_image as scan  # noqa: E402


class NodeInventorySizeDiagnosticsTests(unittest.TestCase):
    def setUp(self):
        self.measurements = {
            "metadata_bytes": 100,
            "database_bytes": image.MAX_GRYPE_DB_EXPANDED_BYTES,
            "expanded_bytes": image.MAX_GRYPE_DB_EXPANDED_BYTES + 100,
            "maximum_bytes": image.MAX_GRYPE_DB_EXPANDED_BYTES,
        }
        self.line = image.node_inventory_size_diagnostic(self.measurements)
        self.assertIsNotNone(self.line)

    def test_measurements_require_closed_consistent_bounded_integers(self):
        invalid = [None, [], {**self.measurements, "private": "hidden"},
                   {key: value for key, value in self.measurements.items()
                    if key != "metadata_bytes"}]
        for key in self.measurements:
            for value in (True, "123", 1.0, -1, 2**63):
                invalid.append({**self.measurements, key: value})
        invalid += [{**self.measurements, "metadata_bytes": 0},
                    {**self.measurements, "expanded_bytes": 100},
                    {**self.measurements, "maximum_bytes": 1}]
        for value in invalid:
            with self.subTest(value=value):
                self.assertIsNone(image.node_inventory_size_diagnostic(value))
                with self.assertRaises(ValueError):
                    if value is not None:
                        node.NodeAdvisoryFailure("node-db-inventory-expanded-bound",
                                                 inventory_sizes=value)
                    else:
                        node.NodeAdvisoryFailure("node-db-inventory-read",
                                                 inventory_sizes=self.measurements)

    def test_parser_rejects_malformed_duplicate_and_noncanonical_lines(self):
        self.assertEqual(assurance._node_inventory_size_diagnostic(self.line), self.line)
        for text in (
            self.line + "\n" + self.line,
            self.line + "\nnode_db_inventory_sizes malformed",
            self.line + "\nnode_db_inventory_sizes",
            self.line.replace("metadata_bytes=100", "metadata_bytes=0100"),
            self.line.replace("metadata_bytes=100", "metadata_bytes=" + "9" * 100),
            self.line + " private=hidden",
            self.line.replace("metadata_bytes=100", "metadata_bytes=101"),
        ):
            with self.subTest(text=text):
                self.assertIsNone(assurance._node_inventory_size_diagnostic(text))

    def test_cli_serialises_only_checked_scalars_and_detaches_exit(self):
        failure = node.NodeAdvisoryFailure("node-db-inventory-expanded-bound",
                                           inventory_sizes=self.measurements)
        stdout, stderr = io.StringIO(), io.StringIO()
        with (mock.patch.object(scan, "main", side_effect=failure),
              contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr),
              self.assertRaises(SystemExit) as raised):
            scan.cli()
        self.assertEqual(raised.exception.code, 115)
        self.assertIsNone(raised.exception.__context__)
        self.assertIsNone(raised.exception.__cause__)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), self.line + "\n")

    def run_child(self, *, phase="vulnerability-scan", code=115, stdout=b"",
                  stderr=None, timeout=None, overflow=False):
        if stderr is None:
            stderr = (self.line + "\n").encode()
        command = (f"import os,sys,time;os.write(1,{stdout!r});"
                   f"os.write(2,{stderr!r});")
        if overflow:
            command += f"sys.stdout.buffer.write(b'x'*{assurance.MAX_PHASE_OUTPUT_BYTES + 1});sys.stdout.flush();"
        if timeout is not None:
            command += "time.sleep(5);"
        command += f"sys.exit({code})"
        output = io.StringIO()
        kwargs = {} if timeout is None else {"timeout_seconds": timeout}
        with (contextlib.redirect_stdout(output), contextlib.redirect_stderr(output),
              self.assertRaises(ValueError) as raised):
            assurance.run_checked(phase, [sys.executable, "-c", command], **kwargs)
        self.assertIsNone(raised.exception.__context__)
        return output.getvalue()

    def test_parent_projects_sizes_only_for_correct_failed_phase_and_code(self):
        rendered = self.run_child(stderr=("unretained public text\n" + self.line + "\n").encode())
        self.assertIn("failure_stage=node-db-inventory-expanded-bound", rendered)
        self.assertEqual(rendered.count(self.line), 1)
        self.assertNotIn("unretained public text", rendered)
        for kwargs in ({"phase": "sbom"}, {"code": 102}, {"code": 125},
                       {"timeout": 0.1}, {"stdout": (self.line + "\n").encode()}):
            with self.subTest(kwargs=kwargs):
                self.assertNotIn(self.line, self.run_child(**kwargs))
        overflow = self.run_child(overflow=True)
        self.assertIn("output_reason=over-bound", overflow)
        self.assertNotIn(self.line, overflow)

    def test_private_malformed_or_duplicate_output_cannot_publish_measurements(self):
        for payload in (b"Bearer SYNTHETIC-SECRET", b"/home/synthetic/private.txt",
                        b"::warning::synthetic", b"\xff", b"\0"):
            for stream in ("stdout", "stderr"):
                kwargs = ({"stdout": payload} if stream == "stdout" else
                          {"stderr": payload + b"\n" + (self.line + "\n").encode()})
                with self.subTest(stream=stream, payload=payload):
                    rendered = self.run_child(**kwargs)
                    self.assertNotIn(self.line, rendered)
                    self.assertNotIn("SYNTHETIC-SECRET", rendered)
                    self.assertNotIn("/home/synthetic/private.txt", rendered)
        for extra in (self.line, "node_db_inventory_sizes malformed"):
            with self.subTest(extra=extra):
                rendered = self.run_child(stderr=(self.line + "\n" + extra + "\n").encode())
                self.assertNotIn(self.line, rendered)


if __name__ == "__main__":
    unittest.main()
