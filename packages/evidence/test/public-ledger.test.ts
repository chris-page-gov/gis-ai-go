import assert from "node:assert/strict";
import {
  chmodSync,
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
  CANONICALISATION,
  PUBLIC_POLICY_OBLIGATIONS,
  PublicEvidenceLedgerError,
  buildInlineReceipt,
  buildPublicPolicyDecision,
  openPublicEvidenceLedger,
  type InlineReceiptBuildInput,
  type InlineReceiptVerificationMaterial,
} from "../src/index.js";
import { withLowerPublicEvidenceLedgerEventLimitForTest } from "../src/public-ledger-capacity.js";
import { makeReceiptBuildInput } from "./fixtures.js";
import * as evidencePackage from "../src/index.js";

const PERSISTED_AT = new Date("2026-08-20T12:00:00.000Z");

interface TestReceipt {
  readonly receipt: ReturnType<typeof buildInlineReceipt>;
  readonly material: InlineReceiptVerificationMaterial;
}

function temporaryDirectory(): string {
  return mkdtempSync(join(tmpdir(), "gis-ai-go-evidence-ledger-"));
}

function receiptFixture(
  requestId = "request-fixture-1",
  traceId = "0123456789abcdef0123456789abcdef",
  query = "phrase retained only in digest material",
): TestReceipt {
  const base = makeReceiptBuildInput();
  const resultCore = {
    ...(base.resultCore as Record<string, unknown>),
    request_id: requestId,
    trace_id: traceId,
  };
  const policyDecision = buildPublicPolicyDecision({
    schema: "gis-ai-go.public-policy-decision.v1",
    canonicalisation: CANONICALISATION,
    request_id: requestId,
    trace_id: traceId,
    authority_context_id: base.authorityContext.context_id,
    policy_id: base.publicPolicy.policy_id,
    policy_version: base.publicPolicy.version,
    policy_default_effect: "deny",
    operation: "catalogue.search",
    effect: "allow-with-obligations",
    reason_code: "public-catalogue-read-allowed",
    obligations: PUBLIC_POLICY_OBLIGATIONS,
  });
  const input: InlineReceiptBuildInput = {
    ...base,
    requestId,
    traceId,
    normalisedParameters: {
      ...(base.normalisedParameters as Record<string, unknown>),
      query,
    },
    policyDecision,
    resultCore,
  };
  const receipt = buildInlineReceipt(input);
  return {
    receipt,
    material: {
      normalisedParameters: input.normalisedParameters,
      resultCore,
      publicPolicy: input.publicPolicy,
      licenceObligations: input.licenceObligations,
      expectedAuthorityContext: input.authorityContext,
      expectedPolicyDecision: policyDecision,
      expectedCatalogue: input.catalogue,
      expectedSoftware: input.software,
    },
  };
}

function expectLedgerError(
  run: () => unknown,
  code: PublicEvidenceLedgerError["code"],
): PublicEvidenceLedgerError {
  let captured: PublicEvidenceLedgerError | undefined;
  assert.throws(run, (error: unknown) => {
    assert.ok(error instanceof PublicEvidenceLedgerError);
    assert.equal(error.code, code);
    captured = error;
    return true;
  });
  assert.ok(captured);
  return captured;
}

function populatedLedger(): {
  readonly root: string;
  readonly stored: ReturnType<ReturnType<typeof openPublicEvidenceLedger>["persistReceipt"]>;
} {
  const root = temporaryDirectory();
  const ledger = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 30,
    now: () => PERSISTED_AT,
  });
  const fixture = receiptFixture();
  const stored = ledger.persistReceipt(fixture.receipt, fixture.material);
  return { root, stored };
}

function ledgerSnapshot(root: string): Readonly<Record<string, unknown>> {
  const files = (directory: "records" | "events") =>
    readdirSync(join(root, directory))
      .sort()
      .map((name) => Object.freeze({
        name,
        text: readFileSync(join(root, directory, name), "utf8"),
      }));
  return Object.freeze({
    descriptor: readFileSync(join(root, "ledger.json"), "utf8"),
    records: files("records"),
    events: files("events"),
  });
}

test("persists authorised open receipts and verifies them after restart", () => {
  const root = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger({
      rootDirectory: root,
      retentionDays: 30,
      now: () => PERSISTED_AT,
    });
    assert.deepEqual(ledger.verify(), {
      status: "verified",
      ledger_id: ledger.descriptor.ledger_id,
      event_count: 0,
      record_count: 0,
      last_event_id: null,
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

    const fixture = receiptFixture();
    const stored = ledger.persistReceipt(fixture.receipt, fixture.material);
    assert.equal(stored.reference.status, "persisted");
    assert.equal(stored.reference.persisted_at, "2026-08-20T12:00:00.000Z");
    assert.equal(stored.reference.retain_until, "2026-09-19T12:00:00.000Z");
    assert.equal(stored.record.receipt.receipt_id, fixture.receipt.receipt_id);
    assert.deepEqual(stored.record.receipt.evidence_handling, {
      attestation: "not-attested",
      delivery: "inline-only",
      persistence: "not-persisted",
    });
    assert.equal(stored.event.previous_event_id, null);
    assert.equal(Object.isFrozen(stored), true);

    const restarted = openPublicEvidenceLedger({
      rootDirectory: root,
      retentionDays: 30,
      now: () => new Date("2028-01-01T00:00:00.000Z"),
    });
    assert.equal(restarted.verify().event_count, 1);
    assert.deepEqual(restarted.inspect(fixture.receipt.receipt_id), stored);
    assert.deepEqual(restarted.inspect(stored.record.record_id), stored);
    assert.equal(restarted.inspect("gis-ai-go:evidence-receipt:sha256:" + "0".repeat(64)), null);

    const storedText = [
      readFileSync(join(root, "ledger.json"), "utf8"),
      ...readdirSync(join(root, "records")).map((name) =>
        readFileSync(join(root, "records", name), "utf8"),
      ),
      ...readdirSync(join(root, "events")).map((name) =>
        readFileSync(join(root, "events", name), "utf8"),
      ),
    ].join("\n");
    assert.equal(storedText.includes("phrase retained only in digest material"), false);
    assert.equal(storedText.includes("/Users/"), false);
    assert.equal(storedText.includes("Bearer "), false);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("chains distinct events and rejects exact or semantic replay without overwrite", () => {
  const root = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger({
      rootDirectory: root,
      retentionDays: 365,
      now: () => PERSISTED_AT,
    });
    const first = receiptFixture();
    const storedFirst = ledger.persistReceipt(first.receipt, first.material);
    const beforeReplay = readFileSync(
      join(root, "records", `${storedFirst.record.record_id.slice(-64)}.json`),
      "utf8",
    );
    expectLedgerError(() => ledger.persistReceipt(first.receipt, first.material), "replay");
    assert.equal(
      readFileSync(
        join(root, "records", `${storedFirst.record.record_id.slice(-64)}.json`),
        "utf8",
      ),
      beforeReplay,
    );
    const reissuedInput = makeReceiptBuildInput();
    const reissued = buildInlineReceipt({
      ...reissuedInput,
      createdAt: "2026-08-20T07:00:01Z",
    });
    expectLedgerError(
      () =>
        ledger.persistReceipt(reissued, {
          normalisedParameters: reissuedInput.normalisedParameters,
          resultCore: reissuedInput.resultCore,
          publicPolicy: reissuedInput.publicPolicy,
          licenceObligations: reissuedInput.licenceObligations,
        }),
      "replay",
    );

    const second = receiptFixture(
      "request-fixture-2",
      "1123456789abcdef0123456789abcdef",
      "second semantic request",
    );
    const storedSecond = ledger.persistReceipt(second.receipt, second.material);
    assert.equal(storedSecond.event.sequence, 2);
    assert.equal(storedSecond.event.previous_event_id, storedFirst.event.event_id);
    assert.equal(ledger.verify().event_count, 2);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("refuses a new receipt at capacity before either immutable ledger write", () => {
  const root = temporaryDirectory();
  try {
    const options = withLowerPublicEvidenceLedgerEventLimitForTest(
      {
        rootDirectory: root,
        retentionDays: 30,
        now: () => PERSISTED_AT,
      },
      2,
    );
    const ledger = openPublicEvidenceLedger(options);
    const first = receiptFixture();
    const second = receiptFixture(
      "request-capacity-2",
      "2123456789abcdef0123456789abcdef",
      "second capacity fixture",
    );
    const rejected = receiptFixture(
      "request-capacity-3",
      "3123456789abcdef0123456789abcdef",
      "rejected capacity fixture",
    );
    const storedFirst = ledger.persistReceipt(first.receipt, first.material);
    ledger.persistReceipt(second.receipt, second.material);

    const before = ledgerSnapshot(root);
    expectLedgerError(
      () => ledger.persistReceipt(first.receipt, first.material),
      "replay",
    );
    assert.deepEqual(ledger.inspect(first.receipt.receipt_id), storedFirst);
    expectLedgerError(
      () => ledger.persistReceipt(rejected.receipt, rejected.material),
      "capacity",
    );
    assert.deepEqual(ledgerSnapshot(root), before);
    assert.deepEqual(ledger.verify(), {
      status: "verified",
      ledger_id: ledger.descriptor.ledger_id,
      event_count: 2,
      record_count: 2,
      last_event_id: ledger.verify().last_event_id,
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

    const reopened = openPublicEvidenceLedger(
      withLowerPublicEvidenceLedgerEventLimitForTest(
        {
          rootDirectory: root,
          retentionDays: 30,
          now: () => PERSISTED_AT,
        },
        2,
      ),
    );
    assert.equal(reopened.verify().event_count, 2);
    assert.deepEqual(reopened.inspect(first.receipt.receipt_id), storedFirst);
    expectLedgerError(
      () => reopened.persistReceipt(first.receipt, first.material),
      "replay",
    );
    assert.deepEqual(ledgerSnapshot(root), before);

    assert.throws(
      () =>
        withLowerPublicEvidenceLedgerEventLimitForTest(
          { rootDirectory: root, retentionDays: 30 },
          Number.MAX_SAFE_INTEGER,
        ),
      RangeError,
    );
    assert.equal(
      "withLowerPublicEvidenceLedgerEventLimitForTest" in evidencePackage,
      false,
    );
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("rejects corruption, truncation, identity collision and orphaned records on restart", () => {
  const base = populatedLedger();
  try {
    const variants = {
      corruption: temporaryDirectory(),
      truncation: temporaryDirectory(),
      collision: temporaryDirectory(),
      orphan: temporaryDirectory(),
    };
    try {
      for (const target of Object.values(variants)) {
        cpSync(base.root, target, { recursive: true });
        if (process.platform !== "win32") {
          chmodSync(target, 0o700);
          chmodSync(join(target, "records"), 0o700);
          chmodSync(join(target, "events"), 0o700);
          chmodSync(join(target, "ledger.json"), 0o600);
          for (const name of readdirSync(join(target, "records"))) {
            chmodSync(join(target, "records", name), 0o600);
          }
          for (const name of readdirSync(join(target, "events"))) {
            chmodSync(join(target, "events", name), 0o600);
          }
        }
      }

      const corruptRecord = readdirSync(join(variants.corruption, "records"))[0]!;
      const corruptPath = join(variants.corruption, "records", corruptRecord);
      writeFileSync(
        corruptPath,
        readFileSync(corruptPath, "utf8").replace("not-attested", "self-attested"),
      );
      expectLedgerError(
        () =>
          openPublicEvidenceLedger({
            rootDirectory: variants.corruption,
            retentionDays: 30,
          }),
        "corruption",
      );

      const truncatedEvent = readdirSync(join(variants.truncation, "events"))[0]!;
      const truncatedPath = join(variants.truncation, "events", truncatedEvent);
      const complete = readFileSync(truncatedPath, "utf8");
      writeFileSync(truncatedPath, complete.slice(0, -1));
      expectLedgerError(
        () =>
          openPublicEvidenceLedger({
            rootDirectory: variants.truncation,
            retentionDays: 30,
          }),
        "truncation",
      );

      const originalRecord = readdirSync(join(variants.collision, "records"))[0]!;
      cpSync(
        join(variants.collision, "records", originalRecord),
        join(variants.collision, "records", `${"b".repeat(64)}.json`),
      );
      expectLedgerError(
        () =>
          openPublicEvidenceLedger({
            rootDirectory: variants.collision,
            retentionDays: 30,
          }),
        "collision",
      );

      const orphanEvent = readdirSync(join(variants.orphan, "events"))[0]!;
      rmSync(join(variants.orphan, "events", orphanEvent));
      expectLedgerError(
        () =>
          openPublicEvidenceLedger({
            rootDirectory: variants.orphan,
            retentionDays: 30,
          }),
        "truncation",
      );
    } finally {
      for (const target of Object.values(variants)) {
        rmSync(target, { recursive: true, force: true });
      }
    }
  } finally {
    rmSync(base.root, { recursive: true, force: true });
  }
});

test("fails closed on wrong verification material, private paths and retention changes", () => {
  const root = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger({
      rootDirectory: root,
      retentionDays: 30,
      now: () => PERSISTED_AT,
    });
    const fixture = receiptFixture();
    expectLedgerError(
      () =>
        ledger.persistReceipt(fixture.receipt, {
          ...fixture.material,
          resultCore: { ...(fixture.material.resultCore as object), unexpected: true },
        }),
      "invalid-receipt",
    );

    const privateInput = makeReceiptBuildInput();
    const privateMachinePath = ["", "Users", "alice", "private-evidence"].join("/");
    const privateObligations = privateInput.licenceObligations.map((obligation, index) =>
      index === 0 ? { ...obligation, attribution: privateMachinePath } : obligation,
    );
    const privateReceipt = buildInlineReceipt({
      ...privateInput,
      licenceObligations: privateObligations,
    });
    expectLedgerError(
      () =>
        ledger.persistReceipt(privateReceipt, {
          normalisedParameters: privateInput.normalisedParameters,
          resultCore: privateInput.resultCore,
          publicPolicy: privateInput.publicPolicy,
          licenceObligations: privateObligations,
        }),
      "invalid-receipt",
    );

    expectLedgerError(
      () => openPublicEvidenceLedger({ rootDirectory: root, retentionDays: 31 }),
      "retention-mismatch",
    );
    assert.equal(ledger.verify().event_count, 0);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("rejects a raw reconciliation key embedded in a valid receipt before any write", () => {
  const root = temporaryDirectory();
  try {
    const ledger = openPublicEvidenceLedger({ rootDirectory: root, retentionDays: 30 });
    const rawKey = `gis-ai-go:ik:v1:${"a".repeat(64)}`;
    const fixture = receiptFixture(rawKey);
    expectLedgerError(
      () => ledger.persistReceipt(fixture.receipt, fixture.material),
      "invalid-receipt",
    );
    assert.deepEqual(readdirSync(join(root, "records")), []);
    assert.deepEqual(readdirSync(join(root, "events")), []);
    assert.equal(readFileSync(join(root, "ledger.json"), "utf8").includes(rawKey), false);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("rejects unsafe configuration and unrelated roots before creating ledger files", () => {
  const root = temporaryDirectory();
  try {
    writeFileSync(join(root, "unrelated.txt"), "keep\n");
    expectLedgerError(
      () => openPublicEvidenceLedger({ rootDirectory: root }),
      "invalid-configuration",
    );
    assert.deepEqual(readdirSync(root), ["unrelated.txt"]);

    expectLedgerError(
      () =>
        openPublicEvidenceLedger(
          new Proxy({ rootDirectory: join(root, "proxy") }, {}) as {
            rootDirectory: string;
          },
        ),
      "invalid-configuration",
    );
    const accessor = {} as { rootDirectory: string };
    Object.defineProperty(accessor, "rootDirectory", {
      enumerable: true,
      get: () => join(root, "accessor"),
    });
    expectLedgerError(
      () => openPublicEvidenceLedger(accessor),
      "invalid-configuration",
    );
    assert.equal(readdirSync(root).length, 1);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("requires exact private directory and file modes on POSIX", {
  skip: process.platform === "win32",
}, () => {
  const variants = ["root", "records", "events", "descriptor", "record", "event"] as const;
  for (const variant of variants) {
    const populated = populatedLedger();
    try {
      const target = variant === "root"
        ? populated.root
        : variant === "records" || variant === "events"
          ? join(populated.root, variant)
          : variant === "descriptor"
            ? join(populated.root, "ledger.json")
            : variant === "record"
              ? join(populated.root, "records", readdirSync(join(populated.root, "records"))[0]!)
              : join(populated.root, "events", readdirSync(join(populated.root, "events"))[0]!);
      chmodSync(target, variant === "root" || variant === "records" || variant === "events" ? 0o755 : 0o644);
      expectLedgerError(
        () => openPublicEvidenceLedger({ rootDirectory: populated.root, retentionDays: 30 }),
        "corruption",
      );
    } finally {
      rmSync(populated.root, { recursive: true, force: true });
    }
  }
});

test("bulk receipt inspection snapshots closed arrays without invoking accessors", () => {
  const populated = populatedLedger();
  try {
    const ledger = openPublicEvidenceLedger({
      rootDirectory: populated.root,
      retentionDays: 30,
    });
    const receiptId = populated.stored.record.receipt.receipt_id;
    assert.deepEqual(ledger.inspectReceipts([receiptId]), [populated.stored]);

    let reads = 0;
    const accessor = [receiptId];
    Object.defineProperty(accessor, "0", {
      enumerable: true,
      get: () => {
        reads += 1;
        return receiptId;
      },
    });
    expectLedgerError(() => ledger.inspectReceipts(accessor), "invalid-configuration");
    assert.equal(reads, 0);
    expectLedgerError(
      () => ledger.inspectReceipts(new Proxy([receiptId], {})),
      "invalid-configuration",
    );
    const extra = [receiptId] as string[] & { unexpected?: string };
    extra.unexpected = receiptId;
    expectLedgerError(() => ledger.inspectReceipts(extra), "invalid-configuration");
    const sparse = new Array<string>(1);
    expectLedgerError(() => ledger.inspectReceipts(sparse), "invalid-configuration");
  } finally {
    rmSync(populated.root, { recursive: true, force: true });
  }
});
