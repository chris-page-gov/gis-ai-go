---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-net-api%2Ftechnical-specification%2Frinex.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Rinex",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex.md",
      "retrievedAt": "2026-10-02T07:28:51.652481Z",
      "responseSha256": "8c114c362c859b4d042afcc97d5f3464cb921e4bfbe9e28b94e48984fb644545",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/137",
      "normalisedRecordSha256": "dd684041bbaade3be122dd84cee101a36785b87e72cf6e427f06ae9dfd5b8ca0",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex.md"
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
          },
          "stationId": {
            "in": "path",
            "name": "stationId",
            "required": true,
            "schema": {
              "maxLength": 4,
              "minLength": 4,
              "pattern": "^[a-zA-Z0-9]*$",
              "type": "string"
            }
          }
        },
        "fragmentSha256": "316dba295674958d6c56ed582817e779d8fadd4b9ed997393396b96ce76bf288",
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
            "operationId": "Get station data",
            "parameters": [
              {
                "$ref": "#/components/parameters/stationId"
              },
              {
                "$ref": "#/components/parameters/RequiredTemporalParameters"
              },
              {
                "$ref": "#/components/parameters/dataFrequency"
              }
            ],
            "path": "/stations/{stationId}/rinex",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "items": {
                        "$ref": "#/components/schemas/RinexFile"
                      },
                      "type": "array"
                    }
                  }
                }
              },
              "400": {
                "content": {
                  "application/problem+json": {
                    "schema": {
                      "type": "object"
                    }
                  }
                }
              },
              "403": {
                "content": {
                  "application/problem+json": {
                    "schema": {
                      "type": "object"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {
          "OSNetDownload": {
            "properties": {
              "fileName": {
                "type": "string"
              },
              "format": {
                "type": "string"
              },
              "md5": {
                "type": "string"
              },
              "size": {
                "format": "int64",
                "type": "integer"
              },
              "subformat": {
                "type": "string"
              },
              "url": {
                "format": "uri",
                "type": "string"
              }
            },
            "required": [
              "url",
              "fileName"
            ],
            "type": "object"
          },
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
          },
          "RinexFile": {
            "allOf": [
              {
                "$ref": "#/components/schemas/OSNetDownload"
              },
              {
                "properties": {
                  "dataFrequency": {
                    "type": "string"
                  },
                  "duration": {
                    "type": "string"
                  },
                  "percentageComplete": {
                    "maximum": 100,
                    "minimum": 0,
                    "type": "integer"
                  },
                  "start": {
                    "format": "date-time",
                    "type": "string"
                  },
                  "station": {
                    "maxLength": 4,
                    "minLength": 4,
                    "type": "string"
                  }
                },
                "type": "object"
              }
            ]
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
        "fragmentSha256": "c2aa041733c2b3ab6ce1529ec4fbb2a621c378796184ff1ccccedca4314363cb",
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
            "operationId": "Get Rinex Data Years",
            "parameters": [],
            "path": "/rinex",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/MetaData"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {
          "Link": {
            "properties": {
              "description": {
                "type": "string"
              },
              "href": {
                "format": "uri",
                "type": "string"
              },
              "rel": {
                "type": "string"
              },
              "title": {
                "type": "string"
              },
              "type": {
                "type": "string"
              }
            },
            "required": [
              "href",
              "rel",
              "type",
              "title",
              "description"
            ],
            "type": "object"
          },
          "MetaData": {
            "properties": {
              "description": {
                "type": "string"
              },
              "links": {
                "items": {
                  "$ref": "#/components/schemas/Link"
                },
                "type": "array"
              },
              "title": {
                "type": "string"
              }
            },
            "required": [
              "title",
              "description",
              "links"
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
          "year": {
            "in": "path",
            "name": "year",
            "required": true,
            "schema": {
              "format": "int32",
              "minimum": 2024,
              "type": "integer"
            }
          }
        },
        "fragmentSha256": "ca5f760239d7067dd79b5671130d9e275be46b7d404faa22fd9536c927c4d6d2",
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
            "operationId": "Get Rinex Data Days",
            "parameters": [
              {
                "$ref": "#/components/parameters/year"
              }
            ],
            "path": "/rinex/{year}",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/MetaData"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {
          "Link": {
            "properties": {
              "description": {
                "type": "string"
              },
              "href": {
                "format": "uri",
                "type": "string"
              },
              "rel": {
                "type": "string"
              },
              "title": {
                "type": "string"
              },
              "type": {
                "type": "string"
              }
            },
            "required": [
              "href",
              "rel",
              "type",
              "title",
              "description"
            ],
            "type": "object"
          },
          "MetaData": {
            "properties": {
              "description": {
                "type": "string"
              },
              "links": {
                "items": {
                  "$ref": "#/components/schemas/Link"
                },
                "type": "array"
              },
              "title": {
                "type": "string"
              }
            },
            "required": [
              "title",
              "description",
              "links"
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
          "dataFrequency": {
            "in": "query",
            "name": "dataFrequency",
            "required": false,
            "schema": {
              "type": "string"
            }
          },
          "dayOfYear": {
            "in": "path",
            "name": "dayOfYear",
            "required": true,
            "schema": {
              "maximum": 366,
              "minimum": 1,
              "type": "integer"
            }
          },
          "year": {
            "in": "path",
            "name": "year",
            "required": true,
            "schema": {
              "format": "int32",
              "minimum": 2024,
              "type": "integer"
            }
          }
        },
        "fragmentSha256": "889e7e5f26305b244d4715cea38639f75b33609e262e549ae6a3e1057c866596",
        "jsonFence": 4,
        "openapi": "3.0.0",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": null,
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": "Get Rinex Data Files",
            "parameters": [
              {
                "$ref": "#/components/parameters/year"
              },
              {
                "$ref": "#/components/parameters/dayOfYear"
              },
              {
                "$ref": "#/components/parameters/dataFrequency"
              }
            ],
            "path": "/rinex/{year}/{dayOfYear}",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "items": {
                        "$ref": "#/components/schemas/RinexFile"
                      },
                      "type": "array"
                    }
                  }
                }
              },
              "400": {
                "content": {
                  "application/problem+json": {
                    "schema": {
                      "type": "object"
                    }
                  }
                }
              },
              "403": {
                "content": {
                  "application/problem+json": {
                    "schema": {
                      "type": "object"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {
          "OSNetDownload": {
            "properties": {
              "fileName": {
                "type": "string"
              },
              "format": {
                "type": "string"
              },
              "md5": {
                "type": "string"
              },
              "size": {
                "format": "int64",
                "type": "integer"
              },
              "subformat": {
                "type": "string"
              },
              "url": {
                "format": "uri",
                "type": "string"
              }
            },
            "required": [
              "url",
              "fileName"
            ],
            "type": "object"
          },
          "RinexFile": {
            "allOf": [
              {
                "$ref": "#/components/schemas/OSNetDownload"
              },
              {
                "properties": {
                  "dataFrequency": {
                    "type": "string"
                  },
                  "duration": {
                    "type": "string"
                  },
                  "percentageComplete": {
                    "maximum": 100,
                    "minimum": 0,
                    "type": "integer"
                  },
                  "start": {
                    "format": "date-time",
                    "type": "string"
                  },
                  "station": {
                    "maxLength": 4,
                    "minLength": 4,
                    "type": "string"
                  }
                },
                "type": "object"
              }
            ]
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
          "dayOfYear": {
            "in": "path",
            "name": "dayOfYear",
            "required": true,
            "schema": {
              "maximum": 366,
              "minimum": 1,
              "type": "integer"
            }
          },
          "filename": {
            "in": "path",
            "name": "filename",
            "required": true,
            "schema": {
              "type": "string"
            }
          },
          "year": {
            "in": "path",
            "name": "year",
            "required": true,
            "schema": {
              "format": "int32",
              "minimum": 2024,
              "type": "integer"
            }
          }
        },
        "fragmentSha256": "72e6e4e4af90162632c40809854057c740935050d185345063ce9d4e57c56658",
        "jsonFence": 5,
        "openapi": "3.0.0",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": null,
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": "GetRinexFile",
            "parameters": [
              {
                "$ref": "#/components/parameters/year"
              },
              {
                "$ref": "#/components/parameters/dayOfYear"
              },
              {
                "$ref": "#/components/parameters/filename"
              }
            ],
            "path": "/rinex/{year}/{dayOfYear}/{filename}",
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
              },
              "204": {
                "content": {
                  "application/problem+json": {
                    "schema": {
                      "type": "object"
                    }
                  }
                }
              },
              "307": {
                "content": {}
              },
              "400": {
                "content": {
                  "application/problem+json": {
                    "schema": {
                      "type": "object"
                    }
                  }
                }
              },
              "403": {
                "content": {
                  "application/problem+json": {
                    "schema": {
                      "type": "object"
                    }
                  }
                }
              },
              "404": {
                "content": {
                  "application/problem+json": {
                    "schema": {
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
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex.md",
    "kind": "documentation-contract",
    "sourceSha256": "8c114c362c859b4d042afcc97d5f3464cb921e4bfbe9e28b94e48984fb644545",
    "title": "Rinex",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex.md"
  }
}
---

# Rinex

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/rinex.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
