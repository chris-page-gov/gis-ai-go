---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-open-products/BuiltUpAreas",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "OS Open Built Up Areas",
  "description": "OS Open Built Up Areas represents the built-up areas of Great Britain equal to or greater than 200,000m² or 20 hectares and they include unique names, alternative language names and GSS codes.",
  "nativeIdentifier": "BuiltUpAreas",
  "sourceFamily": "os-open-products",
  "resource": "https://api.os.uk/downloads/v1/products/BuiltUpAreas",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "areasAndZones",
    "Vector"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/downloads/v1/products/BuiltUpAreas",
      "retrievedAt": "2026-10-02T01:17:59.295994Z",
      "responseSha256": "8f4a0fca65ede8316a7e957ad27ebb58de1d1ea7ffa69c36b32b3d096bea2c8e",
      "sourcePointer": "",
      "normalisedSource": "okf-plus/source/os-open-products.json",
      "normalisedPointer": "/records/13",
      "normalisedRecordSha256": "8c2150ec311a86dd94e73e0466f293bd76df259e73341ae838798e3273443e58",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/downloads/v1/products/BuiltUpAreas"
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
      "https://api.os.uk/downloads/v1/products/BuiltUpAreas",
      "https://docs.os.uk/os-downloads/products/areas-and-zones-portfolio/os-open-built-up-areas"
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
      "areasAndZones"
    ],
    "category": "Lookups",
    "dataStructures": [
      "Vector"
    ],
    "description": [
      "OS Open Built Up Areas represents the built-up areas of Great Britain equal to or greater than 200,000m² or 20 hectares and they include unique names, alternative language names and GSS codes."
    ],
    "documentationUrl": "https://docs.os.uk/os-downloads/products/areas-and-zones-portfolio/os-open-built-up-areas",
    "downloadsUrl": "https://api.os.uk/downloads/v1/products/BuiltUpAreas/downloads",
    "formats": [
      {
        "format": "CSV"
      },
      {
        "format": "GeoPackage"
      }
    ],
    "id": "BuiltUpAreas",
    "name": "OS Open Built Up Areas",
    "supportingInfo": [
      {
        "link": "https://docs.os.uk/os-downloads/products/areas-and-zones-portfolio/os-open-built-up-areas/os-open-built-up-areas-technical-specification",
        "name": "Technical Specification"
      }
    ],
    "url": "https://api.os.uk/downloads/v1/products/BuiltUpAreas",
    "version": "2026-04"
  }
}
---

# OS Open Built Up Areas

OS Open Built Up Areas represents the built-up areas of Great Britain equal to or greater than 200,000m² or 20 hectares and they include unique names, alternative language names and GSS codes.

Native identifier: `BuiltUpAreas`.

Source family: `os-open-products`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/downloads/v1/products/BuiltUpAreas)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://api.os.uk/downloads/v1/products/BuiltUpAreas)
[Release catalogue or change-discovery route](https://docs.os.uk/os-downloads/products/areas-and-zones-portfolio/os-open-built-up-areas)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
