import "./styles.css";
import { findData } from "./discovery";
import { createHostedMcpCall, createMcpCall } from "./mcp-client";
import { createWorkbench, type EvidenceResult, type Plan } from "./controller";
import { registerPageTools } from "./webmcp";

function node<T extends HTMLElement = HTMLElement>(id: string): T {
  const found = document.getElementById(id);
  if (!found) throw new Error(`Missing interface element: ${id}`);
  return found as T;
}
function element(tag: string, text: string, className?: string) {
  const item = document.createElement(tag); item.textContent = text;
  if (className) item.className = className;
  return item;
}
// Build-authored mode only: neither a URL argument nor returned evidence selects it.
const hosted = import.meta.env.MODE === "hosted";
const workbench = hosted
  ? createWorkbench(createHostedMcpCall(window.location), { evidenceMode: "hosted-transaction" })
  : createWorkbench(createMcpCall(window.location));
let currentPlan: Plan | undefined, currentResult: EvidenceResult | undefined, active: AbortController | undefined;
const status = node("status"), retrieveButton = node<HTMLButtonElement>("retrieve-button");
function showDiscovery(input: unknown) {
  const container = node("results");
  let result: ReturnType<typeof findData>;
  try { result = findData(input); }
  catch (error) {
    node("result-count").textContent = error instanceof Error ? error.message : "Search failed.";
    container.replaceChildren(); throw error;
  }
  container.replaceChildren();
  node("result-count").textContent = `${result.records.length} matches · 7 frozen records`;
  for (const record of result.records) {
    const card = element("article", "", `record${record.id === "ons-data-api:cpih01" ? " selected" : ""}`);
    card.append(element("span", record.id, "record-id"), element("h3", record.title), element("p", record.description.slice(0, 260)));
    for (const edge of record.concept_edges) card.append(element("span", `${edge.concept} · curated`, "tag"));
    if (record.id === "ons-data-api:cpih01") {
      card.append(element("p", "Retired endpoint. A separate maintained-series capture is available for this experiment."));
      const button = element("button", "Review maintained-series capture") as HTMLButtonElement;
      button.type = "button"; button.className = "secondary";
      button.addEventListener("click", () => { node("period").focus(); node("desk-heading").scrollIntoView({ block: "start", behavior: "smooth" }); });
      card.append(button);
    } else card.append(element("p", "Discovery only · retrieval not implemented", "tag"));
    container.append(card);
  }
  if (!result.records.length) container.append(element("p", "No match in this seven-record sample. Try fewer keywords; an empty result does not prove that ONS has no relevant data."));
  return result;
}
function showPlan(plan: Plan) {
  currentPlan = plan; currentResult = undefined;
  node<HTMLSelectElement>("period").value = plan.period;
  const target = node("selection"); target.className = "selection-plan"; target.replaceChildren();
  target.append(element("strong", `${plan.period === "2026-07" ? "July" : "January"} 2026 · one captured observation`),
    element("p", "L522 / MM23 · index, 2015 = 100 · no live provider request"),
    element("p", "Plan received. It is a proposal, not permission; the server independently checks the retrieval."));
  node("observation").hidden = true; node("receipt-actions").hidden = true; node("evidence-detail").hidden = true;
  retrieveButton.disabled = false;
  status.textContent = "Selection reviewed. Retrieval will create or replay a durable evidence record.";
  return plan.raw;
}
function showResult(result: EvidenceResult, inspected = false) {
  currentResult = result;
  const panel = node("observation"); panel.replaceChildren(); panel.hidden = false;
  panel.append(element("p", `${result.period === "2026-07" ? "July" : "January"} 2026 · CPIH all items`, "eyebrow"),
    element("div", result.value, "observation-value"), element("p", "Index level · 2015 = 100 · not an inflation percentage", "observation-meta"),
    element("p", inspected ? "Existing receipt returned by MCP inspection. No new receipt was issued."
      : hosted ? "Returned by the private Site's MCP route from the admitted ONS capture. Receipt found in the verified storage snapshot."
      : "Returned by the local MCP server from the admitted ONS capture. Receipt persisted.", "observation-meta"));
  if (hosted) panel.append(element("p", "The server checked the stored snapshot's content and chain. This page receives only the selected evidence: it does not independently prove the complete chain, freshness, rollback protection or an attestation.", "observation-meta"));
  node("receipt-actions").hidden = false; node("evidence-detail").hidden = false;
  node("evidence-json").textContent = JSON.stringify(result.raw, null, 2);
  status.textContent = inspected ? "Stored evidence inspected; no live provider request or new receipt." : "Captured observation retrieved. Repeating this selection reuses its request key.";
  return result.raw;
}
async function execute<T>(action: (signal: AbortSignal) => Promise<T>, signal?: AbortSignal): Promise<T> {
  if (active) throw new Error("An operation is already running.");
  const controller = new AbortController(); active = controller;
  const joined = signal ? AbortSignal.any([controller.signal, signal]) : controller.signal;
  node("cancel-button").hidden = false; status.textContent = hosted ? "Calling this private Site's MCP route…" : "Calling the local MCP server…";
  try { return await action(joined); }
  catch (error) { status.textContent = error instanceof Error ? error.message : "The operation could not be completed."; throw error; }
  finally { active = undefined; node("cancel-button").hidden = true; }
}
const actions = {
  find: async (input: unknown, signal?: AbortSignal) => { signal?.throwIfAborted(); return showDiscovery(input); },
  select: (input: unknown, signal?: AbortSignal) => execute(async (joined) => showPlan(await workbench.select(input, joined)), signal),
  retrieve: (input: unknown, signal?: AbortSignal) => execute(async (joined) => {
    if (!currentPlan) throw new Error("Review the selected month on this page before retrieving it.");
    return showResult(await workbench.retrieve(input, joined));
  }, signal),
  inspect: (input: unknown, signal?: AbortSignal) => execute(async (joined) => showResult(await workbench.inspect(input, joined), true), signal),
};
node("search-form").addEventListener("submit", (event) => {
  event.preventDefault(); try { showDiscovery({ query: node<HTMLInputElement>("query").value }); }
  catch { /* The shared discovery action has already rendered the failure. */ }
});
document.querySelectorAll<HTMLButtonElement>("[data-query]").forEach((button) => button.addEventListener("click", () => {
  node<HTMLInputElement>("query").value = button.dataset.query!; showDiscovery({ query: button.dataset.query });
}));
node("selection-form").addEventListener("submit", (event) => { event.preventDefault(); void actions.select({ period: node<HTMLSelectElement>("period").value }).catch(() => undefined); });
node("period").addEventListener("change", () => {
  active?.abort(); workbench.invalidateSelection();
  currentPlan = undefined; retrieveButton.disabled = true;
  node("selection").replaceChildren(element("p", "The chosen month changed. Review it before retrieving."));
  status.textContent = "The previous selection is no longer staged on this page.";
});
retrieveButton.addEventListener("click", () => { void actions.retrieve({ selection_plan_id: currentPlan?.planId }).catch(() => undefined); });
node("inspect-button").addEventListener("click", () => { void actions.inspect({ receipt_id: currentResult?.receiptId }).catch(() => undefined); });
node("cancel-button").addEventListener("click", () => active?.abort());
node("download-button").addEventListener("click", () => {
  if (!currentResult) return;
  const url = URL.createObjectURL(new Blob([JSON.stringify(currentResult.raw, null, 2) + "\n"], { type: "application/json" }));
  const link = document.createElement("a"); link.href = url; link.download = `gis-ai-go-cpih-${currentResult.period}.json`; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
});
showDiscovery({ query: "consumer prices" });
void registerPageTools(document, actions).then(({ status: registration }) => {
  node("webmcp-status").textContent = registration === "registered"
    ? "Four page tools registered with this browser. Your AI still needs a compatible host connection; registration alone is not an observed AI call."
    : registration === "unsupported" ? "This browser does not expose the page-scoped WebMCP interface. The manual journey remains available."
    : "Page-tool registration failed. No complete tool set is claimed; use the manual journey.";
});
window.addEventListener("pagehide", () => active?.abort(), { once: true });
