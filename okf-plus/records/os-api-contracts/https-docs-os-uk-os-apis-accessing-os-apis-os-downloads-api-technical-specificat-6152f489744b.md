---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-downloads-api%2Ftechnical-specification%2Fdownload-a-data-package.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Download a data package",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-a-data-package.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-a-data-package.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-a-data-package.md",
      "retrievedAt": "2026-10-02T07:28:46.194221Z",
      "responseSha256": "e5c4fc0f00f32efcef65c148155528fea1a6d8cb6bf9d0b9fcf74b7557f233a4",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/132",
      "normalisedRecordSha256": "d3c5ec88d8bc3e4a941d43d20d24bfc64bb573cc456074f52158a16722aea528",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-a-data-package.md"
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
          "dataPackageId": {
            "in": "path",
            "name": "dataPackageId",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        },
        "fragmentSha256": "d2191dce237489f1c164339f389e2ccca7685e329ab52dda28a0ab585f8359ae",
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
            "parameters": [
              {
                "$ref": "#/components/parameters/dataPackageId"
              },
              {
                "in": "path",
                "name": "versionId",
                "required": true,
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "fileName",
                "required": true,
                "schema": {
                  "type": "string"
                }
              }
            ],
            "path": "/dataPackages/{dataPackageId}/versions/{versionId}/downloads",
            "responses": {
              "307": {
                "content": {}
              },
              "401": {
                "$ref": "#/components/responses/UnauthorizedError"
              },
              "404": {
                "$ref": "#/components/responses/NotFoundError"
              }
            },
            "securityDeclaration": "root"
          }
        ],
        "schemas": {},
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
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-a-data-package.md",
    "kind": "documentation-contract",
    "sourceSha256": "e5c4fc0f00f32efcef65c148155528fea1a6d8cb6bf9d0b9fcf74b7557f233a4",
    "title": "Download a data package",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-a-data-package.md"
  }
}
---

# Download a data package

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-a-data-package.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-a-data-package.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
