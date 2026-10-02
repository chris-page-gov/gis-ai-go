---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Feconomy%2Fnationalaccounts%2Fsatelliteaccounts%2Fdatasets%2Fconsumertrendsimplieddeflatorseasonallyadjusted%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Consumer Trends: Implied Deflator, Seasonally Adjusted",
  "description": "Household expenditure full dataset, implied deflator, seasonally adjusted. The estimates published in this workbook are consistent with Blue Book",
  "nativeIdentifier": "/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted/current",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Household Spending",
    "Imputed Rental",
    "Personal Expenditure",
    "Spending per Head",
    "Classification of Individual Consumption by Purpose (COICOP)",
    "dataset"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "responseSha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "sourcePointer": "/items/334",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/334",
      "normalisedRecordSha256": "4055f097efb110a9c397ed4cb4d4b49c3f1076b28fbe34fd37f3cdb01361af32",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted/current"
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
    "releaseVersion": "Current"
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
    "edition": "Current",
    "id": "/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted/current",
    "keywords": [
      "Household Spending",
      "Imputed Rental",
      "Personal Expenditure",
      "Spending per Head",
      "Classification of Individual Consumption by Purpose (COICOP)"
    ],
    "meta_description": "Household expenditure full dataset, implied deflator, seasonally adjusted. The estimates published in this workbook are consistent with Blue Book",
    "nativeIdentityField": "uri",
    "release_date": "2016-01-05T09:20:40.465Z",
    "resource": "https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted/current",
    "sourceEvidence": {
      "pointer": "/items/334",
      "retrievedAt": "2026-10-02T07:58:47.412144Z",
      "sha256": "9a04b8223d1ab2edb2fc93446a4a9cbe8a51fa0e744c338f583cdb3a02145bba",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Household expenditure full dataset, implied deflator, seasonally adjusted. The estimates published in this workbook are consistent with Blue Book 2014.",
    "title": "Consumer Trends: Implied Deflator, Seasonally Adjusted",
    "topics": [
      "4176",
      "1245",
      "2735"
    ],
    "type": "dataset",
    "uri": "/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted/current"
  }
}
---

# Consumer Trends: Implied Deflator, Seasonally Adjusted

Household expenditure full dataset, implied deflator, seasonally adjusted. The estimates published in this workbook are consistent with Blue Book

Native identifier: `/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/datasets/consumertrendsimplieddeflatorseasonallyadjusted/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
