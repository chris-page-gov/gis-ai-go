import { DEFAULT_RECORD_ID } from "./catalogue.js";
import {
  ACCESS_STATES,
  AUTHORITY_CLASSES,
  EXPLORER_VIEWS,
  FRESHNESS_STATUSES,
  RECORD_TYPES,
  RIGHTS_STATES,
  type CatalogueBundle,
  type ExplorerState,
} from "./types.js";

export const MAX_QUERY_LENGTH = 200;
export const MAX_FACET_VALUES = 20;
const MAX_TAG_LENGTH = 128;
const MAX_RECORD_ID_LENGTH = 512;
const UNSAFE_CONTROL = /[\u0000-\u001f\u007f\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]/u;

function compareText(left: string, right: string): number {
  return left < right ? -1 : left > right ? 1 : 0;
}

function normaliseQuery(value: string): string {
  if (UNSAFE_CONTROL.test(value)) {
    return "";
  }
  const bounded = [...value.normalize("NFKC").replace(/\s+/gu, " ").trim()]
    .slice(0, MAX_QUERY_LENGTH)
    .join("")
    .trim();
  return bounded.split(" ").slice(0, 10).join(" ");
}

function uniqueSorted<T extends string>(values: readonly T[]): readonly T[] {
  return [...new Set(values)].sort(compareText);
}

function controlledValues<const T extends readonly string[]>(
  values: readonly string[],
  allowed: T,
): readonly T[number][] {
  if (values.length > MAX_FACET_VALUES) {
    return [];
  }
  const allowedSet = new Set<string>(allowed);
  return uniqueSorted(values.filter((value): value is T[number] => allowedSet.has(value)));
}

function knownTags(bundle: CatalogueBundle): ReadonlySet<string> {
  return new Set(bundle.records.flatMap((record) => record.tags));
}

export function createDefaultExplorerState(bundle: CatalogueBundle): ExplorerState {
  if (!bundle.records.some((record) => record.id === DEFAULT_RECORD_ID)) {
    throw new Error(`Catalogue does not contain the default record ${DEFAULT_RECORD_ID}`);
  }
  return {
    view: "cards",
    query: "inspire",
    types: ["dataset"],
    authority: [],
    access: [],
    rights: [],
    freshness: [],
    tags: [],
    selectedRecordId: DEFAULT_RECORD_ID,
  };
}

/** Constrain a caller-created state to values present in the validated bundle. */
export function canonicaliseState(
  state: ExplorerState,
  bundle: CatalogueBundle,
): ExplorerState {
  const tags = knownTags(bundle);
  return {
    view: EXPLORER_VIEWS.includes(state.view) ? state.view : "cards",
    query: normaliseQuery(state.query),
    types: controlledValues(state.types, RECORD_TYPES),
    authority: controlledValues(state.authority, AUTHORITY_CLASSES),
    access: controlledValues(state.access, ACCESS_STATES),
    rights: controlledValues(state.rights, RIGHTS_STATES),
    freshness: controlledValues(state.freshness, FRESHNESS_STATUSES),
    tags:
      state.tags.length > MAX_FACET_VALUES
        ? []
        : uniqueSorted(
            state.tags.filter(
              (tag) => tag.length <= MAX_TAG_LENGTH && !UNSAFE_CONTROL.test(tag) && tags.has(tag),
            ),
          ),
    selectedRecordId:
      state.selectedRecordId !== null &&
      state.selectedRecordId.length <= MAX_RECORD_ID_LENGTH &&
      !UNSAFE_CONTROL.test(state.selectedRecordId)
        ? state.selectedRecordId
        : null,
  };
}

function singleParameter(search: URLSearchParams, key: string): string | null {
  const values = search.getAll(key);
  return values.length === 1 ? (values[0] ?? null) : null;
}

function parseControlled<const T extends readonly string[]>(
  search: URLSearchParams,
  key: string,
  allowed: T,
): readonly T[number][] {
  return controlledValues(search.getAll(key), allowed);
}

function selectedRecordFromHash(url: URL): string | null {
  if (url.hash.length === 0 || url.hash === "#") {
    return null;
  }
  const hash = new URLSearchParams(url.hash.slice(1));
  if ([...hash.keys()].some((key) => key !== "record")) {
    return null;
  }
  const selected = singleParameter(hash, "record");
  if (
    selected === null ||
    selected.length === 0 ||
    selected.length > MAX_RECORD_ID_LENGTH ||
    UNSAFE_CONTROL.test(selected)
  ) {
    return null;
  }
  return selected;
}

/** Parse only the documented query and hash fields; all other state is discarded. */
export function parseExplorerUrl(
  input: string | URL,
  bundle: CatalogueBundle,
): ExplorerState {
  const url = input instanceof URL ? new URL(input.href) : new URL(input, "https://invalid.local/");
  const query = singleParameter(url.searchParams, "q");
  const view = singleParameter(url.searchParams, "view");
  const tagSet = knownTags(bundle);
  const rawTags = url.searchParams.getAll("tag");
  const parsed: ExplorerState = {
    view: view !== null && EXPLORER_VIEWS.includes(view as (typeof EXPLORER_VIEWS)[number])
      ? (view as (typeof EXPLORER_VIEWS)[number])
      : "cards",
    query: query !== null && query.length <= MAX_QUERY_LENGTH ? normaliseQuery(query) : "",
    types: parseControlled(url.searchParams, "type", RECORD_TYPES),
    authority: parseControlled(url.searchParams, "authority", AUTHORITY_CLASSES),
    access: parseControlled(url.searchParams, "access", ACCESS_STATES),
    rights: parseControlled(url.searchParams, "rights", RIGHTS_STATES),
    freshness: parseControlled(url.searchParams, "freshness", FRESHNESS_STATUSES),
    tags:
      rawTags.length > MAX_FACET_VALUES
        ? []
        : uniqueSorted(
            rawTags.filter(
              (tag) => tag.length <= MAX_TAG_LENGTH && !UNSAFE_CONTROL.test(tag) && tagSet.has(tag),
            ),
          ),
    selectedRecordId: selectedRecordFromHash(url),
  };
  return canonicaliseState(parsed, bundle);
}

/** Serialise a canonical, shareable Explorer URL with stable parameter ordering. */
export function serialiseExplorerUrl(
  state: ExplorerState,
  base: string | URL,
  bundle: CatalogueBundle,
): URL {
  const canonical = canonicaliseState(state, bundle);
  const url = base instanceof URL ? new URL(base.href) : new URL(base);
  const search = new URLSearchParams();
  search.append("view", canonical.view);
  if (canonical.query) {
    search.append("q", canonical.query);
  }
  const add = (key: string, values: readonly string[]): void => {
    values.forEach((value) => search.append(key, value));
  };
  add("type", canonical.types);
  add("authority", canonical.authority);
  add("access", canonical.access);
  add("rights", canonical.rights);
  add("freshness", canonical.freshness);
  add("tag", canonical.tags);
  url.search = search.toString();

  if (canonical.selectedRecordId === null) {
    url.hash = "";
  } else {
    const hash = new URLSearchParams({ record: canonical.selectedRecordId });
    url.hash = hash.toString();
  }
  return url;
}

export function explorerStatesEqual(left: ExplorerState, right: ExplorerState): boolean {
  return (
    left.view === right.view &&
    left.query === right.query &&
    left.selectedRecordId === right.selectedRecordId &&
    left.types.join("\u0000") === right.types.join("\u0000") &&
    left.authority.join("\u0000") === right.authority.join("\u0000") &&
    left.access.join("\u0000") === right.access.join("\u0000") &&
    left.rights.join("\u0000") === right.rights.join("\u0000") &&
    left.freshness.join("\u0000") === right.freshness.join("\u0000") &&
    left.tags.join("\u0000") === right.tags.join("\u0000")
  );
}
