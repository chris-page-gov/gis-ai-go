---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-maps-api%2Ftechnical-specification%2Fwmts.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "WMTS",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/wmts.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/wmts.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/wmts.md",
      "retrievedAt": "2026-10-02T07:27:46.051025Z",
      "responseSha256": "5513520347c2484db6bb0763b39a87d842852dad9a2ae4162e98684baa44e964",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/92",
      "normalisedRecordSha256": "fcf90d6274288014e171691882d92f3a26aaa8162f4c447757ee4817cadd1a1e",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/wmts.md"
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
        "fragmentSha256": "678eb8ffeb2742076d6aa43d9c3af51d4adc3dda3a6e959d099aaa32374fe7e2",
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
            "operationId": "getWMTSTileData",
            "parameters": [
              {
                "in": "query",
                "name": "layer",
                "required": true,
                "schema": {
                  "enum": [
                    "Road_27700",
                    "Road_3857",
                    "Outdoor_27700",
                    "Outdoor_3857",
                    "Light_27700",
                    "Light_3857",
                    "Leisure_27700"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "tileMatrixSet",
                "required": true,
                "schema": {
                  "enum": [
                    "EPSG:27700",
                    "EPSG:3857"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "tileMatrix",
                "required": true,
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "tileRow",
                "required": true,
                "schema": {
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "tileCol",
                "required": true,
                "schema": {
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "service",
                "required": true,
                "schema": {
                  "enum": [
                    "wmts"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "request",
                "required": true,
                "schema": {
                  "enum": [
                    "GetCapabilities",
                    "GetTile"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "style",
                "required": true,
                "schema": {
                  "enum": [
                    "default"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "version",
                "required": false,
                "schema": {
                  "enum": [
                    "1.0.0",
                    "2.0.0"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "height",
                "required": false,
                "schema": {
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "width",
                "required": false,
                "schema": {
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "outputformat",
                "required": false,
                "schema": {
                  "enum": [
                    "image/png"
                  ],
                  "type": "string"
                }
              }
            ],
            "path": "/wmts",
            "responses": {
              "200": {
                "content": {
                  "image/png": {
                    "schema": {}
                  }
                }
              },
              "ServiceMetadata": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/ServiceMetadata"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "root"
          }
        ],
        "schemas": {
          "ServiceMetadata": {
            "properties": {
              "layers": {
                "items": {
                  "type": "string"
                },
                "type": "array"
              },
              "operations": {
                "items": {
                  "type": "string"
                },
                "type": "array"
              },
              "service": {
                "properties": {
                  "description": {
                    "type": "string"
                  },
                  "title": {
                    "type": "string"
                  },
                  "version": {
                    "type": "string"
                  }
                },
                "required": [
                  "title",
                  "description",
                  "version"
                ],
                "type": "object"
              },
              "tileMatrixSets": {
                "items": {
                  "type": "string"
                },
                "type": "array"
              }
            },
            "required": [
              "service",
              "operations",
              "tileMatrixSets",
              "layers"
            ],
            "type": "object"
          }
        },
        "securitySchemes": {
          "api-key": {
            "in": "query",
            "name": "key",
            "type": "apiKey"
          }
        },
        "servers": [
          "https://api.os.uk/maps/raster/v1"
        ],
        "title": "OS Maps API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.0"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/wmts.md",
    "kind": "documentation-contract",
    "sourceSha256": "5513520347c2484db6bb0763b39a87d842852dad9a2ae4162e98684baa44e964",
    "title": "WMTS",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/wmts.md"
  }
}
---

# WMTS

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/wmts.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/wmts.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
