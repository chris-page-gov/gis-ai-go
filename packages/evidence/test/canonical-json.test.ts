import assert from "node:assert/strict";
import test from "node:test";

import {
  CanonicalJsonError,
  canonicalJson,
  canonicalJsonBytes,
  canonicalJsonClone,
} from "../src/index.js";

test("matches the RFC 8785 primitive serialisation example", () => {
  const sample = {
    numbers: [333333333.33333329, 1e30, 4.5, 2e-3, 1e-27],
    string: "€$\u000f\nA'B\"\\\\\"/",
    literals: [null, true, false],
  };

  assert.equal(
    canonicalJson(sample),
    "{\"literals\":[null,true,false],\"numbers\":[333333333.3333333,1e+30,4.5,0.002,1e-27],\"string\":\"€$\\u000f\\nA'B\\\"\\\\\\\\\\\"/\"}",
  );
});

test("orders object properties by UTF-16 code units as RFC 8785 requires", () => {
  const sample = {
    "€": "Euro Sign",
    "\r": "Carriage Return",
    "דּ": "Hebrew Letter Dalet With Dagesh",
    "1": "One",
    "😀": "Emoji: Grinning Face",
    "\u0080": "Control",
    "ö": "Latin Small Letter O With Diaeresis",
  };

  assert.equal(
    canonicalJson(sample),
    "{\"\\r\":\"Carriage Return\",\"1\":\"One\",\"\":\"Control\",\"ö\":\"Latin Small Letter O With Diaeresis\",\"€\":\"Euro Sign\",\"😀\":\"Emoji: Grinning Face\",\"דּ\":\"Hebrew Letter Dalet With Dagesh\"}",
  );
});

test("is independent of object insertion order and emits UTF-8 bytes", () => {
  const first = { z: 2, nested: { beta: "é", alpha: -0 }, a: 1 };
  const second = { a: 1, nested: { alpha: 0, beta: "é" }, z: 2 };

  assert.equal(canonicalJson(first), canonicalJson(second));
  assert.deepEqual(Buffer.from(canonicalJsonBytes({ value: "é" })), Buffer.from('{"value":"é"}', "utf8"));
});

test("allows shared acyclic values and detached null-prototype objects", () => {
  const shared = { value: 1 };
  const detached = Object.create(null) as Record<string, unknown>;
  detached.second = shared;
  detached.first = shared;

  assert.equal(canonicalJson(detached), '{"first":{"value":1},"second":{"value":1}}');
  const clone = canonicalJsonClone(detached);
  assert.ok(Object.isFrozen(clone));
  assert.ok(Object.isFrozen((clone as Record<string, object>).first));
});

test("rejects values outside the interoperable JSON data model", () => {
  const cycle: Record<string, unknown> = {};
  cycle.self = cycle;
  const sparse = new Array(2);
  sparse[1] = "present";
  const accessor = Object.defineProperty({}, "value", {
    enumerable: true,
    get: () => "not evaluated",
  });
  const hidden = Object.defineProperty({}, "value", { enumerable: false, value: 1 });
  const symbolProperty = { value: 1 } as Record<PropertyKey, unknown>;
  symbolProperty[Symbol("hidden")] = 2;
  const extraArray = [1] as unknown[] & { extra?: number };
  extraArray.extra = 2;

  const hostile: readonly unknown[] = [
    undefined,
    1n,
    Symbol("value"),
    () => undefined,
    Number.NaN,
    Number.POSITIVE_INFINITY,
    { value: undefined },
    [undefined],
    sparse,
    new Date("2026-08-20T00:00:00Z"),
    new Map(),
    new Proxy({ value: 1 }, {}),
    cycle,
    accessor,
    hidden,
    symbolProperty,
    extraArray,
    "\ud800",
    "\udc00",
    { "\ud800": "invalid key" },
  ];

  for (const value of hostile) {
    assert.throws(() => canonicalJson(value), CanonicalJsonError);
  }
});
