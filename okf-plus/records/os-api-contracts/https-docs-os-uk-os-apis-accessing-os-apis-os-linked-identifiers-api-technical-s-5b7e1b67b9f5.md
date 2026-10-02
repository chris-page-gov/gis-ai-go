---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-linked-identifiers-api%2Ftechnical-specification%2Fproduct-version-information.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Product version information",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/product-version-information.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/product-version-information.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/product-version-information.md",
      "retrievedAt": "2026-10-02T07:28:22.267592Z",
      "responseSha256": "f9fd9fd49ffa7b3a4e09ffdabe8c7f2daff1eafb7eb468ae46d52b0ef52d6db9",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/118",
      "normalisedRecordSha256": "b254e41d1e7d5fc0e886811bf01a2d3b7d62a91e2439d7a6947cc0aa377e24c3",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/product-version-information.md"
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
        "fragmentSha256": "362d22057f8bfd7169458c5787f1b2409a988294886792fbc2da841b71eb6b7b",
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
                "explode": true,
                "in": "path",
                "name": "correlationMethod",
                "required": true,
                "schema": {
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
                }
              }
            ],
            "path": "/productVersionInfo/{correlationMethod}",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/correlationMethodInformation"
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
          "correlationMethodInformation": {
            "additionalProperties": false,
            "properties": {
              "identifier1Source": {
                "$ref": "#/components/schemas/identifierSource"
              },
              "identifier2Source": {
                "$ref": "#/components/schemas/identifierSource"
              },
              "methodIdentifier": {
                "$ref": "#/components/schemas/correlationMethodIdentifier"
              },
              "productCreationDate": {
                "type": "string"
              },
              "productPublicationName": {
                "type": "string"
              }
            },
            "required": [
              "methodIdentfier",
              "productCreationDate",
              "identifier1Source",
              "identifier2Source"
            ],
            "type": "object"
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
          "identifierSource": {
            "additionalProperties": false,
            "properties": {
              "featureType": {
                "$ref": "#/components/schemas/featureType"
              },
              "identifierType": {
                "$ref": "#/components/schemas/identifierType"
              },
              "productName": {
                "enum": [
                  "AddressBase Premium",
                  "OS MasterMap Highways Network - Roads",
                  "OS MasterMap Topography Layer",
                  "OS Open Roads"
                ],
                "type": "string"
              },
              "productPublicationDate": {
                "type": "string"
              },
              "productPublicationName": {
                "type": "string"
              }
            },
            "required": [
              "productName",
              "productPublicationDate",
              "featureType",
              "identifierType"
            ],
            "type": "object"
          },
          "identifierType": {
            "enum": [
              "GUID",
              "TOID",
              "UPRN",
              "USRN"
            ],
            "type": "string"
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
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/product-version-information.md",
    "kind": "documentation-contract",
    "sourceSha256": "f9fd9fd49ffa7b3a4e09ffdabe8c7f2daff1eafb7eb468ae46d52b0ef52d6db9",
    "title": "Product version information",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/product-version-information.md"
  }
}
---

# Product version information

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/product-version-information.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-linked-identifiers-api/technical-specification/product-version-information.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
