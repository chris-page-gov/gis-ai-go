"""Offline public hand-off integrity and safe-path checks."""
import gzip
import importlib.util
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/okf_plus'))
SPEC = importlib.util.spec_from_file_location('okf_plus_export_tests', ROOT / 'scripts/okf_plus/export.py')
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)
REVISION = 'c' * 40


def fixture(root):
    for name in EXPORT.FIXED:
        path = root / name; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('Synthetic public file.\n')
    (root / 'scripts/scan_secrets.py').write_bytes((ROOT / 'scripts/scan_secrets.py').read_bytes())
    for name in ('okf-plus/records/synthetic/record.md', 'scripts/okf_plus/build.py', 'scripts/okf_plus/verify.py',
                 'docs/implementation/OKF-220_TEST.md'):
        path = root / name; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('# Synthetic metadata\n')
    private = root / 'artifacts/okf-plus/capture/private.body'
    private.parent.mkdir(parents=True); private.write_text('Private evidence must be excluded.\n')
    question_path = root / 'okf-plus/evaluation/questions.json'
    question_path.parent.mkdir(); question_path.write_text('{}\n')


def generated_fixture(root):
    """Synthetic successful report with independently editable digest-chain files."""
    output = root / 'artifacts/okf-plus/verified'

    def write(path, value):
        target = output / path; target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(EXPORT.canonical(value))
        return reference(path)

    def reference(path):
        raw = (output / path).read_bytes()
        return {'path': path, 'bytes': len(raw), 'sha256': EXPORT.sha(raw)}

    inputs = EXPORT.source_inputs(root)
    input_digest = EXPORT.digest(inputs)
    write('bundle/source-lock.json', {'revision': REVISION, 'sha256': input_digest, 'inputs': inputs})
    write('bundle/search-index.json', {'synthetic': 'search'})
    write('bundle/okf-bundle.json', {'synthetic': 'bundle'})
    write('bundle/checksums.json', {p.name: EXPORT.sha(p.read_bytes()) for p in (output / 'bundle').iterdir()})
    write('context/manifest.json', {'synthetic': 'corpus'})
    manifest_ref = reference('context/manifest.json'); manifest_ref['path'] = 'manifest.json'
    write('context/projection-manifest.json', {'inputDigest': input_digest, 'sourceRevision': REVISION,
                                             'outputs': [manifest_ref]})
    projection_ref = reference('context/projection-manifest.json'); projection_ref['path'] = 'projection-manifest.json'
    write('context/descriptor-entrypoints.json', {'entrypoints': {'context_corpus': manifest_ref},
                                                'projectionManifest': projection_ref})
    for path in ('retrieval-evaluation.json', 'context/schema-validation.json',
                 'context/engine-validation.json', 'context-cases.json'):
        write(path, {'synthetic': path})
    required = ['bundle/checksums.json', 'bundle/source-lock.json', 'retrieval-evaluation.json',
                'context/descriptor-entrypoints.json', 'context/schema-validation.json',
                'context/engine-validation.json', 'context-cases.json']
    report = {'schema': 'gis-ai-go.okf-plus-offline-verification.v1', 'status': 'passed-automated-checks',
              'sourceRevision': REVISION, 'inputDigest': input_digest,
              'implementationSha256': EXPORT.sha((root / 'scripts/okf_plus/verify.py').read_bytes()),
              'questionCorpusFileSha256': EXPORT.sha((root / 'okf-plus/evaluation/questions.json').read_bytes()),
              'artifacts': {str(i): reference(path) for i, path in enumerate(required)},
              'transferredInputs': {'search': reference('bundle/search-index.json'),
                                    'bundle': reference('bundle/okf-bundle.json')},
              'stages': {'importer': {'status': 'passed'}, 'build': {'status': 'passed'},
                         'retrieval': {'status': 'passed', 'counts': {'cases': 40, 'passedRetrieval': 36,
                             'failedRetrieval': 0, 'notEvaluatedContextRequired': 4}},
                         'contextEngine': {'status': 'passed', 'cases': 4, 'networkCalls': 0},
                         'wholeCorpus': {'status': 'passed-every-record-and-card', 'inputRecords': 1,
                             'evidenceRecords': 1, 'discoveryCards': 1, 'schemaEvidenceRecords': 1,
                             'omittedRecords': 0, 'omittedSemanticFields': 0,
                             'projectionManifestSha256': projection_ref['sha256'],
                             'corpusManifestSha256': manifest_ref['sha256']}}}
    write('verification.json', report)
    return output


def archive(path, entries):
    with tarfile.open(path, 'w:gz') as output:
        for name, value in entries:
            info = tarfile.TarInfo(name)
            if isinstance(value, bytes):
                info.size = len(value); output.addfile(info, io.BytesIO(value))
            else:
                info.type = tarfile.SYMTYPE; info.linkname = value; output.addfile(info)


class OkfPlusExportTests(unittest.TestCase):
    def test_source_archives_are_relocatable_deterministic_and_exclude_captures(self):
        results = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory); fixture(root)
                output = root / 'artifacts/okf-plus/export'
                receipt = EXPORT.export(root, output, REVISION)
                path = output / receipt['archive']['path']
                manifest = EXPORT.verify_archive(path)
                self.assertEqual(manifest['generatedStatus'], 'not-included')
                self.assertNotIn('artifacts/okf-plus/capture/private.body', [x['path'] for x in manifest['files']])
                self.assertEqual(EXPORT.sha(path.read_bytes()), receipt['archive']['sha256'])
                with tarfile.open(path) as source:
                    for member in source:
                        self.assertEqual((member.mtime, member.uid, member.gid, member.mode), (0, 0, 0, 0o644))
                results.append(path.read_bytes())
        self.assertEqual(*results)

    def test_source_symlink_and_unknown_private_file_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as external:
            root = Path(directory); fixture(root)
            target = Path(external) / 'outside.md'; target.write_text('External bytes')
            link = root / 'okf-plus/records/link.md'; link.symlink_to(target)
            with self.assertRaises(ValueError):
                EXPORT.export(root, root / 'artifacts/okf-plus/export', REVISION)
            link.unlink(); (root / 'okf-plus/.env').write_text('Synthetic private file')
            with self.assertRaises(ValueError):
                EXPORT.export(root, root / 'artifacts/okf-plus/export', REVISION)

    def test_archive_rejects_traversal_absolute_paths_links_and_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'unsafe.tar.gz'
            for entries in ([('../outside', b'x')], [('/absolute', b'x')], [('link', '../outside')],
                            [('same', b'x'), ('same', b'x')], [('a\\b', b'x')]):
                archive(path, entries)
                with self.subTest(entries=entries), self.assertRaises(ValueError):
                    EXPORT.verify_archive(path)

    def test_modified_archive_member_is_rejected_by_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); fixture(root); output = root / 'artifacts/okf-plus/export'
            EXPORT.export(root, output, REVISION)
            path = output / 'okf-plus-metadata.tar.gz'
            with tarfile.open(path) as source:
                entries = [(item.name, source.extractfile(item).read()) for item in source]
            entries = [(name, raw + b'changed' if name == 'LICENSE' else raw) for name, raw in entries]
            archive(path, entries)
            with self.assertRaises(ValueError):
                EXPORT.verify_archive(path)

    def test_failed_generated_verification_does_not_replace_previous_export(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); fixture(root); output = root / 'artifacts/okf-plus/export'
            EXPORT.export(root, output, REVISION)
            before = (output / 'okf-plus-metadata.tar.gz').read_bytes()
            generated = root / 'artifacts/okf-plus'
            (generated / 'verification.json').write_text(json.dumps({
                'schema': 'gis-ai-go.okf-plus-offline-verification.v1', 'status': 'failed'}))
            with self.assertRaises(ValueError):
                EXPORT.export(root, output, REVISION, generated)
            self.assertEqual((output / 'okf-plus-metadata.tar.gz').read_bytes(), before)

    def test_generated_pack_requires_current_source_and_verified_artefact_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); fixture(root); generated = generated_fixture(root)
            output = root / 'artifacts/okf-plus/export'
            receipt = EXPORT.export(root, output, REVISION, generated)
            self.assertEqual(receipt['generatedStatus'], 'verified-automated-checks')
            manifest = EXPORT.verify_archive(output / receipt['archive']['path'])
            self.assertIn('generated/verification.json', {e['path'] for e in manifest['files']})
            source = root / 'okf-plus/records/synthetic/record.md'; before = source.read_bytes()
            source.write_bytes(before + b'changed source')
            with self.assertRaises(ValueError):
                EXPORT.export(root, output, REVISION, generated)
            source.write_bytes(before)
            (generated / 'context/manifest.json').write_text('{}\n')
            with self.assertRaises(ValueError):
                EXPORT.export(root, output, REVISION, generated)

    def test_context_review_questions_cannot_be_silently_counted_as_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); fixture(root); generated = generated_fixture(root)
            path = generated / 'verification.json'; report = json.loads(path.read_text())
            report['stages']['retrieval']['counts'].update(passedRetrieval=40, notEvaluatedContextRequired=0)
            path.write_text(json.dumps(report))
            with self.assertRaises(ValueError):
                EXPORT.export(root, root / 'artifacts/okf-plus/export', REVISION, generated)

    def test_generated_pack_rejects_added_build_inputs_and_preserves_previous_export(self):
        for added in ('okf-plus/records/synthetic/added.md', 'okf-plus/source/added.json',
                      'okf-plus/schemas/added.schema.json', 'scripts/okf_plus/added.py'):
            with self.subTest(added=added), tempfile.TemporaryDirectory() as directory:
                root = Path(directory); fixture(root); generated = generated_fixture(root)
                output = root / 'artifacts/okf-plus/export'
                EXPORT.export(root, output, REVISION, generated)
                before = (output / 'okf-plus-metadata.tar.gz').read_bytes()
                path = root / added; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('New synthetic build input, absent from the verification.\n')
                with self.assertRaisesRegex(ValueError, 'input inventory differs'):
                    EXPORT.export(root, output, REVISION, generated)
                self.assertEqual((output / 'okf-plus-metadata.tar.gz').read_bytes(), before)

    def test_secret_and_machine_path_patterns_fail_closed_in_plain_and_gzip_inputs(self):
        patterns = EXPORT.public_patterns(ROOT)
        sensitive = [('/' + 'Users' + '/synthetic-person/file').encode(), ('s' + 'k-' + 'a' * 24).encode()]
        for raw in sensitive:
            for name, value in [('source.json', raw), ('record.json.gz', gzip.compress(raw))]:
                with self.subTest(name=name), self.assertRaises(ValueError):
                    EXPORT.check_public(value, name, patterns)

    def test_oversized_file_and_unmarked_output_are_rejected(self):
        from unittest import mock
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); fixture(root); output = root / 'artifacts/okf-plus/export'
            with mock.patch.object(EXPORT, 'MAX_FILE', 4), self.assertRaises(ValueError):
                EXPORT.export(root, output, REVISION)
            output.mkdir(); (output / 'keep.txt').write_text('Keep this file.')
            with self.assertRaises(ValueError):
                EXPORT.export(root, output, REVISION)
            self.assertEqual((output / 'keep.txt').read_text(), 'Keep this file.')


if __name__ == '__main__':
    unittest.main()
