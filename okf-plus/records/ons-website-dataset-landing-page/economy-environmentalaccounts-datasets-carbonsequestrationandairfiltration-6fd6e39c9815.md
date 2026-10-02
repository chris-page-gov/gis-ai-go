---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fenvironmentalaccounts%2Fdatasets%2Fcarbonsequestrationandairfiltration",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Carbon sequestration and air filtration",
  "description": "Provides time series data for the carbon sequestration and air filtration ecosystem services in the urban environment.",
  "nativeIdentifier": "/economy/environmentalaccounts/datasets/carbonsequestrationandairfiltration",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/environmentalaccounts/datasets/carbonsequestrationandairfiltration",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "carbon",
    "pollution",
    "urban",
    "natural capital",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/397",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/397",
      "normalisedRecordSha256": "aeab284a61a3bf4f2faa8657249fe1ea8641cceaaceedd151949be7b406d61fc",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/environmentalaccounts/datasets/carbonsequestrationandairfiltration"
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
    "id": "/economy/environmentalaccounts/datasets/carbonsequestrationandairfiltration",
    "keywords": [
      "carbon",
      "pollution",
      "urban",
      "natural capital"
    ],
    "meta_description": "Provides time series data for the carbon sequestration and air filtration ecosystem services in the urban environment.",
    "nativeIdentityField": "uri",
    "release_date": "2019-08-07T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/environmentalaccounts/datasets/carbonsequestrationandairfiltration",
    "sourceEvidence": {
      "pointer": "/items/397",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Provides time series data for the carbon sequestration and air filtration ecosystem services in the urban environment.",
    "title": "Carbon sequestration and air filtration",
    "topics": [
      "1245",
      "3322"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/environmentalaccounts/datasets/carbonsequestrationandairfiltration"
  }
}
---

# Carbon sequestration and air filtration

Provides time series data for the carbon sequestration and air filtration ecosystem services in the urban environment.

Native identifier: `/economy/environmentalaccounts/datasets/carbonsequestrationandairfiltration`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/environmentalaccounts/datasets/carbonsequestrationandairfiltration)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
