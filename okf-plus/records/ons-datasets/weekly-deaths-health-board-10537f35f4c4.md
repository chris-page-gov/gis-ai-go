---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/weekly-deaths-health-board",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Death registrations and occurrences by health board and place of death",
  "description": "Provisional counts of the number of deaths registered in Wales, by health board and place of death, in the latest weeks for which data are available.",
  "nativeIdentifier": "weekly-deaths-health-board",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-health-board",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Deaths",
    "weekly deaths"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/4",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/4",
      "normalisedRecordSha256": "07e89e60296833876757bedad52d549edf75d934154347167fc175855c093df9",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-health-board/editions/2023/versions/50/metadata",
      "retrievedAt": "2026-10-02T01:30:24.871299Z",
      "responseSha256": "bc3d1d8ec96da8d6fdf212d25f7920d3e21a0ea80cc1c983beebecd9ce6431f5",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/4",
      "normalisedRecordSha256": "d1a052bfe86d03562623cae252208f3cfb3d879c173225f90fca4cec6c78d09a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-health-board"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2023",
    "end": "2023",
    "sourceField": "timeMetadata.temporal.options",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "year",
    "derivation": "ONS-native-ISO-period-code.v1"
  },
  "update": {
    "frequency": {
      "status": "source-stated",
      "label": "Weekly",
      "iri": "http://purl.org/linked-data/sdmx/2009/code#freq-W",
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "17 January 2024",
    "metadataModified": "2024-01-09T10:11:08.441Z",
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
    "description": "Provisional counts of the number of deaths registered in Wales, by health board and place of death, in the latest weeks for which data are available.",
    "id": "weekly-deaths-health-board",
    "keywords": [
      "Deaths",
      "weekly deaths"
    ],
    "last_updated": "2024-01-09T10:11:08.441Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-health-board/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-health-board/editions/2023/versions/50",
        "id": "50"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-health-board"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths"
      }
    },
    "national_statistic": true,
    "next_release": "17 January 2024",
    "qmi": {
      "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/methodologies/mortalitystatisticsinenglandandwalesqmi"
    },
    "release_frequency": "Weekly",
    "state": "published",
    "title": "Death registrations and occurrences by health board and place of death",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "calendar-years",
          "label": "Time",
          "name": "time"
        },
        {
          "id": "local-health-board",
          "label": "Geography",
          "name": "geography"
        },
        {
          "id": "week-number",
          "label": "Week",
          "name": "week"
        },
        {
          "id": "cause-of-death",
          "label": "Cause of death",
          "name": "causeofdeath"
        },
        {
          "id": "place-of-death",
          "label": "Place of death",
          "name": "placeofdeath"
        },
        {
          "id": "registration-or-occurrence",
          "label": "Registration or occurrence",
          "name": "registrationoroccurrence"
        }
      ],
      "edition": "2023",
      "id": "weekly-deaths-health-board",
      "metadata": {
        "description": "Provisional counts of the number of deaths registered in Wales, by health board and place of death, in the latest weeks for which data are available.",
        "last_updated": "2024-01-09T10:11:08.441Z",
        "next_release": "17 January 2024",
        "release_date": "2024-01-09T00:00:00.000Z",
        "release_frequency": "Weekly",
        "state": "published",
        "title": "Death registrations and occurrences by health board and place of death"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "2023",
          "id": "weekly-deaths-health-board",
          "version": 50
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:30:24.871299Z",
        "sha256": "bc3d1d8ec96da8d6fdf212d25f7920d3e21a0ea80cc1c983beebecd9ce6431f5",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-health-board/editions/2023/versions/50/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2023",
          "minimumNative": "2023",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "2023",
            "option": "2023"
          }
        ],
        "reportedTotal": 1,
        "retrievedUnique": 1,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "50",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-health-board/editions/2023/versions/50"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-W"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-health-board/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2023",
      "minimumNative": "2023",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Death registrations and occurrences by health board and place of death

Provisional counts of the number of deaths registered in Wales, by health board and place of death, in the latest weeks for which data are available.

Native identifier: `weekly-deaths-health-board`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-health-board)

Update cadence: Weekly.
Temporal evidence: normalised-source-options (available-native-period-options); start 2023, end 2023.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
