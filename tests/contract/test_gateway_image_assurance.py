from __future__ import annotations

import contextlib
import hashlib
import io
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import run_gateway_image_assurance as assurance  # noqa: E402


class GatewayImageAssurancePromotionTests(unittest.TestCase):
    @staticmethod
    def phase(name: str, _arguments: list[str]) -> dict[str, object]:
        return {
            "name": name,
            "started_at": "2026-08-21T00:00:00Z",
            "completed_at": "2026-08-21T00:00:01Z",
            "duration_ms": 1_000,
            "passed": True,
        }

    def invoke(self, root: Path) -> None:
        with (
            mock.patch.object(assurance, "ROOT", root),
            mock.patch.object(
                sys,
                "argv",
                ["run_gateway_image_assurance.py"],
            ),
        ):
            assurance.main()

    def test_promotes_only_after_complete_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            final = root / "artifacts" / "gateway"
            observed_directories: list[Path] = []

            def verify(name: str, arguments: list[str], **_kwargs: object) -> None:
                self.assertEqual(name, "final-verification")
                directory = Path(arguments[arguments.index("--directory") + 1])
                observed_directories.append(directory)
                self.assertTrue(directory.is_dir())
                self.assertTrue(directory.name.startswith(".gateway-quarantine-"))
                self.assertFalse(final.exists())

            with (
                mock.patch.object(assurance, "run_phase", side_effect=self.phase),
                mock.patch.object(assurance, "write_evidence_manifest"),
                mock.patch.object(assurance, "run_checked", side_effect=verify),
            ):
                self.invoke(root)

            self.assertEqual(len(observed_directories), 1)
            self.assertTrue(final.is_dir())
            self.assertEqual(list((root / "artifacts").glob(".gateway-quarantine-*")), [])

    def test_phase_manifest_and_verifier_failures_leave_no_publishable_directory(self) -> None:
        failures = ("phase", "manifest", "verifier")
        for failure in failures:
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                final = root / "artifacts" / "gateway"
                run_phase = mock.Mock(side_effect=self.phase)
                manifest = mock.Mock()
                verifier = mock.Mock()
                if failure == "phase":
                    run_phase.side_effect = ValueError("fixed phase failure")
                elif failure == "manifest":
                    manifest.side_effect = ValueError("fixed manifest failure")
                else:
                    verifier.side_effect = ValueError("fixed verifier failure")

                with (
                    mock.patch.object(assurance, "run_phase", run_phase),
                    mock.patch.object(assurance, "write_evidence_manifest", manifest),
                    mock.patch.object(assurance, "run_checked", verifier),
                    self.assertRaises(ValueError),
                ):
                    self.invoke(root)

                self.assertFalse(final.exists())
                artifacts = root / "artifacts"
                self.assertEqual(list(artifacts.glob(".gateway-quarantine-*")), [])

    def test_symlinked_artifact_root_is_rejected_before_external_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            root = parent / "repository"
            outside = parent / "outside"
            root.mkdir()
            outside.mkdir()
            external_gateway = outside / "gateway"
            external_gateway.mkdir()
            sentinel = external_gateway / "keep.txt"
            sentinel.write_text("external\n")
            (root / "artifacts").symlink_to(outside, target_is_directory=True)

            with self.assertRaisesRegex(ValueError, "must be a real directory"):
                self.invoke(root)

            self.assertEqual(sentinel.read_text(), "external\n")
            self.assertTrue((root / "artifacts").is_symlink())

    def test_artifact_root_identity_change_is_rejected_before_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            final = root / "artifacts" / "gateway"
            final.mkdir(parents=True)
            sentinel = final / "keep.txt"
            sentinel.write_text("existing\n")

            with (
                mock.patch.object(
                    assurance,
                    "_directory_identity",
                    side_effect=((1, 1), (2, 2)),
                ),
                self.assertRaisesRegex(ValueError, "identity changed"),
            ):
                self.invoke(root)

            self.assertEqual(sentinel.read_text(), "existing\n")

    def test_phase_time_artifact_root_swap_stops_before_the_next_phase(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            root = parent / "repository"
            root.mkdir()
            outside = parent / "outside"
            outside.mkdir()
            sentinel = outside / "keep.txt"
            sentinel.write_text("external\n")
            phases: list[str] = []

            def swap_root(name: str, _arguments: list[str]) -> dict[str, object]:
                phases.append(name)
                artifacts = root / "artifacts"
                artifacts.rename(root / "artifacts-old")
                artifacts.symlink_to(outside, target_is_directory=True)
                return self.phase(name, _arguments)

            with (
                mock.patch.object(assurance, "run_phase", side_effect=swap_root),
                self.assertRaisesRegex(ValueError, "must be a real directory"),
            ):
                self.invoke(root)

            self.assertEqual(phases, ["okf"])
            self.assertEqual(sentinel.read_text(), "external\n")
            self.assertTrue((root / "artifacts").is_symlink())
            self.assertFalse((outside / "gateway").exists())

    def test_group_writable_artifact_root_is_rejected_before_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifacts = root / "artifacts"
            final = artifacts / "gateway"
            final.mkdir(parents=True)
            sentinel = final / "keep.txt"
            sentinel.write_text("existing\n")
            artifacts.chmod(0o775)

            with self.assertRaisesRegex(ValueError, "group or world writable"):
                self.invoke(root)

            self.assertEqual(sentinel.read_text(), "existing\n")

    def test_quarantine_mode_change_is_rejected_before_the_next_phase(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            phases: list[str] = []

            def weaken_quarantine(
                name: str, arguments: list[str]
            ) -> dict[str, object]:
                phases.append(name)
                quarantine = next((root / "artifacts").glob(".gateway-quarantine-*"))
                quarantine.chmod(0o755)
                return self.phase(name, arguments)

            with (
                mock.patch.object(assurance, "run_phase", side_effect=weaken_quarantine),
                self.assertRaisesRegex(ValueError, "identity changed"),
            ):
                self.invoke(root)

            self.assertEqual(phases, ["okf"])
            self.assertFalse((root / "artifacts" / "gateway").exists())

    def test_checked_phase_replays_privacy_safe_output(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        command = (
            "import os;"
            "os.write(1,b'privacy-safe stdout https://example.invalid/path\\n');"
            "os.write(2,b'privacy-safe stderr\\n')"
        )
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            assurance.run_checked("fixture", [sys.executable, "-c", command])
        self.assertEqual(
            stdout.getvalue(),
            "privacy-safe stdout https://example.invalid/path\n"
            + assurance.PHASE_OUTPUT_BOUNDARY,
        )
        self.assertEqual(
            stderr.getvalue(),
            "privacy-safe stderr\n" + assurance.PHASE_OUTPUT_BOUNDARY,
        )

    def test_phase_output_keeps_a_reviewed_escaped_cpe_readable(self) -> None:
        value = (
            "cpe:2.3:a:\\\\@modelcontextprotocol\\\\/core:"
            "\\\\@modelcontextprotocol\\\\/core:2.0.0:*:*:*:*:*:*:*"
        )
        output = assurance._PhaseOutput("stdout")
        output.consume(io.BytesIO(value.encode()))
        self.assertEqual(output.classification(), ("readable", "privacy-safe", value))

    def test_checked_phase_frames_successive_safe_replays(self) -> None:
        console = io.StringIO()
        commands = (
            "import os;os.write(1,b':')",
            "import os;os.write(1,b':stop-commands::gateway-token')",
        )
        with contextlib.redirect_stdout(console), contextlib.redirect_stderr(console):
            for command in commands:
                assurance.run_checked("fixture", [sys.executable, "-c", command])
        expected = (
            ":\n"
            + assurance.PHASE_OUTPUT_BOUNDARY
            + ":stop-commands::gateway-token\n"
            + assurance.PHASE_OUTPUT_BOUNDARY
        )
        self.assertEqual(console.getvalue(), expected)
        self.assertFalse(
            any(line.startswith("::") for line in console.getvalue().splitlines())
        )
        credential_console = io.StringIO()
        with (
            contextlib.redirect_stdout(credential_console),
            contextlib.redirect_stderr(credential_console),
        ):
            assurance.run_checked(
                "fixture",
                [sys.executable, "-c", "import os;os.write(1,b'client_sec')"],
            )
            assurance.run_checked(
                "fixture",
                [sys.executable, "-c", "import os;os.write(1,b'ret=hunter22')"],
            )
        self.assertEqual(
            credential_console.getvalue(),
            "client_sec\n"
            + assurance.PHASE_OUTPUT_BOUNDARY
            + "ret=hunter22\n"
            + assurance.PHASE_OUTPUT_BOUNDARY,
        )
        self.assertEqual(
            assurance.prohibited_phase_transcript_reason("name:password\n"),
            "malformed-boundary",
        )
        self.assertNotIn("client_secret=hunter22", credential_console.getvalue())

        token_console = io.StringIO()
        with (
            contextlib.redirect_stdout(token_console),
            contextlib.redirect_stderr(token_console),
        ):
            assurance.run_checked(
                "fixture",
                [sys.executable, "-c", "import os;os.write(1,b'ghp_AAAAAAAA')"],
            )
            assurance.run_checked(
                "fixture",
                [sys.executable, "-c", "import os;os.write(1,b'BBBBBBBBBBBBBBBBBBBB')"],
            )
        self.assertIsNone(
            assurance.prohibited_phase_transcript_reason(token_console.getvalue())
        )
        self.assertNotIn(
            "ghp_AAAAAAAA" + "BBBBBBBBBBBBBBBBBBBB",
            token_console.getvalue(),
        )

        alias_console = io.StringIO()
        with (
            contextlib.redirect_stdout(alias_console),
            contextlib.redirect_stderr(alias_console),
        ):
            assurance.run_checked(
                "fixture",
                [sys.executable, "-c", "import os;os.write(1,b'name:password')"],
            )
            assurance.run_checked(
                "fixture",
                [sys.executable, "-c", "import os;os.write(1,b'value:hunter2')"],
            )
        self.assertIsNone(
            assurance.prohibited_phase_transcript_reason(alias_console.getvalue())
        )

    def test_checked_phase_withholds_safe_text_on_a_nonzero_exit(self) -> None:
        payload = b"benign-looking failure detail"
        command = f"import os,sys;os.write(1,{payload!r});sys.exit(7)"
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            self.assertRaisesRegex(ValueError, "exited unsuccessfully") as raised,
        ):
            assurance.run_checked("fixture", [sys.executable, "-c", command])
        rendered = stdout.getvalue() + stderr.getvalue() + str(raised.exception)
        self.assertNotIn(payload.decode(), rendered)
        self.assertNotIn(f"stdout_bytes={len(payload)}", rendered)
        self.assertNotIn("stdout_bytes=", rendered)
        self.assertNotIn("stdout_sha256=", rendered)
        self.assertNotIn(hashlib.sha256(payload).hexdigest(), rendered)
        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)

    def test_checked_phase_maps_only_the_reserved_database_acquisition_exit(self) -> None:
        private_prefix = "/" + "home/runner"
        payload = (
            b"Bearer SHOULD-NOT-BE-REPLAYED "
            + f"{private_prefix}/work/private".encode()
        )
        command = (
            "import os,sys;"
            f"os.write(2,{payload!r});"
            f"sys.exit({assurance.TRIVY_DB_ACQUISITION_EXIT_CODE})"
        )
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            self.assertRaisesRegex(
                ValueError, "failed during Trivy database acquisition"
            ) as raised,
        ):
            assurance.run_checked(
                "vulnerability-scan", [sys.executable, "-c", command]
            )
        rendered = stdout.getvalue() + stderr.getvalue() + str(raised.exception)
        self.assertIn("failure_stage=trivy-db-acquisition", rendered)
        self.assertIn(
            f"attempted_registry_count={len(assurance.TRIVY_DB_REPOSITORIES)}",
            rendered,
        )
        self.assertNotIn(payload.decode(), rendered)
        self.assertNotIn("Bearer", rendered)
        self.assertNotIn(private_prefix, rendered)

        unrelated = io.StringIO()
        with (
            contextlib.redirect_stdout(unrelated),
            contextlib.redirect_stderr(unrelated),
            self.assertRaisesRegex(ValueError, "exited unsuccessfully"),
        ):
            assurance.run_checked("fixture", [sys.executable, "-c", command])
        self.assertNotIn("failure_stage=trivy-db-acquisition", unrelated.getvalue())

    def test_checked_phase_maps_only_the_reserved_donor_acquisition_exit(self) -> None:
        private_prefix = "/" + "home/runner"
        payload = (
            b"Bearer SHOULD-NOT-BE-REPLAYED "
            + f"{private_prefix}/work/private".encode()
        )
        command = (
            "import os,sys;"
            f"os.write(2,{payload!r});"
            f"sys.exit({assurance.RUNTIME_LIBRARY_DONOR_ACQUISITION_EXIT_CODE})"
        )
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            self.assertRaisesRegex(
                ValueError, "failed during runtime-library donor acquisition"
            ) as raised,
        ):
            assurance.run_checked(
                "vulnerability-scan", [sys.executable, "-c", command]
            )
        rendered = stdout.getvalue() + stderr.getvalue() + str(raised.exception)
        self.assertIn("failure_stage=runtime-library-donor-acquisition", rendered)
        self.assertNotIn(payload.decode(), rendered)
        self.assertNotIn("Bearer", rendered)
        self.assertNotIn(private_prefix, rendered)

        unrelated = io.StringIO()
        with (
            contextlib.redirect_stdout(unrelated),
            contextlib.redirect_stderr(unrelated),
            self.assertRaisesRegex(ValueError, "exited unsuccessfully"),
        ):
            assurance.run_checked("fixture", [sys.executable, "-c", command])
        self.assertNotIn(
            "failure_stage=runtime-library-donor-acquisition",
            unrelated.getvalue(),
        )

    def test_checked_phase_maps_only_the_reserved_donor_validation_exit(self) -> None:
        private_prefix = "/" + "home/runner"
        payload = (
            b"Bearer SHOULD-NOT-BE-REPLAYED "
            + f"{private_prefix}/work/private".encode()
        )
        command = (
            "import os,sys;"
            f"os.write(2,{payload!r});"
            f"sys.exit({assurance.RUNTIME_LIBRARY_DONOR_VALIDATION_EXIT_CODE})"
        )
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            self.assertRaisesRegex(
                ValueError, "failed during runtime-library donor validation"
            ) as raised,
        ):
            assurance.run_checked(
                "vulnerability-scan", [sys.executable, "-c", command]
            )
        rendered = stdout.getvalue() + stderr.getvalue() + str(raised.exception)
        self.assertIn("failure_stage=runtime-library-donor-validation", rendered)
        self.assertNotIn(payload.decode(), rendered)
        self.assertNotIn("Bearer", rendered)
        self.assertNotIn(private_prefix, rendered)

        unrelated = io.StringIO()
        with (
            contextlib.redirect_stdout(unrelated),
            contextlib.redirect_stderr(unrelated),
            self.assertRaisesRegex(ValueError, "exited unsuccessfully"),
        ):
            assurance.run_checked("fixture", [sys.executable, "-c", command])
        self.assertNotIn(
            "failure_stage=runtime-library-donor-validation",
            unrelated.getvalue(),
        )

    def test_checked_phase_withholds_safe_text_on_timeout(self) -> None:
        payload = b"benign-looking timeout detail"
        command = f"import os,time;os.write(1,{payload!r});time.sleep(10)"
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            self.assertRaisesRegex(ValueError, "timed out") as raised,
        ):
            assurance.run_checked(
                "fixture",
                [sys.executable, "-c", command],
                timeout_seconds=0.05,
            )
        rendered = stdout.getvalue() + stderr.getvalue() + str(raised.exception)
        self.assertNotIn(payload.decode(), rendered)
        self.assertNotIn(f"stdout_bytes={len(payload)}", rendered)
        self.assertNotIn("stdout_bytes=", rendered)
        self.assertNotIn("stdout_sha256=", rendered)
        self.assertNotIn(hashlib.sha256(payload).hexdigest(), rendered)
        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)

    def test_checked_phase_classifies_streams_together_before_replay(self) -> None:
        stdout_payload = b"client_" + b"secret="
        stderr_payload = b"hunter22"
        command = (
            "import os;"
            f"os.write(1,{stdout_payload!r});os.write(2,{stderr_payload!r})"
        )
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            self.assertRaisesRegex(ValueError, "emitted prohibited output") as raised,
        ):
            assurance.run_checked("fixture", [sys.executable, "-c", command])
        rendered = stdout.getvalue() + stderr.getvalue() + str(raised.exception)
        self.assertNotIn(stdout_payload.decode(), rendered)
        self.assertNotIn(stderr_payload.decode(), rendered)
        self.assertIn("output_reason=sensitive", rendered)
        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)

    def test_checked_phase_classifies_the_exact_combined_replay(self) -> None:
        stdout_payload = b"client_sec"
        stderr_payload = b"ret=hunter22"
        command = (
            "import os;"
            f"os.write(1,{stdout_payload!r});os.write(2,{stderr_payload!r})"
        )
        console = io.StringIO()
        with (
            contextlib.redirect_stdout(console),
            contextlib.redirect_stderr(console),
            self.assertRaisesRegex(ValueError, "emitted prohibited output") as raised,
        ):
            assurance.run_checked("fixture", [sys.executable, "-c", command])
        rendered = console.getvalue() + str(raised.exception)
        self.assertNotIn("client_secret=hunter22", rendered)
        self.assertIn("output_reason=sensitive", rendered)
        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)

        marker = assurance.PRIVACY_PHASE_OUTPUT_BOUNDARY.encode()
        command = (
            "import os;"
            f"os.write(1,{marker[:12]!r});os.write(2,{marker[12:]!r})"
        )
        console = io.StringIO()
        with (
            contextlib.redirect_stdout(console),
            contextlib.redirect_stderr(console),
            self.assertRaisesRegex(ValueError, "emitted prohibited output") as raised,
        ):
            assurance.run_checked("fixture", [sys.executable, "-c", command])
        self.assertIn("output_reason=reserved-boundary", console.getvalue())
        self.assertNotIn(assurance.PRIVACY_PHASE_OUTPUT_BOUNDARY, console.getvalue())

    def test_checked_phase_rejects_runner_commands_and_boundary_split_secrets(self) -> None:
        boundary_payload = (
            b"x" * (assurance.PHASE_OUTPUT_CHUNK_BYTES - 1)
            + b" Bearer abcdefghijklmnop"
        )
        fixtures = (
            (b"::stop-commands::gateway-token\n", "workflow-command"),
            (assurance.PHASE_OUTPUT_BOUNDARY.encode(), "reserved-boundary"),
            (boundary_payload, "sensitive"),
            (b"github_\n" + b"pat_" + b"A" * 24 + b"\n", "sensitive"),
            (b"github_\n\n" + b"pat_" + b"A" * 24 + b"\n", "sensitive"),
            (b"github_\\\n" + b"pat_" + b"A" * 24 + b"\n", "sensitive"),
            (b"github_\\n" + b"pat_" + b"A" * 24 + b"\n", "sensitive"),
            (b"github_%0A" + b"pat_" + b"A" * 24 + b"\n", "sensitive"),
            (b"github_\\f" + b"pat_" + b"A" * 24 + b"\n", "sensitive"),
            (b"github_\\x0b" + b"pat_" + b"A" * 24 + b"\n", "sensitive"),
            (b"github_\\x0c" + b"pat_" + b"A" * 24 + b"\n", "sensitive"),
            (b"github_\\x85" + b"pat_" + b"A" * 24 + b"\n", "sensitive"),
            (b"github_\\b" + b"pat_" + b"A" * 24 + b"\n", "sensitive"),
            (b"github_\\0" + b"pat_" + b"A" * 24 + b"\n", "sensitive"),
            (
                ("github_\u2028" + "pat_" + "A" * 24 + "\n").encode(),
                "sensitive",
            ),
            (b"-----BEGIN\n " + b"PRIVATE KEY-----\n", "sensitive"),
            (("-----BEGIN\u2028PRIVATE KEY-----\n").encode(), "sensitive"),
            (b"Basic Zm9vOmJhcg==\n", "sensitive"),
            (b"Basic 6TpwYXNz\n", "sensitive"),
            (b"Basic OoA\n", "sensitive"),
            (b"Basic OgA\n", "sensitive"),
            (b"Basic OuKAqA\n", "sensitive"),
            (b"%FF%67%68%70%5F" + b"A" * 24 + b"\n", "sensitive"),
            (
                b'log payload={"key"/*comment*/:"ENCRYPTION_KEY",'
                b'"value":"hunter22",}\n',
                "sensitive",
            ),
            (
                b'log payload={"key":"PRIVATE_KEY",/* } */'
                b'"value":"hunter22",}\n',
                "sensitive",
            ),
            (
                (
                    'log payload={"key":"PRIVATE_KEY",// comment\u2028'
                    '"value":"hunter22",}\n'
                ).encode(),
                "sensitive",
            ),
            (
                b'log payload={/* "key":"PRIVATE_KEY",'
                b'"value":"hunter22" */}\n',
                "sensitive",
            ),
            (
                b"log payload={'message':'{\"key\":\"PRIVATE_KEY\","
                b"\"value\":\"hunter22\"}',}\n",
                "sensitive",
            ),
            (b"{'''password''':'''hunter22'''}\n", "sensitive"),
            (
                b'log payload={"P'
                + b"!" * 512
                + b'ASSWORD":"hunter22",}\n',
                "sensitive",
            ),
            (b"{name:PRIVATE_KEY,note:\",value:hunter22}\n", "sensitive"),
        )
        for payload, reason in fixtures:
            stdout = io.StringIO()
            stderr = io.StringIO()
            command = f"import os;os.write(1,{payload!r})"
            with (
                self.subTest(reason=reason),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
                self.assertRaisesRegex(ValueError, "emitted prohibited output") as raised,
            ):
                assurance.run_checked("fixture", [sys.executable, "-c", command])
            rendered = stdout.getvalue() + stderr.getvalue() + str(raised.exception)
            self.assertNotIn(payload[-24:].decode(), rendered)
            self.assertIn(f"output_reason={reason}", rendered)
            self.assertNotIn("stdout_bytes=", rendered)
            self.assertNotIn("stdout_sha256=", rendered)
            self.assertNotIn(hashlib.sha256(payload).hexdigest(), rendered)
            self.assertIsNone(raised.exception.__cause__)
            self.assertIsNone(raised.exception.__context__)

    def test_checked_phase_replays_safe_jsonc_without_comment_flattening(self) -> None:
        payloads = (
            b'{"url":"a//b",/*note*/"password":"${PASSWORD}"}\n',
            b'{"password":"${PASSWORD}"/*note*/}\n',
            b'{"password":"[redacted]"//note\n}\n',
            b'{"a":"x"//comment\n,/*note*/"b":"y"}\n',
            b'{"regex":"\\\\d+"}\n',
            b'{"message":"literal \\\\n marker"}\n',
        )
        for payload in payloads:
            stdout = io.StringIO()
            with self.subTest(payload=payload), contextlib.redirect_stdout(stdout):
                assurance.run_checked(
                    "fixture",
                    [sys.executable, "-c", f"import os;os.write(1,{payload!r})"],
                )
            self.assertEqual(
                stdout.getvalue(), payload.decode() + assurance.PHASE_OUTPUT_BOUNDARY
            )

    def test_checked_phase_hostile_outputs_are_withheld_for_every_exit_path(self) -> None:
        private = b"password=hunter22"
        secret = b"Bearer abcdefghijklmnop"
        commands = (
            (
                "success",
                (
                    "import os;"
                    f"os.write(1,{private!r});os.write(2,{secret!r})"
                ),
                5.0,
                "gateway image assurance phase fixture emitted prohibited output",
            ),
            (
                "failure",
                (
                    "import os,sys;"
                    f"os.write(1,{private!r});os.write(2,{secret!r});sys.exit(7)"
                ),
                5.0,
                "gateway image assurance phase fixture exited unsuccessfully",
            ),
            (
                "timeout",
                (
                    "import os,time;"
                    f"os.write(1,{private!r});os.write(2,{secret!r});time.sleep(10)"
                ),
                0.05,
                "gateway image assurance phase fixture timed out",
            ),
        )
        for label, command, timeout, expected in commands:
            stdout = io.StringIO()
            stderr = io.StringIO()
            with (
                self.subTest(label=label),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
                self.assertRaisesRegex(ValueError, expected) as raised,
            ):
                assurance.run_checked(
                    "fixture",
                    [sys.executable, "-c", command],
                    timeout_seconds=timeout,
                )
            rendered = stdout.getvalue() + stderr.getvalue() + str(raised.exception)
            self.assertNotIn(private.decode(), rendered)
            self.assertNotIn(secret.decode(), rendered)
            self.assertNotIn("stdout_bytes=", rendered)
            self.assertNotIn("stdout_sha256=", rendered)
            self.assertNotIn(hashlib.sha256(private).hexdigest(), rendered)
            self.assertNotIn("stderr_bytes=", rendered)
            self.assertNotIn("stderr_sha256=", rendered)
            self.assertNotIn(hashlib.sha256(secret).hexdigest(), rendered)
            self.assertIsNone(raised.exception.__cause__)
            self.assertIsNone(raised.exception.__context__)

    def test_checked_phase_start_error_is_fixed_and_detached(self) -> None:
        private = "/home/" + "runner/work/private/nonexistent-command"
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            self.assertRaisesRegex(
                ValueError,
                "gateway image assurance phase fixture could not be started",
            ) as raised,
        ):
            assurance.run_checked("fixture", [private])
        rendered = stdout.getvalue() + stderr.getvalue() + str(raised.exception)
        self.assertNotIn(private, rendered)
        self.assertNotIn("stdout_bytes=", rendered)
        self.assertNotIn("stdout_sha256=", rendered)
        self.assertNotIn("stderr_bytes=", rendered)
        self.assertNotIn("stderr_sha256=", rendered)
        self.assertIn("process-start-failed", rendered)
        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)

    def test_checked_phase_streams_concurrently_and_enforces_the_binary_bound(self) -> None:
        size = assurance.MAX_PHASE_OUTPUT_BYTES + 1
        command = (
            "import sys;"
            f"sys.stdout.buffer.write(b'A'*{size});sys.stdout.buffer.flush();"
            f"sys.stderr.buffer.write(b'B'*{size});sys.stderr.buffer.flush()"
        )
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            self.assertRaisesRegex(ValueError, "emitted prohibited output") as raised,
        ):
            assurance.run_checked(
                "fixture", [sys.executable, "-c", command], timeout_seconds=5
            )
        rendered = stdout.getvalue() + stderr.getvalue() + str(raised.exception)
        self.assertNotIn("A" * 64, rendered)
        self.assertNotIn("B" * 64, rendered)
        self.assertNotIn("stdout_bytes=", rendered)
        self.assertNotIn("stdout_sha256=", rendered)
        self.assertNotIn("stderr_bytes=", rendered)
        self.assertNotIn("stderr_sha256=", rendered)
        self.assertIn("stdout_reason=over-bound", rendered)
        self.assertIn("stderr_reason=over-bound", rendered)
        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)

    def test_checked_phase_accepts_the_exact_binary_bound(self) -> None:
        size = assurance.MAX_PHASE_OUTPUT_BYTES
        command = f"import os;os.write(1,b'A'*{size})"
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            assurance.run_checked(
                "fixture", [sys.executable, "-c", command], timeout_seconds=5
            )
        self.assertEqual(
            len(stdout.getvalue()), size + 1 + len(assurance.PHASE_OUTPUT_BOUNDARY)
        )
        self.assertTrue(stdout.getvalue().endswith(assurance.PHASE_OUTPUT_BOUNDARY))
        self.assertEqual(set(stdout.getvalue()[:size]), {"A"})
        self.assertEqual(stderr.getvalue(), "")

    def test_checked_phase_withholds_invalid_utf8(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            self.assertRaisesRegex(ValueError, "emitted prohibited output") as raised,
        ):
            assurance.run_checked(
                "fixture",
                [sys.executable, "-c", "import os;os.write(1,b'\\xff')"],
            )
        rendered = stdout.getvalue() + stderr.getvalue() + str(raised.exception)
        self.assertNotIn("stdout_bytes=", rendered)
        self.assertNotIn("stdout_sha256=", rendered)
        self.assertIn("stdout_reason=invalid-utf8", rendered)
        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)

    def test_checked_phase_withholds_terminal_control_characters(self) -> None:
        fixtures = (b"safe\x00text", b"\x1b[31mred", "safe\u202etext".encode())
        for payload in fixtures:
            stdout = io.StringIO()
            stderr = io.StringIO()
            command = f"import os;os.write(1,{payload!r})"
            with (
                self.subTest(payload=payload),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
                self.assertRaisesRegex(ValueError, "emitted prohibited output") as raised,
            ):
                assurance.run_checked("fixture", [sys.executable, "-c", command])
            rendered = stdout.getvalue() + stderr.getvalue() + str(raised.exception)
            self.assertIn("stdout_reason=unsafe-control", rendered)
            self.assertNotIn("safe\u202e", rendered)
            self.assertNotIn("[31mred", rendered)
            self.assertIsNone(raised.exception.__cause__)
            self.assertIsNone(raised.exception.__context__)

    def test_checked_phase_fails_closed_when_a_descendant_holds_the_pipes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            marker = Path(temporary) / "late-descendant-write"
            descendant = (
                "import time;from pathlib import Path;time.sleep(0.5);"
                f"Path({str(marker)!r}).write_text('unsafe')"
            )
            command = (
                "import subprocess,sys;"
                f"subprocess.Popen([sys.executable,'-c',{descendant!r}])"
            )
            stdout = io.StringIO()
            stderr = io.StringIO()
            with (
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
                self.assertRaisesRegex(ValueError, "could not be completed") as raised,
            ):
                assurance.run_checked("fixture", [sys.executable, "-c", command])
            rendered = stdout.getvalue() + stderr.getvalue() + str(raised.exception)
            self.assertIn("output_reason=could-not-be-completed", rendered)
            self.assertNotIn(str(marker), rendered)
            time.sleep(0.6)
            self.assertFalse(marker.exists())
            self.assertIsNone(raised.exception.__cause__)
            self.assertIsNone(raised.exception.__context__)

    def test_checked_phase_timeout_terminates_descendants(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            marker = Path(temporary) / "late-timeout-write"
            descendant = (
                "import time;from pathlib import Path;time.sleep(0.5);"
                f"Path({str(marker)!r}).write_text('unsafe')"
            )
            command = (
                "import subprocess,sys,time;"
                f"subprocess.Popen([sys.executable,'-c',{descendant!r}]);"
                "time.sleep(10)"
            )
            console = io.StringIO()
            with (
                contextlib.redirect_stdout(console),
                contextlib.redirect_stderr(console),
                self.assertRaisesRegex(ValueError, "timed out") as raised,
            ):
                assurance.run_checked(
                    "fixture",
                    [sys.executable, "-c", command],
                    timeout_seconds=0.05,
                )
            rendered = console.getvalue() + str(raised.exception)
            self.assertIn("output_reason=timed-out", rendered)
            self.assertNotIn(str(marker), rendered)
            time.sleep(0.6)
            self.assertFalse(marker.exists())
            self.assertIsNone(raised.exception.__cause__)
            self.assertIsNone(raised.exception.__context__)

    def test_checked_phase_rejects_an_untrusted_phase_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "phase name is invalid") as raised:
            assurance.run_checked("fixture\n::warning::forged", [sys.executable])
        self.assertIsNone(raised.exception.__cause__)
        self.assertIsNone(raised.exception.__context__)

    def test_preexisting_final_symlink_is_unlinked_before_a_failed_phase(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifacts = root / "artifacts"
            artifacts.mkdir()
            final = artifacts / "gateway"
            external = root / "external"
            external.mkdir()
            marker = external / "marker"
            marker.write_text("preserve")
            final.symlink_to(external, target_is_directory=True)

            with (
                mock.patch.object(
                    assurance,
                    "run_phase",
                    side_effect=ValueError("fixed phase failure"),
                ),
                self.assertRaisesRegex(ValueError, "fixed phase failure"),
            ):
                self.invoke(root)

            self.assertFalse(final.exists())
            self.assertFalse(final.is_symlink())
            self.assertEqual(marker.read_text(), "preserve")
            self.assertEqual(list(artifacts.glob(".gateway-quarantine-*")), [])

    def test_unexpected_final_directory_is_removed_without_promotion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            final = root / "artifacts" / "gateway"

            def create_final(_name: str, _arguments: list[str], **_kwargs: object) -> None:
                final.mkdir()
                (final / "partial").write_text("unsafe")

            with (
                mock.patch.object(assurance, "run_phase", side_effect=self.phase),
                mock.patch.object(assurance, "write_evidence_manifest"),
                mock.patch.object(assurance, "run_checked", side_effect=create_final),
                self.assertRaisesRegex(ValueError, "appeared before verified promotion"),
            ):
                self.invoke(root)

            self.assertFalse(final.exists())
            self.assertEqual(list((root / "artifacts").glob(".gateway-quarantine-*")), [])

    def test_unexpected_final_symlink_is_unlinked_without_following_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            final = root / "artifacts" / "gateway"
            external = root / "external"
            external.mkdir()
            marker = external / "marker"
            marker.write_text("preserve")

            def create_final(_name: str, _arguments: list[str], **_kwargs: object) -> None:
                final.symlink_to(external, target_is_directory=True)

            with (
                mock.patch.object(assurance, "run_phase", side_effect=self.phase),
                mock.patch.object(assurance, "write_evidence_manifest"),
                mock.patch.object(assurance, "run_checked", side_effect=create_final),
                self.assertRaisesRegex(ValueError, "appeared before verified promotion"),
            ):
                self.invoke(root)

            self.assertFalse(final.exists())
            self.assertEqual(marker.read_text(), "preserve")
            self.assertEqual(list((root / "artifacts").glob(".gateway-quarantine-*")), [])


if __name__ == "__main__":
    unittest.main()
