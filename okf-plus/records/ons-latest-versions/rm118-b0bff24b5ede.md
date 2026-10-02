---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/RM118",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Religion by age",
  "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by religion and by age. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM118",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM118/editions/2021/versions/1",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM118/editions/2021/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:34:08.847108Z",
      "responseSha256": "14fb045b8b660a332a13c4594becedb7832bccd0959e5432826091492d21c629",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/225",
      "normalisedRecordSha256": "5a8d81da40bfff15a1a7d27ba684077481b602c84a1ef71495864866b3027141",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM118/editions/2021/versions/1"
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
    "metadataModified": "0001-01-01T00:00:00Z",
    "releaseVersion": "1"
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [],
  "details": {
    "dimensions": [
      {
        "description": "Lower tier local authorities provide a range of local services. There are 309 lower tier local authorities in England made up of 181 non-metropolitan districts, 59 unitary authorities, 36 metropolitan districts and 33 London boroughs (including City of London). In Wales there are 22 local authorities made up of 22 unitary authorities.",
        "id": "ltla",
        "label": "Lower tier local authorities",
        "name": "ltla"
      },
      {
        "description": "The religion people connect or identify with (their religious affiliation), whether or not they practise or have belief in it. This question was voluntary and includes people who identified with one of 8 tick-box response options, including \"No religion\", alongside those who chose not to answer this question.",
        "id": "religion_tb",
        "label": "Religion (10 categories)",
        "name": "religion_tb"
      },
      {
        "description": "A person’s age on Census Day, 21 March 2021 in England and Wales. Infants aged under 1 year are classified as 0 years of age.",
        "id": "resident_age_8a",
        "label": "Age (8 categories)",
        "name": "resident_age_8a"
      }
    ],
    "edition": "2021",
    "id": "RM118",
    "metadata": {
      "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by religion and by age. The estimates are as at Census Day, 21 March 2021.",
      "last_updated": "0001-01-01T00:00:00Z",
      "release_date": "2023-03-28T00:00:00.000Z",
      "state": "published",
      "title": "Religion by age",
      "unit_of_measure": "Person"
    },
    "metadataContract": {
      "catalogueType": "cantabular_multivariate_table",
      "dimensionListPresent": true,
      "identityEvidence": {
        "datasetLinks": {
          "editions": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/RM118/editions"
          },
          "latest_version": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/RM118/editions/2021/versions/1",
            "id": "1"
          },
          "self": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/RM118"
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
      "retrievedAt": "2026-10-02T01:34:08.847108Z",
      "sha256": "14fb045b8b660a332a13c4594becedb7832bccd0959e5432826091492d21c629",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/RM118/editions/2021/versions/1/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "maximumNative": null,
      "minimumNative": null,
      "reason": "no-native-time-dimension",
      "status": "unknown"
    },
    "version": "1",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM118/editions/2021/versions/1"
  }
}
---

# Religion by age

This dataset provides Census 2021 estimates that classify usual residents in England and Wales by religion and by age. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM118`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM118/editions/2021/versions/1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
