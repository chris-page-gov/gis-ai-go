import { randomBytes } from "node:crypto";

import { catalogueActivation } from "./activation.js";
import {
  createCatalogueApplication,
  type CatalogueApplication,
  type CatalogueApplicationOptions,
} from "./catalogue-application.js";
import type { CatalogueSnapshot } from "./catalogue-snapshot.js";
import {
  EvidenceInspectError,
  type EvidenceInspectApplication,
} from "./evidence-application.js";
import { gatewayMetadata } from "./metadata.js";
import {
  createCatalogueOpenApiDocument,
  type GatewayApiOperation,
} from "./openapi.js";
import {
  createCatalogueProblem,
  isCanonicalCatalogueProblemInstance,
  isCatalogueProblemError,
  type CatalogueProblemContext,
} from "./problem.js";

const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/u;
const TRACE_ID = /^[0-9a-f]{32}$/u;
const CONTENT_LENGTH = /^(?:0|[1-9][0-9]*)$/u;
const JSON_NUMBER = /^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/u;
const MAX_URL_LENGTH = 4_096;
const MAX_ACCEPT_LENGTH = 1_024;
const MAX_CONTENT_TYPE_LENGTH = 256;
const MAX_JSON_NESTING = 16;
export const MAX_JSON_BODY_BYTES = 32_768;
export const MAX_JSON_RESPONSE_BYTES = 4_194_304;
const MAX_CONFIGURED_JSON_BODY_BYTES = 1_048_576;

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
  readonly allowedHosts?: readonly string[];
  readonly allowedOrigins?: readonly string[];
  readonly createTraceId?: () => string;
  readonly enabledApiOperations?: readonly GatewayApiOperation[];
  readonly application?: CatalogueApplication;
  readonly evidenceApplication?: EvidenceInspectApplication;
  readonly catalogueApplicationOptions?: CatalogueApplicationOptions;
  /** Reporting only. Error details are never returned to the caller. */
  readonly onerror?: (error: Error) => void;
}

export type BoundedJsonFailure = "duplicate" | "malformed" | "too_large";

export class BoundedJsonError extends Error {
  public constructor(public readonly failure: BoundedJsonFailure) {
    super(failure);
    this.name = "BoundedJsonError";
  }
}

function jsonResponse(
  value: unknown,
  status: number,
  contentType = "application/json",
): Response {
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
    if (
      mediaType !== "application/json" &&
      mediaType !== "application/*" &&
      mediaType !== "*/*"
    ) {
      return false;
    }
    let quality = 1;
    let qualitySeen = false;
    for (const rawParameter of parameters) {
      const parameter = rawParameter.trim();
      if (parameter === "") return false;
      const separator = parameter.indexOf("=");
      if (separator < 1) return false;
      const name = parameter.slice(0, separator).trim();
      const parameterValue = parameter.slice(separator + 1).trim();
      if (name !== "q") continue;
      if (
        qualitySeen ||
        !/^(?:0(?:\.[0-9]{0,3})?|1(?:\.0{0,3})?)$/u.test(parameterValue)
      ) {
        return false;
      }
      qualitySeen = true;
      quality = Number(parameterValue);
    }
    return quality > 0;
  });
}

function isJsonContentType(value: string | null): boolean {
  if (value === null || value.length > MAX_CONTENT_TYPE_LENGTH) return false;
  const [mediaTypePart, ...parameters] = value.toLowerCase().split(";");
  if (mediaTypePart?.trim() !== "application/json") return false;
  let charsetSeen = false;
  for (const rawParameter of parameters) {
    const parameter = rawParameter.trim();
    if (parameter === "") return false;
    const separator = parameter.indexOf("=");
    if (separator < 1) return false;
    const name = parameter.slice(0, separator).trim();
    let parameterValue = parameter.slice(separator + 1).trim();
    if (parameterValue.startsWith('"') || parameterValue.endsWith('"')) {
      if (!(parameterValue.startsWith('"') && parameterValue.endsWith('"'))) return false;
      parameterValue = parameterValue.slice(1, -1);
    }
    if (name !== "charset" || charsetSeen || parameterValue !== "utf-8") return false;
    charsetSeen = true;
  }
  return true;
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

function evidenceProblemResponse(
  error: EvidenceInspectError,
  context: CatalogueProblemContext,
): Response {
  const problem = createCatalogueProblem(error.code, context);
  return jsonResponse(problem, problem.status, "application/problem+json");
}

function report(options: GatewayHttpOptions, error: unknown): void {
  const reported = error instanceof Error ? error : new Error("Non-Error direct API failure");
  try {
    options.onerror?.(reported);
  } catch {
    // Reporting must never change or disclose the client result.
  }
}

function catalogueSuccessResponse(
  value: unknown,
  context: CatalogueProblemContext,
  options: GatewayHttpOptions,
): Response {
  let serialised: string;
  try {
    const candidate = JSON.stringify(value);
    if (candidate === undefined) throw new TypeError("Catalogue result is not JSON serialisable");
    serialised = candidate;
  } catch (error) {
    report(options, error);
    return problemResponse("internal_error", context, "The request could not be processed.");
  }
  if (new TextEncoder().encode(serialised).byteLength > MAX_JSON_RESPONSE_BYTES) {
    report(options, new Error("Catalogue application result exceeded the direct API byte limit"));
    return problemResponse(
      "complexity_limit_exceeded",
      context,
      `The JSON response exceeds ${MAX_JSON_RESPONSE_BYTES} bytes. Narrow the request.`,
    );
  }
  return new Response(`${serialised}\n`, {
    status: 200,
    headers: {
      "cache-control": "no-store",
      "content-type": "application/json; charset=utf-8",
      "x-content-type-options": "nosniff",
    },
  });
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

function hasValidUnicodeScalars(value: string): boolean {
  for (let index = 0; index < value.length; index += 1) {
    const unit = value.charCodeAt(index);
    if (unit >= 0xd800 && unit <= 0xdbff) {
      const next = value.charCodeAt(index + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) return false;
      index += 1;
    } else if (unit >= 0xdc00 && unit <= 0xdfff) {
      return false;
    }
  }
  return true;
}

class StrictJsonScanner {
  private index = 0;

  public constructor(private readonly text: string) {}

  public scan(): void {
    this.skipWhitespace();
    this.scanValue(0);
    this.skipWhitespace();
    if (this.index !== this.text.length) this.malformed();
  }

  private malformed(): never {
    throw new BoundedJsonError("malformed");
  }

  private skipWhitespace(): void {
    while (
      this.text[this.index] === " " ||
      this.text[this.index] === "\t" ||
      this.text[this.index] === "\n" ||
      this.text[this.index] === "\r"
    ) {
      this.index += 1;
    }
  }

  private scanValue(depth: number): void {
    if (depth > MAX_JSON_NESTING) this.malformed();
    const token = this.text[this.index];
    if (token === "{") {
      this.scanObject(depth);
      return;
    }
    if (token === "[") {
      this.scanArray(depth);
      return;
    }
    if (token === '"') {
      this.scanString();
      return;
    }
    if (token === "t") {
      this.scanLiteral("true");
      return;
    }
    if (token === "f") {
      this.scanLiteral("false");
      return;
    }
    if (token === "n") {
      this.scanLiteral("null");
      return;
    }
    this.scanNumber();
  }

  private scanObject(depth: number): void {
    this.index += 1;
    this.skipWhitespace();
    const keys = new Set<string>();
    if (this.text[this.index] === "}") {
      this.index += 1;
      return;
    }
    while (this.index < this.text.length) {
      if (this.text[this.index] !== '"') this.malformed();
      const key = this.scanString();
      if (keys.has(key)) throw new BoundedJsonError("duplicate");
      keys.add(key);
      this.skipWhitespace();
      if (this.text[this.index] !== ":") this.malformed();
      this.index += 1;
      this.skipWhitespace();
      this.scanValue(depth + 1);
      this.skipWhitespace();
      const separator = this.text[this.index];
      if (separator === "}") {
        this.index += 1;
        return;
      }
      if (separator !== ",") this.malformed();
      this.index += 1;
      this.skipWhitespace();
    }
    this.malformed();
  }

  private scanArray(depth: number): void {
    this.index += 1;
    this.skipWhitespace();
    if (this.text[this.index] === "]") {
      this.index += 1;
      return;
    }
    while (this.index < this.text.length) {
      this.scanValue(depth + 1);
      this.skipWhitespace();
      const separator = this.text[this.index];
      if (separator === "]") {
        this.index += 1;
        return;
      }
      if (separator !== ",") this.malformed();
      this.index += 1;
      this.skipWhitespace();
    }
    this.malformed();
  }

  private scanString(): string {
    const start = this.index;
    this.index += 1;
    while (this.index < this.text.length) {
      const unit = this.text.charCodeAt(this.index);
      if (unit < 0x20) this.malformed();
      if (this.text[this.index] === '"') {
        this.index += 1;
        let decoded: unknown;
        try {
          decoded = JSON.parse(this.text.slice(start, this.index));
        } catch {
          this.malformed();
        }
        if (typeof decoded !== "string" || !hasValidUnicodeScalars(decoded)) {
          this.malformed();
        }
        return decoded;
      }
      if (this.text[this.index] === "\\") {
        this.index += 1;
        const escaped = this.text[this.index];
        if (escaped === "u") {
          if (
            !/^[0-9a-fA-F]{4}$/u.test(
              this.text.slice(this.index + 1, this.index + 5),
            )
          ) {
            this.malformed();
          }
          this.index += 5;
          continue;
        }
        if (escaped === undefined || !'"\\/bfnrt'.includes(escaped)) this.malformed();
      }
      this.index += 1;
    }
    this.malformed();
  }

  private scanLiteral(literal: string): void {
    if (this.text.slice(this.index, this.index + literal.length) !== literal) {
      this.malformed();
    }
    this.index += literal.length;
  }

  private scanNumber(): void {
    const match = JSON_NUMBER.exec(this.text.slice(this.index));
    if (match?.[0] === undefined || !Number.isFinite(Number(match[0]))) this.malformed();
    this.index += match[0].length;
  }
}

function assertMaximumBodyBytes(maximumBytes: number): void {
  if (
    !Number.isSafeInteger(maximumBytes) ||
    maximumBytes < 1 ||
    maximumBytes > MAX_CONFIGURED_JSON_BODY_BYTES
  ) {
    throw new TypeError("maximum JSON body bytes must be an integer from 1 to 1048576");
  }
}

/** Parse one strict UTF-8 JSON value with duplicate-key and nesting protection. */
export function parseBoundedJsonBytes(
  bytes: Uint8Array,
  maximumBytes: number,
): unknown {
  assertMaximumBodyBytes(maximumBytes);
  if (!(bytes instanceof Uint8Array)) throw new TypeError("JSON body must be bytes");
  if (bytes.byteLength > maximumBytes) throw new BoundedJsonError("too_large");
  let text: string;
  try {
    text = new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(bytes);
  } catch {
    throw new BoundedJsonError("malformed");
  }
  new StrictJsonScanner(text).scan();
  try {
    return JSON.parse(text) as unknown;
  } catch {
    throw new BoundedJsonError("malformed");
  }
}

function declaredContentLength(request: Request, maximumBytes: number): number | null {
  const value = request.headers.get("content-length");
  if (value === null) return null;
  if (!CONTENT_LENGTH.test(value)) throw new BoundedJsonError("malformed");
  const length = Number(value);
  if (!Number.isSafeInteger(length)) throw new BoundedJsonError("malformed");
  if (length > maximumBytes) throw new BoundedJsonError("too_large");
  return length;
}

async function readBoundedJson(request: Request): Promise<unknown> {
  const declaredLength = declaredContentLength(request, MAX_JSON_BODY_BYTES);
  if (request.body === null) throw new BoundedJsonError("malformed");
  const reader = request.body.getReader();
  const chunks: Uint8Array[] = [];
  let length = 0;
  try {
    while (true) {
      const result = await reader.read();
      if (result.done) break;
      length += result.value.byteLength;
      if (length > MAX_JSON_BODY_BYTES) {
        await reader.cancel();
        throw new BoundedJsonError("too_large");
      }
      chunks.push(result.value);
    }
  } catch (error) {
    if (error instanceof BoundedJsonError) throw error;
    throw new BoundedJsonError("malformed");
  } finally {
    reader.releaseLock();
  }
  if (declaredLength !== null && declaredLength !== length) {
    throw new BoundedJsonError("malformed");
  }
  const bytes = new Uint8Array(length);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return parseBoundedJsonBytes(bytes, MAX_JSON_BODY_BYTES);
}

function bodyFailureResponse(error: BoundedJsonError, context: CatalogueProblemContext): Response {
  const detail = error.failure === "too_large"
    ? `The JSON request body exceeds ${MAX_JSON_BODY_BYTES} bytes.`
    : error.failure === "duplicate"
      ? "The JSON request body contains duplicate object properties."
      : "Supply one well-formed UTF-8 JSON request body.";
  return problemResponse("invalid_request", context, detail);
}

interface OperationApplications {
  readonly catalogue?: CatalogueApplication;
  readonly evidence?: EvidenceInspectApplication;
}

function operationApplications(
  options: GatewayHttpOptions,
  enabledApiOperations: readonly GatewayApiOperation[],
): OperationApplications {
  if (options.application !== undefined && options.catalogueApplicationOptions !== undefined) {
    throw new TypeError(
      "Supply either a shared catalogue application or catalogue application options, not both",
    );
  }
  const needsCatalogue = enabledApiOperations.some((operation) =>
    operation === "catalogue.search" || operation === "catalogue.describe"
  );
  const needsEvidence = enabledApiOperations.includes("evidence.inspect");
  if (needsEvidence && options.evidenceApplication === undefined) {
    throw new TypeError(
      "evidenceApplication is required when evidence.inspect is explicitly mounted",
    );
  }
  return Object.freeze({
    ...(needsCatalogue
      ? {
          catalogue: options.application ?? createCatalogueApplication(
            options.snapshot,
            options.catalogueApplicationOptions ?? {
              software: {
                name: "gis-ai-go-mcp-gateway",
                version: gatewayMetadata.version,
                revision: options.snapshot.revision,
              },
            },
          ),
        }
      : {}),
    ...(needsEvidence
      ? { evidence: options.evidenceApplication as EvidenceInspectApplication }
      : {}),
  });
}

export function createGatewayHttpHandler(
  options: GatewayHttpOptions,
): (request: Request) => Promise<Response> {
  const allowedHosts = new Set(
    (options.allowedHosts ?? DEFAULT_ALLOWED_HOSTS).map((host) => host.toLowerCase()),
  );
  const allowedOrigins = new Set(options.allowedOrigins ?? DEFAULT_ALLOWED_ORIGINS);
  const enabledApiOperations = options.enabledApiOperations ??
    catalogueActivation.activeApiOperations;
  const openApiDocument = createCatalogueOpenApiDocument(enabledApiOperations);
  const applications = operationApplications(options, enabledApiOperations);
  const enabled = new Set(enabledApiOperations);
  const createTraceId = options.createTraceId ?? (() => randomBytes(16).toString("hex"));

  if (allowedHosts.size === 0 || allowedOrigins.size === 0) {
    throw new TypeError("The gateway requires explicit allowed hosts and origins");
  }
  if (
    [...allowedHosts].some((host) => host === "") ||
    [...allowedOrigins].some((origin) => origin === "")
  ) {
    throw new TypeError("Allowed hosts and origins must not contain empty values");
  }
  if (options.onerror !== undefined && typeof options.onerror !== "function") {
    throw new TypeError("onerror must be a function");
  }

  return async (request: Request): Promise<Response> => {
    const traceId = createTraceId();
    if (!TRACE_ID.test(traceId)) {
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
    if (
      host === null ||
      !allowedHosts.has(host.toLowerCase()) ||
      parsedUrl.protocol !== "http:" ||
      parsedUrl.host.toLowerCase() !== host.toLowerCase() ||
      parsedUrl.username !== "" ||
      parsedUrl.password !== ""
    ) {
      return problemResponse(
        "invalid_request",
        context,
        "The request Host header is not allowed.",
      );
    }
    const origin = request.headers.get("origin");
    if (origin !== null && !allowedOrigins.has(origin)) {
      return problemResponse(
        "invalid_request",
        context,
        "The request Origin header is not allowed.",
      );
    }
    if (parsedUrl.search !== "" || parsedUrl.hash !== "") {
      return problemResponse(
        "invalid_request",
        context,
        "Query parameters and fragments are not supported.",
      );
    }
    if (!acceptsJson(request.headers.get("accept"))) {
      return problemResponse(
        "not_acceptable",
        context,
        "The response is available only as JSON.",
      );
    }

    if (
      parsedUrl.pathname === "/healthz" ||
      parsedUrl.pathname === "/readyz" ||
      parsedUrl.pathname === "/openapi.json"
    ) {
      if (request.method !== "GET") {
        return problemResponse(
          "invalid_request",
          context,
          "This route accepts GET requests only.",
        );
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
      }
    }

    const operation = parsedUrl.pathname === "/catalogue/search"
      ? "catalogue.search"
      : parsedUrl.pathname === "/catalogue/describe"
        ? "catalogue.describe"
        : parsedUrl.pathname === "/evidence/inspect"
          ? "evidence.inspect"
        : undefined;
    if (operation === undefined || !enabled.has(operation)) {
      return problemResponse(
        "invalid_request",
        context,
        "The requested route is not part of this candidate.",
      );
    }
    if (request.method !== "POST") {
      return problemResponse("invalid_request", context, "This route accepts POST requests only.");
    }
    if (!isJsonContentType(request.headers.get("content-type"))) {
      return problemResponse(
        "invalid_request",
        context,
        "The request body is available only as application/json with UTF-8 encoding.",
      );
    }

    let body: unknown;
    try {
      body = await readBoundedJson(request);
    } catch (error) {
      if (error instanceof BoundedJsonError) return bodyFailureResponse(error, context);
      report(options, error);
      return problemResponse("internal_error", context, "The request could not be processed.");
    }

    try {
      const result = operation === "catalogue.search"
        ? (applications.catalogue as CatalogueApplication).search(body, context)
        : operation === "catalogue.describe"
          ? (applications.catalogue as CatalogueApplication).describe(body, context)
          : (applications.evidence as EvidenceInspectApplication).inspect(body, context);
      return catalogueSuccessResponse(result, context, options);
    } catch (error) {
      if (isCatalogueProblemError(error)) {
        return jsonResponse(error.problem, error.problem.status, "application/problem+json");
      }
      if (error instanceof EvidenceInspectError) {
        return evidenceProblemResponse(error, context);
      }
      report(options, error);
      return problemResponse("internal_error", context, "The request could not be processed.");
    }
  };
}
