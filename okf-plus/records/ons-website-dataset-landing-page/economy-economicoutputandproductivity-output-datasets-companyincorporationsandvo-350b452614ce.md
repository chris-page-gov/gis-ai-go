---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Feconomicoutputandproductivity%2Foutput%2Fdatasets%2Fcompanyincorporationsandvoluntarydissolutions",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Company incorporations, voluntary dissolutions and compulsory dissolutions",
  "description": "Weekly data showing the number of Companies House incorporations, voluntary dissolutions accepted, and companies placed into compulsory dissolution in the UK. These are official statistics in development. Source: Companies House.",
  "nativeIdentifier": "/economy/economicoutputandproductivity/output/datasets/companyincorporationsandvoluntarydissolutions",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/companyincorporationsandvoluntarydissolutions",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "realtimeindicators",
    "Company incorporation",
    "voluntary dissolution",
    "compulsory dissolution",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/536",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/536",
      "normalisedRecordSha256": "b927bd432db82d7074b73df10d4d490b9b3883043f2f4a3750431795c9b33c8d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/companyincorporationsandvoluntarydissolutions"
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
    "id": "/economy/economicoutputandproductivity/output/datasets/companyincorporationsandvoluntarydissolutions",
    "keywords": [
      "realtimeindicators",
      "Company incorporation",
      "voluntary dissolution",
      "compulsory dissolution"
    ],
    "meta_description": "Weekly data showing the number of Companies House incorporations, voluntary dissolutions accepted, and companies placed into compulsory dissolution in the UK. These are official statistics in development. Source: Companies House.",
    "nativeIdentityField": "uri",
    "release_date": "2025-01-30T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/companyincorporationsandvoluntarydissolutions",
    "sourceEvidence": {
      "pointer": "/items/536",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Weekly data showing the number of Companies House incorporations, voluntary dissolutions accepted, and companies placed into compulsory dissolution in the UK. These are official statistics in development. Source: Companies House.",
    "title": "Company incorporations, voluntary dissolutions and compulsory dissolutions",
    "topics": [
      "1245",
      "2621",
      "6625"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/economicoutputandproductivity/output/datasets/companyincorporationsandvoluntarydissolutions"
  }
}
---

# Company incorporations, voluntary dissolutions and compulsory dissolutions

Weekly data showing the number of Companies House incorporations, voluntary dissolutions accepted, and companies placed into compulsory dissolution in the UK. These are official statistics in development. Source: Companies House.

Native identifier: `/economy/economicoutputandproductivity/output/datasets/companyincorporationsandvoluntarydissolutions`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/companyincorporationsandvoluntarydissolutions)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
