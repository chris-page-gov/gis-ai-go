import AxeBuilder from "@axe-core/playwright";

import { expect, test } from "../fixtures/assurance";

const views = [
  ["cards", "Catalogue"],
  ["graph", "Evidence graph"],
  ["timeline", "Catalogue timeline"],
  ["map", "Coverage schematic — not a property map"],
] as const;

for (const [view, heading] of views) {
  test(`${view} view has no detectable WCAG A or AA violations`, async ({ page }) => {
    await page.goto(`/?view=${view}`);
    await expect(page.getByRole("heading", { level: 2, name: heading })).toBeVisible();

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
      .analyze();
    expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([]);
  });
}

test("visual catalogue views provide complete text alternatives", async ({ page }) => {
  await page.goto("/?view=graph");
  await expect(
    page.getByRole("heading", { level: 3, name: "Complete relationship list" }),
  ).toBeVisible();
  const visualNodes = await page.locator("svg .graph-node").count();
  expect(visualNodes).toBeGreaterThan(0);
  await expect(page.locator("ol.adjacency-list > li")).toHaveCount(visualNodes);

  await page.goto("/?view=timeline");
  await expect(page.getByRole("heading", { level: 3, name: "Dates not recorded" })).toBeVisible();
  await expect(page.getByRole("heading", { level: 3, name: "Recorded events" })).toBeVisible();
  await expect(page.locator(".timeline-legend dt")).toHaveText([
    "Observation",
    "Modification",
    "Publication",
    "Release",
  ]);

  await page.goto("/?view=map");
  const alternative = page.locator(".map-alternative");
  await expect(
    alternative.getByRole("heading", { level: 3, name: "Complete text description" }),
  ).toBeVisible();
  await expect(alternative.getByRole("listitem")).toHaveCount(7);
  await expect(
    alternative.getByText(
      "The polygons are indicative and do not establish the exact legal extent of a title.",
      { exact: true },
    ),
  ).toBeVisible();
});

test.describe("small touch viewport", () => {
  test.use({ hasTouch: true, viewport: { height: 800, width: 320 } });

  test("remains operable without document-level horizontal scrolling", async ({ page }) => {
    await page.goto("/?view=cards");
    await page.getByRole("link", { name: /^Map$/i }).tap();
    await expect(
      page.getByRole("heading", { level: 2, name: "Coverage schematic — not a property map" }),
    ).toBeVisible();

    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    expect(overflow).toBeLessThanOrEqual(1);
  });
});

test("remains usable in forced-colours mode", async ({ page }) => {
  await page.emulateMedia({ forcedColors: "active" });
  await page.goto("/?view=graph");

  expect(await page.evaluate(() => matchMedia("(forced-colors: active)").matches)).toBe(true);
  await expect(page.getByRole("heading", { level: 2, name: "Evidence graph" })).toBeVisible();
  const search = page.getByRole("searchbox", { name: /Search(?: the public)? catalogue/i });
  await search.focus();
  await expect(search).toBeFocused();
  await page.getByRole("link", { name: /^Map$/i }).click();
  await expect(
    page.getByRole("heading", { level: 3, name: "Complete text description" }),
  ).toBeVisible();
});

test("honours reduced-motion preference across view changes", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/?view=cards");

  expect(await page.evaluate(() => matchMedia("(prefers-reduced-motion: reduce)").matches)).toBe(
    true,
  );
  await page.getByRole("link", { name: /^Timeline$/i }).click();
  await expect(page.getByRole("heading", { level: 2, name: "Catalogue timeline" })).toBeVisible();
  const activeAnimations = await page.evaluate(() =>
    document
      .getAnimations()
      .filter((animation) => {
        const duration = animation.effect?.getComputedTiming().duration;
        return animation.playState !== "finished" && typeof duration === "number" && duration > 1;
      })
      .map((animation) => animation.id),
  );
  expect(activeAnimations).toEqual([]);
});
