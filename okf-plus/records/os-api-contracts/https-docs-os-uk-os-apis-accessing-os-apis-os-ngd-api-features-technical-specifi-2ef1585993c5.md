---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-ngd-api-features%2Ftechnical-specification%2Fconformance.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Conformance",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/conformance.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/conformance.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/conformance.md",
      "retrievedAt": "2026-10-02T07:26:26.389885Z",
      "responseSha256": "f952e132b8893385062189954c88564765ebde06063873d5381c6a3bf996f6f3",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/26",
      "normalisedRecordSha256": "af0d44cfff4522d2460c4f179fba0c75802394b777ef4cb7991c64987ecbf1c9",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/conformance.md"
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
        "fragmentSha256": "75bc4d32a0e109705c4ce84440fdf7f4d0236e58fe3015e1f7cd25a7e132846e",
        "jsonFence": 1,
        "openapi": "3.0.1",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": null,
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": "getConformanceResponse",
            "parameters": [],
            "path": "/conformance",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/ConformanceResponse"
                    }
                  }
                }
              },
              "400": {
                "content": {}
              },
              "405": {
                "content": {}
              },
              "406": {
                "content": {}
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {
          "ConformanceResponse": {
            "properties": {
              "conformsTo": {
                "items": {
                  "type": "string"
                },
                "type": "array"
              }
            },
            "type": "object"
          }
        },
        "securitySchemes": {},
        "servers": [
          "https://api.os.uk/features/ngd/ofa/v1"
        ],
        "title": "OS NGD API – Features",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.8.1"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/conformance.md",
    "kind": "documentation-contract",
    "sourceSha256": "f952e132b8893385062189954c88564765ebde06063873d5381c6a3bf996f6f3",
    "title": "Conformance",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/conformance.md"
  }
}
---

# Conformance

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/conformance.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/conformance.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
