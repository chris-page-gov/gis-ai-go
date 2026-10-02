// Exact-source offline package for the separate experimental Sites profile.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdir, readFile, readdir, realpath, writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createVerifiedFileLoader, planOutputDirectory, createOutputDirectory } from './package_web216_hosted_runtime.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
assert(args.length === 4 && args[0] === '--tooling-root' && args[2] === '--output-dir',
  'Use --tooling-root <pinned Site tooling> --output-dir <new directory outside source>');
const tooling = await realpath(resolve(args[1]));
const destination = await planOutputDirectory(args[3], [root, tooling]);
const git = (...values) => execFileSync('git', values, { cwd: root, maxBuffer: 8_388_608 });
const revision = git('rev-parse', 'HEAD').toString().trim();
assert.equal(git('status', '--porcelain', '--untracked-files=all').toString(), '', 'Package only a clean committed source');
assert.equal(JSON.parse(await readFile(join(tooling, 'node_modules/esbuild/package.json'))).version, '0.28.1');
const require = createRequire(join(tooling, 'package.json'));
const { build } = await import(pathToFileURL(require.resolve('esbuild')).href);
const loader = createVerifiedFileLoader({ root: await realpath(root), trackedBytes: path => git('show', `${revision}:${path}`) });
const supporting = ['pnpm-lock.yaml', 'scripts/package_sites_pilot_runtime.mjs', 'scripts/package_web216_hosted_runtime.mjs', 'LICENSE'];
for (const path of supporting) await loader.capture(path);
const compiled = await build({ absWorkingDir: root, entryPoints: ['scripts/sites_pilot_bundle_entry.ts'], bundle: true,
  write: false, format: 'esm', platform: 'neutral', target: 'es2023', conditions: ['workerd'], external: ['node:*'],
  metafile: true, plugins: [loader.plugin], nodePaths: [join(root, 'apps/mcp-gateway/node_modules')],
  alias: { '@gis-ai-go/evidence/web216-pure': join(root, 'packages/evidence/src/web216-pure.ts'),
    '@gis-ai-go/provider-adapter-sdk/sites-pilot': join(root, 'packages/provider-adapter-sdk/src/sites-pilot-providers.ts') },
});
assert.equal(compiled.outputFiles.length, 1);
const bytes = compiled.outputFiles[0].contents;
assert(bytes.byteLength > 0 && bytes.byteLength <= 4_194_304);
const imports = [...new Set(Object.values(compiled.metafile.outputs).flatMap(x => x.imports.map(y => y.path)))].sort();
assert(imports.every(path => ['node:crypto', 'node:util', 'node:async_hooks'].includes(path)), 'Unexpected external module');
const paths = [...new Set([...Object.keys(compiled.metafile.inputs), ...supporting])].sort();
assert(paths.some(path => path.endsWith('/shimsWorkerd.mjs')));
assert(!paths.some(path => /\/shims(?:Node|Browser)\.mjs$/.test(path) || path.includes('packages/evidence/dist/')));
const inputs = paths.map(path => loader.entry(path).material);
const digest = data => createHash('sha256').update(data).digest('hex');
const dependencies = new Map();
const retained = new Map();
for (const path of paths) {
  const { actual, content, material } = loader.entry(path);
  retained.set(material.sha256, content);
  if (material.binding !== 'observed-installed-dependency-bytes') continue;
  let directory = dirname(actual), found = false;
  while (directory.startsWith(join(root, 'node_modules') + '/')) {
    let dependency;
    try { dependency = JSON.parse(await readFile(join(directory, 'package.json'), 'utf8')); }
    catch (error) { if (error.code !== 'ENOENT') throw error; }
    if (typeof dependency?.name === 'string' && typeof dependency?.version === 'string') {
      if (!dependencies.has(directory)) {
        const notices = [];
        for (const name of (await readdir(directory)).filter(name => /^(?:licen[sc]e|notice|copying)(?:[.-].*)?$/iu.test(name)).sort()) {
          const text = await readFile(join(directory, name), 'utf8');
          assert(Buffer.byteLength(text) <= 262_144);
          notices.push({ name, text });
        }
        assert(notices.length > 0, `Missing licence notice for ${dependency.name}`);
        dependencies.set(directory, { name: dependency.name, version: dependency.version, licence: dependency.license ?? null, notices });
      }
      found = true; break;
    }
    directory = dirname(directory);
  }
  assert(found, 'Dependency has no named package manifest');
}
const thirdParty = [...dependencies.values()].sort((a, b) => a.name.localeCompare(b.name));
const notices = thirdParty.map(item => `${item.name} ${item.version}\n${item.notices.map(notice => `${notice.name}\n${notice.text}`).join('\n')}`).join('\n\n') + '\n';
const manifest = { schema: 'gis-ai-go.sites-pilot-package.v1', source_revision: revision,
  bundle: { path: 'sites-pilot-runtime.mjs', bytes: bytes.byteLength, sha256: digest(bytes) }, inputs,
  compiler: { name: 'esbuild', version: '0.28.1' }, external_imports: imports,
  third_party_notices: { path: 'third-party-notices.txt', sha256: digest(notices),
    dependencies: thirdParty.map(({name, version, licence}) => ({name, version, licence})) },
  boundary: { deployed: false, attested: false, native_sites_mcp_declared: false,
    provider_egress_possible_only_after_runtime_admission: true, source_identity_not_independent_attestation: true } };
assert.equal(git('rev-parse', 'HEAD').toString().trim(), revision);
assert.equal(git('status', '--porcelain', '--untracked-files=all').toString(), '');
const output = await createOutputDirectory(destination);
await mkdir(join(output, 'inputs'), {mode: 0o700});
for (const [hash, content] of retained) await writeFile(join(output, 'inputs', hash), content, {flag: 'wx', mode: 0o600});
await writeFile(join(output, manifest.bundle.path), bytes, { flag: 'wx', mode: 0o600 });
await writeFile(join(output, 'bundle-manifest.json'), JSON.stringify(manifest, null, 2) + '\n', { flag: 'wx', mode: 0o600 });
await writeFile(join(output, 'LICENSE'), loader.entry('LICENSE').content, { flag: 'wx', mode: 0o600 });
await writeFile(join(output, 'third-party-notices.txt'), notices, { flag: 'wx', mode: 0o600 });
console.log(JSON.stringify({ source_revision: revision, sha256: manifest.bundle.sha256, bytes: bytes.byteLength, output }));
