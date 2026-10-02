---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/sexual-orientation-by-region",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Sexual orientation by English regions and UK countries",
  "description": "Sexual orientation in the UK from 2012 to 2020 by region. Data source: Annual Population Survey, ONS",
  "nativeIdentifier": "sexual-orientation-by-region",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-region",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "gay",
    "lesbian,bisexual,straight,LGB"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/13",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/13",
      "normalisedRecordSha256": "a999e34c0bd6b6f9076e754769930585400658e378191ac4f7a7841af7972d12",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-region/editions/time-series/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:30:39.129930Z",
      "responseSha256": "9af4b0fd686c842cd3708146c0fbe558ed95e15abab8107c8163aaccc656a1a1",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/13",
      "normalisedRecordSha256": "56cc618575dbc5bcb81beb435644a03b9b273d209df9f0e21c3d791c8668965c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-region"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2012",
    "end": "2022",
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
    "metadataModified": "2023-10-18T09:27:23.046Z",
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
    "description": "Sexual orientation in the UK from 2012 to 2020 by region.\n\nData source: Annual Population Survey, ONS\n",
    "id": "sexual-orientation-by-region",
    "keywords": [
      "gay",
      "lesbian,bisexual,straight,LGB"
    ],
    "last_updated": "2023-10-18T09:27:23.046Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-region/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-region/editions/time-series/versions/3",
        "id": "3"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-region"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/culturalidentity/sexuality"
      }
    },
    "national_statistic": false,
    "next_release": "To be announced",
    "qmi": {
      "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/sexuality/methodologies/sexualidentityukqmi"
    },
    "related_datasets": [
      {
        "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/sexuality/datasets/sexualidentityuk",
        "title": "Sexual orientation, UK, dataset"
      }
    ],
    "release_frequency": "Annual",
    "state": "published",
    "title": "Sexual orientation by English regions and UK countries",
    "type": "filterable",
    "unit_of_measure": "Number of people (thousands) and percentage",
    "timeMetadata": {
      "dimensions": [
        {
          "description": "Estimates of sexual orientation by region for 2012 and 2013 are available for Northern Ireland only",
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
          "id": "sexual-orientation",
          "label": "Sexual orientation",
          "name": "sexualorientation"
        },
        {
          "description": "Percentages are calculated out of all people aged 16 and over within a region within a particular year. For example, 1.3% of people aged 16 and over in the North East in 2019 identified as gay or lesbian. The percentages of each sexual orientation response category within a region within a particular year will add up to 100% (subject to rounding).",
          "id": "unit-of-measure",
          "label": "Unit of measure",
          "name": "unitofmeasure"
        }
      ],
      "edition": "time-series",
      "id": "sexual-orientation-by-region",
      "metadata": {
        "description": "Sexual orientation in the UK from 2012 to 2020 by region. Data source: Annual Population Survey, ONS",
        "last_updated": "2023-10-18T09:27:23.046Z",
        "next_release": "To be announced",
        "release_date": "2023-10-18T00:00:00.000Z",
        "release_frequency": "Annual",
        "state": "published",
        "title": "Sexual orientation by English regions and UK countries",
        "type": "filterable",
        "unit_of_measure": "Number of people (thousands) and percentage"
      },
      "metadataContract": {
        "catalogueType": "filterable",
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "sexual-orientation-by-region",
          "version": 3
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:30:39.129930Z",
        "sha256": "9af4b0fd686c842cd3708146c0fbe558ed95e15abab8107c8163aaccc656a1a1",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-region/editions/time-series/versions/3/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2022",
          "minimumNative": "2012",
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
          }
        ],
        "reportedTotal": 11,
        "retrievedUnique": 11,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "3",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-region/editions/time-series/versions/3"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-region/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2022",
      "minimumNative": "2012",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Sexual orientation by English regions and UK countries

Sexual orientation in the UK from 2012 to 2020 by region. Data source: Annual Population Survey, ONS

Native identifier: `sexual-orientation-by-region`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/sexual-orientation-by-region)

Update cadence: Annual.
Temporal evidence: normalised-source-options (available-native-period-options); start 2012, end 2022.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
