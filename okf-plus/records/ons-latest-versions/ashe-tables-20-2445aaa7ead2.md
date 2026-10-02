---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/ashe-tables-20",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Earnings and hours worked, age group by occupation by two-digit SOC: ASHE Table 20",
  "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by age group and two-digit Standard Occupational Classification 2010. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
  "nativeIdentifier": "ashe-tables-20",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-20/editions/time-series/versions/5",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-20/editions/time-series/versions/5/metadata",
      "retrievedAt": "2026-10-02T01:31:34.742721Z",
      "responseSha256": "0050856d757f1719a21f7b3881a962f835ace59bb8326dc82f259f06348b51d2",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/46",
      "normalisedRecordSha256": "1af9ea7166d970f7644843ea7d8dfc44376a189d0b9fbd567a7d81e51f1f2908",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-20/editions/time-series/versions/5"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2011",
    "end": "2022",
    "sourceField": "temporal.options",
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
    "metadataModified": "2023-09-04T09:19:56.498Z",
    "releaseVersion": "5"
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [],
  "details": {
    "dimensions": [
      {
        "id": "calendar-years",
        "label": "Year",
        "name": "time"
      },
      {
        "id": "uk-only",
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
      },
      {
        "id": "age-groups",
        "label": "Age groups",
        "name": "agegroups"
      }
    ],
    "edition": "time-series",
    "id": "ashe-tables-20",
    "metadata": {
      "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by age group and two-digit Standard Occupational Classification 2010. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
      "last_updated": "2023-09-04T09:19:56.498Z",
      "next_release": "To be announced",
      "release_date": "2023-09-01T00:00:00.000Z",
      "release_frequency": "Annual",
      "state": "published",
      "title": "Earnings and hours worked, age group by occupation by two-digit SOC: ASHE Table 20"
    },
    "metadataContract": {
      "catalogueType": null,
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "time-series",
        "id": "ashe-tables-20",
        "version": 5
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:31:34.742721Z",
      "sha256": "0050856d757f1719a21f7b3881a962f835ace59bb8326dc82f259f06348b51d2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-20/editions/time-series/versions/5/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "bounds": {
        "basis": "published time-dimension option codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": "2022",
        "minimumNative": "2011",
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
        },
        {
          "dimension": "time",
          "label": "2013",
          "option": "2013"
        },
        {
          "dimension": "time",
          "label": "2012",
          "option": "2012"
        },
        {
          "dimension": "time",
          "label": "2011",
          "option": "2011"
        }
      ],
      "reportedTotal": 12,
      "retrievedUnique": 12,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "5",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-20/editions/time-series/versions/5"
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2022",
      "minimumNative": "2011",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Earnings and hours worked, age group by occupation by two-digit SOC: ASHE Table 20

Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by age group and two-digit Standard Occupational Classification 2010. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.

Native identifier: `ashe-tables-20`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-20/editions/time-series/versions/5)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2011, end 2022.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
