---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-ngd-api-tiles%2Ftechnical-specification%2Ftile-matrix-sets.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Tile matrix sets",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/tile-matrix-sets.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/tile-matrix-sets.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/tile-matrix-sets.md",
      "retrievedAt": "2026-10-02T07:26:55.104732Z",
      "responseSha256": "846c2040470b758cc0059f761656c619ba6be051ed36bc344a905155a13e75da",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/50",
      "normalisedRecordSha256": "be7986fe89930a5208dde2ffd0e04078fe8a784a37496ff45ff756751f6a5612",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/tile-matrix-sets.md"
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
        "fragmentSha256": "fe560e24c43ea6ff31ad95c7b205c826308ca3ebd271f10deeb0f55e698e22c5",
        "jsonFence": 1,
        "openapi": "3.0.1",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": null,
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": "getTileMatrixSetsList",
            "parameters": [],
            "path": "/tilematrixsets",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/getTileMatrixSetsList_200_response"
                    }
                  }
                }
              },
              "400": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/exceptionDto"
                    }
                  }
                }
              },
              "404": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/exceptionDto"
                    }
                  }
                }
              },
              "405": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/exceptionDto"
                    }
                  }
                }
              },
              "406": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/exceptionDto"
                    }
                  }
                }
              },
              "500": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/exceptionDto"
                    }
                  }
                }
              },
              "504": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/exceptionDto"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {
          "crs": {
            "format": "uri",
            "type": "string"
          },
          "exceptionDto": {
            "properties": {
              "code": {
                "type": "integer"
              },
              "description": {
                "type": "string"
              },
              "detail": {
                "type": "string"
              },
              "help": {
                "type": "string"
              },
              "instance": {
                "type": "string"
              },
              "status": {
                "type": "integer"
              },
              "title": {
                "type": "string"
              },
              "type": {
                "type": "string"
              }
            },
            "required": [
              "type"
            ],
            "type": "object"
          },
          "getTileMatrixSetsList_200_response": {
            "properties": {
              "tileMatrixSets": {
                "items": {
                  "$ref": "#/components/schemas/tileMatrixSet-item"
                },
                "type": "array"
              }
            },
            "type": "object"
          },
          "link": {
            "properties": {
              "href": {
                "type": "string"
              },
              "hreflang": {
                "type": "string"
              },
              "length": {
                "type": "integer"
              },
              "rel": {
                "type": "string"
              },
              "templated": {
                "type": "boolean"
              },
              "title": {
                "type": "string"
              },
              "type": {
                "type": "string"
              },
              "varBase": {
                "type": "string"
              }
            },
            "required": [
              "href",
              "rel"
            ],
            "type": "object"
          },
          "tileMatrixSet-item": {
            "properties": {
              "crs": {
                "allOf": [
                  {
                    "type": "object"
                  },
                  {
                    "$ref": "#/components/schemas/crs"
                  }
                ]
              },
              "id": {
                "type": "string"
              },
              "links": {
                "items": {
                  "$ref": "#/components/schemas/link"
                },
                "type": "array"
              },
              "title": {
                "type": "string"
              },
              "uri": {
                "format": "uri",
                "type": "string"
              }
            },
            "required": [
              "links"
            ],
            "type": "object"
          }
        },
        "securitySchemes": {},
        "servers": [
          "https://api.os.uk/maps/vector/ngd/ota/v1"
        ],
        "title": "OS NGD API - Tiles",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.8"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/tile-matrix-sets.md",
    "kind": "documentation-contract",
    "sourceSha256": "846c2040470b758cc0059f761656c619ba6be051ed36bc344a905155a13e75da",
    "title": "Tile matrix sets",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/tile-matrix-sets.md"
  }
}
---

# Tile matrix sets

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/tile-matrix-sets.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/tile-matrix-sets.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
