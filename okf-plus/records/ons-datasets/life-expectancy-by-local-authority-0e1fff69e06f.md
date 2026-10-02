---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/life-expectancy-by-local-authority",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Life Expectancy by Local Authority",
  "description": "Subnational trends in the average number of years people will live beyond their current age measured by “period life expectancy”.",
  "nativeIdentifier": "life-expectancy-by-local-authority",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/life-expectancy-by-local-authority",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "life expectancy"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/28",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/28",
      "normalisedRecordSha256": "87115ce47132cb481c002399d21f1bbe631717202a8804351cca0669c890d4b1",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/life-expectancy-by-local-authority/editions/time-series/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:31:04.520425Z",
      "responseSha256": "b2e67b492eb768603558d7fd9eed37ee8f17cb42b2c86ebbb4807a8068ca8c9e",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/28",
      "normalisedRecordSha256": "d99874c48d13ecf7ee828d0a3c797d7f60ebb5e6437263078d26b081d18a13fb",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/life-expectancy-by-local-authority"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "not-evidenced",
    "kind": "dataset-reference-period",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "No supported reference-period extent in captured metadata; release and catalogue dates are separate."
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
    "nextRelease": "To be announced",
    "metadataModified": "2020-12-16T13:05:35.252Z",
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
    "description": "Subnational trends in the average number of years people will live beyond their current age measured by “period life expectancy”.",
    "id": "life-expectancy-by-local-authority",
    "keywords": [
      "life expectancy"
    ],
    "last_updated": "2020-12-16T13:05:35.252Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/life-expectancy-by-local-authority/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/life-expectancy-by-local-authority/editions/time-series/versions/1",
        "id": "1"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/life-expectancy-by-local-authority"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies"
      }
    },
    "next_release": "To be announced",
    "qmi": {
      "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/methodologies/healthstatelifeexpectanciesukqmi"
    },
    "release_frequency": "Annual",
    "state": "published",
    "title": "Life Expectancy by Local Authority",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "two-year-intervals",
          "label": "Time",
          "name": "time"
        },
        {
          "id": "administrative-geography",
          "label": "Geography",
          "name": "geography"
        },
        {
          "id": "sex",
          "label": "Sex",
          "name": "sex"
        },
        {
          "id": "age-groups",
          "label": "Age group",
          "name": "agegroups"
        }
      ],
      "edition": "time-series",
      "id": "life-expectancy-by-local-authority",
      "metadata": {
        "description": "Subnational trends in the average number of years people will live beyond their current age measured by “period life expectancy”.",
        "last_updated": "2020-12-16T13:05:35.252Z",
        "next_release": "To be announced",
        "release_date": "2020-11-09T00:00:00.000Z",
        "release_frequency": "Annual",
        "state": "published",
        "title": "Life Expectancy by Local Authority"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "life-expectancy-by-local-authority",
          "version": 1
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:31:04.520425Z",
        "sha256": "b2e67b492eb768603558d7fd9eed37ee8f17cb42b2c86ebbb4807a8068ca8c9e",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/life-expectancy-by-local-authority/editions/time-series/versions/1/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "continuityEstablished": false,
          "maximumNative": null,
          "minimumNative": null,
          "status": "unknown-unrecognised-or-mixed-period-codes"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "2001-03",
            "option": "2001-03"
          },
          {
            "dimension": "time",
            "label": "2002-04",
            "option": "2002-04"
          },
          {
            "dimension": "time",
            "label": "2003-05",
            "option": "2003-05"
          },
          {
            "dimension": "time",
            "label": "2004-06",
            "option": "2004-06"
          },
          {
            "dimension": "time",
            "label": "2005-07",
            "option": "2005-07"
          },
          {
            "dimension": "time",
            "label": "2006-08",
            "option": "2006-08"
          },
          {
            "dimension": "time",
            "label": "2007-09",
            "option": "2007-09"
          },
          {
            "dimension": "time",
            "label": "2008-10",
            "option": "2008-10"
          },
          {
            "dimension": "time",
            "label": "2009-11",
            "option": "2009-11"
          },
          {
            "dimension": "time",
            "label": "2010-12",
            "option": "2010-12"
          },
          {
            "dimension": "time",
            "label": "2011-13",
            "option": "2011-13"
          },
          {
            "dimension": "time",
            "label": "2012-14",
            "option": "2012-14"
          },
          {
            "dimension": "time",
            "label": "2013-15",
            "option": "2013-15"
          },
          {
            "dimension": "time",
            "label": "2014-16",
            "option": "2014-16"
          },
          {
            "dimension": "time",
            "label": "2015-17",
            "option": "2015-17"
          },
          {
            "dimension": "time",
            "label": "2016-18",
            "option": "2016-18"
          },
          {
            "dimension": "time",
            "label": "2017-19",
            "option": "2017-19"
          }
        ],
        "reportedTotal": 17,
        "retrievedUnique": 17,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "1",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/life-expectancy-by-local-authority/editions/time-series/versions/1"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/life-expectancy-by-local-authority/editions"
  }
}
---

# Life Expectancy by Local Authority

Subnational trends in the average number of years people will live beyond their current age measured by “period life expectancy”.

Native identifier: `life-expectancy-by-local-authority`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/life-expectancy-by-local-authority)

Update cadence: Annual.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
