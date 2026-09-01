import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import test, { type TestContext } from "node:test";

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
  LOCAL_CANDIDATE_HOST,
  LOCAL_CANDIDATE_DATA_QUERY_SOURCE,
  LOCAL_CANDIDATE_LIFECYCLE_SCHEMA,
  LOCAL_CANDIDATE_PORT,
  LOCAL_CANDIDATE_PROVIDER_OBSERVATION,
  LOCAL_CANDIDATE_STATE_ROOT_MODE,
  LOCAL_CANDIDATE_TARGET_RELEASE,
  assertFixedLocalCandidateArguments,
  createProviderFreeLocalCandidateAssembly,
  createRetryableLocalCandidateStateCleanup,
  localCandidateLifecycleRecord,
  localCandidateProviderTransportAttemptCount,
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

async function localAssembly(t: TestContext) {
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
  );
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
