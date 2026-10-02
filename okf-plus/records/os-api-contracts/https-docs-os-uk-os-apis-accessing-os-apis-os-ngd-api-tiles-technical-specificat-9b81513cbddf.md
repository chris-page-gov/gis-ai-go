---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-ngd-api-tiles%2Ftechnical-specification%2Fcollection.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Collection",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/collection.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/collection.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/collection.md",
      "retrievedAt": "2026-10-02T07:26:53.899288Z",
      "responseSha256": "3e016222fbfeefdda605b78145d734728d21bbc110f242a96da568d08ac2b56f",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/49",
      "normalisedRecordSha256": "4075d7fc70f5e0f628e7289373cb4164ca4fb854022f7b1085c2829a86222345",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/collection.md"
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
        "fragmentSha256": "0c5d20951f0b33100c3e9f712ce17d873619766a6c13cbc50bdb602b3633b21c",
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
            "operationId": "getCollection",
            "parameters": [
              {
                "in": "path",
                "name": "collectionId",
                "required": true,
                "schema": {
                  "$ref": "#/components/schemas/AllCollections"
                }
              }
            ],
            "path": "/collections/{collectionId}",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/collectionInfo"
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
          "AllCollections": {
            "enum": [
              "ngd-base",
              "asu-bdy",
              "wtr-ctch",
              "trn-ntwk-railway",
              "wtr-tidalboundary"
            ],
            "type": "string"
          },
          "collectionInfo": {
            "properties": {
              "description": {
                "type": "string"
              },
              "extent": {
                "$ref": "#/components/schemas/extent-uad"
              },
              "id": {
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
              "id",
              "links"
            ],
            "type": "object"
          },
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
          "extent": {
            "properties": {
              "spatial": {
                "$ref": "#/components/schemas/extent_spatial"
              }
            },
            "type": "object"
          },
          "extent-uad": {
            "allOf": [
              {
                "$ref": "#/components/schemas/extent"
              },
              {
                "type": "object"
              }
            ]
          },
          "extent_spatial": {
            "properties": {
              "bbox": {
                "items": {
                  "items": {
                    "type": "number"
                  },
                  "maxItems": 4,
                  "minItems": 4,
                  "type": "array"
                },
                "minItems": 1,
                "type": "array"
              },
              "crs": {
                "enum": [
                  "http://www.opengis.net/def/crs/EPSG/0/3857",
                  "http://www.opengis.net/def/crs/EPSG/0/3857h",
                  "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
                  "http://www.opengis.net/def/crs/OGC/0/CRS84h"
                ],
                "type": "string"
              }
            },
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
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/collection.md",
    "kind": "documentation-contract",
    "sourceSha256": "3e016222fbfeefdda605b78145d734728d21bbc110f242a96da568d08ac2b56f",
    "title": "Collection",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/collection.md"
  }
}
---

# Collection

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/collection.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-tiles/technical-specification/collection.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
