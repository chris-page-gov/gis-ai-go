---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-places-api%2Ftechnical-specification%2Fbbox.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "BBOX",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/bbox.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/bbox.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/bbox.md",
      "retrievedAt": "2026-10-02T07:27:54.801826Z",
      "responseSha256": "813f97c771c16255a6b7a12e9846b30d940d4adb0f67915b782513619645ad92",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/100",
      "normalisedRecordSha256": "7732e2ed963b6767716429531fe47b1f359878d63e6a644e86821e872864491c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/bbox.md"
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
        "fragmentSha256": "5f1a7678fc19c1c90792ae5c2ca05c1283deda43605c8c68364f6e0059d199cd",
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
            "operationId": "getBbox",
            "parameters": [
              {
                "in": "query",
                "name": "bbox",
                "required": true,
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "format",
                "required": false,
                "schema": {
                  "enum": [
                    "JSON",
                    "XML"
                  ],
                  "type": "string"
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
            "path": "/bbox",
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
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/bbox.md",
    "kind": "documentation-contract",
    "sourceSha256": "813f97c771c16255a6b7a12e9846b30d940d4adb0f67915b782513619645ad92",
    "title": "BBOX",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/bbox.md"
  }
}
---

# BBOX

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/bbox.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-places-api/technical-specification/bbox.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
