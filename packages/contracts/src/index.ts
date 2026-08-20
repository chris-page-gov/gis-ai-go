export const contractMetadata = Object.freeze({
  product: "GIS AI GO",
  contractVersion: 1,
  lifecycle: "v0.2-foundation",
  schemaNamespace: "urn:gis-ai-go:schema",
} as const);

export * from "./catalogue/index.js";
export * from "./execution/index.js";
