import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { performance } from "node:perf_hooks";
import { DatabaseSync, type SQLInputValue } from "node:sqlite";
import test, { type TestContext } from "node:test";
import { canonicalJson } from "../src/canonical-json.js";
import { buildWeb216CpihReceipt } from "../src/web216-cpih-receipt.js";
import {
  applyWeb216TransactionalPlanModel, createWeb216TransactionalSnapshot,
  lookupWeb216TransactionalRecord, planWeb216TransactionalAppend,
  type Web216TransactionalAppendPlan, type Web216TransactionalSnapshot,
} from "../src/web216-transactional-contract.js";
import {
  createWeb216D1SnapshotStore, isWeb216D1SnapshotStore, Web216D1SnapshotError,
  WEB216_D1_MAX_SNAPSHOT_BYTES, WEB216_D1_SQL, WEB216_D1_SCHEMA_SQL,
  type Web216D1Database, type Web216D1Statement,
} from "../src/web216-transactional-d1.js";

const PROJECTION: unknown = JSON.parse(readFileSync(new URL(
  "../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url,
), "utf8"));
const SOFTWARE = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) } as const;
const TIME = "2026-09-14T18:00:00.000Z";
const key = (i: number) => ["gis-ai-go", "ik", "v1", i.toString(16).padStart(64, "0")].join(":");
type Hooks = { beforeFirst?: (sql: string) => Promise<void>; beforeRun?: (sql: string) => Promise<void>; afterRun?: (sql: string) => Promise<void> };

/** Executes the exact adapter SQL in actual SQLite; hooks inject transport failures. */
class SqliteD1 implements Web216D1Database {
  readonly sqlite: DatabaseSync;
  readonly hooks: Hooks = {};
  constructor(readonly path: string = ":memory:", migrated = true) {
    this.sqlite = new DatabaseSync(path);
    // Test setup owns schema creation; the adapter must never execute DDL.
    if (migrated) this.sqlite.exec(WEB216_D1_SCHEMA_SQL);
  }
  prepare(sql: string): Web216D1Statement {
    const make = (values: unknown[]): Web216D1Statement => ({
      bind: (...next: unknown[]) => make(next),
      first: async <T>() => {
        await this.hooks.beforeFirst?.(sql);
        return (this.sqlite.prepare(sql).get(...values as SQLInputValue[]) ?? null) as T | null;
      },
      run: async () => {
        await this.hooks.beforeRun?.(sql);
        const result = this.sqlite.prepare(sql).run(...values as SQLInputValue[]);
        await this.hooks.afterRun?.(sql);
        return { success: true, meta: { changes: Number(result.changes) } };
      },
    });
    return make([]);
  }
  close() { this.sqlite.close(); }
}
function inputs(maximumRecords = 128) {
  const initialSnapshot = createWeb216TransactionalSnapshot({ projection: PROJECTION, software: SOFTWARE,
    createdAt: TIME, storeNonce: "1".repeat(32), maximumRecords });
  return { initialSnapshot, material: { projection: PROJECTION, expectedSoftware: SOFTWARE,
    expectedStoreId: initialSnapshot.descriptor.store_id } };
}
function fixture(t: TestContext, maximumRecords = 128) {
  const database = new SqliteD1(); t.after(() => database.close());
  const options = inputs(maximumRecords);
  return { database, ...options, store: createWeb216D1SnapshotStore({ database, ...options }) };
}
function plan(state: Web216TransactionalSnapshot, i: number, options = inputs()): Web216TransactionalAppendPlan {
  const result = planWeb216TransactionalAppend(state, { idempotencyKey: key(i), recordedAt: TIME,
    receipt: buildWeb216CpihReceipt({ projection: PROJECTION, software: SOFTWARE, createdAt: TIME,
      period: i % 2 === 0 ? "2026-01" : "2026-07", traceId: "d".repeat(32), requestId: `d1-test-${i}` }),
  }, options.material);
  assert.equal(result.status, "append-plan-not-committed");
  if (result.status !== "append-plan-not-committed") throw Error("Expected plan");
  return result.plan;
}
function errorCode(code: Web216D1SnapshotError["code"]) {
  return (error: unknown) => error instanceof Web216D1SnapshotError && error.code === code;
}

test("real SQLite initialisation, CAS publication and independent reopen preserve complete evidence", async (t) => {
  const directory = mkdtempSync(join(tmpdir(), "web216-d1-restart-"));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  const path = join(directory, "capture.sqlite"); const options = inputs();
  let database = new SqliteD1(path);
  try {
    const store = createWeb216D1SnapshotStore({ database, ...options });
    assert.equal(isWeb216D1SnapshotStore(store), true);
    assert.equal(isWeb216D1SnapshotStore({ ...store }), false);
    const empty = await store.initialiseIfAbsent();
    assert.deepEqual(empty, options.initialSnapshot);
    const result = await store.publish(plan(empty, 1));
    assert.equal(result.status, "published-and-verified");
    if (result.status !== "published-and-verified") throw Error("Expected publication");
    assert.equal(result.observation.persistence, "database-acknowledged-and-verified-readback");
    assert.equal(result.observation.attestation, "not-attested");
    assert.equal(result.record.receipt.evidence.persistence, "not-persisted");
    assert.equal(canonicalJson(result).includes(key(1)), false);
    database.close(); database = new SqliteD1(path);
    const reopened = createWeb216D1SnapshotStore({ database, ...options });
    assert.deepEqual(await reopened.initialiseIfAbsent(), result.snapshot);
    assert.equal(lookupWeb216TransactionalRecord(await reopened.readSnapshot(), key(1), options.material).status, "found-model-record");
  } finally { database.close(); }
});

test("concurrent plans on independent SQLite connections publish one indivisible snapshot", async (t) => {
  const directory = mkdtempSync(join(tmpdir(), "web216-d1-race-"));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  const path = join(directory, "capture.sqlite"); const options = inputs();
  const first = new SqliteD1(path); const second = new SqliteD1(path);
  t.after(() => { first.close(); second.close(); });
  const a = createWeb216D1SnapshotStore({ database: first, ...options });
  const b = createWeb216D1SnapshotStore({ database: second, ...options });
  const state = await a.initialiseIfAbsent();
  let both!: () => void; const ready = new Promise<void>((resolve) => { both = resolve; });
  let arrived = 0;
  const barrier = async (sql: string) => { if (sql === WEB216_D1_SQL.update) { arrived += 1; if (arrived === 2) both(); await ready; } };
  first.hooks.beforeRun = barrier; second.hooks.beforeRun = barrier;
  const outcomes = await Promise.all([a.publish(plan(state, 1)), b.publish(plan(state, 2))]);
  assert.deepEqual(outcomes.map((outcome) => outcome.status).sort(), ["published-and-verified", "stale-head"]);
  const current = await a.readSnapshot();
  assert.equal(current.records.length, 1); assert.equal(current.events.length, 1); assert.equal(current.head.sequence, 1);
  const loser = current.records[0]!.period === "2026-07" ? 2 : 1;
  assert.equal(lookupWeb216TransactionalRecord(current, key(loser), options.material).status, "not-found-in-verified-snapshot");
  delete first.hooks.beforeRun; delete second.hooks.beforeRun;
  assert.equal((await b.publish(plan(current, loser))).status, "published-and-verified");
  assert.equal((await a.readSnapshot()).head.sequence, 2);
});

test("failed SQL leaves the previous snapshot; lost acknowledgement never reports success", async (t) => {
  const f = fixture(t); const empty = await f.store.initialiseIfAbsent(); const proposed = plan(empty, 1);
  f.database.hooks.beforeRun = async (sql) => { if (sql === WEB216_D1_SQL.update) throw Error("synthetic failure before commit"); };
  await assert.rejects(f.store.publish(proposed), errorCode("uncertain-write"));
  assert.deepEqual(await f.store.readSnapshot(), empty);
  delete f.database.hooks.beforeRun;
  f.database.hooks.afterRun = async (sql) => { if (sql === WEB216_D1_SQL.update) throw Error("synthetic timeout after commit"); };
  await assert.rejects(f.store.publish(proposed), errorCode("uncertain-write"));
  delete f.database.hooks.afterRun;
  const recovered = await f.store.readSnapshot();
  assert.equal(recovered.records.length, 1); assert.deepEqual(recovered.records[0], proposed.record);
  assert.equal((await f.store.publish(proposed)).status, "stale-head");
  assert.equal(recovered.events.length, 1);
});

test("read-back failure after a committed CAS is uncertain, not successful or definitely absent", async (t) => {
  const f = fixture(t); const empty = await f.store.initialiseIfAbsent();
  f.database.hooks.afterRun = async (sql) => {
    if (sql === WEB216_D1_SQL.update) f.database.sqlite.exec("UPDATE web216_cpih_snapshot SET snapshot_json = '{}'");
  };
  await assert.rejects(f.store.publish(plan(empty, 1)), errorCode("uncertain-write"));
  await assert.rejects(f.store.readSnapshot(), errorCode("corruption"));
});

test("read-back failure after initial INSERT is uncertain; existing-row read errors stay explicit", async (t) => {
  const f = fixture(t);
  f.database.hooks.afterRun = async (sql) => {
    if (sql === WEB216_D1_SQL.insert) f.database.sqlite.exec("UPDATE web216_cpih_snapshot SET snapshot_json = '{}'");
  };
  await assert.rejects(f.store.initialiseIfAbsent(), errorCode("uncertain-write"));
  delete f.database.hooks.afterRun;
  await assert.rejects(f.store.initialiseIfAbsent(), errorCode("corruption"));
});

test("abort before or during the internal read cannot continue to issue a CAS", async (t) => {
  const f = fixture(t); const empty = await f.store.initialiseIfAbsent(); const proposed = plan(empty, 1);
  const controller = new AbortController(); let writes = 0;
  f.database.hooks.beforeRun = async (sql) => { if (sql === WEB216_D1_SQL.update) writes += 1; };
  let entered!: () => void; let release!: () => void;
  const waiting = new Promise<void>((resolve) => { entered = resolve; });
  const gate = new Promise<void>((resolve) => { release = resolve; });
  f.database.hooks.beforeFirst = async () => { entered(); await gate; };
  const operation = f.store.publish(proposed, { signal: controller.signal });
  await waiting; controller.abort(); release();
  await assert.rejects(operation, errorCode("cancelled-before-write"));
  delete f.database.hooks.beforeFirst;
  await assert.rejects(f.store.publish(proposed, { signal: controller.signal }), errorCode("cancelled-before-write"));
  assert.equal(writes, 0); assert.deepEqual(await f.store.readSnapshot(), empty);
});

test("abort after UPDATE issuance remains uncertain even when the committed write is recovered", async (t) => {
  const f = fixture(t); const empty = await f.store.initialiseIfAbsent(); const proposed = plan(empty, 1);
  const controller = new AbortController(); let entered!: () => void; let release!: () => void;
  const waiting = new Promise<void>((resolve) => { entered = resolve; });
  const gate = new Promise<void>((resolve) => { release = resolve; });
  f.database.hooks.afterRun = async (sql) => { if (sql === WEB216_D1_SQL.update) { entered(); await gate; } };
  const operation = f.store.publish(proposed, { signal: controller.signal });
  await waiting; controller.abort(); release();
  await assert.rejects(operation, errorCode("uncertain-write"));
  delete f.database.hooks.afterRun;
  const recovered = await f.store.readSnapshot();
  assert.deepEqual(recovered.records[0], proposed.record); assert.equal(recovered.head.sequence, 1);
});

test("capacity is subtractive, replay remains a model lookup and no extra row is written", async (t) => {
  const f = fixture(t, 1); const empty = await f.store.initialiseIfAbsent();
  await f.store.publish(plan(empty, 1, f));
  const current = await f.store.readSnapshot();
  assert.throws(() => plan(current, 2, f), /capacity/u);
  assert.equal(lookupWeb216TransactionalRecord(current, key(1), f.material).status, "found-model-record");
  assert.equal((await f.store.initialiseIfAbsent()).head.sequence, 1);
});

test("the trusted descriptor is not derived from a stored row or accepted from another store", async (t) => {
  const f = fixture(t); await f.store.initialiseIfAbsent();
  const alternate = inputs(32);
  const other = createWeb216D1SnapshotStore({ database: f.database, ...alternate });
  await assert.rejects(other.initialiseIfAbsent(), errorCode("corruption"));
  assert.equal((await f.store.readSnapshot()).descriptor.maximum_records, 128);
  assert.throws(() => createWeb216D1SnapshotStore({ ...f,
    material: { ...f.material, expectedSoftware: { ...SOFTWARE, revision: "b".repeat(40) } },
  }), errorCode("invalid-input"));
});

test("byte, canonical JSON, column and receipt corruption fail closed", async (t) => {
  const f = fixture(t); const empty = await f.store.initialiseIfAbsent();
  const changed = await f.store.publish(plan(empty, 1));
  if (changed.status !== "published-and-verified") throw Error("Expected publication");
  const original = canonicalJson(changed.snapshot);
  for (const encoded of ["{}", original + " ", original.replace('"schema":', '"schema":"duplicated","schema":'),
    original.replace('"period":"2026-07"', '"period":"2026-08"')]) {
    f.database.sqlite.prepare("UPDATE web216_cpih_snapshot SET snapshot_json = ?").run(encoded);
    await assert.rejects(f.store.readSnapshot(), errorCode("corruption"));
  }
  f.database.sqlite.prepare("UPDATE web216_cpih_snapshot SET snapshot_json = ?").run(original);
  for (const sql of ["UPDATE web216_cpih_snapshot SET checkpoint_id = 'wrong'",
    "UPDATE web216_cpih_snapshot SET store_id = 'wrong'", "UPDATE web216_cpih_snapshot SET sequence = 0"]) {
    f.database.sqlite.exec(sql); await assert.rejects(f.store.readSnapshot(), errorCode("corruption"));
    f.database.sqlite.prepare("UPDATE web216_cpih_snapshot SET checkpoint_id = ?, store_id = ?, sequence = 1")
      .run(changed.snapshot.head.checkpoint_id, changed.snapshot.descriptor.store_id);
  }
});

test("malformed replacement schema cannot hide duplicate singleton rows or oversized JSON", async (t) => {
  const f = fixture(t); const empty = await f.store.initialiseIfAbsent();
  f.database.sqlite.exec("DROP TABLE web216_cpih_snapshot; CREATE TABLE web216_cpih_snapshot(singleton, store_id, checkpoint_id, sequence, snapshot_json)");
  const insert = f.database.sqlite.prepare("INSERT INTO web216_cpih_snapshot VALUES(1, ?, ?, 0, ?)");
  const values = [empty.descriptor.store_id, empty.head.checkpoint_id, canonicalJson(empty)];
  insert.run(...values); insert.run(...values);
  await assert.rejects(f.store.readSnapshot(), errorCode("corruption"));
  f.database.sqlite.exec("DELETE FROM web216_cpih_snapshot");
  insert.run(...values.slice(0, 2), "x".repeat(WEB216_D1_MAX_SNAPSHOT_BYTES + 1));
  const returned = f.database.sqlite.prepare(WEB216_D1_SQL.read).get();
  assert.equal(returned!.snapshot_json, null);
  await assert.rejects(f.store.readSnapshot(), errorCode("corruption"));
});

test("missing database, malformed plans and copied stores do not grant execution", async (t) => {
  const unmigrated = new SqliteD1(":memory:", false); t.after(() => unmigrated.close());
  const unsupported = createWeb216D1SnapshotStore({ database: unmigrated, ...inputs() });
  await assert.rejects(unsupported.readSnapshot(), errorCode("unavailable"));
  await assert.rejects(unsupported.initialiseIfAbsent(), errorCode("uncertain-write"));
  assert.equal(unmigrated.sqlite.prepare("SELECT COUNT(*) AS n FROM sqlite_schema WHERE type='table'").get()!.n, 0);
  const f = fixture(t);
  await assert.rejects(f.store.readSnapshot(), errorCode("uninitialised"));
  const empty = await f.store.initialiseIfAbsent();
  await assert.rejects(f.store.publish({ ...plan(empty, 1) }), errorCode("invalid-input"));
  f.database.sqlite.exec("DELETE FROM web216_cpih_snapshot");
  await assert.rejects(f.store.readSnapshot(), errorCode("uninitialised"));
});

test("32/128 record comparison records bounded local SQLite costs, not a D1 hosting benchmark", async (t) => {
  const startedAt = new Date().toISOString();
  const directory = mkdtempSync(join(tmpdir(), "web216-d1-size-"));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  const options = inputs(); let state = options.initialSnapshot;
  const measurements = [];
  for (let i = 1; i <= 128; i += 1) {
    const previous = state; const proposed = plan(state, i);
    state = applyWeb216TransactionalPlanModel(state, proposed, options.material);
    if (i !== 32 && i !== 128) continue;
    const path = join(directory, `capacity-${i}.sqlite`); const database = new SqliteD1(path);
    try {
      const store = createWeb216D1SnapshotStore({ database, ...options }); await store.initialiseIfAbsent();
      const json = canonicalJson(state); const bytes = Buffer.byteLength(json);
      assert.ok(bytes <= WEB216_D1_MAX_SNAPSHOT_BYTES);
      // Seed a verified predecessor, then time one real adapter CAS/read-back.
      database.sqlite.prepare("UPDATE web216_cpih_snapshot SET snapshot_json = ?, checkpoint_id = ?, sequence = ?")
        .run(canonicalJson(previous), previous.head.checkpoint_id, previous.head.sequence);
      const publishStart = performance.now();
      const published = await store.publish(proposed);
      const publishMs = Number((performance.now() - publishStart).toFixed(3));
      assert.equal(published.status, "published-and-verified");
      assert.deepEqual(published.snapshot, state);
      const warm = [];
      for (let repetition = 0; repetition < 3; repetition += 1) {
        const start = performance.now(); assert.equal((await store.readSnapshot()).head.sequence, i);
        warm.push(Number((performance.now() - start).toFixed(3)));
      }
      const cold = [];
      for (let repetition = 0; repetition < 3; repetition += 1) {
        const start = performance.now(); const reopened = new SqliteD1(path);
        try { assert.equal((await createWeb216D1SnapshotStore({ database: reopened, ...options }).readSnapshot()).head.sequence, i); }
        finally { reopened.close(); }
        cold.push(Number((performance.now() - start).toFixed(3)));
      }
      measurements.push({ records: i, snapshot_bytes: bytes, sqlite_file_bytes: statSync(path).size,
        cas_with_validation_and_readback_ms: publishMs,
        warm_full_validation_ms: warm, reopen_full_validation_ms: cold });
    } finally { database.close(); }
  }
  t.diagnostic(JSON.stringify({ kind: "local-sqlite-not-d1", node: process.version, platform: process.platform,
    architecture: process.arch, started_at: startedAt, finished_at: new Date().toISOString(), measurements }));
});
