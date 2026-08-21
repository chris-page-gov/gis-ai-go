import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

import {
  PublicEvidenceLedger,
  PublicEvidenceReconciliationIndex,
} from "@gis-ai-go/evidence";

import { catalogueActivation } from "./activation.js";
import { loadCatalogueSnapshot } from "./catalogue-snapshot.js";
import { createGatewayNodeServer, type GatewayNodeServer } from "./http-server.js";
import { gatewayMetadata } from "./metadata.js";

export const GATEWAY_CONTAINER_HOST = "0.0.0.0" as const;
export const GATEWAY_CONTAINER_PORT = 8_787 as const;
export const GATEWAY_CONTAINER_CATALOGUE_ROOT = "/app/artifacts/okf" as const;
export const GATEWAY_CONTAINER_LEDGER_ROOT = "/var/lib/gis-ai-go/ledger" as const;
export const GATEWAY_CONTAINER_RECONCILIATION_ROOT =
  "/var/lib/gis-ai-go/reconciliation" as const;

const START_EVENT = "gateway_started";
const STOP_EVENT = "gateway_stopped";
const START_FAILURE_EVENT = "gateway_start_failed";

function writeLifecycleEvent(event: string, revision?: string): void {
  process.stdout.write(
    `${JSON.stringify({
      event,
      lifecycle: gatewayMetadata.lifecycle,
      ...(revision === undefined ? {} : { revision }),
    })}\n`,
  );
}

/** Fail closed if the reviewed production authority has changed beneath this image. */
export function assertBlockedContainerAuthority(): void {
  if (
    catalogueActivation.state !== "blocked" ||
    catalogueActivation.activeTools.length !== 0 ||
    catalogueActivation.activeApiOperations.length !== 0 ||
    gatewayMetadata.lifecycle !== "candidate-blocked" ||
    gatewayMetadata.liveProviderCalls !== false ||
    gatewayMetadata.activeTools.length !== 0 ||
    gatewayMetadata.activeApiOperations.length !== 0
  ) {
    throw new Error("The gateway container authority is not blocked");
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

/**
 * Start the repository-only blocked candidate.
 *
 * The ledger and reconciliation index are opened only to verify the fixed durable
 * volume boundary. They are deliberately not supplied to an application because
 * this entry point mounts no operation, resource, provider or application.
 */
export async function runGatewayContainerMain(): Promise<void> {
  assertFixedContainerArguments(process.argv);
  assertBlockedContainerAuthority();

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

  // Omission of every explicit seam is the reviewed zero-capability production path.
  const server = createGatewayNodeServer(snapshot);
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
