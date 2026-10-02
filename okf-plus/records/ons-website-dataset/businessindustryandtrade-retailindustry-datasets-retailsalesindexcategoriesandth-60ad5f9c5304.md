---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Fbusinessindustryandtrade%2Fretailindustry%2Fdatasets%2Fretailsalesindexcategoriesandtheirpercentageweights%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Retail sales index categories and their percentage weights",
  "description": "Retail sales categories and descriptions and their percentage of all retailing.",
  "nativeIdentifier": "/businessindustryandtrade/retailindustry/datasets/retailsalesindexcategoriesandtheirpercentageweights/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/datasets/retailsalesindexcategoriesandtheirpercentageweights/current",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "dataset"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=1000",
      "retrievedAt": "2026-10-02T07:58:48.612491Z",
      "responseSha256": "827bff4267a994c7c49a1be34a175d59ed55be78b2add562ce0c2326b8c4f2c1",
      "sourcePointer": "/items/484",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/1484",
      "normalisedRecordSha256": "f963b34979372430685326b32f076edf8c7174f4bc74b2760d52f1daedd548e1",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/datasets/retailsalesindexcategoriesandtheirpercentageweights/current"
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
    "id": "/businessindustryandtrade/retailindustry/datasets/retailsalesindexcategoriesandtheirpercentageweights/current",
    "keywords": [],
    "meta_description": "Retail sales categories and descriptions and their percentage of all retailing.",
    "nativeIdentityField": "uri",
    "release_date": "2015-12-21T09:01:42.079Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/datasets/retailsalesindexcategoriesandtheirpercentageweights/current",
    "sourceEvidence": {
      "pointer": "/items/484",
      "retrievedAt": "2026-10-02T07:58:48.612491Z",
      "sha256": "827bff4267a994c7c49a1be34a175d59ed55be78b2add562ce0c2326b8c4f2c1",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Retail sales categories and descriptions and their percentage of all retailing.",
    "title": "Retail sales index categories and their percentage weights",
    "topics": [
      "9658",
      "3545"
    ],
    "type": "dataset",
    "uri": "/businessindustryandtrade/retailindustry/datasets/retailsalesindexcategoriesandtheirpercentageweights/current"
  }
}
---

# Retail sales index categories and their percentage weights

Retail sales categories and descriptions and their percentage of all retailing.

Native identifier: `/businessindustryandtrade/retailindustry/datasets/retailsalesindexcategoriesandtheirpercentageweights/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/retailindustry/datasets/retailsalesindexcategoriesandtheirpercentageweights/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
