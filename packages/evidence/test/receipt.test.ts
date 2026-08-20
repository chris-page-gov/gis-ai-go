import assert from "node:assert/strict";
import test from "node:test";

import {
  CANONICALISATION,
  CANONICAL_DOMAINS,
  PUBLIC_POLICY_OBLIGATIONS,
  buildInlineReceipt,
  buildPublicAuthorityContext,
  buildPublicPolicyDecision,
  canonicalJson,
  contentAddress,
  domainSeparatedSha256,
  verifyInlineReceipt,
  verifyPublicAuthorityContext,
  verifyPublicPolicy,
  verifyPublicPolicyDecision,
  type InlineReceiptBuildInput,
  type PublicAuthorityContextCore,
  type PublicPolicy,
  type PublicPolicyDecisionCore,
} from "../src/index.js";
import {
  CATALOGUE,
  REQUEST_ID,
  SOFTWARE,
  TRACE_ID,
  makeAuthorityContext,
  makePolicyDecision,
  makePublicPolicy,
  makeReceiptBuildInput,
  makeReceiptFixture,
} from "./fixtures.js";

function mutable<T>(value: T): T {
  return JSON.parse(JSON.stringify(value)) as T;
}

function readdress(
  value: Record<string, unknown>,
  identityKey: string,
  prefix: string,
  domain: string,
): void {
  delete value[identityKey];
  value[identityKey] = contentAddress(prefix, domain, value);
}

test("builds and verifies an actual content-addressed inline search receipt", () => {
  const fixture = makeReceiptFixture();
  const { receipt } = fixture;

  assert.equal(verifyPublicAuthorityContext(receipt.authority_context), true);
  assert.equal(verifyPublicPolicy(fixture.publicPolicy), true);
  assert.equal(verifyPublicPolicyDecision(receipt.policy_decision), true);
  assert.match(receipt.receipt_id, /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u);
  assert.equal(receipt.evidence_handling.delivery, "inline-only");
  assert.equal(receipt.evidence_handling.persistence, "not-persisted");
  assert.equal(receipt.evidence_handling.attestation, "not-attested");
  assert.equal(receipt.verification.canonicalisation, "rfc8785-jcs");
  assert.equal(receipt.result.returned_record_count, 2);
  assert.deepEqual(
    receipt.licence_obligations.map((obligation) => obligation.record_id),
    ["urn:record:\ue000", "urn:record:😀"],
  );
  assert.equal(canonicalJson(receipt).includes("phrase retained only in digest material"), false);

  assert.deepEqual(
    verifyInlineReceipt(receipt, {
      normalisedParameters: fixture.normalisedParameters,
      resultCore: fixture.resultCore,
      publicPolicy: fixture.publicPolicy,
      licenceObligations: receipt.licence_obligations,
      expectedAuthorityContext: fixture.authorityContext,
      expectedPolicyDecision: fixture.policyDecision,
      expectedCatalogue: CATALOGUE,
      expectedSoftware: SOFTWARE,
    }),
    {
      valid: true,
      checks: [
        "authority-context",
        "catalogue-integrity",
        "licence-obligations",
        "normalised-parameters-digest",
        "public-policy-decision",
        "result-core-digest",
        "schema",
      ],
      errors: [],
    },
  );
});

test("is deterministic for insertion-order-equivalent parameter and result material", () => {
  const first = makeReceiptBuildInput();
  const firstReceipt = buildInlineReceipt(first);
  const reorderedResult = {
    data: (first.resultCore as Record<string, unknown>).data,
    warnings: [],
    catalogue: CATALOGUE,
    trace_id: TRACE_ID,
    request_id: REQUEST_ID,
    operation: "catalogue.search",
    schema: "gis-ai-go.catalogue-result.v1",
  };
  const secondReceipt = buildInlineReceipt({
    ...first,
    normalisedParameters: {
      cursor: null,
      limit: 20,
      facets: { types: ["dataset"] },
      query: "phrase retained only in digest material",
    },
    resultCore: reorderedResult,
  });

  assert.equal(firstReceipt.receipt_id, secondReceipt.receipt_id);
  assert.equal(firstReceipt.result.sha256, secondReceipt.result.sha256);
  assert.equal(
    firstReceipt.operation.normalised_parameters.sha256,
    secondReceipt.operation.normalised_parameters.sha256,
  );
});

test("builds and verifies a catalogue description receipt", () => {
  const authorityContext = makeAuthorityContext();
  const publicPolicy = makePublicPolicy();
  const policyDecision = buildPublicPolicyDecision({
    schema: "gis-ai-go.public-policy-decision.v1",
    canonicalisation: CANONICALISATION,
    request_id: REQUEST_ID,
    trace_id: TRACE_ID,
    authority_context_id: authorityContext.context_id,
    policy_id: publicPolicy.policy_id,
    policy_version: publicPolicy.version,
    policy_default_effect: "deny",
    operation: "catalogue.describe",
    effect: "allow-with-obligations",
    reason_code: "public-catalogue-read-allowed",
    obligations: PUBLIC_POLICY_OBLIGATIONS,
  });
  const resultCore = {
    schema: "gis-ai-go.catalogue-result.v1",
    operation: "catalogue.describe",
    request_id: REQUEST_ID,
    trace_id: TRACE_ID,
    catalogue: CATALOGUE,
    warnings: [],
    data: {
      record: {
        id: "urn:record:one",
        type: "dataset",
        title: "One",
        description: "A complete synthetic record.",
        authority: {
          class: "project-authoritative",
          statement: "The project is authoritative for this synthetic record.",
          source: "README.md",
        },
        publication: {
          classification: "public",
          contains_personal_data: false,
          contains_protected_data: false,
        },
        access: {
          tier: "open",
          state: "public-metadata",
          authentication: "None",
        },
        rights: {
          state: "project-mit",
          record_licence: "MIT",
          described_resource_licence: "Open Government Licence v3.0",
          attribution: "Example publisher",
        },
        freshness: {
          observed_at: "2026-08-20T00:00:00Z",
          reviewed_at: "2026-08-20T00:00:00Z",
          stale_after: "2027-02-20T00:00:00Z",
          status: "current",
        },
        status: "candidate",
        source_refs: ["urn:record:source"],
        limitations: ["Synthetic fixture only."],
        tags: ["synthetic"],
        details: { fixture: true },
      },
      included: {
        relationships: [{ relation: "source", record_id: "urn:record:relationship-only" }],
        sources: [
          {
            id: "urn:record:source",
            title: "Source",
            authority: "source-authoritative",
            access: "public",
            rights: "open-with-conditions",
            freshness: "current",
          },
        ],
      },
    },
  };
  const licenceObligations = [
    {
      record_id: "urn:record:one",
      record_licence: "MIT",
      described_resource_licence: "Open Government Licence v3.0",
      attribution: "Example publisher",
    },
    {
      record_id: "urn:record:source",
      record_licence: "MIT",
      described_resource_licence: "Open Government Licence v3.0",
      attribution: "Source publisher",
    },
  ] as const;
  const buildInput: InlineReceiptBuildInput = {
    createdAt: "2026-08-20T07:00:00+01:00",
    requestId: REQUEST_ID,
    traceId: TRACE_ID,
    operation: "catalogue.describe",
    normalisedParameters: { record_id: "urn:record:one", include: [] },
    authorityContext,
    publicPolicy,
    policyDecision,
    catalogue: CATALOGUE,
    transformations: [
      { name: "load-checksum-verified-catalogue", version: "v1" },
      { name: "normalise-parameters", version: "v1" },
      { name: "project-result-core", version: "v1" },
    ],
    software: SOFTWARE,
    resultCore,
    licenceObligations,
  };
  const receipt = buildInlineReceipt(buildInput);

  assert.equal(
    verifyInlineReceipt(receipt, {
      normalisedParameters: { include: [], record_id: "urn:record:one" },
      resultCore,
      publicPolicy,
      licenceObligations,
    }).valid,
    true,
  );

  const excessiveSourceRefs = mutable(resultCore);
  excessiveSourceRefs.data.record.source_refs = Array.from(
    { length: 100 },
    (_, index) => `urn:record:source:${index}`,
  );
  assert.throws(
    () => buildInlineReceipt({ ...buildInput, resultCore: excessiveSourceRefs }),
    /source_refs.*1 to 99 items/u,
  );

  const readdressedReceipt = mutable(receipt) as unknown as Record<string, unknown>;
  (readdressedReceipt.result as Record<string, unknown>).sha256 = domainSeparatedSha256(
    CANONICAL_DOMAINS.catalogueResultCore,
    excessiveSourceRefs,
  );
  readdress(
    readdressedReceipt,
    "receipt_id",
    "gis-ai-go:evidence-receipt",
    CANONICAL_DOMAINS.evidenceReceipt,
  );
  const verification = verifyInlineReceipt(readdressedReceipt, {
    normalisedParameters: buildInput.normalisedParameters,
    resultCore: excessiveSourceRefs,
    publicPolicy,
    licenceObligations,
  });
  assert.equal(verification.valid, false);
  assert.match(verification.errors.join("\n"), /source_refs.*1 to 99 items/u);
  assert.equal(receipt.result.returned_record_count, 2);
  assert.equal(
    receipt.licence_obligations.some(
      (obligation) => obligation.record_id === "urn:record:relationship-only",
    ),
    false,
  );
});

test("supports a content-addressed default-deny policy decision", () => {
  const authority = makeAuthorityContext();
  const policy = makePublicPolicy();
  const core: PublicPolicyDecisionCore = {
    schema: "gis-ai-go.public-policy-decision.v1",
    canonicalisation: CANONICALISATION,
    request_id: REQUEST_ID,
    trace_id: TRACE_ID,
    authority_context_id: authority.context_id,
    policy_id: policy.policy_id,
    policy_version: policy.version,
    policy_default_effect: "deny",
    operation: "data.query",
    effect: "deny",
    reason_code: "operation-not-allowed",
    obligations: [],
  };
  const decision = buildPublicPolicyDecision(core);
  assert.equal(verifyPublicPolicyDecision(decision), true);
  assert.throws(
    () =>
      buildPublicPolicyDecision({
        ...core,
        effect: "allow-with-obligations",
        reason_code: "public-catalogue-read-allowed",
        obligations: PUBLIC_POLICY_OBLIGATIONS,
      }),
    /allow decision is limited/u,
  );
});

test("fails verification on parameter, result and receipt tampering", () => {
  const fixture = makeReceiptFixture();
  const baseMaterial = {
    normalisedParameters: fixture.normalisedParameters,
    resultCore: fixture.resultCore,
    publicPolicy: fixture.publicPolicy,
    licenceObligations: fixture.receipt.licence_obligations,
  };

  assert.equal(
    verifyInlineReceipt(fixture.receipt, {
      ...baseMaterial,
      normalisedParameters: { ...fixture.normalisedParameters, limit: 21 },
    }).valid,
    false,
  );
  assert.equal(
    verifyInlineReceipt(fixture.receipt, {
      ...baseMaterial,
      resultCore: { ...fixture.resultCore, warnings: ["tampered"] },
    }).valid,
    false,
  );
  assert.equal(
    verifyInlineReceipt(fixture.receipt, {
      ...baseMaterial,
      licenceObligations: fixture.receipt.licence_obligations.map((obligation, index) =>
        index === 0 ? { ...obligation, attribution: "tampered attribution" } : obligation,
      ),
    }).valid,
    false,
  );
  const tamperedReceipt = mutable(fixture.receipt) as unknown as Record<string, unknown>;
  (tamperedReceipt.result as Record<string, unknown>).sha256 = "0".repeat(64);
  assert.equal(verifyInlineReceipt(tamperedReceipt, baseMaterial).valid, false);
});

test("rejects forbidden semantics even when an attacker recomputes every affected identity", () => {
  const fixture = makeReceiptFixture();
  const hostile = mutable(fixture.receipt) as unknown as Record<string, unknown>;
  const authority = hostile.authority_context as Record<string, unknown>;
  (authority.construction as Record<string, unknown>).unexpected = "forbidden";
  readdress(
    authority,
    "context_id",
    "gis-ai-go:public-authority-context",
    CANONICAL_DOMAINS.authorityContext,
  );
  const decision = hostile.policy_decision as Record<string, unknown>;
  decision.authority_context_id = authority.context_id;
  readdress(
    decision,
    "decision_id",
    "gis-ai-go:public-policy-decision",
    CANONICAL_DOMAINS.publicPolicyDecision,
  );
  readdress(hostile, "receipt_id", "gis-ai-go:evidence-receipt", CANONICAL_DOMAINS.evidenceReceipt);

  const verification = verifyInlineReceipt(hostile, {
    normalisedParameters: fixture.normalisedParameters,
    resultCore: fixture.resultCore,
    publicPolicy: fixture.publicPolicy,
    licenceObligations: fixture.receipt.licence_obligations,
  });
  assert.equal(verification.valid, false);
  assert.match(verification.errors[0] ?? "", /unexpected or missing property/u);

  const persisted = mutable(fixture.receipt) as unknown as Record<string, unknown>;
  (persisted.evidence_handling as Record<string, unknown>).persistence = "persisted";
  readdress(persisted, "receipt_id", "gis-ai-go:evidence-receipt", CANONICAL_DOMAINS.evidenceReceipt);
  assert.equal(
    verifyInlineReceipt(persisted, {
      normalisedParameters: fixture.normalisedParameters,
      resultCore: fixture.resultCore,
      publicPolicy: fixture.publicPolicy,
      licenceObligations: fixture.receipt.licence_obligations,
    }).valid,
    false,
  );
});

test("rejects malformed runtime-cast builders and invalid normalised calendar dates", () => {
  const validAuthority = makeAuthorityContext();
  const { context_id: _contextId, ...authorityCore } = validAuthority;
  const extraAuthority = mutable(authorityCore) as PublicAuthorityContextCore & { unexpected: true };
  extraAuthority.unexpected = true;
  assert.throws(
    () => buildPublicAuthorityContext(extraAuthority as PublicAuthorityContextCore),
    /unexpected or missing property/u,
  );

  const input = makeReceiptBuildInput();
  assert.throws(
    () => buildInlineReceipt({ ...input, createdAt: "2026-02-31T07:00:00Z" }),
    /real calendar date/u,
  );
  assert.throws(
    () => buildInlineReceipt({ ...input, createdAt: "2026-08-20T24:00:00Z" }),
    /bounded time components/u,
  );
  assert.doesNotThrow(() =>
    buildInlineReceipt({ ...input, createdAt: "2026-08-20T07:00:00.123456789+01:30" }),
  );
  assert.doesNotThrow(() =>
    buildInlineReceipt({ ...input, createdAt: "1990-12-31T15:59:60-08:00" }),
  );

  const duplicate = input.licenceObligations[0]!;
  assert.throws(
    () => buildInlineReceipt({ ...input, licenceObligations: [duplicate, duplicate] }),
    /record only once/u,
  );
  const wrongCoverage: InlineReceiptBuildInput = {
    ...input,
    licenceObligations: [
      {
        ...duplicate,
        record_id: "urn:record:not-returned",
      },
      input.licenceObligations[1]!,
    ],
  };
  assert.throws(() => buildInlineReceipt(wrongCoverage), /cover each returned record/u);
});

test("snapshots build and verification wrappers without invoking accessors or proxies", () => {
  const input = makeReceiptBuildInput();
  let operationReads = 0;
  const stateful = { ...input } as Record<string, unknown>;
  Object.defineProperty(stateful, "operation", {
    enumerable: true,
    get: () => {
      operationReads += 1;
      return operationReads < 4 ? "catalogue.search" : "catalogue.describe";
    },
  });
  assert.throws(
    () => buildInlineReceipt(stateful as unknown as InlineReceiptBuildInput),
    /accessor properties are not supported/u,
  );
  assert.equal(operationReads, 0);
  assert.throws(
    () => buildInlineReceipt(new Proxy(input, {}) as InlineReceiptBuildInput),
    /proxy objects are not supported/u,
  );
  assert.throws(
    () =>
      buildInlineReceipt({
        ...input,
        rawQuery: "must not be accepted on the wrapper",
      } as unknown as InlineReceiptBuildInput),
    /unexpected or missing property/u,
  );

  const receipt = buildInlineReceipt(input);
  let resultReads = 0;
  const material = {
    normalisedParameters: input.normalisedParameters,
    resultCore: input.resultCore,
    publicPolicy: input.publicPolicy,
    licenceObligations: input.licenceObligations,
  } as Record<string, unknown>;
  Object.defineProperty(material, "resultCore", {
    enumerable: true,
    get: () => {
      resultReads += 1;
      return input.resultCore;
    },
  });
  assert.equal(
    verifyInlineReceipt(receipt, material as unknown as Parameters<typeof verifyInlineReceipt>[1])
      .valid,
    false,
  );
  assert.equal(resultReads, 0);
});

test("rejects schema-invalid result cores and false transformation provenance", () => {
  const input = makeReceiptBuildInput();
  const resultCore = mutable(input.resultCore) as Record<string, unknown>;
  assert.throws(
    () => buildInlineReceipt({ ...input, resultCore: { ...resultCore, unexpected: true } }),
    /unexpected or missing property/u,
  );

  const withoutWarnings = mutable(resultCore);
  delete withoutWarnings.warnings;
  assert.throws(
    () => buildInlineReceipt({ ...input, resultCore: withoutWarnings }),
    /unexpected or missing property/u,
  );

  const missingRecordField = mutable(resultCore);
  const missingRecordData = missingRecordField.data as Record<string, unknown>;
  const missingRecords = missingRecordData.records as Record<string, unknown>[];
  delete missingRecords[0]!.description;
  assert.throws(
    () => buildInlineReceipt({ ...input, resultCore: missingRecordField }),
    /unexpected or missing property/u,
  );

  const incompleteFacets = mutable(resultCore);
  delete ((incompleteFacets.data as Record<string, unknown>).facets as Record<string, unknown>).tags;
  assert.throws(
    () => buildInlineReceipt({ ...input, resultCore: incompleteFacets }),
    /unexpected or missing property/u,
  );

  const incompletePage = mutable(resultCore);
  delete ((incompletePage.data as Record<string, unknown>).page as Record<string, unknown>).matched;
  assert.throws(
    () => buildInlineReceipt({ ...input, resultCore: incompletePage }),
    /unexpected or missing property/u,
  );

  const overLimitPage = mutable(resultCore);
  ((overLimitPage.data as Record<string, unknown>).page as Record<string, unknown>).limit = 1;
  assert.throws(
    () => buildInlineReceipt({ ...input, resultCore: overLimitPage }),
    /limit, returned and matched counts must agree/u,
  );

  const duplicateFacetValue = mutable(resultCore);
  (((duplicateFacetValue.data as Record<string, unknown>).facets as Record<string, unknown>)
    .types as unknown[]) = [
    { value: "dataset", count: 1 },
    { value: "dataset", count: 2 },
  ];
  assert.throws(
    () => buildInlineReceipt({ ...input, resultCore: duplicateFacetValue }),
    /facet values must be unique/u,
  );

  assert.throws(
    () =>
      buildInlineReceipt({
        ...input,
        transformations: [{ name: "filter-catalogue", version: "v1" }],
      }),
    /exact ordered catalogue.search transformation pipeline/u,
  );

  const fixture = makeReceiptFixture();
  const readdressed = mutable(fixture.receipt) as unknown as Record<string, unknown>;
  (readdressed.transformations as unknown[]).reverse();
  readdress(
    readdressed,
    "receipt_id",
    "gis-ai-go:evidence-receipt",
    CANONICAL_DOMAINS.evidenceReceipt,
  );
  assert.equal(
    verifyInlineReceipt(readdressed, {
      normalisedParameters: fixture.normalisedParameters,
      resultCore: fixture.resultCore,
      publicPolicy: fixture.publicPolicy,
      licenceObligations: fixture.receipt.licence_obligations,
    }).valid,
    false,
  );
});

test("rejects a re-addressed public policy with schema-forbidden content", () => {
  const fixture = makeReceiptFixture();
  const hostilePolicy = mutable(fixture.publicPolicy) as unknown as Record<string, unknown>;
  (hostilePolicy.compilation as Record<string, unknown>).command = "untrusted";
  readdress(hostilePolicy, "policy_id", "gis-ai-go:public-policy", CANONICAL_DOMAINS.publicPolicy);
  assert.equal(verifyPublicPolicy(hostilePolicy), false);
  assert.equal(
    verifyInlineReceipt(fixture.receipt, {
      normalisedParameters: fixture.normalisedParameters,
      resultCore: fixture.resultCore,
      publicPolicy: hostilePolicy as unknown as PublicPolicy,
      licenceObligations: fixture.receipt.licence_obligations,
    }).valid,
    false,
  );
});
