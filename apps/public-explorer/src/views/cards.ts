import {
  appendChildren,
  bulletList,
  button,
  definitionList,
  element,
  formatDate,
  humaniseToken,
  link,
  recordHeadingId,
  time,
} from "../dom";
import { safeNavigableHref } from "../links";
import type { CatalogueRecord, JsonValue } from "../types";

export interface CardNavigation {
  readonly hrefForRecord: (recordId: string | null) => string;
  readonly selectRecord: (recordId: string | null) => void;
}

function stringDetail(record: CatalogueRecord, name: string): string | null {
  const value = record.details[name];
  return typeof value === "string" && value.length > 0 ? value : null;
}

function stringArrayDetail(record: CatalogueRecord, name: string): readonly string[] {
  const value = record.details[name];
  if (!Array.isArray(value)) {
    return [];
  }
  return value.filter((item): item is string => typeof item === "string");
}

function firstLimitation(record: CatalogueRecord): string {
  const legalWarning = record.limitations.find((limitation) =>
    /indicative|legal|definitive|ownership|boundary/iu.test(limitation),
  );
  return legalWarning ?? record.limitations[0] ?? "Consult the source before reuse.";
}

function navigationLink(
  label: string,
  recordId: string | null,
  navigation: CardNavigation,
  className?: string,
): HTMLAnchorElement {
  const node = link(label, navigation.hrefForRecord(recordId), className);
  node.addEventListener("click", (event) => {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    ) {
      return;
    }
    event.preventDefault();
    navigation.selectRecord(recordId);
  });
  return node;
}

function renderTags(record: CatalogueRecord): HTMLUListElement {
  const list = element("ul", { className: "tag-list", id: `tags-${encodeURIComponent(record.id)}` });
  for (const tag of record.tags) {
    list.append(element("li", { className: "topic-tag", text: tag }));
  }
  return list;
}

export function renderRecordCard(
  record: CatalogueRecord,
  navigation: CardNavigation,
): HTMLLIElement {
  const item = element("li");
  const article = element("article", { className: "record-card" });
  const heading = element("h3");
  heading.append(navigationLink(record.title, record.id, navigation));
  const warningId = `warning-${encodeURIComponent(record.id)}`;
  article.setAttribute("aria-describedby", warningId);
  article.append(
    heading,
    element("p", { text: record.description }),
    element("div", { className: "metadata-summary" }, [
      element("span", { className: "status-tag", text: humaniseToken(record.type) }),
      element("span", {
        className: "status-tag",
        text: humaniseToken(record.authority.class),
      }),
      element("span", {
        className: "status-tag",
        text: humaniseToken(record.rights.state),
      }),
    ]),
    element("p", {
      className: "warning-panel",
      id: warningId,
      text: `Important limitation: ${firstLimitation(record)}`,
    }),
    element("p", {}, [
      "Observed ",
      time(record.freshness.observedAt),
      ". Review by ",
      time(record.freshness.staleAfter),
      ".",
    ]),
    renderTags(record),
  );
  item.append(article);
  return item;
}

function publisherName(record: CatalogueRecord): string {
  return stringDetail(record, "publisher") ??
    stringDetail(record, "organisation") ??
    "GIS AI GO catalogue";
}

function citationText(record: CatalogueRecord): string {
  return `${publisherName(record)}, “${record.title}” (${record.id}), metadata observed ${formatDate(
    record.freshness.observedAt,
  )}; GIS AI GO metadata projection reviewed ${formatDate(record.freshness.reviewedAt)}.`;
}

function renderCitation(record: CatalogueRecord): HTMLElement {
  const section = element("section", { className: "citation-box" });
  const headingId = `citation-${encodeURIComponent(record.id)}`;
  const citationId = `citation-text-${encodeURIComponent(record.id)}`;
  section.setAttribute("aria-labelledby", headingId);
  const copyButton = button("Copy citation", "secondary-button");
  const status = element("p", { className: "copy-status" });
  status.setAttribute("role", "status");
  status.setAttribute("aria-live", "polite");
  const citation = citationText(record);
  copyButton.addEventListener("click", () => {
    void navigator.clipboard
      ?.writeText(citation)
      .then(() => {
        status.textContent = "Citation copied.";
      })
      .catch(() => {
        status.textContent = "Copy unavailable. Select and copy the citation text.";
      });
    if (navigator.clipboard === undefined) {
      status.textContent = "Copy unavailable. Select and copy the citation text.";
    }
  });
  section.append(
    element("h3", { id: headingId, text: "Cite this catalogue record" }),
    element("p", { id: citationId, text: citation }),
    copyButton,
    status,
  );
  copyButton.setAttribute("aria-describedby", citationId);
  return section;
}

function externalSourceLink(record: CatalogueRecord): HTMLAnchorElement | null {
  const candidates = [stringDetail(record, "url"), record.authority.source];
  for (const candidate of candidates) {
    if (candidate === null || !/^https:/iu.test(candidate)) {
      continue;
    }
    const safe = safeNavigableHref(candidate, document.baseURI);
    if (safe !== null) {
      return link(`Official source: ${new URL(candidate).hostname}`, safe);
    }
  }
  return null;
}

function detailRows(record: CatalogueRecord): ReturnType<typeof definitionList> {
  const formats = stringArrayDetail(record, "formats");
  const rows = [
    { term: "Source-native ID", description: record.id },
    { term: "Record type", description: humaniseToken(record.type) },
    { term: "Publisher", description: publisherName(record) },
    { term: "Authority", description: `${humaniseToken(record.authority.class)} — ${record.authority.statement}` },
    { term: "Publication classification", description: "Public metadata" },
    { term: "Contains personal data", description: "No" },
    { term: "Contains protected data", description: "No" },
    { term: "Access", description: `${humaniseToken(record.access.state)}; ${record.access.authentication}` },
    { term: "Rights state", description: humaniseToken(record.rights.state) },
    { term: "Record licence", description: record.rights.recordLicence },
    { term: "Described resource licence", description: record.rights.describedResourceLicence },
    { term: "Attribution", description: record.rights.attribution },
    { term: "Observed", description: time(record.freshness.observedAt) },
    { term: "Reviewed", description: time(record.freshness.reviewedAt) },
    { term: "Review by", description: time(record.freshness.staleAfter) },
  ];

  const jurisdiction = stringDetail(record, "jurisdiction");
  const cadence = stringDetail(record, "cadence");
  const accessModel = stringDetail(record, "accessModel");
  if (jurisdiction !== null) {
    rows.push({ term: "Geographic coverage", description: jurisdiction });
  }
  if (cadence !== null) {
    rows.push({ term: "Update cadence", description: cadence });
  }
  if (accessModel !== null) {
    rows.push({ term: "Source access model", description: accessModel });
  }
  if (formats.length > 0) {
    rows.push({ term: "Formats", description: formats.join(", ") });
  }
  return definitionList(rows);
}

function renderSourceReferences(
  record: CatalogueRecord,
  recordsById: ReadonlyMap<string, CatalogueRecord>,
  navigation: CardNavigation,
): HTMLElement {
  const section = element("section");
  section.append(element("h3", { text: "Source evidence" }));
  const list = element("ul");
  for (const sourceId of record.sourceRefs) {
    const source = recordsById.get(sourceId);
    const item = element("li");
    if (source === undefined || sourceId === record.id) {
      item.textContent = source?.title ?? sourceId;
    } else {
      item.append(navigationLink(source.title, source.id, navigation));
    }
    list.append(item);
  }
  section.append(list);
  const official = externalSourceLink(record);
  if (official !== null) {
    section.append(element("p", {}, [official]));
  }
  return section;
}

export function renderRecordDetail(
  record: CatalogueRecord,
  allRecords: readonly CatalogueRecord[],
  navigation: CardNavigation,
): HTMLElement {
  const article = element("article", { className: "record-detail" });
  const headingId = recordHeadingId(record.id);
  article.setAttribute("aria-labelledby", headingId);
  article.append(
    navigationLink("Back to catalogue", null, navigation, "back-link"),
    element("h2", { id: headingId, text: record.title }),
    element("p", { className: "lede", text: record.description }),
    element("div", { className: "warning-panel" }, [
      element("h3", { text: "Important limitations" }),
      bulletList(record.limitations),
    ]),
    detailRows(record),
    renderSourceReferences(
      record,
      new Map(allRecords.map((candidate) => [candidate.id, candidate])),
      navigation,
    ),
    element("section", {}, [
      element("h3", { text: "Topics" }),
      renderTags(record),
    ]),
    renderCitation(record),
  );
  return article;
}

export function renderCardsView(
  records: readonly CatalogueRecord[],
  allRecords: readonly CatalogueRecord[],
  selectedRecord: CatalogueRecord | null,
  navigation: CardNavigation,
): HTMLElement {
  const section = element("section");
  section.setAttribute("aria-labelledby", "view-heading-cards");
  section.append(element("h2", { id: "view-heading-cards", text: "Catalogue" }));

  if (selectedRecord !== null) {
    section.append(renderRecordDetail(selectedRecord, allRecords, navigation));
    return section;
  }

  if (records.length === 0) {
    section.append(
      element("div", { className: "empty-state" }, [
        element("h3", { text: "No catalogue records found" }),
        element("p", { text: "Change or clear the search and filters to see more records." }),
      ]),
    );
    return section;
  }

  const list = element("ol", { className: "result-list" });
  for (const record of records) {
    list.append(renderRecordCard(record, navigation));
  }
  section.append(list);
  return section;
}
