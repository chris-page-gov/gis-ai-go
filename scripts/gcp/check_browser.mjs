#!/usr/bin/env node
/** Actual Chromium against local assets and an explicitly synthetic API fixture. */
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { createServer } from "node:http";
import { readFile, mkdir, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { join, resolve, relative } from "node:path";
import { ROOT } from "./prepare.mjs";

const require = createRequire(join(ROOT, "apps/public-data-workbench/package.json"));
const { chromium } = require("@playwright/test");
const { default: AxeBuilder } = require("@axe-core/playwright");
const outputIndex = process.argv.indexOf("--output");
const output = resolve(ROOT, outputIndex >= 0 ? process.argv[outputIndex + 1] : "artifacts/gcp/browser-local");
assert(output.startsWith(join(ROOT, "artifacts/gcp") + "/"), "Browser evidence belongs under artifacts/gcp");
await mkdir(output, { recursive: true });
const assetFiles = new Map([
  ["/", ["infra/gcp/container/index.html", "text/html; charset=utf-8"]],
  ["/knowledge", ["infra/gcp/container/knowledge/index.html", "text/html; charset=utf-8"]],
  ["/knowledge/", ["infra/gcp/container/knowledge/index.html", "text/html; charset=utf-8"]],
  ["/knowledge/knowledge.js", ["infra/gcp/container/knowledge/knowledge.js", "text/javascript; charset=utf-8"]],
  ["/portal.css", ["infra/gcp/container/portal.css", "text/css; charset=utf-8"]],
]);
const assets = new Map(), source = [];
for (const [route, [path, contentType]] of assetFiles) {
  const bytes = await readFile(join(ROOT, path)); assets.set(route, { bytes, contentType });
  if (!source.some((row) => row.path === path)) source.push({ path, bytes: bytes.length, sha256: createHash("sha256").update(bytes).digest("hex") });
}
const fixture = { id: "synthetic:geography:1", title: "<img src=x onerror=window.__fixtureXss=1> Synthetic geography metadata",
  description: "A made-up public-metadata contract fixture, not an observed provider record.", sourceFamily: "synthetic-fixture",
  temporal: { status: "not-evidenced" }, rights: { executionAdmitted: false, describedData: "Synthetic fixture only" },
  limitations: ["No live data or provider authority"], sources: [{ resource: "https://example.invalid/synthetic" }] };
const release = { schema: "gis-ai-go.gcp-knowledge-release.v1", release_sha256: "a".repeat(64),
  bundles: [{ id: "okf", record_count: 1 }, { id: "okf-plus", record_count: 1 }], classification: "public-metadata",
  provider_egress: false, limitations: ["Synthetic local API fixture; no hosted identity or persistence test"] };
let refuse = false;
const apiRequests = [];
const server = createServer((request, response) => {
  const url = new URL(request.url, "http://127.0.0.1");
  if (url.pathname.startsWith("/api/")) {
    apiRequests.push({ path: url.pathname, bundle: url.searchParams.get("bundle"), limit: url.searchParams.get("limit") });
    response.setHeader("content-type", "application/json"); response.setHeader("cache-control", "no-store");
    if (refuse) { response.writeHead(403); response.end(JSON.stringify({ error: "Synthetic policy refusal" })); return; }
    if (url.pathname === "/api/release") { response.end(JSON.stringify(release)); return; }
    if (url.pathname === "/api/knowledge/search") {
      if (url.searchParams.get("limit") !== "10" || !["okf", "okf-plus"].includes(url.searchParams.get("bundle"))) { response.writeHead(400); response.end("{}"); return; }
      response.end(JSON.stringify({ schema: "gis-ai-go.gcp-knowledge-search.v1", bundle: url.searchParams.get("bundle"), query: url.searchParams.get("query"),
        matched_count: 1, truncated: false, records: [fixture], provenance: release, metadata_only: true, provider_egress: false })); return;
    }
    if (url.pathname === "/api/knowledge/describe" && url.searchParams.get("id") === fixture.id) {
      response.end(JSON.stringify({ schema: "gis-ai-go.gcp-knowledge-record.v1", bundle: url.searchParams.get("bundle"),
        record: fixture, provenance: release, metadata_only: true, provider_egress: false })); return;
    }
    response.writeHead(404); response.end("{}"); return;
  }
  const asset = assets.get(url.pathname);
  if (asset) { response.setHeader("content-type", asset.contentType); response.end(asset.bytes); }
  else { response.writeHead(url.pathname === "/favicon.ico" ? 204 : 404); response.end(); }
});
await new Promise((accept) => server.listen(0, "127.0.0.1", accept));
const origin = "http://127.0.0.1:" + server.address().port;
const report = { schema: "gis-ai-go.gcp-browser-local.v1", status: "running", source,
  scope: "Actual Chromium and existing private assets with a synthetic local API fixture. No cloud, Google/Okta identity, persistent backend, model or live provider acceptance.",
  apiFixture: { records: 1, classification: "synthetic", authentication: "not-tested", persistence: "not-tested" },
  browser: null, checks: [], pageErrors: [], unexpectedNetworkOrigins: [], apiRequests, screenshots: [] };
let browser;
const save = () => writeFile(join(output, "report.json"), JSON.stringify(report, null, 2) + "\n", { mode: 0o600 });
async function check(id, action) {
  try { const evidence = await action(); report.checks.push({ id, status: "passed", ...(evidence ? { evidence } : {}) }); }
  catch (error) { report.checks.push({ id, status: "failed", error: String(error.message).replaceAll(ROOT, "<repository>").slice(0, 1000) }); }
  await save();
}
try {
  browser = await chromium.launch({ headless: true, timeout: 15000 }); report.browser = browser.version();
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, locale: "en-GB", timezoneId: "Europe/London" });
  await context.route("**/*", (route) => {
    if (new URL(route.request().url()).origin !== origin) {
      report.unexpectedNetworkOrigins.push(new URL(route.request().url()).origin); return route.abort("blockedbyclient");
    }
    return route.continue();
  });
  const page = await context.newPage(); page.setDefaultTimeout(5000);
  page.on("pageerror", (error) => report.pageErrors.push(String(error.message).slice(0, 1000)));
  await check("portal-retains-true-authored-corpus-labels", async () => {
    await page.goto(origin + "/", { waitUntil: "networkidle" });
    await page.getByRole("heading", { name: "Find the source. Follow the evidence." }).waitFor();
    assert.match(await page.locator("main").innerText(), /30,833 metadata records/);
    assert.match(await page.locator("main").innerText(), /seven frozen metadata projections/);
    assert.match(await page.locator("main").innerText(), /36-record curated/);
    assert.equal(await page.getByRole("link", { name: "Search and inspect OKF+ metadata" }).getAttribute("href"), "/knowledge");
    return { authoredLabels: [30833, 7, 36], runtimeCorpusNotExercised: true };
  });
  await check("ordinary-browser-search-inspect-and-inert-source-text", async () => {
    await page.getByRole("link", { name: "Search and inspect OKF+ metadata" }).click();
    await page.waitForFunction(() => document.getElementById("release").textContent.includes("okf-plus: 1"));
    await page.getByLabel("One to ten English keywords").fill("synthetic geography");
    await page.getByRole("button", { name: "Search metadata" }).click();
    await page.getByRole("button", { name: "Inspect exact record, sources and rights" }).waitFor();
    assert.equal(await page.locator("#results img").count(), 0);
    assert.match(await page.locator("#results h2").innerText(), /<img src=x/);
    assert.equal(await page.evaluate(() => window.__fixtureXss), undefined);
    await page.getByRole("button", { name: "Inspect exact record, sources and rights" }).click();
    await page.locator("#detail").waitFor({ state: "visible" });
    const evidence = JSON.parse(await page.locator("#record").innerText());
    assert.equal(evidence.record.id, fixture.id); assert.equal(evidence.record.rights.executionAdmitted, false);
    assert.equal(evidence.provenance.release_sha256, release.release_sha256);
    return { fixtureIdentity: fixture.id, sourceInstructionsExecuted: false, modelCalls: 0 };
  });
  for (const [width, scale] of [[320, 1], [390, 1], [1280, 1], [320, 2], [390, 2], [1280, 2]]) {
    await check(`keyboard-layout-and-accessibility-${width}-text-${scale}`, async () => {
      await page.setViewportSize({ width, height: 900 });
      await page.evaluate((scale) => { document.documentElement.style.fontSize = `${scale * 100}%`; }, scale);
      const overflow = await page.evaluate(() => ({ width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
        elements: [...document.querySelectorAll("body *")].filter((node) => node.getBoundingClientRect().right > innerWidth + 2)
          .slice(0, 5).map((node) => ({ tag: node.tagName, id: node.id, width: Math.round(node.getBoundingClientRect().width) })) }));
      assert(overflow.scrollWidth <= overflow.width + 2, "Horizontal overflow: " + JSON.stringify(overflow));
      await page.getByLabel("One to ten English keywords").focus(); await page.keyboard.press("ControlOrMeta+A"); await page.keyboard.type("synthetic"); await page.keyboard.press("Enter");
      await page.getByRole("button", { name: "Inspect exact record, sources and rights" }).waitFor();
      const axe = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa"]).analyze();
      assert.deepEqual(axe.violations.map(({ id }) => id), []);
      const shot = `knowledge-${width}-text-${scale}.png`; await page.screenshot({ path: join(output, shot), fullPage: true });
      report.screenshots.push(relative(ROOT, join(output, shot))); return { width, scale, axeViolations: 0, keyboardSubmit: true };
    });
  }
  await check("visible-policy-refusal", async () => {
    refuse = true; await page.getByRole("button", { name: "Search metadata" }).click();
    await page.waitForFunction(() => document.getElementById("status").textContent.includes("not authorised"));
    assert.equal(await page.locator("#results section").count(), 0); assert.equal(await page.locator("#detail").isHidden(), true);
  });
  assert.deepEqual(report.pageErrors, []); assert.deepEqual(report.unexpectedNetworkOrigins, []);
  report.status = report.checks.every(({ status }) => status === "passed") ? "passed-local-browser-with-synthetic-backend" : "failed-local-browser";
  process.exitCode = report.status === "failed-local-browser" ? 1 : 0;
  await context.close();
} catch (error) {
  report.status = "blocked-or-failed-local-browser";
  report.failure = String(error.message).replaceAll(ROOT, "<repository>").replace(/\/(?:Users|home|Volumes)\/[^\s]+/gu, "<local-path>").slice(0, 1500);
  process.exitCode = 1;
} finally { await browser?.close(); await new Promise((done) => server.close(done)); await save(); }
console.log(JSON.stringify({ status: report.status, checks: report.checks.length, failed: report.checks.filter(({ status }) => status !== "passed").length,
  browser: report.browser, report: relative(ROOT, join(output, "report.json")), hostedAuthentication: false, hostedPersistence: false, bdukAcceptance: false }));
