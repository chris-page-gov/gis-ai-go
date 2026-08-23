import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { Resolver } from "node:dns/promises";
import { mkdtempSync, readFileSync, readdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  CANONICAL_DOMAINS,
  EvidenceReconciliationIndexError,
  PUBLIC_READ_ONS_RESOURCE,
  PublicEvidenceLedger,
  canonicalJson,
  domainSeparatedSha256,
  openEvidenceReconciliationIndex,
  verifyPublicReadReceipt,
} from "@gis-ai-go/evidence";
import {
  ApprovedOnsDataQueryCache,
  FixedHttpsTransportError,
  ONS_ADAPTER_REQUEST,
  ONS_EGRESS_POLICY,
  OnsDataApiAdapter,
  ProviderAdapterFault,
  createApprovedOnsDataQueryCache,
  executePristineOnsDataApiAdapter,
  type AdapterLifecycle,
  type FixedHttpsResponse,
  type FixedHttpsTransport,
  type ProviderAdapterExecutionOptions,
  type ProviderAdapterQuery,
  type ProviderAdapterResult,
} from "@gis-ai-go/provider-adapter-sdk";
import { PUBLIC_READ_POLICY } from "@gis-ai-go/policy-client";

import {
  APPROVED_CACHE_WARNING,
  DataQueryApplicationError,
  PUBLIC_ONS_DATA_QUERY_PARAMETERS,
  createDataQueryApplication,
  type DataQueryApplicationOptions,
  type DataQueryProblemCode,
  type DataQueryReconciliationProblemCode,
} from "../src/data-query-application.js";

const SOFTWARE = Object.freeze({
  name: "gis-ai-go-mcp-gateway",
  version: "0.1.0",
  revision: "e1fc1cbe69ea72c9aa310607d80f392ef56b0d58",
} as const);

const CONTEXT = Object.freeze({
  requestId: "request-data-query-application-1",
  traceId: "7123456789abcdef0123456789abcdef",
  trace: Object.freeze({
    traceparent:
      "00-7123456789abcdef0123456789abcdef-89abcdef01234567-01",
    tracestate: "govuk=public-read,ons=weekly-deaths",
  }),
  instance: "/data/query",
} as const);

const IDEMPOTENCY_KEY = `gis-ai-go:ik:v1:${"a".repeat(64)}`;

function reconciledRequest(key = IDEMPOTENCY_KEY) {
  return {
    schema: "gis-ai-go.data-query-request.v1" as const,
    idempotency_key: key,
    parameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
  };
}

const ACTIVE_INVOCATION = Object.freeze({
  discovery: "suspended",
  invocation: "active",
  reason: "Explicit application-only data query test.",
} as const);

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
        "http://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/" +
        "editions/time-series/versions/121/metadata",
    },
    self: {
      href:
        "http://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/" +
        "editions/time-series/versions/121/observations?causeofdeath=all-causes&" +
        "geography=E92000001&time=2026&week=week-24",
    },
    version: {
      href:
        "http://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/" +
        "editions/time-series/versions/121",
      id: "121",
    },
  },
  observations: [{ metadata: { "Data Marking": "" }, observation: "10471" }],
  offset: 0,
  total_observations: 1,
});

function mutable<T>(value: T): T {
  return JSON.parse(JSON.stringify(value)) as T;
}

function response(payload: unknown = VALID_PAYLOAD, status = 200): FixedHttpsResponse {
  const body = Buffer.from(JSON.stringify(payload), "utf8");
  return {
    status,
    headers: Object.freeze({ "content-type": "application/json" }),
    body,
    telemetry: Object.freeze({
      dnsMs: 1,
      resolvedAddressCount: 1,
      selectedAddressFamily: 4,
      connectMs: 2,
      responseMs: 3,
      totalMs: 6,
      compressedBytes: body.byteLength,
      tlsProtocol: "TLSv1.3",
      tlsCipher: "TLS_AES_256_GCM_SHA384",
    }),
  };
}

function transport(
  calls: { count: number; urls: string[] },
  payload: unknown = VALID_PAYLOAD,
): FixedHttpsTransport {
  return async ({ policy, url }) => {
    calls.count += 1;
    calls.urls.push(url);
    assert.equal(policy, ONS_EGRESS_POLICY);
    return response(payload);
  };
}

function adapter(
  calls: { count: number; urls: string[] } = { count: 0, urls: [] },
  lifecycle: AdapterLifecycle = ACTIVE_INVOCATION,
): OnsDataApiAdapter {
  return new OnsDataApiAdapter({
    lifecycle,
    transport: transport(calls),
    now: () => Date.parse("2030-01-01T00:00:00Z"),
  });
}

function application(
  injected: OnsDataApiAdapter,
  options: Partial<Omit<DataQueryApplicationOptions, "adapter" | "software">> = {},
) {
  return createDataQueryApplication({
    adapter: injected,
    software: SOFTWARE,
    now: () => new Date("2026-08-21T01:00:00.000Z"),
    ...options,
  });
}

function approvedCache() {
  const record = JSON.parse(
    readFileSync(
      new URL(
        "../../../../providers/ons/data-query-approved-cache.v1.json",
        import.meta.url,
      ),
      "utf8",
    ),
  );
  return createApprovedOnsDataQueryCache(record);
}

function malformedFixedHttpsGatewayProbe(): unknown {
  const gatewayModuleUrl = new URL("../src/data-query-application.js", import.meta.url).href;
  const providerModuleUrl = new URL(
    "../../../../packages/provider-adapter-sdk/dist/src/index.js",
    import.meta.url,
  ).href;
  const cacheUrl = new URL(
    "../../../../providers/ons/data-query-approved-cache.v1.json",
    import.meta.url,
  ).href;
  const probe = spawnSync(
    process.execPath,
    [
      "--input-type=module",
      "-e",
      `
        import https from "node:https";
        import http from "node:http";
        import dns from "node:dns/promises";
        import { readFileSync } from "node:fs";
        import { syncBuiltinESMExports } from "node:module";
        import { Duplex } from "node:stream";

        class ResponseSocket extends Duplex {
          sent = false;
          authorized = true;
          connecting = false;
          constructor(response) {
            super();
            this.response = response;
            Object.defineProperty(this, "remoteAddress", { value: "93.184.216.34" });
          }
          _read() {
            if (this.sent) return;
            this.sent = true;
            queueMicrotask(() => {
              this.push(Buffer.from(this.response, "latin1"));
              this.push(null);
            });
          }
          _write(_chunk, _encoding, callback) { callback(); }
          setTimeout() { return this; }
          setNoDelay() { return this; }
          setKeepAlive() { return this; }
          getProtocol() { return "TLSv1.3"; }
          getCipher() { return { name: "TLS_AES_256_GCM_SHA384" }; }
        }

        dns.Resolver.prototype.resolve4 = async function () { return ["93.184.216.34"]; };
        dns.Resolver.prototype.resolve6 = async function () { throw new Error("no IPv6"); };
        let wireResponse = "";
        let requestCount = 0;
        https.request = function (options, callback) {
          requestCount += 1;
          const socket = new ResponseSocket(wireResponse);
          const agent = new http.Agent();
          agent.createConnection = () => socket;
          const request = http.request({ ...options, protocol: "http:", agent }, callback);
          request.once("socket", () => queueMicrotask(() => socket.emit("secureConnect")));
          return request;
        };
        syncBuiltinESMExports();

        const gateway = await import(${JSON.stringify(gatewayModuleUrl)});
        const sdk = await import(${JSON.stringify(providerModuleUrl)});
        const cacheRecord = JSON.parse(readFileSync(new URL(${JSON.stringify(cacheUrl)}), "utf8"));
        const results = {};
        let index = 0;
        for (const [name, response] of [
          ["short-content-length", "HTTP/1.1 200 OK\\r\\nContent-Length: 10\\r\\n\\r\\nabc"],
          ["short-chunked", "HTTP/1.1 200 OK\\r\\nTransfer-Encoding: chunked\\r\\n\\r\\n3\\r\\nabc\\r\\n"],
          ["short-redirect", "HTTP/1.1 302 Found\\r\\nLocation: https://evil.invalid/\\r\\nContent-Length: 10\\r\\n\\r\\nabc"],
        ]) {
          index += 1;
          wireResponse = response;
          const before = requestCount;
          const adapter = new sdk.OnsDataApiAdapter({
            lifecycle: {
              discovery: "suspended",
              invocation: "active",
              reason: "Offline incomplete-response gateway probe.",
            },
            transport: sdk.fixedHttpsGet,
            sleep: async () => undefined,
          });
          const application = gateway.createDataQueryApplication({
            adapter,
            approvedCache: sdk.createApprovedOnsDataQueryCache(cacheRecord),
            software: {
              name: "gis-ai-go-mcp-gateway",
              version: "0.1.0",
              revision: "e1fc1cbe69ea72c9aa310607d80f392ef56b0d58",
            },
            now: () => new Date("2026-08-22T12:00:00.000Z"),
          });
          try {
            const result = await application.query(
              gateway.PUBLIC_ONS_DATA_QUERY_PARAMETERS,
              {
                requestId: "request-incomplete-response-" + index,
                traceId: String(index).repeat(32),
                instance: "/data/query",
              },
            );
            results[name] = {
              outcome: "result",
              cache: result.data.cache?.status ?? null,
              receipt: "evidence_receipt" in result,
              requests: requestCount - before,
            };
          } catch (error) {
            const serialised = JSON.stringify(error?.problem ?? null);
            results[name] = {
              outcome: "problem",
              code: error?.problem?.code ?? null,
              receipt: serialised.includes("receipt"),
              reflectedLocation: serialised.includes("evil.invalid"),
              requests: requestCount - before,
            };
          }
        }
        process.stdout.write(JSON.stringify(results));
      `,
    ],
    { encoding: "utf8", timeout: 5_000 },
  );
  assert.equal(probe.status, 0, probe.stderr);
  return JSON.parse(probe.stdout) as unknown;
}

async function expectProblem(
  run: () => Promise<unknown>,
  code: DataQueryProblemCode,
): Promise<DataQueryApplicationError> {
  let captured: DataQueryApplicationError | undefined;
  await assert.rejects(run, (error: unknown) => {
    assert.ok(error instanceof DataQueryApplicationError);
    assert.equal(error.problem.code, code);
    assert.equal(error.problem.schema, "gis-ai-go.data-query-problem.v1");
    const serialised = canonicalJson(error.problem);
    assert.equal(serialised.includes("receipt"), false);
    assert.equal(serialised.includes("providerStatus"), false);
    assert.equal(serialised.includes("stack"), false);
    captured = error;
    return true;
  });
  assert.ok(captured);
  return captured;
}

async function expectReconciliationProblem(
  run: () => Promise<unknown>,
  code: DataQueryReconciliationProblemCode,
): Promise<DataQueryApplicationError> {
  let captured: DataQueryApplicationError | undefined;
  await assert.rejects(run, (error: unknown) => {
    assert.ok(error instanceof DataQueryApplicationError);
    assert.equal(error.problem.code, code);
    assert.equal(
      error.problem.schema,
      "gis-ai-go.data-query-reconciliation-problem.v1",
    );
    assert.equal(error.problem.status, 409);
    const serialised = canonicalJson(error.problem);
    assert.equal(serialised.includes(IDEMPOTENCY_KEY), false);
    assert.equal(serialised.includes("receipt"), false);
    captured = error;
    return true;
  });
  assert.ok(captured);
  return captured;
}

function validAdapterResult(injected: OnsDataApiAdapter): ProviderAdapterResult {
  return {
    schema: "gis-ai-go.provider-adapter-result.v1",
    provider: {
      id: PUBLIC_READ_ONS_RESOURCE.provider.id,
      adapterId: PUBLIC_READ_ONS_RESOURCE.provider.adapter_id,
    },
    dataset: {
      id: PUBLIC_READ_ONS_RESOURCE.dataset.id,
      edition: PUBLIC_READ_ONS_RESOURCE.dataset.edition,
      version: PUBLIC_READ_ONS_RESOURCE.dataset.version,
      versionUri: PUBLIC_READ_ONS_RESOURCE.dataset.version_uri,
    },
    dimensions: PUBLIC_READ_ONS_RESOURCE.selections,
    observations: [
      {
        value: "10471",
        unit: null,
        metadata: [{ name: "Data Marking", value: "" }],
      },
    ],
    rights: injected.licence_evidence(),
    provenance: injected.provenance(),
  };
}

test("requires an explicitly injected exact ONS adapter and closed options", () => {
  assert.throws(
    () =>
      createDataQueryApplication({ software: SOFTWARE } as unknown as DataQueryApplicationOptions),
    /unexpected shape/u,
  );
  assert.throws(
    () =>
      createDataQueryApplication({
        adapter: {} as OnsDataApiAdapter,
        software: SOFTWARE,
      }),
    /explicitly injected ONS adapter/u,
  );
  assert.throws(
    () =>
      createDataQueryApplication({
        adapter: adapter(),
        software: SOFTWARE,
        unexpected: true,
      } as unknown as DataQueryApplicationOptions),
    /unexpected shape/u,
  );
  let getterCalls = 0;
  const exactPrototypeForgery = Object.create(
    ApprovedOnsDataQueryCache.prototype,
  ) as object;
  Object.defineProperty(exactPrototypeForgery, "read", {
    get: () => {
      getterCalls += 1;
      return () => null;
    },
  });
  Object.freeze(exactPrototypeForgery);
  const ownMethodForgery = Object.create(
    ApprovedOnsDataQueryCache.prototype,
  ) as object;
  Object.defineProperty(ownMethodForgery, "read", {
    configurable: true,
    value: () => null,
  });
  Object.freeze(ownMethodForgery);
  let proxyTraps = 0;
  const proxiedCache = new Proxy(approvedCache(), {
    getPrototypeOf: () => {
      proxyTraps += 1;
      throw new Error("cache proxy must not be traversed");
    },
    isExtensible: () => {
      proxyTraps += 1;
      throw new Error("cache proxy must not be traversed");
    },
  });
  class SubstitutedCache extends ApprovedOnsDataQueryCache {}
  for (const substitutedCache of [
    Object.freeze(Object.create(approvedCache())),
    Object.freeze(Object.create(ApprovedOnsDataQueryCache.prototype)),
    exactPrototypeForgery,
    ownMethodForgery,
    proxiedCache,
    new SubstitutedCache(
      JSON.parse(
        readFileSync(
          new URL(
            "../../../../providers/ons/data-query-approved-cache.v1.json",
            import.meta.url,
          ),
          "utf8",
        ),
      ),
    ),
  ] as unknown[]) {
    assert.throws(
      () =>
        createDataQueryApplication({
          adapter: adapter(),
          approvedCache: substitutedCache as ApprovedOnsDataQueryCache,
          software: SOFTWARE,
        }),
      /approved cache is invalid/u,
    );
  }
  assert.equal(getterCalls, 0);
  assert.equal(proxyTraps, 0);
});

test("executes one fixed query with discovery suspended and verified evidence", async () => {
  const calls = { count: 0, urls: [] as string[] };
  const injected = adapter(calls);
  const result = await application(injected).query(
    mutable(PUBLIC_ONS_DATA_QUERY_PARAMETERS),
    CONTEXT,
  );
  assert.equal(calls.count, 1);
  assert.deepEqual(calls.urls, [
    "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/" +
      "editions/time-series/versions/121/observations?time=2026&" +
      "geography=E92000001&week=week-24&causeofdeath=all-causes",
  ]);
  assert.deepEqual(result.data, {
    status: "succeeded",
    observations: [{ value: "10471", unit: null }],
  });
  assert.equal(result.evidence_receipt.operation.name, "data.query");
  assert.equal(result.evidence_receipt.resource.resource_id, PUBLIC_READ_ONS_RESOURCE.resource_id);
  assert.equal(result.evidence_receipt.resource.dataset.dimension_order[1], "geography");
  assert.equal(result.evidence_receipt.resource.rights.licence, "Open Government Licence v3.0");
  assert.equal(result.evidence_storage, undefined);
  const core = {
    schema: result.schema,
    operation: result.operation,
    request_id: result.request_id,
    trace_id: result.trace_id,
    evidence_binding: result.evidence_binding,
    data: result.data,
    warnings: result.warnings,
  };
  assert.equal(
    verifyPublicReadReceipt(result.evidence_receipt, {
      normalisedParameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
      resultCore: core,
      publicPolicy: PUBLIC_READ_POLICY,
      expectedAuthorityContext: result.evidence_receipt.authority_context,
      expectedPolicyDecision: result.evidence_receipt.policy_decision,
      expectedResource: PUBLIC_READ_ONS_RESOURCE,
      expectedSoftware: SOFTWARE,
    }).valid,
    true,
  );
  assert.equal(Object.isFrozen(result), true);
});

test(
  "propagates exact validated Trace Context to the adapter without provider headers",
  async (t) => {
    let transportRequestKeys: readonly PropertyKey[] = [];
    const injected = new OnsDataApiAdapter({
      lifecycle: ACTIVE_INVOCATION,
      transport: async (request) => {
        transportRequestKeys = Reflect.ownKeys(request).sort();
        return response();
      },
      now: () => Date.parse("2030-01-01T00:00:00Z"),
    });
    const originalExecute = injected.execute.bind(injected);
    let observed: ProviderAdapterExecutionOptions | undefined;
    t.mock.method(injected, "execute", async (
      request: unknown,
      options: ProviderAdapterExecutionOptions = {},
    ) => {
      observed = options;
      return await originalExecute(request, options);
    });

    const result = await application(injected).query(
      PUBLIC_ONS_DATA_QUERY_PARAMETERS,
      CONTEXT,
    );

    assert.deepEqual(observed?.trace, CONTEXT.trace);
    assert.equal(observed?.signal, undefined);
    assert.equal(observed?.deadline, undefined);
    assert.deepEqual(transportRequestKeys, ["policy", "signal", "url"]);
    assert.equal(result.trace_id, CONTEXT.traceId);
    assert.equal(result.evidence_receipt.trace_id, CONTEXT.traceId);
    assert.equal(JSON.stringify(result).includes(CONTEXT.trace.traceparent), false);
    assert.equal(JSON.stringify(result).includes(CONTEXT.trace.tracestate), false);
  },
);

test("creates a random-ID-flagged provider trace for a trusted legacy context", async (t) => {
  const injected = adapter();
  const originalExecute = injected.execute.bind(injected);
  let observed: ProviderAdapterExecutionOptions | undefined;
  t.mock.method(injected, "execute", async (
    request: unknown,
    options: ProviderAdapterExecutionOptions = {},
  ) => {
    observed = options;
    return await originalExecute(request, options);
  });
  const legacyContext = {
    requestId: "request-data-query-legacy-trace",
    traceId: CONTEXT.traceId,
    instance: "/data/query",
  };

  const result = await application(injected).query(
    PUBLIC_ONS_DATA_QUERY_PARAMETERS,
    legacyContext,
  );

  assert.ok(observed?.trace !== undefined);
  assert.match(
    observed.trace.traceparent,
    new RegExp(`^00-${CONTEXT.traceId}-[0-9a-f]{16}-02$`, "u"),
  );
  assert.equal(observed.trace.tracestate, undefined);
  assert.equal(Object.isFrozen(observed.trace), true);
  assert.equal(result.trace_id, CONTEXT.traceId);
  assert.equal(result.evidence_receipt.trace_id, CONTEXT.traceId);
});

test("rejects a mismatched provider trace before egress", async () => {
  const calls = { count: 0, urls: [] as string[] };
  const mismatched = {
    ...CONTEXT,
    trace: {
      traceparent:
        "00-8123456789abcdef0123456789abcdef-89abcdef01234567-00",
    },
  };
  await assert.rejects(
    application(adapter(calls)).query(
      PUBLIC_ONS_DATA_QUERY_PARAMETERS,
      mismatched,
    ),
    /traceparent/u,
  );
  assert.equal(calls.count, 0);
});

test("uses exact approved cache after a classified HTTP 500 to 599 response", async () => {
  const calls = { count: 0, urls: [] as string[] };
  const injected = new OnsDataApiAdapter({
    lifecycle: ACTIVE_INVOCATION,
    transport: async ({ url }) => {
      calls.count += 1;
      calls.urls.push(url);
      return response(null, 503);
    },
    sleep: async () => undefined,
    now: () => Date.parse("2030-01-01T00:00:00Z"),
  });
  const result = await application(injected, {
    approvedCache: approvedCache(),
    now: () => new Date("2026-08-22T12:00:00.000Z"),
  }).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT);

  assert.equal(calls.count, 2);
  assert.deepEqual(result.data, {
    status: "succeeded",
    observations: [{ value: "10471", unit: null }],
    cache: {
      status: "approved-current",
      cache_id:
        "gis-ai-go:approved-provider-cache:sha256:06dd19673c2f9d605dbad2c64a21903f6448fb4965838098bd16df40f6db4961",
      source_uri:
        "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121/observations?time=2026&geography=E92000001&week=week-24&causeofdeath=all-causes",
      provider_result_sha256:
        "309a7c0a374f93f20d4b4cc8aaa4530c4a828ea27e4e26e266b367e59b7da3bd",
      retrieved_at: "2026-08-20T20:21:08.947Z",
      stale_after: "2027-02-20T20:21:08.947Z",
      checked_at: "2026-08-22T12:00:00.000Z",
    },
  });
  assert.deepEqual(result.warnings, [APPROVED_CACHE_WARNING]);
  assert.deepEqual(result.evidence_receipt.transformations, [
    { name: "normalise-public-read-parameters", version: "v1" },
    { name: "read-approved-provider-cache", version: "v1" },
    { name: "project-public-read-result-core", version: "v1" },
  ]);
  assert.equal(result.evidence_receipt.created_at, result.data.cache?.checked_at);
  const core = {
    schema: result.schema,
    operation: result.operation,
    request_id: result.request_id,
    trace_id: result.trace_id,
    evidence_binding: result.evidence_binding,
    data: result.data,
    warnings: result.warnings,
  };
  assert.equal(
    verifyPublicReadReceipt(result.evidence_receipt, {
      normalisedParameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
      resultCore: core,
      publicPolicy: PUBLIC_READ_POLICY,
      expectedAuthorityContext: result.evidence_receipt.authority_context,
      expectedPolicyDecision: result.evidence_receipt.policy_decision,
      expectedResource: PUBLIC_READ_ONS_RESOURCE,
      expectedSoftware: SOFTWARE,
    }).valid,
    true,
  );

  const wrongPipeline = mutable(result.evidence_receipt) as unknown as {
    transformations: Array<{ name: string; version: string }>;
  };
  wrongPipeline.transformations[1] = {
    name: "execute-fixed-provider-query",
    version: "v1",
  };
  assert.equal(
    verifyPublicReadReceipt(wrongPipeline, {
      normalisedParameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
      resultCore: core,
      publicPolicy: PUBLIC_READ_POLICY,
    }).valid,
    false,
  );
});

test("uses exact approved cache after an internally classified network failure", async (t) => {
  const admissionNow = Date.now() + 60_001;
  let resolve4Calls = 0;
  let resolve6Calls = 0;
  t.mock.method(Date, "now", () => admissionNow);
  t.mock.method(Resolver.prototype, "resolve4", async () => {
    resolve4Calls += 1;
    throw Object.assign(new Error("offline DNS failure"), { code: "ENOTFOUND" });
  });
  t.mock.method(Resolver.prototype, "resolve6", async () => {
    resolve6Calls += 1;
    throw Object.assign(new Error("offline DNS failure"), { code: "EAI_AGAIN" });
  });
  const injected = new OnsDataApiAdapter({
    lifecycle: ACTIVE_INVOCATION,
    sleep: async () => undefined,
    now: () => Date.parse("2030-01-01T00:00:00Z"),
  });
  const result = await application(injected, {
    approvedCache: approvedCache(),
    now: () => new Date("2026-08-22T12:00:00.000Z"),
  }).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT);
  assert.equal(resolve4Calls, 2);
  assert.equal(resolve6Calls, 2);
  assert.equal(result.data.cache?.status, "approved-current");
  assert.deepEqual(result.warnings, [APPROVED_CACHE_WARNING]);
  assert.deepEqual(result.evidence_receipt.transformations, [
    { name: "normalise-public-read-parameters", version: "v1" },
    { name: "read-approved-provider-cache", version: "v1" },
    { name: "project-public-read-result-core", version: "v1" },
  ]);
  const core = {
    schema: result.schema,
    operation: result.operation,
    request_id: result.request_id,
    trace_id: result.trace_id,
    evidence_binding: result.evidence_binding,
    data: result.data,
    warnings: result.warnings,
  };
  assert.equal(
    verifyPublicReadReceipt(result.evidence_receipt, {
      normalisedParameters: PUBLIC_ONS_DATA_QUERY_PARAMETERS,
      resultCore: core,
      publicPolicy: PUBLIC_READ_POLICY,
      expectedAuthorityContext: result.evidence_receipt.authority_context,
      expectedPolicyDecision: result.evidence_receipt.policy_decision,
      expectedResource: PUBLIC_READ_ONS_RESOURCE,
      expectedSoftware: SOFTWARE,
    }).valid,
    true,
  );
});

test("does not use cache for stale, suspended or rate-limited provider states", async () => {
  const stale = new OnsDataApiAdapter({
    lifecycle: ACTIVE_INVOCATION,
    transport: async () => response(null, 599),
    sleep: async () => undefined,
    now: () => Date.parse("2030-01-01T00:00:00Z"),
  });
  await expectProblem(
    () =>
      application(stale, {
        approvedCache: approvedCache(),
        now: () => new Date("2027-02-20T20:21:08.947Z"),
      }).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT),
    "provider_unavailable",
  );

  const rateLimited = new OnsDataApiAdapter({
    lifecycle: ACTIVE_INVOCATION,
    now: () => {
      throw new ProviderAdapterFault("PROVIDER_RATE_LIMITED", { retryable: true });
    },
  });
  await expectProblem(
    () =>
      application(rateLimited, {
        approvedCache: approvedCache(),
        now: () => new Date("2026-08-22T12:00:00.000Z"),
      }).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT),
    "provider_rate_limited",
  );

  const suspended = adapter(undefined, {
    discovery: "suspended",
    invocation: "suspended",
    reason: "The cache cannot authorise a suspended provider.",
  });
  await expectProblem(
    () =>
      application(suspended, {
        approvedCache: approvedCache(),
        now: () => new Date("2026-08-22T12:00:00.000Z"),
      }).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT),
    "provider_suspended",
  );
});

test(
  "keeps 3xx, 4xx, timeout, unsafe, malformed, opaque and unbranded failures receipt-free",
  async () => {
  for (const [status, expected] of [
    [302, "provider_unavailable"],
    [401, "provider_unavailable"],
    [403, "provider_unavailable"],
    [429, "provider_rate_limited"],
    [451, "provider_unavailable"],
    [499, "provider_unavailable"],
  ] as const) {
    const injected = new OnsDataApiAdapter({
      lifecycle: ACTIVE_INVOCATION,
      transport: async () => response(null, status),
      sleep: async () => undefined,
      now: () => Date.parse("2030-01-01T00:00:00Z"),
    });
    await expectProblem(
      () => application(injected, {
        approvedCache: approvedCache(),
        now: () => new Date("2026-08-22T12:00:00.000Z"),
      }).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT),
      expected,
    );
  }

  for (const [kind, expected] of [
    ["network", "provider_unavailable"],
    ["unsafe-address", "provider_unavailable"],
    ["connect-timeout", "provider_timeout"],
    ["response-timeout", "provider_timeout"],
    ["response-too-large", "provider_contract_failed"],
    ["invalid-response-framing", "provider_contract_failed"],
    ["invalid-response-headers", "provider_contract_failed"],
  ] as const) {
    const injected = new OnsDataApiAdapter({
      lifecycle: ACTIVE_INVOCATION,
      transport: async () => {
        throw new FixedHttpsTransportError(kind);
      },
      now: () => Date.parse("2030-01-01T00:00:00Z"),
    });
    await expectProblem(
      () => application(injected, {
        approvedCache: approvedCache(),
        now: () => new Date("2026-08-22T12:00:00.000Z"),
      }).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT),
      expected,
    );
  }

  for (const thrown of [
    new Error("opaque provider failure"),
    new ProviderAdapterFault("PROVIDER_OUTAGE", {
      providerStatus: 503,
      retryable: true,
    }),
  ]) {
    const injected = new OnsDataApiAdapter({
      lifecycle: ACTIVE_INVOCATION,
      now: () => {
        throw thrown;
      },
    });
    await expectProblem(
      () => application(injected, {
        approvedCache: approvedCache(),
        now: () => new Date("2026-08-22T12:00:00.000Z"),
      }).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT),
      "provider_unavailable",
    );
  }

  let capturedOutage: unknown;
  let replayCapturedOutage = false;
  const replaySource = new OnsDataApiAdapter({
    lifecycle: ACTIVE_INVOCATION,
    transport: async () => response(null, 599),
    sleep: async () => undefined,
    now: () => {
      if (replayCapturedOutage) throw capturedOutage;
      return Date.parse("2030-01-01T00:00:00Z");
    },
  });
  const priorExecution = executePristineOnsDataApiAdapter(
    replaySource,
    ONS_ADAPTER_REQUEST,
    {},
  );
  try {
    await priorExecution.result;
    assert.fail("expected a classified provider outage");
  } catch (error) {
    capturedOutage = error;
  }
  replayCapturedOutage = true;
  await expectProblem(
    () => application(replaySource, {
      approvedCache: approvedCache(),
      now: () => new Date("2026-08-22T12:00:00.000Z"),
    }).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, {
      ...CONTEXT,
      requestId: "request-data-query-prior-execution-outage-1",
    }),
    "provider_unavailable",
  );
  assert.equal(
    priorExecution.approvedCacheOutage(
      capturedOutage,
      replaySource.normalise_error(capturedOutage),
    ),
    null,
  );

  let replayCalls = 0;
  const preSubstituted = adapter();
  Object.defineProperty(preSubstituted, "execute", {
    configurable: true,
    value: async () => {
      replayCalls += 1;
      throw capturedOutage;
    },
  });
  assert.throws(
    () => application(preSubstituted, {
      approvedCache: approvedCache(),
      now: () => new Date("2026-08-22T12:00:00.000Z"),
    }),
    /requires an unmodified ONS adapter/u,
  );

  const postSubstituted = adapter();
  const replayApplication = application(postSubstituted, {
    approvedCache: approvedCache(),
    now: () => new Date("2026-08-22T12:00:00.000Z"),
  });
  Object.defineProperty(postSubstituted, "execute", {
    configurable: true,
    value: async () => {
      replayCalls += 1;
      throw capturedOutage;
    },
  });
  await expectProblem(
    () => replayApplication.query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, {
      ...CONTEXT,
      requestId: "request-data-query-replayed-outage-1",
    }),
    "provider_contract_failed",
  );

  class SubstitutedAdapter extends OnsDataApiAdapter {
    public override async execute(): Promise<ProviderAdapterResult> {
      replayCalls += 1;
      throw capturedOutage;
    }
  }
  assert.throws(
    () => application(new SubstitutedAdapter({ lifecycle: ACTIVE_INVOCATION }), {
      approvedCache: approvedCache(),
      now: () => new Date("2026-08-22T12:00:00.000Z"),
    }),
    /subclassing is not supported/u,
  );
  assert.equal(replayCalls, 0);
  const malformedProblem = {
    outcome: "problem",
    code: "provider_contract_failed",
    receipt: false,
    reflectedLocation: false,
    requests: 1,
  };
  assert.deepEqual(malformedFixedHttpsGatewayProbe(), {
    "short-content-length": malformedProblem,
    "short-chunked": malformedProblem,
    "short-redirect": malformedProblem,
  });
  },
);

test("reproduces the promoted successful application fixture", async () => {
  const fixture = JSON.parse(
    readFileSync(
      new URL("../../../../providers/fixtures/data-query-result.example.json", import.meta.url),
      "utf8",
    ),
  ) as Record<string, unknown>;
  const result = await application(adapter()).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, {
    requestId: "request-data-query-example-1",
    traceId: "8123456789abcdef0123456789abcdef",
  });
  assert.deepEqual(result, fixture);
});

test("keeps discovery and invocation lifecycle planes independent", async (context) => {
  const invocationCalls = { count: 0, urls: [] as string[] };
  const invocationOnly = adapter(invocationCalls, {
    discovery: "suspended",
    invocation: "active",
    reason: "Invocation-only application test.",
  });
  assert.equal(
    (
      await application(invocationOnly).query(
        PUBLIC_ONS_DATA_QUERY_PARAMETERS,
        CONTEXT,
      )
    ).data.status,
    "succeeded",
  );
  assert.equal(invocationCalls.count, 1);

  const discoveryCalls = { count: 0, urls: [] as string[] };
  const discoveryOnly = adapter(discoveryCalls, {
    discovery: "active",
    invocation: "suspended",
    reason: "Discovery cannot authorise invocation.",
  });
  let discoveryOnlyEstimates = 0;
  context.mock.method(discoveryOnly, "estimate", () => {
    discoveryOnlyEstimates += 1;
    throw new Error("estimate must not run while invocation is suspended");
  });
  await expectProblem(
    () => application(discoveryOnly).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT),
    "provider_suspended",
  );
  assert.equal(discoveryCalls.count, 0);
  assert.equal(discoveryOnlyEstimates, 0);

  const suspendedCalls = { count: 0, urls: [] as string[] };
  const suspended = adapter(suspendedCalls, {
    discovery: "suspended",
    invocation: "suspended",
    reason: "Both planes suspended.",
  });
  await expectProblem(
    () => application(suspended).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT),
    "provider_suspended",
  );
  assert.equal(suspendedCalls.count, 0);
});

test("orders every adapter check before the single execute call", async (context) => {
  const injected = adapter();
  const order: string[] = [];
  const originalHealth = injected.health.bind(injected);
  const originalEstimate = injected.estimate.bind(injected);
  const originalRights = injected.licence_evidence.bind(injected);
  const originalProvenance = injected.provenance.bind(injected);
  const result = validAdapterResult(injected);
  context.mock.method(injected, "health", () => {
    order.push("health");
    return originalHealth();
  });
  context.mock.method(injected, "estimate", (request: unknown) => {
    order.push("estimate");
    return originalEstimate(request);
  });
  context.mock.method(injected, "licence_evidence", () => {
    order.push("rights");
    return originalRights();
  });
  context.mock.method(injected, "provenance", () => {
    order.push("provenance");
    return originalProvenance();
  });
  context.mock.method(injected, "execute", async () => {
    order.push("execute");
    return result;
  });
  await application(injected).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT);
  assert.deepEqual(order, ["health", "estimate", "rights", "provenance", "execute"]);
});

test("rejects every deviation from the exact five-key request before execution", async () => {
  const calls = { count: 0, urls: [] as string[] };
  const run = application(adapter(calls));
  const cases: unknown[] = [
    {},
    { ...PUBLIC_ONS_DATA_QUERY_PARAMETERS, limit: 2 },
    { ...PUBLIC_ONS_DATA_QUERY_PARAMETERS, url: "https://example.invalid" },
    {
      ...PUBLIC_ONS_DATA_QUERY_PARAMETERS,
      dataset: { ...PUBLIC_ONS_DATA_QUERY_PARAMETERS.dataset, version: "latest" },
    },
    {
      ...PUBLIC_ONS_DATA_QUERY_PARAMETERS,
      selections: [...PUBLIC_ONS_DATA_QUERY_PARAMETERS.selections].reverse(),
    },
  ];
  const cyclic: Record<string, unknown> = {};
  cyclic.self = cyclic;
  cases.push(cyclic);
  const accessor = {};
  Object.defineProperty(accessor, "schema", { enumerable: true, get: () => "secret" });
  cases.push(accessor);
  cases.push(new Proxy(mutable(PUBLIC_ONS_DATA_QUERY_PARAMETERS), {}));
  for (const candidate of cases) {
    await expectProblem(() => run.query(candidate, CONTEXT), "invalid_request");
  }
  assert.equal(calls.count, 0);
});

test("checks health, estimate, rights and provenance before execute", async (context) => {
  for (const field of ["health", "estimate", "licence_evidence", "provenance"] as const) {
    const injected = adapter();
    const originalHealth = injected.health();
    let executions = 0;
    context.mock.method(injected, "execute", async () => {
      executions += 1;
      return validAdapterResult(injected);
    });
    if (field === "health") {
      context.mock.method(injected, field, () => ({
        ...originalHealth,
        adapterId: "another-adapter",
      }));
    } else if (field === "estimate") {
      context.mock.method(injected, field, () => ({
        confidence: "upper-bound",
        maxObservations: 2,
        maxAttempts: 2,
        maxCompressedResponseBytes: 262_144,
        maxDecompressedResponseBytes: 1_048_576,
        maxCanonicalResponseBytes: 262_144,
      }));
    } else if (field === "licence_evidence") {
      const rights = mutable(injected.licence_evidence());
      (rights as { licence: string }).licence = "Unknown";
      context.mock.method(injected, field, () => rights);
    } else {
      const provenance = mutable(injected.provenance());
      (provenance.providerVersion as { version: string }).version = "latest";
      context.mock.method(injected, field, () => provenance);
    }
    await expectProblem(
      () => application(injected).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT),
      "provider_contract_failed",
    );
    assert.equal(executions, 0, `${field} drift must fail before execute`);
    context.mock.reset();
  }

  const malformedHealth = adapter();
  let malformedExecutions = 0;
  context.mock.method(malformedHealth, "health", () => null as never);
  context.mock.method(malformedHealth, "execute", async () => {
    malformedExecutions += 1;
    return validAdapterResult(malformedHealth);
  });
  await expectProblem(
    () => application(malformedHealth).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT),
    "provider_contract_failed",
  );
  assert.equal(malformedExecutions, 0);
});

test("independently rejects result and evidence drift", async (context) => {
  const mutations: readonly ((result: ProviderAdapterResult) => void)[] = [
    (result) => {
      (result.provider as { id: string }).id = "other-provider";
    },
    (result) => {
      (result.dataset as { version: string }).version = "latest";
    },
    (result) => {
      (result.dimensions as { dimension: string; option: string }[]).reverse();
    },
    (result) => {
      (result.rights as { licence: string }).licence = "Unknown";
    },
    (result) => {
      (result.observations[0] as { value: string }).value = "10.5";
    },
    (result) => {
      (result.observations[0] as { unit: string | null }).unit = "deaths";
    },
    (result) => {
      (result.observations as unknown as Array<{ value: string; unit: null }>)[0] = {
        value: "10471",
        unit: null,
      };
    },
  ];
  for (const mutate of mutations) {
    const injected = adapter();
    const candidate = mutable(validAdapterResult(injected));
    mutate(candidate);
    let executions = 0;
    context.mock.method(injected, "execute", async () => {
      executions += 1;
      return candidate;
    });
    await expectProblem(
      () => application(injected).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT),
      "provider_contract_failed",
    );
    assert.equal(executions, 1);
    context.mock.reset();
  }
});

test("maps malformed adapter return shapes to a closed contract problem", async (context) => {
  for (const candidate of [null, {}, [], "10471"]) {
    const injected = adapter();
    context.mock.method(injected, "execute", async () => candidate as never);
    await expectProblem(
      () => application(injected).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT),
      "provider_contract_failed",
    );
    context.mock.reset();
  }
});

test("maps adapter failures to fixed non-reflective receipt-free problems", async (context) => {
  const mappings: readonly [unknown, DataQueryProblemCode][] = [
    [
      new ProviderAdapterFault("PROVIDER_RATE_LIMITED", { providerStatus: 429 }),
      "provider_rate_limited",
    ],
    [new ProviderAdapterFault("PROVIDER_TIMEOUT"), "provider_timeout"],
    [new ProviderAdapterFault("PROVIDER_OUTAGE", { providerStatus: 503 }), "provider_unavailable"],
    [new ProviderAdapterFault("MALFORMED_PROVIDER_RESPONSE"), "provider_contract_failed"],
    [new ProviderAdapterFault("RIGHTS_UNKNOWN"), "provider_contract_failed"],
    [new ProviderAdapterFault("STALE_PROVIDER_VERSION"), "provider_contract_failed"],
    [new Error("Bearer secret-token at provider-internal-location"), "provider_unavailable"],
  ];
  for (const [thrown, expected] of mappings) {
    const injected = adapter();
    context.mock.method(injected, "execute", async () => {
      throw thrown;
    });
    const error = await expectProblem(
      () => application(injected).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT),
      expected,
    );
    const problem = canonicalJson(error.problem);
    assert.equal(problem.includes("secret-token"), false);
    assert.equal(problem.includes("provider-internal-location"), false);
    assert.equal(problem.includes("MALFORMED_PROVIDER_RESPONSE"), false);
    context.mock.reset();
  }
});

test("propagates live controls and keeps an adapter-local timeout at 504", async (context) => {
  const injected = adapter();
  const signal = new AbortController().signal;
  const deadline = "2030-01-01T00:00:10Z";
  let observedRequest: unknown;
  let observedOptions: unknown;
  let executions = 0;
  context.mock.method(injected, "execute", async (
    requestValue: unknown,
    options?: ProviderAdapterExecutionOptions,
  ) => {
    executions += 1;
    observedRequest = requestValue;
    observedOptions = options;
    throw new ProviderAdapterFault("PROVIDER_TIMEOUT");
  });
  const timeout = await expectProblem(
    () =>
      application(injected).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT, {
        signal,
        deadline,
      }),
    "provider_timeout",
  );
  assert.equal(timeout.problem.status, 504);
  assert.equal(executions, 1);
  assert.equal(observedRequest, ONS_ADAPTER_REQUEST);
  assert.deepEqual(observedOptions, { signal, deadline, trace: CONTEXT.trace });
  assert.equal(signal.aborted, false);
});

test("rejects invalid and unknown controls before execution", async () => {
  const calls = { count: 0, urls: [] as string[] };
  const injected = adapter(calls);
  const run = application(injected);
  await expectProblem(
    () =>
      run.query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT, {
        deadline: "not-a-deadline",
      }),
    "invalid_request",
  );
  await expectProblem(
    () =>
      run.query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT, {
        unexpected: true,
      } as unknown as { deadline: string }),
    "invalid_request",
  );
  assert.equal(calls.count, 0);
});

test("attributes ended controls before policy, adapter checks or evidence", async (context) => {
  const directory = mkdtempSync(join(tmpdir(), "gis-ai-go-data-query-controls-"));
  try {
    const ledger = PublicEvidenceLedger.open({ rootDirectory: directory });
    let evidenceWrites = 0;
    context.mock.method(ledger, "persistReceipt", () => {
      evidenceWrites += 1;
      throw new Error("evidence must not be written for ended controls");
    });

    const injected = adapter();
    const adapterCalls: string[] = [];
    const originalHealth = injected.health.bind(injected);
    const originalEstimate = injected.estimate.bind(injected);
    const originalRights = injected.licence_evidence.bind(injected);
    const originalProvenance = injected.provenance.bind(injected);
    context.mock.method(injected, "health", () => {
      adapterCalls.push("health");
      return originalHealth();
    });
    context.mock.method(injected, "estimate", (request: ProviderAdapterQuery) => {
      adapterCalls.push("estimate");
      return originalEstimate(request);
    });
    context.mock.method(injected, "licence_evidence", () => {
      adapterCalls.push("rights");
      return originalRights();
    });
    context.mock.method(injected, "provenance", () => {
      adapterCalls.push("provenance");
      return originalProvenance();
    });
    context.mock.method(injected, "execute", async () => {
      adapterCalls.push("execute");
      return validAdapterResult(injected);
    });

    const run = application(injected, {
      evidenceLedger: ledger,
      now: () => new Date("2026-08-21T01:00:00.000Z"),
    });
    const controller = new AbortController();
    controller.abort("private-cancellation-reason");
    const cancelled = await expectProblem(
      () =>
        run.query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT, {
          signal: controller.signal,
        }),
      "query_cancelled",
    );
    assert.equal(cancelled.problem.status, 408);
    assert.equal(canonicalJson(cancelled.problem).includes("private-cancellation-reason"), false);

    const expiredDeadline = "2026-08-21T00:59:59.123Z";
    const expired = await expectProblem(
      () =>
        run.query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT, {
          deadline: expiredDeadline,
        }),
      "query_deadline_exceeded",
    );
    assert.equal(expired.problem.status, 408);
    assert.equal(canonicalJson(expired.problem).includes(expiredDeadline), false);

    const simultaneous = await expectProblem(
      () =>
        run.query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT, {
          signal: controller.signal,
          deadline: expiredDeadline,
        }),
      "query_cancelled",
    );
    assert.equal(simultaneous.problem.status, 408);
    assert.deepEqual(adapterCalls, []);
    assert.equal(evidenceWrites, 0);
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});

test("reattributes controls that end during a rejected execution", async (context) => {
  for (const kind of ["cancel", "deadline", "simultaneous"] as const) {
    let current = Date.parse("2030-01-01T00:00:00Z");
    const deadline = "2030-01-01T00:00:10Z";
    const controller = new AbortController();
    const injected = adapter();
    let executions = 0;
    context.mock.method(injected, "execute", async () => {
      executions += 1;
      if (kind !== "deadline") controller.abort("private-during-execute-reason");
      if (kind !== "cancel") current = Date.parse(deadline);
      throw new ProviderAdapterFault("PROVIDER_TIMEOUT");
    });
    const error = await expectProblem(
      () =>
        application(injected, { now: () => new Date(current) }).query(
          PUBLIC_ONS_DATA_QUERY_PARAMETERS,
          CONTEXT,
          {
            ...(kind === "deadline" ? {} : { signal: controller.signal }),
            ...(kind === "cancel" ? {} : { deadline }),
          },
        ),
      kind === "deadline" ? "query_deadline_exceeded" : "query_cancelled",
    );
    const problem = canonicalJson(error.problem);
    assert.equal(error.problem.status, 408);
    assert.equal(problem.includes("private-during-execute-reason"), false);
    assert.equal(problem.includes(deadline), false);
    assert.equal(executions, 1);
    context.mock.reset();
  }
});

test("checks ended controls immediately after successful execution before evidence", async (
  context,
) => {
  for (const kind of ["cancel", "deadline", "simultaneous"] as const) {
    const directory = mkdtempSync(join(tmpdir(), "gis-ai-go-data-query-after-success-"));
    try {
      let current = Date.parse("2030-01-01T00:00:00Z");
      const deadline = "2030-01-01T00:00:10Z";
      const controller = new AbortController();
      const ledger = PublicEvidenceLedger.open({ rootDirectory: directory });
      let evidenceWrites = 0;
      context.mock.method(ledger, "persistReceipt", () => {
        evidenceWrites += 1;
        throw new Error("evidence must not be written after controls end");
      });
      const injected = adapter();
      const result = validAdapterResult(injected);
      let executions = 0;
      context.mock.method(injected, "execute", async () => {
        executions += 1;
        if (kind !== "deadline") controller.abort("private-after-success-reason");
        if (kind !== "cancel") current = Date.parse(deadline);
        return result;
      });
      const error = await expectProblem(
        () =>
          application(injected, {
            evidenceLedger: ledger,
            now: () => new Date(current),
          }).query(PUBLIC_ONS_DATA_QUERY_PARAMETERS, CONTEXT, {
            ...(kind === "deadline" ? {} : { signal: controller.signal }),
            ...(kind === "cancel" ? {} : { deadline }),
          }),
        kind === "deadline" ? "query_deadline_exceeded" : "query_cancelled",
      );
      const problem = canonicalJson(error.problem);
      assert.equal(error.problem.status, 408);
      assert.equal(problem.includes("private-after-success-reason"), false);
      assert.equal(problem.includes(deadline), false);
      assert.equal(executions, 1);
      assert.equal(evidenceWrites, 0);
    } finally {
      context.mock.reset();
      rmSync(directory, { recursive: true, force: true });
    }
  }
});

test("persists only fully verified v2 evidence through the optional ledger seam", async () => {
  const directory = mkdtempSync(join(tmpdir(), "gis-ai-go-data-query-ledger-"));
  try {
    const ledger = PublicEvidenceLedger.open({
      rootDirectory: directory,
      now: () => new Date("2026-08-21T01:00:01.000Z"),
    });
    const result = await application(adapter(), { evidenceLedger: ledger }).query(
      PUBLIC_ONS_DATA_QUERY_PARAMETERS,
      CONTEXT,
    );
    assert.equal(result.evidence_storage?.status, "persisted");
    const stored = ledger.inspect(result.evidence_receipt.receipt_id);
    assert.equal(stored?.record.schema, "gis-ai-go.public-evidence-record.v2");
    assert.equal(stored?.record.receipt.operation.name, "data.query");
    assert.equal(canonicalJson(stored).includes("10471"), false);
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});

test("returns no receipt when evidence time or storage fails", async (context) => {
  await expectProblem(
    () =>
      application(adapter(), { now: () => new Date(Number.NaN) }).query(
        PUBLIC_ONS_DATA_QUERY_PARAMETERS,
        CONTEXT,
      ),
    "evidence_unavailable",
  );

  const directory = mkdtempSync(join(tmpdir(), "gis-ai-go-data-query-ledger-failure-"));
  try {
    const ledger = PublicEvidenceLedger.open({ rootDirectory: directory });
    context.mock.method(ledger, "persistReceipt", () => {
      throw new Error("Bearer private-ledger-secret at ledger-internal-location");
    });
    const error = await expectProblem(
      () =>
        application(adapter(), { evidenceLedger: ledger }).query(
          PUBLIC_ONS_DATA_QUERY_PARAMETERS,
          CONTEXT,
        ),
      "evidence_unavailable",
    );
    assert.equal(canonicalJson(error.problem).includes("private-ledger-secret"), false);
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});

test("reconciles a lost success after restart without provider preflight or execution", async (context) => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-data-query-reconcile-"));
  try {
    const ledgerRoot = join(parent, "ledger");
    const indexRoot = join(parent, "index");
    const ledger = PublicEvidenceLedger.open({
      rootDirectory: ledgerRoot,
      retentionDays: 30,
      now: () => new Date("2026-08-21T01:00:01.000Z"),
    });
    const index = openEvidenceReconciliationIndex({
      rootDirectory: indexRoot,
      ledger,
      now: () => new Date("2026-08-21T01:00:00.000Z"),
    });
    const firstCalls = { count: 0, urls: [] as string[] };
    const first = application(adapter(firstCalls), {
      evidenceLedger: ledger,
      reconciliationIndex: index,
    });
    const deliveredButSuppressed = await first.query(reconciledRequest(), CONTEXT);
    assert.equal(firstCalls.count, 1);
    assert.equal(deliveredButSuppressed.evidence_storage?.status, "persisted");

    const restartedLedger = PublicEvidenceLedger.open({
      rootDirectory: ledgerRoot,
      retentionDays: 30,
    });
    const restartedIndex = openEvidenceReconciliationIndex({
      rootDirectory: indexRoot,
      ledger: restartedLedger,
    });
    const retryCalls = { count: 0, urls: [] as string[] };
    const retryAdapter = adapter(retryCalls, {
      discovery: "suspended",
      invocation: "suspended",
      reason: "Completed reconciliation must bypass provider preflight.",
    });
    context.mock.method(retryAdapter, "health", () => {
      throw new Error("provider preflight must not run for completed reconciliation");
    });
    const retry = application(retryAdapter, {
      evidenceLedger: restartedLedger,
      reconciliationIndex: restartedIndex,
    });
    await expectReconciliationProblem(
      () =>
        retry.query(reconciledRequest(), {
          requestId: "request-data-query-retry-2",
          traceId: "8123456789abcdef0123456789abcdef",
        }),
      "idempotency_completed",
    );
    assert.equal(retryCalls.count, 0);
    assert.equal(restartedLedger.verify().record_count, 1);
    assert.equal(restartedLedger.verify().event_count, 1);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("keeps an executed but unreceipted key pending and never executes it twice", async () => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-data-query-pending-"));
  try {
    const ledger = PublicEvidenceLedger.open({ rootDirectory: join(parent, "ledger") });
    const index = openEvidenceReconciliationIndex({
      rootDirectory: join(parent, "index"),
      ledger,
    });
    const calls = { count: 0, urls: [] as string[] };
    const reconciled = application(adapter(calls), {
      evidenceLedger: ledger,
      reconciliationIndex: index,
      now: () => new Date(Number.NaN),
    });
    await expectProblem(
      () => reconciled.query(reconciledRequest(), CONTEXT),
      "evidence_unavailable",
    );
    assert.equal(calls.count, 1);
    await expectReconciliationProblem(
      () => reconciled.query(reconciledRequest(), CONTEXT),
      "idempotency_pending",
    );
    assert.equal(calls.count, 1);
    assert.equal(ledger.verify().record_count, 0);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("maps exhausted reconciliation admission to a fixed evidence-unavailable problem", async (
  context,
) => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-data-query-capacity-"));
  try {
    const indexRoot = join(parent, "index");
    const ledger = PublicEvidenceLedger.open({ rootDirectory: join(parent, "ledger") });
    const index = openEvidenceReconciliationIndex({ rootDirectory: indexRoot, ledger });
    context.mock.method(index, "claim", () => {
      throw new EvidenceReconciliationIndexError(
        "capacity",
        `private capacity detail for ${IDEMPOTENCY_KEY}`,
      );
    });
    const calls = { count: 0, urls: [] as string[] };
    const error = await expectProblem(
      () =>
        application(adapter(calls), {
          evidenceLedger: ledger,
          reconciliationIndex: index,
        }).query(reconciledRequest(), CONTEXT),
      "evidence_unavailable",
    );
    assert.equal(error.problem.status, 503);
    assert.equal(canonicalJson(error.problem).includes(IDEMPOTENCY_KEY), false);
    assert.equal(canonicalJson(error.problem).includes("private capacity detail"), false);
    assert.equal(calls.count, 0);
    assert.deepEqual(readdirSync(join(indexRoot, "claim-ownership")), []);
    assert.deepEqual(readdirSync(join(indexRoot, "claims")), []);
    assert.deepEqual(readdirSync(join(indexRoot, "claim-ready")), []);
  } finally {
    context.mock.reset();
    rmSync(parent, { recursive: true, force: true });
  }
});

test("admits only one simultaneous same-key execution and completes one evidence chain", async () => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-data-query-concurrent-key-"));
  try {
    const ledger = PublicEvidenceLedger.open({ rootDirectory: join(parent, "ledger") });
    const index = openEvidenceReconciliationIndex({
      rootDirectory: join(parent, "index"),
      ledger,
    });
    let executions = 0;
    let signalStarted: (() => void) | undefined;
    const started = new Promise<void>((resolve) => {
      signalStarted = resolve;
    });
    let releaseExecution: (() => void) | undefined;
    const release = new Promise<void>((resolve) => {
      releaseExecution = resolve;
    });
    const holdingTransport: FixedHttpsTransport = async ({ policy }) => {
      executions += 1;
      assert.equal(policy, ONS_EGRESS_POLICY);
      signalStarted?.();
      await release;
      return response();
    };
    const reconciled = application(
      new OnsDataApiAdapter({
        lifecycle: ACTIVE_INVOCATION,
        transport: holdingTransport,
        now: () => Date.parse("2030-01-01T00:00:00Z"),
      }),
      { evidenceLedger: ledger, reconciliationIndex: index },
    );

    const first = reconciled.query(reconciledRequest(), CONTEXT);
    await started;
    const second = expectReconciliationProblem(
      () =>
        reconciled.query(reconciledRequest(), {
          requestId: "request-data-query-concurrent-2",
          traceId: "a123456789abcdef0123456789abcdef",
        }),
      "idempotency_pending",
    );
    await second;
    assert.equal(executions, 1);
    releaseExecution?.();
    const result = await first;
    assert.equal(result.evidence_storage?.status, "persisted");

    const indexHealth = index.verify();
    const ledgerHealth = ledger.verify();
    assert.equal(indexHealth.claim_count, 1);
    assert.equal(indexHealth.resolution_count, 1);
    assert.equal(indexHealth.completed_count, 1);
    assert.equal(indexHealth.pending_count, 0);
    assert.equal(ledgerHealth.record_count, 1);
    assert.equal(ledgerHealth.event_count, 1);
    assert.equal(executions, 1);
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("detects a pre-existing different fingerprint before provider preflight", async (context) => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-data-query-conflict-"));
  try {
    const ledger = PublicEvidenceLedger.open({ rootDirectory: join(parent, "ledger") });
    const index = openEvidenceReconciliationIndex({
      rootDirectory: join(parent, "index"),
      ledger,
    });
    index.claim({
      idempotencyKey: IDEMPOTENCY_KEY,
      operation: "data.query",
      requestId: "request-hostile-preseed",
      traceId: "9123456789abcdef0123456789abcdef",
      resourceId: PUBLIC_READ_ONS_RESOURCE.resource_id,
      normalisedParametersSha256: "b".repeat(64),
    });
    const calls = { count: 0, urls: [] as string[] };
    const injected = adapter(calls);
    context.mock.method(injected, "health", () => {
      throw new Error("provider preflight must not run for a conflicting key");
    });
    const reconciled = application(injected, {
      evidenceLedger: ledger,
      reconciliationIndex: index,
    });
    await expectReconciliationProblem(
      () => reconciled.query(reconciledRequest(), CONTEXT),
      "idempotency_conflict",
    );
    assert.equal(calls.count, 0);
    assert.notEqual(
      domainSeparatedSha256(
        CANONICAL_DOMAINS.dataQueryParameters,
        PUBLIC_ONS_DATA_QUERY_PARAMETERS,
      ),
      "b".repeat(64),
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});

test("requires the exact ledger linked to a supplied reconciliation index", () => {
  const parent = mkdtempSync(join(tmpdir(), "gis-ai-go-data-query-link-"));
  try {
    const ledger = PublicEvidenceLedger.open({ rootDirectory: join(parent, "ledger") });
    const other = PublicEvidenceLedger.open({ rootDirectory: join(parent, "other-ledger") });
    const index = openEvidenceReconciliationIndex({
      rootDirectory: join(parent, "index"),
      ledger,
    });
    assert.throws(
      () => application(adapter(), { evidenceLedger: other, reconciliationIndex: index }),
      /exact explicitly linked evidence ledger/u,
    );
  } finally {
    rmSync(parent, { recursive: true, force: true });
  }
});
