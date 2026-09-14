import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { DatabaseSync, type SQLInputValue } from "node:sqlite";
import test, { type TestContext } from "node:test";
import {
  createWeb216D1SnapshotStore, createWeb216TransactionalSnapshot,
  WEB216_D1_SCHEMA_SQL, WEB216_D1_SQL,
  type Web216D1Database, type Web216D1Statement, type Web216CpihPeriod,
} from "@gis-ai-go/evidence";
import {
  createWeb216HostedCpihApplication, isWeb216HostedCpihApplication,
  Web216HostedCpihApplicationError, type Web216HostedCpihApplicationErrorCode,
} from "../src/web216-hosted-cpih-application.js";
import { resolveWeb216CpihSelection } from "../src/web216-cpih-selection.js";

const PROJECTION: unknown = JSON.parse(readFileSync(new URL("../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url), "utf8"));
const SOFTWARE = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) } as const;
const NOW = () => new Date("2026-09-14T18:00:00.000Z");
const CONTEXT = { requestId: "server-authored-hosted-test", traceId: "d".repeat(32) };
const key = (i: number) => ["gis-ai-go", "ik", "v1", i.toString(16).padStart(64, "0")].join(":");
type Hooks = { beforeRead?: () => Promise<void>; beforeWrite?: (sql: string) => Promise<void>; afterWrite?: (sql: string) => Promise<void> };
class SqliteD1 implements Web216D1Database {
  readonly sqlite = new DatabaseSync(":memory:");
  readonly hooks: Hooks = {};
  readonly writes: string[] = [];
  constructor() { this.sqlite.exec(WEB216_D1_SCHEMA_SQL); }
  prepare(sql: string): Web216D1Statement {
    const statement = (values: unknown[]): Web216D1Statement => ({
      bind: (...next: unknown[]) => statement(next),
      first: async <T>() => { await this.hooks.beforeRead?.(); return (this.sqlite.prepare(sql).get(...values as SQLInputValue[]) ?? null) as T | null; },
      run: async () => {
        await this.hooks.beforeWrite?.(sql);
        this.writes.push(sql);
        const result = this.sqlite.prepare(sql).run(...values as SQLInputValue[]);
        await this.hooks.afterWrite?.(sql);
        return { success: true, meta: { changes: Number(result.changes) } };
      },
    });
    return statement([]);
  }
}
async function scenario(t: TestContext, maximumRecords = 32, provisioned = true) {
  const database = new SqliteD1(); t.after(() => database.sqlite.close());
  const initialSnapshot = createWeb216TransactionalSnapshot({ projection: PROJECTION, software: SOFTWARE,
    createdAt: NOW().toISOString(), storeNonce: "1".repeat(32), maximumRecords });
  const material = { projection: PROJECTION, expectedSoftware: SOFTWARE, expectedStoreId: initialSnapshot.descriptor.store_id };
  const store = createWeb216D1SnapshotStore({ database, initialSnapshot, material });
  if (provisioned) await store.initialiseIfAbsent();
  const options = { store, projection: PROJECTION, software: SOFTWARE, expectedStoreId: material.expectedStoreId, now: NOW };
  return { database, store, options, application: createWeb216HostedCpihApplication(options) };
}
function request(period: Web216CpihPeriod = "2026-07", idempotencyKey = key(1)) {
  return { period, selection_plan_id: resolveWeb216CpihSelection({ period }).plan_id, idempotency_key: idempotencyKey };
}
function errorCode(code: Web216HostedCpihApplicationErrorCode) {
  return (error: unknown) => error instanceof Web216HostedCpihApplicationError && error.code === code;
}
function gate() {
  let release!: () => void; let entered!: () => void;
  const blocked = new Promise<void>((resolve) => { release = resolve; });
  const waiting = new Promise<void>((resolve) => { entered = resolve; });
  return { release, waiting, stop: async () => { entered(); await blocked; } };
}

test("hosted construction/selection are non-mutating and distinct from an arbitrary copied application/store", async (t) => {
  const s = await scenario(t);
  assert.equal(isWeb216HostedCpihApplication(s.application), true);
  assert.equal(isWeb216HostedCpihApplication({ ...s.application }), false);
  assert.equal(Object.isFrozen(s.application), true);
  assert.deepEqual(await s.application.readiness(), { status: "ready", new_writes_available: true,
    inspection_available: true, record_count: 0, maximum_records: 32 });
  assert.equal((await s.application.resolve({ period: "2026-07" })).authority.grants_execution, false);
  assert.deepEqual(s.database.writes, [WEB216_D1_SQL.insert]);
  assert.throws(() => createWeb216HostedCpihApplication({ ...s.options, store: { ...s.store } }), errorCode("unavailable"));
});

test("January and July produce the exact captured values with honest database evidence, then inspect by either identity", async (t) => {
  const s = await scenario(t);
  for (const [period, value, id] of [["2026-01", "139.4", 1], ["2026-07", "142.7", 2]] as const) {
    const result = await s.application.query(request(period, key(id)), { ...CONTEXT, requestId: `server-${period}` });
    assert.equal(result.schema, "gis-ai-go.web216-hosted-cpih-result.v1");
    assert.equal(result.result.observation.value, value); assert.equal(typeof result.result.observation.value, "string");
    assert.equal(result.result.series.base_year, 2015);
    assert.equal(result.evidence.receipt.evidence.persistence, "not-persisted");
    assert.equal(result.evidence.record.boundary.persistence, "not-established-by-contract");
    assert.equal(result.evidence.storage_observation.persistence, "present-in-verified-adapter-snapshot");
    assert.equal(result.evidence.storage_observation.checkpoint_scope, "verified-returned-snapshot");
    assert.equal(result.evidence.storage_observation.read_freshness, "not-established-by-application");
    assert.equal(result.evidence.storage_observation.integrity, "full-snapshot-content-and-chain-verified-internally");
    assert.equal(result.evidence.storage_observation.returned_evidence_scope, "selected-record-event-and-head-subset");
    assert.equal(result.evidence.storage_observation.independent_rollback_anchor, false);
    assert.equal(result.evidence.event.record_id, result.evidence.record.record_id);
    assert.equal(result.evidence.checkpoint.tail_event_id, result.evidence.event.event_id);
    assert.equal(JSON.stringify(result).includes(key(id)), false);
    assert.equal(result.boundary.provider_egress, false);
    assert.deepEqual(await s.application.inspect({ receipt_id: result.evidence.receipt.receipt_id }), result);
    assert.deepEqual(await s.application.inspect({ idempotency_key: key(id) }), result);
  }
  assert.equal((await s.store.readSnapshot()).head.sequence, 2);
});

test("lost-response replay and application reopen retain original receipt and reject same-key changed period", async (t) => {
  const s = await scenario(t);
  const first = await s.application.query(request(), CONTEXT);
  const reopened = createWeb216HostedCpihApplication(s.options);
  assert.deepEqual(await reopened.query(request(), { ...CONTEXT, requestId: "server-retry" }), first);
  await assert.rejects(reopened.query(request("2026-01"), CONTEXT), errorCode("conflict"));
  assert.equal((await s.store.readSnapshot()).head.sequence, 1);
  assert.equal(s.database.writes.filter((sql) => sql === WEB216_D1_SQL.update).length, 1);
});

test("same-key retry recovers an actually committed but unacknowledged SQLite write without issuing another CAS", async (t) => {
  const s = await scenario(t);
  s.database.hooks.afterWrite = async (sql) => { if (sql === WEB216_D1_SQL.update) throw Error("synthetic lost acknowledgement"); };
  await assert.rejects(s.application.query(request(), CONTEXT), errorCode("uncertain-write"));
  delete s.database.hooks.afterWrite;
  const stored = await s.store.readSnapshot();
  const recovered = await s.application.query(request(), { ...CONTEXT, requestId: "server-after-timeout" });
  assert.deepEqual(recovered.evidence.receipt, stored.records[0]!.receipt);
  assert.equal(s.database.writes.filter((sql) => sql === WEB216_D1_SQL.update).length, 1);
});

test("competing same-key calls have one winner and one retryable conflict with no automatic CAS retry", async (t) => {
  const s = await scenario(t); const other = createWeb216HostedCpihApplication(s.options);
  let release!: () => void; const both = new Promise<void>((resolve) => { release = resolve; }); let count = 0;
  s.database.hooks.beforeWrite = async (sql) => { if (sql === WEB216_D1_SQL.update) { count += 1; if (count === 2) release(); await both; } };
  const outcomes = await Promise.allSettled([s.application.query(request(), CONTEXT), other.query(request(), { ...CONTEXT, requestId: "server-competing" })]);
  assert.equal(outcomes.filter((outcome) => outcome.status === "fulfilled").length, 1);
  const rejected = outcomes.find((outcome) => outcome.status === "rejected");
  assert.ok(rejected?.status === "rejected" && errorCode("retryable-conflict")(rejected.reason));
  assert.equal(count, 2); delete s.database.hooks.beforeWrite;
  const retry = await other.query(request(), { ...CONTEXT, requestId: "server-retry" });
  assert.equal((await s.store.readSnapshot()).head.sequence, 1);
  assert.equal(retry.evidence.record.record_id, (await s.store.readSnapshot()).records[0]!.record_id);
  assert.equal(count, 2);
});

test("a full subtractive store becomes read-only while replay and receipt inspection remain available", async (t) => {
  const s = await scenario(t, 1); const first = await s.application.query(request(), CONTEXT);
  assert.deepEqual(await s.application.readiness(), { status: "read-only", new_writes_available: false,
    inspection_available: true, record_count: 1, maximum_records: 1 });
  await assert.rejects(s.application.query(request("2026-01", key(2)), CONTEXT), errorCode("capacity"));
  assert.deepEqual(await s.application.query(request(), CONTEXT), first);
  assert.deepEqual(await s.application.inspect({ receipt_id: first.evidence.receipt.receipt_id }), first);
});

test("normal calls never initialise an absent row and corruption never supplies a success", async (t) => {
  const s = await scenario(t, 32, false);
  assert.equal((await s.application.readiness()).status, "unavailable");
  await assert.rejects(s.application.query(request(), CONTEXT), errorCode("unavailable"));
  await assert.rejects(s.application.inspect({ idempotency_key: key(1) }), errorCode("unavailable"));
  assert.deepEqual(s.database.writes, []);
  await s.store.initialiseIfAbsent(); await s.application.query(request(), CONTEXT);
  s.database.sqlite.exec("UPDATE web216_cpih_snapshot SET snapshot_json = '{}'");
  assert.equal((await s.application.readiness()).status, "unavailable");
  await assert.rejects(s.application.query(request(), CONTEXT), errorCode("unavailable"));
  await assert.rejects(s.application.inspect({ idempotency_key: key(1) }), errorCode("unavailable"));
});

test("aborting either the application read or the adapter internal read prevents all later writes", async (t) => {
  for (const stalledRead of [1, 2]) {
    const s = await scenario(t); const stop = gate(); const controller = new AbortController(); let reads = 0;
    s.database.hooks.beforeRead = async () => { reads += 1; if (reads === stalledRead) await stop.stop(); };
    const operation = s.application.query(request(), { ...CONTEXT, signal: controller.signal });
    await stop.waiting; controller.abort(); stop.release();
    await assert.rejects(operation, errorCode("cancelled"));
    delete s.database.hooks.beforeRead;
    assert.equal((await s.store.readSnapshot()).head.sequence, 0);
    assert.equal(s.database.writes.filter((sql) => sql === WEB216_D1_SQL.update).length, 0);
  }
});

test("aborting an issued write cannot claim absence; a fresh same-key request recovers it", async (t) => {
  const s = await scenario(t); const stop = gate(); const controller = new AbortController();
  s.database.hooks.afterWrite = async (sql) => { if (sql === WEB216_D1_SQL.update) await stop.stop(); };
  const operation = s.application.query(request(), { ...CONTEXT, signal: controller.signal });
  await stop.waiting; controller.abort(); stop.release();
  await assert.rejects(operation, errorCode("uncertain-write")); delete s.database.hooks.afterWrite;
  assert.equal((await s.application.query(request(), CONTEXT)).evidence.checkpoint.sequence, 1);
  assert.equal(s.database.writes.filter((sql) => sql === WEB216_D1_SQL.update).length, 1);
});

test("invalid queries, raw-key correlation, foreign material and unknown lookup fields fail closed", async (t) => {
  const s = await scenario(t);
  for (const input of [{ ...request(), period: "latest" }, { ...request(), selection_plan_id: "forged" },
    { ...request(), provider: "live" }, { ...request(), policy: "allow" }]) {
    await assert.rejects(s.application.query(input, CONTEXT), errorCode("invalid-input"));
  }
  await assert.rejects(s.application.query(request(), { ...CONTEXT, requestId: key(1) }), errorCode("invalid-input"));
  for (const input of [{ idempotency_key: key(1), receipt_id: "extra" }, { idempotency_key: "invalid" }, { path: "arbitrary" }]) {
    await assert.rejects(s.application.inspect(input), errorCode("invalid-input"));
  }
  await assert.rejects(s.application.inspect({ idempotency_key: key(1) }), errorCode("not-found"));
  assert.throws(() => createWeb216HostedCpihApplication({ ...s.options, projection: {} }), errorCode("unavailable"));
  const wrong = createWeb216HostedCpihApplication({ ...s.options, expectedStoreId: `gis-ai-go:web216-transactional-store:sha256:${"f".repeat(64)}` });
  assert.equal((await wrong.readiness()).status, "unavailable");
  await assert.rejects(wrong.query(request(), CONTEXT), errorCode("unavailable"));
  assert.equal((await s.store.readSnapshot()).head.sequence, 0);
});
