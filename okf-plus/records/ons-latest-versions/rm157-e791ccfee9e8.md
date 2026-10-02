---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/RM157",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Disability by ability to speak Welsh by age",
  "description": "This dataset provides Census 2021 estimates that classify usual residents in Wales aged 3 years and over in Wales by disability, by ability to speak Welsh, and by age. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM157",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM157/editions/2021/versions/1",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM157/editions/2021/versions/1/metadata",
      "retrievedAt": "2026-10-02T01:33:36.104840Z",
      "responseSha256": "d353fd2e0c1ec8be22de94ed90de0b95e7bc9b1db7688d25057b8509e26663cd",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/186",
      "normalisedRecordSha256": "d93573a8df8f70df2d8c609020537806474044ec5b0d12d96b74e376d524ecb7",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM157/editions/2021/versions/1"
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
        "description": "People who assessed their day-to-day activities as limited by long-term physical or mental health conditions or illnesses are considered disabled. This definition of a disabled person meets the harmonised standard for measuring disability and is in line with the Equality Act (2010).",
        "id": "disability_4a",
        "label": "Disability - Equality act disabled (4 categories)",
        "name": "disability_4a"
      },
      {
        "description": "This classifies a person as being able to \"Speak Welsh\". They may have also ticked one or more of the following: * understand spoken Welsh * read Welsh * write Welsh In results that classify people by Welsh language skills, a person may appear in more than one category depending on which combination of skills they have.",
        "id": "welsh_skills_speak",
        "label": "Welsh speaking ability (3 categories)",
        "name": "welsh_skills_speak"
      },
      {
        "description": "A person’s age on Census Day, 21 March 2021 in England and Wales. Infants aged under 1 year are classified as 0 years of age.",
        "id": "resident_age_3b",
        "label": "Age (B) (3 categories)",
        "name": "resident_age_3b"
      }
    ],
    "edition": "2021",
    "id": "RM157",
    "metadata": {
      "description": "This dataset provides Census 2021 estimates that classify usual residents in Wales aged 3 years and over in Wales by disability, by ability to speak Welsh, and by age. The estimates are as at Census Day, 21 March 2021.",
      "last_updated": "0001-01-01T00:00:00Z",
      "release_date": "2023-03-28T00:00:00.000Z",
      "state": "published",
      "title": "Disability by ability to speak Welsh by age",
      "unit_of_measure": "Person"
    },
    "metadataContract": {
      "catalogueType": "cantabular_multivariate_table",
      "dimensionListPresent": true,
      "identityEvidence": {
        "datasetLinks": {
          "editions": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/RM157/editions"
          },
          "latest_version": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/RM157/editions/2021/versions/1",
            "id": "1"
          },
          "self": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/RM157"
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
      "retrievedAt": "2026-10-02T01:33:36.104840Z",
      "sha256": "d353fd2e0c1ec8be22de94ed90de0b95e7bc9b1db7688d25057b8509e26663cd",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/RM157/editions/2021/versions/1/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "maximumNative": null,
      "minimumNative": null,
      "reason": "no-native-time-dimension",
      "status": "unknown"
    },
    "version": "1",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM157/editions/2021/versions/1"
  }
}
---

# Disability by ability to speak Welsh by age

This dataset provides Census 2021 estimates that classify usual residents in Wales aged 3 years and over in Wales by disability, by ability to speak Welsh, and by age. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM157`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM157/editions/2021/versions/1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
