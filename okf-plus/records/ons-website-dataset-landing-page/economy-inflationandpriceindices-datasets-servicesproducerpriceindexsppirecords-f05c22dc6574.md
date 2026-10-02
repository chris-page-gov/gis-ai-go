---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Finflationandpriceindices%2Fdatasets%2Fservicesproducerpriceindexsppirecords",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Services Producer Price Inflation (SPPI) records",
  "description": "Services producer price inflation (SPPI) records showing higher, lower and equal to quarterly service Producer Price Index movements for selected UK services sectors.",
  "nativeIdentifier": "/economy/inflationandpriceindices/datasets/servicesproducerpriceindexsppirecords",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/servicesproducerpriceindexsppirecords",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "SPPI",
    "services producer price indices",
    "services prices",
    "service sector",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/277",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3277",
      "normalisedRecordSha256": "51ff46dd220dc8ac8f8c6e4f9df5feff32f67a6ca6b0b45900bbc2c5869f163e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/servicesproducerpriceindexsppirecords"
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
    "metadataModified": null,
    "releaseVersion": ""
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "Website and API representations are retained separately; matching titles do not prove equivalence.",
    "Release dates do not establish the period covered by statistical observations."
  ],
  "details": {
    "canonical_topic": "",
    "cdid": "",
    "dataset_id": "",
    "edition": "",
    "id": "/economy/inflationandpriceindices/datasets/servicesproducerpriceindexsppirecords",
    "keywords": [
      "SPPI",
      "services producer price indices",
      "services prices",
      "service sector"
    ],
    "meta_description": "Services producer price inflation (SPPI) records showing higher, lower and equal to quarterly service Producer Price Index movements for selected UK services sectors.",
    "nativeIdentityField": "uri",
    "release_date": "2025-01-15T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/servicesproducerpriceindexsppirecords",
    "sourceEvidence": {
      "pointer": "/items/277",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Services producer price inflation (SPPI) records showing higher, lower and equal to quarterly service Producer Price Index movements for selected UK services sectors.",
    "title": "Services Producer Price Inflation (SPPI) records",
    "topics": [
      "1245",
      "4972"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/inflationandpriceindices/datasets/servicesproducerpriceindexsppirecords"
  }
}
---

# Services Producer Price Inflation (SPPI) records

Services producer price inflation (SPPI) records showing higher, lower and equal to quarterly service Producer Price Index movements for selected UK services sectors.

Native identifier: `/economy/inflationandpriceindices/datasets/servicesproducerpriceindexsppirecords`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/servicesproducerpriceindexsppirecords)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
