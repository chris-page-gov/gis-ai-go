---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Feconomicoutputandproductivity%2Foutput%2Fdatasets%2Fshelfavailabilityofitemsfromukshops",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Shelf availability of items from UK shops",
  "description": "Data provided by Kantar Public, recording item availability of 23 popular products across the UK and English regions.",
  "nativeIdentifier": "/economy/economicoutputandproductivity/output/datasets/shelfavailabilityofitemsfromukshops",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/shelfavailabilityofitemsfromukshops",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "faster indicators",
    "supply",
    "realtimeindicators",
    "shortages",
    "unavailable items",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/338",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3338",
      "normalisedRecordSha256": "9ff0a3c0cac8f6697262a0da79ff079ab7a40a645560c1f8fe9b013a94975008",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/shelfavailabilityofitemsfromukshops"
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
    "id": "/economy/economicoutputandproductivity/output/datasets/shelfavailabilityofitemsfromukshops",
    "keywords": [
      "faster indicators",
      "supply",
      "realtimeindicators",
      "shortages",
      "unavailable items"
    ],
    "meta_description": "Data provided by Kantar Public, recording item availability of 23 popular products across the UK and English regions.",
    "nativeIdentityField": "uri",
    "release_date": "2022-03-10T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/shelfavailabilityofitemsfromukshops",
    "sourceEvidence": {
      "pointer": "/items/338",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Data provided by Kantar Public, recording item availability of 21 popular products across the UK and English regions.",
    "title": "Shelf availability of items from UK shops",
    "topics": [
      "6625",
      "1245",
      "2621"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/economicoutputandproductivity/output/datasets/shelfavailabilityofitemsfromukshops"
  }
}
---

# Shelf availability of items from UK shops

Data provided by Kantar Public, recording item availability of 23 popular products across the UK and English regions.

Native identifier: `/economy/economicoutputandproductivity/output/datasets/shelfavailabilityofitemsfromukshops`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/shelfavailabilityofitemsfromukshops)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
