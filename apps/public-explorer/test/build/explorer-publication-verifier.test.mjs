import assert from "node:assert/strict";
import { once } from "node:events";
import http from "node:http";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import test from "node:test";
import {
  APP, LIMITS, deploymentBudget, hash, ledger, parseLedger, readVerified, runBounded, safePath, settings, waitForPublication,
} from "../browser/verify-explorer-publication.mjs";

test("paths remain local and ledger rows are exact, unique and byte-sorted", () => {
  const a = { path: "explorer/a file.js", bytes: 1, sha256: hash("a") };
  const b = { path: "gis/explorer/records/00000.json", bytes: 1, sha256: hash("b") };
  assert.deepEqual(parseLedger(Buffer.from(ledger([a, b]))), [
    { path: a.path, sha256: a.sha256 }, { path: b.path, sha256: b.sha256 },
  ]);
  for (const value of ["/absolute", "../escape", "a/../b", "a//b", "a/./b", "a\\b", "a\0b", "a\nb", "a\rb", "a\tb", "a\u007fb"]) {
    assert.throws(() => safePath(value), /unsafe publication path/u);
  }
  for (const rows of [[a, a], [b, a]]) {
    assert.throws(() => parseLedger(Buffer.from(ledger(rows))), /unique and sorted/u);
  }
  assert.throws(() => parseLedger(Buffer.from(ledger([a]).trimEnd())), /newline/u);
  assert.throws(() => parseLedger(Buffer.from(hash("") + "  .nojekyll\n")), /excluded/u);
  assert.throws(() => parseLedger(Buffer.from(hash("") + "  publication/CHECKSUMS.sha256\n")), /excluded/u);
});

test("the complete member budget includes the control file and all five publication files", () => {
  assert.deepEqual(deploymentBudget(49_995, 999_999_999), {
    archiveFiles: 50_000, fetchedFiles: 49_999, totalBytes: 999_999_999,
  });
  assert.throws(() => deploymentBudget(49_996, 999_999_999), /file ceiling/u);
  assert.throws(() => deploymentBudget(49_995, 1_000_000_000), /byte limit/u);
  const rows = Array.from({ length: 49_999 }, (_, index) => ({
    path: String(index).padStart(5, "0"), sha256: "a".repeat(64),
  }));
  assert.throws(() => parseLedger(Buffer.from(ledger(rows))), /file limit/u);
});

test("external expected identities require the real publication prefix and safe origin", () => {
  const env = {
    PUBLIC_BASE_URL: "http://127.0.0.1:8131/gis-ai-go/",
    EXPECTED_SOURCE_COMMIT: "a".repeat(40),
    EXPECTED_VERSION: "0.1.0",
    EXPECTED_ARCHIVE_SHA256: "b".repeat(64),
    EXPECTED_OKF_CONTENT_ROOT: "c".repeat(64),
    EXPECTED_PAYLOAD_ROOT: "d".repeat(64),
    EXPECTED_PUBLIC_CHECKSUMS_SHA256: "e".repeat(64),
  };
  assert.equal(settings(env).mode, "loopback-candidate");
  assert.equal(settings({ ...env, EXPECTED_VERSION: "1.2.3-rc.1+build.2" }).version, "1.2.3-rc.1+build.2");
  assert.equal(settings({ ...env, PUBLIC_BASE_URL: "https://chris-page-gov.github.io/gis-ai-go/" }).mode, "deployed-publication");
  for (const address of [
    "http://example.test/gis-ai-go/", "https://example.test/", "https://user:password@example.test/gis-ai-go/",
    "https://example.test/gis-ai-go/", "https://example.test/gis-ai-go/?q=x", "https://example.test/gis-ai-go/#record=x",
  ]) assert.throws(() => settings({ ...env, PUBLIC_BASE_URL: address }));
  assert.throws(() => settings({ ...env, EXPECTED_SOURCE_COMMIT: "main" }), /SOURCE_COMMIT/u);
  assert.throws(() => settings({ ...env, EXPECTED_PAYLOAD_ROOT: "no digest" }), /PAYLOAD_ROOT/u);
  assert.equal(APP.treeSha256, "d127aadb96a77711d5f7cc7aec8cf731cbf5ec1e3d49304d8132189ea4991f93");
});

test("bounded workers verify every item once and honour the concurrency ceiling", async () => {
  const seen = [];
  let active = 0;
  let peak = 0;
  await runBounded(Array.from({ length: 29 }, (_, index) => index), async item => {
    active += 1;
    peak = Math.max(peak, active);
    await new Promise(resolve => setTimeout(resolve, 2));
    seen.push(item);
    active -= 1;
  }, { concurrency: 3 });
  assert.equal(peak, 3);
  assert.deepEqual(seen.sort((a, b) => a - b), Array.from({ length: 29 }, (_, index) => index));
  await assert.rejects(runBounded([1], async () => {}, { concurrency: LIMITS.concurrency + 1 }), /concurrency/u);
});

test("public readiness waits for the exact accepted identity within its fixed attempt bound", async () => {
  const expected = {
    baseUrl: new URL("https://chris-page-gov.github.io/gis-ai-go/"),
    sourceCommit: "a".repeat(40), version: "0.1.0", payloadRoot: "b".repeat(64), okfRoot: "c".repeat(64),
  };
  const receipt = {
    schema: "gis-ai-go.pages-site-receipt.v2",
    repository: "chris-page-gov/gis-ai-go",
    canonicalUrl: expected.baseUrl.href, basePath: "/gis-ai-go/",
    sourceCommit: expected.sourceCommit, version: expected.version,
    payloadRootSha256: expected.payloadRoot, okfContentRootSha256: expected.okfRoot,
    app: APP,
  };
  let requests = 0;
  const observed = await waitForPublication(expected, {
    deadlineMs: 1000, attemptLimit: 3, pauseMs: 0,
    fetcher: async (url, options) => {
      assert.equal(new URL(url).searchParams.get("source"), expected.sourceCommit);
      assert.equal(options.redirect, "error");
      requests += 1;
      return new Response(JSON.stringify(requests === 1 ? { ...receipt, sourceCommit: "d".repeat(40) } : receipt));
    },
  });
  assert.equal(observed.status, "ready");
  assert.equal(observed.attempts, 2);
  assert.equal(requests, 2);
  let mismatches = 0;
  await assert.rejects(waitForPublication(expected, {
    deadlineMs: 1000, attemptLimit: 3, pauseMs: 0,
    fetcher: async () => { mismatches += 1; return new Response(JSON.stringify({ ...receipt, payloadRootSha256: "e".repeat(64) })); },
  }), /readiness did not pass/u);
  assert.equal(mismatches, 3);
});

test("one worker failure aborts in-flight work and prevents further scheduling", async () => {
  const controller = new AbortController();
  const started = [];
  await assert.rejects(runBounded([0, 1, 2, 3, 4, 5], async (item, signal) => {
    started.push(item);
    if (item === 1) throw Error("tampered source");
    await new Promise((resolve, reject) => {
      if (signal.aborted) { reject(signal.reason); return; }
      signal.addEventListener("abort", () => reject(signal.reason), { once: true });
    });
  }, { concurrency: 2, controller }), /tampered source/u);
  assert.equal(controller.signal.aborted, true);
  assert.deepEqual(started, [0, 1]);
});

test("streaming transport checks each byte, digest, response and hard size ceiling", async () => {
  const chunks = [Buffer.from("complete "), Buffer.from("public "), Buffer.from("bytes")];
  const bytes = Buffer.concat(chunks);
  let accounted = 0;
  const fetcher = async (_url, options) => {
    assert.equal(options.redirect, "error");
    assert.equal(options.credentials, "omit");
    assert.equal(options.cache, "no-store");
    return new Response(new ReadableStream({
      start(controller) {
        for (const chunk of chunks) controller.enqueue(chunk);
        controller.close();
      },
    }));
  };
  const observed = await readVerified("https://example.test/file", {
    fetcher, maximum: 100, expectedBytes: bytes.length, expectedSha256: hash(bytes), retain: true,
    account: size => { accounted += size; },
  });
  assert.deepEqual(observed.value, bytes);
  assert.equal(accounted, bytes.length);
  await assert.rejects(readVerified("https://example.test/file", {
    fetcher, maximum: bytes.length - 1, expectedSha256: hash(bytes),
  }), /byte limit/u);
  await assert.rejects(readVerified("https://example.test/file", {
    fetcher, maximum: 100, expectedBytes: bytes.length + 1,
  }), /byte length/u);
  await assert.rejects(readVerified("https://example.test/file", {
    fetcher, maximum: 100, expectedSha256: hash("changed"),
  }), /SHA-256/u);
  await assert.rejects(readVerified("https://example.test/file", {
    fetcher: async () => new Response("", { status: 404 }), maximum: 100,
  }), /HTTP 404/u);
});

test("real HTTP redirects and stalled bodies fail without following a target", async () => {
  let targetRequests = 0;
  const server = http.createServer((request, response) => {
    if (request.url === "/redirect") {
      response.writeHead(302, { location: "/target" }).end();
    } else if (request.url === "/target") {
      targetRequests += 1;
      response.end("unexpected");
    } else {
      response.writeHead(200);
      response.write("partial");
    }
  });
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  const address = server.address();
  assert.ok(address && typeof address === "object");
  const base = "http://127.0.0.1:" + address.port;
  try {
    await assert.rejects(readVerified(base + "/redirect", { maximum: 100, requestTimeoutMs: 1000 }), /fetch failed/u);
    assert.equal(targetRequests, 0);
    await assert.rejects(readVerified(base + "/stall", { maximum: 100, requestTimeoutMs: 25 }), /deadline exceeded|aborted/u);
  } finally {
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
  }
});

test("a failed CLI run replaces an earlier passing evidence report", async () => {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), "explorer-publication-verifier-"));
  const report = path.join(directory, "test-results/explorer-public/public-byte-verification.json");
  try {
    await fs.mkdir(path.dirname(report), { recursive: true });
    await fs.writeFile(report, JSON.stringify({ status: "passed", sourceCommit: "stale" }));
    const result = spawnSync(process.execPath, [
      fileURLToPath(new URL("../browser/verify-explorer-publication.mjs", import.meta.url)),
    ], {
      cwd: directory,
      env: { ...process.env, PUBLIC_BASE_URL: "https://wrong.example/gis-ai-go/" },
      encoding: "utf8",
      timeout: 5000,
    });
    assert.equal(result.status, 1);
    assert.match(result.stderr, /exact canonical GIS URL/u);
    const observed = JSON.parse(await fs.readFile(report, "utf8"));
    assert.equal(observed.status, "failed");
    assert.equal(observed.sourceCommit, undefined);
  } finally { await fs.rm(directory, { recursive: true, force: true }); }
});
