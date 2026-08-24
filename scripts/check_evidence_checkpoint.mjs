#!/usr/bin/env node

import process from "node:process";

import {
  EvidenceCheckpointError,
  canonicalJson,
  verifyEvidenceCheckpoint,
} from "../packages/evidence/dist/src/index.js";

function usage() {
  process.stderr.write(
    "Usage: node scripts/check_evidence_checkpoint.mjs " +
      "--checkpoint-directory <directory> --external-checkpoint-file <file>\n",
  );
}

function parseArguments(arguments_) {
  const accepted = new Set(["--checkpoint-directory", "--external-checkpoint-file"]);
  const options = new Map();
  for (let index = 0; index < arguments_.length; index += 2) {
    const key = arguments_[index];
    const value = arguments_[index + 1];
    if (
      typeof key !== "string" ||
      typeof value !== "string" ||
      !accepted.has(key) ||
      options.has(key) ||
      value.length === 0
    ) {
      return null;
    }
    options.set(key, value);
  }
  if (options.size !== accepted.size) return null;
  return {
    checkpointDirectory: options.get("--checkpoint-directory"),
    externalCheckpointFile: options.get("--external-checkpoint-file"),
  };
}

const options = parseArguments(process.argv.slice(2));
if (options === null) {
  usage();
  process.exitCode = 2;
} else {
  try {
    const result = verifyEvidenceCheckpoint(options);
    process.stdout.write(
      `${canonicalJson({
        schema: "gis-ai-go.evidence-checkpoint-check.v1",
        status: "passed",
        publication_durability: "not-established-by-read-only-check",
        checkpoint_id: result.checkpoint_id,
        ledger: {
          ledger_id: result.ledger.ledger_id,
          event_count: result.ledger.event_count,
          record_count: result.ledger.record_count,
          last_event_id: result.ledger.last_event_id,
        },
        reconciliation_index: {
          index_id: result.reconciliation_index.index_id,
          ledger_id: result.reconciliation_index.ledger_id,
          claim_count: result.reconciliation_index.claim_count,
          completed_count: result.reconciliation_index.completed_count,
          pending_count: result.reconciliation_index.pending_count,
        },
      })}\n`,
    );
  } catch (error) {
    const code =
      error instanceof EvidenceCheckpointError ? error.code : "unexpected-verification-failure";
    process.stderr.write(
      `${canonicalJson({
        schema: "gis-ai-go.evidence-checkpoint-check.v1",
        status: "failed",
        code,
      })}\n`,
    );
    process.exitCode = 1;
  }
}
