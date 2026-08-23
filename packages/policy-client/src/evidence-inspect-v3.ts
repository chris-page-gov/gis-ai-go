import { types as utilTypes } from "node:util";

import { getPublicEvidenceInspectionAuthorityContext } from "@gis-ai-go/authority-context";
import {
  CANONICALISATION,
  EVIDENCE_INSPECTION_OBLIGATIONS,
  buildEvidenceInspectionPolicy,
  buildEvidenceInspectionPolicyDecision,
  canonicalJson,
  canonicalJsonClone,
  isRestartVerifiedStoredPublicEvidence,
  verifyEvidenceInspectionAuthorityContext,
  verifyEvidenceInspectionPolicy,
  verifyEvidenceInspectionPolicyDecision,
  verifyStoredPublicEvidenceProjection,
  type EvidenceInspectionAuthorityContext,
  type EvidenceInspectionPolicy,
  type EvidenceInspectionPolicyCore,
  type EvidenceInspectionPolicyDecision,
  type StoredPublicEvidence,
} from "@gis-ai-go/evidence";

import checkedInPolicy from "./public-evidence-inspect-v3.json" with { type: "json" };

const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]*$/u;
const TRACE_ID = /^[0-9a-f]{32}$/u;

const PUBLIC_EVIDENCE_INSPECTION_POLICY_CORE = {
  schema: "gis-ai-go.public-policy.v3",
  version: "3.0.0",
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
    stored_evidence_verification: "restart-verified",
  },
  rules: [{
    rule_id: "public-evidence-inspect",
    operation: "evidence.inspect",
    effect: "allow-with-obligations",
    obligations: EVIDENCE_INSPECTION_OBLIGATIONS,
  }],
} as const satisfies EvidenceInspectionPolicyCore;

const expectedPolicy = buildEvidenceInspectionPolicy(
  PUBLIC_EVIDENCE_INSPECTION_POLICY_CORE,
);
if (
  !verifyEvidenceInspectionPolicy(checkedInPolicy) ||
  canonicalJson(checkedInPolicy) !== canonicalJson(expectedPolicy)
) {
  throw new Error("The checked-in public evidence inspection policy failed closed");
}

/** Exact default-deny policy for verified anonymous-open evidence inspection. */
export const PUBLIC_EVIDENCE_INSPECTION_POLICY: EvidenceInspectionPolicy =
  canonicalJsonClone(checkedInPolicy) as EvidenceInspectionPolicy;

export interface EvidenceInspectionPolicyEvaluationInput {
  readonly requestId: string;
  readonly traceId: string;
  readonly operation: string;
  /** The exact frozen tuple returned by a successful restart-verifying ledger inspection. */
  readonly verifiedStoredEvidence: StoredPublicEvidence;
}

export interface EvidenceInspectionPolicyEvaluation {
  readonly allowed: boolean;
  readonly authorityContext: EvidenceInspectionAuthorityContext;
  readonly policy: EvidenceInspectionPolicy;
  readonly decision: EvidenceInspectionPolicyDecision;
}

function isAnonymousOpenStoredEvidence(stored: StoredPublicEvidence): boolean {
  try {
    const authority = stored.record.receipt.authority_context;
    const decision = stored.record.receipt.policy_decision;
    return (
      authority.construction.profile === "anonymous-open" &&
      authority.access.tier === "open" &&
      authority.access.publication_classification === "public" &&
      authority.access.contains_personal_data === false &&
      authority.access.contains_protected_data === false &&
      decision.effect === "allow-with-obligations" &&
      (decision.reason_code === "public-catalogue-read-allowed" ||
        decision.reason_code === "public-read-operation-allowed")
    );
  } catch {
    return false;
  }
}

function snapshotInput(input: unknown): EvidenceInspectionPolicyEvaluationInput {
  try {
    if (
      input === null ||
      typeof input !== "object" ||
      Array.isArray(input) ||
      utilTypes.isProxy(input) ||
      Object.getPrototypeOf(input) !== Object.prototype
    ) {
      throw new TypeError("unsafe input");
    }
    const descriptors = Object.getOwnPropertyDescriptors(input);
    const keys = Reflect.ownKeys(input);
    const expected = ["operation", "requestId", "traceId", "verifiedStoredEvidence"];
    if (
      keys.some((key) => typeof key !== "string") ||
      keys.length !== expected.length ||
      (keys as string[]).sort().some((key, index) => key !== expected[index]) ||
      Object.values(descriptors).some(
        (descriptor) => !("value" in descriptor) || descriptor.enumerable !== true,
      )
    ) {
      throw new TypeError("unsafe input");
    }
    const requestId = descriptors.requestId?.value as unknown;
    const traceId = descriptors.traceId?.value as unknown;
    const operation = descriptors.operation?.value as unknown;
    const verifiedStoredEvidence = descriptors.verifiedStoredEvidence?.value as unknown;
    if (
      typeof requestId !== "string" ||
      requestId.length > 128 ||
      !REQUEST_ID.test(requestId) ||
      typeof traceId !== "string" ||
      !TRACE_ID.test(traceId) ||
      typeof operation !== "string" ||
      !isRestartVerifiedStoredPublicEvidence(verifiedStoredEvidence) ||
      !verifyStoredPublicEvidenceProjection(verifiedStoredEvidence)
    ) {
      throw new TypeError("invalid input");
    }
    return Object.freeze({
      requestId,
      traceId,
      operation,
      verifiedStoredEvidence,
    });
  } catch {
    throw new TypeError(
      "Evidence inspection policy input must be closed data with restart-verified evidence and without proxies or accessors",
    );
  }
}

/**
 * Decide only after the ledger has returned a restart-verified stored record.
 * A caller-supplied receipt or idempotency key is never policy authority.
 */
export function evaluateEvidenceInspectionPolicy(
  input: EvidenceInspectionPolicyEvaluationInput,
): EvidenceInspectionPolicyEvaluation {
  const snapshot = snapshotInput(input);
  const authorityContext = getPublicEvidenceInspectionAuthorityContext();
  if (!verifyEvidenceInspectionAuthorityContext(authorityContext)) {
    throw new Error("The server-owned inspection authority context failed closed");
  }
  const operationAllowed = snapshot.operation === "evidence.inspect";
  const publicRecord = isAnonymousOpenStoredEvidence(snapshot.verifiedStoredEvidence);
  const allowed = operationAllowed && publicRecord;
  const decision = buildEvidenceInspectionPolicyDecision({
    schema: "gis-ai-go.public-policy-decision.v3",
    canonicalisation: CANONICALISATION,
    request_id: snapshot.requestId,
    trace_id: snapshot.traceId,
    authority_context_id: authorityContext.context_id,
    policy_id: PUBLIC_EVIDENCE_INSPECTION_POLICY.policy_id,
    policy_version: PUBLIC_EVIDENCE_INSPECTION_POLICY.version,
    policy_default_effect: "deny",
    operation: "evidence.inspect",
    inspected_receipt_id: allowed
      ? snapshot.verifiedStoredEvidence.record.receipt.receipt_id
      : null,
    effect: allowed ? "allow-with-obligations" : "deny",
    reason_code: allowed
      ? "anonymous-open-evidence-inspection-allowed"
      : operationAllowed
        ? "stored-evidence-not-public"
        : "operation-not-allowed",
    obligations: allowed ? EVIDENCE_INSPECTION_OBLIGATIONS : [],
  });
  if (!verifyEvidenceInspectionPolicyDecision(decision)) {
    throw new Error("The evidence inspection policy decision failed closed");
  }
  return Object.freeze({
    allowed,
    authorityContext,
    policy: PUBLIC_EVIDENCE_INSPECTION_POLICY,
    decision,
  });
}
