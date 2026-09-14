/** Inactive, closed application over the admitted public capture; no transport. */
import { types as utilTypes } from "node:util";
import {
  buildWeb216CpihReceipt,
  buildWeb216CpihResult,
  canonicalJsonClone,
  EvidenceReconciliationIndexError,
  verifyWeb216CpihReceipt,
  type EvidenceSoftwareIdentity,
  type PublicEvidenceLedger,
  type StoredPublicEvidence,
  type Web216CpihReconciliationIndex,
} from "@gis-ai-go/evidence";
import {
  createWeb216CpihReadinessIntegrity,
  evidenceReconciliationClaimCapacity,
  verifyEvidenceReadinessIntegrity,
} from "./readiness-integrity.js";
import { normaliseWeb216CpihQueryProposal, resolveWeb216CpihSelection } from "./web216-cpih-selection.js";

export type Web216CpihApplicationErrorCode =
  | "unavailable" | "pending" | "conflict" | "not-found" | "cancelled";
export class Web216CpihApplicationError extends Error {
  public constructor(public readonly code: Web216CpihApplicationErrorCode) {
    super(`Experimental captured-data operation ${code}`);
    this.name = "Web216CpihApplicationError";
  }
}

export interface Web216CpihCallContext {
  readonly requestId: string;
  readonly traceId: string;
  readonly signal?: AbortSignal;
}
export interface Web216CpihApplicationOptions {
  readonly ledger: PublicEvidenceLedger;
  readonly reconciliationIndex: Web216CpihReconciliationIndex;
  readonly projection: unknown;
  /** Trusted server build identity; never a tool argument or provider field. */
  readonly software: EvidenceSoftwareIdentity;
  readonly now?: () => Date;
}

function unavailable(): never { throw new Web216CpihApplicationError("unavailable"); }
function cancelled(signal: AbortSignal | undefined): void {
  if (signal?.aborted === true) throw new Web216CpihApplicationError("cancelled");
}

function capturedResult(projection: unknown, stored: StoredPublicEvidence) {
  if (stored.record.schema !== "gis-ai-go.public-evidence-record.v3") unavailable();
  const receipt = stored.record.receipt;
  const result = buildWeb216CpihResult(projection, receipt.operation.period);
  if (!verifyWeb216CpihReceipt(receipt, {
    projection, normalisedParameters: { period: receipt.operation.period },
    resultCore: result, expectedSoftware: receipt.software,
  }).valid) unavailable();
  return canonicalJsonClone({
    schema: "gis-ai-go.web216-cpih-query-result.v1",
    result,
    evidence: { receipt, storage: stored.reference, record: stored.record, event: stored.event },
    boundary: { provider_egress: false, activated_supported_release: false, attested: false },
  } as const);
}

export type Web216CpihQueryResult = ReturnType<typeof capturedResult>;
const APPLICATIONS = new WeakSet<object>();
export interface Web216CpihApplication {
  readonly resolve: typeof resolveWeb216CpihSelection;
  readonly query: (input: unknown, context: Web216CpihCallContext) => Web216CpihQueryResult;
  /** Reads the original persisted operation; does not claim an inspection receipt. */
  readonly inspect: (input: unknown) => Web216CpihQueryResult;
  readonly readiness: () => { readonly status: "ready" | "blocked"; readonly new_claims_available: boolean };
}
export function isWeb216CpihApplication(value: unknown): value is Web216CpihApplication {
  return typeof value === "object" && value !== null && APPLICATIONS.has(value);
}

export function createWeb216CpihApplication(options: Web216CpihApplicationOptions): Web216CpihApplication {
  if (options === null || typeof options !== "object" || utilTypes.isProxy(options) ||
      Object.getPrototypeOf(options) !== Object.prototype) unavailable();
  const allowed = ["ledger", "reconciliationIndex", "projection", "software", "now"];
  const descriptors = Object.getOwnPropertyDescriptors(options);
  for (const key of Reflect.ownKeys(options)) {
    const descriptor = typeof key === "string" ? descriptors[key] : undefined;
    if (typeof key !== "string" || !allowed.includes(key) || descriptor === undefined ||
        !("value" in descriptor) || descriptor.enumerable !== true) unavailable();
  }
  for (const key of allowed.slice(0, 4)) if (!Object.hasOwn(descriptors, key)) unavailable();
  const projection = canonicalJsonClone(options.projection);
  const software = canonicalJsonClone(options.software);
  const now = options.now ?? (() => new Date());
  if (typeof now !== "function") unavailable();
  // Validate both admitted rows and the trusted software/time before admitting
  // any request. Construction does not execute a query or persist a receipt.
  for (const period of ["2026-01", "2026-07"] as const) {
    buildWeb216CpihReceipt({ projection, software, period,
      requestId: "web216-construction-check", traceId: "1".repeat(32), createdAt: now().toISOString() });
  }
  const ledger = options.ledger;
  const index = options.reconciliationIndex;
  const integrity = createWeb216CpihReadinessIntegrity(ledger, index);

  function query(input: unknown, context: Web216CpihCallContext): Web216CpihQueryResult {
    const proposal = normaliseWeb216CpihQueryProposal(input);
    cancelled(context.signal);
    try {
      verifyEvidenceReadinessIntegrity(integrity);
      // Validate correlation/time and admitted material before acquiring a claim.
      // This receipt is a proposal until durable storage and reconciliation pass.
      const receipt = buildWeb216CpihReceipt({ projection, software, period: proposal.period,
        requestId: context.requestId, traceId: context.traceId, createdAt: now().toISOString() });
      // Existing claims remain inspectable/replayable at capacity. A new key may
      // not consume an irreversible claim when the linked ledger is already full.
      if (index.lookup(proposal.idempotency_key).status === "not-found" &&
          ledger.appendCapacity().status !== "available") unavailable();
      const claim = index.claim({ idempotencyKey: proposal.idempotency_key, period: proposal.period,
        requestId: context.requestId, traceId: context.traceId });
      if (claim.status === "completed") return capturedResult(projection, claim.stored);
      if (claim.status === "pending") throw new Web216CpihApplicationError("pending");
      cancelled(context.signal);
      const resultCore = buildWeb216CpihResult(projection, proposal.period);
      const material = { projection, normalisedParameters: { period: proposal.period }, resultCore, expectedSoftware: software };
      if (!verifyWeb216CpihReceipt(receipt, material).valid) unavailable();
      index.resolve(claim.claim, receipt);
      ledger.persistReceipt(receipt, material);
      const complete = index.lookup(proposal.idempotency_key);
      if (complete.status !== "completed") unavailable();
      return capturedResult(projection, complete.stored);
    } catch (error) {
      if (error instanceof Web216CpihApplicationError) throw error;
      if (error instanceof EvidenceReconciliationIndexError && error.code === "conflict") {
        throw new Web216CpihApplicationError("conflict");
      }
      return unavailable();
    }
  }

  function inspect(input: unknown): Web216CpihQueryResult {
    try {
      const request = canonicalJsonClone(input) as Record<string, unknown>;
      if (request === null || typeof request !== "object" || Array.isArray(request) ||
          Object.keys(request).length !== 1) unavailable();
      verifyEvidenceReadinessIntegrity(integrity);
      let stored: StoredPublicEvidence | null;
      if (typeof request.receipt_id === "string" &&
          /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u.test(request.receipt_id)) {
        stored = ledger.inspect(request.receipt_id);
      } else if (typeof request.idempotency_key === "string") {
        const lookup = index.lookup(request.idempotency_key);
        if (lookup.status === "pending") throw new Web216CpihApplicationError("pending");
        stored = lookup.status === "completed" ? lookup.stored : null;
      } else return unavailable();
      if (stored === null) throw new Web216CpihApplicationError("not-found");
      return capturedResult(projection, stored);
    } catch (error) {
      if (error instanceof Web216CpihApplicationError) throw error;
      return unavailable();
    }
  }

  const application: Web216CpihApplication = Object.freeze({
    resolve: resolveWeb216CpihSelection, query, inspect,
    readiness: () => {
      try {
        const capacity = evidenceReconciliationClaimCapacity(integrity);
        const available = capacity.status === "available" && ledger.appendCapacity().status === "available";
        return Object.freeze({ status: available ? "ready" : "blocked", new_claims_available: available });
      } catch { return Object.freeze({ status: "blocked", new_claims_available: false }); }
    },
  });
  APPLICATIONS.add(application);
  return application;
}
