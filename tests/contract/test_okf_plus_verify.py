"""Offline assurance boundaries, complete-corpus audit and failure exit tests."""
from copy import deepcopy
import gzip
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts.okf_plus import verify
from scripts.okf_plus.context_projection import canonical, project, sha
from tests.contract.test_okf_plus_context import BASE, CAPTURED, fixture


def evaluation(failed=0):
    return {'counts': {'cases': 40, 'passedRetrieval': 36 - failed, 'failedRetrieval': failed,
                       'notEvaluatedContextRequired': 4},
            'cases': ([{'id': 'retrieval-' + str(x), 'status': 'failed' if x < failed else 'passed-retrieval'}
                       for x in range(36)] + [{'id': 'context-' + str(x), 'status': 'not-evaluated-context-required'}
                                             for x in range(4)])}


class VerificationTests(unittest.TestCase):
    def test_retrieval_failure_and_unrun_context_are_separate(self):
        gate = verify.retrieval_gate(evaluation(1))
        self.assertEqual(gate['status'], 'failed')
        self.assertEqual(gate['failedCaseIds'], ['retrieval-0'])
        self.assertEqual(len(gate['unassessedContextCaseIds']), 4)
        self.assertEqual(verify.retrieval_gate(evaluation())['status'], 'passed')
        bad = evaluation(); bad['counts']['notEvaluatedContextRequired'] = 0
        with self.assertRaisesRegex(ValueError, 'boundary changed'):
            verify.retrieval_gate(bad)

    def test_complete_corpus_audit_checks_every_source_field_and_passage(self):
        search, bundle = fixture()
        outputs, _ = project(search, bundle, base_url=BASE, captured_at=CAPTURED)
        result = verify.audit_complete_corpus(search, bundle, outputs)
        self.assertEqual(result['evidenceRecords'], 41)
        self.assertEqual(result['discoveryCards'], 41)
        self.assertEqual(result['omittedSemanticFields'], 0)
        changed = deepcopy(bundle)
        changed['records'][-1]['update']['nextRelease'] = 'Unretained source correction'
        with self.assertRaisesRegex(ValueError, 'Whole source metadata omitted'):
            verify.audit_complete_corpus(search, changed, outputs)

    def test_duplicate_discovery_identity_fails_even_with_rebound_shard_hash(self):
        search, bundle = fixture()
        outputs, _ = project(search, bundle, base_url=BASE, captured_at=CAPTURED)
        manifest = json.loads(outputs['manifest.json'])
        reference = manifest['discovery']['shards'][0]
        data = json.loads(gzip.decompress(outputs[reference['path']]))
        data['cards'][1] = deepcopy(data['cards'][0])
        decoded = canonical(data); raw = gzip.compress(decoded, mtime=0)
        outputs[reference['path']] = raw
        reference.update(sha256=sha(raw), decoded_sha256=sha(decoded))
        outputs['manifest.json'] = canonical(manifest)
        with self.assertRaisesRegex(ValueError, 'duplicate or stale discovery'):
            verify.audit_complete_corpus(search, bundle, outputs)

    def test_real_case_selection_requires_tail_and_literal_cadence_feed_rights(self):
        search, bundle = fixture()
        for row, parent in zip(search['records'], bundle['records']):
            row['sourceFamily'] = parent['sourceFamily'] = 'ons-datasets'
        search['records'][-2]['nativeIdentifier'] = bundle['records'][-2]['nativeIdentifier'] = 'cpih01'
        outputs, projection = project(search, bundle, base_url=BASE, captured_at=CAPTURED)
        cases = verify.representative_cases(search, projection)
        self.assertEqual(cases[0]['expectedId'], search['records'][-1]['id'])
        self.assertGreater(cases[0]['selectionEvidence']['canonicalOrdinal'], 16)
        self.assertTrue(cases[0]['selectionEvidence']['outsideRepresentativeIndex'])
        self.assertIn(canonical(search['records'][-2]['rights']).decode(), cases[1]['requiredText'])
        self.assertTrue(cases[2]['expectInsufficient'])
        self.assertTrue(cases[3]['expectEmpty'])

    def test_failed_importer_produces_bounded_path_free_machine_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'repo'; root.mkdir()
            output = root / 'artifacts/okf-plus'
            private_marker = b'example private subprocess details'
            stderr = str(root).encode() + private_marker + b'x' * verify.MAX_DIAGNOSTIC_BYTES
            def failed_importer(*_args, **_kwargs):
                running = json.loads((output / 'verification.json').read_bytes())
                self.assertEqual(running['status'], 'running')
                self.assertEqual(running['activeStage'], 'importer-check')
                return subprocess.CompletedProcess([], 1, stdout=b'', stderr=stderr)
            with patch.object(verify.subprocess, 'run', side_effect=failed_importer), \
                    patch('sys.stdout', new_callable=io.StringIO) as stdout:
                report, code = verify.run_verification(root, output, 'a' * 40, CAPTURED)
            self.assertEqual(code, 2)
            self.assertEqual(report['failure']['stage'], 'importer-check')
            self.assertIsNone(report['activeStage'])
            self.assertEqual(report['timing']['stages']['importer-check']['state'], 'failed')
            raw = (output / 'verification.json').read_bytes()
            self.assertNotIn(temporary.encode(), raw)
            self.assertNotIn(private_marker, raw)
            self.assertLess(len(raw), verify.MAX_REPORT_BYTES)
            diagnostic = report['failure']['privateDiagnostic']
            path = output / diagnostic['path']
            self.assertLessEqual(path.stat().st_size, verify.MAX_DIAGNOSTIC_BYTES)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertTrue(diagnostic['truncated'])
            self.assertEqual(diagnostic['sha256'], sha(path.read_bytes()))
            self.assertIn(private_marker, path.read_bytes())
            self.assertNotIn('artifacts', report)
            self.assertIn('importer-check started', stdout.getvalue())
            self.assertIn('importer-check failed', stdout.getvalue())

    def test_checkpoints_persist_monotonic_stage_boundaries_without_claiming_passes(self):
        with tempfile.TemporaryDirectory() as temporary, \
                patch.object(verify.time, 'monotonic', side_effect=[100, 101, 111, 115]), \
                patch('sys.stdout', new_callable=io.StringIO):
            output = Path(temporary); report = {'status': 'running', 'stages': {}}
            checkpoints = verify.Checkpoints(output, report)
            checkpoints.enter('first')
            first = json.loads((output / 'verification.json').read_bytes())
            self.assertEqual(first['activeStage'], 'first')
            self.assertEqual(first['timing']['elapsedSeconds'], 1)
            checkpoints.enter('second')
            second = json.loads((output / 'verification.json').read_bytes())
            self.assertEqual(second['status'], 'running')
            self.assertEqual(second['timing']['stages']['first'], {'state': 'finished', 'elapsedSeconds': 10})
            self.assertEqual(second['timing']['stages']['second']['state'], 'running')
            self.assertEqual(second['stages'], {})
            report['status'] = 'failed-retrieval-checks'
            checkpoints.finish(failed=False)
            final = json.loads((output / 'verification.json').read_bytes())
            self.assertEqual(final['status'], 'failed-retrieval-checks')
            self.assertEqual(final['timing']['elapsedSeconds'], 15)
            self.assertEqual(final['timing']['stages']['second'], {'state': 'finished', 'elapsedSeconds': 4})
            self.assertIsNone(final['activeStage'])
            self.assertEqual(list(output.glob('.verification-*')), [])

    def test_private_diagnostic_uses_concise_error_and_refuses_symlink(self):
        class ConciseError(ValueError):
            message = 'A bounded useful validation detail'
            def __str__(self):
                raise AssertionError('Expanded source dump must not be formatted')
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            reference = verify._private_diagnostic(output, 'schema', ConciseError())
            self.assertIn(b'A bounded useful validation detail', (output / reference['path']).read_bytes())
            (output / reference['path']).unlink()
            (output / 'private-diagnostics').rmdir()
            (output / 'private-diagnostics').symlink_to(output, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'must not be a symlink'):
                verify._private_diagnostic(output, 'schema', ConciseError())

    def test_cli_propagates_nonzero_retrieval_failure(self):
        report = {'status': 'failed-retrieval-checks', 'stages': {'retrieval': {
            'unassessedContextCaseIds': ['K37', 'K38', 'K39', 'K40']}}}
        with patch.object(verify, 'run_verification', return_value=(report, 1)), \
                patch.object(verify.sys, 'addaudithook'), patch('sys.stdout', new_callable=io.StringIO) as stdout:
            code = verify.main(['--revision', 'a' * 40, '--captured-at', CAPTURED])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(stdout.getvalue())['unassessedContextCases'], ['K37', 'K38', 'K39', 'K40'])

    def test_child_wrapper_resolves_local_helpers_and_denies_network_before_dns(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'helper.py').write_text('VALUE = "local-helper-loaded"\n')
            script = root / 'script.py'
            script.write_text('from helper import VALUE\nimport socket\nprint(VALUE, flush=True)\nsocket.getaddrinfo("example.invalid", 443)\n')
            result = subprocess.run([verify.sys.executable, '-c', verify.OFFLINE_SCRIPT_WRAPPER, str(script)],
                                    cwd='/', capture_output=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, b'local-helper-loaded\n')
            self.assertIn(b'Network forbidden during offline verification', result.stderr)


if __name__ == '__main__':
    unittest.main()
