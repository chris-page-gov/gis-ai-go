---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-vector-tile-api%2Ftechnical-specification%2Fstylesheet.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Stylesheet",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/stylesheet.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/stylesheet.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/stylesheet.md",
      "retrievedAt": "2026-10-02T07:27:30.358575Z",
      "responseSha256": "ecb701ce2860f49507a83d3a48ccb151d0c2b2225e7c6f1b5b2b0be69305cb9a",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/79",
      "normalisedRecordSha256": "f011d6aac9e9ef0219455878d695c74e57dc1fdf5d16b4edd762d404c4c010dd",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/stylesheet.md"
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
        "fragmentSha256": "2467e7a7bf6da31ef267ca4a18f91d7954d0e3efb0fc5e9f22657436095e5941",
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
            "operationId": "discoverStyles",
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
            "path": "/vts/resources/styles",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/StylesResponse"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "root"
          }
        ],
        "schemas": {
          "StylesResponse": {
            "properties": {
              "glyphs": {
                "type": "string"
              },
              "layers": {
                "items": {
                  "properties": {
                    "filter": {
                      "items": {
                        "type": "string"
                      },
                      "type": "array"
                    },
                    "id": {
                      "type": "string"
                    },
                    "layout": {
                      "type": "object"
                    },
                    "maxzoom": {
                      "type": "integer"
                    },
                    "minzoom": {
                      "type": "integer"
                    },
                    "paint": {
                      "type": "object"
                    },
                    "source": {
                      "type": "string"
                    },
                    "source-layer": {
                      "type": "string"
                    },
                    "type": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "id",
                    "type",
                    "source"
                  ],
                  "type": "object"
                },
                "type": "array"
              },
              "sources": {
                "additionalProperties": {
                  "properties": {
                    "type": {
                      "type": "string"
                    },
                    "url": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "type",
                    "url"
                  ],
                  "type": "object"
                },
                "type": "object"
              },
              "sprite": {
                "type": "string"
              },
              "version": {
                "type": "integer"
              }
            },
            "required": [
              "version",
              "sprite",
              "glyphs",
              "sources",
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
          "https://api.os.uk/maps/vector/v1"
        ],
        "title": "OS Vector Tiles API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.0"
      },
      {
        "componentParameters": {},
        "fragmentSha256": "59e52582e80084136894eb6781c6177003e279299cc132b3fc3bcdd060868ffb",
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
            "operationId": "discoverOverlayStyles",
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
            "path": "/vts/{layer-name}/resources/styles",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/StylesResponse"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "root"
          }
        ],
        "schemas": {
          "StylesResponse": {
            "properties": {
              "glyphs": {
                "type": "string"
              },
              "layers": {
                "items": {
                  "properties": {
                    "filter": {
                      "items": {
                        "type": "string"
                      },
                      "type": "array"
                    },
                    "id": {
                      "type": "string"
                    },
                    "layout": {
                      "type": "object"
                    },
                    "maxzoom": {
                      "type": "integer"
                    },
                    "minzoom": {
                      "type": "integer"
                    },
                    "paint": {
                      "type": "object"
                    },
                    "source": {
                      "type": "string"
                    },
                    "source-layer": {
                      "type": "string"
                    },
                    "type": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "id",
                    "type",
                    "source"
                  ],
                  "type": "object"
                },
                "type": "array"
              },
              "sources": {
                "additionalProperties": {
                  "properties": {
                    "type": {
                      "type": "string"
                    },
                    "url": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "type",
                    "url"
                  ],
                  "type": "object"
                },
                "type": "object"
              },
              "sprite": {
                "type": "string"
              },
              "version": {
                "type": "integer"
              }
            },
            "required": [
              "version",
              "sprite",
              "glyphs",
              "sources",
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
          "https://api.os.uk/maps/vector/v1"
        ],
        "title": "OS Vector Tiles API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.0"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/stylesheet.md",
    "kind": "documentation-contract",
    "sourceSha256": "ecb701ce2860f49507a83d3a48ccb151d0c2b2225e7c6f1b5b2b0be69305cb9a",
    "title": "Stylesheet",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/stylesheet.md"
  }
}
---

# Stylesheet

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/stylesheet.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-vector-tile-api/technical-specification/stylesheet.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
