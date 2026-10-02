---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/weekly-deaths-local-authority",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Death registrations and occurrences by local authority and place of death",
  "description": "Provisional counts of the number of deaths registered in England and Wales, including deaths involving the coronavirus (COVID-19), by local authority, health board and place of death in the latest weeks for which data are available.",
  "nativeIdentifier": "weekly-deaths-local-authority",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-local-authority",
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
      "sourcePointer": "/items/3",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/3",
      "normalisedRecordSha256": "0c96d4242949036812d6efd0a3eb9f34eff4887f21afda003e8a0fc18a8b20bc",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-local-authority/editions/2023/versions/50/metadata",
      "retrievedAt": "2026-10-02T01:30:23.173252Z",
      "responseSha256": "8e3be6568f6b5af63c743e6d5445f2019f15bb570b9341c7d6c29ed7651c75b1",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/3",
      "normalisedRecordSha256": "7c0713295d5c1504f8327bd503e7766e3b5878417edd1b8f7db1840d20480f8d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-local-authority"
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
    "metadataModified": "2024-01-09T10:10:57.755Z",
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
    "description": "Provisional counts of the number of deaths registered in England and Wales, including deaths involving the coronavirus (COVID-19), by local authority, health board and place of death in the latest weeks for which data are available.",
    "id": "weekly-deaths-local-authority",
    "keywords": [
      "Deaths",
      "weekly deaths"
    ],
    "last_updated": "2024-01-09T10:10:57.755Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-local-authority/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-local-authority/editions/2023/versions/50",
        "id": "50"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-local-authority"
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
    "title": "Death registrations and occurrences by local authority and place of death",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "calendar-years",
          "label": "time",
          "name": "time"
        },
        {
          "id": "administrative-geography",
          "label": "geography",
          "name": "geography"
        },
        {
          "id": "week-number",
          "label": "week",
          "name": "week"
        },
        {
          "id": "cause-of-death",
          "label": "causeofdeath",
          "name": "causeofdeath"
        },
        {
          "id": "place-of-death",
          "label": "placeofdeath",
          "name": "placeofdeath"
        },
        {
          "id": "registration-or-occurrence",
          "label": "registrationoroccurrence",
          "name": "registrationoroccurrence"
        }
      ],
      "edition": "2023",
      "id": "weekly-deaths-local-authority",
      "metadata": {
        "description": "Provisional counts of the number of deaths registered in England and Wales, including deaths involving the coronavirus (COVID-19), by local authority, health board and place of death in the latest weeks for which data are available.",
        "last_updated": "2024-01-09T10:10:57.755Z",
        "next_release": "17 January 2024",
        "release_date": "2024-01-09T00:00:00.000Z",
        "release_frequency": "Weekly",
        "state": "published",
        "title": "Death registrations and occurrences by local authority and place of death"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "2023",
          "id": "weekly-deaths-local-authority",
          "version": 50
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:30:23.173252Z",
        "sha256": "8e3be6568f6b5af63c743e6d5445f2019f15bb570b9341c7d6c29ed7651c75b1",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-local-authority/editions/2023/versions/50/metadata"
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
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-local-authority/editions/2023/versions/50"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-W"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-local-authority/editions"
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

# Death registrations and occurrences by local authority and place of death

Provisional counts of the number of deaths registered in England and Wales, including deaths involving the coronavirus (COVID-19), by local authority, health board and place of death in the latest weeks for which data are available.

Native identifier: `weekly-deaths-local-authority`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-local-authority)

Update cadence: Weekly.
Temporal evidence: normalised-source-options (available-native-period-options); start 2023, end 2023.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
