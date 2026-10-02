---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-open-products/OpenNames",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "OS Open Names",
  "description": "A comprehensive dataset of place names, roads numbers and postcodes for Great Britain.",
  "nativeIdentifier": "OpenNames",
  "sourceFamily": "os-open-products",
  "resource": "https://api.os.uk/downloads/v1/products/OpenNames",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "addressesAndNames",
    "Vector"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/downloads/v1/products/OpenNames",
      "retrievedAt": "2026-10-02T01:18:00.122039Z",
      "responseSha256": "aae35bb5c233ab608e1eaf99bbf26bdcc7f503ee4fed1c629e7a6e9525502379",
      "sourcePointer": "",
      "normalisedSource": "okf-plus/source/os-open-products.json",
      "normalisedPointer": "/records/16",
      "normalisedRecordSha256": "b1ba313edfb1a0645455921f76c9b719aeb78ba47937e14bb5d78fc501f267c6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/downloads/v1/products/OpenNames"
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
      "https://api.os.uk/downloads/v1/products/OpenNames",
      "https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/os-open-names/os-open-names-overview"
    ],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": null,
    "releaseVersion": "2026-07"
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
      "addressesAndNames"
    ],
    "category": "Lookups",
    "dataStructures": [
      "Vector"
    ],
    "description": [
      "A comprehensive dataset of place names, roads numbers and postcodes for Great Britain."
    ],
    "documentationUrl": "https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/os-open-names/os-open-names-overview",
    "downloadsUrl": "https://api.os.uk/downloads/v1/products/OpenNames/downloads",
    "formats": [
      {
        "format": "CSV"
      },
      {
        "format": "GML",
        "subformat": "3"
      },
      {
        "format": "GeoPackage"
      }
    ],
    "id": "OpenNames",
    "name": "OS Open Names",
    "supportingInfo": [
      {
        "link": "https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/os-open-names/os-open-names-technical-specification",
        "name": "Technical Specification"
      },
      {
        "link": "https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/os-open-names/os-open-names-getting-started-guide",
        "name": "Getting Started"
      }
    ],
    "url": "https://api.os.uk/downloads/v1/products/OpenNames",
    "version": "2026-07"
  }
}
---

# OS Open Names

A comprehensive dataset of place names, roads numbers and postcodes for Great Britain.

Native identifier: `OpenNames`.

Source family: `os-open-products`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/downloads/v1/products/OpenNames)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://api.os.uk/downloads/v1/products/OpenNames)
[Release catalogue or change-discovery route](https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/os-open-names/os-open-names-overview)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
