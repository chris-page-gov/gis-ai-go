---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/TS035",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Welsh language skills (reading)",
  "description": "This dataset provides Census 2021 estimates that classify usual residents aged 3 years and over in Wales by their ability to read Welsh. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "TS035",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS035/editions/2021/versions/3",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS035/editions/2021/versions/3/metadata",
      "retrievedAt": "2026-10-02T01:32:18.191428Z",
      "responseSha256": "6a223c530885d61851e67ad0c80a8a06d413635be2831f1d82dbe7a6d3ee2d7e",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/93",
      "normalisedRecordSha256": "eda81e76bcca6077275b35d13fed747de440210d131153c04a1a19bdfb659ff5",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/TS035/editions/2021/versions/3"
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
        "description": "This classifies a person as being able to \"Read Welsh\". They may have also ticked one or more of the following: * understand spoken Welsh * speak Welsh * write Welsh In results that classify people by Welsh language skills, a person may appear in more than one category depending on which combination of skills they have.",
        "id": "welsh_skills_read",
        "label": "Welsh reading ability (3 categories)",
        "name": "welsh_skills_read"
      }
    ],
    "edition": "2021",
    "id": "TS035",
    "metadata": {
      "description": "This dataset provides Census 2021 estimates that classify usual residents aged 3 years and over in Wales by their ability to read Welsh. The estimates are as at Census Day, 21 March 2021.",
      "last_updated": "0001-01-01T00:00:00Z",
      "release_date": "2023-03-28T00:00:00.000Z",
      "state": "published",
      "title": "Welsh language skills (reading)",
      "unit_of_measure": "Person"
    },
    "metadataContract": {
      "catalogueType": "cantabular_flexible_table",
      "dimensionListPresent": true,
      "identityEvidence": {
        "datasetLinks": {
          "editions": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS035/editions"
          },
          "latest_version": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS035/editions/2021/versions/3",
            "id": "3"
          },
          "self": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS035"
          }
        },
        "isBasedOn": {
          "@id": "UR",
          "@type": "cantabular_flexible_table"
        }
      },
      "variant": "cantabular-dataset-links"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:32:18.191428Z",
      "sha256": "6a223c530885d61851e67ad0c80a8a06d413635be2831f1d82dbe7a6d3ee2d7e",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/TS035/editions/2021/versions/3/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "maximumNative": null,
      "minimumNative": null,
      "reason": "no-native-time-dimension",
      "status": "unknown"
    },
    "version": "3",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/TS035/editions/2021/versions/3"
  }
}
---

# Welsh language skills (reading)

This dataset provides Census 2021 estimates that classify usual residents aged 3 years and over in Wales by their ability to read Welsh. The estimates are as at Census Day, 21 March 2021.

Native identifier: `TS035`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/TS035/editions/2021/versions/3)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
