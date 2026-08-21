import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, readdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
} from "@gis-ai-go/evidence";
import {
  ONS_EGRESS_POLICY,
  OnsDataApiAdapter,
  type FixedHttpsResponse,
  type FixedHttpsTransport,
} from "@gis-ai-go/provider-adapter-sdk";

import {
  DataQueryApplicationError,
  PUBLIC_ONS_DATA_QUERY_PARAMETERS,
  createDataQueryApplication,
} from "../src/data-query-application.js";
import { createEvidenceInspectApplication } from "../src/evidence-application.js";

const IDEMPOTENCY_KEY = `gis-ai-go:ik:v1:${"6".repeat(64)}`;
const REQUEST = Object.freeze({
  schema: "gis-ai-go.data-query-request.v1" as const,
  idempotency_key: IDEMPOTENCY_KEY,
  parameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
});
const SOFTWARE = Object.freeze({
  name: "gis-ai-go-mcp-gateway" as const,
  version: "0.1.0",
  revision: "b2b72f09b2b72f09b2b72f09b2b72f09b2b72f09",
});
const FIRST_CONTEXT = Object.freeze({
  requestId: "qual-206-host-015-first",
  traceId: "6123456789abcdef0123456789abcdef",
  instance: "/data/query",
});
const RETRY_CONTEXT = Object.freeze({
  requestId: "qual-206-host-015-retry",
  traceId: "7123456789abcdef0123456789abcdef",
  instance: "/data/query",
});
const INSPECT_CONTEXT = Object.freeze({
  requestId: "qual-206-host-015-inspect",
  traceId: "8123456789abcdef0123456789abcdef",
  instance: "/evidence/inspect",
});

const PROVIDER_PAYLOAD = Object.freeze({
  dimensions: {
    causeofdeath: {
      option: {
        href: "http://api.beta.ons.gov.uk/v1/code-lists/cause-of-death/codes/all-causes",
        id: "all-causes",
      },
    },
    geography: {
      option: {
        href:
          "http://api.beta.ons.gov.uk/v1/code-lists/administrative-geography/" +
          "codes/E92000001",
        id: "E92000001",
      },
    },
    time: {
      option: {
        href: "http://api.beta.ons.gov.uk/v1/code-lists/calendar-years/codes/2026",
        id: "2026",
      },
    },
    week: {
      option: {
        href: "http://api.beta.ons.gov.uk/v1/code-lists/week-number/codes/week-24",
        id: "week-24",
      },
    },
  },
  limit: 10_000,
  links: {
    dataset_metadata: {
      href:
        "http://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/" +
        "editions/time-series/versions/121/metadata",
    },
    self: {
      href:
        "http://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/" +
        "editions/time-series/versions/121/observations?causeofdeath=all-causes&" +
        "geography=E92000001&time=2026&week=week-24",
    },
    version: {
      href:
        "http://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/" +
        "editions/time-series/versions/121",
      id: "121",
    },
  },
  observations: [{ metadata: { "Data Marking": "" }, observation: "10471" }],
  offset: 0,
  total_observations: 1,
});

function fixedResponse(): FixedHttpsResponse {
  const body = Buffer.from(JSON.stringify(PROVIDER_PAYLOAD), "utf8");
  return {
    status: 200,
    headers: Object.freeze({ "content-type": "application/json" }),
    body,
    telemetry: Object.freeze({
      dnsMs: 1,
      resolvedAddressCount: 1,
      selectedAddressFamily: 4,
      connectMs: 2,
      responseMs: 3,
      totalMs: 6,
      compressedBytes: body.byteLength,
      tlsProtocol: "TLSv1.3",
      tlsCipher: "TLS_AES_256_GCM_SHA384",
    }),
  };
}

function adapter(transport: FixedHttpsTransport): OnsDataApiAdapter {
  return new OnsDataApiAdapter({
    lifecycle: {
      discovery: "suspended",
      invocation: "active",
      reason: "Explicit deterministic QUAL-206 HOST-015 fixture.",
    },
    transport,
    now: () => Date.parse("2030-01-01T00:00:00Z"),
  });
}

function storedText(root: string): string {
  const visit = (directory: string): string[] => readdirSync(
    directory,
    { withFileTypes: true },
  ).flatMap((entry) => {
    const path = join(directory, entry.name);
    return entry.isDirectory() ? visit(path) : [readFileSync(path, "utf8")];
  });
  return visit(root).join("\n");
}

test("QUAL-206-HOST-015 drops a persisted response then reconciles after restart", async (t) => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-qual-host-015-"));
  t.after(() => rmSync(parent, { recursive: true, force: true }));
  const ledgerRoot = join(parent, "ledger");
  const indexRoot = join(parent, "reconciliation");
  const ledger = openPublicEvidenceLedger({
    rootDirectory: ledgerRoot,
    retentionDays: 365,
    now: () => new Date("2026-08-21T01:00:01.000Z"),
  });
  const index = openEvidenceReconciliationIndex({
    rootDirectory: indexRoot,
    ledger,
    now: () => new Date("2026-08-21T01:00:00.000Z"),
  });
  let providerExecutions = 0;
  const firstAdapter = adapter(async ({ policy, signal, url }) => {
    providerExecutions += 1;
    assert.equal(policy, ONS_EGRESS_POLICY);
    assert.equal(signal instanceof AbortSignal, true);
    assert.match(url, /^https:\/\/api\.beta\.ons\.gov\.uk\//u);
    return fixedResponse();
  });
  const firstApplication = createDataQueryApplication({
    adapter: firstAdapter,
    software: SOFTWARE,
    now: () => new Date("2026-08-21T01:00:00.000Z"),
    evidenceLedger: ledger,
    reconciliationIndex: index,
  });
  const responseDrop = new Error("fault-injected response drop after persistence");
  const invokeAcrossFaultBoundary = async (): Promise<never> => {
    await firstApplication.query(REQUEST, FIRST_CONTEXT);
    throw responseDrop;
  };
  await assert.rejects(invokeAcrossFaultBoundary, (error: unknown) => error === responseDrop);
  assert.equal(providerExecutions, 1);

  const restartedLedger = openPublicEvidenceLedger({
    rootDirectory: ledgerRoot,
    retentionDays: 365,
    now: () => new Date("2026-08-21T01:01:01.000Z"),
  });
  const restartedIndex = openEvidenceReconciliationIndex({
    rootDirectory: indexRoot,
    ledger: restartedLedger,
    now: () => new Date("2026-08-21T01:01:00.000Z"),
  });
  const retryAdapter = adapter(async () => {
    providerExecutions += 1;
    throw new Error("A completed retry must not execute the provider");
  });
  const providerPreflight: string[] = [];
  for (const method of ["health", "estimate", "licence_evidence", "provenance"] as const) {
    t.mock.method(retryAdapter, method, () => {
      providerPreflight.push(method);
      throw new Error("A completed retry must not run provider preflight");
    });
  }
  const retryApplication = createDataQueryApplication({
    adapter: retryAdapter,
    software: SOFTWARE,
    now: () => new Date("2026-08-21T01:01:00.000Z"),
    evidenceLedger: restartedLedger,
    reconciliationIndex: restartedIndex,
  });
  let completedProblem: DataQueryApplicationError | undefined;
  try {
    await retryApplication.query(REQUEST, RETRY_CONTEXT);
    assert.fail("A completed key must return a receipt-free 409");
  } catch (error) {
    assert.ok(error instanceof DataQueryApplicationError);
    completedProblem = error;
  }
  assert.ok(completedProblem);
  assert.equal(completedProblem.problem.status, 409);
  assert.equal(completedProblem.problem.code, "idempotency_completed");
  assert.equal(completedProblem.problem.schema, "gis-ai-go.data-query-reconciliation-problem.v1");
  const completedProblemText = JSON.stringify(completedProblem.problem);
  assert.equal(completedProblemText.includes(IDEMPOTENCY_KEY), false);
  assert.equal(completedProblemText.includes("evidence-receipt"), false);
  assert.equal(completedProblemText.includes("10471"), false);
  assert.deepEqual(providerPreflight, []);
  assert.equal(providerExecutions, 1);

  const inspector = createEvidenceInspectApplication(restartedLedger, restartedIndex);
  const inspection = inspector.inspect(
    {
      schema: "gis-ai-go.evidence-inspect-request.v2",
      source_operation: "data.query",
      idempotency_key: IDEMPOTENCY_KEY,
    },
    INSPECT_CONTEXT,
  );
  assert.equal(inspection.schema, "gis-ai-go.evidence-inspect-result.v2");
  assert.equal(inspection.data.record.receipt.operation.name, "data.query");
  assert.match(
    inspection.data.record.receipt.receipt_id,
    /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u,
  );
  assert.equal(JSON.stringify(inspection).includes(IDEMPOTENCY_KEY), false);
  assert.equal(JSON.stringify(inspection).includes("10471"), false);

  const ledgerHealth = restartedLedger.verify();
  const indexHealth = restartedIndex.verify();
  assert.equal(ledgerHealth.record_count, 1);
  assert.equal(ledgerHealth.event_count, 1);
  assert.equal(indexHealth.claim_count, 1);
  assert.equal(indexHealth.resolution_count, 1);
  assert.equal(indexHealth.completed_count, 1);
  assert.equal(indexHealth.pending_count, 0);
  const indexText = storedText(indexRoot);
  assert.equal(indexText.includes(IDEMPOTENCY_KEY), false);
  assert.equal(indexText.includes("10471"), false);
  assert.equal(indexText.includes('"observations"'), false);
});
