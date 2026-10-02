---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/RM017",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Economic activity status by country of birth",
  "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales by economic activity status and by country of birth. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM017",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM017",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "economic_activity_status_10a,country_of_birth_13a"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=300",
      "retrievedAt": "2026-10-02T01:18:03.582092Z",
      "responseSha256": "49f3fe8ddc5f16a3c2801331f3e03dcac39702fa0a6d3b856b562bcc92dec23b",
      "sourcePointer": "/items/25",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/325",
      "normalisedRecordSha256": "c65d245453ef8232e516457d7b4660059f38129f3ac9f5f4a4eb2a06ba8fa336",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM017/editions/2021/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:35:32.433620Z",
      "responseSha256": "f6ed546b85e72cf74958095d2cd0c2e5e0d89aaacb586f78f40317458b59e309",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/325",
      "normalisedRecordSha256": "c499eda075f66be62708d041b7033196cc5720ed0da323886aa9b689a2b984c2",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM017"
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
    "metadataModified": "2024-01-15T10:00:05.1Z",
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
    "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales by economic activity status and by country of birth. The estimates are as at Census Day, 21 March 2021.",
    "id": "RM017",
    "keywords": [
      "ltla",
      "economic_activity_status_10a,country_of_birth_13a"
    ],
    "last_updated": "2024-01-15T10:00:05.1Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM017/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM017/editions/2021/versions/3",
        "id": "3"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM017"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "Economic activity status by country of birth",
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
          "description": "People aged 16 years and over are economically active if, between 15 March and 21 March 2021, they were: * in employment (an employee or self-employed) * unemployed, but looking for work and could start within two weeks * unemployed, but waiting to start a job that had been offered and accepted It is a measure of whether or not a person was an active participant in the labour market during this period. Economically inactive are those aged 16 years and over who did not have a job between 15 March to 21 March 2021 and had not looked for work between 22 February to 21 March 2021 or could not start work within two weeks. The census definition differs from International Labour Organization definition used on the Labour Force Survey, so estimates are not directly comparable. This classification splits out full-time students from those who are not full-time students when they are employed or unemployed. It is recommended to sum these together to look at all of those in employment or unemployed, or to use the four category labour market classification, if you want to look at all those with a particular labour market status.",
          "id": "economic_activity_status_10a",
          "label": "Economic activity status (10 categories)",
          "name": "economic_activity_status_10a"
        },
        {
          "description": "The country in which a person was born. For people not born in one of the four countries of the UK or the Republic of Ireland, there was an option to select \"elsewhere\". People who selected \"elsewhere\" were asked to write in the current name for their country of birth.",
          "id": "country_of_birth_13a",
          "label": "Country of birth (13 categories)",
          "name": "country_of_birth_13a"
        }
      ],
      "edition": "2021",
      "id": "RM017",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales by economic activity status and by country of birth. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2024-01-15T00:00:00.000Z",
        "state": "published",
        "title": "Economic activity status by country of birth",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_multivariate_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM017/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM017/editions/2021/versions/3",
              "id": "3"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM017"
            }
          },
          "isBasedOn": {
            "@id": "UR",
            "@type": "cantabular_multivariate_table"
          }
        },
        "variant": "cantabular-dataset-links"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:35:32.433620Z",
        "sha256": "f6ed546b85e72cf74958095d2cd0c2e5e0d89aaacb586f78f40317458b59e309",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/RM017/editions/2021/versions/3/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "3",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM017/editions/2021/versions/3"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM017/editions"
  }
}
---

# Economic activity status by country of birth

This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales by economic activity status and by country of birth. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM017`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM017)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
