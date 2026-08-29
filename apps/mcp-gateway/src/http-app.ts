import { randomBytes } from "node:crypto";

import { normaliseW3CTraceContext } from "@gis-ai-go/provider-adapter-sdk";

import { catalogueActivation } from "./activation.js";
import {
  createCatalogueApplication,
  type CatalogueApplication,
  type CatalogueApplicationOptions,
} from "./catalogue-application.js";
import type { CatalogueSnapshot } from "./catalogue-snapshot.js";
import {
  EvidenceInspectError,
  isReconciledEvidenceInspectApplication,
  type EvidenceInspectApplication,
} from "./evidence-application.js";
import {
  DataQueryApplicationError,
  isReconciledDataQueryApplication,
  type DataQueryApplication,
} from "./data-query-application.js";
import {
  assessGovernedCandidateReadiness,
  governedCandidateAssemblyBindings,
  snapshotGovernedCandidateOptions,
  snapshotGovernedCandidateStringArray,
  verifyGovernedCandidateOperation,
  type GovernedCandidateAssembly,
} from "./governed-assembly.js";
import { gatewayMetadata } from "./metadata.js";
import {
  createCatalogueOpenApiDocument,
  createGovernedCandidateOpenApiDocument,
  type GatewayApiOperation,
} from "./openapi.js";
import {
  createCatalogueProblem,
  isCanonicalCatalogueProblemInstance,
  isCatalogueProblemError,
  type CatalogueProblemContext,
} from "./problem.js";
import { parsePublicHttpsOrigin } from "./public-origin.js";
import {
  EVIDENCE_READINESS_INTEGRITY_FAILURE_MESSAGE,
  verifyEvidenceReadinessIntegrity,
  type EvidenceReadinessIntegrity,
} from "./readiness-integrity.js";
import { haveExactlyLinkedReconciliationApplications } from "./reconciliation-applications.js";
import {
  type SelectionResolveApplication,
  type SelectionResolveProblem,
} from "./selection-application.js";

const REQUEST_ID = /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/u;
const RAW_IDEMPOTENCY_KEY_TEXT = /gis-ai-go:ik:v1:[0-9a-f]{64}/u;
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
  /** One canonical public HTTPS origin projected into the governed OpenAPI document. */
  readonly openApiServerOrigin?: string;
  /** Trusted test seam. Reconciled data.query always ignores caller request IDs. */
  readonly createRequestId?: () => string;
  readonly createTraceId?: () => string;
  /** Trusted test seam; callers cannot supply the provider-bound parent identifier. */
  readonly createTraceParentId?: () => string;
  readonly enabledApiOperations?: readonly GatewayApiOperation[];
  readonly application?: CatalogueApplication;
  readonly evidenceApplication?: EvidenceInspectApplication;
  readonly selectionApplication?: SelectionResolveApplication;
  readonly dataQueryApplication?: DataQueryApplication;
  /** Exact candidate-only assembly; production entrypoints deliberately omit it. */
  readonly governedCandidateAssembly?: GovernedCandidateAssembly;
  readonly catalogueApplicationOptions?: CatalogueApplicationOptions;
  /** Branded inactive seam; verification can block readiness but never enable it. */
  readonly evidenceReadinessIntegrity?: EvidenceReadinessIntegrity;
  /** Reporting only. Error details are never returned to the caller. */
  readonly onerror?: (error: Error) => void;
}

export type GovernedCandidateHttpOptions = Pick<
  GatewayHttpOptions,
  | "allowedHosts"
  | "allowedOrigins"
  | "openApiServerOrigin"
  | "createRequestId"
  | "createTraceId"
  | "createTraceParentId"
  | "onerror"
>;

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
  return candidate !== null &&
      REQUEST_ID.test(candidate) &&
      !RAW_IDEMPOTENCY_KEY_TEXT.test(candidate)
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

function report(onerror: GatewayHttpOptions["onerror"], error: unknown): void {
  const reported = error instanceof Error ? error : new Error("Non-Error direct API failure");
  try {
    onerror?.(reported);
  } catch {
    // Reporting must never change or disclose the client result.
  }
}

function catalogueSuccessResponse(
  value: unknown,
  context: CatalogueProblemContext,
  onerror: GatewayHttpOptions["onerror"],
): Response {
  let serialised: string;
  try {
    const candidate = JSON.stringify(value);
    if (candidate === undefined) throw new TypeError("Catalogue result is not JSON serialisable");
    serialised = candidate;
  } catch (error) {
    report(onerror, error);
    return problemResponse("internal_error", context, "The request could not be processed.");
  }
  if (new TextEncoder().encode(serialised).byteLength > MAX_JSON_RESPONSE_BYTES) {
    report(onerror, new Error("Catalogue application result exceeded the direct API byte limit"));
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
  readonly selection?: SelectionResolveApplication;
  readonly dataQuery?: DataQueryApplication;
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
  const needsSelection = enabledApiOperations.includes("selection.resolve");
  const needsDataQuery = enabledApiOperations.includes("data.query");
  if (needsDataQuery && !needsEvidence) {
    throw new TypeError(
      "data.query transport requires the exact linked evidence.inspect operation",
    );
  }
  if (needsEvidence && options.evidenceApplication === undefined) {
    throw new TypeError(
      "evidenceApplication is required when evidence.inspect is explicitly mounted",
    );
  }
  if (
    needsEvidence &&
    !isReconciledEvidenceInspectApplication(
      options.evidenceApplication as EvidenceInspectApplication,
    )
  ) {
    throw new TypeError(
      "evidence.inspect transport requires a ledger-linked reconciliation application",
    );
  }
  if (needsSelection && options.selectionApplication === undefined) {
    throw new TypeError(
      "selectionApplication is required when selection.resolve is explicitly mounted",
    );
  }
  if (needsDataQuery && options.dataQueryApplication === undefined) {
    throw new TypeError(
      "dataQueryApplication is required when data.query is explicitly mounted",
    );
  }
  if (
    needsDataQuery &&
    !isReconciledDataQueryApplication(
      options.dataQueryApplication as DataQueryApplication,
    )
  ) {
    throw new TypeError(
      "data.query transport requires a ledger-linked reconciliation application",
    );
  }
  if (
    needsDataQuery &&
    !haveExactlyLinkedReconciliationApplications(
      options.dataQueryApplication as DataQueryApplication,
      options.evidenceApplication as EvidenceInspectApplication,
    )
  ) {
    throw new TypeError(
      "data.query and evidence.inspect transports require the exact shared reconciliation index",
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
    ...(needsSelection
      ? { selection: options.selectionApplication as SelectionResolveApplication }
      : {}),
    ...(needsDataQuery
      ? { dataQuery: options.dataQueryApplication as DataQueryApplication }
      : {}),
  });
}

function isSelectionProblem(value: unknown): value is SelectionResolveProblem {
  return (
    typeof value === "object" &&
    value !== null &&
    !Array.isArray(value) &&
    (value as { readonly schema?: unknown }).schema ===
      "gis-ai-go.selection-resolve-problem.v1"
  );
}

export function createGatewayHttpHandler(
  options: GatewayHttpOptions,
): (request: Request) => Promise<Response> {
  const governedAssembly = options.governedCandidateAssembly;
  const governedBindings = governedAssembly === undefined
    ? undefined
    : governedCandidateAssemblyBindings(governedAssembly);
  if (governedBindings !== undefined) {
    if (
      options.snapshot !== governedBindings.snapshot ||
      options.enabledApiOperations !== undefined ||
      options.application !== undefined ||
      options.evidenceApplication !== undefined ||
      options.selectionApplication !== undefined ||
      options.dataQueryApplication !== undefined ||
      options.catalogueApplicationOptions !== undefined ||
      options.evidenceReadinessIntegrity !== undefined
    ) {
      throw new TypeError(
        "Governed candidate HTTP exposure cannot be combined with independent applications or activation",
      );
    }
  }
  const snapshot = governedBindings?.snapshot ?? options.snapshot;
  const allowedHosts = new Set(
    (options.allowedHosts ?? DEFAULT_ALLOWED_HOSTS).map((host) => host.toLowerCase()),
  );
  const allowedOrigins = new Set(options.allowedOrigins ?? DEFAULT_ALLOWED_ORIGINS);
  const openApiServerOrigin = options.openApiServerOrigin === undefined
    ? undefined
    : parsePublicHttpsOrigin(options.openApiServerOrigin);
  const enabledApiOperations = governedAssembly?.apiOperations ??
    options.enabledApiOperations ?? catalogueActivation.activeApiOperations;
  const openApiDocument = governedAssembly === undefined
    ? createCatalogueOpenApiDocument(enabledApiOperations)
    : createGovernedCandidateOpenApiDocument(
        enabledApiOperations,
        openApiServerOrigin?.origin,
      );
  const applications = governedBindings === undefined
    ? operationApplications(options, enabledApiOperations)
    : Object.freeze({
        catalogue: governedBindings.catalogueApplication,
        evidence: governedBindings.evidenceApplication,
        selection: governedBindings.selectionApplication,
        dataQuery: governedBindings.dataQueryApplication,
      });
  const enabled = new Set(enabledApiOperations);
  const createRequestId = options.createRequestId ?? (() => randomBytes(16).toString("hex"));
  const createTraceId = options.createTraceId ?? (() => randomBytes(16).toString("hex"));
  const createTraceParentId = options.createTraceParentId ??
    (() => randomBytes(8).toString("hex"));
  const evidenceReadinessIntegrity = options.evidenceReadinessIntegrity;
  const onerror = options.onerror;

  if (allowedHosts.size === 0 || allowedOrigins.size === 0) {
    throw new TypeError("The gateway requires explicit allowed hosts and origins");
  }
  if (
    [...allowedHosts].some((host) => host === "") ||
    [...allowedOrigins].some((origin) => origin === "")
  ) {
    throw new TypeError("Allowed hosts and origins must not contain empty values");
  }
  if (openApiServerOrigin !== undefined) {
    const expectedHosts = new Set([
      openApiServerOrigin.hostname,
      `${openApiServerOrigin.hostname}:443`,
    ]);
    if (
      governedAssembly === undefined ||
      allowedHosts.size !== expectedHosts.size ||
      [...expectedHosts].some((host) => !allowedHosts.has(host)) ||
      allowedOrigins.size !== 1 ||
      !allowedOrigins.has(openApiServerOrigin.origin)
    ) {
      throw new TypeError(
        "The public OpenAPI origin must match the exact direct Host and Origin boundary",
      );
    }
  }
  if (onerror !== undefined && typeof onerror !== "function") {
    throw new TypeError("onerror must be a function");
  }
  if (evidenceReadinessIntegrity !== undefined) {
    try {
      verifyEvidenceReadinessIntegrity(evidenceReadinessIntegrity);
    } catch {
      throw new TypeError("evidenceReadinessIntegrity must be a verified evidence pair");
    }
  }
  if (
    options.createRequestId !== undefined &&
    typeof options.createRequestId !== "function"
  ) {
    throw new TypeError("createRequestId must be a function");
  }
  for (const [name, value] of [
    ["createTraceId", options.createTraceId],
    ["createTraceParentId", options.createTraceParentId],
  ] as const) {
    if (value !== undefined && typeof value !== "function") {
      throw new TypeError(`${name} must be a function`);
    }
  }

  return async (request: Request): Promise<Response> => {
    const traceId = createTraceId();
    if (!TRACE_ID.test(traceId)) {
      throw new TypeError("Trace identifiers must be 16-byte lowercase hexadecimal values");
    }
    const trace = normaliseW3CTraceContext(
      {
        traceparent: `00-${traceId}-${createTraceParentId()}-02`,
      },
      traceId,
    );
    const parsedUrl = new URL(request.url);
    const generatedRequestId = parsedUrl.pathname === "/data/query"
      ? createRequestId()
      : requestId(request);
    if (
      !REQUEST_ID.test(generatedRequestId) ||
      RAW_IDEMPOTENCY_KEY_TEXT.test(generatedRequestId)
    ) {
      throw new TypeError(
        "Generated request identifiers must match the catalogue problem contract",
      );
    }
    const context: CatalogueProblemContext = {
      requestId: generatedRequestId,
      traceId,
      trace,
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
              lifecycle: governedAssembly?.state ?? gatewayMetadata.lifecycle,
              ...(governedAssembly === undefined
                ? {}
                : { production_registration: false }),
              catalogue: catalogueIdentity(snapshot),
            },
            200,
          );
        case "/readyz":
          if (governedAssembly !== undefined) {
            const readiness = assessGovernedCandidateReadiness(governedAssembly);
            if (readiness.reason === "evidence-integrity-failed") {
              report(onerror, new Error(EVIDENCE_READINESS_INTEGRITY_FAILURE_MESSAGE));
            }
            return jsonResponse(
              {
                status: readiness.status,
                reason: readiness.reason,
                production_registration: readiness.productionRegistration,
                active_tools: readiness.activeTools,
                active_api_operations: readiness.activeApiOperations,
              },
              readiness.status === "ready" ? 200 : 503,
            );
          }
          if (evidenceReadinessIntegrity !== undefined) {
            try {
              verifyEvidenceReadinessIntegrity(evidenceReadinessIntegrity);
            } catch {
              report(
                onerror,
                new Error(EVIDENCE_READINESS_INTEGRITY_FAILURE_MESSAGE),
              );
            }
          }
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
          : parsedUrl.pathname === "/selection/resolve"
            ? "selection.resolve"
            : parsedUrl.pathname === "/data/query"
              ? "data.query"
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
      report(onerror, error);
      return problemResponse("internal_error", context, "The request could not be processed.");
    }
    if (governedAssembly !== undefined) {
      try {
        verifyGovernedCandidateOperation(governedAssembly, operation);
      } catch {
        return problemResponse(
          "service_unavailable",
          context,
          "The governed candidate dependencies are not ready.",
        );
      }
    }

    try {
      const result = operation === "catalogue.search"
        ? (applications.catalogue as CatalogueApplication).search(body, context)
        : operation === "catalogue.describe"
          ? (applications.catalogue as CatalogueApplication).describe(body, context)
          : operation === "evidence.inspect"
            ? (applications.evidence as EvidenceInspectApplication).inspect(body, context)
            : operation === "selection.resolve"
              ? (applications.selection as SelectionResolveApplication).resolve(body, context)
              : await (applications.dataQuery as DataQueryApplication).query(
                  body,
                  context,
                  { signal: request.signal },
                );
      if (operation === "selection.resolve" && isSelectionProblem(result)) {
        return jsonResponse(result, result.status, "application/problem+json");
      }
      return catalogueSuccessResponse(result, context, onerror);
    } catch (error) {
      if (isCatalogueProblemError(error)) {
        return jsonResponse(error.problem, error.problem.status, "application/problem+json");
      }
      if (error instanceof EvidenceInspectError) {
        return evidenceProblemResponse(error, context);
      }
      if (error instanceof DataQueryApplicationError) {
        return jsonResponse(
          error.problem,
          error.problem.status,
          "application/problem+json",
        );
      }
      report(onerror, error);
      return problemResponse("internal_error", context, "The request could not be processed.");
    }
  };
}

/** Create the direct face from one branded, candidate-unregistered assembly. */
export function createGovernedCandidateHttpHandler(
  assembly: GovernedCandidateAssembly,
  options: GovernedCandidateHttpOptions = {},
): (request: Request) => Promise<Response> {
  const exactOptions = snapshotGovernedCandidateOptions(
    options,
    [
      "allowedHosts",
      "allowedOrigins",
      "openApiServerOrigin",
      "createRequestId",
      "createTraceId",
      "createTraceParentId",
      "onerror",
    ],
    "Governed candidate HTTP options",
  ) as GovernedCandidateHttpOptions;
  const bindings = governedCandidateAssemblyBindings(assembly);
  const allowedHosts = exactOptions.allowedHosts === undefined
    ? undefined
    : snapshotGovernedCandidateStringArray(
        exactOptions.allowedHosts,
        "Governed candidate HTTP allowedHosts",
      );
  const allowedOrigins = exactOptions.allowedOrigins === undefined
    ? undefined
    : snapshotGovernedCandidateStringArray(
        exactOptions.allowedOrigins,
        "Governed candidate HTTP allowedOrigins",
      );
  return createGatewayHttpHandler({
    ...exactOptions,
    ...(allowedHosts === undefined ? {} : { allowedHosts }),
    ...(allowedOrigins === undefined ? {} : { allowedOrigins }),
    snapshot: bindings.snapshot,
    governedCandidateAssembly: assembly,
  });
}
