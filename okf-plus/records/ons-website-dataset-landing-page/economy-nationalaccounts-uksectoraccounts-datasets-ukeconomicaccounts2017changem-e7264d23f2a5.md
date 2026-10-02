---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fnationalaccounts%2Fuksectoraccounts%2Fdatasets%2Fukeconomicaccounts2017changematrix",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "UK Economic Accounts 2017 change matrix",
  "description": "Provides details of the changes to UK Economic Accounts tables",
  "nativeIdentifier": "/economy/nationalaccounts/uksectoraccounts/datasets/ukeconomicaccounts2017changematrix",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/ukeconomicaccounts2017changematrix",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Blue book",
    "changes",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/640",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3640",
      "normalisedRecordSha256": "ce7a800b7ca21520115ea56921160cbad986a751f8f6492fcd885e2c95758b83",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/ukeconomicaccounts2017changematrix"
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
    "id": "/economy/nationalaccounts/uksectoraccounts/datasets/ukeconomicaccounts2017changematrix",
    "keywords": [
      "Blue book",
      "changes"
    ],
    "meta_description": "Provides details of the changes to UK Economic Accounts tables",
    "nativeIdentityField": "uri",
    "release_date": "2017-07-05T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/ukeconomicaccounts2017changematrix",
    "sourceEvidence": {
      "pointer": "/items/640",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Provides details of the changes to UK Economic Accounts tables.",
    "title": "UK Economic Accounts 2017 change matrix",
    "topics": [
      "7859",
      "1245",
      "2735"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/nationalaccounts/uksectoraccounts/datasets/ukeconomicaccounts2017changematrix"
  }
}
---

# UK Economic Accounts 2017 change matrix

Provides details of the changes to UK Economic Accounts tables

Native identifier: `/economy/nationalaccounts/uksectoraccounts/datasets/ukeconomicaccounts2017changematrix`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/ukeconomicaccounts2017changematrix)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
