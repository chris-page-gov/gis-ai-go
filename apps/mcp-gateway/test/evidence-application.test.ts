import assert from "node:assert/strict";
import {
  mkdtempSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { getPublicReadAuthorityContext } from "@gis-ai-go/authority-context";
import {
  PUBLIC_READ_ONS_RESOURCE,
  PublicEvidenceLedgerError,
  buildPublicReadReceipt,
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
  publicIdempotencyKeySha256,
  publicReadResultEvidenceBinding,
  verifyEvidenceInspectionReceiptStructure,
} from "@gis-ai-go/evidence";
import {
  PUBLIC_READ_POLICY,
  evaluatePublicReadPolicy,
} from "@gis-ai-go/policy-client";

import { createCatalogueApplication } from "../src/catalogue-application.js";
import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";
import {
  EvidenceInspectError,
  createEvidenceInspectApplication,
} from "../src/evidence-application.js";

const SOURCE_CATALOGUE = fileURLToPath(
  new URL("../../../../artifacts/okf/", import.meta.url),
);
const SNAPSHOT = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
  now: new Date("2026-08-20T12:00:00Z"),
});
const CONTEXT = Object.freeze({
  requestId: "request-evidence-inspect-001",
  traceId: "2123456789abcdef0123456789abcdef",
});
const INSPECTION_OPTIONS = Object.freeze({
  software: Object.freeze({
    name: "gis-ai-go-mcp-gateway" as const,
    version: "0.1.0",
    revision: "e".repeat(40),
  }),
  now: () => new Date("2026-08-23T10:00:00.000Z"),
});

function expectInspectError(
  run: () => unknown,
  code: EvidenceInspectError["code"],
): void {
  assert.throws(run, (error: unknown) => {
    assert.ok(error instanceof EvidenceInspectError);
    assert.equal(error.code, code);
    return true;
  });
}

test("inspects one authorised open receipt without activating a transport", () => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-evidence-inspect-"));
  try {
    const ledger = openPublicEvidenceLedger({
      rootDirectory: root,
      retentionDays: 365,
      now: () => new Date("2026-08-20T12:34:57Z"),
    });
    const catalogue = createCatalogueApplication(SNAPSHOT, {
      software: {
        name: "gis-ai-go-mcp-gateway",
        version: "0.1.0",
        revision: "b".repeat(40),
      },
      now: () => new Date("2026-08-20T12:34:56Z"),
      evidenceLedger: ledger,
    });
    const catalogueResult = catalogue.search({ query: "INSPIRE", limit: 1 }, {
      requestId: "request-persist-before-inspect-001",
      traceId: "3123456789abcdef0123456789abcdef",
    });
    assert.ok(catalogueResult.evidence_storage);
    const eventCount = ledger.verify().event_count;

    const application = createEvidenceInspectApplication(
      ledger,
      undefined,
      INSPECTION_OPTIONS,
    );
    const result = application.inspect(
      { receipt_id: catalogueResult.evidence_receipt.receipt_id },
      CONTEXT,
    );
    assert.equal(result.schema, "gis-ai-go.evidence-inspect-result.v3");
    assert.equal(result.operation, "evidence.inspect");
    assert.equal(result.data.record.schema, "gis-ai-go.public-evidence-record.v1");
    assert.equal(
      result.data.record.receipt.receipt_id,
      catalogueResult.evidence_receipt.receipt_id,
    );
    assert.deepEqual(result.data.storage, catalogueResult.evidence_storage);
    assert.equal(result.verification.status, "passed");
    assert.equal(result.verification.ingest_material, "verified-at-ingest-not-retained");
    assert.equal(result.verification.attestation, "not-attested");
    assert.equal(verifyEvidenceInspectionReceiptStructure(result.evidence_receipt), true);
    assert.equal(result.evidence_receipt.request_id, CONTEXT.requestId);
    assert.equal(result.evidence_receipt.trace_id, CONTEXT.traceId);
    assert.equal(
      result.evidence_receipt.policy_decision.inspected_receipt_id,
      catalogueResult.evidence_receipt.receipt_id,
    );
    assert.equal(
      result.data.record.receipt.request_id,
      "request-persist-before-inspect-001",
    );
    assert.notEqual(
      result.evidence_receipt.trace_id,
      result.data.record.receipt.trace_id,
    );
    assert.equal(result.evidence_receipt.evidence_handling.ledger_event, "not-created");
    assert.equal(ledger.verify().event_count, eventCount);
    assert.equal(Object.isFrozen(result), true);

    for (const request of [
      {},
      { receipt_id: catalogueResult.evidence_receipt.receipt_id, extra: true },
      { receipt_id: catalogueResult.evidence_storage.record_id },
      { receipt_id: "../../private" },
    ]) {
      expectInspectError(() => application.inspect(request, CONTEXT), "invalid_request");
    }
    expectInspectError(
      () =>
        application.inspect(
          { receipt_id: `gis-ai-go:evidence-receipt:sha256:${"0".repeat(64)}` },
          CONTEXT,
        ),
      "evidence_not_found",
    );
    const eventName = readdirSync(join(root, "events"))[0]!;
    const eventPath = join(root, "events", eventName);
    const eventText = readFileSync(eventPath, "utf8");
    writeFileSync(eventPath, eventText.slice(0, -1));
    expectInspectError(
      () =>
        application.inspect(
          { receipt_id: catalogueResult.evidence_receipt.receipt_id },
          CONTEXT,
        ),
      "evidence_unavailable",
    );
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("inspects a durable public-read v2 receipt through the current v3 result", () => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-public-read-inspect-"));
  const indexRoot = `${root}-reconciliation`;
  try {
    const ledger = openPublicEvidenceLedger({
      rootDirectory: root,
      retentionDays: 365,
      now: () => new Date("2026-08-20T19:00:01Z"),
    });
    const requestId = "request-public-read-inspect-001";
    const traceId = "5123456789abcdef0123456789abcdef";
    const evaluation = evaluatePublicReadPolicy({
      requestId,
      traceId,
      operation: "data.query",
      resource: PUBLIC_READ_ONS_RESOURCE,
    });
    assert.ok(evaluation.decision);
    assert.equal(evaluation.allowed, true);
    const normalisedParameters = {
      schema: "gis-ai-go.data-query-parameters.v1",
      resource_id: PUBLIC_READ_ONS_RESOURCE.resource_id,
      dataset: {
        id: PUBLIC_READ_ONS_RESOURCE.dataset.id,
        edition: PUBLIC_READ_ONS_RESOURCE.dataset.edition,
        version: PUBLIC_READ_ONS_RESOURCE.dataset.version,
      },
      selections: PUBLIC_READ_ONS_RESOURCE.selections,
      limit: 1,
    };
    const resultCore = {
      schema: "gis-ai-go.data-query-result.v1",
      operation: "data.query",
      request_id: requestId,
      trace_id: traceId,
      evidence_binding: publicReadResultEvidenceBinding(),
      data: { status: "succeeded", observations: [{ value: "fixture" }] },
      warnings: [],
    };
    const authorityContext = getPublicReadAuthorityContext();
    const software = {
      name: "gis-ai-go-mcp-gateway" as const,
      version: "0.1.0",
      revision: "c".repeat(40),
    };
    const receipt = buildPublicReadReceipt({
      createdAt: "2026-08-20T19:00:00Z",
      requestId,
      traceId,
      operation: "data.query",
      normalisedParameters,
      authorityContext,
      publicPolicy: PUBLIC_READ_POLICY,
      policyDecision: evaluation.decision,
      resource: PUBLIC_READ_ONS_RESOURCE,
      transformations: [
        { name: "normalise-public-read-parameters", version: "v1" },
        { name: "execute-fixed-provider-query", version: "v1" },
        { name: "project-public-read-result-core", version: "v1" },
      ],
      software,
      resultCore,
    });
    const reconciliation = openEvidenceReconciliationIndex({
      rootDirectory: indexRoot,
      ledger,
      now: () => new Date("2026-08-20T19:00:00Z"),
    });
    const key = `gis-ai-go:ik:v1:${"c".repeat(64)}`;
    const claim = reconciliation.claim({
      idempotencyKey: key,
      operation: "data.query",
      requestId,
      traceId,
      resourceId: receipt.resource.resource_id,
      normalisedParametersSha256: receipt.operation.normalised_parameters.sha256,
    });
    assert.equal(claim.status, "claimed");
    if (claim.status !== "claimed") assert.fail("claim was not acquired");
    reconciliation.resolve(claim.claim, receipt);
    ledger.persistReceipt(receipt, {
      normalisedParameters,
      resultCore,
      publicPolicy: PUBLIC_READ_POLICY,
      expectedAuthorityContext: authorityContext,
      expectedPolicyDecision: evaluation.decision,
      expectedResource: PUBLIC_READ_ONS_RESOURCE,
      expectedSoftware: software,
    });

    const application = createEvidenceInspectApplication(
      ledger,
      reconciliation,
      INSPECTION_OPTIONS,
    );
    const inspected = application.inspect(
      { receipt_id: receipt.receipt_id },
      CONTEXT,
    );
    assert.equal(inspected.schema, "gis-ai-go.evidence-inspect-result.v3");
    assert.equal(inspected.data.record.schema, "gis-ai-go.public-evidence-record.v2");
    assert.equal(inspected.data.record.receipt.receipt_id, receipt.receipt_id);
    assert.equal(inspected.verification.status, "passed");

    const recovered = application.inspect(
      {
        schema: "gis-ai-go.evidence-inspect-request.v2",
        source_operation: "data.query",
        idempotency_key: key,
      },
      {
        requestId: "request-evidence-reconcile-002",
        traceId: "6123456789abcdef0123456789abcdef",
      },
    );
    assert.equal(recovered.schema, "gis-ai-go.evidence-inspect-result.v3");
    assert.equal(recovered.data.record.receipt.receipt_id, receipt.receipt_id);
    assert.equal(JSON.stringify(recovered).includes(key), false);
    assert.equal(
      JSON.stringify(recovered).includes(publicIdempotencyKeySha256(key)),
      false,
    );
    assert.deepEqual(recovered.evidence_receipt.transformations.slice(0, 2), [
      { name: "hash-public-idempotency-key", version: "v1" },
      { name: "resolve-evidence-reconciliation-index", version: "v1" },
    ]);
    assert.equal(ledger.verify().event_count, 1);

    expectInspectError(
      () =>
        application.inspect(
          {
            schema: "gis-ai-go.evidence-inspect-request.v2",
            source_operation: "data.query",
            idempotency_key: `gis-ai-go:ik:v1:${"d".repeat(64)}`,
          },
          CONTEXT,
        ),
      "evidence_not_found",
    );
    const pendingKey = `gis-ai-go:ik:v1:${"e".repeat(64)}`;
    assert.equal(
      reconciliation.claim({
        idempotencyKey: pendingKey,
        operation: "data.query",
        requestId: "request-pending-inspect",
        traceId: "7123456789abcdef0123456789abcdef",
        resourceId: receipt.resource.resource_id,
        normalisedParametersSha256: receipt.operation.normalised_parameters.sha256,
      }).status,
      "claimed",
    );
    expectInspectError(
      () =>
        application.inspect(
          {
            schema: "gis-ai-go.evidence-inspect-request.v2",
            source_operation: "data.query",
            idempotency_key: pendingKey,
          },
          CONTEXT,
        ),
      "evidence_unavailable",
    );
  } finally {
    rmSync(root, { recursive: true, force: true });
    rmSync(indexRoot, { recursive: true, force: true });
  }
});

test("rejects proxy-wrapped and non-exact evidence reconciliation dependencies", () => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-evidence-inspect-constructor-"));
  try {
    const ledger = openPublicEvidenceLedger({ rootDirectory: join(parent, "ledger") });
    const otherLedger = openPublicEvidenceLedger({
      rootDirectory: join(parent, "other-ledger"),
    });
    const reconciliation = openEvidenceReconciliationIndex({
      rootDirectory: join(parent, "reconciliation"),
      ledger,
    });
    const proxyLedger = new Proxy(ledger, {});
    let indexGets = 0;
    const proxyIndex = new Proxy(reconciliation, {
      get(target, property, receiver) {
        indexGets += 1;
        return Reflect.get(target, property, receiver);
      },
    });
    assert.throws(
      () => createEvidenceInspectApplication(proxyLedger, reconciliation, INSPECTION_OPTIONS),
      /requires a public evidence ledger/u,
    );
    assert.throws(
      () => createEvidenceInspectApplication(ledger, proxyIndex, INSPECTION_OPTIONS),
      /exact linked ledger and index/u,
    );
    assert.equal(indexGets, 0);
    assert.throws(
      () => createEvidenceInspectApplication(otherLedger, reconciliation, INSPECTION_OPTIONS),
      /exact linked ledger and index/u,
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("returns an inline receipt when the durable ledger is already at capacity", async () => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-evidence-inspect-capacity-"));
  try {
    const testSupportPath = new URL(
      "../../../../packages/evidence/dist/src/public-ledger-capacity.js",
      import.meta.url,
    ).href;
    const support = await import(testSupportPath) as {
      withLowerPublicEvidenceLedgerEventLimitForTest<T extends object>(
        options: T,
        maximumEvents: number,
      ): T;
    };
    const ledger = openPublicEvidenceLedger(
      support.withLowerPublicEvidenceLedgerEventLimitForTest(
        {
          rootDirectory: root,
          retentionDays: 365,
          now: () => new Date("2026-08-23T10:00:00.000Z"),
        },
        1,
      ),
    );
    const catalogue = createCatalogueApplication(SNAPSHOT, {
      software: INSPECTION_OPTIONS.software,
      now: () => new Date("2026-08-23T09:59:59.000Z"),
      evidenceLedger: ledger,
    });
    const persisted = catalogue.search({ query: "INSPIRE", limit: 1 }, {
      requestId: "request-fill-inspection-ledger-001",
      traceId: "9123456789abcdef0123456789abcdef",
    });
    assert.ok(persisted.evidence_storage);
    assert.throws(
      () => catalogue.search({ query: "INSPIRE", limit: 1 }, {
        requestId: "request-over-inspection-ledger-capacity",
        traceId: "a123456789abcdef0123456789abcdef",
      }),
      (error: unknown) => {
        assert.ok(error instanceof PublicEvidenceLedgerError);
        assert.equal(error.code, "capacity");
        return true;
      },
    );
    assert.equal(ledger.verify().event_count, 1);

    const inspector = createEvidenceInspectApplication(
      ledger,
      undefined,
      INSPECTION_OPTIONS,
    );
    const inspected = inspector.inspect(
      { receipt_id: persisted.evidence_receipt.receipt_id },
      CONTEXT,
    );
    assert.equal(inspected.schema, "gis-ai-go.evidence-inspect-result.v3");
    assert.equal(inspected.evidence_receipt.evidence_handling.ledger_event, "not-created");
    assert.equal(ledger.verify().event_count, 1);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});
