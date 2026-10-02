---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Feconomicoutputandproductivity%2Fproductivitymeasures%2Fdatasets%2Fexperimentalinfrastructurestatistics",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Infrastructure statistics",
  "description": "Infrastructure in the UK, covering investment, construction activity and capital stocks, up to 2024. These are official statistics in development.",
  "nativeIdentifier": "/economy/economicoutputandproductivity/productivitymeasures/datasets/experimentalinfrastructurestatistics",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/economicoutputandproductivity/productivitymeasures/datasets/experimentalinfrastructurestatistics",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "infrastructure",
    "capital stocks",
    "government",
    "water",
    "construction",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/879",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1879",
      "normalisedRecordSha256": "131f3b603a50fd0b06a03ac46f4b47f1bf473b82fb149230ec5b94d9cb473e95",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/economicoutputandproductivity/productivitymeasures/datasets/experimentalinfrastructurestatistics"
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
    "id": "/economy/economicoutputandproductivity/productivitymeasures/datasets/experimentalinfrastructurestatistics",
    "keywords": [
      "infrastructure",
      "capital stocks",
      "government",
      "water",
      "construction"
    ],
    "meta_description": "Infrastructure in the UK, covering investment, construction activity and capital stocks, up to 2024. These are official statistics in development.",
    "nativeIdentityField": "uri",
    "release_date": "2026-06-30T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/economicoutputandproductivity/productivitymeasures/datasets/experimentalinfrastructurestatistics",
    "sourceEvidence": {
      "pointer": "/items/879",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Infrastructure in the UK, covering investment, construction activity and capital stocks, up to 2025. These are official statistics in development.",
    "title": "Infrastructure statistics",
    "topics": [
      "1245",
      "2621",
      "4696"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/economicoutputandproductivity/productivitymeasures/datasets/experimentalinfrastructurestatistics"
  }
}
---

# Infrastructure statistics

Infrastructure in the UK, covering investment, construction activity and capital stocks, up to 2024. These are official statistics in development.

Native identifier: `/economy/economicoutputandproductivity/productivitymeasures/datasets/experimentalinfrastructurestatistics`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/economicoutputandproductivity/productivitymeasures/datasets/experimentalinfrastructurestatistics)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
