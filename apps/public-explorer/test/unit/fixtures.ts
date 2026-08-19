import { DEFAULT_BOUNDARY_CAVEAT, DEFAULT_RECORD_ID } from "../../src/catalogue.js";

const SOURCE_ID = "source:hmlr-inspire";

export function validCatalogueFixture() {
  const common = {
    schema: "gis-ai-go-okf-concept.v1",
    publication: {
      classification: "public",
      containsPersonalData: false,
      containsProtectedData: false,
    },
    access: {
      tier: "open",
      state: "public-metadata",
      authentication: "None.",
    },
    freshness: {
      observedAt: "2026-07-29T07:53:38Z",
      reviewedAt: "2026-08-19T00:00:00Z",
      staleAfter: "2026-11-19T00:00:00Z",
      status: "current",
    },
  };

  return {
    schema: "gis-ai-go-okf-bundle.v1",
    id: "https://chris-page-gov.github.io/gis-ai-go/id/bundle/public-discovery",
    title: "GIS AI GO public discovery bundle",
    description: "A bounded public metadata catalogue.",
    okfVersion: "0.2",
    profile: "https://chris-page-gov.github.io/gis-ai-go/profile/public-discovery/v1/",
    profileStatus: "candidate-pending-consumer-acceptance",
    version: "0.0.0",
    revision: "4ff9cc79946b1977a2022428336687a3dedb04b3",
    status: "candidate",
    authority: {
      bundleAuthority: "Metadata normalisation and publication only.",
      officialSourceAuthority: "External live publisher sources.",
      legalAdvice: false,
      notEndorsedBySource: true,
    },
    scope: {
      kind: "bounded-public-metadata-discovery",
      metadataOnly: true,
      containsProtectedData: false,
      excludes: ["Property records and real geometry."],
    },
    rights: {
      statement: "Project material is MIT; third-party records retain their terms.",
      thirdPartyNotices: "THIRD_PARTY.md",
    },
    observedAt: "2026-07-29T07:53:38Z",
    reviewedAt: "2026-08-19T00:00:00Z",
    staleAfter: "2026-11-19T00:00:00Z",
    recordCount: 2,
    records: [
      {
        ...common,
        id: DEFAULT_RECORD_ID,
        type: "dataset",
        title: "Index polygons spatial data (INSPIRE)",
        description:
          "Indicative freehold extent metadata for England and Wales, not a title plan.",
        authority: {
          class: "source-authoritative",
          statement: "HM Land Registry is authoritative for the source metadata.",
          source: "https://www.gov.uk/guidance/inspire-index-polygons-spatial-data",
        },
        access: { ...common.access, state: "public" },
        rights: {
          state: "open-with-conditions",
          recordLicence: "CC BY 4.0 for upstream metadata.",
          describedResourceLicence: "Use is subject to the named source terms.",
          attribution: "HM Land Registry and Ordnance Survey.",
        },
        status: "candidate-metadata",
        sourceRefs: [SOURCE_ID],
        limitations: [
          DEFAULT_BOUNDARY_CAVEAT,
          "The catalogue contains no provider geometry.",
        ],
        tags: ["hmlr", "inspire", "metadata-only"],
        details: {
          publisher: "HM Land Registry",
          jurisdiction: "England and Wales",
          formats: ["GML"],
          cadence: "Monthly",
          publisherLastUpdated: "2026-07-05",
          url: "https://www.gov.uk/guidance/inspire-index-polygons-spatial-data",
        },
      },
      {
        ...common,
        id: SOURCE_ID,
        type: "source",
        title: "Official HMLR INSPIRE guidance",
        description: "The official public evidence page.",
        authority: {
          class: "source-authoritative",
          statement: "The named publisher is authoritative for this evidence page.",
          source: "https://www.gov.uk/guidance/inspire-index-polygons-spatial-data",
        },
        rights: {
          state: "metadata-citation",
          recordLicence: "MIT for the catalogue record.",
          describedResourceLicence: "Source-specific.",
          attribution: "HM Land Registry.",
        },
        status: "external-source",
        sourceRefs: [SOURCE_ID],
        limitations: ["A cited page does not relicense linked content."],
        tags: ["hmlr", "official-source"],
        details: {
          publisher: "HM Land Registry",
          published: "2026-06-01",
          url: "https://www.gov.uk/guidance/inspire-index-polygons-spatial-data",
        },
      },
    ],
  };
}
