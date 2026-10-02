---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fnationalaccounts%2Fuksectoraccounts%2Fdatasets%2Fcapitalstock",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Capital stocks and fixed capital consumption time series",
  "description": "Annual estimates of the value and types of non-financial assets used in the production of goods or services within the UK economy and their loss in value over time.",
  "nativeIdentifier": "/economy/nationalaccounts/uksectoraccounts/datasets/capitalstock",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/capitalstock",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "national income",
    "physical capital",
    "fixed assets",
    "depreciation",
    "cap stock",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/393",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/393",
      "normalisedRecordSha256": "1b46498497d491265f8ae50e3461a378bf247ab2c9f82af0351dd8517e6534f1",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/capitalstock"
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
    "dataset_id": "CAPSTK",
    "edition": "",
    "id": "/economy/nationalaccounts/uksectoraccounts/datasets/capitalstock",
    "keywords": [
      "national income",
      "physical capital",
      "fixed assets",
      "depreciation",
      "cap stock"
    ],
    "meta_description": "Annual estimates of the value and types of non-financial assets used in the production of goods or services within the UK economy and their loss in value over time.",
    "nativeIdentityField": "uri",
    "release_date": "2025-11-27T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/capitalstock",
    "sourceEvidence": {
      "pointer": "/items/393",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "The value and types of non-financial assets used in the production of goods or services within the UK economy and their loss in value over time, annual estimates.",
    "title": "Capital stocks and fixed capital consumption time series",
    "topics": [
      "7859",
      "1245",
      "2735"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/nationalaccounts/uksectoraccounts/datasets/capitalstock"
  }
}
---

# Capital stocks and fixed capital consumption time series

Annual estimates of the value and types of non-financial assets used in the production of goods or services within the UK economy and their loss in value over time.

Native identifier: `/economy/nationalaccounts/uksectoraccounts/datasets/capitalstock`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/capitalstock)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
