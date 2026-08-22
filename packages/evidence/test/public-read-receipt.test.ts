import assert from "node:assert/strict";
import test from "node:test";

import {
  CANONICALISATION,
  PUBLIC_DATA_QUERY_APPROVED_CACHE_WARNING,
  PUBLIC_READ_ONS_RESOURCE,
  PUBLIC_READ_ONS_SELECTION_PLAN,
  PUBLIC_READ_SELECTION_PROFILE,
  PublicReadReceiptError,
  buildPublicSelectionPlan,
  buildPublicSelectionProfile,
  buildPublicReadPolicyDecision,
  buildPublicReadReceipt,
  canonicalJson,
  publicReadResultEvidenceBinding,
  verifyPublicReadPolicyDecision,
  verifyPublicReadResource,
  verifyPublicReadReceipt,
  verifyPublicReadReceiptStructure,
  verifyPublicSelectionPlan,
  verifyPublicSelectionProfile,
} from "../src/index.js";
import {
  makePublicReadReceiptBuildInput,
  makePublicReadReceiptFixture,
} from "./public-read-fixtures.js";

test("builds deterministic operation-specific v2 receipts without raw material", () => {
  const query = makePublicReadReceiptFixture("data.query");
  const selection = makePublicReadReceiptFixture(
    "selection.resolve",
    "request-public-read-fixture-2",
    "2123456789abcdef0123456789abcdef",
  );

  assert.equal(verifyPublicReadReceiptStructure(query.receipt), true);
  assert.equal(verifyPublicReadReceipt(query.receipt, query.material).valid, true);
  assert.equal(verifyPublicReadReceipt(selection.receipt, selection.material).valid, true);
  assert.equal(query.receipt.operation.normalised_parameters.domain, "gis-ai-go.data-query-parameters.v1");
  assert.equal(query.receipt.result.domain, "gis-ai-go.data-query-result-core.v1");
  assert.equal(
    selection.receipt.operation.normalised_parameters.domain,
    "gis-ai-go.selection-resolve-parameters.v1",
  );
  assert.equal(
    selection.receipt.result.domain,
    "gis-ai-go.selection-resolve-result-core.v1",
  );
  assert.notEqual(query.receipt.receipt_id, selection.receipt.receipt_id);
  assert.equal(Object.isFrozen(query.receipt), true);

  const stored = canonicalJson(query.receipt);
  assert.equal(stored.includes("raw-observation-value-should-not-appear"), false);
  assert.equal(stored.includes("data-query-parameters"), true);
  assert.equal(stored.includes(PUBLIC_READ_ONS_RESOURCE.rights.attribution), true);
});

test("binds an approved-cache result to its distinct pipeline and freshness check", () => {
  const input = makePublicReadReceiptBuildInput("data.query");
  const checkedAt = "2026-08-22T12:00:00.000Z";
  const resultCore = structuredClone(input.resultCore) as {
    data: {
      cache?: Record<string, unknown>;
      observations: unknown[];
      status: string;
    };
    warnings: string[];
  };
  resultCore.data.observations = [{ value: "10471", unit: null }];
  resultCore.data.cache = {
    cache_id:
      "gis-ai-go:approved-provider-cache:sha256:06dd19673c2f9d605dbad2c64a21903f6448fb4965838098bd16df40f6db4961",
    checked_at: checkedAt,
    provider_result_sha256:
      "309a7c0a374f93f20d4b4cc8aaa4530c4a828ea27e4e26e266b367e59b7da3bd",
    retrieved_at: "2026-08-20T20:21:08.947Z",
    source_uri:
      "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121/observations?time=2026&geography=E92000001&week=week-24&causeofdeath=all-causes",
    stale_after: "2027-02-20T20:21:08.947Z",
    status: "approved-current",
  };
  resultCore.warnings = [PUBLIC_DATA_QUERY_APPROVED_CACHE_WARNING];
  const transformations = [
    { name: "normalise-public-read-parameters", version: "v1" },
    { name: "read-approved-provider-cache", version: "v1" },
    { name: "project-public-read-result-core", version: "v1" },
  ] as const;
  const cachedInput = {
    ...input,
    createdAt: checkedAt,
    transformations,
    resultCore,
  };
  const receipt = buildPublicReadReceipt(cachedInput);

  assert.equal(verifyPublicReadReceiptStructure(receipt), true);
  assert.equal(
    verifyPublicReadReceipt(receipt, {
      normalisedParameters: cachedInput.normalisedParameters,
      resultCore,
      publicPolicy: cachedInput.publicPolicy,
      expectedAuthorityContext: cachedInput.authorityContext,
      expectedPolicyDecision: cachedInput.policyDecision,
      expectedResource: cachedInput.resource,
      expectedSoftware: cachedInput.software,
    }).valid,
    true,
  );
  assert.deepEqual(receipt.transformations, transformations);
  assert.throws(
    () => buildPublicReadReceipt({ ...cachedInput, transformations: input.transformations }),
    PublicReadReceiptError,
  );
  assert.throws(
    () => buildPublicReadReceipt({ ...cachedInput, createdAt: "2026-08-22T12:00:01.000Z" }),
    PublicReadReceiptError,
  );
  for (const [field, value] of [
    [
      "cache_id",
      `gis-ai-go:approved-provider-cache:sha256:${"a".repeat(64)}`,
    ],
    ["provider_result_sha256", "b".repeat(64)],
    ["retrieved_at", "2026-08-20T20:21:08.948Z"],
    ["stale_after", "2027-02-20T20:21:08.948Z"],
  ] as const) {
    const candidate = structuredClone(resultCore);
    candidate.data.cache![field] = value;
    assert.throws(
      () => buildPublicReadReceipt({ ...cachedInput, resultCore: candidate }),
      PublicReadReceiptError,
    );
  }
  const wrongObservation = structuredClone(resultCore);
  wrongObservation.data.observations = [{ value: "10472", unit: null }];
  assert.throws(
    () => buildPublicReadReceipt({ ...cachedInput, resultCore: wrongObservation }),
    PublicReadReceiptError,
  );
  const beforeApproval = structuredClone(resultCore);
  beforeApproval.data.cache!.checked_at = "2026-08-21T12:00:00.000Z";
  assert.throws(
    () =>
      buildPublicReadReceipt({
        ...cachedInput,
        createdAt: "2026-08-21T12:00:00.000Z",
        resultCore: beforeApproval,
      }),
    PublicReadReceiptError,
  );
});

test("binds the exact profile, provider, dataset, version and rights evidence", () => {
  const fixture = makePublicReadReceiptFixture("data.query");
  const binding = fixture.input.resultCore as {
    evidence_binding: Record<string, unknown>;
  };
  assert.deepEqual(binding.evidence_binding, {
    adapter_id: "gis-ai-go.ons-data-api",
    dataset_id: "weekly-deaths-region",
    edition: "time-series",
    profile_sha256: "535e6eb65fc9af4507e30700d425393a658a085a3a240689f4b37124dc8f8622",
    provider_id: "ons-data-api",
    resource_id: PUBLIC_READ_ONS_RESOURCE.resource_id,
    returned_item_count: 1,
    rights_sha256: "305b49e6d1f55de0109de12b2cbf0b7ec5da1d573e111f5884736c832b2e4b17",
    version: "121",
  });
});

test("binds the exact reviewed selection profile and non-executable plan", () => {
  assert.equal(verifyPublicSelectionPlan(PUBLIC_READ_ONS_SELECTION_PLAN), true);
  assert.equal(verifyPublicSelectionProfile(PUBLIC_READ_SELECTION_PROFILE), true);
  assert.equal(
    PUBLIC_READ_ONS_SELECTION_PLAN.plan_id,
    "gis-ai-go:selection-plan:sha256:dbae1e78051a3a3bdfd0b49c0318d54df3a500effcb85df8cf34ad4e3cd31d9e",
  );
  assert.equal(
    PUBLIC_READ_SELECTION_PROFILE.selection_profile_id,
    "gis-ai-go:public-selection-profile:sha256:344fe6d8cbec7c355735ee711cd19b067be306f4087b30c341efec6c5e819f8e",
  );
  assert.equal(PUBLIC_READ_ONS_SELECTION_PLAN.execution, "forbidden");
  assert.equal(PUBLIC_READ_ONS_SELECTION_PLAN.controls.provider_execution, false);

  const alteredPlan = structuredClone(PUBLIC_READ_ONS_SELECTION_PLAN) as unknown as {
    plan_id?: string;
    data_query: { dataset: { version: string } };
  };
  delete alteredPlan.plan_id;
  alteredPlan.data_query.dataset.version = "latest";
  assert.throws(
    () => buildPublicSelectionPlan(alteredPlan as never),
    PublicReadReceiptError,
  );

  const alteredProfile = structuredClone(PUBLIC_READ_SELECTION_PROFILE) as unknown as {
    selection_profile_id?: string;
    ranking: { tie_handling: string };
  };
  delete alteredProfile.selection_profile_id;
  alteredProfile.ranking.tie_handling = "choose-first";
  assert.throws(
    () => buildPublicSelectionProfile(alteredProfile as never),
    PublicReadReceiptError,
  );
});

test("fails closed on altered parameters, result material and retained identities", () => {
  const fixture = makePublicReadReceiptFixture("data.query");
  assert.equal(
    verifyPublicReadReceipt(fixture.receipt, {
      ...fixture.material,
      normalisedParameters: { unexpected: true },
    }).valid,
    false,
  );
  assert.equal(
    verifyPublicReadReceipt(fixture.receipt, {
      ...fixture.material,
      resultCore: { ...(fixture.material.resultCore as object), unexpected: true },
    }).valid,
    false,
  );
  const tampered = structuredClone(fixture.receipt) as unknown as Record<string, unknown>;
  const resource = tampered.resource as { rights: { attribution: string } };
  resource.rights.attribution = "Unreviewed attribution";
  assert.equal(verifyPublicReadReceiptStructure(tampered), false);
});

test("does not fabricate a success receipt for denial or ambiguity", () => {
  const deniedInput = makePublicReadReceiptBuildInput("data.query");
  const deniedDecision = buildPublicReadPolicyDecision({
    schema: "gis-ai-go.public-policy-decision.v2",
    canonicalisation: CANONICALISATION,
    request_id: deniedInput.requestId,
    trace_id: deniedInput.traceId,
    authority_context_id: deniedInput.authorityContext.context_id,
    policy_id: deniedInput.publicPolicy.policy_id,
    policy_version: "2.0.0",
    policy_default_effect: "deny",
    operation: "data.query",
    resource_id: null,
    effect: "deny",
    reason_code: "resource-not-approved",
    obligations: [],
  });
  assert.throws(
    () => buildPublicReadReceipt({ ...deniedInput, policyDecision: deniedDecision }),
    PublicReadReceiptError,
  );

  const ambiguousInput = makePublicReadReceiptBuildInput("selection.resolve");
  const ambiguousResult = structuredClone(ambiguousInput.resultCore) as {
    data: { status: string };
  };
  ambiguousResult.data.status = "ambiguous";
  assert.throws(
    () => buildPublicReadReceipt({ ...ambiguousInput, resultCore: ambiguousResult }),
    PublicReadReceiptError,
  );
});

test("rejects cross-operation parameters and non-singleton successful results", () => {
  const query = makePublicReadReceiptBuildInput("data.query");
  const selection = makePublicReadReceiptBuildInput("selection.resolve");
  assert.throws(
    () => buildPublicReadReceipt({ ...query, normalisedParameters: selection.normalisedParameters }),
    PublicReadReceiptError,
  );
  assert.throws(
    () => buildPublicReadReceipt({ ...selection, normalisedParameters: query.normalisedParameters }),
    PublicReadReceiptError,
  );

  for (const observations of [[], [{ value: "one" }, { value: "two" }]]) {
    const resultCore = structuredClone(query.resultCore) as {
      data: { observations: unknown[] };
    };
    resultCore.data.observations = observations;
    assert.throws(
      () => buildPublicReadReceipt({ ...query, resultCore }),
      PublicReadReceiptError,
    );
  }

  for (const patch of [
    { ambiguity: { reason: "tie" } },
    { resource_id: `gis-ai-go:public-read-resource:sha256:${"0".repeat(64)}` },
  ]) {
    const resultCore = structuredClone(selection.resultCore) as {
      data: Record<string, unknown>;
    };
    Object.assign(resultCore.data, patch);
    assert.throws(
      () => buildPublicReadReceipt({ ...selection, resultCore }),
      PublicReadReceiptError,
    );
  }
});

test("enforces every fixed parameter and closed successful-result boundary", () => {
  const query = makePublicReadReceiptBuildInput("data.query");
  const selection = makePublicReadReceiptBuildInput("selection.resolve");
  const queryParameters = structuredClone(query.normalisedParameters) as {
    dataset: { version: string };
    limit: number;
    selections: Array<{ dimension: string; option: string }>;
    unexpected?: boolean;
  };
  const parameterMutations: Array<() => void> = [
    () => { queryParameters.dataset.version = "latest"; },
    () => { queryParameters.limit = 2; },
    () => { queryParameters.selections[0]!.option = "1900"; },
    () => { queryParameters.selections.reverse(); },
    () => { queryParameters.unexpected = true; },
  ];
  for (const mutate of parameterMutations) {
    queryParameters.dataset.version = "121";
    queryParameters.limit = 1;
    queryParameters.selections = PUBLIC_READ_ONS_RESOURCE.selections.map(
      ({ dimension, option }) => ({ dimension, option }),
    );
    delete queryParameters.unexpected;
    mutate();
    assert.throws(
      () => buildPublicReadReceipt({ ...query, normalisedParameters: queryParameters }),
      PublicReadReceiptError,
    );
  }

  const selectionParameters = structuredClone(selection.normalisedParameters) as {
    profile_id: string;
    provider_id: string;
  };
  selectionParameters.profile_id = "unreviewed-profile";
  assert.throws(
    () => buildPublicReadReceipt({ ...selection, normalisedParameters: selectionParameters }),
    PublicReadReceiptError,
  );
  selectionParameters.profile_id = PUBLIC_READ_ONS_RESOURCE.profile.id;
  selectionParameters.provider_id = "unreviewed-provider";
  assert.throws(
    () => buildPublicReadReceipt({ ...selection, normalisedParameters: selectionParameters }),
    PublicReadReceiptError,
  );

  const queryResult = structuredClone(query.resultCore) as {
    data: { observations: Array<Record<string, unknown>> };
  };
  queryResult.data.observations[0]!.extra = true;
  assert.throws(
    () => buildPublicReadReceipt({ ...query, resultCore: queryResult }),
    PublicReadReceiptError,
  );

  const selectionResult = structuredClone(selection.resultCore) as {
    data: Record<string, unknown>;
  };
  selectionResult.data.extra = true;
  assert.throws(
    () => buildPublicReadReceipt({ ...selection, resultCore: selectionResult }),
    PublicReadReceiptError,
  );

  const alteredPlanResult = structuredClone(selection.resultCore) as {
    data: { plan: { execution: string } };
  };
  alteredPlanResult.data.plan.execution = "allowed";
  assert.throws(
    () => buildPublicReadReceipt({ ...selection, resultCore: alteredPlanResult }),
    PublicReadReceiptError,
  );

  const alteredRankingResult = structuredClone(selection.resultCore) as {
    data: { ranking: { score: number; top_score_tied: boolean } };
  };
  alteredRankingResult.data.ranking.score += 1;
  alteredRankingResult.data.ranking.top_score_tied = true;
  assert.throws(
    () => buildPublicReadReceipt({ ...selection, resultCore: alteredRankingResult }),
    PublicReadReceiptError,
  );
});

test("rejects proxy and accessor material before any trust decision", () => {
  const resource = structuredClone(PUBLIC_READ_ONS_RESOURCE);
  let reads = 0;
  const proxy = new Proxy(resource, {
    get(target, property, receiver) {
      reads += 1;
      return Reflect.get(target, property, receiver);
    },
  });
  assert.equal(verifyPublicReadResource(proxy), false);
  assert.throws(() => publicReadResultEvidenceBinding(proxy), PublicReadReceiptError);
  assert.equal(reads, 0);

  const fixture = makePublicReadReceiptFixture("data.query");
  assert.equal(verifyPublicReadReceiptStructure(new Proxy(fixture.receipt, {})), false);
  assert.throws(
    () => buildPublicReadReceipt(new Proxy(fixture.input, {})),
    PublicReadReceiptError,
  );
  assert.equal(
    verifyPublicReadReceipt(fixture.receipt, new Proxy(fixture.material, {})).valid,
    false,
  );
});

test("requires exact policy identities and disjoint denial reasons", () => {
  const input = makePublicReadReceiptBuildInput("data.query");
  const allowed = input.policyDecision;
  for (const patch of [
    { authority_context_id: `gis-ai-go:public-authority-context:sha256:${"a".repeat(64)}` },
    { policy_id: `gis-ai-go:public-policy:sha256:${"b".repeat(64)}` },
    {
      effect: "deny",
      reason_code: "operation-not-allowed",
      resource_id: null,
      obligations: [],
    },
  ]) {
    const core = structuredClone(allowed) as unknown as Record<string, unknown>;
    delete core.decision_id;
    Object.assign(core, patch);
    assert.throws(
      () => buildPublicReadPolicyDecision(core as never),
      PublicReadReceiptError,
    );
  }
  assert.equal(verifyPublicReadPolicyDecision(allowed), true);

  for (const denial of [
    {
      operation: "data.query",
      reason_code: "authority-context-not-applicable",
    },
    {
      operation: "map.render",
      reason_code: "operation-not-allowed",
    },
    {
      operation: "selection.resolve",
      reason_code: "resource-not-approved",
    },
  ] as const) {
    const core = structuredClone(allowed) as unknown as Record<string, unknown>;
    delete core.decision_id;
    Object.assign(core, denial, {
      effect: "deny",
      resource_id: null,
      obligations: [],
    });
    assert.equal(
      verifyPublicReadPolicyDecision(buildPublicReadPolicyDecision(core as never)),
      true,
    );
  }
});
