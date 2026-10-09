"""Tiny hostile headers prove rejection before hidden body allocation."""

import gzip
import hashlib
import io
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from security import bounded_tar
from tests.deployment.test_security_image_assurance import runner
import gateway_image
import scan_gateway_image


def header(kind, size):
    item = tarfile.TarInfo("metadata")
    item.type = kind
    item.size = size
    return item.tobuf(format=tarfile.GNU_FORMAT)


class HeaderOnly(io.BytesIO):
    def read(self, size=-1):
        if self.tell() >= tarfile.BLOCKSIZE:
            raise AssertionError("extension body was read before admission")
        return super().read(size)


def pax_record(key, value):
    suffix = f" {key}={value}\n".encode()
    count = len(suffix) + 1
    while count != len(str(count)) + len(suffix):
        count = len(str(count)) + len(suffix)
    return str(count).encode() + suffix


def extension(kind, body):
    return header(kind, len(body)) + body + b"\0" * (-len(body) % 512)


def ordinary():
    item = tarfile.TarInfo("ordinary")
    return item.tobuf() + b"\0" * 1024


class BoundedTarTests(unittest.TestCase):
    def test_all_hidden_extension_types_reject_before_body_read(self):
        for kind in (tarfile.XHDTYPE, tarfile.XGLTYPE, tarfile.SOLARIS_XHDTYPE,
                     tarfile.GNUTYPE_LONGNAME, tarfile.GNUTYPE_LONGLINK):
            for mode in ("r:", "r|"):
                with self.subTest(kind=kind, mode=mode):
                    with self.assertRaisesRegex(tarfile.ReadError, "extension exceeds byte"):
                        tarfile.open(fileobj=HeaderOnly(header(kind, 2**32)), mode=mode,
                                     tarinfo=bounded_tar.BoundedTarInfo)

    def test_negative_hidden_size_is_not_silently_eof(self):
        raw = header(tarfile.REGTYPE, 0) + header(tarfile.XHDTYPE, -1)
        with self.assertRaisesRegex(tarfile.ReadError, "extension exceeds byte"):
            with tarfile.open(fileobj=io.BytesIO(raw), mode="r:", tarinfo=bounded_tar.BoundedTarInfo) as archive:
                list(archive)

    def test_extension_nesting_and_aggregate_budgets(self):
        raw = extension(tarfile.GNUTYPE_LONGNAME, b"ordinary\0")
        with self.assertRaisesRegex(tarfile.ReadError, "nesting"):
            tarfile.open(fileobj=io.BytesIO(raw * 17 + ordinary()), mode="r:", tarinfo=bounded_tar.BoundedTarInfo)
        for setting, value in (("MAX_EXTENSION_HEADERS", 1), ("MAX_EXTENSION_TOTAL", 1023)):
            with self.subTest(setting=setting), patch.object(bounded_tar, setting, value):
                with self.assertRaisesRegex(tarfile.ReadError, "aggregate"):
                    tarfile.open(fileobj=io.BytesIO(raw * 2 + ordinary()), mode="r:", tarinfo=bounded_tar.BoundedTarInfo)

    def test_accumulated_global_pax_and_sparse_maps_are_bounded(self):
        raw = b""
        for index in range(129):
            raw += extension(tarfile.XGLTYPE, pax_record(f"opaque-{index}", "value")) + header(tarfile.REGTYPE, 0)
        with self.assertRaisesRegex(tarfile.ReadError, "attribute count"):
            with tarfile.open(fileobj=io.BytesIO(raw + b"\0" * 1024), mode="r:", tarinfo=bounded_tar.BoundedTarInfo) as archive:
                for _ in archive:
                    archive.members.clear()
        for key in ("GNU.sparse.map", "GNU.sparse.size", "GNU.sparse.major"):
            with self.subTest(key=key), self.assertRaises(tarfile.ReadError):
                tarfile.open(fileobj=io.BytesIO(extension(tarfile.XHDTYPE, pax_record(key, "1")) + ordinary()),
                             mode="r:", tarinfo=bounded_tar.BoundedTarInfo)

    def test_valid_gnu_pax_xattrs_and_raw_diffid_preserved_without_cache_growth(self):
        for form in (tarfile.GNU_FORMAT, tarfile.PAX_FORMAT):
            with self.subTest(form=form):
                buffer = io.BytesIO()
                with tarfile.open(fileobj=buffer, mode="w", format=form,
                                  pax_headers={"opaque-global": "bounded"} if form == tarfile.PAX_FORMAT else None) as archive:
                    for index in range(64):
                        item = tarfile.TarInfo("long/" + "a" * 150 + str(index))
                        if form == tarfile.PAX_FORMAT:
                            item.pax_headers = {"SCHILY.xattr.user.fixture": "opaque"}
                        archive.addfile(item)
                raw = buffer.getvalue()
                cache = []
                original = bounded_tar.BoundedTarInfo.fromtarfile
                def observed(cls, archive):
                    cache.append(len(archive.members))
                    return original(archive)
                with patch.object(bounded_tar.BoundedTarInfo, "fromtarfile", classmethod(observed)):
                    result, _, _ = runner._layer_identity(io.BytesIO(gzip.compress(raw)), True, [0], None, False, False)
                self.assertEqual(result, "sha256:" + hashlib.sha256(raw).hexdigest())
                self.assertLessEqual(max(cache), 1)

    def test_actual_image_layer_legacy_and_received_database_entrypoints(self):
        raw = header(tarfile.XHDTYPE, 2**32)
        with self.assertRaisesRegex(tarfile.ReadError, "extension exceeds"):
            runner._layer_identity(HeaderOnly(raw), False, [0], None, False, False)
        with self.assertRaisesRegex(ValueError, "valid tar"):
            gateway_image._validate_layer_tar(HeaderOnly(raw))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.tar"
            path.write_bytes(raw)
            with self.assertRaisesRegex(runner.Blocked, "invalid_oci_archive_or_layer"):
                runner.inspect_oci(path, "sha256:" + "0" * 64)
            path.write_bytes(gzip.compress(raw))
            with self.assertRaisesRegex(tarfile.ReadError, "extension exceeds"):
                scan_gateway_image.inspect_database_archive(path)


if __name__ == "__main__":
    unittest.main()
