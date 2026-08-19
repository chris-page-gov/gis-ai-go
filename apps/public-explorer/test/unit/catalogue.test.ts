import { describe, expect, it } from "vitest";

import {
  DEFAULT_BOUNDARY_CAVEAT,
  DEFAULT_RECORD_ID,
  deriveFacetOptions,
  deriveGraph,
  deriveTimeline,
  parseCatalogue,
  parseCatalogueJson,
  searchRecords,
} from "../../src/catalogue.js";
import { createDefaultExplorerState } from "../../src/state.js";
import type { ExplorerState } from "../../src/types.js";
import { validCatalogueFixture } from "./fixtures.js";

function cloneFixture() {
  return structuredClone(validCatalogueFixture());
}

describe("canonical catalogue validation", () => {
  it("accepts the bounded public fixture and preserves the legal-boundary caveat", () => {
    const bundle = parseCatalogue(cloneFixture());
    expect(bundle.recordCount).toBe(2);
    expect(bundle.records.find((record) => record.id === DEFAULT_RECORD_ID)?.limitations).toContain(
      DEFAULT_BOUNDARY_CAVEAT,
    );
    expect(parseCatalogueJson(JSON.stringify(validCatalogueFixture()))).toEqual(bundle);
  });

  it("rejects protected flags, extra fields and unresolved references", () => {
    const protectedFixture = cloneFixture();
    protectedFixture.records[0]!.publication.containsProtectedData = true;
    expect(() => parseCatalogue(protectedFixture)).toThrow(/containsProtectedData/);

    const extraFixture = cloneFixture();
    Object.assign(extraFixture.records[0]!, { unexpected: true });
    expect(() => parseCatalogue(extraFixture)).toThrow(/expected keys/);

    const unresolvedFixture = cloneFixture();
    unresolvedFixture.records[0]!.sourceRefs = ["source:missing"];
    expect(() => parseCatalogue(unresolvedFixture)).toThrow(/unresolved source reference/);
  });

  it("rejects unsafe HTML, bidi controls and unsafe navigable URLs", () => {
    const markup = cloneFixture();
    markup.records[0]!.title = '<img src=x onerror="globalThis.pwned=true">';
    expect(() => parseCatalogue(markup)).toThrow(/HTML-like/);

    const bidi = cloneFixture();
    bidi.records[0]!.description = "Trusted\u202eevil";
    expect(() => parseCatalogue(bidi)).toThrow(/unsafe control/);

    const unsafeUrl = cloneFixture();
    unsafeUrl.records[0]!.details.url = "javascript:alert(1)";
    expect(() => parseCatalogue(unsafeUrl)).toThrow(/navigable URL/);
  });

  it("rejects a missing legal caveat and dangerous object keys", () => {
    const missingCaveat = cloneFixture();
    missingCaveat.records[0]!.limitations = ["Not a complete dataset."];
    expect(() => parseCatalogue(missingCaveat)).toThrow(/indicative-versus-legal-boundary/);

    const dangerous = JSON.parse(JSON.stringify(validCatalogueFixture())) as ReturnType<
      typeof validCatalogueFixture
    >;
    Object.defineProperty(dangerous.records[0]!.details, "__proto__", {
      enumerable: true,
      value: { polluted: true },
    });
    expect(() => parseCatalogue(dangerous)).toThrow(/dangerous object key/);

    const nonJsonObject = cloneFixture();
    nonJsonObject.records[0]!.details.publisher = new Date("2026-08-19T00:00:00Z") as never;
    expect(() => parseCatalogue(nonJsonObject)).toThrow(/plain JSON object/);
  });
});

describe("search and facets", () => {
  it("searches only controlled fields with NFKC normalisation and ten terms", () => {
    const bundle = parseCatalogue(cloneFixture());
    const base = createDefaultExplorerState(bundle);
    const state: ExplorerState = {
      ...base,
      query: "HM Land Registry England GML Monthly polygons indicative extent metadata hmlr ignored",
      types: ["dataset"],
      authority: ["source-authoritative"],
      access: ["public"],
      rights: ["open-with-conditions"],
      freshness: ["current"],
      tags: ["inspire"],
    };
    expect(searchRecords(bundle.records, state).map((record) => record.id)).toEqual([
      DEFAULT_RECORD_ID,
    ]);

    const rightsOnly = { ...base, query: "upstream", types: [] as const };
    expect(searchRecords(bundle.records, rightsOnly)).toHaveLength(0);
  });

  it("derives state-aware counts while retaining zero-count known choices", () => {
    const bundle = parseCatalogue(cloneFixture());
    const state: ExplorerState = {
      ...createDefaultExplorerState(bundle),
      query: "inspire",
      types: ["source"],
    };
    const facets = deriveFacetOptions(bundle.records, state);
    expect(facets.types).toEqual([
      { value: "dataset", count: 1 },
      { value: "source", count: 1 },
    ]);
    expect(facets.access).toContainEqual({ value: "public", count: 0 });
    expect(facets.tags).toContainEqual({ value: "metadata-only", count: 0 });
  });
});

describe("derived evidence views", () => {
  it("derives one-hop evidence without self-loop edges", () => {
    const bundle = parseCatalogue(cloneFixture());
    const graph = deriveGraph(bundle.records, [DEFAULT_RECORD_ID]);
    expect(graph.nodes.map((node) => node.id)).toEqual([DEFAULT_RECORD_ID, "source:hmlr-inspire"]);
    expect(graph.edges).toEqual([
      {
        from: DEFAULT_RECORD_ID,
        to: "source:hmlr-inspire",
        relation: "source",
        selfReference: false,
      },
    ]);
    expect(graph.adjacency.map((item) => item.sourceIds)).toEqual([
      ["source:hmlr-inspire"],
      [],
    ]);
  });

  it("keeps observation, modification, publication and release semantics separate", () => {
    const bundle = parseCatalogue(cloneFixture());
    const timeline = deriveTimeline(bundle.records);
    expect(timeline.events.filter((event) => event.kind === "observation")).toHaveLength(2);
    expect(timeline.events.filter((event) => event.kind === "modification")).toHaveLength(1);
    expect(timeline.events.filter((event) => event.kind === "publication")).toHaveLength(1);
    expect(timeline.events.filter((event) => event.kind === "release")).toHaveLength(0);
    expect(timeline.missing).toEqual([
      { kind: "modification", recordCount: 1 },
      { kind: "publication", recordCount: 1 },
      { kind: "release", recordCount: 2 },
    ]);
  });
});
