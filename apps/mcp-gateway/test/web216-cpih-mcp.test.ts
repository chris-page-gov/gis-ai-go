import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test, { type TestContext } from "node:test";
import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";
import { fromJsonSchema, type CallToolResult, type JsonSchemaType } from "@modelcontextprotocol/server";
import { openPublicEvidenceLedger, openWeb216CpihReconciliationIndex, verifyStoredPublicEvidenceProjection } from "@gis-ai-go/evidence";
import { createWeb216CpihApplication, type Web216CpihApplication } from "../src/web216-cpih-application.js";
import { createCatalogueMcpHttpHandler, createWeb216CpihMcpHttpHandler } from "../src/mcp-http.js";
import { createCatalogueApplication } from "../src/catalogue-application.js";
import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";
import { createWeb216CpihMcpServerFactory, WEB216_CPIH_MCP_SCHEMAS, WEB216_CPIH_MCP_TOOLS } from "../src/web216-cpih-mcp.js";
import { MCP_MAX_TOOL_RESULT_BYTES, MCP_PROTOCOL_VERSION } from "../src/mcp-server.js";

const PROJECTION: unknown = JSON.parse(readFileSync(new URL("../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url), "utf8"));
const SOFTWARE = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) } as const;
const NOW = () => new Date("2026-09-14T18:00:00.000Z");
const KEY = ["gis-ai-go", "ik", "v1", "a".repeat(64)].join(":");
const SECOND_KEY = ["gis-ai-go", "ik", "v1", "b".repeat(64)].join(":");
const URL_BASE = "http://127.0.0.1:8788/mcp";

function scenario(t: TestContext) {
  const root = mkdtempSync(join(tmpdir(), "web216-mcp-"));
  const ledger = openPublicEvidenceLedger({ rootDirectory: join(root, "ledger"), now: NOW });
  const reconciliationIndex = openWeb216CpihReconciliationIndex({ rootDirectory: join(root, "index"), ledger, now: NOW });
  const application = createWeb216CpihApplication({ ledger, reconciliationIndex, projection: PROJECTION, software: SOFTWARE, now: NOW });
  const handler = createWeb216CpihMcpHttpHandler(application);
  t.after(async () => { await handler.close(); rmSync(root, { recursive: true, force: true }); });
  return { ledger, reconciliationIndex, application, handler };
}

async function connect(t: TestContext, s: ReturnType<typeof scenario>) {
  const methods: string[] = [];
  const localFetch: typeof fetch = (input, init) => {
    const request = new Request(input, init);
    methods.push(request.headers.get("mcp-method") ?? "none");
    return s.handler.fetch(request);
  };
  const client = new Client({ name: "gis-ai-go-web216-wire-test", version: "1.0.0" }, {
    capabilities: {}, versionNegotiation: { mode: { pin: MCP_PROTOCOL_VERSION } },
  });
  const transport = new StreamableHTTPClientTransport(new URL(URL_BASE), { fetch: localFetch });
  t.after(() => client.close());
  await client.connect(transport);
  assert.equal(client.getProtocolEra(), "modern");
  assert.equal(client.getNegotiatedProtocolVersion(), MCP_PROTOCOL_VERSION);
  return { client, methods };
}

function body(result: CallToolResult): Record<string, any> {
  assert.equal(result.content.length, 1);
  const block = result.content[0];
  assert.equal(block?.type, "text");
  if (block?.type !== "text") throw Error("Expected text block");
  assert.deepEqual(JSON.parse(block.text), result.structuredContent);
  assert.ok(new TextEncoder().encode(JSON.stringify(result)).length <= MCP_MAX_TOOL_RESULT_BYTES);
  assert.equal(JSON.stringify(result).includes(KEY), false);
  assert.equal(JSON.stringify(result).includes(SECOND_KEY), false);
  return result.structuredContent as Record<string, any>;
}
function proposal(s: ReturnType<typeof scenario>, period: "2026-01" | "2026-07" = "2026-07", key = KEY) {
  return { period, selection_plan_id: s.application.resolve({ period }).plan_id, idempotency_key: key };
}
function raw(name: string, args: unknown, options: {
  id?: string; url?: string; headers?: Record<string, string>; signal?: AbortSignal;
} = {}): Request {
  return new Request(options.url ?? URL_BASE, {
    method: "POST", ...(options.signal === undefined ? {} : { signal: options.signal }),
    headers: {
      accept: "application/json, text/event-stream", "content-type": "application/json",
      "mcp-protocol-version": MCP_PROTOCOL_VERSION, "mcp-method": "tools/call", "mcp-name": name,
      ...options.headers,
    },
    body: JSON.stringify({ jsonrpc: "2.0", id: options.id ?? "wire-call", method: "tools/call", params: {
      name, arguments: args, _meta: {
        "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
        "io.modelcontextprotocol/clientCapabilities": {},
        "io.modelcontextprotocol/clientInfo": { name: "web216-wire-test", version: "1.0.0" },
      },
    } }),
  });
}

test("official SDK discovers exactly three closed experimental tools with truthful write effects", async (t) => {
  const s = scenario(t); const { client, methods } = await connect(t, s);
  const tools = (await client.listTools()).tools;
  assert.deepEqual(tools.map((tool) => tool.name).sort(), [...WEB216_CPIH_MCP_TOOLS].sort());
  for (const tool of tools) {
    const name = tool.name as typeof WEB216_CPIH_MCP_TOOLS[number];
    assert.deepEqual(tool.inputSchema, WEB216_CPIH_MCP_SCHEMAS[name].input);
    assert.deepEqual(tool.outputSchema, WEB216_CPIH_MCP_SCHEMAS[name].output);
    assert.equal(tool.annotations?.readOnlyHint, name !== "web216_cpih_query");
    assert.equal(tool.annotations?.destructiveHint, false);
    assert.equal(tool.annotations?.idempotentHint, true);
    assert.equal(tool.annotations?.openWorldHint, false);
  }
  const selected = body(await client.callTool({ name: "web216_cpih_select", arguments: { period: "2026-07" } }));
  assert.equal(selected.authority.grants_execution, false);
  assert.equal(selected.currency, "captured-data-not-live-or-always-current");
  assert.ok(methods.includes("server/discover")); assert.ok(methods.includes("tools/list"));
  assert.equal(s.ledger.verify().event_count, 0); assert.equal(s.reconciliationIndex.verify().claim_count, 0);
});

test("official SDK select/query/inspect preserves decimal strings and durable full-material evidence for both periods", async (t) => {
  const s = scenario(t); const { client } = await connect(t, s);
  for (const [period, value, key] of [["2026-01", "139.4", KEY], ["2026-07", "142.7", SECOND_KEY]] as const) {
    const selected = body(await client.callTool({ name: "web216_cpih_select", arguments: { period } }));
    const response = await client.callTool({ name: "web216_cpih_query", arguments: { period, selection_plan_id: selected.plan_id, idempotency_key: key } });
    assert.notEqual(response.isError, true);
    const result = body(response);
    assert.equal(result.result.observation.value, value);
    assert.equal(typeof result.result.observation.value, "string");
    assert.equal(result.result.series.base_year, 2015);
    assert.equal(result.result.provider_egress, false);
    assert.equal(result.evidence.storage.status, "persisted");
    assert.equal(result.evidence.receipt.evidence.persistence, "not-persisted");
    assert.equal(result.evidence.record.schema, "gis-ai-go.public-evidence-record.v3");
    assert.equal(result.evidence.record.verification.receipt, "full-material-verified-at-ingest");
    assert.equal(result.boundary.activated_supported_release, false);
    assert.equal(result.boundary.attested, false);
    assert.match(result.evidence.receipt.request_id, /^web216-[0-9a-f-]{36}$/u);
    assert.match(result.evidence.receipt.trace_id, /^[0-9a-f]{32}$/u);
    assert.equal(verifyStoredPublicEvidenceProjection({ record: result.evidence.record, event: result.evidence.event, reference: result.evidence.storage }), true);
    for (const arguments_ of [{ receipt_id: result.evidence.receipt.receipt_id }, { idempotency_key: key }]) {
      assert.deepEqual(body(await client.callTool({ name: "web216_cpih_inspect", arguments: arguments_ })), result);
    }
  }
  assert.equal(s.ledger.verify().event_count, 2); assert.equal(s.reconciliationIndex.verify().completed_count, 2);
});

test("same-key replay returns the original stored result; conflicting selection and invalid input make no new claim", async (t) => {
  const s = scenario(t); const { client } = await connect(t, s);
  const call = { name: "web216_cpih_query", arguments: proposal(s) };
  const first = body(await client.callTool(call));
  assert.deepEqual(body(await client.callTool(call)), first);
  const conflict = await client.callTool({ name: call.name, arguments: proposal(s, "2026-01") });
  assert.equal(conflict.isError, true); assert.equal(body(conflict).code, "conflict");
  for (const args of [{ ...proposal(s), url: "https://example.org/private" }, { ...proposal(s), selection_plan_id: KEY }, { ...proposal(s), period: "latest" }]) {
    const rejected = await client.callTool({ name: call.name, arguments: args });
    assert.equal(rejected.isError, true); assert.equal(body(rejected).code, "invalid-request");
    assert.equal(JSON.stringify(rejected).includes("example.org"), false);
  }
  assert.equal(s.ledger.verify().event_count, 1); assert.equal(s.reconciliationIndex.verify().claim_count, 1);
});

test("read-only missing lookup and pre-admission HTTP cancellation return bounded problems without writes", async (t) => {
  const s = scenario(t); const { client } = await connect(t, s);
  const missing = await client.callTool({ name: "web216_cpih_inspect", arguments: { idempotency_key: KEY } });
  assert.equal(missing.isError, true); assert.equal(body(missing).code, "not-found");
  const controller = new AbortController(); controller.abort();
  const response = await s.handler.fetch(raw("web216_cpih_query", proposal(s), { signal: controller.signal }));
  assert.equal(response.status, 200);
  const wire = await response.json() as { result: CallToolResult };
  assert.equal(wire.result.isError, true); assert.equal(body(wire.result).code, "cancelled");
  assert.equal(s.ledger.verify().event_count, 0); assert.equal(s.reconciliationIndex.verify().claim_count, 0);
});

test("loopback authority, Origin, Host and route are closed before application calls", async (t) => {
  const s = scenario(t);
  for (const options of [
    { url: "https://127.0.0.1:8788/mcp" }, { url: "http://example.org:8788/mcp" },
    { url: "http://127.0.0.1:8788/other" }, { url: `${URL_BASE}?query=anything` },
    { url: "http://127.0.0.1:8787/mcp" }, { url: "http://127.0.0.1/mcp" },
    { headers: { origin: "https://example.org" } }, { headers: { origin: "null" } },
    { headers: { host: "example.org" } },
  ]) {
    const response = await s.handler.fetch(raw("web216_cpih_query", proposal(s), options));
    assert.equal(response.status, 403);
    assert.equal((await response.json() as any).error.data.reason, "experimental_loopback_boundary");
  }
  const allowed = await s.handler.fetch(raw("web216_cpih_select", { period: "2026-01" }, { headers: { origin: "http://127.0.0.1:8788", host: "127.0.0.1:8788" } }));
  assert.equal(allowed.status, 200);
  assert.equal(s.ledger.verify().event_count, 0); assert.equal(s.reconciliationIndex.verify().claim_count, 0);
});

test("sensitive JSON-RPC control fields and oversized wire bodies are rejected without reflection or writes", { timeout: 2_000 }, async (t) => {
  const s = scenario(t);
  for (const request of [
    raw("web216_cpih_query", proposal(s), { id: KEY }),
    raw("web216_cpih_query", proposal(s), { id: encodeURIComponent(KEY) }),
    raw(KEY, proposal(s)),
  ]) {
    const response = await s.handler.fetch(request);
    assert.equal(response.status, 400);
    const value = await response.json() as any;
    assert.equal(value.id, null); assert.equal(JSON.stringify(value).includes(KEY), false);
    assert.equal(JSON.stringify(value).includes(encodeURIComponent(KEY)), false);
  }
  const oversized = await s.handler.fetch(raw("web216_cpih_query", { ...proposal(s), extra: "x".repeat(65_536) }));
  assert.equal(oversized.status, 413);
  assert.equal(s.ledger.verify().event_count, 0); assert.equal(s.reconciliationIndex.verify().claim_count, 0);
});

test("the existing catalogue wrapper also refuses oversized streaming bodies without waiting for producer cleanup", { timeout: 2_000 }, async (t) => {
  const snapshot = await loadCatalogueSnapshot(new URL("../../../../artifacts/okf/", import.meta.url).pathname, { now: NOW() });
  const application = createCatalogueApplication(snapshot, { software: SOFTWARE, now: NOW });
  const handler = createCatalogueMcpHttpHandler({ application, snapshot });
  t.after(() => handler.close());
  let producerCancelled = false;
  const stream = new ReadableStream<Uint8Array>({
    start(controller) { controller.enqueue(new TextEncoder().encode("x".repeat(65_537))); },
    cancel() { producerCancelled = true; return new Promise<void>(() => undefined); },
  });
  const request = new Request("http://127.0.0.1:8787/mcp", {
    method: "POST", body: stream, duplex: "half",
    headers: { accept: "application/json, text/event-stream", "content-type": "application/json" },
  } as RequestInit & { duplex: "half" });
  const response = await handler.fetch(request);
  assert.equal(response.status, 413);
  assert.equal((await response.json() as any).error.data.reason, "request_body_too_large");
  assert.equal(producerCancelled, true);
});

test("the experimental wrapper parses wire bytes, not supplied parsed-body overrides, and retains protocol guards", async (t) => {
  const s = scenario(t);
  const fabricated = JSON.parse(await raw("web216_cpih_query", proposal(s)).text()) as unknown;
  const actualSelection = raw("web216_cpih_select", { period: "2026-01" });
  const selectionResponse = await s.handler.fetch(actualSelection, { parsedBody: fabricated });
  assert.equal(selectionResponse.status, 200);
  const selection = (await selectionResponse.json() as { result: CallToolResult }).result;
  assert.equal(body(selection).schema, "gis-ai-go.web216-cpih-selection-plan.v1");
  for (const headers of [
    { "mcp-protocol-version": "2025-11-25" },
    { "mcp-name": "data.query" },
    { accept: "application/json" },
  ]) {
    const response = await s.handler.fetch(raw("web216_cpih_query", proposal(s), { headers }));
    assert.ok(response.status >= 400);
  }
  const duplicate = new Request(URL_BASE, {
    method: "POST", headers: { accept: "application/json, text/event-stream", "content-type": "application/json" },
    body: '{"jsonrpc":"2.0","id":1,"id":2,"method":"tools/call"}',
  });
  assert.equal((await s.handler.fetch(duplicate)).status, 400);
  assert.equal(s.ledger.verify().event_count, 0); assert.equal(s.reconciliationIndex.verify().claim_count, 0);
});

test("output schema rejects substituted scientific content and unknown nested evidence; fake applications cannot construct the MCP face", async (t) => {
  const s = scenario(t); const { client } = await connect(t, s);
  const result = body(await client.callTool({ name: "web216_cpih_query", arguments: proposal(s) }));
  const schema = fromJsonSchema<unknown>(WEB216_CPIH_MCP_SCHEMAS.web216_cpih_query.output as JsonSchemaType);
  for (const change of [
    (value: any) => { value.result.observation.value = 142.7; },
    (value: any) => { value.result.series.unit = "percentage"; },
    (value: any) => { value.evidence.storage.extra = "unknown"; },
    (value: any) => { value.evidence.receipt.policy_scope.grants_provider_permission = true; },
  ]) {
    const altered: unknown = JSON.parse(JSON.stringify(result)); change(altered);
    assert.ok((await schema["~standard"].validate(altered)).issues);
  }
  assert.throws(() => createWeb216CpihMcpServerFactory({ ...s.application }), /genuine/u);
  assert.throws(() => createWeb216CpihMcpHttpHandler({} as Web216CpihApplication), /genuine/u);
  let touched = false;
  const fake = new Proxy({}, { get() { touched = true; throw Error("Do not execute"); } });
  assert.throws(() => createWeb216CpihMcpServerFactory(fake as Web216CpihApplication), /genuine/u);
  assert.equal(touched, false);
});
