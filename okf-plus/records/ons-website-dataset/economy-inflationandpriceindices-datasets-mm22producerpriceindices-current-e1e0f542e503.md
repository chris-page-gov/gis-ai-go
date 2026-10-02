---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Feconomy%2Finflationandpriceindices%2Fdatasets%2Fmm22producerpriceindices%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "MM22 Producer Price Indices",
  "description": "Price movement data at all manufacturing, aggregated industry and product group level. Data supplied from individual UK manufacturers, importers and exporters.",
  "nativeIdentifier": "/economy/inflationandpriceindices/datasets/mm22producerpriceindices/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/mm22producerpriceindices/current",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "dataset"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "responseSha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "sourcePointer": "/items/849",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/849",
      "normalisedRecordSha256": "12571fb11e9c6a7a9816c7409b446dbc93af76d46140dbf2805fddb9c9015f95",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/mm22producerpriceindices/current"
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
    "releaseVersion": "Current"
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
    "edition": "Current",
    "id": "/economy/inflationandpriceindices/datasets/mm22producerpriceindices/current",
    "keywords": [],
    "meta_description": "Price movement data at all manufacturing, aggregated industry and product group level. Data supplied from individual UK manufacturers, importers and exporters.",
    "nativeIdentityField": "uri",
    "release_date": "2015-12-16T08:57:53.943Z",
    "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/mm22producerpriceindices/current",
    "sourceEvidence": {
      "pointer": "/items/849",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "sha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Price movement data at all manufacturing, aggregated industry and product group level. Data supplied from individual UK manufacturers, importers and exporters.",
    "title": "MM22 Producer Price Indices",
    "topics": [
      "1245",
      "4972"
    ],
    "type": "dataset",
    "uri": "/economy/inflationandpriceindices/datasets/mm22producerpriceindices/current"
  }
}
---

# MM22 Producer Price Indices

Price movement data at all manufacturing, aggregated industry and product group level. Data supplied from individual UK manufacturers, importers and exporters.

Native identifier: `/economy/inflationandpriceindices/datasets/mm22producerpriceindices/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/mm22producerpriceindices/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
