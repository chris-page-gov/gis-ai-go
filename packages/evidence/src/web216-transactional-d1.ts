/** Inactive, bounded D1-API adapter. No provider, SQL registry or Sessions API.
 * A trusted assembly supplies the DB binding and independent initial descriptor.
 * Structural API compatibility does not prove the binding is D1, deployed,
 * region-pinned, durable under disaster, attested or authorised for a caller.
 */
import { canonicalJson, canonicalJsonClone } from "./canonical-json.js";
import {
  applyWeb216TransactionalPlanModel, verifyWeb216TransactionalSnapshot,
  Web216TransactionalError,
  type Web216TransactionalAppendPlan, type Web216TransactionalMaterial,
  type Web216TransactionalRecord, type Web216TransactionalSnapshot,
} from "./web216-transactional-contract.js";

export const WEB216_D1_MAX_SNAPSHOT_BYTES = 1_048_576;
/** Test/migration reference only. The runtime adapter never executes schema SQL. */
export const WEB216_D1_SCHEMA_SQL = `CREATE TABLE IF NOT EXISTS web216_cpih_snapshot (
    singleton INTEGER PRIMARY KEY CHECK(singleton = 1),
    store_id TEXT NOT NULL, checkpoint_id TEXT NOT NULL,
    sequence INTEGER NOT NULL CHECK(sequence >= 0 AND sequence <= 128),
    snapshot_json TEXT NOT NULL CHECK(length(CAST(snapshot_json AS BLOB)) <= 1048576)
  )`;
export const WEB216_D1_SQL = Object.freeze({
  read: `SELECT singleton, store_id, checkpoint_id, sequence,
    CASE WHEN length(CAST(snapshot_json AS BLOB)) <= 1048576 THEN snapshot_json ELSE NULL END AS snapshot_json,
    length(CAST(snapshot_json AS BLOB)) AS snapshot_bytes,
    (SELECT COUNT(*) FROM (SELECT 1 FROM web216_cpih_snapshot LIMIT 2)) AS row_count
    FROM web216_cpih_snapshot LIMIT 1`,
  insert: `INSERT INTO web216_cpih_snapshot
    (singleton, store_id, checkpoint_id, sequence, snapshot_json) VALUES (1, ?, ?, 0, ?)
    ON CONFLICT(singleton) DO NOTHING`,
  update: `UPDATE web216_cpih_snapshot SET snapshot_json = ?, checkpoint_id = ?, sequence = ?
    WHERE singleton = 1 AND store_id = ? AND checkpoint_id = ? AND sequence = ?`,
} as const);

export interface Web216D1Statement {
  bind(...values: unknown[]): Web216D1Statement;
  first<T = Record<string, unknown>>(): Promise<T | null>;
  run(): Promise<{ success: boolean; meta: { changes: number } }>;
}
export interface Web216D1Database { prepare(sql: string): Web216D1Statement }
export class Web216D1SnapshotError extends TypeError {
  constructor(public readonly code: "invalid-input" | "uninitialised" | "unavailable" | "corruption" | "snapshot-too-large" | "uncertain-write" | "cancelled-before-write") {
    super(`CPIH snapshot adapter rejected: ${code}`);
    this.name = "Web216D1SnapshotError";
  }
}
function fail(code: Web216D1SnapshotError["code"]): never { throw new Web216D1SnapshotError(code); }
function serialise(value: Web216TransactionalSnapshot): string {
  const encoded = canonicalJson(value);
  if (new TextEncoder().encode(encoded).byteLength > WEB216_D1_MAX_SNAPSHOT_BYTES) fail("snapshot-too-large");
  return encoded;
}
const OBSERVATION = Object.freeze({
  persistence: "database-acknowledged-and-verified-readback",
  attestation: "not-attested", provider_egress: false, execution_authority: false,
  disaster_recovery: "not-established", deployment: "not-established-by-adapter",
} as const);
export type Web216D1PublishOutcome =
  | { readonly status: "stale-head"; readonly snapshot: Web216TransactionalSnapshot }
  | { readonly status: "published-and-verified"; readonly snapshot: Web216TransactionalSnapshot;
      readonly record: Web216TransactionalRecord; readonly observation: typeof OBSERVATION };
export interface Web216D1SnapshotStore {
  /** INSERT only; a separately applied migration must have created the table. */
  initialiseIfAbsent(): Promise<Web216TransactionalSnapshot>;
  /** One complete primary statement; does not use a session or replica bookmark. */
  readSnapshot(): Promise<Web216TransactionalSnapshot>;
  /** CAS only. Does not create a plan, execute a provider or retry any write. */
  publish(plan: Web216TransactionalAppendPlan, options?: { readonly signal?: AbortSignal }): Promise<Web216D1PublishOutcome>;
}
const STORES = new WeakSet<object>();
export function isWeb216D1SnapshotStore(value: unknown): value is Web216D1SnapshotStore {
  return typeof value === "object" && value !== null && STORES.has(value);
}

export function createWeb216D1SnapshotStore(input: {
  readonly database: Web216D1Database;
  readonly initialSnapshot: Web216TransactionalSnapshot;
  readonly material: Omit<Web216TransactionalMaterial, "expectedCheckpointId">;
}): Web216D1SnapshotStore {
  // The database binding is a trusted runtime object, never parsed from JSON.
  const database = input.database;
  let material: Web216TransactionalMaterial;
  let initial: Web216TransactionalSnapshot;
  let initialJson: string;
  try {
    material = canonicalJsonClone(input.material);
    if (Object.keys(material).sort().join(",") !== "expectedSoftware,expectedStoreId,projection") fail("invalid-input");
    initial = verifyWeb216TransactionalSnapshot(input.initialSnapshot, material);
    if (initial.head.sequence !== 0 || initial.records.length !== 0) fail("invalid-input");
    initialJson = serialise(initial);
    if (database === null || typeof database !== "object" || typeof database.prepare !== "function") fail("invalid-input");
  } catch { return fail("invalid-input"); }
  const descriptorJson = canonicalJson(initial.descriptor);

  async function readSnapshot(): Promise<Web216TransactionalSnapshot> {
    let row: Record<string, unknown> | null;
    try { row = await database.prepare(WEB216_D1_SQL.read).first<Record<string, unknown>>(); }
    catch { return fail("unavailable"); }
    if (row === null) fail("uninitialised");
    try {
      row = canonicalJsonClone(row);
      if (Object.keys(row).sort().join(",") !== "checkpoint_id,row_count,sequence,singleton,snapshot_bytes,snapshot_json,store_id" ||
          row.singleton !== 1 || row.row_count !== 1 || typeof row.snapshot_json !== "string" ||
          !Number.isSafeInteger(row.snapshot_bytes) || (row.snapshot_bytes as number) < 1 ||
          (row.snapshot_bytes as number) > WEB216_D1_MAX_SNAPSHOT_BYTES ||
          new TextEncoder().encode(row.snapshot_json).byteLength !== row.snapshot_bytes) fail("corruption");
      // Exact canonical bytes reject duplicate JSON keys and alternative encodings.
      const parsed: unknown = JSON.parse(row.snapshot_json);
      if (canonicalJson(parsed) !== row.snapshot_json) fail("corruption");
      const verified = verifyWeb216TransactionalSnapshot(parsed, material);
      if (canonicalJson(verified.descriptor) !== descriptorJson || row.store_id !== verified.descriptor.store_id ||
          row.checkpoint_id !== verified.head.checkpoint_id || row.sequence !== verified.head.sequence) fail("corruption");
      return verified;
    } catch { return fail("corruption"); }
  }

  async function initialiseIfAbsent(): Promise<Web216TransactionalSnapshot> {
    let changes: number;
    try {
      const inserted = await database.prepare(WEB216_D1_SQL.insert).bind(
        initial.descriptor.store_id, initial.head.checkpoint_id, initialJson,
      ).run();
      if (inserted.success !== true || ![0, 1].includes(inserted.meta.changes)) fail("uncertain-write");
      changes = inserted.meta.changes;
    } catch { return fail("uncertain-write"); }
    // Existing data must match the independently supplied store, not be adopted.
    try { return await readSnapshot(); }
    catch (error) { if (changes === 1) return fail("uncertain-write"); throw error; }
  }

  async function publish(plan: Web216TransactionalAppendPlan, options: { readonly signal?: AbortSignal } = {}): Promise<Web216D1PublishOutcome> {
    const signal = options.signal;
    function beforeWrite(): void { if (signal?.aborted === true) fail("cancelled-before-write"); }
    function afterWrite(): void { if (signal?.aborted === true) fail("uncertain-write"); }
    beforeWrite();
    let current: Web216TransactionalSnapshot;
    try { current = await readSnapshot(); }
    catch (error) { beforeWrite(); throw error; }
    beforeWrite();
    let next: Web216TransactionalSnapshot;
    try { next = applyWeb216TransactionalPlanModel(current, plan, material); }
    catch (error) {
      if (error instanceof Web216TransactionalError && error.code === "stale-head") {
        return Object.freeze({ status: "stale-head", snapshot: current });
      }
      return fail("invalid-input");
    }
    const encoded = serialise(next);
    let changes: number;
    let issued = false;
    try {
      const statement = database.prepare(WEB216_D1_SQL.update).bind(encoded, next.head.checkpoint_id,
        next.head.sequence, current.descriptor.store_id, current.head.checkpoint_id, current.head.sequence);
      beforeWrite();
      issued = true;
      const result = await statement.run();
      afterWrite();
      if (result.success !== true || ![0, 1].includes(result.meta.changes)) fail("uncertain-write");
      changes = result.meta.changes;
    } catch { if (!issued) beforeWrite(); return fail("uncertain-write"); }
    try {
      const verified = await readSnapshot();
      afterWrite();
      if (changes === 0) return Object.freeze({ status: "stale-head", snapshot: verified });
      // Another valid writer may have advanced the head since this CAS succeeded.
      const record = verified.records.find((item) => item.record_id === plan.record.record_id);
      if (record === undefined || canonicalJson(record) !== canonicalJson(plan.record)) fail("uncertain-write");
      return Object.freeze({ status: "published-and-verified", snapshot: verified, record, observation: OBSERVATION });
    } catch { return fail("uncertain-write"); }
  }
  const store = Object.freeze({ initialiseIfAbsent, readSnapshot, publish });
  STORES.add(store);
  return store;
}
