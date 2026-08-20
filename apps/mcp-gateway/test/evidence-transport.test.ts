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

import { openPublicEvidenceLedger } from "@gis-ai-go/evidence";

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

function evidenceFixture(t: TestContext): EvidenceFixture {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-evidence-transport-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
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
  return {
    root,
    receiptId: persisted.evidence_receipt.receipt_id,
    application: createEvidenceInspectApplication(restarted),
    catalogueApplication,
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
): Promise<Record<string, unknown>> {
  const method = body.method as string;
  const response = await handler.fetch(rawRequest(body, method, name));
  assert.equal(response.status, 200);
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
  const fixture = evidenceFixture(t);
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
  const validation = await fromJsonSchema(
    EVIDENCE_OPERATION_JSON_SCHEMAS["evidence.inspect"].outputSchema as JsonSchemaType,
  )["~standard"].validate(
    fixture.application.inspect({ receipt_id: fixture.receiptId }, CONTEXT),
  );
  assert.equal("issues" in validation, false, JSON.stringify(validation));

  const handler = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    evidenceApplication: fixture.application,
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
