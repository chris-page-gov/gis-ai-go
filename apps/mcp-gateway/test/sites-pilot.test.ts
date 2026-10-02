import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { DatabaseSync, type SQLInputValue } from "node:sqlite";
import test, { type TestContext } from "node:test";
import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";
import { WebStandardStreamableHTTPServerTransport, type CallToolResult } from "@modelcontextprotocol/server";
import type { Web216D1Database, Web216D1Statement } from "@gis-ai-go/evidence/web216-pure";
import { createSitesPilotHttpHandler, SITES_PILOT_INPUTS, type SitesPilotOptions } from "../src/sites-pilot-http.js";
import { createSitesPilotStore, makePilotResult, pilotHash, SITES_PILOT_SQL, SitesPilotStoreError,
  verifyPilotResult, type PilotProvider, type PilotResult } from "../src/sites-pilot-store.js";

const ORIGIN = "https://pilot.example.invalid";
const ENDPOINT = `${ORIGIN}/pilot/mcp`;
const REVISION = "a".repeat(40);
const NOW = Date.parse("2026-10-01T12:00:00.000Z");
const TEST_TOKEN = "synthetic-private-test-token-".repeat(3);
const TEST_TOKEN_HASH = createHash("sha256").update(TEST_TOKEN).digest("hex");
const OS_KEY = "synthetic-os-key-not-a-real-credential";
const PROJECTION = JSON.parse(readFileSync(new URL("../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url), "utf8")) as { search: unknown; data: unknown };
const copy = <T>(value: T): T => JSON.parse(JSON.stringify(value)) as T;
const json = (value: unknown) => Response.json(value);

/** Executes the actual D1 SQL against SQLite, rather than mocking its outcomes. */
class SqliteD1 implements Web216D1Database {
  readonly sqlite: DatabaseSync;
  constructor(path = ":memory:") {
    this.sqlite = new DatabaseSync(path);
    for (const sql of SITES_PILOT_SQL.schema) this.sqlite.exec(sql);
  }
  prepare(sql: string): Web216D1Statement {
    const statement = (values: unknown[]): Web216D1Statement => ({
      bind: (...next) => statement(next),
      first: async <T>() => {
        await Promise.resolve();
        return (this.sqlite.prepare(sql).get(...values as SQLInputValue[]) ?? null) as T | null;
      },
      run: async () => {
        const result = this.sqlite.prepare(sql).run(...values as SQLInputValue[]);
        return { success: true, meta: { changes: Number(result.changes) } };
      },
    });
    return statement([]);
  }
  seed(provider: PilotProvider, maximum = 200, enabled = 1) {
    this.sqlite.prepare("INSERT INTO sites_pilot_allowance_v1 VALUES (?, ?, 0, ?, 0, 0)").run(provider, enabled, maximum);
  }
  used(provider: PilotProvider): number {
    return (this.sqlite.prepare("SELECT used FROM sites_pilot_allowance_v1 WHERE provider = ?").get(provider) as { used: number }).used;
  }
  receipts(): number {
    return (this.sqlite.prepare("SELECT COUNT(*) AS count FROM sites_pilot_receipts_v1").get() as { count: number }).count;
  }
}
function database(t: TestContext) {
  const db = new SqliteD1(); t.after(() => db.sqlite.close()); return db;
}
async function rejectsCode(action: Promise<unknown>, code: SitesPilotStoreError["code"]) {
  await assert.rejects(action, (error: unknown) => error instanceof SitesPilotStoreError && error.code === code);
}
function receipt(index = 0): PilotResult {
  return makePilotResult("sites_os_names", { query: "Warwick", index }, { place: "Warwick", index }, REVISION,
    new Date(NOW + index), true);
}
function names() {
  return { header: { query: "Warwick", format: "JSON", maxresults: 5, offset: 0, totalresults: 1 },
    results: [{ GAZETTEER_ENTRY: { ID: "osgb4000000074555874", NAMES_URI: "http://data.ordnancesurvey.co.uk/id/4000000074555874",
      NAME1: "Warwick", TYPE: "populatedPlace", LOCAL_TYPE: "Town", GEOMETRY_X: 428119, GEOMETRY_Y: 265114,
      COUNTRY: "England", COUNTY_UNITARY: "Warwickshire" } }] };
}
function product() {
  return { id: "OpenNames", name: "OS Open Names", version: "2026-07", areas: ["GB"], formats: [{ format: "CSV" }],
    url: "https://api.os.uk/downloads/v1/products/OpenNames", downloadsUrl: "https://api.os.uk/downloads/v1/products/OpenNames/downloads" };
}
function areas() {
  return { fields: [{ name: "MSOA21CD", type: "esriFieldTypeString" }, { name: "MSOA21NM", type: "esriFieldTypeString" }],
    exceededTransferLimit: true, features: [{ attributes: { MSOA21CD: "E02006519", MSOA21NM: "Warwick 001" } }] };
}
function scenario(t: TestContext, changes: Partial<SitesPilotOptions> = {}, enableTestToken = true) {
  const db = database(t);
  for (const provider of ["os-names", "os-open-data", "ons-cpih", "ons-geography"] as const) db.seed(provider);
  const outgoing: { url: string; headers: Headers }[] = [];
  const fetcher: typeof fetch = async (input, init) => {
    const url = String(input); outgoing.push({ url, headers: new Headers(init?.headers) });
    if (url.startsWith("https://api.os.uk/search/names/v1/find?")) return json(names());
    if (url === product().url) return json(product());
    if (url.startsWith("https://api.beta.ons.gov.uk/v1/search?")) return json(PROJECTION.search);
    if (url.startsWith("https://api.beta.ons.gov.uk/v1/data?")) return json(PROJECTION.data);
    if (new URL(url).hostname === "services1.arcgis.com" && new URL(url).pathname.endsWith("/query")) return json(areas());
    throw new Error("Unexpected provider destination");
  };
  const store = createSitesPilotStore(db);
  const handler = createSitesPilotHttpHandler({ origin: ORIGIN, path: "/pilot/mcp", softwareRevision: REVISION,
    store, fetch: fetcher, osApiKey: OS_KEY, ...(enableTestToken ? { testTokenSha256: TEST_TOKEN_HASH } : {}), now: () => NOW, ...changes });
  t.after(() => handler.close());
  return { db, outgoing, store, handler };
}
async function connect(t: TestContext, s: ReturnType<typeof scenario>, protocol: "2025-11-25" | "2026-07-28") {
  const client = new Client({ name: "sites-pilot-offline-test", version: "1.0.0" }, {
    capabilities: {}, versionNegotiation: { mode: protocol === "2025-11-25" ? "legacy" : { pin: protocol } },
  });
  const wire: { method: string | null; protocol: string | null }[] = [];
  const localFetch: typeof fetch = async (input, init) => {
    const request = new Request(input, init);
    request.headers.set("x-sites-pilot-test-token", TEST_TOKEN);
    wire.push({ method: request.headers.get("mcp-method"), protocol: request.headers.get("mcp-protocol-version") });
    return s.handler.fetch(request);
  };
  t.after(() => client.close());
  await client.connect(new StreamableHTTPClientTransport(new URL(ENDPOINT), { fetch: localFetch }));
  assert.equal(client.getNegotiatedProtocolVersion(), protocol);
  return { client, wire };
}
function resultBody(result: CallToolResult): Record<string, any> {
  assert.equal(result.content.length, 1);
  const block = result.content[0]; assert.equal(block?.type, "text");
  if (block?.type !== "text") throw new Error("Missing text result");
  assert.deepEqual(JSON.parse(block.text), result.structuredContent);
  assert.equal(block.text.includes(OS_KEY), false); assert.equal(block.text.includes(TEST_TOKEN), false);
  return result.structuredContent as Record<string, any>;
}
function request(body: string | object = { jsonrpc: "2.0", id: 1, method: "tools/list", params: {} },
  change: { url?: string; method?: string; headers?: Record<string, string>; remove?: string[]; signal?: AbortSignal } = {}) {
  const headers = new Headers({ "content-type": "application/json", accept: "application/json, text/event-stream",
    "mcp-protocol-version": "2025-11-25", "x-sites-pilot-test-token": TEST_TOKEN, ...change.headers });
  for (const key of change.remove ?? []) headers.delete(key);
  return new Request(change.url ?? ENDPOINT, { method: change.method ?? "POST", headers,
    ...(["GET", "HEAD"].includes(change.method ?? "POST") ? {} : { body: typeof body === "string" ? body : JSON.stringify(body) }),
    ...(change.signal ? { signal: change.signal } : {}) });
}

test("one durable allowance is enforced across independent SQLite connections and store instances", async (t) => {
  const directory = mkdtempSync(join(tmpdir(), "gis-sites-pilot-test-"));
  const first = new SqliteD1(join(directory, "pilot.sqlite")), second = new SqliteD1(join(directory, "pilot.sqlite"));
  t.after(() => { first.sqlite.close(); second.sqlite.close(); rmSync(directory, { recursive: true, force: true }); });
  first.seed("os-names", 7);
  const stores = [createSitesPilotStore(first), createSitesPilotStore(second)];
  const outcomes = await Promise.allSettled(Array.from({ length: 30 }, (_, index) => stores[index % 2]!.admit("os-names", NOW)));
  assert.equal(outcomes.filter((value) => value.status === "fulfilled").length, 7);
  assert.equal(first.used("os-names"), 7); assert.equal(second.used("os-names"), 7);
  await rejectsCode(stores[0]!.admit("os-names", NOW + 60_000), "allowance-denied");
});

test("minute limit resets at its boundary without resetting lifetime usage", async (t) => {
  const db = database(t); db.seed("ons-cpih", 25); const store = createSitesPilotStore(db);
  const outcomes = await Promise.allSettled(Array.from({ length: 35 }, () => store.admit("ons-cpih", NOW)));
  assert.equal(outcomes.filter((value) => value.status === "fulfilled").length, 20);
  await rejectsCode(store.admit("ons-cpih", NOW + 59_999), "allowance-denied");
  for (let index = 0; index < 5; index++) await store.admit("ons-cpih", NOW + 60_000);
  assert.equal(db.used("ons-cpih"), 25);
  await rejectsCode(store.admit("ons-cpih", NOW + 120_000), "allowance-denied");
});

test("missing, disabled and unavailable allowance fail closed", async (t) => {
  const db = database(t), store = createSitesPilotStore(db);
  await rejectsCode(store.admit("os-names", NOW), "allowance-denied");
  db.seed("os-names", 10, 0);
  await rejectsCode(store.admit("os-names", NOW), "allowance-denied");
  assert.equal(db.used("os-names"), 0);
  db.sqlite.exec("DROP TABLE sites_pilot_allowance_v1");
  await rejectsCode(store.admit("os-names", NOW), "store-unavailable");
});

test("allowance refuses invalid provider and clock before executing SQL", async (t) => {
  const store = createSitesPilotStore(database(t));
  for (const now of [-1, NaN, Infinity, 1.5]) await assert.rejects(store.admit("os-names", now), TypeError);
  await assert.rejects(store.admit("other" as PilotProvider, NOW), TypeError);
});

test("SQLite receipt capacity is atomic across overlapping appends and preserves existing records", async (t) => {
  const db = database(t), store = createSitesPilotStore(db);
  db.sqlite.exec("CREATE TABLE web216_cpih_snapshot (marker TEXT); INSERT INTO web216_cpih_snapshot VALUES ('legacy-unchanged')");
  const outcomes = await Promise.allSettled(Array.from({ length: 140 }, (_, index) => store.append(receipt(index))));
  assert.equal(outcomes.filter((value) => value.status === "fulfilled").length, 128); assert.equal(db.receipts(), 128);
  assert.deepEqual(await store.inspect(receipt().evidence.receipt_id), receipt());
  await rejectsCode(store.append(receipt(150)), "store-full");
  db.seed("os-names");
  await rejectsCode(store.admit("os-names", NOW), "allowance-denied");
  assert.equal(db.used("os-names"), 0);
  assert.equal((db.sqlite.prepare("SELECT marker FROM web216_cpih_snapshot").get() as { marker: string }).marker, "legacy-unchanged");
});

test("receipt inspection survives reopening SQLite and binds the requested identifier", async (t) => {
  const directory = mkdtempSync(join(tmpdir(), "gis-sites-pilot-restart-")), path = join(directory, "pilot.sqlite");
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  const first = new SqliteD1(path), value = receipt(); await createSitesPilotStore(first).append(value); first.sqlite.close();
  const second = new SqliteD1(path); t.after(() => second.sqlite.close());
  assert.deepEqual(await createSitesPilotStore(second).inspect(value.evidence.receipt_id), value);
  second.sqlite.prepare("UPDATE sites_pilot_receipts_v1 SET receipt_id = ?").run(receipt(1).evidence.receipt_id);
  await rejectsCode(createSitesPilotStore(second).inspect(receipt(1).evidence.receipt_id), "corrupt-evidence");
});

test("receipt verification detects data, evidence and unhashed envelope tampering", async (t) => {
  const mutations: ((value: PilotResult) => void)[] = [
    (value) => { value.data.place = "Tampered"; },
    (value) => { value.evidence.provider_egress = false; },
    (value) => { value.tool = "sites_other"; },
    (value) => { (value as unknown as Record<string, unknown>).authorised = true; },
    (value) => { (value.evidence as unknown as Record<string, unknown>).extra = "unreviewed"; },
  ];
  for (const mutate of mutations) {
    const db = database(t), store = createSitesPilotStore(db), original = receipt(), changed = copy(original);
    await store.append(original); mutate(changed);
    assert.equal(verifyPilotResult(changed), false);
    db.sqlite.prepare("UPDATE sites_pilot_receipts_v1 SET result_json = ?").run(JSON.stringify(changed));
    await rejectsCode(store.inspect(original.evidence.receipt_id), "corrupt-evidence");
  }
});

test("result and receipt bounds reject excessive material and invalid identities", () => {
  assert.throws(() => makePilotResult("sites_os_names", {}, { text: "x".repeat(65_536) }, REVISION, new Date(NOW), true), RangeError);
  assert.throws(() => makePilotResult("data.query", {}, {}, REVISION, new Date(NOW), true), TypeError);
  assert.throws(() => makePilotResult("sites_os_names", {}, {}, "not-a-revision", new Date(NOW), true), TypeError);
  assert.equal(verifyPilotResult(null), false); assert.equal(verifyPilotResult({}), false);
  assert.equal(pilotHash({ b: 2, a: 1 }), pilotHash({ a: 1, b: 2 }));
});

for (const protocol of ["2025-11-25", "2026-07-28"] as const) {
  test(`${protocol} SDK wire discovery and capabilities retain the separate experimental profile`, async (t) => {
    const s = scenario(t), { client } = await connect(t, s, protocol);
    const tools = (await client.listTools()).tools;
    assert.deepEqual(tools.map((tool) => tool.name).sort(), Object.keys(SITES_PILOT_INPUTS).sort());
    for (const tool of tools) {
      assert.deepEqual(tool.inputSchema, SITES_PILOT_INPUTS[tool.name as keyof typeof SITES_PILOT_INPUTS]);
      const readsOnly = ["sites_capabilities", "sites_evidence_inspect"].includes(tool.name);
      assert.equal(tool.annotations?.readOnlyHint, readsOnly); assert.equal(tool.annotations?.idempotentHint, readsOnly);
    }
    const body = resultBody(await client.callTool({ name: "sites_capabilities", arguments: {} }));
    assert.equal(body.data.supported_release, false); assert.equal(body.data.providers.psga, "disabled-rights-not-established");
    assert.equal(body.evidence.provider_egress, false); assert.equal(s.outgoing.length, 0); assert.equal(s.db.receipts(), 0);
  });

  test(`${protocol} SDK OS and ONS calls produce inspectable durable source-native evidence`, async (t) => {
    const s = scenario(t), { client } = await connect(t, s, protocol);
    const namesResult = resultBody(await client.callTool({ name: "sites_os_names", arguments: { query: "Warwick" } }));
    assert.equal(namesResult.data.data.candidates[0].GEOMETRY_X, 428119);
    assert.equal(s.db.used("os-names"), 1); assert.equal(s.outgoing[0]?.headers.get("key"), OS_KEY);
    const inspected = resultBody(await client.callTool({ name: "sites_evidence_inspect", arguments: { receipt_id: namesResult.evidence.receipt_id } }));
    assert.deepEqual(inspected, namesResult); assert.equal(s.outgoing.length, 1);
    const cpih = resultBody(await client.callTool({ name: "sites_ons_cpih", arguments: { periods: ["2026-01", "2026-07"] } }));
    assert.equal(cpih.data.data.comparison.difference_index_points, "3.3");
    assert.equal(cpih.data.data.measure_kind, "index-not-inflation-percentage");
    assert.equal(s.db.used("ons-cpih"), 2); assert.equal(s.db.receipts(), 2);
    assert.ok(s.outgoing.slice(1).every((value) => value.headers.get("key") === null));
    const geography = resultBody(await client.callTool({ name: "sites_ons_areas", arguments: { name_prefix: "Warwick" } }));
    assert.deepEqual(geography.data.data.areas, [{ MSOA21CD: "E02006519", MSOA21NM: "Warwick 001" }]);
    assert.equal(geography.data.data.complete, false);
    assert.equal(geography.data.data.selection_basis, "name-prefix-not-spatial-containment");
    assert.equal(s.db.used("ons-geography"), 1); assert.equal(s.db.receipts(), 3);
  });

  test(`${protocol} unknown input, unavailable tool and excessive bounds cause no provider call`, async (t) => {
    const s = scenario(t), { client } = await connect(t, s, protocol);
    for (const [name, args] of [
      ["sites_os_names", { query: "Warwick", url: "https://untrusted.invalid" }],
      ["sites_os_names", { query: "Warwick", max_results: 6 }],
      ["sites_ons_cpih", { periods: ["2026-01", "2026-01"] }],
      ["sites_ons_cpih", { periods: ["2026-13"] }],
      ["sites_os_open_product", { product: "Premium" }],
      ["sites_ons_areas", { name_prefix: "Warwick", where: "1=1" }],
      ["sites_capabilities", { unexpected: true }],
      ["data.query", {}],
    ] as [string, Record<string, unknown>][]) {
      let rejected = false;
      try { rejected = (await client.callTool({ name, arguments: args })).isError === true; } catch { rejected = true; }
      assert.equal(rejected, true, `must reject ${name} ${JSON.stringify(args)}`);
    }
    assert.equal(s.outgoing.length, 0); assert.equal(s.db.receipts(), 0);
    assert.equal(s.db.used("os-names"), 0); assert.equal(s.db.used("ons-cpih"), 0);
  });
}

test("a provider error consumes its admission without retry, refund, secret leakage or successful receipt", async (t) => {
  let attempts = 0;
  const s = scenario(t, { fetch: async () => { attempts++; throw new Error(`do not expose ${OS_KEY}`); } });
  const { client } = await connect(t, s, "2026-07-28");
  const result = await client.callTool({ name: "sites_os_names", arguments: { query: "Warwick" } });
  assert.equal(result.isError, true); const body = resultBody(result);
  assert.equal(body.code, "upstream-unavailable"); assert.equal(body.provider_attempt_refund, false);
  assert.equal(attempts, 1); assert.equal(s.db.used("os-names"), 1); assert.equal(s.db.receipts(), 0);
});

test("receipt storage failure prevents data success after a completed provider call", async (t) => {
  const s = scenario(t), { client } = await connect(t, s, "2026-07-28");
  s.db.sqlite.exec("CREATE TRIGGER fail_pilot_write BEFORE INSERT ON sites_pilot_receipts_v1 BEGIN SELECT RAISE(ABORT, 'synthetic-write-failure'); END");
  const result = await client.callTool({ name: "sites_os_open_product", arguments: { product: "OpenNames" } });
  assert.equal(result.isError, true); assert.equal(resultBody(result).code, "store-unavailable");
  assert.equal(s.outgoing.length, 1); assert.equal(s.db.used("os-open-data"), 1);
});

test("cancelled provider execution consumes its attempt and cannot produce a successful receipt", { timeout: 2000 }, async (t) => {
  let entered!: () => void;
  const started = new Promise<void>((resolve) => { entered = resolve; });
  const s = scenario(t, { fetch: async (_input, init) => new Promise<Response>((_resolve, reject) => {
    entered();
    init!.signal!.addEventListener("abort", () => reject(new Error("synthetic-cancel")), { once: true });
  }) });
  const cancellation = new AbortController();
  const pending = s.handler.fetch(request({ jsonrpc: "2.0", id: 1, method: "tools/call",
    params: { name: "sites_os_names", arguments: { query: "Warwick" } } }, { signal: cancellation.signal }));
  await started; cancellation.abort();
  assert.equal((await pending).status, 408);
  assert.equal(s.db.used("os-names"), 1); assert.equal(s.db.receipts(), 0);
});

test("denied provider allowance prevents egress and does not fabricate an open-data fallback", async (t) => {
  const s = scenario(t), { client } = await connect(t, s, "2026-07-28");
  s.db.sqlite.exec("UPDATE sites_pilot_allowance_v1 SET enabled = 0");
  const result = await client.callTool({ name: "sites_os_names", arguments: { query: "Warwick" } });
  assert.equal(result.isError, true); assert.equal(resultBody(result).code, "admission-denied");
  assert.equal(s.outgoing.length, 0); assert.equal(s.db.receipts(), 0);
});

test("private test authentication is explicit, bounded and absent by default", async (t) => {
  const s = scenario(t);
  for (const token of [undefined, "wrong-token".repeat(5), "x".repeat(4097), "short"]) {
    const response = await s.handler.fetch(request(undefined, token === undefined ? { remove: ["x-sites-pilot-test-token"] }
      : { headers: { "x-sites-pilot-test-token": token } }));
    assert.equal(response.status, 401);
  }
  const disabled = scenario(t, {}, false);
  assert.equal((await disabled.handler.fetch(request())).status, 401);
  // Synthetic trusted-ingress fixture only: this does not verify the Sites dispatcher strips forged identity.
  const signedIn = await disabled.handler.fetch(request(undefined, { remove: ["x-sites-pilot-test-token"], headers: { "oai-authenticated-user-id": "synthetic-owner" } }));
  assert.equal(signedIn.status, 200);
  assert.equal(s.outgoing.length, 0);
});

test("HTTP authority, same-origin, route, method and content type guards reject before MCP execution", async (t) => {
  const s = scenario(t);
  const cases: [Parameters<typeof request>[1], number][] = [
    [{ headers: { host: "untrusted.invalid" } }, 403],
    [{ headers: { origin: "https://untrusted.invalid" } }, 403],
    [{ headers: { "sec-fetch-site": "cross-site" } }, 403],
    [{ headers: { "sec-fetch-site": "same-site" } }, 403],
    [{ url: `${ENDPOINT}?extra=true` }, 404],
    [{ url: `${ORIGIN}/wrong` }, 404],
    [{ method: "GET" }, 405],
    [{ headers: { "content-type": "text/plain" } }, 415],
  ];
  for (const [change, status] of cases) assert.equal((await s.handler.fetch(request(undefined, change))).status, status);
  assert.equal(s.outgoing.length, 0); assert.equal(s.db.receipts(), 0);
});

test("caller Accept and protocol are validated without quietly repairing malformed clients", async (t) => {
  const s = scenario(t);
  for (const change of [{ remove: ["accept"] }, { headers: { accept: "text/plain" } },
    { headers: { accept: "application/json;q=0, text/event-stream" } },
    { headers: { accept: "application/json, text/event-stream;q=0" } },
    { headers: { accept: "x-application/json, x-text/event-stream" } },
    { headers: { "mcp-protocol-version": "1900-01-01" } }]) {
    const response = await s.handler.fetch(request(undefined, change));
    assert.ok(response.status >= 400, `expected rejection, got ${response.status}`);
  }
  assert.equal(s.outgoing.length, 0);
});

test("finite-method admission rejects method-header substitution before dispatch", async (t) => {
  const s = scenario(t);
  assert.equal((await s.handler.fetch(request(undefined, { headers: { "mcp-method": "subscriptions/listen" } }))).status, 400);
  assert.equal(s.outgoing.length, 0); assert.equal(s.db.receipts(), 0);
});

test("an unexpected SDK SSE response is independently refused and cancelled", async (t) => {
  let cancelled = false;
  t.mock.method(WebStandardStreamableHTTPServerTransport.prototype, "handleRequest", async () => new Response(
    new ReadableStream<Uint8Array>({ cancel() { cancelled = true; } }), { headers: { "content-type": "text/event-stream" } }));
  const s = scenario(t), response = await s.handler.fetch(request());
  assert.equal(response.status, 400); assert.deepEqual(await response.json(), { error: "streaming-not-supported" });
  assert.equal(cancelled, true); assert.equal(s.outgoing.length, 0);
});

test("strict wire parsing rejects duplicate keys, malformed JSON and excessive request bytes", async (t) => {
  const s = scenario(t);
  for (const body of ["{", '{"jsonrpc":"2.0","id":1,"id":2,"method":"tools/list"}',
    JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/list", padding: "x".repeat(16_384) })]) {
    assert.equal((await s.handler.fetch(request(body))).status, 400);
  }
  assert.equal(s.outgoing.length, 0); assert.equal(s.db.receipts(), 0);
});

test("two unfinished request bodies consume capacity until cancellation settles", async (t) => {
  const s = scenario(t);
  const first = new AbortController(), second = new AbortController();
  const held = (controller: AbortController) => new Request(ENDPOINT, {
    method: "POST", headers: request().headers, signal: controller.signal,
    body: new ReadableStream<Uint8Array>({ start(stream) { stream.enqueue(new TextEncoder().encode("{")); } }),
    duplex: "half",
  } as RequestInit);
  const pending = [s.handler.fetch(held(first)), s.handler.fetch(held(second))];
  const blocked = await s.handler.fetch(request()); assert.equal(blocked.status, 429);
  first.abort(); second.abort();
  const completed = await Promise.all(pending); assert.ok(completed.every((response) => response.status === 408));
  assert.equal((await s.handler.fetch(request())).status, 200);
  assert.equal(s.outgoing.length, 0);
});

function deferred() {
  let release!: () => void;
  const promise = new Promise<void>((resolve) => { release = resolve; });
  return { promise, release };
}
function wireCall(protocol: "2025-11-25" | "2026-07-28", tool: string, args: Record<string, unknown>, signal?: AbortSignal) {
  return request({ jsonrpc: "2.0", id: 1, method: "tools/call", params: {
    name: tool, arguments: args,
    ...(protocol === "2026-07-28" ? { _meta: {
      "io.modelcontextprotocol/protocolVersion": protocol,
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": { name: "synthetic-capacity-test", version: "1.0.0" },
    } } : {}),
  } }, { headers: { "mcp-protocol-version": protocol, "mcp-method": "tools/call", "mcp-name": tool },
    ...(signal ? { signal } : {}) });
}

for (const protocol of ["2025-11-25", "2026-07-28"] as const) {
  for (const stage of ["admit", "append", "inspect"] as const) {
    test(`${protocol} cancelled ${stage} retains capacity until the underlying operation settles`, { timeout: 3000 }, async (t) => {
      const held = [deferred(), deferred()], entered = [deferred(), deferred()];
      let calls = 0;
      const backgrounds: Promise<void>[] = [];
      const hold = async () => {
        const index = calls++; entered[index]!.release(); await held[index]!.promise;
      };
      const s = scenario(t, {
        store: {
          admit: async () => { if (stage === "admit") await hold(); },
          append: async () => { if (stage === "append") await hold(); },
          inspect: async () => { if (stage === "inspect") await hold(); return receipt(); },
        },
        waitUntil: (completion: Promise<void>) => { backgrounds.push(completion); },
      } as Partial<SitesPilotOptions>);
      const tool = stage === "inspect" ? "sites_evidence_inspect" : "sites_os_open_product";
      const args = stage === "inspect" ? { receipt_id: receipt().evidence.receipt_id } : { product: "OpenNames" };
      try {
        for (let index = 0; index < 2; index++) {
          const controller = new AbortController();
          const pending = s.handler.fetch(wireCall(protocol, tool, args, controller.signal));
          await entered[index]!.promise; controller.abort();
          assert.equal((await pending).status, 408);
        }
        assert.equal(calls, 2);
        assert.equal((await s.handler.fetch(request())).status, 429);
        assert.equal(calls, 2);
        assert.equal(s.outgoing.length, stage === "append" ? 2 : 0);
      } finally {
        for (const item of held) item.release();
        await Promise.all(backgrounds);
        // Flush completed application callbacks even on the pre-fix failure path.
        await new Promise<void>((resolve) => setImmediate(resolve));
      }
      assert.equal((await s.handler.fetch(request())).status, 200);
      assert.ok(backgrounds.length >= 2, "background application settlement must be registered with the host");
    });
  }

  test(`${protocol} subscription streaming is rejected before SDK dispatch`, { timeout: 2000 }, async (t) => {
    const s = scenario(t), controller = new AbortController();
    const deadline = setTimeout(() => controller.abort(), 100);
    const params = protocol === "2026-07-28" ? { _meta: {
      "io.modelcontextprotocol/protocolVersion": protocol,
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": { name: "synthetic-subscription-test", version: "1.0.0" },
    } } : {};
    try {
      const response = await s.handler.fetch(request({ jsonrpc: "2.0", id: 1, method: "subscriptions/listen", params }, {
        headers: { "mcp-protocol-version": protocol, "mcp-method": "subscriptions/listen" }, signal: controller.signal,
      }));
      assert.equal(response.status, 400); assert.equal(controller.signal.aborted, false);
      assert.equal(s.outgoing.length, 0); assert.equal(s.db.receipts(), 0);
    } finally { clearTimeout(deadline); controller.abort(); }
  });
}
