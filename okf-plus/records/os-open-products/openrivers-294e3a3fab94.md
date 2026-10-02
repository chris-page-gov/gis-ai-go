---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-open-products/OpenRivers",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "OS Open Rivers",
  "description": "An open dataset of the high-level view of watercourse in Great Britain.",
  "nativeIdentifier": "OpenRivers",
  "sourceFamily": "os-open-products",
  "resource": "https://api.os.uk/downloads/v1/products/OpenRivers",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "water",
    "Vector"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/downloads/v1/products/OpenRivers",
      "retrievedAt": "2026-10-02T01:18:00.372364Z",
      "responseSha256": "90550edcf615558bcc2f784847e101cbcde63285d84d435946ccccd1fab72f57",
      "sourcePointer": "",
      "normalisedSource": "okf-plus/source/os-open-products.json",
      "normalisedPointer": "/records/17",
      "normalisedRecordSha256": "3b08929c054b898e4918964da149883744e73f649644c92fb75d0ec8979d917b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/downloads/v1/products/OpenRivers"
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
      "https://api.os.uk/downloads/v1/products/OpenRivers",
      "https://docs.os.uk/os-downloads/products/water-portfolio/os-open-rivers/os-open-rivers-overview"
    ],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": null,
    "releaseVersion": "2026-04"
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
      "water"
    ],
    "category": "Networks",
    "dataStructures": [
      "Vector"
    ],
    "description": [
      "An open dataset of the high-level view of watercourse in Great Britain."
    ],
    "documentationUrl": "https://docs.os.uk/os-downloads/products/water-portfolio/os-open-rivers/os-open-rivers-overview",
    "downloadsUrl": "https://api.os.uk/downloads/v1/products/OpenRivers/downloads",
    "formats": [
      {
        "format": "ESRI® Shapefile"
      },
      {
        "format": "GML",
        "subformat": "3"
      },
      {
        "format": "GeoPackage"
      },
      {
        "format": "Vector Tiles",
        "subformat": "(MBTiles)"
      }
    ],
    "id": "OpenRivers",
    "name": "OS Open Rivers",
    "supportingInfo": [
      {
        "link": "https://docs.os.uk/os-downloads/products/water-portfolio/os-open-rivers/os-open-rivers-technical-specification",
        "name": "Technical Specification"
      }
    ],
    "url": "https://api.os.uk/downloads/v1/products/OpenRivers",
    "version": "2026-04"
  }
}
---

# OS Open Rivers

An open dataset of the high-level view of watercourse in Great Britain.

Native identifier: `OpenRivers`.

Source family: `os-open-products`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/downloads/v1/products/OpenRivers)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://api.os.uk/downloads/v1/products/OpenRivers)
[Release catalogue or change-discovery route](https://docs.os.uk/os-downloads/products/water-portfolio/os-open-rivers/os-open-rivers-overview)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
