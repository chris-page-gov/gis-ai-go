import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { openPublicEvidenceLedger, PublicEvidenceLedgerError } from "../src/public-ledger.js";
import {
  PUBLIC_EVIDENCE_LEDGER_MAX_EVENTS, withLowerPublicEvidenceLedgerEventLimitForTest,
} from "../src/public-ledger-capacity.js";
import { makePublicReadReceiptFixture } from "./public-read-fixtures.js";

const NOW = new Date("2026-09-14T17:00:00.000Z");
function withRoot(run: (root: string) => void) {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-append-capacity-"));
  try { run(root); } finally { rmSync(root, { recursive: true, force: true }); }
}
function options(root: string, maximum?: number) {
  const value = { rootDirectory: root, retentionDays: 30, now: () => NOW };
  return maximum === undefined ? value : withLowerPublicEvidenceLedgerEventLimitForTest(value, maximum);
}
function fixture(sequence: number) {
  return makePublicReadReceiptFixture("data.query", `append-capacity-${sequence}`,
    sequence.toString(16).padStart(32, "0"));
}

test("default append capacity exposes the fixed limit without adding or modifying evidence", () => {
  withRoot((root) => {
    const ledger = openPublicEvidenceLedger(options(root));
    const before = readFileSync(join(root, "ledger.json"), "utf8");
    const capacity = ledger.appendCapacity();
    assert.deepEqual(capacity, { status: "available", maximum_events: PUBLIC_EVIDENCE_LEDGER_MAX_EVENTS,
      event_count: 0, remaining_events: PUBLIC_EVIDENCE_LEDGER_MAX_EVENTS });
    assert.equal(Object.isFrozen(capacity), true);
    assert.equal(readFileSync(join(root, "ledger.json"), "utf8"), before);
    assert.deepEqual(readdirSync(join(root, "events")), []);
    assert.deepEqual(readdirSync(join(root, "records")), []);
  });
});

test("lowered-limit capacity tracks verified appends and restart without claiming a reservation", () => {
  withRoot((root) => {
    const ledger = openPublicEvidenceLedger(options(root, 2));
    const first = fixture(1); const second = fixture(2); const third = fixture(3);
    ledger.persistReceipt(first.receipt, first.material);
    const previous = ledger.appendCapacity();
    assert.deepEqual(previous, { status: "available", maximum_events: 2, event_count: 1, remaining_events: 1 });
    ledger.persistReceipt(second.receipt, second.material);
    const exhausted = { status: "exhausted", maximum_events: 2, event_count: 2, remaining_events: 0 };
    assert.deepEqual(ledger.appendCapacity(), exhausted);
    assert.equal(previous.remaining_events, 1); // Immutable earlier snapshot, not a held slot.
    assert.deepEqual(openPublicEvidenceLedger(options(root, 2)).appendCapacity(), exhausted);
    const events = readdirSync(join(root, "events"));
    const records = readdirSync(join(root, "records"));
    assert.throws(() => ledger.persistReceipt(third.receipt, third.material),
      (error: unknown) => error instanceof PublicEvidenceLedgerError && error.code === "capacity");
    assert.deepEqual(readdirSync(join(root, "events")), events);
    assert.deepEqual(readdirSync(join(root, "records")), records);
    assert.ok(ledger.inspect(first.receipt.receipt_id));
    assert.deepEqual(openPublicEvidenceLedger(options(root, 1)).appendCapacity(),
      { status: "exhausted", maximum_events: 1, event_count: 2, remaining_events: 0 });
  });
});

test("append capacity fails closed on corrupted or missing committed evidence", () => {
  withRoot((root) => {
    const ledger = openPublicEvidenceLedger(options(root, 2));
    const first = fixture(1);
    ledger.persistReceipt(first.receipt, first.material);
    const eventPath = join(root, "events", readdirSync(join(root, "events"))[0]!);
    writeFileSync(eventPath, "{", { mode: 0o600 });
    assert.throws(() => ledger.appendCapacity(), PublicEvidenceLedgerError);
    rmSync(eventPath);
    assert.throws(() => ledger.appendCapacity(), PublicEvidenceLedgerError);
  });
});
