---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/weekly-deaths-age-sex",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Deaths registered weekly in England and Wales by age and sex",
  "description": "Provisional counts of the number of deaths registered in England and Wales, by age and sex, in the latest weeks for which data are available.",
  "nativeIdentifier": "weekly-deaths-age-sex",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-age-sex",
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
      "sourcePointer": "/items/5",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/5",
      "normalisedRecordSha256": "12a01214b375b970628338294239dba4a16f76dc1b595ccdc7f409b658ec35de",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-age-sex/editions/2026/versions/20/metadata",
      "retrievedAt": "2026-10-02T01:30:26.555022Z",
      "responseSha256": "bfecb2a562dd57f0558b84ccadb55b6517d0a817c4b77a6651cb3939c3043c93",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/5",
      "normalisedRecordSha256": "40dc8802be4a2fbbe13d415e77ac9bfe9ada961ab735a405458cde3f8a26a5da",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-age-sex"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2026",
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
    "metadataModified": "2026-07-01T10:46:24.825Z",
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
    "description": "Provisional counts of the number of deaths registered in England and Wales, by age and sex, in the latest weeks for which data are available.",
    "id": "weekly-deaths-age-sex",
    "keywords": [
      "Deaths",
      "weekly deaths"
    ],
    "last_updated": "2026-07-01T10:46:24.825Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-age-sex/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-age-sex/editions/2026/versions/20",
        "id": "20"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-age-sex"
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
    "title": "Deaths registered weekly in England and Wales by age and sex",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "calendar-years",
          "name": "time"
        },
        {
          "id": "administrative-geography",
          "name": "geography"
        },
        {
          "id": "week-number",
          "name": "week"
        },
        {
          "id": "sex",
          "name": "sex"
        },
        {
          "id": "age-groups",
          "label": "age groups",
          "name": "agegroups"
        },
        {
          "id": "registration-or-occurrence",
          "label": "registration or occurrence",
          "name": "registrationoroccurrence"
        }
      ],
      "edition": "2026",
      "id": "weekly-deaths-age-sex",
      "metadata": {
        "description": "Provisional counts of the number of deaths registered in England and Wales, by age and sex, in the latest weeks for which data are available.",
        "last_updated": "2026-07-01T10:46:24.825Z",
        "next_release": "24 June 2026",
        "release_date": "2026-07-01T00:00:00.000Z",
        "release_frequency": "Weekly",
        "state": "published",
        "title": "Deaths registered weekly in England and Wales by age and sex"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "2026",
          "id": "weekly-deaths-age-sex",
          "version": 20
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:30:26.555022Z",
        "sha256": "bfecb2a562dd57f0558b84ccadb55b6517d0a817c4b77a6651cb3939c3043c93",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-age-sex/editions/2026/versions/20/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2026",
          "minimumNative": "2026",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "2026",
            "option": "2026"
          }
        ],
        "reportedTotal": 1,
        "retrievedUnique": 1,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "20",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-age-sex/editions/2026/versions/20"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-W"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-age-sex/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2026",
      "minimumNative": "2026",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Deaths registered weekly in England and Wales by age and sex

Provisional counts of the number of deaths registered in England and Wales, by age and sex, in the latest weeks for which data are available.

Native identifier: `weekly-deaths-age-sex`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/weekly-deaths-age-sex)

Update cadence: Weekly.
Temporal evidence: normalised-source-options (available-native-period-options); start 2026, end 2026.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
