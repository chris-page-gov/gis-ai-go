---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-features-api%2Ftechnical-specification%2Fgetfeature.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "getFeature",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/technical-specification/getfeature.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/technical-specification/getfeature.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/technical-specification/getfeature.md",
      "retrievedAt": "2026-10-02T07:27:14.640559Z",
      "responseSha256": "486bd0fb88ba03b7c3c703afaf22c527b2970321f61c32b0f2e832f23e473795",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/66",
      "normalisedRecordSha256": "94120b60fdff83c1825fd7561513c894bfa3ac4e60c9787f6f2ceab70d7714cb",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/technical-specification/getfeature.md"
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
        "fragmentSha256": "0d61bd3529af49e6ffa88c5de5e5e933a976df0f3037a50d429e89ba71392670",
        "jsonFence": 1,
        "openapi": "3.0.1",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": [
              {
                "api-key": [],
                "api-key-header": [],
                "oauth2": []
              }
            ],
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": "GetFeature",
            "parameters": [
              {
                "in": "query",
                "name": "request",
                "required": true,
                "schema": {
                  "enum": [
                    "GetCapabilities",
                    "DescribeFeatureType",
                    "GetFeature"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "service",
                "required": true,
                "schema": {
                  "enum": [
                    "WFS"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "version",
                "required": true,
                "schema": {
                  "enum": [
                    "1.0.0",
                    "1.1.0",
                    "2.0.0"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "typeNames",
                "required": true,
                "schema": {
                  "enum": [
                    "DetailedPathNetwork_RouteLink",
                    "DetailedPathNetwork_RouteNode",
                    "Highways_RoadLink",
                    "Highways_RoadNode",
                    "Highways_FerryLink",
                    "Highways_FerryNode",
                    "Highways_Street",
                    "Highways_ConnectingLink",
                    "Highways_ConnectingNode",
                    "Highways_PathLink",
                    "Highways_PathNode",
                    "Greenspace_GreenspaceArea",
                    "Sites_AccessPoint",
                    "Sites_RoutingPoint",
                    "Sites_FunctionalSite",
                    "Topography_CartographicText",
                    "Topography_CartographicSymbol",
                    "Topography_TopographicPoint",
                    "Topography_TopographicLine",
                    "Topography_TopographicArea",
                    "Topography_BoundaryLine",
                    "WaterNetwork_HydroNode",
                    "WaterNetwork_WatercourseLink",
                    "Zoomstack_Airports",
                    "Zoomstack_Boundaries",
                    "Zoomstack_Contours",
                    "Zoomstack_DistrictBuildings",
                    "Zoomstack_ETL",
                    "Zoomstack_Foreshore",
                    "Zoomstack_Greenspace",
                    "Zoomstack_LocalBuildings",
                    "Zoomstack_Names",
                    "Zoomstack_NationalParks",
                    "Zoomstack_RailwayStations",
                    "Zoomstack_Rail",
                    "Zoomstack_RoadsLocal",
                    "Zoomstack_RoadsNational",
                    "Zoomstack_RoadsRegional",
                    "Zoomstack_Sites",
                    "Zoomstack_Surfacewater",
                    "Zoomstack_UrbanAreas",
                    "Zoomstack_Waterlines",
                    "Zoomstack_Woodland",
                    "OpenUPRN_Address",
                    "OpenUSRN_USRN",
                    "OpenTOID_TopographyLayer",
                    "OpenTOID_HighwaysNetwork",
                    "OpenTOID_SitesLayer"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "bbox",
                "required": false,
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "filter",
                "required": false,
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "count",
                "required": false,
                "schema": {
                  "maximum": 100,
                  "minimum": 1,
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "maxFeatures",
                "required": false,
                "schema": {
                  "maximum": 100,
                  "minimum": 1,
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "propertyName",
                "required": false,
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "startIndex",
                "required": false,
                "schema": {
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "outputFormat",
                "required": false,
                "schema": {
                  "enum": [
                    "GML32",
                    "GML3",
                    "GML2",
                    "GEOJSON"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "resultType",
                "required": false,
                "schema": {
                  "enum": [
                    "results",
                    "hits"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "srsName",
                "required": false,
                "schema": {
                  "enum": [
                    "EPSG:27700",
                    "EPSG:4326",
                    "EPSG:3857"
                  ],
                  "type": "string"
                }
              }
            ],
            "path": "/wfs",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/FeatureCollection"
                    }
                  },
                  "application/xml": {
                    "schema": {
                      "$ref": "#/components/schemas/FeatureCollection"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "root"
          }
        ],
        "schemas": {
          "Coordinate": {
            "properties": {
              "x": {
                "format": "double",
                "type": "number"
              },
              "y": {
                "format": "double",
                "type": "number"
              }
            },
            "type": "object"
          },
          "Feature": {
            "properties": {
              "geometry": {
                "$ref": "#/components/schemas/Geometry"
              },
              "properties": {
                "additionalProperties": {
                  "type": "object"
                },
                "type": "object"
              },
              "type": {
                "type": "string"
              }
            },
            "type": "object"
          },
          "FeatureCollection": {
            "properties": {
              "features": {
                "items": {
                  "$ref": "#/components/schemas/Feature"
                },
                "type": "array"
              },
              "type": {
                "type": "string"
              }
            },
            "type": "object"
          },
          "Geometry": {
            "properties": {
              "coordinates": {
                "items": {
                  "$ref": "#/components/schemas/Coordinate"
                },
                "type": "array"
              },
              "type": {
                "type": "string"
              }
            },
            "type": "object"
          }
        },
        "securitySchemes": {
          "api-key": {
            "in": "query",
            "name": "key",
            "type": "apiKey"
          }
        },
        "servers": [
          "https://api.os.uk/features/v1"
        ],
        "title": "OS Features API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.0"
      },
      {
        "componentParameters": {},
        "fragmentSha256": "6832fbdef9a1349ad9396114b99d3ae1cf56d3ba662f17a6fc07b98878d34cf3",
        "jsonFence": 2,
        "openapi": "3.0.1",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": [
              {
                "api-key": [],
                "api-key-header": [],
                "oauth2": []
              }
            ],
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": "GetArchiveFeature",
            "parameters": [
              {
                "in": "path",
                "name": "year",
                "required": true,
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "request",
                "required": true,
                "schema": {
                  "enum": [
                    "GetCapabilities",
                    "DescribeFeatureType",
                    "GetFeature"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "service",
                "required": true,
                "schema": {
                  "enum": [
                    "WFS"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "version",
                "required": true,
                "schema": {
                  "enum": [
                    "1.0.0",
                    "1.1.0",
                    "2.0.0"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "typeNames",
                "required": true,
                "schema": {
                  "enum": [
                    "Highways_RoadLink",
                    "Highways_RoadNode",
                    "Highways_FerryLink",
                    "Highways_FerryNode",
                    "Highways_Street",
                    "Highways_ConnectingLink",
                    "Highways_ConnectingNode",
                    "Highways_PathLink",
                    "Highways_PathNode",
                    "Topography_CartographicText",
                    "Topography_CartographicSymbol",
                    "Topography_TopographicPoint",
                    "Topography_TopographicLine",
                    "Topography_TopographicArea",
                    "Topography_BoundaryLine",
                    "OpenUPRN_Address",
                    "ITN_Roads_FerryNode",
                    "ITN_Roads_RoadLink",
                    "ITN_Roads_RoadNode",
                    "ITN_UrbanPaths_ConnectingNode",
                    "ITN_UrbanPaths_FerryNode",
                    "ITN_UrbanPaths_PathLink",
                    "ITN_UrbanPaths_PathNode"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "bbox",
                "required": false,
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "filter",
                "required": false,
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "count",
                "required": false,
                "schema": {
                  "maximum": 100,
                  "minimum": 1,
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "maxFeatures",
                "required": false,
                "schema": {
                  "maximum": 100,
                  "minimum": 1,
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "propertyName",
                "required": false,
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "startIndex",
                "required": false,
                "schema": {
                  "type": "integer"
                }
              },
              {
                "in": "query",
                "name": "outputFormat",
                "required": false,
                "schema": {
                  "enum": [
                    "GML32",
                    "GML3",
                    "GML2",
                    "GEOJSON"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "resultType",
                "required": false,
                "schema": {
                  "enum": [
                    "results",
                    "hits"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "srsName",
                "required": false,
                "schema": {
                  "enum": [
                    "EPSG:27700",
                    "EPSG:4326",
                    "EPSG:3857"
                  ],
                  "type": "string"
                }
              }
            ],
            "path": "/wfs/archive/{year}",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/FeatureCollection"
                    }
                  },
                  "application/xml": {
                    "schema": {
                      "$ref": "#/components/schemas/FeatureCollection"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "root"
          }
        ],
        "schemas": {
          "Coordinate": {
            "properties": {
              "x": {
                "format": "double",
                "type": "number"
              },
              "y": {
                "format": "double",
                "type": "number"
              }
            },
            "type": "object"
          },
          "Feature": {
            "properties": {
              "geometry": {
                "$ref": "#/components/schemas/Geometry"
              },
              "properties": {
                "additionalProperties": {
                  "type": "object"
                },
                "type": "object"
              },
              "type": {
                "type": "string"
              }
            },
            "type": "object"
          },
          "FeatureCollection": {
            "properties": {
              "features": {
                "items": {
                  "$ref": "#/components/schemas/Feature"
                },
                "type": "array"
              },
              "type": {
                "type": "string"
              }
            },
            "type": "object"
          },
          "Geometry": {
            "properties": {
              "coordinates": {
                "items": {
                  "$ref": "#/components/schemas/Coordinate"
                },
                "type": "array"
              },
              "type": {
                "type": "string"
              }
            },
            "type": "object"
          }
        },
        "securitySchemes": {
          "api-key": {
            "in": "query",
            "name": "key",
            "type": "apiKey"
          }
        },
        "servers": [
          "https://api.os.uk/features/v1"
        ],
        "title": "OS Features API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.0"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/technical-specification/getfeature.md",
    "kind": "documentation-contract",
    "sourceSha256": "486bd0fb88ba03b7c3c703afaf22c527b2970321f61c32b0f2e832f23e473795",
    "title": "getFeature",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/technical-specification/getfeature.md"
  }
}
---

# getFeature

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/technical-specification/getfeature.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-features-api/technical-specification/getfeature.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
