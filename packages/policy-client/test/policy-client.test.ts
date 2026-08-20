import assert from "node:assert/strict";
import test from "node:test";

import type { CatalogueBundle } from "@gis-ai-go/contracts";
import {
  PUBLIC_POLICY_OBLIGATIONS,
  canonicalJson,
  verifyPublicPolicy,
  verifyPublicPolicyDecision,
} from "@gis-ai-go/evidence";

import {
  PUBLIC_CATALOGUE_POLICY,
  PublicPolicyInputError,
  evaluatePublicCataloguePolicy,
  isPublicCatalogueBoundary,
} from "../src/index.js";

const REQUEST_ID = "request-public-catalogue-001";
const TRACE_ID = "0123456789abcdef0123456789abcdef";

function publicCatalogue(): CatalogueBundle {
  return {
    schema: "gis-ai-go-okf-bundle.v1",
    id: "https://example.gov.uk/id/bundle/public",
    title: "Public catalogue",
    description: "A bounded public metadata catalogue.",
    okfVersion: "0.2",
    profile: "https://example.gov.uk/profile/public/v1/",
    profileStatus: "candidate-pending-consumer-acceptance",
    version: "0.0.0",
    revision: "0123456789abcdef0123456789abcdef01234567",
    status: "candidate",
    authority: {
      bundleAuthority: "Metadata publication only.",
      officialSourceAuthority: "The named source publisher.",
      legalAdvice: false,
      notEndorsedBySource: true,
    },
    scope: {
      kind: "bounded-public-metadata-discovery",
      metadataOnly: true,
      containsProtectedData: false,
      excludes: ["Protected data."],
    },
    rights: {
      statement: "Third-party records retain their terms.",
      thirdPartyNotices: "THIRD_PARTY.md",
    },
    observedAt: "2026-08-19T00:00:00Z",
    reviewedAt: "2026-08-19T00:00:00Z",
    staleAfter: "2026-11-19T00:00:00Z",
    recordCount: 1,
    records: [
      {
        schema: "gis-ai-go-okf-concept.v1",
        id: "dataset:public",
        type: "dataset",
        title: "Public dataset metadata",
        description: "Public metadata only.",
        authority: {
          class: "source-authoritative",
          statement: "The source publisher is authoritative.",
          source: "https://example.gov.uk/dataset",
        },
        publication: {
          classification: "public",
          containsPersonalData: false,
          containsProtectedData: false,
        },
        access: { tier: "open", state: "public", authentication: "None." },
        rights: {
          state: "open-with-conditions",
          recordLicence: "CC BY 4.0.",
          describedResourceLicence: "Source terms.",
          attribution: "Example publisher.",
        },
        freshness: {
          observedAt: "2026-08-19T00:00:00Z",
          reviewedAt: "2026-08-19T00:00:00Z",
          staleAfter: "2026-11-19T00:00:00Z",
          status: "current",
        },
        status: "candidate-metadata",
        sourceRefs: ["dataset:public"],
        limitations: ["This is public metadata only."],
        tags: ["public"],
        details: {},
      },
    ],
  };
}

test("loads the exact checked-in default-deny policy with a verified content identity", () => {
  assert.equal(verifyPublicPolicy(PUBLIC_CATALOGUE_POLICY), true);
  assert.equal(
    PUBLIC_CATALOGUE_POLICY.policy_id,
    "gis-ai-go:public-policy:sha256:f39abe3f35f910dd27c9af9296bbccba33f76fec6d8d6acbba7c3b846d9a1e8f",
  );
  assert.equal(PUBLIC_CATALOGUE_POLICY.default_effect, "deny");
  assert.deepEqual(
    PUBLIC_CATALOGUE_POLICY.rules.map((rule) => rule.operation),
    ["catalogue.describe", "catalogue.search"],
  );
  assert.equal(Object.isFrozen(PUBLIC_CATALOGUE_POLICY.rules), true);

  const tampered = structuredClone(PUBLIC_CATALOGUE_POLICY);
  (tampered as unknown as { version: string }).version = "1.0.1";
  assert.equal(verifyPublicPolicy(tampered), false);
});

test("allows only search and describe with exact evidence obligations", () => {
  const catalogue = publicCatalogue();
  assert.equal(isPublicCatalogueBoundary(catalogue), true);

  for (const operation of ["catalogue.search", "catalogue.describe"] as const) {
    const evaluation = evaluatePublicCataloguePolicy({
      requestId: REQUEST_ID,
      traceId: TRACE_ID,
      operation,
      catalogue,
    });
    assert.equal(evaluation.allowed, true);
    assert.equal(evaluation.effect, "allow-with-obligations");
    assert.equal(evaluation.reasonCode, "public-catalogue-read-allowed");
    assert.ok(evaluation.decision);
    assert.equal(verifyPublicPolicyDecision(evaluation.decision), true);
    assert.deepEqual(evaluation.decision.obligations, PUBLIC_POLICY_OBLIGATIONS);
    assert.equal(evaluation.decision.policy_id, PUBLIC_CATALOGUE_POLICY.policy_id);
    assert.equal(evaluation.authorityContext.construction.source, "server");
  }
});

test("returns explicit default-deny outcomes for governed and unknown operations", () => {
  const governed = evaluatePublicCataloguePolicy({
    requestId: REQUEST_ID,
    traceId: TRACE_ID,
    operation: "data.query",
    catalogue: publicCatalogue(),
  });
  assert.equal(governed.allowed, false);
  assert.equal(governed.effect, "deny");
  assert.equal(governed.reasonCode, "operation-not-allowed");
  assert.ok(governed.decision);
  assert.equal(governed.decision.effect, "deny");
  assert.deepEqual(governed.decision.obligations, []);
  assert.equal(verifyPublicPolicyDecision(governed.decision), true);

  const unknown = evaluatePublicCataloguePolicy({
    requestId: REQUEST_ID,
    traceId: TRACE_ID,
    operation: "catalogue.delete",
    catalogue: publicCatalogue(),
  });
  assert.equal(unknown.allowed, false);
  assert.equal(unknown.effect, "deny");
  assert.equal(unknown.reasonCode, "operation-not-allowed");
  assert.equal(unknown.decision, null);
});

test("denies any catalogue that crosses the public metadata boundary", () => {
  const mutations: Array<(catalogue: CatalogueBundle) => void> = [
    (catalogue) => {
      (catalogue.scope as { metadataOnly: boolean }).metadataOnly = false;
    },
    (catalogue) => {
      (catalogue.scope as { containsProtectedData: boolean }).containsProtectedData = true;
    },
    (catalogue) => {
      (catalogue.records[0]!.publication as { classification: string }).classification = "private";
    },
    (catalogue) => {
      (catalogue.records[0]!.publication as { containsPersonalData: boolean }).containsPersonalData = true;
    },
    (catalogue) => {
      (catalogue.records[0]!.publication as { containsProtectedData: boolean }).containsProtectedData = true;
    },
    (catalogue) => {
      (catalogue.records[0]!.access as { tier: string }).tier = "protected";
    },
  ];

  for (const mutate of mutations) {
    const catalogue = structuredClone(publicCatalogue());
    mutate(catalogue);
    assert.equal(isPublicCatalogueBoundary(catalogue), false);
    const evaluation = evaluatePublicCataloguePolicy({
      requestId: REQUEST_ID,
      traceId: TRACE_ID,
      operation: "catalogue.search",
      catalogue,
    });
    assert.equal(evaluation.allowed, false);
    assert.equal(evaluation.reasonCode, "publication-not-public");
    assert.ok(evaluation.decision);
    assert.equal(evaluation.decision.effect, "deny");
  }
});

test("rejects unbounded or malformed decision identifiers before evaluation", () => {
  assert.throws(
    () =>
      evaluatePublicCataloguePolicy({
        requestId: `request-${"x".repeat(128)}`,
        traceId: TRACE_ID,
        operation: "catalogue.search",
        catalogue: publicCatalogue(),
      }),
    PublicPolicyInputError,
  );
  assert.throws(
    () =>
      evaluatePublicCataloguePolicy({
        requestId: REQUEST_ID,
        traceId: "ABC",
        operation: "catalogue.search",
        catalogue: publicCatalogue(),
      }),
    PublicPolicyInputError,
  );
});

test("policy evaluation is deterministic for the same bounded inputs", () => {
  const input = {
    requestId: REQUEST_ID,
    traceId: TRACE_ID,
    operation: "catalogue.search",
    catalogue: publicCatalogue(),
  } as const;
  const first = evaluatePublicCataloguePolicy(input);
  const second = evaluatePublicCataloguePolicy(input);
  assert.equal(canonicalJson(first), canonicalJson(second));
});
