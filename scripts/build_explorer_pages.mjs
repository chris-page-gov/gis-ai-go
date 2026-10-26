import fs from 'node:fs/promises';
import { constants } from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PIN_PATH = path.join(ROOT, 'config/explorer-publication.json');
const MANIFEST = 'EXPLORER-DISTRIBUTION.json';
const MAX_FILE_BYTES = 32 * 1024 * 1024;
// Six archive entries are reserved for .nojekyll and publication metadata.
const MAX_FILES = 49_994;
const MAX_TOTAL_BYTES = 999_999_999;
const MAX_GUIDE_BYTES = 40 * 1024 * 1024;
const SHA = /^[0-9a-f]{64}$/;
const COMMIT = /^[0-9a-f]{40}$/;
const GUIDE_ROOTS = ['docs/', 'profile/'];
const GUIDE_REFERENCES = ['profiles/', 'registry/', 'constraints/', 'catalogue/', 'stack/',
  'standards/', 'federated/', 'frameworks/', 'glossary/'];
const GUIDE_FILES = ['okf-bundle.json', 'okf-bundle.jsonld', 'okf-bundle.yamlld', 'okf-registry.json',
  'okf-estate-registry.json', 'okf.publication.json', 'LICENSE-CODE.md', 'LICENSE.md',
  'LICENSE-CODE.html', 'LICENSE.html', 'CHANGELOG.html'];

function requireThat(value, message) { if (!value) throw new Error(message); }
const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const jsonBytes = value => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const sorted = values => [...values].sort((a, b) => a < b ? -1 : a > b ? 1 : 0);
export function canonicalJsonBytes(value) {
  const ordered = item => Array.isArray(item) ? item.map(ordered)
    : item && typeof item === 'object' ? Object.fromEntries(sorted(Object.keys(item)).map(key => [key, ordered(item[key])])) : item;
  return Buffer.from(JSON.stringify(ordered(value), null, 2) + '\n');
}

export function safePath(value) {
  requireThat(typeof value === 'string' && value.length > 0 && !value.startsWith('/')
    && !value.includes('\\') && !/[\u0000-\u001f\u007f]/u.test(value)
    && !value.split('/').some(part => ['', '.', '..'].includes(part)), `Unsafe publication path: ${value}`);
  requireThat(!value.split('/').some(part => ['.git', 'node_modules', 'research', 'private'].includes(part.toLowerCase()))
    && !value.split('/').some(part => part.startsWith('.'))
    && !value.toLowerCase().endsWith('.map'), `Out-of-scope publication path: ${value}`);
  return value;
}

async function regular(file, maximum = MAX_FILE_BYTES) {
  const stat = await fs.lstat(file);
  requireThat(stat.isFile() && !stat.isSymbolicLink() && stat.nlink === 1, `Expected an ordinary single-link file: ${file}`);
  requireThat(stat.size <= maximum, `File exceeds ${maximum} bytes: ${file}`);
  return stat;
}

async function realDirectory(directory) {
  const stat = await fs.lstat(directory);
  requireThat(stat.isDirectory() && !stat.isSymbolicLink(), `Expected a real directory: ${directory}`);
}

async function readJson(file) { await regular(file); return JSON.parse(await fs.readFile(file, 'utf8')); }

async function inspectFile(file, relative) {
  const before = await regular(file);
  const handle = await fs.open(file, constants.O_RDONLY | (constants.O_NOFOLLOW || 0));
  try {
    const opened = await handle.stat();
    requireThat(opened.ino === before.ino && opened.dev === before.dev && opened.size === before.size,
      `Input changed while opening: ${relative}`);
    const hash = crypto.createHash('sha256'); let bytes = 0;
    for await (const chunk of handle.createReadStream({ autoClose: false })) { bytes += chunk.length; hash.update(chunk); }
    const after = await handle.stat();
    requireThat(bytes === before.size && after.size === before.size && after.mtimeMs === before.mtimeMs,
      `Input changed while reading: ${relative}`);
    return { path: relative, bytes, sha256: hash.digest('hex') };
  } finally { await handle.close(); }
}

async function inventory(root, { ignoredMarkers = new Set() } = {}) {
  await realDirectory(root); const rows = new Map(); let total = 0;
  async function walk(directory, prefix = '') {
    for (const entry of (await fs.readdir(directory, { withFileTypes: true })).sort((a, b) => a.name < b.name ? -1 : 1)) {
      const relative = prefix + entry.name;
      if (ignoredMarkers.has(relative)) { await regular(path.join(root, relative)); continue; }
      safePath(relative);
      requireThat(!relative.split('/').some(part => part.startsWith('.')),
        `Unexpected hidden input: ${relative}`);
      const target = path.join(directory, entry.name);
      const stat = await fs.lstat(target);
      if (stat.isDirectory() && !stat.isSymbolicLink()) await walk(target, relative + '/');
      else {
        requireThat(rows.size < MAX_FILES, 'Input exceeds the publication file limit');
        const row = await inspectFile(target, relative); total += row.bytes;
        requireThat(total <= MAX_TOTAL_BYTES, 'Input exceeds the publication byte limit');
        rows.set(relative, row);
      }
    }
  }
  await walk(root); return rows;
}

function requireRows(rows, bindings, label) {
  requireThat(Array.isArray(bindings) && bindings.length > 0, `${label} has no bound files`);
  const paths = bindings.map(row => safePath(row.path));
  requireThat(paths.length === new Set(paths).size && JSON.stringify(paths) === JSON.stringify(sorted(paths)),
    `${label} file paths must be unique and sorted`);
  for (const binding of bindings) {
    const row = rows.get(binding.path);
    requireThat(Number.isSafeInteger(binding.bytes) && binding.bytes >= 0 && SHA.test(binding.sha256)
      && row?.bytes === binding.bytes && row?.sha256 === binding.sha256, `${label} byte binding mismatch: ${binding.path}`);
  }
}

export async function validateApp(root, pin) {
  const rows = await inventory(root);
  const manifestRow = rows.get('okf-explorer-build-manifest.json');
  requireThat(manifestRow?.sha256 === pin.appManifestSha256, 'Canonical app manifest differs from the reviewed pin');
  const app = await readJson(path.join(root, 'okf-explorer-build-manifest.json'));
  requireThat(app.schema === 'okf-explorer-app-build-manifest.v1'
    && app.algorithm === 'sha256-canonical-json-materials-v1'
    && app.tree_sha256 === pin.appTreeSha256 && app.file_count === app.materials?.length,
  'Canonical app identity differs from the reviewed pin');
  requireRows(rows, app.materials, 'Canonical app');
  requireThat(digest(Buffer.from(JSON.stringify(app.materials) + '\n')) === app.tree_sha256,
    'Canonical app tree digest differs from its materials');
  requireThat(rows.size === app.materials.length + 1 && !app.materials.some(row => row.path === manifestRow.path),
    'Canonical app has unbound files');
  return { rows, app };
}

export async function validateProjection(root, sourceCommit, pin) {
  const rows = await inventory(root, { ignoredMarkers: new Set(['.okf-plus-explorer']) });
  requireThat(await fs.readFile(path.join(root, '.okf-plus-explorer'), 'utf8') === 'gis-ai-go.okf-plus-explorer-projection.v1\n',
    'Reader projection marker differs from the generated source contract');
  const report = await readJson(path.join(root, 'projection-manifest.json'));
  requireThat(report.schema === 'gis-ai-go.okf-plus-explorer-projection.v1'
    && report.sourceRevision === sourceCommit && report.capturedAt === pin.capturedAt && SHA.test(report.inputDigest)
    && typeof report.snapshot === 'string' && report.snapshot.startsWith('okf-plus-'),
  'Reader projection does not bind the requested GIS source');
  requireRows(rows, report.outputs, 'Reader projection');
  requireThat(rows.size === report.outputs.length + 1, 'Reader projection has unbound or missing files');
  const descriptor = await readJson(path.join(root, 'okf-explorer.json'));
  const context = await readJson(path.join(root, 'context/manifest.json'));
  const contextReport = await readJson(path.join(root, 'context/projection-manifest.json'));
  requireThat(descriptor.source?.revision === sourceCommit && descriptor.source?.inputDigest === report.inputDigest
    && descriptor.snapshot === report.snapshot && descriptor.counts?.records === report.readerRecords,
  'Reader descriptor source or count differs from its projection');
  requireThat(context.schema === 'okf-context-corpus.v3' && context.bundle?.source_url === pin.contextPublicationBase + 'manifest.json'
    && context.bundle?.snapshot === report.snapshot && context.semantic_source_snapshot === report.snapshot
    && contextReport.sourceRevision === sourceCommit && contextReport.capturedAt === pin.capturedAt
    && contextReport.inputDigest === report.inputDigest && contextReport.snapshot === report.snapshot,
  'Context must be regenerated for this exact public source and URL; localhost bindings cannot be published');
  const contextRows = new Map([...rows].filter(([name]) => name.startsWith('context/'))
    .map(([name, row]) => [name.slice(8), { ...row, path: name.slice(8) }]));
  requireRows(contextRows, contextReport.outputs, 'Context projection');
  return { rows, report, descriptor, context };
}

export async function validateLegacy(root, sourceCommit, version) {
  const rows = await inventory(root, { ignoredMarkers: new Set(['catalogue/.explorer-generated']) });
  const marker = path.join(root, 'catalogue/.explorer-generated');
  requireThat(await fs.readFile(marker, 'utf8') === 'gis-ai-go-public-explorer-data.v1\n', 'Legacy catalogue marker differs');
  rows.set('catalogue/.explorer-generated', await inspectFile(marker, 'catalogue/.explorer-generated'));
  const ledger = await fs.readFile(path.join(root, 'catalogue/CHECKSUMS.sha256'), 'utf8');
  requireThat(ledger.endsWith('\n'), 'Legacy catalogue checksums need a final newline');
  const bindings = ledger.trimEnd().split('\n').map(line => {
    const match = /^([0-9a-f]{64})  (.+)$/.exec(line);
    requireThat(match, 'Invalid legacy checksum ledger');
    const name = safePath(match[2]);
    return { path: 'catalogue/' + name, sha256: match[1], bytes: rows.get('catalogue/' + name)?.bytes };
  });
  requireRows(rows, bindings, 'Legacy catalogue');
  const cataloguePaths = sorted([...rows.keys()].filter(name => name.startsWith('catalogue/')));
  requireThat(JSON.stringify(cataloguePaths) === JSON.stringify(sorted([
    'catalogue/.explorer-generated', 'catalogue/CHECKSUMS.sha256', ...bindings.map(row => row.path),
  ])), 'Legacy catalogue inventory is not exact');
  const receipt = await readJson(path.join(root, 'catalogue/build-receipt.json'));
  requireThat(receipt.revision === sourceCommit && receipt.version === version,
    'Legacy catalogue identity differs from the selected GIS source/version');
  for (const name of ['manifest.json', 'okf-bundle.json', 'okf-bundle.jsonld', 'okf-explorer.json']) {
    requireThat(rows.has('catalogue/' + name), `Legacy catalogue is missing ${name}`);
  }
  requireThat(SHA.test(receipt.contentRootSha256) && receipt.manifestSha256 === rows.get('catalogue/manifest.json').sha256
    && typeof receipt.builder === 'string' && receipt.builder.length > 0
    && typeof receipt.builderVersion === 'string' && receipt.builderVersion.length > 0,
  'Legacy catalogue receipt does not bind its manifest and builder');
  const index = await fs.readFile(path.join(root, 'index.html'), 'utf8');
  const references = new Set();
  for (const match of index.matchAll(/(?:href|src)=["']([^"']+)["']/gu)) {
    const raw = match[1]; if (raw.startsWith('#')) continue;
    requireThat(!/^(?:[a-z]+:|\/)/iu.test(raw), `Legacy entry has a non-relative asset: ${raw}`);
    references.add(safePath(decodeURIComponent(raw.split(/[?#]/u)[0]).replace(/^\.\//u, '')));
  }
  requireThat(references.has('favicon.svg'), 'Legacy entry does not bind its favicon');
  const expected = sorted(new Set(['index.html', ...cataloguePaths, ...references]));
  requireThat(JSON.stringify(sorted(rows.keys())) === JSON.stringify(expected), 'Legacy distribution contains unbound files');
  return rows;
}

export function routeTarget(href) {
  const current = new URL(href); const base = new URL('./', current);
  const legacyKeys = new Set(['q', 'view', 'type', 'authority', 'access', 'rights', 'freshness', 'tag']);
  const legacy = [...current.searchParams.keys()].some(key => legacyKeys.has(key)) || current.hash.startsWith('#record=');
  const target = new URL(legacy ? './legacy/' : './explorer/explore/', base);
  target.search = current.search;
  target.hash = current.hash;
  if (!legacy) {
    if (!target.searchParams.has('bundle')) target.searchParams.set('bundle', new URL('./gis/explorer/okf-explorer.json', base).href);
    if (!target.hash) target.hash = '#overview';
  }
  return target.href;
}

const ROUTER = `${routeTarget.toString()}\nlocation.replace(routeTarget(location.href));\n`;
const STYLE = 'body{font:1rem/1.5 system-ui,sans-serif;max-width:48rem;margin:3rem auto;padding:0 1rem;color:#17202a}a{color:#005ea5}a:focus-visible{outline:3px solid #ffdd00;outline-offset:3px}li{margin:.75rem 0}\n';
const INDEX = `<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'">
<title>GIS AI GO Explorer</title><link rel="stylesheet" href="./style.css"><script src="./router.js" defer></script></head>
<body><main><h1>GIS AI GO Explorer</h1><p>Opening the OS and ONS knowledge Explorer.</p>
<p>Browse source-linked metadata, inspect field explanations and follow the pavement width, building heights and road elevation learning paths.</p>
<ul><li><a href="./explorer/explore/?bundle=%2Fgis-ai-go%2Fgis%2Fexplorer%2Fokf-explorer.json#overview">Open the knowledge Explorer</a></li>
<li><a href="./explorer/docs/onboarding/index.html">Read the Explorer guide</a></li>
<li><a href="./legacy/">Open the earlier catalogue</a></li></ul>
<noscript><p>Interactive browsing requires JavaScript. Metadata remains available in the <a href="./gis/explorer/okf-explorer.json">Reader descriptor</a> and <a href="./catalogue/okf-bundle.json">earlier catalogue JSON</a>.</p></noscript>
</main></body></html>\n`;

async function sourceHref(checkout, sitePath, fragment, pin) {
  const candidates = sitePath.endsWith('.html') ? [sitePath.slice(0, -5) + '.md', sitePath] : [sitePath];
  if (sitePath.endsWith('/index.html')) candidates.push(sitePath.slice(0, -10) + 'README.md');
  for (const candidate of candidates) {
    try {
      const stat = await fs.lstat(path.join(checkout, candidate));
      if (!stat.isFile() || stat.isSymbolicLink()) continue;
      let stableFragment = fragment;
      if (fragment && candidate.endsWith('.md')) {
        const text = await fs.readFile(path.join(checkout, candidate), 'utf8');
        const headings = [...text.matchAll(/^#{1,6}\s+(.+)$/gmu)].map(match => match[1].trim().toLowerCase()
          .replace(/[^\p{L}\p{N}\s_-]/gu, '').replace(/\s/gu, '-'));
        if (!headings.includes(decodeURIComponent(fragment.slice(1)))) stableFragment = '';
      }
      const encoded = candidate.split('/').map(encodeURIComponent).join('/');
      return { candidate, href: `https://github.com/${pin.repository}/blob/${pin.sourceCommit}/${encoded}${stableFragment}` };
    } catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  return { candidate: null, href: `https://github.com/${pin.repository}/tree/${pin.sourceCommit}/` };
}

export async function guides(checkout, siteRoot, appRows, pin) {
  const assembly = await readJson(path.join(checkout, '.site-components/assembly/site-assembly-manifest.json'));
  const identity = await readJson(path.join(siteRoot, 'okf-publication-identity.json'));
  requireThat(identity.schema === 'okf-publication-deployment-identity.v1' && identity.commit === pin.sourceCommit,
    'Build the generated Explorer guides from the pinned source commit');
  requireThat(Array.isArray(assembly.materials), 'Assembled Site has no material inventory');
  const materials = new Map(assembly.materials.map(row => [row.path, row]));
  requireThat(materials.size === assembly.materials.length, 'Assembled Site repeats a material path');
  const selected = new Map(); const queue = [];
  const rewrites = []; const missing = [];
  let bytes = 0;
  async function add(name) {
    if (appRows.has(name) || selected.has(name)) return;
    safePath(name);
    const binding = materials.get(name);
    requireThat(binding, `Generated guide is absent from the assembled Site: ${name}`);
    const actual = await inspectFile(path.join(siteRoot, name), name);
    requireThat(actual.bytes === binding.bytes && actual.sha256 === binding.sha256,
      `Generated guide differs from its assembled Site material: ${name}`);
    bytes += actual.bytes; requireThat(bytes <= MAX_GUIDE_BYTES, 'Generated guide closure exceeds its 40 MiB budget');
    selected.set(name, { ...actual, source: path.join(siteRoot, name) });
    queue.push(name);
  }
  for (const name of sorted(materials.keys())) {
    if (GUIDE_ROOTS.some(prefix => name.startsWith(prefix)) || GUIDE_FILES.includes(name)) await add(name);
  }
  requireThat(selected.has('docs/onboarding/index.html') && selected.has('docs/beginners/index.html'),
    'Build the complete core Explorer guides');
  for (let index = 0; index < queue.length; index++) {
    const name = queue[index]; if (!name.endsWith('.html')) continue;
    const original = await fs.readFile(selected.get(name).source, 'utf8');
    let changed = false;
    const chunks = []; let previous = 0;
    for (const match of original.matchAll(/\b(href|src)=(["'])([^"']+)\2/gu)) {
      const [, attribute, quote, raw] = match;
      const upstreamSource = `https://github.com/${pin.repository}/`;
      if (raw.startsWith(upstreamSource + 'blob/main/') || raw.startsWith(upstreamSource + 'tree/main/')) {
        const href = raw.replace(/\/(blob|tree)\/main\//u, `/$1/${pin.sourceCommit}/`);
        chunks.push(original.slice(previous, match.index), `${attribute}=${quote}${href}${quote}`);
        previous = match.index + match[0].length; changed = true;
        rewrites.push({ guide: name, attribute, original: raw, source: null, href });
        continue;
      }
      if (/^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/iu.test(raw)) continue;
      const url = new URL(raw.replaceAll('&amp;', '&'), 'https://site.invalid/' + name);
      let target = decodeURIComponent(url.pathname.slice(1));
      if (!target || target.endsWith('/')) target += 'index.html';
      const local = appRows.has(target) || selected.has(target)
        || ((GUIDE_ROOTS.some(prefix => target.startsWith(prefix)) || GUIDE_REFERENCES.some(prefix => target.startsWith(prefix))
          || GUIDE_FILES.includes(target)) && materials.has(target));
      if (local) { if (!appRows.has(target)) await add(target); continue; }
      requireThat(attribute === 'href', `Supporting embedded asset needs an explicit local publication rule: ${name} -> ${target}`);
      const source = await sourceHref(checkout, target, url.hash, pin);
      const href = source.href;
      if (!source.candidate) missing.push({ guide: name, target, reason: 'No authored path for the generated-only resource; link to the pinned source tree.' });
      const replacement = href.replaceAll('&', '&amp;');
      chunks.push(original.slice(previous, match.index), `${attribute}=${quote}${replacement}${quote}`);
      previous = match.index + match[0].length; changed = true;
      rewrites.push({ guide: name, attribute, original: raw, source: source.candidate, href });
    }
    if (changed) {
      chunks.push(original.slice(previous));
      const provenanceHref = path.posix.relative(path.posix.dirname(name), 'GUIDE-PROVENANCE.json');
      const note = `<aside role="note"><p>Additional source references open online. <a href="${provenanceHref}">View reference details</a>.</p></aside>`;
      const derived = Buffer.from(chunks.join('').replace(/(<main\b[^>]*>)/u, '$1' + note));
      selected.set(name, { ...selected.get(name), derived, originalSha256: selected.get(name).sha256,
        bytes: derived.length, sha256: digest(derived) });
    }
  }
  const provenance = jsonBytes({ schema: 'gis-ai-go.explorer-guide-derivatives.v1',
    explorerSourceCommit: pin.sourceCommit, originalSiteTreeSha256: assembly.tree_sha256,
    policy: 'Core generated guides and bounded schema/reference closure remain local. Out-of-scope links point to immutable authored source; the canonical app is unchanged.',
    files: sorted(selected.keys()).map(name => ({ path: name, sourceSha256: selected.get(name).originalSha256 || selected.get(name).sha256,
      sha256: selected.get(name).sha256 })), rewrites, missing });
  selected.set('GUIDE-PROVENANCE.json', { path: 'GUIDE-PROVENANCE.json', bytes: provenance.length, sha256: digest(provenance), derived: provenance });
  return selected;
}

async function copyBoundFile(source, destination, expected) {
  await fs.mkdir(path.dirname(destination), { recursive: true });
  const before = await regular(source);
  const input = await fs.open(source, constants.O_RDONLY | (constants.O_NOFOLLOW || 0));
  const output = await fs.open(destination, constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL, 0o644);
  const hash = crypto.createHash('sha256'); let bytes = 0;
  try {
    const opened = await input.stat();
    requireThat(opened.ino === before.ino && opened.dev === before.dev, 'Input changed before copying');
    for await (const chunk of input.createReadStream({ autoClose: false })) {
      let offset = 0;
      while (offset < chunk.length) {
        const written = await output.write(chunk, offset, chunk.length - offset);
        requireThat(written.bytesWritten > 0, 'The output filesystem stopped accepting data');
        offset += written.bytesWritten;
      }
      bytes += chunk.length; hash.update(chunk);
    }
    requireThat(bytes === expected.bytes && hash.digest('hex') === expected.sha256, `Input changed while copying: ${expected.path}`);
  } finally { await input.close(); await output.close(); }
}

function gitHead(directory) { return execFileSync('git', ['-C', directory, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim(); }

export async function assemble(options, pin) {
  requireThat(pin.schema === 'gis-ai-go.explorer-publication.v1' && pin.repository === 'chris-page-gov/okf-explorer'
    && COMMIT.test(pin.sourceCommit) && SHA.test(pin.appTreeSha256) && SHA.test(pin.appManifestSha256)
    && pin.canonicalUrl === 'https://chris-page-gov.github.io/gis-ai-go/' && pin.basePath === '/gis-ai-go/'
    && pin.contextPublicationBase === pin.canonicalUrl + 'gis/explorer/context/', 'Invalid reviewed Explorer publication pin');
  requireThat(COMMIT.test(options.sourceCommit) && gitHead(ROOT) === options.sourceCommit, 'GIS source commit must equal this checkout HEAD');
  requireThat(gitHead(options.explorerCheckout) === pin.sourceCommit, 'Explorer checkout does not match its reviewed immutable source pin');
  requireThat((await fs.readFile(path.join(ROOT, 'VERSION'), 'utf8')).trim() === options.version, 'Publication version must equal VERSION');
  const output = path.resolve(options.output);
  try { await fs.lstat(output); throw new Error('Retain existing candidates; choose a new output directory'); }
  catch (error) { if (error.code !== 'ENOENT') throw error; }
  const appRoot = path.join(options.explorerCheckout, 'apps/okf-explorer/build');
  const siteRoot = path.join(options.explorerCheckout, '_site');
  const projectionRoot = path.join(options.projectionRoot, 'explorer');
  for (const input of [appRoot, siteRoot, projectionRoot, options.legacyDist]) {
    requireThat(output !== path.resolve(input) && !output.startsWith(path.resolve(input) + path.sep), 'Output must not be inside an input tree');
  }
  const { rows: appRows } = await validateApp(appRoot, pin);
  const projection = await validateProjection(projectionRoot, options.sourceCommit, pin);
  const legacyRows = await validateLegacy(options.legacyDist, options.sourceCommit, options.version);
  const guideRows = await guides(options.explorerCheckout, siteRoot, appRows, pin);
  const sources = new Map();
  function addRows(rows, root, prefix) { for (const [name, row] of rows) sources.set(prefix + name, { ...row, path: prefix + name, source: path.join(root, name) }); }
  addRows(appRows, appRoot, 'explorer/');
  for (const [name, row] of guideRows) sources.set('explorer/' + name, { ...row, path: 'explorer/' + name });
  addRows(projection.rows, projectionRoot, 'gis/explorer/');
  addRows(legacyRows, options.legacyDist, 'legacy/');
  for (const [name, row] of legacyRows) if (name.startsWith('catalogue/')) sources.set(name, { ...row, source: path.join(options.legacyDist, name) });
  for (const [name, body] of [['index.html', INDEX], ['router.js', ROUTER], ['style.css', STYLE]]) {
    const derived = Buffer.from(body); sources.set(name, { path: name, bytes: derived.length, sha256: digest(derived), derived });
  }
  for (const [name, source] of [['GIS-LICENCE', path.join(ROOT, 'LICENSE')],
    ['EXPLORER-LICENSE-CODE.md', path.join(options.explorerCheckout, 'LICENSE-CODE.md')],
    ['EXPLORER-LICENSE.md', path.join(options.explorerCheckout, 'LICENSE.md')]]) sources.set(name, { ...await inspectFile(source, name), source });
  requireThat(sources.size + 1 <= MAX_FILES, 'Distribution exceeds its 49,994-file limit before publication metadata');
  const files = sorted(sources.keys()).map(name => { const row = sources.get(name); return { path: name, bytes: row.bytes, sha256: row.sha256 }; });
  const manifest = { schema: 'gis-ai-go.explorer-distribution.v1', repository: 'chris-page-gov/gis-ai-go',
    sourceCommit: options.sourceCommit, version: options.version, basePath: pin.basePath, canonicalUrl: pin.canonicalUrl,
    app: { sourceCommit: pin.sourceCommit, treeSha256: pin.appTreeSha256, manifestSha256: pin.appManifestSha256,
      path: 'explorer/okf-explorer-build-manifest.json' },
    okf: { sourceRevision: options.sourceCommit, inputDigest: projection.report.inputDigest, snapshot: projection.report.snapshot,
      descriptorPath: 'gis/explorer/okf-explorer.json', contextManifestPath: 'gis/explorer/context/manifest.json' }, files };
  const manifestBytes = canonicalJsonBytes(manifest);
  requireThat(files.reduce((sum, row) => sum + row.bytes, manifestBytes.length) <= MAX_TOTAL_BYTES, 'Publication exceeds its served-byte budget');
  await fs.mkdir(path.dirname(output), { recursive: true });
  const staging = await fs.mkdtemp(path.join(path.dirname(output), '.explorer-pages-'));
  try {
    for (const row of files) {
      const entry = sources.get(row.path); const destination = path.join(staging, row.path);
      if (entry.derived) { await fs.mkdir(path.dirname(destination), { recursive: true }); await fs.writeFile(destination, entry.derived, { flag: 'wx', mode: 0o644 }); }
      else await copyBoundFile(entry.source, destination, row);
    }
    await fs.writeFile(path.join(staging, MANIFEST), manifestBytes, { flag: 'wx', mode: 0o644 });
    // Reserve the final name only after all input bytes have been verified and
    // copied. mkdir is exclusive, so a candidate created during the long copy
    // is retained rather than replaced by POSIX rename's empty-dir behaviour.
    await fs.mkdir(output, { mode: 0o700 });
    try { await fs.rename(staging, output); }
    catch (error) { await fs.rmdir(output).catch(() => {}); throw error; }
  } catch (error) { await fs.rm(staging, { recursive: true, force: true }); throw error; }
  return { output, files: files.length + 1, bytes: files.reduce((sum, row) => sum + row.bytes, manifestBytes.length), appTreeSha256: pin.appTreeSha256, snapshot: projection.report.snapshot };
}

function argumentsFor(argv) {
  const names = new Map([['--explorer-checkout', 'explorerCheckout'], ['--projection-root', 'projectionRoot'],
    ['--legacy-dist', 'legacyDist'], ['--output', 'output'], ['--source-commit', 'sourceCommit'], ['--version', 'version']]);
  const options = {};
  for (let i = 0; i < argv.length; i += 2) {
    const key = names.get(argv[i]); requireThat(key && argv[i + 1] && !options[key], 'Invalid or duplicate assembler argument');
    options[key] = key === 'sourceCommit' || key === 'version' ? argv[i + 1] : path.resolve(argv[i + 1]);
  }
  requireThat(Object.keys(options).length === names.size, 'Usage: node scripts/build_explorer_pages.mjs --explorer-checkout PATH --projection-root PATH --legacy-dist PATH --output NEWPATH --source-commit SHA --version VERSION');
  return options;
}

if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  try { console.log(JSON.stringify(await assemble(argumentsFor(process.argv.slice(2)), await readJson(PIN_PATH)))); }
  catch (error) { console.error(error.message); process.exitCode = 1; }
}
