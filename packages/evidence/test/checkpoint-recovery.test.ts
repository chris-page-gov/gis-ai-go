import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import {
  chmodSync,
  cpSync,
  existsSync,
  linkSync,
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
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { canonicalJson } from "../src/canonical-json.js";
import { contentAddress } from "../src/digest.js";
import {
  EvidenceCheckpointError,
  createEvidenceCheckpoint,
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
  restoreEvidenceCheckpoint,
  verifyEvidenceCheckpoint,
  verifyEvidenceRootsAgainstExternalCheckpoint,
  type CreateEvidenceCheckpointOptions,
} from "../src/index.js";
import {
  CATALOGUE,
  LICENCE_OBLIGATIONS,
  SOFTWARE,
  makeReceiptFixture,
} from "./fixtures.js";
import {
  PUBLIC_READ_REQUEST_ID,
  PUBLIC_READ_TRACE_ID,
  makePublicReadReceiptFixture,
} from "./public-read-fixtures.js";

const KEY = `gis-ai-go:ik:v1:${"1".repeat(64)}`;
const OPENED_AT = new Date("2026-08-24T08:00:00.000Z");
const CHECKPOINT_AT = new Date("2026-08-24T09:00:00.000Z");

interface MutableCheckpointManifest extends Record<string, unknown> {
  checkpoint_id: string;
  created_at: string;
  ledger: {
    root: {
      entry_count: number;
      file_count: number;
      total_bytes: number;
    };
  };
  reconciliation_index: {
    root: {
      entry_count: number;
      file_count: number;
      total_bytes: number;
    };
  };
}

function temporaryParent(): string {
  return mkdtempSync(join(tmpdir(), "gis-ai-go-evidence-checkpoint-"));
}

function openPair(parent: string, openedAt = OPENED_AT) {
  const ledgerRoot = join(parent, "ledger");
  const indexRoot = join(parent, "reconciliation-index");
  const ledger = openPublicEvidenceLedger({
    rootDirectory: ledgerRoot,
    retentionDays: 30,
    now: () => openedAt,
  });
  const reconciliationIndex = openEvidenceReconciliationIndex({
    rootDirectory: indexRoot,
    ledger,
    now: () => openedAt,
  });
  return { ledgerRoot, indexRoot, ledger, reconciliationIndex };
}

function populateLinkedPair(pair: ReturnType<typeof openPair>, key = KEY) {
  const fixture = makePublicReadReceiptFixture();
  const claim = pair.reconciliationIndex.claim({
    idempotencyKey: key,
    operation: "data.query",
    requestId: PUBLIC_READ_REQUEST_ID,
    traceId: PUBLIC_READ_TRACE_ID,
    resourceId: fixture.receipt.resource.resource_id,
    normalisedParametersSha256: fixture.receipt.operation.normalised_parameters.sha256,
  });
  assert.equal(claim.status, "claimed");
  if (claim.status !== "claimed") assert.fail("checkpoint fixture did not acquire its claim");
  pair.reconciliationIndex.resolve(claim.claim, fixture.receipt);
  pair.ledger.persistReceipt(fixture.receipt, fixture.material);
  assert.equal(pair.reconciliationIndex.lookup(key).status, "completed");
}

function checkpointPair(parent: string, pair: ReturnType<typeof openPair>, name = "checkpoint") {
  const checkpointDirectory = join(parent, name);
  const externalCheckpointFile = join(parent, `${name}.external.json`);
  const verification = createEvidenceCheckpoint({
    ledgerRootDirectory: pair.ledgerRoot,
    reconciliationIndexRootDirectory: pair.indexRoot,
    checkpointDirectory,
    externalCheckpointFile,
    stoppedSingleWriter: true,
    now: () => CHECKPOINT_AT,
  });
  return { checkpointDirectory, externalCheckpointFile, verification };
}

function checkpointChecker(): string {
  return resolve(
    dirname(fileURLToPath(import.meta.url)),
    "../../../..",
    "scripts/check_evidence_checkpoint.mjs",
  );
}

function expectStandaloneCheckpointFailure(
  checkpointDirectory: string,
  externalCheckpointFile: string,
  code: EvidenceCheckpointError["code"],
): void {
  const checked = spawnSync(
    process.execPath,
    [
      checkpointChecker(),
      "--checkpoint-directory",
      checkpointDirectory,
      "--external-checkpoint-file",
      externalCheckpointFile,
    ],
    { encoding: "utf8" },
  );
  assert.equal(checked.status, 1, checked.stdout);
  assert.deepEqual(JSON.parse(checked.stderr), {
    schema: "gis-ai-go.evidence-checkpoint-check.v1",
    status: "failed",
    code,
  });
}

function expectCheckpointError(
  run: () => unknown,
  codes: EvidenceCheckpointError["code"] | readonly EvidenceCheckpointError["code"][],
): void {
  const accepted = Array.isArray(codes) ? codes : [codes];
  assert.throws(run, (error: unknown) => {
    assert.ok(error instanceof EvidenceCheckpointError);
    assert.ok(accepted.includes(error.code));
    return true;
  });
}

function copyCheckpoint(source: string, parent: string, name: string): string {
  const destination = join(parent, name);
  cpSync(source, destination, { recursive: true, preserveTimestamps: true });
  normaliseCopiedModes(destination);
  return destination;
}

function normaliseCopiedModes(root: string): void {
  chmodSync(root, 0o700);
  for (const entry of readdirSync(root, { recursive: true, encoding: "utf8" })) {
    const path = join(root, entry);
    chmodSync(path, lstatSync(path).isDirectory() ? 0o700 : 0o600);
  }
}

function rewriteCheckpointDocuments(
  checkpointDirectory: string,
  externalCheckpointFile: string,
  mutate: (manifest: MutableCheckpointManifest) => void,
): void {
  const manifestPath = join(checkpointDirectory, "manifest.json");
  const manifest = JSON.parse(readFileSync(manifestPath, "utf8")) as MutableCheckpointManifest;
  mutate(manifest);
  const core: Record<string, unknown> = { ...manifest };
  delete core.checkpoint_id;
  manifest.checkpoint_id = contentAddress(
    "gis-ai-go:evidence-checkpoint",
    "gis-ai-go.evidence-checkpoint-manifest.v1",
    core,
  );
  const manifestBytes = Buffer.from(`${canonicalJson(manifest)}\n`, "utf8");
  writeFileSync(manifestPath, manifestBytes);
  writeFileSync(
    externalCheckpointFile,
    `${canonicalJson({
      schema: "gis-ai-go.evidence-external-checkpoint.v1",
      created_at: manifest.created_at,
      checkpoint_id: manifest.checkpoint_id,
      manifest_sha256: createHash("sha256").update(manifestBytes).digest("hex"),
      storage_boundary: "external-to-backup-required",
      ledger: manifest.ledger,
      reconciliation_index: manifest.reconciliation_index,
    })}\n`,
  );
}

test("creates one linked manifest, passes a fresh standalone check and restores", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpointDirectory = join(parent, "checkpoint");
    const externalCheckpointFile = join(parent, "checkpoint.external.json");
    expectCheckpointError(
      () =>
        createEvidenceCheckpoint({
          ledgerRootDirectory: pair.ledgerRoot,
          reconciliationIndexRootDirectory: pair.indexRoot,
          checkpointDirectory,
          externalCheckpointFile,
          stoppedSingleWriter: false,
        } as unknown as CreateEvidenceCheckpointOptions),
      "quiescence-required",
    );

    const checkpoint = checkpointPair(parent, pair);
    assert.equal(checkpoint.verification.status, "verified");
    assert.equal(checkpoint.verification.ledger.event_count, 1);
    assert.equal(checkpoint.verification.reconciliation_index.completed_count, 1);
    assert.equal(lstatSync(checkpoint.checkpointDirectory).mode & 0o777, 0o700);
    assert.equal(lstatSync(checkpoint.externalCheckpointFile).mode & 0o777, 0o600);
    const manifestText = readFileSync(
      join(checkpoint.checkpointDirectory, "manifest.json"),
      "utf8",
    );
    assert.equal(manifestText.includes(parent), false);
    assert.equal(manifestText.includes('"source_path":false'), true);
    assert.equal(manifestText.includes('"destination_path":false'), true);
    assert.equal(manifestText.includes('"writer":"stopped-single-writer"'), true);

    const checked = spawnSync(
      process.execPath,
      [
        checkpointChecker(),
        "--checkpoint-directory",
        checkpoint.checkpointDirectory,
        "--external-checkpoint-file",
        checkpoint.externalCheckpointFile,
      ],
      { encoding: "utf8" },
    );
    assert.equal(checked.status, 0, checked.stderr);
    const checkResult = JSON.parse(checked.stdout) as Record<string, unknown>;
    assert.equal(checkResult.status, "passed");
    assert.equal(checkResult.checkpoint_id, checkpoint.verification.checkpoint_id);
    assert.equal(checked.stdout.includes(parent), false);

    const restoredLedgerRoot = join(parent, "restored-ledger");
    const restoredIndexRoot = join(parent, "restored-index");
    mkdirSync(restoredLedgerRoot, { mode: 0o700 });
    mkdirSync(restoredIndexRoot, { mode: 0o700 });
    const restored = restoreEvidenceCheckpoint({
      checkpointDirectory: checkpoint.checkpointDirectory,
      externalCheckpointFile: checkpoint.externalCheckpointFile,
      ledgerDestinationRoot: restoredLedgerRoot,
      reconciliationIndexDestinationRoot: restoredIndexRoot,
      now: () => new Date("2026-08-24T10:00:00.000Z"),
    });
    assert.deepEqual(restored, checkpoint.verification);
    const ledger = openPublicEvidenceLedger({
      rootDirectory: restoredLedgerRoot,
      retentionDays: 30,
    });
    const index = openEvidenceReconciliationIndex({
      rootDirectory: restoredIndexRoot,
      ledger,
    });
    assert.equal(index.lookup(KEY).status, "completed");
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("rejects dot-prefixed children of both source roots but permits disjoint siblings", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    for (const [label, sourceRoot] of [
      ["ledger", pair.ledgerRoot],
      ["index", pair.indexRoot],
    ] as const) {
      const checkpointDirectory = join(parent, `rejected-${label}-checkpoint`);
      const externalCheckpointFile = join(sourceRoot, `..${label}-external.json`);
      expectCheckpointError(
        () =>
          createEvidenceCheckpoint({
            ledgerRootDirectory: pair.ledgerRoot,
            reconciliationIndexRootDirectory: pair.indexRoot,
            checkpointDirectory,
            externalCheckpointFile,
            stoppedSingleWriter: true,
          }),
        "invalid-configuration",
      );
      assert.equal(existsSync(checkpointDirectory), false);
      assert.equal(existsSync(externalCheckpointFile), false);
    }
    assert.equal(pair.ledger.verify().event_count, 1);
    assert.equal(pair.reconciliationIndex.verify().completed_count, 1);

    const accepted = createEvidenceCheckpoint({
      ledgerRootDirectory: pair.ledgerRoot,
      reconciliationIndexRootDirectory: pair.indexRoot,
      checkpointDirectory: join(parent, "..checkpoint"),
      externalCheckpointFile: join(parent, "..checkpoint.external.json"),
      stoppedSingleWriter: true,
      now: () => CHECKPOINT_AT,
    });
    assert.equal(accepted.status, "verified");
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("does not publish after a valid source advance before the snapshot point", () => {
  const parent = temporaryParent();
  try {
    for (const source of ["ledger", "reconciliation-index"] as const) {
      const caseParent = join(parent, source);
      mkdirSync(caseParent, { mode: 0o700 });
      const pair = openPair(caseParent);
      populateLinkedPair(pair);
      const checkpointDirectory = join(caseParent, "late-change-checkpoint");
      const externalCheckpointFile = join(caseParent, "late-change.external.json");
      let changed = false;
      expectCheckpointError(
        () =>
          createEvidenceCheckpoint({
            ledgerRootDirectory: pair.ledgerRoot,
            reconciliationIndexRootDirectory: pair.indexRoot,
            checkpointDirectory,
            externalCheckpointFile,
            stoppedSingleWriter: true,
            now: () => {
              changed = true;
              if (source === "ledger") {
                const fixture = makeReceiptFixture();
                pair.ledger.persistReceipt(fixture.receipt, {
                  normalisedParameters: fixture.normalisedParameters,
                  resultCore: fixture.resultCore,
                  publicPolicy: fixture.publicPolicy,
                  licenceObligations: LICENCE_OBLIGATIONS,
                  expectedAuthorityContext: fixture.authorityContext,
                  expectedPolicyDecision: fixture.policyDecision,
                  expectedCatalogue: CATALOGUE,
                  expectedSoftware: SOFTWARE,
                });
              } else {
                const fixture = makePublicReadReceiptFixture();
                const claim = pair.reconciliationIndex.claim({
                  idempotencyKey: `gis-ai-go:ik:v1:${"2".repeat(64)}`,
                  operation: "data.query",
                  requestId: "request-late-index-advance",
                  traceId: "2123456789abcdef0123456789abcdef",
                  resourceId: fixture.receipt.resource.resource_id,
                  normalisedParametersSha256:
                    fixture.receipt.operation.normalised_parameters.sha256,
                });
                assert.equal(claim.status, "claimed");
              }
              return CHECKPOINT_AT;
            },
          }),
        "corruption",
      );
      assert.equal(changed, true);
      assert.equal(existsSync(join(checkpointDirectory, "manifest.json")), true);
      assert.equal(existsSync(externalCheckpointFile), false);
      expectStandaloneCheckpointFailure(
        checkpointDirectory,
        externalCheckpointFile,
        "io-failure",
      );
      assert.equal(pair.ledger.verify().event_count, source === "ledger" ? 2 : 1);
      assert.equal(
        pair.reconciliationIndex.verify().pending_count,
        source === "reconciliation-index" ? 1 : 0,
      );
    }
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("keeps a checkpoint unverifiable when its external commit path is claimed late", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpointDirectory = join(parent, "publication-collision-checkpoint");
    const externalCheckpointFile = join(parent, "publication-collision.external.json");
    expectCheckpointError(
      () =>
        createEvidenceCheckpoint({
          ledgerRootDirectory: pair.ledgerRoot,
          reconciliationIndexRootDirectory: pair.indexRoot,
          checkpointDirectory,
          externalCheckpointFile,
          stoppedSingleWriter: true,
          now: () => {
            writeFileSync(externalCheckpointFile, "", { mode: 0o600 });
            return CHECKPOINT_AT;
          },
        }),
      "collision",
    );
    assert.equal(existsSync(join(checkpointDirectory, "manifest.json")), true);
    expectStandaloneCheckpointFailure(
      checkpointDirectory,
      externalCheckpointFile,
      "corruption",
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("enforces manifest-derived entry and aggregate-byte bounds before hostile reads", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpoint = checkpointPair(parent, pair);

    const extraEntry = copyCheckpoint(checkpoint.checkpointDirectory, parent, "extra-entry");
    const extraEntryExternal = join(parent, "extra-entry.external.json");
    cpSync(checkpoint.externalCheckpointFile, extraEntryExternal, { preserveTimestamps: true });
    chmodSync(extraEntryExternal, 0o600);
    writeFileSync(
      join(extraEntry, "reconciliation-index", "resolutions", `${"f".repeat(64)}.json`),
      "untrusted bytes that must not be read\n",
      { mode: 0o000 },
    );
    assert.throws(
      () =>
        verifyEvidenceCheckpoint({
          checkpointDirectory: extraEntry,
          externalCheckpointFile: extraEntryExternal,
        }),
      (error: unknown) => {
        assert.ok(error instanceof EvidenceCheckpointError);
        assert.equal(error.code, "corruption");
        assert.match(error.message, /fixed entry bound/u);
        return true;
      },
    );

    const byteUndercount = copyCheckpoint(
      checkpoint.checkpointDirectory,
      parent,
      "byte-undercount",
    );
    const byteUndercountExternal = join(parent, "byte-undercount.external.json");
    cpSync(checkpoint.externalCheckpointFile, byteUndercountExternal, {
      preserveTimestamps: true,
    });
    chmodSync(byteUndercountExternal, 0o600);
    rewriteCheckpointDocuments(byteUndercount, byteUndercountExternal, (manifest) => {
      manifest.ledger.root.total_bytes -= 1;
    });
    assert.throws(
      () =>
        verifyEvidenceCheckpoint({
          checkpointDirectory: byteUndercount,
          externalCheckpointFile: byteUndercountExternal,
        }),
      (error: unknown) => {
        assert.ok(error instanceof EvidenceCheckpointError);
        assert.equal(error.code, "corruption");
        assert.match(error.message, /fixed byte bound/u);
        return true;
      },
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("rejects role-specific declared traversal ceilings without large fixtures", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpoint = checkpointPair(parent, pair);
    for (const [name, mutate] of [
      [
        "ledger-byte-limit",
        (manifest: MutableCheckpointManifest): void => {
          manifest.ledger.root.total_bytes = 4_259_840_016_385;
        },
      ],
      [
        "index-byte-limit",
        (manifest: MutableCheckpointManifest): void => {
          manifest.reconciliation_index.root.total_bytes = 201_342_977;
        },
      ],
    ] as const) {
      const checkpointDirectory = copyCheckpoint(
        checkpoint.checkpointDirectory,
        parent,
        name,
      );
      const externalCheckpointFile = join(parent, `${name}.external.json`);
      cpSync(checkpoint.externalCheckpointFile, externalCheckpointFile, {
        preserveTimestamps: true,
      });
      chmodSync(externalCheckpointFile, 0o600);
      rewriteCheckpointDocuments(checkpointDirectory, externalCheckpointFile, mutate);
      expectCheckpointError(
        () =>
          verifyEvidenceCheckpoint({ checkpointDirectory, externalCheckpointFile }),
        "corruption",
      );
    }
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("rejects incomplete, cross-paired, tampered, linked and broader-mode backups", () => {
  const parent = temporaryParent();
  try {
    const firstParent = join(parent, "first");
    const secondParent = join(parent, "second");
    mkdirSync(firstParent, { mode: 0o700 });
    mkdirSync(secondParent, { mode: 0o700 });
    const firstPair = openPair(firstParent, OPENED_AT);
    const secondPair = openPair(secondParent, new Date("2026-08-24T08:05:00.000Z"));
    populateLinkedPair(firstPair, KEY);
    populateLinkedPair(secondPair, `gis-ai-go:ik:v1:${"2".repeat(64)}`);
    const first = checkpointPair(firstParent, firstPair);
    const second = checkpointPair(secondParent, secondPair);

    const incomplete = copyCheckpoint(first.checkpointDirectory, parent, "incomplete");
    const missingEvent = readdirSync(join(incomplete, "ledger", "events"))[0];
    assert.ok(missingEvent);
    rmSync(join(incomplete, "ledger", "events", missingEvent));
    expectCheckpointError(
      () =>
        verifyEvidenceCheckpoint({
          checkpointDirectory: incomplete,
          externalCheckpointFile: first.externalCheckpointFile,
        }),
      ["checkpoint-mismatch", "io-failure"],
    );

    const crossPaired = copyCheckpoint(first.checkpointDirectory, parent, "cross-paired");
    rmSync(join(crossPaired, "ledger"), { recursive: true });
    cpSync(join(second.checkpointDirectory, "ledger"), join(crossPaired, "ledger"), {
      recursive: true,
      preserveTimestamps: true,
    });
    normaliseCopiedModes(join(crossPaired, "ledger"));
    expectCheckpointError(
      () =>
        verifyEvidenceCheckpoint({
          checkpointDirectory: crossPaired,
          externalCheckpointFile: first.externalCheckpointFile,
        }),
      "checkpoint-mismatch",
    );

    const tampered = copyCheckpoint(first.checkpointDirectory, parent, "tampered");
    const descriptorPath = join(tampered, "ledger", "ledger.json");
    writeFileSync(descriptorPath, `${readFileSync(descriptorPath, "utf8")} `, { mode: 0o600 });
    expectCheckpointError(
      () =>
        verifyEvidenceCheckpoint({
          checkpointDirectory: tampered,
          externalCheckpointFile: first.externalCheckpointFile,
        }),
      ["corruption", "checkpoint-mismatch"],
    );

    const linked = copyCheckpoint(first.checkpointDirectory, parent, "linked");
    const linkedEvent = readdirSync(join(linked, "ledger", "events"))[0];
    assert.ok(linkedEvent);
    const linkedEventPath = join(linked, "ledger", "events", linkedEvent);
    rmSync(linkedEventPath);
    symlinkSync(join("..", "ledger.json"), linkedEventPath);
    expectCheckpointError(
      () =>
        verifyEvidenceCheckpoint({
          checkpointDirectory: linked,
          externalCheckpointFile: first.externalCheckpointFile,
        }),
      ["corruption", "io-failure"],
    );

    const broaderMode = copyCheckpoint(first.checkpointDirectory, parent, "broader-mode");
    chmodSync(join(broaderMode, "ledger", "ledger.json"), 0o640);
    expectCheckpointError(
      () =>
        verifyEvidenceCheckpoint({
          checkpointDirectory: broaderMode,
          externalCheckpointFile: first.externalCheckpointFile,
        }),
      ["corruption", "io-failure"],
    );

    const hardLinked = copyCheckpoint(first.checkpointDirectory, parent, "hard-linked");
    const hardLinkedEvent = readdirSync(join(hardLinked, "ledger", "events"))[0];
    assert.ok(hardLinkedEvent);
    const hardLinkedEventPath = join(hardLinked, "ledger", "events", hardLinkedEvent);
    rmSync(hardLinkedEventPath);
    linkSync(join(hardLinked, "ledger", "ledger.json"), hardLinkedEventPath);
    expectCheckpointError(
      () =>
        verifyEvidenceCheckpoint({
          checkpointDirectory: hardLinked,
          externalCheckpointFile: first.externalCheckpointFile,
        }),
      ["corruption", "io-failure"],
    );

    expectCheckpointError(
      () =>
        verifyEvidenceCheckpoint({
          checkpointDirectory: first.checkpointDirectory,
          externalCheckpointFile: second.externalCheckpointFile,
        }),
      "checkpoint-mismatch",
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("refuses non-empty recovery roots before copying either member", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpoint = checkpointPair(parent, pair);
    const ledgerDestinationRoot = join(parent, "destination-ledger");
    const reconciliationIndexDestinationRoot = join(parent, "destination-index");
    mkdirSync(ledgerDestinationRoot, { mode: 0o700 });
    mkdirSync(reconciliationIndexDestinationRoot, { mode: 0o700 });
    writeFileSync(join(reconciliationIndexDestinationRoot, "unrelated"), "blocked", {
      mode: 0o600,
    });
    expectCheckpointError(
      () =>
        restoreEvidenceCheckpoint({
          checkpointDirectory: checkpoint.checkpointDirectory,
          externalCheckpointFile: checkpoint.externalCheckpointFile,
          ledgerDestinationRoot,
          reconciliationIndexDestinationRoot,
        }),
      "destination-not-empty",
    );
    assert.deepEqual(readdirSync(ledgerDestinationRoot), []);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("external checkpoint detects a structurally valid complete ledger tail deletion", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const inlineFixture = makeReceiptFixture();
    pair.ledger.persistReceipt(inlineFixture.receipt, {
      normalisedParameters: inlineFixture.normalisedParameters,
      resultCore: inlineFixture.resultCore,
      publicPolicy: inlineFixture.publicPolicy,
      licenceObligations: LICENCE_OBLIGATIONS,
      expectedAuthorityContext: inlineFixture.authorityContext,
      expectedPolicyDecision: inlineFixture.policyDecision,
      expectedCatalogue: CATALOGUE,
      expectedSoftware: SOFTWARE,
    });
    assert.equal(pair.ledger.verify().event_count, 2);
    const checkpoint = checkpointPair(parent, pair);
    assert.equal(
      verifyEvidenceRootsAgainstExternalCheckpoint({
        ledgerRootDirectory: pair.ledgerRoot,
        reconciliationIndexRootDirectory: pair.indexRoot,
        externalCheckpointFile: checkpoint.externalCheckpointFile,
      }).status,
      "verified",
    );

    const truncatedParent = join(parent, "truncated");
    mkdirSync(truncatedParent, { mode: 0o700 });
    const truncatedLedgerRoot = join(truncatedParent, "ledger");
    const truncatedIndexRoot = join(truncatedParent, "reconciliation-index");
    cpSync(pair.ledgerRoot, truncatedLedgerRoot, { recursive: true, preserveTimestamps: true });
    cpSync(pair.indexRoot, truncatedIndexRoot, { recursive: true, preserveTimestamps: true });
    normaliseCopiedModes(truncatedLedgerRoot);
    normaliseCopiedModes(truncatedIndexRoot);
    const eventNames = readdirSync(join(truncatedLedgerRoot, "events")).sort();
    const tailName = eventNames.at(-1);
    assert.ok(tailName);
    const tail = JSON.parse(
      readFileSync(join(truncatedLedgerRoot, "events", tailName), "utf8"),
    ) as { readonly record_id: string };
    rmSync(join(truncatedLedgerRoot, "events", tailName));
    rmSync(
      join(
        truncatedLedgerRoot,
        "records",
        `${tail.record_id.slice(tail.record_id.lastIndexOf(":") + 1)}.json`,
      ),
    );

    const truncatedLedger = openPublicEvidenceLedger({
      rootDirectory: truncatedLedgerRoot,
      retentionDays: 30,
    });
    const truncatedIndex = openEvidenceReconciliationIndex({
      rootDirectory: truncatedIndexRoot,
      ledger: truncatedLedger,
    });
    assert.equal(truncatedLedger.verify().event_count, 1);
    assert.equal(truncatedIndex.verify().completed_count, 1);
    expectCheckpointError(
      () =>
        verifyEvidenceRootsAgainstExternalCheckpoint({
          ledgerRootDirectory: truncatedLedgerRoot,
          reconciliationIndexRootDirectory: truncatedIndexRoot,
          externalCheckpointFile: checkpoint.externalCheckpointFile,
        }),
      "checkpoint-mismatch",
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});
