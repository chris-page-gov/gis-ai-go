import assert from "node:assert/strict";
import test from "node:test";

import { canonicalJson, verifyPublicAuthorityContext } from "@gis-ai-go/evidence";

import { PUBLIC_AUTHORITY_CONTEXT, getPublicAuthorityContext } from "../src/index.js";

function assertRecursivelyFrozen(value: unknown): void {
  if (value === null || typeof value !== "object") {
    return;
  }
  assert.equal(Object.isFrozen(value), true);
  for (const child of Object.values(value)) {
    assertRecursivelyFrozen(child);
  }
}

function keysIn(value: unknown): Set<string> {
  const keys = new Set<string>();
  if (Array.isArray(value)) {
    for (const child of value) {
      for (const key of keysIn(child)) keys.add(key);
    }
  } else if (value !== null && typeof value === "object") {
    for (const [key, child] of Object.entries(value)) {
      keys.add(key);
      for (const nested of keysIn(child)) keys.add(nested);
    }
  }
  return keys;
}

test("constructs a deterministic frozen anonymous-open context without caller input", () => {
  const first = getPublicAuthorityContext();
  const second = getPublicAuthorityContext();

  assert.notEqual(first, second);
  assert.equal(canonicalJson(first), canonicalJson(second));
  assert.equal(canonicalJson(first), canonicalJson(PUBLIC_AUTHORITY_CONTEXT));
  assert.equal(verifyPublicAuthorityContext(first), true);
  assertRecursivelyFrozen(first);

  assert.deepEqual(first.permitted_operations, ["catalogue.describe", "catalogue.search"]);
  assert.equal(first.construction.source, "server");
  assert.equal(first.construction.profile, "anonymous-open");
  assert.equal(first.access.authentication, "none");
  assert.equal(first.access.read_only, true);
  assert.equal(first.evidence.persistence, "not-persisted");
  assert.equal(first.evidence.attestation, "not-attested");

  const forbidden = new Set([
    "actor",
    "client",
    "credential",
    "device",
    "entitlement",
    "organisation",
    "request_time",
    "role",
    "subject",
    "token",
    "user_id",
    "workload",
  ]);
  assert.equal([...keysIn(first)].some((key) => forbidden.has(key)), false);
});

test("detects any mutation of a detached context", () => {
  const tampered = structuredClone(getPublicAuthorityContext());
  (tampered.access as unknown as { contains_protected_data: boolean }).contains_protected_data =
    true;
  assert.equal(verifyPublicAuthorityContext(tampered), false);
});
