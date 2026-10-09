/** Private-pilot entrypoint, distinct from deliberately blocked generic production and loopback editions. */
import { createHash } from "node:crypto";
import { lstatSync, readFileSync, realpathSync } from "node:fs";
import { dirname, join, resolve, sep } from "node:path";
import { pathToFileURL } from "node:url";
import { canonicalJson } from "@gis-ai-go/evidence/web216-pure";
import { createGcpFirestoreRestStore } from "./gcp-firestore.js";
import { createGcpKnowledgeService, type GcpKnowledgeBundle } from "./gcp-knowledge.js";
import { createGcpServer, type GcpReleaseAsset, type GcpRuntimeConfig } from "./gcp-server.js";
import { createGcpJwtVerifier, createGcpIdentityAdapter } from "./gcp-identity.js";
import { createGcpEvidenceSeed } from "./gcp-application.js";
import { parseBoundedJsonBytes } from "./bounded-json.js";

const sha256 = (bytes: Uint8Array | string) => createHash("sha256").update(bytes).digest("hex");
export interface GcpReleaseFile { readonly path: string; readonly bytes: number; readonly sha256: string }
export interface GcpReleaseManifest {
  readonly schema: "gis-ai-go.gcp-release.v1"; readonly source_revision: string; readonly release_sha256: string;
  readonly files: readonly GcpReleaseFile[];
  readonly bundles: readonly { readonly id: "okf" | "okf-plus"; readonly path: string; readonly record_count: number; readonly source_lock_sha256: string; readonly input_digest?: string }[];
}
function safePath(root: string, relative: string) {
  if (!relative || /[\\\x00-\x1f\x7f:]/u.test(relative) || relative.startsWith("/") ||
      relative.split("/").some((part) => !part || part === "." || part === "..")) throw Error("Unsafe release path");
  let path = root;
  for (const part of relative.split("/")) { path = join(path, part); if (lstatSync(path).isSymbolicLink()) throw Error("Symlink release path"); }
  const resolved = realpathSync(path);
  if (!resolved.startsWith(root + sep) || !lstatSync(path).isFile()) throw Error("Invalid release file");
  return path;
}
export function readGcpRuntimeConfig(root = "/app", env: Readonly<Record<string, string | undefined>> = process.env): GcpRuntimeConfig | null {
  const raw = env.GCP_RUNTIME_CONFIG_JSON ?? readFileSync(env.GCP_RUNTIME_CONFIG ?? join(root, "runtime-config.json"), "utf8");
  const value = parseBoundedJsonBytes(Buffer.from(raw), 65_536) as GcpRuntimeConfig;
  if (value?.schema !== "gis-ai-go.gcp-runtime.v1" || !["personal", "bduk"].includes(value.profile)) throw Error("Invalid private runtime configuration");
  const merged = { ...value,
    ...(env.GCP_TRANSPORT_SUBJECT ? { transportSubject: env.GCP_TRANSPORT_SUBJECT } : {}),
    ...(env.GCP_TRANSPORT_AUDIENCE ? { transportAudience: env.GCP_TRANSPORT_AUDIENCE } : {}),
  };
  // A first, explicitly planned bootstrap revision is process-healthy and denies all application content.
  // Missing identity or stable state settings never select a mock or developer identity.
  if (!merged.publicOrigin || !merged.transportSubject || !merged.firestore?.projectId || !merged.firestore.databaseId ||
      !merged.firestore.collection || !merged.evidence || !merged.identity ||
      (merged.identity.mode === "oidc" && (!merged.identity.issuer || !merged.identity.audience || !merged.identity.jwksUri))) return null;
  if (!Array.isArray(merged.allowedOrigins) || !/^https:\/\//u.test(merged.transportAudience ?? merged.publicOrigin)) throw Error("Invalid private audience configuration");
  createGcpIdentityAdapter(merged, createGcpJwtVerifier());
  // Validate provisioned descriptor material during release loading with the real capture.
  return Object.freeze(merged);
}
function contentType(path: string) {
  return path.endsWith(".html") ? "text/html; charset=utf-8" : path.endsWith(".js") || path.endsWith(".mjs") ? "text/javascript; charset=utf-8"
    : path.endsWith(".css") ? "text/css; charset=utf-8" : path.endsWith(".svg") ? "image/svg+xml" : path.endsWith(".png") ? "image/png"
      : path.endsWith(".woff2") ? "font/woff2" : path.endsWith(".json") || path.endsWith(".jsonld") ? "application/json; charset=utf-8"
        : path.endsWith(".md") || path.endsWith(".txt") ? "text/plain; charset=utf-8" : "application/octet-stream";
}
/** Verify the entire generated allowlist before serving any content. Never look up an arbitrary request path. */
export function loadGcpRelease(directory = "/app") {
  const root = realpathSync(directory);
  const manifest = JSON.parse(readFileSync(safePath(root, "release-manifest.json"), "utf8")) as GcpReleaseManifest;
  if (manifest.schema !== "gis-ai-go.gcp-release.v1" || !/^[0-9a-f]{40}$/u.test(manifest.source_revision) ||
      !/^[0-9a-f]{64}$/u.test(manifest.release_sha256) || !Array.isArray(manifest.files) || manifest.files.length < 1 || manifest.files.length > 100_000 ||
      !Array.isArray(manifest.bundles) || manifest.bundles.length !== 2) throw Error("Invalid private release manifest");
  const paths = new Set<string>(); const assets = new Map<string, GcpReleaseAsset>();
  for (const file of manifest.files) {
    if (paths.has(file.path) || !Number.isSafeInteger(file.bytes) || file.bytes < 0 || !/^[0-9a-f]{64}$/u.test(file.sha256)) throw Error("Invalid release inventory");
    paths.add(file.path);
    const bytes = readFileSync(safePath(root, file.path));
    if (bytes.length !== file.bytes || sha256(bytes) !== file.sha256) throw Error("Release bytes differ from admitted inventory");
    if (file.path.startsWith("static/")) {
      // Explorer's local copy of the catalogue is still an authorised knowledge route.
      const kind = /\/(?:okf|data)\//u.test(file.path) || /\.(?:json|jsonld|md)$/u.test(file.path) ? "knowledge" : "website";
      const route = "/" + file.path.slice("static/".length);
      const asset = { bytes, contentType: contentType(file.path), kind } as const;
      assets.set(route, asset);
      if (route.endsWith("/index.html")) {
        const short = route.slice(0, -"/index.html".length); assets.set(short, asset); assets.set(short + "/", asset);
      }
    }
    // Whole corpus downloads require the separate export grant, even when the source is public metadata.
    if (/^bundles\/(?:okf|okf-plus|okf-plus-context)\//u.test(file.path)) {
      const path = safePath(root, file.path); const stat = lstatSync(path);
      assets.set("/exports/" + file.path, { filePath: path, size: stat.size, sha256: file.sha256, inode: stat.ino,
        mtimeMs: stat.mtimeMs, contentType: contentType(file.path), kind: "export" });
    }
  }
  const rootDigest = sha256(manifest.files.map((file) => `${file.sha256} ${file.bytes} ${file.path}\n`).sort().join(""));
  if (rootDigest !== manifest.release_sha256) throw Error("Release root differs from its pinned inventory");
  const bundles: GcpKnowledgeBundle[] = [];
  for (const declared of manifest.bundles) {
    const path = declared.path + "/okf-bundle.json";
    if (!paths.has(path)) throw Error("Required OKF bundle is outside the admitted release");
    const body = JSON.parse(readFileSync(safePath(root, path), "utf8")) as Record<string, unknown>;
    if (body.revision !== manifest.source_revision || !Array.isArray(body.records) || body.records.length !== declared.record_count ||
        (declared.id === "okf" && (body.schema !== "gis-ai-go-okf-bundle.v1" || declared.record_count !== 36)) ||
        (declared.id === "okf-plus" && (body.schema !== "gis-ai-go.okf-plus-bundle.v1" || declared.record_count !== 30_833))) throw Error("Knowledge release identity/count differs from its admitted build");
    bundles.push({ id: declared.id, revision: body.revision as string, inputDigest: declared.input_digest ?? declared.source_lock_sha256,
      records: body.records as Record<string, unknown>[] });
  }
  const projectionPath = "bundles/cpih-projection.json";
  if (!paths.has(projectionPath)) throw Error("Captured CPIH is missing from admitted inventory");
  const projection: unknown = JSON.parse(readFileSync(safePath(root, projectionPath), "utf8"));
  return { manifest, assets, projection, knowledge: createGcpKnowledgeService(bundles, manifest.release_sha256) };
}
export async function runGcpMain() {
  if (process.argv.length !== 2) throw Error("The private runtime accepts no CLI arguments");
  const root = process.env.GCP_APP_ROOT ?? "/app";
  const release = loadGcpRelease(root); const config = readGcpRuntimeConfig(root);
  if (config) createGcpEvidenceSeed({ projection: release.projection, evidence: config.evidence, principalScope: "1".repeat(64) });
  const rawPort = process.env.PORT ?? "8080";
  if (!/^[1-9]\d{0,4}$/u.test(rawPort) || Number(rawPort) > 65_535) throw Error("Invalid Cloud Run port");
  const backend = config ? createGcpFirestoreRestStore(config.firestore) : {
    read: async () => { throw Error("Unbound runtime"); }, compareAndSet: async () => { throw Error("Unbound runtime"); },
  };
  const server = createGcpServer({ config, projection: release.projection, knowledge: release.knowledge, assets: release.assets, backend,
    ...(process.env.GCP_BROWSER_SESSION_KEY ? { browserSecrets: { sessionKey: process.env.GCP_BROWSER_SESSION_KEY,
      ...(process.env.GCP_OIDC_CLIENT_SECRET ? { clientSecret: process.env.GCP_OIDC_CLIENT_SECRET } : {}),
    } } : {}),
  });
  await new Promise<void>((resolveListen, reject) => {
    server.once("error", reject); server.listen(Number(rawPort), "0.0.0.0", () => { server.removeListener("error", reject); resolveListen(); });
  });
  process.stdout.write(canonicalJson({ schema: "gis-ai-go.gcp-runtime-lifecycle.v1", event: "started", port: Number(rawPort),
    release_sha256: release.manifest.release_sha256, source_revision: release.manifest.source_revision,
    identity: config?.identity.mode ?? "blocked-runtime-binding", provider_egress: false, external_model_calls: false,
    hosted_acceptance: "not-established-by-startup", supported_release_activation: false }) + "\n");
  let stopping = false;
  const stop = () => { if (stopping) return; stopping = true;
    void server.closePrivateRuntime().catch(() => { process.exitCode = 1; }).finally(() => {
      process.removeListener("SIGTERM", stop); process.removeListener("SIGINT", stop);
      process.stdout.write(canonicalJson({ schema: "gis-ai-go.gcp-runtime-lifecycle.v1", event: "stopped" }) + "\n");
    });
  };
  process.once("SIGTERM", stop); process.once("SIGINT", stop);
}
const entry = process.argv[1];
if (entry && pathToFileURL(resolve(entry)).href === import.meta.url) await runGcpMain().catch(() => {
  process.stderr.write('{"schema":"gis-ai-go.gcp-runtime-lifecycle.v1","event":"failed"}\n'); process.exitCode = 1;
});
