import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import {
  buildWeb216CpihReceipt, buildWeb216CpihResult, openPublicEvidenceLedger,
  openWeb216CpihReconciliationIndex, verifyStoredPublicEvidenceProjection, verifyWeb216CpihReceipt,
} from "@gis-ai-go/evidence";
import { EvidenceInspectError, createEvidenceInspectApplication } from "../src/evidence-application.js";

const PROJECTION = JSON.parse(readFileSync(new URL(
  "../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url,
), "utf8"));
const NOW = new Date("2026-09-14T17:00:00.000Z");
const SOFTWARE = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) } as const;

test("legacy receipt-id inspection refuses genuine stored CPIH data without changing its ledger", () => {
  for (const period of ["2026-01", "2026-07"] as const) {
    const root = mkdtempSync(join(tmpdir(), "gis-ai-go-cpih-legacy-app-"));
    try {
      const ledger = openPublicEvidenceLedger({ rootDirectory: root, retentionDays: 30, now: () => NOW });
      const receipt = buildWeb216CpihReceipt({ projection: PROJECTION, period,
        requestId: "cpih-source-application-test", traceId: "1".repeat(32),
        createdAt: NOW.toISOString(), software: SOFTWARE });
      const material = { projection: PROJECTION, normalisedParameters: { period },
        resultCore: buildWeb216CpihResult(PROJECTION, period), expectedSoftware: SOFTWARE };
      assert.equal(verifyWeb216CpihReceipt(receipt, material).valid, true);
      const persisted = ledger.persistReceipt(receipt, material);
      assert.equal(persisted.record.schema, "gis-ai-go.public-evidence-record.v3");
      const reopened = openPublicEvidenceLedger({ rootDirectory: root, retentionDays: 30, now: () => NOW });
      const stored = reopened.inspect(receipt.receipt_id);
      assert.ok(stored);
      assert.equal(verifyStoredPublicEvidenceProjection(stored), true);
      const before = reopened.verify();
      const application = createEvidenceInspectApplication(reopened, undefined,
        { software: SOFTWARE, now: () => NOW });
      assert.throws(() => application.inspect({ receipt_id: receipt.receipt_id }, {
        requestId: "legacy-inspection-application-test", traceId: "2".repeat(32),
      }), (error: unknown) => error instanceof EvidenceInspectError && error.code === "evidence_unavailable");
      assert.deepEqual(reopened.verify(), before);
      assert.deepEqual(reopened.inspect(receipt.receipt_id), stored);
    } finally { rmSync(root, { recursive: true, force: true }); }
  }
});

test("legacy inspector cannot accept the separately branded CPIH reconciliation capability", () => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-cpih-legacy-index-"));
  try {
    const ledger = openPublicEvidenceLedger({ rootDirectory: join(parent, "ledger"), now: () => NOW });
    const index = openWeb216CpihReconciliationIndex({ rootDirectory: join(parent, "index"), ledger, now: () => NOW });
    assert.throws(() => createEvidenceInspectApplication(ledger, index as never,
      { software: SOFTWARE, now: () => NOW }), /exact linked ledger and index/u);
    assert.equal(index.verify().claim_count, 0);
    assert.equal(ledger.verify().event_count, 0);
  } finally { rmSync(parent, { recursive: true, force: true }); }
});
