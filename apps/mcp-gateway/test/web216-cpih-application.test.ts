import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import {
  buildWeb216CpihReceipt, openPublicEvidenceLedger, openWeb216CpihReconciliationIndex,
  type Web216CpihPeriod,
} from "@gis-ai-go/evidence";
import { createWeb216CpihApplication, isWeb216CpihApplication, Web216CpihApplicationError } from "../src/web216-cpih-application.js";
import { Web216CpihSelectionError } from "../src/web216-cpih-selection.js";
const testSupportPath = new URL("../../../../packages/evidence/dist/src/public-ledger-capacity.js", import.meta.url).href;
const { withLowerPublicEvidenceLedgerEventLimitForTest } = await import(testSupportPath) as {
  withLowerPublicEvidenceLedgerEventLimitForTest<T extends object>(options: T, maximumEvents: number): T;
};

const PROJECTION: unknown = JSON.parse(readFileSync(new URL("../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url), "utf8"));
const SOFTWARE = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) } as const;
const NOW = () => new Date("2026-09-14T18:00:00.000Z");
const KEY = ["gis-ai-go", "ik", "v1", "a".repeat(64)].join(":");
const SECOND_KEY = ["gis-ai-go", "ik", "v1", "b".repeat(64)].join(":");
const CONTEXT = { requestId: "web216-query-test", traceId: "c".repeat(32) };

function scenario(maximumEvents?: number) {
  const root = mkdtempSync(join(tmpdir(), "web216-application-"));
  function open() {
    const ledgerOptions = { rootDirectory: join(root, "ledger"), now: NOW };
    const ledger = openPublicEvidenceLedger(maximumEvents === undefined ? ledgerOptions :
      withLowerPublicEvidenceLedgerEventLimitForTest(ledgerOptions, maximumEvents));
    const reconciliationIndex = openWeb216CpihReconciliationIndex({ rootDirectory: join(root, "index"), ledger, now: NOW });
    return { ledger, reconciliationIndex, application: createWeb216CpihApplication({ ledger, reconciliationIndex, projection: PROJECTION, software: SOFTWARE, now: NOW }) };
  }
  return { root, open, ...open(), close: () => rmSync(root, { recursive: true, force: true }) };
}
function request(application: ReturnType<typeof scenario>["application"], period: Web216CpihPeriod = "2026-07", key = KEY) {
  return { period, selection_plan_id: application.resolve({ period }).plan_id, idempotency_key: key };
}
function expectError(run: () => unknown, code: Web216CpihApplicationError["code"]) {
  assert.throws(run, (error: unknown) => error instanceof Web216CpihApplicationError && error.code === code);
}

test("construction and selection do not write claims or receipts or activate a transport", () => {
  const s = scenario();
  try {
    assert.equal(isWeb216CpihApplication(s.application), true);
    assert.equal(isWeb216CpihApplication({ ...s.application }), false);
    assert.equal(Object.isFrozen(s.application), true);
    assert.deepEqual(s.application.readiness(), { status: "ready", new_claims_available: true });
    const selection = s.application.resolve({ period: "2026-07" });
    assert.equal(selection.authority.grants_execution, false);
    assert.equal(s.ledger.verify().event_count, 0);
    assert.equal(s.reconciliationIndex.verify().claim_count, 0);
  } finally { s.close(); }
});

test("each exact captured period becomes a full-material-verified durable result and inspectable receipt", () => {
  const s = scenario();
  try {
    for (const [period, value, key] of [["2026-07", "142.7", KEY], ["2026-01", "139.4", SECOND_KEY]] as const) {
      const response = s.application.query(request(s.application, period, key), { ...CONTEXT, requestId: `read-${period}` });
      assert.equal(response.result.observation.value, value);
      assert.equal(response.result.series.base_year, 2015);
      assert.equal(response.result.provider_egress, false);
      assert.equal(response.evidence.storage.status, "persisted");
      assert.equal(response.evidence.receipt.evidence.persistence, "not-persisted");
      assert.equal(response.evidence.record.verification.receipt, "full-material-verified-at-ingest");
      assert.deepEqual(s.application.inspect({ receipt_id: response.evidence.receipt.receipt_id }), response);
      assert.deepEqual(s.application.inspect({ idempotency_key: key }), response);
      assert.equal(JSON.stringify(response).includes(key), false);
    }
    assert.equal(s.ledger.verify().event_count, 2);
    assert.equal(s.reconciliationIndex.verify().completed_count, 2);
  } finally { s.close(); }
});

test("lost-response retry and clean restart return the original receipt without new execution", () => {
  const s = scenario();
  try {
    const input = request(s.application);
    const first = s.application.query(input, CONTEXT);
    const repeat = s.application.query(input, { requestId: "another-transport-request", traceId: "d".repeat(32) });
    assert.deepEqual(repeat, first);
    const reopened = s.open();
    assert.deepEqual(reopened.application.query(input, { requestId: "after-restart", traceId: "e".repeat(32) }), first);
    assert.equal(reopened.ledger.verify().event_count, 1);
    expectError(() => reopened.application.query(request(reopened.application, "2026-01"), CONTEXT), "conflict");
    assert.equal(reopened.ledger.verify().event_count, 1);
  } finally { s.close(); }
});

test("invalid plan, unknown provider inputs and invalid correlation are rejected before a claim", () => {
  const s = scenario();
  try {
    const valid = request(s.application);
    for (const input of [{ ...valid, selection_plan_id: "forged" }, { ...valid, period: "latest" }, { ...valid, policy: "allow" }, { ...valid, url: "https://example.org" }]) {
      assert.throws(() => s.application.query(input, CONTEXT), Web216CpihSelectionError);
    }
    expectError(() => s.application.query(valid, { ...CONTEXT, requestId: "bad request" }), "unavailable");
    assert.equal(s.reconciliationIndex.verify().claim_count, 0);
    assert.equal(s.ledger.verify().event_count, 0);
  } finally { s.close(); }
});

test("cancellation before admission creates no claim, and read-only missing lookup creates no receipt", () => {
  const s = scenario();
  try {
    const controller = new AbortController(); controller.abort();
    expectError(() => s.application.query(request(s.application), { ...CONTEXT, signal: controller.signal }), "cancelled");
    expectError(() => s.application.inspect({ idempotency_key: KEY }), "not-found");
    expectError(() => s.application.inspect({ receipt_id: `gis-ai-go:evidence-receipt:sha256:${"e".repeat(64)}` }), "not-found");
    assert.equal(s.reconciliationIndex.verify().claim_count, 0);
    assert.equal(s.ledger.verify().event_count, 0);
  } finally { s.close(); }
});

test("a published resolution without the record remains pending and is never silently reclaimed", () => {
  const s = scenario();
  try {
    const claim = s.reconciliationIndex.claim({ idempotencyKey: KEY, period: "2026-07", ...CONTEXT });
    assert.equal(claim.status, "claimed");
    if (claim.status !== "claimed") throw Error("Expected new claim");
    const receipt = buildWeb216CpihReceipt({ projection: PROJECTION, software: SOFTWARE, period: "2026-07", ...CONTEXT, createdAt: NOW().toISOString() });
    s.reconciliationIndex.resolve(claim.claim, receipt);
    expectError(() => s.application.query(request(s.application), CONTEXT), "pending");
    expectError(() => s.application.inspect({ idempotency_key: KEY }), "pending");
    assert.equal(s.ledger.verify().event_count, 0);
    assert.equal(s.reconciliationIndex.verify().pending_count, 1);
  } finally { s.close(); }
});

test("corrupt durable material blocks readiness, execution and inspection without leaking content", () => {
  const s = scenario();
  try {
    const result = s.application.query(request(s.application), CONTEXT);
    const records = join(s.root, "ledger", "records");
    const file = readdirSync(records)[0]; assert.ok(file);
    writeFileSync(join(records, file), "not canonical evidence\n", { mode: 0o600 });
    assert.deepEqual(s.application.readiness(), { status: "blocked", new_claims_available: false });
    expectError(() => s.application.query(request(s.application), CONTEXT), "unavailable");
    expectError(() => s.application.inspect({ receipt_id: result.evidence.receipt.receipt_id }), "unavailable");
  } finally { s.close(); }
});

test("copied index, foreign ledger and substituted capture cannot construct the application", () => {
  const s = scenario(); const foreign = scenario();
  try {
    const options = { ledger: s.ledger, reconciliationIndex: s.reconciliationIndex, projection: PROJECTION, software: SOFTWARE, now: NOW };
    assert.throws(() => createWeb216CpihApplication({ ...options, reconciliationIndex: { ...s.reconciliationIndex } }));
    assert.throws(() => createWeb216CpihApplication({ ...options, ledger: foreign.ledger }));
    assert.throws(() => createWeb216CpihApplication({ ...options, projection: {} }));
    assert.throws(() => createWeb216CpihApplication({ ...options, get projection() { throw Error("Do not execute getter"); } }));
    assert.throws(() => createWeb216CpihApplication({ ...options, [Symbol("authority")]: "allow" }));
    assert.throws(() => createWeb216CpihApplication(Object.defineProperty({ ...options }, "projection", { value: PROJECTION, enumerable: false })));
    assert.equal(s.ledger.verify().event_count, 0);
  } finally { s.close(); foreign.close(); }
});

test("a full ledger blocks new claims but preserves replay and inspection", () => {
  const s = scenario(1);
  try {
    const first = s.application.query(request(s.application), CONTEXT);
    assert.deepEqual(s.application.readiness(), { status: "blocked", new_claims_available: false });
    expectError(() => s.application.query(request(s.application, "2026-01", SECOND_KEY), CONTEXT), "unavailable");
    assert.equal(s.reconciliationIndex.verify().claim_count, 1);
    assert.equal(s.reconciliationIndex.verify().pending_count, 0);
    assert.deepEqual(s.application.query(request(s.application), { ...CONTEXT, requestId: "capacity-retry" }), first);
    assert.deepEqual(s.application.inspect({ receipt_id: first.evidence.receipt.receipt_id }), first);
  } finally { s.close(); }
});
