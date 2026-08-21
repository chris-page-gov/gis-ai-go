import assert from "node:assert/strict";
import { EventEmitter } from "node:events";
import { request as nodeRequest, type Server } from "node:http";
import { createConnection } from "node:net";
import { fileURLToPath } from "node:url";
import test from "node:test";

import {
  Client,
  StreamableHTTPClientTransport,
} from "@modelcontextprotocol/client";

import {
  createCatalogueApplication,
  type CatalogueApplication,
} from "../src/catalogue-application.js";
import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";
import { MAX_JSON_BODY_BYTES } from "../src/http-app.js";
import {
  createGatewayNodeServer,
  directRequestAbortBridge,
  MAX_MCP_JSON_BODY_BYTES,
  type GatewayNodeServer,
} from "../src/http-server.js";
import { MCP_PROTOCOL_VERSION } from "../src/mcp-server.js";

const snapshot = await loadCatalogueSnapshot(
  fileURLToPath(new URL("../../../../artifacts/okf/", import.meta.url)),
  { now: new Date("2026-08-20T12:00:00Z") },
);
const application = createCatalogueApplication(snapshot, {
  software: {
    name: "gis-ai-go-mcp-gateway",
    version: "0.1.0",
    revision: snapshot.revision,
  },
  now: () => new Date("2026-08-20T12:34:56Z"),
});

interface ReceivedResponse {
  readonly status: number;
  readonly headers: Readonly<Record<string, string | string[] | undefined>>;
  readonly body: string;
}

async function listen(server: Server): Promise<number> {
  await new Promise<void>((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", () => resolve());
  });
  const address = server.address();
  assert.ok(address !== null && typeof address === "object");
  return address.port;
}

async function close(server: Server): Promise<void> {
  await new Promise<void>((resolve, reject) => {
    server.close((error) => error === undefined ? resolve() : reject(error));
  });
}

function send(
  port: number,
  path: string,
  method: string,
  body?: string,
  headers: Readonly<Record<string, string | number>> = {},
): Promise<ReceivedResponse> {
  return new Promise((resolve, reject) => {
    const request = nodeRequest(
      {
        hostname: "127.0.0.1",
        port,
        path,
        method,
        headers: {
          host: "127.0.0.1:8787",
          ...(body === undefined ? {} : { "content-length": Buffer.byteLength(body) }),
          ...headers,
        },
      },
      (response) => {
        const chunks: Buffer[] = [];
        response.on("data", (chunk: Buffer) => chunks.push(chunk));
        response.on("end", () => {
          resolve({
            status: response.statusCode ?? 0,
            headers: response.headers,
            body: Buffer.concat(chunks).toString("utf8"),
          });
        });
      },
    );
    request.once("error", reject);
    request.end(body);
  });
}

function sendRaw(port: number, request: string): Promise<ReceivedResponse> {
  return new Promise((resolve, reject) => {
    const socket = createConnection({ host: "127.0.0.1", port });
    const chunks: Buffer[] = [];
    const timeout = setTimeout(() => {
      socket.destroy();
      reject(new Error("A raw HTTP request did not close promptly"));
    }, 1_000);
    socket.once("connect", () => socket.end(request));
    socket.on("data", (chunk: Buffer) => chunks.push(chunk));
    socket.once("error", (error) => {
      clearTimeout(timeout);
      reject(error);
    });
    socket.once("close", () => {
      clearTimeout(timeout);
      const response = Buffer.concat(chunks).toString("utf8");
      const separator = response.indexOf("\r\n\r\n");
      assert.notEqual(separator, -1);
      const lines = response.slice(0, separator).split("\r\n");
      const statusMatch = /^HTTP\/1\.1 (\d{3}) /u.exec(lines.shift() ?? "");
      assert.notEqual(statusMatch, null);
      const headers: Record<string, string> = {};
      for (const line of lines) {
        const colon = line.indexOf(":");
        assert.ok(colon > 0);
        headers[line.slice(0, colon).toLowerCase()] = line.slice(colon + 1).trim();
      }
      resolve({
        status: Number(statusMatch?.[1]),
        headers,
        body: response.slice(separator + 4),
      });
    });
  });
}

function sendStalledRejected(
  port: number,
  headers: Readonly<Record<string, string | number>>,
): Promise<ReceivedResponse> {
  return new Promise((resolve, reject) => {
    let settled = false;
    const request = nodeRequest(
      {
        hostname: "127.0.0.1",
        port,
        path: "/mcp",
        method: "POST",
        headers: {
          host: "127.0.0.1:8787",
          ...headers,
        },
      },
      (response) => {
        const chunks: Buffer[] = [];
        response.on("data", (chunk: Buffer) => chunks.push(chunk));
        response.on("end", () => {
          if (settled) return;
          settled = true;
          clearTimeout(timeout);
          request.destroy();
          resolve({
            status: response.statusCode ?? 0,
            headers: response.headers,
            body: Buffer.concat(chunks).toString("utf8"),
          });
        });
      },
    );
    request.on("error", (error) => {
      if (!settled) {
        settled = true;
        clearTimeout(timeout);
        reject(error);
      }
    });
    const timeout = setTimeout(() => {
      if (settled) return;
      settled = true;
      request.destroy();
      reject(new Error("A pre-body rejection did not close promptly"));
    }, 1_000);
    request.write("{");
  });
}

function modernBody(
  id: number,
  method: string,
  parameters: Readonly<Record<string, unknown>> = {},
): string {
  return JSON.stringify({
    jsonrpc: "2.0",
    id,
    method,
    params: {
      _meta: {
        "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
        "io.modelcontextprotocol/clientCapabilities": {},
        "io.modelcontextprotocol/clientInfo": {
          name: "gis-ai-go-node-test",
          version: "1.0.0",
        },
      },
      ...parameters,
    },
  });
}

function mcpHeaders(method: string, name?: string): Readonly<Record<string, string>> {
  return {
    accept: "application/json, text/event-stream",
    "content-type": "application/json",
    "mcp-protocol-version": MCP_PROTOCOL_VERSION,
    "mcp-method": method,
    ...(name === undefined ? {} : { "mcp-name": name }),
  };
}

function jsonObject(response: ReceivedResponse): Record<string, unknown> {
  return JSON.parse(response.body) as Record<string, unknown>;
}

function mcpToolResult(response: ReceivedResponse): Record<string, unknown> {
  const message = jsonObject(response);
  const result = message.result;
  assert.equal(typeof result, "object");
  assert.notEqual(result, null);
  return result as Record<string, unknown>;
}

function parityServer(app: CatalogueApplication): GatewayNodeServer {
  return createGatewayNodeServer(snapshot, {
    application: app,
    enabledApiOperations: ["catalogue.describe", "catalogue.search"],
    enabledMcpOperations: ["catalogue.describe", "catalogue.search"],
    enabledMcpResources: ["catalogue.public", "catalogue.record"],
    createTraceId: () => "1".repeat(32),
    createMcpRequestContext: () => ({
      requestId: "transport-parity-request",
      traceId: "1".repeat(32),
      instance: "/catalogue/search",
    }),
  });
}

async function wait(milliseconds: number): Promise<void> {
  await new Promise<void>((resolve) => setTimeout(resolve, milliseconds));
}

test("bridges already-destroyed Node state without treating a complete body as cancellation", () => {
  const request = Object.assign(new EventEmitter(), {
    aborted: false,
    complete: true,
    destroyed: false,
  });
  const response = Object.assign(new EventEmitter(), {
    destroyed: false,
    writableEnded: false,
  });
  const bridge = directRequestAbortBridge(request, response);
  assert.equal(bridge.signal.aborted, false);
  request.emit("aborted");
  assert.equal(bridge.signal.aborted, true);
  bridge.close();
  assert.equal(request.listenerCount("aborted"), 0);
  assert.equal(response.listenerCount("close"), 0);

  const alreadyDestroyedRequest = Object.assign(new EventEmitter(), {
    aborted: false,
    complete: true,
    destroyed: true,
  });
  const openResponse = Object.assign(new EventEmitter(), {
    destroyed: false,
    writableEnded: false,
  });
  const destroyedRequestBridge = directRequestAbortBridge(
    alreadyDestroyedRequest,
    openResponse,
  );
  assert.equal(destroyedRequestBridge.signal.aborted, true);
  destroyedRequestBridge.close();

  const healthyRequest = Object.assign(new EventEmitter(), {
    aborted: false,
    complete: true,
    destroyed: false,
  });
  const alreadyDestroyedResponse = Object.assign(new EventEmitter(), {
    destroyed: true,
    writableEnded: false,
  });
  const destroyedResponseBridge = directRequestAbortBridge(
    healthyRequest,
    alreadyDestroyedResponse,
  );
  assert.equal(destroyedResponseBridge.signal.aborted, true);
  destroyedResponseBridge.close();

  const completedResponse = Object.assign(new EventEmitter(), {
    destroyed: false,
    writableEnded: true,
  });
  const completedBridge = directRequestAbortBridge(healthyRequest, completedResponse);
  completedResponse.emit("close");
  assert.equal(completedBridge.signal.aborted, false);
  completedBridge.close();

  const openResponseBeforeClose = Object.assign(new EventEmitter(), {
    destroyed: false,
    writableEnded: false,
  });
  const openBridge = directRequestAbortBridge(healthyRequest, openResponseBeforeClose);
  openResponseBeforeClose.emit("close");
  assert.equal(openBridge.signal.aborted, true);
  openBridge.close();
});

test("keeps the mounted Node transport blocked by default", async () => {
  const server = createGatewayNodeServer(snapshot);
  const port = await listen(server);
  try {
    const discovery = await send(
      port,
      "/mcp",
      "POST",
      modernBody(1, "server/discover"),
      mcpHeaders("server/discover"),
    );
    assert.equal(discovery.status, 200);
    const result = jsonObject(discovery).result as Record<string, unknown>;
    assert.deepEqual(result.capabilities, {});

    const direct = await send(
      port,
      "/catalogue/search",
      "POST",
      "{}",
      { accept: "application/json", "content-type": "application/json" },
    );
    assert.equal(direct.status, 400);
    assert.equal(jsonObject(direct).code, "invalid_request");
  } finally {
    await close(server);
  }
});

test("returns byte-equivalent direct and MCP success envelopes", async () => {
  const server = parityServer(application);
  const port = await listen(server);
  const argumentsValue = { query: "Price Paid", limit: 1 };
  try {
    const direct = await send(
      port,
      "/catalogue/search",
      "POST",
      JSON.stringify(argumentsValue),
      {
        accept: "application/json",
        "content-type": "application/json",
        "x-request-id": "transport-parity-request",
      },
    );
    assert.equal(direct.status, 200);
    const directResult = jsonObject(direct);

    const mcp = await send(
      port,
      "/mcp",
      "POST",
      modernBody(2, "tools/call", {
        name: "catalogue.search",
        arguments: argumentsValue,
      }),
      mcpHeaders("tools/call", "catalogue.search"),
    );
    assert.equal(mcp.status, 200);
    const toolResult = mcpToolResult(mcp);
    assert.deepEqual(toolResult.structuredContent, directResult);
    assert.equal(
      (toolResult.content as Record<string, unknown>[])[0]?.text,
      JSON.stringify(directResult),
    );
  } finally {
    await close(server);
  }
});

test("serves the pinned official client through the real Node HTTP adapter", async () => {
  const server = parityServer(application);
  const port = await listen(server);
  const transport = new StreamableHTTPClientTransport(
    new URL(`http://127.0.0.1:${port}/mcp`),
  );
  const client = new Client(
    { name: "gis-ai-go-node-client", version: "1.0.0" },
    {
      capabilities: {},
      versionNegotiation: { mode: { pin: MCP_PROTOCOL_VERSION } },
    },
  );
  try {
    await client.connect(transport);
    assert.deepEqual(
      (await client.listTools()).tools.map((tool) => tool.name),
      ["catalogue.describe", "catalogue.search"],
    );
    const called = await client.callTool({
      name: "catalogue.search",
      arguments: { query: "Price Paid", limit: 1 },
    });
    assert.equal(
      (called.structuredContent as Record<string, unknown>).operation,
      "catalogue.search",
    );
    const resources = await client.listResources();
    assert.deepEqual(
      resources.resources.map((resource) => resource.uri),
      ["gis-ai-go://catalogue/public"],
    );
  } finally {
    await client.close();
    await server.closeGateway();
  }
});

test("returns the same canonical invalid-input problem over both faces", async () => {
  const server = parityServer(application);
  const port = await listen(server);
  const invalid = { unexpected: true };
  try {
    const direct = await send(
      port,
      "/catalogue/search",
      "POST",
      JSON.stringify(invalid),
      {
        accept: "application/json",
        "content-type": "application/json",
        "x-request-id": "transport-parity-request",
      },
    );
    assert.equal(direct.status, 400);
    const directProblem = jsonObject(direct);

    const mcp = await send(
      port,
      "/mcp",
      "POST",
      modernBody(3, "tools/call", {
        name: "catalogue.search",
        arguments: invalid,
      }),
      mcpHeaders("tools/call", "catalogue.search"),
    );
    assert.equal(mcp.status, 200);
    const toolResult = mcpToolResult(mcp);
    assert.equal(toolResult.isError, true);
    assert.deepEqual(toolResult.structuredContent, directProblem);
    assert.equal(
      (toolResult.content as Record<string, unknown>[])[0]?.text,
      JSON.stringify(directProblem),
    );

    const oversizedDirect = await send(
      port,
      "/catalogue/search",
      "POST",
      "x".repeat(MAX_JSON_BODY_BYTES + 1),
      {
        accept: "application/json",
        "content-type": "application/json",
        "x-request-id": "transport-parity-request",
      },
    );
    assert.equal(oversizedDirect.status, 400);
    assert.match(
      String(oversizedDirect.headers["content-type"]),
      /^application\/problem\+json/u,
    );
    assert.equal(oversizedDirect.headers.connection, "close");
    assert.equal(jsonObject(oversizedDirect).code, "invalid_request");

    const oversizedHealth = await send(
      port,
      "/healthz",
      "GET",
      "x".repeat(MAX_JSON_BODY_BYTES + 1),
      { accept: "application/json" },
    );
    assert.equal(oversizedHealth.status, 400);
    assert.match(
      String(oversizedHealth.headers["content-type"]),
      /^application\/problem\+json/u,
    );
    assert.equal(oversizedHealth.headers.connection, "close");
    assert.equal(jsonObject(oversizedHealth).code, "invalid_request");
  } finally {
    await close(server);
  }
});

test("enforces MCP ingress headers, framing and byte bounds before dispatch", async () => {
  const server = parityServer(application);
  const port = await listen(server);
  try {
    const missingVersion = await send(
      port,
      "/mcp",
      "POST",
      modernBody(4, "server/discover"),
      {
        accept: "application/json, text/event-stream",
        "content-type": "application/json",
        "mcp-method": "server/discover",
      },
    );
    assert.equal(missingVersion.status, 400);
    assert.equal(
      (jsonObject(missingVersion).error as Record<string, unknown>).code,
      -32_020,
    );

    const badHost = await send(
      port,
      "/mcp",
      "POST",
      modernBody(5, "server/discover"),
      { ...mcpHeaders("server/discover"), host: "attacker.invalid" },
    );
    assert.equal(badHost.status, 403);

    const wrongLoopbackOrigin = await send(
      port,
      "/mcp",
      "POST",
      modernBody(50, "server/discover"),
      {
        ...mcpHeaders("server/discover"),
        origin: "https://localhost:9999",
      },
    );
    assert.equal(wrongLoopbackOrigin.status, 403);
    assert.equal(wrongLoopbackOrigin.headers["cache-control"], "no-store");

    const stalledWrongOrigin = await sendStalledRejected(port, {
      ...mcpHeaders("server/discover"),
      "content-length": 100,
      origin: "https://localhost:9999",
    });
    assert.equal(stalledWrongOrigin.status, 403);
    assert.equal(stalledWrongOrigin.headers.connection, "close");
    assert.equal(stalledWrongOrigin.headers["cache-control"], "no-store");
    assert.equal(stalledWrongOrigin.headers["x-content-type-options"], "nosniff");

    const stalledTransferEncoding = await sendStalledRejected(port, {
      ...mcpHeaders("server/discover"),
      "transfer-encoding": "chunked",
    });
    assert.equal(stalledTransferEncoding.status, 400);
    assert.equal(stalledTransferEncoding.headers.connection, "close");

    const duplicateJson = modernBody(6, "server/discover").replace(
      '"jsonrpc":"2.0"',
      '"jsonrpc":"2.0","jsonrpc":"2.0"',
    );
    const duplicate = await send(
      port,
      "/mcp",
      "POST",
      duplicateJson,
      mcpHeaders("server/discover"),
    );
    assert.equal(duplicate.status, 400);
    assert.equal((jsonObject(duplicate).error as Record<string, unknown>).code, -32_700);

    const oversized = await send(
      port,
      "/mcp",
      "POST",
      "x".repeat(MAX_MCP_JSON_BODY_BYTES + 1),
      mcpHeaders("server/discover"),
    );
    assert.equal(oversized.status, 413);
    assert.equal((jsonObject(oversized).error as Record<string, unknown>).code, -32_000);
    assert.equal(oversized.headers.connection, "close");

    for (const path of ["/x/%2e%2e/healthz", "/mcp/%2e%2e/mcp"]) {
      const aliased = await send(port, path, "GET");
      assert.equal(aliased.status, 400);
      assert.equal(aliased.headers.connection, "close");
    }

    const fillerHeaders = Array.from(
      { length: 64 },
      (_, index) => `X-Filler-${index.toString().padStart(2, "0")}: value`,
    );
    const hiddenTransferEncoding = await sendRaw(
      port,
      [
        "POST /mcp HTTP/1.1",
        "Host: 127.0.0.1:8787",
        ...fillerHeaders,
        "Transfer-Encoding: chunked",
        "",
        "1",
        "{",
        "0",
        "",
        "",
      ].join("\r\n"),
    );
    assert.equal(hiddenTransferEncoding.status, 431);
    assert.equal(hiddenTransferEncoding.headers.connection, "close");

    for (const method of ["TRACE", "TRACK"]) {
      const directMethod = await send(port, "/healthz", method);
      assert.equal(directMethod.status, 400);
      if (method === "TRACE") {
        assert.equal(jsonObject(directMethod).code, "invalid_request");
      } else {
        assert.equal(directMethod.body, "");
        assert.equal(directMethod.headers.connection, "close");
      }

      const mcpMethod = await send(
        port,
        "/mcp",
        method,
        undefined,
        mcpHeaders("server/discover"),
      );
      if (method === "TRACE") {
        assert.equal(mcpMethod.status, 405);
        assert.equal(
          (jsonObject(mcpMethod).error as Record<string, unknown>).code,
          -32_000,
        );
      } else {
        assert.equal(mcpMethod.status, 400);
        assert.equal(mcpMethod.body, "");
        assert.equal(mcpMethod.headers.connection, "close");
      }
    }

    const oversizedTrace = await send(
      port,
      "/healthz",
      "TRACE",
      "x".repeat(MAX_JSON_BODY_BYTES + 1),
    );
    assert.equal(oversizedTrace.status, 400);
    assert.equal(oversizedTrace.headers.connection, "close");
    assert.equal(jsonObject(oversizedTrace).code, "invalid_request");
  } finally {
    await close(server);
  }
});

test("bounds concurrent admission and recovers after an abandoned request", async () => {
  const server = createGatewayNodeServer(snapshot, {
    application,
    enabledMcpOperations: ["catalogue.search"],
    maxConcurrentRequests: 1,
  });
  const port = await listen(server);
  const stalled = nodeRequest({
    hostname: "127.0.0.1",
    port,
    path: "/mcp",
    method: "POST",
    headers: {
      host: "127.0.0.1:8787",
      ...mcpHeaders("server/discover"),
      "content-length": 100,
    },
  });
  stalled.on("error", () => undefined);
  stalled.write("{");
  await wait(25);
  try {
    const directLimited = await send(
      port,
      "/catalogue/search",
      "POST",
      "{}",
      { accept: "application/json", "content-type": "application/json" },
    );
    assert.equal(directLimited.status, 429);
    assert.equal(directLimited.headers["retry-after"], "1");
    assert.equal(jsonObject(directLimited).code, "rate_limited");

    const limited = await send(
      port,
      "/mcp",
      "POST",
      modernBody(7, "server/discover"),
      mcpHeaders("server/discover"),
    );
    assert.equal(limited.status, 429);
    assert.equal(limited.headers["retry-after"], "1");
    assert.equal((jsonObject(limited).error as Record<string, unknown>).code, -32_000);

    stalled.destroy();
    let recovered: ReceivedResponse | undefined;
    for (let attempt = 0; attempt < 20; attempt += 1) {
      await wait(10);
      recovered = await send(
        port,
        "/mcp",
        "POST",
        modernBody(8, "server/discover"),
        mcpHeaders("server/discover"),
      );
      if (recovered.status !== 429) break;
    }
    assert.equal(recovered?.status, 200);
  } finally {
    stalled.destroy();
    await close(server);
  }
});

test("provides an idempotent MCP-first gateway shutdown", async () => {
  const server = createGatewayNodeServer(snapshot);
  assert.equal(
    (server as unknown as { connectionsCheckingInterval: number })
      .connectionsCheckingInterval,
    1_000,
  );
  assert.equal(server.headersTimeout, 5_000);
  assert.equal(server.requestTimeout, 5_000);
  assert.equal(server.timeout, 25_000);
  assert.equal(server.keepAliveTimeout, 5_000);
  await listen(server);
  await server.closeGateway();
  await server.closeGateway();
  assert.equal(server.listening, false);
});
