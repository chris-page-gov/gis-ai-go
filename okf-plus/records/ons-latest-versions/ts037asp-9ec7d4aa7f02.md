---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-latest-versions/TS037ASP",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "General health, age-standardised proportions",
  "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by the state of their general health. The estimates are as at Census Day, 21 March 2021. Age-standardisation allows for comparisons between populations that may contain proportions of different ages, represented as a percentage.",
  "nativeIdentifier": "TS037ASP",
  "sourceFamily": "ons-latest-versions",
  "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS037ASP/editions/2021/versions/2",
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
      "resource": "https://api.beta.ons.gov.uk/v1/datasets/TS037ASP/editions/2021/versions/2/metadata",
      "retrievedAt": "2026-10-02T01:32:15.681799Z",
      "responseSha256": "a6ab3d71818f8d8bc17a791d9e87560bfc23e3f17a39d6a7c0be1f3c8bc82c5d",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-latest-versions.json",
      "normalisedPointer": "/records/90",
      "normalisedRecordSha256": "20d9274126397612167ec6ae8dd764663b6058c4247d2b0d664f4752e02439d0",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.beta.ons.gov.uk/v1/datasets/TS037ASP/editions/2021/versions/2"
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
    "releaseVersion": "2"
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
        "description": "Lower tier local authorities provide a range of local services. In England there are 309 lower tier local authorities. These are made up of non-metropolitan districts (181), unitary authorities (59), metropolitan districts (36) and London boroughs (33, including City of London). In Wales there are 22 local authorities made up of 22 unitary authorities. Of these local authority types, only non-metropolitan districts are not additionally classified as upper tier local authorities.",
        "id": "ltla",
        "label": "Lower Tier Local Authorities",
        "name": "ltla"
      },
      {
        "description": "A person's assessment of the general state of their health from very good to very bad. This assessment is not based on a person's health over any specified period of time.",
        "id": "health_in_general",
        "label": "General health (6 categories)",
        "name": "health_in_general"
      }
    ],
    "edition": "2021",
    "id": "TS037ASP",
    "metadata": {
      "description": "This dataset provides Census 2021 estimates that classify usual residents in England and Wales by the state of their general health. The estimates are as at Census Day, 21 March 2021. Age-standardisation allows for comparisons between populations that may contain proportions of different ages, represented as a percentage.",
      "last_updated": "0001-01-01T00:00:00Z",
      "release_date": "2023-02-16T00:00:00.000Z",
      "state": "published",
      "title": "General health, age-standardised proportions",
      "unit_of_measure": "Person"
    },
    "metadataContract": {
      "catalogueType": "cantabular_flexible_table",
      "dimensionListPresent": true,
      "identityEvidence": {
        "datasetLinks": {
          "editions": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS037ASP/editions"
          },
          "latest_version": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS037ASP/editions/2021/versions/2",
            "id": "2"
          },
          "self": {
            "href": "https://api.beta.ons.gov.uk/v1/datasets/TS037ASP"
          }
        },
        "isBasedOn": {
          "@id": "atc-ts-hduc-ur-asp-ltla",
          "@type": "cantabular_flexible_table"
        }
      },
      "variant": "cantabular-dataset-links"
    },
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T01:32:15.681799Z",
      "sha256": "a6ab3d71818f8d8bc17a791d9e87560bfc23e3f17a39d6a7c0be1f3c8bc82c5d",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/datasets/TS037ASP/editions/2021/versions/2/metadata"
    },
    "metadataStatus": "captured",
    "temporal": {
      "maximumNative": null,
      "minimumNative": null,
      "reason": "no-native-time-dimension",
      "status": "unknown"
    },
    "version": "2",
    "versionUrl": "https://api.beta.ons.gov.uk/v1/datasets/TS037ASP/editions/2021/versions/2"
  }
}
---

# General health, age-standardised proportions

This dataset provides Census 2021 estimates that classify usual residents in England and Wales by the state of their general health. The estimates are as at Census Day, 21 March 2021. Age-standardisation allows for comparisons between populations that may contain proportions of different ages, represented as a percentage.

Native identifier: `TS037ASP`.

Source family: `ons-latest-versions`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.beta.ons.gov.uk/v1/datasets/TS037ASP/editions/2021/versions/2)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
