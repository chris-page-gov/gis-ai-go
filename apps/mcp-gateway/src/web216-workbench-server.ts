/** Separate local workbench ingress; no generic or LOCAL-212 registration changes. */
import { createHash } from "node:crypto";
import { closeSync, constants, fstatSync, lstatSync, openSync, readdirSync, readSync, realpathSync } from "node:fs";
import { createServer, type IncomingMessage, type Server, type ServerResponse } from "node:http";
import { join } from "node:path";
import { toNodeHandler } from "@modelcontextprotocol/node";
import { canonicalJson } from "@gis-ai-go/evidence";
import { createWeb216CpihMcpHttpHandler, MCP_HTTP_MAX_STANDALONE_BODY_BYTES } from "./mcp-http.js";
import { isWeb216CpihApplication, type Web216CpihApplication } from "./web216-cpih-application.js";
import { WEB216_CPIH_MCP_TOOLS } from "./web216-cpih-mcp.js";
import { BodyReadError, declaredLength, readBoundedBody, GATEWAY_HEADER_BODY_TIMEOUT_MS } from "./http-server.js";

export const WEB216_WORKBENCH_HOST = "127.0.0.1";
export const WEB216_WORKBENCH_PORT = 8_788;
export const WEB216_WORKBENCH_MAX_CONCURRENT = 8;
export const WEB216_WORKBENCH_PROCESSING_MS = 10_000;
const MAX_ASSET_BYTES = 2_097_152;
const MAX_TOTAL_ASSET_BYTES = 8_388_608;
const ASSET_NAME = /^[A-Za-z0-9_-]+-[A-Za-z0-9_-]{6,16}\.(?:js|css|svg|png|woff2)$/u;
const SINGLETON = ["host", "origin", "content-length", "content-type", "transfer-encoding", "mcp-method", "mcp-name", "mcp-protocol-version"];
const FORWARD = ["host", "origin", "content-length", "content-type", "accept", "mcp-method", "mcp-name", "mcp-protocol-version"];
const SECURITY_HEADERS = Object.freeze({
  "cache-control": "no-store", "x-content-type-options": "nosniff", "x-frame-options": "DENY",
  "referrer-policy": "no-referrer", "cross-origin-resource-policy": "same-origin",
  "content-security-policy": "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; font-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
});

export interface Web216WorkbenchServer extends Server {
  readonly assetSha256: string;
  closeWorkbench(): Promise<void>;
}
function safeFile(path: string, maximum: number): Buffer {
  const before = lstatSync(path);
  if (!before.isFile() || before.isSymbolicLink() || before.nlink !== 1 || before.size > maximum) throw Error("Invalid workbench asset");
  const fd = openSync(path, constants.O_RDONLY | constants.O_NOFOLLOW);
  try {
    const opened = fstatSync(fd);
    if (!opened.isFile() || before.ino !== opened.ino || before.dev !== opened.dev || before.size !== opened.size) throw Error("Changed workbench asset");
    const buffer = Buffer.alloc(before.size + 1);
    let count = 0;
    while (count < buffer.length) {
      const got = readSync(fd, buffer, count, buffer.length - count, count);
      if (got === 0) break;
      count += got;
    }
    const after = fstatSync(fd);
    if (count !== before.size || after.size !== before.size || after.mtimeMs !== before.mtimeMs) throw Error("Changed workbench asset");
    return buffer.subarray(0, count);
  } finally { closeSync(fd); }
}
function assetsAt(publicDirectory: string) {
  if (!lstatSync(publicDirectory).isDirectory() || lstatSync(publicDirectory).isSymbolicLink()) throw Error("Invalid workbench directory");
  const root = realpathSync(publicDirectory);
  if (readdirSync(root).sort().join(",") !== "assets,index.html") throw Error("Unexpected workbench build output");
  const assetRoot = join(root, "assets");
  const stat = lstatSync(assetRoot);
  if (!stat.isDirectory() || stat.isSymbolicLink()) throw Error("Invalid workbench asset directory");
  const names = readdirSync(assetRoot).sort();
  if (names.length < 1 || names.length > 64 || names.some((name) => name.length > 180 || !ASSET_NAME.test(name))) throw Error("Unexpected workbench asset name");
  const files = new Map<string, { bytes: Buffer; contentType: string }>();
  files.set("/", { bytes: safeFile(join(root, "index.html"), 65_536), contentType: "text/html; charset=utf-8" });
  let total = files.get("/")!.bytes.length;
  for (const name of names) {
    const bytes = safeFile(join(assetRoot, name), MAX_ASSET_BYTES);
    total += bytes.length;
    if (total > MAX_TOTAL_ASSET_BYTES) throw Error("Workbench assets exceed the total bound");
    const extension = name.slice(name.lastIndexOf(".") + 1);
    const contentType = ({ js: "text/javascript; charset=utf-8", css: "text/css; charset=utf-8", svg: "image/svg+xml", png: "image/png", woff2: "font/woff2" } as Record<string, string>)[extension]!;
    files.set(`/assets/${name}`, { bytes, contentType });
  }
  const html = new TextDecoder("utf-8", { fatal: true }).decode(files.get("/")!.bytes);
  for (const match of html.matchAll(/<(?:script|link)\b[^>]*\b(?:src|href)=["']([^"']+)["']/gu)) {
    const reference = match[1]!;
    // Vite base './' emits document-relative references. Admit only the same
    // closed asset route; never resolve general relative URLs or traversal.
    const route = reference.startsWith("./assets/") ? reference.slice(1) : reference;
    if (!route.startsWith("/assets/") || !ASSET_NAME.test(route.slice("/assets/".length)) || !files.has(route)) {
      throw Error("Workbench page references an unavailable asset");
    }
  }
  const manifest = [...files].map(([path, asset]) => ({ path, bytes: asset.bytes.length, sha256: createHash("sha256").update(asset.bytes).digest("hex") }));
  return { files, sha256: createHash("sha256").update(canonicalJson(manifest)).digest("hex") };
}
function reply(response: ServerResponse, status: number, body: Buffer | string = "", type = "application/json; charset=utf-8", head = false): void {
  if (response.destroyed || response.writableEnded) return;
  response.writeHead(status, { ...SECURITY_HEADERS, "content-type": type, "content-length": Buffer.byteLength(body) });
  response.end(head ? undefined : body);
}
function reject(request: IncomingMessage, response: ServerResponse, status: number): void {
  response.shouldKeepAlive = false;
  response.setHeader("connection", "close");
  response.once("finish", () => request.destroy());
  reply(response, status, JSON.stringify({ error: "workbench_request_rejected", status }));
  request.resume();
}

/** The only injectable input is a trusted static build directory, never a request path. */
export function createWeb216WorkbenchServer(application: Web216CpihApplication, publicDirectory: string): Web216WorkbenchServer {
  if (!isWeb216CpihApplication(application)) throw TypeError("Expected a genuine CPIH application");
  const assets = assetsAt(publicDirectory);
  const mcp = createWeb216CpihMcpHttpHandler(application);
  const nodeMcp = toNodeHandler({ fetch: async (request) => {
    const result = await mcp.fetch(request);
    const headers = new Headers(result.headers);
    for (const [key, value] of Object.entries(SECURITY_HEADERS)) headers.set(key, value);
    return new Response(result.body, { status: result.status, headers });
  } });
  let active = 0;
  let stopping = false;
  const server = createServer({
    requireHostHeader: true, maxHeaderSize: 16_384, connectionsCheckingInterval: 1_000,
    headersTimeout: GATEWAY_HEADER_BODY_TIMEOUT_MS, requestTimeout: GATEWAY_HEADER_BODY_TIMEOUT_MS,
    keepAliveTimeout: GATEWAY_HEADER_BODY_TIMEOUT_MS, rejectNonStandardBodyWrites: true,
  }, (request, response) => {
    const address = server.address();
    const authority = typeof address === "object" && address !== null && address.address === WEB216_WORKBENCH_HOST
      ? `${WEB216_WORKBENCH_HOST}:${address.port}` : undefined;
    const counts = new Map<string, number>();
    for (let index = 0; index < request.rawHeaders.length; index += 2) {
      const name = request.rawHeaders[index]!.toLowerCase(); counts.set(name, (counts.get(name) ?? 0) + 1);
    }
    if (stopping || authority === undefined || request.headers.host !== authority ||
        (request.headers.origin !== undefined && request.headers.origin !== `http://${authority}`) ||
        counts.get("host") !== 1 || request.rawHeaders.length / 2 > 64 ||
        SINGLETON.some((name) => (counts.get(name) ?? 0) > 1) || request.headers["transfer-encoding"] !== undefined) {
      reject(request, response, 403); return;
    }
    const target = request.url ?? "";
    const isMcp = target === "/mcp";
    if (target.length > 256 || (!isMcp && target !== "/healthz" && target !== "/readyz" && !assets.files.has(target))) {
      reject(request, response, 404); return;
    }
    if ((!isMcp && request.method !== "GET" && request.method !== "HEAD") ||
        (isMcp && request.method !== "POST" && request.method !== "GET" && request.method !== "DELETE")) {
      reject(request, response, 405); return;
    }
    if (active >= WEB216_WORKBENCH_MAX_CONCURRENT) {
      response.setHeader("retry-after", "1"); reject(request, response, 429); return;
    }
    try {
      const length = declaredLength(request, isMcp ? MCP_HTTP_MAX_STANDALONE_BODY_BYTES : 0);
      if (isMcp && request.method === "POST" && length === undefined) { reject(request, response, 411); return; }
    } catch (error) { reject(request, response, error instanceof BodyReadError && error.failure === "too_large" ? 413 : 400); return; }
    active += 1;
    let released = false;
    let timer = setTimeout(() => reject(request, response, 408), GATEWAY_HEADER_BODY_TIMEOUT_MS);
    timer.unref();
    const release = () => { if (!released) { released = true; active -= 1; clearTimeout(timer); } };
    response.once("close", release); response.once("finish", release);
    void readBoundedBody(request, isMcp ? MCP_HTTP_MAX_STANDALONE_BODY_BYTES : 0).then(async (body) => {
      if (response.destroyed || response.writableEnded) return;
      clearTimeout(timer);
      timer = setTimeout(() => { request.destroy(); response.destroy(); }, WEB216_WORKBENCH_PROCESSING_MS);
      timer.unref();
      if (isMcp) {
        const headers: Record<string, string> = {};
        for (const name of FORWARD) if (typeof request.headers[name] === "string") headers[name] = request.headers[name];
        await nodeMcp({ method: request.method!, url: "/mcp", headers,
          async *[Symbol.asyncIterator]() { if (body.length > 0) yield body; },
        }, response);
      } else if (target === "/healthz" || target === "/readyz") {
        const readiness = application.readiness();
        reply(response, target === "/readyz" && readiness.status !== "ready" ? 503 : 200,
          JSON.stringify({ schema: "gis-ai-go.web216-workbench-readiness.v1", ...readiness,
            provider_egress: false, activated_supported_release: false, storage: "private-local-durable",
            tools: WEB216_CPIH_MCP_TOOLS, static_content_sha256: assets.sha256,
          }), undefined, request.method === "HEAD");
      } else {
        const asset = assets.files.get(target)!;
        reply(response, 200, asset.bytes, asset.contentType, request.method === "HEAD");
      }
    }).catch((error: unknown) => {
      if (response.destroyed || response.writableEnded) return;
      reject(request, response, error instanceof BodyReadError && error.failure === "too_large" ? 413 : 400);
    });
  }) as Web216WorkbenchServer;
  server.maxHeadersCount = 65; server.maxRequestsPerSocket = 100; server.maxConnections = 32;
  server.setTimeout(WEB216_WORKBENCH_PROCESSING_MS, (socket) => socket.destroy());
  Object.defineProperty(server, "assetSha256", { value: assets.sha256, enumerable: true });
  let closing: Promise<void> | undefined;
  server.closeWorkbench = () => closing ??= (async () => {
    stopping = true;
    const closed = server.listening ? new Promise<void>((resolve, rejectClose) => server.close((error) => error ? rejectClose(error) : resolve())) : Promise.resolve();
    const timeout = setTimeout(() => server.closeAllConnections(), GATEWAY_HEADER_BODY_TIMEOUT_MS); timeout.unref();
    try { await closed; await mcp.close(); } finally { clearTimeout(timeout); }
  })();
  server.once("close", () => { void mcp.close().catch(() => undefined); });
  return server;
}
