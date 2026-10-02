---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/ashe-tables-27-and-28",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Earnings and hours worked, place of work and place of residence by local enterprise partnerships: ASHE Tables 27 and 28",
  "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by work-based and home-based local enterprise partnerships. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
  "nativeIdentifier": "ashe-tables-27-and-28",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-27-and-28/editions/2021/versions/2",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-27-and-28/editions/2021/versions/2/metadata",
      "retrievedAt": "2026-10-02T01:31:29.714935Z",
      "responseSha256": "9584edf1286a213f4e785fd5b8e8bf44a4bb5623742806fddd535c5f6b8a0b4d",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/43",
      "normalisedRecordSha256": "386d5953ffe5f3348e7dd03bd993327e254f81c82a46aea9a8a587f84290810d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-27-and-28/editions/2021/versions/2"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2021",
    "end": "2021",
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
    "metadataModified": "2023-09-04T09:20:04.12Z",
    "releaseVersion": "2"
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
        "id": "enterprise-regions",
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
    "edition": "2021",
    "id": "ashe-tables-27-and-28",
    "metadata": {
      "description": "Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by work-based and home-based local enterprise partnerships. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.",
      "last_updated": "2023-09-04T09:20:04.12Z",
      "next_release": "To be announced",
      "release_date": "2023-08-31T00:00:00.000Z",
      "release_frequency": "Annual",
      "state": "published",
      "title": "Earnings and hours worked, place of work and place of residence by local enterprise partnerships: ASHE Tables 27 and 28"
    },
    "metadataContract": {
      "catalogueType": null,
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "2021",
        "id": "ashe-tables-27-and-28",
        "version": 2
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:31:29.714935Z",
      "sha256": "9584edf1286a213f4e785fd5b8e8bf44a4bb5623742806fddd535c5f6b8a0b4d",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-27-and-28/editions/2021/versions/2/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "bounds": {
        "basis": "published time-dimension option codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": "2021",
        "minimumNative": "2021",
        "status": "known-option-extrema"
      },
      "complete": true,
      "duplicateCount": 0,
      "options": [
        {
          "dimension": "time",
          "label": "2021",
          "option": "2021"
        }
      ],
      "reportedTotal": 1,
      "retrievedUnique": 1,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "2",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-27-and-28/editions/2021/versions/2"
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
      "maximumNative": "2021",
      "minimumNative": "2021",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Earnings and hours worked, place of work and place of residence by local enterprise partnerships: ASHE Tables 27 and 28

Annual estimates of paid hours worked and earnings for UK employees by sex, and full-time and part-time, by work-based and home-based local enterprise partnerships. Hourly and weekly estimates are provided for the pay period that included a specified date in April. They relate to employees on adult rates of pay, whose earnings for the survey pay period were not affected by absence. Estimates for 2020 and 2021 include employees who have been furloughed under the Coronavirus Job Retention Scheme (CJRS). Annual estimates are provided for the tax year that ended on 5th April in the reference year. They relate to employees on adult rates of pay who have been in the same job for more than a year.

Native identifier: `ashe-tables-27-and-28`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/ashe-tables-27-and-28/editions/2021/versions/2)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2021, end 2021.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
