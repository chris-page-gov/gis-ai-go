---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/uk-spending-on-cards",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "UK spending on credit and debit cards",
  "description": "These data series are experimental faster indicators for monitoring UK spending using debit and credit cards.",
  "nativeIdentifier": "uk-spending-on-cards",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/uk-spending-on-cards/editions/time-series/versions/130",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/uk-spending-on-cards/editions/time-series/versions/130/metadata",
      "retrievedAt": "2026-10-02T01:30:28.236811Z",
      "responseSha256": "db97e5590d6540bd9d270e7597a4ca7aa0ab5e893d7d5666d122f57a272161f7",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/6",
      "normalisedRecordSha256": "5896206ad41c3d12219b748bfab4df3f8019a73e4f7317428867439065859eba",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/uk-spending-on-cards/editions/time-series/versions/130"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2020",
    "end": "2024",
    "sourceField": "temporal.options",
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
    "metadataModified": "2024-05-16T09:00:13.637Z",
    "releaseVersion": "130"
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
        "id": "uk-only",
        "label": "Geography",
        "name": "geography"
      },
      {
        "id": "dd-mm",
        "label": "Day/month",
        "name": "daymonth"
      },
      {
        "id": "spend-category",
        "label": "Category",
        "name": "category"
      }
    ],
    "edition": "time-series",
    "id": "uk-spending-on-cards",
    "metadata": {
      "description": "These data series are experimental faster indicators for monitoring UK spending using debit and credit cards.",
      "last_updated": "2024-05-16T09:00:13.637Z",
      "next_release": "To be announced",
      "release_date": "2024-05-16T00:00:00.000Z",
      "release_frequency": "Weekly",
      "state": "published",
      "title": "UK spending on credit and debit cards",
      "type": "filterable"
    },
    "metadataContract": {
      "catalogueType": "filterable",
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "time-series",
        "id": "uk-spending-on-cards",
        "version": 130
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:30:28.236811Z",
      "sha256": "db97e5590d6540bd9d270e7597a4ca7aa0ab5e893d7d5666d122f57a272161f7",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/uk-spending-on-cards/editions/time-series/versions/130/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "bounds": {
        "basis": "published time-dimension option codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": "2024",
        "minimumNative": "2020",
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
        }
      ],
      "reportedTotal": 5,
      "retrievedUnique": 5,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "130",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/uk-spending-on-cards/editions/time-series/versions/130"
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-W"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2024",
      "minimumNative": "2020",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# UK spending on credit and debit cards

These data series are experimental faster indicators for monitoring UK spending using debit and credit cards.

Native identifier: `uk-spending-on-cards`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/uk-spending-on-cards/editions/time-series/versions/130)

Update cadence: Weekly.
Temporal evidence: normalised-source-options (available-native-period-options); start 2020, end 2024.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
