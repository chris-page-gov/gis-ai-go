import {
  CANONICALISATION,
  buildPublicAuthorityContext,
  canonicalJsonClone,
  verifyPublicAuthorityContext,
  type PublicAuthorityContext,
  type PublicAuthorityContextCore,
} from "@gis-ai-go/evidence";

const PUBLIC_AUTHORITY_CONTEXT_CORE = {
  schema: "gis-ai-go.public-authority-context.v1",
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
  permitted_operations: ["catalogue.describe", "catalogue.search"],
  evidence: {
    receipt: "inline-required",
    persistence: "not-persisted",
    attestation: "not-attested",
  },
} as const satisfies PublicAuthorityContextCore;

/**
 * The only authority context in the anonymous public catalogue slice.
 *
 * It is constructed entirely from server-owned constants and contains no
 * identity, entitlement, credential, device or request-time material.
 */
export const PUBLIC_AUTHORITY_CONTEXT: PublicAuthorityContext =
  buildPublicAuthorityContext(PUBLIC_AUTHORITY_CONTEXT_CORE);

if (!verifyPublicAuthorityContext(PUBLIC_AUTHORITY_CONTEXT)) {
  throw new Error("The server-owned public authority context failed its content identity check");
}

/** Return a detached, recursively frozen copy of the server-owned context. */
export function getPublicAuthorityContext(): PublicAuthorityContext {
  return canonicalJsonClone(PUBLIC_AUTHORITY_CONTEXT);
}

export * from "./public-read-v2.js";
