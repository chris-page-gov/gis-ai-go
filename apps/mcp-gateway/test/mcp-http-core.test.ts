import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { DatabaseSync, type SQLInputValue } from "node:sqlite";
import test, { type TestContext } from "node:test";
import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";
import { McpServer } from "@modelcontextprotocol/server";
import {
  createWeb216D1SnapshotStore, createWeb216TransactionalSnapshot, WEB216_D1_SCHEMA_SQL, WEB216_D1_SQL,
  type Web216D1Database, type Web216D1Statement,
} from "@gis-ai-go/evidence/web216-pure";
import * as guards from "../src/mcp-wire-guards.js";
import * as originalGuards from "../src/mcp-server.js";
import { BoundedJsonError, parseBoundedJsonBytes } from "../src/bounded-json.js";
import { BoundedJsonError as OriginalJsonError, parseBoundedJsonBytes as originalParser } from "../src/http-app.js";
import { MCP_HTTP_MAX_STANDALONE_BODY_BYTES as originalBodyLimit } from "../src/mcp-http.js";
import { createBoundedMcpHttpHandler, createBoundedJsonOnlyMcpHttpHandler, MCP_HTTP_MAX_STANDALONE_BODY_BYTES } from "../src/mcp-http-core.js";
import { MCP_PROTOCOL_VERSION } from "../src/mcp-constants.js";
import { createWeb216HostedCpihApplication } from "../src/web216-hosted-cpih-application.js";
import { createWeb216HostedCpihMcpHttpHandler } from "../src/web216-hosted-cpih-http.js";
import { resolveWeb216CpihSelection } from "../src/web216-cpih-selection.js";

const URL_BASE = "https://example.invalid/workbench/mcp";
const KEY = ["gis-ai-go", "ik", "v1", "a".repeat(64)].join(":");
const SOFTWARE = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) } as const;
const NOW = () => new Date("2026-09-14T18:00:00.000Z");
const PROJECTION: unknown = JSON.parse(readFileSync(new URL("../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url), "utf8"));
const encoder = new TextEncoder();
function message(method = "tools/call", name = "web216_cpih_query", arguments_: unknown = proposal()) {
  return { jsonrpc: "2.0", id: "http-core-test", method, params: { name, arguments: arguments_, _meta: {
    "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
    "io.modelcontextprotocol/clientCapabilities": {},
    "io.modelcontextprotocol/clientInfo": { name: "bounded-http-test", version: "1.0.0" },
  } } };
}
function request(body: string | Uint8Array = JSON.stringify(message()), headers: Record<string, string> = {}, signal?: AbortSignal) {
  return new Request(URL_BASE, { method: "POST", body: body as BodyInit, ...(signal === undefined ? {} : { signal }), headers: {
    accept: "application/json, text/event-stream", "content-type": "application/json",
    "mcp-protocol-version": MCP_PROTOCOL_VERSION, "mcp-method": "tools/call", "mcp-name": "web216_cpih_query", ...headers,
  } });
}
function proposal() {
  return { period: "2026-07", selection_plan_id: resolveWeb216CpihSelection({ period: "2026-07" }).plan_id, idempotency_key: KEY };
}
async function decoded(response: Response) {
  assert.equal(response.status, 200); assert.match(response.headers.get("content-type") ?? "", /^application\/json/u);
  const result = (await response.json() as Record<string, any>).result;
  assert.deepEqual(JSON.parse(result.content[0].text), result.structuredContent);
  assert(!JSON.stringify(result).includes(KEY)); return result;
}
class SqliteD1 implements Web216D1Database {
  readonly sqlite = new DatabaseSync(":memory:");
  beforeRead?: () => Promise<void>;
  afterUpdate?: () => Promise<void>;
  updates = 0;
  constructor() { this.sqlite.exec(WEB216_D1_SCHEMA_SQL); }
  prepare(sql: string): Web216D1Statement {
    const bound = (values: unknown[]): Web216D1Statement => ({
      bind: (...next) => bound(next),
      first: async <T>() => { await this.beforeRead?.(); return (this.sqlite.prepare(sql).get(...values as SQLInputValue[]) ?? null) as T | null; },
      run: async () => {
        const result = this.sqlite.prepare(sql).run(...values as SQLInputValue[]);
        if (sql === WEB216_D1_SQL.update) { this.updates += 1; await this.afterUpdate?.(); }
        return { success: true, meta: { changes: Number(result.changes) } };
      },
    });
    return bound([]);
  }
}
async function scenario(t: TestContext) {
  const database = new SqliteD1();
  const initialSnapshot = createWeb216TransactionalSnapshot({ projection: PROJECTION, software: SOFTWARE,
    createdAt: NOW().toISOString(), storeNonce: "1".repeat(32), maximumRecords: 32 });
  const store = createWeb216D1SnapshotStore({ database, initialSnapshot,
    material: { projection: PROJECTION, expectedSoftware: SOFTWARE, expectedStoreId: initialSnapshot.descriptor.store_id } });
  await store.initialiseIfAbsent();
  const application = createWeb216HostedCpihApplication({ store, projection: PROJECTION, software: SOFTWARE,
    expectedStoreId: initialSnapshot.descriptor.store_id, now: NOW });
  const handler = createWeb216HostedCpihMcpHttpHandler(application);
  t.after(async () => { await handler.close(); database.sqlite.close(); });
  return { database, handler, application, store };
}
function gate() {
  let entered!: () => void; let release!: () => void;
  const waiting = new Promise<void>((resolve) => { entered = resolve; });
  const blocked = new Promise<void>((resolve) => { release = resolve; });
  return { waiting, release, stop: async () => { entered(); await blocked; } };
}

test("wire grammar and parser retain exact original export identities", () => {
  for (const name of Object.keys(guards) as (keyof typeof guards)[]) assert.equal(originalGuards[name], guards[name]);
  assert.equal(OriginalJsonError, BoundedJsonError); assert.equal(originalParser, parseBoundedJsonBytes);
  assert.equal(originalBodyLimit, MCP_HTTP_MAX_STANDALONE_BODY_BYTES); assert.equal(originalBodyLimit, 65_536);
  for (const value of ["", "😀".repeat(128), 0, Number.MAX_SAFE_INTEGER]) assert.equal(guards.isBoundedMcpRequestId(value), true);
  for (const value of ["😀".repeat(129), "bad\u0000id", 0.5, null, Number.MAX_SAFE_INTEGER + 1, KEY]) assert.equal(guards.isBoundedMcpRequestId(value), false);
  for (const value of [KEY, encodeURIComponent(KEY), `%zz${encodeURIComponent(encodeURIComponent(KEY))}`]) {
    assert.equal(guards.containsRawIdempotencyKeyInMcpText(value), true);
    assert.equal(guards.containsRawIdempotencyKeyInMcpResourceUri(`gis-ai-go://evidence/${value}`), true);
  }
  assert.equal(guards.isBoundedMcpResourceUri(""), false);
  assert.equal(guards.isBoundedMcpResourceUri("a".repeat(2_048)), true);
  assert.equal(guards.isBoundedMcpResourceUri("a".repeat(2_049)), false);
});

test("extracted strict JSON preserves UTF-8, duplicate, scalar, numeric and depth bounds", () => {
  assert.deepEqual(parseBoundedJsonBytes(encoder.encode('{"a":"😀","b":[1,true,null]}'), 128), { a: "😀", b: [1, true, null] });
  for (const bytes of [encoder.encode('{"a":1,"\\u0061":2}'), Uint8Array.of(0xc3, 0x28),
    encoder.encode('"\\ud800"'), encoder.encode("1e400"), encoder.encode("[".repeat(18) + "0" + "]".repeat(18)),
    Uint8Array.of(0xef, 0xbb, 0xbf, 0x7b, 0x7d)]) {
    assert.throws(() => parseBoundedJsonBytes(bytes, 65_536), OriginalJsonError);
  }
  assert.throws(() => parseBoundedJsonBytes(encoder.encode("{}"), 1), (e: unknown) => e instanceof BoundedJsonError && e.failure === "too_large");
  for (const limit of [0, 1.5, 1_048_577]) assert.throws(() => parseBoundedJsonBytes(encoder.encode("{}"), limit), TypeError);
});

test("automatic and JSON-only cores reject the same hostile bytes and controls before SDK construction", async (t) => {
  let constructed = 0;
  const factory = () => { constructed += 1; return new McpServer({ name: "core-test", version: "1.0.0" }); };
  const handlers = [createBoundedMcpHttpHandler(factory, undefined), createBoundedJsonOnlyMcpHttpHandler(factory)];
  t.after(async () => { for (const h of handlers) await h.close(); });
  const sensitive = { ...message(), id: encodeURIComponent(KEY) };
  const missingVersion = request(); missingVersion.headers.delete("mcp-protocol-version");
  const resource = { ...message("resources/read"), params: { uri: `gis-ai-go://evidence/${KEY}` } };
  const vectors = [request("{}", { accept: "application/json, text/event-stream;q=0" }),
    request("{"), request('{"a":1,"a":2}'), request(Uint8Array.of(0xc3, 0x28)),
    request(" ".repeat(65_537)), request(JSON.stringify(sensitive)), missingVersion,
    request(JSON.stringify(message()), { "mcp-name": KEY }), request(JSON.stringify(resource))];
  for (const vector of vectors) {
    const outputs = [];
    for (const handler of handlers) {
      const response = await handler.fetch(vector.clone());
      outputs.push({ status: response.status, headers: Object.fromEntries(response.headers), body: await response.text() });
    }
    assert.deepEqual(outputs[0], outputs[1]); assert(outputs[0]!.status >= 400);
    assert(!outputs[0]!.body.includes(KEY));
  }
  assert.equal(constructed, 0);
});

test("hosted wrapper parses actual bytes even when a fabricated parsedBody is supplied", async (t) => {
  const s = await scenario(t);
  const fabricated = message();
  const refused = await s.handler.fetch(request("{"), { parsedBody: fabricated });
  assert.equal(refused.status, 400); assert.equal(s.database.updates, 0);
  const valid = await decoded(await s.handler.fetch(request(), { parsedBody: { ...fabricated, id: KEY } }));
  assert.notEqual(valid.isError, true); assert.equal(valid.structuredContent.result.observation.value, "142.7");
  assert.equal(s.database.updates, 1);
});

test("official client discovers and calls the JSON-only hosted face with closed results and replay", async (t) => {
  const s = await scenario(t); const contentTypes: string[] = [];
  const client = new Client({ name: "hosted-http-test", version: "1.0.0" }, { capabilities: {}, versionNegotiation: { mode: { pin: MCP_PROTOCOL_VERSION } } });
  t.after(() => client.close());
  await client.connect(new StreamableHTTPClientTransport(new URL(URL_BASE), { fetch: async (input, init) => {
    const response = await s.handler.fetch(new Request(input, init)); contentTypes.push(response.headers.get("content-type") ?? ""); return response;
  } }));
  assert.deepEqual((await client.listTools()).tools.map((x) => x.name).sort(), ["web216_cpih_inspect", "web216_cpih_query", "web216_cpih_select"]);
  const first = await client.callTool({ name: "web216_cpih_query", arguments: proposal() });
  assert.notEqual(first.isError, true);
  assert.deepEqual(await client.callTool({ name: "web216_cpih_query", arguments: proposal() }), first);
  assert(contentTypes.every((x) => x.startsWith("application/json"))); assert.equal(s.database.updates, 1);
  const invalid = await client.callTool({ name: "web216_cpih_query", arguments: { ...proposal(), policy: "allow" } });
  assert.equal(invalid.isError, true); assert.equal(s.database.updates, 1);
});

test("hosted HTTP rejects sensitive notification fields silently and rejects a legacy protocol", async (t) => {
  const s = await scenario(t);
  const { id: _id, ...notification } = message();
  const silent = await s.handler.fetch(request(JSON.stringify(notification), { "mcp-name": KEY }));
  assert.equal(silent.status, 202); assert.equal(await silent.text(), "");
  const legacy = await s.handler.fetch(request(JSON.stringify(message()), { "mcp-protocol-version": "2025-11-25" }));
  assert(legacy.status >= 400); assert.equal(s.database.updates, 0);
  assert.throws(() => createWeb216HostedCpihMcpHttpHandler({ ...s.application }), /genuine/u);
});

test("HTTP query cancellation after a stalled read returns its envelope and never issues a write", async (t) => {
  const s = await scenario(t); const waiting = gate(); const abort = new AbortController();
  s.database.beforeRead = waiting.stop;
  const pending = s.handler.fetch(request(undefined, {}, abort.signal));
  await waiting.waiting; abort.abort(); waiting.release();
  const result = await decoded(await pending);
  assert.equal(result.isError, true); assert.equal(result.structuredContent.code, "cancelled");
  assert.equal(s.database.updates, 0);
});

test("HTTP query cancellation after write issuance remains uncertain and same-key retry recovers once", async (t) => {
  const s = await scenario(t); const waiting = gate(); const abort = new AbortController();
  s.database.afterUpdate = waiting.stop;
  const pending = s.handler.fetch(request(undefined, {}, abort.signal));
  await waiting.waiting; abort.abort(); waiting.release();
  const uncertain = await decoded(await pending);
  assert.equal(uncertain.isError, true); assert.equal(uncertain.structuredContent.code, "uncertain-write");
  delete s.database.afterUpdate;
  const recovered = await decoded(await s.handler.fetch(request()));
  assert.equal(recovered.structuredContent.evidence.receipt.receipt_id, (await s.store.readSnapshot()).records[0]!.receipt.receipt_id);
  assert.equal(s.database.updates, 1);
});
