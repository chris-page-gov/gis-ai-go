import { expect, test, type Page } from "@playwright/test";

interface CapturedTool {
  readonly name: string;
  execute(
    input: unknown,
    options: { readonly signal: AbortSignal },
  ): Promise<Record<string, unknown>>;
}

async function installWebMcpCapture(page: Page): Promise<void> {
  await page.addInitScript(() => {
    const tools: unknown[] = [];
    Object.defineProperty(globalThis, "__gisAiGoCapturedWebMcpTools", {
      configurable: false,
      enumerable: false,
      value: tools,
      writable: false,
    });
    Object.defineProperty(document, "modelContext", {
      configurable: true,
      enumerable: false,
      value: {
        async registerTool(tool: unknown): Promise<void> {
          tools.push(tool);
        },
      },
      writable: false,
    });
  });
}

test("tool calls stay same-origin and create no browser-side history", async ({
  baseURL,
  context,
  page,
}) => {
  if (baseURL === undefined) throw new Error("The browser suite requires a base URL");
  const expectedOrigin = new URL(baseURL).origin;
  const externalRequests: string[] = [];
  page.on("request", (request) => {
    if (new URL(request.url()).origin !== expectedOrigin) {
      externalRequests.push(`${request.method()} ${request.url()}`);
    }
  });
  await installWebMcpCapture(page);
  await page.goto("/");
  await expect(page.locator("#webmcp-status")).toHaveText(
    "2 read-only page tools available in this browser.",
  );

  await page.evaluate(async () => {
    const tools = Reflect.get(
      globalThis,
      "__gisAiGoCapturedWebMcpTools",
    ) as CapturedTool[];
    const search = tools.find((tool) => tool.name === "explorer_search_catalogue");
    const describe = tools.find((tool) => tool.name === "explorer_describe_record");
    if (search === undefined || describe === undefined) throw new Error("Page tools are missing");
    const searchResult = await search.execute(
      { query: "Price Paid", limit: 1 },
      { signal: new AbortController().signal },
    );
    const record = (
      searchResult.matches as { records: Array<{ id: string }> }
    ).records[0];
    if (record === undefined) throw new Error("Search returned no record");
    await describe.execute(
      { record_id: record.id },
      { signal: new AbortController().signal },
    );
  });

  const browserState = await page.evaluate(async () => ({
    cacheNames: await caches.keys(),
    cookies: document.cookie,
    indexedDatabases: (await indexedDB.databases()).map((database) => database.name),
    localStorageKeys: Object.keys(localStorage),
    serviceWorkers: (await navigator.serviceWorker.getRegistrations()).length,
    sessionStorageKeys: Object.keys(sessionStorage),
  }));
  expect(browserState).toEqual({
    cacheNames: [],
    cookies: "",
    indexedDatabases: [],
    localStorageKeys: [],
    serviceWorkers: 0,
    sessionStorageKeys: [],
  });
  expect(await context.cookies(baseURL)).toEqual([]);
  expect(externalRequests).toEqual([]);
});

test("rejects extra personal and cross-site fields before execution", async ({
  baseURL,
  page,
}) => {
  if (baseURL === undefined) throw new Error("The browser suite requires a base URL");
  const expectedOrigin = new URL(baseURL).origin;
  const externalRequests: string[] = [];
  page.on("request", (request) => {
    if (new URL(request.url()).origin !== expectedOrigin) {
      externalRequests.push(request.url());
    }
  });
  await installWebMcpCapture(page);
  await page.goto("/");
  await expect(page.locator("#webmcp-status")).toContainText("2 read-only page tools");

  const outcomes = await page.evaluate(async () => {
    const tools = Reflect.get(
      globalThis,
      "__gisAiGoCapturedWebMcpTools",
    ) as CapturedTool[];
    const search = tools.find((tool) => tool.name === "explorer_search_catalogue");
    const describe = tools.find((tool) => tool.name === "explorer_describe_record");
    if (search === undefined || describe === undefined) throw new Error("Page tools are missing");
    const rejected = async (
      tool: CapturedTool,
      input: unknown,
    ): Promise<{ accepted: boolean; message: string }> => {
      try {
        await tool.execute(input, { signal: new AbortController().signal });
        return { accepted: true, message: "" };
      } catch (error) {
        return {
          accepted: false,
          message: error instanceof Error ? error.message : String(error),
        };
      }
    };
    return {
      crossSite: await rejected(search, {
        query: "ONS",
        endpoint: "https://attacker.invalid/collect",
      }),
      describeCrossSite: await rejected(describe, {
        record_id: "hmlr:dataset:price-paid-data",
        caller_url: "https://attacker.invalid/collect",
      }),
      personal: await rejected(search, {
        query: "ONS",
        person_name: "Example Person",
      }),
    };
  });

  for (const outcome of Object.values(outcomes)) {
    expect(outcome.accepted).toBe(false);
    expect(outcome.message).toContain("contains unsupported fields");
  }
  expect(outcomes.crossSite.message).toContain("endpoint");
  expect(outcomes.describeCrossSite.message).toContain("caller_url");
  expect(outcomes.personal.message).toContain("person_name");
  await expect(page.locator("#demo-results")).toBeHidden();
  await expect(page.locator("#demo-status")).toHaveText(
    "Ready. The manual controls and any registered page tools use the same functions.",
  );
  expect(externalRequests).toEqual([]);
});

test.describe("JavaScript-free boundary", () => {
  test.use({ javaScriptEnabled: false });

  test("keeps the explanation and governed downloads available", async ({ page }) => {
    await page.goto("/");

    await expect(page.getByRole("heading", { name: "JavaScript is off" })).toBeVisible();
    await expect(
      page.getByText(
        "WebMCP and the manual tool simulation need JavaScript. The architectural " +
          "explanation and the governed catalogue downloads remain available; no " +
          "substitute data has been selected.",
        { exact: true },
      ),
    ).toBeVisible();
    await expect(
      page.getByRole("heading", {
        name: "WebMCP complements the gateway; it does not replace it",
      }),
    ).toBeVisible();
    await expect(
      page.getByRole("link", { name: "Download the catalogue JSON used by this page" }),
    ).toBeVisible();
    await expect(
      page.getByRole("link", { name: "Download the catalogue checksum ledger" }),
    ).toBeVisible();
  });

  test("never serialises the manual query into a URL", async ({ page }) => {
    const sentinel = "private-sentinel-WEBMCP-598";
    const requests: string[] = [];
    page.on("request", (request) => requests.push(request.url()));
    await page.goto("/");
    await page.locator("#catalogue-query").fill(sentinel);
    const submission = page.waitForRequest((request) => request.isNavigationRequest());
    // The no-field form reloads the same URL, so observe the native request rather
    // than depending on Playwright's actionability or navigation lifecycle timing.
    await page.getByRole("button", { name: "Run search tool" }).click({
      force: true,
      noWaitAfter: true,
    });
    const submittedRequest = await submission;

    expect(submittedRequest.url()).not.toContain(sentinel);
    expect(page.url()).not.toContain(sentinel);
    expect(requests.every((url) => !new URL(url).searchParams.has("query"))).toBe(true);
  });
});
