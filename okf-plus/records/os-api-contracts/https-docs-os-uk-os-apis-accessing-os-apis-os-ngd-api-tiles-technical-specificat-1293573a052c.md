---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-ngd-api-tiles%2Ftechnical-specification%2Flanding-page.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Landing page",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/landing-page.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/landing-page.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/landing-page.md",
      "retrievedAt": "2026-10-02T07:26:50.095001Z",
      "responseSha256": "d5e7db87d3fb62385591fcbe3ca94bbe18aa43091d131388d51be2f1f45001f6",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/46",
      "normalisedRecordSha256": "fa3f2f58eeaa77a4289cd4d0b26b0f88aa4ce72e925b6a1a57e3b4fcfcef8145",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/landing-page.md"
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
        "fragmentSha256": "e9a993aa2143163dc43cee0cf2da227c1905f823fb4126b263545438ad854405",
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
            "operationId": "getLandingPage",
            "parameters": [],
            "path": "/",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/landingPage"
                    }
                  }
                }
              },
              "400": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/exceptionDto"
                    }
                  }
                }
              },
              "404": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/exceptionDto"
                    }
                  }
                }
              },
              "405": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/exceptionDto"
                    }
                  }
                }
              },
              "406": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/exceptionDto"
                    }
                  }
                }
              },
              "500": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/exceptionDto"
                    }
                  }
                }
              },
              "504": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/exceptionDto"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {
          "exceptionDto": {
            "properties": {
              "code": {
                "type": "integer"
              },
              "description": {
                "type": "string"
              },
              "detail": {
                "type": "string"
              },
              "help": {
                "type": "string"
              },
              "instance": {
                "type": "string"
              },
              "status": {
                "type": "integer"
              },
              "title": {
                "type": "string"
              },
              "type": {
                "type": "string"
              }
            },
            "required": [
              "type"
            ],
            "type": "object"
          },
          "landingPage": {
            "properties": {
              "attribution": {
                "type": "string"
              },
              "description": {
                "type": "string"
              },
              "links": {
                "items": {
                  "$ref": "#/components/schemas/link"
                },
                "type": "array"
              },
              "title": {
                "type": "string"
              }
            },
            "required": [
              "links"
            ],
            "type": "object"
          },
          "link": {
            "properties": {
              "href": {
                "type": "string"
              },
              "hreflang": {
                "type": "string"
              },
              "length": {
                "type": "integer"
              },
              "rel": {
                "type": "string"
              },
              "templated": {
                "type": "boolean"
              },
              "title": {
                "type": "string"
              },
              "type": {
                "type": "string"
              },
              "varBase": {
                "type": "string"
              }
            },
            "required": [
              "href",
              "rel"
            ],
            "type": "object"
          }
        },
        "securitySchemes": {},
        "servers": [
          "https://api.os.uk/maps/vector/ngd/ota/v1"
        ],
        "title": "OS NGD API - Tiles",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.8"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/landing-page.md",
    "kind": "documentation-contract",
    "sourceSha256": "d5e7db87d3fb62385591fcbe3ca94bbe18aa43091d131388d51be2f1f45001f6",
    "title": "Landing page",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/landing-page.md"
  }
}
---

# Landing page

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/landing-page.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/landing-page.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
