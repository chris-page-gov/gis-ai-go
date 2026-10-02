---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/ashe-tables-25",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Earnings and hours worked, UK region by public and private sector: ASHE Table 25",
  "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by region, and public and private sector, and non-profit bodies and mutual associations. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
  "nativeIdentifier": "ashe-tables-25",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-25/editions/time-series/versions/7",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-25/editions/time-series/versions/7/metadata",
      "retrievedAt": "2026-10-02T01:31:33.066177Z",
      "responseSha256": "d3099fe6e209d66ffde47edf487a9b19a0a4bf401d5b44c716ef8603c3ce1064",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/45",
      "normalisedRecordSha256": "ac3e496af8906ea9c7d2c65e08b9cd93abbe95b65f8056094d7d30dbb3bdf175",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-25/editions/time-series/versions/7"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2016",
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
    "metadataModified": "2024-01-23T09:47:34.802Z",
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
        "id": "sector",
        "label": "Sector",
        "name": "sector"
      }
    ],
    "edition": "time-series",
    "id": "ashe-tables-25",
    "metadata": {
      "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by region, and public and private sector, and non-profit bodies and mutual associations. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
      "last_updated": "2024-01-23T09:47:34.802Z",
      "next_release": "To be announced",
      "release_date": "2024-01-15T00:00:00.000Z",
      "release_frequency": "Annual",
      "state": "published",
      "title": "Earnings and hours worked, UK region by public and private sector: ASHE Table 25"
    },
    "metadataContract": {
      "catalogueType": null,
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "time-series",
        "id": "ashe-tables-25",
        "version": 7
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:31:33.066177Z",
      "sha256": "d3099fe6e209d66ffde47edf487a9b19a0a4bf401d5b44c716ef8603c3ce1064",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-25/editions/time-series/versions/7/metadata"
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
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-25/editions/time-series/versions/7"
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
      "minimumNative": "2016",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Earnings and hours worked, UK region by public and private sector: ASHE Table 25

Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by region, and public and private sector, and non-profit bodies and mutual associations. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.

Native identifier: `ashe-tables-25`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-25/editions/time-series/versions/7)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2016, end 2023.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
