import type { ApprovedOnsDataQueryCacheRecord } from "@gis-ai-go/provider-adapter-sdk";

import type { GovernedCandidateAssembly } from "./governed-assembly.js";

export interface LocalCandidateCapabilityHealth {
  readonly schema: "gis-ai-go.local-candidate-capability-health.v1";
  readonly checked_at: string | null;
  readonly data_query: "available" | "expired" | "not-yet-approved" | "clock-unavailable";
  readonly data_vintage: {
    readonly dataset: Readonly<ApprovedOnsDataQueryCacheRecord["query"]["dataset"]>;
    readonly selections: ApprovedOnsDataQueryCacheRecord["query"]["selections"];
    readonly source_uri: string;
    readonly retrieved_at: string;
    readonly current_statistics: false;
  };
  readonly approved_cache: {
    readonly cache_id: string;
    readonly approved_at: string;
    readonly stale_after: string;
    readonly stale_use: "forbidden";
  };
  readonly evidence_retention: "current-session-only";
  readonly expiry_effect: "data.query fails closed; evidence inspection remains available";
}

const LOCAL_CAPABILITIES = new WeakMap<
  GovernedCandidateAssembly,
  () => LocalCandidateCapabilityHealth
>();

/** @internal Registered only by the fixed local assembly after cache validation. */
export function registerLocalCandidateCapability(
  assembly: GovernedCandidateAssembly,
  record: ApprovedOnsDataQueryCacheRecord,
  now: () => Date,
): void {
  if (LOCAL_CAPABILITIES.has(assembly)) {
    throw new TypeError("Local candidate capability is already registered");
  }
  const dataVintage = Object.freeze({
    dataset: Object.freeze({ ...record.query.dataset }),
    selections: Object.freeze(record.query.selections.map(
      (selection) => Object.freeze({ ...selection }),
    )),
    source_uri: record.source.source_uri,
    retrieved_at: record.source.retrieved_at,
    current_statistics: false as const,
  });
  const approvedCache = Object.freeze({
    cache_id: record.cache_id,
    approved_at: record.approval.approved_at,
    stale_after: record.freshness.stale_after,
    stale_use: "forbidden" as const,
  });
  const availableFrom = Math.max(
    Date.parse(dataVintage.retrieved_at),
    Date.parse(approvedCache.approved_at),
  );
  const expiresAt = Date.parse(approvedCache.stale_after);
  LOCAL_CAPABILITIES.set(assembly, () => {
    let checkedAt = Number.NaN;
    try {
      checkedAt = Date.prototype.getTime.call(now());
    } catch {
      // A bad clock must never make the cache appear available.
    }
    return Object.freeze({
      schema: "gis-ai-go.local-candidate-capability-health.v1",
      checked_at: Number.isFinite(checkedAt) ? new Date(checkedAt).toISOString() : null,
      data_query: !Number.isFinite(checkedAt)
        ? "clock-unavailable"
        : checkedAt < availableFrom
          ? "not-yet-approved"
          : checkedAt >= expiresAt ? "expired" : "available",
      data_vintage: dataVintage,
      approved_cache: approvedCache,
      evidence_retention: "current-session-only",
      expiry_effect: "data.query fails closed; evidence inspection remains available",
    });
  });
}

/** No value is exposed for generic, production or other candidate assemblies. */
export function localCandidateCapabilityHealth(
  assembly: GovernedCandidateAssembly,
): LocalCandidateCapabilityHealth | undefined {
  return LOCAL_CAPABILITIES.get(assembly)?.();
}
