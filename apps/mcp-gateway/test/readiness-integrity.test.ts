import assert from "node:assert/strict";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
} from "@gis-ai-go/evidence";

import type { CatalogueSnapshot } from "../src/catalogue-snapshot.js";
import { createGatewayHttpHandler } from "../src/http-app.js";
import {
  EVIDENCE_READINESS_INTEGRITY_FAILURE_MESSAGE,
  EVIDENCE_READINESS_INTEGRITY_KIND,
  createEvidenceReadinessIntegrity,
  verifyEvidenceReadinessIntegrity,
  type EvidenceReadinessIntegrity,
} from "../src/readiness-integrity.js";

const SNAPSHOT = {
  bundle: { records: [] },
  recordsById: new Map(),
  version: "0.1.0",
  revision: "a".repeat(40),
  contentRootSha256: "b".repeat(64),
  manifestSha256: "c".repeat(64),
  recordCount: 36,
  stale: false,
  warnings: Object.freeze([]),
  root: "/verified/catalogue",
} as unknown as CatalogueSnapshot;

function request(path: string): Request {
  return new Request(`http://127.0.0.1:8787${path}`, {
    headers: { host: "127.0.0.1:8787" },
  });
}

function errorMessages(errors: readonly Error[]): readonly string[] {
  return errors.map((error) => error.message);
}

test("re-verifies configured evidence storage on every readiness evaluation", async (t) => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-readiness-integrity-"));
  t.after(() => rmSync(parent, { recursive: true, force: true }));
  const ledgerRoot = join(parent, "ledger");
  const ledger = openPublicEvidenceLedger({
    rootDirectory: ledgerRoot,
    retentionDays: 365,
    now: () => new Date("2026-08-23T12:00:00.000Z"),
  });
  const reconciliationIndex = openEvidenceReconciliationIndex({
    rootDirectory: join(parent, "reconciliation"),
    ledger,
  });
  const integrity = createEvidenceReadinessIntegrity(ledger, reconciliationIndex);
  const reported: Error[] = [];
  const replacedReports: Error[] = [];
  const mutableOptions = {
    snapshot: SNAPSHOT,
    evidenceReadinessIntegrity: integrity,
    createTraceId: () => "7".repeat(32),
    createTraceParentId: () => "8".repeat(16),
    onerror: (error: Error) => reported.push(error),
  };
  const handle = createGatewayHttpHandler(mutableOptions);
  assert.equal(Reflect.set(mutableOptions, "evidenceReadinessIntegrity", undefined), true);
  assert.equal(
    Reflect.set(mutableOptions, "onerror", (error: Error) => replacedReports.push(error)),
    true,
  );

  const expected = {
    status: "blocked",
    reason: "transport-and-interoperability-unverified",
    active_tools: [],
    active_api_operations: [],
  };
  const first = await handle(request("/readyz"));
  assert.equal(first.status, 503);
  assert.deepEqual(await first.json(), expected);
  assert.deepEqual(reported, []);

  writeFileSync(join(ledgerRoot, "ledger.json"), "{}\n", { mode: 0o600 });
  const second = await handle(request("/readyz"));
  assert.equal(second.status, 503);
  assert.deepEqual(await second.json(), expected);
  assert.equal(reported.length, 1);
  assert.deepEqual(errorMessages(reported), [
    EVIDENCE_READINESS_INTEGRITY_FAILURE_MESSAGE,
  ]);
  assert.deepEqual(replacedReports, []);
  assert.equal(JSON.stringify(reported).includes(parent), false);

  const health = await handle(request("/healthz"));
  assert.equal(health.status, 200);
  assert.equal(reported.length, 1);
});

test("accepts only the branded exact linked evidence pair", (t) => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-readiness-brand-"));
  t.after(() => rmSync(parent, { recursive: true, force: true }));
  const firstLedger = openPublicEvidenceLedger({
    rootDirectory: join(parent, "first-ledger"),
    retentionDays: 365,
  });
  const secondLedger = openPublicEvidenceLedger({
    rootDirectory: join(parent, "second-ledger"),
    retentionDays: 365,
  });
  const index = openEvidenceReconciliationIndex({
    rootDirectory: join(parent, "reconciliation"),
    ledger: firstLedger,
  });
  const integrity = createEvidenceReadinessIntegrity(firstLedger, index);
  assert.equal(integrity.kind, EVIDENCE_READINESS_INTEGRITY_KIND);
  assert.equal(Object.isFrozen(integrity), true);
  verifyEvidenceReadinessIntegrity(integrity);
  assert.throws(
    () => createEvidenceReadinessIntegrity(secondLedger, index),
    /exact linked evidence ledger/u,
  );

  assert.throws(() => Object.defineProperty(firstLedger, "verify", { value: () => [] }));
  assert.throws(() => Object.defineProperty(index, "verify", { value: () => [] }));
  verifyEvidenceReadinessIntegrity(integrity);

  let substitutedInspectionCalls = 0;
  assert.throws(
    () => Object.defineProperty(firstLedger, "inspectReceipts", {
      value: () => {
        substitutedInspectionCalls += 1;
        return [];
      },
    }),
  );
  assert.equal(substitutedInspectionCalls, 0);
  verifyEvidenceReadinessIntegrity(integrity);

  assert.throws(
    () => Object.defineProperty(index, "ledger", { value: secondLedger }),
  );

  for (const invalid of [
    { kind: EVIDENCE_READINESS_INTEGRITY_KIND },
    new Proxy(integrity, {}),
  ] as unknown as EvidenceReadinessIntegrity[]) {
    assert.throws(
      () => verifyEvidenceReadinessIntegrity(invalid),
      /integrity seam is invalid/u,
    );
  }
});
