---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "RoutingStructure v1",
  "description": "These indicate the location of key structures related to the highway network. These may be: Barriers: Structures or equipment constructed to control, obstruct, or prevent passage or access Bridges and Tunnels Crossings and Signals: Equipment such as traffic signals, and locations that control the flow of traffic",
  "nativeIdentifier": "trn-rami-routingstructure-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "OS NGD",
    "trn",
    "schema",
    "queryables"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections",
      "retrievedAt": "2026-10-02T01:18:50.822323Z",
      "responseSha256": "cf6f9c7670533ff42c64af98a8f7bb8aa60911463d937623a4fc6f5bb8767de9",
      "sourcePointer": "/collections/80",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/80",
      "normalisedRecordSha256": "ae997be58b27d2268075c412b5560c0e0d5e807d2d2e4fd335019f035751453b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1"
  },
  "dcterms:conformsTo": [
    {
      "@id": "http://www.opengis.net/spec/ogcapi-features-1/1.0"
    },
    {
      "@id": "http://www.opengis.net/def/crs/EPSG/0/27700"
    }
  ],
  "temporal": {
    "status": "source-stated",
    "kind": "advertised-collection-temporal-extent",
    "start": "2022-08-24T00:00:00Z",
    "end": null,
    "sourceField": "extent.temporal.interval[0]",
    "note": "An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support."
  },
  "update": {
    "frequency": {
      "status": "not-evidenced",
      "label": null,
      "iri": null,
      "sourceField": null
    },
    "releaseCatalogue": [
      "https://docs.os.uk/osngd/getting-started/os-ngd-release-notes"
    ],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": null,
    "releaseVersion": null
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "OS NGD protected data: licence and entitlement required; public schemas do not grant feature access or AI-hosting rights.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [],
  "details": {
    "crs": [
      "http://www.opengis.net/def/crs/EPSG/0/27700",
      "http://www.opengis.net/def/crs/EPSG/0/3857",
      "http://www.opengis.net/def/crs/EPSG/0/4326",
      "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
    ],
    "description": "These indicate the location of key structures related to the highway network. These may be:\nBarriers: Structures or equipment constructed to control, obstruct, or prevent passage or access\nBridges and Tunnels\nCrossings and Signals: Equipment such as traffic signals, and locations that control the flow of traffic",
    "extent": {
      "spatial": {
        "bbox": [
          [
            -8.82,
            49.79,
            1.92,
            60.94
          ]
        ],
        "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
      },
      "temporal": {
        "interval": [
          [
            "2022-08-24T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "trn-rami-routingstructure-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1",
        "rel": "self",
        "title": "The 'RoutingStructure v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/items",
        "rel": "items",
        "title": "The features in the 'RoutingStructure v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'RoutingStructure v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'RoutingStructure v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/queryables",
        "properties": {
          "description": {
            "enum": [
              "Barrier",
              "Bridge Over Road",
              "Bridge Under Road",
              "Gate",
              "Level Crossing Fully Barriered",
              "Level Crossing Part Barriered",
              "Level Crossing Unbarriered",
              "Moveable Barrier",
              "Pedestrian Crossing",
              "Rising Bollards",
              "Street Lighting",
              "Structure",
              "Toll Indicator",
              "Traffic Calming",
              "Traffic Signal",
              "Tunnel"
            ],
            "type": [
              "string"
            ]
          },
          "geometry_length": {
            "type": [
              "number"
            ]
          },
          "osid": {
            "type": [
              "string"
            ]
          },
          "toid": {
            "type": [
              "string",
              "null"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "c2945d9a2f7b58574ae308d34d32c38b576267ef6c329e3573a4a09583885243",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-rami-routingstructure-1.0",
        "properties": {
          "atpositionxcoordinate": {
            "type": [
              "number",
              "null"
            ]
          },
          "atpositionycoordinate": {
            "type": [
              "number",
              "null"
            ]
          },
          "changetype": {
            "enum": [
              "End Of Life",
              "Modified Attributes",
              "Modified Geometry",
              "Modified Geometry And Attributes",
              "Moved From A Different Feature Type",
              "Moved To A Different Feature Type",
              "New"
            ],
            "type": "string"
          },
          "description": {
            "enum": [
              "Barrier",
              "Bridge Over Road",
              "Bridge Under Road",
              "Gate",
              "Level Crossing Fully Barriered",
              "Level Crossing Part Barriered",
              "Level Crossing Unbarriered",
              "Moveable Barrier",
              "Pedestrian Crossing",
              "Rising Bollards",
              "Street Lighting",
              "Structure",
              "Toll Indicator",
              "Traffic Calming",
              "Traffic Signal",
              "Tunnel"
            ],
            "type": "string"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/MultiLineString.json"
          },
          "geometry_length": {
            "type": "number"
          },
          "osid": {
            "type": "string"
          },
          "routingstructurenetworkreference": {
            "items": {
              "properties": {
                "networkfeaturetype": {
                  "description": "The type of network feature referenced.",
                  "enum": [
                    "Road Link",
                    "Road Node"
                  ],
                  "maxLength": 9,
                  "originalName": "networkFeatureType",
                  "type": "string"
                },
                "networkreferenceid": {
                  "description": "The identifier of the network reference feature.",
                  "maxLength": 36,
                  "originalName": "networkReferenceID",
                  "type": "string"
                },
                "routingstructureid": {
                  "description": "The identifier for the Routing Structure feature.",
                  "maxLength": 36,
                  "originalName": "routingStructureID",
                  "type": "string"
                },
                "routingstructureversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "routingStructureVersionDate",
                  "pattern": "YYYY-MM-DD",
                  "type": "string"
                }
              },
              "type": "object"
            },
            "type": "array"
          },
          "structuredescription": {
            "type": [
              "string",
              "null"
            ]
          },
          "theme": {
            "enum": [
              "Address",
              "Administrative and Statistical Units",
              "Buildings",
              "Geographical Names",
              "Land",
              "Land Use",
              "Structures",
              "Transport",
              "Water"
            ],
            "type": "string"
          },
          "toid": {
            "type": [
              "string",
              "null"
            ]
          },
          "versionavailablefromdate": {
            "format": "date-time",
            "type": "string"
          },
          "versionavailabletodate": {
            "format": "date-time",
            "type": [
              "string",
              "null"
            ]
          },
          "versiondate": {
            "format": "date",
            "type": "string"
          }
        },
        "required": [
          "changetype",
          "description",
          "geometry",
          "geometry_length",
          "osid",
          "theme",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "63bfbfed6b5c8383e257dd460cc26069f88f4aa77688c21929be8eb32181c15b",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "RoutingStructure v1"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2022-08-24T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/queryables",
      "responseSha256": "c2945d9a2f7b58574ae308d34d32c38b576267ef6c329e3573a4a09583885243",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema",
      "responseSha256": "63bfbfed6b5c8383e257dd460cc26069f88f4aa77688c21929be8eb32181c15b",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/atpositionxcoordinate",
      "@type": "rdf:Property",
      "dcterms:identifier": "atpositionxcoordinate",
      "rdfs:label": "atpositionxcoordinate",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "number",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/atpositionycoordinate",
      "@type": "rdf:Property",
      "dcterms:identifier": "atpositionycoordinate",
      "rdfs:label": "atpositionycoordinate",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "number",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/changetype",
      "@type": "rdf:Property",
      "dcterms:identifier": "changetype",
      "rdfs:label": "changetype",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "End Of Life",
            "Modified Attributes",
            "Modified Geometry",
            "Modified Geometry And Attributes",
            "Moved From A Different Feature Type",
            "Moved To A Different Feature Type",
            "New"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Barrier",
            "Bridge Over Road",
            "Bridge Under Road",
            "Gate",
            "Level Crossing Fully Barriered",
            "Level Crossing Part Barriered",
            "Level Crossing Unbarriered",
            "Moveable Barrier",
            "Pedestrian Crossing",
            "Rising Bollards",
            "Street Lighting",
            "Structure",
            "Toll Indicator",
            "Traffic Calming",
            "Traffic Signal",
            "Tunnel"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/geometry",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry",
      "rdfs:label": "geometry",
      "okfp:schemaDefinition": {
        "@value": {
          "$ref": "https://geojson.org/schema/MultiLineString.json"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/geometry_length",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry_length",
      "rdfs:label": "geometry_length",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/osid",
      "@type": "rdf:Property",
      "dcterms:identifier": "osid",
      "rdfs:label": "osid",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/routingstructurenetworkreference",
      "@type": "rdf:Property",
      "dcterms:identifier": "routingstructurenetworkreference",
      "rdfs:label": "routingstructurenetworkreference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "networkfeaturetype": {
                "description": "The type of network feature referenced.",
                "enum": [
                  "Road Link",
                  "Road Node"
                ],
                "maxLength": 9,
                "originalName": "networkFeatureType",
                "type": "string"
              },
              "networkreferenceid": {
                "description": "The identifier of the network reference feature.",
                "maxLength": 36,
                "originalName": "networkReferenceID",
                "type": "string"
              },
              "routingstructureid": {
                "description": "The identifier for the Routing Structure feature.",
                "maxLength": 36,
                "originalName": "routingStructureID",
                "type": "string"
              },
              "routingstructureversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "routingStructureVersionDate",
                "pattern": "YYYY-MM-DD",
                "type": "string"
              }
            },
            "type": "object"
          },
          "type": "array"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/structuredescription",
      "@type": "rdf:Property",
      "dcterms:identifier": "structuredescription",
      "rdfs:label": "structuredescription",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/theme",
      "@type": "rdf:Property",
      "dcterms:identifier": "theme",
      "rdfs:label": "theme",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Address",
            "Administrative and Statistical Units",
            "Buildings",
            "Geographical Names",
            "Land",
            "Land Use",
            "Structures",
            "Transport",
            "Water"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/toid",
      "@type": "rdf:Property",
      "dcterms:identifier": "toid",
      "rdfs:label": "toid",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/versionavailablefromdate",
      "@type": "rdf:Property",
      "dcterms:identifier": "versionavailablefromdate",
      "rdfs:label": "versionavailablefromdate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date-time",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/versionavailabletodate",
      "@type": "rdf:Property",
      "dcterms:identifier": "versionavailabletodate",
      "rdfs:label": "versionavailabletodate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date-time",
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-routingstructure-1/field/versiondate",
      "@type": "rdf:Property",
      "dcterms:identifier": "versiondate",
      "rdfs:label": "versiondate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1/schema"
      }
    }
  ]
}
---

# RoutingStructure v1

These indicate the location of key structures related to the highway network. These may be: Barriers: Structures or equipment constructed to control, obstruct, or prevent passage or access Bridges and Tunnels Crossings and Signals: Equipment such as traffic signals, and locations that control the flow of traffic

Native identifier: `trn-rami-routingstructure-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-routingstructure-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2022-08-24T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
