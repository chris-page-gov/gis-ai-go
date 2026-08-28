import assert from "node:assert/strict";
import { execFileSync, spawn } from "node:child_process";
import { createHash, randomUUID } from "node:crypto";
import { once } from "node:events";
import { createServer } from "node:net";
import {
  chmodSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  realpathSync,
  rmSync,
  statSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { advertisedToolSchemasExact } from
  "../../scripts/qual_206_exact_five_event_collector.mjs";
import {
  CHATGPT_TUNNEL_OBSERVATION_WINDOWS,
  createChatGptTunnelObservationDeadlines,
  parseChatGptTunnelObserverArguments,
} from
  "../../scripts/qual_206_chatgpt_tunnel_exact_five_observer.mjs";
import {
  measureGeneratedRuntimeClosure,
  measureInstalledDependencyClosure,
} from "../../scripts/qual_206_claude_runtime_closure.mjs";

const ROOT = realpathSync(fileURLToPath(new URL("../../", import.meta.url)));
const OBSERVER = join(
  ROOT,
  "scripts",
  "qual_206_chatgpt_tunnel_exact_five_observer.mjs",
);
const PROFILE = JSON.parse(readFileSync(join(
  ROOT,
  "tests",
  "interoperability",
  "fixtures",
  "qual_206_chatgpt_tunnel_exact_five_profile.v1.json",
), "utf8"));
const AUTHORITY = "--chatgpt-tunnel-exact-five-observation-only";
const ENABLE_FLAG = "GIS_AI_GO_QUAL_206_CHATGPT_TUNNEL_EXACT_FIVE";
const CAPTURE_FLAG = "GIS_AI_GO_QUAL_206_EVENT_CAPTURE";
const NETWORK_SANDBOX_VARIABLE = "GIS_AI_GO_QUAL_206_MCP_NETWORK_SANDBOX";
const HOST_ATTESTATION_VARIABLE = "GIS_AI_GO_QUAL_206_HOST_ATTESTATION";
const PROTOCOL = "2026-07-28";
const SANDBOX_EXEC = "/usr/bin/sandbox-exec";
const NETWORK_SANDBOX_PROFILE = "(version 1) (allow default) (deny network*)";
const OPERATIONS = Object.freeze([
  "catalogue.search",
  "catalogue.describe",
  "selection.resolve",
  "data.query",
  "evidence.inspect",
]);
const PORTABLE_RUNTIME_CLOSURE = Object.freeze({
  generated_first_party_closure: Object.freeze({
    bytes: 123,
    file_count: 4,
    manifest_sha256: "a".repeat(64),
    reference_manifest_sha256: "a".repeat(64),
    reference_matches_current: true,
  }),
  installed_dependency_closure: Object.freeze({
    bytes: 456,
    entry_count: 7,
    manifest_sha256: "b".repeat(64),
  }),
});
const CREDENTIAL_VARIABLES = Object.freeze([
  "OPENAI_API_KEY",
  "CONTROL_PLANE_API_KEY",
  "CODEX_API_KEY",
  "ANTHROPIC_API_KEY",
  "ANTHROPIC_AUTH_TOKEN",
  "CLAUDE_CODE_OAUTH_TOKEN",
  "ANTHROPIC_BASE_URL",
  "AWS_ACCESS_KEY_ID",
  "AWS_SECRET_ACCESS_KEY",
  "AWS_SESSION_TOKEN",
  "GOOGLE_APPLICATION_CREDENTIALS",
  "AZURE_CLIENT_SECRET",
]);
const macRuntimeTest = process.platform === "darwin" ? test : test.skip;
let expectedRuntimeClosure;

function currentCommit() {
  return execFileSync(
    "git",
    ["-C", ROOT, "rev-parse", "--verify", "HEAD^{commit}"],
    { encoding: "utf8" },
  ).trim();
}

function executableIdentity() {
  const executable = realpathSync(process.execPath);
  const bytes = readFileSync(executable);
  return Object.freeze({
    bytes: statSync(executable).size,
    sha256: createHash("sha256").update(bytes).digest("hex"),
  });
}

function runtimeClosure() {
  if (expectedRuntimeClosure !== undefined) return expectedRuntimeClosure;
  const generated = measureGeneratedRuntimeClosure(ROOT);
  expectedRuntimeClosure = Object.freeze({
    generated_first_party_closure: Object.freeze({
      ...generated,
      reference_manifest_sha256: generated.manifest_sha256,
      reference_matches_current: true,
    }),
    installed_dependency_closure: measureInstalledDependencyClosure(ROOT),
  });
  return expectedRuntimeClosure;
}

function privateRoot(t) {
  const path = mkdtempSync(join(
    realpathSync(tmpdir()),
    "gis-ai-go-chatgpt-tunnel-observer-test-",
  ));
  chmodSync(path, 0o700);
  t.after(() => rmSync(path, { recursive: true, force: true }));
  return path;
}

function closedEnvironment(extra = {}) {
  const environment = {
    ...process.env,
    ...extra,
    [ENABLE_FLAG]: "1",
    [CAPTURE_FLAG]: "1",
    [NETWORK_SANDBOX_VARIABLE]: "macos-seatbelt-deny-network",
    [HOST_ATTESTATION_VARIABLE]: "outer-harness-bound-tunnel-client",
  };
  for (const name of CREDENTIAL_VARIABLES) delete environment[name];
  return environment;
}

function observerArguments(captureRoot, runId, closure = runtimeClosure()) {
  const parent = executableIdentity();
  const generated = closure.generated_first_party_closure;
  const installed = closure.installed_dependency_closure;
  return [
    OBSERVER,
    AUTHORITY,
    "--capture-root",
    captureRoot,
    "--run-id",
    runId,
    "--client",
    "fake-chatgpt-tunnel-host",
    "--source-commit",
    currentCommit(),
    "--expected-parent-sha256",
    parent.sha256,
    "--expected-parent-bytes",
    String(parent.bytes),
    "--expected-generated-runtime-bytes",
    String(generated.bytes),
    "--expected-generated-runtime-file-count",
    String(generated.file_count),
    "--expected-generated-runtime-manifest-sha256",
    generated.manifest_sha256,
    "--expected-generated-runtime-reference-manifest-sha256",
    generated.reference_manifest_sha256,
    "--expected-generated-runtime-reference-matches-current",
    "true",
    "--expected-installed-dependency-bytes",
    String(installed.bytes),
    "--expected-installed-dependency-entry-count",
    String(installed.entry_count),
    "--expected-installed-dependency-manifest-sha256",
    installed.manifest_sha256,
  ];
}

function withTimeout(promise, label, milliseconds = 20_000) {
  let timer;
  return Promise.race([
    promise,
    new Promise((_resolve, reject) => {
      timer = setTimeout(
        () => reject(new Error(`Timed out waiting for ${label}`)),
        milliseconds,
      );
    }),
  ]).finally(() => clearTimeout(timer));
}

function lineReader(stream) {
  let buffered = "";
  let ended = false;
  const queued = [];
  const waiters = [];
  stream.setEncoding("utf8");
  stream.on("data", (chunk) => {
    buffered += chunk;
    while (buffered.includes("\n")) {
      const end = buffered.indexOf("\n");
      const line = buffered.slice(0, end);
      buffered = buffered.slice(end + 1);
      if (line === "") continue;
      const value = JSON.parse(line);
      const waiter = waiters.shift();
      if (waiter === undefined) queued.push(value);
      else waiter.resolve(value);
    }
  });
  stream.once("end", () => {
    ended = true;
    for (const waiter of waiters.splice(0)) {
      waiter.reject(new Error("observer output ended before the next response"));
    }
  });
  return () => {
    const value = queued.shift();
    if (value !== undefined) return Promise.resolve(value);
    if (ended) return Promise.reject(new Error("observer output has ended"));
    return new Promise((resolve, reject) => waiters.push({ reject, resolve }));
  };
}

function startObserver(t, captureRoot, runId, argumentsValue = null) {
  const child = spawn(
    process.execPath,
    argumentsValue ?? observerArguments(captureRoot, runId),
    {
    cwd: ROOT,
    env: closedEnvironment(),
    stdio: ["pipe", "pipe", "pipe"],
    },
  );
  let stderr = "";
  child.stderr.setEncoding("utf8");
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  const completion = new Promise((resolve) => {
    child.once("close", (code, signal) => resolve({ code, signal, stderr }));
  });
  t.after(() => {
    if (child.exitCode === null && child.signalCode === null) child.kill("SIGKILL");
  });
  return Object.freeze({
    child,
    completion,
    nextMessage: lineReader(child.stdout),
  });
}

function modernMeta() {
  return {
    "io.modelcontextprotocol/protocolVersion": PROTOCOL,
    "io.modelcontextprotocol/clientCapabilities": {},
    "io.modelcontextprotocol/clientInfo": {
      name: "qual-206-fake-chatgpt-tunnel",
      version: "1.0.0",
    },
  };
}

async function writeFrame(stream, value) {
  await new Promise((resolve, reject) => {
    stream.write(`${JSON.stringify(value)}\n`, (error) => {
      if (error === null || error === undefined) resolve();
      else reject(error);
    });
  });
}

async function request(observer, id, method, parameters = {}) {
  await writeFrame(observer.child.stdin, {
    jsonrpc: "2.0",
    id,
    method,
    params: { ...parameters, _meta: modernMeta() },
  });
  let response;
  try {
    response = await withTimeout(observer.nextMessage(), `${method} response`);
  } catch {
    const { code, signal, stderr } = await withTimeout(
      observer.completion,
      `${method} observer failure`,
    );
    throw new Error(
      `observer ended before ${method}: code=${String(code)} ` +
        `signal=${String(signal)} stderr=${stderr}`,
    );
  }
  assert.equal(response.id, id);
  assert.equal(response.error, undefined, JSON.stringify(response.error));
  return response.result;
}

async function finish(observer) {
  if (!observer.child.stdin.writableEnded) observer.child.stdin.end();
  return await withTimeout(observer.completion, "observer completion");
}

function waitMilliseconds(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

async function finishWithImmediateTunnelStop(observer) {
  if (!observer.child.stdin.writableEnded) observer.child.stdin.end();
  observer.child.kill("SIGTERM");
  return await withTimeout(observer.completion, "tunnel-client observer completion");
}

async function finishWithSignalBeforeEof(observer) {
  observer.child.kill("SIGTERM");
  await waitMilliseconds(25);
  if (!observer.child.stdin.writableEnded) observer.child.stdin.end();
  return await withTimeout(observer.completion, "signal-first observer completion");
}

function sessionEvents(captureRoot, slot) {
  return readFileSync(join(captureRoot, slot, "events.jsonl"), "utf8")
    .trim()
    .split("\n")
    .map((line) => JSON.parse(line));
}

function directChildProcessId(parentPid) {
  const values = execFileSync(
    "/usr/bin/pgrep",
    ["-P", String(parentPid)],
    { encoding: "utf8" },
  ).trim().split(/\s+/u).filter(Boolean).map(Number);
  assert.equal(values.length, 1, `expected one direct fixture child, received ${values}`);
  assert.equal(Number.isSafeInteger(values[0]) && values[0] > 1, true);
  return values[0];
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function anomalyClassifications(captureRoot, slot) {
  return sessionEvents(captureRoot, slot)
    .filter(({ event }) => event === "anomaly")
    .map(({ classification }) => classification);
}

function fakeTimerScheduler() {
  let now = 0;
  let nextId = 0;
  const timers = new Map();
  return Object.freeze({
    advance(milliseconds) {
      const target = now + milliseconds;
      while (true) {
        const due = [...timers.entries()]
          .filter(([, timer]) => timer.at <= target)
          .sort((left, right) => left[1].at - right[1].at)[0];
        if (due === undefined) break;
        timers.delete(due[0]);
        now = due[1].at;
        due[1].callback();
      }
      now = target;
    },
    clearTimer(id) {
      timers.delete(id);
    },
    setTimer(callback, milliseconds) {
      nextId += 1;
      timers.set(nextId, { at: now + milliseconds, callback });
      return nextId;
    },
  });
}

async function sandboxedLoopbackProbe(port) {
  const source = [
    'const { createConnection } = require("node:net");',
    "let complete = false;",
    "const finish = (code, outcome) => {",
    "  if (complete) return;",
    "  complete = true;",
    "  clearTimeout(timer);",
    "  socket.destroy();",
    "  process.stdout.write(`${JSON.stringify(outcome)}\\n`);",
    "  process.exitCode = code;",
    "};",
    `const socket = createConnection({ host: "127.0.0.1", port: ${String(port)} });`,
    "const timer = setTimeout(() => finish(4, { error: \"timeout\" }), 2000);",
    "socket.once(\"connect\", () => finish(3, { error: null }));",
    "socket.once(\"error\", (error) => finish(",
    "  error.code === \"EPERM\" || error.code === \"EACCES\" ? 0 : 5,",
    "  { error: error.code || \"unknown\" },",
    "));",
  ].join("\n");
  const child = spawn(SANDBOX_EXEC, [
    "-p",
    NETWORK_SANDBOX_PROFILE,
    process.execPath,
    "-e",
    source,
  ], {
    env: { LANG: "C", LC_ALL: "C", PATH: "/usr/bin:/bin" },
    stdio: ["ignore", "pipe", "pipe"],
  });
  let stdout = "";
  let stderr = "";
  child.stdout.setEncoding("utf8");
  child.stderr.setEncoding("utf8");
  child.stdout.on("data", (chunk) => { stdout += chunk; });
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  const [code, signal] = await withTimeout(once(child, "close"), "sandbox probe");
  return { code, signal, stderr, value: JSON.parse(stdout) };
}

test("the observer requires every bounded authority marker and rejects credentials", () => {
  const parent = executableIdentity();
  const closure = PORTABLE_RUNTIME_CLOSURE;
  const argumentsValue = observerArguments(
    realpathSync(tmpdir()),
    randomUUID(),
    closure,
  ).slice(1);
  assert.throws(
    () => parseChatGptTunnelObserverArguments(argumentsValue, {}),
    new RegExp(`${ENABLE_FLAG}=1`, "u"),
  );
  for (const name of CREDENTIAL_VARIABLES) {
    assert.throws(
      () => parseChatGptTunnelObserverArguments(argumentsValue, {
        ...closedEnvironment(),
        [name]: "present",
      }),
      /recognised credential variable/u,
    );
  }
  const parsed = parseChatGptTunnelObserverArguments(
    argumentsValue,
    closedEnvironment(),
  );
  assert.equal(parsed.expectedParentBytes, parent.bytes);
  assert.equal(parsed.expectedParentSha256, parent.sha256);
  assert.deepEqual(parsed.expectedRuntimeClosure, closure);
});

test("observation deadlines separate attach, inter-frame and overall limits", () => {
  assert.deepEqual(CHATGPT_TUNNEL_OBSERVATION_WINDOWS, {
    pre_first_frame_milliseconds: 600_000,
    inter_frame_idle_milliseconds: 180_000,
    overall_observation_milliseconds: 900_000,
  });

  const firstScheduler = fakeTimerScheduler();
  const firstTimeouts = [];
  createChatGptTunnelObservationDeadlines({
    onTimeout: (value) => firstTimeouts.push(value),
    setTimer: firstScheduler.setTimer,
    clearTimer: firstScheduler.clearTimer,
  });
  firstScheduler.advance(599_999);
  assert.deepEqual(firstTimeouts, []);
  firstScheduler.advance(1);
  assert.deepEqual(firstTimeouts, ["pre-first-frame-timeout"]);

  const idleScheduler = fakeTimerScheduler();
  const idleTimeouts = [];
  const idle = createChatGptTunnelObservationDeadlines({
    onTimeout: (value) => idleTimeouts.push(value),
    setTimer: idleScheduler.setTimer,
    clearTimer: idleScheduler.clearTimer,
  });
  idle.hostFrame();
  idleScheduler.advance(179_999);
  idle.activity();
  idleScheduler.advance(179_999);
  assert.deepEqual(idleTimeouts, []);
  idleScheduler.advance(1);
  assert.deepEqual(idleTimeouts, ["inter-frame-idle-timeout"]);

  const overallScheduler = fakeTimerScheduler();
  const overallTimeouts = [];
  const overall = createChatGptTunnelObservationDeadlines({
    onTimeout: (value) => overallTimeouts.push(value),
    setTimer: overallScheduler.setTimer,
    clearTimer: overallScheduler.clearTimer,
  });
  overall.hostFrame();
  for (let elapsed = 170_000; elapsed <= 850_000; elapsed += 170_000) {
    overallScheduler.advance(170_000);
    overall.activity();
  }
  overallScheduler.advance(50_000);
  assert.deepEqual(overallTimeouts, ["observation-timeout"]);
});

macRuntimeTest("the reviewed macOS sandbox denies a node:net loopback connection", async (t) => {
  const bytes = readFileSync(SANDBOX_EXEC);
  assert.equal(bytes.length, 102_560);
  assert.equal(
    createHash("sha256").update(bytes).digest("hex"),
    "8290e4be7387a0df83cd1559e86afd880464f269450573d012795761fe298f16",
  );
  const server = createServer();
  t.after(() => server.close());
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  const address = server.address();
  assert.notEqual(address, null);
  const result = await sandboxedLoopbackProbe(address.port);
  assert.deepEqual(result, {
    code: 0,
    signal: null,
    stderr: "",
    value: { error: "EPERM" },
  });
});

macRuntimeTest("v0.0.13 immediate managed stop records its observed teardown order", async (t) => {
  const captureRoot = privateRoot(t);
  const observer = startObserver(t, captureRoot, randomUUID());
  await request(observer, "discover-1", "server/discover");
  const completion = await finishWithImmediateTunnelStop(observer);
  assert.deepEqual(completion, { code: 0, signal: null, stderr: "" });
  const events = sessionEvents(captureRoot, "session-1");
  const teardown = events.find(({ phase }) => phase === "parent-teardown-signal");
  assert.equal(teardown?.signal, "SIGTERM");
  assert.equal(teardown?.immediate_parent_verified, true);
  const pair = [
    teardown?.stdin_closed_before_signal,
    teardown?.stdin_eof_observed_within_grace,
  ];
  assert.equal(
    JSON.stringify(pair) === JSON.stringify([true, false]) ||
      JSON.stringify(pair) === JSON.stringify([false, true]),
    true,
  );
  assert.equal(
    events.find(({ phase }) => phase === "session-end").closure_stimulus,
    pair[0] ? "stdin-eof-and-sigterm" : "sigterm-then-stdin-eof",
  );
});

macRuntimeTest("SIGTERM followed by EOF within grace is a clean truthful teardown", async (t) => {
  const captureRoot = privateRoot(t);
  const observer = startObserver(t, captureRoot, randomUUID());
  await request(observer, "discover-1", "server/discover");
  const completion = await finishWithSignalBeforeEof(observer);
  assert.deepEqual(completion, { code: 0, signal: null, stderr: "" });
  const events = sessionEvents(captureRoot, "session-1");
  const teardown = events.find(({ phase }) => phase === "parent-teardown-signal");
  assert.deepEqual({
    signal: teardown?.signal,
    stdin_closed_before_signal: teardown?.stdin_closed_before_signal,
    stdin_eof_observed_within_grace: teardown?.stdin_eof_observed_within_grace,
    immediate_parent_verified: teardown?.immediate_parent_verified,
  }, {
    signal: "SIGTERM",
    stdin_closed_before_signal: false,
    stdin_eof_observed_within_grace: true,
    immediate_parent_verified: true,
  });
  assert.equal(
    events.find(({ phase }) => phase === "session-end").closure_stimulus,
    "sigterm-then-stdin-eof",
  );
});

macRuntimeTest("SIGTERM without stdin EOF fails closed after the bounded grace", async (t) => {
  const captureRoot = privateRoot(t);
  const observer = startObserver(t, captureRoot, randomUUID());
  await request(observer, "discover-1", "server/discover");
  observer.child.kill("SIGTERM");
  const completion = await withTimeout(observer.completion, "premature SIGTERM rejection");
  assert.equal(completion.code, 2, completion.stderr);
  assert.deepEqual(
    anomalyClassifications(captureRoot, "session-1"),
    ["premature-parent-sigterm"],
  );
  const events = sessionEvents(captureRoot, "session-1");
  assert.equal(events.some(({ phase }) => phase === "parent-teardown-signal"), false);
  assert.equal(
    events.find(({ phase }) => phase === "session-end")?.protocol_session_status,
    "failed",
  );
});

macRuntimeTest("a partial host frame remains fatal during signal-first teardown", async (t) => {
  const captureRoot = privateRoot(t);
  const observer = startObserver(t, captureRoot, randomUUID());
  await request(observer, "discover-1", "server/discover");
  await new Promise((resolve, reject) => {
    observer.child.stdin.write('{"jsonrpc":"2.0"', (error) => {
      if (error === null || error === undefined) resolve();
      else reject(error);
    });
  });
  const completion = await finishWithSignalBeforeEof(observer);
  assert.equal(completion.code, 2, completion.stderr);
  assert.deepEqual(
    anomalyClassifications(captureRoot, "session-1"),
    ["truncated-frame"],
  );
});

macRuntimeTest("host bytes after SIGTERM cannot widen the accepted observation", async (t) => {
  const captureRoot = privateRoot(t);
  const observer = startObserver(t, captureRoot, randomUUID());
  await request(observer, "discover-1", "server/discover");
  observer.child.kill("SIGTERM");
  await waitMilliseconds(25);
  await writeFrame(observer.child.stdin, {
    jsonrpc: "2.0",
    id: "late-list",
    method: "tools/list",
    params: { _meta: modernMeta() },
  });
  if (!observer.child.stdin.writableEnded) observer.child.stdin.end();
  const completion = await withTimeout(observer.completion, "late host bytes rejection");
  assert.equal(completion.code, 2, completion.stderr);
  assert.deepEqual(
    anomalyClassifications(captureRoot, "session-1"),
    ["host-bytes-after-parent-teardown-signal"],
  );
});

macRuntimeTest("fixture close before parent stdin EOF poisons teardown", async (t) => {
  const captureRoot = privateRoot(t);
  const observer = startObserver(t, captureRoot, randomUUID());
  await request(observer, "discover-1", "server/discover");
  const fixturePid = directChildProcessId(observer.child.pid);
  observer.child.kill("SIGTERM");
  await waitMilliseconds(25);
  process.kill(-fixturePid, "SIGTERM");
  await waitMilliseconds(25);
  if (!observer.child.stdin.writableEnded) observer.child.stdin.end();
  const completion = await withTimeout(observer.completion, "fixture close rejection");
  assert.equal(completion.code, 2, completion.stderr);
  assert.deepEqual(
    anomalyClassifications(captureRoot, "session-1"),
    ["fixture-close-before-parent-stdin-eof"],
  );
});

macRuntimeTest("runtime closure drift is rejected before fixture launch", async (t) => {
  const captureRoot = privateRoot(t);
  const runId = randomUUID();
  const argumentsValue = observerArguments(captureRoot, runId);
  const manifestOption = argumentsValue.indexOf(
    "--expected-installed-dependency-manifest-sha256",
  );
  argumentsValue[manifestOption + 1] = "0".repeat(64);
  const observer = startObserver(t, captureRoot, runId, argumentsValue);
  const completion = await withTimeout(observer.completion, "runtime closure rejection");
  assert.equal(completion.code, 2);
  assert.match(completion.stderr, /runtime closure does not match/u);
  assert.deepEqual(readdirSync(captureRoot), []);
});

macRuntimeTest(
  "a fake tunnel host completes discovery then one canonical exact-five session",
  async (t) => {
  const captureRoot = privateRoot(t);
  const runId = randomUUID();

  const discovery = startObserver(t, captureRoot, runId);
  const discovered = await request(discovery, "discover-1", "server/discover");
  assert.deepEqual(discovered.supportedVersions, [PROTOCOL]);
  assert.deepEqual(await finish(discovery), { code: 0, signal: null, stderr: "" });

  const exactFive = startObserver(t, captureRoot, runId);
  // ChatGPT's current MCP 2026-07-28 client reuses integer 0 after each
  // completed response. This is valid because no request with that ID remains
  // in flight.
  const listing = await request(exactFive, 0, "tools/list");
  assert.equal(advertisedToolSchemasExact(listing.tools), true);
  assert.deepEqual(
    listing.tools.map(({ name }) => name).sort(),
    [...OPERATIONS].sort(),
  );
  const evidenceInput = listing.tools.find(
    ({ name }) => name === "evidence.inspect",
  ).inputSchema;
  assert.equal(Object.hasOwn(evidenceInput, "oneOf"), true);
  assert.equal(Object.hasOwn(evidenceInput, "$defs"), true);

  let searchReceiptId = null;
  for (const [index, operation] of PROFILE.operations.entries()) {
    const argumentsValue = operation.name === "evidence.inspect"
      ? { receipt_id: searchReceiptId }
      : operation.arguments;
    const result = await request(exactFive, 0, "tools/call", {
      name: operation.name,
      arguments: argumentsValue,
    });
    if (operation.name === "catalogue.search") {
      searchReceiptId = result.structuredContent.evidence_receipt.receipt_id;
    }
  }
  assert.match(
    searchReceiptId,
    /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u,
  );
  assert.deepEqual(
    await finishWithSignalBeforeEof(exactFive),
    { code: 0, signal: null, stderr: "" },
  );

  assert.deepEqual(readdirSync(captureRoot).sort(), [
    "exact-five-v1.claim.json",
    "session-1",
    "session-2",
  ]);
  const negotiationSummary = readJson(join(
    captureRoot,
    "session-1",
    "exact-five-session.json",
  ));
  assert.equal(negotiationSummary.slot, "session-1");
  assert.equal(negotiationSummary.session_profile, "negotiation-probe");
  assert.equal(negotiationSummary.result_material, null);

  const summary = readJson(join(captureRoot, "session-2", "exact-five-session.json"));
  assert.equal(summary.slot, "session-2");
  assert.equal(summary.session_profile, "exact-five-session");
  assert.equal(summary.protocol_session_status, "passed");
  assert.equal(summary.capability_scored, false);
  assert.deepEqual(summary.canonical_tool_schema, {
    observed: true,
    exact: true,
    tools_sha256: summary.canonical_tool_schema.tools_sha256,
    projection_applied: false,
  });
  assert.match(summary.canonical_tool_schema.tools_sha256, /^[0-9a-f]{64}$/u);
  assert.deepEqual(
    summary.operations.map(({ response }) => response.operation),
    OPERATIONS,
  );
  assert.equal(summary.inspection_relationship.valid, true);
  assert.equal(summary.audit.provider_transport_calls, 1);
  assert.equal(summary.audit.aborted_provider_calls, 0);
  assert.equal(summary.audit.guarded_api_invocations, 0);
  assert.equal(summary.audit.ledger_event_count, 4);
  assert.equal(summary.result_material.name, "exact-five-results.json");
  const exactFiveEvents = sessionEvents(captureRoot, "session-2");
  const exactFiveTeardown = exactFiveEvents.find(
    ({ phase }) => phase === "parent-teardown-signal",
  );
  assert.deepEqual({
    stdin_closed_before_signal: exactFiveTeardown?.stdin_closed_before_signal,
    stdin_eof_observed_within_grace:
      exactFiveTeardown?.stdin_eof_observed_within_grace,
    closure_stimulus: exactFiveEvents.find(
      ({ phase }) => phase === "session-end",
    )?.closure_stimulus,
  }, {
    stdin_closed_before_signal: false,
    stdin_eof_observed_within_grace: true,
    closure_stimulus: "sigterm-then-stdin-eof",
  });

  const resultMaterial = readJson(join(
    captureRoot,
    "session-2",
    "exact-five-results.json",
  ));
  assert.deepEqual(
    resultMaterial.results.map(({ method }) => method),
    ["tools/list", ...OPERATIONS.map(() => "tools/call")],
  );
  const capturedListing = resultMaterial.results[0].result;
  assert.deepEqual(capturedListing, listing);
  assert.equal(advertisedToolSchemasExact(capturedListing.tools), true);
  },
);

macRuntimeTest(
  "a wrong order claims the run and prevents split call-bearing sessions",
  async (t) => {
  const captureRoot = privateRoot(t);
  const runId = randomUUID();
  const first = startObserver(t, captureRoot, runId);
  await request(first, "list-1", "tools/list");
  await writeFrame(first.child.stdin, {
    jsonrpc: "2.0",
    id: "call-wrong-order",
    method: "tools/call",
    params: {
      name: PROFILE.operations[1].name,
      arguments: PROFILE.operations[1].arguments,
      _meta: modernMeta(),
    },
  });
  first.child.stdin.end();
  const firstCompletion = await withTimeout(first.completion, "wrong-order rejection");
  assert.equal(firstCompletion.code, 2, firstCompletion.stderr);
  assert.deepEqual(
    anomalyClassifications(captureRoot, "session-1"),
    ["journey-order-or-input-drift"],
  );

  const second = startObserver(t, captureRoot, runId);
  await request(second, "list-2", "tools/list");
  await writeFrame(second.child.stdin, {
    jsonrpc: "2.0",
    id: "call-split-session",
    method: "tools/call",
    params: {
      name: PROFILE.operations[0].name,
      arguments: PROFILE.operations[0].arguments,
      _meta: modernMeta(),
    },
  });
  second.child.stdin.end();
  const secondCompletion = await withTimeout(second.completion, "split-session rejection");
  assert.equal(secondCompletion.code, 2, secondCompletion.stderr);
  assert.deepEqual(
    anomalyClassifications(captureRoot, "session-2"),
    ["exact-five-call-already-claimed"],
  );
  },
);
