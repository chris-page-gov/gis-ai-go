---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/RM154",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Ability to speak Welsh by employment history",
  "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in Wales by ability to speak Welsh and by whether and when they were last employed. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "RM154",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM154/editions/2021/versions/3",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/RM154/editions/2021/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:33:38.605975Z",
      "responseSha256": "70590f1cfe07a19ccf228eac95d27f0fcd7ea799509575f1f06b162a126a4431",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/189",
      "normalisedRecordSha256": "7bd0960a9671c2c460f2f55a12d5fbd3eb2a045c57ef0478a8b4c6e6732b7177",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/RM154/editions/2021/versions/3"
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
    "releaseVersion": "3"
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
        "description": "This classifies a person as being able to \"Speak Welsh\". They may have also ticked one or more of the following: * understand spoken Welsh * read Welsh * write Welsh In results that classify people by Welsh language skills, a person may appear in more than one category depending on which combination of skills they have.",
        "id": "welsh_skills_speak",
        "label": "Welsh speaking ability (3 categories)",
        "name": "welsh_skills_speak"
      },
      {
        "description": "Classifies people who were not in employment on Census Day into: * Not in employment: Worked in the last 12 months * Not in employment: Not worked in the last 12 months * Not in employment: Never worked",
        "id": "has_ever_worked",
        "label": "Employment history (4 categories)",
        "name": "has_ever_worked"
      }
    ],
    "edition": "2021",
    "id": "RM154",
    "metadata": {
      "description": "This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in Wales by ability to speak Welsh and by whether and when they were last employed. The estimates are as at Census Day, 21 March 2021.",
      "last_updated": "0001-01-01T00:00:00Z",
      "release_date": "2024-01-15T00:00:00.000Z",
      "state": "published",
      "title": "Ability to speak Welsh by employment history",
      "unit_of_measure": "Person"
    },
    "metadataContract": {
      "catalogueType": "cantabular_multivariate_table",
      "dimensionListPresent": true,
      "identityEvidence": {
        "datasetLinks": {
          "editions": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/RM154/editions"
          },
          "latest_version": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/RM154/editions/2021/versions/3",
            "id": "3"
          },
          "self": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/RM154"
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
      "retrievedAt": "2026-10-02T01:33:38.605975Z",
      "sha256": "70590f1cfe07a19ccf228eac95d27f0fcd7ea799509575f1f06b162a126a4431",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/RM154/editions/2021/versions/3/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "maximumNative": null,
      "minimumNative": null,
      "reason": "no-native-time-dimension",
      "status": "unknown"
    },
    "version": "3",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/RM154/editions/2021/versions/3"
  }
}
---

# Ability to speak Welsh by employment history

This dataset provides Census 2021 estimates that classify usual residents aged 16 years and over in Wales by ability to speak Welsh and by whether and when they were last employed. The estimates are as at Census Day, 21 March 2021.

Native identifier: `RM154`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/RM154/editions/2021/versions/3)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
