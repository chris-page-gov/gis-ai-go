import {
  CANONICALISATION,
  PUBLIC_POLICY_OBLIGATIONS,
  buildInlineReceipt,
  buildPublicAuthorityContext,
  buildPublicPolicy,
  buildPublicPolicyDecision,
  type CatalogueIdentity,
  type EvidenceSoftwareIdentity,
  type InlineEvidenceReceipt,
  type InlineReceiptBuildInput,
  type PublicAuthorityContext,
  type PublicPolicy,
  type PublicPolicyDecision,
  type RecordLicenceObligation,
} from "../src/index.js";

export const REQUEST_ID = "request-fixture-1";
export const TRACE_ID = "0123456789abcdef0123456789abcdef";

export const CATALOGUE: CatalogueIdentity = Object.freeze({
  id: "urn:gis-ai-go:okf:public-catalogue",
  version: "0.1.0",
  revision: "4948890c10adb4f0ac6f427cda21cb0c0c4607dd",
  content_root_sha256: "57bfb5a190424289ea09b7eb0729ecdad08292ec7cb8abed148ddf29c9f975d1",
  record_count: 36,
  reviewed_at: "2026-08-20T06:00:00Z",
  stale_after: "2026-11-20T06:00:00Z",
});

export const SOFTWARE: EvidenceSoftwareIdentity = Object.freeze({
  name: "gis-ai-go-mcp-gateway",
  version: "0.1.0",
  revision: "4948890c10adb4f0ac6f427cda21cb0c0c4607dd",
});

export function makeAuthorityContext(): PublicAuthorityContext {
  return buildPublicAuthorityContext({
    schema: "gis-ai-go.public-authority-context.v1",
    canonicalisation: CANONICALISATION,
    construction: {
      source: "server",
      profile: "anonymous-open",
      product: "gis-ai-go-gateway",
    },
    access: {
      authentication: "none",
      tier: "open",
      publication_classification: "public",
      contains_personal_data: false,
      contains_protected_data: false,
      read_only: true,
    },
    permitted_operations: ["catalogue.describe", "catalogue.search"],
    evidence: {
      receipt: "inline-required",
      persistence: "not-persisted",
      attestation: "not-attested",
    },
  });
}

export function makePublicPolicy(): PublicPolicy {
  return buildPublicPolicy({
    schema: "gis-ai-go.public-policy.v1",
    version: "1.0.0",
    canonicalisation: CANONICALISATION,
    compilation: {
      kind: "compiled-json",
      runtime: "gis-ai-go-gateway",
    },
    default_effect: "deny",
    applies_to: {
      authority_profile: "anonymous-open",
      access_tier: "open",
      publication_classification: "public",
      contains_personal_data: false,
      contains_protected_data: false,
      read_only: true,
    },
    rules: [
      {
        rule_id: "public-catalogue-describe",
        operation: "catalogue.describe",
        effect: "allow-with-obligations",
        obligations: PUBLIC_POLICY_OBLIGATIONS,
      },
      {
        rule_id: "public-catalogue-search",
        operation: "catalogue.search",
        effect: "allow-with-obligations",
        obligations: PUBLIC_POLICY_OBLIGATIONS,
      },
    ],
  });
}

export function makePolicyDecision(
  authorityContext = makeAuthorityContext(),
  publicPolicy = makePublicPolicy(),
): PublicPolicyDecision {
  return buildPublicPolicyDecision({
    schema: "gis-ai-go.public-policy-decision.v1",
    canonicalisation: CANONICALISATION,
    request_id: REQUEST_ID,
    trace_id: TRACE_ID,
    authority_context_id: authorityContext.context_id,
    policy_id: publicPolicy.policy_id,
    policy_version: publicPolicy.version,
    policy_default_effect: "deny",
    operation: "catalogue.search",
    effect: "allow-with-obligations",
    reason_code: "public-catalogue-read-allowed",
    obligations: PUBLIC_POLICY_OBLIGATIONS,
  });
}

export function makeResultCore(): Record<string, unknown> {
  return {
    schema: "gis-ai-go.catalogue-result.v1",
    operation: "catalogue.search",
    request_id: REQUEST_ID,
    trace_id: TRACE_ID,
    catalogue: CATALOGUE,
    warnings: [],
    data: {
      records: [
        {
          id: "urn:record:😀",
          type: "dataset",
          title: "Supplementary-plane record",
          description: "A public synthetic record.",
          authority: "project-authoritative",
          access: "public-metadata",
          rights: "project-mit",
          freshness: "current",
          status: "candidate",
          tags: ["synthetic"],
        },
        {
          id: "urn:record:\ue000",
          type: "source",
          title: "Private-use record",
          description: "A second public synthetic record.",
          authority: "source-authoritative",
          access: "public",
          rights: "open-with-conditions",
          freshness: "review-required",
          status: "external-source",
          tags: [],
        },
      ],
      facets: {
        types: [],
        authority: [],
        access: [],
        rights: [],
        freshness: [],
        tags: [],
      },
      page: {
        limit: 20,
        returned: 2,
        matched: 2,
        next_cursor: null,
      },
    },
  };
}

export const LICENCE_OBLIGATIONS: readonly RecordLicenceObligation[] = Object.freeze([
  Object.freeze({
    record_id: "urn:record:😀",
    record_licence: "MIT",
    described_resource_licence: "Open Government Licence v3.0",
    attribution: "Supplementary-plane publisher",
  }),
  Object.freeze({
    record_id: "urn:record:\ue000",
    record_licence: "MIT",
    described_resource_licence: "Open Government Licence v3.0",
    attribution: "Private-use publisher",
  }),
]);

export interface ReceiptFixture {
  readonly receipt: InlineEvidenceReceipt;
  readonly authorityContext: PublicAuthorityContext;
  readonly publicPolicy: PublicPolicy;
  readonly policyDecision: PublicPolicyDecision;
  readonly normalisedParameters: Record<string, unknown>;
  readonly resultCore: Record<string, unknown>;
}

export function makeReceiptBuildInput(): InlineReceiptBuildInput {
  const authorityContext = makeAuthorityContext();
  const publicPolicy = makePublicPolicy();
  const policyDecision = makePolicyDecision(authorityContext, publicPolicy);
  const normalisedParameters = {
    query: "phrase retained only in digest material",
    facets: { types: ["dataset"] },
    limit: 20,
    cursor: null,
  };
  const resultCore = makeResultCore();
  return {
    createdAt: "2026-08-20T07:00:00Z",
    requestId: REQUEST_ID,
    traceId: TRACE_ID,
    operation: "catalogue.search",
    normalisedParameters,
    authorityContext,
    publicPolicy,
    policyDecision,
    catalogue: CATALOGUE,
    transformations: [
      { name: "load-checksum-verified-catalogue", version: "v1" },
      { name: "normalise-parameters", version: "v1" },
      { name: "filter-catalogue", version: "v1" },
      { name: "project-result-core", version: "v1" },
    ],
    software: SOFTWARE,
    resultCore,
    licenceObligations: LICENCE_OBLIGATIONS,
  };
}

export function makeReceiptFixture(): ReceiptFixture {
  const input = makeReceiptBuildInput();
  const receipt = buildInlineReceipt(input);
  const {
    authorityContext,
    publicPolicy,
    policyDecision,
    normalisedParameters,
    resultCore,
  } = input;
  return {
    receipt,
    authorityContext,
    publicPolicy,
    policyDecision,
    normalisedParameters: normalisedParameters as Record<string, unknown>,
    resultCore: resultCore as Record<string, unknown>,
  };
}
