---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/RM123",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Sexual orientation by disability",
  "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales by sexual orientation by disability. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM123",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM123/editions/2021/versions/4",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM123/editions/2021/versions/4/metadata",
      "retrievedAt": "2026-10-02T01:34:04.670946Z",
      "responseSha256": "f5aa11a0cf180c7eb878842b99c0ca675f50c2204e9a53e2154ff6cf811b5c9d",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/220",
      "normalisedRecordSha256": "0b2b2d15c328807ad097f0133a5ec14e6d8cded756287d856b1fc9b5d2e98832",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM123/editions/2021/versions/4"
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
    "releaseVersion": "4"
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
        "description": "Classifies people according to the responses to the sexual orientation question. This question was voluntary and was only asked of people aged 16 years and over.",
        "id": "sexual_orientation_6a",
        "label": "Sexual orientation (6 categories)",
        "name": "sexual_orientation_6a"
      },
      {
        "description": "People who assessed their day-to-day activities as limited by long-term physical or mental health conditions or illnesses are considered disabled. This definition of a disabled person meets the harmonised standard for measuring disability and is in line with the Equality Act (2010).",
        "id": "disability_4a",
        "label": "Disability - Equality act disabled (4 categories)",
        "name": "disability_4a"
      }
    ],
    "edition": "2021",
    "id": "RM123",
    "metadata": {
      "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales by sexual orientation by disability. The estimates are as at Census Day, 21 March 2021.",
      "last_updated": "0001-01-01T00:00:00Z",
      "release_date": "2024-01-15T00:00:00.000Z",
      "state": "published",
      "title": "Sexual orientation by disability",
      "unit_of_measure": "Person"
    },
    "metadataContract": {
      "catalogueType": "cantabular_flexible_table",
      "dimensionListPresent": true,
      "identityEvidence": {
        "datasetLinks": {
          "editions": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/RM123/editions"
          },
          "latest_version": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/RM123/editions/2021/versions/4",
            "id": "4"
          },
          "self": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/RM123"
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
      "retrievedAt": "2026-10-02T01:34:04.670946Z",
      "sha256": "f5aa11a0cf180c7eb878842b99c0ca675f50c2204e9a53e2154ff6cf811b5c9d",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/RM123/editions/2021/versions/4/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "maximumNative": null,
      "minimumNative": null,
      "reason": "no-native-time-dimension",
      "status": "unknown"
    },
    "version": "4",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM123/editions/2021/versions/4"
  }
}
---

# Sexual orientation by disability

This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in England and Wales by sexual orientation by disability. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM123`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM123/editions/2021/versions/4)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
