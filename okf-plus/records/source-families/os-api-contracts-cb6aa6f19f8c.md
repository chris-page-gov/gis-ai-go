---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/source-families/os-api-contracts",
  "@type": [
    "dcat:Catalog",
    "okfp:MetadataRecord"
  ],
  "type": "SourceFamily",
  "title": "OS API specifications and technical guides",
  "description": "Separate OpenAPI fragments describe operations, constraints and security; documented operations are not admitted MCP tools.",
  "nativeIdentifier": "os-api-contracts",
  "sourceFamily": "source-families",
  "resource": "https://docs.os.uk/os-apis",
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
      "resource": "https://docs.os.uk/os-apis",
      "evidenceKind": "official-reference",
      "reviewedOn": "2026-10-02",
      "reviewBasis": "OKF-220 OS/ONS source reviews; reference does not imply full catalogue traversal."
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis"
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
      "https://docs.os.uk/os-apis"
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
    "inventoryStatus": "captured-documentation-and-contract-fragments",
    "sourceLane": "os-api-contracts",
    "globalDenominator": "not-established",
    "captureFamilies": [
      "os-api-contracts"
    ]
  },
  "dcterms:publisher": {
    "@id": "https://www.ordnancesurvey.co.uk/"
  },
  "okfp:machineImported": false
}
---

# OS API specifications and technical guides

Separate OpenAPI fragments describe operations, constraints and security; documented operations are not admitted MCP tools.

Inventory state: `captured-documentation-and-contract-fragments`.

[Official source](https://docs.os.uk/os-apis)

[Update and release discovery](https://docs.os.uk/os-apis)

This record describes the source lane. Consult the generated coverage report and captured receipts for measured counts; do not infer a complete inventory from a reviewed link.
