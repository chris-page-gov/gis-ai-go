import assert from "node:assert/strict";
import fs, {
  chmodSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { syncBuiltinESMExports } from "node:module";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  CANONICAL_DOMAINS,
  PublicEvidenceLedgerError,
  WEB216_CPIH_DOMAINS,
  buildInlineReceipt,
  buildWeb216CpihReceipt,
  buildWeb216CpihResult,
  canonicalJson,
  contentAddress,
  domainSeparatedSha256,
  isRestartVerifiedStoredPublicEvidence,
  openPublicEvidenceLedger,
  verifyStoredPublicEvidenceProjection,
  type PublicEvidenceReceipt,
  type StoredPublicEvidence,
  type Web216CpihPeriod,
  type Web216CpihReceiptBuildInput,
  type Web216CpihReceiptVerificationMaterial,
} from "../src/index.js";
import { withLowerPublicEvidenceLedgerEventLimitForTest } from "../src/public-ledger-capacity.js";
import { makeReceiptBuildInput } from "./fixtures.js";
import { makePublicReadReceiptFixture } from "./public-read-fixtures.js";

const PERSISTED_AT = new Date("2026-09-14T17:00:00.000Z");
const PROJECTION: unknown = JSON.parse(readFileSync(new URL(
  "../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url,
), "utf8"));

function fixture(selected: Web216CpihPeriod = "2026-07", sequence = 1) {
  const input: Web216CpihReceiptBuildInput = {
    period: selected,
    projection: structuredClone(PROJECTION),
    requestId: `web216-ledger-test-${sequence}`,
    traceId: sequence.toString(16).padStart(32, "0"),
    createdAt: "2026-09-14T16:00:00.000Z",
    software: { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) },
  };
  const receipt = buildWeb216CpihReceipt(input);
  const material: Web216CpihReceiptVerificationMaterial = {
    projection: input.projection,
    normalisedParameters: { period: selected },
    resultCore: buildWeb216CpihResult(input.projection, selected),
    expectedSoftware: input.software,
  };
  return { input, receipt, material };
}

function temporaryDirectory(): string {
  return mkdtempSync(join(tmpdir(), "gis-ai-go-cpih-ledger-"));
}

function options(root: string) {
  return { rootDirectory: root, retentionDays: 30, now: () => PERSISTED_AT };
}

function expectError(run: () => unknown, code: PublicEvidenceLedgerError["code"]): void {
  assert.throws(run, (error: unknown) => {
    assert.ok(error instanceof PublicEvidenceLedgerError);
    assert.equal(error.code, code);
    return true;
  });
}

function snapshot(root: string): string {
  return canonicalJson(["records", "events"].map((directory) => ({
    directory,
    files: readdirSync(join(root, directory)).sort().map((name) => ({
      name, bytes: readFileSync(join(root, directory, name), "utf8"),
    })),
  })));
}

function recordPath(root: string, stored: StoredPublicEvidence): string {
  return join(root, "records", `${stored.record.record_id.slice(-64)}.json`);
}

test("persists a separate v3 wrapper, reopens and inspects both exact captured months", () => {
  const root = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger(options(root));
    const july = fixture();
    const first = ledger.persistReceipt(july.receipt, july.material);
    const january = fixture("2026-01", 2);
    const second = ledger.persistReceipt(january.receipt, january.material);
    assert.equal(first.record.schema, "gis-ai-go.public-evidence-record.v3");
    assert.deepEqual(first.record.receipt, july.receipt);
    assert.equal(first.record.receipt.evidence.persistence, "not-persisted");
    assert.equal(first.record.receipt.evidence.attestation, "not-attested");
    assert.equal(first.record.verification.receipt, "full-material-verified-at-ingest");
    assert.equal(first.record.verification.restart, "structure-and-content-verified");
    assert.equal(first.reference.status, "persisted");
    assert.equal(first.reference.persisted_at, "2026-09-14T17:00:00.000Z");
    assert.equal(first.reference.retain_until, "2026-10-14T17:00:00.000Z");
    assert.equal(first.event.schema, "gis-ai-go.evidence-ledger-event.v1");
    assert.equal(second.event.previous_event_id, first.event.event_id);
    const { record_id: identity, ...core } = first.record;
    assert.equal(identity, contentAddress(
      "gis-ai-go:public-evidence-record", CANONICAL_DOMAINS.publicEvidenceRecordV3, core,
    ));
    assert.notEqual(identity, contentAddress(
      "gis-ai-go:public-evidence-record", CANONICAL_DOMAINS.publicEvidenceRecordV2, core,
    ));
    const reopened = openPublicEvidenceLedger(options(root));
    assert.equal(reopened.verify().event_count, 2);
    assert.equal(reopened.verify().record_count, 2);
    const inspected = reopened.inspect(july.receipt.receipt_id);
    assert.deepEqual(inspected, first);
    assert.equal(isRestartVerifiedStoredPublicEvidence(inspected), true);
    assert.equal(isRestartVerifiedStoredPublicEvidence(structuredClone(inspected)), false);
    assert.equal(verifyStoredPublicEvidenceProjection(inspected), true);
    assert.deepEqual(reopened.inspect(first.record.record_id), first);
    assert.deepEqual(reopened.inspectReceipts([
      july.receipt.receipt_id, january.receipt.receipt_id,
    ]), [first, second]);
    const bytes = snapshot(root);
    assert.equal(bytes.includes("2026 JUL"), false);
    assert.equal(bytes.includes('"value":"142.7"'), false);
    assert.equal(bytes.includes("contacts"), false);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test("v1 and v2 remain separate, identity-stable members of a mixed-family ledger", () => {
  const root = temporaryDirectory();
  try {
    let now = new Date("2026-08-20T12:00:00.000Z");
    const ledger = openPublicEvidenceLedger({ ...options(root), now: () => now });
    const v1Input = makeReceiptBuildInput();
    const v1Receipt = buildInlineReceipt(v1Input);
    const first = ledger.persistReceipt(v1Receipt, {
      normalisedParameters: v1Input.normalisedParameters,
      resultCore: v1Input.resultCore,
      publicPolicy: v1Input.publicPolicy,
      licenceObligations: v1Input.licenceObligations,
      expectedAuthorityContext: v1Input.authorityContext,
      expectedPolicyDecision: v1Input.policyDecision,
      expectedCatalogue: v1Input.catalogue,
      expectedSoftware: v1Input.software,
    });
    assert.equal(first.record.record_id,
      "gis-ai-go:public-evidence-record:sha256:f4afb5dcffb1ed6ad9a878633c6139b26787f69c2fb69a286a0d18052c8460ea");
    assert.equal(first.event.event_id,
      "gis-ai-go:evidence-ledger-event:sha256:a170a3be16c911fe477972ed8d24b3c462f3d95a02f2ab16a48a6858c7dc12ca");
    const v2 = makePublicReadReceiptFixture("data.query");
    const second = ledger.persistReceipt(v2.receipt, v2.material);
    assert.equal(second.record.schema, "gis-ai-go.public-evidence-record.v2");
    const beforeV3 = [first, second].map((stored) => readFileSync(recordPath(root, stored), "utf8"));
    now = PERSISTED_AT;
    const v3 = fixture();
    const third = ledger.persistReceipt(v3.receipt, v3.material);
    assert.equal(third.event.previous_event_id, second.event.event_id);
    const reopened = openPublicEvidenceLedger(options(root));
    assert.equal(reopened.verify().record_count, 3);
    for (const [index, stored] of [first, second].entries()) {
      assert.equal(readFileSync(recordPath(root, stored), "utf8"), beforeV3[index]);
      assert.deepEqual(reopened.inspect(stored.record.receipt.receipt_id), stored);
    }
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test("full-material ingest rejects absent, substituted and wrong-family material before any write", () => {
  const root = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger(options(root));
    const { receipt, material } = fixture();
    const before = snapshot(root);
    const alternatives = [
      { ...material, projection: { projection_sha256: receipt.capture.projection_sha256 } },
      { ...material, normalisedParameters: { period: "2026-01" as const } },
      { ...material, resultCore: { ...material.resultCore, provider_egress: true } },
      { ...material, expectedSoftware: { ...material.expectedSoftware, revision: "b".repeat(40) } },
      makePublicReadReceiptFixture("data.query").material,
    ];
    for (const alternative of alternatives) {
      expectError(() => ledger.persistReceipt(
        receipt, alternative as Web216CpihReceiptVerificationMaterial,
      ), "invalid-receipt");
      assert.equal(snapshot(root), before);
    }
    for (const unknown of [null, { ...receipt, schema: "gis-ai-go.evidence-receipt.v999" }]) {
      expectError(() => ledger.persistReceipt(
        unknown as unknown as PublicEvidenceReceipt, material,
      ), "invalid-receipt");
    }
    assert.equal(snapshot(root), before);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test("schema-bound replay keys reject reissued bindings without overwriting immutable records", () => {
  const root = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger(options(root));
    const { receipt, material, input } = fixture();
    const stored = ledger.persistReceipt(receipt, material);
    const before = snapshot(root);
    const binding = {
      request_id: receipt.request_id,
      trace_id: receipt.trace_id,
      operation: receipt.operation.name,
      normalised_parameters_sha256: receipt.operation.normalised_parameters.sha256,
      result_sha256: receipt.result.sha256,
    };
    assert.equal(stored.event.replay_key_sha256, domainSeparatedSha256(
      CANONICAL_DOMAINS.evidenceReplayKey, { receipt_schema: receipt.schema, ...binding },
    ));
    assert.notEqual(stored.event.replay_key_sha256,
      domainSeparatedSha256(CANONICAL_DOMAINS.evidenceReplayKey, binding));
    expectError(() => ledger.persistReceipt(receipt, material), "replay");
    const reissued = buildWeb216CpihReceipt({ ...input, createdAt: "2026-09-14T16:00:01.000Z" });
    assert.notEqual(reissued.receipt_id, receipt.receipt_id);
    expectError(() => ledger.persistReceipt(reissued, material), "replay");
    assert.equal(snapshot(root), before);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test("restart and portable inspection reject corrupt v3 content and family relabelling", () => {
  const root = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger(options(root));
    const { receipt, material } = fixture();
    const stored = ledger.persistReceipt(receipt, material);
    for (const schema of ["gis-ai-go.public-evidence-record.v2", "gis-ai-go.public-evidence-record.v999"]) {
      const changed = structuredClone(stored) as unknown as {
        record: Record<string, unknown>; event: unknown; reference: unknown;
      };
      changed.record.schema = schema;
      const { record_id: _old, ...core } = changed.record;
      changed.record.record_id = contentAddress(
        "gis-ai-go:public-evidence-record", CANONICAL_DOMAINS.publicEvidenceRecordV2, core,
      );
      assert.equal(verifyStoredPublicEvidenceProjection(changed), false);
    }
    const path = recordPath(root, stored);
    writeFileSync(path, readFileSync(path, "utf8").replace("not-attested", "self-attested"));
    expectError(() => openPublicEvidenceLedger(options(root)), "corruption");
    expectError(() => ledger.inspect(receipt.receipt_id), "corruption");
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test("a completely rehashed forged authority is still rejected at restart", () => {
  const root = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger(options(root));
    const { receipt, material } = fixture();
    const stored = ledger.persistReceipt(receipt, material);
    const { receipt_id: _receiptId, ...receiptCore } = structuredClone(receipt);
    const forgedCore = { ...receiptCore, policy_scope: { ...receiptCore.policy_scope, provider_egress: true } };
    const forgedReceipt = { ...forgedCore, receipt_id: contentAddress(
      "gis-ai-go:evidence-receipt", WEB216_CPIH_DOMAINS.receipt, forgedCore,
    ) };
    expectError(() => ledger.persistReceipt(
      forgedReceipt as unknown as PublicEvidenceReceipt, material,
    ), "invalid-receipt");
    const { record_id: _recordId, ...recordCore } = stored.record;
    const forgedRecordCore = { ...recordCore, receipt: forgedReceipt };
    const forgedRecord = { ...forgedRecordCore, record_id: contentAddress(
      "gis-ai-go:public-evidence-record", CANONICAL_DOMAINS.publicEvidenceRecordV3, forgedRecordCore,
    ) };
    // Replace only this test's generated record; its filename also matches the
    // forged hash, so restart must reject the receipt boundary, not just a name.
    rmSync(recordPath(root, stored));
    writeFileSync(join(root, "records", `${forgedRecord.record_id.slice(-64)}.json`),
      `${canonicalJson(forgedRecord)}\n`, { flag: "wx", mode: 0o600 });
    expectError(() => openPublicEvidenceLedger(options(root)), "corruption");
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test("new-family storage retains capacity, retention and private-file checks", () => {
  const root = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger(withLowerPublicEvidenceLedgerEventLimitForTest(options(root), 1));
    const first = fixture();
    const stored = ledger.persistReceipt(first.receipt, first.material);
    const before = snapshot(root);
    const second = fixture("2026-01", 2);
    expectError(() => ledger.persistReceipt(second.receipt, second.material), "capacity");
    assert.equal(snapshot(root), before);
    expectError(() => openPublicEvidenceLedger({ ...options(root), retentionDays: 31 }), "retention-mismatch");
    if (process.platform !== "win32") {
      chmodSync(recordPath(root, stored), 0o644);
      expectError(() => openPublicEvidenceLedger(options(root)), "corruption");
    }
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test("failed immutable writes never return a persisted reference and partial writes fail restart", (t) => {
  for (const failOnWrite of [1, 2]) {
    const root = temporaryDirectory();
    try {
      const ledger = openPublicEvidenceLedger(options(root));
      const { receipt, material } = fixture();
      const original = fs.writeSync;
      let calls = 0;
      const mocked = t.mock.method(fs, "writeSync", (...args: Parameters<typeof original>) => {
        calls++;
        if (calls === failOnWrite) throw Object.assign(new Error("synthetic write failure"), { code: "EIO" });
        return Reflect.apply(original, fs, args) as number;
      });
      syncBuiltinESMExports();
      let returned: StoredPublicEvidence | undefined;
      try {
        expectError(() => { returned = ledger.persistReceipt(receipt, material); }, "io-failure");
      } finally {
        mocked.mock.restore();
        syncBuiltinESMExports();
      }
      assert.equal(returned, undefined);
      assert.equal(calls, failOnWrite);
      // Exclusive creation happened before the injected failure. The zero-byte
      // record/event is deliberately not concealed as successful persistence.
      expectError(() => openPublicEvidenceLedger(options(root)), "truncation");
    } finally { rmSync(root, { recursive: true, force: true }); }
  }
});
