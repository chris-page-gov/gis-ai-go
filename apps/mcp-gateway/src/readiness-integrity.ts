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
const INSPECT_LEDGER_RECEIPTS = PublicEvidenceLedger.prototype.inspectReceipts;

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
  let ownInspectReceipts: PropertyDescriptor | undefined;
  let prototypeInspectReceipts: PropertyDescriptor | undefined;
  try {
    ledgerPrototype = Object.getPrototypeOf(ledger) as object | null;
    reconciliationPrototype = Object.getPrototypeOf(reconciliationIndex) as object | null;
    linkedLedger = Object.getOwnPropertyDescriptor(reconciliationIndex, "ledger");
    ledgerDescriptor = Object.getOwnPropertyDescriptor(ledger, "descriptor");
    reconciliationDescriptor = Object.getOwnPropertyDescriptor(
      reconciliationIndex,
      "descriptor",
    );
    ownInspectReceipts = Object.getOwnPropertyDescriptor(ledger, "inspectReceipts");
    prototypeInspectReceipts = Object.getOwnPropertyDescriptor(
      LEDGER_PROTOTYPE,
      "inspectReceipts",
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
    ownInspectReceipts !== undefined ||
    prototypeInspectReceipts === undefined ||
    !("value" in prototypeInspectReceipts) ||
    prototypeInspectReceipts.value !== INSPECT_LEDGER_RECEIPTS
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
