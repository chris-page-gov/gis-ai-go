const get = (id) => document.getElementById(id);
const node = (tag, text) => { const element = document.createElement(tag); element.textContent = text; return element; };
const status = get("status"), results = get("results");
let pending;

async function request(path, signal) {
  const target = new URL(path, window.location.origin);
  if (target.origin !== window.location.origin || !["/api/release", "/api/knowledge/search", "/api/knowledge/describe"].includes(target.pathname)) throw Error("Unapproved knowledge route");
  const response = await fetch(target, { credentials: "same-origin", redirect: "error", cache: "no-store",
    signal: AbortSignal.any([AbortSignal.timeout(15000), ...(signal ? [signal] : [])]) });
  if (!response.ok) throw Error(response.status === 401 || response.status === 403 ? "This private connection is not authorised for the requested knowledge." : "The admitted knowledge release is currently unavailable.");
  return response.json();
}

async function inspect(bundle, id, signal) {
  const selected = await request("/api/knowledge/describe?" + new URLSearchParams({ bundle, id }), signal);
  if (selected.schema !== "gis-ai-go.gcp-knowledge-record.v1" || selected.bundle !== bundle || !selected.record ||
      (selected.record.id ?? selected.record["@id"]) !== id || selected.provider_egress !== false) throw Error("The server returned an unexpected knowledge record.");
  get("detail").hidden = false;
  get("detail-summary").textContent = selected.record.title;
  get("record").textContent = JSON.stringify(selected, null, 2);
  get("detail").scrollIntoView({ block: "start" });
  status.textContent = "Exact retained record inspected. Source rights and evidence limits are shown below.";
}

get("search-form").addEventListener("submit", async (event) => {
  event.preventDefault(); pending?.abort(); const controller = new AbortController(); pending = controller;
  const bundle = get("bundle").value, query = get("query").value;
  status.textContent = "Searching this deployment's admitted release…"; results.replaceChildren(); get("detail").hidden = true;
  try {
    const found = await request("/api/knowledge/search?" + new URLSearchParams({ bundle, query, limit: "10" }), controller.signal);
    if (found.schema !== "gis-ai-go.gcp-knowledge-search.v1" || found.bundle !== bundle || !Array.isArray(found.records) || found.records.length > 10 || found.provider_egress !== false) throw Error("The server returned an unexpected knowledge result.");
    status.textContent = `${found.matched_count} matching catalogue representations; showing ${found.records.length}${found.truncated ? ". More matches are omitted by this bounded view." : "."}`;
    for (const record of found.records) {
      const card = node("section", ""); card.append(node("h2", record.title), node("p", record.description ?? ""));
      if (record.sourceFamily) card.append(node("p", `Source family: ${record.sourceFamily}`));
      card.append(node("p", JSON.stringify(record.temporal ?? {}, null, 2)));
      for (const limit of record.limitations ?? []) card.append(node("p", limit));
      const button = node("button", "Inspect exact record, sources and rights"); button.type = "button";
      button.addEventListener("click", () => { void inspect(bundle, record.id, controller.signal).catch((error) => { status.textContent = error.message; }); });
      card.append(button); results.append(card);
    }
    if (!found.records.length) results.append(node("p", "No retained match. This does not prove the source has no relevant data."));
  } catch (error) { if (!controller.signal.aborted) status.textContent = error.message; }
});

void request("/api/release").then((release) => {
  if (release.schema !== "gis-ai-go.gcp-knowledge-release.v1" || !Array.isArray(release.bundles)) throw Error("Unexpected release descriptor");
  get("release").textContent = release.bundles.map((bundle) => `${bundle.id}: ${bundle.record_count.toLocaleString("en-GB")} source-native records`).join(" · ") + ` · content identity ${release.release_sha256}`;
}).catch((error) => { get("release").textContent = error.message; });
