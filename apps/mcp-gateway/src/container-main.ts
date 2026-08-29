import { createHash } from "node:crypto";
import { lstatSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

import {
  PublicEvidenceLedger,
  PublicEvidenceReconciliationIndex,
} from "@gis-ai-go/evidence";
import {
  createApprovedOnsDataQueryCache,
  parseStrictJson,
  type ApprovedOnsDataQueryCacheRecord,
} from "@gis-ai-go/provider-adapter-sdk";

import { catalogueActivation } from "./activation.js";
import {
  CANDIDATE_ACTIVATION_LIFECYCLE,
  CANDIDATE_ACTIVATION_OPERATIONS,
  CANDIDATE_ACTIVATION_RESOURCES,
  createCandidateActivation,
} from "./candidate-activation.js";
import { loadCatalogueSnapshot } from "./catalogue-snapshot.js";
import {
  createGovernedCandidateNodeServer,
  type GatewayNodeServer,
} from "./http-server.js";
import { gatewayContainerIngressOptions } from "./container-ingress.js";
import { gatewayMetadata } from "./metadata.js";
import {
  EVIDENCE_READINESS_INTEGRITY_FAILURE_MESSAGE,
} from "./readiness-integrity.js";
import {
  assessGovernedCandidateReadiness,
  governedCandidateAssemblyBindings,
  type GovernedCandidateAssembly,
} from "./governed-assembly.js";

export const GATEWAY_CONTAINER_HOST = "0.0.0.0" as const;
export const GATEWAY_CONTAINER_PORT = 8_787 as const;
export const GATEWAY_CONTAINER_CATALOGUE_ROOT = "/app/artifacts/okf" as const;
export const GATEWAY_CONTAINER_LEDGER_ROOT = "/var/lib/gis-ai-go/ledger" as const;
export const GATEWAY_CONTAINER_RECONCILIATION_ROOT =
  "/var/lib/gis-ai-go/reconciliation" as const;
export const GATEWAY_CONTAINER_APPROVED_CACHE_PATH =
  "/app/providers/ons/data-query-approved-cache.v1.json" as const;
export const GATEWAY_CONTAINER_APPROVED_CACHE_BYTES = 3_066 as const;
export const GATEWAY_CONTAINER_APPROVED_CACHE_SHA256 =
  "4b60e567d700d64ba98b87001e7adb10e25b2342403040b4a996d373b2714b8c" as const;

const START_EVENT = "gateway_started";
const STOP_EVENT = "gateway_stopped";
const START_FAILURE_EVENT = "gateway_start_failed";
export const GATEWAY_CONTAINER_READINESS_INTEGRITY_FAILURE_EVENT =
  "gateway_readiness_integrity_failed" as const;
export const GATEWAY_CONTAINER_REQUEST_FAILURE_EVENT =
  "gateway_request_failed" as const;

/** Map every operational error to a fixed path-free lifecycle event name. */
export function gatewayContainerErrorEvent(
  error: Error,
):
  | typeof GATEWAY_CONTAINER_READINESS_INTEGRITY_FAILURE_EVENT
  | typeof GATEWAY_CONTAINER_REQUEST_FAILURE_EVENT {
  return error.message === EVIDENCE_READINESS_INTEGRITY_FAILURE_MESSAGE
    ? GATEWAY_CONTAINER_READINESS_INTEGRITY_FAILURE_EVENT
    : GATEWAY_CONTAINER_REQUEST_FAILURE_EVENT;
}

function writeLifecycleEvent(event: string, revision?: string): void {
  process.stdout.write(
    `${JSON.stringify({
      event,
      lifecycle: CANDIDATE_ACTIVATION_LIFECYCLE,
      production_registration: false,
      ...(revision === undefined ? {} : { revision }),
    })}\n`,
  );
}

/** Fail closed unless the fixed image assembly is the exact unregistered five. */
export function assertCandidateContainerAuthority(
  assembly: GovernedCandidateAssembly,
): void {
  governedCandidateAssemblyBindings(assembly);
  const readiness = assessGovernedCandidateReadiness(assembly);
  if (
    // Generic constructors and non-container entrypoints remain blocked.
    catalogueActivation.state !== "blocked" ||
    catalogueActivation.activeTools.length !== 0 ||
    catalogueActivation.activeApiOperations.length !== 0 ||
    gatewayMetadata.lifecycle !== "candidate-blocked" ||
    gatewayMetadata.liveProviderCalls !== false ||
    gatewayMetadata.activeTools.length !== 0 ||
    gatewayMetadata.activeApiOperations.length !== 0 ||
    assembly.state !== CANDIDATE_ACTIVATION_LIFECYCLE ||
    assembly.productionRegistration !== false ||
    assembly.suspensions.length !== 0 ||
    assembly.operations.length !== CANDIDATE_ACTIVATION_OPERATIONS.length ||
    assembly.operations.some(
      (operation, index) => operation !== CANDIDATE_ACTIVATION_OPERATIONS[index],
    ) ||
    assembly.apiOperations !== assembly.operations ||
    assembly.mcpOperations !== assembly.operations ||
    assembly.mcpResources.length !== CANDIDATE_ACTIVATION_RESOURCES.length ||
    assembly.mcpResources.some(
      (resource, index) => resource !== CANDIDATE_ACTIVATION_RESOURCES[index],
    ) ||
    !(
      (readiness.status === "ready" &&
        readiness.reason === "candidate-assembly-verified") ||
      (readiness.status === "blocked" &&
        readiness.reason === "reconciliation-capacity-exhausted")
    ) ||
    readiness.productionRegistration !== false ||
    readiness.activeTools !== assembly.operations ||
    readiness.activeApiOperations !== assembly.operations
  ) {
    throw new Error("The gateway container candidate authority is invalid");
  }
}

/** The container entry point has no command-line configuration or activation seam. */
export function assertFixedContainerArguments(argv: readonly string[]): void {
  if (argv.length !== 2) {
    throw new Error("The gateway container does not accept arguments");
  }
}

function listen(server: GatewayNodeServer): Promise<void> {
  return new Promise((resolveListen, reject) => {
    const onError = (error: Error): void => reject(error);
    server.once("error", onError);
    server.listen(GATEWAY_CONTAINER_PORT, GATEWAY_CONTAINER_HOST, () => {
      server.removeListener("error", onError);
      resolveListen();
    });
  });
}

function loadFixedApprovedCacheRecord(): ApprovedOnsDataQueryCacheRecord {
  const metadata = lstatSync(GATEWAY_CONTAINER_APPROVED_CACHE_PATH);
  if (
    !metadata.isFile() ||
    metadata.size !== GATEWAY_CONTAINER_APPROVED_CACHE_BYTES
  ) {
    throw new Error("The fixed approved ONS cache record is unavailable");
  }
  const bytes = readFileSync(GATEWAY_CONTAINER_APPROVED_CACHE_PATH);
  if (
    bytes.byteLength !== GATEWAY_CONTAINER_APPROVED_CACHE_BYTES ||
    createHash("sha256").update(bytes).digest("hex") !==
      GATEWAY_CONTAINER_APPROVED_CACHE_SHA256
  ) {
    throw new Error("The fixed approved ONS cache record failed byte verification");
  }
  const record = parseStrictJson(
    new TextDecoder("utf-8", { fatal: true }).decode(bytes),
  );
  // Validate the exact content address, query, source, rights, approval, coverage
  // and freshness contract before handing the detached record to the closed builder.
  createApprovedOnsDataQueryCache(record);
  return record as ApprovedOnsDataQueryCacheRecord;
}

/**
 * Start the repository-only, local and unregistered exact-five candidate.
 */
export async function runGatewayContainerMain(): Promise<void> {
  assertFixedContainerArguments(process.argv);
  const ingress = gatewayContainerIngressOptions(process.env);

  const snapshot = await loadCatalogueSnapshot(resolve(GATEWAY_CONTAINER_CATALOGUE_ROOT));
  const ledger = PublicEvidenceLedger.open({
    rootDirectory: GATEWAY_CONTAINER_LEDGER_ROOT,
  });
  ledger.verify();
  const reconciliationIndex = PublicEvidenceReconciliationIndex.open({
    rootDirectory: GATEWAY_CONTAINER_RECONCILIATION_ROOT,
    ledger,
  });
  reconciliationIndex.verify();
  const approvedCacheRecord = loadFixedApprovedCacheRecord();
  const assembly = createCandidateActivation(
    snapshot,
    ledger,
    reconciliationIndex,
    approvedCacheRecord,
  );
  assertCandidateContainerAuthority(assembly);

  const server = createGovernedCandidateNodeServer(assembly, {
    ...ingress,
    onerror: (error) => writeLifecycleEvent(
      gatewayContainerErrorEvent(error),
      snapshot.revision,
    ),
  });
  await listen(server);
  writeLifecycleEvent(START_EVENT, snapshot.revision);

  let stopping = false;
  const stop = (): void => {
    if (stopping) return;
    stopping = true;
    void server.closeGateway().then(
      () => writeLifecycleEvent(STOP_EVENT, snapshot.revision),
      () => {
        process.exitCode = 1;
      },
    );
  };
  process.once("SIGINT", stop);
  process.once("SIGTERM", stop);
}

const entryPath = process.argv[1];
if (entryPath !== undefined && pathToFileURL(resolve(entryPath)).href === import.meta.url) {
  await runGatewayContainerMain().catch(() => {
    writeLifecycleEvent(START_FAILURE_EVENT);
    process.exitCode = 1;
  });
}
