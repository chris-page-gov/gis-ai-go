import assert from "node:assert/strict";
import test from "node:test";

import { StrictJsonParseError, parseStrictJson } from "../src/index.js";

test("parses strict JSON without normalising Unicode or insertion order", () => {
  const parsed = parseStrictJson('{"z":"é","a":[-0,1.5,true,null]}') as Record<
    string,
    unknown
  >;
  assert.equal(Object.getPrototypeOf(parsed), null);
  assert.equal(parsed.z, "é");
  assert.deepEqual(parsed.a, [0, 1.5, true, null]);
});

test("rejects literal and escape-equivalent duplicate keys", () => {
  for (const value of [
    '{"same":1,"same":2}',
    '{"same":1,"s\\u0061me":2}',
    '{"nested":{"x":1,"\\u0078":2}}',
  ]) {
    assert.throws(() => parseStrictJson(value), StrictJsonParseError);
  }
});

test("rejects malformed, ambiguous and computationally excessive JSON", () => {
  const tooDeep = `${"[".repeat(34)}0${"]".repeat(34)}`;
  const hostile = [
    "",
    "01",
    "1.",
    "1e",
    "1e400",
    "9007199254740992",
    "[1,]",
    '{"x":1,}',
    '"\\u12xx"',
    '"\\ud800"',
    '"\\udc00"',
    '{"\\ud800":1}',
    '"unterminated',
    "true false",
    tooDeep,
  ];
  for (const value of hostile) {
    assert.throws(() => parseStrictJson(value), StrictJsonParseError);
  }
});
