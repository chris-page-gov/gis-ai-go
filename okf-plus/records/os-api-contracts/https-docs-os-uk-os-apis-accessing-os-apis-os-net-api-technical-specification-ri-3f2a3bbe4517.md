---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-net-api%2Ftechnical-specification%2Frinex-zip.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Rinex Zip",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex-zip.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex-zip.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex-zip.md",
      "retrievedAt": "2026-10-02T07:28:52.794247Z",
      "responseSha256": "9c91b7cd996c171d8feacb7261d25f391ae8a3e8d7df7c5feadc2d5277e34f62",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/138",
      "normalisedRecordSha256": "92449fb20a4e6ebdfd99a028758dfd090f78cd6754ab1b0cdd9a8d0231e1b154",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex-zip.md"
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
        "componentParameters": {
          "RequiredTemporalParameters": {
            "explode": true,
            "in": "query",
            "name": "RequiredTemporalParameters",
            "required": true,
            "schema": {
              "$ref": "#/components/schemas/RequiredTemporalParameters"
            }
          },
          "dataFrequency": {
            "in": "query",
            "name": "dataFrequency",
            "required": false,
            "schema": {
              "type": "string"
            }
          }
        },
        "fragmentSha256": "56fde63e9c1a264962ff15c90c06765527812d7fade565fe070842171fef8981",
        "jsonFence": 1,
        "openapi": "3.0.0",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": null,
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": "Prepare to download RINEX Data for a set of stations",
            "parameters": [
              {
                "in": "query",
                "name": "stationId",
                "required": true,
                "schema": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                }
              },
              {
                "in": "query",
                "name": "filename",
                "schema": {
                  "type": "string"
                }
              },
              {
                "$ref": "#/components/parameters/RequiredTemporalParameters"
              },
              {
                "$ref": "#/components/parameters/dataFrequency"
              }
            ],
            "path": "/prepareRinexZipDownload",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "properties": {
                        "url": {
                          "type": "string"
                        }
                      },
                      "type": "object"
                    }
                  }
                }
              },
              "404": {
                "content": {}
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {
          "RequiredTemporalParameters": {
            "properties": {
              "end": {
                "format": "date-time",
                "type": "string"
              },
              "start": {
                "format": "date-time",
                "type": "string"
              }
            },
            "required": [
              "start",
              "end"
            ],
            "type": "object"
          }
        },
        "securitySchemes": {},
        "servers": [
          "https://api.os.uk/positioning/osnet/v1"
        ],
        "title": "OS Net API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "1.6.1-SNAPSHOT"
      },
      {
        "componentParameters": {
          "RequiredTemporalParameters": {
            "explode": true,
            "in": "query",
            "name": "RequiredTemporalParameters",
            "required": true,
            "schema": {
              "$ref": "#/components/schemas/RequiredTemporalParameters"
            }
          },
          "dataFrequency": {
            "in": "query",
            "name": "dataFrequency",
            "required": false,
            "schema": {
              "type": "string"
            }
          }
        },
        "fragmentSha256": "c74187bce4558ffb40d935f728b0a4f668d83c65f8c437eb84061142beee9d68",
        "jsonFence": 2,
        "openapi": "3.0.0",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": null,
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": "startRinexZipDownload",
            "parameters": [
              {
                "in": "query",
                "name": "stationId",
                "required": true,
                "schema": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                }
              },
              {
                "in": "query",
                "name": "filename",
                "schema": {
                  "type": "string"
                }
              },
              {
                "$ref": "#/components/parameters/RequiredTemporalParameters"
              },
              {
                "$ref": "#/components/parameters/dataFrequency"
              }
            ],
            "path": "/startRinexZipDownload",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "properties": {
                        "token": {
                          "type": "string"
                        }
                      },
                      "type": "object"
                    }
                  }
                }
              },
              "404": {
                "content": {}
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {
          "RequiredTemporalParameters": {
            "properties": {
              "end": {
                "format": "date-time",
                "type": "string"
              },
              "start": {
                "format": "date-time",
                "type": "string"
              }
            },
            "required": [
              "start",
              "end"
            ],
            "type": "object"
          }
        },
        "securitySchemes": {},
        "servers": [
          "https://api.os.uk/positioning/osnet/v1"
        ],
        "title": "OS Net API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "1.6.1-SNAPSHOT"
      },
      {
        "componentParameters": {},
        "fragmentSha256": "e9c57e3d33dd6aad4ae7aa3753e0c867c3f6cb69398ff5fd97a5b1b3accca97e",
        "jsonFence": 3,
        "openapi": "3.0.0",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": null,
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": "collectRinexZipDownload",
            "parameters": [
              {
                "in": "query",
                "name": "token",
                "required": true,
                "schema": {
                  "type": "string"
                }
              }
            ],
            "path": "/collectRinexZipDownload",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "properties": {
                        "percentageComplete": {
                          "format": "int32",
                          "maximum": 100,
                          "minimum": 0,
                          "type": "number"
                        },
                        "url": {
                          "type": "string"
                        }
                      },
                      "type": "object"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {},
        "securitySchemes": {},
        "servers": [
          "https://api.os.uk/positioning/osnet/v1"
        ],
        "title": "OS Net API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "1.6.1-SNAPSHOT"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex-zip.md",
    "kind": "documentation-contract",
    "sourceSha256": "9c91b7cd996c171d8feacb7261d25f391ae8a3e8d7df7c5feadc2d5277e34f62",
    "title": "Rinex Zip",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex-zip.md"
  }
}
---

# Rinex Zip

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex-zip.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex-zip.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
