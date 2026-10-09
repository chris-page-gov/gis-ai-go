"""Controls for explicit offline development-container admission and preparation."""
import argparse
from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('dev_environment', ROOT / 'scripts/environment/environment.py')
env = importlib.util.module_from_spec(spec)
spec.loader.exec_module(env)


class EnvironmentControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.private = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / '.devcontainer', self.root / '.devcontainer')
        self.scope = patch.object(env, 'ROOT', self.root)
        self.scope.start()
        self.source = {'source_sha256': 'a' * 64, 'files': []}

    def tearDown(self):
        self.scope.stop()
        self.temp.cleanup()
        self.private.cleanup()

    def args(self, **kwargs):
        return argparse.Namespace(profile='bduk', image='registry.example/toolchain@sha256:' + 'b' * 64,
                                  source_review=None, image_review=None, workspace_review=None,
                                  assurance_receipt=None, output=None, approval=None, **kwargs)

    def reviews(self):
        args = self.args()
        private = Path(self.private.name)
        args.source_review = private / 'source-review.json'
        args.image_review = private / 'image-review.json'
        args.approval = private / 'approval.json'
        args.assurance_receipt = private / 'assurance.json'
        args.source_review.write_text(json.dumps({'kind': 'gis-ai-go.full-source-review.v1',
            'scope': 'full-source', 'source_sha256': self.source['source_sha256'], 'status': 'PASS',
            'canonical_report_sha256': 'f' * 64, 'coverage_checked': True, 'unresolved_findings': []}))
        args.assurance_receipt.write_text(json.dumps({'schema': 'gis-ai-go.offline-image-assurance.v1',
            'status': 'PASS', 'network': 'none', 'archive': {'sha256': 'e' * 64},
            'image': {'resolved_uid': 1000, 'requested_manifest_digest': args.image.rsplit('@', 1)[-1],
                      'manifest_digest': 'sha256:' + 'd' * 64, 'config_digest': 'sha256:' + 'c' * 64}}))
        args.image_review.write_text(json.dumps({'kind': 'gis-ai-go.devcontainer-image-review.v1',
            'image_reference': args.image, 'status': 'PASS', 'signature_verified': True,
            'provenance_verified': True, 'platform_policy_checked': True, 'unresolved_findings': [],
            'assurance_receipt_sha256': env.sha(args.assurance_receipt), 'oci_archive_sha256': 'e' * 64,
            'oci_manifest_digest': args.image.rsplit('@', 1)[-1]}))
        approval = {'kind': 'gis-ai-go.devcontainer-platform-approval.v1', 'approved': True,
                    'approved_by': 'synthetic-platform-reviewer', 'change_id': 'SYNTHETIC-1',
                    'source_sha256': self.source['source_sha256'], 'image_reference': args.image,
                    'source_review_sha256': env.sha(args.source_review),
                    'image_review_sha256': env.sha(args.image_review), 'profile': 'bduk', 'network': 'none',
                    'expires_at': (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()}
        args.approval.write_text(json.dumps(approval))
        return args

    def test_all_profiles_share_manual_offline_hardening(self):
        for profile in ('local', 'cloud', 'bduk'):
            config = env.profile_check(profile)
            self.assertEqual(config['runArgs'], env.BASE_RUN_ARGS)
            self.assertEqual(config['mounts'], [])
            self.assertEqual(config['containerUser'], '1000:1000')
            self.assertEqual(config['remoteUser'], '1000')

    def test_profile_rejects_socket_mount_privilege_or_open_hook(self):
        path = self.root / '.devcontainer/bduk/devcontainer.json'
        original = json.loads(path.read_text())
        mutations = [{'mounts': ['source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind']},
                     {'runArgs': env.BASE_RUN_ARGS + ['--privileged']},
                     {'postCreateCommand': 'pnpm install'}, {'features': {'any': {}}}]
        for mutation in mutations:
            path.write_text(json.dumps(original | mutation))
            with self.assertRaises(env.Blocked):
                env.profile_check('bduk')

    def test_unconfigured_image_never_runs_docker(self):
        args = self.args()
        args.image = None
        with patch.dict(env.os.environ, {}, clear=True), patch.object(env, 'inspect_image') as inspect:
            with self.assertRaises(env.Blocked):
                env.preflight(args)
            inspect.assert_not_called()

    def test_mutable_image_tag_never_runs_docker(self):
        with patch.object(env, 'run') as run:
            with self.assertRaises(env.Blocked):
                env.inspect_image('registry.example/toolchain:latest')
            run.assert_not_called()

    def test_cached_root_image_rejected(self):
        record = [{'Os': 'linux', 'Architecture': 'amd64', 'Config': {'User': 'root'}}]
        with patch.object(env.shutil, 'which', return_value='/mock/docker'), patch.object(
                env, 'run', return_value=subprocess.CompletedProcess([], 0, json.dumps(record))):
            with self.assertRaises(env.Blocked):
                env.inspect_image(self.args().image)

    def test_local_config_digest_works_without_registry_publication(self):
        image = 'sha256:' + 'c' * 64
        record = [{'Os': 'linux', 'Architecture': 'amd64', 'Config': {'User': 'node:node'},
                   'Id': image, 'RepoDigests': []}]
        with patch.object(env.shutil, 'which', return_value='/mock/docker'), patch.object(
                env, 'run', return_value=subprocess.CompletedProcess([], 0, json.dumps(record))):
            result = env.inspect_image(image)
        self.assertEqual(result['reference_kind'], 'local-config-digest')

    def test_bduk_rejects_local_config_digest(self):
        args = self.args()
        args.image = 'sha256:' + 'c' * 64
        with patch.object(env, 'source_manifest', return_value=self.source), \
                patch.object(env, 'review_gate') as review:
            with self.assertRaises(env.Blocked):
                env.preflight(args)
            review.assert_not_called()

    def test_bduk_requires_exact_reviews_and_platform_record(self):
        with self.assertRaises(env.Blocked):
            env.review_gate(self.args(), self.source)
        args = self.reviews()
        self.assertIn('platform_approval_sha256', env.review_gate(args, self.source))
        args.source_review.write_text(json.dumps({'source_sha256': 'c' * 64, 'status': 'PASS'}))
        with self.assertRaises(env.Blocked):
            env.review_gate(args, self.source)

    def test_generic_pass_or_unresolved_security_review_is_not_admitted(self):
        args = self.reviews()
        original = json.loads(args.source_review.read_text())
        for record in ({'status': 'PASS', 'source_sha256': self.source['source_sha256']},
                       original | {'unresolved_findings': ['SYNTHETIC-BLOCKER']},
                       original | {'coverage_checked': False}):
            args.source_review.write_text(json.dumps(record))
            approval = json.loads(args.approval.read_text()) | {'source_review_sha256': env.sha(args.source_review)}
            args.approval.write_text(json.dumps(approval))
            with self.assertRaises(env.Blocked):
                env.review_gate(args, self.source)

    def test_blocked_offline_assurance_never_becomes_platform_acceptance(self):
        args = self.reviews()
        assurance = json.loads(args.assurance_receipt.read_text()) | {'status': 'BLOCKED'}
        args.assurance_receipt.write_text(json.dumps(assurance))
        ir = json.loads(args.image_review.read_text()) | {'assurance_receipt_sha256': env.sha(args.assurance_receipt)}
        args.image_review.write_text(json.dumps(ir))
        approval = json.loads(args.approval.read_text()) | {'image_review_sha256': env.sha(args.image_review)}
        args.approval.write_text(json.dumps(approval))
        with self.assertRaises(env.Blocked):
            env.review_gate(args, self.source)

    def test_approved_image_receipt_must_bind_the_editor_uid(self):
        for uid in (0, 1001, None):
            args = self.reviews()
            assurance = json.loads(args.assurance_receipt.read_text())
            assurance['image']['resolved_uid'] = uid
            args.assurance_receipt.write_text(json.dumps(assurance))
            ir = json.loads(args.image_review.read_text())
            ir['assurance_receipt_sha256'] = env.sha(args.assurance_receipt)
            args.image_review.write_text(json.dumps(ir))
            approval = json.loads(args.approval.read_text())
            approval['image_review_sha256'] = env.sha(args.image_review)
            args.approval.write_text(json.dumps(approval))
            with self.assertRaises(env.Blocked):
                env.review_gate(args, self.source)

    def test_platform_expiry_and_network_change_block_admission(self):
        args = self.reviews()
        original = json.loads(args.approval.read_text())
        for changes in ({'expires_at': '2000-01-01T00:00:00Z'}, {'network': 'bridge'}, {'approved': False}):
            args.approval.write_text(json.dumps(original | changes))
            with self.assertRaises(env.Blocked):
                env.review_gate(args, self.source)

    def test_initial_bduk_workspace_rejects_ignored_material_without_deleting_it(self):
        with patch.object(env, 'run', return_value=subprocess.CompletedProcess([], 0, 'artifacts/\0')):
            with self.assertRaises(env.Blocked):
                env.workspace_check(self.args(), self.source)

    def test_local_workspace_preserves_and_reports_existing_material(self):
        args = self.args()
        args.profile = 'local'
        with patch.object(env, 'run', return_value=subprocess.CompletedProcess([], 0, 'artifacts/\0')):
            result = env.workspace_check(args, self.source)
        self.assertTrue(result['ignored_content'])

    def test_reopen_requires_exact_review_of_every_ignored_file(self):
        args = self.reviews()
        args.workspace_review = self.root / 'workspace-review.json'
        material = {'workspace_sha256': 'd' * 64, 'files': [{'path': 'node_modules/package/index.js'}]}
        args.workspace_review.write_text(json.dumps({'kind': 'gis-ai-go.workspace-review.v1', 'status': 'PASS',
            'source_sha256': self.source['source_sha256'], 'workspace_sha256': material['workspace_sha256']}))
        approval = json.loads(args.approval.read_text()) | {'workspace_sha256': material['workspace_sha256'],
                     'workspace_review_sha256': env.sha(args.workspace_review)}
        args.approval.write_text(json.dumps(approval))
        with patch.object(env, 'run', return_value=subprocess.CompletedProcess([], 0, 'node_modules/\0')), \
                patch.object(env, 'workspace_manifest', return_value=material):
            self.assertTrue(env.workspace_check(args, self.source)['ignored_content'])
            material['workspace_sha256'] = 'e' * 64
            with self.assertRaises(env.Blocked):
                env.workspace_check(args, self.source)

    def test_credentials_remain_excluded_even_with_workspace_review(self):
        args = self.reviews()
        args.workspace_review = self.root / 'workspace-review.json'
        args.workspace_review.write_text('{}')
        material = {'workspace_sha256': 'd' * 64, 'files': [{'path': 'artifacts/private/service-account.pem'}]}
        with patch.object(env, 'run', return_value=subprocess.CompletedProcess([], 0, 'artifacts/\0')), \
                patch.object(env, 'workspace_manifest', return_value=material):
            with self.assertRaises(env.Blocked):
                env.workspace_check(args, self.source)

    def test_mirror_requires_verified_https_without_credentials(self):
        for url in ('http://mirror.example/tool', 'https://user:secret@mirror.example/tool',
                    'https://mirror.example/tool?token=secret'):
            with self.assertRaises(env.Blocked):
                env.secure_url(url)
        self.assertEqual(env.secure_url('https://mirror.example/tool'), 'https://mirror.example/tool')

    def test_context_preparation_never_downloads_implicitly(self):
        args = argparse.Namespace(output=self.root / 'context', cache=self.root / 'cache',
                                  ca_file=None, mirror=None, download=False)
        with self.assertRaises(env.Blocked):
            env.prepare_image(args)
        self.assertFalse(args.output.exists())

    def test_context_rejects_extra_repository_or_credentials(self):
        context = self.root / 'context'
        context.mkdir()
        (context / 'context-manifest.json').write_text('{}')
        (context / '.env').write_text('synthetic fixture')
        with self.assertRaises(env.Blocked):
            env.validate_context(context)

    def test_context_checks_complete_digest_and_reviewed_source(self):
        context = self.root / 'context'
        (context / 'inputs').mkdir(parents=True)
        for name in env.IMAGE_FILES:
            shutil.copyfile(self.root / '.devcontainer/image' / name, context / name)
        pins = env.lock()
        for item in pins['artifacts']:
            payload = b'synthetic archive fixture'
            (context / 'inputs' / item['name']).write_bytes(payload)
            item['sha256'] = env.sha(context / 'inputs' / item['name'])
        files = [{'path': str(path.relative_to(context)), 'sha256': env.sha(path), 'bytes': path.stat().st_size}
                 for path in sorted(context.rglob('*')) if path.is_file()]
        manifest = {'files': files, 'context_sha256': env.hashlib.sha256(env.canonical(files)).hexdigest()}
        (context / 'context-manifest.json').write_text(json.dumps(manifest))
        with patch.object(env, 'lock', return_value=pins):
            self.assertEqual(env.validate_context(context), manifest)
            (context / 'Containerfile').write_text('tampered')
            with self.assertRaises(env.Blocked):
                env.validate_context(context)

    def test_container_rejects_root_before_accepting_privileges(self):
        args = argparse.Namespace(container=True)
        versions = {'node': 'v24.19.0', 'pnpm': '10.33.2', 'python3': 'Python 3.12.14',
                    'uv': 'uv 0.12.2', 'terraform': 'Terraform v1.13.4', 'git': 'git fixture', 'bash': 'bash fixture'}
        def fake_run(command, **kwargs):
            return subprocess.CompletedProcess(command, 0, versions[command[0]] + '\n')
        with patch.object(env.shutil, 'which', return_value='/mock/tool'), \
                patch.object(env, 'run', side_effect=fake_run), patch.object(env.os, 'getuid', return_value=0):
            with self.assertRaises(env.Blocked):
                env.check_tools(args)

    def test_exact_uv_version_allows_official_build_target_but_not_another_release(self):
        args = argparse.Namespace(container=False)
        versions = {'node': 'v24.19.0', 'pnpm': '10.33.2', 'python3': 'Python 3.12.14',
                    'uv': 'uv 0.12.2 (x86_64-unknown-linux-gnu)', 'terraform': 'Terraform v1.13.4',
                    'git': 'git fixture', 'bash': 'bash fixture'}
        def fake_run(command, **kwargs):
            return subprocess.CompletedProcess(command, 0, versions[command[0]] + '\n')
        with patch.object(env.shutil, 'which', return_value='/mock/tool'), \
                patch.object(env, 'run', side_effect=fake_run):
            self.assertEqual(env.check_tools(args)['tools']['uv'], 'uv 0.12.2')
            versions['uv'] = 'uv 0.12.20 (x86_64-unknown-linux-gnu)'
            with self.assertRaises(env.Blocked):
                env.check_tools(args)

    def test_install_is_frozen_offline_and_does_not_run_dependency_hooks(self):
        for name in ('pnpm-lock.yaml', 'uv.lock', 'package.json', 'pyproject.toml'):
            (self.root / name).write_text('synthetic fixture')
        args = argparse.Namespace(container=False)
        with patch.object(env, 'check_tools'), patch.object(env, 'run') as run, \
                patch.dict(env.os.environ, {}, clear=True):
            result = env.install(args)
        self.assertTrue(result['offline'])
        self.assertIn('--ignore-scripts', run.call_args_list[0].args[0])
        self.assertIn('--frozen-lockfile', run.call_args_list[0].args[0])
        self.assertIn('--locked', run.call_args_list[1].args[0])
        self.assertIn('--no-build', run.call_args_list[1].args[0])


if __name__ == '__main__':
    unittest.main()
