import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  CANONICALISATION,
  DATA_QUERY_OBLIGATIONS,
  EVIDENCE_INSPECTION_OBLIGATIONS,
  PUBLIC_POLICY_OBLIGATIONS,
  PUBLIC_READ_ONS_RESOURCE,
  buildInlineReceipt,
  buildPublicAuthorityContext,
  buildPublicPolicy,
  buildPublicPolicyDecision,
  buildPublicReadAuthorityContext,
  buildPublicReadPolicyDecision,
  buildPublicReadReceipt,
  canonicalJson,
  openPublicEvidenceLedger,
  publicReadResultEvidenceBinding,
  verifyEvidenceInspectionPolicy,
  verifyEvidenceInspectionPolicyDecision,
  type StoredPublicEvidence,
} from "@gis-ai-go/evidence";

import {
  PUBLIC_EVIDENCE_INSPECTION_POLICY,
  PUBLIC_READ_POLICY,
  evaluateEvidenceInspectionPolicy,
} from "../src/index.js";

const REQUEST_ID = "request-evidence-inspection-policy-001";
const TRACE_ID = "abcdefabcdefabcdefabcdefabcdefab";
const SOFTWARE = Object.freeze({
  name: "gis-ai-go-mcp-gateway" as const,
  version: "0.1.0",
  revision: "9".repeat(40),
});

function v1ReceiptFixture() {
  const requestId = "request-inspection-policy-v1-source";
  const traceId = "0123456789abcdef0123456789abcdef";
  const authorityContext = buildPublicAuthorityContext({
    schema: "gis-ai-go.public-authority-context.v1",
    canonicalisation: CANONICALISATION,
    construction: { source: "server", profile: "anonymous-open", product: "gis-ai-go-gateway" },
    access: {
      authentication: "none",
      tier: "open",
      publication_classification: "public",
      contains_personal_data: false,
      contains_protected_data: false,
      read_only: true,
    },
    permitted_operations: ["catalogue.describe", "catalogue.search"],
    evidence: { receipt: "inline-required", persistence: "not-persisted", attestation: "not-attested" },
  });
  const publicPolicy = buildPublicPolicy({
    schema: "gis-ai-go.public-policy.v1",
    version: "1.0.0",
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
  const policyDecision = buildPublicPolicyDecision({
    schema: "gis-ai-go.public-policy-decision.v1",
    canonicalisation: CANONICALISATION,
    request_id: requestId,
    trace_id: traceId,
    authority_context_id: authorityContext.context_id,
    policy_id: publicPolicy.policy_id,
    policy_version: publicPolicy.version,
    policy_default_effect: "deny",
    operation: "catalogue.search",
    effect: "allow-with-obligations",
    reason_code: "public-catalogue-read-allowed",
    obligations: PUBLIC_POLICY_OBLIGATIONS,
  });
  const catalogue = {
    id: "urn:gis-ai-go:okf:public-catalogue",
    version: "0.1.0",
    revision: "4".repeat(40),
    content_root_sha256: "5".repeat(64),
    record_count: 36,
    reviewed_at: "2026-08-20T06:00:00Z",
    stale_after: "2026-11-20T06:00:00Z",
  } as const;
  const normalisedParameters = { query: "policy-boundary-fixture", limit: 1, cursor: null };
  const resultCore = {
    schema: "gis-ai-go.catalogue-result.v1",
    operation: "catalogue.search",
    request_id: requestId,
    trace_id: traceId,
    catalogue,
    warnings: [],
    data: {
      records: [],
      facets: { types: [], authority: [], access: [], rights: [], freshness: [], tags: [] },
      page: { limit: 1, returned: 0, matched: 0, next_cursor: null },
    },
  } as const;
  const input = {
    createdAt: "2026-08-20T07:00:00Z",
    requestId,
    traceId,
    operation: "catalogue.search" as const,
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
    ] as const,
    software: SOFTWARE,
    resultCore,
    licenceObligations: [],
  };
  const receipt = buildInlineReceipt(input);
  return {
    receipt,
    material: {
      normalisedParameters,
      resultCore,
      publicPolicy,
      licenceObligations: [],
      expectedAuthorityContext: authorityContext,
      expectedPolicyDecision: policyDecision,
      expectedCatalogue: catalogue,
      expectedSoftware: SOFTWARE,
    },
  };
}

function v2ReceiptFixture() {
  const requestId = "request-inspection-policy-v2-source";
  const traceId = "1123456789abcdef0123456789abcdef";
  const authorityContext = buildPublicReadAuthorityContext({
    schema: "gis-ai-go.public-authority-context.v2",
    canonicalisation: CANONICALISATION,
    construction: { source: "server", profile: "anonymous-open", product: "gis-ai-go-gateway" },
    access: {
      authentication: "none",
      tier: "open",
      publication_classification: "public",
      contains_personal_data: false,
      contains_protected_data: false,
      read_only: true,
    },
    permitted_operations: ["data.query", "selection.resolve"],
    evidence: { receipt: "inline-required", persistence: "not-persisted", attestation: "not-attested" },
  });
  const policyDecision = buildPublicReadPolicyDecision({
    schema: "gis-ai-go.public-policy-decision.v2",
    canonicalisation: CANONICALISATION,
    request_id: requestId,
    trace_id: traceId,
    authority_context_id: authorityContext.context_id,
    policy_id: PUBLIC_READ_POLICY.policy_id,
    policy_version: "2.0.0",
    policy_default_effect: "deny",
    operation: "data.query",
    resource_id: PUBLIC_READ_ONS_RESOURCE.resource_id,
    effect: "allow-with-obligations",
    reason_code: "public-read-operation-allowed",
    obligations: DATA_QUERY_OBLIGATIONS,
  });
  const normalisedParameters = {
    schema: "gis-ai-go.data-query-parameters.v1",
    resource_id: PUBLIC_READ_ONS_RESOURCE.resource_id,
    dataset: {
      id: PUBLIC_READ_ONS_RESOURCE.dataset.id,
      edition: PUBLIC_READ_ONS_RESOURCE.dataset.edition,
      version: PUBLIC_READ_ONS_RESOURCE.dataset.version,
    },
    selections: PUBLIC_READ_ONS_RESOURCE.selections,
    limit: 1,
  } as const;
  const resultCore = {
    schema: "gis-ai-go.data-query-result.v1",
    operation: "data.query",
    request_id: requestId,
    trace_id: traceId,
    evidence_binding: publicReadResultEvidenceBinding(),
    data: {
      status: "succeeded",
      observations: [{ value: "fixture-value-not-retained", unit: "deaths" }],
    },
    warnings: [],
  } as const;
  const input = {
    createdAt: "2026-08-20T18:00:00Z",
    requestId,
    traceId,
    operation: "data.query" as const,
    normalisedParameters,
    authorityContext,
    publicPolicy: PUBLIC_READ_POLICY,
    policyDecision,
    resource: PUBLIC_READ_ONS_RESOURCE,
    transformations: [
      { name: "normalise-public-read-parameters", version: "v1" },
      { name: "execute-fixed-provider-query", version: "v1" },
      { name: "project-public-read-result-core", version: "v1" },
    ] as const,
    software: SOFTWARE,
    resultCore,
  };
  const receipt = buildPublicReadReceipt(input);
  return {
    receipt,
    material: {
      normalisedParameters,
      resultCore,
      publicPolicy: PUBLIC_READ_POLICY,
      expectedAuthorityContext: authorityContext,
      expectedPolicyDecision: policyDecision,
      expectedResource: PUBLIC_READ_ONS_RESOURCE,
      expectedSoftware: SOFTWARE,
    },
  };
}

function inspectedEvidence(version: "v1" | "v2") {
  const root = mkdtempSync(join(tmpdir(), `gis-ai-go-inspection-policy-${version}-`));
  const ledger = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 30,
    now: () => new Date("2026-08-23T09:00:00.000Z"),
  });
  const fixture = version === "v1" ? v1ReceiptFixture() : v2ReceiptFixture();
  const persisted = ledger.persistReceipt(fixture.receipt, fixture.material);
  const restarted = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 30,
    now: () => new Date("2026-08-23T09:00:01.000Z"),
  });
  const inspected = restarted.inspect(fixture.receipt.receipt_id);
  assert.ok(inspected);
  return { root, persisted, inspected, receiptId: fixture.receipt.receipt_id };
}

test("loads the exact default-deny evidence inspection policy", () => {
  assert.equal(verifyEvidenceInspectionPolicy(PUBLIC_EVIDENCE_INSPECTION_POLICY), true);
  assert.equal(
    PUBLIC_EVIDENCE_INSPECTION_POLICY.policy_id,
    "gis-ai-go:public-policy:sha256:fb394e84b427864ba0f7e978aadab0fc7594ea2dcfa8fa0a1ad5463b2400c484",
  );
  assert.equal(PUBLIC_EVIDENCE_INSPECTION_POLICY.default_effect, "deny");
  assert.deepEqual(
    PUBLIC_EVIDENCE_INSPECTION_POLICY.rules[0].obligations,
    EVIDENCE_INSPECTION_OBLIGATIONS,
  );
  const tampered = structuredClone(PUBLIC_EVIDENCE_INSPECTION_POLICY);
  (tampered as { version: string }).version = "3.0.1";
  assert.equal(verifyEvidenceInspectionPolicy(tampered), false);
});

test("allows only exact branded v1 and v2 inspection tuples", () => {
  const fixtures = [inspectedEvidence("v1"), inspectedEvidence("v2")];
  try {
    for (const fixture of fixtures) {
      const input = {
        requestId: REQUEST_ID,
        traceId: TRACE_ID,
        operation: "evidence.inspect",
        verifiedStoredEvidence: fixture.inspected,
      } as const;
      const first = evaluateEvidenceInspectionPolicy(input);
      const second = evaluateEvidenceInspectionPolicy(input);
      assert.equal(first.allowed, true);
      assert.equal(canonicalJson(first), canonicalJson(second));
      assert.equal(first.decision.request_id, REQUEST_ID);
      assert.equal(first.decision.trace_id, TRACE_ID);
      assert.equal(first.decision.inspected_receipt_id, fixture.receiptId);
      assert.deepEqual(first.decision.obligations, EVIDENCE_INSPECTION_OBLIGATIONS);
      assert.equal(verifyEvidenceInspectionPolicyDecision(first.decision), true);

      assert.throws(
        () => evaluateEvidenceInspectionPolicy({ ...input, verifiedStoredEvidence: fixture.persisted }),
        /restart-verified evidence/u,
      );
      assert.throws(
        () => evaluateEvidenceInspectionPolicy({
          ...input,
          verifiedStoredEvidence: structuredClone(fixture.inspected),
        }),
        /restart-verified evidence/u,
      );
    }

    const denied = evaluateEvidenceInspectionPolicy({
      requestId: REQUEST_ID,
      traceId: TRACE_ID,
      operation: "catalogue.search",
      verifiedStoredEvidence: fixtures[0]!.inspected,
    });
    assert.equal(denied.allowed, false);
    assert.equal(denied.decision.inspected_receipt_id, null);
    assert.equal(denied.decision.reason_code, "operation-not-allowed");

    assert.throws(
      () => evaluateEvidenceInspectionPolicy({
        requestId: REQUEST_ID,
        traceId: TRACE_ID,
        operation: "evidence.inspect",
        verifiedStoredEvidence: {
          record: { receipt: { receipt_id: fixtures[0]!.receiptId } },
          event: {},
          reference: {},
        } as unknown as StoredPublicEvidence,
      }),
      /restart-verified evidence/u,
    );
  } finally {
    fixtures.forEach((fixture) => rmSync(fixture.root, { recursive: true, force: true }));
  }
});

test("rejects hostile policy inputs without invoking traps or accessors", () => {
  const fixture = inspectedEvidence("v1");
  try {
    const input = {
      requestId: REQUEST_ID,
      traceId: TRACE_ID,
      operation: "evidence.inspect",
      verifiedStoredEvidence: fixture.inspected,
    } as const;
    let trapCalls = 0;
    const proxy = new Proxy(input, {
      get() {
        trapCalls += 1;
        throw new Error("policy input proxy trap must not run");
      },
      getOwnPropertyDescriptor() {
        trapCalls += 1;
        throw new Error("policy input descriptor trap must not run");
      },
      ownKeys() {
        trapCalls += 1;
        throw new Error("policy input ownKeys trap must not run");
      },
    });
    assert.throws(
      () => evaluateEvidenceInspectionPolicy(proxy),
      /without proxies or accessors/u,
    );
    assert.equal(trapCalls, 0);

    let accessorCalls = 0;
    const accessor = { ...input } as Record<string, unknown>;
    Object.defineProperty(accessor, "requestId", {
      configurable: true,
      enumerable: true,
      get() {
        accessorCalls += 1;
        throw new Error("policy input accessor must not run");
      },
    });
    assert.throws(
      () => evaluateEvidenceInspectionPolicy(
        accessor as unknown as Parameters<typeof evaluateEvidenceInspectionPolicy>[0],
      ),
      /without proxies or accessors/u,
    );
    assert.equal(accessorCalls, 0);
  } finally {
    rmSync(fixture.root, { recursive: true, force: true });
  }
});
