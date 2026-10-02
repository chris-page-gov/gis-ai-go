---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Road Link v5",
  "description": "A Road Link is a linear spatial object that defines the geometry and connectivity of a road network between two points in the network. Road Links can represent single carriageways, dual carriageways, slip roads, roundabouts, and indicative trajectories across traffic squares. Road Links will be split for connectivity purposes (for example, at junctions) and Road Nodes will connect the Road Links together. Each Road Link will provide a reference to the Road Nodes at the start and end of the Road Link.",
  "nativeIdentifier": "trn-ntwk-roadlink-5",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5",
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
      "sourcePointer": "/collections/66",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/66",
      "normalisedRecordSha256": "d1fba96baf673cb25e776e8c2b841327e0a69fa60095b1552dc94ebd8d0a2190",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5"
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
    "start": "2025-08-20T00:00:00Z",
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
    "description": "A Road Link is a linear spatial object that defines the geometry and connectivity of a road network between two points in the network. Road Links can represent single carriageways, dual carriageways, slip roads, roundabouts, and indicative trajectories across traffic squares. Road Links will be split for connectivity purposes (for example, at junctions) and Road Nodes will connect the Road Links together. Each Road Link will provide a reference to the Road Nodes at the start and end of the Road Link.",
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
            "2025-08-20T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "trn-ntwk-roadlink-5",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5",
        "rel": "self",
        "title": "The 'Road Link v5' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/items",
        "rel": "items",
        "title": "The features in the 'Road Link v5' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema",
        "rel": "describedby",
        "title": "Schema for the 'Road Link v5' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Road Link v5' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/queryables",
        "properties": {
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
            "format": "uuid",
            "type": [
              "string"
            ]
          },
          "presenceofbuslane_overall_m": {
            "type": [
              "number"
            ]
          },
          "presenceofbuslane_overallpercentage": {
            "type": [
              "integer"
            ]
          },
          "presenceofcyclelane_overall_m": {
            "type": [
              "number"
            ]
          },
          "presenceofcyclelane_overallpercentage": {
            "type": [
              "integer"
            ]
          },
          "presenceofpavement_averagewidth_m": {
            "type": [
              "number"
            ]
          },
          "presenceofpavement_left_m": {
            "type": [
              "number"
            ]
          },
          "presenceofpavement_leftpercentage": {
            "type": [
              "integer"
            ]
          },
          "presenceofpavement_minimumwidth_m": {
            "type": [
              "number"
            ]
          },
          "presenceofpavement_overall_m": {
            "type": [
              "number"
            ]
          },
          "presenceofpavement_overallpercentage": {
            "type": [
              "integer"
            ]
          },
          "presenceofpavement_right_m": {
            "type": [
              "number"
            ]
          },
          "presenceofpavement_rightpercentage": {
            "type": [
              "integer"
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
          "presenceoftram_extentoflink": {
            "enum": [
              "Full Extent",
              "Partial Extent"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "primaryroute": {
            "type": [
              "boolean"
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
              "string"
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
              "boolean"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "784a95ffcb5c3e1c8bf886715f6aefff049ae18dc78dc0cc6cc40ea218e6e3c0",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-ntwk-roadlink-5.0",
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
          "name1_language": {
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
            "type": "string"
          },
          "osid": {
            "format": "uuid",
            "type": "string"
          },
          "presenceofbuslane_capturemethod": {
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
          "presenceofbuslane_evidencedate": {
            "format": "date",
            "type": "string"
          },
          "presenceofbuslane_indirection_m": {
            "type": "number"
          },
          "presenceofbuslane_indirectionpercentage": {
            "type": "integer"
          },
          "presenceofbuslane_inoppositedirection_m": {
            "type": "number"
          },
          "presenceofbuslane_inoppositedirectionpercentage": {
            "type": "integer"
          },
          "presenceofbuslane_overall_m": {
            "type": "number"
          },
          "presenceofbuslane_overallpercentage": {
            "type": "integer"
          },
          "presenceofbuslane_updatedate": {
            "format": "date",
            "type": "string"
          },
          "presenceofcyclelane_capturemethod": {
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
          "presenceofcyclelane_evidencedate": {
            "format": "date",
            "type": "string"
          },
          "presenceofcyclelane_indirection_m": {
            "type": "number"
          },
          "presenceofcyclelane_indirectionpercentage": {
            "type": "integer"
          },
          "presenceofcyclelane_indirectionsegregated_m": {
            "type": "number"
          },
          "presenceofcyclelane_inoppositedirection_m": {
            "type": "number"
          },
          "presenceofcyclelane_inoppositedirectionpercentage": {
            "type": "integer"
          },
          "presenceofcyclelane_inoppositedirectionsegregated_m": {
            "type": "number"
          },
          "presenceofcyclelane_overall_m": {
            "type": "number"
          },
          "presenceofcyclelane_overallpercentage": {
            "type": "integer"
          },
          "presenceofcyclelane_updatedate": {
            "format": "date",
            "type": "string"
          },
          "presenceofpavement_averagewidth_m": {
            "type": "number"
          },
          "presenceofpavement_capturemethod": {
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
          "presenceofpavement_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "presenceofpavement_left_m": {
            "type": "number"
          },
          "presenceofpavement_leftpercentage": {
            "type": "integer"
          },
          "presenceofpavement_minimumwidth_m": {
            "type": "number"
          },
          "presenceofpavement_overall_m": {
            "type": "number"
          },
          "presenceofpavement_overallpercentage": {
            "type": "integer"
          },
          "presenceofpavement_right_m": {
            "type": "number"
          },
          "presenceofpavement_rightpercentage": {
            "type": "integer"
          },
          "presenceofpavement_source": {
            "type": [
              "string",
              "null"
            ]
          },
          "presenceofpavement_updatedate": {
            "format": "date",
            "type": "string"
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
          "presenceoftram_extentoflink": {
            "enum": [
              "Full Extent",
              "Partial Extent"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "presenceoftram_linkdirection": {
            "enum": [
              "Both Directions",
              "In Direction",
              "In Opposite Direction"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "presenceoftram_source": {
            "type": [
              "string",
              "null"
            ]
          },
          "presenceoftram_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "primaryroute": {
            "type": "boolean"
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
            "type": "string"
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
                  "format": "uuid",
                  "maxLength": 36,
                  "originalName": "roadLinkID",
                  "type": "string"
                },
                "roadlinkversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "roadLinkVersionDate",
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
            "type": "boolean"
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
          "roadclassification",
          "routehierarchy",
          "trunkroad",
          "primaryroute",
          "roadclassificationnumber",
          "name1_text",
          "name1_language",
          "name2_text",
          "name2_language",
          "alternatename1_text",
          "alternatename1_language",
          "alternatename2_text",
          "alternatename2_language",
          "operationalstate",
          "directionality",
          "roadstructure",
          "roadwidth_average",
          "roadwidth_minimum",
          "roadwidth_confidencelevel",
          "elevationgain_indirection",
          "elevationgain_againstdirection",
          "heightingmethod",
          "capturespecification",
          "matchstatus",
          "startnode",
          "startgradeseparation",
          "endnode",
          "endgradeseparation",
          "presenceofpavement_overall_m",
          "presenceofpavement_overallpercentage",
          "presenceofpavement_left_m",
          "presenceofpavement_leftpercentage",
          "presenceofpavement_right_m",
          "presenceofpavement_rightpercentage",
          "presenceofpavement_minimumwidth_m",
          "presenceofpavement_averagewidth_m",
          "presenceofpavement_evidencedate",
          "presenceofpavement_updatedate",
          "presenceofpavement_source",
          "presenceofpavement_capturemethod",
          "presenceoftram_extentoflink",
          "presenceoftram_linkdirection",
          "presenceoftram_updatedate",
          "presenceoftram_source",
          "presenceOfstreetlight_coverage",
          "presenceofstreetlight_evidencedate",
          "presenceofstreetlight_updatedate",
          "presenceofstreetlight_capturemethod",
          "presenceofbuslane_overall_m",
          "presenceofbuslane_overallpercentage",
          "presenceofbuslane_indirection_m",
          "presenceofbuslane_indirectionpercentage",
          "presenceofbuslane_inoppositedirection_m",
          "presenceofbuslane_inoppositedirectionpercentage",
          "presenceofbuslane_evidencedate",
          "presenceofbuslane_updatedate",
          "presenceofbuslane_capturemethod",
          "presenceofcyclelane_overall_m",
          "presenceofcyclelane_overallPercentage",
          "presenceofcyclelane_indirection_m",
          "presenceofcyclelane_indirectionsegregated_m",
          "presenceofcyclelane_indirectionpercentage",
          "presenceofcyclelane_inoppositedirection_m",
          "presenceofcyclelane_inoppositedirectionsegregated_m",
          "presenceofcyclelane_inoppositedirectionpercentage",
          "presenceofcyclelane_evidencedate",
          "presenceofcyclelane_updatedate",
          "presenceofcyclelane_capturemethod",
          "roadtrackorpathreference"
        ],
        "requiredUndeclared": [
          "presenceOfstreetlight_coverage",
          "presenceofcyclelane_overallPercentage"
        ],
        "sha256": "7b01fa50a923f9ee00790a08f2f686614fcf2146f2de592d06873f68a9bb30f3",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/7405",
    "title": "Road Link v5"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2025-08-20T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/queryables",
      "responseSha256": "784a95ffcb5c3e1c8bf886715f6aefff049ae18dc78dc0cc6cc40ea218e6e3c0",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema",
      "responseSha256": "7b01fa50a923f9ee00790a08f2f686614fcf2146f2de592d06873f68a9bb30f3",
      "requiredUndeclared": [
        "presenceOfstreetlight_coverage",
        "presenceofcyclelane_overallPercentage"
      ]
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/alternatename1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/alternatename1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/alternatename2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/alternatename2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/capturespecification",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/description",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/directionality",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/elevationgain_againstdirection",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/elevationgain_indirection",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/endgradeseparation",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/endnode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/geometry_length_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/heightingmethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/matchstatus",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/name1_language",
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
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/name1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/name2_language",
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
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/operationalstate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofbuslane_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofbuslane_capturemethod",
      "rdfs:label": "presenceofbuslane_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofbuslane_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofbuslane_evidencedate",
      "rdfs:label": "presenceofbuslane_evidencedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofbuslane_indirection_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofbuslane_indirection_m",
      "rdfs:label": "presenceofbuslane_indirection_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofbuslane_indirectionpercentage",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofbuslane_indirectionpercentage",
      "rdfs:label": "presenceofbuslane_indirectionpercentage",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofbuslane_inoppositedirection_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofbuslane_inoppositedirection_m",
      "rdfs:label": "presenceofbuslane_inoppositedirection_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofbuslane_inoppositedirectionpercentage",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofbuslane_inoppositedirectionpercentage",
      "rdfs:label": "presenceofbuslane_inoppositedirectionpercentage",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofbuslane_overall_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofbuslane_overall_m",
      "rdfs:label": "presenceofbuslane_overall_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofbuslane_overallpercentage",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofbuslane_overallpercentage",
      "rdfs:label": "presenceofbuslane_overallpercentage",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofbuslane_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofbuslane_updatedate",
      "rdfs:label": "presenceofbuslane_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofcyclelane_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofcyclelane_capturemethod",
      "rdfs:label": "presenceofcyclelane_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofcyclelane_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofcyclelane_evidencedate",
      "rdfs:label": "presenceofcyclelane_evidencedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofcyclelane_indirection_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofcyclelane_indirection_m",
      "rdfs:label": "presenceofcyclelane_indirection_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofcyclelane_indirectionpercentage",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofcyclelane_indirectionpercentage",
      "rdfs:label": "presenceofcyclelane_indirectionpercentage",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofcyclelane_indirectionsegregated_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofcyclelane_indirectionsegregated_m",
      "rdfs:label": "presenceofcyclelane_indirectionsegregated_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofcyclelane_inoppositedirection_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofcyclelane_inoppositedirection_m",
      "rdfs:label": "presenceofcyclelane_inoppositedirection_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofcyclelane_inoppositedirectionpercentage",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofcyclelane_inoppositedirectionpercentage",
      "rdfs:label": "presenceofcyclelane_inoppositedirectionpercentage",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofcyclelane_inoppositedirectionsegregated_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofcyclelane_inoppositedirectionsegregated_m",
      "rdfs:label": "presenceofcyclelane_inoppositedirectionsegregated_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofcyclelane_overall_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofcyclelane_overall_m",
      "rdfs:label": "presenceofcyclelane_overall_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofcyclelane_overallpercentage",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofcyclelane_overallpercentage",
      "rdfs:label": "presenceofcyclelane_overallpercentage",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofcyclelane_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofcyclelane_updatedate",
      "rdfs:label": "presenceofcyclelane_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofpavement_averagewidth_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofpavement_averagewidth_m",
      "rdfs:label": "presenceofpavement_averagewidth_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofpavement_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofpavement_capturemethod",
      "rdfs:label": "presenceofpavement_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofpavement_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofpavement_evidencedate",
      "rdfs:label": "presenceofpavement_evidencedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofpavement_left_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofpavement_left_m",
      "rdfs:label": "presenceofpavement_left_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofpavement_leftpercentage",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofpavement_leftpercentage",
      "rdfs:label": "presenceofpavement_leftpercentage",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofpavement_minimumwidth_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofpavement_minimumwidth_m",
      "rdfs:label": "presenceofpavement_minimumwidth_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofpavement_overall_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofpavement_overall_m",
      "rdfs:label": "presenceofpavement_overall_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofpavement_overallpercentage",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofpavement_overallpercentage",
      "rdfs:label": "presenceofpavement_overallpercentage",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofpavement_right_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofpavement_right_m",
      "rdfs:label": "presenceofpavement_right_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofpavement_rightpercentage",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofpavement_rightpercentage",
      "rdfs:label": "presenceofpavement_rightpercentage",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofpavement_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofpavement_source",
      "rdfs:label": "presenceofpavement_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofpavement_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceofpavement_updatedate",
      "rdfs:label": "presenceofpavement_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofstreetlight_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofstreetlight_coverage",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofstreetlight_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceofstreetlight_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceoftram_extentoflink",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceoftram_extentoflink",
      "rdfs:label": "presenceoftram_extentoflink",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Full Extent",
            "Partial Extent"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceoftram_linkdirection",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceoftram_linkdirection",
      "rdfs:label": "presenceoftram_linkdirection",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Both Directions",
            "In Direction",
            "In Opposite Direction"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceoftram_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceoftram_source",
      "rdfs:label": "presenceoftram_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/presenceoftram_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "presenceoftram_updatedate",
      "rdfs:label": "presenceoftram_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/primaryroute",
      "@type": "rdf:Property",
      "dcterms:identifier": "primaryroute",
      "rdfs:label": "primaryroute",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "boolean"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/roadclassification",
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
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/roadclassificationnumber",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/roadstructure",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/roadtrackorpathreference",
      "@type": "rdf:Property",
      "dcterms:identifier": "roadtrackorpathreference",
      "rdfs:label": "roadtrackorpathreference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "roadlinkid": {
                "description": "The identifier of the road link feature.",
                "format": "uuid",
                "maxLength": 36,
                "originalName": "roadLinkID",
                "type": "string"
              },
              "roadlinkversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "roadLinkVersionDate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/roadwidth_average",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/roadwidth_confidencelevel",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/roadwidth_minimum",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/routehierarchy",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/startgradeseparation",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/startnode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/toid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/trunkroad",
      "@type": "rdf:Property",
      "dcterms:identifier": "trunkroad",
      "rdfs:label": "trunkroad",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "boolean"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-roadlink-5/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5/schema"
      }
    }
  ]
}
---

# Road Link v5

A Road Link is a linear spatial object that defines the geometry and connectivity of a road network between two points in the network. Road Links can represent single carriageways, dual carriageways, slip roads, roundabouts, and indicative trajectories across traffic squares. Road Links will be split for connectivity purposes (for example, at junctions) and Road Nodes will connect the Road Links together. Each Road Link will provide a reference to the Road Nodes at the start and end of the Road Link.

Native identifier: `trn-ntwk-roadlink-5`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-roadlink-5)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2025-08-20T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
