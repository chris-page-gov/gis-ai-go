import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  existsSync,
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
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  createEvidenceCheckpoint,
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
} from "../src/index.js";
import {
  PUBLIC_READ_REQUEST_ID,
  PUBLIC_READ_TRACE_ID,
  makePublicReadReceiptFixture,
} from "./public-read-fixtures.js";

const KEY = `gis-ai-go:ik:v1:${"1".repeat(64)}`;
const REPOSITORY_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../../..");
const FILESYSTEM_OBSERVED_AT = "2026-08-30T08:30:00.000Z";
const MOUNT_IDENTITY_SHA256 = "a".repeat(64);
const FILESYSTEM_SCHEMA_PATH =
  "schemas/evidence-filesystem-capability-check.schema.json";

function temporaryParent(): string {
  return mkdtempSync(join(tmpdir(), "gis-ai-go-evidence-operator-"));
}

function repositoryScript(name: string): string {
  return resolve(REPOSITORY_ROOT, "scripts", name);
}

function filesystemSchemaContract() {
  return {
    path: FILESYSTEM_SCHEMA_PATH,
    sha256: createHash("sha256")
      .update(readFileSync(resolve(REPOSITORY_ROOT, FILESYSTEM_SCHEMA_PATH)))
      .digest("hex"),
  };
}

function filesystemProbeArguments(
  probeDirectory: string,
  overrides: {
    classification?: string;
    observedAt?: string;
    mountIdentitySha256?: string;
  } = {},
): string[] {
  return [
    "--classification",
    overrides.classification ?? "direct-filesystem-observation",
    "--observed-at",
    overrides.observedAt ?? FILESYSTEM_OBSERVED_AT,
    "--mount-identity-sha256",
    overrides.mountIdentitySha256 ?? MOUNT_IDENTITY_SHA256,
    "--probe-directory",
    probeDirectory,
  ];
}

function runScript(name: string, arguments_: readonly string[]) {
  return spawnSync(process.execPath, [repositoryScript(name), ...arguments_], {
    encoding: "utf8",
  });
}

function parseResult(text: string): Record<string, unknown> {
  const value: unknown = JSON.parse(text);
  assert.ok(value !== null && typeof value === "object" && !Array.isArray(value));
  return value as Record<string, unknown>;
}

function openPopulatedPair(parent: string) {
  const ledgerRoot = join(parent, "ledger");
  const indexRoot = join(parent, "reconciliation-index");
  const ledger = openPublicEvidenceLedger({
    rootDirectory: ledgerRoot,
    retentionDays: 30,
    now: () => new Date("2026-08-30T08:00:00.000Z"),
  });
  const index = openEvidenceReconciliationIndex({
    rootDirectory: indexRoot,
    ledger,
    now: () => new Date("2026-08-30T08:00:00.000Z"),
  });
  const fixture = makePublicReadReceiptFixture();
  const claim = index.claim({
    idempotencyKey: KEY,
    operation: "data.query",
    requestId: PUBLIC_READ_REQUEST_ID,
    traceId: PUBLIC_READ_TRACE_ID,
    resourceId: fixture.receipt.resource.resource_id,
    normalisedParametersSha256: fixture.receipt.operation.normalised_parameters.sha256,
  });
  assert.equal(claim.status, "claimed");
  if (claim.status !== "claimed") assert.fail("operator fixture did not acquire its claim");
  index.resolve(claim.claim, fixture.receipt);
  ledger.persistReceipt(fixture.receipt, fixture.material);
  return { ledgerRoot, indexRoot };
}

function createArguments(
  pair: ReturnType<typeof openPopulatedPair>,
  checkpointDirectory: string,
  externalCheckpointFile: string,
): string[] {
  return [
    "--ledger-root-directory",
    pair.ledgerRoot,
    "--reconciliation-index-root-directory",
    pair.indexRoot,
    "--checkpoint-directory",
    checkpointDirectory,
    "--external-checkpoint-file",
    externalCheckpointFile,
  ];
}

test("requires both create assertions and refuses every existing output without path disclosure", () => {
  const parent = temporaryParent();
  try {
    const pair = openPopulatedPair(parent);
    const checkpointDirectory = join(parent, "checkpoint");
    const externalCheckpointFile = join(parent, "checkpoint.external.json");
    const baseArguments = createArguments(pair, checkpointDirectory, externalCheckpointFile);

    const missingAssertions = runScript("create_evidence_checkpoint.mjs", baseArguments);
    assert.equal(missingAssertions.status, 2);
    assert.equal(missingAssertions.stdout, "");
    assert.deepEqual(parseResult(missingAssertions.stderr), {
      schema: "gis-ai-go.evidence-checkpoint-create-result.v1",
      status: "failed",
      code: "invalid-arguments",
    });
    assert.equal(missingAssertions.stderr.includes(parent), false);
    assert.equal(existsSync(checkpointDirectory), false);

    const created = runScript("create_evidence_checkpoint.mjs", [
      ...baseArguments,
      "--stopped-single-writer-confirmed",
      "--exclusive-checkpoint-owner-confirmed",
    ]);
    assert.equal(created.status, 0, created.stderr);
    assert.equal(created.stderr, "");
    const createdResult = parseResult(created.stdout);
    assert.equal(createdResult.status, "passed");
    assert.equal(createdResult.operation, "create");
    assert.equal(created.stdout.includes(parent), false);
    const manifestBefore = readFileSync(join(checkpointDirectory, "manifest.json"));
    const externalBefore = readFileSync(externalCheckpointFile);

    const collision = runScript("create_evidence_checkpoint.mjs", [
      ...baseArguments,
      "--stopped-single-writer-confirmed",
      "--exclusive-checkpoint-owner-confirmed",
    ]);
    assert.equal(collision.status, 1);
    assert.equal(collision.stdout, "");
    assert.deepEqual(parseResult(collision.stderr), {
      schema: "gis-ai-go.evidence-checkpoint-create-result.v1",
      status: "failed",
      code: "collision",
    });
    assert.equal(collision.stderr.includes(parent), false);
    assert.deepEqual(readFileSync(join(checkpointDirectory, "manifest.json")), manifestBefore);
    assert.deepEqual(readFileSync(externalCheckpointFile), externalBefore);

    const sentinel = join(parent, "sentinel");
    const linkedOutput = join(parent, "linked.external.json");
    writeFileSync(sentinel, "do-not-replace\n", { mode: 0o600 });
    symlinkSync(sentinel, linkedOutput);
    const linkedCollision = runScript("create_evidence_checkpoint.mjs", [
      ...createArguments(pair, join(parent, "linked-checkpoint"), linkedOutput),
      "--stopped-single-writer-confirmed",
      "--exclusive-checkpoint-owner-confirmed",
    ]);
    assert.equal(linkedCollision.status, 1);
    assert.equal((parseResult(linkedCollision.stderr).code), "collision");
    assert.equal(readFileSync(sentinel, "utf8"), "do-not-replace\n");
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("requires restore fencing, restores once and leaves non-empty destinations unchanged", () => {
  const parent = temporaryParent();
  try {
    const pair = openPopulatedPair(parent);
    const checkpointDirectory = join(parent, "checkpoint");
    const externalCheckpointFile = join(parent, "checkpoint.external.json");
    createEvidenceCheckpoint({
      ledgerRootDirectory: pair.ledgerRoot,
      reconciliationIndexRootDirectory: pair.indexRoot,
      checkpointDirectory,
      externalCheckpointFile,
      stoppedSingleWriter: true,
      now: () => new Date("2026-08-30T09:00:00.000Z"),
    });
    const ledgerDestination = join(parent, "restored-ledger");
    const indexDestination = join(parent, "restored-index");
    mkdirSync(ledgerDestination, { mode: 0o700 });
    mkdirSync(indexDestination, { mode: 0o700 });
    const baseArguments = [
      "--checkpoint-directory",
      checkpointDirectory,
      "--external-checkpoint-file",
      externalCheckpointFile,
      "--ledger-destination-root",
      ledgerDestination,
      "--reconciliation-index-destination-root",
      indexDestination,
    ];

    const missingAssertions = runScript("restore_evidence_checkpoint.mjs", baseArguments);
    assert.equal(missingAssertions.status, 2);
    assert.equal(parseResult(missingAssertions.stderr).code, "invalid-arguments");
    assert.deepEqual(readdirSync(ledgerDestination), []);
    assert.deepEqual(readdirSync(indexDestination), []);

    const restored = runScript("restore_evidence_checkpoint.mjs", [
      ...baseArguments,
      "--stopped-single-writer-confirmed",
      "--exclusive-restore-owner-confirmed",
    ]);
    assert.equal(restored.status, 0, restored.stderr);
    const result = parseResult(restored.stdout);
    assert.equal(result.status, "passed");
    assert.equal(result.restored_pair, "verified");
    assert.equal(result.deployment_readiness, "not-evaluated");
    assert.equal(restored.stdout.includes(parent), false);
    const ledgerDescriptorBefore = readFileSync(join(ledgerDestination, "ledger.json"));
    const indexDescriptorBefore = readFileSync(join(indexDestination, "index.json"));

    const repeated = runScript("restore_evidence_checkpoint.mjs", [
      ...baseArguments,
      "--stopped-single-writer-confirmed",
      "--exclusive-restore-owner-confirmed",
    ]);
    assert.equal(repeated.status, 1);
    assert.equal(parseResult(repeated.stderr).code, "destination-not-empty");
    assert.equal(repeated.stderr.includes(parent), false);
    assert.deepEqual(readFileSync(join(ledgerDestination, "ledger.json")), ledgerDescriptorBefore);
    assert.deepEqual(readFileSync(join(indexDestination, "index.json")), indexDescriptorBefore);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("probes the exact filesystem primitives, removes its residue and rejects a symlink root", () => {
  const parent = temporaryParent();
  try {
    const before = readdirSync(parent);
    const checked = runScript(
      "check_evidence_filesystem_capabilities.mjs",
      filesystemProbeArguments(parent),
    );
    assert.equal(checked.status, 0, checked.stderr);
    const result = parseResult(checked.stdout);
    assert.equal(result.status, "passed");
    assert.equal(result.classification, "direct-filesystem-observation");
    assert.equal(result.scope, "one-caller-identified-filesystem");
    assert.equal(result.observed_at, FILESYSTEM_OBSERVED_AT);
    assert.equal(result.mount_identity_sha256, MOUNT_IDENTITY_SHA256);
    assert.deepEqual(result.schema_contract, filesystemSchemaContract());
    assert.deepEqual(result.limitations, {
      same_filesystem_only: true,
      full_hardware_flush: "not-established",
      mount_identity_provenance: "caller-supplied-not-attested",
    });
    assert.equal(checked.stdout.includes(parent), false);
    assert.deepEqual(readdirSync(parent), before);

    const missingObservationMetadata = runScript(
      "check_evidence_filesystem_capabilities.mjs",
      ["--probe-directory", parent],
    );
    assert.equal(missingObservationMetadata.status, 2);
    assert.deepEqual(parseResult(missingObservationMetadata.stderr), {
      schema: "gis-ai-go.evidence-filesystem-capability-check.v1",
      status: "failed",
      code: "invalid-arguments",
      schema_contract: filesystemSchemaContract(),
    });
    assert.equal(missingObservationMetadata.stderr.includes(parent), false);
    assert.deepEqual(readdirSync(parent), before);

    for (const invalidMetadata of [
      { classification: "provider-attested" },
      { observedAt: "2026-08-30T08:30:00Z" },
      { mountIdentitySha256: "A".repeat(64) },
    ]) {
      const rejectedMetadata = runScript(
        "check_evidence_filesystem_capabilities.mjs",
        filesystemProbeArguments(parent, invalidMetadata),
      );
      assert.equal(rejectedMetadata.status, 1);
      assert.deepEqual(parseResult(rejectedMetadata.stderr), {
        schema: "gis-ai-go.evidence-filesystem-capability-check.v1",
        status: "failed",
        code: "invalid-observation-metadata",
        schema_contract: filesystemSchemaContract(),
      });
      assert.equal(rejectedMetadata.stderr.includes(parent), false);
      assert.deepEqual(readdirSync(parent), before);
    }

    const alias = join(dirname(parent), `${parent.split("/").at(-1)}-alias`);
    symlinkSync(parent, alias);
    try {
      const rejected = runScript(
        "check_evidence_filesystem_capabilities.mjs",
        filesystemProbeArguments(alias),
      );
      assert.equal(rejected.status, 1);
      assert.deepEqual(parseResult(rejected.stderr), {
        schema: "gis-ai-go.evidence-filesystem-capability-check.v1",
        status: "failed",
        code: "unsafe-probe-root",
        schema_contract: filesystemSchemaContract(),
      });
      assert.equal(rejected.stderr.includes(parent), false);
      assert.deepEqual(readdirSync(parent), before);
    } finally {
      rmSync(alias, { force: true });
    }
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});
