// Optional local compatibility experiment. No installs, providers or deployments.
// Uses an existing trusted tooling installation read-only, never its Site code.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { writeFileSync } from "node:fs";
import { mkdir, mkdtemp, readFile, realpath, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { tmpdir } from "node:os";
import { dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const FIXTURE = join(ROOT, "scripts/web216_worker_mcp_fixture.ts");
const VERSIONS = { miniflare: "5.20260911.1-alpha", workerd: "1.20260911.1", esbuild: "0.28.1" };
const PROTOCOL = "2026-07-28";
const TOOLS = ["web216_cpih_select", "web216_cpih_query", "web216_cpih_inspect"];
const KEY = ["gis-ai-go", "ik", "v1", "a".repeat(64)].join(":");
const args = process.argv.slice(2);
if (args.length !== 2 || args[0] !== "--tooling-root" || !args[1]) {
  throw Error("node scripts/web216_worker_mcp_probe.mjs --tooling-root <existing-installation-root>");
}
const toolingRoot = await realpath(resolve(args[1]));
const temporaryRoot = await realpath(tmpdir());
const inside = (root, path) => { const part = relative(root, path); return part === "" ||
  (!isAbsolute(part) && part !== ".." && !part.startsWith(`..${sep}`)); };
assert(!inside(ROOT, temporaryRoot) && !inside(toolingRoot, temporaryRoot), "Temporary output must be outside repository and tooling");
process.umask(0o077);
const directory = await mkdtemp(join(temporaryRoot, "gis-ai-go-web216-worker-mcp-"));
await mkdir(join(directory, "sources"), { mode: 0o700 });
const startedAt = new Date().toISOString();
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const save = async (name, value) => writeFile(join(directory, name),
  Buffer.isBuffer(value) || typeof value === "string" ? value : JSON.stringify(value, null, 2) + "\n",
  { mode: 0o600, flag: "wx" });
console.log(JSON.stringify({ directory, started_at: startedAt }));
const blobs = new Set();
async function preserveSource(path) {
  const bytes = await readFile(path); const hash = sha256(bytes);
  if (!blobs.has(hash)) { await save(`sources/${hash}`, bytes); blobs.add(hash); }
  return { path: relative(ROOT, path), bytes: bytes.length, sha256: hash, retained_as: `sources/${hash}` };
}
let phase = "preflight";
let outboundAttempts = 0;
let wireCount = 0;
let worker;
let client;
const runtimeErrors = [];
const wireRecords = [];
const overallEnd = Date.now() + 120_000;
const plan = { experiment: "local-workerd-mcp-d1-not-hosted", started_at: startedAt,
  tooling_root: toolingRoot, expected_versions: VERSIONS, sdk_version: "2.0.0", protocol: PROTOCOL,
  source_commit: execFileSync("git", ["rev-parse", "HEAD"], { cwd: ROOT, encoding: "utf8" }).trim(),
  source_state: "working-tree-inputs-not-attested", conditions: ["workerd"],
  provider_egress: false, telemetry: false, deployment: false,
  response_deadline_ms: 20_000, overall_deadline_ms: 120_000,
  response_byte_limit: 1_048_576, request_byte_limit: 16_384, maximum_wire_requests: 20,
  synthetic_software_revision: "a".repeat(40), synthetic_clock: "2026-09-14T18:00:00.000Z",
  limitation: "Local SDK/Workers compatibility and orderly D1 reopen only; no product ingress, identity, crash recovery, cloud durability or accepted-build attestation." };
// Workerd startup can raise an uncaught listener error outside its constructor's
// promise. Preserve it without suppressing Node's normal failing termination.
process.once("uncaughtExceptionMonitor", (error, origin) => {
  writeFileSync(join(directory, "uncaught-failure.json"), JSON.stringify({ outcome: "uncaught-runtime-failure",
    phase, origin, completed_at: new Date().toISOString(), error: { name: error.name, message: error.message,
      code: error.code, stack: error.stack }, plan, wire_requests: wireCount,
    outbound_attempts: outboundAttempts, runtime_errors: runtimeErrors }, null, 2) + "\n", { flag: "wx", mode: 0o600 });
});

async function bounded(operation) {
  const milliseconds = Math.min(plan.response_deadline_ms, overallEnd - Date.now());
  assert(milliseconds > 0, "Overall probe deadline exceeded");
  const controller = new AbortController(); let timer;
  try { return await Promise.race([operation(controller.signal), new Promise((_, reject) => {
    timer = setTimeout(() => { controller.abort(); reject(Error("Local probe deadline exceeded")); }, milliseconds);
  })]); } finally { clearTimeout(timer); }
}
async function requestWorker(input, init) {
  assert(++wireCount <= plan.maximum_wire_requests, "Probe request limit exceeded");
  const request = new Request(input, init);
  const url = new URL(request.url);
  assert.equal(url.origin, "http://localhost"); assert.equal(url.search, "");
  assert(["/mcp", "/provision", "/state"].includes(url.pathname));
  for (const header of ["authorization", "cookie", "proxy-authorization"]) assert.equal(request.headers.has(header), false);
  const id = String(wireCount).padStart(2, "0");
  const requestBytes = Buffer.from(await request.clone().arrayBuffer());
  assert(requestBytes.length <= plan.request_byte_limit, "Probe request body exceeds bound");
  await save(`${id}-request.body`, requestBytes);
  const record = { sequence: wireCount, phase, started_at: new Date().toISOString(), method: request.method,
    url: request.url, request_headers: Object.fromEntries(request.headers), request_body_bytes: requestBytes.length,
    request_body_sha256: sha256(requestBytes), response_status: null, response_complete: false };
  const chunks = []; let bytes = 0; let response;
  try {
    await bounded(async (signal) => {
      const dispatch = await worker.getWorker("web216-mcp-probe");
      response = await dispatch.fetch(new Request(request, { signal }));
      record.response_status = response.status; record.response_headers = Object.fromEntries(response.headers);
      const reader = response.body?.getReader();
      if (reader) while (true) {
        const item = await reader.read(); if (item.done) break;
        bytes += item.value.byteLength;
        if (bytes > plan.response_byte_limit) { void reader.cancel().catch(() => {}); throw Error("Probe response exceeds bound"); }
        chunks.push(Buffer.from(item.value));
      }
      record.response_complete = true;
    });
  } catch (error) { record.error = { name: error?.name ?? "unknown", message: String(error?.message ?? error) }; }
  const body = Buffer.concat(chunks);
  Object.assign(record, { completed_at: new Date().toISOString(), response_body_bytes: body.length, response_body_sha256: sha256(body) });
  await save(`${id}-response.body`, body); await save(`${id}-wire.json`, record); wireRecords.push(record);
  assert.equal(record.error, undefined, "See preserved wire failure");
  return new Response(body.length === 0 ? null : body, { status: response.status, headers: response.headers });
}
async function json(path, method = "GET") {
  const response = await requestWorker(`http://localhost/${path}`, { method });
  assert.equal(response.status, 200, "See preserved non-200 fixture response"); return response.json();
}
function result(response, error = false) {
  assert.equal(response.isError === true, error);
  assert.equal(response.content.length, 1); assert.equal(response.content[0].type, "text");
  assert.deepEqual(JSON.parse(response.content[0].text), response.structuredContent);
  assert(!JSON.stringify(response).includes(KEY), "Raw key must not be reflected by a tool result");
  return response.structuredContent;
}
try {
  plan.sources = await Promise.all([fileURLToPath(import.meta.url), FIXTURE, join(ROOT, "pnpm-lock.yaml"),
    join(ROOT, "tests/fixtures/web216/current-cpih-projection.json")].map(preserveSource));
  const require = createRequire(join(toolingRoot, "package.json"));
  const entries = {};
  for (const [name, version] of Object.entries(VERSIONS)) {
    const packageRoot = await realpath(join(toolingRoot, "node_modules", name));
    const manifest = JSON.parse(await readFile(join(packageRoot, "package.json"), "utf8"));
    assert.equal(manifest.version, version, `Pre-existing ${name} version mismatch; no installation attempted`);
    entries[name] = await realpath(require.resolve(name)); assert(inside(packageRoot, entries[name]));
    plan.sources.push(await preserveSource(join(packageRoot, "package.json")));
  }
  const sdkRequire = createRequire(join(ROOT, "apps/mcp-gateway/package.json"));
  for (const name of ["server", "client"]) {
    const manifestPath = join(ROOT, `apps/mcp-gateway/node_modules/@modelcontextprotocol/${name}/package.json`);
    assert.equal(JSON.parse(await readFile(manifestPath, "utf8")).version, "2.0.0");
    plan.sources.push(await preserveSource(manifestPath));
  }
  const { Client, StreamableHTTPClientTransport } = await import(pathToFileURL(sdkRequire.resolve("@modelcontextprotocol/client")).href);
  const { build } = await import(pathToFileURL(entries.esbuild).href);
  const { Miniflare, convertV4MiniflareOptions, NoOpLog } = await import(pathToFileURL(entries.miniflare).href);
  phase = "bundle";
  const compiled = await build({ absWorkingDir: ROOT, entryPoints: [FIXTURE], bundle: true, write: false,
    format: "esm", platform: "neutral", target: "es2023", conditions: plan.conditions,
    nodePaths: [join(ROOT, "apps/mcp-gateway/node_modules")], external: ["node:*"], metafile: true });
  const script = compiled.outputFiles[0].text;
  await save("worker.mjs", script); await save("bundle-metafile.json", compiled.metafile);
  plan.bundle_sha256 = sha256(script); plan.bundle_bytes = Buffer.byteLength(script);
  plan.compiled_inputs = [];
  for (const path of Object.keys(compiled.metafile.inputs).sort()) {
    const actual = await realpath(resolve(ROOT, path));
    assert(inside(ROOT, actual), "Worker bundle input must be inside the implementation worktree");
    plan.compiled_inputs.push(await preserveSource(actual));
  }
  const inputs = Object.keys(compiled.metafile.inputs);
  assert(inputs.some((path) => path.endsWith("/shimsWorkerd.mjs")), "SDK must resolve its actual Workers shim");
  assert(!inputs.some((path) => /\/shims(?:Node|Browser)\.mjs$/u.test(path)), "Unexpected SDK shim");
  plan.graph_concerns = { mcp_server_source_in_graph: inputs.includes("apps/mcp-gateway/src/mcp-server.ts"),
    emitted_node_imports: [...new Set(Object.values(compiled.metafile.outputs).flatMap((output) => output.imports.map((entry) => entry.path)))].sort(),
    note: "Metafile includes parsed/tree-shaken inputs; emitted bytes and runtime success do not establish that all source modules are Workers-portable." };
  const options = () => ({ ...convertV4MiniflareOptions({ name: "web216-mcp-probe", modules: true, script,
    host: "127.0.0.1", cf: false, compatibilityDate: "2026-09-14", compatibilityFlags: ["nodejs_compat"],
    d1Databases: { DB: "web216-mcp-public-fixture" }, resourcePersistencePath: join(directory, "database"),
    log: new NoOpLog(), outboundService: () => { outboundAttempts += 1; return new Response("Outbound egress refused", { status: 503 }); },
  }), telemetry: { enabled: false }, handleUncaughtError: (error) => runtimeErrors.push(String(error)) });
  await save("attempt-plan.json", plan);
  const connect = async () => {
    client = new Client({ name: "web216-local-worker-probe", version: "1.0.0" }, {
      capabilities: {}, versionNegotiation: { mode: { pin: PROTOCOL } },
    });
    await bounded(() => client.connect(new StreamableHTTPClientTransport(new URL("http://localhost/mcp"), { fetch: requestWorker })));
    assert.equal(client.getProtocolEra(), "modern"); assert.equal(client.getNegotiatedProtocolVersion(), PROTOCOL);
  };
  phase = "explicit-test-provisioning"; worker = new Miniflare(options());
  assert.equal((await json("provision", "POST")).record_count, 0);
  phase = "sdk-discover-list"; await connect();
  const listed = await bounded(() => client.listTools());
  assert.deepEqual(listed.tools.map((tool) => tool.name).sort(), [...TOOLS].sort());
  for (const tool of listed.tools) {
    assert.equal(tool.annotations.readOnlyHint, tool.name !== "web216_cpih_query");
    assert.equal(tool.annotations.openWorldHint, false); assert.equal(tool.annotations.destructiveHint, false);
    assert.equal(tool.inputSchema.additionalProperties, tool.name === "web216_cpih_inspect" ? undefined : false);
    assert(tool.outputSchema);
  }
  phase = "select-query-inspect-replay";
  const selection = result(await bounded(() => client.callTool({ name: TOOLS[0], arguments: { period: "2026-07" } })));
  assert.equal(selection.authority.grants_execution, false);
  const query = { period: "2026-07", selection_plan_id: selection.plan_id, idempotency_key: KEY };
  const first = result(await bounded(() => client.callTool({ name: TOOLS[1], arguments: query })));
  assert.equal(first.schema, "gis-ai-go.web216-hosted-cpih-result.v1");
  assert.equal(first.result.observation.value, "142.7");
  assert.equal(first.evidence.storage_observation.read_freshness, "not-established-by-application");
  assert.deepEqual(result(await bounded(() => client.callTool({ name: TOOLS[2], arguments: { receipt_id: first.evidence.receipt.receipt_id } }))), first);
  assert.deepEqual(result(await bounded(() => client.callTool({ name: TOOLS[1], arguments: query }))), first);
  phase = "invalid-input";
  const rejected = result(await bounded(() => client.callTool({ name: TOOLS[1], arguments: { ...query, policy: "allow" } })), true);
  assert.equal(rejected.code, "invalid-input");
  const before = await json("state"); assert.equal(before.record_count, 1); assert.equal(before.event_count, 1);
  await save("first-result.json", first);
  await bounded(() => client.close()); client = undefined;
  await bounded(() => worker.dispose()); worker = undefined;
  phase = "restart-inspect"; worker = new Miniflare(options()); await connect();
  const reopened = result(await bounded(() => client.callTool({ name: TOOLS[2], arguments: { receipt_id: first.evidence.receipt.receipt_id } })));
  assert.deepEqual(reopened, first);
  const after = await json("state"); assert.deepEqual(after, before);
  await save("reopened-result.json", reopened);
  assert(wireRecords.some((record) => record.request_headers["mcp-method"] === "server/discover"));
  assert.equal(outboundAttempts, 0); assert.deepEqual(runtimeErrors, []);
  await bounded(() => client.close()); client = undefined;
  await bounded(() => worker.dispose()); worker = undefined;
  const outcome = { outcome: "local-workers-mcp-d1-restart-pass", started_at: startedAt, completed_at: new Date().toISOString(),
    tool_names: TOOLS, protocol: PROTOCOL, observation_value: "142.7", record_count: 1,
    receipt_id: first.evidence.receipt.receipt_id, restart_exact_match: true, snapshot_sha256: sha256(after.canonical),
    wire_requests: wireCount, outbound_attempts: outboundAttempts, runtime_errors: runtimeErrors,
    bundle_sha256: plan.bundle_sha256, plan_sha256: sha256(await readFile(join(directory, "attempt-plan.json"))),
    product_ingress_tested: false, hosted_deployment: false, crash_recovery_established: false, attested: false };
  await save("outcome.json", outcome); console.log(JSON.stringify({ directory, ...outcome }));
} catch (error) {
  await save("failure.json", { outcome: "failed-or-unavailable", phase, completed_at: new Date().toISOString(),
    error: { name: error?.name ?? "unknown", message: String(error?.message ?? error), stack: error?.stack },
    plan, wire_requests: wireCount, outbound_attempts: outboundAttempts, runtime_errors: runtimeErrors });
  console.error(JSON.stringify({ directory, phase, outcome: "failed-or-unavailable", message: String(error?.message ?? error) }));
  process.exitCode = 1;
} finally {
  if (client !== undefined) await bounded(() => client.close()).catch(() => {});
  if (worker !== undefined) await worker.dispose().catch(() => {});
}
