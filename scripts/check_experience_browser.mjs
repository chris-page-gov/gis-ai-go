import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { createRequire } from 'node:module';
import { mkdir, readFile, writeFile, realpath } from 'node:fs/promises';
import { resolve, relative, sep } from 'node:path';
import { pathToFileURL } from 'node:url';
import { deflateRawSync } from 'node:zlib';

// Real offline browser journeys. The modelContext seam is an explicit mock;
// nothing in this harness claims a real AI/Voice connection or user study.
const root = resolve(import.meta.dirname, '..');
const options = new Map(process.argv.slice(2).map(value => {
  const match = /^--(input|output|channel)=(.+)$/u.exec(value);
  assert(match, 'Use --input=path, --output=path or --channel=chrome|chromium');
  return [match[1], match[2]];
}));
const input = resolve(root, options.get('input') ?? 'artifacts/experience/learn-by-trying.html');
const output = resolve(root, options.get('output') ?? 'output/playwright/experience');
const channel = options.get('channel') ?? 'chrome';
assert(['chrome', 'chromium'].includes(channel), 'Use installed Chrome or Chromium; this script never installs a browser');
assert(input.startsWith(root + sep) && output.startsWith(root + sep), 'Input and reports must stay in the repository');
const require = createRequire(resolve(root, 'apps/public-data-workbench/package.json'));
const { chromium } = require('@playwright/test');
const { default: AxeBuilder } = require('@axe-core/playwright');
const source = await readFile(input);
assert((await realpath(input)).startsWith(root + sep), 'Input symlink must stay in the repository');
await mkdir(output, { recursive: true });
const report = {
  schema: 'gis-ai-go.experience-browser-observation.v1', startedAt: new Date().toISOString(),
  input: relative(root, input), sha256: createHash('sha256').update(source).digest('hex'),
  browser: { channel, version: null }, status: 'running',
  scope: 'Built offline page, synthetic fixtures, explicit modelContext mock; no real Voice, provider, client or participant acceptance.',
  networkPolicy: 'All page HTTP(S) requests are recorded and aborted. No live provider calls are permitted.',
  tests: [], screenshots: [], networkRequests: [], pageErrors: [], axe: [],
};
function safeError(error) {
  return (error instanceof Error ? error.message : String(error))
    .replaceAll(root, '<repository>')
    .replace(/(?:file:\/\/)?\/(?:Users|home|Volumes|private\/tmp|var\/folders)\/[^\s"'<>]+/gu, '<local-path>')
    .replace(/\u001b\[[0-9;]*m/gu, '')
    .slice(0, 6_000);
}
const serialise = () => JSON.stringify(report, (_key, value) => typeof value === 'string' ? safeError(value) : value, 2) + '\n';
const save = async () => writeFile(resolve(output, 'checkpoint.json'), serialise());
let browser;
let context;
let page;
const deadline = setTimeout(() => {
  report.status = 'deadline-exceeded';
  void save().finally(async () => { await browser?.close().catch(() => undefined); process.exitCode = 1; });
}, 150_000);
deadline.unref();

function crc32(bytes) {
  let value = 0xffffffff;
  for (const byte of bytes) { value ^= byte; for (let bit = 0; bit < 8; bit++) value = value & 1 ? 0xedb88320 ^ value >>> 1 : value >>> 1; }
  return (value ^ 0xffffffff) >>> 0;
}
function syntheticZip() {
  const locals = [], central = []; let offset = 0;
  for (const name of ['maps/places.shp', 'maps/places.shx', 'maps/places.dbf', 'maps/places.prj']) {
    const filename = Buffer.from(name), raw = Buffer.from('Synthetic companion bytes; not validated map features.');
    const compressed = deflateRawSync(raw), checksum = crc32(raw), local = Buffer.alloc(30), entry = Buffer.alloc(46);
    local.writeUInt32LE(0x04034b50); local.writeUInt16LE(20, 4); local.writeUInt16LE(0x800, 6); local.writeUInt16LE(8, 8);
    local.writeUInt32LE(checksum, 14); local.writeUInt32LE(compressed.length, 18); local.writeUInt32LE(raw.length, 22); local.writeUInt16LE(filename.length, 26);
    entry.writeUInt32LE(0x02014b50); entry.writeUInt16LE(20, 4); entry.writeUInt16LE(20, 6); entry.writeUInt16LE(0x800, 8); entry.writeUInt16LE(8, 10);
    entry.writeUInt32LE(checksum, 16); entry.writeUInt32LE(compressed.length, 20); entry.writeUInt32LE(raw.length, 24); entry.writeUInt16LE(filename.length, 28); entry.writeUInt32LE(offset, 42);
    const part = Buffer.concat([local, filename, compressed]); locals.push(part); central.push(Buffer.concat([entry, filename])); offset += part.length;
  }
  const directory = Buffer.concat(central), end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50); end.writeUInt16LE(4, 8); end.writeUInt16LE(4, 10); end.writeUInt32LE(directory.length, 12); end.writeUInt32LE(offset, 16);
  return Buffer.concat([...locals, directory, end]);
}
async function shot(name) {
  const path = resolve(output, `${name}.png`);
  await page.screenshot({ path, fullPage: false }); report.screenshots.push(relative(root, path));
}
async function check(id, action) {
  const started = performance.now();
  try { const evidence = await action(); report.tests.push({ id, status: 'passed', durationMs: Math.round(performance.now() - started), ...(evidence === undefined ? {} : { evidence }) }); }
  catch (error) {
    report.tests.push({ id, status: 'failed', durationMs: Math.round(performance.now() - started), error: safeError(error) });
    await shot(`failure-${id}`).catch(() => undefined);
  }
  await save();
}
const text = selector => page.locator(selector).innerText();
async function tool(name, input) {
  return page.evaluate(async ({ name, input }) => {
    const definition = window.__experienceMockTools.get(name);
    if (!definition) throw new Error(`Unregistered mock tool: ${name}`);
    return definition.execute(input);
  }, { name, input });
}
async function file(name, contents, mimeType = 'text/plain') {
  await page.locator('#intake-files').setInputFiles({ name, mimeType, buffer: Buffer.from(contents) });
  await page.waitForFunction(() => !document.querySelector('#intake-status').textContent.includes('Checking small files'));
}
async function delayedFolderDrop() {
  await page.evaluate(() => {
    let resolveFile;
    window.__lateFolderResult = new Promise(resolve => { resolveFile = resolve; });
    const entry = { name: 'late-private.csv', isFile: true, isDirectory: false, file(success) { window.__releaseLateFolder = () => { success(new File(['label,count\nSTALE_FOLDER_MARKER,9'], 'late-private.csv')); resolveFile(); }; } };
    const directory = { name: 'delayed-folder', isDirectory: true, isFile: false, createReader() { let first = true; return { readEntries(success) { success(first ? (first = false, [entry]) : []); } }; } };
    const event = new Event('drop', { bubbles: true, cancelable: true });
    Object.defineProperty(event, 'dataTransfer', { value: { files: [], items: [{ kind: 'file', webkitGetAsEntry() { return directory; } }] } });
    document.querySelector('#drop-zone').dispatchEvent(event);
  });
  await page.waitForFunction(() => typeof window.__releaseLateFolder === 'function');
}

try {
  await save();
  browser = await chromium.launch({ headless: true, ...(channel === 'chrome' ? { channel } : {}), timeout: 15_000 });
  report.browser.version = browser.version();
  context = await browser.newContext({ viewport: { width: 1280, height: 900 }, locale: 'en-GB', timezoneId: 'Europe/London', acceptDownloads: true });
  await context.route(/^https?:\/\//u, async route => {
    // Retain only origin; test output must not accidentally persist query credentials.
    report.networkRequests.push({ method: route.request().method(), origin: new URL(route.request().url()).origin });
    await route.abort('blockedbyclient');
  });
  await context.addInitScript(() => {
    window.__experienceMockTools = new Map();
    Object.defineProperty(document, 'modelContext', { configurable: true, value: {
      registerTool(definition, options) {
        window.__experienceMockTools.set(definition.name, definition);
        options.signal.addEventListener('abort', () => window.__experienceMockTools.delete(definition.name), { once: true });
      },
    } });
  });
  page = await context.newPage(); page.setDefaultTimeout(5_000); page.setDefaultNavigationTimeout(10_000);
  page.on('pageerror', error => report.pageErrors.push(safeError(error)));
  await page.goto(pathToFileURL(input).href, { waitUntil: 'load' });

  await check('offline-load-and-explicit-mock', async () => {
    await page.getByRole('heading', { name: 'What would you like to find out?' }).waitFor();
    await page.waitForFunction(() => window.__experienceMockTools.size === 4);
    const state = await tool('experience_get_state', {});
    assert.equal(state.providerCalls, 0); assert(state.features.length > 10);
    assert.equal(new Set(await page.evaluate(() => [...window.__experienceMockTools.keys()])).size, 4);
    return { featureCount: state.features.length, mockToolCount: 4, realVoiceTested: false };
  });
  await check('persona-language-variants', async () => {
    await page.locator('#example-choice').selectOption('public-search');
    await page.locator('#example-persona').selectOption('additional-english'); const simpler = await text('#example-content');
    assert.match(simpler, /Need find public data about soil/u);
    await page.locator('#example-persona').selectOption('geospatial-specialist'); const specialist = await text('#example-content');
    assert.match(specialist, /frozen catalogue.*provenance/u); assert.notEqual(simpler, specialist);
    await page.locator('#example-persona').selectOption('teen-explorer');
    return { personas: ['additional-english', 'geospatial-specialist', 'teen-explorer'], outcome: 'Visible question wording changes; authored examples are not scored as user success.' };
  });
  await check('feature-table-evidence-and-jit-preserve-view', async () => {
    await tool('experience_show_example', { feature_id: 'pilot-names' });
    await tool('experience_set_view', { view: 'table' });
    assert(await page.locator('#example-content table').count());
    const before = await page.locator('#example-content').innerHTML();
    await tool('experience_explain', { concept_id: 'crs' });
    assert.equal(await page.locator('#example-content').innerHTML(), before);
    assert.match(await text('#concept-detail'), /coordinate|map|position/iu);
    assert.equal((await tool('experience_get_state', {})).view, 'table');
    await tool('experience_set_view', { view: 'evidence' });
    assert.match(await text('#example-content'), /Where the information comes from/u);
    assert(await page.locator('#example-content a[href^="https://"]').count());
    const invalid = await tool('experience_show_example', { feature_id: 'unrecognised' });
    assert.equal(invalid.isError, true); assert.equal((await tool('experience_get_state', {})).selectedFeature, 'pilot-names');
    await tool('experience_set_view', { view: 'cards' });
    return { displayedFeature: 'pilot-names', views: ['table', 'evidence', 'cards'], retainedWhileExplaining: true };
  });
  await check('synthetic-dataset-has-a-visible-name-and-source', async () => {
    await page.locator('#synthetic-example').click();
    const result = await text('#intake-results');
    assert.match(result, /Example park/u); assert.match(result, /Made-up teaching fixture/u); assert.match(result, /preview ready/u);
    assert.match(await text('#intake-status'), /No upload or download/u);
  });
  await check('csv-literal-rendering-and-file-state-exclusion', async () => {
    await file('private-synthetic.csv', 'label,value\nUNIQUE_LOCAL_FILE_MARKER,"<img src=x onerror=window.__intakeXss=1>"\nformula,=1+1', 'text/csv');
    assert.match(await text('#intake-results'), /<img src=x onerror=window.__intakeXss=1>/u);
    assert.equal(await page.locator('#intake-results img').count(), 0);
    assert.equal(await page.evaluate(() => window.__intakeXss), undefined);
    const state = JSON.stringify(await tool('experience_get_state', {}));
    assert(!state.includes('UNIQUE_LOCAL_FILE_MARKER')); assert(!state.includes('private-synthetic.csv'));
    const pending = page.waitForEvent('download'); await page.locator('#download-session').click();
    const download = await pending; const stream = await download.createReadStream(); assert(stream);
    const chunks = []; for await (const chunk of stream) chunks.push(chunk);
    const serialised = Buffer.concat(chunks).toString('utf8');
    assert(!serialised.includes('UNIQUE_LOCAL_FILE_MARKER')); assert(!serialised.includes('private-synthetic.csv'));
    const checklist = JSON.parse(serialised); assert.equal(checklist.containsUploadedFiles, false);
    assert(checklist.questions.every(question => question.observedOutcome === 'not-recorded'));
    return { uploadContentInPageState: false, uploadContentInChecklist: false, scriptsExecuted: false };
  });
  await check('invalid-geojson-is-explained-without-repair', async () => {
    await file('wrong-grid.geojson', '{"type":"Point","coordinates":[430000,280000]}', 'application/geo+json');
    assert.match(await text('#intake-results'), /coordinate system|longitude\/latitude/iu);
    assert.doesNotMatch(await text('#intake-results'), /preview ready/u);
  });
  await check('selected-shapefile-companions-group-automatically', async () => {
    await page.locator('#intake-files').setInputFiles(['shp', 'shx', 'dbf', 'prj'].map(ext => ({ name: `places.${ext}`, mimeType: 'application/octet-stream', buffer: Buffer.from('Synthetic descriptor bytes only') })));
    await page.waitForFunction(() => document.querySelector('#intake-results').textContent.includes('matching Shapefile'));
    const result = await text('#intake-results'); assert.match(result, /4 matching Shapefile/u); assert.doesNotMatch(result, /Add the matching/u);
    assert.match(result, /unopened|No map features have been imported/u);
  });
  await check('zip-inventory-finds-real-member-names', async () => {
    await page.locator('#intake-files').setInputFiles({ name: 'synthetic-maps.zip', mimeType: 'application/zip', buffer: syntheticZip() });
    await page.waitForFunction(() => document.querySelector('#intake-results').textContent.includes('ZIP entries inspected'));
    const result = await text('#intake-results'); assert.match(result, /4 ZIP entries/u); assert.match(result, /synthetic-maps\.zip: places\.shp/u);
    assert.match(result, /4 matching Shapefile/u); assert.doesNotMatch(result, /Add the matching/u);
    assert.match(result, /No file was extracted/u);
    return { archiveMembers: 4, automaticallyGrouped: true, extractionClaimed: false };
  });
  await check('url-companion-plan-performs-no-fetch', async () => {
    const requests = report.networkRequests.length;
    await page.locator('#intake-url').fill('https://example.org/maps/places.shp'); await page.locator('#url-form button').click();
    assert.match(await text('#intake-results'), /places\.shx/u); assert.match(await text('#intake-results'), /not verified files/u);
    assert.equal(report.networkRequests.length, requests);
  });
  await check('clear-removes-preview-and-inputs', async () => {
    await page.locator('#clear-intake').click(); assert.equal(await text('#intake-results'), '');
    for (const id of ['intake-files', 'intake-folder', 'intake-url']) assert.equal(await page.locator(`#${id}`).inputValue(), '');
    assert.match(await text('#intake-status'), /cleared/u);
  });
  for (const replacement of ['synthetic', 'url', 'new-file']) {
    await check(`late-folder-drop-does-not-overwrite-${replacement}`, async () => {
      await delayedFolderDrop();
      if (replacement === 'synthetic') await page.locator('#synthetic-example').click();
      else if (replacement === 'url') { await page.locator('#intake-url').fill('https://example.org/new.geojson'); await page.locator('#url-form button').click(); }
      else await file('new-selection.csv', 'label,value\nCURRENT_FILE_MARKER,2', 'text/csv');
      const before = await text('#intake-results');
      await page.evaluate(async () => { window.__releaseLateFolder(); await window.__lateFolderResult; await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))); });
      assert.equal(await text('#intake-results'), before); assert(!before.includes('STALE_FOLDER_MARKER'));
      return { oldCallbackReleased: true, currentSelectionPreserved: true };
    });
  }
  await page.locator('#clear-intake').click();
  for (const width of [320, 390, 1280]) for (const fontPercent of [100, 200]) {
    await check(`layout-${width}-${fontPercent}`, async () => {
      await page.setViewportSize({ width, height: 900 });
      await page.evaluate(font => { document.documentElement.style.fontSize = `${font}%`; window.scrollTo(0, 0); }, fontPercent);
      await page.locator('#example-choice').selectOption('public-search');
      const initial = await page.evaluate(() => {
        const learning = document.querySelector('.learning'), rect = learning.getBoundingClientRect();
        return { width: document.documentElement.clientWidth, scrollWidth: document.documentElement.scrollWidth,
          learning: { top: rect.top, bottom: rect.bottom, left: rect.left, right: rect.right, position: getComputedStyle(learning).position } };
      });
      assert(initial.scrollWidth <= initial.width + 1, `Horizontal document overflow: ${JSON.stringify(initial)}`);
      assert(initial.learning.top >= 0 && initial.learning.bottom <= 901 && initial.learning.left >= 0 && initial.learning.right <= width + 1, `Learning panel is off screen: ${JSON.stringify(initial.learning)}`);
      await page.locator('#example-search').focus();
      const focused = [];
      for (let step = 0; step < 18; step++) {
        await page.keyboard.press('Tab');
        const observation = await page.evaluate(() => {
          const element = document.activeElement;
          if (!(element instanceof HTMLElement) || element === document.body) return null;
          const rect = element.getBoundingClientRect(), x = Math.max(0, Math.min(innerWidth - 1, rect.left + rect.width / 2)), y = Math.max(0, Math.min(innerHeight - 1, rect.top + rect.height / 2));
          const covering = document.elementFromPoint(x, y);
          return { id: element.id || element.textContent.slice(0, 55), top: rect.top, bottom: rect.bottom, left: rect.left, right: rect.right,
            visible: rect.bottom > 0 && rect.top < innerHeight && rect.right > 0 && rect.left < innerWidth,
            covered: covering !== element && !element.contains(covering), covering: covering?.closest('.learning') ? 'learning-panel' : covering?.tagName,
            outline: getComputedStyle(element).outlineStyle };
        });
        if (!observation) continue; focused.push(observation);
        assert(observation.visible && !observation.covered, `Keyboard focus is hidden: ${JSON.stringify(observation)}`);
        assert.notEqual(observation.outline, 'none', `No visible keyboard focus indicator: ${observation.id}`);
      }
      await page.locator('#example-search').focus(); await shot(`layout-${width}-${fontPercent}`);
      const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']).analyze();
      const violations = results.violations.map(value => ({ id: value.id, impact: value.impact, description: value.description, targets: value.nodes.map(node => node.target) }));
      report.axe.push({ width, fontPercent, violations, incompleteRules: results.incomplete.map(value => value.id) });
      assert.equal(violations.filter(value => ['serious', 'critical'].includes(value.impact)).length, 0, `Serious/critical axe findings: ${JSON.stringify(violations)}`);
      return { width, fontPercent, learningPanelVisible: true, documentOverflows: false, keyboardStopsChecked: focused.length, axeViolations: violations.length };
    });
  }
  await check('offline-and-console-boundary', async () => {
    assert.equal(createHash('sha256').update(await readFile(input)).digest('hex'), report.sha256,
      'The offline bundle changed during browser evaluation; rebuild once and rerun against stable bytes.');
    assert.equal(report.networkRequests.length, 0, `Unexpected attempted HTTP(S) requests: ${JSON.stringify(report.networkRequests)}`);
    assert.deepEqual(report.pageErrors, []);
    return { attemptedHttpRequests: 0, pageErrors: 0 };
  });
  report.status = report.tests.every(test => test.status === 'passed') ? 'passed' : 'failed';
} catch (error) {
  report.status = 'blocked'; report.error = safeError(error);
} finally {
  clearTimeout(deadline);
  await context?.close().catch(() => undefined); await browser?.close().catch(() => undefined);
  report.completedAt = new Date().toISOString();
  await save(); await writeFile(resolve(output, 'report.json'), serialise());
  console.log(JSON.stringify({ status: report.status, passed: report.tests.filter(test => test.status === 'passed').length, failed: report.tests.filter(test => test.status === 'failed').length,
    report: relative(root, resolve(output, 'report.json')), error: report.error ?? null }));
  if (report.status !== 'passed') process.exitCode = 1;
}
