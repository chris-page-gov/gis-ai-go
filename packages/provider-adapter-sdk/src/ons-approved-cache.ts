import {
  CANONICAL_DOMAINS,
  PUBLIC_DATA_QUERY_APPROVED_CACHE_ID,
  PUBLIC_DATA_QUERY_APPROVED_CACHE_PROVIDER_RESULT_SHA256,
  PUBLIC_READ_ONS_RESOURCE,
  PUBLIC_READ_POLICY_ID,
  canonicalJson,
  canonicalJsonBytes,
  canonicalJsonClone,
  publicReadResultEvidenceBinding,
  verifyContentAddress,
} from "@gis-ai-go/evidence";

import { ProviderAdapterFault } from "./contract.js";
import { ONS_ADAPTER_REQUEST, ONS_OBSERVATION_URI } from "./ons-data-api.js";
import type { ProviderAdapterQuery } from "./types.js";

const CACHE_ID_PREFIX = "gis-ai-go:approved-provider-cache";
const REBUILD_ID_PREFIX = "gis-ai-go:approved-cache-rebuild";
const ACCEPTED_OBSERVATION_VALUE = "10471";
const ACCEPTED_PROBE_PATH = "providers/ons/data-api-adapter-live-probe.v1.json";
const ACCEPTED_PROBE_SHA256 =
  "51fc8acb0465c368aa7d2925f8be37c28b4f87ab395a306c29f586dd4d0e344b";
const ACCEPTED_PROBE_GIT_BLOB = "80aefe6ec0acd54f0510ab92715db55ad1ab2143";
const RFC3339_MILLISECONDS =
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/u;
const NUMERIC_OBSERVATION = /^(?:0|[1-9][0-9]{0,14})$/u;
const APPROVED_ONS_CACHE_INSTANCES = new WeakSet<object>();

export interface ApprovedOnsDataQueryCacheRecord {
  readonly schema: "gis-ai-go.approved-provider-cache.v1";
  readonly cache_id: typeof PUBLIC_DATA_QUERY_APPROVED_CACHE_ID;
  readonly operation: "data.query";
  readonly resource_id: typeof PUBLIC_READ_ONS_RESOURCE.resource_id;
  readonly query: ProviderAdapterQuery;
  readonly observation: {
    readonly value: string;
    readonly unit: null;
    readonly metadata: readonly [{ readonly name: "Data Marking"; readonly value: "" }];
  };
  readonly rights_sha256: string;
  readonly source: {
    readonly source_uri: typeof ONS_OBSERVATION_URI;
    readonly retrieved_at: string;
    readonly provider_result: {
      readonly domain: typeof CANONICAL_DOMAINS.providerAdapterResult;
      readonly sha256: typeof PUBLIC_DATA_QUERY_APPROVED_CACHE_PROVIDER_RESULT_SHA256;
    };
    readonly probe: {
      readonly path: typeof ACCEPTED_PROBE_PATH;
      readonly sha256: typeof ACCEPTED_PROBE_SHA256;
      readonly git_blob: typeof ACCEPTED_PROBE_GIT_BLOB;
    };
  };
  readonly coverage: {
    readonly expected_shards: 1;
    readonly ingested_shards: 1;
    readonly expected_observations: 1;
    readonly ingested_observations: 1;
    readonly complete: true;
  };
  readonly freshness: {
    readonly stale_after: string;
    readonly stale_use: "forbidden";
  };
  readonly approval: {
    readonly kind: "compiled-repository-policy";
    readonly policy_id: typeof PUBLIC_READ_POLICY_ID;
    readonly rule_id: "public-data-query-ons-v121";
    readonly effect: "allow-with-obligations";
    readonly operation: "data.query";
    readonly resource_id: typeof PUBLIC_READ_ONS_RESOURCE.resource_id;
    readonly permitted_provider_failures: readonly ["PROVIDER_OUTAGE"];
    readonly cache_eligibility: {
      readonly code: "PROVIDER_OUTAGE";
      readonly transport_failure_kinds: readonly ["network"];
      readonly provider_status_minimum: 500;
      readonly provider_status_maximum: 599;
      readonly local_timeout_use: "forbidden";
      readonly non_5xx_use: "forbidden";
    };
    readonly freshness: "current-only";
    readonly approved_at: string;
  };
  readonly rebuild: {
    readonly rebuild_id: string;
    readonly algorithm: "verified-single-observation-cache-projection.v1";
    readonly source_probe_sha256: typeof ACCEPTED_PROBE_SHA256;
    readonly provider_result_sha256:
      typeof PUBLIC_DATA_QUERY_APPROVED_CACHE_PROVIDER_RESULT_SHA256;
  };
}

export interface ApprovedOnsDataQueryCacheReadContext {
  readonly checked_at: string;
  readonly policy_id: string;
  readonly policy_effect: string;
  readonly operation: string;
  readonly resource_id: string | null;
  readonly provider_failure: string;
  readonly provider_outage_source: "network" | "http-5xx";
  readonly provider_status: number | null;
}

export interface ApprovedOnsDataQueryCacheHit {
  readonly cache_id: typeof PUBLIC_DATA_QUERY_APPROVED_CACHE_ID;
  readonly observation: ApprovedOnsDataQueryCacheRecord["observation"];
  readonly source_uri: typeof ONS_OBSERVATION_URI;
  readonly provider_result_sha256:
    typeof PUBLIC_DATA_QUERY_APPROVED_CACHE_PROVIDER_RESULT_SHA256;
  readonly freshness: {
    readonly status: "current";
    readonly retrieved_at: string;
    readonly stale_after: string;
    readonly checked_at: string;
  };
}

function recordAt(value: unknown, label: string): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError(`${label} must be an object`);
  }
  return value as Record<string, unknown>;
}

function exactKeys(
  value: Record<string, unknown>,
  expected: readonly string[],
  label: string,
): void {
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  if (actual.length !== wanted.length || actual.some((key, index) => key !== wanted[index])) {
    throw new TypeError(`${label} has an unexpected shape`);
  }
}

function canonicalTimestamp(value: unknown, label: string): string {
  if (typeof value !== "string" || !RFC3339_MILLISECONDS.test(value)) {
    throw new TypeError(`${label} must be a canonical UTC timestamp`);
  }
  const milliseconds = Date.parse(value);
  if (!Number.isFinite(milliseconds) || new Date(milliseconds).toISOString() !== value) {
    throw new TypeError(`${label} must be a valid canonical UTC timestamp`);
  }
  return value;
}

function sameCanonical(left: unknown, right: unknown): boolean {
  try {
    return canonicalJson(left) === canonicalJson(right);
  } catch {
    return false;
  }
}

function parseRecord(value: unknown): ApprovedOnsDataQueryCacheRecord {
  let snapshot: unknown;
  try {
    snapshot = canonicalJsonClone(value);
  } catch {
    throw new TypeError("Approved ONS cache must be detached canonical JSON");
  }
  if (canonicalJsonBytes(snapshot).byteLength > 32_768) {
    throw new TypeError("Approved ONS cache exceeds the fixed canonical byte limit");
  }
  const record = recordAt(snapshot, "Approved ONS cache");
  exactKeys(
    record,
    [
      "approval",
      "cache_id",
      "coverage",
      "freshness",
      "observation",
      "operation",
      "query",
      "rebuild",
      "resource_id",
      "rights_sha256",
      "schema",
      "source",
    ],
    "Approved ONS cache",
  );
  if (
    record.schema !== "gis-ai-go.approved-provider-cache.v1" ||
    record.operation !== "data.query" ||
    record.resource_id !== PUBLIC_READ_ONS_RESOURCE.resource_id ||
    !sameCanonical(record.query, ONS_ADAPTER_REQUEST) ||
    record.rights_sha256 !== publicReadResultEvidenceBinding().rights_sha256
  ) {
    throw new TypeError("Approved ONS cache does not bind the exact public ONS query");
  }

  const observation = recordAt(record.observation, "Approved ONS cache observation");
  exactKeys(observation, ["metadata", "unit", "value"], "Approved ONS cache observation");
  if (
    typeof observation.value !== "string" ||
    !NUMERIC_OBSERVATION.test(observation.value) ||
    observation.value !== ACCEPTED_OBSERVATION_VALUE ||
    observation.unit !== null ||
    !sameCanonical(observation.metadata, [{ name: "Data Marking", value: "" }])
  ) {
    throw new TypeError("Approved ONS cache observation is invalid");
  }

  const source = recordAt(record.source, "Approved ONS cache source");
  exactKeys(
    source,
    ["probe", "provider_result", "retrieved_at", "source_uri"],
    "Approved ONS cache source",
  );
  const retrievedAt = canonicalTimestamp(
    source.retrieved_at,
    "Approved ONS cache retrieval time",
  );
  const providerResult = recordAt(
    source.provider_result,
    "Approved ONS cache provider result",
  );
  exactKeys(providerResult, ["domain", "sha256"], "Approved ONS cache provider result");
  const probe = recordAt(source.probe, "Approved ONS cache probe");
  exactKeys(probe, ["git_blob", "path", "sha256"], "Approved ONS cache probe");
  if (
    source.source_uri !== ONS_OBSERVATION_URI ||
    providerResult.domain !== CANONICAL_DOMAINS.providerAdapterResult ||
    providerResult.sha256 !==
      PUBLIC_DATA_QUERY_APPROVED_CACHE_PROVIDER_RESULT_SHA256 ||
    probe.path !== ACCEPTED_PROBE_PATH ||
    probe.sha256 !== ACCEPTED_PROBE_SHA256 ||
    probe.git_blob !== ACCEPTED_PROBE_GIT_BLOB
  ) {
    throw new TypeError("Approved ONS cache source evidence is not the accepted probe");
  }

  const coverage = recordAt(record.coverage, "Approved ONS cache coverage");
  exactKeys(
    coverage,
    [
      "complete",
      "expected_observations",
      "expected_shards",
      "ingested_observations",
      "ingested_shards",
    ],
    "Approved ONS cache coverage",
  );
  if (
    coverage.complete !== true ||
    coverage.expected_shards !== 1 ||
    coverage.ingested_shards !== 1 ||
    coverage.expected_observations !== 1 ||
    coverage.ingested_observations !== 1
  ) {
    throw new TypeError("Approved ONS cache coverage must be complete and exact");
  }

  const freshness = recordAt(record.freshness, "Approved ONS cache freshness");
  exactKeys(freshness, ["stale_after", "stale_use"], "Approved ONS cache freshness");
  const staleAfter = canonicalTimestamp(
    freshness.stale_after,
    "Approved ONS cache stale-after time",
  );
  if (freshness.stale_use !== "forbidden" || Date.parse(staleAfter) <= Date.parse(retrievedAt)) {
    throw new TypeError("Approved ONS cache freshness policy is invalid");
  }

  const approval = recordAt(record.approval, "Approved ONS cache approval");
  exactKeys(
    approval,
    [
      "approved_at",
      "cache_eligibility",
      "effect",
      "freshness",
      "kind",
      "operation",
      "permitted_provider_failures",
      "policy_id",
      "resource_id",
      "rule_id",
    ],
    "Approved ONS cache approval",
  );
  const approvedAt = canonicalTimestamp(
    approval.approved_at,
    "Approved ONS cache approval time",
  );
  const cacheEligibility = recordAt(
    approval.cache_eligibility,
    "Approved ONS cache eligibility",
  );
  exactKeys(
    cacheEligibility,
    [
      "code",
      "local_timeout_use",
      "non_5xx_use",
      "provider_status_maximum",
      "provider_status_minimum",
      "transport_failure_kinds",
    ],
    "Approved ONS cache eligibility",
  );
  if (
    approval.kind !== "compiled-repository-policy" ||
    approval.policy_id !== PUBLIC_READ_POLICY_ID ||
    approval.rule_id !== "public-data-query-ons-v121" ||
    approval.effect !== "allow-with-obligations" ||
    approval.operation !== "data.query" ||
    approval.resource_id !== PUBLIC_READ_ONS_RESOURCE.resource_id ||
    approval.freshness !== "current-only" ||
    !sameCanonical(approval.permitted_provider_failures, ["PROVIDER_OUTAGE"]) ||
    cacheEligibility.code !== "PROVIDER_OUTAGE" ||
    !sameCanonical(cacheEligibility.transport_failure_kinds, ["network"]) ||
    cacheEligibility.provider_status_minimum !== 500 ||
    cacheEligibility.provider_status_maximum !== 599 ||
    cacheEligibility.local_timeout_use !== "forbidden" ||
    cacheEligibility.non_5xx_use !== "forbidden" ||
    Date.parse(approvedAt) < Date.parse(retrievedAt) ||
    Date.parse(approvedAt) >= Date.parse(staleAfter)
  ) {
    throw new TypeError("Approved ONS cache approval is invalid");
  }

  const rebuild = recordAt(record.rebuild, "Approved ONS cache rebuild");
  exactKeys(
    rebuild,
    ["algorithm", "provider_result_sha256", "rebuild_id", "source_probe_sha256"],
    "Approved ONS cache rebuild",
  );
  if (
    rebuild.algorithm !== "verified-single-observation-cache-projection.v1" ||
    rebuild.provider_result_sha256 !==
      PUBLIC_DATA_QUERY_APPROVED_CACHE_PROVIDER_RESULT_SHA256 ||
    rebuild.source_probe_sha256 !== ACCEPTED_PROBE_SHA256
  ) {
    throw new TypeError("Approved ONS cache rebuild evidence is invalid");
  }
  const { rebuild_id: rebuildId, ...rebuildCore } = rebuild;
  if (
    typeof rebuildId !== "string" ||
    !verifyContentAddress(
      rebuildId,
      REBUILD_ID_PREFIX,
      CANONICAL_DOMAINS.approvedProviderCacheRebuild,
      rebuildCore,
    )
  ) {
    throw new TypeError("Approved ONS cache rebuild identity is invalid");
  }

  const { cache_id: cacheId, ...cacheCore } = record;
  if (
    typeof cacheId !== "string" ||
    cacheId !== PUBLIC_DATA_QUERY_APPROVED_CACHE_ID ||
    !verifyContentAddress(
      cacheId,
      CACHE_ID_PREFIX,
      CANONICAL_DOMAINS.approvedProviderCache,
      cacheCore,
    )
  ) {
    throw new TypeError("Approved ONS cache content identity is invalid");
  }
  return snapshot as ApprovedOnsDataQueryCacheRecord;
}

function parseReadContext(value: unknown): ApprovedOnsDataQueryCacheReadContext {
  let snapshot: unknown;
  try {
    snapshot = canonicalJsonClone(value);
  } catch {
    throw new TypeError("Approved ONS cache read context must be canonical JSON");
  }
  const context = recordAt(snapshot, "Approved ONS cache read context");
  exactKeys(
    context,
    [
      "checked_at",
      "operation",
      "policy_effect",
      "policy_id",
      "provider_failure",
      "provider_outage_source",
      "provider_status",
      "resource_id",
    ],
    "Approved ONS cache read context",
  );
  canonicalTimestamp(context.checked_at, "Approved ONS cache check time");
  return snapshot as ApprovedOnsDataQueryCacheReadContext;
}

/**
 * One exact, content-addressed and policy-bound ONS cache. Construction and use
 * are explicit; the shipped runtime has no loader, environment switch or default.
 */
export class ApprovedOnsDataQueryCache {
  readonly #record: ApprovedOnsDataQueryCacheRecord;

  public constructor(value: unknown) {
    this.#record = parseRecord(value);
    Object.freeze(this);
    APPROVED_ONS_CACHE_INSTANCES.add(this);
  }

  public read(
    request: unknown,
    contextValue: ApprovedOnsDataQueryCacheReadContext,
  ): ApprovedOnsDataQueryCacheHit | null {
    let query: unknown;
    try {
      query = canonicalJsonClone(request);
    } catch {
      throw new ProviderAdapterFault("INVALID_REQUEST");
    }
    if (!sameCanonical(query, ONS_ADAPTER_REQUEST)) {
      throw new ProviderAdapterFault("INVALID_REQUEST");
    }
    const context = parseReadContext(contextValue);
    if (
      context.policy_id !== this.#record.approval.policy_id ||
      context.policy_effect !== this.#record.approval.effect ||
      context.operation !== this.#record.approval.operation ||
      context.resource_id !== this.#record.approval.resource_id ||
      !this.#record.approval.permitted_provider_failures.includes(
        context.provider_failure as "PROVIDER_OUTAGE",
      ) ||
      (context.provider_outage_source === "network"
        ? context.provider_status !== null ||
          !this.#record.approval.cache_eligibility.transport_failure_kinds.includes(
            "network",
          )
        : context.provider_outage_source === "http-5xx"
          ? !Number.isInteger(context.provider_status) ||
            context.provider_status! <
              this.#record.approval.cache_eligibility.provider_status_minimum ||
            context.provider_status! >
              this.#record.approval.cache_eligibility.provider_status_maximum
          : true)
    ) {
      return null;
    }
    const checkedAt = Date.parse(context.checked_at);
    if (
      checkedAt < Date.parse(this.#record.source.retrieved_at) ||
      checkedAt < Date.parse(this.#record.approval.approved_at) ||
      checkedAt >= Date.parse(this.#record.freshness.stale_after)
    ) {
      return null;
    }
    return canonicalJsonClone({
      cache_id: this.#record.cache_id,
      observation: this.#record.observation,
      source_uri: this.#record.source.source_uri,
      provider_result_sha256: PUBLIC_DATA_QUERY_APPROVED_CACHE_PROVIDER_RESULT_SHA256,
      freshness: {
        status: "current",
        retrieved_at: this.#record.source.retrieved_at,
        stale_after: this.#record.freshness.stale_after,
        checked_at: context.checked_at,
      },
    });
  }
}

Object.freeze(ApprovedOnsDataQueryCache.prototype);
Object.freeze(ApprovedOnsDataQueryCache);

export function isExactApprovedOnsDataQueryCache(
  value: unknown,
): value is ApprovedOnsDataQueryCache {
  if (
    typeof value !== "object" ||
    value === null ||
    !APPROVED_ONS_CACHE_INSTANCES.has(value)
  ) {
    return false;
  }
  return (
    Object.getPrototypeOf(value) === ApprovedOnsDataQueryCache.prototype &&
    Object.isFrozen(value)
  );
}

export function createApprovedOnsDataQueryCache(value: unknown): ApprovedOnsDataQueryCache {
  return new ApprovedOnsDataQueryCache(value);
}
