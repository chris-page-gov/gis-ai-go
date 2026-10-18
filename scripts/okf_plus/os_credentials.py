"""Read the explicitly configured OS credential without executing secret files.

OS_API_KEY takes precedence. Only when that default variable is absent can the
dedicated ~/.secrets/os_api_key file supply the key. An explicitly selected
different environment variable remains environment-only. No ai.env, shell
profile, neighbouring file or generic dotenv source is read or executed.
"""
from __future__ import annotations

import errno
import os
from pathlib import Path
import re
import stat

MAX_KEY_BYTES = 512
MAX_FILE_BYTES = 1024


class CredentialError(ValueError):
    """Fixed error codes contain neither paths nor credential values."""

    def __init__(self, code):
        self.code = code
        super().__init__(code)


def _validate(value):
    if (not isinstance(value, str) or not 1 <= len(value) <= MAX_KEY_BYTES
            or any(not 33 <= ord(character) <= 126 for character in value)):
        raise CredentialError("credential-invalid")
    return value


def load_os_key(key_env="OS_API_KEY", *, environ=None, home=None, allow_file=True):
    """Return one key in memory; do not print, persist, log or fetch anything.

    The fallback directory must be owned by the effective current user with
    exact 0700 permissions; its regular, non-symlink key file must have the same
    owner and exact 0600 permissions. Descriptor-relative access binds the file
    to the checked directory. Reads are bounded, including trailing newlines.
    ``home`` and ``environ`` are injection seams for synthetic offline tests.
    """
    if not isinstance(key_env, str) or re.fullmatch(r"[A-Z_][A-Z_0-9]{0,99}", key_env) is None:
        raise CredentialError("credential-invalid")
    environment = os.environ if environ is None else environ
    if key_env in environment:
        # An invalid explicitly configured value must not silently select a
        # different credential. Environment values may not contain line breaks.
        return _validate(environment[key_env])
    if not allow_file or key_env != "OS_API_KEY":
        raise CredentialError("credential-missing")

    directory_descriptor = file_descriptor = None
    try:
        directory = (Path.home() if home is None else Path(home)) / ".secrets"
        directory_descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        directory_stat = os.fstat(directory_descriptor)
        if (not stat.S_ISDIR(directory_stat.st_mode) or directory_stat.st_uid != os.geteuid()
                or stat.S_IMODE(directory_stat.st_mode) != 0o700):
            raise CredentialError("credential-file-unsafe")
        # NONBLOCK prevents a malicious FIFO from blocking before fstat rejects
        # it. A regular file is checked before reading any of its contents.
        file_descriptor = os.open("os_api_key", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC,
                                  dir_fd=directory_descriptor)
        file_stat = os.fstat(file_descriptor)
        if (not stat.S_ISREG(file_stat.st_mode) or file_stat.st_uid != os.geteuid()
                or stat.S_IMODE(file_stat.st_mode) != 0o600):
            raise CredentialError("credential-file-unsafe")
        if file_stat.st_size > MAX_FILE_BYTES:
            raise CredentialError("credential-invalid")
        raw = bytearray()
        while len(raw) <= MAX_FILE_BYTES:
            block = os.read(file_descriptor, MAX_FILE_BYTES + 1 - len(raw))
            if not block:
                break
            raw.extend(block)
        if len(raw) > MAX_FILE_BYTES:
            raise CredentialError("credential-invalid")
        try:
            value = raw.rstrip(b"\r\n").decode("ascii")
        except UnicodeError:
            raise CredentialError("credential-invalid") from None
        return _validate(value)
    except FileNotFoundError:
        raise CredentialError("credential-missing") from None
    except OSError as error:
        code = "credential-file-unsafe" if error.errno in (errno.ELOOP, errno.ENOTDIR, errno.EACCES, errno.EPERM) else "credential-unavailable"
        raise CredentialError(code) from None
    except (RuntimeError, TypeError):
        raise CredentialError("credential-unavailable") from None
    finally:
        if file_descriptor is not None:
            os.close(file_descriptor)
        if directory_descriptor is not None:
            os.close(directory_descriptor)


def credential_status(key_env="OS_API_KEY", *, environ=None, home=None, allow_file=True):
    """Return presence/validation status only; never include key, source or path."""
    try:
        load_os_key(key_env, environ=environ, home=home, allow_file=allow_file)
    except CredentialError as error:
        return error.code
    return "credential-present"
