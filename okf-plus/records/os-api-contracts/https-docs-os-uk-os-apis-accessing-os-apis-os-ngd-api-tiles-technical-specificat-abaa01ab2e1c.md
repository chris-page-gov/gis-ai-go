---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-ngd-api-tiles%2Ftechnical-specification%2Fstyles.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Styles",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/styles.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/styles.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/styles.md",
      "retrievedAt": "2026-10-02T07:26:57.597992Z",
      "responseSha256": "118ac6a7152155f9896dff04f8e5935081c3851aff237c57f5398d3b3b866fc0",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/52",
      "normalisedRecordSha256": "9d6f5dd2f1c8390c134361f4069e66620a84310c496f73b3e1c4c9f34638b609",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/styles.md"
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
        "fragmentSha256": "a06e52674176be4384db9f15659d708828aff3026ac48c5ea3e26f06c527edb7",
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
            "operationId": "getStyleRoot",
            "parameters": [
              {
                "in": "path",
                "name": "collectionId",
                "required": true,
                "schema": {
                  "$ref": "#/components/schemas/AllCollections"
                }
              },
              {
                "in": "path",
                "name": "styleId",
                "required": true,
                "schema": {
                  "$ref": "#/components/schemas/Styles"
                }
              }
            ],
            "path": "/collections/{collectionId}/styles/{styleId}",
            "responses": {
              "200": {
                "content": {
                  "*/*": {
                    "schema": {
                      "type": "object"
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
          "AllCollections": {
            "enum": [
              "ngd-base",
              "asu-bdy",
              "wtr-ctch",
              "trn-ntwk-railway",
              "wtr-tidalboundary"
            ],
            "type": "string"
          },
          "Styles": {
            "enum": [
              "3857",
              "27700",
              "road-27700",
              "road-3857",
              "light-27700",
              "light-3857",
              "blackwhite-27700",
              "blackwhite-3857"
            ],
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
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/styles.md",
    "kind": "documentation-contract",
    "sourceSha256": "118ac6a7152155f9896dff04f8e5935081c3851aff237c57f5398d3b3b866fc0",
    "title": "Styles",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/styles.md"
  }
}
---

# Styles

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/styles.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/styles.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
