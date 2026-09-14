import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import {
  buildWeb216CpihReceipt, buildWeb216CpihResult, isRestartVerifiedStoredPublicEvidence,
  openPublicEvidenceLedger, verifyStoredPublicEvidenceProjection, verifyWeb216CpihReceipt,
  type Web216CpihPeriod,
} from "@gis-ai-go/evidence";
import { evaluateEvidenceInspectionPolicy } from "../src/evidence-inspect-v3.js";

const PROJECTION = JSON.parse(readFileSync(new URL(
  "../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url,
), "utf8"));
const NOW = new Date("2026-09-14T17:00:00.000Z");
const SOFTWARE = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) } as const;

test("legacy inspection policy denies both genuine, restart-verified stored CPIH observations", () => {
  for (const period of ["2026-01", "2026-07"] as const satisfies readonly Web216CpihPeriod[]) {
    const root = mkdtempSync(join(tmpdir(), "gis-ai-go-cpih-legacy-policy-"));
    try {
      const ledger = openPublicEvidenceLedger({ rootDirectory: root, retentionDays: 30, now: () => NOW });
      const receipt = buildWeb216CpihReceipt({ projection: PROJECTION, period,
        requestId: "cpih-source-policy-test", traceId: "1".repeat(32),
        createdAt: NOW.toISOString(), software: SOFTWARE });
      const material = { projection: PROJECTION, normalisedParameters: { period },
        resultCore: buildWeb216CpihResult(PROJECTION, period), expectedSoftware: SOFTWARE };
      assert.equal(verifyWeb216CpihReceipt(receipt, material).valid, true);
      ledger.persistReceipt(receipt, material);
      const reopened = openPublicEvidenceLedger({ rootDirectory: root, retentionDays: 30, now: () => NOW });
      const stored = reopened.inspect(receipt.receipt_id);
      assert.ok(stored);
      assert.equal(stored.record.schema, "gis-ai-go.public-evidence-record.v3");
      assert.equal(isRestartVerifiedStoredPublicEvidence(stored), true);
      assert.equal(verifyStoredPublicEvidenceProjection(stored), true);
      const before = reopened.verify();
      const denied = evaluateEvidenceInspectionPolicy({
        requestId: "legacy-inspection-policy-test", traceId: "2".repeat(32),
        operation: "evidence.inspect", verifiedStoredEvidence: stored,
      });
      assert.equal(denied.allowed, false);
      assert.equal(denied.decision.effect, "deny");
      assert.equal(denied.decision.inspected_receipt_id, null);
      assert.deepEqual(denied.decision.obligations, []);
      assert.deepEqual(reopened.verify(), before);
    } finally { rmSync(root, { recursive: true, force: true }); }
  }
});
