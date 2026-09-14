import type { McpCall } from "./mcp-client";

export type Period = "2026-01" | "2026-07";
export interface Plan { readonly period: Period; readonly planId: string; readonly raw: Record<string, unknown>; }
export interface EvidenceResult {
  readonly period: Period; readonly value: string; readonly receiptId: string;
  readonly raw: Record<string, unknown>;
}
export function closed(input: unknown, keys: readonly string[]): Record<string, unknown> {
  if (input === null || typeof input !== "object" || Array.isArray(input) ||
      Object.keys(input).length !== keys.length || keys.some((key) => !Object.hasOwn(input, key))) throw new TypeError("Unexpected or missing fields.");
  return input as Record<string, unknown>;
}
export function period(input: unknown): Period {
  if (input !== "2026-01" && input !== "2026-07") throw new TypeError("Choose January or July 2026; latest and other months are not supported.");
  return input;
}
function object(input: unknown): Record<string, unknown> {
  if (input === null || typeof input !== "object" || Array.isArray(input)) throw new TypeError("Invalid MCP response.");
  return input as Record<string, unknown>;
}
function evidence(raw: Record<string, unknown>): EvidenceResult {
  const result = object(raw.result), observation = object(result.observation), material = object(raw.evidence);
  const series = object(result.series);
  const receipt = object(material.receipt), storage = object(material.storage), selected = period(result.period);
  // Server performs full source-material and durable-record verification. The page
  // checks its narrow display contract; this is not independent cryptographic attestation.
  if (raw.schema !== "gis-ai-go.web216-cpih-query-result.v1" ||
      result.state !== "validated-captured-observation" || result.provider_egress !== false ||
      series.cdid !== "L522" || series.dataset_id !== "MM23" || series.base_year !== 2015 ||
      series.unit !== "Index, base year = 100" ||
      storage.status !== "persisted" || typeof observation.value !== "string" ||
      !/^\d{1,3}\.\d$/.test(observation.value) || typeof receipt.receipt_id !== "string" ||
      !/^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/.test(receipt.receipt_id)) throw new Error("The returned evidence does not match the display contract.");
  return { period: selected, value: observation.value, receiptId: receipt.receipt_id, raw };
}
function newKey(): string {
  return `gis-ai-go:ik:v1:${Array.from(crypto.getRandomValues(new Uint8Array(32)), (byte) => byte.toString(16).padStart(2, "0")).join("")}`;
}
/** Manual controls and page tools use this one bounded controller. */
export function createWorkbench(call: McpCall) {
  let plan: Plan | undefined, busy = false, generation = 0;
  const keys = new Map<string, string>(); // At most the two admitted month plans.
  async function run<T>(operation: () => Promise<T>): Promise<T> {
    if (busy) throw new Error("An operation is already running. Wait for it or cancel it first.");
    busy = true;
    try { return await operation(); } finally { busy = false; }
  }
  return {
    invalidateSelection() { generation += 1; plan = undefined; },
    select: (input: unknown, signal?: AbortSignal) => run(async () => {
      const selected = period(closed(input, ["period"]).period);
      const started = ++generation;
      const raw = await call("web216_cpih_select", { period: selected }, signal);
      if (started !== generation) throw new Error("The chosen month changed while selection was running. Review it again.");
      if (raw.schema !== "gis-ai-go.web216-cpih-selection-plan.v1" ||
          object(raw.selection).period !== selected || object(raw.authority).grants_execution !== false ||
          typeof raw.plan_id !== "string" || !/^gis-ai-go:web216-cpih-selection-plan:sha256:[0-9a-f]{64}$/.test(raw.plan_id)) throw new Error("Invalid non-authorising selection plan.");
      // Keep the key when reselecting the same plan, including after a lost response.
      if (!keys.has(raw.plan_id)) keys.set(raw.plan_id, newKey());
      plan = { period: selected, planId: raw.plan_id, raw };
      return plan;
    }),
    retrieve: (input: unknown, signal?: AbortSignal) => run(async () => {
      const requested = closed(input, ["selection_plan_id"]).selection_plan_id;
      const selected = plan, started = generation;
      if (!selected || requested !== selected.planId) throw new Error("Review the exact selection on this page before retrieving it.");
      const key = keys.get(selected.planId);
      if (!key) throw new Error("The request key is unavailable.");
      const result = evidence(await call("web216_cpih_query", { period: selected.period, selection_plan_id: selected.planId, idempotency_key: key }, signal));
      if (result.period !== selected.period) throw new Error("The returned period does not match the selection.");
      if (generation !== started) throw new Error("The selection changed. A receipt may already exist; review the original month to replay it.");
      return result;
    }),
    inspect: (input: unknown, signal?: AbortSignal) => run(async () => {
      const receiptId = closed(input, ["receipt_id"]).receipt_id;
      if (typeof receiptId !== "string" || !/^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/.test(receiptId)) throw new Error("Use an exact receipt ID returned by this experiment.");
      const result = evidence(await call("web216_cpih_inspect", { receipt_id: receiptId }, signal));
      if (result.receiptId !== receiptId) throw new Error("The returned receipt does not match the requested receipt.");
      return result;
    }),
  };
}
