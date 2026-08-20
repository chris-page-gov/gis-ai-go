import { performance } from "node:perf_hooks";

import {
  ONS_ADAPTER_REQUEST,
  buildOnsLiveProbeRecord,
  createOnsDataApiAdapter,
  type OnsAttemptTelemetry,
} from "./index.js";

if (process.env.GIS_AI_GO_ONS_LIVE_PROBE !== "1") {
  process.stderr.write(
    "ONS live probe not run: set GIS_AI_GO_ONS_LIVE_PROBE=1 for one bounded public request.\n",
  );
  process.exitCode = 2;
} else {
  const attempts: OnsAttemptTelemetry[] = [];
  const adapter = createOnsDataApiAdapter({
    lifecycle: {
      discovery: "active",
      invocation: "active",
      reason: "Explicit opt-in bounded live probe.",
    },
    onAttempt: (entry) => attempts.push(entry),
  });
  const started = performance.now();
  try {
    const result = await adapter.execute(ONS_ADAPTER_REQUEST, {
      deadline: new Date(Date.now() + 20_000).toISOString(),
    });
    const description = adapter.describe();
    const rights = adapter.licence_evidence();
    const record = buildOnsLiveProbeRecord({
      observedAt: new Date().toISOString(),
      durationMs: Math.max(0, Math.round((performance.now() - started) * 1_000) / 1_000),
      description,
      rights,
      result,
      attempts,
    });
    process.stdout.write(`${JSON.stringify(record, null, 2)}\n`);
  } catch (error) {
    const failure = {
      schema: "gis-ai-go.provider-live-probe-failure.v1",
      observedAt: new Date().toISOString(),
      status: "failed",
      bounded: true,
      credentialsUsed: false,
      payloadStored: false,
      durationMs: Math.max(0, Math.round((performance.now() - started) * 1_000) / 1_000),
      attempts,
      error: adapter.normalise_error(error),
    };
    process.stdout.write(`${JSON.stringify(failure, null, 2)}\n`);
    process.exitCode = 1;
  }
}
