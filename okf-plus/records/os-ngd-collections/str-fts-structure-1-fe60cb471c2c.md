---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Structure v1",
  "description": "Polygon feature representing a manmade construction that is not a building. Examples include a mast, a chimney, and a crane.",
  "nativeIdentifier": "str-fts-structure-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1",
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
      "sourcePointer": "/collections/30",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/30",
      "normalisedRecordSha256": "1b5dba2861e2129ba41b76097922d1e7a6656144d69a7e2ff173ef356a11e3b9",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1"
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
    "description": "Polygon feature representing a manmade construction that is not a building. Examples include a mast, a chimney, and a crane.",
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
    "id": "str-fts-structure-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1",
        "rel": "self",
        "title": "The 'Structure v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/items",
        "rel": "items",
        "title": "The features in the 'Structure v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Structure v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Structure v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/queryables",
        "properties": {
          "absoluteheightmaximum": {
            "type": [
              "number",
              "null"
            ]
          },
          "absoluteheightminimum": {
            "type": [
              "number",
              "null"
            ]
          },
          "absoluteheightroofbase": {
            "type": [
              "number",
              "null"
            ]
          },
          "description": {
            "enum": [
              "Cleit",
              "Air Traffic Control Tower",
              "Aircraft Landing Light",
              "Aircraft Navigation Beacon",
              "Arch",
              "Bandstand",
              "Bell",
              "Bell And Light",
              "Bell Tower",
              "Boat Rollers",
              "Boom",
              "Boulder Structure",
              "Boulders",
              "Boundary Marker",
              "Broch",
              "Burial Chamber",
              "Buried Covered Reservoir",
              "Buried Open Reservoir",
              "Buried Open Storage Tank",
              "Buried Storage Tank",
              "Butt",
              "Cable Gantry",
              "Cairn",
              "Caisson",
              "Cannon",
              "Capstan",
              "Chamber",
              "Chambered Cairn",
              "Chimney",
              "Clock",
              "Clock Tower",
              "Conveyor",
              "Cooling Tower",
              "Crane",
              "Crane On Gantry",
              "Cross",
              "Cross And Fixed Structure",
              "Cross Base",
              "Cross Slab",
              "Daymark",
              "Daymark and Light",
              "Diving Platform",
              "Dolphin",
              "Double Wall",
              "Dovecot",
              "Dry Open Tank Reservoir",
              "Dry Reservoir",
              "Dry Weir",
              "Electricity Metal Monopole",
              "Electricity Pylon",
              "Empty Dew Pond",
              "Escalator",
              "Fish Ladder",
              "Fish Trap",
              "Fishing Platform",
              "Fixed Structure",
              "Flare Stack",
              "Floating Crane",
              "Floating Structure",
              "Floating Structure With Light",
              "Flood Controlling Wall",
              "Flood Or Water Controlling Wall",
              "Flue",
              "Fog Bell",
              "Fog Horn",
              "Fog Light",
              "Fountain",
              "Gantry",
              "Gas Holder",
              "Gateway",
              "Gazebo",
              "Glasshouse",
              "Grandstand",
              "Gravestone",
              "Grid",
              "Groyne",
              "Guide Stone",
              "Guide Stone As Boundary Marker",
              "Henge",
              "Hide",
              "Historic Battery",
              "Historic Vessel",
              "Hoist",
              "Holed Stone",
              "Hopper",
              "Hydraulic Ram",
              "Inscribed Rock",
              "Kiln",
              "Lattice Tower",
              "Leat",
              "Lighthouse",
              "Lighting Tower",
              "Lock",
              "Lock Gate",
              "Made Sealed Surface Covered with Solar Panels",
              "Made Unsealed Surface Covered with Solar Panels",
              "Marked Rock",
              "Marked Stone",
              "Market Cross",
              "Mast",
              "Maze",
              "Memorial Wall",
              "Meteorological Station",
              "Mine Shaft",
              "Motor Vehicle Weighbridge",
              "Mound Of Earth",
              "Moveable Glasshouse",
              "Moveable Structure",
              "Navigation Tower",
              "Obelisk",
              "Observation Platform",
              "Open Sludge Tank",
              "Open Slurry Storage Tank",
              "Open Storage Tank",
              "Ornamental Structure",
              "Outfall",
              "Overflow",
              "Paddling Pool",
              "Partially Buried Reservoir",
              "Partially Buried Slurry Storage Tank",
              "Partially Buried Storage Tank",
              "Path On Lock Gate",
              "Pillar",
              "Pipe Bridge",
              "Pipeline",
              "Plinth",
              "Post",
              "Post And Stone",
              "Pump",
              "Pump Waste Water",
              "Pump Water Controlling",
              "Pump Water Distribution",
              "Radar Tower",
              "Radio Telescope",
              "Rail Gantry",
              "Rail Signal Gantry",
              "Rail Signal Light",
              "Rail Vehicle Weighbridge",
              "Remains Of Cairn",
              "Remains Of Chambered Cairn",
              "Remains Of Cross",
              "Retaining Wall",
              "Road Gantry",
              "Rock Shelter",
              "Roofed Conveyor",
              "Roofed Fish Trap",
              "Roofed Hopper",
              "Roofed Reservoir",
              "Roofed Rowing Tank",
              "Roofed Sludge Tank",
              "Roofed Slurry Storage Tank",
              "Roofed Storage Tank",
              "Roofed Telescope",
              "Ruined Structure",
              "Ruined Supported Structure",
              "Ruined Tower",
              "Ruined Windmill",
              "Satellite Dish",
              "Sea Wall",
              "Seat",
              "Seat On Supported Structure",
              "Shaft",
              "Shelter",
              "Shooting Tower",
              "Signal Light As Boundary Marker",
              "Silo",
              "Siren",
              "Slipway",
              "Sloping Masonry",
              "Solar Panels",
              "Solar Panels On Bare Earth Or Grass",
              "Source Of Watercourse",
              "Speakers Platform",
              "Spring",
              "Stand",
              "Standing Stone",
              "Statue",
              "Steps",
              "Stone",
              "Stone Pillar",
              "Supported Conveyor",
              "Supported Flue Pipe",
              "Supported Structure",
              "Surge Shaft",
              "Swimming Platform",
              "Swimming Pool",
              "Target",
              "Telecommunications Mast",
              "Telecommunications Tower",
              "Terraces",
              "Tide Gauge",
              "Toboggan Run",
              "Tomb",
              "Tower",
              "Travelling Conveyor",
              "Travelling Crane",
              "Travelling Radio Telescope",
              "Travelling Structure",
              "Trough",
              "Upper Level Of Communication",
              "Vehicle Dip",
              "Ventilation Shaft",
              "War Memorial",
              "War Memorial Wall",
              "Warning Light",
              "Warning Sign And Stone",
              "Water Controlling Wall",
              "Water Point",
              "Water Storage Tank On Tower",
              "Water Tower",
              "Waterwheel",
              "Weir",
              "Well",
              "Well As Spring",
              "Wind Pump",
              "Wind Turbine"
            ],
            "type": [
              "string"
            ]
          },
          "geometry_area": {
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
          "oslandcovertiera": {
            "enum": [
              "Constructed",
              "Made",
              "Mineral",
              "Open Vegetation",
              "Structure",
              "Trees",
              "Water"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "oslandcovertierb": {
            "items": {
              "enum": [
                "Bare Earth Or Grass",
                "Boulder Structure",
                "Boulders",
                "Coniferous Trees",
                "Heath",
                "Inland Water",
                "Inter Tidal",
                "Made Sealed",
                "Made Unknown",
                "Made Unsealed",
                "Maze",
                "Mixed Trees",
                "Non-Coniferous Trees",
                "Rough Grassland",
                "Scrub",
                "Solar Panels",
                "Structure",
                "Travelling Crane",
                "Tidal Water"
              ],
              "enumeration": true,
              "maxLength": 100,
              "type": [
                "string",
                "null"
              ]
            },
            "type": [
              "array"
            ]
          },
          "oslandusetiera": {
            "enum": [
              "Agriculture Or Aquaculture",
              "Attraction Or Activity",
              "Commercial Activity: Animal Services",
              "Commercial Activity: Distribution Or Storage",
              "Commercial Activity: Industrial Or Manufacturing",
              "Commercial Activity: Other",
              "Commercial Activity: Retail",
              "Community Services: Emergency Services",
              "Community Services: Funerary",
              "Community Services: Other",
              "Community Services: Religious Worship",
              "Construction",
              "Defence",
              "Education",
              "Government Services",
              "Historic",
              "Medical Or Health Care",
              "Residential Accommodation",
              "Sports Attraction Or Facility",
              "Temporary Or Holiday Accommodation",
              "Transport: Air",
              "Transport: Rail",
              "Transport: Road, Track Or Path",
              "Transport: Water",
              "Unknown Use",
              "Utility Or Environmental Protection",
              "Unknown Or Unused Artificial",
              "Unknown Or Unused Natural",
              "Mixed Use"
            ],
            "type": [
              "string"
            ]
          },
          "oslandusetierb": {
            "items": {
              "enum": [
                "Agriculture",
                "Air Travel Interchange",
                "Allotments",
                "Ambulance Services",
                "Aquaculture",
                "Athletics",
                "Bowls",
                "Buddhist Temple",
                "Bus Network Interchange",
                "Camp Site",
                "Caravan Site",
                "Cathedral",
                "Cemetery",
                "Chapel",
                "Chemical Processing",
                "Church",
                "Coach Network Interchange",
                "Coastal Protection",
                "Coastguard Services",
                "Communal Residential",
                "Community Meeting Place",
                "Cricket",
                "Cycling Sports",
                "Diplomatic Services",
                "Electricity Distribution",
                "Energy Generation",
                "Equestrian Sports",
                "Ferry Terminal",
                "Fire Services",
                "First School",
                "Fisheries",
                "Fishing Sport",
                "Flood Or Water Controlling",
                "Football",
                "Further Education",
                "Gas Distribution Or Storage",
                "Gas Extraction",
                "Gas Production",
                "Golf",
                "Greyhound Racing",
                "Gurdwara",
                "Higher Education",
                "Hindu Temple",
                "Hockey",
                "Holiday Accommodation",
                "Holiday Centre",
                "Horse Racing",
                "Ice Sports",
                "Infant School",
                "Junior School",
                "Kingdom Hall",
                "Leisure Or Sports Centre",
                "Lifeboat Services",
                "Light Rail System Interchange",
                "Mainline Railway Interchange",
                "Mainline Railway Principal Interchange",
                "Mainline Railway Station (Non Public Accessible)",
                "Middle School",
                "Mineral Or Fuel Extraction",
                "Mosque",
                "Motor Sports",
                "Multi-Purpose Community Site",
                "Non State Primary Or Preparatory School",
                "Non State Secondary School",
                "Observation",
                "Oil Extraction",
                "Oil Refinery",
                "Oil Terminal",
                "Outdoor Amenity",
                "Place Of Worship",
                "Police Services",
                "Preserved Railway Interchange",
                "Primary Health Care",
                "Primary School",
                "Prison Services",
                "Private Residence",
                "Pupil Referral",
                "Racquet Sports",
                "Rail Travel Interchange",
                "Religious Meeting Place",
                "Residential Garden",
                "Rugby",
                "School",
                "School For Special Needs",
                "Secondary Health Care",
                "Secondary School",
                "Shooting",
                "Skiing",
                "Stupa",
                "Swimming Pool",
                "Synagogue",
                "Telecommunications",
                "Underground Railway System Interchange",
                "University",
                "University Halls Of Residence",
                "Waste Disposal",
                "Waste Water Treatment",
                "Water Distribution",
                "Water Sports",
                "Weather Observation"
              ],
              "enumeration": true,
              "maxLength": 200,
              "type": [
                "string",
                "null"
              ]
            },
            "type": [
              "array"
            ]
          },
          "relativeheightmaximum": {
            "type": [
              "number",
              "null"
            ]
          },
          "relativeheightroofbase": {
            "type": [
              "number",
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
        "sha256": "405de8de8ae403f6377e382ab35ab8cc7a461597d38c710e06a28f24a63f4eca",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "str-fts-structure-1.0",
        "properties": {
          "absoluteheightmaximum": {
            "type": [
              "number",
              "null"
            ]
          },
          "absoluteheightminimum": {
            "type": [
              "number",
              "null"
            ]
          },
          "absoluteheightroofbase": {
            "type": [
              "number",
              "null"
            ]
          },
          "associatedstructure": {
            "enum": [
              "Aqueduct",
              "Breakwater",
              "Bridge",
              "Clapper Bridge",
              "Dam",
              "Footbridge",
              "Leisure Pier",
              "Lift Bridge",
              "Sluice",
              "Swing Bridge",
              "Tanker Berthing",
              "Transporter Bridge",
              "Underpass",
              "Viaduct"
            ],
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
              "Cleit",
              "Air Traffic Control Tower",
              "Aircraft Landing Light",
              "Aircraft Navigation Beacon",
              "Arch",
              "Bandstand",
              "Bell",
              "Bell And Light",
              "Bell Tower",
              "Boat Rollers",
              "Boom",
              "Boulder Structure",
              "Boulders",
              "Boundary Marker",
              "Broch",
              "Burial Chamber",
              "Buried Covered Reservoir",
              "Buried Open Reservoir",
              "Buried Open Storage Tank",
              "Buried Storage Tank",
              "Butt",
              "Cable Gantry",
              "Cairn",
              "Caisson",
              "Cannon",
              "Capstan",
              "Chamber",
              "Chambered Cairn",
              "Chimney",
              "Clock",
              "Clock Tower",
              "Conveyor",
              "Cooling Tower",
              "Crane",
              "Crane On Gantry",
              "Cross",
              "Cross And Fixed Structure",
              "Cross Base",
              "Cross Slab",
              "Daymark",
              "Daymark and Light",
              "Diving Platform",
              "Dolphin",
              "Double Wall",
              "Dovecot",
              "Dry Open Tank Reservoir",
              "Dry Reservoir",
              "Dry Weir",
              "Electricity Metal Monopole",
              "Electricity Pylon",
              "Empty Dew Pond",
              "Escalator",
              "Fish Ladder",
              "Fish Trap",
              "Fishing Platform",
              "Fixed Structure",
              "Flare Stack",
              "Floating Crane",
              "Floating Structure",
              "Floating Structure With Light",
              "Flood Controlling Wall",
              "Flood Or Water Controlling Wall",
              "Flue",
              "Fog Bell",
              "Fog Horn",
              "Fog Light",
              "Fountain",
              "Gantry",
              "Gas Holder",
              "Gateway",
              "Gazebo",
              "Glasshouse",
              "Grandstand",
              "Gravestone",
              "Grid",
              "Groyne",
              "Guide Stone",
              "Guide Stone As Boundary Marker",
              "Henge",
              "Hide",
              "Historic Battery",
              "Historic Vessel",
              "Hoist",
              "Holed Stone",
              "Hopper",
              "Hydraulic Ram",
              "Inscribed Rock",
              "Kiln",
              "Lattice Tower",
              "Leat",
              "Lighthouse",
              "Lighting Tower",
              "Lock",
              "Lock Gate",
              "Made Sealed Surface Covered with Solar Panels",
              "Made Unsealed Surface Covered with Solar Panels",
              "Marked Rock",
              "Marked Stone",
              "Market Cross",
              "Mast",
              "Maze",
              "Memorial Wall",
              "Meteorological Station",
              "Mine Shaft",
              "Motor Vehicle Weighbridge",
              "Mound Of Earth",
              "Moveable Glasshouse",
              "Moveable Structure",
              "Navigation Tower",
              "Obelisk",
              "Observation Platform",
              "Open Sludge Tank",
              "Open Slurry Storage Tank",
              "Open Storage Tank",
              "Ornamental Structure",
              "Outfall",
              "Overflow",
              "Paddling Pool",
              "Partially Buried Reservoir",
              "Partially Buried Slurry Storage Tank",
              "Partially Buried Storage Tank",
              "Path On Lock Gate",
              "Pillar",
              "Pipe Bridge",
              "Pipeline",
              "Plinth",
              "Post",
              "Post And Stone",
              "Pump",
              "Pump Waste Water",
              "Pump Water Controlling",
              "Pump Water Distribution",
              "Radar Tower",
              "Radio Telescope",
              "Rail Gantry",
              "Rail Signal Gantry",
              "Rail Signal Light",
              "Rail Vehicle Weighbridge",
              "Remains Of Cairn",
              "Remains Of Chambered Cairn",
              "Remains Of Cross",
              "Retaining Wall",
              "Road Gantry",
              "Rock Shelter",
              "Roofed Conveyor",
              "Roofed Fish Trap",
              "Roofed Hopper",
              "Roofed Reservoir",
              "Roofed Rowing Tank",
              "Roofed Sludge Tank",
              "Roofed Slurry Storage Tank",
              "Roofed Storage Tank",
              "Roofed Telescope",
              "Ruined Structure",
              "Ruined Supported Structure",
              "Ruined Tower",
              "Ruined Windmill",
              "Satellite Dish",
              "Sea Wall",
              "Seat",
              "Seat On Supported Structure",
              "Shaft",
              "Shelter",
              "Shooting Tower",
              "Signal Light As Boundary Marker",
              "Silo",
              "Siren",
              "Slipway",
              "Sloping Masonry",
              "Solar Panels",
              "Solar Panels On Bare Earth Or Grass",
              "Source Of Watercourse",
              "Speakers Platform",
              "Spring",
              "Stand",
              "Standing Stone",
              "Statue",
              "Steps",
              "Stone",
              "Stone Pillar",
              "Supported Conveyor",
              "Supported Flue Pipe",
              "Supported Structure",
              "Surge Shaft",
              "Swimming Platform",
              "Swimming Pool",
              "Target",
              "Telecommunications Mast",
              "Telecommunications Tower",
              "Terraces",
              "Tide Gauge",
              "Toboggan Run",
              "Tomb",
              "Tower",
              "Travelling Conveyor",
              "Travelling Crane",
              "Travelling Radio Telescope",
              "Travelling Structure",
              "Trough",
              "Upper Level Of Communication",
              "Vehicle Dip",
              "Ventilation Shaft",
              "War Memorial",
              "War Memorial Wall",
              "Warning Light",
              "Warning Sign And Stone",
              "Water Controlling Wall",
              "Water Point",
              "Water Storage Tank On Tower",
              "Water Tower",
              "Waterwheel",
              "Weir",
              "Well",
              "Well As Spring",
              "Wind Pump",
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
            "$ref": "https://geojson.org/schema/Polygon.json"
          },
          "geometry_area": {
            "type": "number"
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
          "height_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "height_source": {
            "type": [
              "string",
              "null"
            ]
          },
          "height_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "heightconfidencelevel": {
            "enum": [
              "High",
              "Incomplete",
              "Low",
              "Moderate",
              "Not Assessed"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "ishistoric": {
            "type": "boolean"
          },
          "isobscured": {
            "type": "boolean"
          },
          "istidal": {
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
          "oslandcover_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "oslandcover_source": {
            "type": [
              "string",
              "null"
            ]
          },
          "oslandcover_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "oslandcovertiera": {
            "enum": [
              "Constructed",
              "Made",
              "Mineral",
              "Open Vegetation",
              "Structure",
              "Trees",
              "Water"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "oslandcovertierb": {
            "items": {
              "enum": [
                "Bare Earth Or Grass",
                "Boulder Structure",
                "Boulders",
                "Coniferous Trees",
                "Heath",
                "Inland Water",
                "Inter Tidal",
                "Made Sealed",
                "Made Unknown",
                "Made Unsealed",
                "Maze",
                "Mixed Trees",
                "Non-Coniferous Trees",
                "Rough Grassland",
                "Scrub",
                "Solar Panels",
                "Structure",
                "Travelling Crane",
                "Tidal Water"
              ],
              "maxLength": 100,
              "type": [
                "string",
                "null"
              ]
            },
            "type": "array"
          },
          "oslanduse_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "oslanduse_source": {
            "type": [
              "string",
              "null"
            ]
          },
          "oslanduse_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "oslandusetiera": {
            "enum": [
              "Agriculture Or Aquaculture",
              "Attraction Or Activity",
              "Commercial Activity: Animal Services",
              "Commercial Activity: Distribution Or Storage",
              "Commercial Activity: Industrial Or Manufacturing",
              "Commercial Activity: Other",
              "Commercial Activity: Retail",
              "Community Services: Emergency Services",
              "Community Services: Funerary",
              "Community Services: Other",
              "Community Services: Religious Worship",
              "Construction",
              "Defence",
              "Education",
              "Government Services",
              "Historic",
              "Medical Or Health Care",
              "Residential Accommodation",
              "Sports Attraction Or Facility",
              "Temporary Or Holiday Accommodation",
              "Transport: Air",
              "Transport: Rail",
              "Transport: Road, Track Or Path",
              "Transport: Water",
              "Unknown Use",
              "Utility Or Environmental Protection",
              "Unknown Or Unused Artificial",
              "Unknown Or Unused Natural",
              "Mixed Use"
            ],
            "type": "string"
          },
          "oslandusetierb": {
            "items": {
              "enum": [
                "Agriculture",
                "Air Travel Interchange",
                "Allotments",
                "Ambulance Services",
                "Aquaculture",
                "Athletics",
                "Bowls",
                "Buddhist Temple",
                "Bus Network Interchange",
                "Camp Site",
                "Caravan Site",
                "Cathedral",
                "Cemetery",
                "Chapel",
                "Chemical Processing",
                "Church",
                "Coach Network Interchange",
                "Coastal Protection",
                "Coastguard Services",
                "Communal Residential",
                "Community Meeting Place",
                "Cricket",
                "Cycling Sports",
                "Diplomatic Services",
                "Electricity Distribution",
                "Energy Generation",
                "Equestrian Sports",
                "Ferry Terminal",
                "Fire Services",
                "First School",
                "Fisheries",
                "Fishing Sport",
                "Flood Or Water Controlling",
                "Football",
                "Further Education",
                "Gas Distribution Or Storage",
                "Gas Extraction",
                "Gas Production",
                "Golf",
                "Greyhound Racing",
                "Gurdwara",
                "Higher Education",
                "Hindu Temple",
                "Hockey",
                "Holiday Accommodation",
                "Holiday Centre",
                "Horse Racing",
                "Ice Sports",
                "Infant School",
                "Junior School",
                "Kingdom Hall",
                "Leisure Or Sports Centre",
                "Lifeboat Services",
                "Light Rail System Interchange",
                "Mainline Railway Interchange",
                "Mainline Railway Principal Interchange",
                "Mainline Railway Station (Non Public Accessible)",
                "Middle School",
                "Mineral Or Fuel Extraction",
                "Mosque",
                "Motor Sports",
                "Multi-Purpose Community Site",
                "Non State Primary Or Preparatory School",
                "Non State Secondary School",
                "Observation",
                "Oil Extraction",
                "Oil Refinery",
                "Oil Terminal",
                "Outdoor Amenity",
                "Place Of Worship",
                "Police Services",
                "Preserved Railway Interchange",
                "Primary Health Care",
                "Primary School",
                "Prison Services",
                "Private Residence",
                "Pupil Referral",
                "Racquet Sports",
                "Rail Travel Interchange",
                "Religious Meeting Place",
                "Residential Garden",
                "Rugby",
                "School",
                "School For Special Needs",
                "Secondary Health Care",
                "Secondary School",
                "Shooting",
                "Skiing",
                "Stupa",
                "Swimming Pool",
                "Synagogue",
                "Telecommunications",
                "Underground Railway System Interchange",
                "University",
                "University Halls Of Residence",
                "Waste Disposal",
                "Waste Water Treatment",
                "Water Distribution",
                "Water Sports",
                "Weather Observation"
              ],
              "maxLength": 200,
              "type": [
                "string",
                "null"
              ]
            },
            "type": "array"
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
          "relativeheightmaximum": {
            "type": [
              "number",
              "null"
            ]
          },
          "relativeheightroofbase": {
            "type": [
              "number",
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
          "capturespecification",
          "changetype",
          "description",
          "description_updatedate",
          "geometry",
          "geometry_area",
          "geometry_updatedate",
          "ishistoric",
          "isobscured",
          "istidal",
          "osid",
          "physicallevel",
          "theme",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "0dfac183f0fd73e7febdd7f5cec16029d00bfdf6e7f0c0343a49bcee472454d8",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Structure v1"
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
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/queryables",
      "responseSha256": "405de8de8ae403f6377e382ab35ab8cc7a461597d38c710e06a28f24a63f4eca",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema",
      "responseSha256": "0dfac183f0fd73e7febdd7f5cec16029d00bfdf6e7f0c0343a49bcee472454d8",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/absoluteheightmaximum",
      "@type": "rdf:Property",
      "dcterms:identifier": "absoluteheightmaximum",
      "rdfs:label": "absoluteheightmaximum",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/absoluteheightminimum",
      "@type": "rdf:Property",
      "dcterms:identifier": "absoluteheightminimum",
      "rdfs:label": "absoluteheightminimum",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/absoluteheightroofbase",
      "@type": "rdf:Property",
      "dcterms:identifier": "absoluteheightroofbase",
      "rdfs:label": "absoluteheightroofbase",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/associatedstructure",
      "@type": "rdf:Property",
      "dcterms:identifier": "associatedstructure",
      "rdfs:label": "associatedstructure",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Aqueduct",
            "Breakwater",
            "Bridge",
            "Clapper Bridge",
            "Dam",
            "Footbridge",
            "Leisure Pier",
            "Lift Bridge",
            "Sluice",
            "Swing Bridge",
            "Tanker Berthing",
            "Transporter Bridge",
            "Underpass",
            "Viaduct"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/capturespecification",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Cleit",
            "Air Traffic Control Tower",
            "Aircraft Landing Light",
            "Aircraft Navigation Beacon",
            "Arch",
            "Bandstand",
            "Bell",
            "Bell And Light",
            "Bell Tower",
            "Boat Rollers",
            "Boom",
            "Boulder Structure",
            "Boulders",
            "Boundary Marker",
            "Broch",
            "Burial Chamber",
            "Buried Covered Reservoir",
            "Buried Open Reservoir",
            "Buried Open Storage Tank",
            "Buried Storage Tank",
            "Butt",
            "Cable Gantry",
            "Cairn",
            "Caisson",
            "Cannon",
            "Capstan",
            "Chamber",
            "Chambered Cairn",
            "Chimney",
            "Clock",
            "Clock Tower",
            "Conveyor",
            "Cooling Tower",
            "Crane",
            "Crane On Gantry",
            "Cross",
            "Cross And Fixed Structure",
            "Cross Base",
            "Cross Slab",
            "Daymark",
            "Daymark and Light",
            "Diving Platform",
            "Dolphin",
            "Double Wall",
            "Dovecot",
            "Dry Open Tank Reservoir",
            "Dry Reservoir",
            "Dry Weir",
            "Electricity Metal Monopole",
            "Electricity Pylon",
            "Empty Dew Pond",
            "Escalator",
            "Fish Ladder",
            "Fish Trap",
            "Fishing Platform",
            "Fixed Structure",
            "Flare Stack",
            "Floating Crane",
            "Floating Structure",
            "Floating Structure With Light",
            "Flood Controlling Wall",
            "Flood Or Water Controlling Wall",
            "Flue",
            "Fog Bell",
            "Fog Horn",
            "Fog Light",
            "Fountain",
            "Gantry",
            "Gas Holder",
            "Gateway",
            "Gazebo",
            "Glasshouse",
            "Grandstand",
            "Gravestone",
            "Grid",
            "Groyne",
            "Guide Stone",
            "Guide Stone As Boundary Marker",
            "Henge",
            "Hide",
            "Historic Battery",
            "Historic Vessel",
            "Hoist",
            "Holed Stone",
            "Hopper",
            "Hydraulic Ram",
            "Inscribed Rock",
            "Kiln",
            "Lattice Tower",
            "Leat",
            "Lighthouse",
            "Lighting Tower",
            "Lock",
            "Lock Gate",
            "Made Sealed Surface Covered with Solar Panels",
            "Made Unsealed Surface Covered with Solar Panels",
            "Marked Rock",
            "Marked Stone",
            "Market Cross",
            "Mast",
            "Maze",
            "Memorial Wall",
            "Meteorological Station",
            "Mine Shaft",
            "Motor Vehicle Weighbridge",
            "Mound Of Earth",
            "Moveable Glasshouse",
            "Moveable Structure",
            "Navigation Tower",
            "Obelisk",
            "Observation Platform",
            "Open Sludge Tank",
            "Open Slurry Storage Tank",
            "Open Storage Tank",
            "Ornamental Structure",
            "Outfall",
            "Overflow",
            "Paddling Pool",
            "Partially Buried Reservoir",
            "Partially Buried Slurry Storage Tank",
            "Partially Buried Storage Tank",
            "Path On Lock Gate",
            "Pillar",
            "Pipe Bridge",
            "Pipeline",
            "Plinth",
            "Post",
            "Post And Stone",
            "Pump",
            "Pump Waste Water",
            "Pump Water Controlling",
            "Pump Water Distribution",
            "Radar Tower",
            "Radio Telescope",
            "Rail Gantry",
            "Rail Signal Gantry",
            "Rail Signal Light",
            "Rail Vehicle Weighbridge",
            "Remains Of Cairn",
            "Remains Of Chambered Cairn",
            "Remains Of Cross",
            "Retaining Wall",
            "Road Gantry",
            "Rock Shelter",
            "Roofed Conveyor",
            "Roofed Fish Trap",
            "Roofed Hopper",
            "Roofed Reservoir",
            "Roofed Rowing Tank",
            "Roofed Sludge Tank",
            "Roofed Slurry Storage Tank",
            "Roofed Storage Tank",
            "Roofed Telescope",
            "Ruined Structure",
            "Ruined Supported Structure",
            "Ruined Tower",
            "Ruined Windmill",
            "Satellite Dish",
            "Sea Wall",
            "Seat",
            "Seat On Supported Structure",
            "Shaft",
            "Shelter",
            "Shooting Tower",
            "Signal Light As Boundary Marker",
            "Silo",
            "Siren",
            "Slipway",
            "Sloping Masonry",
            "Solar Panels",
            "Solar Panels On Bare Earth Or Grass",
            "Source Of Watercourse",
            "Speakers Platform",
            "Spring",
            "Stand",
            "Standing Stone",
            "Statue",
            "Steps",
            "Stone",
            "Stone Pillar",
            "Supported Conveyor",
            "Supported Flue Pipe",
            "Supported Structure",
            "Surge Shaft",
            "Swimming Platform",
            "Swimming Pool",
            "Target",
            "Telecommunications Mast",
            "Telecommunications Tower",
            "Terraces",
            "Tide Gauge",
            "Toboggan Run",
            "Tomb",
            "Tower",
            "Travelling Conveyor",
            "Travelling Crane",
            "Travelling Radio Telescope",
            "Travelling Structure",
            "Trough",
            "Upper Level Of Communication",
            "Vehicle Dip",
            "Ventilation Shaft",
            "War Memorial",
            "War Memorial Wall",
            "Warning Light",
            "Warning Sign And Stone",
            "Water Controlling Wall",
            "Water Point",
            "Water Storage Tank On Tower",
            "Water Tower",
            "Waterwheel",
            "Weir",
            "Well",
            "Well As Spring",
            "Wind Pump",
            "Wind Turbine"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/description_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/description_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/description_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/firstdigitalcapturedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/geometry",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry",
      "rdfs:label": "geometry",
      "okfp:schemaDefinition": {
        "@value": {
          "$ref": "https://geojson.org/schema/Polygon.json"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/geometry_area",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry_area",
      "rdfs:label": "geometry_area",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/geometry_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/geometry_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/geometry_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/height_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "height_evidencedate",
      "rdfs:label": "height_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/height_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "height_source",
      "rdfs:label": "height_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/height_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "height_updatedate",
      "rdfs:label": "height_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/heightconfidencelevel",
      "@type": "rdf:Property",
      "dcterms:identifier": "heightconfidencelevel",
      "rdfs:label": "heightconfidencelevel",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "High",
            "Incomplete",
            "Low",
            "Moderate",
            "Not Assessed"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/ishistoric",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/isobscured",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/istidal",
      "@type": "rdf:Property",
      "dcterms:identifier": "istidal",
      "rdfs:label": "istidal",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "boolean"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/name1_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/name1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/name1_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/name1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/name1_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/name2_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/name2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/name2_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/name2_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/operationalstatus",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/oslandcover_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslandcover_evidencedate",
      "rdfs:label": "oslandcover_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/oslandcover_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslandcover_source",
      "rdfs:label": "oslandcover_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/oslandcover_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslandcover_updatedate",
      "rdfs:label": "oslandcover_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/oslandcovertiera",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslandcovertiera",
      "rdfs:label": "oslandcovertiera",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Constructed",
            "Made",
            "Mineral",
            "Open Vegetation",
            "Structure",
            "Trees",
            "Water"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/oslandcovertierb",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslandcovertierb",
      "rdfs:label": "oslandcovertierb",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "enum": [
              "Bare Earth Or Grass",
              "Boulder Structure",
              "Boulders",
              "Coniferous Trees",
              "Heath",
              "Inland Water",
              "Inter Tidal",
              "Made Sealed",
              "Made Unknown",
              "Made Unsealed",
              "Maze",
              "Mixed Trees",
              "Non-Coniferous Trees",
              "Rough Grassland",
              "Scrub",
              "Solar Panels",
              "Structure",
              "Travelling Crane",
              "Tidal Water"
            ],
            "maxLength": 100,
            "type": [
              "string",
              "null"
            ]
          },
          "type": "array"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/oslanduse_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslanduse_evidencedate",
      "rdfs:label": "oslanduse_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/oslanduse_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslanduse_source",
      "rdfs:label": "oslanduse_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/oslanduse_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslanduse_updatedate",
      "rdfs:label": "oslanduse_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/oslandusetiera",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslandusetiera",
      "rdfs:label": "oslandusetiera",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Agriculture Or Aquaculture",
            "Attraction Or Activity",
            "Commercial Activity: Animal Services",
            "Commercial Activity: Distribution Or Storage",
            "Commercial Activity: Industrial Or Manufacturing",
            "Commercial Activity: Other",
            "Commercial Activity: Retail",
            "Community Services: Emergency Services",
            "Community Services: Funerary",
            "Community Services: Other",
            "Community Services: Religious Worship",
            "Construction",
            "Defence",
            "Education",
            "Government Services",
            "Historic",
            "Medical Or Health Care",
            "Residential Accommodation",
            "Sports Attraction Or Facility",
            "Temporary Or Holiday Accommodation",
            "Transport: Air",
            "Transport: Rail",
            "Transport: Road, Track Or Path",
            "Transport: Water",
            "Unknown Use",
            "Utility Or Environmental Protection",
            "Unknown Or Unused Artificial",
            "Unknown Or Unused Natural",
            "Mixed Use"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/oslandusetierb",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslandusetierb",
      "rdfs:label": "oslandusetierb",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "enum": [
              "Agriculture",
              "Air Travel Interchange",
              "Allotments",
              "Ambulance Services",
              "Aquaculture",
              "Athletics",
              "Bowls",
              "Buddhist Temple",
              "Bus Network Interchange",
              "Camp Site",
              "Caravan Site",
              "Cathedral",
              "Cemetery",
              "Chapel",
              "Chemical Processing",
              "Church",
              "Coach Network Interchange",
              "Coastal Protection",
              "Coastguard Services",
              "Communal Residential",
              "Community Meeting Place",
              "Cricket",
              "Cycling Sports",
              "Diplomatic Services",
              "Electricity Distribution",
              "Energy Generation",
              "Equestrian Sports",
              "Ferry Terminal",
              "Fire Services",
              "First School",
              "Fisheries",
              "Fishing Sport",
              "Flood Or Water Controlling",
              "Football",
              "Further Education",
              "Gas Distribution Or Storage",
              "Gas Extraction",
              "Gas Production",
              "Golf",
              "Greyhound Racing",
              "Gurdwara",
              "Higher Education",
              "Hindu Temple",
              "Hockey",
              "Holiday Accommodation",
              "Holiday Centre",
              "Horse Racing",
              "Ice Sports",
              "Infant School",
              "Junior School",
              "Kingdom Hall",
              "Leisure Or Sports Centre",
              "Lifeboat Services",
              "Light Rail System Interchange",
              "Mainline Railway Interchange",
              "Mainline Railway Principal Interchange",
              "Mainline Railway Station (Non Public Accessible)",
              "Middle School",
              "Mineral Or Fuel Extraction",
              "Mosque",
              "Motor Sports",
              "Multi-Purpose Community Site",
              "Non State Primary Or Preparatory School",
              "Non State Secondary School",
              "Observation",
              "Oil Extraction",
              "Oil Refinery",
              "Oil Terminal",
              "Outdoor Amenity",
              "Place Of Worship",
              "Police Services",
              "Preserved Railway Interchange",
              "Primary Health Care",
              "Primary School",
              "Prison Services",
              "Private Residence",
              "Pupil Referral",
              "Racquet Sports",
              "Rail Travel Interchange",
              "Religious Meeting Place",
              "Residential Garden",
              "Rugby",
              "School",
              "School For Special Needs",
              "Secondary Health Care",
              "Secondary School",
              "Shooting",
              "Skiing",
              "Stupa",
              "Swimming Pool",
              "Synagogue",
              "Telecommunications",
              "Underground Railway System Interchange",
              "University",
              "University Halls Of Residence",
              "Waste Disposal",
              "Waste Water Treatment",
              "Water Distribution",
              "Water Sports",
              "Weather Observation"
            ],
            "maxLength": 200,
            "type": [
              "string",
              "null"
            ]
          },
          "type": "array"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/physicallevel",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/relativeheightmaximum",
      "@type": "rdf:Property",
      "dcterms:identifier": "relativeheightmaximum",
      "rdfs:label": "relativeheightmaximum",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/relativeheightroofbase",
      "@type": "rdf:Property",
      "dcterms:identifier": "relativeheightroofbase",
      "rdfs:label": "relativeheightroofbase",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/toid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-structure-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1/schema"
      }
    }
  ]
}
---

# Structure v1

Polygon feature representing a manmade construction that is not a building. Examples include a mast, a chimney, and a crane.

Native identifier: `str-fts-structure-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-structure-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2022-08-27T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
