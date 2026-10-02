---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-places-api%2Ftechnical-specification%2Fpolygon.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Polygon",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/polygon.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/polygon.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/polygon.md",
      "retrievedAt": "2026-10-02T07:27:57.885990Z",
      "responseSha256": "c667425a04282bdc25b623f0d2516a24d15e066d11eaab88077fc2552372773b",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/102",
      "normalisedRecordSha256": "fb63c4944780dbc451d400a71dc807dc9ad1677ea35cd3e9f872d09dde50454d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/polygon.md"
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
        "fragmentSha256": "ef4802de1b1ea266354789c613b493987519090819c403b1138279a3fc281502",
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
            "httpMethodSemantics": "potential-state-change",
            "method": "POST",
            "operationId": "postPolygon",
            "parameters": [
              {
                "in": "header",
                "name": "Content-Type",
                "required": true,
                "schema": {
                  "enum": [
                    "application/json"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "referencepoint",
                "required": false,
                "schema": {
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "maxresults",
                "required": false,
                "schema": {
                  "maximum": 100,
                  "minimum": 1,
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "offset",
                "required": false,
                "schema": {
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "dataset",
                "required": false,
                "schema": {
                  "enum": [
                    "DPA",
                    "LPI"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "lr",
                "required": false,
                "schema": {
                  "enum": [
                    "EN",
                    "CY"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "output_srs",
                "required": false,
                "schema": {
                  "enum": [
                    "BNG",
                    "EPSG:27700",
                    "WGS84",
                    "EPSG:4326",
                    "EPSG:3857",
                    "EPSG:4258"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "srs",
                "required": false,
                "schema": {
                  "enum": [
                    "BNG",
                    "EPSG:27700",
                    "WGS84",
                    "EPSG:4326",
                    "EPSG:3857",
                    "EPSG:4258"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "fq",
                "required": false,
                "schema": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                }
              }
            ],
            "path": "/polygon",
            "requestBody": {
              "content": {
                "application/json": {
                  "schema": {
                    "properties": {
                      "geometry": {
                        "type": "object"
                      },
                      "type": {
                        "type": "string"
                      }
                    },
                    "required": [
                      "type",
                      "geometry"
                    ],
                    "type": "object"
                  }
                }
              },
              "required": true
            },
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/SearchResult"
                    }
                  },
                  "application/xml": {
                    "schema": {
                      "$ref": "#/components/schemas/SearchResult"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "root"
          }
        ],
        "schemas": {
          "DPA": {
            "properties": {
              "ADDRESS": {
                "type": "string"
              },
              "BLPU_STATE_CODE": {
                "type": "string"
              },
              "BLPU_STATE_CODE_DESCRIPTION": {
                "type": "string"
              },
              "BLPU_STATE_DATE": {
                "type": "string"
              },
              "BUILDING_NAME": {
                "type": "string"
              },
              "BUILDING_NUMBER": {
                "type": "string"
              },
              "CLASSIFICATION_CODE": {
                "type": "string"
              },
              "CLASSIFICATION_CODE_DESCRIPTION": {
                "type": "string"
              },
              "COUNTRY_CODE": {
                "type": "string"
              },
              "COUNTRY_CODE_DESCRIPTION": {
                "type": "string"
              },
              "DELIVERY_POINT_SUFFIX": {
                "type": "string"
              },
              "DEPARTMENT_NAME": {
                "type": "string"
              },
              "DEPENDENT_LOCALITY": {
                "type": "string"
              },
              "DEPENDENT_THOROUGHFARE_NAME": {
                "type": "string"
              },
              "DOUBLE_DEPENDENT_LOCALITY": {
                "type": "string"
              },
              "ENTRY_DATE": {
                "type": "string"
              },
              "LANGUAGE": {
                "type": "string"
              },
              "LAST_UPDATE_DATE": {
                "type": "string"
              },
              "LAT": {
                "type": "number"
              },
              "LEGAL_NAME": {
                "type": "string"
              },
              "LNG": {
                "type": "number"
              },
              "LOCAL_CUSTODIAN_CODE": {
                "type": "integer"
              },
              "LOCAL_CUSTODIAN_CODE_DESCRIPTION": {
                "type": "string"
              },
              "LOGICAL_STATUS_CODE": {
                "type": "string"
              },
              "MATCH": {
                "type": "number"
              },
              "MATCH_DESCRIPTION": {
                "type": "string"
              },
              "ORGANISATION_NAME": {
                "type": "string"
              },
              "PARENT_UPRN": {
                "type": "string"
              },
              "PARISH_CODE": {
                "type": "string"
              },
              "POSTAL_ADDRESS_CODE": {
                "type": "string"
              },
              "POSTAL_ADDRESS_CODE_DESCRIPTION": {
                "type": "string"
              },
              "POSTCODE": {
                "type": "string"
              },
              "POST_TOWN": {
                "type": "string"
              },
              "RPC": {
                "type": "string"
              },
              "STATUS": {
                "type": "string"
              },
              "SUB_BUILDING_NAME": {
                "type": "string"
              },
              "THOROUGHFARE_NAME": {
                "type": "string"
              },
              "TOPOGRAPHY_LAYER_TOID": {
                "type": "string"
              },
              "UDPRN": {
                "type": "string"
              },
              "UPRN": {
                "type": "string"
              },
              "WARD_CODE": {
                "type": "string"
              },
              "X_COORDINATE": {
                "type": "number"
              },
              "Y_COORDINATE": {
                "type": "number"
              }
            },
            "type": "object"
          },
          "LPI": {
            "properties": {
              "ADDRESS": {
                "type": "string"
              },
              "ADMINISTRATIVE_AREA": {
                "type": "string"
              },
              "AREA_NAME": {
                "type": "string"
              },
              "BLPU_STATE_CODE": {
                "type": "string"
              },
              "BLPU_STATE_CODE_DESCRIPTION": {
                "type": "string"
              },
              "BLPU_STATE_DATE": {
                "type": "string"
              },
              "CLASSIFICATION_CODE": {
                "type": "string"
              },
              "CLASSIFICATION_CODE_DESCRIPTION": {
                "type": "string"
              },
              "COUNTRY_CODE": {
                "type": "string"
              },
              "COUNTRY_CODE_DESCRIPTION": {
                "type": "string"
              },
              "ENTRY_DATE": {
                "type": "string"
              },
              "LANGUAGE": {
                "type": "string"
              },
              "LAST_UPDATE_DATE": {
                "type": "string"
              },
              "LAT": {
                "type": "number"
              },
              "LEGAL_NAME": {
                "type": "string"
              },
              "LNG": {
                "type": "number"
              },
              "LOCALITY_NAME": {
                "type": "string"
              },
              "LOCAL_CUSTODIAN_CODE": {
                "type": "integer"
              },
              "LOCAL_CUSTODIAN_CODE_DESCRIPTION": {
                "type": "string"
              },
              "LOGICAL_STATUS_CODE": {
                "type": "string"
              },
              "LPI_KEY": {
                "type": "string"
              },
              "LPI_LOGICAL_STATUS_CODE": {
                "type": "string"
              },
              "LPI_LOGICAL_STATUS_CODE_DESCRIPTION": {
                "type": "string"
              },
              "MATCH": {
                "type": "number"
              },
              "MATCH_DESCRIPTION": {
                "type": "string"
              },
              "ORGANISATION": {
                "type": "string"
              },
              "PAO_END_NUMBER": {
                "type": "string"
              },
              "PAO_END_SUFFIX": {
                "type": "string"
              },
              "PAO_START_NUMBER": {
                "type": "string"
              },
              "PAO_START_SUFFIX": {
                "type": "string"
              },
              "PAO_TEXT": {
                "type": "string"
              },
              "PARENT_UPRN": {
                "type": "string"
              },
              "PARISH_CODE": {
                "type": "string"
              },
              "POSTAL_ADDRESS_CODE": {
                "type": "string"
              },
              "POSTAL_ADDRESS_CODE_DESCRIPTION": {
                "type": "string"
              },
              "POSTCODE_LOCATOR": {
                "type": "string"
              },
              "RPC": {
                "type": "string"
              },
              "SAO_END_NUMBER": {
                "type": "string"
              },
              "SAO_END_SUFFIX": {
                "type": "string"
              },
              "SAO_START_NUMBER": {
                "type": "string"
              },
              "SAO_START_SUFFIX": {
                "type": "string"
              },
              "SAO_TEXT": {
                "type": "string"
              },
              "STATUS": {
                "type": "string"
              },
              "STREET_CLASSIFICATION_CODE": {
                "type": "string"
              },
              "STREET_CLASSIFICATION_CODE_DESCRIPTION": {
                "type": "string"
              },
              "STREET_DESCRIPTION": {
                "type": "string"
              },
              "STREET_STATE_CODE": {
                "type": "string"
              },
              "STREET_STATE_CODE_DESCRIPTION": {
                "type": "string"
              },
              "TOPOGRAPHY_LAYER_TOID": {
                "type": "string"
              },
              "TOWN_NAME": {
                "type": "string"
              },
              "UPRN": {
                "type": "string"
              },
              "USRN": {
                "type": "string"
              },
              "WARD_CODE": {
                "type": "string"
              },
              "X_COORDINATE": {
                "type": "number"
              },
              "Y_COORDINATE": {
                "type": "number"
              }
            },
            "type": "object"
          },
          "SearchResult": {
            "properties": {
              "header": {
                "properties": {
                  "dataset": {
                    "type": "string"
                  },
                  "epoch": {
                    "type": "string"
                  },
                  "format": {
                    "type": "string"
                  },
                  "lastupdate": {
                    "type": "string"
                  },
                  "lr": {
                    "type": "string"
                  },
                  "matchprecision": {
                    "type": "integer"
                  },
                  "maxresults": {
                    "type": "integer"
                  },
                  "offset": {
                    "type": "integer"
                  },
                  "output_srs": {
                    "type": "string"
                  },
                  "query": {
                    "type": "string"
                  },
                  "totalresults": {
                    "type": "integer"
                  },
                  "uri": {
                    "type": "string"
                  }
                },
                "required": [
                  "uri",
                  "query",
                  "offset",
                  "totalresults",
                  "format",
                  "dataset",
                  "lr",
                  "maxresults",
                  "matchprecision",
                  "epoch",
                  "lastupdate",
                  "output_srs"
                ],
                "type": "object"
              },
              "results": {
                "items": {
                  "properties": {
                    "DPA": {
                      "$ref": "#/components/schemas/DPA"
                    },
                    "LPI": {
                      "$ref": "#/components/schemas/LPI"
                    }
                  },
                  "type": "object"
                },
                "type": "array"
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
          "https://api.os.uk/search/places/v1"
        ],
        "title": "OS Places API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.0"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/polygon.md",
    "kind": "documentation-contract",
    "sourceSha256": "c667425a04282bdc25b623f0d2516a24d15e066d11eaab88077fc2552372773b",
    "title": "Polygon",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/polygon.md"
  }
}
---

# Polygon

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/polygon.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/polygon.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
