#!/usr/bin/env python3
"""Explicit development environment operations; nothing runs when VS Code opens.

This helper does not authenticate, deploy, install host tooling or change network
policy. On a secured machine review its entire source before executing it.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import ssl
import subprocess
import sys
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
IMAGE_FILES = ('Containerfile', '.dockerignore', 'toolchain.lock.json', 'install_image.py')
IMAGE_REF = re.compile(r'^[a-z0-9][a-z0-9./:_-]*@sha256:[a-f0-9]{64}$')
IMAGE_ID = re.compile(r'^sha256:[a-f0-9]{64}$')
BASE_RUN_ARGS = ['--pull=never', '--network=none', '--cap-drop=ALL',
                 '--security-opt=no-new-privileges', '--pids-limit=256', '--memory=4g']


class Blocked(RuntimeError):
    pass


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def load(path: Path) -> dict:
    if path.is_symlink():
        raise Blocked('Input symlinks are not admitted')
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise Blocked('Expected a JSON object')
    return value


def run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=True, text=True, **kwargs)


def lock() -> dict:
    result = load(ROOT / '.devcontainer/image/toolchain.lock.json')
    if result.get('platform') != 'linux/amd64':
        raise Blocked('Only the reviewed linux/amd64 toolchain is supported')
    return result


def source_manifest() -> dict:
    tracked = run(['git', '-C', str(ROOT), 'ls-files', '-z', '--cached', '--others',
                   '--exclude-standard'], stdout=subprocess.PIPE).stdout.split('\0')
    entries = []
    for name in sorted(set(filter(None, tracked))):
        path = ROOT / name
        if path.is_symlink():
            entries.append({'path': name, 'symlink': os.readlink(path)})
        elif path.is_file():
            entries.append({'path': name, 'sha256': sha(path), 'bytes': path.stat().st_size,
                            'executable': bool(path.stat().st_mode & 0o111)})
        else:
            raise Blocked('Source contains a missing file or unsupported Git submodule')
    return {'kind': 'gis-ai-go.source-manifest.v1', 'files': entries,
            'source_sha256': hashlib.sha256(canonical(entries)).hexdigest()}


def workspace_manifest() -> dict:
    names = run(['git', '-C', str(ROOT), 'ls-files', '-z', '--others', '--ignored',
                 '--exclude-standard'], stdout=subprocess.PIPE).stdout.split('\0')
    entries = []
    for name in sorted(set(filter(None, names))):
        path = ROOT / name
        if path.is_symlink() or not path.is_file():
            raise Blocked('Ignored workspace links or special files cannot be mounted')
        entries.append({'path': name, 'sha256': sha(path), 'bytes': path.stat().st_size,
                        'executable': bool(path.stat().st_mode & 0o111)})
    return {'kind': 'gis-ai-go.workspace-manifest.v1', 'files': entries,
            'workspace_sha256': hashlib.sha256(canonical(entries)).hexdigest()}


def workspace_check(args: argparse.Namespace, source: dict) -> dict:
    # A bind of the checkout includes ignored files too. A source-only clone is
    # required so private artifacts, credentials and original archives never
    # become an implicit mount. Do not remove or reset an existing checkout.
    ignored = run(['git', '-C', str(ROOT), 'ls-files', '-z', '--others', '--ignored',
                   '--exclude-standard', '--directory'], stdout=subprocess.PIPE).stdout
    if args.profile != 'bduk':
        return {'source_only': not bool(ignored), 'ignored_content': bool(ignored),
                'notice': 'Existing checkout preserved; review ignored material before mounting it.'}
    if any('symlink' in entry for entry in source['files']):
        raise Blocked('Workspace symlinks require a separate reviewed contained-source configuration')
    if ignored:
        if not args.workspace_review:
            raise Blocked('BDUK workspace contains ignored material; use a source-only clone or exact workspace review')
        material = workspace_manifest()
        # Reopening after a reviewed install/build is possible with exact material
        # approval. Credentials and private archives remain excluded regardless.
        forbidden = re.compile(r'(^|/)(\.env(?:\..*)?|\.ssh|\.aws|gcloud|credentials[^/]*)(/|$)|'
                               r'\.(?:tfstate(?:\..*)?|p12|pfx|pem|key|docx?|pdf)$', re.I)
        if any(forbidden.search(entry['path']) for entry in material['files']):
            raise Blocked('Ignored workspace includes credentials, state or original-document archives')
        review = load(args.workspace_review)
        approval = load(args.approval)
        if (review.get('kind') != 'gis-ai-go.workspace-review.v1' or review.get('status') != 'PASS' or
                review.get('source_sha256') != source['source_sha256'] or
                review.get('workspace_sha256') != material['workspace_sha256'] or
                approval.get('workspace_review_sha256') != sha(args.workspace_review) or
                approval.get('workspace_sha256') != material['workspace_sha256']):
            raise Blocked('Workspace review/approval does not bind every ignored mounted file')
        return {'source_only': False, 'ignored_content': True,
                'workspace_sha256': material['workspace_sha256'],
                'workspace_review_sha256': sha(args.workspace_review)}
    return {'source_only': True, 'ignored_content': False, 'symlinks': False}


def profile_check(profile: str) -> dict:
    path = ROOT / '.devcontainer' / profile / 'devcontainer.json'
    config = load(path)
    allowed = {'name', 'image', 'containerUser', 'remoteUser', 'updateRemoteUserUID',
               'workspaceFolder', 'workspaceMount', 'mounts', 'runArgs', 'privileged',
               'forwardPorts', 'portsAttributes', 'otherPortsAttributes', 'remoteEnv',
               'containerEnv', 'customizations'}
    if set(config) - allowed:
        raise Blocked('Profile contains an unreviewed Dev Containers property')
    forbidden = {'build', 'features', 'initializeCommand', 'onCreateCommand',
                 'updateContentCommand', 'postCreateCommand', 'postStartCommand',
                 'postAttachCommand', 'dockerComposeFile', 'appPort'}
    if forbidden.intersection(config):
        raise Blocked('Profile contains an automatic operation or extra build surface')
    expected_env = 'GIS_AI_GO_SECURE_DEV_IMAGE' if profile == 'bduk' else 'GIS_AI_GO_DEV_IMAGE'
    requirements = {
        'image': '${localEnv:' + expected_env + '}', 'containerUser': '1000:1000',
        'remoteUser': '1000', 'updateRemoteUserUID': False,
        'workspaceFolder': '/workspace/gis-ai-go',
        'workspaceMount': 'source=${localWorkspaceFolder},target=/workspace/gis-ai-go,type=bind',
        'mounts': [], 'runArgs': BASE_RUN_ARGS, 'privileged': False, 'forwardPorts': [],
    }
    if any(config.get(key) != value for key, value in requirements.items()):
        raise Blocked('Profile hardening or fixed workspace contract changed')
    settings = config.get('customizations', {}).get('vscode', {}).get('settings', {})
    if (settings.get('remote.localPortHost') != 'localhost' or
            settings.get('remote.autoForwardPorts') is not False or
            settings.get('git.enabled') is not False or
            config.get('customizations', {}).get('vscode', {}).get('extensions') != [] or
            config.get('remoteEnv', {}).get('SSH_AUTH_SOCK') != ''):
        raise Blocked('Automatic extension, credential or port integration changed')
    return config


def inspect_image(image: str) -> dict:
    registry = bool(IMAGE_REF.fullmatch(image))
    if not registry and not IMAGE_ID.fullmatch(image):
        raise Blocked('An exact registry digest or local Docker config digest is required; tags are not admitted')
    if not shutil.which('docker'):
        raise Blocked('Docker CLI is absent; no installation was attempted')
    # Local inspection does not pull, run the image or contact a registry.
    try:
        records = json.loads(run(['docker', 'image', 'inspect', image],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout)
    except subprocess.CalledProcessError:
        raise Blocked('Exact image is not cached in the selected approved Docker engine') from None
    record = records[0]
    if record.get('Os') != 'linux' or record.get('Architecture') != 'amd64':
        raise Blocked('Image architecture differs from reviewed linux/amd64')
    if record.get('Config', {}).get('User') not in ('node', 'node:node', '1000', '1000:1000'):
        raise Blocked('Image default user is not the reviewed non-root user')
    if registry and image not in record.get('RepoDigests', []):
        raise Blocked('Cached image does not bind the exact approved registry digest')
    if not registry and record.get('Id') != image:
        raise Blocked('Cached image does not bind the exact local config digest')
    return {'image_reference': image, 'image_id': record['Id'],
            'reference_kind': 'registry-manifest-or-index' if registry else 'local-config-digest',
            'platform': 'linux/amd64', 'default_user': record['Config']['User']}


def review_gate(args: argparse.Namespace, source: dict) -> dict:
    if not args.source_review or not args.image_review or not args.approval or not args.assurance_receipt:
        raise Blocked('BDUK requires full source review, immutable image review and platform approval')
    for path in (args.source_review, args.image_review, args.approval, args.assurance_receipt,
                 args.workspace_review, args.output):
        if path and (path.resolve() == ROOT.resolve() or ROOT.resolve() in path.resolve().parents):
            raise Blocked('BDUK private review records must be outside the mounted source workspace')
    sr, ir, approval = map(load, (args.source_review, args.image_review, args.approval))
    assurance = load(args.assurance_receipt)
    assurance_archive = assurance.get('archive')
    assurance_image = assurance.get('image')
    if (not isinstance(assurance_archive, dict) or not isinstance(assurance_image, dict) or
            not re.fullmatch(r'[a-f0-9]{64}', str(assurance_archive.get('sha256', ''))) or
            not IMAGE_ID.fullmatch(str(assurance_image.get('config_digest', ''))) or
            not IMAGE_ID.fullmatch(str(assurance_image.get('manifest_digest', '')))):
        raise Blocked('Offline assurance lacks immutable archive, image and config digests')
    now = datetime.now(timezone.utc)
    try:
        expires = datetime.fromisoformat(approval['expires_at'].replace('Z', '+00:00'))
    except (KeyError, ValueError, TypeError):
        raise Blocked('Platform approval requires an explicit UTC expiry') from None
    if expires.tzinfo is None or expires <= now:
        raise Blocked('Platform approval has expired')
    expected = {'kind': 'gis-ai-go.devcontainer-platform-approval.v1', 'approved': True,
                'source_sha256': source['source_sha256'], 'image_reference': args.image,
                'source_review_sha256': sha(args.source_review),
                'image_review_sha256': sha(args.image_review), 'network': 'none',
                'profile': 'bduk'}
    if any(approval.get(key) != value for key, value in expected.items()):
        raise Blocked('Platform approval does not bind this full source, image, reviews and offline profile')
    if not approval.get('approved_by') or not approval.get('change_id'):
        raise Blocked('Platform approver and change reference are required')
    if (sr.get('kind') != 'gis-ai-go.full-source-review.v1' or sr.get('scope') != 'full-source' or
            sr.get('source_sha256') != source['source_sha256'] or sr.get('status') != 'PASS' or
            sr.get('coverage_checked') is not True or sr.get('unresolved_findings') != [] or
            not re.fullmatch(r'[a-f0-9]{64}', str(sr.get('canonical_report_sha256', '')))):
        raise Blocked('Full source review is missing, failed or refers to another tree')
    digest = args.image.rsplit('@', 1)[-1]
    if (ir.get('kind') != 'gis-ai-go.devcontainer-image-review.v1' or
            ir.get('image_reference') != args.image or ir.get('status') != 'PASS' or
            ir.get('signature_verified') is not True or ir.get('provenance_verified') is not True or
            ir.get('platform_policy_checked') is not True or ir.get('unresolved_findings') != [] or
            ir.get('assurance_receipt_sha256') != sha(args.assurance_receipt) or
            ir.get('oci_archive_sha256') != assurance_archive['sha256'] or
            ir.get('oci_manifest_digest') != digest or
            assurance.get('schema') != 'gis-ai-go.offline-image-assurance.v1' or
            assurance.get('status') != 'PASS' or assurance.get('network') != 'none' or
            assurance_image.get('requested_manifest_digest') != digest or
            assurance_image.get('resolved_uid') != 1000):
        raise Blocked('Immutable image review is missing, failed or refers to another image')
    # These are operator records, not cryptographic evidence of an approver's identity.
    return {'platform_approval_sha256': sha(args.approval),
            'source_review_sha256': sha(args.source_review),
            'image_review_sha256': sha(args.image_review),
            'assurance_receipt_sha256': sha(args.assurance_receipt), 'expires_at': approval['expires_at']}


def preflight(args: argparse.Namespace) -> dict:
    config = profile_check(args.profile)
    image = args.image or os.environ.get('GIS_AI_GO_SECURE_DEV_IMAGE' if args.profile == 'bduk'
                                         else 'GIS_AI_GO_DEV_IMAGE', '')
    args.image = image
    if not image:
        raise Blocked('Image is unconfigured; no pull or container open was attempted')
    source = source_manifest()
    if args.profile == 'bduk' and not IMAGE_REF.fullmatch(image):
        raise Blocked('BDUK requires an approved registry image digest; a local config digest is insufficient')
    review = review_gate(args, source) if args.profile == 'bduk' else {}
    workspace = workspace_check(args, source)
    return {'kind': 'gis-ai-go.devcontainer-admission.v1', 'status': 'PASS',
            'profile': args.profile, 'source_sha256': source['source_sha256'],
            'profile_sha256': sha(ROOT / '.devcontainer' / args.profile / 'devcontainer.json'),
            'image': inspect_image(image), 'reviews': review,
            'network': 'none', 'configuration': config, 'workspace': workspace,
            'notice': 'Manual readiness evidence; reopening and forwarding remain explicit host actions.'}


class StrictRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Blocked('Artifact redirects require a reviewed updated URL')


def secure_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise Blocked('Tooling mirrors must use HTTPS without embedded credentials')
    if parsed.query or parsed.fragment:
        raise Blocked('Tooling URLs cannot carry credentials in query/fragment')
    return url


def prepare_image(args: argparse.Namespace) -> dict:
    pins = lock()
    output = args.output.resolve()
    if output.exists():
        raise Blocked('Build context already exists; select a fresh output directory')
    context = ssl.create_default_context(cafile=str(args.ca_file) if args.ca_file else None)
    opener = urllib.request.build_opener(StrictRedirect(), urllib.request.HTTPSHandler(context=context))
    args.cache.mkdir(parents=True, exist_ok=True)
    for item in pins['artifacts']:
        dest = args.cache / item['name']
        if not dest.exists():
            if not args.download:
                raise Blocked('Verified artifact absent; explicit --download or pre-approved cache is required')
            url = secure_url(args.mirror.rstrip('/') + '/' + item['name'] if args.mirror else item['url'])
            with opener.open(url, timeout=60) as response:
                data = response.read(item['maximum_bytes'] + 1)
            if len(data) > item['maximum_bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise Blocked('Downloaded artifact exceeds bound or differs from reviewed digest')
            # No secrets or certificates are copied into the minimal build context.
            with dest.open('xb') as stream:
                stream.write(data)
        if dest.is_symlink() or dest.stat().st_size > item['maximum_bytes'] or sha(dest) != item['sha256']:
            raise Blocked('Tooling cache digest mismatch: ' + item['name'])
    output.mkdir(parents=True)
    (output / 'inputs').mkdir()
    for name in IMAGE_FILES:
        shutil.copyfile(ROOT / '.devcontainer/image' / name, output / name)
    for item in pins['artifacts']:
        shutil.copyfile(args.cache / item['name'], output / 'inputs' / item['name'])
    result = {'kind': 'gis-ai-go.dev-image-context.v1', 'platform': pins['platform'],
              'files': [{'path': str(path.relative_to(output)), 'sha256': sha(path),
                         'bytes': path.stat().st_size} for path in sorted(output.rglob('*')) if path.is_file()]}
    result['context_sha256'] = hashlib.sha256(canonical(result['files'])).hexdigest()
    (output / 'context-manifest.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def validate_context(context: Path) -> dict:
    manifest = load(context / 'context-manifest.json')
    expected = set(IMAGE_FILES) | {'inputs/' + item['name'] for item in lock()['artifacts']}
    actual = {str(path.relative_to(context)) for path in context.rglob('*') if path.is_file()}
    if actual != expected | {'context-manifest.json'} or any(path.is_symlink() for path in context.rglob('*')):
        raise Blocked('Build context includes extra files, links, source or secret material')
    entries = [{'path': name, 'sha256': sha(context / name), 'bytes': (context / name).stat().st_size}
               for name in sorted(expected)]
    if entries != manifest.get('files') or hashlib.sha256(canonical(entries)).hexdigest() != manifest.get('context_sha256'):
        raise Blocked('Build context changed after preparation')
    for name in IMAGE_FILES:
        if sha(context / name) != sha(ROOT / '.devcontainer/image' / name):
            raise Blocked('Build context differs from the reviewed image source')
    for item in lock()['artifacts']:
        if sha(context / 'inputs' / item['name']) != item['sha256']:
            raise Blocked('Staged tooling artifact differs from its immutable pin')
    return manifest


def build_image(args: argparse.Namespace) -> dict:
    manifest = validate_context(args.context)
    if args.output.exists():
        raise Blocked('Image output already exists; select a fresh path')
    builder = args.builder or os.environ.get('GIS_AI_GO_BUILDX_BUILDER')
    if not builder:
        raise Blocked('Explicit approved buildx OCI-capable builder is required')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    run(['docker', 'buildx', 'build', '--builder', builder, '--platform', 'linux/amd64',
         '--network=none', '--provenance=mode=max', '--file', str(args.context / 'Containerfile'),
         '--output', 'type=oci,dest=' + str(args.output), str(args.context)])
    return {'kind': 'gis-ai-go.dev-image-build.v1', 'status': 'BUILT_NOT_APPROVED',
            'context_sha256': manifest['context_sha256'], 'oci_sha256': sha(args.output),
            'oci_bytes': args.output.stat().st_size,
            'notice': 'Requires immutable OCI security review, platform approval and approved registry digest.'}


def check_tools(args: argparse.Namespace) -> dict:
    expected = lock()['versions']
    checks = {'node': (['node', '--version'], 'v' + expected['node']),
              'pnpm': (['pnpm', '--version'], expected['pnpm']),
              'python': (['python3', '--version'], 'Python ' + expected['python']),
              'uv': (['uv', '--version'], 'uv ' + expected['uv']),
              'terraform': (['terraform', 'version'], 'Terraform v' + expected['terraform'])}
    result = {}
    for name, (command, wanted) in checks.items():
        if not shutil.which(command[0]):
            raise Blocked('Pinned tool is absent: ' + name)
        observed = run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.splitlines()[0]
        if name == 'uv' and re.fullmatch(r'uv 0\.12\.2(?: \([A-Za-z0-9_+.:/ -]{1,128}\))?', observed):
            observed = 'uv 0.12.2'
        if observed != wanted:
            raise Blocked('Wrong tool version: ' + name + '; require ' + wanted)
        result[name] = wanted
    for tool in ('git', 'bash'):
        result[tool] = run([tool, '--version'], stdout=subprocess.PIPE).stdout.splitlines()[0]
    if args.container:
        if os.getuid() == 0 or os.environ.get('SSH_AUTH_SOCK') or Path('/var/run/docker.sock').exists():
            raise Blocked('Container is root, forwards an SSH agent or exposes Docker')
        status = Path('/proc/self/status').read_text()
        if not re.search(r'^NoNewPrivs:\s+1$', status, re.M) or not re.search(r'^CapEff:\s+0+$', status, re.M):
            raise Blocked('Container privilege controls are absent')
        helper = subprocess.run(['git', 'config', '--global', '--get-all', 'credential.helper'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if helper.returncode not in (0, 1) or helper.stdout.strip():
            raise Blocked('Git credential forwarding/configuration is present or cannot be inspected')
        for path in (Path.home() / '.ssh', Path.home() / '.aws', Path.home() / '.config/gcloud'):
            if path.exists() and any(path.rglob('*')):
                raise Blocked('Home contains an unapproved credential/configuration mount')
        names = ('GOOGLE_APPLICATION_CREDENTIALS', 'GOOGLE_OAUTH_ACCESS_TOKEN',
                 'CLOUDSDK_AUTH_ACCESS_TOKEN', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
                 'GITHUB_TOKEN', 'GH_TOKEN', 'SSH_AUTH_SOCK')
        if any(os.environ.get(name) for name in names):
            raise Blocked('Unapproved authentication binding is present')
        # Blanking SSH_AUTH_SOCK does not remove a forwarding socket installed by
        # the host editor or Docker Desktop. Inspect the effective filesystem too.
        forwarded = list(Path('/tmp').glob('vscode-ssh-auth*'))
        forwarded += list(Path('/tmp').glob('ssh-*/agent*'))
        forwarded.append(Path('/run/host-services/ssh-auth.sock'))
        if any(path.exists() for path in forwarded):
            raise Blocked('An editor/host SSH forwarding socket is present')
        mounts = Path('/proc/self/mountinfo').read_text()
        if re.search(r'(?:docker\.sock|ssh-auth\.sock|/\.ssh(?:/|\s)|/\.aws(?:/|\s)|/gcloud(?:/|\s))', mounts):
            raise Blocked('Effective mounts include Docker or host credential material')
    return {'kind': 'gis-ai-go.dev-tool-check.v1', 'status': 'PASS', 'tools': result}


def install(args: argparse.Namespace) -> dict:
    args.container = args.container or bool(os.environ.get('GIS_AI_GO_ENVIRONMENT_PROFILE'))
    check_tools(args)
    before = {name: sha(ROOT / name) for name in ('pnpm-lock.yaml', 'uv.lock', 'package.json', 'pyproject.toml')}
    # Frozen caches only. No dependency hooks, toolchain downloads, auth or cloud action.
    pnpm_store = getattr(args, 'pnpm_store', None) or ROOT / '.pnpm-store'
    uv_cache = getattr(args, 'uv_cache', None) or ROOT / '.uv-cache'
    run(['pnpm', 'install', '--frozen-lockfile', '--offline', '--ignore-scripts',
         '--package-import-method=copy',
         '--store-dir', str(pnpm_store)], cwd=ROOT)
    run(['uv', 'sync', '--locked', '--offline', '--no-managed-python', '--no-build',
         '--python', 'python3', '--cache-dir', str(uv_cache)], cwd=ROOT)
    if any(sha(ROOT / name) != digest for name, digest in before.items()):
        raise Blocked('Frozen dependency installation changed an input lock')
    return {'kind': 'gis-ai-go.dev-dependency-install.v1', 'status': 'PASS',
            'locks': before, 'offline': True, 'dependency_scripts': False}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('source-manifest').add_argument('--output', type=Path)
    sub.add_parser('workspace-manifest').add_argument('--output', type=Path, required=True)
    for command in ('preflight', 'admit'):
        q = sub.add_parser(command)
        q.add_argument('--profile', choices=('local', 'cloud', 'bduk'), default='local')
        q.add_argument('--image')
        for flag in ('source-review', 'image-review', 'assurance-receipt', 'workspace-review', 'approval'):
            q.add_argument('--' + flag, type=Path)
        q.add_argument('--output', type=Path)
    q = sub.add_parser('prepare-image')
    q.add_argument('--output', type=Path, required=True)
    q.add_argument('--cache', type=Path, default=ROOT / 'artifacts/environment/downloads')
    q.add_argument('--download', action='store_true', help='Explicit verified public artifact acquisition')
    q.add_argument('--mirror', help='Approved HTTPS mirror root; pinned bytes must match')
    q.add_argument('--ca-file', type=Path, help='Approved combined CA bundle; never baked into image')
    q = sub.add_parser('build-image')
    q.add_argument('--context', type=Path, required=True)
    q.add_argument('--output', type=Path, required=True)
    q.add_argument('--builder', help='Existing approved buildx OCI-capable builder')
    sub.add_parser('check').add_argument('--container', action='store_true')
    q = sub.add_parser('install')
    q.add_argument('--container', action='store_true')
    q.add_argument('--pnpm-store', type=Path, help='Approved offline cache; defaults to checkout .pnpm-store')
    q.add_argument('--uv-cache', type=Path, help='Approved offline cache; defaults to checkout .uv-cache')
    return p


def main() -> int:
    args = parser().parse_args()
    try:
        commands = {'source-manifest': lambda _: source_manifest(),
                    'workspace-manifest': lambda _: workspace_manifest(), 'preflight': preflight,
                    'admit': preflight, 'prepare-image': prepare_image, 'build-image': build_image,
                    'check': check_tools, 'install': install}
        result = commands[args.command](args)
        if getattr(args, 'output', None) and args.command in ('admit', 'preflight', 'source-manifest', 'workspace-manifest'):
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open('x') as stream:
                json.dump(result, stream, indent=2)
                stream.write('\n')
            args.output.chmod(0o600)
            if args.command in ('source-manifest', 'workspace-manifest'):
                result = {key: value for key, value in result.items() if key != 'files'} | {'files': len(result['files'])}
        print(json.dumps(result, indent=2))
        return 0
    except (Blocked, OSError, ValueError, subprocess.CalledProcessError) as error:
        # Do not print subprocess output, proxy URLs, credentials or arbitrary server text.
        reason = str(error) if isinstance(error, Blocked) else type(error).__name__
        print(json.dumps({'status': 'BLOCKED', 'reason': reason}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
