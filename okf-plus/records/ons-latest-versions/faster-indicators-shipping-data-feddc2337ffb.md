---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/faster-indicators-shipping-data",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Coronavirus and the latest indicators for the UK economy and society: Shipping indicators",
  "description": "These shipping indicators are based on counts of all vessels, and cargo and tanker vessels. As discussed in Faster indicators of UK economic activity: shipping (please see the related links), we expect the shipping indicators to be related to the import and export of goods.",
  "nativeIdentifier": "faster-indicators-shipping-data",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/faster-indicators-shipping-data/editions/2023-time-series/versions/75",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/faster-indicators-shipping-data/editions/2023-time-series/versions/75/metadata",
      "retrievedAt": "2026-10-02T01:31:19.631136Z",
      "responseSha256": "c20899e6da98c0d676ae627ee5854fc4490dacd4f88ba30a185ea807a65168a8",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/37",
      "normalisedRecordSha256": "ab286e1f196690013aca946ca6a286e69bfe670d8ff7c7cd15ff5ac3a29da133",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/faster-indicators-shipping-data/editions/2023-time-series/versions/75"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2018",
    "end": "2025",
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
    "nextRelease": "TBA",
    "metadataModified": "2025-12-04T10:37:02.61Z",
    "releaseVersion": "75"
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
        "label": "time",
        "name": "time"
      },
      {
        "id": "uk-only",
        "label": "geography",
        "name": "geography"
      },
      {
        "id": "week-number",
        "label": "week",
        "name": "week"
      },
      {
        "id": "shipping-port",
        "label": "port",
        "name": "port"
      },
      {
        "id": "ship-and-visit-type",
        "label": "shipandvisittype",
        "name": "shipandvisittype"
      }
    ],
    "edition": "2023-time-series",
    "id": "faster-indicators-shipping-data",
    "metadata": {
      "description": "These shipping indicators are based on counts of all vessels, and cargo and tanker vessels. As discussed in Faster indicators of UK economic activity: shipping (please see the related links), we expect the shipping indicators to be related to the import and export of goods.",
      "last_updated": "2025-12-04T10:37:02.61Z",
      "next_release": "TBA",
      "release_date": "2025-12-04T00:00:00.000Z",
      "release_frequency": "Weekly",
      "state": "published",
      "title": "Coronavirus and the latest indicators for the UK economy and society: Shipping indicators"
    },
    "metadataContract": {
      "catalogueType": null,
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "2023-time-series",
        "id": "faster-indicators-shipping-data",
        "version": 75
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:31:19.631136Z",
      "sha256": "c20899e6da98c0d676ae627ee5854fc4490dacd4f88ba30a185ea807a65168a8",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/faster-indicators-shipping-data/editions/2023-time-series/versions/75/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "bounds": {
        "basis": "published time-dimension option codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": "2025",
        "minimumNative": "2018",
        "status": "known-option-extrema"
      },
      "complete": true,
      "duplicateCount": 0,
      "options": [
        {
          "dimension": "time",
          "label": "2025",
          "option": "2025"
        },
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
        }
      ],
      "reportedTotal": 8,
      "retrievedUnique": 8,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "75",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/faster-indicators-shipping-data/editions/2023-time-series/versions/75"
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
      "maximumNative": "2025",
      "minimumNative": "2018",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Coronavirus and the latest indicators for the UK economy and society: Shipping indicators

These shipping indicators are based on counts of all vessels, and cargo and tanker vessels. As discussed in Faster indicators of UK economic activity: shipping (please see the related links), we expect the shipping indicators to be related to the import and export of goods.

Native identifier: `faster-indicators-shipping-data`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/faster-indicators-shipping-data/editions/2023-time-series/versions/75)

Update cadence: Weekly.
Temporal evidence: normalised-source-options (available-native-period-options); start 2018, end 2025.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
