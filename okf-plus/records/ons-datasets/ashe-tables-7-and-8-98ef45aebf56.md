---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/ashe-tables-7-and-8",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Earnings and hours worked, place of work and residence by local authority: ASHE Tables 7 and 8",
  "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by work-based and residence-based region to local and unitary authority level. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
  "nativeIdentifier": "ashe-tables-7-and-8",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-7-and-8",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ASHE",
    "pay"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/41",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/41",
      "normalisedRecordSha256": "66c5de81408f3cb3c73731d27c9cf2845df01b47504936947fcbdca8b1d3fb81",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-7-and-8/editions/2022/versions/2/metadata",
      "retrievedAt": "2026-10-02T01:31:26.378844Z",
      "responseSha256": "08090808fafa58274078bc6961592352c7c6e2c704dda3aeaf537391a314ee55",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/41",
      "normalisedRecordSha256": "c984a0e91f2541d3ff8f742f64491bbe74d7fe5e90c8b865432a9b763f9f05a4",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-7-and-8"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2022",
    "end": "2022",
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
    "nextRelease": "To be announced",
    "metadataModified": "2024-01-23T09:47:44.212Z",
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
    "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by work-based and residence-based region to local and unitary authority level. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
    "id": "ashe-tables-7-and-8",
    "keywords": [
      "ASHE",
      "pay"
    ],
    "last_updated": "2024-01-23T09:47:44.212Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-7-and-8/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-7-and-8/editions/2022/versions/2",
        "id": "2"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-7-and-8"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/employmentandlabourmarket/peopleinwork/earningsandworkinghours"
      }
    },
    "national_statistic": true,
    "next_release": "To be announced",
    "qmi": {
      "href": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/methodologies/annualsurveyofhoursandearningslowpayandannualsurveyofhoursandearningspensionresultsqmi"
    },
    "release_frequency": "Annual",
    "state": "published",
    "title": "Earnings and hours worked, place of work and residence by local authority: ASHE Tables 7 and 8 ",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "calendar-years",
          "label": "Time",
          "name": "time"
        },
        {
          "id": "administrative-geography",
          "label": "Geography",
          "name": "geography"
        },
        {
          "id": "averages-and-percentiles",
          "label": "Averages and percentiles",
          "name": "averagesandpercentiles"
        },
        {
          "id": "sex",
          "label": "Sex",
          "name": "sex"
        },
        {
          "id": "working-pattern",
          "label": "Working pattern",
          "name": "workingpattern"
        },
        {
          "id": "hours-and-earnings",
          "label": "Hours and earnings",
          "name": "hoursandearnings"
        },
        {
          "id": "workplace-or-residence",
          "label": "Workplace or residence",
          "name": "workplaceorresidence"
        }
      ],
      "edition": "2022",
      "id": "ashe-tables-7-and-8",
      "metadata": {
        "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by work-based and residence-based region to local and unitary authority level. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
        "last_updated": "2024-01-23T09:47:44.212Z",
        "next_release": "To be announced",
        "release_date": "2024-01-17T00:00:00.000Z",
        "release_frequency": "Annual",
        "state": "published",
        "title": "Earnings and hours worked, place of work and residence by local authority: ASHE Tables 7 and 8"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "2022",
          "id": "ashe-tables-7-and-8",
          "version": 2
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:31:26.378844Z",
        "sha256": "08090808fafa58274078bc6961592352c7c6e2c704dda3aeaf537391a314ee55",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-7-and-8/editions/2022/versions/2/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2022",
          "minimumNative": "2022",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "2022",
            "option": "2022"
          }
        ],
        "reportedTotal": 1,
        "retrievedUnique": 1,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "2",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-7-and-8/editions/2022/versions/2"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-7-and-8/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2022",
      "minimumNative": "2022",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Earnings and hours worked, place of work and residence by local authority: ASHE Tables 7 and 8

Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by work-based and residence-based region to local and unitary authority level. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.

Native identifier: `ashe-tables-7-and-8`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-7-and-8)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2022, end 2022.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
