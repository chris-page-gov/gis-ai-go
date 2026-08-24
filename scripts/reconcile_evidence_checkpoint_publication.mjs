#!/usr/bin/env node

import process from "node:process";

import {
  EvidenceCheckpointError,
  canonicalJson,
  reconcileEvidenceCheckpointPublication,
} from "../packages/evidence/dist/src/index.js";

function usage() {
  process.stderr.write(
    "Usage: node scripts/reconcile_evidence_checkpoint_publication.mjs " +
      "--checkpoint-directory <directory> --external-checkpoint-file <file> " +
      "--stopped-single-writer-confirmed --exclusive-publication-owner-confirmed\n",
  );
}

function parseArguments(arguments_) {
  const acceptedValues = new Set(["--checkpoint-directory", "--external-checkpoint-file"]);
  const acceptedAssertions = new Set([
    "--stopped-single-writer-confirmed",
    "--exclusive-publication-owner-confirmed",
  ]);
  const options = new Map();
  const assertions = new Set();
  for (let index = 0; index < arguments_.length; index += 1) {
    const key = arguments_[index];
    if (typeof key !== "string") return null;
    if (acceptedAssertions.has(key)) {
      if (assertions.has(key)) return null;
      assertions.add(key);
      continue;
    }
    if (!acceptedValues.has(key) || options.has(key)) return null;
    const value = arguments_[index + 1];
    if (typeof value !== "string" || value.length === 0) return null;
    options.set(key, value);
    index += 1;
  }
  if (options.size !== acceptedValues.size || assertions.size !== acceptedAssertions.size) {
    return null;
  }
  return {
    checkpointDirectory: options.get("--checkpoint-directory"),
    exclusivePublicationOwner: true,
    externalCheckpointFile: options.get("--external-checkpoint-file"),
    stoppedSingleWriter: true,
  };
}

const options = parseArguments(process.argv.slice(2));
if (options === null) {
  usage();
  process.exitCode = 2;
} else {
  try {
    const result = reconcileEvidenceCheckpointPublication(options);
    process.stdout.write(
      `${canonicalJson({
        schema: "gis-ai-go.evidence-checkpoint-publication-reconciliation.v1",
        status: "passed",
        publication_durability: "file-and-parent-directory-synchronised",
        checkpoint_id: result.checkpoint_id,
        ledger_id: result.ledger.ledger_id,
        reconciliation_index_id: result.reconciliation_index.index_id,
      })}\n`,
    );
  } catch (error) {
    const code =
      error instanceof EvidenceCheckpointError ? error.code : "unexpected-reconciliation-failure";
    process.stderr.write(
      `${canonicalJson({
        schema: "gis-ai-go.evidence-checkpoint-publication-reconciliation.v1",
        status: "failed",
        code,
      })}\n`,
    );
    process.exitCode = 1;
  }
}
