import { getPublicReadAuthorityContext } from "@gis-ai-go/authority-context";
import {
  CANONICALISATION,
  DATA_QUERY_OBLIGATIONS,
  GOVERNED_OPERATIONS,
  PUBLIC_READ_ONS_RESOURCE,
  SELECTION_RESOLVE_OBLIGATIONS,
  buildPublicReadPolicy,
  buildPublicReadPolicyDecision,
  canonicalJson,
  canonicalJsonClone,
  verifyPublicReadAuthorityContext,
  verifyPublicReadPolicy,
  verifyPublicReadResource,
  type GovernedOperation,
  type PublicReadAuthorityContext,
  type PublicReadOperation,
  type PublicReadPolicy,
  type PublicReadPolicyCore,
  type PublicReadPolicyDecision,
  type PublicReadPolicyReasonCode,
  type PublicReadResource,
} from "@gis-ai-go/evidence";

import checkedInPolicy from "./public-read-v2.json" with { type: "json" };

const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]*$/u;
const TRACE_ID = /^[0-9a-f]{32}$/u;
const CONTROL = /[\u0000-\u001f\u007f]/u;

export const PUBLIC_READ_POLICY_CORE = {
  schema: "gis-ai-go.public-policy.v2",
  version: "2.0.0",
  canonicalisation: CANONICALISATION,
  compilation: {
    kind: "compiled-json",
    runtime: "gis-ai-go-gateway",
  },
  default_effect: "deny",
  applies_to: {
    authority_profile: "anonymous-open",
    access_tier: "open",
    publication_classification: "public",
    contains_personal_data: false,
    contains_protected_data: false,
    read_only: true,
  },
  resources: [PUBLIC_READ_ONS_RESOURCE],
  rules: [
    {
      rule_id: "public-data-query-ons-v121",
      operation: "data.query",
      resource_id: PUBLIC_READ_ONS_RESOURCE.resource_id,
      effect: "allow-with-obligations",
      obligations: DATA_QUERY_OBLIGATIONS,
    },
    {
      rule_id: "public-selection-resolve-ons-v121",
      operation: "selection.resolve",
      resource_id: PUBLIC_READ_ONS_RESOURCE.resource_id,
      effect: "allow-with-obligations",
      obligations: SELECTION_RESOLVE_OBLIGATIONS,
    },
  ],
} as const satisfies PublicReadPolicyCore;

const expectedPolicy = buildPublicReadPolicy(PUBLIC_READ_POLICY_CORE);
if (
  !verifyPublicReadPolicy(checkedInPolicy) ||
  canonicalJson(checkedInPolicy) !== canonicalJson(expectedPolicy)
) {
  throw new Error("The checked-in public-read v2 policy failed its content identity check");
}

/** The exact checked-in policy for the inactive selection and fixed ONS query plane. */
export const PUBLIC_READ_POLICY: PublicReadPolicy = canonicalJsonClone(
  checkedInPolicy,
) as PublicReadPolicy;

export class PublicReadPolicyInputError extends TypeError {
  public constructor(message: string) {
    super(message);
    this.name = "PublicReadPolicyInputError";
  }
}

export interface PublicReadPolicyEvaluationInput {
  readonly requestId: string;
  readonly traceId: string;
  readonly operation: string;
  /** Server-selected policy resource; callers cannot define or extend it. */
  readonly resource: unknown;
}

interface PublicReadPolicyEvaluationBase {
  readonly allowed: boolean;
  readonly effect: "allow-with-obligations" | "deny";
  readonly reasonCode: PublicReadPolicyReasonCode;
  readonly authorityContext: PublicReadAuthorityContext;
  readonly policy: PublicReadPolicy;
}

export interface PublicReadPolicyDecisionEvaluation extends PublicReadPolicyEvaluationBase {
  readonly decision: PublicReadPolicyDecision;
}

export interface UnknownPublicReadOperationDenial extends PublicReadPolicyEvaluationBase {
  readonly allowed: false;
  readonly effect: "deny";
  readonly reasonCode: "operation-not-allowed";
  readonly decision: null;
}

export type PublicReadPolicyEvaluation =
  | PublicReadPolicyDecisionEvaluation
  | UnknownPublicReadOperationDenial;

function assertIdentifiers(requestId: string, traceId: string): void {
  if (requestId.length > 128 || !REQUEST_ID.test(requestId)) {
    throw new PublicReadPolicyInputError(
      "requestId must be a valid bounded request identifier",
    );
  }
  if (!TRACE_ID.test(traceId)) {
    throw new PublicReadPolicyInputError(
      "traceId must be 32 lower-case hexadecimal characters",
    );
  }
}

function isGovernedOperation(operation: string): operation is GovernedOperation {
  return (GOVERNED_OPERATIONS as readonly string[]).includes(operation);
}

function isApprovedResource(value: unknown): value is PublicReadResource {
  return (
    verifyPublicReadResource(value) &&
    canonicalJson(value) === canonicalJson(PUBLIC_READ_ONS_RESOURCE)
  );
}

function snapshotEvaluationInput(value: unknown): PublicReadPolicyEvaluationInput {
  let snapshot: unknown;
  try {
    snapshot = canonicalJsonClone(value);
  } catch {
    throw new PublicReadPolicyInputError(
      "input must be detached canonical JSON without proxies or accessors",
    );
  }
  if (snapshot === null || typeof snapshot !== "object" || Array.isArray(snapshot)) {
    throw new PublicReadPolicyInputError("input must be a closed object");
  }
  const record = snapshot as Record<string, unknown>;
  const keys = Object.keys(record).sort();
  const expected = ["operation", "requestId", "resource", "traceId"];
  if (keys.length !== expected.length || keys.some((key, index) => key !== expected[index])) {
    throw new PublicReadPolicyInputError("input has an unexpected or missing property");
  }
  if (
    typeof record.requestId !== "string" ||
    typeof record.traceId !== "string" ||
    typeof record.operation !== "string" ||
    record.operation.length === 0 ||
    Array.from(record.operation).length > 128 ||
    CONTROL.test(record.operation)
  ) {
    throw new PublicReadPolicyInputError("operation must be a bounded control-free string");
  }
  return snapshot as PublicReadPolicyEvaluationInput;
}

function freezeEvaluation<T extends PublicReadPolicyEvaluation>(evaluation: T): T {
  return Object.freeze(evaluation);
}

/**
 * Evaluate the local default-deny v2 policy. This function neither calls a
 * provider nor accepts caller identity, purpose, entitlement or credentials.
 */
export function evaluatePublicReadPolicy(
  input: PublicReadPolicyEvaluationInput,
): PublicReadPolicyEvaluation {
  const snapshot = snapshotEvaluationInput(input);
  assertIdentifiers(snapshot.requestId, snapshot.traceId);
  const authorityContext = getPublicReadAuthorityContext();
  if (!verifyPublicReadAuthorityContext(authorityContext)) {
    throw new Error("The server-owned public-read authority context failed closed");
  }

  if (!isGovernedOperation(snapshot.operation)) {
    return freezeEvaluation({
      allowed: false,
      effect: "deny",
      reasonCode: "operation-not-allowed",
      authorityContext,
      policy: PUBLIC_READ_POLICY,
      decision: null,
    });
  }

  const rule = PUBLIC_READ_POLICY.rules.find(
    (candidate) => candidate.operation === snapshot.operation,
  );
  let effect: "allow-with-obligations" | "deny" = "deny";
  let reasonCode: PublicReadPolicyReasonCode = "operation-not-allowed";
  let resourceId: string | null = null;
  let obligations: readonly [] | typeof DATA_QUERY_OBLIGATIONS | typeof SELECTION_RESOLVE_OBLIGATIONS = [];

  if (rule !== undefined) {
    if (
      isApprovedResource(snapshot.resource) &&
      rule.resource_id === snapshot.resource.resource_id
    ) {
      effect = "allow-with-obligations";
      reasonCode = "public-read-operation-allowed";
      resourceId = snapshot.resource.resource_id;
      obligations = snapshot.operation === "data.query"
        ? DATA_QUERY_OBLIGATIONS
        : SELECTION_RESOLVE_OBLIGATIONS;
    } else {
      reasonCode = "resource-not-approved";
    }
  }

  const decision = buildPublicReadPolicyDecision({
    schema: "gis-ai-go.public-policy-decision.v2",
    canonicalisation: CANONICALISATION,
    request_id: snapshot.requestId,
    trace_id: snapshot.traceId,
    authority_context_id: authorityContext.context_id,
    policy_id: PUBLIC_READ_POLICY.policy_id,
    policy_version: "2.0.0",
    policy_default_effect: "deny",
    operation: snapshot.operation,
    resource_id: resourceId,
    effect,
    reason_code: reasonCode,
    obligations,
  });

  return freezeEvaluation({
    allowed: effect === "allow-with-obligations",
    effect,
    reasonCode,
    authorityContext,
    policy: PUBLIC_READ_POLICY,
    decision,
  });
}

/** Narrow an allowed evaluation without giving a caller control of the operation. */
export function isAllowedPublicReadOperation(
  evaluation: PublicReadPolicyEvaluation,
  operation: PublicReadOperation,
): evaluation is PublicReadPolicyDecisionEvaluation {
  return (
    evaluation.allowed &&
    evaluation.decision !== null &&
    evaluation.decision.operation === operation
  );
}
