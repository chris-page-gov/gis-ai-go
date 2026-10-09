"""Bound hidden tar metadata before stdlib processing; never extract payloads."""

from __future__ import annotations

import tarfile

MAX_EXTENSION_BYTES = 64 * 1024
MAX_EXTENSION_TOTAL = 64 * 1024 * 1024
MAX_EXTENSION_HEADERS = 100_000
MAX_EXTENSION_DEPTH = 16
MAX_PAX_ATTRIBUTES = 128
MAX_PAX_STATE_BYTES = 64 * 1024


def _check_pax(headers: dict[str, str]) -> None:
    if len(headers) > MAX_PAX_ATTRIBUTES:
        raise tarfile.ReadError("tar metadata attribute count exceeds limit")
    size = 0
    for key, value in headers.items():
        size += len(key.encode("utf-8", "surrogateescape")) + len(value.encode("utf-8", "surrogateescape")) + 2
        if size > MAX_PAX_STATE_BYTES:
            raise tarfile.ReadError("tar metadata state exceeds byte limit")


class BoundedTarInfo(tarfile.TarInfo):
    """Resource limits independent of a caller's path and metadata policy.

    ReadError deliberately bypasses TarFile.next's permissive HeaderError/EOF
    handling. Ordinary bounded GNU/PAX metadata and opaque xattrs remain valid.
    """

    @classmethod
    def fromtarfile(cls, archive):
        try:
            return super().fromtarfile(archive)
        except (tarfile.EmptyHeaderError, tarfile.TruncatedHeaderError, tarfile.InvalidHeaderError) as error:
            raise tarfile.ReadError("invalid or truncated tar header") from error

    def _proc_member(self, archive):
        _check_pax(archive.pax_headers)
        if self.type == tarfile.GNUTYPE_SPARSE:
            raise tarfile.ReadError("sparse tar metadata is unsupported")
        extensions = (tarfile.XHDTYPE, tarfile.XGLTYPE, tarfile.SOLARIS_XHDTYPE,
                      tarfile.GNUTYPE_LONGNAME, tarfile.GNUTYPE_LONGLINK)
        if self.type not in extensions:
            return super()._proc_member(archive)
        # Check the signed size before _block can raise a swallowable header error.
        if not 0 <= self.size <= MAX_EXTENSION_BYTES:
            raise tarfile.ReadError("tar extension exceeds byte limit")
        padded = self._block(self.size)
        count = getattr(archive, "_bounded_extension_count", 0) + 1
        total = getattr(archive, "_bounded_extension_bytes", 0) + tarfile.BLOCKSIZE + padded
        depth = getattr(archive, "_bounded_extension_depth", 0) + 1
        if padded > MAX_EXTENSION_BYTES or total > MAX_EXTENSION_TOTAL or count > MAX_EXTENSION_HEADERS:
            raise tarfile.ReadError("tar extensions exceed aggregate limit")
        if depth > MAX_EXTENSION_DEPTH:
            raise tarfile.ReadError("tar extension nesting exceeds limit")
        archive._bounded_extension_count = count
        archive._bounded_extension_bytes = total
        archive._bounded_extension_depth = depth
        try:
            return super()._proc_member(archive)
        finally:
            archive._bounded_extension_depth -= 1

    def _apply_pax_info(self, headers, encoding, errors):
        _check_pax(headers)
        if (any(key.startswith("GNU.sparse.") or key in ("SCHILY.realsize", "SCHILY.holesdata") for key in headers)
                or headers.get("SCHILY.filetype") == "sparse"):
            raise tarfile.ReadError("sparse tar metadata is unsupported")
        return super()._apply_pax_info(headers, encoding, errors)

    def _proc_gnusparse_00(self, *args):
        raise tarfile.ReadError("sparse tar metadata is unsupported")

    def _proc_gnusparse_01(self, *args):
        raise tarfile.ReadError("sparse tar metadata is unsupported")

    def _proc_gnusparse_10(self, *args):
        raise tarfile.ReadError("sparse tar metadata is unsupported")
