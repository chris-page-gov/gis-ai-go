import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { request as httpRequest, type ClientRequest } from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test, { type TestContext } from "node:test";
import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";
import { openWeb216WorkbenchState } from "../src/web216-workbench-main.js";
import { createWeb216WorkbenchServer, WEB216_WORKBENCH_MAX_CONCURRENT, WEB216_WORKBENCH_PORT } from "../src/web216-workbench-server.js";
import { MCP_PROTOCOL_VERSION } from "../src/mcp-server.js";
const PROJECTION: unknown = JSON.parse(readFileSync(new URL("../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url), "utf8"));
const SOFTWARE = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) } as const;
const NOW = () => new Date("2026-09-14T18:00:00.000Z");
const KEY = ["gis-ai-go", "ik", "v1", "a".repeat(64)].join(":");
function setup(t: TestContext) {
  const root = mkdtempSync(join(tmpdir(), "web216-listener-"));
  const publicDirectory = join(root, "public"); mkdirSync(publicDirectory);
  mkdirSync(join(publicDirectory, "assets"));
  writeFileSync(join(publicDirectory, "index.html"), '<!doctype html><html lang="en-GB"><script type="module" src="/assets/index-abcdefgh.js"></script><body>Captured CPIH fixture</body></html>');
  writeFileSync(join(publicDirectory, "assets", "index-abcdefgh.js"), 'document.title = "Captured CPIH fixture";');
  const state = openWeb216WorkbenchState(root, PROJECTION, SOFTWARE, NOW);
  const server = createWeb216WorkbenchServer(state.application, publicDirectory);
  t.after(async () => { await server.closeWorkbench(); rmSync(root, { recursive: true, force: true }); });
  return { root, publicDirectory, state, server };
}
async function listen(s: ReturnType<typeof setup>) {
  await new Promise<void>((resolve, reject) => { s.server.once("error", reject); s.server.listen(WEB216_WORKBENCH_PORT, "127.0.0.1", resolve); });
  const address = s.server.address(); assert.ok(address !== null && typeof address === "object");
  return `http://127.0.0.1:${address.port}`;
}
async function raw(origin: string, path: string, headers: string[] | Record<string, string>, body?: string): Promise<{ status: number; body: string }> {
  return new Promise((resolve, reject) => {
    const request = httpRequest(`${origin}${path}`, { method: body === undefined ? "GET" : "POST", headers }, (response) => {
      let text = ""; response.setEncoding("utf8"); response.on("data", (data) => { text += data; });
      response.on("end", () => resolve({ status: response.statusCode!, body: text }));
    });
    request.on("error", reject); request.end(body);
  });
}

test("real loopback serves immutable allowlisted assets and an official-client CPIH journey with retained evidence", async (t) => {
  const s = setup(t); const origin = await listen(s);
  const page = await fetch(origin);
  assert.equal(page.status, 200); assert.match(await page.text(), /Captured CPIH fixture/u);
  assert.equal(page.headers.get("cache-control"), "no-store");
  assert.match(page.headers.get("content-security-policy")!, /connect-src 'self'/u);
  const head = await fetch(`${origin}/`, { method: "HEAD" }); assert.equal(await head.text(), "");
  writeFileSync(join(s.publicDirectory, "assets", "index-abcdefgh.js"), "changed after admission");
  const asset = await fetch(`${origin}/assets/index-abcdefgh.js`);
  assert.equal(asset.headers.get("content-type"), "text/javascript; charset=utf-8");
  assert.equal(await asset.text(), 'document.title = "Captured CPIH fixture";');
  const ready = await fetch(`${origin}/readyz`); assert.equal(ready.status, 200);
  const readiness = await ready.json() as any;
  assert.equal(readiness.provider_egress, false); assert.equal(readiness.static_content_sha256, s.server.assetSha256);
  const client = new Client({ name: "web216-local-test", version: "1.0.0" }, {
    capabilities: {}, versionNegotiation: { mode: { pin: MCP_PROTOCOL_VERSION } },
  });
  t.after(() => client.close());
  await client.connect(new StreamableHTTPClientTransport(new URL(`${origin}/mcp`)));
  const selection = (await client.callTool({ name: "web216_cpih_select", arguments: { period: "2026-07" } })).structuredContent as any;
  const query = (await client.callTool({ name: "web216_cpih_query", arguments: { period: "2026-07", selection_plan_id: selection.plan_id, idempotency_key: KEY } })).structuredContent as any;
  assert.equal(query.result.observation.value, "142.7"); assert.equal(query.evidence.storage.status, "persisted");
  assert.equal(JSON.stringify(query).includes(KEY), false);
  await client.close(); await s.server.closeWorkbench();
  const reopened = openWeb216WorkbenchState(s.root, PROJECTION, SOFTWARE, NOW);
  assert.deepEqual(reopened.application.inspect({ idempotency_key: KEY }), query);
  assert.equal(reopened.ledger.verify().event_count, 1);
});

test("exact Host/Origin, singleton headers, method, route and body admission reject before claims", async (t) => {
  const s = setup(t); const origin = await listen(s); const host = new URL(origin).host;
  for (const headers of [
    { host: "localhost" }, { host, origin: "https://example.org" }, { host, origin: "null" },
    ["Host", host, "Host", host],
  ]) assert.equal((await raw(origin, "/readyz", headers)).status, 403);
  for (const path of ["/index.html", "/assets/../identity.json", "/assets/%2e%2e/identity.json", "/assets/index-abcdefgh.js?x=1", "/mcp?x=1", "/.git/config"]) {
    assert.equal((await raw(origin, path, { host })).status, 404);
  }
  assert.equal((await raw(origin, "/mcp", { host, "content-length": "65537" }, "x")).status, 413);
  assert.equal((await raw(origin, "/mcp", { host, "transfer-encoding": "chunked" }, "{}")).status, 403);
  const get = await fetch(`${origin}/mcp`); assert.equal(get.status, 405);
  assert.equal(s.state.reconciliationIndex.verify().claim_count, 0);
});

test("corrupt storage blocks readiness but not liveness and never discloses the corrupt bytes", async (t) => {
  const s = setup(t); const origin = await listen(s);
  writeFileSync(join(s.root, "web216-public-data-workbench-v1", "ledger", "ledger.json"), "synthetic corrupted marker");
  const ready = await fetch(`${origin}/readyz`); assert.equal(ready.status, 503);
  const value = await ready.json() as any;
  assert.equal(value.status, "blocked"); assert.equal(value.new_claims_available, false);
  assert.equal(JSON.stringify(value).includes("synthetic corrupted marker"), false);
  const health = await fetch(`${origin}/healthz`); assert.equal(health.status, 200); await health.text();
});

test("eight incomplete bodies exhaust admission; disconnect releases capacity without executing a query", { timeout: 3_000 }, async (t) => {
  const s = setup(t); const origin = await listen(s); const requests: ClientRequest[] = [];
  t.after(() => { for (const request of requests) request.destroy(); });
  for (let index = 0; index < WEB216_WORKBENCH_MAX_CONCURRENT; index += 1) {
    const request = httpRequest(`${origin}/mcp`, { method: "POST", headers: { "content-length": "50" } });
    requests.push(request); request.on("error", () => undefined); request.flushHeaders();
    await new Promise<void>((resolve) => request.once("socket", (socket) => socket.once("connect", resolve)));
  }
  await new Promise<void>((resolve) => setImmediate(resolve));
  const blocked = await fetch(`${origin}/readyz`); assert.equal(blocked.status, 429);
  assert.equal(blocked.headers.get("retry-after"), "1");
  for (const request of requests) request.destroy();
  await new Promise<void>((resolve) => s.server.getConnections((_error, count) => { assert.ok(count <= 9); resolve(); }));
  await new Promise<void>((resolve) => setImmediate(resolve));
  const recovered = await fetch(`${origin}/readyz`); assert.equal(recovered.status, 200);
  assert.equal(s.state.reconciliationIndex.verify().claim_count, 0);
});

test("a stalled body times out without a claim and shutdown is idempotent", { timeout: 8_000 }, async (t) => {
  const s = setup(t); const origin = await listen(s);
  const result = await new Promise<number>((resolve, reject) => {
    const request = httpRequest(`${origin}/mcp`, { method: "POST", headers: { "content-length": "50" } }, (response) => {
      response.resume(); response.on("end", () => resolve(response.statusCode!));
    });
    t.after(() => request.destroy()); request.on("error", reject); request.flushHeaders();
  });
  assert.equal(result, 408); assert.equal(s.state.ledger.verify().event_count, 0);
  await s.server.closeWorkbench(); await s.server.closeWorkbench(); assert.equal(s.server.listening, false);
});

test("startup rejects unbounded, unrecognised, linked or missing static material", (t) => {
  const s = setup(t);
  writeFileSync(join(s.publicDirectory, "extra.json"), "{}");
  assert.throws(() => createWeb216WorkbenchServer(s.state.application, s.publicDirectory), /Unexpected/u);
  rmSync(join(s.publicDirectory, "extra.json"));
  rmSync(join(s.publicDirectory, "assets", "index-abcdefgh.js"));
  const outside = join(s.root, "outside.js"); writeFileSync(outside, "outside");
  symlinkSync(outside, join(s.publicDirectory, "assets", "index-abcdefgh.js"));
  assert.throws(() => createWeb216WorkbenchServer(s.state.application, s.publicDirectory), /Invalid/u);
  rmSync(join(s.publicDirectory, "assets", "index-abcdefgh.js"));
  writeFileSync(join(s.publicDirectory, "assets", "index-abcdefgh.js"), "x".repeat(2_097_153));
  assert.throws(() => createWeb216WorkbenchServer(s.state.application, s.publicDirectory), /Invalid/u);
});

test("Vite document-relative script and stylesheet assets are admitted without widening URL resolution", async (t) => {
  const s = setup(t);
  // Exact tag shape and hashed filenames observed in the Vite build on
  // 14 September 2026; payloads remain explicitly synthetic test material.
  writeFileSync(join(s.publicDirectory, "assets", "index-DJfBpQic.js"), "// synthetic Vite-shaped script fixture");
  writeFileSync(join(s.publicDirectory, "assets", "index-dkytjW4d.css"), "/* synthetic Vite-shaped style fixture */");
  const page = '<!doctype html><html lang="en-GB"><head><script type="module" crossorigin src="./assets/index-DJfBpQic.js"></script><link rel="stylesheet" crossorigin href="./assets/index-dkytjW4d.css"></head><body>Fixture</body></html>';
  const index = join(s.publicDirectory, "index.html");
  writeFileSync(index, page);
  const admitted = createWeb216WorkbenchServer(s.state.application, s.publicDirectory);
  assert.match(admitted.assetSha256, /^[0-9a-f]{64}$/u); await admitted.closeWorkbench();
  for (const reference of [
    "../assets/index-DJfBpQic.js", "./assets/../index-DJfBpQic.js",
    "./assets/%2e%2e/index-DJfBpQic.js", "assets/index-DJfBpQic.js",
    "//example.org/assets/index-DJfBpQic.js", "https://example.org/assets/index-DJfBpQic.js",
    "./assets/index-DJfBpQic.js?x=1", "./assets/index-DJfBpQic.js#fragment", "/",
  ]) {
    writeFileSync(index, page.replace("./assets/index-DJfBpQic.js", reference));
    assert.throws(() => createWeb216WorkbenchServer(s.state.application, s.publicDirectory), /unavailable asset/u);
  }
});
