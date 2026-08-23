import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { request as nodeRequest, type Server } from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import test, { after, type TestContext } from "node:test";

import {
  InMemoryTransport,
  fromJsonSchema,
  type JSONRPCMessage,
  type JsonSchemaType,
  type McpHttpHandler,
} from "@modelcontextprotocol/server";

import {
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
  type PublicEvidenceLedger,
  type PublicEvidenceReconciliationIndex,
} from "@gis-ai-go/evidence";
import {
  FixedHttpsTransportError,
  ONS_CALL_DEADLINE_MS,
  ONS_EGRESS_POLICY,
  OnsDataApiAdapter,
  type FixedHttpsResponse,
  type FixedHttpsTransport,
  type ProviderAdapterExecutionOptions,
  type W3CTraceContext,
} from "@gis-ai-go/provider-adapter-sdk";

import { createCatalogueApplication } from "../src/catalogue-application.js";
import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";
import {
  DataQueryApplicationError,
  PUBLIC_ONS_DATA_QUERY_PARAMETERS,
  createDataQueryApplication,
  type DataQueryApplication,
  type DataQueryProblemCode,
} from "../src/data-query-application.js";
import {
  createEvidenceInspectApplication,
  type EvidenceInspectApplication,
} from "../src/evidence-application.js";
import { createGatewayHttpHandler } from "../src/http-app.js";
import { createCatalogueMcpHttpHandler } from "../src/mcp-http.js";
import {
  dataQueryRequestSignal,
  withMcpHttpDataQuerySignal,
} from "../src/mcp-request-signal.js";
import {
  GATEWAY_HEADER_BODY_TIMEOUT_MS,
  GATEWAY_PROCESSING_SOCKET_TIMEOUT_MS,
  createGatewayNodeServer,
} from "../src/http-server.js";
import {
  MCP_EVIDENCE_RECEIPT_URI_TEMPLATE,
  MCP_LEGACY_CONFORMANCE_ONLY,
  MCP_PROTOCOL_VERSION,
  MCP_PUBLIC_READ_INPUT_SCHEMAS,
  MCP_PUBLIC_READ_OUTPUT_SCHEMAS,
  createCatalogueLegacyConformanceMcpServerFactory,
} from "../src/mcp-server.js";
import { startCatalogueStdio } from "../src/mcp-stdio.js";
import {
  PUBLIC_READ_OPERATION_JSON_SCHEMAS,
  createCatalogueOpenApiDocument,
} from "../src/openapi.js";
import {
  createSelectionResolveApplication,
  type SelectionResolveRequest,
} from "../src/selection-application.js";

const SOURCE_CATALOGUE = fileURLToPath(
  new URL("../../../../artifacts/okf/", import.meta.url),
);
const SNAPSHOT = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
  now: new Date("2026-08-20T12:00:00Z"),
});
const SOFTWARE = Object.freeze({
  name: "gis-ai-go-mcp-gateway" as const,
  version: "0.1.0",
  revision: SNAPSHOT.revision,
});
const REQUEST_ID = "public-read-transport-request-001";
const TRACE_ID = "8123456789abcdef0123456789abcdef";
const MODERN_META = Object.freeze({
  "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
  "io.modelcontextprotocol/clientCapabilities": Object.freeze({}),
  "io.modelcontextprotocol/clientInfo": Object.freeze({
    name: "gis-ai-go-public-read-transport-test",
    version: "1.0.0",
  }),
});
const ACTIVE_INVOCATION = Object.freeze({
  discovery: "suspended",
  invocation: "active",
  reason: "Explicit inactive public-read transport test.",
} as const);
const DATA_QUERY_IDEMPOTENCY_KEY = `gis-ai-go:ik:v1:${"9".repeat(64)}`;
const DATA_QUERY_REQUEST = Object.freeze({
  schema: "gis-ai-go.data-query-request.v1" as const,
  idempotency_key: DATA_QUERY_IDEMPOTENCY_KEY,
  parameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
});
const GENERATED_DATA_ROOTS: string[] = [];
const RECONCILIATION_INDEXES = new WeakMap<
  PublicEvidenceLedger,
  PublicEvidenceReconciliationIndex
>();
const EVIDENCE_BY_DATA_APPLICATION = new WeakMap<
  DataQueryApplication,
  EvidenceInspectApplication
>();

after(() => {
  for (const root of GENERATED_DATA_ROOTS) {
    rmSync(root, { recursive: true, force: true });
  }
});

const SELECTION_REQUEST: SelectionResolveRequest = Object.freeze({
  question: "Weekly deaths for England in week 24 of 2026, all causes",
  candidate_record_ids: Object.freeze(["PV-ONS-DATA"]),
  constraints: Object.freeze({
    profile_ids: Object.freeze(["PV-ONS-DATA"]),
    provider_ids: Object.freeze(["ons-data-api"]),
    dataset_ids: Object.freeze(["weekly-deaths-region"]),
    editions: Object.freeze(["time-series"]),
    versions: Object.freeze(["121"]),
    dimensions: Object.freeze({
      time: Object.freeze(["2026"]),
      geography: Object.freeze(["E92000001"]),
      week: Object.freeze(["week-24"]),
      causeofdeath: Object.freeze(["all-causes"]),
    }),
  }),
});

const VALID_ONS_PAYLOAD = Object.freeze({
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

function fixedResponse(payload: unknown = VALID_ONS_PAYLOAD): FixedHttpsResponse {
  const body = Buffer.from(JSON.stringify(payload), "utf8");
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

function successTransport(): FixedHttpsTransport {
  return async ({ policy, url, signal }) => {
    assert.equal(policy, ONS_EGRESS_POLICY);
    assert.match(url, /^https:\/\/api\.beta\.ons\.gov\.uk\//u);
    assert.equal(signal instanceof AbortSignal, true);
    return fixedResponse();
  };
}

function adapter(transport: FixedHttpsTransport = successTransport()): OnsDataApiAdapter {
  return new OnsDataApiAdapter({
    lifecycle: ACTIVE_INVOCATION,
    transport,
    now: () => Date.parse("2030-01-01T00:00:00Z"),
  });
}

function catalogueApplication() {
  return createCatalogueApplication(SNAPSHOT, {
    software: SOFTWARE,
    now: () => new Date("2026-08-21T01:00:00.000Z"),
  });
}

function selectionApplication(evidenceLedger?: ReturnType<typeof openPublicEvidenceLedger>) {
  return createSelectionResolveApplication({
    software: SOFTWARE,
    now: () => new Date("2026-08-21T01:00:00.000Z"),
    ...(evidenceLedger === undefined ? {} : { evidenceLedger }),
  });
}

function dataApplication(
  transport: FixedHttpsTransport = successTransport(),
  evidenceLedger?: ReturnType<typeof openPublicEvidenceLedger>,
  observeExecutionOptions?: (options: ProviderAdapterExecutionOptions) => void,
): DataQueryApplication {
  let ledger = evidenceLedger;
  if (ledger === undefined) {
    const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-public-read-data-"));
    GENERATED_DATA_ROOTS.push(parent);
    ledger = openPublicEvidenceLedger({
      rootDirectory: join(parent, "ledger"),
      retentionDays: 365,
      now: () => new Date("2026-08-21T01:00:01.000Z"),
    });
  }
  let reconciliationIndex = RECONCILIATION_INDEXES.get(ledger);
  if (reconciliationIndex === undefined) {
    reconciliationIndex = openEvidenceReconciliationIndex({
      rootDirectory: `${ledger.storageRootDirectory()}-reconciliation`,
      ledger,
    });
    RECONCILIATION_INDEXES.set(ledger, reconciliationIndex);
  }
  const providerAdapter = adapter(transport);
  if (observeExecutionOptions !== undefined) {
    const execute = providerAdapter.execute.bind(providerAdapter);
    Object.defineProperty(providerAdapter, "execute", {
      configurable: true,
      value: async (
        request: unknown,
        options: ProviderAdapterExecutionOptions = {},
      ) => {
        observeExecutionOptions(options);
        return await execute(request, options);
      },
    });
  }
  const application = createDataQueryApplication({
    adapter: providerAdapter,
    software: SOFTWARE,
    now: () => new Date("2026-08-21T01:00:00.000Z"),
    evidenceLedger: ledger,
    reconciliationIndex,
  });
  EVIDENCE_BY_DATA_APPLICATION.set(
    application,
    createEvidenceInspectApplication(ledger, reconciliationIndex),
  );
  return application;
}

function evidenceForData(application: DataQueryApplication): EvidenceInspectApplication {
  const evidence = EVIDENCE_BY_DATA_APPLICATION.get(application);
  assert.ok(evidence !== undefined);
  return evidence;
}

function evidenceApplication(ledger: PublicEvidenceLedger) {
  const reconciliationIndex = RECONCILIATION_INDEXES.get(ledger) ??
    openEvidenceReconciliationIndex({
      rootDirectory: `${ledger.storageRootDirectory()}-reconciliation`,
      ledger,
    });
  RECONCILIATION_INDEXES.set(ledger, reconciliationIndex);
  return createEvidenceInspectApplication(ledger, reconciliationIndex);
}

function directRequest(
  path: "/selection/resolve" | "/data/query" | "/evidence/inspect",
  body: unknown,
  signal?: AbortSignal,
): Request {
  return new Request(`http://127.0.0.1:8787${path}`, {
    method: "POST",
    headers: {
      accept: "application/json",
      "content-type": "application/json",
      host: "127.0.0.1:8787",
      "x-request-id": REQUEST_ID,
    },
    body: JSON.stringify(body),
    ...(signal === undefined ? {} : { signal }),
  });
}

function rawBody(
  id: number,
  method: string,
  params: Readonly<Record<string, unknown>> = {},
): Record<string, unknown> {
  return {
    jsonrpc: "2.0",
    id,
    method,
    params: { _meta: MODERN_META, ...params },
  };
}

function rawRequest(
  body: Record<string, unknown>,
  name?: string,
  signal?: AbortSignal,
): Request {
  const method = String(body.method);
  return new Request("http://127.0.0.1:8787/mcp", {
    method: "POST",
    headers: {
      accept: "application/json, text/event-stream",
      "content-type": "application/json",
      "mcp-method": method,
      ...(name === undefined ? {} : { "mcp-name": name }),
      "mcp-protocol-version": MCP_PROTOCOL_VERSION,
    },
    body: JSON.stringify(body),
    ...(signal === undefined ? {} : { signal }),
  });
}

async function rawExchange(
  handler: McpHttpHandler,
  body: Record<string, unknown>,
  name?: string,
): Promise<Record<string, unknown>> {
  const response = await handler.fetch(rawRequest(body, name));
  assert.equal(response.status, 200);
  return await response.json() as Record<string, unknown>;
}

function toolResult(message: Record<string, unknown>): Record<string, unknown> {
  assert.equal(typeof message.result, "object");
  assert.notEqual(message.result, null);
  return message.result as Record<string, unknown>;
}

function nextMessage(transport: InMemoryTransport): Promise<JSONRPCMessage> {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(
      () => reject(new Error("Timed out waiting for public-read STDIO reply")),
      2_000,
    );
    transport.onmessage = (message) => {
      clearTimeout(timeout);
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

function collectReferences(value: unknown, references: string[] = []): readonly string[] {
  if (Array.isArray(value)) {
    value.forEach((item) => collectReferences(item, references));
  } else if (value !== null && typeof value === "object") {
    for (const [key, item] of Object.entries(value)) {
      if (key === "$ref" && typeof item === "string") references.push(item);
      else collectReferences(item, references);
    }
  }
  return references;
}

function context(operation: "selection.resolve" | "data.query" | "evidence.inspect") {
  return {
    requestId: REQUEST_ID,
    traceId: TRACE_ID,
    instance: operation === "selection.resolve"
      ? "/selection/resolve"
      : operation === "data.query"
        ? "/data/query"
        : "/evidence/inspect",
  };
}

function deferred<T>(): {
  readonly promise: Promise<T>;
  readonly resolve: (value: T) => void;
} {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((complete) => {
    resolve = complete;
  });
  return { promise, resolve };
}

function cancellationTransport(
  started: ReturnType<typeof deferred<AbortSignal>>,
  finished?: ReturnType<typeof deferred<void>>,
): FixedHttpsTransport {
  return async ({ signal }) => {
    assert.ok(signal instanceof AbortSignal);
    started.resolve(signal);
    try {
      return await new Promise<FixedHttpsResponse>((_resolve, reject) => {
        const abort = (): void => reject(new FixedHttpsTransportError("aborted"));
        signal.addEventListener("abort", abort, { once: true });
        if (signal.aborted) abort();
      });
    } finally {
      finished?.resolve(undefined);
    }
  };
}

async function listen(server: Server): Promise<number> {
  await new Promise<void>((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolve);
  });
  const address = server.address();
  assert.ok(address !== null && typeof address === "object");
  return address.port;
}

test("keeps public-read capabilities absent by default and requires explicit applications", async (t) => {
  const direct = createGatewayHttpHandler({ snapshot: SNAPSHOT });
  const blocked = await direct(directRequest("/selection/resolve", SELECTION_REQUEST));
  assert.equal(blocked.status, 400);
  assert.equal((await blocked.json() as { code?: unknown }).code, "invalid_request");

  assert.throws(
    () => createGatewayHttpHandler({
      snapshot: SNAPSHOT,
      enabledApiOperations: ["selection.resolve"],
    }),
    /selectionApplication is required/u,
  );
  assert.throws(
    () => createGatewayHttpHandler({
      snapshot: SNAPSHOT,
      enabledApiOperations: ["data.query"],
    }),
    /linked evidence\.inspect operation/u,
  );

  const mcp = createCatalogueMcpHttpHandler({
    application: catalogueApplication(),
    snapshot: SNAPSHOT,
  });
  t.after(() => mcp.close());
  const discovered = await rawExchange(mcp, rawBody(1, "server/discover"));
  assert.deepEqual(
    (discovered.result as { capabilities?: unknown }).capabilities,
    {},
  );
  assert.equal(
    (discovered.result as { instructions?: unknown }).instructions,
    "No tools or resources are registered. This candidate remains inactive.",
  );
  assert.throws(
    () => createCatalogueMcpHttpHandler({
      application: catalogueApplication(),
      snapshot: SNAPSHOT,
      enabledOperations: ["data.query"],
    }),
    /linked evidence\.inspect operation/u,
  );

  const selectionOnly = createCatalogueMcpHttpHandler({
    application: catalogueApplication(),
    selectionApplication: selectionApplication(),
    snapshot: SNAPSHOT,
    enabledOperations: ["selection.resolve"],
  });
  t.after(() => selectionOnly.close());
  const selectionDiscovery = await rawExchange(
    selectionOnly,
    rawBody(2, "server/discover"),
  );
  const selectionInstructions = String(
    (selectionDiscovery.result as { instructions?: unknown }).instructions,
  );
  assert.match(selectionInstructions, /non-executing selection planning/u);
  assert.doesNotMatch(selectionInstructions, /ONS query/u);
  assert.doesNotMatch(selectionInstructions, /verified public evidence/u);

  const data = dataApplication();
  assert.throws(
    () => createGatewayHttpHandler({
      snapshot: SNAPSHOT,
      dataQueryApplication: data,
      enabledApiOperations: ["data.query"],
    }),
    /linked evidence\.inspect operation/u,
  );
  assert.throws(
    () => createCatalogueMcpHttpHandler({
      application: catalogueApplication(),
      dataQueryApplication: data,
      snapshot: SNAPSHOT,
      enabledOperations: ["data.query"],
    }),
    /linked evidence\.inspect operation/u,
  );

  const dataWithRecovery = createCatalogueMcpHttpHandler({
    application: catalogueApplication(),
    dataQueryApplication: data,
    evidenceApplication: evidenceForData(data),
    snapshot: SNAPSHOT,
    enabledOperations: ["data.query", "evidence.inspect"],
  });
  t.after(() => dataWithRecovery.close());
  const dataDiscovery = await rawExchange(
    dataWithRecovery,
    rawBody(3, "server/discover"),
  );
  const dataInstructions = String(
    (dataDiscovery.result as { instructions?: unknown }).instructions,
  );
  assert.match(dataInstructions, /one exact bounded public ONS query/u);
  assert.doesNotMatch(dataInstructions, /selection planning/u);

  const pairRoot = mkdtempSync(join(tmpdir(), "gis-ai-go-reconciliation-pair-"));
  t.after(() => rmSync(pairRoot, { recursive: true, force: true }));
  const dataLedger = openPublicEvidenceLedger({
    rootDirectory: join(pairRoot, "data-ledger"),
    retentionDays: 365,
    now: () => new Date("2026-08-21T01:00:01.000Z"),
  });
  const inspectLedger = openPublicEvidenceLedger({
    rootDirectory: join(pairRoot, "inspect-ledger"),
    retentionDays: 365,
    now: () => new Date("2026-08-21T01:00:01.000Z"),
  });
  const mismatchedData = dataApplication(successTransport(), dataLedger);
  const mismatchedEvidence = evidenceApplication(inspectLedger);
  assert.throws(
    () => createGatewayHttpHandler({
      snapshot: SNAPSHOT,
      dataQueryApplication: mismatchedData,
      evidenceApplication: mismatchedEvidence,
      enabledApiOperations: ["data.query", "evidence.inspect"],
    }),
    /exact shared reconciliation index/u,
  );
  assert.throws(
    () => createCatalogueMcpHttpHandler({
      application: catalogueApplication(),
      snapshot: SNAPSHOT,
      dataQueryApplication: mismatchedData,
      evidenceApplication: mismatchedEvidence,
      enabledOperations: ["data.query", "evidence.inspect"],
    }),
    /exact shared reconciliation index/u,
  );

  const linkedEvidence = evidenceApplication(dataLedger);
  assert.throws(
    () => createGatewayHttpHandler({
      snapshot: SNAPSHOT,
      dataQueryApplication: new Proxy(mismatchedData, {}),
      evidenceApplication: linkedEvidence,
      enabledApiOperations: ["data.query", "evidence.inspect"],
    }),
    /ledger-linked reconciliation application/u,
  );
  assert.throws(
    () => createCatalogueMcpHttpHandler({
      application: catalogueApplication(),
      snapshot: SNAPSHOT,
      dataQueryApplication: mismatchedData,
      evidenceApplication: new Proxy(linkedEvidence, {}),
      enabledOperations: ["data.query", "evidence.inspect"],
    }),
    /ledger-linked reconciliation application/u,
  );
});

test("propagates exact Trace Context across direct, MCP HTTP and STDIO boundaries", async (t) => {
  const observedTrace: W3CTraceContext[] = [];
  const transportKeys: (readonly PropertyKey[])[] = [];
  const transportSerialisations: string[] = [];
  const transport: FixedHttpsTransport = async (request) => {
    transportKeys.push(Reflect.ownKeys(request).sort());
    transportSerialisations.push(JSON.stringify(request));
    return await successTransport()(request);
  };
  const application = dataApplication(transport, undefined, (options) => {
    assert.ok(options.trace !== undefined);
    observedTrace.push(options.trace);
  });
  const evidenceApplication = evidenceForData(application);
  const query = (seed: string) => ({
    ...DATA_QUERY_REQUEST,
    idempotency_key: `gis-ai-go:ik:v1:${seed.repeat(64)}`,
  });

  const directParentId = "1".repeat(16);
  const directTrace = Object.freeze({
    traceparent: `00-${TRACE_ID}-${directParentId}-02`,
  });
  const direct = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    dataQueryApplication: application,
    evidenceApplication,
    enabledApiOperations: ["data.query", "evidence.inspect"],
    createRequestId: () => `${REQUEST_ID}-direct`,
    createTraceId: () => TRACE_ID,
    createTraceParentId: () => directParentId,
  });
  const callerTrace = `00-${"c".repeat(32)}-${"d".repeat(16)}-ff`;
  const directResponse = await direct(
    new Request("http://127.0.0.1:8787/data/query", {
      method: "POST",
      headers: {
        accept: "application/json",
        authorization: "Bearer caller-controlled-secret",
        baggage: "private-path=/tmp/caller-controlled",
        "content-type": "application/json",
        host: "127.0.0.1:8787",
        traceparent: callerTrace,
        tracestate: "caller=controlled",
      },
      body: JSON.stringify(query("1")),
    }),
  );
  assert.equal(directResponse.status, 200);
  const directText = await directResponse.text();
  assert.equal(directText.includes(callerTrace), false);
  assert.equal(directText.includes("caller-controlled"), false);

  const mcpTraceId = "9".repeat(32);
  const mcpTrace = Object.freeze({
    traceparent: `00-${mcpTraceId}-${"a".repeat(16)}-ff`,
    tracestate: "\t,0gov@uk=public-read ,ons=weekly-deaths, ",
  });
  const mcp = createCatalogueMcpHttpHandler({
    application: catalogueApplication(),
    dataQueryApplication: application,
    evidenceApplication,
    snapshot: SNAPSHOT,
    enabledOperations: ["data.query", "evidence.inspect"],
    createRequestContext: () => ({
      requestId: `${REQUEST_ID}-mcp`,
      traceId: mcpTraceId,
      trace: mcpTrace,
      instance: "/data/query",
    }),
  });
  t.after(() => mcp.close());
  const mcpResponse = await rawExchange(
    mcp,
    rawBody(81, "tools/call", {
      name: "data.query",
      arguments: query("2"),
    }),
    "data.query",
  );
  assert.equal(toolResult(mcpResponse).isError, undefined);

  const stdioTraceId = "a".repeat(32);
  const stdioTrace = Object.freeze({
    traceparent: `00-${stdioTraceId}-${"b".repeat(16)}-03`,
    tracestate: "",
  });
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const stdio = startCatalogueStdio({
    application: catalogueApplication(),
    dataQueryApplication: application,
    evidenceApplication,
    snapshot: SNAPSHOT,
    enabledOperations: ["data.query", "evidence.inspect"],
    createRequestContext: () => ({
      requestId: `${REQUEST_ID}-stdio`,
      traceId: stdioTraceId,
      trace: stdioTrace,
      instance: "/data/query",
    }),
    transport: serverTransport,
  });
  t.after(async () => {
    await stdio.close();
    await clientTransport.close();
  });
  const stdioResponse = await stdioExchange(clientTransport, {
    jsonrpc: "2.0",
    id: 82,
    method: "tools/call",
    params: {
      _meta: MODERN_META,
      name: "data.query",
      arguments: query("3"),
    },
  });
  assert.equal("result" in stdioResponse, true);

  assert.deepEqual(observedTrace, [directTrace, mcpTrace, stdioTrace]);
  assert.equal(observedTrace.every((trace) => Object.isFrozen(trace)), true);
  assert.deepEqual(transportKeys, [
    ["policy", "signal", "url"],
    ["policy", "signal", "url"],
    ["policy", "signal", "url"],
  ]);
  assert.equal(
    transportSerialisations.some((request) =>
      request.includes("traceparent") ||
      request.includes("tracestate") ||
      request.includes("authorization") ||
      request.includes("caller-controlled")
    ),
    false,
  );
});

test("never reflects a raw idempotency key through request contexts", async (t) => {
  const rawKey = DATA_QUERY_IDEMPOTENCY_KEY;
  const nameLikeCallerRequestId = "Chris-Page-Personal-Request";
  const generatedRequestId = "server-data-query-request-001";
  let providerExecutions = 0;
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-request-id-privacy-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const ledger = openPublicEvidenceLedger({
    rootDirectory: join(root, "ledger"),
    retentionDays: 365,
    now: () => new Date("2026-08-21T01:00:01.000Z"),
  });
  const application = dataApplication(async (request) => {
    providerExecutions += 1;
    return await successTransport()(request);
  }, ledger);
  const reported: unknown[] = [];
  const direct = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    dataQueryApplication: application,
    evidenceApplication: evidenceForData(application),
    enabledApiOperations: ["data.query", "evidence.inspect"],
    createRequestId: () => generatedRequestId,
    createTraceId: () => TRACE_ID,
    onerror: (error) => reported.push(error),
  });
  const hostileDirectRequest = (callerRequestId: string) =>
    new Request("http://127.0.0.1:8787/data/query", {
    method: "POST",
    headers: {
      accept: "application/json",
      "content-type": "application/json",
      host: "127.0.0.1:8787",
      "x-request-id": callerRequestId,
    },
    body: JSON.stringify(DATA_QUERY_REQUEST),
  });
  const success = await direct(hostileDirectRequest(nameLikeCallerRequestId));
  assert.equal(success.status, 200);
  const successText = await success.text();
  assert.equal(successText.includes(rawKey), false);
  assert.equal(successText.includes(nameLikeCallerRequestId), false);
  assert.equal(
    (JSON.parse(successText) as { request_id: string }).request_id,
    generatedRequestId,
  );
  const retry = await direct(hostileDirectRequest(`prefix-${rawKey}`));
  assert.equal(retry.status, 409);
  const retryText = await retry.text();
  assert.equal(retryText.includes(rawKey), false);
  assert.equal(
    (JSON.parse(retryText) as { code: string }).code,
    "idempotency_completed",
  );
  assert.equal(providerExecutions, 1);
  assert.equal(JSON.stringify(reported).includes(rawKey), false);
  assert.equal(JSON.stringify(reported).includes(nameLikeCallerRequestId), false);
  const storedLookup = RECONCILIATION_INDEXES.get(ledger)!.lookup(rawKey);
  assert.equal(storedLookup.status, "completed");
  assert.equal(JSON.stringify(storedLookup).includes(rawKey), false);
  assert.equal(JSON.stringify(storedLookup).includes(nameLikeCallerRequestId), false);
  if (storedLookup.status === "completed") {
    assert.equal(storedLookup.claim.request_id, generatedRequestId);
    assert.equal(storedLookup.stored.record.receipt.request_id, generatedRequestId);
  }

  let hostileApplicationEgress = 0;
  const hostileApplication = dataApplication(async (request) => {
    hostileApplicationEgress += 1;
    return await successTransport()(request);
  });
  await assert.rejects(
    hostileApplication.query(DATA_QUERY_REQUEST, {
      requestId: `prefix-${rawKey}`,
      traceId: TRACE_ID,
      instance: "/data/query",
    }),
    (error: unknown) => {
      assert.ok(error instanceof TypeError);
      assert.equal(error.message.includes(rawKey), false);
      return true;
    },
  );
  await assert.rejects(
    hostileApplication.query(DATA_QUERY_REQUEST, {
      requestId: REQUEST_ID,
      traceId: TRACE_ID,
      instance: `/data/${rawKey}`,
    }),
    (error: unknown) => {
      assert.ok(error instanceof TypeError);
      assert.equal(error.message.includes(rawKey), false);
      return true;
    },
  );
  assert.equal(hostileApplicationEgress, 0);

  const mcpReported: unknown[] = [];
  const mcp = createCatalogueMcpHttpHandler({
    application: catalogueApplication(),
    dataQueryApplication: hostileApplication,
    evidenceApplication: evidenceForData(hostileApplication),
    snapshot: SNAPSHOT,
    enabledOperations: ["data.query", "evidence.inspect"],
    createRequestContext: () => ({
      requestId: `prefix-${rawKey}`,
      traceId: TRACE_ID,
      instance: "/data/query",
    }),
    onerror: (error) => mcpReported.push(error),
  });
  t.after(() => mcp.close());
  const body = rawBody(8, "tools/call", {
    name: "data.query",
    arguments: DATA_QUERY_REQUEST,
  });
  const mcpResponse = await mcp.fetch(rawRequest(body, "data.query"));
  const mcpText = await mcpResponse.text();
  assert.equal(mcpText.includes(rawKey), false);
  assert.equal(JSON.stringify(mcpReported).includes(rawKey), false);
  assert.equal(hostileApplicationEgress, 0);
});

test("publishes self-contained OpenAPI and identical MCP schemas with every status", async () => {
  assert.throws(
    () => createCatalogueOpenApiDocument(["data.query"]),
    /linked evidence\.inspect operation/u,
  );
  const document = createCatalogueOpenApiDocument([
    "evidence.inspect",
    "selection.resolve",
    "data.query",
  ]);
  assert.deepEqual(Object.keys(document.paths).sort(), [
    "/data/query",
    "/evidence/inspect",
    "/healthz",
    "/openapi.json",
    "/readyz",
    "/selection/resolve",
  ]);
  assert.ok(collectReferences(document).length > 0);
  assert.equal(
    collectReferences(document).every((reference) => reference.startsWith("#")),
    true,
  );
  assert.deepEqual(
    MCP_PUBLIC_READ_INPUT_SCHEMAS["selection.resolve"],
    PUBLIC_READ_OPERATION_JSON_SCHEMAS["selection.resolve"].inputSchema,
  );
  assert.deepEqual(
    MCP_PUBLIC_READ_OUTPUT_SCHEMAS["selection.resolve"],
    PUBLIC_READ_OPERATION_JSON_SCHEMAS["selection.resolve"].outputSchema,
  );
  assert.deepEqual(
    MCP_PUBLIC_READ_INPUT_SCHEMAS["data.query"],
    PUBLIC_READ_OPERATION_JSON_SCHEMAS["data.query"].inputSchema,
  );
  assert.deepEqual(
    MCP_PUBLIC_READ_OUTPUT_SCHEMAS["data.query"],
    PUBLIC_READ_OPERATION_JSON_SCHEMAS["data.query"].outputSchema,
  );

  const paths = document.paths as Record<string, {
    post: { responses: Record<string, unknown> };
  }>;
  assert.deepEqual(Object.keys(paths["/selection/resolve"]!.post.responses), [
    "200", "400", "404", "406", "409", "422", "429", "500", "503",
  ]);
  assert.deepEqual(Object.keys(paths["/data/query"]!.post.responses), [
    "200", "400", "403", "406", "408", "409", "429", "500", "502", "503", "504",
  ]);

  const selection = selectionApplication().resolve(
    SELECTION_REQUEST,
    context("selection.resolve"),
  );
  assert.equal(selection.schema, "gis-ai-go.selection-resolve-result.v1");
  const data = await dataApplication().query(
    DATA_QUERY_REQUEST,
    context("data.query"),
  );
  for (const [operation, value] of [
    ["selection.resolve", selection],
    ["data.query", data],
  ] as const) {
    const validator = fromJsonSchema(
      PUBLIC_READ_OPERATION_JSON_SCHEMAS[operation].outputSchema as JsonSchemaType,
    );
    const validation = await validator["~standard"].validate(value);
    assert.equal("issues" in validation, false, JSON.stringify(validation));
    assert.equal(
      collectReferences(PUBLIC_READ_OPERATION_JSON_SCHEMAS[operation].outputSchema)
        .every((reference) => reference.startsWith("#/$defs/")),
      true,
    );
  }
});

test("keeps direct and MCP HTTP success and problem JSON exactly equivalent", async (t) => {
  const selection = selectionApplication();
  const directData = dataApplication();
  const mcpData = dataApplication();
  const direct = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    selectionApplication: selection,
    dataQueryApplication: directData,
    evidenceApplication: evidenceForData(directData),
    enabledApiOperations: ["selection.resolve", "data.query", "evidence.inspect"],
    createRequestId: () => REQUEST_ID,
    createTraceId: () => TRACE_ID,
  });
  const mcp = createCatalogueMcpHttpHandler({
    application: catalogueApplication(),
    selectionApplication: selection,
    dataQueryApplication: mcpData,
    evidenceApplication: evidenceForData(mcpData),
    snapshot: SNAPSHOT,
    enabledOperations: ["selection.resolve", "data.query", "evidence.inspect"],
    createRequestContext: (operation) => context(
      operation as "selection.resolve" | "data.query",
    ),
  });
  t.after(() => mcp.close());
  const expected = new Map<string, Record<string, unknown>>();

  for (const [id, operation, path, argumentsValue] of [
    [10, "selection.resolve", "/selection/resolve", SELECTION_REQUEST],
    [11, "data.query", "/data/query", DATA_QUERY_REQUEST],
  ] as const) {
    const directResponse = await direct(directRequest(path, argumentsValue));
    assert.equal(directResponse.status, 200);
    const directResult = await directResponse.json() as Record<string, unknown>;
    expected.set(`${operation}:success`, directResult);
    const mcpResponse = await rawExchange(
      mcp,
      rawBody(id, "tools/call", {
        name: operation,
        arguments: argumentsValue,
      }),
      operation,
    );
    const called = toolResult(mcpResponse);
    assert.deepEqual(called.structuredContent, directResult);
    assert.equal(
      (called.content as { readonly text?: string }[])[0]?.text,
      JSON.stringify(directResult),
    );
    assert.equal(called.isError, undefined);
  }

  for (const [id, operation, path, argumentsValue] of [
    [12, "selection.resolve", "/selection/resolve", { unexpected: true }],
    [
      13,
      "data.query",
      "/data/query",
      {
        ...DATA_QUERY_REQUEST,
        parameters: { ...PUBLIC_ONS_DATA_QUERY_PARAMETERS, limit: 2 },
      },
    ],
  ] as const) {
    const directResponse = await direct(directRequest(path, argumentsValue));
    assert.equal(directResponse.status, 400);
    assert.match(
      directResponse.headers.get("content-type") ?? "",
      /^application\/problem\+json/u,
    );
    const directProblem = await directResponse.json() as Record<string, unknown>;
    expected.set(`${operation}:problem`, directProblem);
    const mcpResponse = await rawExchange(
      mcp,
      rawBody(id, "tools/call", {
        name: operation,
        arguments: argumentsValue,
      }),
      operation,
    );
    const called = toolResult(mcpResponse);
    assert.equal(called.isError, true);
    assert.deepEqual(called.structuredContent, directProblem);
    assert.equal(
      (called.content as { readonly text?: string }[])[0]?.text,
      JSON.stringify(directProblem),
    );
  }

  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const stdioData = dataApplication();
  const stdio = startCatalogueStdio({
    application: catalogueApplication(),
    selectionApplication: selection,
    dataQueryApplication: stdioData,
    evidenceApplication: evidenceForData(stdioData),
    snapshot: SNAPSHOT,
    enabledOperations: ["selection.resolve", "data.query", "evidence.inspect"],
    createRequestContext: (operation) => context(
      operation as "selection.resolve" | "data.query",
    ),
    transport: serverTransport,
  });
  t.after(async () => {
    await stdio.close();
    await clientTransport.close();
  });
  for (const [id, operation, argumentsValue, outcome] of [
    [14, "selection.resolve", SELECTION_REQUEST, "success"],
    [15, "data.query", DATA_QUERY_REQUEST, "success"],
    [16, "selection.resolve", { unexpected: true }, "problem"],
    [
      17,
      "data.query",
      {
        ...DATA_QUERY_REQUEST,
        parameters: { ...PUBLIC_ONS_DATA_QUERY_PARAMETERS, limit: 2 },
      },
      "problem",
    ],
  ] as const) {
    const reply = await stdioExchange(clientTransport, {
      jsonrpc: "2.0",
      id,
      method: "tools/call",
      params: {
        _meta: MODERN_META,
        name: operation,
        arguments: argumentsValue,
      },
    });
    assert.equal("result" in reply, true);
    if (!("result" in reply)) return;
    const wanted = expected.get(`${operation}:${outcome}`);
    assert.ok(wanted);
    assert.deepEqual(reply.result.structuredContent, wanted);
    assert.equal(
      (reply.result.content as { readonly text?: string }[])[0]?.text,
      JSON.stringify(wanted),
    );
    assert.equal(reply.result.isError, outcome === "problem" ? true : undefined);
  }
});

test("reconciles a dropped data.query success without replaying provider results", async (t) => {
  let providerExecutions = 0;
  const countedTransport: FixedHttpsTransport = async (request) => {
    providerExecutions += 1;
    return await successTransport()(request);
  };
  const createSlice = () => {
    const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-lost-response-transport-"));
    t.after(() => rmSync(parent, { recursive: true, force: true }));
    const ledger = openPublicEvidenceLedger({
      rootDirectory: join(parent, "ledger"),
      retentionDays: 365,
      now: () => new Date("2026-08-21T01:00:01.000Z"),
    });
    const data = dataApplication(countedTransport, ledger);
    return {
      data,
      evidence: evidenceApplication(ledger),
      ledger,
    };
  };
  const inspectRequest = {
    schema: "gis-ai-go.evidence-inspect-request.v2",
    source_operation: "data.query",
    idempotency_key: DATA_QUERY_IDEMPOTENCY_KEY,
  } as const;
  const completedProblems: Record<string, unknown>[] = [];

  const directSlice = createSlice();
  const direct = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    dataQueryApplication: directSlice.data,
    evidenceApplication: directSlice.evidence,
    enabledApiOperations: ["data.query", "evidence.inspect"],
    createRequestId: () => REQUEST_ID,
    createTraceId: () => TRACE_ID,
  });
  const droppedDirectSuccess = await direct(directRequest("/data/query", DATA_QUERY_REQUEST));
  assert.equal(droppedDirectSuccess.status, 200);
  const directSuccess = await droppedDirectSuccess.json() as {
    evidence_receipt: { receipt_id: string };
  };
  const directRetry = await direct(directRequest("/data/query", DATA_QUERY_REQUEST));
  assert.equal(directRetry.status, 409);
  const directProblem = await directRetry.json() as Record<string, unknown>;
  assert.equal(directProblem.code, "idempotency_completed");
  completedProblems.push(directProblem);
  const directInspection = await direct(directRequest("/evidence/inspect", inspectRequest));
  assert.equal(directInspection.status, 200);
  const directEvidence = await directInspection.json() as {
    data: { record: { receipt: { receipt_id: string } } };
  };
  assert.equal(
    directEvidence.data.record.receipt.receipt_id,
    directSuccess.evidence_receipt.receipt_id,
  );
  assert.equal(directSlice.ledger.verify().event_count, 1);

  const mcpSlice = createSlice();
  const mcp = createCatalogueMcpHttpHandler({
    application: catalogueApplication(),
    dataQueryApplication: mcpSlice.data,
    evidenceApplication: mcpSlice.evidence,
    snapshot: SNAPSHOT,
    enabledOperations: ["data.query", "evidence.inspect"],
    createRequestContext: (operation) => context(
      operation as "data.query" | "evidence.inspect",
    ),
  });
  t.after(() => mcp.close());
  const droppedMcpSuccess = toolResult(await rawExchange(
    mcp,
    rawBody(180, "tools/call", {
      name: "data.query",
      arguments: DATA_QUERY_REQUEST,
    }),
    "data.query",
  ));
  const mcpReceiptId = (
    droppedMcpSuccess.structuredContent as {
      evidence_receipt: { receipt_id: string };
    }
  ).evidence_receipt.receipt_id;
  const mcpRetry = toolResult(await rawExchange(
    mcp,
    rawBody(181, "tools/call", {
      name: "data.query",
      arguments: DATA_QUERY_REQUEST,
    }),
    "data.query",
  ));
  assert.equal(mcpRetry.isError, true);
  const mcpProblem = mcpRetry.structuredContent as Record<string, unknown>;
  assert.equal(mcpProblem.code, "idempotency_completed");
  assert.equal(
    (mcpRetry.content as { readonly text?: string }[])[0]?.text,
    JSON.stringify(mcpProblem),
  );
  completedProblems.push(mcpProblem);
  const mcpInspection = toolResult(await rawExchange(
    mcp,
    rawBody(182, "tools/call", {
      name: "evidence.inspect",
      arguments: inspectRequest,
    }),
    "evidence.inspect",
  ));
  assert.equal(
    ((mcpInspection.structuredContent as {
      data: { record: { receipt: { receipt_id: string } } };
    }).data.record.receipt.receipt_id),
    mcpReceiptId,
  );
  assert.equal(mcpSlice.ledger.verify().event_count, 1);

  const stdioSlice = createSlice();
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const stdio = startCatalogueStdio({
    application: catalogueApplication(),
    dataQueryApplication: stdioSlice.data,
    evidenceApplication: stdioSlice.evidence,
    snapshot: SNAPSHOT,
    enabledOperations: ["data.query", "evidence.inspect"],
    createRequestContext: (operation) => context(
      operation as "data.query" | "evidence.inspect",
    ),
    transport: serverTransport,
  });
  t.after(async () => {
    await stdio.close();
    await clientTransport.close();
  });
  const stdioCall = async (id: number, name: "data.query" | "evidence.inspect", args: unknown) => {
    const reply = await stdioExchange(clientTransport, {
      jsonrpc: "2.0",
      id,
      method: "tools/call",
      params: { _meta: MODERN_META, name, arguments: args },
    });
    assert.equal("result" in reply, true);
    if (!("result" in reply)) assert.fail("STDIO reply did not contain a result");
    return reply.result;
  };
  const droppedStdioSuccess = await stdioCall(183, "data.query", DATA_QUERY_REQUEST);
  const stdioReceiptId = (
    droppedStdioSuccess.structuredContent as {
      evidence_receipt: { receipt_id: string };
    }
  ).evidence_receipt.receipt_id;
  const stdioRetry = await stdioCall(184, "data.query", DATA_QUERY_REQUEST);
  assert.equal(stdioRetry.isError, true);
  const stdioProblem = stdioRetry.structuredContent as Record<string, unknown>;
  assert.equal(stdioProblem.code, "idempotency_completed");
  assert.equal(
    (stdioRetry.content as { readonly text?: string }[])[0]?.text,
    JSON.stringify(stdioProblem),
  );
  completedProblems.push(stdioProblem);
  const stdioInspection = await stdioCall(185, "evidence.inspect", inspectRequest);
  assert.equal(
    ((stdioInspection.structuredContent as {
      data: { record: { receipt: { receipt_id: string } } };
    }).data.record.receipt.receipt_id),
    stdioReceiptId,
  );
  assert.equal(stdioSlice.ledger.verify().event_count, 1);

  assert.deepEqual(completedProblems[1], completedProblems[0]);
  assert.deepEqual(completedProblems[2], completedProblems[0]);
  assert.equal(providerExecutions, 3);
  for (const problem of completedProblems) {
    const text = JSON.stringify(problem);
    assert.equal(text.includes(DATA_QUERY_IDEMPOTENCY_KEY), false);
    assert.equal(text.includes("evidence-receipt"), false);
    assert.equal(text.includes("observations"), false);
  }
});

test("persists selection and data evidence and inspects both through direct and STDIO", async (t) => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-public-read-transport-ledger-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const ledger = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 365,
    now: () => new Date("2026-08-21T01:00:01.000Z"),
  });
  const selection = selectionApplication(ledger);
  const data = dataApplication(successTransport(), ledger);
  const evidence = evidenceApplication(ledger);
  const direct = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    selectionApplication: selection,
    evidenceApplication: evidence,
    enabledApiOperations: ["selection.resolve", "evidence.inspect"],
    createTraceId: () => TRACE_ID,
  });

  const selectionResponse = await direct(
    directRequest("/selection/resolve", SELECTION_REQUEST),
  );
  assert.equal(selectionResponse.status, 200);
  const selectionResult = await selectionResponse.json() as {
    evidence_receipt: { receipt_id: string };
    evidence_storage?: Record<string, unknown> & { status?: string };
  };
  assert.equal(selectionResult.evidence_storage?.status, "persisted");
  assert.equal(typeof selectionResult.evidence_storage?.record_id, "string");

  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const stdio = startCatalogueStdio({
    application: catalogueApplication(),
    evidenceApplication: evidence,
    selectionApplication: selection,
    dataQueryApplication: data,
    snapshot: SNAPSHOT,
    enabledOperations: ["selection.resolve", "data.query", "evidence.inspect"],
    enabledResources: ["evidence.receipt"],
    createRequestContext: (operation) => context(
      operation as "selection.resolve" | "data.query" | "evidence.inspect",
    ),
    transport: serverTransport,
  });
  t.after(async () => {
    await stdio.close();
    await clientTransport.close();
  });

  const listing = await stdioExchange(clientTransport, {
    jsonrpc: "2.0",
    id: 20,
    method: "tools/list",
    params: { _meta: MODERN_META },
  });
  assert.equal("result" in listing, true);
  if (!("result" in listing)) return;
  const tools = listing.result.tools as {
    readonly name: string;
    readonly annotations?: { readonly idempotentHint?: boolean };
  }[];
  assert.deepEqual(tools.map(({ name }) => name), [
    "evidence.inspect",
    "selection.resolve",
    "data.query",
  ]);
  assert.equal(
    tools.find(({ name }) => name === "data.query")?.annotations?.idempotentHint,
    true,
  );

  const dataReply = await stdioExchange(clientTransport, {
    jsonrpc: "2.0",
    id: 21,
    method: "tools/call",
    params: {
      _meta: MODERN_META,
      name: "data.query",
      arguments: DATA_QUERY_REQUEST,
    },
  });
  assert.equal("result" in dataReply, true);
  if (!("result" in dataReply)) return;
  const dataResult = dataReply.result.structuredContent as {
    evidence_receipt: { receipt_id: string; operation: { name: string } };
    evidence_storage?: Record<string, unknown> & { status?: string };
  };
  assert.equal(dataResult.evidence_receipt.operation.name, "data.query");
  assert.equal(dataResult.evidence_storage?.status, "persisted");
  assert.equal(ledger.verify().event_count, 2);

  for (const [id, operation, receiptId, storage] of [
    [
      22,
      "selection.resolve",
      selectionResult.evidence_receipt.receipt_id,
      selectionResult.evidence_storage,
    ],
    [
      23,
      "data.query",
      dataResult.evidence_receipt.receipt_id,
      dataResult.evidence_storage,
    ],
  ] as const) {
    const directInspectionResponse = await direct(
      directRequest("/evidence/inspect", { receipt_id: receiptId }),
    );
    assert.equal(directInspectionResponse.status, 200);
    const directInspection = await directInspectionResponse.json() as Record<string, unknown>;
    const inspectionReply = await stdioExchange(clientTransport, {
      jsonrpc: "2.0",
      id,
      method: "tools/call",
      params: {
        _meta: MODERN_META,
        name: "evidence.inspect",
        arguments: { receipt_id: receiptId },
      },
    });
    assert.equal("result" in inspectionReply, true);
    if (!("result" in inspectionReply)) return;
    assert.deepEqual(inspectionReply.result.structuredContent, directInspection);
    const uri = MCP_EVIDENCE_RECEIPT_URI_TEMPLATE.replace(
      "{receipt_id}",
      encodeURIComponent(receiptId),
    );
    const resourceReply = await stdioExchange(clientTransport, {
      jsonrpc: "2.0",
      id: id + 100,
      method: "resources/read",
      params: { _meta: MODERN_META, uri },
    });
    assert.equal("result" in resourceReply, true);
    if (!("result" in resourceReply)) return;
    const contents = resourceReply.result.contents as { readonly text?: string }[];
    assert.equal(contents[0]?.text, JSON.stringify(directInspection));
    assert.deepEqual(JSON.parse(contents[0]?.text ?? "null"), directInspection);
    const inspected = directInspection as {
      data?: {
        record?: {
          receipt?: { operation?: { name?: unknown }; receipt_id?: unknown };
        };
        storage?: Record<string, unknown>;
      };
      verification?: { status?: unknown; ledger?: unknown };
    };
    assert.equal(inspected.data?.record?.receipt?.operation?.name, operation);
    assert.equal(inspected.data?.record?.receipt?.receipt_id, receiptId);
    assert.deepEqual(inspected.data?.storage, storage);
    assert.deepEqual(inspected.verification, {
      status: "passed",
      ledger: "restart-verified",
      receipt: "structure-and-content-verified",
      ingest_material: "verified-at-ingest-not-retained",
      attestation: "not-attested",
    });
  }
});

test("preserves caller 408 controls separately from provider timeout 504", async (t) => {
  assert.equal(GATEWAY_HEADER_BODY_TIMEOUT_MS, 5_000);
  assert.equal(ONS_CALL_DEADLINE_MS, 20_000);
  assert.equal(GATEWAY_PROCESSING_SOCKET_TIMEOUT_MS, 25_000);
  assert.ok(ONS_CALL_DEADLINE_MS < GATEWAY_PROCESSING_SOCKET_TIMEOUT_MS);

  let deadlineProviderCalls = 0;
  const deadlineBase = dataApplication(async () => {
    deadlineProviderCalls += 1;
    return fixedResponse();
  });
  const deadlineController = new AbortController();
  let deadlineProblem: Record<string, unknown> | undefined;
  try {
    await deadlineBase.query(DATA_QUERY_REQUEST, context("data.query"), {
      signal: deadlineController.signal,
      deadline: "2020-01-01T00:00:00Z",
    });
    assert.fail("elapsed deadline should fail before provider egress");
  } catch (error) {
    assert.ok(error instanceof DataQueryApplicationError);
    deadlineProblem = error.problem as unknown as Record<string, unknown>;
  }
  assert.ok(deadlineProblem);
  assert.equal(deadlineProblem.code, "query_deadline_exceeded");
  assert.equal(deadlineProviderCalls, 0);

  let timeoutCalls = 0;
  const timeoutTransport: FixedHttpsTransport = async ({ signal }) => {
    timeoutCalls += 1;
    assert.ok(signal instanceof AbortSignal);
    assert.equal(signal.aborted, false);
    throw new FixedHttpsTransportError("response-timeout");
  };
  const timeoutDirectApplication = dataApplication(timeoutTransport);
  const timeoutDirect = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    dataQueryApplication: timeoutDirectApplication,
    evidenceApplication: evidenceForData(timeoutDirectApplication),
    enabledApiOperations: ["data.query", "evidence.inspect"],
    createRequestId: () => REQUEST_ID,
    createTraceId: () => TRACE_ID,
  });
  const timeoutResponse = await timeoutDirect(
    directRequest("/data/query", DATA_QUERY_REQUEST),
  );
  assert.equal(timeoutResponse.status, 504);
  const timeoutProblem = await timeoutResponse.json() as Record<string, unknown>;
  assert.equal(timeoutProblem.code, "provider_timeout");
  assert.equal(timeoutCalls, ONS_EGRESS_POLICY.maxAttempts);

  const timeoutMcpApplication = dataApplication(timeoutTransport);
  const timeoutMcp = createCatalogueMcpHttpHandler({
    application: catalogueApplication(),
    dataQueryApplication: timeoutMcpApplication,
    evidenceApplication: evidenceForData(timeoutMcpApplication),
    snapshot: SNAPSHOT,
    enabledOperations: ["data.query", "evidence.inspect"],
    createRequestContext: () => context("data.query"),
  });
  t.after(() => timeoutMcp.close());
  const timeoutReply = await rawExchange(
    timeoutMcp,
    rawBody(30, "tools/call", {
      name: "data.query",
      arguments: DATA_QUERY_REQUEST,
    }),
    "data.query",
  );
  const timeoutToolResult = toolResult(timeoutReply);
  assert.equal(timeoutToolResult.isError, true);
  assert.deepEqual(timeoutToolResult.structuredContent, timeoutProblem);
  assert.equal(timeoutCalls, ONS_EGRESS_POLICY.maxAttempts * 2);
});

test("maps an aborted direct Request to query_cancelled with no receipt or ledger event", async (t) => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-public-read-direct-cancel-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const ledger = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 365,
    now: () => new Date("2026-08-21T01:00:01.000Z"),
  });
  const started = deferred<AbortSignal>();
  const directData = dataApplication(cancellationTransport(started), ledger);
  const direct = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    dataQueryApplication: directData,
    evidenceApplication: evidenceForData(directData),
    enabledApiOperations: ["data.query", "evidence.inspect"],
    createRequestId: () => REQUEST_ID,
    createTraceId: () => TRACE_ID,
  });
  const controller = new AbortController();
  const pending = direct(
    directRequest("/data/query", DATA_QUERY_REQUEST, controller.signal),
  );
  const adapterSignal = await started.promise;
  assert.equal(adapterSignal.aborted, false);
  controller.abort("caller disconnected");
  const response = await pending;
  assert.equal(adapterSignal.aborted, true);
  assert.equal(response.status, 408);
  assert.equal(
    (await response.json() as { code?: unknown }).code,
    "query_cancelled",
  );
  assert.equal(ledger.verify().event_count, 0);
});

test("propagates modern MCP HTTP cancellation with no receipt or ledger event", async (t) => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-public-read-mcp-cancel-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const ledger = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 365,
    now: () => new Date("2026-08-21T01:00:01.000Z"),
  });
  const started = deferred<AbortSignal>();
  const mcpData = dataApplication(cancellationTransport(started), ledger);
  const mcp = createCatalogueMcpHttpHandler({
    application: catalogueApplication(),
    dataQueryApplication: mcpData,
    evidenceApplication: evidenceForData(mcpData),
    snapshot: SNAPSHOT,
    enabledOperations: ["data.query", "evidence.inspect"],
    createRequestContext: () => context("data.query"),
  });
  t.after(() => mcp.close());
  const body = rawBody(35, "tools/call", {
    name: "data.query",
    arguments: DATA_QUERY_REQUEST,
  });
  const controller = new AbortController();
  const pending = mcp.fetch(rawRequest(body, "data.query", controller.signal));
  const adapterSignal = await started.promise;
  assert.equal(adapterSignal.aborted, false);
  controller.abort("MCP HTTP caller disconnected");
  const response = await pending;
  assert.equal(response.status, 200);
  const message = await response.json() as Record<string, unknown>;
  const called = toolResult(message);
  assert.equal(adapterSignal.aborted, true);
  assert.equal(called.isError, true);
  assert.equal(
    (called.structuredContent as { code?: unknown }).code,
    "query_cancelled",
  );
  assert.equal(
    (called.content as { readonly text?: string }[])[0]?.text,
    JSON.stringify(called.structuredContent),
  );
  assert.equal(ledger.verify().event_count, 0);

  let alreadyAbortedEgress = 0;
  const alreadyAbortedData = dataApplication(async () => {
    alreadyAbortedEgress += 1;
    return fixedResponse();
  });
  const alreadyAborted = createCatalogueMcpHttpHandler({
    application: catalogueApplication(),
    dataQueryApplication: alreadyAbortedData,
    evidenceApplication: evidenceForData(alreadyAbortedData),
    snapshot: SNAPSHOT,
    enabledOperations: ["data.query", "evidence.inspect"],
    createRequestContext: () => context("data.query"),
  });
  t.after(() => alreadyAborted.close());
  const preAbortedController = new AbortController();
  preAbortedController.abort("Already disconnected");
  const preAbortedBody = rawBody(36, "tools/call", {
    name: "data.query",
    arguments: DATA_QUERY_REQUEST,
  });
  const preAbortedResponse = await alreadyAborted.fetch(
    rawRequest(preAbortedBody, "data.query", preAbortedController.signal),
    { parsedBody: preAbortedBody },
  );
  assert.equal(preAbortedResponse.status, 200);
  const preAbortedMessage = await preAbortedResponse.json() as Record<string, unknown>;
  assert.equal(
    (toolResult(preAbortedMessage).structuredContent as { code?: unknown }).code,
    "query_cancelled",
  );
  assert.equal(alreadyAbortedEgress, 0);

  const noClientInfoBody = rawBody(361, "tools/call", {
    _meta: {
      "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
      "io.modelcontextprotocol/clientCapabilities": {},
    },
    name: "data.query",
    arguments: DATA_QUERY_REQUEST,
  });
  const noClientInfoResponse = await alreadyAborted.fetch(
    rawRequest(noClientInfoBody, "data.query", preAbortedController.signal),
    { parsedBody: noClientInfoBody },
  );
  assert.equal(noClientInfoResponse.status, 200);
  const noClientInfoMessage = await noClientInfoResponse.json() as Record<string, unknown>;
  assert.equal(
    (toolResult(noClientInfoMessage).structuredContent as { code?: unknown }).code,
    "query_cancelled",
  );
  assert.equal(alreadyAbortedEgress, 0);

  const missingCapabilitiesBody = rawBody(362, "tools/call", {
    _meta: {
      "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
      "io.modelcontextprotocol/clientInfo": {
        name: "malformed-modern-client",
        version: "1.0.0",
      },
    },
    name: "data.query",
    arguments: DATA_QUERY_REQUEST,
  });
  const missingCapabilitiesResponse = await alreadyAborted.fetch(
    rawRequest(missingCapabilitiesBody, "data.query", preAbortedController.signal),
    { parsedBody: missingCapabilitiesBody },
  );
  assert.equal(missingCapabilitiesResponse.status, 400);
  const missingCapabilitiesMessage =
    await missingCapabilitiesResponse.json() as Record<string, unknown>;
  assert.equal("error" in missingCapabilitiesMessage, true);
  assert.equal("result" in missingCapabilitiesMessage, false);
  assert.equal(alreadyAbortedEgress, 0);

  const selectionOnly = createCatalogueMcpHttpHandler({
    application: catalogueApplication(),
    selectionApplication: selectionApplication(),
    snapshot: SNAPSHOT,
    enabledOperations: ["selection.resolve"],
    createRequestContext: () => context("selection.resolve"),
  });
  t.after(() => selectionOnly.close());
  const selectionBody = rawBody(37, "tools/call", {
    name: "selection.resolve",
    arguments: SELECTION_REQUEST,
  });
  const abortedSelection = await selectionOnly.fetch(
    rawRequest(selectionBody, "selection.resolve", preAbortedController.signal),
    { parsedBody: selectionBody },
  );
  assert.equal(abortedSelection.status, 499);

  const mismatchedData = await alreadyAborted.fetch(
    rawRequest(preAbortedBody, "selection.resolve", preAbortedController.signal),
    { parsedBody: preAbortedBody },
  );
  assert.equal(mismatchedData.status, 400);
  const mismatchedMessage = await mismatchedData.json() as {
    error?: { code?: unknown };
  };
  assert.equal(mismatchedMessage.error?.code, -32_020);
});

test("isolates overlapping MCP HTTP signals and combines SDK-side cancellation", async () => {
  const httpA = new AbortController();
  const httpB = new AbortController();
  const sdkA = new AbortController();
  const sdkB = new AbortController();
  const release = deferred<void>();
  let bindingA: ReturnType<typeof dataQueryRequestSignal> | undefined;
  let bindingB: ReturnType<typeof dataQueryRequestSignal> | undefined;

  await Promise.all([
    withMcpHttpDataQuerySignal(httpA.signal, async () => {
      bindingA = dataQueryRequestSignal(sdkA.signal);
      await release.promise;
    }),
    withMcpHttpDataQuerySignal(httpB.signal, async () => {
      bindingB = dataQueryRequestSignal(sdkB.signal);
      release.resolve(undefined);
    }),
  ]);
  assert.ok(bindingA);
  assert.ok(bindingB);
  assert.notEqual(bindingA.signal, bindingB.signal);
  httpA.abort("HTTP A");
  assert.equal(bindingA.signal.aborted, true);
  assert.equal(bindingB.signal.aborted, false);
  assert.equal(bindingA.signal.reason, "HTTP A");

  sdkB.abort("SDK B");
  assert.equal(bindingB.signal.aborted, true);
  assert.equal(bindingB.signal.reason, "SDK B");
  bindingA.close();
  bindingB.close();

  const rawSdk = new AbortController();
  const stdioBinding = dataQueryRequestSignal(rawSdk.signal);
  assert.equal(stdioBinding.signal, rawSdk.signal);
  rawSdk.abort("STDIO cancellation");
  assert.equal(stdioBinding.signal.aborted, true);
  stdioBinding.close();
});

test("honours STDIO cancellation without a response, receipt or ledger event", async (t) => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-public-read-stdio-cancel-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const ledger = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 365,
    now: () => new Date("2026-08-21T01:00:01.000Z"),
  });
  const started = deferred<AbortSignal>();
  const finished = deferred<void>();
  const application = dataApplication(cancellationTransport(started, finished), ledger);
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const stdio = startCatalogueStdio({
    application: catalogueApplication(),
    dataQueryApplication: application,
    evidenceApplication: evidenceForData(application),
    snapshot: SNAPSHOT,
    enabledOperations: ["data.query", "evidence.inspect"],
    createRequestContext: () => context("data.query"),
    transport: serverTransport,
  });
  t.after(async () => {
    await stdio.close();
    await clientTransport.close();
  });

  let unexpectedResponses = 0;
  clientTransport.onmessage = () => {
    unexpectedResponses += 1;
  };
  await clientTransport.send({
    jsonrpc: "2.0",
    id: 40,
    method: "tools/call",
    params: {
      _meta: MODERN_META,
      name: "data.query",
      arguments: DATA_QUERY_REQUEST,
    },
  });
  const adapterSignal = await started.promise;
  await clientTransport.send({
    jsonrpc: "2.0",
    method: "notifications/cancelled",
    params: {
      _meta: MODERN_META,
      requestId: 40,
      reason: "Caller cancelled the STDIO request",
    },
  });
  await finished.promise;
  await new Promise<void>((resolve) => setImmediate(resolve));
  assert.equal(adapterSignal.aborted, true);
  assert.equal(unexpectedResponses, 0);
  assert.equal(ledger.verify().event_count, 0);

  await clientTransport.send({
    jsonrpc: "2.0",
    method: "notifications/cancelled",
    params: {
      _meta: MODERN_META,
      requestId: 999,
      reason: "Unknown completed request",
    },
  });
  await new Promise<void>((resolve) => setImmediate(resolve));
  assert.equal(unexpectedResponses, 0);
});

test("cancels a real direct listener disconnect before any ledger event", async (t) => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-public-read-listener-cancel-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const ledger = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 365,
    now: () => new Date("2026-08-21T01:00:01.000Z"),
  });
  const started = deferred<AbortSignal>();
  const finished = deferred<void>();
  const application = dataApplication(cancellationTransport(started, finished), ledger);
  const server = createGatewayNodeServer(SNAPSHOT, {
    dataQueryApplication: application,
    evidenceApplication: evidenceForData(application),
    enabledApiOperations: ["data.query", "evidence.inspect"],
    createRequestId: () => REQUEST_ID,
    createTraceId: () => TRACE_ID,
  });
  const port = await listen(server);
  t.after(() => server.closeGateway());
  const body = JSON.stringify(DATA_QUERY_REQUEST);
  const client = nodeRequest({
    hostname: "127.0.0.1",
    port,
    path: "/data/query",
    method: "POST",
    headers: {
      accept: "application/json",
      "content-length": Buffer.byteLength(body),
      "content-type": "application/json",
      host: "127.0.0.1:8787",
      "x-request-id": REQUEST_ID,
    },
  });
  client.on("response", (response) => response.resume());
  client.on("error", () => undefined);
  client.end(body);
  const adapterSignal = await started.promise;
  assert.equal(adapterSignal.aborted, false);
  client.destroy();
  let cancellationTimer: ReturnType<typeof setTimeout> | undefined;
  try {
    await Promise.race([
      finished.promise,
      new Promise<never>((_resolve, reject) => {
        cancellationTimer = setTimeout(
          () => reject(new Error("Listener disconnect did not cancel promptly")),
          2_000,
        );
      }),
    ]);
  } finally {
    if (cancellationTimer !== undefined) clearTimeout(cancellationTimer);
  }
  assert.equal(adapterSignal.aborted, true);
  assert.equal(ledger.verify().event_count, 0);

  const healthStatus = await new Promise<number>((resolve, reject) => {
    const request = nodeRequest(
      {
        hostname: "127.0.0.1",
        port,
        path: "/healthz",
        method: "GET",
        headers: { host: "127.0.0.1:8787" },
      },
      (response) => {
        response.resume();
        response.once("end", () => resolve(response.statusCode ?? 0));
      },
    );
    request.once("error", reject);
    request.end();
  });
  assert.equal(healthStatus, 200);
});

test("cancels a real MCP listener disconnect before any ledger event", async (t) => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-public-read-mcp-listener-cancel-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const ledger = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 365,
    now: () => new Date("2026-08-21T01:00:01.000Z"),
  });
  const started = deferred<AbortSignal>();
  const finished = deferred<void>();
  const reportedErrors: unknown[] = [];
  const application = dataApplication(cancellationTransport(started, finished), ledger);
  const server = createGatewayNodeServer(SNAPSHOT, {
    dataQueryApplication: application,
    evidenceApplication: evidenceForData(application),
    enabledMcpOperations: ["data.query", "evidence.inspect"],
    createMcpRequestContext: () => context("data.query"),
    onerror: (error) => reportedErrors.push(error),
  });
  const port = await listen(server);
  t.after(() => server.closeGateway());
  const requestBody = rawBody(41, "tools/call", {
    name: "data.query",
    arguments: DATA_QUERY_REQUEST,
  });
  const body = JSON.stringify(requestBody);
  const client = nodeRequest({
    hostname: "127.0.0.1",
    port,
    path: "/mcp",
    method: "POST",
    headers: {
      accept: "application/json, text/event-stream",
      "content-length": Buffer.byteLength(body),
      "content-type": "application/json",
      host: `127.0.0.1:${port}`,
      "mcp-method": "tools/call",
      "mcp-name": "data.query",
      "mcp-protocol-version": MCP_PROTOCOL_VERSION,
    },
  });
  client.on("response", (response) => response.resume());
  client.on("error", () => undefined);
  client.end(body);
  const adapterSignal = await started.promise;
  assert.equal(adapterSignal.aborted, false);
  client.destroy();
  let cancellationTimer: ReturnType<typeof setTimeout> | undefined;
  try {
    await Promise.race([
      finished.promise,
      new Promise<never>((_resolve, reject) => {
        cancellationTimer = setTimeout(
          () => reject(new Error("MCP listener disconnect did not cancel promptly")),
          2_000,
        );
      }),
    ]);
  } finally {
    if (cancellationTimer !== undefined) clearTimeout(cancellationTimer);
  }
  assert.equal(adapterSignal.aborted, true);
  assert.equal(ledger.verify().event_count, 0);
  assert.deepEqual(reportedErrors, []);

  const healthStatus = await new Promise<number>((resolve, reject) => {
    const request = nodeRequest(
      {
        hostname: "127.0.0.1",
        port,
        path: "/healthz",
        method: "GET",
        headers: { host: "127.0.0.1:8787" },
      },
      (response) => {
        response.resume();
        response.once("end", () => resolve(response.statusCode ?? 0));
      },
    );
    request.once("error", reject);
    request.end();
  });
  assert.equal(healthStatus, 200);
  assert.deepEqual(reportedErrors, []);
});

test("keeps the legacy conformance factory structurally catalogue-only", (t) => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-public-read-legacy-ledger-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const ledger = openPublicEvidenceLedger({
    rootDirectory: root,
    retentionDays: 365,
    now: () => new Date("2026-08-21T01:00:01.000Z"),
  });
  const base = {
    application: catalogueApplication(),
    snapshot: SNAPSHOT,
  };
  assert.throws(
    () => createCatalogueLegacyConformanceMcpServerFactory(
      {
        ...base,
        selectionApplication: selectionApplication(),
        enabledOperations: ["selection.resolve"],
      },
      MCP_LEGACY_CONFORMANCE_ONLY,
    ),
    /structurally limited to catalogue operations and resources/u,
  );
  assert.throws(
    () => createCatalogueLegacyConformanceMcpServerFactory(
      {
        ...base,
        dataQueryApplication: dataApplication(),
        enabledOperations: ["data.query"],
      },
      MCP_LEGACY_CONFORMANCE_ONLY,
    ),
    /structurally limited to catalogue operations and resources/u,
  );
  const evidenceApplication = createEvidenceInspectApplication(ledger);
  for (const options of [
    { enabledOperations: ["evidence.inspect"] as const, enabledResources: [] },
    { enabledOperations: [] as const, enabledResources: ["evidence.receipt"] as const },
  ]) {
    assert.throws(
      () => createCatalogueLegacyConformanceMcpServerFactory(
        {
          ...base,
          evidenceApplication,
          ...options,
        },
        MCP_LEGACY_CONFORMANCE_ONLY,
      ),
      /structurally limited to catalogue operations and resources/u,
    );
  }
});
