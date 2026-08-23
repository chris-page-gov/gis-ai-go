import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { CANONICAL_DOMAINS, domainSeparatedSha256 } from "@gis-ai-go/evidence";

import {
  buildSyntheticExecutionRequest,
  parseExecutionResult,
} from "../src/execution-envelope.js";

function fixture(name: string): unknown {
  return JSON.parse(
    readFileSync(new URL(`../../../../providers/fixtures/${name}`, import.meta.url), "utf-8"),
  ) as unknown;
}

const NOW = new Date("2026-08-20T12:00:00Z");
const DIGEST_PARITY_VALUE = {
  unicode: "Café 😀",
  integer: 9_007_199_254_740_991,
  decimal: 333333333.33333329,
  exponent_large: 1e30,
  exponent_small: 1e-7,
  fixed_small: 1e-6,
  negative_zero: -0,
};
const DIGEST_PARITY_INPUT =
  "4afb2bfe5ee293d98a8525f34418c79011251e30f94a8dfecac0fb93e3841a48";
const DIGEST_PARITY_OUTPUT =
  "f89af91ec033f5d1c6e04dfbf66ac8af8624b7dcc43c33290ef48ef040b70502";
const TRACE_ID = "4bf92f3577b34da6a3ce929d0e0e4736";
const PARENT_ID = "00f067aa0ba902b7";

function traceparent(flags = "01"): string {
  return `00-${TRACE_ID}-${PARENT_ID}-${flags}`;
}

const VALID_LEVEL_2_TRACE_VECTORS = [
  ["all lower-case hexadecimal flags", { traceparent: traceparent("ff") }],
  ["empty tracestate header", { traceparent: traceparent(), tracestate: "" }],
  [
    "OWS and empty members",
    { traceparent: traceparent(), tracestate: "\t, 1vendor/@_*= leading value \t,," },
  ],
  [
    "32 members",
    {
      traceparent: traceparent(),
      tracestate: Array.from({ length: 32 }, (_, index) => `vendor${index}=value`).join(","),
    },
  ],
  [
    "256-character key",
    { traceparent: traceparent(), tracestate: `${"a".repeat(256)}=value` },
  ],
  [
    "256-character value",
    { traceparent: traceparent(), tracestate: `vendor=${" ".repeat(255)}x` },
  ],
  [
    "repository input ceiling",
    { traceparent: traceparent(), tracestate: " ".repeat(512) },
  ],
] as const;

const INVALID_LEVEL_2_TRACE_VECTORS = [
  ["upper-case flag", { traceparent: `00-${TRACE_ID}-${PARENT_ID}-0A` }],
  ["traceparent terminal newline", { traceparent: `${traceparent()}\n` }],
  ["zero trace identifier", { traceparent: `00-${"0".repeat(32)}-${PARENT_ID}-01` }],
  ["zero parent identifier", { traceparent: `00-${TRACE_ID}-${"0".repeat(16)}-01` }],
  ["33 empty members", { traceparent: traceparent(), tracestate: ",".repeat(32) }],
  ["upper-case key", { traceparent: traceparent(), tracestate: "Vendor=value" }],
  ["invalid initial key character", { traceparent: traceparent(), tracestate: "_vendor=value" }],
  [
    "257-character key",
    { traceparent: traceparent(), tracestate: `${"a".repeat(257)}=value` },
  ],
  ["empty value", { traceparent: traceparent(), tracestate: "vendor=" }],
  [
    "257-character value",
    { traceparent: traceparent(), tracestate: `vendor=${"x".repeat(257)}` },
  ],
  [
    "duplicate key",
    { traceparent: traceparent(), tracestate: "vendor=first,\t vendor=second" },
  ],
  ["equals sign in value", { traceparent: traceparent(), tracestate: "vendor=one=two" }],
  ["tab in value", { traceparent: traceparent(), tracestate: "vendor=one\ttwo" }],
  ["non-printable value", { traceparent: traceparent(), tracestate: "vendor=one\u007ftwo" }],
  [
    "tracestate terminal newline",
    { traceparent: traceparent(), tracestate: "vendor=value\n" },
  ],
  [
    "near-bound non-printable value",
    { traceparent: traceparent(), tracestate: `${" ".repeat(511)}\u007f` },
  ],
  [
    "repository input ceiling exceeded",
    { traceparent: traceparent(), tracestate: " ".repeat(513) },
  ],
] as const;

function builderInput(): Record<string, unknown> {
  const request = fixture("execution-request.example.json") as Record<string, unknown>;
  const authorisation = request.gateway_authorisation as Record<string, unknown>;
  const parameters = request.parameters as Record<string, unknown>;
  return {
    request_id: request.request_id,
    trace: request.trace,
    decision_id: authorisation.decision_id,
    decision_digest: authorisation.decision_digest,
    deadline: request.deadline,
    limits: request.limits,
    geometry: parameters.geometry,
    limit: parameters.limit,
  };
}

test("builds the exact closed gateway-to-Python fixture envelope", () => {
  assert.deepEqual(
    buildSyntheticExecutionRequest(builderInput(), NOW),
    fixture("execution-request.example.json"),
  );
});

test("accepts the W3C Trace Context Level 2 parity vectors", () => {
  for (const [name, trace] of VALID_LEVEL_2_TRACE_VECTORS) {
    const input = builderInput();
    input.trace = trace;
    assert.deepEqual(buildSyntheticExecutionRequest(input, NOW).trace, trace, name);
  }
});

test("rejects the invalid W3C Trace Context Level 2 parity vectors", () => {
  for (const [name, trace] of INVALID_LEVEL_2_TRACE_VECTORS) {
    const input = builderInput();
    input.trace = trace;
    assert.throws(() => buildSyntheticExecutionRequest(input, NOW), name);
  }
});

test("rejects extra fields, unsafe traces, excessive limits and stale deadlines", () => {
  const extra = builderInput();
  extra.url = "file:///tmp/secret";
  assert.throws(() => buildSyntheticExecutionRequest(extra, NOW), /unknown or missing/);

  const badTrace = builderInput();
  badTrace.trace = { traceparent: `00-${"0".repeat(32)}-${"1".repeat(16)}-01` };
  assert.throws(() => buildSyntheticExecutionRequest(badTrace, NOW), /traceparent/);

  const excessive = builderInput();
  excessive.limits = { ...(excessive.limits as object), max_features: 101 };
  assert.throws(() => buildSyntheticExecutionRequest(excessive, NOW), /integer range/);

  const expired = builderInput();
  expired.deadline = NOW.toISOString();
  assert.throws(() => buildSyntheticExecutionRequest(expired, NOW), /execution window/);

  const nonCanonicalDeadline = builderInput();
  nonCanonicalDeadline.deadline = "2026-08-20 12:00:10+00:00";
  assert.throws(
    () => buildSyntheticExecutionRequest(nonCanonicalDeadline, NOW),
    /execution window/,
  );

  const complex = builderInput();
  complex.limits = { ...(complex.limits as object), max_complexity: 16 };
  assert.throws(() => buildSyntheticExecutionRequest(complex, NOW), /complexity/);
});

test("validates and detaches the deterministic Python result with trace and source intact", () => {
  const request = buildSyntheticExecutionRequest(builderInput(), NOW);
  const result = parseExecutionResult(fixture("execution-result.example.json"), request);
  assert.deepEqual(result.trace, request.trace);
  assert.deepEqual(result.evidence.source, request.parameters.source);
  assert.notEqual(result, fixture("execution-result.example.json"));
});

test("accepts alternate object insertion order while preserving verified evidence", () => {
  const request = buildSyntheticExecutionRequest(builderInput(), NOW);
  const result = fixture("execution-result.example.json") as Record<string, any>;
  const data = result.data;
  result.data = {
    features: data.features.map((feature: Record<string, any>) => ({
      properties: {
        category: feature.properties.category,
        name: feature.properties.name,
        native_id: feature.properties.native_id,
      },
      geometry: {
        coordinates: feature.geometry.coordinates,
        type: feature.geometry.type,
      },
      id: feature.id,
      type: feature.type,
    })),
    axis_order: data.axis_order,
    crs: data.crs,
    type: data.type,
  };

  assert.deepEqual(
    parseExecutionResult(result, request),
    fixture("execution-result.example.json"),
  );
});

test("rejects forged or stale execution evidence digests", () => {
  const request = buildSyntheticExecutionRequest(builderInput(), NOW);

  const forgedInput = fixture("execution-result.example.json") as Record<string, any>;
  forgedInput.evidence.input_sha256 = `sha256:${"b".repeat(64)}`;
  assert.throws(() => parseExecutionResult(forgedInput, request), /input digest/u);

  const forgedOutput = fixture("execution-result.example.json") as Record<string, any>;
  forgedOutput.evidence.output_sha256 = `sha256:${"c".repeat(64)}`;
  assert.throws(() => parseExecutionResult(forgedOutput, request), /output digest/u);

  const changedData = fixture("execution-result.example.json") as Record<string, any>;
  changedData.data.features[0].properties.name = "Altered synthetic place";
  assert.throws(() => parseExecutionResult(changedData, request), /output digest/u);
});

test("matches the Python RFC 8785 domain-separated execution digest vectors", () => {
  assert.equal(
    domainSeparatedSha256(CANONICAL_DOMAINS.executionParameters, DIGEST_PARITY_VALUE),
    DIGEST_PARITY_INPUT,
  );
  assert.equal(
    domainSeparatedSha256(CANONICAL_DOMAINS.executionResultData, DIGEST_PARITY_VALUE),
    DIGEST_PARITY_OUTPUT,
  );
  assert.notEqual(DIGEST_PARITY_INPUT, DIGEST_PARITY_OUTPUT);
});

test("rejects result overproduction, source substitution and additional error material", () => {
  const request = buildSyntheticExecutionRequest(builderInput(), NOW);

  const overproduction = fixture("execution-result.example.json") as Record<string, any>;
  overproduction.data.features = Array.from(
    { length: 11 },
    () => overproduction.data.features[0],
  );
  assert.throws(() => parseExecutionResult(overproduction, request), /feature count/);

  const source = fixture("execution-result.example.json") as Record<string, any>;
  source.evidence.source.source_uri = "https://attacker.invalid/source";
  assert.throws(() => parseExecutionResult(source, request), /source evidence/);

  const duplicate = fixture("execution-result.example.json") as Record<string, any>;
  duplicate.data.features[1] = duplicate.data.features[0];
  assert.throws(() => parseExecutionResult(duplicate, request), /duplicated/);

  const stack = fixture("execution-result.example.json") as Record<string, any>;
  stack.stack = "/tmp/secret";
  assert.throws(() => parseExecutionResult(stack, request), /unknown or missing/);
});
