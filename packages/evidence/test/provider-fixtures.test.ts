import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import {
  PUBLIC_READ_ONS_RESOURCE,
  buildInlineReceipt,
  buildPublicReadReceipt,
  verifyInlineReceipt,
  verifyPublicAuthorityContext,
  verifyPublicPolicy,
  verifyPublicPolicyDecision,
  verifyPublicReadAuthorityContext,
  verifyPublicReadPolicy,
  verifyPublicReadPolicyDecision,
  verifyPublicReadReceipt,
  verifyPublicReadResource,
} from "../src/index.js";
import { makePublicReadReceiptBuildInput } from "./public-read-fixtures.js";

function readJson(relativeUrl: string): unknown {
  return JSON.parse(readFileSync(new URL(relativeUrl, import.meta.url), "utf8")) as unknown;
}

test("published synthetic fixtures have reproducible content identities", () => {
  const authorityContext = readJson(
    "../../../../providers/fixtures/public-authority-context.example.json",
  );
  const policyDecision = readJson(
    "../../../../providers/fixtures/public-policy-decision.example.json",
  );
  const receipt = readJson("../../../../providers/fixtures/evidence-receipt.example.json");
  const publicPolicy = readJson("../../../policy-client/src/public-catalogue-v1.json");

  if (!verifyPublicAuthorityContext(authorityContext)) {
    assert.fail("the public authority fixture must have a valid content identity");
  }
  if (!verifyPublicPolicy(publicPolicy)) {
    assert.fail("the checked-in policy must have a valid content identity");
  }
  if (!verifyPublicPolicyDecision(policyDecision)) {
    assert.fail("the public policy-decision fixture must have a valid content identity");
  }

  const normalisedParameters = {
    query: "inspire",
    facets: {
      types: ["dataset"],
      authority: [],
      access: [],
      rights: [],
      freshness: [],
      tags: [],
    },
    limit: 20,
    offset: 0,
  };
  const catalogue = {
    id: "gis-ai-go:bundle:public-discovery",
    version: "0.1.0",
    revision: "1111111111111111111111111111111111111111",
    content_root_sha256:
      "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
    record_count: 36,
    reviewed_at: "2026-08-20T00:00:00Z",
    stale_after: "2027-02-20T00:00:00Z",
  };
  const resultCore = {
    schema: "gis-ai-go.catalogue-result.v1",
    operation: "catalogue.search",
    request_id: "request-public-catalogue-001",
    trace_id: "0123456789abcdef0123456789abcdef",
    catalogue,
    warnings: [],
    data: {
      records: [
        {
          id: "hmlr:dataset:inspire-index-polygons",
          type: "dataset",
          title: "HM Land Registry INSPIRE index polygons",
          description: "Public discovery metadata with a non-legal boundary caveat.",
          authority: "source-authoritative",
          access: "public-metadata",
          rights: "open-with-conditions",
          freshness: "current",
          status: "candidate-metadata",
          tags: ["hmlr", "boundaries"],
        },
      ],
      facets: {
        types: [{ value: "dataset", count: 1 }],
        authority: [{ value: "source-authoritative", count: 1 }],
        access: [{ value: "public-metadata", count: 1 }],
        rights: [{ value: "open-with-conditions", count: 1 }],
        freshness: [{ value: "current", count: 1 }],
        tags: [{ value: "hmlr", count: 1 }],
      },
      page: { limit: 20, returned: 1, matched: 1, next_cursor: null },
    },
  };
  const licenceObligations = [
    {
      record_id: "hmlr:dataset:inspire-index-polygons",
      record_licence: "MIT",
      described_resource_licence: "Open Government Licence",
      attribution: "Contains HM Land Registry public sector information.",
    },
  ];
  const software = {
    name: "gis-ai-go-mcp-gateway" as const,
    version: "0.1.0",
    revision: "1111111111111111111111111111111111111111",
  };
  const expectedReceipt = buildInlineReceipt({
    createdAt: "2026-08-20T08:00:00Z",
    requestId: "request-public-catalogue-001",
    traceId: "0123456789abcdef0123456789abcdef",
    operation: "catalogue.search",
    normalisedParameters,
    authorityContext,
    publicPolicy,
    policyDecision,
    catalogue,
    transformations: [
      { name: "load-checksum-verified-catalogue", version: "v1" },
      { name: "normalise-parameters", version: "v1" },
      { name: "filter-catalogue", version: "v1" },
      { name: "project-result-core", version: "v1" },
    ],
    software,
    resultCore,
    licenceObligations,
  });

  assert.deepEqual(receipt, expectedReceipt);
  assert.deepEqual(
    verifyInlineReceipt(receipt, {
      normalisedParameters,
      resultCore,
      publicPolicy,
      licenceObligations,
      expectedAuthorityContext: authorityContext,
      expectedPolicyDecision: policyDecision,
      expectedCatalogue: catalogue,
      expectedSoftware: software,
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

test("published public-read fixtures reproduce their v2 identities", () => {
  const resource = readJson("../../../../providers/fixtures/public-read-resource.example.json");
  const authority = readJson(
    "../../../../providers/fixtures/public-authority-context-v2.example.json",
  );
  const decision = readJson(
    "../../../../providers/fixtures/public-policy-decision-v2.example.json",
  );
  const receipt = readJson("../../../../providers/fixtures/evidence-receipt-v2.example.json");
  const policy = readJson("../../../policy-client/src/public-read-v2.json");

  assert.deepEqual(resource, PUBLIC_READ_ONS_RESOURCE);
  assert.equal(verifyPublicReadResource(resource), true);
  assert.equal(verifyPublicReadAuthorityContext(authority), true);
  assert.equal(verifyPublicReadPolicy(policy), true);
  assert.equal(verifyPublicReadPolicyDecision(decision), true);

  const input = makePublicReadReceiptBuildInput("data.query");
  assert.deepEqual(resource, input.resource);
  assert.deepEqual(authority, input.authorityContext);
  assert.deepEqual(decision, input.policyDecision);
  assert.deepEqual(receipt, buildPublicReadReceipt(input));
  assert.equal(
    verifyPublicReadReceipt(receipt, {
      normalisedParameters: input.normalisedParameters,
      resultCore: input.resultCore,
      publicPolicy: input.publicPolicy,
      expectedAuthorityContext: input.authorityContext,
      expectedPolicyDecision: input.policyDecision,
      expectedResource: input.resource,
      expectedSoftware: input.software,
    }).valid,
    true,
  );
});
