import assert from "node:assert/strict";
import test from "node:test";

import {
  DATA_QUERY_OBLIGATIONS,
  PUBLIC_READ_ONS_RESOURCE,
  SELECTION_RESOLVE_OBLIGATIONS,
  canonicalJson,
  verifyPublicReadPolicy,
  verifyPublicReadPolicyDecision,
} from "@gis-ai-go/evidence";

import {
  PUBLIC_READ_POLICY,
  PublicReadPolicyInputError,
  evaluatePublicReadPolicy,
  isAllowedPublicReadOperation,
} from "../src/index.js";

const REQUEST_ID = "request-public-read-policy-001";
const TRACE_ID = "4123456789abcdef0123456789abcdef";

test("loads the exact checked-in default-deny public-read v2 policy", () => {
  assert.equal(verifyPublicReadPolicy(PUBLIC_READ_POLICY), true);
  assert.equal(
    PUBLIC_READ_POLICY.policy_id,
    "gis-ai-go:public-policy:sha256:b1a37b2ebf6900e2b5d62dfa20bcdaa1232e1c4c9f9630f90ac9d3dde738624a",
  );
  assert.equal(PUBLIC_READ_POLICY.default_effect, "deny");
  assert.deepEqual(
    PUBLIC_READ_POLICY.rules.map((rule) => rule.operation),
    ["data.query", "selection.resolve"],
  );
  assert.deepEqual(PUBLIC_READ_POLICY.resources, [PUBLIC_READ_ONS_RESOURCE]);
  assert.equal(Object.isFrozen(PUBLIC_READ_POLICY.resources[0]), true);
});

test("allows only each exact operation and exact reviewed ONS resource", () => {
  for (const operation of ["data.query", "selection.resolve"] as const) {
    const evaluation = evaluatePublicReadPolicy({
      requestId: REQUEST_ID,
      traceId: TRACE_ID,
      operation,
      resource: PUBLIC_READ_ONS_RESOURCE,
    });
    assert.equal(evaluation.allowed, true);
    assert.equal(evaluation.reasonCode, "public-read-operation-allowed");
    assert.equal(isAllowedPublicReadOperation(evaluation, operation), true);
    assert.ok(evaluation.decision);
    assert.equal(verifyPublicReadPolicyDecision(evaluation.decision), true);
    assert.equal(evaluation.decision.resource_id, PUBLIC_READ_ONS_RESOURCE.resource_id);
    assert.deepEqual(
      evaluation.decision.obligations,
      operation === "data.query"
        ? DATA_QUERY_OBLIGATIONS
        : SELECTION_RESOLVE_OBLIGATIONS,
    );
  }
});

test("denies wrong resources, other governed operations and unknown operations", () => {
  const altered = structuredClone(PUBLIC_READ_ONS_RESOURCE) as unknown as {
    dataset: { version: string };
  };
  altered.dataset.version = "latest";
  const wrongResource = evaluatePublicReadPolicy({
    requestId: REQUEST_ID,
    traceId: TRACE_ID,
    operation: "data.query",
    resource: altered,
  });
  assert.equal(wrongResource.allowed, false);
  assert.equal(wrongResource.reasonCode, "resource-not-approved");
  assert.ok(wrongResource.decision);
  assert.equal(wrongResource.decision.resource_id, null);
  assert.deepEqual(wrongResource.decision.obligations, []);

  const governed = evaluatePublicReadPolicy({
    requestId: REQUEST_ID,
    traceId: TRACE_ID,
    operation: "map.render",
    resource: PUBLIC_READ_ONS_RESOURCE,
  });
  assert.equal(governed.allowed, false);
  assert.equal(governed.reasonCode, "operation-not-allowed");
  assert.ok(governed.decision);
  assert.equal(verifyPublicReadPolicyDecision(governed.decision), true);

  const unknown = evaluatePublicReadPolicy({
    requestId: REQUEST_ID,
    traceId: TRACE_ID,
    operation: "data.delete",
    resource: PUBLIC_READ_ONS_RESOURCE,
  });
  assert.equal(unknown.allowed, false);
  assert.equal(unknown.reasonCode, "operation-not-allowed");
  assert.equal(unknown.decision, null);
});

test("is deterministic and rejects malformed decision identifiers", () => {
  const input = {
    requestId: REQUEST_ID,
    traceId: TRACE_ID,
    operation: "selection.resolve",
    resource: PUBLIC_READ_ONS_RESOURCE,
  } as const;
  assert.equal(
    canonicalJson(evaluatePublicReadPolicy(input)),
    canonicalJson(evaluatePublicReadPolicy(input)),
  );
  assert.throws(
    () => evaluatePublicReadPolicy({ ...input, traceId: "invalid" }),
    PublicReadPolicyInputError,
  );
});

test("snapshots the closed evaluator input before operation or resource checks", () => {
  let reads = 0;
  const accessor = {
    requestId: REQUEST_ID,
    traceId: TRACE_ID,
    resource: PUBLIC_READ_ONS_RESOURCE,
  } as Record<string, unknown>;
  Object.defineProperty(accessor, "operation", {
    enumerable: true,
    get() {
      reads += 1;
      return reads === 1 ? "map.render" : "data.query";
    },
  });
  assert.throws(
    () => evaluatePublicReadPolicy(accessor as never),
    PublicReadPolicyInputError,
  );
  assert.equal(reads, 0);

  const input = {
    requestId: REQUEST_ID,
    traceId: TRACE_ID,
    operation: "data.query",
    resource: PUBLIC_READ_ONS_RESOURCE,
  } as const;
  let proxyReads = 0;
  const proxy = new Proxy(input, {
    get(target, property, receiver) {
      proxyReads += 1;
      return Reflect.get(target, property, receiver);
    },
  });
  assert.throws(() => evaluatePublicReadPolicy(proxy), PublicReadPolicyInputError);
  assert.equal(proxyReads, 0);
  assert.throws(
    () => evaluatePublicReadPolicy({ ...input, extra: true } as never),
    PublicReadPolicyInputError,
  );
  assert.throws(
    () => evaluatePublicReadPolicy({ ...input, operation: "x".repeat(129) }),
    PublicReadPolicyInputError,
  );
});
