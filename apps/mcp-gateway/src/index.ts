export interface StageZeroRequest {
  readonly synthetic: boolean;
  readonly networkAccess: boolean;
}

export const gatewayMetadata = Object.freeze({
  product: "GIS AI GO",
  repository: "gis-ai-go",
  registryId: "io.github.chris-page-gov/gis-ai-go",
  protocolTarget: "2026-07-28",
  stage: 0,
  liveProviderCalls: false,
} as const);

export function assertStageZeroRequest(request: StageZeroRequest): typeof gatewayMetadata {
  if (!request.synthetic) {
    throw new Error("Stage 0 accepts synthetic requests only");
  }
  if (request.networkAccess) {
    throw new Error("Stage 0 forbids network and provider access");
  }
  return gatewayMetadata;
}
