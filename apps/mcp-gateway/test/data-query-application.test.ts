import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  PUBLIC_READ_ONS_RESOURCE,
  PublicEvidenceLedger,
  canonicalJson,
  verifyPublicReadReceipt,
} from "@gis-ai-go/evidence";
import {
  ONS_ADAPTER_REQUEST,
  ONS_EGRESS_POLICY,
  OnsDataApiAdapter,
  ProviderAdapterFault,
  type AdapterLifecycle,
  type FixedHttpsResponse,
  type FixedHttpsTransport,
  type ProviderAdapterExecutionOptions,
  type ProviderAdapterQuery,
  type ProviderAdapterResult,
} from "@gis-ai-go/provider-adapter-sdk";
import { PUBLIC_READ_POLICY } from "@gis-ai-go/policy-client";

import {
  DataQueryApplicationError,
  PUBLIC_ONS_DATA_QUERY_PARAMETERS,
  createDataQueryApplication,
  type DataQueryApplicationOptions,
  type DataQueryProblemCode,
} from "../src/data-query-application.js";

const SOFTWARE = Object.freeze({
  name: "gis-ai-go-mcp-gateway",
  version: "0.1.0",
  revision: "e1fc1cbe69ea72c9aa310607d80f392ef56b0d58",
} as const);

const CONTEXT = Object.freeze({
  requestId: "request-data-query-application-1",
  traceId: "7123456789abcdef0123456789abcdef",
  instance: "/data/query",
} as const);

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

function response(payload: unknown = VALID_PAYLOAD): FixedHttpsResponse {
  const body = Buffer.from(JSON.stringify(payload), "utf8");
  return {
    status: 200,
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
  assert.deepEqual(observedOptions, { signal, deadline });
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
