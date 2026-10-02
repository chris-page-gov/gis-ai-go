---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-vector-tile-api%2Ftechnical-specification%2Ftile-request.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Tile request",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/tile-request.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/tile-request.md",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "specification",
    "documentation"
  ],
  "sources": [
    {
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/tile-request.md",
      "retrievedAt": "2026-10-02T07:27:31.400062Z",
      "responseSha256": "7ab6bc480fe06d3c71f53b930c129fcd4e032ce3798385a4f897bcd27a68b3c4",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/80",
      "normalisedRecordSha256": "3e475d3bba3b7c8123dec10bd2842b90c91cffa09b42d17c8cec076ff50f2615",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/tile-request.md"
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
    "releaseCatalogue": [],
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
  "limitations": [],
  "details": {
    "callable": false,
    "contentCaptured": true,
    "contracts": [
      {
        "componentParameters": {},
        "fragmentSha256": "91cfedabb8f68935acb90c95abf3681ea3a918d7330fb7a4827e6516917736ec",
        "jsonFence": 1,
        "openapi": "3.0.1",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": [
              {
                "api-key": [],
                "api-key-header": [],
                "oauth2": []
              }
            ],
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": "getTileData",
            "parameters": [
              {
                "in": "path",
                "name": "z",
                "required": true,
                "schema": {
                  "format": "int32",
                  "type": "integer"
                }
              },
              {
                "in": "path",
                "name": "y",
                "required": true,
                "schema": {
                  "format": "int32",
                  "type": "integer"
                }
              },
              {
                "in": "path",
                "name": "x",
                "required": true,
                "schema": {
                  "format": "int32",
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "srs",
                "required": false,
                "schema": {
                  "enum": [
                    "27700",
                    "3857"
                  ],
                  "type": "string"
                }
              }
            ],
            "path": "/vts/tile/{z}/{y}/{x}.pbf",
            "responses": {
              "200": {
                "content": {
                  "application/octet-stream": {
                    "schema": {
                      "format": "binary",
                      "type": "string"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "root"
          }
        ],
        "schemas": {},
        "securitySchemes": {
          "api-key": {
            "in": "query",
            "name": "key",
            "type": "apiKey"
          }
        },
        "servers": [
          "https://api.os.uk/maps/vector/v1"
        ],
        "title": "OS Vector Tiles API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.0"
      },
      {
        "componentParameters": {},
        "fragmentSha256": "7793c5ac7d2a3a32b4b29a1218a5434b27effa060dfac8f32fec3738812766f5",
        "jsonFence": 2,
        "openapi": "3.0.1",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": [
              {
                "api-key": [],
                "api-key-header": [],
                "oauth2": []
              }
            ],
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": "getOverlayTileData",
            "parameters": [
              {
                "in": "path",
                "name": "layer-name",
                "required": true,
                "schema": {
                  "enum": [
                    "boundaries",
                    "greenspace",
                    "sites",
                    "water",
                    "highways",
                    "paths"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "path",
                "name": "z",
                "required": true,
                "schema": {
                  "format": "int32",
                  "type": "integer"
                }
              },
              {
                "in": "path",
                "name": "y",
                "required": true,
                "schema": {
                  "format": "int32",
                  "type": "integer"
                }
              },
              {
                "in": "path",
                "name": "x",
                "required": true,
                "schema": {
                  "format": "int32",
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "srs",
                "schema": {
                  "enum": [
                    "27700",
                    "3857"
                  ],
                  "type": "string"
                }
              }
            ],
            "path": "/vts/{layer-name}/tile/{z}/{y}/{x}.pbf",
            "responses": {
              "200": {
                "content": {
                  "application/octet-stream": {
                    "schema": {
                      "format": "binary",
                      "type": "string"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "root"
          }
        ],
        "schemas": {},
        "securitySchemes": {
          "api-key": {
            "in": "query",
            "name": "key",
            "type": "apiKey"
          }
        },
        "servers": [
          "https://api.os.uk/maps/vector/v1"
        ],
        "title": "OS Vector Tiles API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.0"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/tile-request.md",
    "kind": "documentation-contract",
    "sourceSha256": "7ab6bc480fe06d3c71f53b930c129fcd4e032ce3798385a4f897bcd27a68b3c4",
    "title": "Tile request",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/tile-request.md"
  }
}
---

# Tile request

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/tile-request.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/tile-request.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
