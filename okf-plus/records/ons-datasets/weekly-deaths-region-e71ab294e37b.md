---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/weekly-deaths-region",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Deaths registered weekly in England and Wales by region",
  "description": "Provisional counts of the number of deaths registered in England and Wales, by region, in the latest weeks for which data are available.",
  "nativeIdentifier": "weekly-deaths-region",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region",
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
      "sourcePointer": "/items/2",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/2",
      "normalisedRecordSha256": "30a843daab1f83cfaf9aa62237f59bc762c4355f3bd6004c5826c800aa628901",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121/metadata",
      "retrievedAt": "2026-10-02T01:30:21.467028Z",
      "responseSha256": "de8c50bc396fb4a16a72c9bf6d9cdfa91bd0e3594d6352d1a9c4397529a58055",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/2",
      "normalisedRecordSha256": "e4b5616e679fbddf7971eb06830b83af66183f0633af2f72baa5baa6b3582233",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2025",
    "end": "2026",
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
    "nextRelease": "24 June 2026",
    "metadataModified": "2026-07-01T10:46:27.849Z",
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
    "description": "Provisional counts of the number of deaths registered in England and Wales, by region, in the latest weeks for which data are available.",
    "id": "weekly-deaths-region",
    "keywords": [
      "Deaths",
      "weekly deaths"
    ],
    "last_updated": "2026-07-01T10:46:27.849Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121",
        "id": "121"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths"
      }
    },
    "national_statistic": true,
    "next_release": "24 June 2026",
    "qmi": {
      "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/methodologies/mortalitystatisticsinenglandandwalesqmi"
    },
    "release_frequency": "Weekly",
    "state": "published",
    "title": "Deaths registered weekly in England and Wales by region",
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
          "label": "cause of death",
          "name": "causeofdeath"
        }
      ],
      "edition": "time-series",
      "id": "weekly-deaths-region",
      "metadata": {
        "description": "Provisional counts of the number of deaths registered in England and Wales, by region, in the latest weeks for which data are available.",
        "last_updated": "2026-07-01T10:46:27.849Z",
        "next_release": "24 June 2026",
        "release_date": "2026-07-01T00:00:00.000Z",
        "release_frequency": "Weekly",
        "state": "published",
        "title": "Deaths registered weekly in England and Wales by region"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "weekly-deaths-region",
          "version": 121
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:30:21.467028Z",
        "sha256": "de8c50bc396fb4a16a72c9bf6d9cdfa91bd0e3594d6352d1a9c4397529a58055",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2026",
          "minimumNative": "2025",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "2026",
            "option": "2026"
          },
          {
            "dimension": "time",
            "label": "2025",
            "option": "2025"
          }
        ],
        "reportedTotal": 2,
        "retrievedUnique": 2,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "121",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions/time-series/versions/121"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-W"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2026",
      "minimumNative": "2025",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Deaths registered weekly in England and Wales by region

Provisional counts of the number of deaths registered in England and Wales, by region, in the latest weeks for which data are available.

Native identifier: `weekly-deaths-region`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-region)

Update cadence: Weekly.
Temporal evidence: normalised-source-options (available-native-period-options); start 2025, end 2026.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
