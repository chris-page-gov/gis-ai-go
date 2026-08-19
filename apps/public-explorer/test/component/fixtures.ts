import type { CatalogueRecord } from "../../src/types";

export const focusedRecord: CatalogueRecord = {
  schema: "gis-ai-go-okf-concept.v1",
  id: "hmlr:dataset:inspire-index-polygons",
  type: "dataset",
  title: "Index polygons spatial data (INSPIRE)",
  description:
    "Monthly GML files showing the indicative position and extent of registered freehold property in England and Wales by local authority area.",
  authority: {
    class: "source-authoritative",
    statement:
      "Source metadata is publisher-authored; GIS AI GO provides only a deterministic, metadata-only projection.",
    source: "https://use-land-property-data.service.gov.uk/datasets/inspire",
  },
  publication: {
    classification: "public",
    containsPersonalData: false,
    containsProtectedData: false,
  },
  access: {
    tier: "open",
    state: "public",
    authentication: "none",
  },
  rights: {
    state: "open-with-conditions",
    recordLicence: "CC BY 4.0 for upstream metadata; GIS AI GO additions are MIT.",
    describedResourceLicence:
      "Open Government Licence v3.0 plus required HM Land Registry and Ordnance Survey attribution conditions",
    attribution:
      "HM Land Registry and Ordnance Survey attribution is required by the source terms.",
  },
  freshness: {
    observedAt: "2026-07-29T07:53:38Z",
    reviewedAt: "2026-08-19T00:00:00Z",
    staleAfter: "2026-11-19T00:00:00Z",
    status: "current",
  },
  status: "candidate-metadata",
  sourceRefs: ["source:dataset", "source:download", "source:guidance"],
  limitations: [
    "Polygons are indicative and do not establish the exact legal extent of a title.",
    "The source GML uses British National Grid (EPSG:27700); reprojection may introduce positional error.",
    "This is a freehold subset, not all registered titles or all land.",
    "A title may have several polygons; local-authority boundary polygons may be duplicated across files.",
  ],
  tags: ["epsg-27700", "geospatial-data", "hmlr", "inspire"],
  details: {
    publisher: "HM Land Registry",
    jurisdiction: "England and Wales",
    cadence: "monthly, on the first Sunday for the preceding month",
    formats: ["GML"],
    publisherLastUpdated: "2026-07-05",
  },
};

export function sourceRecord(id: string, title: string): CatalogueRecord {
  return {
    ...focusedRecord,
    id,
    type: "source",
    title,
    description: "Public evidence page cited by the selected upstream metadata record.",
    authority: {
      class: "source-authoritative",
      statement: "Official publisher evidence remains authoritative.",
      source: `https://example.test/${encodeURIComponent(id)}`,
    },
    access: {
      tier: "open",
      state: "public-metadata",
      authentication: "None.",
    },
    rights: {
      state: "metadata-citation",
      recordLicence: "MIT",
      describedResourceLicence: "Source-specific.",
      attribution: "Consult the publisher.",
    },
    status: "external-source",
    sourceRefs: [id],
    limitations: ["A public evidence page does not make linked data open."],
    tags: ["source"],
    details: { url: `https://example.test/${encodeURIComponent(id)}` },
  };
}

export const sources = [
  sourceRecord("source:dataset", "Official dataset page"),
  sourceRecord("source:download", "Official download page"),
  sourceRecord("source:guidance", "Official technical guidance"),
];

export const navigation = {
  hrefForRecord: (recordId: string | null): string =>
    recordId === null ? "?view=cards" : `?view=cards#record=${encodeURIComponent(recordId)}`,
  selectRecord: (): void => undefined,
};
