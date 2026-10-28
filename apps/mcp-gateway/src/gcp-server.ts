/** Additive Cloud Run HTTP assembly. Existing local and blocked production launchers stay separate. */
import { createHash } from "node:crypto";
import { constants, createReadStream, lstatSync, openSync } from "node:fs";
import { createServer, type Server } from "node:http";
import { Readable } from "node:stream";
import { toNodeHandler } from "@modelcontextprotocol/node";
import { canonicalJson } from "@gis-ai-go/evidence/web216-pure";
import { createGcpIdentityAdapter, gcpAuthorise, GcpIdentityError, type GcpIdentityConfig, type GcpJwtVerifier } from "./gcp-identity.js";
import { createGcpCpihApplication, type GcpEvidenceConfig } from "./gcp-application.js";
import { createGcpMcpHandler } from "./gcp-mcp.js";
import { type GcpAtomicDocumentStore, type GcpFirestoreConfig } from "./gcp-firestore.js";
import { type GcpKnowledgeService } from "./gcp-knowledge.js";
import { readBoundedBody } from "./http-server.js";
import { createGcpBrowserOidc, GcpBrowserIdentityError, validateGcpBrowserConfig, type GcpBrowserSecrets } from "./gcp-oidc-browser.js";

export interface GcpRuntimeConfig extends GcpIdentityConfig {
  readonly schema: "gis-ai-go.gcp-runtime.v1";
  readonly allowedOrigins: readonly string[];
  readonly transportPrincipal?: string;
  readonly firestore: GcpFirestoreConfig;
  readonly evidence: GcpEvidenceConfig;
}
export type GcpReleaseAsset = { readonly contentType: string; readonly kind: "website" | "knowledge" | "export" } & (
  { readonly bytes: Uint8Array } | { readonly filePath: string; readonly size: number; readonly sha256: string; readonly inode: number; readonly mtimeMs: number }
);
export interface GcpRuntimeOptions {
  readonly config: GcpRuntimeConfig | null;
  readonly projection: unknown;
  readonly knowledge: GcpKnowledgeService;
  /** Only release-manifest allowlisted files are exposed; request paths never touch disk. */
  readonly assets: ReadonlyMap<string, GcpReleaseAsset>;
  readonly backend: GcpAtomicDocumentStore;
  readonly verifier?: GcpJwtVerifier;
  readonly now?: () => Date;
  readonly browserSecrets?: GcpBrowserSecrets;
  /** Trusted isolated-test HTTP seam only; runtime configuration never selects a mock issuer. */
  readonly browserFetch?: typeof fetch;
}
const HEADERS = Object.freeze({
  "cache-control": "no-store", "x-content-type-options": "nosniff", "referrer-policy": "no-referrer",
  "x-frame-options": "DENY", "cross-origin-resource-policy": "same-origin",
  "content-security-policy": "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; font-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
});
function json(status: number, value: unknown, extra: Record<string, string> = {}) {
  return new Response(canonicalJson(value), { status, headers: { ...HEADERS, "content-type": "application/json; charset=utf-8", ...extra } });
}
function denied(status: number) { return json(status, { schema: "gis-ai-go.gcp-request-problem.v1", code: "request-not-authorised", status }); }
/** Fetch seam is usable in isolated signed-identity tests; it never opens a listener. */
export function createGcpFetchHandler(options: GcpRuntimeOptions) {
  const config = options.config; const now = options.now ?? (() => new Date());
  const identity = config === null ? null : createGcpIdentityAdapter(config, options.verifier);
  const browserConfig = config?.identity.mode === "oidc" ? config.identity.browser : null;
  if (config && browserConfig) validateGcpBrowserConfig(browserConfig, config.publicOrigin);
  const browser = config && browserConfig && options.browserSecrets ? createGcpBrowserOidc({ browser: browserConfig,
    identity: config.identity as Extract<GcpRuntimeConfig["identity"], { mode: "oidc" }>, publicOrigin: config.publicOrigin,
    environment: config.profile, backend: options.backend, secrets: options.browserSecrets, now: () => now().getTime(),
    ...(options.verifier ? { verifier: options.verifier } : {}), ...(options.browserFetch ? { fetch: options.browserFetch } : {}),
  }) : null;
  if (config !== null) for (const origin of config.allowedOrigins) {
    const url = new URL(origin);
    if (url.origin !== origin || url.username || url.password ||
        (url.protocol !== "https:" && !(config.profile === "personal" && url.protocol === "http:" && url.hostname === "127.0.0.1"))) throw Error("Invalid private browser origin");
  }
  const origins = new Set(config?.allowedOrigins ?? []);
  if (config) origins.add(config.publicOrigin);
  const hosts = new Set([...origins].map((origin) => new URL(origin).host));
  if (config?.transportAudience) hosts.add(new URL(config.transportAudience).host);
  let active = 0; let stopped = false;
  return Object.freeze({
    stop: () => { stopped = true; },
    fetch: async (request: Request): Promise<Response> => {
      const url = new URL(request.url); const path = url.pathname;
      if (path === "/healthz" && request.method === "GET") return json(stopped ? 503 : 200, { status: stopped ? "stopping" : "process-alive" });
      if (stopped || config === null || identity === null) return json(503, { status: "blocked-runtime-binding", hosted_authentication: "not-established" });
      const stateKeys = /^\/(?:explorer|webmcp)(?:\/|\/index\.html)?$/u.test(path)
        ? ["q", "view", "tag", "type", "authority", "access", "rights", "freshness"]
        : path === "/knowledge" || path === "/knowledge/" ? ["q"]
          : path === "/api/knowledge/search" ? ["bundle", "query", "limit"] : path === "/api/knowledge/describe" ? ["bundle", "id"] : [];
      const routeKeys = path === "/auth/callback" ? ["code", "state", "iss", "error", "error_description"] : stateKeys;
      if (url.search.length > 4_096 || [...url.searchParams].length > 64 || [...url.searchParams.keys()].some((key) => !routeKeys.includes(key)) ||
          /%|\\|\/\.\.?\//u.test(path) || !hosts.has(request.headers.get("host") ?? url.host) ||
          (request.headers.has("origin") && !origins.has(request.headers.get("origin")!))) return denied(400);
      if (!["GET", "HEAD", "POST"].includes(request.method)) return denied(405);
      if (active >= 8) return denied(429);
      active += 1;
      try {
        if (path.startsWith("/auth/")) {
          await identity.authenticateTransport(request);
          if (!browser) return json(503, { gate: "approved-browser-registration-and-secret-references-required" });
          const response = await browser.handle(request); if (!response) return json(404, { status: "not-found" });
          const headers = new Headers(response.headers);
          for (const [key, value] of Object.entries(HEADERS)) headers.set(key, value);
          return new Response(response.body, { status: response.status, headers });
        }
        if ((path === "/.well-known/oauth-protected-resource/mcp" || path === "/.well-known/oauth-protected-resource") && request.method === "GET") {
          // OAuth bootstrap verifies private workload transport, before demanding an application bearer.
          // This public protocol metadata includes no corpus or evidence content.
          await identity.authenticateTransport(request);
          if (config.identity.mode !== "oidc") return json(404, { status: "single-owner-transport-pilot-not-oauth" });
          return json(200, { resource: config.publicOrigin + "/mcp", authorization_servers: [config.identity.issuer],
            bearer_methods_supported: ["header"], scopes_supported: [], resource_name: "GIS AI GO private MCP" });
        }
        // Transport is verified before decrypting or reading a browser session. A cookie never conveys workload identity.
        await identity.authenticateTransport(request);
        const authenticated = browser ? await browser.authenticateRequest(request) : request;
        const envelope = await identity.authenticate(authenticated);
        const principal = envelope.principal;
        const resource = { classification: "public-metadata", environment: config.profile };
        const allowed = (capability: Parameters<typeof gcpAuthorise>[1]) => gcpAuthorise(principal, capability, resource, now().getTime());
        if (path === "/readyz" && request.method === "GET") {
          if (!allowed("operations.status")) return denied(403);
          return json(200, { status: "release-verified-and-identity-bound", identity_kind: principal.kind,
            persistence: "requires-hosted-verification", provider_egress: false, external_model_calls: false });
        }
        if (path === "/mcp") {
          const application = createGcpCpihApplication({ backend: options.backend, principal, projection: options.projection,
            evidence: config.evidence, now });
          const response = await createGcpMcpHandler({ principal, application, knowledge: options.knowledge, now: () => now().getTime() }).fetch(request);
          const headers = new Headers(response.headers);
          for (const [key, value] of Object.entries(HEADERS)) headers.set(key, value);
          return new Response(response.body, { status: response.status, headers });
        }
        if (request.method === "POST") return denied(405);
        if (path === "/api/release") {
          if (!allowed("knowledge.read")) return denied(403); return json(200, options.knowledge.release());
        }
        if (path === "/api/knowledge/search" || path === "/api/knowledge/describe") {
          const search = path.endsWith("/search");
          if (!allowed(search ? "knowledge.search" : "knowledge.read")) return denied(403);
          if (stateKeys.some((key) => url.searchParams.getAll(key).length !== 1)) return denied(400);
          const body = search ? options.knowledge.search({ bundle: url.searchParams.get("bundle"), query: url.searchParams.get("query"), limit: Number(url.searchParams.get("limit")) })
            : options.knowledge.describe({ bundle: url.searchParams.get("bundle"), id: url.searchParams.get("id") });
          if (Buffer.byteLength(canonicalJson(body)) > 262_144) return json(413, { code: "narrow-the-metadata-selection" });
          return json(200, body);
        }
        const asset = options.assets.get(path);
        if (!asset) return json(404, { status: "not-found" });
        const capability = asset.kind === "website" ? "website" : asset.kind === "export" ? "knowledge.export" : "knowledge.read";
        if (!allowed(capability)) return denied(403);
        let body: BodyInit | null; let size: number; let digest: string;
        if ("bytes" in asset) {
          size = asset.bytes.length; digest = createHash("sha256").update(asset.bytes).digest("hex");
          body = request.method === "HEAD" ? null : new Uint8Array(asset.bytes);
        } else {
          const stat = lstatSync(asset.filePath);
          if (!stat.isFile() || stat.isSymbolicLink() || stat.ino !== asset.inode || stat.size !== asset.size || stat.mtimeMs !== asset.mtimeMs) return denied(503);
          size = asset.size; digest = asset.sha256;
          body = request.method === "HEAD" ? null : Readable.toWeb(createReadStream(asset.filePath, { fd: openSync(asset.filePath, constants.O_RDONLY | constants.O_NOFOLLOW), autoClose: true })) as ReadableStream<Uint8Array>;
        }
        return new Response(body, { status: 200,
          headers: { ...HEADERS, "content-type": asset.contentType, "content-length": String(size), "x-gis-content-sha256": digest } });
      } catch (error) {
        if (error instanceof GcpIdentityError || error instanceof GcpBrowserIdentityError) {
          if (browser && request.method === "GET" && options.assets.get(path)?.kind === "website" &&
              request.headers.get("accept")?.includes("text/html")) return new Response(null, { status: 302,
            headers: { ...HEADERS, location: config.publicOrigin + "/auth/login" } });
          return json(401, { code: "signed-identity-required" },
          config.identity.mode === "oidc" ? { "www-authenticate": `Bearer resource_metadata="${config.publicOrigin}/.well-known/oauth-protected-resource/mcp"` } : {});
        }
        return json(503, { code: "private-runtime-unavailable" });
      } finally { active -= 1; }
    },
  });
}
export function createGcpServer(options: GcpRuntimeOptions): Server & { closePrivateRuntime(): Promise<void> } {
  const handler = createGcpFetchHandler(options);
  const node = toNodeHandler({ fetch: handler.fetch });
  const singleton = new Set(["host", "origin", "authorization", "x-gis-invocation-proof", "content-length", "content-type", "transfer-encoding",
    "mcp-method", "mcp-name", "mcp-protocol-version"]);
  const server = createServer({ maxHeaderSize: 32_768, requireHostHeader: true,
    headersTimeout: 5_000, requestTimeout: 15_000, keepAliveTimeout: 5_000 }, (request, response) => {
    const seen = new Set<string>();
    for (let index = 0; index < request.rawHeaders.length; index += 2) {
      const key = request.rawHeaders[index]!.toLowerCase();
      if (singleton.has(key) && seen.has(key)) { response.writeHead(400, HEADERS); response.end(); request.resume(); return; }
      seen.add(key);
    }
    const length = request.headers["content-length"];
    if ((length !== undefined && (!/^\d+$/u.test(length) || Number(length) > 65_536)) ||
        (length !== undefined && request.headers["transfer-encoding"] !== undefined)) {
      response.writeHead(413, HEADERS); response.end(); request.resume(); return;
    }
    const timer = setTimeout(() => { request.destroy(); response.destroy(); }, 15_000); timer.unref();
    response.once("close", () => clearTimeout(timer)); response.once("finish", () => clearTimeout(timer));
    void readBoundedBody(request, 65_536).then((body) => node({
      method: request.method ?? "GET", url: request.url ?? "/", headers: request.headers,
      async *[Symbol.asyncIterator]() { if (body.length) yield body; },
    }, response)).catch(() => { if (!response.headersSent) response.writeHead(503, HEADERS); response.end(); });
  }) as Server & { closePrivateRuntime(): Promise<void> };
  server.closePrivateRuntime = async () => {
    handler.stop(); server.closeIdleConnections();
    await new Promise<void>((resolve, reject) => {
      const deadline = setTimeout(() => { server.closeAllConnections(); }, 8_000); deadline.unref();
      server.close((error) => { clearTimeout(deadline); error ? reject(error) : resolve(); });
    });
  };
  return server;
}
