import assert from "node:assert/strict";
import test from "node:test";
import { fromJsonSchema, type JsonSchemaType } from "@modelcontextprotocol/server";
import { MCP_CATALOGUE_INPUT_SCHEMAS, MCP_EVIDENCE_INPUT_SCHEMAS, MCP_PUBLIC_READ_INPUT_SCHEMAS } from "../src/mcp-server.js";
import { MCP_MAX_TOOL_INPUT_ELEMENTS } from "../src/mcp-constants.js";
import { WEB216_CPIH_INPUT_SCHEMAS } from "../src/web216-cpih-input-schemas.js";
import { SITES_PILOT_INPUTS } from "../src/sites-pilot-http.js";

type Schema = Record<string, any>;
function elements(value: unknown): number {
  if (Array.isArray(value)) return value.length + value.reduce((sum, v) => sum + elements(v), 0);
  if (value !== null && typeof value === "object") {
    const values = Object.values(value); return values.length + values.reduce<number>((sum, v) => sum + elements(v), 0);
  }
  return 0;
}
/** Conservative upper bound for the exact closed schema constructs used here.
 * A new unbounded or unsupported construct requires explicit review. */
function maximum(schema: Schema, root: Schema = schema, depth = 0): number {
  assert(depth <= 16, "Recursive input schema requires separate review");
  if (Object.hasOwn(schema, "const")) return elements(schema.const);
  if (schema.enum !== undefined) return Math.max(...schema.enum.map(elements));
  if (schema.$ref !== undefined) {
    assert.match(schema.$ref, /^#\/\$defs\/[^/]+$/u);
    const target = root.$defs[schema.$ref.slice("#/$defs/".length)]; assert(target);
    return maximum(target, root, depth + 1);
  }
  if (schema.oneOf !== undefined) return Math.max(...schema.oneOf.map((s: Schema) => maximum(s, root, depth + 1)));
  assert(schema.allOf === undefined && schema.anyOf === undefined && schema.patternProperties === undefined);
  if (schema.type === "object") {
    assert.equal(schema.additionalProperties, false);
    const values = Object.values(schema.properties) as Schema[];
    return values.length + values.reduce((sum, child) => sum + maximum(child, root, depth + 1), 0);
  }
  if (schema.type === "array") {
    assert(Number.isSafeInteger(schema.maxItems) && schema.maxItems >= 0);
    return schema.maxItems * (1 + maximum(schema.items, root, depth + 1));
  }
  assert(["string", "integer", "number", "boolean", "null"].includes(schema.type), "Unbounded input requires review");
  return 0;
}

test("every registered input schema fits the SDK limit at its full structural maximum", () => {
  const schemas = { ...MCP_CATALOGUE_INPUT_SCHEMAS, ...MCP_EVIDENCE_INPUT_SCHEMAS,
    ...MCP_PUBLIC_READ_INPUT_SCHEMAS, ...WEB216_CPIH_INPUT_SCHEMAS, ...SITES_PILOT_INPUTS };
  const bounds = Object.fromEntries(Object.entries(schemas).map(([name, schema]) => [name, maximum(schema)]));
  assert.deepEqual(bounds, {
    "catalogue.describe": 4, "catalogue.search": 76, "evidence.inspect": 3,
    "selection.resolve": 53, "data.query": 23,
    web216_cpih_select: 1, web216_cpih_query: 3, web216_cpih_inspect: 1,
    sites_capabilities: 0, sites_os_names: 2, sites_os_open_product: 1,
    sites_ons_areas: 2, sites_ons_cpih: 3, sites_evidence_inspect: 1,
  });
  assert.equal(MCP_MAX_TOOL_INPUT_ELEMENTS, 1_024);
  assert(Math.max(...Object.values(bounds)) < MCP_MAX_TOOL_INPUT_ELEMENTS);
});

test("largest catalogue input uses all allowed facets and array entries", async () => {
  const schema = MCP_CATALOGUE_INPUT_SCHEMAS["catalogue.search"] as Schema;
  const facets = Object.fromEntries(Object.entries(schema.properties.facets.properties as Record<string, Schema>)
    .map(([name, value]) => [name, value.items.enum ?? Array.from({ length: value.maxItems }, (_, i) => `tag${i}`)]));
  const input = { query: "synthetic", facets, limit: 100, cursor: "synthetic" };
  assert.equal(elements(input), 76);
  const validated = await fromJsonSchema(schema as JsonSchemaType)["~standard"].validate(input);
  assert.equal(validated.issues, undefined);
});
