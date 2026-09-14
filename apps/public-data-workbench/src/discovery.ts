import state from "./generated/discovery.json";

export const records = Object.values(state.entries).map((entry) => entry.view);
export type DiscoveryRecord = typeof records[number];
export const discoveryProvenance = { version: state.version, logical_sha256: state.logical_sha256 };

/** Deliberately narrower than the Python experiment: explicit ASCII English input. */
export function findData(input: unknown) {
  if (input === null || typeof input !== "object" || Array.isArray(input) ||
      Object.keys(input).length !== 1 || !Object.hasOwn(input, "query")) {
    throw new TypeError("Supply only a query.");
  }
  const query = (input as { query?: unknown }).query;
  if (typeof query !== "string" || !query.trim() || query.length > 256 || /[^\x20-\x7e]/.test(query)) {
    throw new TypeError("Use 1 to 10 English keywords, at most 256 characters.");
  }
  const terms = query.toLowerCase().match(/[a-z0-9]+/g) ?? [];
  if (!terms.length || terms.length > 10) throw new TypeError("Use 1 to 10 English keywords, at most 256 characters.");
  const postings: Record<string, readonly string[]> = state.postings;
  const scores = new Map<string, number>();
  for (const term of new Set(terms)) for (const id of Object.hasOwn(postings, term) ? postings[term]! : []) scores.set(id, (scores.get(id) ?? 0) + 1);
  const matches = records.filter((record) => scores.has(record.id))
    .sort((a, b) => scores.get(b.id)! - scores.get(a.id)! || (a.id < b.id ? -1 : 1))
    .slice(0, 5).map((record) => ({ ...record, score: scores.get(record.id)! }));
  return { schema: "web216.browser-discovery.v1", query, records: matches,
    provenance: discoveryProvenance, metadata_only: true, provider_egress: false,
    limitation: "Seven frozen metadata records; English keyword ranking, not general intent understanding or execution permission." };
}
