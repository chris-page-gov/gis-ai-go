import assert from "node:assert/strict";
import test from "node:test";

import { catalogueActivation } from "../src/activation.js";
import {
  assertBlockedContainerAuthority,
  assertFixedContainerArguments,
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
import { assertFixedHealthcheckArguments } from "../src/container-healthcheck.js";

test("keeps the container entry point fixed and production authority blocked", () => {
  assert.equal(GATEWAY_CONTAINER_HOST, "0.0.0.0");
  assert.equal(GATEWAY_CONTAINER_PORT, 8_787);
  assert.equal(GATEWAY_CONTAINER_CATALOGUE_ROOT, "/app/artifacts/okf");
  assert.equal(GATEWAY_CONTAINER_LEDGER_ROOT, "/var/lib/gis-ai-go/ledger");
  assert.equal(
    GATEWAY_CONTAINER_RECONCILIATION_ROOT,
    "/var/lib/gis-ai-go/reconciliation",
  );
  assert.notEqual(GATEWAY_CONTAINER_LEDGER_ROOT, GATEWAY_CONTAINER_RECONCILIATION_ROOT);
  assert.deepEqual(catalogueActivation.activeTools, []);
  assert.deepEqual(catalogueActivation.activeApiOperations, []);
  assertBlockedContainerAuthority();
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
