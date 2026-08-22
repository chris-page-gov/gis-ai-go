import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { CANONICAL_DOMAINS, contentAddress } from "@gis-ai-go/evidence";

import {
  ApprovedOnsDataQueryCache,
  ONS_ADAPTER_REQUEST,
  ProviderAdapterFault,
  createApprovedOnsDataQueryCache,
  isExactApprovedOnsDataQueryCache,
} from "../src/index.js";

const CACHE_PATH = new URL(
  "../../../../providers/ons/data-query-approved-cache.v1.json",
  import.meta.url,
);
const CACHE_RECORD = JSON.parse(readFileSync(CACHE_PATH, "utf8")) as Record<string, any>;
const CURRENT_CONTEXT = Object.freeze({
  checked_at: "2026-08-22T12:00:00.000Z",
  policy_id:
    "gis-ai-go:public-policy:sha256:b1a37b2ebf6900e2b5d62dfa20bcdaa1232e1c4c9f9630f90ac9d3dde738624a",
  policy_effect: "allow-with-obligations",
  operation: "data.query",
  resource_id:
    "gis-ai-go:public-read-resource:sha256:c7130712a40d75e71bcf0259792404389bea2e549adf6733f34d491f83e99f68",
  provider_failure: "PROVIDER_OUTAGE",
  provider_outage_source: "network",
  provider_status: null,
} as const);

function mutable<T>(value: T): T {
  return JSON.parse(JSON.stringify(value)) as T;
}

function resignCache(record: Record<string, any>): void {
  const { cache_id: ignored, ...core } = record;
  record.cache_id = contentAddress(
    "gis-ai-go:approved-provider-cache",
    CANONICAL_DOMAINS.approvedProviderCache,
    core,
  );
}

test("reads only the exact current policy-approved ONS cache", () => {
  const cache = createApprovedOnsDataQueryCache(CACHE_RECORD);
  const hit = cache.read(ONS_ADAPTER_REQUEST, CURRENT_CONTEXT);
  assert.deepEqual(hit, {
    cache_id:
      "gis-ai-go:approved-provider-cache:sha256:06dd19673c2f9d605dbad2c64a21903f6448fb4965838098bd16df40f6db4961",
    observation: {
      value: "10471",
      unit: null,
      metadata: [{ name: "Data Marking", value: "" }],
    },
    source_uri:
      "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121/observations?time=2026&geography=E92000001&week=week-24&causeofdeath=all-causes",
    provider_result_sha256:
      "309a7c0a374f93f20d4b4cc8aaa4530c4a828ea27e4e26e266b367e59b7da3bd",
    freshness: {
      status: "current",
      retrieved_at: "2026-08-20T20:21:08.947Z",
      stale_after: "2027-02-20T20:21:08.947Z",
      checked_at: "2026-08-22T12:00:00.000Z",
    },
  });
  assert.equal(Object.isFrozen(cache), true);
  assert.equal(Object.isFrozen(Object.getPrototypeOf(cache)), true);
  assert.equal(Object.isFrozen(hit), true);
  assert.equal(Object.isFrozen(hit?.freshness), true);
  assert.equal(isExactApprovedOnsDataQueryCache(cache), true);
  for (const providerStatus of [500, 503, 504, 599]) {
    assert.notEqual(
      cache.read(ONS_ADAPTER_REQUEST, {
        ...CURRENT_CONTEXT,
        provider_outage_source: "http-5xx",
        provider_status: providerStatus,
      }),
      null,
    );
  }
});

test("brands only constructor-validated exact cache instances", () => {
  const cache = createApprovedOnsDataQueryCache(CACHE_RECORD);
  let getterCalls = 0;
  const forged = Object.create(ApprovedOnsDataQueryCache.prototype) as object;
  Object.defineProperty(forged, "read", {
    enumerable: true,
    get: () => {
      getterCalls += 1;
      return () => null;
    },
  });
  Object.freeze(forged);

  class SubstitutedCache extends ApprovedOnsDataQueryCache {}

  assert.equal(isExactApprovedOnsDataQueryCache(forged), false);
  assert.equal(getterCalls, 0);
  assert.equal(isExactApprovedOnsDataQueryCache(new Proxy(cache, {})), false);
  assert.equal(isExactApprovedOnsDataQueryCache(new SubstitutedCache(CACHE_RECORD)), false);
  assert.equal(isExactApprovedOnsDataQueryCache(Object.freeze({ read: () => null })), false);
});

test("rejects cache content, coverage, approval and rebuild drift after re-signing", () => {
  const mutations: Array<[string, (record: Record<string, any>) => void]> = [
    ["observation", (record) => { record.observation.value = "10472"; }],
    ["coverage", (record) => { record.coverage.ingested_shards = 0; }],
    [
      "policy",
      (record) => {
        record.approval.policy_id = `gis-ai-go:public-policy:sha256:${"a".repeat(64)}`;
      },
    ],
    ["probe", (record) => { record.source.probe.sha256 = "b".repeat(64); }],
    ["freshness", (record) => { record.freshness.stale_after = record.source.retrieved_at; }],
    [
      "cache eligibility",
      (record) => { record.approval.cache_eligibility.provider_status_minimum = 400; },
    ],
    [
      "cache eligibility maximum",
      (record) => { record.approval.cache_eligibility.provider_status_maximum = 600; },
    ],
    [
      "cache eligibility transport",
      (record) => {
        record.approval.cache_eligibility.transport_failure_kinds = [
          "network",
          "unsafe-address",
        ];
      },
    ],
    [
      "cache eligibility timeout",
      (record) => { record.approval.cache_eligibility.local_timeout_use = "allowed"; },
    ],
    [
      "cache eligibility status",
      (record) => { record.approval.cache_eligibility.non_5xx_use = "allowed"; },
    ],
  ];
  for (const [label, mutate] of mutations) {
    const candidate = mutable(CACHE_RECORD);
    mutate(candidate);
    resignCache(candidate);
    assert.throws(
      () => createApprovedOnsDataQueryCache(candidate),
      TypeError,
      label,
    );
  }

  const rebuild = mutable(CACHE_RECORD);
  rebuild.rebuild.algorithm = "unreviewed-cache-rebuild.v1";
  const { rebuild_id: ignored, ...rebuildCore } = rebuild.rebuild;
  rebuild.rebuild.rebuild_id = contentAddress(
    "gis-ai-go:approved-cache-rebuild",
    CANONICAL_DOMAINS.approvedProviderCacheRebuild,
    rebuildCore,
  );
  resignCache(rebuild);
  assert.throws(() => createApprovedOnsDataQueryCache(rebuild), TypeError);
});

test("fails closed for stale, pre-retrieval, pre-approval or unauthorised reads", () => {
  const cache = createApprovedOnsDataQueryCache(CACHE_RECORD);
  const denied = [
    { ...CURRENT_CONTEXT, checked_at: "2026-08-20T20:21:08.946Z" },
    { ...CURRENT_CONTEXT, checked_at: "2026-08-21T12:00:00.000Z" },
    { ...CURRENT_CONTEXT, checked_at: "2027-02-20T20:21:08.947Z" },
    { ...CURRENT_CONTEXT, policy_effect: "deny" },
    { ...CURRENT_CONTEXT, resource_id: null },
    { ...CURRENT_CONTEXT, provider_failure: "PROVIDER_TIMEOUT" },
    { ...CURRENT_CONTEXT, provider_outage_source: "network", provider_status: 503 },
    { ...CURRENT_CONTEXT, provider_outage_source: "http-5xx", provider_status: null },
    { ...CURRENT_CONTEXT, provider_outage_source: "http-5xx", provider_status: 499 },
    { ...CURRENT_CONTEXT, provider_outage_source: "http-5xx", provider_status: 600 },
    { ...CURRENT_CONTEXT, provider_outage_source: "unsafe-address" },
  ];
  for (const context of denied) {
    assert.equal(
      cache.read(
        ONS_ADAPTER_REQUEST,
        context as Parameters<typeof cache.read>[1],
      ),
      null,
    );
  }

  const wrongQuery = {
    ...ONS_ADAPTER_REQUEST,
    selections: ONS_ADAPTER_REQUEST.selections.map((selection) => ({ ...selection })),
  };
  wrongQuery.selections[0]!.option = "2025";
  assert.throws(
    () => cache.read(wrongQuery, CURRENT_CONTEXT),
    (error: unknown) =>
      error instanceof ProviderAdapterFault && error.code === "INVALID_REQUEST",
  );
});
