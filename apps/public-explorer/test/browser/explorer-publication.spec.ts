import { createHash } from "node:crypto";
import AxeBuilder from "@axe-core/playwright";
import { expect, test as base, type Page } from "@playwright/test";

const PUBLIC_BASE = new URL(required("PUBLIC_BASE_URL"));
const SOURCE = required("EXPECTED_SOURCE_COMMIT");
const CANONICAL = new URL("https://chris-page-gov.github.io/gis-ai-go/");
const DESCRIPTOR = new URL("gis/explorer/okf-explorer.json", CANONICAL).href;
const LOCAL = PUBLIC_BASE.hostname === "127.0.0.1" || PUBLIC_BASE.hostname === "localhost";
const APP_TREE = "d127aadb96a77711d5f7cc7aec8cf731cbf5ec1e3d49304d8132189ea4991f93";
const APP_MANIFEST = "ab227164e2e114148425a453a0e04b6bb21230f79be1e059a3ff6936d57f45f2";
type Step = { title: string; route: string };
type LearningPath = { id: string; title: string; steps: Step[] };
type Descriptor = {
  schema: string;
  snapshot: string;
  source: { revision: string; inputDigest: string };
  counts: { records: number };
  learning_presentation: { paths: LearningPath[] };
};
type Transport = { requests: string[]; mirrorRequests: string[] };

function required(name: string): string {
  const value = process.env[name]?.trim();
  if (!value) throw new Error(name + " is required for Explorer publication assurance");
  return value;
}
function publicUrl(relative = ""): string {
  return new URL(relative, PUBLIC_BASE).href;
}
function readerUrl(route = "overview"): string {
  const url = new URL("explorer/explore/", PUBLIC_BASE);
  url.searchParams.set("bundle", DESCRIPTOR);
  url.hash = route;
  return url.href;
}
function inPrefix(value: string, prefix: URL): boolean {
  const url = new URL(value);
  return url.origin === prefix.origin && url.pathname.startsWith(prefix.pathname);
}
function shards(requests: string[]): string[] {
  return [...new Set(requests.filter(value => /\/gis\/explorer\/records\/\d+\.json(?:\?|$)/u.test(value)))];
}
async function selectedRoute(page: Page, route: string): Promise<void> {
  await expect.poll(() => new URL(page.url()).hash.slice(1)).toBe(encodeURI(route));
}
async function axe(page: Page): Promise<void> {
  const result = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
    .analyze();
  expect(result.violations.filter(item => item.impact === "serious" || item.impact === "critical")).toEqual([]);
}

const test = base.extend<{ transport: Transport }>({
  transport: [
    async ({ page, context, request }, use, info) => {
      const requests: string[] = [];
      const mirrorRequests: string[] = [];
      const failures: string[] = [];
      const statuses = new Map<string, number>();
      if (LOCAL) {
        // Offline candidate transport only: preserve the canonical requested URL
        // and digest-bound response bytes while reading the exact staged mirror.
        // The deployed-publication mode never installs this interception.
        await context.route(CANONICAL.href + "**", async route => {
          const original = new URL(route.request().url());
          if (!inPrefix(original.href, CANONICAL)) throw new Error("canonical mirror escaped publication prefix");
          const mirror = new URL(original.pathname.slice(CANONICAL.pathname.length) + original.search, PUBLIC_BASE);
          mirrorRequests.push(original.href);
          const response = await request.get(mirror.href, { maxRedirects: 0, timeout: 30_000 });
          expect(response.status(), "the exact local publication mirror must be available").toBe(200);
          await route.fulfill({
            response,
            headers: { ...response.headers(), "access-control-allow-origin": PUBLIC_BASE.origin },
          });
        });
      }
      page.on("request", requestValue => {
        const value = requestValue.url();
        if (requests.length >= 4000) failures.push("UI publication request ceiling exceeded");
        else requests.push(value);
        if (!inPrefix(value, PUBLIC_BASE) && !(LOCAL && inPrefix(value, CANONICAL))) {
          failures.push("unexpected request: " + value);
        }
      });
      page.on("response", response => {
        statuses.set(response.url(), response.status());
        if (response.status() >= 400) failures.push("HTTP " + response.status() + ": " + response.url());
      });
      page.on("requestfailed", value => {
        const successfulAbort = value.failure()?.errorText === "net::ERR_ABORTED" &&
          (statuses.get(value.url()) ?? 0) >= 200 && (statuses.get(value.url()) ?? 0) < 300;
        if (!successfulAbort) failures.push("request failed: " + value.url() + " " + value.failure()?.errorText);
      });
      page.on("pageerror", error => failures.push("page error: " + error.message));
      page.on("console", message => {
        if (message.type() === "error") failures.push("console error: " + message.text());
      });
      await use({ requests, mirrorRequests });
      await info.attach("publication-transport", {
        body: JSON.stringify({
          mode: LOCAL ? "loopback-candidate-with-canonical-byte-mirror" : "deployed-publication",
          sourceCommit: SOURCE, requests, mirrorRequests, failures,
        }, null, 2),
        contentType: "application/json",
      });
      expect(failures, "publication UI transport and runtime must remain clean").toEqual([]);
    },
    { auto: true },
  ],
});

async function descriptor(page: Page): Promise<Descriptor> {
  const response = await page.request.get(publicUrl("gis/explorer/okf-explorer.json"), { maxRedirects: 0 });
  expect(response.status()).toBe(200);
  const value = await response.json() as Descriptor;
  expect(value.schema).toBe("okf-explorer-large-corpus.v1");
  expect(value.source.revision).toBe(SOURCE);
  expect(value.source.inputDigest).toBe(required("EXPECTED_OKF_CONTENT_ROOT"));
  expect(value.counts.records).toBe(30_876);
  expect(value.learning_presentation.paths).toHaveLength(3);
  expect(value.learning_presentation.paths.flatMap(item => item.steps)).toHaveLength(11);
  return value;
}

test("GIS root opens the accepted full Explorer with linked learning and no eager record shards", async ({ page, transport }) => {
  const value = await descriptor(page);
  const manifestResponse = await page.request.get(publicUrl("explorer/okf-explorer-build-manifest.json"), { maxRedirects: 0 });
  expect(manifestResponse.status()).toBe(200);
  const bytes = await manifestResponse.body();
  expect(createHash("sha256").update(bytes).digest("hex")).toBe(APP_MANIFEST);
  expect(JSON.parse(bytes.toString()).tree_sha256).toBe(APP_TREE);
  await page.goto(publicUrl(), { waitUntil: "networkidle" });
  expect(new URL(page.url()).pathname).toBe(PUBLIC_BASE.pathname + "explorer/explore/");
  expect(new URL(page.url()).searchParams.get("bundle")).toBe(publicUrl("gis/explorer/okf-explorer.json"));
  await expect(page.getByRole("heading", { name: "INSPIRE polygon: indicative or legal boundary?", exact: true })).toHaveCount(0);
  const paths = page.getByRole("region", { name: "Learning paths", exact: true });
  await expect(paths).toBeVisible();
  await expect(paths.locator(":scope > details")).toHaveCount(3);
  expect(shards(transport.requests)).toEqual([]);
  for (const [index, learning] of value.learning_presentation.paths.entries()) {
    const details = paths.locator(":scope > details").nth(index);
    if (await details.getAttribute("open") === null) await details.locator("summary").click();
    for (const step of learning.steps) {
      const before = transport.requests.length;
      await paths.getByRole("button", { name: step.title, exact: true }).click();
      await selectedRoute(page, step.route);
      await expect(paths.getByRole("status")).toContainText(step.title);
      // A shared route may reuse a retained shard; a new route is targeted.
      expect(shards(transport.requests.slice(before)).length).toBeLessThanOrEqual(1);
    }
  }
  const first = value.learning_presentation.paths[0]!;
  const details = paths.locator(":scope > details").first();
  if (await details.getAttribute("open") === null) await details.locator("summary").click();
  const step = first.steps[0]!;
  await paths.getByRole("button", { name: step.title, exact: true }).focus();
  await page.keyboard.press("Enter");
  await selectedRoute(page, step.route);
  await paths.getByRole("checkbox", { name: "I have completed " + step.title, exact: true }).check();
  await expect(details.locator("summary")).toContainText("1/" + first.steps.length + " complete");
  await paths.getByRole("button", { name: "Reset learning progress", exact: true }).click();
  await expect(details.locator("summary")).toContainText("0/" + first.steps.length + " complete");
  await page.getByRole("link", { name: "OKF Explorer — return to the learning hub", exact: true }).click();
  await expect(page.getByRole("heading", { level: 1 })).toContainText("Use knowledge you can inspect");
  await page.getByRole("link", { name: "Read the beginner guide", exact: true }).click();
  expect(new URL(page.url()).pathname).toBe(PUBLIC_BASE.pathname + "explorer/docs/beginners/index.html");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
});

test("native field context retains sources and gaps and prefills evidence discovery without running it", async ({ page }) => {
  const value = await descriptor(page);
  await page.goto(readerUrl(), { waitUntil: "networkidle" });
  const paths = page.getByRole("region", { name: "Learning paths", exact: true });
  for (const sample of [
    { title: "Inspect Road Link v5 width fields", field: "presenceofpavement_averagewidth_m" },
    { title: "Inspect the Building v4 field evidence", field: "height_relativemax_m" },
    { title: "Inspect road geometry and elevation fields", field: "elevationgain_indirection" },
  ]) {
    const index = value.learning_presentation.paths.findIndex(item => item.steps.some(step => step.title === sample.title));
    expect(index).toBeGreaterThanOrEqual(0);
    const details = paths.locator(":scope > details").nth(index);
    if (await details.getAttribute("open") === null) await details.locator("summary").click();
    await paths.getByRole("button", { name: sample.title, exact: true }).click();
    const explanation = page.getByRole("region", { name: "Record explanation and sources", exact: true });
    await expect(explanation).toBeVisible();
    const fields = explanation.getByRole("combobox", { name: "Choose a native field", exact: true });
    const fieldValue = await fields.locator("option").evaluateAll((options, name) => {
      return (options.find(option => option.textContent?.includes(name)) as HTMLOptionElement | undefined)?.value;
    }, sample.field);
    expect(fieldValue).toBeTruthy();
    await fields.selectOption(fieldValue!);
    await expect(explanation.getByRole("heading", { name: "Selected field: " + sample.field, exact: true })).toBeVisible();
    await expect(explanation).toContainText(SOURCE);
    await expect(explanation).toContainText(/not supplied|not evidenced|not established|unresolved|not retained|not recorded|missing|unknown/iu);
    const links = await explanation.getByRole("link").evaluateAll(nodes => nodes.map(node => (node as HTMLAnchorElement).href));
    expect(links.some(href => href.startsWith("https://"))).toBe(true);
    await explanation.getByRole("button", { name: "Find supporting evidence", exact: true }).click();
    await expect(page.getByRole("heading", { name: "Ask OKF", exact: true })).toBeVisible();
    await expect(page.getByRole("textbox", { name: "Question", exact: true })).not.toHaveValue("");
    await expect(page.locator(".context-package")).toHaveCount(0);
    await page.getByRole("button", { name: "Search", exact: true }).first().click();
  }
});

test("full-corpus search and Ask preserve bounded evidence and explicit insufficiency", async ({ page }) => {
  test.setTimeout(180_000);
  await page.goto(readerUrl(), { waitUntil: "networkidle" });
  for (const query of ["pavement width", "building height", "road elevation"]) {
    await page.getByRole("button", { name: "Search", exact: true }).first().click();
    await page.locator("input.search-input").fill(query);
    await expect.poll(() => new URL(page.url()).searchParams.get("q")).toBe(query);
    const results = page.locator('[data-okf-ranked-results="primary"]');
    await expect(results).toHaveAttribute("data-okf-query", query);
    await expect(results).toHaveAttribute("data-okf-search-state", "settled");
    await expect(page.locator("[data-okf-ranked-result]").first()).toBeVisible();
  }
  await page.getByRole("button", { name: "Ask OKF", exact: true }).click();
  for (const query of ["pavement width", "building height", "road elevation"]) {
    const previous = await page.locator(".context-package").count()
      ? await page.locator(".context-package").getAttribute("data-context-id") : null;
    await page.getByRole("textbox", { name: "Question", exact: true }).fill(query);
    await page.getByRole("button", { name: "Build evidence package", exact: true }).click();
    await expect(page.locator(".context-package")).toBeVisible({ timeout: 45_000 });
    await expect.poll(() => page.locator(".context-package").getAttribute("data-context-id"), { timeout: 45_000 }).not.toBe(previous);
    await page.getByRole("button", { name: "Inspect package JSON", exact: true }).click();
    const evidence = JSON.parse(await page.getByLabel("Evidence package JSON", { exact: true }).inputValue()) as {
      evidence_status: string;
      retrieval: {
        corpus_records: number; candidate_count: number; fetched_files: number; fetched_bytes: number; decoded_bytes: number;
        limits: { files: number; fetched_bytes: number; decoded_bytes: number };
      };
      budget: { used_nodes: number; max_nodes: number };
    };
    expect(evidence.evidence_status).toBe("insufficient");
    expect(evidence.retrieval.corpus_records).toBe(30_876);
    expect(evidence.retrieval.candidate_count).toBeGreaterThan(0);
    expect(evidence.retrieval.fetched_files).toBeLessThanOrEqual(evidence.retrieval.limits.files);
    expect(evidence.retrieval.fetched_bytes).toBeLessThanOrEqual(evidence.retrieval.limits.fetched_bytes);
    expect(evidence.retrieval.decoded_bytes).toBeLessThanOrEqual(evidence.retrieval.limits.decoded_bytes);
    expect(evidence.budget.used_nodes).toBeLessThanOrEqual(evidence.budget.max_nodes);
  }
});

for (const width of [1440, 390, 320]) {
  test("compact facets preserve exact state, palette keyboard controls and accessibility at " + width + "px", async ({ page }) => {
    const state = { preview: { source_family: ["ons-website-dataset"], record_type: ["Concept"] }, reductions: [] };
    const url = new URL(readerUrl("records/geospatial-concepts/height-datum.md"));
    url.searchParams.set("explore", JSON.stringify(state));
    await page.setViewportSize({ width, height: width === 1440 ? 1000 : 844 });
    await page.goto(url.href, { waitUntil: "networkidle" });
    if (width < 1100) await page.getByRole("button", { name: "Search & facets", exact: true }).click();
    await expect(page.locator(".facet-section")).toHaveCount(2);
    await expect(page.locator(".exploration-toolbar")).toContainText("0 highlighted / 30,876 in scope");
    await selectedRoute(page, "records/geospatial-concepts/height-datum.md");
    const cards = page.locator(".facet-section");
    for (const facet of await cards.all()) {
      expect(await facet.locator(".facet-values").isVisible()).toBe(false);
      const bounds = await facet.boundingBox();
      expect(bounds!.height).toBeLessThanOrEqual(64);
      expect((await facet.locator(".proportional-bar").boundingBox())!.height).toBe(12);
      const tracks = await facet.locator(".highlight-track").evaluateAll(nodes => nodes.map(node => node.getBoundingClientRect().height));
      expect(tracks.length).toBeGreaterThan(0);
      expect(tracks.every(height => height === 4)).toBe(true);
      const summary = facet.locator(".facet-quick-values > summary");
      const target = await summary.boundingBox();
      expect(target!.width).toBe(36);
      expect(target!.height).toBe(36);
    }
    await expect(page.locator(".facet-instructions .bar-legend")).toBeHidden();
    const documentWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    expect(documentWidth).toBeLessThanOrEqual(width);
    await axe(page);
    for (const key of ["record_type", "source_family"]) {
      const facet = page.locator('.facet-section[data-facet-key="' + key + '"]');
      const palette = facet.locator(".facet-quick-values");
      const summary = palette.locator(":scope > summary");
      await summary.focus();
      await page.keyboard.press("Enter");
      await expect(palette).toHaveAttribute("open", "");
      const popup = await palette.locator(".quick-grid").boundingBox();
      expect(popup!.x).toBeGreaterThanOrEqual(0);
      expect(popup!.x + popup!.width).toBeLessThanOrEqual(width);
      expect((await facet.boundingBox())!.height).toBeLessThanOrEqual(64);
      await axe(page);
      if (key === "record_type") {
        const concept = palette.locator('.quick-value[data-facet-colour="Concept"]');
        for (const selected of [false, true]) {
          await concept.focus();
          await page.keyboard.press("Enter");
          await expect.poll(() => {
            const current = JSON.parse(new URL(page.url()).searchParams.get("explore")!) as typeof state;
            return current.preview.record_type?.[0] === "Concept";
          }).toBe(selected);
        }
      }
      await page.keyboard.press("Escape");
      await expect(palette).not.toHaveAttribute("open", "");
      await expect(summary).toBeFocused();
    }
    expect(JSON.parse(new URL(page.url()).searchParams.get("explore")!)).toEqual(state);
    await selectedRoute(page, "records/geospatial-concepts/height-datum.md");
  });
}

test("legacy links keep their own record state and original catalogue download URLs", async ({ page, request }) => {
  const query = "?view=cards&q=Price%20Paid&type=dataset#record=hmlr%3Adataset%3Aprice-paid-data";
  await page.goto(publicUrl(query), { waitUntil: "networkidle" });
  expect(new URL(page.url()).pathname).toBe(PUBLIC_BASE.pathname + "legacy/");
  expect(new URL(page.url()).searchParams.get("q")).toBe("Price Paid");
  expect(decodeURIComponent(new URL(page.url()).hash)).toBe("#record=hmlr:dataset:price-paid-data");
  await expect(page.getByRole("heading", { level: 2, name: "Price Paid Data", exact: true })).toBeVisible();
  for (const file of ["okf-bundle.json", "okf-bundle.jsonld", "CHECKSUMS.sha256"]) {
    const response = await request.get(publicUrl("catalogue/" + file), { maxRedirects: 0 });
    expect(response.status()).toBe(200);
  }
});
