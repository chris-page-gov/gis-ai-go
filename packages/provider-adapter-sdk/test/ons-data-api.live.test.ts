import assert from "node:assert/strict";
import test from "node:test";

import {
  ONS_ADAPTER_REQUEST,
  ONS_OBSERVATION_URI,
  createOnsDataApiAdapter,
  digestProviderAdapterResult,
  type OnsAttemptTelemetry,
} from "../src/index.js";

test(
  "performs the exact bounded no-credential ONS probe only when explicitly enabled",
  {
    skip: process.env.GIS_AI_GO_ONS_LIVE_PROBE !== "1",
    timeout: 25_000,
  },
  async () => {
    const attempts: OnsAttemptTelemetry[] = [];
    const adapter = createOnsDataApiAdapter({
      lifecycle: {
        discovery: "active",
        invocation: "active",
        reason: "Explicit opt-in live test.",
      },
      onAttempt: (entry) => attempts.push(entry),
    });
    const result = await adapter.execute(ONS_ADAPTER_REQUEST, {
      deadline: new Date(Date.now() + 20_000).toISOString(),
    });
    assert.equal(result.dataset.version, "121");
    assert.deepEqual(
      result.dimensions.map(({ dimension }) => dimension),
      ["time", "geography", "week", "causeofdeath"],
    );
    assert.equal(result.provenance.sourceUri, ONS_OBSERVATION_URI);
    assert.match(digestProviderAdapterResult(result).sha256, /^[0-9a-f]{64}$/u);
    assert.equal(attempts.length >= 1 && attempts.length <= 2, true);
    assert.equal(JSON.stringify(attempts).includes(result.observations[0]!.value), false);
  },
);
