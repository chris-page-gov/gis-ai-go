import { createHash } from "node:crypto";
import AxeBuilder from "@axe-core/playwright";
import { expect, test as base, type Page } from "@playwright/test";

const PUBLIC_BASE = new URL(required("PUBLIC_BASE_URL"));
const SOURCE = required("EXPECTED_SOURCE_COMMIT");
const CANONICAL = new URL("https://chris-page-gov.github.io/gis-ai-go/");
const DESCRIPTOR = new URL("gis/explorer/okf-explorer.json", CANONICAL).href;
const LOCAL = PUBLIC_BASE.hostname === "127.0.0.1" || PUBLIC_BASE.hostname === "localhost";
// The accepted pre-discovery v2 archive remains a valid rollback target. Its
// exact source identity selects its historical contract; no other source may
// fall back when discovery metadata is missing.
const HISTORICAL_PUBLIC_SOURCE = "8e67ae88e68341120a712d102f692894fbd89659";
const CURRENT_APP_TREE = "827ac61a364500a2c73ad949dfda36f0839e54056644edd414ddb34f96aee960";
const CURRENT_APP_MANIFEST = "bbb482b252b9385149ab06a0bb5cbaae778e65a9498ea5c06d3683f4aa297d7a";
const APP_TREE = SOURCE === HISTORICAL_PUBLIC_SOURCE
  ? "d127aadb96a77711d5f7cc7aec8cf731cbf5ec1e3d49304d8132189ea4991f93" : CURRENT_APP_TREE;
const APP_MANIFEST = SOURCE === HISTORICAL_PUBLIC_SOURCE
  ? "ab227164e2e114148425a453a0e04b6bb21230f79be1e059a3ff6936d57f45f2" : CURRENT_APP_MANIFEST;
const DISCOVERY_FACET_KEYS = [
  "record_type", "source_family", "tag", "source_publisher", "review_status", "assertion_status",
  "lifecycle_status", "temporal_status", "temporal_kind", "update_frequency", "update_frequency_status",
  "release_version", "retrieval_authority", "source_evidence_kind", "unit", "spatial_reference", "crs", "storage_crs",
];
type Step = { title: string; route: string };
type LearningPath = { id: string; title: string; steps: Step[] };
type ProjectionReference = string | { path: string; bytes?: number; sha256?: string };
type FacetPostings = Record<string, Record<string, number[]>>;
type ProjectionManifest = {
  counts: { records: number; resources: number; publishers: number; relationships: number };
  indexes: { record_locator: ProjectionReference; record_resources?: ProjectionReference };
  chunks: { datasets: ProjectionReference[]; relationships: ProjectionReference[]; resources: ProjectionReference[]; publishers: ProjectionReference[] };
};
type ProjectedRecord = {
  id: string; name: string; route: string; title: string;
  okf_plus: { metadata: Record<string, unknown> & { "@id": string; tags: string[]; reviewStatus: string; "skos:related"?: { "@id": string }[] } };
};
type ProjectedRelationship = {
  id: string; source: string; target: string; source_iri: string; target_iri: string;
  predicate: string; assertion_status: string; assertion_scope: string; authority: { class: string }; evidence: unknown[];
};
type ProjectedSourceReference = {
  id: string; name: string; dataset: string; route: string; url: string;
  resource_type: string; downloadability: string; execution_admitted: boolean;
  download_url?: string; provenance: { record_route: string };
  source_access: { url: string; label: string; display_mode: string };
};
type Descriptor = {
  schema: string;
  snapshot: string;
  source: { revision: string; inputDigest: string };
  counts: { records: number; resources: number; publishers: number; relationships: number };
  entrypoints: Record<string, ProjectionReference>;
  vocabulary: Record<string, string>;
  extensions: { gis_ai_go: { discoveryCoverage?: ProjectionReference } };
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
async function projectionJson<T>(page: Page, reference: ProjectionReference): Promise<T> {
  const path = typeof reference === "string" ? reference : reference.path;
  const response = await page.request.get(publicUrl("gis/explorer/" + path), { maxRedirects: 0 });
  expect(response.status(), "the exact advertised projection resource must exist: " + path).toBe(200);
  const bytes = await response.body();
  if (typeof reference !== "string") {
    if (reference.bytes !== undefined) expect(bytes.byteLength).toBe(reference.bytes);
    if (reference.sha256 !== undefined) expect(createHash("sha256").update(bytes).digest("hex")).toBe(reference.sha256);
  }
  return JSON.parse(bytes.toString()) as T;
}
function routeBucket(route: string): string {
  let hash = 0x811c9dc5;
  for (const character of route) hash = Math.imul(hash ^ character.charCodeAt(0), 0x01000193) >>> 0;
  return (hash >>> 24).toString(16).padStart(2, "0");
}
async function projectionRecord(page: Page, manifest: ProjectionManifest, routeOrOrdinal: string | number): Promise<ProjectedRecord> {
  const locator = await projectionJson<{
    chunk_size: number; record_chunks: ProjectionReference[]; buckets: Record<string, ProjectionReference>;
  }>(page, manifest.indexes.record_locator);
  let chunkIndex: number;
  let rowIndex: number;
  if (typeof routeOrOrdinal === "number") {
    chunkIndex = Math.floor(routeOrOrdinal / locator.chunk_size);
    rowIndex = routeOrOrdinal % locator.chunk_size;
  } else {
    const bucket = await projectionJson<Record<string, [number, number]>>(page, locator.buckets[routeBucket(routeOrOrdinal)]!);
    expect(bucket[routeOrOrdinal], "the source record must have a bounded record locator").toBeTruthy();
    [chunkIndex, rowIndex] = bucket[routeOrOrdinal]!;
  }
  const records = await projectionJson<ProjectedRecord[]>(page, locator.record_chunks[chunkIndex]!);
  const value = records[rowIndex]!;
  if (typeof routeOrOrdinal === "string") expect(value.route).toBe(routeOrOrdinal);
  return value;
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
    const fieldOption = fields.getByRole("option", { name: sample.field, exact: true });
    await expect(fieldOption).toHaveCount(1);
    const fieldValue = await fieldOption.getAttribute("value");
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

test("retained metadata is exposed as exact facets, source references and governed concept relationships", async ({ page, transport }, info) => {
  test.setTimeout(180_000);
  const value = await descriptor(page);
  const manifest = await projectionJson<ProjectionManifest>(page, value.entrypoints.data_manifest!);
  const search = await projectionJson<{ entrypoints: { facets: ProjectionReference } }>(page, value.entrypoints.search_manifest!);
  const postings = await projectionJson<FacetPostings>(page, search.entrypoints.facets);
  if (SOURCE === HISTORICAL_PUBLIC_SOURCE) {
    expect(Object.keys(postings).sort()).toEqual(["record_type", "source_family"]);
    expect(value.counts).toMatchObject({ records: 30_876, resources: 0, publishers: 0, relationships: 0 });
    expect(manifest.counts).toMatchObject(value.counts);
    expect(value.extensions.gis_ai_go.discoveryCoverage).toBeUndefined();
    await page.goto(readerUrl(), { waitUntil: "networkidle" });
    await page.getByLabel("Facet visibility", { exact: true }).getByRole("button", { name: "All", exact: true }).click();
    await expect(page.locator(".facet-section")).toHaveCount(2);
    await expect(page.locator('[data-metric="resources"] strong')).toHaveText("0");
    await expect(page.locator('[data-metric="relationships"] strong')).toHaveText("0");
    await info.attach("discovery-acceptance-contract", {
      body: JSON.stringify({ profile: "accepted-pre-discovery-v2", sourceCommit: SOURCE, facets: 2, relationships: 0 }),
      contentType: "application/json",
    });
    return;
  }
  expect(value.extensions.gis_ai_go.discoveryCoverage, "every new source requires the complete discovery coverage contract").toBeTruthy();
  const coverage = await projectionJson<{
    schema: string;
    facets: Record<string, { nonemptyRecords: number; distinctValues: number; memberships: number }>;
  }>(page, value.extensions.gis_ai_go.discoveryCoverage!);
  expect(coverage.schema).toBe("gis-ai-go.okf-plus-explorer-discovery-coverage.v1");
  expect(Object.keys(postings).sort()).toEqual([...DISCOVERY_FACET_KEYS].sort());
  expect(Object.keys(coverage.facets).sort()).toEqual([...DISCOVERY_FACET_KEYS].sort());
  for (const key of DISCOVERY_FACET_KEYS) {
    expect(postings[key], "a retained metadata dimension must be indexed: " + key).toBeTruthy();
    const values = Object.values(postings[key]!);
    expect(coverage.facets[key]!.distinctValues).toBe(values.length);
    expect(coverage.facets[key]!.memberships).toBe(values.reduce((sum, members) => sum + members.length, 0));
    expect(coverage.facets[key]!.nonemptyRecords).toBe(new Set(values.flat()).size);
  }
  expect(value.counts).toMatchObject(manifest.counts);
  expect(value.counts.relationships).toBe(137);
  expect(value.counts.resources).toBeGreaterThanOrEqual(value.counts.records);
  expect(value.counts.publishers).toBeGreaterThan(0);
  expect(value.vocabulary.resource_plural).toBe("source references");
  await info.attach("discovery-acceptance-contract", {
    body: JSON.stringify({
      profile: "full-discovery-v1", sourceCommit: SOURCE, facets: DISCOVERY_FACET_KEYS.length,
      relationships: value.counts.relationships, sourceReferences: value.counts.resources, publishers: value.counts.publishers,
    }),
    contentType: "application/json",
  });

  const access = await projectionRecord(page, manifest, "records/geospatial-concepts/access-rights.md");
  const metadata = access.okf_plus.metadata;
  expect(metadata.tags).toContain("rights");
  expect(metadata["skos:related"]).toHaveLength(2);
  const frequency = Object.keys(postings.update_frequency!).find(item => item.trim());
  expect(frequency).toBeTruthy();
  const dated = await projectionRecord(page, manifest, postings.update_frequency![frequency!]![0]!);
  const update = dated.okf_plus.metadata.update as { frequency: { label: string } };
  expect(update.frequency.label.trim()).toBe(frequency);
  const examples = [
    { key: "tag", value: "rights" },
    { key: "review_status", value: metadata.reviewStatus },
    { key: "update_frequency", value: frequency! },
  ];
  for (const example of examples) {
    await page.goto(readerUrl(), { waitUntil: "networkidle" });
    await page.getByLabel("Facet visibility", { exact: true }).getByRole("button", { name: "All", exact: true }).click();
    await expect(page.locator(".facet-section")).toHaveCount(Object.keys(postings).length);
    const facet = page.locator('.facet-section[data-facet-key="' + example.key + '"]');
    await facet.locator(".facet-toggle").click();
    const findValue = facet.locator(".facet-values input");
    if (await findValue.count()) await findValue.fill(example.value);
    const member = facet.locator(".facet-value[data-facet-value=" + JSON.stringify(example.value) + "]");
    await expect(member).toHaveCount(1);
    await expect(member.locator("small")).toHaveText(new RegExp("/ " + postings[example.key]![example.value]!.length.toLocaleString("en-GB") + "$"));
    await member.click();
    await expect.poll(() => {
      const state = JSON.parse(new URL(page.url()).searchParams.get("explore") || "{}") as { preview?: Record<string, string[]> };
      return state.preview?.[example.key];
    }).toEqual([example.value]);
    await expect(page.locator(".exploration-toolbar")).toContainText(
      postings[example.key]![example.value]!.length.toLocaleString("en-GB") + " highlighted / 30,876 in scope",
    );
  }
  // This retained route is outside the connected concept graph. Its authored
  // title must remain available through the record locator as well.
  const datedRecordStart = transport.requests.length;
  await page.goto(readerUrl(dated.route), { waitUntil: "networkidle" });
  await expect(page.locator(".right-panel").getByRole("heading", { name: dated.title, exact: true })).toBeVisible();
  expect(shards(transport.requests.slice(datedRecordStart))).toHaveLength(1);

  const firstReferences = await projectionJson<ProjectedSourceReference[]>(page, manifest.chunks.resources[0]!);
  expect(firstReferences.length).toBeGreaterThan(0);
  const sourceReference = firstReferences[0]!;
  expect(sourceReference.resource_type).toBe("source-reference");
  expect(sourceReference.downloadability).toBe("not-established");
  expect(sourceReference.execution_admitted).toBe(false);
  expect(sourceReference.download_url).toBeUndefined();
  const citedRecord = await projectionRecord(page, manifest, sourceReference.provenance.record_route);
  const citedMetadata = citedRecord.okf_plus.metadata;
  const sources = citedMetadata.sources as { resource: string }[];
  expect([citedMetadata.resource, ...sources.map(item => item.resource)]).toContain(sourceReference.url);
  const publishers = await projectionJson<{ name: string; provenance: { source_property: string } }[]>(page, manifest.chunks.publishers[0]!);
  expect(publishers.length).toBeGreaterThan(0);
  expect(publishers[0]!.name).toMatch(/^https?:\/\//u);
  expect(publishers[0]!.provenance.source_property).toBe("dcterms:publisher");

  expect(value.entrypoints.record_resources, "every new source must advertise bounded record references").toBeTruthy();
  expect(manifest.indexes.record_resources).toEqual(value.entrypoints.record_resources);
  const resourceIndex = await projectionJson<{
    schema: string; snapshot: string; algorithm: string; buckets: Record<string, ProjectionReference>;
  }>(page, value.entrypoints.record_resources!);
  expect(resourceIndex.schema).toBe("okf-record-resource-index.v1");
  expect(resourceIndex.snapshot).toBe(value.snapshot);
  expect(resourceIndex.algorithm).toBe("fnv1a32-prefix-2");
  const resourceBucketReference = resourceIndex.buckets[routeBucket(access.route)]!;
  expect(resourceBucketReference).toBeTruthy();
  const resourceBucket = await projectionJson<Record<string, {
    dataset: string; count: number; chunks: (ProjectionReference & { rows: number[] })[];
  }>>(page, resourceBucketReference);
  const selectedReferences = resourceBucket[access.route]!;
  expect(selectedReferences.dataset).toBe(access.name);
  expect(selectedReferences.count).toBeGreaterThan(0);
  expect(selectedReferences.count).toBeLessThanOrEqual(256);
  expect(selectedReferences.chunks.length).toBeLessThanOrEqual(16);
  const selectedSources: ProjectedSourceReference[] = [];
  for (const reference of selectedReferences.chunks) {
    const rows = await projectionJson<ProjectedSourceReference[]>(page, reference);
    expect(rows.length).toBeLessThanOrEqual(1024);
    expect(new Set(reference.rows).size).toBe(reference.rows.length);
    for (const index of reference.rows) {
      expect(Number.isSafeInteger(index) && index >= 0 && index < rows.length).toBe(true);
      const row = rows[index]!;
      expect(row.dataset).toBe(access.name);
      expect(row.provenance.record_route).toBe(access.route);
      expect(row.source_access).toMatchObject({ url: row.url, label: "Retained source reference", display_mode: "link" });
      selectedSources.push(row);
    }
  }
  expect(selectedSources).toHaveLength(selectedReferences.count);
  const sourceRequestStart = transport.requests.length;
  // Retain the same document: URL/history navigation from the dated record
  // must hydrate this newly selected Reader context, including its references.
  await page.goto(readerUrl(access.route), { waitUntil: "networkidle" });
  const sourceLinks = page.locator(".right-panel .detail-actions").getByRole("link", {
    name: "Open Retained source reference ↗", exact: true,
  });
  await expect(sourceLinks).toHaveCount(selectedSources.length);
  expect((await sourceLinks.evaluateAll(nodes => nodes.map(node => (node as HTMLAnchorElement).href))).sort())
    .toEqual(selectedSources.map(row => row.url).sort());
  await expect(page.getByRole("button", { name: "View source data", exact: true })).toHaveCount(0);
  await expect(page.getByRole("link", { name: "Open official source ↗", exact: true })).toHaveCount(0);
  await page.getByLabel("Views", { exact: true }).getByRole("button", { name: "Resources", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Source references", exact: true })).toBeVisible();
  await expect(page.getByText(selectedSources.length + " source references shown from current reduction", { exact: true })).toBeVisible();
  const sourceStack = page.locator(".resource-stack-view");
  await expect(sourceStack.locator(":scope > article")).toHaveCount(1);
  await expect(sourceStack.locator(".stack-heading strong")).toHaveText(access.title);
  await expect(sourceStack.locator(".resource-stack > button strong"))
    .toHaveText(selectedSources.slice(0, 12).map(row => row.name));
  await sourceStack.locator(".resource-stack > button").first().click();
  await expect(page.locator(".right-panel").getByRole("heading", { name: selectedSources[0]!.name, exact: true })).toBeVisible();
  const sourceUiRequests = transport.requests.slice(sourceRequestStart);
  const projectionPath = (reference: ProjectionReference): string =>
    new URL(typeof reference === "string" ? reference : reference.path, DESCRIPTOR).pathname;
  const sourceChunkRequests = sourceUiRequests.filter(url => /\/gis\/explorer\/resources\/\d+\.json(?:\?|$)/u.test(url));
  expect(sourceChunkRequests.map(url => new URL(url).pathname).sort())
    .toEqual(selectedReferences.chunks.map(projectionPath).sort());
  // The dated record and this record share the one manifest cache. Switching
  // to Resources must reuse both the selected chunk and that manifest.
  const referenceNavigationRequests = transport.requests.slice(datedRecordStart);
  for (const reference of [value.entrypoints.record_resources!, resourceBucketReference]) {
    expect(referenceNavigationRequests.filter(url => new URL(url).pathname === projectionPath(reference))).toHaveLength(1);
  }
  expect(shards(sourceUiRequests), "Reader and selected source references may load only their one record shard").toHaveLength(1);
  for (const row of selectedSources) expect(sourceUiRequests).not.toContain(row.url);
  await info.attach("selected-source-reference-transport", {
    body: JSON.stringify({ route: access.route, references: selectedSources.length, requests: sourceUiRequests }, null, 2),
    contentType: "application/json",
  });

  const relationships = (await Promise.all(manifest.chunks.relationships.map(reference =>
    projectionJson<ProjectedRelationship[]>(page, reference)))).flat();
  const related = relationships.filter(row => row.predicate === "http://www.w3.org/2004/02/skos/core#related");
  expect(related).toHaveLength(137);
  expect(new Set(related.map(row => row.id)).size).toBe(137);
  const outgoing = related.filter(row => row.source_iri === metadata["@id"]);
  expect(outgoing.map(row => row.target_iri).sort()).toEqual(metadata["skos:related"]!.map(row => row["@id"]).sort());
  for (const relationship of outgoing) {
    expect(relationship.source).toBe(access.route);
    expect(relationship.authority.class).toBe("derived");
    expect(relationship.assertion_status).toBe("normalized");
    expect(relationship.assertion_scope).toBe("real-world");
    expect(relationship.evidence.length).toBeGreaterThan(0);
  }

  const graphRequestStart = transport.requests.length;
  await page.goto(readerUrl(access.route), { waitUntil: "networkidle" });
  await expect(page.locator('[data-metric="source-references"] strong')).toHaveText(value.counts.resources.toLocaleString("en-GB"));
  await expect(page.locator('[data-metric="relationships"] strong')).toHaveText("137");
  await page.getByRole("button", { name: "Links", exact: true }).click();
  const first = outgoing[0]!;
  const target = await projectionRecord(page, manifest, first.target);
  const exactText = (text: string) => new RegExp("^" + text.replace(/[.*+?^${}()|[\]\\]/gu, "\\$&") + "$");
  const row = page.locator(".links-view > button").filter({
    has: page.locator("strong:first-child").filter({ hasText: exactText(access.title) }),
  }).filter({
    has: page.locator("strong:last-child").filter({ hasText: exactText(target.title) }),
  });
  await expect(row).toHaveCount(1);
  await expect(row).toHaveAttribute("data-relationship-authority", "derived");
  await expect(row).toHaveAttribute("data-relationship-status", "normalized");
  await expect(row).toHaveAttribute("data-relationship-scope", "real-world");
  await row.click();
  await page.getByRole("tablist", { name: "Relationship data card", exact: true }).getByRole("tab", { name: "Relationship", exact: true }).click();
  const relationshipCard = page.locator(".relationship-detail-content");
  await expect(relationshipCard).toContainText(first.predicate);
  await expect(relationshipCard).toContainText(metadata["@id"]);
  await expect(relationshipCard).toContainText(first.target_iri);
  await expect(relationshipCard.getByRole("heading", { name: "Relationship evidence and provenance", exact: true })).toBeVisible();
  await relationshipCard.getByText("Relationship JSON", { exact: true }).click();
  const inspected = JSON.parse(await relationshipCard.locator(".json-panel pre").innerText()) as Omit<ProjectedRelationship, "authority"> & { authority: string };
  expect(inspected.id).toBe(first.id);
  expect(inspected.predicate).toBe(first.predicate);
  expect(inspected.source_iri).toBe(metadata["@id"]);
  expect(inspected.target_iri).toBe(first.target_iri);
  expect(inspected.authority).toBe("derived");
  expect(inspected.assertion_scope).toBe("real-world");
  expect(inspected.evidence.length).toBeGreaterThan(0);
  await page.getByRole("button", { name: "Graph", exact: true }).first().click();
  await expect(page.locator('.graph-node[data-route="' + access.route + '"]')).toBeVisible();
  for (const relationship of outgoing) {
    await expect(page.locator('.graph-node[data-route="' + relationship.target + '"]')).toBeVisible();
  }
  expect(shards(transport.requests.slice(graphRequestStart)).length, "selected concept links must not hydrate the full record corpus").toBeLessThanOrEqual(3);
});

for (const width of [1440, 390, 320]) {
  test("compact facets preserve exact state, palette keyboard controls and accessibility at " + width + "px", async ({ page }) => {
    const state = { preview: { source_family: ["ons-website-dataset"], record_type: ["Concept"] }, reductions: [] };
    const url = new URL(readerUrl("records/geospatial-concepts/height-datum.md"));
    url.searchParams.set("explore", JSON.stringify(state));
    await page.setViewportSize({ width, height: width === 1440 ? 1000 : 844 });
    await page.goto(url.href, { waitUntil: "networkidle" });
    if (width < 1100) await page.getByRole("button", { name: "Search & facets", exact: true }).click();
    const expectedFacetKeys = SOURCE === HISTORICAL_PUBLIC_SOURCE
      ? ["record_type", "source_family"]
      : ["record_type", "source_family", "tag", "review_status"];
    await expect(page.locator(".facet-section")).toHaveCount(expectedFacetKeys.length);
    for (const key of expectedFacetKeys) {
      await expect(page.locator('.facet-section[data-facet-key="' + key + '"]')).toBeVisible();
    }
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
