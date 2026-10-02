---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/health-accounts",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Expenditure on healthcare: UK Health Accounts",
  "description": "Healthcare expenditure statistics, produced to the international definitions of the System of Health Accounts 2011. Subcategories may not sum to aggregates due to rounding.",
  "nativeIdentifier": "health-accounts",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/health-accounts",
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
      "sourcePointer": "/items/32",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/32",
      "normalisedRecordSha256": "e68e13a741761282fee51f76bc55e4e4e33a3b2523952af21316fff831c3d2fe",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/health-accounts/editions/time-series/versions/2/metadata",
      "retrievedAt": "2026-10-02T01:31:11.236960Z",
      "responseSha256": "95384a564557a59b1e2f0641f4638ff39d8cb6580ffc0af0fd2c8b95b9bc763a",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/32",
      "normalisedRecordSha256": "799b34407a94f41b4ea7b7ec42c30a7d89316962f4276dcff9c817d450f53907",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/health-accounts"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2013",
    "end": "2019",
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
    "metadataModified": "2021-07-23T09:18:21.763Z",
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
    "description": "Healthcare expenditure statistics, produced to the international definitions of the System of Health Accounts 2011.\n\nSubcategories may not sum to aggregates due to rounding.",
    "id": "health-accounts",
    "last_updated": "2021-07-23T09:18:21.763Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/health-accounts/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/health-accounts/editions/time-series/versions/2",
        "id": "2"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/health-accounts"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/healthandsocialcare/healthcaresystem"
      }
    },
    "methodologies": [
      {
        "href": "http://www.oecd.org/els/health-systems/a-system-of-health-accounts-2011-9789264270985-en.htm",
        "title": "International Classification of Health Accounts (ICHA) codes"
      }
    ],
    "next_release": "To be announced",
    "qmi": {
      "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthcaresystem/methodologies/ukhealthaccountsqmi"
    },
    "related_datasets": [
      {
        "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthcaresystem/datasets/healthaccountsreferencetables",
        "title": "UK Health Accounts reference tables"
      }
    ],
    "release_frequency": "Annual",
    "state": "published",
    "title": "Expenditure on healthcare: UK Health Accounts",
    "timeMetadata": {
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
          "description": "Figures provided in real terms are are adjusted for inflation and presented in 2019 prices. The GDP deflator (series: IHYS) [data released 31st March 2021] was used to deflate current price expenditure.",
          "id": "type-of-prices",
          "label": "Prices",
          "name": "prices"
        },
        {
          "id": "healthcare-financing-scheme",
          "label": "Financing scheme",
          "name": "financingscheme"
        },
        {
          "id": "healthcare-provider",
          "label": "Healthcare provider",
          "name": "healthcareprovider"
        },
        {
          "id": "healthcare-function",
          "label": "Healthcare function",
          "name": "healthcarefunction"
        }
      ],
      "edition": "time-series",
      "id": "health-accounts",
      "metadata": {
        "description": "Healthcare expenditure statistics, produced to the international definitions of the System of Health Accounts 2011. Subcategories may not sum to aggregates due to rounding.",
        "last_updated": "2021-07-23T09:18:21.763Z",
        "next_release": "To be announced",
        "release_date": "2021-07-16T00:00:00.000Z",
        "release_frequency": "Annual",
        "state": "published",
        "title": "Expenditure on healthcare: UK Health Accounts"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "health-accounts",
          "version": 2
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:31:11.236960Z",
        "sha256": "95384a564557a59b1e2f0641f4638ff39d8cb6580ffc0af0fd2c8b95b9bc763a",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/health-accounts/editions/time-series/versions/2/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2019",
          "minimumNative": "2013",
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
          }
        ],
        "reportedTotal": 7,
        "retrievedUnique": 7,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "2",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/health-accounts/editions/time-series/versions/2"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/health-accounts/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2019",
      "minimumNative": "2013",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Expenditure on healthcare: UK Health Accounts

Healthcare expenditure statistics, produced to the international definitions of the System of Health Accounts 2011. Subcategories may not sum to aggregates due to rounding.

Native identifier: `health-accounts`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/health-accounts)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2013, end 2019.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
