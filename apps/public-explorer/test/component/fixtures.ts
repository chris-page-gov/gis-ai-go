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

export const workedQuestionRecord: CatalogueRecord = {
  ...focusedRecord,
  id: "LR-Q003",
  type: "workflow",
  title: "LR-Q003 — Online copy or official copy?",
  description: "A reviewed, non-executing retrieval question.",
  access: {
    tier: "open",
    state: "planned-non-executing",
    authentication: "Not applicable: this is a non-executing description.",
  },
  rights: {
    state: "project-mit",
    recordLicence: "MIT",
    describedResourceLicence: "Not applicable; this is a non-executing description.",
    attribution: "Copyright © 2026 Chris Page.",
  },
  status: "candidate-non-executing",
  sourceRefs: ["source:dataset", "source:guidance"],
  limitations: [
    "An online copy is not proof of ownership.",
    "Official copies and ordinary online downloads are distinct products.",
  ],
  tags: ["hmlr", "official-copy", "worked-question"],
  details: {
    questionId: "LR-Q003",
    query: "online copy or official copy proof of ownership",
    intent: "Distinguish informational downloads from official copies.",
    expectedPropositions: [
      "An online copy is not proof of ownership.",
      "Official copies have a distinct order route and evidential role.",
    ],
    nearMissRule:
      "Merely linking to a paid download without explaining its evidential status is insufficient.",
  },
};

export const onsProviderRecord: CatalogueRecord = {
  ...focusedRecord,
  id: "PV-ONS-DATA",
  type: "provider",
  title: "ONS Data API",
  description: "Version-bound discovery of public ONS data capabilities.",
  access: {
    tier: "open",
    state: "public-metadata",
    authentication: "No provider connection is made by this candidate bundle.",
  },
  rights: {
    state: "metadata-citation",
    recordLicence: "MIT",
    describedResourceLicence: "Open Government Licence where stated.",
    attribution: "Office for National Statistics.",
  },
  status: "candidate-metadata",
  sourceRefs: ["source:dataset"],
  limitations: ["No live provider call, data distribution or service response is included."],
  tags: ["ons", "provider"],
  details: {
    geographicScope: "UK statistics; dataset-specific",
    datasetsServices: ["datasets", "versions", "editions", "dimensions", "observations"],
    mechanisms: ["REST API", "bulk downloads"],
    updateFrequency: "Dataset-specific",
    formats: ["JSON", "CSV"],
    recommendedIntegration: "Version-bound observation retrieval; this record does not execute it.",
  },
};

export const landisProviderRecord: CatalogueRecord = {
  ...onsProviderRecord,
  id: "PV-LANDIS",
  title: "LandIS",
  description: "Cranfield University soil information service metadata.",
  rights: {
    ...onsProviderRecord.rights,
    describedResourceLicence:
      "Read and enforce each record licence; do not infer one blanket licence from open access.",
    attribution: "Cranfield University and LandIS; apply source-specific attribution.",
  },
  limitations: [
    "No live provider call, data distribution or service response is included.",
    "Access and rights remain mixed and product-specific.",
  ],
  tags: ["landis", "provider", "soil"],
  details: {
    geographicScope: "England and Wales; product-specific",
    datasetsServices: ["NATMAP", "Soilscapes", "National Soil Inventory"],
    mechanisms: ["public portal", "downloads", "OGC API – Records catalogue"],
    accessTiers: ["open", "commercial or restricted where record terms require"],
    recommendedIntegration:
      "Harvest records as metadata; cache only licence-confirmed products; do not execute here.",
  },
};

export const navigation = {
  hrefForRecord: (recordId: string | null): string =>
    recordId === null ? "?view=cards" : `?view=cards#record=${encodeURIComponent(recordId)}`,
  selectRecord: (): void => undefined,
};
