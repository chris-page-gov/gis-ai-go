import assert from "node:assert/strict";
import test from "node:test";

import {
  CANONICAL_DOMAINS,
  canonicalDigest,
  contentAddress,
  domainSeparatedSha256,
  verifyContentAddress,
  verifyDomainSeparatedSha256,
} from "../src/index.js";

test("produces stable domain-separated digests for canonical content", () => {
  const first = { query: "roads", limit: 20 };
  const second = { limit: 20, query: "roads" };
  const digest = domainSeparatedSha256(CANONICAL_DOMAINS.catalogueParameters, first);

  assert.match(digest, /^[0-9a-f]{64}$/u);
  assert.equal(digest, domainSeparatedSha256(CANONICAL_DOMAINS.catalogueParameters, second));
  assert.deepEqual(canonicalDigest(CANONICAL_DOMAINS.catalogueParameters, first), {
    domain: "gis-ai-go.catalogue-parameters.v1",
    sha256: digest,
  });
  assert.equal(verifyDomainSeparatedSha256(digest, CANONICAL_DOMAINS.catalogueParameters, second), true);
  assert.equal(
    verifyDomainSeparatedSha256(digest, CANONICAL_DOMAINS.catalogueParameters, { ...second, limit: 21 }),
    false,
  );
});

test("separates equal canonical bytes in different semantic domains", () => {
  const value = { id: "same-content" };
  assert.notEqual(
    domainSeparatedSha256(CANONICAL_DOMAINS.catalogueParameters, value),
    domainSeparatedSha256(CANONICAL_DOMAINS.catalogueResultCore, value),
  );
  assert.notEqual(
    domainSeparatedSha256(CANONICAL_DOMAINS.providerAdapterResult, value),
    domainSeparatedSha256(CANONICAL_DOMAINS.executionResultData, value),
  );
});

test("creates and verifies namespaced content identities", () => {
  const value = { schema: "example.v1", value: true };
  const identity = contentAddress(
    "gis-ai-go:evidence-receipt",
    CANONICAL_DOMAINS.evidenceReceipt,
    value,
  );
  assert.match(identity, /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u);
  assert.equal(
    verifyContentAddress(
      identity,
      "gis-ai-go:evidence-receipt",
      CANONICAL_DOMAINS.evidenceReceipt,
      value,
    ),
    true,
  );
  assert.equal(
    verifyContentAddress(
      identity,
      "gis-ai-go:evidence-receipt",
      CANONICAL_DOMAINS.evidenceReceipt,
      { ...value, value: false },
    ),
    false,
  );
});

test("rejects ambiguous or unversioned digest domains", () => {
  for (const domain of ["", "example", "Example.v1", "example.v0", "example.v1\u0000other"] as const) {
    assert.throws(() => domainSeparatedSha256(domain, null), TypeError);
  }
});
