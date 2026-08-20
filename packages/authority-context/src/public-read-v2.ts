import {
  CANONICALISATION,
  buildPublicReadAuthorityContext,
  canonicalJsonClone,
  verifyPublicReadAuthorityContext,
  type PublicReadAuthorityContext,
  type PublicReadAuthorityContextCore,
} from "@gis-ai-go/evidence";

const PUBLIC_READ_AUTHORITY_CONTEXT_CORE = {
  schema: "gis-ai-go.public-authority-context.v2",
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
  permitted_operations: ["data.query", "selection.resolve"],
  evidence: {
    receipt: "inline-required",
    persistence: "not-persisted",
    attestation: "not-attested",
  },
} as const satisfies PublicReadAuthorityContextCore;

/**
 * The server-owned anonymous-open authority for the inactive public-read v2 plane.
 * It carries no caller identity, entitlement, credential or request-time claim.
 */
export const PUBLIC_READ_AUTHORITY_CONTEXT: PublicReadAuthorityContext =
  buildPublicReadAuthorityContext(PUBLIC_READ_AUTHORITY_CONTEXT_CORE);

if (!verifyPublicReadAuthorityContext(PUBLIC_READ_AUTHORITY_CONTEXT)) {
  throw new Error("The server-owned public-read authority context failed its identity check");
}

/** Return a detached, recursively frozen copy without accepting caller input. */
export function getPublicReadAuthorityContext(): PublicReadAuthorityContext {
  return canonicalJsonClone(PUBLIC_READ_AUTHORITY_CONTEXT);
}
