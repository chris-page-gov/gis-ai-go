import assert from "node:assert/strict";
import {
  execFileSync,
  spawn,
  type ChildProcess,
} from "node:child_process";
import { EventEmitter, once } from "node:events";
import { request as nodeRequest } from "node:http";
import { fileURLToPath } from "node:url";
import type { Readable } from "node:stream";
import test, { type TestContext } from "node:test";

import { PUBLIC_ONS_DATA_QUERY_PARAMETERS } from
  "../src/data-query-application.js";
import {
  MCP_CATALOGUE_RECORD_URI_TEMPLATE,
  MCP_EVIDENCE_RECEIPT_URI_TEMPLATE,
  MCP_PROTOCOL_VERSION,
  MCP_PUBLIC_CATALOGUE_URI,
} from "../src/mcp-server.js";

type JsonObject = Record<string, unknown>;

const ROOT = fileURLToPath(new URL("../../../../", import.meta.url));
const SERVER = fileURLToPath(new URL(
  "../../test/fixtures/qual-206-exact-five-http-server.mjs",
  import.meta.url,
));
const PROVIDER_EGRESS_GUARD = fileURLToPath(new URL(
  "../../../../tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs",
  import.meta.url,
));
const SOURCE_COMMIT = execFileSync("git", ["rev-parse", "HEAD"], {
  cwd: ROOT,
  encoding: "utf8",
}).trim();
const ENABLE_FLAG = "GIS_AI_GO_QUAL_206_EXACT_FIVE_HTTP";
const SOURCE_COMMIT_VARIABLE = "GIS_AI_GO_QUAL_206_SOURCE_COMMIT";
const AUDIT_FD_VARIABLE = "GIS_AI_GO_QUAL_206_PRIVATE_AUDIT_FD";
const AUTHORITY_ARGUMENT = "--exact-five-http-conformance-only";
const AUDIT_SCHEMA = "gis-ai-go.qual-206-exact-five-http-audit.v1";
const GRACEFUL_SHUTDOWN_MILLISECONDS = 8_000;
const FORCED_SHUTDOWN_MILLISECONDS = 2_000;
const EXTERNAL_SUITE_TIMEOUT_MILLISECONDS = 50_000;
const MAX_EXTERNAL_SUITE_OUTPUT_BYTES = 1_048_576;
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
const META = Object.freeze({
  "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
  "io.modelcontextprotocol/clientCapabilities": Object.freeze({}),
  "io.modelcontextprotocol/clientInfo": Object.freeze({
    name: "gis-ai-go-exact-five-real-socket-test",
    version: "1.0.0",
  }),
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

function withTimeout<T>(
  promise: Promise<T>,
  label: string,
  milliseconds = 8_000,
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

function terminateDetachedProcessGroup(child: ChildProcess): void {
  if (process.platform !== "win32" && child.pid !== undefined) {
    try {
      process.kill(-child.pid, "SIGKILL");
      return;
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "ESRCH") throw error;
    }
  }
  if (child.exitCode === null && child.signalCode === null) {
    child.kill("SIGKILL");
  }
}

async function runExternalLocalHttpSuite(
  timeoutMilliseconds = EXTERNAL_SUITE_TIMEOUT_MILLISECONDS,
): Promise<{ readonly stderr: string; readonly stdout: string }> {
  const environment: NodeJS.ProcessEnv = {
    ...process.env,
    CI: "1",
    NO_COLOR: "1",
  };
  delete environment.NODE_TEST_CONTEXT;
  const child = spawn(
    process.execPath,
    ["--test", "tests/interoperability/test_qual_206_local_http_preflight.mjs"],
    {
      cwd: ROOT,
      detached: process.platform !== "win32",
      env: environment,
      stdio: ["ignore", "pipe", "pipe"],
    },
  );
  const stdout: string[] = [];
  const stderr: string[] = [];
  let outputBytes = 0;
  let failure: Error | undefined;
  const append = (chunks: string[], label: string, chunk: Buffer): void => {
    outputBytes += chunk.length;
    if (outputBytes > MAX_EXTERNAL_SUITE_OUTPUT_BYTES) {
      failure ??= new Error(`${label} exceeded the external-suite output bound`);
      terminateDetachedProcessGroup(child);
      return;
    }
    chunks.push(chunk.toString("utf8"));
  };
  child.stdout?.on("data", (chunk: Buffer) => append(stdout, "stdout", chunk));
  child.stderr?.on("data", (chunk: Buffer) => append(stderr, "stderr", chunk));
  const timeout = setTimeout(() => {
    failure ??= new Error("Independent local HTTP preflight suite timed out");
    terminateDetachedProcessGroup(child);
  }, timeoutMilliseconds);
  try {
    const [code, signal] = await once(child, "close") as [
      number | null,
      NodeJS.Signals | null,
    ];
    if (failure !== undefined) throw failure;
    assert.equal(signal, null);
    assert.equal(
      code,
      0,
      `Independent local HTTP preflight suite failed:\n${stdout.join("")}\n${stderr.join("")}`,
    );
    return Object.freeze({ stderr: stderr.join(""), stdout: stdout.join("") });
  } finally {
    clearTimeout(timeout);
    terminateDetachedProcessGroup(child);
  }
}

function attachJsonLines(
  stream: Readable,
  values: JsonObject[],
  errors: unknown[],
  emitter: EventEmitter,
): () => string {
  let buffer = "";
  stream.setEncoding("utf8");
  stream.on("data", (chunk: string) => {
    buffer += chunk;
    while (buffer.includes("\n")) {
      const lineEnd = buffer.indexOf("\n");
      const line = buffer.slice(0, lineEnd);
      buffer = buffer.slice(lineEnd + 1);
      if (line.length === 0) continue;
      try {
        const value = JSON.parse(line) as JsonObject;
        values.push(value);
        if (typeof value.event === "string") {
          emitter.emit(`audit:event:${value.event}`, value);
        }
      } catch (error) {
        errors.push(error);
      }
    }
  });
  return () => buffer;
}

interface ChildCloseOutcome {
  readonly code: number | null;
  readonly forced: boolean;
  readonly signal: NodeJS.Signals | null;
}

async function closeChildWithForcedFallback(
  child: ChildProcess,
  childClose: Promise<[number | null, NodeJS.Signals | null]>,
  label: string,
  initiateGracefulClose: () => void,
  gracefulMilliseconds = GRACEFUL_SHUTDOWN_MILLISECONDS,
  forcedMilliseconds = FORCED_SHUTDOWN_MILLISECONDS,
): Promise<ChildCloseOutcome> {
  let outcome: [number | null, NodeJS.Signals | null] | undefined;
  let gracefulFailure: unknown;
  let forced = false;
  try {
    initiateGracefulClose();
    outcome = await withTimeout(
      childClose,
      `${label} graceful close`,
      gracefulMilliseconds,
    );
  } catch (error) {
    gracefulFailure = error;
  } finally {
    if (outcome === undefined) {
      if (child.exitCode === null && child.signalCode === null) {
        forced = true;
        child.kill("SIGKILL");
      }
      try {
        outcome = await withTimeout(
          childClose,
          `${label} forced close`,
          forcedMilliseconds,
        );
      } catch (forcedFailure) {
        if (child.exitCode === null && child.signalCode === null) {
          child.kill("SIGKILL");
        }
        throw new AggregateError(
          [gracefulFailure, forcedFailure].filter(
            (value): value is NonNullable<unknown> => value !== undefined,
          ),
          `${label} did not close after forced termination`,
        );
      }
    }
  }
  if (outcome === undefined) {
    throw new Error(`${label} produced no close outcome`);
  }
  return Object.freeze({
    code: outcome[0],
    forced,
    signal: outcome[1],
  });
}

interface RunningFixture {
  readonly audits: JsonObject[];
  readonly endpoint: URL;
  close(): Promise<JsonObject>;
  waitForAudit(
    event: string,
    predicate?: (value: JsonObject) => boolean,
  ): Promise<JsonObject>;
}

async function startFixture(
  t: TestContext,
  scenario: string,
): Promise<RunningFixture> {
  const child = spawn(
    process.execPath,
    [
      "--import",
      PROVIDER_EGRESS_GUARD,
      SERVER,
      AUTHORITY_ARGUMENT,
      `--scenario=${scenario}`,
    ],
    {
      cwd: ROOT,
      env: {
        [ENABLE_FLAG]: "1",
        [SOURCE_COMMIT_VARIABLE]: SOURCE_COMMIT,
        [AUDIT_FD_VARIABLE]: "3",
      },
      stdio: ["ignore", "pipe", "pipe", "pipe"],
    },
  );
  assert.ok(child.stdout);
  assert.ok(child.stderr);
  const auditStream = child.stdio[3] as Readable | null;
  assert.ok(auditStream);

  const emitter = new EventEmitter();
  const audits: JsonObject[] = [];
  const parseErrors: unknown[] = [];
  let stdout = "";
  let stderr = "";
  child.stdout.setEncoding("utf8");
  child.stderr.setEncoding("utf8");
  child.stdout.on("data", (chunk: string) => {
    stdout += chunk;
  });
  child.stderr.on("data", (chunk: string) => {
    stderr += chunk;
  });
  const auditRemainder = attachJsonLines(
    auditStream,
    audits,
    parseErrors,
    emitter,
  );
  const childClose = once(child, "close") as Promise<[
    number | null,
    NodeJS.Signals | null,
  ]>;
  let closed = false;
  let closeAttempt: Promise<JsonObject> | undefined;

  async function waitForAudit(
    event: string,
    predicate: (value: JsonObject) => boolean = () => true,
  ): Promise<JsonObject> {
    const existing = audits.find(
      (value) => value.event === event && predicate(value),
    );
    if (existing !== undefined) return existing;
    return await withTimeout(
      new Promise<JsonObject>((resolve) => {
        const eventName = `audit:event:${event}`;
        const listener = (value: JsonObject): void => {
          if (!predicate(value)) return;
          emitter.removeListener(eventName, listener);
          resolve(value);
        };
        emitter.on(eventName, listener);
      }),
      `audit event ${event} for ${scenario}`,
    );
  }

  async function closeOnce(): Promise<JsonObject> {
    const termination = await closeChildWithForcedFallback(
      child,
      childClose,
      `scenario ${scenario} process close`,
      () => {
        if (child.exitCode === null && child.signalCode === null) {
          child.kill("SIGTERM");
        }
      },
    );
    closed = true;
    assert.equal(termination.forced, false, "fixture required forced termination");
    assert.equal(termination.signal, null);
    assert.equal(termination.code, 0, stderr);
    assert.equal(stdout, "");
    assert.equal(stderr, "");
    assert.deepEqual(parseErrors, []);
    assert.equal(auditRemainder(), "");

    const ready = audits.filter((value) =>
      value.event === "provider-egress-guard-ready"
    );
    const blocked = audits.filter((value) =>
      value.event === "provider-egress-guard-blocked"
    );
    const guardSummary = audits.filter((value) =>
      value.event === "provider-egress-guard-summary"
    );
    const summaries = audits.filter((value) => value.event === "session-summary");
    assert.equal(ready.length, 1, JSON.stringify(audits));
    assert.equal(blocked.length, 0, JSON.stringify(audits));
    assert.equal(guardSummary.length, 1, JSON.stringify(audits));
    assert.equal(guardSummary[0]?.guarded_api_invocation_count, 0);
    assert.equal(summaries.length, 1, JSON.stringify(audits));
    const summary = summaries[0] as JsonObject;
    assert.equal(summary.schema, AUDIT_SCHEMA);
    assert.equal(summary.scenario, scenario);
    assert.equal(summary.source_commit, SOURCE_COMMIT);
    assert.equal(summary.transport, "operating-system-loopback-http");
    assert.equal(summary.host, "127.0.0.1");
    assert.equal(summary.state, "candidate-unregistered");
    assert.equal(summary.production_registration, false);
    assert.equal(summary.private_state_root_mode, "0700");
    assert.equal(summary.guarded_api_invocation_count, 0);
    return summary;
  }

  function close(): Promise<JsonObject> {
    closeAttempt ??= closeOnce();
    return closeAttempt;
  }

  t.after(async () => {
    if (!closed) await close();
  });

  const listening = await waitForAudit("server-listening");
  assert.equal(listening.schema, AUDIT_SCHEMA);
  assert.equal(listening.scenario, scenario);
  assert.equal(listening.source_commit, SOURCE_COMMIT);
  assert.equal(listening.transport, "operating-system-loopback-http");
  assert.equal(listening.host, "127.0.0.1");
  assert.equal(listening.state, "candidate-unregistered");
  assert.equal(listening.production_registration, false);
  assert.equal(Number.isSafeInteger(listening.port), true);
  const port = listening.port as number;
  assert.ok(port >= 1 && port <= 65_535);
  return Object.freeze({
    audits,
    endpoint: new URL(`http://127.0.0.1:${port}/mcp`),
    close,
    waitForAudit,
  });
}

function rawBody(
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

async function rawExchange(
  endpoint: URL,
  id: number,
  method: string,
  parameters: Readonly<Record<string, unknown>> = {},
  signal?: AbortSignal,
): Promise<{
  readonly response: Response;
  readonly message: JsonObject;
  readonly rawText: string;
}> {
  const name = method === "tools/call" && typeof parameters.name === "string"
    ? parameters.name
    : method === "resources/read" && typeof parameters.uri === "string"
      ? parameters.uri
      : undefined;
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      accept: "application/json, text/event-stream",
      "content-type": "application/json",
      "mcp-method": method,
      "mcp-protocol-version": MCP_PROTOCOL_VERSION,
      ...(name === undefined ? {} : { "mcp-name": name }),
    },
    body: JSON.stringify(rawBody(id, method, parameters)),
    ...(signal === undefined ? {} : { signal }),
  });
  const rawText = await response.text();
  return {
    response,
    message: JSON.parse(rawText) as JsonObject,
    rawText,
  };
}

async function directGet(endpoint: URL, pathname: string): Promise<{
  readonly body: string;
  readonly status: number;
}> {
  return await new Promise((resolve, reject) => {
    const request = nodeRequest(
      {
        hostname: endpoint.hostname,
        port: endpoint.port,
        path: pathname,
        method: "GET",
        headers: {
          accept: "application/json",
          host: "127.0.0.1",
        },
      },
      (response) => {
        const chunks: Buffer[] = [];
        response.on("data", (chunk: Buffer) => chunks.push(chunk));
        response.once("end", () => {
          resolve({
            body: Buffer.concat(chunks).toString("utf8"),
            status: response.statusCode ?? 0,
          });
        });
      },
    );
    request.once("error", reject);
    request.end();
  });
}

function resultOf(message: JsonObject): JsonObject {
  assert.equal(typeof message.result, "object", JSON.stringify(message));
  assert.notEqual(message.result, null);
  return message.result as JsonObject;
}

function errorOf(message: JsonObject): JsonObject {
  assert.equal(typeof message.error, "object", JSON.stringify(message));
  assert.notEqual(message.error, null);
  return message.error as JsonObject;
}

function assertToolParity(
  message: JsonObject,
  operation: string,
  expectedError = false,
): JsonObject {
  const called = resultOf(message);
  assert.equal(called.isError === true, expectedError);
  assert.equal(typeof called.structuredContent, "object");
  assert.notEqual(called.structuredContent, null);
  assert.deepEqual(called.content, [{
    type: "text",
    text: JSON.stringify(called.structuredContent),
  }]);
  const structured = called.structuredContent as JsonObject;
  if (!expectedError) assert.equal(structured.operation, operation);
  return structured;
}

function resourceProjection(operations: readonly string[]): readonly string[] {
  return [
    ...(operations.includes("catalogue.search") &&
      operations.includes("catalogue.describe")
      ? ["catalogue.public"]
      : []),
    ...(operations.includes("catalogue.describe") ? ["catalogue.record"] : []),
    ...(operations.includes("evidence.inspect") ? ["evidence.receipt"] : []),
  ];
}

async function assertDiscovery(
  endpoint: URL,
  operations: readonly string[],
  idOffset = 0,
): Promise<void> {
  const discovered = resultOf((await rawExchange(
    endpoint,
    idOffset + 1,
    "server/discover",
  )).message);
  assert.deepEqual(discovered.supportedVersions, [MCP_PROTOCOL_VERSION]);

  const listed = resultOf((await rawExchange(
    endpoint,
    idOffset + 2,
    "tools/list",
  )).message);
  assert.ok(Array.isArray(listed.tools));
  const listedNames = listed.tools.map((value: unknown) => {
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
  assert.equal(listedNames.every((name: unknown) => typeof name === "string"), true);
  assert.deepEqual(
    [...listedNames].sort(),
    [...operations].sort(),
  );

  const expectedResources = resourceProjection(operations);
  const resources = resultOf((await rawExchange(
    endpoint,
    idOffset + 3,
    "resources/list",
  )).message);
  assert.ok(Array.isArray(resources.resources));
  assert.deepEqual(
    resources.resources.map((value: unknown) => (value as JsonObject).uri),
    expectedResources.includes("catalogue.public") ? [MCP_PUBLIC_CATALOGUE_URI] : [],
  );
  const templates = resultOf((await rawExchange(
    endpoint,
    idOffset + 4,
    "resources/templates/list",
  )).message);
  assert.ok(Array.isArray(templates.resourceTemplates));
  assert.deepEqual(
    templates.resourceTemplates.map(
      (value: unknown) => (value as JsonObject).uriTemplate,
    ),
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

function safeCatalogueCall(operations: readonly string[]): {
  readonly operation: string;
  readonly argumentsValue: Readonly<Record<string, unknown>>;
} {
  if (operations.includes("catalogue.search")) {
    return Object.freeze({
      operation: "catalogue.search",
      argumentsValue: Object.freeze({ query: "INSPIRE", limit: 1 }),
    });
  }
  return Object.freeze({
    operation: "catalogue.describe",
    argumentsValue: Object.freeze({ record_id: "LR-Q003" }),
  });
}

interface RejectedInvocation {
  readonly audit: string;
  readonly code: number | null;
  readonly forced: boolean;
  readonly signal: NodeJS.Signals | null;
  readonly stderr: string;
  readonly stdout: string;
}

async function rejectedInvocation(
  argumentsValue: readonly string[],
  environment: Readonly<Record<string, string>>,
  options: {
    readonly auditPipe?: boolean;
    readonly guard?: boolean;
  } = {},
): Promise<RejectedInvocation> {
  const guardArguments = options.guard === false
    ? []
    : ["--import", PROVIDER_EGRESS_GUARD];
  const auditPipe = options.auditPipe !== false;
  const child = spawn(
    process.execPath,
    [...guardArguments, SERVER, ...argumentsValue],
    {
      cwd: ROOT,
      env: environment,
      stdio: auditPipe
        ? ["ignore", "pipe", "pipe", "pipe"]
        : ["ignore", "pipe", "pipe"],
    },
  );
  assert.ok(child.stdout);
  assert.ok(child.stderr);
  let stdout = "";
  let stderr = "";
  let audit = "";
  child.stdout.setEncoding("utf8");
  child.stderr.setEncoding("utf8");
  child.stdout.on("data", (chunk: string) => {
    stdout += chunk;
  });
  child.stderr.on("data", (chunk: string) => {
    stderr += chunk;
  });
  const auditStream = child.stdio[3] as Readable | null | undefined;
  if (auditStream !== null && auditStream !== undefined) {
    auditStream.setEncoding("utf8");
    auditStream.on("data", (chunk: string) => {
      audit += chunk;
    });
  }
  const termination = await closeChildWithForcedFallback(
    child,
    once(child, "close") as Promise<[number | null, NodeJS.Signals | null]>,
    "rejected HTTP fixture process",
    () => undefined,
  );
  return {
    audit,
    code: termination.code,
    forced: termination.forced,
    signal: termination.signal,
    stderr,
    stdout,
  };
}

function assertRejectedBeforeListening(invocation: RejectedInvocation): void {
  assert.notEqual(invocation.code, 0);
  assert.equal(invocation.forced, false);
  assert.equal(invocation.signal, null);
  assert.equal(invocation.stdout, "");
  assert.equal(invocation.audit.includes('"event":"server-listening"'), false);
  assert.equal(invocation.audit.includes('"event":"session-summary"'), false);
}

test("forces and awaits a child that ignores graceful termination", async (t) => {
  const child = spawn(
    process.execPath,
    [
      "--eval",
      [
        'process.on("SIGTERM", () => undefined);',
        'process.stdout.write("ready\\n");',
        "setInterval(() => undefined, 1_000);",
      ].join(""),
    ],
    { stdio: ["ignore", "pipe", "pipe"] },
  );
  assert.ok(child.stdout);
  const childClose = once(child, "close") as Promise<[
    number | null,
    NodeJS.Signals | null,
  ]>;
  t.after(async () => {
    if (child.exitCode === null && child.signalCode === null) {
      child.kill("SIGKILL");
      await withTimeout(childClose, "forced-fallback regression cleanup");
    }
  });
  await withTimeout(once(child.stdout, "data"), "hung child readiness");
  const termination = await closeChildWithForcedFallback(
    child,
    childClose,
    "hung child regression",
    () => {
      child.kill("SIGTERM");
    },
    50,
    2_000,
  );
  assert.equal(termination.code, null);
  assert.equal(termination.forced, true);
  assert.equal(termination.signal, "SIGKILL");
  assert.notEqual(child.signalCode, null);
});

test("fails closed unless the exact-five HTTP fixture authority is complete", async () => {
  const missingFlag = await rejectedInvocation(
    [AUTHORITY_ARGUMENT, "--scenario=capability-pack"],
    { [SOURCE_COMMIT_VARIABLE]: SOURCE_COMMIT, [AUDIT_FD_VARIABLE]: "3" },
  );
  assertRejectedBeforeListening(missingFlag);
  assert.match(missingFlag.stderr, new RegExp(`${ENABLE_FLAG}=1`, "u"));

  const missingArgument = await rejectedInvocation(
    ["--scenario=capability-pack"],
    {
      [ENABLE_FLAG]: "1",
      [SOURCE_COMMIT_VARIABLE]: SOURCE_COMMIT,
      [AUDIT_FD_VARIABLE]: "3",
    },
  );
  assertRejectedBeforeListening(missingArgument);
  assert.match(missingArgument.stderr, /exact authority and closed scenario/u);

  const unknownScenario = await rejectedInvocation(
    [AUTHORITY_ARGUMENT, "--scenario=not-closed"],
    {
      [ENABLE_FLAG]: "1",
      [SOURCE_COMMIT_VARIABLE]: SOURCE_COMMIT,
      [AUDIT_FD_VARIABLE]: "3",
    },
  );
  assertRejectedBeforeListening(unknownScenario);
  assert.match(unknownScenario.stderr, /exact authority and closed scenario/u);

  const malformedSource = await rejectedInvocation(
    [AUTHORITY_ARGUMENT, "--scenario=capability-pack"],
    {
      [ENABLE_FLAG]: "1",
      [SOURCE_COMMIT_VARIABLE]: "not-a-commit",
      [AUDIT_FD_VARIABLE]: "3",
    },
  );
  assertRejectedBeforeListening(malformedSource);
  assert.match(malformedSource.stderr, /full lowercase Git commit/u);

  const missingGuard = await rejectedInvocation(
    [AUTHORITY_ARGUMENT, "--scenario=capability-pack"],
    {
      [ENABLE_FLAG]: "1",
      [SOURCE_COMMIT_VARIABLE]: SOURCE_COMMIT,
      [AUDIT_FD_VARIABLE]: "3",
    },
    { guard: false },
  );
  assertRejectedBeforeListening(missingGuard);
  assert.match(missingGuard.stderr, /requires its provider egress guard/u);

  const missingAudit = await rejectedInvocation(
    [AUTHORITY_ARGUMENT, "--scenario=capability-pack"],
    { [ENABLE_FLAG]: "1", [SOURCE_COMMIT_VARIABLE]: SOURCE_COMMIT },
    { auditPipe: false },
  );
  assertRejectedBeforeListening(missingAudit);
  assert.equal(missingAudit.audit, "");
  assert.match(missingAudit.stderr, new RegExp(`${AUDIT_FD_VARIABLE}=3`, "u"));
});

test(
  "runs the exact-five journey, cancellation and parity through a real HTTP socket",
  { timeout: 30_000 },
  async (t) => {
    const fixture = await startFixture(t, "capability-pack");
    await assertDiscovery(fixture.endpoint, EXACT_OPERATIONS);

    const publicRead = resultOf((await rawExchange(
      fixture.endpoint,
      5,
      "resources/read",
      { uri: MCP_PUBLIC_CATALOGUE_URI },
    )).message);
    assert.ok(Array.isArray(publicRead.contents));
    const publicContent = publicRead.contents[0] as JsonObject;
    assert.equal(publicContent.uri, MCP_PUBLIC_CATALOGUE_URI);
    assert.doesNotThrow(() => JSON.parse(publicContent.text as string));

    const recordUri = "gis-ai-go://catalogue/records/LR-Q003";
    const recordRead = resultOf((await rawExchange(
      fixture.endpoint,
      6,
      "resources/read",
      { uri: recordUri },
    )).message);
    assert.ok(Array.isArray(recordRead.contents));
    const recordContent = recordRead.contents[0] as JsonObject;
    assert.equal(recordContent.uri, recordUri);
    assert.equal(JSON.parse(recordContent.text as string).id, "LR-Q003");

    const calls: readonly [string, Readonly<Record<string, unknown>>][] = [
      ["catalogue.search", { query: "INSPIRE", limit: 1 }],
      ["catalogue.describe", { record_id: "LR-Q003" }],
      ["selection.resolve", SELECTION_REQUEST],
      ["data.query", DATA_QUERY_REQUEST],
    ];
    const resultsByOperation = new Map<string, JsonObject>();
    for (const [offset, [operation, argumentsValue]] of calls.entries()) {
      const structured = assertToolParity(
        (await rawExchange(
          fixture.endpoint,
          7 + offset,
          "tools/call",
          { name: operation, arguments: argumentsValue },
        )).message,
        operation,
      );
      resultsByOperation.set(operation, structured);
      const receipt = structured.evidence_receipt as JsonObject;
      assert.match(
        receipt.receipt_id as string,
        /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u,
      );
    }

    const searchResult = resultsByOperation.get("catalogue.search");
    assert.ok(searchResult);
    const searchReceipt = (searchResult.evidence_receipt as JsonObject).receipt_id;
    assert.ok(typeof searchReceipt === "string");
    const inspection = assertToolParity(
      (await rawExchange(
        fixture.endpoint,
        11,
        "tools/call",
        {
          name: "evidence.inspect",
          arguments: { receipt_id: searchReceipt },
        },
      )).message,
      "evidence.inspect",
    );
    const inspectedData = inspection.data as JsonObject;
    const inspectedRecord = inspectedData.record as JsonObject;
    const inspectedReceipt = inspectedRecord.receipt as JsonObject;
    assert.equal(inspectedReceipt.receipt_id, searchReceipt);

    const evidenceUri =
      `gis-ai-go://evidence/receipts/${encodeURIComponent(searchReceipt)}`;
    const evidenceRead = resultOf((await rawExchange(
      fixture.endpoint,
      12,
      "resources/read",
      { uri: evidenceUri },
    )).message);
    assert.ok(Array.isArray(evidenceRead.contents));
    const evidenceContent = evidenceRead.contents[0] as JsonObject;
    assert.equal(evidenceContent.uri, evidenceUri);
    const evidenceProjection = JSON.parse(evidenceContent.text as string) as JsonObject;
    const projectedData = evidenceProjection.data as JsonObject;
    const projectedRecord = projectedData.record as JsonObject;
    assert.equal(
      (projectedRecord.receipt as JsonObject).receipt_id,
      searchReceipt,
    );

    const openApiResponse = await directGet(fixture.endpoint, "/openapi.json");
    assert.equal(openApiResponse.status, 200);
    const openApi = JSON.parse(openApiResponse.body) as JsonObject;
    assert.deepEqual(
      [...(openApi["x-gis-ai-go-candidate-operations"] as string[])].sort(),
      [...EXACT_OPERATIONS].sort(),
    );
    assert.equal(openApi["x-gis-ai-go-lifecycle"], "candidate-unregistered");
    assert.equal(openApi["x-gis-ai-go-production-registration"], false);

    const readinessResponse = await directGet(fixture.endpoint, "/readyz");
    assert.equal(readinessResponse.status, 200);
    const readiness = JSON.parse(readinessResponse.body) as JsonObject;
    assert.equal(readiness.production_registration, false);
    assert.deepEqual(
      [...(readiness.active_tools as string[])].sort(),
      [...EXACT_OPERATIONS].sort(),
    );
    assert.deepEqual(
      [...(readiness.active_api_operations as string[])].sort(),
      [...EXACT_OPERATIONS].sort(),
    );

    const controller = new AbortController();
    const started = fixture.waitForAudit(
      "provider-transport-started",
      (value) => value.ordinal === 2,
    );
    const cancelledResponse = rawExchange(
      fixture.endpoint,
      13,
      "tools/call",
      { name: "data.query", arguments: CANCELLED_DATA_QUERY_REQUEST },
      controller.signal,
    );
    await started;
    const aborted = fixture.waitForAudit(
      "provider-transport-aborted",
      (value) => value.ordinal === 2,
    );
    controller.abort(new Error("Caller cancelled the real HTTP request"));
    await assert.rejects(cancelledResponse);
    await aborted;

    const rejected = errorOf((await rawExchange(
      fixture.endpoint,
      14,
      "prompts/list",
    )).message);
    assert.deepEqual(rejected, { code: -32_601, message: "Method not found" });

    const summary = await fixture.close();
    assert.deepEqual(summary.operations, EXACT_OPERATIONS);
    assert.deepEqual(summary.resources, EXACT_RESOURCES);
    assert.deepEqual(summary.suspensions, []);
    assert.equal(summary.provider_transport_calls, 2);
    assert.equal(summary.aborted_provider_calls, 1);
    assert.equal(summary.ledger_event_count, 4);
    assert.equal(summary.reported_error_count, 0);
    assert.deepEqual(
      fixture.audits
        .filter((value) => value.event === "provider-transport-started")
        .map((value) => value.ordinal),
      [1, 2],
    );
    assert.deepEqual(
      fixture.audits
        .filter((value) => value.event === "provider-transport-aborted")
        .map((value) => value.ordinal),
      [2],
    );
  },
);

test(
  "keeps all seven governed suspensions absent and uncallable over real HTTP",
  { timeout: 30_000 },
  async (t) => {
    assert.equal(SUSPENSION_SCENARIOS.length, 7);
    let resultingSuspensions = 0;
    for (const [scenarioIndex, scenario] of SUSPENSION_SCENARIOS.entries()) {
      await t.test(scenario.name, async (t) => {
        const fixture = await startFixture(t, scenario.name);
        await assertDiscovery(fixture.endpoint, scenario.operations, scenarioIndex * 20);
        for (const [offset, suspension] of scenario.suspensions.entries()) {
          const rejected = errorOf((await rawExchange(
            fixture.endpoint,
            100 + (scenarioIndex * 10) + offset,
            "tools/call",
            { name: suspension.operation, arguments: {} },
          )).message);
          assert.deepEqual(rejected, {
            code: -32_602,
            message: `Tool ${suspension.operation} not found`,
          });
        }

        const safe = safeCatalogueCall(scenario.operations);
        assertToolParity(
          (await rawExchange(
            fixture.endpoint,
            190 + scenarioIndex,
            "tools/call",
            { name: safe.operation, arguments: safe.argumentsValue },
          )).message,
          safe.operation,
        );
        const summary = await fixture.close();
        assert.deepEqual(summary.operations, scenario.operations);
        assert.deepEqual(summary.resources, resourceProjection(scenario.operations));
        assert.deepEqual(summary.suspensions, scenario.suspensions);
        assert.equal(summary.provider_transport_calls, 0);
        assert.equal(summary.aborted_provider_calls, 0);
        assert.equal(summary.ledger_event_count, 1);
        assert.equal(summary.reported_error_count, 0);
        resultingSuspensions += scenario.suspensions.length;
      });
    }
    assert.equal(resultingSuspensions, 9);
  },
);

test(
  "runs the owner-only capture and independent-verifier regression suite",
  { timeout: 60_000 },
  async () => {
    const result = await runExternalLocalHttpSuite();
    assert.equal(result.stderr, "");
    assert.match(result.stdout, /\btests 10\b/u);
    assert.match(result.stdout, /\bpass 10\b/u);
  },
);
