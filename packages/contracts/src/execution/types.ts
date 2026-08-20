export const EXECUTION_OPERATIONS = ["fixture.features.query"] as const;
export type ExecutionOperation = (typeof EXECUTION_OPERATIONS)[number];

export interface ExecutionTrace {
  readonly traceparent: string;
  readonly tracestate?: string;
}

export interface GatewayAuthorisation {
  readonly schema: "gis-ai-go.gateway-authorisation.v1";
  readonly decision_id: string;
  readonly decision_digest: `sha256:${string}`;
  readonly permitted_operation: ExecutionOperation;
}

export interface ExecutionLimits {
  readonly max_features: number;
  readonly max_coordinates: number;
  readonly max_input_bytes: number;
  readonly max_output_bytes: number;
  readonly max_complexity: number;
}

export interface SyntheticSource {
  readonly provider_id: "gis-ai-go.synthetic-fixture";
  readonly dataset_id: "synthetic-gb-places";
  readonly version: "1.0.0";
  readonly rights: "CC0-1.0";
  readonly source_uri: "urn:gis-ai-go:fixture:synthetic-gb-places:1";
}

export type Position = readonly [longitude: number, latitude: number];

export interface Polygon {
  readonly type: "Polygon";
  readonly coordinates: readonly [readonly Position[]];
}

export interface SyntheticFixtureParameters {
  readonly fixture_id: "synthetic-gb-places-v1";
  readonly source: SyntheticSource;
  readonly crs: "EPSG:4326";
  readonly axis_order: "longitude-latitude";
  readonly geometry: Polygon;
  readonly limit: number;
}

export interface ExecutionRequest {
  readonly schema: "gis-ai-go.execution-request.v1";
  readonly request_id: string;
  readonly operation: "fixture.features.query";
  readonly trace: ExecutionTrace;
  readonly gateway_authorisation: GatewayAuthorisation;
  readonly deadline: string;
  readonly limits: ExecutionLimits;
  readonly parameters: SyntheticFixtureParameters;
}

export interface SyntheticFeature {
  readonly type: "Feature";
  readonly id: string;
  readonly geometry: {
    readonly type: "Point";
    readonly coordinates: Position;
  };
  readonly properties: {
    readonly native_id: string;
    readonly name: string;
    readonly category: "synthetic-place";
  };
}

export interface ExecutionResult {
  readonly schema: "gis-ai-go.execution-result.v1";
  readonly request_id: string;
  readonly operation: "fixture.features.query";
  readonly status: "succeeded";
  readonly trace: ExecutionTrace;
  readonly data: {
    readonly type: "FeatureCollection";
    readonly crs: "EPSG:4326";
    readonly axis_order: "longitude-latitude";
    readonly features: readonly SyntheticFeature[];
  };
  readonly evidence: {
    readonly schema: "gis-ai-go.execution-evidence.v1";
    readonly input_sha256: `sha256:${string}`;
    readonly output_sha256: `sha256:${string}`;
    readonly feature_count: number;
    readonly source: SyntheticSource;
    readonly transformation: {
      readonly operation: "synthetic-point-in-polygon-v1";
      readonly source_crs: "EPSG:4326";
      readonly source_axis_order: "longitude-latitude";
      readonly output_crs: "EPSG:4326";
      readonly output_axis_order: "longitude-latitude";
      readonly geometry_repair: "none";
      readonly geometry_simplification: "none";
    };
    readonly software: {
      readonly name: "gis-ai-go-execution";
      readonly version: "0.1.0";
      readonly algorithm: "synthetic-point-in-polygon-v1";
    };
  };
}

export const EXECUTION_PROBLEM_CODES = [
  "INVALID_REQUEST",
  "NOT_FOUND",
  "METHOD_NOT_ALLOWED",
  "UNKNOWN_OPERATION",
  "SOURCE_MISMATCH",
  "INVALID_CRS",
  "INVALID_AXIS_ORDER",
  "INVALID_GEOMETRY",
  "LIMIT_EXCEEDED",
  "DEADLINE_EXCEEDED",
  "EXECUTION_CANCELLED",
  "OUTPUT_LIMIT_EXCEEDED",
  "CAPACITY_EXCEEDED",
  "INTERNAL_ERROR",
] as const;
export type ExecutionProblemCode = (typeof EXECUTION_PROBLEM_CODES)[number];

export interface ExecutionProblem {
  readonly schema: "gis-ai-go.execution-problem.v1";
  readonly request_id: string | null;
  readonly trace: ExecutionTrace | null;
  readonly status: 400 | 404 | 405 | 408 | 409 | 413 | 422 | 429 | 500;
  readonly code: ExecutionProblemCode;
  readonly title: string;
  readonly detail: string;
  readonly retryable: boolean;
}
