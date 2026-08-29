import "./styles.css";

import { parseCatalogueJson, type CatalogueBundle } from "@gis-ai-go/contracts";

import {
  executePageDescribe,
  executePageSearch,
  PageToolInputError,
  type CompactRecord,
  type PageDescribeResult,
  type PageSearchResult,
  type PageToolResult,
} from "./catalogue-tools";
import { definitionList, element, requiredElement } from "./dom";
import { registerWebMcpTools } from "./webmcp-adapter";

document.documentElement.classList.remove("no-js");

const catalogueStatus = requiredElement<HTMLElement>("#catalogue-status");
const webMcpStatus = requiredElement<HTMLElement>("#webmcp-status");
const form = requiredElement<HTMLFormElement>("#catalogue-search-form");
const queryInput = requiredElement<HTMLInputElement>("#catalogue-query");
const demoStatus = requiredElement<HTMLElement>("#demo-status");
const resultsRoot = requiredElement<HTMLElement>("#demo-results");
const cardsRoot = requiredElement<HTMLElement>("#result-cards");
const jsonRoot = requiredElement<HTMLElement>("#result-json");

let bundle: CatalogueBundle | undefined;

function recordCard(record: CompactRecord, allowDescribe: boolean): HTMLElement {
  const article = element("article", { className: "record-card" });
  const type = element("p", { className: "record-type", text: record.type });
  const heading = element("h4", { text: record.title });
  const description = element("p", { text: record.description });
  article.append(
    type,
    heading,
    description,
    definitionList([
      { term: "Identifier", description: record.id },
      { term: "Authority", description: record.authority_class },
      { term: "Access", description: record.access_state },
      { term: "Rights", description: record.rights_state },
      { term: "Freshness", description: record.freshness_status },
    ]),
  );
  if (allowDescribe) {
    const describe = element("button", { text: "Describe record and sources" });
    describe.type = "button";
    describe.addEventListener("click", () => {
      if (bundle === undefined) return;
      try {
        renderResult(executePageDescribe(bundle, { record_id: record.id }), "Manual describe call");
      } catch (error) {
        renderFailure(error);
      }
    });
    article.append(describe);
  }
  return article;
}

function describePanel(result: PageDescribeResult): HTMLElement {
  const fragment = element("div", { className: "describe-panel" });
  fragment.append(recordCard(result.record, false));
  const limitations = element("section", { className: "record-section" });
  limitations.append(element("h4", { text: "Limitations" }));
  const limitationList = element("ul");
  for (const limitation of result.record.limitations) {
    limitationList.append(element("li", { text: limitation }));
  }
  limitations.append(limitationList);
  fragment.append(limitations);

  const sources = element("section", { className: "record-section" });
  sources.append(element("h4", { text: "Linked foundational source records" }));
  if (result.record.source_records.length === 0) {
    sources.append(
      element("p", {
        text: "This record has no further catalogue source record to expand.",
      }),
    );
  } else {
    for (const source of result.record.source_records) {
      sources.append(recordCard(source, true));
    }
  }
  fragment.append(sources);
  return fragment;
}

function renderResult(result: PageToolResult, origin: string): void {
  cardsRoot.replaceChildren();
  if (result.page_tool === "explorer_search_catalogue") {
    for (const record of result.matches.records) cardsRoot.append(recordCard(record, true));
    if (result.matches.returned === 0) {
      cardsRoot.append(
        element("p", {
          className: "empty-state",
          text: "No validated catalogue record matched those bounded terms.",
        }),
      );
    }
    demoStatus.textContent = `${origin}: ${result.matches.total} matching catalogue ${
      result.matches.total === 1 ? "record" : "records"
    }; ${result.matches.returned} returned.`;
  } else {
    cardsRoot.append(describePanel(result));
    demoStatus.textContent = `${origin}: described ${result.record.id} and ${
      result.record.source_records.length
    } linked source ${result.record.source_records.length === 1 ? "record" : "records"}.`;
  }
  jsonRoot.textContent = JSON.stringify(result, null, 2);
  resultsRoot.hidden = false;
}

function renderFailure(error: unknown): void {
  const message =
    error instanceof PageToolInputError || error instanceof Error
      ? error.message
      : "The bounded page tool could not complete.";
  demoStatus.textContent = `Call rejected: ${message}`;
}

async function registerTools(validatedBundle: CatalogueBundle): Promise<void> {
  try {
    const registration = await registerWebMcpTools({
      document,
      bundle: validatedBundle,
      onResult: (result) => renderResult(result, "Browser-hosted AI page-tool call"),
    });
    if (registration.status === "registered") {
      webMcpStatus.textContent = `${registration.toolNames.length} read-only page tools available in this browser.`;
      webMcpStatus.classList.add("status-ready");
    } else {
      webMcpStatus.textContent =
        "Not available in this browser. The complete manual demonstration still works.";
      webMcpStatus.classList.add("status-neutral");
    }
  } catch {
    webMcpStatus.textContent =
      "Tool registration failed closed. The complete manual demonstration still works.";
    webMcpStatus.classList.add("status-warning");
  }
}

async function start(): Promise<void> {
  try {
    const response = await fetch("./catalogue/okf-bundle.json", {
      credentials: "same-origin",
      headers: { Accept: "application/json" },
      redirect: "error",
    });
    if (!response.ok) throw new Error(`Catalogue request failed with status ${response.status}.`);
    bundle = parseCatalogueJson(await response.text());
    catalogueStatus.textContent = `Validated ${bundle.recordCount} records · version ${bundle.version} · revision ${bundle.revision.slice(0, 8)}`;
    catalogueStatus.classList.add("status-ready");
    demoStatus.textContent = "Ready. The manual controls and any registered page tools use the same functions.";
    await registerTools(bundle);
  } catch (error) {
    const message = error instanceof Error ? error.message : "The catalogue could not be read.";
    catalogueStatus.textContent = `Unavailable: ${message}`;
    catalogueStatus.classList.add("status-warning");
    webMcpStatus.textContent = "Not registered because the governed catalogue failed validation.";
    webMcpStatus.classList.add("status-warning");
    demoStatus.textContent =
      "The demonstration stopped. It has not selected substitute data or contacted a provider.";
    queryInput.disabled = true;
    form.querySelector<HTMLButtonElement>("button")!.disabled = true;
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (bundle === undefined) return;
  try {
    const result: PageSearchResult = executePageSearch(bundle, {
      query: queryInput.value,
      limit: 5,
    });
    renderResult(result, "Manual search call");
  } catch (error) {
    renderFailure(error);
  }
});

void start();
