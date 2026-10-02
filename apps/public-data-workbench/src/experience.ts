import "./experience.css";
import catalogue from "../../../evaluation/experience/catalogue.v1.json";
import { planIntake, canPreviewText, inspectZipArchive, INTAKE_LIMITS, type IntakeFile, type IntakePlan } from "../../../packages/experience-intake/src/index";
import { registerExperienceTools, VIEWS, type ExperienceView } from "./experience-tools";
import { readDroppedFiles } from "./experience-drop";

// The checked-in evaluation catalogue is the authored source for this interface.
interface Feature { id: string; title: string; status: string; maturity?: string; surface: string; operation: string; sourceIds: string[]; conceptIds: string[]; jitSummary: string; boundary: string }
interface Question { id: string; storyId: string; featureIds: string[]; caseType: string; prompt: string; variants: { personaId: string; text: string }[]; jitSummary: string; assertions: { id: string; description: string }[]; executionStatus: string; presentationFormIds: string[] }
interface Catalogue { schema: string; statusDate: string; features: Feature[]; questions: Question[]; personas: { id: string; label: string; languageStyle: string }[]; concepts: { id: string; label: string; jitSummary: string }[]; sources: { id: string; label: string; apiOrData: string; urls: string[]; rightsBoundary: string }[]; presentationForms: { id: string; label: string }[] }
const data = catalogue as Catalogue;
function node<T extends HTMLElement = HTMLElement>(id: string): T { const item = document.getElementById(id); if (!item) throw new Error(`Missing interface: ${id}`); return item as T; }
function element<K extends keyof HTMLElementTagNameMap>(tag: K, text = "", className?: string) { const result = document.createElement(tag); result.textContent = text; if (className) result.className = className; return result; }
const list = (values: string[]) => { const ul = element("ul"); for (const value of values) ul.append(element("li", value)); return ul; };
const featureSelect = node<HTMLSelectElement>("example-choice"), personaSelect = node<HTMLSelectElement>("example-persona"), conceptSelect = node<HTMLSelectElement>("concept-choice"), viewSelect = node<HTMLSelectElement>("example-view");
let selected = data.features[0]!;
let currentView: ExperienceView = "cards";
let fileGeneration = 0;
let dropController: AbortController | undefined;
for (const persona of data.personas) personaSelect.add(new Option(persona.label, persona.id));
for (const concept of data.concepts) conceptSelect.add(new Option(concept.label, concept.id));
function questions() { return data.questions.filter(question => question.featureIds.includes(selected.id)); }
function prompt(question: Question) { return question.variants.find(variant => variant.personaId === personaSelect.value)?.text ?? question.prompt; }
function state() {
  return { schema: "gis-ai-go.experience-page-state.v1", selectedFeature: selected.id, selectedConcept: conceptSelect.value, view: currentView,
    features: data.features.map(({ id, title, status, surface }) => ({ id, title, status, surface })),
    concepts: data.concepts.map(({ id, label }) => ({ id, label })), views: VIEWS, providerCalls: 0,
    limitation: "Authored learning examples; no natural-language or spoken execution is implied. File inputs and previews are excluded from page tools." };
}
function explain(id: string) {
  const concept = data.concepts.find(item => item.id === id); if (!concept) throw new Error("Unknown concept.");
  conceptSelect.value = id; node("concept-detail").replaceChildren(element("h3", concept.label), element("p", concept.jitSummary));
  return { concept: concept.id, explanation: concept.jitSummary };
}
function updateHash() { const params = new URLSearchParams({ feature: selected.id, view: currentView }); history.replaceState(null, "", `#${params}`); }
function render() {
  const detail = node("example-detail"); detail.replaceChildren(element("h2", selected.title), element("span", selected.maturity === "local-increment-unaccepted" ? "Learning preview · separate from live data" : selected.status === "current" ? "Available in its stated profile" : selected.status.replaceAll("-", " "), "tag"), element("span", selected.surface, "tag"), element("p", selected.boundary, "boundary"));
  node("jit-summary").textContent = selected.jitSummary;
  const content = node("example-content"); content.replaceChildren(); const cases = questions();
  if (currentView === "table") {
    const wrap = element("div", "", "table-wrap"), table = element("table"), head = element("thead"), tr = element("tr");
    for (const label of ["Try asking", "What to check", "Kind of test"]) tr.append(element("th", label));
    head.append(tr); table.append(head); const body = element("tbody");
    for (const question of cases) { const row = element("tr"); row.append(element("td", prompt(question)), element("td", question.assertions.map(check => check.description).join(" ")), element("td", question.caseType)); body.append(row); }
    table.append(body); wrap.append(table); content.append(wrap);
  } else if (currentView === "evidence") {
    content.append(element("h3", "Where the information comes from"));
    for (const id of selected.sourceIds) {
      const source = data.sources.find(item => item.id === id); if (!source) continue;
      const article = element("article", "", "example-card"); article.append(element("h3", source.label), element("p", source.apiOrData), element("p", source.rightsBoundary));
      for (const url of source.urls) { try { if (new URL(url).protocol !== "https:") continue; const link = element("a", "Open source documentation"); link.href = url; link.rel = "noreferrer"; article.append(link, element("br")); } catch { /* Invalid source links stay unlinked. */ } }
      content.append(article);
    }
    content.append(element("p", "An example can be documented before it has been tried with a person or an AI. Record what actually happened separately.", "boundary"));
    for (const question of cases) content.append(element("h3", question.id), element("p", `Recorded execution: ${question.executionStatus}`), list(question.assertions.map(check => check.description)));
  } else {
    for (const question of cases) {
      const card = element("article", "", "example-card"); card.append(element("span", question.caseType, "tag"), element("p", prompt(question), "question"), element("p", question.jitSummary));
      card.append(element("h3", "How to tell whether it helped"), list(question.assertions.map(check => check.description)));
      const presentations = question.presentationFormIds.map(id => data.presentationForms.find(form => form.id === id)?.label ?? id);
      card.append(element("p", `Suitable results: ${presentations.join(", ")}.`, "note")); content.append(card);
    }
  }
  if (!cases.length) content.append(element("p", "This facility is planned. Its worked examples and execution checks are still to be admitted.", "boundary"));
  if (selected.surface === "private-sites" && location.protocol !== "file:") { const link = element("a", "Open the private live-data pilot"); link.href = "/pilot"; content.append(link); }
  updateHash();
}
function filter() {
  const query = node<HTMLInputElement>("example-search").value.trim().toLocaleLowerCase("en-GB");
  const matches = data.features.filter(feature => !query || [feature.title, feature.jitSummary, feature.boundary, ...feature.conceptIds].join(" ").toLocaleLowerCase("en-GB").includes(query));
  featureSelect.replaceChildren(); for (const feature of matches) featureSelect.add(new Option(feature.title, feature.id));
  node("example-count").textContent = `${matches.length} activities. Examples are authored; successful use is measured separately.`;
  featureSelect.disabled = !matches.length;
  if (!matches.length) { node("example-detail").replaceChildren(element("p", "No example matches those words. Try a shorter phrase.")); node("example-content").replaceChildren(); return; }
  const next = matches.find(feature => feature.id === selected.id) ?? matches[0]!;
  const changed = next.id !== selected.id; selected = next; featureSelect.value = selected.id; render();
  if (changed && selected.conceptIds[0]) explain(selected.conceptIds[0]);
}
function show(id: string) { const feature = data.features.find(item => item.id === id); if (!feature) throw new Error("Unknown feature."); selected = feature; node<HTMLInputElement>("example-search").value = ""; filter(); if (selected.conceptIds[0]) explain(selected.conceptIds[0]); return { feature: selected.id, title: selected.title, view: currentView, providerCalls: 0 }; }
function setView(view: ExperienceView) { currentView = view; viewSelect.value = view; render(); return { feature: selected.id, view, providerCalls: 0 }; }
node("example-filter").addEventListener("submit", event => { event.preventDefault(); filter(); });
personaSelect.addEventListener("change", render);
featureSelect.addEventListener("change", () => show(featureSelect.value));
conceptSelect.addEventListener("change", () => explain(conceptSelect.value));
viewSelect.addEventListener("change", () => setView(viewSelect.value as ExperienceView));
const hash = new URLSearchParams(location.hash.slice(1));
const requestedFeature = data.features.find(feature => feature.id === hash.get("feature")); if (requestedFeature) selected = requestedFeature;
if (VIEWS.includes(hash.get("view") as ExperienceView)) { currentView = hash.get("view") as ExperienceView; viewSelect.value = currentView; }
filter();
if (selected.conceptIds[0]) explain(selected.conceptIds[0]);
void registerExperienceTools(document, { state, show, view: setView, explain }).then(result => {
  node("page-tool-state").textContent = result.status === "registered" ? "Four learning page tools registered. A connected assistant can choose an example, change its view and explain a word. A spoken connection has not yet been verified." : "Use the controls above. This browser has not registered the learning page tools with an assistant.";
});

function showIntake(plan: IntakePlan) {
  const output = node("intake-results"); output.replaceChildren();
  node("intake-status").textContent = `${plan.evidence.fileCount} files checked. ${plan.evidence.urlCount} links checked. No upload or download.`;
  for (const issue of plan.issues) output.append(element("p", issue.message, "error"));
  for (const item of plan.items) {
    const article = element("article", "", "example-card"); article.append(element("h3", item.label), element("span", item.status.replaceAll("-", " "), "tag"), element("p", item.summary), element("p", item.jit), list(item.nextSteps));
    for (const issue of item.issues) article.append(element("p", issue.message, issue.severity === "error" ? "error" : "note"));
    if (item.preview) {
      article.append(element("h3", "Local preview"), element("p", item.preview.summary));
      if (item.preview.rows) { const wrap = element("div", "", "table-wrap"), table = element("table");
        table.append(element("caption", "Preview rows; check the heading-row assumption below"));
        for (const values of item.preview.rows) { const row = element("tr"); for (const value of values) row.append(element("td", value)); table.append(row); } wrap.append(table); article.append(wrap);
      } else if (item.preview.excerpt !== undefined) article.append(element("pre", item.preview.excerpt));
      else article.append(element("pre", JSON.stringify(item.preview, null, 2)));
      article.append(list(item.preview.limitations));
    }
    if (item.companionSuggestions?.length) { article.append(element("h3", "Possible companion locations"), element("p", "These are suggestions from the name, not verified files. No website has been contacted."), list(item.companionSuggestions)); }
    output.append(article);
  }
}
async function readFiles(files: readonly File[], paths?: string[]) {
  dropController?.abort();
  const generation = ++fileGeneration;
  const descriptors: IntakeFile[] = files.map((file, i) => ({ name: file.name, size: file.size, ...(paths?.[i] || file.webkitRelativePath ? { relativePath: paths?.[i] || file.webkitRelativePath } : {}) }));
  const preflight = planIntake({ files: descriptors });
  if (preflight.status === "blocked") { showIntake(preflight); return; }
  let total = 0; node("intake-status").textContent = "Checking small files on this device…";
  try {
    const archives: { index: number; plan: IntakePlan }[] = [];
    let batchEntries = files.length, batchBytes = files.reduce((sum, file) => sum + file.size, 0);
    for (let i = 0; i < files.length; i++) { if (generation !== fileGeneration) return; const file = files[i]!, descriptor = descriptors[i]!;
      if (canPreviewText(file.name, file.size) && total + file.size <= INTAKE_LIMITS.totalPreviewBytes) { total += file.size; descriptor.text = await file.text(); }
      else if (/\.zip$/iu.test(file.name) && file.size <= INTAKE_LIMITS.fileBytes) {
        const plan = inspectZipArchive(file.name, await file.arrayBuffer());
        batchEntries += plan.evidence.archive?.memberCount ?? 0; batchBytes += plan.evidence.archive?.declaredExpandedBytes ?? 0;
        if (batchEntries > INTAKE_LIMITS.files || batchBytes > INTAKE_LIMITS.totalBytes) {
          if (generation !== fileGeneration) return;
          const refused = planIntake({ files: [] }); refused.status = "blocked";
          refused.issues.push({ code: "archive-batch-limit", severity: "error", message: "The selected files and their ZIP members exceed 64 entries or 50 MiB in total. Choose one smaller dataset; no partial inventory is shown." });
          showIntake(refused); return;
        }
        archives.push({ index: i, plan });
      }
    }
    if (generation === fileGeneration) {
      const plan = planIntake({ files: descriptors });
      for (const archive of archives) {
        plan.items.push(...archive.plan.items.map(item => ({ ...item, id: `archive-${archive.index}-${item.id}`, label: `${files[archive.index]!.name}: ${item.label}` })));
        plan.issues.push(...archive.plan.issues);
        if (archive.plan.status === "blocked") plan.status = "blocked";
      }
      // Retain the original archive's unextracted-content warning beside its member inventory.
      showIntake(plan);
    }
  } catch { if (generation === fileGeneration) node("intake-status").textContent = "A file could not be read. Select it again or try the made-up example."; }
}
for (const id of ["intake-files", "intake-folder"]) node<HTMLInputElement>(id).addEventListener("change", () => { void readFiles(Array.from(node<HTMLInputElement>(id).files ?? [])); });
const dropZone = node("drop-zone");
dropZone.addEventListener("dragover", event => { event.preventDefault(); dropZone.classList.add("dragging"); });
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragging"));
dropZone.addEventListener("drop", event => { event.preventDefault(); dropZone.classList.remove("dragging");
  if (!event.dataTransfer) return;
  dropController?.abort(); const controller = new AbortController(); dropController = controller;
  const generation = ++fileGeneration; node("intake-status").textContent = "Checking the dropped files and folders…";
  void readDroppedFiles(event.dataTransfer, controller.signal).then(result => { if (!controller.signal.aborted && generation === fileGeneration) return readFiles(result.files, result.paths); }).catch(() => {
    if (!controller.signal.aborted && generation === fileGeneration) node("intake-status").textContent = "The dropped folder could not be read within the file and time limits. Choose a smaller folder or select the matching files together.";
  });
});
node("url-form").addEventListener("submit", event => { event.preventDefault(); ++fileGeneration; dropController?.abort(); showIntake(planIntake({ files: [], urls: [node<HTMLInputElement>("intake-url").value] })); });
node("synthetic-example").addEventListener("click", () => { ++fileGeneration; dropController?.abort(); const text = JSON.stringify({ type: "FeatureCollection", features: [{ type: "Feature", properties: { name: "Example park", source: "Made-up teaching fixture; not a real park" }, geometry: { type: "Point", coordinates: [-4, 51.6] } }] }, null, 2); showIntake(planIntake({ files: [{ name: "made-up-park.geojson", size: new TextEncoder().encode(text).byteLength, text }] })); node("intake-results").append(element("h3", "The made-up source: try changing its name in your programme"), element("pre", text)); });
node("clear-intake").addEventListener("click", () => { ++fileGeneration; dropController?.abort(); node("intake-results").replaceChildren(); node("intake-status").textContent = "Files and previews cleared from this page."; for (const id of ["intake-files", "intake-folder", "intake-url"]) node<HTMLInputElement>(id).value = ""; });
window.addEventListener("pagehide", () => { ++fileGeneration; dropController?.abort(); }, { once: true });
node("download-session").addEventListener("click", () => {
  const checklist = { schema: "gis-ai-go.experience-checklist.v1", featureId: selected.id, view: currentView, personaId: personaSelect.value || null,
    questions: questions().map(question => ({ id: question.id, prompt: prompt(question), assertions: question.assertions, observedOutcome: "not-recorded" })),
    providerCalls: 0, containsUploadedFiles: false };
  const url = URL.createObjectURL(new Blob([JSON.stringify(checklist, null, 2) + "\n"], { type: "application/json" }));
  const link = element("a"); link.href = url; link.download = "gis-ai-go-example-checklist.json"; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
});
