---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fgrossdomesticproductgdp%2Fdatasets%2Fbluebook2025advancedaggregateestimates",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Blue Book 2025: advanced aggregate estimates",
  "description": "Annual and quarterly data for UK gross domestic product (GDP) estimates, in chained volume measures and current market prices.",
  "nativeIdentifier": "/economy/grossdomesticproductgdp/datasets/bluebook2025advancedaggregateestimates",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/bluebook2025advancedaggregateestimates",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "BB25",
    "bluebook 2025",
    "UK National Accounts",
    "revisions",
    "growth rates",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/300",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/300",
      "normalisedRecordSha256": "b384b0c8fec2c3b4301a9fbf4bff3b54d246d7c1397755accaa2588335ed726b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/bluebook2025advancedaggregateestimates"
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
    "id": "/economy/grossdomesticproductgdp/datasets/bluebook2025advancedaggregateestimates",
    "keywords": [
      "BB25",
      "bluebook 2025",
      "UK National Accounts",
      "revisions",
      "growth rates"
    ],
    "meta_description": "Annual and quarterly data for UK gross domestic product (GDP) estimates, in chained volume measures and current market prices.",
    "nativeIdentityField": "uri",
    "release_date": "2025-08-18T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/bluebook2025advancedaggregateestimates",
    "sourceEvidence": {
      "pointer": "/items/300",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Annual and quarterly data for UK gross domestic product (GDP) estimates, in chained volume measures and current market prices.",
    "title": "Blue Book 2025: advanced aggregate estimates",
    "topics": [
      "1245",
      "9691"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/grossdomesticproductgdp/datasets/bluebook2025advancedaggregateestimates"
  }
}
---

# Blue Book 2025: advanced aggregate estimates

Annual and quarterly data for UK gross domestic product (GDP) estimates, in chained volume measures and current market prices.

Native identifier: `/economy/grossdomesticproductgdp/datasets/bluebook2025advancedaggregateestimates`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/bluebook2025advancedaggregateestimates)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
