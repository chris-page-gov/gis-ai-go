import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import {
  ADAPTER_OPERATIONS,
  ProviderAdapterFault,
  assertFixedEgressTarget,
  createOnsDataApiAdapter,
  type FixedEgressPolicy,
  type ProviderAdapterEstimate,
} from "../src/index.js";

interface PreflightRecord {
  readonly integrationState: string;
  readonly operations: readonly string[];
  readonly lifecycle: { readonly discovery: string; readonly invocation: string };
  readonly providerVersion: {
    readonly providerId: string;
    readonly datasetId: string;
    readonly edition: string;
    readonly versionId: string;
    readonly versionNumber: number;
    readonly versionUri: string;
    readonly sourceDate: string;
    readonly lastUpdated: string;
    readonly dimensionOrder: readonly string[];
    readonly codeListIds: Readonly<Record<string, string>>;
  };
  readonly egressPolicy: FixedEgressPolicy;
  readonly estimate: ProviderAdapterEstimate;
  readonly rights: {
    readonly state: string;
    readonly licence: string;
    readonly licenceUri: string;
    readonly attribution: string;
    readonly obligations: readonly string[];
    readonly exceptions: readonly string[];
    readonly evidenceUris: readonly string[];
    readonly reviewedAt: string;
  };
  readonly probe: {
    readonly credentialsUsed: boolean;
    readonly payloadStored: boolean;
    readonly selection: readonly { readonly dimension: string; readonly option: string }[];
  };
  readonly dependency: {
    readonly workItem: string;
    readonly status: string;
    readonly acceptedCommit: string;
    readonly providedByExecutionBoundary: readonly string[];
  };
}

function preflightRecord(): PreflightRecord {
  const url = new URL(
    "../../../../providers/ons/data-api-adapter-preflight.v1.json",
    import.meta.url,
  );
  return JSON.parse(readFileSync(url, "utf8")) as PreflightRecord;
}

test("locks the selected ONS identity, dimension order, rights and inactive boundary", () => {
  const record = preflightRecord();

  assert.equal(record.integrationState, "implemented-inactive");
  assert.deepEqual(record.operations, ADAPTER_OPERATIONS);
  assert.deepEqual(
    {
      discovery: record.lifecycle.discovery,
      invocation: record.lifecycle.invocation,
    },
    { discovery: "suspended", invocation: "suspended" },
  );
  assert.deepEqual(record.providerVersion, {
    providerId: "ons-data-api",
    datasetId: "weekly-deaths-region",
    edition: "time-series",
    versionId: "121",
    versionNumber: 121,
    versionUri:
      "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/" +
      "time-series/versions/121",
    sourceDate: "2026-07-01",
    lastUpdated: "2026-07-01T10:46:34.602Z",
    dimensionOrder: ["time", "geography", "week", "causeofdeath"],
    codeListIds: {
      time: "calendar-years",
      geography: "administrative-geography",
      week: "week-number",
      causeofdeath: "cause-of-death",
    },
  });
  assert.deepEqual(record.egressPolicy, {
    mode: "fixed",
    origin: "https://api.beta.ons.gov.uk",
    method: "GET",
    routes: [
      {
        path: "/v1/datasets/weekly-deaths-region/editions/time-series",
        queryParameters: [],
        canonicalRawQuery: "",
      },
      {
        path: "/v1/datasets/weekly-deaths-region/editions/time-series/versions/121",
        queryParameters: [],
        canonicalRawQuery: "",
      },
      {
        path:
          "/v1/datasets/weekly-deaths-region/editions/time-series/versions/121/" +
          "observations",
        queryParameters: [
          { name: "time", value: "2026" },
          { name: "geography", value: "E92000001" },
          { name: "week", value: "week-24" },
          { name: "causeofdeath", value: "all-causes" },
        ],
        canonicalRawQuery:
          "time=2026&geography=E92000001&week=week-24&causeofdeath=all-causes",
      },
    ],
    allowCallerUrl: false,
    allowCredentials: false,
    maxRedirects: 0,
    connectTimeoutMs: 2_000,
    responseTimeoutMs: 5_000,
    maxCompressedBytes: 262_144,
    maxDecompressedBytes: 1_048_576,
    maxAttempts: 2,
    retryableStatuses: [429, 502, 503, 504],
    maxRetryAfterSeconds: 5,
  });
  assert.equal(record.estimate.confidence, "upper-bound");
  if (record.estimate.confidence !== "upper-bound") {
    assert.fail("The ONS preflight must use an upper-bound estimate");
  }
  assert.deepEqual(record.estimate, {
    confidence: "upper-bound",
    maxObservations: 1,
    maxAttempts: 2,
    maxCompressedResponseBytes: 262_144,
    maxDecompressedResponseBytes: 1_048_576,
    maxCanonicalResponseBytes: 262_144,
  });
  assert.equal(record.rights.licence, "Open Government Licence v3.0");
  assert.equal(
    record.rights.licenceUri,
    "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
  );
  assert.equal(
    record.rights.attribution,
    "Source: Office for National Statistics licensed under the Open Government Licence v.3.0",
  );
  assert.deepEqual(record.rights.exceptions, [
    "The ONS logo is excluded and is not retrieved or redistributed.",
    "Any record-level third-party exception overrides this general evidence and must fail closed.",
    "The selected aggregate dataset page stated no additional exception when reviewed.",
  ]);
  assert.deepEqual(record.rights.evidenceUris, [
    "https://www.ons.gov.uk/datasets/weekly-deaths-region/editions/time-series/versions/121",
    "https://www.ons.gov.uk/help/terms-conditions",
    "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
  ]);
  assert.equal(record.rights.reviewedAt, "2026-08-20T17:40:35Z");
  assert.deepEqual(createOnsDataApiAdapter().licence_evidence(), record.rights);
  assert.equal(record.probe.credentialsUsed, false);
  assert.equal(record.probe.payloadStored, false);
  assert.deepEqual(record.probe.selection, [
    { dimension: "time", option: "2026" },
    { dimension: "geography", option: "E92000001" },
    { dimension: "week", option: "week-24" },
    { dimension: "causeofdeath", option: "all-causes" },
  ]);
  assert.equal(record.dependency.workItem, "EXEC-202");
  assert.equal(record.dependency.status, "accepted");
  assert.equal(
    record.dependency.acceptedCommit,
    "6837af6eaa01ffb45e7da08d6a9131cedd1b1a0b",
  );
  assert.deepEqual(record.dependency.providedByExecutionBoundary, [
    "authorised-operation",
    "complexity-budget",
    "deadline",
    "cancellation",
    "trace-context",
    "request-schema",
    "result-schema",
    "error-schema",
  ]);
});

test("allows only the exact reviewed HTTPS origin, path, method and fixed query", () => {
  const policy = preflightRecord().egressPolicy;
  const accepted =
    "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/" +
    "time-series/versions/121/observations?time=2026&geography=E92000001&" +
    "week=week-24&causeofdeath=all-causes";

  assert.equal(
    assertFixedEgressTarget(policy, {
      method: "GET",
      redirectCount: 0,
      url: accepted,
    }).href,
    accepted,
  );

  const rejected = [
    accepted.replace("https://", "http://"),
    accepted.replace("api.beta.ons.gov.uk", "api.beta.ons.gov.uk.evil.invalid"),
    accepted.replace("https://", "https://user:secret@"),
    accepted.replace("api.beta.ons.gov.uk", "api.beta.ons.gov.uk:444"),
    accepted.replace("versions/121", "versions/122"),
    `${accepted}&url=https%3A%2F%2Fevil.invalid`,
    accepted.replace("time=2026", "time=2025"),
    accepted.replace("geography=E92000001", "geography=E92000002"),
    accepted.replace("week=week-24", "week=week-25"),
    accepted.replace("causeofdeath=all-causes", "causeofdeath=heart-disease"),
    `${accepted}&time=2025`,
    accepted.replace(
      "time=2026&geography=E92000001",
      "geography=E92000001&time=2026",
    ),
    accepted.replace("time=2026", "time=*"),
    accepted.replace("time=2026", "t%69me=2026"),
    accepted.replace("time=2026", "time=%32%30%32%36"),
    accepted.replace("week=week-24", "week=week%2D24"),
    `${accepted}&`,
    accepted.replace("&week=week-24", ""),
    `${accepted}#fragment`,
  ];

  for (const url of rejected) {
    assert.throws(
      () => assertFixedEgressTarget(policy, { method: "GET", redirectCount: 0, url }),
      ProviderAdapterFault,
    );
  }
  assert.throws(
    () => assertFixedEgressTarget(policy, { method: "POST", redirectCount: 0, url: accepted }),
    ProviderAdapterFault,
  );
  assert.throws(
    () => assertFixedEgressTarget(policy, { method: "GET", redirectCount: 1, url: accepted }),
    ProviderAdapterFault,
  );
});

test("allows exact metadata routes without accepting a caller-selected dataset", () => {
  const policy = preflightRecord().egressPolicy;
  for (const path of [
    "/v1/datasets/weekly-deaths-region/editions/time-series",
    "/v1/datasets/weekly-deaths-region/editions/time-series/versions/121",
  ]) {
    assert.equal(
      assertFixedEgressTarget(policy, {
        method: "GET",
        redirectCount: 0,
        url: `https://api.beta.ons.gov.uk${path}`,
      }).pathname,
      path,
    );
  }
  assert.throws(
    () =>
      assertFixedEgressTarget(policy, {
        method: "GET",
        redirectCount: 0,
        url: "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series?",
      }),
    ProviderAdapterFault,
  );
  assert.throws(
    () =>
      assertFixedEgressTarget(policy, {
        method: "GET",
        redirectCount: 0,
        url: "https://api.beta.ons.gov.uk/v1/datasets/caller-selected/editions/current",
      }),
    ProviderAdapterFault,
  );
});

test("rejects malformed or unbounded fixed-egress policy records", () => {
  const policy = preflightRecord().egressPolicy;
  const candidate = {
    method: "GET",
    redirectCount: 0,
    url:
      "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/" +
      "time-series/versions/121",
  };
  const malformed = [
    { ...policy, origin: "http://api.beta.ons.gov.uk" },
    { ...policy, allowCallerUrl: true },
    { ...policy, maxAttempts: 4 },
    { ...policy, retryableStatuses: [] },
    {
      ...policy,
      routes: [
        {
          path: "/v1/datasets/example",
          queryParameters: [
            { name: "time", value: "2026" },
            { name: "time", value: "2025" },
          ],
          canonicalRawQuery: "time=2026&time=2025",
        },
      ],
    },
    {
      ...policy,
      routes: [
        {
          path: "/v1/datasets/example",
          queryParameters: [{ name: "time", value: "2026" }],
          canonicalRawQuery: "x".repeat(4_097),
        },
      ],
    },
    {
      ...policy,
      routes: [
        {
          path: "/v1/datasets/example",
          queryParameters: [{ name: "time", value: "2026" }],
          canonicalRawQuery: "time=%32%30%32%36",
        },
      ],
    },
    {
      ...policy,
      routes: [
        {
          path: "/v1/datasets/example",
          queryParameters: [{ name: "time", value: "*" }],
          canonicalRawQuery: "time=*",
        },
      ],
    },
  ];

  for (const invalid of malformed) {
    assert.throws(
      () => assertFixedEgressTarget(invalid as unknown as FixedEgressPolicy, candidate),
      TypeError,
    );
  }
});
