import { expect, test } from "../fixtures/assurance";

const PRICE_PAID_ID = "hmlr:dataset:price-paid-data";

test("answers the focused question by default without WebMCP", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", {
      level: 1,
      name: "INSPIRE polygon: indicative or legal boundary?",
    }),
  ).toBeVisible();
  await expect(
    page
      .getByText(
        "Polygons are indicative and do not establish the exact legal extent of a title.",
        { exact: true },
      )
      .first(),
  ).toBeVisible();

  const canonical = new URL(page.url());
  expect(canonical.searchParams.get("view")).toBe("cards");
  expect(canonical.searchParams.get("q")).toBe("inspire");
  expect(canonical.searchParams.getAll("type")).toEqual(["dataset"]);
  expect(decodeURIComponent(canonical.hash)).toBe(
    "#record=hmlr:dataset:inspire-index-polygons",
  );

  const optionalBrowserApis = await page.evaluate(() => ({
    globalModelContext: Reflect.get(globalThis, "modelContext"),
    navigatorModelContext: Reflect.get(navigator, "modelContext"),
    webMCP: Reflect.get(globalThis, "webMCP"),
  }));
  expect(optionalBrowserApis).toEqual({
    globalModelContext: undefined,
    navigatorModelContext: undefined,
    webMCP: undefined,
  });
});

test("searches, filters and clears through labelled controls", async ({ page }) => {
  await page.goto("/?view=cards");

  const search = page.getByRole("searchbox", {
    name: /Search(?: the public)? catalogue/i,
  });
  await search.fill("Price Paid");
  await page.getByRole("checkbox", { name: /Dataset/i }).check();
  await page.getByRole("button", { name: /^Search$/i }).click();

  await expect(page.getByRole("link", { name: "Price Paid Data", exact: true })).toHaveCount(1);
  await expect(
    page.getByRole("link", { name: "Index polygons spatial data (INSPIRE)", exact: true }),
  ).toHaveCount(0);
  await expect.poll(() => new URL(page.url()).searchParams.get("q")).toBe("Price Paid");
  expect(new URL(page.url()).searchParams.getAll("type")).toEqual(["dataset"]);

  await page.getByRole("button", { name: "Clear search and filters", exact: true }).click();
  await expect(search).toHaveValue("");
  await expect(page.getByRole("checkbox", { name: /Dataset/i })).not.toBeChecked();
  await expect.poll(() => new URL(page.url()).searchParams.has("q")).toBe(false);
  expect(new URL(page.url()).searchParams.has("type")).toBe(false);
});

test("restores a direct URL containing every approved facet", async ({ page }) => {
  const parameters = new URLSearchParams([
    ["view", "cards"],
    ["q", "Price Paid"],
    ["type", "dataset"],
    ["authority", "source-authoritative"],
    ["access", "public"],
    ["rights", "open-with-conditions"],
    ["freshness", "current"],
    ["tag", "hmlr"],
  ]);
  await page.goto(`/?${parameters.toString()}#record=${encodeURIComponent(PRICE_PAID_ID)}`);

  await expect(page.getByRole("heading", { level: 2, name: "Price Paid Data" })).toBeVisible();
  await expect(
    page.getByRole("searchbox", { name: /Search(?: the public)? catalogue/i }),
  ).toHaveValue("Price Paid");
  for (const label of [
    /Dataset/i,
    /Source authoritative/i,
    /^Public(?: \(\d+\))?$/i,
    /Open with conditions/i,
    /^Current(?: \(\d+\))?$/i,
    /^hmlr(?: \(\d+\))?$/i,
  ]) {
    await expect(page.getByRole("checkbox", { name: label })).toBeChecked();
  }

  const current = new URL(page.url());
  expect([...new Set(current.searchParams.keys())].sort()).toEqual([
    "access",
    "authority",
    "freshness",
    "q",
    "rights",
    "tag",
    "type",
    "view",
  ]);
  expect(current.hash.startsWith("#record=")).toBe(true);
  expect(decodeURIComponent(current.hash)).toBe(`#record=${PRICE_PAID_ID}`);
});

test("keeps list and record state in browser history", async ({ page }) => {
  await page.goto("/?view=cards&q=Price%20Paid&type=dataset");
  await page.getByRole("link", { name: "Price Paid Data", exact: true }).click();

  await expect.poll(() => decodeURIComponent(new URL(page.url()).hash)).toBe(
    `#record=${PRICE_PAID_ID}`,
  );
  await expect(page.getByRole("heading", { level: 2, name: "Price Paid Data" })).toBeVisible();

  await page.goBack();
  await expect.poll(() => new URL(page.url()).hash).toBe("");
  await expect(page.getByRole("link", { name: "Price Paid Data", exact: true })).toBeVisible();
  await expect(
    page.getByRole("searchbox", { name: /Search(?: the public)? catalogue/i }),
  ).toHaveValue("Price Paid");

  await page.goForward();
  await expect.poll(() => decodeURIComponent(new URL(page.url()).hash)).toBe(
    `#record=${PRICE_PAID_ID}`,
  );
  await expect(page.getByRole("heading", { level: 2, name: "Price Paid Data" })).toBeVisible();
});

test("supports skip navigation and view changes from the keyboard", async ({ page }) => {
  await page.goto("/?view=cards");

  await page.keyboard.press("Tab");
  const skipLink = page.getByRole("link", { name: "Skip to main content" });
  await expect(skipLink).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.locator("#main-content")).toBeFocused();

  const graphLink = page.getByRole("link", { name: /^Graph$/i });
  await graphLink.focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { level: 2, name: "Evidence graph" })).toBeVisible();
  await expect(graphLink).toHaveAttribute("aria-current", "page");
  await expect.poll(() => new URL(page.url()).searchParams.get("view")).toBe("graph");
});
