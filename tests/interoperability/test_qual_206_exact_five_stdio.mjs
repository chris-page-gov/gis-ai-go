import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { EventEmitter, once } from "node:events";
import test from "node:test";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { PUBLIC_ONS_DATA_QUERY_PARAMETERS } from
  "../../apps/mcp-gateway/dist/src/data-query-application.js";
import {
  MCP_CATALOGUE_RECORD_URI_TEMPLATE,
  MCP_EVIDENCE_RECEIPT_URI_TEMPLATE,
  MCP_PROTOCOL_VERSION,
  MCP_PUBLIC_CATALOGUE_URI,
} from "../../apps/mcp-gateway/dist/src/mcp-server.js";

const ROOT = fileURLToPath(new URL("../../", import.meta.url));
const SERVER = join(
  ROOT,
  "tests",
  "interoperability",
  "fixtures",
  "qual_206_exact_five_stdio_server.mjs",
);
const SOURCE_COMMIT = "fedba12b619e9be6e443e8b249d680b26f73ce9e";
const ENABLE_FLAG = "GIS_AI_GO_QUAL_206_EXACT_FIVE_STDIO";
const SOURCE_COMMIT_VARIABLE = "GIS_AI_GO_QUAL_206_SOURCE_COMMIT";
const AUTHORITY_ARGUMENT = "--exact-five-stdio-conformance-only";
const EXACT_OPERATIONS = Object.freeze([
  "catalogue.search",
  "catalogue.describe",
  "selection.resolve",
  "data.query",
  "evidence.inspect",
]);
const EXACT_RESOURCES = Object.freeze([
  "catalogue.public",
  "catalogue.record",
  "evidence.receipt",
]);
const META = Object.freeze({
  "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
  "io.modelcontextprotocol/clientCapabilities": Object.freeze({}),
  "io.modelcontextprotocol/clientInfo": Object.freeze({
    name: "gis-ai-go-exact-five-subprocess-test",
    version: "1.0.0",
  }),
});
const DATA_QUERY_REQUEST = Object.freeze({
  schema: "gis-ai-go.data-query-request.v1",
  idempotency_key: `gis-ai-go:ik:v1:${"9".repeat(64)}`,
  parameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
});
const SELECTION_REQUEST = Object.freeze({
  question: "Weekly deaths for England in week 24 of 2026, all causes",
  candidate_record_ids: Object.freeze(["PV-ONS-DATA"]),
  constraints: Object.freeze({
    profile_ids: Object.freeze(["PV-ONS-DATA"]),
    provider_ids: Object.freeze(["ons-data-api"]),
    dataset_ids: Object.freeze(["weekly-deaths-region"]),
    editions: Object.freeze(["time-series"]),
    versions: Object.freeze(["121"]),
    dimensions: Object.freeze({
      time: Object.freeze(["2026"]),
      geography: Object.freeze(["E92000001"]),
      week: Object.freeze(["week-24"]),
      causeofdeath: Object.freeze(["all-causes"]),
    }),
  }),
});

const SUSPENSION_SCENARIOS = Object.freeze([
  Object.freeze({
    name: "provider-discovery",
    operations: Object.freeze([
      "catalogue.search",
      "catalogue.describe",
      "evidence.inspect",
    ]),
    suspensions: Object.freeze([
      Object.freeze({ operation: "selection.resolve", source: "provider-discovery" }),
      Object.freeze({ operation: "data.query", source: "provider-discovery" }),
    ]),
  }),
  Object.freeze({
    name: "provider-invocation",
    operations: Object.freeze([
      "catalogue.search",
      "catalogue.describe",
      "selection.resolve",
      "evidence.inspect",
    ]),
    suspensions: Object.freeze([
      Object.freeze({ operation: "data.query", source: "provider-invocation" }),
    ]),
  }),
  ...Object.freeze([
    "catalogue.search",
    "catalogue.describe",
    "selection.resolve",
    "data.query",
  ]).map((operation) => Object.freeze({
    name: `explicit-${operation}`,
    operations: Object.freeze(EXACT_OPERATIONS.filter((name) => name !== operation)),
    suspensions: Object.freeze([
      Object.freeze({ operation, source: "explicit-tool-suspension" }),
    ]),
  })),
  Object.freeze({
    name: "explicit-evidence.inspect",
    operations: Object.freeze([
      "catalogue.search",
      "catalogue.describe",
      "selection.resolve",
    ]),
    suspensions: Object.freeze([
      Object.freeze({ operation: "data.query", source: "required-evidence-operation" }),
      Object.freeze({
        operation: "evidence.inspect",
        source: "explicit-tool-suspension",
      }),
    ]),
  }),
]);

function withTimeout(promise, label, milliseconds = 4_000) {
  let timeout;
  return Promise.race([
    promise,
    new Promise((_resolve, reject) => {
      timeout = setTimeout(
        () => reject(new Error(`Timed out waiting for ${label}`)),
        milliseconds,
      );
    }),
  ]).finally(() => clearTimeout(timeout));
}

function attachJsonLines(stream, values, errors, emitter, prefix) {
  let buffer = "";
  stream.setEncoding("utf8");
  stream.on("data", (chunk) => {
    buffer += chunk;
    while (buffer.includes("\n")) {
      const lineEnd = buffer.indexOf("\n");
      const line = buffer.slice(0, lineEnd);
      buffer = buffer.slice(lineEnd + 1);
      if (line.length === 0) continue;
      try {
        const value = JSON.parse(line);
        values.push(value);
        emitter.emit(`${prefix}:value`, value);
        if (Object.hasOwn(value, "id")) {
          emitter.emit(`${prefix}:id:${String(value.id)}`, value);
        }
        if (typeof value.event === "string") {
          emitter.emit(`${prefix}:event:${value.event}`, value);
        }
      } catch (error) {
        errors.push(error);
      }
    }
  });
  return () => buffer;
}

function writeChunk(stream, value) {
  return new Promise((resolve, reject) => {
    stream.write(value, (error) => {
      if (error === null || error === undefined) resolve();
      else reject(error);
    });
  });
}

function startFixture(t, scenario) {
  const child = spawn(
    process.execPath,
    [SERVER, AUTHORITY_ARGUMENT, `--scenario=${scenario}`],
    {
      cwd: ROOT,
      env: {
        [ENABLE_FLAG]: "1",
        [SOURCE_COMMIT_VARIABLE]: SOURCE_COMMIT,
      },
      stdio: ["pipe", "pipe", "pipe", "pipe"],
    },
  );
  assert.ok(child.stdin);
  assert.ok(child.stdout);
  assert.ok(child.stderr);
  assert.ok(child.stdio[3]);

  const emitter = new EventEmitter();
  const messages = [];
  const audits = [];
  const parseErrors = [];
  let stderr = "";
  child.stderr.setEncoding("utf8");
  child.stderr.on("data", (chunk) => {
    stderr += chunk;
  });
  const stdoutRemainder = attachJsonLines(
    child.stdout,
    messages,
    parseErrors,
    emitter,
    "response",
  );
  const auditRemainder = attachJsonLines(
    child.stdio[3],
    audits,
    parseErrors,
    emitter,
    "audit",
  );
  const exit = once(child, "exit");
  t.after(() => {
    if (child.exitCode === null) {
      child.stdin.end();
      child.kill("SIGTERM");
    }
  });

  async function send(value, fragmented = false) {
    const frame = `${JSON.stringify(value)}\n`;
    if (!fragmented) {
      await writeChunk(child.stdin, frame);
      return;
    }
    const first = Math.max(1, Math.floor(frame.length / 3));
    const second = Math.max(first + 1, Math.floor((frame.length * 2) / 3));
    await writeChunk(child.stdin, frame.slice(0, first));
    await new Promise((resolve) => setImmediate(resolve));
    await writeChunk(child.stdin, frame.slice(first, second));
    await new Promise((resolve) => setImmediate(resolve));
    await writeChunk(child.stdin, frame.slice(second));
  }

  async function request(id, method, params, fragmented = false) {
    const reply = withTimeout(
      once(emitter, `response:id:${String(id)}`).then(([value]) => value),
      `STDIO response ${String(id)}`,
    );
    await send({ jsonrpc: "2.0", id, method, params }, fragmented);
    return await reply;
  }

  async function waitForAudit(event) {
    const existing = audits.find((value) => value.event === event);
    if (existing !== undefined) return existing;
    return await withTimeout(
      once(emitter, `audit:event:${event}`).then(([value]) => value),
      `audit event ${event}`,
    );
  }

  async function close() {
    child.stdin.end();
    const [code, signal] = await withTimeout(exit, `scenario ${scenario} exit`);
    assert.equal(signal, null);
    assert.equal(code, 0, stderr);
    assert.equal(stderr, "");
    assert.deepEqual(parseErrors, []);
    assert.equal(stdoutRemainder(), "");
    assert.equal(auditRemainder(), "");
    const summaries = audits.filter((value) => value.event === "session-summary");
    assert.equal(summaries.length, 1, JSON.stringify(audits));
    return summaries[0];
  }

  return Object.freeze({
    audits,
    child,
    close,
    messages,
    request,
    send,
    waitForAudit,
  });
}

function metaParams(value = {}) {
  return { _meta: META, ...value };
}

function result(reply) {
  assert.equal(typeof reply.result, "object", JSON.stringify(reply));
  assert.notEqual(reply.result, null);
  return reply.result;
}

function error(reply) {
  assert.equal(typeof reply.error, "object", JSON.stringify(reply));
  assert.notEqual(reply.error, null);
  return reply.error;
}

function assertToolParity(reply, operation, expectedError = false) {
  const called = result(reply);
  assert.equal(called.isError === true, expectedError);
  assert.equal(typeof called.structuredContent, "object");
  assert.notEqual(called.structuredContent, null);
  assert.deepEqual(called.content, [{
    type: "text",
    text: JSON.stringify(called.structuredContent),
  }]);
  if (!expectedError) {
    assert.equal(called.structuredContent.operation, operation);
  }
  return called.structuredContent;
}

function resourceProjection(operations) {
  return [
    ...(operations.includes("catalogue.search") &&
      operations.includes("catalogue.describe")
      ? ["catalogue.public"]
      : []),
    ...(operations.includes("catalogue.describe") ? ["catalogue.record"] : []),
    ...(operations.includes("evidence.inspect") ? ["evidence.receipt"] : []),
  ];
}

async function assertDiscovery(client, operations, fragmented = false) {
  const discovered = result(await client.request(
    1,
    "server/discover",
    metaParams(),
    fragmented,
  ));
  assert.deepEqual(discovered.supportedVersions, [MCP_PROTOCOL_VERSION]);
  const expectedResources = resourceProjection(operations);
  assert.deepEqual(discovered.capabilities, {
    ...(operations.length === 0 ? {} : { tools: { listChanged: false } }),
    ...(expectedResources.length === 0
      ? {}
      : { resources: { listChanged: false, subscribe: false } }),
  });

  const listed = result(await client.request(2, "tools/list", metaParams()));
  const listedNames = listed.tools.map(({ name }) => name);
  assert.equal(listedNames.length, operations.length);
  assert.deepEqual([...listedNames].sort(), [...operations].sort());
  for (const tool of listed.tools) {
    assert.equal(typeof tool.inputSchema, "object");
    assert.equal(typeof tool.outputSchema, "object");
  }

  const resources = result(await client.request(3, "resources/list", metaParams()));
  assert.deepEqual(
    resources.resources.map(({ uri }) => uri),
    expectedResources.includes("catalogue.public") ? [MCP_PUBLIC_CATALOGUE_URI] : [],
  );
  const templates = result(await client.request(
    4,
    "resources/templates/list",
    metaParams(),
  ));
  assert.deepEqual(
    templates.resourceTemplates.map(({ uriTemplate }) => uriTemplate),
    [
      ...(expectedResources.includes("catalogue.record")
        ? [MCP_CATALOGUE_RECORD_URI_TEMPLATE]
        : []),
      ...(expectedResources.includes("evidence.receipt")
        ? [MCP_EVIDENCE_RECEIPT_URI_TEMPLATE]
        : []),
    ],
  );
}

function safeCatalogueCall(operations) {
  if (operations.includes("catalogue.search")) {
    return Object.freeze({
      operation: "catalogue.search",
      arguments: Object.freeze({ query: "INSPIRE", limit: 1 }),
    });
  }
  return Object.freeze({
    operation: "catalogue.describe",
    arguments: Object.freeze({ record_id: "LR-Q003" }),
  });
}

async function rejectedInvocation(args, env) {
  const child = spawn(process.execPath, [SERVER, ...args], {
    cwd: ROOT,
    env,
    stdio: ["pipe", "pipe", "pipe", "pipe"],
  });
  let stdout = "";
  let stderr = "";
  let audit = "";
  child.stdout.setEncoding("utf8");
  child.stderr.setEncoding("utf8");
  child.stdio[3].setEncoding("utf8");
  child.stdout.on("data", (chunk) => { stdout += chunk; });
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  child.stdio[3].on("data", (chunk) => { audit += chunk; });
  child.stdin.end();
  const [code] = await withTimeout(once(child, "exit"), "rejected fixture exit");
  return { audit, code, stderr, stdout };
}

test("fails closed unless the exact-five subprocess authority is complete", async () => {
  const missingFlag = await rejectedInvocation(
    [AUTHORITY_ARGUMENT, "--scenario=active"],
    { [SOURCE_COMMIT_VARIABLE]: SOURCE_COMMIT },
  );
  assert.notEqual(missingFlag.code, 0);
  assert.equal(missingFlag.stdout, "");
  assert.equal(missingFlag.audit, "");
  assert.match(missingFlag.stderr, new RegExp(`${ENABLE_FLAG}=1`, "u"));

  const missingArgument = await rejectedInvocation(
    ["--scenario=active"],
    { [ENABLE_FLAG]: "1", [SOURCE_COMMIT_VARIABLE]: SOURCE_COMMIT },
  );
  assert.notEqual(missingArgument.code, 0);
  assert.equal(missingArgument.stdout, "");
  assert.equal(missingArgument.audit, "");
  assert.match(missingArgument.stderr, /exact authority and closed scenario/u);

  const malformedSource = await rejectedInvocation(
    [AUTHORITY_ARGUMENT, "--scenario=active"],
    { [ENABLE_FLAG]: "1", [SOURCE_COMMIT_VARIABLE]: "not-a-commit" },
  );
  assert.notEqual(malformedSource.code, 0);
  assert.equal(malformedSource.stdout, "");
  assert.equal(malformedSource.audit, "");
  assert.match(malformedSource.stderr, /full lowercase Git commit/u);
});

test("serves the exact five operations and catalogue resources through real STDIO pipes", async (t) => {
  const client = startFixture(t, "active");
  await assertDiscovery(client, EXACT_OPERATIONS, true);

  const publicRead = result(await client.request(
    5,
    "resources/read",
    metaParams({ uri: MCP_PUBLIC_CATALOGUE_URI }),
  ));
  assert.equal(publicRead.contents.length, 1);
  assert.equal(publicRead.contents[0].uri, MCP_PUBLIC_CATALOGUE_URI);
  assert.doesNotThrow(() => JSON.parse(publicRead.contents[0].text));

  const recordUri = "gis-ai-go://catalogue/records/LR-Q003";
  const recordRead = result(await client.request(
    6,
    "resources/read",
    metaParams({ uri: recordUri }),
  ));
  assert.equal(recordRead.contents[0].uri, recordUri);
  assert.equal(JSON.parse(recordRead.contents[0].text).id, "LR-Q003");

  const calls = [
    ["catalogue.search", { query: "INSPIRE", limit: 1 }],
    ["catalogue.describe", { record_id: "LR-Q003" }],
    ["selection.resolve", SELECTION_REQUEST],
    ["data.query", DATA_QUERY_REQUEST],
  ];
  const resultsByOperation = new Map();
  for (const [offset, [operation, argumentsValue]] of calls.entries()) {
    const structured = assertToolParity(
      await client.request(
        10 + offset,
        "tools/call",
        metaParams({ name: operation, arguments: argumentsValue }),
      ),
      operation,
    );
    resultsByOperation.set(operation, structured);
    assert.match(
      structured.evidence_receipt.receipt_id,
      /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u,
    );
  }

  const searchReceipt = resultsByOperation.get("catalogue.search")
    .evidence_receipt.receipt_id;
  const inspection = assertToolParity(
    await client.request(
      14,
      "tools/call",
      metaParams({
        name: "evidence.inspect",
        arguments: { receipt_id: searchReceipt },
      }),
    ),
    "evidence.inspect",
  );
  assert.equal(inspection.data.record.receipt.receipt_id, searchReceipt);

  const evidenceUri = `gis-ai-go://evidence/receipts/${encodeURIComponent(searchReceipt)}`;
  const evidenceRead = result(await client.request(
    15,
    "resources/read",
    metaParams({ uri: evidenceUri }),
  ));
  assert.equal(evidenceRead.contents[0].uri, evidenceUri);
  assert.equal(
    JSON.parse(evidenceRead.contents[0].text).data.record.receipt.receipt_id,
    searchReceipt,
  );

  const summary = await client.close();
  assert.equal(summary.transport, "operating-system-stdio-pipes");
  assert.equal(summary.state, "candidate-unregistered");
  assert.equal(summary.production_registration, false);
  assert.deepEqual(summary.operations, EXACT_OPERATIONS);
  assert.deepEqual(summary.resources, EXACT_RESOURCES);
  assert.deepEqual(summary.suspensions, []);
  assert.equal(summary.provider_transport_calls, 1);
  assert.equal(summary.aborted_provider_calls, 0);
  assert.equal(summary.ledger_event_count, 4);
  assert.equal(summary.reported_error_count, 0);
});

test("cancels a real-process data query without response or completed evidence", async (t) => {
  const client = startFixture(t, "cancellation");
  await assertDiscovery(client, EXACT_OPERATIONS, true);
  const started = client.waitForAudit("provider-transport-started");
  await client.send({
    jsonrpc: "2.0",
    id: 40,
    method: "tools/call",
    params: metaParams({ name: "data.query", arguments: DATA_QUERY_REQUEST }),
  }, true);
  await started;
  const aborted = client.waitForAudit("provider-transport-aborted");
  await client.send({
    jsonrpc: "2.0",
    method: "notifications/cancelled",
    params: metaParams({
      requestId: 40,
      reason: "Caller cancelled the exact-five subprocess request",
    }),
  });
  await aborted;

  const listing = result(await client.request(41, "tools/list", metaParams()));
  assert.deepEqual(
    listing.tools.map(({ name }) => name).sort(),
    [...EXACT_OPERATIONS].sort(),
  );
  const missing = assertToolParity(
    await client.request(
      42,
      "tools/call",
      metaParams({
        name: "evidence.inspect",
        arguments: {
          schema: "gis-ai-go.evidence-inspect-request.v2",
          source_operation: "data.query",
          idempotency_key: DATA_QUERY_REQUEST.idempotency_key,
        },
      }),
    ),
    "evidence.inspect",
    true,
  );
  assert.equal(missing.code, "evidence_unavailable");
  assert.equal(client.messages.some(({ id }) => id === 40), false);

  const summary = await client.close();
  assert.equal(client.messages.some(({ id }) => id === 40), false);
  assert.equal(summary.provider_transport_calls, 1);
  assert.equal(summary.aborted_provider_calls, 1);
  assert.equal(summary.ledger_event_count, 0);
  assert.equal(summary.reported_error_count, 0);
});

test("rejects unsupported real-process STDIO traffic without provider dispatch", async (t) => {
  const client = startFixture(t, "unsupported");
  await assertDiscovery(client, EXACT_OPERATIONS, true);
  const rejected = error(await client.request(50, "prompts/list", metaParams()));
  assert.equal(rejected.code, -32_601);
  assert.equal(rejected.message, "Method not found");
  const listing = result(await client.request(51, "tools/list", metaParams()));
  assert.deepEqual(
    listing.tools.map(({ name }) => name).sort(),
    [...EXACT_OPERATIONS].sort(),
  );

  const summary = await client.close();
  assert.equal(summary.provider_transport_calls, 0);
  assert.equal(summary.aborted_provider_calls, 0);
  assert.equal(summary.ledger_event_count, 0);
  assert.equal(summary.reported_error_count, 0);
});

test("keeps all seven governed suspensions absent and uncallable through real STDIO pipes", async (t) => {
  assert.equal(SUSPENSION_SCENARIOS.length, 7);
  let resultingSuspensions = 0;
  for (const [scenarioIndex, scenario] of SUSPENSION_SCENARIOS.entries()) {
    await t.test(scenario.name, async (t) => {
      const client = startFixture(t, scenario.name);
      await assertDiscovery(client, scenario.operations, true);
      for (const [offset, suspension] of scenario.suspensions.entries()) {
        const rejected = error(await client.request(
          100 + (scenarioIndex * 10) + offset,
          "tools/call",
          metaParams({ name: suspension.operation, arguments: {} }),
        ));
        assert.deepEqual(rejected, {
          code: -32_602,
          message: `Tool ${suspension.operation} not found`,
        });
      }

      const safe = safeCatalogueCall(scenario.operations);
      assertToolParity(
        await client.request(
          190 + scenarioIndex,
          "tools/call",
          metaParams({ name: safe.operation, arguments: safe.arguments }),
        ),
        safe.operation,
      );
      const summary = await client.close();
      assert.equal(summary.production_registration, false);
      assert.deepEqual(summary.operations, scenario.operations);
      assert.deepEqual(summary.resources, resourceProjection(scenario.operations));
      assert.deepEqual(summary.suspensions, scenario.suspensions);
      assert.equal(summary.provider_transport_calls, 0);
      assert.equal(summary.aborted_provider_calls, 0);
      assert.equal(summary.ledger_event_count, 1);
      assert.equal(summary.reported_error_count, 0);
      resultingSuspensions += summary.suspensions.length;
    });
  }
  assert.equal(resultingSuspensions, 9);
});
