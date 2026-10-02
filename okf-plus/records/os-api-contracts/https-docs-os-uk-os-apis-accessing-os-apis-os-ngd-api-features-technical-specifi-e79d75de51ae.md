---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-ngd-api-features%2Ftechnical-specification%2Fcollection.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Collection",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collection.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collection.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collection.md",
      "retrievedAt": "2026-10-02T07:26:28.740672Z",
      "responseSha256": "a676f5abca7a4cf09feffe258d05b0a37d4cbaf92ea9f20b104e9737f8bb89fe",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/28",
      "normalisedRecordSha256": "7a2f1bc6ccd77ce8f70b393ac6433425e1e1fa9f81309b3f7c2348c94ad7cc7a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collection.md"
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
        "fragmentSha256": "15c092e92eb691c984ff7413a83c2b8d0a3e6413d5209246c53c326bd707ec28",
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
            "operationId": "getCollectionById",
            "parameters": [
              {
                "in": "path",
                "name": "collectionId",
                "required": true,
                "schema": {
                  "enum": [
                    "asu-gbpcd-postcodeunitarea-1",
                    "asu-gbpcd-postcodeunitpoint-1",
                    "bld-fts-building-1",
                    "bld-fts-building-2",
                    "bld-fts-building-3",
                    "bld-fts-building-4",
                    "bld-fts-buildingaccesslocation-1",
                    "bld-fts-buildingline-1",
                    "bld-fts-buildingpart-1",
                    "bld-fts-buildingpart-2",
                    "gnm-fts-crowdsourcednamepoint-1",
                    "gnm-fts-namedarea-1",
                    "gnm-fts-namedpoint-1",
                    "gnm-fts-namedroadjunction-1",
                    "lnd-fts-land-1",
                    "lnd-fts-land-2",
                    "lnd-fts-land-3",
                    "lnd-fts-landform-1",
                    "lnd-fts-landformline-1",
                    "lnd-fts-landformpoint-1",
                    "lnd-fts-landpoint-1",
                    "lus-fts-site-1",
                    "lus-fts-site-2",
                    "lus-fts-siteaccesslocation-1",
                    "lus-fts-siteaccesslocation-2",
                    "lus-fts-siteroutingpoint-1",
                    "str-fts-compoundstructure-1",
                    "str-fts-compoundstructure-2",
                    "str-fts-compoundstructure-3",
                    "str-fts-fieldboundary-1",
                    "str-fts-structure-1",
                    "str-fts-structure-2",
                    "str-fts-structure-3",
                    "str-fts-structureline-1",
                    "str-fts-structurepoint-1",
                    "trn-fts-cartographicraildetail-1",
                    "trn-fts-rail-1",
                    "trn-fts-rail-2",
                    "trn-fts-rail-3",
                    "trn-fts-roadline-1",
                    "trn-fts-roadtrackorpath-1",
                    "trn-fts-roadtrackorpath-2",
                    "trn-fts-roadtrackorpath-3",
                    "trn-fts-streetlight-1",
                    "trn-ntwk-buslane-1",
                    "trn-ntwk-connectinglink-1",
                    "trn-ntwk-connectingnode-1",
                    "trn-ntwk-cyclelane-1",
                    "trn-ntwk-ferrylink-1",
                    "trn-ntwk-ferrynode-1",
                    "trn-ntwk-ferryterminal-1",
                    "trn-ntwk-path-1",
                    "trn-ntwk-pathlink-1",
                    "trn-ntwk-pathlink-2",
                    "trn-ntwk-pathlink-3",
                    "trn-ntwk-pathnode-1",
                    "trn-ntwk-pavementlink-1",
                    "trn-ntwk-railwaylink-1",
                    "trn-ntwk-railwaylinkset-1",
                    "trn-ntwk-railwaynode-1",
                    "trn-ntwk-road-1",
                    "trn-ntwk-roadjunction-1",
                    "trn-ntwk-roadlink-1",
                    "trn-ntwk-roadlink-2",
                    "trn-ntwk-roadlink-3",
                    "trn-ntwk-roadlink-4",
                    "trn-ntwk-roadlink-5",
                    "trn-ntwk-roadnode-1",
                    "trn-ntwk-street-1",
                    "trn-ntwk-tramonroad-1",
                    "trn-rami-averageandindicativespeed-1",
                    "trn-rami-highwaydedication-1",
                    "trn-rami-maintenancearea-1",
                    "trn-rami-maintenanceline-1",
                    "trn-rami-maintenancepoint-1",
                    "trn-rami-reinstatementarea-1",
                    "trn-rami-reinstatementline-1",
                    "trn-rami-reinstatementpoint-1",
                    "trn-rami-restriction-1",
                    "trn-rami-routinghazard-1",
                    "trn-rami-routingstructure-1",
                    "trn-rami-specialdesignationarea-1",
                    "trn-rami-specialdesignationline-1",
                    "trn-rami-specialdesignationpoint-1",
                    "wtr-fts-intertidalline-1",
                    "wtr-fts-tidalboundary-1",
                    "wtr-fts-water-1",
                    "wtr-fts-water-2",
                    "wtr-fts-water-3",
                    "wtr-fts-waterpoint-1",
                    "wtr-ntwk-waterlink-1",
                    "wtr-ntwk-waterlink-2",
                    "wtr-ntwk-waterlinkset-1",
                    "wtr-ntwk-waternode-1"
                  ],
                  "type": "string"
                }
              }
            ],
            "path": "/collections/{collectionId}",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/CollectionResponse"
                    }
                  }
                }
              },
              "400": {
                "content": {}
              },
              "404": {
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
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collection.md",
    "kind": "documentation-contract",
    "sourceSha256": "a676f5abca7a4cf09feffe258d05b0a37d4cbaf92ea9f20b104e9737f8bb89fe",
    "title": "Collection",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collection.md"
  }
}
---

# Collection

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collection.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/collection.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
