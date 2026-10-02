---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/source-families/os-download-guides",
  "@type": [
    "dcat:Catalog",
    "okfp:MetadataRecord"
  ],
  "type": "SourceFamily",
  "title": "OS download product specifications and release notes",
  "description": "The complete published navigation index and two selected refresh/withdrawal guides are captured. Other indexed product guides, specifications and release histories remain references; the index includes historic/template pages.",
  "nativeIdentifier": "os-download-guides",
  "sourceFamily": "source-families",
  "resource": "https://docs.os.uk/os-downloads",
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
      "resource": "https://docs.os.uk/os-downloads",
      "evidenceKind": "official-reference",
      "reviewedOn": "2026-10-02",
      "reviewBasis": "OKF-220 OS/ONS source reviews; reference does not imply full catalogue traversal."
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-downloads"
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
      "https://docs.os.uk/os-downloads/resources/product-resources/product-refresh-dates"
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
    "Source-family coverage status is separate from product count, schema coverage, semantic curation and live Ask OKF admission.",
    "Only two selected Download guide pages are structurally projected; remaining index entries do not prove content capture.",
    "Captured refresh and withdrawal guides do not establish a complete release or retirement-event history."
  ],
  "details": {
    "inventoryStatus": "captured-index-selected-guide-structures",
    "sourceLane": "os-download-guides",
    "globalDenominator": "not-established",
    "captureFamilies": [
      "os-downloads-documentation",
      "os-download-guide-pages"
    ]
  },
  "dcterms:publisher": {
    "@id": "https://www.ordnancesurvey.co.uk/"
  },
  "okfp:machineImported": false
}
---

# OS download product specifications and release notes

The complete published navigation index and two selected refresh/withdrawal guides are captured. Other indexed product guides, specifications and release histories remain references; the index includes historic/template pages.

Inventory state: `captured-index-selected-guide-structures`.

[Official source](https://docs.os.uk/os-downloads)

[Update and release discovery](https://docs.os.uk/os-downloads/resources/product-resources/product-refresh-dates)

This record describes the source lane. Consult the generated coverage report and captured receipts for measured counts; do not infer a complete inventory from a reviewed link.

The published navigation inventory contains 1,673 distinct URLs. The separate selected cohort contains two pages: product refresh dates and end-of-life product notices; both were captured and structurally projected. These two pages are part of the index, not additional products or proof that all 1,673 page contents were acquired. The seven-guide lifecycle capture overlaps these references and must not be added as seven further unique pages. Refresh schedules, data-cut dates and withdrawal dates require source-specific interpretation; the withdrawal page projection preserves structure and references without extracting a complete retirement-event history.
