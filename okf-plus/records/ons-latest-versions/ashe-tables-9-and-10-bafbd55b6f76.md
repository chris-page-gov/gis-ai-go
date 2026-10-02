---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/ashe-tables-9-and-10",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Earnings and hours worked, place of work and place of residence by Parliamentary constituency: ASHE Tables 9 and 10",
  "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by home and work-based Parliamentary constituency. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
  "nativeIdentifier": "ashe-tables-9-and-10",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-9-and-10/editions/time-series/versions/7",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-9-and-10/editions/time-series/versions/7/metadata",
      "retrievedAt": "2026-10-02T01:31:24.693958Z",
      "responseSha256": "0955edc580c94b16772fd8984d6545307b6404fc601b30db65a48db986e7fba3",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/40",
      "normalisedRecordSha256": "f0e940cd2fb1ac70d671c0362095c4616c58dacf20c8f9b3a0063bb74696cab1",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-9-and-10/editions/time-series/versions/7"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2014",
    "end": "2023",
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
    "metadataModified": "2024-01-25T09:40:12.013Z",
    "releaseVersion": "7"
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
        "label": "Time",
        "name": "time"
      },
      {
        "id": "parliamentary-constituencies",
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
    "edition": "time-series",
    "id": "ashe-tables-9-and-10",
    "metadata": {
      "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by home and work-based Parliamentary constituency. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
      "last_updated": "2024-01-25T09:40:12.013Z",
      "next_release": "To be announced",
      "release_date": "2024-01-24T00:00:00.000Z",
      "release_frequency": "Annual",
      "state": "published",
      "title": "Earnings and hours worked, place of work and place of residence by Parliamentary constituency: ASHE Tables 9 and 10"
    },
    "metadataContract": {
      "catalogueType": null,
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "time-series",
        "id": "ashe-tables-9-and-10",
        "version": 7
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:31:24.693958Z",
      "sha256": "0955edc580c94b16772fd8984d6545307b6404fc601b30db65a48db986e7fba3",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-9-and-10/editions/time-series/versions/7/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "bounds": {
        "basis": "published time-dimension option codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": "2023",
        "minimumNative": "2014",
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
      "reportedTotal": 10,
      "retrievedUnique": 10,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "7",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-9-and-10/editions/time-series/versions/7"
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
      "maximumNative": "2023",
      "minimumNative": "2014",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Earnings and hours worked, place of work and place of residence by Parliamentary constituency: ASHE Tables 9 and 10

Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by home and work-based Parliamentary constituency. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.

Native identifier: `ashe-tables-9-and-10`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-9-and-10/editions/time-series/versions/7)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2014, end 2023.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
