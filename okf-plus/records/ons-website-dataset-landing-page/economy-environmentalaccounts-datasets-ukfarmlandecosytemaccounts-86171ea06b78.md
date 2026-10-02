---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fenvironmentalaccounts%2Fdatasets%2Fukfarmlandecosytemaccounts",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "UK Farmland Ecosytem Accounts",
  "description": "Farmland ecosystem extent and condition accounts, physical flows of ecosystem services, bird populations, protected farmlands and mean richness scores from the Countryside Survey.",
  "nativeIdentifier": "/economy/environmentalaccounts/datasets/ukfarmlandecosytemaccounts",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/environmentalaccounts/datasets/ukfarmlandecosytemaccounts",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/656",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3656",
      "normalisedRecordSha256": "3b3e400ac1d3c3c366da1d675bd7a3b1f61ab05e965daf95e2edbc6f80e18a77",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/environmentalaccounts/datasets/ukfarmlandecosytemaccounts"
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
    "id": "/economy/environmentalaccounts/datasets/ukfarmlandecosytemaccounts",
    "keywords": [],
    "meta_description": "Farmland ecosystem extent and condition accounts, physical flows of ecosystem services, bird populations, protected farmlands and mean richness scores from the Countryside Survey.",
    "nativeIdentityField": "uri",
    "release_date": "2016-02-15T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/environmentalaccounts/datasets/ukfarmlandecosytemaccounts",
    "sourceEvidence": {
      "pointer": "/items/656",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Farmland ecosystem extent and condition accounts, physical flows of ecosystem services, bird populations, protected farmlands and mean richness scores from the Countryside Survey.",
    "title": "UK Farmland Ecosytem Accounts",
    "topics": [
      "1245",
      "3322"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/environmentalaccounts/datasets/ukfarmlandecosytemaccounts"
  }
}
---

# UK Farmland Ecosytem Accounts

Farmland ecosystem extent and condition accounts, physical flows of ecosystem services, bird populations, protected farmlands and mean richness scores from the Countryside Survey.

Native identifier: `/economy/environmentalaccounts/datasets/ukfarmlandecosytemaccounts`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/environmentalaccounts/datasets/ukfarmlandecosytemaccounts)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
