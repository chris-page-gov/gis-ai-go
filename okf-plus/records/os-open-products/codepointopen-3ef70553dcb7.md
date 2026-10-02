---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-open-products/CodePointOpen",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Code-Point® Open",
  "description": "An open dataset of all the current postcode units in Great Britain. Get started with geographical analysis, simple route planning and asset management.",
  "nativeIdentifier": "CodePointOpen",
  "sourceFamily": "os-open-products",
  "resource": "https://api.os.uk/downloads/v1/products/CodePointOpen",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "addressesAndNames",
    "areasAndZones",
    "Vector"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/downloads/v1/products/CodePointOpen",
      "retrievedAt": "2026-10-02T01:17:58.500725Z",
      "responseSha256": "e4becaaad09c4745e19ee513f6d580a64b699cfe02e7c197f55183fe57163266",
      "sourcePointer": "",
      "normalisedSource": "okf-plus/source/os-open-products.json",
      "normalisedPointer": "/records/10",
      "normalisedRecordSha256": "0af6196b340b635cf42c128e2f56ef63f5a77e114d847da2edf0a77ddbc7dab9",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/downloads/v1/products/CodePointOpen"
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
      "https://api.os.uk/downloads/v1/products/CodePointOpen",
      "https://docs.os.uk/os-downloads/products/areas-and-zones-portfolio/code-point-open/code-point-open-overview"
    ],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": null,
    "releaseVersion": "2026-08"
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "OpenData catalogue entry; consult product attribution and licence, including partner rights.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [],
  "details": {
    "areas": [
      "GB"
    ],
    "categories": [
      "addressesAndNames",
      "areasAndZones"
    ],
    "category": "Lookups",
    "dataStructures": [
      "Vector"
    ],
    "description": [
      "An open dataset of all the current postcode units in Great Britain. Get started with geographical analysis, simple route planning and asset management."
    ],
    "documentationUrl": "https://docs.os.uk/os-downloads/products/areas-and-zones-portfolio/code-point-open/code-point-open-overview",
    "downloadsUrl": "https://api.os.uk/downloads/v1/products/CodePointOpen/downloads",
    "formats": [
      {
        "format": "CSV"
      },
      {
        "format": "GeoPackage"
      }
    ],
    "id": "CodePointOpen",
    "name": "Code-Point® Open",
    "supportingInfo": [
      {
        "link": "https://docs.os.uk/os-downloads/products/areas-and-zones-portfolio/code-point-open/code-point-open-technical-specification",
        "name": "Technical Specification"
      },
      {
        "link": "https://docs.os.uk/os-downloads/products/areas-and-zones-portfolio/code-point-open/code-point-open-getting-started-guide",
        "name": "Getting Started"
      }
    ],
    "url": "https://api.os.uk/downloads/v1/products/CodePointOpen",
    "version": "2026-08"
  }
}
---

# Code-Point® Open

An open dataset of all the current postcode units in Great Britain. Get started with geographical analysis, simple route planning and asset management.

Native identifier: `CodePointOpen`.

Source family: `os-open-products`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/downloads/v1/products/CodePointOpen)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://api.os.uk/downloads/v1/products/CodePointOpen)
[Release catalogue or change-discovery route](https://docs.os.uk/os-downloads/products/areas-and-zones-portfolio/code-point-open/code-point-open-overview)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
