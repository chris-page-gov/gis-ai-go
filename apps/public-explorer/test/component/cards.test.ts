import { describe, expect, it } from "vitest";

import { renderCardsView, renderRecordCard } from "../../src/views/cards";
import { focusedRecord, navigation, sources } from "./fixtures";

describe("catalogue cards", () => {
  it("renders untrusted catalogue text without creating markup", () => {
    const malicious = {
      ...focusedRecord,
      title: '<img src="https://attacker.invalid/track" onerror="alert(1)">',
      description: "<script>globalThis.compromised = true</script>",
    };

    const rendered = renderRecordCard(malicious, navigation);

    expect(rendered.querySelector("img")).toBeNull();
    expect(rendered.querySelector("script")).toBeNull();
    expect(rendered.textContent).toContain("<img");
    expect(rendered.textContent).toContain("<script>");
  });

  it("puts the exact legal limitation and rights distinctions in the selected record", () => {
    const rendered = renderCardsView(
      [focusedRecord],
      [focusedRecord, ...sources],
      focusedRecord,
      navigation,
    );

    expect(
      [...rendered.querySelectorAll("h2[id]")].find(
        (heading) => heading.id === `record-heading-${encodeURIComponent(focusedRecord.id)}`,
      )?.textContent,
    ).toBe(focusedRecord.title);
    expect(rendered.textContent).toContain(
      "Polygons are indicative and do not establish the exact legal extent of a title.",
    );
    expect(rendered.textContent).toContain("Record licence");
    expect(rendered.textContent).toContain("Described resource licence");
    expect(rendered.textContent).toContain("Contains protected data");
    expect(rendered.textContent).toContain("No");
    expect(
      [...rendered.querySelectorAll("a")].some(
        (anchor) => anchor.textContent === "Back to catalogue",
      ),
    ).toBe(true);
  });

  it("links each explicit source reference without inventing a provider", () => {
    const rendered = renderCardsView(
      [focusedRecord],
      [focusedRecord, ...sources],
      focusedRecord,
      navigation,
    );
    const labels = [...rendered.querySelectorAll("a")].map((anchor) => anchor.textContent);

    expect(labels).toContain("Official dataset page");
    expect(labels).toContain("Official download page");
    expect(labels).toContain("Official technical guidance");
    expect(labels).not.toContain("HM Land Registry open publications");
  });
});
