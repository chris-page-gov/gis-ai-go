import { isSafeNavigableHref } from "./links.js";
import {
  ACCESS_STATES,
  AUTHORITY_CLASSES,
  FRESHNESS_STATUSES,
  RECORD_STATUSES,
  RECORD_TYPES,
  RIGHTS_STATES,
  TIMELINE_EVENT_KINDS,
  type AccessState,
  type AuthorityClass,
  type CatalogueBundle,
  type CatalogueRecord,
  type ExplorerState,
  type FacetOption,
  type FacetOptions,
  type FreshnessStatus,
  type GraphModel,
  type JsonValue,
  type RecordStatus,
  type RecordType,
  type RightsState,
  type TimelineEvent,
  type TimelineEventKind,
  type TimelineModel,
} from "./types.js";

export const DEFAULT_RECORD_ID = "hmlr:dataset:inspire-index-polygons";
export const DEFAULT_BOUNDARY_CAVEAT =
  "Polygons are indicative and do not establish the exact legal extent of a title.";

export const MAX_CATALOGUE_JSON_BYTES = 8 * 1024 * 1024;
export const MAX_CATALOGUE_RECORDS = 10_000;
const MAX_STRING_LENGTH = 65_536;
const MAX_DISPLAY_STRING_LENGTH = 16_384;
const MAX_ARRAY_ITEMS = 10_000;
const MAX_OBJECT_KEYS = 256;
const MAX_JSON_DEPTH = 16;
const MAX_JSON_NODES = 250_000;
const PUBLICATION_BASE = "https://chris-page-gov.github.io/gis-ai-go/";

const DATE = /^\d{4}-\d{2}-\d{2}$/u;
const DATE_TIME =
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/u;
const SHA_40 = /^[0-9a-f]{40}$/u;
const SEMVER = /^(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)$/u;
const HTML_LIKE = /<\s*(?:!--|!doctype\b|\/?[a-z][^>]*)>/iu;
const CONTROL_CHARACTER = /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/u;
const BIDI_CONTROL = /[\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]/u;
const DANGEROUS_KEYS = new Set(["__proto__", "constructor", "prototype"]);

type ObjectValue = Record<string, unknown>;

function fail(path: string, message: string): never {
  throw new Error(`Invalid catalogue at ${path}: ${message}`);
}

function isObject(value: unknown): value is ObjectValue {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function objectAt(value: unknown, path: string): ObjectValue {
  if (!isObject(value)) {
    fail(path, "expected an object");
  }
  return value;
}

function exactKeys(value: ObjectValue, expected: readonly string[], path: string): void {
  const actual = Object.keys(value).sort();
  const required = [...expected].sort();
  if (actual.length !== required.length || actual.some((key, index) => key !== required[index])) {
    fail(path, `expected keys ${required.join(", ")}; found ${actual.join(", ")}`);
  }
}

function stringAt(
  value: unknown,
  path: string,
  options: { readonly plain?: boolean; readonly max?: number } = {},
): string {
  if (typeof value !== "string" || value.length === 0) {
    fail(path, "expected a non-empty string");
  }
  if (value.length > (options.max ?? MAX_STRING_LENGTH)) {
    fail(path, "string exceeds the permitted length");
  }
  if (CONTROL_CHARACTER.test(value) || BIDI_CONTROL.test(value)) {
    fail(path, "string contains an unsafe control character");
  }
  if (options.plain && HTML_LIKE.test(value)) {
    fail(path, "HTML-like content is not permitted");
  }
  return value;
}

function literalAt<T extends string | boolean>(value: unknown, expected: T, path: string): T {
  if (value !== expected) {
    fail(path, `expected ${JSON.stringify(expected)}`);
  }
  return expected;
}

function enumAt<const T extends readonly string[]>(
  value: unknown,
  values: T,
  path: string,
): T[number] {
  if (typeof value !== "string" || !(values as readonly string[]).includes(value)) {
    fail(path, `expected one of ${values.join(", ")}`);
  }
  return value as T[number];
}

function validCalendarDate(value: string): boolean {
  const datePart = value.slice(0, 10);
  if (!DATE.test(datePart)) {
    return false;
  }
  const [year, month, day] = datePart.split("-").map(Number);
  const candidate = new Date(Date.UTC(year ?? 0, (month ?? 1) - 1, day ?? 1));
  return (
    candidate.getUTCFullYear() === year &&
    candidate.getUTCMonth() + 1 === month &&
    candidate.getUTCDate() === day
  );
}

function dateTimeAt(value: unknown, path: string): string {
  const text = stringAt(value, path, { max: 64 });
  if (!DATE_TIME.test(text) || !validCalendarDate(text) || !Number.isFinite(Date.parse(text))) {
    fail(path, "expected an RFC 3339 date-time");
  }
  return text;
}

function dateLikeAt(value: unknown, path: string): string {
  const text = stringAt(value, path, { max: 64 });
  if (DATE.test(text)) {
    if (!validCalendarDate(text)) {
      fail(path, "expected a valid calendar date");
    }
    return text;
  }
  return dateTimeAt(text, path);
}

function uniqueStringsAt(
  value: unknown,
  path: string,
  options: { readonly plain?: boolean; readonly min?: number } = {},
): readonly string[] {
  if (!Array.isArray(value) || value.length < (options.min ?? 0) || value.length > MAX_ARRAY_ITEMS) {
    fail(path, "expected a bounded string array");
  }
  const strings = value.map((item, index) => {
    const stringOptions =
      options.plain === undefined
        ? { max: MAX_DISPLAY_STRING_LENGTH }
        : { plain: options.plain, max: MAX_DISPLAY_STRING_LENGTH };
    return stringAt(item, `${path}[${index}]`, stringOptions);
  });
  if (new Set(strings).size !== strings.length) {
    fail(path, "values must be unique");
  }
  return strings;
}

function assertSafeJson(value: unknown): void {
  let nodes = 0;
  const ancestors = new WeakSet<object>();

  function visit(item: unknown, path: string, depth: number): void {
    nodes += 1;
    if (nodes > MAX_JSON_NODES) {
      fail(path, "JSON value exceeds the node limit");
    }
    if (depth > MAX_JSON_DEPTH) {
      fail(path, "JSON value exceeds the depth limit");
    }
    if (item === null || typeof item === "boolean") {
      return;
    }
    if (typeof item === "string") {
      stringAt(item, path, { max: MAX_STRING_LENGTH, plain: true });
      return;
    }
    if (typeof item === "number") {
      if (!Number.isFinite(item)) {
        fail(path, "number must be finite");
      }
      return;
    }
    if (typeof item !== "object") {
      fail(path, "value is not JSON-compatible");
    }
    const prototype = Object.getPrototypeOf(item);
    if (prototype !== Object.prototype && prototype !== null && !Array.isArray(item)) {
      fail(path, "object must be a plain JSON object");
    }
    if (ancestors.has(item)) {
      fail(path, "cyclic values are not permitted");
    }
    ancestors.add(item);
    if (Array.isArray(item)) {
      if (item.length > MAX_ARRAY_ITEMS) {
        fail(path, "array exceeds the item limit");
      }
      item.forEach((child, index) => visit(child, `${path}[${index}]`, depth + 1));
    } else {
      const keys = Object.keys(item);
      if (keys.length > MAX_OBJECT_KEYS) {
        fail(path, "object exceeds the key limit");
      }
      for (const key of keys) {
        if (DANGEROUS_KEYS.has(key)) {
          fail(`${path}.${key}`, "dangerous object key is not permitted");
        }
        stringAt(key, `${path}.<key>`, { max: 256 });
        visit((item as ObjectValue)[key], `${path}.${key}`, depth + 1);
      }
    }
    ancestors.delete(item);
  }

  visit(value, "$", 0);
}

function httpsUrlAt(value: unknown, path: string): string {
  const text = stringAt(value, path, { max: 2_048 });
  let url: URL;
  try {
    url = new URL(text);
  } catch {
    fail(path, "expected an absolute HTTPS URL");
  }
  if (url.protocol !== "https:" || url.username || url.password) {
    fail(path, "expected an HTTPS URL without credentials");
  }
  return text;
}

function validateDetailLinks(details: ObjectValue, path: string): void {
  const visit = (value: unknown, key: string, itemPath: string): void => {
    if (typeof value === "string" && new Set(["url", "profile", "compatibilityProfile"]).has(key)) {
      if (!isSafeNavigableHref(value, PUBLICATION_BASE)) {
        fail(itemPath, "navigable URL is not HTTPS or a safe publication-relative path");
      }
      return;
    }
    if (Array.isArray(value)) {
      value.forEach((child, index) => visit(child, key, `${itemPath}[${index}]`));
    } else if (isObject(value)) {
      Object.entries(value).forEach(([childKey, child]) =>
        visit(child, childKey, `${itemPath}.${childKey}`),
      );
    }
  };
  Object.entries(details).forEach(([key, value]) => visit(value, key, `${path}.${key}`));
}

function parseRecord(value: unknown, index: number): CatalogueRecord {
  const path = `$.records[${index}]`;
  const record = objectAt(value, path);
  exactKeys(
    record,
    [
      "schema",
      "id",
      "type",
      "title",
      "description",
      "authority",
      "publication",
      "access",
      "rights",
      "freshness",
      "status",
      "sourceRefs",
      "limitations",
      "tags",
      "details",
    ],
    path,
  );

  literalAt(record.schema, "gis-ai-go-okf-concept.v1", `${path}.schema`);
  const id = stringAt(record.id, `${path}.id`, { max: 512 });
  const type = enumAt(record.type, RECORD_TYPES, `${path}.type`);
  const title = stringAt(record.title, `${path}.title`, {
    plain: true,
    max: MAX_DISPLAY_STRING_LENGTH,
  });
  const description = stringAt(record.description, `${path}.description`, {
    plain: true,
    max: MAX_DISPLAY_STRING_LENGTH,
  });

  const authority = objectAt(record.authority, `${path}.authority`);
  exactKeys(authority, ["class", "statement", "source"], `${path}.authority`);
  const authorityClass = enumAt(authority.class, AUTHORITY_CLASSES, `${path}.authority.class`);
  const authorityStatement = stringAt(authority.statement, `${path}.authority.statement`, {
    plain: true,
    max: MAX_DISPLAY_STRING_LENGTH,
  });
  const authoritySource = stringAt(authority.source, `${path}.authority.source`, {
    plain: true,
    max: 2_048,
  });
  if (/^[a-z][a-z0-9+.-]*:/iu.test(authoritySource) && !authoritySource.startsWith("https://")) {
    fail(`${path}.authority.source`, "absolute authority links must use HTTPS");
  }
  if (authoritySource.startsWith("https://") && !isSafeNavigableHref(authoritySource, PUBLICATION_BASE)) {
    fail(`${path}.authority.source`, "authority URL is unsafe");
  }

  const publication = objectAt(record.publication, `${path}.publication`);
  exactKeys(
    publication,
    ["classification", "containsPersonalData", "containsProtectedData"],
    `${path}.publication`,
  );
  literalAt(publication.classification, "public", `${path}.publication.classification`);
  literalAt(publication.containsPersonalData, false, `${path}.publication.containsPersonalData`);
  literalAt(
    publication.containsProtectedData,
    false,
    `${path}.publication.containsProtectedData`,
  );

  const access = objectAt(record.access, `${path}.access`);
  exactKeys(access, ["tier", "state", "authentication"], `${path}.access`);
  literalAt(access.tier, "open", `${path}.access.tier`);
  const accessState = enumAt(access.state, ACCESS_STATES, `${path}.access.state`);
  const authentication = stringAt(access.authentication, `${path}.access.authentication`, {
    plain: true,
    max: MAX_DISPLAY_STRING_LENGTH,
  });

  const rights = objectAt(record.rights, `${path}.rights`);
  exactKeys(
    rights,
    ["state", "recordLicence", "describedResourceLicence", "attribution"],
    `${path}.rights`,
  );
  const rightsState = enumAt(rights.state, RIGHTS_STATES, `${path}.rights.state`);
  const recordLicence = stringAt(rights.recordLicence, `${path}.rights.recordLicence`, {
    plain: true,
    max: MAX_DISPLAY_STRING_LENGTH,
  });
  const describedResourceLicence = stringAt(
    rights.describedResourceLicence,
    `${path}.rights.describedResourceLicence`,
    { plain: true, max: MAX_DISPLAY_STRING_LENGTH },
  );
  const attribution = stringAt(rights.attribution, `${path}.rights.attribution`, {
    plain: true,
    max: MAX_DISPLAY_STRING_LENGTH,
  });

  const freshness = objectAt(record.freshness, `${path}.freshness`);
  exactKeys(
    freshness,
    ["observedAt", "reviewedAt", "staleAfter", "status"],
    `${path}.freshness`,
  );
  const observedAt = dateTimeAt(freshness.observedAt, `${path}.freshness.observedAt`);
  const reviewedAt = dateTimeAt(freshness.reviewedAt, `${path}.freshness.reviewedAt`);
  const staleAfter = dateTimeAt(freshness.staleAfter, `${path}.freshness.staleAfter`);
  const freshnessStatus = enumAt(
    freshness.status,
    FRESHNESS_STATUSES,
    `${path}.freshness.status`,
  );

  const status = enumAt(record.status, RECORD_STATUSES, `${path}.status`);
  const sourceRefs = uniqueStringsAt(record.sourceRefs, `${path}.sourceRefs`, { min: 1 });
  const limitations = uniqueStringsAt(record.limitations, `${path}.limitations`, {
    plain: true,
    min: 1,
  });
  const tags = uniqueStringsAt(record.tags, `${path}.tags`);
  const details = objectAt(record.details, `${path}.details`);
  validateDetailLinks(details, `${path}.details`);
  for (const key of [
    "metadataSnapshotGeneratedAt",
    "publisherLastUpdated",
    "published",
    "questionResearchCutoff",
    "retrieved",
    "retrievedOn",
    "releaseTaggedAt",
    "releasedAt",
    "releaseDate",
  ] as const) {
    const detail = details[key];
    if (detail !== undefined && detail !== null) {
      dateLikeAt(detail, `${path}.details.${key}`);
    }
  }

  return {
    schema: "gis-ai-go-okf-concept.v1",
    id,
    type,
    title,
    description,
    authority: {
      class: authorityClass,
      statement: authorityStatement,
      source: authoritySource,
    },
    publication: {
      classification: "public",
      containsPersonalData: false,
      containsProtectedData: false,
    },
    access: { tier: "open", state: accessState, authentication },
    rights: {
      state: rightsState,
      recordLicence,
      describedResourceLicence,
      attribution,
    },
    freshness: {
      observedAt,
      reviewedAt,
      staleAfter,
      status: freshnessStatus,
    },
    status,
    sourceRefs,
    limitations,
    tags,
    details: details as Readonly<Record<string, JsonValue>>,
  };
}

/** Parse and validate JSON text before it reaches the Explorer model. */
export function parseCatalogueJson(text: string): CatalogueBundle {
  if (new TextEncoder().encode(text).byteLength > MAX_CATALOGUE_JSON_BYTES) {
    throw new Error(`Catalogue JSON exceeds ${MAX_CATALOGUE_JSON_BYTES} bytes`);
  }
  let value: unknown;
  try {
    value = JSON.parse(text) as unknown;
  } catch (error) {
    throw new Error("Catalogue is not valid JSON", { cause: error });
  }
  return parseCatalogue(value);
}

/** Validate an unknown value against the bounded GIS AI GO public bundle contract. */
export function parseCatalogue(value: unknown): CatalogueBundle {
  assertSafeJson(value);
  const bundle = objectAt(value, "$");
  exactKeys(
    bundle,
    [
      "schema",
      "id",
      "title",
      "description",
      "okfVersion",
      "profile",
      "profileStatus",
      "version",
      "revision",
      "status",
      "authority",
      "scope",
      "rights",
      "observedAt",
      "reviewedAt",
      "staleAfter",
      "recordCount",
      "records",
    ],
    "$",
  );

  literalAt(bundle.schema, "gis-ai-go-okf-bundle.v1", "$.schema");
  const id = httpsUrlAt(bundle.id, "$.id");
  const title = stringAt(bundle.title, "$.title", { plain: true, max: MAX_DISPLAY_STRING_LENGTH });
  const description = stringAt(bundle.description, "$.description", {
    plain: true,
    max: MAX_DISPLAY_STRING_LENGTH,
  });
  literalAt(bundle.okfVersion, "0.2", "$.okfVersion");
  const profile = httpsUrlAt(bundle.profile, "$.profile");
  literalAt(
    bundle.profileStatus,
    "candidate-pending-consumer-acceptance",
    "$.profileStatus",
  );
  const version = stringAt(bundle.version, "$.version", { max: 64 });
  if (!SEMVER.test(version)) {
    fail("$.version", "expected a semantic version");
  }
  const revision = stringAt(bundle.revision, "$.revision", { max: 40 });
  if (!SHA_40.test(revision)) {
    fail("$.revision", "expected a lowercase 40-character Git SHA");
  }
  literalAt(bundle.status, "candidate", "$.status");

  const authority = objectAt(bundle.authority, "$.authority");
  exactKeys(
    authority,
    ["bundleAuthority", "officialSourceAuthority", "legalAdvice", "notEndorsedBySource"],
    "$.authority",
  );
  const bundleAuthority = stringAt(authority.bundleAuthority, "$.authority.bundleAuthority", {
    plain: true,
    max: MAX_DISPLAY_STRING_LENGTH,
  });
  const officialSourceAuthority = stringAt(
    authority.officialSourceAuthority,
    "$.authority.officialSourceAuthority",
    { plain: true, max: MAX_DISPLAY_STRING_LENGTH },
  );
  literalAt(authority.legalAdvice, false, "$.authority.legalAdvice");
  literalAt(authority.notEndorsedBySource, true, "$.authority.notEndorsedBySource");

  const scope = objectAt(bundle.scope, "$.scope");
  exactKeys(scope, ["kind", "metadataOnly", "containsProtectedData", "excludes"], "$.scope");
  literalAt(scope.kind, "bounded-public-metadata-discovery", "$.scope.kind");
  literalAt(scope.metadataOnly, true, "$.scope.metadataOnly");
  literalAt(scope.containsProtectedData, false, "$.scope.containsProtectedData");
  const excludes = uniqueStringsAt(scope.excludes, "$.scope.excludes", { plain: true, min: 1 });

  const rights = objectAt(bundle.rights, "$.rights");
  exactKeys(rights, ["statement", "thirdPartyNotices"], "$.rights");
  const rightsStatement = stringAt(rights.statement, "$.rights.statement", {
    plain: true,
    max: MAX_DISPLAY_STRING_LENGTH,
  });
  literalAt(rights.thirdPartyNotices, "THIRD_PARTY.md", "$.rights.thirdPartyNotices");

  const observedAt = dateTimeAt(bundle.observedAt, "$.observedAt");
  const reviewedAt = dateTimeAt(bundle.reviewedAt, "$.reviewedAt");
  const staleAfter = dateTimeAt(bundle.staleAfter, "$.staleAfter");
  if (
    typeof bundle.recordCount !== "number" ||
    !Number.isInteger(bundle.recordCount) ||
    bundle.recordCount < 1
  ) {
    fail("$.recordCount", "expected a positive integer");
  }
  const recordCount = bundle.recordCount;
  if (!Array.isArray(bundle.records) || bundle.records.length > MAX_CATALOGUE_RECORDS) {
    fail("$.records", `expected no more than ${MAX_CATALOGUE_RECORDS} records`);
  }
  if (recordCount !== bundle.records.length) {
    fail("$.recordCount", "does not match the records array length");
  }

  const records = bundle.records.map(parseRecord);
  const byId = new Map(records.map((record) => [record.id, record]));
  if (byId.size !== records.length) {
    fail("$.records", "record IDs must be unique");
  }
  for (const record of records) {
    for (const sourceRef of record.sourceRefs) {
      if (!byId.has(sourceRef)) {
        fail(`$.records.${record.id}.sourceRefs`, `unresolved source reference ${sourceRef}`);
      }
    }
  }
  const defaultRecord = byId.get(DEFAULT_RECORD_ID);
  if (!defaultRecord) {
    fail("$.records", `missing canonical default record ${DEFAULT_RECORD_ID}`);
  }
  if (!defaultRecord.limitations.includes(DEFAULT_BOUNDARY_CAVEAT)) {
    fail(
      `$.records.${DEFAULT_RECORD_ID}.limitations`,
      "missing the required indicative-versus-legal-boundary caveat",
    );
  }

  return {
    schema: "gis-ai-go-okf-bundle.v1",
    id,
    title,
    description,
    okfVersion: "0.2",
    profile,
    profileStatus: "candidate-pending-consumer-acceptance",
    version,
    revision,
    status: "candidate",
    authority: {
      bundleAuthority,
      officialSourceAuthority,
      legalAdvice: false,
      notEndorsedBySource: true,
    },
    scope: {
      kind: "bounded-public-metadata-discovery",
      metadataOnly: true,
      containsProtectedData: false,
      excludes,
    },
    rights: {
      statement: rightsStatement,
      thirdPartyNotices: "THIRD_PARTY.md",
    },
    observedAt,
    reviewedAt,
    staleAfter,
    recordCount: records.length,
    records,
  };
}

function normaliseSearchText(value: string): string {
  return value
    .normalize("NFKC")
    .toLocaleLowerCase("en-GB")
    .replace(/\s+/gu, " ")
    .trim();
}

function approvedDetailText(value: JsonValue | undefined): string[] {
  if (value === undefined) {
    return [];
  }
  if (value === null) {
    return [];
  }
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
    return [String(value)];
  }
  if (Array.isArray(value)) {
    return value.flatMap(approvedDetailText);
  }
  return [];
}

// This is deliberately an allowlist. In particular, do not replace it with a
// recursive walk of `details` or include rights text: those fields may contain
// long, provider-specific material that is not part of the controlled search
// contract.
const SEARCHABLE_DETAIL_FIELDS = [
  "publisher",
  "organisation",
  "jurisdiction",
  "geographicScope",
  "formats",
  "cadence",
  "updateFrequency",
  "accessModel",
  "questionId",
  "query",
  "intent",
  "expectedTerms",
  "expectedPropositions",
  "datasetsServices",
  "mechanisms",
] as const;

function searchableText(record: CatalogueRecord): string {
  return normaliseSearchText(
    [
      record.id,
      record.type,
      record.title,
      record.description,
      record.authority.statement,
      ...record.limitations,
      ...record.tags,
      ...SEARCHABLE_DETAIL_FIELDS.flatMap((field) =>
        approvedDetailText(record.details[field]),
      ),
    ].join(" "),
  );
}

function compareText(left: string, right: string): number {
  return left < right ? -1 : left > right ? 1 : 0;
}

/** Apply bounded full-text search and the controlled Explorer facets. */
export function searchRecords(
  records: readonly CatalogueRecord[],
  state: ExplorerState,
): readonly CatalogueRecord[] {
  const tokens = normaliseSearchText(state.query).split(" ").filter(Boolean).slice(0, 10);
  const matches = records.filter((record) => {
    const haystack = searchableText(record);
    return (
      tokens.every((token) => haystack.includes(token)) &&
      (state.types.length === 0 || state.types.includes(record.type)) &&
      (state.authority.length === 0 || state.authority.includes(record.authority.class)) &&
      (state.access.length === 0 || state.access.includes(record.access.state)) &&
      (state.rights.length === 0 || state.rights.includes(record.rights.state)) &&
      (state.freshness.length === 0 || state.freshness.includes(record.freshness.status)) &&
      (state.tags.length === 0 || state.tags.some((tag) => record.tags.includes(tag)))
    );
  });

  return [...matches].sort((left, right) => {
    if (tokens.length > 0) {
      const leftTitle = normaliseSearchText(left.title);
      const rightTitle = normaliseSearchText(right.title);
      const leftScore = tokens.reduce(
        (score, token) => score + (leftTitle === token ? 8 : leftTitle.startsWith(token) ? 4 : leftTitle.includes(token) ? 2 : 0),
        0,
      );
      const rightScore = tokens.reduce(
        (score, token) => score + (rightTitle === token ? 8 : rightTitle.startsWith(token) ? 4 : rightTitle.includes(token) ? 2 : 0),
        0,
      );
      if (leftScore !== rightScore) {
        return rightScore - leftScore;
      }
    }
    return compareText(left.title, right.title) || compareText(left.id, right.id);
  });
}

function countedOptions<T extends string>(values: readonly T[]): readonly FacetOption<T>[] {
  const counts = new Map<T, number>();
  values.forEach((value) => counts.set(value, (counts.get(value) ?? 0) + 1));
  return [...counts.entries()]
    .sort(([left], [right]) => compareText(left, right))
    .map(([value, count]) => ({ value, count }));
}

function stateWithoutFacet(
  state: ExplorerState,
  facet: "types" | "authority" | "access" | "rights" | "freshness" | "tags",
): ExplorerState {
  return { ...state, [facet]: [] };
}

function countedKnownOptions<T extends string>(
  known: readonly T[],
  matching: readonly T[],
): readonly FacetOption<T>[] {
  const counts = new Map<T, number>();
  matching.forEach((value) => counts.set(value, (counts.get(value) ?? 0) + 1));
  return uniqueFacetValues(known)
    .sort(compareText)
    .map((value) => ({ value, count: counts.get(value) ?? 0 }));
}

function uniqueFacetValues<T extends string>(values: readonly T[]): T[] {
  return [...new Set(values)];
}

export function deriveFacetOptions(
  records: readonly CatalogueRecord[],
  state?: ExplorerState,
): FacetOptions {
  if (state === undefined) {
    return {
      types: countedOptions(records.map((record) => record.type)),
      authority: countedOptions(records.map((record) => record.authority.class)),
      access: countedOptions(records.map((record) => record.access.state)),
      rights: countedOptions(records.map((record) => record.rights.state)),
      freshness: countedOptions(records.map((record) => record.freshness.status)),
      tags: countedOptions(records.flatMap((record) => record.tags)),
    };
  }
  const matching = (facet: Parameters<typeof stateWithoutFacet>[1]): readonly CatalogueRecord[] =>
    searchRecords(records, stateWithoutFacet(state, facet));
  return {
    types: countedKnownOptions(
      records.map((record) => record.type),
      matching("types").map((record) => record.type),
    ),
    authority: countedKnownOptions(
      records.map((record) => record.authority.class),
      matching("authority").map((record) => record.authority.class),
    ),
    access: countedKnownOptions(
      records.map((record) => record.access.state),
      matching("access").map((record) => record.access.state),
    ),
    rights: countedKnownOptions(
      records.map((record) => record.rights.state),
      matching("rights").map((record) => record.rights.state),
    ),
    freshness: countedKnownOptions(
      records.map((record) => record.freshness.status),
      matching("freshness").map((record) => record.freshness.status),
    ),
    tags: countedKnownOptions(
      records.flatMap((record) => record.tags),
      matching("tags").flatMap((record) => record.tags),
    ),
  };
}

const FACET_LABELS: Readonly<Record<string, string>> = {
  bundle: "Bundle",
  dataset: "Dataset",
  provider: "Provider",
  source: "Source",
  workflow: "Workflow",
  derived: "Derived",
  "project-authoritative": "Project authoritative",
  "source-authoritative": "Source authoritative",
  "planned-non-executing": "Planned, non-executing",
  public: "Public",
  "public-metadata": "Public metadata",
  "metadata-citation": "Metadata citation",
  "open-with-conditions": "Open with conditions",
  "project-mit": "Project MIT",
  current: "Current",
  "review-required": "Review required",
};

export function facetLabel(value: string): string {
  return FACET_LABELS[value] ?? value;
}

/**
 * Derive source-reference nodes, edges and a complete adjacency alternative.
 * When IDs are supplied they represent filtered records; their immediate referenced
 * evidence nodes are added so the graph retains its one-hop evidence context.
 */
export function deriveGraph(
  records: readonly CatalogueRecord[],
  includeRecordIds?: readonly string[],
): GraphModel {
  const byId = new Map(records.map((record) => [record.id, record]));
  if (byId.size !== records.length) {
    throw new Error("Cannot derive a graph from duplicate record IDs");
  }
  const explicit = new Set(includeRecordIds ?? records.map((record) => record.id));
  for (const id of explicit) {
    if (!byId.has(id)) {
      throw new Error(`Cannot derive a graph for unknown record ${id}`);
    }
  }

  const included = new Set(explicit);
  for (const id of explicit) {
    const record = byId.get(id);
    if (!record) {
      throw new Error(`Graph record disappeared: ${id}`);
    }
    for (const sourceId of record.sourceRefs) {
      if (!byId.has(sourceId)) {
        throw new Error(`Unresolved graph source ${sourceId} from ${record.id}`);
      }
      if (!included.has(sourceId)) {
        included.add(sourceId);
      }
    }
  }

  const includedRecords = records
    .filter((record) => included.has(record.id))
    .sort((left, right) => compareText(left.type, right.type) || compareText(left.id, right.id));
  return {
    nodes: includedRecords.map((record) => ({
      id: record.id,
      type: record.type,
      title: record.title,
      status: record.status,
      explicitlyIncluded: explicit.has(record.id),
    })),
    edges: includedRecords.flatMap((record) =>
      explicit.has(record.id) ? record.sourceRefs.filter((sourceId) => sourceId !== record.id).map((sourceId) => ({
        from: record.id,
        to: sourceId,
        relation: "source" as const,
        selfReference: false,
      })) : [],
    ),
    adjacency: includedRecords.map((record) => ({
      recordId: record.id,
      recordTitle: record.title,
      sourceIds: explicit.has(record.id)
        ? record.sourceRefs.filter((sourceId) => sourceId !== record.id).sort(compareText)
        : [],
    })),
  };
}

function optionalDetailDate(record: CatalogueRecord, keys: readonly string[]): string | null {
  for (const key of keys) {
    const value = record.details[key];
    if (typeof value === "string") {
      return dateLikeAt(value, `record ${record.id}.details.${key}`);
    }
  }
  return null;
}

export function deriveTimeline(records: readonly CatalogueRecord[]): TimelineModel {
  const events: TimelineEvent[] = [];
  const missing = new Map<TimelineEventKind, number>(
    TIMELINE_EVENT_KINDS.map((kind) => [kind, 0]),
  );
  const add = (record: CatalogueRecord, kind: TimelineEventKind, date: string | null): void => {
    if (date === null) {
      missing.set(kind, (missing.get(kind) ?? 0) + 1);
      return;
    }
    events.push({
      id: `${record.id}|${kind}|${date}`,
      recordId: record.id,
      recordTitle: record.title,
      kind,
      date,
    });
  };

  for (const record of records) {
    add(record, "observation", record.freshness.observedAt);
    add(record, "modification", optionalDetailDate(record, ["publisherLastUpdated"]));
    add(record, "publication", optionalDetailDate(record, ["published"]));
    add(
      record,
      "release",
      optionalDetailDate(record, ["releaseTaggedAt", "releasedAt", "releaseDate"]),
    );
  }

  const kindOrder = new Map(TIMELINE_EVENT_KINDS.map((kind, index) => [kind, index]));
  events.sort(
    (left, right) =>
      Date.parse(right.date) - Date.parse(left.date) ||
      (kindOrder.get(left.kind) ?? 0) - (kindOrder.get(right.kind) ?? 0) ||
      compareText(left.recordId, right.recordId),
  );
  return {
    events,
    missing: TIMELINE_EVENT_KINDS.map((kind) => ({
      kind,
      recordCount: missing.get(kind) ?? 0,
    })).filter((item) => item.recordCount > 0),
  };
}

// These aliases make the controlled facet types discoverable to UI consumers.
export type CatalogueRecordType = RecordType;
export type CatalogueAuthorityClass = AuthorityClass;
export type CatalogueAccessState = AccessState;
export type CatalogueRightsState = RightsState;
export type CatalogueFreshnessStatus = FreshnessStatus;
export type CatalogueRecordStatus = RecordStatus;
