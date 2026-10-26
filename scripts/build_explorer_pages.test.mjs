import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { guides, routeTarget, safePath, validateApp, validateLegacy, validateProjection } from './build_explorer_pages.mjs';

const sha = value => crypto.createHash('sha256').update(value).digest('hex');
const rawJson = value => Buffer.from(JSON.stringify(value) + '\n');
const source = 'a'.repeat(40);
const snapshot = 'okf-plus-' + 'b'.repeat(24);
const inputDigest = 'c'.repeat(64);
const canonicalUrl = 'https://chris-page-gov.github.io/gis-ai-go/';
const publicationBase = canonicalUrl + 'gis/explorer/context/';
const capturedAt = '2026-10-24T11:06:00Z';
async function temp(context) { const root = await fs.mkdtemp(path.join(os.tmpdir(), 'gis-pages-assembler-')); context.after(() => fs.rm(root, { recursive: true, force: true })); return root; }
async function write(root, name, raw) { const file = path.join(root, name); await fs.mkdir(path.dirname(file), { recursive: true }); await fs.writeFile(file, raw); return { path: name, bytes: Buffer.byteLength(raw), sha256: sha(raw) }; }
const byPath = (a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0;

test('root opens the canonical GIS bundle under the actual project prefix', () => {
  assert.equal(routeTarget(canonicalUrl), canonicalUrl + 'explorer/explore/?bundle=https%3A%2F%2Fchris-page-gov.github.io%2Fgis-ai-go%2Fgis%2Fexplorer%2Fokf-explorer.json#overview');
  const local = new URL(routeTarget('http://127.0.0.1:4190/gis-ai-go/'));
  assert.equal(local.pathname, '/gis-ai-go/explorer/explore/');
  assert.equal(local.searchParams.get('bundle'), 'http://127.0.0.1:4190/gis-ai-go/gis/explorer/okf-explorer.json');
});

test('old explicit catalogue links retain exact search and record state through legacy', () => {
  const search = '?view=cards&q=inspire&type=dataset&tag=a&tag=b';
  const hash = '#record=hmlr%3Adataset%3Ainspire-index-polygons';
  assert.equal(routeTarget(canonicalUrl + search + hash), canonicalUrl + 'legacy/' + search + hash);
  assert.equal(routeTarget(canonicalUrl + '#record=unknown'), canonicalUrl + 'legacy/#record=unknown');
});

test('new record/highlight routes survive and redirect-like parameters cannot change the destination', () => {
  const url = new URL(routeTarget(canonicalUrl + '?next=https://outside.invalid/&explore=%7B%7D#records/geospatial-concepts/height-datum.md'));
  assert.equal(url.origin, new URL(canonicalUrl).origin);
  assert.equal(url.pathname, '/gis-ai-go/explorer/explore/');
  assert.equal(url.searchParams.get('explore'), '{}');
  assert.equal(url.hash, '#records/geospatial-concepts/height-datum.md');
  assert.equal(url.searchParams.get('bundle'), canonicalUrl + 'gis/explorer/okf-explorer.json');
});

test('unsafe/private distribution paths are refused', () => {
  for (const name of ['../escape', '/absolute', 'a//b', 'a\\b', 'a/./b', '.git/config', 'explorer/research/data', 'node_modules/x', 'a.js.map', 'x\0y', 'docs/.DS_Store']) assert.throws(() => safePath(name));
  assert.equal(safePath('explorer/docs/beginners/index.html'), 'explorer/docs/beginners/index.html');
});

async function appFixture(root) {
  const row = await write(root, 'index.html', '<html>Canonical app</html>');
  const manifest = { schema: 'okf-explorer-app-build-manifest.v1', algorithm: 'sha256-canonical-json-materials-v1', file_count: 1,
    tree_sha256: sha(rawJson([row])), materials: [row] };
  const manifestRaw = rawJson(manifest);
  await write(root, 'okf-explorer-build-manifest.json', manifestRaw);
  return { appTreeSha256: manifest.tree_sha256, appManifestSha256: sha(manifestRaw) };
}

test('canonical app validation rejects changed or unbound executable bytes', async context => {
  const root = await temp(context); const pin = await appFixture(root);
  await validateApp(root, pin);
  await write(root, 'extra.js', 'unexpected executable');
  await assert.rejects(validateApp(root, pin), /unbound files/);
  await fs.rm(path.join(root, 'extra.js'));
  await write(root, 'index.html', 'modified app');
  await assert.rejects(validateApp(root, pin), /byte binding mismatch/);
});

test('canonical app validation rejects symlinked and hard-linked inputs', async context => {
  const root = await temp(context); const pin = await appFixture(root);
  await fs.link(path.join(root, 'index.html'), path.join(root, 'hardlink.html'));
  await assert.rejects(validateApp(root, pin), /single-link/);
  await fs.rm(path.join(root, 'hardlink.html'));
  await fs.symlink(path.join(root, 'index.html'), path.join(root, 'link.html'));
  await assert.rejects(validateApp(root, pin), /single-link/);
});

async function projectionFixture(root, base = publicationBase) {
  await write(root, '.okf-plus-explorer', 'gis-ai-go.okf-plus-explorer-projection.v1\n');
  const rows = [];
  rows.push(await write(root, 'context/base-index.json', rawJson({ records: [] })));
  rows.push(await write(root, 'context/manifest.json', rawJson({ schema: 'okf-context-corpus.v3',
    bundle: { source_url: base + 'manifest.json', snapshot }, semantic_source_snapshot: snapshot })));
  const contextRows = rows.map(row => ({ ...row, path: row.path.slice(8) })).sort(byPath);
  rows.push(await write(root, 'context/projection-manifest.json', rawJson({ snapshot, inputDigest, sourceRevision: source, capturedAt, outputs: contextRows })));
  rows.push(await write(root, 'okf-explorer.json', rawJson({ source: { revision: source, inputDigest }, snapshot, counts: { records: 1 } })));
  await write(root, 'projection-manifest.json', rawJson({ schema: 'gis-ai-go.okf-plus-explorer-projection.v1',
    sourceRevision: source, inputDigest, snapshot, capturedAt, readerRecords: 1, outputs: rows.sort(byPath) }));
}

test('complete Reader/context closure is required and localhost bindings cannot be published', async context => {
  const root = await temp(context); await projectionFixture(root);
  await validateProjection(root, source, { contextPublicationBase: publicationBase, capturedAt });
  await write(root, 'unbound-record.json', '{}');
  await assert.rejects(validateProjection(root, source, { contextPublicationBase: publicationBase, capturedAt }), /unbound or missing/);
  await fs.rm(path.join(root, 'unbound-record.json'));
  const local = await temp(context); await projectionFixture(local, 'http://127.0.0.1:8130/gis/explorer/context/');
  await assert.rejects(validateProjection(local, source, { contextPublicationBase: publicationBase, capturedAt }), /localhost bindings/);
});

test('a different GIS revision cannot acquire the reviewed projection identity', async context => {
  const root = await temp(context); await projectionFixture(root);
  await assert.rejects(validateProjection(root, 'd'.repeat(40), { contextPublicationBase: publicationBase, capturedAt }), /requested GIS source/);
});

test('legacy distribution is source-bound and cannot carry unrelated extra files', async context => {
  const root = await temp(context);
  await write(root, 'index.html', '<link rel="icon" href="./favicon.svg"><script src="./app.js"></script>');
  await write(root, 'favicon.svg', '<svg/>'); await write(root, 'app.js', 'legacy();');
  await write(root, 'catalogue/.explorer-generated', 'gis-ai-go-public-explorer-data.v1\n');
  const rows = [];
  for (const name of ['manifest.json', 'okf-bundle.json', 'okf-bundle.jsonld', 'okf-explorer.json']) rows.push(await write(root, 'catalogue/' + name, '{}'));
  rows.push(await write(root, 'catalogue/build-receipt.json', rawJson({ revision: source, version: '0.1.0', contentRootSha256: inputDigest,
    manifestSha256: rows[0].sha256, builder: 'synthetic fixture', builderVersion: '1.0.0' })));
  await write(root, 'catalogue/CHECKSUMS.sha256', rows.sort(byPath).map(row => `${row.sha256}  ${row.path.slice(10)}\n`).join(''));
  await validateLegacy(root, source, '0.1.0');
  await assert.rejects(validateLegacy(root, 'd'.repeat(40), '0.1.0'), /source\/version/);
  await write(root, 'notes.txt', 'not a publication input');
  await assert.rejects(validateLegacy(root, source, '0.1.0'), /unbound files/);
});

test('guide derivatives keep local core links and send excluded research to exact authored source', async context => {
  const root = await temp(context); const site = path.join(root, '_site');
  const pin = { sourceCommit: source, repository: 'chris-page-gov/okf-explorer' };
  const rows = [];
  rows.push(await write(site, 'docs/onboarding/index.html', '<html><body><main><a href="../beginners/index.html">Beginner</a><a href="../../research/report.html#stable-heading">Report</a></main></body></html>'));
  rows.push(await write(site, 'docs/beginners/index.html', '<html><body><main>Beginner guide</main></body></html>'));
  await write(root, 'research/report.md', '# Stable heading\n\nPublic source evidence.\n');
  await write(site, 'okf-publication-identity.json', rawJson({ schema: 'okf-publication-deployment-identity.v1', commit: source }));
  await write(root, '.site-components/assembly/site-assembly-manifest.json', rawJson({ tree_sha256: 'e'.repeat(64), materials: rows }));
  const selected = await guides(root, site, new Map(), pin);
  const html = selected.get('docs/onboarding/index.html').derived.toString();
  assert.match(html, /href="\.\.\/beginners\/index.html"/);
  assert.ok(html.includes(`https://github.com/chris-page-gov/okf-explorer/blob/${source}/research/report.md#stable-heading`));
  assert.match(html, /Additional source references open online/);
  assert.ok(!selected.has('research/report.html'));
  const provenance = JSON.parse(selected.get('GUIDE-PROVENANCE.json').derived);
  assert.equal(provenance.rewrites.length, 1);
  assert.equal(provenance.rewrites[0].source, 'research/report.md');
});

test('guide provenance refuses stale Site identity and unbound guide bytes', async context => {
  const root = await temp(context); const site = path.join(root, '_site');
  const pin = { sourceCommit: source, repository: 'chris-page-gov/okf-explorer' };
  const rows = [await write(site, 'docs/onboarding/index.html', '<main>Guide</main>'),
    await write(site, 'docs/beginners/index.html', '<main>Beginner</main>')];
  await write(site, 'okf-publication-identity.json', rawJson({ schema: 'okf-publication-deployment-identity.v1', commit: 'f'.repeat(40) }));
  await write(root, '.site-components/assembly/site-assembly-manifest.json', rawJson({ tree_sha256: 'e'.repeat(64), materials: rows }));
  await assert.rejects(guides(root, site, new Map(), pin), /pinned source commit/);
  await write(site, 'okf-publication-identity.json', rawJson({ schema: 'okf-publication-deployment-identity.v1', commit: source }));
  await write(site, 'docs/onboarding/index.html', '<main>Altered after Site assembly</main>');
  await assert.rejects(guides(root, site, new Map(), pin), /assembled Site material/);
});
