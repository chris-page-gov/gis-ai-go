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
  type Transport,
} from "@modelcontextprotocol/server";

import { createCatalogueApplication } from "../src/catalogue-application.js";
import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";
import {
  MCP_CATALOGUE_OPERATIONS,
  MCP_CATALOGUE_RESOURCES,
  MCP_CATALOGUE_RECORD_URI_TEMPLATE,
  MCP_LEGACY_CONFORMANCE_ONLY,
  MCP_LEGACY_CONFORMANCE_PROTOCOL_VERSION,
  MCP_PROTOCOL_VERSION,
  MCP_PUBLIC_CATALOGUE_URI,
} from "../src/mcp-server.js";
import {
  MCP_STDIO_MAX_BUFFER_BYTES,
  startCatalogueLegacyConformanceStdio,
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

function legacyConformanceSubprocessScript(): string {
  const applicationModule = new URL(
    "../src/catalogue-application.js",
    import.meta.url,
  ).href;
  const snapshotModule = new URL("../src/catalogue-snapshot.js", import.meta.url).href;
  const serverModule = new URL("../src/mcp-server.js", import.meta.url).href;
  const stdioModule = new URL("../src/mcp-stdio.js", import.meta.url).href;
  return [
    `import { createCatalogueApplication } from ${JSON.stringify(applicationModule)};`,
    `import { loadCatalogueSnapshot } from ${JSON.stringify(snapshotModule)};`,
    `import { MCP_LEGACY_CONFORMANCE_ONLY } from ${JSON.stringify(serverModule)};`,
    `import { startCatalogueLegacyConformanceStdio } from ${JSON.stringify(stdioModule)};`,
    "const snapshot = await loadCatalogueSnapshot(process.argv[1], { now: new Date('2026-08-20T12:00:00Z') });",
    "const application = createCatalogueApplication(snapshot, { software: { name: 'gis-ai-go-mcp-gateway', version: '0.1.0', revision: 'a'.repeat(40) }, now: () => new Date('2026-08-20T12:34:56Z') });",
    "startCatalogueLegacyConformanceStdio({ compatibility: MCP_LEGACY_CONFORMANCE_ONLY, application, snapshot, enabledOperations: ['catalogue.describe', 'catalogue.search'], enabledResources: ['catalogue.public', 'catalogue.record'] });",
  ].join("\n");
}

async function subprocessExchange(
  args: readonly string[],
  frame: string,
  environment: Readonly<Record<string, string>> = {},
): Promise<{
  readonly reply: Record<string, unknown>;
  readonly stdout: string;
  readonly stderr: string;
  readonly exitCode: number | null;
}> {
  const child = spawn(process.execPath, [...args], {
    env: { ...process.env, ...environment },
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

test("rejects raw idempotency keys in registered and unregistered STDIO resource URIs", async (t) => {
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const reported: Error[] = [];
  const handle = startCatalogueStdio({
    application: APPLICATION,
    snapshot: SNAPSHOT,
    enabledOperations: [],
    enabledResources: MCP_CATALOGUE_RESOURCES,
    transport: serverTransport,
    onerror: (error) => reported.push(error),
  });
  t.after(async () => {
    await handle.close();
    await clientTransport.close();
  });
  const rawKey = `gis-ai-go:ik:v1:${"e".repeat(64)}`;
  const encodedKey = encodeURIComponent(rawKey);
  const multiplyEncodedKey = encodeURIComponent(encodedKey);
  const resourceUris = [
    `gis-ai-go://catalogue/records/${rawKey}`,
    `gis-ai-go://catalogue/records/${encodedKey}`,
    `gis-ai-go://catalogue/records/${multiplyEncodedKey}`,
    `gis-ai-go://evidence/receipts/${rawKey}`,
    `gis-ai-go://evidence/receipts/${encodedKey}`,
    `gis-ai-go://evidence/receipts/${multiplyEncodedKey}`,
    `gis-ai-go://unregistered/${rawKey}`,
    `gis-ai-go://unregistered/${encodedKey}`,
    `gis-ai-go://unregistered/${multiplyEncodedKey}`,
  ];

  for (const [offset, uri] of resourceUris.entries()) {
    const reply = await exchange(clientTransport, {
      jsonrpc: "2.0",
      id: 50 + offset,
      method: "resources/read",
      params: { _meta: META, uri },
    });
    assert.equal("error" in reply, true);
    if (!("error" in reply)) return;
    assert.equal(reply.error.code, -32_602);
    assert.equal(reply.error.message, "Invalid params");
    assert.deepEqual(reply.error.data, {
      reason: "privacy_sensitive_resource_uri",
      field: "params.uri",
    });
    const serialised = JSON.stringify(reply);
    assert.equal(serialised.includes(rawKey), false);
    assert.equal(serialised.includes(encodedKey), false);
    assert.equal(serialised.includes(multiplyEncodedKey), false);
  }
  const overboundUri =
    `gis-ai-go://unregistered/${"x".repeat(2_048)}/${multiplyEncodedKey}`;
  const overbound = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 70,
    method: "resources/read",
    params: { _meta: META, uri: overboundUri },
  });
  assert.equal("error" in overbound, true);
  if ("error" in overbound) {
    assert.deepEqual(overbound.error.data, {
      reason: "request_field_out_of_bounds",
      field: "params.uri",
    });
    assert.equal(JSON.stringify(overbound).includes(multiplyEncodedKey), false);
  }

  let unexpectedResponses = 0;
  clientTransport.onmessage = () => {
    unexpectedResponses += 1;
  };
  for (const uri of [
    `gis-ai-go://catalogue/records/${rawKey}`,
    `gis-ai-go://evidence/receipts/${multiplyEncodedKey}`,
    overboundUri,
  ]) {
    await clientTransport.send({
      jsonrpc: "2.0",
      method: "resources/read",
      params: { _meta: META, uri },
    });
  }
  await new Promise<void>((resolve) => setImmediate(resolve));
  assert.equal(unexpectedResponses, 0);
  assert.deepEqual(reported, []);
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
  const reported: Error[] = [];
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
    onerror: (error) => reported.push(error),
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
  const rawKey = `gis-ai-go:ik:v1:${"b".repeat(64)}`;
  const encodedKey = encodeURIComponent(rawKey);
  const multiplyEncodedKey = encodeURIComponent(encodedKey);
  for (const id of [
    "x".repeat(129),
    "unsafe\nid",
    Number.MAX_SAFE_INTEGER + 1,
    rawKey,
    `request-${rawKey}`,
    encodedKey,
    multiplyEncodedKey,
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
    const wire = `${JSON.stringify(reply)}\n`;
    assert.ok(Buffer.byteLength(wire) <= MCP_STDIO_MAX_BUFFER_BYTES);
    assert.equal(wire.includes(rawKey), false);
    assert.equal(wire.includes(encodedKey), false);
    assert.equal(wire.includes(multiplyEncodedKey), false);
  }
  for (const id of ["request-42", 42] as const) {
    const accepted = await exchange(clientTransport, {
      jsonrpc: "2.0",
      id,
      method: "server/discover",
      params: { _meta: META },
    });
    assert.equal("result" in accepted, true);
    assert.equal("id" in accepted ? accepted.id : undefined, id);
  }
  let unexpectedResponses = 0;
  clientTransport.onmessage = () => {
    unexpectedResponses += 1;
  };
  await clientTransport.send({
    jsonrpc: "2.0",
    method: "notifications/cancelled",
    params: { _meta: META, requestId: "request-42" },
  });
  await new Promise<void>((resolve) => setImmediate(resolve));
  assert.equal(unexpectedResponses, 0);
  assert.equal(applicationCalls, 0);
  assert.deepEqual(reported, []);
});

test("rejects reconciliation keys in STDIO protocol control fields before SDK dispatch", async (t) => {
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const reported: Error[] = [];
  const handle = startCatalogueStdio({
    application: APPLICATION,
    snapshot: SNAPSHOT,
    enabledOperations: MCP_CATALOGUE_OPERATIONS,
    transport: serverTransport,
    onerror: (error) => reported.push(error),
  });
  t.after(async () => {
    await handle.close();
    await clientTransport.close();
  });
  const rawKey = `gis-ai-go:ik:v1:${"d".repeat(64)}`;
  const prefixedKey = `request-${rawKey}`;
  const encodedKey = encodeURIComponent(rawKey);
  const multiplyEncodedKey = encodeURIComponent(encodedKey);
  const protocolKey = "io.modelcontextprotocol/protocolVersion";
  let id = 71;

  for (const sensitiveValue of [
    rawKey,
    prefixedKey,
    encodedKey,
    multiplyEncodedKey,
  ]) {
    const requestCases = [
      {
        jsonrpc: "2.0",
        id,
        method: sensitiveValue,
        params: { _meta: META },
      },
      {
        jsonrpc: "2.0",
        id,
        method: "tools/call",
        params: { _meta: META, name: sensitiveValue, arguments: {} },
      },
      {
        jsonrpc: "2.0",
        id,
        method: "server/discover",
        params: {
          _meta: { ...META, [protocolKey]: sensitiveValue },
        },
      },
    ] as const;
    for (const item of requestCases) {
      const reply = await exchange(clientTransport, {
        ...item,
        id,
      });
      id += 1;
      assert.equal("error" in reply, true);
      if (!("error" in reply)) return;
      assert.equal(reply.id, null);
      assert.equal(reply.error.code, -32_600);
      assert.equal(reply.error.message, "Invalid Request");
      assert.deepEqual(reply.error.data, {
        reason: "privacy_sensitive_protocol_field",
      });
      const wire = JSON.stringify(reply);
      for (const keyForm of [
        rawKey,
        prefixedKey,
        encodedKey,
        multiplyEncodedKey,
      ]) {
        assert.equal(wire.includes(keyForm), false);
      }
    }

    let unexpectedResponses = 0;
    clientTransport.onmessage = () => {
      unexpectedResponses += 1;
    };
    for (const notification of [
      {
        jsonrpc: "2.0",
        method: sensitiveValue,
        params: { _meta: META },
      },
      {
        jsonrpc: "2.0",
        method: "tools/call",
        params: { _meta: META, name: sensitiveValue, arguments: {} },
      },
      {
        jsonrpc: "2.0",
        method: "notifications/cancelled",
        params: {
          _meta: { ...META, [protocolKey]: sensitiveValue },
          requestId: "request-42",
        },
      },
    ] as const) {
      await clientTransport.send(notification);
    }
    await new Promise<void>((resolve) => setImmediate(resolve));
    assert.equal(unexpectedResponses, 0);
  }
  assert.deepEqual(reported, []);
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

test("serves the bounded raw 2025-06-18 conformance journey explicitly", async (t) => {
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await clientTransport.start();
  const handle = startCatalogueLegacyConformanceStdio({
    compatibility: MCP_LEGACY_CONFORMANCE_ONLY,
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

  const initialized = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 12,
    method: "initialize",
    params: {
      protocolVersion: MCP_LEGACY_CONFORMANCE_PROTOCOL_VERSION,
      capabilities: {},
      clientInfo: { name: "legacy-conformance-test", version: "1.0.0" },
    },
  });
  assert.equal("result" in initialized, true);
  if (!("result" in initialized)) return;
  assert.equal(
    (initialized.result as { readonly protocolVersion?: unknown }).protocolVersion,
    MCP_LEGACY_CONFORMANCE_PROTOCOL_VERSION,
  );
  await clientTransport.send({
    jsonrpc: "2.0",
    method: "notifications/initialized",
  });

  const toolsReply = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 13,
    method: "tools/list",
    params: {},
  });
  assert.equal("result" in toolsReply, true);
  if (!("result" in toolsReply)) return;
  const tools = (toolsReply.result as {
    readonly tools: readonly { readonly name: string }[];
  }).tools;
  assert.deepEqual(
    tools.map((tool) => tool.name),
    ["catalogue.describe", "catalogue.search"],
  );

  const called = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 14,
    method: "tools/call",
    params: {
      name: "catalogue.describe",
      arguments: { record_id: "LR-Q003" },
    },
  });
  assert.equal("result" in called, true);
  if (!("result" in called)) return;
  const callResult = called.result as {
    readonly structuredContent?: { readonly operation?: unknown };
    readonly content?: readonly { readonly type: string; readonly text?: string }[];
  };
  assert.equal(callResult.structuredContent?.operation, "catalogue.describe");
  assert.equal(
    callResult.content?.[0]?.text,
    JSON.stringify(callResult.structuredContent),
  );

  const resourcesReply = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 15,
    method: "resources/list",
    params: {},
  });
  assert.equal("result" in resourcesReply, true);
  if (!("result" in resourcesReply)) return;
  assert.deepEqual(
    (resourcesReply.result as {
      readonly resources: readonly { readonly uri: string }[];
    }).resources.map((resource) => resource.uri),
    [MCP_PUBLIC_CATALOGUE_URI],
  );

  const templatesReply = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 16,
    method: "resources/templates/list",
    params: {},
  });
  assert.equal("result" in templatesReply, true);
  if (!("result" in templatesReply)) return;
  assert.deepEqual(
    (templatesReply.result as {
      readonly resourceTemplates: readonly { readonly uriTemplate: string }[];
    }).resourceTemplates.map((template) => template.uriTemplate),
    [MCP_CATALOGUE_RECORD_URI_TEMPLATE],
  );

  const read = await exchange(clientTransport, {
    jsonrpc: "2.0",
    id: 17,
    method: "resources/read",
    params: { uri: MCP_PUBLIC_CATALOGUE_URI },
  });
  assert.equal("result" in read, true);
  if (!("result" in read)) return;
  const contents = (read.result as {
    readonly contents: readonly { readonly text?: string }[];
  }).contents;
  assert.equal(contents[0]?.text, JSON.stringify(SNAPSHOT.bundle));
});

test("fails closed before transport start without exact conformance authority", () => {
  let transportStarts = 0;
  const transport: Transport = {
    start: () => {
      transportStarts += 1;
      return Promise.resolve();
    },
    send: () => Promise.resolve(),
    close: () => Promise.resolve(),
  };
  const baseOptions = {
    application: APPLICATION,
    snapshot: SNAPSHOT,
    enabledOperations: MCP_CATALOGUE_OPERATIONS,
    transport,
  };
  assert.throws(
    () =>
      startCatalogueLegacyConformanceStdio({
        ...baseOptions,
        compatibility: Symbol("gis-ai-go.mcp-legacy-conformance-only"),
      } as unknown as Parameters<typeof startCatalogueLegacyConformanceStdio>[0]),
    /explicit conformance authority/u,
  );
  assert.throws(
    () =>
      startCatalogueLegacyConformanceStdio(
        baseOptions as unknown as Parameters<
          typeof startCatalogueLegacyConformanceStdio
        >[0],
      ),
    /explicit conformance authority/u,
  );
  assert.equal(transportStarts, 0);
});

test("legacy conformance reuses modern schemas, application results and errors", async () => {
  async function journey(legacy: boolean) {
    const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
    await clientTransport.start();
    const options = {
      application: APPLICATION,
      snapshot: SNAPSHOT,
      enabledOperations: MCP_CATALOGUE_OPERATIONS,
      enabledResources: MCP_CATALOGUE_RESOURCES,
      createRequestContext: () => ({
        requestId: "mcp-parity-test",
        traceId: "1".repeat(32),
      }),
      transport: serverTransport,
    };
    const handle = legacy
      ? startCatalogueLegacyConformanceStdio({
          ...options,
          compatibility: MCP_LEGACY_CONFORMANCE_ONLY,
        })
      : startCatalogueStdio(options);
    try {
      if (legacy) {
        await exchange(clientTransport, {
          jsonrpc: "2.0",
          id: 30,
          method: "initialize",
          params: {
            protocolVersion: MCP_LEGACY_CONFORMANCE_PROTOCOL_VERSION,
            capabilities: {},
            clientInfo: { name: "parity-test", version: "1.0.0" },
          },
        });
        await clientTransport.send({
          jsonrpc: "2.0",
          method: "notifications/initialized",
        });
      } else {
        await exchange(clientTransport, {
          jsonrpc: "2.0",
          id: 30,
          method: "server/discover",
          params: { _meta: META },
        });
      }
      const params = <T extends Record<string, unknown>>(value: T) =>
        legacy ? value : { _meta: META, ...value };
      const tools = await exchange(clientTransport, {
        jsonrpc: "2.0",
        id: 31,
        method: "tools/list",
        params: params({}),
      });
      const called = await exchange(clientTransport, {
        jsonrpc: "2.0",
        id: 32,
        method: "tools/call",
        params: params({
          name: "catalogue.describe",
          arguments: { record_id: "LR-Q003" },
        }),
      });
      const invalid = await exchange(clientTransport, {
        jsonrpc: "2.0",
        id: 33,
        method: "tools/call",
        params: params({ name: "catalogue.describe", arguments: {} }),
      });
      const resources = await exchange(clientTransport, {
        jsonrpc: "2.0",
        id: 34,
        method: "resources/list",
        params: params({}),
      });
      const read = await exchange(clientTransport, {
        jsonrpc: "2.0",
        id: 35,
        method: "resources/read",
        params: params({ uri: MCP_PUBLIC_CATALOGUE_URI }),
      });
      return { called, invalid, read, resources, tools };
    } finally {
      await handle.close();
      await clientTransport.close();
    }
  }

  const modern = await journey(false);
  const legacy = await journey(true);
  const protocolDecorations = new Set([
    "_meta",
    "cacheScope",
    "execution",
    "resultType",
    "ttlMs",
  ]);
  const semanticResult = (value: unknown): unknown =>
    JSON.parse(
      JSON.stringify(value, (key, item) =>
        protocolDecorations.has(key) ? undefined : item,
      ),
    );
  for (const key of ["tools", "called", "invalid", "resources", "read"] as const) {
    assert.equal("result" in modern[key], true);
    assert.equal("result" in legacy[key], true);
    if ("result" in modern[key] && "result" in legacy[key]) {
      assert.deepEqual(
        semanticResult(legacy[key].result),
        semanticResult(modern[key].result),
        key,
      );
    }
  }
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

test("interoperates explicitly with the official legacy-mode STDIO client", async (t) => {
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [
      "--input-type=module",
      "--eval",
      legacyConformanceSubprocessScript(),
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
    { name: "gis-ai-go-official-legacy-test-client", version: "1.0.0" },
    {
      capabilities: {},
      versionNegotiation: { mode: "legacy" },
    },
  );
  let closed = false;
  t.after(async () => {
    if (!closed) await client.close().catch(() => undefined);
  });

  await client.connect(transport);
  assert.notEqual(transport.pid, null);
  assert.equal(
    client.getNegotiatedProtocolVersion(),
    MCP_LEGACY_CONFORMANCE_PROTOCOL_VERSION,
  );
  assert.deepEqual(
    (await client.listTools()).tools.map((tool) => tool.name),
    ["catalogue.describe", "catalogue.search"],
  );
  const called = await client.callTool({
    name: "catalogue.describe",
    arguments: { record_id: "LR-Q003" },
  });
  assert.equal(
    (called.structuredContent as { readonly operation?: unknown }).operation,
    "catalogue.describe",
  );
  assert.deepEqual(
    (await client.listResources()).resources.map((resource) => resource.uri),
    [MCP_PUBLIC_CATALOGUE_URI],
  );
  assert.deepEqual(
    (await client.listResourceTemplates()).resourceTemplates.map(
      (template) => template.uriTemplate,
    ),
    [MCP_CATALOGUE_RECORD_URI_TEMPLATE],
  );
  const read = await client.readResource({ uri: MCP_PUBLIC_CATALOGUE_URI });
  const resourceContent = read.contents[0];
  assert.ok(resourceContent !== undefined && "text" in resourceContent);
  assert.equal(resourceContent.text, JSON.stringify(SNAPSHOT.bundle));
  await client.close();
  closed = true;
  assert.equal(diagnostics, "");
});

test("production STDIO cannot enable legacy serving through conformance environment", async () => {
  const executable = fileURLToPath(
    new URL("../src/mcp-stdio-main.js", import.meta.url),
  );
  const frame = `${JSON.stringify({
    jsonrpc: "2.0",
    id: 18,
    method: "initialize",
    params: {
      protocolVersion: MCP_LEGACY_CONFORMANCE_PROTOCOL_VERSION,
      capabilities: {},
      clientInfo: { name: "production-bypass-test", version: "1.0.0" },
    },
  })}\n`;
  const exchangeResult = await subprocessExchange(
    [executable, SOURCE_CATALOGUE],
    frame,
    {
      GIS_AI_GO_QUAL_206_CONFORMANCE: "1",
      GIS_AI_GO_MCP_LEGACY_PROTOCOL_VERSION:
        MCP_LEGACY_CONFORMANCE_PROTOCOL_VERSION,
    },
  );
  assert.equal(exchangeResult.reply.id, 18);
  const error = exchangeResult.reply.error as Record<string, unknown>;
  assert.equal(error.code, -32_022);
  assert.equal(exchangeResult.stderr, "");
  assert.equal(exchangeResult.exitCode, 0);
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

test("keeps raw and encoded reconciliation keys out of actual STDIO request-ID replies", async () => {
  const executable = fileURLToPath(
    new URL("../src/mcp-stdio-main.js", import.meta.url),
  );
  const rawKey = `gis-ai-go:ik:v1:${"c".repeat(64)}`;
  const encodedKey = encodeURIComponent(rawKey);
  const multiplyEncodedKey = encodeURIComponent(encodedKey);
  const rejectedIds = [
    rawKey,
    `request-${rawKey}`,
    encodedKey,
    multiplyEncodedKey,
  ] as const;
  const request = (id: number | string) => `${JSON.stringify({
    jsonrpc: "2.0",
    id,
    method: "server/discover",
    params: { _meta: META },
  })}\n`;
  const rejected = [];
  for (const id of rejectedIds) {
    const result = await subprocessExchange(
      [executable, SOURCE_CATALOGUE],
      request(id),
    );
    rejected.push(result);
    assert.equal(result.reply.id, null);
    const error = result.reply.error as Record<string, unknown>;
    assert.equal(error.code, -32_600);
    assert.equal(error.message, "Invalid Request");
    assert.deepEqual(error.data, { reason: "invalid_request_id" });
    assert.equal(result.stdout.trimEnd().split("\n").length, 1);
    assert.equal(result.stderr, "");
    assert.equal(result.exitCode, 0);
  }
  const accepted = [];
  for (const id of ["request-42", 42] as const) {
    const result = await subprocessExchange(
      [executable, SOURCE_CATALOGUE],
      request(id),
    );
    accepted.push(result);
    assert.equal(result.reply.id, id);
    assert.equal("result" in result.reply, true);
    assert.equal(result.stderr, "");
    assert.equal(result.exitCode, 0);
  }
  const stdout = [...rejected, ...accepted].map((result) => result.stdout).join("");
  assert.equal(stdout.includes(rawKey), false);
  assert.equal(stdout.includes(encodedKey), false);
  assert.equal(stdout.includes(multiplyEncodedKey), false);
});

test("keeps reconciliation keys in protocol controls out of actual STDIO replies", async () => {
  const rawKey = `gis-ai-go:ik:v1:${"e".repeat(64)}`;
  const encodedKey = encodeURIComponent(rawKey);
  const multiplyEncodedKey = encodeURIComponent(encodedKey);
  const protocolKey = "io.modelcontextprotocol/protocolVersion";
  const messages = [
    {
      jsonrpc: "2.0",
      id: 81,
      method: rawKey,
      params: { _meta: META },
    },
    {
      jsonrpc: "2.0",
      id: 82,
      method: "tools/call",
      params: { _meta: META, name: encodedKey, arguments: {} },
    },
    {
      jsonrpc: "2.0",
      id: 83,
      method: "server/discover",
      params: {
        _meta: { ...META, [protocolKey]: multiplyEncodedKey },
      },
    },
  ] as const;
  const results = [];
  for (const message of messages) {
    const result = await subprocessExchange(
      [
        "--input-type=module",
        "--eval",
        enabledSubprocessScript(),
        SOURCE_CATALOGUE,
      ],
      `${JSON.stringify(message)}\n`,
    );
    results.push(result);
    assert.equal(result.reply.id, null);
    const error = result.reply.error as Record<string, unknown>;
    assert.equal(error.code, -32_600);
    assert.equal(error.message, "Invalid Request");
    assert.deepEqual(error.data, {
      reason: "privacy_sensitive_protocol_field",
    });
    assert.equal(result.stdout.trimEnd().split("\n").length, 1);
    assert.equal(result.stderr, "");
    assert.equal(result.exitCode, 0);
  }
  const stdout = results.map((result) => result.stdout).join("");
  assert.equal(stdout.includes(rawKey), false);
  assert.equal(stdout.includes(encodedKey), false);
  assert.equal(stdout.includes(multiplyEncodedKey), false);
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
