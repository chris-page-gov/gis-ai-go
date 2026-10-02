---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fregionalaccounts%2Fgrossdisposablehouseholdincome%2Fdatasets%2Fregionalrealhouseholddisposableincome",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Regional Real Household Disposable Income",
  "description": "Estimates of money residents have for spending or saving, after taxes and other social contributions are deducted, adjusted to remove the effect of inflation.",
  "nativeIdentifier": "/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalrealhouseholddisposableincome",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalrealhouseholddisposableincome",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "inflation",
    "volume",
    "CVM",
    "RHDI",
    "cost of living",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/81",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3081",
      "normalisedRecordSha256": "1e7b19c020a8093a924b1bfb9f30fe94283421d3a90c218b4aefd1f9aa77db00",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalrealhouseholddisposableincome"
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
    "id": "/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalrealhouseholddisposableincome",
    "keywords": [
      "inflation",
      "volume",
      "CVM",
      "RHDI",
      "cost of living"
    ],
    "meta_description": "Estimates of money residents have for spending or saving, after taxes and other social contributions are deducted, adjusted to remove the effect of inflation.",
    "nativeIdentityField": "uri",
    "release_date": "2026-08-18T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalrealhouseholddisposableincome",
    "sourceEvidence": {
      "pointer": "/items/81",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Estimates of money residents have for spending or saving, after taxes and other social contributions are deducted, adjusted to remove the effect of inflation.",
    "title": "Regional Real Household Disposable Income",
    "topics": [
      "1245",
      "2724",
      "9831"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalrealhouseholddisposableincome"
  }
}
---

# Regional Real Household Disposable Income

Estimates of money residents have for spending or saving, after taxes and other social contributions are deducted, adjusted to remove the effect of inflation.

Native identifier: `/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalrealhouseholddisposableincome`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalrealhouseholddisposableincome)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
