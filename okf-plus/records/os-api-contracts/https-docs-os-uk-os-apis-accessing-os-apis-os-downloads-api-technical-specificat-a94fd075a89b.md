---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-downloads-api%2Ftechnical-specification%2Fopendata-product-image.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "OpenData product image",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-product-image.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-product-image.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-product-image.md",
      "retrievedAt": "2026-10-02T07:28:36.137163Z",
      "responseSha256": "2b79e655710b6e314049b0b6bacf96fac3cb86ff185776da00d04e38f688db51",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/127",
      "normalisedRecordSha256": "bbb615cf4558fbfe0721f99f846d63cd118fbfd0185a7a223f68effcf00d8fdc",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-product-image.md"
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
        "fragmentSha256": "f62706597084c1bb2fa909ad5c333436375e7b5cfe2477aab3ae3e4796d4a0ae",
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
            "operationId": null,
            "parameters": [
              {
                "in": "path",
                "name": "productId",
                "required": true,
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "path",
                "name": "index",
                "required": true,
                "schema": {
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "large",
                "schema": {
                  "type": "boolean"
                }
              }
            ],
            "path": "/products/{productId}/images/{index}",
            "responses": {
              "200": {
                "content": {
                  "image/jpeg": {
                    "schema": {
                      "format": "binary",
                      "type": "string"
                    }
                  }
                }
              },
              "307": {
                "content": {}
              },
              "404": {
                "$ref": "#/components/responses/NotFoundError"
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {},
        "securitySchemes": {},
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
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-product-image.md",
    "kind": "documentation-contract",
    "sourceSha256": "2b79e655710b6e314049b0b6bacf96fac3cb86ff185776da00d04e38f688db51",
    "title": "OpenData product image",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-product-image.md"
  }
}
---

# OpenData product image

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-product-image.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-product-image.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
