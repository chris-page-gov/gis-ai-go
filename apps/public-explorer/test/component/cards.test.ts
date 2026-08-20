import { describe, expect, it } from "vitest";

import { renderCardsView, renderRecordCard } from "../../src/views/cards";
import {
  focusedRecord,
  landisProviderRecord,
  navigation,
  onsProviderRecord,
  sources,
  workedQuestionRecord,
} from "./fixtures";

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
    expect(
      [...rendered.querySelectorAll("a")].some(
        (anchor) =>
          anchor.textContent === "Open publisher evidence for Official dataset page" &&
          anchor.href.includes("source%3Adataset"),
      ),
    ).toBe(true);
  });

  it("shows reviewed worked-question findings as governed, non-executing detail", () => {
    const rendered = renderCardsView(
      [workedQuestionRecord],
      [workedQuestionRecord, ...sources],
      workedQuestionRecord,
      navigation,
    );

    expect(rendered.textContent).toContain("Worked question");
    expect(rendered.textContent).toContain("LR-Q003");
    expect(rendered.textContent).toContain("online copy or official copy proof of ownership");
    expect(rendered.textContent).toContain("An online copy is not proof of ownership.");
    expect(rendered.textContent).toContain("Planned Non Executing");
  });

  it("shows bounded ONS capabilities and mixed, per-record LandIS conditions", () => {
    const ons = renderCardsView(
      [onsProviderRecord],
      [onsProviderRecord, ...sources],
      onsProviderRecord,
      navigation,
    );
    expect(ons.textContent).toContain("datasets");
    expect(ons.textContent).toContain("observations");
    expect(ons.textContent).toContain("REST API");
    expect(ons.textContent).toContain("No provider connection is made");

    const landis = renderCardsView(
      [landisProviderRecord],
      [landisProviderRecord, ...sources],
      landisProviderRecord,
      navigation,
    );
    expect(landis.textContent).toContain("Commercial or restricted where record terms require");
    expect(landis.textContent).toContain("Read and enforce each record licence");
    expect(landis.textContent).toContain("No live provider call");
    expect(landis.textContent).toContain("do not execute here");
  });
});
