---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-open-products/OpenRoads",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "OS Open Roads",
  "description": "Get a high-level view of the road network, from motorways to country lanes.",
  "nativeIdentifier": "OpenRoads",
  "sourceFamily": "os-open-products",
  "resource": "https://api.os.uk/downloads/v1/products/OpenRoads",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "transportNetworks",
    "Vector"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/downloads/v1/products/OpenRoads",
      "retrievedAt": "2026-10-02T01:18:00.633766Z",
      "responseSha256": "b69675fb481c193a6cd1e4a938933395dd349952e95b5075bd181144e34b5396",
      "sourcePointer": "",
      "normalisedSource": "okf-plus/source/os-open-products.json",
      "normalisedPointer": "/records/18",
      "normalisedRecordSha256": "a17279018614f187522e4faed435e0ab7c28db8b1403031dea18d00c2b6a833b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/downloads/v1/products/OpenRoads"
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
      "https://api.os.uk/downloads/v1/products/OpenRoads",
      "https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-open-roads/os-open-roads-overview"
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
      "transportNetworks"
    ],
    "category": "Networks",
    "dataStructures": [
      "Vector"
    ],
    "description": [
      "Get a high-level view of the road network, from motorways to country lanes."
    ],
    "documentationUrl": "https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-open-roads/os-open-roads-overview",
    "downloadsUrl": "https://api.os.uk/downloads/v1/products/OpenRoads/downloads",
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
    "id": "OpenRoads",
    "name": "OS Open Roads",
    "supportingInfo": [
      {
        "link": "https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-open-roads/os-open-roads-technical-specification",
        "name": "Technical Specification"
      }
    ],
    "url": "https://api.os.uk/downloads/v1/products/OpenRoads",
    "version": "2026-04"
  }
}
---

# OS Open Roads

Get a high-level view of the road network, from motorways to country lanes.

Native identifier: `OpenRoads`.

Source family: `os-open-products`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/downloads/v1/products/OpenRoads)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://api.os.uk/downloads/v1/products/OpenRoads)
[Release catalogue or change-discovery route](https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-open-roads/os-open-roads-overview)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
