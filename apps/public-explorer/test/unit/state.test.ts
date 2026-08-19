import { describe, expect, it } from "vitest";

import { DEFAULT_RECORD_ID, parseCatalogue } from "../../src/catalogue.js";
import {
  canonicaliseState,
  createDefaultExplorerState,
  explorerStatesEqual,
  parseExplorerUrl,
  serialiseExplorerUrl,
} from "../../src/state.js";
import type { ExplorerState } from "../../src/types.js";
import { validCatalogueFixture } from "./fixtures.js";

const bundle = parseCatalogue(validCatalogueFixture());

describe("Explorer URL state", () => {
  it("defines the focused default journey", () => {
    expect(createDefaultExplorerState(bundle)).toEqual({
      view: "cards",
      query: "inspire",
      types: ["dataset"],
      authority: [],
      access: [],
      rights: [],
      freshness: [],
      tags: [],
      selectedRecordId: DEFAULT_RECORD_ID,
    });
  });

  it("parses only the controlled facets and preserves an unknown direct record", () => {
    const state = parseExplorerUrl(
      "https://example.test/gis-ai-go/?view=graph&q=inspire&type=dataset&type=unknown" +
        "&authority=source-authoritative&access=public&rights=open-with-conditions" +
        "&freshness=current&tag=hmlr&status=candidate&unknown=value#record=missing%3Arecord",
      bundle,
    );
    expect(state).toMatchObject({
      view: "graph",
      query: "inspire",
      types: ["dataset"],
      authority: ["source-authoritative"],
      access: ["public"],
      rights: ["open-with-conditions"],
      freshness: ["current"],
      tags: ["hmlr"],
      selectedRecordId: "missing:record",
    });
  });

  it("leaves a direct filtered-list URL unselected and round trips it", () => {
    const parsed = parseExplorerUrl("https://example.test/gis-ai-go/?q=hmlr&type=dataset", bundle);
    expect(parsed.selectedRecordId).toBeNull();
    const url = serialiseExplorerUrl(parsed, "https://example.test/gis-ai-go/", bundle);
    expect(url.href).toBe(
      "https://example.test/gis-ai-go/?view=cards&q=hmlr&type=dataset",
    );
    expect(explorerStatesEqual(parseExplorerUrl(url, bundle), parsed)).toBe(true);
  });

  it("serialises in a stable order with a canonical hash record", () => {
    const state: ExplorerState = {
      view: "map",
      query: "  inspire   boundary ",
      types: ["source", "dataset", "dataset"],
      authority: ["source-authoritative"],
      access: ["public"],
      rights: ["open-with-conditions"],
      freshness: ["current"],
      tags: ["inspire", "hmlr"],
      selectedRecordId: DEFAULT_RECORD_ID,
    };
    const url = serialiseExplorerUrl(state, "https://example.test/gis-ai-go/?ignored=yes#old", bundle);
    expect(url.href).toBe(
      "https://example.test/gis-ai-go/?view=map&q=inspire+boundary&type=dataset&type=source" +
        "&authority=source-authoritative&access=public&rights=open-with-conditions" +
        "&freshness=current&tag=hmlr&tag=inspire#record=hmlr%3Adataset%3Ainspire-index-polygons",
    );
    expect(explorerStatesEqual(parseExplorerUrl(url, bundle), canonicaliseState(state, bundle))).toBe(
      true,
    );
  });

  it("fails closed on oversized, duplicate and bidi-controlled values", () => {
    const oversized = "x".repeat(201);
    expect(
      parseExplorerUrl(`https://example.test/gis-ai-go/?q=${oversized}&q=second#record=a`, bundle),
    ).toMatchObject({ query: "", selectedRecordId: "a" });
    expect(
      parseExplorerUrl("https://example.test/gis-ai-go/?q=safe%20%E2%80%AEevil#record=a", bundle)
        .query,
    ).toBe("");
    expect(
      parseExplorerUrl(
        "https://example.test/gis-ai-go/?q=safe#record=a&record=b",
        bundle,
    ).selectedRecordId,
    ).toBeNull();
  });

  it("normalises compatibility characters and bounds committed search terms", () => {
    const canonical = canonicaliseState(
      {
        ...createDefaultExplorerState(bundle),
        query: "ＩＮＳＰＩＲＥ one two three four five six seven eight nine ten eleven",
      },
      bundle,
    );
    expect(canonical.query).toBe("INSPIRE one two three four five six seven eight nine");
  });
});
