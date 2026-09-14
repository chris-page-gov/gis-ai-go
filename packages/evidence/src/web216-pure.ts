/**
 * Explicit WEB-216 contracts and injected transactional adapter.
 * No filesystem ledger, checkpoint, reconciliation index or registry is imported.
 * Node-compatible crypto/util remain required; this is not a browser-only module.
 * Importing the adapter does not provision a schema, execute SQL or establish storage.
 */
export * from "./canonical-json.js";
export * from "./digest.js";
export { PUBLIC_IDEMPOTENCY_KEY } from "./idempotency-constants.js";
export { isStrictEvidenceDateTime, type EvidenceSoftwareIdentity } from "./receipt.js";
export * from "./web216-cpih-receipt.js";
export * from "./web216-transactional-contract.js";
export * from "./web216-transactional-d1.js";
