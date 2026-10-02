---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Feconomicoutputandproductivity%2Foutput%2Fdatasets%2Finvestmentinflooddefencesintheuk",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Investment in flood defences in the UK",
  "description": "Dataset contains flood management expenditure data taken from reports published by the Environment Agency and the Department for Environment, Food and Rural Affairs on gov.uk.",
  "nativeIdentifier": "/economy/economicoutputandproductivity/output/datasets/investmentinflooddefencesintheuk",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/investmentinflooddefencesintheuk",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "flood",
    "investment",
    "environment",
    "infrastructure",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "responseSha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "sourcePointer": "/items/975",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/1975",
      "normalisedRecordSha256": "796430de5da2c00a623bbae4b7244408c8a8951914834d8a071d8e29f531ac48",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/investmentinflooddefencesintheuk"
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
    "id": "/economy/economicoutputandproductivity/output/datasets/investmentinflooddefencesintheuk",
    "keywords": [
      "flood",
      "investment",
      "environment",
      "infrastructure"
    ],
    "meta_description": "Dataset contains flood management expenditure data taken from reports published by the Environment Agency and the Department for Environment, Food and Rural Affairs on gov.uk.",
    "nativeIdentityField": "uri",
    "release_date": "2023-05-16T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/investmentinflooddefencesintheuk",
    "sourceEvidence": {
      "pointer": "/items/975",
      "retrievedAt": "2026-10-02T07:58:51.109895Z",
      "sha256": "096d4f3d6adcd37b38f0bbf15c984de9130344bd7a7c6666b1bf88819b2d9767",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Dataset contains flood management expenditure data taken from reports published by the Environment Agency and the Department for Environment, Food and Rural Affairs on gov.uk.",
    "title": "Investment in flood defences in the UK",
    "topics": [
      "1245",
      "2621",
      "6625"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/economicoutputandproductivity/output/datasets/investmentinflooddefencesintheuk"
  }
}
---

# Investment in flood defences in the UK

Dataset contains flood management expenditure data taken from reports published by the Environment Agency and the Department for Environment, Food and Rural Affairs on gov.uk.

Native identifier: `/economy/economicoutputandproductivity/output/datasets/investmentinflooddefencesintheuk`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/investmentinflooddefencesintheuk)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
