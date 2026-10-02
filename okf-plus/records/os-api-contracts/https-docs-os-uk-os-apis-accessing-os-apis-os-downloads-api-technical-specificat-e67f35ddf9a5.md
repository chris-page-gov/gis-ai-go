---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-downloads-api%2Ftechnical-specification%2Fdownload-an-opendata-product.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Download an OpenData product",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-an-opendata-product.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-an-opendata-product.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-an-opendata-product.md",
      "retrievedAt": "2026-10-02T07:28:33.083082Z",
      "responseSha256": "b833a9abf296253b1b89af567f9100368c82bc9936cebc627f3d8ffa55c264b0",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/126",
      "normalisedRecordSha256": "546f16e1cd56a530b1d642ecdd441d470610a035303e750a266ce5b741f29a9a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-an-opendata-product.md"
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
        "fragmentSha256": "7d6d1147473ff91a70691e5ed58b044879a6d9110d720495c6afeab2d0902d9d",
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
                "in": "query",
                "name": "fileName",
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "format",
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "subformat",
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "area",
                "schema": {
                  "$ref": "#/components/schemas/Area"
                }
              },
              {
                "in": "query",
                "name": "redirect",
                "schema": {
                  "type": "boolean"
                }
              }
            ],
            "path": "/products/{productId}/downloads",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "items": {
                        "$ref": "#/components/schemas/ProductDownload"
                      },
                      "type": "array"
                    }
                  }
                }
              },
              "307": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/ProductDownload"
                    }
                  }
                }
              },
              "404": {
                "$ref": "#/components/responses/NotFoundError"
              }
            },
            "securityDeclaration": "not-declared"
          }
        ],
        "schemas": {
          "Area": {
            "enum": [
              "GB",
              "HP",
              "HT",
              "HU",
              "HW",
              "HX",
              "HY",
              "HZ",
              "NA",
              "NB",
              "NC",
              "ND",
              "NF",
              "NG",
              "NH",
              "NJ",
              "NK",
              "NL",
              "NM",
              "NN",
              "NO",
              "NR",
              "NS",
              "NT",
              "NU",
              "NW",
              "NX",
              "NY",
              "NZ",
              "OV",
              "SD",
              "SE",
              "TA",
              "SH",
              "SJ",
              "SK",
              "TF",
              "TG",
              "SM",
              "SN",
              "SO",
              "SP",
              "TL",
              "TM",
              "SR",
              "SS",
              "ST",
              "SU",
              "TQ",
              "TR",
              "SV",
              "SW",
              "SX",
              "SY",
              "SZ",
              "TV"
            ],
            "type": "string"
          },
          "Download": {
            "properties": {
              "fileName": {
                "type": "string"
              },
              "md5": {
                "type": "string"
              },
              "size": {
                "type": "integer"
              },
              "url": {
                "format": "uri",
                "type": "string"
              }
            },
            "required": [
              "url",
              "fileName"
            ],
            "type": "object"
          },
          "ProductDownload": {
            "allOf": [
              {
                "$ref": "#/components/schemas/Download"
              },
              {
                "properties": {
                  "area": {
                    "$ref": "#/components/schemas/Area"
                  },
                  "format": {
                    "type": "string"
                  },
                  "subformat": {
                    "type": "string"
                  }
                },
                "required": [
                  "area",
                  "format"
                ],
                "type": "object"
              }
            ]
          }
        },
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
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-an-opendata-product.md",
    "kind": "documentation-contract",
    "sourceSha256": "b833a9abf296253b1b89af567f9100368c82bc9936cebc627f3d8ffa55c264b0",
    "title": "Download an OpenData product",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-an-opendata-product.md"
  }
}
---

# Download an OpenData product

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-an-opendata-product.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/download-an-opendata-product.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
