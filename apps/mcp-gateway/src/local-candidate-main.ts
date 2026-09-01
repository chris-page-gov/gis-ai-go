import { createHash } from "node:crypto";
import {
  chmodSync,
  lstatSync,
  mkdtempSync,
  readFileSync,
  realpathSync,
  rmSync,
  statSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

import {
  PublicEvidenceLedger,
  PublicEvidenceReconciliationIndex,
} from "@gis-ai-go/evidence";
import {
  ONS_EGRESS_POLICY,
  ONS_OBSERVATION_URI,
  createApprovedOnsDataQueryCache,
  createOnsDataApiAdapter,
  parseStrictJson,
  type ApprovedOnsDataQueryCacheRecord,
  type FixedHttpsResponse,
} from "@gis-ai-go/provider-adapter-sdk";

import type { CatalogueSnapshot } from "./catalogue-snapshot.js";
import { loadCatalogueSnapshot } from "./catalogue-snapshot.js";
import {
  CANDIDATE_ACTIVATION_LIFECYCLE,
  CANDIDATE_ACTIVATION_PROVIDER_REASON,
} from "./candidate-activation.js";
import {
  GATEWAY_CONTAINER_APPROVED_CACHE_BYTES,
  GATEWAY_CONTAINER_APPROVED_CACHE_SHA256,
  assertCandidateContainerAuthority,
} from "./container-main.js";
import {
  createGovernedCandidateAssembly,
  type GovernedCandidateAssembly,
} from "./governed-assembly.js";
import {
  createGovernedCandidateNodeServer,
  type GatewayNodeServer,
} from "./http-server.js";
import { gatewayMetadata } from "./metadata.js";

export const LOCAL_CANDIDATE_HOST = "127.0.0.1" as const;
export const LOCAL_CANDIDATE_PORT = 8_787 as const;
export const LOCAL_CANDIDATE_TARGET_RELEASE = "0.2.0" as const;
export const LOCAL_CANDIDATE_LIFECYCLE_SCHEMA =
  "gis-ai-go.local-candidate-lifecycle.v1" as const;
export const LOCAL_CANDIDATE_STATE_ROOT_MODE = 0o700 as const;
export const LOCAL_CANDIDATE_PROVIDER_OBSERVATION =
  "deterministic-in-memory-http-503" as const;
export const LOCAL_CANDIDATE_DATA_QUERY_SOURCE =
  "byte-verified-approved-cache" as const;

const LOCAL_CANDIDATE_ENDPOINT =
  `http://${LOCAL_CANDIDATE_HOST}:${LOCAL_CANDIDATE_PORT}/mcp` as const;
const LOCAL_CANDIDATE_ORIGIN =
  `http://${LOCAL_CANDIDATE_HOST}:${LOCAL_CANDIDATE_PORT}` as const;
const LOCAL_CANDIDATE_AUTHORITY =
  `${LOCAL_CANDIDATE_HOST}:${LOCAL_CANDIDATE_PORT}` as const;
const LOCAL_CANDIDATE_PROVIDER_REASON =
  `${CANDIDATE_ACTIVATION_PROVIDER_REASON} ` +
  "The provider-free local runner uses only its deterministic outage and approved cache.";
const LOCAL_CANDIDATE_CATALOGUE_ROOT = fileURLToPath(
  new URL("../../../../artifacts/okf/", import.meta.url),
);
const LOCAL_CANDIDATE_APPROVED_CACHE_PATH = fileURLToPath(
  new URL(
    "../../../../providers/ons/data-query-approved-cache.v1.json",
    import.meta.url,
  ),
);
const LOCAL_CANDIDATE_PROVIDER_TRANSPORT_ATTEMPTS = new WeakMap<
  object,
  () => number
>();

export type LocalCandidateLifecycleEvent =
  | "local_candidate_started"
  | "local_candidate_stopped"
  | "local_candidate_start_failed"
  | "local_candidate_cleanup_failed"
  | "local_candidate_request_failed";

export function localCandidateLifecycleRecord(
  event: LocalCandidateLifecycleEvent,
  revision?: string,
): Readonly<Record<string, unknown>> {
  return Object.freeze({
    schema: LOCAL_CANDIDATE_LIFECYCLE_SCHEMA,
    event,
    endpoint: LOCAL_CANDIDATE_ENDPOINT,
    software_version: gatewayMetadata.version,
    target_release: LOCAL_CANDIDATE_TARGET_RELEASE,
    lifecycle: CANDIDATE_ACTIVATION_LIFECYCLE,
    production_registration: false,
    provider_egress: false,
    provider_observation: LOCAL_CANDIDATE_PROVIDER_OBSERVATION,
    data_query_source: LOCAL_CANDIDATE_DATA_QUERY_SOURCE,
    ...(revision === undefined ? {} : { revision }),
  });
}

function writeLifecycleEvent(
  event: LocalCandidateLifecycleEvent,
  revision?: string,
): void {
  process.stdout.write(
    `${JSON.stringify(localCandidateLifecycleRecord(event, revision))}\n`,
  );
}

/** Reject every command-line option so the local runner cannot become an activation seam. */
export function assertFixedLocalCandidateArguments(argv: readonly string[]): void {
  if (argv.length !== 2) {
    throw new Error("The provider-free local candidate does not accept arguments");
  }
}

function loadApprovedCacheRecord(): ApprovedOnsDataQueryCacheRecord {
  const metadata = lstatSync(LOCAL_CANDIDATE_APPROVED_CACHE_PATH);
  if (
    !metadata.isFile() ||
    metadata.size !== GATEWAY_CONTAINER_APPROVED_CACHE_BYTES
  ) {
    throw new Error("The provider-free local candidate cache is unavailable");
  }
  const bytes = readFileSync(LOCAL_CANDIDATE_APPROVED_CACHE_PATH);
  if (
    bytes.byteLength !== GATEWAY_CONTAINER_APPROVED_CACHE_BYTES ||
    createHash("sha256").update(bytes).digest("hex") !==
      GATEWAY_CONTAINER_APPROVED_CACHE_SHA256
  ) {
    throw new Error("The provider-free local candidate cache failed verification");
  }
  const record = parseStrictJson(
    new TextDecoder("utf-8", { fatal: true }).decode(bytes),
  );
  createApprovedOnsDataQueryCache(record);
  return record as ApprovedOnsDataQueryCacheRecord;
}

function deterministicProviderOutage(): FixedHttpsResponse {
  const body = Buffer.from(
    JSON.stringify({ status: "provider-free-local-candidate-outage" }),
    "utf8",
  );
  return Object.freeze({
    status: 503,
    headers: Object.freeze({
      "content-type": "application/json",
      "retry-after": "6",
    }),
    body,
    telemetry: Object.freeze({
      dnsMs: 0,
      resolvedAddressCount: 0,
      selectedAddressFamily: 4,
      connectMs: 0,
      responseMs: 0,
      totalMs: 0,
      compressedBytes: body.byteLength,
      tlsProtocol: null,
      tlsCipher: null,
    }),
  });
}

/**
 * Build the exact-five local candidate over the exact approved-cache fallback.
 *
 * The adapter transport validates its fixed request and returns one deterministic
 * in-memory 503. The governed application then labels and receipts its use of the
 * byte-verified approved cache. There is no DNS, socket, HTTPS, fetch or credential
 * seam, so provider egress is impossible.
 */
export function createProviderFreeLocalCandidateAssembly(
  snapshot: CatalogueSnapshot,
  evidenceLedger: PublicEvidenceLedger,
  reconciliationIndex: PublicEvidenceReconciliationIndex,
  approvedCacheRecord: ApprovedOnsDataQueryCacheRecord,
): GovernedCandidateAssembly {
  if (arguments.length !== 4) {
    throw new TypeError(
      "Provider-free local candidate assembly requires the exact fixed input tuple",
    );
  }
  const approvedCache = createApprovedOnsDataQueryCache(approvedCacheRecord);
  let providerTransportAttempts = 0;
  const adapter = createOnsDataApiAdapter({
    lifecycle: Object.freeze({
      discovery: "active",
      invocation: "active",
      reason: LOCAL_CANDIDATE_PROVIDER_REASON,
    }),
    sleep: async () => {
      throw new TypeError(
        "The provider-free local request attempted a provider retry",
      );
    },
    transport: async ({ policy, url, signal }) => {
      providerTransportAttempts += 1;
      if (
        policy !== ONS_EGRESS_POLICY ||
        url !== ONS_OBSERVATION_URI ||
        !(signal instanceof AbortSignal)
      ) {
        throw new TypeError(
          "The provider-free local request escaped its fixed contract",
        );
      }
      return deterministicProviderOutage();
    },
  });
  const assembly = createGovernedCandidateAssembly({
    snapshot,
    evidenceLedger,
    reconciliationIndex,
    adapter,
    approvedCache,
  });
  assertCandidateContainerAuthority(assembly);
  LOCAL_CANDIDATE_PROVIDER_TRANSPORT_ATTEMPTS.set(
    assembly,
    () => providerTransportAttempts,
  );
  return assembly;
}

/** Read the transport-attempt count for a genuine local-candidate assembly. */
export function localCandidateProviderTransportAttemptCount(
  assembly: GovernedCandidateAssembly,
): number {
  const count = LOCAL_CANDIDATE_PROVIDER_TRANSPORT_ATTEMPTS.get(assembly);
  if (count === undefined) {
    throw new TypeError("Local candidate assembly transport evidence is unavailable");
  }
  return count();
}

function createPrivateStateRoot(): string {
  const root = mkdtempSync(
    join(realpathSync(tmpdir()), "gis-ai-go-local-candidate-"),
  );
  chmodSync(root, LOCAL_CANDIDATE_STATE_ROOT_MODE);
  if ((statSync(root).mode & 0o777) !== LOCAL_CANDIDATE_STATE_ROOT_MODE) {
    rmSync(root, { recursive: true, force: true });
    throw new Error("The provider-free local candidate state root is not private");
  }
  return root;
}

type RemoveStateRoot = (stateRoot: string) => void;

/**
 * Return an idempotent cleanup that records completion only after deletion.
 * A failed attempt can therefore be retried by the process exit hook.
 */
export function createRetryableLocalCandidateStateCleanup(
  stateRoot: string,
  removeStateRoot: RemoveStateRoot,
): () => void {
  let removed = false;
  return (): void => {
    if (removed) return;
    removeStateRoot(stateRoot);
    removed = true;
  };
}

function listen(server: GatewayNodeServer): Promise<void> {
  return new Promise((resolveListen, reject) => {
    const onError = (error: Error): void => reject(error);
    server.once("error", onError);
    server.listen(LOCAL_CANDIDATE_PORT, LOCAL_CANDIDATE_HOST, () => {
      server.removeListener("error", onError);
      resolveListen();
    });
  });
}

/** Start the persistent, loopback-only provider-free v0.2.0 local candidate. */
export async function runProviderFreeLocalCandidateMain(): Promise<void> {
  assertFixedLocalCandidateArguments(process.argv);
  const stateRoot = createPrivateStateRoot();
  const removeState = createRetryableLocalCandidateStateCleanup(
    stateRoot,
    (root) => rmSync(root, { recursive: true, force: true }),
  );
  const reportCleanupFailure = (revision?: string): void => {
    process.exitCode = 1;
    try {
      writeLifecycleEvent("local_candidate_cleanup_failed", revision);
    } catch {
      // Keep the original startup or shutdown failure authoritative.
    }
  };
  const removeStateOnExit = (): void => {
    try {
      removeState();
    } catch {
      process.exitCode = 1;
    }
  };
  process.once("exit", removeStateOnExit);

  let server: GatewayNodeServer | undefined;
  try {
    const snapshot = await loadCatalogueSnapshot(LOCAL_CANDIDATE_CATALOGUE_ROOT);
    const ledger = PublicEvidenceLedger.open({
      rootDirectory: join(stateRoot, "ledger"),
    });
    ledger.verify();
    const reconciliationIndex = PublicEvidenceReconciliationIndex.open({
      rootDirectory: join(stateRoot, "reconciliation"),
      ledger,
    });
    reconciliationIndex.verify();
    const assembly = createProviderFreeLocalCandidateAssembly(
      snapshot,
      ledger,
      reconciliationIndex,
      loadApprovedCacheRecord(),
    );
    server = createGovernedCandidateNodeServer(assembly, {
      directAllowedHosts: Object.freeze([LOCAL_CANDIDATE_AUTHORITY]),
      directAllowedOrigins: Object.freeze([LOCAL_CANDIDATE_ORIGIN]),
      mcpAllowedHosts: Object.freeze([LOCAL_CANDIDATE_AUTHORITY]),
      mcpAllowedHostnames: Object.freeze([LOCAL_CANDIDATE_HOST]),
      mcpAllowedOrigins: Object.freeze([LOCAL_CANDIDATE_ORIGIN]),
      onerror: () => writeLifecycleEvent(
        "local_candidate_request_failed",
        snapshot.revision,
      ),
    });
    await listen(server);
    writeLifecycleEvent("local_candidate_started", snapshot.revision);

    let stopping = false;
    const stop = (): void => {
      if (stopping) return;
      stopping = true;
      void server?.closeGateway().then(
        () => {
          try {
            removeState();
            writeLifecycleEvent("local_candidate_stopped", snapshot.revision);
          } catch {
            reportCleanupFailure(snapshot.revision);
          }
        },
        () => {
          try {
            removeState();
          } catch {
            reportCleanupFailure(snapshot.revision);
          }
          process.exitCode = 1;
        },
      );
    };
    process.once("SIGINT", stop);
    process.once("SIGTERM", stop);
  } catch (error) {
    if (server !== undefined) await server.closeGateway().catch(() => undefined);
    try {
      removeState();
    } catch {
      reportCleanupFailure();
    }
    throw error;
  }
}

const entryPath = process.argv[1];
if (
  entryPath !== undefined &&
  pathToFileURL(resolve(entryPath)).href === import.meta.url
) {
  await runProviderFreeLocalCandidateMain().catch(() => {
    writeLifecycleEvent("local_candidate_start_failed");
    process.exitCode = 1;
  });
}
