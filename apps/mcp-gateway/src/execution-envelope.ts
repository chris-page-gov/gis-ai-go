import {
  type ExecutionLimits,
  type ExecutionRequest,
  type ExecutionResult,
  type ExecutionTrace,
  type Polygon,
  type SyntheticFeature,
  type SyntheticSource,
} from "@gis-ai-go/contracts";
import { CANONICAL_DOMAINS, domainSeparatedSha256 } from "@gis-ai-go/evidence";
import { normaliseW3CTraceContext } from "@gis-ai-go/provider-adapter-sdk";

const IDENTIFIER = /^[a-z0-9][a-z0-9._:-]{0,127}$/u;
const SHA256 = /^sha256:[0-9a-f]{64}$/u;
const FEATURE_ID = /^SYN-[0-9]{3}$/u;
const RFC3339 = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/u;

function executionDigest(domain: string, value: unknown): `sha256:${string}` {
  return `sha256:${domainSeparatedSha256(domain, value)}`;
}

export const SYNTHETIC_EXECUTION_SOURCE = Object.freeze({
  provider_id: "gis-ai-go.synthetic-fixture",
  dataset_id: "synthetic-gb-places",
  version: "1.0.0",
  rights: "CC0-1.0",
  source_uri: "urn:gis-ai-go:fixture:synthetic-gb-places:1",
} as const satisfies SyntheticSource);

export interface SyntheticExecutionRequestInput {
  readonly request_id: string;
  readonly trace: ExecutionTrace;
  readonly decision_id: string;
  readonly decision_digest: `sha256:${string}`;
  readonly deadline: string;
  readonly limits: ExecutionLimits;
  readonly geometry: Polygon;
  readonly limit: number;
}

type ObjectValue = Record<string, unknown>;

function fail(message: string): never {
  throw new Error(`Invalid private execution envelope: ${message}`);
}

function objectAt(value: unknown, expected: readonly string[], label: string): ObjectValue {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    fail(`${label} must be an object`);
  }
  const result = value as ObjectValue;
  const actual = Object.keys(result).sort();
  const required = [...expected].sort();
  if (actual.length !== required.length || actual.some((key, index) => key !== required[index])) {
    fail(`${label} has an unknown or missing field`);
  }
  return result;
}

function integerAt(value: unknown, minimum: number, maximum: number, label: string): number {
  if (!Number.isSafeInteger(value) || (value as number) < minimum || (value as number) > maximum) {
    fail(`${label} is outside the permitted integer range`);
  }
  return value as number;
}

function literalAt<T extends string>(value: unknown, expected: T, label: string): T {
  if (value !== expected) fail(`${label} does not match the contract`);
  return expected;
}

function identifierAt(value: unknown, label: string): string {
  if (typeof value !== "string" || !IDENTIFIER.test(value)) {
    fail(`${label} is not a bounded identifier`);
  }
  return value;
}

function traceAt(value: unknown): ExecutionTrace {
  try {
    return normaliseW3CTraceContext(value);
  } catch (error) {
    fail(error instanceof Error ? error.message : "trace is invalid");
  }
}

function limitsAt(value: unknown): ExecutionLimits {
  const limits = objectAt(
    value,
    [
      "max_features",
      "max_coordinates",
      "max_input_bytes",
      "max_output_bytes",
      "max_complexity",
    ],
    "limits",
  );
  return {
    max_features: integerAt(limits.max_features, 1, 100, "max_features"),
    max_coordinates: integerAt(limits.max_coordinates, 4, 128, "max_coordinates"),
    max_input_bytes: integerAt(limits.max_input_bytes, 1_024, 65_536, "max_input_bytes"),
    max_output_bytes: integerAt(
      limits.max_output_bytes,
      1_024,
      262_144,
      "max_output_bytes",
    ),
    max_complexity: integerAt(limits.max_complexity, 16, 20_000, "max_complexity"),
  };
}

function positionAt(value: unknown, label: string): readonly [number, number] {
  if (!Array.isArray(value) || value.length !== 2) fail(`${label} is not a position`);
  const longitude = value[0];
  const latitude = value[1];
  if (
    typeof longitude !== "number" ||
    typeof latitude !== "number" ||
    !Number.isFinite(longitude) ||
    !Number.isFinite(latitude) ||
    longitude < -180 ||
    longitude > 180 ||
    latitude < -90 ||
    latitude > 90
  ) {
    fail(`${label} is outside EPSG 4326 longitude latitude bounds`);
  }
  return [longitude, latitude];
}

function polygonAt(value: unknown, maximum: number): Polygon {
  const polygon = objectAt(value, ["type", "coordinates"], "geometry");
  literalAt(polygon.type, "Polygon", "geometry type");
  if (!Array.isArray(polygon.coordinates) || polygon.coordinates.length !== 1) {
    fail("geometry must have one outer ring");
  }
  const rawRing = polygon.coordinates[0];
  if (!Array.isArray(rawRing) || rawRing.length < 4 || rawRing.length > maximum) {
    fail("geometry coordinate count is outside the limit");
  }
  const ring = rawRing.map((position, index) => positionAt(position, `geometry[${index}]`));
  const first = ring[0];
  const last = ring.at(-1);
  if (first === undefined || last === undefined || first[0] !== last[0] || first[1] !== last[1]) {
    fail("geometry ring is not closed");
  }
  return { type: "Polygon", coordinates: [ring] };
}

/**
 * Construct the only gateway-to-Python request currently allowed.
 *
 * The gateway assertion is deliberately not a credential. Python verifies this
 * closed hand-off but does not authenticate an end user or make a policy decision.
 */
export function buildSyntheticExecutionRequest(
  value: unknown,
  now: Date = new Date(),
): ExecutionRequest {
  const input = objectAt(
    value,
    [
      "request_id",
      "trace",
      "decision_id",
      "decision_digest",
      "deadline",
      "limits",
      "geometry",
      "limit",
    ],
    "request input",
  );
  const limits = limitsAt(input.limits);
  const deadline =
    typeof input.deadline === "string" && RFC3339.test(input.deadline)
      ? Date.parse(input.deadline)
      : Number.NaN;
  if (
    !Number.isFinite(deadline) ||
    deadline <= now.getTime() ||
    deadline - now.getTime() > 30_000
  ) {
    fail("deadline is outside the thirty second execution window");
  }
  if (typeof input.decision_digest !== "string" || !SHA256.test(input.decision_digest)) {
    fail("decision digest is invalid");
  }
  const limit = integerAt(input.limit, 1, limits.max_features, "feature limit");
  const request: ExecutionRequest = {
    schema: "gis-ai-go.execution-request.v1",
    request_id: identifierAt(input.request_id, "request identifier"),
    operation: "fixture.features.query",
    trace: traceAt(input.trace),
    gateway_authorisation: {
      schema: "gis-ai-go.gateway-authorisation.v1",
      decision_id: identifierAt(input.decision_id, "decision identifier"),
      decision_digest: input.decision_digest as `sha256:${string}`,
      permitted_operation: "fixture.features.query",
    },
    deadline: input.deadline as string,
    limits,
    parameters: {
      fixture_id: "synthetic-gb-places-v1",
      source: SYNTHETIC_EXECUTION_SOURCE,
      crs: "EPSG:4326",
      axis_order: "longitude-latitude",
      geometry: polygonAt(input.geometry, limits.max_coordinates),
      limit,
    },
  };
  const segmentCount = request.parameters.geometry.coordinates[0].length - 1;
  if (segmentCount ** 2 + 5 > limits.max_complexity) {
    fail("geometry exceeds the gateway complexity limit");
  }
  if (new TextEncoder().encode(JSON.stringify(request)).length > limits.max_input_bytes) {
    fail("request exceeds the gateway input byte limit");
  }
  return structuredClone(request);
}

function sourceAt(value: unknown, request: ExecutionRequest): SyntheticSource {
  const source = objectAt(
    value,
    ["provider_id", "dataset_id", "version", "rights", "source_uri"],
    "source evidence",
  );
  for (const [key, expected] of Object.entries(request.parameters.source)) {
    if (source[key] !== expected) fail("source evidence does not match the gateway selection");
  }
  return structuredClone(request.parameters.source);
}

function featureAt(value: unknown, index: number): SyntheticFeature {
  const feature = objectAt(value, ["type", "id", "geometry", "properties"], `feature ${index}`);
  literalAt(feature.type, "Feature", `feature ${index} type`);
  if (typeof feature.id !== "string" || !FEATURE_ID.test(feature.id)) {
    fail(`feature ${index} identifier is invalid`);
  }
  const geometry = objectAt(feature.geometry, ["type", "coordinates"], `feature ${index} geometry`);
  literalAt(geometry.type, "Point", `feature ${index} geometry type`);
  const properties = objectAt(
    feature.properties,
    ["native_id", "name", "category"],
    `feature ${index} properties`,
  );
  if (properties.native_id !== feature.id) fail(`feature ${index} native identifier differs`);
  if (
    typeof properties.name !== "string" ||
    properties.name.length < 1 ||
    properties.name.length > 80
  ) {
    fail(`feature ${index} name is invalid`);
  }
  literalAt(properties.category, "synthetic-place", `feature ${index} category`);
  return {
    type: "Feature",
    id: feature.id,
    geometry: { type: "Point", coordinates: positionAt(geometry.coordinates, `feature ${index}`) },
    properties: {
      native_id: feature.id,
      name: properties.name,
      category: "synthetic-place",
    },
  };
}

/** Validate and detach the untrusted Python result before the gateway uses it. */
export function parseExecutionResult(value: unknown, request: ExecutionRequest): ExecutionResult {
  const result = objectAt(
    value,
    ["schema", "request_id", "operation", "status", "trace", "data", "evidence"],
    "result",
  );
  literalAt(result.schema, "gis-ai-go.execution-result.v1", "result schema");
  if (result.request_id !== request.request_id) fail("result request identifier differs");
  literalAt(result.operation, "fixture.features.query", "result operation");
  literalAt(result.status, "succeeded", "result status");
  const trace = traceAt(result.trace);
  if (JSON.stringify(trace) !== JSON.stringify(request.trace)) fail("result trace differs");

  const data = objectAt(result.data, ["type", "crs", "axis_order", "features"], "result data");
  literalAt(data.type, "FeatureCollection", "result data type");
  literalAt(data.crs, "EPSG:4326", "result CRS");
  literalAt(data.axis_order, "longitude-latitude", "result axis order");
  if (
    !Array.isArray(data.features) ||
    data.features.length > request.limits.max_features ||
    data.features.length > request.parameters.limit
  ) {
    fail("result feature count exceeds the request limit");
  }
  const features = data.features.map(featureAt);
  const identifiers = features.map((feature) => feature.id);
  const sortedIdentifiers = [...identifiers].sort();
  if (
    new Set(identifiers).size !== identifiers.length ||
    identifiers.some((identifier, index) => identifier !== sortedIdentifiers[index])
  ) {
    fail("result feature identifiers are duplicated or not canonical");
  }
  const parsedData = {
    type: "FeatureCollection" as const,
    crs: "EPSG:4326" as const,
    axis_order: "longitude-latitude" as const,
    features,
  };

  const evidence = objectAt(
    result.evidence,
    [
      "schema",
      "input_sha256",
      "output_sha256",
      "feature_count",
      "source",
      "transformation",
      "software",
    ],
    "result evidence",
  );
  literalAt(evidence.schema, "gis-ai-go.execution-evidence.v1", "evidence schema");
  if (
    typeof evidence.input_sha256 !== "string" ||
    !SHA256.test(evidence.input_sha256) ||
    typeof evidence.output_sha256 !== "string" ||
    !SHA256.test(evidence.output_sha256)
  ) {
    fail("evidence digest is invalid");
  }
  const inputSha256 = executionDigest(
    CANONICAL_DOMAINS.executionParameters,
    request.parameters,
  );
  if (evidence.input_sha256 !== inputSha256) {
    fail("evidence input digest does not match the request parameters");
  }
  const outputSha256 = executionDigest(CANONICAL_DOMAINS.executionResultData, parsedData);
  if (evidence.output_sha256 !== outputSha256) {
    fail("evidence output digest does not match the result data");
  }
  if (evidence.feature_count !== features.length) fail("evidence feature count differs");
  const source = sourceAt(evidence.source, request);
  const transformation = objectAt(
    evidence.transformation,
    [
      "operation",
      "source_crs",
      "source_axis_order",
      "output_crs",
      "output_axis_order",
      "geometry_repair",
      "geometry_simplification",
    ],
    "transformation evidence",
  );
  literalAt(transformation.operation, "synthetic-point-in-polygon-v1", "transformation");
  literalAt(transformation.source_crs, "EPSG:4326", "source CRS evidence");
  literalAt(transformation.source_axis_order, "longitude-latitude", "source axis evidence");
  literalAt(transformation.output_crs, "EPSG:4326", "output CRS evidence");
  literalAt(transformation.output_axis_order, "longitude-latitude", "output axis evidence");
  literalAt(transformation.geometry_repair, "none", "repair evidence");
  literalAt(transformation.geometry_simplification, "none", "simplification evidence");
  const software = objectAt(
    evidence.software,
    ["name", "version", "algorithm"],
    "software evidence",
  );
  literalAt(software.name, "gis-ai-go-execution", "software name");
  literalAt(software.version, "0.1.0", "software version");
  literalAt(software.algorithm, "synthetic-point-in-polygon-v1", "software algorithm");

  const parsed: ExecutionResult = {
    schema: "gis-ai-go.execution-result.v1",
    request_id: request.request_id,
    operation: "fixture.features.query",
    status: "succeeded",
    trace,
    data: parsedData,
    evidence: {
      schema: "gis-ai-go.execution-evidence.v1",
      input_sha256: inputSha256,
      output_sha256: outputSha256,
      feature_count: features.length,
      source,
      transformation: {
        operation: "synthetic-point-in-polygon-v1",
        source_crs: "EPSG:4326",
        source_axis_order: "longitude-latitude",
        output_crs: "EPSG:4326",
        output_axis_order: "longitude-latitude",
        geometry_repair: "none",
        geometry_simplification: "none",
      },
      software: {
        name: "gis-ai-go-execution",
        version: "0.1.0",
        algorithm: "synthetic-point-in-polygon-v1",
      },
    },
  };
  if (new TextEncoder().encode(JSON.stringify(parsed)).length > request.limits.max_output_bytes) {
    fail("result exceeds the gateway output limit");
  }
  return structuredClone(parsed);
}
