import { readFileSync } from "node:fs";

import {
  ACTIVATION_REQUIREMENTS,
  TOOL_PROFILE_IDS,
  TOOL_PROFILE_NAMES,
  V02_TARGET_ACTIVE_TOOL_NAMES,
  type AcceptedRuntimeSchemaReference,
  type ActivationGates,
  type ImplementationState,
  type LifecycleState,
  type ReleaseTarget,
  type RuntimeSchemaReference,
  type ToolProfile,
  type ToolProfileId,
  type ToolProfileName,
  type ToolRegistry,
  type ToolRegistryDocument,
  type ToolRegistryFilter,
  type V02LifecycleState,
} from "./types.js";

export const TOOL_REGISTRY_ERROR_CODES = Object.freeze([
  "INVALID_TOOL_REGISTRY",
  "INVALID_TOOL_REGISTRY_FILTER",
  "UNKNOWN_TOOL_PROFILE",
] as const);

export type ToolRegistryErrorCode = (typeof TOOL_REGISTRY_ERROR_CODES)[number];

const SAFE_MESSAGES: Readonly<Record<ToolRegistryErrorCode, string>> = Object.freeze({
  INVALID_TOOL_REGISTRY: "The tool registry failed closed validation.",
  INVALID_TOOL_REGISTRY_FILTER: "The tool registry filter is invalid.",
  UNKNOWN_TOOL_PROFILE: "The requested tool profile is not recognised.",
});

const RESEARCH_SHA256 =
  "851f626bae4d63e8355ff9ca4021b56041ffa7e432d41f7f682c214151b5a8c3";
const RESEARCH_GIT_BLOB = "0514fba4ff4765c951c632f6a1c122fe02b1d178";
const TOOL_NAME_PATTERN = /^[a-z]+\.[a-z]+$/u;
const ERROR_CODE_PATTERN = /^[A-Z][A-Z0-9_]*$/u;
const RUNTIME_SCHEMA_PATTERN = /^schemas\/[a-z0-9-]+\.schema\.json$/u;
const TOOL_POINTER_PATTERN = /^\/tools\/(?:[0-9]|1[01])$/u;

const CURRENT_IMPLEMENTED_IDS = Object.freeze([
  "T01",
  "T02",
  "T03",
  "T04",
  "T11",
] as const);

const RELEASE_TARGET_BY_ID: Readonly<Record<ToolProfileId, ReleaseTarget>> = Object.freeze({
  T01: "v0.2.0",
  T02: "v0.2.0",
  T03: "v0.2.0",
  T04: "v0.2.0",
  T05: "later-reviewed-release",
  T06: "later-reviewed-release",
  T07: "later-reviewed-release",
  T08: "later-reviewed-release",
  T09: "later-reviewed-release",
  T10: "later-reviewed-release",
  T11: "v0.2.0",
  T12: "v0.3.0",
});

const RUNTIME_SCHEMA_REFS_BY_ID: Readonly<
  Record<
    ToolProfileId,
    {
      readonly input: string | null;
      readonly output: string | null;
      readonly problem: string | null;
    }
  >
> = Object.freeze({
  T01: {
    input: "schemas/catalogue-search-request.schema.json",
    output: "schemas/catalogue-result.schema.json",
    problem: "schemas/catalogue-problem.schema.json",
  },
  T02: {
    input: "schemas/catalogue-describe-request.schema.json",
    output: "schemas/catalogue-result.schema.json",
    problem: "schemas/catalogue-problem.schema.json",
  },
  T03: {
    input: "schemas/selection-resolve-request.schema.json",
    output: "schemas/selection-resolve-result.schema.json",
    problem: "schemas/selection-resolve-problem.schema.json",
  },
  T04: {
    input: "schemas/data-query-request.schema.json",
    output: "schemas/data-query-result.schema.json",
    problem: "schemas/data-query-operation-problem.schema.json",
  },
  T05: { input: null, output: null, problem: null },
  T06: { input: null, output: null, problem: null },
  T07: { input: null, output: null, problem: null },
  T08: { input: null, output: null, problem: null },
  T09: { input: null, output: null, problem: null },
  T10: { input: null, output: null, problem: null },
  T11: {
    input: "schemas/evidence-inspect-operation-request.schema.json",
    output: "schemas/evidence-inspect-operation-result-v3.schema.json",
    problem: "schemas/catalogue-problem.schema.json",
  },
  T12: { input: null, output: null, problem: null },
});

const CURRENT_PUBLIC_READ_PROVIDER_DEPENDENCIES = Object.freeze({
  T03: Object.freeze([
    "reviewed public selection profile",
    "public-read policy",
    "public evidence contract",
  ]),
  T04: Object.freeze([
    "explicitly injected ONS Data API adapter",
    "explicitly injected approved ONS cache",
    "public-read policy",
    "durable public evidence ledger",
    "receipt-only idempotency reconciliation index",
  ]),
  T11: Object.freeze([
    "durable public evidence ledger",
    "receipt-only idempotency reconciliation index",
    "anonymous-open evidence inspection policy",
  ]),
} as const);

const CURRENT_PUBLIC_READ_CONTROLLED_ERRORS = Object.freeze({
  T03: Object.freeze([
    "INVALID_REQUEST",
    "AMBIGUOUS_SELECTION",
    "MISSING_DIMENSION",
    "CONTRADICTORY_CONSTRAINTS",
    "NO_COMPATIBLE_PROVIDER",
    "POLICY_DENIED",
    "EVIDENCE_UNAVAILABLE",
  ]),
  T04: Object.freeze([
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
  ]),
  T11: Object.freeze([
    "INVALID_REQUEST",
    "EVIDENCE_NOT_FOUND",
    "EVIDENCE_UNAVAILABLE",
  ]),
} as const);

const PROFILE_KEYS = Object.freeze([
  "id",
  "name",
  "namespace",
  "purpose",
  "readOnly",
  "mutating",
  "releaseTarget",
  "current",
  "v02Target",
  "runtimeSchemas",
  "support",
  "accessTiers",
  "policyAttributes",
  "costPerformance",
  "controlledErrors",
  "cursor",
  "crs",
  "provenance",
  "fallback",
  "threats",
  "source",
] as const);

const FILTER_KEYS = Object.freeze([
  "ids",
  "names",
  "implementationState",
  "lifecycleState",
  "v02LifecycleState",
  "releaseTarget",
  "readOnly",
  "mutating",
  "discoveryEligible",
] as const);

export class ToolRegistryFault extends Error {
  public readonly code: ToolRegistryErrorCode;

  public constructor(code: ToolRegistryErrorCode) {
    super(SAFE_MESSAGES[code]);
    this.name = "ToolRegistryFault";
    this.code = code;
  }
}

function invalidRegistry(): never {
  throw new ToolRegistryFault("INVALID_TOOL_REGISTRY");
}

function invalidFilter(): never {
  throw new ToolRegistryFault("INVALID_TOOL_REGISTRY_FILTER");
}

function assertPassiveJsonTree(value: unknown, seen = new WeakSet<object>()): void {
  if (value === null || typeof value === "string" || typeof value === "boolean") return;
  if (typeof value === "number") {
    if (!Number.isFinite(value)) throw new TypeError("non-finite registry number");
    return;
  }
  if (typeof value !== "object") throw new TypeError("non-JSON registry value");
  if (seen.has(value)) throw new TypeError("shared or cyclic registry value");
  seen.add(value);

  const array = Array.isArray(value);
  const prototype = Object.getPrototypeOf(value);
  if (
    (array && prototype !== Array.prototype) ||
    (!array && prototype !== Object.prototype && prototype !== null)
  ) {
    throw new TypeError("non-plain registry object");
  }

  const keys = Reflect.ownKeys(value);
  if (keys.some((key) => typeof key === "symbol")) {
    throw new TypeError("symbol registry key");
  }
  if (array) {
    const lengthDescriptor = Object.getOwnPropertyDescriptor(value, "length");
    if (
      lengthDescriptor === undefined ||
      !("value" in lengthDescriptor) ||
      !Number.isSafeInteger(lengthDescriptor.value) ||
      lengthDescriptor.value < 0 ||
      lengthDescriptor.value > 64
    ) {
      throw new TypeError("invalid registry array length");
    }
    const expected = new Set<string>(["length"]);
    for (let index = 0; index < lengthDescriptor.value; index += 1) {
      expected.add(String(index));
    }
    if (keys.length !== expected.size) {
      throw new TypeError("sparse or extended registry array");
    }
    for (const key of keys) {
      if (typeof key !== "string" || !expected.has(key)) {
        throw new TypeError("extended registry array");
      }
    }
  }

  for (const key of keys) {
    if (array && key === "length") continue;
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (
      descriptor === undefined ||
      !("value" in descriptor) ||
      !descriptor.enumerable
    ) {
      throw new TypeError("active or hidden registry property");
    }
    assertPassiveJsonTree(descriptor.value, seen);
  }
}

function cloneInput(value: unknown, code: "registry" | "filter"): unknown {
  try {
    assertPassiveJsonTree(value);
    return structuredClone(value);
  } catch {
    return code === "registry" ? invalidRegistry() : invalidFilter();
  }
}

function asRecord(value: unknown, code: "registry" | "filter" = "registry"):
  Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    return code === "registry" ? invalidRegistry() : invalidFilter();
  }
  const prototype = Object.getPrototypeOf(value);
  if (prototype !== Object.prototype && prototype !== null) {
    return code === "registry" ? invalidRegistry() : invalidFilter();
  }
  return value as Record<string, unknown>;
}

function assertExactKeys(
  record: Readonly<Record<string, unknown>>,
  expected: readonly string[],
  code: "registry" | "filter" = "registry",
): void {
  const actual = Object.keys(record).sort();
  const wanted = [...expected].sort();
  if (
    actual.length !== wanted.length ||
    actual.some((key, index) => key !== wanted[index])
  ) {
    if (code === "registry") invalidRegistry();
    invalidFilter();
  }
}

function assertString(value: unknown, minimum: number, maximum: number): asserts value is string {
  if (typeof value !== "string" || value.length < minimum || value.length > maximum) {
    invalidRegistry();
  }
}

function assertBoolean(value: unknown): asserts value is boolean {
  if (typeof value !== "boolean") invalidRegistry();
}

function assertEnum<T extends string>(value: unknown, allowed: readonly T[]): asserts value is T {
  if (typeof value !== "string" || !allowed.includes(value as T)) invalidRegistry();
}

function validateStringArray(
  value: unknown,
  minimum: number,
  maximum: number,
  pattern?: RegExp,
): readonly string[] {
  if (!Array.isArray(value) || value.length < minimum || value.length > maximum) {
    invalidRegistry();
  }
  const observed = value as unknown[];
  for (const item of observed) {
    assertString(item, 1, 256);
    if (pattern !== undefined && !pattern.test(item)) invalidRegistry();
  }
  if (new Set(observed).size !== observed.length) invalidRegistry();
  return observed as readonly string[];
}

function assertExactSequence(value: unknown, expected: readonly string[]): void {
  if (
    !Array.isArray(value) ||
    value.length !== expected.length ||
    value.some((item, index) => item !== expected[index])
  ) {
    invalidRegistry();
  }
}

function validateActivationGates(value: unknown): ActivationGates {
  const record = asRecord(value);
  assertExactKeys(record, [
    "releaseEnabled",
    "policy",
    "schema",
    "threat",
    "evidence",
    "interoperability",
    "fallback",
  ]);
  for (const field of Object.keys(record)) assertBoolean(record[field]);
  return record as unknown as ActivationGates;
}

function validateRuntimeSchemaReference(value: unknown): RuntimeSchemaReference {
  const record = asRecord(value);
  assertExactKeys(record, ["state", "ref"]);
  assertEnum(record.state, ["accepted", "missing"] as const);
  if (record.state === "accepted") {
    assertString(record.ref, 1, 128);
    if (!RUNTIME_SCHEMA_PATTERN.test(record.ref)) invalidRegistry();
    return record as unknown as AcceptedRuntimeSchemaReference;
  }
  if (record.ref !== null) invalidRegistry();
  return record as unknown as RuntimeSchemaReference;
}

function validateProfile(value: unknown, index: number): ToolProfile {
  const profile = asRecord(value);
  assertExactKeys(profile, PROFILE_KEYS);

  const expectedId = TOOL_PROFILE_IDS[index];
  const expectedName = TOOL_PROFILE_NAMES[index];
  if (expectedId === undefined || expectedName === undefined) invalidRegistry();
  if (profile.id !== expectedId || profile.name !== expectedName) invalidRegistry();

  assertString(profile.namespace, 1, 32);
  assertString(profile.purpose, 1, 256);
  assertBoolean(profile.readOnly);
  assertBoolean(profile.mutating);
  assertEnum(profile.releaseTarget, [
    "v0.2.0",
    "later-reviewed-release",
    "v0.3.0",
  ] as const);
  if (
    !TOOL_NAME_PATTERN.test(expectedName) ||
    profile.namespace !== expectedName.split(".")[0] ||
    profile.readOnly === profile.mutating ||
    profile.releaseTarget !== RELEASE_TARGET_BY_ID[expectedId]
  ) {
    invalidRegistry();
  }

  const current = asRecord(profile.current);
  assertExactKeys(current, [
    "implementationState",
    "lifecycleState",
    "discoveryEligible",
    "activationGates",
  ]);
  assertEnum(current.implementationState, ["implemented", "not-implemented"] as const);
  assertEnum(current.lifecycleState, ["active", "planned", "retired", "suspended"] as const);
  assertBoolean(current.discoveryEligible);
  const gates = validateActivationGates(current.activationGates);

  const implemented = CURRENT_IMPLEMENTED_IDS.includes(expectedId as never);
  if (
    current.implementationState !== (implemented ? "implemented" : "not-implemented") ||
    current.lifecycleState !== (implemented ? "suspended" : "planned") ||
    current.discoveryEligible ||
    Object.values(gates).some(Boolean)
  ) {
    invalidRegistry();
  }

  const target = asRecord(profile.v02Target);
  assertExactKeys(target, ["lifecycleState", "discoveryIntended", "runtimeAuthority"]);
  assertEnum(target.lifecycleState, ["active", "planned"] as const);
  assertBoolean(target.discoveryIntended);
  if (target.runtimeAuthority !== false) invalidRegistry();
  const targetActive = V02_TARGET_ACTIVE_TOOL_NAMES.includes(expectedName as never);
  if (
    target.lifecycleState !== (targetActive ? "active" : "planned") ||
    target.discoveryIntended !== targetActive
  ) {
    invalidRegistry();
  }

  const runtimeSchemas = asRecord(profile.runtimeSchemas);
  assertExactKeys(runtimeSchemas, ["input", "output", "problem"]);
  const inputSchema = validateRuntimeSchemaReference(runtimeSchemas.input);
  const outputSchema = validateRuntimeSchemaReference(runtimeSchemas.output);
  const problemSchema = validateRuntimeSchemaReference(runtimeSchemas.problem);
  const expectedSchemas = RUNTIME_SCHEMA_REFS_BY_ID[expectedId];
  if (
    inputSchema.ref !== expectedSchemas.input ||
    outputSchema.ref !== expectedSchemas.output ||
    problemSchema.ref !== expectedSchemas.problem
  ) {
    invalidRegistry();
  }
  if (implemented) {
    if (inputSchema.state !== "accepted" || outputSchema.state !== "accepted") {
      invalidRegistry();
    }
    if (problemSchema.state !== "accepted") {
      invalidRegistry();
    }
  } else if (
    inputSchema.state !== "missing" ||
    outputSchema.state !== "missing" ||
    problemSchema.state !== "missing"
  ) {
    invalidRegistry();
  }

  const support = asRecord(profile.support);
  assertExactKeys(support, [
    "operation",
    "operationState",
    "providerState",
    "providerDependencies",
  ]);
  if (support.operation !== expectedName) invalidRegistry();
  assertEnum(support.operationState, ["implemented-inactive", "not-implemented"] as const);
  assertEnum(support.providerState, ["candidate-partial", "planned"] as const);
  validateStringArray(support.providerDependencies, 1, 32);
  if (
    support.operationState !== (implemented ? "implemented-inactive" : "not-implemented") ||
    support.providerState !== (implemented ? "candidate-partial" : "planned")
  ) {
    invalidRegistry();
  }

  validateStringArray(profile.accessTiers, 1, 32);
  validateStringArray(profile.policyAttributes, 1, 32);
  assertString(profile.costPerformance, 1, 256);
  validateStringArray(profile.controlledErrors, 1, 16, ERROR_CODE_PATTERN);
  if (expectedId === "T03" || expectedId === "T04" || expectedId === "T11") {
    assertExactSequence(
      support.providerDependencies,
      CURRENT_PUBLIC_READ_PROVIDER_DEPENDENCIES[expectedId],
    );
    assertExactSequence(
      profile.controlledErrors,
      CURRENT_PUBLIC_READ_CONTROLLED_ERRORS[expectedId],
    );
  }

  const cursor = asRecord(profile.cursor);
  assertExactKeys(cursor, ["state", "maxLength", "artefactFallback", "researchStatement"]);
  assertEnum(cursor.state, ["none", "optional", "not-implemented"] as const);
  assertEnum(cursor.artefactFallback, ["implemented", "not-implemented"] as const);
  assertString(cursor.researchStatement, 1, 256);
  const maxLength = cursor.maxLength;
  if (
    maxLength !== null &&
    (typeof maxLength !== "number" ||
      !Number.isSafeInteger(maxLength) ||
      maxLength < 1 ||
      maxLength > 4_096)
  ) {
    invalidRegistry();
  }
  if ((cursor.state === "optional") !== (maxLength !== null)) invalidRegistry();
  if (cursor.artefactFallback !== "not-implemented") invalidRegistry();

  const crs = asRecord(profile.crs);
  assertExactKeys(crs, ["state", "requirements"]);
  assertEnum(crs.state, ["not-applicable", "required-before-implementation"] as const);
  const crsRequirements = validateStringArray(crs.requirements, 0, 4);
  if ((crs.state === "not-applicable") !== (crsRequirements.length === 0)) {
    invalidRegistry();
  }

  const provenance = asRecord(profile.provenance);
  assertExactKeys(provenance, ["requiredFields"]);
  validateStringArray(provenance.requiredFields, 1, 32);

  const fallback = asRecord(profile.fallback);
  assertExactKeys(fallback, ["state", "behaviour"]);
  assertEnum(fallback.state, ["implemented", "partial", "not-implemented"] as const);
  assertString(fallback.behaviour, 1, 256);
  if (expectedId === "T03") {
    if (
      cursor.state !== "none" ||
      cursor.maxLength !== null ||
      crs.state !== "not-applicable" ||
      fallback.state !== "implemented" ||
      fallback.behaviour !== "Return required choices and no executable plan."
    ) {
      invalidRegistry();
    }
  }
  if (expectedId === "T04") {
    if (
      cursor.state !== "none" ||
      cursor.maxLength !== null ||
      crs.state !== "not-applicable" ||
      fallback.state !== "implemented" ||
      fallback.behaviour !==
        "Use the exact approved cache only after an internally classified network failure or " +
          "HTTP 500 to 599 response; reject 3xx/4xx, local-timeout, unsafe-address, " +
          "malformed-response, opaque or unbranded failures; expose retrieval and " +
          "stale-after times."
    ) {
      invalidRegistry();
    }
  }
  if (expectedId === "T11") {
    if (
      cursor.state !== "none" ||
      cursor.maxLength !== null ||
      crs.state !== "not-applicable" ||
      fallback.state !== "not-implemented" ||
      fallback.behaviour !==
        "Fail closed; no alternate receipt, result replay or challenge route is implemented."
    ) {
      invalidRegistry();
    }
  }

  const threats = asRecord(profile.threats);
  assertExactKeys(threats, ["risks"]);
  validateStringArray(threats.risks, 1, 32);

  const source = asRecord(profile.source);
  assertExactKeys(source, [
    "researchId",
    "pointer",
    "inputSchemaPointer",
    "outputSchemaPointer",
  ]);
  const expectedPointer = `/tools/${index}`;
  if (
    source.researchId !== expectedId ||
    source.pointer !== expectedPointer ||
    source.inputSchemaPointer !== `${expectedPointer}/input_schema` ||
    source.outputSchemaPointer !== `${expectedPointer}/output_schema` ||
    !TOOL_POINTER_PATTERN.test(expectedPointer)
  ) {
    invalidRegistry();
  }

  if (
    (expectedId === "T12" && (!profile.mutating || profile.readOnly)) ||
    (expectedId !== "T12" && (profile.mutating || !profile.readOnly))
  ) {
    invalidRegistry();
  }
  return profile as unknown as ToolProfile;
}

function validateDocument(value: unknown): ToolRegistryDocument {
  const document = asRecord(value);
  assertExactKeys(document, [
    "schema",
    "version",
    "canonicalOrder",
    "activationRequirements",
    "candidateAssembly",
    "runtimeAuthority",
    "source",
    "tools",
  ]);
  if (document.schema !== "gis-ai-go.tool-registry.v1" || document.version !== "1.2.0") {
    invalidRegistry();
  }
  assertExactSequence(document.canonicalOrder, TOOL_PROFILE_NAMES);
  assertExactSequence(document.activationRequirements, ACTIVATION_REQUIREMENTS);

  const candidateAssembly = asRecord(document.candidateAssembly);
  assertExactKeys(candidateAssembly, [
    "state",
    "source",
    "operations",
    "productionRegistration",
  ]);
  if (
    candidateAssembly.state !== "candidate-unregistered" ||
    candidateAssembly.source !== "apps/mcp-gateway/src/governed-assembly.ts" ||
    candidateAssembly.productionRegistration !== false
  ) {
    invalidRegistry();
  }
  assertExactSequence(candidateAssembly.operations, V02_TARGET_ACTIVE_TOOL_NAMES);

  const runtimeAuthority = asRecord(document.runtimeAuthority);
  assertExactKeys(runtimeAuthority, [
    "source",
    "registryCanActivate",
    "environmentOverride",
    "productionRegistration",
  ]);
  if (
    runtimeAuthority.source !== "apps/mcp-gateway/src/activation.ts" ||
    runtimeAuthority.registryCanActivate !== false ||
    runtimeAuthority.environmentOverride !== false ||
    runtimeAuthority.productionRegistration !== false
  ) {
    invalidRegistry();
  }

  const source = asRecord(document.source);
  assertExactKeys(source, ["decision", "research"]);
  const decision = asRecord(source.decision);
  assertExactKeys(decision, ["path", "status"]);
  if (
    decision.path !== "docs/decisions/ADR-0009-read-only-mcp-tool-lifecycle.md" ||
    decision.status !== "accepted"
  ) {
    invalidRegistry();
  }
  const research = asRecord(source.research);
  assertExactKeys(research, [
    "path",
    "retrieved",
    "sha256",
    "gitBlob",
    "immutable",
    "records",
  ]);
  if (
    research.path !== "docs/research/2026-08-19/research-pack/data/tool-catalogue.json" ||
    research.retrieved !== "2026-08-19" ||
    research.sha256 !== RESEARCH_SHA256 ||
    research.gitBlob !== RESEARCH_GIT_BLOB ||
    research.immutable !== true
  ) {
    invalidRegistry();
  }
  assertExactSequence(research.records, TOOL_PROFILE_IDS);

  if (!Array.isArray(document.tools) || document.tools.length !== TOOL_PROFILE_NAMES.length) {
    invalidRegistry();
  }
  const profiles = document.tools.map((profile, index) => validateProfile(profile, index));
  if (
    new Set(profiles.map(({ id }) => id)).size !== profiles.length ||
    new Set(profiles.map(({ name }) => name)).size !== profiles.length
  ) {
    invalidRegistry();
  }
  return document as unknown as ToolRegistryDocument;
}

function deepFreeze<T>(value: T, seen = new WeakSet<object>()): T {
  if (value === null || typeof value !== "object") return value;
  const object = value as object;
  if (seen.has(object)) return value;
  seen.add(object);
  for (const child of Object.values(value as Record<string, unknown>)) {
    deepFreeze(child, seen);
  }
  return Object.freeze(value);
}

function isAccepted(reference: RuntimeSchemaReference):
  reference is AcceptedRuntimeSchemaReference {
  return reference.state === "accepted";
}

function isCurrentCallable(profile: ToolProfile): boolean {
  const gates = profile.current.activationGates;
  return (
    profile.current.implementationState === "implemented" &&
    profile.current.lifecycleState === "active" &&
    profile.current.discoveryEligible &&
    profile.readOnly &&
    !profile.mutating &&
    gates.releaseEnabled &&
    gates.policy &&
    gates.schema &&
    gates.threat &&
    gates.evidence &&
    gates.interoperability &&
    gates.fallback &&
    isAccepted(profile.runtimeSchemas.input) &&
    isAccepted(profile.runtimeSchemas.output) &&
    isAccepted(profile.runtimeSchemas.problem)
  );
}

function isCandidateAssemblyTool(
  profile: ToolProfile,
  operations: readonly string[],
): boolean {
  return (
    operations.includes(profile.name) &&
    profile.current.implementationState === "implemented" &&
    profile.v02Target.lifecycleState === "active" &&
    profile.v02Target.discoveryIntended &&
    profile.readOnly &&
    !profile.mutating &&
    isAccepted(profile.runtimeSchemas.input) &&
    isAccepted(profile.runtimeSchemas.output) &&
    isAccepted(profile.runtimeSchemas.problem)
  );
}

function validateFilter(value: ToolRegistryFilter): ToolRegistryFilter {
  const snapshot = asRecord(cloneInput(value, "filter"), "filter");
  const actualKeys = Object.keys(snapshot);
  if (actualKeys.some((key) => !FILTER_KEYS.includes(key as never))) invalidFilter();

  const validateKnownList = <T extends string>(
    candidate: unknown,
    allowed: readonly T[],
  ): readonly T[] => {
    if (
      !Array.isArray(candidate) ||
      candidate.length < 1 ||
      candidate.length > allowed.length ||
      candidate.some((item) => typeof item !== "string" || !allowed.includes(item as T)) ||
      new Set(candidate).size !== candidate.length
    ) {
      invalidFilter();
    }
    return candidate as readonly T[];
  };

  if (Object.hasOwn(snapshot, "ids")) validateKnownList(snapshot.ids, TOOL_PROFILE_IDS);
  if (Object.hasOwn(snapshot, "names")) validateKnownList(snapshot.names, TOOL_PROFILE_NAMES);
  if (
    Object.hasOwn(snapshot, "implementationState") &&
    !(["implemented", "not-implemented"] as const).includes(
      snapshot.implementationState as ImplementationState,
    )
  ) {
    invalidFilter();
  }
  if (
    Object.hasOwn(snapshot, "lifecycleState") &&
    !(["active", "planned", "retired", "suspended"] as const).includes(
      snapshot.lifecycleState as LifecycleState,
    )
  ) {
    invalidFilter();
  }
  if (
    Object.hasOwn(snapshot, "v02LifecycleState") &&
    !(["active", "planned"] as const).includes(
      snapshot.v02LifecycleState as V02LifecycleState,
    )
  ) {
    invalidFilter();
  }
  if (
    Object.hasOwn(snapshot, "releaseTarget") &&
    !(["v0.2.0", "later-reviewed-release", "v0.3.0"] as const).includes(
      snapshot.releaseTarget as ReleaseTarget,
    )
  ) {
    invalidFilter();
  }
  for (const field of ["readOnly", "mutating", "discoveryEligible"] as const) {
    if (Object.hasOwn(snapshot, field) && typeof snapshot[field] !== "boolean") invalidFilter();
  }
  return deepFreeze(snapshot) as unknown as ToolRegistryFilter;
}

function matchesFilter(profile: ToolProfile, filter: ToolRegistryFilter): boolean {
  return (
    (filter.ids === undefined || filter.ids.includes(profile.id)) &&
    (filter.names === undefined || filter.names.includes(profile.name)) &&
    (filter.implementationState === undefined ||
      profile.current.implementationState === filter.implementationState) &&
    (filter.lifecycleState === undefined ||
      profile.current.lifecycleState === filter.lifecycleState) &&
    (filter.v02LifecycleState === undefined ||
      profile.v02Target.lifecycleState === filter.v02LifecycleState) &&
    (filter.releaseTarget === undefined || profile.releaseTarget === filter.releaseTarget) &&
    (filter.readOnly === undefined || profile.readOnly === filter.readOnly) &&
    (filter.mutating === undefined || profile.mutating === filter.mutating) &&
    (filter.discoveryEligible === undefined ||
      profile.current.discoveryEligible === filter.discoveryEligible)
  );
}

/** Build an immutable view after closed structural and lifecycle validation. */
export function createToolRegistry(value: unknown): ToolRegistry {
  const document = deepFreeze(validateDocument(cloneInput(value, "registry")));
  const byName = new Map<ToolProfileName, ToolProfile>(
    document.tools.map((profile) => [profile.name, profile]),
  );
  const list = (): readonly ToolProfile[] => Object.freeze([...document.tools]);
  const filter = (criteria: ToolRegistryFilter): readonly ToolProfile[] => {
    const validated = validateFilter(criteria);
    return Object.freeze(document.tools.filter((profile) => matchesFilter(profile, validated)));
  };
  const registry: ToolRegistry = {
    document,
    list,
    get: (name: string): ToolProfile => {
      const profile = byName.get(name as ToolProfileName);
      if (profile === undefined) throw new ToolRegistryFault("UNKNOWN_TOOL_PROFILE");
      return profile;
    },
    filter,
    listCandidateAssemblyTools: (): readonly ToolProfile[] =>
      Object.freeze(
        document.tools.filter((profile) =>
          isCandidateAssemblyTool(profile, document.candidateAssembly.operations)),
      ),
    listCurrentCallable: (): readonly ToolProfile[] =>
      Object.freeze(document.tools.filter(isCurrentCallable)),
  };
  return Object.freeze(registry);
}

function loadBundledRegistry(): unknown {
  try {
    const path = new URL("../profile/tool-registry.v1.json", import.meta.url);
    return JSON.parse(readFileSync(path, "utf8")) as unknown;
  } catch {
    return invalidRegistry();
  }
}

export const CANONICAL_TOOL_REGISTRY: ToolRegistry = createToolRegistry(loadBundledRegistry());
export const TOOL_REGISTRY_DOCUMENT: ToolRegistryDocument = CANONICAL_TOOL_REGISTRY.document;

/** Return all 12 profiles in ADR-0009 order. Profiles and the returned array are frozen. */
export function listToolProfiles(): readonly ToolProfile[] {
  return CANONICAL_TOOL_REGISTRY.list();
}

/** Return one frozen profile or a controlled `UNKNOWN_TOOL_PROFILE` failure. */
export function getToolProfile(name: string): ToolProfile {
  return CANONICAL_TOOL_REGISTRY.get(name);
}

/** Apply a closed metadata filter while retaining canonical order. */
export function filterToolProfiles(filter: ToolRegistryFilter): readonly ToolProfile[] {
  return CANONICAL_TOOL_REGISTRY.filter(filter);
}

/**
 * Return the exact implemented read-only candidate assembly. This candidate-only
 * projection cannot register production operations and never includes a planned
 * or mutating profile.
 */
export function listCandidateAssemblyTools(): readonly ToolProfile[] {
  return CANONICAL_TOOL_REGISTRY.listCandidateAssemblyTools();
}

/**
 * Return profiles that satisfy every current activation gate and have complete
 * accepted runtime schema references. The candidate deliberately returns none.
 * `v02Target` is never consulted by this helper.
 */
export function listCurrentCallableTools(): readonly ToolProfile[] {
  return CANONICAL_TOOL_REGISTRY.listCurrentCallable();
}
