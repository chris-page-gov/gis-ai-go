---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Path Link v2",
  "description": "A Path Link is a linear spatial object that defines the geometry and connectivity of the path network between two points in the network. Path Links will be split for connectivity purposes (for example, at junctions) and Path Nodes will connect the Path Links together. Each Path Link will provide a reference to the Path Nodes at the start and end of the Path Link. Path Links will be captured where: They provide a route that cannot be inferred from the Road Network. They provide connectivity between road networks. There is a canal path or tow path. There are paths over footbridges and under subways. Path Links will not be captured where: They run parallel to the Road Network (for example, a pavement). They are connected to a motorway. There is a physical obstruction which prevents connectivity.",
  "nativeIdentifier": "trn-ntwk-pathlink-2",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2",
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
      "sourcePointer": "/collections/53",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/53",
      "normalisedRecordSha256": "a36ef86287c5dbcee7e00a2515de037092a602005f81f89dcb286c5b4e12ad69",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2"
  },
  "dcterms:conformsTo": [
    {
      "@id": "http://www.opengis.net/spec/ogcapi-features-1/1.0"
    },
    {
      "@id": "http://www.opengis.net/def/crs/EPSG/0/7405"
    }
  ],
  "temporal": {
    "status": "source-stated",
    "kind": "advertised-collection-temporal-extent",
    "start": "2025-03-22T00:00:00Z",
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
      "http://www.opengis.net/def/crs/EPSG/0/7405",
      "http://www.opengis.net/def/crs/EPSG/0/27700",
      "http://www.opengis.net/def/crs/EPSG/0/3857",
      "http://www.opengis.net/def/crs/EPSG/0/4326",
      "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
    ],
    "description": "A Path Link is a linear spatial object that defines the geometry and connectivity of the path network between two points in the network. Path Links will be split for connectivity purposes (for example, at junctions) and Path Nodes will connect the Path Links together. Each Path Link will provide a reference to the Path Nodes at the start and end of the Path Link. Path Links will be captured where: They provide a route that cannot be inferred from the Road Network. They provide connectivity between road networks. There is a canal path or tow path. There are paths over footbridges and under subways. Path Links will not be captured where: They run parallel to the Road Network (for example, a pavement). They are connected to a motorway. There is a physical obstruction which prevents connectivity.",
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
            "2025-03-22T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "trn-ntwk-pathlink-2",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2",
        "rel": "self",
        "title": "The 'Path Link v2' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/items",
        "rel": "items",
        "title": "The features in the 'Path Link v2' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema",
        "rel": "describedby",
        "title": "Schema for the 'Path Link v2' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Path Link v2' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/queryables",
        "properties": {
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
            "type": [
              "string"
            ]
          },
          "description": {
            "enum": [
              "Canal Path",
              "Collapsed Dual Carriageway",
              "Dual Carriageway",
              "Enclosed Traffic Area",
              "Footbridge",
              "Guided Busway",
              "Layby",
              "Path",
              "Path With Ford",
              "Path With Level Crossing",
              "Path With Steps",
              "Roundabout",
              "Service Road",
              "Shared Use Carriageway",
              "Single Carriageway",
              "Slip Road",
              "Subway",
              "Track",
              "Traffic Island Link",
              "Traffic Island Link At Junction"
            ],
            "type": [
              "string"
            ]
          },
          "geometry_length_m": {
            "type": [
              "number"
            ]
          },
          "osid": {
            "format": "uuid",
            "type": [
              "string"
            ]
          },
          "pathname1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "pathname2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "presenceofstreetlight_coverage": {
            "enum": [
              "Fully Lit",
              "Mostly Lit",
              "Mostly Unlit",
              "Fully Unlit",
              "Unknown"
            ],
            "type": [
              "string"
            ]
          },
          "surfacetype": {
            "enum": [
              "Made Sealed",
              "Made Unknown",
              "Made Unsealed",
              "Unmade"
            ],
            "type": [
              "string",
              "null"
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
        "sha256": "3ff2843a7d2f80e7f7edbbf19622713e43789c8cb40728c062035070d6d67a5f",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-ntwk-pathlink-2.0",
        "properties": {
          "alternatename1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "alternatename1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "alternatename2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "alternatename2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "capturespecification": {
            "enum": [
              "Moorland",
              "Rural",
              "Urban"
            ],
            "type": "string"
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
          "cyclefacility": {
            "enum": [
              "Advisory Cycle Lane Along Road",
              "Mandatory Cycle Lane Along Road",
              "Marking Segregated Cycle Route Along Footway",
              "Physically Segregated Cycle Lane Along Road",
              "Physically Segregated Cycle Route Along Footway",
              "Shared Use Cycle Route Along Footway",
              "Signed Cycle Route",
              "Unknown Type Of Cycle Route Along Footway",
              "Unknown Type Of Cycle Route Along Road"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "cyclefacility_wholelink": {
            "type": [
              "boolean",
              "null"
            ]
          },
          "description": {
            "enum": [
              "Canal Path",
              "Collapsed Dual Carriageway",
              "Dual Carriageway",
              "Enclosed Traffic Area",
              "Footbridge",
              "Guided Busway",
              "Layby",
              "Path",
              "Path With Ford",
              "Path With Level Crossing",
              "Path With Steps",
              "Roundabout",
              "Service Road",
              "Shared Use Carriageway",
              "Single Carriageway",
              "Slip Road",
              "Subway",
              "Track",
              "Traffic Island Link",
              "Traffic Island Link At Junction"
            ],
            "type": "string"
          },
          "elevationgain_againstdirection": {
            "type": "number"
          },
          "elevationgain_indirection": {
            "type": "number"
          },
          "endgradeseparation": {
            "type": "integer"
          },
          "endnode": {
            "type": "string"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/LineString.json",
            "type": "object"
          },
          "geometry_length_m": {
            "type": "number"
          },
          "heightingmethod": {
            "enum": [
              "DTM",
              "Interpolated Bridge",
              "Interpolated Tunnel"
            ],
            "type": "string"
          },
          "matchstatus": {
            "enum": [
              "Matched",
              "Matched With Attribute Discrepancy",
              "No Match",
              "Not Matched Awaiting Review"
            ],
            "type": "string"
          },
          "osid": {
            "format": "uuid",
            "type": "string"
          },
          "pathname1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "pathname1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "pathname2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "pathname2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "presenceofstreetlight_capturemethod": {
            "enum": [
              "Automated Process",
              "Default Value",
              "Desk-Based",
              "Field Survey",
              "Remote Sensing Survey",
              "Sensor Measurement",
              "Third Party Unknown"
            ],
            "type": "string"
          },
          "presenceofstreetlight_coverage": {
            "enum": [
              "Fully Lit",
              "Mostly Lit",
              "Mostly Unlit",
              "Fully Unlit",
              "Unknown"
            ],
            "type": "string"
          },
          "presenceofstreetlight_evidencedate": {
            "format": "date",
            "type": "string"
          },
          "presenceofstreetlight_updatedate": {
            "format": "date",
            "type": "string"
          },
          "startgradeseparation": {
            "type": "integer"
          },
          "startnode": {
            "type": "string"
          },
          "surfacetype": {
            "enum": [
              "Made Sealed",
              "Made Unknown",
              "Made Unsealed",
              "Unmade"
            ],
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
          "osid",
          "toid",
          "versiondate",
          "versionavailablefromdate",
          "versionavailabletodate",
          "changetype",
          "geometry",
          "geometry_length_m",
          "theme",
          "description",
          "pathname1_text",
          "pathname1_language",
          "pathname2_text",
          "pathname2_language",
          "alternatename1_text",
          "alternatename1_language",
          "alternatename2_text",
          "alternatename2_language",
          "surfacetype",
          "cyclefacility",
          "cyclefacility_wholelink",
          "elevationgain_indirection",
          "elevationgain_againstdirection",
          "heightingmethod",
          "capturespecification",
          "matchstatus",
          "startnode",
          "startgradeseparation",
          "endnode",
          "endgradeseparation",
          "presenceofstreetlight_coverage",
          "presenceofstreetlight_evidencedate",
          "presenceofstreetlight_updatedate",
          "presenceofstreetlight_capturemethod"
        ],
        "requiredUndeclared": [],
        "sha256": "ee559966a99adeedaabf39599a58a43675139f0edbebd7ee17f64e6c13920f65",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/7405",
    "title": "Path Link v2"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2025-03-22T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/queryables",
      "responseSha256": "3ff2843a7d2f80e7f7edbbf19622713e43789c8cb40728c062035070d6d67a5f",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema",
      "responseSha256": "ee559966a99adeedaabf39599a58a43675139f0edbebd7ee17f64e6c13920f65",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/alternatename1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "alternatename1_language",
      "rdfs:label": "alternatename1_language",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "eng",
            "gla",
            "cym"
          ],
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/alternatename1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "alternatename1_text",
      "rdfs:label": "alternatename1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/alternatename2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "alternatename2_language",
      "rdfs:label": "alternatename2_language",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "eng",
            "gla",
            "cym"
          ],
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/alternatename2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "alternatename2_text",
      "rdfs:label": "alternatename2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/capturespecification",
      "@type": "rdf:Property",
      "dcterms:identifier": "capturespecification",
      "rdfs:label": "capturespecification",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Moorland",
            "Rural",
            "Urban"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/changetype",
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
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/cyclefacility",
      "@type": "rdf:Property",
      "dcterms:identifier": "cyclefacility",
      "rdfs:label": "cyclefacility",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Advisory Cycle Lane Along Road",
            "Mandatory Cycle Lane Along Road",
            "Marking Segregated Cycle Route Along Footway",
            "Physically Segregated Cycle Lane Along Road",
            "Physically Segregated Cycle Route Along Footway",
            "Shared Use Cycle Route Along Footway",
            "Signed Cycle Route",
            "Unknown Type Of Cycle Route Along Footway",
            "Unknown Type Of Cycle Route Along Road"
          ],
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/cyclefacility_wholelink",
      "@type": "rdf:Property",
      "dcterms:identifier": "cyclefacility_wholelink",
      "rdfs:label": "cyclefacility_wholelink",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Canal Path",
            "Collapsed Dual Carriageway",
            "Dual Carriageway",
            "Enclosed Traffic Area",
            "Footbridge",
            "Guided Busway",
            "Layby",
            "Path",
            "Path With Ford",
            "Path With Level Crossing",
            "Path With Steps",
            "Roundabout",
            "Service Road",
            "Shared Use Carriageway",
            "Single Carriageway",
            "Slip Road",
            "Subway",
            "Track",
            "Traffic Island Link",
            "Traffic Island Link At Junction"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/elevationgain_againstdirection",
      "@type": "rdf:Property",
      "dcterms:identifier": "elevationgain_againstdirection",
      "rdfs:label": "elevationgain_againstdirection",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/elevationgain_indirection",
      "@type": "rdf:Property",
      "dcterms:identifier": "elevationgain_indirection",
      "rdfs:label": "elevationgain_indirection",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/endgradeseparation",
      "@type": "rdf:Property",
      "dcterms:identifier": "endgradeseparation",
      "rdfs:label": "endgradeseparation",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/endnode",
      "@type": "rdf:Property",
      "dcterms:identifier": "endnode",
      "rdfs:label": "endnode",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/geometry",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry",
      "rdfs:label": "geometry",
      "okfp:schemaDefinition": {
        "@value": {
          "$ref": "https://geojson.org/schema/LineString.json",
          "type": "object"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/geometry_length_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry_length_m",
      "rdfs:label": "geometry_length_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/heightingmethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "heightingmethod",
      "rdfs:label": "heightingmethod",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "DTM",
            "Interpolated Bridge",
            "Interpolated Tunnel"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/matchstatus",
      "@type": "rdf:Property",
      "dcterms:identifier": "matchstatus",
      "rdfs:label": "matchstatus",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Matched",
            "Matched With Attribute Discrepancy",
            "No Match",
            "Not Matched Awaiting Review"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/osid",
      "@type": "rdf:Property",
      "dcterms:identifier": "osid",
      "rdfs:label": "osid",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "uuid",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/pathname1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "pathname1_language",
      "rdfs:label": "pathname1_language",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "eng",
            "gla",
            "cym"
          ],
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/pathname1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "pathname1_text",
      "rdfs:label": "pathname1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/pathname2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "pathname2_language",
      "rdfs:label": "pathname2_language",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "eng",
            "gla",
            "cym"
          ],
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/pathname2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "pathname2_text",
      "rdfs:label": "pathname2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/presenceofstreetlight_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofstreetlight_capturemethod",
      "rdfs:label": "presenceofstreetlight_capturemethod",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Automated Process",
            "Default Value",
            "Desk-Based",
            "Field Survey",
            "Remote Sensing Survey",
            "Sensor Measurement",
            "Third Party Unknown"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/presenceofstreetlight_coverage",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofstreetlight_coverage",
      "rdfs:label": "presenceofstreetlight_coverage",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Fully Lit",
            "Mostly Lit",
            "Mostly Unlit",
            "Fully Unlit",
            "Unknown"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/presenceofstreetlight_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofstreetlight_evidencedate",
      "rdfs:label": "presenceofstreetlight_evidencedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/presenceofstreetlight_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofstreetlight_updatedate",
      "rdfs:label": "presenceofstreetlight_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/startgradeseparation",
      "@type": "rdf:Property",
      "dcterms:identifier": "startgradeseparation",
      "rdfs:label": "startgradeseparation",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/startnode",
      "@type": "rdf:Property",
      "dcterms:identifier": "startnode",
      "rdfs:label": "startnode",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/surfacetype",
      "@type": "rdf:Property",
      "dcterms:identifier": "surfacetype",
      "rdfs:label": "surfacetype",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Made Sealed",
            "Made Unknown",
            "Made Unsealed",
            "Unmade"
          ],
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/toid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-pathlink-2/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2/schema"
      }
    }
  ]
}
---

# Path Link v2

A Path Link is a linear spatial object that defines the geometry and connectivity of the path network between two points in the network. Path Links will be split for connectivity purposes (for example, at junctions) and Path Nodes will connect the Path Links together. Each Path Link will provide a reference to the Path Nodes at the start and end of the Path Link. Path Links will be captured where: They provide a route that cannot be inferred from the Road Network. They provide connectivity between road networks. There is a canal path or tow path. There are paths over footbridges and under subways. Path Links will not be captured where: They run parallel to the Road Network (for example, a pavement). They are connected to a motorway. There is a physical obstruction which prevents connectivity.

Native identifier: `trn-ntwk-pathlink-2`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-pathlink-2)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2025-03-22T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
