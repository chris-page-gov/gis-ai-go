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
import { fileURLToPath } from "node:url";
import test, { type TestContext } from "node:test";

import {
  InMemoryTransport,
  fromJsonSchema,
  type JSONRPCMessage,
  type JsonSchemaType,
  type McpHttpHandler,
} from "@modelcontextprotocol/server";

import { getPublicReadAuthorityContext } from "@gis-ai-go/authority-context";
import {
  PUBLIC_READ_ONS_RESOURCE,
  buildPublicReadReceipt,
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
  publicReadResultEvidenceBinding,
} from "@gis-ai-go/evidence";
import {
  PUBLIC_READ_POLICY,
  evaluatePublicReadPolicy,
} from "@gis-ai-go/policy-client";

import { createCatalogueApplication } from "../src/catalogue-application.js";
import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";
import { createEvidenceInspectApplication } from "../src/evidence-application.js";
import { createGatewayHttpHandler } from "../src/http-app.js";
import { createCatalogueMcpHttpHandler } from "../src/mcp-http.js";
import {
  MCP_EVIDENCE_INPUT_SCHEMAS,
  MCP_EVIDENCE_OUTPUT_SCHEMAS,
  MCP_EVIDENCE_RECEIPT_URI_TEMPLATE,
  MCP_PROTOCOL_VERSION,
} from "../src/mcp-server.js";
import { startCatalogueStdio } from "../src/mcp-stdio.js";
import {
  EVIDENCE_OPERATION_JSON_SCHEMAS,
  createCatalogueOpenApiDocument,
} from "../src/openapi.js";

const SOURCE_CATALOGUE = fileURLToPath(
  new URL("../../../../artifacts/okf/", import.meta.url),
);
const SNAPSHOT = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
  now: new Date("2026-08-20T12:00:00Z"),
});
const CONTEXT = Object.freeze({
  requestId: "evidence-transport-request-001",
  traceId: "4123456789abcdef0123456789abcdef",
  instance: "/evidence/inspect",
});
const MODERN_META = Object.freeze({
  "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
  "io.modelcontextprotocol/clientCapabilities": Object.freeze({}),
  "io.modelcontextprotocol/clientInfo": Object.freeze({
    name: "gis-ai-go-evidence-test-client",
    version: "1.0.0",
  }),
});

interface EvidenceFixture {
  readonly root: string;
  readonly receiptId: string;
  readonly application: ReturnType<typeof createEvidenceInspectApplication>;
  readonly catalogueApplication: ReturnType<typeof createCatalogueApplication>;
}

interface PublicReadEvidenceFixture {
  readonly root: string;
  readonly receiptId: string;
  readonly idempotencyKey: string;
  readonly application: ReturnType<typeof createEvidenceInspectApplication>;
}

function evidenceFixture(t: TestContext): EvidenceFixture {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-evidence-transport-"));
  const indexRoot = `${root}-reconciliation`;
  t.after(() => {
    rmSync(root, { recursive: true, force: true });
    rmSync(indexRoot, { recursive: true, force: true });
  });
  const ledger = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 365,
    now: () => new Date("2026-08-20T12:34:57Z"),
  });
  const catalogueApplication = createCatalogueApplication(SNAPSHOT, {
    software: {
      name: "gis-ai-go-mcp-gateway",
      version: "0.1.0",
      revision: SNAPSHOT.revision,
    },
    now: () => new Date("2026-08-20T12:34:56Z"),
    evidenceLedger: ledger,
  });
  const persisted = catalogueApplication.search(
    { query: "INSPIRE", limit: 1 },
    {
      requestId: "evidence-persistence-request-001",
      traceId: "5123456789abcdef0123456789abcdef",
    },
  );
  assert.ok(persisted.evidence_storage);
  const restarted = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 365,
    now: () => new Date("2026-08-21T12:00:00Z"),
  });
  assert.equal(restarted.verify().event_count, 1);
  const reconciliation = openEvidenceReconciliationIndex({
    rootDirectory: indexRoot,
    ledger: restarted,
  });
  return {
    root,
    receiptId: persisted.evidence_receipt.receipt_id,
    application: createEvidenceInspectApplication(restarted, reconciliation),
    catalogueApplication,
  };
}

function publicReadEvidenceFixture(t: TestContext): PublicReadEvidenceFixture {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-public-read-transport-"));
  const indexRoot = `${root}-reconciliation`;
  t.after(() => {
    rmSync(root, { recursive: true, force: true });
    rmSync(indexRoot, { recursive: true, force: true });
  });
  const ledger = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 365,
    now: () => new Date("2026-08-20T19:00:01Z"),
  });
  const requestId = "request-public-read-transport-001";
  const traceId = "6123456789abcdef0123456789abcdef";
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
    revision: "d".repeat(40),
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
  const idempotencyKey = `gis-ai-go:ik:v1:${"8".repeat(64)}`;
  const reconciliation = openEvidenceReconciliationIndex({
    rootDirectory: indexRoot,
    ledger,
    now: () => new Date("2026-08-20T19:00:00Z"),
  });
  const claim = reconciliation.claim({
    idempotencyKey,
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
  const restarted = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 365,
    now: () => new Date("2026-08-21T19:00:00Z"),
  });
  const restartedReconciliation = openEvidenceReconciliationIndex({
    rootDirectory: indexRoot,
    ledger: restarted,
  });
  assert.equal(restarted.verify().event_count, 1);
  return {
    root,
    receiptId: receipt.receipt_id,
    idempotencyKey,
    application: createEvidenceInspectApplication(restarted, restartedReconciliation),
  };
}

function directRequest(body: unknown): Request {
  return new Request("http://127.0.0.1:8787/evidence/inspect", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      host: "127.0.0.1:8787",
      "x-request-id": CONTEXT.requestId,
    },
    body: JSON.stringify(body),
  });
}

function rawBody(
  id: number,
  method: string,
  params: Readonly<Record<string, unknown>>,
): Record<string, unknown> {
  return {
    jsonrpc: "2.0",
    id,
    method,
    params: { _meta: MODERN_META, ...params },
  };
}

function rawRequest(
  body: unknown,
  method: string,
  name?: string,
): Request {
  return new Request("http://127.0.0.1:8787/mcp", {
    method: "POST",
    headers: {
      accept: "application/json, text/event-stream",
      "content-type": "application/json",
      "mcp-protocol-version": MCP_PROTOCOL_VERSION,
      "mcp-method": method,
      ...(name === undefined ? {} : { "mcp-name": name }),
    },
    body: JSON.stringify(body),
  });
}

async function rawExchange(
  handler: McpHttpHandler,
  body: Record<string, unknown>,
  name?: string,
  expectedStatus = 200,
): Promise<Record<string, unknown>> {
  const method = body.method as string;
  const response = await handler.fetch(rawRequest(body, method, name));
  assert.equal(response.status, expectedStatus);
  return await response.json() as Record<string, unknown>;
}

function result(message: Record<string, unknown>): Record<string, unknown> {
  assert.equal(typeof message.result, "object");
  assert.notEqual(message.result, null);
  return message.result as Record<string, unknown>;
}

function toolResult(message: Record<string, unknown>): Record<string, unknown> {
  const candidate = result(message);
  assert.ok(Array.isArray(candidate.content));
  return candidate;
}

function nextMessage(transport: InMemoryTransport): Promise<JSONRPCMessage> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(
      () => reject(new Error("Timed out waiting for evidence STDIO reply")),
      2_000,
    );
    transport.onmessage = (message) => {
      clearTimeout(timer);
      resolve(message);
    };
  });
}

async function stdioExchange(
  transport: InMemoryTransport,
  message: JSONRPCMessage,
): Promise<JSONRPCMessage> {
  const reply = nextMessage(transport);
  await transport.send(message);
  return reply;
}

function resourceUri(receiptId: string): string {
  return MCP_EVIDENCE_RECEIPT_URI_TEMPLATE.replace(
    "{receipt_id}",
    encodeURIComponent(receiptId),
  );
}

function corruptFirstEvent(root: string): void {
  const name = readdirSync(join(root, "events"))[0];
  assert.ok(name);
  const path = join(root, "events", name);
  const bytes = readFileSync(path, "utf8");
  writeFileSync(path, bytes.slice(0, -1));
}

test("keeps evidence inspection absent without explicit applications and activation", () => {
  assert.throws(
    () => createGatewayHttpHandler({
      snapshot: SNAPSHOT,
      enabledApiOperations: ["evidence.inspect"],
    }),
    /evidenceApplication is required/u,
  );
  assert.throws(
    () => createCatalogueMcpHttpHandler({
      application: createCatalogueApplication(SNAPSHOT, {
        software: {
          name: "gis-ai-go-mcp-gateway",
          version: "0.1.0",
          revision: SNAPSHOT.revision,
        },
      }),
      snapshot: SNAPSHOT,
      enabledOperations: ["evidence.inspect"],
    }),
    /evidenceApplication must implement inspection/u,
  );
});

test("publishes self-contained exact evidence schemas only on the explicit route", async (t) => {
  const fixtureV1 = evidenceFixture(t);
  const fixtureV2 = publicReadEvidenceFixture(t);
  const document = createCatalogueOpenApiDocument(["evidence.inspect"]);
  assert.deepEqual(Object.keys(document.paths).sort(), [
    "/evidence/inspect",
    "/healthz",
    "/openapi.json",
    "/readyz",
  ]);
  const components = (document.components as {
    schemas: Record<string, unknown>;
  }).schemas;
  assert.deepEqual(
    components.EvidenceInspectRequest,
    EVIDENCE_OPERATION_JSON_SCHEMAS["evidence.inspect"].inputSchema,
  );
  assert.deepEqual(
    components.EvidenceInspectResult,
    EVIDENCE_OPERATION_JSON_SCHEMAS["evidence.inspect"].outputSchema,
  );
  assert.deepEqual(
    MCP_EVIDENCE_INPUT_SCHEMAS["evidence.inspect"],
    EVIDENCE_OPERATION_JSON_SCHEMAS["evidence.inspect"].inputSchema,
  );
  assert.deepEqual(
    MCP_EVIDENCE_OUTPUT_SCHEMAS["evidence.inspect"],
    EVIDENCE_OPERATION_JSON_SCHEMAS["evidence.inspect"].outputSchema,
  );
  const serialised = JSON.stringify(
    EVIDENCE_OPERATION_JSON_SCHEMAS["evidence.inspect"].outputSchema,
  );
  const references = serialised.match(/"\$ref":"([^"]+)"/gu) ?? [];
  assert.ok(references.length > 0);
  assert.ok(references.every((reference) => reference.includes('"#/$defs/')));
  const outputSchema = EVIDENCE_OPERATION_JSON_SCHEMAS["evidence.inspect"].outputSchema;
  assert.equal(
    outputSchema.$id,
    "urn:gis-ai-go:schema:evidence-inspect-operation-result:v1",
  );
  assert.equal(Array.isArray(outputSchema.oneOf), true);
  const outputValidator = fromJsonSchema(
    EVIDENCE_OPERATION_JSON_SCHEMAS["evidence.inspect"].outputSchema as JsonSchemaType,
  );
  for (const [fixture, expectedSchema] of [
    [fixtureV1, "gis-ai-go.evidence-inspect-result.v1"],
    [fixtureV2, "gis-ai-go.evidence-inspect-result.v2"],
  ] as const) {
    const result = fixture.application.inspect(
      { receipt_id: fixture.receiptId },
      CONTEXT,
    );
    assert.equal(result.schema, expectedSchema);
    const validation = await outputValidator["~standard"].validate(result);
    assert.equal("issues" in validation, false, JSON.stringify(validation));
  }

  const handler = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    evidenceApplication: fixtureV1.application,
    enabledApiOperations: ["evidence.inspect"],
    createTraceId: () => CONTEXT.traceId,
  });
  const readiness = await handler(
    new Request("http://127.0.0.1:8787/readyz", {
      headers: { host: "127.0.0.1:8787" },
    }),
  );
  assert.equal(readiness.status, 503);
  assert.deepEqual(await readiness.json(), {
    status: "blocked",
    reason: "transport-and-interoperability-unverified",
    active_tools: [],
    active_api_operations: [],
  });
});

test("keeps direct, MCP HTTP, STDIO, resource and plain-text evidence byte-equivalent", async (t) => {
  const fixture = evidenceFixture(t);
  const direct = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    application: fixture.catalogueApplication,
    evidenceApplication: fixture.application,
    enabledApiOperations: ["evidence.inspect"],
    createTraceId: () => CONTEXT.traceId,
  });
  const directResponse = await direct(
    directRequest({ receipt_id: fixture.receiptId }),
  );
  assert.equal(directResponse.status, 200);
  const directResult = await directResponse.json() as Record<string, unknown>;
  assert.deepEqual(
    directResult,
    fixture.application.inspect({ receipt_id: fixture.receiptId }, CONTEXT),
  );

  const handler = createCatalogueMcpHttpHandler({
    application: fixture.catalogueApplication,
    evidenceApplication: fixture.application,
    snapshot: SNAPSHOT,
    enabledOperations: ["evidence.inspect"],
    enabledResources: ["evidence.receipt"],
    createRequestContext: () => CONTEXT,
  });
  t.after(() => handler.close());
  const called = await rawExchange(
    handler,
    rawBody(1, "tools/call", {
      name: "evidence.inspect",
      arguments: { receipt_id: fixture.receiptId },
    }),
    "evidence.inspect",
  );
  const calledResult = toolResult(called);
  assert.deepEqual(calledResult.structuredContent, directResult);
  assert.equal(
    (calledResult.content as { readonly text?: string }[])[0]?.text,
    JSON.stringify(directResult),
  );

  const uri = resourceUri(fixture.receiptId);
  const read = await rawExchange(
    handler,
    rawBody(2, "resources/read", { uri }),
    uri,
  );
  const contents = result(read).contents as { readonly text?: string }[];
  assert.equal(contents[0]?.text, JSON.stringify(directResult));

  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const stdio = startCatalogueStdio({
    application: fixture.catalogueApplication,
    evidenceApplication: fixture.application,
    snapshot: SNAPSHOT,
    enabledOperations: ["evidence.inspect"],
    createRequestContext: () => CONTEXT,
    transport: serverTransport,
  });
  t.after(async () => {
    await stdio.close();
    await clientTransport.close();
  });
  const stdioReply = await stdioExchange(clientTransport, {
    jsonrpc: "2.0",
    id: 3,
    method: "tools/call",
    params: {
      _meta: MODERN_META,
      name: "evidence.inspect",
      arguments: { receipt_id: fixture.receiptId },
    },
  });
  assert.equal("result" in stdioReply, true);
  if ("result" in stdioReply) {
    assert.deepEqual(stdioReply.result.structuredContent, directResult);
    assert.equal(
      (stdioReply.result.content as { readonly text?: string }[])[0]?.text,
      JSON.stringify(directResult),
    );
  }
});

test("reconciles a completed data query by key across direct, MCP HTTP and STDIO", async (t) => {
  const fixture = publicReadEvidenceFixture(t);
  const reported: Error[] = [];
  const catalogue = createCatalogueApplication(SNAPSHOT, {
    software: {
      name: "gis-ai-go-mcp-gateway",
      version: "0.1.0",
      revision: SNAPSHOT.revision,
    },
  });
  const completedRequest = {
    schema: "gis-ai-go.evidence-inspect-request.v2",
    source_operation: "data.query",
    idempotency_key: fixture.idempotencyKey,
  } as const;
  const missingRequest = {
    ...completedRequest,
    idempotency_key: `gis-ai-go:ik:v1:${"7".repeat(64)}`,
  } as const;
  const direct = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    evidenceApplication: fixture.application,
    enabledApiOperations: ["evidence.inspect"],
    createTraceId: () => CONTEXT.traceId,
  });
  const directCompleted = await direct(directRequest(completedRequest));
  assert.equal(directCompleted.status, 200);
  const completed = await directCompleted.json() as Record<string, unknown>;
  assert.equal(completed.schema, "gis-ai-go.evidence-inspect-result.v2");
  assert.equal(
    ((completed.data as { record: { receipt: { receipt_id: string } } }).record.receipt)
      .receipt_id,
    fixture.receiptId,
  );
  assert.equal(JSON.stringify(completed).includes(fixture.idempotencyKey), false);
  const directMissing = await direct(directRequest(missingRequest));
  assert.equal(directMissing.status, 404);
  const missingProblem = await directMissing.json() as Record<string, unknown>;
  assert.equal(missingProblem.code, "evidence_not_found");
  assert.equal(JSON.stringify(missingProblem).includes(missingRequest.idempotency_key), false);

  const mcp = createCatalogueMcpHttpHandler({
    application: catalogue,
    evidenceApplication: fixture.application,
    snapshot: SNAPSHOT,
    enabledOperations: ["evidence.inspect"],
    enabledResources: ["evidence.receipt"],
    createRequestContext: () => CONTEXT,
    onerror: (error) => reported.push(error),
  });
  t.after(() => mcp.close());
  const templates = await rawExchange(
    mcp,
    rawBody(39, "resources/templates/list", {}),
  );
  const resourceTemplates = (result(templates).resourceTemplates ?? []) as {
    readonly uriTemplate: string;
  }[];
  assert.deepEqual(
    resourceTemplates.map(({ uriTemplate }) => uriTemplate),
    [MCP_EVIDENCE_RECEIPT_URI_TEMPLATE],
  );
  assert.equal(JSON.stringify(resourceTemplates).includes("idempotency"), false);
  assert.equal(JSON.stringify(resourceTemplates).includes(fixture.idempotencyKey), false);
  const unsafeResourceUri =
    `gis-ai-go://evidence/receipts/${encodeURIComponent(fixture.idempotencyKey)}`;
  const unsafeResource = await rawExchange(
    mcp,
    rawBody(44, "resources/read", { uri: unsafeResourceUri }),
    unsafeResourceUri,
    400,
  );
  assert.equal("error" in unsafeResource, true);
  assert.equal(JSON.stringify(unsafeResource).includes(fixture.idempotencyKey), false);
  assert.equal(
    JSON.stringify(unsafeResource).includes(encodeURIComponent(fixture.idempotencyKey)),
    false,
  );
  for (const [id, request, expected, isError] of [
    [40, completedRequest, completed, false],
    [41, missingRequest, missingProblem, true],
  ] as const) {
    const reply = await rawExchange(
      mcp,
      rawBody(id, "tools/call", {
        name: "evidence.inspect",
        arguments: request,
      }),
      "evidence.inspect",
    );
    const called = toolResult(reply);
    assert.deepEqual(called.structuredContent, expected);
    assert.equal(called.isError, isError ? true : undefined);
    assert.equal(JSON.stringify(called).includes(request.idempotency_key), false);
  }

  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const stdio = startCatalogueStdio({
    application: catalogue,
    evidenceApplication: fixture.application,
    snapshot: SNAPSHOT,
    enabledOperations: ["evidence.inspect"],
    enabledResources: ["evidence.receipt"],
    createRequestContext: () => CONTEXT,
    onerror: (error) => reported.push(error),
    transport: serverTransport,
  });
  t.after(async () => {
    await stdio.close();
    await clientTransport.close();
  });
  for (const [id, request, expected, isError] of [
    [42, completedRequest, completed, false],
    [43, missingRequest, missingProblem, true],
  ] as const) {
    const reply = await stdioExchange(clientTransport, {
      jsonrpc: "2.0",
      id,
      method: "tools/call",
      params: {
        _meta: MODERN_META,
        name: "evidence.inspect",
        arguments: request,
      },
    });
    assert.equal("result" in reply, true);
    if (!("result" in reply)) continue;
    assert.deepEqual(reply.result.structuredContent, expected);
    assert.equal(reply.result.isError, isError ? true : undefined);
    assert.equal(JSON.stringify(reply.result).includes(request.idempotency_key), false);
  }
  const stdioUnsafeResource = await stdioExchange(clientTransport, {
    jsonrpc: "2.0",
    id: 46,
    method: "resources/read",
    params: {
      _meta: MODERN_META,
      uri: unsafeResourceUri,
    },
  });
  assert.equal("error" in stdioUnsafeResource, true);
  assert.equal(JSON.stringify(stdioUnsafeResource).includes(fixture.idempotencyKey), false);
  assert.equal(
    JSON.stringify(stdioUnsafeResource).includes(encodeURIComponent(fixture.idempotencyKey)),
    false,
  );
  assert.deepEqual(reported, []);
});

test("maps v2 linked-ledger corruption to unavailable across every operation face", async (t) => {
  const fixture = publicReadEvidenceFixture(t);
  const catalogue = createCatalogueApplication(SNAPSHOT, {
    software: {
      name: "gis-ai-go-mcp-gateway",
      version: "0.1.0",
      revision: SNAPSHOT.revision,
    },
  });
  const request = {
    schema: "gis-ai-go.evidence-inspect-request.v2",
    source_operation: "data.query",
    idempotency_key: fixture.idempotencyKey,
  } as const;
  corruptFirstEvent(fixture.root);

  const direct = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    evidenceApplication: fixture.application,
    enabledApiOperations: ["evidence.inspect"],
    createTraceId: () => CONTEXT.traceId,
  });
  const directResponse = await direct(directRequest(request));
  assert.equal(directResponse.status, 503);
  const directProblem = await directResponse.json() as Record<string, unknown>;
  assert.equal(directProblem.code, "evidence_unavailable");
  assert.equal(JSON.stringify(directProblem).includes(fixture.idempotencyKey), false);
  assert.equal(JSON.stringify(directProblem).includes(fixture.root), false);

  const mcp = createCatalogueMcpHttpHandler({
    application: catalogue,
    evidenceApplication: fixture.application,
    snapshot: SNAPSHOT,
    enabledOperations: ["evidence.inspect"],
    createRequestContext: () => CONTEXT,
  });
  t.after(() => mcp.close());
  const mcpReply = await rawExchange(
    mcp,
    rawBody(44, "tools/call", {
      name: "evidence.inspect",
      arguments: request,
    }),
    "evidence.inspect",
  );
  const mcpProblem = toolResult(mcpReply);
  assert.equal(mcpProblem.isError, true);
  assert.deepEqual(mcpProblem.structuredContent, directProblem);
  assert.equal(
    (mcpProblem.content as { readonly text?: string }[])[0]?.text,
    JSON.stringify(directProblem),
  );
  assert.equal(JSON.stringify(mcpProblem).includes(fixture.idempotencyKey), false);
  assert.equal(JSON.stringify(mcpProblem).includes(fixture.root), false);

  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const stdio = startCatalogueStdio({
    application: catalogue,
    evidenceApplication: fixture.application,
    snapshot: SNAPSHOT,
    enabledOperations: ["evidence.inspect"],
    createRequestContext: () => CONTEXT,
    transport: serverTransport,
  });
  t.after(async () => {
    await stdio.close();
    await clientTransport.close();
  });
  const stdioReply = await stdioExchange(clientTransport, {
    jsonrpc: "2.0",
    id: 45,
    method: "tools/call",
    params: {
      _meta: MODERN_META,
      name: "evidence.inspect",
      arguments: request,
    },
  });
  assert.equal("result" in stdioReply, true);
  if ("result" in stdioReply) {
    assert.equal(stdioReply.result.isError, true);
    assert.deepEqual(stdioReply.result.structuredContent, directProblem);
    assert.equal(
      (stdioReply.result.content as { readonly text?: string }[])[0]?.text,
      JSON.stringify(directProblem),
    );
    assert.equal(JSON.stringify(stdioReply.result).includes(fixture.idempotencyKey), false);
    assert.equal(JSON.stringify(stdioReply.result).includes(fixture.root), false);
  }
});

test("returns closed missing, invalid and corruption problems without reflecting inputs", async (t) => {
  const fixture = evidenceFixture(t);
  const direct = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    evidenceApplication: fixture.application,
    enabledApiOperations: ["evidence.inspect"],
    createTraceId: () => CONTEXT.traceId,
  });
  const mcp = createCatalogueMcpHttpHandler({
    application: fixture.catalogueApplication,
    evidenceApplication: fixture.application,
    snapshot: SNAPSHOT,
    enabledOperations: ["evidence.inspect"],
    createRequestContext: () => CONTEXT,
  });
  t.after(() => mcp.close());

  const missingId = `gis-ai-go:evidence-receipt:sha256:${"0".repeat(64)}`;
  for (const [requestBody, status, code] of [
    [{ receipt_id: "../../private/receipt" }, 400, "invalid_request"],
    [{ receipt_id: missingId }, 404, "evidence_not_found"],
  ] as const) {
    const directResponse = await direct(directRequest(requestBody));
    assert.equal(directResponse.status, status);
    const directText = await directResponse.text();
    assert.equal(directText.includes(String(requestBody.receipt_id)), false);
    assert.equal(JSON.parse(directText).code, code);

    const mcpResponse = await rawExchange(
      mcp,
      rawBody(status, "tools/call", {
        name: "evidence.inspect",
        arguments: requestBody,
      }),
      "evidence.inspect",
    );
    const mcpResult = toolResult(mcpResponse);
    const structured = mcpResult.structuredContent as Record<string, unknown>;
    assert.equal(mcpResult.isError, true);
    assert.equal(structured.code, code);
    assert.equal(
      (mcpResult.content as { readonly text?: string }[])[0]?.text,
      JSON.stringify(structured),
    );
    assert.equal(JSON.stringify(mcpResult).includes(String(requestBody.receipt_id)), false);
  }

  corruptFirstEvent(fixture.root);
  const unavailable = await direct(
    directRequest({ receipt_id: fixture.receiptId }),
  );
  assert.equal(unavailable.status, 503);
  const unavailableText = await unavailable.text();
  assert.equal(JSON.parse(unavailableText).code, "evidence_unavailable");
  assert.equal(unavailableText.includes(fixture.root), false);

  const mcpUnavailable = await rawExchange(
    mcp,
    rawBody(503, "tools/call", {
      name: "evidence.inspect",
      arguments: { receipt_id: fixture.receiptId },
    }),
    "evidence.inspect",
  );
  const unavailableResult = toolResult(mcpUnavailable);
  assert.equal(
    (unavailableResult.structuredContent as Record<string, unknown>).code,
    "evidence_unavailable",
  );
  assert.equal(JSON.stringify(unavailableResult).includes(fixture.root), false);
});
