#!/usr/bin/env node

import assert from "node:assert/strict";
import { execFileSync, spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { EventEmitter, once } from "node:events";
import {
  chmodSync,
  closeSync,
  constants,
  fchmodSync,
  fstatSync,
  fsyncSync,
  lstatSync,
  mkdtempSync,
  openSync,
  readSync,
  realpathSync,
  rmSync,
  writeSync,
} from "node:fs";
import http from "node:http";
import { tmpdir } from "node:os";
import {
  basename,
  dirname,
  isAbsolute,
  join,
  relative,
  resolve,
  sep,
} from "node:path";
import { fileURLToPath } from "node:url";

import { PUBLIC_ONS_DATA_QUERY_PARAMETERS } from
  "../apps/mcp-gateway/dist/src/data-query-application.js";
import {
  MCP_CATALOGUE_RECORD_URI_TEMPLATE,
  MCP_EVIDENCE_RECEIPT_URI_TEMPLATE,
  MCP_PROTOCOL_VERSION,
  MCP_PUBLIC_CATALOGUE_URI,
} from "../apps/mcp-gateway/dist/src/mcp-server.js";

const ROOT = realpathSync(fileURLToPath(new URL("../", import.meta.url)));
const FIXTURE = join(
  ROOT,
  "apps",
  "mcp-gateway",
  "test",
  "fixtures",
  "qual-206-exact-five-http-server.mjs",
);
const PROVIDER_EGRESS_GUARD = join(
  ROOT,
  "tests",
  "interoperability",
  "fixtures",
  "qual_206_provider_egress_guard.mjs",
);
const PRIVATE_CAPTURE_SCHEMA =
  "gis-ai-go.qual-206-local-http-private-capture.v1";
const AUDIT_SCHEMA = "gis-ai-go.qual-206-exact-five-http-audit.v1";
const GUARD_SCHEMA = "gis-ai-go.qual-206-provider-egress-guard.v1";
const ENABLE_FLAG = "GIS_AI_GO_QUAL_206_EXACT_FIVE_HTTP";
const CAPTURE_FLAG = "GIS_AI_GO_QUAL_206_LOCAL_HTTP_CAPTURE";
const PRIVATE_AUDIT_FD_VARIABLE = "GIS_AI_GO_QUAL_206_PRIVATE_AUDIT_FD";
const SOURCE_COMMIT_VARIABLE = "GIS_AI_GO_QUAL_206_SOURCE_COMMIT";
const AUTHORITY_ARGUMENT = "--exact-five-http-conformance-only";
const SCENARIO = "capability-pack";
const FULL_COMMIT = /^[0-9a-f]{40}$/u;
const RECEIPT_ID = /^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/u;
const MAX_HTTP_RESPONSE_BYTES = 1_048_576;
const MAX_OPENAPI_BYTES = 4 * 1_048_576;
const MAX_AUDIT_BYTES = 1_048_576;
const MAX_STDIO_BYTES = 65_536;
const MAX_REQUEST_BYTES = 65_536;
const MAX_SOURCE_MATERIAL_BYTES = 16 * 1_048_576;
const GIT_EXECUTABLE = "/usr/bin/git";
const GIT_CONFIG_ARGUMENTS = Object.freeze([
  "--no-replace-objects",
  "-c",
  "core.fsmonitor=false",
  "-c",
  "core.untrackedCache=false",
]);
const SOURCE_MATERIAL_PATHS = Object.freeze([
  "scripts/qual_206_local_http_preflight.mjs",
  "scripts/qual_206_verify_local_http_preflight.py",
  "schemas/qual-206-exact-five-tool-schema-digests.v1.json",
  "schemas/qual-206-local-http-transport-preflight.schema.json",
  "schemas/qual-206-local-http-private-capture-v1.schema.json",
  "artifacts/okf/manifest.json",
  "artifacts/okf/okf-bundle.json",
  "scripts/qual_206_exact_five_event_collector.mjs",
  "tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs",
  "apps/mcp-gateway/test/fixtures/qual-206-exact-five-http-server.mjs",
  "apps/mcp-gateway/dist/src/mcp-http.js",
  "apps/mcp-gateway/dist/src/mcp-server.js",
]);
const EXPECTED_DERIVED_UNTRACKED_MATERIALS = new Set([
  "artifacts/okf/manifest.json",
  "artifacts/okf/okf-bundle.json",
  "apps/mcp-gateway/dist/src/mcp-http.js",
  "apps/mcp-gateway/dist/src/mcp-server.js",
]);
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
    name: "gis-ai-go-local-http-preflight",
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

function dataQueryRequest(digit) {
  return Object.freeze({
    schema: "gis-ai-go.data-query-request.v1",
    idempotency_key: `gis-ai-go:ik:v1:${digit.repeat(64)}`,
    parameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
  });
}

function withTimeout(promise, label, milliseconds = 10_000) {
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

function gitBytes(argumentsValue, root = ROOT) {
  return execFileSync(GIT_EXECUTABLE, [...GIT_CONFIG_ARGUMENTS, ...argumentsValue], {
    cwd: root,
    env: { LANG: "C", LC_ALL: "C", PATH: "/usr/bin:/bin" },
    maxBuffer: 20 * 1_048_576,
    stdio: ["ignore", "pipe", "pipe"],
    timeout: 10_000,
  });
}

function gitOutput(argumentsValue, root = ROOT) {
  return gitBytes(argumentsValue, root).toString("utf8").trim();
}

function assertCleanIndexState(root) {
  for (const flag of ["-v", "-f"]) {
    const rows = gitBytes(["ls-files", flag, "-z"], root)
      .toString("utf8")
      .split("\0")
      .filter((row) => row.length > 0);
    for (const row of rows) {
      if (!row.startsWith("H ")) {
        throw new Error(
          "A passing clean source must not use assume-unchanged, skip-worktree " +
          "or filesystem-monitor index state",
        );
      }
    }
  }
}

export function localHttpSourceState(repositoryRoot = ROOT) {
  const canonicalRoot = realpathSync(repositoryRoot);
  const root = realpathSync(gitOutput(["rev-parse", "--show-toplevel"], canonicalRoot));
  assert.equal(root, canonicalRoot, "The capture must run from the bound repository root");
  const commit = gitOutput(["rev-parse", "HEAD"], canonicalRoot);
  const tree = gitOutput(["rev-parse", "HEAD^{tree}"], canonicalRoot);
  assert.match(commit, FULL_COMMIT);
  assert.match(tree, FULL_COMMIT);
  const status = gitOutput(
    ["status", "--porcelain=v1", "--untracked-files=all"],
    canonicalRoot,
  );
  if (status === "") assertCleanIndexState(canonicalRoot);
  return Object.freeze({
    repository: "chris-page-gov/gis-ai-go",
    commit,
    tree,
    working_tree_clean: status === "",
  });
}

export function assertLocalHttpSourceMaterialsMatchTree(
  source,
  materials,
  repositoryRoot = ROOT,
) {
  if (source.working_tree_clean !== true) return;
  const canonicalRoot = realpathSync(repositoryRoot);
  for (const material of materials) {
    const entry = gitOutput(
      ["ls-tree", "--full-tree", source.tree, "--", material.path],
      canonicalRoot,
    );
    if (entry === "") {
      assert.equal(
        EXPECTED_DERIVED_UNTRACKED_MATERIALS.has(material.path),
        true,
        `Clean source material ${material.path} is unexpectedly absent from the Git tree`,
      );
      continue;
    }
    const separator = entry.indexOf("\t");
    assert.ok(separator > 0, `Git tree entry for ${material.path} is malformed`);
    const metadata = entry.slice(0, separator).match(
      /^(100644|100755) blob ([0-9a-f]{40})$/u,
    );
    assert.notEqual(metadata, null, `Git tree entry for ${material.path} is not a regular blob`);
    assert.equal(entry.slice(separator + 1), material.path);
    const treeBytes = gitBytes(["cat-file", "blob", metadata[2]], canonicalRoot);
    assert.ok(
      treeBytes.length > 0 && treeBytes.length <= MAX_SOURCE_MATERIAL_BYTES,
      `Git tree blob for ${material.path} is outside its byte bound`,
    );
    assert.equal(
      createHash("sha256").update(treeBytes).digest("hex"),
      material.sha256,
      `Clean source material ${material.path} differs from its recorded Git tree blob`,
    );
  }
}

function isWithin(root, candidate) {
  const remainder = relative(root, candidate);
  return remainder === "" || (
    remainder !== ".." &&
    !remainder.startsWith(`..${sep}`) &&
    !isAbsolute(remainder)
  );
}

function sameFileIdentity(left, right) {
  return left.dev === right.dev &&
    left.ino === right.ino &&
    left.mode === right.mode &&
    left.uid === right.uid &&
    left.gid === right.gid &&
    left.nlink === right.nlink &&
    left.size === right.size &&
    left.mtimeMs === right.mtimeMs &&
    left.ctimeMs === right.ctimeMs;
}

function hashSourceMaterial(root, relativePath) {
  const canonicalRoot = realpathSync(root);
  const lexicalPath = resolve(canonicalRoot, relativePath);
  const canonicalPath = realpathSync(lexicalPath);
  if (
    !isWithin(canonicalRoot, canonicalPath) ||
    lexicalPath !== canonicalPath
  ) {
    throw new Error(`Source material ${relativePath} escaped or traversed a symbolic link`);
  }
  const descriptor = openSync(
    canonicalPath,
    constants.O_RDONLY | (constants.O_NOFOLLOW ?? 0),
  );
  try {
    const openedBefore = fstatSync(descriptor);
    const namedBefore = lstatSync(canonicalPath);
    if (
      !openedBefore.isFile() ||
      !namedBefore.isFile() ||
      namedBefore.isSymbolicLink() ||
      !sameFileIdentity(openedBefore, namedBefore) ||
      openedBefore.size < 1 ||
      openedBefore.size > MAX_SOURCE_MATERIAL_BYTES
    ) {
      throw new Error(`Source material ${relativePath} is not one bounded regular file`);
    }
    const digest = createHash("sha256");
    const buffer = Buffer.allocUnsafe(Math.min(65_536, openedBefore.size));
    let offset = 0;
    while (offset < openedBefore.size) {
      const count = readSync(
        descriptor,
        buffer,
        0,
        Math.min(buffer.length, openedBefore.size - offset),
        offset,
      );
      if (count <= 0) {
        throw new Error(`Source material ${relativePath} read made no progress`);
      }
      digest.update(buffer.subarray(0, count));
      offset += count;
    }
    const openedAfter = fstatSync(descriptor);
    const namedAfter = lstatSync(canonicalPath);
    if (
      !sameFileIdentity(openedBefore, openedAfter) ||
      !sameFileIdentity(openedAfter, namedAfter)
    ) {
      throw new Error(`Source material ${relativePath} changed while it was hashed`);
    }
    return digest.digest("hex");
  } finally {
    closeSync(descriptor);
  }
}

export function snapshotLocalHttpSourceMaterials(
  root = ROOT,
  relativePaths = SOURCE_MATERIAL_PATHS,
) {
  return Object.freeze(relativePaths.map((path) => Object.freeze({
    path,
    sha256: hashSourceMaterial(root, path),
  })));
}

export function bindExecutedLocalHttpSourceMaterials(before, after) {
  assert.equal(before.length, after.length, "The source-material set changed during execution");
  return Object.freeze(before.map((earlier, index) => {
    const later = after[index];
    assert.equal(later?.path, earlier.path, "The source-material order changed during execution");
    assert.equal(
      later.sha256,
      earlier.sha256,
      `Source material ${earlier.path} changed during observed execution`,
    );
    return Object.freeze({
      path: earlier.path,
      sha256_before_execution: earlier.sha256,
      sha256_after_execution: later.sha256,
    });
  }));
}

function exactPrivateOutputPath(value) {
  if (
    typeof value !== "string" ||
    !isAbsolute(value) ||
    resolve(value) !== value ||
    basename(value).length === 0
  ) {
    throw new TypeError("The capture path must be one canonical absolute new file");
  }
  let existing;
  try {
    existing = lstatSync(value);
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
  if (existing !== undefined) {
    if (existing.isSymbolicLink()) {
      let target;
      try {
        target = realpathSync(value);
      } catch {
        throw new TypeError("The capture path must not be a symbolic link");
      }
      if (isWithin(ROOT, target)) {
        throw new TypeError("The private capture must not link into the repository");
      }
    }
    throw new TypeError("The capture path must be one canonical absolute new file");
  }
  const parent = dirname(value);
  const canonicalParent = realpathSync(parent);
  if (canonicalParent !== parent) {
    throw new TypeError("The capture parent must not traverse a symbolic link");
  }
  if (isWithin(ROOT, canonicalParent)) {
    throw new TypeError("The private capture must be outside the repository");
  }
  const parentStat = lstatSync(parent);
  if (
    !parentStat.isDirectory() ||
    parentStat.isSymbolicLink() ||
    parentStat.uid !== process.getuid?.() ||
    (parentStat.mode & 0o777) !== 0o700 ||
    parentStat.nlink < 2
  ) {
    throw new TypeError("The capture parent must be one owner-owned 0700 directory");
  }
  return value;
}

function isolatedChildEnvironment(sourceCommit, temporaryRoot) {
  return {
    [ENABLE_FLAG]: "1",
    [SOURCE_COMMIT_VARIABLE]: sourceCommit,
    [PRIVATE_AUDIT_FD_VARIABLE]: "3",
    CI: "1",
    NO_COLOR: "1",
    TMPDIR: temporaryRoot,
    TMP: temporaryRoot,
    TEMP: temporaryRoot,
    TZ: "Europe/London",
  };
}

function boundedTextCollector(stream, label, maximum) {
  let value = "";
  let failure;
  stream.setEncoding("utf8");
  stream.on("data", (chunk) => {
    value += chunk;
    if (Buffer.byteLength(value, "utf8") > maximum) {
      failure ??= new Error(`${label} exceeded its byte bound`);
      stream.destroy(failure);
    }
  });
  stream.on("error", (error) => {
    failure ??= error;
  });
  return Object.freeze({ failure: () => failure, value: () => value });
}

function auditCollector(stream) {
  const emitter = new EventEmitter();
  const lines = [];
  const events = [];
  let buffer = "";
  let totalBytes = 0;
  let completed = false;
  let failure;
  stream.setEncoding("utf8");
  stream.on("data", (chunk) => {
    totalBytes += Buffer.byteLength(chunk, "utf8");
    if (totalBytes > MAX_AUDIT_BYTES) {
      failure ??= new Error("The private audit stream exceeded its byte bound");
      stream.destroy(failure);
      return;
    }
    buffer += chunk;
    while (buffer.includes("\n")) {
      const index = buffer.indexOf("\n");
      const line = buffer.slice(0, index);
      buffer = buffer.slice(index + 1);
      if (line.length === 0) continue;
      if (Buffer.byteLength(line, "utf8") > MAX_STDIO_BYTES) {
        failure ??= new Error("One private audit event exceeded its byte bound");
        stream.destroy(failure);
        return;
      }
      try {
        const event = JSON.parse(line);
        assert.equal(typeof event, "object");
        assert.notEqual(event, null);
        assert.equal(Array.isArray(event), false);
        lines.push(line);
        events.push(event);
        emitter.emit("event", event);
      } catch (error) {
        failure ??= error;
        stream.destroy(error);
        return;
      }
    }
  });
  stream.once("end", () => {
    completed = true;
    if (buffer.length !== 0) {
      failure ??= new Error("The private audit stream ended mid-frame");
      emitter.emit("failure", failure);
    }
    emitter.emit("ended");
  });
  stream.once("error", (error) => {
    failure ??= error;
    emitter.emit("failure", failure);
  });

  function find(predicate) {
    return events.find(predicate);
  }

  async function waitFor(predicate, label) {
    const existing = find(predicate);
    if (existing !== undefined) return existing;
    if (failure !== undefined) throw failure;
    if (completed) throw new Error(`The private audit stream ended before ${label}`);
    return await withTimeout(new Promise((resolveValue, rejectValue) => {
      const onEvent = (event) => {
        if (!predicate(event)) return;
        emitter.removeListener("failure", onFailure);
        emitter.removeListener("ended", onEnded);
        emitter.removeListener("event", onEvent);
        resolveValue(event);
      };
      const onFailure = (error) => {
        emitter.removeListener("event", onEvent);
        emitter.removeListener("ended", onEnded);
        rejectValue(error);
      };
      const onEnded = () => {
        emitter.removeListener("event", onEvent);
        emitter.removeListener("failure", onFailure);
        rejectValue(new Error(`The private audit stream ended before ${label}`));
      };
      emitter.on("event", onEvent);
      emitter.once("failure", onFailure);
      emitter.once("ended", onEnded);
    }), label);
  }

  return Object.freeze({
    completed: () => completed,
    events: () => [...events],
    failure: () => failure,
    lines: () => [...lines],
    waitFor,
  });
}

function httpRequest({
  port,
  path,
  method,
  headers,
  body = "",
  signal,
  maximum = MAX_HTTP_RESPONSE_BYTES,
}) {
  return new Promise((resolveValue, rejectValue) => {
    const request = http.request({
      host: "127.0.0.1",
      port,
      path,
      method,
      headers: {
        connection: "close",
        ...headers,
      },
      signal,
    });
    request.once("error", rejectValue);
    request.once("response", (response) => {
      const chunks = [];
      let bytes = 0;
      response.on("data", (chunk) => {
        bytes += chunk.length;
        if (bytes > maximum) {
          response.destroy(new Error("The HTTP response exceeded its byte bound"));
          return;
        }
        chunks.push(chunk);
      });
      response.once("error", rejectValue);
      response.once("end", () => {
        const raw = Buffer.concat(chunks, bytes).toString("utf8");
        resolveValue(Object.freeze({
          status: response.statusCode,
          contentType: String(response.headers["content-type"] ?? "")
            .split(";", 1)[0]
            .trim()
            .toLowerCase(),
          raw,
          bytes,
        }));
      });
    });
    request.setTimeout(10_000, () => request.destroy(new Error("HTTP request timed out")));
    request.end(body);
  });
}

function mcpBody(id, method, value = {}) {
  return {
    jsonrpc: "2.0",
    id,
    method,
    params: { _meta: META, ...value },
  };
}

function parseResponse(exchange) {
  assert.equal(exchange.contentType, "application/json");
  const value = JSON.parse(exchange.raw);
  if (exchange.status === 404) {
    assert.equal(value?.error?.code, -32601, exchange.raw);
  } else {
    assert.equal(exchange.status, 200, exchange.raw);
  }
  assert.equal(value.jsonrpc, "2.0");
  return value;
}

function result(message) {
  assert.equal(typeof message.result, "object");
  assert.notEqual(message.result, null);
  return message.result;
}

async function capturedMcpRequest(port, ordinal, requestBody, signal) {
  const requestJson = JSON.stringify(requestBody);
  const requestBytes = Buffer.byteLength(requestJson, "utf8");
  assert.ok(requestBytes > 0 && requestBytes <= MAX_REQUEST_BYTES);
  const name = requestBody.method === "tools/call"
    ? requestBody.params?.name
    : requestBody.method === "resources/read"
      ? requestBody.params?.uri
      : undefined;
  const response = await httpRequest({
    port,
    path: "/mcp",
    method: "POST",
    headers: {
      accept: "application/json, text/event-stream",
      "content-type": "application/json",
      "content-length": String(requestBytes),
      "mcp-protocol-version": MCP_PROTOCOL_VERSION,
      "mcp-method": requestBody.method,
      ...(typeof name === "string" ? { "mcp-name": name } : {}),
    },
    body: requestJson,
    signal,
  });
  return Object.freeze({
    capture: Object.freeze({
      ordinal,
      request_json: requestJson,
      request_bytes: requestBytes,
      response_json: response.raw,
      response_bytes: response.bytes,
      transport_outcome: "response",
    }),
    message: parseResponse(response),
  });
}

function writePrivateCapture(path, capture) {
  const parent = dirname(path);
  const parentBefore = lstatSync(parent);
  if (
    !parentBefore.isDirectory() ||
    parentBefore.isSymbolicLink() ||
    parentBefore.uid !== process.getuid?.() ||
    (parentBefore.mode & 0o777) !== 0o700 ||
    parentBefore.nlink < 2
  ) {
    throw new Error("The private capture parent changed before creation");
  }
  const descriptor = openSync(
    path,
    constants.O_RDWR |
      constants.O_CREAT |
      constants.O_EXCL |
      (constants.O_NOFOLLOW ?? 0),
    0o600,
  );
  try {
    fchmodSync(descriptor, 0o600);
    const opened = fstatSync(descriptor);
    if (
      !opened.isFile() ||
      opened.uid !== process.getuid?.() ||
      opened.nlink !== 1 ||
      (opened.mode & 0o777) !== 0o600
    ) {
      throw new Error("The private capture did not open as one owner-only regular file");
    }
    const raw = Buffer.from(`${JSON.stringify(capture, null, 2)}\n`, "utf8");
    let offset = 0;
    while (offset < raw.length) {
      const written = writeSync(descriptor, raw, offset, raw.length - offset, null);
      if (written <= 0) throw new Error("The private capture write made no progress");
      offset += written;
    }
    fsyncSync(descriptor);
    const finalOpened = fstatSync(descriptor);
    const named = lstatSync(path);
    if (
      !finalOpened.isFile() ||
      !named.isFile() ||
      named.isSymbolicLink() ||
      finalOpened.dev !== named.dev ||
      finalOpened.ino !== named.ino ||
      finalOpened.uid !== process.getuid?.() ||
      finalOpened.nlink !== 1 ||
      (finalOpened.mode & 0o777) !== 0o600 ||
      finalOpened.size !== raw.length
    ) {
      throw new Error("The private capture identity changed before finalisation");
    }
    const digest = createHash("sha256");
    const buffer = Buffer.allocUnsafe(65_536);
    let bytes = 0;
    while (bytes < raw.length) {
      const count = readSync(
        descriptor,
        buffer,
        0,
        Math.min(buffer.length, raw.length - bytes),
        bytes,
      );
      if (count <= 0) throw new Error("The private capture read made no progress");
      digest.update(buffer.subarray(0, count));
      bytes += count;
    }
    if (digest.digest("hex") !== createHash("sha256").update(raw).digest("hex")) {
      throw new Error("The private capture bytes changed during finalisation");
    }
    const parentAfter = lstatSync(parent);
    if (
      parentBefore.dev !== parentAfter.dev ||
      parentBefore.ino !== parentAfter.ino ||
      parentBefore.uid !== parentAfter.uid ||
      parentBefore.mode !== parentAfter.mode
    ) {
      throw new Error("The private capture parent changed during creation");
    }
  } finally {
    closeSync(descriptor);
  }
}

export async function runLocalHttpPreflightCapture(capturePath) {
  const outputPath = exactPrivateOutputPath(capturePath);
  const source = localHttpSourceState();
  const sourceMaterialsBefore = snapshotLocalHttpSourceMaterials();
  assertLocalHttpSourceMaterialsMatchTree(source, sourceMaterialsBefore);
  assert.deepEqual(
    localHttpSourceState(),
    source,
    "The Git source identity changed before observed execution",
  );
  const temporaryRoot = mkdtempSync(join(realpathSync(tmpdir()), "gis-ai-go-http-preflight-"));
  chmodSync(temporaryRoot, 0o700);
  const child = spawn(
    process.execPath,
    [
      "--import",
      PROVIDER_EGRESS_GUARD,
      FIXTURE,
      AUTHORITY_ARGUMENT,
      `--scenario=${SCENARIO}`,
    ],
    {
      cwd: ROOT,
      env: isolatedChildEnvironment(source.commit, temporaryRoot),
      stdio: ["ignore", "pipe", "pipe", "pipe"],
    },
  );
  assert.ok(child.stdout);
  assert.ok(child.stderr);
  assert.ok(child.stdio[3]);
  const stdout = boundedTextCollector(child.stdout, "Fixture stdout", MAX_STDIO_BYTES);
  const stderr = boundedTextCollector(child.stderr, "Fixture stderr", MAX_STDIO_BYTES);
  const audit = auditCollector(child.stdio[3]);
  const close = once(child, "close");
  let childCloseObserved = false;
  void close.then(
    () => { childCloseObserved = true; },
    () => { childCloseObserved = true; },
  );
  const started = new Date().toISOString();
  let captureWritten = false;
  try {
    const listening = await audit.waitFor(
      (event) => event.schema === AUDIT_SCHEMA && event.event === "server-listening",
      "the loopback listener",
    );
    assert.deepEqual(Object.keys(listening).sort(), [
      "event",
      "host",
      "port",
      "production_registration",
      "scenario",
      "schema",
      "source_commit",
      "state",
      "transport",
    ]);
    assert.equal(listening.scenario, SCENARIO);
    assert.equal(listening.source_commit, source.commit);
    assert.equal(listening.transport, "operating-system-loopback-http");
    assert.equal(listening.host, "127.0.0.1");
    assert.ok(Number.isSafeInteger(listening.port));
    assert.equal(listening.state, "candidate-unregistered");
    assert.equal(listening.production_registration, false);
    const port = listening.port;
    const requests = [];

    async function request(ordinal, body) {
      const exchange = await capturedMcpRequest(port, ordinal, body);
      requests.push(exchange.capture);
      return exchange.message;
    }

    const discovered = result(await request(1, mcpBody(1, "server/discover")));
    assert.deepEqual(discovered.supportedVersions, [MCP_PROTOCOL_VERSION]);

    const listed = result(await request(2, mcpBody(2, "tools/list")));
    assert.deepEqual(
      listed.tools.map(({ name }) => name).sort(),
      [...EXACT_OPERATIONS].sort(),
    );

    const resourceList = result(await request(3, mcpBody(3, "resources/list")));
    assert.deepEqual(resourceList.resources.map(({ uri }) => uri), [MCP_PUBLIC_CATALOGUE_URI]);
    const templates = result(await request(
      4,
      mcpBody(4, "resources/templates/list"),
    ));
    assert.deepEqual(
      templates.resourceTemplates.map(({ uriTemplate }) => uriTemplate),
      [MCP_CATALOGUE_RECORD_URI_TEMPLATE, MCP_EVIDENCE_RECEIPT_URI_TEMPLATE],
    );

    await request(5, mcpBody(5, "resources/read", { uri: MCP_PUBLIC_CATALOGUE_URI }));
    const recordUri = "gis-ai-go://catalogue/records/LR-Q003";
    await request(6, mcpBody(6, "resources/read", { uri: recordUri }));

    const calls = [
      ["catalogue.search", { query: "INSPIRE", limit: 1 }],
      ["catalogue.describe", { record_id: "LR-Q003" }],
      ["selection.resolve", SELECTION_REQUEST],
      ["data.query", dataQueryRequest("9")],
    ];
    let searchReceipt;
    for (const [offset, [operation, argumentsValue]] of calls.entries()) {
      const message = await request(
        7 + offset,
        mcpBody(10 + offset, "tools/call", { name: operation, arguments: argumentsValue }),
      );
      const structured = result(message).structuredContent;
      if (operation === "catalogue.search") {
        searchReceipt = structured?.evidence_receipt?.receipt_id;
        assert.match(searchReceipt, RECEIPT_ID);
      }
    }
    assert.match(searchReceipt, RECEIPT_ID);
    const inspection = await request(
      11,
      mcpBody(14, "tools/call", {
        name: "evidence.inspect",
        arguments: { receipt_id: searchReceipt },
      }),
    );
    assert.equal(
      result(inspection).structuredContent?.data?.record?.receipt?.receipt_id,
      searchReceipt,
    );
    await request(
      12,
      mcpBody(15, "resources/read", {
        uri: `gis-ai-go://evidence/receipts/${encodeURIComponent(searchReceipt)}`,
      }),
    );

    const openapiResponse = await httpRequest({
      port,
      path: "/openapi.json",
      method: "GET",
      headers: { accept: "application/json", host: "127.0.0.1" },
      maximum: MAX_OPENAPI_BYTES,
    });
    assert.equal(openapiResponse.status, 200);
    assert.equal(openapiResponse.contentType, "application/json");
    JSON.parse(openapiResponse.raw);
    const readinessResponse = await httpRequest({
      port,
      path: "/readyz",
      method: "GET",
      headers: { accept: "application/json", host: "127.0.0.1" },
      maximum: MAX_STDIO_BYTES,
    });
    assert.equal(readinessResponse.status, 200);
    assert.equal(readinessResponse.contentType, "application/json");
    const readiness = JSON.parse(readinessResponse.raw);
    assert.equal(readiness.production_registration, false);
    assert.deepEqual([...readiness.active_tools].sort(), [...EXACT_OPERATIONS].sort());
    assert.deepEqual(
      [...readiness.active_api_operations].sort(),
      [...EXACT_OPERATIONS].sort(),
    );

    const cancellationBody = mcpBody(20, "tools/call", {
      name: "data.query",
      arguments: dataQueryRequest("8"),
    });
    const cancellationJson = JSON.stringify(cancellationBody);
    const cancellationBytes = Buffer.byteLength(cancellationJson, "utf8");
    const controller = new AbortController();
    const pendingCancellation = capturedMcpRequest(
      port,
      13,
      cancellationBody,
      controller.signal,
    );
    await audit.waitFor(
      (event) =>
        event.schema === AUDIT_SCHEMA &&
        event.event === "provider-transport-started" &&
        event.scenario === SCENARIO &&
        event.ordinal === 2,
      "the second deterministic provider transport",
    );
    controller.abort();
    await assert.rejects(pendingCancellation, (error) => error?.name === "AbortError");
    requests.push(Object.freeze({
      ordinal: 13,
      request_json: cancellationJson,
      request_bytes: cancellationBytes,
      response_json: null,
      response_bytes: 0,
      transport_outcome: "client-aborted",
    }));
    await audit.waitFor(
      (event) =>
        event.schema === AUDIT_SCHEMA &&
        event.event === "provider-transport-aborted" &&
        event.scenario === SCENARIO &&
        event.ordinal === 2,
      "the deterministic provider abort",
    );

    const unsupported = await request(14, mcpBody(21, "prompts/list"));
    assert.equal(unsupported.error?.code, -32601);
    assert.equal(unsupported.error?.message, "Method not found");
    assert.deepEqual(requests.map(({ ordinal }) => ordinal),
      Array.from({ length: 14 }, (_value, index) => index + 1));

    child.kill("SIGTERM");
    const [code, signal] = await withTimeout(close, "the HTTP fixture to close");
    assert.equal(code, 0);
    assert.equal(signal, null);
    assert.equal(audit.failure(), undefined);
    assert.equal(audit.completed(), true);
    assert.equal(stdout.failure(), undefined);
    assert.equal(stderr.failure(), undefined);
    assert.equal(stdout.value(), "");
    assert.equal(stderr.value(), "");

    const summary = audit.events().find(
      (event) => event.schema === AUDIT_SCHEMA && event.event === "session-summary",
    );
    assert.notEqual(summary, undefined);
    assert.deepEqual(summary.operations, EXACT_OPERATIONS);
    assert.deepEqual(summary.resources, EXACT_RESOURCES);
    assert.deepEqual(summary.suspensions, []);
    assert.equal(summary.provider_transport_calls, 2);
    assert.equal(summary.aborted_provider_calls, 1);
    assert.equal(summary.ledger_event_count, 4);
    assert.equal(summary.reported_error_count, 0);
    assert.equal(summary.guarded_api_invocation_count, 0);
    const guardSummary = audit.events().find(
      (event) => event.schema === GUARD_SCHEMA && event.event === "provider-egress-guard-summary",
    );
    assert.equal(guardSummary?.guarded_api_invocation_count, 0);
    const sourceMaterialsAfter = snapshotLocalHttpSourceMaterials();
    assertLocalHttpSourceMaterialsMatchTree(source, sourceMaterialsAfter);
    const sourceMaterials = bindExecutedLocalHttpSourceMaterials(
      sourceMaterialsBefore,
      sourceMaterialsAfter,
    );
    assert.deepEqual(
      localHttpSourceState(),
      source,
      "The Git source identity changed during observed execution",
    );

    const capture = Object.freeze({
      schema: PRIVATE_CAPTURE_SCHEMA,
      observed_at: Object.freeze({ started, completed: new Date().toISOString() }),
      source,
      source_materials: sourceMaterials,
      runtime: Object.freeze({
        node_version: process.version,
        mcp_server_version: "2.0.0",
      }),
      fixture: Object.freeze({
        scenario: SCENARIO,
        transport: listening.transport,
        host: listening.host,
        port,
        state: listening.state,
        production_registration: listening.production_registration,
      }),
      requests: Object.freeze(requests),
      openapi: Object.freeze({
        http_status: openapiResponse.status,
        content_type: openapiResponse.contentType,
        response_bytes: openapiResponse.bytes,
        response_json: openapiResponse.raw,
      }),
      readiness: Object.freeze({
        http_status: readinessResponse.status,
        content_type: readinessResponse.contentType,
        response_bytes: readinessResponse.bytes,
        response_json: readinessResponse.raw,
      }),
      audit_lines: Object.freeze(audit.lines()),
      child: Object.freeze({
        exit_code: code,
        signal,
        stdout: stdout.value(),
        stderr: stderr.value(),
        audit_stream_complete: audit.completed(),
      }),
    });
    writePrivateCapture(outputPath, capture);
    captureWritten = true;
    return capture;
  } finally {
    if (!childCloseObserved) {
      if (child.exitCode === null && child.signalCode === null) child.kill("SIGTERM");
      try {
        await withTimeout(close, "failed fixture TERM teardown", 1_000);
      } catch {
        if (child.exitCode === null && child.signalCode === null) child.kill("SIGKILL");
        await withTimeout(close, "failed fixture KILL teardown", 2_000);
      }
    }
    rmSync(temporaryRoot, { recursive: true, force: true });
    if (!captureWritten) {
      // Exclusive creation occurs only after every check, so a failed run leaves no partial file.
    }
  }
}

function parseArguments(argv, environment = process.env) {
  if (environment[CAPTURE_FLAG] !== "1") {
    throw new Error(`Refusing private capture without ${CAPTURE_FLAG}=1`);
  }
  if (argv.length !== 2 || argv[0] !== "--capture") {
    throw new Error("Usage: --capture ABSOLUTE_NEW_OWNER_ONLY_JSON");
  }
  return Object.freeze({ capturePath: exactPrivateOutputPath(argv[1]) });
}

const invokedPath = process.argv[1] === undefined ? "" : resolve(process.argv[1]);
if (invokedPath === fileURLToPath(import.meta.url)) {
  try {
    const options = parseArguments(process.argv.slice(2));
    await runLocalHttpPreflightCapture(options.capturePath);
    process.stdout.write("QUAL-206 private local HTTP capture completed.\n");
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    process.stderr.write(`QUAL-206 local HTTP capture failed: ${message}\n`);
    process.exitCode = 1;
  }
}
