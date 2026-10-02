---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-ngd-api-tiles%2Ftechnical-specification%2Fconformance.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Conformance",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/conformance.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/conformance.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/conformance.md",
      "retrievedAt": "2026-10-02T07:26:51.276862Z",
      "responseSha256": "bcd586222eeeb10133f61acd169eb6c3f2610237dc892aa159dbc2c30a9ccb95",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/47",
      "normalisedRecordSha256": "b636041459c09cf2f42213318032f2f959dca527ec39b4355dd00f0731ff70b3",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/conformance.md"
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
        "fragmentSha256": "bd4d2157cfb956147ff65a96743173d0203075d37d54407177cc20d02bfc6a56",
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
            "operationId": "getConformance",
            "parameters": [],
            "path": "/conformance",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/getConformance_200_response"
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
          "confClasses": {
            "properties": {
              "conformsTo": {
                "items": {
                  "type": "string"
                },
                "type": "array"
              }
            },
            "required": [
              "conformsTo"
            ],
            "type": "object"
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
          "getConformance_200_response": {
            "allOf": [
              {
                "$ref": "#/components/schemas/confClasses"
              }
            ]
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
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/conformance.md",
    "kind": "documentation-contract",
    "sourceSha256": "bcd586222eeeb10133f61acd169eb6c3f2610237dc892aa159dbc2c30a9ccb95",
    "title": "Conformance",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/conformance.md"
  }
}
---

# Conformance

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/conformance.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/conformance.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
