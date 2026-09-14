import type { McpCall } from "./mcp-client";

export type Period = "2026-01" | "2026-07";
export type EvidenceMode = "local-filesystem" | "hosted-transaction";
export interface WorkbenchOptions { readonly evidenceMode?: EvidenceMode; }
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
function constructionMode(options: WorkbenchOptions): EvidenceMode {
  if (options === null || typeof options !== "object" || Object.getPrototypeOf(options) !== Object.prototype) throw new TypeError("Invalid workbench construction options.");
  const keys = Reflect.ownKeys(options);
  if (keys.length === 0) return "local-filesystem";
  const descriptor = Object.getOwnPropertyDescriptor(options, "evidenceMode");
  if (keys.length !== 1 || keys[0] !== "evidenceMode" || !descriptor ||
      !("value" in descriptor) || descriptor.enumerable !== true ||
      (descriptor.value !== "local-filesystem" && descriptor.value !== "hosted-transaction")) throw new TypeError("Invalid workbench construction options.");
  return descriptor.value;
}
function identity(value: unknown, family: string): boolean {
  return typeof value === "string" && new RegExp(`^gis-ai-go:${family}:sha256:[0-9a-f]{64}$`).test(value);
}
function sameJson(left: unknown, right: unknown): boolean {
  if (left === right) return true;
  if (left === null || right === null || typeof left !== "object" || typeof right !== "object" ||
      Array.isArray(left) !== Array.isArray(right)) return false;
  const a = left as Record<string, unknown>, b = right as Record<string, unknown>;
  const keys = Object.keys(a);
  return keys.length === Object.keys(b).length && keys.every((key) => Object.hasOwn(b, key) && sameJson(a[key], b[key]));
}
function exactValues(input: unknown, values: Record<string, unknown>): void {
  const value = closed(input, Object.keys(values));
  if (Object.entries(values).some(([key, expected]) => value[key] !== expected)) throw new Error("The returned evidence does not match the display contract.");
}
function hostedEvidence(raw: Record<string, unknown>, selected: Period): void {
  closed(raw, ["schema", "result", "evidence", "boundary"]);
  const material = closed(raw.evidence, ["receipt", "record", "event", "checkpoint", "storage_observation"]);
  const receipt = object(material.receipt), operation = object(receipt.operation), result = object(raw.result);
  const record = closed(material.record, ["schema", "store_id", "idempotency_key_sha256", "request_fingerprint_sha256",
    "period", "recorded_at", "retain_until", "receipt", "verification", "boundary", "record_id"]);
  const event = closed(material.event, ["schema", "store_id", "sequence", "previous_event_id", "record_id", "receipt_id",
    "idempotency_key_sha256", "recorded_at", "event_id"]);
  const head = closed(material.checkpoint, ["schema", "store_id", "sequence", "tail_event_id", "checkpoint_id"]);
  const sequence = event.sequence, headSequence = head.sequence;
  const hash = (value: unknown) => typeof value === "string" && /^[0-9a-f]{64}$/.test(value);
  if (result.schema !== "gis-ai-go.web216-cpih-result-core.v1" || result.currency !== "as-of-recorded-capture-not-always-current" ||
      receipt.schema !== "gis-ai-go.web216-cpih-receipt.v1" || receipt.outcome !== "success" ||
      receipt.execution_scope !== "experimental-pinned-capture-read-not-live-provider-evidence" ||
      operation.name !== "read-validated-cpih-capture" || operation.contract_version !== "v1" || operation.period !== selected ||
      record.schema !== "gis-ai-go.web216-transactional-record.v1" || record.period !== selected ||
      record.verification !== "full-material-verified-model-record" || !sameJson(receipt, record.receipt) ||
      !identity(record.store_id, "web216-transactional-store") || !identity(record.record_id, "web216-transactional-record") ||
      !hash(record.idempotency_key_sha256) || !hash(record.request_fingerprint_sha256) ||
      typeof record.recorded_at !== "string" || typeof record.retain_until !== "string" ||
      event.schema !== "gis-ai-go.web216-transactional-event.v1" || !identity(event.event_id, "web216-transactional-event") ||
      event.store_id !== record.store_id || event.record_id !== record.record_id || event.receipt_id !== receipt.receipt_id ||
      event.idempotency_key_sha256 !== record.idempotency_key_sha256 || event.recorded_at !== record.recorded_at ||
      head.schema !== "gis-ai-go.web216-transactional-head.v1" || head.store_id !== record.store_id ||
      !identity(head.checkpoint_id, "web216-transactional-checkpoint") || !identity(head.tail_event_id, "web216-transactional-event") ||
      typeof sequence !== "number" || !Number.isInteger(sequence) || sequence < 1 || sequence > 128 ||
      typeof headSequence !== "number" || !Number.isInteger(headSequence) || headSequence < sequence || headSequence > 128 ||
      (sequence === 1 ? event.previous_event_id !== null : !identity(event.previous_event_id, "web216-transactional-event")) ||
      event.previous_event_id === event.event_id ||
      (headSequence === sequence ? head.tail_event_id !== event.event_id : head.tail_event_id === event.event_id)) throw new Error("The returned evidence does not match the display contract.");
  exactValues(material.storage_observation, {
    schema: "gis-ai-go.web216-hosted-storage-observation.v1", persistence: "present-in-verified-adapter-snapshot",
    checkpoint_scope: "verified-returned-snapshot", read_freshness: "not-established-by-application", store_id: record.store_id,
    integrity: "full-snapshot-content-and-chain-verified-internally", returned_evidence_scope: "selected-record-event-and-head-subset",
    attestation: "not-attested", independent_rollback_anchor: false, disaster_recovery: "not-established", deployment: "not-established-by-application",
  });
  exactValues(raw.boundary, { provider_egress: false, activated_supported_release: false, attested: false });
  exactValues(record.boundary, { persistence: "not-established-by-contract", attestation: "not-attested", provider_egress: false, execution_authority: false });
  exactValues(receipt.evidence, { delivery: "inline-only", persistence: "not-persisted", attestation: "not-attested" });
  // Only the selected record/event and current head are returned. This checks
  // their display links, not intervening events, content hashes, full-chain
  // integrity, an independent rollback anchor, read freshness or attestation.
}
function evidence(raw: Record<string, unknown>, mode: EvidenceMode): EvidenceResult {
  const result = object(raw.result), observation = object(result.observation), material = object(raw.evidence);
  const series = object(result.series);
  const receipt = object(material.receipt), selected = period(result.period);
  // Server performs full source-material and durable-record verification. The page
  // checks its narrow display contract; this is not independent cryptographic attestation.
  const schema = mode === "local-filesystem" ? "gis-ai-go.web216-cpih-query-result.v1" : "gis-ai-go.web216-hosted-cpih-result.v1";
  if (raw.schema !== schema ||
      result.state !== "validated-captured-observation" || result.provider_egress !== false ||
      series.cdid !== "L522" || series.dataset_id !== "MM23" || series.base_year !== 2015 ||
      series.unit !== "Index, base year = 100" ||
      typeof observation.value !== "string" ||
      !/^\d{1,3}\.\d$/.test(observation.value) || typeof receipt.receipt_id !== "string" ||
      !/^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/.test(receipt.receipt_id)) throw new Error("The returned evidence does not match the display contract.");
  if (mode === "hosted-transaction") hostedEvidence(raw, selected);
  else if (object(material.storage).status !== "persisted" || Object.hasOwn(material, "storage_observation") ||
      Object.hasOwn(material, "checkpoint") ||
      (Object.hasOwn(material, "record") && object(material.record).schema !== "gis-ai-go.public-evidence-record.v3") ||
      (Object.hasOwn(material, "event") && object(material.event).schema !== "gis-ai-go.evidence-ledger-event.v1")) throw new Error("The returned evidence does not match the display contract.");
  return { period: selected, value: observation.value, receiptId: receipt.receipt_id, raw };
}
function newKey(): string {
  return `gis-ai-go:ik:v1:${Array.from(crypto.getRandomValues(new Uint8Array(32)), (byte) => byte.toString(16).padStart(2, "0")).join("")}`;
}
/** Manual controls and page tools use this one bounded controller. */
export function createWorkbench(call: McpCall, options: WorkbenchOptions = {}) {
  const evidenceMode = constructionMode(options); // Never inferred from a response or tool arguments.
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
      const result = evidence(await call("web216_cpih_query", { period: selected.period, selection_plan_id: selected.planId, idempotency_key: key }, signal), evidenceMode);
      if (result.period !== selected.period) throw new Error("The returned period does not match the selection.");
      if (generation !== started) throw new Error("The selection changed. A receipt may already exist; review the original month to replay it.");
      return result;
    }),
    inspect: (input: unknown, signal?: AbortSignal) => run(async () => {
      const receiptId = closed(input, ["receipt_id"]).receipt_id;
      if (typeof receiptId !== "string" || !/^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$/.test(receiptId)) throw new Error("Use an exact receipt ID returned by this experiment.");
      const result = evidence(await call("web216_cpih_inspect", { receipt_id: receiptId }, signal), evidenceMode);
      if (result.receiptId !== receiptId) throw new Error("The returned receipt does not match the requested receipt.");
      return result;
    }),
  };
}
