---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-vector-tile-api%2Ftechnical-specification%2Fservice-metadata.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Service metadata",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/service-metadata.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/service-metadata.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/service-metadata.md",
      "retrievedAt": "2026-10-02T07:27:29.303618Z",
      "responseSha256": "3cb41bdc96918a8f0cc16797ab6156df30325dcf79197949450dd5e1b63c3572",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/78",
      "normalisedRecordSha256": "f92aac2558702dfb52c2908988faa7b11a580e277ef25fd211c14d0a2a48facf",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/service-metadata.md"
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
        "fragmentSha256": "149f0f1774887ba5acdb2ccac757d9ff6a01a5e784dc70e5e92211f1d92db4ed",
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
            "operationId": "getServiceMetadata",
            "parameters": [
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
            "path": "/vts",
            "responses": {
              "200": {
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
          "Extent": {
            "properties": {
              "spatialReference": {
                "properties": {
                  "latestWkid": {
                    "type": "integer"
                  },
                  "wkid": {
                    "type": "integer"
                  }
                },
                "type": "object"
              },
              "xmax": {
                "type": "number"
              },
              "xmin": {
                "type": "number"
              },
              "ymax": {
                "type": "number"
              },
              "ymin": {
                "type": "number"
              }
            },
            "type": "object"
          },
          "Lod": {
            "properties": {
              "level": {
                "type": "integer"
              },
              "resolution": {
                "type": "number"
              },
              "scale": {
                "type": "number"
              }
            },
            "type": "object"
          },
          "ServiceMetadata": {
            "properties": {
              "capabilities": {
                "type": "string"
              },
              "currentVersion": {
                "type": "number"
              },
              "defaultStyles": {
                "type": "string"
              },
              "exportTilesAllowed": {
                "type": "boolean"
              },
              "fullExtent": {
                "$ref": "#/components/schemas/Extent"
              },
              "initialExtent": {
                "$ref": "#/components/schemas/Extent"
              },
              "maxExportTilesCount": {
                "type": "integer"
              },
              "maxLOD": {
                "type": "integer"
              },
              "maxScale": {
                "type": "number"
              },
              "maxzoom": {
                "type": "integer"
              },
              "minLOD": {
                "type": "integer"
              },
              "minScale": {
                "type": "number"
              },
              "name": {
                "type": "string"
              },
              "resourceInfo": {
                "properties": {
                  "cacheInfo": {
                    "properties": {
                      "storageInfo": {
                        "properties": {
                          "packetSize": {
                            "type": "integer"
                          },
                          "storageFormat": {
                            "type": "string"
                          }
                        },
                        "type": "object"
                      }
                    },
                    "type": "object"
                  },
                  "styleVersion": {
                    "type": "integer"
                  },
                  "tileCompression": {
                    "type": "string"
                  }
                },
                "type": "object"
              },
              "serviceItemId": {
                "type": "string"
              },
              "tileInfo": {
                "$ref": "#/components/schemas/TileInfo"
              },
              "tiles": {
                "items": {
                  "type": "string"
                },
                "type": "array"
              },
              "type": {
                "type": "string"
              }
            },
            "type": "object"
          },
          "TileInfo": {
            "properties": {
              "cols": {
                "type": "integer"
              },
              "dpi": {
                "type": "integer"
              },
              "format": {
                "type": "string"
              },
              "lods": {
                "items": {
                  "$ref": "#/components/schemas/Lod"
                },
                "type": "array"
              },
              "origin": {
                "properties": {
                  "x": {
                    "type": "number"
                  },
                  "y": {
                    "type": "number"
                  }
                },
                "type": "object"
              },
              "rows": {
                "type": "integer"
              },
              "spatialReference": {
                "$ref": "#/components/schemas/Extent"
              }
            },
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
          "https://api.os.uk/maps/vector/v1"
        ],
        "title": "OS Vector Tiles API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.0"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/service-metadata.md",
    "kind": "documentation-contract",
    "sourceSha256": "3cb41bdc96918a8f0cc16797ab6156df30325dcf79197949450dd5e1b63c3572",
    "title": "Service metadata",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/service-metadata.md"
  }
}
---

# Service metadata

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/service-metadata.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/service-metadata.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
