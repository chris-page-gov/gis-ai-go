---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/ashe-tables-3",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Earnings and hours worked, region by occupation by two-digit SOC: ASHE Table 3",
  "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by region and two-digit Standard Occupational Classification 2010. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
  "nativeIdentifier": "ashe-tables-3",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-3",
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
      "sourcePointer": "/items/42",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/42",
      "normalisedRecordSha256": "fc27d3bbeb619bc469cdba673730b7a9d0d7be9236442997d39b8a0e62b3275e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-3/editions/time-series/versions/7/metadata",
      "retrievedAt": "2026-10-02T01:31:28.045406Z",
      "responseSha256": "51db8be121d1cd4cb47bab0cc8740ec7306da4cf42e8e483e20a76da91dfb2e6",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/42",
      "normalisedRecordSha256": "2553a1d2c9b97f47d35db53d697c1577bbdd77beb1aa7d435be8612ed2136efb",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-3"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2016",
    "end": "2023",
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
    "metadataModified": "2024-01-23T09:47:39.729Z",
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
    "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by region and two-digit Standard Occupational Classification 2010. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
    "id": "ashe-tables-3",
    "keywords": [
      "ASHE",
      "pay"
    ],
    "last_updated": "2024-01-23T09:47:39.729Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-3/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-3/editions/time-series/versions/7",
        "id": "7"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-3"
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
    "title": "Earnings and hours worked, region by occupation by two-digit SOC: ASHE Table 3",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "calendar-years",
          "label": "Year",
          "name": "time"
        },
        {
          "id": "administrative-geography",
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
          "id": "soc",
          "label": "Standard Occupational Classification",
          "name": "standardoccupationalclassification"
        }
      ],
      "edition": "time-series",
      "id": "ashe-tables-3",
      "metadata": {
        "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by region and two-digit Standard Occupational Classification 2010. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
        "last_updated": "2024-01-23T09:47:39.729Z",
        "next_release": "To be announced",
        "release_date": "2024-01-19T00:00:00.000Z",
        "release_frequency": "Annual",
        "state": "published",
        "title": "Earnings and hours worked, region by occupation by two-digit SOC: ASHE Table 3"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "ashe-tables-3",
          "version": 7
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:31:28.045406Z",
        "sha256": "51db8be121d1cd4cb47bab0cc8740ec7306da4cf42e8e483e20a76da91dfb2e6",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-3/editions/time-series/versions/7/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2023",
          "minimumNative": "2016",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
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
          }
        ],
        "reportedTotal": 8,
        "retrievedUnique": 8,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "7",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-3/editions/time-series/versions/7"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-3/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2023",
      "minimumNative": "2016",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Earnings and hours worked, region by occupation by two-digit SOC: ASHE Table 3

Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by region and two-digit Standard Occupational Classification 2010. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.

Native identifier: `ashe-tables-3`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-3)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2016, end 2023.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
