import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import test, { type TestContext } from "node:test";

import {
  PUBLIC_READ_ONS_RESOURCE,
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
  CANDIDATE_ACTIVATION_OPERATIONS,
  CANDIDATE_ACTIVATION_RESOURCES,
  createCandidateActivation,
} from "../src/candidate-activation.js";
import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";
import { createGatewayHttpHandler } from "../src/http-app.js";
import { assessGovernedCandidateReadiness } from "../src/governed-assembly.js";
import { gatewayMetadata } from "../src/metadata.js";
import { assertCandidateContainerAuthority } from "../src/container-main.js";

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

async function activation(t: TestContext) {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-candidate-activation-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const snapshot = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
    now: new Date("2026-08-29T00:00:00.000Z"),
  });
  const ledger = openPublicEvidenceLedger({
    rootDirectory: join(root, "ledger"),
    now: () => new Date("2026-08-29T00:00:01.000Z"),
  });
  const reconciliationIndex = openEvidenceReconciliationIndex({
    rootDirectory: join(root, "reconciliation"),
    ledger,
    now: () => new Date("2026-08-29T00:00:02.000Z"),
  });
  return {
    snapshot,
    ledger,
    reconciliationIndex,
    assembly: createCandidateActivation(
      snapshot,
      ledger,
      reconciliationIndex,
      CACHE_RECORD,
    ),
  };
}

test("builds only the fixed local unregistered exact-five activation", async (t) => {
  const { assembly } = await activation(t);
  assert.equal(assembly.state, CANDIDATE_ACTIVATION_LIFECYCLE);
  assert.equal(assembly.productionRegistration, false);
  assert.deepEqual(assembly.operations, V02_TARGET_ACTIVE_TOOL_NAMES);
  assert.deepEqual(assembly.operations, CANDIDATE_ACTIVATION_OPERATIONS);
  assert.equal(assembly.apiOperations, assembly.operations);
  assert.equal(assembly.mcpOperations, assembly.operations);
  assert.deepEqual(assembly.mcpResources, CANDIDATE_ACTIVATION_RESOURCES);
  assert.deepEqual(assembly.suspensions, []);
  assert.equal(assembly.bindings.provider.discovery, "active");
  assert.equal(assembly.bindings.provider.invocation, "active");
  assert.equal(assembly.operations.includes("map.render" as never), false);
  assert.equal(assembly.operations.includes("workflow.execute" as never), false);

  assert.equal(catalogueActivation.state, "blocked");
  assert.deepEqual(catalogueActivation.activeTools, []);
  assert.deepEqual(catalogueActivation.activeApiOperations, []);
  assert.equal(gatewayMetadata.lifecycle, "candidate-blocked");
  assert.deepEqual(gatewayMetadata.activeTools, []);
  assert.deepEqual(gatewayMetadata.activeApiOperations, []);
});

test("keeps generic constructors blocked while the candidate assembly is ready", async (t) => {
  const { snapshot, assembly } = await activation(t);
  const blocked = createGatewayHttpHandler({
    snapshot,
    createTraceId: () => "a".repeat(32),
    createTraceParentId: () => "b".repeat(16),
  });
  const blockedReady = await blocked(new Request("http://127.0.0.1:8787/readyz", {
    headers: { host: "127.0.0.1:8787" },
  }));
  assert.equal(blockedReady.status, 503);
  assert.deepEqual(await blockedReady.json(), {
    status: "blocked",
    reason: "transport-and-interoperability-unverified",
    active_tools: [],
    active_api_operations: [],
  });

  assert.equal(assembly.productionRegistration, false);
  assert.deepEqual(assembly.operations, V02_TARGET_ACTIVE_TOOL_NAMES);
});

test("restarts the fixed candidate at capacity while reporting readiness blocked", async (t) => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-candidate-capacity-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const snapshot = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
    now: new Date("2026-08-29T00:00:00.000Z"),
  });
  const ledger = openPublicEvidenceLedger({
    rootDirectory: join(root, "ledger"),
    now: () => new Date("2026-08-29T00:00:01.000Z"),
  });
  const capacityModuleUrl = new URL(
    "../../../../packages/evidence/dist/src/reconciliation-index-capacity.js",
    import.meta.url,
  ).href;
  const capacityModule = await import(capacityModuleUrl) as {
    withLowerEvidenceReconciliationClaimLimitForTest<T extends object>(
      options: T,
      maximumClaims: number,
    ): T;
  };
  const reconciliationIndex = openEvidenceReconciliationIndex(
    capacityModule.withLowerEvidenceReconciliationClaimLimitForTest(
      {
        rootDirectory: join(root, "reconciliation"),
        ledger,
        now: () => new Date("2026-08-29T00:00:02.000Z"),
      },
      1,
    ),
  );
  assert.equal(reconciliationIndex.claim({
    idempotencyKey: `gis-ai-go:ik:v1:${"7".repeat(64)}`,
    operation: "data.query",
    requestId: "candidate-capacity-request-001",
    traceId: "7".repeat(32),
    resourceId: PUBLIC_READ_ONS_RESOURCE.resource_id,
    normalisedParametersSha256: "7".repeat(64),
  }).status, "claimed");

  const assembly = createCandidateActivation(
    snapshot,
    ledger,
    reconciliationIndex,
    CACHE_RECORD,
  );
  assert.deepEqual(assessGovernedCandidateReadiness(assembly), {
    status: "blocked",
    reason: "reconciliation-capacity-exhausted",
    productionRegistration: false,
    activeTools: V02_TARGET_ACTIVE_TOOL_NAMES,
    activeApiOperations: V02_TARGET_ACTIVE_TOOL_NAMES,
  });
  assertCandidateContainerAuthority(assembly);
});

test("rejects substituted cache material and any additional activation argument", async (t) => {
  const { snapshot, ledger, reconciliationIndex } = await activation(t);
  const changed = structuredClone(CACHE_RECORD) as unknown as Record<string, unknown>;
  const observation = changed.observation as Record<string, unknown>;
  observation.value = "10472";
  assert.throws(
    () => createCandidateActivation(
      snapshot,
      ledger,
      reconciliationIndex,
      changed as unknown as ApprovedOnsDataQueryCacheRecord,
    ),
    /Approved ONS cache observation is invalid/u,
  );
  assert.throws(
    () => (createCandidateActivation as unknown as (...values: unknown[]) => unknown)(
      snapshot,
      ledger,
      reconciliationIndex,
      CACHE_RECORD,
      { suspendedTools: ["data.query"] },
    ),
    /exact fixed input tuple/u,
  );
});
