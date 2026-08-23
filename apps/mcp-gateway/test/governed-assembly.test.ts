import assert from "node:assert/strict";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import type { AddressInfo } from "node:net";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import test, { type TestContext } from "node:test";

import {
  InMemoryTransport,
  type JSONRPCMessage,
  type McpHttpHandler,
} from "@modelcontextprotocol/server";

import {
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
  type PublicEvidenceLedger,
  type PublicEvidenceReconciliationIndex,
} from "@gis-ai-go/evidence";
import {
  ONS_EGRESS_POLICY,
  createOnsDataApiAdapter,
  type FixedHttpsResponse,
  type FixedHttpsTransport,
  type OnsDataApiAdapter,
} from "@gis-ai-go/provider-adapter-sdk";
import { V02_TARGET_ACTIVE_TOOL_NAMES } from "@gis-ai-go/tool-registry";

import { catalogueActivation } from "../src/activation.js";
import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";
import {
  DataQueryApplicationError,
  PUBLIC_ONS_DATA_QUERY_PARAMETERS,
} from "../src/data-query-application.js";
import {
  GOVERNED_CANDIDATE_OPERATIONS,
  createGovernedCandidateAssembly,
  governedCandidateAssemblyBindings,
  type GovernedCandidateAssembly,
  type GovernedCandidateAssemblyOptions,
  type GovernedCandidateOperation,
} from "../src/governed-assembly.js";
import {
  createGovernedCandidateHttpHandler,
  createGatewayHttpHandler,
} from "../src/http-app.js";
import {
  createGatewayNodeServer,
  createGovernedCandidateNodeServer,
} from "../src/http-server.js";
import { createGovernedCandidateMcpHttpHandler } from "../src/mcp-http.js";
import {
  MCP_CATALOGUE_RECORD_URI_TEMPLATE,
  MCP_EVIDENCE_RECEIPT_URI_TEMPLATE,
  MCP_PROTOCOL_VERSION,
  MCP_PUBLIC_CATALOGUE_URI,
  createGovernedCandidateMcpServerFactory,
} from "../src/mcp-server.js";
import { startGovernedCandidateStdio } from "../src/mcp-stdio.js";
import type { SelectionResolveRequest } from "../src/selection-application.js";

const SOURCE_CATALOGUE = fileURLToPath(
  new URL("../../../../artifacts/okf/", import.meta.url),
);
const SNAPSHOT = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
  now: new Date("2026-08-23T12:00:00.000Z"),
});
const ACTIVE_LIFECYCLE = Object.freeze({
  discovery: "active",
  invocation: "active",
  reason: "Exact governed candidate assembly test.",
} as const);
const MODERN_META = Object.freeze({
  "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
  "io.modelcontextprotocol/clientCapabilities": Object.freeze({}),
  "io.modelcontextprotocol/clientInfo": Object.freeze({
    name: "gis-ai-go-governed-candidate-test",
    version: "1.0.0",
  }),
});
const OPERATION_PATHS = Object.freeze({
  "catalogue.search": "/catalogue/search",
  "catalogue.describe": "/catalogue/describe",
  "evidence.inspect": "/evidence/inspect",
  "selection.resolve": "/selection/resolve",
  "data.query": "/data/query",
} as const);
const REQUEST_CONTEXTS = Object.freeze({
  "catalogue.search": Object.freeze({
    requestId: "candidate-search-request-001",
    traceId: "1".repeat(32),
  }),
  "catalogue.describe": Object.freeze({
    requestId: "candidate-describe-request-001",
    traceId: "2".repeat(32),
  }),
  "selection.resolve": Object.freeze({
    requestId: "candidate-selection-request-001",
    traceId: "3".repeat(32),
  }),
  "data.query": Object.freeze({
    requestId: "candidate-data-request-001",
    traceId: "4".repeat(32),
  }),
  "evidence.inspect": Object.freeze({
    requestId: "candidate-inspect-request-001",
    traceId: "5".repeat(32),
  }),
});
const DATA_QUERY_REQUEST = Object.freeze({
  schema: "gis-ai-go.data-query-request.v1" as const,
  idempotency_key: `gis-ai-go:ik:v1:${"9".repeat(64)}`,
  parameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
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

interface CandidateFixture {
  readonly assembly: GovernedCandidateAssembly;
  readonly ledger: PublicEvidenceLedger;
  readonly ledgerRoot: string;
  readonly options: GovernedCandidateAssemblyOptions;
  readonly reconciliationIndex: PublicEvidenceReconciliationIndex;
  readonly adapter: OnsDataApiAdapter;
}

function fixedResponse(): FixedHttpsResponse {
  const body = Buffer.from(JSON.stringify(VALID_ONS_PAYLOAD), "utf8");
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

const SUCCESS_TRANSPORT: FixedHttpsTransport = async ({ policy, url, signal }) => {
  assert.equal(policy, ONS_EGRESS_POLICY);
  assert.match(url, /^https:\/\/api\.beta\.ons\.gov\.uk\//u);
  assert.equal(signal instanceof AbortSignal, true);
  return fixedResponse();
};

function fixture(
  t: TestContext,
  lifecycle: {
    readonly discovery: "active" | "suspended";
    readonly invocation: "active" | "suspended";
    readonly reason: string;
  } = ACTIVE_LIFECYCLE,
  suspendedTools?: GovernedCandidateAssemblyOptions["suspendedTools"],
): CandidateFixture {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-governed-candidate-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const ledgerRoot = join(root, "ledger");
  const ledger = openPublicEvidenceLedger({
    rootDirectory: ledgerRoot,
    retentionDays: 365,
    now: () => new Date("2026-08-23T12:00:01.000Z"),
  });
  const reconciliationIndex = openEvidenceReconciliationIndex({
    rootDirectory: join(root, "reconciliation"),
    ledger,
    now: () => new Date("2026-08-23T12:00:02.000Z"),
  });
  const adapter = createOnsDataApiAdapter({
    lifecycle,
    transport: SUCCESS_TRANSPORT,
    now: () => Date.parse("2030-01-01T00:00:00.000Z"),
  });
  const options: GovernedCandidateAssemblyOptions = {
    snapshot: SNAPSHOT,
    evidenceLedger: ledger,
    reconciliationIndex,
    adapter,
    now: () => new Date("2026-08-23T12:00:00.000Z"),
    ...(suspendedTools === undefined ? {} : { suspendedTools }),
  };
  const assembly = createGovernedCandidateAssembly(options);
  return { assembly, ledger, ledgerRoot, options, reconciliationIndex, adapter };
}

function directRequest(
  operation: GovernedCandidateOperation,
  body: unknown,
): Request {
  const context = REQUEST_CONTEXTS[operation];
  return new Request(`http://127.0.0.1:8787${OPERATION_PATHS[operation]}`, {
    method: "POST",
    headers: {
      accept: "application/json",
      "content-type": "application/json",
      host: "127.0.0.1:8787",
      "x-request-id": context.requestId,
    },
    body: JSON.stringify(body),
  });
}

function metadataRequest(path: "/healthz" | "/readyz" | "/openapi.json"): Request {
  return new Request(`http://127.0.0.1:8787${path}`, {
    headers: { host: "127.0.0.1:8787" },
  });
}

function rawMcpBody(
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

function rawMcpRequest(body: Record<string, unknown>, name?: string): Request {
  return new Request("http://127.0.0.1:8787/mcp", {
    method: "POST",
    headers: {
      accept: "application/json, text/event-stream",
      "content-type": "application/json",
      "mcp-method": String(body.method),
      ...(name === undefined ? {} : { "mcp-name": name }),
      "mcp-protocol-version": MCP_PROTOCOL_VERSION,
    },
    body: JSON.stringify(body),
  });
}

async function rawMcpExchange(
  handler: McpHttpHandler,
  body: Record<string, unknown>,
  name?: string,
): Promise<Record<string, unknown>> {
  const response = await handler.fetch(rawMcpRequest(body, name));
  assert.equal(response.status, 200);
  return await response.json() as Record<string, unknown>;
}

function toolResult(message: Record<string, unknown>): Record<string, unknown> {
  assert.equal(typeof message.result, "object");
  assert.notEqual(message.result, null);
  return message.result as Record<string, unknown>;
}

function listedTools(message: Record<string, unknown>): readonly string[] {
  const result = toolResult(message);
  assert.ok(Array.isArray(result.tools));
  return (result.tools as { readonly name: string }[]).map(({ name }) => name);
}

function nextMessage(transport: InMemoryTransport): Promise<JSONRPCMessage> {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(
      () => reject(new Error("Timed out waiting for governed candidate STDIO reply")),
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

async function listen(server: ReturnType<typeof createGovernedCandidateNodeServer>) {
  await new Promise<void>((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolve);
  });
  return (server.address() as AddressInfo).port;
}

function context(operation: GovernedCandidateOperation) {
  const value = REQUEST_CONTEXTS[operation];
  return {
    ...value,
    instance: OPERATION_PATHS[operation],
  };
}

function directOperations(document: Record<string, unknown>): readonly string[] {
  const paths = document.paths as Record<string, unknown>;
  return GOVERNED_CANDIDATE_OPERATIONS.filter((operation) =>
    Object.hasOwn(paths, OPERATION_PATHS[operation])
  );
}

test("assembles one immutable exact-five candidate for direct, MCP HTTP and STDIO", async (t) => {
  const { assembly } = fixture(t);
  assert.equal(Object.isFrozen(assembly), true);
  assert.equal(Object.isFrozen(assembly.operations), true);
  assert.equal(assembly.productionRegistration, false);
  assert.equal(assembly.state, "candidate-unregistered");
  assert.deepEqual(assembly.operations, V02_TARGET_ACTIVE_TOOL_NAMES);
  assert.equal(assembly.operations, assembly.apiOperations);
  assert.equal(assembly.operations, assembly.mcpOperations);
  assert.deepEqual(catalogueActivation.activeTools, []);
  assert.deepEqual(catalogueActivation.activeApiOperations, []);
  assert.equal(assembly.operations.includes("map.render" as never), false);

  const direct = createGovernedCandidateHttpHandler(assembly, {
    createTraceId: () => "a".repeat(32),
    createTraceParentId: () => "b".repeat(16),
  });
  const health = await direct(metadataRequest("/healthz"));
  assert.equal(health.status, 200);
  assert.deepEqual(
    Object.assign({}, await health.json() as Record<string, unknown>, { catalogue: null }),
    {
      status: "ok",
      product: "GIS AI GO",
      lifecycle: "candidate-unregistered",
      production_registration: false,
      catalogue: null,
    },
  );
  const readiness = await direct(metadataRequest("/readyz"));
  assert.equal(readiness.status, 200);
  assert.deepEqual(await readiness.json(), {
    status: "ready",
    reason: "candidate-assembly-verified",
    production_registration: false,
    active_tools: V02_TARGET_ACTIVE_TOOL_NAMES,
    active_api_operations: V02_TARGET_ACTIVE_TOOL_NAMES,
  });
  const openApi = await direct(metadataRequest("/openapi.json"));
  const directDocument = await openApi.json() as Record<string, unknown>;
  assert.deepEqual(directOperations(directDocument), V02_TARGET_ACTIVE_TOOL_NAMES);
  assert.equal(directDocument["x-gis-ai-go-lifecycle"], "candidate-unregistered");
  assert.equal(directDocument["x-gis-ai-go-production-registration"], false);
  assert.deepEqual(
    directDocument["x-gis-ai-go-candidate-operations"],
    V02_TARGET_ACTIVE_TOOL_NAMES,
  );
  const readyPath = (directDocument.paths as Record<string, Record<string, unknown>>)
    ["/readyz"]!;
  const readyResponses = (readyPath.get as Record<string, Record<string, unknown>>)
    .responses!;
  assert.deepEqual(Object.keys(readyResponses).filter((status) => /^[25]/u.test(status)), [
    "200",
    "503",
  ]);

  const mcp = createGovernedCandidateMcpHttpHandler(assembly);
  t.after(() => mcp.close());
  const mcpListing = await rawMcpExchange(mcp, rawMcpBody(1, "tools/list"));
  assert.deepEqual(
    [...listedTools(mcpListing)].sort(),
    [...directOperations(directDocument)].sort(),
  );

  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const stdio = startGovernedCandidateStdio(assembly, { transport: serverTransport });
  t.after(async () => {
    await stdio.close();
    await clientTransport.close();
  });
  const stdioListing = await stdioExchange(clientTransport, {
    jsonrpc: "2.0",
    id: 2,
    method: "tools/list",
    params: { _meta: MODERN_META },
  });
  assert.equal("result" in stdioListing, true);
  if (!("result" in stdioListing)) return;
  assert.deepEqual(
    (stdioListing.result.tools as { readonly name: string }[])
      .map(({ name }) => name)
      .sort(),
    [...directOperations(directDocument)].sort(),
  );

  const defaultDirect = createGatewayHttpHandler({
    snapshot: SNAPSHOT,
    createTraceId: () => "c".repeat(32),
    createTraceParentId: () => "d".repeat(16),
  });
  assert.equal((await defaultDirect(metadataRequest("/readyz"))).status, 503);
});

test("applies provider and tool suspension identically and fails readiness closed", async (t) => {
  for (const [lifecycle, suspendedTools, expected] of [
    [
      { discovery: "active", invocation: "suspended", reason: "Invocation suspended." },
      undefined,
      [
        "catalogue.search",
        "catalogue.describe",
        "selection.resolve",
        "evidence.inspect",
      ],
    ],
    [
      { discovery: "suspended", invocation: "active", reason: "Discovery suspended." },
      undefined,
      ["catalogue.search", "catalogue.describe", "evidence.inspect"],
    ],
    [
      ACTIVE_LIFECYCLE,
      ["evidence.inspect"],
      ["catalogue.search", "catalogue.describe", "selection.resolve"],
    ],
    [
      ACTIVE_LIFECYCLE,
      ["catalogue.describe"],
      ["catalogue.search", "selection.resolve", "data.query", "evidence.inspect"],
    ],
    [
      ACTIVE_LIFECYCLE,
      ["catalogue.search"],
      ["catalogue.describe", "selection.resolve", "data.query", "evidence.inspect"],
    ],
  ] as const) {
    const expectedOperations: readonly GovernedCandidateOperation[] = expected;
    const { assembly } = fixture(t, lifecycle, suspendedTools);
    assert.deepEqual(assembly.operations, expected);
    assert.equal(assembly.productionRegistration, false);
    const direct = createGovernedCandidateHttpHandler(assembly, {
      createTraceId: () => "6".repeat(32),
      createTraceParentId: () => "7".repeat(16),
    });
    const readiness = await direct(metadataRequest("/readyz"));
    assert.equal(readiness.status, 503);
    assert.deepEqual(await readiness.json(), {
      status: "blocked",
      reason: "relevant-capability-suspended",
      production_registration: false,
      active_tools: expected,
      active_api_operations: expected,
    });
    const openApi = await direct(metadataRequest("/openapi.json"));
    const directDocument = await openApi.json() as Record<string, unknown>;
    const mcp = createGovernedCandidateMcpHttpHandler(assembly);
    const mcpListing = await rawMcpExchange(mcp, rawMcpBody(3, "tools/list"));
    assert.deepEqual(directOperations(directDocument), expected);
    assert.deepEqual(
      [...listedTools(mcpListing)].sort(),
      [...expected].sort(),
    );
    const publicCatalogueExpected =
      expectedOperations.includes("catalogue.search") &&
      expectedOperations.includes("catalogue.describe");
    const expectedResources = [
      ...(publicCatalogueExpected ? ["catalogue.public"] : []),
      ...(expectedOperations.includes("catalogue.describe") ? ["catalogue.record"] : []),
      ...(expectedOperations.includes("evidence.inspect") ? ["evidence.receipt"] : []),
    ];
    assert.deepEqual(assembly.mcpResources, expectedResources);
    const resourceListing = toolResult(await rawMcpExchange(
      mcp,
      rawMcpBody(4, "resources/list"),
    ));
    assert.deepEqual(
      (resourceListing.resources as { readonly uri: string }[]).map(({ uri }) => uri),
      publicCatalogueExpected ? [MCP_PUBLIC_CATALOGUE_URI] : [],
    );
    const templateListing = toolResult(await rawMcpExchange(
      mcp,
      rawMcpBody(5, "resources/templates/list"),
    ));
    assert.deepEqual(
      (templateListing.resourceTemplates as { readonly uriTemplate: string }[])
        .map(({ uriTemplate }) => uriTemplate),
      [
        ...(expectedOperations.includes("catalogue.describe")
          ? [MCP_CATALOGUE_RECORD_URI_TEMPLATE]
          : []),
        ...(expectedOperations.includes("evidence.inspect")
          ? [MCP_EVIDENCE_RECEIPT_URI_TEMPLATE]
          : []),
      ],
    );
    const publicRead = await mcp.fetch(rawMcpRequest(
      rawMcpBody(6, "resources/read", { uri: MCP_PUBLIC_CATALOGUE_URI }),
      MCP_PUBLIC_CATALOGUE_URI,
    ));
    const publicExpected = publicCatalogueExpected;
    assert.equal(publicRead.status, 200);
    assert.equal(
      Object.hasOwn(await publicRead.json() as Record<string, unknown>, "result"),
      publicExpected,
    );
    const recordUri = "gis-ai-go://catalogue/records/LR-Q003";
    const recordRead = await mcp.fetch(rawMcpRequest(
      rawMcpBody(7, "resources/read", { uri: recordUri }),
      recordUri,
    ));
    const recordExpected = expectedOperations.includes("catalogue.describe");
    assert.equal(recordRead.status, 200);
    assert.equal(
      Object.hasOwn(await recordRead.json() as Record<string, unknown>, "result"),
      recordExpected,
    );
    await mcp.close();

    if (lifecycle.discovery === "active" && lifecycle.invocation === "suspended") {
      const directCallFixture = fixture(t, lifecycle);
      const directCall = createGovernedCandidateHttpHandler(
        directCallFixture.assembly,
        {
          createTraceId: () => "8".repeat(32),
          createTraceParentId: () => "9".repeat(16),
        },
      );
      const directSearch = await directCall(directRequest("catalogue.search", {
        query: "INSPIRE",
        limit: 1,
      }));
      assert.equal(directSearch.status, 200);
      const directResult = await directSearch.json() as Record<string, unknown>;
      const directReceipt = directResult.evidence_receipt as Record<string, unknown>;
      assert.equal(
        (directReceipt.policy_decision as Record<string, unknown>).effect,
        "allow-with-obligations",
      );
      assert.equal(
        (await directCall(directRequest("data.query", DATA_QUERY_REQUEST))).status,
        400,
      );

      const mcpCallFixture = fixture(t, lifecycle);
      const mcpCall = createGovernedCandidateMcpHttpHandler(
        mcpCallFixture.assembly,
        {
          createRequestContext: (operation) => ({
            ...context(operation as GovernedCandidateOperation),
            traceId: "8".repeat(32),
          }),
        },
      );
      const mcpSearch = toolResult(await rawMcpExchange(
        mcpCall,
        rawMcpBody(30, "tools/call", {
          name: "catalogue.search",
          arguments: { query: "INSPIRE", limit: 1 },
        }),
        "catalogue.search",
      ));
      const mcpResult = mcpSearch.structuredContent as Record<string, unknown>;
      assert.equal(mcpSearch.isError, undefined);
      assert.deepEqual(mcpResult, directResult);
      assert.equal(
        (mcpSearch.content as { readonly text?: string }[])[0]?.text,
        JSON.stringify(mcpResult),
      );
      assert.equal(
        ((mcpResult.evidence_receipt as Record<string, unknown>)
          .policy_decision as Record<string, unknown>).effect,
        "allow-with-obligations",
      );
      assert.equal(
        Object.hasOwn(
          await rawMcpExchange(
            mcpCall,
            rawMcpBody(31, "tools/call", {
              name: "data.query",
              arguments: DATA_QUERY_REQUEST,
            }),
            "data.query",
          ),
          "error",
        ),
        true,
      );
      await mcpCall.close();
    }
  }

  const allSuspended = fixture(
    t,
    ACTIVE_LIFECYCLE,
    GOVERNED_CANDIDATE_OPERATIONS,
  ).assembly;
  assert.deepEqual(allSuspended.operations, []);
  assert.deepEqual(allSuspended.mcpResources, []);
  const allSuspendedDirect = createGovernedCandidateHttpHandler(allSuspended, {
    createTraceId: () => "a".repeat(32),
    createTraceParentId: () => "b".repeat(16),
  });
  assert.equal((await allSuspendedDirect(metadataRequest("/readyz"))).status, 503);
  const allSuspendedOpenApi = await allSuspendedDirect(metadataRequest("/openapi.json"));
  const allSuspendedDocument = await allSuspendedOpenApi.json() as
    Record<string, unknown>;
  assert.deepEqual(directOperations(allSuspendedDocument), []);
  const schemas = ((allSuspendedDocument.components as Record<string, unknown>)
    .schemas as Record<string, unknown>);
  const readinessSchema = schemas.Readiness as Record<string, unknown>;
  const properties = readinessSchema.properties as Record<string, unknown>;
  assert.equal(
    (properties.active_tools as Record<string, unknown>).items,
    false,
  );
  assert.equal(
    (properties.active_api_operations as Record<string, unknown>).items,
    false,
  );
  assert.equal(JSON.stringify(readinessSchema).includes('"enum":[]'), false);
});

test("snapshots suspension inputs without invoking hostile traps or accessors", (t) => {
  const supplied: GovernedCandidateOperation[] = ["catalogue.search"];
  const snapshot = fixture(t, ACTIVE_LIFECYCLE, supplied).assembly;
  supplied[0] = "catalogue.describe";
  supplied.push("selection.resolve");
  assert.deepEqual(snapshot.operations, [
    "catalogue.describe",
    "selection.resolve",
    "data.query",
    "evidence.inspect",
  ]);

  assert.throws(
    () => fixture(t, ACTIVE_LIFECYCLE, ["map.render"] as never),
    /unique candidate-operation subset/u,
  );
  assert.throws(
    () => fixture(t, ACTIVE_LIFECYCLE, ["catalogue.search", "catalogue.search"]),
    /unique candidate-operation subset/u,
  );

  let proxyTrapCalls = 0;
  const proxy = new Proxy([] as GovernedCandidateOperation[], {
    get() {
      proxyTrapCalls += 1;
      throw new Error("proxy get trap must not run");
    },
    getOwnPropertyDescriptor() {
      proxyTrapCalls += 1;
      throw new Error("proxy descriptor trap must not run");
    },
    ownKeys() {
      proxyTrapCalls += 1;
      throw new Error("proxy ownKeys trap must not run");
    },
  });
  assert.throws(
    () => fixture(t, ACTIVE_LIFECYCLE, proxy),
    /unique candidate-operation subset/u,
  );
  assert.equal(proxyTrapCalls, 0);

  let accessorCalls = 0;
  const accessor = new Array<GovernedCandidateOperation>(1);
  Object.defineProperty(accessor, "0", {
    enumerable: true,
    get: () => {
      accessorCalls += 1;
      return "catalogue.search";
    },
  });
  assert.throws(
    () => fixture(t, ACTIVE_LIFECYCLE, accessor),
    /unique candidate-operation subset/u,
  );
  assert.equal(accessorCalls, 0);
});

test("rejects hostile or forged assembly authority and independent activation", (t) => {
  const { assembly, options } = fixture(t);
  let proxyTrapCalls = 0;
  const proxyOptions = new Proxy(options, {
    get() {
      proxyTrapCalls += 1;
      throw new Error("options get trap must not run");
    },
    getPrototypeOf() {
      proxyTrapCalls += 1;
      throw new Error("options prototype trap must not run");
    },
    ownKeys() {
      proxyTrapCalls += 1;
      throw new Error("options ownKeys trap must not run");
    },
  });
  assert.throws(
    () => createGovernedCandidateAssembly(proxyOptions),
    /plain object/u,
  );
  assert.equal(proxyTrapCalls, 0);

  let accessorCalls = 0;
  const accessorOptions = { ...options } as Record<string, unknown>;
  Object.defineProperty(accessorOptions, "snapshot", {
    enumerable: true,
    get: () => {
      accessorCalls += 1;
      return SNAPSHOT;
    },
  });
  assert.throws(
    () => createGovernedCandidateAssembly(accessorOptions as never),
    /data properties/u,
  );
  assert.equal(accessorCalls, 0);
  assert.throws(
    () => createGovernedCandidateAssembly({ ...options, unexpected: true } as never),
    /unexpected shape/u,
  );
  const symbolOptions = { ...options } as Record<PropertyKey, unknown>;
  symbolOptions[Symbol("activation")] = true;
  assert.throws(
    () => createGovernedCandidateAssembly(symbolOptions as never),
    /unexpected shape/u,
  );
  const hiddenOptions = { ...options };
  Object.defineProperty(hiddenOptions, "adapter", {
    enumerable: false,
    value: options.adapter,
  });
  assert.throws(
    () => createGovernedCandidateAssembly(hiddenOptions as never),
    /data properties/u,
  );

  const forged = { ...assembly } as GovernedCandidateAssembly;
  assert.throws(
    () => governedCandidateAssemblyBindings(forged),
    /assembly is invalid/u,
  );
  let assemblyProxyTrapCalls = 0;
  const proxyAssembly = new Proxy(assembly, {
    get() {
      assemblyProxyTrapCalls += 1;
      throw new Error("assembly get trap must not run");
    },
  });
  assert.throws(
    () => governedCandidateAssemblyBindings(proxyAssembly),
    /assembly is invalid/u,
  );
  assert.equal(assemblyProxyTrapCalls, 0);
  assert.throws(
    () => createGatewayHttpHandler({
      snapshot: SNAPSHOT,
      governedCandidateAssembly: assembly,
      enabledApiOperations: [],
    }),
    /independent applications or activation/u,
  );
  assert.throws(
    () => createGatewayNodeServer(SNAPSHOT, {
      governedCandidateAssembly: assembly,
      enabledMcpOperations: [],
    }),
    /independent applications or activation/u,
  );

  assert.throws(
    () => createGovernedCandidateAssembly({
      ...options,
      snapshot: { ...SNAPSHOT },
    }),
    /not an exact verified snapshot/u,
  );
  let snapshotProxyCalls = 0;
  const snapshotProxy = new Proxy(SNAPSHOT, {
    get() {
      snapshotProxyCalls += 1;
      throw new Error("snapshot proxy trap must not run");
    },
  });
  assert.throws(
    () => createGovernedCandidateAssembly({ ...options, snapshot: snapshotProxy }),
    /not an exact verified snapshot/u,
  );
  assert.equal(snapshotProxyCalls, 0);
  const revoked = Proxy.revocable(SNAPSHOT, {});
  revoked.revoke();
  assert.throws(
    () => createGovernedCandidateAssembly({ ...options, snapshot: revoked.proxy }),
    /not an exact verified snapshot/u,
  );
  assert.equal(Reflect.set(SNAPSHOT, "revision", "0".repeat(40)), false);
  const recordsPrototype = Object.getPrototypeOf(SNAPSHOT.recordsById) as object;
  assert.equal(Object.isFrozen(recordsPrototype), true);
  let substitutedRecordCalls = 0;
  assert.equal(
    Reflect.defineProperty(recordsPrototype, "get", {
      value: () => {
        substitutedRecordCalls += 1;
        return undefined;
      },
    }),
    false,
  );
  assert.equal(substitutedRecordCalls, 0);
});

test("rejects every hostile governed wrapper option bag without invoking it", async (t) => {
  const { assembly } = fixture(t);
  let trapCalls = 0;
  const proxy = new Proxy({}, {
    get() {
      trapCalls += 1;
      throw new Error("wrapper get trap must not run");
    },
    getPrototypeOf() {
      trapCalls += 1;
      throw new Error("wrapper prototype trap must not run");
    },
    ownKeys() {
      trapCalls += 1;
      throw new Error("wrapper ownKeys trap must not run");
    },
  });
  const wrappers = [
    () => createGovernedCandidateHttpHandler(assembly, proxy as never),
    () => createGovernedCandidateMcpServerFactory(assembly, proxy as never),
    () => createGovernedCandidateMcpHttpHandler(assembly, proxy as never),
    () => startGovernedCandidateStdio(assembly, proxy as never),
    () => createGovernedCandidateNodeServer(assembly, proxy as never),
  ];
  for (const create of wrappers) {
    assert.throws(create, /must be a plain object/u);
  }
  assert.equal(trapCalls, 0);

  let accessorCalls = 0;
  const accessor = Object.create(Object.prototype) as Record<string, unknown>;
  Object.defineProperty(accessor, "onerror", {
    enumerable: true,
    get: () => {
      accessorCalls += 1;
      return undefined;
    },
  });
  for (const create of [
    () => createGovernedCandidateHttpHandler(assembly, accessor as never),
    () => createGovernedCandidateMcpServerFactory(assembly, accessor as never),
    () => createGovernedCandidateMcpHttpHandler(assembly, accessor as never),
    () => startGovernedCandidateStdio(assembly, accessor as never),
    () => createGovernedCandidateNodeServer(assembly, accessor as never),
  ]) {
    assert.throws(create, /enumerable data properties/u);
  }
  assert.equal(accessorCalls, 0);

  let nestedTrapCalls = 0;
  const nestedProxy = new Proxy(["127.0.0.1"], {
    get() {
      nestedTrapCalls += 1;
      throw new Error("nested allowlist get trap must not run");
    },
    getOwnPropertyDescriptor() {
      nestedTrapCalls += 1;
      throw new Error("nested allowlist descriptor trap must not run");
    },
    ownKeys() {
      nestedTrapCalls += 1;
      throw new Error("nested allowlist ownKeys trap must not run");
    },
  });
  for (const create of [
    () => createGovernedCandidateHttpHandler(assembly, {
      allowedHosts: nestedProxy,
    }),
    () => createGovernedCandidateNodeServer(assembly, {
      directAllowedHosts: nestedProxy,
    }),
    () => createGovernedCandidateNodeServer(assembly, {
      directAllowedOrigins: nestedProxy,
    }),
    () => createGovernedCandidateNodeServer(assembly, {
      mcpAllowedHostnames: nestedProxy,
    }),
    () => createGovernedCandidateNodeServer(assembly, {
      mcpAllowedOrigins: nestedProxy,
    }),
  ]) {
    assert.throws(create, /dense string array/u);
  }
  assert.equal(nestedTrapCalls, 0);

  let nestedAccessorCalls = 0;
  const nestedAccessor = ["127.0.0.1"];
  Object.defineProperty(nestedAccessor, "0", {
    configurable: true,
    enumerable: true,
    get: () => {
      nestedAccessorCalls += 1;
      return "127.0.0.1";
    },
  });
  for (const create of [
    () => createGovernedCandidateHttpHandler(assembly, {
      allowedOrigins: nestedAccessor,
    }),
    () => createGovernedCandidateNodeServer(assembly, {
      directAllowedHosts: nestedAccessor,
    }),
    () => createGovernedCandidateNodeServer(assembly, {
      directAllowedOrigins: nestedAccessor,
    }),
    () => createGovernedCandidateNodeServer(assembly, {
      mcpAllowedHostnames: nestedAccessor,
    }),
    () => createGovernedCandidateNodeServer(assembly, {
      mcpAllowedOrigins: nestedAccessor,
    }),
  ]) {
    assert.throws(create, /dense string array/u);
  }
  assert.equal(nestedAccessorCalls, 0);

  const mutableHosts = ["candidate.local"];
  const snapshotted = createGovernedCandidateHttpHandler(assembly, {
    allowedHosts: mutableHosts,
    createTraceId: () => "d".repeat(32),
    createTraceParentId: () => "e".repeat(16),
  });
  mutableHosts[0] = "substituted.local";
  const snapshottedHealth = await snapshotted(new Request(
    "http://candidate.local/healthz",
    { headers: { host: "candidate.local" } },
  ));
  assert.equal(snapshottedHealth.status, 200);
});

test("keeps corrupt evidence readiness blocked without implying registration", async (t) => {
  const { assembly, ledgerRoot } = fixture(t);
  const reported: Error[] = [];
  const direct = createGovernedCandidateHttpHandler(assembly, {
    createTraceId: () => "8".repeat(32),
    createTraceParentId: () => "9".repeat(16),
    onerror: (error) => reported.push(error),
  });
  writeFileSync(join(ledgerRoot, "ledger.json"), "{}\n", { mode: 0o600 });
  const readiness = await direct(metadataRequest("/readyz"));
  assert.equal(readiness.status, 503);
  assert.deepEqual(await readiness.json(), {
    status: "blocked",
    reason: "evidence-integrity-failed",
    production_registration: false,
    active_tools: V02_TARGET_ACTIVE_TOOL_NAMES,
    active_api_operations: V02_TARGET_ACTIVE_TOOL_NAMES,
  });
  assert.equal(reported.length, 1);
  assert.equal(
    reported[0]?.message,
    "Configured evidence storage failed readiness verification",
  );
});

test("rechecks provider integrity before reporting candidate readiness", async (t) => {
  const { assembly, adapter } = fixture(t);
  const direct = createGovernedCandidateHttpHandler(assembly, {
    createTraceId: () => "b".repeat(32),
    createTraceParentId: () => "c".repeat(16),
  });
  assert.equal(Reflect.set(adapter, "operations", []), true);
  const readiness = await direct(metadataRequest("/readyz"));
  assert.equal(readiness.status, 503);
  assert.deepEqual(await readiness.json(), {
    status: "blocked",
    reason: "relevant-capability-suspended",
    production_registration: false,
    active_tools: V02_TARGET_ACTIVE_TOOL_NAMES,
    active_api_operations: V02_TARGET_ACTIVE_TOOL_NAMES,
  });
});

test("locks every evidence dispatch surface against mid-call substitution", async (t) => {
  const { assembly, ledger, reconciliationIndex } = fixture(t);
  let substitutedCalls = 0;
  for (const [target, method] of [
    [ledger, "verify"],
    [ledger, "persistReceipt"],
    [ledger, "inspect"],
    [ledger, "inspectReceipts"],
    [reconciliationIndex, "verify"],
    [reconciliationIndex, "lookup"],
    [reconciliationIndex, "claim"],
    [reconciliationIndex, "resolve"],
  ] as const) {
    assert.equal(
      Reflect.defineProperty(target, method, {
        value: () => {
          substitutedCalls += 1;
          return undefined;
        },
      }),
      false,
    );
  }
  assert.equal(Object.isFrozen(ledger), true);
  assert.equal(Object.isFrozen(reconciliationIndex), true);
  assert.equal(Object.isFrozen(Object.getPrototypeOf(ledger)), true);
  assert.equal(Object.isFrozen(Object.getPrototypeOf(reconciliationIndex)), true);

  const direct = createGovernedCandidateHttpHandler(assembly, {
    createTraceId: () => "d".repeat(32),
    createTraceParentId: () => "e".repeat(16),
  });
  const response = await direct(directRequest("catalogue.search", {
    query: "INSPIRE",
    limit: 1,
  }));
  assert.equal(response.status, 200);
  assert.equal(substitutedCalls, 0);
});

test("uses the pristine provider execution seam on calls without a readiness probe", async (t) => {
  const { assembly, adapter } = fixture(t);
  const direct = createGovernedCandidateHttpHandler(assembly, {
    createRequestId: () => REQUEST_CONTEXTS["data.query"].requestId,
    createTraceId: () => REQUEST_CONTEXTS["data.query"].traceId,
    createTraceParentId: () => "f".repeat(16),
  });
  const mcp = createGovernedCandidateMcpHttpHandler(assembly, {
    createRequestContext: (operation) => context(operation as GovernedCandidateOperation),
  });
  t.after(() => mcp.close());
  let substitutedExecutions = 0;
  Object.defineProperty(adapter, "execute", {
    configurable: true,
    value: async () => {
      substitutedExecutions += 1;
      return {};
    },
  });

  await assert.rejects(
    governedCandidateAssemblyBindings(assembly).dataQueryApplication.query(
      DATA_QUERY_REQUEST,
      context("data.query"),
    ),
    (error: unknown) =>
      error instanceof DataQueryApplicationError &&
      error.problem.code === "provider_contract_failed",
  );
  const directResponse = await direct(directRequest("data.query", DATA_QUERY_REQUEST));
  assert.equal(directResponse.status, 503);
  const mcpMessage = await rawMcpExchange(
    mcp,
    rawMcpBody(30, "tools/call", {
      name: "data.query",
      arguments: DATA_QUERY_REQUEST,
    }),
    "data.query",
  );
  const mcpResult = toolResult(mcpMessage);
  assert.equal(mcpResult.isError, true);
  assert.equal(
    (mcpResult.structuredContent as { code?: unknown }).code,
    "internal_error",
  );
  assert.equal(substitutedExecutions, 0);
});

test("keeps the Node candidate MCP face behind the same readiness guard", async (t) => {
  const { assembly, adapter } = fixture(t);
  const server = createGovernedCandidateNodeServer(assembly, {
    createMcpRequestContext: (operation) =>
      context(operation as GovernedCandidateOperation),
  });
  t.after(() => server.closeGateway());
  const port = await listen(server);
  let substitutedExecutions = 0;
  Object.defineProperty(adapter, "execute", {
    configurable: true,
    value: async () => {
      substitutedExecutions += 1;
      return {};
    },
  });
  const body = rawMcpBody(31, "tools/call", {
    name: "data.query",
    arguments: DATA_QUERY_REQUEST,
  });
  const response = await fetch(`http://127.0.0.1:${port}/mcp`, {
    method: "POST",
    headers: {
      accept: "application/json, text/event-stream",
      "content-type": "application/json",
      "mcp-method": "tools/call",
      "mcp-name": "data.query",
      "mcp-protocol-version": MCP_PROTOCOL_VERSION,
    },
    body: JSON.stringify(body),
  });
  assert.equal(response.status, 200);
  const message = await response.json() as Record<string, unknown>;
  assert.equal(toolResult(message).isError, true);
  assert.equal(substitutedExecutions, 0);
});

test("keeps exact-five success, receipt and plain-text semantics across transports", async (t) => {
  const directFixture = fixture(t);
  const mcpFixture = fixture(t);
  const directTraceIds = [...Object.values(REQUEST_CONTEXTS)].map(({ traceId }) => traceId);
  const direct = createGovernedCandidateHttpHandler(directFixture.assembly, {
    createRequestId: () => REQUEST_CONTEXTS["data.query"].requestId,
    createTraceId: () => {
      const value = directTraceIds.shift();
      assert.ok(value);
      return value;
    },
    createTraceParentId: () => "a".repeat(16),
  });
  const mcp = createGovernedCandidateMcpHttpHandler(mcpFixture.assembly, {
    createRequestContext: (operation) => context(operation as GovernedCandidateOperation),
  });
  t.after(() => mcp.close());

  const directResults = new Map<GovernedCandidateOperation, Record<string, unknown>>();
  const mcpResults = new Map<GovernedCandidateOperation, Record<string, unknown>>();
  const requests: readonly [GovernedCandidateOperation, unknown][] = [
    ["catalogue.search", { query: "INSPIRE", limit: 1 }],
    ["catalogue.describe", { record_id: "LR-Q003" }],
    ["selection.resolve", SELECTION_REQUEST],
    ["data.query", DATA_QUERY_REQUEST],
  ];
  for (const [index, [operation, argumentsValue]] of requests.entries()) {
    const directResponse = await direct(directRequest(operation, argumentsValue));
    assert.equal(directResponse.status, 200);
    const directResult = await directResponse.json() as Record<string, unknown>;
    directResults.set(operation, directResult);

    const mcpMessage = await rawMcpExchange(
      mcp,
      rawMcpBody(index + 10, "tools/call", {
        name: operation,
        arguments: argumentsValue,
      }),
      operation,
    );
    const called = toolResult(mcpMessage);
    assert.deepEqual(called.structuredContent, directResult);
    assert.equal(
      (called.content as { readonly text?: string }[])[0]?.text,
      JSON.stringify(directResult),
    );
    assert.equal(called.isError, undefined);
    mcpResults.set(operation, called.structuredContent as Record<string, unknown>);

    const receipt = directResult.evidence_receipt as Record<string, unknown>;
    const decision = receipt.policy_decision as Record<string, unknown>;
    assert.equal(directResult.request_id, REQUEST_CONTEXTS[operation].requestId);
    assert.equal(directResult.trace_id, REQUEST_CONTEXTS[operation].traceId);
    assert.equal(decision.request_id, directResult.request_id);
    assert.equal(decision.trace_id, directResult.trace_id);
    assert.match(String(decision.effect), /^allow/u);
  }

  const directSearchReceipt = directResults.get("catalogue.search")!
    .evidence_receipt as Record<string, unknown>;
  const mcpSearchReceipt = mcpResults.get("catalogue.search")!
    .evidence_receipt as Record<string, unknown>;
  assert.equal(directSearchReceipt.receipt_id, mcpSearchReceipt.receipt_id);
  const beforeDirectInspect = directFixture.ledger.verify().event_count;
  const beforeMcpInspect = mcpFixture.ledger.verify().event_count;
  const directInspectResponse = await direct(directRequest("evidence.inspect", {
    receipt_id: directSearchReceipt.receipt_id,
  }));
  assert.equal(directInspectResponse.status, 200);
  const directInspection = await directInspectResponse.json() as Record<string, unknown>;
  const mcpInspectMessage = await rawMcpExchange(
    mcp,
    rawMcpBody(20, "tools/call", {
      name: "evidence.inspect",
      arguments: { receipt_id: mcpSearchReceipt.receipt_id },
    }),
    "evidence.inspect",
  );
  const mcpInspectionResult = toolResult(mcpInspectMessage);
  assert.deepEqual(mcpInspectionResult.structuredContent, directInspection);
  assert.equal(
    (mcpInspectionResult.content as { readonly text?: string }[])[0]?.text,
    JSON.stringify(directInspection),
  );
  assert.equal(directInspection.request_id, REQUEST_CONTEXTS["evidence.inspect"].requestId);
  assert.equal(directInspection.trace_id, REQUEST_CONTEXTS["evidence.inspect"].traceId);
  assert.equal(directInspection.schema, "gis-ai-go.evidence-inspect-result.v3");
  const inspectionReceipt = directInspection.evidence_receipt as Record<string, unknown>;
  const inspectionDecision = inspectionReceipt.policy_decision as Record<string, unknown>;
  assert.equal(inspectionReceipt.schema, "gis-ai-go.evidence-receipt.v3");
  assert.equal(inspectionReceipt.request_id, directInspection.request_id);
  assert.equal(inspectionReceipt.trace_id, directInspection.trace_id);
  assert.equal(inspectionDecision.request_id, directInspection.request_id);
  assert.equal(inspectionDecision.trace_id, directInspection.trace_id);
  const inspectedData = directInspection.data as Record<string, unknown>;
  const inspectedRecord = inspectedData.record as Record<string, unknown>;
  const inspectedReceipt = inspectedRecord.receipt as Record<string, unknown>;
  const inspectedDecision = inspectedReceipt.policy_decision as Record<string, unknown>;
  assert.equal(inspectedReceipt.receipt_id, directSearchReceipt.receipt_id);
  assert.equal(inspectedDecision.request_id, REQUEST_CONTEXTS["catalogue.search"].requestId);
  assert.equal(inspectedDecision.trace_id, REQUEST_CONTEXTS["catalogue.search"].traceId);
  assert.notEqual(inspectedDecision.trace_id, directInspection.trace_id);
  assert.equal(directFixture.ledger.verify().event_count, beforeDirectInspect);
  assert.equal(mcpFixture.ledger.verify().event_count, beforeMcpInspect);

  const stdioFixture = fixture(t);
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const stdio = startGovernedCandidateStdio(stdioFixture.assembly, {
    createRequestContext: (operation) => context(operation as GovernedCandidateOperation),
    transport: serverTransport,
  });
  t.after(async () => {
    await stdio.close();
    await clientTransport.close();
  });
  const stdioSearch = await stdioExchange(clientTransport, {
    jsonrpc: "2.0",
    id: 21,
    method: "tools/call",
    params: {
      _meta: MODERN_META,
      name: "catalogue.search",
      arguments: { query: "INSPIRE", limit: 1 },
    },
  });
  assert.equal("result" in stdioSearch, true);
  if (!("result" in stdioSearch)) return;
  assert.deepEqual(
    stdioSearch.result.structuredContent,
    directResults.get("catalogue.search"),
  );
  assert.equal(
    (stdioSearch.result.content as { readonly text?: string }[])[0]?.text,
    JSON.stringify(directResults.get("catalogue.search")),
  );
});

test("keeps v2 inspection identity separate from the recovered data receipt", async (t) => {
  const directFixture = fixture(t);
  const mcpFixture = fixture(t);
  const traces = [
    REQUEST_CONTEXTS["data.query"].traceId,
    REQUEST_CONTEXTS["evidence.inspect"].traceId,
  ];
  const direct = createGovernedCandidateHttpHandler(directFixture.assembly, {
    createRequestId: () => REQUEST_CONTEXTS["data.query"].requestId,
    createTraceId: () => traces.shift()!,
    createTraceParentId: () => "a".repeat(16),
  });
  const mcp = createGovernedCandidateMcpHttpHandler(mcpFixture.assembly, {
    createRequestContext: (operation) => context(operation as GovernedCandidateOperation),
  });
  t.after(() => mcp.close());

  const directData = await direct(directRequest("data.query", DATA_QUERY_REQUEST));
  assert.equal(directData.status, 200);
  const directDataResult = await directData.json() as Record<string, unknown>;
  const mcpData = toolResult(await rawMcpExchange(
    mcp,
    rawMcpBody(40, "tools/call", {
      name: "data.query",
      arguments: DATA_QUERY_REQUEST,
    }),
    "data.query",
  ));
  assert.deepEqual(mcpData.structuredContent, directDataResult);

  const inspectRequest = {
    schema: "gis-ai-go.evidence-inspect-request.v2",
    source_operation: "data.query",
    idempotency_key: DATA_QUERY_REQUEST.idempotency_key,
  } as const;
  const directCount = directFixture.ledger.verify().event_count;
  const mcpCount = mcpFixture.ledger.verify().event_count;
  const directInspect = await direct(directRequest("evidence.inspect", inspectRequest));
  assert.equal(directInspect.status, 200);
  const directInspection = await directInspect.json() as Record<string, unknown>;
  const mcpInspect = toolResult(await rawMcpExchange(
    mcp,
    rawMcpBody(41, "tools/call", {
      name: "evidence.inspect",
      arguments: inspectRequest,
    }),
    "evidence.inspect",
  ));
  assert.deepEqual(mcpInspect.structuredContent, directInspection);
  assert.equal(
    (mcpInspect.content as { readonly text?: string }[])[0]?.text,
    JSON.stringify(directInspection),
  );
  assert.equal(directInspection.request_id, REQUEST_CONTEXTS["evidence.inspect"].requestId);
  assert.equal(directInspection.trace_id, REQUEST_CONTEXTS["evidence.inspect"].traceId);
  const record = (directInspection.data as { record: Record<string, unknown> }).record;
  const receipt = record.receipt as Record<string, unknown>;
  const decision = receipt.policy_decision as Record<string, unknown>;
  assert.equal(decision.request_id, REQUEST_CONTEXTS["data.query"].requestId);
  assert.equal(decision.trace_id, REQUEST_CONTEXTS["data.query"].traceId);
  assert.notEqual(decision.trace_id, directInspection.trace_id);
  assert.equal(directInspection.schema, "gis-ai-go.evidence-inspect-result.v3");
  const inspectionReceipt = directInspection.evidence_receipt as Record<string, unknown>;
  const inspectionDecision = inspectionReceipt.policy_decision as Record<string, unknown>;
  assert.equal(inspectionReceipt.schema, "gis-ai-go.evidence-receipt.v3");
  assert.equal(inspectionReceipt.request_id, directInspection.request_id);
  assert.equal(inspectionReceipt.trace_id, directInspection.trace_id);
  assert.equal(inspectionDecision.request_id, directInspection.request_id);
  assert.equal(inspectionDecision.trace_id, directInspection.trace_id);
  assert.notEqual(inspectionReceipt.receipt_id, receipt.receipt_id);
  assert.equal(directFixture.ledger.verify().event_count, directCount);
  assert.equal(mcpFixture.ledger.verify().event_count, mcpCount);
});
