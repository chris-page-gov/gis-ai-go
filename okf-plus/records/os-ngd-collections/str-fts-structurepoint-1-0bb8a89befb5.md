---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Structure Point v1",
  "description": "Feature which has a point geometry and represents a freestanding manmade construction that is not a building and is less than 4m square but is considered to be of sufficient interest to be captured. Examples include a statue, a telephone call box, and a post box.",
  "nativeIdentifier": "str-fts-structurepoint-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "OS NGD",
    "str",
    "schema",
    "queryables"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections",
      "retrievedAt": "2026-10-02T01:18:50.822323Z",
      "responseSha256": "cf6f9c7670533ff42c64af98a8f7bb8aa60911463d937623a4fc6f5bb8767de9",
      "sourcePointer": "/collections/34",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/34",
      "normalisedRecordSha256": "cf8c1ddde841e681cc8843d165246ceb4ef10d6ffb2b5c041a9c4b291dafb378",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1"
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
    "start": "2022-08-27T00:00:00Z",
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
    "description": "Feature which has a point geometry and represents a freestanding manmade construction that is not a building and is less than 4m square but is considered to be of sufficient interest to be captured. Examples include a statue, a telephone call box, and a post box.",
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
            "2022-08-27T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "str-fts-structurepoint-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1",
        "rel": "self",
        "title": "The 'Structure Point v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/items",
        "rel": "items",
        "title": "The features in the 'Structure Point v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Structure Point v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Structure Point v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/queryables",
        "properties": {
          "description": {
            "enum": [
              "Air Quality Monitoring Station",
              "Aircraft Landing Light",
              "Aircraft Navigation Beacon",
              "Aircraft Navigation Tower",
              "Anchor",
              "Anchorage Post",
              "Anemometer",
              "Arch",
              "Bell",
              "Bell Pit",
              "Bell Tower",
              "Bore Hole",
              "Boundary Marker",
              "Broch",
              "Burial Chamber",
              "Burnt Mound",
              "Butt",
              "Cable Terminal Station",
              "Cairn",
              "Cairn And Memorial",
              "Cairn And Shelter",
              "Capstan",
              "Cell",
              "Chamber",
              "Chambered Cairn",
              "Chimney",
              "Cleit",
              "Cist",
              "Clock",
              "Clock Tower",
              "Column",
              "Crane",
              "Crannog",
              "Cross",
              "Cross Base",
              "Dene-hole",
              "Distance Marker",
              "Dolphin",
              "Dovecot",
              "Dry Weir",
              "Dun",
              "Electricity Sub Station",
              "Electricity Support Pole",
              "Electricity Support Poles",
              "Emergency Assistance Or Equipment Point",
              "Emergency Telephone In Call Box",
              "Emergency Telephone On Post",
              "Fish Trap",
              "Fishing Platform",
              "Fixed Structure",
              "Flagstaff",
              "Flare Stack",
              "Floating Structure",
              "Fog Horn",
              "Folly",
              "Font",
              "Fountain",
              "Gallows",
              "Gas Governor",
              "Gibbet Post",
              "Grave",
              "Gravestone",
              "Guide Post",
              "Guide Stone",
              "Gun",
              "Henge",
              "Hide",
              "Hoist",
              "Hut",
              "Hydraulic Ram",
              "Kiln",
              "Lattice Tower",
              "Light",
              "Lighting Pole Or Tower",
              "Loading Gauge",
              "Mail Pick Up Post",
              "Manhole",
              "Marker Post Or Stone",
              "Mast",
              "Maypole",
              "Memorial",
              "Memorial Fountain",
              "Memorial Stone",
              "Meteorological Station",
              "Meteorological Tower",
              "Mile Stone",
              "Mine Shaft",
              "Mooring Post",
              "Mound Of Earth",
              "Nautical Beacon",
              "Nautical Daymark",
              "Nautical Daymark And Light",
              "Nautical Light",
              "Nautical Mark",
              "Nautical Perch",
              "Nautical Radar Reflector",
              "Obelisk",
              "Observation Point",
              "Observation Telescope",
              "Observation Tower",
              "Open Kiln",
              "Open Well",
              "Ornamental Arch",
              "Ornamental Structure",
              "Other Support Pole",
              "Other Support Poles",
              "Outfall",
              "Pillar",
              "Plinth",
              "Pole",
              "Post",
              "Post Box",
              "Post Box And Guide Post",
              "Post Restricting Vehicular Access",
              "Postal Delivery Box",
              "Pump",
              "Pump And Memorial",
              "Pump And Well",
              "Radar",
              "Radar Mast",
              "Radar Tower",
              "Radio Telescope",
              "Rail Distance Marker",
              "Rail Signal Light",
              "Rail Signal Post",
              "Rail Signal Tower",
              "Reflector",
              "Remains Of Cairn",
              "Remains Of Chambered Cairn",
              "Remains Of Cross",
              "Rising Bollard",
              "Road Mile Post",
              "Road Mile Stone",
              "Rock",
              "Rock Shelter",
              "Roofed Hopper",
              "Roofed Telescope",
              "Roofed Tower",
              "Roofed Well",
              "Ruined Structure",
              "Ruined Tower",
              "Ruined Windmill",
              "Satellite Dish",
              "Seat",
              "Shaft",
              "Sheep Dip",
              "Shieling",
              "Shooting Tower",
              "Shrine",
              "Signal Staff",
              "Siren",
              "Sluice Gate",
              "Solar Panel",
              "Speakers Platform",
              "Spring",
              "Standing Stone",
              "Statue",
              "Stepping Stone",
              "Stocks",
              "Stone",
              "Structure",
              "Sundial",
              "Target",
              "Telecommunications Lattice Tower",
              "Telecommunications Mast",
              "Telephone Call Box",
              "Telephone Call Box And Defibrillator",
              "Telephone Call Post",
              "Telephone In Wall",
              "Tide Gauge",
              "Tomb",
              "Tombstone",
              "Tower",
              "Ventilation Shaft",
              "Viewpoint Guide",
              "War Memorial",
              "Warning Marker",
              "Warning Sign",
              "Water Monitoring Device",
              "Water Point",
              "Water Pumping Chamber",
              "Water Tank",
              "Water Tower",
              "Weir",
              "Well",
              "Well As Spring",
              "Whipping Post",
              "Winch",
              "Wind Pump",
              "Wind Sock",
              "Wind Turbine"
            ],
            "type": [
              "string"
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
          "operationalstatus": {
            "enum": [
              "Active",
              "Inactive",
              "Unknown"
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
          "toid": {
            "type": [
              "string",
              "null"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "5fdc289308b28c6116effef17f4a854029a26eb4f224ca704479a641fc2c33dc",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "str-fts-structurepoint-1.0",
        "properties": {
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
              "Air Quality Monitoring Station",
              "Aircraft Landing Light",
              "Aircraft Navigation Beacon",
              "Aircraft Navigation Tower",
              "Anchor",
              "Anchorage Post",
              "Anemometer",
              "Arch",
              "Bell",
              "Bell Pit",
              "Bell Tower",
              "Bore Hole",
              "Boundary Marker",
              "Broch",
              "Burial Chamber",
              "Burnt Mound",
              "Butt",
              "Cable Terminal Station",
              "Cairn",
              "Cairn And Memorial",
              "Cairn And Shelter",
              "Capstan",
              "Cell",
              "Chamber",
              "Chambered Cairn",
              "Chimney",
              "Cleit",
              "Cist",
              "Clock",
              "Clock Tower",
              "Column",
              "Crane",
              "Crannog",
              "Cross",
              "Cross Base",
              "Dene-hole",
              "Distance Marker",
              "Dolphin",
              "Dovecot",
              "Dry Weir",
              "Dun",
              "Electricity Sub Station",
              "Electricity Support Pole",
              "Electricity Support Poles",
              "Emergency Assistance Or Equipment Point",
              "Emergency Telephone In Call Box",
              "Emergency Telephone On Post",
              "Fish Trap",
              "Fishing Platform",
              "Fixed Structure",
              "Flagstaff",
              "Flare Stack",
              "Floating Structure",
              "Fog Horn",
              "Folly",
              "Font",
              "Fountain",
              "Gallows",
              "Gas Governor",
              "Gibbet Post",
              "Grave",
              "Gravestone",
              "Guide Post",
              "Guide Stone",
              "Gun",
              "Henge",
              "Hide",
              "Hoist",
              "Hut",
              "Hydraulic Ram",
              "Kiln",
              "Lattice Tower",
              "Light",
              "Lighting Pole Or Tower",
              "Loading Gauge",
              "Mail Pick Up Post",
              "Manhole",
              "Marker Post Or Stone",
              "Mast",
              "Maypole",
              "Memorial",
              "Memorial Fountain",
              "Memorial Stone",
              "Meteorological Station",
              "Meteorological Tower",
              "Mile Stone",
              "Mine Shaft",
              "Mooring Post",
              "Mound Of Earth",
              "Nautical Beacon",
              "Nautical Daymark",
              "Nautical Daymark And Light",
              "Nautical Light",
              "Nautical Mark",
              "Nautical Perch",
              "Nautical Radar Reflector",
              "Obelisk",
              "Observation Point",
              "Observation Telescope",
              "Observation Tower",
              "Open Kiln",
              "Open Well",
              "Ornamental Arch",
              "Ornamental Structure",
              "Other Support Pole",
              "Other Support Poles",
              "Outfall",
              "Pillar",
              "Plinth",
              "Pole",
              "Post",
              "Post Box",
              "Post Box And Guide Post",
              "Post Restricting Vehicular Access",
              "Postal Delivery Box",
              "Pump",
              "Pump And Memorial",
              "Pump And Well",
              "Radar",
              "Radar Mast",
              "Radar Tower",
              "Radio Telescope",
              "Rail Distance Marker",
              "Rail Signal Light",
              "Rail Signal Post",
              "Rail Signal Tower",
              "Reflector",
              "Remains Of Cairn",
              "Remains Of Chambered Cairn",
              "Remains Of Cross",
              "Rising Bollard",
              "Road Mile Post",
              "Road Mile Stone",
              "Rock",
              "Rock Shelter",
              "Roofed Hopper",
              "Roofed Telescope",
              "Roofed Tower",
              "Roofed Well",
              "Ruined Structure",
              "Ruined Tower",
              "Ruined Windmill",
              "Satellite Dish",
              "Seat",
              "Shaft",
              "Sheep Dip",
              "Shieling",
              "Shooting Tower",
              "Shrine",
              "Signal Staff",
              "Siren",
              "Sluice Gate",
              "Solar Panel",
              "Speakers Platform",
              "Spring",
              "Standing Stone",
              "Statue",
              "Stepping Stone",
              "Stocks",
              "Stone",
              "Structure",
              "Sundial",
              "Target",
              "Telecommunications Lattice Tower",
              "Telecommunications Mast",
              "Telephone Call Box",
              "Telephone Call Box And Defibrillator",
              "Telephone Call Post",
              "Telephone In Wall",
              "Tide Gauge",
              "Tomb",
              "Tombstone",
              "Tower",
              "Ventilation Shaft",
              "Viewpoint Guide",
              "War Memorial",
              "Warning Marker",
              "Warning Sign",
              "Water Monitoring Device",
              "Water Point",
              "Water Pumping Chamber",
              "Water Tank",
              "Water Tower",
              "Weir",
              "Well",
              "Well As Spring",
              "Whipping Post",
              "Winch",
              "Wind Pump",
              "Wind Sock",
              "Wind Turbine"
            ],
            "type": "string"
          },
          "description_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "description_source": {
            "type": [
              "string",
              "null"
            ]
          },
          "description_updatedate": {
            "format": "date",
            "type": "string"
          },
          "firstdigitalcapturedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/MultiPoint.json"
          },
          "geometry_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "geometry_source": {
            "type": [
              "string",
              "null"
            ]
          },
          "geometry_updatedate": {
            "format": "date",
            "type": "string"
          },
          "ishistoric": {
            "type": "boolean"
          },
          "isobscured": {
            "type": "boolean"
          },
          "name1_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "name1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "name1_source": {
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
          "name1_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "name2_evidencedate": {
            "format": "date",
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
          "name2_source": {
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
          "name2_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "operationalstatus": {
            "enum": [
              "Active",
              "Inactive",
              "Unknown"
            ],
            "type": "string"
          },
          "osid": {
            "type": "string"
          },
          "physicallevel": {
            "enum": [
              "Level 1",
              "Level 2",
              "Level 3",
              "Overhead",
              "Surface Level",
              "Underground"
            ],
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
          "description_updatedate",
          "geometry",
          "geometry_updatedate",
          "ishistoric",
          "isobscured",
          "osid",
          "physicallevel",
          "theme",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "9f4b0209d1d324f774df3c6bcc5042d3952d4769407473e775c79e9ebbae2609",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Structure Point v1"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2022-08-27T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/queryables",
      "responseSha256": "5fdc289308b28c6116effef17f4a854029a26eb4f224ca704479a641fc2c33dc",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema",
      "responseSha256": "9f4b0209d1d324f774df3c6bcc5042d3952d4769407473e775c79e9ebbae2609",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/capturespecification",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Air Quality Monitoring Station",
            "Aircraft Landing Light",
            "Aircraft Navigation Beacon",
            "Aircraft Navigation Tower",
            "Anchor",
            "Anchorage Post",
            "Anemometer",
            "Arch",
            "Bell",
            "Bell Pit",
            "Bell Tower",
            "Bore Hole",
            "Boundary Marker",
            "Broch",
            "Burial Chamber",
            "Burnt Mound",
            "Butt",
            "Cable Terminal Station",
            "Cairn",
            "Cairn And Memorial",
            "Cairn And Shelter",
            "Capstan",
            "Cell",
            "Chamber",
            "Chambered Cairn",
            "Chimney",
            "Cleit",
            "Cist",
            "Clock",
            "Clock Tower",
            "Column",
            "Crane",
            "Crannog",
            "Cross",
            "Cross Base",
            "Dene-hole",
            "Distance Marker",
            "Dolphin",
            "Dovecot",
            "Dry Weir",
            "Dun",
            "Electricity Sub Station",
            "Electricity Support Pole",
            "Electricity Support Poles",
            "Emergency Assistance Or Equipment Point",
            "Emergency Telephone In Call Box",
            "Emergency Telephone On Post",
            "Fish Trap",
            "Fishing Platform",
            "Fixed Structure",
            "Flagstaff",
            "Flare Stack",
            "Floating Structure",
            "Fog Horn",
            "Folly",
            "Font",
            "Fountain",
            "Gallows",
            "Gas Governor",
            "Gibbet Post",
            "Grave",
            "Gravestone",
            "Guide Post",
            "Guide Stone",
            "Gun",
            "Henge",
            "Hide",
            "Hoist",
            "Hut",
            "Hydraulic Ram",
            "Kiln",
            "Lattice Tower",
            "Light",
            "Lighting Pole Or Tower",
            "Loading Gauge",
            "Mail Pick Up Post",
            "Manhole",
            "Marker Post Or Stone",
            "Mast",
            "Maypole",
            "Memorial",
            "Memorial Fountain",
            "Memorial Stone",
            "Meteorological Station",
            "Meteorological Tower",
            "Mile Stone",
            "Mine Shaft",
            "Mooring Post",
            "Mound Of Earth",
            "Nautical Beacon",
            "Nautical Daymark",
            "Nautical Daymark And Light",
            "Nautical Light",
            "Nautical Mark",
            "Nautical Perch",
            "Nautical Radar Reflector",
            "Obelisk",
            "Observation Point",
            "Observation Telescope",
            "Observation Tower",
            "Open Kiln",
            "Open Well",
            "Ornamental Arch",
            "Ornamental Structure",
            "Other Support Pole",
            "Other Support Poles",
            "Outfall",
            "Pillar",
            "Plinth",
            "Pole",
            "Post",
            "Post Box",
            "Post Box And Guide Post",
            "Post Restricting Vehicular Access",
            "Postal Delivery Box",
            "Pump",
            "Pump And Memorial",
            "Pump And Well",
            "Radar",
            "Radar Mast",
            "Radar Tower",
            "Radio Telescope",
            "Rail Distance Marker",
            "Rail Signal Light",
            "Rail Signal Post",
            "Rail Signal Tower",
            "Reflector",
            "Remains Of Cairn",
            "Remains Of Chambered Cairn",
            "Remains Of Cross",
            "Rising Bollard",
            "Road Mile Post",
            "Road Mile Stone",
            "Rock",
            "Rock Shelter",
            "Roofed Hopper",
            "Roofed Telescope",
            "Roofed Tower",
            "Roofed Well",
            "Ruined Structure",
            "Ruined Tower",
            "Ruined Windmill",
            "Satellite Dish",
            "Seat",
            "Shaft",
            "Sheep Dip",
            "Shieling",
            "Shooting Tower",
            "Shrine",
            "Signal Staff",
            "Siren",
            "Sluice Gate",
            "Solar Panel",
            "Speakers Platform",
            "Spring",
            "Standing Stone",
            "Statue",
            "Stepping Stone",
            "Stocks",
            "Stone",
            "Structure",
            "Sundial",
            "Target",
            "Telecommunications Lattice Tower",
            "Telecommunications Mast",
            "Telephone Call Box",
            "Telephone Call Box And Defibrillator",
            "Telephone Call Post",
            "Telephone In Wall",
            "Tide Gauge",
            "Tomb",
            "Tombstone",
            "Tower",
            "Ventilation Shaft",
            "Viewpoint Guide",
            "War Memorial",
            "Warning Marker",
            "Warning Sign",
            "Water Monitoring Device",
            "Water Point",
            "Water Pumping Chamber",
            "Water Tank",
            "Water Tower",
            "Weir",
            "Well",
            "Well As Spring",
            "Whipping Post",
            "Winch",
            "Wind Pump",
            "Wind Sock",
            "Wind Turbine"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/description_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "description_evidencedate",
      "rdfs:label": "description_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/description_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "description_source",
      "rdfs:label": "description_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/description_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "description_updatedate",
      "rdfs:label": "description_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/firstdigitalcapturedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "firstdigitalcapturedate",
      "rdfs:label": "firstdigitalcapturedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/geometry",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry",
      "rdfs:label": "geometry",
      "okfp:schemaDefinition": {
        "@value": {
          "$ref": "https://geojson.org/schema/MultiPoint.json"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/geometry_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry_evidencedate",
      "rdfs:label": "geometry_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/geometry_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry_source",
      "rdfs:label": "geometry_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/geometry_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry_updatedate",
      "rdfs:label": "geometry_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/ishistoric",
      "@type": "rdf:Property",
      "dcterms:identifier": "ishistoric",
      "rdfs:label": "ishistoric",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "boolean"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/isobscured",
      "@type": "rdf:Property",
      "dcterms:identifier": "isobscured",
      "rdfs:label": "isobscured",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "boolean"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/name1_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "name1_evidencedate",
      "rdfs:label": "name1_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/name1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/name1_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "name1_source",
      "rdfs:label": "name1_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/name1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/name1_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "name1_updatedate",
      "rdfs:label": "name1_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/name2_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "name2_evidencedate",
      "rdfs:label": "name2_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/name2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/name2_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "name2_source",
      "rdfs:label": "name2_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/name2_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "name2_updatedate",
      "rdfs:label": "name2_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/operationalstatus",
      "@type": "rdf:Property",
      "dcterms:identifier": "operationalstatus",
      "rdfs:label": "operationalstatus",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Active",
            "Inactive",
            "Unknown"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/physicallevel",
      "@type": "rdf:Property",
      "dcterms:identifier": "physicallevel",
      "rdfs:label": "physicallevel",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Level 1",
            "Level 2",
            "Level 3",
            "Overhead",
            "Surface Level",
            "Underground"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/toid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structurepoint-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1/schema"
      }
    }
  ]
}
---

# Structure Point v1

Feature which has a point geometry and represents a freestanding manmade construction that is not a building and is less than 4m square but is considered to be of sufficient interest to be captured. Examples include a statue, a telephone call box, and a post box.

Native identifier: `str-fts-structurepoint-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structurepoint-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2022-08-27T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
