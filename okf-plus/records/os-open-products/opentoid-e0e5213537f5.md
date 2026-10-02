---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-open-products/OpenTOID",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "OS Open TOID",
  "description": "An open dataset providing access to a generalised location to key features found in OS MasterMap premium products enabling visualisation of third party data linked to their respective TOID identifier.",
  "nativeIdentifier": "OpenTOID",
  "sourceFamily": "os-open-products",
  "resource": "https://api.os.uk/downloads/v1/products/OpenTOID",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "buildingsAndInfrastructure",
    "landAndTerrain",
    "water",
    "Vector"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/downloads/v1/products/OpenTOID",
      "retrievedAt": "2026-10-02T01:18:00.962133Z",
      "responseSha256": "3871b2f55ce9a45996bf98812b460276bc3dd47db1b927cd526c19d456c90495",
      "sourcePointer": "",
      "normalisedSource": "okf-plus/source/os-open-products.json",
      "normalisedPointer": "/records/19",
      "normalisedRecordSha256": "b62a98023150b0036c662d66d1539a958d0341fb3d6ba687fb1e5e2f5bd8882d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/downloads/v1/products/OpenTOID"
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
      "https://api.os.uk/downloads/v1/products/OpenTOID",
      "https://docs.os.uk/os-downloads/products/buildings-and-infrastructure-portfolio/os-open-toid/os-open-toid-overview"
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
      "HP",
      "HT",
      "HU",
      "HW",
      "HX",
      "HY",
      "HZ",
      "NA",
      "NB",
      "NC",
      "ND",
      "NF",
      "NG",
      "NH",
      "NJ",
      "NK",
      "NL",
      "NM",
      "NN",
      "NO",
      "NR",
      "NS",
      "NT",
      "NU",
      "NW",
      "NX",
      "NY",
      "NZ",
      "SD",
      "SE",
      "SH",
      "SJ",
      "SK",
      "SM",
      "SN",
      "SO",
      "SP",
      "SR",
      "SS",
      "ST",
      "SU",
      "SV",
      "SW",
      "SX",
      "SY",
      "SZ",
      "TA",
      "TF",
      "TG",
      "TL",
      "TM",
      "TQ",
      "TR",
      "TV"
    ],
    "categories": [
      "buildingsAndInfrastructure",
      "landAndTerrain",
      "water"
    ],
    "category": "Identifiers",
    "dataStructures": [
      "Vector"
    ],
    "description": [
      "An open dataset providing access to a generalised location to key features found in OS MasterMap premium products enabling visualisation of third party data linked to their respective TOID identifier."
    ],
    "documentationUrl": "https://docs.os.uk/os-downloads/products/buildings-and-infrastructure-portfolio/os-open-toid/os-open-toid-overview",
    "downloadsUrl": "https://api.os.uk/downloads/v1/products/OpenTOID/downloads",
    "formats": [
      {
        "format": "CSV"
      },
      {
        "format": "GeoPackage"
      }
    ],
    "id": "OpenTOID",
    "name": "OS Open TOID",
    "supportingInfo": [
      {
        "link": "https://docs.os.uk/os-downloads/products/buildings-and-infrastructure-portfolio/os-open-toid/os-open-toid-technical-specification",
        "name": "Technical Specification"
      }
    ],
    "url": "https://api.os.uk/downloads/v1/products/OpenTOID",
    "version": "2026-08"
  }
}
---

# OS Open TOID

An open dataset providing access to a generalised location to key features found in OS MasterMap premium products enabling visualisation of third party data linked to their respective TOID identifier.

Native identifier: `OpenTOID`.

Source family: `os-open-products`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/downloads/v1/products/OpenTOID)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://api.os.uk/downloads/v1/products/OpenTOID)
[Release catalogue or change-discovery route](https://docs.os.uk/os-downloads/products/buildings-and-infrastructure-portfolio/os-open-toid/os-open-toid-overview)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
