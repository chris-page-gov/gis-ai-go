import {
  CANONICALISATION,
  DATA_QUERY_OBLIGATIONS,
  PUBLIC_READ_ONS_RESOURCE,
  SELECTION_RESOLVE_OBLIGATIONS,
  buildPublicReadAuthorityContext,
  buildPublicReadPolicy,
  buildPublicReadPolicyDecision,
  buildPublicReadReceipt,
  publicReadResultEvidenceBinding,
  type PublicReadOperation,
  type PublicReadReceiptBuildInput,
  type PublicReadReceiptVerificationMaterial,
} from "../src/index.js";

export const PUBLIC_READ_REQUEST_ID = "request-public-read-fixture-1";
export const PUBLIC_READ_TRACE_ID = "1123456789abcdef0123456789abcdef";

export function makePublicReadAuthorityContext() {
  return buildPublicReadAuthorityContext({
    schema: "gis-ai-go.public-authority-context.v2",
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
    permitted_operations: ["data.query", "selection.resolve"],
    evidence: {
      receipt: "inline-required",
      persistence: "not-persisted",
      attestation: "not-attested",
    },
  });
}

export function makePublicReadPolicy() {
  return buildPublicReadPolicy({
    schema: "gis-ai-go.public-policy.v2",
    version: "2.0.0",
    canonicalisation: CANONICALISATION,
    compilation: { kind: "compiled-json", runtime: "gis-ai-go-gateway" },
    default_effect: "deny",
    applies_to: {
      authority_profile: "anonymous-open",
      access_tier: "open",
      publication_classification: "public",
      contains_personal_data: false,
      contains_protected_data: false,
      read_only: true,
    },
    resources: [PUBLIC_READ_ONS_RESOURCE],
    rules: [
      {
        rule_id: "public-data-query-ons-v121",
        operation: "data.query",
        resource_id: PUBLIC_READ_ONS_RESOURCE.resource_id,
        effect: "allow-with-obligations",
        obligations: DATA_QUERY_OBLIGATIONS,
      },
      {
        rule_id: "public-selection-resolve-ons-v121",
        operation: "selection.resolve",
        resource_id: PUBLIC_READ_ONS_RESOURCE.resource_id,
        effect: "allow-with-obligations",
        obligations: SELECTION_RESOLVE_OBLIGATIONS,
      },
    ],
  });
}

function normalisedParameters(operation: PublicReadOperation): Record<string, unknown> {
  if (operation === "selection.resolve") {
    return {
      schema: "gis-ai-go.selection-resolve-parameters.v1",
      profile_id: PUBLIC_READ_ONS_RESOURCE.profile.id,
      provider_id: PUBLIC_READ_ONS_RESOURCE.provider.id,
      dataset: {
        id: PUBLIC_READ_ONS_RESOURCE.dataset.id,
        edition: PUBLIC_READ_ONS_RESOURCE.dataset.edition,
        version: PUBLIC_READ_ONS_RESOURCE.dataset.version,
      },
      selections: PUBLIC_READ_ONS_RESOURCE.selections,
    };
  }
  return {
    schema: "gis-ai-go.data-query-parameters.v1",
    resource_id: PUBLIC_READ_ONS_RESOURCE.resource_id,
    dataset: {
      id: PUBLIC_READ_ONS_RESOURCE.dataset.id,
      edition: PUBLIC_READ_ONS_RESOURCE.dataset.edition,
      version: PUBLIC_READ_ONS_RESOURCE.dataset.version,
    },
    selections: PUBLIC_READ_ONS_RESOURCE.selections,
    limit: 1,
  };
}

function resultCore(
  operation: PublicReadOperation,
  requestId: string,
  traceId: string,
): Record<string, unknown> {
  return {
    schema:
      operation === "data.query"
        ? "gis-ai-go.data-query-result.v1"
        : "gis-ai-go.selection-resolve-result.v1",
    operation,
    request_id: requestId,
    trace_id: traceId,
    evidence_binding: publicReadResultEvidenceBinding(),
    data:
      operation === "data.query"
        ? {
            status: "succeeded",
            observations: [
              { value: "raw-observation-value-should-not-appear", unit: "deaths" },
            ],
          }
        : {
            status: "resolved",
            ambiguity: null,
            resource_id: PUBLIC_READ_ONS_RESOURCE.resource_id,
          },
    warnings: [],
  };
}

export function makePublicReadReceiptBuildInput(
  operation: PublicReadOperation = "data.query",
  requestId = PUBLIC_READ_REQUEST_ID,
  traceId = PUBLIC_READ_TRACE_ID,
): PublicReadReceiptBuildInput {
  const authorityContext = makePublicReadAuthorityContext();
  const publicPolicy = makePublicReadPolicy();
  const policyDecision = buildPublicReadPolicyDecision({
    schema: "gis-ai-go.public-policy-decision.v2",
    canonicalisation: CANONICALISATION,
    request_id: requestId,
    trace_id: traceId,
    authority_context_id: authorityContext.context_id,
    policy_id: publicPolicy.policy_id,
    policy_version: "2.0.0",
    policy_default_effect: "deny",
    operation,
    resource_id: PUBLIC_READ_ONS_RESOURCE.resource_id,
    effect: "allow-with-obligations",
    reason_code: "public-read-operation-allowed",
    obligations:
      operation === "data.query"
        ? DATA_QUERY_OBLIGATIONS
        : SELECTION_RESOLVE_OBLIGATIONS,
  });
  return {
    createdAt: "2026-08-20T18:00:00Z",
    requestId,
    traceId,
    operation,
    normalisedParameters: normalisedParameters(operation),
    authorityContext,
    publicPolicy,
    policyDecision,
    resource: PUBLIC_READ_ONS_RESOURCE,
    transformations:
      operation === "data.query"
        ? [
            { name: "normalise-public-read-parameters", version: "v1" },
            { name: "execute-fixed-provider-query", version: "v1" },
            { name: "project-public-read-result-core", version: "v1" },
          ]
        : [
            { name: "normalise-public-read-parameters", version: "v1" },
            { name: "resolve-fixed-selection-profile", version: "v1" },
            { name: "project-public-read-result-core", version: "v1" },
          ],
    software: {
      name: "gis-ai-go-mcp-gateway",
      version: "0.1.0",
      revision: "c4d43f9d0f7af143e01eb3381e5adc4625fac2f0",
    },
    resultCore: resultCore(operation, requestId, traceId),
  };
}

export function makePublicReadReceiptFixture(
  operation: PublicReadOperation = "data.query",
  requestId = PUBLIC_READ_REQUEST_ID,
  traceId = PUBLIC_READ_TRACE_ID,
) {
  const input = makePublicReadReceiptBuildInput(operation, requestId, traceId);
  const receipt = buildPublicReadReceipt(input);
  const material: PublicReadReceiptVerificationMaterial = {
    normalisedParameters: input.normalisedParameters,
    resultCore: input.resultCore,
    publicPolicy: input.publicPolicy,
    expectedAuthorityContext: input.authorityContext,
    expectedPolicyDecision: input.policyDecision,
    expectedResource: input.resource,
    expectedSoftware: input.software,
  };
  return { input, receipt, material };
}
