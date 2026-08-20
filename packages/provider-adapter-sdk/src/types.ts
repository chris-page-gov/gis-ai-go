export const ADAPTER_OPERATIONS = Object.freeze([
  "describe",
  "health",
  "estimate",
  "execute",
  "normalise_error",
  "licence_evidence",
  "provenance",
] as const);

export type AdapterOperation = (typeof ADAPTER_OPERATIONS)[number];
export type AdapterPlaneState = "active" | "suspended";

export interface AdapterLifecycle {
  readonly discovery: AdapterPlaneState;
  readonly invocation: AdapterPlaneState;
  readonly reason: string;
}

export interface ProviderVersionIdentity {
  readonly providerId: string;
  readonly datasetId: string;
  readonly edition: string;
  readonly version: string;
  readonly versionUri: string;
  readonly sourceDate: string;
  readonly dimensionOrder: readonly string[];
}

export interface ProviderRights {
  readonly state: "open-with-conditions" | "project-synthetic" | "unknown";
  readonly licence: string;
  readonly licenceUri: string;
  readonly attribution: string;
  readonly obligations: readonly string[];
  readonly exceptions: readonly string[];
  readonly evidenceUris: readonly string[];
  readonly reviewedAt: string;
}

export interface NoEgressPolicy {
  readonly mode: "none";
  readonly reason: string;
}

export interface FixedEgressPolicy {
  readonly mode: "fixed";
  readonly origin: string;
  readonly method: "GET";
  readonly routes: readonly {
    readonly path: string;
    readonly queryParameters: readonly {
      readonly name: string;
      readonly value: string;
    }[];
    /** Exact query bytes after `?`; empty means that no `?` may be present. */
    readonly canonicalRawQuery: string;
  }[];
  readonly allowCallerUrl: false;
  readonly allowCredentials: false;
  readonly maxRedirects: 0;
  readonly connectTimeoutMs: number;
  readonly responseTimeoutMs: number;
  readonly maxCompressedBytes: number;
  readonly maxDecompressedBytes: number;
  readonly maxAttempts: number;
  readonly retryableStatuses: readonly number[];
  readonly maxRetryAfterSeconds: number;
}

export type AdapterEgressPolicy = NoEgressPolicy | FixedEgressPolicy;

export interface AdapterDescription {
  readonly adapterId: string;
  readonly adapterVersion: string;
  readonly name: string;
  readonly operations: readonly AdapterOperation[];
  readonly lifecycle: AdapterLifecycle;
  readonly providerVersion: ProviderVersionIdentity;
  readonly egress: AdapterEgressPolicy;
}

export interface AdapterHealth {
  readonly adapterId: string;
  readonly discovery: AdapterPlaneState;
  readonly invocation: AdapterPlaneState;
  readonly network: "not-used" | "not-checked";
}

export interface ProviderSelection {
  readonly dimension: string;
  readonly option: string;
}

/** Internal adapter query only; this is not the EXEC-202 service envelope. */
export interface ProviderAdapterQuery {
  readonly dataset: {
    readonly id: string;
    readonly edition: string;
    readonly version: string;
  };
  readonly selections: readonly ProviderSelection[];
}

export interface ExactProviderAdapterEstimate {
  readonly observations: number;
  readonly canonicalResponseBytes: number;
  readonly confidence: "exact";
}

export interface UpperBoundProviderAdapterEstimate {
  readonly confidence: "upper-bound";
  readonly maxObservations: number;
  readonly maxAttempts: number;
  readonly maxCompressedResponseBytes: number;
  readonly maxDecompressedResponseBytes: number;
  readonly maxCanonicalResponseBytes: number;
}

export type ProviderAdapterEstimate =
  | ExactProviderAdapterEstimate
  | UpperBoundProviderAdapterEstimate;

export interface ProviderAdapterProvenance {
  readonly providerVersion: ProviderVersionIdentity;
  readonly adapter: {
    readonly id: string;
    readonly version: string;
  };
  readonly transformations: readonly string[];
  readonly synthetic: boolean;
  /** Exact internally constructed source URI; provider-returned links are never trusted. */
  readonly sourceUri?: string;
}

export interface ProviderAdapterResult {
  readonly schema: "gis-ai-go.provider-adapter-result.v1";
  readonly provider: {
    readonly id: string;
    readonly adapterId: string;
  };
  readonly dataset: {
    readonly id: string;
    readonly edition: string;
    readonly version: string;
    readonly versionUri: string;
  };
  readonly dimensions: readonly ProviderSelection[];
  readonly observations: readonly {
    readonly value: string;
    /** `null` preserves an upstream response that supplies no unit. */
    readonly unit: string | null;
    readonly metadata?: readonly {
      readonly name: string;
      readonly value: string;
    }[];
  }[];
  readonly rights: ProviderRights;
  readonly provenance: ProviderAdapterProvenance;
}

export const ADAPTER_ERROR_CODES = Object.freeze([
  "ADAPTER_DISCOVERY_SUSPENDED",
  "ADAPTER_INVOCATION_SUSPENDED",
  "INCOMPATIBLE_OPERATION",
  "INVALID_REQUEST",
  "MALFORMED_PROVIDER_RESPONSE",
  "PROVIDER_OUTAGE",
  "PROVIDER_RATE_LIMITED",
  "PROVIDER_TIMEOUT",
  "RIGHTS_UNKNOWN",
  "STALE_PROVIDER_VERSION",
] as const);

export type AdapterErrorCode = (typeof ADAPTER_ERROR_CODES)[number];

export interface NormalisedAdapterError {
  readonly code: AdapterErrorCode;
  readonly message: string;
  readonly retryable: boolean;
  readonly providerStatus: number | null;
}

export interface ProviderAdapter {
  readonly operations: readonly AdapterOperation[];
  describe(): AdapterDescription;
  health(): AdapterHealth;
  estimate(request: unknown): ProviderAdapterEstimate;
  execute(request: unknown): ProviderAdapterResult;
  normalise_error(error: unknown): NormalisedAdapterError;
  licence_evidence(): ProviderRights;
  provenance(): ProviderAdapterProvenance;
}

export interface ProviderAdapterExecutionOptions {
  readonly signal?: AbortSignal;
  /** Accepted EXEC-202 absolute RFC 3339 deadline; the adapter also applies its lower local ceiling. */
  readonly deadline?: string;
}

/** Live adapters have the same seven operations but execute asynchronously. */
export interface AsyncProviderAdapter {
  readonly operations: readonly AdapterOperation[];
  describe(): AdapterDescription;
  health(): AdapterHealth;
  estimate(request: unknown): ProviderAdapterEstimate;
  execute(
    request: unknown,
    options?: ProviderAdapterExecutionOptions,
  ): Promise<ProviderAdapterResult>;
  normalise_error(error: unknown): NormalisedAdapterError;
  licence_evidence(): ProviderRights;
  provenance(): ProviderAdapterProvenance;
}
