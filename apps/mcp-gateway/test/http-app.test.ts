import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
import test from "node:test";

import { fromJsonSchema, type JsonSchemaType } from "@modelcontextprotocol/server";

import {
  createCatalogueApplication,
  type CatalogueApplication,
} from "../src/catalogue-application.js";
import {
  loadCatalogueSnapshot,
  type CatalogueSnapshot,
} from "../src/catalogue-snapshot.js";
import {
  MAX_JSON_BODY_BYTES,
  MAX_JSON_RESPONSE_BYTES,
  BoundedJsonError,
  createGatewayHttpHandler,
  parseBoundedJsonBytes,
} from "../src/http-app.js";
import {
  CATALOGUE_OPERATION_JSON_SCHEMAS,
  catalogueOpenApiDocument,
  createCatalogueOpenApiDocument,
} from "../src/openapi.js";

const snapshot = {
  bundle: { records: [] },
  recordsById: new Map(),
  version: "0.1.0",
  revision: "a".repeat(40),
  contentRootSha256: "b".repeat(64),
  manifestSha256: "c".repeat(64),
  recordCount: 36,
  stale: false,
  warnings: Object.freeze([]),
  root: "/verified/catalogue",
} as unknown as CatalogueSnapshot;

const handle = createGatewayHttpHandler({
  snapshot,
  createTraceId: () => "d".repeat(32),
});

const SOURCE_CATALOGUE = fileURLToPath(
  new URL("../../../../artifacts/okf/", import.meta.url),
);
const VERIFIED_SNAPSHOT = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
  now: new Date("2026-08-20T12:00:00Z"),
});
const APPLICATION = createCatalogueApplication(VERIFIED_SNAPSHOT, {
  software: {
    name: "gis-ai-go-mcp-gateway",
    version: "0.1.0",
    revision: VERIFIED_SNAPSHOT.revision,
  },
  now: () => new Date("2026-08-20T12:34:56Z"),
});
const API_CONTEXT = Object.freeze({
  requestId: "direct-api-request-42",
  traceId: "e".repeat(32),
  instance: "/catalogue/search",
});
const directHandle = createGatewayHttpHandler({
  snapshot: VERIFIED_SNAPSHOT,
  application: APPLICATION,
  enabledApiOperations: ["catalogue.search", "catalogue.describe"],
  createTraceId: () => API_CONTEXT.traceId,
});

function request(path: string, init: RequestInit = {}): Request {
  const headers = new Headers(init.headers);
  if (!headers.has("host")) headers.set("host", "127.0.0.1:8787");
  return new Request(`http://127.0.0.1:8787${path}`, { ...init, headers });
}

function apiRequest(path: string, body: BodyInit, init: RequestInit = {}): Request {
  const headers = new Headers(init.headers);
  if (!headers.has("host")) headers.set("host", "127.0.0.1:8787");
  if (!headers.has("content-type")) headers.set("content-type", "application/json");
  if (!headers.has("x-request-id")) headers.set("x-request-id", API_CONTEXT.requestId);
  return new Request(`http://127.0.0.1:8787${path}`, {
    ...init,
    method: init.method ?? "POST",
    body,
    headers,
  });
}

function jsonPointerTarget(resource: unknown, reference: string): unknown {
  assert.match(reference, /^#\//u);
  return reference.slice(2).split("/").reduce<unknown>((current, token) => {
    assert.equal(typeof current, "object");
    assert.notEqual(current, null);
    assert.equal(Array.isArray(current), false);
    const key = token.replaceAll("~1", "/").replaceAll("~0", "~");
    assert.ok(key in (current as Record<string, unknown>), `unresolved ${reference}`);
    return (current as Record<string, unknown>)[key];
  }, resource);
}

function assertDocumentReferencesResolve(value: unknown, resource: unknown = value): void {
  if (Array.isArray(value)) {
    for (const item of value) assertDocumentReferencesResolve(item, resource);
    return;
  }
  if (value === null || typeof value !== "object") return;
  const record = value as Record<string, unknown>;
  const currentResource = typeof record.$id === "string" ? record : resource;
  if (typeof record.$ref === "string" && record.$ref.startsWith("#/")) {
    jsonPointerTarget(currentResource, record.$ref);
  }
  for (const child of Object.values(record)) {
    assertDocumentReferencesResolve(child, currentResource);
  }
}

test("reports verified catalogue health without activating operations", async () => {
  const response = await handle(request("/healthz"));
  assert.equal(response.status, 200);
  assert.equal(response.headers.get("cache-control"), "no-store");
  assert.deepEqual(await response.json(), {
    status: "ok",
    product: "GIS AI GO",
    lifecycle: "candidate-blocked",
    catalogue: {
      version: "0.1.0",
      revision: "a".repeat(40),
      content_root_sha256: "b".repeat(64),
      record_count: 36,
      stale: false,
      warnings: [],
    },
  });
});

test("readiness is deliberately blocked with zero active operations", async () => {
  const response = await handle(request("/readyz"));
  assert.equal(response.status, 503);
  assert.deepEqual(await response.json(), {
    status: "blocked",
    reason: "transport-and-interoperability-unverified",
    active_tools: [],
    active_api_operations: [],
  });
});

test("serves an OpenAPI candidate with no catalogue operation paths", async () => {
  const response = await handle(request("/openapi.json"));
  assert.equal(response.status, 200);
  const document = (await response.json()) as { paths: Record<string, unknown> };
  assert.deepEqual(Object.keys(document.paths).sort(), ["/healthz", "/openapi.json", "/readyz"]);
  assert.equal("/catalogue/search" in document.paths, false);
  assert.equal("/catalogue/describe" in document.paths, false);
  assert.equal(Object.isFrozen(catalogueOpenApiDocument), true);
  assert.equal(Object.isFrozen(catalogueOpenApiDocument.paths), true);
});

test("OpenAPI exactly follows the explicitly selected local-candidate routes", async () => {
  const response = await directHandle(request("/openapi.json"));
  assert.equal(response.status, 200);
  const document = (await response.json()) as {
    paths: Record<string, unknown>;
    components: {
      responses: Record<string, unknown>;
      schemas: Record<string, unknown>;
    };
    ["x-gis-ai-go-active-catalogue-operations"]: readonly string[];
    ["x-gis-ai-go-mounted-candidate-catalogue-operations"]: readonly string[];
    ["x-gis-ai-go-public-deployment"]: boolean;
  };
  assert.deepEqual(Object.keys(document.paths).sort(), [
    "/catalogue/describe",
    "/catalogue/search",
    "/healthz",
    "/openapi.json",
    "/readyz",
  ]);
  assert.deepEqual(document["x-gis-ai-go-active-catalogue-operations"], []);
  assert.deepEqual(document["x-gis-ai-go-mounted-candidate-catalogue-operations"], [
    "catalogue.describe",
    "catalogue.search",
  ]);
  assert.equal(document["x-gis-ai-go-public-deployment"], false);
  for (const [path, method] of [
    ["/healthz", "get"],
    ["/readyz", "get"],
    ["/openapi.json", "get"],
    ["/catalogue/search", "post"],
    ["/catalogue/describe", "post"],
  ] as const) {
    const pathItem = document.paths[path] as Record<string, unknown>;
    const operation = pathItem[method] as { responses: Record<string, unknown> };
    assert.deepEqual(operation.responses["429"], {
      $ref: "#/components/responses/RateLimited",
    });
  }
  assert.deepEqual(document.components.responses.RateLimited, {
    description: "The bounded listener has no free request-admission slot",
    headers: {
      "Retry-After": {
        description: "Seconds to wait before trying the request again",
        schema: { type: "integer", minimum: 1 },
      },
    },
    content: {
      "application/problem+json": {
        schema: { $ref: "#/components/schemas/CatalogueProblem" },
      },
    },
  });
  assert.deepEqual(
    document.components.schemas.CatalogueSearchResult,
    CATALOGUE_OPERATION_JSON_SCHEMAS["catalogue.search"].outputSchema,
  );
  assert.deepEqual(
    document.components.schemas.CatalogueDescribeResult,
    CATALOGUE_OPERATION_JSON_SCHEMAS["catalogue.describe"].outputSchema,
  );
  assert.equal(
    (document.components.schemas.CatalogueSearchResult as Record<string, unknown>).$id,
    "urn:gis-ai-go:schema:catalogue-search-result:v1",
  );
  assert.equal(
    (document.components.schemas.CatalogueDescribeResult as Record<string, unknown>).$id,
    "urn:gis-ai-go:schema:catalogue-describe-result:v1",
  );
  assertDocumentReferencesResolve(document);

  const searchOnly = createCatalogueOpenApiDocument(["catalogue.search"]);
  assert.equal("/catalogue/search" in searchOnly.paths, true);
  assert.equal("/catalogue/describe" in searchOnly.paths, false);
  assert.equal(Object.isFrozen(searchOnly.paths), true);
  assert.throws(
    () => createCatalogueOpenApiDocument(["catalogue.search", "catalogue.search"]),
    /must be unique/u,
  );
  assert.throws(
    () => createCatalogueOpenApiDocument(["spatial.locate" as never]),
    /unknown operation/u,
  );
});

test("built runtime exports self-contained exact schemas shared with MCP", async () => {
  assert.match(import.meta.url, /\/dist\/test\/http-app\.test\.js$/u);
  const contexts = {
    "catalogue.describe": {
      request: { record_id: "hmlr:dataset:price-paid-data" },
      context: { ...API_CONTEXT, instance: "/catalogue/describe" },
    },
    "catalogue.search": {
      request: { query: "Price Paid", limit: 1 },
      context: API_CONTEXT,
    },
  } as const;
  for (const operation of ["catalogue.describe", "catalogue.search"] as const) {
    const schema = CATALOGUE_OPERATION_JSON_SCHEMAS[operation].outputSchema;
    const references = JSON.stringify(schema).match(/"\$ref":"([^"]+)"/gu) ?? [];
    assert.ok(references.length > 0);
    assert.ok(references.every((reference) => reference.includes('"#/$defs/')));
    const standard = fromJsonSchema(schema as JsonSchemaType);
    const fixture = operation === "catalogue.search"
      ? APPLICATION.search(contexts[operation].request, contexts[operation].context)
      : APPLICATION.describe(contexts[operation].request, contexts[operation].context);
    const validation = await standard["~standard"].validate(fixture);
    assert.equal("issues" in validation, false, JSON.stringify(validation));
  }
});

test("rejects unrecognised hosts and cross-origin requests", async () => {
  const badHost = await handle(
    request("/healthz", { headers: { host: "attacker.invalid" } }),
  );
  assert.equal(badHost.status, 400);
  const badOrigin = await handle(
    request("/healthz", { headers: { origin: "https://attacker.invalid" } }),
  );
  assert.equal(badOrigin.status, 400);
  assert.equal(badOrigin.headers.get("access-control-allow-origin"), null);

  const mismatchedAuthority = await handle(
    new Request("http://attacker.invalid/healthz", {
      headers: { host: "127.0.0.1:8787" },
    }),
  );
  assert.equal(mismatchedAuthority.status, 400);
});

test("rejects methods, query strings, unknown routes and unacceptable media", async () => {
  for (const candidate of [
    request("/healthz", { method: "POST" }),
    request("/healthz?verbose=true"),
    request("/catalogue/search"),
    request("/healthz", { headers: { accept: "text/html" } }),
  ]) {
    const response = await handle(candidate);
    assert.ok(response.status >= 400);
    assert.equal(response.headers.get("content-type"), "application/problem+json; charset=utf-8");
    const problem = (await response.json()) as Record<string, unknown>;
    assert.equal(problem.schema, "gis-ai-go.catalogue-problem.v1");
    assert.equal(problem.trace_id, "d".repeat(32));
  }
});

test("rejects non-canonical request paths without escaping the problem envelope", async () => {
  for (const path of ["/%41", "/%2f", "/%ZZ"]) {
    const response = await handle(request(path));
    assert.equal(response.status, 400);
    assert.equal(response.headers.get("content-type"), "application/problem+json; charset=utf-8");
    const problem = (await response.json()) as Record<string, unknown>;
    assert.equal(problem.schema, "gis-ai-go.catalogue-problem.v1");
    assert.equal(problem.code, "invalid_request");
    assert.equal(problem.trace_id, "d".repeat(32));
    assert.equal("instance" in problem, false);
  }

  const canonical = await handle(request("/unknown"));
  assert.equal((await canonical.json() as Record<string, unknown>).instance, "/unknown");
});

test("accepts a bounded request identifier without reflecting an invalid one", async () => {
  const accepted = await handle(
    request("/unknown", { headers: { "x-request-id": "caller-request:42" } }),
  );
  assert.equal((await accepted.json() as Record<string, unknown>).request_id, "caller-request:42");

  const rejected = await handle(
    request("/unknown", { headers: { "x-request-id": "bad request id" } }),
  );
  assert.match(
    (await rejected.json() as Record<string, unknown>).request_id as string,
    /^[0-9a-f]{32}$/u,
  );
});

test("direct search returns evidenced Price Paid and INSPIRE results", async () => {
  const originalFetch = globalThis.fetch;
  let providerCalls = 0;
  globalThis.fetch = (() => {
    providerCalls += 1;
    throw new Error("A catalogue route must not make a provider call");
  }) as typeof fetch;
  try {
    const pricePaidRequest = {
      query: "Price Paid",
      facets: { types: ["dataset"] },
    };
    const pricePaidResponse = await directHandle(
      apiRequest("/catalogue/search", JSON.stringify(pricePaidRequest)),
    );
    assert.equal(pricePaidResponse.status, 200);
    assert.equal(pricePaidResponse.headers.get("content-type"), "application/json; charset=utf-8");
    assert.equal(pricePaidResponse.headers.get("access-control-allow-origin"), null);
    const pricePaid = await pricePaidResponse.json() as {
      operation: string;
      request_id: string;
      trace_id: string;
      data: { records: readonly { id: string }[] };
      evidence_receipt: {
        schema: string;
        evidence_handling: Readonly<Record<string, string>>;
      };
    };
    assert.equal(pricePaid.operation, "catalogue.search");
    assert.equal(pricePaid.request_id, API_CONTEXT.requestId);
    assert.equal(pricePaid.trace_id, API_CONTEXT.traceId);
    assert.equal(pricePaid.data.records[0]?.id, "hmlr:dataset:price-paid-data");
    assert.equal(pricePaid.evidence_receipt.schema, "gis-ai-go.evidence-receipt.v1");
    assert.deepEqual(pricePaid.evidence_receipt.evidence_handling, {
      attestation: "not-attested",
      delivery: "inline-only",
      persistence: "not-persisted",
    });

    const inspireRequest = {
      query: "INSPIRE",
      facets: { tags: ["inspire"] },
      limit: 100,
    };
    const inspireResponse = await directHandle(
      apiRequest("/catalogue/search", JSON.stringify(inspireRequest)),
    );
    assert.equal(inspireResponse.status, 200);
    const inspire = await inspireResponse.json() as {
      data: { records: readonly { id: string }[] };
    };
    const inspireIds = inspire.data.records.map(({ id }) => id);
    assert.ok(inspireIds.includes("hmlr:dataset:inspire-index-polygons"));
    assert.ok(inspireIds.includes("hmlr:dataset:local-land-charges-inspire"));
    assert.equal(providerCalls, 0);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("direct API material is byte-equivalent to the shared application result", async () => {
  const searchRequest = {
    query: "  PRICE   paid ",
    facets: {
      rights: ["open-with-conditions"],
      types: ["dataset"],
    },
    limit: 5,
  };
  const searchResponse = await directHandle(
    apiRequest("/catalogue/search", JSON.stringify(searchRequest)),
  );
  assert.equal(searchResponse.status, 200);
  assert.deepEqual(
    await searchResponse.json(),
    APPLICATION.search(searchRequest, API_CONTEXT),
  );

  const describeRequest = {
    record_id: "hmlr:dataset:inspire-index-polygons",
    include: ["sources", "relationships"],
  };
  const describeResponse = await directHandle(
    apiRequest("/catalogue/describe", JSON.stringify(describeRequest)),
  );
  assert.equal(describeResponse.status, 200);
  const described = await describeResponse.json() as {
    operation: string;
    data: { record: { id: string }; included: { sources: readonly unknown[] } };
    evidence_receipt: { operation: { name: string } };
  };
  assert.deepEqual(described, APPLICATION.describe(describeRequest, {
    ...API_CONTEXT,
    instance: "/catalogue/describe",
  }));
  assert.equal(described.operation, "catalogue.describe");
  assert.equal(described.data.record.id, "hmlr:dataset:inspire-index-polygons");
  assert.ok(described.data.included.sources.length > 0);
  assert.equal(described.evidence_receipt.operation.name, "catalogue.describe");
});

test("direct API returns the controlled validation and not-found problem envelopes", async () => {
  const invalid = await directHandle(
    apiRequest("/catalogue/search", JSON.stringify({ provider: "hmlr" })),
  );
  assert.equal(invalid.status, 400);
  assert.equal(invalid.headers.get("content-type"), "application/problem+json; charset=utf-8");
  const invalidProblem = await invalid.json() as {
    schema: string;
    code: string;
    request_id: string;
    trace_id: string;
    errors: readonly { path: string; code: string }[];
  };
  assert.equal(invalidProblem.schema, "gis-ai-go.catalogue-problem.v1");
  assert.equal(invalidProblem.code, "invalid_request");
  assert.equal(invalidProblem.request_id, API_CONTEXT.requestId);
  assert.equal(invalidProblem.trace_id, API_CONTEXT.traceId);
  assert.deepEqual(invalidProblem.errors[0], {
    path: "$.provider",
    code: "unknown_property",
    message: "Remove the unknown property provider.",
  });

  const missing = await directHandle(
    apiRequest(
      "/catalogue/describe",
      JSON.stringify({ record_id: "missing:record" }),
    ),
  );
  assert.equal(missing.status, 404);
  assert.equal((await missing.json() as Record<string, unknown>).code, "record_not_found");
});

test("direct API rejects malformed, duplicate and oversized JSON", async () => {
  const malformedBodies = [
    "",
    "{",
    "{} trailing",
    "{\"query\":}",
    "{\"query\":\"\\ud800\"}",
    `{${'"a":{'.repeat(18)}"value":true${"}".repeat(18)}}`,
  ];
  for (const body of malformedBodies) {
    const response = await directHandle(apiRequest("/catalogue/search", body));
    assert.equal(response.status, 400);
    assert.equal((await response.json() as Record<string, unknown>).code, "invalid_request");
  }

  for (const body of [
    "{\"query\":\"Price\",\"query\":\"Paid\"}",
    "{\"facets\":{\"tags\":[\"inspire\"],\"tags\":[\"hmlr\"]}}",
    "{\"query\":\"Price\",\"\\u0071uery\":\"Paid\"}",
  ]) {
    const response = await directHandle(apiRequest("/catalogue/search", body));
    assert.equal(response.status, 400);
    assert.match(
      (await response.json() as Record<string, unknown>).detail as string,
      /duplicate object properties/u,
    );
  }

  const oversized = JSON.stringify({ query: "x".repeat(MAX_JSON_BODY_BYTES) });
  const oversizedResponse = await directHandle(
    apiRequest("/catalogue/search", oversized),
  );
  assert.equal(oversizedResponse.status, 400);
  assert.match(
    (await oversizedResponse.json() as Record<string, unknown>).detail as string,
    /exceeds 32768 bytes/u,
  );

  const declaredOversized = await directHandle(
    apiRequest("/catalogue/search", "{}", {
      headers: { "content-length": String(MAX_JSON_BODY_BYTES + 1) },
    }),
  );
  assert.equal(declaredOversized.status, 400);
});

test("shared byte parser provides the same strict boundary for Node and MCP ingress", () => {
  const encoder = new TextEncoder();
  assert.deepEqual(
    parseBoundedJsonBytes(encoder.encode('{"query":"Price Paid"}'), 65_536),
    { query: "Price Paid" },
  );
  const failures: readonly [Uint8Array, BoundedJsonError["failure"]][] = [
    [new Uint8Array([0xff]), "malformed"],
    [encoder.encode('{"query":"a","\\u0071uery":"b"}'), "duplicate"],
    [encoder.encode("{}"), "too_large"],
  ];
  for (const [bytes, failure] of failures) {
    assert.throws(
      () => parseBoundedJsonBytes(bytes, failure === "too_large" ? 1 : 65_536),
      (error: unknown) => error instanceof BoundedJsonError && error.failure === failure,
    );
  }
  assert.throws(() => parseBoundedJsonBytes(encoder.encode("{}"), 0), TypeError);
  assert.throws(
    () => parseBoundedJsonBytes(encoder.encode("{}"), 1_048_577),
    TypeError,
  );
});

test("direct API closes media, method, query, host and origin boundaries", async () => {
  const cases: readonly Request[] = [
    apiRequest("/catalogue/search?query=Price", "{}"),
    apiRequest("/catalogue/search", "{}", { method: "PUT" }),
    apiRequest("/catalogue/search", "{}", { method: "OPTIONS" }),
    apiRequest("/catalogue/search", "{}", { headers: { accept: "text/html" } }),
    apiRequest("/catalogue/search", "{}", { headers: { accept: "application/json;q=0" } }),
    apiRequest("/catalogue/search", "{}", { headers: { "content-type": "text/plain" } }),
    apiRequest("/catalogue/search", "{}", {
      headers: { "content-type": "application/json; charset=iso-8859-1" },
    }),
    apiRequest("/catalogue/search", "{}", {
      headers: { "content-type": "application/json; charset=\"utf-8" },
    }),
    apiRequest("/catalogue/search", "{}", {
      headers: { "content-type": "application/json; charset=utf-8\"" },
    }),
    apiRequest("/catalogue/search", "{}", { headers: { host: "attacker.invalid" } }),
    apiRequest("/catalogue/search", "{}", {
      headers: { origin: "https://attacker.invalid" },
    }),
  ];
  for (const candidate of cases) {
    const response = await directHandle(candidate);
    assert.ok(response.status >= 400);
    assert.equal(response.headers.get("access-control-allow-origin"), null);
    assert.equal(response.headers.get("content-type"), "application/problem+json; charset=utf-8");
    assert.equal(
      (await response.json() as Record<string, unknown>).schema,
      "gis-ai-go.catalogue-problem.v1",
    );
  }

  const utf8 = await directHandle(
    apiRequest("/catalogue/search", "{}", {
      headers: { "content-type": "application/json; charset=\"UTF-8\"" },
    }),
  );
  assert.equal(utf8.status, 200);
  assert.equal(utf8.headers.get("access-control-allow-origin"), null);
});

test("implemented routes remain absent unless explicitly selected", async () => {
  const response = await handle(
    apiRequest("/catalogue/search", JSON.stringify({ query: "Price Paid" })),
  );
  assert.equal(response.status, 400);
  const problem = await response.json() as Record<string, unknown>;
  assert.equal(problem.code, "invalid_request");
  assert.equal(problem.detail, "The requested route is not part of this candidate.");

  assert.throws(
    () => createGatewayHttpHandler({
      snapshot: VERIFIED_SNAPSHOT,
      application: APPLICATION,
      catalogueApplicationOptions: {
        software: {
          name: "gis-ai-go-mcp-gateway",
          version: "0.1.0",
          revision: VERIFIED_SNAPSHOT.revision,
        },
      },
      enabledApiOperations: ["catalogue.search"],
    }),
    /either a shared catalogue application or catalogue application options/u,
  );
});

test("direct API bounds success bytes and safely reports failures", async () => {
  const reported: Error[] = [];
  const base = APPLICATION.search({}, {
    ...API_CONTEXT,
    instance: "/catalogue/search",
  });
  const oversizedApplication = {
    search: () => ({
      ...base,
      warnings: ["x".repeat(MAX_JSON_RESPONSE_BYTES)],
    }) as never,
    describe: APPLICATION.describe,
  } satisfies CatalogueApplication;
  const oversizedHandler = createGatewayHttpHandler({
    snapshot: VERIFIED_SNAPSHOT,
    application: oversizedApplication,
    enabledApiOperations: ["catalogue.search"],
    createTraceId: () => API_CONTEXT.traceId,
    onerror: (error) => reported.push(error),
  });
  const oversized = await oversizedHandler(
    apiRequest("/catalogue/search", "{}"),
  );
  assert.equal(oversized.status, 422);
  assert.equal(
    (await oversized.json() as Record<string, unknown>).code,
    "complexity_limit_exceeded",
  );
  assert.equal(reported.length, 1);

  const secret = new Error("do not return this application detail");
  const brokenHandler = createGatewayHttpHandler({
    snapshot: VERIFIED_SNAPSHOT,
    application: {
      search: () => {
        throw secret;
      },
      describe: APPLICATION.describe,
    },
    enabledApiOperations: ["catalogue.search"],
    createTraceId: () => API_CONTEXT.traceId,
    onerror: (error) => {
      reported.push(error);
      throw new Error("reporting failure must be contained");
    },
  });
  const broken = await brokenHandler(apiRequest("/catalogue/search", "{}"));
  assert.equal(broken.status, 500);
  const problemText = await broken.text();
  assert.equal(problemText.includes(secret.message), false);
  assert.equal(problemText.includes("reporting failure"), false);
  assert.equal(JSON.parse(problemText).code, "internal_error");
  assert.deepEqual(reported, [reported[0], secret]);
});
