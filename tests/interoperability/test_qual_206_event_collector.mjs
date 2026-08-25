import assert from "node:assert/strict";
import { execFileSync, spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { EventEmitter, once } from "node:events";
import {
  chmodSync,
  mkdtempSync,
  readFileSync,
  realpathSync,
  rmSync,
  statSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { PUBLIC_ONS_DATA_QUERY_PARAMETERS } from
  "../../apps/mcp-gateway/dist/src/data-query-application.js";
import { parseStrictJson } from
  "../../packages/provider-adapter-sdk/dist/src/index.js";
import {
  MCP_CATALOGUE_INPUT_SCHEMAS,
  MCP_CATALOGUE_OUTPUT_SCHEMAS,
  MCP_CATALOGUE_RECORD_URI_TEMPLATE,
  MCP_EVIDENCE_INPUT_SCHEMAS,
  MCP_EVIDENCE_OUTPUT_SCHEMAS,
  MCP_EVIDENCE_RECEIPT_URI_TEMPLATE,
  MCP_PROTOCOL_VERSION,
  MCP_PUBLIC_CATALOGUE_URI,
  MCP_PUBLIC_READ_INPUT_SCHEMAS,
  MCP_PUBLIC_READ_OUTPUT_SCHEMAS,
} from "../../apps/mcp-gateway/dist/src/mcp-server.js";
import {
  advertisedToolSchemasExact,
  BoundedLineTap,
  cacheableCompleteResultValid,
  nextCapturedStderrBytes,
  parseArguments,
  requestId,
  resourceContentContractValid,
  resourceFacts,
  toolFacts,
  toolOutputContractValidation,
  toolOutputContractValid,
} from "../../scripts/qual_206_exact_five_event_collector.mjs";

const ROOT = fileURLToPath(new URL("../../", import.meta.url));
const COLLECTOR = join(ROOT, "scripts", "qual_206_exact_five_event_collector.mjs");
const CAPTURE_FLAG = "GIS_AI_GO_QUAL_206_EVENT_CAPTURE";
const AUTHORITY_ARGUMENT = "--exact-five-event-capture-only";
const EXACT_OPERATIONS = Object.freeze([
  "catalogue.search",
  "catalogue.describe",
  "selection.resolve",
  "data.query",
  "evidence.inspect",
]);
const expectedAdvertisedInputSchema = (schema) => schema.type === undefined
  ? { type: "object", ...schema }
  : schema;
const EXPECTED_SCHEMAS = Object.freeze({
  "catalogue.search": {
    inputSchema: expectedAdvertisedInputSchema(
      MCP_CATALOGUE_INPUT_SCHEMAS["catalogue.search"],
    ),
    outputSchema: MCP_CATALOGUE_OUTPUT_SCHEMAS["catalogue.search"],
  },
  "catalogue.describe": {
    inputSchema: expectedAdvertisedInputSchema(
      MCP_CATALOGUE_INPUT_SCHEMAS["catalogue.describe"],
    ),
    outputSchema: MCP_CATALOGUE_OUTPUT_SCHEMAS["catalogue.describe"],
  },
  "selection.resolve": {
    inputSchema: expectedAdvertisedInputSchema(
      MCP_PUBLIC_READ_INPUT_SCHEMAS["selection.resolve"],
    ),
    outputSchema: MCP_PUBLIC_READ_OUTPUT_SCHEMAS["selection.resolve"],
  },
  "data.query": {
    inputSchema: expectedAdvertisedInputSchema(
      MCP_PUBLIC_READ_INPUT_SCHEMAS["data.query"],
    ),
    outputSchema: MCP_PUBLIC_READ_OUTPUT_SCHEMAS["data.query"],
  },
  "evidence.inspect": {
    inputSchema: expectedAdvertisedInputSchema(
      MCP_EVIDENCE_INPUT_SCHEMAS["evidence.inspect"],
    ),
    outputSchema: MCP_EVIDENCE_OUTPUT_SCHEMAS["evidence.inspect"],
  },
});
const META = Object.freeze({
  "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
  "io.modelcontextprotocol/clientCapabilities": Object.freeze({}),
  "io.modelcontextprotocol/clientInfo": Object.freeze({
    name: "gis-ai-go-event-collector-test",
    version: "qual-206-client-version-v1",
  }),
});
const INTEGER_IDS = Object.freeze({
  discover: 8_123_456_789_012_301,
  resources: 8_123_456_789_012_303,
  publicCatalogue: 8_123_456_789_012_305,
  search: 8_123_456_789_012_307,
  selection: 8_123_456_789_012_309,
  inspection: 8_123_456_789_012_311,
  cancelled: 8_123_456_789_012_313,
});
const DATA_QUERY_REQUEST = Object.freeze({
  schema: "gis-ai-go.data-query-request.v1",
  idempotency_key: `gis-ai-go:ik:v1:${"9".repeat(64)}`,
  parameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
});
const CANCELLED_DATA_QUERY_REQUEST = Object.freeze({
  ...DATA_QUERY_REQUEST,
  idempotency_key: `gis-ai-go:ik:v1:${"8".repeat(64)}`,
});
const SELECTION_QUESTION =
  "Weekly deaths for England in week 24 of 2026, all causes";
const SELECTION_REQUEST = Object.freeze({
  question: SELECTION_QUESTION,
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

function currentCommit() {
  return execFileSync(
    "git",
    ["-C", ROOT, "rev-parse", "--verify", "HEAD^{commit}"],
    { encoding: "utf8" },
  ).trim();
}

function executableIdentity() {
  const executable = realpathSync(process.execPath);
  const bytes = statSync(executable).size;
  const sha256 = createHash("sha256")
    .update(readFileSync(executable))
    .digest("hex");
  return Object.freeze({ bytes, sha256 });
}

function withTimeout(promise, label, milliseconds = 8_000) {
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

function writeRawFrame(stream, value) {
  return new Promise((resolve, reject) => {
    stream.write(`${value}\n`, (error) => {
      if (error === null || error === undefined) resolve();
      else reject(error);
    });
  });
}

function writeFrame(stream, value) {
  return writeRawFrame(stream, JSON.stringify(value));
}

function metaParams(value = {}) {
  return { _meta: META, ...value };
}

function result(reply) {
  assert.equal(typeof reply.result, "object", JSON.stringify(reply));
  assert.notEqual(reply.result, null);
  return reply.result;
}

function assertToolParity(reply, operation) {
  const called = result(reply);
  assert.notEqual(called.isError, true);
  assert.equal(typeof called.structuredContent, "object");
  assert.notEqual(called.structuredContent, null);
  assert.equal(called.structuredContent.operation, operation);
  assert.deepEqual(called.content, [{
    type: "text",
    text: JSON.stringify(called.structuredContent),
  }]);
  return called.structuredContent;
}

function readCompleteEvents(logPath) {
  try {
    const text = readFileSync(logPath, "utf8");
    return text
      .split("\n")
      .filter((line) => line.length > 0)
      .map((line) => JSON.parse(line));
  } catch (error) {
    if (error?.code === "ENOENT") return [];
    throw error;
  }
}

function safeLogDiagnostics(logPath) {
  try {
    const events = readCompleteEvents(logPath);
    const counts = {};
    for (const { event } of events) {
      counts[event] = (counts[event] ?? 0) + 1;
    }
    return JSON.stringify({
      event_count: events.length,
      event_counts: counts,
      final_event: events.at(-1)?.event ?? null,
      protocol_session_status:
        events.at(-1)?.protocol_session_status ?? null,
      response_diagnostics: events
        .filter(({ event }) => event === "server_response")
        .map(({ facts, operation, request_method: method, resource, semantic }) => ({
          facts,
          method,
          operation,
          resource,
          semantic,
        })),
      anomalies: events
        .filter(({ event }) => event === "capture_anomaly")
        .map(({ classification }) => classification),
    });
  } catch (error) {
    return `event diagnostics unavailable: ${error.message}`;
  }
}

async function waitForLogEvent(logPath, predicate, label) {
  const deadline = Date.now() + 8_000;
  while (Date.now() < deadline) {
    const event = readCompleteEvents(logPath).find(predicate);
    if (event !== undefined) return event;
    await new Promise((resolve) => setTimeout(resolve, 10));
  }
  throw new Error(`Timed out waiting for ${label}`);
}

function startCollector(t) {
  const temporaryRoot = realpathSync(mkdtempSync(join(tmpdir(), "qual-206-events-")));
  chmodSync(temporaryRoot, 0o700);
  const logPath = join(temporaryRoot, "events.jsonl");
  const manifestPath = join(temporaryRoot, "manifest.json");
  const parent = executableIdentity();
  const sourceCommit = currentCommit();
  const child = spawn(
    process.execPath,
    [
      COLLECTOR,
      AUTHORITY_ARGUMENT,
      "--log",
      logPath,
      "--manifest",
      manifestPath,
      "--client",
      "synthetic-raw-client",
      "--source-commit",
      sourceCommit,
      "--expected-parent-sha256",
      parent.sha256,
      "--expected-parent-bytes",
      String(parent.bytes),
    ],
    {
      cwd: ROOT,
      env: {
        [CAPTURE_FLAG]: "1",
        LANG: "C.UTF-8",
        LC_ALL: "C.UTF-8",
        TZ: "UTC",
      },
      stdio: ["pipe", "pipe", "pipe"],
    },
  );
  assert.ok(child.stdin);
  assert.ok(child.stdout);
  assert.ok(child.stderr);

  const emitter = new EventEmitter();
  const messages = [];
  const parseErrors = [];
  let stdoutRemainder = "";
  let stderr = "";
  child.stdout.setEncoding("utf8");
  child.stdout.on("data", (chunk) => {
    stdoutRemainder += chunk;
    while (stdoutRemainder.includes("\n")) {
      const end = stdoutRemainder.indexOf("\n");
      const line = stdoutRemainder.slice(0, end);
      stdoutRemainder = stdoutRemainder.slice(end + 1);
      if (line.length === 0) continue;
      try {
        const message = JSON.parse(line);
        messages.push(message);
        if (Object.hasOwn(message, "id")) {
          emitter.emit(`response:${typeof message.id}:${String(message.id)}`, message);
        }
      } catch (error) {
        parseErrors.push(error);
      }
    }
  });
  child.stderr.setEncoding("utf8");
  child.stderr.on("data", (chunk) => {
    stderr += chunk;
  });
  const closed = once(child, "close");

  t.after(async () => {
    if (child.exitCode === null) {
      child.stdin.end();
      child.kill("SIGTERM");
    }
    await withTimeout(closed, "collector cleanup", 5_000).catch(() => {});
    rmSync(temporaryRoot, { force: true, recursive: true });
  });

  async function send(value) {
    await writeFrame(child.stdin, value);
  }

  async function sendRaw(value) {
    await writeRawFrame(child.stdin, value);
  }

  async function request(id, method, params) {
    const event = `response:${typeof id}:${String(id)}`;
    const response = withTimeout(Promise.race([
      once(emitter, event).then(([value]) => value),
      closed.then(([code, signal]) => {
        throw new Error(
          `Collector closed before response ${String(id)}: code=${String(code)} ` +
            `signal=${String(signal)} stderr=${stderr}`,
        );
      }),
    ]),
      `collector response ${String(id)}`,
    );
    await send({ jsonrpc: "2.0", id, method, params });
    return await response;
  }

  return Object.freeze({
    child,
    close: async () => {
      child.stdin.end();
      const [code, signal] = await withTimeout(closed, "collector close", 20_000);
      return {
        code,
        logPath,
        manifestPath,
        messages,
        parseErrors,
        signal,
        sourceCommit,
        stderr,
        stdoutRemainder,
        temporaryRoot,
      };
    },
    logPath,
    messages,
    request,
    send,
    sendRaw,
  });
}

test(
  "captures one closed strict-modern exact-five host journey without scoring capability",
  { timeout: 45_000 },
  async (t) => {
    const client = startCollector(t);

    const discovered = result(await client.request(
      INTEGER_IDS.discover,
      "server/discover",
      metaParams(),
    ));
    assert.deepEqual(discovered.supportedVersions, [MCP_PROTOCOL_VERSION]);
    assert.equal(cacheableCompleteResultValid(
      discovered,
      ["capabilities", "instructions", "supportedVersions"],
    ), true);
    assert.equal(cacheableCompleteResultValid(
      { ...discovered, nextCursor: "partial-discovery" },
      ["capabilities", "instructions", "supportedVersions"],
    ), false);

    const tools = result(await client.request(
      "tools-list-2",
      "tools/list",
      metaParams(),
    ));
    assert.deepEqual(
      tools.tools.map(({ name }) => name).sort(),
      [...EXACT_OPERATIONS].sort(),
    );
    assert.equal(tools.tools.every(({ inputSchema }) => inputSchema !== null), true);
    assert.equal(tools.tools.every(({ outputSchema }) => outputSchema !== null), true);
    for (const tool of tools.tools) {
      assert.deepEqual(tool.inputSchema, EXPECTED_SCHEMAS[tool.name].inputSchema);
      assert.deepEqual(tool.outputSchema, EXPECTED_SCHEMAS[tool.name].outputSchema);
    }
    assert.equal(cacheableCompleteResultValid(tools, ["tools"]), true);
    assert.equal(cacheableCompleteResultValid(
      { ...tools, nextCursor: "partial-tools" },
      ["tools"],
    ), false);
    assert.equal(advertisedToolSchemasExact(tools.tools), true);
    const sentinelSchemas = structuredClone(tools.tools);
    sentinelSchemas[0].inputSchema = { oneOf: [] };
    assert.equal(advertisedToolSchemasExact(sentinelSchemas), false);

    const resources = result(await client.request(
      INTEGER_IDS.resources,
      "resources/list",
      metaParams(),
    ));
    assert.deepEqual(
      resources.resources.map(({ uri }) => uri),
      [MCP_PUBLIC_CATALOGUE_URI],
    );
    assert.equal(cacheableCompleteResultValid(resources, ["resources"]), true);
    assert.equal(cacheableCompleteResultValid(
      { ...resources, nextCursor: "partial-resources" },
      ["resources"],
    ), false);

    const templates = result(await client.request(
      "templates-list-4",
      "resources/templates/list",
      metaParams(),
    ));
    assert.deepEqual(
      templates.resourceTemplates.map(({ uriTemplate }) => uriTemplate),
      [MCP_CATALOGUE_RECORD_URI_TEMPLATE, MCP_EVIDENCE_RECEIPT_URI_TEMPLATE],
    );
    assert.equal(cacheableCompleteResultValid(
      templates,
      ["resourceTemplates"],
    ), true);
    assert.equal(cacheableCompleteResultValid(
      { ...templates, nextCursor: "partial-templates" },
      ["resourceTemplates"],
    ), false);

    const publicCatalogue = result(await client.request(
      INTEGER_IDS.publicCatalogue,
      "resources/read",
      metaParams({ uri: MCP_PUBLIC_CATALOGUE_URI }),
    ));
    assert.equal(publicCatalogue.contents[0].uri, MCP_PUBLIC_CATALOGUE_URI);
    const publicCatalogueValue = JSON.parse(publicCatalogue.contents[0].text);
    const expectedCatalogueBundle = JSON.parse(
      readFileSync(join(ROOT, "artifacts", "okf", "okf-bundle.json"), "utf8"),
    );
    const expectedCatalogueRecord = expectedCatalogueBundle.records.find(
      ({ id }) => id === "LR-Q003",
    );
    const expectedCatalogue = {
      bundle: expectedCatalogueBundle,
      record: expectedCatalogueRecord,
      revision: expectedCatalogueBundle.revision,
    };
    assert.equal(resourceContentContractValid(
      "catalogue.public",
      publicCatalogueValue,
      expectedCatalogue,
      null,
      null,
    ), true);
    const duplicateKeyResource = structuredClone(publicCatalogue);
    duplicateKeyResource.contents[0].text =
      '{"revision":"first","revision":"second"}';
    assert.equal(resourceFacts(
      duplicateKeyResource,
      "catalogue.public",
      MCP_PUBLIC_CATALOGUE_URI,
      expectedCatalogue,
      null,
      null,
    ).semantic, "resource-read-fail");
    const changedCatalogue = structuredClone(publicCatalogueValue);
    changedCatalogue.title = `${changedCatalogue.title} changed`;
    assert.equal(resourceContentContractValid(
      "catalogue.public",
      changedCatalogue,
      expectedCatalogue,
      null,
      null,
    ), false);

    const recordUri = "gis-ai-go://catalogue/records/LR-Q003";
    const record = result(await client.request(
      "record-read-6",
      "resources/read",
      metaParams({ uri: recordUri }),
    ));
    assert.equal(record.contents[0].uri, recordUri);
    const recordValue = JSON.parse(record.contents[0].text);
    assert.equal(recordValue.id, "LR-Q003");
    assert.equal(resourceContentContractValid(
      "catalogue.record",
      recordValue,
      expectedCatalogue,
      null,
      null,
    ), true);
    const changedRecord = structuredClone(recordValue);
    changedRecord.title = `${changedRecord.title} changed`;
    assert.equal(resourceContentContractValid(
      "catalogue.record",
      changedRecord,
      expectedCatalogue,
      null,
      null,
    ), false);

    const searchReply = await client.request(
        INTEGER_IDS.search,
        "tools/call",
        metaParams({
          name: "catalogue.search",
          arguments: { query: "INSPIRE", limit: 1 },
        }),
      );
    const search = assertToolParity(
      searchReply,
      "catalogue.search",
    );
    assert.equal(toolOutputContractValid("catalogue.search", search), true);
    const strictSearch = parseStrictJson(JSON.stringify(search));
    const strictSearchValidation = toolOutputContractValidation(
      "catalogue.search",
      strictSearch,
    );
    assert.equal(
      strictSearchValidation.valid,
      true,
      JSON.stringify(strictSearchValidation),
    );
    assert.equal(toolOutputContractValid("catalogue.search", {
      schema: search.schema,
      operation: search.operation,
    }), false);
    const searchAnalysis = toolFacts(
      result(searchReply),
      "catalogue.search",
      expectedCatalogue,
      null,
    );
    assert.equal(
      searchAnalysis.semantic,
      "tool-success-pass",
      JSON.stringify({
        facts: searchAnalysis.facts,
        result_keys: Object.keys(result(searchReply)).sort(),
        result_meta: result(searchReply)._meta,
        result_type: result(searchReply).resultType,
      }),
    );
    const searchReceipt = search.evidence_receipt.receipt_id;
    assert.match(
      searchReceipt,
      /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u,
    );

    assertToolParity(
      await client.request(
        "describe-8",
        "tools/call",
        metaParams({
          name: "catalogue.describe",
          arguments: { record_id: "LR-Q003" },
        }),
      ),
      "catalogue.describe",
    );
    assertToolParity(
      await client.request(
        INTEGER_IDS.selection,
        "tools/call",
        metaParams({ name: "selection.resolve", arguments: SELECTION_REQUEST }),
      ),
      "selection.resolve",
    );

    const query = assertToolParity(
      await client.request(
        "data-success-10",
        "tools/call",
        metaParams({ name: "data.query", arguments: DATA_QUERY_REQUEST }),
      ),
      "data.query",
    );
    assert.equal(query.data.observations[0].value, "10471");
    await waitForLogEvent(
      client.logPath,
      (event) => event.event === "server_audit" &&
        event.audit_kind === "provider-transport-started" && event.ordinal === 1,
      "first provider start evidence",
    );

    const inspection = assertToolParity(
      await client.request(
        INTEGER_IDS.inspection,
        "tools/call",
        metaParams({
          name: "evidence.inspect",
          arguments: { receipt_id: searchReceipt },
        }),
      ),
      "evidence.inspect",
    );
    assert.equal(inspection.data.record.receipt.receipt_id, searchReceipt);

    const receiptUri =
      `gis-ai-go://evidence/receipts/${encodeURIComponent(searchReceipt)}`;
    const receipt = result(await client.request(
      "receipt-read-12",
      "resources/read",
      metaParams({ uri: receiptUri }),
    ));
    assert.equal(receipt.contents[0].uri, receiptUri);
    assert.equal(
      JSON.parse(receipt.contents[0].text).data.record.receipt.receipt_id,
      searchReceipt,
    );
    const receiptValue = JSON.parse(receipt.contents[0].text);
    assert.equal(resourceContentContractValid(
      "evidence.receipt",
      receiptValue,
      expectedCatalogue,
      searchReceipt,
      inspection,
    ), true);
    const differentReceipt = structuredClone(receiptValue);
    differentReceipt.request_id = `${differentReceipt.request_id}-different`;
    assert.equal(
      toolOutputContractValid("evidence.inspect", differentReceipt),
      true,
    );
    assert.equal(resourceContentContractValid(
      "evidence.receipt",
      differentReceipt,
      expectedCatalogue,
      searchReceipt,
      inspection,
    ), false);

    const cancelledId = INTEGER_IDS.cancelled;
    await client.send({
      jsonrpc: "2.0",
      id: cancelledId,
      method: "tools/call",
      params: metaParams({
        name: "data.query",
        arguments: CANCELLED_DATA_QUERY_REQUEST,
      }),
    });
    await waitForLogEvent(
      client.logPath,
      (event) => event.event === "server_audit" &&
        event.audit_kind === "provider-transport-started" && event.ordinal === 2,
      "second provider start evidence",
    );
    const cancellationReason = "Raw client cancelled its second data query";
    await client.send({
      jsonrpc: "2.0",
      method: "notifications/cancelled",
      params: metaParams({ requestId: cancelledId, reason: cancellationReason }),
    });
    await waitForLogEvent(
      client.logPath,
      (event) => event.event === "server_audit" &&
        event.audit_kind === "provider-transport-aborted" && event.ordinal === 2,
      "provider cancellation evidence",
    );

    const unsupported = await client.request(
      "prompts-list-14",
      "prompts/list",
      metaParams(),
    );
    assert.deepEqual(unsupported.error, {
      code: -32_601,
      message: "Method not found",
    });
    assert.equal(client.messages.some(({ id }) => id === cancelledId), false);

    const completed = await client.close();
    assert.equal(completed.signal, null);
    assert.equal(
      completed.code,
      0,
      `${completed.stderr}\n${safeLogDiagnostics(completed.logPath)}`,
    );
    assert.equal(completed.stderr, "");
    assert.deepEqual(completed.parseErrors, []);
    assert.equal(completed.stdoutRemainder, "");
    assert.equal(completed.messages.some(({ id }) => id === cancelledId), false);

    const manifest = JSON.parse(readFileSync(completed.manifestPath, "utf8"));
    assert.equal(manifest.source_commit, completed.sourceCommit);
    assert.equal(manifest.status, "complete");
    assert.equal(manifest.protocol_session_status, "passed");
    assert.equal(manifest.capability_scored, false);
    assert.equal(manifest.exact_five_host_capability, false);
    assert.equal(statSync(completed.temporaryRoot).mode & 0o777, 0o700);
    assert.equal(statSync(completed.logPath).mode & 0o777, 0o600);
    assert.equal(statSync(completed.manifestPath).mode & 0o777, 0o600);

    const verification = execFileSync(
      "uv",
      [
        "run",
        "--locked",
        "--cache-dir",
        ".uv-cache",
        "python",
        join(ROOT, "scripts", "verify_qual_206_strict_modern_host_events.py"),
        "--event-log",
        completed.logPath,
        "--manifest",
        completed.manifestPath,
      ],
      { cwd: ROOT, encoding: "utf8" },
    );
    assert.match(
      verification,
      /^QUAL-206 private event capture verified \(\d+ events; passed\)\.\n$/u,
    );

    const logText = readFileSync(completed.logPath, "utf8");
    const events = readCompleteEvents(completed.logPath);
    const sessionEnd = events.at(-1);
    assert.equal(sessionEnd.event, "session_end");
    assert.equal(sessionEnd.protocol_session_status, "passed");
    assert.equal(sessionEnd.capability_scored, false);
    assert.equal(sessionEnd.exact_five_host_capability, false);
    assert.equal(events.some(({ event }) => event === "capture_anomaly"), false);
    const requestIdKinds = new Set(
      events
        .filter(({ event }) => event === "client_request")
        .map(({ request_id_kind: kind }) => kind),
    );
    assert.deepEqual([...requestIdKinds].sort(), ["integer", "string"]);
    for (const secret of [
      "INSPIRE",
      "LR-Q003",
      SELECTION_QUESTION,
      DATA_QUERY_REQUEST.idempotency_key,
      CANCELLED_DATA_QUERY_REQUEST.idempotency_key,
      cancellationReason,
      "10471",
      searchReceipt,
      "gis-ai-go-event-collector-test",
      "qual-206-client-version-v1",
      "tools-list-2",
      "templates-list-4",
      "record-read-6",
      "describe-8",
      "data-success-10",
      "receipt-read-12",
      "prompts-list-14",
      ...Object.values(INTEGER_IDS).map(String),
    ]) {
      assert.equal(logText.includes(secret), false, `raw value leaked: ${secret}`);
    }
  },
);

test(
  "fails closed on malformed and duplicate-key JSON-RPC wire frames",
  { timeout: 45_000 },
  async (t) => {
    const client = startCollector(t);
    await client.sendRaw(
      '{"jsonrpc":"2.0","id":"first","id":"second",' +
        '"method":"server/discover","params":{}}',
    );
    await client.sendRaw("{");
    const completed = await client.close();
    assert.equal(completed.signal, null);
    assert.equal(completed.code, 2);
    const events = readCompleteEvents(completed.logPath);
    assert.ok(
      events.filter(
        ({ classification, event }) =>
          event === "capture_anomaly" && classification === "invalid-json-rpc",
      ).length >= 2,
    );
    assert.equal(events.at(-1)?.event, "session_end");
    assert.equal(events.at(-1)?.protocol_session_status, "failed");
    const manifest = JSON.parse(readFileSync(completed.manifestPath, "utf8"));
    assert.equal(manifest.protocol_session_status, "failed");
    assert.equal(manifest.capability_scored, false);
  },
);

test("accepts only the exact event-capture argument contract", () => {
  const root = "/tmp/qual-206-argument-contract";
  const argv = [
    AUTHORITY_ARGUMENT,
    "--log",
    `${root}/events.jsonl`,
    "--manifest",
    `${root}/manifest.json`,
    "--client",
    "raw-client",
    "--source-commit",
    "a".repeat(40),
    "--expected-parent-sha256",
    "b".repeat(64),
    "--expected-parent-bytes",
    "123",
  ];
  const parsed = parseArguments(argv, { [CAPTURE_FLAG]: "1" });
  assert.equal(parsed.client, "raw-client");
  assert.equal(parsed.expectedParentBytes, 123);
  assert.equal(parsed.expectedParentSha256, "b".repeat(64));
  assert.equal(parsed.sourceCommit, "a".repeat(40));
  assert.throws(() => parseArguments(argv, {}), new RegExp(`${CAPTURE_FLAG}=1`, "u"));
  const reordered = [...argv];
  [reordered[1], reordered[3]] = [reordered[3], reordered[1]];
  assert.throws(
    () => parseArguments(reordered, { [CAPTURE_FLAG]: "1" }),
    /expected exact argument --log/u,
  );
});

test("treats a newline-terminated frame at the exact byte limit as valid", () => {
  const frames = [];
  const anomalies = [];
  const tap = new BoundedLineTap(
    4,
    (frame, bytes) => frames.push({ bytes, text: frame.toString("utf8") }),
    (anomaly) => anomalies.push(anomaly),
    "unit-test",
  );
  tap.push(Buffer.from("abc\n", "utf8"));
  tap.push(Buffer.from("defg\n", "utf8"));
  const summary = tap.flush();
  assert.deepEqual(frames, [{ bytes: 4, text: "abc" }]);
  assert.equal(anomalies.length, 1);
  assert.equal(anomalies[0].classification, "oversized-frame");
  assert.equal(anomalies[0].bytes, 5);
  assert.deepEqual(summary, { bytes: 9, frames: 2 });
});

test("rejects ambiguous request identifiers before hashing", () => {
  assert.equal(requestId(0).valid, true);
  assert.equal(requestId(-0).valid, false);
  assert.equal(requestId(1.5).valid, false);
  assert.equal(requestId("").valid, false);
  assert.equal(requestId("request-1").valid, true);
  const rawKey = `gis-ai-go:ik:v1:${"7".repeat(64)}`;
  const encodedKey = encodeURIComponent(rawKey);
  assert.equal(requestId(rawKey).valid, false);
  assert.equal(requestId(encodedKey).valid, false);
  assert.equal(requestId(encodeURIComponent(encodedKey)).valid, false);
});

test("accepts stderr at exactly 64 KiB and rejects the next byte", () => {
  assert.equal(nextCapturedStderrBytes(0, 65_536), 65_536);
  assert.equal(nextCapturedStderrBytes(65_535, 1), 65_536);
  assert.throws(() => nextCapturedStderrBytes(65_536, 1));
});
