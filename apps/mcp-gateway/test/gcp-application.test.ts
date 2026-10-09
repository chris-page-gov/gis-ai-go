import assert from "node:assert/strict";
import test from "node:test";
import { createGcpCpihApplication, provisionGcpCpihPrincipal } from "../src/gcp-application.js";
import { Web216HostedCpihApplicationError } from "../src/web216-hosted-cpih-application.js";
import { validateWeb216HostedCpihMcpResult } from "../src/web216-hosted-cpih-mcp.js";
import { resolveWeb216CpihSelection } from "../src/web216-cpih-selection.js";
import { CLOCK, EVIDENCE, FakeAtomicStore, principal, PROJECTION } from "./gcp-test-support.js";
const KEY = `gis-ai-go:ik:v1:${"a".repeat(64)}`;
const CONTEXT = { requestId: "server-generated-synthetic-1", traceId: "b".repeat(32) };
const query = (period: "2026-01" | "2026-07" = "2026-07", key = KEY) => ({ period,
  selection_plan_id: resolveWeb216CpihSelection({ period }).plan_id, idempotency_key: key });
const code = (expected: string) => (error: unknown) => error instanceof Web216HostedCpihApplicationError && error.code === expected;
async function setup(enrol = true) {
  const backend = new FakeAtomicStore(); const actor = await principal();
  if (enrol) await provisionGcpCpihPrincipal({ backend, principalScope: actor.scope, projection: PROJECTION, evidence: EVIDENCE });
  const options = { backend, principal: actor, projection: PROJECTION, evidence: EVIDENCE, now: () => new Date(CLOCK) };
  return { backend, options, application: createGcpCpihApplication(options) };
}

test("explicit provision, query and restart preserve exact maintained evidence and semantic replay without raw key disclosure", async () => {
  const s = await setup(); const first = await s.application.query(query(), CONTEXT);
  assert.equal(await validateWeb216HostedCpihMcpResult(first), true); assert.equal(first.result.observation.value, "142.7");
  assert.equal(JSON.stringify(first).includes(KEY), false); assert.equal(first.boundary.provider_egress, false);
  const writes = s.backend.writes; const restarted = createGcpCpihApplication(s.options);
  assert.deepEqual(await restarted.query(query(), { ...CONTEXT, requestId: "new-correlation-after-restart" }), first);
  assert.deepEqual(await restarted.inspect({ receipt_id: first.evidence.receipt.receipt_id }), first);
  assert.deepEqual(await restarted.inspect({ idempotency_key: KEY }), first); assert.equal(s.backend.writes, writes);
  await assert.rejects(restarted.query(query("2026-01"), CONTEXT), code("conflict"));
  assert.equal(first.evidence.storage_observation.disaster_recovery, "not-established");
});

test("unprovisioned or deleted history fails closed; no HTTP application path recreates state", async () => {
  const s = await setup(false);
  assert.equal((await s.application.resolve({ period: "2026-07" })).authority.grants_execution, false);
  await assert.rejects(s.application.query(query(), CONTEXT)); await assert.rejects(s.application.inspect({ idempotency_key: KEY }));
  assert.equal(s.backend.writes, 0); assert.equal(s.backend.rows.size, 0);
  await provisionGcpCpihPrincipal({ backend: s.backend, principalScope: s.options.principal.scope, projection: PROJECTION, evidence: EVIDENCE });
  await s.application.query(query(), CONTEXT); const writes = s.backend.writes; s.backend.rows.clear();
  await assert.rejects(s.application.query(query(), CONTEXT)); assert.equal(s.backend.writes, writes); assert.equal(s.backend.rows.size, 0);
});

test("concurrent same-key claims have one atomic winner, one retryable conflict and the losing caller replays exact original receipt", async () => {
  const s = await setup(); let entered = 0; let release!: () => void;
  const both = new Promise<void>((resolve) => { release = resolve; });
  s.backend.beforeSet = async () => { if (++entered === 2) release(); await both; };
  const outcomes = await Promise.allSettled([s.application.query(query(), CONTEXT), createGcpCpihApplication(s.options).query(query(), { ...CONTEXT, requestId: "server-other" })]);
  delete s.backend.beforeSet;
  assert.equal(outcomes.filter((item) => item.status === "fulfilled").length, 1);
  const rejected = outcomes.find((item) => item.status === "rejected"); assert.ok(rejected?.status === "rejected" && code("retryable-conflict")(rejected.reason));
  const replay = await s.application.query(query(), { ...CONTEXT, requestId: "server-retry" });
  assert.equal(replay.evidence.checkpoint.sequence, 1); assert.equal(s.backend.writes, 2);
});

test("lost commit response remains uncertain, then same-key inspection/replay reconciles with no duplicate receipt", async () => {
  const s = await setup(); s.backend.afterSet = async () => { throw Error("synthetic lost acknowledgement after actual atomic write"); };
  await assert.rejects(s.application.query(query(), CONTEXT), code("uncertain-write")); delete s.backend.afterSet;
  const replay = await createGcpCpihApplication(s.options).query(query(), { ...CONTEXT, requestId: "server-after-response-loss" });
  assert.equal(replay.evidence.checkpoint.sequence, 1); assert.equal(s.backend.writes, 2);
  assert.deepEqual(await s.application.inspect({ idempotency_key: KEY }), replay);
});

test("principal isolation, absent-role policy and expired retained claims prevent leakage or key reuse", async () => {
  const s = await setup(); const stored = await s.application.query(query(), CONTEXT);
  const other = await principal(["analyst"], "different-human");
  const application = createGcpCpihApplication({ ...s.options, principal: other });
  await assert.rejects(application.inspect({ receipt_id: stored.evidence.receipt.receipt_id }));
  assert.equal(s.backend.rows.size, 1);
  await provisionGcpCpihPrincipal({ backend: s.backend, principalScope: other.scope, projection: PROJECTION, evidence: EVIDENCE });
  await assert.rejects(application.inspect({ receipt_id: stored.evidence.receipt.receipt_id }), code("not-found"));
  const otherResult = await application.query(query(), { ...CONTEXT, requestId: "other-principal-query" });
  assert.notEqual(otherResult.evidence.record.store_id, stored.evidence.record.store_id);
  const noQuery = createGcpCpihApplication({ ...s.options, principal: await principal(["viewer"]) });
  await assert.rejects(noQuery.query(query("2026-01", `gis-ai-go:ik:v1:${"c".repeat(64)}`), CONTEXT), code("unavailable"));
  const expiredClock = CLOCK + 366 * 86_400_000;
  const reauthenticated = await principal(["analyst"], "synthetic-human", expiredClock);
  const expired = createGcpCpihApplication({ ...s.options, principal: reauthenticated, now: () => new Date(expiredClock) });
  await assert.rejects(expired.query(query(), CONTEXT), code("not-found"));
  await assert.rejects(expired.inspect({ idempotency_key: KEY }), code("not-found"));
  assert.equal(s.backend.writes, 4);
});

test("a changed provisioning seed/software or corrupt atomic document cannot adopt existing history", async () => {
  const s = await setup(); await s.application.query(query(), CONTEXT);
  const changed = createGcpCpihApplication({ ...s.options, evidence: { ...EVIDENCE, sourceRevision: "f".repeat(40) } });
  await assert.rejects(changed.inspect({ idempotency_key: KEY }));
  const row = s.backend.rows.get(s.options.principal.scope)!;
  s.backend.rows.set(s.options.principal.scope, { ...row, fields: { ...row.fields, principal_scope: "f".repeat(64) } });
  await assert.rejects(s.application.query(query(), CONTEXT));
});
