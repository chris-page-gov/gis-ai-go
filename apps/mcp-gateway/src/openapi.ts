import openApiDocument from "../openapi/catalogue-api.openapi.json" with { type: "json" };

export type OpenApiDocument = Readonly<typeof openApiDocument>;

function deepFreeze<T>(value: T, seen = new WeakSet<object>()): T {
  if (value === null || typeof value !== "object" || seen.has(value)) return value;
  seen.add(value);
  for (const child of Object.values(value as Record<string, unknown>)) {
    deepFreeze(child, seen);
  }
  return Object.freeze(value);
}

export const catalogueOpenApiDocument: OpenApiDocument = deepFreeze(openApiDocument);
