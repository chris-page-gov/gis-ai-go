---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/RM028",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Ethnic group by occupancy rating (bedrooms)",
  "description": "This dataset provides Census 2021 estimates that classify usual residents in households in England and Wales by ethnic group and by occupancy rating (bedrooms). The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM028",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM028",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "ethnic_group_tb_8a,occupancy_rating_bedrooms_5a"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=300",
      "retrievedAt": "2026-10-02T01:18:03.582092Z",
      "responseSha256": "49f3fe8ddc5f16a3c2801331f3e03dcac39702fa0a6d3b856b562bcc92dec23b",
      "sourcePointer": "/items/14",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/314",
      "normalisedRecordSha256": "88f7706f5c3188a45671d1299ef5dbdafde6c4e939ce15445bd7a7a4526062d2",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM028/editions/2021/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:35:23.227041Z",
      "responseSha256": "115bb852953a09e9d343551873d65ee8c2ef78a03e7dd3399eda960a7a816dc4",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/314",
      "normalisedRecordSha256": "a9045ed17d2cb0bd0b5357cdcc3640c06cd9f12f97ac8850f0c254ae15e1003b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM028"
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
    "nextRelease": null,
    "metadataModified": "2023-03-28T08:30:08.54Z",
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
    "description": "This dataset provides Census 2021 estimates that classify usual residents in households in England and Wales by ethnic group and by occupancy rating (bedrooms). The estimates are as at Census Day, 21 March 2021.",
    "id": "RM028",
    "keywords": [
      "ltla",
      "ethnic_group_tb_8a,occupancy_rating_bedrooms_5a"
    ],
    "last_updated": "2023-03-28T08:30:08.54Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM028/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM028/editions/2021/versions/1",
        "id": "1"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM028"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "Ethnic group by occupancy rating (bedrooms)",
    "type": "cantabular_multivariate_table",
    "unit_of_measure": "Person",
    "timeMetadata": {
      "dimensions": [
        {
          "description": "Lower tier local authorities provide a range of local services. There are 309 lower tier local authorities in England made up of 181 non-metropolitan districts, 59 unitary authorities, 36 metropolitan districts and 33 London boroughs (including City of London). In Wales there are 22 local authorities made up of 22 unitary authorities.",
          "id": "ltla",
          "label": "Lower tier local authorities",
          "name": "ltla"
        },
        {
          "description": "The ethnic group that the person completing the census feels they belong to. This could be based on their culture, family background, identity or physical appearance. Respondents could choose one out of 19 tick-box response categories, including write-in response options.",
          "id": "ethnic_group_tb_8a",
          "label": "Ethnic group (8 categories)",
          "name": "ethnic_group_tb_8a"
        },
        {
          "description": "Whether a household's accommodation is overcrowded, ideally occupied or under-occupied. This is calculated by comparing the number of bedrooms the household requires to the number of available bedrooms. The number of bedrooms the household requires is calculated according to the Bedroom Standard, where the following should have their own bedroom: 1. adult couple 2. any remaining adult (aged 21 years or over) 3. two males (aged 10 to 20 years) 4. one male (aged 10 to 20 years) and one male (aged 9 years or under), if there are an odd number of males aged 10-20 5. one male aged 10-20 if there are no males aged 0-9 to pair with him. 6. repeat steps 3-5 for females 7. two children (aged 9 years or under) regardless of sex 8. any remaining child (aged 9 years or under) An occupancy rating of: * -1 or less implies that a household’s accommodation has fewer bedrooms than required (overcrowded) * +1 or more implies that a household’s accommodation has more bedrooms than required (under-occupied) * 0 suggests that a household’s accommodation has an ideal number of bedrooms",
          "id": "occupancy_rating_bedrooms_5a",
          "label": "Occupancy rating for bedrooms (5 categories)",
          "name": "occupancy_rating_bedrooms_5a"
        }
      ],
      "edition": "2021",
      "id": "RM028",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents in households in England and Wales by ethnic group and by occupancy rating (bedrooms). The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2023-03-28T00:00:00.000Z",
        "state": "published",
        "title": "Ethnic group by occupancy rating (bedrooms)",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_multivariate_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM028/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM028/editions/2021/versions/1",
              "id": "1"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM028"
            }
          },
          "isBasedOn": {
            "@id": "UR_HH",
            "@type": "cantabular_multivariate_table"
          }
        },
        "variant": "cantabular-dataset-links"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:35:23.227041Z",
        "sha256": "115bb852953a09e9d343551873d65ee8c2ef78a03e7dd3399eda960a7a816dc4",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/RM028/editions/2021/versions/1/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "1",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM028/editions/2021/versions/1"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM028/editions"
  }
}
---

# Ethnic group by occupancy rating (bedrooms)

This dataset provides Census 2021 estimates that classify usual residents in households in England and Wales by ethnic group and by occupancy rating (bedrooms). The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM028`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM028)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
