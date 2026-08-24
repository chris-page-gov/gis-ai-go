import assert from "node:assert/strict";
import {
  chmodSync,
  cpSync,
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

test("creates one path-free linked manifest and restores only after complete verification", () => {
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

    const checker = resolve(
      dirname(fileURLToPath(import.meta.url)),
      "../../../..",
      "scripts/check_evidence_checkpoint.mjs",
    );
    const checked = spawnSync(
      process.execPath,
      [
        checker,
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
      "checkpoint-mismatch",
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
