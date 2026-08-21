import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import {
  TOOL_PROFILE_IDS,
  TOOL_PROFILE_NAMES,
  TOOL_REGISTRY_DOCUMENT,
  ToolRegistryFault,
  V02_TARGET_ACTIVE_TOOL_NAMES,
  createToolRegistry,
  filterToolProfiles,
  getToolProfile,
  listCurrentCallableTools,
  listToolProfiles,
} from "../src/index.js";

function profileRecord(): Record<string, unknown> {
  const url = new URL("../../../../profiles/tool-registry.v1.json", import.meta.url);
  return JSON.parse(readFileSync(url, "utf8")) as Record<string, unknown>;
}

function assertRecursivelyFrozen(value: unknown): void {
  if (value === null || typeof value !== "object") return;
  assert.equal(Object.isFrozen(value), true);
  for (const child of Object.values(value)) assertRecursivelyFrozen(child);
}

function expectInvalidRegistry(value: unknown): void {
  assert.throws(
    () => createToolRegistry(value),
    (error: unknown) =>
      error instanceof ToolRegistryFault &&
      error.code === "INVALID_TOOL_REGISTRY" &&
      error.message === "The tool registry failed closed validation.",
  );
}

test("loads exactly 12 deterministic frozen profiles from the canonical data", () => {
  const first = listToolProfiles();
  const second = listToolProfiles();

  assert.notEqual(first, second);
  assert.deepEqual(first.map(({ id }) => id), TOOL_PROFILE_IDS);
  assert.deepEqual(first.map(({ name }) => name), TOOL_PROFILE_NAMES);
  assert.deepEqual(TOOL_REGISTRY_DOCUMENT, profileRecord());
  assertRecursivelyFrozen(TOOL_REGISTRY_DOCUMENT);
  assertRecursivelyFrozen(first);

  assert.deepEqual(
    first
      .filter(({ current }) => current.implementationState === "implemented")
      .map(({ name }) => name),
    [
      "catalogue.search",
      "catalogue.describe",
      "selection.resolve",
      "data.query",
      "evidence.inspect",
    ],
  );
  assert.deepEqual(
    first
      .filter(({ v02Target }) => v02Target.lifecycleState === "active")
      .map(({ name }) => name),
    V02_TARGET_ACTIVE_TOOL_NAMES,
  );
  assert.equal(getToolProfile("workflow.execute").mutating, true);
  assert.equal(getToolProfile("workflow.execute").releaseTarget, "v0.3.0");
  assert.deepEqual(getToolProfile("evidence.inspect").runtimeSchemas.output, {
    state: "accepted",
    ref: "schemas/evidence-inspect-operation-result.schema.json",
  });
  assert.deepEqual(getToolProfile("evidence.inspect").runtimeSchemas.input, {
    state: "accepted",
    ref: "schemas/evidence-inspect-operation-request.schema.json",
  });
  assert.deepEqual(getToolProfile("evidence.inspect").runtimeSchemas.problem, {
    state: "accepted",
    ref: "schemas/catalogue-problem.schema.json",
  });
  assert.deepEqual(getToolProfile("evidence.inspect").fallback, {
    state: "not-implemented",
    behaviour:
      "Fail closed; no alternate receipt, result replay or challenge route is implemented.",
  });
});

test("keeps target lifecycle metadata separate from an empty current callable set", () => {
  const target = filterToolProfiles({ v02LifecycleState: "active" });
  assert.deepEqual(target.map(({ name }) => name), V02_TARGET_ACTIVE_TOOL_NAMES);
  for (const name of ["selection.resolve", "data.query"] as const) {
    const profile = getToolProfile(name);
    assert.equal(profile.current.implementationState, "implemented");
    assert.equal(profile.current.lifecycleState, "suspended");
    assert.equal(profile.current.discoveryEligible, false);
    assert.equal(Object.values(profile.current.activationGates).some(Boolean), false);
  }
  const selection = getToolProfile("selection.resolve");
  assert.deepEqual(selection.cursor, {
    state: "none",
    maxLength: null,
    artefactFallback: "not-implemented",
    researchStatement:
      "Bounded inline response; cursor pagination or immutable artefact when limits are exceeded.",
  });
  assert.deepEqual(selection.fallback, {
    state: "implemented",
    behaviour: "Return required choices and no executable plan.",
  });
  assert.equal(selection.support.providerDependencies.includes("PostGIS"), false);
  assert.equal(selection.support.providerDependencies.includes("object storage"), false);

  const data = getToolProfile("data.query");
  assert.deepEqual(data.cursor, {
    state: "none",
    maxLength: null,
    artefactFallback: "not-implemented",
    researchStatement:
      "Bounded inline response; cursor pagination or immutable artefact when limits are exceeded.",
  });
  assert.deepEqual(data.crs, { state: "not-applicable", requirements: [] });
  assert.deepEqual(data.fallback, {
    state: "not-implemented",
    behaviour:
      "Fail closed; no result cache, alternate provider or result fallback is permitted.",
  });
  assert.equal(data.support.providerDependencies.includes("PostGIS"), false);
  assert.equal(data.support.providerDependencies.includes("object storage"), false);
  assert.deepEqual(data.controlledErrors, [
    "INVALID_REQUEST",
    "QUERY_CANCELLED",
    "QUERY_DEADLINE_EXCEEDED",
    "POLICY_DENIED",
    "PROVIDER_SUSPENDED",
    "PROVIDER_RATE_LIMITED",
    "PROVIDER_TIMEOUT",
    "PROVIDER_UNAVAILABLE",
    "PROVIDER_CONTRACT_FAILED",
    "EVIDENCE_UNAVAILABLE",
    "IDEMPOTENCY_PENDING",
    "IDEMPOTENCY_COMPLETED",
    "IDEMPOTENCY_CONFLICT",
  ]);
  assert.deepEqual(data.runtimeSchemas.input, {
    state: "accepted",
    ref: "schemas/data-query-request.schema.json",
  });
  assert.deepEqual(data.runtimeSchemas.problem, {
    state: "accepted",
    ref: "schemas/data-query-operation-problem.schema.json",
  });
  assert.deepEqual(listCurrentCallableTools(), []);
  assert.equal(Object.isFrozen(listCurrentCallableTools()), true);

  const planned = filterToolProfiles({ implementationState: "not-implemented" });
  assert.equal(planned.length, 7);
  assert.equal(planned.some(({ current }) => current.discoveryEligible), false);
  assert.equal(
    planned.some(({ name }) => listCurrentCallableTools().some((tool) => tool.name === name)),
    false,
  );
});

test("provides closed deterministic get and filter helpers", () => {
  assert.deepEqual(
    filterToolProfiles({ readOnly: true, releaseTarget: "v0.2.0" }).map(({ name }) => name),
    [
      "catalogue.search",
      "catalogue.describe",
      "selection.resolve",
      "data.query",
      "evidence.inspect",
    ],
  );
  assert.deepEqual(
    filterToolProfiles({ ids: ["T11", "T02"] }).map(({ id }) => id),
    ["T02", "T11"],
  );
  assert.throws(
    () => getToolProfile("catalogue.unknown"),
    (error: unknown) =>
      error instanceof ToolRegistryFault && error.code === "UNKNOWN_TOOL_PROFILE",
  );
  assert.throws(
    () => filterToolProfiles({ unexpected: true } as never),
    (error: unknown) =>
      error instanceof ToolRegistryFault && error.code === "INVALID_TOOL_REGISTRY_FILTER",
  );
  assert.throws(
    () => filterToolProfiles({ names: ["catalogue.unknown"] as never }),
    (error: unknown) =>
      error instanceof ToolRegistryFault && error.code === "INVALID_TOOL_REGISTRY_FILTER",
  );
  assert.throws(
    () => filterToolProfiles({ ids: ["T01", "T01"] }),
    (error: unknown) =>
      error instanceof ToolRegistryFault && error.code === "INVALID_TOOL_REGISTRY_FILTER",
  );
});

test("rejects duplicate IDs, reordered profiles and unknown fields", () => {
  const duplicate = structuredClone(profileRecord()) as {
    tools: { id: string }[];
  };
  duplicate.tools[1]!.id = duplicate.tools[0]!.id;
  expectInvalidRegistry(duplicate);

  const reordered = structuredClone(profileRecord()) as {
    tools: Record<string, unknown>[];
  };
  [reordered.tools[0], reordered.tools[1]] = [reordered.tools[1]!, reordered.tools[0]!];
  expectInvalidRegistry(reordered);

  const unknownRoot = structuredClone(profileRecord());
  unknownRoot.unexpected = true;
  expectInvalidRegistry(unknownRoot);

  const unknownNested = structuredClone(profileRecord()) as {
    tools: { current: Record<string, unknown> }[];
  };
  unknownNested.tools[0]!.current.environmentOverride = true;
  expectInvalidRegistry(unknownNested);
});

test("rejects lifecycle, mutability, schema and target substitutions", () => {
  const advertisedPlanned = structuredClone(profileRecord()) as {
    tools: { current: { discoveryEligible: boolean } }[];
  };
  advertisedPlanned.tools[2]!.current.discoveryEligible = true;
  expectInvalidRegistry(advertisedPlanned);

  const missingSchema = structuredClone(profileRecord()) as {
    tools: { runtimeSchemas: { problem: { state: string; ref: string | null } } }[];
  };
  missingSchema.tools[0]!.runtimeSchemas.problem = { state: "missing", ref: null };
  expectInvalidRegistry(missingSchema);

  const substitutedSchema = structuredClone(profileRecord()) as {
    tools: { runtimeSchemas: { input: { state: string; ref: string | null } } }[];
  };
  substitutedSchema.tools[0]!.runtimeSchemas.input = {
    state: "accepted",
    ref: "schemas/catalogue-describe-request.schema.json",
  };
  expectInvalidRegistry(substitutedSchema);

  const workflowReadOnly = structuredClone(profileRecord()) as {
    tools: { readOnly: boolean; mutating: boolean }[];
  };
  workflowReadOnly.tools[11]!.readOnly = true;
  workflowReadOnly.tools[11]!.mutating = false;
  expectInvalidRegistry(workflowReadOnly);

  const targetAsRuntime = structuredClone(profileRecord()) as {
    tools: { v02Target: { runtimeAuthority: boolean } }[];
  };
  targetAsRuntime.tools[0]!.v02Target.runtimeAuthority = true;
  expectInvalidRegistry(targetAsRuntime);
});

test("rejects substitutions in the implemented public-read slice metadata", () => {
  const providerSubstitution = structuredClone(profileRecord()) as {
    tools: { support: { providerDependencies: string[] } }[];
  };
  providerSubstitution.tools[3]!.support.providerDependencies[0] = "PostGIS";
  expectInvalidRegistry(providerSubstitution);

  const errorSubstitution = structuredClone(profileRecord()) as {
    tools: { controlledErrors: string[] }[];
  };
  errorSubstitution.tools[2]!.controlledErrors[0] = "NOT_IMPLEMENTED";
  expectInvalidRegistry(errorSubstitution);

  const cursorSubstitution = structuredClone(profileRecord()) as {
    tools: { cursor: { state: string; maxLength: number | null } }[];
  };
  cursorSubstitution.tools[2]!.cursor.state = "not-implemented";
  expectInvalidRegistry(cursorSubstitution);

  const crsSubstitution = structuredClone(profileRecord()) as {
    tools: { crs: { state: string; requirements: string[] } }[];
  };
  crsSubstitution.tools[3]!.crs = {
    state: "required-before-implementation",
    requirements: ["Define a CRS before implementation."],
  };
  expectInvalidRegistry(crsSubstitution);

  const fallbackSubstitution = structuredClone(profileRecord()) as {
    tools: { fallback: { state: string; behaviour: string } }[];
  };
  fallbackSubstitution.tools[3]!.fallback.state = "partial";
  expectInvalidRegistry(fallbackSubstitution);

  const evidenceFallbackSubstitution = structuredClone(profileRecord()) as {
    tools: { fallback: { state: string; behaviour: string } }[];
  };
  evidenceFallbackSubstitution.tools[10]!.fallback.behaviour =
    "Return a challenge route.";
  expectInvalidRegistry(evidenceFallbackSubstitution);
});

test("clones caller data, rejects mutation and ignores environment state", (t) => {
  const input = profileRecord();
  const registry = createToolRegistry(input);
  const first = registry.get("catalogue.search");

  (input.tools as { purpose: string }[])[0]!.purpose = "Substituted after validation";
  assert.notEqual(registry.get("catalogue.search").purpose, "Substituted after validation");
  assert.throws(
    () => {
      (first as unknown as { purpose: string }).purpose = "Mutation";
    },
    TypeError,
  );
  assert.throws(
    () => {
      (registry.list() as unknown as unknown[]).push(first);
    },
    TypeError,
  );

  const environmentKey = "GIS_AI_GO_TOOL_REGISTRY";
  const previous = process.env[environmentKey];
  process.env[environmentKey] = "activate-all";
  t.after(() => {
    if (previous === undefined) delete process.env[environmentKey];
    else process.env[environmentKey] = previous;
  });
  assert.deepEqual(listCurrentCallableTools(), []);
  assert.equal(TOOL_REGISTRY_DOCUMENT.runtimeAuthority.environmentOverride, false);
});

test("rejects active input properties without invoking them", () => {
  const input = profileRecord();
  let invoked = false;
  Object.defineProperty(input, "tools", {
    enumerable: true,
    get: () => {
      invoked = true;
      return [];
    },
  });

  expectInvalidRegistry(input);
  assert.equal(invoked, false);
});
