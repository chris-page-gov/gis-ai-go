import { types as utilTypes } from "node:util";

import {
  PublicEvidenceLedger,
  PublicEvidenceReconciliationIndex,
} from "@gis-ai-go/evidence";

export const EVIDENCE_READINESS_INTEGRITY_KIND =
  "gis-ai-go.evidence-readiness-integrity.v1" as const;
export const EVIDENCE_READINESS_INTEGRITY_FAILURE_MESSAGE =
  "Configured evidence storage failed readiness verification" as const;

export interface EvidenceReadinessIntegrity {
  readonly kind: typeof EVIDENCE_READINESS_INTEGRITY_KIND;
}

const VERIFIERS = new WeakMap<object, () => void>();
const LEDGER_PROTOTYPE = PublicEvidenceLedger.prototype;
const RECONCILIATION_PROTOTYPE = PublicEvidenceReconciliationIndex.prototype;
const VERIFY_LEDGER = PublicEvidenceLedger.prototype.verify;
const VERIFY_RECONCILIATION = PublicEvidenceReconciliationIndex.prototype.verify;
const LEDGER_DISPATCH_METHODS = Object.freeze({
  verify: VERIFY_LEDGER,
  persistReceipt: PublicEvidenceLedger.prototype.persistReceipt,
  inspect: PublicEvidenceLedger.prototype.inspect,
  inspectReceipts: PublicEvidenceLedger.prototype.inspectReceipts,
});
const RECONCILIATION_DISPATCH_METHODS = Object.freeze({
  verify: VERIFY_RECONCILIATION,
  lookup: PublicEvidenceReconciliationIndex.prototype.lookup,
  claim: PublicEvidenceReconciliationIndex.prototype.claim,
  resolve: PublicEvidenceReconciliationIndex.prototype.resolve,
});

function hasExactDispatchMethods(
  value: object,
  prototype: object,
  expected: Readonly<Record<string, (...args: never[]) => unknown>>,
): boolean {
  for (const [name, implementation] of Object.entries(expected)) {
    if (Object.getOwnPropertyDescriptor(value, name) !== undefined) return false;
    const descriptor = Object.getOwnPropertyDescriptor(prototype, name);
    if (
      descriptor === undefined ||
      !("value" in descriptor) ||
      descriptor.value !== implementation
    ) {
      return false;
    }
  }
  return true;
}

function assertExactStores(
  ledger: PublicEvidenceLedger,
  reconciliationIndex: PublicEvidenceReconciliationIndex,
): void {
  if (
    typeof ledger !== "object" ||
    ledger === null ||
    utilTypes.isProxy(ledger) ||
    typeof reconciliationIndex !== "object" ||
    reconciliationIndex === null ||
    utilTypes.isProxy(reconciliationIndex)
  ) {
    throw new TypeError(
      "Readiness integrity requires one exact linked evidence ledger and reconciliation index",
    );
  }
  let ledgerPrototype: object | null;
  let reconciliationPrototype: object | null;
  let linkedLedger: PropertyDescriptor | undefined;
  let ledgerDescriptor: PropertyDescriptor | undefined;
  let reconciliationDescriptor: PropertyDescriptor | undefined;
  try {
    ledgerPrototype = Object.getPrototypeOf(ledger) as object | null;
    reconciliationPrototype = Object.getPrototypeOf(reconciliationIndex) as object | null;
    linkedLedger = Object.getOwnPropertyDescriptor(reconciliationIndex, "ledger");
    ledgerDescriptor = Object.getOwnPropertyDescriptor(ledger, "descriptor");
    reconciliationDescriptor = Object.getOwnPropertyDescriptor(
      reconciliationIndex,
      "descriptor",
    );
  } catch {
    throw new TypeError(
      "Readiness integrity requires one exact linked evidence ledger and reconciliation index",
    );
  }
  if (
    ledgerPrototype !== LEDGER_PROTOTYPE ||
    reconciliationPrototype !== RECONCILIATION_PROTOTYPE ||
    linkedLedger === undefined ||
    !("value" in linkedLedger) ||
    linkedLedger.value !== ledger ||
    ledgerDescriptor === undefined ||
    !("value" in ledgerDescriptor) ||
    reconciliationDescriptor === undefined ||
    !("value" in reconciliationDescriptor) ||
    !hasExactDispatchMethods(ledger, LEDGER_PROTOTYPE, LEDGER_DISPATCH_METHODS) ||
    !hasExactDispatchMethods(
      reconciliationIndex,
      RECONCILIATION_PROTOTYPE,
      RECONCILIATION_DISPATCH_METHODS,
    )
  ) {
    throw new TypeError(
      "Readiness integrity requires one exact linked evidence ledger and reconciliation index",
    );
  }
}

function verifyExactStores(
  ledger: PublicEvidenceLedger,
  reconciliationIndex: PublicEvidenceReconciliationIndex,
): void {
  assertExactStores(ledger, reconciliationIndex);
  VERIFY_LEDGER.call(ledger);
  // Recheck immediately before reconciliation because its verifier performs a
  // nested ledger receipt inspection through the linked instance.
  assertExactStores(ledger, reconciliationIndex);
  VERIFY_RECONCILIATION.call(reconciliationIndex);
  assertExactStores(ledger, reconciliationIndex);
}

/**
 * Create the inactive readiness verifier for one exact durable evidence pair.
 *
 * Construction verifies both stores immediately. The private verifier repeats
 * those complete checks whenever readiness is evaluated; it carries no operation,
 * route, provider, storage path or activation state.
 */
export function createEvidenceReadinessIntegrity(
  ledger: PublicEvidenceLedger,
  reconciliationIndex: PublicEvidenceReconciliationIndex,
): EvidenceReadinessIntegrity {
  verifyExactStores(ledger, reconciliationIndex);
  // Governed calls dispatch these public methods after asynchronous boundaries.
  // Lock the exact instances and captured prototypes so no own or prototype
  // substitution can enter between readiness and durable evidence dispatch.
  Object.freeze(LEDGER_PROTOTYPE);
  Object.freeze(RECONCILIATION_PROTOTYPE);
  Object.freeze(ledger);
  Object.freeze(reconciliationIndex);
  verifyExactStores(ledger, reconciliationIndex);
  const integrity = Object.freeze({ kind: EVIDENCE_READINESS_INTEGRITY_KIND });
  VERIFIERS.set(integrity, () => verifyExactStores(ledger, reconciliationIndex));
  return integrity;
}

/** Repeat the complete linked-store verification for a branded readiness seam. */
export function verifyEvidenceReadinessIntegrity(
  integrity: EvidenceReadinessIntegrity,
): void {
  if (
    typeof integrity !== "object" ||
    integrity === null ||
    utilTypes.isProxy(integrity)
  ) {
    throw new TypeError("Evidence readiness integrity seam is invalid");
  }
  const verify = VERIFIERS.get(integrity);
  if (verify === undefined) {
    throw new TypeError("Evidence readiness integrity seam is invalid");
  }
  verify();
}
