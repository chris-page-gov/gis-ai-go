import { request as nodeRequest } from "node:http";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

import {
  CANDIDATE_ACTIVATION_LIFECYCLE,
  CANDIDATE_ACTIVATION_OPERATIONS,
} from "./candidate-activation.js";
import { gatewayContainerHealthHeaders } from "./container-ingress.js";
import { gatewayMetadata } from "./metadata.js";
import { parsePublicHttpsOrigin } from "./public-origin.js";

const HEALTH_URL = "http://127.0.0.1:8787/healthz";
const READINESS_URL = "http://127.0.0.1:8787/readyz";
const HEALTH_TIMEOUT_MS = 2_000;
const MAX_HEALTH_RESPONSE_BYTES = 32_768;

interface GatewayContainerHealthResponse {
  readonly status: number;
  json(): Promise<unknown>;
}

export function assertFixedHealthcheckArguments(argv: readonly string[]): void {
  if (argv.length !== 2) throw new Error("The gateway health check does not accept arguments");
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

/**
 * Use Node HTTP only when public mode must send an exact Host header.
 *
 * Node fetch implementations may replace a caller-supplied Host. The native
 * request API preserves it while the URL remains restricted to the private
 * loopback health surface.
 */
export function requestGatewayContainerHealth(
  rawUrl: string,
  headers: Readonly<Record<string, string>>,
): Promise<GatewayContainerHealthResponse> {
  const url = new URL(rawUrl);
  const headerKeys = Object.keys(headers).sort().join(",");
  if (
    url.protocol !== "http:" ||
    url.hostname !== "127.0.0.1" ||
    url.port === "" ||
    url.username !== "" ||
    url.password !== "" ||
    url.search !== "" ||
    url.hash !== "" ||
    (url.pathname !== "/healthz" && url.pathname !== "/readyz") ||
    headers.accept !== "application/json" ||
    (headerKeys !== "accept" && headerKeys !== "accept,host") ||
    (headers.host !== undefined &&
      parsePublicHttpsOrigin(`https://${headers.host}`).hostname !== headers.host)
  ) {
    throw new Error("The gateway health request boundary is invalid");
  }
  if (headers.host === undefined) {
    return fetch(rawUrl, {
      headers,
      signal: AbortSignal.timeout(HEALTH_TIMEOUT_MS),
    });
  }
  return new Promise((resolveRequest, rejectRequest) => {
    let settled = false;
    const fail = (error: Error): void => {
      if (settled) return;
      settled = true;
      rejectRequest(error);
    };
    const request = nodeRequest(url, { method: "GET", headers }, (response) => {
      const chunks: Buffer[] = [];
      let length = 0;
      response.on("data", (chunk: Buffer) => {
        length += chunk.byteLength;
        if (length > MAX_HEALTH_RESPONSE_BYTES) {
          response.destroy(new Error("The gateway health response is too large"));
          return;
        }
        chunks.push(chunk);
      });
      response.once("error", fail);
      response.once("end", () => {
        if (settled) return;
        settled = true;
        const body = Buffer.concat(chunks).toString("utf8");
        resolveRequest(Object.freeze({
          status: response.statusCode ?? 0,
          json: async (): Promise<unknown> => JSON.parse(body) as unknown,
        }));
      });
    });
    request.once("error", fail);
    request.setTimeout(HEALTH_TIMEOUT_MS, () => {
      request.destroy(new Error("The gateway health request timed out"));
    });
    request.end();
  });
}

export async function checkGatewayContainerHealth(): Promise<void> {
  assertFixedHealthcheckArguments(process.argv);
  const headers = gatewayContainerHealthHeaders(process.env);
  const healthResponse = await requestGatewayContainerHealth(HEALTH_URL, headers);
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

  const readinessResponse = await requestGatewayContainerHealth(READINESS_URL, headers);
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
