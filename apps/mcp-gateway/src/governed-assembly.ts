import { types as utilTypes } from "node:util";

import {
  PublicEvidenceLedger,
  PublicEvidenceReconciliationIndex,
  type EvidenceSoftwareIdentity,
} from "@gis-ai-go/evidence";
import {
  PUBLIC_CATALOGUE_POLICY,
  PUBLIC_EVIDENCE_INSPECTION_POLICY,
  PUBLIC_READ_POLICY,
} from "@gis-ai-go/policy-client";
import {
  ONS_ADAPTER_ID,
  ONS_ADAPTER_VERSION,
  requirePristineOnsDataApiAdapter,
  type AdapterHealth,
  type ApprovedOnsDataQueryCache,
  type OnsDataApiAdapter,
} from "@gis-ai-go/provider-adapter-sdk";
import {
  TOOL_REGISTRY_DOCUMENT,
  V02_TARGET_ACTIVE_TOOL_NAMES,
  listCandidateAssemblyTools,
  type V02TargetActiveToolName,
} from "@gis-ai-go/tool-registry";

import {
  createCatalogueApplication,
  type CatalogueApplication,
} from "./catalogue-application.js";
import {
  requireExactCatalogueSnapshot,
  type CatalogueSnapshot,
} from "./catalogue-snapshot.js";
import {
  GOVERNED_PRISTINE_ONS_EXECUTION,
  createDataQueryApplication,
  type DataQueryApplication,
} from "./data-query-application.js";
import {
  createEvidenceInspectApplication,
  type EvidenceInspectApplication,
} from "./evidence-application.js";
import { gatewayMetadata } from "./metadata.js";
import {
  createEvidenceReadinessIntegrity,
  evidenceReconciliationClaimCapacity,
  verifyEvidenceReadinessIntegrity,
  type EvidenceReadinessIntegrity,
} from "./readiness-integrity.js";
import {
  createSelectionResolveApplication,
  type SelectionResolveApplication,
} from "./selection-application.js";

export const GOVERNED_CANDIDATE_ASSEMBLY_KIND =
  "gis-ai-go.governed-candidate-assembly.v1" as const;
export const GOVERNED_CANDIDATE_OPERATIONS = Object.freeze(
  listCandidateAssemblyTools().map(({ name }) => name),
) as readonly V02TargetActiveToolName[];
export const GOVERNED_CANDIDATE_MCP_RESOURCES = Object.freeze([
  "catalogue.public",
  "catalogue.record",
  "evidence.receipt",
] as const);

const OPTION_KEYS = Object.freeze([
  "adapter",
  "approvedCache",
  "evidenceLedger",
  "now",
  "reconciliationIndex",
  "snapshot",
  "suspendedTools",
] as const);

if (
  TOOL_REGISTRY_DOCUMENT.runtimeAuthority.productionRegistration !== false ||
  TOOL_REGISTRY_DOCUMENT.candidateAssembly.productionRegistration !== false ||
  GOVERNED_CANDIDATE_OPERATIONS.length !== V02_TARGET_ACTIVE_TOOL_NAMES.length ||
  GOVERNED_CANDIDATE_OPERATIONS.some(
    (operation, index) => operation !== V02_TARGET_ACTIVE_TOOL_NAMES[index],
  )
) {
  throw new Error("The governed candidate registry projection failed closed");
}

export type GovernedCandidateOperation = V02TargetActiveToolName;

export type GovernedCandidateSuspensionSource =
  | "explicit-tool-suspension"
  | "policy"
  | "provider-discovery"
  | "provider-invocation"
  | "required-evidence-operation";

export interface GovernedCandidateSuspension {
  readonly operation: GovernedCandidateOperation;
  readonly source: GovernedCandidateSuspensionSource;
}

export interface GovernedCandidateAssemblyOptions {
  readonly snapshot: CatalogueSnapshot;
  readonly evidenceLedger: PublicEvidenceLedger;
  readonly reconciliationIndex: PublicEvidenceReconciliationIndex;
  readonly adapter: OnsDataApiAdapter;
  readonly approvedCache?: ApprovedOnsDataQueryCache;
  readonly now?: () => Date;
  /** Subtractive lifecycle seam. It can never add an operation or planned profile. */
  readonly suspendedTools?: readonly GovernedCandidateOperation[];
}

export interface GovernedCandidateAssembly {
  readonly kind: typeof GOVERNED_CANDIDATE_ASSEMBLY_KIND;
  readonly state: "candidate-unregistered";
  readonly productionRegistration: false;
  readonly operations: readonly GovernedCandidateOperation[];
  readonly apiOperations: readonly GovernedCandidateOperation[];
  readonly mcpOperations: readonly GovernedCandidateOperation[];
  readonly mcpResources: readonly (
    | "catalogue.public"
    | "catalogue.record"
    | "evidence.receipt"
  )[];
  readonly suspensions: readonly GovernedCandidateSuspension[];
  readonly bindings: {
    readonly registry: {
      readonly schema: "gis-ai-go.tool-registry.v1";
      readonly version: "1.2.0";
    };
    readonly policies: readonly [string, string, string];
    readonly provider: {
      readonly adapterId: typeof ONS_ADAPTER_ID;
      readonly adapterVersion: typeof ONS_ADAPTER_VERSION;
      readonly discovery: "active" | "suspended";
      readonly invocation: "active" | "suspended";
    };
    readonly evidence: {
      readonly ledgerId: string;
      readonly reconciliationIndexId: string;
    };
  };
}

export interface GovernedCandidateAssemblyBindings {
  readonly snapshot: CatalogueSnapshot;
  readonly catalogueApplication: CatalogueApplication;
  readonly evidenceApplication: EvidenceInspectApplication;
  readonly selectionApplication: SelectionResolveApplication;
  readonly dataQueryApplication: DataQueryApplication;
  readonly evidenceReadinessIntegrity: EvidenceReadinessIntegrity;
  readonly verifyProviderReadiness: () => void;
}

export interface GovernedCandidateReadiness {
  readonly status: "ready" | "blocked";
  readonly reason: "candidate-assembly-verified" | "evidence-integrity-failed" |
    "reconciliation-capacity-exhausted" | "relevant-capability-suspended";
  readonly productionRegistration: false;
  readonly activeTools: readonly GovernedCandidateOperation[];
  readonly activeApiOperations: readonly GovernedCandidateOperation[];
}

const ASSEMBLY_BINDINGS = new WeakMap<object, GovernedCandidateAssemblyBindings>();

export function snapshotGovernedCandidateOptions(
  value: unknown,
  allowedKeys: readonly string[],
  label: string,
): Readonly<Record<string, unknown>> {
  if (
    typeof value !== "object" ||
    value === null ||
    Array.isArray(value) ||
    utilTypes.isProxy(value)
  ) {
    throw new TypeError(`${label} must be a plain object`);
  }
  const prototype = Object.getPrototypeOf(value) as object | null;
  if (prototype !== Object.prototype && prototype !== null) {
    throw new TypeError(`${label} must be a plain object`);
  }
  const keys = Reflect.ownKeys(value);
  const descriptors = Object.getOwnPropertyDescriptors(value);
  if (
    keys.some((key) => typeof key !== "string" || !allowedKeys.includes(key))
  ) {
    throw new TypeError(`${label} have an unexpected shape`);
  }
  for (const descriptor of Object.values(descriptors)) {
    if (!("value" in descriptor) || descriptor.enumerable !== true) {
      throw new TypeError(`${label} must use enumerable data properties`);
    }
  }
  return Object.freeze(
    Object.fromEntries(
      Object.entries(descriptors).map(([key, descriptor]) => [key, descriptor.value]),
    ),
  );
}

/** Snapshot one nested authority allowlist without invoking proxies or accessors. */
export function snapshotGovernedCandidateStringArray(
  value: unknown,
  label: string,
): readonly string[] {
  if (utilTypes.isProxy(value) || !Array.isArray(value)) {
    throw new TypeError(`${label} must be a dense string array`);
  }
  const descriptors = Object.getOwnPropertyDescriptors(value);
  const length = Object.getOwnPropertyDescriptor(value, "length");
  const lengthValue =
    length !== undefined && "value" in length && typeof length.value === "number"
      ? length.value
      : undefined;
  if (
    lengthValue === undefined ||
    !Number.isSafeInteger(lengthValue) ||
    lengthValue < 0 ||
    lengthValue > 256 ||
    Reflect.ownKeys(descriptors).length !== lengthValue + 1
  ) {
    throw new TypeError(`${label} must be a dense string array`);
  }
  const snapshot: string[] = [];
  for (let index = 0; index < lengthValue; index += 1) {
    const descriptor = descriptors[String(index)];
    if (
      descriptor === undefined ||
      !("value" in descriptor) ||
      descriptor.enumerable !== true ||
      typeof descriptor.value !== "string"
    ) {
      throw new TypeError(`${label} must be a dense string array`);
    }
    snapshot.push(descriptor.value);
  }
  return Object.freeze(snapshot);
}

function dataProperties(value: unknown): Readonly<Record<string, unknown>> {
  const properties = snapshotGovernedCandidateOptions(
    value,
    OPTION_KEYS,
    "Governed candidate assembly options",
  );
  if (
    !["adapter", "evidenceLedger", "reconciliationIndex", "snapshot"].every((key) =>
      Object.hasOwn(properties, key))
  ) {
    throw new TypeError("Governed candidate assembly options have an unexpected shape");
  }
  return properties;
}

function exactSuspensions(value: unknown): ReadonlySet<GovernedCandidateOperation> {
  if (value === undefined) return new Set<GovernedCandidateOperation>();
  if (!Array.isArray(value) || utilTypes.isProxy(value)) {
    throw new TypeError("suspendedTools must be a unique candidate-operation subset");
  }
  const descriptors = Object.getOwnPropertyDescriptors(value);
  const length = Object.getOwnPropertyDescriptor(value, "length");
  const lengthValue =
    length !== undefined && "value" in length && typeof length.value === "number"
      ? length.value
      : undefined;
  if (
    lengthValue === undefined ||
    !Number.isSafeInteger(lengthValue) ||
    lengthValue < 0 ||
    lengthValue > GOVERNED_CANDIDATE_OPERATIONS.length ||
    Reflect.ownKeys(descriptors).length !== lengthValue + 1
  ) {
    throw new TypeError("suspendedTools must be a unique candidate-operation subset");
  }
  const snapshot: GovernedCandidateOperation[] = [];
  for (let index = 0; index < lengthValue; index += 1) {
    const descriptor = descriptors[String(index)];
    if (
      descriptor === undefined ||
      !("value" in descriptor) ||
      descriptor.enumerable !== true ||
      typeof descriptor.value !== "string" ||
      !GOVERNED_CANDIDATE_OPERATIONS.includes(
        descriptor.value as GovernedCandidateOperation,
      )
    ) {
      throw new TypeError("suspendedTools must be a unique candidate-operation subset");
    }
    snapshot.push(descriptor.value as GovernedCandidateOperation);
  }
  if (new Set(snapshot).size !== snapshot.length) {
    throw new TypeError("suspendedTools must be a unique candidate-operation subset");
  }
  return new Set(snapshot);
}

function exactProviderHealth(adapter: OnsDataApiAdapter): AdapterHealth {
  requirePristineOnsDataApiAdapter(adapter);
  const health = adapter.health();
  if (
    health.adapterId !== ONS_ADAPTER_ID ||
    (health.discovery !== "active" && health.discovery !== "suspended") ||
    (health.invocation !== "active" && health.invocation !== "suspended") ||
    health.network !== "not-checked" ||
    Object.keys(health).sort().join(",") !==
      "adapterId,discovery,invocation,network"
  ) {
    throw new TypeError("The governed candidate provider lifecycle is invalid");
  }
  return Object.freeze({ ...health });
}

function publicPolicyOperations(ledger: PublicEvidenceLedger): ReadonlySet<string> {
  return new Set([
    ...PUBLIC_CATALOGUE_POLICY.rules.map(({ operation }) => operation),
    ...PUBLIC_EVIDENCE_INSPECTION_POLICY.rules.map(({ operation }) => operation),
    ...PUBLIC_READ_POLICY.rules.map(({ operation }) => operation),
  ]);
}

function mcpResources(
  operations: readonly GovernedCandidateOperation[],
): GovernedCandidateAssembly["mcpResources"] {
  const resources: ("catalogue.public" | "catalogue.record" | "evidence.receipt")[] = [];
  if (
    operations.includes("catalogue.search") &&
    operations.includes("catalogue.describe")
  ) {
    resources.push("catalogue.public");
  }
  if (operations.includes("catalogue.describe")) resources.push("catalogue.record");
  if (operations.includes("evidence.inspect")) resources.push("evidence.receipt");
  return Object.freeze(resources);
}

function suspensionMap(
  explicit: ReadonlySet<GovernedCandidateOperation>,
  policy: ReadonlySet<string>,
  health: AdapterHealth,
): ReadonlyMap<GovernedCandidateOperation, GovernedCandidateSuspensionSource> {
  const suspended = new Map<GovernedCandidateOperation, GovernedCandidateSuspensionSource>();
  for (const operation of GOVERNED_CANDIDATE_OPERATIONS) {
    if (explicit.has(operation)) {
      suspended.set(operation, "explicit-tool-suspension");
    } else if (!policy.has(operation)) {
      suspended.set(operation, "policy");
    }
  }
  if (health.discovery !== "active") {
    if (!suspended.has("selection.resolve")) {
      suspended.set("selection.resolve", "provider-discovery");
    }
    if (!suspended.has("data.query")) {
      suspended.set("data.query", "provider-discovery");
    }
  } else if (health.invocation !== "active" && !suspended.has("data.query")) {
    suspended.set("data.query", "provider-invocation");
  }
  if (suspended.has("evidence.inspect") && !suspended.has("data.query")) {
    suspended.set("data.query", "required-evidence-operation");
  }
  return suspended;
}

/**
 * Assemble the exact repository-reviewed v0.2 read-only candidate.
 *
 * This is an explicit embedding constructor, not a shipped entrypoint. Registry,
 * policy and provider state may only reduce its exact five-tool projection;
 * production registration remains false and planned profiles cannot be added.
 */
export function createGovernedCandidateAssembly(
  suppliedOptions: GovernedCandidateAssemblyOptions,
): GovernedCandidateAssembly {
  const options = dataProperties(suppliedOptions);
  const snapshot = requireExactCatalogueSnapshot(options.snapshot);
  const evidenceLedger = options.evidenceLedger as PublicEvidenceLedger;
  const reconciliationIndex = options.reconciliationIndex as
    PublicEvidenceReconciliationIndex;
  const adapter = requirePristineOnsDataApiAdapter(options.adapter);
  const health = exactProviderHealth(adapter);
  const verifyProviderReadiness = (): void => {
    const current = exactProviderHealth(adapter);
    if (
      current.discovery !== health.discovery ||
      current.invocation !== health.invocation
    ) {
      throw new TypeError("The governed candidate provider lifecycle changed");
    }
  };
  const explicitSuspensions = exactSuspensions(options.suspendedTools);
  const integrity = createEvidenceReadinessIntegrity(
    evidenceLedger,
    reconciliationIndex,
  );
  const software: EvidenceSoftwareIdentity = Object.freeze({
    name: "gis-ai-go-mcp-gateway",
    version: gatewayMetadata.version,
    revision: snapshot.revision,
  });
  const now = options.now as (() => Date) | undefined;
  if (now !== undefined && typeof now !== "function") {
    throw new TypeError("Governed candidate assembly now must be a function");
  }
  const approvedCache = options.approvedCache as ApprovedOnsDataQueryCache | undefined;

  const catalogueApplication = createCatalogueApplication(snapshot, {
    software,
    evidenceLedger,
    ...(now === undefined ? {} : { now }),
  });
  const selectionApplication = createSelectionResolveApplication({
    software,
    evidenceLedger,
    ...(now === undefined ? {} : { now }),
  });
  const dataQueryApplication = createDataQueryApplication({
    adapter,
    governedPristineExecution: GOVERNED_PRISTINE_ONS_EXECUTION,
    software,
    evidenceLedger,
    reconciliationIndex,
    ...(approvedCache === undefined ? {} : { approvedCache }),
    ...(now === undefined ? {} : { now }),
  });
  const evidenceApplication = createEvidenceInspectApplication(
    evidenceLedger,
    reconciliationIndex,
    {
      software,
      ...(now === undefined ? {} : { now }),
    },
  );

  const suspended = suspensionMap(
    explicitSuspensions,
    publicPolicyOperations(evidenceLedger),
    health,
  );
  const operations = Object.freeze(
    GOVERNED_CANDIDATE_OPERATIONS.filter((operation) => !suspended.has(operation)),
  );
  const suspensions = Object.freeze(
    GOVERNED_CANDIDATE_OPERATIONS.flatMap((operation) => {
      const source = suspended.get(operation);
      return source === undefined
        ? []
        : [Object.freeze({ operation, source })];
    }),
  );
  const assembly: GovernedCandidateAssembly = Object.freeze({
    kind: GOVERNED_CANDIDATE_ASSEMBLY_KIND,
    state: "candidate-unregistered",
    productionRegistration: false,
    operations,
    apiOperations: operations,
    mcpOperations: operations,
    mcpResources: mcpResources(operations),
    suspensions,
    bindings: Object.freeze({
      registry: Object.freeze({
        schema: TOOL_REGISTRY_DOCUMENT.schema,
        version: TOOL_REGISTRY_DOCUMENT.version,
      }),
      policies: Object.freeze([
        PUBLIC_CATALOGUE_POLICY.policy_id,
        PUBLIC_EVIDENCE_INSPECTION_POLICY.policy_id,
        PUBLIC_READ_POLICY.policy_id,
      ]) as readonly [string, string, string],
      provider: Object.freeze({
        adapterId: ONS_ADAPTER_ID,
        adapterVersion: ONS_ADAPTER_VERSION,
        discovery: health.discovery,
        invocation: health.invocation,
      }),
      evidence: Object.freeze({
        ledgerId: evidenceLedger.descriptor.ledger_id,
        reconciliationIndexId: reconciliationIndex.descriptor.index_id,
      }),
    }),
  });
  ASSEMBLY_BINDINGS.set(
    assembly,
    Object.freeze({
      snapshot,
      catalogueApplication,
      evidenceApplication,
      selectionApplication,
      dataQueryApplication,
      evidenceReadinessIntegrity: integrity,
      verifyProviderReadiness,
    }),
  );
  return assembly;
}

/** Resolve only a genuine assembly created by this module. */
export function governedCandidateAssemblyBindings(
  assembly: GovernedCandidateAssembly,
): GovernedCandidateAssemblyBindings {
  if (
    typeof assembly !== "object" ||
    assembly === null ||
    utilTypes.isProxy(assembly)
  ) {
    throw new TypeError("Governed candidate assembly is invalid");
  }
  const bindings = ASSEMBLY_BINDINGS.get(assembly);
  if (bindings === undefined) {
    throw new TypeError("Governed candidate assembly is invalid");
  }
  return bindings;
}

/** Re-verify dependencies for one operation that remains in the advertised subset. */
export function verifyGovernedCandidateOperation(
  assembly: GovernedCandidateAssembly,
  operation: GovernedCandidateOperation,
): void {
  const bindings = governedCandidateAssemblyBindings(assembly);
  if (
    !GOVERNED_CANDIDATE_OPERATIONS.includes(operation) ||
    !assembly.operations.includes(operation)
  ) {
    throw new TypeError("Governed candidate operation is not advertised");
  }
  verifyEvidenceReadinessIntegrity(bindings.evidenceReadinessIntegrity);
  bindings.verifyProviderReadiness();
}

/** Re-verify the exact evidence pair and current candidate operation set. */
export function assessGovernedCandidateReadiness(
  assembly: GovernedCandidateAssembly,
): GovernedCandidateReadiness {
  const bindings = governedCandidateAssemblyBindings(assembly);
  try {
    verifyEvidenceReadinessIntegrity(bindings.evidenceReadinessIntegrity);
  } catch {
    return Object.freeze({
      status: "blocked",
      reason: "evidence-integrity-failed",
      productionRegistration: false,
      activeTools: assembly.operations,
      activeApiOperations: assembly.operations,
    });
  }
  try {
    bindings.verifyProviderReadiness();
  } catch {
    return Object.freeze({
      status: "blocked",
      reason: "relevant-capability-suspended",
      productionRegistration: false,
      activeTools: assembly.operations,
      activeApiOperations: assembly.operations,
    });
  }
  if (
    assembly.operations.length !== GOVERNED_CANDIDATE_OPERATIONS.length ||
    assembly.operations.some(
      (operation, index) => operation !== GOVERNED_CANDIDATE_OPERATIONS[index],
    )
  ) {
    return Object.freeze({
      status: "blocked",
      reason: "relevant-capability-suspended",
      productionRegistration: false,
      activeTools: assembly.operations,
      activeApiOperations: assembly.operations,
    });
  }
  try {
    if (
      evidenceReconciliationClaimCapacity(bindings.evidenceReadinessIntegrity).status ===
      "exhausted"
    ) {
      return Object.freeze({
        status: "blocked",
        reason: "reconciliation-capacity-exhausted",
        productionRegistration: false,
        activeTools: assembly.operations,
        activeApiOperations: assembly.operations,
      });
    }
  } catch {
    return Object.freeze({
      status: "blocked",
      reason: "evidence-integrity-failed",
      productionRegistration: false,
      activeTools: assembly.operations,
      activeApiOperations: assembly.operations,
    });
  }
  return Object.freeze({
    status: "ready",
    reason: "candidate-assembly-verified",
    productionRegistration: false,
    activeTools: assembly.operations,
    activeApiOperations: assembly.operations,
  });
}
