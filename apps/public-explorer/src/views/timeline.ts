import { element, humaniseToken, link, time } from "../dom";
import type {
  CatalogueRecord,
  TimelineEvent,
  TimelineEventKind,
  TimelineModel,
} from "../types";

export interface TimelineNavigation {
  readonly hrefForRecord: (recordId: string | null) => string;
  readonly selectRecord: (recordId: string | null) => void;
}

const KIND_DEFINITIONS: Readonly<Record<TimelineEventKind, string>> = {
  observation: "When the source metadata was retrieved or observed.",
  modification: "When the publisher says the described resource was last changed.",
  publication: "An explicit publication date supplied by the source.",
  release: "An explicit release date supplied by the source.",
};

function recordLink(
  event: TimelineEvent,
  navigation: TimelineNavigation,
): HTMLAnchorElement {
  const node = link(event.recordTitle, navigation.hrefForRecord(event.recordId));
  node.addEventListener("click", (clickEvent) => {
    if (
      clickEvent.defaultPrevented ||
      clickEvent.button !== 0 ||
      clickEvent.metaKey ||
      clickEvent.ctrlKey ||
      clickEvent.shiftKey ||
      clickEvent.altKey
    ) {
      return;
    }
    clickEvent.preventDefault();
    navigation.selectRecord(event.recordId);
  });
  return node;
}

function renderLegend(): HTMLDListElement {
  const list = element("dl", { className: "timeline-legend" });
  for (const kind of ["observation", "modification", "publication", "release"] as const) {
    const wrapper = element("div");
    wrapper.append(
      element("dt", { text: humaniseToken(kind) }),
      element("dd", { text: KIND_DEFINITIONS[kind] }),
    );
    list.append(wrapper);
  }
  return list;
}

function renderEvent(
  event: TimelineEvent,
  navigation: TimelineNavigation,
): HTMLLIElement {
  const item = element("li");
  item.append(
    element("span", {
      className: "timeline-event-type",
      text: humaniseToken(event.kind),
    }),
    time(event.date),
    element("span", { text: " — " }),
    recordLink(event, navigation),
    element("span", { className: "visually-hidden", text: `, record ID ${event.recordId}` }),
  );
  return item;
}

export function renderTimelineView(
  model: TimelineModel,
  records: readonly CatalogueRecord[],
  navigation: TimelineNavigation,
): HTMLElement {
  const section = element("section");
  section.setAttribute("aria-labelledby", "view-heading-timeline");
  section.append(
    element("h2", { id: "view-heading-timeline", text: "Catalogue timeline" }),
    element("p", {
      text: "Dates retain their source meaning. Review dates and review-by dates are governance information and are not relabelled as publication or release dates.",
    }),
    renderLegend(),
  );

  if (records.length === 0) {
    section.append(
      element("div", { className: "empty-state" }, [
        element("h3", { text: "No timeline records found" }),
        element("p", { text: "Change or clear the search and filters to see dated records." }),
      ]),
    );
    return section;
  }

  const missingSection = element("section");
  missingSection.setAttribute("aria-labelledby", "missing-dates-heading");
  missingSection.append(element("h3", { id: "missing-dates-heading", text: "Dates not recorded" }));
  const missingList = element("ul");
  const missingSummaries = model.missing.filter((summary) => summary.recordCount > 0);
  for (const missing of missingSummaries) {
    const qualifier =
      missing.recordCount === records.length
        ? "all shown records"
        : `${missing.recordCount} of ${records.length} shown records`;
    missingList.append(
      element("li", {
        text: `${humaniseToken(missing.kind)} date is not recorded for ${qualifier}.`,
      }),
    );
  }
  if (missingSummaries.length === 0) {
    missingList.append(element("li", { text: "Every recognised date type is recorded." }));
  }
  missingSection.append(missingList);

  const eventSection = element("section");
  eventSection.setAttribute("aria-labelledby", "timeline-events-heading");
  eventSection.append(element("h3", { id: "timeline-events-heading", text: "Recorded events" }));
  if (model.events.length === 0) {
    eventSection.append(element("p", { text: "No recognised dates are recorded." }));
  } else {
    const list = element("ol", { className: "timeline-list" });
    for (const event of model.events) {
      list.append(renderEvent(event, navigation));
    }
    eventSection.append(list);
  }
  section.append(missingSection, eventSection);
  return section;
}
