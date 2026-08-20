import { randomBytes } from "node:crypto";

import { catalogueActivation } from "./activation.js";
import type { CatalogueSnapshot } from "./catalogue-snapshot.js";
import { gatewayMetadata } from "./metadata.js";
import { catalogueOpenApiDocument, type OpenApiDocument } from "./openapi.js";
import {
  createCatalogueProblem,
  isCanonicalCatalogueProblemInstance,
  type CatalogueProblemContext,
} from "./problem.js";

const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/u;
const MAX_URL_LENGTH = 4_096;
const MAX_ACCEPT_LENGTH = 1_024;

export const DEFAULT_ALLOWED_HOSTS = Object.freeze([
  "127.0.0.1:8787",
  "localhost:8787",
] as const);

export const DEFAULT_ALLOWED_ORIGINS = Object.freeze([
  "http://127.0.0.1:8787",
  "http://localhost:8787",
] as const);

export interface GatewayHttpOptions {
  readonly snapshot: CatalogueSnapshot;
  readonly openApiDocument?: OpenApiDocument;
  readonly allowedHosts?: readonly string[];
  readonly allowedOrigins?: readonly string[];
  readonly createTraceId?: () => string;
}

function jsonResponse(value: unknown, status: number, contentType = "application/json"): Response {
  return new Response(`${JSON.stringify(value)}\n`, {
    status,
    headers: {
      "cache-control": "no-store",
      "content-type": `${contentType}; charset=utf-8`,
      "x-content-type-options": "nosniff",
    },
  });
}

function acceptsJson(value: string | null): boolean {
  if (value === null || value.trim() === "") return true;
  if (value.length > MAX_ACCEPT_LENGTH) return false;
  return value.split(",").some((entry) => {
    const [mediaTypePart, ...parameters] = entry.trim().toLowerCase().split(";");
    const mediaType = mediaTypePart?.trim();
    if (mediaType !== "application/json" && mediaType !== "application/*" && mediaType !== "*/*") {
      return false;
    }
    return !parameters.some((parameter) => /^\s*q\s*=\s*0(?:\.0*)?\s*$/u.test(parameter));
  });
}

function requestId(request: Request): string {
  const candidate = request.headers.get("x-request-id");
  return candidate !== null && REQUEST_ID.test(candidate)
    ? candidate
    : randomBytes(16).toString("hex");
}

function problemResponse(
  code: Parameters<typeof createCatalogueProblem>[0],
  context: CatalogueProblemContext,
  detail: string,
): Response {
  const problem = createCatalogueProblem(code, context, { detail });
  return jsonResponse(problem, problem.status, "application/problem+json");
}

function catalogueIdentity(snapshot: CatalogueSnapshot): Readonly<Record<string, unknown>> {
  return Object.freeze({
    version: snapshot.version,
    revision: snapshot.revision,
    content_root_sha256: snapshot.contentRootSha256,
    record_count: snapshot.recordCount,
    stale: snapshot.stale,
    warnings: snapshot.warnings,
  });
}

export function createGatewayHttpHandler(
  options: GatewayHttpOptions,
): (request: Request) => Promise<Response> {
  const allowedHosts = new Set(options.allowedHosts ?? DEFAULT_ALLOWED_HOSTS);
  const allowedOrigins = new Set(options.allowedOrigins ?? DEFAULT_ALLOWED_ORIGINS);
  const openApiDocument = options.openApiDocument ?? catalogueOpenApiDocument;
  const createTraceId = options.createTraceId ?? (() => randomBytes(16).toString("hex"));

  if (allowedHosts.size === 0 || allowedOrigins.size === 0) {
    throw new TypeError("The gateway requires explicit allowed hosts and origins");
  }

  return async (request: Request): Promise<Response> => {
    const traceId = createTraceId();
    if (!/^[0-9a-f]{32}$/u.test(traceId)) {
      throw new TypeError("Trace identifiers must be 16-byte lowercase hexadecimal values");
    }
    const parsedUrl = new URL(request.url);
    const context: CatalogueProblemContext = {
      requestId: requestId(request),
      traceId,
      ...(isCanonicalCatalogueProblemInstance(parsedUrl.pathname)
        ? { instance: parsedUrl.pathname }
        : {}),
    };

    if (request.url.length > MAX_URL_LENGTH) {
      return problemResponse("invalid_request", context, "The request URL is too long.");
    }
    const host = request.headers.get("host");
    if (host === null || !allowedHosts.has(host.toLowerCase())) {
      return problemResponse("invalid_request", context, "The request Host header is not allowed.");
    }
    const origin = request.headers.get("origin");
    if (origin !== null && !allowedOrigins.has(origin)) {
      return problemResponse(
        "invalid_request",
        context,
        "The request Origin header is not allowed.",
      );
    }
    if (request.method !== "GET") {
      return problemResponse(
        "invalid_request",
        context,
        "This candidate accepts GET requests only.",
      );
    }
    if (!acceptsJson(request.headers.get("accept"))) {
      return problemResponse(
        "not_acceptable",
        context,
        "The response is available only as JSON.",
      );
    }

    if (parsedUrl.search !== "") {
      return problemResponse("invalid_request", context, "Query parameters are not supported.");
    }

    switch (parsedUrl.pathname) {
      case "/healthz":
        return jsonResponse(
          {
            status: "ok",
            product: gatewayMetadata.product,
            lifecycle: gatewayMetadata.lifecycle,
            catalogue: catalogueIdentity(options.snapshot),
          },
          200,
        );
      case "/readyz":
        return jsonResponse(
          {
            status: catalogueActivation.state,
            reason: catalogueActivation.reason,
            active_tools: catalogueActivation.activeTools,
            active_api_operations: catalogueActivation.activeApiOperations,
          },
          503,
        );
      case "/openapi.json":
        return jsonResponse(openApiDocument, 200);
      default:
        return problemResponse(
          "invalid_request",
          context,
          "The requested route is not part of this candidate.",
        );
    }
  };
}
