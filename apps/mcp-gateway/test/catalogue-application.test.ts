import assert from "node:assert/strict";
import {
  mkdtempSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

import { fromJsonSchema, type JsonSchemaType } from "@modelcontextprotocol/server";

import {
  parseCatalogue,
  type CatalogueBundle,
  type CatalogueRecord,
  type JsonValue,
} from "@gis-ai-go/contracts";
import {
  PublicEvidenceLedgerError,
  openPublicEvidenceLedger,
  verifyInlineReceipt,
} from "@gis-ai-go/evidence";
import { PUBLIC_CATALOGUE_POLICY } from "@gis-ai-go/policy-client";

import {
  assertCatalogueResultSnapshotBounds,
  createCatalogueApplication,
  type CatalogueSearchResult,
} from "../src/catalogue-application.js";
import {
  loadCatalogueSnapshot,
  type CatalogueSnapshot,
} from "../src/catalogue-snapshot.js";
import {
  CatalogueProblemError,
  createCatalogueProblem,
  isCanonicalCatalogueProblemInstance,
  type CatalogueProblemCode,
} from "../src/problem.js";
import { MCP_CATALOGUE_OUTPUT_SCHEMAS } from "../src/mcp-server.js";

const SOURCE_CATALOGUE = fileURLToPath(
  new URL("../../../../artifacts/okf/", import.meta.url),
);
const CONTEXT = Object.freeze({
  requestId: "request-catalogue-test",
  traceId: "0123456789abcdef0123456789abcdef",
});
const SNAPSHOT = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
  now: new Date("2026-08-20T12:00:00Z"),
});
const TEST_APPLICATION_OPTIONS = Object.freeze({
  software: Object.freeze({
    name: "gis-ai-go-mcp-gateway" as const,
    version: "0.1.0",
    revision: "a".repeat(40),
  }),
  now: () => new Date("2026-08-20T12:34:56Z"),
});

function testApplication(snapshot: CatalogueSnapshot = SNAPSHOT) {
  return createCatalogueApplication(snapshot, TEST_APPLICATION_OPTIONS);
}

const APPLICATION = testApplication();
const MUTATION_RECORD_ID = "hmlr:dataset:price-paid-data";

function snapshotForBundle(bundle: CatalogueBundle): CatalogueSnapshot {
  return Object.freeze({
    ...SNAPSHOT,
    bundle,
    recordsById: new Map(bundle.records.map((record) => [record.id, record])),
    recordCount: bundle.records.length,
  });
}

function parserValidSnapshotWithRecord(
  overrides: Partial<CatalogueRecord>,
): CatalogueSnapshot {
  const records = SNAPSHOT.bundle.records.map((record) =>
    record.id === MUTATION_RECORD_ID ? { ...record, ...overrides } : record,
  );
  return snapshotForBundle(parseCatalogue({ ...SNAPSHOT.bundle, records }));
}

function uncheckedSnapshotWithRecord(
  overrides: Partial<CatalogueRecord>,
): CatalogueSnapshot {
  const records = SNAPSHOT.bundle.records.map((record) =>
    record.id === MUTATION_RECORD_ID ? { ...record, ...overrides } : record,
  );
  const bundle = { ...SNAPSHOT.bundle, records } satisfies CatalogueBundle;
  return snapshotForBundle(bundle);
}

function expectProblem(run: () => unknown, code: CatalogueProblemCode): CatalogueProblemError {
  let captured: CatalogueProblemError | undefined;
  assert.throws(run, (error: unknown) => {
    assert.ok(error instanceof CatalogueProblemError);
    assert.equal(error.problem.code, code);
    assert.equal(error.problem.request_id, CONTEXT.requestId);
    assert.equal(error.problem.trace_id, CONTEXT.traceId);
    captured = error;
    return true;
  });
  assert.ok(captured);
  return captured;
}

function firstIds(result: CatalogueSearchResult): readonly string[] {
  return result.data.records.map(({ id }) => id);
}

test("search returns governed Price Paid and INSPIRE summaries with controlled facets", () => {
  const pricePaid = APPLICATION.search(
    { query: "Price Paid", facets: { types: ["dataset"] } },
    CONTEXT,
  );
  assert.equal(pricePaid.operation, "catalogue.search");
  assert.equal(pricePaid.catalogue.content_root_sha256, SNAPSHOT.contentRootSha256);
  assert.equal(pricePaid.catalogue.record_count, SNAPSHOT.recordCount);
  assert.equal(pricePaid.data.records[0]?.id, "hmlr:dataset:price-paid-data");
  assert.equal(pricePaid.data.records[0]?.authority, "source-authoritative");
  assert.equal(pricePaid.data.records[0]?.rights, "open-with-conditions");
  assert.ok(pricePaid.data.facets.types.some(({ value }) => value === "dataset"));
  assert.equal(pricePaid.evidence_receipt.schema, "gis-ai-go.evidence-receipt.v1");
  assert.equal(pricePaid.evidence_receipt.operation.name, "catalogue.search");
  assert.equal(pricePaid.evidence_receipt.policy_decision.effect, "allow-with-obligations");
  assert.equal(pricePaid.evidence_receipt.policy_decision.policy_default_effect, "deny");
  assert.deepEqual(
    pricePaid.evidence_receipt.licence_obligations.map(({ record_id: id }) => id),
    pricePaid.data.records.map(({ id }) => id).sort(),
  );
  assert.deepEqual(pricePaid.evidence_receipt.evidence_handling, {
    attestation: "not-attested",
    delivery: "inline-only",
    persistence: "not-persisted",
  });
  assert.equal(Object.isFrozen(pricePaid), true);
  assert.equal(Object.isFrozen(pricePaid.evidence_receipt), true);
  assert.equal(JSON.stringify(pricePaid.evidence_receipt).includes("Price Paid"), false);

  const { evidence_receipt: pricePaidReceipt, ...pricePaidCore } = pricePaid;
  const receiptVerification = verifyInlineReceipt(pricePaidReceipt, {
    normalisedParameters: {
      query: "price paid",
      facets: {
        types: ["dataset"],
        authority: [],
        access: [],
        rights: [],
        freshness: [],
        tags: [],
      },
      limit: 20,
      offset: 0,
    },
    resultCore: pricePaidCore,
    publicPolicy: PUBLIC_CATALOGUE_POLICY,
    expectedCatalogue: pricePaid.catalogue,
    expectedSoftware: TEST_APPLICATION_OPTIONS.software,
    licenceObligations: pricePaidReceipt.licence_obligations,
  });
  assert.equal(receiptVerification.valid, true, receiptVerification.errors.join("; "));

  const inspire = APPLICATION.search(
    { query: "INSPIRE", facets: { tags: ["inspire"] }, limit: 100 },
    CONTEXT,
  );
  assert.ok(firstIds(inspire).includes("hmlr:dataset:inspire-index-polygons"));
  assert.ok(
    firstIds(inspire).includes("hmlr:dataset:local-land-charges-inspire"),
  );
  assert.equal(inspire.data.page.returned, inspire.data.records.length);
  assert.equal(inspire.data.page.next_cursor, null);
});

test("inline receipt verification rejects parameter replay and result or rights tampering", () => {
  const result = APPLICATION.search({ query: "Price Paid", limit: 1 }, CONTEXT);
  const { evidence_receipt: receipt, ...resultCore } = result;
  const normalisedParameters = {
    query: "price paid",
    facets: {
      types: [],
      authority: [],
      access: [],
      rights: [],
      freshness: [],
      tags: [],
    },
    limit: 1,
    offset: 0,
  };
  const expectedLicences = receipt.licence_obligations;

  const replay = verifyInlineReceipt(receipt, {
    normalisedParameters: { ...normalisedParameters, offset: 1 },
    resultCore,
    publicPolicy: PUBLIC_CATALOGUE_POLICY,
    licenceObligations: expectedLicences,
  });
  assert.equal(replay.valid, false);

  const changedResult = {
    ...resultCore,
    data: {
      ...resultCore.data,
      page: {
        ...resultCore.data.page,
        matched: resultCore.data.page.matched + 1,
      },
    },
  };
  const resultTamper = verifyInlineReceipt(receipt, {
    normalisedParameters,
    resultCore: changedResult,
    publicPolicy: PUBLIC_CATALOGUE_POLICY,
    licenceObligations: expectedLicences,
  });
  assert.equal(resultTamper.valid, false);

  const changedReceipt = {
    ...receipt,
    licence_obligations: receipt.licence_obligations.map((obligation, index) =>
      index === 0 ? { ...obligation, attribution: "Changed attribution" } : obligation,
    ),
  };
  const rightsTamper = verifyInlineReceipt(changedReceipt, {
    normalisedParameters,
    resultCore,
    publicPolicy: PUBLIC_CATALOGUE_POLICY,
    licenceObligations: expectedLicences,
  });
  assert.equal(rightsTamper.valid, false);
});

test("returns a durable reference only after the configured append-only write succeeds", async () => {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-catalogue-evidence-"));
  try {
    const ledger = openPublicEvidenceLedger({
      rootDirectory: root,
      retentionDays: 365,
      now: () => new Date("2026-08-20T12:34:57Z"),
    });
    const application = createCatalogueApplication(SNAPSHOT, {
      ...TEST_APPLICATION_OPTIONS,
      evidenceLedger: ledger,
    });
    const context = {
      requestId: "request-durable-catalogue-001",
      traceId: "1123456789abcdef0123456789abcdef",
    };
    const result = application.search({ query: "Price Paid", limit: 1 }, context);

    assert.equal(result.evidence_storage?.status, "persisted");
    assert.equal(result.evidence_storage?.ledger_id, ledger.descriptor.ledger_id);
    assert.deepEqual(
      ledger.inspect(result.evidence_receipt.receipt_id)?.reference,
      result.evidence_storage,
    );
    const outputSchema = fromJsonSchema<unknown>(
      MCP_CATALOGUE_OUTPUT_SCHEMAS["catalogue.search"] as JsonSchemaType,
    );
    const outputValidation = await outputSchema["~standard"].validate(result);
    assert.equal(outputValidation.issues, undefined);
    assert.equal(result.evidence_receipt.evidence_handling.persistence, "not-persisted");
    assert.equal("evidence_storage" in APPLICATION.search({}, CONTEXT), false);

    const eventName = readdirSync(join(root, "events"))[0]!;
    const eventPath = join(root, "events", eventName);
    const event = readFileSync(eventPath, "utf8");
    writeFileSync(eventPath, event.slice(0, -1));
    assert.throws(
      () =>
        application.search(
          { query: "INSPIRE", limit: 1 },
          {
            requestId: "request-durable-catalogue-002",
            traceId: "2123456789abcdef0123456789abcdef",
          },
        ),
      (error: unknown) => {
        assert.ok(error instanceof PublicEvidenceLedgerError);
        assert.equal(error.code, "truncation");
        return true;
      },
    );
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("application creation requires exact software identity and a valid injected clock", () => {
  const invalidOptions = [
    {},
    { software: TEST_APPLICATION_OPTIONS.software, unexpected: true },
    { software: { ...TEST_APPLICATION_OPTIONS.software, name: "other-gateway" } },
    { software: { ...TEST_APPLICATION_OPTIONS.software, version: "0.1.0-dev" } },
    { software: { ...TEST_APPLICATION_OPTIONS.software, revision: "A".repeat(40) } },
    { software: TEST_APPLICATION_OPTIONS.software, now: "not-a-function" },
  ] as const;
  for (const options of invalidOptions) {
    assert.throws(
      () => createCatalogueApplication(SNAPSHOT, options as never),
      TypeError,
    );
  }

  const invalidClock = createCatalogueApplication(SNAPSHOT, {
    software: TEST_APPLICATION_OPTIONS.software,
    now: () => new Date(Number.NaN),
  });
  assert.throws(() => invalidClock.search({}, CONTEXT), /clock must return a valid Date/u);
});

test("application creation rejects parser-valid records outside the result contract", () => {
  const base = SNAPSHOT.recordsById.get(MUTATION_RECORD_ID);
  assert.ok(base);

  const cases: readonly [string, Partial<CatalogueRecord>][] = [
    ["title", { title: "t".repeat(513) }],
    ["description", { description: "d".repeat(4_097) }],
    [
      "authority.statement",
      { authority: { ...base.authority, statement: "s".repeat(4_097) } },
    ],
    [
      "authority.source",
      { authority: { ...base.authority, source: "s".repeat(513) } },
    ],
    [
      "access.authentication",
      { access: { ...base.access, authentication: "a".repeat(513) } },
    ],
    [
      "rights.recordLicence",
      { rights: { ...base.rights, recordLicence: "r".repeat(2_049) } },
    ],
    [
      "rights.describedResourceLicence",
      {
        rights: {
          ...base.rights,
          describedResourceLicence: "r".repeat(2_049),
        },
      },
    ],
    [
      "rights.attribution",
      { rights: { ...base.rights, attribution: "a".repeat(8_193) } },
    ],
    ["limitations", { limitations: Array.from({ length: 51 }, (_, index) => `l-${index}`) }],
    ["limitations[0]", { limitations: ["l".repeat(2_049)] }],
    ["tags", { tags: Array.from({ length: 51 }, (_, index) => `tag-${index}`) }],
    ["tags[0]", { tags: ["t".repeat(129)] }],
  ];

  for (const [path, overrides] of cases) {
    const snapshot = parserValidSnapshotWithRecord(overrides);
    assert.throws(() => testApplication(snapshot), (error: unknown) => {
      assert.ok(error instanceof Error);
      assert.match(error.message, /^Catalogue result contract rejected at /u);
      assert.ok(error.message.includes(path));
      return true;
    });
  }
});

test("result bounds reject excessive source references, facets and source-native details", () => {
  const base = SNAPSHOT.recordsById.get(MUTATION_RECORD_ID);
  assert.ok(base);

  const sourceRefs = Array.from({ length: 100 }, (_, index) => `source:${index}`);
  assert.throws(
    () => testApplication(uncheckedSnapshotWithRecord({ sourceRefs })),
    /sourceRefs/u,
  );

  const tooManyProperties = Object.fromEntries(
    Array.from({ length: 257 }, (_, index) => [`property${index}`, index]),
  );
  const detailCases: readonly Readonly<Record<string, JsonValue>>[] = [
    tooManyProperties,
    { ["k".repeat(257)]: true },
    { text: "x".repeat(65_537) },
    { values: Array.from({ length: 10_001 }, () => null) },
  ];
  for (const details of detailCases) {
    assert.throws(
      () => testApplication(uncheckedSnapshotWithRecord({ details })),
      /details/u,
    );
  }

  const records = SNAPSHOT.bundle.records.map((record, recordIndex) => ({
    ...record,
    tags: Array.from({ length: 3 }, (_, tagIndex) =>
      `facet-${recordIndex}-${tagIndex}`,
    ),
  }));
  const facetSnapshot = snapshotForBundle(
    parseCatalogue({ ...SNAPSHOT.bundle, records }),
  );
  assert.throws(
    () => assertCatalogueResultSnapshotBounds(facetSnapshot),
    /facets\.tags.*100 options/u,
  );
});

test("pagination is deterministic and rejects tampering or replay", () => {
  const first = APPLICATION.search({ query: "HMLR", limit: 1 }, CONTEXT);
  assert.equal(first.data.records.length, 1);
  assert.ok(first.data.page.matched > 1);
  assert.ok(first.data.page.next_cursor);
  const cursor = first.data.page.next_cursor;

  const second = APPLICATION.search({ query: "hmlr", limit: 1, cursor }, CONTEXT);
  assert.equal(second.data.records.length, 1);
  assert.notEqual(second.data.records[0]?.id, first.data.records[0]?.id);
  assert.equal(second.data.page.matched, first.data.page.matched);

  const alteredFinalCharacter = cursor.endsWith("0") ? "1" : "0";
  expectProblem(
    () =>
      APPLICATION.search(
        { query: "HMLR", limit: 1, cursor: `${cursor.slice(0, -1)}${alteredFinalCharacter}` },
        CONTEXT,
      ),
    "invalid_cursor",
  );
  expectProblem(
    () => APPLICATION.search({ query: "INSPIRE", limit: 1, cursor }, CONTEXT),
    "invalid_cursor",
  );

  const changedSnapshot = Object.freeze({
    ...SNAPSHOT,
    contentRootSha256: "f".repeat(64),
  }) satisfies CatalogueSnapshot;
  const changedApplication = testApplication(changedSnapshot);
  expectProblem(
    () => changedApplication.search({ query: "HMLR", limit: 1, cursor }, CONTEXT),
    "invalid_cursor",
  );
});

test("query limits count normalised terms and Unicode code points", () => {
  const tenTerms = "one two three four five six seven eight nine ten";
  assert.doesNotThrow(() => APPLICATION.search({ query: tenTerms }, CONTEXT));

  const elevenTerms = `${tenTerms} eleven`;
  const tooManyTerms = expectProblem(
    () => APPLICATION.search({ query: elevenTerms }, CONTEXT),
    "complexity_limit_exceeded",
  );
  assert.equal(tooManyTerms.problem.errors?.[0]?.path, "$.query");

  const astralCharacter = "𐐀";
  assert.doesNotThrow(() =>
    APPLICATION.search({ query: astralCharacter.repeat(256) }, CONTEXT),
  );
  expectProblem(
    () => APPLICATION.search({ query: astralCharacter.repeat(257) }, CONTEXT),
    "invalid_request",
  );

  const unpairedSurrogate = expectProblem(
    () => APPLICATION.search({ query: "\ud800" }, CONTEXT),
    "invalid_request",
  );
  assert.deepEqual(unpairedSurrogate.problem.errors, [
    {
      path: "$.query",
      code: "invalid_value",
      message: "Query must contain valid Unicode scalar values.",
    },
  ]);
});

test("closed requests reject unknown properties, facet values and tags", () => {
  const safeUnknown = expectProblem(
    () => APPLICATION.search({ provider: "hmlr" }, CONTEXT),
    "invalid_request",
  );
  assert.equal(safeUnknown.problem.errors?.[0]?.path, "$.provider");
  assert.equal(
    safeUnknown.problem.errors?.[0]?.message,
    "Remove the unknown property provider.",
  );
  expectProblem(
    () => APPLICATION.search({ facets: { types: ["collection"] } }, CONTEXT),
    "invalid_request",
  );
  expectProblem(
    () => APPLICATION.search({ facets: { tags: ["not-a-governed-tag"] } }, CONTEXT),
    "invalid_request",
  );
  expectProblem(
    () => APPLICATION.search({ facets: { types: ["dataset", "dataset"] } }, CONTEXT),
    "invalid_request",
  );
});

test("hostile unknown property identities remain controlled catalogue problems", () => {
  const hostileKeys = ["x".repeat(300), "unsafe\nproperty", "\ud800"] as const;
  for (const key of hostileKeys) {
    const root = expectProblem(
      () => APPLICATION.search({ [key]: true }, CONTEXT),
      "invalid_request",
    );
    assert.equal(root.problem.detail, "Remove the unknown property.");
    assert.deepEqual(root.problem.errors, [
      {
        path: "$",
        code: "unknown_property",
        message: "Remove the unknown property.",
      },
    ]);

    const nested = expectProblem(
      () => APPLICATION.search({ facets: { [key]: true } }, CONTEXT),
      "invalid_request",
    );
    assert.equal(nested.problem.errors?.[0]?.path, "$.facets");
    assert.equal(nested.problem.errors?.[0]?.message, "Remove the unknown property.");
  }
});

test("the central problem factory accepts schema boundaries and rejects invalid envelopes", () => {
  const boundary = createCatalogueProblem(
    "rate_limited",
    {
      requestId: `r${"a".repeat(127)}`,
      traceId: "f".repeat(32),
      instance: "/".repeat(2_048),
    },
    {
      detail: "𐐀".repeat(1_024),
      retryAfterSeconds: 3_600,
      errors: Array.from({ length: 20 }, (_, index) => ({
        path: `$.field${index}`,
        code: "invalid_value" as const,
        message: index === 0 ? "m".repeat(512) : `Invalid value ${index}.`,
      })),
    },
  );
  assert.equal(boundary.status, 429);
  assert.equal(boundary.type, "urn:gis-ai-go:problem:rate-limited");
  assert.equal(boundary.errors?.length, 20);
  assert.equal(isCanonicalCatalogueProblemInstance("/catalogue/records:hmlr"), true);
  assert.equal(isCanonicalCatalogueProblemInstance("/%41"), false);
  assert.equal(isCanonicalCatalogueProblemInstance("/%2f"), false);
  assert.equal(isCanonicalCatalogueProblemInstance("/%ZZ"), false);
  assert.equal(isCanonicalCatalogueProblemInstance("not/a/path"), false);

  const validContext = { requestId: "request-1", traceId: "a".repeat(32) };
  const invalidRuns: readonly (() => unknown)[] = [
    () => createCatalogueProblem("invalid_request", { ...validContext, requestId: "" }),
    () =>
      createCatalogueProblem("invalid_request", {
        ...validContext,
        requestId: `r${"a".repeat(128)}`,
      }),
    () => createCatalogueProblem("invalid_request", { ...validContext, traceId: "A".repeat(32) }),
    () =>
      createCatalogueProblem("invalid_request", {
        ...validContext,
        instance: "/".repeat(2_049),
      }),
    () =>
      createCatalogueProblem("invalid_request", {
        ...validContext,
        instance: "not a URI",
      }),
    () =>
      createCatalogueProblem("invalid_request", {
        ...validContext,
        instance: "/requests/not canonical",
      }),
    () =>
      createCatalogueProblem("invalid_request", {
        ...validContext,
        instance: "/requests/%6fver-encoded",
      }),
    () => createCatalogueProblem("invalid_request", validContext, { detail: "" }),
    () =>
      createCatalogueProblem("invalid_request", validContext, {
        detail: "d".repeat(1_025),
      }),
    () =>
      createCatalogueProblem("invalid_request", validContext, {
        detail: "unsafe\u0000detail",
      }),
    () =>
      createCatalogueProblem("rate_limited", validContext, { retryAfterSeconds: 0 }),
    () =>
      createCatalogueProblem("rate_limited", validContext, { retryAfterSeconds: 3_601 }),
    () =>
      createCatalogueProblem("rate_limited", validContext, { retryAfterSeconds: 1.5 }),
    () => createCatalogueProblem("invalid_request", validContext, { errors: [] }),
    () =>
      createCatalogueProblem("invalid_request", validContext, {
        errors: Array.from({ length: 21 }, (_, index) => ({
          path: `$.field${index}`,
          code: "invalid_value" as const,
          message: `Invalid value ${index}.`,
        })),
      }),
    () =>
      createCatalogueProblem("invalid_request", validContext, {
        errors: [
          { path: "$.field", code: "invalid_value", message: "Invalid." },
          { path: "$.field", code: "invalid_value", message: "Invalid." },
        ],
      }),
    () =>
      createCatalogueProblem("invalid_request", validContext, {
        errors: [{ path: "", code: "invalid_value", message: "Invalid." }],
      }),
    () =>
      createCatalogueProblem("invalid_request", validContext, {
        errors: [{ path: "$.field", code: "invalid_value", message: "" }],
      }),
    () =>
      createCatalogueProblem("invalid_request", validContext, {
        errors: [
          { path: "$.field", code: "not-controlled" as never, message: "Invalid." },
        ],
      }),
    () =>
      createCatalogueProblem("invalid_request", validContext, {
        errors: [
          {
            path: "$.field",
            code: "invalid_value",
            message: "Invalid.",
            unexpected: true,
          } as never,
        ],
      }),
  ];
  for (const run of invalidRuns) assert.throws(run, TypeError);
});

test("success envelopes reject invalid request and trace identities", () => {
  const invalidContexts = [
    { requestId: "unsafe request", traceId: "a".repeat(32) },
    { requestId: "request-1", traceId: "A".repeat(32) },
  ] as const;

  for (const context of invalidContexts) {
    assert.throws(() => APPLICATION.search({}, context), TypeError);
    assert.throws(
      () => APPLICATION.describe({ record_id: "hmlr:dataset:price-paid-data" }, context),
      TypeError,
    );
  }
});

test("semantically equivalent search criteria produce byte-equivalent values", () => {
  const first = APPLICATION.search(
    {
      query: "  PRICE   paid ",
      facets: {
        types: ["source", "dataset"],
        rights: ["metadata-citation", "open-with-conditions"],
      },
      limit: 5,
    },
    CONTEXT,
  );
  const second = APPLICATION.search(
    {
      limit: 5,
      facets: {
        rights: ["open-with-conditions", "metadata-citation"],
        types: ["dataset", "source"],
      },
      query: "price paid",
    },
    CONTEXT,
  );
  assert.deepEqual(first, second);
  assert.equal(JSON.stringify(first), JSON.stringify(second));
});

test("describe preserves full governed fields and stable source expansions", () => {
  const result = APPLICATION.describe(
    { record_id: "hmlr:dataset:price-paid-data" },
    CONTEXT,
  );
  assert.equal(result.operation, "catalogue.describe");
  assert.equal(result.data.record.id, "hmlr:dataset:price-paid-data");
  assert.equal(result.data.record.authority.class, "source-authoritative");
  assert.equal(result.data.record.publication.contains_personal_data, false);
  assert.equal(result.data.record.publication.contains_protected_data, false);
  assert.equal(result.data.record.access.tier, "open");
  assert.equal(result.data.record.rights.state, "open-with-conditions");
  assert.match(result.data.record.rights.attribution, /Land Registry/u);
  assert.ok(result.data.record.limitations.length > 0);
  assert.ok(result.data.record.source_refs.length > 0);
  assert.equal("sourceRefs" in result.data.record, false);
  assert.equal("recordLicence" in result.data.record.rights, false);
  assert.equal(result.data.record.details.sourceNativeId, "hmlr:dataset:price-paid-data");

  const relationshipIds = result.data.included.relationships?.map(({ record_id: id }) => id);
  const sourceIds = result.data.included.sources?.map(({ id }) => id);
  assert.deepEqual(relationshipIds, [...(relationshipIds ?? [])].sort());
  assert.deepEqual(sourceIds, relationshipIds);
  assert.ok(result.data.included.sources?.every((source) => source.title.length > 0));

  assert.equal(result.evidence_receipt.operation.name, "catalogue.describe");
  const evidencedRecordIds = [result.data.record.id, ...(sourceIds ?? [])].sort();
  assert.equal(
    result.evidence_receipt.result.returned_record_count,
    evidencedRecordIds.length,
  );
  assert.deepEqual(
    result.evidence_receipt.licence_obligations.map(({ record_id: id }) => id),
    evidencedRecordIds,
  );
  const { evidence_receipt: receipt, ...resultCore } = result;
  const verification = verifyInlineReceipt(receipt, {
    normalisedParameters: {
      record_id: "hmlr:dataset:price-paid-data",
      include: ["relationships", "sources"],
    },
    resultCore,
    publicPolicy: PUBLIC_CATALOGUE_POLICY,
    licenceObligations: receipt.licence_obligations,
  });
  assert.equal(verification.valid, true, verification.errors.join("; "));
});

test("describe include order is canonical and IDs are exact and case-sensitive", () => {
  const sourcesFirst = APPLICATION.describe(
    {
      record_id: "hmlr:dataset:inspire-index-polygons",
      include: ["sources", "relationships"],
    },
    CONTEXT,
  );
  const relationshipsFirst = APPLICATION.describe(
    {
      include: ["relationships", "sources"],
      record_id: "hmlr:dataset:inspire-index-polygons",
    },
    CONTEXT,
  );
  assert.deepEqual(sourcesFirst, relationshipsFirst);
  assert.equal(JSON.stringify(sourcesFirst), JSON.stringify(relationshipsFirst));

  const sourcesOnly = APPLICATION.describe(
    { record_id: "hmlr:dataset:inspire-index-polygons", include: ["sources"] },
    CONTEXT,
  );
  assert.equal("sources" in sourcesOnly.data.included, true);
  assert.equal("relationships" in sourcesOnly.data.included, false);

  expectProblem(
    () => APPLICATION.describe({ record_id: "HMLR:DATASET:INSPIRE-INDEX-POLYGONS" }, CONTEXT),
    "record_not_found",
  );
  expectProblem(
    () => APPLICATION.describe({ record_id: "missing:record" }, CONTEXT),
    "record_not_found",
  );

  const safeMissingId = "s".repeat(512);
  const safeMissing = expectProblem(
    () => APPLICATION.describe({ record_id: safeMissingId }, CONTEXT),
    "record_not_found",
  );
  assert.ok(safeMissing.problem.detail?.includes(safeMissingId));

  const hostileMissing = expectProblem(
    () => APPLICATION.describe({ record_id: "missing\nrecord" }, CONTEXT),
    "record_not_found",
  );
  assert.equal(
    hostileMissing.problem.detail,
    "No catalogue record has the supplied exact ID.",
  );
  assert.equal(hostileMissing.problem.detail?.includes("missing\nrecord"), false);
});

test("describe does not duplicate a self-referencing source projection or licence", () => {
  const result = APPLICATION.describe({ record_id: "S-ARAZZO" }, CONTEXT);
  assert.deepEqual(result.data.record.source_refs, ["S-ARAZZO"]);
  assert.deepEqual(result.data.included.relationships, [
    { relation: "source", record_id: "S-ARAZZO" },
  ]);
  assert.deepEqual(result.data.included.sources, []);
  assert.deepEqual(
    result.evidence_receipt.licence_obligations.map(({ record_id: id }) => id),
    ["S-ARAZZO"],
  );
  assert.equal(result.evidence_receipt.result.returned_record_count, 1);
});
