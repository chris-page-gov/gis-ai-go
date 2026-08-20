import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { once } from "node:events";
import { fileURLToPath } from "node:url";
import test from "node:test";

import {
  Client,
} from "@modelcontextprotocol/client";
import {
  StdioClientTransport,
} from "@modelcontextprotocol/client/stdio";
import {
  InMemoryTransport,
  type JSONRPCMessage,
} from "@modelcontextprotocol/server";

import { createCatalogueApplication } from "../src/catalogue-application.js";
import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";
import {
  MCP_CATALOGUE_OPERATIONS,
  MCP_CATALOGUE_RESOURCES,
  MCP_PROTOCOL_VERSION,
  MCP_PUBLIC_CATALOGUE_URI,
} from "../src/mcp-server.js";
import {
  MCP_STDIO_MAX_BUFFER_BYTES,
  startCatalogueStdio,
} from "../src/mcp-stdio.js";

const SOURCE_CATALOGUE = fileURLToPath(
  new URL("../../../../artifacts/okf/", import.meta.url),
);
const SNAPSHOT = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
  now: new Date("2026-08-20T12:00:00Z"),
});
const APPLICATION = createCatalogueApplication(SNAPSHOT, {
  software: {
    name: "gis-ai-go-mcp-gateway",
    version: "0.1.0",
    revision: "a".repeat(40),
  },
  now: () => new Date("2026-08-20T12:34:56Z"),
});
const META = {
  "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
  "io.modelcontextprotocol/clientCapabilities": {},
  "io.modelcontextprotocol/clientInfo": {
    name: "gis-ai-go-stdio-test-client",
    version: "1.0.0",
  },
};

function enabledSubprocessScript(): string {
  const applicationModule = new URL(
    "../src/catalogue-application.js",
    import.meta.url,
  ).href;
  const snapshotModule = new URL("../src/catalogue-snapshot.js", import.meta.url).href;
  const stdioModule = new URL("../src/mcp-stdio.js", import.meta.url).href;
  return [
    `import { createCatalogueApplication } from ${JSON.stringify(applicationModule)};`,
    `import { loadCatalogueSnapshot } from ${JSON.stringify(snapshotModule)};`,
    `import { startCatalogueStdio } from ${JSON.stringify(stdioModule)};`,
    "const snapshot = await loadCatalogueSnapshot(process.argv[1], { now: new Date('2026-08-20T12:00:00Z') });",
    "const application = createCatalogueApplication(snapshot, { software: { name: 'gis-ai-go-mcp-gateway', version: '0.1.0', revision: 'a'.repeat(40) }, now: () => new Date('2026-08-20T12:34:56Z') });",
    "startCatalogueStdio({ application, snapshot, enabledOperations: ['catalogue.describe', 'catalogue.search'], enabledResources: ['catalogue.public', 'catalogue.record'] });",
  ].join("\n");
}

async function subprocessExchange(
  args: readonly string[],
  frame: string,
): Promise<{
  readonly reply: Record<string, unknown>;
  readonly stdout: string;
  readonly stderr: string;
  readonly exitCode: number | null;
}> {
  const child = spawn(process.execPath, [...args], {
    stdio: ["pipe", "pipe", "pipe"],
  });
  child.stdout.setEncoding("utf8");
  child.stderr.setEncoding("utf8");
  let stdout = "";
  let stderr = "";
  let inspect = (): void => undefined;
  child.stdout.on("data", (chunk: string) => {
    stdout += chunk;
    inspect();
  });
  child.stderr.on("data", (chunk: string) => {
    stderr += chunk;
  });
  const exit = once(child, "exit");
  const reply = new Promise<Record<string, unknown>>((resolve, reject) => {
    const timer = setTimeout(
      () => reject(new Error("Timed out waiting for subprocess STDIO reply")),
      5_000,
    );
    inspect = (): void => {
      const newline = stdout.indexOf("\n");
      if (newline === -1) return;
      clearTimeout(timer);
      try {
        resolve(JSON.parse(stdout.slice(0, newline)) as Record<string, unknown>);
      } catch (error) {
        reject(error);
      }
    };
    child.once("error", (error) => {
      clearTimeout(timer);
      reject(error);
    });
    child.once("exit", () => {
      if (stdout.includes("\n")) return;
      clearTimeout(timer);
      reject(new Error(`STDIO subprocess exited without a reply: ${stderr}`));
    });
  });
  child.stdin.end(frame);
  try {
    const parsed = await reply;
    await exit;
    return { reply: parsed, stdout, stderr, exitCode: child.exitCode };
  } catch (error) {
    if (child.exitCode === null) child.kill("SIGTERM");
    await exit.catch(() => undefined);
    throw error;
  }
}

function nextMessage(transport: InMemoryTransport): Promise<JSONRPCMessage> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("Timed out waiting for STDIO reply")), 2_000);
    transport.onmessage = (message) => {
      clearTimeout(timer);
      resolve(message);
    };
  });
}

async function exchange(
  transport: InMemoryTransport,
  message: JSONRPCMessage,
): Promise<JSONRPCMessage> {
  const reply = nextMessage(transport);
  await transport.send(message);
  return reply;
}

test("serves a raw modern STDIO transcript through the same registered factory", async (t) => {
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const handle = startCatalogueStdio({
    application: APPLICATION,
    snapshot: SNAPSHOT,
    enabledOperations: MCP_CATALOGUE_OPERATIONS,
    enabledResources: MCP_CATALOGUE_RESOURCES,
    transport: serverTransport,
  });
  t.after(async () => {
    await handle.close();
    await clientTransport.close();
  });

  const discovery = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 1,
    method: "server/discover",
    params: { _meta: META },
  });
  assert.equal("result" in discovery, true);
  if (!("result" in discovery)) return;
  assert.deepEqual(discovery.result.supportedVersions, [MCP_PROTOCOL_VERSION]);
  assert.deepEqual(discovery.result.capabilities, {
    tools: { listChanged: false },
    resources: { listChanged: false, subscribe: false },
  });

  const listing = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 2,
    method: "tools/list",
    params: { _meta: META },
  });
  assert.equal("result" in listing, true);
  if (!("result" in listing)) return;
  const tools = listing.result.tools as { readonly name: string }[];
  assert.deepEqual(
    tools.map((tool) => tool.name),
    ["catalogue.describe", "catalogue.search"],
  );

  const called = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 3,
    method: "tools/call",
    params: {
      _meta: META,
      name: "catalogue.describe",
      arguments: { record_id: "LR-Q003" },
    },
  });
  assert.equal("result" in called, true);
  if (!("result" in called)) return;
  const structured = called.result.structuredContent as { operation?: unknown };
  const content = called.result.content as { type: string; text?: string }[];
  assert.equal(
    structured.operation,
    "catalogue.describe",
  );
  assert.equal(
    content[0]?.type === "text" && content[0].text !== undefined
      ? (JSON.parse(content[0].text) as { operation?: unknown }).operation
      : undefined,
    "catalogue.describe",
  );

  const resources = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 4,
    method: "resources/list",
    params: { _meta: META },
  });
  assert.equal("result" in resources, true);
  if (!("result" in resources)) return;
  assert.deepEqual(
    (resources.result.resources as { readonly uri: string }[]).map(
      (resource) => resource.uri,
    ),
    [MCP_PUBLIC_CATALOGUE_URI],
  );

  const read = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 5,
    method: "resources/read",
    params: { _meta: META, uri: MCP_PUBLIC_CATALOGUE_URI },
  });
  assert.equal("result" in read, true);
  if (!("result" in read)) return;
  const resourceContent = read.result.contents as { readonly text?: string }[];
  assert.equal(resourceContent[0]?.text, JSON.stringify(SNAPSHOT.bundle));
});

test("returns canonical structured problems for invalid STDIO tool arguments", async (t) => {
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const handle = startCatalogueStdio({
    application: APPLICATION,
    snapshot: SNAPSHOT,
    enabledOperations: MCP_CATALOGUE_OPERATIONS,
    transport: serverTransport,
  });
  t.after(async () => {
    await handle.close();
    await clientTransport.close();
  });

  const cases = [
    { id: 6, name: "catalogue.describe", arguments: {} },
    { id: 7, name: "catalogue.search", arguments: { unexpected: true } },
    { id: 8, name: "catalogue.search", arguments: { limit: "one" } },
  ] as const;
  for (const item of cases) {
    const reply = await exchange(clientTransport, {
      jsonrpc: "2.0",
      id: item.id,
      method: "tools/call",
      params: {
        _meta: META,
        name: item.name,
        arguments: item.arguments,
      },
    });
    assert.equal("result" in reply, true);
    if (!("result" in reply)) return;
    assert.equal(reply.result.isError, true);
    const structured = reply.result.structuredContent as {
      readonly schema?: unknown;
      readonly code?: unknown;
    };
    const content = reply.result.content as { readonly text?: string }[];
    assert.equal(structured.schema, "gis-ai-go.catalogue-problem.v1");
    assert.equal(structured.code, "invalid_request");
    assert.equal(content[0]?.text, JSON.stringify(structured));
    assert.equal(JSON.stringify(reply.result).includes("Input validation error"), false);
  }
});

test("rejects every unsafe STDIO request ID before application dispatch", async (t) => {
  let applicationCalls = 0;
  const countedApplication = {
    search: (...args: Parameters<typeof APPLICATION.search>) => {
      applicationCalls += 1;
      return APPLICATION.search(...args);
    },
    describe: (...args: Parameters<typeof APPLICATION.describe>) => {
      applicationCalls += 1;
      return APPLICATION.describe(...args);
    },
  };
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const handle = startCatalogueStdio({
    application: countedApplication,
    snapshot: SNAPSHOT,
    enabledOperations: MCP_CATALOGUE_OPERATIONS,
    transport: serverTransport,
  });
  t.after(async () => {
    await handle.close();
    await clientTransport.close();
  });

  const discovery = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 9,
    method: "server/discover",
    params: { _meta: META },
  });
  assert.equal("result" in discovery, true);
  for (const id of [
    "x".repeat(129),
    "unsafe\nid",
    Number.MAX_SAFE_INTEGER + 1,
  ] as const) {
    const reply = await exchange(clientTransport, {
      jsonrpc: "2.0",
      id,
      method: "tools/call",
      params: {
        _meta: META,
        name: "catalogue.search",
        arguments: {},
      },
    });
    assert.equal("error" in reply, true);
    if (!("error" in reply)) return;
    assert.equal(reply.id, null);
    assert.equal(reply.error.code, -32_600);
    assert.equal(reply.error.message, "Invalid Request");
    assert.deepEqual(reply.error.data, { reason: "invalid_request_id" });
    assert.ok(
      Buffer.byteLength(`${JSON.stringify(reply)}\n`) <= MCP_STDIO_MAX_BUFFER_BYTES,
    );
  }
  assert.equal(applicationCalls, 0);
});

test("rejects a legacy STDIO opening without pinning the connection to it", async (t) => {
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const handle = startCatalogueStdio({
    application: APPLICATION,
    snapshot: SNAPSHOT,
    enabledOperations: MCP_CATALOGUE_OPERATIONS,
    transport: serverTransport,
  });
  t.after(async () => {
    await handle.close();
    await clientTransport.close();
  });

  const legacy = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 10,
    method: "initialize",
    params: {
      protocolVersion: "2025-11-25",
      capabilities: {},
      clientInfo: { name: "legacy-test", version: "1.0.0" },
    },
  });
  assert.equal("error" in legacy, true);
  if (!("error" in legacy)) return;
  assert.equal(legacy.error.code, -32_022);

  const modern = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 11,
    method: "server/discover",
    params: { _meta: META },
  });
  assert.equal("result" in modern, true);
  if (!("result" in modern)) return;
  assert.deepEqual(modern.result.supportedVersions, [MCP_PROTOCOL_VERSION]);
});

test("bounds the process STDIO read buffer", () => {
  assert.equal(MCP_STDIO_MAX_BUFFER_BYTES, 1_048_576);
});

test("interoperates with the pinned official STDIO client in an enabled subprocess", async (t) => {
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [
      "--input-type=module",
      "--eval",
      enabledSubprocessScript(),
      SOURCE_CATALOGUE,
    ],
    stderr: "pipe",
    maxBufferSize: MCP_STDIO_MAX_BUFFER_BYTES,
  });
  let diagnostics = "";
  transport.stderr?.on("data", (chunk: unknown) => {
    diagnostics += String(chunk);
  });
  const client = new Client(
    { name: "gis-ai-go-official-stdio-test-client", version: "1.0.0" },
    {
      capabilities: {},
      versionNegotiation: { mode: { pin: MCP_PROTOCOL_VERSION } },
    },
  );
  let closed = false;
  t.after(async () => {
    if (!closed) await client.close().catch(() => undefined);
  });

  await client.connect(transport);
  assert.notEqual(transport.pid, null);
  assert.deepEqual(client.getServerCapabilities(), {
    tools: { listChanged: false },
    resources: { listChanged: false, subscribe: false },
  });
  assert.deepEqual(
    (await client.listTools()).tools.map((tool) => tool.name),
    ["catalogue.describe", "catalogue.search"],
  );
  assert.deepEqual(
    (await client.listResources()).resources.map((resource) => resource.uri),
    [MCP_PUBLIC_CATALOGUE_URI],
  );
  assert.deepEqual(
    (await client.listResourceTemplates()).resourceTemplates.map(
      (template) => template.uriTemplate,
    ),
    ["gis-ai-go://catalogue/records/{record_id}"],
  );
  const read = await client.readResource({ uri: MCP_PUBLIC_CATALOGUE_URI });
  const resourceContent = read.contents[0];
  assert.ok(resourceContent !== undefined && "text" in resourceContent);
  assert.equal(resourceContent.text, JSON.stringify(SNAPSHOT.bundle));
  const called = await client.callTool({
    name: "catalogue.describe",
    arguments: { record_id: "LR-Q003" },
  });
  const structured = called.structuredContent as { readonly operation?: unknown };
  assert.equal(structured.operation, "catalogue.describe");
  assert.equal(
    "text" in (called.content[0] ?? {})
      ? (called.content[0] as { readonly text: string }).text
      : undefined,
    JSON.stringify(called.structuredContent),
  );
  await client.close();
  closed = true;
  assert.equal(diagnostics, "");
});

test("bounds the reply to an exactly 1 MiB subprocess request with a huge ID", async () => {
  const executable = fileURLToPath(
    new URL("../src/mcp-stdio-main.js", import.meta.url),
  );
  const prefix = '{"jsonrpc":"2.0","id":"';
  const suffix = `","method":"server/discover","params":{"_meta":${JSON.stringify(META)}}}\n`;
  const idLength =
    MCP_STDIO_MAX_BUFFER_BYTES -
    Buffer.byteLength(prefix) -
    Buffer.byteLength(suffix);
  assert.ok(idLength > 128);
  const frame = `${prefix}${"x".repeat(idLength)}${suffix}`;
  assert.equal(Buffer.byteLength(frame), MCP_STDIO_MAX_BUFFER_BYTES);

  const exchangeResult = await subprocessExchange(
    [executable, SOURCE_CATALOGUE],
    frame,
  );
  const error = exchangeResult.reply.error as Record<string, unknown>;
  assert.equal(exchangeResult.reply.id, null);
  assert.equal(error.code, -32_600);
  assert.equal(error.message, "Invalid Request");
  assert.deepEqual(error.data, { reason: "invalid_request_id" });
  assert.ok(
    Buffer.byteLength(exchangeResult.stdout) <= MCP_STDIO_MAX_BUFFER_BYTES,
  );
  assert.equal(exchangeResult.stdout.trimEnd().split("\n").length, 1);
  assert.equal(exchangeResult.stderr, "");
  assert.equal(exchangeResult.exitCode, 0);
});

test("does not reflect an oversized resource URI from an enabled subprocess", async () => {
  const uriPrefix = "gis-ai-go://catalogue/records/";
  const uri = `${uriPrefix}${"x".repeat(999_999 - uriPrefix.length)}`;
  assert.equal(uri.length, 999_999);
  const frame = `${JSON.stringify({
    jsonrpc: "2.0",
    id: 21,
    method: "resources/read",
    params: { _meta: META, uri },
  })}\n`;
  assert.ok(Buffer.byteLength(frame) <= MCP_STDIO_MAX_BUFFER_BYTES);

  const exchangeResult = await subprocessExchange(
    [
      "--input-type=module",
      "--eval",
      enabledSubprocessScript(),
      SOURCE_CATALOGUE,
    ],
    frame,
  );
  const error = exchangeResult.reply.error as Record<string, unknown>;
  assert.equal(exchangeResult.reply.id, 21);
  assert.equal(error.code, -32_602);
  assert.equal(error.message, "Invalid params");
  assert.deepEqual(error.data, {
    reason: "request_field_out_of_bounds",
    field: "params.uri",
  });
  assert.ok(
    Buffer.byteLength(exchangeResult.stdout) <= MCP_STDIO_MAX_BUFFER_BYTES,
  );
  assert.equal(exchangeResult.stdout.includes(uri), false);
  assert.equal(exchangeResult.stdout.trimEnd().split("\n").length, 1);
  assert.equal(exchangeResult.stderr, "");
  assert.equal(exchangeResult.exitCode, 0);
});

test("keeps the executable stdout protocol-clean with frozen zero activation", async (t) => {
  const executable = fileURLToPath(
    new URL("../src/mcp-stdio-main.js", import.meta.url),
  );
  const child = spawn(process.execPath, [executable, SOURCE_CATALOGUE], {
    stdio: ["pipe", "pipe", "pipe"],
  });
  t.after(() => {
    if (child.exitCode === null) child.kill("SIGTERM");
  });
  child.stdout.setEncoding("utf8");
  child.stderr.setEncoding("utf8");
  let stdout = "";
  let stderr = "";
  child.stdout.on("data", (chunk: string) => {
    stdout += chunk;
  });
  child.stderr.on("data", (chunk: string) => {
    stderr += chunk;
  });
  child.stdin.write(
    `${JSON.stringify({
      jsonrpc: "2.0",
      id: 20,
      method: "server/discover",
      params: { _meta: META },
    })}\n`,
  );

  const reply = await new Promise<JSONRPCMessage>((resolve, reject) => {
    const timer = setTimeout(
      () => reject(new Error("Timed out waiting for executable STDIO reply")),
      4_000,
    );
    const inspect = (): void => {
      const newline = stdout.indexOf("\n");
      if (newline === -1) return;
      clearTimeout(timer);
      try {
        resolve(JSON.parse(stdout.slice(0, newline)) as JSONRPCMessage);
      } catch (error) {
        reject(error);
      }
    };
    child.stdout.on("data", inspect);
    child.once("error", (error) => {
      clearTimeout(timer);
      reject(error);
    });
    inspect();
  });
  assert.equal("result" in reply, true);
  if ("result" in reply) {
    assert.deepEqual(reply.result.capabilities, {});
    assert.deepEqual(reply.result.supportedVersions, [MCP_PROTOCOL_VERSION]);
  }
  assert.equal(stdout.trimEnd().split("\n").length, 1);
  assert.equal(stderr, "");
  child.stdin.end();
  await once(child, "exit");
  assert.equal(child.exitCode, 0);
});
