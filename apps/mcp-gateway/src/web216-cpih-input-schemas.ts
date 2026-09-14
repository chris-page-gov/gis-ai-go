/** Closed, non-executable inputs shared by the separate local and hosted faces. */
import { canonicalJsonClone } from "@gis-ai-go/evidence";

type Schema = Readonly<Record<string, unknown>>;
const closed = (properties: Record<string, Schema>): Schema => ({
  type: "object", properties, required: Object.keys(properties), additionalProperties: false,
});
const text = (pattern: string, maxLength = 256): Schema => ({ type: "string", pattern, maxLength });
const period = { type: "string", enum: ["2026-01", "2026-07"] };
const key = text("^gis-ai-go:ik:v1:(?!0{64}$)[0-9a-f]{64}$", 80);

export const WEB216_CPIH_INPUT_SCHEMAS = canonicalJsonClone({
  web216_cpih_select: closed({ period }),
  web216_cpih_query: closed({
    period, selection_plan_id: text("^gis-ai-go:web216-cpih-selection-plan:sha256:[0-9a-f]{64}$"), idempotency_key: key,
  }),
  web216_cpih_inspect: { type: "object", oneOf: [
    closed({ receipt_id: text("^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$") }),
    closed({ idempotency_key: key }),
  ] },
} as const);
