import { describe, expect, it } from "vitest";

import { renderGraphView } from "../../src/views/graph";
import type { GraphModel } from "../../src/types";
import { focusedRecord, navigation, sources } from "./fixtures";

const model: GraphModel = {
  nodes: [
    {
      id: focusedRecord.id,
      type: "dataset",
      title: focusedRecord.title,
      status: focusedRecord.status,
      explicitlyIncluded: true,
    },
    ...sources.map((source) => ({
      id: source.id,
      type: source.type,
      title: source.title,
      status: source.status,
      explicitlyIncluded: false,
    })),
  ],
  edges: [
    ...sources.map((source) => ({
      from: focusedRecord.id,
      to: source.id,
      relation: "source" as const,
      selfReference: false,
    })),
    {
      from: sources[0]!.id,
      to: sources[0]!.id,
      relation: "source",
      selfReference: true,
    },
  ],
  adjacency: [],
};

describe("evidence graph", () => {
  it("renders a decorative visual and a complete semantic adjacency list", () => {
    const rendered = renderGraphView(model, [focusedRecord, ...sources], navigation);

    expect(rendered.querySelector('svg[aria-hidden="true"]')).not.toBeNull();
    expect(rendered.querySelectorAll(".graph-edge")).toHaveLength(3);
    expect(rendered.querySelectorAll(".adjacency-list > li")).toHaveLength(4);
    expect(rendered.textContent).toContain("3 supporting source records");
    expect(rendered.textContent).toContain("Cites");
    expect(rendered.textContent).toContain("Cited by");
  });

  it("omits source identity self-references from both representations", () => {
    const rendered = renderGraphView(model, [focusedRecord, ...sources], navigation);
    const sourceItem = [...rendered.querySelectorAll(".adjacency-list > li")].find(
      (item) => item.querySelector("h4")?.textContent === sources[0]!.title,
    );

    expect(sourceItem?.textContent).toContain("CitesNone");
  });
});
