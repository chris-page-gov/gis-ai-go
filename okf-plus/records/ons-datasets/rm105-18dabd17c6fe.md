---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/RM105",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Occupation by hours worked",
  "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in employment the week before the census in England and Wales by occupation and by hours worked. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM105",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM105",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "occupation_current_10a,hours_per_week_worked"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=200",
      "retrievedAt": "2026-10-02T01:18:03.316175Z",
      "responseSha256": "23965e57a732be944cd1c9954229e9957ca9a52c28b0632525da9642ff12011b",
      "sourcePointer": "/items/38",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/238",
      "normalisedRecordSha256": "c0383a128556c684cdf3dc58ff899b445bc3770c3036bd10dfe7321caf8fa481",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM105/editions/2021/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:34:19.699174Z",
      "responseSha256": "f5b165fa946a8b890e7ab1496b4cf8d21eb4f5ee3bbb90d4ca9fec12fbee3b0c",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/238",
      "normalisedRecordSha256": "1649d8e352bbe3c604e2a9ddb5d85ced389095384f8b6030f4f792e7fce9e520",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM105"
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
    "metadataModified": "2024-01-15T10:00:04.811Z",
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
    "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in employment the week before the census in England and Wales by occupation and by hours worked. The estimates are as at Census Day, 21 March 2021.",
    "id": "RM105",
    "keywords": [
      "ltla",
      "occupation_current_10a,hours_per_week_worked"
    ],
    "last_updated": "2024-01-15T10:00:04.811Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM105/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM105/editions/2021/versions/3",
        "id": "3"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM105"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "Occupation by hours worked",
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
          "description": "Classifies what people aged 16 years and over do as their main job. Their job title or details of activities they do in their job and any supervisory or management responsibilities form this classification. This information is used to code responses to an occupation using the Standard Occupational Classification (SOC) 2020. It classifies people who were in employment between 15 March and 21 March 2021, by the SOC code that represents their current occupation. The lowest level of detail available is the four-digit SOC code which includes all codes in three, two and one digit SOC code levels.",
          "id": "occupation_current_10a",
          "label": "Occupation (current) (10 categories)",
          "name": "occupation_current_10a"
        },
        {
          "description": "The number of hours worked per week before the census includes paid and unpaid overtime. This covers the main job of anyone aged 16 years and over.",
          "id": "hours_per_week_worked",
          "label": "Hours worked (5 categories)",
          "name": "hours_per_week_worked"
        }
      ],
      "edition": "2021",
      "id": "RM105",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in employment the week before the census in England and Wales by occupation and by hours worked. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2024-01-15T00:00:00.000Z",
        "state": "published",
        "title": "Occupation by hours worked",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_multivariate_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM105/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM105/editions/2021/versions/3",
              "id": "3"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM105"
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
        "retrievedAt": "2026-10-02T01:34:19.699174Z",
        "sha256": "f5b165fa946a8b890e7ab1496b4cf8d21eb4f5ee3bbb90d4ca9fec12fbee3b0c",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/RM105/editions/2021/versions/3/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "3",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM105/editions/2021/versions/3"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM105/editions"
  }
}
---

# Occupation by hours worked

This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in employment the week before the census in England and Wales by occupation and by hours worked. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM105`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM105)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
