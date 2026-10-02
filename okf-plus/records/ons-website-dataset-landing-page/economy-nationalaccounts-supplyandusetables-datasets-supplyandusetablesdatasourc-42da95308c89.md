---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fnationalaccounts%2Fsupplyandusetables%2Fdatasets%2Fsupplyandusetablesdatasourcescatalogue",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Supply and use tables data sources catalogue",
  "description": "A list of the data sources used to compile the supply and use tables. This also includes how this data is sourced, the area of National Accounts that use it and the transaction it feeds into.",
  "nativeIdentifier": "/economy/nationalaccounts/supplyandusetables/datasets/supplyandusetablesdatasourcescatalogue",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/nationalaccounts/supplyandusetables/datasets/supplyandusetablesdatasourcescatalogue",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "SIC",
    "economy",
    "CPA",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/446",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3446",
      "normalisedRecordSha256": "524aadb9b9e0a7c0ccd625327481a2b89f534afcb09b73d615eb2459b14fea0f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/nationalaccounts/supplyandusetables/datasets/supplyandusetablesdatasourcescatalogue"
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
    "id": "/economy/nationalaccounts/supplyandusetables/datasets/supplyandusetablesdatasourcescatalogue",
    "keywords": [
      "SIC",
      "economy",
      "CPA"
    ],
    "meta_description": "A list of the data sources used to compile the supply and use tables. This also includes how this data is sourced, the area of National Accounts that use it and the transaction it feeds into.",
    "nativeIdentityField": "uri",
    "release_date": "2025-10-31T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/nationalaccounts/supplyandusetables/datasets/supplyandusetablesdatasourcescatalogue",
    "sourceEvidence": {
      "pointer": "/items/446",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "A list of the data sources used to compile the supply and use tables. This also includes how this data is sourced, the area of National Accounts that use it and the transaction it feeds into.",
    "title": "Supply and use tables data sources catalogue",
    "topics": [
      "2735",
      "1245",
      "3741"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/nationalaccounts/supplyandusetables/datasets/supplyandusetablesdatasourcescatalogue"
  }
}
---

# Supply and use tables data sources catalogue

A list of the data sources used to compile the supply and use tables. This also includes how this data is sourced, the area of National Accounts that use it and the transaction it feeds into.

Native identifier: `/economy/nationalaccounts/supplyandusetables/datasets/supplyandusetablesdatasourcescatalogue`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/nationalaccounts/supplyandusetables/datasets/supplyandusetablesdatasourcescatalogue)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
