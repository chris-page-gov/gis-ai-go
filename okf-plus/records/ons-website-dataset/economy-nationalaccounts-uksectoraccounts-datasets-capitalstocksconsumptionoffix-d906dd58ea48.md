---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Feconomy%2Fnationalaccounts%2Fuksectoraccounts%2Fdatasets%2Fcapitalstocksconsumptionoffixedcapital%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Capital Stocks, Consumption of Fixed Capital",
  "description": "Capital stocks represents the value of all fixed assets used in production in the economy.",
  "nativeIdentifier": "/economy/nationalaccounts/uksectoraccounts/datasets/capitalstocksconsumptionoffixedcapital/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/capitalstocksconsumptionoffixedcapital/current",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "National Income",
    "Income",
    "Cap Stock",
    "dataset"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "responseSha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "sourcePointer": "/items/237",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/237",
      "normalisedRecordSha256": "368a18e156a66b0594af0ef77b136bd6e3d55d9831564b03602564a5da3fa28f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/capitalstocksconsumptionoffixedcapital/current"
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
    "id": "/economy/nationalaccounts/uksectoraccounts/datasets/capitalstocksconsumptionoffixedcapital/current",
    "keywords": [
      "National Income",
      "Income",
      "Cap Stock"
    ],
    "meta_description": "Capital stocks represents the value of all fixed assets used in production in the economy.",
    "nativeIdentityField": "uri",
    "release_date": "2015-12-01T15:21:27.048Z",
    "resource": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/capitalstocksconsumptionoffixedcapital/current",
    "sourceEvidence": {
      "pointer": "/items/237",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "sha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Capital stocks represents the value of all fixed assets used in production in the economy.",
    "title": "Capital Stocks, Consumption of Fixed Capital",
    "topics": [
      "1245",
      "2735",
      "7859"
    ],
    "type": "dataset",
    "uri": "/economy/nationalaccounts/uksectoraccounts/datasets/capitalstocksconsumptionoffixedcapital/current"
  }
}
---

# Capital Stocks, Consumption of Fixed Capital

Capital stocks represents the value of all fixed assets used in production in the economy.

Native identifier: `/economy/nationalaccounts/uksectoraccounts/datasets/capitalstocksconsumptionoffixedcapital/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/capitalstocksconsumptionoffixedcapital/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
