/** Separately branded capture application; no transport, schema migration or provider. */
import { types as utilTypes } from "node:util";
import {
  buildWeb216CpihReceipt, buildWeb216CpihResult, canonicalJson, canonicalJsonClone,
  isWeb216D1SnapshotStore, lookupWeb216TransactionalRecord, planWeb216TransactionalAppend,
  Web216D1SnapshotError, Web216TransactionalError,
  type EvidenceSoftwareIdentity, type Web216D1SnapshotStore,
  type Web216TransactionalMaterial, type Web216TransactionalRecord,
  type Web216TransactionalSnapshot,
} from "@gis-ai-go/evidence/web216-pure";
import {
  normaliseWeb216CpihQueryProposal, resolveWeb216CpihSelection, Web216CpihSelectionError,
  type Web216CpihSelectionPlan,
} from "./web216-cpih-selection.js";

export type Web216HostedCpihApplicationErrorCode =
  | "invalid-input" | "unavailable" | "capacity" | "conflict" | "retryable-conflict"
  | "not-found" | "cancelled" | "uncertain-write";
export class Web216HostedCpihApplicationError extends Error {
  public constructor(public readonly code: Web216HostedCpihApplicationErrorCode) {
    super(`Experimental hosted capture operation ${code}`);
    this.name = "Web216HostedCpihApplicationError";
  }
}
function fail(code: Web216HostedCpihApplicationErrorCode): never { throw new Web216HostedCpihApplicationError(code); }
function cancelled(signal?: AbortSignal): void { if (signal?.aborted === true) fail("cancelled"); }
function translate(error: unknown): never {
  if (error instanceof Web216HostedCpihApplicationError) throw error;
  if (error instanceof Web216CpihSelectionError) fail("invalid-input");
  if (error instanceof Web216TransactionalError && (error.code === "conflict" || error.code === "capacity")) fail(error.code);
  if (error instanceof Web216D1SnapshotError) {
    if (error.code === "cancelled-before-write") fail("cancelled");
    if (error.code === "uncertain-write") fail("uncertain-write");
    if (error.code === "snapshot-too-large") fail("capacity");
  }
  return fail("unavailable");
}
function plain(value: unknown, allowed: readonly string[], required: readonly string[]): Record<string, unknown> {
  if (value === null || typeof value !== "object" || utilTypes.isProxy(value) || Object.getPrototypeOf(value) !== Object.prototype) fail("invalid-input");
  const descriptors = Object.getOwnPropertyDescriptors(value);
  for (const key of Reflect.ownKeys(value)) {
    const descriptor = typeof key === "string" ? descriptors[key] : undefined;
    if (typeof key !== "string" || !allowed.includes(key) || descriptor === undefined ||
        !("value" in descriptor) || descriptor.enumerable !== true) fail("invalid-input");
  }
  if (required.some((key) => !Object.hasOwn(descriptors, key))) fail("invalid-input");
  return value as Record<string, unknown>;
}
export interface Web216HostedCpihSignalContext { readonly signal?: AbortSignal }
export interface Web216HostedCpihCallContext extends Web216HostedCpihSignalContext {
  /** Server-generated correlation only; never copy JSON-RPC IDs or a raw key. */
  readonly requestId: string;
  readonly traceId: string;
}
function checkedSignal(value: unknown): AbortSignal | undefined {
  if (value === undefined) return undefined;
  if (typeof value !== "object" || value === null || utilTypes.isProxy(value) || !(value instanceof AbortSignal)) fail("invalid-input");
  return value;
}
function signalContext(value: Web216HostedCpihSignalContext = {}): AbortSignal | undefined {
  return checkedSignal(plain(value, ["signal"], []).signal);
}
function callContext(value: Web216HostedCpihCallContext) {
  const input = plain(value, ["requestId", "traceId", "signal"], ["requestId", "traceId"]);
  if (typeof input.requestId !== "string" || input.requestId.length > 128 ||
      !/^[A-Za-z0-9][A-Za-z0-9._:-]*$/u.test(input.requestId) || /gis-ai-go:ik:v1:[0-9a-f]{64}/iu.test(input.requestId) ||
      typeof input.traceId !== "string" || !/^(?!0{32}$)[0-9a-f]{32}$/u.test(input.traceId)) fail("invalid-input");
  return Object.freeze({ requestId: input.requestId, traceId: input.traceId, signal: checkedSignal(input.signal) });
}

function capturedResult(projection: unknown, snapshot: Web216TransactionalSnapshot, record: Web216TransactionalRecord) {
  const event = snapshot.events.find((item) => item.record_id === record.record_id);
  if (event === undefined) fail("unavailable");
  return canonicalJsonClone({
    schema: "gis-ai-go.web216-hosted-cpih-result.v1",
    result: buildWeb216CpihResult(projection, record.period),
    evidence: {
      receipt: record.receipt, record, event, checkpoint: snapshot.head,
      storage_observation: {
        schema: "gis-ai-go.web216-hosted-storage-observation.v1",
        persistence: "present-in-verified-adapter-snapshot",
        checkpoint_scope: "verified-returned-snapshot",
        read_freshness: "not-established-by-application",
        store_id: snapshot.descriptor.store_id,
        integrity: "full-snapshot-content-and-chain-verified-internally",
        returned_evidence_scope: "selected-record-event-and-head-subset",
        attestation: "not-attested", independent_rollback_anchor: false,
        disaster_recovery: "not-established", deployment: "not-established-by-application",
      },
    },
    boundary: { provider_egress: false, activated_supported_release: false, attested: false },
  } as const);
}
export type Web216HostedCpihResult = ReturnType<typeof capturedResult>;
export interface Web216HostedCpihReadiness {
  readonly status: "ready" | "read-only" | "unavailable";
  readonly new_writes_available: boolean;
  readonly inspection_available: boolean;
  readonly record_count: number | null;
  readonly maximum_records: number | null;
}
export interface Web216HostedCpihApplication {
  readonly resolve: (input: unknown, context?: Web216HostedCpihSignalContext) => Promise<Web216CpihSelectionPlan>;
  readonly readiness: (context?: Web216HostedCpihSignalContext) => Promise<Web216HostedCpihReadiness>;
  readonly query: (input: unknown, context: Web216HostedCpihCallContext) => Promise<Web216HostedCpihResult>;
  /** Re-reads existing evidence; does not invent a new inspection receipt. */
  readonly inspect: (input: unknown, context?: Web216HostedCpihSignalContext) => Promise<Web216HostedCpihResult>;
}
export interface Web216HostedCpihApplicationOptions {
  readonly store: Web216D1SnapshotStore;
  readonly projection: unknown;
  readonly software: EvidenceSoftwareIdentity;
  /** Independently retained provisioning identity, never adopted from a DB row. */
  readonly expectedStoreId: string;
  readonly now?: () => Date;
}
const APPLICATIONS = new WeakSet<object>();
export function isWeb216HostedCpihApplication(value: unknown): value is Web216HostedCpihApplication {
  return typeof value === "object" && value !== null && APPLICATIONS.has(value);
}

export function createWeb216HostedCpihApplication(options: Web216HostedCpihApplicationOptions): Web216HostedCpihApplication {
  plain(options, ["store", "projection", "software", "expectedStoreId", "now"], ["store", "projection", "software", "expectedStoreId"]);
  if (!isWeb216D1SnapshotStore(options.store) || typeof options.expectedStoreId !== "string" ||
      !/^gis-ai-go:web216-transactional-store:sha256:[0-9a-f]{64}$/u.test(options.expectedStoreId)) fail("unavailable");
  const store = options.store;
  const projection = canonicalJsonClone(options.projection);
  const software = canonicalJsonClone(options.software);
  const material: Web216TransactionalMaterial = canonicalJsonClone({ projection, expectedSoftware: software, expectedStoreId: options.expectedStoreId });
  const now = options.now ?? (() => new Date());
  if (typeof now !== "function") fail("unavailable");
  try {
    for (const period of ["2026-01", "2026-07"] as const) buildWeb216CpihReceipt({
      projection, software, period, requestId: "hosted-construction-check", traceId: "1".repeat(32), createdAt: now().toISOString(),
    });
  } catch { return fail("unavailable"); }

  async function read(signal?: AbortSignal): Promise<Web216TransactionalSnapshot> {
    cancelled(signal);
    let snapshot: Web216TransactionalSnapshot;
    try { snapshot = await store.readSnapshot(); } catch (error) { cancelled(signal); return translate(error); }
    cancelled(signal);
    if (snapshot.descriptor.store_id !== material.expectedStoreId || canonicalJson(snapshot.descriptor.software) !== canonicalJson(software)) fail("unavailable");
    return snapshot;
  }
  async function resolve(input: unknown, context?: Web216HostedCpihSignalContext): Promise<Web216CpihSelectionPlan> {
    try { cancelled(signalContext(context)); return resolveWeb216CpihSelection(input); } catch (error) { return translate(error); }
  }
  async function readiness(context?: Web216HostedCpihSignalContext): Promise<Web216HostedCpihReadiness> {
    try {
      const snapshot = await read(signalContext(context));
      const available = snapshot.records.length < snapshot.descriptor.maximum_records;
      return Object.freeze({ status: available ? "ready" : "read-only", new_writes_available: available,
        inspection_available: true, record_count: snapshot.records.length, maximum_records: snapshot.descriptor.maximum_records });
    } catch (error) {
      if (error instanceof Web216HostedCpihApplicationError && (error.code === "cancelled" || error.code === "invalid-input")) throw error;
      return Object.freeze({ status: "unavailable", new_writes_available: false, inspection_available: false, record_count: null, maximum_records: null });
    }
  }
  async function query(input: unknown, suppliedContext: Web216HostedCpihCallContext): Promise<Web216HostedCpihResult> {
    try {
      const proposal = normaliseWeb216CpihQueryProposal(input);
      const context = callContext(suppliedContext);
      const snapshot = await read(context.signal);
      const existing = lookupWeb216TransactionalRecord(snapshot, proposal.idempotency_key, material);
      if (existing.status === "found-model-record") {
        if (existing.record.period !== proposal.period) fail("conflict");
        cancelled(context.signal);
        return capturedResult(projection, snapshot, existing.record);
      }
      const createdAt = now().toISOString();
      const receipt = buildWeb216CpihReceipt({ projection, software, period: proposal.period, createdAt,
        requestId: context.requestId, traceId: context.traceId });
      const outcome = planWeb216TransactionalAppend(snapshot, { idempotencyKey: proposal.idempotency_key, receipt, recordedAt: createdAt }, material);
      if (outcome.status !== "append-plan-not-committed") fail("unavailable");
      cancelled(context.signal);
      const published = await store.publish(outcome.plan, context.signal === undefined ? {} : { signal: context.signal });
      // Once publish has started, cancellation cannot establish definite absence.
      if (context.signal?.aborted === true) fail("uncertain-write");
      if (published.status === "stale-head") fail("retryable-conflict");
      return capturedResult(projection, published.snapshot, published.record);
    } catch (error) { return translate(error); }
  }
  async function inspect(input: unknown, context?: Web216HostedCpihSignalContext): Promise<Web216HostedCpihResult> {
    try {
      const request = canonicalJsonClone(input) as Record<string, unknown>;
      if (request === null || typeof request !== "object" || Array.isArray(request) || Object.keys(request).length !== 1) fail("invalid-input");
      const byReceipt = typeof request.receipt_id === "string" && /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u.test(request.receipt_id);
      const byKey = typeof request.idempotency_key === "string" && /^gis-ai-go:ik:v1:(?!0{64}$)[0-9a-f]{64}$/u.test(request.idempotency_key);
      if (!byReceipt && !byKey) fail("invalid-input");
      const signal = signalContext(context); const snapshot = await read(signal);
      let record: Web216TransactionalRecord | undefined;
      if (byReceipt) record = snapshot.records.find((item) => item.receipt.receipt_id === request.receipt_id);
      else {
        const found = lookupWeb216TransactionalRecord(snapshot, request.idempotency_key as string, material);
        if (found.status === "found-model-record") record = found.record;
      }
      if (record === undefined) fail("not-found");
      cancelled(signal);
      return capturedResult(projection, snapshot, record);
    } catch (error) { return translate(error); }
  }
  const application = Object.freeze({ resolve, readiness, query, inspect });
  APPLICATIONS.add(application);
  return application;
}
