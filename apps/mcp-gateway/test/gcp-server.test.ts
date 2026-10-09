import assert from "node:assert/strict";
import { request as httpRequest } from "node:http";
import test, { type TestContext } from "node:test";
import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";
import { createGcpFetchHandler, createGcpServer, type GcpReleaseAsset } from "../src/gcp-server.js";
import { createGcpJwtVerifier, type GcpRole } from "../src/gcp-identity.js";
import { provisionGcpCpihPrincipal } from "../src/gcp-application.js";
import { GCP_TOOL_CAPABILITIES } from "../src/gcp-mcp.js";
import { MCP_PROTOCOL_VERSION } from "../src/mcp-constants.js";
import { CLOCK, credentials, EVIDENCE, FakeAtomicStore, jwksFetch, knowledge, ORIGIN, principal, PROJECTION, runtimeConfig } from "./gcp-test-support.js";
function assets() {
  const files = new Map<string, GcpReleaseAsset>();
  files.set("/", { bytes: Buffer.from("<h1>Current private GIS AI GO site</h1>"), contentType: "text/html", kind: "website" });
  files.set("/explorer", files.get("/")!);
  files.set("/bundles/okf-plus/metadata.json", { bytes: Buffer.from('{"admitted":"public-metadata"}'), contentType: "application/json", kind: "knowledge" });
  files.set("/exports/bundles/okf-plus/okf-bundle.json", { bytes: Buffer.from('{"admitted":"public-metadata"}'), contentType: "application/json", kind: "export" });
  return files;
}
function scenario(roles: readonly GcpRole[] = ["analyst"], personal = false) {
  const config = runtimeConfig(roles, personal ? "personal" : "bduk"); const backend = new FakeAtomicStore();
  const options = { config, projection: PROJECTION, knowledge: knowledge(), assets: assets(), backend,
    verifier: createGcpJwtVerifier({ fetch: jwksFetch, now: () => CLOCK }), now: () => new Date(CLOCK) };
  return { options, backend, config, handler: createGcpFetchHandler(options) };
}
function request(s: ReturnType<typeof scenario>, path: string, options: RequestInit = {}) {
  return new Request(ORIGIN + path, { ...options, headers: { ...credentials(s.config), origin: ORIGIN, ...Object.fromEntries(new Headers(options.headers)) } });
}
async function client(t: TestContext, s: ReturnType<typeof scenario>) {
  const c = new Client({ name: "synthetic-private-gcp-test", version: "1.0.0" }, { capabilities: {}, versionNegotiation: { mode: { pin: MCP_PROTOCOL_VERSION } } });
  t.after(() => c.close());
  await c.connect(new StreamableHTTPClientTransport(new URL(`${ORIGIN}/mcp`), { fetch: async (input, init) => {
    const req = new Request(input, init); const headers = new Headers(req.headers);
    for (const [key, value] of Object.entries(credentials(s.config))) headers.set(key, value);
    headers.set("origin", ORIGIN); return s.handler.fetch(new Request(req, { headers }));
  } }));
  return c;
}

test("all corpus/HTML/export routes require signed identities; role/scope controls cannot be supplied via URLs", async () => {
  const s = scenario(["viewer"]);
  for (const path of ["/", "/api/release", "/bundles/okf-plus/metadata.json", "/exports/bundles/okf-plus/okf-bundle.json", "/mcp"]) {
    assert.equal((await s.handler.fetch(new Request(ORIGIN + path))).status, 401);
  }
  assert.equal((await s.handler.fetch(new Request(ORIGIN + "/healthz"))).status, 200);
  assert.equal((await s.handler.fetch(request(s, "/"))).status, 200);
  assert.equal((await s.handler.fetch(request(s, "/bundles/okf-plus/metadata.json"))).status, 200);
  assert.equal((await s.handler.fetch(request(s, "/exports/bundles/okf-plus/okf-bundle.json"))).status, 403);
  assert.equal((await s.handler.fetch(request(s, "/explorer?q=inflation&view=table&tag=ons"))).status, 200);
  for (const path of ["/?role=owner", "/mcp?role=owner", "/bundles/okf-plus/metadata.json?token=anything"]) {
    assert.equal((await s.handler.fetch(request(s, path))).status, 400);
  }
  assert.equal((await s.handler.fetch(request(s, "/", { headers: { origin: "https://attacker.example" } }))).status, 400);
  assert.equal((await s.handler.fetch(request(s, "/", { headers: { host: "attacker.example" } }))).status, 400);
  assert.equal(s.backend.writes, 0);
});

test("OAuth metadata bootstrap requires verified private transport but no pre-existing application bearer", async () => {
  const s = scenario(); const supplied = credentials(s.config);
  const discovery = new Request(`${ORIGIN}/.well-known/oauth-protected-resource/mcp`, { headers: { "x-gis-invocation-proof": supplied["x-gis-invocation-proof"] } });
  const response = await s.handler.fetch(discovery); assert.equal(response.status, 200);
  assert.equal((await response.json() as { resource: string }).resource, `${ORIGIN}/mcp`);
  assert.equal((await s.handler.fetch(new Request(discovery.url))).status, 401);
  const unavailable = await s.handler.fetch(new Request(`${ORIGIN}/mcp`, { headers: { "x-gis-invocation-proof": supplied["x-gis-invocation-proof"] } }));
  assert.equal(unavailable.status, 401); assert.match(unavailable.headers.get("www-authenticate")!, /resource_metadata=/u);
  const owner = scenario([], true);
  assert.equal((await owner.handler.fetch(request(owner, "/.well-known/oauth-protected-resource/mcp"))).status, 404);
});

test("role-filtered official-client discovery, direct invocation, resource reads and exports share policy", async (t) => {
  const expected: readonly [GcpRole, string[]][] = [
    ["viewer", ["okf_describe", "okf_search", "web216_cpih_select"]],
    ["analyst", ["okf_describe", "okf_search", "web216_cpih_inspect", "web216_cpih_query", "web216_cpih_select"]],
    ["evidence-auditor", ["okf_describe", "okf_search", "web216_cpih_inspect"]],
    ["platform-operator", []], ["owner", Object.keys(GCP_TOOL_CAPABILITIES).sort()],
  ];
  for (const [role, names] of expected) {
    const s = scenario([role]); const c = await client(t, s);
    assert.deepEqual((await c.listTools()).tools.map((tool) => tool.name).sort(), names);
    assert.equal((await c.listResources()).resources.length, role === "platform-operator" ? 0 : 1);
    if (role === "viewer" || role === "platform-operator") {
      await assert.rejects(c.callTool({ name: "web216_cpih_query", arguments: { period: "2026-07", selection_plan_id: "unapproved", idempotency_key: `gis-ai-go:ik:v1:${"a".repeat(64)}` } }));
      assert.equal(s.backend.writes, 0);
    }
    if (role === "platform-operator") {
      await assert.rejects(c.readResource({ uri: "gis-ai-go://gcp/release" }));
      assert.equal((await s.handler.fetch(request(s, "/api/release"))).status, 403);
    }
    assert.equal((await s.handler.fetch(request(s, "/exports/bundles/okf-plus/okf-bundle.json"))).status, role === "owner" ? 200 : 403);
    await c.close();
  }
});

test("official custom MCP returns maintained CPIH receipt and shared metadata release, with no provider requests", async (t) => {
  const s = scenario(["analyst"]); const actor = await principal();
  await provisionGcpCpihPrincipal({ backend: s.backend, principalScope: actor.scope, projection: PROJECTION, evidence: EVIDENCE });
  const c = await client(t, s);
  const plan = (await c.callTool({ name: "web216_cpih_select", arguments: { period: "2026-07" } })).structuredContent as { plan_id: string };
  const result = (await c.callTool({ name: "web216_cpih_query", arguments: { period: "2026-07", selection_plan_id: plan.plan_id, idempotency_key: `gis-ai-go:ik:v1:${"a".repeat(64)}` } })).structuredContent as { result: { observation: { value: string } }; evidence: { receipt: { receipt_id: string } } };
  assert.equal(result.result.observation.value, "142.7");
  const inspected = (await c.callTool({ name: "web216_cpih_inspect", arguments: { receipt_id: result.evidence.receipt.receipt_id } })).structuredContent;
  assert.deepEqual(inspected, result);
  const metadata = (await c.callTool({ name: "okf_search", arguments: { bundle: "okf-plus", query: "inflation", limit: 1 } })).structuredContent as { records: { sources: unknown[] }[]; truncated: boolean; provenance: { release_sha256: string } };
  assert.equal(metadata.records.length, 1); assert.equal(metadata.truncated, true); assert.ok(metadata.records[0]!.sources.length);
  const api = await s.handler.fetch(request(s, "/api/knowledge/search?bundle=okf-plus&query=inflation&limit=1"));
  assert.deepEqual(await api.json(), metadata);
  assert.equal(metadata.provenance.release_sha256, "d".repeat(64));
});

test("real Node listener honours Cloud Run bind contract, duplicate headers, body bounds and graceful shutdown", async (t) => {
  const s = scenario([], true); const server = createGcpServer(s.options);
  t.after(async () => { if (server.listening) await server.closePrivateRuntime(); });
  await new Promise<void>((done) => server.listen(0, "0.0.0.0", done));
  const address = server.address(); assert.ok(address && typeof address === "object"); assert.equal(address.address, "0.0.0.0");
  const target = `http://127.0.0.1:${address.port}`;
  assert.equal((await fetch(target + "/healthz")).status, 200);
  const headers = { ...credentials(s.config), host: new URL(ORIGIN).host, origin: "http://127.0.0.1:8789" };
  const authorised = await new Promise<number>((done, reject) => {
    const r = httpRequest(target, { headers }, (res) => { res.resume(); res.on("end", () => done(res.statusCode!)); });
    r.on("error", reject); r.end();
  });
  assert.equal(authorised, 200);
  const duplicate = await new Promise<number>((done, reject) => {
    const r = httpRequest(target, { headers: ["Host", new URL(ORIGIN).host, "X-Gis-Invocation-Proof", headers["x-gis-invocation-proof"], "X-Gis-Invocation-Proof", headers["x-gis-invocation-proof"]] }, (res) => { res.resume(); res.on("end", () => done(res.statusCode!)); });
    r.on("error", reject); r.end();
  });
  assert.equal(duplicate, 400);
  assert.equal((await fetch(target + "/mcp", { method: "POST", headers, body: "x".repeat(65_537) })).status, 413);
  await server.closePrivateRuntime(); assert.equal(server.listening, false);
});

test("bootstrap revision only serves liveness; it cannot expose content or choose a mock identity", async () => {
  const s = scenario(); const handler = createGcpFetchHandler({ ...s.options, config: null });
  assert.equal((await handler.fetch(new Request(ORIGIN + "/healthz"))).status, 200);
  for (const path of ["/", "/mcp", "/api/release", "/readyz"]) assert.equal((await handler.fetch(request(s, path))).status, 503);
});

test("approved private browser origin and canonical Cloud Run transport Host stay distinct", async () => {
  const s = scenario(["viewer"]); const privateOrigin = "https://synthetic.private.example";
  const config = { ...s.config, publicOrigin: privateOrigin, transportAudience: ORIGIN, allowedOrigins: [privateOrigin] };
  const handler = createGcpFetchHandler({ ...s.options, config });
  const headers = { ...credentials(config), host: new URL(ORIGIN).host, origin: privateOrigin };
  assert.equal((await handler.fetch(new Request(ORIGIN, { headers }))).status, 200);
  assert.equal((await handler.fetch(new Request(ORIGIN, { headers: { ...headers, origin: ORIGIN } }))).status, 400);
  const discovery = await handler.fetch(new Request(ORIGIN + "/.well-known/oauth-protected-resource/mcp", { headers: { host: new URL(ORIGIN).host,
    "x-gis-invocation-proof": headers["x-gis-invocation-proof"] } }));
  assert.equal(discovery.status, 200); assert.equal((await discovery.json() as { resource: string }).resource, privateOrigin + "/mcp");
});
