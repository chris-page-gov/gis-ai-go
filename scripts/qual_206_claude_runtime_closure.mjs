import { createHash } from "node:crypto";
import {
  closeSync,
  fstatSync,
  lstatSync,
  openSync,
  readSync,
  readlinkSync,
  realpathSync,
  readdirSync,
} from "node:fs";
import { isAbsolute, join, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = realpathSync(fileURLToPath(new URL("../", import.meta.url)));
const MAX_DEPTH = 32;
const MAX_VALUES = 20_000;
const MAX_FILE_BYTES = 536_870_912;
const MAX_CLOSURE_BYTES = 536_870_912;
const MAX_CLOSURE_FILES = 4_096;
const MAX_DEPENDENCY_BYTES = 1_073_741_824;
const MAX_DEPENDENCY_FILES = 20_000;
const NUMBER = /-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/uy;
const HEX = /^[0-9A-Fa-f]{4}$/u;
const DOMAIN_PREFIX = "GIS-AI-GO\0canonical-json\0sha256\0v1\0";
const CLOSURE_DOMAIN = "gis-ai-go.qual-206-claude-runtime-closure.v1";
const DEPENDENCY_DOMAIN = "gis-ai-go.qual-206-claude-dependency-closure.v1";

export const GENERATED_RUNTIME_ROOTS = Object.freeze([
  "apps/mcp-gateway/dist",
  "artifacts/okf",
  "packages/authority-context/dist",
  "packages/contracts/dist",
  "packages/evidence/dist",
  "packages/policy-client/dist",
  "packages/provider-adapter-sdk/dist",
  "packages/tool-registry/dist",
]);

export const TRACKED_CAPABILITY_MATERIALS = Object.freeze([
  "package.json",
  "pnpm-lock.yaml",
  "schemas/qual-206-claude-capability-evidence-v1.schema.json",
  "schemas/qual-206-claude-capability-private-run-v1.schema.json",
  "schemas/qual-206-claude-capability-session-v1.schema.json",
  "schemas/qual-206-claude-composite-host-event-capture-v1.schema.json",
  "schemas/qual-206-claude-composite-host-event-v1.schema.json",
  "scripts/qual_206_claude_capability_harness.mjs",
  "scripts/qual_206_claude_runtime_closure.mjs",
  "scripts/qual_206_claude_stdio_observer.mjs",
  "scripts/qual_206_exact_five_event_collector.mjs",
  "scripts/verify_qual_206_claude_capability.py",
  "scripts/verify_qual_206_claude_composite_observation.py",
  "tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs",
  "tests/interoperability/fixtures/qual_206_strict_modern_event_server.mjs",
  "tests/interoperability/qual_206_cases.json",
]);

export const TRACKED_EXACT_FIVE_CAPABILITY_MATERIALS = Object.freeze([
  "package.json",
  "pnpm-lock.yaml",
  "schemas/qual-206-claude-exact-five-capability-evidence-v1.schema.json",
  "schemas/qual-206-claude-exact-five-capability-private-run-v1.schema.json",
  "schemas/qual-206-claude-exact-five-capability-session-v1.schema.json",
  "schemas/qual-206-claude-composite-host-event-capture-v1.schema.json",
  "schemas/qual-206-claude-composite-host-event-v1.schema.json",
  "scripts/qual_206_claude_capability_harness.mjs",
  "scripts/qual_206_claude_exact_five_capability_harness.mjs",
  "scripts/qual_206_claude_runtime_closure.mjs",
  "scripts/qual_206_claude_stdio_observer.mjs",
  "scripts/qual_206_exact_five_event_collector.mjs",
  "scripts/verify_qual_206_claude_exact_five_capability.py",
  "scripts/verify_qual_206_claude_exact_five_results.mjs",
  "scripts/verify_qual_206_claude_composite_observation.py",
  "tests/interoperability/fixtures/qual_206_claude_exact_five_profile.v1.json",
  "tests/interoperability/fixtures/qual_206_provider_egress_guard.mjs",
  "tests/interoperability/fixtures/qual_206_strict_modern_event_server.mjs",
]);

export const INSTALLED_DEPENDENCY_ROOTS = Object.freeze([
  "node_modules",
  "apps/mcp-gateway/node_modules",
  "apps/public-explorer/node_modules",
  "packages/authority-context/node_modules",
  "packages/policy-client/node_modules",
  "packages/provider-adapter-sdk/node_modules",
]);

export const WORKSPACE_DEPENDENCY_TARGETS = Object.freeze([
  "apps/mcp-gateway",
  "apps/public-explorer",
  "packages/authority-context",
  "packages/contracts",
  "packages/evidence",
  "packages/policy-client",
  "packages/provider-adapter-sdk",
  "packages/tool-registry",
]);

function fail(message) {
  throw new Error(message);
}

function assertPairedSurrogates(value) {
  for (let index = 0; index < value.length; index += 1) {
    const codeUnit = value.charCodeAt(index);
    if (codeUnit >= 0xd800 && codeUnit <= 0xdbff) {
      const next = value.charCodeAt(index + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) fail("invalid JSON string");
      index += 1;
    } else if (codeUnit >= 0xdc00 && codeUnit <= 0xdfff) {
      fail("invalid JSON string");
    }
  }
}

function canonicalValue(value, ancestors) {
  if (value === null) return "null";
  if (typeof value === "boolean") return value ? "true" : "false";
  if (typeof value === "number") {
    if (!Number.isFinite(value)) fail("invalid canonical JSON number");
    return JSON.stringify(value);
  }
  if (typeof value === "string") {
    assertPairedSurrogates(value);
    return JSON.stringify(value);
  }
  if (typeof value !== "object") fail("unsupported canonical JSON value");
  if (ancestors.has(value)) fail("cyclic canonical JSON value");
  ancestors.add(value);
  try {
    if (Array.isArray(value)) {
      if (Object.keys(value).length !== value.length) fail("sparse canonical JSON array");
      return `[${value.map((item) => canonicalValue(item, ancestors)).join(",")}]`;
    }
    const prototype = Object.getPrototypeOf(value);
    if (prototype !== Object.prototype && prototype !== null) {
      fail("non-plain canonical JSON object");
    }
    const keys = Reflect.ownKeys(value);
    if (keys.some((key) => typeof key !== "string")) {
      fail("symbol canonical JSON property");
    }
    return `{${keys.sort().map((key) => {
      const descriptor = Object.getOwnPropertyDescriptor(value, key);
      if (descriptor === undefined || !("value" in descriptor) || !descriptor.enumerable) {
        fail("unsafe canonical JSON property");
      }
      assertPairedSurrogates(key);
      return `${JSON.stringify(key)}:${canonicalValue(descriptor.value, ancestors)}`;
    }).join(",")}}`;
  } finally {
    ancestors.delete(value);
  }
}

export function canonicalJson(value) {
  return canonicalValue(value, new WeakSet());
}

export function parseStrictJson(text) {
  let index = 0;
  let values = 0;
  function whitespace() {
    while (index < text.length && /[\u0009\u000a\u000d\u0020]/u.test(text[index])) {
      index += 1;
    }
  }
  function stringValue() {
    if (text[index] !== '"') fail("invalid strict JSON");
    const start = index;
    index += 1;
    while (index < text.length) {
      const code = text.charCodeAt(index);
      if (code === 0x22) {
        index += 1;
        try {
          const parsed = JSON.parse(text.slice(start, index));
          assertPairedSurrogates(parsed);
          return parsed;
        } catch {
          fail("invalid strict JSON");
        }
      }
      if (code < 0x20) fail("invalid strict JSON");
      if (code === 0x5c) {
        index += 1;
        const escape = text[index];
        if (escape === undefined || !'"\\/bfnrtu'.includes(escape)) {
          fail("invalid strict JSON");
        }
        if (escape === "u") {
          const digits = text.slice(index + 1, index + 5);
          if (!HEX.test(digits)) fail("invalid strict JSON");
          index += 4;
        }
      }
      index += 1;
    }
    fail("invalid strict JSON");
  }
  function value(depth) {
    if (depth > MAX_DEPTH || ++values > MAX_VALUES) fail("invalid strict JSON");
    whitespace();
    const first = text[index];
    if (first === '"') return stringValue();
    if (first === "{") {
      index += 1;
      whitespace();
      const result = Object.create(null);
      const keys = new Set();
      if (text[index] === "}") {
        index += 1;
        return result;
      }
      while (true) {
        whitespace();
        const key = stringValue();
        if (keys.has(key)) fail("invalid strict JSON");
        keys.add(key);
        whitespace();
        if (text[index] !== ":") fail("invalid strict JSON");
        index += 1;
        result[key] = value(depth + 1);
        whitespace();
        if (text[index] === "}") {
          index += 1;
          return result;
        }
        if (text[index] !== ",") fail("invalid strict JSON");
        index += 1;
      }
    }
    if (first === "[") {
      index += 1;
      whitespace();
      const result = [];
      if (text[index] === "]") {
        index += 1;
        return result;
      }
      while (true) {
        result.push(value(depth + 1));
        whitespace();
        if (text[index] === "]") {
          index += 1;
          return result;
        }
        if (text[index] !== ",") fail("invalid strict JSON");
        index += 1;
      }
    }
    for (const [literal, parsed] of [
      ["true", true],
      ["false", false],
      ["null", null],
    ]) {
      if (text.startsWith(literal, index)) {
        index += literal.length;
        return parsed;
      }
    }
    NUMBER.lastIndex = index;
    const match = NUMBER.exec(text);
    if (match === null) fail("invalid strict JSON");
    index = NUMBER.lastIndex;
    const parsed = Number(match[0]);
    if (!Number.isFinite(parsed) || (Number.isInteger(parsed) && !Number.isSafeInteger(parsed))) {
      fail("invalid strict JSON");
    }
    return Object.is(parsed, -0) ? 0 : parsed;
  }
  const parsed = value(0);
  whitespace();
  if (index !== text.length) fail("invalid strict JSON");
  return parsed;
}

export function hashStableRegularFile(
  path,
  label,
  maximum = MAX_FILE_BYTES,
  requireSingleLink = true,
) {
  if (realpathSync(path) !== path) fail(`${label} must not traverse an alias`);
  const before = lstatSync(path);
  if (
    !before.isFile() || before.isSymbolicLink() ||
    (requireSingleLink && before.nlink !== 1) || before.size > maximum
  ) {
    fail(`${label} must be one bounded singly linked regular file`);
  }
  const descriptor = openSync(path, "r");
  try {
    const opened = fstatSync(descriptor);
    if (opened.dev !== before.dev || opened.ino !== before.ino) {
      fail(`${label} changed before opening`);
    }
    const digest = createHash("sha256");
    const buffer = Buffer.allocUnsafe(65_536);
    let bytes = 0;
    while (true) {
      const count = readSync(descriptor, buffer, 0, buffer.length, null);
      if (count === 0) break;
      bytes += count;
      if (bytes > maximum) fail(`${label} exceeded its byte boundary`);
      digest.update(buffer.subarray(0, count));
    }
    const after = fstatSync(descriptor);
    if (
      after.dev !== before.dev || after.ino !== before.ino ||
      after.size !== before.size || after.mtimeMs !== before.mtimeMs || bytes !== before.size
    ) {
      fail(`${label} changed while hashing`);
    }
    return Object.freeze({ bytes, sha256: digest.digest("hex") });
  } finally {
    closeSync(descriptor);
  }
}

function generatedFiles(root) {
  const files = [];
  function visit(path, depth) {
    if (depth > MAX_DEPTH) fail("generated runtime closure is too deeply nested");
    const state = lstatSync(path);
    if (!state.isDirectory() || state.isSymbolicLink() || realpathSync(path) !== path) {
      fail("generated runtime root must be one real directory");
    }
    for (const entry of readdirSync(path, { withFileTypes: true })
      .sort((left, right) => left.name < right.name ? -1 : left.name > right.name ? 1 : 0)) {
      const child = join(path, entry.name);
      if (entry.isDirectory()) visit(child, depth + 1);
      else if (entry.isFile()) {
        if (files.length >= MAX_CLOSURE_FILES) {
          fail("generated runtime has too many files");
        }
        files.push(child);
      }
      else fail("generated runtime closure contains a link or special file");
    }
  }
  for (const name of GENERATED_RUNTIME_ROOTS) visit(join(root, name), 0);
  return files;
}

export function measureGeneratedRuntimeClosure(root = ROOT) {
  const canonicalRoot = realpathSync(root);
  if (canonicalRoot !== root) fail("runtime root must be canonical");
  const identities = new Set();
  const entries = [];
  let bytes = 0;
  for (const path of generatedFiles(root)) {
    const state = lstatSync(path);
    const identity = `${state.dev}:${state.ino}`;
    if (identities.has(identity) || state.nlink !== 1) {
      fail("generated runtime file must be singly linked and unique");
    }
    identities.add(identity);
    const measured = hashStableRegularFile(path, "generated runtime file");
    bytes += measured.bytes;
    if (!Number.isSafeInteger(bytes) || bytes > MAX_CLOSURE_BYTES) {
      fail("generated runtime closure exceeds its byte boundary");
    }
    entries.push({
      bytes: measured.bytes,
      path: relative(root, path).split(sep).join("/"),
      sha256: measured.sha256,
    });
  }
  const digest = createHash("sha256")
    .update(DOMAIN_PREFIX, "utf8")
    .update(CLOSURE_DOMAIN, "utf8")
    .update("\0", "utf8")
    .update(canonicalJson(entries), "utf8")
    .digest("hex");
  return Object.freeze({ bytes, file_count: entries.length, manifest_sha256: digest });
}

export function dependencyLinkTargetAllowed(root, resolvedTarget) {
  if (!isAbsolute(root) || !isAbsolute(resolvedTarget)) return false;
  const dependencyRoots = INSTALLED_DEPENDENCY_ROOTS.map((name) => join(root, name));
  if (dependencyRoots.some(
    (dependencyRoot) =>
      resolvedTarget === dependencyRoot || resolvedTarget.startsWith(`${dependencyRoot}${sep}`),
  )) {
    return true;
  }
  return WORKSPACE_DEPENDENCY_TARGETS.some(
    (workspaceTarget) => resolvedTarget === join(root, workspaceTarget),
  );
}

export function measureInstalledDependencyClosure(root = ROOT) {
  if (realpathSync(root) !== root) fail("dependency runtime root must be canonical");
  const entries = [];
  const identities = new Set();
  let bytes = 0;
  function visit(path, depth) {
    if (depth > MAX_DEPTH) fail("installed dependency closure is too deeply nested");
    const state = lstatSync(path);
    const relativePath = relative(root, path).split(sep).join("/");
    if (state.isSymbolicLink()) {
      const target = readlinkSync(path, "utf8");
      const resolved = realpathSync(path);
      const after = lstatSync(path);
      if (
        isAbsolute(target) || target.includes("\0") ||
        (resolved !== root && !resolved.startsWith(`${root}${sep}`)) ||
        !dependencyLinkTargetAllowed(root, resolved) ||
        after.dev !== state.dev || after.ino !== state.ino ||
        after.mtimeMs !== state.mtimeMs || readlinkSync(path, "utf8") !== target
      ) {
        fail("installed dependency closure contains an unsafe link target");
      }
      entries.push({ kind: "symlink", path: relativePath, target });
    } else if (state.isDirectory()) {
      for (const entry of readdirSync(path, { withFileTypes: true })
        .sort((left, right) => left.name < right.name ? -1 : left.name > right.name ? 1 : 0)) {
        visit(join(path, entry.name), depth + 1);
      }
    } else if (state.isFile()) {
      const identity = `${state.dev}:${state.ino}`;
      if (state.nlink !== 1 || identities.has(identity)) {
        fail("installed dependency file must be singly linked and unique");
      }
      identities.add(identity);
      const measured = hashStableRegularFile(
        path,
        "installed dependency file",
        MAX_FILE_BYTES,
      );
      bytes += measured.bytes;
      if (!Number.isSafeInteger(bytes) || bytes > MAX_DEPENDENCY_BYTES) {
        fail("installed dependency closure exceeds its byte boundary");
      }
      entries.push({ kind: "file", path: relativePath, ...measured });
    } else {
      fail("installed dependency closure contains a special file");
    }
    if (entries.length > MAX_DEPENDENCY_FILES) {
      fail("installed dependency closure has too many entries");
    }
  }
  for (const name of INSTALLED_DEPENDENCY_ROOTS) visit(join(root, name), 0);
  const digest = createHash("sha256")
    .update(DOMAIN_PREFIX, "utf8")
    .update(DEPENDENCY_DOMAIN, "utf8")
    .update("\0", "utf8")
    .update(canonicalJson(entries), "utf8")
    .digest("hex");
  return Object.freeze({ bytes, entry_count: entries.length, manifest_sha256: digest });
}
