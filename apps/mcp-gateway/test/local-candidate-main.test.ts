import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import test, { type TestContext } from "node:test";
import { fromJsonSchema, type JsonSchemaType } from "@modelcontextprotocol/server";

import {
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
} from "@gis-ai-go/evidence";
import type {
  ApprovedOnsDataQueryCacheRecord,
} from "@gis-ai-go/provider-adapter-sdk";
import { V02_TARGET_ACTIVE_TOOL_NAMES } from "@gis-ai-go/tool-registry";

import { catalogueActivation } from "../src/activation.js";
import {
  CANDIDATE_ACTIVATION_LIFECYCLE,
  CANDIDATE_ACTIVATION_RESOURCES,
} from "../src/candidate-activation.js";
import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";
import {
  APPROVED_CACHE_WARNING,
  PUBLIC_ONS_DATA_QUERY_PARAMETERS,
} from "../src/data-query-application.js";
import { governedCandidateAssemblyBindings } from "../src/governed-assembly.js";
import {
  createGatewayHttpHandler,
  createGovernedCandidateHttpHandler,
} from "../src/http-app.js";
import {
  localCandidateCapabilityHealth,
  type LocalCandidateCapabilityHealth,
} from "../src/local-candidate-capability.js";
import { createGovernedCandidateMcpHttpHandler } from "../src/mcp-http.js";
import {
  LOCAL_CANDIDATE_HOST,
  LOCAL_CANDIDATE_DATA_QUERY_SOURCE,
  LOCAL_CANDIDATE_LIFECYCLE_SCHEMA,
  LOCAL_CANDIDATE_PORT,
  LOCAL_CANDIDATE_PROVIDER_OBSERVATION,
  LOCAL_CANDIDATE_STATE_ROOT_MODE,
  LOCAL_CANDIDATE_TARGET_RELEASE,
  assertFixedLocalCandidateArguments,
  createIdempotentLocalCandidateStop,
  createProviderFreeLocalCandidateAssembly,
  createRetryableLocalCandidateStateCleanup,
  localCandidateLifecycleRecord,
  localCandidateProviderTransportAttemptCount,
  localCandidateStartFailureRecord,
} from "../src/local-candidate-main.js";
import { gatewayMetadata } from "../src/metadata.js";

const SOURCE_CATALOGUE = fileURLToPath(
  new URL("../../../../artifacts/okf/", import.meta.url),
);
const CACHE_RECORD = JSON.parse(
  readFileSync(
    new URL(
      "../../../../providers/ons/data-query-approved-cache.v1.json",
      import.meta.url,
    ),
    "utf8",
  ),
) as ApprovedOnsDataQueryCacheRecord;
const LOCAL_CANDIDATE_WRAPPER = fileURLToPath(
  new URL("../../../../scripts/start-local-candidate", import.meta.url),
);

async function localAssembly(
  t: TestContext,
  now: () => Date = () => new Date("2026-09-01T12:00:00.000Z"),
) {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-local-candidate-unit-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const snapshot = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
    now: new Date("2026-09-01T12:00:00.000Z"),
  });
  const ledger = openPublicEvidenceLedger({
    rootDirectory: join(root, "ledger"),
    now: () => new Date("2026-09-01T12:00:01.000Z"),
  });
  const reconciliationIndex = openEvidenceReconciliationIndex({
    rootDirectory: join(root, "reconciliation"),
    ledger,
    now: () => new Date("2026-09-01T12:00:02.000Z"),
  });
  return createProviderFreeLocalCandidateAssembly(
    snapshot,
    ledger,
    reconciliationIndex,
    CACHE_RECORD,
    now,
  );
}

function localRequest(path: string, body?: unknown): Request {
  return new Request(`http://127.0.0.1:8787${path}`, {
    method: body === undefined ? "GET" : "POST",
    headers: {
      accept: "application/json", "content-type": "application/json",
      host: "127.0.0.1:8787",
    },
    ...(body === undefined ? {} : { body: JSON.stringify(body) }),
  });
}

test("fixes the provider-free local candidate identity and authority", async (t) => {
  const assembly = await localAssembly(t);
  assert.equal(LOCAL_CANDIDATE_HOST, "127.0.0.1");
  assert.equal(LOCAL_CANDIDATE_PORT, 8_787);
  assert.equal(LOCAL_CANDIDATE_TARGET_RELEASE, "0.2.0");
  assert.equal(
    LOCAL_CANDIDATE_LIFECYCLE_SCHEMA,
    "gis-ai-go.local-candidate-lifecycle.v1",
  );
  assert.equal(LOCAL_CANDIDATE_STATE_ROOT_MODE, 0o700);
  assert.equal(
    LOCAL_CANDIDATE_PROVIDER_OBSERVATION,
    "deterministic-in-memory-http-503",
  );
  assert.equal(
    LOCAL_CANDIDATE_DATA_QUERY_SOURCE,
    "byte-verified-approved-cache",
  );
  assert.equal(gatewayMetadata.version, "0.1.0");
  assert.equal(assembly.state, CANDIDATE_ACTIVATION_LIFECYCLE);
  assert.equal(assembly.productionRegistration, false);
  assert.deepEqual(assembly.operations, V02_TARGET_ACTIVE_TOOL_NAMES);
  assert.equal(assembly.apiOperations, assembly.operations);
  assert.equal(assembly.mcpOperations, assembly.operations);
  assert.deepEqual(assembly.mcpResources, CANDIDATE_ACTIVATION_RESOURCES);
  assert.deepEqual(assembly.suspensions, []);

  assert.equal(catalogueActivation.state, "blocked");
  assert.deepEqual(catalogueActivation.activeTools, []);
  assert.deepEqual(catalogueActivation.activeApiOperations, []);
  assert.equal(gatewayMetadata.lifecycle, "candidate-blocked");
  assert.deepEqual(gatewayMetadata.activeTools, []);
  assert.deepEqual(gatewayMetadata.activeApiOperations, []);
});

test("reports fixed path-free local provenance and retries failed state cleanup", () => {
  const failure = localCandidateLifecycleRecord(
    "local_candidate_cleanup_failed",
    "a".repeat(40),
  );
  assert.deepEqual(failure, {
    schema: "gis-ai-go.local-candidate-lifecycle.v1",
    event: "local_candidate_cleanup_failed",
    endpoint: "http://127.0.0.1:8787/mcp",
    software_version: "0.1.0",
    target_release: "0.2.0",
    lifecycle: "candidate-unregistered",
    production_registration: false,
    provider_egress: false,
    provider_observation: "deterministic-in-memory-http-503",
    data_query_source: "byte-verified-approved-cache",
    revision: "a".repeat(40),
  });
  assert.equal(JSON.stringify(failure).includes("/private/"), false);

  let attempts = 0;
  const cleanup = createRetryableLocalCandidateStateCleanup(
    "opaque-state-root",
    (stateRoot) => {
      assert.equal(stateRoot, "opaque-state-root");
      attempts += 1;
      if (attempts === 1) throw new Error("injected cleanup failure");
    },
  );
  assert.throws(cleanup, /injected cleanup failure/u);
  assert.doesNotThrow(cleanup);
  assert.doesNotThrow(cleanup);
  assert.equal(attempts, 2);
});

test("explains port conflicts without disclosing raw startup errors", () => {
  const occupied = Object.assign(new Error("private source and state details"), {
    code: "EADDRINUSE",
  });
  const report = localCandidateStartFailureRecord(occupied);
  assert.equal(report.event, "local_candidate_start_failed");
  assert.equal(report.reason, "port-in-use");
  assert.equal(report.message,
    "Port 8787 is already in use. Stop the other local process and try again.");
  assert.equal(JSON.stringify(report).includes(occupied.message), false);
  const failure = localCandidateStartFailureRecord(new Error("private failure"));
  assert.equal(failure.reason, "startup-check-failed");
  assert.equal(JSON.stringify(failure).includes("private failure"), false);
});

test("labels the deterministic outage as exact approved-cache evidence", async (t) => {
  const assembly = await localAssembly(t);
  const result = await governedCandidateAssemblyBindings(
    assembly,
  ).dataQueryApplication.query(
    {
      schema: "gis-ai-go.data-query-request.v1",
      idempotency_key: `gis-ai-go:ik:v1:${"6".repeat(64)}`,
      parameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
    },
    {
      requestId: "local-candidate-approved-cache-001",
      traceId: "6".repeat(32),
      instance: "/data/query",
    },
  );
  assert.equal(result.data.cache?.status, "approved-current");
  assert.deepEqual(result.warnings, [APPROVED_CACHE_WARNING]);
  assert.deepEqual(
    result.evidence_receipt.transformations.map(({ name }) => name),
    [
      "normalise-public-read-parameters",
      "read-approved-provider-cache",
      "project-public-read-result-core",
    ],
  );
  assert.equal(
    result.evidence_receipt.transformations.some(
      ({ name }) => name === "execute-fixed-provider-query",
    ),
    false,
  );
  assert.equal(localCandidateProviderTransportAttemptCount(assembly), 1);
});

test("publishes immutable cache approval and vintage for a fixed observation", async (t) => {
  let now = new Date("2026-09-01T12:00:00.000Z");
  const assembly = await localAssembly(t, () => now);
  const health = localCandidateCapabilityHealth(assembly)!;
  assert.equal(health.data_query, "available");
  assert.equal(health.checked_at, now.toISOString());
  assert.deepEqual(health.approved_cache, {
    cache_id: CACHE_RECORD.cache_id,
    approved_at: CACHE_RECORD.approval.approved_at,
    stale_after: "2027-02-20T20:21:08.947Z",
    stale_use: "forbidden",
  });
  assert.deepEqual(health.data_vintage, {
    dataset: CACHE_RECORD.query.dataset,
    selections: CACHE_RECORD.query.selections,
    source_uri: CACHE_RECORD.source.source_uri,
    retrieved_at: "2026-08-20T20:21:08.947Z",
    current_statistics: false,
  });
  assert.equal(health.evidence_retention, "current-session-only");
  for (const value of [
    health, health.approved_cache, health.data_vintage, health.data_vintage.dataset,
    health.data_vintage.selections, ...health.data_vintage.selections,
  ]) assert.equal(Object.isFrozen(value), true);
  assert.equal(localCandidateLifecycleRecord(
    "local_candidate_started", "a".repeat(40), health,
  ).local_capability_health, health);

  now = new Date(Date.parse(CACHE_RECORD.approval.approved_at) - 1);
  assert.equal(localCandidateCapabilityHealth(assembly)?.data_query, "not-yet-approved");
  now = new Date(Number.NaN);
  assert.equal(localCandidateCapabilityHealth(assembly)?.data_query, "clock-unavailable");
  assert.equal(localCandidateCapabilityHealth(assembly)?.checked_at, null);
  assert.equal(health.data_query, "available");
});

for (const transport of ["direct", "mcp"] as const) {
  test(`${transport} rejects expired queries and preserves session evidence`, async (t) => {
    const expiresAt = Date.parse(CACHE_RECORD.freshness.stale_after);
    let now = expiresAt - 1;
    const assembly = await localAssembly(t, () => new Date(now));
    const direct = createGovernedCandidateHttpHandler(assembly);
    const document = await (await direct(localRequest("/openapi.json"))).json() as {
      components: { schemas: Record<string, Record<string, unknown>> };
    };
    const schemas = document.components.schemas;
    const healthSchema = structuredClone(schemas.Health!);
    (healthSchema.properties as Record<string, unknown>).catalogue = schemas.CatalogueIdentity;
    const healthValidator = fromJsonSchema(healthSchema as JsonSchemaType);
    const readinessValidator = fromJsonSchema(schemas.Readiness as JsonSchemaType);
    const mcp = createGovernedCandidateMcpHttpHandler(assembly);
    t.after(() => mcp.close());
    let requestId = 0;
    async function exchange(method: string, params: Record<string, unknown>) {
      const response = await mcp.fetch(new Request("http://127.0.0.1:8787/mcp", {
        method: "POST",
        headers: {
          accept: "application/json, text/event-stream",
          "content-type": "application/json",
          "mcp-method": method,
          "mcp-protocol-version": "2026-07-28",
          ...(typeof params.name === "string" ? { "mcp-name": params.name } : {}),
          ...(typeof params.uri === "string" ? { "mcp-name": params.uri } : {}),
        },
        body: JSON.stringify({
          jsonrpc: "2.0", id: ++requestId, method,
          params: {
            _meta: {
              "io.modelcontextprotocol/protocolVersion": "2026-07-28",
              "io.modelcontextprotocol/clientCapabilities": {},
              "io.modelcontextprotocol/clientInfo": {
                name: "local-candidate-expiry-test", version: "1.0.0",
              },
            },
            ...params,
          },
        }),
      }));
      assert.equal(response.status, 200);
      const message = await response.json() as {
        result: {
          isError?: boolean;
          structuredContent: Record<string, unknown>;
          content: readonly unknown[];
          tools: { name: string }[];
          contents: { text: string }[];
        };
      };
      assert.ok(message.result);
      return message.result;
    }
    async function call(operation: "data.query" | "evidence.inspect", body: unknown) {
      if (transport === "direct") {
        const response = await direct(localRequest(
          operation === "data.query" ? "/data/query" : "/evidence/inspect", body,
        ));
        return { status: response.status, body: await response.json() as Record<string, unknown> };
      }
      const result = await exchange("tools/call", { name: operation, arguments: body });
      assert.deepEqual(result.content, [{
        type: "text", text: JSON.stringify(result.structuredContent),
      }]);
      return {
        status: result.isError === true ? result.structuredContent.status : 200,
        body: result.structuredContent,
      };
    }
    let successfulReceipt: unknown;
    const successfulKey = `gis-ai-go:ik:v1:${"1".repeat(64)}`;
    for (const [index, offset] of [-1, 0, 1].entries()) {
      now = expiresAt + offset;
      for (const path of ["/healthz", "/readyz"]) {
        const response = await direct(localRequest(path));
        assert.equal(response.status, 200);
        const body = await response.json() as {
          local_capability_health: LocalCandidateCapabilityHealth;
        };
        const validator = path === "/healthz" ? healthValidator : readinessValidator;
        const validation = await validator["~standard"].validate(body);
        assert.equal("issues" in validation, false, JSON.stringify(validation));
        assert.equal(body.local_capability_health.checked_at, new Date(now).toISOString());
        assert.equal(body.local_capability_health.data_query, offset < 0 ? "available" : "expired");
        assert.equal(
          body.local_capability_health.approved_cache.stale_after,
          CACHE_RECORD.freshness.stale_after,
        );
      }
      const queried = await call("data.query", {
        schema: "gis-ai-go.data-query-request.v1",
        idempotency_key: `gis-ai-go:ik:v1:${String(index + 1).repeat(64)}`,
        parameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
      });
      if (offset < 0) {
        assert.equal(queried.status, 200, JSON.stringify(queried.body));
        successfulReceipt = queried.body.evidence_receipt;
      } else {
        assert.equal(queried.status, 503);
        assert.equal(queried.body.code, "provider_unavailable");
        assert.equal(queried.body.evidence_receipt, undefined);
        const inspected = await call("evidence.inspect", {
          schema: "gis-ai-go.evidence-inspect-request.v2",
          source_operation: "data.query", idempotency_key: successfulKey,
        });
        assert.equal(inspected.status, 200);
        const data = inspected.body.data as { record: { receipt: unknown } };
        assert.deepEqual(data.record.receipt, successfulReceipt);
      }
    }
    assert.equal(localCandidateProviderTransportAttemptCount(assembly), 3);
    assert.deepEqual(assembly.operations, V02_TARGET_ACTIVE_TOOL_NAMES);
    assert.deepEqual(assembly.mcpResources, CANDIDATE_ACTIVATION_RESOURCES);
    const tools = await exchange("tools/list", {});
    assert.deepEqual(
      tools.tools.map(({ name }) => name).sort(), [...V02_TARGET_ACTIVE_TOOL_NAMES].sort(),
    );
    const receiptId = (successfulReceipt as { receipt_id: string }).receipt_id;
    const resource = await exchange("resources/read", {
      uri: `gis-ai-go://evidence/receipts/${encodeURIComponent(receiptId)}`,
    });
    const resourceBody = JSON.parse(resource.contents[0]!.text) as {
      data: { record: { receipt: unknown } };
    };
    assert.deepEqual(resourceBody.data.record.receipt, successfulReceipt);
    const changedHealth = await (await direct(localRequest("/healthz"))).json() as {
      local_capability_health: { approved_cache: { stale_after: string } };
    };
    changedHealth.local_capability_health.approved_cache.stale_after = "2028-02-20T20:21:08.947Z";
    assert.equal("issues" in await healthValidator["~standard"].validate(changedHealth), true);
  });
}

test("keeps default health and blocked readiness free of local capability claims", async (t) => {
  const assembly = await localAssembly(t);
  const { snapshot } = governedCandidateAssemblyBindings(assembly);
  const handler = createGatewayHttpHandler({ snapshot });
  for (const [path, status] of [["/healthz", 200], ["/readyz", 503]] as const) {
    const response = await handler(localRequest(path));
    assert.equal(response.status, status);
    const body = await response.json() as Record<string, unknown>;
    assert.equal(Object.hasOwn(body, "local_capability_health"), false);
    if (path === "/readyz") {
      assert.deepEqual(body.active_tools, []);
      assert.deepEqual(body.active_api_operations, []);
    }
  }
});

test("coalesces repeated clean stops before and after completion", async () => {
  let closes = 0;
  let removals = 0;
  const cleanup = createRetryableLocalCandidateStateCleanup("opaque-state-root", () => {
    removals += 1;
  });
  const stop = createIdempotentLocalCandidateStop(async () => {
    closes += 1;
    await Promise.resolve();
    cleanup();
  });
  const first = stop();
  assert.equal(stop(), first);
  await first;
  assert.equal(stop(), first);
  await stop();
  assert.equal(closes, 1);
  assert.equal(removals, 1);
});

test("rejects command-line widening and substituted approved cache material", async (t) => {
  assert.doesNotThrow(() => assertFixedLocalCandidateArguments(["node", "entry"]));
  assert.throws(
    () => assertFixedLocalCandidateArguments(["node", "entry", "--port=9000"]),
    /does not accept arguments/u,
  );

  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-local-candidate-cache-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const snapshot = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
    now: new Date("2026-09-01T12:00:00.000Z"),
  });
  const ledger = openPublicEvidenceLedger({
    rootDirectory: join(root, "ledger"),
  });
  const reconciliationIndex = openEvidenceReconciliationIndex({
    rootDirectory: join(root, "reconciliation"),
    ledger,
  });
  const changed = structuredClone(CACHE_RECORD) as unknown as Record<string, unknown>;
  const observation = changed.observation as Record<string, unknown>;
  observation.value = "10472";
  assert.throws(
    () => createProviderFreeLocalCandidateAssembly(
      snapshot,
      ledger,
      reconciliationIndex,
      changed as unknown as ApprovedOnsDataQueryCacheRecord,
    ),
    /Approved ONS cache observation is invalid/u,
  );
  for (const staleAfter of ["not-a-date", "2027-02-30T20:21:08.947Z"]) {
    const malformed = {
      ...CACHE_RECORD,
      freshness: { ...CACHE_RECORD.freshness, stale_after: staleAfter },
    };
    assert.throws(
      () => createProviderFreeLocalCandidateAssembly(
        snapshot, ledger, reconciliationIndex, malformed,
      ),
      /Approved ONS cache stale-after time must be (?:a |a valid )canonical UTC timestamp/u,
    );
  }
  assert.throws(
    () => (
      createProviderFreeLocalCandidateAssembly as unknown as
        (...values: unknown[]) => unknown
    )(
      snapshot,
      ledger,
      reconciliationIndex,
      CACHE_RECORD,
      { host: "0.0.0.0" },
    ),
    /exact fixed input tuple/u,
  );
});

test(
  "keeps the POSIX launcher executable and replaces itself with the runtime",
  { skip: process.platform === "win32" },
  () => {
    const mode = statSync(LOCAL_CANDIDATE_WRAPPER).mode & 0o777;
    assert.equal(mode & 0o111, 0o111);
    const source = readFileSync(LOCAL_CANDIDATE_WRAPPER, "utf8");
    assert.match(source, /^#!\/bin\/sh\n/u);
    assert.match(
      source,
      /^pnpm --filter @gis-ai-go\/mcp-gateway run prepare:test$/mu,
    );
    assert.match(
      source,
      /^pnpm --filter @gis-ai-go\/mcp-gateway run build$/mu,
    );
    assert.doesNotMatch(source, /pnpm exec/u);
    assert.doesNotMatch(source, /run start:local-candidate/u);
    const executableLines = source
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0 && !line.startsWith("#"));
    assert.equal(
      executableLines.at(-1),
      "exec node apps/mcp-gateway/dist/src/local-candidate-main.js",
    );
  },
);
