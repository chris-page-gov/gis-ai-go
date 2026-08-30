import process from "node:process";

import {
  EvidenceCheckpointError,
  canonicalJson,
  createEvidenceCheckpoint,
  restoreEvidenceCheckpoint,
} from "../packages/evidence/dist/src/index.js";

export const CREATE_RESULT_SCHEMA =
  "gis-ai-go.evidence-checkpoint-create-result.v1";
export const RESTORE_RESULT_SCHEMA =
  "gis-ai-go.evidence-checkpoint-restore-result.v1";

export function parseClosedArguments(arguments_, valueFlags, assertionFlags) {
  const acceptedValues = new Set(valueFlags);
  const acceptedAssertions = new Set(assertionFlags);
  const values = new Map();
  const assertions = new Set();
  for (let index = 0; index < arguments_.length; index += 1) {
    const key = arguments_[index];
    if (typeof key !== "string") return null;
    if (acceptedAssertions.has(key)) {
      if (assertions.has(key)) return null;
      assertions.add(key);
      continue;
    }
    if (!acceptedValues.has(key) || values.has(key)) return null;
    const value = arguments_[index + 1];
    if (typeof value !== "string" || value.length === 0) return null;
    values.set(key, value);
    index += 1;
  }
  if (values.size !== acceptedValues.size || assertions.size !== acceptedAssertions.size) {
    return null;
  }
  return { assertions, values };
}

export function verificationSummary(result) {
  return {
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
  };
}

export function createCheckpointOperatorResult(configuration, now) {
  const result = createEvidenceCheckpoint({
    ...configuration,
    stoppedSingleWriter: true,
    ...(now === undefined ? {} : { now }),
  });
  return {
    schema: CREATE_RESULT_SCHEMA,
    status: "passed",
    operation: "create",
    operator_assertions: {
      stopped_single_writer: "operator-confirmed",
      exclusive_operation_owner: "operator-confirmed",
    },
    publication_durability: "file-and-parent-directory-synchronised",
    ...verificationSummary(result),
  };
}

export function restoreCheckpointOperatorResult(configuration, now) {
  const result = restoreEvidenceCheckpoint({
    ...configuration,
    ...(now === undefined ? {} : { now }),
  });
  return {
    schema: RESTORE_RESULT_SCHEMA,
    status: "passed",
    operation: "restore",
    operator_assertions: {
      stopped_single_writer: "operator-confirmed",
      exclusive_operation_owner: "operator-confirmed",
    },
    source_checkpoint: "verified",
    restored_pair: "verified",
    deployment_readiness: "not-evaluated",
    ...verificationSummary(result),
  };
}

export function operationErrorCode(error, unexpectedCode) {
  return error instanceof EvidenceCheckpointError ? error.code : unexpectedCode;
}

export function writeCanonicalResult(stream, result) {
  stream.write(`${canonicalJson(result)}\n`);
}

export function finishOperatorCommand({ options, run, schema, unexpectedCode }) {
  if (options === null) {
    writeCanonicalResult(process.stderr, {
      schema,
      status: "failed",
      code: "invalid-arguments",
    });
    process.exitCode = 2;
    return;
  }
  try {
    writeCanonicalResult(process.stdout, run(options));
  } catch (error) {
    writeCanonicalResult(process.stderr, {
      schema,
      status: "failed",
      code: operationErrorCode(error, unexpectedCode),
    });
    process.exitCode = 1;
  }
}
