---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fnationalaccounts%2Fsatelliteaccounts%2Fdatasets%2Fconsumertrendsimplieddeflatorseasonallyadjusted",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Consumer trends: implied deflator, seasonally adjusted",
  "description": "Household expenditure full dataset, implied deflator, seasonally adjusted.",
  "nativeIdentifier": "/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "household spending",
    "personal expenditure",
    "spending per head",
    "classification of individual consumption by purpose",
    "COICOP",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/604",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/604",
      "normalisedRecordSha256": "2b7b6b377e8e34f4180062cd34e7fee3d83629c72037975dd388de5a8070ee5e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted"
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
    "id": "/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted",
    "keywords": [
      "household spending",
      "personal expenditure",
      "spending per head",
      "classification of individual consumption by purpose",
      "COICOP"
    ],
    "meta_description": "Household expenditure full dataset, implied deflator, seasonally adjusted.",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-29T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted",
    "sourceEvidence": {
      "pointer": "/items/604",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Quarterly and annual data for household expenditure in the UK, implied deflator, seasonally adjusted.",
    "title": "Consumer trends: implied deflator, seasonally adjusted",
    "topics": [
      "1245",
      "2735",
      "4176"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted"
  }
}
---

# Consumer trends: implied deflator, seasonally adjusted

Household expenditure full dataset, implied deflator, seasonally adjusted.

Native identifier: `/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
