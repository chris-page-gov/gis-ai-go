---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/projections-older-people-sex-ratios",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Local authority ageing statistics, projected sex ratios for older people",
  "description": "Projected indicators included are derived from the published 2018-based subnational population projections for England, Wales, Scotland and Northern Ireland up to the year 2043. The indicators are the projected sex ratio for those aged 65 years and over and the projected sex ratio for those aged 85 years and over. A sex ratio shows the number of males in the population for every 100 females. This dataset has been produced by the Ageing Analysis Team for inclusion in the subnational ageing tool, which was published on July 20, 2020 (see link in Related datasets). The tool is interactive, and users can compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. Note on data sources: England, Wales, Scotland and Northern Ireland independently publish subnational population projections and the data available here are a compilation of these datasets. The ONS publish national level data for the UK, England, Wales and England & Wales, which has been included. National level data for Scotland and Northern Ireland have been taken from their subnational population projections datasets.",
  "nativeIdentifier": "projections-older-people-sex-ratios",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/projections-older-people-sex-ratios/editions/time-series/versions/1",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/projections-older-people-sex-ratios/editions/time-series/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:30:51.051875Z",
      "responseSha256": "5d6fe24cd1d25f4cac738213d7f7ff05fbf512a2a8788866258d0b5084a1155a",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/20",
      "normalisedRecordSha256": "1e0d6248adcf5368c4b71f528a00e7786abb19f087b87637fec040dc063488ed",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/projections-older-people-sex-ratios/editions/time-series/versions/1"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2018",
    "end": "2043",
    "sourceField": "temporal.options",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "year",
    "derivation": "ONS-native-ISO-period-code.v1"
  },
  "update": {
    "frequency": {
      "status": "source-stated",
      "label": "Biennial",
      "iri": null,
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "To be announced",
    "metadataModified": "2020-11-02T11:02:21.237Z",
    "releaseVersion": "1"
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [],
  "details": {
    "dimensions": [
      {
        "description": "All years between 2018 and 2043",
        "id": "calendar-years",
        "label": "Time",
        "name": "time"
      },
      {
        "description": "Data are available at a local authority, region and country level for England, Wales, Scotland and Northern Ireland.",
        "id": "administrative-geography",
        "label": "Geography",
        "name": "geography"
      },
      {
        "description": "Sex ratio 65 years and over, Sex ratio 85 years and over.",
        "id": "age-groups",
        "label": "Age group",
        "name": "agegroups"
      }
    ],
    "edition": "time-series",
    "id": "projections-older-people-sex-ratios",
    "metadata": {
      "description": "Projected indicators included are derived from the published 2018-based subnational population projections for England, Wales, Scotland and Northern Ireland up to the year 2043. The indicators are the projected sex ratio for those aged 65 years and over and the projected sex ratio for those aged 85 years and over. A sex ratio shows the number of males in the population for every 100 females. This dataset has been produced by the Ageing Analysis Team for inclusion in the subnational ageing tool, which was published on July 20, 2020 (see link in Related datasets). The tool is interactive, and users can compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. Note on data sources: England, Wales, Scotland and Northern Ireland independently publish subnational population projections and the data available here are a compilation of these datasets. The ONS publish national level data for the UK, England, Wales and England & Wales, which has been included. National level data for Scotland and Northern Ireland have been taken from their subnational population projections datasets.",
      "last_updated": "2020-11-02T11:02:21.237Z",
      "next_release": "To be announced",
      "release_date": "2020-08-17T00:00:00.000Z",
      "release_frequency": "Biennial",
      "state": "published",
      "title": "Local authority ageing statistics, projected sex ratios for older people"
    },
    "metadataContract": {
      "catalogueType": null,
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "time-series",
        "id": "projections-older-people-sex-ratios",
        "version": 1
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:30:51.051875Z",
      "sha256": "5d6fe24cd1d25f4cac738213d7f7ff05fbf512a2a8788866258d0b5084a1155a",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/projections-older-people-sex-ratios/editions/time-series/versions/1/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "bounds": {
        "basis": "published time-dimension option codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": "2043",
        "minimumNative": "2018",
        "status": "known-option-extrema"
      },
      "complete": true,
      "duplicateCount": 0,
      "options": [
        {
          "dimension": "time",
          "label": "2018",
          "option": "2018"
        },
        {
          "dimension": "time",
          "label": "2019",
          "option": "2019"
        },
        {
          "dimension": "time",
          "label": "2020",
          "option": "2020"
        },
        {
          "dimension": "time",
          "label": "2021",
          "option": "2021"
        },
        {
          "dimension": "time",
          "label": "2022",
          "option": "2022"
        },
        {
          "dimension": "time",
          "label": "2023",
          "option": "2023"
        },
        {
          "dimension": "time",
          "label": "2024",
          "option": "2024"
        },
        {
          "dimension": "time",
          "label": "2025",
          "option": "2025"
        },
        {
          "dimension": "time",
          "label": "2026",
          "option": "2026"
        },
        {
          "dimension": "time",
          "label": "2027",
          "option": "2027"
        },
        {
          "dimension": "time",
          "label": "2028",
          "option": "2028"
        },
        {
          "dimension": "time",
          "label": "2029",
          "option": "2029"
        },
        {
          "dimension": "time",
          "label": "2030",
          "option": "2030"
        },
        {
          "dimension": "time",
          "label": "2031",
          "option": "2031"
        },
        {
          "dimension": "time",
          "label": "2032",
          "option": "2032"
        },
        {
          "dimension": "time",
          "label": "2033",
          "option": "2033"
        },
        {
          "dimension": "time",
          "label": "2034",
          "option": "2034"
        },
        {
          "dimension": "time",
          "label": "2035",
          "option": "2035"
        },
        {
          "dimension": "time",
          "label": "2036",
          "option": "2036"
        },
        {
          "dimension": "time",
          "label": "2037",
          "option": "2037"
        },
        {
          "dimension": "time",
          "label": "2038",
          "option": "2038"
        },
        {
          "dimension": "time",
          "label": "2039",
          "option": "2039"
        },
        {
          "dimension": "time",
          "label": "2040",
          "option": "2040"
        },
        {
          "dimension": "time",
          "label": "2041",
          "option": "2041"
        },
        {
          "dimension": "time",
          "label": "2042",
          "option": "2042"
        },
        {
          "dimension": "time",
          "label": "2043",
          "option": "2043"
        }
      ],
      "reportedTotal": 26,
      "retrievedUnique": 26,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "1",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/projections-older-people-sex-ratios/editions/time-series/versions/1"
  },
  "dcterms:accrualPeriodicity": {
    "@type": "dcterms:Frequency",
    "rdfs:label": "Biennial"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2043",
      "minimumNative": "2018",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Local authority ageing statistics, projected sex ratios for older people

Projected indicators included are derived from the published 2018-based subnational population projections for England, Wales, Scotland and Northern Ireland up to the year 2043. The indicators are the projected sex ratio for those aged 65 years and over and the projected sex ratio for those aged 85 years and over. A sex ratio shows the number of males in the population for every 100 females. This dataset has been produced by the Ageing Analysis Team for inclusion in the subnational ageing tool, which was published on July 20, 2020 (see link in Related datasets). The tool is interactive, and users can compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. Note on data sources: England, Wales, Scotland and Northern Ireland independently publish subnational population projections and the data available here are a compilation of these datasets. The ONS publish national level data for the UK, England, Wales and England & Wales, which has been included. National level data for Scotland and Northern Ireland have been taken from their subnational population projections datasets.

Native identifier: `projections-older-people-sex-ratios`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/projections-older-people-sex-ratios/editions/time-series/versions/1)

Update cadence: Biennial.
Temporal evidence: normalised-source-options (available-native-period-options); start 2018, end 2043.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
