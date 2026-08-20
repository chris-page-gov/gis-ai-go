import { expect, test } from "../fixtures/assurance";

const PRICE_PAID_ID = "hmlr:dataset:price-paid-data";

const INERT_WEBMCP_SENTINEL = String.raw`
(() => {
  const activity = [];
  const record = (message) => {
    activity.push(message);
  };
  const method = (name) => new Proxy(Object.freeze(function () {}), {
    apply() {
      record(name + " called");
      return undefined;
    },
    construct() {
      record(name + " constructed");
      return {};
    },
    set() {
      record(name + " property set");
      return false;
    },
    defineProperty() {
      record(name + " property defined");
      return false;
    },
    deleteProperty() {
      record(name + " property deleted");
      return false;
    },
    setPrototypeOf() {
      record(name + " prototype changed");
      return false;
    },
  });
  const target = Object.freeze(Object.assign(function () {}, {
    registerTool: method("registerTool"),
    unregisterTool: method("unregisterTool"),
    provideContext: method("provideContext"),
    clearContext: method("clearContext"),
  }));
  const sentinel = new Proxy(target, {
    apply() {
      record("sentinel called");
      return undefined;
    },
    construct() {
      record("sentinel constructed");
      return {};
    },
    set() {
      record("sentinel property set");
      return false;
    },
    defineProperty() {
      record("sentinel property defined");
      return false;
    },
    deleteProperty() {
      record("sentinel property deleted");
      return false;
    },
    setPrototypeOf() {
      record("sentinel prototype changed");
      return false;
    },
  });

  const expose = (owner, name, label) => {
    Object.defineProperty(owner, name, {
      configurable: false,
      enumerable: false,
      get: () => sentinel,
      set: () => record(label + " replaced"),
    });
  };
  expose(globalThis, "webMCP", "globalThis.webMCP");
  expose(globalThis, "modelContext", "globalThis.modelContext");
  expose(navigator, "modelContext", "navigator.modelContext");

  Object.defineProperty(globalThis, "__gisAiGoWebMcpAudit", {
    configurable: false,
    enumerable: false,
    writable: false,
    value: Object.freeze({
      snapshot: () => ({
        activity: [...activity],
        globalModelContextIntact: Reflect.get(globalThis, "modelContext") === sentinel,
        navigatorModelContextIntact: Reflect.get(navigator, "modelContext") === sentinel,
        webMCPIntact: Reflect.get(globalThis, "webMCP") === sentinel,
      }),
    }),
  });
})();
`;

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

test("gracefully ignores inert WebMCP sentinels during the focused journey", async ({ page }) => {
  // This is graceful non-use assurance, not a claim of WebMCP capability or interoperability.
  await page.route("**/webmcp-sentinel.js", async (route) => {
    await route.fulfill({
      body: INERT_WEBMCP_SENTINEL,
      contentType: "application/javascript; charset=utf-8",
      status: 200,
    });
  });

  let sentinelInjected = false;
  await page.route(
    "**/",
    async (route) => {
      const response = await route.fetch();
      const html = await response.text();
      const moduleMarker = '<script type="module"';
      if (!html.includes(moduleMarker)) {
        throw new Error("Explorer entry page has no module script marker");
      }
      sentinelInjected = true;
      await route.fulfill({
        response,
        body: html.replace(
          moduleMarker,
          '<script src="./webmcp-sentinel.js"></script>\n    <script type="module"',
        ),
      });
    },
    { times: 1 },
  );

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
  expect(sentinelInjected).toBe(true);

  const audit = await page.evaluate(() => {
    const value = Reflect.get(globalThis, "__gisAiGoWebMcpAudit") as {
      snapshot: () => {
        activity: string[];
        globalModelContextIntact: boolean;
        navigatorModelContextIntact: boolean;
        webMCPIntact: boolean;
      };
    };
    return value.snapshot();
  });
  expect(audit).toEqual({
    activity: [],
    globalModelContextIntact: true,
    navigatorModelContextIntact: true,
    webMCPIntact: true,
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
  for (const id of [
    "#facet-types-dataset",
    "#facet-authority-source-authoritative",
    "#facet-access-public",
    "#facet-rights-open-with-conditions",
    "#facet-freshness-current",
    "#facet-tags-hmlr",
  ]) {
    await expect(page.locator(id)).toBeChecked();
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
