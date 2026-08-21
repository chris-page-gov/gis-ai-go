export const PUBLIC_EVIDENCE_LEDGER_MAX_EVENTS = 1_000_000;

const TEST_ONLY_LOWER_LIMITS = new WeakMap<object, number>();

/** Preserve the accepted ledger ceiling unless an internal test lowers it. */
export function publicEvidenceLedgerEventLimit(options: object): number {
  return TEST_ONLY_LOWER_LIMITS.get(options) ?? PUBLIC_EVIDENCE_LEDGER_MAX_EVENTS;
}

/**
 * Internal test seam for the exact pre-write boundary. It cannot raise the
 * accepted ceiling, survives neither copying nor serialisation, and is not
 * exported by the package barrel.
 */
export function withLowerPublicEvidenceLedgerEventLimitForTest<T extends object>(
  options: T,
  maximumEvents: number,
): T {
  if (
    !Number.isSafeInteger(maximumEvents) ||
    maximumEvents < 1 ||
    maximumEvents > PUBLIC_EVIDENCE_LEDGER_MAX_EVENTS
  ) {
    throw new RangeError("Test evidence event limit must not raise the accepted ceiling");
  }
  TEST_ONLY_LOWER_LIMITS.set(options, maximumEvents);
  return options;
}
