import { describe, expect, it } from "vitest";

import { renderTimelineView } from "../../src/views/timeline";
import type { TimelineModel } from "../../src/types";
import { focusedRecord, navigation } from "./fixtures";

const model: TimelineModel = {
  events: [
    {
      id: `${focusedRecord.id}:observation`,
      recordId: focusedRecord.id,
      recordTitle: focusedRecord.title,
      kind: "observation",
      date: "2026-07-29T07:53:38Z",
    },
    {
      id: `${focusedRecord.id}:modification`,
      recordId: focusedRecord.id,
      recordTitle: focusedRecord.title,
      kind: "modification",
      date: "2026-07-05",
    },
  ],
  missing: [
    { kind: "publication", recordCount: 1 },
    { kind: "release", recordCount: 1 },
  ],
};

describe("catalogue timeline", () => {
  it("distinguishes source date meanings and exposes truthful empty categories", () => {
    const rendered = renderTimelineView(model, [focusedRecord], navigation);

    expect(rendered.textContent).toContain("Observation");
    expect(rendered.textContent).toContain("Modification");
    expect(rendered.textContent).toContain(
      "Publication date is not recorded for all shown records.",
    );
    expect(rendered.textContent).toContain("Release date is not recorded for all shown records.");
    expect(rendered.querySelector('time[datetime="2026-07-05"]')?.textContent).toBe(
      "5 July 2026",
    );
  });

  it("does not relabel governance dates as publication or release", () => {
    const rendered = renderTimelineView(model, [focusedRecord], navigation);
    const eventDates = [...rendered.querySelectorAll(".timeline-list time")].map((node) =>
      node.getAttribute("datetime"),
    );

    expect(eventDates).not.toContain(focusedRecord.freshness.reviewedAt);
    expect(eventDates).not.toContain(focusedRecord.freshness.staleAfter);
  });
});
