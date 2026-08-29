import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

import {
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
} from "@gis-ai-go/evidence";
import type {
  ApprovedOnsDataQueryCacheRecord,
} from "@gis-ai-go/provider-adapter-sdk";

import { catalogueActivation } from "../src/activation.js";
import { createCandidateActivation } from "../src/candidate-activation.js";
import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";
import {
  GATEWAY_CONTAINER_PUBLIC_HTTPS_ORIGIN_VARIABLE,
  gatewayContainerHealthHeaders,
  gatewayContainerIngressOptions,
} from "../src/container-ingress.js";
import {
  assertCandidateContainerAuthority,
  assertFixedContainerArguments,
  GATEWAY_CONTAINER_APPROVED_CACHE_BYTES,
  GATEWAY_CONTAINER_APPROVED_CACHE_PATH,
  GATEWAY_CONTAINER_APPROVED_CACHE_SHA256,
  GATEWAY_CONTAINER_CATALOGUE_ROOT,
  GATEWAY_CONTAINER_HOST,
  GATEWAY_CONTAINER_LEDGER_ROOT,
  GATEWAY_CONTAINER_PORT,
  GATEWAY_CONTAINER_READINESS_INTEGRITY_FAILURE_EVENT,
  GATEWAY_CONTAINER_RECONCILIATION_ROOT,
  GATEWAY_CONTAINER_REQUEST_FAILURE_EVENT,
  gatewayContainerErrorEvent,
} from "../src/container-main.js";
import { EVIDENCE_READINESS_INTEGRITY_FAILURE_MESSAGE } from "../src/readiness-integrity.js";
import {
  assertFixedHealthcheckArguments,
  checkGatewayContainerHealth,
} from "../src/container-healthcheck.js";

test("keeps the container entry point fixed and activates only the unregistered exact five", async (t) => {
  assert.equal(GATEWAY_CONTAINER_HOST, "0.0.0.0");
  assert.equal(GATEWAY_CONTAINER_PORT, 8_787);
  assert.equal(GATEWAY_CONTAINER_CATALOGUE_ROOT, "/app/artifacts/okf");
  assert.equal(GATEWAY_CONTAINER_LEDGER_ROOT, "/var/lib/gis-ai-go/ledger");
  assert.equal(
    GATEWAY_CONTAINER_RECONCILIATION_ROOT,
    "/var/lib/gis-ai-go/reconciliation",
  );
  assert.notEqual(GATEWAY_CONTAINER_LEDGER_ROOT, GATEWAY_CONTAINER_RECONCILIATION_ROOT);
  assert.equal(
    GATEWAY_CONTAINER_APPROVED_CACHE_PATH,
    "/app/providers/ons/data-query-approved-cache.v1.json",
  );
  assert.equal(GATEWAY_CONTAINER_APPROVED_CACHE_BYTES, 3_066);
  assert.equal(
    GATEWAY_CONTAINER_APPROVED_CACHE_SHA256,
    "4b60e567d700d64ba98b87001e7adb10e25b2342403040b4a996d373b2714b8c",
  );
  assert.deepEqual(catalogueActivation.activeTools, []);
  assert.deepEqual(catalogueActivation.activeApiOperations, []);

  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-container-authority-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const snapshot = await loadCatalogueSnapshot(
    fileURLToPath(new URL("../../../../artifacts/okf/", import.meta.url)),
    { now: new Date("2026-08-29T00:00:00.000Z") },
  );
  const ledger = openPublicEvidenceLedger({
    rootDirectory: join(root, "ledger"),
    now: () => new Date("2026-08-29T00:00:01.000Z"),
  });
  const reconciliationIndex = openEvidenceReconciliationIndex({
    rootDirectory: join(root, "reconciliation"),
    ledger,
    now: () => new Date("2026-08-29T00:00:02.000Z"),
  });
  const record = JSON.parse(readFileSync(new URL(
    "../../../../providers/ons/data-query-approved-cache.v1.json",
    import.meta.url,
  ), "utf8")) as ApprovedOnsDataQueryCacheRecord;
  const assembly = createCandidateActivation(
    snapshot,
    ledger,
    reconciliationIndex,
    record,
  );
  assertCandidateContainerAuthority(assembly);
});

test("rejects command-line configuration for the server and health check", () => {
  assertFixedContainerArguments(["node", "container-main.js"]);
  assertFixedHealthcheckArguments(["node", "container-healthcheck.js"]);
  assert.throws(
    () => assertFixedContainerArguments(["node", "container-main.js", "--activate"]),
    /does not accept arguments/u,
  );
  assert.throws(
    () => assertFixedHealthcheckArguments(["node", "container-healthcheck.js", "--url"]),
    /does not accept arguments/u,
  );
});

test("selects either the fixed loopback boundary or one canonical public HTTPS origin", () => {
  assert.deepEqual(gatewayContainerIngressOptions({}), {
    directAllowedHosts: ["127.0.0.1:8787", "localhost:8787"],
    directAllowedOrigins: ["http://127.0.0.1:8787", "http://localhost:8787"],
    mcpAllowedHosts: ["127.0.0.1:8787", "localhost:8787"],
    mcpAllowedHostnames: ["127.0.0.1", "localhost"],
    mcpAllowedOrigins: ["http://127.0.0.1:8787", "http://localhost:8787"],
  });
  assert.deepEqual(gatewayContainerHealthHeaders({}), { accept: "application/json" });
  const origin = "https://gateway.example.com";
  const options = gatewayContainerIngressOptions({
    [GATEWAY_CONTAINER_PUBLIC_HTTPS_ORIGIN_VARIABLE]: origin,
  });
  assert.deepEqual(options, {
    directAllowedHosts: [
      "gateway.example.com",
      "gateway.example.com:443",
    ],
    directAllowedOrigins: [origin],
    mcpAllowedHosts: [
      "gateway.example.com",
      "gateway.example.com:443",
    ],
    mcpAllowedHostnames: ["gateway.example.com"],
    mcpAllowedOrigins: [origin],
    openApiServerOrigin: origin,
  });
  assert.deepEqual(
    gatewayContainerHealthHeaders({
      [GATEWAY_CONTAINER_PUBLIC_HTTPS_ORIGIN_VARIABLE]: origin,
    }),
    { accept: "application/json", host: "gateway.example.com" },
  );
  assert.equal(Object.isFrozen(options), true);
  for (const value of Object.values(options)) assert.equal(Object.isFrozen(value), true);
});

test("rejects widened or non-canonical public ingress origins", () => {
  const rejected = [
    "",
    " https://gateway.example.com",
    "https://gateway.example.com/",
    "http://gateway.example.com",
    "https://GATEWAY.example.com",
    "https://gateway.example.com:443",
    "https://gateway.example.com/path",
    "https://gateway.example.com?query=1",
    "https://gateway.example.com#fragment",
    "https://user:password@gateway.example.com",
    "https://*.example.com",
    "https://gateway_name.example.com",
    "https://single-label",
    "https://127.0.0.1",
    "https://localhost",
    "https://gateway.alt",
    "https://gateway.home.arpa",
    "https://gateway.internal",
    "https://mcp.invalid",
    "https://mcp.example",
    "https://mcp.test",
    "https://mcp.local",
    "https://mcp.onion",
    "https://caf\u00e9.example.com",
  ];
  for (const rawOrigin of rejected) {
    assert.throws(
      () => gatewayContainerIngressOptions({
        [GATEWAY_CONTAINER_PUBLIC_HTTPS_ORIGIN_VARIABLE]: rawOrigin,
      }),
      /public HTTPS origin is invalid/u,
      rawOrigin,
    );
  }
  assert.throws(
    () => gatewayContainerIngressOptions({
      [GATEWAY_CONTAINER_PUBLIC_HTTPS_ORIGIN_VARIABLE]: 42 as unknown as string,
    }),
    /public HTTPS origin is invalid/u,
  );
});

test("keeps the container healthy when only new-claim readiness is exhausted", async (context) => {
  context.mock.method(globalThis, "fetch", async (input: string | URL | Request) => {
    const url = typeof input === "string"
      ? input
      : input instanceof URL
        ? input.href
        : input.url;
    const payload = url.endsWith("/healthz")
      ? {
          status: "ok",
          product: "GIS AI GO",
          lifecycle: "candidate-unregistered",
          production_registration: false,
          catalogue: {
            version: "0.2.0",
            revision: "a".repeat(40),
            content_root_sha256: "b".repeat(64),
          },
        }
      : {
          status: "blocked",
          reason: "reconciliation-capacity-exhausted",
          production_registration: false,
          active_tools: [
            "catalogue.search",
            "catalogue.describe",
            "selection.resolve",
            "data.query",
            "evidence.inspect",
          ],
          active_api_operations: [
            "catalogue.search",
            "catalogue.describe",
            "selection.resolve",
            "data.query",
            "evidence.inspect",
          ],
        };
    return new Response(JSON.stringify(payload), {
      status: url.endsWith("/healthz") ? 200 : 503,
      headers: { "content-type": "application/json" },
    });
  });
  await checkGatewayContainerHealth();
});

test("maps readiness corruption and hostile errors to fixed path-free events", () => {
  assert.equal(
    gatewayContainerErrorEvent(
      new Error(EVIDENCE_READINESS_INTEGRITY_FAILURE_MESSAGE),
    ),
    GATEWAY_CONTAINER_READINESS_INTEGRITY_FAILURE_EVENT,
  );
  const hostile = "/var/lib/private/ledger Bearer secret raw-idempotency-key";
  const event = gatewayContainerErrorEvent(new Error(hostile));
  assert.equal(event, GATEWAY_CONTAINER_REQUEST_FAILURE_EVENT);
  assert.equal(event.includes(hostile), false);
  assert.equal(event.includes("/var/"), false);
  assert.equal(event.includes("Bearer"), false);
});
