import assert from "node:assert/strict";
import { execFileSync, spawn } from "node:child_process";
import { createHash, randomUUID } from "node:crypto";
import { once } from "node:events";
import { createRequire } from "node:module";
import {
  chmodSync,
  lstatSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  realpathSync,
  rmSync,
  statSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  canonicalJson,
  domainSeparatedSha256,
} from "../../packages/evidence/dist/src/index.js";
import {
  createBoundedChildCloser,
  GRACEFUL_CLOSE_KILL_MILLISECONDS,
  GRACEFUL_CLOSE_TERM_MILLISECONDS,
  parseClaudeObserverArguments,
} from "../../scripts/qual_206_claude_stdio_observer.mjs";

const ROOT = fileURLToPath(new URL("../../", import.meta.url));
const gatewayRequire = createRequire(join(ROOT, "apps", "mcp-gateway", "package.json"));
const { AjvJsonSchemaValidator } = gatewayRequire(
  "@modelcontextprotocol/server/validators/ajv",
);
const OBSERVER = join(ROOT, "scripts", "qual_206_claude_stdio_observer.mjs");
const FIXTURE = join(
  ROOT,
  "tests",
  "interoperability",
  "fixtures",
  "qual_206_strict_modern_event_server.mjs",
);
const EVENT_SCHEMA_PATH = join(
  ROOT,
  "schemas",
  "qual-206-claude-composite-host-event-v1.schema.json",
);
const MANIFEST_SCHEMA_PATH = join(
  ROOT,
  "schemas",
  "qual-206-claude-composite-host-event-capture-v1.schema.json",
);
const CAPTURE_FLAG = "GIS_AI_GO_QUAL_206_EVENT_CAPTURE";
const AUTHORITY = "--claude-composite-observation-only";
const EVENT_SCHEMA = "gis-ai-go.qual-206-claude-composite-host-event.v1";
const MANIFEST_SCHEMA =
  "gis-ai-go.qual-206-claude-composite-host-event-capture.v1";
const PROTOCOL_TARGET = "2026-07-28";
const CREDENTIAL_VARIABLES = Object.freeze([
  "OPENAI_API_KEY",
  "CODEX_API_KEY",
  "ANTHROPIC_API_KEY",
  "ANTHROPIC_AUTH_TOKEN",
  "CLAUDE_CODE_OAUTH_TOKEN",
  "AWS_ACCESS_KEY_ID",
  "AWS_SECRET_ACCESS_KEY",
  "AWS_SESSION_TOKEN",
  "GOOGLE_APPLICATION_CREDENTIALS",
  "AZURE_CLIENT_SECRET",
]);
const PRIVATE_SENTINEL = "observer-private-environment-sentinel-87c442";
const schemaValidator = new AjvJsonSchemaValidator();
const validateEvent = schemaValidator.getValidator(
  JSON.parse(readFileSync(EVENT_SCHEMA_PATH, "utf8")),
);
const validateManifest = schemaValidator.getValidator(
  JSON.parse(readFileSync(MANIFEST_SCHEMA_PATH, "utf8")),
);

function currentCommit() {
  return execFileSync(
    "git",
    ["-C", ROOT, "rev-parse", "--verify", "HEAD^{commit}"],
    { encoding: "utf8" },
  ).trim();
}

function executableIdentity() {
  const executable = realpathSync(process.execPath);
  return Object.freeze({
    bytes: statSync(executable).size,
    sha256: createHash("sha256").update(readFileSync(executable)).digest("hex"),
  });
}

function privateRoot(t) {
  const path = mkdtempSync(join(realpathSync(tmpdir()), "gis-ai-go-claude-observer-test-"));
  chmodSync(path, 0o700);
  t.after(() => rmSync(path, { recursive: true, force: true }));
  return path;
}

function closedEnvironment(extra = {}) {
  const environment = { ...process.env, ...extra, [CAPTURE_FLAG]: "1" };
  for (const name of CREDENTIAL_VARIABLES) delete environment[name];
  environment.QUAL_206_PRIVATE_SENTINEL = PRIVATE_SENTINEL;
  return environment;
}

function observerArguments(captureRoot, runId, client = "claude-observer-test") {
  const parent = executableIdentity();
  return [
    OBSERVER,
    AUTHORITY,
    "--capture-root",
    captureRoot,
    "--run-id",
    runId,
    "--client",
    client,
    "--source-commit",
    currentCommit(),
    "--expected-parent-sha256",
    parent.sha256,
    "--expected-parent-bytes",
    String(parent.bytes),
  ];
}

function lineReader(stream) {
  let buffered = "";
  const queued = [];
  const waiters = [];
  stream.setEncoding("utf8");
  stream.on("data", (chunk) => {
    buffered += chunk;
    while (true) {
      const newline = buffered.indexOf("\n");
      if (newline < 0) break;
      const line = buffered.slice(0, newline);
      buffered = buffered.slice(newline + 1);
      if (line.length === 0) continue;
      const value = JSON.parse(line);
      const waiter = waiters.shift();
      if (waiter === undefined) queued.push(value);
      else waiter.resolve(value);
    }
  });
  return () => {
    const queuedValue = queued.shift();
    if (queuedValue !== undefined) return Promise.resolve(queuedValue);
    return new Promise((resolve, reject) => waiters.push({ reject, resolve }));
  };
}

function withTimeout(promise, label, milliseconds = 20_000) {
  let timer;
  return Promise.race([
    promise,
    new Promise((_resolve, reject) => {
      timer = setTimeout(() => reject(new Error(`Timed out waiting for ${label}`)), milliseconds);
    }),
  ]).finally(() => clearTimeout(timer));
}

function startObserver(captureRoot, runId, options = {}) {
  const child = spawn(
    process.execPath,
    observerArguments(captureRoot, runId, options.client),
    {
      cwd: ROOT,
      env: options.environment ?? closedEnvironment(),
      stdio: ["pipe", "pipe", "pipe"],
    },
  );
  let stderr = "";
  child.stderr.setEncoding("utf8");
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  const completion = new Promise((resolve) => {
    child.once("close", (code, signal) => resolve({ code, signal, stderr }));
  });
  return Object.freeze({
    child,
    completion,
    nextMessage: lineReader(child.stdout),
  });
}

function directFixturePid(observerPid) {
  const output = execFileSync(
    "/usr/bin/pgrep",
    ["-P", String(observerPid)],
    { encoding: "utf8" },
  ).trim();
  const values = output.split("\n").filter(Boolean).map(Number);
  assert.equal(values.length, 1, output);
  assert.equal(Number.isSafeInteger(values[0]) && values[0] > 1, true);
  return values[0];
}

async function assertProcessExited(pid, label, milliseconds = 750) {
  const deadline = Date.now() + milliseconds;
  while (Date.now() < deadline) {
    try {
      process.kill(pid, 0);
    } catch (error) {
      if (error?.code === "ESRCH") return;
      throw error;
    }
    await new Promise((resolve) => setTimeout(resolve, 10));
  }
  assert.fail(`${label} process ${pid} survived its observer`);
}

function modernMeta(clientName, clientVersion) {
  return {
    "io.modelcontextprotocol/protocolVersion": PROTOCOL_TARGET,
    "io.modelcontextprotocol/clientCapabilities": {},
    "io.modelcontextprotocol/clientInfo": {
      name: clientName,
      version: clientVersion,
    },
  };
}

function requestFrame(id, method, clientName, clientVersion) {
  return {
    jsonrpc: "2.0",
    id,
    method,
    params: { _meta: modernMeta(clientName, clientVersion) },
  };
}

function writeFrame(stream, value) {
  return new Promise((resolve, reject) => {
    stream.write(`${JSON.stringify(value)}\n`, (error) => {
      if (error === null || error === undefined) resolve();
      else reject(error);
    });
  });
}

function writeRawFrame(stream, value) {
  return new Promise((resolve, reject) => {
    stream.write(`${value}\n`, (error) => {
      if (error === null || error === undefined) resolve();
      else reject(error);
    });
  });
}

function readEvents(path) {
  return readFileSync(path, "utf8")
    .split("\n")
    .filter((line) => line.length > 0)
    .map((line) => JSON.parse(line));
}

async function waitForCapturedEvent(captureRoot, predicate, label) {
  const deadline = Date.now() + 10_000;
  while (Date.now() < deadline) {
    for (const slot of readdirSync(captureRoot)) {
      const path = join(captureRoot, slot, "events.jsonl");
      try {
        const match = readEvents(path).find(predicate);
        if (match !== undefined) return match;
      } catch (error) {
        if (error?.code !== "ENOENT") throw error;
      }
    }
    await new Promise((resolve) => setTimeout(resolve, 10));
  }
  throw new Error(`Timed out waiting for ${label}`);
}

function verifyCapture(slotPath, expectedRunId) {
  assert.deepEqual(readdirSync(slotPath).sort(), ["events.jsonl", "manifest.json"]);
  assert.equal(lstatSync(slotPath).mode & 0o777, 0o700);
  const eventPath = join(slotPath, "events.jsonl");
  const manifestPath = join(slotPath, "manifest.json");
  assert.equal(lstatSync(eventPath).mode & 0o777, 0o600);
  assert.equal(lstatSync(manifestPath).mode & 0o777, 0o600);
  const eventBytes = readFileSync(eventPath);
  const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
  const events = readEvents(eventPath);
  const manifestValidation = validateManifest(manifest);
  assert.equal(manifestValidation.valid, true, JSON.stringify(manifestValidation));
  assert.equal(manifest.schema, MANIFEST_SCHEMA);
  assert.equal(manifest.event_schema, EVENT_SCHEMA);
  assert.equal(manifest.run_id, expectedRunId);
  assert.equal(manifest.status, "complete");
  assert.equal(manifest.capability_scored, false);
  assert.equal(manifest.host_capability, false);
  assert.equal(manifest.source_binding_ready, false);
  assert.equal(manifest.event_log.bytes, eventBytes.length);
  assert.equal(manifest.event_log.event_count, events.length);
  assert.equal(
    manifest.event_log.sha256,
    createHash("sha256").update(eventBytes).digest("hex"),
  );
  assert.equal(manifest.event_log.last_event_sha256, events.at(-1).event_sha256);
  for (const [index, event] of events.entries()) {
    const eventValidation = validateEvent(event);
    assert.equal(eventValidation.valid, true, JSON.stringify(eventValidation));
    assert.equal(event.schema, EVENT_SCHEMA);
    assert.equal(event.run_id, expectedRunId);
    assert.equal(event.sequence, index);
    assert.equal(event.previous_event_sha256, index === 0 ? null : events[index - 1].event_sha256);
    const core = { ...event };
    delete core.event_sha256;
    assert.equal(event.event_sha256, domainSeparatedSha256(EVENT_SCHEMA, core));
  }
  assert.equal(events[0].event, "lifecycle");
  assert.equal(events[0].phase, "session-start");
  assert.equal(events[0].credential_environment_observed, false);
  assert.equal(events[0].credential_environment_forwarded, false);
  assert.equal(
    events[0].observer_runtime.fixture_source_sha256,
    createHash("sha256").update(readFileSync(FIXTURE)).digest("hex"),
  );
  assert.equal(events.at(-1).event, "lifecycle");
  assert.equal(events.at(-1).phase, "session-end");
  return { events, manifest, text: eventBytes.toString("utf8") };
}

test("fixed-order authority arguments and environment gate are fail closed", () => {
  const root = realpathSync(tmpdir());
  const parent = executableIdentity();
  const runId = randomUUID();
  const args = observerArguments(root, runId).slice(1);
  const parsed = parseClaudeObserverArguments(args, { [CAPTURE_FLAG]: "1" });
  assert.equal(parsed.captureRoot, root);
  assert.equal(parsed.runId, runId);
  assert.equal(parsed.expectedParentBytes, parent.bytes);
  assert.throws(() => parseClaudeObserverArguments(args, {}), /without/);
  const shuffled = [...args];
  [shuffled[1], shuffled[3]] = [shuffled[3], shuffled[1]];
  assert.throws(
    () => parseClaudeObserverArguments(shuffled, { [CAPTURE_FLAG]: "1" }),
    /expected exact argument/,
  );
});

test("closed event variants reject properties belonging to another event type", () => {
  const request = {
    schema: EVENT_SCHEMA,
    run_id: randomUUID(),
    session_id: randomUUID(),
    slot: "session-1",
    sequence: 0,
    observed_at: "2026-08-25T10:00:00.000Z",
    event: "request",
    previous_event_sha256: null,
    event_sha256: "1".repeat(64),
    direction: "host-to-fixture",
    frame_bytes: 128,
    frame_sha256: "2".repeat(64),
    request_ordinal: 0,
    request_id_sha256: "3".repeat(64),
    request_id_kind: "string",
    request_id_unique: true,
    method: "tools/list",
    operation: "not-applicable",
    protocol_claim: PROTOCOL_TARGET,
  };
  assert.equal(validateEvent(request).valid, true);
  assert.equal(validateEvent({ ...request, request_count: 1 }).valid, false);
  assert.equal(validateEvent({ ...request, audit_kind: "session-summary" }).valid, false);
});

test("bounded closer kills a real child which ignores EOF and TERM below one second", async (t) => {
  const adversary = spawn(
    process.execPath,
    [
      "-e",
      "process.on('SIGTERM',()=>process.stdout.write(JSON.stringify('term')+'\\n'));" +
        "process.stdin.resume();process.stdout.write(JSON.stringify('ready')+'\\n');" +
        "setInterval(()=>{},1000)",
    ],
    { stdio: ["pipe", "pipe", "pipe"] },
  );
  const nextMessage = lineReader(adversary.stdout);
  assert.equal(await withTimeout(nextMessage(), "adversarial child ready"), "ready");
  const started = process.hrtime.bigint();
  const closer = createBoundedChildCloser({
    endInput: () => adversary.stdin.end(),
    signal: (signal) => adversary.kill(signal),
  });
  assert.equal(closer.begin(), true);
  assert.equal(closer.begin(), false);
  assert.equal(await withTimeout(nextMessage(), "adversarial TERM"), "term");
  const [code, signal] = await withTimeout(once(adversary, "close"), "adversarial KILL");
  closer.clear();
  const elapsedMs = Number(process.hrtime.bigint() - started) / 1_000_000;
  assert.equal(code, null);
  assert.equal(signal, "SIGKILL");
  assert.ok(
    elapsedMs >= GRACEFUL_CLOSE_KILL_MILLISECONDS - 50,
    `adversarial child died unexpectedly early at ${elapsedMs.toFixed(1)} ms`,
  );
  assert.ok(elapsedMs <= 900, `adversarial close took ${elapsedMs.toFixed(1)} ms`);
  t.diagnostic(`Non-cooperative child close timing: ${elapsedMs.toFixed(1)} ms`);
  assert.ok(GRACEFUL_CLOSE_TERM_MILLISECONDS < GRACEFUL_CLOSE_KILL_MILLISECONDS);
  assert.ok(GRACEFUL_CLOSE_KILL_MILLISECONDS < 1_000);
});

test("probe and modern sessions allocate unique private slots and close manifests", async (t) => {
  const captureRoot = privateRoot(t);
  const runId = randomUUID();
  const probeId = "private-probe-request-68f497";
  const modernId = "private-tools-request-43a81e";
  const probeClient = "private-probe-client-1786";
  const modernClient = "private-tools-client-6249";
  const version = "private-client-version-9897";
  const probe = startObserver(captureRoot, runId);
  const modern = startObserver(captureRoot, runId);
  await Promise.all([
    writeFrame(probe.child.stdin, requestFrame(
      probeId,
      "server/discover",
      probeClient,
      version,
    )),
    writeFrame(modern.child.stdin, requestFrame(
      modernId,
      "tools/list",
      modernClient,
      version,
    )),
  ]);
  const [probeReply, modernReply] = await Promise.all([
    withTimeout(probe.nextMessage(), "probe reply"),
    withTimeout(modern.nextMessage(), "tools/list reply"),
  ]);
  assert.equal(probeReply.id, probeId);
  assert.equal(modernReply.id, modernId);
  probe.child.stdin.end();
  modern.child.stdin.end();
  const [probeExit, modernExit] = await Promise.all([
    withTimeout(probe.completion, "probe observer close"),
    withTimeout(modern.completion, "modern observer close"),
  ]);
  assert.deepEqual(probeExit, { code: 0, signal: null, stderr: "" });
  assert.deepEqual(modernExit, { code: 0, signal: null, stderr: "" });

  const slots = readdirSync(captureRoot).sort();
  assert.equal(slots.length, 2);
  assert.ok(slots.every((slot) => ["session-1", "session-2", "session-3"].includes(slot)));
  const captures = slots.map((slot) => verifyCapture(join(captureRoot, slot), runId));
  assert.equal(new Set(captures.map(({ manifest }) => manifest.session_id)).size, 2);
  assert.deepEqual(
    captures.map(({ manifest }) => manifest.session_profile).sort(),
    ["modern-session", "negotiation-probe"],
  );
  for (const { events, text } of captures) {
    assert.equal(events.at(-1).protocol_session_status, "passed");
    assert.equal(events.at(-1).capability_scored, false);
    assert.equal(events.at(-1).host_capability, false);
    assert.equal(events.at(-1).source_binding_ready, false);
    assert.equal(events.filter(({ event }) => event === "anomaly").length, 0);
    for (const privateValue of [
      probeId,
      modernId,
      probeClient,
      modernClient,
      version,
      PRIVATE_SENTINEL,
    ]) {
      assert.equal(text.includes(privateValue), false, privateValue);
    }
    assert.equal(text.includes('"params"'), false);
    assert.equal(text.includes('"result"'), false);
  }
});

test("host SIGTERM after a complete probe or modern exchange closes safely", async (t) => {
  const captureRoot = privateRoot(t);
  const runId = randomUUID();
  const probe = startObserver(captureRoot, runId);
  const modern = startObserver(captureRoot, runId);
  await Promise.all([
    writeFrame(probe.child.stdin, requestFrame(
      "sigterm-probe-request",
      "server/discover",
      "sigterm-probe-client",
      "sigterm-version",
    )),
    writeFrame(modern.child.stdin, requestFrame(
      "sigterm-tools-request",
      "tools/list",
      "sigterm-tools-client",
      "sigterm-version",
    )),
  ]);
  await Promise.all([
    withTimeout(probe.nextMessage(), "SIGTERM probe reply"),
    withTimeout(modern.nextMessage(), "SIGTERM tools reply"),
  ]);
  const probeFixturePid = directFixturePid(probe.child.pid);
  const modernFixturePid = directFixturePid(modern.child.pid);
  const probeSignalStarted = process.hrtime.bigint();
  assert.equal(probe.child.kill("SIGTERM"), true);
  const modernSignalStarted = process.hrtime.bigint();
  modern.child.stdin.end();
  assert.equal(modern.child.kill("SIGTERM"), true);
  const completions = await Promise.all([
    withTimeout(probe.completion, "SIGTERM probe close").then((result) => ({
      elapsedMs: Number(process.hrtime.bigint() - probeSignalStarted) / 1_000_000,
      result,
    })),
    withTimeout(modern.completion, "SIGTERM tools close").then((result) => ({
      elapsedMs: Number(process.hrtime.bigint() - modernSignalStarted) / 1_000_000,
      result,
    })),
  ]);
  const exits = completions.map(({ result }) => result);
  assert.deepEqual(exits.map(({ code, signal }) => ({ code, signal })), [
    { code: 0, signal: null },
    { code: 0, signal: null },
  ]);
  for (const { elapsedMs } of completions) {
    assert.ok(elapsedMs <= 750, `observer close took ${elapsedMs.toFixed(1)} ms`);
  }
  t.diagnostic(
    `Claude-style close timings: ${completions.map(({ elapsedMs }) =>
      `${elapsedMs.toFixed(1)} ms`).join(", ")}`,
  );
  await Promise.all([
    assertProcessExited(probeFixturePid, "probe fixture"),
    assertProcessExited(modernFixturePid, "modern fixture"),
  ]);
  const captures = readdirSync(captureRoot)
    .sort()
    .map((slot) => verifyCapture(join(captureRoot, slot), runId));
  assert.deepEqual(
    captures.map(({ manifest }) => manifest.session_profile).sort(),
    ["modern-session", "negotiation-probe"],
  );
  const stimuli = captures.map(({ events }) => events.at(-1).closure_stimulus);
  assert.ok(stimuli.includes("sigterm"));
  assert.ok(stimuli.every((value) =>
    ["sigterm", "stdin-eof", "stdin-eof-and-sigterm"].includes(value)));
});

test("host SIGTERM before a complete request-response exchange fails closed", async (t) => {
  const captureRoot = privateRoot(t);
  const runId = randomUUID();
  const observer = startObserver(captureRoot, runId);
  await writeFrame(observer.child.stdin, {
    jsonrpc: "2.0",
    method: "notifications/cancelled",
    params: {
      _meta: modernMeta("incomplete-signal-client", "incomplete-signal-version"),
      requestId: "incomplete-private-request",
      reason: "incomplete-private-reason",
    },
  });
  await waitForCapturedEvent(
    captureRoot,
    ({ event }) => event === "notification",
    "incomplete notification capture",
  );
  assert.equal(observer.child.kill("SIGTERM"), true);
  const result = await withTimeout(observer.completion, "incomplete SIGTERM close");
  assert.equal(result.code, 2, result.stderr);
  const [slot] = readdirSync(captureRoot);
  const capture = verifyCapture(join(captureRoot, slot), runId);
  assert.equal(capture.manifest.session_profile, "invalid");
  assert.equal(capture.events.at(-1).closure_stimulus, "none");
  assert.ok(capture.events.some(
    ({ event, classification }) =>
      event === "anomaly" && classification === "observer-signal",
  ));
  for (const value of [
    "incomplete-signal-client",
    "incomplete-signal-version",
    "incomplete-private-request",
    "incomplete-private-reason",
  ]) {
    assert.equal(capture.text.includes(value), false);
  }
});

test("SIGKILL cannot produce a complete capture manifest", async (t) => {
  const captureRoot = privateRoot(t);
  const runId = randomUUID();
  const observer = startObserver(captureRoot, runId);
  await writeFrame(observer.child.stdin, requestFrame(
    "sigkill-private-request",
    "tools/list",
    "sigkill-private-client",
    "sigkill-private-version",
  ));
  await withTimeout(observer.nextMessage(), "SIGKILL tools reply");
  const fixturePid = directFixturePid(observer.child.pid);
  assert.equal(observer.child.kill("SIGKILL"), true);
  const result = await withTimeout(observer.completion, "SIGKILL observer close");
  assert.deepEqual({ code: result.code, signal: result.signal }, {
    code: null,
    signal: "SIGKILL",
  });
  const [slot] = readdirSync(captureRoot);
  const manifestPath = join(captureRoot, slot, "manifest.json");
  assert.equal(readFileSync(manifestPath).length, 0);
  assert.equal(
    readEvents(join(captureRoot, slot, "events.jsonl"))
      .some(({ event, phase }) => event === "lifecycle" && phase === "session-end"),
    false,
  );
  await assertProcessExited(fixturePid, "SIGKILL fixture");
});

test("unsafe roots and credentials fail before allocation", async (t) => {
  const unsafeModeRoot = privateRoot(t);
  chmodSync(unsafeModeRoot, 0o755);
  const unsafeMode = startObserver(unsafeModeRoot, randomUUID());
  unsafeMode.child.stdin.end();
  const unsafeModeExit = await withTimeout(unsafeMode.completion, "unsafe mode failure");
  assert.equal(unsafeModeExit.code, 2);
  assert.deepEqual(readdirSync(unsafeModeRoot), []);

  const unexpectedRoot = privateRoot(t);
  writeFileSync(join(unexpectedRoot, "unexpected"), "not a session slot", { mode: 0o600 });
  const unexpected = startObserver(unexpectedRoot, randomUUID());
  unexpected.child.stdin.end();
  const unexpectedExit = await withTimeout(unexpected.completion, "unexpected entry failure");
  assert.equal(unexpectedExit.code, 2);
  assert.deepEqual(readdirSync(unexpectedRoot), ["unexpected"]);

  const maliciousRoot = privateRoot(t);
  symlinkSync(realpathSync(tmpdir()), join(maliciousRoot, "session-1"));
  const malicious = startObserver(maliciousRoot, randomUUID());
  malicious.child.stdin.end();
  const maliciousExit = await withTimeout(malicious.completion, "malicious slot failure");
  assert.equal(maliciousExit.code, 2);
  assert.deepEqual(readdirSync(maliciousRoot), ["session-1"]);

  const credentialRoot = privateRoot(t);
  const credentialEnvironment = closedEnvironment();
  const credentialVariable = ["ANTHROPIC", "API", "KEY"].join("_");
  credentialEnvironment[credentialVariable] = "must-not-be-read";
  const credential = startObserver(credentialRoot, randomUUID(), {
    environment: credentialEnvironment,
  });
  credential.child.stdin.end();
  const credentialExit = await withTimeout(credential.completion, "credential refusal");
  assert.equal(credentialExit.code, 2);
  assert.deepEqual(readdirSync(credentialRoot), []);
  assert.equal(credentialExit.stderr.includes("must-not-be-read"), false);
});

test("three occupied private slots exhaust the bounded allocator", async (t) => {
  const captureRoot = privateRoot(t);
  for (const slot of ["session-1", "session-2", "session-3"]) {
    mkdirSync(join(captureRoot, slot), { mode: 0o700 });
    chmodSync(join(captureRoot, slot), 0o700);
  }
  const observer = startObserver(captureRoot, randomUUID());
  observer.child.stdin.end();
  const result = await withTimeout(observer.completion, "slot exhaustion");
  assert.equal(result.code, 2);
  assert.match(result.stderr, /three composite observation session slots are exhausted/);
  for (const slot of readdirSync(captureRoot)) {
    assert.deepEqual(readdirSync(join(captureRoot, slot)), []);
  }
});

async function assertInvalidSession(t, rawFrame, label) {
  const captureRoot = privateRoot(t);
  const runId = randomUUID();
  const observer = startObserver(captureRoot, runId);
  await writeRawFrame(observer.child.stdin, rawFrame);
  observer.child.stdin.end();
  const result = await withTimeout(observer.completion, `${label} observer close`);
  assert.equal(result.code, 2, result.stderr);
  const slots = readdirSync(captureRoot);
  assert.equal(slots.length, 1);
  const capture = verifyCapture(join(captureRoot, slots[0]), runId);
  assert.equal(capture.manifest.session_profile, "invalid");
  assert.equal(capture.manifest.protocol_session_status, "failed");
  assert.equal(capture.events.at(-1).anomaly_count >= 1, true);
  assert.equal(capture.text.includes("private-raw-identifier"), false);
  return capture;
}

test("duplicate-key JSON is never forwarded or retained", async (t) => {
  const meta = JSON.stringify(modernMeta("private-duplicate-client", "private-version"));
  const raw =
    `{"jsonrpc":"2.0","id":"private-raw-identifier",` +
    `"id":"private-second-identifier","method":"tools/list","params":{"_meta":${meta}}}`;
  const capture = await assertInvalidSession(t, raw, "duplicate JSON");
  assert.ok(capture.events.some(
    ({ event, classification }) => event === "anomaly" && classification === "invalid-json-rpc",
  ));
  assert.equal(capture.text.includes("private-second-identifier"), false);
  assert.equal(capture.text.includes("private-duplicate-client"), false);
});

test("legacy initialize traffic fails closed and remains private", async (t) => {
  const raw = JSON.stringify({
    jsonrpc: "2.0",
    id: "private-raw-identifier",
    method: "initialize",
    params: {
      protocolVersion: "2025-06-18",
      capabilities: {},
      clientInfo: { name: "private-legacy-client", version: "private-legacy-version" },
      _meta: modernMeta("private-meta-client", "private-meta-version"),
    },
  });
  const capture = await assertInvalidSession(t, raw, "legacy initialize");
  assert.ok(capture.events.some(
    ({ event, classification }) =>
      event === "anomaly" && classification === "legacy-initialize-traffic",
  ));
  for (const value of [
    "private-legacy-client",
    "private-legacy-version",
    "private-meta-client",
    "private-meta-version",
    "2025-06-18",
  ]) {
    assert.equal(capture.text.includes(value), false);
  }
});
