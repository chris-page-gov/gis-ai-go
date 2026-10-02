---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-datasets/RM173",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Gender identity by religion",
  "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales, by gender identity and religion. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM173",
  "sourceFamily": "ons-datasets",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM173",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "ltla",
    "gender_identity_4a,religion_tb"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets?limit=100&offset=100",
      "retrievedAt": "2026-10-02T01:18:03.044616Z",
      "responseSha256": "57e4e2bdf76ce87eb7454338471def5f4540c0d91439e9ea0bbfae1b77ef302b",
      "sourcePointer": "/items/71",
      "normalisedSource": "okf-plus/source/ons-datasets.json",
      "normalisedPointer": "/records/171",
      "normalisedRecordSha256": "6f19df96b335c0f31f5c1b99a9f66b41f624604c42425aa85632f95fd0e69034",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM173/editions/2021/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:33:23.508722Z",
      "responseSha256": "b3d6cacaf9063364e927600ea8eb203d8966acdad1bedf13beb80cc219d759e2",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/171",
      "normalisedRecordSha256": "5f38ac7eda8a7e1887fbef29ad42a45f62b0043c85631c295b7213ac3a96ae4a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM173"
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
    "metadataModified": "2024-09-25T14:48:59.064Z",
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
    "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales, by gender identity and religion. The estimates are as at Census Day, 21 March 2021.",
    "id": "RM173",
    "keywords": [
      "ltla",
      "gender_identity_4a,religion_tb"
    ],
    "last_updated": "2024-09-25T14:48:59.064Z",
    "links": {
      "editions": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM173/editions"
      },
      "latest_version": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM173/editions/2021/versions/3",
        "id": "3"
      },
      "self": {
        "href": "https://api.beta.ons.gov.uk/v1/datasets/RM173"
      }
    },
    "national_statistic": false,
    "qmi": {},
    "state": "published",
    "title": "Gender identity by religion",
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
          "id": "gender_identity_4a",
          "label": "Gender identity (4 categories)",
          "name": "gender_identity_4a"
        },
        {
          "description": "The religion people connect or identify with (their religious affiliation), whether or not they practise or have belief in it. This question was voluntary and includes people who identified with one of 8 tick-box response options, including \"No religion\", alongside those who chose not to answer this question.",
          "id": "religion_tb",
          "label": "Religion (10 categories)",
          "name": "religion_tb"
        }
      ],
      "edition": "2021",
      "id": "RM173",
      "metadata": {
        "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales, by gender identity and religion. The estimates are as at Census Day, 21 March 2021.",
        "last_updated": "0001-01-01T00:00:00Z",
        "release_date": "2023-04-28T00:00:00.000Z",
        "state": "published",
        "title": "Gender identity by religion",
        "unit_of_measure": "Person"
      },
      "metadataContract": {
        "catalogueType": "cantabular_flexible_table",
        "dimensionListPresent": true,
        "identityEvidence": {
          "datasetLinks": {
            "editions": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM173/editions"
            },
            "latest_version": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM173/editions/2021/versions/3",
              "id": "3"
            },
            "self": {
              "href": "https://api.beta.ons.gov.uk/v1/datasets/RM173"
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
        "retrievedAt": "2026-10-02T01:33:23.508722Z",
        "sha256": "b3d6cacaf9063364e927600ea8eb203d8966acdad1bedf13beb80cc219d759e2",
        "status": 200,
        "url": "https://api.beta.ons.gov.uk/v1/datasets/RM173/editions/2021/versions/3/metadata"
      },
      "metadataStatus": "captured",
      "temporal": {
        "maximumNative": null,
        "minimumNative": null,
        "reason": "no-native-time-dimension",
        "status": "unknown"
      },
      "version": "3",
      "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM173/editions/2021/versions/3"
    }
  },
  "qb:structure": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM173/editions"
  }
}
---

# Gender identity by religion

This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales, by gender identity and religion. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM173`.

Source family: `ons-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM173)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
