import { expect, test, type Page } from "@playwright/test";

interface CapturedTool {
  readonly name: string;
  readonly title: string;
  readonly description: string;
  readonly inputSchema: Readonly<Record<string, unknown>>;
  readonly annotations: {
    readonly readOnlyHint: boolean;
    readonly untrustedContentHint: boolean;
  };
  execute(
    input: unknown,
    options?: { readonly signal?: AbortSignal },
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

test("manually searches and describes a governed catalogue record", async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(document, "modelContext", {
      configurable: true,
      value: undefined,
    });
  });
  await page.goto("/");

  await expect(page.locator("#catalogue-status")).toContainText(/^Validated \d+ records/);
  await expect(page.locator("#webmcp-status")).toHaveText(
    "Not available in this browser. The complete manual demonstration still works.",
  );

  const search = page.getByRole("searchbox", { name: "Search the governed catalogue" });
  await search.fill("Price Paid");
  await page.getByRole("button", { name: "Run search tool" }).click();

  await expect(page.locator("#demo-status")).toContainText("Manual search call:");
  await expect(
    page.getByRole("heading", { name: "Price Paid Data", exact: true }).first(),
  ).toBeVisible();

  const searchResult = JSON.parse((await page.locator("#result-json").textContent()) ?? "") as {
    page_tool: string;
    matches: { records: Array<{ id: string }> };
  };
  expect(searchResult.page_tool).toBe("explorer_search_catalogue");
  expect(searchResult.matches.records.map((record) => record.id)).toContain(
    "hmlr:dataset:price-paid-data",
  );

  await page
    .locator(".record-card")
    .filter({
      has: page.locator("dd").filter({ hasText: /^hmlr:dataset:price-paid-data$/ }),
    })
    .getByRole("button", { name: "Describe record and sources" })
    .click();

  await expect(page.locator("#demo-status")).toContainText(
    "Manual describe call: described hmlr:dataset:price-paid-data",
  );
  await expect(
    page.getByRole("heading", { name: "Linked foundational source records" }),
  ).toBeVisible();

  const describeResult = JSON.parse((await page.locator("#result-json").textContent()) ?? "") as {
    page_tool: string;
    record: { id: string; source_records: unknown[] };
  };
  expect(describeResult.page_tool).toBe("explorer_describe_record");
  expect(describeResult.record.id).toBe("hmlr:dataset:price-paid-data");
  expect(describeResult.record.source_records.length).toBeGreaterThan(0);
});

test("the default demonstration query finds the production ONS provider record", async ({
  page,
}) => {
  await page.goto("/");

  const search = page.getByRole("searchbox", { name: "Search the governed catalogue" });
  await expect(search).toHaveValue("ONS statistics");
  await page.getByRole("button", { name: "Run search tool" }).click();

  await expect(page.locator("#demo-status")).toContainText("Manual search call:");
  await expect(page.getByRole("heading", { name: "ONS Data API", exact: true })).toBeVisible();
  const result = JSON.parse((await page.locator("#result-json").textContent()) ?? "") as {
    matches: { records: Array<{ id: string }>; returned: number };
  };
  expect(result.matches.returned).toBeGreaterThan(0);
  expect(result.matches.returned).toBeLessThanOrEqual(5);
  expect(result.matches.records.map(({ id }) => id)).toContain("PV-ONS-DATA");
});

test("registers exactly two bounded page tools and renders both AI calls", async ({ page }) => {
  await installWebMcpCapture(page);
  await page.goto("/");

  await expect(page.locator("#webmcp-status")).toHaveText(
    "2 read-only page tools available in this browser.",
  );

  const metadata = await page.evaluate(() => {
    const tools = Reflect.get(
      globalThis,
      "__gisAiGoCapturedWebMcpTools",
    ) as CapturedTool[];
    return tools.map((tool) => ({
      name: tool.name,
      title: tool.title,
      description: tool.description,
      inputSchema: tool.inputSchema,
      annotations: tool.annotations,
    }));
  });

  expect(metadata).toHaveLength(2);
  expect(metadata.map((tool) => tool.name)).toEqual([
    "explorer_search_catalogue",
    "explorer_describe_record",
  ]);
  for (const tool of metadata) {
    expect(tool.title.length).toBeGreaterThan(0);
    expect(tool.description.length).toBeGreaterThan(0);
    expect(tool.annotations).toEqual({
      readOnlyHint: true,
      untrustedContentHint: true,
    });
    expect(tool.inputSchema).toMatchObject({
      type: "object",
      additionalProperties: false,
    });
  }
  expect(metadata[0]?.inputSchema).toMatchObject({
    required: ["query"],
    properties: {
      query: { type: "string", maxLength: 256 },
      limit: { type: "integer", maximum: 5 },
    },
  });
  expect(metadata[1]?.inputSchema).toMatchObject({
    required: ["record_id"],
    properties: {
      record_id: { type: "string", maxLength: 512 },
    },
  });

  const observation = await page.evaluate(async () => {
    const tools = Reflect.get(
      globalThis,
      "__gisAiGoCapturedWebMcpTools",
    ) as CapturedTool[];
    const searchTool = tools.find((tool) => tool.name === "explorer_search_catalogue");
    const describeTool = tools.find((tool) => tool.name === "explorer_describe_record");
    if (searchTool === undefined || describeTool === undefined) {
      throw new Error("Expected WebMCP tools were not registered");
    }
    const options = { signal: new AbortController().signal };
    const input = { query: "Price Paid", limit: 2 };
    const firstSearch = await searchTool.execute(input);
    const secondSearch = await searchTool.execute(input, options);
    const described = await describeTool.execute(
      { record_id: "hmlr:dataset:price-paid-data" },
    );
    return {
      firstSearch,
      secondSearch,
      described,
      firstSearchBytes: new TextEncoder().encode(JSON.stringify(firstSearch)).byteLength,
    };
  });

  expect(observation.firstSearch).toEqual(observation.secondSearch);
  expect(observation.firstSearchBytes).toBeLessThan(10_000);
  expect(observation.firstSearch).toMatchObject({
    schema: "gis-ai-go.webmcp-page-result.v1",
    page_tool: "explorer_search_catalogue",
    related_gateway_operation: "catalogue.search",
    boundary: {
      data_scope: "validated public catalogue metadata only",
      page_scoped: true,
      provider_call: false,
      durable_receipt: false,
      persistent_service: false,
      visible_page_update: true,
    },
  });
  const matches = (
    observation.firstSearch as {
      matches: {
        records: Array<{ description: string; tags: string[] }>;
        returned: number;
      };
    }
  ).matches;
  expect(matches.returned).toBeGreaterThan(0);
  expect(matches.returned).toBeLessThanOrEqual(2);
  expect(matches.records).toHaveLength(matches.returned);
  for (const record of matches.records) {
    expect(Array.from(record.description).length).toBeLessThanOrEqual(240);
    expect(record.tags.length).toBeLessThanOrEqual(8);
  }
  expect(observation.described).toMatchObject({
    schema: "gis-ai-go.webmcp-page-result.v1",
    page_tool: "explorer_describe_record",
    related_gateway_operation: "catalogue.describe",
    record: { id: "hmlr:dataset:price-paid-data" },
  });

  await expect(page.locator("#demo-status")).toContainText(
    "Browser-hosted AI page-tool call: described hmlr:dataset:price-paid-data",
  );
  await expect(page.locator("#result-json")).toContainText(
    '"page_tool": "explorer_describe_record"',
  );
  await expect(
    page.getByRole("heading", { name: "Linked foundational source records" }),
  ).toBeVisible();
});
