---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/source-families/os-product-catalogue",
  "@type": [
    "dcat:Catalog",
    "okfp:MetadataRecord"
  ],
  "type": "SourceFamily",
  "title": "OS product and service catalogue",
  "description": "Broader catalogue of downloads, APIs and services including products outside the OpenData API.",
  "nativeIdentifier": "os-product-catalogue",
  "sourceFamily": "source-families",
  "resource": "https://www.ordnancesurvey.co.uk/products/search-for-os-products",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "assertionStatus": "normalised",
  "reviewStatus": "source-review-recorded",
  "tags": [
    "os",
    "catalogue",
    "coverage",
    "updates"
  ],
  "sources": [
    {
      "resource": "https://www.ordnancesurvey.co.uk/products/search-for-os-products",
      "evidenceKind": "official-reference",
      "reviewedOn": "2026-10-02",
      "reviewBasis": "OKF-220 OS/ONS source reviews; reference does not imply full catalogue traversal."
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ordnancesurvey.co.uk/products/search-for-os-products"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "not-applicable",
    "kind": "dataset-reference-period",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "Dataset reference-period extent is not applicable to this record type."
  },
  "update": {
    "frequency": {
      "status": "not-applicable",
      "label": null,
      "iri": null,
      "sourceField": null
    },
    "releaseCatalogue": [
      "https://docs.os.uk/os-downloads/resources/product-resources/end-of-life-product-notices"
    ],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": null,
    "releaseVersion": null
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "Source-family coverage status is separate from product count, schema coverage, semantic curation and live Ask OKF admission."
  ],
  "details": {
    "inventoryStatus": "captured-http-partial-rendered-supplement",
    "sourceLane": "os-product-catalogue",
    "globalDenominator": "not-established",
    "captureFamilies": [
      "os-product-search"
    ]
  },
  "dcterms:publisher": {
    "@id": "https://www.ordnancesurvey.co.uk/"
  },
  "okfp:machineImported": false
}
---

# OS product and service catalogue

Broader catalogue of downloads, APIs and services including products outside the OpenData API.

Inventory state: `captured-http-partial-rendered-supplement`.

[Official source](https://www.ordnancesurvey.co.uk/products/search-for-os-products)

[Update and release discovery](https://docs.os.uk/os-downloads/resources/product-resources/end-of-life-product-notices)

This record describes the source lane. Consult the generated coverage report and captured receipts for measured counts; do not infer a complete inventory from a reviewed link.
