---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/source-families/os-gemini",
  "@type": [
    "dcat:Catalog",
    "okfp:MetadataRecord"
  ],
  "type": "SourceFamily",
  "title": "OS GEMINI metadata catalogue",
  "description": "Metadata records declare products, themes, dates and profiles. Catalogue items are metadata, not NGD feature items.",
  "nativeIdentifier": "os-gemini",
  "sourceFamily": "source-families",
  "resource": "https://osmetadata.astuntechnology.com/geonetwork",
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
      "resource": "https://osmetadata.astuntechnology.com/geonetwork",
      "evidenceKind": "official-reference",
      "reviewedOn": "2026-10-02",
      "reviewBasis": "OKF-220 OS/ONS source reviews; reference does not imply full catalogue traversal."
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://osmetadata.astuntechnology.com/geonetwork"
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
      "https://osmetadata.astuntechnology.com/geonetwork/api/collections/main/items?f=rss&sortby=-createDate&size=30"
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
    "inventoryStatus": "captured-catalogue",
    "sourceLane": "os-gemini",
    "globalDenominator": "not-established",
    "captureFamilies": [
      "os-gemini-metadata"
    ]
  },
  "dcterms:publisher": {
    "@id": "https://www.ordnancesurvey.co.uk/"
  },
  "okfp:machineImported": false
}
---

# OS GEMINI metadata catalogue

Metadata records declare products, themes, dates and profiles. Catalogue items are metadata, not NGD feature items.

Inventory state: `captured-catalogue`.

[Official source](https://osmetadata.astuntechnology.com/geonetwork)

[Update and release discovery](https://osmetadata.astuntechnology.com/geonetwork/api/collections/main/items?f=rss&sortby=-createDate&size=30)

This record describes the source lane. Consult the generated coverage report and captured receipts for measured counts; do not infer a complete inventory from a reviewed link.
