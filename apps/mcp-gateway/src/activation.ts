export const ACTIVATION_BLOCK_REASON =
  "inline-evidence-and-public-policy-unavailable" as const;

export interface BlockedCatalogueActivation {
  readonly state: "blocked";
  readonly reason: typeof ACTIVATION_BLOCK_REASON;
  readonly activeTools: readonly [];
  readonly activeApiOperations: readonly [];
}

/**
 * The only production activation state in this candidate.
 *
 * EVID-204 must replace this closed value with a reviewed policy decision and
 * inline receipt factory before any catalogue operation is mounted or advertised.
 * There is deliberately no environment-variable or command-line override.
 */
export const catalogueActivation: BlockedCatalogueActivation = Object.freeze({
  state: "blocked",
  reason: ACTIVATION_BLOCK_REASON,
  activeTools: Object.freeze([]) as readonly [],
  activeApiOperations: Object.freeze([]) as readonly [],
});
