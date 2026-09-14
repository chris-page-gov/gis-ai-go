/**
 * Inactive CPIH transaction model: plans and snapshots, never storage evidence.
 *
 * A future adapter must atomically compare the expected head, enforce unique key
 * and receipt identities, append the immutable record/event and replace the head.
 * A zero-row compare must abort the WHOLE transaction, not let later inserts run.
 * Ambiguous backend outcomes require a consistency-guaranteed read; this model
 * cannot turn a timeout, a stale replica or a caller-supplied hash into a commit.
 *
 * No filesystem, SQL, provider or D1 API is imported. Existing canonical helpers
 * still use node:crypto/node:util; target-runtime compatibility remains unproven.
 */
import { canonicalJson, canonicalJsonClone } from "./canonical-json.js";
import { contentAddress, domainSeparatedSha256 } from "./digest.js";
import { isStrictEvidenceDateTime, type EvidenceSoftwareIdentity } from "./receipt.js";
import {
  buildWeb216CpihReceipt, buildWeb216CpihResult, verifyWeb216CpihReceipt,
  WEB216_CPIH_CAPTURE, type Web216CpihPeriod, type Web216CpihReceipt,
} from "./web216-cpih-receipt.js";

export const WEB216_TRANSACTIONAL_MAX_RECORDS = 128;
export const WEB216_TRANSACTIONAL_RETENTION_DAYS = 365;
export const WEB216_TRANSACTIONAL_DOMAINS = Object.freeze({
  descriptor: "gis-ai-go.web216-transactional-descriptor.v1",
  record: "gis-ai-go.web216-transactional-record.v1",
  event: "gis-ai-go.web216-transactional-event.v1",
  head: "gis-ai-go.web216-transactional-head.v1",
  key: "gis-ai-go.web216-transactional-key.v1",
  fingerprint: "gis-ai-go.web216-transactional-fingerprint.v1",
} as const);
const D = WEB216_TRANSACTIONAL_DOMAINS;
const SNAPSHOT = "gis-ai-go.web216-transactional-snapshot.v1";
const PLAN = "gis-ai-go.web216-transactional-append-plan.v1";
const BOUNDARY = Object.freeze({
  persistence: "not-established-by-contract", attestation: "not-attested",
  provider_egress: false, execution_authority: false,
} as const);
const PLANS = new WeakSet<object>();

export class Web216TransactionalError extends TypeError {
  constructor(public readonly code: "invalid-input" | "corruption" | "conflict" | "capacity" | "stale-head" | "invalid-plan") {
    super(`CPIH transaction contract rejected: ${code}`);
    this.name = "Web216TransactionalError";
  }
}
function fail(code: Web216TransactionalError["code"]): never { throw new Web216TransactionalError(code); }
function object(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) fail("invalid-input");
  return value as Record<string, unknown>;
}
function keys(value: unknown, allowed: readonly string[]): Record<string, unknown> {
  const result = object(value);
  if (Object.keys(result).length !== allowed.length || allowed.some((key) => !Object.hasOwn(result, key))) fail("invalid-input");
  return result;
}
function snapshot<T>(value: T): T {
  try { return canonicalJsonClone(value); } catch { return fail("invalid-input"); }
}
function utcNanoseconds(value: unknown): bigint {
  if (!isStrictEvidenceDateTime(value)) fail("invalid-input");
  const match = /^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d{1,9}))?Z$/u.exec(value);
  if (match === null) fail("invalid-input");
  return BigInt(Date.parse(`${match[1]}Z`)) * 1_000_000n + BigInt((match[2] ?? "").padEnd(9, "0"));
}
function millisTimestamp(value: string): string {
  utcNanoseconds(value);
  if (new Date(value).toISOString() !== value) fail("invalid-input");
  return value;
}
function period(value: unknown): Web216CpihPeriod {
  if (value !== "2026-01" && value !== "2026-07") fail("invalid-input");
  return value;
}
function keyHash(value: unknown): string {
  if (typeof value !== "string" || !/^gis-ai-go:ik:v1:(?!0{64}$)[0-9a-f]{64}$/u.test(value)) fail("invalid-input");
  return domainSeparatedSha256(D.key, { operation: "read-validated-cpih-capture", key: value });
}
function fingerprint(value: Web216CpihPeriod): string {
  return domainSeparatedSha256(D.fingerprint, {
    operation: "read-validated-cpih-capture", period: period(value),
    capture_projection_sha256: WEB216_CPIH_CAPTURE.projection_sha256,
  });
}

export interface Web216TransactionalMaterial {
  readonly projection: unknown;
  /** Independently supplied by the trusted future application, not a DB row. */
  readonly expectedSoftware: EvidenceSoftwareIdentity;
  readonly expectedStoreId: string;
  /** An independently retained checkpoint detects a self-consistent rollback. */
  readonly expectedCheckpointId?: string;
}
export interface Web216TransactionalDescriptorInput {
  readonly storeNonce: string;
  readonly createdAt: string;
  readonly software: EvidenceSoftwareIdentity;
  readonly projection: unknown;
  /** Subtractive capacity only: 1..128; omission fixes the 128-record ceiling. */
  readonly maximumRecords?: number;
}
function descriptorFor(input: Web216TransactionalDescriptorInput) {
  const value = snapshot(input);
  const fields = Object.keys(object(value));
  if (fields.some((key) => !["storeNonce", "createdAt", "software", "projection", "maximumRecords"].includes(key)) ||
      ["storeNonce", "createdAt", "software", "projection"].some((key) => !Object.hasOwn(value, key))) fail("invalid-input");
  const maximum = Object.hasOwn(value, "maximumRecords") ? value.maximumRecords! : WEB216_TRANSACTIONAL_MAX_RECORDS;
  if (!Number.isSafeInteger(maximum) || maximum < 1 || maximum > WEB216_TRANSACTIONAL_MAX_RECORDS ||
      typeof value.storeNonce !== "string" || !/^(?!0{32}$)[0-9a-f]{32}$/u.test(value.storeNonce)) fail("invalid-input");
  millisTimestamp(value.createdAt);
  // Validate full pinned material and software, without publishing this proposal.
  buildWeb216CpihReceipt({ projection: value.projection, software: value.software, period: "2026-01",
    createdAt: value.createdAt, requestId: "transactional-construction", traceId: "1".repeat(32) });
  const core = {
    schema: D.descriptor, created_at: value.createdAt, store_nonce: value.storeNonce,
    capture_projection_sha256: WEB216_CPIH_CAPTURE.projection_sha256, software: value.software,
    maximum_records: maximum, retention_days: WEB216_TRANSACTIONAL_RETENTION_DAYS,
    operation: "read-validated-cpih-capture", admitted_periods: ["2026-01", "2026-07"],
    atomicity: "key-record-event-head-all-or-none", boundary: BOUNDARY,
  } as const;
  return snapshot({ ...core, store_id: contentAddress("gis-ai-go:web216-transactional-store", D.descriptor, core) });
}
export type Web216TransactionalDescriptor = ReturnType<typeof descriptorFor>;
function headFor(storeId: string, sequence: number, tail: string | null) {
  const core = { schema: D.head, store_id: storeId, sequence, tail_event_id: tail } as const;
  return snapshot({ ...core, checkpoint_id: contentAddress("gis-ai-go:web216-transactional-checkpoint", D.head, core) });
}
export type Web216TransactionalHead = ReturnType<typeof headFor>;
function recordFor(descriptor: Web216TransactionalDescriptor, keySha256: string, receipt: Web216CpihReceipt, recordedAt: string) {
  millisTimestamp(recordedAt);
  if (!/^[0-9a-f]{64}$/u.test(keySha256) || utcNanoseconds(recordedAt) < utcNanoseconds(receipt.created_at) ||
      utcNanoseconds(recordedAt) < utcNanoseconds(descriptor.created_at)) fail("invalid-input");
  const core = {
    schema: D.record, store_id: descriptor.store_id, idempotency_key_sha256: keySha256,
    request_fingerprint_sha256: fingerprint(receipt.operation.period), period: receipt.operation.period,
    recorded_at: recordedAt,
    retain_until: new Date(Date.parse(recordedAt) + WEB216_TRANSACTIONAL_RETENTION_DAYS * 86_400_000).toISOString(),
    receipt, verification: "full-material-verified-model-record", boundary: BOUNDARY,
  } as const;
  return snapshot({ ...core, record_id: contentAddress("gis-ai-go:web216-transactional-record", D.record, core) });
}
export type Web216TransactionalRecord = ReturnType<typeof recordFor>;
function eventFor(record: Web216TransactionalRecord, previous: Web216TransactionalHead) {
  const core = {
    schema: D.event, store_id: record.store_id, sequence: previous.sequence + 1,
    previous_event_id: previous.tail_event_id, record_id: record.record_id,
    receipt_id: record.receipt.receipt_id, idempotency_key_sha256: record.idempotency_key_sha256,
    recorded_at: record.recorded_at,
  } as const;
  return snapshot({ ...core, event_id: contentAddress("gis-ai-go:web216-transactional-event", D.event, core) });
}
export type Web216TransactionalEvent = ReturnType<typeof eventFor>;
export interface Web216TransactionalSnapshot {
  readonly schema: typeof SNAPSHOT;
  readonly descriptor: Web216TransactionalDescriptor;
  /** Both arrays are complete, in event sequence order; no filtered DB joins. */
  readonly records: readonly Web216TransactionalRecord[];
  readonly events: readonly Web216TransactionalEvent[];
  readonly head: Web216TransactionalHead;
}

/** Empty model only: creates no database, filesystem entry or committed head. */
export function createWeb216TransactionalSnapshot(input: Web216TransactionalDescriptorInput): Web216TransactionalSnapshot {
  try {
    const descriptor = descriptorFor(input);
    return snapshot({ schema: SNAPSHOT, descriptor, records: [], events: [], head: headFor(descriptor.store_id, 0, null) });
  } catch { return fail("invalid-input"); }
}
function checkedMaterial(value: Web216TransactionalMaterial): Web216TransactionalMaterial {
  const material = snapshot(value);
  const fields = Object.keys(object(material));
  if (fields.some((key) => !["projection", "expectedSoftware", "expectedStoreId", "expectedCheckpointId"].includes(key)) ||
      ["projection", "expectedSoftware", "expectedStoreId"].some((key) => !Object.hasOwn(material, key)) ||
      typeof material.expectedStoreId !== "string") fail("invalid-input");
  if (material.expectedCheckpointId !== undefined && typeof material.expectedCheckpointId !== "string") fail("invalid-input");
  return material;
}
function verifyReceipt(receipt: Web216CpihReceipt, material: Web216TransactionalMaterial): void {
  const selected = period(receipt.operation.period);
  // The receipt body's identifier grammar alone permits this ASCII spelling.
  // A transactional public record must additionally exclude reconciliation keys.
  if (/gis-ai-go:ik:v1:[0-9a-f]{64}/iu.test(receipt.request_id)) fail("corruption");
  if (!verifyWeb216CpihReceipt(receipt, {
    projection: material.projection, expectedSoftware: material.expectedSoftware,
    normalisedParameters: { period: selected }, resultCore: buildWeb216CpihResult(material.projection, selected),
  }).valid) fail("corruption");
}

/**
 * Full-material consistency check, not evidence of actual publication or durable
 * storage. Without an independent expected checkpoint, whole-store rollback or
 * replacement by another self-consistent snapshot cannot be detected by hashes.
 */
export function verifyWeb216TransactionalSnapshot(value: unknown, supplied: Web216TransactionalMaterial): Web216TransactionalSnapshot {
  try {
    const material = checkedMaterial(supplied);
    const candidate = snapshot(value) as Web216TransactionalSnapshot;
    keys(candidate, ["schema", "descriptor", "records", "events", "head"]);
    if (candidate.schema !== SNAPSHOT || !Array.isArray(candidate.records) || !Array.isArray(candidate.events) ||
        candidate.records.length > WEB216_TRANSACTIONAL_MAX_RECORDS || candidate.records.length !== candidate.events.length) fail("corruption");
    const d = candidate.descriptor;
    const expected = descriptorFor({ storeNonce: d.store_nonce, createdAt: d.created_at,
      software: material.expectedSoftware, projection: material.projection, maximumRecords: d.maximum_records });
    if (canonicalJson(d) !== canonicalJson(expected) || d.store_id !== material.expectedStoreId ||
        candidate.records.length > d.maximum_records) fail("corruption");
    let head = headFor(d.store_id, 0, null);
    let previousTime = utcNanoseconds(d.created_at);
    const keysSeen = new Set<string>(); const receiptsSeen = new Set<string>(); const recordsSeen = new Set<string>();
    for (let index = 0; index < candidate.records.length; index += 1) {
      const record = candidate.records[index]!;
      verifyReceipt(record.receipt, material);
      const expectedRecord = recordFor(d, record.idempotency_key_sha256, record.receipt, record.recorded_at);
      const event = eventFor(expectedRecord, head);
      if (canonicalJson(record) !== canonicalJson(expectedRecord) || canonicalJson(candidate.events[index]) !== canonicalJson(event) ||
          utcNanoseconds(record.recorded_at) < previousTime || keysSeen.has(record.idempotency_key_sha256) ||
          receiptsSeen.has(record.receipt.receipt_id) || recordsSeen.has(record.record_id)) fail("corruption");
      previousTime = utcNanoseconds(record.recorded_at);
      keysSeen.add(record.idempotency_key_sha256); receiptsSeen.add(record.receipt.receipt_id); recordsSeen.add(record.record_id);
      head = headFor(d.store_id, index + 1, event.event_id);
    }
    if (canonicalJson(candidate.head) !== canonicalJson(head) ||
        (material.expectedCheckpointId !== undefined && material.expectedCheckpointId !== head.checkpoint_id)) fail("corruption");
    return candidate;
  } catch { return fail("corruption"); }
}

export interface Web216TransactionalAppendInput {
  readonly idempotencyKey: string;
  readonly receipt: Web216CpihReceipt;
  readonly recordedAt: string;
}
export interface Web216TransactionalAppendPlan {
  readonly schema: typeof PLAN;
  readonly store_id: string;
  readonly expected_head: Web216TransactionalHead;
  readonly record: Web216TransactionalRecord;
  readonly event: Web216TransactionalEvent;
  readonly next_head: Web216TransactionalHead;
  readonly boundary: typeof BOUNDARY;
}
export type Web216TransactionalPlanOutcome =
  | { readonly status: "replay-model-record"; readonly record: Web216TransactionalRecord }
  | { readonly status: "append-plan-not-committed"; readonly plan: Web216TransactionalAppendPlan };

/** Input material is checked even on replay; a replay never replaces old evidence. */
export function planWeb216TransactionalAppend(value: unknown, input: Web216TransactionalAppendInput, material: Web216TransactionalMaterial): Web216TransactionalPlanOutcome {
  const current = verifyWeb216TransactionalSnapshot(value, material);
  let request: Web216TransactionalAppendInput;
  try {
    request = snapshot(input); keys(request, ["idempotencyKey", "receipt", "recordedAt"]);
    keyHash(request.idempotencyKey); verifyReceipt(request.receipt, material); millisTimestamp(request.recordedAt);
  } catch { return fail("invalid-input"); }
  const hash = keyHash(request.idempotencyKey);
  // Even replay requests must satisfy receipt/descriptor publication chronology.
  const record = recordFor(current.descriptor, hash, request.receipt, request.recordedAt);
  const existing = current.records.find((record) => record.idempotency_key_sha256 === hash);
  if (existing !== undefined) {
    if (existing.request_fingerprint_sha256 !== fingerprint(request.receipt.operation.period)) fail("conflict");
    return snapshot({ status: "replay-model-record", record: existing });
  }
  if (current.records.length >= current.descriptor.maximum_records) fail("capacity");
  if (current.records.some((record) => record.receipt.receipt_id === request.receipt.receipt_id)) fail("conflict");
  const previous = current.records.at(-1);
  if (previous !== undefined && utcNanoseconds(record.recorded_at) < utcNanoseconds(previous.recorded_at)) fail("invalid-input");
  const event = eventFor(record, current.head);
  const plan: Web216TransactionalAppendPlan = snapshot({ schema: PLAN, store_id: current.descriptor.store_id,
    expected_head: current.head, record, event, next_head: headFor(current.descriptor.store_id, event.sequence, event.event_id), boundary: BOUNDARY });
  PLANS.add(plan);
  return Object.freeze({ status: "append-plan-not-committed", plan });
}

/** Pure reference transition. Its return value is explicitly NOT a commit receipt. */
export function applyWeb216TransactionalPlanModel(value: unknown, plan: Web216TransactionalAppendPlan, material: Web216TransactionalMaterial): Web216TransactionalSnapshot {
  if (typeof plan !== "object" || plan === null || !PLANS.has(plan)) fail("invalid-plan");
  const current = verifyWeb216TransactionalSnapshot(value, material);
  if (plan.store_id !== current.descriptor.store_id || canonicalJson(plan.expected_head) !== canonicalJson(current.head)) fail("stale-head");
  const next = snapshot({ schema: SNAPSHOT, descriptor: current.descriptor,
    records: [...current.records, plan.record], events: [...current.events, plan.event], head: plan.next_head });
  // The caller's pre-transaction checkpoint pins current, not the proposed next.
  return verifyWeb216TransactionalSnapshot(next, {
    projection: material.projection, expectedSoftware: material.expectedSoftware,
    expectedStoreId: material.expectedStoreId, expectedCheckpointId: plan.next_head.checkpoint_id,
  });
}

/** Model lookup cannot assert read freshness, transaction success or persistence. */
export function lookupWeb216TransactionalRecord(value: unknown, idempotencyKey: string, material: Web216TransactionalMaterial) {
  const current = verifyWeb216TransactionalSnapshot(value, material);
  const hash = keyHash(idempotencyKey);
  const record = current.records.find((item) => item.idempotency_key_sha256 === hash);
  return record === undefined
    ? snapshot({ status: "not-found-in-verified-snapshot" } as const)
    : snapshot({ status: "found-model-record", record } as const);
}
