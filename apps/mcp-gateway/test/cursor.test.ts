import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";

import {
  InvalidCatalogueCursorError,
  canonicalJson,
  decodeCatalogueCursor,
  encodeCatalogueCursor,
  sha256CanonicalJson,
} from "../src/cursor.js";

const ROOT = "a".repeat(64);
const OTHER_ROOT = "b".repeat(64);
const CRITERIA = sha256CanonicalJson({ facets: { tags: ["hmlr"] }, limit: 5, query: "land" });
const OTHER_CRITERIA = sha256CanonicalJson({
  facets: { tags: ["hmlr"] },
  limit: 5,
  query: "price",
});

test("canonical JSON and cursor encoding are independent of object insertion order", () => {
  assert.equal(
    canonicalJson({ z: [3, 2, 1], a: { right: true, left: null } }),
    canonicalJson({ a: { left: null, right: true }, z: [3, 2, 1] }),
  );

  const binding = { contentRootSha256: ROOT, criteriaSha256: CRITERIA };
  const first = encodeCatalogueCursor(binding, 5);
  const second = encodeCatalogueCursor(binding, 5);
  assert.equal(first, second);
  assert.equal(first.includes("="), false);
  assert.equal(
    decodeCatalogueCursor(first, { ...binding, limit: 5 }),
    5,
  );
});

test("rejects corruption and replay against changed criteria or catalogue bytes", () => {
  const token = encodeCatalogueCursor(
    { contentRootSha256: ROOT, criteriaSha256: CRITERIA },
    10,
  );
  const changedFinalCharacter = token.endsWith("0") ? "1" : "0";
  const tampered = `${token.slice(0, -1)}${changedFinalCharacter}`;

  assert.throws(
    () =>
      decodeCatalogueCursor(tampered, {
        contentRootSha256: ROOT,
        criteriaSha256: CRITERIA,
        limit: 5,
      }),
    InvalidCatalogueCursorError,
  );
  assert.throws(
    () =>
      decodeCatalogueCursor(token, {
        contentRootSha256: ROOT,
        criteriaSha256: OTHER_CRITERIA,
        limit: 5,
      }),
    /different search criteria/u,
  );
  assert.throws(
    () =>
      decodeCatalogueCursor(token, {
        contentRootSha256: OTHER_ROOT,
        criteriaSha256: CRITERIA,
        limit: 5,
      }),
    /different catalogue revision/u,
  );
});

test("rejects non-canonical payloads and offsets that are not page aligned", () => {
  const nonCanonicalJson = JSON.stringify({
    v: 1,
    offset: 5,
    criteria_sha256: CRITERIA,
    content_root_sha256: ROOT,
  });
  const body = Buffer.from(nonCanonicalJson, "utf8").toString("base64url");
  const digest = createHash("sha256").update(nonCanonicalJson, "utf8").digest("hex");
  assert.throws(
    () =>
      decodeCatalogueCursor(`${body}.${digest}`, {
        contentRootSha256: ROOT,
        criteriaSha256: CRITERIA,
        limit: 5,
      }),
    /not canonical JSON/u,
  );

  const misaligned = encodeCatalogueCursor(
    { contentRootSha256: ROOT, criteriaSha256: CRITERIA },
    7,
  );
  assert.throws(
    () =>
      decodeCatalogueCursor(misaligned, {
        contentRootSha256: ROOT,
        criteriaSha256: CRITERIA,
        limit: 5,
      }),
    /not aligned/u,
  );
});

test("rejects malformed tokens and invalid encoder inputs", () => {
  const binding = { contentRootSha256: ROOT, criteriaSha256: CRITERIA, limit: 5 };
  for (const token of ["", "not-a-cursor", "a.b.c", "=." + "0".repeat(64)]) {
    assert.throws(() => decodeCatalogueCursor(token, binding), InvalidCatalogueCursorError);
  }
  assert.throws(
    () => encodeCatalogueCursor({ contentRootSha256: ROOT, criteriaSha256: CRITERIA }, 0),
    /positive safe integer/u,
  );
});
