---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Road Link v1",
  "description": "A Road Link is a linear spatial object that defines the geometry and connectivity of a road network between two points in the network. Road Links can represent single carriageways, dual carriageways, slip roads, roundabouts, and indicative trajectories across traffic squares. Road Links will be split for connectivity purposes (for example at junctions) and Road Nodes will connect the Road Links together. Each Road Link will provide a reference to the Road Nodes at the start and end of the Road Link.",
  "nativeIdentifier": "trn-ntwk-roadlink-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1",
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
      "sourcePointer": "/collections/62",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/62",
      "normalisedRecordSha256": "71beb51383002f6fb759dfcdba819fe9407592ccf30d8577d3df7de970223721",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1"
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
    "start": "2022-08-23T00:00:00Z",
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
    "description": "A Road Link is a linear spatial object that defines the geometry and connectivity of a road network between two points in the network. Road Links can represent single carriageways, dual carriageways, slip roads, roundabouts, and indicative trajectories across traffic squares. Road Links will be split for connectivity purposes (for example at junctions) and Road Nodes will connect the Road Links together. Each Road Link will provide a reference to the Road Nodes at the start and end of the Road Link.",
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
            "2022-08-23T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "trn-ntwk-roadlink-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1",
        "rel": "self",
        "title": "The 'Road Link v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/items",
        "rel": "items",
        "title": "The features in the 'Road Link v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Road Link v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Road Link v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/queryables",
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
          "geometry_length": {
            "type": [
              "number"
            ]
          },
          "name1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "name2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "operationalstate": {
            "enum": [
              "Addressing Only",
              "Open",
              "Permanently Closed",
              "Prospective",
              "Temporarily Closed",
              "Under Construction"
            ],
            "type": [
              "string"
            ]
          },
          "osid": {
            "type": [
              "string"
            ]
          },
          "primaryroute": {
            "type": [
              "boolean",
              "null"
            ]
          },
          "roadclassification": {
            "enum": [
              "A Road",
              "B Road",
              "Classified Unnumbered",
              "Motorway",
              "Not Classified",
              "Unclassified",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roadclassificationnumber": {
            "type": [
              "string",
              "null"
            ]
          },
          "roadstructure": {
            "enum": [
              "In Tunnel",
              "On Bridge"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roadwidth_average": {
            "type": [
              "number",
              "null"
            ]
          },
          "roadwidth_minimum": {
            "type": [
              "number",
              "null"
            ]
          },
          "routehierarchy": {
            "enum": [
              "A Road",
              "A Road Primary",
              "B Road",
              "B Road Primary",
              "Local Access Road",
              "Local Road",
              "Minor Road",
              "Motorway",
              "Restricted Local Access Road",
              "Restricted Secondary Access Road",
              "Secondary Access Road",
              "Shared Use Road"
            ],
            "type": [
              "string"
            ]
          },
          "toid": {
            "type": [
              "string",
              "null"
            ]
          },
          "trunkroad": {
            "type": [
              "boolean",
              "null"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "a299880f2183220a7fde82149a2f7d81f6a8cb80bbf91548f37733534d3e0a80",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-ntwk-roadlink-1.0",
        "properties": {
          "alternatename1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
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
            "type": "string"
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
          "directionality": {
            "enum": [
              "Both Directions",
              "In Direction",
              "In Opposite Direction"
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
            "type": [
              "integer",
              "null"
            ]
          },
          "endnode": {
            "type": "string"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/LineString.json"
          },
          "geometry_length": {
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
          "name1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "name1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "name2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "name2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "operationalstate": {
            "enum": [
              "Addressing Only",
              "Open",
              "Permanently Closed",
              "Prospective",
              "Temporarily Closed",
              "Under Construction"
            ],
            "type": "string"
          },
          "osid": {
            "type": "string"
          },
          "primaryroute": {
            "type": [
              "boolean",
              "null"
            ]
          },
          "roadclassification": {
            "enum": [
              "A Road",
              "B Road",
              "Classified Unnumbered",
              "Motorway",
              "Not Classified",
              "Unclassified",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roadclassificationnumber": {
            "type": [
              "string",
              "null"
            ]
          },
          "roadstructure": {
            "enum": [
              "In Tunnel",
              "On Bridge"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roadtrackorpathreference": {
            "items": {
              "properties": {
                "roadlinkid": {
                  "description": "The identifier of the road link feature.",
                  "maxLength": 36,
                  "originalName": "roadLinkID",
                  "type": "string"
                },
                "roadlinkversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "roadLinkVersionDate",
                  "pattern": "YYYY-MM-DD",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "roadtrackorpathid": {
                  "description": "The identifier of the road track or path feature.",
                  "maxLength": 36,
                  "originalName": "roadTrackOrPathID",
                  "type": "string"
                }
              },
              "type": "object"
            },
            "type": "array"
          },
          "roadwidth_average": {
            "type": [
              "number",
              "null"
            ]
          },
          "roadwidth_confidencelevel": {
            "enum": [
              "OS Moorland And Full Extent",
              "OS Moorland And Part Extent",
              "OS Rural And Full Extent",
              "OS Rural And Part Extent",
              "OS Urban And Full Extent",
              "OS Urban And Part Extent"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roadwidth_minimum": {
            "type": [
              "number",
              "null"
            ]
          },
          "routehierarchy": {
            "enum": [
              "A Road",
              "A Road Primary",
              "B Road",
              "B Road Primary",
              "Local Access Road",
              "Local Road",
              "Minor Road",
              "Motorway",
              "Restricted Local Access Road",
              "Restricted Secondary Access Road",
              "Secondary Access Road",
              "Shared Use Road"
            ],
            "type": "string"
          },
          "startgradeseparation": {
            "type": [
              "integer",
              "null"
            ]
          },
          "startnode": {
            "type": "string"
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
          "trunkroad": {
            "type": [
              "boolean",
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
          "capturespecification",
          "changetype",
          "description",
          "directionality",
          "elevationgain_againstdirection",
          "elevationgain_indirection",
          "endnode",
          "geometry",
          "geometry_length",
          "heightingmethod",
          "matchstatus",
          "operationalstate",
          "osid",
          "roadclassification",
          "routehierarchy",
          "startnode",
          "theme",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "a1a4b4952a34bff9528a06caaab2bf060c60ad34788b9af507d71c2324e965d0",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/7405",
    "title": "Road Link v1"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2022-08-23T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/queryables",
      "responseSha256": "a299880f2183220a7fde82149a2f7d81f6a8cb80bbf91548f37733534d3e0a80",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema",
      "responseSha256": "a1a4b4952a34bff9528a06caaab2bf060c60ad34788b9af507d71c2324e965d0",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/alternatename1_language",
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
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/alternatename1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/alternatename2_language",
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
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/alternatename2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/capturespecification",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/cyclefacility",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/cyclefacility_wholelink",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/description",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/directionality",
      "@type": "rdf:Property",
      "dcterms:identifier": "directionality",
      "rdfs:label": "directionality",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Both Directions",
            "In Direction",
            "In Opposite Direction"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/elevationgain_againstdirection",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/elevationgain_indirection",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/endgradeseparation",
      "@type": "rdf:Property",
      "dcterms:identifier": "endgradeseparation",
      "rdfs:label": "endgradeseparation",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "integer",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/endnode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/geometry",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry",
      "rdfs:label": "geometry",
      "okfp:schemaDefinition": {
        "@value": {
          "$ref": "https://geojson.org/schema/LineString.json"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/geometry_length",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/heightingmethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/matchstatus",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/name1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "name1_language",
      "rdfs:label": "name1_language",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "eng",
            "gla",
            "cym"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/name1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "name1_text",
      "rdfs:label": "name1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/name2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "name2_language",
      "rdfs:label": "name2_language",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "eng",
            "gla",
            "cym"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/name2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "name2_text",
      "rdfs:label": "name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/operationalstate",
      "@type": "rdf:Property",
      "dcterms:identifier": "operationalstate",
      "rdfs:label": "operationalstate",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Addressing Only",
            "Open",
            "Permanently Closed",
            "Prospective",
            "Temporarily Closed",
            "Under Construction"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/primaryroute",
      "@type": "rdf:Property",
      "dcterms:identifier": "primaryroute",
      "rdfs:label": "primaryroute",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/roadclassification",
      "@type": "rdf:Property",
      "dcterms:identifier": "roadclassification",
      "rdfs:label": "roadclassification",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "A Road",
            "B Road",
            "Classified Unnumbered",
            "Motorway",
            "Not Classified",
            "Unclassified",
            "Unknown"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/roadclassificationnumber",
      "@type": "rdf:Property",
      "dcterms:identifier": "roadclassificationnumber",
      "rdfs:label": "roadclassificationnumber",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/roadstructure",
      "@type": "rdf:Property",
      "dcterms:identifier": "roadstructure",
      "rdfs:label": "roadstructure",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "In Tunnel",
            "On Bridge"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/roadtrackorpathreference",
      "@type": "rdf:Property",
      "dcterms:identifier": "roadtrackorpathreference",
      "rdfs:label": "roadtrackorpathreference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "roadlinkid": {
                "description": "The identifier of the road link feature.",
                "maxLength": 36,
                "originalName": "roadLinkID",
                "type": "string"
              },
              "roadlinkversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "roadLinkVersionDate",
                "pattern": "YYYY-MM-DD",
                "type": [
                  "string",
                  "null"
                ]
              },
              "roadtrackorpathid": {
                "description": "The identifier of the road track or path feature.",
                "maxLength": 36,
                "originalName": "roadTrackOrPathID",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/roadwidth_average",
      "@type": "rdf:Property",
      "dcterms:identifier": "roadwidth_average",
      "rdfs:label": "roadwidth_average",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "number",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/roadwidth_confidencelevel",
      "@type": "rdf:Property",
      "dcterms:identifier": "roadwidth_confidencelevel",
      "rdfs:label": "roadwidth_confidencelevel",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "OS Moorland And Full Extent",
            "OS Moorland And Part Extent",
            "OS Rural And Full Extent",
            "OS Rural And Part Extent",
            "OS Urban And Full Extent",
            "OS Urban And Part Extent"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/roadwidth_minimum",
      "@type": "rdf:Property",
      "dcterms:identifier": "roadwidth_minimum",
      "rdfs:label": "roadwidth_minimum",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "number",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/routehierarchy",
      "@type": "rdf:Property",
      "dcterms:identifier": "routehierarchy",
      "rdfs:label": "routehierarchy",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "A Road",
            "A Road Primary",
            "B Road",
            "B Road Primary",
            "Local Access Road",
            "Local Road",
            "Minor Road",
            "Motorway",
            "Restricted Local Access Road",
            "Restricted Secondary Access Road",
            "Secondary Access Road",
            "Shared Use Road"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/startgradeseparation",
      "@type": "rdf:Property",
      "dcterms:identifier": "startgradeseparation",
      "rdfs:label": "startgradeseparation",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "integer",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/startnode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/toid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/trunkroad",
      "@type": "rdf:Property",
      "dcterms:identifier": "trunkroad",
      "rdfs:label": "trunkroad",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1/schema"
      }
    }
  ]
}
---

# Road Link v1

A Road Link is a linear spatial object that defines the geometry and connectivity of a road network between two points in the network. Road Links can represent single carriageways, dual carriageways, slip roads, roundabouts, and indicative trajectories across traffic squares. Road Links will be split for connectivity purposes (for example at junctions) and Road Nodes will connect the Road Links together. Each Road Link will provide a reference to the Road Nodes at the start and end of the Road Link.

Native identifier: `trn-ntwk-roadlink-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2022-08-23T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
