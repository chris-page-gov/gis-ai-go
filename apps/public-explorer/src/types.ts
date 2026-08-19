export const RECORD_TYPES = ["bundle", "dataset", "provider", "source", "workflow"] as const;
export type RecordType = (typeof RECORD_TYPES)[number];

export const AUTHORITY_CLASSES = [
  "derived",
  "project-authoritative",
  "source-authoritative",
] as const;
export type AuthorityClass = (typeof AUTHORITY_CLASSES)[number];

export const ACCESS_STATES = ["planned-non-executing", "public", "public-metadata"] as const;
export type AccessState = (typeof ACCESS_STATES)[number];

export const RIGHTS_STATES = [
  "metadata-citation",
  "open-with-conditions",
  "project-mit",
] as const;
export type RightsState = (typeof RIGHTS_STATES)[number];

export const RECORD_STATUSES = [
  "candidate",
  "candidate-metadata",
  "candidate-non-executing",
  "external-source",
] as const;
export type RecordStatus = (typeof RECORD_STATUSES)[number];

export const FRESHNESS_STATUSES = ["current", "review-required"] as const;
export type FreshnessStatus = (typeof FRESHNESS_STATUSES)[number];

export const EXPLORER_VIEWS = ["cards", "graph", "timeline", "map"] as const;
export type ExplorerView = (typeof EXPLORER_VIEWS)[number];

export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | readonly JsonValue[] | { readonly [key: string]: JsonValue };

export interface RecordAuthority {
  readonly class: AuthorityClass;
  readonly statement: string;
  readonly source: string;
}

export interface PublicationEnvelope {
  readonly classification: "public";
  readonly containsPersonalData: false;
  readonly containsProtectedData: false;
}

export interface RecordAccess {
  readonly tier: "open";
  readonly state: AccessState;
  readonly authentication: string;
}

export interface RecordRights {
  readonly state: RightsState;
  readonly recordLicence: string;
  readonly describedResourceLicence: string;
  readonly attribution: string;
}

export interface RecordFreshness {
  readonly observedAt: string;
  readonly reviewedAt: string;
  readonly staleAfter: string;
  readonly status: FreshnessStatus;
}

export interface CatalogueRecord {
  readonly schema: "gis-ai-go-okf-concept.v1";
  readonly id: string;
  readonly type: RecordType;
  readonly title: string;
  readonly description: string;
  readonly authority: RecordAuthority;
  readonly publication: PublicationEnvelope;
  readonly access: RecordAccess;
  readonly rights: RecordRights;
  readonly freshness: RecordFreshness;
  readonly status: RecordStatus;
  readonly sourceRefs: readonly string[];
  readonly limitations: readonly string[];
  readonly tags: readonly string[];
  readonly details: Readonly<Record<string, JsonValue>>;
}

export interface CatalogueBundle {
  readonly schema: "gis-ai-go-okf-bundle.v1";
  readonly id: string;
  readonly title: string;
  readonly description: string;
  readonly okfVersion: "0.2";
  readonly profile: string;
  readonly profileStatus: "candidate-pending-consumer-acceptance";
  readonly version: string;
  readonly revision: string;
  readonly status: "candidate";
  readonly authority: {
    readonly bundleAuthority: string;
    readonly officialSourceAuthority: string;
    readonly legalAdvice: false;
    readonly notEndorsedBySource: true;
  };
  readonly scope: {
    readonly kind: "bounded-public-metadata-discovery";
    readonly metadataOnly: true;
    readonly containsProtectedData: false;
    readonly excludes: readonly string[];
  };
  readonly rights: {
    readonly statement: string;
    readonly thirdPartyNotices: "THIRD_PARTY.md";
  };
  readonly observedAt: string;
  readonly reviewedAt: string;
  readonly staleAfter: string;
  readonly recordCount: number;
  readonly records: readonly CatalogueRecord[];
}

export interface ExplorerState {
  readonly view: ExplorerView;
  readonly query: string;
  readonly types: readonly RecordType[];
  readonly authority: readonly AuthorityClass[];
  readonly access: readonly AccessState[];
  readonly rights: readonly RightsState[];
  readonly freshness: readonly FreshnessStatus[];
  readonly tags: readonly string[];
  readonly selectedRecordId: string | null;
}

export interface FacetOption<T extends string = string> {
  readonly value: T;
  readonly count: number;
}

export interface FacetOptions {
  readonly types: readonly FacetOption<RecordType>[];
  readonly authority: readonly FacetOption<AuthorityClass>[];
  readonly access: readonly FacetOption<AccessState>[];
  readonly rights: readonly FacetOption<RightsState>[];
  readonly freshness: readonly FacetOption<FreshnessStatus>[];
  readonly tags: readonly FacetOption[];
}

export interface GraphNode {
  readonly id: string;
  readonly type: RecordType;
  readonly title: string;
  readonly status: RecordStatus;
  readonly explicitlyIncluded: boolean;
}

export interface GraphEdge {
  readonly from: string;
  readonly to: string;
  readonly relation: "source";
  readonly selfReference: boolean;
}

export interface GraphAdjacency {
  readonly recordId: string;
  readonly recordTitle: string;
  readonly sourceIds: readonly string[];
}

export interface GraphModel {
  readonly nodes: readonly GraphNode[];
  readonly edges: readonly GraphEdge[];
  readonly adjacency: readonly GraphAdjacency[];
}

export const TIMELINE_EVENT_KINDS = [
  "observation",
  "modification",
  "publication",
  "release",
] as const;
export type TimelineEventKind = (typeof TIMELINE_EVENT_KINDS)[number];

export interface TimelineEvent {
  readonly id: string;
  readonly recordId: string;
  readonly recordTitle: string;
  readonly kind: TimelineEventKind;
  readonly date: string;
}

export interface TimelineMissingSummary {
  readonly kind: TimelineEventKind;
  readonly recordCount: number;
}

export interface TimelineModel {
  readonly events: readonly TimelineEvent[];
  readonly missing: readonly TimelineMissingSummary[];
}
