import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

import { gatewayMetadata } from "./metadata.js";

const HEALTH_URL = "http://127.0.0.1:8787/healthz";
const HEALTH_TIMEOUT_MS = 2_000;

export function assertFixedHealthcheckArguments(argv: readonly string[]): void {
  if (argv.length !== 2) throw new Error("The gateway health check does not accept arguments");
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

export async function checkGatewayContainerHealth(): Promise<void> {
  assertFixedHealthcheckArguments(process.argv);
  const response = await fetch(HEALTH_URL, {
    headers: { accept: "application/json" },
    signal: AbortSignal.timeout(HEALTH_TIMEOUT_MS),
  });
  if (response.status !== 200) throw new Error("The gateway health response is unavailable");
  const body: unknown = await response.json();
  if (
    !isRecord(body) ||
    body.status !== "ok" ||
    body.product !== gatewayMetadata.product ||
    body.lifecycle !== "candidate-blocked" ||
    !isRecord(body.catalogue) ||
    typeof body.catalogue.version !== "string" ||
    typeof body.catalogue.revision !== "string" ||
    !/^[0-9a-f]{40}$/u.test(body.catalogue.revision) ||
    !/^[0-9a-f]{64}$/u.test(String(body.catalogue.content_root_sha256))
  ) {
    throw new Error("The gateway health response does not match the blocked candidate");
  }
}

const entryPath = process.argv[1];
if (entryPath !== undefined && pathToFileURL(resolve(entryPath)).href === import.meta.url) {
  await checkGatewayContainerHealth().catch(() => {
    process.exitCode = 1;
  });
}
