#!/usr/bin/env node

import process from "node:process";

import {
  CREATE_RESULT_SCHEMA,
  createCheckpointOperatorResult,
  finishOperatorCommand,
  parseClosedArguments,
} from "./evidence_checkpoint_operator_common.mjs";

const parsed = parseClosedArguments(
  process.argv.slice(2),
  [
    "--ledger-root-directory",
    "--reconciliation-index-root-directory",
    "--checkpoint-directory",
    "--external-checkpoint-file",
  ],
  ["--stopped-single-writer-confirmed", "--exclusive-checkpoint-owner-confirmed"],
);

const options =
  parsed === null
    ? null
    : {
        ledgerRootDirectory: parsed.values.get("--ledger-root-directory"),
        reconciliationIndexRootDirectory: parsed.values.get(
          "--reconciliation-index-root-directory",
        ),
        checkpointDirectory: parsed.values.get("--checkpoint-directory"),
        externalCheckpointFile: parsed.values.get("--external-checkpoint-file"),
      };

finishOperatorCommand({
  options,
  schema: CREATE_RESULT_SCHEMA,
  unexpectedCode: "unexpected-create-failure",
  run: (configuration) => createCheckpointOperatorResult(configuration),
});
