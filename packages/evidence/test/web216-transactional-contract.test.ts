import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { canonicalJson } from "../src/canonical-json.js";
import { buildWeb216CpihReceipt, type Web216CpihPeriod } from "../src/web216-cpih-receipt.js";
import {
  applyWeb216TransactionalPlanModel, createWeb216TransactionalSnapshot,
  lookupWeb216TransactionalRecord, planWeb216TransactionalAppend,
  verifyWeb216TransactionalSnapshot, Web216TransactionalError,
  WEB216_TRANSACTIONAL_MAX_RECORDS,
  type Web216TransactionalAppendInput, type Web216TransactionalAppendPlan,
  type Web216TransactionalDescriptorInput, type Web216TransactionalMaterial,
  type Web216TransactionalSnapshot,
} from "../src/web216-transactional-contract.js";

const PROJECTION: unknown = JSON.parse(readFileSync(new URL(
  "../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url,
), "utf8"));
const SOFTWARE = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) } as const;
const CREATED = "2026-09-14T18:00:00.000Z";
const KEY_A = ["gis-ai-go", "ik", "v1", "a".repeat(64)].join(":");
const KEY_B = ["gis-ai-go", "ik", "v1", "b".repeat(64)].join(":");
const KEY_C = ["gis-ai-go", "ik", "v1", "c".repeat(64)].join(":");
function fixture(maximumRecords?: number, nonce = "1".repeat(32)) {
  const input: Web216TransactionalDescriptorInput = {
    projection: PROJECTION, software: SOFTWARE, createdAt: CREATED, storeNonce: nonce,
    ...(maximumRecords === undefined ? {} : { maximumRecords }),
  };
  const state = createWeb216TransactionalSnapshot(input);
  const material: Web216TransactionalMaterial = { projection: PROJECTION, expectedSoftware: SOFTWARE, expectedStoreId: state.descriptor.store_id };
  return { input, state, material };
}
function request(key = KEY_A, selected: Web216CpihPeriod = "2026-07", requestId = "transactional-test-a"): Web216TransactionalAppendInput {
  return { idempotencyKey: key, recordedAt: "2026-09-14T18:01:00.000Z", receipt: buildWeb216CpihReceipt({
    projection: PROJECTION, software: SOFTWARE, period: selected, requestId, traceId: "d".repeat(32), createdAt: CREATED,
  }) };
}
function plan(state: Web216TransactionalSnapshot, input: Web216TransactionalAppendInput, material: Web216TransactionalMaterial): Web216TransactionalAppendPlan {
  const outcome = planWeb216TransactionalAppend(state, input, material);
  assert.equal(outcome.status, "append-plan-not-committed");
  if (outcome.status !== "append-plan-not-committed") throw Error("Expected an append plan");
  return outcome.plan;
}
function reject(run: () => unknown, code: Web216TransactionalError["code"]) {
  assert.throws(run, (error: unknown) => error instanceof Web216TransactionalError && error.code === code);
}

test("empty model and append plan make no storage, provider or authority claim", () => {
  const f = fixture();
  assert.equal(f.state.descriptor.maximum_records, WEB216_TRANSACTIONAL_MAX_RECORDS);
  assert.equal(f.state.head.sequence, 0); assert.equal(f.state.head.tail_event_id, null);
  assert.deepEqual(verifyWeb216TransactionalSnapshot(f.state, f.material), f.state);
  const proposed = plan(f.state, request(), f.material);
  assert.equal(proposed.boundary.persistence, "not-established-by-contract");
  assert.equal(proposed.boundary.provider_egress, false);
  assert.equal(proposed.boundary.execution_authority, false);
  assert.equal(proposed.record.receipt.evidence.persistence, "not-persisted");
  assert.equal(proposed.record.receipt.evidence.attestation, "not-attested");
  assert.equal(proposed.expected_head.checkpoint_id, f.state.head.checkpoint_id);
  assert.equal(proposed.next_head.sequence, 1);
  assert.equal(f.state.records.length, 0);
  assert.equal(JSON.stringify(proposed).includes(KEY_A), false);
  assert.equal(Object.isFrozen(proposed.record.receipt), true);
});

test("model append binds both exact CPIH months, unchanged receipt bodies and a complete chain", () => {
  const f = fixture(); let state = f.state;
  for (const [key, selected, requestId] of [[KEY_A, "2026-01", "january"], [KEY_B, "2026-07", "july"]] as const) {
    const input = request(key, selected, requestId);
    const before = canonicalJson(state);
    const proposed = plan(state, input, f.material);
    const next = applyWeb216TransactionalPlanModel(state, proposed, f.material);
    assert.equal(canonicalJson(state), before);
    assert.deepEqual(next.records.at(-1)!.receipt, input.receipt);
    assert.equal(next.records.at(-1)!.period, selected);
    assert.equal(next.events.at(-1)!.previous_event_id, state.head.tail_event_id);
    assert.equal(next.head.sequence, state.head.sequence + 1);
    state = next;
  }
  assert.deepEqual(verifyWeb216TransactionalSnapshot(JSON.parse(JSON.stringify(state)), {
    ...f.material, expectedCheckpointId: state.head.checkpoint_id,
  }), state);
  assert.equal(state.records.length, 2); assert.equal(state.events.length, 2);
});

test("same semantic key replays original evidence; changed period or reused receipt under a new key conflicts", () => {
  const f = fixture(); const original = request();
  const state = applyWeb216TransactionalPlanModel(f.state, plan(f.state, original, f.material), f.material);
  const replay = planWeb216TransactionalAppend(state, request(KEY_A, "2026-07", "different-request-id"), f.material);
  assert.equal(replay.status, "replay-model-record");
  if (replay.status !== "replay-model-record") throw Error("Expected replay");
  assert.deepEqual(replay.record, state.records[0]);
  reject(() => planWeb216TransactionalAppend(state, request(KEY_A, "2026-01"), f.material), "conflict");
  reject(() => planWeb216TransactionalAppend(state, { ...original, idempotencyKey: KEY_B }, f.material), "conflict");
  assert.equal(state.records.length, 1);
});

test("competing expected heads cannot both apply; a fresh plan serialises the other key", () => {
  const f = fixture();
  const first = plan(f.state, request(), f.material);
  const secondInput = request(KEY_B, "2026-01", "request-b");
  const second = plan(f.state, secondInput, f.material);
  const next = applyWeb216TransactionalPlanModel(f.state, first, f.material);
  reject(() => applyWeb216TransactionalPlanModel(next, second, f.material), "stale-head");
  const final = applyWeb216TransactionalPlanModel(next, plan(next, secondInput, f.material), f.material);
  assert.equal(final.records.length, 2); assert.equal(final.head.sequence, 2);
  assert.equal(final.events[1]!.previous_event_id, final.events[0]!.event_id);
});

test("subtractive capacity blocks only new keys, preserving replay and lookup", () => {
  const f = fixture(1);
  const state = applyWeb216TransactionalPlanModel(f.state, plan(f.state, request(), f.material), f.material);
  reject(() => planWeb216TransactionalAppend(state, request(KEY_B, "2026-01", "request-b"), f.material), "capacity");
  assert.equal(planWeb216TransactionalAppend(state, request(), f.material).status, "replay-model-record");
  assert.equal(lookupWeb216TransactionalRecord(state, KEY_A, f.material).status, "found-model-record");
  assert.equal(lookupWeb216TransactionalRecord(state, KEY_C, f.material).status, "not-found-in-verified-snapshot");
  assert.equal(state.records.length, 1);
});

test("an aborted model plan leaves nothing published and a copied or altered plan has no capability", () => {
  const f = fixture(); const proposed = plan(f.state, request(), f.material);
  assert.equal(lookupWeb216TransactionalRecord(f.state, KEY_A, f.material).status, "not-found-in-verified-snapshot");
  reject(() => applyWeb216TransactionalPlanModel(f.state, { ...proposed }, f.material), "invalid-plan");
  reject(() => applyWeb216TransactionalPlanModel(f.state, { ...proposed, boundary: { ...proposed.boundary, persistence: "persisted" } } as unknown as Web216TransactionalAppendPlan, f.material), "invalid-plan");
  reject(() => verifyWeb216TransactionalSnapshot({ ...f.state, records: [proposed.record] }, f.material), "corruption");
  reject(() => verifyWeb216TransactionalSnapshot({ ...f.state, events: [proposed.event] }, f.material), "corruption");
  assert.equal(f.state.head.sequence, 0);
});

test("restart rejects incomplete arrays, duplicates, changed links, extra fields and unknown receipt families", () => {
  const f = fixture();
  const state = applyWeb216TransactionalPlanModel(f.state, plan(f.state, request(), f.material), f.material);
  const mutations: ((value: any) => void)[] = [
    (v) => { v.records = []; }, (v) => { v.events = []; },
    (v) => { v.records.push(v.records[0]); }, (v) => { v.events.push(v.events[0]); },
    (v) => { v.events[0].sequence = 2; }, (v) => { v.events[0].previous_event_id = v.events[0].event_id; },
    (v) => { v.events[0].record_id = "forged"; }, (v) => { v.head.sequence = 0; },
    (v) => { v.head.checkpoint_id = f.state.head.checkpoint_id; },
    (v) => { v.records[0].boundary.persistence = "persisted"; },
    (v) => { v.records[0].extra = "unknown"; }, (v) => { v.descriptor.provider = "arbitrary"; },
    (v) => { v.records[0].receipt.schema = "gis-ai-go.public-read-receipt.v2"; },
  ];
  for (const mutate of mutations) {
    const altered = JSON.parse(JSON.stringify(state)) as unknown; mutate(altered);
    reject(() => verifyWeb216TransactionalSnapshot(altered, f.material), "corruption");
  }
});

test("an independent checkpoint is necessary to reject a self-consistent whole-store rollback", () => {
  const f = fixture();
  const next = applyWeb216TransactionalPlanModel(f.state, plan(f.state, request(), f.material), f.material);
  // Hash consistency alone must not be described as rollback protection.
  assert.deepEqual(verifyWeb216TransactionalSnapshot(f.state, f.material), f.state);
  reject(() => verifyWeb216TransactionalSnapshot(f.state, {
    ...f.material, expectedCheckpointId: next.head.checkpoint_id,
  }), "corruption");
  assert.deepEqual(verifyWeb216TransactionalSnapshot(next, {
    ...f.material, expectedCheckpointId: next.head.checkpoint_id,
  }), next);
});

test("wrong source material, independent software expectation and store identity fail closed", () => {
  const f = fixture();
  const state = applyWeb216TransactionalPlanModel(f.state, plan(f.state, request(), f.material), f.material);
  for (const material of [
    { ...f.material, projection: {} },
    { ...f.material, expectedSoftware: { ...SOFTWARE, revision: "b".repeat(40) } },
    { ...f.material, expectedStoreId: fixture(undefined, "2".repeat(32)).state.descriptor.store_id },
  ]) reject(() => verifyWeb216TransactionalSnapshot(state, material), "corruption");
  const corrupted = JSON.parse(JSON.stringify(request()));
  corrupted.receipt.capture.original_body_sha256.data = "0".repeat(64);
  reject(() => planWeb216TransactionalAppend(f.state, corrupted as Web216TransactionalAppendInput, f.material), "invalid-input");
});

test("timestamp checks preserve sub-millisecond ordering and prevent backwards publication", () => {
  const f = fixture();
  const precise = request();
  const receipt = buildWeb216CpihReceipt({ projection: PROJECTION, software: SOFTWARE, period: "2026-07",
    requestId: "precise-clock", traceId: "d".repeat(32), createdAt: "2026-09-14T18:01:00.000001Z" });
  reject(() => planWeb216TransactionalAppend(f.state, { ...precise, receipt }, f.material), "invalid-input");
  const state = applyWeb216TransactionalPlanModel(f.state, plan(f.state, request(), f.material), f.material);
  reject(() => planWeb216TransactionalAppend(state, { ...request(KEY_B, "2026-01", "request-b"), recordedAt: CREATED }, f.material), "invalid-input");
  reject(() => planWeb216TransactionalAppend(f.state, { ...request(), recordedAt: "2026-02-30T18:00:00.000Z" }, f.material), "invalid-input");
});

test("same-key replay cannot bypass receipt or descriptor publication chronology", () => {
  const f = fixture();
  const state = applyWeb216TransactionalPlanModel(f.state, plan(f.state, request(), f.material), f.material);
  const laterReceipt = buildWeb216CpihReceipt({ projection: PROJECTION, software: SOFTWARE, period: "2026-07",
    requestId: "later-replay", traceId: "d".repeat(32), createdAt: "2026-09-14T18:02:00.000Z" });
  reject(() => planWeb216TransactionalAppend(state, { ...request(), receipt: laterReceipt }, f.material), "invalid-input");
  const earlierReceipt = buildWeb216CpihReceipt({ projection: PROJECTION, software: SOFTWARE, period: "2026-07",
    requestId: "earlier-replay", traceId: "d".repeat(32), createdAt: "2026-09-14T17:50:00.000Z" });
  reject(() => planWeb216TransactionalAppend(state, { ...request(), receipt: earlierReceipt,
    recordedAt: "2026-09-14T17:59:00.000Z" }, f.material), "invalid-input");
  assert.equal(state.records.length, 1);
});

test("malformed keys and raw keys in receipt correlation never enter model records or errors", () => {
  const f = fixture();
  for (const idempotencyKey of ["", "a".repeat(64), ["gis-ai-go", "ik", "v1", "0".repeat(64)].join(":"), 1]) {
    reject(() => planWeb216TransactionalAppend(f.state, { ...request(), idempotencyKey } as Web216TransactionalAppendInput, f.material), "invalid-input");
  }
  const leaked = request(KEY_A, "2026-07", KEY_A);
  try { planWeb216TransactionalAppend(f.state, leaked, f.material); assert.fail("Expected privacy refusal"); }
  catch (error) { assert.ok(error instanceof Web216TransactionalError); assert.equal(error.message.includes(KEY_A), false); }
  reject(() => planWeb216TransactionalAppend(f.state, { ...request(), policy: "allow" } as Web216TransactionalAppendInput, f.material), "invalid-input");
});

test("descriptor inputs cannot increase capacity or introduce arbitrary fields, authority or coercible non-string identities", () => {
  const f = fixture();
  for (const maximumRecords of [0, -1, 129, 4097, 1.5, null, "128"]) {
    reject(() => createWeb216TransactionalSnapshot({ ...f.input, maximumRecords } as Web216TransactionalDescriptorInput), "invalid-input");
  }
  for (const storeNonce of ["0".repeat(32), ["1".repeat(32)], "wrong"]) {
    reject(() => createWeb216TransactionalSnapshot({ ...f.input, storeNonce } as Web216TransactionalDescriptorInput), "invalid-input");
  }
  reject(() => createWeb216TransactionalSnapshot({ ...f.input, authority: "allow-live" } as Web216TransactionalDescriptorInput), "invalid-input");
});
