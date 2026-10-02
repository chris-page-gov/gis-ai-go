---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/ashe-tables-11-and-12",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Earnings and Hours Worked, Work and Residence-Based Travel to Work Area: ASHE Tables 11 and 12",
  "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by home-based and work-based travel to work area. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
  "nativeIdentifier": "ashe-tables-11-and-12",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-11-and-12",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ASHE",
    "pay,wages,income,comparison of earnings"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/47",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/47",
      "normalisedRecordSha256": "6d03c37862d4f8c0f268e40c2930a42d0e311502379223428a02a42d396d6c89",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-11-and-12/editions/time-series/versions/4/metadata",
      "retrievedAt": "2026-10-02T01:31:36.411881Z",
      "responseSha256": "3dc5d5c3d1c99feecd2ffbd7cf6c18bddfb224a43540b6e93dcd9c0741edc001",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/47",
      "normalisedRecordSha256": "28fbbf2a915a287ef5b2d1d4e561aabc9f7389cf1e39a80170f1c8c5b07f7950",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-11-and-12"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2014",
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
    "metadataModified": "2023-09-04T09:19:54.005Z",
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
    "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by home-based and work-based travel to work area. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
    "id": "ashe-tables-11-and-12",
    "keywords": [
      "ASHE",
      "pay,wages,income,comparison of earnings"
    ],
    "last_updated": "2023-09-04T09:19:54.005Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-11-and-12/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-11-and-12/editions/time-series/versions/4",
        "id": "4"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-11-and-12"
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
    "title": "Earnings and Hours Worked, Work and Residence-Based Travel to Work Area: ASHE Tables 11 and 12",
    "timeMetadata": {
      "dimensions": [
        {
          "description": "The latest year has provisional data. All other years have revised data.",
          "id": "calendar-years",
          "label": "Time",
          "name": "time"
        },
        {
          "id": "travel-to-work-area",
          "label": "Geography",
          "name": "geography"
        },
        {
          "id": "averages-and-percentiles",
          "label": "Statistics",
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
      "edition": "time-series",
      "id": "ashe-tables-11-and-12",
      "metadata": {
        "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by home-based and work-based travel to work area. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
        "last_updated": "2023-09-04T09:19:54.005Z",
        "next_release": "To be announced",
        "release_date": "2023-09-01T00:00:00.000Z",
        "release_frequency": "Annual",
        "state": "published",
        "title": "Earnings and Hours Worked, Work and Residence-Based Travel to Work Area: ASHE Tables 11 and 12"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "ashe-tables-11-and-12",
          "version": 4
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:31:36.411881Z",
        "sha256": "3dc5d5c3d1c99feecd2ffbd7cf6c18bddfb224a43540b6e93dcd9c0741edc001",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-11-and-12/editions/time-series/versions/4/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2022",
          "minimumNative": "2014",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
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
          },
          {
            "dimension": "time",
            "label": "2017",
            "option": "2017"
          },
          {
            "dimension": "time",
            "label": "2016",
            "option": "2016"
          },
          {
            "dimension": "time",
            "label": "2015",
            "option": "2015"
          },
          {
            "dimension": "time",
            "label": "2014",
            "option": "2014"
          }
        ],
        "reportedTotal": 9,
        "retrievedUnique": 9,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "4",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-11-and-12/editions/time-series/versions/4"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-11-and-12/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2022",
      "minimumNative": "2014",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Earnings and Hours Worked, Work and Residence-Based Travel to Work Area: ASHE Tables 11 and 12

Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by home-based and work-based travel to work area. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.

Native identifier: `ashe-tables-11-and-12`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-11-and-12)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2014, end 2022.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
