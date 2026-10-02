---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/gva-by-industry-by-local-authority",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "GVA by industry by local authority",
  "description": "Gross value added (balanced) in current basic prices and as chained volume measures, with a breakdown by 24 industry sectors, for each local authority district, metropolitan district, London borough and Scottish Council area in the UK.",
  "nativeIdentifier": "gva-by-industry-by-local-authority",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/gva-by-industry-by-local-authority",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/33",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/33",
      "normalisedRecordSha256": "27938537005e9b505c3d4001b4dbdc76d19c2a1ef5f2a2a7d6adb0075668c2eb",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/gva-by-industry-by-local-authority/editions/time-series/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:31:12.905416Z",
      "responseSha256": "9247898ba65660372a1446127d0eb4aaf5aa45a426717def900c3cddd5bf5916",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/33",
      "normalisedRecordSha256": "604b7b6cdf45357fbbeb1dc9b27cf9304fde9e05034a7fe29c7db0e7936f7dc9",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/gva-by-industry-by-local-authority"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "1998",
    "end": "2018",
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
    "nextRelease": "TBA",
    "metadataModified": "2021-02-18T09:40:22.499Z",
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
    "description": "Gross value added (balanced) in current basic prices and as chained volume measures, with a breakdown by 24 industry sectors, for each local authority district, metropolitan district, London borough and Scottish Council area in the UK.",
    "id": "gva-by-industry-by-local-authority",
    "last_updated": "2021-02-18T09:40:22.499Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/gva-by-industry-by-local-authority/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/gva-by-industry-by-local-authority/editions/time-series/versions/1",
        "id": "1"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/gva-by-industry-by-local-authority"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/economy/grossvalueaddedgva"
      }
    },
    "next_release": "TBA",
    "qmi": {
      "href": "https://www.ons.gov.uk/economy/regionalaccounts/grossdisposablehouseholdincome/methodologies/regionalaccounts"
    },
    "release_frequency": "Annual",
    "state": "published",
    "title": "GVA by industry by local authority",
    "type": "filterable",
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
          "id": "sic-unofficial",
          "label": "Standard Industrial Classification",
          "name": "unofficialstandardindustrialclassification"
        },
        {
          "id": "type-of-prices",
          "label": "Variables",
          "name": "prices"
        }
      ],
      "edition": "time-series",
      "id": "gva-by-industry-by-local-authority",
      "metadata": {
        "description": "Gross value added (balanced) in current basic prices and as chained volume measures, with a breakdown by 24 industry sectors, for each local authority district, metropolitan district, London borough and Scottish Council area in the UK.",
        "last_updated": "2021-02-18T09:40:22.499Z",
        "next_release": "TBA",
        "release_date": "2021-01-11T00:00:00.000Z",
        "release_frequency": "Annual",
        "state": "published",
        "title": "GVA by industry by local authority",
        "type": "filterable"
      },
      "metadataContract": {
        "catalogueType": "filterable",
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "gva-by-industry-by-local-authority",
          "version": 1
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:31:12.905416Z",
        "sha256": "9247898ba65660372a1446127d0eb4aaf5aa45a426717def900c3cddd5bf5916",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/gva-by-industry-by-local-authority/editions/time-series/versions/1/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2018",
          "minimumNative": "1998",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "1998",
            "option": "1998"
          },
          {
            "dimension": "time",
            "label": "1999",
            "option": "1999"
          },
          {
            "dimension": "time",
            "label": "2000",
            "option": "2000"
          },
          {
            "dimension": "time",
            "label": "2001",
            "option": "2001"
          },
          {
            "dimension": "time",
            "label": "2002",
            "option": "2002"
          },
          {
            "dimension": "time",
            "label": "2003",
            "option": "2003"
          },
          {
            "dimension": "time",
            "label": "2004",
            "option": "2004"
          },
          {
            "dimension": "time",
            "label": "2005",
            "option": "2005"
          },
          {
            "dimension": "time",
            "label": "2006",
            "option": "2006"
          },
          {
            "dimension": "time",
            "label": "2007",
            "option": "2007"
          },
          {
            "dimension": "time",
            "label": "2008",
            "option": "2008"
          },
          {
            "dimension": "time",
            "label": "2009",
            "option": "2009"
          },
          {
            "dimension": "time",
            "label": "2010",
            "option": "2010"
          },
          {
            "dimension": "time",
            "label": "2011",
            "option": "2011"
          },
          {
            "dimension": "time",
            "label": "2012",
            "option": "2012"
          },
          {
            "dimension": "time",
            "label": "2013",
            "option": "2013"
          },
          {
            "dimension": "time",
            "label": "2014",
            "option": "2014"
          },
          {
            "dimension": "time",
            "label": "2015",
            "option": "2015"
          },
          {
            "dimension": "time",
            "label": "2016",
            "option": "2016"
          },
          {
            "dimension": "time",
            "label": "2017",
            "option": "2017"
          },
          {
            "dimension": "time",
            "label": "2018",
            "option": "2018"
          }
        ],
        "reportedTotal": 21,
        "retrievedUnique": 21,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "1",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/gva-by-industry-by-local-authority/editions/time-series/versions/1"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/gva-by-industry-by-local-authority/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2018",
      "minimumNative": "1998",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# GVA by industry by local authority

Gross value added (balanced) in current basic prices and as chained volume measures, with a breakdown by 24 industry sectors, for each local authority district, metropolitan district, London borough and Scottish Council area in the UK.

Native identifier: `gva-by-industry-by-local-authority`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/gva-by-industry-by-local-authority)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 1998, end 2018.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
