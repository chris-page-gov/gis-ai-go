import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";

import {
  ADAPTER_OPERATIONS,
  ProviderAdapterFault,
  createSyntheticFixtureAdapter,
  serialiseProviderAdapterResult,
} from "../src/index.js";

const ACTIVE = Object.freeze({
  discovery: "active",
  invocation: "active",
  reason: "Explicit deterministic fixture test.",
} as const);

const REQUEST = Object.freeze({
  dataset: { id: "population-count", edition: "2026", version: "1" },
  selections: [
    { dimension: "time", option: "2026" },
    { dimension: "geography", option: "FIXTURE-EW" },
    { dimension: "measure", option: "population" },
  ],
});

test("is suspended by default and exposes the reviewed operation vocabulary", () => {
  const adapter = createSyntheticFixtureAdapter();

  assert.deepEqual(adapter.operations, ADAPTER_OPERATIONS);
  assert.deepEqual(
    Object.getOwnPropertyNames(Object.getPrototypeOf(adapter))
      .filter((name) => name !== "constructor")
      .sort(),
    [...ADAPTER_OPERATIONS].sort(),
  );
  assert.deepEqual(adapter.health(), {
    adapterId: "gis-ai-go.synthetic-statistics",
    discovery: "suspended",
    invocation: "suspended",
    network: "not-used",
  });
  assert.throws(
    () => adapter.describe(),
    (error: unknown) =>
      error instanceof ProviderAdapterFault && error.code === "ADAPTER_DISCOVERY_SUSPENDED",
  );
  assert.throws(
    () =>
      createSyntheticFixtureAdapter({
        discovery: "active",
        invocation: "invalid" as "active",
        reason: "Invalid fixture test.",
      }),
    TypeError,
  );
  assert.throws(
    () => adapter.execute(REQUEST),
    (error: unknown) =>
      error instanceof ProviderAdapterFault && error.code === "ADAPTER_INVOCATION_SUSPENDED",
  );
});

test("suspends discovery and invocation independently", () => {
  const discoverable = createSyntheticFixtureAdapter({
    discovery: "active",
    invocation: "suspended",
    reason: "Discovery-only fixture test.",
  });
  assert.equal(discoverable.describe().lifecycle.invocation, "suspended");
  assert.throws(
    () => discoverable.estimate(REQUEST),
    (error: unknown) =>
      error instanceof ProviderAdapterFault && error.code === "ADAPTER_INVOCATION_SUSPENDED",
  );

  const invocable = createSyntheticFixtureAdapter({
    discovery: "suspended",
    invocation: "active",
    reason: "Invocation-only fixture test.",
  });
  assert.throws(
    () => invocable.describe(),
    (error: unknown) =>
      error instanceof ProviderAdapterFault && error.code === "ADAPTER_DISCOVERY_SUSPENDED",
  );
  assert.equal(invocable.execute(REQUEST).observations[0]?.value, "1000");
});

test("preserves native identifiers and emits byte-identical canonical results", () => {
  const adapter = createSyntheticFixtureAdapter(ACTIVE);
  const reorderedInput = {
    selections: [
      { option: "2026", dimension: "time" },
      { option: "FIXTURE-EW", dimension: "geography" },
      { option: "population", dimension: "measure" },
    ],
    dataset: { version: "1", edition: "2026", id: "population-count" },
  };

  const first = adapter.execute(REQUEST);
  const second = adapter.execute(reorderedInput);
  const firstBytes = serialiseProviderAdapterResult(first);
  const secondBytes = serialiseProviderAdapterResult(second);

  assert.deepEqual(first.dataset, {
    edition: "2026",
    id: "population-count",
    version: "1",
    versionUri:
      "urn:gis-ai-go:fixture:provider:fixture.statistics:datasets:population-count:editions:2026:versions:1",
  });
  assert.deepEqual(
    first.dimensions.map(({ dimension }) => dimension),
    ["time", "geography", "measure"],
  );
  assert.equal(first.rights.state, "project-synthetic");
  assert.deepEqual(first.rights.exceptions, []);
  assert.equal(first.provenance.synthetic, true);
  assert.deepEqual(firstBytes, secondBytes);
  assert.equal(
    createHash("sha256").update(firstBytes).digest("hex"),
    "666f825e622deb3bc410f155f76783ee27bd856238032cccd42e04b928b6a053",
  );

  firstBytes[0] = 0;
  assert.notDeepEqual(firstBytes, serialiseProviderAdapterResult(first));
  assert.ok(Object.isFrozen(first));
  assert.ok(Object.isFrozen(first.dimensions));
});

test("estimates the exact canonical result size", () => {
  const adapter = createSyntheticFixtureAdapter(ACTIVE);
  const result = adapter.execute(REQUEST);

  assert.deepEqual(adapter.estimate(REQUEST), {
    canonicalResponseBytes: serialiseProviderAdapterResult(result).byteLength,
    confidence: "exact",
    observations: 1,
  });
});

test("fails closed on extra fields, stale versions, wrong order and unknown options", () => {
  const adapter = createSyntheticFixtureAdapter(ACTIVE);
  const invalid = [
    { ...REQUEST, callerUrl: "https://example.invalid" },
    { ...REQUEST, dataset: { ...REQUEST.dataset, version: "2" } },
    {
      ...REQUEST,
      selections: [REQUEST.selections[1], REQUEST.selections[0], REQUEST.selections[2]],
    },
    {
      ...REQUEST,
      selections: [
        REQUEST.selections[0],
        { dimension: "geography", option: "NOT-A-FIXTURE-AREA" },
        REQUEST.selections[2],
      ],
    },
    new Proxy(REQUEST, {}),
  ];

  for (const request of invalid) {
    assert.throws(() => adapter.execute(request), ProviderAdapterFault);
  }
  assert.throws(
    () => adapter.execute(invalid[1]),
    (error: unknown) =>
      error instanceof ProviderAdapterFault && error.code === "STALE_PROVIDER_VERSION",
  );
});

test("normalises expected and unknown errors without reflecting hostile details", () => {
  const adapter = createSyntheticFixtureAdapter(ACTIVE);
  const rateLimit = adapter.normalise_error(
    new ProviderAdapterFault("PROVIDER_RATE_LIMITED", {
      providerStatus: 429,
      retryable: true,
    }),
  );
  assert.deepEqual(rateLimit, {
    code: "PROVIDER_RATE_LIMITED",
    message: "The provider rate limit was reached.",
    providerStatus: 429,
    retryable: true,
  });

  const secret = "secret-provider-path-and-token";
  const normalised = adapter.normalise_error(new Error(secret));
  assert.equal(normalised.code, "PROVIDER_OUTAGE");
  assert.equal(normalised.retryable, true);
  assert.doesNotMatch(JSON.stringify(normalised), new RegExp(secret, "u"));

  const aborted = new Error(secret);
  aborted.name = "AbortError";
  assert.equal(adapter.normalise_error(aborted).code, "PROVIDER_TIMEOUT");

  const hostile = new Proxy(new Error(secret), {
    getPrototypeOf: () => {
      throw new Error(secret);
    },
  });
  assert.equal(adapter.normalise_error(hostile).code, "PROVIDER_OUTAGE");
});
