---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fbusinessindustryandtrade%2Fretailindustry%2Fdatasets%2Fretailsalesindexreportingperiods",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Retail Sales Index reporting periods",
  "description": "Reporting periods for the Retail Sales Index in Great Britain.",
  "nativeIdentifier": "/businessindustryandtrade/retailindustry/datasets/retailsalesindexreportingperiods",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/datasets/retailsalesindexreportingperiods",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "RSI",
    "goods bought",
    "buying",
    "spending",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/181",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3181",
      "normalisedRecordSha256": "0215085f87b1596556d0c2c6e0d7a9d02772120a2637ad99ce0b866c718ca51d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/datasets/retailsalesindexreportingperiods"
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
    "id": "/businessindustryandtrade/retailindustry/datasets/retailsalesindexreportingperiods",
    "keywords": [
      "RSI",
      "goods bought",
      "buying",
      "spending"
    ],
    "meta_description": "Reporting periods for the Retail Sales Index in Great Britain.",
    "nativeIdentityField": "uri",
    "release_date": "2025-11-21T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/datasets/retailsalesindexreportingperiods",
    "sourceEvidence": {
      "pointer": "/items/181",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Reporting periods for the Retail Sales Index in Great Britain.",
    "title": "Retail Sales Index reporting periods",
    "topics": [
      "9658",
      "3545"
    ],
    "type": "dataset_landing_page",
    "uri": "/businessindustryandtrade/retailindustry/datasets/retailsalesindexreportingperiods"
  }
}
---

# Retail Sales Index reporting periods

Reporting periods for the Retail Sales Index in Great Britain.

Native identifier: `/businessindustryandtrade/retailindustry/datasets/retailsalesindexreportingperiods`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/retailindustry/datasets/retailsalesindexreportingperiods)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
