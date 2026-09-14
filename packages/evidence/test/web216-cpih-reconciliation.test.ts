import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { canonicalJson } from "../src/canonical-json.js";
import { contentAddress } from "../src/digest.js";
import { openPublicEvidenceLedger } from "../src/public-ledger.js";
import {
  EvidenceReconciliationIndexError, PublicEvidenceReconciliationIndex,
  isWeb216CpihReconciliationIndex, openEvidenceReconciliationIndex,
  openWeb216CpihReconciliationIndex, publicIdempotencyKeySha256,
  web216CpihIdempotencyKeySha256, web216CpihReconciliationRequestFingerprint,
  type Web216CpihReconciliationClaim,
} from "../src/reconciliation-index.js";
import { withLowerEvidenceReconciliationClaimLimitForTest } from "../src/reconciliation-index-capacity.js";
import {
  WEB216_CPIH_CAPTURE, buildWeb216CpihReceipt, buildWeb216CpihResult, verifyWeb216CpihReceipt,
  type Web216CpihPeriod,
} from "../src/web216-cpih-receipt.js";
import { makePublicReadReceiptFixture } from "./public-read-fixtures.js";

const KEY = `gis-ai-go:ik:v1:${"1".repeat(64)}`;
const OTHER_KEY = `gis-ai-go:ik:v1:${"2".repeat(64)}`;
const NOW = new Date("2026-09-14T17:00:00.000Z");
const PROJECTION = JSON.parse(readFileSync(new URL(
  "../../../../tests/fixtures/web216/current-cpih-projection.json", import.meta.url,
), "utf8"));

function fixture(period: Web216CpihPeriod = "2026-07") {
  const software = { name: "gis-ai-go-mcp-gateway", version: "0.1.0", revision: "a".repeat(40) } as const;
  const input = { period, idempotencyKey: KEY, requestId: "web216-cpih-reconciliation-test",
    traceId: "0123456789abcdef0123456789abcdef" };
  const receipt = buildWeb216CpihReceipt({ projection: PROJECTION, period,
    requestId: input.requestId, traceId: input.traceId, createdAt: NOW.toISOString(), software });
  const material = { projection: PROJECTION, normalisedParameters: { period },
    resultCore: buildWeb216CpihResult(PROJECTION, period), expectedSoftware: software };
  return { input, receipt, material };
}

function openPair(parent: string, maximumClaims?: number) {
  const ledgerRoot = join(parent, "ledger");
  const indexRoot = join(parent, "index");
  const ledger = openPublicEvidenceLedger({ rootDirectory: ledgerRoot, retentionDays: 30, now: () => NOW });
  const options = { rootDirectory: indexRoot, ledger, now: () => NOW };
  const index = openWeb216CpihReconciliationIndex(maximumClaims === undefined ? options
    : withLowerEvidenceReconciliationClaimLimitForTest(options, maximumClaims));
  return { index, ledger, ledgerRoot, indexRoot };
}

function withPair(run: (pair: ReturnType<typeof openPair>, parent: string) => void, maximumClaims?: number) {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-cpih-reconciliation-"));
  try { run(openPair(parent, maximumClaims), parent); }
  finally { rmSync(parent, { recursive: true, force: true }); }
}

function expectCode(run: () => unknown, code: string) {
  assert.throws(run, (error: unknown) => error instanceof EvidenceReconciliationIndexError && error.code === code);
}

function requireClaim(pair: ReturnType<typeof openPair>, f = fixture()): Web216CpihReconciliationClaim {
  const outcome = pair.index.claim(f.input);
  assert.equal(outcome.status, "claimed");
  if (outcome.status !== "claimed") assert.fail("Expected an exclusively owned claim");
  return outcome.claim;
}

test("CPIH is a frozen branded capability, not a legacy index or caller-authored replacement", () => {
  withPair(({ index, ledger }) => {
    assert.equal(isWeb216CpihReconciliationIndex(index), true);
    assert.equal(isWeb216CpihReconciliationIndex({ ...index }), false);
    assert.equal(isWeb216CpihReconciliationIndex(new Proxy(index, {})), false);
    assert.equal(index instanceof PublicEvidenceReconciliationIndex, false);
    assert.equal(Object.isFrozen(index), true);
    assert.equal(Object.isFrozen(index.descriptor.scope), true);
    assert.equal(index.ledger, ledger);
    assert.deepEqual(index.descriptor.scope.source_operations, ["read-validated-cpih-capture"]);
    assert.equal(index.descriptor.scope.capture_projection_sha256, WEB216_CPIH_CAPTURE.projection_sha256);
    assert.throws(() => PublicEvidenceReconciliationIndex.prototype.claim.call(index as never, {} as never));
  });
});

test("both periods recover only a linked durable CPIH record after restart and lost response", () => {
  for (const period of ["2026-01", "2026-07"] as const) {
    withPair((pair) => {
      const f = fixture(period);
      assert.equal(pair.index.lookup(KEY).status, "not-found");
      const claim = requireClaim(pair, f);
      assert.equal(claim.period, period);
      assert.equal(claim.capture_projection_sha256, WEB216_CPIH_CAPTURE.projection_sha256);
      assert.equal(Object.hasOwn(claim, "resource_id"), false);
      assert.equal(verifyWeb216CpihReceipt(f.receipt, f.material).valid, true);
      const resolution = pair.index.resolve(claim, f.receipt);
      assert.deepEqual(pair.index.lookup(KEY), { status: "pending", claim, resolution });
      const stored = pair.ledger.persistReceipt(f.receipt, f.material);
      assert.equal(stored.record.schema, "gis-ai-go.public-evidence-record.v3");
      const restartedLedger = openPublicEvidenceLedger({ rootDirectory: pair.ledgerRoot,
        retentionDays: 30, now: () => new Date("2026-09-15T17:00:00.000Z") });
      const restarted = openWeb216CpihReconciliationIndex({ rootDirectory: pair.indexRoot,
        ledger: restartedLedger, now: () => new Date("2026-09-15T17:00:00.000Z") });
      const recovered = restarted.lookup(KEY);
      assert.equal(recovered.status, "completed");
      if (recovered.status !== "completed") assert.fail("Expected durable recovery");
      assert.deepEqual(recovered.stored, stored);
      let executionCount = 1;
      const retry = restarted.claim({ ...f.input, requestId: "new-transport-request", traceId: "b".repeat(32) });
      if (retry.status === "claimed") executionCount++;
      assert.equal(retry.status, "completed");
      assert.equal(executionCount, 1);
      assert.equal(restarted.verify().claim_count, 1);
      const documents = ["index.json", ...["claims", "resolutions"].flatMap((directory) =>
        readdirSync(join(pair.indexRoot, directory)).map((name) => `${directory}/${name}`))]
        .map((name) => readFileSync(join(pair.indexRoot, name), "utf8")).join("\n");
      assert.equal(documents.includes(KEY), false);
      assert.equal(documents.includes('"value"'), false);
      assert.equal(documents.includes('"projection"'), false);
    });
  }
});

test("same-key pending and completed retries conflict on a different admitted period", () => {
  withPair((pair) => {
    const f = fixture(); const claim = requireClaim(pair, f);
    assert.equal(pair.index.claim(f.input).status, "pending");
    expectCode(() => pair.index.claim({ ...f.input, period: "2026-01" }), "conflict");
    pair.index.resolve(claim, f.receipt);
    pair.ledger.persistReceipt(f.receipt, f.material);
    expectCode(() => pair.index.claim({ ...f.input, period: "2026-01" }), "conflict");
    assert.equal(pair.index.verify().claim_count, 1);
    assert.notEqual(web216CpihIdempotencyKeySha256(KEY), publicIdempotencyKeySha256(KEY));
    assert.notEqual(web216CpihReconciliationRequestFingerprint("2026-01"),
      web216CpihReconciliationRequestFingerprint("2026-07"));
  });
});

test("caller fields, unsupported periods and accessor or proxy claims fail before publication", () => {
  withPair((pair) => {
    const input = fixture().input;
    for (const extra of [{ operation: "data.query" }, { capture_projection_sha256: "0".repeat(64) },
      { resourceId: "invented" }, { normalisedParametersSha256: "0".repeat(64) }, { authority: "allow" }]) {
      expectCode(() => pair.index.claim({ ...input, ...extra }), "invalid-input");
    }
    for (const period of ["latest", "2026-02", null]) {
      expectCode(() => pair.index.claim({ ...input, period } as never), "invalid-input");
    }
    let reads = 0;
    const accessor = Object.defineProperty({ ...input }, "period", { enumerable: true, get() { reads++; return "2026-07"; } });
    expectCode(() => pair.index.claim(accessor), "invalid-input");
    expectCode(() => pair.index.claim(new Proxy(input, {})), "invalid-input");
    expectCode(() => pair.index.claim({ ...input, requestId: KEY }), "invalid-input");
    assert.equal(reads, 0);
    assert.equal(pair.index.verify().claim_count, 0);
  });
});

test("cross-family openers, foreign ledgers, foreign claims and legacy receipts fail closed", () => {
  withPair((pair, parent) => {
    const f = fixture(); const claim = requireClaim(pair, f);
    expectCode(() => openEvidenceReconciliationIndex({ rootDirectory: pair.indexRoot, ledger: pair.ledger }), "corruption");
    const legacy = openEvidenceReconciliationIndex({ rootDirectory: join(parent, "legacy-index"), ledger: pair.ledger, now: () => NOW });
    expectCode(() => openWeb216CpihReconciliationIndex({ rootDirectory: join(parent, "legacy-index"), ledger: pair.ledger }), "corruption");
    const foreignLedger = openPublicEvidenceLedger({ rootDirectory: join(parent, "foreign-ledger"),
      now: () => new Date("2026-09-14T17:00:01.000Z") });
    expectCode(() => openWeb216CpihReconciliationIndex({ rootDirectory: pair.indexRoot, ledger: foreignLedger }), "corruption");
    const foreign = openWeb216CpihReconciliationIndex({ rootDirectory: join(parent, "foreign-index"), ledger: foreignLedger, now: () => NOW });
    const foreignClaim = foreign.claim(f.input);
    if (foreignClaim.status !== "claimed") assert.fail("Expected foreign claim");
    expectCode(() => pair.index.resolve(foreignClaim.claim, f.receipt), "corruption");
    expectCode(() => pair.index.resolve(claim, makePublicReadReceiptFixture().receipt as never), "invalid-input");
    expectCode(() => legacy.resolve(claim as never, f.receipt as never), "corruption");
    assert.equal(pair.index.verify().resolution_count, 0);
  });
});

test("ordinary and rehashed changed capture, period or receipt links cannot resolve a claim", () => {
  withPair((pair) => {
    const f = fixture(); const claim = requireClaim(pair, f);
    for (const mutation of [{ capture_projection_sha256: "0".repeat(64) }, { period: "2026-01" },
      { request_id: "different" }, { ledger_id: "gis-ai-go:public-evidence-ledger:sha256:" + "0".repeat(64) }]) {
      const { claim_id: _id, ...core } = { ...claim, ...mutation };
      const rehashed = { ...core, claim_id: contentAddress("gis-ai-go:evidence-reconciliation-claim",
        "gis-ai-go.web216-cpih-reconciliation-claim.v1", core) };
      assert.throws(() => pair.index.resolve(rehashed as never, f.receipt));
    }
    expectCode(() => pair.index.resolve(claim, fixture("2026-01").receipt), "invalid-input");
    assert.equal(pair.index.verify().resolution_count, 0);
  });
});

test("ownership and partial unpublished claim state stay pending without automatic reclamation", () => {
  withPair((pair) => {
    const key = web216CpihIdempotencyKeySha256(KEY);
    writeFileSync(join(pair.indexRoot, "claim-ownership", key), "", { mode: 0o600 });
    assert.deepEqual(pair.index.lookup(KEY), { status: "pending" });
    writeFileSync(join(pair.indexRoot, "claims", `${key}.json`), "{", { mode: 0o600 });
    assert.deepEqual(pair.index.lookup(KEY), { status: "pending" });
    assert.equal(pair.index.claim(fixture().input).status, "pending");
    assert.equal(readFileSync(join(pair.indexRoot, "claims", `${key}.json`), "utf8"), "{");
    assert.deepEqual(readdirSync(join(pair.indexRoot, "claim-ready")), []);
  });
});

test("published partial or missing claims and resolutions are corruption, never completed", () => {
  for (const stage of ["claim", "resolution"] as const) {
    withPair((pair) => {
      const f = fixture(); const claim = requireClaim(pair, f);
      if (stage === "resolution") pair.index.resolve(claim, f.receipt);
      const directory = stage === "claim" ? "claims" : "resolutions";
      const path = join(pair.indexRoot, directory, `${web216CpihIdempotencyKeySha256(KEY)}.json`);
      writeFileSync(path, "{", { mode: 0o600 });
      assert.throws(() => pair.index.lookup(KEY));
      rmSync(path);
      expectCode(() => pair.index.lookup(KEY), "truncation");
    });
  }
});

test("resolution precedes persistence; failed persistence is pending and corrupt stores fail closed", () => {
  withPair((pair) => {
    const f = fixture(); const claim = requireClaim(pair, f);
    pair.ledger.persistReceipt(f.receipt, f.material);
    expectCode(() => pair.index.resolve(claim, f.receipt), "conflict");
    assert.deepEqual(readdirSync(join(pair.indexRoot, "resolutions")), []);
  });
  withPair((pair) => {
    const f = fixture(); const claim = requireClaim(pair, f);
    pair.index.resolve(claim, f.receipt);
    assert.throws(() => pair.ledger.persistReceipt(f.receipt, { ...f.material, projection: {} }));
    assert.equal(pair.index.lookup(KEY).status, "pending");
    const stored = pair.ledger.persistReceipt(f.receipt, f.material);
    const path = join(pair.ledgerRoot, "records", `${stored.record.record_id.split(":").at(-1)}.json`);
    writeFileSync(path, "{", { mode: 0o600 });
    assert.throws(() => pair.index.lookup(KEY));
    rmSync(path);
    assert.throws(() => pair.index.lookup(KEY));
  });
});

test("bounded capacity retains old pending and completed keys but refuses a new one", () => {
  withPair((pair) => {
    const f = fixture(); const claim = requireClaim(pair, f);
    assert.equal(pair.index.claimCapacity().status, "exhausted");
    assert.equal(pair.index.claim(f.input).status, "pending");
    expectCode(() => pair.index.claim({ ...f.input, idempotencyKey: OTHER_KEY }), "capacity");
    pair.index.resolve(claim, f.receipt); pair.ledger.persistReceipt(f.receipt, f.material);
    assert.equal(pair.index.claim(f.input).status, "completed");
    assert.equal(pair.index.verify().claim_count, 1);
  }, 1);
});

test("legacy descriptor, claim, resolution and fingerprints retain their exact pre-change identities", () => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-legacy-reconciliation-"));
  try {
    const now = () => new Date("2026-08-21T08:00:00.000Z");
    const ledger = openPublicEvidenceLedger({ rootDirectory: join(parent, "ledger"), retentionDays: 30, now });
    const index = openEvidenceReconciliationIndex({ rootDirectory: join(parent, "index"), ledger, now });
    const f = makePublicReadReceiptFixture(); const r = f.receipt;
    const outcome = index.claim({ idempotencyKey: KEY, operation: "data.query", requestId: r.request_id,
      traceId: r.trace_id, resourceId: r.resource.resource_id,
      normalisedParametersSha256: r.operation.normalised_parameters.sha256 });
    if (outcome.status !== "claimed") assert.fail("Expected legacy claim");
    const resolution = index.resolve(outcome.claim, r);
    assert.equal(index.descriptor.index_id, "gis-ai-go:evidence-reconciliation-index:sha256:85357f6dd2d8ac372226d325e24bc8b9abc81b86a6fc4295c0e62395a8362249");
    assert.equal(outcome.claim.claim_id, "gis-ai-go:evidence-reconciliation-claim:sha256:c90a7cabb31e5cfd9d38784bfb9af119bdfb30c6a0b487a1a4fe141ac6090dc2");
    assert.equal(resolution.resolution_id, "gis-ai-go:evidence-reconciliation-resolution:sha256:f42e9ba3e61e5ee1c4c62ea571d83fd2dd9d8eee53495565abd785d90854f305");
    assert.equal(outcome.claim.idempotency_key_sha256, "ff8c9eb4ba06bf13465e7a9ffc315f51a72ff077d921699d433ee606a1d70dde");
    assert.equal(outcome.claim.request_fingerprint_sha256, "517e649e9ff36842582a30cb17f0ea3ac7bf4209b395edf6a3816be5aa76e5bc");
    assert.equal(canonicalJson(index.descriptor).includes("web216"), false);
  } finally { rmSync(parent, { recursive: true, force: true }); }
});
