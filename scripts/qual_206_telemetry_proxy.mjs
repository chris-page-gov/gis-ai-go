import { spawn } from "node:child_process";
import { createHash, randomUUID } from "node:crypto";
import { closeSync, constants, fchmodSync, openSync, writeSync } from "node:fs";

const TELEMETRY_SCHEMA = "gis-ai-go.qual-206-host-telemetry.v1";
const MAX_FRAME_BYTES = 1_048_576;
const MAX_CLIENT_LABEL_CODE_POINTS = 64;
const FULL_COMMIT = /^[0-9a-f]{40}$/u;
const CLIENT_LABEL = /^[a-z0-9](?:[a-z0-9._-]{0,62}[a-z0-9])?$/u;
const TELEMETRY_METHODS = new Set([
  "resources/list",
  "resources/read",
  "resources/templates/list",
  "server/discover",
  "tools/call",
  "tools/list",
]);
const TELEMETRY_OPERATIONS = new Set([
  "catalogue.describe",
  "catalogue.search",
]);

function usage() {
  throw new Error(
    "Usage: node scripts/qual_206_telemetry_proxy.mjs " +
      "--log <absolute-jsonl-path> --client <label> -- <command> [args...]",
  );
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function parseArguments(argv) {
  const separator = argv.indexOf("--");
  if (separator === -1 || separator === argv.length - 1) usage();
  const options = argv.slice(0, separator);
  const command = argv.slice(separator + 1);
  let logPath = "";
  let client = "";
  for (let index = 0; index < options.length; index += 2) {
    const name = options[index];
    const value = options[index + 1];
    if (value === undefined) usage();
    if (name === "--log") logPath = value;
    else if (name === "--client") client = value;
    else usage();
  }
  if (!logPath.startsWith("/") || logPath.includes("\0")) usage();
  const clientPoints = Array.from(client);
  if (
    clientPoints.length === 0 ||
    clientPoints.length > MAX_CLIENT_LABEL_CODE_POINTS ||
    !CLIENT_LABEL.test(client)
  ) {
    usage();
  }
  return { client, command, logPath };
}

const { client, command, logPath } = parseArguments(process.argv.slice(2));
const log = openSync(
  logPath,
  constants.O_APPEND |
    constants.O_CREAT |
    constants.O_WRONLY |
    (constants.O_NOFOLLOW ?? 0),
  0o600,
);
fchmodSync(log, 0o600);
const sessionId = randomUUID();
const requests = new Map();
let logClosed = false;

function writeEvent(event) {
  if (logClosed) return;
  const value = {
    schema: TELEMETRY_SCHEMA,
    session_id: sessionId,
    observed_at: new Date().toISOString(),
    ...event,
  };
  writeSync(log, `${JSON.stringify(value)}\n`);
}

function closeLog() {
  if (logClosed) return;
  logClosed = true;
  closeSync(log);
}

function allowlistedLabel(value, allowed) {
  return typeof value === "string" && allowed.has(value) ? value : "other";
}

function idDigest(value) {
  return value === undefined ? undefined : sha256(JSON.stringify(value));
}

function recordFrame(direction, frame) {
  if (frame.length === 0 || frame.length > MAX_FRAME_BYTES) {
    writeEvent({
      event: "invalid_frame",
      direction,
      frame_bytes: frame.length,
      frame_sha256: sha256(frame),
    });
    return;
  }
  let message;
  try {
    message = JSON.parse(frame.toString("utf8"));
  } catch {
    writeEvent({
      event: "non_json_frame",
      direction,
      frame_bytes: frame.length,
      frame_sha256: sha256(frame),
    });
    return;
  }
  if (message === null || typeof message !== "object" || Array.isArray(message)) {
    writeEvent({
      event: "non_object_frame",
      direction,
      frame_bytes: frame.length,
      frame_sha256: sha256(frame),
    });
    return;
  }

  const requestIdSha256 = idDigest(message.id);
  if (direction === "client_to_server" && typeof message.method === "string") {
    const params = message.params ?? null;
    const paramsBytes = Buffer.from(JSON.stringify(params));
    if (requestIdSha256 !== undefined) {
      requests.set(requestIdSha256, process.hrtime.bigint());
    }
    writeEvent({
      event: "request",
      direction,
      method: allowlistedLabel(message.method, TELEMETRY_METHODS),
      operation:
        message.method === "tools/call"
          ? allowlistedLabel(params?.name, TELEMETRY_OPERATIONS)
          : undefined,
      request_id_sha256: requestIdSha256,
      frame_bytes: frame.length,
      frame_sha256: sha256(frame),
      parameters_bytes: paramsBytes.length,
      parameters_sha256: sha256(paramsBytes),
    });
    return;
  }

  if (direction === "server_to_client") {
    const started = requestIdSha256 === undefined ? undefined : requests.get(requestIdSha256);
    if (requestIdSha256 !== undefined) requests.delete(requestIdSha256);
    writeEvent({
      event: "response",
      direction,
      request_id_sha256: requestIdSha256,
      outcome: Object.hasOwn(message, "error") ? "error" : "success",
      error_code:
        typeof message.error?.code === "number" ? message.error.code : undefined,
      duration_ms:
        started === undefined
          ? undefined
          : Number(process.hrtime.bigint() - started) / 1_000_000,
      frame_bytes: frame.length,
      frame_sha256: sha256(frame),
    });
  }
}

function frameTap(direction) {
  let pending = Buffer.alloc(0);
  return {
    flush() {
      if (pending.length === 0) return;
      writeEvent({
        event: "truncated_frame",
        direction,
        frame_bytes: pending.length,
        frame_sha256: sha256(pending),
      });
      pending = Buffer.alloc(0);
    },
    push(chunk) {
      pending = Buffer.concat([pending, chunk]);
      while (true) {
        const newline = pending.indexOf(0x0a);
        if (newline === -1) break;
        let frame = pending.subarray(0, newline);
        pending = pending.subarray(newline + 1);
        if (frame.at(-1) === 0x0d) frame = frame.subarray(0, -1);
        recordFrame(direction, frame);
      }
      if (pending.length > MAX_FRAME_BYTES) {
        recordFrame(direction, pending);
        pending = Buffer.alloc(0);
      }
    },
  };
}

writeEvent({
  event: "session_start",
  client,
  command_sha256: sha256(JSON.stringify(command)),
  node_version: process.version,
  source_commit: FULL_COMMIT.test(
    process.env.GIS_AI_GO_QUAL_206_SOURCE_COMMIT ?? "",
  )
    ? process.env.GIS_AI_GO_QUAL_206_SOURCE_COMMIT
    : "unknown",
});

const child = spawn(command[0], command.slice(1), {
  env: Object.fromEntries(
    [
      "GIS_AI_GO_QUAL_206_CONFORMANCE",
      "GIS_AI_GO_QUAL_206_SOURCE_COMMIT",
      "LANG",
      "LC_ALL",
      "PATH",
      "TMPDIR",
      "TZ",
    ]
      .filter((name) => process.env[name] !== undefined)
      .map((name) => [name, process.env[name]]),
  ),
  stdio: ["pipe", "pipe", "pipe"],
});
const captureInput = frameTap("client_to_server");
const captureOutput = frameTap("server_to_client");

process.stdin.on("data", (chunk) => {
  captureInput.push(chunk);
  child.stdin.write(chunk);
});
process.stdin.on("end", () => {
  captureInput.flush();
  child.stdin.end();
});
child.stdout.on("data", (chunk) => {
  captureOutput.push(chunk);
  process.stdout.write(chunk);
});
child.stdout.on("end", () => captureOutput.flush());
child.stderr.on("data", (chunk) => {
  const digest = sha256(chunk);
  writeEvent({
    event: "server_stderr",
    bytes: chunk.length,
    sha256: digest,
  });
  process.stderr.write(
    `[qual-206] child stderr bytes=${chunk.length} sha256=${digest}\n`,
  );
});
child.once("error", (error) => {
  writeEvent({ event: "spawn_error", name: error.name });
  closeLog();
  process.exitCode = 1;
});
child.once("close", (code, signal) => {
  captureOutput.flush();
  writeEvent({
    event: "session_end",
    exit_code: code,
    signal: signal ?? undefined,
    pending_request_count: requests.size,
  });
  closeLog();
  process.exitCode = code ?? 1;
});

for (const signal of ["SIGINT", "SIGTERM"]) {
  process.once(signal, () => child.kill(signal));
}
