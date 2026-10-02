---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/regional-gdp-by-quarter",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Quarterly GDP for England, Wales and the English regions",
  "description": "Quarterly economic activity within England, Wales and the nine English regions (North East, North West, Yorkshire and The Humber, East Midlands, West Midlands, East of England, London, South East, South West).",
  "nativeIdentifier": "regional-gdp-by-quarter",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-quarter",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "regional GDP"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/19",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/19",
      "normalisedRecordSha256": "cb2aeceadab1b6d3b2006487480fffac7c3aa3baec6a7718c1d014dda0d790a8",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-quarter/editions/time-series/versions/6/metadata",
      "retrievedAt": "2026-10-02T01:30:49.372047Z",
      "responseSha256": "1b37f2847d24d26c385d8f6b569d4ea66dcf807dffdba7d99b29149d3e17bf27",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/19",
      "normalisedRecordSha256": "41ac0e93a4764bffffcb4f66bfc0576eb08e256b5b3a6f406b7097d1795b9806",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-quarter"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "not-evidenced",
    "kind": "dataset-reference-period",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "No supported reference-period extent in captured metadata; release and catalogue dates are separate."
  },
  "update": {
    "frequency": {
      "status": "source-stated",
      "label": "To be announced",
      "iri": null,
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "To be announced",
    "metadataModified": "2023-05-24T08:36:17.711Z",
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
    "description": "Quarterly economic activity within England, Wales and the nine English regions (North East, North West, Yorkshire and The Humber, East Midlands, West Midlands, East of England, London, South East, South West).",
    "id": "regional-gdp-by-quarter",
    "keywords": [
      "regional GDP"
    ],
    "last_updated": "2023-05-24T08:36:17.711Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-quarter/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-quarter/editions/time-series/versions/6",
        "id": "6"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-quarter"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/economy/grossdomesticproductgdp"
      }
    },
    "national_statistic": false,
    "next_release": "To be announced",
    "qmi": {
      "href": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/methodologies/grossdomesticproductgdpukregionsandcountriesqmi"
    },
    "release_frequency": "To be announced",
    "state": "published",
    "title": "Quarterly GDP for England, Wales and the English regions",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "yyyy-qq",
          "label": "Time",
          "name": "time"
        },
        {
          "id": "nuts",
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
          "label": "Prices",
          "name": "prices"
        },
        {
          "id": "quarterly-index-and-growth-rate",
          "label": "Measure",
          "name": "growthrate"
        }
      ],
      "edition": "time-series",
      "id": "regional-gdp-by-quarter",
      "metadata": {
        "description": "Quarterly economic activity within England, Wales and the nine English regions (North East, North West, Yorkshire and The Humber, East Midlands, West Midlands, East of England, London, South East, South West).",
        "last_updated": "2023-05-24T08:36:17.711Z",
        "next_release": "To be announced",
        "release_date": "2023-05-18T00:00:00.000Z",
        "release_frequency": "To be announced",
        "state": "published",
        "title": "Quarterly GDP for England, Wales and the English regions"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "regional-gdp-by-quarter",
          "version": 6
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:30:49.372047Z",
        "sha256": "1b37f2847d24d26c385d8f6b569d4ea66dcf807dffdba7d99b29149d3e17bf27",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-quarter/editions/time-series/versions/6/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "continuityEstablished": false,
          "maximumNative": null,
          "minimumNative": null,
          "status": "unknown-unrecognised-or-mixed-period-codes"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "2022 Q3",
            "option": "2022-q3"
          },
          {
            "dimension": "time",
            "label": "2022 Q2",
            "option": "2022-q2"
          },
          {
            "dimension": "time",
            "label": "2022 Q1",
            "option": "2022-q1"
          },
          {
            "dimension": "time",
            "label": "2021 Q4",
            "option": "2021-q4"
          },
          {
            "dimension": "time",
            "label": "2021 Q3",
            "option": "2021-q3"
          },
          {
            "dimension": "time",
            "label": "2021 Q2",
            "option": "2021-q2"
          },
          {
            "dimension": "time",
            "label": "2021 Q1",
            "option": "2021-q1"
          },
          {
            "dimension": "time",
            "label": "2020 Q4",
            "option": "2020-q4"
          },
          {
            "dimension": "time",
            "label": "2020 Q3",
            "option": "2020-q3"
          },
          {
            "dimension": "time",
            "label": "2020 Q2",
            "option": "2020-q2"
          },
          {
            "dimension": "time",
            "label": "2020 Q1",
            "option": "2020-q1"
          },
          {
            "dimension": "time",
            "label": "2019 Q4",
            "option": "2019-q4"
          },
          {
            "dimension": "time",
            "label": "2019 Q3",
            "option": "2019-q3"
          },
          {
            "dimension": "time",
            "label": "2019 Q2",
            "option": "2019-q2"
          },
          {
            "dimension": "time",
            "label": "2019 Q1",
            "option": "2019-q1"
          },
          {
            "dimension": "time",
            "label": "2018 Q4",
            "option": "2018-q4"
          },
          {
            "dimension": "time",
            "label": "2018 Q3",
            "option": "2018-q3"
          },
          {
            "dimension": "time",
            "label": "2018 Q2",
            "option": "2018-q2"
          },
          {
            "dimension": "time",
            "label": "2018 Q1",
            "option": "2018-q1"
          },
          {
            "dimension": "time",
            "label": "2017 Q4",
            "option": "2017-q4"
          },
          {
            "dimension": "time",
            "label": "2017 Q3",
            "option": "2017-q3"
          },
          {
            "dimension": "time",
            "label": "2017 Q2",
            "option": "2017-q2"
          },
          {
            "dimension": "time",
            "label": "2017 Q1",
            "option": "2017-q1"
          },
          {
            "dimension": "time",
            "label": "2016 Q4",
            "option": "2016-q4"
          },
          {
            "dimension": "time",
            "label": "2016 Q3",
            "option": "2016-q3"
          },
          {
            "dimension": "time",
            "label": "2016 Q2",
            "option": "2016-q2"
          },
          {
            "dimension": "time",
            "label": "2016 Q1",
            "option": "2016-q1"
          },
          {
            "dimension": "time",
            "label": "2015 Q4",
            "option": "2015-q4"
          },
          {
            "dimension": "time",
            "label": "2015 Q3",
            "option": "2015-q3"
          },
          {
            "dimension": "time",
            "label": "2015 Q2",
            "option": "2015-q2"
          },
          {
            "dimension": "time",
            "label": "2015 Q1",
            "option": "2015-q1"
          },
          {
            "dimension": "time",
            "label": "2014 Q4",
            "option": "2014-q4"
          },
          {
            "dimension": "time",
            "label": "2014 Q3",
            "option": "2014-q3"
          },
          {
            "dimension": "time",
            "label": "2014 Q2",
            "option": "2014-q2"
          },
          {
            "dimension": "time",
            "label": "2014 Q1",
            "option": "2014-q1"
          },
          {
            "dimension": "time",
            "label": "2013 Q4",
            "option": "2013-q4"
          },
          {
            "dimension": "time",
            "label": "2013 Q3",
            "option": "2013-q3"
          },
          {
            "dimension": "time",
            "label": "2013 Q2",
            "option": "2013-q2"
          },
          {
            "dimension": "time",
            "label": "2013 Q1",
            "option": "2013-q1"
          },
          {
            "dimension": "time",
            "label": "2012 Q4",
            "option": "2012-q4"
          },
          {
            "dimension": "time",
            "label": "2012 Q3",
            "option": "2012-q3"
          },
          {
            "dimension": "time",
            "label": "2012 Q2",
            "option": "2012-q2"
          },
          {
            "dimension": "time",
            "label": "2012 Q1",
            "option": "2012-q1"
          }
        ],
        "reportedTotal": 43,
        "retrievedUnique": 43,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "6",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-quarter/editions/time-series/versions/6"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@type": "dcterms:Frequency",
    "rdfs:label": "To be announced"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-quarter/editions"
  }
}
---

# Quarterly GDP for England, Wales and the English regions

Quarterly economic activity within England, Wales and the nine English regions (North East, North West, Yorkshire and The Humber, East Midlands, West Midlands, East of England, London, South East, South West).

Native identifier: `regional-gdp-by-quarter`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/regional-gdp-by-quarter)

Update cadence: To be announced.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
