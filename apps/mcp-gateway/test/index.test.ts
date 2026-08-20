import assert from "node:assert/strict";
import test from "node:test";

import * as gateway from "../src/index.js";
import { catalogueActivation, gatewayMetadata } from "../src/index.js";

test("publishes the agreed inactive gateway identity", () => {
  assert.equal(gatewayMetadata.product, "GIS AI GO");
  assert.equal(gatewayMetadata.registryId, "io.github.chris-page-gov/gis-ai-go");
  assert.equal(gatewayMetadata.protocolTarget, "2026-07-28");
  assert.equal(gatewayMetadata.liveProviderCalls, false);
  assert.equal(gatewayMetadata.lifecycle, "candidate-blocked");
});

test("has no activation or environment-variable escape hatch", () => {
  assert.deepEqual(catalogueActivation, {
    state: "blocked",
    reason: "transport-and-interoperability-unverified",
    activeTools: [],
    activeApiOperations: [],
  });
  assert.equal(Object.isFrozen(catalogueActivation), true);
  assert.deepEqual(gatewayMetadata.activeTools, []);
  assert.deepEqual(gatewayMetadata.activeApiOperations, []);
  assert.equal("searchCatalogue" in gateway, false);
  assert.equal("describeCatalogue" in gateway, false);
});
