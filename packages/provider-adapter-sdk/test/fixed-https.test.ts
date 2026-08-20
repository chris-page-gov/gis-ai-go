import assert from "node:assert/strict";
import test from "node:test";

import {
  FixedHttpsTransportError,
  ONS_EGRESS_POLICY,
  ONS_OBSERVATION_URI,
  assertPublicProviderAddress,
  fixedHttpsGet,
} from "../src/index.js";

test("accepts only ordinary public resolver answers", () => {
  assert.doesNotThrow(() => assertPublicProviderAddress("1.1.1.1", 4));
  assert.doesNotThrow(() => assertPublicProviderAddress("8.8.8.8", 4));
  assert.doesNotThrow(() => assertPublicProviderAddress("2606:4700:4700::1111", 6));

  const blocked: readonly [string, number][] = [
    ["0.0.0.0", 4],
    ["10.0.0.1", 4],
    ["100.64.0.1", 4],
    ["127.0.0.1", 4],
    ["169.254.169.254", 4],
    ["172.16.0.1", 4],
    ["192.168.1.1", 4],
    ["198.18.0.1", 4],
    ["192.0.2.1", 4],
    ["192.88.99.1", 4],
    ["224.0.0.1", 4],
    ["255.255.255.255", 4],
    ["::", 6],
    ["::1", 6],
    ["::ffff:127.0.0.1", 6],
    ["64:ff9b::7f00:1", 6],
    ["2001:30::1", 6],
    ["2001:db8::1", 6],
    ["2620:4f:8000::1", 6],
    ["3fff::1", 6],
    ["5f00::1", 6],
    ["fc00::1", 6],
    ["fe80::1", 6],
    ["ff02::1", 6],
    ["not-an-address", 4],
    ["1.1.1.1", 6],
  ];
  for (const [address, family] of blocked) {
    assert.throws(
      () => assertPublicProviderAddress(address, family),
      (error: unknown) =>
        error instanceof FixedHttpsTransportError && error.kind === "unsafe-address",
    );
  }
});

test("stops before DNS when the fixed request is already cancelled", async () => {
  const controller = new AbortController();
  controller.abort();
  await assert.rejects(
    () =>
      fixedHttpsGet({
        policy: ONS_EGRESS_POLICY,
        url: ONS_OBSERVATION_URI,
        signal: controller.signal,
      }),
    (error: unknown) =>
      error instanceof FixedHttpsTransportError && error.kind === "aborted",
  );
});
