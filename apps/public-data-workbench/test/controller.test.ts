import { describe, expect, it, vi } from "vitest";
import { createWorkbench } from "../src/controller";
import { findData, records } from "../src/discovery";
import { createMcpCall } from "../src/mcp-client";
import { PAGE_TOOL_DEFINITIONS, registerPageTools } from "../src/webmcp";
const PLAN = `gis-ai-go:web216-cpih-selection-plan:sha256:${"a".repeat(64)}`;
const RECEIPT = `gis-ai-go:evidence-receipt:sha256:${"b".repeat(64)}`;
const rawPlan = { schema: "gis-ai-go.web216-cpih-selection-plan.v1", selection: { period: "2026-07" }, authority: { grants_execution: false }, plan_id: PLAN };
const rawResult = { schema: "gis-ai-go.web216-cpih-query-result.v1", result: { state: "validated-captured-observation", period: "2026-07", series: { cdid: "L522", dataset_id: "MM23", base_year: 2015, unit: "Index, base year = 100" }, observation: { value: "142.7" }, provider_egress: false }, evidence: { receipt: { receipt_id: RECEIPT }, storage: { status: "persisted" } } };

describe("bounded public-data workbench", () => {
  it("discovers CPIH without claiming retrieval and omits contact fields", () => {
    const result = findData({ query: "CONSUMER prices" });
    expect(result.records[0]?.id).toBe("ons-data-api:cpih01");
    expect(result.metadata_only).toBe(true); expect(records).toHaveLength(7);
    expect(JSON.stringify(records)).not.toMatch(/contact|email|@ons\./i);
  });
  it("rejects unknown fields and excessive or unsupported queries without truncation", () => {
    for (const value of [{ query: "a ".repeat(11) }, { query: "a".repeat(257) }, { query: "é" }, { query: "" }, { query: "prices", endpoint: "https://invalid.example" }]) expect(() => findData(value)).toThrow();
    expect(findData({ query: "xxzznotadataset" }).records).toEqual([]);
    expect(findData({ query: "constructor" }).records).toEqual([]);
  });
  it("refuses execution before selection and unsupported months", async () => {
    const call = vi.fn(), app = createWorkbench(call);
    await expect(app.retrieve({ selection_plan_id: PLAN })).rejects.toThrow();
    await expect(app.select({ period: "latest" })).rejects.toThrow(); expect(call).not.toHaveBeenCalled();
  });
  it("uses the same key after response loss, same-plan review and replay", async () => {
    let lose = true;
    const call = vi.fn(async (name: string, _input: Record<string, unknown>) => { if (name === "web216_cpih_select") return rawPlan; if (lose) { lose = false; throw new Error("lost"); } return rawResult; });
    const app = createWorkbench(call); await app.select({ period: "2026-07" });
    await expect(app.retrieve({ selection_plan_id: PLAN })).rejects.toThrow("lost");
    await app.select({ period: "2026-07" }); expect((await app.retrieve({ selection_plan_id: PLAN })).value).toBe("142.7");
    expect(call.mock.calls[1]?.[1]).toEqual(call.mock.calls[3]?.[1]);
  });
  it("rejects substituted plans and malformed success rather than presenting a value", async () => {
    const app = createWorkbench(vi.fn(async (name) => name === "web216_cpih_select" ? rawPlan : { ...rawResult, result: { ...rawResult.result, provider_egress: true } }));
    await app.select({ period: "2026-07" });
    await expect(app.retrieve({ selection_plan_id: `${PLAN}x` })).rejects.toThrow();
    await expect(app.retrieve({ selection_plan_id: PLAN })).rejects.toThrow("display contract");
  });
  it("inspects by exact receipt ID without a second query", async () => {
    const call = vi.fn(async (_name: string, _input: Record<string, unknown>) => rawResult), app = createWorkbench(call);
    expect((await app.inspect({ receipt_id: RECEIPT })).receiptId).toBe(RECEIPT);
    expect(call.mock.calls[0]?.[0]).toBe("web216_cpih_inspect");
  });
  it("prevents overlapping operations", async () => {
    let finish!: (value: typeof rawPlan) => void;
    const app = createWorkbench(() => new Promise((resolve) => { finish = resolve; }));
    const first = app.select({ period: "2026-07" }); await expect(app.select({ period: "2026-07" })).rejects.toThrow("already running");
    finish(rawPlan); await first;
  });
  it("does not restage a delayed selection after the user changes month", async () => {
    let finish!: (value: typeof rawPlan) => void;
    const app = createWorkbench(() => new Promise((resolve) => { finish = resolve; }));
    const pending = app.select({ period: "2026-07" }); app.invalidateSelection(); finish(rawPlan);
    await expect(pending).rejects.toThrow("month changed");
    await expect(app.retrieve({ selection_plan_id: PLAN })).rejects.toThrow("Review the exact selection");
  });
  it("binds returned observation and receipt to the exact requested identity", async () => {
    const wrongMonth = { ...rawResult, result: { ...rawResult.result, period: "2026-01" } };
    const app = createWorkbench(async (name) => name === "web216_cpih_select" ? rawPlan : wrongMonth);
    await app.select({ period: "2026-07" }); await expect(app.retrieve({ selection_plan_id: PLAN })).rejects.toThrow("returned period");
    const inspect = createWorkbench(async () => rawResult);
    await expect(inspect.inspect({ receipt_id: RECEIPT.replace(/b/g, "c") })).rejects.toThrow("returned receipt");
  });
  it("rejects substituted series, unit and base year", async () => {
    for (const replacement of [{ cdid: "OTHER" }, { dataset_id: "OTHER" }, { unit: "Percentage" }, { base_year: 2020 }]) {
      const app = createWorkbench(async () => ({ ...rawResult, result: { ...rawResult.result, series: { ...rawResult.result.series, ...replacement } } }));
      await expect(app.inspect({ receipt_id: RECEIPT })).rejects.toThrow("display contract");
    }
  });
  it("prevents preview or hosted pages from reaching another origin", async () => {
    const call = createMcpCall({ origin: "https://example.invalid" } as Location);
    await expect(call("web216_cpih_select", { period: "2026-07" })).rejects.toThrow("local workbench");
  });
  it("registers four explicit tools, updates shared actions and handles invalid calls", async () => {
    const registered: Array<{ name: string; execute(input: unknown): Promise<unknown> }> = [];
    const signals: AbortSignal[] = [];
    Object.defineProperty(document, "modelContext", { configurable: true, value: { registerTool(tool: typeof registered[number], options: { signal: AbortSignal }) { registered.push(tool); signals.push(options.signal); } } });
    const actions = { find: vi.fn(async (input) => findData(input)), select: vi.fn(), retrieve: vi.fn(), inspect: vi.fn() };
    const registration = await registerPageTools(document, actions);
    expect(registration.status).toBe("registered"); expect(registered.map((tool) => tool.name)).toEqual(PAGE_TOOL_DEFINITIONS.map((tool) => tool.name));
    await registered[0]!.execute({ query: "prices" }); expect(actions.find).toHaveBeenCalled();
    expect(await registered[0]!.execute({ unexpected: true })).toMatchObject({ isError: true });
    registration.dispose(); expect(signals.every((signal) => signal.aborted)).toBe(true);
    Reflect.deleteProperty(document, "modelContext");
  });
  it("reports unsupported hosts without a fake registration", async () => {
    const result = await registerPageTools(document, { find: vi.fn(), select: vi.fn(), retrieve: vi.fn(), inspect: vi.fn() });
    expect(result.status).toBe("unsupported");
  });
});
