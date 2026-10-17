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

  it.each([
    {
      name: "supplementary characters at the HTML input limit",
      query: "𐐀".repeat(100),
      expected: "𐐀".repeat(100),
    },
    {
      name: "a caller-created state beyond the supplementary-character limit",
      query: "𐐀".repeat(101),
      expected: "𐐀".repeat(100),
    },
    {
      name: "a supplementary character straddling the final UTF-16 unit",
      query: "a".repeat(199) + "𐐀",
      expected: "a".repeat(199),
    },
    {
      name: "a complete supplementary character occupying the final two units",
      query: "a".repeat(198) + "𐐀z",
      expected: "a".repeat(198) + "𐐀",
    },
  ])("round trips $name without splitting a surrogate pair", ({ query, expected }) => {
    const state = { ...createDefaultExplorerState(bundle), query };
    const canonical = canonicaliseState(state, bundle);
    const url = serialiseExplorerUrl(state, "https://example.test/gis-ai-go/", bundle);

    expect(canonical.query).toBe(expected);
    expect(canonical.query.length).toBeLessThanOrEqual(200);
    expect(url.searchParams.get("q")).toBe(expected);
    expect(parseExplorerUrl(url, bundle)).toEqual(canonical);
  });

  it.each([
    { query: "ﬃ".repeat(67), expected: "ffi".repeat(66) + "ff" },
    { query: "ﬃ".repeat(66) + "𐐀z", expected: "ffi".repeat(66) + "𐐀" },
  ])("bounds NFKC expansion before serialising a shareable query", ({ query, expected }) => {
    const input = new URL("https://example.test/gis-ai-go/");
    input.searchParams.set("q", query);
    const parsed = parseExplorerUrl(input, bundle);
    const serialised = serialiseExplorerUrl(parsed, input, bundle);

    expect(parsed.query).toBe(expected);
    expect(parsed.query.length).toBe(200);
    expect(parseExplorerUrl(serialised, bundle)).toEqual(parsed);
  });

  it.each([
    "x".repeat(201),
    "𐐀".repeat(101),
    "a".repeat(199) + "𐐀",
  ])("rejects an oversized raw URL query without truncating it", (query) => {
    const url = new URL("https://example.test/gis-ai-go/#record=missing%3Arecord");
    url.searchParams.set("q", query);

    expect(parseExplorerUrl(url, bundle)).toMatchObject({
      query: "",
      selectedRecordId: "missing:record",
    });
  });
});
