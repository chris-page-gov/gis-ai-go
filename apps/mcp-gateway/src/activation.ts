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
 * Reviewed applications and explicit local-conformance transport seams now exist
 * for catalogue and public evidence operations. Host interoperability, release
 * activation and deployment remain unverified, so no operation is mounted or
 * advertised by production defaults. There is deliberately no environment-variable
 * or command-line override.
 */
export const catalogueActivation: BlockedCatalogueActivation = Object.freeze({
  state: "blocked",
  reason: ACTIVATION_BLOCK_REASON,
  activeTools: Object.freeze([]) as readonly [],
  activeApiOperations: Object.freeze([]) as readonly [],
});
