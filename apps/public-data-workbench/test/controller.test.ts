import { describe, expect, it, vi } from "vitest";
import { createWorkbench, type Period, type WorkbenchOptions } from "../src/controller";
import { findData, records } from "../src/discovery";
import { createMcpCall } from "../src/mcp-client";
import { PAGE_TOOL_DEFINITIONS, registerPageTools } from "../src/webmcp";
const PLAN = `gis-ai-go:web216-cpih-selection-plan:sha256:${"a".repeat(64)}`;
const RECEIPT = `gis-ai-go:evidence-receipt:sha256:${"b".repeat(64)}`;
const rawPlan = { schema: "gis-ai-go.web216-cpih-selection-plan.v1", selection: { period: "2026-07" }, authority: { grants_execution: false }, plan_id: PLAN };
const rawResult = { schema: "gis-ai-go.web216-cpih-query-result.v1", result: { state: "validated-captured-observation", period: "2026-07", series: { cdid: "L522", dataset_id: "MM23", base_year: 2015, unit: "Index, base year = 100" }, observation: { value: "142.7" }, provider_egress: false }, evidence: { receipt: { receipt_id: RECEIPT }, storage: { status: "persisted" } } };
const contentId = (family: string, digit: string) => `gis-ai-go:${family}:sha256:${digit.repeat(64)}`;
// Synthetic display-contract fixture. IDs are not recomputed and this is not
// full-material/chain verification; those belong to the server's own tests.
function hostedResult(selected: Period = "2026-07") {
  const receipt = { schema: "gis-ai-go.web216-cpih-receipt.v1", receipt_id: RECEIPT,
    outcome: "success", execution_scope: "experimental-pinned-capture-read-not-live-provider-evidence",
    operation: { name: "read-validated-cpih-capture", contract_version: "v1", period: selected },
    evidence: { delivery: "inline-only", persistence: "not-persisted", attestation: "not-attested" } };
  const storeId = contentId("web216-transactional-store", "c");
  const recordId = contentId("web216-transactional-record", "d");
  const eventId = contentId("web216-transactional-event", "e");
  return {
    schema: "gis-ai-go.web216-hosted-cpih-result.v1",
    result: { ...structuredClone(rawResult.result), schema: "gis-ai-go.web216-cpih-result-core.v1", period: selected,
      observation: { value: selected === "2026-01" ? "139.4" : "142.7" }, currency: "as-of-recorded-capture-not-always-current" },
    evidence: { receipt,
      record: { schema: "gis-ai-go.web216-transactional-record.v1", record_id: recordId, store_id: storeId,
        idempotency_key_sha256: "1".repeat(64), request_fingerprint_sha256: "2".repeat(64), period: selected,
        recorded_at: "2026-09-14T18:01:00.000Z", retain_until: "2027-09-14T18:01:00.000Z",
        receipt: structuredClone(receipt), verification: "full-material-verified-model-record",
        boundary: { persistence: "not-established-by-contract", attestation: "not-attested", provider_egress: false, execution_authority: false } },
      event: { schema: "gis-ai-go.web216-transactional-event.v1", event_id: eventId, store_id: storeId,
        sequence: 1, previous_event_id: null as string | null, record_id: recordId, receipt_id: RECEIPT,
        idempotency_key_sha256: "1".repeat(64), recorded_at: "2026-09-14T18:01:00.000Z" },
      checkpoint: { schema: "gis-ai-go.web216-transactional-head.v1", store_id: storeId,
        sequence: 1, tail_event_id: eventId, checkpoint_id: contentId("web216-transactional-checkpoint", "f") },
      storage_observation: { schema: "gis-ai-go.web216-hosted-storage-observation.v1", persistence: "present-in-verified-adapter-snapshot",
        checkpoint_scope: "verified-returned-snapshot", read_freshness: "not-established-by-application", store_id: storeId,
        integrity: "full-snapshot-content-and-chain-verified-internally", returned_evidence_scope: "selected-record-event-and-head-subset",
        attestation: "not-attested", independent_rollback_anchor: false, disaster_recovery: "not-established", deployment: "not-established-by-application" },
    },
    boundary: { provider_egress: false, activated_supported_release: false, attested: false },
  };
}

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
  it("defaults to local evidence and admits hosted evidence only through a closed construction-time mode", async () => {
    expect((await createWorkbench(async () => rawResult).inspect({ receipt_id: RECEIPT })).value).toBe("142.7");
    const options: WorkbenchOptions = { evidenceMode: "hosted-transaction" };
    const app = createWorkbench(async () => hostedResult(), options);
    Reflect.set(options, "evidenceMode", "local-filesystem"); // Captured once, not read on each call.
    expect((await app.inspect({ receipt_id: RECEIPT })).value).toBe("142.7");
    const getter = vi.fn(() => "hosted-transaction");
    const accessor = Object.defineProperty({}, "evidenceMode", { enumerable: true, get: getter });
    for (const bad of [null, [], "hosted-transaction", { evidenceMode: "auto" }, { evidenceMode: undefined },
      { evidenceMode: "hosted-transaction", endpoint: "https://invalid.example" },
      { evidenceMode: "hosted-transaction", [Symbol("extra")]: true },
      Object.create({ evidenceMode: "hosted-transaction" }), accessor,
      Object.defineProperty({}, "evidenceMode", { value: "hosted-transaction" })]) {
      expect(() => createWorkbench(vi.fn(), bad as WorkbenchOptions)).toThrow("construction options");
    }
    expect(getter).not.toHaveBeenCalled();
  });
  it("rejects local/hosted family substitutions and mixed storage envelopes", async () => {
    const cases = [
      { mode: "local-filesystem", result: hostedResult() },
      { mode: "hosted-transaction", result: rawResult },
      { mode: "hosted-transaction", result: { ...hostedResult(), evidence: { ...hostedResult().evidence, storage: { status: "persisted" } } } },
      { mode: "local-filesystem", result: { ...rawResult, evidence: { ...rawResult.evidence, storage_observation: hostedResult().evidence.storage_observation } } },
      { mode: "local-filesystem", result: { ...rawResult, evidence: { ...rawResult.evidence, checkpoint: hostedResult().evidence.checkpoint } } },
      { mode: "local-filesystem", result: { ...rawResult, evidence: { ...rawResult.evidence, record: hostedResult().evidence.record } } },
      { mode: "local-filesystem", result: { ...rawResult, evidence: { ...rawResult.evidence, event: hostedResult().evidence.event } } },
    ] as const;
    for (const item of cases) {
      const app = createWorkbench(async () => item.result, { evidenceMode: item.mode });
      await expect(app.inspect({ receipt_id: RECEIPT })).rejects.toThrow();
    }
  });
  it("uses the same shared selection/retrieval/inspection and lost-response key in hosted mode", async () => {
    let lose = true;
    const call = vi.fn(async (name: string, _input: Record<string, unknown>) => {
      if (name === "web216_cpih_select") return rawPlan;
      if (lose) { lose = false; throw Error("lost"); }
      return hostedResult();
    });
    const app = createWorkbench(call, { evidenceMode: "hosted-transaction" });
    await expect(app.retrieve({ selection_plan_id: PLAN })).rejects.toThrow("Review");
    await app.select({ period: "2026-07" });
    await expect(app.retrieve({ selection_plan_id: PLAN })).rejects.toThrow("lost");
    await app.select({ period: "2026-07" });
    expect((await app.retrieve({ selection_plan_id: PLAN })).receiptId).toBe(RECEIPT);
    expect(call.mock.calls[1]?.[1]).toEqual(call.mock.calls[3]?.[1]);
    expect((await app.inspect({ receipt_id: RECEIPT })).value).toBe("142.7");
    expect(call.mock.calls[4]?.[0]).toBe("web216_cpih_inspect");
    await expect(app.select({ period: "2026-07", evidenceMode: "local-filesystem" })).rejects.toThrow();
  });
  it("allows an earlier hosted record under a later checkpoint without claiming the omitted chain is verified by the page", async () => {
    const raw = hostedResult("2026-01");
    raw.evidence.checkpoint.sequence = 2;
    raw.evidence.checkpoint.tail_event_id = contentId("web216-transactional-event", "3");
    const app = createWorkbench(async () => raw, { evidenceMode: "hosted-transaction" });
    const result = await app.inspect({ receipt_id: RECEIPT });
    expect(result.period).toBe("2026-01"); expect(result.value).toBe("139.4");
    expect(result.raw.evidence).toEqual(raw.evidence);
  });
  it("binds hosted record, duplicated receipt, event, period, store and checkpoint subset", async () => {
    const mutations: Array<(raw: ReturnType<typeof hostedResult>) => void> = [
      (raw) => { raw.evidence.receipt.receipt_id = contentId("evidence-receipt", "3"); },
      (raw) => { raw.evidence.record.receipt.outcome = "other"; },
      (raw) => { raw.evidence.record.period = "2026-01"; },
      (raw) => { raw.evidence.receipt.operation.period = "2026-01"; },
      (raw) => { raw.evidence.event.record_id = contentId("web216-transactional-record", "3"); },
      (raw) => { raw.evidence.event.receipt_id = contentId("evidence-receipt", "3"); },
      (raw) => { raw.evidence.event.store_id = contentId("web216-transactional-store", "3"); },
      (raw) => { raw.evidence.event.idempotency_key_sha256 = "3".repeat(64); },
      (raw) => { raw.evidence.event.recorded_at = "2026-09-14T19:00:00.000Z"; },
      (raw) => { raw.evidence.record.record_id = "not-a-record-id"; },
      (raw) => { raw.evidence.checkpoint.store_id = contentId("web216-transactional-store", "3"); },
      (raw) => { raw.evidence.checkpoint.checkpoint_id = "not-a-checkpoint"; },
      (raw) => { raw.evidence.checkpoint.tail_event_id = contentId("web216-transactional-event", "3"); },
      (raw) => { raw.evidence.checkpoint.sequence = 0; },
      (raw) => { raw.evidence.checkpoint.sequence = 2; },
      (raw) => { raw.evidence.event.sequence = 1.5; },
      (raw) => { raw.evidence.event.sequence = 0; },
      (raw) => { raw.evidence.event.sequence = 129; },
      (raw) => { raw.evidence.event.previous_event_id = raw.evidence.event.event_id; },
      (raw) => { raw.evidence.event.sequence = 2; raw.evidence.checkpoint.sequence = 2; },
      (raw) => { raw.result.series.base_year = 2020; },
      (raw) => { raw.result.series.cdid = "OTHER"; },
      (raw) => { raw.result.series.unit = "Percentage"; },
    ];
    for (const mutate of mutations) {
      const raw = hostedResult(); mutate(raw);
      const app = createWorkbench(async () => raw, { evidenceMode: "hosted-transaction" });
      await expect(app.inspect({ receipt_id: RECEIPT })).rejects.toThrow();
    }
  });
  it("rejects altered hosted storage limitations, boundary claims and receipt persistence claims", async () => {
    for (const key of Object.keys(hostedResult().evidence.storage_observation)) {
      const raw = hostedResult(); Reflect.set(raw.evidence.storage_observation, key, "altered");
      await expect(createWorkbench(async () => raw, { evidenceMode: "hosted-transaction" }).inspect({ receipt_id: RECEIPT })).rejects.toThrow();
    }
    const mutations: Array<(raw: ReturnType<typeof hostedResult>) => void> = [
      (raw) => { Reflect.set(raw.evidence.storage_observation, "current", true); },
      (raw) => { raw.boundary.attested = true; },
      (raw) => { raw.boundary.activated_supported_release = true; },
      (raw) => { raw.boundary.provider_egress = true; },
      (raw) => { raw.evidence.record.boundary.execution_authority = true; },
      (raw) => { raw.evidence.record.boundary.persistence = "persisted"; },
      (raw) => { raw.evidence.receipt.evidence.persistence = "persisted"; raw.evidence.record.receipt = structuredClone(raw.evidence.receipt); },
      (raw) => { raw.result.currency = "current"; },
    ];
    for (const mutate of mutations) {
      const raw = hostedResult(); mutate(raw);
      await expect(createWorkbench(async () => raw, { evidenceMode: "hosted-transaction" }).inspect({ receipt_id: RECEIPT })).rejects.toThrow();
    }
  });
  it("preserves hosted generation safeguards and exact requested period/receipt checks", async () => {
    let finish!: (value: ReturnType<typeof hostedResult>) => void;
    const app = createWorkbench(async (name) => name === "web216_cpih_select" ? rawPlan : new Promise((resolve) => { finish = resolve; }), { evidenceMode: "hosted-transaction" });
    await app.select({ period: "2026-07" });
    const pending = app.retrieve({ selection_plan_id: PLAN }); app.invalidateSelection(); finish(hostedResult());
    await expect(pending).rejects.toThrow("selection changed");
    const wrongMonth = createWorkbench(async (name) => name === "web216_cpih_select" ? rawPlan : hostedResult("2026-01"), { evidenceMode: "hosted-transaction" });
    await wrongMonth.select({ period: "2026-07" });
    await expect(wrongMonth.retrieve({ selection_plan_id: PLAN })).rejects.toThrow("returned period");
    const inspect = createWorkbench(async () => hostedResult(), { evidenceMode: "hosted-transaction" });
    await expect(inspect.inspect({ receipt_id: contentId("evidence-receipt", "3") })).rejects.toThrow("returned receipt");
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
