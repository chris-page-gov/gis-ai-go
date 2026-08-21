import type { PublicEvidenceReconciliationIndex } from "@gis-ai-go/evidence";

const DATA_QUERY_INDEXES = new WeakMap<object, PublicEvidenceReconciliationIndex>();
const EVIDENCE_INSPECT_INDEXES = new WeakMap<object, PublicEvidenceReconciliationIndex>();

export function registerReconciledDataQueryApplication(
  application: object,
  index: PublicEvidenceReconciliationIndex,
): void {
  DATA_QUERY_INDEXES.set(application, index);
}

export function registerReconciledEvidenceInspectApplication(
  application: object,
  index: PublicEvidenceReconciliationIndex,
): void {
  EVIDENCE_INSPECT_INDEXES.set(application, index);
}

export function hasReconciledDataQueryApplication(application: object): boolean {
  return DATA_QUERY_INDEXES.has(application);
}

export function hasReconciledEvidenceInspectApplication(application: object): boolean {
  return EVIDENCE_INSPECT_INDEXES.has(application);
}

export function haveExactlyLinkedReconciliationApplications(
  dataQueryApplication: object,
  evidenceInspectApplication: object,
): boolean {
  const dataIndex = DATA_QUERY_INDEXES.get(dataQueryApplication);
  return (
    dataIndex !== undefined &&
    EVIDENCE_INSPECT_INDEXES.get(evidenceInspectApplication) === dataIndex
  );
}
