"""Synthetic credential handling tests; never inspect the real user's secrets."""
from __future__ import annotations

import errno
import io
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/okf_plus"))
import os_credentials as credentials

KEY = "synthetic-file-key-keep-private"


class CredentialTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.home = Path(self.temporary.name)
        self.directory = self.home / ".secrets"
        self.directory.mkdir(mode=0o700)
        self.key_file = self.directory / "os_api_key"
        self.key_file.write_bytes(KEY.encode() + b"\r\n\n")
        self.key_file.chmod(0o600)

    def load(self, **options):
        return credentials.load_os_key(environ=options.pop("environ", {}), home=self.home, **options)

    def test_private_file_fallback_trims_trailing_newlines_without_executing_ai_env(self):
        marker = self.home / "should-not-exist"
        (self.directory / "ai.env").write_text(f"touch {marker}\nOS_API_KEY=wrong\n")
        self.assertEqual(self.load(), KEY)
        self.assertFalse(marker.exists())

    def test_environment_wins_without_reading_any_secret_file(self):
        with mock.patch.object(credentials.os, "open", side_effect=AssertionError("file must not be opened")):
            self.assertEqual(self.load(environ={"OS_API_KEY": "synthetic-env-key"}), "synthetic-env-key")
            self.assertEqual(credentials.load_os_key("CUSTOM_OS_KEY", environ={"CUSTOM_OS_KEY": KEY}), KEY)

    def test_explicit_custom_environment_variable_does_not_fall_back(self):
        with self.assertRaisesRegex(credentials.CredentialError, "^credential-missing$"):
            self.load(key_env="CUSTOM_OS_KEY")
        with self.assertRaisesRegex(credentials.CredentialError, "^credential-missing$"):
            self.load(allow_file=False)

    def test_invalid_environment_does_not_silently_use_file(self):
        for key in ("", " ", KEY + "\n", KEY + "\x00", KEY + "\t", "x" * 513, "caf\u00e9"):
            with self.subTest(key_length=len(key)), self.assertRaisesRegex(credentials.CredentialError, "^credential-invalid$"):
                self.load(environ={"OS_API_KEY": key})

    def test_blank_control_embedded_newline_and_oversized_files_rejected(self):
        for raw in (b"\n\r\n", b" ", b"a\nb", b"a\x00b", b"a\tb", b"x" * 513,
                    b"x" + b"\n" * credentials.MAX_FILE_BYTES, b"\xff"):
            self.key_file.write_bytes(raw)
            with self.subTest(length=len(raw)), self.assertRaisesRegex(credentials.CredentialError, "^credential-invalid$"):
                self.load()

    def test_parent_and_file_permissions_must_be_private(self):
        for path, permissions in ((self.directory, 0o755), (self.key_file, 0o644), (self.key_file, 0o400)):
            expected = 0o700 if path == self.directory else 0o600
            path.chmod(permissions)
            with self.subTest(mode=permissions), self.assertRaisesRegex(credentials.CredentialError, "^credential-file-unsafe$"):
                self.load()
            path.chmod(expected)

    def test_foreign_owner_is_rejected(self):
        with mock.patch.object(credentials.os, "geteuid", return_value=os.geteuid() + 1):
            with self.assertRaisesRegex(credentials.CredentialError, "^credential-file-unsafe$"):
                self.load()
        original_stat = os.fstat
        calls = 0
        def foreign_file(descriptor):
            nonlocal calls
            value = original_stat(descriptor)
            calls += 1
            if calls == 2:
                fields = list(value)
                fields[4] = os.geteuid() + 1
                return os.stat_result(fields)
            return value
        with mock.patch.object(credentials.os, "fstat", side_effect=foreign_file):
            with self.assertRaisesRegex(credentials.CredentialError, "^credential-file-unsafe$"):
                self.load()

    def test_file_and_parent_symlinks_are_rejected(self):
        target = self.home / "other-key"
        self.key_file.rename(target)
        self.key_file.symlink_to(target)
        with self.assertRaisesRegex(credentials.CredentialError, "^credential-file-unsafe$"):
            self.load()
        self.key_file.unlink()
        target.rename(self.key_file)
        relocated = self.home / "other-directory"
        self.directory.rename(relocated)
        self.directory.symlink_to(relocated, target_is_directory=True)
        with self.assertRaisesRegex(credentials.CredentialError, "^credential-file-unsafe$"):
            self.load()

    def test_fifo_is_rejected_without_blocking(self):
        self.key_file.unlink()
        os.mkfifo(self.key_file, 0o600)
        with self.assertRaisesRegex(credentials.CredentialError, "^credential-file-unsafe$"):
            self.load()

    def test_missing_key_does_not_read_ai_env_and_errors_omit_path_and_values(self):
        self.key_file.unlink()
        (self.directory / "ai.env").write_text("=".join(("OS_API_KEY", KEY)))
        output = io.StringIO()
        with mock.patch("sys.stdout", output), mock.patch("sys.stderr", output):
            status = credentials.credential_status(environ={}, home=self.home)
        self.assertEqual(status, "credential-missing")
        self.assertEqual(output.getvalue(), "")
        with mock.patch.object(credentials.os, "open", side_effect=OSError(errno.EIO, KEY, str(self.key_file))):
            self.assertEqual(credentials.credential_status(environ={}, home=self.home), "credential-unavailable")

    def test_read_remains_bounded_when_file_grows_after_stat(self):
        lengths = []
        def growing(_descriptor, limit):
            lengths.append(limit)
            return b"x" * limit
        with mock.patch.object(credentials.os, "read", side_effect=growing):
            with self.assertRaisesRegex(credentials.CredentialError, "^credential-invalid$"):
                self.load()
        self.assertEqual(sum(lengths), credentials.MAX_FILE_BYTES + 1)


if __name__ == "__main__":
    unittest.main()
