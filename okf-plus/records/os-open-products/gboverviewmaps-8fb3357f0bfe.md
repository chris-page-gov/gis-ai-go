---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-open-products/GBOverviewMaps",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "GB Overview Maps",
  "description": "Our simplest overview maps of Great Britain.",
  "nativeIdentifier": "GBOverviewMaps",
  "sourceFamily": "os-open-products",
  "resource": "https://api.os.uk/downloads/v1/products/GBOverviewMaps",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "mapsAndImagery",
    "Raster"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/downloads/v1/products/GBOverviewMaps",
      "retrievedAt": "2026-10-02T01:17:58.768549Z",
      "responseSha256": "9f34dca861bb59c7f7fecb38bf0a16f80ba4174411d3bae18980a08137d919db",
      "sourcePointer": "",
      "normalisedSource": "okf-plus/source/os-open-products.json",
      "normalisedPointer": "/records/11",
      "normalisedRecordSha256": "dc2d4f32beaac5de54a9c5e17a097f27a61864ab188568b0fee7aa77ea61c397",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/downloads/v1/products/GBOverviewMaps"
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
      "https://api.os.uk/downloads/v1/products/GBOverviewMaps"
    ],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": null,
    "releaseVersion": "2026-01"
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
      "Raster"
    ],
    "description": [
      "Our simplest overview maps of Great Britain."
    ],
    "downloadsUrl": "https://api.os.uk/downloads/v1/products/GBOverviewMaps/downloads",
    "formats": [
      {
        "format": "GeoTIFF",
        "subformat": "Full Colour"
      }
    ],
    "id": "GBOverviewMaps",
    "name": "GB Overview Maps",
    "supportingInfo": [
      {
        "link": "https://docs.os.uk/os-downloads/products/maps-and-imagery-portfolio/gb-overview-maps/gb-overview-maps-technical-specification",
        "name": "Technical Specification"
      }
    ],
    "url": "https://api.os.uk/downloads/v1/products/GBOverviewMaps",
    "version": "2026-01"
  }
}
---

# GB Overview Maps

Our simplest overview maps of Great Britain.

Native identifier: `GBOverviewMaps`.

Source family: `os-open-products`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/downloads/v1/products/GBOverviewMaps)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://api.os.uk/downloads/v1/products/GBOverviewMaps)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
