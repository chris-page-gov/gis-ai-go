import { catalogueActivation } from "./activation.js";

export const gatewayMetadata = Object.freeze({
  product: "GIS AI GO",
  repository: "chris-page-gov/gis-ai-go",
  registryId: "io.github.chris-page-gov/gis-ai-go",
  version: "0.1.0",
  protocolTarget: "2026-07-28",
  lifecycle: "candidate-blocked",
  liveProviderCalls: false,
  activeTools: catalogueActivation.activeTools,
  activeApiOperations: catalogueActivation.activeApiOperations,
} as const);
