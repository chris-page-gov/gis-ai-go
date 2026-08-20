export const ACTIVATION_BLOCK_REASON =
  "transport-and-interoperability-unverified" as const;

export interface BlockedCatalogueActivation {
  readonly state: "blocked";
  readonly reason: typeof ACTIVATION_BLOCK_REASON;
  readonly activeTools: readonly [];
  readonly activeApiOperations: readonly [];
}

/**
 * The only production activation state in this candidate.
 *
 * EVID-204A supplies reviewed in-process public policy decisions and inline
 * receipts. Transport registration, protocol conformance and interoperability
 * remain unverified, so no catalogue operation is mounted or advertised. There
 * is deliberately no environment-variable or command-line override.
 */
export const catalogueActivation: BlockedCatalogueActivation = Object.freeze({
  state: "blocked",
  reason: ACTIVATION_BLOCK_REASON,
  activeTools: Object.freeze([]) as readonly [],
  activeApiOperations: Object.freeze([]) as readonly [],
});
