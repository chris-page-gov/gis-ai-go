import { expect, test } from "../fixtures/assurance";

test("fails hostile and unknown URL state closed without creating markup", async ({ page }) => {
  const hostile = '<img src="https://attacker.invalid/track" onerror="alert(1)">';
  await page.goto(
    `/?view=javascript%3Aalert%281%29&q=${encodeURIComponent(hostile)}` +
      "&unknown=https%3A%2F%2Fattacker.invalid#record=does-not-exist",
  );

  await expect(page.locator('.warning-panel[role="status"]')).toContainText(
    /ignored|not recognised|invalid/i,
  );
  await expect(page.getByRole("heading", { name: "Record not found" })).toBeVisible();
  await expect(
    page.getByRole("searchbox", { name: /Search(?: the public)? catalogue/i }),
  ).toHaveValue(hostile.slice(0, 200));
  await expect(page.locator('img[src*="attacker.invalid"]')).toHaveCount(0);
  await expect(page.locator("script:not([type=module])")).toHaveCount(0);
  await expect(
    page.getByRole("heading", { name: "Index polygons spatial data (INSPIRE)" }),
  ).toHaveCount(0);

  const current = new URL(page.url());
  expect([...current.searchParams.keys()].every((key) => key === "view" || key === "q")).toBe(
    true,
  );
  expect(current.searchParams.get("view")).toBe("cards");
});

test("primary controls retain 44 CSS-pixel targets", async ({ page }) => {
  await page.goto("/?view=cards");
  const controls = page.locator(
    '.view-navigation a, button, input[type="search"], .checkbox-item label',
  );
  await expect(controls.first()).toBeVisible();
  expect(await controls.count()).toBeGreaterThan(0);
  for (const control of await controls.all()) {
    const box = await control.boundingBox();
    expect(box, await control.getAttribute("aria-label") ?? (await control.textContent()) ?? "control")
      .not.toBeNull();
    expect(box!.height).toBeGreaterThanOrEqual(44);
  }
});

test.describe("JavaScript-free fallback", () => {
  test.use({ javaScriptEnabled: false });

  test("keeps the legal answer and governed downloads available", async ({ page }) => {
    await page.goto("/");

    await expect(
      page.getByRole("heading", {
        name: "INSPIRE polygon: indicative or legal boundary?",
      }),
    ).toBeVisible();
    await expect(
      page.getByText(
        "Polygons are indicative and do not establish the exact legal extent of a title.",
        { exact: true },
      ),
    ).toBeVisible();
    await expect(page.getByRole("link", { name: "Download JSON", exact: true })).toBeVisible();
    await expect(page.getByRole("link", { name: "Download JSON-LD", exact: true })).toBeVisible();
    await expect(
      page.getByRole("link", { name: "Download checksums", exact: true }),
    ).toBeVisible();
  });
});
