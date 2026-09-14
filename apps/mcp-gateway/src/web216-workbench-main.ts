/** Explicit provider-free workbench launcher, separate from every existing entrypoint. */
import { execFileSync } from "node:child_process";
import { closeSync, constants, fstatSync, fsyncSync, lstatSync, mkdirSync, openSync, readSync, readdirSync, realpathSync, writeSync } from "node:fs";
import { homedir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import {
  canonicalJson, openPublicEvidenceLedger, openWeb216CpihReconciliationIndex,
  WEB216_CPIH_CAPTURE, type EvidenceSoftwareIdentity,
} from "@gis-ai-go/evidence";
import { parseBoundedJsonBytes } from "./http-app.js";
import { createWeb216CpihApplication } from "./web216-cpih-application.js";
import { gatewayMetadata } from "./metadata.js";
import { createWeb216WorkbenchServer, WEB216_WORKBENCH_HOST, WEB216_WORKBENCH_PORT } from "./web216-workbench-server.js";

export const WEB216_WORKBENCH_ORIGIN = `http://${WEB216_WORKBENCH_HOST}:${WEB216_WORKBENCH_PORT}`;
const STORE_NAME = "web216-public-data-workbench-v1";
const repositoryRoot = fileURLToPath(new URL("../../../../", import.meta.url));
const publicDirectory = join(repositoryRoot, "apps", "public-data-workbench", "dist");
const projectionPath = join(repositoryRoot, "tests", "fixtures", "web216", "current-cpih-projection.json");

function directory(path: string, create: boolean): void {
  if (create) {
    try { mkdirSync(path, { mode: 0o700 }); }
    catch (error) { if ((error as NodeJS.ErrnoException).code !== "EEXIST") throw Error("Private workbench storage unavailable"); }
  }
  const stat = lstatSync(path);
  if (!stat.isDirectory() || stat.isSymbolicLink() || (stat.mode & 0o777) !== 0o700 ||
      (process.getuid !== undefined && stat.uid !== process.getuid())) throw Error("Private workbench directory failed validation");
}
function readJson(path: string, maximum: number, privateFile: boolean): unknown {
  const before = lstatSync(path);
  if (!before.isFile() || before.isSymbolicLink() || before.nlink !== 1 || before.size > maximum ||
      (privateFile && ((before.mode & 0o777) !== 0o600 || (process.getuid !== undefined && before.uid !== process.getuid())))) {
    throw Error("Workbench input failed validation");
  }
  const fd = openSync(path, constants.O_RDONLY | constants.O_NOFOLLOW);
  try {
    const opened = fstatSync(fd);
    if (opened.dev !== before.dev || opened.ino !== before.ino || opened.size !== before.size) throw Error("Workbench input changed");
    const buffer = Buffer.alloc(before.size + 1);
    let total = 0;
    while (total < buffer.length) {
      const count = readSync(fd, buffer, total, buffer.length - total, total);
      if (count === 0) break;
      total += count;
    }
    const after = fstatSync(fd);
    if (total !== before.size || after.size !== before.size || after.mtimeMs !== before.mtimeMs) throw Error("Workbench input changed");
    return parseBoundedJsonBytes(buffer.subarray(0, total), maximum);
  } finally { closeSync(fd); }
}
function persistIdentity(path: string, value: unknown): void {
  const fd = openSync(path, constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL | constants.O_NOFOLLOW, 0o600);
  try {
    const bytes = Buffer.from(canonicalJson(value));
    let count = 0;
    while (count < bytes.length) {
      const written = writeSync(fd, bytes, count, bytes.length - count);
      if (written < 1) throw Error("Workbench identity write did not complete");
      count += written;
    }
    fsyncSync(fd);
  } finally { closeSync(fd); }
}

/** Trusted embedding/test seam. The shipped CLI fixes the parent directory itself. */
export function openWeb216WorkbenchState(parentDirectory: string, projection: unknown, software: EvidenceSoftwareIdentity, now?: () => Date) {
  directory(parentDirectory, false);
  const root = join(realpathSync(parentDirectory), STORE_NAME);
  directory(root, true);
  const entries = readdirSync(root).sort();
  const fresh = entries.length === 0;
  if (!fresh && entries.join(",") !== "identity.json,ledger,reconciliation") throw Error("Workbench state is incomplete or unrecognised");
  // Verify the identity document before opening existing storage, so a missing or
  // substituted marker cannot turn an unrelated store into this workbench.
  const previous = fresh ? undefined : readJson(join(root, "identity.json"), 4_096, true);
  const ledger = openPublicEvidenceLedger({ rootDirectory: join(root, "ledger"), ...(now === undefined ? {} : { now }) });
  const reconciliationIndex = openWeb216CpihReconciliationIndex({ rootDirectory: join(root, "reconciliation"), ledger, ...(now === undefined ? {} : { now }) });
  const identity = {
    schema: "gis-ai-go.web216-workbench-store.v1", scope: "private-local-durable-captured-cpih",
    capture_projection_sha256: WEB216_CPIH_CAPTURE.projection_sha256,
    ledger_id: ledger.descriptor.ledger_id, index_id: reconciliationIndex.verify().index_id,
    provider_egress: false, attested: false,
  } as const;
  if (fresh) {
    persistIdentity(join(root, "identity.json"), identity);
    const fd = openSync(root, constants.O_RDONLY); try { fsyncSync(fd); } finally { closeSync(fd); }
  } else if (canonicalJson(previous) !== canonicalJson(identity)) throw Error("Workbench store identity mismatch");
  const application = createWeb216CpihApplication({ ledger, reconciliationIndex, projection, software, ...(now === undefined ? {} : { now }) });
  return Object.freeze({ application, ledger, reconciliationIndex, identity });
}

export function assertWeb216WorkbenchArguments(argv: readonly string[]): void {
  if (argv.length !== 2) throw Error("The local public-data workbench accepts no arguments");
}
export function web216WorkbenchLifecycle(event: "started" | "stopped" | "failed", revision?: string, staticContentSha256?: string) {
  return Object.freeze({
    schema: "gis-ai-go.web216-workbench-lifecycle.v1", event, origin: WEB216_WORKBENCH_ORIGIN,
    mcp_endpoint: `${WEB216_WORKBENCH_ORIGIN}/mcp`, provider_egress: false,
    activated_supported_release: false, storage: "private-local-durable-retained-after-shutdown",
    runtime_build_attestation: "not-attested", source_revision_scope: "checkout-HEAD-not-a-clean-build-attestation",
    ...(revision === undefined ? {} : { revision }),
    ...(staticContentSha256 === undefined ? {} : { static_content_sha256: staticContentSha256 }),
  });
}
function output(event: Parameters<typeof web216WorkbenchLifecycle>[0], revision?: string, staticContentSha256?: string) {
  process.stdout.write(`${JSON.stringify(web216WorkbenchLifecycle(event, revision, staticContentSha256))}\n`);
}

export async function runWeb216WorkbenchMain(): Promise<void> {
  assertWeb216WorkbenchArguments(process.argv);
  const revision = execFileSync("git", ["-C", repositoryRoot, "rev-parse", "--verify", "HEAD"], { encoding: "utf8", timeout: 2_000, stdio: ["ignore", "pipe", "ignore"] }).trim();
  if (!/^[0-9a-f]{40}$/u.test(revision)) throw Error("Workbench source revision unavailable");
  const privateParent = join(realpathSync(homedir()), ".gis-ai-go");
  directory(privateParent, true);
  const state = openWeb216WorkbenchState(privateParent, readJson(projectionPath, 16_384, false), {
    name: "gis-ai-go-mcp-gateway", version: gatewayMetadata.version, revision,
  });
  const server = createWeb216WorkbenchServer(state.application, publicDirectory);
  try {
    await new Promise<void>((resolveListen, reject) => {
      const error = (failure: Error) => reject(failure);
      server.once("error", error);
      server.listen(WEB216_WORKBENCH_PORT, WEB216_WORKBENCH_HOST, () => {
        server.removeListener("error", error); resolveListen();
      });
    });
  } catch (error) { await server.closeWorkbench(); throw error; }
  output("started", revision, server.assetSha256);
  let stopping = false;
  const stop = () => {
    if (stopping) return; stopping = true;
    void server.closeWorkbench().then(() => output("stopped", revision, server.assetSha256), () => {
      output("failed"); process.exitCode = 1;
    }).finally(() => { process.removeListener("SIGINT", stop); process.removeListener("SIGTERM", stop); });
  };
  process.once("SIGINT", stop); process.once("SIGTERM", stop);
}

const entry = process.argv[1];
if (entry !== undefined && pathToFileURL(resolve(entry)).href === import.meta.url) {
  await runWeb216WorkbenchMain().catch(() => { output("failed"); process.exitCode = 1; });
}
