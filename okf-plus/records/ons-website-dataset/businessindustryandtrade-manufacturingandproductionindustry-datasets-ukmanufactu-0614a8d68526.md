---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset/%2Fbusinessindustryandtrade%2Fmanufacturingandproductionindustry%2Fdatasets%2Fukmanufacturerssalesbyproductprodcomintermediateresults2013andfinalresults2012referencetables%2Fintermediateest_ualitymeasures",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "UK Manufacturers’ Sales by Product (PRODCOM): Intermediate Results 2013 and Final Results 2012 reference tables",
  "description": "The sales by UK based manufacturers of the individual products covered by the PRODCOM inquiry. It contains the quality measures for 2013 intermediate and final estimates for 2012 and intermediate estimates of manufacturers’ sales by product, from businesses based in the UK in 2013, and final estimates for 2012.",
  "nativeIdentifier": "/businessindustryandtrade/manufacturingandproductionindustry/datasets/ukmanufacturerssalesbyproductprodcomintermediateresults2013andfinalresults2012referencetables/intermediateest_ualitymeasures",
  "sourceFamily": "ons-website-dataset",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/manufacturingandproductionindustry/datasets/ukmanufacturerssalesbyproductprodcomintermediateresults2013andfinalresults2012referencetables/intermediateest_ualitymeasures",
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
      "sourcePointer": "/items/785",
      "normalisedSource": "okf-plus/source/ons-website-dataset.json",
      "normalisedPointer": "/records/1785",
      "normalisedRecordSha256": "021556c84e83020f2c596c5b61040ba4b50e1f0a03bb03257545367896e5f634",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/manufacturingandproductionindustry/datasets/ukmanufacturerssalesbyproductprodcomintermediateresults2013andfinalresults2012referencetables/intermediateest_ualitymeasures"
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
    "releaseVersion": "Intermediate Estimates 2013, Quality Measures"
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
    "edition": "Intermediate Estimates 2013, Quality Measures",
    "id": "/businessindustryandtrade/manufacturingandproductionindustry/datasets/ukmanufacturerssalesbyproductprodcomintermediateresults2013andfinalresults2012referencetables/intermediateest_ualitymeasures",
    "keywords": [],
    "meta_description": "The sales by UK based manufacturers of the individual products covered by the PRODCOM inquiry. It contains the quality measures for 2013 intermediate and final estimates for 2012 and intermediate estimates of manufacturers’ sales by product, from businesses based in the UK in 2013, and final estimates for 2012.",
    "nativeIdentityField": "uri",
    "release_date": "2014-12-18T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/manufacturingandproductionindustry/datasets/ukmanufacturerssalesbyproductprodcomintermediateresults2013andfinalresults2012referencetables/intermediateest_ualitymeasures",
    "sourceEvidence": {
      "pointer": "/items/785",
      "retrievedAt": "2026-10-02T07:58:48.612491Z",
      "sha256": "827bff4267a994c7c49a1be34a175d59ed55be78b2add562ce0c2326b8c4f2c1",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset&sort=title&highlight=false&limit=1000&offset=1000"
    },
    "summary": "The sales by UK based manufacturers of the individual products covered by the PRODCOM inquiry. It contains the quality measures for 2013 intermediate and final estimates for 2012 and intermediate estimates of manufacturers’ sales by product, from businesses based in the UK in 2013, and final estimates for 2012.",
    "title": "UK Manufacturers’ Sales by Product (PRODCOM): Intermediate Results 2013 and Final Results 2012 reference tables",
    "topics": [
      "9658",
      "8413"
    ],
    "type": "dataset",
    "uri": "/businessindustryandtrade/manufacturingandproductionindustry/datasets/ukmanufacturerssalesbyproductprodcomintermediateresults2013andfinalresults2012referencetables/intermediateest_ualitymeasures"
  }
}
---

# UK Manufacturers’ Sales by Product (PRODCOM): Intermediate Results 2013 and Final Results 2012 reference tables

The sales by UK based manufacturers of the individual products covered by the PRODCOM inquiry. It contains the quality measures for 2013 intermediate and final estimates for 2012 and intermediate estimates of manufacturers’ sales by product, from businesses based in the UK in 2013, and final estimates for 2012.

Native identifier: `/businessindustryandtrade/manufacturingandproductionindustry/datasets/ukmanufacturerssalesbyproductprodcomintermediateresults2013andfinalresults2012referencetables/intermediateest_ualitymeasures`.

Source family: `ons-website-dataset`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/manufacturingandproductionindustry/datasets/ukmanufacturerssalesbyproductprodcomintermediateresults2013andfinalresults2012referencetables/intermediateest_ualitymeasures)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
