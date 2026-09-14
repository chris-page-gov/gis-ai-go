/** Experimental capture selection: a plan is never an execution permission. */
import {
  canonicalJsonClone,
  contentAddress,
  PUBLIC_IDEMPOTENCY_KEY,
  WEB216_CPIH_CAPTURE,
  type Web216CpihPeriod,
} from "@gis-ai-go/evidence";

const PLAN_DOMAIN = "gis-ai-go.web216-cpih-selection-plan.v1";

export class Web216CpihSelectionError extends TypeError {
  public readonly code = "invalid-experimental-selection";
  public constructor() {
    super("Use an explicitly supported CPIH period and its exact non-authorising selection plan");
    this.name = "Web216CpihSelectionError";
  }
}

function reject(): never { throw new Web216CpihSelectionError(); }

function closed(value: unknown, keys: readonly string[]): Record<string, unknown> {
  let snapshot: unknown;
  try { snapshot = canonicalJsonClone(value); } catch { return reject(); }
  if (snapshot === null || typeof snapshot !== "object" || Array.isArray(snapshot)) reject();
  const object = snapshot as Record<string, unknown>;
  if (Object.keys(object).length !== keys.length || keys.some((key) => !Object.hasOwn(object, key))) reject();
  return object;
}

function supportedPeriod(value: unknown): Web216CpihPeriod {
  if (value !== "2026-01" && value !== "2026-07") reject();
  return value;
}

function planFor(period: Web216CpihPeriod) {
  const core = canonicalJsonClone({
    schema: "gis-ai-go.web216-cpih-selection-plan.v1",
    nature: "proposal-not-execution-authority",
    resource: {
      source_qualified_id: "ons-timeseries:L522:MM23",
      cdid: "L522",
      dataset_id: "MM23",
      uri: "/economy/inflationandpriceindices/timeseries/l522/mm23",
      capture_projection_sha256: WEB216_CPIH_CAPTURE.projection_sha256,
      captured_at: WEB216_CPIH_CAPTURE.captured_at,
      public_page: WEB216_CPIH_CAPTURE.urls.public_page,
    },
    selection: { period },
    measure: { kind: "index-not-percentage", unit: "Index, base year = 100", base_year: 2015 },
    proposed_transformation: "read-validated-cpih-capture",
    observation_limit: 1,
    authority: {
      grants_execution: false,
      grants_provider_permission: false,
      requires_active_experimental_assembly: true,
      requires_independent_query_policy_check: true,
      requires_verified_capture_material: true,
      requires_durable_receipt: true,
    },
    currency: "captured-data-not-live-or-always-current",
  } as const);
  return canonicalJsonClone({
    ...core,
    plan_id: contentAddress("gis-ai-go:web216-cpih-selection-plan", PLAN_DOMAIN, core),
  });
}

export type Web216CpihSelectionPlan = ReturnType<typeof planFor>;

/** No provider call, material read, policy decision or receipt is performed here. */
export function resolveWeb216CpihSelection(input: unknown): Web216CpihSelectionPlan {
  const request = closed(input, ["period"]);
  return planFor(supportedPeriod(request.period));
}

export interface Web216CpihQueryProposal {
  readonly period: Web216CpihPeriod;
  readonly selection_plan_id: string;
  /** Correlation input only: never retain this raw value in a receipt or public log. */
  readonly idempotency_key: string;
}

/**
 * Checks proposal consistency, not permission. The query application must still
 * check its private assembly binding, admitted material, policy and evidence store.
 */
export function normaliseWeb216CpihQueryProposal(input: unknown): Web216CpihQueryProposal {
  const request = closed(input, ["period", "selection_plan_id", "idempotency_key"]);
  const period = supportedPeriod(request.period);
  if (request.selection_plan_id !== planFor(period).plan_id ||
      typeof request.idempotency_key !== "string" || !PUBLIC_IDEMPOTENCY_KEY.test(request.idempotency_key) ||
      request.idempotency_key === `gis-ai-go:ik:v1:${"0".repeat(64)}`) {
    reject();
  }
  return canonicalJsonClone({
    period,
    selection_plan_id: request.selection_plan_id,
    idempotency_key: request.idempotency_key,
  });
}
