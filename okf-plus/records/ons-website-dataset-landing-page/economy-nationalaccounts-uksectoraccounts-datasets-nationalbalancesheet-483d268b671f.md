---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fnationalaccounts%2Fuksectoraccounts%2Fdatasets%2Fnationalbalancesheet",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "The UK national balance sheet time series",
  "description": "Annual estimates of the market value of financial and non-financial assets for the UK, providing a measure of the nation's wealth.",
  "nativeIdentifier": "/economy/nationalaccounts/uksectoraccounts/datasets/nationalbalancesheet",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/nationalbalancesheet",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "investments",
    "dwellings",
    "land",
    "national wealth",
    "net worth",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/540",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3540",
      "normalisedRecordSha256": "63c8ad0d57ba9626d6afb58bd3ee327781eeb295a5426e47a941bc37c972bcd0",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/nationalbalancesheet"
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
    "dataset_id": "NBS",
    "edition": "",
    "id": "/economy/nationalaccounts/uksectoraccounts/datasets/nationalbalancesheet",
    "keywords": [
      "investments",
      "dwellings",
      "land",
      "national wealth",
      "net worth"
    ],
    "meta_description": "Annual estimates of the market value of financial and non-financial assets for the UK, providing a measure of the nation's wealth.",
    "nativeIdentityField": "uri",
    "release_date": "2026-06-09T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/nationalbalancesheet",
    "sourceEvidence": {
      "pointer": "/items/540",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Annual estimates of the market value of financial and non-financial assets for the UK, providing a measure of the nation's wealth.",
    "title": "The UK national balance sheet time series",
    "topics": [
      "1245",
      "2735",
      "7859"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/nationalaccounts/uksectoraccounts/datasets/nationalbalancesheet"
  }
}
---

# The UK national balance sheet time series

Annual estimates of the market value of financial and non-financial assets for the UK, providing a measure of the nation's wealth.

Native identifier: `/economy/nationalaccounts/uksectoraccounts/datasets/nationalbalancesheet`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/nationalbalancesheet)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
