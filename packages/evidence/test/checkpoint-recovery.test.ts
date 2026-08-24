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
  reconcileEvidenceCheckpointPublication,
  restoreEvidenceCheckpoint,
  verifyEvidenceCheckpoint,
  verifyEvidenceRootsAgainstExternalCheckpoint,
  type CreateEvidenceCheckpointOptions,
  type ReconcileEvidenceCheckpointPublicationOptions,
} from "../src/index.js";
import {
  withEvidenceCheckpointPublicationHookForTest,
} from "../src/checkpoint-publication-test-seam.js";
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

function checkpointPublicationReconciler(): string {
  return resolve(
    dirname(fileURLToPath(import.meta.url)),
    "../../../..",
    "scripts/reconcile_evidence_checkpoint_publication.mjs",
  );
}

function checkpointTransactionDirectory(externalCheckpointFile: string): string {
  const canonicalTarget = resolve(externalCheckpointFile);
  const digest = createHash("sha256")
    .update("gis-ai-go.evidence-external-checkpoint-transaction.v1\0", "utf8")
    .update(canonicalTarget, "utf8")
    .digest("hex");
  return join(
    dirname(canonicalTarget),
    `.gis-ai-go-evidence-checkpoint-transaction-${digest}`,
  );
}

function checkpointTransactionEntries(parent: string): string[] {
  return readdirSync(parent)
    .filter((entry) => entry.startsWith(".gis-ai-go-evidence-checkpoint-transaction-"))
    .sort();
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
    assert.equal(
      checkResult.publication_durability,
      "not-established-by-read-only-check",
    );
    assert.equal(checkResult.checkpoint_id, checkpoint.verification.checkpoint_id);
    assert.equal(checked.stdout.includes(parent), false);
    assert.deepEqual(checkpointTransactionEntries(parent), []);

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

test("keeps the declared snapshot when a writer violates quiescence after its snapshot point", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpointDirectory = join(parent, "post-snapshot-write-checkpoint");
    const externalCheckpointFile = join(parent, "post-snapshot-write.external.json");
    let advanced = false;
    const options = withEvidenceCheckpointPublicationHookForTest(
      {
        ledgerRootDirectory: pair.ledgerRoot,
        reconciliationIndexRootDirectory: pair.indexRoot,
        checkpointDirectory,
        externalCheckpointFile,
        stoppedSingleWriter: true as const,
        now: () => CHECKPOINT_AT,
      },
      ({ phase }) => {
        if (phase !== "before-target-link" || advanced) return;
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
        advanced = true;
      },
    );
    const created = createEvidenceCheckpoint(options);
    assert.equal(advanced, true);
    assert.equal(created.ledger.event_count, 1);
    assert.equal(pair.ledger.verify().event_count, 2);
    assert.equal(
      verifyEvidenceCheckpoint({ checkpointDirectory, externalCheckpointFile }).ledger
        .event_count,
      1,
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("keeps the final path absent when the closed stage cannot be synchronised", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpointDirectory = join(parent, "stage-fsync-checkpoint");
    const externalCheckpointFile = join(parent, "stage-fsync.external.json");
    let observedStagePath: string | undefined;
    const options = withEvidenceCheckpointPublicationHookForTest(
      {
        ledgerRootDirectory: pair.ledgerRoot,
        reconciliationIndexRootDirectory: pair.indexRoot,
        checkpointDirectory,
        externalCheckpointFile,
        stoppedSingleWriter: true as const,
        now: () => CHECKPOINT_AT,
      },
      ({ phase, stagePath, targetPath }) => {
        if (phase !== "before-stage-file-sync") return;
        observedStagePath = stagePath;
        assert.equal(targetPath, externalCheckpointFile);
        assert.equal(existsSync(stagePath), true);
        assert.equal(existsSync(targetPath), false);
        expectCheckpointError(
          () => verifyEvidenceCheckpoint({ checkpointDirectory, externalCheckpointFile }),
          "io-failure",
        );
        const error = new Error("simulated stage file fsync failure") as NodeJS.ErrnoException;
        error.code = "EIO";
        throw error;
      },
    );
    expectCheckpointError(() => createEvidenceCheckpoint(options), "io-failure");
    assert.ok(observedStagePath);
    assert.equal(existsSync(externalCheckpointFile), false);
    assert.equal(existsSync(observedStagePath), false);
    assert.deepEqual(checkpointTransactionEntries(parent), []);
    expectStandaloneCheckpointFailure(
      checkpointDirectory,
      externalCheckpointFile,
      "io-failure",
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("retains an unverifiable linked state until indeterminate publication is reconciled", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpointDirectory = join(parent, "linked-publication-checkpoint");
    const externalCheckpointFile = join(parent, "linked-publication.external.json");
    let observedStagePath: string | undefined;
    let rejectedWhileVisible = false;
    const options = withEvidenceCheckpointPublicationHookForTest(
      {
        ledgerRootDirectory: pair.ledgerRoot,
        reconciliationIndexRootDirectory: pair.indexRoot,
        checkpointDirectory,
        externalCheckpointFile,
        stoppedSingleWriter: true as const,
        now: () => CHECKPOINT_AT,
      },
      ({ phase, stagePath, targetPath }) => {
        observedStagePath = stagePath;
        if (phase === "after-target-link") {
          assert.equal(existsSync(targetPath), true);
          assert.equal(lstatSync(stagePath).nlink, 2);
          assert.equal(lstatSync(targetPath).nlink, 2);
          expectCheckpointError(
            () => verifyEvidenceCheckpoint({ checkpointDirectory, externalCheckpointFile }),
            "corruption",
          );
          rejectedWhileVisible = true;
        }
        if (phase === "before-target-parent-sync") {
          const error = new Error(
            "simulated target parent-directory fsync failure",
          ) as NodeJS.ErrnoException;
          error.code = "EIO";
          throw error;
        }
      },
    );
    expectCheckpointError(
      () => createEvidenceCheckpoint(options),
      "publication-indeterminate",
    );
    assert.equal(rejectedWhileVisible, true);
    assert.ok(observedStagePath);
    assert.equal(lstatSync(observedStagePath).nlink, 2);
    assert.equal(lstatSync(externalCheckpointFile).nlink, 2);
    assert.equal(lstatSync(observedStagePath).ino, lstatSync(externalCheckpointFile).ino);
    expectStandaloneCheckpointFailure(
      checkpointDirectory,
      externalCheckpointFile,
      "corruption",
    );

    const reconciled = spawnSync(
      process.execPath,
      [
        checkpointPublicationReconciler(),
        "--checkpoint-directory",
        checkpointDirectory,
        "--external-checkpoint-file",
        externalCheckpointFile,
        "--stopped-single-writer-confirmed",
        "--exclusive-publication-owner-confirmed",
      ],
      { encoding: "utf8" },
    );
    assert.equal(reconciled.status, 0, reconciled.stderr);
    const result = JSON.parse(reconciled.stdout) as Record<string, unknown>;
    assert.equal(result.status, "passed");
    assert.equal(
      result.publication_durability,
      "file-and-parent-directory-synchronised",
    );
    assert.equal(lstatSync(externalCheckpointFile).nlink, 1);
    assert.equal(existsSync(observedStagePath), false);
    assert.equal(
      verifyEvidenceCheckpoint({ checkpointDirectory, externalCheckpointFile }).status,
      "verified",
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("contains a lost hard-link response as indeterminate linked publication", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpointDirectory = join(parent, "lost-link-response-checkpoint");
    const externalCheckpointFile = join(parent, "lost-link-response.external.json");
    let stagePath: string | undefined;
    const options = withEvidenceCheckpointPublicationHookForTest(
      {
        ledgerRootDirectory: pair.ledgerRoot,
        reconciliationIndexRootDirectory: pair.indexRoot,
        checkpointDirectory,
        externalCheckpointFile,
        stoppedSingleWriter: true as const,
        now: () => CHECKPOINT_AT,
      },
      (state) => {
        stagePath = state.stagePath;
        if (state.phase !== "before-target-link") return;
        linkSync(state.stagePath, state.targetPath);
        const error = new Error("simulated lost hard-link response") as NodeJS.ErrnoException;
        error.code = "EIO";
        throw error;
      },
    );
    expectCheckpointError(
      () => createEvidenceCheckpoint(options),
      "publication-indeterminate",
    );
    assert.ok(stagePath);
    assert.equal(lstatSync(stagePath).nlink, 2);
    assert.equal(lstatSync(externalCheckpointFile).nlink, 2);
    expectStandaloneCheckpointFailure(
      checkpointDirectory,
      externalCheckpointFile,
      "corruption",
    );
    assert.equal(
      reconcileEvidenceCheckpointPublication({
        checkpointDirectory,
        exclusivePublicationOwner: true,
        externalCheckpointFile,
        stoppedSingleWriter: true,
      }).status,
      "verified",
    );
    assert.equal(existsSync(stagePath), false);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("keeps linked recovery indeterminate when its reopen has an I/O fault", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpointDirectory = join(parent, "linked-reopen-checkpoint");
    const externalCheckpointFile = join(parent, "linked-reopen.external.json");
    let stagePath: string | undefined;
    const creatingOptions = withEvidenceCheckpointPublicationHookForTest(
      {
        ledgerRootDirectory: pair.ledgerRoot,
        reconciliationIndexRootDirectory: pair.indexRoot,
        checkpointDirectory,
        externalCheckpointFile,
        stoppedSingleWriter: true as const,
        now: () => CHECKPOINT_AT,
      },
      (state) => {
        stagePath = state.stagePath;
        if (state.phase !== "before-target-parent-sync") return;
        const error = new Error(
          "simulated initial target-parent fsync failure",
        ) as NodeJS.ErrnoException;
        error.code = "EIO";
        throw error;
      },
    );
    expectCheckpointError(
      () => createEvidenceCheckpoint(creatingOptions),
      "publication-indeterminate",
    );
    assert.ok(stagePath);
    assert.equal(lstatSync(stagePath).nlink, 2);
    assert.equal(lstatSync(externalCheckpointFile).nlink, 2);

    const reconcilingOptions = withEvidenceCheckpointPublicationHookForTest(
      {
        checkpointDirectory,
        exclusivePublicationOwner: true as const,
        externalCheckpointFile,
        stoppedSingleWriter: true as const,
      },
      ({ phase }) => {
        if (phase !== "before-linked-recovery-reopen") return;
        const error = new Error(
          "simulated linked recovery reopen I/O fault",
        ) as NodeJS.ErrnoException;
        error.code = "EIO";
        throw error;
      },
    );
    expectCheckpointError(
      () => reconcileEvidenceCheckpointPublication(reconcilingOptions),
      "publication-indeterminate",
    );
    assert.equal(lstatSync(stagePath).nlink, 2);
    assert.equal(lstatSync(externalCheckpointFile).nlink, 2);
    expectStandaloneCheckpointFailure(
      checkpointDirectory,
      externalCheckpointFile,
      "corruption",
    );
    assert.equal(
      reconcileEvidenceCheckpointPublication({
        checkpointDirectory,
        exclusivePublicationOwner: true,
        externalCheckpointFile,
        stoppedSingleWriter: true,
      }).status,
      "verified",
    );
    assert.equal(existsSync(stagePath), false);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("reconciles a durable target left linked when staging removal fails", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpointDirectory = join(parent, "unlink-failure-checkpoint");
    const externalCheckpointFile = join(parent, "unlink-failure.external.json");
    let stagePath: string | undefined;
    let targetWasSynchronised = false;
    const options = withEvidenceCheckpointPublicationHookForTest(
      {
        ledgerRootDirectory: pair.ledgerRoot,
        reconciliationIndexRootDirectory: pair.indexRoot,
        checkpointDirectory,
        externalCheckpointFile,
        stoppedSingleWriter: true as const,
        now: () => CHECKPOINT_AT,
      },
      (state) => {
        stagePath = state.stagePath;
        if (state.phase === "after-target-parent-sync") {
          targetWasSynchronised = true;
        }
        if (state.phase === "before-stage-unlink") {
          throw new Error("simulated staging unlink failure");
        }
      },
    );
    expectCheckpointError(
      () => createEvidenceCheckpoint(options),
      "publication-indeterminate",
    );
    assert.equal(targetWasSynchronised, true);
    assert.ok(stagePath);
    assert.equal(lstatSync(stagePath).nlink, 2);
    assert.equal(lstatSync(externalCheckpointFile).nlink, 2);
    expectStandaloneCheckpointFailure(
      checkpointDirectory,
      externalCheckpointFile,
      "corruption",
    );
    assert.equal(
      reconcileEvidenceCheckpointPublication({
        checkpointDirectory,
        exclusivePublicationOwner: true,
        externalCheckpointFile,
        stoppedSingleWriter: true,
      }).status,
      "verified",
    );
    assert.equal(existsSync(stagePath), false);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("reports clean-up durability ambiguity without hiding currently verified content", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpointDirectory = join(parent, "cleanup-sync-checkpoint");
    const externalCheckpointFile = join(parent, "cleanup-sync.external.json");
    let observedStagePath: string | undefined;
    const options = withEvidenceCheckpointPublicationHookForTest(
      {
        ledgerRootDirectory: pair.ledgerRoot,
        reconciliationIndexRootDirectory: pair.indexRoot,
        checkpointDirectory,
        externalCheckpointFile,
        stoppedSingleWriter: true as const,
        now: () => CHECKPOINT_AT,
      },
      ({ phase, stagePath }) => {
        observedStagePath = stagePath;
        if (phase !== "before-cleanup-parent-sync") return;
        const error = new Error(
          "simulated staging clean-up directory fsync failure",
        ) as NodeJS.ErrnoException;
        error.code = "EIO";
        throw error;
      },
    );
    expectCheckpointError(
      () => createEvidenceCheckpoint(options),
      "publication-indeterminate",
    );
    assert.ok(observedStagePath);
    assert.equal(existsSync(observedStagePath), false);
    assert.equal(lstatSync(externalCheckpointFile).nlink, 1);
    assert.equal(
      verifyEvidenceCheckpoint({ checkpointDirectory, externalCheckpointFile }).status,
      "verified",
    );

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
    assert.equal(checked.status, 0, checked.stderr);
    assert.equal(
      (JSON.parse(checked.stdout) as Record<string, unknown>).publication_durability,
      "not-established-by-read-only-check",
    );
    assert.equal(
      reconcileEvidenceCheckpointPublication({
        checkpointDirectory,
        exclusivePublicationOwner: true,
        externalCheckpointFile,
        stoppedSingleWriter: true,
      }).status,
      "verified",
    );
    assert.deepEqual(checkpointTransactionEntries(parent), []);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("reports target-only durability ambiguity after transaction-directory removal", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpointDirectory = join(parent, "target-only-checkpoint");
    const externalCheckpointFile = join(parent, "target-only.external.json");
    const transactionDirectory = checkpointTransactionDirectory(externalCheckpointFile);
    let removalObserved = false;
    const options = withEvidenceCheckpointPublicationHookForTest(
      {
        ledgerRootDirectory: pair.ledgerRoot,
        reconciliationIndexRootDirectory: pair.indexRoot,
        checkpointDirectory,
        externalCheckpointFile,
        stoppedSingleWriter: true as const,
        now: () => CHECKPOINT_AT,
      },
      ({ phase }) => {
        if (phase !== "after-transaction-directory-remove") return;
        removalObserved = true;
        assert.equal(existsSync(transactionDirectory), false);
        assert.equal(lstatSync(externalCheckpointFile).nlink, 1);
        const error = new Error(
          "simulated target-parent fsync failure after transaction removal",
        ) as NodeJS.ErrnoException;
        error.code = "EIO";
        throw error;
      },
    );
    expectCheckpointError(
      () => createEvidenceCheckpoint(options),
      "publication-indeterminate",
    );
    assert.equal(removalObserved, true);
    assert.equal(existsSync(transactionDirectory), false);
    assert.equal(
      verifyEvidenceCheckpoint({ checkpointDirectory, externalCheckpointFile }).status,
      "verified",
    );
    assert.equal(
      reconcileEvidenceCheckpointPublication({
        checkpointDirectory,
        exclusivePublicationOwner: true,
        externalCheckpointFile,
        stoppedSingleWriter: true,
      }).status,
      "verified",
    );
    assert.deepEqual(checkpointTransactionEntries(parent), []);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("keeps a checkpoint unverifiable when its external commit path is claimed by partial data", () => {
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

test("converges on an exact canonical late claimant as idempotent verified success", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const reference = checkpointPair(parent, pair, "reference-checkpoint");
    const checkpointDirectory = join(parent, "exact-claimant-checkpoint");
    const externalCheckpointFile = join(parent, "exact-claimant.external.json");
    let claimantInode: number | undefined;
    const expectedBytes = readFileSync(reference.externalCheckpointFile);
    const created = createEvidenceCheckpoint({
      ledgerRootDirectory: pair.ledgerRoot,
      reconciliationIndexRootDirectory: pair.indexRoot,
      checkpointDirectory,
      externalCheckpointFile,
      stoppedSingleWriter: true,
      now: () => {
        cpSync(reference.externalCheckpointFile, externalCheckpointFile, {
          preserveTimestamps: true,
        });
        chmodSync(externalCheckpointFile, 0o600);
        claimantInode = lstatSync(externalCheckpointFile).ino;
        return CHECKPOINT_AT;
      },
    });
    assert.equal(created.status, "verified");
    assert.equal(created.checkpoint_id, reference.verification.checkpoint_id);
    assert.equal(lstatSync(externalCheckpointFile).ino, claimantInode);
    assert.deepEqual(readFileSync(externalCheckpointFile), expectedBytes);
    assert.deepEqual(checkpointTransactionEntries(parent), []);

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
    assert.equal(checked.status, 0, checked.stderr);
    assert.equal(
      (JSON.parse(checked.stdout) as Record<string, unknown>).checkpoint_id,
      created.checkpoint_id,
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("reconciles an exact late claimant after its directory durability is indeterminate", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const reference = checkpointPair(parent, pair, "uncertain-reference");
    const checkpointDirectory = join(parent, "uncertain-exact-checkpoint");
    const externalCheckpointFile = join(parent, "uncertain-exact.external.json");
    let stagePath: string | undefined;
    let claimed = false;
    const options = withEvidenceCheckpointPublicationHookForTest(
      {
        ledgerRootDirectory: pair.ledgerRoot,
        reconciliationIndexRootDirectory: pair.indexRoot,
        checkpointDirectory,
        externalCheckpointFile,
        stoppedSingleWriter: true as const,
        now: () => CHECKPOINT_AT,
      },
      (state) => {
        stagePath = state.stagePath;
        if (state.phase === "before-target-link") {
          cpSync(reference.externalCheckpointFile, externalCheckpointFile, {
            preserveTimestamps: true,
          });
          chmodSync(externalCheckpointFile, 0o600);
          claimed = true;
        }
        if (state.phase === "before-target-parent-sync") {
          const error = new Error(
            "simulated exact claimant directory fsync failure",
          ) as NodeJS.ErrnoException;
          error.code = "EIO";
          throw error;
        }
      },
    );
    expectCheckpointError(
      () => createEvidenceCheckpoint(options),
      "publication-indeterminate",
    );
    assert.equal(claimed, true);
    assert.ok(stagePath);
    assert.equal(lstatSync(stagePath).nlink, 1);
    assert.equal(lstatSync(externalCheckpointFile).nlink, 1);
    assert.equal(
      verifyEvidenceCheckpoint({ checkpointDirectory, externalCheckpointFile }).status,
      "verified",
    );
    assert.equal(
      reconcileEvidenceCheckpointPublication({
        checkpointDirectory,
        exclusivePublicationOwner: true,
        externalCheckpointFile,
        stoppedSingleWriter: true,
      }).status,
      "verified",
    );
    assert.equal(existsSync(stagePath), false);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("preserves an exact late claimant when inspection or verification has an I/O fault", () => {
  const parent = temporaryParent();
  try {
    for (const faultPhase of [
      "before-existing-target-open",
      "before-existing-target-verification",
    ] as const) {
      const caseParent = join(parent, faultPhase);
      mkdirSync(caseParent, { mode: 0o700 });
      const pair = openPair(caseParent);
      populateLinkedPair(pair);
      const reference = checkpointPair(caseParent, pair, "reference");
      const checkpointDirectory = join(caseParent, "checkpoint");
      const externalCheckpointFile = join(caseParent, "external.json");
      let stagePath: string | undefined;
      const options = withEvidenceCheckpointPublicationHookForTest(
        {
          ledgerRootDirectory: pair.ledgerRoot,
          reconciliationIndexRootDirectory: pair.indexRoot,
          checkpointDirectory,
          externalCheckpointFile,
          stoppedSingleWriter: true as const,
          now: () => CHECKPOINT_AT,
        },
        (state) => {
          stagePath = state.stagePath;
          if (state.phase === "before-target-link") {
            cpSync(reference.externalCheckpointFile, externalCheckpointFile, {
              preserveTimestamps: true,
            });
            chmodSync(externalCheckpointFile, 0o600);
          }
          if (state.phase === faultPhase) {
            const error = new Error(
              "simulated exact claimant inspection I/O fault",
            ) as NodeJS.ErrnoException;
            error.code = "EIO";
            throw error;
          }
        },
      );
      expectCheckpointError(
        () => createEvidenceCheckpoint(options),
        "publication-indeterminate",
      );
      assert.ok(stagePath);
      assert.equal(lstatSync(stagePath).nlink, 1);
      assert.equal(
        verifyEvidenceCheckpoint({ checkpointDirectory, externalCheckpointFile }).status,
        "verified",
      );
      assert.equal(
        reconcileEvidenceCheckpointPublication({
          checkpointDirectory,
          exclusivePublicationOwner: true,
          externalCheckpointFile,
          stoppedSingleWriter: true,
        }).status,
        "verified",
      );
      assert.equal(existsSync(stagePath), false);
    }
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("rejects and preserves different, linked and special late claimants", () => {
  const parent = temporaryParent();
  try {
    for (const claimant of [
      "different",
      "symbolic-link",
      "hard-link",
      "directory",
    ] as const) {
      const caseParent = join(parent, claimant);
      mkdirSync(caseParent, { mode: 0o700 });
      const pair = openPair(caseParent);
      populateLinkedPair(pair);
      const checkpointDirectory = join(caseParent, "checkpoint");
      const externalCheckpointFile = join(caseParent, "external.json");
      const linkTarget = join(caseParent, "link-target.json");
      let differentReference: string | undefined;
      if (claimant === "different") {
        differentReference = join(caseParent, "different-reference.external.json");
        createEvidenceCheckpoint({
          ledgerRootDirectory: pair.ledgerRoot,
          reconciliationIndexRootDirectory: pair.indexRoot,
          checkpointDirectory: join(caseParent, "different-reference-checkpoint"),
          externalCheckpointFile: differentReference,
          stoppedSingleWriter: true,
          now: () => new Date("2026-08-24T09:01:00.000Z"),
        });
      }
      if (claimant === "symbolic-link" || claimant === "hard-link") {
        writeFileSync(linkTarget, "{}\n", { mode: 0o600 });
      }
      expectCheckpointError(
        () =>
          createEvidenceCheckpoint({
            ledgerRootDirectory: pair.ledgerRoot,
            reconciliationIndexRootDirectory: pair.indexRoot,
            checkpointDirectory,
            externalCheckpointFile,
            stoppedSingleWriter: true,
            now: () => {
              if (claimant === "different") {
                assert.ok(differentReference);
                cpSync(differentReference, externalCheckpointFile, {
                  preserveTimestamps: true,
                });
                chmodSync(externalCheckpointFile, 0o600);
              } else if (claimant === "symbolic-link") {
                symlinkSync(linkTarget, externalCheckpointFile);
              } else if (claimant === "hard-link") {
                linkSync(linkTarget, externalCheckpointFile);
              } else {
                mkdirSync(externalCheckpointFile, { mode: 0o700 });
              }
              return CHECKPOINT_AT;
            },
          }),
        "collision",
      );
      assert.deepEqual(checkpointTransactionEntries(caseParent), []);
      if (claimant === "different") {
        assert.ok(differentReference);
        assert.deepEqual(
          readFileSync(externalCheckpointFile),
          readFileSync(differentReference),
        );
      } else if (claimant === "symbolic-link") {
        assert.equal(lstatSync(externalCheckpointFile).isSymbolicLink(), true);
      } else if (claimant === "hard-link") {
        assert.equal(lstatSync(externalCheckpointFile).nlink, 2);
      } else {
        assert.equal(lstatSync(externalCheckpointFile).isDirectory(), true);
      }
      expectStandaloneCheckpointFailure(
        checkpointDirectory,
        externalCheckpointFile,
        claimant === "different" ? "checkpoint-mismatch" : "corruption",
      );
    }
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("treats an existing publication transaction as busy without adopting its stage", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpointDirectory = join(parent, "owner-checkpoint");
    const externalCheckpointFile = join(parent, "shared.external.json");
    let competingAttempted = false;
    const ownerOptions = withEvidenceCheckpointPublicationHookForTest(
      {
        ledgerRootDirectory: pair.ledgerRoot,
        reconciliationIndexRootDirectory: pair.indexRoot,
        checkpointDirectory,
        externalCheckpointFile,
        stoppedSingleWriter: true as const,
        now: () => CHECKPOINT_AT,
      },
      ({ phase, stagePath }) => {
        if (phase !== "after-stage-parent-sync" || competingAttempted) return;
        competingAttempted = true;
        const before = lstatSync(stagePath);
        const beforeBytes = readFileSync(stagePath);
        expectCheckpointError(
          () =>
            createEvidenceCheckpoint({
              ledgerRootDirectory: pair.ledgerRoot,
              reconciliationIndexRootDirectory: pair.indexRoot,
              checkpointDirectory: join(parent, "competing-checkpoint"),
              externalCheckpointFile,
              stoppedSingleWriter: true,
              now: () => CHECKPOINT_AT,
            }),
          "publication-indeterminate",
        );
        const after = lstatSync(stagePath);
        assert.equal(after.dev, before.dev);
        assert.equal(after.ino, before.ino);
        assert.equal(after.nlink, 1);
        assert.deepEqual(readFileSync(stagePath), beforeBytes);
        assert.equal(existsSync(externalCheckpointFile), false);
      },
    );

    assert.equal(createEvidenceCheckpoint(ownerOptions).status, "verified");
    assert.equal(competingAttempted, true);
    assert.deepEqual(checkpointTransactionEntries(parent), []);
    assert.equal(
      verifyEvidenceCheckpoint({ checkpointDirectory, externalCheckpointFile }).status,
      "verified",
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("reconciles each bounded transaction residue under exclusive authority", () => {
  const parent = temporaryParent();
  try {
    for (const state of ["empty", "stage-only", "linked", "target-only"] as const) {
      const caseParent = join(parent, state);
      mkdirSync(caseParent, { mode: 0o700 });
      const pair = openPair(caseParent);
      populateLinkedPair(pair);
      const checkpoint = checkpointPair(caseParent, pair);
      const expectedBytes = readFileSync(checkpoint.externalCheckpointFile);
      rmSync(checkpoint.externalCheckpointFile);
      const transactionDirectory = checkpointTransactionDirectory(
        checkpoint.externalCheckpointFile,
      );
      const stagePath = join(transactionDirectory, "stage");

      if (state !== "target-only") {
        mkdirSync(transactionDirectory, { mode: 0o700 });
      }
      if (state === "stage-only" || state === "linked") {
        writeFileSync(stagePath, expectedBytes, { mode: 0o600 });
      }
      if (state === "linked") {
        linkSync(stagePath, checkpoint.externalCheckpointFile);
        assert.equal(lstatSync(stagePath).nlink, 2);
      }
      if (state === "target-only") {
        writeFileSync(checkpoint.externalCheckpointFile, expectedBytes, { mode: 0o600 });
      }

      const reconciled = reconcileEvidenceCheckpointPublication({
        checkpointDirectory: checkpoint.checkpointDirectory,
        exclusivePublicationOwner: true,
        externalCheckpointFile: checkpoint.externalCheckpointFile,
        stoppedSingleWriter: true,
      });
      assert.equal(reconciled.status, "verified");
      assert.equal(lstatSync(checkpoint.externalCheckpointFile).nlink, 1);
      assert.deepEqual(readFileSync(checkpoint.externalCheckpointFile), expectedBytes);
      assert.equal(existsSync(transactionDirectory), false);
      assert.equal(
        verifyEvidenceCheckpoint({
          checkpointDirectory: checkpoint.checkpointDirectory,
          externalCheckpointFile: checkpoint.externalCheckpointFile,
        }).status,
        "verified",
      );
    }
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("requires explicit stopped-writer and exclusive-owner reconciliation assertions", () => {
  const parent = temporaryParent();
  try {
    const pair = openPair(parent);
    populateLinkedPair(pair);
    const checkpoint = checkpointPair(parent, pair);
    for (const invalid of [
      { stoppedSingleWriter: false, exclusivePublicationOwner: true },
      { stoppedSingleWriter: true, exclusivePublicationOwner: false },
    ]) {
      expectCheckpointError(
        () =>
          reconcileEvidenceCheckpointPublication({
            checkpointDirectory: checkpoint.checkpointDirectory,
            externalCheckpointFile: checkpoint.externalCheckpointFile,
            ...invalid,
          } as unknown as ReconcileEvidenceCheckpointPublicationOptions),
        "quiescence-required",
      );
    }
    const missingCliAssertions = spawnSync(
      process.execPath,
      [
        checkpointPublicationReconciler(),
        "--checkpoint-directory",
        checkpoint.checkpointDirectory,
        "--external-checkpoint-file",
        checkpoint.externalCheckpointFile,
      ],
      { encoding: "utf8" },
    );
    assert.equal(missingCliAssertions.status, 2);
    assert.match(missingCliAssertions.stderr, /exclusive-publication-owner-confirmed/u);
    assert.deepEqual(checkpointTransactionEntries(parent), []);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("preserves mismatched and unexpected transaction-directory residue", () => {
  const parent = temporaryParent();
  try {
    for (const residue of ["different-stage", "symbolic-stage", "unexpected-entry"] as const) {
      const caseParent = join(parent, residue);
      mkdirSync(caseParent, { mode: 0o700 });
      const pair = openPair(caseParent);
      populateLinkedPair(pair);
      const checkpoint = checkpointPair(caseParent, pair);
      rmSync(checkpoint.externalCheckpointFile);
      const transactionDirectory = checkpointTransactionDirectory(
        checkpoint.externalCheckpointFile,
      );
      const stagePath = join(transactionDirectory, "stage");
      const linkTarget = join(caseParent, "foreign-stage-target.json");
      mkdirSync(transactionDirectory, { mode: 0o700 });
      if (residue === "different-stage") {
        writeFileSync(stagePath, "foreign-stage\n", { mode: 0o600 });
      } else if (residue === "symbolic-stage") {
        writeFileSync(linkTarget, "foreign-stage\n", { mode: 0o600 });
        symlinkSync(linkTarget, stagePath);
      } else {
        writeFileSync(join(transactionDirectory, "unexpected"), "foreign\n", {
          mode: 0o600,
        });
      }

      expectCheckpointError(
        () =>
          reconcileEvidenceCheckpointPublication({
            checkpointDirectory: checkpoint.checkpointDirectory,
            exclusivePublicationOwner: true,
            externalCheckpointFile: checkpoint.externalCheckpointFile,
            stoppedSingleWriter: true,
          }),
        "collision",
      );
      assert.equal(existsSync(checkpoint.externalCheckpointFile), false);
      assert.equal(existsSync(transactionDirectory), true);
      if (residue === "different-stage") {
        assert.equal(readFileSync(stagePath, "utf8"), "foreign-stage\n");
      } else if (residue === "symbolic-stage") {
        assert.equal(lstatSync(stagePath).isSymbolicLink(), true);
      } else {
        assert.equal(
          readFileSync(join(transactionDirectory, "unexpected"), "utf8"),
          "foreign\n",
        );
      }
    }
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
