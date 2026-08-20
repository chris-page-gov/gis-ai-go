import AxeBuilder from "@axe-core/playwright";
import { expect, test as base, type Page } from "@playwright/test";

import {
  encodedPublicationPath,
  verifyPayloadBytes,
  verifyPayloadManifest,
} from "../fixtures/publication";

const PUBLIC_BASE_URL = requireEnvironment("PUBLIC_BASE_URL");
const EXPECTED_SOURCE_COMMIT = requireHex("EXPECTED_SOURCE_COMMIT", 40);
const EXPECTED_ARCHIVE_SHA256 = requireHex("EXPECTED_ARCHIVE_SHA256", 64);
const EXPECTED_OKF_CONTENT_ROOT = requireHex("EXPECTED_OKF_CONTENT_ROOT", 64);
const EXPECTED_PAYLOAD_ROOT = requireHex("EXPECTED_PAYLOAD_ROOT", 64);
const EXPECTED_PUBLIC_CHECKSUMS_SHA256 = requireHex("EXPECTED_PUBLIC_CHECKSUMS_SHA256", 64);
const EXPECTED_VERSION = requireEnvironment("EXPECTED_VERSION");
const EXPECTED_REPOSITORY = "chris-page-gov/gis-ai-go";
const REQUIRED_CSP =
  "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; " +
  "font-src 'self'; connect-src 'self'; media-src 'none'; object-src 'none'; " +
  "frame-src 'none'; worker-src 'none'; manifest-src 'self'; base-uri 'none'; " +
  "form-action 'none'";
const baseUrl = new URL(PUBLIC_BASE_URL);
const expectedCanonicalUrl = new URL(
  process.env.EXPECTED_CANONICAL_URL?.trim() || PUBLIC_BASE_URL,
).href;

function requireEnvironment(name: string): string {
  const value = process.env[name]?.trim();
  if (!value) throw new Error(`${name} is required for public deployment assurance`);
  return value;
}

function requireHex(name: string, length: number): string {
  const value = requireEnvironment(name);
  if (!new RegExp(`^[0-9a-f]{${length}}$`, "u").test(value)) {
    throw new Error(`${name} must be a lower-case ${length}-character hexadecimal value`);
  }
  return value;
}

function publicUrl(relative = ""): string {
  return new URL(relative, baseUrl).href;
}

function isPublicationRequest(requestUrl: string): boolean {
  const candidate = new URL(requestUrl);
  return candidate.origin === baseUrl.origin && candidate.pathname.startsWith(baseUrl.pathname);
}

function asObject(value: unknown, label: string): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${label} must be a JSON object`);
  }
  return value as Record<string, unknown>;
}

function expectIdentity(
  value: unknown,
  schema: string,
  label: string,
): Record<string, unknown> {
  const document = asObject(value, label);
  expect(document.schema).toBe(schema);
  expect(document.repository).toBe(EXPECTED_REPOSITORY);
  expect(document.sourceCommit).toBe(EXPECTED_SOURCE_COMMIT);
  expect(document.version).toBe(EXPECTED_VERSION);
  expect(document.basePath).toBe(baseUrl.pathname);
  expect(document.canonicalUrl).toBe(expectedCanonicalUrl);
  expect(document.okfContentRootSha256).toBe(EXPECTED_OKF_CONTENT_ROOT);
  return document;
}

type PublicAssurance = { publicAssurance: void };
const test = base.extend<PublicAssurance>({
  publicAssurance: [
    async ({ page }, use, testInfo) => {
      const failures: string[] = [];
      const unexpectedRequests: string[] = [];
      page.on("console", (message) => {
        if (message.type() === "error") failures.push(`console: ${message.text()}`);
      });
      page.on("pageerror", (error) => failures.push(`pageerror: ${error.message}`));
      page.on("requestfailed", (request) => {
        failures.push(`requestfailed: ${request.method()} ${request.url()}`);
      });
      page.on("response", (response) => {
        if (response.status() >= 400) failures.push(`response ${response.status()}: ${response.url()}`);
      });
      page.on("request", (request) => {
        if (!isPublicationRequest(request.url())) {
          unexpectedRequests.push(`${request.method()} ${request.url()}`);
        }
      });
      await use();
      if (failures.length || unexpectedRequests.length) {
        await testInfo.attach("public-deployment-errors", {
          body: [...failures, ...unexpectedRequests.map((item) => `unexpected: ${item}`)].join("\n"),
          contentType: "text/plain",
        });
      }
      expect(unexpectedRequests, "the public Explorer must request only its publication path").toEqual([]);
      expect(failures, "the public Explorer console and request lifecycle must stay clean").toEqual([]);
    },
    { auto: true },
  ],
});

test.beforeAll(async ({ request }) => {
  test.setTimeout(120_000);
  await expect
    .poll(
      async () => {
        const response = await request.get(
          publicUrl(`publication/site-receipt.json?source=${EXPECTED_SOURCE_COMMIT}`),
          { headers: { "cache-control": "no-cache" } },
        );
        if (!response.ok()) return { status: response.status() };
        const receipt = asObject(await response.json(), "site receipt");
        return {
          status: response.status(),
          sourceCommit: receipt.sourceCommit,
          version: receipt.version,
          okfContentRootSha256: receipt.okfContentRootSha256,
          payloadRootSha256: receipt.payloadRootSha256,
        };
      },
      { message: "wait for the exact deployed publication", timeout: 110_000 },
    )
    .toEqual({
      status: 200,
      sourceCommit: EXPECTED_SOURCE_COMMIT,
      version: EXPECTED_VERSION,
      okfContentRootSha256: EXPECTED_OKF_CONTENT_ROOT,
      payloadRootSha256: EXPECTED_PAYLOAD_ROOT,
    });
});

test("publishes the exact identity, policy and checksum-bound files", async ({ page, request }) => {
  const response = await page.goto(publicUrl(`?publication=${EXPECTED_SOURCE_COMMIT}`), {
    waitUntil: "networkidle",
  });
  expect(response?.status()).toBe(200);
  await expect(page).toHaveTitle("Catalogue – GIS AI GO");

  const csp = await page.locator('meta[http-equiv="Content-Security-Policy"]').getAttribute("content");
  expect(csp).toBe(REQUIRED_CSP);

  const publication = await page.evaluate(async () => {
    const readJson = async (path: string): Promise<unknown> => {
      const response = await fetch(path, { cache: "no-store" });
      if (!response.ok) throw new Error(`${path} returned ${response.status}`);
      return response.json();
    };
    return Promise.all([
      readJson("./publication/site-receipt.json"),
      readJson("./publication/provenance.json"),
      readJson("./publication/manifest.json"),
    ]);
  });

  const receipt = expectIdentity(publication[0], "gis-ai-go.pages-site-receipt.v1", "site receipt");
  const provenance = asObject(publication[1], "provenance");
  expect(provenance.schema).toBe("gis-ai-go.pages-provenance.v1");
  expect(provenance.repository).toBe(EXPECTED_REPOSITORY);
  expect(provenance.sourceCommit).toBe(EXPECTED_SOURCE_COMMIT);
  expect(provenance.version).toBe(EXPECTED_VERSION);
  expect(provenance.basePath).toBe(baseUrl.pathname);
  expect(provenance.canonicalUrl).toBe(expectedCanonicalUrl);
  expect(asObject(provenance.okf, "provenance.okf").contentRootSha256).toBe(
    EXPECTED_OKF_CONTENT_ROOT,
  );
  const manifest = expectIdentity(publication[2], "gis-ai-go.pages-manifest.v1", "manifest");
  const manifestPayload = asObject(manifest.payload, "manifest.payload");
  expect(receipt.payloadRootSha256).toBe(EXPECTED_PAYLOAD_ROOT);
  expect(manifestPayload.rootSha256).toBe(EXPECTED_PAYLOAD_ROOT);
  const payloadEntries = verifyPayloadManifest(manifestPayload, EXPECTED_PAYLOAD_ROOT);
  for (const entry of payloadEntries) {
    if (entry.path === ".nojekyll") {
      verifyPayloadBytes(entry, new Uint8Array());
      continue;
    }
    const payloadResponse = await request.get(publicUrl(encodedPublicationPath(entry.path)), {
      headers: { "cache-control": "no-cache" },
    });
    expect(payloadResponse.ok(), `${entry.path} must be publicly fetchable`).toBe(true);
    verifyPayloadBytes(entry, new Uint8Array(await payloadResponse.body()));
  }

  const checksumReport = await page.evaluate(async () => {
    const ledgerResponse = await fetch("./publication/CHECKSUMS.sha256", { cache: "no-store" });
    if (!ledgerResponse.ok) throw new Error(`checksum ledger returned ${ledgerResponse.status}`);
    const ledgerBytes = await ledgerResponse.arrayBuffer();
    const ledgerSha256 = [...new Uint8Array(await crypto.subtle.digest("SHA-256", ledgerBytes))]
      .map((value) => value.toString(16).padStart(2, "0"))
      .join("");
    const rows = new TextDecoder().decode(ledgerBytes).trimEnd().split("\n");
    const failures: string[] = [];
    let entries = 0;
    for (const row of rows) {
      const match = /^([0-9a-f]{64}) {2}([^\\\0]+)$/u.exec(row);
      if (!match?.[1] || !match[2] || match[2].startsWith("/") || match[2].split("/").includes("..")) {
        failures.push(`invalid row: ${row}`);
        continue;
      }
      const fileResponse = await fetch(`./${match[2]}`, { cache: "no-store" });
      if (!fileResponse.ok) {
        failures.push(`${match[2]} returned ${fileResponse.status}`);
        continue;
      }
      const digest = [...new Uint8Array(await crypto.subtle.digest("SHA-256", await fileResponse.arrayBuffer()))]
        .map((value) => value.toString(16).padStart(2, "0"))
        .join("");
      if (digest !== match[1]) failures.push(`${match[2]} checksum mismatch`);
      entries += 1;
    }
    return { entries, failures, ledgerSha256 };
  });
  expect(checksumReport.entries).toBeGreaterThan(0);
  expect(checksumReport.failures).toEqual([]);
  expect(checksumReport.ledgerSha256).toBe(EXPECTED_PUBLIC_CHECKSUMS_SHA256);
  expect(EXPECTED_ARCHIVE_SHA256).toMatch(/^[0-9a-f]{64}$/u);
});

async function search(page: Page, query: string): Promise<void> {
  await page.goto(publicUrl("?view=cards"));
  const box = page.getByRole("searchbox", { name: /Search(?: the public)? catalogue/i });
  await box.fill(query);
  await page.getByRole("button", { name: /^Search$/i }).click();
}

test("answers the legal-boundary question and exposes reviewed examples", async ({ page }) => {
  await page.goto(publicUrl());
  await expect(
    page.getByRole("heading", { level: 1, name: "INSPIRE polygon: indicative or legal boundary?" }),
  ).toBeVisible();
  await expect(
    page
      .getByText(
        "Polygons are indicative and do not establish the exact legal extent of a title.",
        { exact: true },
      )
      .first(),
  ).toBeVisible();

  for (const [query, recordId, marker] of [
    ["Price Paid", "hmlr:dataset:price-paid-data", "Price Paid Data"],
    ["PV-ONS-DATA", "PV-ONS-DATA", "ONS Data API"],
    ["PV-ONS-GEO", "PV-ONS-GEO", "ONS Geography and Open Geography Portal"],
    ["PV-LANDIS", "PV-LANDIS", "LandIS"],
  ] as const) {
    await search(page, query);
    const link = page.locator(
      `article.record-card a[href*="#record=${encodeURIComponent(recordId)}"]`,
    );
    await expect(link).toHaveCount(1);
    await expect(link).toContainText(marker);
  }
});

test("preserves direct state, browser history and projection parity", async ({ page }) => {
  const recordId = "hmlr:dataset:price-paid-data";
  await page.goto(
    publicUrl(`?view=cards&q=Price%20Paid&type=dataset#record=${encodeURIComponent(recordId)}`),
  );
  await expect(page.getByRole("heading", { level: 2, name: "Price Paid Data" })).toBeVisible();
  await page.getByRole("link", { name: "Back to catalogue", exact: true }).click();
  await expect(page.getByRole("link", { name: "Price Paid Data", exact: true })).toBeVisible();
  await page.goBack();
  await expect(page.getByRole("heading", { level: 2, name: "Price Paid Data" })).toBeVisible();
  await page.goForward();
  await expect(page.getByRole("link", { name: "Price Paid Data", exact: true })).toBeVisible();

  const identifiers = await page.evaluate(async () => {
    const [jsonResponse, jsonLdResponse] = await Promise.all([
      fetch("./catalogue/okf-bundle.json"),
      fetch("./catalogue/okf-bundle.jsonld"),
    ]);
    if (!jsonResponse.ok || !jsonLdResponse.ok) {
      throw new Error(`projection response ${jsonResponse.status}/${jsonLdResponse.status}`);
    }
    const json = (await jsonResponse.json()) as { records: Array<{ id: string }> };
    const jsonLd = (await jsonLdResponse.json()) as { "@graph": Array<{ identifier: string }> };
    return {
      json: json.records.map((record) => record.id).sort(),
      jsonLd: jsonLd["@graph"].map((record) => record.identifier).sort(),
    };
  });
  expect(identifiers.json.length).toBe(36);
  expect(identifiers.jsonLd).toEqual(identifiers.json);
});

test("passes public keyboard, WCAG and 320-pixel reflow acceptance", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 800 });
  await page.goto(publicUrl("?view=cards"));
  await page.keyboard.press("Tab");
  const skipLink = page.getByRole("link", { name: "Skip to main content" });
  await expect(skipLink).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.locator("#main-content")).toBeFocused();

  const violations = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22a", "wcag22aa"])
    .analyze();
  expect(violations.violations, JSON.stringify(violations.violations, null, 2)).toEqual([]);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    ),
  ).toBeLessThanOrEqual(1);
});

export { expect, test };
