---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-net-api%2Ftechnical-specification%2Fstations.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Stations",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/stations.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/stations.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/stations.md",
      "retrievedAt": "2026-10-02T07:28:50.599960Z",
      "responseSha256": "f14c4f5052661d4e0cedb603efb7bbba70c5eceb67081855aeea3048dd308a90",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/136",
      "normalisedRecordSha256": "907bb8f6d3779c6eae0ce0cc6e048b1258536bb542dc6cdf8d0d5c671732bf07",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/stations.md"
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
          "SpatialParameters": {
            "explode": true,
            "in": "query",
            "name": "SpatialParameters",
            "required": false,
            "schema": {
              "$ref": "#/components/schemas/SpatialParameters"
            }
          },
          "TemporalParameters": {
            "explode": true,
            "in": "query",
            "name": "TemporalParameters",
            "required": false,
            "schema": {
              "$ref": "#/components/schemas/TemporalParameters"
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
        "fragmentSha256": "933349244c469a924e7d2666b7c3acd297411543a3730b2fbbc4e77da83be4b1",
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
            "operationId": "Get Stations",
            "parameters": [
              {
                "$ref": "#/components/parameters/SpatialParameters"
              },
              {
                "$ref": "#/components/parameters/TemporalParameters"
              },
              {
                "$ref": "#/components/parameters/dataFrequency"
              }
            ],
            "path": "/stations",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "items": {
                        "$ref": "#/components/schemas/Station"
                      },
                      "type": "array"
                    }
                  },
                  "text/plain": {
                    "schema": {
                      "type": "object"
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
          "SpatialParameters": {
            "properties": {
              "location": {
                "type": "string"
              },
              "radius": {
                "type": "integer"
              },
              "stationCount": {
                "type": "integer"
              }
            },
            "type": "object"
          },
          "Station": {
            "properties": {
              "ETRS89_H": {
                "type": "number"
              },
              "ETRS89_Lat": {
                "type": "string"
              },
              "ETRS89_Long": {
                "type": "string"
              },
              "ETRS89_X": {
                "type": "number"
              },
              "ETRS89_Y": {
                "type": "number"
              },
              "ETRS89_Z": {
                "type": "number"
              },
              "OSGB36_E": {
                "type": "number"
              },
              "OSGB36_N": {
                "type": "number"
              },
              "dataFrequency": {
                "type": "string"
              },
              "distance": {
                "type": "number"
              },
              "links": {
                "items": {
                  "$ref": "#/components/schemas/Link"
                },
                "type": "array"
              },
              "ortho_Datum": {
                "type": "string"
              },
              "ortho_h": {
                "type": "number"
              },
              "percentageComplete": {
                "maximum": 100,
                "minimum": 0,
                "type": "integer"
              },
              "stationId": {
                "type": "string"
              },
              "stationName": {
                "type": "string"
              },
              "tranModel": {
                "type": "string"
              }
            },
            "required": [
              "stationId",
              "ETRS89_X",
              "ETRS89_Y",
              "ETRS89_Z",
              "ETRS89_Lat",
              "ETRS89_Long",
              "ETRS89_H",
              "OSGB36_N",
              "OSGB36_E",
              "ortho_h",
              "ortho_Datum",
              "tranModel",
              "percentageComplete"
            ],
            "type": "object"
          },
          "TemporalParameters": {
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
          "date": {
            "in": "query",
            "name": "date",
            "required": true,
            "schema": {
              "format": "date",
              "type": "string"
            }
          }
        },
        "fragmentSha256": "991ad9286661e85c7e4c220b14ac938c7e5e554282b451fe5e682b7f80503946",
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
            "operationId": "Get Network Health",
            "parameters": [
              {
                "$ref": "#/components/parameters/date"
              },
              {
                "$ref": "#/components/parameters/dataFrequency"
              }
            ],
            "path": "/stations/health",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/StationNetworkHealth"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {
          "HourlyData": {
            "items": {
              "properties": {
                "dataFrequency": {
                  "type": "string"
                },
                "hour": {
                  "maximum": 23,
                  "minimum": 0,
                  "type": "integer"
                },
                "percentageComplete": {
                  "maximum": 100,
                  "minimum": 0,
                  "type": "integer"
                }
              },
              "type": "object"
            },
            "type": "array"
          },
          "StationNetworkHealth": {
            "items": {
              "properties": {
                "hourlyData": {
                  "$ref": "#/components/schemas/HourlyData"
                },
                "stationId": {
                  "type": "string"
                }
              },
              "type": "object"
            },
            "type": "array"
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
          "TemporalParameters": {
            "explode": true,
            "in": "query",
            "name": "TemporalParameters",
            "required": false,
            "schema": {
              "$ref": "#/components/schemas/TemporalParameters"
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
        "fragmentSha256": "69c12f7491f59d2ededb2bee5c5019dfdf2e3336d9af4ee133f1af8b309b7eb5",
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
            "operationId": "Get Station",
            "parameters": [
              {
                "$ref": "#/components/parameters/stationId"
              },
              {
                "$ref": "#/components/parameters/TemporalParameters"
              },
              {
                "$ref": "#/components/parameters/dataFrequency"
              }
            ],
            "path": "/stations/{stationId}",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/Station"
                    }
                  },
                  "text/plain": {
                    "schema": {
                      "type": "object"
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
          "Station": {
            "properties": {
              "ETRS89_H": {
                "type": "number"
              },
              "ETRS89_Lat": {
                "type": "string"
              },
              "ETRS89_Long": {
                "type": "string"
              },
              "ETRS89_X": {
                "type": "number"
              },
              "ETRS89_Y": {
                "type": "number"
              },
              "ETRS89_Z": {
                "type": "number"
              },
              "OSGB36_E": {
                "type": "number"
              },
              "OSGB36_N": {
                "type": "number"
              },
              "dataFrequency": {
                "type": "string"
              },
              "distance": {
                "type": "number"
              },
              "links": {
                "items": {
                  "$ref": "#/components/schemas/Link"
                },
                "type": "array"
              },
              "ortho_Datum": {
                "type": "string"
              },
              "ortho_h": {
                "type": "number"
              },
              "percentageComplete": {
                "maximum": 100,
                "minimum": 0,
                "type": "integer"
              },
              "stationId": {
                "type": "string"
              },
              "stationName": {
                "type": "string"
              },
              "tranModel": {
                "type": "string"
              }
            },
            "required": [
              "stationId",
              "ETRS89_X",
              "ETRS89_Y",
              "ETRS89_Z",
              "ETRS89_Lat",
              "ETRS89_Long",
              "ETRS89_H",
              "OSGB36_N",
              "OSGB36_E",
              "ortho_h",
              "ortho_Datum",
              "tranModel",
              "percentageComplete"
            ],
            "type": "object"
          },
          "TemporalParameters": {
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
        "fragmentSha256": "2a15547fba9075d02b0ec67a386faba7d3d4ad4f6dfd176b9e6ccfcd83d3df35",
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
            "operationId": "Get Station Health",
            "parameters": [
              {
                "$ref": "#/components/parameters/stationId"
              },
              {
                "$ref": "#/components/parameters/dataFrequency"
              }
            ],
            "path": "/stations/{stationId}/health",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/HealthByDate"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {
          "HealthByDate": {
            "items": {
              "properties": {
                "date": {
                  "format": "date",
                  "type": "string"
                },
                "hourlyData": {
                  "$ref": "#/components/schemas/HourlyData"
                }
              },
              "type": "object"
            },
            "type": "array"
          },
          "HourlyData": {
            "items": {
              "properties": {
                "dataFrequency": {
                  "type": "string"
                },
                "hour": {
                  "maximum": 23,
                  "minimum": 0,
                  "type": "integer"
                },
                "percentageComplete": {
                  "maximum": 100,
                  "minimum": 0,
                  "type": "integer"
                }
              },
              "type": "object"
            },
            "type": "array"
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
        "fragmentSha256": "0ba1def98cb6d88e1b2c6d0968cfa4ee57658ff383267e555a4921848e029c2d",
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
            "operationId": "Get Station Logs",
            "parameters": [
              {
                "$ref": "#/components/parameters/stationId"
              }
            ],
            "path": "/stations/{stationId}/log",
            "responses": {
              "200": {
                "content": {
                  "application/xml": {
                    "schema": {
                      "type": "string"
                    }
                  },
                  "text/plain": {
                    "schema": {
                      "type": "string"
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
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/stations.md",
    "kind": "documentation-contract",
    "sourceSha256": "f14c4f5052661d4e0cedb603efb7bbba70c5eceb67081855aeea3048dd308a90",
    "title": "Stations",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/stations.md"
  }
}
---

# Stations

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/stations.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-net-api/technical-specification/stations.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
