import assert from "node:assert/strict";
import test from "node:test";

import type { CatalogueSnapshot } from "../src/catalogue-snapshot.js";
import { createGatewayHttpHandler } from "../src/http-app.js";
import { catalogueOpenApiDocument } from "../src/openapi.js";

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

function request(path: string, init: RequestInit = {}): Request {
  const headers = new Headers(init.headers);
  if (!headers.has("host")) headers.set("host", "127.0.0.1:8787");
  return new Request(`http://127.0.0.1:8787${path}`, { ...init, headers });
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
    reason: "inline-evidence-and-public-policy-unavailable",
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
