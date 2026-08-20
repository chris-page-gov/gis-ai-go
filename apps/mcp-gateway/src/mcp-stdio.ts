import {
  serializeMessage,
  type JSONRPCMessage,
  type RequestId,
  type Transport,
  type TransportSendOptions,
} from "@modelcontextprotocol/server";
import {
  StdioServerTransport,
  serveStdio,
  type StdioServerHandle,
} from "@modelcontextprotocol/server/stdio";

import {
  createCatalogueMcpServerFactory,
  isBoundedMcpRequestId,
  type CatalogueMcpOptions,
} from "./mcp-server.js";

export const MCP_STDIO_MAX_FRAME_BYTES = 1_048_576;
export const MCP_STDIO_MAX_BUFFER_BYTES = MCP_STDIO_MAX_FRAME_BYTES;
export const MCP_STDIO_MAX_METHOD_CODE_POINTS = 128;
export const MCP_STDIO_MAX_NAME_CODE_POINTS = 128;
export const MCP_STDIO_MAX_RESOURCE_URI_CODE_POINTS = 2_048;

const INVALID_REQUEST = -32_600;
const INVALID_PARAMS = -32_602;
const INTERNAL_ERROR = -32_603;
const CONTROL_CHARACTER = /[\u0000-\u001f\u007f]/u;

type TransportMessageExtra = Parameters<NonNullable<Transport["onmessage"]>>[1];

export interface CatalogueMcpStdioOptions extends CatalogueMcpOptions {
  /** Test or embedding seam. Omission uses the current process's stdio. */
  readonly transport?: Transport;
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value) as unknown;
  return prototype === Object.prototype || prototype === null;
}

function isBoundedField(value: unknown, maximumCodePoints: number): value is string {
  return (
    typeof value === "string" &&
    Array.from(value).length >= 1 &&
    Array.from(value).length <= maximumCodePoints &&
    !CONTROL_CHARACTER.test(value)
  );
}

function requestError(
  id: RequestId | null,
  code: number,
  message: string,
  reason: string,
  field?: string,
): JSONRPCMessage {
  const response = {
    jsonrpc: "2.0",
    id,
    error: {
      code,
      message,
      data: {
        reason,
        ...(field === undefined ? {} : { field }),
      },
    },
  };
  return response as unknown as JSONRPCMessage;
}

function ingressRejection(message: JSONRPCMessage): JSONRPCMessage | undefined {
  if (!isPlainObject(message)) return undefined;
  const candidate = message as unknown as Record<string, unknown>;
  if (
    candidate.jsonrpc !== "2.0" ||
    typeof candidate.method !== "string" ||
    !Object.hasOwn(candidate, "id")
  ) {
    return undefined;
  }
  if (!isBoundedMcpRequestId(candidate.id)) {
    return requestError(
      null,
      INVALID_REQUEST,
      "Invalid Request",
      "invalid_request_id",
    );
  }
  if (!isBoundedField(candidate.method, MCP_STDIO_MAX_METHOD_CODE_POINTS)) {
    return requestError(
      candidate.id,
      INVALID_REQUEST,
      "Invalid Request",
      "request_field_out_of_bounds",
      "method",
    );
  }
  if (!isPlainObject(candidate.params)) return undefined;
  const params = candidate.params;
  if (
    Object.hasOwn(params, "uri") &&
    !isBoundedField(params.uri, MCP_STDIO_MAX_RESOURCE_URI_CODE_POINTS)
  ) {
    return requestError(
      candidate.id,
      INVALID_PARAMS,
      "Invalid params",
      "request_field_out_of_bounds",
      "params.uri",
    );
  }
  if (
    Object.hasOwn(params, "name") &&
    !isBoundedField(params.name, MCP_STDIO_MAX_NAME_CODE_POINTS)
  ) {
    return requestError(
      candidate.id,
      INVALID_PARAMS,
      "Invalid params",
      "request_field_out_of_bounds",
      "params.name",
    );
  }
  return undefined;
}

function responseId(message: JSONRPCMessage): RequestId | null {
  if (
    ("result" in message || "error" in message) &&
    isBoundedMcpRequestId(message.id)
  ) {
    return message.id;
  }
  return null;
}

function frameBytes(message: JSONRPCMessage): number {
  return Buffer.byteLength(serializeMessage(message), "utf8");
}

/**
 * Guard the shared STDIO channel before SDK dispatch and immediately before
 * every stdout write. No single emitted JSON-RPC frame may exceed 1 MiB.
 */
class BoundedStdioTransport implements Transport {
  public onclose?: () => void;
  public onerror?: (error: Error) => void;
  public onmessage?: NonNullable<Transport["onmessage"]>;

  public constructor(private readonly inner: Transport) {}

  public get sessionId(): string | undefined {
    return this.inner.sessionId;
  }

  public set sessionId(value: string | undefined) {
    this.inner.sessionId = value;
  }

  public setProtocolVersion(version: string): void {
    this.inner.setProtocolVersion?.(version);
  }

  public setSupportedProtocolVersions(versions: string[]): void {
    this.inner.setSupportedProtocolVersions?.(versions);
  }

  public async start(): Promise<void> {
    this.inner.onmessage = (message, extra) => {
      this.receive(message, extra);
    };
    this.inner.onerror = (error) => {
      this.onerror?.(error);
    };
    this.inner.onclose = () => {
      this.onclose?.();
    };
    await this.inner.start();
  }

  public async send(
    message: JSONRPCMessage,
    options?: TransportSendOptions,
  ): Promise<void> {
    let withinBound = false;
    try {
      withinBound = frameBytes(message) <= MCP_STDIO_MAX_FRAME_BYTES;
    } catch {
      // A non-serialisable SDK result follows the same fixed failure path.
    }
    if (withinBound) {
      await this.inner.send(message, options);
      return;
    }
    this.onerror?.(new Error("MCP STDIO response exceeded its encoded frame bound"));
    const fallback = requestError(
      responseId(message),
      INTERNAL_ERROR,
      "Internal error",
      "response_too_large",
    );
    if (frameBytes(fallback) > MCP_STDIO_MAX_FRAME_BYTES) {
      throw new RangeError("MCP STDIO fixed overflow response exceeds its frame bound");
    }
    await this.inner.send(fallback, options);
  }

  public async close(): Promise<void> {
    await this.inner.close();
  }

  private receive(message: JSONRPCMessage, extra?: TransportMessageExtra): void {
    const rejection = ingressRejection(message);
    if (rejection === undefined) {
      this.onmessage?.(message, extra);
      return;
    }
    void this.send(rejection).catch((error: unknown) => {
      this.onerror?.(
        error instanceof Error ? error : new Error("MCP STDIO rejection write failed"),
      );
    });
  }
}

/** Start one strict modern-only MCP connection over bounded STDIO framing. */
export function startCatalogueStdio(
  options: CatalogueMcpStdioOptions,
): StdioServerHandle {
  const transport =
    options.transport ??
    new StdioServerTransport(undefined, undefined, {
      maxBufferSize: MCP_STDIO_MAX_BUFFER_BYTES,
    });
  return serveStdio(createCatalogueMcpServerFactory(options), {
    legacy: "reject",
    transport: new BoundedStdioTransport(transport),
    ...(options.onerror === undefined ? {} : { onerror: options.onerror }),
  });
}
