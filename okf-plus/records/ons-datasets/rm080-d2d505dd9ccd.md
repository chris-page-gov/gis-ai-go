---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/RM080",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Multi-language households by ethnic group of Household Reference Person",
  "description": "This dataset provides Census 2021 estimates that classify Household Reference Persons in England and Wales by whether one or multiple languages are spoken, and by ethnic group. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM080",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM080",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "hh_multi_language,ethnic_group_tb_8a"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=200",
      "retrievedAt": "2026-10-02T01:18:03.316175Z",
      "responseSha256": "23965e57a732be944cd1c9954229e9957ca9a52c28b0632525da9642ff12011b",
      "sourcePointer": "/items/63",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/263",
      "normalisedRecordSha256": "fa271ca91c38f2bf678ee602e7ab4d30953746640f253823f67a0abbe0d97a57",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM080/editions/2021/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:34:40.579582Z",
      "responseSha256": "0ab3a6fff10faa8bd52ce2f1930ae14008792c5fdaa7a274215a5569879025e7",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/263",
      "normalisedRecordSha256": "1e6f8ce4a36dd8bceb146de6cf27f3583ceeef5004ffb465e5100cd31473bac9",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM080"
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
    "metadataModified": "2023-03-28T08:30:08.962Z",
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
    "description": "This dataset provides Census 2021 estimates that classify Household Reference Persons in England and Wales by whether one or multiple languages are spoken, and by ethnic group. The estimates are as at Census Day, 21 March 2021.",
    "id": "RM080",
    "keywords": [
      "ltla",
      "hh_multi_language,ethnic_group_tb_8a"
    ],
    "last_updated": "2023-03-28T08:30:08.962Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM080/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM080/editions/2021/versions/1",
        "id": "1"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM080"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "Multi-language households by ethnic group of Household Reference Person",
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
          "description": "Classifies households by whether members speak the same or different main language. If multiple main languages are spoken, this identifies whether they differ between generations or partnerships within the household.",
          "id": "hh_multi_language",
          "label": "Multiple main languages in household (6 categories)",
          "name": "hh_multi_language"
        },
        {
          "description": "The ethnic group that the person completing the census feels they belong to. This could be based on their culture, family background, identity or physical appearance. Respondents could choose one out of 19 tick-box response categories, including write-in response options.",
          "id": "ethnic_group_tb_8a",
          "label": "Ethnic group (8 categories)",
          "name": "ethnic_group_tb_8a"
        }
      ],
      "edition": "2021",
      "id": "RM080",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify Household Reference Persons in England and Wales by whether one or multiple languages are spoken, and by ethnic group. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2023-03-28T00:00:00.000Z",
        "state": "published",
        "title": "Multi-language households by ethnic group of Household Reference Person",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_multivariate_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM080/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM080/editions/2021/versions/1",
              "id": "1"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM080"
            }
          },
          "isBasedOn": {
            "@id": "HRP",
            "@type": "cantabular_multivariate_table"
          }
        },
        "variant": "cantabular-dataset-links"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:34:40.579582Z",
        "sha256": "0ab3a6fff10faa8bd52ce2f1930ae14008792c5fdaa7a274215a5569879025e7",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/RM080/editions/2021/versions/1/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "1",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM080/editions/2021/versions/1"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM080/editions"
  }
}
---

# Multi-language households by ethnic group of Household Reference Person

This dataset provides Census 2021 estimates that classify Household Reference Persons in England and Wales by whether one or multiple languages are spoken, and by ethnic group. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM080`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM080)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
