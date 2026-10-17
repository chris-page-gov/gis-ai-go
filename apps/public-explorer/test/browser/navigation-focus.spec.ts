import { expect, test } from "../fixtures/assurance";

const destinations = [
  ["Catalogue", "Catalogue"],
  ["Graph", "Evidence graph"],
  ["Timeline", "Catalogue timeline"],
  ["Map", "Coverage schematic — not a property map"],
  ["About", "About this Explorer"],
] as const;

for (const [label, heading] of destinations) {
  test(`keyboard navigation moves focus to the ${label} heading`, async ({ page }) => {
    await page.goto("/?view=cards");
    const destination = page.getByRole("navigation", { name: "Explore catalogue" })
      .getByRole("link", { name: label, exact: true });
    await destination.focus();
    await page.keyboard.press("Enter");
    await expect(page.getByRole("heading", { name: heading, exact: true })).toBeFocused();
  });
}

test("record navigation and browser history restore focus to the displayed heading", async ({ page }) => {
  await page.goto("/?view=cards&q=Price%20Paid&type=dataset");
  const record = page.getByRole("link", { name: "Price Paid Data", exact: true });
  await record.focus();
  await page.keyboard.press("Enter");
  const recordHeading = page.getByRole("heading", { level: 2, name: "Price Paid Data" });
  await expect(recordHeading).toBeFocused();

  await page.getByRole("link", { name: "Back to catalogue", exact: true }).press("Enter");
  const catalogueHeading = page.getByRole("heading", { level: 2, name: "Catalogue", exact: true });
  await expect(catalogueHeading).toBeFocused();
  await page.goBack();
  await expect(recordHeading).toBeFocused();
  await page.goForward();
  await expect(catalogueHeading).toBeFocused();
});

test("history restores focus between a view and About", async ({ page }) => {
  await page.goto("/?view=cards");
  const navigation = page.getByRole("navigation", { name: "Explore catalogue" });
  await navigation.getByRole("link", { name: "Graph", exact: true }).press("Enter");
  await expect(page.getByRole("heading", { name: "Evidence graph", exact: true })).toBeFocused();
  await navigation.getByRole("link", { name: "About", exact: true }).press("Enter");
  await expect(page.getByRole("heading", { name: "About this Explorer", exact: true })).toBeFocused();
  await page.goBack();
  await expect(page.getByRole("heading", { name: "Evidence graph", exact: true })).toBeFocused();
  await page.goForward();
  await expect(page.getByRole("heading", { name: "About this Explorer", exact: true })).toBeFocused();
});

for (const hash of ["record=missing-record", "record=", "record=one&record=two"]) {
  test(`record hash ${hash} focuses its error heading`, async ({ page }) => {
    await page.goto("/?view=cards");
    await expect(page.getByRole("heading", { level: 2, name: "Catalogue", exact: true })).toBeVisible();
    await page.evaluate((value) => { window.location.hash = value; }, hash);
    await expect(page.getByRole("heading", { name: "Record not found", exact: true })).toBeFocused();
    await page.getByRole("link", { name: "Back to catalogue", exact: true }).press("Enter");
    await expect(page.getByRole("heading", { level: 2, name: "Catalogue", exact: true })).toBeFocused();
  });
}

for (const [view, heading] of destinations.slice(1, 4)) {
  test(`history focuses ${view} when a selected record has no detail heading`, async ({ page }) => {
    await page.goto(`/?view=${view.toLowerCase()}#record=hmlr%3Adataset%3Aprice-paid-data`);
    await expect(page.getByRole("heading", { name: heading, exact: true })).toBeVisible();
    await page.getByRole("navigation", { name: "Explore catalogue" })
      .getByRole("link", { name: "Catalogue", exact: true }).press("Enter");
    await expect(page.getByRole("heading", { name: "Catalogue", exact: true })).toBeFocused();
    await page.goBack();
    await expect(page.getByRole("heading", { name: heading, exact: true })).toBeFocused();
  });
}

test("a native About fragment focuses About without stored navigation metadata", async ({ page }) => {
  await page.goto("/?view=cards");
  await expect(page.getByRole("heading", { level: 2, name: "Catalogue", exact: true })).toBeVisible();
  await page.evaluate(() => { window.location.hash = "about"; });
  await expect(page.getByRole("heading", { name: "About this Explorer", exact: true })).toBeFocused();
});

test("search, facet and clear actions preserve control focus after rendering", async ({ page }) => {
  await page.goto("/?view=cards");
  await page.getByRole("searchbox", { name: "Search catalogue", exact: true }).fill("Price Paid");
  const submit = page.getByRole("button", { name: "Search", exact: true });
  await submit.press("Enter");
  await expect(submit).toBeFocused();

  const facet = page.getByRole("group", { name: "Type", exact: true }).getByRole("checkbox").first();
  await facet.press("Space");
  await expect(facet).toBeFocused();
  const clear = page.getByRole("button", { name: "Clear search and filters", exact: true });
  await clear.press("Enter");
  await expect(clear).toBeFocused();
});

test("restoring heading focus preserves the stored scroll position", async ({ page }) => {
  await page.goto("/?view=graph");
  const heading = page.getByRole("heading", { name: "Evidence graph", exact: true });
  await expect(heading).toBeVisible();
  await expect(page.locator("body")).toBeFocused();
  const previousScroll = await page.evaluate(() => {
    window.scrollTo(0, 400);
    return window.scrollY;
  });
  expect(previousScroll).toBeGreaterThan(0);
  // Dispatch without scrolling the off-screen navigation link into view first.
  await page.getByRole("navigation", { name: "Explore catalogue" })
    .getByRole("link", { name: "About", exact: true }).dispatchEvent("click");
  await expect(page.getByRole("heading", { name: "About this Explorer", exact: true })).toBeFocused();
  await page.goBack();
  await expect(heading).toBeFocused();
  await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(previousScroll);
});
