---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Finflationandpriceindices%2Fdatasets%2Fonlinepricechangesforhighdemandproducts",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Online price changes for high-demand products",
  "description": "The online price changes of selected high demand products (HDP) dataset. These data are experimental estimates developed to deliver timely indicators to help understand the impact of COVID-19.",
  "nativeIdentifier": "/economy/inflationandpriceindices/datasets/onlinepricechangesforhighdemandproducts",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/onlinepricechangesforhighdemandproducts",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "economy",
    "faster indicators",
    "high demand products",
    "prices online",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/646",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2646",
      "normalisedRecordSha256": "7b30dab5d726a89981c97afb307bc50c918009752a947d46dc71a1aca65631bc",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/onlinepricechangesforhighdemandproducts"
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
    "id": "/economy/inflationandpriceindices/datasets/onlinepricechangesforhighdemandproducts",
    "keywords": [
      "economy",
      "faster indicators",
      "high demand products",
      "prices online"
    ],
    "meta_description": "The online price changes of selected high demand products (HDP) dataset. These data are experimental estimates developed to deliver timely indicators to help understand the impact of COVID-19.",
    "nativeIdentityField": "uri",
    "release_date": "2020-08-19T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/onlinepricechangesforhighdemandproducts",
    "sourceEvidence": {
      "pointer": "/items/646",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "The online price changes of selected high-demand products (HDPs) dataset. These data are experimental estimates developed to deliver timely indicators to help understand the impact of the coronavirus (COVID-19).",
    "title": "Online price changes for high-demand products",
    "topics": [
      "1245",
      "4972"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/inflationandpriceindices/datasets/onlinepricechangesforhighdemandproducts"
  }
}
---

# Online price changes for high-demand products

The online price changes of selected high demand products (HDP) dataset. These data are experimental estimates developed to deliver timely indicators to help understand the impact of COVID-19.

Native identifier: `/economy/inflationandpriceindices/datasets/onlinepricechangesforhighdemandproducts`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/onlinepricechangesforhighdemandproducts)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
