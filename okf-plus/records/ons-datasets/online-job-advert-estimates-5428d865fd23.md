---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/online-job-advert-estimates",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Faster Indicators - Online Job Advert Estimates",
  "description": "Experimental job advert indices covering the UK job market.",
  "nativeIdentifier": "online-job-advert-estimates",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/online-job-advert-estimates",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/23",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/23",
      "normalisedRecordSha256": "f10dcdafe813b8bba3b714fa04cfc3a96d1d5a5d8348bd0bcdace8fd72008303",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/online-job-advert-estimates/editions/feb-2020-index-by-category/versions/175/metadata",
      "retrievedAt": "2026-10-02T01:30:56.118496Z",
      "responseSha256": "2b85ca3884163ee5bfa715aceea851660020cee7c89564cc96e0df09869b7067",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/23",
      "normalisedRecordSha256": "1ef94012d4875c2f1a87d254d3a985a488c5412a4cda07ddfaa3729f32668379",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/online-job-advert-estimates"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2018",
    "end": "2024",
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
    "nextRelease": "To be announced",
    "metadataModified": "2024-10-24T09:07:19.412Z",
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
    "description": "Experimental job advert indices covering the UK job market.",
    "id": "online-job-advert-estimates",
    "last_updated": "2024-10-24T09:07:19.412Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/online-job-advert-estimates/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/online-job-advert-estimates/editions/feb-2020-index-by-category/versions/175",
        "id": "175"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/online-job-advert-estimates"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/businessindustryandtrade/business/activitysizeandlocation"
      }
    },
    "national_statistic": false,
    "next_release": "To be announced",
    "qmi": {
      "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/methodologies/usingadzunadatatoderiveanindicatorofweeklyvacanciesexperimentalstatistics"
    },
    "release_frequency": "Weekly",
    "state": "published",
    "title": "Faster Indicators - Online Job Advert Estimates",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "calendar-years",
          "label": "Time",
          "name": "time"
        },
        {
          "id": "uk-only",
          "label": "Geography",
          "name": "geography"
        },
        {
          "id": "week-number",
          "label": "Week",
          "name": "week"
        },
        {
          "id": "adzuna-jobs-category",
          "label": "Adzuna jobs category",
          "name": "adzunajobscategory"
        }
      ],
      "edition": "feb-2020-index-by-category",
      "id": "online-job-advert-estimates",
      "metadata": {
        "description": "Experimental job advert indices covering the UK job market.",
        "last_updated": "2024-10-24T09:07:19.412Z",
        "next_release": "To be announced",
        "release_date": "2024-10-24T00:00:00.000Z",
        "release_frequency": "Weekly",
        "state": "published",
        "title": "Faster Indicators - Online Job Advert Estimates"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "feb-2020-index-by-category",
          "id": "online-job-advert-estimates",
          "version": 175
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:30:56.118496Z",
        "sha256": "2b85ca3884163ee5bfa715aceea851660020cee7c89564cc96e0df09869b7067",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/online-job-advert-estimates/editions/feb-2020-index-by-category/versions/175/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2024",
          "minimumNative": "2018",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "2024",
            "option": "2024"
          },
          {
            "dimension": "time",
            "label": "2023",
            "option": "2023"
          },
          {
            "dimension": "time",
            "label": "2022",
            "option": "2022"
          },
          {
            "dimension": "time",
            "label": "2021",
            "option": "2021"
          },
          {
            "dimension": "time",
            "label": "2020",
            "option": "2020"
          },
          {
            "dimension": "time",
            "label": "2019",
            "option": "2019"
          },
          {
            "dimension": "time",
            "label": "2018",
            "option": "2018"
          }
        ],
        "reportedTotal": 7,
        "retrievedUnique": 7,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "175",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/online-job-advert-estimates/editions/feb-2020-index-by-category/versions/175"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-W"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/online-job-advert-estimates/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2024",
      "minimumNative": "2018",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Faster Indicators - Online Job Advert Estimates

Experimental job advert indices covering the UK job market.

Native identifier: `online-job-advert-estimates`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/online-job-advert-estimates)

Update cadence: Weekly.
Temporal evidence: normalised-source-options (available-native-period-options); start 2018, end 2024.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
