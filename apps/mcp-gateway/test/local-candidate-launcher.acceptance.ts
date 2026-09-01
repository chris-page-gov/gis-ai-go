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
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import type { Readable } from "node:stream";
import { setTimeout as delay } from "node:timers/promises";
import { fileURLToPath } from "node:url";
import test from "node:test";

type JsonObject = Record<string, unknown>;

const ROOT = fileURLToPath(new URL("../../../../", import.meta.url));
const LOCAL_CANDIDATE_WRAPPER = join(ROOT, "scripts", "start-local-candidate");
const ENDPOINT = new URL("http://127.0.0.1:8787/mcp");
const MAX_CHILD_OUTPUT_BYTES = 1_048_576;

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

function checkoutState(): string {
  return execFileSync(
    "git",
    ["status", "--porcelain=v1", "--untracked-files=all"],
    { cwd: ROOT, encoding: "utf8" },
  );
}

function isolatedChildEnvironment(sandbox: string): {
  readonly childHome: string;
  readonly childTmp: string;
  readonly environment: NodeJS.ProcessEnv;
} {
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

function launcherSearchPath(): string {
  const commandDirectories = ["node", "pnpm", "uv"].map((command) =>
    dirname(execFileSync("/usr/bin/which", [command], { encoding: "utf8" }).trim())
  );
  return [...new Set([...commandDirectories, "/usr/bin", "/bin"])].join(":");
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
  timeoutMilliseconds = 30_000,
): Promise<JsonObject> {
  const deadline = Date.now() + timeoutMilliseconds;
  let lastFailure: unknown;
  while (Date.now() < deadline) {
    if (child.exitCode !== null || child.signalCode !== null) {
      throw new Error("The local candidate launcher stopped before becoming healthy");
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
  throw new Error("The local candidate launcher did not become healthy", {
    cause: lastFailure,
  });
}

test(
  "runs the documented launcher and stops it without changing the checkout",
  { skip: process.platform === "win32", timeout: 60_000 },
  async (t) => {
    const sandbox = mkdtempSync(join(tmpdir(), "gis-ai-go-launcher-acceptance-"));
    chmodSync(sandbox, 0o700);
    const { childHome, childTmp, environment } = isolatedChildEnvironment(sandbox);
    const checkoutBefore = checkoutState();
    const child = spawn(LOCAL_CANDIDATE_WRAPPER, [], {
      cwd: ROOT,
      env: Object.freeze({ ...environment, PATH: launcherSearchPath() }),
      stdio: ["ignore", "pipe", "pipe"],
    });
    assert.ok(child.stdout);
    assert.ok(child.stderr);
    const streamErrors: Error[] = [];
    const stdout = collectBounded(child.stdout, "launcher stdout", streamErrors);
    const stderr = collectBounded(child.stderr, "launcher stderr", streamErrors);
    const childClose = once(child, "close") as Promise<[
      number | null,
      NodeJS.Signals | null,
    ]>;
    let stopped = false;
    t.after(async () => {
      if (!stopped && child.exitCode === null && child.signalCode === null) {
        child.kill("SIGKILL");
        await withTimeout(childClose, "forced launcher cleanup").catch(
          () => undefined,
        );
      }
      rmSync(sandbox, { recursive: true, force: true });
    });

    const health = await waitUntilListening(child);
    assert.equal(health.status, "ok");
    assert.equal(
      readdirSync(childTmp).filter((name) =>
        name.startsWith("gis-ai-go-local-candidate-")
      ).length,
      1,
    );
    const readiness = await getJson("/readyz");
    assert.equal(readiness.status, 200);
    assert.equal(readiness.body.status, "ready");

    child.kill("SIGINT");
    const [code, signal] = await withTimeout(
      childClose,
      "documented launcher shutdown",
    );
    stopped = true;
    assert.equal(code, 0, stderr());
    assert.equal(signal, null);
    assert.deepEqual(streamErrors, []);
    assert.equal(stderr(), "");
    assert.equal(stdout().includes("ELIFECYCLE"), false);
    const lifecycleEvents = stdout()
      .split("\n")
      .filter((line) =>
        line.includes('"schema":"gis-ai-go.local-candidate-lifecycle.v1"')
      )
      .map((line) => JSON.parse(line) as JsonObject);
    assert.deepEqual(
      lifecycleEvents.map(({ event }) => event),
      ["local_candidate_started", "local_candidate_stopped"],
    );
    assert.deepEqual(readdirSync(childHome), []);
    assert.deepEqual(
      readdirSync(childTmp).filter((name) =>
        name.startsWith("gis-ai-go-local-candidate-")
      ),
      [],
    );
    assert.equal(checkoutState(), checkoutBefore);
  },
);
