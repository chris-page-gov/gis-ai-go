---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/older-people-economic-activity",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Local authority ageing statistics, older people economic activity",
  "description": "Indicators included are economic activity and employment rates for those aged 50-64 years, by country, region and local authority. Both economic activity and employment rates are displayed as percentages. These have been calculated from the ONS Annual Population Survey and have been extracted from NOMIS. https://www.nomisweb.co.uk/ This dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which will be published in July 2020. The tool will be interactive, and users will be able to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. Note on update frequency: NOMIS provide quarterly updates on both indicators. For consistency with other indicators presented in the subnational ageing tool, these will be updated on an annual basis.",
  "nativeIdentifier": "older-people-economic-activity",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/older-people-economic-activity",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ageing",
    "population"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=0",
      "retrievedAt": "2026-10-02T01:18:02.763023Z",
      "responseSha256": "569b4c5ce256d4d8fa3ab4f9592a32655c63cdb045ad28fdcda658680b15fccf",
      "sourcePointer": "/items/26",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/26",
      "normalisedRecordSha256": "3dd559a8b4917a2bd29b8ad0d600357fa07c83c5b26344099d4c12589c30c4a6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/older-people-economic-activity/editions/time-series/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:31:01.165564Z",
      "responseSha256": "5812db242f0ec519a937221591fbee76bbb41c768232361c2a37f482f52d7d28",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/26",
      "normalisedRecordSha256": "a47c6d90b7f454d248067d78117f64235a7377dfe8d642971a3987bb537afba2",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/older-people-economic-activity"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "2019",
    "end": "2019",
    "sourceField": "timeMetadata.temporal.options",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "year",
    "derivation": "ONS-native-ISO-period-code.v1"
  },
  "update": {
    "frequency": {
      "status": "source-stated",
      "label": "Quarterly but updated on CMD annually",
      "iri": null,
      "sourceField": "release_frequency"
    },
    "releaseCatalogue": [
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": "1 June 2021",
    "metadataModified": "2020-11-02T10:40:51.094Z",
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
    "description": "Indicators included are economic activity and employment rates for those aged 50-64 years, by country, region and local authority. Both economic activity and employment rates are displayed as percentages. These have been calculated from the ONS Annual Population Survey and have been extracted from NOMIS.\n\nhttps://www.nomisweb.co.uk/\n\nThis dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which will be published in July 2020. The tool will be interactive, and users will be able to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. \n\nNote on update frequency: NOMIS provide quarterly updates on both indicators. For consistency with other indicators presented in the subnational ageing tool, these will be updated on an annual basis.",
    "id": "older-people-economic-activity",
    "keywords": [
      "ageing",
      "population"
    ],
    "last_updated": "2020-11-02T10:40:51.094Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/older-people-economic-activity/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/older-people-economic-activity/editions/time-series/versions/1",
        "id": "1"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/older-people-economic-activity"
      },
      "taxonomy": {
        "href": "https://api.beta.ons.gov.uk/v1/peoplepopulationandcommunity/birthsdeathsandmarriages/ageing"
      }
    },
    "next_release": "1 June 2021",
    "qmi": {
      "href": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/methodologies/annualpopulationsurveyapsqmi"
    },
    "related_datasets": [
      {
        "href": "https://www.nomisweb.co.uk/",
        "title": "Link to NOMIS website"
      }
    ],
    "release_frequency": "Quarterly but updated on CMD annually",
    "state": "published",
    "title": "Local authority ageing statistics, older people economic activity",
    "timeMetadata": {
      "dimensions": [
        {
          "id": "calendar-years",
          "label": "Time",
          "name": "time"
        },
        {
          "description": "Data are available at a local authority, region and country level for England, Wales and Scotland.",
          "id": "administrative-geography",
          "label": "Geography",
          "name": "geography"
        },
        {
          "description": "Data are available for All Persons, Males and Females.",
          "id": "sex",
          "label": "Sex",
          "name": "sex"
        },
        {
          "description": "Economic activity and employment rates for those aged 50-64 years.",
          "id": "economic-activity",
          "label": "Economic activity",
          "name": "economicactivity"
        }
      ],
      "edition": "time-series",
      "id": "older-people-economic-activity",
      "metadata": {
        "description": "Indicators included are economic activity and employment rates for those aged 50-64 years, by country, region and local authority. Both economic activity and employment rates are displayed as percentages. These have been calculated from the ONS Annual Population Survey and have been extracted from NOMIS. https://www.nomisweb.co.uk/ This dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which will be published in July 2020. The tool will be interactive, and users will be able to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. Note on update frequency: NOMIS provide quarterly updates on both indicators. For consistency with other indicators presented in the subnational ageing tool, these will be updated on an annual basis.",
        "last_updated": "2020-11-02T10:40:51.094Z",
        "next_release": "1 June 2021",
        "release_date": "2020-06-30T00:00:00.000Z",
        "release_frequency": "Quarterly but updated on CMD annually",
        "state": "published",
        "title": "Local authority ageing statistics, older people economic activity"
      },
      "metadataContract": {
        "catalogueType": null,
        "dimensionListPresent": true,
        "identityEvidence": {
          "edition": "time-series",
          "id": "older-people-economic-activity",
          "version": 1
        },
        "variant": "filterable-scalar-identity"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:31:01.165564Z",
        "sha256": "5812db242f0ec519a937221591fbee76bbb41c768232361c2a37f482f52d7d28",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/older-people-economic-activity/editions/time-series/versions/1/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "bounds": {
          "basis": "published time-dimension option codes; no observations",
          "comparisonRule": "ONS-native-ISO-period-code.v1",
          "continuityEstablished": false,
          "granularity": "year",
          "maximumNative": "2019",
          "minimumNative": "2019",
          "status": "known-option-extrema"
        },
        "complete": true,
        "duplicateCount": 0,
        "options": [
          {
            "dimension": "time",
            "label": "2019",
            "option": "2019"
          }
        ],
        "reportedTotal": 1,
        "retrievedUnique": 1,
        "stableReportedTotal": true,
        "stopReason": "exhausted"
      },
      "version": "1",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/older-people-economic-activity/editions/time-series/versions/1"
    }
  },
  "dcterms:accrualPeriodicity": {
    "@type": "dcterms:Frequency",
    "rdfs:label": "Quarterly but updated on CMD annually"
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/older-people-economic-activity/editions"
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "published time-dimension option codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": "2019",
      "minimumNative": "2019",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# Local authority ageing statistics, older people economic activity

Indicators included are economic activity and employment rates for those aged 50-64 years, by country, region and local authority. Both economic activity and employment rates are displayed as percentages. These have been calculated from the ONS Annual Population Survey and have been extracted from NOMIS. https://www.nomisweb.co.uk/ This dataset has been produced by the Ageing Analysis Team for inclusion in a subnational ageing tool, which will be published in July 2020. The tool will be interactive, and users will be able to compare latest and projected measures of ageing for up to four different areas through selection on a map or from a drop-down menu. Note on update frequency: NOMIS provide quarterly updates on both indicators. For consistency with other indicators presented in the subnational ageing tool, these will be updated on an annual basis.

Native identifier: `older-people-economic-activity`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/older-people-economic-activity)

Update cadence: Quarterly but updated on CMD annually.
Temporal evidence: normalised-source-options (available-native-period-options); start 2019, end 2019.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
