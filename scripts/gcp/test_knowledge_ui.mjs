import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { join } from "node:path";
import { ROOT } from "./prepare.mjs";

const require = createRequire(join(ROOT, "apps/public-data-workbench/package.json"));
const { JSDOM } = require("jsdom");
const tick = () => new Promise((resolve) => setTimeout(resolve, 15));

test("ordinary knowledge journey uses same-origin bounded APIs and treats metadata as text (local mock)", async () => {
  const html = await readFile(join(ROOT, "infra/gcp/container/knowledge/index.html"), "utf8");
  const code = await readFile(join(ROOT, "infra/gcp/container/knowledge/knowledge.js"), "utf8");
  const dom = new JSDOM(html, { url: "https://private-pilot.run.app/knowledge/", runScripts: "outside-only" });
  const { window } = dom;
  window.AbortSignal = AbortSignal; window.AbortController = AbortController;
  window.HTMLElement.prototype.scrollIntoView = () => undefined;
  const calls = [], title = "<img src=x onerror=alert(1)> Synthetic metadata";
  const record = { id: "synthetic:record", title, description: "Admitted synthetic evidence", limitations: ["No live retrieval"], sources: [], rights: { executionAdmitted: false } };
  window.fetch = async (target, options) => {
    const url = new URL(String(target)); calls.push({ url, options });
    assert.equal(url.origin, "https://private-pilot.run.app");
    assert.equal(options.credentials, "same-origin"); assert.equal(options.redirect, "error"); assert.equal(options.cache, "no-store");
    assert.ok(options.signal instanceof AbortSignal);
    let body;
    if (url.pathname === "/api/release") body = { schema: "gis-ai-go.gcp-knowledge-release.v1", bundles: [{ id: "okf", record_count: 36 }, { id: "okf-plus", record_count: 30833 }], release_sha256: "a".repeat(64) };
    else if (url.pathname === "/api/knowledge/search") {
      assert.equal(url.searchParams.get("limit"), "10"); assert.equal(url.searchParams.get("bundle"), "okf-plus");
      body = { schema: "gis-ai-go.gcp-knowledge-search.v1", bundle: "okf-plus", records: [record], matched_count: 14, truncated: true, provider_egress: false };
    } else if (url.pathname === "/api/knowledge/describe") {
      assert.equal(url.searchParams.get("id"), "synthetic:record");
      body = { schema: "gis-ai-go.gcp-knowledge-record.v1", bundle: "okf-plus", record, provider_egress: false };
    } else assert.fail("Unexpected network request");
    return new Response(JSON.stringify(body), { headers: { "content-type": "application/json" } });
  };
  try {
    window.eval(code); await tick();
    assert.match(window.document.getElementById("release").textContent, /30,833/);
    window.document.getElementById("search-form").dispatchEvent(new window.Event("submit", { bubbles: true, cancelable: true }));
    await tick();
    assert.match(window.document.getElementById("status").textContent, /14 matching.*More matches/);
    assert.equal(window.document.querySelector("#results h2").textContent, title);
    assert.equal(window.document.querySelector("#results img"), null);
    window.document.querySelector("#results button").click(); await tick();
    assert.equal(window.document.getElementById("detail").hidden, false);
    assert.match(window.document.getElementById("record").textContent, /executionAdmitted/);
    assert.deepEqual(calls.map(({ url }) => url.pathname), ["/api/release", "/api/knowledge/search", "/api/knowledge/describe"]);
  } finally { window.close(); }
});

test("knowledge refusal is visible and never presented as empty successful evidence (local mock)", async () => {
  const html = await readFile(join(ROOT, "infra/gcp/container/knowledge/index.html"), "utf8");
  const code = await readFile(join(ROOT, "infra/gcp/container/knowledge/knowledge.js"), "utf8");
  const dom = new JSDOM(html, { url: "https://private-pilot.run.app/knowledge/", runScripts: "outside-only" });
  const { window } = dom; window.AbortSignal = AbortSignal; window.AbortController = AbortController;
  window.fetch = async () => new Response("", { status: 403 });
  try {
    window.eval(code); await tick();
    window.document.getElementById("search-form").dispatchEvent(new window.Event("submit", { bubbles: true, cancelable: true }));
    await tick();
    assert.match(window.document.getElementById("status").textContent, /not authorised/);
    assert.equal(window.document.getElementById("results").childElementCount, 0);
    assert.equal(window.document.getElementById("detail").hidden, true);
  } finally { window.close(); }
});
