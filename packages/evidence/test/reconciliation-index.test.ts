import assert from "node:assert/strict";
import {
  chmodSync,
  existsSync,
  lstatSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  EvidenceReconciliationIndexError,
  evidenceReconciliationRequestFingerprint,
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
  publicIdempotencyKeySha256,
} from "../src/index.js";
import { withLowerEvidenceReconciliationClaimLimitForTest } from "../src/reconciliation-index-capacity.js";
import {
  PUBLIC_READ_REQUEST_ID,
  PUBLIC_READ_TRACE_ID,
  makePublicReadReceiptFixture,
} from "./public-read-fixtures.js";
import * as evidencePackage from "../src/index.js";

const KEY = `gis-ai-go:ik:v1:${"1".repeat(64)}`;
const OPENED_AT = new Date("2026-08-21T08:00:00.000Z");

function temporaryParent(): string {
  return mkdtempSync(join(tmpdir(), "gis-ai-go-reconciliation-"));
}

function openPair(parent: string) {
  const ledgerRoot = join(parent, "ledger");
  const indexRoot = join(parent, "reconciliation");
  const ledger = openPublicEvidenceLedger({
    rootDirectory: ledgerRoot,
    retentionDays: 30,
    now: () => OPENED_AT,
  });
  const index = openEvidenceReconciliationIndex({
    rootDirectory: indexRoot,
    ledger,
    now: () => OPENED_AT,
  });
  return { indexRoot, ledgerRoot, ledger, index };
}

function claimInput(
  fixture: ReturnType<typeof makePublicReadReceiptFixture>,
  key = KEY,
) {
  return {
    idempotencyKey: key,
    operation: "data.query" as const,
    requestId: fixture.receipt.request_id,
    traceId: fixture.receipt.trace_id,
    resourceId: fixture.receipt.resource.resource_id,
    normalisedParametersSha256:
      fixture.receipt.operation.normalised_parameters.sha256,
  };
}

function expectIndexError(
  run: () => unknown,
  code: EvidenceReconciliationIndexError["code"],
): void {
  assert.throws(run, (error: unknown) => {
    assert.ok(error instanceof EvidenceReconciliationIndexError);
    assert.equal(error.code, code);
    return true;
  });
}

function storedText(root: string): string {
  const paths = readdirSync(root, { recursive: true, encoding: "utf8" });
  return paths
    .map((path) => join(root, path))
    .filter((path) => lstatSync(path).isFile() && lstatSync(path).size > 0)
    .map((path) => readFileSync(path, "utf8"))
    .join("\n");
}

function reconciliationEntries(root: string): Readonly<Record<string, readonly string[]>> {
  return Object.freeze(
    Object.fromEntries(
      ["claim-ownership", "claim-ready", "claims", "resolution-ready", "resolutions"]
        .map((directory) => [directory, readdirSync(join(root, directory)).sort()]),
    ),
  );
}

test("recovers only a durable receipt after restart without retaining the raw key or result", () => {
  const parent = temporaryParent();
  try {
    const { indexRoot, ledgerRoot, index, ledger } = openPair(parent);
    const fixture = makePublicReadReceiptFixture();
    const claimed = index.claim(claimInput(fixture));
    assert.equal(claimed.status, "claimed");
    if (claimed.status !== "claimed") assert.fail("claim was not acquired");

    const resolution = index.resolve(claimed.claim, fixture.receipt);
    assert.equal(resolution.receipt_id, fixture.receipt.receipt_id);
    assert.deepEqual(index.lookup(KEY), {
      status: "pending",
      claim: claimed.claim,
      resolution,
    });

    const persisted = ledger.persistReceipt(fixture.receipt, fixture.material);
    const firstCompleted = index.lookup(KEY);
    assert.equal(firstCompleted.status, "completed");
    if (firstCompleted.status !== "completed") assert.fail("receipt was not reconciled");
    assert.deepEqual(firstCompleted.stored, persisted);

    const restartedLedger = openPublicEvidenceLedger({
      rootDirectory: ledgerRoot,
      retentionDays: 30,
      now: () => new Date("2026-08-22T08:00:00.000Z"),
    });
    const restarted = openEvidenceReconciliationIndex({
      rootDirectory: indexRoot,
      ledger: restartedLedger,
      now: () => new Date("2026-08-22T08:00:00.000Z"),
    });
    const recovered = restarted.lookup(KEY);
    assert.equal(recovered.status, "completed");
    if (recovered.status !== "completed") assert.fail("receipt was not recovered");
    assert.deepEqual(recovered.stored, persisted);
    assert.equal(JSON.stringify(recovered).includes("raw-observation-value"), false);

    const bytes = storedText(indexRoot);
    assert.equal(bytes.includes(KEY), false);
    assert.equal(bytes.includes("raw-observation-value"), false);
    assert.equal(bytes.includes('"query":'), false);
    assert.equal(bytes.includes('"value":'), false);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("same-key retries are completed, pending or conflicting without a second claim", () => {
  const parent = temporaryParent();
  try {
    const { index, ledger } = openPair(parent);
    const fixture = makePublicReadReceiptFixture();
    const first = index.claim(claimInput(fixture));
    assert.equal(first.status, "claimed");
    assert.equal(index.claim(claimInput(fixture)).status, "pending");
    if (first.status !== "claimed") assert.fail("claim was not acquired");
    index.resolve(first.claim, fixture.receipt);
    ledger.persistReceipt(fixture.receipt, fixture.material);
    assert.equal(index.claim(claimInput(fixture)).status, "completed");

    expectIndexError(
      () =>
        index.claim({
          ...claimInput(fixture),
          normalisedParametersSha256: "b".repeat(64),
        }),
      "conflict",
    );
    assert.equal(index.verify().claim_count, 1);
    assert.equal(index.verify().completed_count, 1);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("refuses a new claim at the local admission boundary without changing the store", () => {
  const parent = temporaryParent();
  try {
    const ledgerRoot = join(parent, "ledger");
    const indexRoot = join(parent, "reconciliation");
    const ledger = openPublicEvidenceLedger({
      rootDirectory: ledgerRoot,
      retentionDays: 30,
      now: () => OPENED_AT,
    });
    const indexOptions = withLowerEvidenceReconciliationClaimLimitForTest(
      {
        rootDirectory: indexRoot,
        ledger,
        now: () => OPENED_AT,
      },
      2,
    );
    const index = openEvidenceReconciliationIndex(indexOptions);
    const completedFixture = makePublicReadReceiptFixture();
    const completed = index.claim(claimInput(completedFixture));
    assert.equal(completed.status, "claimed");
    if (completed.status !== "claimed") assert.fail("first claim was not acquired");
    index.resolve(completed.claim, completedFixture.receipt);
    ledger.persistReceipt(completedFixture.receipt, completedFixture.material);

    const pendingKey = `gis-ai-go:ik:v1:${"2".repeat(64)}`;
    const pendingFixture = makePublicReadReceiptFixture(
      "data.query",
      "request-capacity-pending",
      "2".repeat(32),
    );
    assert.equal(index.claim(claimInput(pendingFixture, pendingKey)).status, "claimed");

    assert.equal(index.claim(claimInput(completedFixture)).status, "completed");
    assert.equal(index.claim(claimInput(pendingFixture, pendingKey)).status, "pending");
    const before = reconciliationEntries(indexRoot);
    const rejectedKey = `gis-ai-go:ik:v1:${"3".repeat(64)}`;
    const rejectedFixture = makePublicReadReceiptFixture(
      "data.query",
      "request-capacity-rejected",
      "3".repeat(32),
    );
    expectIndexError(
      () => index.claim(claimInput(rejectedFixture, rejectedKey)),
      "capacity",
    );
    assert.deepEqual(reconciliationEntries(indexRoot), before);
    assert.deepEqual(index.lookup(rejectedKey), { status: "not-found" });
    assert.deepEqual(index.verify(), {
      status: "verified",
      index_id: index.descriptor.index_id,
      ledger_id: ledger.descriptor.ledger_id,
      claim_count: 2,
      resolution_count: 1,
      completed_count: 1,
      pending_count: 1,
      checks: [
        "descriptor",
        "canonical-files",
        "content-identities",
        "exclusive-key-bindings",
        "receipt-linkage",
        "retention",
        "privacy",
      ],
    });

    const reopenedLedger = openPublicEvidenceLedger({
      rootDirectory: ledgerRoot,
      retentionDays: 30,
      now: () => OPENED_AT,
    });
    const reopened = openEvidenceReconciliationIndex(
      withLowerEvidenceReconciliationClaimLimitForTest(
        { rootDirectory: indexRoot, ledger: reopenedLedger, now: () => OPENED_AT },
        2,
      ),
    );
    assert.equal(reopened.lookup(KEY).status, "completed");
    assert.equal(reopened.lookup(pendingKey).status, "pending");
    assert.equal(reopened.verify().claim_count, 2);

    assert.throws(
      () =>
        withLowerEvidenceReconciliationClaimLimitForTest(
          { rootDirectory: indexRoot, ledger: reopenedLedger },
          Number.MAX_SAFE_INTEGER,
        ),
      RangeError,
    );
    assert.equal(
      "withLowerEvidenceReconciliationClaimLimitForTest" in evidencePackage,
      false,
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("rejects persist-before-resolution without publishing resolution state", () => {
  const parent = temporaryParent();
  try {
    const { indexRoot, index, ledger } = openPair(parent);
    const fixture = makePublicReadReceiptFixture();
    const claimed = index.claim(claimInput(fixture));
    assert.equal(claimed.status, "claimed");
    if (claimed.status !== "claimed") assert.fail("claim was not acquired");
    ledger.persistReceipt(fixture.receipt, fixture.material);
    expectIndexError(() => index.resolve(claimed.claim, fixture.receipt), "conflict");
    assert.deepEqual(readdirSync(join(indexRoot, "resolutions")), []);
    assert.deepEqual(readdirSync(join(indexRoot, "resolution-ready")), []);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("verifies many resolutions with one bulk lookup and no per-resolution inspection", () => {
  const parent = temporaryParent();
  try {
    const { index, ledger } = openPair(parent);
    for (let position = 1; position <= 8; position += 1) {
      const hex = position.toString(16);
      const fixture = makePublicReadReceiptFixture(
        "data.query",
        `request-linear-${position}`,
        `${hex.repeat(32)}`,
      );
      const key = `gis-ai-go:ik:v1:${hex.repeat(64)}`;
      const claimed = index.claim(claimInput(fixture, key));
      assert.equal(claimed.status, "claimed");
      if (claimed.status !== "claimed") assert.fail("claim was not acquired");
      index.resolve(claimed.claim, fixture.receipt);
      ledger.persistReceipt(fixture.receipt, fixture.material);
    }

    const originalBulk = ledger.inspectReceipts.bind(ledger);
    let bulkCalls = 0;
    let singleCalls = 0;
    Object.defineProperty(ledger, "inspectReceipts", {
      value: (identities: readonly string[]) => {
        bulkCalls += 1;
        return originalBulk(identities);
      },
    });
    Object.defineProperty(ledger, "inspect", {
      value: () => {
        singleCalls += 1;
        throw new Error("per-resolution inspection must not run");
      },
    });
    const health = index.verify();
    assert.equal(health.completed_count, 8);
    const firstFixture = makePublicReadReceiptFixture(
      "data.query",
      "request-linear-1",
      "1".repeat(32),
    );
    const firstKey = `gis-ai-go:ik:v1:${"1".repeat(64)}`;
    assert.equal(index.lookup(firstKey).status, "completed");
    assert.equal(index.claim(claimInput(firstFixture, firstKey)).status, "completed");
    assert.equal(bulkCalls, 3);
    assert.equal(singleCalls, 0);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("an ownership marker or unpublished partial claim is stable pending", () => {
  const parent = temporaryParent();
  try {
    const { indexRoot, index } = openPair(parent);
    const digest = publicIdempotencyKeySha256(KEY);
    writeFileSync(join(indexRoot, "claim-ownership", digest), "", { mode: 0o600 });
    assert.deepEqual(index.lookup(KEY), { status: "pending" });
    assert.equal(index.verify().pending_count, 1);

    writeFileSync(join(indexRoot, "claims", `${digest}.json`), "{", { mode: 0o600 });
    assert.deepEqual(index.lookup(KEY), { status: "pending" });
    assert.equal(index.verify().pending_count, 1);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("rejects a raw key smuggled through request identity before writing a claim", () => {
  const parent = temporaryParent();
  try {
    const { indexRoot, index } = openPair(parent);
    const fixture = makePublicReadReceiptFixture(
      "data.query",
      KEY,
      PUBLIC_READ_TRACE_ID,
    );
    expectIndexError(() => index.claim(claimInput(fixture)), "invalid-input");
    assert.deepEqual(readdirSync(join(indexRoot, "claim-ownership")), []);
    assert.deepEqual(readdirSync(join(indexRoot, "claims")), []);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("requires private directories and files on POSIX", {
  skip: process.platform === "win32",
}, () => {
  const directoryParent = temporaryParent();
  const fileParent = temporaryParent();
  try {
    const directoryPair = openPair(directoryParent);
    chmodSync(join(directoryPair.indexRoot, "claims"), 0o755);
    expectIndexError(() => directoryPair.index.verify(), "corruption");

    const filePair = openPair(fileParent);
    chmodSync(join(filePair.indexRoot, "index.json"), 0o644);
    expectIndexError(() => filePair.index.verify(), "corruption");
  } finally {
    rmSync(directoryParent, { recursive: true, force: true });
    rmSync(fileParent, { recursive: true, force: true });
  }
});

test("rejects same, nested and symbolic-link storage roots before any index write", {
  skip: process.platform === "win32",
}, () => {
  const parent = temporaryParent();
  try {
    const ledgerRoot = join(parent, "ledger");
    const ledger = openPublicEvidenceLedger({ rootDirectory: ledgerRoot, retentionDays: 30 });
    expectIndexError(
      () => openEvidenceReconciliationIndex({ rootDirectory: ledgerRoot, ledger }),
      "invalid-configuration",
    );
    expectIndexError(
      () =>
        openEvidenceReconciliationIndex({
          rootDirectory: join(ledgerRoot, "reconciliation"),
          ledger,
        }),
      "invalid-configuration",
    );
    expectIndexError(
      () => openEvidenceReconciliationIndex({ rootDirectory: parent, ledger }),
      "invalid-configuration",
    );

    const realIndex = join(parent, "real-index");
    const alias = join(parent, "index-alias");
    writeFileSync(join(parent, "sentinel"), "unchanged\n", { mode: 0o600 });
    // Create a real private directory without invoking the index initialiser.
    mkdirSync(realIndex, { mode: 0o700 });
    symlinkSync(realIndex, alias);
    expectIndexError(
      () => openEvidenceReconciliationIndex({ rootDirectory: alias, ledger }),
      "invalid-configuration",
    );
    assert.equal(readFileSync(join(parent, "sentinel"), "utf8"), "unchanged\n");
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("rejects the all-zero key and keeps ordinary request identities", () => {
  const parent = temporaryParent();
  try {
    const { index } = openPair(parent);
    const fixture = makePublicReadReceiptFixture(
      "data.query",
      PUBLIC_READ_REQUEST_ID,
      PUBLIC_READ_TRACE_ID,
    );
    expectIndexError(
      () => index.claim(claimInput(fixture, `gis-ai-go:ik:v1:${"0".repeat(64)}`)),
      "invalid-input",
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("rejects proxies and accessors without invoking them or writing claim state", () => {
  const parent = temporaryParent();
  try {
    const { indexRoot, ledger, index } = openPair(parent);
    let optionReads = 0;
    const accessorOptions = { ledger } as {
      ledger: typeof ledger;
      rootDirectory: string;
    };
    Object.defineProperty(accessorOptions, "rootDirectory", {
      enumerable: true,
      get: () => {
        optionReads += 1;
        return join(parent, "accessor-index");
      },
    });
    expectIndexError(
      () => openEvidenceReconciliationIndex(accessorOptions),
      "invalid-configuration",
    );
    assert.equal(optionReads, 0);
    assert.equal(existsSync(join(parent, "accessor-index")), false);

    const fixture = makePublicReadReceiptFixture();
    let claimReads = 0;
    const hostileClaim = { ...claimInput(fixture) } as Record<string, unknown>;
    Object.defineProperty(hostileClaim, "requestId", {
      enumerable: true,
      get: () => {
        claimReads += 1;
        return PUBLIC_READ_REQUEST_ID;
      },
    });
    expectIndexError(
      () => index.claim(hostileClaim as ReturnType<typeof claimInput>),
      "invalid-input",
    );
    assert.equal(claimReads, 0);
    assert.deepEqual(readdirSync(join(indexRoot, "claim-ownership")), []);

    let fingerprintReads = 0;
    const hostileFingerprint = {
      operation: "data.query",
      resourceId: fixture.receipt.resource.resource_id,
    } as {
      operation: "data.query";
      resourceId: string;
      normalisedParametersSha256: string;
    };
    Object.defineProperty(hostileFingerprint, "normalisedParametersSha256", {
      enumerable: true,
      get: () => {
        fingerprintReads += 1;
        return fixture.receipt.operation.normalised_parameters.sha256;
      },
    });
    expectIndexError(
      () => evidenceReconciliationRequestFingerprint(hostileFingerprint),
      "invalid-input",
    );
    assert.equal(fingerprintReads, 0);

    expectIndexError(
      () => index.claim(new Proxy(claimInput(fixture), {})),
      "invalid-input",
    );
    assert.deepEqual(readdirSync(join(indexRoot, "claim-ownership")), []);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("rejects a raw idempotency key embedded in either storage root", () => {
  const parent = temporaryParent();
  try {
    const ledger = openPublicEvidenceLedger({
      rootDirectory: join(parent, "ordinary-ledger"),
      retentionDays: 30,
    });
    const rawIndexRoot = join(parent, KEY);
    expectIndexError(
      () => openEvidenceReconciliationIndex({ rootDirectory: rawIndexRoot, ledger }),
      "invalid-configuration",
    );
    assert.equal(existsSync(rawIndexRoot), false);

    const keyParent = join(parent, KEY);
    mkdirSync(keyParent, { mode: 0o700 });
    const keyedLedger = openPublicEvidenceLedger({
      rootDirectory: join(keyParent, "ledger"),
      retentionDays: 30,
    });
    const candidate = join(parent, "candidate-index");
    expectIndexError(
      () => openEvidenceReconciliationIndex({ rootDirectory: candidate, ledger: keyedLedger }),
      "invalid-configuration",
    );
    assert.equal(existsSync(candidate), false);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});
