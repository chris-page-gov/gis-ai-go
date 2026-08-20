/**
 * Explorer compatibility adapter for the shared governed catalogue contract.
 *
 * Keep catalogue parsing and search semantics in one package so the static
 * Explorer, direct API and MCP gateway cannot drift into different answers.
 */
export {
  DEFAULT_BOUNDARY_CAVEAT,
  DEFAULT_RECORD_ID,
  MAX_CATALOGUE_JSON_BYTES,
  MAX_CATALOGUE_QUERY_LENGTH,
  MAX_CATALOGUE_QUERY_TERMS,
  MAX_CATALOGUE_RECORDS,
  analyseCatalogueQuery,
  deriveFacetOptions,
  deriveGraph,
  deriveTimeline,
  facetLabel,
  parseCatalogue,
  parseCatalogueJson,
  searchRecords,
} from "@gis-ai-go/contracts";

export type {
  CatalogueAccessState,
  CatalogueAuthorityClass,
  CatalogueFreshnessStatus,
  CatalogueQueryAnalysis,
  CatalogueRecordStatus,
  CatalogueRecordType,
  CatalogueRightsState,
} from "@gis-ai-go/contracts";
