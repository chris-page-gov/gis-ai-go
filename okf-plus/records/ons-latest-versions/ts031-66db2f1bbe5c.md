---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/TS031",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Religion (detailed)",
  "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by religion. The estimates are as at Census Day, 21 March 2021.",
  "nativeIdentifier": "TS031",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS031/editions/2021/versions/4",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS031/editions/2021/versions/4/metadata",
      "retrievedAt": "2026-10-02T01:32:21.547297Z",
      "responseSha256": "239d0d0b9164646b7ad1d2c1bb4027e16472f0d3ac7b7611f7ae6570bcb60e5d",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/97",
      "normalisedRecordSha256": "9221b0a7d0be05f5b789b8fcab14aba30e073d41cb707046cfc3c0d3559dcc0d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/TS031/editions/2021/versions/4"
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
        "description": "The religion people connect or identify with (their religious affiliation), whether or not they practise or have belief in it. This question was voluntary and the variable includes people who answered the question, including \"No Religion\", alongside those who chose not to answer this question. This variable classifies responses into the eight tick-box response options. Write-in responses are classified by their \"parent\" religious affiliation, including \"No Religion\", where applicable.",
        "id": "religion_58a",
        "label": "Religion (detailed) (58 categories)",
        "name": "religion_58a"
      }
    ],
    "edition": "2021",
    "id": "TS031",
    "metadata": {
      "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by religion. The estimates are as at Census Day, 21 March 2021.",
      "last_updated": "0001-01-01T00:00:00Z",
      "release_date": "2023-04-05T00:00:00.000Z",
      "state": "published",
      "title": "Religion (detailed)",
      "unit_of_measure": "Person"
    },
    "metadataContract": {
      "catalogueType": "cantabular_flexible_table",
      "dimensionListPresent": true,
      "identityEvidence": {
        "datasetLinks": {
          "editions": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS031/editions"
          },
          "latest_version": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS031/editions/2021/versions/4",
            "id": "4"
          },
          "self": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS031"
          }
        },
        "isBasedOn": {
          "@id": "atc-ts-eilr-ur-ct-msoa",
          "@type": "cantabular_flexible_table"
        }
      },
      "variant": "cantabular-dataset-links"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:32:21.547297Z",
      "sha256": "239d0d0b9164646b7ad1d2c1bb4027e16472f0d3ac7b7611f7ae6570bcb60e5d",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/TS031/editions/2021/versions/4/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "maximumNative": null,
      "minimumNative": null,
      "reason": "no-native-time-dimension",
      "status": "unknown"
    },
    "version": "4",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/TS031/editions/2021/versions/4"
  }
}
---

# Religion (detailed)

This dataset provides Census 2021 estimates that classify usual residents in England and Wales by religion. The estimates are as at Census Day, 21 March 2021.

Native identifier: `TS031`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/TS031/editions/2021/versions/4)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
