// Local compatibility probe of the actual built Site. Installs nothing and never deploys.
// Identity is synthetic; every provider response is mocked; D1 is temporary local storage.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdtemp, readFile, readdir, realpath, rm } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
assert(args.length === 6 && args[0] === '--tooling-root' && args[2] === '--site-root' && args[4] === '--bundle-manifest',
  'Use --tooling-root <pinned tooling> --site-root <built Site> --bundle-manifest <package manifest>');
const tooling = await realpath(resolve(args[1]));
const site = await realpath(resolve(args[3]));
const manifestPath = await realpath(resolve(args[5]));
const versions = { miniflare: '5.20260911.1-alpha', workerd: '1.20260911.1' };
const toolingRequire = createRequire(join(tooling, 'package.json'));
for (const [name, version] of Object.entries(versions)) {
  assert.equal(JSON.parse(await readFile(join(tooling, 'node_modules', name, 'package.json'), 'utf8')).version, version,
    `Use the pinned ${name}; this probe installs nothing`);
}
const { Miniflare, convertV4MiniflareOptions, NoOpLog } = await import(pathToFileURL(toolingRequire.resolve('miniflare')).href);
const sdkRequire = createRequire(join(root, 'apps/mcp-gateway/package.json'));
const { Client, StreamableHTTPClientTransport } = await import(pathToFileURL(sdkRequire.resolve('@modelcontextprotocol/client')).href);
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const canonical = (value) => value !== null && typeof value === 'object'
  ? Array.isArray(value) ? `[${value.map(canonical).join(',')}]`
    : `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`
  : JSON.stringify(value);
const valueHash = (value) => hash(canonical(value));
const manifestBytes = await readFile(manifestPath);
const manifest = JSON.parse(manifestBytes);
assert.equal(manifest.schema, 'gis-ai-go.sites-pilot-package.v1');
assert.match(manifest.source_revision, /^[0-9a-f]{40}$/u);
assert.equal(manifest.bundle.path, 'sites-pilot-runtime.mjs');
assert.match(manifest.bundle.sha256, /^[0-9a-f]{64}$/u);
const installedManifest = await readFile(join(site, 'server/vendor/sites-pilot/bundle-manifest.json'));
assert.equal(hash(installedManifest), hash(manifestBytes), 'Installed package must have the supplied manifest');
const installedBundle = await readFile(join(site, 'server/vendor/sites-pilot/sites-pilot-runtime.mjs'));
assert.equal(hash(installedBundle), manifest.bundle.sha256);
assert.equal(installedBundle.byteLength, manifest.bundle.bytes);

// Reuse the existing authored, fixed authority without embedding any account/host identity here.
// This URL only labels local ingress; outboundService below never forwards network traffic.
const admissionSource = await readFile(join(site, 'server/web216-admission.mjs'), 'utf8');
const originMatch = admissionSource.match(/^export const WEB216_ORIGIN = '(https:\/\/[^']+)';$/mu);
assert(originMatch, 'Existing Site must declare one fixed HTTPS authority');
const origin = originMatch[1];
assert.equal(new URL(origin).origin, origin);
const syntheticKey = 'synthetic-local-os-key-not-a-credential';
const syntheticOperator = 'a'.repeat(64);
const protocol = '2025-11-25';
const tools = ['sites_capabilities', 'sites_evidence_inspect', 'sites_ons_areas', 'sites_ons_cpih', 'sites_os_names', 'sites_os_open_product'];
const fixture = JSON.parse(await readFile(join(root, 'tests/fixtures/web216/current-cpih-projection.json'), 'utf8'));
const msoaUrl = 'https://services1.arcgis.com/ESMARspQHYMw9BZ9/ArcGIS/rest/services/MSOA_DEC_2021_EW_NC_v3/FeatureServer/0/query';
const msoaQuery = new URL(msoaUrl);
for (const [name, value] of Object.entries({ f: 'json', where: "MSOA21NM LIKE 'Warwick%'", outFields: 'MSOA21CD,MSOA21NM',
  returnGeometry: 'false', resultRecordCount: '5', orderByFields: 'MSOA21CD' })) msoaQuery.searchParams.set(name, value);
const mocks = new Map([
  ['https://api.os.uk/search/names/v1/find?query=Warwick&maxresults=5&format=JSON', { provider: 'os-names', body: {
    header: { query: 'Warwick', format: 'json', maxresults: 5, offset: 0, totalresults: 1 }, results: [{ GAZETTEER_ENTRY: {
      ID: 'osgb4000000074555874', NAMES_URI: 'http://data.ordnancesurvey.co.uk/id/4000000074555874', NAME1: 'Warwick',
      TYPE: 'populatedPlace', LOCAL_TYPE: 'Town', GEOMETRY_X: 428119, GEOMETRY_Y: 265114, COUNTRY: 'England',
    } }],
  } }],
  ['https://api.os.uk/downloads/v1/products/OpenNames', { provider: 'os-open-data', body: {
    id: 'OpenNames', name: 'OS Open Names', version: '2026-07', areas: ['GB'], formats: [{ format: 'CSV' }],
    url: 'https://api.os.uk/downloads/v1/products/OpenNames', downloadsUrl: 'https://api.os.uk/downloads/v1/products/OpenNames/downloads',
  } }],
  [msoaQuery.href, { provider: 'ons-geography', body: {
    fields: [{ name: 'MSOA21CD', type: 'esriFieldTypeString' }, { name: 'MSOA21NM', type: 'esriFieldTypeString' }],
    exceededTransferLimit: true, features: [{ attributes: { MSOA21CD: 'E02006519', MSOA21NM: 'Warwick 001' } }],
  } }],
  ['https://api.beta.ons.gov.uk/v1/search?content_type=timeseries&cdids=L522', { provider: 'ons-cpih', body: fixture.search }],
  ['https://api.beta.ons.gov.uk/v1/data?uri=%2Feconomy%2Finflationandpriceindices%2Ftimeseries%2Fl522%2Fmm23', { provider: 'ons-cpih', body: fixture.data }],
]);
process.umask(0o077);
const directory = await mkdtemp(join(tmpdir(), 'sites-pilot-built-worker-'));
const started = performance.now();
const finishBy = Date.now() + 120_000;
let phase = 'source-inventory', worker, legacyClient, modules, sequence = 0, rpcId = 0, outboundAttempts = 0, unexpectedOutbound = 0;
const observations = [], providerObservations = [], runtimeErrors = [], sources = [];
const problems = [];
let sourceBytes = 0;
async function bounded(operation) {
  const duration = Math.min(20_000, finishBy - Date.now()); assert(duration > 0, 'Probe duration bound');
  const controller = new AbortController(); let timer;
  try { return await Promise.race([operation(controller.signal), new Promise((_, reject) => {
    timer = setTimeout(() => { controller.abort(); reject(new Error('Bounded local probe deadline')); }, duration);
  })]); } finally { clearTimeout(timer); }
}
async function inventory(path) {
  for (const entry of (await readdir(join(site, path), { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name))) {
    const next = `${path}/${entry.name}`;
    if (entry.isDirectory()) await inventory(next);
    else {
      assert(entry.isFile(), 'Built materials must not contain symlinks');
      const bytes = await readFile(join(site, next)); sourceBytes += bytes.length;
      assert(sourceBytes <= 67_108_864 && sources.length < 2000, 'Built material bound');
      sources.push({ path: next, bytes: bytes.length, sha256: hash(bytes) });
    }
  }
}
const options = (revision = manifest.source_revision) => ({ ...convertV4MiniflareOptions({
  name: 'sites-pilot-built-probe', modules, modulesRoot: join(site, 'dist/server'),
  assets: { directory: join(site, 'dist/client'), binding: 'ASSETS', routerConfig: { has_user_worker: true } },
  host: '127.0.0.1', upstream: origin, cf: false,
  compatibilityDate: '2026-09-11', compatibilityFlags: ['nodejs_compat'],
  bindings: { SITES_PILOT_ORIGIN: origin, SITES_PILOT_SOURCE_REVISION: revision,
    OS_NAMES_API_KEY: syntheticKey, WEB216_OPERATOR_TOKEN: syntheticOperator },
  d1Databases: { DB: 'sites-pilot-built-local-test' }, resourcePersistencePath: join(directory, 'database'),
  log: new NoOpLog(),
  outboundService(request) {
    outboundAttempts++;
    const mock = mocks.get(request.url);
    if (!mock || outboundAttempts > 5 || request.method !== 'GET' ||
        request.headers.get('key') !== (mock.provider === 'os-names' ? syntheticKey : null)) {
      unexpectedOutbound++; return new Response('Unexpected mock request refused', { status: 503 });
    }
    const body = JSON.stringify(mock.body);
    providerObservations.push({ provider: mock.provider, response_bytes: Buffer.byteLength(body), response_sha256: hash(body) });
    return new Response(body, { status: 200, headers: { 'content-type': 'application/json' } });
  },
}), telemetry: { enabled: false }, handleUncaughtError: (error) => runtimeErrors.push(hash(String(error))) });
async function wire(input, init = {}, identity = true) {
  assert(++sequence <= 50, 'Inbound request bound');
  const request = new Request(input, init); assert.equal(new URL(request.url).origin, origin);
  const headers = new Headers(request.headers); headers.set('host', new URL(origin).host);
  if (identity) headers.set('oai-authenticated-user-id', 'synthetic-local-user');
  const body = request.body === null ? undefined : new Uint8Array(await request.arrayBuffer());
  assert((body?.byteLength ?? 0) <= 16_384);
  const start = performance.now();
  return bounded(async (signal) => {
    const response = await worker.dispatchFetch(request.url, { method: request.method, headers: Object.fromEntries(headers), body, signal, redirect: 'manual' });
    const reader = response.body?.getReader(); const chunks = []; let length = 0;
    try {
      if (reader) for (;;) {
        const item = await reader.read(); if (item.done) break;
        length += item.value.byteLength; assert(length <= 1_048_576, 'Inbound response bound'); chunks.push(Buffer.from(item.value));
      }
    } finally { await reader?.cancel().catch(() => {}); }
    const bytes = Buffer.concat(chunks);
    assert(!bytes.includes(Buffer.from(syntheticKey)) && !bytes.includes(Buffer.from(syntheticOperator)), 'Synthetic credential must not escape');
    observations.push({ sequence, phase, status: response.status, elapsed_ms: Number((performance.now() - start).toFixed(3)),
      request_bytes: body?.byteLength ?? 0, request_sha256: hash(body ?? new Uint8Array()), response_bytes: length, response_sha256: hash(bytes) });
    return new Response(bytes.length ? bytes : null, { status: response.status, headers: response.headers });
  });
}
function rpcRequest(method, params, id = ++rpcId) {
  return { method: 'POST', headers: { 'content-type': 'application/json', accept: 'application/json, text/event-stream',
    origin, 'mcp-protocol-version': protocol }, body: JSON.stringify({ jsonrpc: '2.0', ...(id === null ? {} : { id }), method, ...(params === undefined ? {} : { params }) }) };
}
async function rpc(method, params, id = ++rpcId, path = '/pilot/mcp') {
  assert(['/pilot/mcp', '/mcp'].includes(path));
  const response = await wire(`${origin}${path}`, rpcRequest(method, params, id));
  if (id === null) { assert.equal(response.status, 202); return; }
  assert.equal(response.status, 200); assert.match(response.headers.get('content-type') ?? '', /^application\/json/iu);
  const message = await response.json(); assert.equal(message.jsonrpc, '2.0'); assert.equal(message.id, id); assert.equal(message.error, undefined);
  return message.result;
}
async function callTool(name, parameters, expectedError, path = '/pilot/mcp') {
  const result = await rpc('tools/call', { name, arguments: parameters }, undefined, path);
  assert.equal(result.content.length, 1); assert.equal(result.content[0].type, 'text');
  assert.deepEqual(JSON.parse(result.content[0].text), result.structuredContent);
  if (result.isError === true) problems.push({ tool: tools.includes(name) ? name : 'unknown',
    code: typeof result.structuredContent?.code === 'string' && /^[a-z][a-z-]{1,40}$/u.test(result.structuredContent.code)
      ? result.structuredContent.code : 'unrecognised' });
  if (expectedError) { assert.equal(result.isError, true); assert.equal(result.structuredContent.code, expectedError); }
  else assert.notEqual(result.isError, true);
  return result.structuredContent;
}
async function staticPage(path, phrase) {
  let url = `${origin}${path}`;
  for (let attempt = 0; attempt < 3; attempt++) {
    const response = await wire(url);
    if (![301, 302, 307, 308].includes(response.status)) {
      assert.equal(response.status, 200); assert.match(response.headers.get('content-type') ?? '', /^text\/html/iu);
      const bytes = Buffer.from(await response.arrayBuffer()); if (phrase) assert(bytes.includes(Buffer.from(phrase)));
      return hash(bytes);
    }
    assert(response.headers.has('location')); url = new URL(response.headers.get('location'), url).href;
    assert.equal(new URL(url).origin, origin, 'Static redirect must remain inside local authority');
  }
  throw new Error('Static redirect bound');
}
async function migrate(database, text) {
  const statements = text.split('--> statement-breakpoint').map(statement => statement.trim()).filter(Boolean);
  assert(statements.length > 0 && statements.length <= 4);
  for (const statement of statements) await bounded(() => database.prepare(statement).run());
}
const quotaRows = (database) => bounded(async () => (await database.prepare('SELECT * FROM sites_pilot_allowance_v1 ORDER BY provider').all()).results);
const receiptCount = (database) => bounded(() => database.prepare('SELECT COUNT(*) AS count FROM sites_pilot_receipts_v1').first());
const legacyRow = (database) => bounded(() => database.prepare('SELECT * FROM web216_cpih_snapshot WHERE singleton = 1').first());
function verifyResult(result, tool, parameters) {
  assert.equal(result.schema, 'gis-ai-go.sites-pilot-result.v1'); assert.equal(result.tool, tool);
  assert.equal(result.evidence.software_revision, manifest.source_revision);
  assert.equal(result.evidence.parameters_sha256, valueHash(parameters)); assert.equal(result.evidence.data_sha256, valueHash(result.data));
  assert.equal(result.evidence.persistence, 'd1-append-only-application-contract'); assert.equal(result.evidence.attestation, 'not-attested');
  assert.equal(result.evidence.rollback_protection, 'requires-independent-checkpoint'); assert.equal(result.evidence.provider_egress, true);
  const { receipt_id, ...core } = result.evidence;
  assert.equal(receipt_id, `sites-pilot:sha256:${valueHash({ tool, ...core })}`);
  assert.equal(result.data.source_mode, 'live-provider-response');
  // The production adapter labels its transport path. This probe establishes only mock-backed execution.
  for (const request of result.data.requests) assert(providerObservations.some(mock => mock.response_sha256 === request.body_sha256));
}
try {
  await inventory('dist/server'); await inventory('dist/client');
  const moduleSources = sources.filter(source => source.path.startsWith('dist/server/') && /\.m?js$/u.test(source.path));
  assert(moduleSources.some(source => source.path === 'dist/server/index.js'));
  moduleSources.sort((a, b) => a.path === 'dist/server/index.js' ? -1 : b.path === 'dist/server/index.js' ? 1 : a.path.localeCompare(b.path));
  modules = await Promise.all(moduleSources.map(async source => {
    const contents = await readFile(join(site, source.path), 'utf8'); assert.equal(hash(contents), source.sha256);
    return { type: 'ESModule', path: join(site, source.path), contents };
  }));
  assert(modules.some(module => module.contents.includes(manifest.source_revision)), 'Built Worker must contain the source binding');
  const oldMigration = await readFile(join(site, 'drizzle/0000_brief_jamie_braddock.sql'), 'utf8');
  const pilotMigration = await readFile(join(site, 'drizzle/0001_sites_pilot.sql'), 'utf8');
  assert.equal(hash(pilotMigration), hash(await readFile(join(root, 'sites/private-pilot/drizzle/0001_sites_pilot.sql'))));
  phase = 'initial-migrations'; worker = new Miniflare(options());
  let database = await bounded(() => worker.getD1Database('DB', 'sites-pilot-built-probe'));
  await migrate(database, oldMigration); await migrate(database, pilotMigration);
  const initialQuotas = await quotaRows(database);
  assert.deepEqual(initialQuotas.map(row => [row.provider, row.enabled, row.used, row.maximum]),
    ['ons-cpih', 'ons-geography', 'os-names', 'os-open-data'].map(provider => [provider, 1, 0, 120]));
  phase = 'legacy-initialisation';
  const operator = await wire(`${origin}/workbench/operator`, { method: 'POST', headers: { 'content-type': 'application/json',
    'x-web216-operator': syntheticOperator }, body: '{"operation":"initialise"}' });
  assert.equal(operator.status, 200); const legacyBefore = await legacyRow(database); assert(legacyBefore);
  legacyClient = new Client({ name: 'sites-pilot-local-legacy-probe', version: '1.0.0' },
    { capabilities: {}, versionNegotiation: { mode: { pin: '2026-07-28' } } });
  await bounded(() => legacyClient.connect(new StreamableHTTPClientTransport(new URL(`${origin}/workbench/mcp`), { fetch: wire })));
  assert.deepEqual((await bounded(() => legacyClient.listTools())).tools.map(tool => tool.name).sort(),
    ['web216_cpih_inspect', 'web216_cpih_query', 'web216_cpih_select']);
  await bounded(() => legacyClient.close()); legacyClient = undefined;
  phase = 'static-routes';
  const staticBefore = { demo: await staticPage('/demo.html'), workbench: await staticPage('/workbench/index.html') };
  await staticPage('/pilot', 'Ask a bounded question of live public data');
  phase = 'identity-origin-denials';
  for (const path of ['/pilot/mcp', '/mcp']) {
    assert.equal((await wire(`${origin}${path}`, rpcRequest('tools/list'), false)).status, 401);
    const wrongOrigin = rpcRequest('tools/list'); wrongOrigin.headers.origin = 'https://untrusted.invalid';
    assert.equal((await wire(`${origin}${path}`, wrongOrigin)).status, 403);
  }
  assert.equal(outboundAttempts, 0); assert.deepEqual(await receiptCount(database), { count: 0 });
  phase = 'native-mount-discovery';
  assert.equal((await rpc('initialize', { protocolVersion: protocol, capabilities: {},
    clientInfo: { name: 'synthetic-local-native-client', version: '1.0.0' } }, undefined, '/mcp')).protocolVersion, protocol);
  await rpc('notifications/initialized', undefined, null, '/mcp');
  assert.deepEqual((await rpc('tools/list', undefined, undefined, '/mcp')).tools.map(tool => tool.name).sort(), tools);
  const nativeCapabilities = await callTool('sites_capabilities', {}, undefined, '/mcp');
  assert.equal(nativeCapabilities.evidence.software_revision, manifest.source_revision);
  assert.equal(nativeCapabilities.evidence.provider_egress, false);
  assert.equal(outboundAttempts, 0); assert.deepEqual(await quotaRows(database), initialQuotas);
  phase = 'six-tool-journey';
  assert.equal((await rpc('initialize', { protocolVersion: protocol, capabilities: {}, clientInfo: { name: 'synthetic-local-client', version: '1.0.0' } })).protocolVersion, protocol);
  await rpc('notifications/initialized', undefined, null);
  assert.deepEqual((await rpc('tools/list')).tools.map(tool => tool.name).sort(), tools);
  const capabilities = await callTool('sites_capabilities', {});
  assert.equal(capabilities.evidence.software_revision, manifest.source_revision); assert.equal(capabilities.evidence.provider_egress, false);
  assert.equal(capabilities.data.providers.psga, 'disabled-rights-not-established');
  const queries = [
    ['sites_os_names', { query: 'Warwick', max_results: 5 }],
    ['sites_os_open_product', { product: 'OpenNames' }],
    ['sites_ons_areas', { name_prefix: 'Warwick', max_results: 5 }],
    ['sites_ons_cpih', { periods: ['2026-01', '2026-07'] }],
  ];
  const receipts = [];
  for (const [tool, parameters] of queries) { const result = await callTool(tool, parameters); verifyResult(result, tool, parameters); receipts.push(result); }
  assert.equal(receipts[0].data.data.crs_basis, 'fixed-os-open-names-source-contract');
  assert.equal(receipts[0].data.data.candidates[0].ID, 'osgb4000000074555874');
  assert.equal(receipts[1].data.data.version, '2026-07');
  assert.equal(receipts[2].data.data.complete, false); assert.equal(receipts[2].data.data.areas[0].MSOA21CD, 'E02006519');
  assert.equal(receipts[3].data.data.comparison.difference_index_points, '3.3');
  assert.equal(receipts[3].data.data.comparison.relative_change_percent, '2.367288');
  assert.deepEqual(await callTool('sites_evidence_inspect', { receipt_id: receipts[0].evidence.receipt_id }), receipts[0]);
  assert.deepEqual(await callTool('sites_evidence_inspect', { receipt_id: receipts[0].evidence.receipt_id }, undefined, '/mcp'), receipts[0]);
  assert.equal(outboundAttempts, 5); assert.equal(unexpectedOutbound, 0); assert.deepEqual(await receiptCount(database), { count: 4 });
  assert.deepEqual((await quotaRows(database)).map(row => [row.provider, row.used]),
    [['ons-cpih', 2], ['ons-geography', 1], ['os-names', 1], ['os-open-data', 1]]);
  phase = 'migration-replay-preserves-allowance';
  await bounded(() => database.prepare("UPDATE sites_pilot_allowance_v1 SET enabled = 0, used = 7 WHERE provider = 'os-names'").run());
  const stoppedQuotas = await quotaRows(database); await migrate(database, pilotMigration);
  assert.deepEqual(await quotaRows(database), stoppedQuotas);
  await callTool('sites_os_names', queries[0][1], 'admission-denied');
  await callTool('sites_os_names', queries[0][1], 'admission-denied', '/mcp');
  assert.equal(outboundAttempts, 5); assert.deepEqual(await receiptCount(database), { count: 4 });
  assert.deepEqual(await legacyRow(database), legacyBefore);
  phase = 'restart-persistence';
  await bounded(() => worker.dispose()); worker = undefined; worker = new Miniflare(options());
  database = await bounded(() => worker.getD1Database('DB', 'sites-pilot-built-probe'));
  for (const receipt of receipts) assert.deepEqual(await callTool('sites_evidence_inspect', { receipt_id: receipt.evidence.receipt_id }), receipt);
  for (const receipt of receipts) assert.deepEqual(await callTool('sites_evidence_inspect', { receipt_id: receipt.evidence.receipt_id }, undefined, '/mcp'), receipt);
  assert.deepEqual(await quotaRows(database), stoppedQuotas); assert.deepEqual(await legacyRow(database), legacyBefore);
  assert.deepEqual({ demo: await staticPage('/demo.html'), workbench: await staticPage('/workbench/index.html') }, staticBefore);
  phase = 'source-revision-mismatch';
  await bounded(() => worker.dispose()); worker = undefined;
  worker = new Miniflare(options(manifest.source_revision === '0'.repeat(40) ? '1'.repeat(40) : '0'.repeat(40)));
  assert.equal((await wire(`${origin}/pilot/mcp`, rpcRequest('tools/list'))).status, 503);
  assert.equal((await wire(`${origin}/mcp`, rpcRequest('tools/list'))).status, 503);
  assert.equal(outboundAttempts, 5); assert.equal(unexpectedOutbound, 0); assert.deepEqual(runtimeErrors, []);
  // Ensure neither executing the Worker nor serving assets modified the recorded build.
  for (const source of sources) assert.equal(hash(await readFile(join(site, source.path))), source.sha256);
  console.log(JSON.stringify({ schema: 'gis-ai-go.sites-pilot-built-worker-probe.v1', outcome: 'pass',
    boundary: { identity: 'synthetic-header-not-hosted-authentication', providers: 'fixed-mock-responses-no-live-network',
      storage: 'temporary-local-d1-dispose-recreate', hosted_backup: false, cloud_durability: false, deployed: false, independent_attestation: false },
    versions, source_revision: manifest.source_revision, package_manifest_sha256: hash(manifestBytes), bundle_sha256: manifest.bundle.sha256,
    built_material_count: sources.length, built_material_bytes: sourceBytes, built_inventory_sha256: valueHash(sources),
    mounted_paths: ['/pilot/mcp', '/mcp'], native_oauth_verified: false,
    migrations_sha256: { existing: hash(oldMigration), pilot: hash(pilotMigration) },
    requests: sequence, mocked_provider_requests: outboundAttempts, unexpected_outbound_requests: unexpectedOutbound, receipts: receipts.length,
    receipt_hashes: receipts.map(receipt => valueHash(receipt)), legacy_snapshot_sha256: valueHash(legacyBefore),
    allowance_rows_sha256: valueHash(stoppedQuotas), static_response_sha256: staticBefore,
    elapsed_ms: Number((performance.now() - started).toFixed(3)), observations, provider_observations: providerObservations }));
} catch (error) {
  console.error(JSON.stringify({ schema: 'gis-ai-go.sites-pilot-built-worker-probe.v1', outcome: 'fail', phase,
    error_name: error?.name ?? 'Error', error_sha256: hash(String(error)), requests: sequence,
    mocked_provider_requests: outboundAttempts, unexpected_outbound_requests: unexpectedOutbound,
    elapsed_ms: Number((performance.now() - started).toFixed(3)), problems, observations, runtime_error_hashes: runtimeErrors }));
  process.exitCode = 1;
} finally {
  if (legacyClient) await bounded(() => legacyClient.close()).catch(() => {});
  if (worker) await bounded(() => worker.dispose()).catch(() => {});
  await rm(directory, { recursive: true, force: true });
}
