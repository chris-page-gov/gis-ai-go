#!/usr/bin/env node

import process from "node:process";

import {
  RESTORE_RESULT_SCHEMA,
  finishOperatorCommand,
  parseClosedArguments,
  restoreCheckpointOperatorResult,
} from "./evidence_checkpoint_operator_common.mjs";

const parsed = parseClosedArguments(
  process.argv.slice(2),
  [
    "--checkpoint-directory",
    "--external-checkpoint-file",
    "--ledger-destination-root",
    "--reconciliation-index-destination-root",
  ],
  ["--stopped-single-writer-confirmed", "--exclusive-restore-owner-confirmed"],
);

const options =
  parsed === null
    ? null
    : {
        checkpointDirectory: parsed.values.get("--checkpoint-directory"),
        externalCheckpointFile: parsed.values.get("--external-checkpoint-file"),
        ledgerDestinationRoot: parsed.values.get("--ledger-destination-root"),
        reconciliationIndexDestinationRoot: parsed.values.get(
          "--reconciliation-index-destination-root",
        ),
      };

finishOperatorCommand({
  options,
  schema: RESTORE_RESULT_SCHEMA,
  unexpectedCode: "unexpected-restore-failure",
  run: (configuration) => restoreCheckpointOperatorResult(configuration),
});
