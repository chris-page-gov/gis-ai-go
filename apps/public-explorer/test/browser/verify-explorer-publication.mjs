import { createHash } from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { isDeepStrictEqual } from "node:util";
import { setTimeout as pause } from "node:timers/promises";

// Independent acceptance pins: these must change deliberately with an accepted
// upstream application, rather than trusting a self-declared deployed manifest.
export const APP = Object.freeze({
  sourceCommit: "7ffa3297ec85bf28c27963724f221d80579bed1b",
  treeSha256: "d127aadb96a77711d5f7cc7aec8cf731cbf5ec1e3d49304d8132189ea4991f93",
  manifestSha256: "ab227164e2e114148425a453a0e04b6bb21230f79be1e059a3ff6936d57f45f2",
  path: "explorer/okf-explorer-build-manifest.json",
});
export const LIMITS = Object.freeze({
  files: 50_000,
  payloadFiles: 49_995,
  payloadFileBytes: 32 * 1024 * 1024,
  metadataBytes: 64 * 1024 * 1024,
  manifestBytes: 24 * 1024 * 1024,
  ledgerBytes: 8 * 1024 * 1024,
  retainedJsonBytes: 24 * 1024 * 1024,
  totalBytes: 999_999_999,
  concurrency: 12,
  requestTimeoutMs: 30_000,
  deadlineMs: 20 * 60_000,
});
export const TRANSPORT_LIMITS = Object.freeze({
  extraAttemptsPerFile: 2,
  extraRequests: 64,
  replayBytes: 64 * 1024 * 1024,
  retryAfterMs: 10_000,
  startIntervalMs: 20,
});
const TRANSIENT_STATUS = new Set([429, 502, 503, 504]);
const REPOSITORY = "chris-page-gov/gis-ai-go";
const BASE_PATH = "/gis-ai-go/";
const CANONICAL_URL = "https://chris-page-gov.github.io/gis-ai-go/";
const HEX = /^[0-9a-f]{64}$/u;
const EMPTY_SHA256 = hash(new Uint8Array());
const SUPPORT = [
  "publication/provenance.json",
  "publication/sbom.cdx.json",
  "publication/site-receipt.json",
];
const RETAIN = new Set([
  APP.path,
  "EXPLORER-DISTRIBUTION.json",
  "gis/explorer/okf-explorer.json",
  "gis/explorer/context/manifest.json",
  "publication/provenance.json",
  "publication/site-receipt.json",
]);
const READINESS = Object.freeze({
  deadlineMs: 110_000, attempts: 55, fileBytes: 64 * 1024, requestTimeoutMs: 5000, pauseMs: 2000,
});

function invariant(condition, message) {
  if (!condition) throw Error(message);
}
function throwIfAborted(signal) {
  if (signal?.aborted) throw signal.reason ?? Error("publication request aborted");
}
function abortable(value, signal) {
  if (!signal) return Promise.resolve(value);
  if (signal.aborted) {
    // Attach rejection handling even when an operation was already initiated.
    Promise.resolve(value).catch(() => {});
    return Promise.reject(signal.reason ?? Error("publication request aborted"));
  }
  return new Promise((resolve, reject) => {
    const cancelled = () => {
      signal.removeEventListener("abort", cancelled);
      reject(signal.reason ?? Error("publication request aborted"));
    };
    signal.addEventListener("abort", cancelled, { once: true });
    Promise.resolve(value).then(result => {
      signal.removeEventListener("abort", cancelled);
      resolve(result);
    }, error => {
      signal.removeEventListener("abort", cancelled);
      reject(error);
    });
  });
}
export class HttpStatusError extends Error {
  constructor(url, status, retryAfter, bodyCancelled) {
    super(url + " returned HTTP " + status);
    this.name = "HttpStatusError";
    this.status = status;
    this.retryAfter = retryAfter;
    this.bodyCancelled = bodyCancelled;
  }
}
export function retryDelay(error, extraAttempt, now = Date.now()) {
  invariant(error instanceof HttpStatusError && TRANSIENT_STATUS.has(error.status),
    "only an observed transient HTTP status can be retried");
  invariant(Number.isSafeInteger(extraAttempt) && extraAttempt >= 1 &&
    extraAttempt <= TRANSPORT_LIMITS.extraAttemptsPerFile, "retry attempt is out of bounds");
  let declared = 0;
  if (error.retryAfter !== null) {
    invariant(typeof error.retryAfter === "string" && error.retryAfter.length <= 256,
      "Retry-After header is out of bounds");
    const value = error.retryAfter.trim();
    if (/^\d+$/u.test(value)) {
      const seconds = Number(value);
      invariant(Number.isSafeInteger(seconds), "Retry-After must be a bounded delay");
      declared = seconds * 1000;
    } else {
      const timestamp = Date.parse(value);
      invariant(Number.isFinite(timestamp) && new Date(timestamp).toUTCString() === value,
        "Retry-After must be integer seconds or an HTTP date");
      declared = Math.max(0, timestamp - now);
    }
    invariant(declared <= TRANSPORT_LIMITS.retryAfterMs, "Retry-After exceeds the 10-second ceiling");
  }
  return Math.max(extraAttempt * 1000, declared);
}

// Serialise only request starts. A delayed event loop cannot release overdue
// tickets in a burst: each next grant is measured from the actual previous one.
export function createRequestPacer({
  enabled,
  signal,
  clock = () => performance.now(),
  wait = (milliseconds, waitSignal) => pause(milliseconds, undefined, { signal: waitSignal }),
} = {}) {
  let tail = Promise.resolve();
  let previousStart;
  let queued = 0;
  let peakQueued = 0;
  let starts = 0;
  let minimumGap;
  async function start(operation, requestSignal) {
    const effectiveSignal = signal && requestSignal ? AbortSignal.any([signal, requestSignal]) : signal ?? requestSignal;
    throwIfAborted(effectiveSignal);
    const invoke = () => {
      throwIfAborted(effectiveSignal);
      const observed = clock();
      if (previousStart !== undefined) {
        const gap = observed - previousStart;
        minimumGap = minimumGap === undefined ? gap : Math.min(minimumGap, gap);
      }
      starts += 1;
      try {
        return operation();
      } finally {
        // Include synchronous fetch initialisation in the previous start.
        // The next launch waits 20ms after this operation returned its promise,
        // without waiting for response headers or body completion.
        previousStart = clock();
      }
    };
    if (!enabled) return invoke();
    invariant(queued < LIMITS.concurrency, "request-start queue exceeds the worker ceiling");
    queued += 1;
    peakQueued = Math.max(peakQueued, queued);
    const preceding = tail;
    let release;
    tail = new Promise(resolve => { release = resolve; });
    try {
      await preceding;
      throwIfAborted(effectiveSignal);
      while (previousStart !== undefined) {
        const remaining = previousStart + TRANSPORT_LIMITS.startIntervalMs - clock();
        if (remaining <= 0) break;
        await abortable(wait(remaining, effectiveSignal), effectiveSignal);
        throwIfAborted(effectiveSignal);
      }
      return invoke();
    } finally {
      queued -= 1;
      release();
    }
  }
  return {
    start,
    snapshot: () => ({
      enabled: Boolean(enabled),
      minimumStartIntervalMs: enabled ? TRANSPORT_LIMITS.startIntervalMs : 0,
      requestsPerSecondLimit: enabled ? 50 : null,
      startedRequests: starts,
      peakQueuedStarts: peakQueued,
      minimumObservedStartGapMs: minimumGap ?? null,
    }),
  };
}

export function createReadPolicy({
  signal,
  deployed = false,
  fetcher = fetch,
  clock = () => performance.now(),
  wallClock = () => Date.now(),
  wait = (milliseconds, waitSignal) => pause(milliseconds, undefined, { signal: waitSignal }),
} = {}) {
  const pacer = createRequestPacer({ enabled: deployed, signal, clock, wait });
  const events = [];
  const retriedFiles = new Set();
  const statusCounts = { 429: 0, 502: 0, 503: 0, 504: 0 };
  let reservations = 0;
  let additionalRequests = 0;
  let reservedReplayBytes = 0;
  let additionalResponseBytes = 0;
  let cancelledErrorBodies = 0;
  let activeRequests = 0;
  let peakActiveRequests = 0;
  const snapshot = () => ({
    ...pacer.snapshot(),
    retryReservations: reservations,
    additionalRequests,
    reservedReplayBytes,
    additionalResponseBytes,
    retriedFiles: retriedFiles.size,
    transientStatusCounts: { ...statusCounts },
    cancelledErrorBodies,
    // Error bodies are cancelled before application reads; this is not a
    // measurement of bytes the HTTP implementation may have prefetched.
    errorBodyBytesConsumed: 0,
    peakActiveRequests,
    retryEvents: events.map(event => ({ ...event })),
  });
  async function read(url, options) {
    const resource = safePath(options.resource ?? new URL(url).pathname.replace(/^\/+/u, ""));
    let attempt = 0;
    let event;
    while (true) {
      throwIfAborted(signal);
      let started = false;
      try {
        try {
          return await readVerified(url, {
            ...options,
            fetcher,
            signal,
            startRequest: (operation, requestSignal) => pacer.start(() => {
              started = true;
              activeRequests += 1;
              peakActiveRequests = Math.max(peakActiveRequests, activeRequests);
              if (attempt > 0) {
                additionalRequests += 1;
                retriedFiles.add(resource);
                event.started = true;
              }
              return operation();
            }, requestSignal),
            account: bytes => {
              if (attempt > 0) additionalResponseBytes += bytes;
              options.account?.(bytes);
              if (attempt > 0) {
                invariant(additionalResponseBytes <= TRANSPORT_LIMITS.replayBytes,
                  "additional response byte ceiling exceeded");
              }
            },
          });
        } finally {
          if (started) activeRequests -= 1;
        }
      } catch (error) {
        if (!(error instanceof HttpStatusError)) throw error;
        if (error.bodyCancelled) cancelledErrorBodies += 1;
        if (!TRANSIENT_STATUS.has(error.status)) throw error;
        statusCounts[error.status] += 1;
        if (attempt >= TRANSPORT_LIMITS.extraAttemptsPerFile) throw error;
        const delayMs = retryDelay(error, attempt + 1, wallClock());
        const replayBytes = options.expectedBytes ?? options.maximum;
        invariant(Number.isSafeInteger(replayBytes) && replayBytes >= 0,
          "retry requires a declared response byte ceiling");
        // Reserve both shared budgets without an intervening await.
        invariant(reservations < TRANSPORT_LIMITS.extraRequests, "additional request ceiling exceeded");
        invariant(reservedReplayBytes + replayBytes <= TRANSPORT_LIMITS.replayBytes,
          "reserved replay byte ceiling exceeded");
        reservations += 1;
        reservedReplayBytes += replayBytes;
        event = { path: resource, status: error.status, attempt: attempt + 2, delayMs, reservedBytes: replayBytes, started: false };
        events.push(event);
        attempt += 1;
        await abortable(wait(delayMs, signal), signal);
        throwIfAborted(signal);
      }
    }
  }
  return { read, snapshot };
}
export function hash(value) {
  return createHash("sha256").update(value).digest("hex");
}
function object(value, label) {
  invariant(value && typeof value === "object" && !Array.isArray(value), label + " must be an object");
  return value;
}
function json(bytes, label) {
  try { return object(JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes)), label); }
  catch (error) { throw Error(label + " is not valid JSON: " + error.message); }
}
function byteOrder(a, b) {
  return Buffer.compare(Buffer.from(a), Buffer.from(b));
}
export function safePath(value) {
  invariant(typeof value === "string" && value.length > 0 && Buffer.byteLength(value) <= 1024,
    "unsafe publication path");
  invariant(!value.startsWith("/") && !/[\\\u0000-\u001f\u007f]/u.test(value),
    "unsafe publication path: " + value);
  invariant(value.split("/").every(part => part && part !== "." && part !== ".."),
    "unsafe publication path: " + value);
  return value;
}
function encodedPath(value) {
  return safePath(value).split("/").map(encodeURIComponent).join("/");
}
export function ledger(entries) {
  return entries.map(entry => entry.sha256 + "  " + entry.path + "\n").join("");
}
function requireDigest(value, label) {
  invariant(typeof value === "string" && HEX.test(value), label + " must be a SHA-256");
  return value;
}
function entry(value, maximum, label) {
  object(value, label);
  invariant(Object.keys(value).sort().join(",") === "bytes,path,sha256", label + " fields differ");
  safePath(value.path);
  requireDigest(value.sha256, label + " digest");
  invariant(Number.isSafeInteger(value.bytes) && value.bytes >= 0 && value.bytes <= maximum,
    label + " byte limit exceeded");
  return value;
}
function entries(value, maximum, label) {
  invariant(Array.isArray(value) && value.length > 0 && value.length <= LIMITS.files,
    label + " file count is out of bounds");
  const result = value.map(row => entry(row, maximum, label));
  const paths = result.map(row => row.path);
  invariant(paths.every((name, index) => index === 0 || byteOrder(paths[index - 1], name) < 0),
    label + " paths must be unique and sorted");
  return result;
}
export function parseLedger(bytes) {
  const text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  invariant(text.endsWith("\n"), "checksum ledger must end with a newline");
  const lines = text.slice(0, -1).split("\n");
  // The empty control file and this ledger itself are not ledger rows.
  invariant(lines.length > 0 && lines.length <= LIMITS.files - 2, "checksum ledger file limit exceeded");
  const rows = lines.map(line => {
    const match = /^([0-9a-f]{64})  (.+)$/u.exec(line);
    invariant(match, "invalid checksum ledger row");
    return { path: safePath(match[2]), sha256: match[1] };
  });
  invariant(rows.every((row, index) => index === 0 || byteOrder(rows[index - 1].path, row.path) < 0),
    "checksum ledger paths must be unique and sorted");
  invariant(!rows.some(row => row.path === ".nojekyll" || row.path === "publication/CHECKSUMS.sha256"),
    "checksum ledger contains an excluded file");
  return rows;
}
export function deploymentBudget(payloadFiles, totalBytes) {
  invariant(Number.isSafeInteger(payloadFiles) && payloadFiles > 0 &&
    payloadFiles <= LIMITS.payloadFiles, "payload file ceiling exceeded");
  // payload already contains empty .nojekyll; add the three supporting JSON
  // documents, publication manifest and checksum ledger to count every member.
  const archiveFiles = payloadFiles + SUPPORT.length + 2;
  invariant(archiveFiles <= LIMITS.files, "complete publication file ceiling exceeded");
  invariant(Number.isSafeInteger(totalBytes) && totalBytes >= 0 && totalBytes <= LIMITS.totalBytes,
    "declared complete publication byte limit exceeded");
  return { archiveFiles, fetchedFiles: archiveFiles - 1, totalBytes };
}
function identity(document, schema, expected) {
  invariant(document.schema === schema, "unexpected " + schema + " schema");
  for (const [key, value] of Object.entries({
    repository: REPOSITORY,
    sourceCommit: expected.sourceCommit,
    version: expected.version,
    basePath: BASE_PATH,
    canonicalUrl: CANONICAL_URL,
  })) invariant(document[key] === value, schema + " identity mismatch: " + key);
}
function appIdentity(value) {
  object(value, "app identity");
  for (const [key, expected] of Object.entries(APP)) {
    invariant(value[key] === expected, "app identity mismatch: " + key);
  }
}
export function settings(environment = process.env) {
  function required(name) {
    invariant(typeof environment[name] === "string" && environment[name].trim(), name + " is required");
    return environment[name].trim();
  }
  const baseUrl = new URL(required("PUBLIC_BASE_URL"));
  const local = baseUrl.hostname === "127.0.0.1" || baseUrl.hostname === "localhost";
  invariant(baseUrl.protocol === "https:" || (local && baseUrl.protocol === "http:"),
    "PUBLIC_BASE_URL must use HTTPS except for loopback HTTP");
  invariant(!baseUrl.username && !baseUrl.password && !baseUrl.search && !baseUrl.hash,
    "PUBLIC_BASE_URL must not contain credentials, a query or a fragment");
  invariant(baseUrl.pathname === BASE_PATH, "PUBLIC_BASE_URL must preserve /gis-ai-go/");
  invariant(local || baseUrl.href === CANONICAL_URL, "public verification must use the exact canonical GIS URL");
  const sourceCommit = required("EXPECTED_SOURCE_COMMIT");
  invariant(/^[0-9a-f]{40}$/u.test(sourceCommit), "EXPECTED_SOURCE_COMMIT is invalid");
  const version = required("EXPECTED_VERSION");
  invariant(/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/u.test(version),
    "EXPECTED_VERSION is invalid");
  return {
    baseUrl,
    sourceCommit,
    version,
    archiveSha256: requireDigest(required("EXPECTED_ARCHIVE_SHA256"), "EXPECTED_ARCHIVE_SHA256"),
    okfRoot: requireDigest(required("EXPECTED_OKF_CONTENT_ROOT"), "EXPECTED_OKF_CONTENT_ROOT"),
    payloadRoot: requireDigest(required("EXPECTED_PAYLOAD_ROOT"), "EXPECTED_PAYLOAD_ROOT"),
    checksumsSha256: requireDigest(required("EXPECTED_PUBLIC_CHECKSUMS_SHA256"), "EXPECTED_PUBLIC_CHECKSUMS_SHA256"),
    mode: local ? "loopback-candidate" : "deployed-publication",
  };
}

// Only fixed-size chunks and selected bounded JSON documents are retained.
// redirect:error, independent file ceilings and a shared abort signal apply to
// every request, including supporting metadata.
export async function readVerified(url, options) {
  const {
    fetcher = fetch,
    signal,
    maximum,
    expectedBytes,
    expectedSha256,
    retain = false,
    requestTimeoutMs = LIMITS.requestTimeoutMs,
    account = () => {},
    startRequest = operation => operation(),
  } = options;
  invariant(Number.isSafeInteger(requestTimeoutMs) && requestTimeoutMs > 0 &&
    requestTimeoutMs <= LIMITS.requestTimeoutMs, "request deadline is out of bounds");
  const localAbort = new AbortController();
  const requestSignal = signal ? AbortSignal.any([signal, localAbort.signal]) : localAbort.signal;
  let timeout;
  try {
    const response = await startRequest(() => {
      throwIfAborted(requestSignal);
      // Queueing and backoff consume the walk deadline. The per-request clock
      // begins at this actual fetch start, including headers and body lifetime.
      timeout = setTimeout(() => localAbort.abort(Error("publication request deadline exceeded")), requestTimeoutMs);
      return abortable(fetcher(url, {
        redirect: "error",
        credentials: "omit",
        cache: "no-store",
        headers: { "cache-control": "no-cache" },
        signal: requestSignal,
      }), requestSignal);
    }, requestSignal);
    if (response.status !== 200) {
      const hasBody = Boolean(response.body);
      if (hasBody) await abortable(response.body.cancel(), requestSignal);
      throw new HttpStatusError(url, response.status, response.headers.get("retry-after"), hasBody);
    }
    invariant(response.body, url + " has no response body");
    const reader = response.body.getReader();
    const digest = createHash("sha256");
    let length = 0;
    const buffers = [];
    try {
      while (true) {
        if (requestSignal.aborted) throw requestSignal.reason;
        const { done, value } = await abortable(reader.read(), requestSignal);
        if (done) break;
        invariant(value instanceof Uint8Array, "response body must contain bytes");
        length += value.byteLength;
        account(value.byteLength);
        invariant(length <= maximum && (expectedBytes === undefined || length <= expectedBytes),
          url + " exceeds its byte limit");
        digest.update(value);
        if (retain) buffers.push(Buffer.from(value));
      }
    } finally { await abortable(reader.cancel(), requestSignal); }
    invariant(expectedBytes === undefined || length === expectedBytes, url + " byte length differs");
    const sha256 = digest.digest("hex");
    invariant(expectedSha256 === undefined || sha256 === expectedSha256, url + " SHA-256 differs");
    return { bytes: length, sha256, ...(retain ? { value: Buffer.concat(buffers, length) } : {}) };
  } finally { clearTimeout(timeout); }
}

export async function waitForPublication(expected, options = {}) {
  const controller = new AbortController();
  const deadlineMs = options.deadlineMs ?? READINESS.deadlineMs;
  const attemptLimit = options.attemptLimit ?? READINESS.attempts;
  invariant(Number.isSafeInteger(deadlineMs) && deadlineMs > 0 && deadlineMs <= READINESS.deadlineMs,
    "readiness deadline is out of bounds");
  invariant(Number.isSafeInteger(attemptLimit) && attemptLimit > 0 && attemptLimit <= READINESS.attempts,
    "readiness attempt limit is out of bounds");
  const timer = setTimeout(() => controller.abort(Error("exact publication readiness deadline exceeded")), deadlineMs);
  const url = new URL("publication/site-receipt.json", expected.baseUrl);
  url.searchParams.set("source", expected.sourceCommit);
  const maximumProbeBytes = READINESS.attempts * READINESS.fileBytes;
  let bytes = 0;
  let attempts = 0;
  let last = "no matching receipt";
  try {
    while (attempts < attemptLimit) {
      if (controller.signal.aborted) throw controller.signal.reason;
      attempts += 1;
      try {
        const response = await readVerified(url.href, {
          fetcher: options.fetcher ?? fetch,
          signal: controller.signal,
          maximum: READINESS.fileBytes,
          requestTimeoutMs: READINESS.requestTimeoutMs,
          retain: true,
          account: size => {
            bytes += size;
            invariant(bytes <= maximumProbeBytes, "readiness probe byte ceiling exceeded");
          },
        });
        const receipt = json(response.value, "readiness receipt");
        const ready = receipt.schema === "gis-ai-go.pages-site-receipt.v2" &&
          receipt.repository === REPOSITORY && receipt.canonicalUrl === CANONICAL_URL &&
          receipt.basePath === BASE_PATH && receipt.sourceCommit === expected.sourceCommit &&
          receipt.version === expected.version && receipt.payloadRootSha256 === expected.payloadRoot &&
          receipt.okfContentRootSha256 === expected.okfRoot &&
          receipt.app?.sourceCommit === APP.sourceCommit && receipt.app?.treeSha256 === APP.treeSha256 &&
          receipt.app?.manifestSha256 === APP.manifestSha256;
        if (ready) return { status: "ready", attempts, probeBytes: bytes, deadlineMs };
        last = "the served receipt still describes another publication";
      } catch (error) {
        if (controller.signal.aborted || bytes > maximumProbeBytes) throw error;
        last = error.message;
      }
      if (attempts < attemptLimit) {
        await pause(options.pauseMs ?? READINESS.pauseMs, undefined, { signal: controller.signal });
      }
    }
    throw Error("exact publication readiness did not pass: " + last);
  } finally { clearTimeout(timer); controller.abort(); }
}

export async function runBounded(items, worker, options = {}) {
  const concurrency = options.concurrency ?? LIMITS.concurrency;
  invariant(Number.isSafeInteger(concurrency) && concurrency > 0 && concurrency <= LIMITS.concurrency,
    "verification concurrency is out of bounds");
  const controller = options.controller ?? new AbortController();
  let next = 0;
  const results = await Promise.allSettled(Array.from({ length: Math.min(concurrency, items.length) }, async () => {
    try {
      while (next < items.length) {
        if (controller.signal.aborted) throw controller.signal.reason;
        const item = items[next++];
        await worker(item, controller.signal);
      }
    } catch (error) { controller.abort(error); throw error; }
  }));
  const failed = results.find(result => result.status === "rejected");
  if (failed) throw failed.reason;
}

export async function verifyPublication(expected, options = {}) {
  const started = Date.now();
  const controller = new AbortController();
  const deadlineMs = options.deadlineMs ?? LIMITS.deadlineMs;
  invariant(Number.isSafeInteger(deadlineMs) && deadlineMs > 0 && deadlineMs <= LIMITS.deadlineMs,
    "complete publication deadline is out of bounds");
  const timer = setTimeout(() => controller.abort(Error("complete publication deadline exceeded")), deadlineMs);
  const policy = createReadPolicy({
    signal: controller.signal,
    deployed: expected.mode === "deployed-publication",
    fetcher: options.fetcher ?? fetch,
  });
  let fetchedBytes = 0;
  let fetchedFiles = 0;
  const retained = new Map();
  const base = expected.baseUrl instanceof URL ? expected.baseUrl : new URL(expected.baseUrl);
  const read = async (relative, maximum, extras = {}) => {
    const url = new URL(encodedPath(relative), base);
    invariant(url.origin === base.origin && url.pathname.startsWith(base.pathname), "publication URL escaped its base");
    const result = await policy.read(url.href, {
      resource: relative,
      maximum,
      requestTimeoutMs: options.requestTimeoutMs ?? LIMITS.requestTimeoutMs,
      account: bytes => {
        fetchedBytes += bytes;
        invariant(fetchedBytes <= LIMITS.totalBytes, "complete publication byte limit exceeded");
      },
      ...extras,
    });
    fetchedFiles += 1;
    return result;
  };
  try {
    const checksumFile = await read("publication/CHECKSUMS.sha256", LIMITS.ledgerBytes, {
      expectedSha256: expected.checksumsSha256, retain: true,
    });
    const checksumRows = parseLedger(checksumFile.value);
    const checksums = new Map(checksumRows.map(row => [row.path, row.sha256]));
    const manifestDigest = checksums.get("publication/manifest.json");
    invariant(manifestDigest, "checksum ledger has no publication manifest");
    const manifestFile = await read("publication/manifest.json", LIMITS.manifestBytes, {
      expectedSha256: manifestDigest, retain: true,
    });
    const manifest = json(manifestFile.value, "publication manifest");
    identity(manifest, "gis-ai-go.pages-manifest.v2", expected);
    invariant(manifest.okfContentRootSha256 === expected.okfRoot, "manifest OKF root differs");
    appIdentity(manifest.app);
    const okf = object(manifest.okf, "OKF identity");
    invariant(okf.sourceRevision === expected.sourceCommit && okf.inputDigest === expected.okfRoot,
      "OKF source identity differs");
    invariant(okf.descriptorPath === "gis/explorer/okf-explorer.json" &&
      okf.contextManifestPath === "gis/explorer/context/manifest.json", "OKF paths differ");
    const payload = object(manifest.payload, "manifest payload");
    const payloadEntries = entries(payload.files, LIMITS.payloadFileBytes, "payload");
    invariant(payloadEntries.length <= LIMITS.payloadFiles, "payload file ceiling exceeded");
    invariant(payload.fileCount === payloadEntries.length, "payload file count differs");
    invariant(payload.rootSha256 === expected.payloadRoot && hash(ledger(payloadEntries)) === expected.payloadRoot,
      "payload root differs");
    const empty = payloadEntries.find(row => row.path === ".nojekyll");
    invariant(empty?.bytes === 0 && empty.sha256 === EMPTY_SHA256, ".nojekyll must be the empty control file");
    const supporting = entries(manifest.publicationFiles, LIMITS.metadataBytes, "publication metadata");
    invariant(supporting.map(row => row.path).join("\n") === SUPPORT.join("\n"),
      "supporting metadata inventory differs");
    const served = [...payloadEntries.filter(row => row.path !== ".nojekyll"), ...supporting];
    const expectedPaths = [...served.map(row => row.path), "publication/manifest.json"].sort(byteOrder);
    invariant(new Set(expectedPaths).size === expectedPaths.length, "publication inventory contains duplicate paths");
    invariant(expectedPaths.length + 2 <= LIMITS.files && expectedPaths.join("\n") === checksumRows.map(row => row.path).join("\n"),
      "checksum ledger does not cover the exact publication inventory");
    let declaredBytes = checksumFile.bytes + manifestFile.bytes;
    for (const row of served) {
      invariant(checksums.get(row.path) === row.sha256, "checksum inventory differs: " + row.path);
      declaredBytes += row.bytes;
    }
    const budget = deploymentBudget(payloadEntries.length, declaredBytes);
    const appEntry = served.find(row => row.path === APP.path);
    invariant(appEntry?.sha256 === APP.manifestSha256, "app manifest is not the accepted build");
    const concurrency = options.concurrency ?? LIMITS.concurrency;
    await runBounded(served, async row => {
      const retain = RETAIN.has(row.path);
      if (retain) invariant(row.bytes <= LIMITS.retainedJsonBytes, "retained JSON byte limit exceeded");
      const result = await read(row.path, row.path.startsWith("publication/") ? LIMITS.metadataBytes : LIMITS.payloadFileBytes, {
        expectedBytes: row.bytes, expectedSha256: row.sha256, retain,
      });
      if (retain) retained.set(row.path, result.value);
    }, { concurrency, controller });
    const appManifest = json(retained.get(APP.path), "app build manifest");
    invariant(appManifest.schema === "okf-explorer-app-build-manifest.v1" &&
      appManifest.algorithm === "sha256-canonical-json-materials-v1" && appManifest.tree_sha256 === APP.treeSha256,
      "app build manifest identity differs");
    const appMaterials = entries(appManifest.materials, LIMITS.payloadFileBytes, "app build");
    invariant(appManifest.file_count === appMaterials.length, "app build material count differs");
    const payloadByPath = new Map(payloadEntries.map(row => [row.path, row]));
    for (const material of appMaterials) {
      const shipped = payloadByPath.get("explorer/" + material.path);
      invariant(shipped?.bytes === material.bytes && shipped?.sha256 === material.sha256,
        "app build material is missing or changed: " + material.path);
    }
    const site = json(retained.get("publication/site-receipt.json"), "site receipt");
    identity(site, "gis-ai-go.pages-site-receipt.v2", expected);
    invariant(site.payloadRootSha256 === expected.payloadRoot && site.okfContentRootSha256 === expected.okfRoot &&
      site.fileCount === payloadEntries.length, "site receipt roots or file count differ");
    appIdentity(site.app);
    invariant(isDeepStrictEqual(site.okf, manifest.okf), "site receipt OKF identity differs");
    invariant(site.provenanceSha256 === checksums.get("publication/provenance.json") &&
      site.sbomSha256 === checksums.get("publication/sbom.cdx.json"), "site receipt metadata hashes differ");
    invariant(site.okfManifestSha256 === checksums.get(okf.descriptorPath), "site receipt descriptor hash differs");
    const provenance = json(retained.get("publication/provenance.json"), "provenance");
    identity(provenance, "gis-ai-go.pages-provenance.v2", expected);
    appIdentity(provenance.app);
    invariant(isDeepStrictEqual(provenance.okf, manifest.okf), "provenance OKF identity differs");
    const source = object(provenance.source, "provenance source");
    invariant(source.path === "artifacts/explorer-pages-dist" &&
      source.payloadRootSha256 === expected.payloadRoot && source.fileCount === payloadEntries.length,
      "provenance payload differs");
    const descriptor = json(retained.get(okf.descriptorPath), "GIS descriptor");
    invariant(descriptor.schema === "okf-explorer-large-corpus.v1" &&
      descriptor.source?.revision === expected.sourceCommit && descriptor.source?.inputDigest === expected.okfRoot &&
      descriptor.snapshot === okf.snapshot, "GIS descriptor identity differs");
    const context = json(retained.get(okf.contextManifestPath), "GIS context");
    invariant(context.schema === "okf-context-corpus.v3" && context.bundle?.snapshot === okf.snapshot &&
      context.bundle?.source_url === CANONICAL_URL + "gis/explorer/context/manifest.json",
      "GIS context is not bound to the canonical publication");
    const distribution = json(retained.get("EXPLORER-DISTRIBUTION.json"), "distribution manifest");
    identity(distribution, "gis-ai-go.explorer-distribution.v1", expected);
    appIdentity(distribution.app);
    invariant(isDeepStrictEqual(distribution.okf, manifest.okf), "distribution OKF identity differs");
    const distributionFiles = entries(distribution.files, LIMITS.payloadFileBytes, "distribution");
    const expectedDistribution = payloadEntries.filter(row => row.path !== ".nojekyll" && row.path !== "EXPLORER-DISTRIBUTION.json");
    invariant(isDeepStrictEqual(distributionFiles, expectedDistribution),
      "distribution manifest does not cover the exact payload");
    invariant(fetchedBytes === declaredBytes, "verified byte count differs from the complete inventory");
    invariant(fetchedFiles === budget.fetchedFiles, "verified file count differs from the complete inventory");
    return {
      schema: "gis-ai-go.explorer-public-byte-verification.v1",
      status: "passed",
      mode: expected.mode,
      baseUrl: base.href,
      sourceCommit: expected.sourceCommit,
      acceptedArchiveSha256: expected.archiveSha256,
      payloadRootSha256: expected.payloadRoot,
      okfContentRootSha256: expected.okfRoot,
      publicChecksumsSha256: expected.checksumsSha256,
      app: APP,
      verifiedFiles: fetchedFiles,
      verifiedBytes: fetchedBytes,
      logicalPayloadFiles: payloadEntries.length,
      emptyControlFiles: 1,
      concurrency,
      peakActiveRequests: policy.snapshot().peakActiveRequests,
      transport: policy.snapshot(),
      elapsedMs: Date.now() - started,
    };
  } catch (error) {
    // runBounded waits for all its workers to settle before this snapshot.
    error.verificationTransport = policy.snapshot();
    throw error;
  } finally { clearTimeout(timer); controller.abort(); }
}

async function main() {
  const destination = path.resolve("test-results/explorer-public/public-byte-verification.json");
  await fs.mkdir(path.dirname(destination), { recursive: true });
  await fs.writeFile(destination, JSON.stringify({
    schema: "gis-ai-go.explorer-public-byte-verification.v1", status: "running",
  }) + "\n");
  try {
    const expected = settings();
    const readiness = expected.mode === "deployed-publication" ? await waitForPublication(expected) : undefined;
    const report = await verifyPublication(expected);
    if (readiness) report.readiness = readiness;
    await fs.writeFile(destination, JSON.stringify(report, null, 2) + "\n");
    console.log(JSON.stringify(report));
  } catch (error) {
    await fs.writeFile(destination, JSON.stringify({
      schema: "gis-ai-go.explorer-public-byte-verification.v1",
      status: "failed",
      error: String(error.message).slice(0, 4096),
      ...(error.verificationTransport ? { transport: error.verificationTransport } : {}),
    }, null, 2) + "\n");
    throw error;
  }
}
if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  main().catch(error => { console.error(error.message); process.exitCode = 1; });
}
