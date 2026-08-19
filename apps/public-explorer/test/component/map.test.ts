import { describe, expect, it } from "vitest";

import { renderMapView } from "../../src/views/map";
import { focusedRecord, navigation } from "./fixtures";

describe("coverage schematic", () => {
  it("keeps the visual decorative and provides a complete visible text description", () => {
    const rendered = renderMapView([focusedRecord], focusedRecord, navigation);

    expect(rendered.querySelector('svg[aria-hidden="true"]')).not.toBeNull();
    expect(rendered.querySelector("canvas")).toBeNull();
    expect(rendered.textContent).toContain("Illustration only — not to scale");
    expect(rendered.textContent).toContain("Geographic coverage: England and Wales.");
    expect(rendered.textContent).toContain("British National Grid, EPSG:27700");
    expect(rendered.textContent).toContain(
      "The polygons are indicative and do not establish the exact legal extent of a title.",
    );
    expect(rendered.textContent).toContain(
      "The Explorer contains metadata only and no geometry, property record or address.",
    );
  });
});
