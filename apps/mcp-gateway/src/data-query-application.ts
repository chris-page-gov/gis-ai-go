import { randomBytes } from "node:crypto";
import { types as utilTypes } from "node:util";

import {
  PUBLIC_READ_ONS_RESOURCE,
  PUBLIC_DATA_QUERY_APPROVED_CACHE_WARNING,
  CANONICAL_DOMAINS,
  EvidenceReconciliationIndexError,
  PublicEvidenceLedger,
  PublicEvidenceReconciliationIndex,
  buildPublicReadReceipt,
  canonicalJson,
  canonicalJsonClone,
  domainSeparatedSha256,
  evidenceReconciliationRequestFingerprint,
  publicReadResultEvidenceBinding,
  verifyPublicReadAuthorityContext,
  verifyPublicReadPolicy,
  verifyPublicReadPolicyDecision,
  verifyPublicReadReceipt,
  verifyPublicReadResource,
  type EvidenceSoftwareIdentity,
  type PublicEvidenceStorageReference,
  type PublicReadEvidenceReceipt,
} from "@gis-ai-go/evidence";
import {
  ADAPTER_ERROR_CODES,
  ONS_ADAPTER_ID,
  ONS_ADAPTER_REQUEST,
  ONS_ADAPTER_VERSION,
  ONS_OBSERVATION_URI,
  OnsDataApiAdapter,
  isExactApprovedOnsDataQueryCache,
  normaliseAdapterError,
  normalisePristineOnsDataApiAdapterError,
  normaliseW3CTraceContext,
  reservePristineOnsDataApiAdapterExecution,
  requireExactOnsDataApiAdapter,
  requirePristineOnsDataApiAdapter,
  type AdapterErrorCode,
  type AdapterHealth,
  type ApprovedOnsDataQueryCache,
  type ApprovedOnsDataQueryCacheHit,
  type NormalisedAdapterError,
  type OnsDataApiAdapterAdmissionLease,
  type OnsDataApiAdapterExecution,
  type ProviderAdapterEstimate,
  type ProviderAdapterExecutionOptions,
  type ProviderAdapterProvenance,
  type ProviderAdapterResult,
  type ProviderRights,
} from "@gis-ai-go/provider-adapter-sdk";
import {
  evaluatePublicReadPolicy,
  isAllowedPublicReadOperation,
} from "@gis-ai-go/policy-client";

import {
  assertCatalogueProblemContext,
  type CatalogueProblemContext,
} from "./problem.js";
import {
  hasReconciledDataQueryApplication,
  registerReconciledDataQueryApplication,
} from "./reconciliation-applications.js";

const SEMVER = /^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)$/u;
const SHA40 = /^[0-9a-f]{40}$/u;
const NUMERIC_OBSERVATION = /^(?:0|[1-9][0-9]{0,14})$/u;
const DEADLINE =
  /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,9})?(?:Z|([+-])(\d{2}):(\d{2}))$/u;

export const DATA_QUERY_PROBLEM_CODES = Object.freeze([
  "invalid_request",
  "query_cancelled",
  "query_deadline_exceeded",
  "policy_denied",
  "provider_suspended",
  "provider_rate_limited",
  "provider_timeout",
  "provider_unavailable",
  "provider_contract_failed",
  "evidence_unavailable",
] as const);

export type DataQueryProblemCode = (typeof DATA_QUERY_PROBLEM_CODES)[number];

export const DATA_QUERY_RECONCILIATION_PROBLEM_CODES = Object.freeze([
  "idempotency_pending",
  "idempotency_completed",
  "idempotency_conflict",
] as const);

export type DataQueryReconciliationProblemCode =
  (typeof DATA_QUERY_RECONCILIATION_PROBLEM_CODES)[number];

interface DataQueryProblemDefinition {
  readonly type: string;
  readonly title: string;
  readonly status: 400 | 403 | 408 | 429 | 502 | 503 | 504;
  readonly detail: string;
}

const PROBLEM_DEFINITIONS: Readonly<Record<DataQueryProblemCode, DataQueryProblemDefinition>> =
  Object.freeze({
    invalid_request: {
      type: "urn:gis-ai-go:problem:data-query-invalid-request",
      title: "Invalid data query request",
      status: 400,
      detail: "The request must match the reviewed public ONS query.",
    },
    query_cancelled: {
      type: "urn:gis-ai-go:problem:data-query-cancelled",
      title: "Data query cancelled",
      status: 408,
      detail: "The caller cancelled the data query.",
    },
    query_deadline_exceeded: {
      type: "urn:gis-ai-go:problem:data-query-deadline-exceeded",
      title: "Data query deadline exceeded",
      status: 408,
      detail: "The caller deadline elapsed before the data query completed.",
    },
    policy_denied: {
      type: "urn:gis-ai-go:problem:data-query-policy-denied",
      title: "Data query denied",
      status: 403,
      detail: "The public-read policy did not authorise this data query.",
    },
    provider_suspended: {
      type: "urn:gis-ai-go:problem:data-query-provider-suspended",
      title: "Data provider suspended",
      status: 503,
      detail: "The reviewed provider adapter is suspended for invocation.",
    },
    provider_rate_limited: {
      type: "urn:gis-ai-go:problem:data-query-provider-rate-limited",
      title: "Data provider rate limited",
      status: 429,
      detail: "The bounded provider admission limit has been reached.",
    },
    provider_timeout: {
      type: "urn:gis-ai-go:problem:data-query-provider-timeout",
      title: "Data provider timed out",
      status: 504,
      detail: "The provider adapter timed out while caller controls remained active.",
    },
    provider_unavailable: {
      type: "urn:gis-ai-go:problem:data-query-provider-unavailable",
      title: "Data provider unavailable",
      status: 503,
      detail: "The reviewed provider is temporarily unavailable.",
    },
    provider_contract_failed: {
      type: "urn:gis-ai-go:problem:data-query-provider-contract-failed",
      title: "Data provider response rejected",
      status: 502,
      detail: "Provider evidence did not match the reviewed public-read contract.",
    },
    evidence_unavailable: {
      type: "urn:gis-ai-go:problem:data-query-evidence-unavailable",
      title: "Data query evidence unavailable",
      status: 503,
      detail: "Verified evidence could not be completed for this data query.",
    },
  });

export interface DataQueryProblem {
  readonly schema: "gis-ai-go.data-query-problem.v1";
  readonly type: string;
  readonly title: string;
  readonly status: 400 | 403 | 408 | 429 | 502 | 503 | 504;
  readonly code: DataQueryProblemCode;
  readonly detail: string;
  readonly request_id: string;
  readonly trace_id: string;
  readonly instance?: string;
}

export interface DataQueryReconciliationProblem {
  readonly schema: "gis-ai-go.data-query-reconciliation-problem.v1";
  readonly type: string;
  readonly title: string;
  readonly status: 409;
  readonly code: DataQueryReconciliationProblemCode;
  readonly detail: string;
  readonly request_id: string;
  readonly trace_id: string;
  readonly instance?: string;
}

export type DataQueryOperationProblem =
  | DataQueryProblem
  | DataQueryReconciliationProblem;

/** A closed, receipt-free operational failure for the application-only seam. */
export class DataQueryApplicationError extends Error {
  public constructor(public readonly problem: DataQueryOperationProblem) {
    super(problem.title);
    this.name = "DataQueryApplicationError";
  }
}

export interface DataQueryParameters {
  readonly schema: "gis-ai-go.data-query-parameters.v1";
  readonly resource_id: typeof PUBLIC_READ_ONS_RESOURCE.resource_id;
  readonly dataset: {
    readonly id: "weekly-deaths-region";
    readonly edition: "time-series";
    readonly version: "121";
  };
  readonly selections: typeof PUBLIC_READ_ONS_RESOURCE.selections;
  readonly limit: 1;
}

export interface DataQueryRequest {
  readonly schema: "gis-ai-go.data-query-request.v1";
  readonly idempotency_key: string;
  readonly parameters: DataQueryParameters;
}

export const PUBLIC_ONS_DATA_QUERY_PARAMETERS: DataQueryParameters = canonicalJsonClone({
  schema: "gis-ai-go.data-query-parameters.v1",
  resource_id: PUBLIC_READ_ONS_RESOURCE.resource_id,
  dataset: {
    id: PUBLIC_READ_ONS_RESOURCE.dataset.id,
    edition: PUBLIC_READ_ONS_RESOURCE.dataset.edition,
    version: PUBLIC_READ_ONS_RESOURCE.dataset.version,
  },
  selections: PUBLIC_READ_ONS_RESOURCE.selections,
  limit: 1,
});

export interface DataQueryResultCore {
  readonly schema: "gis-ai-go.data-query-result.v1";
  readonly operation: "data.query";
  readonly request_id: string;
  readonly trace_id: string;
  readonly evidence_binding: ReturnType<typeof publicReadResultEvidenceBinding>;
  readonly data: {
    readonly status: "succeeded";
    readonly observations: readonly [{ readonly value: string; readonly unit: null }];
    readonly cache?: {
      readonly status: "approved-current";
      readonly cache_id: string;
      readonly source_uri: typeof ONS_OBSERVATION_URI;
      readonly provider_result_sha256: string;
      readonly retrieved_at: string;
      readonly stale_after: string;
      readonly checked_at: string;
    };
  };
  readonly warnings:
    | readonly []
    | readonly [typeof APPROVED_CACHE_WARNING];
}

export const APPROVED_CACHE_WARNING = PUBLIC_DATA_QUERY_APPROVED_CACHE_WARNING;

export interface DataQueryResult extends DataQueryResultCore {
  readonly evidence_receipt: PublicReadEvidenceReceipt;
  readonly evidence_storage?: PublicEvidenceStorageReference;
}

export interface DataQueryInvocationOptions {
  readonly signal?: AbortSignal;
  readonly deadline?: string;
}

/** Compile-time authority for captured pristine execution in the governed assembly. */
export const GOVERNED_PRISTINE_ONS_EXECUTION = Symbol(
  "gis-ai-go.governed-pristine-ons-execution",
);

export interface DataQueryApplicationOptions {
  /** Mandatory explicit injection; omission never constructs or activates an adapter. */
  readonly adapter: OnsDataApiAdapter;
  /**
   * Optional explicit exact-cache injection; omission preserves provider-only
   * fail-closed behaviour.
   */
  readonly approvedCache?: ApprovedOnsDataQueryCache;
  readonly software: EvidenceSoftwareIdentity;
  readonly now?: () => Date;
  readonly evidenceLedger?: PublicEvidenceLedger;
  readonly reconciliationIndex?: PublicEvidenceReconciliationIndex;
  readonly governedPristineExecution?: typeof GOVERNED_PRISTINE_ONS_EXECUTION;
}

export interface DataQueryApplication {
  readonly query: (
    request: unknown,
    context: CatalogueProblemContext,
    options?: DataQueryInvocationOptions,
  ) => Promise<DataQueryResult>;
}

interface DataQueryRuntime {
  readonly adapter: OnsDataApiAdapter;
  readonly approvedCache?: ApprovedOnsDataQueryCache;
  readonly software: EvidenceSoftwareIdentity;
  readonly now: () => Date;
  readonly evidenceLedger?: PublicEvidenceLedger;
  readonly reconciliationIndex?: PublicEvidenceReconciliationIndex;
  readonly governedPristineExecution: boolean;
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  if (
    value === null ||
    typeof value !== "object" ||
    Array.isArray(value) ||
    utilTypes.isProxy(value)
  ) {
    return false;
  }
  const prototype = Object.getPrototypeOf(value) as object | null;
  return prototype === Object.prototype || prototype === null;
}

function dataProperties(
  value: unknown,
  allowed: readonly string[],
  required: readonly string[],
  label: string,
): Readonly<Record<string, unknown>> {
  if (!isPlainObject(value)) throw new TypeError(`${label} must be a plain object`);
  let keys: readonly PropertyKey[];
  let descriptors: PropertyDescriptorMap;
  try {
    keys = Reflect.ownKeys(value);
    descriptors = Object.getOwnPropertyDescriptors(value);
  } catch {
    throw new TypeError(`${label} could not be inspected`);
  }
  if (
    keys.some((key) => typeof key !== "string") ||
    keys.some((key) => !allowed.includes(key as string)) ||
    required.some((key) => !Object.hasOwn(descriptors, key))
  ) {
    throw new TypeError(`${label} has an unexpected shape`);
  }
  for (const descriptor of Object.values(descriptors)) {
    if (!("value" in descriptor) || descriptor.enumerable !== true) {
      throw new TypeError(`${label} must use enumerable data properties`);
    }
  }
  return Object.freeze(
    Object.fromEntries(
      Object.entries(descriptors).map(([key, descriptor]) => [key, descriptor.value]),
    ),
  );
}

function applicationRuntime(options: DataQueryApplicationOptions): DataQueryRuntime {
  const values = dataProperties(
    options,
    [
      "adapter",
      "approvedCache",
      "evidenceLedger",
      "governedPristineExecution",
      "now",
      "reconciliationIndex",
      "software",
    ],
    ["adapter", "software"],
    "Data query application options",
  );
  let adapter: OnsDataApiAdapter;
  try {
    adapter = requireExactOnsDataApiAdapter(values.adapter);
  } catch {
    throw new TypeError("Data query application requires an explicitly injected ONS adapter");
  }
  if (
    values.approvedCache !== undefined &&
    !isExactApprovedOnsDataQueryCache(values.approvedCache)
  ) {
    throw new TypeError("Data query application approved cache is invalid");
  }
  if (
    values.governedPristineExecution !== undefined &&
    values.governedPristineExecution !== GOVERNED_PRISTINE_ONS_EXECUTION
  ) {
    throw new TypeError("Data query governed pristine execution authority is invalid");
  }
  const governedPristineExecution =
    values.governedPristineExecution === GOVERNED_PRISTINE_ONS_EXECUTION;
  const requiresPristineExecution =
    values.approvedCache !== undefined ||
    governedPristineExecution ||
    values.reconciliationIndex !== undefined;
  if (requiresPristineExecution) {
    try {
      requirePristineOnsDataApiAdapter(adapter);
    } catch {
      throw new TypeError(
        "Data query application pristine execution requires an unmodified ONS adapter",
      );
    }
  }
  let software: EvidenceSoftwareIdentity;
  try {
    software = canonicalJsonClone(values.software) as EvidenceSoftwareIdentity;
  } catch {
    throw new TypeError("Data query application software identity is invalid");
  }
  if (
    !isPlainObject(software) ||
    Object.keys(software).sort().join(",") !== "name,revision,version" ||
    software.name !== "gis-ai-go-mcp-gateway" ||
    !SEMVER.test(software.version) ||
    !SHA40.test(software.revision)
  ) {
    throw new TypeError("Data query application software identity is invalid");
  }
  if (values.now !== undefined && typeof values.now !== "function") {
    throw new TypeError("Data query application now option must be a function");
  }
  if (
    values.evidenceLedger !== undefined &&
    (!(values.evidenceLedger instanceof PublicEvidenceLedger) ||
      utilTypes.isProxy(values.evidenceLedger))
  ) {
    throw new TypeError("Data query application evidence ledger is invalid");
  }
  const evidenceLedger = values.evidenceLedger as PublicEvidenceLedger | undefined;
  if (
    values.reconciliationIndex !== undefined &&
    (!(values.reconciliationIndex instanceof PublicEvidenceReconciliationIndex) ||
      utilTypes.isProxy(values.reconciliationIndex))
  ) {
    throw new TypeError("Data query application reconciliation index is invalid");
  }
  const reconciliationIndex = values.reconciliationIndex as
    | PublicEvidenceReconciliationIndex
    | undefined;
  if (
    reconciliationIndex !== undefined &&
    (evidenceLedger === undefined || reconciliationIndex.ledger !== evidenceLedger)
  ) {
    throw new TypeError(
      "Data query reconciliation requires the exact explicitly linked evidence ledger",
    );
  }
  evidenceLedger?.verify();
  reconciliationIndex?.verify();
  return Object.freeze({
    adapter,
    ...(values.approvedCache === undefined
      ? {}
      : { approvedCache: values.approvedCache as ApprovedOnsDataQueryCache }),
    software,
    now: (values.now as (() => Date) | undefined) ?? (() => new Date()),
    ...(evidenceLedger === undefined ? {} : { evidenceLedger }),
    ...(reconciliationIndex === undefined ? {} : { reconciliationIndex }),
    governedPristineExecution,
  });
}

function createDataQueryProblem(
  code: DataQueryProblemCode,
  context: CatalogueProblemContext,
): DataQueryProblem {
  const definition = PROBLEM_DEFINITIONS[code];
  return canonicalJsonClone({
    schema: "gis-ai-go.data-query-problem.v1",
    ...definition,
    code,
    request_id: context.requestId,
    trace_id: context.traceId,
    ...(context.instance === undefined ? {} : { instance: context.instance }),
  });
}

function fail(code: DataQueryProblemCode, context: CatalogueProblemContext): never {
  throw new DataQueryApplicationError(createDataQueryProblem(code, context));
}

function assertApprovedCacheAdapter(
  runtime: DataQueryRuntime,
  context: CatalogueProblemContext,
): void {
  if (runtime.approvedCache !== undefined || runtime.governedPristineExecution) {
    try {
      requirePristineOnsDataApiAdapter(runtime.adapter);
    } catch {
      fail("provider_contract_failed", context);
    }
  }
}

function reconciliationProblem(
  code: DataQueryReconciliationProblemCode,
  context: CatalogueProblemContext,
): DataQueryReconciliationProblem {
  const definitions = {
    idempotency_pending: {
      type: "urn:gis-ai-go:problem:data-query-idempotency-pending",
      title: "Data query reconciliation pending",
      detail: "This idempotency key is already owned by an unfinished data query.",
    },
    idempotency_completed: {
      type: "urn:gis-ai-go:problem:data-query-idempotency-completed",
      title: "Data query already completed",
      detail: "This idempotency key completed previously; inspect its durable evidence.",
    },
    idempotency_conflict: {
      type: "urn:gis-ai-go:problem:data-query-idempotency-conflict",
      title: "Data query idempotency conflict",
      detail: "This idempotency key is bound to a different semantic request.",
    },
  } as const;
  return canonicalJsonClone({
    schema: "gis-ai-go.data-query-reconciliation-problem.v1",
    ...definitions[code],
    status: 409,
    code,
    request_id: context.requestId,
    trace_id: context.traceId,
    ...(context.instance === undefined ? {} : { instance: context.instance }),
  });
}

function failReconciliation(
  code: DataQueryReconciliationProblemCode,
  context: CatalogueProblemContext,
): never {
  throw new DataQueryApplicationError(reconciliationProblem(code, context));
}

interface NormalisedDataQueryRequest {
  readonly parameters: DataQueryParameters;
  readonly idempotencyKey?: string;
}

function normaliseRequest(
  runtime: DataQueryRuntime,
  request: unknown,
  context: CatalogueProblemContext,
): NormalisedDataQueryRequest {
  let snapshot: unknown;
  try {
    snapshot = canonicalJsonClone(request);
  } catch {
    return fail("invalid_request", context);
  }
  if (runtime.reconciliationIndex === undefined) {
    if (canonicalJson(snapshot) !== canonicalJson(PUBLIC_ONS_DATA_QUERY_PARAMETERS)) {
      return fail("invalid_request", context);
    }
    return Object.freeze({ parameters: snapshot as DataQueryParameters });
  }
  if (!isPlainObject(snapshot)) return fail("invalid_request", context);
  const record = snapshot;
  if (
    Object.keys(record).sort().join(",") !== "idempotency_key,parameters,schema" ||
    record.schema !== "gis-ai-go.data-query-request.v1" ||
    typeof record.idempotency_key !== "string" ||
    !/^gis-ai-go:ik:v1:[0-9a-f]{64}$/u.test(record.idempotency_key) ||
    record.idempotency_key === `gis-ai-go:ik:v1:${"0".repeat(64)}` ||
    canonicalJson(record.parameters) !== canonicalJson(PUBLIC_ONS_DATA_QUERY_PARAMETERS)
  ) {
    return fail("invalid_request", context);
  }
  return Object.freeze({
    parameters: record.parameters as DataQueryParameters,
    idempotencyKey: record.idempotency_key,
  });
}

function validDeadline(value: string): boolean {
  if (value.length > 64) return false;
  const match = DEADLINE.exec(value);
  if (match === null) return false;
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const hour = Number(match[4]);
  const minute = Number(match[5]);
  const second = Number(match[6]);
  const offsetHour = match[8] === undefined ? 0 : Number(match[8]);
  const offsetMinute = match[9] === undefined ? 0 : Number(match[9]);
  const leapYear = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const monthDays = [31, leapYear ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  return (
    year >= 1 &&
    month >= 1 &&
    month <= 12 &&
    day >= 1 &&
    day <= monthDays[month - 1]! &&
    hour <= 23 &&
    minute <= 59 &&
    second <= 59 &&
    offsetHour <= 23 &&
    offsetMinute <= 59 &&
    Number.isFinite(Date.parse(value))
  );
}

function invocationOptions(
  options: DataQueryInvocationOptions | undefined,
  context: CatalogueProblemContext,
): DataQueryInvocationOptions {
  if (options === undefined) return Object.freeze({});
  let values: Readonly<Record<string, unknown>>;
  try {
    values = dataProperties(options, ["deadline", "signal"], [], "Data query invocation options");
  } catch {
    return fail("invalid_request", context);
  }
  if (
    values.signal !== undefined &&
    (!(values.signal instanceof AbortSignal) || utilTypes.isProxy(values.signal))
  ) {
    return fail("invalid_request", context);
  }
  if (
    values.deadline !== undefined &&
    (typeof values.deadline !== "string" || !validDeadline(values.deadline))
  ) {
    return fail("invalid_request", context);
  }
  return Object.freeze({
    ...(values.signal === undefined ? {} : { signal: values.signal as AbortSignal }),
    ...(values.deadline === undefined ? {} : { deadline: values.deadline as string }),
  });
}

function providerInvocationOptions(
  invocation: DataQueryInvocationOptions,
  context: CatalogueProblemContext,
): ProviderAdapterExecutionOptions {
  const candidate = context.trace ?? {
    traceparent: `00-${context.traceId}-${randomBytes(8).toString("hex")}-02`,
  };
  let trace: ReturnType<typeof normaliseW3CTraceContext>;
  try {
    trace = normaliseW3CTraceContext(candidate, context.traceId);
  } catch {
    return fail("invalid_request", context);
  }
  return Object.freeze({ ...invocation, trace });
}

function trustedNowMilliseconds(
  runtime: DataQueryRuntime,
  context: CatalogueProblemContext,
): number {
  let current: unknown;
  try {
    current = runtime.now();
  } catch {
    return fail("evidence_unavailable", context);
  }
  if (!(current instanceof Date) || utilTypes.isProxy(current)) {
    return fail("evidence_unavailable", context);
  }
  let milliseconds: number;
  try {
    milliseconds = Date.prototype.getTime.call(current);
  } catch {
    return fail("evidence_unavailable", context);
  }
  if (!Number.isFinite(milliseconds)) return fail("evidence_unavailable", context);
  return milliseconds;
}

function signalIsAborted(
  signal: AbortSignal,
  context: CatalogueProblemContext,
): boolean {
  try {
    return Reflect.get(AbortSignal.prototype, "aborted", signal) === true;
  } catch {
    return fail("invalid_request", context);
  }
}

function assertInvocationControls(
  runtime: DataQueryRuntime,
  invocation: DataQueryInvocationOptions,
  context: CatalogueProblemContext,
): void {
  if (invocation.signal !== undefined && signalIsAborted(invocation.signal, context)) {
    fail("query_cancelled", context);
  }
  if (
    invocation.deadline !== undefined &&
    trustedNowMilliseconds(runtime, context) >= Date.parse(invocation.deadline)
  ) {
    fail("query_deadline_exceeded", context);
  }
}

function sameCanonical(left: unknown, right: unknown): boolean {
  try {
    return canonicalJson(left) === canonicalJson(right);
  } catch {
    return false;
  }
}

function expectedRights(): ProviderRights {
  const rights = PUBLIC_READ_ONS_RESOURCE.rights;
  return canonicalJsonClone({
    state: rights.state,
    licence: rights.licence,
    licenceUri: rights.licence_uri,
    attribution: rights.attribution,
    obligations: rights.obligations,
    exceptions: rights.exceptions,
    evidenceUris: rights.evidence_uris,
    reviewedAt: rights.reviewed_at,
  });
}

function expectedProvenance(): ProviderAdapterProvenance {
  const resource = PUBLIC_READ_ONS_RESOURCE;
  return canonicalJsonClone({
    providerVersion: {
      providerId: resource.provider.id,
      datasetId: resource.dataset.id,
      edition: resource.dataset.edition,
      version: resource.dataset.version,
      versionUri: resource.dataset.version_uri,
      sourceDate: resource.dataset.source_date,
      dimensionOrder: resource.dataset.dimension_order,
    },
    adapter: {
      id: resource.provider.adapter_id,
      version: resource.provider.adapter_version,
    },
    transformations: [
      "ons-cmd-single-observation.v1",
      "provider-native-identifiers-preserved.v1",
      "untrusted-provider-links-validated-and-omitted.v1",
      "rfc8785-canonical-json.v1",
    ],
    synthetic: false,
    sourceUri: ONS_OBSERVATION_URI,
  });
}

function expectedEstimate(): ProviderAdapterEstimate {
  const limits = PUBLIC_READ_ONS_RESOURCE.limits;
  return canonicalJsonClone({
    confidence: "upper-bound",
    maxObservations: limits.max_observations,
    maxAttempts: limits.max_attempts,
    maxCompressedResponseBytes: limits.max_compressed_response_bytes,
    maxDecompressedResponseBytes: limits.max_decompressed_response_bytes,
    maxCanonicalResponseBytes: limits.max_canonical_response_bytes,
  });
}

function mapAdapterCode(code: AdapterErrorCode): DataQueryProblemCode {
  switch (code) {
    case "ADAPTER_INVOCATION_SUSPENDED":
      return "provider_suspended";
    case "PROVIDER_RATE_LIMITED":
      return "provider_rate_limited";
    case "PROVIDER_TIMEOUT":
      return "provider_timeout";
    case "PROVIDER_OUTAGE":
      return "provider_unavailable";
    case "ADAPTER_DISCOVERY_SUSPENDED":
    case "INCOMPATIBLE_OPERATION":
    case "INVALID_REQUEST":
    case "MALFORMED_PROVIDER_RESPONSE":
    case "RIGHTS_UNKNOWN":
    case "STALE_PROVIDER_VERSION":
      return "provider_contract_failed";
  }
}

function failAdapter(
  adapter: OnsDataApiAdapter,
  error: unknown,
  context: CatalogueProblemContext,
): never {
  return fail(mapAdapterCode(trustedAdapterError(adapter, error, context).code), context);
}

function trustedAdapterError(
  adapter: OnsDataApiAdapter,
  error: unknown,
  context: CatalogueProblemContext,
  requirePristine = false,
): NormalisedAdapterError {
  const trusted = normaliseAdapterError(error);
  let candidateValue: unknown;
  try {
    candidateValue = canonicalJsonClone(
      requirePristine
        ? normalisePristineOnsDataApiAdapterError(adapter, error)
        : adapter.normalise_error(error),
    );
  } catch {
    return fail("provider_contract_failed", context);
  }
  if (
    !isPlainObject(candidateValue) ||
    Object.keys(candidateValue).sort().join(",") !==
      "code,message,providerStatus,retryable"
  ) {
    return fail("provider_contract_failed", context);
  }
  const candidate = candidateValue as unknown as NormalisedAdapterError;
  if (
    !(ADAPTER_ERROR_CODES as readonly string[]).includes(candidate.code) ||
    !sameCanonical(candidate, trusted)
  ) {
    return fail("provider_contract_failed", context);
  }
  return trusted;
}

function assertHealth(
  health: unknown,
  context: CatalogueProblemContext,
): void {
  if (!isPlainObject(health)) fail("provider_contract_failed", context);
  const keys = Object.keys(health).sort();
  if (
    keys.join(",") !== "adapterId,discovery,invocation,network" ||
    health.adapterId !== ONS_ADAPTER_ID ||
    (health.discovery !== "active" && health.discovery !== "suspended") ||
    (health.invocation !== "active" && health.invocation !== "suspended") ||
    health.network !== "not-checked"
  ) {
    fail("provider_contract_failed", context);
  }
  if (health.invocation !== "active") fail("provider_suspended", context);
}

function adapterEvidence<T>(
  adapter: OnsDataApiAdapter,
  read: () => unknown,
  context: CatalogueProblemContext,
): T {
  let value: unknown;
  try {
    value = read();
  } catch (error) {
    return failAdapter(adapter, error, context);
  }
  try {
    return canonicalJsonClone(value) as T;
  } catch {
    return fail("provider_contract_failed", context);
  }
}

function preflightAdapter(
  adapter: OnsDataApiAdapter,
  context: CatalogueProblemContext,
): { readonly rights: ProviderRights; readonly provenance: ProviderAdapterProvenance } {
  const health = adapterEvidence<AdapterHealth>(adapter, () => adapter.health(), context);
  assertHealth(health, context);
  const estimate = adapterEvidence<ProviderAdapterEstimate>(
    adapter,
    () => adapter.estimate(ONS_ADAPTER_REQUEST),
    context,
  );
  const rights = adapterEvidence<ProviderRights>(
    adapter,
    () => adapter.licence_evidence(),
    context,
  );
  const provenance = adapterEvidence<ProviderAdapterProvenance>(
    adapter,
    () => adapter.provenance(),
    context,
  );
  if (
    !sameCanonical(estimate, expectedEstimate()) ||
    !sameCanonical(rights, expectedRights()) ||
    !sameCanonical(provenance, expectedProvenance())
  ) {
    fail("provider_contract_failed", context);
  }
  return Object.freeze({ rights, provenance });
}

function validateAdapterResult(
  value: unknown,
  checked: { readonly rights: ProviderRights; readonly provenance: ProviderAdapterProvenance },
  context: CatalogueProblemContext,
): ProviderAdapterResult {
  let result: ProviderAdapterResult;
  try {
    result = canonicalJsonClone(value) as ProviderAdapterResult;
  } catch {
    return fail("provider_contract_failed", context);
  }
  if (
    new TextEncoder().encode(canonicalJson(result)).byteLength >
    PUBLIC_READ_ONS_RESOURCE.limits.max_canonical_response_bytes
  ) {
    return fail("provider_contract_failed", context);
  }
  if (
    !isPlainObject(result) ||
    !Array.isArray(result.observations) ||
    result.observations.length !== 1 ||
    !isPlainObject(result.observations[0])
  ) {
    return fail("provider_contract_failed", context);
  }
  const observation = result.observations[0];
  const observationValue = observation?.value;
  if (
    observation === undefined ||
    Object.keys(observation).sort().join(",") !== "metadata,unit,value" ||
    typeof observationValue !== "string" ||
    !NUMERIC_OBSERVATION.test(observationValue) ||
    observation.unit !== null
  ) {
    return fail("provider_contract_failed", context);
  }
  const expected: ProviderAdapterResult = canonicalJsonClone({
    schema: "gis-ai-go.provider-adapter-result.v1",
    provider: {
      id: PUBLIC_READ_ONS_RESOURCE.provider.id,
      adapterId: PUBLIC_READ_ONS_RESOURCE.provider.adapter_id,
    },
    dataset: {
      id: PUBLIC_READ_ONS_RESOURCE.dataset.id,
      edition: PUBLIC_READ_ONS_RESOURCE.dataset.edition,
      version: PUBLIC_READ_ONS_RESOURCE.dataset.version,
      versionUri: PUBLIC_READ_ONS_RESOURCE.dataset.version_uri,
    },
    dimensions: PUBLIC_READ_ONS_RESOURCE.selections,
    observations: [
      {
        value: observationValue,
        unit: null,
        metadata: [{ name: "Data Marking", value: "" }],
      },
    ],
    rights: checked.rights,
    provenance: checked.provenance,
  });
  if (!sameCanonical(result, expected)) return fail("provider_contract_failed", context);
  return result;
}

function cachedAdapterResult(
  hit: ApprovedOnsDataQueryCacheHit,
  checked: { readonly rights: ProviderRights; readonly provenance: ProviderAdapterProvenance },
  context: CatalogueProblemContext,
): ProviderAdapterResult {
  const candidate: ProviderAdapterResult = canonicalJsonClone({
    schema: "gis-ai-go.provider-adapter-result.v1",
    provider: {
      id: PUBLIC_READ_ONS_RESOURCE.provider.id,
      adapterId: PUBLIC_READ_ONS_RESOURCE.provider.adapter_id,
    },
    dataset: {
      id: PUBLIC_READ_ONS_RESOURCE.dataset.id,
      edition: PUBLIC_READ_ONS_RESOURCE.dataset.edition,
      version: PUBLIC_READ_ONS_RESOURCE.dataset.version,
      versionUri: PUBLIC_READ_ONS_RESOURCE.dataset.version_uri,
    },
    dimensions: PUBLIC_READ_ONS_RESOURCE.selections,
    observations: [hit.observation],
    rights: checked.rights,
    provenance: checked.provenance,
  });
  if (
    domainSeparatedSha256(CANONICAL_DOMAINS.providerAdapterResult, candidate) !==
    hit.provider_result_sha256
  ) {
    return fail("provider_contract_failed", context);
  }
  return candidate;
}

function receiptTimestamp(runtime: DataQueryRuntime, context: CatalogueProblemContext): string {
  return new Date(trustedNowMilliseconds(runtime, context)).toISOString();
}

async function query(
  runtime: DataQueryRuntime,
  requestValue: unknown,
  context: CatalogueProblemContext,
  invocationValue: DataQueryInvocationOptions | undefined,
): Promise<DataQueryResult> {
  assertCatalogueProblemContext(context);
  assertApprovedCacheAdapter(runtime, context);
  const request = normaliseRequest(runtime, requestValue, context);
  const invocation = invocationOptions(invocationValue, context);
  const providerInvocation = providerInvocationOptions(invocation, context);
  assertInvocationControls(runtime, invocation, context);
  const normalisedParametersSha256 = domainSeparatedSha256(
    CANONICAL_DOMAINS.dataQueryParameters,
    request.parameters,
  );
  const expectedReconciliationFingerprint = evidenceReconciliationRequestFingerprint({
    operation: "data.query",
    resourceId: PUBLIC_READ_ONS_RESOURCE.resource_id,
    normalisedParametersSha256,
  });

  if (runtime.reconciliationIndex !== undefined) {
    let existing: ReturnType<PublicEvidenceReconciliationIndex["lookup"]>;
    try {
      existing = runtime.reconciliationIndex.lookup(request.idempotencyKey!);
    } catch {
      return fail("evidence_unavailable", context);
    }
    if (
      existing.status !== "not-found" &&
      existing.claim !== undefined &&
      existing.claim.request_fingerprint_sha256 !== expectedReconciliationFingerprint
    ) {
      return failReconciliation("idempotency_conflict", context);
    }
    if (existing.status === "pending") {
      return failReconciliation("idempotency_pending", context);
    }
    if (existing.status === "completed") {
      return failReconciliation("idempotency_completed", context);
    }
  }

  let policyEvaluation: ReturnType<typeof evaluatePublicReadPolicy>;
  try {
    policyEvaluation = evaluatePublicReadPolicy({
      requestId: context.requestId,
      traceId: context.traceId,
      operation: "data.query",
      resource: PUBLIC_READ_ONS_RESOURCE,
    });
  } catch {
    return fail("policy_denied", context);
  }
  if (
    !isAllowedPublicReadOperation(policyEvaluation, "data.query") ||
    !verifyPublicReadAuthorityContext(policyEvaluation.authorityContext) ||
    !verifyPublicReadPolicy(policyEvaluation.policy) ||
    !verifyPublicReadPolicyDecision(policyEvaluation.decision) ||
    !verifyPublicReadResource(PUBLIC_READ_ONS_RESOURCE)
  ) {
    return fail("policy_denied", context);
  }

  assertInvocationControls(runtime, invocation, context);
  assertApprovedCacheAdapter(runtime, context);
  const checked = preflightAdapter(runtime.adapter, context);
  assertApprovedCacheAdapter(runtime, context);
  assertInvocationControls(runtime, invocation, context);
  const usesPristineExecution =
    runtime.reconciliationIndex !== undefined ||
    runtime.approvedCache !== undefined ||
    runtime.governedPristineExecution;
  let providerAdmission: OnsDataApiAdapterAdmissionLease | undefined;
  if (usesPristineExecution) {
    try {
      providerAdmission = reservePristineOnsDataApiAdapterExecution(
        runtime.adapter,
        ONS_ADAPTER_REQUEST,
        providerInvocation,
      );
    } catch (error) {
      const adapterError = trustedAdapterError(runtime.adapter, error, context, true);
      return fail(mapAdapterCode(adapterError.code), context);
    }
  }
  const releaseProviderAdmission = (): void => {
    providerAdmission?.release();
    providerAdmission = undefined;
  };
  let reconciliationClaim:
    | Extract<
        ReturnType<PublicEvidenceReconciliationIndex["claim"]>,
        { readonly status: "claimed" }
      >["claim"]
    | undefined;
  if (runtime.reconciliationIndex !== undefined) {
    try {
      const outcome = runtime.reconciliationIndex.claim({
        idempotencyKey: request.idempotencyKey!,
        operation: "data.query",
        requestId: context.requestId,
        traceId: context.traceId,
        resourceId: PUBLIC_READ_ONS_RESOURCE.resource_id,
        normalisedParametersSha256,
      });
      if (outcome.status === "pending") {
        releaseProviderAdmission();
        return failReconciliation("idempotency_pending", context);
      }
      if (outcome.status === "completed") {
        releaseProviderAdmission();
        return failReconciliation("idempotency_completed", context);
      }
      reconciliationClaim = outcome.claim;
    } catch (error) {
      releaseProviderAdmission();
      if (
        error instanceof EvidenceReconciliationIndexError &&
        error.code === "conflict"
      ) {
        return failReconciliation("idempotency_conflict", context);
      }
      if (error instanceof DataQueryApplicationError) throw error;
      return fail("evidence_unavailable", context);
    }
  }
  let adapterResult: ProviderAdapterResult;
  let cacheHit: ApprovedOnsDataQueryCacheHit | undefined;
  let cacheCheckedAt: string | undefined;
  let approvedCacheExecution: OnsDataApiAdapterExecution | undefined;
  try {
    assertInvocationControls(runtime, invocation, context);
    assertApprovedCacheAdapter(runtime, context);
    if (usesPristineExecution) {
      if (providerAdmission === undefined) {
        return fail("provider_contract_failed", context);
      }
      approvedCacheExecution = providerAdmission.start();
      providerAdmission = undefined;
    }
  } catch (error) {
    releaseProviderAdmission();
    if (error instanceof DataQueryApplicationError) throw error;
    return fail("provider_contract_failed", context);
  }
  try {
    adapterResult = await (
      approvedCacheExecution?.result ??
      runtime.adapter.execute(ONS_ADAPTER_REQUEST, providerInvocation)
    );
    assertApprovedCacheAdapter(runtime, context);
  } catch (error) {
    assertInvocationControls(runtime, invocation, context);
    assertApprovedCacheAdapter(runtime, context);
    const adapterError = trustedAdapterError(
      runtime.adapter,
      error,
      context,
      runtime.approvedCache !== undefined || runtime.governedPristineExecution,
    );
    const approvedOutage =
      approvedCacheExecution?.approvedCacheOutage(error, adapterError) ?? null;
    if (approvedOutage === null || runtime.approvedCache === undefined) {
      return fail(mapAdapterCode(adapterError.code), context);
    }
    cacheCheckedAt = new Date(trustedNowMilliseconds(runtime, context)).toISOString();
    assertApprovedCacheAdapter(runtime, context);
    try {
      cacheHit = runtime.approvedCache.read(ONS_ADAPTER_REQUEST, {
        checked_at: cacheCheckedAt,
        policy_id: policyEvaluation.decision.policy_id,
        policy_effect: policyEvaluation.decision.effect,
        operation: policyEvaluation.decision.operation,
        resource_id: policyEvaluation.decision.resource_id,
        provider_failure: adapterError.code,
        provider_outage_source: approvedOutage.source,
        provider_status: approvedOutage.providerStatus,
      }) ?? undefined;
    } catch {
      return fail("provider_contract_failed", context);
    }
    if (cacheHit === undefined) return fail("provider_unavailable", context);
    adapterResult = cachedAdapterResult(cacheHit, checked, context);
  }
  assertInvocationControls(runtime, invocation, context);
  const result = validateAdapterResult(adapterResult, checked, context);
  const resultCore: DataQueryResultCore = canonicalJsonClone({
    schema: "gis-ai-go.data-query-result.v1",
    operation: "data.query",
    request_id: context.requestId,
    trace_id: context.traceId,
    evidence_binding: publicReadResultEvidenceBinding(PUBLIC_READ_ONS_RESOURCE),
    data: {
      status: "succeeded",
      observations: [{ value: result.observations[0]!.value, unit: null }],
      ...(cacheHit === undefined
        ? {}
        : {
            cache: {
              status: "approved-current",
              cache_id: cacheHit.cache_id,
              source_uri: cacheHit.source_uri,
              provider_result_sha256: cacheHit.provider_result_sha256,
              retrieved_at: cacheHit.freshness.retrieved_at,
              stale_after: cacheHit.freshness.stale_after,
              checked_at: cacheHit.freshness.checked_at,
            },
          }),
    },
    warnings: cacheHit === undefined ? [] : [APPROVED_CACHE_WARNING],
  });

  const verificationMaterial = {
    normalisedParameters: request.parameters,
    resultCore,
    publicPolicy: policyEvaluation.policy,
    expectedAuthorityContext: policyEvaluation.authorityContext,
    expectedPolicyDecision: policyEvaluation.decision,
    expectedResource: PUBLIC_READ_ONS_RESOURCE,
    expectedSoftware: runtime.software,
  } as const;
  let receipt: PublicReadEvidenceReceipt;
  let evidenceStorage: PublicEvidenceStorageReference | undefined;
  try {
    receipt = buildPublicReadReceipt({
      createdAt: cacheCheckedAt ?? receiptTimestamp(runtime, context),
      requestId: context.requestId,
      traceId: context.traceId,
      operation: "data.query",
      normalisedParameters: request.parameters,
      authorityContext: policyEvaluation.authorityContext,
      publicPolicy: policyEvaluation.policy,
      policyDecision: policyEvaluation.decision,
      resource: PUBLIC_READ_ONS_RESOURCE,
      transformations: [
        { name: "normalise-public-read-parameters", version: "v1" },
        {
          name:
            cacheHit === undefined
              ? "execute-fixed-provider-query"
              : "read-approved-provider-cache",
          version: "v1",
        },
        { name: "project-public-read-result-core", version: "v1" },
      ],
      software: runtime.software,
      resultCore,
    });
    const verification = verifyPublicReadReceipt(receipt, verificationMaterial);
    if (!verification.valid) return fail("evidence_unavailable", context);
    if (
      runtime.reconciliationIndex !== undefined &&
      runtime.evidenceLedger !== undefined &&
      reconciliationClaim !== undefined
    ) {
      const resolution = runtime.reconciliationIndex.resolve(
        reconciliationClaim,
        receipt,
      );
      const persisted = runtime.evidenceLedger.persistReceipt(
        receipt,
        verificationMaterial,
      );
      const completed = runtime.reconciliationIndex.lookup(request.idempotencyKey!);
      if (
        completed.status !== "completed" ||
        completed.resolution.resolution_id !== resolution.resolution_id ||
        completed.resolution.receipt_id !== receipt.receipt_id ||
        canonicalJson(completed.stored) !== canonicalJson(persisted)
      ) {
        return fail("evidence_unavailable", context);
      }
      evidenceStorage = completed.stored.reference;
    } else {
      evidenceStorage = runtime.evidenceLedger?.persistReceipt(
        receipt,
        verificationMaterial,
      ).reference;
    }
  } catch (error) {
    if (error instanceof DataQueryApplicationError) throw error;
    return fail("evidence_unavailable", context);
  }

  return canonicalJsonClone({
    ...resultCore,
    evidence_receipt: receipt,
    ...(evidenceStorage === undefined ? {} : { evidence_storage: evidenceStorage }),
  });
}

/**
 * Create the inactive transport-neutral data.query application.
 *
 * It has no default adapter and no environment activation seam. Discovery state
 * is deliberately ignored: only an explicitly injected, invocation-active ONS
 * adapter can execute the fixed reviewed request.
 */
export function createDataQueryApplication(
  options: DataQueryApplicationOptions,
): DataQueryApplication {
  const runtime = applicationRuntime(options);
  const application = Object.freeze({
    query: (
      request: unknown,
      context: CatalogueProblemContext,
      invocation?: DataQueryInvocationOptions,
    ) => query(runtime, request, context, invocation),
  });
  if (runtime.reconciliationIndex !== undefined) {
    registerReconciledDataQueryApplication(application, runtime.reconciliationIndex);
  }
  return application;
}

/** True only for instances closed over an explicitly linked ledger and index. */
export function isReconciledDataQueryApplication(
  application: DataQueryApplication,
): boolean {
  return hasReconciledDataQueryApplication(application);
}
