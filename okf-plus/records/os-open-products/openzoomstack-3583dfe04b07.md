---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-open-products/OpenZoomstack",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "OS Open Zoomstack",
  "description": "A comprehensive basemap of Great Britain showing coverage from national level right down to street detail.",
  "nativeIdentifier": "OpenZoomstack",
  "sourceFamily": "os-open-products",
  "resource": "https://api.os.uk/downloads/v1/products/OpenZoomstack",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "mapsAndImagery",
    "Vector"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/downloads/v1/products/OpenZoomstack",
      "retrievedAt": "2026-10-02T01:18:01.728105Z",
      "responseSha256": "6a82a72f35701aad0a2526bc703212f0d9716868f660dc1e9db6549e90afd450",
      "sourcePointer": "",
      "normalisedSource": "okf-plus/source/os-open-products.json",
      "normalisedPointer": "/records/22",
      "normalisedRecordSha256": "28b8a882dad27c10046886495cf8fd4afdfc3fe572f3834d394ddd6fad9ab93c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/downloads/v1/products/OpenZoomstack"
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
      "https://api.os.uk/downloads/v1/products/OpenZoomstack",
      "https://docs.os.uk/os-downloads/products/maps-and-imagery-portfolio/os-open-zoomstack"
    ],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": null,
    "releaseVersion": "2026-06"
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
      "mapsAndImagery"
    ],
    "category": "Mapping",
    "dataStructures": [
      "Vector"
    ],
    "description": [
      "A comprehensive basemap of Great Britain showing coverage from national level right down to street detail."
    ],
    "documentationUrl": "https://docs.os.uk/os-downloads/products/maps-and-imagery-portfolio/os-open-zoomstack",
    "downloadsUrl": "https://api.os.uk/downloads/v1/products/OpenZoomstack/downloads",
    "formats": [
      {
        "format": "GeoPackage"
      },
      {
        "format": "Vector Tiles",
        "subformat": "(MBTiles)"
      }
    ],
    "id": "OpenZoomstack",
    "name": "OS Open Zoomstack",
    "supportingInfo": [
      {
        "link": "https://docs.os.uk/os-downloads/products/maps-and-imagery-portfolio/os-open-zoomstack/os-open-zoomstack-technical-specification",
        "name": "Technical Specification"
      },
      {
        "link": "https://docs.os.uk/os-downloads/products/maps-and-imagery-portfolio/os-open-zoomstack/os-open-zoomstack-getting-started-guide",
        "name": "Getting Started"
      }
    ],
    "url": "https://api.os.uk/downloads/v1/products/OpenZoomstack",
    "version": "2026-06"
  }
}
---

# OS Open Zoomstack

A comprehensive basemap of Great Britain showing coverage from national level right down to street detail.

Native identifier: `OpenZoomstack`.

Source family: `os-open-products`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/downloads/v1/products/OpenZoomstack)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://api.os.uk/downloads/v1/products/OpenZoomstack)
[Release catalogue or change-discovery route](https://docs.os.uk/os-downloads/products/maps-and-imagery-portfolio/os-open-zoomstack)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
