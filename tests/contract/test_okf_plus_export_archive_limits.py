"""Pre-parser resource bounds shared by public and private OKF+ verification."""
import gzip
import io
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest import mock

from tests.contract.test_okf_plus_export import EXPORT


PUBLIC = 'gis-ai-go.okf-plus-export-manifest.v1'
PRIVATE = 'gis-ai-go.okf-plus-private-document-export.v1'
EXTENSIONS = (tarfile.XHDTYPE, tarfile.XGLTYPE, tarfile.SOLARIS_XHDTYPE,
              tarfile.GNUTYPE_LONGNAME, tarfile.GNUTYPE_LONGLINK)


def member(name, body=b'', kind=tarfile.REGTYPE, declared=None):
    info = tarfile.TarInfo(name)
    info.type = kind
    info.size = len(body) if declared is None else declared
    return info.tobuf(tarfile.USTAR_FORMAT) + body + b'\0' * (-len(body) % 512)


def pax(key, value):
    record = f' {key}={value}\n'.encode()
    length = len(record) + 1
    while len(str(length)) + len(record) != length:
        length = len(str(length)) + len(record)
    return str(length).encode() + record


def valid_tar(schema=PUBLIC, format=tarfile.PAX_FORMAT, global_headers=None):
    name = 'métadonnées/角度.md' if format == tarfile.PAX_FORMAT else 'metadata/' + 'segment/' * 25 + 'record.md'
    payload = b'Synthetic public metadata.\n'
    entry = {'path': name, 'bytes': len(payload), 'sha256': EXPORT.sha(payload)}
    manifest = {'schema': schema, 'fileCount': 1, 'payloadBytes': len(payload), 'files': [entry]}
    result = io.BytesIO()
    with tarfile.open(fileobj=result, mode='w', format=format, pax_headers=global_headers) as archive:
        for path, raw in [(name, payload), (EXPORT.MANIFEST, EXPORT.canonical(manifest))]:
            info = tarfile.TarInfo(path)
            info.size = len(raw)
            archive.addfile(info, io.BytesIO(raw))
    return result.getvalue(), manifest


def canonical_local_pax_tar(schema, count=30):
    entries = [{'path': f'empty-{number}.txt', 'bytes': 0, 'sha256': EXPORT.sha(b'')} for number in range(count)]
    manifest = {'schema': schema, 'fileCount': count, 'payloadBytes': 0, 'files': entries}
    raw = b''.join(member('local-path', pax('path', entry['path']), tarfile.XHDTYPE)
                   + member(entry['path']) for entry in entries)
    raw += member(EXPORT.MANIFEST, EXPORT.canonical(manifest)) + b'\0' * 1024
    return raw, manifest


class ArchivePreParserLimitsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'synthetic.tar.gz'

    def tearDown(self):
        self.temp.cleanup()

    def write(self, raw):
        self.path.write_bytes(gzip.compress(raw, mtime=0))

    def spy_reads(self):
        reads = []
        original = EXPORT._ExpandedReader.read
        def read(reader, size):
            reads.append((reader.tell(), size))
            return original(reader, size)
        return reads, mock.patch.object(EXPORT._ExpandedReader, 'read', read)

    def test_oversized_local_global_solaris_and_gnu_bodies_rejected_before_read(self):
        for schema in (PUBLIC, PRIVATE):
            for kind in EXTENSIONS:
                with self.subTest(schema=schema, kind=kind):
                    self.write(member('extension', b'x' * 1024, kind, declared=513) + b'\0' * 1024)
                    reads, spy = self.spy_reads()
                    with mock.patch.object(EXPORT, 'MAX_EXTENSION_BYTES', 512), spy:
                        with self.assertRaisesRegex(ValueError, 'extension exceeds byte ceiling'):
                            EXPORT.verify_archive(self.path, schema)
                    self.assertEqual([(0, 512)], reads, 'No extension body read may reach gzip')

    def test_canonical_local_pax_padded_size_is_guarded_before_body_read(self):
        self.write(member('extension', pax('path', 'x' * 243), tarfile.XHDTYPE, declared=257) + b'\0' * 1024)
        reads, spy = self.spy_reads()
        with mock.patch.object(EXPORT, 'MAX_EXTENSION_BYTES', 300), spy:
            with self.assertRaisesRegex(ValueError, 'extension exceeds byte ceiling'):
                EXPORT.verify_archive(self.path)
        self.assertEqual([(0, 512)], reads)

    def test_canonical_local_pax_aggregate_and_count_limits_apply_before_next_body_read(self):
        raw, _ = canonical_local_pax_tar(PUBLIC, count=2)
        for setting, value in [('MAX_EXTENSION_TOTAL', 1024), ('MAX_EXTENSION_HEADERS', 1)]:
            with self.subTest(setting=setting):
                self.write(raw)
                reads, spy = self.spy_reads()
                with mock.patch.object(EXPORT, setting, value), spy:
                    with self.assertRaisesRegex(ValueError, 'aggregate ceiling'):
                        EXPORT.verify_archive(self.path)
                self.assertEqual([(0, 512), (512, 512), (1024, 512), (1536, 512)], reads)

    def test_canonical_local_pax_bodies_and_headers_share_one_byte_budget(self):
        raw, _ = canonical_local_pax_tar(PUBLIC, count=2)
        self.write(raw)
        reads, spy = self.spy_reads()
        with mock.patch.object(EXPORT, 'MAX_EXTENSION_TOTAL', 1024), spy:
            with self.assertRaisesRegex(ValueError, 'aggregate ceiling'):
                EXPORT.verify_archive(self.path)
        self.assertEqual([(0, 512), (512, 512), (1024, 512), (1536, 512)], reads)

    def test_local_pax_depth_guard_precedes_nested_metadata_body_read(self):
        raw = member('local', pax('path', 'payload'), tarfile.XHDTYPE) * 4 + member('payload', b'x') + b'\0' * 1024
        self.write(raw)
        reads, spy = self.spy_reads()
        with mock.patch.object(EXPORT, 'MAX_EXTENSION_DEPTH', 1), spy:
            with self.assertRaisesRegex(ValueError, 'nesting exceeds ceiling'):
                EXPORT.verify_archive(self.path)
        self.assertEqual((1024, 512), reads[-1])

    def test_canonical_local_pax_count_is_cumulative_across_separate_payload_members(self):
        raw = member('local-one', pax('path', 'one'), tarfile.XHDTYPE) + member('one', b'x')
        raw += member('local-two', pax('path', 'two'), tarfile.XHDTYPE) + member('two', b'x')
        self.write(raw + b'\0' * 1024)
        with mock.patch.object(EXPORT, 'MAX_EXTENSION_HEADERS', 1):
            with self.assertRaisesRegex(ValueError, 'aggregate ceiling'):
                EXPORT.verify_archive(self.path)

    def test_expanded_gzip_budget_rejects_large_header_request_before_allocation(self):
        source = mock.Mock()
        source.read.return_value = b'x' * 33
        with mock.patch.object(EXPORT, 'MAX_EXPANDED', 32):
            reader = EXPORT._ExpandedReader(source)
            with self.assertRaisesRegex(ValueError, 'Expanded archive'):
                reader.read(2**40)
        source.read.assert_called_once_with(33)

    def test_raw_header_and_payload_padding_are_counted(self):
        self.write(member('payload', b'x') + b'\0' * 1024)
        with mock.patch.object(EXPORT, 'MAX_EXPANDED', 600):
            with self.assertRaisesRegex(ValueError, 'Expanded archive'):
                EXPORT.verify_archive(self.path)

    def test_trailing_zero_padding_and_concatenated_gzip_output_are_counted(self):
        raw, _ = valid_tar()
        self.path.write_bytes(gzip.compress(raw) + gzip.compress(b'\0' * 1024))
        with mock.patch.object(EXPORT, 'MAX_EXPANDED', len(raw) + 32):
            with self.assertRaisesRegex(ValueError, 'Expanded archive'):
                EXPORT.verify_archive(self.path)

    def test_nonzero_trailing_data_is_not_hidden_after_tar_terminator(self):
        raw, _ = valid_tar()
        for archive in (gzip.compress(raw + b'hidden payload'), gzip.compress(raw) + gzip.compress(b'hidden payload')):
            self.path.write_bytes(archive)
            with self.assertRaisesRegex(ValueError, 'Nonzero trailing'):
                EXPORT.verify_archive(self.path)

    def test_normal_zero_padding_and_split_gzip_streams_roundtrip(self):
        raw, expected = valid_tar()
        self.path.write_bytes(gzip.compress(raw[:512]) + gzip.compress(raw[512:] + b'\0' * 512))
        self.assertEqual(expected, EXPORT.verify_archive(self.path))

    def test_old_gnu_sparse_rejected_before_extra_sparse_blocks(self):
        header = bytearray(member('sparse', b'', tarfile.GNUTYPE_SPARSE)[:512])
        header[482] = 1  # Signals an arbitrarily long hidden sparse-map block chain.
        header[148:156] = b' ' * 8
        header[148:156] = f'{sum(header):06o}\0 '.encode()
        self.write(bytes(header) + b'x' * 4096)
        reads, spy = self.spy_reads()
        with spy, mock.patch.object(tarfile.TarInfo, '_proc_sparse', side_effect=AssertionError('hidden map read')):
            with self.assertRaisesRegex(ValueError, 'Sparse archive'):
                EXPORT.verify_archive(self.path)
        self.assertEqual([(0, 512)], reads)

    def test_pax_sparse_variants_rejected_before_map_parser_or_hidden_read(self):
        variants = [pax('GNU.sparse.map', '0,1,2,3'), pax('GNU.sparse.size', '1'),
                    pax('GNU.sparse.major', '1') + pax('GNU.sparse.minor', '0'),
                    pax('GNU.sparse.realsize', '999999999'), pax('SCHILY.filetype', 'sparse')]
        for kind in (tarfile.XHDTYPE, tarfile.XGLTYPE, tarfile.SOLARIS_XHDTYPE):
            for body in variants:
                with self.subTest(kind=kind, body=body):
                    self.write(member('sparse-metadata', body, kind) + member('file', b'') + b'x' * 512)
                    reads, spy = self.spy_reads()
                    with (spy, mock.patch.object(tarfile.TarInfo, '_proc_gnusparse_00', side_effect=AssertionError('sparse00')),
                            mock.patch.object(tarfile.TarInfo, '_proc_gnusparse_01', side_effect=AssertionError('sparse01')),
                            mock.patch.object(tarfile.TarInfo, '_proc_gnusparse_10', side_effect=AssertionError('sparse10'))):
                        expected = 'Sparse archive' if kind == tarfile.XHDTYPE else 'Unsupported or nested archive metadata'
                        with self.assertRaisesRegex(ValueError, expected):
                            EXPORT.verify_archive(self.path)
                    self.assertEqual([(0, 512), (512, 512), (1024, 512)] if kind == tarfile.XHDTYPE else [(0, 512)], reads)

    def test_truncated_headers_extension_payloads_padding_and_gzip_fail_closed(self):
        raw, _ = valid_tar()
        cases = [raw[:100], raw[:512], member('metadata', b'x', tarfile.XHDTYPE, declared=512)[:600],
                 member('payload', b'x')[:513], raw[:len(raw.rstrip(b'\0'))], raw[:len(raw.rstrip(b'\0'))] + b'\0' * 512]
        for value in cases:
            with self.subTest(bytes=len(value)):
                self.write(value)
                with self.assertRaises(ValueError):
                    EXPORT.verify_archive(self.path)
        self.write(raw)
        self.path.write_bytes(self.path.read_bytes()[:-8])
        with self.assertRaisesRegex(ValueError, 'compressed archive'):
            EXPORT.verify_archive(self.path)

    def test_canonical_local_pax_unicode_paths_roundtrip_both_schemas(self):
        for schema in (PUBLIC, PRIVATE):
            with self.subTest(schema=schema):
                raw, expected = valid_tar(schema)
                self.write(raw)
                self.assertEqual(expected, EXPORT.verify_archive(self.path, schema))

    def test_strict_policy_rejects_global_solaris_and_gnu_metadata_before_body_or_copy(self):
        for schema in (PUBLIC, PRIVATE):
            for kind in EXTENSIONS[1:]:
                with self.subTest(schema=schema, kind=kind):
                    self.write(member('metadata', pax('path', 'record.txt'), kind) + member('record.txt') + b'\0' * 1024)
                    reads, spy = self.spy_reads()
                    expected = 'GNU archive metadata' if kind in (tarfile.GNUTYPE_LONGNAME, tarfile.GNUTYPE_LONGLINK) else 'Unsupported or nested archive metadata'
                    with spy, mock.patch.object(tarfile.TarInfo, '_apply_pax_info', side_effect=AssertionError('metadata copy')):
                        with self.assertRaisesRegex(ValueError, expected):
                            EXPORT.verify_archive(self.path, schema)
                    self.assertEqual([(0, 512)], reads)

    def test_strict_policy_rejects_500_attribute_global_header_before_body_or_member_copy(self):
        for schema in (PUBLIC, PRIVATE):
            body = b''.join(pax(f'vendor.attribute-{number}', 'fixture') for number in range(500))
            self.write(member('global', body, tarfile.XGLTYPE) + member('file') + b'\0' * 1024)
            reads, spy = self.spy_reads()
            with spy, mock.patch.object(tarfile.TarInfo, '_apply_pax_info', side_effect=AssertionError('unbounded copy')):
                with self.assertRaisesRegex(ValueError, 'Unsupported or nested archive metadata'):
                    EXPORT.verify_archive(self.path, schema)
            self.assertEqual([(0, 512)], reads)

    def test_many_canonical_local_pax_members_do_not_accumulate_cached_state(self):
        for schema in (PUBLIC, PRIVATE):
            raw, expected = canonical_local_pax_tar(schema)
            self.write(raw)
            retained = []
            original_next = tarfile.TarFile.next
            def observe(archive):
                result = original_next(archive)
                retained.append((len(archive.members), sum(len(info.pax_headers) for info in archive.members)))
                return result
            with mock.patch.object(tarfile.TarFile, 'next', observe):
                self.assertEqual(expected, EXPORT.verify_archive(self.path, schema))
            self.assertEqual(1, max(count for count, _ in retained))
            self.assertEqual(1, max(attributes for _, attributes in retained))
            self.assertEqual((0, 0), retained[-1])

    def test_strict_policy_rejects_global_pax_after_regular_member_before_body_or_copy(self):
        raw = member('one') + member('global', pax('vendor.value', 'one'), tarfile.XGLTYPE)
        raw += member('two') + b'\0' * 1024
        for schema in (PUBLIC, PRIVATE):
            self.write(raw)
            reads, spy = self.spy_reads()
            original_apply = tarfile.TarInfo._apply_pax_info
            copied = []
            def observe(info, headers, encoding, errors):
                copied.append(dict(headers))
                return original_apply(info, headers, encoding, errors)
            with spy, mock.patch.object(tarfile.TarInfo, '_apply_pax_info', observe):
                with self.assertRaisesRegex(ValueError, 'Unsupported or nested archive metadata'):
                    EXPORT.verify_archive(self.path, schema)
            self.assertEqual([(0, 512), (512, 512)], reads)
            self.assertTrue(all(not headers for headers in copied))

    def test_canonical_local_pax_state_values_are_bounded_before_copy(self):
        original_apply = tarfile.TarInfo._apply_pax_info
        for schema in (PUBLIC, PRIVATE):
            self.write(member('local', pax('path', 'x' * 40), tarfile.XHDTYPE) + member('file') + b'\0' * 1024)
            copied = []
            def observe(info, headers, encoding, errors):
                copied.append(dict(headers))
                self.assertFalse(headers, 'Over-limit local PAX state must not reach the copy')
                return original_apply(info, headers, encoding, errors)
            with (mock.patch.object(EXPORT, 'MAX_PAX_STATE_BYTES', 32),
                  mock.patch.object(tarfile.TarInfo, '_apply_pax_info', observe)):
                with self.assertRaisesRegex(ValueError, 'PAX state exceeds'):
                    EXPORT.verify_archive(self.path, schema)
            self.assertEqual([{}], copied)

    def test_canonical_local_pax_attribute_count_is_bounded_before_copy(self):
        original_apply = tarfile.TarInfo._apply_pax_info
        for schema in (PUBLIC, PRIVATE):
            self.write(member('local', pax('path', 'file'), tarfile.XHDTYPE) + member('file') + b'\0' * 1024)
            copied = []
            def observe(info, headers, encoding, errors):
                copied.append(dict(headers))
                self.assertFalse(headers, 'Over-limit local PAX state must not reach the copy')
                return original_apply(info, headers, encoding, errors)
            with (mock.patch.object(EXPORT, 'MAX_PAX_ATTRIBUTES', 0),
                  mock.patch.object(tarfile.TarInfo, '_apply_pax_info', observe)):
                with self.assertRaisesRegex(ValueError, 'PAX attribute count'):
                    EXPORT.verify_archive(self.path, schema)
            self.assertEqual([{}], copied)

    def test_strict_policy_rejects_bounded_unknown_local_pax_attributes_before_payload_read(self):
        for schema in (PUBLIC, PRIVATE):
            for attributes in (pax('vendor.comment', 'fixture'), pax('path', 'file') + pax('vendor.comment', 'fixture')):
                with self.subTest(schema=schema, attributes=attributes):
                    self.write(member('local', attributes, tarfile.XHDTYPE) + member('file', b'x') + b'\0' * 1024)
                    reads, spy = self.spy_reads()
                    with spy, mock.patch.object(tarfile.TarFile, 'extractfile', side_effect=AssertionError('payload read')):
                        with self.assertRaisesRegex(ValueError, 'non-canonical PAX metadata'):
                            EXPORT.verify_archive(self.path, schema)
                    self.assertEqual([(0, 512), (512, 512), (1024, 512)], reads)


if __name__ == '__main__':
    unittest.main()
