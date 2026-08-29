import {
  ACCESS_STATES,
  AUTHORITY_CLASSES,
  FRESHNESS_STATUSES,
  RECORD_TYPES,
  RIGHTS_STATES,
  analyseCatalogueQuery,
  searchRecords,
  type AccessState,
  type AuthorityClass,
  type CatalogueBundle,
  type CatalogueRecord,
  type ExplorerState,
  type FreshnessStatus,
  type RecordType,
  type RightsState,
} from "@gis-ai-go/contracts";

const CONTROL_CHARACTER = /[\u0000-\u001f\u007f]/u;
const BIDI_CONTROL = /[\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]/u;
const SEARCH_KEYS = new Set(["query", "facets", "limit"]);
const FACET_KEYS = new Set([
  "types",
  "authority",
  "access",
  "rights",
  "freshness",
  "tags",
]);

export const WEBMCP_PAGE_RESULT_SCHEMA = "gis-ai-go.webmcp-page-result.v1" as const;

export class PageToolInputError extends Error {
  public constructor(
    public readonly code:
      | "invalid_arguments"
      | "query_too_complex"
      | "record_not_found",
    message: string,
  ) {
    super(message);
    this.name = "PageToolInputError";
  }
}

interface SearchFacets {
  readonly types: readonly RecordType[];
  readonly authority: readonly AuthorityClass[];
  readonly access: readonly AccessState[];
  readonly rights: readonly RightsState[];
  readonly freshness: readonly FreshnessStatus[];
  readonly tags: readonly string[];
}

export interface PageSearchInput {
  readonly query: string;
  readonly facets: SearchFacets;
  readonly limit: number;
}

export interface PageDescribeInput {
  readonly recordId: string;
}

interface CatalogueIdentity {
  readonly id: string;
  readonly version: string;
  readonly revision: string;
  readonly record_count: number;
}

interface PageBoundary {
  readonly data_scope: "validated public catalogue metadata only";
  readonly page_scoped: true;
  readonly provider_call: false;
  readonly durable_receipt: false;
  readonly persistent_service: false;
  readonly visible_page_update: true;
}

export interface CompactRecord {
  readonly id: string;
  readonly type: RecordType;
  readonly title: string;
  readonly description: string;
  readonly description_truncated: boolean;
  readonly authority_class: AuthorityClass;
  readonly access_state: AccessState;
  readonly rights_state: RightsState;
  readonly freshness_status: FreshnessStatus;
  readonly tags: readonly string[];
}

export interface DetailedRecord extends CompactRecord {
  readonly authority: CatalogueRecord["authority"];
  readonly access: CatalogueRecord["access"];
  readonly rights: CatalogueRecord["rights"];
  readonly freshness: CatalogueRecord["freshness"];
  readonly status: CatalogueRecord["status"];
  readonly source_refs: readonly string[];
  readonly source_records: readonly CompactRecord[];
  readonly limitations: readonly string[];
}

export interface PageSearchResult {
  readonly schema: typeof WEBMCP_PAGE_RESULT_SCHEMA;
  readonly page_tool: "explorer_search_catalogue";
  readonly related_gateway_operation: "catalogue.search";
  readonly catalogue: CatalogueIdentity;
  readonly matches: {
    readonly total: number;
    readonly returned: number;
    readonly truncated: boolean;
    readonly records: readonly CompactRecord[];
  };
  readonly boundary: PageBoundary;
}

export interface PageDescribeResult {
  readonly schema: typeof WEBMCP_PAGE_RESULT_SCHEMA;
  readonly page_tool: "explorer_describe_record";
  readonly related_gateway_operation: "catalogue.describe";
  readonly catalogue: CatalogueIdentity;
  readonly record: DetailedRecord;
  readonly boundary: PageBoundary;
}

export type PageToolResult = PageSearchResult | PageDescribeResult;

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return (
    typeof value === "object" &&
    value !== null &&
    !Array.isArray(value) &&
    (Object.getPrototypeOf(value) === Object.prototype || Object.getPrototypeOf(value) === null)
  );
}

function assertExactKeys(
  value: Record<string, unknown>,
  allowed: ReadonlySet<string>,
  label: string,
): void {
  const unexpected = Object.keys(value).filter((key) => !allowed.has(key));
  if (unexpected.length > 0) {
    throw new PageToolInputError(
      "invalid_arguments",
      `${label} contains unsupported fields: ${unexpected.sort().join(", ")}.`,
    );
  }
}

function boundedText(value: unknown, label: string, maximum: number): string {
  if (typeof value !== "string" || value.length === 0) {
    throw new PageToolInputError("invalid_arguments", `${label} must be a non-empty string.`);
  }
  if (Array.from(value).length > maximum) {
    throw new PageToolInputError(
      "invalid_arguments",
      `${label} exceeds the ${maximum}-character limit.`,
    );
  }
  if (CONTROL_CHARACTER.test(value) || BIDI_CONTROL.test(value)) {
    throw new PageToolInputError(
      "invalid_arguments",
      `${label} contains an unsupported control character.`,
    );
  }
  return value;
}

function enumArray<T extends string>(
  value: unknown,
  label: string,
  allowed: readonly T[],
  maximum: number,
): readonly T[] {
  if (!Array.isArray(value) || value.length < 1 || value.length > maximum) {
    throw new PageToolInputError(
      "invalid_arguments",
      `${label} must contain between 1 and ${maximum} values.`,
    );
  }
  if (value.some((item) => typeof item !== "string" || !allowed.includes(item as T))) {
    throw new PageToolInputError("invalid_arguments", `${label} contains an unsupported value.`);
  }
  if (new Set(value).size !== value.length) {
    throw new PageToolInputError("invalid_arguments", `${label} must not contain duplicates.`);
  }
  return value as readonly T[];
}

function tagArray(value: unknown): readonly string[] {
  if (!Array.isArray(value) || value.length < 1 || value.length > 10) {
    throw new PageToolInputError(
      "invalid_arguments",
      "facets.tags must contain between 1 and 10 values.",
    );
  }
  const tags = value.map((item, index) => boundedText(item, `facets.tags[${index}]`, 128));
  if (new Set(tags).size !== tags.length) {
    throw new PageToolInputError("invalid_arguments", "facets.tags must not contain duplicates.");
  }
  return tags;
}

function parseFacets(value: unknown): SearchFacets {
  const empty: SearchFacets = {
    types: [],
    authority: [],
    access: [],
    rights: [],
    freshness: [],
    tags: [],
  };
  if (value === undefined) return empty;
  if (!isPlainObject(value) || Object.keys(value).length === 0) {
    throw new PageToolInputError(
      "invalid_arguments",
      "facets must be a non-empty object when supplied.",
    );
  }
  assertExactKeys(value, FACET_KEYS, "facets");
  return {
    types:
      value.types === undefined ? [] : enumArray(value.types, "facets.types", RECORD_TYPES, 5),
    authority:
      value.authority === undefined
        ? []
        : enumArray(value.authority, "facets.authority", AUTHORITY_CLASSES, 3),
    access:
      value.access === undefined
        ? []
        : enumArray(value.access, "facets.access", ACCESS_STATES, 3),
    rights:
      value.rights === undefined
        ? []
        : enumArray(value.rights, "facets.rights", RIGHTS_STATES, 3),
    freshness:
      value.freshness === undefined
        ? []
        : enumArray(value.freshness, "facets.freshness", FRESHNESS_STATUSES, 2),
    tags: value.tags === undefined ? [] : tagArray(value.tags),
  };
}

export function parsePageSearchInput(value: unknown): PageSearchInput {
  if (!isPlainObject(value)) {
    throw new PageToolInputError("invalid_arguments", "Search arguments must be an object.");
  }
  assertExactKeys(value, SEARCH_KEYS, "Search arguments");
  const query = boundedText(value.query, "query", 256);
  const analysis = analyseCatalogueQuery(query);
  if (analysis.terms.length === 0) {
    throw new PageToolInputError("invalid_arguments", "query must contain a searchable term.");
  }
  if (analysis.exceedsCharacterLimit || analysis.exceedsTermLimit) {
    throw new PageToolInputError(
      "query_too_complex",
      "query accepts 1 to 10 searchable catalogue keywords (up to 256 characters), " +
        "not a full question. Try 'ONS statistics'.",
    );
  }
  const limit = value.limit ?? 5;
  if (!Number.isInteger(limit) || (limit as number) < 1 || (limit as number) > 5) {
    throw new PageToolInputError("invalid_arguments", "limit must be an integer from 1 to 5.");
  }
  return { query, facets: parseFacets(value.facets), limit: limit as number };
}

export function parsePageDescribeInput(value: unknown): PageDescribeInput {
  if (!isPlainObject(value)) {
    throw new PageToolInputError("invalid_arguments", "Describe arguments must be an object.");
  }
  assertExactKeys(value, new Set(["record_id"]), "Describe arguments");
  return { recordId: boundedText(value.record_id, "record_id", 512) };
}

function catalogueIdentity(bundle: CatalogueBundle): CatalogueIdentity {
  return {
    id: bundle.id,
    version: bundle.version,
    revision: bundle.revision,
    record_count: bundle.recordCount,
  };
}

function boundary(): PageBoundary {
  return {
    data_scope: "validated public catalogue metadata only",
    page_scoped: true,
    provider_call: false,
    durable_receipt: false,
    persistent_service: false,
    visible_page_update: true,
  };
}

function compactText(value: string, maximum: number): { text: string; truncated: boolean } {
  const characters = Array.from(value);
  if (characters.length <= maximum) return { text: value, truncated: false };
  return { text: `${characters.slice(0, maximum - 1).join("")}…`, truncated: true };
}

function compactRecord(record: CatalogueRecord): CompactRecord {
  const description = compactText(record.description, 240);
  return {
    id: record.id,
    type: record.type,
    title: record.title,
    description: description.text,
    description_truncated: description.truncated,
    authority_class: record.authority.class,
    access_state: record.access.state,
    rights_state: record.rights.state,
    freshness_status: record.freshness.status,
    tags: record.tags.slice(0, 8),
  };
}

export function executePageSearch(
  bundle: CatalogueBundle,
  unknownInput: unknown,
): PageSearchResult {
  const input = parsePageSearchInput(unknownInput);
  const state: ExplorerState = {
    view: "cards",
    query: input.query,
    types: input.facets.types,
    authority: input.facets.authority,
    access: input.facets.access,
    rights: input.facets.rights,
    freshness: input.facets.freshness,
    tags: input.facets.tags,
    selectedRecordId: null,
  };
  const matches = searchRecords(bundle.records, state);
  const returned = matches.slice(0, input.limit).map(compactRecord);
  return {
    schema: WEBMCP_PAGE_RESULT_SCHEMA,
    page_tool: "explorer_search_catalogue",
    related_gateway_operation: "catalogue.search",
    catalogue: catalogueIdentity(bundle),
    matches: {
      total: matches.length,
      returned: returned.length,
      truncated: matches.length > returned.length,
      records: returned,
    },
    boundary: boundary(),
  };
}

export function executePageDescribe(
  bundle: CatalogueBundle,
  unknownInput: unknown,
): PageDescribeResult {
  const input = parsePageDescribeInput(unknownInput);
  const record = bundle.records.find((candidate) => candidate.id === input.recordId);
  if (record === undefined) {
    throw new PageToolInputError(
      "record_not_found",
      "The validated catalogue does not contain that exact record identifier.",
    );
  }
  const compact = compactRecord(record);
  const sources = record.sourceRefs
    .map((sourceId) => bundle.records.find((candidate) => candidate.id === sourceId))
    .filter((candidate): candidate is CatalogueRecord => candidate !== undefined)
    .map(compactRecord);
  return {
    schema: WEBMCP_PAGE_RESULT_SCHEMA,
    page_tool: "explorer_describe_record",
    related_gateway_operation: "catalogue.describe",
    catalogue: catalogueIdentity(bundle),
    record: {
      ...compact,
      authority: record.authority,
      access: record.access,
      rights: record.rights,
      freshness: record.freshness,
      status: record.status,
      source_refs: record.sourceRefs,
      source_records: sources,
      limitations: record.limitations.slice(0, 8),
    },
    boundary: boundary(),
  };
}
