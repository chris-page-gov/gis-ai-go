import {
  PROTOCOL_VERSION_META_KEY,
  createMcpHandler,
  type JSONRPCRequest,
  type McpHttpHandler,
} from "@modelcontextprotocol/server";

import {
  MCP_PROTOCOL_VERSION,
  createCatalogueMcpServerFactory,
  isBoundedMcpRequestId,
  type CatalogueMcpOptions,
} from "./mcp-server.js";
import { withMcpHttpDataQuerySignal } from "./mcp-request-signal.js";
import { BoundedJsonError, parseBoundedJsonBytes } from "./http-app.js";

const HEADER_MISMATCH = -32_020;
const TRANSPORT_ERROR = -32_000;
const INVALID_REQUEST = -32_600;
const PARSE_ERROR = -32_700;
const REQUIRED_ACCEPT_TYPES = Object.freeze([
  "application/json",
  "text/event-stream",
] as const);

export const MCP_HTTP_MAX_STANDALONE_BODY_BYTES = 65_536;

function isPlainObject(value: unknown): value is Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value) as unknown;
  return prototype === Object.prototype || prototype === null;
}

function isModernRequest(value: unknown): value is JSONRPCRequest {
  if (!isPlainObject(value) || value.jsonrpc !== "2.0") return false;
  if (!Object.hasOwn(value, "id") || !isBoundedMcpRequestId(value.id)) return false;
  if (typeof value.method !== "string") return false;
  if (!isPlainObject(value.params) || !isPlainObject(value.params._meta)) return false;
  return value.params._meta[PROTOCOL_VERSION_META_KEY] === MCP_PROTOCOL_VERSION;
}

function missingVersionResponse(request: JSONRPCRequest): Response {
  const body = JSON.stringify({
    jsonrpc: "2.0",
    id: request.id,
    error: {
      code: HEADER_MISMATCH,
      message:
        "Bad Request: MCP-Protocol-Version header is required for protocol revision 2026-07-28",
      data: {
        reason: "missing_protocol_version_header",
        expected: MCP_PROTOCOL_VERSION,
      },
    },
  });
  return new Response(body, {
    status: 400,
    headers: {
      "cache-control": "no-store",
      "content-type": "application/json; charset=utf-8",
      "x-content-type-options": "nosniff",
    },
  });
}

function errorResponse(
  status: number,
  code: number,
  message: string,
  data: Readonly<Record<string, unknown>>,
): Response {
  return new Response(
    JSON.stringify({
      jsonrpc: "2.0",
      id: null,
      error: { code, message, data },
    }),
    {
      status,
      headers: {
        "cache-control": "no-store",
        "content-type": "application/json; charset=utf-8",
        "x-content-type-options": "nosniff",
      },
    },
  );
}

function positiveQuality(parameters: readonly string[]): boolean {
  const qualityParameters = parameters
    .map((parameter) => parameter.trim())
    .filter((parameter) => parameter.split("=", 1)[0]?.trim().toLowerCase() === "q");
  if (qualityParameters.length === 0) return true;
  if (qualityParameters.length !== 1) return false;
  const match = /^q\s*=\s*(0(?:\.\d{0,3})?|1(?:\.0{0,3})?)$/iu.exec(
    qualityParameters[0] as string,
  );
  return match !== null && Number(match[1]) > 0;
}

function hasRequiredAcceptTypes(header: string | null): boolean {
  if (header === null) return false;
  const accepted = new Set<string>();
  for (const entry of header.split(",")) {
    const [rawEssence, ...parameters] = entry.split(";");
    const essence = rawEssence?.trim().toLowerCase();
    if (
      essence !== undefined &&
      (REQUIRED_ACCEPT_TYPES as readonly string[]).includes(essence) &&
      positiveQuality(parameters)
    ) {
      accepted.add(essence);
    }
  }
  return REQUIRED_ACCEPT_TYPES.every((type) => accepted.has(type));
}

function rejectIncompleteAccept(request: Request): Response | undefined {
  if (request.method.toUpperCase() !== "POST") return undefined;
  if (hasRequiredAcceptTypes(request.headers.get("accept"))) return undefined;
  return errorResponse(
    406,
    TRANSPORT_ERROR,
    "Not Acceptable: Accept must include application/json and text/event-stream",
    {
      reason: "missing_required_accept_types",
      required: REQUIRED_ACCEPT_TYPES,
    },
  );
}

interface PreparedBody {
  readonly body: unknown;
  readonly response?: undefined;
}

interface PreparedBodyFailure {
  readonly body?: undefined;
  readonly response: Response;
}

async function prepareBody(
  request: Request,
  parsedBody: unknown,
): Promise<PreparedBody | PreparedBodyFailure> {
  if (parsedBody !== undefined || request.method.toUpperCase() !== "POST") {
    return { body: parsedBody };
  }
  const body = request.clone().body;
  if (body === null) return { body: undefined };
  const reader = body.getReader();
  const chunks: Uint8Array[] = [];
  let length = 0;
  try {
    while (true) {
      const item = await reader.read();
      if (item.done) break;
      if (item.value !== undefined) {
        length += item.value.byteLength;
        if (length > MCP_HTTP_MAX_STANDALONE_BODY_BYTES) {
          await reader.cancel();
          return {
            response: errorResponse(
              413,
              TRANSPORT_ERROR,
              "Request body too large",
              { reason: "request_body_too_large" },
            ),
          };
        }
        chunks.push(item.value);
      }
    }
  } catch {
    return {
      response: errorResponse(400, PARSE_ERROR, "Parse error", {
        reason: "malformed_json",
      }),
    };
  }
  if (length === 0) return { body: undefined };
  const bytes = new Uint8Array(length);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.byteLength;
  }
  try {
    return {
      body: parseBoundedJsonBytes(bytes, MCP_HTTP_MAX_STANDALONE_BODY_BYTES),
    };
  } catch (error) {
    if (!(error instanceof BoundedJsonError)) throw error;
    return {
      response: errorResponse(400, PARSE_ERROR, "Parse error", {
        reason: "malformed_json",
      }),
    };
  }
}

function rejectInvalidRequestId(body: unknown): Response | undefined {
  if (
    !isPlainObject(body) ||
    body.jsonrpc !== "2.0" ||
    !Object.hasOwn(body, "id") ||
    isBoundedMcpRequestId(body.id)
  ) {
    return undefined;
  }
  return errorResponse(400, INVALID_REQUEST, "Invalid Request: JSON-RPC id is invalid", {
    reason: "invalid_request_id",
  });
}

function rejectMissingModernProtocolHeader(
  request: Request,
  body: unknown,
): Response | undefined {
  if (
    request.method.toUpperCase() !== "POST" ||
    request.headers.get("mcp-protocol-version") !== null
  ) {
    return undefined;
  }
  return isModernRequest(body) ? missingVersionResponse(body) : undefined;
}

function isDataQueryCall(request: Request, body: unknown): boolean {
  if (
    request.method.toUpperCase() !== "POST" ||
    request.headers.get("mcp-protocol-version") !== MCP_PROTOCOL_VERSION ||
    request.headers.get("mcp-method") !== "tools/call" ||
    request.headers.get("mcp-name") !== "data.query" ||
    !isModernRequest(body) ||
    body.method !== "tools/call"
  ) {
    return false;
  }
  if (!isPlainObject(body.params) || body.params.name !== "data.query") return false;
  const meta = body.params._meta;
  if (!isPlainObject(meta)) return false;
  const clientCapabilities = meta["io.modelcontextprotocol/clientCapabilities"];
  const clientInfo = meta["io.modelcontextprotocol/clientInfo"];
  if (
    !isPlainObject(clientCapabilities) ||
    !isPlainObject(body.params.arguments)
  ) {
    return false;
  }
  if (
    clientInfo !== undefined &&
    (
      !isPlainObject(clientInfo) ||
      typeof clientInfo.name !== "string" ||
      clientInfo.name.length < 1 ||
      clientInfo.name.length > 128 ||
      typeof clientInfo.version !== "string" ||
      clientInfo.version.length < 1 ||
      clientInfo.version.length > 64
    )
  ) {
    return false;
  }
  return true;
}

/**
 * Create the modern-only fetch face. Host, Origin, route, body-size,
 * concurrency and timeout controls belong to the Node ingress that mounts it.
 */
export function createCatalogueMcpHttpHandler(
  options: CatalogueMcpOptions,
): McpHttpHandler {
  const handler = createMcpHandler(createCatalogueMcpServerFactory(options), {
    legacy: "reject",
    responseMode: "auto",
    ...(options.onerror === undefined ? {} : { onerror: options.onerror }),
  });
  return {
    ...handler,
    fetch: async (request, requestOptions) => {
      const unacceptable = rejectIncompleteAccept(request);
      if (unacceptable !== undefined) return unacceptable;
      const prepared = await prepareBody(request, requestOptions?.parsedBody);
      if (prepared.response !== undefined) return prepared.response;
      const invalidId = rejectInvalidRequestId(prepared.body);
      if (invalidId !== undefined) return invalidId;
      const guarded = rejectMissingModernProtocolHeader(request, prepared.body);
      if (guarded !== undefined) return guarded;
      const exactRequestOptions = prepared.body === undefined
        ? requestOptions
        : { ...requestOptions, parsedBody: prepared.body };
      if (!isDataQueryCall(request, prepared.body)) {
        return handler.fetch(request, exactRequestOptions);
      }
      /*
       * SDK 2.0.0 converts an aborted Fetch request into HTTP 499 even after
       * the tool has produced its closed query_cancelled result. Keep the
       * original signal for the application but isolate only this response
       * lifecycle so in-process conformance receives the canonical envelope.
       */
      const responseLifetime = new AbortController();
      const responseRequest = new Request(request, {
        signal: responseLifetime.signal,
      });
      return withMcpHttpDataQuerySignal(request.signal, () =>
        handler.fetch(responseRequest, exactRequestOptions));
    },
  };
}
