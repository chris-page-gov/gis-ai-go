---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/ageing-population-estimates",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Local authority ageing statistics, based on annual mid-year population estimates",
  "description": "Indicators included have been derived from the published 2019 mid-year population estimates for the UK, England, Wales, Scotland and Northern Ireland. These are the number of persons and percentage of the population aged 65 years and over, 85 years and over, 0 to 15 years, 16 to 64 years, 16 years to State Pension age, State Pension age and over, median age and the Old Age Dependency Ratio (the number of people of State Pension age per 1000 of those aged 16 years to below State Pension age). This dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which was published in July 2020. The tool enables users to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu.",
  "nativeIdentifier": "ageing-population-estimates",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-estimates",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ageing",
    "population"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/50",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/50",
      "normalisedRecordSha256": "5a973c1a0382d49326b38ddd4abcf73dcb7886bbbbf4e46436d5fbe49dcbca56",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-estimates/editions/time-series/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:31:41.460692Z",
      "responseSha256": "b6b7a248c1f5baf2fe07cb7ea126adadf91821295329e9de69978aeefb88cf74",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/50",
      "normalisedRecordSha256": "bd8db97d28536b94d7c4576d08d0134655a2075c9a40564bfdb8914cd4360c3c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-estimates"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2019",
    "end": "2019",
    "sourceField": "timeMetadata.temporal.options",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "year",
    "derivation": "ONS-native-ISO-period-code.v1"
  },
  "update": {
    "frequency": {
      "status": "source-stated",
      "label": "Annual",
      "iri": "http://purl.org/linked-data/sdmx/2009/code#freq-A",
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "1 June 2021",
    "metadataModified": "2020-11-02T10:07:34.426Z",
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
    "description": "Indicators included have been derived from the published 2019 mid-year population estimates for the UK, England, Wales, Scotland and Northern Ireland. These are the number of persons and percentage of the population aged 65 years and over, 85 years and over, 0 to 15 years, 16 to 64 years, 16 years to State Pension age, State Pension age and over, median age and the Old Age Dependency Ratio (the number of people of State Pension age per 1000 of those aged 16 years to below State Pension age).\n\nThis dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which was published in July 2020. The tool enables users to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu.",
    "id": "ageing-population-estimates",
    "keywords": [
      "ageing",
      "population"
    ],
    "last_updated": "2020-11-02T10:07:34.426Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-estimates/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-estimates/editions/time-series/versions/1",
        "id": "1"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-estimates"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/birthsdeathsandmarriages/ageing"
      }
    },
    "next_release": "1 June 2021",
    "qmi": {
      "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/methodologies/annualmidyearpopulationestimatesqmi"
    },
    "related_datasets": [
      {
        "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland",
        "title": "Estimates of the population for the UK, England and Wales, Scotland and Northern Ireland"
      }
    ],
    "release_frequency": "Annual",
    "state": "published",
    "title": "Local authority ageing statistics, based on annual mid-year population estimates",
    "timeMetadata": {
      "dimensions": [
        {
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
          "description": "Data are available for All Persons, Males and Females.",
          "id": "sex",
          "label": "Sex",
          "name": "sex"
        },
        {
          "description": "Number and % 15 years and under, number and % 16-64 years, number and % 65 years and over, number and % 85 years and over, number and % 16 years and up to State Pension age, number and % State Pension age and over, Median age, Old Age Dependency Ratio (the number of people of State Pension age per 1000 of those aged 16 years to below State Pension age)",
          "id": "age-groups",
          "label": "Age groups",
          "name": "agegroups"
        },
        {
          "description": "Data are available for the number of persons and percentage of the population.",
          "id": "unit-of-measure",
          "label": "Unit of measure",
          "name": "unitofmeasure"
        }
      ],
      "edition": "time-series",
      "id": "ageing-population-estimates",
      "metadata": {
        "description": "Indicators included have been derived from the published 2019 mid-year population estimates for the UK, England, Wales, Scotland and Northern Ireland. These are the number of persons and percentage of the population aged 65 years and over, 85 years and over, 0 to 15 years, 16 to 64 years, 16 years to State Pension age, State Pension age and over, median age and the Old Age Dependency Ratio (the number of people of State Pension age per 1000 of those aged 16 years to below State Pension age). This dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which was published in July 2020. The tool enables users to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu.",
        "last_updated": "2020-11-02T10:07:34.426Z",
        "next_release": "1 June 2021",
        "release_date": "2020-06-30T00:00:00.000Z",
        "release_frequency": "Annual",
        "state": "published",
        "title": "Local authority ageing statistics, based on annual mid-year population estimates"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "ageing-population-estimates",
          "version": 1
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:31:41.460692Z",
        "sha256": "b6b7a248c1f5baf2fe07cb7ea126adadf91821295329e9de69978aeefb88cf74",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-estimates/editions/time-series/versions/1/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2019",
          "minimumNative": "2019",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "2019",
            "option": "2019"
          }
        ],
        "reportedTotal": 1,
        "retrievedUnique": 1,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "1",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-estimates/editions/time-series/versions/1"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ageing-population-estimates/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2019",
      "minimumNative": "2019",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Local authority ageing statistics, based on annual mid-year population estimates

Indicators included have been derived from the published 2019 mid-year population estimates for the UK, England, Wales, Scotland and Northern Ireland. These are the number of persons and percentage of the population aged 65 years and over, 85 years and over, 0 to 15 years, 16 to 64 years, 16 years to State Pension age, State Pension age and over, median age and the Old Age Dependency Ratio (the number of people of State Pension age per 1000 of those aged 16 years to below State Pension age). This dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which was published in July 2020. The tool enables users to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu.

Native identifier: `ageing-population-estimates`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/ageing-population-estimates)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2019, end 2019.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
