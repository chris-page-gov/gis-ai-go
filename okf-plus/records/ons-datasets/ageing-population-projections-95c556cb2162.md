---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/ageing-population-projections",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Local authority ageing statistics, population projections for older people",
  "description": "Projected indicators included are derived from the published 2018-based subnational population projections for England, Wales, Scotland and Northern Ireland up to the year 2043. The indicators are the projected percentage of the population aged 65 years and over, 85 years and over, 0 to 15 years, 16 to 64 years, 16 years to State Pension age, State Pension age and over, median age and the Old Age Dependency Ratio (the number of people of State Pension age per 1000 of those aged 16 years to below State Pension age). This dataset has been produced by the Ageing Analysis Team for inclusion in the subnational ageing tool, which was published on July 20, 2020 (see link in Related datasets). The tool is interactive, and users can compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. Note on data sources: England, Wales, Scotland and Northern Ireland independently publish subnational population projections and the data available here are a compilation of these datasets. The ONS publish national level data for the UK, England, Wales and England & Wales, which has been included. National level data for Scotland and Northern Ireland have been taken from their subnational population projections datasets.",
  "nativeIdentifier": "ageing-population-projections",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-projections",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ageing",
    "projections",
    "population"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/49",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/49",
      "normalisedRecordSha256": "e8447801ad5919c49894f3dbff6c96f4755ec3919c68388932ebb1f9868dc982",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-projections/editions/time-series/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:31:39.779512Z",
      "responseSha256": "0fe516bdcf02f993557d0047c16c038ead6f71b538d14da785d615c9480aaae5",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/49",
      "normalisedRecordSha256": "8339cc16f055696a86db2dafe633841e5c5e0bf4f33edadad23abb382e46558c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-projections"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2018",
    "end": "2043",
    "sourceField": "timeMetadata.temporal.options",
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
    "metadataModified": "2020-11-02T10:36:31.034Z",
    "releaseVersion": null
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "ONS published-data terms apply; dataset-specific notices and third-party rights must be checked.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "Time-option extrema describe available native codes; continuity and populated observation cells have not been established."
  ],
  "details": {
    "description": "Projected indicators included are derived from the published 2018-based subnational population projections for England, Wales, Scotland and Northern Ireland up to the year 2043. The indicators are the projected percentage of the population aged 65 years and over, 85 years and over, 0 to 15 years, 16 to 64 years, 16 years to State Pension age, State Pension age and over, median age and the Old Age Dependency Ratio (the number of people of State Pension age per 1000 of those aged 16 years to below State Pension age). \n\nThis dataset has been produced by the Ageing Analysis Team for inclusion in the subnational ageing tool, which was published on July 20, 2020 (see link in Related datasets). The tool is interactive, and users can compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. \n\nNote on data sources: England, Wales, Scotland and Northern Ireland independently publish subnational population projections and the data available here are a compilation of these datasets. The ONS publish national level data for the UK, England, Wales and England & Wales, which has been included. National level data for Scotland and Northern Ireland have been taken from their subnational population projections datasets.",
    "id": "ageing-population-projections",
    "keywords": [
      "ageing",
      "projections",
      "population"
    ],
    "last_updated": "2020-11-02T10:36:31.034Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-projections/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-projections/editions/time-series/versions/1",
        "id": "1"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-projections"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/birthsdeathsandmarriages/ageing"
      }
    },
    "methodologies": [
      {
        "href": "https://www.nrscotland.gov.uk/files//statistics/population-projections/sub-national-pp-18/pop-proj-principal-18-methodology.pdf",
        "title": "Scotland Methodology Guide"
      },
      {
        "href": "https://gov.wales/population-and-household-statistics-technical-information",
        "title": "Wales technical information"
      },
      {
        "href": "https://www.nisra.gov.uk/sites/nisra.gov.uk/files/publications/SNPP18-Methodology.pdf",
        "title": "Northern Ireland methodology paper"
      }
    ],
    "next_release": "To be announced",
    "qmi": {
      "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationprojections/methodologies/subnationalpopulationprojectionsqmi"
    },
    "related_datasets": [
      {
        "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationprojections/bulletins/subnationalpopulationprojectionsforengland/2018based",
        "title": "Subnational population projections for England: 2018-based"
      },
      {
        "href": "https://www.nrscotland.gov.uk/statistics-and-data/statistics/statistics-by-theme/population/population-projections/sub-national-population-projections/2018-based",
        "title": "Population Projections for Scottish Areas (2018-based)"
      },
      {
        "href": "https://gov.wales/subnational-population-projections-2018-based",
        "title": "Wales subnational population projections (local authority): 2018-based"
      },
      {
        "href": "https://www.nisra.gov.uk/publications/2018-based-population-projections-areas-within-northern-ireland",
        "title": "2018-based Population Projections for Areas within Northern Ireland"
      },
      {
        "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/ageing/articles/subnationalageingtool/2020-07-20",
        "title": "Subnational ageing tool"
      }
    ],
    "release_frequency": "Biennial",
    "state": "published",
    "title": "Local authority ageing statistics, population projections for older people",
    "timeMetadata": {
      "dimensions": [
        {
          "description": "Data are available for the years 2018 to 2043.",
          "id": "calendar-years",
          "label": "Time",
          "name": "time"
        },
        {
          "description": "Data are available at a local authority, region and country level for England, Wales, Scotland and Northern Ireland",
          "id": "administrative-geography",
          "label": "Geography",
          "name": "geography"
        },
        {
          "description": "Data are available for All Persons, Males and Females.",
          "id": "sex",
          "label": "Sex",
          "name": "sex"
        },
        {
          "description": "% 15 years and under, % 16-64 years, % 65 years and over, % 85 years and over, % 16 years and up to State Pension age, % State Pension age and over, Median age, Old Age Dependency Ratio (the number of people of State Pension age per 1000 of those aged 16 years to below State Pension age)",
          "id": "age-groups",
          "label": "Age groups",
          "name": "agegroups"
        },
        {
          "id": "unit-of-measure",
          "label": "Unit of measure",
          "name": "unitofmeasure"
        }
      ],
      "edition": "time-series",
      "id": "ageing-population-projections",
      "metadata": {
        "description": "Projected indicators included are derived from the published 2018-based subnational population projections for England, Wales, Scotland and Northern Ireland up to the year 2043. The indicators are the projected percentage of the population aged 65 years and over, 85 years and over, 0 to 15 years, 16 to 64 years, 16 years to State Pension age, State Pension age and over, median age and the Old Age Dependency Ratio (the number of people of State Pension age per 1000 of those aged 16 years to below State Pension age). This dataset has been produced by the Ageing Analysis Team for inclusion in the subnational ageing tool, which was published on July 20, 2020 (see link in Related datasets). The tool is interactive, and users can compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. Note on data sources: England, Wales, Scotland and Northern Ireland independently publish subnational population projections and the data available here are a compilation of these datasets. The ONS publish national level data for the UK, England, Wales and England & Wales, which has been included. National level data for Scotland and Northern Ireland have been taken from their subnational population projections datasets.",
        "last_updated": "2020-11-02T10:36:31.034Z",
        "next_release": "To be announced",
        "release_date": "2020-08-18T00:00:00.000Z",
        "release_frequency": "Biennial",
        "state": "published",
        "title": "Local authority ageing statistics, population projections for older people"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "ageing-population-projections",
          "version": 1
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:31:39.779512Z",
        "sha256": "0fe516bdcf02f993557d0047c16c038ead6f71b538d14da785d615c9480aaae5",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-projections/editions/time-series/versions/1/metadata"
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
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-projections/editions/time-series/versions/1"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@type": "dcterms:Frequency",
    "rdfs:label": "Biennial"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-projections/editions"
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

# Local authority ageing statistics, population projections for older people

Projected indicators included are derived from the published 2018-based subnational population projections for England, Wales, Scotland and Northern Ireland up to the year 2043. The indicators are the projected percentage of the population aged 65 years and over, 85 years and over, 0 to 15 years, 16 to 64 years, 16 years to State Pension age, State Pension age and over, median age and the Old Age Dependency Ratio (the number of people of State Pension age per 1000 of those aged 16 years to below State Pension age). This dataset has been produced by the Ageing Analysis Team for inclusion in the subnational ageing tool, which was published on July 20, 2020 (see link in Related datasets). The tool is interactive, and users can compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. Note on data sources: England, Wales, Scotland and Northern Ireland independently publish subnational population projections and the data available here are a compilation of these datasets. The ONS publish national level data for the UK, England, Wales and England & Wales, which has been included. National level data for Scotland and Northern Ireland have been taken from their subnational population projections datasets.

Native identifier: `ageing-population-projections`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/ageing-population-projections)

Update cadence: Biennial.
Temporal evidence: normalised-source-options (available-native-period-options); start 2018, end 2043.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
