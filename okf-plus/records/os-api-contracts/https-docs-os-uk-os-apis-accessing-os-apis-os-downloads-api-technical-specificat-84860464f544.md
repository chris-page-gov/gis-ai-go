---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-downloads-api%2Ftechnical-specification%2Fdata-packages.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Data packages",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/data-packages.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/data-packages.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/data-packages.md",
      "retrievedAt": "2026-10-02T07:28:38.417316Z",
      "responseSha256": "01eee7620652ebbf8156676346585b600636226d638cb98e77c89815dfa50078",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/128",
      "normalisedRecordSha256": "b13253d00ed116e6ae5b76f4b4d7305ba91bfff1cdf8da959af53c27ca1b959a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/data-packages.md"
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
        "fragmentSha256": "25289b0a903a73fbc0ca459d1dda98dc1d8245989b2bcac87722d55b1c7ab681",
        "jsonFence": 1,
        "openapi": "3.0.0",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": [
              {
                "OAuth2": []
              },
              {
                "APIKeyQuery": []
              },
              {
                "APIKeyHeader": []
              }
            ],
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": null,
            "parameters": [],
            "path": "/dataPackages",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "items": {
                        "$ref": "#/components/schemas/DataPackage"
                      },
                      "type": "array"
                    }
                  }
                }
              },
              "401": {
                "$ref": "#/components/responses/UnauthorizedError"
              }
            },
            "securityDeclaration": "root"
          }
        ],
        "schemas": {
          "DataPackage": {
            "properties": {
              "createdOn": {
                "format": "date",
                "type": "string"
              },
              "id": {
                "type": "string"
              },
              "name": {
                "type": "string"
              },
              "productId": {
                "type": "string"
              },
              "productName": {
                "type": "string"
              },
              "url": {
                "format": "uri",
                "type": "string"
              },
              "versions": {
                "items": {
                  "$ref": "#/components/schemas/DataPackageVersionSummary"
                },
                "type": "array"
              }
            },
            "required": [
              "id",
              "name",
              "url",
              "createdOn",
              "productId",
              "productName",
              "versions"
            ],
            "type": "object"
          },
          "DataPackageVersionSummary": {
            "properties": {
              "createdOn": {
                "format": "date",
                "type": "string"
              },
              "dataPackageUrl": {
                "format": "uri",
                "type": "string"
              },
              "format": {
                "type": "string"
              },
              "id": {
                "type": "string"
              },
              "productVersion": {
                "type": "string"
              },
              "reason": {
                "enum": [
                  "INITIAL",
                  "UPDATE",
                  "EXPANSION",
                  "RESUPPLY",
                  "ONLINE_ORDER"
                ],
                "type": "string"
              },
              "supplyType": {
                "enum": [
                  "FULL",
                  "COU"
                ],
                "type": "string"
              },
              "url": {
                "format": "uri",
                "type": "string"
              }
            },
            "required": [
              "id",
              "url",
              "createdOn",
              "reason",
              "supplyType",
              "productVersion",
              "productFormat"
            ],
            "type": "object"
          }
        },
        "securitySchemes": {
          "APIKeyHeader": {
            "in": "header",
            "name": "key",
            "type": "apiKey"
          },
          "APIKeyQuery": {
            "in": "query",
            "name": "key",
            "type": "apiKey"
          },
          "OAuth2": {
            "flows": {
              "clientCredentials": {
                "scopeNames": [],
                "tokenUrl": "https://api.os.uk/oauth2/token/v1"
              }
            },
            "type": "oauth2"
          }
        },
        "servers": [
          "https://api.os.uk/downloads/v1/"
        ],
        "title": "Ordnance Survey Download API",
        "unresolvedComponentClasses": [
          "responses"
        ],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "1.0.0"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/data-packages.md",
    "kind": "documentation-contract",
    "sourceSha256": "01eee7620652ebbf8156676346585b600636226d638cb98e77c89815dfa50078",
    "title": "Data packages",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/data-packages.md"
  }
}
---

# Data packages

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/data-packages.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/data-packages.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
