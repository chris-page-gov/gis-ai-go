import assert from "node:assert/strict";
import test from "node:test";

import {
  DEFAULT_BOUNDARY_CAVEAT,
  DEFAULT_RECORD_ID,
  MAX_CATALOGUE_JSON_BYTES,
  MAX_CATALOGUE_QUERY_LENGTH,
  MAX_CATALOGUE_QUERY_TERMS,
  analyseCatalogueQuery,
  deriveFacetOptions,
  deriveGraph,
  deriveTimeline,
  facetLabel,
  parseCatalogue,
  parseCatalogueJson,
  searchRecords,
  type CatalogueBundle,
  type ExplorerState,
} from "../src/index.js";
import { validCatalogueFixture } from "./fixtures.js";

function cloneFixture(): ReturnType<typeof validCatalogueFixture> {
  return structuredClone(validCatalogueFixture());
}

function defaultState(bundle: CatalogueBundle): ExplorerState {
  return {
    view: "cards",
    query: "",
    types: [],
    authority: [],
    access: [],
    rights: [],
    freshness: [],
    tags: [],
    selectedRecordId: bundle.records[0]?.id ?? null,
  };
}

test("accepts the bounded public fixture and preserves the legal-boundary caveat", () => {
  const bundle = parseCatalogue(cloneFixture());
  assert.equal(bundle.recordCount, 2);
  assert.ok(
    bundle.records
      .find((record) => record.id === DEFAULT_RECORD_ID)
      ?.limitations.includes(DEFAULT_BOUNDARY_CAVEAT),
  );
  assert.deepEqual(parseCatalogueJson(JSON.stringify(validCatalogueFixture())), bundle);
});

test("rejects oversized or malformed JSON before it reaches the model", () => {
  assert.throws(() => parseCatalogueJson("{"), /not valid JSON/);
  const oversized = `{"padding":"${"a".repeat(MAX_CATALOGUE_JSON_BYTES)}"}`;
  assert.throws(() => parseCatalogueJson(oversized), /exceeds/);
});

test("rejects protected flags and non-open access at record and bundle boundaries", () => {
  const protectedRecord = cloneFixture();
  protectedRecord.records[0]!.publication.containsProtectedData = true;
  assert.throws(() => parseCatalogue(protectedRecord), /containsProtectedData/);

  const personalRecord = cloneFixture();
  personalRecord.records[0]!.publication.containsPersonalData = true;
  assert.throws(() => parseCatalogue(personalRecord), /containsPersonalData/);

  const protectedBundle = cloneFixture();
  protectedBundle.scope.containsProtectedData = true;
  assert.throws(() => parseCatalogue(protectedBundle), /containsProtectedData/);

  const protectedTier = cloneFixture();
  protectedTier.records[0]!.access.tier = "protected" as "open";
  assert.throws(() => parseCatalogue(protectedTier), /tier/);
});

test("rejects extra fields, duplicate IDs and unresolved source references", () => {
  const extraFixture = cloneFixture();
  Object.assign(extraFixture.records[0]!, { unexpected: true });
  assert.throws(() => parseCatalogue(extraFixture), /expected keys/);

  const duplicateFixture = cloneFixture();
  duplicateFixture.records[1]!.id = duplicateFixture.records[0]!.id;
  duplicateFixture.records[0]!.sourceRefs = [duplicateFixture.records[0]!.id];
  duplicateFixture.records[1]!.sourceRefs = [duplicateFixture.records[0]!.id];
  assert.throws(() => parseCatalogue(duplicateFixture), /record IDs must be unique/);

  const unresolvedFixture = cloneFixture();
  unresolvedFixture.records[0]!.sourceRefs = ["source:missing"];
  assert.throws(() => parseCatalogue(unresolvedFixture), /unresolved source reference/);
});

test("rejects unsafe HTML, controls, bidi text and unsafe navigable URLs", () => {
  const markup = cloneFixture();
  markup.records[0]!.title = '<img src=x onerror="globalThis.pwned=true">';
  assert.throws(() => parseCatalogue(markup), /HTML-like/);

  const control = cloneFixture();
  control.records[0]!.description = "Trusted\u0007evil";
  assert.throws(() => parseCatalogue(control), /unsafe control/);

  const bidi = cloneFixture();
  bidi.records[0]!.description = "Trusted\u202eevil";
  assert.throws(() => parseCatalogue(bidi), /unsafe control/);

  const unsafeUrl = cloneFixture();
  unsafeUrl.records[0]!.details.url = "javascript:alert(1)";
  assert.throws(() => parseCatalogue(unsafeUrl), /navigable URL/);

  const credentials = cloneFixture();
  credentials.records[0]!.authority.source = "https://user:secret@example.org/record";
  assert.throws(() => parseCatalogue(credentials), /authority URL is unsafe/);
});

test("rejects invalid calendar values and malformed release identity", () => {
  const invalidDate = cloneFixture();
  Object.assign(invalidDate.records[0]!.details, { retrieved: "2026-02-30" });
  assert.throws(() => parseCatalogue(invalidDate), /valid calendar date|RFC 3339/);

  const invalidRevision = cloneFixture();
  invalidRevision.revision = "ABC";
  assert.throws(() => parseCatalogue(invalidRevision), /40-character Git SHA/);

  const invalidVersion = cloneFixture();
  invalidVersion.version = "v1";
  assert.throws(() => parseCatalogue(invalidVersion), /semantic version/);
});

test("rejects a missing legal caveat and dangerous or non-JSON objects", () => {
  const missingCaveat = cloneFixture();
  missingCaveat.records[0]!.limitations = ["Not a complete dataset."];
  assert.throws(() => parseCatalogue(missingCaveat), /indicative-versus-legal-boundary/);

  const dangerous = JSON.parse(
    JSON.stringify(validCatalogueFixture()),
  ) as ReturnType<typeof validCatalogueFixture>;
  Object.defineProperty(dangerous.records[0]!.details, "__proto__", {
    enumerable: true,
    value: { polluted: true },
  });
  assert.throws(() => parseCatalogue(dangerous), /dangerous object key/);

  const nonJsonObject = cloneFixture();
  nonJsonObject.records[0]!.details.publisher = new Date(
    "2026-08-19T00:00:00Z",
  ) as never;
  assert.throws(() => parseCatalogue(nonJsonObject), /plain JSON object/);
});

test("searches only controlled fields with NFKC normalisation and a ten-term cap", () => {
  const bundle = parseCatalogue(cloneFixture());
  const base = defaultState(bundle);
  const state: ExplorerState = {
    ...base,
    query:
      "ＨＭ Land Registry England GML Monthly polygons indicative extent metadata hmlr ignored",
    types: ["dataset"],
    authority: ["source-authoritative"],
    access: ["public"],
    rights: ["open-with-conditions"],
    freshness: ["current"],
    tags: ["inspire"],
  };
  assert.deepEqual(
    searchRecords(bundle.records, state).map((record) => record.id),
    [DEFAULT_RECORD_ID],
  );

  const rightsOnly: ExplorerState = {
    ...base,
    query: "upstream",
  };
  assert.equal(searchRecords(bundle.records, rightsOnly).length, 0);
});

test("reports transport query-limit violations without changing Explorer semantics", () => {
  const exact = analyseCatalogueQuery("one two three four five six seven eight nine ten");
  assert.equal(exact.inputTermCount, MAX_CATALOGUE_QUERY_TERMS);
  assert.equal(exact.exceedsTermLimit, false);
  assert.equal(exact.exceedsCharacterLimit, false);

  const extra = analyseCatalogueQuery(
    "one two three four five six seven eight nine ten eleven",
  );
  assert.equal(extra.inputTermCount, MAX_CATALOGUE_QUERY_TERMS + 1);
  assert.equal(extra.terms.length, MAX_CATALOGUE_QUERY_TERMS);
  assert.equal(extra.exceedsTermLimit, true);

  const maximum = analyseCatalogueQuery("q".repeat(MAX_CATALOGUE_QUERY_LENGTH));
  assert.equal(maximum.exceedsCharacterLimit, false);
  const long = analyseCatalogueQuery("q".repeat(MAX_CATALOGUE_QUERY_LENGTH + 1));
  assert.equal(long.exceedsCharacterLimit, true);
  const astral = analyseCatalogueQuery("😀".repeat(MAX_CATALOGUE_QUERY_LENGTH));
  assert.equal(astral.exceedsCharacterLimit, false);
});

test("searches allowlisted question and provider details but not arbitrary details or rights", () => {
  const bundle = parseCatalogue(cloneFixture());
  const base = defaultState(bundle);
  const template = bundle.records[1]!;
  const question = {
    ...template,
    id: "LR-Q003",
    type: "workflow" as const,
    title: "LR-Q003 worked question",
    rights: {
      ...template.rights,
      describedResourceLicence: "rights-only-sentinel",
    },
    details: {
      questionId: "LR-Q003",
      query: "online copy or official copy proof of ownership",
      expectedPropositions: [
        "An online copy is not proof of ownership.",
        "Official copies have a distinct route.",
      ],
      arbitrarySummary: "unknown-detail-sentinel",
      forbiddenTargets: [{ id: "NEGATIVE-TARGET", reason: "nested-detail-sentinel" }],
    },
  };
  const provider = {
    ...template,
    id: "PV-ONS-DATA",
    type: "provider" as const,
    title: "ONS Data API",
    details: {
      datasetsServices: ["datasets", "versions", "editions", "dimensions", "observations"],
    },
  };
  const records = [...bundle.records, question, provider];

  assert.ok(
    searchRecords(records, {
      ...base,
      query: "online copy official copy proof ownership",
    }).some((record) => record.id === "LR-Q003"),
  );
  assert.deepEqual(
    searchRecords(records, { ...base, query: "dimensions observations" }).map(
      (record) => record.id,
    ),
    ["PV-ONS-DATA"],
  );
  assert.deepEqual(searchRecords(records, { ...base, query: "rights-only-sentinel" }), []);
  assert.deepEqual(searchRecords(records, { ...base, query: "unknown-detail-sentinel" }), []);
  assert.deepEqual(searchRecords(records, { ...base, query: "nested-detail-sentinel" }), []);
});

test("uses deterministic title and identifier ordering", () => {
  const bundle = parseCatalogue(cloneFixture());
  const base = defaultState(bundle);
  const source = bundle.records[1]!;
  const records = [
    { ...source, id: "source:z", title: "Same title" },
    { ...source, id: "source:a", title: "Same title" },
    ...bundle.records,
  ];
  assert.deepEqual(
    searchRecords(records, { ...base, query: "same title" }).map((record) => record.id),
    ["source:a", "source:z"],
  );
});

test("derives state-aware facets while retaining zero-count known choices", () => {
  const bundle = parseCatalogue(cloneFixture());
  const state: ExplorerState = {
    ...defaultState(bundle),
    query: "inspire",
    types: ["source"],
  };
  const facets = deriveFacetOptions(bundle.records, state);
  assert.deepEqual(facets.types, [
    { value: "dataset", count: 1 },
    { value: "source", count: 1 },
  ]);
  assert.ok(facets.access.some((item) => item.value === "public" && item.count === 0));
  assert.ok(facets.tags.some((item) => item.value === "metadata-only" && item.count === 0));
  assert.equal(facetLabel("open-with-conditions"), "Open with conditions");
  assert.equal(facetLabel("unmapped"), "unmapped");
});

test("derives one-hop evidence without self-loop edges", () => {
  const bundle = parseCatalogue(cloneFixture());
  const graph = deriveGraph(bundle.records, [DEFAULT_RECORD_ID]);
  assert.deepEqual(
    graph.nodes.map((node) => node.id),
    [DEFAULT_RECORD_ID, "source:hmlr-inspire"],
  );
  assert.deepEqual(graph.edges, [
    {
      from: DEFAULT_RECORD_ID,
      to: "source:hmlr-inspire",
      relation: "source",
      selfReference: false,
    },
  ]);
  assert.deepEqual(
    graph.adjacency.map((item) => item.sourceIds),
    [["source:hmlr-inspire"], []],
  );
});

test("graph derivation rejects duplicate and unknown record identities", () => {
  const bundle = parseCatalogue(cloneFixture());
  assert.throws(
    () => deriveGraph([...bundle.records, bundle.records[0]!]),
    /duplicate record IDs/,
  );
  assert.throws(() => deriveGraph(bundle.records, ["unknown"]), /unknown record/);
});

test("keeps observation, modification, publication and release semantics separate", () => {
  const fixture = cloneFixture();
  Object.assign(fixture.records[0]!.details, {
    releaseTaggedAt: "2026-08-12T01:43:30+01:00",
  });
  const bundle = parseCatalogue(fixture);
  const timeline = deriveTimeline(bundle.records);
  assert.equal(timeline.events.filter((event) => event.kind === "observation").length, 2);
  assert.equal(timeline.events.filter((event) => event.kind === "modification").length, 1);
  assert.equal(timeline.events.filter((event) => event.kind === "publication").length, 1);
  assert.deepEqual(
    timeline.events.filter((event) => event.kind === "release"),
    [
      {
        id: `${DEFAULT_RECORD_ID}|release|2026-08-12T01:43:30+01:00`,
        recordId: DEFAULT_RECORD_ID,
        recordTitle: "Index polygons spatial data (INSPIRE)",
        kind: "release",
        date: "2026-08-12T01:43:30+01:00",
      },
    ],
  );
  assert.deepEqual(timeline.missing, [
    { kind: "modification", recordCount: 1 },
    { kind: "publication", recordCount: 1 },
    { kind: "release", recordCount: 1 },
  ]);
});
