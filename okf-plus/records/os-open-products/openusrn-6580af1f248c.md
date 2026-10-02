---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-open-products/OpenUSRN",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "OS Open USRN",
  "description": "An open dataset of all Unique Street Reference Numbers (USRNs) within OS MasterMap Highways Network, with an associated simplified line geometry representing the geographic extent of each USRN.",
  "nativeIdentifier": "OpenUSRN",
  "sourceFamily": "os-open-products",
  "resource": "https://api.os.uk/downloads/v1/products/OpenUSRN",
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
      "resource": "https://api.os.uk/downloads/v1/products/OpenUSRN",
      "retrievedAt": "2026-10-02T01:18:01.483951Z",
      "responseSha256": "84b27f065ae7da38028d4d0859ff7c35bc15a39ccc44bc8024c1d8c2f159637c",
      "sourcePointer": "",
      "normalisedSource": "okf-plus/source/os-open-products.json",
      "normalisedPointer": "/records/21",
      "normalisedRecordSha256": "ee48bf7814be7d8dcba4f45cbb4b49fd9ccae2e663793402df34bf1168288e11",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/downloads/v1/products/OpenUSRN"
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
      "https://api.os.uk/downloads/v1/products/OpenUSRN",
      "https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-open-usrn/os-open-usrn-overview"
    ],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": null,
    "releaseVersion": "2026-10"
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
    "category": "Identifiers",
    "dataStructures": [
      "Vector"
    ],
    "description": [
      "An open dataset of all Unique Street Reference Numbers (USRNs) within OS MasterMap Highways Network, with an associated simplified line geometry representing the geographic extent of each USRN."
    ],
    "documentationUrl": "https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-open-usrn/os-open-usrn-overview",
    "downloadsUrl": "https://api.os.uk/downloads/v1/products/OpenUSRN/downloads",
    "formats": [
      {
        "format": "GeoPackage"
      }
    ],
    "id": "OpenUSRN",
    "name": "OS Open USRN",
    "supportingInfo": [
      {
        "link": "https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-open-usrn/os-open-usrn-technical-specification",
        "name": "Technical Specification"
      }
    ],
    "url": "https://api.os.uk/downloads/v1/products/OpenUSRN",
    "version": "2026-10"
  }
}
---

# OS Open USRN

An open dataset of all Unique Street Reference Numbers (USRNs) within OS MasterMap Highways Network, with an associated simplified line geometry representing the geographic extent of each USRN.

Native identifier: `OpenUSRN`.

Source family: `os-open-products`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/downloads/v1/products/OpenUSRN)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://api.os.uk/downloads/v1/products/OpenUSRN)
[Release catalogue or change-discovery route](https://docs.os.uk/os-downloads/products/transport-network-portfolio/os-open-usrn/os-open-usrn-overview)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
