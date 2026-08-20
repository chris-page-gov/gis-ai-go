import assert from "node:assert/strict";
import {
  cpSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  PublicEvidenceLedgerError,
  buildInlineReceipt,
  buildPublicReadReceipt,
  openPublicEvidenceLedger,
} from "../src/index.js";
import { makeReceiptBuildInput } from "./fixtures.js";
import {
  makePublicReadReceiptBuildInput,
  makePublicReadReceiptFixture,
} from "./public-read-fixtures.js";

const PERSISTED_AT = new Date("2026-08-20T12:00:00.000Z");

function temporaryDirectory(): string {
  return mkdtempSync(join(tmpdir(), "gis-ai-go-public-read-ledger-"));
}

function expectLedgerError(
  run: () => unknown,
  code: PublicEvidenceLedgerError["code"],
): void {
  assert.throws(run, (error: unknown) => {
    assert.ok(error instanceof PublicEvidenceLedgerError);
    assert.equal(error.code, code);
    return true;
  });
}

test("preserves v1 identities and restarts a mixed v1 and v2 ledger", () => {
  const root = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger({
      rootDirectory: root,
      retentionDays: 30,
      now: () => PERSISTED_AT,
    });
    const v1Input = makeReceiptBuildInput();
    const v1Receipt = buildInlineReceipt(v1Input);
    assert.equal(
      v1Receipt.receipt_id,
      "gis-ai-go:evidence-receipt:sha256:a70f8e6f752de3a6128989e8f88dab448b55aeac76831462e56b5f236be3f033",
    );
    const v1 = ledger.persistReceipt(v1Receipt, {
      normalisedParameters: v1Input.normalisedParameters,
      resultCore: v1Input.resultCore,
      publicPolicy: v1Input.publicPolicy,
      licenceObligations: v1Input.licenceObligations,
      expectedAuthorityContext: v1Input.authorityContext,
      expectedPolicyDecision: v1Input.policyDecision,
      expectedCatalogue: v1Input.catalogue,
      expectedSoftware: v1Input.software,
    });
    assert.equal(v1.record.schema, "gis-ai-go.public-evidence-record.v1");
    assert.equal(
      v1.record.record_id,
      "gis-ai-go:public-evidence-record:sha256:f4afb5dcffb1ed6ad9a878633c6139b26787f69c2fb69a286a0d18052c8460ea",
    );
    assert.equal(
      v1.event.event_id,
      "gis-ai-go:evidence-ledger-event:sha256:a170a3be16c911fe477972ed8d24b3c462f3d95a02f2ab16a48a6858c7dc12ca",
    );

    const v2Fixture = makePublicReadReceiptFixture(
      "data.query",
      "request-public-read-ledger-2",
      "3123456789abcdef0123456789abcdef",
    );
    const v2 = ledger.persistReceipt(v2Fixture.receipt, v2Fixture.material);
    assert.equal(v2.record.schema, "gis-ai-go.public-evidence-record.v2");
    assert.equal(v2.event.sequence, 2);
    assert.equal(v2.event.previous_event_id, v1.event.event_id);

    const restarted = openPublicEvidenceLedger({
      rootDirectory: root,
      retentionDays: 30,
      now: () => new Date("2027-08-20T12:00:00.000Z"),
    });
    assert.deepEqual(restarted.verify(), {
      status: "verified",
      ledger_id: ledger.descriptor.ledger_id,
      event_count: 2,
      record_count: 2,
      last_event_id: v2.event.event_id,
      checks: [
        "descriptor",
        "canonical-files",
        "content-identities",
        "event-sequence",
        "hash-chain",
        "receipt-boundary",
        "replay-keys",
        "retention",
        "privacy",
      ],
    });
    assert.deepEqual(restarted.inspect(v1Receipt.receipt_id), v1);
    assert.deepEqual(restarted.inspect(v2Fixture.receipt.receipt_id), v2);

    const storedBytes = readdirSync(join(root, "records"))
      .map((name) => readFileSync(join(root, "records", name), "utf8"))
      .join("\n");
    assert.equal(storedBytes.includes("raw-observation-value-should-not-appear"), false);
    assert.equal(storedBytes.includes("phrase retained only in digest material"), false);
    assert.equal(storedBytes.includes("/Users/"), false);
    assert.equal(storedBytes.includes("Bearer "), false);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("rejects v2 wrong material, exact replay and semantic replay", () => {
  const root = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger({
      rootDirectory: root,
      retentionDays: 30,
      now: () => PERSISTED_AT,
    });
    const fixture = makePublicReadReceiptFixture("selection.resolve");
    expectLedgerError(
      () =>
        ledger.persistReceipt(fixture.receipt, {
          ...fixture.material,
          normalisedParameters: { wrong: true },
        }),
      "invalid-receipt",
    );
    ledger.persistReceipt(fixture.receipt, fixture.material);
    expectLedgerError(
      () => ledger.persistReceipt(fixture.receipt, fixture.material),
      "replay",
    );

    const reissuedInput = makePublicReadReceiptBuildInput("selection.resolve");
    const reissued = buildPublicReadReceipt({
      ...reissuedInput,
      createdAt: "2026-08-20T18:00:01Z",
    });
    expectLedgerError(
      () =>
        ledger.persistReceipt(reissued, {
          normalisedParameters: reissuedInput.normalisedParameters,
          resultCore: reissuedInput.resultCore,
          publicPolicy: reissuedInput.publicPolicy,
        }),
      "replay",
    );
    assert.equal(ledger.verify().event_count, 1);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("rejects proxied v2 receipts and material before ledger dispatch", () => {
  const root = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger({
      rootDirectory: root,
      retentionDays: 30,
      now: () => PERSISTED_AT,
    });
    const fixture = makePublicReadReceiptFixture("data.query");
    let reads = 0;
    const receipt = new Proxy(fixture.receipt, {
      get(target, property, receiver) {
        reads += 1;
        return Reflect.get(target, property, receiver);
      },
    });
    expectLedgerError(
      () => ledger.persistReceipt(receipt, fixture.material),
      "invalid-receipt",
    );
    assert.equal(reads, 0);

    const material = new Proxy(fixture.material, {
      get(target, property, receiver) {
        reads += 1;
        return Reflect.get(target, property, receiver);
      },
    });
    expectLedgerError(
      () => ledger.persistReceipt(fixture.receipt, material),
      "invalid-receipt",
    );
    assert.equal(reads, 0);
    assert.equal(ledger.verify().event_count, 0);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("detects v2 record tampering after restart", () => {
  const root = temporaryDirectory();
  const corrupt = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger({
      rootDirectory: root,
      retentionDays: 30,
      now: () => PERSISTED_AT,
    });
    const fixture = makePublicReadReceiptFixture("data.query");
    const stored = ledger.persistReceipt(fixture.receipt, fixture.material);
    cpSync(root, corrupt, { recursive: true });
    const recordPath = join(
      corrupt,
      "records",
      `${stored.record.record_id.slice(-64)}.json`,
    );
    writeFileSync(
      recordPath,
      readFileSync(recordPath, "utf8").replace("Open Government Licence v3.0", "Unknown"),
    );
    expectLedgerError(
      () => openPublicEvidenceLedger({ rootDirectory: corrupt, retentionDays: 30 }),
      "corruption",
    );
  } finally {
    rmSync(root, { recursive: true, force: true });
    rmSync(corrupt, { recursive: true, force: true });
  }
});
