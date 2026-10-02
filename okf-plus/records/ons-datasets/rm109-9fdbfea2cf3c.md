---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/RM109",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Passports held by age",
  "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by passports held and by age. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM109",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM109",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "passports_all_18a,resident_age_6a"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=200",
      "retrievedAt": "2026-10-02T01:18:03.316175Z",
      "responseSha256": "23965e57a732be944cd1c9954229e9957ca9a52c28b0632525da9642ff12011b",
      "sourcePointer": "/items/34",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/234",
      "normalisedRecordSha256": "f56b2a30c399ac4cfd520af95a0bbfb0d5719bf99fdf9fecb4f5faa2584c7bfe",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM109/editions/2021/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:34:16.356406Z",
      "responseSha256": "0045a574ff24f4c27591c230e2bcb7f6494844e3c386170f016df4c4ee2dd4aa",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/234",
      "normalisedRecordSha256": "7266178988a9c3615325029cbcebdbe0fb9f312f29cc77f244e1aad6f7f3f946",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM109"
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
    "metadataModified": "2023-03-28T08:30:09.221Z",
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
    "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by passports held and by age. The estimates are as at Census Day, 21 March 2021.",
    "id": "RM109",
    "keywords": [
      "ltla",
      "passports_all_18a,resident_age_6a"
    ],
    "last_updated": "2023-03-28T08:30:09.221Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM109/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM109/editions/2021/versions/1",
        "id": "1"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM109"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "Passports held by age",
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
          "description": "All passports classifies a person according to the passport or passports they held at the time of the census. This included expired passports or travel documents people were entitled to renew. Where a person recorded having more than one passport, they were counted only once, categorised in the following priority order: 1. UK passport, 2. Irish passport, 3. Other passport.",
          "id": "passports_all_18a",
          "label": "Passports held (18 categories)",
          "name": "passports_all_18a"
        },
        {
          "description": "A person’s age on Census Day, 21 March 2021 in England and Wales. Infants aged under 1 year are classified as 0 years of age.",
          "id": "resident_age_6a",
          "label": "Age (6 categories)",
          "name": "resident_age_6a"
        }
      ],
      "edition": "2021",
      "id": "RM109",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by passports held and by age. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2023-03-28T00:00:00.000Z",
        "state": "published",
        "title": "Passports held by age",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_multivariate_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM109/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM109/editions/2021/versions/1",
              "id": "1"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM109"
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
        "retrievedAt": "2026-10-02T01:34:16.356406Z",
        "sha256": "0045a574ff24f4c27591c230e2bcb7f6494844e3c386170f016df4c4ee2dd4aa",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/RM109/editions/2021/versions/1/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "1",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM109/editions/2021/versions/1"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM109/editions"
  }
}
---

# Passports held by age

This dataset provides Census 2021 estimates that classify usual residents in England and Wales by passports held and by age. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM109`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM109)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
