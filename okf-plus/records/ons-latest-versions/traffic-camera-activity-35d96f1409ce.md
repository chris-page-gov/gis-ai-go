---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/traffic-camera-activity",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Traffic Camera Activity",
  "description": "Experimental dataset for business indices covering the UK as part of the real-time indicators release to help better understand economic activity and social change in the UK.",
  "nativeIdentifier": "traffic-camera-activity",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/traffic-camera-activity/editions/time-series/versions/105",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/traffic-camera-activity/editions/time-series/versions/105/metadata",
      "retrievedAt": "2026-10-02T01:30:31.603404Z",
      "responseSha256": "09c439bda08f74fb71341c2dca9f8d30ff6ec2b6707e4895f29acc488c95ad19",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/8",
      "normalisedRecordSha256": "e5275e33d57e6b47dd8543e6099439bb726e3a85d576b9f2a6a491c4850cb1be",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/traffic-camera-activity/editions/time-series/versions/105"
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
    "metadataModified": "2024-06-20T09:00:45.082Z",
    "releaseVersion": "105"
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
        "description": "Because of faulty or missing camera images, there are high levels of imputation in the following areas and periods: All regions 25 April 2021 London 27 to 28 April 2021, 4 July 2021, 21 to 22 September 2021, 5 October 2021, 1 to 5 January 2022, 5 September 2022, 9 September 2022, 21 September 2022, 13 October 2022, 24 October 2022, 12 December 2022 to 19 February 2023, 4 to 5 April 2023, 16 to 18 April 2023, 25 September 2023, 27 to 28 September 2023, 7 November 2023, 20-21 March 2024, 2 May 2024, 9 May 2024 to 10 May 2024, 14 May 2024 to 16 May 2024, 22 May 2024 The North East 2 May 2021, 11 to 12 May 2021, 15 June 2021, 17 June 2021, 19 June 2021, 9 to 13 August 2021, 27 to 29 August 2021, 4 to 5 October 2021, 16 to 17 October 2021, 1 to 7 November 2021, 11 November 2021, 17 November 2021, 6 December 2021, 20 December 2021, 20 January 2022, 25 January 2022, 28 January 2022, 9 February 2022, 9 to 10 March 2022, 15 March 2022, 21 March 2022, 23 March 2022, 28 March to 3 April 2022, 4 April 2022, 10 April 2022, 25 April to 1 May 2022, 9 May 2022, 12 May 2022, 29 May 2022, 7 June 2022, 9 June 2022, 15 to 16 June 2022, 21 June 2022, 23 June 2022, 7 July 2022, 11 July 2022, 3 August 2022, 8 August 2022, 7 September 2022, 27 September 2022, 29-30 September 2022, 9 October 2022, 10 to 12 October 2022, 24 to 27 November 2022, 12 December 2022 to 19 February 2023, 24th April 2023, 4th May 2023, 15th to 16th May 2023, 15th to 20th June 2023, 23rd June 2023, 1 to 2 July 2023, 5 July 2023, 19th July 2023, 21 July 2023, 25 July 2023 to 17 August 2023, 19 August 2023, 24 August to 4 October 2023, 21 November 2023, 29 to 30 November 2023, 3 December 2023, 16 December 2023, 23 December 2023, 30 December 2023, 6 January 2024, 13 to 14 January 2024, 20 January 2024, 27 to 29 January 2024, 6 to 7 February 2024, 10 February 2024, 14 February 2024, 17 February 2024, 24 February 2024, 26 February 2024, 2 March 2024, 9th March 2024, 13 to 14 March 2024, 16 March 2024, 23 March 2024, 25 March 2024, 29 to 30 March 2024, 6 April 2024, 13 April 2024, 20 April 2024, 27 April 2024 Northern Ireland 6 March, 11 April 2021, 29 April 2021, 6 to 7 May 2021, 18 June 2021, 20 June to 1 July 2021, 4 July 2021, 16 August 2021, 11 to 14 April 2022, 16 to 22 May 2022, 6 June 2022, 1 May 2023 to 10 January 2024, 25 to 26 March 2024, 28 April 2024, 4 May 2024 Please note that data in Northern Ireland was unavailable for the period 24 to 30 April 2023. Southend 15 to 16 May 2021, 18 May, 20 to 27 May 2021, 12 to 14 June 2021, 28 June 2021 to 28 November 2021, 29 November to 4 December 2021, 21 to 27 March 2022, 4 April to 21 June 2022. Please note that data in Southend was unavailable for the period 28 March to 3 April 2022, and since 22 June 2022 onwards. Greater Manchester 17 to 22 February 2021, 25 to 26 February 2021, 3 to 11 March 2021, 27 to 29 April 2021, 4 to 6 June 2021, 13 June 2021, 4 July 2021, 15 July 2021, 3 August 2021, 24 August 2021, 5 November 2021, 20 to 22 December 2021, 31 January 2022, 22 February 2022, 4 March 2022, 30 March 2022, 1 April 2022, 12 to 17 April 2022, 26 to 27 May 2022, 19 July 2022, 24 September 2022, 27 to 28 October 2022, 2 to 3 November 2022, 25 November 2022, 5 February 2023, 8 February 2023, 25 to 27 February 2023, 1 to 2 March 2023, 4 to 5 April 2023, 6 to 11 September 2023, 31 October 2023, 1 November 2023, 9 to 10 November 2023, 13 November 2023, 12 to 13 December 2023, 20 to 21 December 2023, 5 February 2024 to 10 March 2024, 2 April 2024 to 5 April 2024, 14 April 2024 to 28 April 2024. Reading 15 February to 14 March 2021, 5 to 18 April 2021, 30 April 2021, 2 May 2021, 4 May 2021, 6 May 2021, 8 May 2021, 12 to 15 May 2021, 22 to 29 May, 5 to 9 June, 12 to 13 June, 17 to 23 July 2021, 27 to 29 July 2021, 5 to 6 August 2021, 4 to 8 September 2021, 10 September 2021, 18 to 22 September 2021, 25 to 28 September 2021, 2 to 3 October 2021, 6 to 11 October 2021, 16 to 22 October 2021, 26 to 31 October 2021, 1 November 2021, 6 to 11 November 2021, 13 to 21 November 2021, 27 November 2021. Please note that data in Reading has been unavailable since 28th November 2021 onwards. Traffic camera images capture the appearance of buses, but they give no indication of the number of passengers using public transport. A * indicates this time point is outside the time series. A # indicates data have been suppressed. A Δ indicates data have been excluded due to reliability issues.",
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
        "id": "traffic-camera-area",
        "label": "Traffic camera area",
        "name": "trafficcameraarea"
      },
      {
        "id": "pedestrians-and-vehicles",
        "label": "Pedestrians and vehicles",
        "name": "pedestriansandvehicles"
      },
      {
        "id": "seasonal-adjustment",
        "label": "Seasonal adjustment",
        "name": "seasonaladjustment"
      }
    ],
    "edition": "time-series",
    "id": "traffic-camera-activity",
    "metadata": {
      "description": "Experimental dataset for business indices covering the UK as part of the real-time indicators release to help better understand economic activity and social change in the UK.",
      "last_updated": "2024-06-20T09:00:45.082Z",
      "next_release": "To be announced",
      "release_date": "2024-06-20T00:00:00.000Z",
      "release_frequency": "Weekly",
      "state": "published",
      "title": "Traffic Camera Activity",
      "type": "filterable"
    },
    "metadataContract": {
      "catalogueType": "filterable",
      "dimensionListPresent": true,
      "identityEvidence": {
        "edition": "time-series",
        "id": "traffic-camera-activity",
        "version": 105
      },
      "variant": "filterable-scalar-identity"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:30:31.603404Z",
      "sha256": "09c439bda08f74fb71341c2dca9f8d30ff6ec2b6707e4895f29acc488c95ad19",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/traffic-camera-activity/editions/time-series/versions/105/metadata"
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
    "version": "105",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/traffic-camera-activity/editions/time-series/versions/105"
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

# Traffic Camera Activity

Experimental dataset for business indices covering the UK as part of the real-time indicators release to help better understand economic activity and social change in the UK.

Native identifier: `traffic-camera-activity`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/traffic-camera-activity/editions/time-series/versions/105)

Update cadence: Weekly.
Temporal evidence: normalised-source-options (available-native-period-options); start 2020, end 2024.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
