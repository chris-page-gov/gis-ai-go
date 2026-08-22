import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { gzipSync } from "node:zlib";
import test, { beforeEach } from "node:test";

import {
  ONS_ADAPTER_REQUEST,
  ONS_EGRESS_POLICY,
  ONS_OBSERVATION_URI,
  FixedHttpsTransportError,
  OnsDataApiAdapter,
  ProviderAdapterFault,
  buildOnsLiveProbeRecord,
  createOnsDataApiAdapter,
  digestProviderAdapterResult,
  executePristineOnsDataApiAdapter,
  requireExactOnsDataApiAdapter,
  requirePristineOnsDataApiAdapter,
  serialiseProviderAdapterResult,
  type FixedHttpsResponse,
  type FixedHttpsTransport,
  type OnsAttemptTelemetry,
  type ProviderAdapterResult,
} from "../src/index.js";
import {
  isExactFixedHttpsTransportError,
  normaliseFixedHttpsRequestError,
} from "../src/fixed-https.js";

const ACTIVE = Object.freeze({
  discovery: "active",
  invocation: "active",
  reason: "Explicit mocked ONS adapter test.",
} as const);

let processAdmissionNow = Date.parse("2030-01-01T00:00:00Z");

const REPOSITORY_ROOT = fileURLToPath(new URL("../../../../", import.meta.url));
const UV_CACHE_DIRECTORY = fileURLToPath(new URL("../../../../.uv-cache", import.meta.url));
const LIVE_PROBE_SCHEMA = fileURLToPath(
  new URL("../../../../schemas/provider-live-probe.schema.json", import.meta.url),
);
const PROVIDER_RESULT_SCHEMA = fileURLToPath(
  new URL("../../../../schemas/provider-adapter-result.schema.json", import.meta.url),
);
const DRAFT_2020_12_CHECK = [
  "import json, sys",
  "from pathlib import Path",
  "from jsonschema import Draft202012Validator, FormatChecker",
  "schema = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))",
  "Draft202012Validator.check_schema(schema)",
  "validator = Draft202012Validator(schema, format_checker=FormatChecker())",
  "records = json.load(sys.stdin)",
  "json.dump([validator.is_valid(record) for record in records], sys.stdout)",
].join("\n");

beforeEach((context) => {
  if (!("mock" in context)) throw new TypeError("ONS tests require a test context");
  processAdmissionNow += 60_001;
  context.mock.method(Date, "now", () => processAdmissionNow);
});

const VALID_PAYLOAD = Object.freeze({
  dimensions: {
    causeofdeath: {
      option: {
        href: "http://api.beta.ons.gov.uk/v1/code-lists/cause-of-death/codes/all-causes",
        id: "all-causes",
      },
    },
    geography: {
      option: {
        href:
          "http://api.beta.ons.gov.uk/v1/code-lists/administrative-geography/codes/E92000001",
        id: "E92000001",
      },
    },
    time: {
      option: {
        href: "http://api.beta.ons.gov.uk/v1/code-lists/calendar-years/codes/2026",
        id: "2026",
      },
    },
    week: {
      option: {
        href: "http://api.beta.ons.gov.uk/v1/code-lists/week-number/codes/week-24",
        id: "week-24",
      },
    },
  },
  limit: 10_000,
  links: {
    dataset_metadata: {
      href:
        "http://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121/metadata",
    },
    self: {
      href:
        "http://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121/observations?causeofdeath=all-causes&geography=E92000001&time=2026&week=week-24",
    },
    version: {
      href:
        "http://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121",
      id: "121",
    },
  },
  observations: [{ metadata: { "Data Marking": "" }, observation: "12345" }],
  offset: 0,
  total_observations: 1,
});

function mutable<T>(value: T): T {
  return JSON.parse(JSON.stringify(value)) as T;
}

function draft202012Validity(
  schemaPath: string,
  records: readonly unknown[],
): readonly boolean[] {
  const validation = spawnSync(
    "uv",
    [
      "run",
      "--locked",
      "--cache-dir",
      UV_CACHE_DIRECTORY,
      "--project",
      REPOSITORY_ROOT,
      "python",
      "-c",
      DRAFT_2020_12_CHECK,
      schemaPath,
    ],
    {
      encoding: "utf8",
      input: JSON.stringify(records),
      maxBuffer: 1_048_576,
    },
  );
  assert.equal(
    validation.status,
    0,
    `Draft 2020-12 validation failed: ${validation.error?.message ?? validation.stderr}`,
  );
  return JSON.parse(validation.stdout) as boolean[];
}

function telemetry(compressedBytes: number) {
  return Object.freeze({
    dnsMs: 1,
    resolvedAddressCount: 2,
    selectedAddressFamily: 4 as const,
    connectMs: 2,
    responseMs: 3,
    totalMs: 6,
    compressedBytes,
    tlsProtocol: "TLSv1.3",
    tlsCipher: "TLS_AES_256_GCM_SHA384",
  });
}

function responseFor(
  payload: unknown = VALID_PAYLOAD,
  options: {
    readonly status?: number;
    readonly headers?: Readonly<Record<string, string>>;
    readonly gzip?: boolean;
    readonly body?: Uint8Array;
  } = {},
): FixedHttpsResponse {
  const plain = options.body ?? Buffer.from(JSON.stringify(payload), "utf8");
  const body = options.gzip === true ? gzipSync(plain) : plain;
  return {
    status: options.status ?? 200,
    headers: Object.freeze({
      "content-type": "application/json",
      ...(options.gzip === true ? { "content-encoding": "gzip" } : {}),
      ...options.headers,
    }),
    body,
    telemetry: telemetry(body.byteLength),
  };
}

function sequenceTransport(
  responses: readonly (FixedHttpsResponse | Error)[],
  observedUrls: string[] = [],
): FixedHttpsTransport {
  let index = 0;
  return async ({ policy, url }) => {
    assert.equal(policy, ONS_EGRESS_POLICY);
    observedUrls.push(url);
    const response = responses[index++];
    if (response === undefined) assert.fail("mock transport was called too many times");
    if (response instanceof Error) throw response;
    return response;
  };
}

async function expectFault(
  run: () => Promise<unknown>,
  code: ProviderAdapterFault["code"],
): Promise<ProviderAdapterFault> {
  let captured: ProviderAdapterFault | undefined;
  await assert.rejects(run, (error: unknown) => {
    assert.ok(error instanceof ProviderAdapterFault);
    assert.equal(error.code, code);
    captured = error;
    return true;
  });
  assert.ok(captured);
  return captured;
}

test("is default-suspended on both independent lifecycle planes", async () => {
  let calls = 0;
  const adapter = createOnsDataApiAdapter({
    transport: async () => {
      calls += 1;
      return responseFor();
    },
  });
  assert.deepEqual(adapter.health(), {
    adapterId: "gis-ai-go.ons-data-api",
    discovery: "suspended",
    invocation: "suspended",
    network: "not-checked",
  });
  assert.throws(
    () => adapter.describe(),
    (error: unknown) =>
      error instanceof ProviderAdapterFault && error.code === "ADAPTER_DISCOVERY_SUSPENDED",
  );
  await expectFault(() => adapter.execute(ONS_ADAPTER_REQUEST), "ADAPTER_INVOCATION_SUSPENDED");
  assert.equal(calls, 0);

  const discoverable = createOnsDataApiAdapter({
    lifecycle: { discovery: "active", invocation: "suspended", reason: "Discovery test." },
  });
  assert.equal(discoverable.describe().lifecycle.invocation, "suspended");
  const invocable = createOnsDataApiAdapter({
    lifecycle: { discovery: "suspended", invocation: "active", reason: "Invocation test." },
    transport: sequenceTransport([responseFor()]),
  });
  assert.throws(() => invocable.describe(), ProviderAdapterFault);
  assert.equal((await invocable.execute(ONS_ADAPTER_REQUEST)).observations.length, 1);
});

test("describes exact version, bounds and upper-bound estimate without a network check", () => {
  const adapter = createOnsDataApiAdapter({ lifecycle: ACTIVE });
  const description = adapter.describe();
  assert.equal(description.adapterId, "gis-ai-go.ons-data-api");
  assert.deepEqual(description.providerVersion, {
    providerId: "ons-data-api",
    datasetId: "weekly-deaths-region",
    edition: "time-series",
    version: "121",
    versionUri:
      "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121",
    sourceDate: "2026-07-01",
    dimensionOrder: ["time", "geography", "week", "causeofdeath"],
  });
  assert.deepEqual(description.egress, ONS_EGRESS_POLICY);
  assert.deepEqual(adapter.estimate(ONS_ADAPTER_REQUEST), {
    confidence: "upper-bound",
    maxObservations: 1,
    maxAttempts: 2,
    maxCompressedResponseBytes: 262_144,
    maxDecompressedResponseBytes: 1_048_576,
    maxCanonicalResponseBytes: 262_144,
  });
});

test("constructs only the fixed URL and returns deterministic native evidence", async () => {
  const urls: string[] = [];
  const attempts: OnsAttemptTelemetry[] = [];
  const adapter = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: sequenceTransport([responseFor(), responseFor()], urls),
    onAttempt: (entry) => attempts.push(entry),
  });
  const first = await adapter.execute(ONS_ADAPTER_REQUEST);
  const reordered = {
    selections: ONS_ADAPTER_REQUEST.selections.map(({ dimension, option }) => ({ option, dimension })),
    dataset: { version: "121", id: "weekly-deaths-region", edition: "time-series" },
  };
  const second = await adapter.execute(reordered);
  assert.deepEqual(urls, [ONS_OBSERVATION_URI, ONS_OBSERVATION_URI]);
  assert.deepEqual(first, second);
  assert.deepEqual(first.dimensions, ONS_ADAPTER_REQUEST.selections);
  assert.deepEqual(first.observations, [
    {
      value: "12345",
      unit: null,
      metadata: [{ name: "Data Marking", value: "" }],
    },
  ]);
  assert.equal(first.dataset.version, "121");
  assert.equal(first.rights.licence, "Open Government Licence v3.0");
  assert.deepEqual(first.rights.exceptions, [
    "The ONS logo is excluded and is not retrieved or redistributed.",
    "Any record-level third-party exception overrides this general evidence and must fail closed.",
    "The selected aggregate dataset page stated no additional exception when reviewed.",
  ]);
  assert.equal(first.provenance.sourceUri, ONS_OBSERVATION_URI);
  assert.equal(first.provenance.synthetic, false);
  assert.deepEqual(serialiseProviderAdapterResult(first), serialiseProviderAdapterResult(second));
  assert.deepEqual(digestProviderAdapterResult(first), digestProviderAdapterResult(second));
  assert.equal(attempts.length, 2);
  assert.equal(JSON.stringify(attempts).includes("12345"), false);
  assert.equal(Object.isFrozen(first), true);
});

test("keeps the checked-in live evidence privacy-safe and deterministically bound", async () => {
  const record = JSON.parse(
    readFileSync(
      new URL("../../../../providers/ons/data-api-adapter-live-probe.v1.json", import.meta.url),
      "utf8",
    ),
  ) as Record<string, any>;
  assert.equal(record.status, "passed");
  assert.equal(record.payloadStored, false);
  assert.equal(record.credentialsUsed, false);
  assert.equal(record.providerVersion.datasetId, "weekly-deaths-region");
  assert.equal(record.providerVersion.version, "121");
  assert.equal(record.rights.licence, "Open Government Licence v3.0");
  assert.equal(record.result.digest.domain, "gis-ai-go.provider-adapter-result.v1");
  assert.equal(
    record.result.digest.sha256,
    "309a7c0a374f93f20d4b4cc8aaa4530c4a828ea27e4e26e266b367e59b7da3bd",
  );
  assert.equal(record.result.canonicalBytes, 2399);
  const observedPayload = mutable(VALID_PAYLOAD);
  observedPayload.observations[0]!.observation = "10471";
  const reproduced = await createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: sequenceTransport([responseFor(observedPayload)]),
  }).execute(ONS_ADAPTER_REQUEST);
  assert.deepEqual(record.result, {
    digest: digestProviderAdapterResult(reproduced),
    canonicalBytes: serialiseProviderAdapterResult(reproduced).byteLength,
  });
  const missingExceptions = mutable<unknown>(reproduced) as {
    rights: { exceptions?: unknown };
  };
  delete missingExceptions.rights.exceptions;
  assert.deepEqual(
    draft202012Validity(PROVIDER_RESULT_SCHEMA, [reproduced, missingExceptions]),
    [true, false],
  );
  const serialised = JSON.stringify(record);
  for (const forbidden of [
    "10471",
    '"observations"',
    '"responseBody"',
    '"remoteAddress"',
    "/Users/",
    "/private/tmp/",
    "Bearer ",
  ]) {
    assert.equal(serialised.includes(forbidden), false);
  }
});

test("rejects caller URL/query, stale versions, wrong selection order and alternate options", async () => {
  let calls = 0;
  const adapter = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: async () => {
      calls += 1;
      return responseFor();
    },
  });
  const invalid = [
    { ...ONS_ADAPTER_REQUEST, url: "https://example.invalid" },
    { ...ONS_ADAPTER_REQUEST, query: "time=*" },
    {
      ...ONS_ADAPTER_REQUEST,
      dataset: { ...ONS_ADAPTER_REQUEST.dataset, version: "122" },
    },
    {
      ...ONS_ADAPTER_REQUEST,
      selections: [
        ONS_ADAPTER_REQUEST.selections[1],
        ONS_ADAPTER_REQUEST.selections[0],
        ...ONS_ADAPTER_REQUEST.selections.slice(2),
      ],
    },
    {
      ...ONS_ADAPTER_REQUEST,
      selections: ONS_ADAPTER_REQUEST.selections.map((selection, index) =>
        index === 2 ? { ...selection, option: "week-25" } : selection,
      ),
    },
    new Proxy(ONS_ADAPTER_REQUEST, {}),
  ];
  for (const request of invalid) await assert.rejects(() => adapter.execute(request));
  assert.equal(calls, 0);
  const stale = await expectFault(() => adapter.execute(invalid[2]), "STALE_PROVIDER_VERSION");
  assert.equal(stale.retryable, false);
});

test("retries only the closed status set and bounded Retry-After", async () => {
  const sleeps: number[] = [];
  const adapter = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: sequenceTransport([
      responseFor(null, { status: 503, headers: { "retry-after": "1" } }),
      responseFor(),
    ]),
    sleep: async (milliseconds) => {
      sleeps.push(milliseconds);
    },
  });
  assert.equal((await adapter.execute(ONS_ADAPTER_REQUEST)).observations[0]?.value, "12345");
  assert.deepEqual(sleeps, [1_000]);

  let tooLongCalls = 0;
  const tooLong = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: async () => {
      tooLongCalls += 1;
      return responseFor(null, { status: 429, headers: { "retry-after": "61" } });
    },
    sleep: async () => assert.fail("overlong Retry-After must not be slept"),
  });
  const rate = await expectFault(() => tooLong.execute(ONS_ADAPTER_REQUEST), "PROVIDER_RATE_LIMITED");
  assert.equal(rate.providerStatus, 429);
  assert.equal(tooLongCalls, 1);

  let redirectCalls = 0;
  const redirect = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: async () => {
      redirectCalls += 1;
      return responseFor(null, { status: 302, headers: { location: "https://evil.invalid" } });
    },
  });
  const outage = await expectFault(() => redirect.execute(ONS_ADAPTER_REQUEST), "PROVIDER_OUTAGE");
  assert.equal(outage.providerStatus, 302);
  assert.equal(outage.retryable, false);
  assert.equal(redirectCalls, 1);
});

test("brands only network and HTTP 500 to 599 faults for approved-cache use", async () => {
  const exactAdapter = createOnsDataApiAdapter({ lifecycle: ACTIVE });
  assert.equal(requireExactOnsDataApiAdapter(exactAdapter), exactAdapter);
  assert.equal(requirePristineOnsDataApiAdapter(exactAdapter), exactAdapter);
  const substitutedAdapter = createOnsDataApiAdapter({ lifecycle: ACTIVE });
  Object.defineProperty(substitutedAdapter, "execute", {
    configurable: true,
    value: async () => {
      throw new Error("substituted adapter execution must not run");
    },
  });
  assert.equal(requireExactOnsDataApiAdapter(substitutedAdapter), substitutedAdapter);
  assert.throws(
    () => requirePristineOnsDataApiAdapter(substitutedAdapter),
    /not pristine/u,
  );
  let adapterProxyTraps = 0;
  const proxiedAdapter = new Proxy(exactAdapter, {
    getPrototypeOf: () => {
      adapterProxyTraps += 1;
      throw new Error("adapter proxy must not be traversed");
    },
    ownKeys: () => {
      adapterProxyTraps += 1;
      throw new Error("adapter proxy must not be traversed");
    },
  });
  assert.throws(() => requireExactOnsDataApiAdapter(proxiedAdapter), /not exact/u);
  assert.throws(() => requirePristineOnsDataApiAdapter(proxiedAdapter), /not pristine/u);
  assert.equal(adapterProxyTraps, 0);
  class SubclassedAdapter extends OnsDataApiAdapter {}
  assert.throws(
    () => new SubclassedAdapter({ lifecycle: ACTIVE }),
    /subclassing is not supported/u,
  );

  for (const code of [
    "HPE_INVALID_HEADER_TOKEN",
    "HPE_HEADER_OVERFLOW",
    "HPE_INVALID_CHUNK_SIZE",
    "HPE_STRICT",
  ]) {
    const parserError = Object.assign(new Error("provider response parse failure"), { code });
    assert.equal(
      normaliseFixedHttpsRequestError(parserError).kind,
      "invalid-response-framing",
    );
  }
  for (const code of [
    "EAI_AGAIN",
    "ENOTFOUND",
    "ECONNREFUSED",
    "ECONNRESET",
    "ERR_TLS_CERT_ALTNAME_INVALID",
    "CERT_HAS_EXPIRED",
    "UNABLE_TO_VERIFY_LEAF_SIGNATURE",
  ]) {
    const networkError = Object.assign(new Error("network failure"), { code });
    assert.equal(normaliseFixedHttpsRequestError(networkError).kind, "network");
  }
  let codeReads = 0;
  const accessorError = new Error("opaque accessor failure");
  Object.defineProperty(accessorError, "code", {
    get: () => {
      codeReads += 1;
      return "ECONNRESET";
    },
  });
  assert.equal(normaliseFixedHttpsRequestError(accessorError).kind, "unclassified");
  assert.equal(codeReads, 0);
  let descriptorTraps = 0;
  const errorProxy = new Proxy(new Error("opaque proxy failure"), {
    getOwnPropertyDescriptor: () => {
      descriptorTraps += 1;
      throw new Error("request-error proxy must not escape closed classification");
    },
  });
  assert.equal(normaliseFixedHttpsRequestError(errorProxy).kind, "unclassified");
  assert.equal(descriptorTraps, 0);
  const transparentProxy = new Proxy(
    Object.assign(new Error("transparent proxy failure"), { code: "ECONNRESET" }),
    {},
  );
  assert.equal(normaliseFixedHttpsRequestError(transparentProxy).kind, "unclassified");
  const directTransportError = new FixedHttpsTransportError("network");
  assert.equal(isExactFixedHttpsTransportError(directTransportError), false);
  assert.equal(normaliseFixedHttpsRequestError(directTransportError).kind, "unclassified");
  const publicSdk = await import("../src/index.js");
  assert.equal("normaliseFixedHttpsRequestError" in publicSdk, false);
  assert.equal("isExactFixedHttpsTransportError" in publicSdk, false);
  class SubclassedTransportError extends FixedHttpsTransportError {}
  assert.equal(
    normaliseFixedHttpsRequestError(new SubclassedTransportError("network")).kind,
    "unclassified",
  );
  const prototypeForgery = Object.assign(
    Object.create(FixedHttpsTransportError.prototype) as object,
    { kind: "network" },
  );
  assert.equal(normaliseFixedHttpsRequestError(prototypeForgery).kind, "unclassified");

  for (const status of [500, 503, 504, 599]) {
    const candidate = createOnsDataApiAdapter({
      lifecycle: ACTIVE,
      transport: async () => responseFor(null, {
        status,
        headers: { "retry-after": "0" },
      }),
      sleep: async () => undefined,
    });
    const execution = executePristineOnsDataApiAdapter(
      candidate,
      ONS_ADAPTER_REQUEST,
      {},
    );
    const fault = await expectFault(
      () => execution.result,
      "PROVIDER_OUTAGE",
    );
    const normalised = candidate.normalise_error(fault);
    assert.deepEqual(
      execution.approvedCacheOutage(fault, normalised),
      {
        source: "http-5xx",
        providerStatus: status,
        retryable: ONS_EGRESS_POLICY.retryableStatuses.includes(status),
      },
    );
    assert.equal(execution.approvedCacheOutage(fault, normalised), null);
  }

  const tamperedCandidate = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: async () => responseFor(null, { status: 599 }),
  });
  const tamperedExecution = executePristineOnsDataApiAdapter(
    tamperedCandidate,
    ONS_ADAPTER_REQUEST,
    {},
  );
  const tamperedFault = await expectFault(
    () => tamperedExecution.result,
    "PROVIDER_OUTAGE",
  );
  const correctTamperedNormalisation = tamperedCandidate.normalise_error(tamperedFault);
  assert.equal(
    tamperedExecution.approvedCacheOutage(tamperedFault, {
      ...correctTamperedNormalisation,
      providerStatus: 500,
    }),
    null,
  );
  assert.equal(
    tamperedExecution.approvedCacheOutage(
      tamperedFault,
      correctTamperedNormalisation,
    ),
    null,
  );

  const outerClockFailure = new Error("outer execution clock failed");
  let nestedResult: Promise<ProviderAdapterResult> | undefined;
  let startNestedExecution = true;
  const executionCandidate = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: async () => responseFor(null, { status: 599 }),
    now: () => {
      if (startNestedExecution) {
        startNestedExecution = false;
        nestedResult = executionCandidate.execute(ONS_ADAPTER_REQUEST);
        throw outerClockFailure;
      }
      return Date.parse("2026-08-22T12:00:00Z");
    },
  });
  const outerExecution = executePristineOnsDataApiAdapter(
    executionCandidate,
    ONS_ADAPTER_REQUEST,
    {},
  );
  await assert.rejects(
    outerExecution.result,
    (error: unknown) => error === outerClockFailure,
  );
  assert.ok(nestedResult);
  const capturedNestedResult = nestedResult;
  const nestedFault = await expectFault(
    () => capturedNestedResult,
    "PROVIDER_OUTAGE",
  );
  assert.equal(
    outerExecution.approvedCacheOutage(
      nestedFault,
      executionCandidate.normalise_error(nestedFault),
    ),
    null,
  );

  for (const status of [302, 401, 403, 451, 499, 600]) {
    const candidate = createOnsDataApiAdapter({
      lifecycle: ACTIVE,
      transport: async () => responseFor(null, { status }),
    });
    const execution = executePristineOnsDataApiAdapter(
      candidate,
      ONS_ADAPTER_REQUEST,
      {},
    );
    const fault = await expectFault(
      () => execution.result,
      "PROVIDER_OUTAGE",
    );
    assert.equal(
      execution.approvedCacheOutage(
        fault,
        candidate.normalise_error(fault),
      ),
      null,
    );
  }

  const rateLimited = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: async () => responseFor(null, {
      status: 429,
      headers: { "retry-after": "61" },
    }),
  });
  const rateExecution = executePristineOnsDataApiAdapter(
    rateLimited,
    ONS_ADAPTER_REQUEST,
    {},
  );
  const rateFault = await expectFault(
    () => rateExecution.result,
    "PROVIDER_RATE_LIMITED",
  );
  assert.equal(
    rateExecution.approvedCacheOutage(
      rateFault,
      rateLimited.normalise_error(rateFault),
    ),
    null,
  );

  for (const [kind, expected] of [
    ["network", "PROVIDER_OUTAGE"],
    ["unsafe-address", "PROVIDER_OUTAGE"],
    ["aborted", "PROVIDER_TIMEOUT"],
    ["connect-timeout", "PROVIDER_TIMEOUT"],
    ["response-timeout", "PROVIDER_TIMEOUT"],
    ["response-too-large", "MALFORMED_PROVIDER_RESPONSE"],
    ["invalid-response-framing", "MALFORMED_PROVIDER_RESPONSE"],
    ["invalid-response-headers", "MALFORMED_PROVIDER_RESPONSE"],
    ["unclassified", "PROVIDER_OUTAGE"],
  ] as const) {
    const candidate = createOnsDataApiAdapter({
      lifecycle: ACTIVE,
      transport: async () => {
        throw new FixedHttpsTransportError(kind);
      },
    });
    const execution = executePristineOnsDataApiAdapter(
      candidate,
      ONS_ADAPTER_REQUEST,
      {},
    );
    const fault = await expectFault(() => execution.result, expected);
    const normalised = candidate.normalise_error(fault);
    assert.deepEqual(
      execution.approvedCacheOutage(fault, normalised),
      null,
    );
  }

  const opaque = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: async () => {
      throw new Error("opaque transport failure");
    },
  });
  const opaqueExecution = executePristineOnsDataApiAdapter(
    opaque,
    ONS_ADAPTER_REQUEST,
    {},
  );
  const opaqueFault = await expectFault(
    () => opaqueExecution.result,
    "PROVIDER_OUTAGE",
  );
  assert.equal(
    opaqueExecution.approvedCacheOutage(
      opaqueFault,
      opaque.normalise_error(opaqueFault),
    ),
    null,
  );

  const manual = new ProviderAdapterFault("PROVIDER_OUTAGE", {
    providerStatus: 503,
    retryable: true,
  });
  const manualAdapter = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    now: () => {
      throw manual;
    },
  });
  const manualExecution = executePristineOnsDataApiAdapter(
    manualAdapter,
    ONS_ADAPTER_REQUEST,
    {},
  );
  const manualFault = await expectFault(() => manualExecution.result, "PROVIDER_OUTAGE");
  assert.equal(manualFault, manual);
  assert.equal(
    manualExecution.approvedCacheOutage(
      manualFault,
      manualAdapter.normalise_error(manualFault),
    ),
    null,
  );
});

test("builds schema-valid passed evidence from actual 503 to 200 telemetry", async () => {
  const attempts: OnsAttemptTelemetry[] = [];
  const adapter = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: sequenceTransport([
      responseFor(null, { status: 503, headers: { "retry-after": "0" } }),
      responseFor(),
    ]),
    sleep: async () => undefined,
    onAttempt: (entry) => attempts.push(entry),
  });
  const result = await adapter.execute(ONS_ADAPTER_REQUEST);
  const retryAttempt = attempts[0];
  const successfulAttempt = attempts[1];
  if (retryAttempt?.outcome !== "response" || successfulAttempt?.outcome !== "response") {
    assert.fail("expected two response telemetry entries");
  }
  assert.equal(retryAttempt.status, 503);
  assert.equal(retryAttempt.decompressedBytes, null);
  assert.equal(successfulAttempt.status, 200);
  assert.equal(typeof successfulAttempt.decompressedBytes, "number");

  const record = buildOnsLiveProbeRecord({
    observedAt: "2030-01-01T00:00:00Z",
    durationMs: 10,
    description: adapter.describe(),
    rights: adapter.licence_evidence(),
    result,
    attempts,
  });
  const serialised = JSON.stringify(record);
  assert.equal(serialised.includes("12345"), false);
  assert.equal(serialised.includes('"observations"'), false);

  const missingSuccessfulBytes = mutable<unknown>(record) as {
    attempts: Array<{ decompressedBytes: number | null }>;
  };
  missingSuccessfulBytes.attempts[1]!.decompressedBytes = null;
  const inventedRetryBytes = mutable<unknown>(record) as {
    attempts: Array<{ decompressedBytes: number | null }>;
  };
  inventedRetryBytes.attempts[0]!.decompressedBytes = 0;
  assert.deepEqual(
    draft202012Validity(LIVE_PROBE_SCHEMA, [
      record,
      missingSuccessfulBytes,
      inventedRetryBytes,
    ]),
    [true, false, false],
  );
});

test("bounds transport retries", async () => {
  let transportCalls = 0;
  const failing = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: async () => {
      transportCalls += 1;
      throw new FixedHttpsTransportError("network");
    },
  });
  await expectFault(() => failing.execute(ONS_ADAPTER_REQUEST), "PROVIDER_OUTAGE");
  assert.equal(transportCalls, 2);
});

test("shares the in-flight admission limit across adapter instances", async () => {
  let release: (() => void) | undefined;
  const deferred = new Promise<void>((resolve) => {
    release = resolve;
  });
  const firstTransport: FixedHttpsTransport = async () => {
    await deferred;
    return responseFor();
  };
  let secondTransportCalls = 0;
  const secondTransport: FixedHttpsTransport = async () => {
    secondTransportCalls += 1;
    return responseFor();
  };
  const firstAdapter = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: firstTransport,
  });
  const secondAdapter = new OnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: secondTransport,
  });
  const first = firstAdapter.execute(ONS_ADAPTER_REQUEST);
  await expectFault(() => secondAdapter.execute(ONS_ADAPTER_REQUEST), "PROVIDER_RATE_LIMITED");
  assert.equal(secondTransportCalls, 0);
  release!();
  await first;
});

test("prevents the 60-attempt two-instance bypass and ignores caller deadline clocks", async () => {
  let transportCalls = 0;
  const firstTransport: FixedHttpsTransport = async () => {
    transportCalls += 1;
    return responseFor();
  };
  const secondTransport: FixedHttpsTransport = async () => {
    transportCalls += 1;
    return responseFor();
  };
  const firstAdapter = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: firstTransport,
  });
  const secondAdapter = new OnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: secondTransport,
  });
  let accepted = 0;
  let rateLimited = 0;
  for (let index = 0; index < 60; index += 1) {
    const adapter = index % 2 === 0 ? firstAdapter : secondAdapter;
    try {
      await adapter.execute(ONS_ADAPTER_REQUEST);
      accepted += 1;
    } catch (error) {
      if (!(error instanceof ProviderAdapterFault) || error.code !== "PROVIDER_RATE_LIMITED") {
        throw error;
      }
      rateLimited += 1;
    }
  }
  assert.equal(accepted, 30);
  assert.equal(rateLimited, 30);
  assert.equal(transportCalls, 30);

  const callerClockCannotReset = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    now: () => Number.MAX_SAFE_INTEGER,
    transport: async () => {
      transportCalls += 1;
      return responseFor();
    },
  });
  await expectFault(
    () => callerClockCannotReset.execute(ONS_ADAPTER_REQUEST),
    "PROVIDER_RATE_LIMITED",
  );
  assert.equal(transportCalls, 30);
  processAdmissionNow += 60_001;
  await secondAdapter.execute(ONS_ADAPTER_REQUEST);
  assert.equal(transportCalls, 31);
});

test("normalises transport timeouts and never reflects hostile provider detail", async () => {
  const secret = "secret-provider-token-and-path";
  const timeout = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: sequenceTransport([new FixedHttpsTransportError("response-timeout"), responseFor()]),
  });
  assert.equal((await timeout.execute(ONS_ADAPTER_REQUEST)).observations.length, 1);

  const aborted = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: sequenceTransport([new FixedHttpsTransportError("aborted")]),
  });
  const controller = new AbortController();
  controller.abort(secret);
  const fault = await expectFault(
    () => aborted.execute(ONS_ADAPTER_REQUEST, { signal: controller.signal }),
    "PROVIDER_TIMEOUT",
  );
  assert.equal(fault.retryable, false);
  assert.doesNotMatch(JSON.stringify(aborted.normalise_error(new Error(secret))), new RegExp(secret));
});

test("propagates EXEC deadline and cancellation without consuming a pre-start attempt", async () => {
  let calls = 0;
  let now = Date.parse("2026-08-20T20:00:00Z");
  const adapter = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    now: () => now,
    transport: async () => {
      calls += 1;
      return responseFor();
    },
  });
  await expectFault(
    () =>
      adapter.execute(ONS_ADAPTER_REQUEST, {
        deadline: "2026-08-20T19:59:59Z",
      }),
    "PROVIDER_TIMEOUT",
  );
  await expectFault(
    () =>
      adapter.execute(ONS_ADAPTER_REQUEST, {
        deadline: "2026-02-30T20:00:00Z",
      }),
    "INVALID_REQUEST",
  );
  const controller = new AbortController();
  controller.abort();
  await expectFault(
    () => adapter.execute(ONS_ADAPTER_REQUEST, { signal: controller.signal }),
    "PROVIDER_TIMEOUT",
  );
  assert.equal(calls, 0);

  for (let index = 0; index < 30; index += 1) await adapter.execute(ONS_ADAPTER_REQUEST);
  assert.equal(calls, 30);
  await expectFault(() => adapter.execute(ONS_ADAPTER_REQUEST), "PROVIDER_RATE_LIMITED");
  processAdmissionNow += 60_001;
  now += 60_001;
  await adapter.execute(ONS_ADAPTER_REQUEST);
});

test("cancels an active transport or retry backoff and does not start another attempt", async () => {
  let transportCalls = 0;
  const transportController = new AbortController();
  const activeTransport = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: async ({ signal }) => {
      transportCalls += 1;
      return await new Promise<FixedHttpsResponse>((_resolve, reject) => {
        signal?.addEventListener(
          "abort",
          () => reject(new FixedHttpsTransportError("aborted")),
          { once: true },
        );
      });
    },
  });
  const active = activeTransport.execute(ONS_ADAPTER_REQUEST, {
    signal: transportController.signal,
  });
  transportController.abort();
  await expectFault(() => active, "PROVIDER_TIMEOUT");
  assert.equal(transportCalls, 1);

  let backoffCalls = 0;
  const backoffController = new AbortController();
  const backoff = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: async () => {
      backoffCalls += 1;
      return responseFor(null, { status: 503, headers: { "retry-after": "5" } });
    },
    sleep: async (_milliseconds, signal) => {
      backoffController.abort();
      if (signal?.aborted === true) throw new ProviderAdapterFault("PROVIDER_TIMEOUT");
    },
  });
  await expectFault(
    () => backoff.execute(ONS_ADAPTER_REQUEST, { signal: backoffController.signal }),
    "PROVIDER_TIMEOUT",
  );
  assert.equal(backoffCalls, 1);

  let defaultBackoffCalls = 0;
  const defaultBackoffController = new AbortController();
  const defaultBackoff = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: async () => {
      defaultBackoffCalls += 1;
      return responseFor(null, { status: 503, headers: { "retry-after": "5" } });
    },
  });
  const pending = defaultBackoff.execute(ONS_ADAPTER_REQUEST, {
    signal: defaultBackoffController.signal,
  });
  setTimeout(() => defaultBackoffController.abort(), 5);
  await expectFault(() => pending, "PROVIDER_TIMEOUT");
  assert.equal(defaultBackoffCalls, 1);
});

test("does not sleep when Retry-After cannot leave one complete attempt inside the deadline", async () => {
  let calls = 0;
  let sleeps = 0;
  const adapter = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    now: () => Date.parse("2026-08-20T20:00:00Z"),
    transport: async () => {
      calls += 1;
      return responseFor(null, { status: 503, headers: { "retry-after": "5" } });
    },
    sleep: async () => {
      sleeps += 1;
    },
  });
  await expectFault(
    () =>
      adapter.execute(ONS_ADAPTER_REQUEST, {
        deadline: "2026-08-20T20:00:10Z",
      }),
    "PROVIDER_OUTAGE",
  );
  assert.equal(calls, 1);
  assert.equal(sleeps, 0);
});

test("accepts gzip and rejects media, encoding, UTF-8 and decompression attacks", async () => {
  const compressed = createOnsDataApiAdapter({
    lifecycle: ACTIVE,
    transport: sequenceTransport([responseFor(VALID_PAYLOAD, { gzip: true })]),
  });
  assert.equal((await compressed.execute(ONS_ADAPTER_REQUEST)).observations.length, 1);

  const invalidResponses = [
    responseFor(VALID_PAYLOAD, { headers: { "content-type": "text/html" } }),
    responseFor(VALID_PAYLOAD, { headers: { "content-encoding": "br" } }),
    responseFor(VALID_PAYLOAD, {
      headers: { "content-encoding": "gzip" },
      body: Buffer.from("not-gzip", "utf8"),
    }),
    responseFor(null, { body: Uint8Array.from([0xc3, 0x28]) }),
    responseFor(null, {
      body: Buffer.from('{"x":1,"\\u0078":2}', "utf8"),
    }),
    responseFor(null, {
      body: gzipSync(Buffer.alloc(ONS_EGRESS_POLICY.maxDecompressedBytes + 1, 0x20)),
      headers: { "content-encoding": "gzip" },
    }),
    responseFor(null, {
      body: Buffer.alloc(ONS_EGRESS_POLICY.maxCompressedBytes + 1),
    }),
    responseFor(VALID_PAYLOAD, { headers: { "content-length": "1" } }),
  ];
  for (const response of invalidResponses) {
    const adapter = createOnsDataApiAdapter({
      lifecycle: ACTIVE,
      transport: sequenceTransport([response]),
    });
    await expectFault(() => adapter.execute(ONS_ADAPTER_REQUEST), "MALFORMED_PROVIDER_RESPONSE");
  }
});

test("fails closed on schema, version, native-ID, link and rights drift", async () => {
  const variants: { readonly payload: unknown; readonly code: ProviderAdapterFault["code"] }[] = [];

  const extra = mutable(VALID_PAYLOAD) as Record<string, unknown>;
  extra.extra = "unexpected";
  variants.push({ payload: extra, code: "MALFORMED_PROVIDER_RESPONSE" });

  const wrongVersion = mutable(VALID_PAYLOAD);
  wrongVersion.links.version.id = "122";
  variants.push({ payload: wrongVersion, code: "STALE_PROVIDER_VERSION" });

  const wrongId = mutable(VALID_PAYLOAD);
  wrongId.dimensions.geography.option.id = "E92000002";
  variants.push({ payload: wrongId, code: "MALFORMED_PROVIDER_RESPONSE" });

  const wrongLink = mutable(VALID_PAYLOAD);
  wrongLink.links.self.href = "https://evil.invalid/steal";
  variants.push({ payload: wrongLink, code: "MALFORMED_PROVIDER_RESPONSE" });

  const marked = mutable(VALID_PAYLOAD);
  marked.observations[0]!.metadata["Data Marking"] = "third-party";
  variants.push({ payload: marked, code: "RIGHTS_UNKNOWN" });

  const twoRows = mutable(VALID_PAYLOAD);
  twoRows.observations.push(mutable(twoRows.observations[0]!));
  (twoRows as { total_observations: number }).total_observations = 2;
  variants.push({ payload: twoRows, code: "MALFORMED_PROVIDER_RESPONSE" });

  for (const { payload, code } of variants) {
    const adapter = createOnsDataApiAdapter({
      lifecycle: ACTIVE,
      transport: sequenceTransport([responseFor(payload)]),
    });
    await expectFault(() => adapter.execute(ONS_ADAPTER_REQUEST), code);
  }
});
