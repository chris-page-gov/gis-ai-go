---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Finflationandpriceindices%2Fdatasets%2Funderstandingthedifferentapproachesofmeasuringowneroccupiershousingcostsoohweightsanalysis",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Measures of owner occupiers’ housing costs: weights analysis",
  "description": "Aggregate inflation measure for owner occupiers' housing costs (OOH). Includes quarterly time series and weights for all three approaches of measuring OOH – payments, rental equivalence and net acquisitions – aggregated with consumer price index (CPI), UK.",
  "nativeIdentifier": "/economy/inflationandpriceindices/datasets/understandingthedifferentapproachesofmeasuringowneroccupiershousingcostsoohweightsanalysis",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/understandingthedifferentapproachesofmeasuringowneroccupiershousingcostsoohweightsanalysis",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "payments",
    "inflation",
    "CPIH",
    "CPI",
    "acquisitions",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/260",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2260",
      "normalisedRecordSha256": "adf617f3bed043573bf7e0e65251fd50710f12fa6f4c665bff657ae117deee4e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/understandingthedifferentapproachesofmeasuringowneroccupiershousingcostsoohweightsanalysis"
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
    "id": "/economy/inflationandpriceindices/datasets/understandingthedifferentapproachesofmeasuringowneroccupiershousingcostsoohweightsanalysis",
    "keywords": [
      "payments",
      "inflation",
      "CPIH",
      "CPI",
      "acquisitions"
    ],
    "meta_description": "Aggregate inflation measure for owner occupiers' housing costs (OOH). Includes quarterly time series and weights for all three approaches of measuring OOH – payments, rental equivalence and net acquisitions – aggregated with consumer price index (CPI), UK.",
    "nativeIdentityField": "uri",
    "release_date": "2021-03-24T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/understandingthedifferentapproachesofmeasuringowneroccupiershousingcostsoohweightsanalysis",
    "sourceEvidence": {
      "pointer": "/items/260",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "Aggregate inflation measure for owner occupiers' housing costs (OOH). Includes monthly time series and weights for all three approaches of measuring OOH – payments, rental equivalence and net acquisitions – aggregated with the Consumer Price Index (CPI), UK.",
    "title": "Measures of owner occupiers’ housing costs: weights analysis",
    "topics": [
      "1245",
      "4972"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/inflationandpriceindices/datasets/understandingthedifferentapproachesofmeasuringowneroccupiershousingcostsoohweightsanalysis"
  }
}
---

# Measures of owner occupiers’ housing costs: weights analysis

Aggregate inflation measure for owner occupiers' housing costs (OOH). Includes quarterly time series and weights for all three approaches of measuring OOH – payments, rental equivalence and net acquisitions – aggregated with consumer price index (CPI), UK.

Native identifier: `/economy/inflationandpriceindices/datasets/understandingthedifferentapproachesofmeasuringowneroccupiershousingcostsoohweightsanalysis`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/understandingthedifferentapproachesofmeasuringowneroccupiershousingcostsoohweightsanalysis)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
