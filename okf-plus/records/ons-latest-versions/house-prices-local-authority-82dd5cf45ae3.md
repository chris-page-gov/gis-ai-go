---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/house-prices-local-authority",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "House price statistics for small areas in England and Wales",
  "description": "Summary statistics for housing transactions by local authority in England and Wales, on an annual basis, updated quarterly using HM Land Registry Price Paid Data. Select values from the Year and Month dimensions for data for a 12-month period ending that month and year (e.g. selecting June and 2018 will return the twelve months to June 2018).",
  "nativeIdentifier": "house-prices-local-authority",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/house-prices-local-authority/editions/time-series/versions/10",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/house-prices-local-authority/editions/time-series/versions/10/metadata",
      "retrievedAt": "2026-10-02T01:31:09.554966Z",
      "responseSha256": "519cd22c6c81efa25e50f82d6e403c0f167c8b0d7656f3b7c6867c771c588f68",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/31",
      "normalisedRecordSha256": "d7140445581d81580dd1c1fea5d644d5325fa04984db34ae5450bef0008ca0b4",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/house-prices-local-authority/editions/time-series/versions/10"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2015",
    "end": "2022",
    "sourceField": "temporal.options",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "year",
    "derivation": "ONS-native-ISO-period-code.v1"
  },
  "update": {
    "frequency": {
      "status": "source-stated",
      "label": "Quarterly",
      "iri": "http://purl.org/linked-data/sdmx/2009/code#freq-Q",
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "December 2022",
    "metadataModified": "2022-10-14T08:32:49.806Z",
    "releaseVersion": "10"
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
        "description": "The year in which the 12-month time period ends.",
        "id": "calendar-years",
        "label": "Year",
        "name": "time"
      },
      {
        "description": "Year ending this month.",
        "id": "mmm",
        "label": "Month",
        "name": "month"
      },
      {
        "description": "Local authority areas in England and Wales.",
        "id": "administrative-geography",
        "label": "Geography",
        "name": "geography"
      },
      {
        "description": "Summary statistics including median, mean, count, lower quartile and tenth-percentile.",
        "id": "house-sales-and-prices",
        "label": "House price variable",
        "name": "housesalesandprices"
      },
      {
        "description": "Type of property transacted: detached, semi-detached, terraced and flats and maisonettes",
        "id": "property-type",
        "label": "Property type",
        "name": "propertytype"
      },
      {
        "description": "Type of property transacted: newly-built property or an existing property",
        "id": "build-status",
        "label": "Property status",
        "name": "buildstatus"
      }
    ],
    "edition": "time-series",
    "id": "house-prices-local-authority",
    "metadata": {
      "description": "Summary statistics for housing transactions by local authority in England and Wales, on an annual basis, updated quarterly using HM Land Registry Price Paid Data. Select values from the Year and Month dimensions for data for a 12-month period ending that month and year (e.g. selecting June and 2018 will return the twelve months to June 2018).",
      "last_updated": "2022-10-14T08:32:49.806Z",
      "next_release": "December 2022",
      "release_date": "2022-09-14T00:00:00.000Z",
      "release_frequency": "Quarterly",
      "state": "published",
      "title": "House price statistics for small areas in England and Wales"
    },
    "metadataContract": {
      "catalogueType": null,
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "time-series",
        "id": "house-prices-local-authority",
        "version": 10
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:31:09.554966Z",
      "sha256": "519cd22c6c81efa25e50f82d6e403c0f167c8b0d7656f3b7c6867c771c588f68",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/house-prices-local-authority/editions/time-series/versions/10/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "bounds": {
        "basis": "published time-dimension option codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": "2022",
        "minimumNative": "2015",
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
        }
      ],
      "reportedTotal": 8,
      "retrievedUnique": 8,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "10",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/house-prices-local-authority/editions/time-series/versions/10"
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-Q"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2022",
      "minimumNative": "2015",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# House price statistics for small areas in England and Wales

Summary statistics for housing transactions by local authority in England and Wales, on an annual basis, updated quarterly using HM Land Registry Price Paid Data. Select values from the Year and Month dimensions for data for a 12-month period ending that month and year (e.g. selecting June and 2018 will return the twelve months to June 2018).

Native identifier: `house-prices-local-authority`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/house-prices-local-authority/editions/time-series/versions/10)

Update cadence: Quarterly.
Temporal evidence: normalised-source-options (available-native-period-options); start 2015, end 2022.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
