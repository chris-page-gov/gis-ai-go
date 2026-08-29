import AxeBuilder from "@axe-core/playwright";
import { expect, test, type Locator, type Page } from "@playwright/test";

async function waitForReadyFallback(page: Page): Promise<void> {
  await expect(page.locator("#catalogue-status")).toContainText(/^Validated \d+ records/);
  await expect(page.locator("#webmcp-status")).toContainText(
    "The complete manual demonstration still works.",
  );
}

async function expectKeyboardFocus(page: Page, control: Locator): Promise<void> {
  for (let attempt = 0; attempt < 80; attempt += 1) {
    await page.keyboard.press("Tab");
    if (await control.evaluate((element) => element === document.activeElement)) break;
  }
  await expect(control).toBeFocused();
  await expect(control).toHaveCSS("outline-style", "solid");
  await expect(control).toHaveCSS("outline-width", "3px");
  await expect(control).toHaveCSS("outline-offset", "2px");
}

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(document, "modelContext", {
      configurable: true,
      value: undefined,
    });
  });
});

test("has no detectable WCAG A or AA violations", async ({ page }) => {
  await page.goto("/");
  await waitForReadyFallback(page);

  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22a", "wcag22aa"])
    .analyze();
  expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([]);
});

test("shows visible keyboard focus through the complete manual journey", async ({ page }) => {
  await page.goto("/");
  await waitForReadyFallback(page);

  const search = page.getByRole("searchbox", {
    name: "Catalogue keywords (1 to 10 terms)",
  });
  await expectKeyboardFocus(page, search);
  await search.fill("Price Paid");

  const submit = page.getByRole("button", { name: "Run search tool" });
  await expectKeyboardFocus(page, submit);
  await page.keyboard.press("Enter");
  await expect(page.locator("#demo-status")).toContainText("Manual search call:");

  const describe = page
    .locator(".record-card")
    .filter({
      has: page.locator("dd").filter({ hasText: /^hmlr:dataset:price-paid-data$/ }),
    })
    .getByRole("button", { name: "Describe record and sources" });
  await expectKeyboardFocus(page, describe);
  await page.keyboard.press("Enter");
  await expect(page.locator("#demo-status")).toContainText("Manual describe call:");
});

test.describe("320 CSS-pixel, 400% zoom-equivalent reflow", () => {
  test.use({ hasTouch: true, viewport: { height: 800, width: 320 } });

  test("keeps the manual journey operable without document-level overflow", async ({ page }) => {
    await page.goto("/");
    await waitForReadyFallback(page);

    const search = page.getByRole("searchbox", {
      name: "Catalogue keywords (1 to 10 terms)",
    });
    await search.fill("Price Paid");
    await page.getByRole("button", { name: "Run search tool" }).tap();
    await expect(
      page.getByRole("heading", { name: "Price Paid Data", exact: true }).first(),
    ).toBeVisible();

    await page
      .locator(".record-card")
      .filter({
        has: page.locator("dd").filter({ hasText: /^hmlr:dataset:price-paid-data$/ }),
      })
      .getByRole("button", { name: "Describe record and sources" })
      .tap();
    await expect(page.locator("#demo-status")).toContainText("Manual describe call:");

    const layout = await page.evaluate(() => {
      const viewportWidth = document.documentElement.clientWidth;
      const offenders = [...document.querySelectorAll<HTMLElement>("body *")]
        .map((element) => ({
          html: element.outerHTML.slice(0, 160),
          right: Math.round(element.getBoundingClientRect().right),
          scrollWidth: element.scrollWidth,
        }))
        .filter((item) => item.right > viewportWidth + 1 || item.scrollWidth > viewportWidth + 1)
        .slice(0, 10);
      return {
        offenders,
        overflow: document.documentElement.scrollWidth - viewportWidth,
      };
    });
    expect(layout.overflow, JSON.stringify(layout.offenders, null, 2)).toBeLessThanOrEqual(1);

    for (const control of await page.locator('button, input[type="search"]').all()) {
      const box = await control.boundingBox();
      expect(box).not.toBeNull();
      expect(box!.height).toBeGreaterThanOrEqual(44);
    }
  });
});
