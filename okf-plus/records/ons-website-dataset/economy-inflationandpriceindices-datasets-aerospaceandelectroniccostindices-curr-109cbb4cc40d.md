---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Feconomy%2Finflationandpriceindices%2Fdatasets%2Faerospaceandelectroniccostindices%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Aerospace and Electronic Cost Indices",
  "description": "Cost indices (purchase of materials and fuels, average weekly earnings, general expenses and combined costs) relating to 4 aerospace and electronics industries.",
  "nativeIdentifier": "/economy/inflationandpriceindices/datasets/aerospaceandelectroniccostindices/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/aerospaceandelectroniccostindices/current",
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
      "sourcePointer": "/items/13",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/13",
      "normalisedRecordSha256": "8a848817d6630bfd1ab52de86ba2725c02990054b8f38e2abb26453175cf964b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/aerospaceandelectroniccostindices/current"
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
    "id": "/economy/inflationandpriceindices/datasets/aerospaceandelectroniccostindices/current",
    "keywords": [],
    "meta_description": "Cost indices (purchase of materials and fuels, average weekly earnings, general expenses and combined costs) relating to 4 aerospace and electronics industries.",
    "nativeIdentityField": "uri",
    "release_date": "2015-12-16T08:55:55.428Z",
    "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/aerospaceandelectroniccostindices/current",
    "sourceEvidence": {
      "pointer": "/items/13",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "sha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Cost indices (purchase of materials and fuels, average weekly earnings, general expenses and combined costs) relating to 4 aerospace and electronics industries.",
    "title": "Aerospace and Electronic Cost Indices",
    "topics": [
      "1245",
      "4972"
    ],
    "type": "dataset",
    "uri": "/economy/inflationandpriceindices/datasets/aerospaceandelectroniccostindices/current"
  }
}
---

# Aerospace and Electronic Cost Indices

Cost indices (purchase of materials and fuels, average weekly earnings, general expenses and combined costs) relating to 4 aerospace and electronics industries.

Native identifier: `/economy/inflationandpriceindices/datasets/aerospaceandelectroniccostindices/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/aerospaceandelectroniccostindices/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
