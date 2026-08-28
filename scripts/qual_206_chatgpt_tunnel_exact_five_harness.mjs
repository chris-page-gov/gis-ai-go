#!/usr/bin/env node

import { execFileSync, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  closeSync,
  constants,
  fchmodSync,
  fstatSync,
  fsyncSync,
  lstatSync,
  mkdirSync,
  openSync,
  readFileSync,
  readSync,
  realpathSync,
  writeSync,
} from "node:fs";
import { dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

import { buildAndBindGeneratedRuntime } from "./qual_206_claude_capability_harness.mjs";

const ROOT = realpathSync(fileURLToPath(new URL("../", import.meta.url)));
const OBSERVER = join(
  ROOT,
  "scripts",
  "qual_206_chatgpt_tunnel_exact_five_observer.mjs",
);
const PLAN_FILE = "qual-206-chatgpt-tunnel-control-plan.v1.json";
const AUTHORITY = "--chatgpt-tunnel-exact-five-harness-only";
const ENABLE_FLAG = "GIS_AI_GO_QUAL_206_CHATGPT_TUNNEL_EXACT_FIVE_HARNESS";
const OBSERVER_AUTHORITY = "--chatgpt-tunnel-exact-five-observation-only";
const TUNNEL_ID = "tunnel_6a873e7214308191bfe27240c1c03f68";
const TUNNEL_NAME = "gis-ai-go-v0-2-interoperability";
const LOCAL_ALIAS = "gis-ai-go-v0-2-exact-five-v1";
const PROFILE_NAME = "gis-ai-go-v0-2-exact-five-v1";
const CLIENT_LABEL = "chatgpt-openai-tunnel-client-0.0.13";
const STATUS_SCHEMA = "gis-ai-go.qual-206-chatgpt-tunnel-status.v1";
const PLAN_SCHEMA = "gis-ai-go.qual-206-chatgpt-tunnel-control-plan.v1";
const GIT_OBJECT_ID = /^[0-9a-f]{40}$/u;
const SHA256 = /^[0-9a-f]{64}$/u;
const UUID_V4 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/u;
const RUNTIME_KEY_ENVIRONMENT_NAMES = new Set([
  "CONTROL_PLANE_API_KEY",
  "OPENAI_API_KEY",
]);
const MAX_COMMAND_OUTPUT_BYTES = 1_048_576;
const MAX_COMMAND_MILLISECONDS = 60_000;
const MAX_HEALTH_COMMAND_MILLISECONDS = 5_000;
const POLL_HEALTH_ATTEMPTS = 8;
const POLL_HEALTH_RETRY_MILLISECONDS = 5_000;
const POLL_NOT_READY_ERROR = "no successful control-plane poll observed";
const MAX_POLL_SUCCESS_AGE_SECONDS = 120;
const MAX_POLL_SUCCESS_FUTURE_SKEW_SECONDS = 5;
const SAFE_GIT_OPTIONS = Object.freeze([
  "-c",
  "core.fsmonitor=false",
  "-c",
  "core.hooksPath=/dev/null",
]);
const CANONICAL_ORIGIN_URLS = new Set([
  "git@github.com:chris-page-gov/gis-ai-go.git",
  "https://github.com/chris-page-gov/gis-ai-go.git",
]);

export const EXPECTED_TUNNEL_CLIENT = Object.freeze({
  version: "0.0.13",
  buildSha: "4b5267f823be0b046bb883aacb51603cfde3a0ea",
  reportedVersion:
    "0.0.13+4b5267f823be0b046bb883aacb51603cfde3a0ea " +
    "(git sha: 4b5267f823be0b046bb883aacb51603cfde3a0ea)",
  bytes: 20_336_818,
  sha256: "814b5e7ad378e6dfeb7eeebf12df37ff879cfe58fd504769cabfc3e3b4cf99f6",
  archiveSha256: "15abf165f06050af642c948ba6bd6c905191dc5420a9422dadde2b49d892e2c6",
  sha256sumsSha256:
    "e6495395e8f5d952b0edc34a0b552426e38472973a7602f94b3868fbcd9aceb4",
  releaseUrl: "https://github.com/openai/tunnel-client/releases/tag/v0.0.13",
});

function fail(message) {
  throw new Error(message);
}

function plainRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  if (plainRecord(value)) {
    return `{${Object.keys(value).sort().map((key) =>
      `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function positiveInteger(value) {
  return Number.isSafeInteger(value) && value > 0;
}

function validateRuntimeClosure(runtime) {
  const generated = runtime?.generated_first_party_closure;
  const dependencies = runtime?.installed_dependency_closure;
  if (
    !plainRecord(runtime) ||
    !plainRecord(generated) ||
    !plainRecord(dependencies) ||
    !positiveInteger(generated.bytes) ||
    !positiveInteger(generated.file_count) ||
    !SHA256.test(generated.manifest_sha256) ||
    !SHA256.test(generated.reference_manifest_sha256) ||
    generated.reference_manifest_sha256 !== generated.manifest_sha256 ||
    generated.reference_matches_current !== true ||
    !positiveInteger(dependencies.bytes) ||
    !positiveInteger(dependencies.entry_count) ||
    !SHA256.test(dependencies.manifest_sha256)
  ) {
    fail("generated and installed runtime closure is invalid");
  }
  return runtime;
}

function fileIdentity(path) {
  const before = lstatSync(path);
  if (
    !before.isFile() || before.isSymbolicLink() || before.nlink !== 1 ||
    before.uid !== process.getuid() || (before.mode & 0o022) !== 0 ||
    (before.mode & 0o100) === 0
  ) {
    fail(`${path} must be a stable regular file`);
  }
  const bytes = readFileSync(path);
  const after = lstatSync(path);
  if (
    before.dev !== after.dev ||
    before.ino !== after.ino ||
    before.size !== after.size ||
    before.mtimeMs !== after.mtimeMs
  ) {
    fail(`${path} changed while it was measured`);
  }
  return Object.freeze({
    bytes: bytes.length,
    sha256: sha256(bytes),
    dev: after.dev,
    ino: after.ino,
    nlink: after.nlink,
    uid: after.uid,
    mode: after.mode,
  });
}

function ensurePrivateDirectory(path, create = false) {
  if (!isAbsolute(path)) fail("private directories must use absolute paths");
  if (create) mkdirSync(path, { mode: 0o700 });
  const info = lstatSync(path);
  if (!info.isDirectory() || info.isSymbolicLink() || realpathSync(path) !== path) {
    fail(`${path} must be a real directory`);
  }
  if (info.uid !== process.getuid() || (info.mode & 0o777) !== 0o700) {
    fail(`${path} must be owner-only with mode 0700`);
  }
}

function directoryIdentity(path) {
  ensurePrivateDirectory(path);
  const info = lstatSync(path);
  return Object.freeze({ dev: info.dev, ino: info.ino, uid: info.uid, mode: info.mode });
}

function sameDirectoryIdentity(path, expected) {
  const actual = directoryIdentity(path);
  return actual.dev === expected.dev && actual.ino === expected.ino &&
    actual.uid === expected.uid && actual.mode === expected.mode;
}

function fsyncDirectory(path) {
  const descriptor = openSync(path, constants.O_RDONLY | (constants.O_DIRECTORY || 0));
  try {
    fsyncSync(descriptor);
  } finally {
    closeSync(descriptor);
  }
}

function writePrivateJson(path, value) {
  const data = Buffer.from(`${canonicalJson(value)}\n`, "utf8");
  const descriptor = openSync(
    path,
    constants.O_WRONLY |
      constants.O_CREAT |
      constants.O_EXCL |
      (constants.O_NOFOLLOW || 0),
    0o600,
  );
  try {
    fchmodSync(descriptor, 0o600);
    const opened = fstatSync(descriptor);
    if (
      !opened.isFile() || opened.uid !== process.getuid() || opened.nlink !== 1 ||
      (opened.mode & 0o777) !== 0o600
    ) {
      fail("private JSON target is not an owner-only regular file");
    }
    let offset = 0;
    while (offset < data.length) {
      const written = writeSync(descriptor, data, offset, data.length - offset);
      if (written <= 0) fail("private JSON write made no progress");
      offset += written;
    }
    fsyncSync(descriptor);
    const written = fstatSync(descriptor);
    const named = lstatSync(path);
    if (
      written.dev !== opened.dev || written.ino !== opened.ino ||
      written.dev !== named.dev || written.ino !== named.ino ||
      written.nlink !== 1 || named.nlink !== 1 ||
      written.size !== data.length || named.size !== data.length ||
      (written.mode & 0o777) !== 0o600 || (named.mode & 0o777) !== 0o600
    ) {
      fail("private JSON target changed while it was written");
    }
  } finally {
    closeSync(descriptor);
  }
  fsyncDirectory(dirname(path));
}

function parseJson(data, label) {
  let parsed;
  try {
    parsed = JSON.parse(data);
  } catch {
    fail(`${label} is not valid JSON`);
  }
  if (!plainRecord(parsed)) fail(`${label} must be a JSON object`);
  return parsed;
}

function shellQuote(value) {
  if (!value.includes("'") && /^[A-Za-z0-9_@%+=:,./-]+$/u.test(value)) return value;
  return `'${value.replaceAll("'", `'"'"'`)}'`;
}

function runGit(args, allowFailure = false) {
  try {
    return execFileSync("/usr/bin/git", [...SAFE_GIT_OPTIONS, ...args], {
      cwd: ROOT,
      encoding: "utf8",
      env: {
        GIT_CONFIG_GLOBAL: "/dev/null",
        GIT_CONFIG_NOSYSTEM: "1",
        HOME: "/var/empty",
        PATH: "/usr/bin:/bin",
        LANG: "en_GB.UTF-8",
        LC_ALL: "en_GB.UTF-8",
        TZ: "Europe/London",
      },
      stdio: ["ignore", "pipe", "pipe"],
    }).trim();
  } catch (error) {
    if (allowFailure) return null;
    const stderr = error && typeof error === "object" && "stderr" in error
      ? String(error.stderr).trim()
      : "";
    fail(`git verification failed${stderr ? `: ${stderr}` : ""}`);
  }
}

export function verifyProtectedMainCheckout(sourceCommit) {
  if (!GIT_OBJECT_ID.test(sourceCommit)) {
    fail("source commit must be a full lowercase SHA");
  }
  const head = runGit(["rev-parse", "HEAD"]);
  const originMain = runGit(["rev-parse", "origin/main"]);
  const tree = runGit(["rev-parse", "HEAD^{tree}"]);
  const origin = runGit(["remote", "get-url", "origin"]);
  const status = runGit(["status", "--porcelain=v1", "--untracked-files=all"]);
  const symbolicHead = runGit(["symbolic-ref", "-q", "HEAD"], true);
  if (head !== sourceCommit || originMain !== sourceCommit) {
    fail("checkout is not exact origin/main at the supplied source commit");
  }
  if (status !== "") fail("checkout is not clean");
  if (symbolicHead !== null) fail("live observation requires a detached checkout");
  if (!CANONICAL_ORIGIN_URLS.has(origin)) fail("repository origin is not canonical");
  return Object.freeze({
    commit: head,
    tree,
    repositoryOrigin: "https://github.com/chris-page-gov/gis-ai-go.git",
  });
}

export function verifyTunnelClient(
  clientPath,
  expected = EXPECTED_TUNNEL_CLIENT,
  versionRunner = null,
) {
  if (!isAbsolute(clientPath)) fail("tunnel client path must be absolute");
  const client = realpathSync(clientPath);
  if (client !== clientPath) fail("tunnel client path must already be canonical");
  const identity = fileIdentity(client);
  if (identity.bytes !== expected.bytes || identity.sha256 !== expected.sha256) {
    fail("tunnel client bytes do not match the reviewed release");
  }
  const runVersion = versionRunner ?? ((path) => execFileSync(path, ["--version"], {
    encoding: "utf8",
    env: {
      PATH: "/usr/bin:/bin",
      LANG: "en_GB.UTF-8",
      LC_ALL: "en_GB.UTF-8",
      TZ: "Europe/London",
    },
    stdio: ["ignore", "pipe", "pipe"],
    timeout: 10_000,
  }).trim());
  const reportedVersion = runVersion(client);
  if (reportedVersion !== expected.reportedVersion) {
    fail("tunnel client reported version does not match the reviewed release");
  }
  const afterVersion = fileIdentity(client);
  if (
    afterVersion.bytes !== identity.bytes || afterVersion.sha256 !== identity.sha256
  ) {
    fail("tunnel client changed while its reported build was verified");
  }
  return Object.freeze({ path: client, ...afterVersion, reportedVersion });
}

function installPinnedTunnelClient(sourcePath, targetPath) {
  const reviewed = verifyTunnelClient(sourcePath);
  const bytes = readFileSync(reviewed.path);
  const descriptor = openSync(
    targetPath,
    constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL |
      (constants.O_NOFOLLOW || 0),
    0o500,
  );
  try {
    fchmodSync(descriptor, 0o500);
    let offset = 0;
    while (offset < bytes.length) {
      const written = writeSync(descriptor, bytes, offset, bytes.length - offset);
      if (written <= 0) fail("managed tunnel-client copy made no progress");
      offset += written;
    }
    fsyncSync(descriptor);
    const opened = fstatSync(descriptor);
    const named = lstatSync(targetPath);
    if (
      !opened.isFile() || opened.dev !== named.dev || opened.ino !== named.ino ||
      opened.nlink !== 1 || named.nlink !== 1 || opened.size !== bytes.length ||
      named.size !== bytes.length || opened.uid !== process.getuid() ||
      (opened.mode & 0o777) !== 0o500 || (named.mode & 0o777) !== 0o500
    ) {
      fail("managed tunnel-client copy changed while it was installed");
    }
  } finally {
    closeSync(descriptor);
  }
  fsyncDirectory(dirname(targetPath));
  return verifyTunnelClient(targetPath);
}

export function buildObserverCommand(options) {
  const runtime = validateRuntimeClosure(options.runtime);
  const generated = runtime.generated_first_party_closure;
  const dependencies = runtime.installed_dependency_closure;
  const node = realpathSync(process.execPath);
  const values = [
    "/usr/bin/env",
    "-i",
    "PATH=/usr/bin:/bin",
    "LANG=en_GB.UTF-8",
    "LC_ALL=en_GB.UTF-8",
    "TZ=Europe/London",
    `TMPDIR=${options.observerTmpDir}`,
    "GIS_AI_GO_QUAL_206_CHATGPT_TUNNEL_EXACT_FIVE=1",
    "GIS_AI_GO_QUAL_206_EVENT_CAPTURE=1",
    "GIS_AI_GO_QUAL_206_MCP_NETWORK_SANDBOX=macos-seatbelt-deny-network",
    "GIS_AI_GO_QUAL_206_HOST_ATTESTATION=outer-harness-bound-tunnel-client",
    node,
    OBSERVER,
    OBSERVER_AUTHORITY,
    "--capture-root",
    options.captureRoot,
    "--run-id",
    options.runId,
    "--client",
    CLIENT_LABEL,
    "--source-commit",
    options.sourceCommit,
    "--expected-parent-sha256",
    options.parentSha256,
    "--expected-parent-bytes",
    String(options.parentBytes),
    "--expected-generated-runtime-bytes",
    String(generated.bytes),
    "--expected-generated-runtime-file-count",
    String(generated.file_count),
    "--expected-generated-runtime-manifest-sha256",
    generated.manifest_sha256,
    "--expected-generated-runtime-reference-manifest-sha256",
    generated.reference_manifest_sha256,
    "--expected-generated-runtime-reference-matches-current",
    String(generated.reference_matches_current),
    "--expected-installed-dependency-bytes",
    String(dependencies.bytes),
    "--expected-installed-dependency-entry-count",
    String(dependencies.entry_count),
    "--expected-installed-dependency-manifest-sha256",
    dependencies.manifest_sha256,
  ];
  return values.map(shellQuote).join(" ");
}

export function parseChatGptTunnelHarnessArguments(argv, environment = process.env) {
  if (environment[ENABLE_FLAG] !== "1" || argv[0] !== AUTHORITY) {
    fail(`refusing tunnel harness without ${ENABLE_FLAG}=1 and ${AUTHORITY}`);
  }
  const values = new Map();
  for (let index = 1; index < argv.length; index += 2) {
    const name = argv[index];
    const value = argv[index + 1];
    if (!name?.startsWith("--") || value === undefined || values.has(name)) {
      fail("tunnel harness arguments must be unique option/value pairs");
    }
    values.set(name, value);
  }
  const phase = values.get("--phase");
  if (!["prepare", "connect", "status-after", "stop"].includes(phase)) {
    fail("phase must be prepare, connect, status-after or stop");
  }
  const allowed = phase === "prepare"
    ? new Set([
      "--phase",
      "--capture-root",
      "--operator-root",
      "--run-id",
      "--source-commit",
      "--client",
      "--pnpm",
      "--runtime-key-env",
    ])
    : new Set(["--phase", "--operator-root"]);
  if ([...values.keys()].some((name) => !allowed.has(name))) {
    fail("tunnel harness received an unsupported option for this phase");
  }
  if ([...allowed].some((name) => !values.has(name))) {
    fail("tunnel harness is missing a required option");
  }
  if (phase === "prepare") {
    if (!UUID_V4.test(values.get("--run-id"))) fail("run ID must be a UUID v4");
    if (!GIT_OBJECT_ID.test(values.get("--source-commit"))) {
      fail("source commit must be a full lowercase SHA");
    }
    if (!RUNTIME_KEY_ENVIRONMENT_NAMES.has(values.get("--runtime-key-env"))) {
      fail("runtime key environment name is outside the closed allowlist");
    }
    const pnpm = values.get("--pnpm");
    let canonicalPnpm = false;
    try {
      canonicalPnpm = isAbsolute(pnpm) && realpathSync(pnpm) === pnpm;
    } catch {
      canonicalPnpm = false;
    }
    if (!canonicalPnpm) {
      fail("pnpm path must be an existing canonical absolute path");
    }
  }
  return Object.freeze({
    phase,
    captureRoot: values.get("--capture-root"),
    operatorRoot: values.get("--operator-root"),
    runId: values.get("--run-id"),
    sourceCommit: values.get("--source-commit"),
    client: values.get("--client"),
    pnpm: values.get("--pnpm"),
    runtimeKeyEnv: values.get("--runtime-key-env"),
  });
}

export function validatePrivateRootLayout(captureRoot, operatorRoot) {
  if (!isAbsolute(captureRoot) || !isAbsolute(operatorRoot)) {
    fail("capture and operator roots must be absolute");
  }
  const capture = resolve(captureRoot);
  const operator = resolve(operatorRoot);
  if (capture !== captureRoot || operator !== operatorRoot) {
    fail("capture and operator roots must already be canonical paths");
  }
  if (capture === operator) fail("capture and operator roots must be separate");
  const captureToOperator = relative(capture, operator);
  const operatorToCapture = relative(operator, capture);
  const inside = (value) => value !== "" && value !== ".." && !value.startsWith(`..${sep}`);
  if (inside(captureToOperator) || inside(operatorToCapture)) {
    fail("capture and operator roots must not contain one another");
  }
  for (const value of [capture, operator]) {
    const fromRepository = relative(ROOT, value);
    if (fromRepository === "" || inside(fromRepository)) {
      fail("private roots must remain outside the Git checkout");
    }
  }
  const captureParent = dirname(capture);
  const operatorParent = dirname(operator);
  if (captureParent !== operatorParent) {
    fail("capture and operator roots must share one owner-only parent");
  }
  ensurePrivateDirectory(captureParent);
}

function commandEnvironment(plan, requireRuntimeKey, ambientEnvironment = process.env) {
  const runtimeValue = ambientEnvironment[plan.runtime_key_environment];
  if (requireRuntimeKey && (
    typeof runtimeValue !== "string" ||
    runtimeValue.trim() === "" ||
    /[\r\n]/u.test(runtimeValue)
  )) {
    fail(`runtime key is unavailable through ${plan.runtime_key_environment}`);
  }
  const environment = {
    HOME: join(plan.operator_root, "home"),
    LANG: "en_GB.UTF-8",
    LC_ALL: "en_GB.UTF-8",
    // Deliberately omit Homebrew and other user-writable command directories.
    // With no tmux on this path, v0.0.13 uses its managed direct-process fallback.
    PATH: "/usr/bin:/bin",
    TMPDIR: join(plan.operator_root, "tmp"),
    TUNNEL_CLIENT_STATE_DIR: join(plan.operator_root, "tunnel-state"),
    TZ: "Europe/London",
    XDG_CONFIG_HOME: join(plan.operator_root, "xdg"),
  };
  if (requireRuntimeKey && runtimeValue !== undefined) {
    environment[plan.runtime_key_environment] = runtimeValue;
  }
  return environment;
}

export function validateTunnelControlPlan(plan, operatorRoot) {
  if (
    !plainRecord(plan) ||
    plan.schema !== PLAN_SCHEMA ||
    plan.operator_root !== operatorRoot ||
    plan.alias !== LOCAL_ALIAS ||
    plan.profile_name !== PROFILE_NAME ||
    plan.tunnel_id !== TUNNEL_ID ||
    plan.tunnel_name !== TUNNEL_NAME ||
    !UUID_V4.test(plan.run_id) ||
    !GIT_OBJECT_ID.test(plan.source_commit) ||
    !GIT_OBJECT_ID.test(plan.source_tree) ||
    !isAbsolute(plan.client_path) ||
    !SHA256.test(plan.client_sha256) ||
    !Number.isSafeInteger(plan.client_dev) ||
    !Number.isSafeInteger(plan.client_ino) ||
    !Number.isSafeInteger(plan.client_uid) ||
    !Number.isSafeInteger(plan.client_mode) ||
    plan.client_nlink !== 1 ||
    !RUNTIME_KEY_ENVIRONMENT_NAMES.has(plan.runtime_key_environment) ||
    !plainRecord(plan.runtime) ||
    typeof plan.mcp_command !== "string" ||
    sha256(Buffer.from(plan.mcp_command, "utf8")) !== plan.mcp_command_sha256
  ) {
    fail("private tunnel control plan is invalid");
  }
  validatePrivateRootLayout(plan.capture_root, plan.operator_root);
  validateRuntimeClosure(plan.runtime);
  if (
    !plainRecord(plan.capture_root_identity) ||
    !plainRecord(plan.operator_root_identity) ||
    !sameDirectoryIdentity(plan.capture_root, plan.capture_root_identity) ||
    !sameDirectoryIdentity(plan.operator_root, plan.operator_root_identity)
  ) {
    fail("private tunnel root identity changed");
  }
  return plan;
}

function readPrivatePlan(path) {
  const descriptor = openSync(path, constants.O_RDONLY | (constants.O_NOFOLLOW || 0));
  try {
    const before = fstatSync(descriptor);
    if (
      !before.isFile() ||
      before.uid !== process.getuid() ||
      (before.mode & 0o777) !== 0o600 ||
      before.size < 2 ||
      before.size > 1_048_576
    ) {
      fail("private tunnel control plan is not an owner-only bounded regular file");
    }
    const data = Buffer.alloc(before.size);
    let offset = 0;
    while (offset < data.length) {
      const read = readSync(descriptor, data, offset, data.length - offset, offset);
      if (read <= 0) fail("private tunnel control plan ended early");
      offset += read;
    }
    const after = fstatSync(descriptor);
    const named = lstatSync(path);
    if (
      before.dev !== after.dev || before.ino !== after.ino ||
      before.size !== after.size || before.mtimeMs !== after.mtimeMs ||
      before.nlink !== 1 || after.nlink !== 1 || named.nlink !== 1 ||
      after.dev !== named.dev || after.ino !== named.ino || after.size !== named.size
    ) {
      fail("private tunnel control plan changed while it was read");
    }
    return parseJson(data.toString("utf8"), "control plan");
  } finally {
    closeSync(descriptor);
  }
}

export function loadTunnelControlPlan(operatorRoot) {
  ensurePrivateDirectory(operatorRoot);
  const path = join(operatorRoot, PLAN_FILE);
  return validateTunnelControlPlan(readPrivatePlan(path), operatorRoot);
}

function executeTunnelClientCommand(
  plan,
  label,
  args,
  requireRuntimeKey = true,
  dependencies = {},
  timeout = MAX_COMMAND_MILLISECONDS,
) {
  const verifyClient = dependencies.verifyTunnelClient ?? verifyTunnelClient;
  const run = dependencies.spawnSync ?? spawnSync;
  const verifiedClient = verifyClient(plan.client_path);
  if (
    verifiedClient.bytes !== plan.client_bytes ||
    verifiedClient.sha256 !== plan.client_sha256 ||
    verifiedClient.dev !== plan.client_dev ||
    verifiedClient.ino !== plan.client_ino ||
    verifiedClient.nlink !== plan.client_nlink ||
    verifiedClient.uid !== plan.client_uid ||
    verifiedClient.mode !== plan.client_mode ||
    verifiedClient.reportedVersion !== plan.client_reported_version
  ) {
    fail("tunnel client no longer matches the private control plan");
  }
  const environment = commandEnvironment(
    plan,
    requireRuntimeKey,
    dependencies.environment ?? process.env,
  );
  const startedAt = new Date().toISOString();
  const result = run(plan.client_path, args, {
    cwd: ROOT,
    encoding: "utf8",
    env: environment,
    maxBuffer: MAX_COMMAND_OUTPUT_BYTES,
    stdio: ["ignore", "pipe", "pipe"],
    timeout,
  });
  const finishedAt = new Date().toISOString();
  const stdout = typeof result.stdout === "string" ? result.stdout : "";
  const stderr = typeof result.stderr === "string" ? result.stderr : "";
  const secret = environment[plan.runtime_key_environment];
  if (secret && (stdout.includes(secret) || stderr.includes(secret))) {
    fail(`${label} attempted to expose the runtime credential`);
  }
  writePrivateJson(join(plan.operator_root, "raw", `${label}.json`), {
    schema: "gis-ai-go.qual-206-chatgpt-tunnel-private-command.v1",
    label,
    started_at: startedAt,
    finished_at: finishedAt,
    exit_code: result.status,
    signal: result.signal,
    stdout,
    stderr,
  });
  const afterExecution = verifyClient(plan.client_path);
  if (
    afterExecution.dev !== plan.client_dev || afterExecution.ino !== plan.client_ino ||
    afterExecution.nlink !== plan.client_nlink ||
    afterExecution.uid !== plan.client_uid || afterExecution.mode !== plan.client_mode ||
    afterExecution.sha256 !== plan.client_sha256
  ) {
    fail("tunnel client changed while the bounded command executed");
  }
  return Object.freeze({ result, stdout, stderr });
}

export function executeBoundedTunnelCommand(
  plan,
  label,
  args,
  requireRuntimeKey = true,
  dependencies = {},
) {
  const { result, stdout } = executeTunnelClientCommand(
    plan,
    label,
    args,
    requireRuntimeKey,
    dependencies,
  );
  if (result.error || result.status !== 0) {
    fail(`${label} failed closed`);
  }
  return parseJson(stdout, `${label} stdout`);
}

function nullableEmpty(value, label) {
  if (value === null || value === undefined || value === "") return null;
  fail(`${label} reported an error`);
}

function nestedRecord(value, key, label) {
  if (!plainRecord(value) || !plainRecord(value[key])) fail(`${label} is missing ${key}`);
  return value[key];
}

function emptyOrAbsent(value) {
  return value === null || value === undefined || value === "";
}

function expectedHealthUrlFile(plan) {
  return join(
    plan.operator_root,
    "tunnel-state",
    "health",
    `${LOCAL_ALIAS}.url`,
  );
}

function validateLoopbackBaseUrl(value, label) {
  let parsed;
  try {
    parsed = new URL(value);
  } catch {
    fail(`${label} is not a valid URL`);
  }
  if (
    parsed.protocol !== "http:" ||
    parsed.hostname !== "127.0.0.1" ||
    parsed.username !== "" ||
    parsed.password !== "" ||
    parsed.pathname !== "/" ||
    parsed.search !== "" ||
    parsed.hash !== "" ||
    !/^[0-9]{1,5}$/u.test(parsed.port) ||
    Number(parsed.port) < 1 ||
    Number(parsed.port) > 65_535
  ) {
    fail(`${label} is not an exact loopback HTTP base URL`);
  }
  return parsed.origin;
}

function validatePollHealthEnvelope(raw, healthUrlFile, expectedPid) {
  if (!plainRecord(raw)) fail("control-plane poll health input is invalid");
  const locator = nestedRecord(raw, "locator", "control-plane poll health");
  const processRecord = nestedRecord(raw, "process", "control-plane poll health");
  const healthz = nestedRecord(raw, "healthz", "control-plane poll health");
  const readyz = nestedRecord(raw, "readyz", "control-plane poll health");
  const poll = nestedRecord(raw, "control_plane_poll", "control-plane poll health");
  const baseUrl = validateLoopbackBaseUrl(
    locator.resolved_base_url,
    "control-plane poll health locator",
  );
  if (
    locator.kind !== "url_file" ||
    locator.url_file !== healthUrlFile ||
    !emptyOrAbsent(locator.error) ||
    processRecord.pid !== expectedPid ||
    processRecord.running !== true ||
    !emptyOrAbsent(processRecord.error) ||
    raw.base_url !== baseUrl ||
    healthz.url !== `${baseUrl}/healthz` ||
    healthz.ok !== true ||
    healthz.status !== 200 ||
    healthz.body !== "live" ||
    !emptyOrAbsent(healthz.error) ||
    readyz.url !== `${baseUrl}/readyz` ||
    readyz.ok !== true ||
    readyz.status !== 200 ||
    readyz.body !== "ready" ||
    !emptyOrAbsent(readyz.error) ||
    poll.url !== `${baseUrl}/metrics`
  ) {
    fail("control-plane poll health does not bind the ready loopback runtime");
  }
  return poll;
}

export function validateSuccessfulPollHealth(
  raw,
  healthUrlFile,
  expectedPid,
  nowMilliseconds = Date.now(),
) {
  const poll = validatePollHealthEnvelope(raw, healthUrlFile, expectedPid);
  const nowSeconds = nowMilliseconds / 1_000;
  const pollAgeSeconds = nowSeconds - poll.value;
  if (
    raw.result !== "ok" ||
    poll.ok !== true ||
    !Number.isSafeInteger(poll.value) ||
    poll.value <= 0 ||
    pollAgeSeconds < -MAX_POLL_SUCCESS_FUTURE_SKEW_SECONDS ||
    pollAgeSeconds > MAX_POLL_SUCCESS_AGE_SECONDS ||
    !emptyOrAbsent(poll.error)
  ) {
    fail("control-plane poll health does not prove a recent successful poll");
  }
  return Object.freeze({ state: "healthy", route_kind: "control_plane" });
}

function validatePendingPollHealth(raw, healthUrlFile, expectedPid) {
  const poll = validatePollHealthEnvelope(raw, healthUrlFile, expectedPid);
  if (
    raw.result !== "fail" ||
    poll.ok !== false ||
    Object.hasOwn(poll, "value") ||
    poll.error !== POLL_NOT_READY_ERROR
  ) {
    fail("control-plane poll health failed outside the bounded startup state");
  }
}

function waitForPollRetry(milliseconds) {
  const signal = new Int32Array(new SharedArrayBuffer(Int32Array.BYTES_PER_ELEMENT));
  Atomics.wait(signal, 0, 0, milliseconds);
}

function validateRuntimeBinding(raw, expectedMcpCommandSha256) {
  const processRecord = nestedRecord(raw, "process", "tunnel status");
  if (
    raw.profile_name !== PROFILE_NAME ||
    processRecord.alias !== LOCAL_ALIAS ||
    processRecord.tunnel_id !== TUNNEL_ID ||
    processRecord.profile_name !== PROFILE_NAME ||
    processRecord.target_kind !== "command" ||
    typeof processRecord.target_value !== "string" ||
    !SHA256.test(expectedMcpCommandSha256) ||
    sha256(Buffer.from(processRecord.target_value, "utf8")) !== expectedMcpCommandSha256
  ) {
    fail("tunnel status does not bind the reviewed profile and MCP command");
  }
  return Object.freeze({
    profile_name: PROFILE_NAME,
    target_kind: "command",
    mcp_command_sha256: expectedMcpCommandSha256,
  });
}

function validateReadyTunnelStatus(raw, expectedMcpCommandSha256, healthUrlFile) {
  if (!plainRecord(raw)) fail("tunnel status input is invalid");
  const binding = validateRuntimeBinding(raw, expectedMcpCommandSha256);
  const processRecord = nestedRecord(raw, "process", "ready tunnel status");
  const remote = raw.remote;
  const local = raw.local;
  const effectiveHealth = nestedRecord(local, "effective_health", "local status");
  const healthz = nestedRecord(effectiveHealth, "healthz", "effective health");
  const readyz = nestedRecord(effectiveHealth, "readyz", "effective health");
  const poll = nestedRecord(raw, "control_plane_poll_health", "tunnel status");
  const route = poll.route;
  const directRoute = plainRecord(route) &&
    ["healthy", "direct"].includes(poll.state) &&
    route.kind === "control_plane";
  const currentRuntimeSnapshotUnavailable =
    poll.state === "unknown" &&
    poll.reason === "no live admin UI system snapshot" &&
    !Object.hasOwn(poll, "route");
  if (
    raw.alias !== LOCAL_ALIAS ||
    raw.tunnel_id !== TUNNEL_ID ||
    !plainRecord(remote) ||
    remote.id !== TUNNEL_ID ||
    remote.name !== TUNNEL_NAME ||
    raw.stale !== false ||
    !emptyOrAbsent(raw.error) ||
    !emptyOrAbsent(raw.remote_error) ||
    raw.runtime_state !== "ready" ||
    raw.healthy !== true ||
    raw.ready !== true ||
    raw.remote_lookup_attempted !== true ||
    raw.process_running !== true ||
    processRecord.mode !== "process" ||
    !positiveInteger(processRecord.pid) ||
    raw.health_url_file !== healthUrlFile ||
    healthz.ok !== true ||
    healthz.status !== 200 ||
    readyz.ok !== true ||
    readyz.status !== 200 ||
    (!directRoute && !currentRuntimeSnapshotUnavailable)
  ) {
    fail("tunnel status does not establish the required healthy ready identity");
  }
  return Object.freeze({ binding, healthz, readyz, pid: processRecord.pid });
}

export function projectTunnelStatus(
  raw,
  pollHealth,
  phase,
  expectedMcpCommandSha256,
  healthUrlFile,
  observedAt = new Date().toISOString(),
) {
  if (!["before", "after"].includes(phase)) {
    fail("tunnel status input is invalid");
  }
  const { binding, pid } = validateReadyTunnelStatus(
    raw,
    expectedMcpCommandSha256,
    healthUrlFile,
  );
  const pollProjection = validateSuccessfulPollHealth(pollHealth, healthUrlFile, pid);
  return Object.freeze({
    schema: STATUS_SCHEMA,
    phase,
    observed_at: observedAt,
    alias: LOCAL_ALIAS,
    tunnel_id: TUNNEL_ID,
    ...binding,
    remote: Object.freeze({ found: true, id: TUNNEL_ID, name: TUNNEL_NAME }),
    stale: false,
    error: nullableEmpty(raw.error, "tunnel status"),
    remote_error: nullableEmpty(raw.remote_error, "remote tunnel lookup"),
    runtime_state: "ready",
    healthy: true,
    ready: true,
    control_plane_poll_health: pollProjection,
    remote_lookup_attempted: true,
    process_running: true,
    local: Object.freeze({
      healthz_status: 200,
      readyz_status: 200,
      direct_healthy_poll_route: true,
    }),
  });
}

export function projectStoppedTunnelStatus(
  raw,
  expectedMcpCommandSha256,
  observedAt = new Date().toISOString(),
) {
  if (!plainRecord(raw)) fail("stopped tunnel status input is invalid");
  const binding = validateRuntimeBinding(raw, expectedMcpCommandSha256);
  const processRecord = nestedRecord(raw, "process", "stopped tunnel status");
  const local = nestedRecord(raw, "local", "stopped tunnel status");
  const effectiveHealth = nestedRecord(local, "effective_health", "stopped local status");
  const healthz = nestedRecord(effectiveHealth, "healthz", "stopped effective health");
  const readyz = nestedRecord(effectiveHealth, "readyz", "stopped effective health");
  const poll = nestedRecord(raw, "control_plane_poll_health", "stopped tunnel status");
  const liveAdmin = nestedRecord(local, "live_admin_ui", "stopped local status");
  if (
    raw.alias !== LOCAL_ALIAS ||
    raw.tunnel_id !== TUNNEL_ID ||
    raw.stale !== false ||
    raw.runtime_state !== "stopped" ||
    raw.healthy !== false ||
    raw.ready !== false ||
    raw.remote_lookup_attempted !== false ||
    raw.process_running !== false ||
    raw.remote !== null ||
    raw.stopped !== true ||
    raw.stop_error !== "" ||
    processRecord.mode !== "stopped" ||
    Object.hasOwn(processRecord, "pid") || Object.hasOwn(raw, "pid") ||
    healthz.ok !== false || healthz.status !== 0 ||
    readyz.ok !== false || readyz.status !== 0 ||
    poll.state !== "unknown" || liveAdmin.found !== false
  ) {
    fail("tunnel stop output does not establish a stopped local runtime");
  }
  return Object.freeze({
    schema: STATUS_SCHEMA,
    phase: "stopped",
    observed_at: observedAt,
    alias: LOCAL_ALIAS,
    tunnel_id: TUNNEL_ID,
    ...binding,
    remote: Object.freeze({
      found: false,
      id: TUNNEL_ID,
      name: TUNNEL_NAME,
    }),
    stale: false,
    error: nullableEmpty(raw.error, "stopped tunnel status"),
    remote_error: nullableEmpty(raw.remote_error, "stopped remote tunnel lookup"),
    runtime_state: "stopped",
    healthy: false,
    ready: false,
    control_plane_poll_health: null,
    remote_lookup_attempted: false,
    process_running: false,
    local: Object.freeze({
      healthz_status: null,
      readyz_status: null,
      direct_healthy_poll_route: false,
    }),
  });
}

function captureStatus(plan, phase, dependencies = {}) {
  const raw = executeBoundedTunnelCommand(
    plan,
    `tunnel-status-${phase}-raw`,
    ["runtimes", "status", LOCAL_ALIAS, "--json"],
    true,
    dependencies,
  );
  const healthUrlFile = expectedHealthUrlFile(plan);
  const { pid } = validateReadyTunnelStatus(
    raw,
    plan.mcp_command_sha256,
    healthUrlFile,
  );
  let pollHealth;
  for (let attempt = 1; attempt <= POLL_HEALTH_ATTEMPTS; attempt += 1) {
    const label = `tunnel-poll-health-${phase}-attempt-${attempt}-raw`;
    const { result, stdout, stderr } = executeTunnelClientCommand(
      plan,
      label,
      [
        "health",
        "--url-file",
        healthUrlFile,
        "--pid",
        String(pid),
        "--require-control-plane-poll",
        "--json",
      ],
      false,
      dependencies,
      MAX_HEALTH_COMMAND_MILLISECONDS,
    );
    if (result.error || result.signal !== null || stderr !== "") {
      fail(`${label} failed closed`);
    }
    const candidate = parseJson(stdout, `${label} stdout`);
    if (result.status === 0) {
      validateSuccessfulPollHealth(candidate, healthUrlFile, pid);
      pollHealth = candidate;
      break;
    }
    if (result.status !== 2) fail(`${label} failed closed`);
    validatePendingPollHealth(candidate, healthUrlFile, pid);
    if (attempt === POLL_HEALTH_ATTEMPTS) {
      fail("control-plane poll did not succeed within the bounded readiness window");
    }
    const wait = dependencies.waitForPollRetry ?? waitForPollRetry;
    wait(POLL_HEALTH_RETRY_MILLISECONDS);
  }
  const status = projectTunnelStatus(
    raw,
    pollHealth,
    phase,
    plan.mcp_command_sha256,
    healthUrlFile,
  );
  writePrivateJson(join(plan.capture_root, `tunnel-status-${phase}.json`), status);
  return status;
}

function errorMessage(error) {
  return error instanceof Error ? error.message : "unknown harness failure";
}

function stopAndProject(plan, rawLabel, dependencies = {}) {
  const output = executeBoundedTunnelCommand(
    plan,
    rawLabel,
    ["runtimes", "stop", LOCAL_ALIAS, "--json"],
    false,
    dependencies,
  );
  const status = projectStoppedTunnelStatus(output, plan.mcp_command_sha256);
  writePrivateJson(join(plan.capture_root, "tunnel-status-stopped.json"), status);
  return status;
}

function bestEffortStop(plan, reason, primaryError, dependencies = {}) {
  try {
    return stopAndProject(plan, `automatic-stop-${reason}`, dependencies);
  } catch (teardownError) {
    throw new AggregateError(
      [primaryError, teardownError],
      `${errorMessage(primaryError)}; automatic tunnel teardown failed: ` +
        errorMessage(teardownError),
      { cause: primaryError },
    );
  }
}

function prepare(options) {
  validatePrivateRootLayout(options.captureRoot, options.operatorRoot);
  const source = verifyProtectedMainCheckout(options.sourceCommit);
  verifyTunnelClient(options.client);
  ensurePrivateDirectory(options.captureRoot, true);
  ensurePrivateDirectory(options.operatorRoot, true);
  const client = installPinnedTunnelClient(
    options.client,
    join(options.operatorRoot, "tunnel-client-v0.0.13"),
  );
  for (const path of [
    join(options.operatorRoot, "home"),
    join(options.operatorRoot, "profiles"),
    join(options.operatorRoot, "raw"),
    join(options.operatorRoot, "tmp"),
    join(options.operatorRoot, "tunnel-state"),
    join(options.operatorRoot, "xdg"),
  ]) ensurePrivateDirectory(path, true);
  const observerTmpDir = join(options.operatorRoot, "tmp", "observer");
  ensurePrivateDirectory(observerTmpDir, true);
  const runtime = validateRuntimeClosure(
    buildAndBindGeneratedRuntime(source.commit, options.pnpm),
  );
  const sourceAfterBuild = verifyProtectedMainCheckout(options.sourceCommit);
  if (sourceAfterBuild.tree !== source.tree) {
    fail("protected-main source tree changed while binding the generated runtime");
  }
  const mcpCommand = buildObserverCommand({
    observerTmpDir,
    captureRoot: options.captureRoot,
    runId: options.runId,
    sourceCommit: options.sourceCommit,
    parentSha256: client.sha256,
    parentBytes: client.bytes,
    runtime,
  });
  const plan = {
    schema: PLAN_SCHEMA,
    run_id: options.runId,
    source_commit: source.commit,
    source_tree: source.tree,
    repository_origin: source.repositoryOrigin,
    clean_detached_checkout: true,
    capture_root: options.captureRoot,
    operator_root: options.operatorRoot,
    capture_root_identity: directoryIdentity(options.captureRoot),
    operator_root_identity: directoryIdentity(options.operatorRoot),
    client_path: client.path,
    client_version: EXPECTED_TUNNEL_CLIENT.version,
    client_build_sha: EXPECTED_TUNNEL_CLIENT.buildSha,
    client_reported_version: client.reportedVersion,
    client_bytes: client.bytes,
    client_sha256: client.sha256,
    client_dev: client.dev,
    client_ino: client.ino,
    client_nlink: client.nlink,
    client_uid: client.uid,
    client_mode: client.mode,
    client_archive_sha256: EXPECTED_TUNNEL_CLIENT.archiveSha256,
    client_sha256sums_sha256: EXPECTED_TUNNEL_CLIENT.sha256sumsSha256,
    client_release_url: EXPECTED_TUNNEL_CLIENT.releaseUrl,
    tunnel_id: TUNNEL_ID,
    tunnel_name: TUNNEL_NAME,
    alias: LOCAL_ALIAS,
    profile_name: PROFILE_NAME,
    runtime_key_environment: options.runtimeKeyEnv,
    runtime,
    mcp_command: mcpCommand,
    mcp_command_sha256: sha256(Buffer.from(mcpCommand, "utf8")),
  };
  writePrivateJson(join(options.operatorRoot, PLAN_FILE), plan);
  return plan;
}

export function runPreparedTunnelConnect(plan, dependencies = {}) {
  const verifyCheckout = dependencies.verifyProtectedMainCheckout ??
    verifyProtectedMainCheckout;
  const verifyClient = dependencies.verifyTunnelClient ?? verifyTunnelClient;
  verifyCheckout(plan.source_commit);
  verifyClient(plan.client_path);
  try {
    executeBoundedTunnelCommand(plan, "tunnel-connect-raw", [
      "runtimes",
      "connect",
      "--alias",
      LOCAL_ALIAS,
      "--profile",
      PROFILE_NAME,
      "--profile-dir",
      join(plan.operator_root, "profiles"),
      "--runtime-api-key",
      `env:${plan.runtime_key_environment}`,
      "--tunnel-id",
      TUNNEL_ID,
      "--mcp-command",
      plan.mcp_command,
      "--json",
    ], true, dependencies);
    return captureStatus(plan, "before", dependencies);
  } catch (error) {
    bestEffortStop(plan, "connect-failure", error, dependencies);
    throw error;
  }
}

export function runPreparedTunnelStatusAfter(plan, dependencies = {}) {
  try {
    return captureStatus(plan, "after", dependencies);
  } catch (error) {
    bestEffortStop(plan, "status-after-failure", error, dependencies);
    throw error;
  }
}

export function runPreparedTunnelStop(plan, dependencies = {}) {
  const verifyClient = dependencies.verifyTunnelClient ?? verifyTunnelClient;
  verifyClient(plan.client_path);
  return stopAndProject(plan, "tunnel-stop-raw", dependencies);
}

async function main() {
  const options = parseChatGptTunnelHarnessArguments(process.argv.slice(2));
  let result;
  let runId;
  if (options.phase === "prepare") {
    result = prepare(options);
    runId = result.run_id;
  } else {
    const plan = loadTunnelControlPlan(options.operatorRoot);
    runId = plan.run_id;
    if (options.phase === "connect") result = runPreparedTunnelConnect(plan);
    if (options.phase === "status-after") result = runPreparedTunnelStatusAfter(plan);
    if (options.phase === "stop") result = runPreparedTunnelStop(plan);
  }
  process.stdout.write(`${canonicalJson({
    status: "complete",
    phase: options.phase,
    run_id: runId,
  })}\n`);
}

const entry = process.argv[1];
if (entry !== undefined && import.meta.url === pathToFileURL(resolve(entry)).href) {
  try {
    await main();
  } catch (error) {
    const message = errorMessage(error);
    process.stderr.write(`QUAL-206 ChatGPT tunnel harness failed: ${message}\n`);
    process.exitCode = 2;
  }
}
