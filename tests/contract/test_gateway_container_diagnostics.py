from __future__ import annotations

import hashlib
import io
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from check_gateway_container import (  # noqa: E402
    DOCKER_LOAD_TIMEOUT_SECONDS,
    MAX_DOCKER_LOAD_DIAGNOSTIC_BYTES,
    ROOT as PROJECT_ROOT,
    _DockerLoadStream,
    load_docker_archive,
)


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class FakeProcess:
    def __init__(
        self,
        *,
        stdout: bytes = b"",
        stderr: bytes = b"",
        return_code: int = 0,
        time_out: bool = False,
    ) -> None:
        self.stdout = io.BytesIO(stdout)
        self.stderr = io.BytesIO(stderr)
        self.return_code = return_code
        self.time_out = time_out
        self.wait_timeouts: list[int] = []
        self.killed = False

    def wait(self, *, timeout: int) -> int:
        self.wait_timeouts.append(timeout)
        if self.time_out and len(self.wait_timeouts) == 1:
            raise subprocess.TimeoutExpired(("docker", "load"), timeout)
        return self.return_code

    def kill(self) -> None:
        self.killed = True


class DockerLoadDiagnosticsTests(unittest.TestCase):
    archive = Path("/workspace/gateway-image.tar")

    def assert_exact_invocation(self, mocked_popen: mock.Mock) -> None:
        mocked_popen.assert_called_once_with(
            ("docker", "load", "--input", str(self.archive)),
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def assert_detached(self, error: ValueError) -> None:
        self.assertIsNone(error.__cause__)
        self.assertIsNone(error.__context__)

    def test_success_preserves_exact_command_and_result(self) -> None:
        process = FakeProcess(stdout=b"Loaded image: exact\n")
        with mock.patch(
            "check_gateway_container.subprocess.Popen", return_value=process
        ) as mocked_popen:
            result = load_docker_archive(self.archive)

        self.assertEqual(result.args, ("docker", "load", "--input", str(self.archive)))
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "Loaded image: exact\n")
        self.assertEqual(result.stderr, "")
        self.assertEqual(process.wait_timeouts, [DOCKER_LOAD_TIMEOUT_SECONDS])
        self.assertFalse(process.killed)
        self.assert_exact_invocation(mocked_popen)

    def test_success_text_keeps_a_reviewed_escaped_cpe_readable(self) -> None:
        value = (
            "cpe:2.3:a:\\\\@modelcontextprotocol\\\\/core:"
            "\\\\@modelcontextprotocol\\\\/core:2.0.0:*:*:*:*:*:*:*"
        )
        output = _DockerLoadStream("stdout")
        output.consume(io.BytesIO(value.encode()))
        self.assertEqual(
            output._classification(), ("withheld", "privacy-safe", value)
        )
        self.assertEqual(output.success_text(), value)

    def test_nonzero_is_detached_and_reports_only_fixed_stream_status(self) -> None:
        stdout = b"safe output"
        stderr = b"safe failure"
        process = FakeProcess(stdout=stdout, stderr=stderr, return_code=17)
        with mock.patch(
            "check_gateway_container.subprocess.Popen", return_value=process
        ) as mocked_popen:
            with self.assertRaises(ValueError) as raised:
                load_docker_archive(self.archive)

        message = str(raised.exception)
        self.assertIn("process_status=exit-code process_exit_code=17", message)
        for label, value in (("stdout", stdout), ("stderr", stderr)):
            self.assertNotIn(f"{label}_bytes=", message)
            self.assertNotIn(f"{label}_sha256=", message)
            self.assertNotIn(sha256(value), message)
            self.assertIn(f"{label}_status=withheld", message)
            self.assertIn(f"{label}_reason=privacy-safe", message)
        self.assertNotIn(stdout.decode(), message)
        self.assertNotIn(stderr.decode(), message)
        self.assertNotIn(str(self.archive), message)
        self.assert_detached(raised.exception)
        self.assert_exact_invocation(mocked_popen)

    def test_timeout_is_detached_and_uses_the_fixed_timeout(self) -> None:
        stdout = b"partial output"
        stderr = b"deadline reached"
        process = FakeProcess(stdout=stdout, stderr=stderr, return_code=-9, time_out=True)
        with mock.patch(
            "check_gateway_container.subprocess.Popen", return_value=process
        ) as mocked_popen:
            with self.assertRaises(ValueError) as raised:
                load_docker_archive(self.archive)

        message = str(raised.exception)
        self.assertIn("process_status=timed-out", message)
        self.assertIn(f"timeout_seconds={DOCKER_LOAD_TIMEOUT_SECONDS}", message)
        for label, value in (("stdout", stdout), ("stderr", stderr)):
            self.assertNotIn(f"{label}_bytes=", message)
            self.assertNotIn(f"{label}_sha256=", message)
            self.assertNotIn(sha256(value), message)
            self.assertIn(f"{label}_status=withheld", message)
            self.assertIn(f"{label}_reason=privacy-safe", message)
            self.assertNotIn(value.decode(), message)
        self.assertNotIn(str(self.archive), message)
        self.assertTrue(process.killed)
        self.assertEqual(process.wait_timeouts, [DOCKER_LOAD_TIMEOUT_SECONDS, 10])
        self.assert_detached(raised.exception)
        self.assert_exact_invocation(mocked_popen)

    def test_oserror_is_detached_without_reflecting_the_raw_exception(self) -> None:
        raw_error = (
            "permission denied for /" + "Users/example/private/gateway-image.tar"
        )
        with mock.patch(
            "check_gateway_container.subprocess.Popen", side_effect=OSError(raw_error)
        ) as mocked_popen:
            with self.assertRaises(ValueError) as raised:
                load_docker_archive(self.archive)

        message = str(raised.exception)
        self.assertIn("process_status=start-failed", message)
        self.assertIn("stdout_status=unavailable stdout_reason=no-captured-output", message)
        self.assertIn("stderr_status=unavailable stderr_reason=no-captured-output", message)
        self.assertNotIn("_bytes=", message)
        self.assertNotIn("_sha256=", message)
        self.assertNotIn(raw_error, message)
        self.assertNotIn(str(self.archive), message)
        self.assert_detached(raised.exception)
        self.assert_exact_invocation(mocked_popen)

    def test_unsafe_and_overbound_streams_are_classified_without_reflection(self) -> None:
        cases = (
            (b"open /" + b"home/runner/work/repo/gateway-image.tar", "private-path"),
            (b"failed,/" + b"home/runner/work/private", "private-path"),
            (b"https://host.invalid/" + b"Users/alice/private", "private-path"),
            (b"file://build-agent/" + b"home/runner/work", "private-path"),
            (("\\\\build-agent\\" + "Users\\alice\\project").encode(), "private-path"),
            (
                ("\\\\build-agent\\C$\\" + "Users\\alice\\project").encode(),
                "private-path",
            ),
            (
                (
                    "\\\\?\\UNC\\build-agent\\share\\"
                    + "Users\\alice\\project"
                ).encode(),
                "private-path",
            ),
            (("\\\\build-agent\\share\\project\\file").encode(), "private-path"),
            (("\\\\wsl$\\Ubuntu\\home\\alice\\project").encode(), "private-path"),
            (
                ("\\\\?\\UNC\\build-agent\\share\\project\\file").encode(),
                "private-path",
            ),
            (("D:\\build\\checkout\\file").encode(), "private-path"),
            (b"file://build-agent/share/project", "private-path"),
            (b"file://[2001:db8::1]/share/project", "private-path"),
            (b"file:/srv/private", "private-path"),
            (b"//build-agent/share/project/file", "private-path"),
            (b"//build-agent\\share\\project\\file", "private-path"),
            (b"/usr/../" + b"home/alice/project", "private-path"),
            (b"/../etc/" + b"passwd", "private-path"),
            (("/" + "a/" * 1025 + "../private").encode(), "private-path"),
            (("\\\\.\\C:\\build\\file").encode(), "private-path"),
            (
                (
                    "\\\\?\\Volume{12345678-1234-1234-1234-123456789abc}"
                    "\\Users\\alice\\private"
                ).encode(),
                "private-path",
            ),
            (("/home/" + "álîcé/work").encode(), "private-path"),
            (("C:\\Users\\" + "álîcé\\project").encode(), "private-path"),
            (("/mnt/c/" + "Users/alice/project").encode(), "private-path"),
            (b"SSH_PRIVATE_" + b"KEY_B64=not-for-diagnostics", "sensitive"),
            (
                b"OPENAI_API_" + b"KEY_BASE64_ENCODED_VALUE=hunter22",
                "sensitive",
            ),
            (b"PRIVATE_" + b"KEYS=hunter22", "sensitive"),
            (b"SSH_PRIVATE_" + b"KEY_PKCS12=hunter22", "sensitive"),
            (
                b"cpe:2.3:a:vendor:ENCRYPTION_"
                + b"KEY:hunter22:*:*:*:*:*:*:*",
                "sensitive",
            ),
            (
                b"cpe:2.3:a:vendor:product:1.0:pass"
                + b"word:hunter2:*:*:*:*:*",
                "sensitive",
            ),
            (b"xapp-1-" + b"A" * 32, "sensitive"),
            (b"github_\n" + b"pat_" + b"A" * 24, "sensitive"),
            (b"github_\\n" + b"pat_" + b"A" * 24, "sensitive"),
            (b"github_%0A" + b"pat_" + b"A" * 24, "sensitive"),
            (b"github_\\f" + b"pat_" + b"A" * 24, "sensitive"),
            (("github_\u2029" + "pat_" + "A" * 24).encode(), "sensitive"),
            (("-----BEGIN\u2028PRIVATE KEY-----").encode(), "sensitive"),
            (b"Basic Zm9vOmJhcg==", "sensitive"),
            (
                b'log payload={"key"/*comment*/:"ENCRYPTION_KEY",'
                b'"value":"hunter22",}',
                "sensitive",
            ),
            (
                b'log payload={"P'
                + b"!" * 512
                + b'ASSWORD":"hunter22",}',
                "sensitive",
            ),
            (b"https://:hunter2@example.invalid/path", "sensitive"),
            (b"PASSWORD=[redacted] hunter22", "sensitive"),
            (b"pass" + b"word[value]=hunter22", "sensitive"),
            (b"PASS" + b"WORD=${PASSWORD}foo=bar", "sensitive"),
            (b"A" * 160 + b"_PASS" + b"WORD=hunter2", "sensitive"),
            (b'"' + b"A" * 160 + b'_PASSWORD":"hunter2"', "sensitive"),
            (b"Authorization: Bearer x", "sensitive"),
            (b"Authorization=Bearer x", "sensitive"),
            (b"HTTP_" + b"AUTHORIZATION=Bearer x", "sensitive"),
            (b"headers[" + b"Authorization]=Bearer x", "sensitive"),
            (b"Authorization: Negotiate hunter22", "sensitive"),
            (b"request.Authorization=Negotiate hunter2", "sensitive"),
            (b"config[pass%77ord][value]=hunter22", "sensitive"),
            (
                b'{"properties":[{"name":"ENCRYPTION_'
                + b'KEY","value":"x"}]}',
                "sensitive",
            ),
            (
                b"eyJhbGciOiJSUzI1NiJ9." + b"B" * 4097 + b"." + b"C" * 342,
                "over-bound",
            ),
            (b"https://example.invalid/?token[]=hunter22", "sensitive"),
            (b"https://example.invalid/?token[0]=x", "sensitive"),
            (b"https://example.invalid/?token%5Bvalue%5D=x", "sensitive"),
            (b"https://example.invalid/?token[0][value]=x", "sensitive"),
            (b"https://example.invalid/?service_token[]=x", "sensitive"),
            (b"//user:hunter22@example.invalid/path", "sensitive"),
            (b"--pass" + b"word hunter22", "sensitive"),
            (b"clientSecret=not-for-diagnostics", "sensitive"),
            (b"password=hunter22", "sensitive"),
            (b"unsafe\x1b[31moutput", "unsafe-control"),
            (b"invalid-utf8-\xff", "invalid-utf8"),
            (b"x" * (MAX_DOCKER_LOAD_DIAGNOSTIC_BYTES + 1), "over-bound"),
            (b"\xff" * (1024 * 1024), "over-bound"),
        )
        for payload, reason in cases:
            with self.subTest(reason=reason):
                process = FakeProcess(stderr=payload, return_code=1)
                with mock.patch(
                    "check_gateway_container.subprocess.Popen", return_value=process
                ):
                    with self.assertRaises(ValueError) as raised:
                        load_docker_archive(self.archive)

                message = str(raised.exception)
                self.assertNotIn("stderr_bytes=", message)
                self.assertNotIn("stderr_sha256=", message)
                self.assertNotIn(sha256(payload), message)
                self.assertIn(f"stderr_status=withheld stderr_reason={reason}", message)
                decoded = payload.decode("utf-8", errors="ignore")
                if decoded:
                    self.assertNotIn(decoded, message)
                self.assertNotIn(str(self.archive), message)
                self.assert_detached(raised.exception)

    def test_unsafe_success_output_fails_closed(self) -> None:
        payload = b"Loaded image: exact\nclient_secret=must-not-escape"
        process = FakeProcess(stdout=payload)
        with mock.patch(
            "check_gateway_container.subprocess.Popen", return_value=process
        ):
            with self.assertRaises(ValueError) as raised:
                load_docker_archive(self.archive)

        message = str(raised.exception)
        self.assertIn("process_status=invalid-success-output", message)
        self.assertNotIn("stdout_bytes=", message)
        self.assertNotIn("stdout_sha256=", message)
        self.assertNotIn(sha256(payload), message)
        self.assertIn("stdout_reason=sensitive", message)
        self.assertNotIn(payload.decode(), message)
        self.assert_detached(raised.exception)


if __name__ == "__main__":
    unittest.main()
