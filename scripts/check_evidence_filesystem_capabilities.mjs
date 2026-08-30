#!/usr/bin/env node

import process from "node:process";
import { createHash } from "node:crypto";
import {
  chmodSync,
  closeSync,
  constants,
  fsyncSync,
  linkSync,
  lstatSync,
  mkdtempSync,
  openSync,
  readFileSync,
  realpathSync,
  rmdirSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { canonicalJson } from "../packages/evidence/dist/src/index.js";
import { parseClosedArguments } from "./evidence_checkpoint_operator_common.mjs";

const SCHEMA = "gis-ai-go.evidence-filesystem-capability-check.v1";
const SCHEMA_CONTRACT_PATH =
  "schemas/evidence-filesystem-capability-check.schema.json";
const SCRIPT_DIRECTORY = dirname(fileURLToPath(import.meta.url));
const SCHEMA_CONTRACT = Object.freeze({
  path: SCHEMA_CONTRACT_PATH,
  sha256: createHash("sha256")
    .update(readFileSync(join(SCRIPT_DIRECTORY, "..", SCHEMA_CONTRACT_PATH)))
    .digest("hex"),
});
const CLASSIFICATIONS = new Set([
  "synthetic-test-fixture",
  "direct-filesystem-observation",
]);
const CANONICAL_UTC_MILLISECONDS =
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/u;
const SHA256 = /^[0-9a-f]{64}$/u;
const PROBE_BYTES = Buffer.from("gis-ai-go-evidence-filesystem-probe-v1\n", "utf8");
const COLLISION_BYTES = Buffer.from("existing-content-must-survive\n", "utf8");

class FilesystemCapabilityError extends Error {
  constructor(code) {
    super(code);
    this.name = "FilesystemCapabilityError";
    this.code = code;
  }
}

function fail(code) {
  throw new FilesystemCapabilityError(code);
}

function expectExistsCollision(run) {
  try {
    run();
  } catch (error) {
    if (error !== null && typeof error === "object" && error.code === "EEXIST") return;
    fail("no-replace-unsupported");
  }
  fail("no-replace-unsupported");
}

function syncRegularFile(path) {
  let descriptor;
  try {
    descriptor = openSync(path, constants.O_RDONLY | constants.O_NOFOLLOW);
    fsyncSync(descriptor);
  } catch {
    fail("file-fsync-unsupported");
  } finally {
    if (descriptor !== undefined) closeSync(descriptor);
  }
}

function syncDirectory(path) {
  let descriptor;
  try {
    descriptor = openSync(path, constants.O_RDONLY | constants.O_DIRECTORY);
    fsyncSync(descriptor);
  } catch {
    fail("directory-fsync-unsupported");
  } finally {
    if (descriptor !== undefined) closeSync(descriptor);
  }
}

function assertPrivateModes(probeDirectory, ...files) {
  if ((lstatSync(probeDirectory).mode & 0o777) !== 0o700) {
    fail("private-modes-unsupported");
  }
  for (const file of files) {
    const stat = lstatSync(file);
    if (!stat.isFile() || stat.isSymbolicLink() || (stat.mode & 0o777) !== 0o600) {
      fail("private-modes-unsupported");
    }
  }
}

function removeKnownProbeEntry(path) {
  try {
    const stat = lstatSync(path);
    if (stat.isDirectory()) fail("cleanup-failed");
    unlinkSync(path);
  } catch (error) {
    if (error instanceof FilesystemCapabilityError) throw error;
    if (error !== null && typeof error === "object" && error.code === "ENOENT") return;
    fail("cleanup-failed");
  }
}

function assertObservationMetadata({ classification, observedAt, mountIdentitySha256 }) {
  let parsedObservation;
  try {
    parsedObservation = new Date(observedAt);
  } catch {
    fail("invalid-observation-metadata");
  }
  if (
    !CLASSIFICATIONS.has(classification) ||
    !CANONICAL_UTC_MILLISECONDS.test(observedAt) ||
    Number.isNaN(parsedObservation.getTime()) ||
    parsedObservation.toISOString() !== observedAt ||
    !SHA256.test(mountIdentitySha256)
  ) {
    fail("invalid-observation-metadata");
  }
}

function probeFilesystem(
  rootDirectory,
  { classification, observedAt, mountIdentitySha256 },
) {
  assertObservationMetadata({ classification, observedAt, mountIdentitySha256 });
  if (process.platform === "win32") fail("posix-semantics-unavailable");
  const requestedRoot = resolve(rootDirectory);
  let rootStat;
  try {
    rootStat = lstatSync(requestedRoot);
  } catch {
    fail("unsafe-probe-root");
  }
  if (!rootStat.isDirectory() || rootStat.isSymbolicLink()) fail("unsafe-probe-root");

  const canonicalRoot = realpathSync(requestedRoot);
  let probeDirectory;
  let stage;
  let target;
  let collision;
  let completed = false;
  try {
    probeDirectory = mkdtempSync(join(canonicalRoot, ".gis-ai-go-evidence-filesystem-probe-"));
    chmodSync(probeDirectory, 0o700);
    syncDirectory(canonicalRoot);

    stage = join(probeDirectory, "stage");
    target = join(probeDirectory, "target");
    collision = join(probeDirectory, "collision");
    writeFileSync(stage, PROBE_BYTES, { flag: "wx", mode: 0o600 });
    syncRegularFile(stage);
    syncDirectory(probeDirectory);
    assertPrivateModes(probeDirectory, stage);

    try {
      linkSync(stage, target);
    } catch {
      fail("hard-links-unsupported");
    }
    const stageStat = lstatSync(stage);
    const targetStat = lstatSync(target);
    if (
      !targetStat.isFile() ||
      targetStat.isSymbolicLink() ||
      stageStat.dev !== targetStat.dev ||
      stageStat.ino !== targetStat.ino ||
      stageStat.nlink !== 2 ||
      targetStat.nlink !== 2
    ) {
      fail("hard-links-unsupported");
    }
    syncDirectory(probeDirectory);

    expectExistsCollision(() => linkSync(stage, target));
    writeFileSync(collision, COLLISION_BYTES, { flag: "wx", mode: 0o600 });
    syncRegularFile(collision);
    expectExistsCollision(() => linkSync(stage, collision));
    expectExistsCollision(() =>
      writeFileSync(collision, PROBE_BYTES, { flag: "wx", mode: 0o600 }),
    );
    if (!readFileSync(collision).equals(COLLISION_BYTES)) fail("no-replace-unsupported");
    assertPrivateModes(probeDirectory, stage, target, collision);
    syncDirectory(probeDirectory);

    unlinkSync(target);
    unlinkSync(stage);
    unlinkSync(collision);
    syncDirectory(probeDirectory);
    rmdirSync(probeDirectory);
    probeDirectory = undefined;
    syncDirectory(canonicalRoot);
    completed = true;
  } finally {
    if (!completed && probeDirectory !== undefined) {
      try {
        for (const path of [target, stage, collision]) {
          if (path !== undefined) removeKnownProbeEntry(path);
        }
        rmdirSync(probeDirectory);
        syncDirectory(canonicalRoot);
      } catch {
        fail("cleanup-failed");
      }
    }
  }

  return {
    schema: SCHEMA,
    status: "passed",
    classification,
    scope: "one-caller-identified-filesystem",
    observed_at: observedAt,
    mount_identity_sha256: mountIdentitySha256,
    schema_contract: SCHEMA_CONTRACT,
    checks: [
      "private-directory-mode-0700",
      "private-file-mode-0600",
      "exclusive-file-create",
      "sibling-hard-link",
      "atomic-no-replace-hard-link",
      "regular-file-fsync",
      "directory-fsync",
      "synchronised-clean-up",
    ],
    limitations: {
      same_filesystem_only: true,
      full_hardware_flush: "not-established",
      mount_identity_provenance: "caller-supplied-not-attested",
    },
  };
}

const parsed = parseClosedArguments(
  process.argv.slice(2),
  [
    "--classification",
    "--observed-at",
    "--mount-identity-sha256",
    "--probe-directory",
  ],
  [],
);
if (parsed === null) {
  process.stderr.write(
    `${canonicalJson({
      schema: SCHEMA,
      status: "failed",
      code: "invalid-arguments",
      schema_contract: SCHEMA_CONTRACT,
    })}\n`,
  );
  process.exitCode = 2;
} else {
  try {
    const result = probeFilesystem(parsed.values.get("--probe-directory"), {
      classification: parsed.values.get("--classification"),
      observedAt: parsed.values.get("--observed-at"),
      mountIdentitySha256: parsed.values.get("--mount-identity-sha256"),
    });
    process.stdout.write(`${canonicalJson(result)}\n`);
  } catch (error) {
    const code =
      error instanceof FilesystemCapabilityError
        ? error.code
        : "unexpected-probe-failure";
    process.stderr.write(
      `${canonicalJson({
        schema: SCHEMA,
        status: "failed",
        code,
        schema_contract: SCHEMA_CONTRACT,
      })}\n`,
    );
    process.exitCode = 1;
  }
}
