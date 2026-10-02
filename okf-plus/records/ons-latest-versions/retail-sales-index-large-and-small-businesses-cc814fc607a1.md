---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/retail-sales-index-large-and-small-businesses",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Retail sales index - large and small businesses",
  "description": "Value and volume of retail sales broken down by size of business",
  "nativeIdentifier": "retail-sales-index-large-and-small-businesses",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/retail-sales-index-large-and-small-businesses/editions/time-series/versions/45",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/retail-sales-index-large-and-small-businesses/editions/time-series/versions/45/metadata",
      "retrievedAt": "2026-10-02T01:30:42.467902Z",
      "responseSha256": "5b68c5985620d6e29637177f075f15b00a3a540c97b96bd2300d3e0aaf0b9368",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/15",
      "normalisedRecordSha256": "e09c97cd219b922590174db4083bc880f09a1a183f2349c220ef05511e342066",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/retail-sales-index-large-and-small-businesses/editions/time-series/versions/45"
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
    "nextRelease": "27 March 2026",
    "metadataModified": "2026-02-20T10:18:30.386Z",
    "releaseVersion": "45"
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
        "id": "years-quarters-months",
        "label": "Time",
        "name": "time"
      },
      {
        "id": "countries",
        "label": "Geography",
        "name": "geography"
      },
      {
        "id": "sic-unofficial",
        "label": "Standard industrial classification",
        "name": "unofficialstandardindustrialclassification"
      },
      {
        "id": "type-of-prices",
        "label": "Prices",
        "name": "prices"
      },
      {
        "id": "seasonal-adjustment",
        "label": "Seasonal adjustment",
        "name": "seasonaladjustment"
      }
    ],
    "edition": "time-series",
    "id": "retail-sales-index-large-and-small-businesses",
    "metadata": {
      "description": "Value and volume of retail sales broken down by size of business",
      "last_updated": "2026-02-20T10:18:30.386Z",
      "next_release": "27 March 2026",
      "release_date": "2026-02-20T00:00:00.000Z",
      "release_frequency": "Monthly",
      "state": "published",
      "title": "Retail sales index - large and small businesses",
      "type": "filterable",
      "unit_of_measure": "2019=100"
    },
    "metadataContract": {
      "catalogueType": "filterable",
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "time-series",
        "id": "retail-sales-index-large-and-small-businesses",
        "version": 45
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:30:42.467902Z",
      "sha256": "5b68c5985620d6e29637177f075f15b00a3a540c97b96bd2300d3e0aaf0b9368",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/retail-sales-index-large-and-small-businesses/editions/time-series/versions/45/metadata"
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
          "label": "2009 - Dec",
          "option": "2009-dec"
        },
        {
          "dimension": "time",
          "label": "2009 - Nov",
          "option": "2009-nov"
        },
        {
          "dimension": "time",
          "label": "2009 - Oct",
          "option": "2009-oct"
        },
        {
          "dimension": "time",
          "label": "2009 - Sep",
          "option": "2009-sep"
        },
        {
          "dimension": "time",
          "label": "2009 - Aug",
          "option": "2009-aug"
        },
        {
          "dimension": "time",
          "label": "2009 - Jul",
          "option": "2009-jul"
        },
        {
          "dimension": "time",
          "label": "2009 - Jun",
          "option": "2009-jun"
        },
        {
          "dimension": "time",
          "label": "2009 - May",
          "option": "2009-may"
        },
        {
          "dimension": "time",
          "label": "2009 - Apr",
          "option": "2009-apr"
        },
        {
          "dimension": "time",
          "label": "2009 - Mar",
          "option": "2009-mar"
        },
        {
          "dimension": "time",
          "label": "2009 - Feb",
          "option": "2009-feb"
        },
        {
          "dimension": "time",
          "label": "2009 - Jan",
          "option": "2009-jan"
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
          "label": "2008 - Dec",
          "option": "2008-dec"
        },
        {
          "dimension": "time",
          "label": "2008 - Nov",
          "option": "2008-nov"
        },
        {
          "dimension": "time",
          "label": "2008 - Oct",
          "option": "2008-oct"
        },
        {
          "dimension": "time",
          "label": "2008 - Sep",
          "option": "2008-sep"
        },
        {
          "dimension": "time",
          "label": "2008 - Aug",
          "option": "2008-aug"
        },
        {
          "dimension": "time",
          "label": "2008 - Jul",
          "option": "2008-jul"
        },
        {
          "dimension": "time",
          "label": "2008 - Jun",
          "option": "2008-jun"
        },
        {
          "dimension": "time",
          "label": "2008 - May",
          "option": "2008-may"
        },
        {
          "dimension": "time",
          "label": "2008 - Apr",
          "option": "2008-apr"
        },
        {
          "dimension": "time",
          "label": "2008 - Mar",
          "option": "2008-mar"
        },
        {
          "dimension": "time",
          "label": "2008 - Feb",
          "option": "2008-feb"
        },
        {
          "dimension": "time",
          "label": "2008 - Jan",
          "option": "2008-jan"
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
          "label": "2007 - Dec",
          "option": "2007-dec"
        },
        {
          "dimension": "time",
          "label": "2007 - Nov",
          "option": "2007-nov"
        },
        {
          "dimension": "time",
          "label": "2007 - Oct",
          "option": "2007-oct"
        },
        {
          "dimension": "time",
          "label": "2007 - Sep",
          "option": "2007-sep"
        },
        {
          "dimension": "time",
          "label": "2007 - Aug",
          "option": "2007-aug"
        },
        {
          "dimension": "time",
          "label": "2007 - Jul",
          "option": "2007-jul"
        },
        {
          "dimension": "time",
          "label": "2007 - Jun",
          "option": "2007-jun"
        },
        {
          "dimension": "time",
          "label": "2007 - May",
          "option": "2007-may"
        },
        {
          "dimension": "time",
          "label": "2007 - Apr",
          "option": "2007-apr"
        },
        {
          "dimension": "time",
          "label": "2007 - Mar",
          "option": "2007-mar"
        },
        {
          "dimension": "time",
          "label": "2007 - Feb",
          "option": "2007-feb"
        },
        {
          "dimension": "time",
          "label": "2007 - Jan",
          "option": "2007-jan"
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
          "label": "2006 - Dec",
          "option": "2006-dec"
        },
        {
          "dimension": "time",
          "label": "2006 - Nov",
          "option": "2006-nov"
        },
        {
          "dimension": "time",
          "label": "2006 - Oct",
          "option": "2006-oct"
        },
        {
          "dimension": "time",
          "label": "2006 - Sep",
          "option": "2006-sep"
        },
        {
          "dimension": "time",
          "label": "2006 - Aug",
          "option": "2006-aug"
        },
        {
          "dimension": "time",
          "label": "2006 - Jul",
          "option": "2006-jul"
        },
        {
          "dimension": "time",
          "label": "2006 - Jun",
          "option": "2006-jun"
        },
        {
          "dimension": "time",
          "label": "2006 - May",
          "option": "2006-may"
        },
        {
          "dimension": "time",
          "label": "2006 - Apr",
          "option": "2006-apr"
        },
        {
          "dimension": "time",
          "label": "2006 - Mar",
          "option": "2006-mar"
        },
        {
          "dimension": "time",
          "label": "2006 - Feb",
          "option": "2006-feb"
        },
        {
          "dimension": "time",
          "label": "2006 - Jan",
          "option": "2006-jan"
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
          "label": "2005 - Dec",
          "option": "2005-dec"
        },
        {
          "dimension": "time",
          "label": "2005 - Nov",
          "option": "2005-nov"
        },
        {
          "dimension": "time",
          "label": "2005 - Oct",
          "option": "2005-oct"
        },
        {
          "dimension": "time",
          "label": "2005 - Sep",
          "option": "2005-sep"
        },
        {
          "dimension": "time",
          "label": "2005 - Aug",
          "option": "2005-aug"
        },
        {
          "dimension": "time",
          "label": "2005 - Jul",
          "option": "2005-jul"
        },
        {
          "dimension": "time",
          "label": "2005 - Jun",
          "option": "2005-jun"
        },
        {
          "dimension": "time",
          "label": "2005 - May",
          "option": "2005-may"
        },
        {
          "dimension": "time",
          "label": "2005 - Apr",
          "option": "2005-apr"
        },
        {
          "dimension": "time",
          "label": "2005 - Mar",
          "option": "2005-mar"
        },
        {
          "dimension": "time",
          "label": "2005 - Feb",
          "option": "2005-feb"
        },
        {
          "dimension": "time",
          "label": "2005 - Jan",
          "option": "2005-jan"
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
          "label": "2004 - Dec",
          "option": "2004-dec"
        },
        {
          "dimension": "time",
          "label": "2004 - Nov",
          "option": "2004-nov"
        },
        {
          "dimension": "time",
          "label": "2004 - Oct",
          "option": "2004-oct"
        },
        {
          "dimension": "time",
          "label": "2004 - Sep",
          "option": "2004-sep"
        },
        {
          "dimension": "time",
          "label": "2004 - Aug",
          "option": "2004-aug"
        },
        {
          "dimension": "time",
          "label": "2004 - Jul",
          "option": "2004-jul"
        },
        {
          "dimension": "time",
          "label": "2004 - Jun",
          "option": "2004-jun"
        },
        {
          "dimension": "time",
          "label": "2004 - May",
          "option": "2004-may"
        },
        {
          "dimension": "time",
          "label": "2004 - Apr",
          "option": "2004-apr"
        },
        {
          "dimension": "time",
          "label": "2004 - Mar",
          "option": "2004-mar"
        },
        {
          "dimension": "time",
          "label": "2004 - Feb",
          "option": "2004-feb"
        },
        {
          "dimension": "time",
          "label": "2004 - Jan",
          "option": "2004-jan"
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
          "label": "2003 - Dec",
          "option": "2003-dec"
        },
        {
          "dimension": "time",
          "label": "2003 - Nov",
          "option": "2003-nov"
        },
        {
          "dimension": "time",
          "label": "2003 - Oct",
          "option": "2003-oct"
        },
        {
          "dimension": "time",
          "label": "2003 - Sep",
          "option": "2003-sep"
        },
        {
          "dimension": "time",
          "label": "2003 - Aug",
          "option": "2003-aug"
        },
        {
          "dimension": "time",
          "label": "2003 - Jul",
          "option": "2003-jul"
        },
        {
          "dimension": "time",
          "label": "2003 - Jun",
          "option": "2003-jun"
        },
        {
          "dimension": "time",
          "label": "2003 - May",
          "option": "2003-may"
        },
        {
          "dimension": "time",
          "label": "2003 - Apr",
          "option": "2003-apr"
        },
        {
          "dimension": "time",
          "label": "2003 - Mar",
          "option": "2003-mar"
        },
        {
          "dimension": "time",
          "label": "2003 - Feb",
          "option": "2003-feb"
        },
        {
          "dimension": "time",
          "label": "2003 - Jan",
          "option": "2003-jan"
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
          "label": "2002 - Dec",
          "option": "2002-dec"
        },
        {
          "dimension": "time",
          "label": "2002 - Nov",
          "option": "2002-nov"
        },
        {
          "dimension": "time",
          "label": "2002 - Oct",
          "option": "2002-oct"
        },
        {
          "dimension": "time",
          "label": "2002 - Sep",
          "option": "2002-sep"
        },
        {
          "dimension": "time",
          "label": "2002 - Aug",
          "option": "2002-aug"
        },
        {
          "dimension": "time",
          "label": "2002 - Jul",
          "option": "2002-jul"
        },
        {
          "dimension": "time",
          "label": "2002 - Jun",
          "option": "2002-jun"
        },
        {
          "dimension": "time",
          "label": "2002 - May",
          "option": "2002-may"
        },
        {
          "dimension": "time",
          "label": "2002 - Apr",
          "option": "2002-apr"
        },
        {
          "dimension": "time",
          "label": "2002 - Mar",
          "option": "2002-mar"
        },
        {
          "dimension": "time",
          "label": "2002 - Feb",
          "option": "2002-feb"
        },
        {
          "dimension": "time",
          "label": "2002 - Jan",
          "option": "2002-jan"
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
          "label": "2001 - Dec",
          "option": "2001-dec"
        },
        {
          "dimension": "time",
          "label": "2001 - Nov",
          "option": "2001-nov"
        },
        {
          "dimension": "time",
          "label": "2001 - Oct",
          "option": "2001-oct"
        },
        {
          "dimension": "time",
          "label": "2001 - Sep",
          "option": "2001-sep"
        },
        {
          "dimension": "time",
          "label": "2001 - Aug",
          "option": "2001-aug"
        },
        {
          "dimension": "time",
          "label": "2001 - Jul",
          "option": "2001-jul"
        },
        {
          "dimension": "time",
          "label": "2001 - Jun",
          "option": "2001-jun"
        },
        {
          "dimension": "time",
          "label": "2001 - May",
          "option": "2001-may"
        },
        {
          "dimension": "time",
          "label": "2001 - Apr",
          "option": "2001-apr"
        },
        {
          "dimension": "time",
          "label": "2001 - Mar",
          "option": "2001-mar"
        },
        {
          "dimension": "time",
          "label": "2001 - Feb",
          "option": "2001-feb"
        },
        {
          "dimension": "time",
          "label": "2001 - Jan",
          "option": "2001-jan"
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
          "label": "2000 - Dec",
          "option": "2000-dec"
        },
        {
          "dimension": "time",
          "label": "2000 - Nov",
          "option": "2000-nov"
        },
        {
          "dimension": "time",
          "label": "2000 - Oct",
          "option": "2000-oct"
        },
        {
          "dimension": "time",
          "label": "2000 - Sep",
          "option": "2000-sep"
        },
        {
          "dimension": "time",
          "label": "2000 - Aug",
          "option": "2000-aug"
        },
        {
          "dimension": "time",
          "label": "2000 - Jul",
          "option": "2000-jul"
        },
        {
          "dimension": "time",
          "label": "2000 - Jun",
          "option": "2000-jun"
        },
        {
          "dimension": "time",
          "label": "2000 - May",
          "option": "2000-may"
        },
        {
          "dimension": "time",
          "label": "2000 - Apr",
          "option": "2000-apr"
        },
        {
          "dimension": "time",
          "label": "2000 - Mar",
          "option": "2000-mar"
        },
        {
          "dimension": "time",
          "label": "2000 - Feb",
          "option": "2000-feb"
        },
        {
          "dimension": "time",
          "label": "2000 - Jan",
          "option": "2000-jan"
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
          "label": "1999 - Dec",
          "option": "1999-dec"
        },
        {
          "dimension": "time",
          "label": "1999 - Nov",
          "option": "1999-nov"
        },
        {
          "dimension": "time",
          "label": "1999 - Oct",
          "option": "1999-oct"
        },
        {
          "dimension": "time",
          "label": "1999 - Sep",
          "option": "1999-sep"
        },
        {
          "dimension": "time",
          "label": "1999 - Aug",
          "option": "1999-aug"
        },
        {
          "dimension": "time",
          "label": "1999 - Jul",
          "option": "1999-jul"
        },
        {
          "dimension": "time",
          "label": "1999 - Jun",
          "option": "1999-jun"
        },
        {
          "dimension": "time",
          "label": "1999 - May",
          "option": "1999-may"
        },
        {
          "dimension": "time",
          "label": "1999 - Apr",
          "option": "1999-apr"
        },
        {
          "dimension": "time",
          "label": "1999 - Mar",
          "option": "1999-mar"
        },
        {
          "dimension": "time",
          "label": "1999 - Feb",
          "option": "1999-feb"
        },
        {
          "dimension": "time",
          "label": "1999 - Jan",
          "option": "1999-jan"
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
          "label": "1998 - Dec",
          "option": "1998-dec"
        },
        {
          "dimension": "time",
          "label": "1998 - Nov",
          "option": "1998-nov"
        },
        {
          "dimension": "time",
          "label": "1998 - Oct",
          "option": "1998-oct"
        },
        {
          "dimension": "time",
          "label": "1998 - Sep",
          "option": "1998-sep"
        },
        {
          "dimension": "time",
          "label": "1998 - Aug",
          "option": "1998-aug"
        },
        {
          "dimension": "time",
          "label": "1998 - Jul",
          "option": "1998-jul"
        },
        {
          "dimension": "time",
          "label": "1998 - Jun",
          "option": "1998-jun"
        },
        {
          "dimension": "time",
          "label": "1998 - May",
          "option": "1998-may"
        },
        {
          "dimension": "time",
          "label": "1998 - Apr",
          "option": "1998-apr"
        },
        {
          "dimension": "time",
          "label": "1998 - Mar",
          "option": "1998-mar"
        },
        {
          "dimension": "time",
          "label": "1998 - Feb",
          "option": "1998-feb"
        },
        {
          "dimension": "time",
          "label": "1998 - Jan",
          "option": "1998-jan"
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
        },
        {
          "dimension": "time",
          "label": "1997 - Dec",
          "option": "1997-dec"
        },
        {
          "dimension": "time",
          "label": "1997 - Nov",
          "option": "1997-nov"
        },
        {
          "dimension": "time",
          "label": "1997 - Oct",
          "option": "1997-oct"
        },
        {
          "dimension": "time",
          "label": "1997 - Sep",
          "option": "1997-sep"
        },
        {
          "dimension": "time",
          "label": "1997 - Aug",
          "option": "1997-aug"
        },
        {
          "dimension": "time",
          "label": "1997 - Jul",
          "option": "1997-jul"
        },
        {
          "dimension": "time",
          "label": "1997 - Jun",
          "option": "1997-jun"
        },
        {
          "dimension": "time",
          "label": "1997 - May",
          "option": "1997-may"
        },
        {
          "dimension": "time",
          "label": "1997 - Apr",
          "option": "1997-apr"
        },
        {
          "dimension": "time",
          "label": "1997 - Mar",
          "option": "1997-mar"
        },
        {
          "dimension": "time",
          "label": "1997 - Feb",
          "option": "1997-feb"
        },
        {
          "dimension": "time",
          "label": "1997 - Jan",
          "option": "1997-jan"
        },
        {
          "dimension": "time",
          "label": "1996",
          "option": "1996"
        },
        {
          "dimension": "time",
          "label": "1996 - Q4",
          "option": "1996-q4"
        },
        {
          "dimension": "time",
          "label": "1996 - Q3",
          "option": "1996-q3"
        },
        {
          "dimension": "time",
          "label": "1996 - Q2",
          "option": "1996-q2"
        },
        {
          "dimension": "time",
          "label": "1996 - Q1",
          "option": "1996-q1"
        },
        {
          "dimension": "time",
          "label": "1996 - Dec",
          "option": "1996-dec"
        },
        {
          "dimension": "time",
          "label": "1996 - Nov",
          "option": "1996-nov"
        },
        {
          "dimension": "time",
          "label": "1996 - Oct",
          "option": "1996-oct"
        },
        {
          "dimension": "time",
          "label": "1996 - Sep",
          "option": "1996-sep"
        },
        {
          "dimension": "time",
          "label": "1996 - Aug",
          "option": "1996-aug"
        },
        {
          "dimension": "time",
          "label": "1996 - Jul",
          "option": "1996-jul"
        },
        {
          "dimension": "time",
          "label": "1996 - Jun",
          "option": "1996-jun"
        },
        {
          "dimension": "time",
          "label": "1996 - May",
          "option": "1996-may"
        },
        {
          "dimension": "time",
          "label": "1996 - Apr",
          "option": "1996-apr"
        },
        {
          "dimension": "time",
          "label": "1996 - Mar",
          "option": "1996-mar"
        },
        {
          "dimension": "time",
          "label": "1996 - Feb",
          "option": "1996-feb"
        },
        {
          "dimension": "time",
          "label": "1996 - Jan",
          "option": "1996-jan"
        },
        {
          "dimension": "time",
          "label": "1995",
          "option": "1995"
        },
        {
          "dimension": "time",
          "label": "1995 - Q4",
          "option": "1995-q4"
        },
        {
          "dimension": "time",
          "label": "1995 - Q3",
          "option": "1995-q3"
        },
        {
          "dimension": "time",
          "label": "1995 - Q2",
          "option": "1995-q2"
        },
        {
          "dimension": "time",
          "label": "1995 - Q1",
          "option": "1995-q1"
        },
        {
          "dimension": "time",
          "label": "1995 - Dec",
          "option": "1995-dec"
        },
        {
          "dimension": "time",
          "label": "1995 - Nov",
          "option": "1995-nov"
        },
        {
          "dimension": "time",
          "label": "1995 - Oct",
          "option": "1995-oct"
        },
        {
          "dimension": "time",
          "label": "1995 - Sep",
          "option": "1995-sep"
        },
        {
          "dimension": "time",
          "label": "1995 - Aug",
          "option": "1995-aug"
        },
        {
          "dimension": "time",
          "label": "1995 - Jul",
          "option": "1995-jul"
        },
        {
          "dimension": "time",
          "label": "1995 - Jun",
          "option": "1995-jun"
        },
        {
          "dimension": "time",
          "label": "1995 - May",
          "option": "1995-may"
        },
        {
          "dimension": "time",
          "label": "1995 - Apr",
          "option": "1995-apr"
        },
        {
          "dimension": "time",
          "label": "1995 - Mar",
          "option": "1995-mar"
        },
        {
          "dimension": "time",
          "label": "1995 - Feb",
          "option": "1995-feb"
        },
        {
          "dimension": "time",
          "label": "1995 - Jan",
          "option": "1995-jan"
        },
        {
          "dimension": "time",
          "label": "1994",
          "option": "1994"
        },
        {
          "dimension": "time",
          "label": "1994 - Q4",
          "option": "1994-q4"
        },
        {
          "dimension": "time",
          "label": "1994 - Q3",
          "option": "1994-q3"
        },
        {
          "dimension": "time",
          "label": "1994 - Q2",
          "option": "1994-q2"
        },
        {
          "dimension": "time",
          "label": "1994 - Q1",
          "option": "1994-q1"
        },
        {
          "dimension": "time",
          "label": "1994 - Dec",
          "option": "1994-dec"
        },
        {
          "dimension": "time",
          "label": "1994 - Nov",
          "option": "1994-nov"
        },
        {
          "dimension": "time",
          "label": "1994 - Oct",
          "option": "1994-oct"
        },
        {
          "dimension": "time",
          "label": "1994 - Sep",
          "option": "1994-sep"
        },
        {
          "dimension": "time",
          "label": "1994 - Aug",
          "option": "1994-aug"
        },
        {
          "dimension": "time",
          "label": "1994 - Jul",
          "option": "1994-jul"
        },
        {
          "dimension": "time",
          "label": "1994 - Jun",
          "option": "1994-jun"
        },
        {
          "dimension": "time",
          "label": "1994 - May",
          "option": "1994-may"
        },
        {
          "dimension": "time",
          "label": "1994 - Apr",
          "option": "1994-apr"
        },
        {
          "dimension": "time",
          "label": "1994 - Mar",
          "option": "1994-mar"
        },
        {
          "dimension": "time",
          "label": "1994 - Feb",
          "option": "1994-feb"
        },
        {
          "dimension": "time",
          "label": "1994 - Jan",
          "option": "1994-jan"
        },
        {
          "dimension": "time",
          "label": "1993",
          "option": "1993"
        },
        {
          "dimension": "time",
          "label": "1993 - Q4",
          "option": "1993-q4"
        },
        {
          "dimension": "time",
          "label": "1993 - Q3",
          "option": "1993-q3"
        },
        {
          "dimension": "time",
          "label": "1993 - Q2",
          "option": "1993-q2"
        },
        {
          "dimension": "time",
          "label": "1993 - Q1",
          "option": "1993-q1"
        },
        {
          "dimension": "time",
          "label": "1993 - Dec",
          "option": "1993-dec"
        },
        {
          "dimension": "time",
          "label": "1993 - Nov",
          "option": "1993-nov"
        },
        {
          "dimension": "time",
          "label": "1993 - Oct",
          "option": "1993-oct"
        },
        {
          "dimension": "time",
          "label": "1993 - Sep",
          "option": "1993-sep"
        },
        {
          "dimension": "time",
          "label": "1993 - Aug",
          "option": "1993-aug"
        },
        {
          "dimension": "time",
          "label": "1993 - Jul",
          "option": "1993-jul"
        },
        {
          "dimension": "time",
          "label": "1993 - Jun",
          "option": "1993-jun"
        },
        {
          "dimension": "time",
          "label": "1993 - May",
          "option": "1993-may"
        },
        {
          "dimension": "time",
          "label": "1993 - Apr",
          "option": "1993-apr"
        },
        {
          "dimension": "time",
          "label": "1993 - Mar",
          "option": "1993-mar"
        },
        {
          "dimension": "time",
          "label": "1993 - Feb",
          "option": "1993-feb"
        },
        {
          "dimension": "time",
          "label": "1993 - Jan",
          "option": "1993-jan"
        },
        {
          "dimension": "time",
          "label": "1992",
          "option": "1992"
        },
        {
          "dimension": "time",
          "label": "1992 - Q4",
          "option": "1992-q4"
        },
        {
          "dimension": "time",
          "label": "1992 - Q3",
          "option": "1992-q3"
        },
        {
          "dimension": "time",
          "label": "1992 - Q2",
          "option": "1992-q2"
        },
        {
          "dimension": "time",
          "label": "1992 - Q1",
          "option": "1992-q1"
        },
        {
          "dimension": "time",
          "label": "1992 - Dec",
          "option": "1992-dec"
        },
        {
          "dimension": "time",
          "label": "1992 - Nov",
          "option": "1992-nov"
        },
        {
          "dimension": "time",
          "label": "1992 - Oct",
          "option": "1992-oct"
        },
        {
          "dimension": "time",
          "label": "1992 - Sep",
          "option": "1992-sep"
        },
        {
          "dimension": "time",
          "label": "1992 - Aug",
          "option": "1992-aug"
        },
        {
          "dimension": "time",
          "label": "1992 - Jul",
          "option": "1992-jul"
        },
        {
          "dimension": "time",
          "label": "1992 - Jun",
          "option": "1992-jun"
        },
        {
          "dimension": "time",
          "label": "1992 - May",
          "option": "1992-may"
        },
        {
          "dimension": "time",
          "label": "1992 - Apr",
          "option": "1992-apr"
        },
        {
          "dimension": "time",
          "label": "1992 - Mar",
          "option": "1992-mar"
        },
        {
          "dimension": "time",
          "label": "1992 - Feb",
          "option": "1992-feb"
        },
        {
          "dimension": "time",
          "label": "1992 - Jan",
          "option": "1992-jan"
        },
        {
          "dimension": "time",
          "label": "1991",
          "option": "1991"
        },
        {
          "dimension": "time",
          "label": "1991 - Q4",
          "option": "1991-q4"
        },
        {
          "dimension": "time",
          "label": "1991 - Q3",
          "option": "1991-q3"
        },
        {
          "dimension": "time",
          "label": "1991 - Q2",
          "option": "1991-q2"
        },
        {
          "dimension": "time",
          "label": "1991 - Q1",
          "option": "1991-q1"
        },
        {
          "dimension": "time",
          "label": "1991 - Dec",
          "option": "1991-dec"
        },
        {
          "dimension": "time",
          "label": "1991 - Nov",
          "option": "1991-nov"
        },
        {
          "dimension": "time",
          "label": "1991 - Oct",
          "option": "1991-oct"
        },
        {
          "dimension": "time",
          "label": "1991 - Sep",
          "option": "1991-sep"
        },
        {
          "dimension": "time",
          "label": "1991 - Aug",
          "option": "1991-aug"
        },
        {
          "dimension": "time",
          "label": "1991 - Jul",
          "option": "1991-jul"
        },
        {
          "dimension": "time",
          "label": "1991 - Jun",
          "option": "1991-jun"
        },
        {
          "dimension": "time",
          "label": "1991 - May",
          "option": "1991-may"
        },
        {
          "dimension": "time",
          "label": "1991 - Apr",
          "option": "1991-apr"
        },
        {
          "dimension": "time",
          "label": "1991 - Mar",
          "option": "1991-mar"
        },
        {
          "dimension": "time",
          "label": "1991 - Feb",
          "option": "1991-feb"
        },
        {
          "dimension": "time",
          "label": "1991 - Jan",
          "option": "1991-jan"
        },
        {
          "dimension": "time",
          "label": "1990",
          "option": "1990"
        },
        {
          "dimension": "time",
          "label": "1990 - Q4",
          "option": "1990-q4"
        },
        {
          "dimension": "time",
          "label": "1990 - Q3",
          "option": "1990-q3"
        },
        {
          "dimension": "time",
          "label": "1990 - Q2",
          "option": "1990-q2"
        },
        {
          "dimension": "time",
          "label": "1990 - Q1",
          "option": "1990-q1"
        },
        {
          "dimension": "time",
          "label": "1990 - Dec",
          "option": "1990-dec"
        },
        {
          "dimension": "time",
          "label": "1990 - Nov",
          "option": "1990-nov"
        },
        {
          "dimension": "time",
          "label": "1990 - Oct",
          "option": "1990-oct"
        },
        {
          "dimension": "time",
          "label": "1990 - Sep",
          "option": "1990-sep"
        },
        {
          "dimension": "time",
          "label": "1990 - Aug",
          "option": "1990-aug"
        },
        {
          "dimension": "time",
          "label": "1990 - Jul",
          "option": "1990-jul"
        },
        {
          "dimension": "time",
          "label": "1990 - Jun",
          "option": "1990-jun"
        },
        {
          "dimension": "time",
          "label": "1990 - May",
          "option": "1990-may"
        },
        {
          "dimension": "time",
          "label": "1990 - Apr",
          "option": "1990-apr"
        },
        {
          "dimension": "time",
          "label": "1990 - Mar",
          "option": "1990-mar"
        },
        {
          "dimension": "time",
          "label": "1990 - Feb",
          "option": "1990-feb"
        },
        {
          "dimension": "time",
          "label": "1990 - Jan",
          "option": "1990-jan"
        },
        {
          "dimension": "time",
          "label": "1989",
          "option": "1989"
        },
        {
          "dimension": "time",
          "label": "1989 - Q4",
          "option": "1989-q4"
        },
        {
          "dimension": "time",
          "label": "1989 - Q3",
          "option": "1989-q3"
        },
        {
          "dimension": "time",
          "label": "1989 - Q2",
          "option": "1989-q2"
        },
        {
          "dimension": "time",
          "label": "1989 - Q1",
          "option": "1989-q1"
        },
        {
          "dimension": "time",
          "label": "1989 - Dec",
          "option": "1989-dec"
        },
        {
          "dimension": "time",
          "label": "1989 - Nov",
          "option": "1989-nov"
        },
        {
          "dimension": "time",
          "label": "1989 - Oct",
          "option": "1989-oct"
        },
        {
          "dimension": "time",
          "label": "1989 - Sep",
          "option": "1989-sep"
        },
        {
          "dimension": "time",
          "label": "1989 - Aug",
          "option": "1989-aug"
        },
        {
          "dimension": "time",
          "label": "1989 - Jul",
          "option": "1989-jul"
        },
        {
          "dimension": "time",
          "label": "1989 - Jun",
          "option": "1989-jun"
        },
        {
          "dimension": "time",
          "label": "1989 - May",
          "option": "1989-may"
        },
        {
          "dimension": "time",
          "label": "1989 - Apr",
          "option": "1989-apr"
        },
        {
          "dimension": "time",
          "label": "1989 - Mar",
          "option": "1989-mar"
        },
        {
          "dimension": "time",
          "label": "1989 - Feb",
          "option": "1989-feb"
        },
        {
          "dimension": "time",
          "label": "1989 - Jan",
          "option": "1989-jan"
        },
        {
          "dimension": "time",
          "label": "1988",
          "option": "1988"
        },
        {
          "dimension": "time",
          "label": "1988 - Q4",
          "option": "1988-q4"
        },
        {
          "dimension": "time",
          "label": "1988 - Q3",
          "option": "1988-q3"
        },
        {
          "dimension": "time",
          "label": "1988 - Q2",
          "option": "1988-q2"
        },
        {
          "dimension": "time",
          "label": "1988 - Q1",
          "option": "1988-q1"
        },
        {
          "dimension": "time",
          "label": "1988 - Dec",
          "option": "1988-dec"
        },
        {
          "dimension": "time",
          "label": "1988 - Nov",
          "option": "1988-nov"
        },
        {
          "dimension": "time",
          "label": "1988 - Oct",
          "option": "1988-oct"
        },
        {
          "dimension": "time",
          "label": "1988 - Sep",
          "option": "1988-sep"
        },
        {
          "dimension": "time",
          "label": "1988 - Aug",
          "option": "1988-aug"
        },
        {
          "dimension": "time",
          "label": "1988 - Jul",
          "option": "1988-jul"
        },
        {
          "dimension": "time",
          "label": "1988 - Jun",
          "option": "1988-jun"
        },
        {
          "dimension": "time",
          "label": "1988 - May",
          "option": "1988-may"
        },
        {
          "dimension": "time",
          "label": "1988 - Apr",
          "option": "1988-apr"
        },
        {
          "dimension": "time",
          "label": "1988 - Mar",
          "option": "1988-mar"
        },
        {
          "dimension": "time",
          "label": "1988 - Feb",
          "option": "1988-feb"
        },
        {
          "dimension": "time",
          "label": "1988 - Jan",
          "option": "1988-jan"
        }
      ],
      "reportedTotal": 647,
      "retrievedUnique": 647,
      "stableReportedTotal": true,
      "stopReason": "exhausted"
    },
    "version": "45",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/retail-sales-index-large-and-small-businesses/editions/time-series/versions/45"
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-M"
  }
}
---

# Retail sales index - large and small businesses

Value and volume of retail sales broken down by size of business

Native identifier: `retail-sales-index-large-and-small-businesses`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/retail-sales-index-large-and-small-businesses/editions/time-series/versions/45)

Update cadence: Monthly.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
