export const TOOL_PROFILE_IDS = Object.freeze([
  "T01",
  "T02",
  "T03",
  "T04",
  "T05",
  "T06",
  "T07",
  "T08",
  "T09",
  "T10",
  "T11",
  "T12",
] as const);

export const TOOL_PROFILE_NAMES = Object.freeze([
  "catalogue.search",
  "catalogue.describe",
  "selection.resolve",
  "data.query",
  "spatial.locate",
  "spatial.analyse",
  "statistics.compare",
  "route.plan",
  "map.render",
  "artefact.export",
  "evidence.inspect",
  "workflow.execute",
] as const);

export const V02_TARGET_ACTIVE_TOOL_NAMES = Object.freeze([
  "catalogue.search",
  "catalogue.describe",
  "selection.resolve",
  "data.query",
  "evidence.inspect",
] as const);

export const ACTIVATION_REQUIREMENTS = Object.freeze([
  "implementation",
  "release",
  "policy",
  "read-only",
  "schema",
  "threat",
  "evidence",
  "interoperability",
  "fallback",
] as const);

export type ToolProfileId = (typeof TOOL_PROFILE_IDS)[number];
export type ToolProfileName = (typeof TOOL_PROFILE_NAMES)[number];
export type V02TargetActiveToolName = (typeof V02_TARGET_ACTIVE_TOOL_NAMES)[number];
export type ActivationRequirement = (typeof ACTIVATION_REQUIREMENTS)[number];

export type ImplementationState = "implemented" | "not-implemented";
export type LifecycleState = "active" | "planned" | "retired" | "suspended";
export type V02LifecycleState = "active" | "planned";
export type ReleaseTarget = "v0.2.0" | "later-reviewed-release" | "v0.3.0";

export interface ActivationGates {
  readonly releaseEnabled: boolean;
  readonly policy: boolean;
  readonly schema: boolean;
  readonly threat: boolean;
  readonly evidence: boolean;
  readonly interoperability: boolean;
  readonly fallback: boolean;
}

export interface CurrentToolState {
  readonly implementationState: ImplementationState;
  readonly lifecycleState: LifecycleState;
  readonly discoveryEligible: boolean;
  readonly activationGates: ActivationGates;
}

export interface V02TargetState {
  readonly lifecycleState: V02LifecycleState;
  readonly discoveryIntended: boolean;
  /** Target lifecycle data is governance metadata and has no runtime authority. */
  readonly runtimeAuthority: false;
}

export interface AcceptedRuntimeSchemaReference {
  readonly state: "accepted";
  readonly ref: string;
}

export interface MissingRuntimeSchemaReference {
  readonly state: "missing";
  readonly ref: null;
}

export type RuntimeSchemaReference =
  | AcceptedRuntimeSchemaReference
  | MissingRuntimeSchemaReference;

export interface RuntimeSchemaReferences {
  readonly input: RuntimeSchemaReference;
  readonly output: RuntimeSchemaReference;
  readonly problem: RuntimeSchemaReference;
}

export interface ToolSupport {
  readonly operation: ToolProfileName;
  readonly operationState: "implemented-inactive" | "not-implemented";
  readonly providerState: "candidate-partial" | "planned";
  readonly providerDependencies: readonly string[];
}

export interface CursorMetadata {
  readonly state: "none" | "optional" | "not-implemented";
  readonly maxLength: number | null;
  readonly artefactFallback: "implemented" | "not-implemented";
  readonly researchStatement: string;
}

export interface CrsMetadata {
  readonly state: "not-applicable" | "required-before-implementation";
  readonly requirements: readonly string[];
}

export interface ProvenanceMetadata {
  readonly requiredFields: readonly string[];
}

export interface FallbackMetadata {
  readonly state: "implemented" | "partial" | "not-implemented";
  readonly behaviour: string;
}

export interface ThreatMetadata {
  readonly risks: readonly string[];
}

export interface ToolSource {
  readonly researchId: ToolProfileId;
  readonly pointer: string;
  readonly inputSchemaPointer: string;
  readonly outputSchemaPointer: string;
}

export interface ToolProfile {
  readonly id: ToolProfileId;
  readonly name: ToolProfileName;
  readonly namespace: string;
  readonly purpose: string;
  readonly readOnly: boolean;
  readonly mutating: boolean;
  readonly releaseTarget: ReleaseTarget;
  readonly current: CurrentToolState;
  readonly v02Target: V02TargetState;
  readonly runtimeSchemas: RuntimeSchemaReferences;
  readonly support: ToolSupport;
  readonly accessTiers: readonly string[];
  readonly policyAttributes: readonly string[];
  readonly costPerformance: string;
  /** Research-profile vocabulary; runtime availability is `runtimeSchemas.problem`. */
  readonly controlledErrors: readonly string[];
  readonly cursor: CursorMetadata;
  readonly crs: CrsMetadata;
  readonly provenance: ProvenanceMetadata;
  readonly fallback: FallbackMetadata;
  readonly threats: ThreatMetadata;
  readonly source: ToolSource;
}

export interface ToolRegistrySource {
  readonly decision: {
    readonly path: "docs/decisions/ADR-0009-read-only-mcp-tool-lifecycle.md";
    readonly status: "accepted";
  };
  readonly research: {
    readonly path: "docs/research/2026-08-19/research-pack/data/tool-catalogue.json";
    readonly retrieved: "2026-08-19";
    readonly sha256: string;
    readonly gitBlob: string;
    readonly immutable: true;
    readonly records: readonly ToolProfileId[];
  };
}

export interface ToolRegistryDocument {
  readonly schema: "gis-ai-go.tool-registry.v1";
  readonly version: "1.0.0";
  readonly canonicalOrder: readonly ToolProfileName[];
  readonly activationRequirements: readonly ActivationRequirement[];
  readonly runtimeAuthority: {
    readonly source: "apps/mcp-gateway/src/activation.ts";
    readonly registryCanActivate: false;
    readonly environmentOverride: false;
    readonly productionRegistration: boolean;
  };
  readonly source: ToolRegistrySource;
  readonly tools: readonly ToolProfile[];
}

export interface ToolRegistryFilter {
  readonly ids?: readonly ToolProfileId[];
  readonly names?: readonly ToolProfileName[];
  readonly implementationState?: ImplementationState;
  readonly lifecycleState?: LifecycleState;
  readonly v02LifecycleState?: V02LifecycleState;
  readonly releaseTarget?: ReleaseTarget;
  readonly readOnly?: boolean;
  readonly mutating?: boolean;
  readonly discoveryEligible?: boolean;
}

export interface ToolRegistry {
  readonly document: ToolRegistryDocument;
  list(): readonly ToolProfile[];
  get(name: string): ToolProfile;
  filter(filter: ToolRegistryFilter): readonly ToolProfile[];
  listCurrentCallable(): readonly ToolProfile[];
}
