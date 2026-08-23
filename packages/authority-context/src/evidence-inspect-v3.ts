import {
  CANONICALISATION,
  buildEvidenceInspectionAuthorityContext,
  canonicalJsonClone,
  verifyEvidenceInspectionAuthorityContext,
  type EvidenceInspectionAuthorityContext,
  type EvidenceInspectionAuthorityContextCore,
} from "@gis-ai-go/evidence";

const PUBLIC_EVIDENCE_INSPECTION_AUTHORITY_CONTEXT_CORE = {
  schema: "gis-ai-go.public-authority-context.v3",
  canonicalisation: CANONICALISATION,
  construction: {
    source: "server",
    profile: "anonymous-open",
    product: "gis-ai-go-gateway",
  },
  access: {
    authentication: "none",
    tier: "open",
    publication_classification: "public",
    contains_personal_data: false,
    contains_protected_data: false,
    read_only: true,
  },
  permitted_operations: ["evidence.inspect"],
  evidence: {
    receipt: "inline-required",
    persistence: "not-persisted",
    attestation: "not-attested",
    ledger_event: "not-created",
  },
} as const satisfies EvidenceInspectionAuthorityContextCore;

/** Exact server-owned authority context for current-call evidence inspection. */
export const PUBLIC_EVIDENCE_INSPECTION_AUTHORITY_CONTEXT:
  EvidenceInspectionAuthorityContext = buildEvidenceInspectionAuthorityContext(
    PUBLIC_EVIDENCE_INSPECTION_AUTHORITY_CONTEXT_CORE,
  );

if (!verifyEvidenceInspectionAuthorityContext(
  PUBLIC_EVIDENCE_INSPECTION_AUTHORITY_CONTEXT,
)) {
  throw new Error("The evidence inspection authority context failed closed");
}

/** Return a detached frozen copy of the inspection authority context. */
export function getPublicEvidenceInspectionAuthorityContext():
  EvidenceInspectionAuthorityContext {
  return canonicalJsonClone(PUBLIC_EVIDENCE_INSPECTION_AUTHORITY_CONTEXT);
}
