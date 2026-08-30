#!/usr/bin/env node

import process from "node:process";
import { join } from "node:path";

import {
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
} from "../packages/evidence/dist/src/index.js";
import {
  PUBLIC_READ_REQUEST_ID,
  PUBLIC_READ_TRACE_ID,
  makePublicReadReceiptFixture,
} from "../packages/evidence/dist/test/public-read-fixtures.js";
import { parseClosedArguments } from "./evidence_checkpoint_operator_common.mjs";

const KEY = `gis-ai-go:ik:v1:${"1".repeat(64)}`;
const parsed = parseClosedArguments(process.argv.slice(2), ["--root-directory"], []);
if (parsed === null) {
  process.exitCode = 2;
} else {
  try {
    const root = parsed.values.get("--root-directory");
    const ledger = openPublicEvidenceLedger({
      rootDirectory: join(root, "ledger"),
      retentionDays: 30,
      now: () => new Date("2026-08-30T08:00:00.000Z"),
    });
    const reconciliationIndex = openEvidenceReconciliationIndex({
      rootDirectory: join(root, "reconciliation-index"),
      ledger,
      now: () => new Date("2026-08-30T08:00:00.000Z"),
    });
    const fixture = makePublicReadReceiptFixture();
    const claim = reconciliationIndex.claim({
      idempotencyKey: KEY,
      operation: "data.query",
      requestId: PUBLIC_READ_REQUEST_ID,
      traceId: PUBLIC_READ_TRACE_ID,
      resourceId: fixture.receipt.resource.resource_id,
      normalisedParametersSha256: fixture.receipt.operation.normalised_parameters.sha256,
    });
    if (claim.status !== "claimed") throw new Error("fixture claim was not acquired");
    reconciliationIndex.resolve(claim.claim, fixture.receipt);
    ledger.persistReceipt(fixture.receipt, fixture.material);
    if (reconciliationIndex.lookup(KEY).status !== "completed") {
      throw new Error("fixture resolution did not complete");
    }
  } catch {
    process.exitCode = 1;
  }
}
