import { getPublicAuthorityContext } from "@gis-ai-go/authority-context";
import type { CatalogueBundle } from "@gis-ai-go/contracts";
import {
  CANONICALISATION,
  GOVERNED_OPERATIONS,
  PUBLIC_POLICY_OBLIGATIONS,
  buildPublicPolicy,
  buildPublicPolicyDecision,
  canonicalJson,
  canonicalJsonClone,
  verifyPublicAuthorityContext,
  verifyPublicPolicy,
  type GovernedOperation,
  type PublicAuthorityContext,
  type PublicPolicy,
  type PublicPolicyCore,
  type PublicPolicyDecision,
  type PublicPolicyReasonCode,
} from "@gis-ai-go/evidence";

import checkedInPolicy from "./public-catalogue-v1.json" with { type: "json" };

const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]*$/u;
const TRACE_ID = /^[0-9a-f]{32}$/u;
const MAX_CATALOGUE_RECORDS = 10_000;

const PUBLIC_POLICY_CORE = {
  schema: "gis-ai-go.public-policy.v1",
  version: "1.0.0",
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
  rules: [
    {
      rule_id: "public-catalogue-describe",
      operation: "catalogue.describe",
      effect: "allow-with-obligations",
      obligations: PUBLIC_POLICY_OBLIGATIONS,
    },
    {
      rule_id: "public-catalogue-search",
      operation: "catalogue.search",
      effect: "allow-with-obligations",
      obligations: PUBLIC_POLICY_OBLIGATIONS,
    },
  ],
} as const satisfies PublicPolicyCore;

const expectedPolicy = buildPublicPolicy(PUBLIC_POLICY_CORE);
if (
  !verifyPublicPolicy(checkedInPolicy) ||
  canonicalJson(checkedInPolicy) !== canonicalJson(expectedPolicy)
) {
  throw new Error("The checked-in public catalogue policy failed its content identity check");
}

/** The exact checked-in compiled policy used by the anonymous public slice. */
export const PUBLIC_CATALOGUE_POLICY: PublicPolicy = canonicalJsonClone(
  checkedInPolicy,
) as PublicPolicy;

export class PublicPolicyInputError extends TypeError {
  public constructor(message: string) {
    super(message);
    this.name = "PublicPolicyInputError";
  }
}

export interface PublicPolicyEvaluationInput {
  readonly requestId: string;
  readonly traceId: string;
  readonly operation: string;
  /** A parsed, checksum-verified catalogue snapshot. */
  readonly catalogue: CatalogueBundle;
}

interface PublicPolicyEvaluationBase {
  readonly allowed: boolean;
  readonly effect: "allow-with-obligations" | "deny";
  readonly reasonCode: PublicPolicyReasonCode;
  readonly authorityContext: PublicAuthorityContext;
  readonly policy: PublicPolicy;
}

export interface PublicPolicyDecisionEvaluation extends PublicPolicyEvaluationBase {
  readonly decision: PublicPolicyDecision;
}

export interface UnknownOperationDenial extends PublicPolicyEvaluationBase {
  readonly allowed: false;
  readonly effect: "deny";
  readonly reasonCode: "operation-not-allowed";
  readonly decision: null;
}

export type PublicPolicyEvaluation = PublicPolicyDecisionEvaluation | UnknownOperationDenial;

function isRecord(value: unknown): value is Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    return false;
  }
  const prototype = Object.getPrototypeOf(value) as object | null;
  return prototype === Object.prototype || prototype === null;
}

/**
 * Check only the policy-relevant publication boundary of a parsed catalogue.
 * No record content or caller-supplied authority claims participate.
 */
export function isPublicCatalogueBoundary(value: unknown): boolean {
  try {
    if (!isRecord(value) || value.schema !== "gis-ai-go-okf-bundle.v1") {
      return false;
    }
    const scope = value.scope;
    const records = value.records;
    if (
      !isRecord(scope) ||
      scope.kind !== "bounded-public-metadata-discovery" ||
      scope.metadataOnly !== true ||
      scope.containsProtectedData !== false ||
      !Array.isArray(records) ||
      records.length < 1 ||
      records.length > MAX_CATALOGUE_RECORDS ||
      value.recordCount !== records.length
    ) {
      return false;
    }
    return records.every((record) => {
      if (!isRecord(record)) return false;
      const publication = record.publication;
      const access = record.access;
      return (
        isRecord(publication) &&
        publication.classification === "public" &&
        publication.containsPersonalData === false &&
        publication.containsProtectedData === false &&
        isRecord(access) &&
        access.tier === "open"
      );
    });
  } catch {
    return false;
  }
}

function isGovernedOperation(operation: string): operation is GovernedOperation {
  return (GOVERNED_OPERATIONS as readonly string[]).includes(operation);
}

function assertIdentifiers(requestId: string, traceId: string): void {
  if (requestId.length > 128 || !REQUEST_ID.test(requestId)) {
    throw new PublicPolicyInputError("requestId must be a valid bounded request identifier");
  }
  if (!TRACE_ID.test(traceId)) {
    throw new PublicPolicyInputError("traceId must be 32 lower-case hexadecimal characters");
  }
}

function freezeEvaluation<T extends PublicPolicyEvaluation>(evaluation: T): T {
  return Object.freeze(evaluation);
}

/**
 * Evaluate the compiled policy without accepting identity or entitlement input.
 * Unknown operations are explicitly denied and are not forced into the closed
 * governed-operation decision schema.
 */
export function evaluatePublicCataloguePolicy(
  input: PublicPolicyEvaluationInput,
): PublicPolicyEvaluation {
  assertIdentifiers(input.requestId, input.traceId);
  const authorityContext = getPublicAuthorityContext();
  if (!verifyPublicAuthorityContext(authorityContext)) {
    throw new Error("The server-owned authority context failed closed");
  }

  if (!isGovernedOperation(input.operation)) {
    return freezeEvaluation({
      allowed: false,
      effect: "deny",
      reasonCode: "operation-not-allowed",
      authorityContext,
      policy: PUBLIC_CATALOGUE_POLICY,
      decision: null,
    });
  }

  const rule = PUBLIC_CATALOGUE_POLICY.rules.find(
    (candidate) => candidate.operation === input.operation,
  );
  let effect: "allow-with-obligations" | "deny" = "deny";
  let reasonCode: PublicPolicyReasonCode = "operation-not-allowed";
  let obligations = [] as readonly [] | typeof PUBLIC_POLICY_OBLIGATIONS;

  if (rule !== undefined) {
    if (isPublicCatalogueBoundary(input.catalogue)) {
      effect = "allow-with-obligations";
      reasonCode = "public-catalogue-read-allowed";
      obligations = PUBLIC_POLICY_OBLIGATIONS;
    } else {
      reasonCode = "publication-not-public";
    }
  }

  const decision = buildPublicPolicyDecision({
    schema: "gis-ai-go.public-policy-decision.v1",
    canonicalisation: CANONICALISATION,
    request_id: input.requestId,
    trace_id: input.traceId,
    authority_context_id: authorityContext.context_id,
    policy_id: PUBLIC_CATALOGUE_POLICY.policy_id,
    policy_version: PUBLIC_CATALOGUE_POLICY.version,
    policy_default_effect: "deny",
    operation: input.operation,
    effect,
    reason_code: reasonCode,
    obligations,
  });

  return freezeEvaluation({
    allowed: effect === "allow-with-obligations",
    effect,
    reasonCode,
    authorityContext,
    policy: PUBLIC_CATALOGUE_POLICY,
    decision,
  });
}

export * from "./public-read-v2.js";
export * from "./evidence-inspect-v3.js";
