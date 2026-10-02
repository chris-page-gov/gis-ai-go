---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-ngd-api-features%2Ftechnical-specification%2Fcollections.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Collections",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collections.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collections.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collections.md",
      "retrievedAt": "2026-10-02T07:26:27.577527Z",
      "responseSha256": "20312bb6e76a03d21eddfa5908b95930259ad24990ab58553c189c06241c0997",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/27",
      "normalisedRecordSha256": "907135cf88e636f83ad7ac584ee35ad1c238c262cc0335d7327dc94284c584f7",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collections.md"
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
        "fragmentSha256": "ea43a847f20bd445277ba7e78ef544e2a32fb3c0a403ec4b9dfb669a0e849674",
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
            "operationId": "getAllCollections",
            "parameters": [],
            "path": "/collections",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/CollectionsResponse"
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
          "CollectionResponse": {
            "properties": {
              "crs": {
                "items": {
                  "enum": [
                    "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
                    "http://www.opengis.net/def/crs/EPSG/0/27700",
                    "http://www.opengis.net/def/crs/EPSG/0/7405",
                    "http://www.opengis.net/def/crs/EPSG/0/4326",
                    "http://www.opengis.net/def/crs/EPSG/0/3857"
                  ],
                  "type": "string"
                },
                "type": "array"
              },
              "description": {
                "type": "string"
              },
              "extent": {
                "$ref": "#/components/schemas/Extent"
              },
              "id": {
                "type": "string"
              },
              "itemType": {
                "type": "string"
              },
              "links": {
                "items": {
                  "$ref": "#/components/schemas/Link"
                },
                "type": "array"
              },
              "storageCrs": {
                "enum": [
                  "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
                  "http://www.opengis.net/def/crs/EPSG/0/27700",
                  "http://www.opengis.net/def/crs/EPSG/0/7405",
                  "http://www.opengis.net/def/crs/EPSG/0/4326",
                  "http://www.opengis.net/def/crs/EPSG/0/3857"
                ],
                "type": "string"
              },
              "title": {
                "type": "string"
              }
            },
            "type": "object"
          },
          "CollectionsResponse": {
            "properties": {
              "collections": {
                "items": {
                  "$ref": "#/components/schemas/CollectionResponse"
                },
                "type": "array"
              },
              "crs": {
                "items": {
                  "enum": [
                    "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
                    "http://www.opengis.net/def/crs/EPSG/0/27700",
                    "http://www.opengis.net/def/crs/EPSG/0/7405",
                    "http://www.opengis.net/def/crs/EPSG/0/4326",
                    "http://www.opengis.net/def/crs/EPSG/0/3857"
                  ],
                  "type": "string"
                },
                "type": "array"
              },
              "links": {
                "items": {
                  "$ref": "#/components/schemas/Link"
                },
                "type": "array"
              }
            },
            "type": "object"
          },
          "Extent": {
            "properties": {
              "spatial": {
                "$ref": "#/components/schemas/SpatialExtent"
              },
              "temporal": {
                "$ref": "#/components/schemas/TemporalExtent"
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
          },
          "SpatialExtent": {
            "properties": {
              "bbox": {
                "items": {
                  "items": {
                    "format": "double",
                    "type": "number"
                  },
                  "type": "array"
                },
                "type": "array"
              },
              "crs": {
                "type": "string"
              }
            },
            "type": "object"
          },
          "TemporalExtent": {
            "properties": {
              "interval": {
                "items": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                },
                "type": "array"
              },
              "trs": {
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
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collections.md",
    "kind": "documentation-contract",
    "sourceSha256": "20312bb6e76a03d21eddfa5908b95930259ad24990ab58553c189c06241c0997",
    "title": "Collections",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collections.md"
  }
}
---

# Collections

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collections.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collections.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
