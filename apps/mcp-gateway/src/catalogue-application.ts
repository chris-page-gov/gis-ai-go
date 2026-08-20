import {
  ACCESS_STATES,
  AUTHORITY_CLASSES,
  FRESHNESS_STATUSES,
  RECORD_STATUSES,
  RECORD_TYPES,
  RIGHTS_STATES,
  analyseCatalogueQuery,
  deriveFacetOptions,
  searchRecords,
  type AccessState,
  type AuthorityClass,
  type CatalogueRecord,
  type ExplorerState,
  type FacetOptions,
  type FreshnessStatus,
  type JsonValue,
  type RecordType,
  type RightsState,
} from "@gis-ai-go/contracts";

import type { CatalogueSnapshot } from "./catalogue-snapshot.js";
import {
  InvalidCatalogueCursorError,
  decodeCatalogueCursor,
  encodeCatalogueCursor,
  sha256CanonicalJson,
} from "./cursor.js";
import {
  assertCatalogueProblemContext,
  throwCatalogueProblem,
  type CatalogueProblemContext,
  type CatalogueProblemFieldCode,
} from "./problem.js";

const SEARCH_REQUEST_KEYS = ["cursor", "facets", "limit", "query"] as const;
const FACET_KEYS = ["access", "authority", "freshness", "rights", "tags", "types"] as const;
const DESCRIBE_REQUEST_KEYS = ["include", "record_id"] as const;
const DESCRIBE_INCLUDES = ["relationships", "sources"] as const;
const DEFAULT_LIMIT = 20;
const MAX_CURSOR_LENGTH = 1_024;
const RESULT_SEMVER = /^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)$/u;
const RESULT_SHA40 = /^[0-9a-f]{40}$/u;
const RESULT_SHA256 = /^[0-9a-f]{64}$/u;
const RESULT_DATE_TIME =
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/u;
const PROBLEM_CONTROL_CHARACTER = /[\u0000-\u001f\u007f]/u;
const SOURCE_NATIVE_STRING_UNSAFE =
  /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]/u;
const SOURCE_NATIVE_KEY_UNSAFE =
  /[\u0000-\u001f\u007f\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]/u;
const SOURCE_NATIVE_DANGEROUS_KEYS = new Set(["__proto__", "constructor", "prototype"]);

type DescribeInclude = (typeof DESCRIBE_INCLUDES)[number];

export interface CatalogueSearchFacets {
  readonly types?: readonly RecordType[];
  readonly authority?: readonly AuthorityClass[];
  readonly access?: readonly AccessState[];
  readonly rights?: readonly RightsState[];
  readonly freshness?: readonly FreshnessStatus[];
  readonly tags?: readonly string[];
}

export interface CatalogueSearchRequest {
  readonly query?: string;
  readonly facets?: CatalogueSearchFacets;
  readonly limit?: number;
  readonly cursor?: string;
}

export interface CatalogueDescribeRequest {
  readonly record_id: string;
  readonly include?: readonly DescribeInclude[];
}

export interface CatalogueIdentity {
  readonly id: string;
  readonly version: string;
  readonly revision: string;
  readonly content_root_sha256: string;
  readonly record_count: number;
  readonly reviewed_at: string;
  readonly stale_after: string;
}

export interface CatalogueRecordSummary {
  readonly id: string;
  readonly type: CatalogueRecord["type"];
  readonly title: string;
  readonly description: string;
  readonly authority: CatalogueRecord["authority"]["class"];
  readonly access: CatalogueRecord["access"]["state"];
  readonly rights: CatalogueRecord["rights"]["state"];
  readonly freshness: CatalogueRecord["freshness"]["status"];
  readonly status: CatalogueRecord["status"];
  readonly tags: readonly string[];
}

export interface CatalogueRecordDetail {
  readonly id: string;
  readonly type: CatalogueRecord["type"];
  readonly title: string;
  readonly description: string;
  readonly authority: {
    readonly class: CatalogueRecord["authority"]["class"];
    readonly statement: string;
    readonly source: string;
  };
  readonly publication: {
    readonly classification: "public";
    readonly contains_personal_data: false;
    readonly contains_protected_data: false;
  };
  readonly access: {
    readonly tier: "open";
    readonly state: CatalogueRecord["access"]["state"];
    readonly authentication: string;
  };
  readonly rights: {
    readonly state: CatalogueRecord["rights"]["state"];
    readonly record_licence: string;
    readonly described_resource_licence: string;
    readonly attribution: string;
  };
  readonly freshness: {
    readonly observed_at: string;
    readonly reviewed_at: string;
    readonly stale_after: string;
    readonly status: CatalogueRecord["freshness"]["status"];
  };
  readonly status: CatalogueRecord["status"];
  readonly source_refs: readonly string[];
  readonly limitations: readonly string[];
  readonly tags: readonly string[];
  readonly details: Readonly<Record<string, JsonValue>>;
}

export interface CatalogueSearchResult {
  readonly schema: "gis-ai-go.catalogue-result.v1";
  readonly operation: "catalogue.search";
  readonly request_id: string;
  readonly trace_id: string;
  readonly catalogue: CatalogueIdentity;
  readonly warnings: readonly string[];
  readonly data: {
    readonly records: readonly CatalogueRecordSummary[];
    readonly facets: FacetOptions;
    readonly page: {
      readonly limit: number;
      readonly returned: number;
      readonly matched: number;
      readonly next_cursor: string | null;
    };
  };
}

export interface CatalogueDescribeResult {
  readonly schema: "gis-ai-go.catalogue-result.v1";
  readonly operation: "catalogue.describe";
  readonly request_id: string;
  readonly trace_id: string;
  readonly catalogue: CatalogueIdentity;
  readonly warnings: readonly string[];
  readonly data: {
    readonly record: CatalogueRecordDetail;
    readonly included: {
      readonly relationships?: readonly {
        readonly relation: "source";
        readonly record_id: string;
      }[];
      readonly sources?: readonly {
        readonly id: string;
        readonly title: string;
        readonly authority: CatalogueRecord["authority"]["class"];
        readonly access: CatalogueRecord["access"]["state"];
        readonly rights: CatalogueRecord["rights"]["state"];
        readonly freshness: CatalogueRecord["freshness"]["status"];
      }[];
    };
  };
}

export interface CatalogueApplication {
  readonly search: (
    request: unknown,
    context: CatalogueProblemContext,
  ) => CatalogueSearchResult;
  readonly describe: (
    request: unknown,
    context: CatalogueProblemContext,
  ) => CatalogueDescribeResult;
}

interface NormalisedSearchRequest {
  readonly query: string;
  readonly facets: {
    readonly types: readonly RecordType[];
    readonly authority: readonly AuthorityClass[];
    readonly access: readonly AccessState[];
    readonly rights: readonly RightsState[];
    readonly freshness: readonly FreshnessStatus[];
    readonly tags: readonly string[];
  };
  readonly limit: number;
  readonly cursor: string | null;
}

interface ResultFacetCount {
  readonly value: string;
  readonly count: number;
}

function codePointLength(value: string): number {
  return Array.from(value).length;
}

function resultContractFailure(path: string, message: string): never {
  throw new Error(`Catalogue result contract rejected at ${path}: ${message}`);
}

function assertResultText(
  value: unknown,
  path: string,
  maximum: number,
  minimum = 1,
): asserts value is string {
  if (
    typeof value !== "string" ||
    codePointLength(value) < minimum ||
    codePointLength(value) > maximum
  ) {
    resultContractFailure(
      path,
      `expected from ${minimum} to ${maximum} Unicode characters`,
    );
  }
}

function assertControlledResultValue(
  value: unknown,
  path: string,
  allowed: readonly string[],
): asserts value is string {
  if (typeof value !== "string" || !allowed.includes(value)) {
    resultContractFailure(path, "value is outside the closed result vocabulary");
  }
}

function assertResultDateTime(value: unknown, path: string): void {
  if (
    typeof value !== "string" ||
    !RESULT_DATE_TIME.test(value) ||
    !Number.isFinite(Date.parse(value))
  ) {
    resultContractFailure(path, "expected an RFC 3339 date-time");
  }
}

function assertResultStringArray(
  value: unknown,
  path: string,
  minimumItems: number,
  maximumItems: number,
  maximumItemLength: number,
): asserts value is readonly string[] {
  if (
    !Array.isArray(value) ||
    value.length < minimumItems ||
    value.length > maximumItems
  ) {
    resultContractFailure(
      path,
      `expected from ${minimumItems} to ${maximumItems} unique strings`,
    );
  }
  value.forEach((item, index) =>
    assertResultText(item, `${path}[${index}]`, maximumItemLength),
  );
  if (new Set(value).size !== value.length) {
    resultContractFailure(path, "strings must be unique");
  }
}

function assertSourceNativeValue(
  value: unknown,
  path: string,
  ancestors: WeakSet<object>,
): void {
  if (value === null || typeof value === "boolean") return;
  if (typeof value === "number") {
    if (!Number.isFinite(value)) {
      resultContractFailure(path, "number must be finite");
    }
    return;
  }
  if (typeof value === "string") {
    if (
      codePointLength(value) > 65_536 ||
      SOURCE_NATIVE_STRING_UNSAFE.test(value)
    ) {
      resultContractFailure(path, "string exceeds the source-native result boundary");
    }
    return;
  }
  if (typeof value !== "object" || value === undefined) {
    resultContractFailure(path, "value is not JSON-compatible");
  }
  if (ancestors.has(value)) {
    resultContractFailure(path, "cyclic values are not permitted");
  }
  ancestors.add(value);

  if (Array.isArray(value)) {
    if (value.length > 10_000) {
      resultContractFailure(path, "array exceeds 10000 items");
    }
    value.forEach((item, index) =>
      assertSourceNativeValue(item, `${path}[${index}]`, ancestors),
    );
    ancestors.delete(value);
    return;
  }

  if (!isPlainObject(value)) {
    resultContractFailure(path, "object must be a plain JSON object");
  }
  const entries = Object.entries(value);
  if (entries.length > 256) {
    resultContractFailure(path, "object exceeds 256 properties");
  }
  entries.forEach(([key, member], index) => {
    if (
      codePointLength(key) < 1 ||
      codePointLength(key) > 256 ||
      SOURCE_NATIVE_KEY_UNSAFE.test(key) ||
      SOURCE_NATIVE_DANGEROUS_KEYS.has(key)
    ) {
      resultContractFailure(
        `${path}.property[${index}]`,
        "property name is outside the source-native result boundary",
      );
    }
    assertSourceNativeValue(member, `${path}.property[${index}].value`, ancestors);
  });
  ancestors.delete(value);
}

function assertResultRecord(record: CatalogueRecord, path: string): void {
  assertResultText(record.id, `${path}.id`, 512);
  assertControlledResultValue(record.type, `${path}.type`, RECORD_TYPES);
  assertResultText(record.title, `${path}.title`, 512);
  assertResultText(record.description, `${path}.description`, 4_096);
  assertControlledResultValue(
    record.authority.class,
    `${path}.authority.class`,
    AUTHORITY_CLASSES,
  );
  assertResultText(record.authority.statement, `${path}.authority.statement`, 4_096);
  assertResultText(record.authority.source, `${path}.authority.source`, 512);
  if (
    record.publication.classification !== "public" ||
    record.publication.containsPersonalData !== false ||
    record.publication.containsProtectedData !== false
  ) {
    resultContractFailure(`${path}.publication`, "publication boundary is not public-only");
  }
  if (record.access.tier !== "open") {
    resultContractFailure(`${path}.access.tier`, "access tier must be open");
  }
  assertControlledResultValue(record.access.state, `${path}.access.state`, ACCESS_STATES);
  assertResultText(record.access.authentication, `${path}.access.authentication`, 512);
  assertControlledResultValue(record.rights.state, `${path}.rights.state`, RIGHTS_STATES);
  assertResultText(record.rights.recordLicence, `${path}.rights.recordLicence`, 2_048);
  assertResultText(
    record.rights.describedResourceLicence,
    `${path}.rights.describedResourceLicence`,
    2_048,
  );
  assertResultText(record.rights.attribution, `${path}.rights.attribution`, 8_192);
  assertResultDateTime(record.freshness.observedAt, `${path}.freshness.observedAt`);
  assertResultDateTime(record.freshness.reviewedAt, `${path}.freshness.reviewedAt`);
  assertResultDateTime(record.freshness.staleAfter, `${path}.freshness.staleAfter`);
  assertControlledResultValue(
    record.freshness.status,
    `${path}.freshness.status`,
    FRESHNESS_STATUSES,
  );
  assertControlledResultValue(record.status, `${path}.status`, RECORD_STATUSES);
  assertResultStringArray(record.sourceRefs, `${path}.sourceRefs`, 1, 100, 512);
  assertResultStringArray(record.limitations, `${path}.limitations`, 1, 50, 2_048);
  assertResultStringArray(record.tags, `${path}.tags`, 0, 50, 128);
  assertSourceNativeValue(record.details, `${path}.details`, new WeakSet<object>());
}

function assertFacetCounts(
  values: readonly ResultFacetCount[],
  path: string,
  maximumItems: number,
  allowedValues?: readonly string[],
): void {
  if (!Array.isArray(values) || values.length > maximumItems) {
    resultContractFailure(path, `facet exceeds ${maximumItems} options`);
  }
  const identities = new Set<string>();
  values.forEach((facet, index) => {
    const itemPath = `${path}[${index}]`;
    if (allowedValues === undefined) {
      assertResultText(facet.value, `${itemPath}.value`, 128);
    } else {
      assertControlledResultValue(facet.value, `${itemPath}.value`, allowedValues);
    }
    if (
      !Number.isInteger(facet.count) ||
      facet.count < 0 ||
      facet.count > 10_000
    ) {
      resultContractFailure(`${itemPath}.count`, "facet count must be from 0 to 10000");
    }
    if (identities.has(facet.value)) {
      resultContractFailure(path, "facet options must be unique");
    }
    identities.add(facet.value);
  });
}

function assertResultFacetBounds(facets: FacetOptions): void {
  assertFacetCounts(facets.types, "$.data.facets.types", 5, RECORD_TYPES);
  assertFacetCounts(facets.authority, "$.data.facets.authority", 3, AUTHORITY_CLASSES);
  assertFacetCounts(facets.access, "$.data.facets.access", 3, ACCESS_STATES);
  assertFacetCounts(facets.rights, "$.data.facets.rights", 3, RIGHTS_STATES);
  assertFacetCounts(facets.freshness, "$.data.facets.freshness", 2, FRESHNESS_STATUSES);
  assertFacetCounts(facets.tags, "$.data.facets.tags", 100);
}

/**
 * Reject any snapshot that could project beyond the closed catalogue-result schema.
 *
 * The shared catalogue parser intentionally supports richer in-process display
 * values, so the gateway must enforce its narrower transport boundary explicitly.
 */
export function assertCatalogueResultSnapshotBounds(snapshot: CatalogueSnapshot): void {
  assertResultText(snapshot.bundle.id, "$.catalogue.id", 512);
  if (!RESULT_SEMVER.test(snapshot.version)) {
    resultContractFailure("$.catalogue.version", "expected a semantic version");
  }
  if (!RESULT_SHA40.test(snapshot.revision)) {
    resultContractFailure("$.catalogue.revision", "expected a lowercase Git SHA");
  }
  if (!RESULT_SHA256.test(snapshot.contentRootSha256)) {
    resultContractFailure(
      "$.catalogue.content_root_sha256",
      "expected a lowercase SHA-256 digest",
    );
  }
  if (
    !Number.isInteger(snapshot.recordCount) ||
    snapshot.recordCount < 1 ||
    snapshot.recordCount > 10_000 ||
    snapshot.recordCount !== snapshot.bundle.records.length
  ) {
    resultContractFailure(
      "$.catalogue.record_count",
      "record count must match from 1 to 10000 records",
    );
  }
  assertResultDateTime(snapshot.bundle.reviewedAt, "$.catalogue.reviewed_at");
  assertResultDateTime(snapshot.bundle.staleAfter, "$.catalogue.stale_after");
  assertResultStringArray(snapshot.warnings, "$.warnings", 0, 20, 1_024);

  if (snapshot.recordsById.size !== snapshot.bundle.records.length) {
    resultContractFailure("$.data.records", "record index does not match the bundle");
  }
  snapshot.bundle.records.forEach((record, index) => {
    assertResultRecord(record, `$.data.records[${index}]`);
    if (snapshot.recordsById.get(record.id) !== record) {
      resultContractFailure(
        `$.data.records[${index}].id`,
        "record index does not reference the canonical bundle record",
      );
    }
  });
  assertResultFacetBounds(deriveFacetOptions(snapshot.bundle.records));
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}

function isProblemBoundedText(value: string, maximum: number): boolean {
  return (
    codePointLength(value) >= 1 &&
    codePointLength(value) <= maximum &&
    !PROBLEM_CONTROL_CHARACTER.test(value)
  );
}

function fieldFailure(
  context: CatalogueProblemContext,
  path: string,
  code: CatalogueProblemFieldCode,
  message: string,
): never {
  throwCatalogueProblem("invalid_request", context, {
    detail: message,
    errors: [{ path, code, message }],
  });
}

function unknownPropertyFailure(
  context: CatalogueProblemContext,
  parentPath: string,
  unknownKey: string,
): never {
  const candidatePath = `${parentPath}.${unknownKey}`;
  const candidateMessage = `Remove the unknown property ${unknownKey}.`;
  const canReflectIdentity =
    isProblemBoundedText(candidatePath, 256) &&
    isProblemBoundedText(candidateMessage, 512);
  fieldFailure(
    context,
    canReflectIdentity ? candidatePath : parentPath,
    "unknown_property",
    canReflectIdentity ? candidateMessage : "Remove the unknown property.",
  );
}

function assertClosedObject(
  value: unknown,
  path: string,
  allowedKeys: readonly string[],
  context: CatalogueProblemContext,
): Record<string, unknown> {
  if (!isPlainObject(value)) {
    fieldFailure(context, path, "invalid_type", "Use a JSON object.");
  }
  const unknownKey = Object.keys(value).find((key) => !allowedKeys.includes(key));
  if (unknownKey !== undefined) {
    unknownPropertyFailure(context, path, unknownKey);
  }
  return value;
}

function hasOwn(value: Record<string, unknown>, key: string): boolean {
  return Object.prototype.hasOwnProperty.call(value, key);
}

function sortedUniqueValues<const T extends string>(
  value: unknown,
  path: string,
  allowed: readonly T[],
  maximum: number,
  context: CatalogueProblemContext,
): readonly T[] {
  if (!Array.isArray(value)) {
    fieldFailure(context, path, "invalid_type", "Use an array of controlled values.");
  }
  if (value.length < 1 || value.length > maximum) {
    fieldFailure(
      context,
      path,
      "out_of_range",
      `Supply between 1 and ${maximum} values.`,
    );
  }
  for (const [index, item] of value.entries()) {
    if (typeof item !== "string" || !allowed.includes(item as T)) {
      fieldFailure(
        context,
        `${path}[${index}]`,
        "invalid_value",
        "Use a value from the governed catalogue facet.",
      );
    }
  }
  const typed = value as T[];
  if (new Set(typed).size !== typed.length) {
    fieldFailure(context, path, "not_unique", "Facet values must be unique.");
  }
  return [...typed].sort();
}

function normaliseFacets(
  value: unknown,
  snapshot: CatalogueSnapshot,
  context: CatalogueProblemContext,
): NormalisedSearchRequest["facets"] {
  if (value === undefined) {
    return { types: [], authority: [], access: [], rights: [], freshness: [], tags: [] };
  }
  const facets = assertClosedObject(value, "$.facets", FACET_KEYS, context);
  if (Object.keys(facets).length === 0) {
    fieldFailure(context, "$.facets", "required", "Supply at least one facet.");
  }
  const availableTags = deriveFacetOptions(snapshot.bundle.records).tags.map(
    ({ value: tag }) => tag,
  );
  return {
    types: hasOwn(facets, "types")
      ? sortedUniqueValues(facets.types, "$.facets.types", RECORD_TYPES, 5, context)
      : [],
    authority: hasOwn(facets, "authority")
      ? sortedUniqueValues(
          facets.authority,
          "$.facets.authority",
          AUTHORITY_CLASSES,
          3,
          context,
        )
      : [],
    access: hasOwn(facets, "access")
      ? sortedUniqueValues(facets.access, "$.facets.access", ACCESS_STATES, 3, context)
      : [],
    rights: hasOwn(facets, "rights")
      ? sortedUniqueValues(facets.rights, "$.facets.rights", RIGHTS_STATES, 3, context)
      : [],
    freshness: hasOwn(facets, "freshness")
      ? sortedUniqueValues(
          facets.freshness,
          "$.facets.freshness",
          FRESHNESS_STATUSES,
          2,
          context,
        )
      : [],
    tags: hasOwn(facets, "tags")
      ? sortedUniqueValues(facets.tags, "$.facets.tags", availableTags, 50, context)
      : [],
  };
}

function normaliseSearchRequest(
  value: unknown,
  snapshot: CatalogueSnapshot,
  context: CatalogueProblemContext,
): NormalisedSearchRequest {
  const request = assertClosedObject(value, "$", SEARCH_REQUEST_KEYS, context);

  let query = "";
  if (hasOwn(request, "query")) {
    if (typeof request.query !== "string") {
      fieldFailure(context, "$.query", "invalid_type", "Use a string query.");
    }
    if (request.query.length === 0) {
      fieldFailure(context, "$.query", "out_of_range", "Query must not be empty.");
    }
    const analysis = analyseCatalogueQuery(request.query);
    if (analysis.exceedsCharacterLimit) {
      fieldFailure(
        context,
        "$.query",
        "out_of_range",
        "Query must not exceed 256 Unicode characters.",
      );
    }
    if (analysis.exceedsTermLimit) {
      throwCatalogueProblem("complexity_limit_exceeded", context, {
        detail: "Query must not exceed 10 normalised terms.",
        errors: [
          {
            path: "$.query",
            code: "out_of_range",
            message: "Use no more than 10 normalised terms.",
          },
        ],
      });
    }
    query = analysis.normalised;
  }

  let limit = DEFAULT_LIMIT;
  if (hasOwn(request, "limit")) {
    if (!Number.isInteger(request.limit)) {
      fieldFailure(context, "$.limit", "invalid_type", "Use an integer page size.");
    }
    if ((request.limit as number) < 1 || (request.limit as number) > 100) {
      fieldFailure(context, "$.limit", "out_of_range", "Use an integer from 1 to 100.");
    }
    limit = request.limit as number;
  }

  let cursor: string | null = null;
  if (hasOwn(request, "cursor")) {
    if (typeof request.cursor !== "string") {
      fieldFailure(context, "$.cursor", "invalid_type", "Use an opaque string cursor.");
    }
    if (request.cursor.length < 1 || request.cursor.length > MAX_CURSOR_LENGTH) {
      fieldFailure(
        context,
        "$.cursor",
        "out_of_range",
        `Cursor must contain from 1 to ${MAX_CURSOR_LENGTH} characters.`,
      );
    }
    cursor = request.cursor;
  }

  return {
    query,
    facets: normaliseFacets(request.facets, snapshot, context),
    limit,
    cursor,
  };
}

function catalogueIdentity(snapshot: CatalogueSnapshot): CatalogueIdentity {
  return {
    id: snapshot.bundle.id,
    version: snapshot.version,
    revision: snapshot.revision,
    content_root_sha256: snapshot.contentRootSha256,
    record_count: snapshot.recordCount,
    reviewed_at: snapshot.bundle.reviewedAt,
    stale_after: snapshot.bundle.staleAfter,
  };
}

function summary(record: CatalogueRecord): CatalogueRecordSummary {
  return {
    id: record.id,
    type: record.type,
    title: record.title,
    description: record.description,
    authority: record.authority.class,
    access: record.access.state,
    rights: record.rights.state,
    freshness: record.freshness.status,
    status: record.status,
    tags: [...record.tags],
  };
}

function cloneJson(value: JsonValue): JsonValue {
  if (Array.isArray(value)) return value.map(cloneJson);
  if (value !== null && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value).map(([key, member]) => [key, cloneJson(member)]),
    );
  }
  return value;
}

function detail(record: CatalogueRecord): CatalogueRecordDetail {
  return {
    id: record.id,
    type: record.type,
    title: record.title,
    description: record.description,
    authority: {
      class: record.authority.class,
      statement: record.authority.statement,
      source: record.authority.source,
    },
    publication: {
      classification: record.publication.classification,
      contains_personal_data: record.publication.containsPersonalData,
      contains_protected_data: record.publication.containsProtectedData,
    },
    access: {
      tier: record.access.tier,
      state: record.access.state,
      authentication: record.access.authentication,
    },
    rights: {
      state: record.rights.state,
      record_licence: record.rights.recordLicence,
      described_resource_licence: record.rights.describedResourceLicence,
      attribution: record.rights.attribution,
    },
    freshness: {
      observed_at: record.freshness.observedAt,
      reviewed_at: record.freshness.reviewedAt,
      stale_after: record.freshness.staleAfter,
      status: record.freshness.status,
    },
    status: record.status,
    source_refs: [...record.sourceRefs],
    limitations: [...record.limitations],
    tags: [...record.tags],
    details: Object.fromEntries(
      Object.entries(record.details).map(([key, member]) => [key, cloneJson(member)]),
    ),
  };
}

function searchState(request: NormalisedSearchRequest): ExplorerState {
  return {
    view: "cards",
    query: request.query,
    types: request.facets.types,
    authority: request.facets.authority,
    access: request.facets.access,
    rights: request.facets.rights,
    freshness: request.facets.freshness,
    tags: request.facets.tags,
    selectedRecordId: null,
  };
}

function criteriaDigest(request: NormalisedSearchRequest): string {
  return sha256CanonicalJson({
    facets: request.facets,
    limit: request.limit,
    query: request.query,
  });
}

function searchCatalogueFromValidatedSnapshot(
  snapshot: CatalogueSnapshot,
  input: unknown,
  context: CatalogueProblemContext,
): CatalogueSearchResult {
  const request = normaliseSearchRequest(input, snapshot, context);
  const state = searchState(request);
  const matched = searchRecords(snapshot.bundle.records, state);
  const digest = criteriaDigest(request);
  const binding = {
    contentRootSha256: snapshot.contentRootSha256,
    criteriaSha256: digest,
    limit: request.limit,
  };

  let offset = 0;
  if (request.cursor !== null) {
    try {
      offset = decodeCatalogueCursor(request.cursor, binding);
    } catch (error) {
      if (!(error instanceof InvalidCatalogueCursorError)) throw error;
      throwCatalogueProblem("invalid_cursor", context, { detail: error.message });
    }
    if (offset >= matched.length) {
      throwCatalogueProblem("invalid_cursor", context, {
        detail: "The cursor points beyond the available results.",
      });
    }
  }

  const pageRecords = matched.slice(offset, offset + request.limit);
  const nextOffset = offset + pageRecords.length;
  const nextCursor =
    nextOffset < matched.length
      ? encodeCatalogueCursor(
          {
            contentRootSha256: snapshot.contentRootSha256,
            criteriaSha256: digest,
          },
          offset + request.limit,
        )
      : null;

  return {
    schema: "gis-ai-go.catalogue-result.v1",
    operation: "catalogue.search",
    request_id: context.requestId,
    trace_id: context.traceId,
    catalogue: catalogueIdentity(snapshot),
    warnings: [...snapshot.warnings],
    data: {
      records: pageRecords.map(summary),
      facets: deriveFacetOptions(snapshot.bundle.records, state),
      page: {
        limit: request.limit,
        returned: pageRecords.length,
        matched: matched.length,
        next_cursor: nextCursor,
      },
    },
  };
}

export function searchCatalogue(
  snapshot: CatalogueSnapshot,
  input: unknown,
  context: CatalogueProblemContext,
): CatalogueSearchResult {
  assertCatalogueProblemContext(context);
  assertCatalogueResultSnapshotBounds(snapshot);
  return searchCatalogueFromValidatedSnapshot(snapshot, input, context);
}

function normaliseDescribeRequest(
  value: unknown,
  context: CatalogueProblemContext,
): { readonly recordId: string; readonly include: ReadonlySet<DescribeInclude> } {
  const request = assertClosedObject(value, "$", DESCRIBE_REQUEST_KEYS, context);
  if (!hasOwn(request, "record_id")) {
    fieldFailure(context, "$.record_id", "required", "Supply a catalogue record ID.");
  }
  if (typeof request.record_id !== "string") {
    fieldFailure(context, "$.record_id", "invalid_type", "Use a string catalogue record ID.");
  }
  if (request.record_id.length === 0 || Array.from(request.record_id).length > 512) {
    fieldFailure(
      context,
      "$.record_id",
      "out_of_range",
      "Record ID must contain from 1 to 512 Unicode characters.",
    );
  }

  let include: readonly DescribeInclude[] = DESCRIBE_INCLUDES;
  if (hasOwn(request, "include")) {
    include = sortedUniqueValues(
      request.include,
      "$.include",
      DESCRIBE_INCLUDES,
      DESCRIBE_INCLUDES.length,
      context,
    );
  }
  return { recordId: request.record_id, include: new Set(include) };
}

function recordNotFoundDetail(recordId: string): string {
  const candidate = `No catalogue record has the exact ID ${recordId}.`;
  return isProblemBoundedText(candidate, 1_024)
    ? candidate
    : "No catalogue record has the supplied exact ID.";
}

function describeCatalogueFromValidatedSnapshot(
  snapshot: CatalogueSnapshot,
  input: unknown,
  context: CatalogueProblemContext,
): CatalogueDescribeResult {
  const request = normaliseDescribeRequest(input, context);
  const record = snapshot.recordsById.get(request.recordId);
  if (record === undefined) {
    throwCatalogueProblem("record_not_found", context, {
      detail: recordNotFoundDetail(request.recordId),
    });
  }

  const sourceIds = [...record.sourceRefs].sort();
  const relationships = sourceIds.map((recordId) => ({
    relation: "source" as const,
    record_id: recordId,
  }));
  const sources = sourceIds.map((recordId) => {
    const source = snapshot.recordsById.get(recordId);
    if (source === undefined) {
      throw new Error(`Validated catalogue source ${recordId} is unavailable`);
    }
    return {
      id: source.id,
      title: source.title,
      authority: source.authority.class,
      access: source.access.state,
      rights: source.rights.state,
      freshness: source.freshness.status,
    };
  });

  return {
    schema: "gis-ai-go.catalogue-result.v1",
    operation: "catalogue.describe",
    request_id: context.requestId,
    trace_id: context.traceId,
    catalogue: catalogueIdentity(snapshot),
    warnings: [...snapshot.warnings],
    data: {
      record: detail(record),
      included: {
        ...(request.include.has("relationships") ? { relationships } : {}),
        ...(request.include.has("sources") ? { sources } : {}),
      },
    },
  };
}

export function describeCatalogue(
  snapshot: CatalogueSnapshot,
  input: unknown,
  context: CatalogueProblemContext,
): CatalogueDescribeResult {
  assertCatalogueProblemContext(context);
  assertCatalogueResultSnapshotBounds(snapshot);
  return describeCatalogueFromValidatedSnapshot(snapshot, input, context);
}

/** Bind the two catalogue operations to one immutable, transport-neutral snapshot. */
export function createCatalogueApplication(snapshot: CatalogueSnapshot): CatalogueApplication {
  assertCatalogueResultSnapshotBounds(snapshot);
  return Object.freeze({
    search: (request: unknown, context: CatalogueProblemContext) => {
      assertCatalogueProblemContext(context);
      return searchCatalogueFromValidatedSnapshot(snapshot, request, context);
    },
    describe: (request: unknown, context: CatalogueProblemContext) => {
      assertCatalogueProblemContext(context);
      return describeCatalogueFromValidatedSnapshot(snapshot, request, context);
    },
  });
}
