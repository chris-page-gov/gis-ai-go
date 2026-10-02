---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/suicides-in-the-uk",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Suicide registrations in England and Wales by local authority",
  "description": "Number of suicides by local authority in England and Wales, registered from 2001. If you are struggling to cope, please call Samaritans for free on 116 123 (UK and ROI) or contact other sources of support, such as those listed on the NHS’s help for suicidal thoughts webpage. Support is available round the clock, every single day of the year, providing a safe place for anyone struggling to cope, whoever they are, however they feel, whatever life has done to them.",
  "nativeIdentifier": "suicides-in-the-uk",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/suicides-in-the-uk",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "suicide",
    "mortality"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/11",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/11",
      "normalisedRecordSha256": "c23992e2615ae1f7e5803d64aa311bd6f77fa7aaac752406321e9a392e127bad",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/suicides-in-the-uk/editions/2023/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:30:36.624481Z",
      "responseSha256": "4a9ad07c33bdb81221f78d6901f321d651dc9ae3338677c632d9210733ff0449",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/11",
      "normalisedRecordSha256": "0c43c2b368ae39f34632e44f891b690e5036ccb7dcf9df171a89136fd5f04228",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/suicides-in-the-uk"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2001",
    "end": "2023",
    "sourceField": "timeMetadata.temporal.options",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "year",
    "derivation": "ONS-native-ISO-period-code.v1"
  },
  "update": {
    "frequency": {
      "status": "source-stated",
      "label": "Annually",
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
    "metadataModified": "2024-09-05T12:10:34.352Z",
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
    "description": "Number of suicides by local authority in England and Wales, registered from 2001.\n\nIf you are struggling to cope, please call Samaritans for free on 116 123 (UK and ROI) or contact other sources of support, such as those listed on the NHS’s help for suicidal thoughts webpage. Support is available round the clock, every single day of the year, providing a safe place for anyone struggling to cope, whoever they are, however they feel, whatever life has done to them.",
    "id": "suicides-in-the-uk",
    "keywords": [
      "suicide",
      "mortality"
    ],
    "last_updated": "2024-09-05T12:10:34.352Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/suicides-in-the-uk/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/suicides-in-the-uk/editions/2023/versions/1",
        "id": "1"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/suicides-in-the-uk"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths"
      }
    },
    "methodologies": [
      {
        "href": "https://www.samaritans.org/",
        "title": "Samaritans"
      },
      {
        "href": "https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/behaviours/help-for-suicidal-thoughts/",
        "title": "Help for suicidal thoughts"
      }
    ],
    "national_statistic": true,
    "next_release": "To be announced",
    "qmi": {
      "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/methodologies/suicideratesintheukqmi"
    },
    "related_datasets": [
      {
        "href": "https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/bulletins/suicidesintheunitedkingdom/latest",
        "title": "Suicides in England and Wales"
      }
    ],
    "release_frequency": "Annually",
    "state": "published",
    "title": "Suicide registrations in England and Wales by local authority",
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
        }
      ],
      "edition": "2023",
      "id": "suicides-in-the-uk",
      "metadata": {
        "description": "Number of suicides by local authority in England and Wales, registered from 2001. If you are struggling to cope, please call Samaritans for free on 116 123 (UK and ROI) or contact other sources of support, such as those listed on the NHS’s help for suicidal thoughts webpage. Support is available round the clock, every single day of the year, providing a safe place for anyone struggling to cope, whoever they are, however they feel, whatever life has done to them.",
        "last_updated": "2024-09-05T12:10:34.352Z",
        "next_release": "To be announced",
        "release_date": "2024-08-29T00:00:00.000Z",
        "release_frequency": "Annually",
        "state": "published",
        "title": "Suicide registrations in England and Wales by local authority"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "2023",
          "id": "suicides-in-the-uk",
          "version": 1
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:30:36.624481Z",
        "sha256": "4a9ad07c33bdb81221f78d6901f321d651dc9ae3338677c632d9210733ff0449",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/suicides-in-the-uk/editions/2023/versions/1/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2023",
          "minimumNative": "2001",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
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
          }
        ],
        "reportedTotal": 23,
        "retrievedUnique": 23,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "1",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/suicides-in-the-uk/editions/2023/versions/1"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@id": "http://purl.org/linked-data/sdmx/2009/code#freq-A"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/suicides-in-the-uk/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2023",
      "minimumNative": "2001",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Suicide registrations in England and Wales by local authority

Number of suicides by local authority in England and Wales, registered from 2001. If you are struggling to cope, please call Samaritans for free on 116 123 (UK and ROI) or contact other sources of support, such as those listed on the NHS’s help for suicidal thoughts webpage. Support is available round the clock, every single day of the year, providing a safe place for anyone struggling to cope, whoever they are, however they feel, whatever life has done to them.

Native identifier: `suicides-in-the-uk`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/suicides-in-the-uk)

Update cadence: Annually.
Temporal evidence: normalised-source-options (available-native-period-options); start 2001, end 2023.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
