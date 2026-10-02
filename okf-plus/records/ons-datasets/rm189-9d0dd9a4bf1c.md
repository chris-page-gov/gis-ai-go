---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/RM189",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Sexual orientation by sex",
  "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales, by sexual orientation and sex. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM189",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM189",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "sexual_orientation_6a,sex"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=100",
      "retrievedAt": "2026-10-02T01:18:03.044616Z",
      "responseSha256": "57e4e2bdf76ce87eb7454338471def5f4540c0d91439e9ea0bbfae1b77ef302b",
      "sourcePointer": "/items/55",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/155",
      "normalisedRecordSha256": "f9ae7dd1ae5350b5c04b8908868b79f131dcf30e16e786136bffd1a197bbd08f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM189/editions/2021/versions/4/metadata",
      "retrievedAt": "2026-10-02T01:33:10.102964Z",
      "responseSha256": "4e43b667fb694fc7170fd761fa7837a4952f4e6fdb25e2d1793dad9563fd4b88",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/155",
      "normalisedRecordSha256": "2fccdbc4a453003919f002c0ab57e4d6534a0e0c74872e9fcc3ef351be4f7c5d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM189"
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
    "metadataModified": "2024-01-15T10:00:05.036Z",
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
    "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales, by sexual orientation and sex. The estimates are as at Census Day, 21 March 2021.",
    "id": "RM189",
    "keywords": [
      "ltla",
      "sexual_orientation_6a,sex"
    ],
    "last_updated": "2024-01-15T10:00:05.036Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM189/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM189/editions/2021/versions/4",
        "id": "4"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM189"
      }
    },
    "national_statistic": true,
    "qmi": {},
    "state": "published",
    "title": "Sexual orientation by sex",
    "type": "cantabular_flexible_table",
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
          "description": "Classifies people according to the responses to the sexual orientation question. This question was voluntary and was only asked of people aged 16 years and over.",
          "id": "sexual_orientation_6a",
          "label": "Sexual orientation (6 categories)",
          "name": "sexual_orientation_6a"
        },
        {
          "description": "This is the sex recorded by the person completing the census. The options were “Female” and “Male”.",
          "id": "sex",
          "label": "Sex (2 categories)",
          "name": "sex"
        }
      ],
      "edition": "2021",
      "id": "RM189",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales, by sexual orientation and sex. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2024-01-15T00:00:00.000Z",
        "state": "published",
        "title": "Sexual orientation by sex",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_flexible_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM189/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM189/editions/2021/versions/4",
              "id": "4"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM189"
            }
          },
          "isBasedOn": {
            "@id": "atc-rm-sogi-ur16o-ct-ltla",
            "@type": "cantabular_flexible_table"
          }
        },
        "variant": "cantabular-dataset-links"
      },
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T01:33:10.102964Z",
        "sha256": "4e43b667fb694fc7170fd761fa7837a4952f4e6fdb25e2d1793dad9563fd4b88",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/RM189/editions/2021/versions/4/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "4",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM189/editions/2021/versions/4"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM189/editions"
  }
}
---

# Sexual orientation by sex

This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales, by sexual orientation and sex. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM189`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM189)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
