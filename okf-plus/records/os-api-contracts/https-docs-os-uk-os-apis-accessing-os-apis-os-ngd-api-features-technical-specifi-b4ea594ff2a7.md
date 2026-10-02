---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-ngd-api-features%2Ftechnical-specification%2Flanding-page.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Landing page",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/landing-page.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/landing-page.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/landing-page.md",
      "retrievedAt": "2026-10-02T07:26:25.064179Z",
      "responseSha256": "8e3d4e4e4a868a3b2c8180b1866eb43fe4cea8654da68c1fc5357d5e351e0254",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/25",
      "normalisedRecordSha256": "1669ae4e4a7e91ce47a994e526d476b8cbab389fa8709a4e30164ca551d6f210",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/landing-page.md"
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
        "fragmentSha256": "4663e14b101513102fcd9034411d380d3591fef6343917555dc045ab8e69a9d0",
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
            "operationId": "getLandingPageResponse",
            "parameters": [],
            "path": "/",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/LandingPageResponse"
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
          "LandingPageResponse": {
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
            "type": "object"
          },
          "Link": {
            "properties": {
              "href": {
                "format": "url",
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
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/landing-page.md",
    "kind": "documentation-contract",
    "sourceSha256": "8e3d4e4e4a868a3b2c8180b1866eb43fe4cea8654da68c1fc5357d5e351e0254",
    "title": "Landing page",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/landing-page.md"
  }
}
---

# Landing page

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/landing-page.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/landing-page.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
