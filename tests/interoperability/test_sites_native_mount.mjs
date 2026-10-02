// Exercises the assembly wrapper with the compiled, real MCP handler and store.
// Identity is synthetic; these checks prove no hosted OAuth or client acceptance.
import assert from 'node:assert/strict';
import { after, before, test } from 'node:test';
import { createHash } from 'node:crypto';
import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const origin = 'https://synthetic-test.chatgpt.site';
const revision = 'a'.repeat(40);
const token = 'synthetic-application-test-token-'.repeat(3);
const tokenHash = createHash('sha256').update(token).digest('hex');
const changedSyntheticCredential = 'synthetic-changed-configuration';
const expectedTools = ['sites_capabilities', 'sites_evidence_inspect', 'sites_ons_areas',
  'sites_ons_cpih', 'sites_os_names', 'sites_os_open_product'];
let directory, wrapper;

before(async () => {
  directory = await mkdtemp(join(tmpdir(), 'sites-native-mount-'));
  await mkdir(join(directory, 'vendor/sites-pilot'), { recursive: true });
  await writeFile(join(directory, 'runtime.mjs'),
    await readFile(join(root, 'sites/private-pilot/server/sites-pilot-runtime.mjs')));
  const runtime = pathToFileURL(join(root, 'apps/mcp-gateway/dist/src/sites-pilot-http.js')).href;
  const store = pathToFileURL(join(root, 'apps/mcp-gateway/dist/src/sites-pilot-store.js')).href;
  await writeFile(join(directory, 'vendor/sites-pilot/sites-pilot-runtime.mjs'),
    `export { createSitesPilotCapacity, createSitesPilotHttpHandler } from ${JSON.stringify(runtime)};\n` +
    `export { createSitesPilotStore } from ${JSON.stringify(store)};\n`);
  await writeFile(join(directory, 'vendor/sites-pilot/bundle-manifest.json'), JSON.stringify({
    schema: 'gis-ai-go.sites-pilot-package.v1', source_revision: revision,
  }));
  wrapper = await import(pathToFileURL(join(directory, 'runtime.mjs')).href);
});
after(async () => { if (directory) await rm(directory, { recursive: true, force: true }); });

function setup(extra = {}) {
  let statements = 0;
  const environment = { DB: { prepare() { statements++; throw new Error('Unexpected database access'); } },
    SITES_PILOT_ORIGIN: origin, SITES_PILOT_SOURCE_REVISION: revision, ...extra };
  const pending = [];
  return { environment, statements: () => statements,
    waitUntil: (completion) => { pending.push(completion); },
    settled: async () => { await Promise.all(pending); } };
}
function request(path, { method = 'tools/list', parameters, identity = 'synthetic-owner', tokenValue,
  httpMethod = 'POST', suppliedOrigin = origin } = {}) {
  return new Request(`${origin}${path}`, { method: httpMethod, headers: {
    'content-type': 'application/json', accept: 'application/json, text/event-stream',
    'mcp-protocol-version': '2025-11-25', origin: suppliedOrigin,
    ...(identity === null ? {} : { 'oai-authenticated-user-id': identity }),
    ...(tokenValue === undefined ? {} : { 'x-sites-pilot-test-token': tokenValue }),
  }, ...(httpMethod === 'GET' ? {} : { body: JSON.stringify({ jsonrpc: '2.0', id: 1, method,
    ...(parameters === undefined ? {} : { params: parameters }) }) }) });
}
async function dispatch(route, req, state) {
  const response = await wrapper[route](req, state.environment, state.waitUntil);
  const body = await response.json();
  await state.settled();
  return { status: response.status, body };
}

test('both exact mounts expose the same six tools with no provider or database operation', async () => {
  const state = setup();
  for (const [route, path] of [['dispatchSitesPilot', '/pilot/mcp'], ['dispatchSitesNativeMcp', '/mcp']]) {
    const initial = await dispatch(route, request(path, { method: 'initialize', parameters: {
      protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'synthetic-test', version: '1' },
    } }), state);
    assert.equal(initial.status, 200); assert.equal(initial.body.result.protocolVersion, '2025-11-25');
    const list = await dispatch(route, request(path), state);
    assert.equal(list.status, 200);
    assert.deepEqual(list.body.result.tools.map(tool => tool.name).sort(), expectedTools);
    const capabilities = await dispatch(route, request(path, { method: 'tools/call', parameters: {
      name: 'sites_capabilities', arguments: {},
    } }), state);
    assert.equal(capabilities.status, 200);
    assert.equal(capabilities.body.result.structuredContent.evidence.provider_egress, false);
    assert.equal(capabilities.body.result.structuredContent.evidence.software_revision, revision);
  }
  assert.equal(state.statements(), 0);
});

test('the native mount rejects the application test token while the historical mount preserves it', async () => {
  const state = setup({ SITES_PILOT_TEST_TOKEN_SHA256: tokenHash });
  const input = { identity: null, tokenValue: token };
  assert.equal((await dispatch('dispatchSitesPilot', request('/pilot/mcp', input), state)).status, 200);
  assert.equal((await dispatch('dispatchSitesNativeMcp', request('/mcp', input), state)).status, 401);
  assert.equal(state.statements(), 0);
});

test('both mounts reject missing identity, hostile origins and non-POST calls', async () => {
  const state = setup();
  for (const [route, path] of [['dispatchSitesPilot', '/pilot/mcp'], ['dispatchSitesNativeMcp', '/mcp']]) {
    assert.equal((await dispatch(route, request(path, { identity: null }), state)).status, 401);
    assert.equal((await dispatch(route, request(path, { suppliedOrigin: 'https://untrusted.invalid' }), state)).status, 403);
    assert.equal((await dispatch(route, request(path, { httpMethod: 'GET' }), state)).status, 405);
  }
  assert.equal(state.statements(), 0);
});

test('mounts do not rewrite paths or admit query strings', async () => {
  const state = setup();
  for (const [route, paths] of [
    ['dispatchSitesPilot', ['/mcp', '/pilot/mcp?query=value', '/pilot/mcp/']],
    ['dispatchSitesNativeMcp', ['/pilot/mcp', '/mcp?query=value', '/mcp/']],
  ]) for (const path of paths) assert.equal((await dispatch(route, request(path), state)).status, 404);
  assert.equal(state.statements(), 0);
});

test('binding changes fail closed across mounts sharing the same database', async () => {
  const state = setup();
  assert.equal((await dispatch('dispatchSitesPilot', request('/pilot/mcp'), state)).status, 200);
  state.environment.OS_NAMES_API_KEY = changedSyntheticCredential;
  assert.equal((await dispatch('dispatchSitesNativeMcp', request('/mcp'), state)).status, 503);
  assert.equal(state.statements(), 0);
});

test('source mismatch and a stopped origin disable both mounts without database access', async () => {
  for (const extra of [{ SITES_PILOT_SOURCE_REVISION: 'b'.repeat(40) }, { SITES_PILOT_ORIGIN: undefined }]) {
    const state = setup(extra);
    for (const [route, path] of [['dispatchSitesPilot', '/pilot/mcp'], ['dispatchSitesNativeMcp', '/mcp']]) {
      assert.equal((await dispatch(route, request(path), state)).status, 503);
    }
    assert.equal(state.statements(), 0);
  }
});

test('the wrapper shares a two-request ceiling across both exact mounts', { timeout: 2000 }, async () => {
  const state = setup();
  const controllers = [new AbortController(), new AbortController()];
  const routes = ['dispatchSitesPilot', 'dispatchSitesNativeMcp'];
  const paths = ['/pilot/mcp', '/mcp'];
  const pending = paths.map((path, index) => wrapper[routes[index]](new Request(`${origin}${path}`, {
    method: 'POST', headers: request(path).headers, signal: controllers[index].signal,
    body: new ReadableStream({ start(stream) { stream.enqueue(new TextEncoder().encode('{')); } }),
    duplex: 'half',
  }), state.environment, state.waitUntil));
  try {
    for (let index = 0; index < paths.length; index++) {
      const blocked = await wrapper[routes[index]](request(paths[index]), state.environment, state.waitUntil);
      assert.equal(blocked.status, 429);
    }
  } finally {
    for (const controller of controllers) controller.abort();
    assert((await Promise.all(pending)).every(response => response.status === 408));
    await state.settled();
  }
  for (let index = 0; index < paths.length; index++) {
    assert.equal((await dispatch(routes[index], request(paths[index]), state)).status, 200);
  }
  assert.equal(state.statements(), 0);
});
