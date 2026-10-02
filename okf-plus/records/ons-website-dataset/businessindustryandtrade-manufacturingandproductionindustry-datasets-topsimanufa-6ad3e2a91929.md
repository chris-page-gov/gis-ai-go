---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Fbusinessindustryandtrade%2Fmanufacturingandproductionindustry%2Fdatasets%2Ftopsimanufacturingexportturnover%2Fcurrent",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "TOPSI: Manufacturing Export Turnover",
  "description": "Current price turnover figures for Production industries by market (Export, Domestic and Total).",
  "nativeIdentifier": "/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover/current",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover/current",
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
      "sourcePointer": "/items/560",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/1560",
      "normalisedRecordSha256": "26417cbab815aebb3dce86e15fa4a5d94ae61bcbceb43ebb532205d38a4796a1",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover/current"
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
    "id": "/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover/current",
    "keywords": [],
    "meta_description": "Current price turnover figures for Production industries by market (Export, Domestic and Total).",
    "nativeIdentityField": "uri",
    "release_date": "2015-12-18T13:14:39.094Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover/current",
    "sourceEvidence": {
      "pointer": "/items/560",
      "retrievedAt": "2026-10-02T07:58:48.612491Z",
      "sha256": "827bff4267a994c7c49a1be34a175d59ed55be78b2add562ce0c2326b8c4f2c1",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "Current price turnover figures for Production industries by market (Export, Domestic and Total).",
    "title": "TOPSI: Manufacturing Export Turnover",
    "topics": [
      "9658",
      "8413"
    ],
    "type": "dataset",
    "uri": "/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover/current"
  }
}
---

# TOPSI: Manufacturing Export Turnover

Current price turnover figures for Production industries by market (Export, Domestic and Total).

Native identifier: `/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover/current`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/manufacturingandproductionindustry/datasets/topsimanufacturingexportturnover/current)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
