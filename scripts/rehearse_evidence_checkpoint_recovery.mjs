#!/usr/bin/env node

import process from "node:process";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  chmodSync,
  closeSync,
  constants,
  fsyncSync,
  mkdirSync,
  mkdtempSync,
  openSync,
  renameSync,
  rmSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import {
  canonicalJson,
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
} from "../packages/evidence/dist/src/index.js";
import {
  createEvidenceReadinessIntegrity,
  verifyEvidenceReadinessIntegrity,
} from "../apps/mcp-gateway/dist/src/readiness-integrity.js";
import {
  createCheckpointOperatorResult,
  restoreCheckpointOperatorResult,
} from "./evidence_checkpoint_operator_common.mjs";

const SCHEMA = "gis-ai-go.evidence-checkpoint-recovery-rehearsal.v1";
const KEY = `gis-ai-go:ik:v1:${"1".repeat(64)}`;
const SCRIPT_DIRECTORY = dirname(fileURLToPath(import.meta.url));
const FILESYSTEM_OBSERVED_AT = "2026-08-30T08:30:00.000Z";
const MOUNT_IDENTITY_SHA256 = createHash("sha256")
  .update("gis-ai-go.evidence-filesystem-rehearsal-mount.v1\0", "utf8")
  .digest("hex");

class RehearsalError extends Error {
  constructor(code) {
    super(code);
    this.name = "RehearsalError";
    this.code = code;
  }
}

function fail(code) {
  throw new RehearsalError(code);
}

function syncDirectory(path) {
  let descriptor;
  try {
    descriptor = openSync(path, constants.O_RDONLY | constants.O_DIRECTORY);
    fsyncSync(descriptor);
  } catch {
    fail("quarantine-sync-failed");
  } finally {
    if (descriptor !== undefined) closeSync(descriptor);
  }
}

function runPathFreeCommand(script, arguments_, failureCode) {
  const completed = spawnSync(process.execPath, [join(SCRIPT_DIRECTORY, script), ...arguments_], {
    encoding: "utf8",
  });
  if (completed.status !== 0 || completed.stderr !== "") fail(failureCode);
  try {
    const result = JSON.parse(completed.stdout);
    if (
      result === null ||
      typeof result !== "object" ||
      Array.isArray(result) ||
      result.status !== "passed"
    ) {
      fail(failureCode);
    }
    return result;
  } catch (error) {
    if (error instanceof RehearsalError) throw error;
    fail(failureCode);
  }
}

let rehearsalRoot;
let result;
let failure;
try {
  if (process.argv.length !== 2) fail("invalid-arguments");
  rehearsalRoot = mkdtempSync(join(tmpdir(), "gis-ai-go-evidence-recovery-rehearsal-"));
  chmodSync(rehearsalRoot, 0o700);

  const filesystemObservation = runPathFreeCommand(
    "check_evidence_filesystem_capabilities.mjs",
    [
      "--classification",
      "synthetic-test-fixture",
      "--observed-at",
      FILESYSTEM_OBSERVED_AT,
      "--mount-identity-sha256",
      MOUNT_IDENTITY_SHA256,
      "--probe-directory",
      rehearsalRoot,
    ],
    "filesystem-capability-check-failed",
  );

  const writer = spawnSync(
    process.execPath,
    [
      join(SCRIPT_DIRECTORY, "evidence_checkpoint_rehearsal_fixture_writer.mjs"),
      "--root-directory",
      rehearsalRoot,
    ],
    { encoding: "utf8" },
  );
  if (writer.status !== 0 || writer.stdout !== "" || writer.stderr !== "") {
    fail("fixture-writer-failed");
  }

  const ledgerRoot = join(rehearsalRoot, "ledger");
  const indexRoot = join(rehearsalRoot, "reconciliation-index");
  const checkpointDirectory = join(rehearsalRoot, "checkpoint");
  const externalCheckpointFile = join(rehearsalRoot, "checkpoint.external.json");
  let created;
  try {
    created = createCheckpointOperatorResult(
      {
        ledgerRootDirectory: ledgerRoot,
        reconciliationIndexRootDirectory: indexRoot,
        checkpointDirectory,
        externalCheckpointFile,
      },
      () => new Date("2026-08-30T09:00:00.000Z"),
    );
  } catch {
    fail("checkpoint-create-failed");
  }
  const checked = runPathFreeCommand(
    "check_evidence_checkpoint.mjs",
    [
      "--checkpoint-directory",
      checkpointDirectory,
      "--external-checkpoint-file",
      externalCheckpointFile,
    ],
    "checkpoint-verification-failed",
  );
  if (checked.checkpoint_id !== created.checkpoint_id) fail("checkpoint-identity-mismatch");

  const quarantine = join(rehearsalRoot, "quarantine");
  mkdirSync(quarantine, { mode: 0o700 });
  renameSync(ledgerRoot, join(quarantine, "ledger"));
  renameSync(indexRoot, join(quarantine, "reconciliation-index"));
  syncDirectory(quarantine);
  syncDirectory(rehearsalRoot);

  const restoredLedgerRoot = join(rehearsalRoot, "restored-ledger");
  const restoredIndexRoot = join(rehearsalRoot, "restored-reconciliation-index");
  mkdirSync(restoredLedgerRoot, { mode: 0o700 });
  mkdirSync(restoredIndexRoot, { mode: 0o700 });
  let restored;
  try {
    restored = restoreCheckpointOperatorResult(
      {
        checkpointDirectory,
        externalCheckpointFile,
        ledgerDestinationRoot: restoredLedgerRoot,
        reconciliationIndexDestinationRoot: restoredIndexRoot,
      },
      () => new Date("2026-08-30T10:00:00.000Z"),
    );
  } catch {
    fail("checkpoint-restore-failed");
  }
  if (restored.checkpoint_id !== created.checkpoint_id) fail("restore-identity-mismatch");

  const restoredLedger = openPublicEvidenceLedger({
    rootDirectory: restoredLedgerRoot,
    retentionDays: 30,
  });
  const restoredIndex = openEvidenceReconciliationIndex({
    rootDirectory: restoredIndexRoot,
    ledger: restoredLedger,
  });
  const readiness = createEvidenceReadinessIntegrity(restoredLedger, restoredIndex);
  verifyEvidenceReadinessIntegrity(readiness);
  if (restoredIndex.lookup(KEY).status !== "completed") fail("restored-lookup-failed");

  result = {
    schema: SCHEMA,
    status: "passed",
    mode: "deterministic-synthetic-non-live",
    writer_lifecycle: "fixture-process-exited-before-checkpoint",
    filesystem_observation: filesystemObservation,
    checkpoint_creation: "passed",
    checkpoint_verification: "passed",
    source_pair: "quarantined-without-deletion",
    restore: "passed",
    readiness: {
      evidence_storage: "verified",
      service: "not-started",
      deployment: "not-evaluated",
    },
    checkpoint_id: created.checkpoint_id,
    ledger_id: restored.ledger.ledger_id,
    reconciliation_index_id: restored.reconciliation_index.index_id,
    event_count: restored.ledger.event_count,
    completed_claim_count: restored.reconciliation_index.completed_count,
    provider_calls: 0,
  };
} catch (error) {
  failure = error instanceof RehearsalError ? error.code : "unexpected-rehearsal-failure";
}

if (rehearsalRoot !== undefined) {
  try {
    rmSync(rehearsalRoot, { recursive: true, force: true });
  } catch {
    failure = "cleanup-failed";
    result = undefined;
  }
}

if (failure !== undefined || result === undefined) {
  const failureCode = failure ?? "unexpected-rehearsal-failure";
  process.stderr.write(
    `${canonicalJson({ schema: SCHEMA, status: "failed", code: failureCode })}\n`,
  );
  process.exitCode = failureCode === "invalid-arguments" ? 2 : 1;
} else {
  process.stdout.write(`${canonicalJson(result)}\n`);
}
