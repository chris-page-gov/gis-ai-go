import type { Page } from "@playwright/test";

import { expect, test } from "../fixtures/assurance";

async function searchAndOpen(
  page: Page,
  query: string,
  marker: string,
  exactRecordId?: string,
): Promise<void> {
  await page.goto("/?view=cards");
  const search = page.getByRole("searchbox", { name: /Search(?: the public)? catalogue/i });
  await search.fill(query);
  await page.getByRole("button", { name: /^Search$/i }).click();

  if (exactRecordId === undefined) {
    const card = page.locator("article.record-card").filter({ hasText: marker });
    await expect(card).toHaveCount(1);
    await card.getByRole("link").first().click();
  } else {
    const recordLink = page.locator(
      `article.record-card a[href*="#record=${encodeURIComponent(exactRecordId)}"]`,
    );
    await expect(recordLink).toHaveCount(1);
    await recordLink.click();
  }
  await expect(page.locator("article.record-detail")).toBeVisible();
}

async function expectPublisherEvidence(page: Page, urls: readonly string[]): Promise<void> {
  const detail = page.locator("article.record-detail");
  const sourceSection = detail
    .getByRole("heading", { level: 3, name: "Source evidence" })
    .locator("..");
  for (const url of urls) {
    await expect(sourceSection.locator(`a[href="${url}"]`)).toHaveCount(1);
  }
}

async function catalogueText(page: Page): Promise<string> {
  return page.evaluate(async () => {
    const response = await fetch("./catalogue/okf-bundle.json");
    if (!response.ok) {
      throw new Error(`catalogue returned ${response.status}`);
    }
    return response.text();
  });
}

test("LR-Q003 distinguishes an online copy from an official copy", async ({ page }) => {
  await searchAndOpen(page, "online copy or official copy proof of ownership", "LR-Q003");

  const detail = page.locator("article.record-detail");
  await expect(detail.getByRole("heading", { level: 2 })).toContainText("LR-Q003");
  await expect(detail).toContainText("An online copy is not proof of ownership.");
  await expect(detail).toContainText(
    "Official copies have a distinct order route and evidential role.",
  );
  await expect(detail).toContainText("non-executing", { ignoreCase: true });
  await expectPublisherEvidence(page, [
    "https://www.gov.uk/search-property-information-land-registry",
    "https://www.gov.uk/guidance/land-registry-portal-how-to-request-official-copies",
  ]);

  expect(await catalogueText(page)).not.toContain(
    "https://businessgateway.landregistry.gov.uk/bg2/s1/v1",
  );
});

test("LR-Q006 gives the documented index-map recovery route", async ({ page }) => {
  await searchAndOpen(
    page,
    "address search misses title search of the index map",
    "LR-Q006",
  );

  const detail = page.locator("article.record-detail");
  await expect(detail).toContainText(
    "Searching only by property details may not show every title affecting the property.",
  );
  await expect(detail).toContainText(
    "A search of the index map is the documented alternative for the relevant task.",
  );
  await expectPublisherEvidence(page, [
    "https://www.gov.uk/guidance/land-registry-portal-how-to-request-official-copies",
    "https://www.gov.uk/guidance/land-registry-portal-request-a-search-of-the-index-map",
    "https://www.gov.uk/search-property-information-land-registry",
  ]);

  const bundle = await catalogueText(page);
  expect(bundle).not.toContain("https://github.com/LandRegistry/address-search-api");
  expect(bundle).not.toContain("https://businessgateway.landregistry.gov.uk/bg2/s1/v1");
});

test("LR-Q012 keeps INSPIRE geometry indicative and links LLC evidence", async ({ page }) => {
  await searchAndOpen(page, "INSPIRE polygon indicative or legal boundary", "LR-Q012");

  const detail = page.locator("article.record-detail");
  await expect(detail).toContainText(
    "Local Land Charges INSPIRE data shows indicative locations.",
  );
  await expect(detail).toContainText(
    "Indicative geometry is a discovery aid and does not establish an exact legal title boundary.",
  );
  await expectPublisherEvidence(page, [
    "https://use-land-property-data.service.gov.uk/datasets/llc",
    "https://www.gov.uk/government/publications/hm-land-registry-plans-boundaries-pg40s3",
  ]);

  expect(await catalogueText(page)).not.toContain(
    "https://use-land-property-data.service.gov.uk/datasets/nps",
  );
});

test("Price Paid shows source date and third-party conditions without publishing rows", async ({
  page,
}) => {
  await searchAndOpen(
    page,
    "Price Paid",
    "Price Paid Data",
    "hmlr:dataset:price-paid-data",
  );

  const detail = page.locator("article.record-detail");
  await expect(detail).toContainText("Open Government Licence v3.0");
  await expect(detail).toContainText("HM Land Registry");
  await expect(detail).toContainText("Ordnance Survey");
  await expect(detail).toContainText("Royal Mail");
  await expect(detail.getByText("28 July 2026", { exact: true })).toBeVisible();

  const selected = await page.evaluate(async () => {
    const response = await fetch("./catalogue/okf-bundle.json");
    const bundle = (await response.json()) as {
      records: Array<{ id: string; details: Record<string, unknown> }>;
    };
    return bundle.records.find((record) => record.id === "hmlr:dataset:price-paid-data");
  });
  expect(selected).toBeDefined();
  expect(selected?.details.publisherLastUpdated).toBe("2026-07-28");
  const forbiddenKeys = new Set([
    "address",
    "addresses",
    "row",
    "rows",
    "transaction",
    "transactions",
  ]);
  expect(Object.keys(selected?.details ?? {}).filter((key) => forbiddenKeys.has(key))).toEqual([]);
});

test("both ONS records expose bounded capabilities without executing a provider", async ({
  page,
}) => {
  await searchAndOpen(page, "PV-ONS-DATA", "ONS Data API");
  let detail = page.locator("article.record-detail");
  for (const capability of [
    "datasets",
    "versions",
    "editions",
    "dimensions",
    "observations",
  ] as const) {
    await expect(detail).toContainText(capability);
  }
  await expect(detail).toContainText("No provider connection is made");

  await searchAndOpen(page, "PV-ONS-GEO", "ONS Geography and Open Geography Portal");
  detail = page.locator("article.record-detail");
  for (const capability of [
    "boundaries",
    "lookups",
    "names and codes",
    "change history",
  ] as const) {
    await expect(detail).toContainText(capability);
  }
  await expect(detail).toContainText("No provider connection is made");
});

test("LandIS remains visibly mixed, per-record and non-executing", async ({ page }) => {
  await searchAndOpen(page, "PV-LANDIS", "LandIS");

  const detail = page.locator("article.record-detail");
  await expect(detail).toContainText("commercial or restricted where record terms require", {
    ignoreCase: true,
  });
  await expect(detail).toContainText("Read and enforce each record licence");
  await expect(detail).toContainText("do not infer one blanket licence", { ignoreCase: true });
  await expect(detail).toContainText("No provider connection is made");
  await expect(detail).toContainText("No live provider call");
});

test("timeline keeps the verified HMLR upstream release date distinct", async ({ page }) => {
  await page.goto("/?view=timeline&q=Digest-locked%20okf-LandRegistry");

  const releaseEvent = page
    .locator(".timeline-list .timeline-event-type", { hasText: /^Release$/ })
    .locator("..")
    .filter({ hasText: "Digest-locked okf-LandRegistry v0.3.0 release" });
  await expect(releaseEvent).toHaveCount(1);
  const releaseTime = releaseEvent.locator("time");
  await expect(releaseTime).toHaveAttribute("datetime", "2026-08-12T01:43:30+01:00");
  await expect(releaseTime).toContainText("12 August 2026");
});
