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
  APP, LEGACY_APP, LEGACY_SOURCE_COMMIT, acceptedAppForSource,
  LIMITS, TRANSPORT_LIMITS, HttpStatusError, createReadPolicy, createRequestPacer, deploymentBudget,
  hash, ledger, parseLedger, readVerified, retryDelay, runBounded, safePath, settings, verifyPublication, waitForPublication,
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
  assert.match(APP.treeSha256, /^[0-9a-f]{64}$/u);
});

test("only the exact accepted historical GIS source selects the immutable legacy app pins", () => {
  assert.equal(LEGACY_SOURCE_COMMIT, "8e67ae88e68341120a712d102f692894fbd89659");
  assert.deepEqual(LEGACY_APP, {
    sourceCommit: "7ffa3297ec85bf28c27963724f221d80579bed1b",
    treeSha256: "d127aadb96a77711d5f7cc7aec8cf731cbf5ec1e3d49304d8132189ea4991f93",
    manifestSha256: "ab227164e2e114148425a453a0e04b6bb21230f79be1e059a3ff6936d57f45f2",
    path: "explorer/okf-explorer-build-manifest.json",
  });
  assert.ok(Object.isFrozen(LEGACY_APP));
  assert.notStrictEqual(APP, LEGACY_APP);
  assert.strictEqual(acceptedAppForSource(LEGACY_SOURCE_COMMIT), LEGACY_APP);
  for (const source of ["a".repeat(40), LEGACY_SOURCE_COMMIT.slice(0, -1) + "0", LEGACY_SOURCE_COMMIT.toUpperCase(), "main", undefined]) {
    assert.strictEqual(acceptedAppForSource(source), APP);
    assert.notStrictEqual(acceptedAppForSource(source), LEGACY_APP);
  }
  assert.throws(() => { LEGACY_APP.treeSha256 = "0".repeat(64); }, TypeError);
});

test("historical readiness requires the accepted source and every legacy app identity field", async () => {
  const expected = {
    baseUrl: new URL("https://chris-page-gov.github.io/gis-ai-go/"),
    sourceCommit: LEGACY_SOURCE_COMMIT, version: "0.1.0", payloadRoot: "b".repeat(64), okfRoot: "c".repeat(64),
  };
  const receipt = {
    schema: "gis-ai-go.pages-site-receipt.v2", repository: "chris-page-gov/gis-ai-go",
    canonicalUrl: expected.baseUrl.href, basePath: "/gis-ai-go/", sourceCommit: expected.sourceCommit,
    version: expected.version, payloadRootSha256: expected.payloadRoot, okfContentRootSha256: expected.okfRoot,
    app: LEGACY_APP,
  };
  const options = { deadlineMs: 1000, attemptLimit: 1, pauseMs: 0 };
  const observed = await waitForPublication(expected, { ...options,
    fetcher: async () => new Response(JSON.stringify(receipt)),
  });
  assert.equal(observed.status, "ready");
  for (const key of ["sourceCommit", "treeSha256", "manifestSha256"]) {
    await assert.rejects(waitForPublication(expected, { ...options,
      fetcher: async () => new Response(JSON.stringify({ ...receipt, app: { ...LEGACY_APP, [key]: "e".repeat(key === "sourceCommit" ? 40 : 64) } })),
    }), /readiness did not pass/u);
  }
  await assert.rejects(waitForPublication(expected, { ...options,
    fetcher: async () => new Response(JSON.stringify({ ...receipt, sourceCommit: "d".repeat(40) })),
  }), /readiness did not pass/u);
});

test("complete verification applies independently selected app pins before reading an untrusted OKF identity", async () => {
  async function probe(sourceCommit, app) {
    const expected = {
      baseUrl: new URL("http://127.0.0.1:8131/gis-ai-go/"), mode: "loopback-candidate",
      sourceCommit, version: "0.1.0", okfRoot: "c".repeat(64),
    };
    const manifest = Buffer.from(JSON.stringify({
      schema: "gis-ai-go.pages-manifest.v2", repository: "chris-page-gov/gis-ai-go",
      sourceCommit, version: expected.version, basePath: "/gis-ai-go/",
      canonicalUrl: "https://chris-page-gov.github.io/gis-ai-go/",
      okfContentRootSha256: expected.okfRoot, app, okf: null,
    }));
    const checksums = Buffer.from(ledger([{ path: "publication/manifest.json", bytes: manifest.length, sha256: hash(manifest) }]));
    expected.checksumsSha256 = hash(checksums);
    return verifyPublication(expected, {
      fetcher: async url => {
        if (new URL(url).pathname.endsWith("publication/CHECKSUMS.sha256")) return new Response(checksums);
        if (new URL(url).pathname.endsWith("publication/manifest.json")) return new Response(manifest);
        throw Error("unexpected request after app identity probe");
      },
    });
  }
  for (const [source, app] of [[LEGACY_SOURCE_COMMIT, LEGACY_APP], ["a".repeat(40), APP]]) {
    await assert.rejects(probe(source, app), /OKF identity must be an object/u);
    for (const key of ["sourceCommit", "treeSha256", "manifestSha256", "path"]) {
      await assert.rejects(probe(source, { ...app, [key]: "unaccepted app identity" }), new RegExp("app identity mismatch: " + key, "u"));
    }
  }
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

function advancingClock() {
  let now = 0;
  const waits = [];
  return {
    clock: () => now,
    waits,
    wait: async (milliseconds, signal) => {
      if (signal?.aborted) throw signal.reason;
      waits.push(milliseconds);
      now += milliseconds;
    },
  };
}

test("a transient response is cancelled unread and only the verified recovery body is counted", async () => {
  const timing = advancingClock();
  let calls = 0;
  let cancelled = 0;
  let accounted = 0;
  const policy = createReadPolicy({
    ...timing,
    fetcher: async () => {
      calls += 1;
      if (calls === 1) return new Response(new ReadableStream({
        start(controller) { controller.enqueue(Buffer.from("never accepted")); },
        cancel() { cancelled += 1; },
      }), { status: 503, headers: { "content-length": "0" } });
      return new Response("exact");
    },
  });
  const response = await policy.read("https://example.test/passage", {
    maximum: 5, expectedBytes: 5, expectedSha256: hash("exact"),
    account: bytes => { accounted += bytes; },
  });
  assert.equal(response.bytes, 5);
  assert.equal(accounted, 5);
  assert.equal(cancelled, 1);
  assert.equal(calls, 2);
  assert.deepEqual(timing.waits, [1000]);
  const report = policy.snapshot();
  assert.equal(report.startedRequests, 2);
  assert.equal(report.additionalRequests, 1);
  assert.equal(report.retryReservations, 1);
  assert.equal(report.reservedReplayBytes, 5);
  assert.equal(report.additionalResponseBytes, 5);
  assert.equal(report.errorBodyBytesConsumed, 0);
  assert.equal(report.retriedFiles, 1);
  assert.equal(report.cancelledErrorBodies, 1);
  assert.equal(report.transientStatusCounts[503], 1);
  assert.deepEqual(report.retryEvents, [
    { path: "passage", status: 503, attempt: 2, delayMs: 1000, reservedBytes: 5, started: true },
  ]);
});

test("Retry-After accepts bounded integer seconds and exact HTTP dates without retrying early", async () => {
  const now = Date.UTC(2026, 9, 26, 21);
  assert.equal(retryDelay(new HttpStatusError("u", 429, "3", true), 1, now), 3000);
  assert.equal(retryDelay(new HttpStatusError("u", 503, new Date(now + 5000).toUTCString(), true), 1, now), 5000);
  assert.equal(retryDelay(new HttpStatusError("u", 504, new Date(now - 5000).toUTCString(), true), 2, now), 2000);
  for (const header of ["-1", "1.5", "Infinity", "eleven", "11", new Date(now + 11_000).toUTCString()]) {
    assert.throws(() => retryDelay(new HttpStatusError("u", 503, header, true), 1, now), /Retry-After/u);
  }
  const timing = advancingClock();
  let calls = 0;
  const policy = createReadPolicy({
    ...timing, wallClock: () => now,
    fetcher: async () => {
      calls += 1;
      if (calls === 1) return new Response("", { status: 429, headers: { "retry-after": "3" } });
      if (calls === 2) return new Response("", { status: 502 });
      return new Response("ok");
    },
  });
  await policy.read("https://example.test/file", { maximum: 2, expectedBytes: 2, expectedSha256: hash("ok") });
  assert.deepEqual(timing.waits, [3000, 2000]);
  assert.equal(calls, 3);
  assert.equal(policy.snapshot().additionalRequests, 2);
});

test("failure telemetry retains retry bytes before an aggregate accounting rejection", async () => {
  let calls = 0;
  const policy = createReadPolicy({
    ...advancingClock(),
    fetcher: async () => {
      calls += 1;
      return calls === 1 ? new Response("", { status: 503 }) : new Response("count");
    },
  });
  await assert.rejects(policy.read("https://example.test/file", {
    maximum: 5, account: () => { throw Error("aggregate byte ceiling exceeded"); },
  }), /aggregate byte ceiling/u);
  assert.equal(calls, 2);
  assert.equal(policy.snapshot().additionalResponseBytes, 5);
  assert.equal(policy.snapshot().additionalRequests, 1);
});

test("the per-file retry ceiling never starts a fourth request", async () => {
  let calls = 0;
  const policy = createReadPolicy({
    ...advancingClock(),
    fetcher: async () => { calls += 1; return new Response("", { status: 504 }); },
  });
  await assert.rejects(policy.read("https://example.test/file", { maximum: 100 }), /HTTP 504/u);
  assert.equal(calls, 3);
  assert.equal(policy.snapshot().additionalRequests, 2);
  assert.equal(policy.snapshot().reservedReplayBytes, 200);
  assert.equal(policy.snapshot().transientStatusCounts[504], 3);
});

test("non-transient status, redirect and arbitrary error text are never retried", async () => {
  for (const status of [301, 400, 401, 403, 404, 500, 501]) {
    let calls = 0;
    const policy = createReadPolicy({
      ...advancingClock(),
      fetcher: async () => { calls += 1; return new Response("", { status }); },
    });
    await assert.rejects(policy.read("https://example.test/file", { maximum: 100 }), /HTTP/u);
    assert.equal(calls, 1);
    assert.equal(policy.snapshot().additionalRequests, 0);
  }
  for (const message of ["HTTP 503 in unrelated network text", "fetch failed", "publication request deadline exceeded"]) {
    let calls = 0;
    const policy = createReadPolicy({
      ...advancingClock(),
      fetcher: async () => { calls += 1; throw Error(message); },
    });
    await assert.rejects(policy.read("https://example.test/file", { maximum: 100 }), new RegExp(message, "u"));
    assert.equal(calls, 1);
    assert.equal(policy.snapshot().retryReservations, 0);
  }
});

test("a recovered 200 still fails immediately on wrong bytes or a failed body read", async () => {
  for (const [body, expected, pattern] of [
    ["bad", { maximum: 3, expectedBytes: 3, expectedSha256: hash("yes") }, /SHA-256/u],
    ["ab", { maximum: 3, expectedBytes: 3, expectedSha256: hash("yes") }, /byte length/u],
    ["long", { maximum: 3, expectedBytes: 3, expectedSha256: hash("yes") }, /byte limit/u],
  ]) {
    let calls = 0;
    const policy = createReadPolicy({
      ...advancingClock(),
      fetcher: async () => {
        calls += 1;
        return calls === 1 ? new Response("", { status: 503 }) : new Response(body);
      },
    });
    await assert.rejects(policy.read("https://example.test/file", expected), pattern);
    assert.equal(calls, 2);
    assert.equal(policy.snapshot().retryReservations, 1);
  }
  let calls = 0;
  const policy = createReadPolicy({
    ...advancingClock(),
    fetcher: async () => {
      calls += 1;
      return new Response(new ReadableStream({ start(controller) { controller.error(Error("503 body read failure")); } }));
    },
  });
  await assert.rejects(policy.read("https://example.test/file", { maximum: 3 }), /503 body read failure/u);
  assert.equal(calls, 1);
  assert.equal(policy.snapshot().additionalRequests, 0);
});

test("concurrent transient failures cannot reserve over 64 extra requests", async () => {
  const controller = new AbortController();
  const calls = new Map();
  const policy = createReadPolicy({
    ...advancingClock(), signal: controller.signal,
    fetcher: async url => {
      const count = (calls.get(url) ?? 0) + 1;
      calls.set(url, count);
      return new Response("", { status: count === 1 ? 503 : 200 });
    },
  });
  await assert.rejects(runBounded(Array.from({ length: 80 }, (_, index) => index), index =>
    policy.read("https://example.test/files/" + index, {
      maximum: 0, expectedBytes: 0, expectedSha256: hash(""),
    }), { concurrency: 12, controller }), /additional request ceiling/u);
  const report = policy.snapshot();
  assert.equal(report.retryReservations, TRANSPORT_LIMITS.extraRequests);
  assert.ok(report.additionalRequests <= 64);
  assert.equal(report.retryEvents.length, 64);
  assert.ok(report.retryEvents.every(event => event.reservedBytes === 0));
  const observed = [...calls.values()].reduce((sum, count) => sum + count, 0);
  await new Promise(resolve => setTimeout(resolve, 0));
  assert.equal([...calls.values()].reduce((sum, count) => sum + count, 0), observed);
});

test("replay bytes are reserved from declared bounds rather than response headers", async () => {
  const calls = new Map();
  const policy = createReadPolicy({
    ...advancingClock(),
    fetcher: async url => {
      const count = (calls.get(url) ?? 0) + 1;
      calls.set(url, count);
      return new Response("", { status: count === 1 ? 503 : 404, headers: { "content-length": "0" } });
    },
  });
  for (const file of ["one", "two"]) {
    await assert.rejects(policy.read("https://example.test/" + file, {
      maximum: 32 * 1024 * 1024, expectedBytes: 32 * 1024 * 1024,
    }), /HTTP 404/u);
  }
  await assert.rejects(policy.read("https://example.test/three", { maximum: 1 }), /reserved replay byte ceiling/u);
  assert.equal(policy.snapshot().reservedReplayBytes, 64 * 1024 * 1024);
  assert.equal(policy.snapshot().additionalRequests, 2);
  assert.equal(policy.snapshot().retryReservations, 2);
  assert.equal(calls.get("https://example.test/three"), 1);
});

test("public starts are spaced while response bodies remain concurrent", async () => {
  const controller = new AbortController();
  const timing = advancingClock();
  const starts = [];
  const waiting = [];
  const deadline = setTimeout(() => controller.abort(Error("pacer serialised response completion")), 500);
  const policy = createReadPolicy({
    ...timing, signal: controller.signal, deployed: true,
    fetcher: () => new Promise(resolve => {
      starts.push(timing.clock());
      waiting.push(resolve);
      if (waiting.length === 12) for (const ready of waiting) ready(new Response("x"));
    }),
  });
  try {
    await Promise.all(Array.from({ length: 12 }, (_, index) => policy.read("https://example.test/" + index, {
      maximum: 1, expectedBytes: 1, expectedSha256: hash("x"),
    })));
  } finally { clearTimeout(deadline); controller.abort(); }
  assert.deepEqual(starts, Array.from({ length: 12 }, (_, index) => index * 20));
  assert.equal(policy.snapshot().minimumObservedStartGapMs, 20);
  assert.equal(policy.snapshot().peakActiveRequests, 12);
  assert.ok(policy.snapshot().peakQueuedStarts <= 12);
});

test("an event-loop stall does not release overdue starts in a catch-up burst", async () => {
  let now = 0;
  let firstWait = true;
  const starts = [];
  const pacer = createRequestPacer({
    enabled: true, clock: () => now,
    wait: async delay => {
      now += firstWait ? 1000 : delay;
      firstWait = false;
    },
  });
  await Promise.all(Array.from({ length: 5 }, () => pacer.start(() => { starts.push(now); })));
  assert.deepEqual(starts, [0, 1000, 1020, 1040, 1060]);
});

test("synchronous fetch initialisation cannot shorten the next actual start gap", async () => {
  let now = 0;
  const starts = [];
  const pacer = createRequestPacer({
    enabled: true, clock: () => now,
    wait: async delay => { now += delay; },
  });
  await Promise.all([0, 1, 2].map(index => pacer.start(() => {
    if (index === 0) now += 5;
    starts.push(now);
  })));
  assert.deepEqual(starts, [5, 25, 45]);
  assert.equal(pacer.snapshot().minimumObservedStartGapMs, 20);
});

test("loopback reads are unpaced and a queued public start cannot outlive global abort", async () => {
  const timing = advancingClock();
  const local = createReadPolicy({ ...timing, fetcher: async () => new Response("x") });
  await Promise.all([1, 2, 3].map(index => local.read("http://127.0.0.1/" + index, { maximum: 1 })));
  assert.deepEqual(timing.waits, []);
  assert.equal(local.snapshot().requestsPerSecondLimit, null);
  const controller = new AbortController();
  const started = [];
  const pacer = createRequestPacer({ enabled: true, signal: controller.signal });
  const work = [0, 1, 2].map(index => pacer.start(() => { started.push(index); }));
  setTimeout(() => controller.abort(Error("global walk deadline")), 2);
  const results = await Promise.allSettled(work);
  assert.deepEqual(started, [0]);
  assert.equal(results.filter(result => result.status === "rejected").length, 2);
  assert.equal(pacer.snapshot().startedRequests, 1);
});

test("request deadlines begin at fetch start and global deadlines include retry backoff", async () => {
  const starts = [];
  const policy = createReadPolicy({
    deployed: true,
    fetcher: async () => { starts.push(performance.now()); return new Response("x"); },
  });
  await Promise.all([1, 2].map(index => policy.read("https://example.test/" + index, {
    maximum: 1, requestTimeoutMs: 10,
  })));
  assert.ok(starts[1] - starts[0] >= 20);
  let calls = 0;
  const began = performance.now();
  await assert.rejects(verifyPublication({
    baseUrl: new URL("https://chris-page-gov.github.io/gis-ai-go/"),
    mode: "deployed-publication", checksumsSha256: "a".repeat(64),
  }, {
    deadlineMs: 30,
    fetcher: async () => { calls += 1; return new Response("", { status: 503 }); },
  }), error => {
    assert.match(error.message, /complete publication deadline/u);
    assert.equal(error.verificationTransport.retryReservations, 1);
    assert.equal(error.verificationTransport.additionalRequests, 0);
    assert.equal(error.verificationTransport.retryEvents[0].started, false);
    return true;
  });
  assert.equal(calls, 1);
  assert.ok(performance.now() - began < 500);
});

test("a stalled error-body cancellation is bounded and never treated as retryable", async () => {
  const policy = createReadPolicy({
    fetcher: async () => new Response(new ReadableStream({
      cancel() { return new Promise(() => {}); },
    }), { status: 503 }),
  });
  await assert.rejects(policy.read("https://example.test/file", {
    maximum: 1, requestTimeoutMs: 20,
  }), /request deadline/u);
  assert.equal(policy.snapshot().startedRequests, 1);
  assert.equal(policy.snapshot().retryReservations, 0);
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
