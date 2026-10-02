---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/RM167",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Gender identity by highest qualification held",
  "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales, by gender identity and highest level of qualification. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM167",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM167",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "gender_identity_7a,highest_qualification"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=100",
      "retrievedAt": "2026-10-02T01:18:03.044616Z",
      "responseSha256": "57e4e2bdf76ce87eb7454338471def5f4540c0d91439e9ea0bbfae1b77ef302b",
      "sourcePointer": "/items/77",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/177",
      "normalisedRecordSha256": "46425eb1dc94489deb9b6fee5b1e38a5ab57deef05f4c1c470e31f41f24b4c64",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM167/editions/2021/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:33:28.532801Z",
      "responseSha256": "29999c851099e0204dead5004e8a2213fb46d73c5ceb28155a8b80f006e11a6a",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/177",
      "normalisedRecordSha256": "beb2affbfaa34516e46fd1d3675316d9f20858491a573b7e05609b4fc30549cc",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM167"
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
    "metadataModified": "2024-09-25T14:48:58.986Z",
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
    "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales, by gender identity and highest level of qualification. The estimates are as at Census Day, 21 March 2021.",
    "id": "RM167",
    "keywords": [
      "ltla",
      "gender_identity_7a,highest_qualification"
    ],
    "last_updated": "2024-09-25T14:48:58.986Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM167/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM167/editions/2021/versions/3",
        "id": "3"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM167"
      }
    },
    "national_statistic": false,
    "qmi": {},
    "state": "published",
    "title": "Gender identity by highest qualification held",
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
          "description": "Classifies people according to the responses to the gender identity question. This question was voluntary and was only asked of people aged 16 years and over.",
          "id": "gender_identity_7a",
          "label": "Gender identity (7 categories)",
          "name": "gender_identity_7a"
        },
        {
          "description": "The highest level of qualification is derived from the question asking people to indicate all qualifications held, or their nearest equivalent. This may include foreign qualifications where they were matched to the closest UK equivalent.",
          "id": "highest_qualification",
          "label": "Highest level of qualification (8 categories)",
          "name": "highest_qualification"
        }
      ],
      "edition": "2021",
      "id": "RM167",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales, by gender identity and highest level of qualification. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2023-04-28T00:00:00.000Z",
        "state": "published",
        "title": "Gender identity by highest qualification held",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_flexible_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM167/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM167/editions/2021/versions/3",
              "id": "3"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM167"
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
        "retrievedAt": "2026-10-02T01:33:28.532801Z",
        "sha256": "29999c851099e0204dead5004e8a2213fb46d73c5ceb28155a8b80f006e11a6a",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/RM167/editions/2021/versions/3/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "3",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM167/editions/2021/versions/3"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM167/editions"
  }
}
---

# Gender identity by highest qualification held

This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales, by gender identity and highest level of qualification. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM167`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM167)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
