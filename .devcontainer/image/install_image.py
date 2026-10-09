#!/usr/bin/env python3
"""Install verified staged tooling offline; never used as a container open hook."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import tarfile
import zipfile

lock = json.loads(Path('/usr/share/gis-ai-go/toolchain.lock.json').read_text())
inputs = Path('/tmp/inputs')
for artifact in lock['artifacts']:
    path = inputs / artifact['name']
    if path.is_symlink() or path.stat().st_size > artifact['maximum_bytes']:
        raise SystemExit('Invalid staged tooling file')
    if hashlib.sha256(path.read_bytes()).hexdigest() != artifact['sha256']:
        raise SystemExit('Staged tooling digest mismatch: ' + artifact['name'])

pnpm = Path('/usr/local/lib/pnpm')
pnpm.mkdir()
with tarfile.open(inputs / 'pnpm-10.33.2.tgz') as archive:
    archive.extractall(pnpm, filter='data')
os.symlink('/usr/local/lib/pnpm/package/bin/pnpm.cjs', '/usr/local/bin/pnpm')
os.symlink('/usr/local/lib/pnpm/package/bin/pnpx.cjs', '/usr/local/bin/pnpx')

with zipfile.ZipFile(inputs / 'uv-0.12.2.whl') as archive:
    for tool in ('uv', 'uvx'):
        matches = [name for name in archive.namelist() if name.endswith('.data/scripts/' + tool)]
        if len(matches) != 1:
            raise SystemExit('Unexpected uv archive layout')
        target = Path('/usr/local/bin') / tool
        target.write_bytes(archive.read(matches[0]))
        target.chmod(0o755)
with zipfile.ZipFile(inputs / 'terraform_1.13.4_linux_amd64.zip') as archive:
    target = Path('/usr/local/bin/terraform')
    target.write_bytes(archive.read('terraform'))
    target.chmod(0o755)

expected = {
    ('node', '--version'): 'v24.19.0',
    ('pnpm', '--version'): '10.33.2',
    ('python3', '--version'): 'Python 3.12.14',
    ('uv', '--version'): 'uv 0.12.2',
    ('terraform', 'version'): 'Terraform v1.13.4',
}
for args, version in expected.items():
    observed = subprocess.check_output(args, text=True).splitlines()[0]
    # The verified PyPI wheel prints its compiled target after the exact version.
    if args[0] == 'uv' and re.fullmatch(r'uv 0\.12\.2(?: \([A-Za-z0-9_+.:/ -]{1,128}\))?', observed):
        observed = 'uv 0.12.2'
    if observed != version:
        raise SystemExit('Toolchain version mismatch: ' + args[0])
for tool in ('git', 'bash'):
    subprocess.run([tool, '--version'], check=True, stdout=subprocess.DEVNULL)
