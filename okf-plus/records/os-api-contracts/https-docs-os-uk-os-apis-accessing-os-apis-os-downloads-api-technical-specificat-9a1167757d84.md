---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-downloads-api%2Ftechnical-specification%2Fopendata-products.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "OpenData products",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-products.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-products.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-products.md",
      "retrievedAt": "2026-10-02T07:28:30.972108Z",
      "responseSha256": "a2b47f1b29647f8b3a75bcc4bb7160121a14c5e200cffa20d2720cc4b6f61c98",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/124",
      "normalisedRecordSha256": "e52b60ca5e6a3fd8c51558d880ebfb4e2597c4189e41e73305050d3236fe035a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-products.md"
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
        "fragmentSha256": "c2c3714b68b2bc1015e57d8c0dff1859f0a15050a7a22da91d9b1f6075cff352",
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
                "in": "query",
                "name": "expanded",
                "schema": {
                  "type": "boolean"
                }
              }
            ],
            "path": "/products",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "items": {
                        "$ref": "#/components/schemas/Product"
                      },
                      "type": "array"
                    }
                  }
                }
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
          "Format": {
            "properties": {
              "format": {
                "type": "string"
              },
              "subformat": {
                "type": "string"
              }
            },
            "required": [
              "format"
            ],
            "type": "object"
          },
          "Product": {
            "properties": {
              "areas": {
                "items": {
                  "$ref": "#/components/schemas/Area"
                },
                "type": "array"
              },
              "categories": {
                "items": {
                  "type": "string"
                },
                "type": "array"
              },
              "category": {
                "type": "string"
              },
              "dataStructures": {
                "items": {
                  "enum": [
                    "Raster",
                    "Vector"
                  ],
                  "type": "string"
                },
                "type": "array"
              },
              "description": {
                "items": {
                  "type": "string"
                },
                "minItems": 1,
                "type": "array"
              },
              "documentationUrl": {
                "type": "string"
              },
              "downloadsUrl": {
                "format": "uri",
                "type": "string"
              },
              "endOfLife": {
                "pattern": "^/d{4}-/d{2}-/d{2}$",
                "type": "string"
              },
              "formats": {
                "items": {
                  "$ref": "#/components/schemas/Format"
                },
                "type": "array"
              },
              "id": {
                "type": "string"
              },
              "imageCount": {
                "type": "integer"
              },
              "imageTemplate": {
                "type": "string"
              },
              "name": {
                "type": "string"
              },
              "thirdPartyInfo": {
                "$ref": "#/components/schemas/ThirdPartyInfo"
              },
              "url": {
                "type": "string"
              },
              "version": {
                "pattern": "^/d{4}-/d{2}$",
                "type": "string"
              },
              "warning": {
                "type": "string"
              }
            },
            "required": [
              "id",
              "name",
              "description",
              "version",
              "url"
            ],
            "type": "object"
          },
          "ThirdPartyInfo": {
            "properties": {
              "alsoAvailable": {
                "items": {
                  "properties": {
                    "link": {
                      "format": "uri",
                      "type": "string"
                    },
                    "name": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "name",
                    "link"
                  ],
                  "type": "object"
                },
                "minItems": 0,
                "type": "array"
              },
              "dataProvider": {
                "properties": {
                  "homepage": {
                    "type": "string"
                  },
                  "logoUrl": {
                    "format": "uri",
                    "type": "string"
                  },
                  "name": {
                    "type": "string"
                  },
                  "shortName": {
                    "type": "string"
                  }
                },
                "required": [
                  "name",
                  "shortName",
                  "homepage",
                  "logoUrl"
                ],
                "type": "object"
              },
              "supportEmail": {
                "format": "email",
                "type": "string"
              },
              "supportingInfo": {
                "items": {
                  "properties": {
                    "link": {
                      "format": "uri",
                      "type": "string"
                    },
                    "name": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "name",
                    "link"
                  ],
                  "type": "object"
                },
                "minItems": 0,
                "type": "array"
              }
            },
            "required": [
              "dataProvider",
              "supportingInfo",
              "alsoAvailable",
              "supportEmail"
            ],
            "type": "object"
          }
        },
        "securitySchemes": {},
        "servers": [
          "https://api.os.uk/downloads/v1/"
        ],
        "title": "Ordnance Survey Download API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "1.0.0"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-products.md",
    "kind": "documentation-contract",
    "sourceSha256": "a2b47f1b29647f8b3a75bcc4bb7160121a14c5e200cffa20d2720cc4b6f61c98",
    "title": "OpenData products",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-products.md"
  }
}
---

# OpenData products

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-products.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification/opendata-products.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
