---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/gdp-by-local-authority",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "GDP by local authority",
  "description": "Gross domestic product (GDP) in current market prices and as chained volume measures, plus GDP per capita, for each local authority district, metropolitan district, London borough and Scottish Council area in the UK.",
  "nativeIdentifier": "gdp-by-local-authority",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/gdp-by-local-authority",
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
      "sourcePointer": "/items/36",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/36",
      "normalisedRecordSha256": "67deb8a233313afc21aa8a1201767aafe6316a40a02a0dc0da5620e83c137cf0",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/gdp-by-local-authority/editions/time-series/versions/2/metadata",
      "retrievedAt": "2026-10-02T01:31:17.966165Z",
      "responseSha256": "b513019af4ec93dcb6fa78e6a13515c45345e3a5f1b5dfc5fd5bb17d03845c62",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/36",
      "normalisedRecordSha256": "e6cf4c055b1c44f270038c5db5d98efee1e939f501daa1aac2efd2a19f43b67c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/gdp-by-local-authority"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "1998",
    "end": "2019",
    "sourceField": "timeMetadata.temporal.options",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "year",
    "derivation": "ONS-native-ISO-period-code.v1"
  },
  "update": {
    "frequency": {
      "status": "not-evidenced",
      "label": null,
      "iri": null,
      "sourceField": null
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "TBA",
    "metadataModified": "2021-06-25T05:49:50.245Z",
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
    "description": "Gross domestic product (GDP) in current market prices and as chained volume measures, plus GDP per capita, for each local authority district, metropolitan district, London borough and Scottish Council area in the UK.",
    "id": "gdp-by-local-authority",
    "last_updated": "2021-06-25T05:49:50.245Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/gdp-by-local-authority/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/gdp-by-local-authority/editions/time-series/versions/2",
        "id": "2"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/gdp-by-local-authority"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/economy/grossdomesticproductgdp"
      }
    },
    "next_release": "TBA",
    "qmi": {
      "href": "https://www.ons.gov.uk/economy/regionalaccounts/grossdisposablehouseholdincome/methodologies/regionalaccounts"
    },
    "state": "published",
    "title": "GDP by local authority",
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
          "id": "type-of-prices",
          "label": "Variables",
          "name": "prices"
        }
      ],
      "edition": "time-series",
      "id": "gdp-by-local-authority",
      "metadata": {
        "description": "Gross domestic product (GDP) in current market prices and as chained volume measures, plus GDP per capita, for each local authority district, metropolitan district, London borough and Scottish Council area in the UK.",
        "last_updated": "2021-06-25T05:49:50.245Z",
        "next_release": "TBA",
        "release_date": "2021-06-24T00:00:00.000Z",
        "state": "published",
        "title": "GDP by local authority",
        "type": "filterable"
      },
      "metadataContract": {
        "catalogueType": "filterable",
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "gdp-by-local-authority",
          "version": 2
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:31:17.966165Z",
        "sha256": "b513019af4ec93dcb6fa78e6a13515c45345e3a5f1b5dfc5fd5bb17d03845c62",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/gdp-by-local-authority/editions/time-series/versions/2/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2019",
          "minimumNative": "1998",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
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
          },
          {
            "dimension": "time",
            "label": "2010",
            "option": "2010"
          },
          {
            "dimension": "time",
            "label": "2009",
            "option": "2009"
          },
          {
            "dimension": "time",
            "label": "2008",
            "option": "2008"
          },
          {
            "dimension": "time",
            "label": "2007",
            "option": "2007"
          },
          {
            "dimension": "time",
            "label": "2006",
            "option": "2006"
          },
          {
            "dimension": "time",
            "label": "2005",
            "option": "2005"
          },
          {
            "dimension": "time",
            "label": "2004",
            "option": "2004"
          },
          {
            "dimension": "time",
            "label": "2003",
            "option": "2003"
          },
          {
            "dimension": "time",
            "label": "2002",
            "option": "2002"
          },
          {
            "dimension": "time",
            "label": "2001",
            "option": "2001"
          },
          {
            "dimension": "time",
            "label": "2000",
            "option": "2000"
          },
          {
            "dimension": "time",
            "label": "1999",
            "option": "1999"
          },
          {
            "dimension": "time",
            "label": "1998",
            "option": "1998"
          }
        ],
        "reportedTotal": 22,
        "retrievedUnique": 22,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "2",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/gdp-by-local-authority/editions/time-series/versions/2"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/gdp-by-local-authority/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2019",
      "minimumNative": "1998",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# GDP by local authority

Gross domestic product (GDP) in current market prices and as chained volume measures, plus GDP per capita, for each local authority district, metropolitan district, London borough and Scottish Council area in the UK.

Native identifier: `gdp-by-local-authority`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/gdp-by-local-authority)

Update cadence: not evidenced in captured metadata.
Temporal evidence: normalised-source-options (available-native-period-options); start 1998, end 2019.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
