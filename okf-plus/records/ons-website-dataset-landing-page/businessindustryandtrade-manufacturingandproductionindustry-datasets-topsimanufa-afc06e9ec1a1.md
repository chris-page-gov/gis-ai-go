---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fbusinessindustryandtrade%2Fmanufacturingandproductionindustry%2Fdatasets%2Ftopsimanufacturingexportturnover",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Turnover in UK production and Great Britain services industries: monthly manufacturing export turnover",
  "description": "Current price turnover figures for production industries by market (export, domestic and total).",
  "nativeIdentifier": "/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "products",
    "index of production",
    "TOPSI",
    "business economy",
    "IoP",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/631",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3631",
      "normalisedRecordSha256": "73aab6d50108f38778b3ac0d0c4ae577f102a28909420d08b37d84d40a1a3680",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover"
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
    "id": "/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover",
    "keywords": [
      "products",
      "index of production",
      "TOPSI",
      "business economy",
      "IoP"
    ],
    "meta_description": "Current price turnover figures for production industries by market (export, domestic and total).",
    "nativeIdentityField": "uri",
    "release_date": "2017-11-10T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover",
    "sourceEvidence": {
      "pointer": "/items/631",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Current price turnover figures for production industries by market (export, domestic and total).",
    "title": "Turnover in UK production and Great Britain services industries: monthly manufacturing export turnover",
    "topics": [
      "8413",
      "9658"
    ],
    "type": "dataset_landing_page",
    "uri": "/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover"
  }
}
---

# Turnover in UK production and Great Britain services industries: monthly manufacturing export turnover

Current price turnover figures for production industries by market (export, domestic and total).

Native identifier: `/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
