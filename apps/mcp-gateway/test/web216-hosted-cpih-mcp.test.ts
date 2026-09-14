import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { DatabaseSync, type SQLInputValue } from "node:sqlite";
import test, { type TestContext } from "node:test";
import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";
import { createMcpHandler, fromJsonSchema, type CallToolResult, type JsonSchemaType } from "@modelcontextprotocol/server";
import { CfWorkerJsonSchemaValidator } from "@modelcontextprotocol/server/validators/cf-worker";
import {
  canonicalJson, createWeb216D1SnapshotStore, createWeb216TransactionalSnapshot, WEB216_D1_SCHEMA_SQL, WEB216_D1_SQL,
  type Web216D1Database, type Web216D1Statement,
} from "@gis-ai-go/evidence";
import { createWeb216HostedCpihApplication, type Web216HostedCpihApplication } from "../src/web216-hosted-cpih-application.js";
import {
  createWeb216HostedCpihMcpServerFactory, validateWeb216HostedCpihMcpResult,
  WEB216_HOSTED_CPIH_MCP_SCHEMAS, WEB216_HOSTED_CPIH_MCP_TOOLS,
} from "../src/web216-hosted-cpih-mcp.js";
import { WEB216_CPIH_INPUT_SCHEMAS } from "../src/web216-cpih-input-schemas.js";
import { WEB216_CPIH_MCP_SCHEMAS } from "../src/web216-cpih-mcp.js";
import { resolveWeb216CpihSelection } from "../src/web216-cpih-selection.js";
import { withMcpHttpDataQuerySignal } from "../src/mcp-request-signal.js";
import { MCP_MAX_TOOL_RESULT_BYTES, MCP_PROTOCOL_VERSION } from "../src/mcp-server.js";
import { MCP_MAX_TOOL_RESULT_BYTES as SHARED_MAX_TOOL_RESULT_BYTES,
  MCP_PROTOCOL_VERSION as SHARED_PROTOCOL_VERSION } from "../src/mcp-constants.js";

const PROJECTION: unknown = JSON.parse(readFileSync(new URL("../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url), "utf8"));
const SOFTWARE = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) } as const;
const NOW = () => new Date("2026-09-14T18:00:00.000Z");
const KEY = ["gis-ai-go", "ik", "v1", "a".repeat(64)].join(":");
const SECOND_KEY = ["gis-ai-go", "ik", "v1", "b".repeat(64)].join(":");
const URL_BASE = "https://example.invalid/mcp";
test("side-effect-free wire constants preserve exact legacy import compatibility", () => {
  assert.equal(SHARED_PROTOCOL_VERSION, "2026-07-28");
  assert.equal(SHARED_MAX_TOOL_RESULT_BYTES, 1_048_576);
  assert.equal(MCP_PROTOCOL_VERSION, SHARED_PROTOCOL_VERSION);
  assert.equal(MCP_MAX_TOOL_RESULT_BYTES, SHARED_MAX_TOOL_RESULT_BYTES);
});
class SqliteD1 implements Web216D1Database {
  readonly sqlite = new DatabaseSync(":memory:");
  readonly hooks: { beforeRead?: () => Promise<void>; afterUpdate?: () => Promise<void> } = {};
  updates = 0;
  constructor() { this.sqlite.exec(WEB216_D1_SCHEMA_SQL); }
  prepare(sql: string): Web216D1Statement {
    const bound = (values: unknown[]): Web216D1Statement => ({
      bind: (...next: unknown[]) => bound(next),
      first: async <T>() => { await this.hooks.beforeRead?.(); return (this.sqlite.prepare(sql).get(...values as SQLInputValue[]) ?? null) as T | null; },
      run: async () => {
        const result = this.sqlite.prepare(sql).run(...values as SQLInputValue[]);
        if (sql === WEB216_D1_SQL.update) { this.updates += 1; await this.hooks.afterUpdate?.(); }
        return { success: true, meta: { changes: Number(result.changes) } };
      },
    });
    return bound([]);
  }
}
async function scenario(t: TestContext, maximumRecords = 32, provisioned = true) {
  const database = new SqliteD1();
  const initialSnapshot = createWeb216TransactionalSnapshot({ projection: PROJECTION, software: SOFTWARE,
    createdAt: NOW().toISOString(), storeNonce: "1".repeat(32), maximumRecords });
  const store = createWeb216D1SnapshotStore({ database, initialSnapshot,
    material: { projection: PROJECTION, expectedSoftware: SOFTWARE, expectedStoreId: initialSnapshot.descriptor.store_id } });
  if (provisioned) await store.initialiseIfAbsent();
  const application = createWeb216HostedCpihApplication({ store, projection: PROJECTION, software: SOFTWARE,
    expectedStoreId: initialSnapshot.descriptor.store_id, now: NOW });
  // Genuine SDK per-request handler, not a listener or the later Site ingress.
  const handler = createMcpHandler(createWeb216HostedCpihMcpServerFactory(application), { legacy: "reject", responseMode: "auto" });
  t.after(async () => { await handler.close(); database.sqlite.close(); });
  return { database, store, application, handler };
}
async function connect(t: TestContext, s: Awaited<ReturnType<typeof scenario>>) {
  const methods: string[] = [];
  const client = new Client({ name: "hosted-cpih-in-process-test", version: "1.0.0" }, {
    capabilities: {}, versionNegotiation: { mode: { pin: MCP_PROTOCOL_VERSION } },
  });
  const localFetch: typeof fetch = (input, init) => {
    const request = new Request(input, init); methods.push(request.headers.get("mcp-method") ?? "none");
    return s.handler.fetch(request);
  };
  t.after(() => client.close());
  await client.connect(new StreamableHTTPClientTransport(new URL(URL_BASE), { fetch: localFetch }));
  assert.equal(client.getProtocolEra(), "modern"); assert.equal(client.getNegotiatedProtocolVersion(), MCP_PROTOCOL_VERSION);
  return { client, methods };
}
function proposal(period: "2026-01" | "2026-07" = "2026-07", key = KEY) {
  return { period, selection_plan_id: resolveWeb216CpihSelection({ period }).plan_id, idempotency_key: key };
}
function body(result: CallToolResult): Record<string, any> {
  assert.equal(result.content.length, 1); const block = result.content[0];
  if (block?.type !== "text") throw Error("Expected a single text block");
  assert.deepEqual(JSON.parse(block.text), result.structuredContent);
  assert.ok(new TextEncoder().encode(JSON.stringify(result)).byteLength <= MCP_MAX_TOOL_RESULT_BYTES);
  assert.equal(JSON.stringify(result).includes(KEY), false); assert.equal(JSON.stringify(result).includes(SECOND_KEY), false);
  return result.structuredContent as Record<string, any>;
}
function raw(name: string, args: unknown, protocol: string = MCP_PROTOCOL_VERSION, clientId = "untrusted-client-correlation") {
  return new Request(URL_BASE, { method: "POST", headers: {
    accept: "application/json, text/event-stream", "content-type": "application/json",
    "mcp-protocol-version": protocol, "mcp-method": "tools/call", "mcp-name": name,
  }, body: JSON.stringify({ jsonrpc: "2.0", id: clientId, method: "tools/call", params: { name, arguments: args, _meta: {
    "io.modelcontextprotocol/protocolVersion": protocol,
    "io.modelcontextprotocol/clientCapabilities": {},
    "io.modelcontextprotocol/clientInfo": { name: "untrusted-test-client", version: "1.0.0" },
    requestId: "untrusted-metadata-request", traceId: "untrusted-metadata-trace",
  } } }) });
}
async function wire(s: Awaited<ReturnType<typeof scenario>>, name: string, args: unknown, signal?: AbortSignal) {
  const request = raw(name, args);
  // Match the existing response-lifetime separation without reimplementing HTTP parsing.
  const response = await (signal === undefined ? s.handler.fetch(request)
    : withMcpHttpDataQuerySignal(signal, () => s.handler.fetch(request)));
  assert.equal(response.status, 200);
  return (await response.json() as { result: CallToolResult }).result;
}
function gate() {
  let release!: () => void; let entered!: () => void;
  const blocked = new Promise<void>((resolve) => { release = resolve; });
  const waiting = new Promise<void>((resolve) => { entered = resolve; });
  return { waiting, release, stop: async () => { entered(); await blocked; } };
}

test("official MCP SDK discovers exact unchanged inputs, new hosted outputs and truthful write annotations", async (t) => {
  const s = await scenario(t); const { client, methods } = await connect(t, s);
  const tools = (await client.listTools()).tools;
  assert.deepEqual(tools.map((tool) => tool.name).sort(), [...WEB216_HOSTED_CPIH_MCP_TOOLS].sort());
  for (const tool of tools) {
    const name = tool.name as typeof WEB216_HOSTED_CPIH_MCP_TOOLS[number];
    assert.deepEqual(tool.inputSchema, WEB216_CPIH_INPUT_SCHEMAS[name]);
    assert.deepEqual(tool.outputSchema, WEB216_HOSTED_CPIH_MCP_SCHEMAS[name].output);
    assert.equal(tool.annotations?.readOnlyHint, name !== "web216_cpih_query");
    assert.equal(tool.annotations?.destructiveHint, false); assert.equal(tool.annotations?.idempotentHint, true);
    assert.equal(tool.annotations?.openWorldHint, false);
  }
  assert.ok(methods.includes("server/discover")); assert.ok(methods.includes("tools/list"));
  assert.equal(s.database.updates, 0);
});

test("real SDK select/query/inspect returns exact index strings and the honest selected-evidence subset", async (t) => {
  const s = await scenario(t); const { client } = await connect(t, s);
  for (const [period, value, key] of [["2026-01", "139.4", KEY], ["2026-07", "142.7", SECOND_KEY]] as const) {
    const selection = body(await client.callTool({ name: "web216_cpih_select", arguments: { period } }));
    assert.equal(selection.authority.grants_execution, false);
    const response = await client.callTool({ name: "web216_cpih_query", arguments: { period, selection_plan_id: selection.plan_id, idempotency_key: key } });
    assert.notEqual(response.isError, true); const result = body(response);
    assert.equal(await validateWeb216HostedCpihMcpResult(result), true);
    assert.equal(result.schema, "gis-ai-go.web216-hosted-cpih-result.v1");
    assert.equal(result.result.observation.value, value); assert.equal(typeof result.result.observation.value, "string");
    assert.equal(result.evidence.receipt.evidence.persistence, "not-persisted");
    assert.equal(result.evidence.storage_observation.persistence, "present-in-verified-adapter-snapshot");
    assert.equal(result.evidence.storage_observation.read_freshness, "not-established-by-application");
    assert.equal(result.evidence.storage_observation.returned_evidence_scope, "selected-record-event-and-head-subset");
    assert.equal(result.boundary.provider_egress, false);
    assert.match(result.evidence.receipt.request_id, /^web216-hosted-[0-9a-f-]{36}$/u);
    assert.match(result.evidence.receipt.trace_id, /^[0-9a-f]{32}$/u);
    for (const arguments_ of [{ receipt_id: result.evidence.receipt.receipt_id }, { idempotency_key: key }]) {
      assert.deepEqual(body(await client.callTool({ name: "web216_cpih_inspect", arguments: arguments_ })), result);
    }
  }
  assert.equal(s.database.updates, 2);
});

test("capacity preserves replay/inspection; changed selection and invalid inputs yield bounded hosted problems", async (t) => {
  const s = await scenario(t, 1); const { client } = await connect(t, s);
  const first = body(await client.callTool({ name: "web216_cpih_query", arguments: proposal() }));
  assert.deepEqual(body(await client.callTool({ name: "web216_cpih_query", arguments: proposal() })), first);
  for (const [arguments_, code] of [[proposal("2026-01"), "conflict"], [proposal("2026-01", SECOND_KEY), "capacity"],
    [{ ...proposal(), policy: "allow" }, "invalid-input"], [{ ...proposal(), selection_plan_id: "forged" }, "invalid-input"]] as const) {
    const response = await client.callTool({ name: "web216_cpih_query", arguments: arguments_ });
    assert.equal(response.isError, true); const problem = body(response);
    assert.equal(problem.schema, "gis-ai-go.web216-hosted-cpih-mcp-problem.v1"); assert.equal(problem.code, code);
    assert.match(problem.request_id, /^web216-hosted-[0-9a-f-]{36}$/u);
  }
  assert.deepEqual(body(await client.callTool({ name: "web216_cpih_inspect", arguments: { idempotency_key: KEY } })), first);
  assert.equal(s.database.updates, 1);
});

test("client JSON-RPC IDs and metadata never become stored server correlation", async (t) => {
  const s = await scenario(t); const response = await s.handler.fetch(raw("web216_cpih_query", proposal()));
  const result = body((await response.json() as { result: CallToolResult }).result);
  assert.notEqual(result.evidence.receipt.request_id, "untrusted-client-correlation");
  assert.notEqual(result.evidence.receipt.request_id, "untrusted-metadata-request");
  assert.notEqual(result.evidence.receipt.trace_id, "untrusted-metadata-trace");
  assert.equal(JSON.stringify(result).includes("untrusted-"), false);
});

test("all three operations receive pre-cancellation; a stalled query read cannot later write", async (t) => {
  const s = await scenario(t); const controller = new AbortController(); controller.abort();
  for (const [name, args] of [["web216_cpih_select", { period: "2026-07" }], ["web216_cpih_query", proposal()],
    ["web216_cpih_inspect", { idempotency_key: KEY }]] as const) {
    const rejected = await wire(s, name, args, controller.signal);
    assert.equal(rejected.isError, true); assert.equal(body(rejected).code, "cancelled");
  }
  const waiting = gate(); const live = new AbortController();
  s.database.hooks.beforeRead = waiting.stop;
  const operation = wire(s, "web216_cpih_query", proposal(), live.signal);
  await waiting.waiting; live.abort(); waiting.release();
  assert.equal(body(await operation).code, "cancelled"); delete s.database.hooks.beforeRead;
  assert.equal(s.database.updates, 0);
});

test("cancellation after a real SQLite commit returns uncertain-write and same-key retry recovers the original", async (t) => {
  const s = await scenario(t); const waiting = gate(); const controller = new AbortController();
  s.database.hooks.afterUpdate = waiting.stop;
  const operation = wire(s, "web216_cpih_query", proposal(), controller.signal);
  await waiting.waiting; controller.abort(); waiting.release();
  const failed = await operation; assert.equal(failed.isError, true); assert.equal(body(failed).code, "uncertain-write");
  delete s.database.hooks.afterUpdate;
  const recovered = body(await wire(s, "web216_cpih_query", proposal()));
  assert.equal(recovered.evidence.receipt.receipt_id, (await s.store.readSnapshot()).records[0]!.receipt.receipt_id);
  assert.equal(s.database.updates, 1);
});

test("closed output rejects altered values, hashes, nested authority and invented stronger evidence claims", async (t) => {
  const s = await scenario(t); const result = body(await wire(s, "web216_cpih_query", proposal()));
  const oldValidator = fromJsonSchema<unknown>(WEB216_CPIH_MCP_SCHEMAS.web216_cpih_query.output as JsonSchemaType);
  assert.ok((await oldValidator["~standard"].validate(result)).issues);
  for (const mutate of [
    (v: any) => { v.result.observation.value = 142.7; },
    (v: any) => { v.result.series.unit = "percentage"; },
    (v: any) => { v.evidence.record.record_id = `gis-ai-go:web216-transactional-record:sha256:${"f".repeat(64)}`; },
    (v: any) => { v.evidence.event.idempotency_key_sha256 = "f".repeat(64); },
    (v: any) => { v.evidence.receipt.policy_scope.extra = "allow"; },
    (v: any) => { v.evidence.storage_observation.read_freshness = "primary-guaranteed"; },
    (v: any) => { v.evidence.storage_observation.independent_rollback_anchor = true; },
    (v: any) => { v.evidence.checkpoint.sequence = 129; },
    (v: any) => { v.evidence.record.boundary.persistence = "persisted"; },
  ]) {
    const altered: unknown = JSON.parse(JSON.stringify(result)); mutate(altered);
    assert.equal(await validateWeb216HostedCpihMcpResult(altered), false);
  }
});

test("Workers schema annotations stay private and preserve frozen public contracts and validation predicates", async (t) => {
  const s = await scenario(t);
  const before = canonicalJson(WEB216_HOSTED_CPIH_MCP_SCHEMAS);
  const selected = body(await wire(s, "web216_cpih_select", { period: "2026-07" }));
  const queried = body(await wire(s, "web216_cpih_query", proposal()));
  const problem = body(await wire(s, "web216_cpih_query", { ...proposal(), policy: "allow" }));
  for (const name of WEB216_HOSTED_CPIH_MCP_TOOLS) {
    const published = WEB216_HOSTED_CPIH_MCP_SCHEMAS[name].output;
    assert.ok(Object.isFrozen(published)); assert.ok(Object.isFrozen(published.oneOf));
    assert.throws(() => fromJsonSchema(published as JsonSchemaType, new CfWorkerJsonSchemaValidator()), /not extensible/u);
    const copy = JSON.parse(canonicalJson(published)) as JsonSchemaType;
    const worker = fromJsonSchema(copy, new CfWorkerJsonSchemaValidator());
    const node = fromJsonSchema(JSON.parse(canonicalJson(published)) as JsonSchemaType);
    assert.equal(Object.hasOwn(copy, "__absolute_uri__"), true);
    assert.equal(Object.hasOwn(published, "__absolute_uri__"), false);
    const valid = name === "web216_cpih_select" ? selected : queried;
    for (const [value, accepted] of [[valid, true], [problem, true], [{ ...valid, extra: "authority" }, false],
      [name === "web216_cpih_select" ? { ...selected, authority: { grants_execution: true } }
        : { ...queried, result: { ...queried.result, observation: { ...queried.result.observation, value: 142.7 } } }, false]] as const) {
      assert.equal((await worker["~standard"].validate(value)).issues === undefined, accepted);
      assert.equal((await node["~standard"].validate(value)).issues === undefined, accepted);
    }
  }
  assert.equal(canonicalJson(WEB216_HOSTED_CPIH_MCP_SCHEMAS), before);
});

test("inspection of an older record discloses a selected subset and a later returned head, not a full chain proof", async (t) => {
  const s = await scenario(t); const first = body(await wire(s, "web216_cpih_query", proposal()));
  await wire(s, "web216_cpih_query", proposal("2026-01", SECOND_KEY));
  const inspected = body(await wire(s, "web216_cpih_inspect", { receipt_id: first.evidence.receipt.receipt_id }));
  assert.deepEqual(inspected.evidence.record, first.evidence.record);
  assert.equal(inspected.evidence.event.sequence, 1); assert.equal(inspected.evidence.checkpoint.sequence, 2);
  assert.equal(inspected.evidence.storage_observation.returned_evidence_scope, "selected-record-event-and-head-subset");
  assert.equal(await validateWeb216HostedCpihMcpResult(inspected), true);
});

test("missing storage stays unavailable; forged applications and old protocol are rejected without writes", async (t) => {
  const s = await scenario(t, 32, false);
  assert.equal(body(await wire(s, "web216_cpih_query", proposal())).code, "unavailable");
  assert.throws(() => createWeb216HostedCpihMcpServerFactory({ ...s.application }), /genuine/u);
  let touched = false; const fake = new Proxy({}, { get() { touched = true; throw Error("Do not execute"); } });
  assert.throws(() => createWeb216HostedCpihMcpServerFactory(fake as Web216HostedCpihApplication), /genuine/u);
  assert.equal(touched, false);
  const factory = createWeb216HostedCpihMcpServerFactory(s.application);
  assert.throws(() => factory({ era: "legacy" }), /modern/u);
  assert.ok((await s.handler.fetch(raw("web216_cpih_query", proposal(), "2025-11-25"))).status >= 400);
  assert.equal(s.database.updates, 0);
});
