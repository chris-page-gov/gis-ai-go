---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fnationalaccounts%2Fuksectoraccounts%2Fdatasets%2Fprofitabilityofukcompanies",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Profitability of UK companies time series",
  "description": "The net rate of return on capital employed for UK private non-financial corporations related to their UK operations.",
  "nativeIdentifier": "/economy/nationalaccounts/uksectoraccounts/datasets/profitabilityofukcompanies",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/profitabilityofukcompanies",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "manufacturing",
    "services",
    "uk continental shelf",
    "PNFCs",
    "ROR",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/878",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2878",
      "normalisedRecordSha256": "6acbb84d01ef8fb3650f76a7887c8c0442391946f6f1bdc913af8a210ac55b8e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/profitabilityofukcompanies"
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
    "dataset_id": "PROF",
    "edition": "",
    "id": "/economy/nationalaccounts/uksectoraccounts/datasets/profitabilityofukcompanies",
    "keywords": [
      "manufacturing",
      "services",
      "uk continental shelf",
      "PNFCs",
      "ROR"
    ],
    "meta_description": "The net rate of return on capital employed for UK private non-financial corporations related to their UK operations.",
    "nativeIdentityField": "uri",
    "release_date": "2025-11-28T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/profitabilityofukcompanies",
    "sourceEvidence": {
      "pointer": "/items/878",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "Annual and quarterly data for the latest profitability estimates of UK companies.",
    "title": "Profitability of UK companies time series",
    "topics": [
      "7859",
      "1245",
      "2735"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/nationalaccounts/uksectoraccounts/datasets/profitabilityofukcompanies"
  }
}
---

# Profitability of UK companies time series

The net rate of return on capital employed for UK private non-financial corporations related to their UK operations.

Native identifier: `/economy/nationalaccounts/uksectoraccounts/datasets/profitabilityofukcompanies`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/profitabilityofukcompanies)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
