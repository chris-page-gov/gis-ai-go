import assert from "node:assert/strict";
import test from "node:test";

import { assertStageZeroRequest, gatewayMetadata } from "../src/index.js";

test("publishes the agreed non-networked identity", () => {
  assert.equal(gatewayMetadata.product, "GIS AI GO");
  assert.equal(gatewayMetadata.registryId, "io.github.chris-page-gov/gis-ai-go");
  assert.equal(gatewayMetadata.liveProviderCalls, false);
});

test("rejects non-synthetic work", () => {
  assert.throws(
    () => assertStageZeroRequest({ synthetic: false, networkAccess: false }),
    /synthetic requests only/,
  );
});

test("rejects network access", () => {
  assert.throws(
    () => assertStageZeroRequest({ synthetic: true, networkAccess: true }),
    /forbids network/,
  );
});

test("accepts an offline synthetic validation request", () => {
  const result = assertStageZeroRequest({ synthetic: true, networkAccess: false });
  assert.equal(result.stage, 0);
});
