---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Finflationandpriceindices%2Fdatasets%2Fdiscretionaryandnondiscretionaryconsumerpriceindicescpi",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Discretionary and non-discretionary Consumer Price Indices (CPI)",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/inflationandpriceindices/datasets/discretionaryandnondiscretionaryconsumerpriceindicescpi",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/discretionaryandnondiscretionaryconsumerpriceindicescpi",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/905",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/905",
      "normalisedRecordSha256": "43473773edf9f7e6e5ea7da588d16f113ff15e03c85b44481a4fb13b3d26d096",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/discretionaryandnondiscretionaryconsumerpriceindicescpi"
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
    "id": "/economy/inflationandpriceindices/datasets/discretionaryandnondiscretionaryconsumerpriceindicescpi",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2021-12-15T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/discretionaryandnondiscretionaryconsumerpriceindicescpi",
    "sourceEvidence": {
      "pointer": "/items/905",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Consumer Price Indices (CPI) data for discretionary and non-discretionary spending inflation in the UK.",
    "title": "Discretionary and non-discretionary Consumer Price Indices (CPI)",
    "topics": [
      "4972",
      "1245"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/inflationandpriceindices/datasets/discretionaryandnondiscretionaryconsumerpriceindicescpi"
  }
}
---

# Discretionary and non-discretionary Consumer Price Indices (CPI)

ONS website catalogue metadata.

Native identifier: `/economy/inflationandpriceindices/datasets/discretionaryandnondiscretionaryconsumerpriceindicescpi`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/discretionaryandnondiscretionaryconsumerpriceindicescpi)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
