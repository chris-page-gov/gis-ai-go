import {
  createServer,
  type IncomingMessage,
  type Server,
  type ServerResponse,
} from "node:http";
import { randomBytes } from "node:crypto";

import { toNodeHandler, type NodeIncomingMessageLike } from "@modelcontextprotocol/node";

import {
  createCatalogueApplication,
  type CatalogueApplication,
} from "./catalogue-application.js";
import type { CatalogueSnapshot } from "./catalogue-snapshot.js";
import type { EvidenceInspectApplication } from "./evidence-application.js";
import {
  BoundedJsonError,
  createGatewayHttpHandler,
  MAX_JSON_BODY_BYTES,
  parseBoundedJsonBytes,
} from "./http-app.js";
import {
  createCatalogueMcpHttpHandler,
  MCP_HTTP_MAX_STANDALONE_BODY_BYTES,
} from "./mcp-http.js";
import {
  type CatalogueMcpRequestContextFactory,
  type GatewayMcpOperation,
  type GatewayMcpResource,
} from "./mcp-server.js";
import { gatewayMetadata } from "./metadata.js";
import type { GatewayApiOperation } from "./openapi.js";
import { createCatalogueProblem } from "./problem.js";

const MAX_URL_LENGTH = 4_096;
const MAX_HEADER_COUNT = 64;
export {
  MCP_HTTP_MAX_STANDALONE_BODY_BYTES as MAX_MCP_JSON_BODY_BYTES,
} from "./mcp-http.js";
export const DEFAULT_MAX_CONCURRENT_REQUESTS = 32;

const DEFAULT_MCP_ALLOWED_HOSTNAMES = Object.freeze([
  "127.0.0.1",
  "localhost",
] as const);
const DEFAULT_MCP_ALLOWED_ORIGINS = Object.freeze([
  "http://127.0.0.1:8787",
  "http://localhost:8787",
] as const);
const FORWARDED_MCP_HEADERS = Object.freeze([
  "accept",
  "content-length",
  "content-type",
  "host",
  "mcp-method",
  "mcp-name",
  "mcp-protocol-version",
  "origin",
] as const);
const SINGLETON_HEADERS = Object.freeze([
  "content-length",
  "content-type",
  "host",
  "mcp-method",
  "mcp-name",
  "mcp-protocol-version",
  "origin",
  "transfer-encoding",
] as const);
const FETCH_FORBIDDEN_METHODS = new Set(["CONNECT", "TRACE", "TRACK"]);

export interface GatewayNodeServerOptions {
  /** Explicit local-conformance seam. Omission keeps every direct route blocked. */
  readonly enabledApiOperations?: readonly GatewayApiOperation[];
  /** Explicit local-conformance seam. Omission keeps every MCP tool blocked. */
  readonly enabledMcpOperations?: readonly GatewayMcpOperation[];
  /** Explicit local-conformance seam. Omission advertises no MCP resources. */
  readonly enabledMcpResources?: readonly GatewayMcpResource[];
  readonly application?: CatalogueApplication;
  readonly evidenceApplication?: EvidenceInspectApplication;
  readonly createTraceId?: () => string;
  readonly createMcpRequestContext?: CatalogueMcpRequestContextFactory;
  readonly directAllowedHosts?: readonly string[];
  readonly directAllowedOrigins?: readonly string[];
  readonly mcpAllowedHostnames?: readonly string[];
  readonly mcpAllowedOrigins?: readonly string[];
  readonly maxConcurrentRequests?: number;
  /** Reporting only. Error detail is never returned to a caller. */
  readonly onerror?: (error: Error) => void;
}

export interface GatewayNodeServer extends Server {
  /** Close MCP state before stopping the listener; safe to call repeatedly. */
  closeGateway(): Promise<void>;
}

type BodyFailure = "malformed" | "too_large";

class BodyReadError extends Error {
  public constructor(public readonly failure: BodyFailure) {
    super(failure);
    this.name = "BodyReadError";
  }
}

function report(options: GatewayNodeServerOptions, error: unknown): void {
  const reported = error instanceof Error ? error : new Error("Non-Error HTTP failure");
  try {
    options.onerror?.(reported);
  } catch {
    // Reporting must never change or disclose the client result.
  }
}

function writeResponse(response: ServerResponse, result: Response): Promise<void> {
  response.statusCode = result.status;
  result.headers.forEach((value, name) => response.setHeader(name, value));
  return result.arrayBuffer().then((body) => {
    response.setHeader("content-length", body.byteLength);
    response.end(Buffer.from(body));
  });
}

function requestUrl(request: IncomingMessage): URL | undefined {
  const host = request.headers.host;
  const target = request.url;
  if (
    host === undefined ||
    target === undefined ||
    target.length > MAX_URL_LENGTH ||
    !target.startsWith("/") ||
    target.startsWith("//") ||
    target.includes("\\") ||
    target.includes("#")
  ) {
    return undefined;
  }
  try {
    const parsed = new URL(target, `http://${host}`);
    if (`${parsed.pathname}${parsed.search}` !== target) return undefined;
    return parsed;
  } catch {
    return undefined;
  }
}

function applicationHeaders(request: IncomingMessage): Headers {
  const headers = new Headers();
  for (const name of [
    "accept",
    "content-length",
    "content-type",
    "host",
    "origin",
    "x-request-id",
  ] as const) {
    const value = request.headers[name];
    if (typeof value === "string") headers.set(name, value);
  }
  return headers;
}

function mcpHeaders(request: IncomingMessage): Record<string, string> {
  const headers: Record<string, string> = {};
  for (const name of FORWARDED_MCP_HEADERS) {
    const value = request.headers[name];
    if (typeof value === "string") headers[name] = value;
  }
  return headers;
}

function headerOccurrences(request: IncomingMessage, expectedName: string): number {
  let count = 0;
  for (let index = 0; index < request.rawHeaders.length; index += 2) {
    if (request.rawHeaders[index]?.toLowerCase() === expectedName) count += 1;
  }
  return count;
}

function hasAmbiguousHeaders(request: IncomingMessage): boolean {
  return SINGLETON_HEADERS.some((name) => headerOccurrences(request, name) > 1);
}

function rejectRequest(
  response: ServerResponse,
  status = 400,
  extraHeaders: Readonly<Record<string, string>> = {},
): void {
  response.writeHead(status, {
    "cache-control": "no-store",
    "content-length": "0",
    "x-content-type-options": "nosniff",
    ...extraHeaders,
  });
  response.end();
}

function jsonRpcError(
  response: ServerResponse,
  status: number,
  code: number,
  message: string,
  extraHeaders: Readonly<Record<string, string>> = {},
): void {
  const body = JSON.stringify({
    jsonrpc: "2.0",
    id: null,
    error: { code, message },
  });
  response.writeHead(status, {
    "cache-control": "no-store",
    "content-length": Buffer.byteLength(body),
    "content-type": "application/json; charset=utf-8",
    "x-content-type-options": "nosniff",
    ...extraHeaders,
  });
  response.end(body);
}

function directAdmissionError(response: ServerResponse): void {
  const problem = createCatalogueProblem(
    "rate_limited",
    {
      requestId: `http-${randomBytes(12).toString("hex")}`,
      traceId: randomBytes(16).toString("hex"),
    },
    {
      detail: "Too many requests are already being processed.",
      retryAfterSeconds: 1,
    },
  );
  const body = JSON.stringify(problem);
  response.writeHead(problem.status, {
    "cache-control": "no-store",
    "content-length": Buffer.byteLength(body),
    "content-type": "application/problem+json; charset=utf-8",
    "retry-after": "1",
    "x-content-type-options": "nosniff",
  });
  response.end(body);
}

function closeAfterResponse(request: IncomingMessage, response: ServerResponse): void {
  response.shouldKeepAlive = false;
  response.setHeader("connection", "close");
  response.once("finish", () => request.destroy());
  request.resume();
}

function rejectBeforeBody(
  request: IncomingMessage,
  response: ServerResponse,
  write: () => void,
): void {
  closeAfterResponse(request, response);
  write();
}

function allowedMcpHostnames(configured: readonly string[]): ReadonlySet<string> {
  const hostnames = new Set<string>();
  for (const candidate of configured) {
    let parsed: URL;
    try {
      parsed = new URL(`http://${candidate}/`);
    } catch {
      throw new TypeError("MCP allowed hostnames must be canonical hostnames");
    }
    if (
      candidate !== candidate.toLowerCase() ||
      parsed.hostname !== candidate ||
      parsed.host !== candidate ||
      parsed.username !== "" ||
      parsed.password !== ""
    ) {
      throw new TypeError("MCP allowed hostnames must be canonical hostnames");
    }
    if (hostnames.has(candidate)) {
      throw new TypeError("MCP allowed hostnames must be unique");
    }
    hostnames.add(candidate);
  }
  if (hostnames.size === 0) {
    throw new TypeError("MCP allowed hostnames must not be empty");
  }
  return hostnames;
}

function requestHostname(request: IncomingMessage): string | undefined {
  const value = request.headers.host;
  if (value === undefined) return undefined;
  try {
    const parsed = new URL(`http://${value}/`);
    if (parsed.username !== "" || parsed.password !== "") return undefined;
    return parsed.hostname.toLowerCase();
  } catch {
    return undefined;
  }
}

function allowedMcpOrigins(configured: readonly string[]): ReadonlySet<string> {
  const origins = new Set<string>();
  for (const candidate of configured) {
    let parsed: URL;
    try {
      parsed = new URL(candidate);
    } catch {
      throw new TypeError("MCP allowed origins must be canonical HTTP origins");
    }
    if (
      (parsed.protocol !== "http:" && parsed.protocol !== "https:") ||
      parsed.origin !== candidate ||
      parsed.username !== "" ||
      parsed.password !== ""
    ) {
      throw new TypeError("MCP allowed origins must be canonical HTTP origins");
    }
    if (origins.has(candidate)) throw new TypeError("MCP allowed origins must be unique");
    origins.add(candidate);
  }
  if (origins.size === 0) throw new TypeError("MCP allowed origins must not be empty");
  return origins;
}

function declaredLength(request: IncomingMessage, maximum: number): number | undefined {
  const value = request.headers["content-length"];
  if (value === undefined) return undefined;
  if (!/^(?:0|[1-9][0-9]*)$/u.test(value)) throw new BodyReadError("malformed");
  const parsed = Number(value);
  if (!Number.isSafeInteger(parsed)) throw new BodyReadError("malformed");
  if (parsed > maximum) throw new BodyReadError("too_large");
  return parsed;
}

async function readBoundedBody(
  request: IncomingMessage,
  maximum: number,
): Promise<Uint8Array> {
  const expectedLength = declaredLength(request, maximum);
  const chunks: Uint8Array[] = [];
  let length = 0;
  try {
    for await (const rawChunk of request) {
      const chunk = typeof rawChunk === "string"
        ? new TextEncoder().encode(rawChunk)
        : new Uint8Array(rawChunk);
      length += chunk.byteLength;
      if (length > maximum) throw new BodyReadError("too_large");
      chunks.push(chunk);
    }
  } catch (error) {
    if (error instanceof BodyReadError) throw error;
    throw new BodyReadError("malformed");
  }
  if (expectedLength !== undefined && expectedLength !== length) {
    throw new BodyReadError("malformed");
  }
  const body = new Uint8Array(length);
  let offset = 0;
  for (const chunk of chunks) {
    body.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return body;
}

function directRequest(
  request: IncomingMessage,
  url: URL,
  body: Uint8Array,
  methodOverride?: string,
): Request {
  const requestedMethod = methodOverride ?? request.method ?? "GET";
  const method = FETCH_FORBIDDEN_METHODS.has(requestedMethod.toUpperCase())
    ? "PUT"
    : requestedMethod;
  const exactBody = body.buffer.slice(
    body.byteOffset,
    body.byteOffset + body.byteLength,
  ) as ArrayBuffer;
  return new Request(url, {
    method,
    headers: applicationHeaders(request),
    ...(method === "GET" || method === "HEAD" || body.byteLength === 0
      ? {}
      : { body: exactBody }),
  });
}

function mcpRequest(request: IncomingMessage): NodeIncomingMessageLike {
  const requestedMethod = request.method;
  const method = requestedMethod !== undefined &&
      FETCH_FORBIDDEN_METHODS.has(requestedMethod.toUpperCase())
    ? "DELETE"
    : requestedMethod;
  return {
    ...(method === undefined ? {} : { method }),
    ...(request.url === undefined ? {} : { url: request.url }),
    headers: mcpHeaders(request),
    async *[Symbol.asyncIterator](): AsyncGenerator<never> {
      return;
    },
  };
}

function assertServerOptions(options: GatewayNodeServerOptions): number {
  const maximum = options.maxConcurrentRequests ?? DEFAULT_MAX_CONCURRENT_REQUESTS;
  if (!Number.isSafeInteger(maximum) || maximum < 1 || maximum > 128) {
    throw new TypeError("maxConcurrentRequests must be an integer from 1 to 128");
  }
  if (options.onerror !== undefined && typeof options.onerror !== "function") {
    throw new TypeError("onerror must be a function");
  }
  return maximum;
}

/** Create the bounded loopback Node adapter without binding a network interface. */
export function createGatewayNodeServer(
  snapshot: CatalogueSnapshot,
  options: GatewayNodeServerOptions = {},
): GatewayNodeServer {
  const maximumConcurrency = assertServerOptions(options);
  const application = options.application ?? createCatalogueApplication(snapshot, {
    software: {
      name: "gis-ai-go-mcp-gateway",
      version: gatewayMetadata.version,
      revision: snapshot.revision,
    },
  });
  const directHandler = createGatewayHttpHandler({
    snapshot,
    application,
    ...(options.evidenceApplication === undefined
      ? {}
      : { evidenceApplication: options.evidenceApplication }),
    ...(options.enabledApiOperations === undefined
      ? {}
      : { enabledApiOperations: options.enabledApiOperations }),
    ...(options.createTraceId === undefined ? {} : { createTraceId: options.createTraceId }),
    ...(options.directAllowedHosts === undefined
      ? {}
      : { allowedHosts: options.directAllowedHosts }),
    ...(options.directAllowedOrigins === undefined
      ? {}
      : { allowedOrigins: options.directAllowedOrigins }),
    ...(options.onerror === undefined ? {} : { onerror: options.onerror }),
  });
  const mcpHandler = createCatalogueMcpHttpHandler({
    application,
    ...(options.evidenceApplication === undefined
      ? {}
      : { evidenceApplication: options.evidenceApplication }),
    snapshot,
    ...(options.enabledMcpOperations === undefined
      ? {}
      : { enabledOperations: options.enabledMcpOperations }),
    ...(options.enabledMcpResources === undefined
      ? {}
      : { enabledResources: options.enabledMcpResources }),
    ...(options.createMcpRequestContext === undefined
      ? {}
      : { createRequestContext: options.createMcpRequestContext }),
    ...(options.onerror === undefined ? {} : { onerror: options.onerror }),
  });
  const mcpNodeHandler = toNodeHandler(
    {
      fetch: async (request, requestOptions) => {
        const result = await mcpHandler.fetch(request, requestOptions);
        const headers = new Headers(result.headers);
        headers.set("cache-control", "no-store");
        headers.set("x-content-type-options", "nosniff");
        if (headers.get("content-type")?.startsWith("text/event-stream") === true) {
          headers.set("x-accel-buffering", "no");
        }
        return new Response(result.body, {
          status: result.status,
          statusText: result.statusText,
          headers,
        });
      },
    },
    { onerror: (error) => report(options, error) },
  );
  const exactMcpHostnames = allowedMcpHostnames(
    options.mcpAllowedHostnames ?? DEFAULT_MCP_ALLOWED_HOSTNAMES,
  );
  const exactMcpOrigins = allowedMcpOrigins(
    options.mcpAllowedOrigins ?? DEFAULT_MCP_ALLOWED_ORIGINS,
  );
  let activeRequests = 0;

  const server = createServer(
    {
      connectionsCheckingInterval: 1_000,
      headersTimeout: 5_000,
      keepAliveTimeout: 5_000,
      maxHeaderSize: 16_384,
      rejectNonStandardBodyWrites: true,
      requestTimeout: 5_000,
      requireHostHeader: true,
    },
    (request, response) => {
      const url = requestUrl(request);
      if (
        url === undefined ||
        request.rawHeaders.length / 2 > MAX_HEADER_COUNT ||
        headerOccurrences(request, "host") !== 1 ||
        hasAmbiguousHeaders(request) ||
        request.headers["transfer-encoding"] !== undefined
      ) {
        rejectBeforeBody(request, response, () => rejectRequest(response));
        return;
      }
      const isMcp = url.pathname === "/mcp" && url.search === "";
      if (isMcp) {
        const origin = request.headers.origin;
        if (
          !exactMcpHostnames.has(requestHostname(request) ?? "") ||
          (origin !== undefined && !exactMcpOrigins.has(origin))
        ) {
          rejectBeforeBody(request, response, () => {
            jsonRpcError(response, 403, -32_000, "Forbidden");
          });
          return;
        }
      }
      if (activeRequests >= maximumConcurrency) {
        rejectBeforeBody(request, response, () => {
          if (isMcp) {
            jsonRpcError(
              response,
              429,
              -32_000,
              "Too many concurrent requests",
              { "retry-after": "1" },
            );
          } else {
            directAdmissionError(response);
          }
        });
        return;
      }
      activeRequests += 1;
      const maximumBody = isMcp
        ? MCP_HTTP_MAX_STANDALONE_BODY_BYTES
        : MAX_JSON_BODY_BYTES;

      void readBoundedBody(request, maximumBody)
        .then(async (body) => {
          const method = request.method ?? "GET";
          if ((method === "GET" || method === "HEAD") && body.byteLength !== 0) {
            rejectRequest(response);
            return;
          }
          if (!isMcp) {
            await writeResponse(response, await directHandler(directRequest(request, url, body)));
            return;
          }
          let parsedBody: unknown;
          if (body.byteLength > 0) {
            try {
              parsedBody = parseBoundedJsonBytes(
                body,
                MCP_HTTP_MAX_STANDALONE_BODY_BYTES,
              );
            } catch (error) {
              if (error instanceof BoundedJsonError) {
                jsonRpcError(response, 400, -32_700, "Parse error");
                return;
              }
              throw error;
            }
          }
          await mcpNodeHandler(mcpRequest(request), response, parsedBody);
        })
        .catch(async (error: unknown) => {
          if (response.writableEnded || response.destroyed) return;
          if (error instanceof BodyReadError) {
            closeAfterResponse(request, response);
            if (isMcp) {
              jsonRpcError(
                response,
                error.failure === "too_large" ? 413 : 400,
                error.failure === "too_large" ? -32_000 : -32_700,
                error.failure === "too_large" ? "Request body too large" : "Parse error",
                { connection: "close" },
              );
            } else {
              const failureBody = error.failure === "too_large"
                ? new Uint8Array(MAX_JSON_BODY_BYTES + 1)
                : new Uint8Array();
              const originalMethod = request.method ?? "GET";
              const failureMethod = originalMethod === "GET" || originalMethod === "HEAD"
                ? "POST"
                : undefined;
              try {
                await writeResponse(
                  response,
                  await directHandler(
                    directRequest(request, url, failureBody, failureMethod),
                  ),
                );
              } catch (nestedError) {
                report(options, nestedError);
                if (!response.writableEnded && !response.destroyed) {
                  rejectRequest(response, 500, { connection: "close" });
                }
              }
            }
            return;
          }
          report(options, error);
          rejectRequest(response, 500);
        })
        .finally(() => {
          activeRequests -= 1;
        });
    },
  );
  // Retain a detectable sentinel header so 65 or more can be rejected explicitly.
  server.maxHeadersCount = MAX_HEADER_COUNT + 1;
  server.maxRequestsPerSocket = 100;
  server.setTimeout(5_000, (socket) => socket.destroy());

  let handlerClose: Promise<void> | undefined;
  const closeHandler = (): Promise<void> => {
    handlerClose ??= mcpHandler.close().catch((error: unknown) => {
      report(options, error);
    });
    return handlerClose;
  };
  server.once("close", () => void closeHandler());
  const gatewayServer = server as GatewayNodeServer;
  gatewayServer.closeGateway = async (): Promise<void> => {
    await closeHandler();
    if (!server.listening) return;
    await new Promise<void>((resolve, reject) => {
      server.close((error) => error === undefined ? resolve() : reject(error));
    });
  };
  return gatewayServer;
}
