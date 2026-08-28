import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { createHash, randomUUID } from "node:crypto";
import {
  chmodSync,
  copyFileSync,
  existsSync,
  lstatSync,
  mkdtempSync,
  mkdirSync,
  readFileSync,
  realpathSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  buildObserverCommand,
  executeBoundedTunnelCommand,
  loadTunnelControlPlan,
  parseChatGptTunnelHarnessArguments,
  projectStoppedTunnelStatus,
  projectTunnelStatus,
  runPreparedTunnelConnect,
  runPreparedTunnelStatusAfter,
  runPreparedTunnelStop,
  validateTunnelControlPlan,
  validateSuccessfulPollHealth,
  validatePrivateRootLayout,
  verifyTunnelClient,
} from "../../scripts/qual_206_chatgpt_tunnel_exact_five_harness.mjs";
import {
  measurePnpmRuntimeClosure,
  verifyPnpmRuntime,
} from
  "../../scripts/qual_206_claude_capability_harness.mjs";

const TUNNEL_ID = "tunnel_6a873e7214308191bfe27240c1c03f68";
const TUNNEL_NAME = "gis-ai-go-v0-2-interoperability";
const ALIAS = "gis-ai-go-v0-2-exact-five-v1";
const HEALTH_URL_FILE =
  "/private/tmp/operator/tunnel-state/health/gis-ai-go-v0-2-exact-five-v1.url";
const HEALTH_BASE_URL = "http://127.0.0.1:61234";
const macRuntimeTest = process.platform === "darwin" ? test : test.skip;

function hash(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

const MCP_COMMAND = "/usr/bin/env -i PATH=/usr/bin:/bin node observer.mjs";
const MCP_COMMAND_SHA256 = hash(Buffer.from(MCP_COMMAND, "utf8"));
const RUNTIME = Object.freeze({
  generated_first_party_closure: Object.freeze({
    bytes: 123,
    file_count: 4,
    manifest_sha256: "c".repeat(64),
    reference_manifest_sha256: "c".repeat(64),
    reference_matches_current: true,
  }),
  installed_dependency_closure: Object.freeze({
    bytes: 456,
    entry_count: 7,
    manifest_sha256: "d".repeat(64),
  }),
});

test("the runbook selects the reviewed Node runtime for every command", () => {
  const runbook = readFileSync(
    new URL("../../docs/operations/QUAL-206_CHATGPT_TUNNEL_EXACT_FIVE.md", import.meta.url),
    "utf8",
  );
  assert.doesNotMatch(runbook, /^node\b/mu);
  assert.equal((runbook.match(/--node "\$QUAL206_NODE"/gu) ?? []).length, 2);
  assert.ok((runbook.match(/^"\$QUAL206_NODE"\s/gmu) ?? []).length >= 6);
});

function validRawStatus(healthUrlFile = HEALTH_URL_FILE, baseUrl = HEALTH_BASE_URL) {
  return {
    alias: ALIAS,
    tunnel_id: TUNNEL_ID,
    profile_name: ALIAS,
    remote: { id: TUNNEL_ID, name: TUNNEL_NAME },
    stale: false,
    error: "",
    remote_error: "",
    runtime_state: "ready",
    healthy: true,
    ready: true,
    control_plane_poll_health: {
      state: "unknown",
      reason: "no live admin UI system snapshot",
    },
    remote_lookup_attempted: true,
    process_running: true,
    health_url_file: healthUrlFile,
    process: {
      alias: ALIAS,
      tunnel_id: TUNNEL_ID,
      profile_name: ALIAS,
      mode: "process",
      pid: 12345,
      target_kind: "command",
      target_value: MCP_COMMAND,
    },
    local: {
      effective_health: {
        base_url: baseUrl,
        healthz: { ok: true, status: 200, url: "private-and-not-projected" },
        readyz: { ok: true, status: 200, url: "private-and-not-projected" },
      },
      live_admin_ui: { base_url: "private-and-not-projected" },
    },
    command: "private-and-not-projected",
    pid: 12345,
  };
}

function validPollHealth(
  healthUrlFile = HEALTH_URL_FILE,
  baseUrl = HEALTH_BASE_URL,
  pid = 12345,
) {
  return {
    locator: {
      kind: "url_file",
      url_file: healthUrlFile,
      resolved_base_url: baseUrl,
    },
    process: { pid, running: true },
    base_url: baseUrl,
    ui_url: `${baseUrl}/ui`,
    healthz: {
      url: `${baseUrl}/healthz`,
      ok: true,
      status: 200,
      body: "live",
    },
    readyz: {
      url: `${baseUrl}/readyz`,
      ok: true,
      status: 200,
      body: "ready",
    },
    control_plane_poll: {
      url: `${baseUrl}/metrics`,
      value: Math.floor(Date.now() / 1_000),
      ok: true,
    },
    result: "ok",
  };
}

function pendingPollHealth(
  healthUrlFile = HEALTH_URL_FILE,
  baseUrl = HEALTH_BASE_URL,
  pid = 12345,
) {
  const value = validPollHealth(healthUrlFile, baseUrl, pid);
  value.control_plane_poll = {
    url: `${baseUrl}/metrics`,
    ok: false,
    error: "no successful control-plane poll observed",
  };
  value.result = "fail";
  return value;
}

function validStoppedRawStatus() {
  const value = validRawStatus();
  Object.assign(value, {
    remote: null,
    runtime_state: "stopped",
    healthy: false,
    ready: false,
    remote_lookup_attempted: false,
    process_running: false,
    stopped: true,
    stop_error: "",
    control_plane_poll_health: {
      state: "unknown",
      reason: "no live admin UI system snapshot",
    },
  });
  delete value.pid;
  value.process.mode = "stopped";
  delete value.process.pid;
  value.local.effective_health.healthz = { ok: false, status: 0 };
  value.local.effective_health.readyz = { ok: false, status: 0 };
  value.local.live_admin_ui = { found: false };
  return value;
}

function operationalHarness(t) {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-tunnel-phase-test-"));
  const captureRoot = join(parent, "capture");
  const operatorRoot = join(parent, "operator");
  mkdirSync(captureRoot, { mode: 0o700 });
  mkdirSync(operatorRoot, { mode: 0o700 });
  mkdirSync(join(operatorRoot, "raw"), { mode: 0o700 });
  t.after(() => rmSync(parent, { force: true, recursive: true }));
  const client = Object.freeze({
    path: join(operatorRoot, "tunnel-client-v0.0.13"),
    bytes: 20_336_818,
    sha256: "b".repeat(64),
    dev: 101,
    ino: 202,
    nlink: 1,
    uid: process.getuid(),
    mode: 0o100500,
    reportedVersion: "0.0.13+test",
  });
  const plan = Object.freeze({
    source_commit: "a".repeat(40),
    capture_root: captureRoot,
    operator_root: operatorRoot,
    client_path: client.path,
    client_bytes: client.bytes,
    client_sha256: client.sha256,
    client_dev: client.dev,
    client_ino: client.ino,
    client_nlink: client.nlink,
    client_uid: client.uid,
    client_mode: client.mode,
    client_reported_version: client.reportedVersion,
    runtime_key_environment: "CONTROL_PLANE_API_KEY",
    mcp_command: MCP_COMMAND,
    mcp_command_sha256: MCP_COMMAND_SHA256,
  });
  const calls = [];
  const waits = [];
  let verificationCount = 0;
  const responses = [];
  const healthUrlFile = join(
    operatorRoot,
    "tunnel-state",
    "health",
    `${ALIAS}.url`,
  );
  const dependencies = {
    environment: { CONTROL_PLANE_API_KEY: "bound" + "ed-test-key" },
    verifyProtectedMainCheckout: () => ({ commit: plan.source_commit }),
    verifyTunnelClient: () => {
      verificationCount += 1;
      return client;
    },
    waitForPollRetry: (milliseconds) => waits.push(milliseconds),
    spawnSync: (_path, argumentsValue, options) => {
      calls.push({ argumentsValue, environment: options.env });
      const response = responses.shift();
      if (response === undefined) throw new Error("fake tunnel response queue ended");
      return {
        status: response.status ?? 0,
        signal: null,
        stdout: `${JSON.stringify(response.payload ?? {})}\n`,
        stderr: response.stderr ?? "",
      };
    },
  };
  return {
    calls,
    client,
    dependencies,
    healthUrlFile,
    plan,
    responses,
    waits,
    verificationCount: () => verificationCount,
  };
}

test("the observer command is credential-free and binds the reviewed parent", () => {
  const command = buildObserverCommand({
    observerTmpDir: "/private/tmp/operator/observer",
    captureRoot: "/private/tmp/capture",
    runId: randomUUID(),
    sourceCommit: "a".repeat(40),
    parentSha256: "b".repeat(64),
    parentBytes: 20_336_818,
    runtime: RUNTIME,
  });

  assert.match(command, /^\/usr\/bin\/env -i /u);
  assert.match(command, /GIS_AI_GO_QUAL_206_CHATGPT_TUNNEL_EXACT_FIVE=1/u);
  assert.match(command, /GIS_AI_GO_QUAL_206_EVENT_CAPTURE=1/u);
  assert.match(command, /--expected-parent-sha256 b{64}/u);
  assert.match(command, /--expected-parent-bytes 20336818/u);
  assert.match(command, /--expected-generated-runtime-bytes 123/u);
  assert.match(command, /--expected-generated-runtime-file-count 4/u);
  assert.match(command, new RegExp(`--expected-generated-runtime-manifest-sha256 c{64}`, "u"));
  assert.match(
    command,
    new RegExp(`--expected-generated-runtime-reference-manifest-sha256 c{64}`, "u"),
  );
  assert.match(command, /--expected-generated-runtime-reference-matches-current true/u);
  assert.match(command, /--expected-installed-dependency-bytes 456/u);
  assert.match(command, /--expected-installed-dependency-entry-count 7/u);
  assert.match(
    command,
    new RegExp(`--expected-installed-dependency-manifest-sha256 d{64}`, "u"),
  );
  assert.doesNotMatch(command, /OPENAI_API_KEY|CONTROL_PLANE_API_KEY|ANTHROPIC_API_KEY/u);
  assert.doesNotMatch(command, /--mcp-server-url|https?:\/\//u);
});

test("the reviewed client check binds bytes and the reported build", (t) => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-tunnel-client-test-"));
  t.after(() => rmSync(root, { force: true, recursive: true }));
  const client = join(root, "client");
  copyFileSync(process.execPath, client);
  chmodSync(client, 0o700);
  const bytes = readFileSync(client);
  const expected = {
    bytes: bytes.length,
    sha256: hash(bytes),
    reportedVersion: "0.0.13+test-build",
  };

  const verified = verifyTunnelClient(client, expected, () => expected.reportedVersion);
  assert.equal(verified.bytes, bytes.length);
  assert.equal(verified.sha256, expected.sha256);

  writeFileSync(client, Buffer.concat([bytes, Buffer.from("mutation", "utf8")]));
  assert.throws(
    () => verifyTunnelClient(client, expected, () => expected.reportedVersion),
    /bytes do not match/u,
  );
});

test("the pnpm verifier binds wrapper, bundled distribution and reported version", (t) => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-pnpm-identity-test-"));
  t.after(() => rmSync(root, { force: true, recursive: true }));
  const bin = join(root, "bin");
  const dist = join(root, "dist");
  const lib = join(root, "lib");
  mkdirSync(bin, { mode: 0o700 });
  mkdirSync(dist, { mode: 0o700 });
  mkdirSync(lib, { mode: 0o700 });
  const wrapper = join(bin, "pnpm.cjs");
  const distribution = join(dist, "pnpm.cjs");
  const support = join(lib, "support.cjs");
  const wrapperBytes = Buffer.from("reviewed wrapper\n", "utf8");
  const distributionBytes = Buffer.from("reviewed distribution\n", "utf8");
  const supportBytes = Buffer.from("reviewed support\n", "utf8");
  writeFileSync(wrapper, wrapperBytes, { mode: 0o700 });
  writeFileSync(distribution, distributionBytes, { mode: 0o600 });
  writeFileSync(support, supportBytes, { mode: 0o600 });
  const expected = {
    version: "10.33.2",
    wrapper: { bytes: wrapperBytes.length, sha256: hash(wrapperBytes) },
    distribution: {
      bytes: distributionBytes.length,
      sha256: hash(distributionBytes),
    },
    package_closure: measurePnpmRuntimeClosure(root),
  };
  let versionCalls = 0;
  assert.equal(
    verifyPnpmRuntime(wrapper, process.execPath, expected, () => {
      versionCalls += 1;
      return "10.33.2";
    }).version,
    "10.33.2",
  );
  assert.equal(versionCalls, 1);
  assert.throws(
    () => verifyPnpmRuntime(wrapper, process.execPath, expected, () => "10.33.1"),
    /identity or reported version/u,
  );
  const reviewedFiles = [
    [wrapper, wrapperBytes],
    [distribution, distributionBytes],
    [support, supportBytes],
  ];
  for (const [path, original] of reviewedFiles) {
    writeFileSync(path, Buffer.concat([original, Buffer.from("precheck mutation")]));
    let unreviewedVersionCalls = 0;
    assert.throws(
      () => verifyPnpmRuntime(wrapper, process.execPath, expected, () => {
        unreviewedVersionCalls += 1;
        return "10.33.2";
      }),
      /identity or reported version/u,
    );
    assert.equal(unreviewedVersionCalls, 0);
    writeFileSync(path, original);
  }

  for (const [path, original] of reviewedFiles) {
    let reviewedVersionCalls = 0;
    assert.throws(
      () => verifyPnpmRuntime(wrapper, process.execPath, expected, () => {
        reviewedVersionCalls += 1;
        writeFileSync(path, Buffer.concat([original, Buffer.from("postcheck mutation")]));
        return "10.33.2";
      }),
      /identity or reported version/u,
    );
    assert.equal(reviewedVersionCalls, 1);
    writeFileSync(path, original);
  }
});

macRuntimeTest("the installed pnpm runtime matches the reviewed 10.33.2 build", () => {
  const command = execFileSync("/usr/bin/which", ["pnpm"], {
    encoding: "utf8",
  }).trim();
  assert.equal(verifyPnpmRuntime(realpathSync(command)).version, "10.33.2");
});

macRuntimeTest("the reference build ignores an ambient pnpmfile hook", (t) => {
  if (process.versions.node !== "26.7.0") {
    t.skip("the exact local evidence runtime requires Node 26.7.0");
    return;
  }
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-pnpm-hook-test-"));
  t.after(() => rmSync(root, { force: true, recursive: true }));
  const marker = join(root, "ambient-hook-ran");
  const hook = join(root, "ambient-pnpmfile.cjs");
  writeFileSync(hook, [
    'const { writeFileSync } = require("node:fs");',
    `writeFileSync(${JSON.stringify(marker)}, "unexpected hook execution\\n");`,
    "module.exports = { hooks: { readPackage: (value) => value } };",
    "",
  ].join("\n"), { mode: 0o600 });
  const command = realpathSync(execFileSync("/usr/bin/which", ["pnpm"], {
    encoding: "utf8",
  }).trim());
  const sourceCommit = execFileSync("/usr/bin/git", ["rev-parse", "HEAD"], {
    cwd: realpathSync(new URL("../../", import.meta.url).pathname),
    encoding: "utf8",
  }).trim();
  const source = [
    'import { buildAndBindGeneratedRuntime } from',
    '  "./scripts/qual_206_claude_capability_harness.mjs";',
    "buildAndBindGeneratedRuntime(process.argv[1], process.argv[2]);",
  ].join("\n");
  execFileSync(process.execPath, [
    "--input-type=module",
    "--eval",
    source,
    sourceCommit,
    command,
  ], {
    cwd: realpathSync(new URL("../../", import.meta.url).pathname),
    env: {
      ...process.env,
      NPM_CONFIG_GLOBAL_PNPMFILE: hook,
      npm_config_global_pnpmfile: hook,
    },
    stdio: ["ignore", "ignore", "pipe"],
    timeout: 60_000,
  });
  assert.equal(existsSync(marker), false);
});

test("status projection retains only healthy allowlisted facts", () => {
  const projection = projectTunnelStatus(
    validRawStatus(),
    validPollHealth(),
    "before",
    MCP_COMMAND_SHA256,
    HEALTH_URL_FILE,
    "2026-08-27T12:00:00.000Z",
  );

  assert.deepEqual(projection, {
    schema: "gis-ai-go.qual-206-chatgpt-tunnel-status.v1",
    phase: "before",
    observed_at: "2026-08-27T12:00:00.000Z",
    alias: ALIAS,
    tunnel_id: TUNNEL_ID,
    profile_name: ALIAS,
    target_kind: "command",
    mcp_command_sha256: MCP_COMMAND_SHA256,
    remote: { found: true, id: TUNNEL_ID, name: TUNNEL_NAME },
    stale: false,
    error: null,
    remote_error: null,
    runtime_state: "ready",
    healthy: true,
    ready: true,
    control_plane_poll_health: {
      state: "healthy",
      route_kind: "control_plane",
    },
    remote_lookup_attempted: true,
    process_running: true,
    local: {
      healthz_status: 200,
      readyz_status: 200,
      direct_healthy_poll_route: true,
    },
  });
  assert.doesNotMatch(
    JSON.stringify(projection),
    /endpoint|"pid":|"command":|base_url|history/u,
  );
});

for (const [name, mutate] of [
  ["remote identity drift", (value) => { value.remote.id = `tunnel_${"0".repeat(32)}`; }],
  ["wrong remote name", (value) => { value.remote.name = "different"; }],
  ["stale alias", (value) => { value.stale = true; }],
  ["unready runtime", (value) => { value.ready = false; }],
  ["missing remote lookup", (value) => { value.remote_lookup_attempted = false; }],
  ["stopped process", (value) => { value.process_running = false; }],
  ["wrong process mode", (value) => { value.process.mode = "tmux"; }],
  ["missing process PID", (value) => { delete value.process.pid; }],
  ["failed local health", (value) => { value.local.effective_health.healthz.status = 503; }],
  ["unexpected poll snapshot", (value) => {
    value.control_plane_poll_health.reason = "different";
  }],
  ["contradictory poll route", (value) => {
    value.control_plane_poll_health.route = { kind: "mcp" };
  }],
  ["remote error", (value) => { value.remote_error = "lookup failed"; }],
]) {
  test(`status projection rejects ${name}`, () => {
    const value = validRawStatus();
    mutate(value);
    assert.throws(() => projectTunnelStatus(
      value,
      validPollHealth(),
      "after",
      MCP_COMMAND_SHA256,
      HEALTH_URL_FILE,
    ));
  });
}

test("status projection rejects MCP command drift", () => {
  const value = validRawStatus();
  value.process.target_value = `${MCP_COMMAND} --mutated`;
  assert.throws(
    () => projectTunnelStatus(
      value,
      validPollHealth(),
      "after",
      MCP_COMMAND_SHA256,
      HEALTH_URL_FILE,
    ),
    /bind the reviewed profile and MCP command/u,
  );
});

for (const [name, mutate] of [
  ["zero poll timestamp", (value) => { value.control_plane_poll.value = 0; }],
  ["missing poll timestamp", (value) => { delete value.control_plane_poll.value; }],
  ["failed poll", (value) => { value.control_plane_poll.ok = false; }],
  ["poll error", (value) => { value.control_plane_poll.error = "synthetic"; }],
  ["stale poll timestamp", (value) => {
    value.control_plane_poll.value = Math.floor(Date.now() / 1_000) - 121;
  }],
  ["future poll timestamp", (value) => {
    value.control_plane_poll.value = Math.floor(Date.now() / 1_000) + 6;
  }],
  ["fractional poll timestamp", (value) => {
    value.control_plane_poll.value = (Date.now() / 1_000) - 1;
  }],
  ["wrong process PID", (value) => { value.process.pid = 54321; }],
  ["stopped process probe", (value) => { value.process.running = false; }],
  ["wrong locator", (value) => { value.locator.url_file = "/private/tmp/other"; }],
  ["non-loopback locator", (value) => {
    value.locator.resolved_base_url = "https://example.invalid";
  }],
  ["failed health endpoint", (value) => { value.healthz.status = 503; }],
  ["failed result", (value) => { value.result = "fail"; }],
]) {
  test(`poll health proof rejects ${name}`, () => {
    const value = validPollHealth();
    mutate(value);
    assert.throws(() => validateSuccessfulPollHealth(value, HEALTH_URL_FILE, 12345));
  });
}

test("stopped projection proves local teardown without claiming a remote lookup", () => {
  const value = validStoppedRawStatus();
  const projection = projectStoppedTunnelStatus(
    value,
    MCP_COMMAND_SHA256,
    "2026-08-27T12:30:00.000Z",
  );
  assert.deepEqual(projection, {
    schema: "gis-ai-go.qual-206-chatgpt-tunnel-status.v1",
    phase: "stopped",
    observed_at: "2026-08-27T12:30:00.000Z",
    alias: ALIAS,
    tunnel_id: TUNNEL_ID,
    profile_name: ALIAS,
    target_kind: "command",
    mcp_command_sha256: MCP_COMMAND_SHA256,
    remote: { found: false, id: TUNNEL_ID, name: TUNNEL_NAME },
    stale: false,
    error: null,
    remote_error: null,
    runtime_state: "stopped",
    healthy: false,
    ready: false,
    control_plane_poll_health: null,
    remote_lookup_attempted: false,
    process_running: false,
    local: {
      healthz_status: null,
      readyz_status: null,
      direct_healthy_poll_route: false,
    },
  });
});

test("stopped projection rejects a process that is still running", () => {
  const value = validStoppedRawStatus();
  value.process_running = true;
  assert.throws(
    () => projectStoppedTunnelStatus(value, MCP_COMMAND_SHA256),
    /does not establish a stopped local runtime/u,
  );
});

test("stopped projection rejects contradictory nested live state", () => {
  const value = validStoppedRawStatus();
  value.local.effective_health.healthz = { ok: true, status: 200 };
  assert.throws(
    () => projectStoppedTunnelStatus(value, MCP_COMMAND_SHA256),
    /does not establish a stopped local runtime/u,
  );
});

test("the harness accepts only explicit pnpm and closed runtime-key references", (t) => {
  const authority = "--chatgpt-tunnel-exact-five-harness-only";
  const fakePath = mkdtempSync(join(tmpdir(), "gis-ai-go-fake-pnpm-path-"));
  t.after(() => rmSync(fakePath, { force: true, recursive: true }));
  writeFileSync(join(fakePath, "pnpm"), "unreviewed PATH command\n", { mode: 0o700 });
  const environment = {
    GIS_AI_GO_QUAL_206_CHATGPT_TUNNEL_EXACT_FIVE_HARNESS: "1",
    PATH: `${fakePath}:/usr/bin:/bin`,
  };
  const argumentsValue = [
    authority,
    "--phase", "prepare",
    "--capture-root", "/private/tmp/capture",
    "--operator-root", "/private/tmp/operator",
    "--run-id", randomUUID(),
    "--source-commit", "a".repeat(40),
    "--client", "/private/tmp/client",
    "--pnpm", realpathSync(process.execPath),
    "--runtime-key-env", "CONTROL_PLANE_API_KEY",
  ];
  const parsed = parseChatGptTunnelHarnessArguments(argumentsValue, environment);
  assert.equal(parsed.runtimeKeyEnv, "CONTROL_PLANE_API_KEY");
  assert.equal(parsed.pnpm, realpathSync(process.execPath));
  const mutated = [...argumentsValue];
  mutated[mutated.indexOf("--runtime-key-env") + 1] = "AWS_SECRET_ACCESS_KEY";
  assert.throws(
    () => parseChatGptTunnelHarnessArguments(mutated, environment),
    /outside the closed allowlist/u,
  );
  const relativePnpm = [...argumentsValue];
  relativePnpm[relativePnpm.indexOf("--pnpm") + 1] = "pnpm";
  assert.throws(
    () => parseChatGptTunnelHarnessArguments(relativePnpm, environment),
    /canonical absolute path/u,
  );
  const missingPnpm = [...argumentsValue];
  missingPnpm.splice(missingPnpm.indexOf("--pnpm"), 2);
  assert.throws(
    () => parseChatGptTunnelHarnessArguments(missingPnpm, environment),
    /missing a required option/u,
  );
  const absentPnpm = [...argumentsValue];
  absentPnpm[absentPnpm.indexOf("--pnpm") + 1] = join(fakePath, "absent-pnpm");
  assert.throws(
    () => parseChatGptTunnelHarnessArguments(absentPnpm, environment),
    /canonical absolute path/u,
  );
  const alias = join(fakePath, "pnpm-alias");
  symlinkSync(realpathSync(process.execPath), alias);
  const aliasedPnpm = [...argumentsValue];
  aliasedPnpm[aliasedPnpm.indexOf("--pnpm") + 1] = alias;
  assert.throws(
    () => parseChatGptTunnelHarnessArguments(aliasedPnpm, environment),
    /canonical absolute path/u,
  );
  assert.equal(parsed.pnpm, realpathSync(process.execPath));
  assert.notEqual(parsed.pnpm, join(fakePath, "pnpm"));
  assert.throws(
    () => parseChatGptTunnelHarnessArguments([
      authority,
      "--phase", "connect",
      "--operator-root", "/private/tmp/operator",
      "--pnpm", realpathSync(process.execPath),
    ], environment),
    /unsupported option/u,
  );
});

test("private roots must be new siblings beneath one owner-only parent", (t) => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-private-root-layout-"));
  const other = mkdtempSync(join(tmpdir(), "gis-ai-go-private-root-other-"));
  t.after(() => rmSync(parent, { force: true, recursive: true }));
  t.after(() => rmSync(other, { force: true, recursive: true }));
  chmodSync(parent, 0o700);
  chmodSync(other, 0o700);

  assert.doesNotThrow(() => validatePrivateRootLayout(
    join(parent, "capture"),
    join(parent, "operator"),
  ));
  assert.throws(
    () => validatePrivateRootLayout(join(parent, "capture"), join(other, "operator")),
    /share one owner-only parent/u,
  );

  const existing = join(parent, "existing");
  mkdirSync(existing, { mode: 0o700 });
  assert.throws(
    () => validatePrivateRootLayout(existing, join(existing, "operator")),
    /must not contain one another/u,
  );
  assert.throws(
    () => validatePrivateRootLayout(
      join(process.cwd(), "capture"),
      join(process.cwd(), "operator"),
    ),
    /outside the Git checkout/u,
  );
});

test("a prepared control plan reloads the repository's real Git tree identity", (t) => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-control-plan-test-"));
  const captureRoot = join(parent, "capture");
  const operatorRoot = join(parent, "operator");
  mkdirSync(captureRoot, { mode: 0o700 });
  mkdirSync(operatorRoot, { mode: 0o700 });
  t.after(() => rmSync(parent, { force: true, recursive: true }));
  const identity = (path) => {
    const info = lstatSync(path);
    return { dev: info.dev, ino: info.ino, uid: info.uid, mode: info.mode };
  };
  const plan = {
    schema: "gis-ai-go.qual-206-chatgpt-tunnel-control-plan.v1",
    run_id: randomUUID(),
    source_commit: "a".repeat(40),
    source_tree: "b".repeat(40),
    repository_origin: "https://github.com/chris-page-gov/gis-ai-go.git",
    clean_detached_checkout: true,
    capture_root: captureRoot,
    operator_root: operatorRoot,
    capture_root_identity: identity(captureRoot),
    operator_root_identity: identity(operatorRoot),
    client_path: join(operatorRoot, "tunnel-client-v0.0.13"),
    client_version: "0.0.13",
    client_build_sha: "c".repeat(40),
    client_reported_version: "0.0.13+test",
    client_bytes: 20_336_818,
    client_sha256: "d".repeat(64),
    client_dev: 101,
    client_ino: 202,
    client_nlink: 1,
    client_uid: process.getuid(),
    client_mode: 0o100500,
    tunnel_id: TUNNEL_ID,
    tunnel_name: TUNNEL_NAME,
    alias: ALIAS,
    profile_name: ALIAS,
    runtime_key_environment: "OPENAI_API_KEY",
    runtime: RUNTIME,
    mcp_command: MCP_COMMAND,
    mcp_command_sha256: MCP_COMMAND_SHA256,
  };

  assert.equal(validateTunnelControlPlan(plan, operatorRoot), plan);
  writeFileSync(
    join(operatorRoot, "qual-206-chatgpt-tunnel-control-plan.v1.json"),
    `${JSON.stringify(plan)}\n`,
    { flag: "wx", mode: 0o600 },
  );
  assert.deepEqual(loadTunnelControlPlan(operatorRoot), plan);
  assert.throws(
    () => validateTunnelControlPlan(
      { ...plan, source_tree: "e".repeat(64) },
      operatorRoot,
    ),
    /private tunnel control plan is invalid/u,
  );
});

test("connect and ready status receive only the allowlisted runtime key", (t) => {
  const harness = operationalHarness(t);
  harness.responses.push(
    { payload: {} },
    { payload: validRawStatus(harness.healthUrlFile) },
    { payload: validPollHealth(harness.healthUrlFile) },
  );
  const status = runPreparedTunnelConnect(harness.plan, harness.dependencies);
  assert.equal(status.phase, "before");
  assert.equal(harness.calls.length, 3);
  for (const call of harness.calls.slice(0, 2)) {
    assert.equal(call.environment.CONTROL_PLANE_API_KEY, "bounded-test-key");
    assert.equal(Object.hasOwn(call.environment, "OPENAI_API_KEY"), false);
  }
  assert.equal(
    Object.hasOwn(harness.calls[2].environment, "CONTROL_PLANE_API_KEY"),
    false,
  );
  assert.deepEqual(harness.calls[2].argumentsValue, [
    "health",
    "--url-file",
    harness.healthUrlFile,
    "--pid",
    "12345",
    "--require-control-plane-poll",
    "--json",
  ]);
  assert.equal(harness.verificationCount(), 7);
  assert.equal(
    existsSync(join(harness.plan.capture_root, "tunnel-status-before.json")),
    true,
  );
});

test("connect retries only the bounded not-yet-polled health result", (t) => {
  const harness = operationalHarness(t);
  harness.responses.push(
    { payload: {} },
    { payload: validRawStatus(harness.healthUrlFile) },
    { status: 2, payload: pendingPollHealth(harness.healthUrlFile) },
    { payload: validPollHealth(harness.healthUrlFile) },
  );
  const status = runPreparedTunnelConnect(harness.plan, harness.dependencies);
  assert.equal(status.control_plane_poll_health.state, "healthy");
  assert.deepEqual(harness.waits, [5_000]);
  assert.equal(harness.calls.length, 4);
  assert.equal(
    existsSync(join(
      harness.plan.operator_root,
      "raw",
      "tunnel-poll-health-before-attempt-1-raw.json",
    )),
    true,
  );
  assert.equal(
    existsSync(join(
      harness.plan.operator_root,
      "raw",
      "tunnel-poll-health-before-attempt-2-raw.json",
    )),
    true,
  );
});

test("connect stops after eight not-yet-polled health results", (t) => {
  const harness = operationalHarness(t);
  harness.responses.push(
    { payload: {} },
    { payload: validRawStatus(harness.healthUrlFile) },
    ...Array.from({ length: 8 }, () => ({
      status: 2,
      payload: pendingPollHealth(harness.healthUrlFile),
    })),
    { payload: validStoppedRawStatus() },
  );
  assert.throws(
    () => runPreparedTunnelConnect(harness.plan, harness.dependencies),
    /bounded readiness window/u,
  );
  assert.deepEqual(harness.waits, Array(7).fill(5_000));
  assert.equal(harness.calls.length, 11);
  assert.equal(
    existsSync(join(harness.plan.capture_root, "tunnel-status-stopped.json")),
    true,
  );
});

test("connect accepts a first successful poll on the eighth attempt", (t) => {
  const harness = operationalHarness(t);
  harness.responses.push(
    { payload: {} },
    { payload: validRawStatus(harness.healthUrlFile) },
    ...Array.from({ length: 7 }, () => ({
      status: 2,
      payload: pendingPollHealth(harness.healthUrlFile),
    })),
    { payload: validPollHealth(harness.healthUrlFile) },
  );
  const status = runPreparedTunnelConnect(harness.plan, harness.dependencies);
  assert.equal(status.control_plane_poll_health.state, "healthy");
  assert.deepEqual(harness.waits, Array(7).fill(5_000));
  assert.equal(harness.calls.length, 10);
});

test("connect does not probe poll health after a status error", (t) => {
  const harness = operationalHarness(t);
  const errored = validRawStatus(harness.healthUrlFile);
  errored.remote_error = "synthetic remote lookup error";
  harness.responses.push(
    { payload: {} },
    { payload: errored },
    { payload: validStoppedRawStatus() },
  );
  assert.throws(
    () => runPreparedTunnelConnect(harness.plan, harness.dependencies),
    /healthy ready identity/u,
  );
  assert.deepEqual(harness.waits, []);
  assert.equal(harness.calls.length, 3);
  assert.deepEqual(harness.calls[2].argumentsValue, [
    "runtimes",
    "stop",
    ALIAS,
    "--json",
  ]);
});

for (const [name, mutate] of [
  ["missing metric", (value) => {
    value.control_plane_poll.error =
      "missing commands_poll_last_successful_timestamp_seconds metric";
  }],
  ["explicit zero metric", (value) => { value.control_plane_poll.value = 0; }],
  ["endpoint failure", (value) => {
    value.readyz.ok = false;
    value.readyz.status = 503;
  }],
  ["locator drift", (value) => { value.locator.url_file = "/private/tmp/drift"; }],
]) {
  test(`connect does not retry ${name}`, (t) => {
    const harness = operationalHarness(t);
    const failed = pendingPollHealth(harness.healthUrlFile);
    mutate(failed);
    harness.responses.push(
      { payload: {} },
      { payload: validRawStatus(harness.healthUrlFile) },
      { status: 2, payload: failed },
      { payload: validStoppedRawStatus() },
    );
    assert.throws(
      () => runPreparedTunnelConnect(harness.plan, harness.dependencies),
      /control-plane poll health/u,
    );
    assert.deepEqual(harness.waits, []);
    assert.equal(harness.calls.length, 4);
  });
}

test("normal stop receives no credential and writes stopped evidence", (t) => {
  const harness = operationalHarness(t);
  harness.responses.push({ payload: validStoppedRawStatus() });
  const status = runPreparedTunnelStop(harness.plan, harness.dependencies);
  assert.equal(status.phase, "stopped");
  assert.equal(harness.calls.length, 1);
  assert.equal(Object.hasOwn(harness.calls[0].environment, "CONTROL_PLANE_API_KEY"), false);
  assert.equal(harness.verificationCount(), 3);
  assert.equal(
    existsSync(join(harness.plan.capture_root, "tunnel-status-stopped.json")),
    true,
  );
});

test("failed connect invokes one credential-free automatic stop", (t) => {
  const harness = operationalHarness(t);
  harness.responses.push(
    { status: 2, payload: { error: "synthetic failure" } },
    { payload: validStoppedRawStatus() },
  );
  assert.throws(
    () => runPreparedTunnelConnect(harness.plan, harness.dependencies),
    /tunnel-connect-raw failed closed/u,
  );
  assert.equal(harness.calls.length, 2);
  assert.equal(harness.calls[0].environment.CONTROL_PLANE_API_KEY, "bounded-test-key");
  assert.equal(Object.hasOwn(harness.calls[1].environment, "CONTROL_PLANE_API_KEY"), false);
  assert.equal(harness.verificationCount(), 5);
  assert.equal(
    JSON.parse(readFileSync(
      join(harness.plan.capture_root, "tunnel-status-stopped.json"),
      "utf8",
    )).phase,
    "stopped",
  );
  assert.equal(
    existsSync(join(
      harness.plan.operator_root,
      "raw",
      "automatic-stop-connect-failure.json",
    )),
    true,
  );
});

test("automatic stop projection failure preserves both errors", (t) => {
  const harness = operationalHarness(t);
  const contradictory = validStoppedRawStatus();
  contradictory.stopped = false;
  harness.responses.push(
    { status: 2, payload: { error: "synthetic connect failure" } },
    { payload: contradictory },
  );
  let caught;
  try {
    runPreparedTunnelConnect(harness.plan, harness.dependencies);
  } catch (error) {
    caught = error;
  }
  assert.equal(caught instanceof AggregateError, true);
  assert.match(caught.message, /automatic tunnel teardown failed/u);
  assert.match(caught.errors[0].message, /tunnel-connect-raw failed closed/u);
  assert.match(caught.errors[1].message, /does not establish a stopped local runtime/u);
  assert.equal(
    existsSync(join(harness.plan.capture_root, "tunnel-status-stopped.json")),
    false,
  );
  assert.equal(
    existsSync(join(
      harness.plan.operator_root,
      "raw",
      "automatic-stop-connect-failure.json",
    )),
    true,
  );
});

test("automatic non-zero stop preserves both errors and no stopped evidence", (t) => {
  const harness = operationalHarness(t);
  harness.responses.push(
    { status: 2, payload: { error: "synthetic connect failure" } },
    { status: 2, payload: { error: "synthetic stop failure" } },
  );
  let caught;
  try {
    runPreparedTunnelConnect(harness.plan, harness.dependencies);
  } catch (error) {
    caught = error;
  }
  assert.equal(caught instanceof AggregateError, true);
  assert.match(caught.errors[0].message, /tunnel-connect-raw failed closed/u);
  assert.match(caught.errors[1].message, /automatic-stop-connect-failure failed closed/u);
  assert.equal(
    existsSync(join(harness.plan.capture_root, "tunnel-status-stopped.json")),
    false,
  );
  assert.equal(
    existsSync(join(
      harness.plan.operator_root,
      "raw",
      "automatic-stop-connect-failure.json",
    )),
    true,
  );
});

test("failed status-after performs one validated credential-free stop", (t) => {
  const harness = operationalHarness(t);
  const invalidReady = validRawStatus(harness.healthUrlFile);
  invalidReady.ready = false;
  harness.responses.push(
    { payload: invalidReady },
    { payload: validStoppedRawStatus() },
  );
  assert.throws(
    () => runPreparedTunnelStatusAfter(harness.plan, harness.dependencies),
    /does not establish the required healthy ready identity/u,
  );
  assert.equal(harness.calls.length, 2);
  assert.equal(harness.calls[0].environment.CONTROL_PLANE_API_KEY, "bounded-test-key");
  assert.equal(Object.hasOwn(harness.calls[1].environment, "CONTROL_PLANE_API_KEY"), false);
  assert.equal(
    existsSync(join(harness.plan.capture_root, "tunnel-status-stopped.json")),
    true,
  );
});

test("status-after rejects a stale successful poll and stops", (t) => {
  const harness = operationalHarness(t);
  const stale = validPollHealth(harness.healthUrlFile);
  stale.control_plane_poll.value = Math.floor(Date.now() / 1_000) - 121;
  harness.responses.push(
    { payload: validRawStatus(harness.healthUrlFile) },
    { payload: stale },
    { payload: validStoppedRawStatus() },
  );
  assert.throws(
    () => runPreparedTunnelStatusAfter(harness.plan, harness.dependencies),
    /recent successful poll/u,
  );
  assert.deepEqual(harness.waits, []);
  assert.equal(harness.calls.length, 3);
  assert.equal(
    existsSync(join(harness.plan.capture_root, "tunnel-status-stopped.json")),
    true,
  );
});

test("failed teardown cannot create stopped evidence", (t) => {
  const harness = operationalHarness(t);
  const contradictory = validStoppedRawStatus();
  contradictory.stopped = false;
  harness.responses.push({ payload: contradictory });
  assert.throws(
    () => runPreparedTunnelStop(harness.plan, harness.dependencies),
    /does not establish a stopped local runtime/u,
  );
  assert.equal(
    existsSync(join(harness.plan.capture_root, "tunnel-status-stopped.json")),
    false,
  );
});

test("a failed bounded command is still followed by a client identity check", (t) => {
  const harness = operationalHarness(t);
  harness.responses.push({ status: 2, payload: { error: "synthetic failure" } });
  assert.throws(
    () => executeBoundedTunnelCommand(
      harness.plan,
      "synthetic-command",
      ["runtimes", "status", ALIAS, "--json"],
      true,
      harness.dependencies,
    ),
    /synthetic-command failed closed/u,
  );
  assert.equal(harness.verificationCount(), 2);
});
