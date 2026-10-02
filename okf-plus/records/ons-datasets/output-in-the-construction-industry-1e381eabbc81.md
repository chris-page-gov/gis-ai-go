---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/output-in-the-construction-industry",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Output in the construction industry",
  "description": "Monthly construction output for Great Britain at current price and chained volume measures, seasonally adjusted by public and private sector.",
  "nativeIdentifier": "output-in-the-construction-industry",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/output-in-the-construction-industry",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "infrastructure",
    "public housing,private housing,non–housing,repairs and maintenance"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/22",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/22",
      "normalisedRecordSha256": "f812c0f6fceeb661ec3b6cb823823d4b2f7ddb8da2a04ac1f0a53660cd9a1670",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/output-in-the-construction-industry/editions/time-series/versions/54/metadata",
      "retrievedAt": "2026-10-02T01:30:54.402752Z",
      "responseSha256": "bf5685566dd355e5a854a20b61a4098aa199e31d8fcbc3a8a1be554301ab8f58",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/22",
      "normalisedRecordSha256": "09efbc09facff11a0a0ccf97132f061c805556994c7d5f5391d88d56375a859a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/output-in-the-construction-industry"
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
      "label": "Monthly",
      "iri": "http://purl.org/linked-data/sdmx/2009/code#freq-M",
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "14 May 2026",
    "metadataModified": "2026-05-14T09:22:31.747Z",
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
    "description": "Monthly construction output for Great Britain at current price and chained volume measures, seasonally adjusted by public and private sector.",
    "id": "output-in-the-construction-industry",
    "keywords": [
      "infrastructure",
      "public housing,private housing,non–housing,repairs and maintenance"
    ],
    "last_updated": "2026-05-14T09:22:31.747Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/output-in-the-construction-industry/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/output-in-the-construction-industry/editions/time-series/versions/54",
        "id": "54"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/output-in-the-construction-industry"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/businessindustryandtrade/constructionindustry"
      }
    },
    "national_statistic": true,
    "next_release": "14 May 2026",
    "qmi": {
      "href": "https://www.ons.gov.uk/businessindustryandtrade/constructionindustry/qmis/constructionoutputqmi"
    },
    "release_frequency": "Monthly",
    "state": "published",
    "title": "Output in the construction industry",
    "type": "filterable",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "years-quarters-months",
          "label": "Time",
          "name": "time"
        },
        {
          "id": "administrative-geography",
          "label": "Geography",
          "name": "geography"
        },
        {
          "id": "seasonal-adjustment",
          "label": "Seasonal adjustment",
          "name": "seasonaladjustment"
        },
        {
          "id": "construction-series-type",
          "label": "Series type",
          "name": "seriestype"
        },
        {
          "id": "construction-classifications",
          "label": "Type of work",
          "name": "typeofwork"
        }
      ],
      "edition": "time-series",
      "id": "output-in-the-construction-industry",
      "metadata": {
        "description": "Monthly construction output for Great Britain at current price and chained volume measures, seasonally adjusted by public and private sector.",
        "last_updated": "2026-05-14T09:22:31.747Z",
        "next_release": "14 May 2026",
        "release_date": "2026-05-14T00:00:00.000Z",
        "release_frequency": "Monthly",
        "state": "published",
        "title": "Output in the construction industry",
        "type": "filterable"
      },
      "metadataContract": {
        "catalogueType": "filterable",
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "output-in-the-construction-industry",
          "version": 54
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:30:54.402752Z",
        "sha256": "bf5685566dd355e5a854a20b61a4098aa199e31d8fcbc3a8a1be554301ab8f58",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/output-in-the-construction-industry/editions/time-series/versions/54/metadata"
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
            "label": "2026 - Q1",
            "option": "2026-q1"
          },
          {
            "dimension": "time",
            "label": "2026 - Mar",
            "option": "2026-mar"
          },
          {
            "dimension": "time",
            "label": "2026 - Feb",
            "option": "2026-feb"
          },
          {
            "dimension": "time",
            "label": "2026 - Jan",
            "option": "2026-jan"
          },
          {
            "dimension": "time",
            "label": "2025",
            "option": "2025"
          },
          {
            "dimension": "time",
            "label": "2025 - Q4",
            "option": "2025-q4"
          },
          {
            "dimension": "time",
            "label": "2025 - Q3",
            "option": "2025-q3"
          },
          {
            "dimension": "time",
            "label": "2025 - Q2",
            "option": "2025-q2"
          },
          {
            "dimension": "time",
            "label": "2025 - Q1",
            "option": "2025-q1"
          },
          {
            "dimension": "time",
            "label": "2025 - Dec",
            "option": "2025-dec"
          },
          {
            "dimension": "time",
            "label": "2025 - Nov",
            "option": "2025-nov"
          },
          {
            "dimension": "time",
            "label": "2025 - Oct",
            "option": "2025-oct"
          },
          {
            "dimension": "time",
            "label": "2025 - Sep",
            "option": "2025-sep"
          },
          {
            "dimension": "time",
            "label": "2025 - Aug",
            "option": "2025-aug"
          },
          {
            "dimension": "time",
            "label": "2025 - Jul",
            "option": "2025-jul"
          },
          {
            "dimension": "time",
            "label": "2025 - Jun",
            "option": "2025-jun"
          },
          {
            "dimension": "time",
            "label": "2025 - May",
            "option": "2025-may"
          },
          {
            "dimension": "time",
            "label": "2025 - Apr",
            "option": "2025-apr"
          },
          {
            "dimension": "time",
            "label": "2025 - Mar",
            "option": "2025-mar"
          },
          {
            "dimension": "time",
            "label": "2025 - Feb",
            "option": "2025-feb"
          },
          {
            "dimension": "time",
            "label": "2025 - Jan",
            "option": "2025-jan"
          },
          {
            "dimension": "time",
            "label": "2024",
            "option": "2024"
          },
          {
            "dimension": "time",
            "label": "2024 - Q4",
            "option": "2024-q4"
          },
          {
            "dimension": "time",
            "label": "2024 - Q3",
            "option": "2024-q3"
          },
          {
            "dimension": "time",
            "label": "2024 - Q2",
            "option": "2024-q2"
          },
          {
            "dimension": "time",
            "label": "2024 - Q1",
            "option": "2024-q1"
          },
          {
            "dimension": "time",
            "label": "2024 - Dec",
            "option": "2024-dec"
          },
          {
            "dimension": "time",
            "label": "2024 - Nov",
            "option": "2024-nov"
          },
          {
            "dimension": "time",
            "label": "2024 - Oct",
            "option": "2024-oct"
          },
          {
            "dimension": "time",
            "label": "2024 - Sep",
            "option": "2024-sep"
          },
          {
            "dimension": "time",
            "label": "2024 - Aug",
            "option": "2024-aug"
          },
          {
            "dimension": "time",
            "label": "2024 - Jul",
            "option": "2024-jul"
          },
          {
            "dimension": "time",
            "label": "2024 - Jun",
            "option": "2024-jun"
          },
          {
            "dimension": "time",
            "label": "2024 - May",
            "option": "2024-may"
          },
          {
            "dimension": "time",
            "label": "2024 - Apr",
            "option": "2024-apr"
          },
          {
            "dimension": "time",
            "label": "2024 - Mar",
            "option": "2024-mar"
          },
          {
            "dimension": "time",
            "label": "2024 - Feb",
            "option": "2024-feb"
          },
          {
            "dimension": "time",
            "label": "2024 - Jan",
            "option": "2024-jan"
          },
          {
            "dimension": "time",
            "label": "2023",
            "option": "2023"
          },
          {
            "dimension": "time",
            "label": "2023 - Q4",
            "option": "2023-q4"
          },
          {
            "dimension": "time",
            "label": "2023 - Q3",
            "option": "2023-q3"
          },
          {
            "dimension": "time",
            "label": "2023 - Q2",
            "option": "2023-q2"
          },
          {
            "dimension": "time",
            "label": "2023 - Q1",
            "option": "2023-q1"
          },
          {
            "dimension": "time",
            "label": "2023 - Dec",
            "option": "2023-dec"
          },
          {
            "dimension": "time",
            "label": "2023 - Nov",
            "option": "2023-nov"
          },
          {
            "dimension": "time",
            "label": "2023 - Oct",
            "option": "2023-oct"
          },
          {
            "dimension": "time",
            "label": "2023 - Sep",
            "option": "2023-sep"
          },
          {
            "dimension": "time",
            "label": "2023 - Aug",
            "option": "2023-aug"
          },
          {
            "dimension": "time",
            "label": "2023 - Jul",
            "option": "2023-jul"
          },
          {
            "dimension": "time",
            "label": "2023 - Jun",
            "option": "2023-jun"
          },
          {
            "dimension": "time",
            "label": "2023 - May",
            "option": "2023-may"
          },
          {
            "dimension": "time",
            "label": "2023 - Apr",
            "option": "2023-apr"
          },
          {
            "dimension": "time",
            "label": "2023 - Mar",
            "option": "2023-mar"
          },
          {
            "dimension": "time",
            "label": "2023 - Feb",
            "option": "2023-feb"
          },
          {
            "dimension": "time",
            "label": "2023 - Jan",
            "option": "2023-jan"
          },
          {
            "dimension": "time",
            "label": "2022",
            "option": "2022"
          },
          {
            "dimension": "time",
            "label": "2022 - Q4",
            "option": "2022-q4"
          },
          {
            "dimension": "time",
            "label": "2022 - Q3",
            "option": "2022-q3"
          },
          {
            "dimension": "time",
            "label": "2022 - Q2",
            "option": "2022-q2"
          },
          {
            "dimension": "time",
            "label": "2022 - Q1",
            "option": "2022-q1"
          },
          {
            "dimension": "time",
            "label": "2022 - Dec",
            "option": "2022-dec"
          },
          {
            "dimension": "time",
            "label": "2022 - Nov",
            "option": "2022-nov"
          },
          {
            "dimension": "time",
            "label": "2022 - Oct",
            "option": "2022-oct"
          },
          {
            "dimension": "time",
            "label": "2022 - Sep",
            "option": "2022-sep"
          },
          {
            "dimension": "time",
            "label": "2022 - Aug",
            "option": "2022-aug"
          },
          {
            "dimension": "time",
            "label": "2022 - Jul",
            "option": "2022-jul"
          },
          {
            "dimension": "time",
            "label": "2022 - Jun",
            "option": "2022-jun"
          },
          {
            "dimension": "time",
            "label": "2022 - May",
            "option": "2022-may"
          },
          {
            "dimension": "time",
            "label": "2022 - Apr",
            "option": "2022-apr"
          },
          {
            "dimension": "time",
            "label": "2022 - Mar",
            "option": "2022-mar"
          },
          {
            "dimension": "time",
            "label": "2022 - Feb",
            "option": "2022-feb"
          },
          {
            "dimension": "time",
            "label": "2022 - Jan",
            "option": "2022-jan"
          },
          {
            "dimension": "time",
            "label": "2021",
            "option": "2021"
          },
          {
            "dimension": "time",
            "label": "2021 - Q4",
            "option": "2021-q4"
          },
          {
            "dimension": "time",
            "label": "2021 - Q3",
            "option": "2021-q3"
          },
          {
            "dimension": "time",
            "label": "2021 - Q2",
            "option": "2021-q2"
          },
          {
            "dimension": "time",
            "label": "2021 - Q1",
            "option": "2021-q1"
          },
          {
            "dimension": "time",
            "label": "2021 - Dec",
            "option": "2021-dec"
          },
          {
            "dimension": "time",
            "label": "2021 - Nov",
            "option": "2021-nov"
          },
          {
            "dimension": "time",
            "label": "2021 - Oct",
            "option": "2021-oct"
          },
          {
            "dimension": "time",
            "label": "2021 - Sep",
            "option": "2021-sep"
          },
          {
            "dimension": "time",
            "label": "2021 - Aug",
            "option": "2021-aug"
          },
          {
            "dimension": "time",
            "label": "2021 - Jul",
            "option": "2021-jul"
          },
          {
            "dimension": "time",
            "label": "2021 - Jun",
            "option": "2021-jun"
          },
          {
            "dimension": "time",
            "label": "2021 - May",
            "option": "2021-may"
          },
          {
            "dimension": "time",
            "label": "2021 - Apr",
            "option": "2021-apr"
          },
          {
            "dimension": "time",
            "label": "2021 - Mar",
            "option": "2021-mar"
          },
          {
            "dimension": "time",
            "label": "2021 - Feb",
            "option": "2021-feb"
          },
          {
            "dimension": "time",
            "label": "2021 - Jan",
            "option": "2021-jan"
          },
          {
            "dimension": "time",
            "label": "2020",
            "option": "2020"
          },
          {
            "dimension": "time",
            "label": "2020 - Q4",
            "option": "2020-q4"
          },
          {
            "dimension": "time",
            "label": "2020 - Q3",
            "option": "2020-q3"
          },
          {
            "dimension": "time",
            "label": "2020 - Q2",
            "option": "2020-q2"
          },
          {
            "dimension": "time",
            "label": "2020 - Q1",
            "option": "2020-q1"
          },
          {
            "dimension": "time",
            "label": "2020 - Dec",
            "option": "2020-dec"
          },
          {
            "dimension": "time",
            "label": "2020 - Nov",
            "option": "2020-nov"
          },
          {
            "dimension": "time",
            "label": "2020 - Oct",
            "option": "2020-oct"
          },
          {
            "dimension": "time",
            "label": "2020 - Sep",
            "option": "2020-sep"
          },
          {
            "dimension": "time",
            "label": "2020 - Aug",
            "option": "2020-aug"
          },
          {
            "dimension": "time",
            "label": "2020 - Jul",
            "option": "2020-jul"
          },
          {
            "dimension": "time",
            "label": "2020 - Jun",
            "option": "2020-jun"
          },
          {
            "dimension": "time",
            "label": "2020 - May",
            "option": "2020-may"
          },
          {
            "dimension": "time",
            "label": "2020 - Apr",
            "option": "2020-apr"
          },
          {
            "dimension": "time",
            "label": "2020 - Mar",
            "option": "2020-mar"
          },
          {
            "dimension": "time",
            "label": "2020 - Feb",
            "option": "2020-feb"
          },
          {
            "dimension": "time",
            "label": "2020 - Jan",
            "option": "2020-jan"
          },
          {
            "dimension": "time",
            "label": "2019",
            "option": "2019"
          },
          {
            "dimension": "time",
            "label": "2019 - Q4",
            "option": "2019-q4"
          },
          {
            "dimension": "time",
            "label": "2019 - Q3",
            "option": "2019-q3"
          },
          {
            "dimension": "time",
            "label": "2019 - Q2",
            "option": "2019-q2"
          },
          {
            "dimension": "time",
            "label": "2019 - Q1",
            "option": "2019-q1"
          },
          {
            "dimension": "time",
            "label": "2019 - Dec",
            "option": "2019-dec"
          },
          {
            "dimension": "time",
            "label": "2019 - Nov",
            "option": "2019-nov"
          },
          {
            "dimension": "time",
            "label": "2019 - Oct",
            "option": "2019-oct"
          },
          {
            "dimension": "time",
            "label": "2019 - Sep",
            "option": "2019-sep"
          },
          {
            "dimension": "time",
            "label": "2019 - Aug",
            "option": "2019-aug"
          },
          {
            "dimension": "time",
            "label": "2019 - Jul",
            "option": "2019-jul"
          },
          {
            "dimension": "time",
            "label": "2019 - Jun",
            "option": "2019-jun"
          },
          {
            "dimension": "time",
            "label": "2019 - May",
            "option": "2019-may"
          },
          {
            "dimension": "time",
            "label": "2019 - Apr",
            "option": "2019-apr"
          },
          {
            "dimension": "time",
            "label": "2019 - Mar",
            "option": "2019-mar"
          },
          {
            "dimension": "time",
            "label": "2019 - Feb",
            "option": "2019-feb"
          },
          {
            "dimension": "time",
            "label": "2019 - Jan",
            "option": "2019-jan"
          },
          {
            "dimension": "time",
            "label": "2018",
            "option": "2018"
          },
          {
            "dimension": "time",
            "label": "2018 - Q4",
            "option": "2018-q4"
          },
          {
            "dimension": "time",
            "label": "2018 - Q3",
            "option": "2018-q3"
          },
          {
            "dimension": "time",
            "label": "2018 - Q2",
            "option": "2018-q2"
          },
          {
            "dimension": "time",
            "label": "2018 - Q1",
            "option": "2018-q1"
          },
          {
            "dimension": "time",
            "label": "2018 - Dec",
            "option": "2018-dec"
          },
          {
            "dimension": "time",
            "label": "2018 - Nov",
            "option": "2018-nov"
          },
          {
            "dimension": "time",
            "label": "2018 - Oct",
            "option": "2018-oct"
          },
          {
            "dimension": "time",
            "label": "2018 - Sep",
            "option": "2018-sep"
          },
          {
            "dimension": "time",
            "label": "2018 - Aug",
            "option": "2018-aug"
          },
          {
            "dimension": "time",
            "label": "2018 - Jul",
            "option": "2018-jul"
          },
          {
            "dimension": "time",
            "label": "2018 - Jun",
            "option": "2018-jun"
          },
          {
            "dimension": "time",
            "label": "2018 - May",
            "option": "2018-may"
          },
          {
            "dimension": "time",
            "label": "2018 - Apr",
            "option": "2018-apr"
          },
          {
            "dimension": "time",
            "label": "2018 - Mar",
            "option": "2018-mar"
          },
          {
            "dimension": "time",
            "label": "2018 - Feb",
            "option": "2018-feb"
          },
          {
            "dimension": "time",
            "label": "2018 - Jan",
            "option": "2018-jan"
          },
          {
            "dimension": "time",
            "label": "2017",
            "option": "2017"
          },
          {
            "dimension": "time",
            "label": "2017 - Q4",
            "option": "2017-q4"
          },
          {
            "dimension": "time",
            "label": "2017 - Q3",
            "option": "2017-q3"
          },
          {
            "dimension": "time",
            "label": "2017 - Q2",
            "option": "2017-q2"
          },
          {
            "dimension": "time",
            "label": "2017 - Q1",
            "option": "2017-q1"
          },
          {
            "dimension": "time",
            "label": "2017 - Dec",
            "option": "2017-dec"
          },
          {
            "dimension": "time",
            "label": "2017 - Nov",
            "option": "2017-nov"
          },
          {
            "dimension": "time",
            "label": "2017 - Oct",
            "option": "2017-oct"
          },
          {
            "dimension": "time",
            "label": "2017 - Sep",
            "option": "2017-sep"
          },
          {
            "dimension": "time",
            "label": "2017 - Aug",
            "option": "2017-aug"
          },
          {
            "dimension": "time",
            "label": "2017 - Jul",
            "option": "2017-jul"
          },
          {
            "dimension": "time",
            "label": "2017 - Jun",
            "option": "2017-jun"
          },
          {
            "dimension": "time",
            "label": "2017 - May",
            "option": "2017-may"
          },
          {
            "dimension": "time",
            "label": "2017 - Apr",
            "option": "2017-apr"
          },
          {
            "dimension": "time",
            "label": "2017 - Mar",
            "option": "2017-mar"
          },
          {
            "dimension": "time",
            "label": "2017 - Feb",
            "option": "2017-feb"
          },
          {
            "dimension": "time",
            "label": "2017 - Jan",
            "option": "2017-jan"
          },
          {
            "dimension": "time",
            "label": "2016",
            "option": "2016"
          },
          {
            "dimension": "time",
            "label": "2016 - Q4",
            "option": "2016-q4"
          },
          {
            "dimension": "time",
            "label": "2016 - Q3",
            "option": "2016-q3"
          },
          {
            "dimension": "time",
            "label": "2016 - Q2",
            "option": "2016-q2"
          },
          {
            "dimension": "time",
            "label": "2016 - Q1",
            "option": "2016-q1"
          },
          {
            "dimension": "time",
            "label": "2016 - Dec",
            "option": "2016-dec"
          },
          {
            "dimension": "time",
            "label": "2016 - Nov",
            "option": "2016-nov"
          },
          {
            "dimension": "time",
            "label": "2016 - Oct",
            "option": "2016-oct"
          },
          {
            "dimension": "time",
            "label": "2016 - Sep",
            "option": "2016-sep"
          },
          {
            "dimension": "time",
            "label": "2016 - Aug",
            "option": "2016-aug"
          },
          {
            "dimension": "time",
            "label": "2016 - Jul",
            "option": "2016-jul"
          },
          {
            "dimension": "time",
            "label": "2016 - Jun",
            "option": "2016-jun"
          },
          {
            "dimension": "time",
            "label": "2016 - May",
            "option": "2016-may"
          },
          {
            "dimension": "time",
            "label": "2016 - Apr",
            "option": "2016-apr"
          },
          {
            "dimension": "time",
            "label": "2016 - Mar",
            "option": "2016-mar"
          },
          {
            "dimension": "time",
            "label": "2016 - Feb",
            "option": "2016-feb"
          },
          {
            "dimension": "time",
            "label": "2016 - Jan",
            "option": "2016-jan"
          },
          {
            "dimension": "time",
            "label": "2015",
            "option": "2015"
          },
          {
            "dimension": "time",
            "label": "2015 - Q4",
            "option": "2015-q4"
          },
          {
            "dimension": "time",
            "label": "2015 - Q3",
            "option": "2015-q3"
          },
          {
            "dimension": "time",
            "label": "2015 - Q2",
            "option": "2015-q2"
          },
          {
            "dimension": "time",
            "label": "2015 - Q1",
            "option": "2015-q1"
          },
          {
            "dimension": "time",
            "label": "2015 - Dec",
            "option": "2015-dec"
          },
          {
            "dimension": "time",
            "label": "2015 - Nov",
            "option": "2015-nov"
          },
          {
            "dimension": "time",
            "label": "2015 - Oct",
            "option": "2015-oct"
          },
          {
            "dimension": "time",
            "label": "2015 - Sep",
            "option": "2015-sep"
          },
          {
            "dimension": "time",
            "label": "2015 - Aug",
            "option": "2015-aug"
          },
          {
            "dimension": "time",
            "label": "2015 - Jul",
            "option": "2015-jul"
          },
          {
            "dimension": "time",
            "label": "2015 - Jun",
            "option": "2015-jun"
          },
          {
            "dimension": "time",
            "label": "2015 - May",
            "option": "2015-may"
          },
          {
            "dimension": "time",
            "label": "2015 - Apr",
            "option": "2015-apr"
          },
          {
            "dimension": "time",
            "label": "2015 - Mar",
            "option": "2015-mar"
          },
          {
            "dimension": "time",
            "label": "2015 - Feb",
            "option": "2015-feb"
          },
          {
            "dimension": "time",
            "label": "2015 - Jan",
            "option": "2015-jan"
          },
          {
            "dimension": "time",
            "label": "2014",
            "option": "2014"
          },
          {
            "dimension": "time",
            "label": "2014 - Q4",
            "option": "2014-q4"
          },
          {
            "dimension": "time",
            "label": "2014 - Q3",
            "option": "2014-q3"
          },
          {
            "dimension": "time",
            "label": "2014 - Q2",
            "option": "2014-q2"
          },
          {
            "dimension": "time",
            "label": "2014 - Q1",
            "option": "2014-q1"
          },
          {
            "dimension": "time",
            "label": "2014 - Dec",
            "option": "2014-dec"
          },
          {
            "dimension": "time",
            "label": "2014 - Nov",
            "option": "2014-nov"
          },
          {
            "dimension": "time",
            "label": "2014 - Oct",
            "option": "2014-oct"
          },
          {
            "dimension": "time",
            "label": "2014 - Sep",
            "option": "2014-sep"
          },
          {
            "dimension": "time",
            "label": "2014 - Aug",
            "option": "2014-aug"
          },
          {
            "dimension": "time",
            "label": "2014 - Jul",
            "option": "2014-jul"
          },
          {
            "dimension": "time",
            "label": "2014 - Jun",
            "option": "2014-jun"
          },
          {
            "dimension": "time",
            "label": "2014 - May",
            "option": "2014-may"
          },
          {
            "dimension": "time",
            "label": "2014 - Apr",
            "option": "2014-apr"
          },
          {
            "dimension": "time",
            "label": "2014 - Mar",
            "option": "2014-mar"
          },
          {
            "dimension": "time",
            "label": "2014 - Feb",
            "option": "2014-feb"
          },
          {
            "dimension": "time",
            "label": "2014 - Jan",
            "option": "2014-jan"
          },
          {
            "dimension": "time",
            "label": "2013",
            "option": "2013"
          },
          {
            "dimension": "time",
            "label": "2013 - Q4",
            "option": "2013-q4"
          },
          {
            "dimension": "time",
            "label": "2013 - Q3",
            "option": "2013-q3"
          },
          {
            "dimension": "time",
            "label": "2013 - Q2",
            "option": "2013-q2"
          },
          {
            "dimension": "time",
            "label": "2013 - Q1",
            "option": "2013-q1"
          },
          {
            "dimension": "time",
            "label": "2013 - Dec",
            "option": "2013-dec"
          },
          {
            "dimension": "time",
            "label": "2013 - Nov",
            "option": "2013-nov"
          },
          {
            "dimension": "time",
            "label": "2013 - Oct",
            "option": "2013-oct"
          },
          {
            "dimension": "time",
            "label": "2013 - Sep",
            "option": "2013-sep"
          },
          {
            "dimension": "time",
            "label": "2013 - Aug",
            "option": "2013-aug"
          },
          {
            "dimension": "time",
            "label": "2013 - Jul",
            "option": "2013-jul"
          },
          {
            "dimension": "time",
            "label": "2013 - Jun",
            "option": "2013-jun"
          },
          {
            "dimension": "time",
            "label": "2013 - May",
            "option": "2013-may"
          },
          {
            "dimension": "time",
            "label": "2013 - Apr",
            "option": "2013-apr"
          },
          {
            "dimension": "time",
            "label": "2013 - Mar",
            "option": "2013-mar"
          },
          {
            "dimension": "time",
            "label": "2013 - Feb",
            "option": "2013-feb"
          },
          {
            "dimension": "time",
            "label": "2013 - Jan",
            "option": "2013-jan"
          },
          {
            "dimension": "time",
            "label": "2012",
            "option": "2012"
          },
          {
            "dimension": "time",
            "label": "2012 - Q4",
            "option": "2012-q4"
          },
          {
            "dimension": "time",
            "label": "2012 - Q3",
            "option": "2012-q3"
          },
          {
            "dimension": "time",
            "label": "2012 - Q2",
            "option": "2012-q2"
          },
          {
            "dimension": "time",
            "label": "2012 - Q1",
            "option": "2012-q1"
          },
          {
            "dimension": "time",
            "label": "2012 - Dec",
            "option": "2012-dec"
          },
          {
            "dimension": "time",
            "label": "2012 - Nov",
            "option": "2012-nov"
          },
          {
            "dimension": "time",
            "label": "2012 - Oct",
            "option": "2012-oct"
          },
          {
            "dimension": "time",
            "label": "2012 - Sep",
            "option": "2012-sep"
          },
          {
            "dimension": "time",
            "label": "2012 - Aug",
            "option": "2012-aug"
          },
          {
            "dimension": "time",
            "label": "2012 - Jul",
            "option": "2012-jul"
          },
          {
            "dimension": "time",
            "label": "2012 - Jun",
            "option": "2012-jun"
          },
          {
            "dimension": "time",
            "label": "2012 - May",
            "option": "2012-may"
          },
          {
            "dimension": "time",
            "label": "2012 - Apr",
            "option": "2012-apr"
          },
          {
            "dimension": "time",
            "label": "2012 - Mar",
            "option": "2012-mar"
          },
          {
            "dimension": "time",
            "label": "2012 - Feb",
            "option": "2012-feb"
          },
          {
            "dimension": "time",
            "label": "2012 - Jan",
            "option": "2012-jan"
          },
          {
            "dimension": "time",
            "label": "2011",
            "option": "2011"
          },
          {
            "dimension": "time",
            "label": "2011 - Q4",
            "option": "2011-q4"
          },
          {
            "dimension": "time",
            "label": "2011 - Q3",
            "option": "2011-q3"
          },
          {
            "dimension": "time",
            "label": "2011 - Q2",
            "option": "2011-q2"
          },
          {
            "dimension": "time",
            "label": "2011 - Q1",
            "option": "2011-q1"
          },
          {
            "dimension": "time",
            "label": "2011 - Dec",
            "option": "2011-dec"
          },
          {
            "dimension": "time",
            "label": "2011 - Nov",
            "option": "2011-nov"
          },
          {
            "dimension": "time",
            "label": "2011 - Oct",
            "option": "2011-oct"
          },
          {
            "dimension": "time",
            "label": "2011 - Sep",
            "option": "2011-sep"
          },
          {
            "dimension": "time",
            "label": "2011 - Aug",
            "option": "2011-aug"
          },
          {
            "dimension": "time",
            "label": "2011 - Jul",
            "option": "2011-jul"
          },
          {
            "dimension": "time",
            "label": "2011 - Jun",
            "option": "2011-jun"
          },
          {
            "dimension": "time",
            "label": "2011 - May",
            "option": "2011-may"
          },
          {
            "dimension": "time",
            "label": "2011 - Apr",
            "option": "2011-apr"
          },
          {
            "dimension": "time",
            "label": "2011 - Mar",
            "option": "2011-mar"
          },
          {
            "dimension": "time",
            "label": "2011 - Feb",
            "option": "2011-feb"
          },
          {
            "dimension": "time",
            "label": "2011 - Jan",
            "option": "2011-jan"
          },
          {
            "dimension": "time",
            "label": "2010",
            "option": "2010"
          },
          {
            "dimension": "time",
            "label": "2010 - Q4",
            "option": "2010-q4"
          },
          {
            "dimension": "time",
            "label": "2010 - Q3",
            "option": "2010-q3"
          },
          {
            "dimension": "time",
            "label": "2010 - Q2",
            "option": "2010-q2"
          },
          {
            "dimension": "time",
            "label": "2010 - Q1",
            "option": "2010-q1"
          },
          {
            "dimension": "time",
            "label": "2010 - Dec",
            "option": "2010-dec"
          },
          {
            "dimension": "time",
            "label": "2010 - Nov",
            "option": "2010-nov"
          },
          {
            "dimension": "time",
            "label": "2010 - Oct",
            "option": "2010-oct"
          },
          {
            "dimension": "time",
            "label": "2010 - Sep",
            "option": "2010-sep"
          },
          {
            "dimension": "time",
            "label": "2010 - Aug",
            "option": "2010-aug"
          },
          {
            "dimension": "time",
            "label": "2010 - Jul",
            "option": "2010-jul"
          },
          {
            "dimension": "time",
            "label": "2010 - Jun",
            "option": "2010-jun"
          },
          {
            "dimension": "time",
            "label": "2010 - May",
            "option": "2010-may"
          },
          {
            "dimension": "time",
            "label": "2010 - Apr",
            "option": "2010-apr"
          },
          {
            "dimension": "time",
            "label": "2010 - Mar",
            "option": "2010-mar"
          },
          {
            "dimension": "time",
            "label": "2010 - Feb",
            "option": "2010-feb"
          },
          {
            "dimension": "time",
            "label": "2010 - Jan",
            "option": "2010-jan"
          },
          {
            "dimension": "time",
            "label": "2009",
            "option": "2009"
          },
          {
            "dimension": "time",
            "label": "2009 - Q4",
            "option": "2009-q4"
          },
          {
            "dimension": "time",
            "label": "2009 - Q3",
            "option": "2009-q3"
          },
          {
            "dimension": "time",
            "label": "2009 - Q2",
            "option": "2009-q2"
          },
          {
            "dimension": "time",
            "label": "2009 - Q1",
            "option": "2009-q1"
          },
          {
            "dimension": "time",
            "label": "2008",
            "option": "2008"
          },
          {
            "dimension": "time",
            "label": "2008 - Q4",
            "option": "2008-q4"
          },
          {
            "dimension": "time",
            "label": "2008 - Q3",
            "option": "2008-q3"
          },
          {
            "dimension": "time",
            "label": "2008 - Q2",
            "option": "2008-q2"
          },
          {
            "dimension": "time",
            "label": "2008 - Q1",
            "option": "2008-q1"
          },
          {
            "dimension": "time",
            "label": "2007",
            "option": "2007"
          },
          {
            "dimension": "time",
            "label": "2007 - Q4",
            "option": "2007-q4"
          },
          {
            "dimension": "time",
            "label": "2007 - Q3",
            "option": "2007-q3"
          },
          {
            "dimension": "time",
            "label": "2007 - Q2",
            "option": "2007-q2"
          },
          {
            "dimension": "time",
            "label": "2007 - Q1",
            "option": "2007-q1"
          },
          {
            "dimension": "time",
            "label": "2006",
            "option": "2006"
          },
          {
            "dimension": "time",
            "label": "2006 - Q4",
            "option": "2006-q4"
          },
          {
            "dimension": "time",
            "label": "2006 - Q3",
            "option": "2006-q3"
          },
          {
            "dimension": "time",
            "label": "2006 - Q2",
            "option": "2006-q2"
          },
          {
            "dimension": "time",
            "label": "2006 - Q1",
            "option": "2006-q1"
          },
          {
            "dimension": "time",
            "label": "2005",
            "option": "2005"
          },
          {
            "dimension": "time",
            "label": "2005 - Q4",
            "option": "2005-q4"
          },
          {
            "dimension": "time",
            "label": "2005 - Q3",
            "option": "2005-q3"
          },
          {
            "dimension": "time",
            "label": "2005 - Q2",
            "option": "2005-q2"
          },
          {
            "dimension": "time",
            "label": "2005 - Q1",
            "option": "2005-q1"
          },
          {
            "dimension": "time",
            "label": "2004",
            "option": "2004"
          },
          {
            "dimension": "time",
            "label": "2004 - Q4",
            "option": "2004-q4"
          },
          {
            "dimension": "time",
            "label": "2004 - Q3",
            "option": "2004-q3"
          },
          {
            "dimension": "time",
            "label": "2004 - Q2",
            "option": "2004-q2"
          },
          {
            "dimension": "time",
            "label": "2004 - Q1",
            "option": "2004-q1"
          },
          {
            "dimension": "time",
            "label": "2003",
            "option": "2003"
          },
          {
            "dimension": "time",
            "label": "2003 - Q4",
            "option": "2003-q4"
          },
          {
            "dimension": "time",
            "label": "2003 - Q3",
            "option": "2003-q3"
          },
          {
            "dimension": "time",
            "label": "2003 - Q2",
            "option": "2003-q2"
          },
          {
            "dimension": "time",
            "label": "2003 - Q1",
            "option": "2003-q1"
          },
          {
            "dimension": "time",
            "label": "2002",
            "option": "2002"
          },
          {
            "dimension": "time",
            "label": "2002 - Q4",
            "option": "2002-q4"
          },
          {
            "dimension": "time",
            "label": "2002 - Q3",
            "option": "2002-q3"
          },
          {
            "dimension": "time",
            "label": "2002 - Q2",
            "option": "2002-q2"
          },
          {
            "dimension": "time",
            "label": "2002 - Q1",
            "option": "2002-q1"
          },
          {
            "dimension": "time",
            "label": "2001",
            "option": "2001"
          },
          {
            "dimension": "time",
            "label": "2001 - Q4",
            "option": "2001-q4"
          },
          {
            "dimension": "time",
            "label": "2001 - Q3",
            "option": "2001-q3"
          },
          {
            "dimension": "time",
            "label": "2001 - Q2",
            "option": "2001-q2"
          },
          {
            "dimension": "time",
            "label": "2001 - Q1",
            "option": "2001-q1"
          },
          {
            "dimension": "time",
            "label": "2000",
            "option": "2000"
          },
          {
            "dimension": "time",
            "label": "2000 - Q4",
            "option": "2000-q4"
          },
          {
            "dimension": "time",
            "label": "2000 - Q3",
            "option": "2000-q3"
          },
          {
            "dimension": "time",
            "label": "2000 - Q2",
            "option": "2000-q2"
          },
          {
            "dimension": "time",
            "label": "2000 - Q1",
            "option": "2000-q1"
          },
          {
            "dimension": "time",
            "label": "1999",
            "option": "1999"
          },
          {
            "dimension": "time",
            "label": "1999 - Q4",
            "option": "1999-q4"
          },
          {
            "dimension": "time",
            "label": "1999 - Q3",
            "option": "1999-q3"
          },
          {
            "dimension": "time",
            "label": "1999 - Q2",
            "option": "1999-q2"
          },
          {
            "dimension": "time",
            "label": "1999 - Q1",
            "option": "1999-q1"
          },
          {
            "dimension": "time",
            "label": "1998",
            "option": "1998"
          },
          {
            "dimension": "time",
            "label": "1998 - Q4",
            "option": "1998-q4"
          },
          {
            "dimension": "time",
            "label": "1998 - Q3",
            "option": "1998-q3"
          },
          {
            "dimension": "time",
            "label": "1998 - Q2",
            "option": "1998-q2"
          },
          {
            "dimension": "time",
            "label": "1998 - Q1",
            "option": "1998-q1"
          },
          {
            "dimension": "time",
            "label": "1997",
            "option": "1997"
          },
          {
            "dimension": "time",
            "label": "1997 - Q4",
            "option": "1997-q4"
          },
          {
            "dimension": "time",
            "label": "1997 - Q3",
            "option": "1997-q3"
          },
          {
            "dimension": "time",
            "label": "1997 - Q2",
            "option": "1997-q2"
          },
          {
            "dimension": "time",
            "label": "1997 - Q1",
            "option": "1997-q1"
          }
        ],
        "reportedTotal": 341,
        "retrievedUnique": 341,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "54",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/output-in-the-construction-industry/editions/time-series/versions/54"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-M"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/output-in-the-construction-industry/editions"
  }
}
---

# Output in the construction industry

Monthly construction output for Great Britain at current price and chained volume measures, seasonally adjusted by public and private sector.

Native identifier: `output-in-the-construction-industry`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/output-in-the-construction-industry)

Update cadence: Monthly.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
