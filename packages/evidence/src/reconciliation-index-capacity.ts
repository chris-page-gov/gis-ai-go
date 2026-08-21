const MAX_LOCAL_CLAIM_ADMISSION = 4_096;

const TEST_ONLY_LOWER_LIMITS = new WeakMap<object, number>();

/** Fixed local safety bound; this is not a deployment or cluster quota. */
export function evidenceReconciliationClaimAdmissionLimit(options: object): number {
  return TEST_ONLY_LOWER_LIMITS.get(options) ?? MAX_LOCAL_CLAIM_ADMISSION;
}

/**
 * Internal test seam for exercising the exact admission boundary without
 * publishing thousands of immutable files. It cannot raise the fixed limit,
 * survives neither copying nor serialisation, and is not exported by the
 * package barrel.
 */
export function withLowerEvidenceReconciliationClaimLimitForTest<T extends object>(
  options: T,
  maximumClaims: number,
): T {
  if (
    !Number.isSafeInteger(maximumClaims) ||
    maximumClaims < 1 ||
    maximumClaims > MAX_LOCAL_CLAIM_ADMISSION
  ) {
    throw new RangeError("Test reconciliation claim limit must lower the fixed local limit");
  }
  TEST_ONLY_LOWER_LIMITS.set(options, maximumClaims);
  return options;
}
