---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-linked-identifiers-api%2Ftechnical-specification%2Ffeature-types.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Feature types",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/feature-types.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/feature-types.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/feature-types.md",
      "retrievedAt": "2026-10-02T07:28:20.162065Z",
      "responseSha256": "37994993cc4f12f64bed38cbd56c618ffccbaac1062bfb468c05b1f451e7f1ef",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/117",
      "normalisedRecordSha256": "057f000387faf2ab77fcc2a7c7433fb2d7cdba09234eceea75e32b7c0f31aa83",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/feature-types.md"
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
          "featureIdentifier": {
            "in": "path",
            "name": "id",
            "required": true,
            "schema": {
              "maxLength": 36,
              "minLength": 1,
              "type": "string"
            }
          }
        },
        "fragmentSha256": "d28c7293d04f25b8f12c9ca6c6af6f2e6568ffa94e5cfd4bf2e46b308fcecc5c",
        "jsonFence": 1,
        "openapi": "3.0.0",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": [
              {
                "ApiKeyAuth": []
              },
              {
                "OAuth2": [
                  "read"
                ]
              }
            ],
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": null,
            "parameters": [
              {
                "$ref": "#/components/parameters/featureIdentifier"
              },
              {
                "explode": true,
                "in": "path",
                "name": "featureType",
                "required": true,
                "schema": {
                  "enum": [
                    "BLPU",
                    "ORRoadNode",
                    "ORRoadLink",
                    "Road",
                    "RoadLink",
                    "Street",
                    "TopographicArea"
                  ],
                  "type": "string"
                }
              }
            ],
            "path": "/featureTypes/{featureType}/{id}",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/linkedIdentifier"
                    }
                  }
                }
              },
              "400": {
                "$ref": "#/components/responses/BadRequest"
              },
              "401": {
                "$ref": "#/components/responses/Unauthorized"
              },
              "403": {
                "$ref": "#/components/responses/Forbidden"
              },
              "404": {
                "$ref": "#/components/responses/NotFound"
              },
              "405": {
                "$ref": "#/components/responses/MethodNotAllowed"
              },
              "429": {
                "$ref": "#/components/responses/TooManyRequests"
              },
              "500": {
                "$ref": "#/components/responses/InternalServerError"
              },
              "503": {
                "$ref": "#/components/responses/ServiceUnavailable"
              }
            },
            "securityDeclaration": "root"
          }
        ],
        "schemas": {
          "correlationMethodIdentifier": {
            "enum": [
              "RoadLink_TOID_TopographicArea_TOID_2",
              "Road_TOID_TopographicArea_TOID_3",
              "Street_USRN_TopographicArea_TOID_4",
              "BLPU_UPRN_TopographicArea_TOID_5",
              "RoadLink_TOID_Road_TOID_7",
              "RoadLink_TOID_Street_USRN_8",
              "BLPU_UPRN_RoadLink_TOID_9",
              "Road_TOID_Street_USRN_10",
              "BLPU_UPRN_Street_USRN_11",
              "ORRoadLink_GUID_RoadLink_TOID_12",
              "ORRoadNode_GUID_RoadLink_TOID_13"
            ],
            "type": "string"
          },
          "featureType": {
            "enum": [
              "BLPU",
              "ORRoadNode",
              "ORRoadLink",
              "Road",
              "RoadLink",
              "Street",
              "TopographicArea"
            ],
            "type": "string"
          },
          "identifierType": {
            "enum": [
              "GUID",
              "TOID",
              "UPRN",
              "USRN"
            ],
            "type": "string"
          },
          "linkedIdentifier": {
            "additionalProperties": false,
            "properties": {
              "correlations": {
                "items": {
                  "additionalProperties": false,
                  "properties": {
                    "correlatedFeatureType": {
                      "$ref": "#/components/schemas/featureType"
                    },
                    "correlatedIdentifierType": {
                      "$ref": "#/components/schemas/identifierType"
                    },
                    "correlatedIdentifiers": {
                      "additionalProperties": false,
                      "items": {
                        "properties": {
                          "confidence": {
                            "type": "string"
                          },
                          "correlationIdentifier": {
                            "type": "string"
                          },
                          "identifier": {
                            "type": "string"
                          },
                          "versionDate": {
                            "type": "string"
                          },
                          "versionNumber": {
                            "type": "number"
                          }
                        },
                        "type": "object"
                      },
                      "required": [
                        "identifier",
                        "confidence",
                        "correlationIdentifier"
                      ],
                      "type": "array"
                    },
                    "correlationMethodIdentifier": {
                      "$ref": "#/components/schemas/correlationMethodIdentifier"
                    },
                    "searchedIdentifierVersionDate": {
                      "type": "string"
                    },
                    "searchedIdentifierVersionNumber": {
                      "type": "number"
                    }
                  },
                  "required": [
                    "correlationMethodIdentifier",
                    "correlatedFeatureType",
                    "correlatedIdentifierType",
                    "correlatedIdentifiers"
                  ],
                  "type": "object"
                },
                "type": "array"
              },
              "linkedIdentifier": {
                "additionalProperties": false,
                "properties": {
                  "featureType": {
                    "$ref": "#/components/schemas/featureType"
                  },
                  "identifier": {
                    "type": "string"
                  },
                  "identifierType": {
                    "$ref": "#/components/schemas/identifierType"
                  }
                },
                "required": [
                  "identifier",
                  "featureType",
                  "identifierType"
                ],
                "type": "object"
              }
            },
            "required": [
              "linkedIdentifier",
              "correlations"
            ],
            "type": "object"
          }
        },
        "securitySchemes": {
          "ApiKeyAuth": {
            "in": "query",
            "name": "key",
            "type": "apiKey"
          },
          "OAuth2": {
            "flows": {
              "clientCredentials": {
                "scopeNames": [
                  "read"
                ],
                "tokenUrl": "https://api.os.uk/oauth2/token/v1"
              }
            },
            "type": "oauth2"
          }
        },
        "servers": [
          "${lids.api.server}/search/links/v1"
        ],
        "title": "OS Linked Identifiers API",
        "unresolvedComponentClasses": [
          "responses"
        ],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "1.0.0"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/feature-types.md",
    "kind": "documentation-contract",
    "sourceSha256": "37994993cc4f12f64bed38cbd56c618ffccbaac1062bfb468c05b1f451e7f1ef",
    "title": "Feature types",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/feature-types.md"
  }
}
---

# Feature types

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/feature-types.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/feature-types.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
