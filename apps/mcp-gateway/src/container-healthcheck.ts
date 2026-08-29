import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

import {
  CANDIDATE_ACTIVATION_LIFECYCLE,
  CANDIDATE_ACTIVATION_OPERATIONS,
} from "./candidate-activation.js";
import { gatewayMetadata } from "./metadata.js";

const HEALTH_URL = "http://127.0.0.1:8787/healthz";
const READINESS_URL = "http://127.0.0.1:8787/readyz";
const HEALTH_TIMEOUT_MS = 2_000;

export function assertFixedHealthcheckArguments(argv: readonly string[]): void {
  if (argv.length !== 2) throw new Error("The gateway health check does not accept arguments");
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

export async function checkGatewayContainerHealth(): Promise<void> {
  assertFixedHealthcheckArguments(process.argv);
  const healthResponse = await fetch(HEALTH_URL, {
    headers: { accept: "application/json" },
    signal: AbortSignal.timeout(HEALTH_TIMEOUT_MS),
  });
  if (healthResponse.status !== 200) {
    throw new Error("The gateway health response is unavailable");
  }
  const health: unknown = await healthResponse.json();
  if (
    !isRecord(health) ||
    health.status !== "ok" ||
    health.product !== gatewayMetadata.product ||
    health.lifecycle !== CANDIDATE_ACTIVATION_LIFECYCLE ||
    health.production_registration !== false ||
    !isRecord(health.catalogue) ||
    typeof health.catalogue.version !== "string" ||
    typeof health.catalogue.revision !== "string" ||
    !/^[0-9a-f]{40}$/u.test(health.catalogue.revision) ||
    !/^[0-9a-f]{64}$/u.test(String(health.catalogue.content_root_sha256))
  ) {
    throw new Error("The gateway health response does not match the exact-five candidate");
  }

  const readinessResponse = await fetch(READINESS_URL, {
    headers: { accept: "application/json" },
    signal: AbortSignal.timeout(HEALTH_TIMEOUT_MS),
  });
  if (readinessResponse.status !== 200 && readinessResponse.status !== 503) {
    throw new Error("The gateway readiness response is unavailable");
  }
  const readiness: unknown = await readinessResponse.json();
  if (!isRecord(readiness)) {
    throw new Error("The gateway readiness response does not match the exact-five candidate");
  }
  const acceptedReadiness = (
    (readinessResponse.status === 200 &&
      readiness.status === "ready" &&
      readiness.reason === "candidate-assembly-verified") ||
    (readinessResponse.status === 503 &&
      readiness.status === "blocked" &&
      readiness.reason === "reconciliation-capacity-exhausted")
  );
  if (
    !acceptedReadiness ||
    readiness.production_registration !== false ||
    !Array.isArray(readiness.active_tools) ||
    !Array.isArray(readiness.active_api_operations) ||
    readiness.active_tools.length !== CANDIDATE_ACTIVATION_OPERATIONS.length ||
    readiness.active_tools.some(
      (operation, index) => operation !== CANDIDATE_ACTIVATION_OPERATIONS[index],
    ) ||
    readiness.active_api_operations.length !== CANDIDATE_ACTIVATION_OPERATIONS.length ||
    readiness.active_api_operations.some(
      (operation, index) => operation !== CANDIDATE_ACTIVATION_OPERATIONS[index],
    )
  ) {
    throw new Error("The gateway readiness response does not match the exact-five candidate");
  }
}

const entryPath = process.argv[1];
if (entryPath !== undefined && pathToFileURL(resolve(entryPath)).href === import.meta.url) {
  await checkGatewayContainerHealth().catch(() => {
    process.exitCode = 1;
  });
}
