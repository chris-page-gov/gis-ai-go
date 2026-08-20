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
    ["catalogue.search", "catalogue.describe", "evidence.inspect"],
  );
  assert.deepEqual(
    first
      .filter(({ v02Target }) => v02Target.lifecycleState === "active")
      .map(({ name }) => name),
    V02_TARGET_ACTIVE_TOOL_NAMES,
  );
  assert.equal(getToolProfile("workflow.execute").mutating, true);
  assert.equal(getToolProfile("workflow.execute").releaseTarget, "v0.3.0");
});

test("keeps target lifecycle metadata separate from an empty current callable set", () => {
  const target = filterToolProfiles({ v02LifecycleState: "active" });
  assert.deepEqual(target.map(({ name }) => name), V02_TARGET_ACTIVE_TOOL_NAMES);
  assert.equal(getToolProfile("selection.resolve").current.implementationState, "not-implemented");
  assert.equal(getToolProfile("data.query").current.implementationState, "not-implemented");
  assert.deepEqual(listCurrentCallableTools(), []);
  assert.equal(Object.isFrozen(listCurrentCallableTools()), true);

  const planned = filterToolProfiles({ implementationState: "not-implemented" });
  assert.equal(planned.length, 9);
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
