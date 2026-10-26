import assert from "node:assert/strict";
import { createRequire } from "node:module";
import test from "node:test";

// Exercise the validator the server actually resolves, rather than a separate
// test-only dependency. GHSA-mrhx-c7xc-m3w5 fixes the order of size admission.
const gatewayRequire = createRequire(import.meta.url);
const sdkRequire = createRequire(gatewayRequire.resolve("@modelcontextprotocol/server"));
const { z } = sdkRequire("zod");

test("the SDK validator rejects an oversized constrained array before visiting elements", () => {
  let visited = 0;
  const schema = z.array(z.string().transform((value: string) => {
    visited += 1;
    return value;
  })).max(2);

  assert.deepEqual(schema.parse(["one", "two"]), ["one", "two"]);
  assert.equal(visited, 2);
  visited = 0;
  const result = schema.safeParse(Array(64).fill("value"));
  assert.equal(result.success, false);
  assert.equal(visited, 0);
  assert.equal(result.error.issues.length, 1);
  assert.equal(result.error.issues[0].code, "too_big");
});
