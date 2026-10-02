---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Feconomy%2Fgrossdomesticproductgdp%2Fdatasets%2Fvatderivednonseasonallyadjustedcurrentpriceturnoverforukmanufacturingandasubsetoftheukservicesindustriessic2007withoutadjustmentfornonresponsemillion",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "VAT-derived non-seasonally adjusted current price turnover for UK manufacturing and a subset of the UK services industries (SIC 2007) without adjustment for non-response, £ million",
  "description": "VAT Turnover estimates for UK manufacturing and a sub-set of the UK services industries from Quarter 1 2014 to Quarter 2 2016.",
  "nativeIdentifier": "/economy/grossdomesticproductgdp/datasets/vatderivednonseasonallyadjustedcurrentpriceturnoverforukmanufacturingandasubsetoftheukservicesindustriessic2007withoutadjustmentfornonresponsemillion",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/vatderivednonseasonallyadjustedcurrentpriceturnoverforukmanufacturingandasubsetoftheukservicesindustriessic2007withoutadjustmentfornonresponsemillion",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "GDP",
    "National Accounts",
    "standard industrial classification",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/794",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3794",
      "normalisedRecordSha256": "f63d34e9e6251537e777eebc72bc12da86363ce3465d791eaad646c47f4cd2b6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/vatderivednonseasonallyadjustedcurrentpriceturnoverforukmanufacturingandasubsetoftheukservicesindustriessic2007withoutadjustmentfornonresponsemillion"
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
    "id": "/economy/grossdomesticproductgdp/datasets/vatderivednonseasonallyadjustedcurrentpriceturnoverforukmanufacturingandasubsetoftheukservicesindustriessic2007withoutadjustmentfornonresponsemillion",
    "keywords": [
      "GDP",
      "National Accounts",
      "standard industrial classification"
    ],
    "meta_description": "VAT Turnover estimates for UK manufacturing and a sub-set of the UK services industries from Quarter 1 2014 to Quarter 2 2016.",
    "nativeIdentityField": "uri",
    "release_date": "2017-02-02T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/vatderivednonseasonallyadjustedcurrentpriceturnoverforukmanufacturingandasubsetoftheukservicesindustriessic2007withoutadjustmentfornonresponsemillion",
    "sourceEvidence": {
      "pointer": "/items/794",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "VAT turnover estimates for UK manufacturing and a sub-set of the UK services industries from Quarter 1 2014 to Quarter 2 2016. Also included are VAT turnover estimates at the 4 digit SIC level for Division 93 - Sports activities and amusement and recreation activities. The estimates presented in these tables are at current prices and are without adjustment for incompleteness (non-response).",
    "title": "VAT-derived non-seasonally adjusted current price turnover for UK manufacturing and a subset of the UK services industries (SIC 2007) without adjustment for non-response, £ million",
    "topics": [
      "1245",
      "9691"
    ],
    "type": "dataset_landing_page",
    "uri": "/economy/grossdomesticproductgdp/datasets/vatderivednonseasonallyadjustedcurrentpriceturnoverforukmanufacturingandasubsetoftheukservicesindustriessic2007withoutadjustmentfornonresponsemillion"
  }
}
---

# VAT-derived non-seasonally adjusted current price turnover for UK manufacturing and a subset of the UK services industries (SIC 2007) without adjustment for non-response, £ million

VAT Turnover estimates for UK manufacturing and a sub-set of the UK services industries from Quarter 1 2014 to Quarter 2 2016.

Native identifier: `/economy/grossdomesticproductgdp/datasets/vatderivednonseasonallyadjustedcurrentpriceturnoverforukmanufacturingandasubsetoftheukservicesindustriessic2007withoutadjustmentfornonresponsemillion`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/vatderivednonseasonallyadjustedcurrentpriceturnoverforukmanufacturingandasubsetoftheukservicesindustriessic2007withoutadjustmentfornonresponsemillion)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
