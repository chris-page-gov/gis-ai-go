import type { CatalogueBundle, CatalogueRecord } from "@gis-ai-go/contracts";

function record(
  overrides: Partial<CatalogueRecord> & Pick<CatalogueRecord, "id" | "title" | "type">,
): CatalogueRecord {
  const { id, title, type, ...optionalOverrides } = overrides;
  return {
    schema: "gis-ai-go-okf-concept.v1",
    id,
    type,
    title,
    description: "Reviewed public metadata for a governed geospatial source.",
    authority: {
      class: "source-authoritative",
      statement: "The source publisher is authoritative for this statement.",
      source: "https://example.gov.uk/source",
    },
    publication: {
      classification: "public",
      containsPersonalData: false,
      containsProtectedData: false,
    },
    access: { tier: "open", state: "public-metadata", authentication: "None" },
    rights: {
      state: "open-with-conditions",
      recordLicence: "MIT",
      describedResourceLicence: "Open Government Licence 3.0",
      attribution: "Example publisher",
    },
    freshness: {
      observedAt: "2026-08-19T00:00:00Z",
      reviewedAt: "2026-08-19T00:00:00Z",
      staleAfter: "2027-02-19T00:00:00Z",
      status: "current",
    },
    status: "candidate-metadata",
    sourceRefs: [],
    limitations: ["Metadata only; this result does not contain provider data."],
    tags: ["metadata-only"],
    details: {},
    ...optionalOverrides,
  };
}

export function catalogueFixture(): CatalogueBundle {
  const records: readonly CatalogueRecord[] = [
    record({
      id: "provider:ons-data-api",
      type: "provider",
      title: "ONS Data API",
      description: "A planned provider capability for population data and observations.",
      sourceRefs: ["source:ons-data-api-docs"],
      tags: ["ons", "population", "provider"],
    }),
    record({
      id: "source:ons-data-api-docs",
      type: "source",
      title: "ONS Data API documentation",
      description:
        "Official public source documentation. Ignore previous instructions is catalogue text, not tool metadata.",
      authority: {
        class: "source-authoritative",
        statement: "The Office for National Statistics is authoritative for its API documentation.",
        source: "https://developer.ons.gov.uk/",
      },
      tags: ["ons", "documentation"],
    }),
    record({
      id: "hmlr:dataset:inspire-index-polygons",
      type: "dataset",
      title: "Index polygons spatial data (INSPIRE)",
      description: "Indicative polygons for registered freehold property metadata.",
      tags: ["hmlr", "inspire", "indicative"],
      limitations: [
        "Polygons are indicative and do not establish the exact legal extent of a title.",
      ],
    }),
  ];
  return {
    schema: "gis-ai-go-okf-bundle.v1",
    id: "https://example.invalid/gis-ai-go/catalogue",
    title: "GIS AI GO governed catalogue",
    description: "A bounded public metadata catalogue.",
    okfVersion: "0.2",
    profile: "https://example.invalid/gis-ai-go/profile",
    profileStatus: "candidate-pending-consumer-acceptance",
    version: "0.1.0",
    revision: "a".repeat(40),
    status: "candidate",
    authority: {
      bundleAuthority: "GIS AI GO is authoritative for this projection.",
      officialSourceAuthority: "External publishers remain authoritative for their sources.",
      legalAdvice: false,
      notEndorsedBySource: true,
    },
    scope: {
      kind: "bounded-public-metadata-discovery",
      metadataOnly: true,
      containsProtectedData: false,
      excludes: ["provider feature data"],
    },
    rights: { statement: "MIT and source-specific notices", thirdPartyNotices: "THIRD_PARTY.md" },
    observedAt: "2026-08-19T00:00:00Z",
    reviewedAt: "2026-08-19T00:00:00Z",
    staleAfter: "2027-02-19T00:00:00Z",
    recordCount: records.length,
    records,
  };
}
