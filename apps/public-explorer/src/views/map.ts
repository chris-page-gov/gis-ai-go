import { bulletList, element, link, svgElement } from "../dom";
import type { CatalogueRecord } from "../types";

const FOCUSED_RECORD_ID = "hmlr:dataset:inspire-index-polygons";

export interface MapNavigation {
  readonly hrefForRecord: (recordId: string | null) => string;
  readonly selectRecord: (recordId: string | null) => void;
}

function stringDetail(record: CatalogueRecord, name: string): string | null {
  const value = record.details[name];
  return typeof value === "string" && value.length > 0 ? value : null;
}

function recordLink(
  record: CatalogueRecord,
  navigation: MapNavigation,
): HTMLAnchorElement {
  const node = link(record.title, navigation.hrefForRecord(record.id));
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
    navigation.selectRecord(record.id);
  });
  return node;
}

function chooseRecord(
  records: readonly CatalogueRecord[],
  selectedRecord: CatalogueRecord | null,
): CatalogueRecord | null {
  if (
    selectedRecord !== null &&
    (selectedRecord.tags.includes("geospatial-data") || selectedRecord.tags.includes("inspire"))
  ) {
    return selectedRecord;
  }
  return (
    records.find((record) => record.id === FOCUSED_RECORD_ID) ??
    records.find(
      (record) =>
        record.tags.includes("geospatial-data") || record.tags.includes("inspire"),
    ) ??
    null
  );
}

function visualLabel(text: string, x: number, y: number): SVGTextElement {
  const node = svgElement("text", {
    class: "map-label",
    x: String(x),
    y: String(y),
  });
  node.textContent = text;
  return node;
}

function renderSchematic(record: CatalogueRecord): HTMLElement {
  const panel = element("div", { className: "visual-panel" });
  const figure = element("figure");
  const svg = svgElement("svg", {
    "aria-hidden": "true",
    focusable: "false",
    role: "presentation",
    viewBox: "0 0 720 430",
  });
  const isFocusedRecord = record.id === FOCUSED_RECORD_ID;
  const groupingLabel = isFocusedRecord
    ? "Local authority area files"
    : "Grouping recorded by source";
  const subsetLabel = isFocusedRecord
    ? "Registered freehold property"
    : "See complete text description";

  svg.append(
    svgElement("rect", { class: "map-area", height: "90", width: "250", x: "30", y: "40" }),
    visualLabel("Coverage", 50, 73),
    visualLabel(stringDetail(record, "jurisdiction") ?? "Coverage recorded by source", 50, 105),
    svgElement("line", { class: "map-connector", x1: "280", x2: "370", y1: "85", y2: "85" }),
    svgElement("rect", { class: "map-area", height: "90", width: "300", x: "370", y: "40" }),
    visualLabel("Source grouping", 390, 73),
    visualLabel(groupingLabel, 390, 105),
    svgElement("line", { class: "map-connector", x1: "520", x2: "520", y1: "130", y2: "210" }),
    svgElement("rect", { class: "map-area", height: "90", width: "300", x: "370", y: "210" }),
    visualLabel("Described subset", 390, 243),
    visualLabel(subsetLabel, 390, 275),
    svgElement("line", { class: "map-connector", x1: "370", x2: "280", y1: "255", y2: "255" }),
    svgElement("rect", { class: "map-symbol", height: "90", width: "250", x: "30", y: "210" }),
    visualLabel("Geometry in Explorer", 50, 243),
    visualLabel("None — metadata only", 50, 275),
    svgElement("rect", { class: "map-area", height: "65", width: "640", x: "30", y: "345" }),
    visualLabel("INDICATIVE — NOT AN EXACT LEGAL EXTENT", 150, 385),
  );

  figure.append(
    svg,
    element("figcaption", {
      text: "Illustration only — not to scale — no real location, title extent or property boundary.",
    }),
  );
  panel.append(figure);
  return panel;
}

function alternativeFacts(record: CatalogueRecord): readonly string[] {
  if (record.id === FOCUSED_RECORD_ID) {
    return [
      "Geographic coverage: England and Wales.",
      "The source groups files by local authority area.",
      "The described data is a registered freehold subset, not all registered titles or all land.",
      "One title may have several polygons, and local-authority boundary polygons may be duplicated across files.",
      "The source GML uses British National Grid, EPSG:27700; reprojection may introduce positional error.",
      "The polygons are indicative and do not establish the exact legal extent of a title.",
      "The Explorer contains metadata only and no geometry, property record or address.",
    ];
  }
  const facts = [
    `Geographic coverage: ${stringDetail(record, "jurisdiction") ?? "consult the source"}.`,
    "The Explorer contains metadata only and no geometry, property record or address.",
    ...record.limitations,
  ];
  return [...new Set(facts)];
}

export function renderMapView(
  records: readonly CatalogueRecord[],
  selectedRecord: CatalogueRecord | null,
  navigation: MapNavigation,
): HTMLElement {
  const section = element("section");
  section.setAttribute("aria-labelledby", "view-heading-map");
  section.append(
    element("h2", { id: "view-heading-map", text: "Coverage schematic — not a property map" }),
    element("p", {
      text: "This schematic summarises catalogue metadata. It uses no basemap, tiles, coordinates or real property geometry.",
    }),
  );
  const record = chooseRecord(records, selectedRecord);
  if (record === null) {
    section.append(
      element("div", { className: "empty-state" }, [
        element("h3", { text: "No geospatial metadata found" }),
        element("p", { text: "Change or clear the search and filters to see a coverage schematic." }),
      ]),
    );
    return section;
  }

  const alternative = element("section", { className: "map-alternative" });
  alternative.setAttribute("aria-labelledby", "map-alternative-heading");
  alternative.append(
    element("h3", { id: "map-alternative-heading", text: "Complete text description" }),
    element("p", {}, ["Record: ", recordLink(record, navigation), "."]),
    bulletList(alternativeFacts(record)),
  );
  section.append(
    element("div", { className: "visual-and-alternative" }, [
      renderSchematic(record),
      alternative,
    ]),
  );
  return section;
}
