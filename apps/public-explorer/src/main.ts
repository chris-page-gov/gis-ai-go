import "./styles.css";

import {
  DEFAULT_BOUNDARY_CAVEAT,
  DEFAULT_RECORD_ID,
  deriveFacetOptions,
  deriveGraph,
  deriveTimeline,
  facetLabel,
  parseCatalogueJson,
  searchRecords,
} from "./catalogue";
import {
  button,
  definitionList,
  element,
  humaniseToken,
  link,
  recordHeadingId,
  setCurrentPage,
} from "./dom";
import { safeNavigableHref } from "./links";
import {
  canonicaliseState,
  createDefaultExplorerState,
  parseExplorerUrl,
  serialiseExplorerUrl,
} from "./state";
import type {
  CatalogueBundle,
  CatalogueRecord,
  ExplorerState,
  FacetOption,
  FacetOptions,
} from "./types";
import { renderCardsView, type CardNavigation } from "./views/cards";
import { renderGraphView } from "./views/graph";
import { renderMapView } from "./views/map";
import { renderTimelineView } from "./views/timeline";

document.documentElement.classList.remove("no-js");

function requireExplorerRoot(): HTMLElement {
  const candidate = document.querySelector<HTMLElement>("#explorer-root");
  if (candidate === null) {
    throw new Error("Explorer root is missing");
  }
  return candidate;
}

const root = requireExplorerRoot();

type FacetStateKey = "types" | "authority" | "access" | "rights" | "freshness" | "tags";

interface HistorySnapshot {
  readonly focusId?: string;
  readonly scrollY?: number;
}

let bundle: CatalogueBundle;
let state: ExplorerState;
let stateWarning = false;
let malformedRecordIntent = false;
let lastHandledLocation = "";

function isUnmodifiedPrimaryClick(event: MouseEvent): boolean {
  return (
    !event.defaultPrevented &&
    event.button === 0 &&
    !event.metaKey &&
    !event.ctrlKey &&
    !event.shiftKey &&
    !event.altKey
  );
}

function isBareEntry(url: URL): boolean {
  return url.search.length === 0 && (url.hash.length === 0 || url.hash === "#");
}

function hasRecordHash(url: URL): boolean {
  if (url.hash.length < 2) {
    return false;
  }
  try {
    return new URLSearchParams(url.hash.slice(1)).has("record");
  } catch {
    return true;
  }
}

function stateUrl(nextState: ExplorerState): URL {
  return serialiseExplorerUrl(nextState, new URL(window.location.href), bundle);
}

function updateCurrentHistoryScroll(): void {
  const current = (history.state ?? {}) as HistorySnapshot;
  history.replaceState(
    { ...current, scrollY: window.scrollY },
    "",
    window.location.href,
  );
}

function focusAfterRender(focusId: string | undefined, scrollY?: number): void {
  if (focusId === undefined && scrollY === undefined) {
    return;
  }
  requestAnimationFrame(() => {
    if (focusId !== undefined) {
      document.getElementById(focusId)?.focus({ preventScroll: scrollY !== undefined });
    }
    if (scrollY !== undefined) {
      window.scrollTo({ left: 0, top: scrollY });
    }
  });
}

function commitState(
  candidate: ExplorerState,
  focusId?: string,
  mode: "push" | "replace" = "push",
): void {
  const nextState = canonicaliseState(candidate, bundle);
  if (mode === "push") {
    updateCurrentHistoryScroll();
  }
  const snapshot: HistorySnapshot = focusId === undefined ? {} : { focusId };
  history[mode === "push" ? "pushState" : "replaceState"](
    snapshot,
    "",
    stateUrl(nextState),
  );
  state = nextState;
  stateWarning = false;
  malformedRecordIntent = false;
  render(focusId);
  lastHandledLocation = window.location.href;
}

function internalLink(
  label: string,
  candidate: ExplorerState,
  focusId: string,
  className?: string,
): HTMLAnchorElement {
  const href = stateUrl(canonicaliseState(candidate, bundle)).href;
  const node = link(label, href, className);
  node.addEventListener("click", (event) => {
    if (!isUnmodifiedPrimaryClick(event)) {
      return;
    }
    event.preventDefault();
    commitState(candidate, focusId);
  });
  return node;
}

function navigation(): CardNavigation {
  return {
    hrefForRecord(recordId: string | null): string {
      return stateUrl(
        canonicaliseState(
          { ...state, view: "cards", selectedRecordId: recordId },
          bundle,
        ),
      ).href;
    },
    selectRecord(recordId: string | null): void {
      commitState(
        { ...state, view: "cards", selectedRecordId: recordId },
        recordId === null ? "view-heading-cards" : recordHeadingId(recordId),
      );
    },
  };
}

function renderQuestion(): HTMLElement {
  const section = element("section");
  section.setAttribute("aria-labelledby", "question-heading");
  section.append(
    element("h1", {
      id: "question-heading",
      text: "INSPIRE polygon: indicative or legal boundary?",
    }),
    element("div", { className: "answer-panel" }, [
      element("p", {}, [
        element("strong", { text: "Indicative." }),
        " The dataset describes polygons showing the indicative position and extent of registered freehold property. ",
        element("span", { text: DEFAULT_BOUNDARY_CAVEAT }),
      ]),
      element("p", {
        text: "This Explorer contains metadata only. It contains no property record, address or geometry and must not be used to decide ownership, title extent or a boundary dispute.",
      }),
    ]),
    element("p", {
      text: "Coverage is England and Wales and the described data is a freehold subset. A title may have several polygons, and absence of an INSPIRE ID does not prove that land is unregistered.",
    }),
    element("p", {
      text: "HM Land Registry remains authoritative for its source metadata. GIS AI GO is authoritative only for this normalised catalogue projection; it is not endorsed by the publisher and is not legal advice.",
    }),
    element("p", {}, [
      internalLink(
        "View the governed INSPIRE catalogue record",
        { ...state, view: "cards", selectedRecordId: DEFAULT_RECORD_ID },
        recordHeadingId(DEFAULT_RECORD_ID),
      ),
    ]),
  );
  return section;
}

function facetGroup(
  legend: string,
  key: FacetStateKey,
  options: readonly FacetOption[],
): HTMLFieldSetElement {
  const fieldset = element("fieldset", { className: "facet-group" });
  fieldset.append(element("legend", { text: legend }));
  const selected = new Set(state[key] as readonly string[]);
  for (const option of options) {
    const encoded = encodeURIComponent(option.value);
    const id = `facet-${key}-${encoded}`;
    const wrapper = element("div", { className: "checkbox-item" });
    const checkbox = element("input");
    checkbox.type = "checkbox";
    checkbox.id = id;
    checkbox.name = key;
    checkbox.value = option.value;
    checkbox.checked = selected.has(option.value);
    const labelNode = element("label", {
      text: `${key === "tags" ? option.value : facetLabel(option.value)} (${option.count})`,
    });
    labelNode.htmlFor = id;
    checkbox.addEventListener("change", () => {
      const values = new Set(state[key] as readonly string[]);
      if (checkbox.checked) {
        values.add(option.value);
      } else {
        values.delete(option.value);
      }
      const next = {
        ...state,
        query:
          document.querySelector<HTMLInputElement>("#catalogue-search")?.value ??
          state.query,
        [key]: [...values].sort(),
        selectedRecordId: null,
      } as ExplorerState;
      commitState(next, id);
    });
    wrapper.append(checkbox, labelNode);
    fieldset.append(wrapper);
  }
  return fieldset;
}

function renderSearch(facets: FacetOptions): HTMLElement {
  const section = element("section", { className: "search-panel" });
  section.setAttribute("aria-labelledby", "search-heading");
  section.append(element("h2", { id: "search-heading", text: "Search and filter" }));
  const form = element("form");
  form.setAttribute("role", "search");
  form.setAttribute("aria-label", "Catalogue search");
  const group = element("div", { className: "form-group" });
  const input = element("input");
  input.type = "search";
  input.id = "catalogue-search";
  input.name = "q";
  input.value = state.query;
  input.maxLength = 200;
  input.autocomplete = "off";
  input.setAttribute("aria-describedby", "catalogue-search-hint");
  const labelNode = element("label", { className: "form-label", text: "Search catalogue" });
  labelNode.htmlFor = input.id;
  const hint = element("span", {
    className: "hint",
    id: "catalogue-search-hint",
    text: "Search public catalogue metadata. Do not enter personal information or a property address. Your search is included in the URL.",
  });
  const submit = button("Search");
  submit.id = "catalogue-search-submit";
  submit.type = "submit";
  group.append(labelNode, hint, element("div", { className: "search-row" }, [input, submit]));
  form.append(group);
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    commitState(
      { ...state, query: input.value, selectedRecordId: null },
      submit.id,
    );
  });

  const facetGrid = element("div", { className: "facet-grid" });
  facetGrid.append(
    facetGroup("Type", "types", facets.types),
    facetGroup("Authority", "authority", facets.authority),
    facetGroup("Access", "access", facets.access),
    facetGroup("Rights", "rights", facets.rights),
    facetGroup("Freshness", "freshness", facets.freshness),
    facetGroup("Topic", "tags", facets.tags),
  );
  const clear = button("Clear search and filters", "secondary-button");
  clear.id = "clear-search-filters";
  clear.addEventListener("click", () => {
    commitState(
      {
        ...state,
        query: "",
        types: [],
        authority: [],
        access: [],
        rights: [],
        freshness: [],
        tags: [],
        selectedRecordId: null,
      },
      clear.id,
    );
  });
  section.append(form, facetGrid, clear);
  return section;
}

function renderViewNavigation(): HTMLElement {
  const nav = element("nav", { className: "view-navigation" });
  nav.setAttribute("aria-label", "Explore catalogue");
  const list = element("ul");
  const views = [
    ["Catalogue", "cards"],
    ["Graph", "graph"],
    ["Timeline", "timeline"],
    ["Map", "map"],
  ] as const;
  for (const [label, view] of views) {
    const item = element("li");
    const node = internalLink(label, { ...state, view }, `view-heading-${view}`);
    setCurrentPage(node, state.view === view);
    item.append(node);
    list.append(item);
  }
  const aboutItem = element("li");
  const about = link("About", "#about");
  about.addEventListener("click", (event) => {
    if (!isUnmodifiedPrimaryClick(event)) {
      return;
    }
    event.preventDefault();
    updateCurrentHistoryScroll();
    const next = canonicaliseState({ ...state, selectedRecordId: null }, bundle);
    const url = stateUrl(next);
    url.hash = "about";
    history.pushState({ focusId: "about-heading" } satisfies HistorySnapshot, "", url);
    state = next;
    stateWarning = false;
    malformedRecordIntent = false;
    render("about-heading");
    lastHandledLocation = window.location.href;
  });
  aboutItem.append(about);
  list.append(aboutItem);
  nav.append(list);
  return nav;
}

function staticDownload(label: string, relative: string): HTMLAnchorElement {
  const safe = safeNavigableHref(relative, document.baseURI);
  if (safe === null) {
    throw new Error(`Unsafe static download path: ${relative}`);
  }
  return link(label, safe);
}

function renderAbout(): HTMLElement {
  const section = element("section", { className: "about-section", id: "about" });
  section.setAttribute("aria-labelledby", "about-heading");
  section.tabIndex = -1;
  section.append(
    element("h2", { id: "about-heading", text: "About this Explorer" }),
    element("p", {
      text: "This static candidate lets people inspect and cite public catalogue metadata without an account, MCP host or WebMCP implementation. It makes no provider request and contains no protected data.",
    }),
    element("h3", { text: "What catalogue terms mean" }),
    definitionList([
      {
        term: "Indicative",
        description: "A general representation, not evidence of an exact legal title extent.",
      },
      {
        term: "Authority",
        description: "Who is responsible for the source statement and what GIS AI GO has normalised.",
      },
      {
        term: "Freshness",
        description: "When metadata was observed, reviewed and due for another review.",
      },
      {
        term: "Rights",
        description: "The licence for the catalogue record is kept separate from the licence and conditions for the described resource.",
      },
      {
        term: "GML",
        description: "Geography Markup Language, a structured format for geographic information.",
      },
      {
        term: "EPSG:27700",
        description: "The identifier for the British National Grid coordinate reference system used by the source GML.",
      },
    ]),
    definitionList([
      { term: "Catalogue version", description: bundle.version },
      { term: "OKF version", description: bundle.okfVersion },
      { term: "Revision", description: bundle.revision },
      { term: "Records", description: String(bundle.recordCount) },
      { term: "Publication state", description: "Candidate public metadata" },
      { term: "Rights", description: bundle.rights.statement },
    ]),
  );

  const downloads = element("section", { className: "downloads-section" });
  downloads.setAttribute("aria-labelledby", "downloads-heading");
  const list = element("ul", { className: "download-list" });
  list.append(
    element("li", {}, [staticDownload("Download JSON", "./catalogue/okf-bundle.json")]),
    element("li", {}, [staticDownload("Download JSON-LD", "./catalogue/okf-bundle.jsonld")]),
    element("li", {}, [staticDownload("Download checksums", "./catalogue/CHECKSUMS.sha256")]),
  );
  downloads.append(
    element("h3", { id: "downloads-heading", text: "Download catalogue" }),
    list,
  );
  section.append(downloads);
  return section;
}

function renderNotFound(navigationModel: CardNavigation): HTMLElement {
  const section = element("section", { className: "error-state" });
  section.setAttribute("aria-labelledby", "record-not-found-heading");
  const back = link("Back to catalogue", navigationModel.hrefForRecord(null));
  back.addEventListener("click", (event) => {
    if (!isUnmodifiedPrimaryClick(event)) {
      return;
    }
    event.preventDefault();
    navigationModel.selectRecord(null);
  });
  section.append(
    element("h2", { id: "record-not-found-heading", text: "Record not found" }),
    element("p", {
      text: "The catalogue does not contain the record named by this link. No substitute record has been selected.",
    }),
    element("p", {}, [back]),
  );
  return section;
}

function renderActiveView(
  matches: readonly CatalogueRecord[],
  selectedRecord: CatalogueRecord | null,
): HTMLElement {
  const navigationModel = navigation();
  if (
    malformedRecordIntent ||
    (state.selectedRecordId !== null && selectedRecord === null)
  ) {
    return renderNotFound(navigationModel);
  }
  switch (state.view) {
    case "cards":
      return renderCardsView(matches, bundle.records, selectedRecord, navigationModel);
    case "graph":
      return renderGraphView(
        deriveGraph(bundle.records, matches.map((record) => record.id)),
        bundle.records,
        navigationModel,
      );
    case "timeline":
      return renderTimelineView(deriveTimeline(matches), matches, navigationModel);
    case "map":
      return renderMapView(matches, selectedRecord, navigationModel);
  }
}

function render(focusId?: string, scrollY?: number): void {
  const previousFocusId = document.activeElement instanceof HTMLElement
    ? document.activeElement.id
    : "";
  const matches = searchRecords(bundle.records, state);
  const selectedRecord =
    state.selectedRecordId === null
      ? null
      : (bundle.records.find((record) => record.id === state.selectedRecordId) ?? null);
  const fragment = document.createDocumentFragment();
  fragment.append(
    renderQuestion(),
    renderSearch(deriveFacetOptions(bundle.records, state)),
    renderViewNavigation(),
  );

  if (stateWarning) {
    const warning = element("p", {
      className: "warning-panel",
      text: "Some settings in this link were not recognised and were ignored.",
    });
    warning.setAttribute("role", "status");
    fragment.append(warning);
  }

  const summary = element("p", {
    className: "result-summary",
    id: "catalogue-result-summary",
    text: `${matches.length} catalogue ${matches.length === 1 ? "record" : "records"} found`,
  });
  summary.setAttribute("role", "status");
  summary.setAttribute("aria-live", "polite");
  summary.setAttribute("aria-atomic", "true");
  fragment.append(summary, renderActiveView(matches, selectedRecord), renderAbout());
  root.replaceChildren(fragment);
  root.setAttribute("aria-busy", "false");

  if (
    malformedRecordIntent ||
    (state.selectedRecordId !== null && selectedRecord === null)
  ) {
    document.title = "Record not found – GIS AI GO";
  } else if (selectedRecord !== null && state.view === "cards") {
    document.title = `${selectedRecord.title} – GIS AI GO`;
  } else {
    const viewTitle =
      state.view === "cards" ? "Catalogue" : humaniseToken(state.view);
    document.title = `${viewTitle} – GIS AI GO`;
  }
  focusAfterRender(focusId ?? (previousFocusId || undefined), scrollY);
}

function comparableStateUrl(url: URL): string {
  if (url.hash === "#about") {
    return `${url.pathname}${url.search}`;
  }
  return `${url.pathname}${url.search}${url.hash}`;
}

function readLocation(initial = false): void {
  const raw = new URL(window.location.href);
  if (initial && isBareEntry(raw)) {
    state = createDefaultExplorerState(bundle);
    history.replaceState({}, "", stateUrl(state));
    stateWarning = false;
    malformedRecordIntent = false;
    return;
  }

  state = parseExplorerUrl(raw, bundle);
  malformedRecordIntent = hasRecordHash(raw) && state.selectedRecordId === null;
  const canonical = stateUrl(state);
  stateWarning = comparableStateUrl(raw) !== comparableStateUrl(canonical);
  if (stateWarning && malformedRecordIntent) {
    canonical.hash = new URLSearchParams({ record: "not-found" }).toString();
    history.replaceState(history.state, "", canonical);
  } else if (stateWarning && raw.hash !== "#about") {
    history.replaceState(history.state, "", canonical);
  }
}

function renderLoadFailure(error: unknown): void {
  const detail = error instanceof Error ? error.message : "The catalogue could not be read.";
  root.replaceChildren(
    element("section", { className: "error-state" }, [
      element("h1", { text: "Catalogue unavailable" }),
      element("p", {
        text: "The Explorer stopped because its governed catalogue did not pass validation. It has not selected substitute data or contacted a provider.",
      }),
      element("p", { text: detail }),
      element("p", {}, [staticDownload("Download JSON", "./catalogue/okf-bundle.json")]),
    ]),
  );
  root.setAttribute("aria-busy", "false");
  document.title = "Catalogue unavailable – GIS AI GO";
}

async function start(): Promise<void> {
  try {
    const response = await fetch("./catalogue/okf-bundle.json", {
      credentials: "same-origin",
      headers: { Accept: "application/json" },
      redirect: "error",
    });
    if (!response.ok) {
      throw new Error(`Catalogue request failed with status ${response.status}.`);
    }
    bundle = parseCatalogueJson(await response.text());
    readLocation(true);
    render();
    lastHandledLocation = window.location.href;
  } catch (error) {
    renderLoadFailure(error);
  }
}

function handleLocationChange(snapshot: HistorySnapshot = {}): void {
  if (bundle === undefined) {
    return;
  }
  if (window.location.href === lastHandledLocation) {
    return;
  }
  readLocation();
  lastHandledLocation = window.location.href;
  const focusId =
    snapshot.focusId ??
    (state.selectedRecordId === null
      ? `view-heading-${state.view}`
      : recordHeadingId(state.selectedRecordId));
  render(focusId, snapshot.scrollY);
}

window.addEventListener("popstate", (event) => {
  handleLocationChange((event.state ?? {}) as HistorySnapshot);
});

window.addEventListener("hashchange", () => {
  handleLocationChange();
});

void start();
