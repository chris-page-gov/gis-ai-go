import assert from "node:assert/strict";
import { execFileSync, spawn, type ChildProcess } from "node:child_process";
import { once } from "node:events";
import {
  chmodSync,
  mkdirSync,
  mkdtempSync,
  readdirSync,
  rmSync,
} from "node:fs";
import { createServer, type Server } from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";
import type { Readable } from "node:stream";
import { setTimeout as delay } from "node:timers/promises";
import { fileURLToPath } from "node:url";
import test from "node:test";

type JsonObject = Record<string, unknown>;

const ROOT = fileURLToPath(new URL("../../../../", import.meta.url));
const ENTRYPOINT = join(
  ROOT,
  "apps",
  "mcp-gateway",
  "dist",
  "src",
  "local-candidate-main.js",
);
const PROVIDER_EGRESS_GUARD = join(
  ROOT,
  "tests",
  "interoperability",
  "fixtures",
  "qual_206_provider_egress_guard.mjs",
);
const ENDPOINT = new URL("http://127.0.0.1:8787/mcp");
const MCP_PROTOCOL_VERSION = "2026-07-28";
const RECEIPT_ID = /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u;
const APPROVED_CACHE_WARNING =
  "The ONS request failed with an internally classified network failure or HTTP " +
  "500 to 599 response. This result uses the exact approved cache; check its " +
  "freshness before use.";
const EXACT_OPERATIONS = Object.freeze([
  "catalogue.search",
  "catalogue.describe",
  "selection.resolve",
  "data.query",
  "evidence.inspect",
] as const);
const EXACT_RESOURCES = Object.freeze([
  "catalogue.public",
  "catalogue.record",
  "evidence.receipt",
] as const);
const PUBLIC_CATALOGUE_URI = "gis-ai-go://catalogue/public";
const RECORD_URI_TEMPLATE = "gis-ai-go://catalogue/records/{record_id}";
const EVIDENCE_URI_TEMPLATE = "gis-ai-go://evidence/receipts/{receipt_id}";
const MAX_CHILD_OUTPUT_BYTES = 1_048_576;
const META = Object.freeze({
  "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
  "io.modelcontextprotocol/clientCapabilities": Object.freeze({}),
  "io.modelcontextprotocol/clientInfo": Object.freeze({
    name: "gis-ai-go-independent-local-candidate-acceptance",
    version: "1.0.0",
  }),
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
const DATA_QUERY_REQUEST = Object.freeze({
  schema: "gis-ai-go.data-query-request.v1",
  idempotency_key: `gis-ai-go:ik:v1:${"7".repeat(64)}`,
  parameters: Object.freeze({
    schema: "gis-ai-go.data-query-parameters.v1",
    resource_id:
      "gis-ai-go:public-read-resource:sha256:" +
      "c7130712a40d75e71bcf0259792404389bea2e549adf6733f34d491f83e99f68",
    dataset: Object.freeze({
      id: "weekly-deaths-region",
      edition: "time-series",
      version: "121",
    }),
    selections: Object.freeze([
      Object.freeze({ dimension: "time", option: "2026" }),
      Object.freeze({ dimension: "geography", option: "E92000001" }),
      Object.freeze({ dimension: "week", option: "week-24" }),
      Object.freeze({ dimension: "causeofdeath", option: "all-causes" }),
    ]),
    limit: 1,
  }),
});

function withTimeout<T>(
  promise: Promise<T>,
  label: string,
  milliseconds = 10_000,
): Promise<T> {
  let timeout: NodeJS.Timeout | undefined;
  return Promise.race([
    promise,
    new Promise<never>((_resolve, reject) => {
      timeout = setTimeout(
        () => reject(new Error(`Timed out waiting for ${label}`)),
        milliseconds,
      );
    }),
  ]).finally(() => {
    if (timeout !== undefined) clearTimeout(timeout);
  });
}

function collectBounded(
  stream: Readable,
  label: string,
  errors: Error[],
): () => string {
  const chunks: Buffer[] = [];
  let bytes = 0;
  stream.on("data", (chunk: Buffer) => {
    bytes += chunk.byteLength;
    if (bytes > MAX_CHILD_OUTPUT_BYTES) {
      errors.push(new Error(`${label} exceeded its output bound`));
      return;
    }
    chunks.push(chunk);
  });
  stream.on("error", (error: Error) => errors.push(error));
  return () => Buffer.concat(chunks).toString("utf8");
}

function parseJsonLines(value: string, label: string): JsonObject[] {
  assert.ok(value.endsWith("\n"), `${label} ended with an incomplete line`);
  return value
    .split("\n")
    .filter((line) => line.length > 0)
    .map((line) => {
      const parsed = JSON.parse(line) as unknown;
      assert.equal(typeof parsed, "object", `${label} line was not an object`);
      assert.notEqual(parsed, null, `${label} line was null`);
      assert.equal(Array.isArray(parsed), false, `${label} line was an array`);
      return parsed as JsonObject;
    });
}

function checkoutState(): string {
  return execFileSync(
    "git",
    ["status", "--porcelain=v1", "--untracked-files=all"],
    { cwd: ROOT, encoding: "utf8" },
  );
}

interface IsolatedChildEnvironment {
  readonly childHome: string;
  readonly childTmp: string;
  readonly environment: NodeJS.ProcessEnv;
}

function isolatedChildEnvironment(sandbox: string): IsolatedChildEnvironment {
  const childHome = join(sandbox, "home");
  const childTmp = join(sandbox, "tmp");
  mkdirSync(childHome, { mode: 0o700 });
  mkdirSync(childTmp, { mode: 0o700 });
  const environment: NodeJS.ProcessEnv = Object.freeze({
    CI: "1",
    HOME: childHome,
    LANG: "C",
    LC_ALL: "C",
    NO_COLOR: "1",
    TMPDIR: childTmp,
    TZ: "Etc/UTC",
  });
  assert.deepEqual(Object.keys(environment).sort(), [
    "CI",
    "HOME",
    "LANG",
    "LC_ALL",
    "NO_COLOR",
    "TMPDIR",
    "TZ",
  ]);
  assert.equal(
    Object.keys(environment).some((name) =>
      /(?:api|auth|credential|key|password|secret|token)/iu.test(name)
    ),
    false,
  );
  return Object.freeze({ childHome, childTmp, environment });
}

function closeServer(server: Server): Promise<void> {
  return new Promise((resolve, reject) => {
    server.close((error) => error === undefined ? resolve() : reject(error));
  });
}

async function getJson(pathname: string): Promise<{
  readonly body: JsonObject;
  readonly status: number;
}> {
  const response = await fetch(new URL(pathname, ENDPOINT), {
    headers: { accept: "application/json" },
    signal: AbortSignal.timeout(2_000),
  });
  const body = await response.json() as unknown;
  assert.equal(typeof body, "object");
  assert.notEqual(body, null);
  assert.equal(Array.isArray(body), false);
  return { body: body as JsonObject, status: response.status };
}

async function waitUntilListening(
  child: ChildProcess,
  timeoutMilliseconds = 10_000,
): Promise<JsonObject> {
  const deadline = Date.now() + timeoutMilliseconds;
  let lastFailure: unknown;
  while (Date.now() < deadline) {
    if (child.exitCode !== null || child.signalCode !== null) {
      throw new Error("The local candidate stopped before becoming healthy");
    }
    try {
      const health = await getJson("/healthz");
      if (health.status === 200) return health.body;
      lastFailure = new Error(`Health returned HTTP ${health.status}`);
    } catch (error) {
      lastFailure = error;
    }
    await delay(50);
  }
  throw new Error("The local candidate did not become healthy", {
    cause: lastFailure,
  });
}

function requestBody(
  id: number,
  method: string,
  parameters: Readonly<Record<string, unknown>> = {},
): JsonObject {
  return {
    jsonrpc: "2.0",
    id,
    method,
    params: { _meta: META, ...parameters },
  };
}

async function exchange(
  id: number,
  method: string,
  parameters: Readonly<Record<string, unknown>> = {},
): Promise<JsonObject> {
  const name = method === "tools/call" && typeof parameters.name === "string"
    ? parameters.name
    : method === "resources/read" && typeof parameters.uri === "string"
      ? parameters.uri
      : undefined;
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      accept: "application/json, text/event-stream",
      "content-type": "application/json",
      "mcp-method": method,
      "mcp-protocol-version": MCP_PROTOCOL_VERSION,
      ...(name === undefined ? {} : { "mcp-name": name }),
    },
    body: JSON.stringify(requestBody(id, method, parameters)),
    signal: AbortSignal.timeout(10_000),
  });
  const raw = await response.text();
  assert.equal(response.status, 200, raw);
  const message = JSON.parse(raw) as JsonObject;
  assert.equal(message.jsonrpc, "2.0");
  assert.equal(message.id, id);
  assert.equal(message.error, undefined, raw);
  return message;
}

function resultOf(message: JsonObject): JsonObject {
  assert.equal(typeof message.result, "object", JSON.stringify(message));
  assert.notEqual(message.result, null);
  return message.result as JsonObject;
}

function assertToolResult(message: JsonObject, operation: string): JsonObject {
  const result = resultOf(message);
  assert.notEqual(result.isError, true);
  assert.equal(typeof result.structuredContent, "object");
  assert.notEqual(result.structuredContent, null);
  const structured = result.structuredContent as JsonObject;
  assert.equal(structured.operation, operation);
  assert.deepEqual(result.content, [{
    type: "text",
    text: JSON.stringify(structured),
  }]);
  const receipt = structured.evidence_receipt as JsonObject;
  assert.equal(typeof receipt, "object");
  assert.notEqual(receipt, null);
  assert.match(receipt.receipt_id as string, RECEIPT_ID);
  return structured;
}

function resourceNames(values: unknown): string[] {
  assert.ok(Array.isArray(values));
  return values.map((value) => {
    assert.equal(typeof value, "object");
    assert.notEqual(value, null);
    const resource = value as JsonObject;
    assert.equal(typeof resource.name, "string");
    return resource.name as string;
  });
}

function resourceText(message: JsonObject, expectedUri: string): JsonObject {
  const result = resultOf(message);
  assert.ok(Array.isArray(result.contents));
  assert.equal(result.contents.length, 1);
  const content = result.contents[0] as JsonObject;
  assert.equal(content.uri, expectedUri);
  assert.equal(content.mimeType, "application/json");
  assert.equal(typeof content.text, "string");
  const parsed = JSON.parse(content.text as string) as unknown;
  assert.equal(typeof parsed, "object");
  assert.notEqual(parsed, null);
  return parsed as JsonObject;
}

test(
  "runs the exact-five provider-free candidate through an independent client",
  { timeout: 40_000 },
  async (t) => {
    const sandbox = mkdtempSync(join(tmpdir(), "gis-ai-go-client-acceptance-"));
    chmodSync(sandbox, 0o700);
    const { childHome, childTmp, environment } = isolatedChildEnvironment(sandbox);

    const checkoutBefore = checkoutState();
    const child = spawn(
      process.execPath,
      ["--import", PROVIDER_EGRESS_GUARD, ENTRYPOINT],
      {
        cwd: ROOT,
        env: environment,
        stdio: ["ignore", "pipe", "pipe", "pipe"],
      },
    );
    assert.ok(child.stdout);
    assert.ok(child.stderr);
    const auditStream = child.stdio[3] as Readable | null;
    assert.ok(auditStream);
    const streamErrors: Error[] = [];
    const stdout = collectBounded(child.stdout, "local candidate stdout", streamErrors);
    const stderr = collectBounded(child.stderr, "local candidate stderr", streamErrors);
    const audit = collectBounded(auditStream, "provider egress audit", streamErrors);
    const childClose = once(child, "close") as Promise<[
      number | null,
      NodeJS.Signals | null,
    ]>;
    let stopped = false;
    t.after(async () => {
      if (!stopped && child.exitCode === null && child.signalCode === null) {
        child.kill("SIGKILL");
        await withTimeout(childClose, "forced local candidate cleanup").catch(
          () => undefined,
        );
      }
      rmSync(sandbox, { recursive: true, force: true });
    });

    const health = await waitUntilListening(child);
    assert.equal(health.status, "ok");
    assert.equal(health.product, "GIS AI GO");
    assert.equal(health.lifecycle, "candidate-unregistered");
    assert.equal(health.production_registration, false);
    assert.equal(typeof health.catalogue, "object");

    const readiness = await getJson("/readyz");
    assert.equal(readiness.status, 200);
    assert.equal(readiness.body.status, "ready");
    assert.equal(readiness.body.reason, "candidate-assembly-verified");
    assert.equal(readiness.body.production_registration, false);
    assert.deepEqual(readiness.body.active_tools, EXACT_OPERATIONS);
    assert.deepEqual(readiness.body.active_api_operations, EXACT_OPERATIONS);

    const discovery = resultOf(await exchange(1, "server/discover"));
    assert.deepEqual(discovery.supportedVersions, [MCP_PROTOCOL_VERSION]);

    const tools = resultOf(await exchange(2, "tools/list"));
    assert.ok(Array.isArray(tools.tools));
    const toolNames = tools.tools.map((value: unknown) => {
      assert.equal(typeof value, "object");
      assert.notEqual(value, null);
      const tool = value as JsonObject;
      assert.equal(typeof tool.inputSchema, "object");
      assert.equal(typeof tool.outputSchema, "object");
      assert.deepEqual(tool.annotations, {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: tool.name === "data.query",
      });
      return tool.name;
    });
    assert.deepEqual([...toolNames].sort(), [...EXACT_OPERATIONS].sort());

    const resources = resultOf(await exchange(3, "resources/list"));
    const resourceTemplates = resultOf(await exchange(4, "resources/templates/list"));
    const discoveredResourceNames = [
      ...resourceNames(resources.resources),
      ...resourceNames(resourceTemplates.resourceTemplates),
    ];
    assert.deepEqual(discoveredResourceNames.sort(), [...EXACT_RESOURCES].sort());
    assert.deepEqual(
      (resources.resources as JsonObject[]).map(({ uri }) => uri),
      [PUBLIC_CATALOGUE_URI],
    );
    assert.deepEqual(
      (resourceTemplates.resourceTemplates as JsonObject[])
        .map(({ uriTemplate }) => uriTemplate),
      [RECORD_URI_TEMPLATE, EVIDENCE_URI_TEMPLATE],
    );

    const catalogue = resourceText(
      await exchange(5, "resources/read", { uri: PUBLIC_CATALOGUE_URI }),
      PUBLIC_CATALOGUE_URI,
    );
    assert.ok(Array.isArray(catalogue.records));
    const recordUri = "gis-ai-go://catalogue/records/PV-ONS-DATA";
    const record = resourceText(
      await exchange(6, "resources/read", { uri: recordUri }),
      recordUri,
    );
    assert.equal(record.id, "PV-ONS-DATA");

    const search = assertToolResult(
      await exchange(7, "tools/call", {
        name: "catalogue.search",
        arguments: {
          query: "ONS Data API",
          facets: { types: ["provider"] },
          limit: 1,
        },
      }),
      "catalogue.search",
    );
    const searchData = search.data as JsonObject;
    assert.ok(Array.isArray(searchData.records));
    assert.equal((searchData.records[0] as JsonObject).id, "PV-ONS-DATA");
    const describe = assertToolResult(
      await exchange(8, "tools/call", {
        name: "catalogue.describe",
        arguments: { record_id: "PV-ONS-DATA" },
      }),
      "catalogue.describe",
    );
    const describeData = describe.data as JsonObject;
    assert.equal((describeData.record as JsonObject).id, "PV-ONS-DATA");
    const selection = assertToolResult(
      await exchange(9, "tools/call", {
        name: "selection.resolve",
        arguments: SELECTION_REQUEST,
      }),
      "selection.resolve",
    );
    const selectionData = selection.data as JsonObject;
    const selectionPlan = selectionData.plan as JsonObject;
    const selectedDataQuery = selectionPlan.data_query as JsonObject;
    assert.deepEqual(selectedDataQuery, DATA_QUERY_REQUEST.parameters);
    const data = assertToolResult(
      await exchange(10, "tools/call", {
        name: "data.query",
        arguments: { ...DATA_QUERY_REQUEST, parameters: selectedDataQuery },
      }),
      "data.query",
    );
    const dataBody = data.data as JsonObject;
    assert.ok(Array.isArray(dataBody.observations));
    assert.equal((dataBody.observations[0] as JsonObject).value, "10471");
    const cache = dataBody.cache as JsonObject;
    assert.equal(typeof cache, "object");
    assert.notEqual(cache, null);
    assert.equal(cache.status, "approved-current");
    assert.deepEqual(data.warnings, [APPROVED_CACHE_WARNING]);
    const dataReceipt = data.evidence_receipt as JsonObject;
    assert.ok(Array.isArray(dataReceipt.transformations));
    assert.deepEqual(
      (dataReceipt.transformations as JsonObject[]).map(({ name }) => name),
      [
        "normalise-public-read-parameters",
        "read-approved-provider-cache",
        "project-public-read-result-core",
      ],
    );

    const dataReceiptId = dataReceipt.receipt_id as string;
    const inspection = assertToolResult(
      await exchange(11, "tools/call", {
        name: "evidence.inspect",
        arguments: { receipt_id: dataReceiptId },
      }),
      "evidence.inspect",
    );
    const inspectionData = inspection.data as JsonObject;
    const inspectedRecord = inspectionData.record as JsonObject;
    const inspectedReceipt = inspectedRecord.receipt as JsonObject;
    assert.equal(inspectedReceipt.receipt_id, dataReceiptId);

    const receipts = [search, describe, selection, data, inspection].map(
      (result) => (result.evidence_receipt as JsonObject).receipt_id,
    );
    assert.equal(new Set(receipts).size, 5);

    const evidenceUri =
      `gis-ai-go://evidence/receipts/${encodeURIComponent(dataReceiptId)}`;
    const evidence = resourceText(
      await exchange(12, "resources/read", { uri: evidenceUri }),
      evidenceUri,
    );
    const evidenceData = evidence.data as JsonObject;
    const evidenceRecord = evidenceData.record as JsonObject;
    assert.equal(
      (evidenceRecord.receipt as JsonObject).receipt_id,
      dataReceiptId,
    );

    child.kill("SIGTERM");
    const [code, signal] = await withTimeout(
      childClose,
      "graceful local candidate shutdown",
    );
    stopped = true;
    const lifecycleOutput = stdout();
    const egressOutput = audit();
    assert.equal(
      code,
      0,
      JSON.stringify({
        audit: egressOutput,
        stderr: stderr(),
        stdout: lifecycleOutput,
      }),
    );
    assert.equal(signal, null);
    assert.deepEqual(streamErrors, []);
    assert.equal(stderr(), "");

    const lifecycleEvents = parseJsonLines(
      lifecycleOutput,
      "local candidate stdout",
    );
    assert.deepEqual(
      lifecycleEvents.map(({ event }) => event),
      ["local_candidate_started", "local_candidate_stopped"],
    );
    for (const event of lifecycleEvents) {
      assert.equal(event.schema, "gis-ai-go.local-candidate-lifecycle.v1");
      assert.equal(event.endpoint, ENDPOINT.href);
      assert.equal(event.target_release, "0.2.0");
      assert.equal(event.lifecycle, "candidate-unregistered");
      assert.equal(event.production_registration, false);
      assert.equal(event.provider_egress, false);
      assert.equal(
        event.provider_observation,
        "deterministic-in-memory-http-503",
      );
      assert.equal(event.data_query_source, "byte-verified-approved-cache");
      assert.equal(typeof event.revision, "string");
      assert.match(event.revision as string, /^[0-9a-f]{40}$/u);
    }

    const egressEvents = parseJsonLines(
      egressOutput,
      "provider egress audit",
    );
    assert.deepEqual(
      egressEvents.map(({ event }) => event),
      ["provider-egress-guard-ready", "provider-egress-guard-summary"],
    );
    assert.equal(egressEvents[1]?.guarded_api_invocation_count, 0);

    assert.deepEqual(readdirSync(childHome), []);
    assert.deepEqual(readdirSync(childTmp), []);
    assert.equal(checkoutState(), checkoutBefore);
  },
);

test(
  "removes private session state after an orderly SIGINT",
  { timeout: 15_000 },
  async (t) => {
    const sandbox = mkdtempSync(join(tmpdir(), "gis-ai-go-sigint-acceptance-"));
    chmodSync(sandbox, 0o700);
    const { childHome, childTmp, environment } = isolatedChildEnvironment(sandbox);
    const checkoutBefore = checkoutState();
    const child = spawn(process.execPath, [ENTRYPOINT], {
      cwd: ROOT,
      env: environment,
      stdio: ["ignore", "pipe", "pipe"],
    });
    assert.ok(child.stdout);
    assert.ok(child.stderr);
    const streamErrors: Error[] = [];
    const stdout = collectBounded(child.stdout, "SIGINT candidate stdout", streamErrors);
    const stderr = collectBounded(child.stderr, "SIGINT candidate stderr", streamErrors);
    const childClose = once(child, "close") as Promise<[
      number | null,
      NodeJS.Signals | null,
    ]>;
    let stopped = false;
    t.after(async () => {
      if (!stopped && child.exitCode === null && child.signalCode === null) {
        child.kill("SIGKILL");
        await withTimeout(childClose, "forced SIGINT candidate cleanup").catch(
          () => undefined,
        );
      }
      rmSync(sandbox, { recursive: true, force: true });
    });

    await waitUntilListening(child);
    child.kill("SIGINT");
    const [code, signal] = await withTimeout(
      childClose,
      "orderly SIGINT candidate shutdown",
    );
    stopped = true;
    assert.equal(code, 0, stderr());
    assert.equal(signal, null);
    assert.deepEqual(streamErrors, []);
    assert.equal(stderr(), "");
    assert.deepEqual(
      parseJsonLines(stdout(), "SIGINT candidate stdout").map(({ event }) => event),
      ["local_candidate_started", "local_candidate_stopped"],
    );
    assert.deepEqual(readdirSync(childHome), []);
    assert.deepEqual(readdirSync(childTmp), []);
    assert.equal(checkoutState(), checkoutBefore);
  },
);

test(
  "reports an occupied-port start failure and removes private state",
  { timeout: 15_000 },
  async (t) => {
    const blocker = createServer();
    await new Promise<void>((resolve, reject) => {
      const onError = (error: Error): void => reject(error);
      blocker.once("error", onError);
      blocker.listen(8_787, "127.0.0.1", () => {
        blocker.removeListener("error", onError);
        resolve();
      });
    });
    t.after(() => blocker.listening ? closeServer(blocker) : undefined);

    const sandbox = mkdtempSync(join(tmpdir(), "gis-ai-go-start-failure-"));
    chmodSync(sandbox, 0o700);
    const { childHome, childTmp, environment } = isolatedChildEnvironment(sandbox);
    const checkoutBefore = checkoutState();
    const child = spawn(process.execPath, [ENTRYPOINT], {
      cwd: ROOT,
      env: environment,
      stdio: ["ignore", "pipe", "pipe"],
    });
    assert.ok(child.stdout);
    assert.ok(child.stderr);
    const streamErrors: Error[] = [];
    const stdout = collectBounded(
      child.stdout,
      "start-failure candidate stdout",
      streamErrors,
    );
    const stderr = collectBounded(
      child.stderr,
      "start-failure candidate stderr",
      streamErrors,
    );
    t.after(() => rmSync(sandbox, { recursive: true, force: true }));

    const [code, signal] = await withTimeout(
      once(child, "close") as Promise<[number | null, NodeJS.Signals | null]>,
      "occupied-port candidate failure",
    );
    assert.equal(code, 1, stderr());
    assert.equal(signal, null);
    assert.deepEqual(streamErrors, []);
    assert.equal(stderr(), "");
    const events = parseJsonLines(stdout(), "start-failure candidate stdout");
    assert.deepEqual(events.map(({ event }) => event), [
      "local_candidate_start_failed",
    ]);
    assert.equal(events[0]?.lifecycle, "candidate-unregistered");
    assert.equal(events[0]?.production_registration, false);
    assert.equal(events[0]?.target_release, "0.2.0");
    assert.deepEqual(readdirSync(childHome), []);
    assert.deepEqual(readdirSync(childTmp), []);
    assert.equal(checkoutState(), checkoutBefore);
    await closeServer(blocker);
  },
);
