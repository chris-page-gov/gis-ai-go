---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Road Track Or Path v1",
  "description": "Features representing, describing or limiting the extents of roadways, tracks and pathways. A road is a metalled way for vehicles. A track is an unmetalled way that is clearly marked, permanent and used by vehicles. A path is defined as any established way other than a road or track.",
  "nativeIdentifier": "trn-fts-roadtrackorpath-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1",
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
      "sourcePointer": "/collections/40",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/40",
      "normalisedRecordSha256": "29562d8023cf2f440c233047a156de2b1183310fe90e8328371dc1e0597b3e95",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1"
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
    "description": "Features representing, describing or limiting the extents of roadways, tracks and pathways. A road is a metalled way for vehicles. A track is an unmetalled way that is clearly marked, permanent and used by vehicles. A path is defined as any established way other than a road or track.",
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
    "id": "trn-fts-roadtrackorpath-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1",
        "rel": "self",
        "title": "The 'Road Track Or Path v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/items",
        "rel": "items",
        "title": "The features in the 'Road Track Or Path v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Road Track Or Path v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Road Track Or Path v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/queryables",
        "properties": {
          "description": {
            "enum": [
              "Central Reservation",
              "Cycle Way",
              "Escape Lane",
              "Ford",
              "Lay-by",
              "Level Crossing",
              "Path",
              "Path And Steps",
              "Path On Pipe",
              "Pavement",
              "Pavement And Steps",
              "Pedestrian Crossing",
              "Road",
              "Road Turntable",
              "Roofed Path",
              "Roofed Track",
              "Sand Drag",
              "Shared Use Carriageway",
              "Towing Path",
              "Track",
              "Traffic Calming",
              "Transport Curtilage",
              "Travelling Walkway",
              "Vehicle Dip"
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
              "Trees",
              "Unmade",
              "Water"
            ],
            "type": [
              "string"
            ]
          },
          "oslandcovertierb": {
            "items": {
              "enum": [
                "Bare Earth Or Grass",
                "Coniferous Trees",
                "Heath",
                "Inland Water",
                "Inter Tidal",
                "Made Sealed",
                "Made Unknown",
                "Made Unsealed",
                "Mixed Trees",
                "Non-Coniferous Trees",
                "Rock",
                "Rough Grassland",
                "Sand",
                "Scattered Coniferous Trees",
                "Scattered Mixed Trees",
                "Scattered Non-Coniferous Trees",
                "Scrub",
                "Structure",
                "Tidal Water",
                "Unmade"
              ],
              "enumeration": true,
              "maxLength": 125,
              "type": [
                "string"
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
          "toid": {
            "type": [
              "string",
              "null"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "eb0bc3ef0320cd437d16a45df87778c28fd683015ae56b180d0d0ef9949f9754",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-fts-roadtrackorpath-1.0",
        "properties": {
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
              "Central Reservation",
              "Cycle Way",
              "Escape Lane",
              "Ford",
              "Lay-by",
              "Level Crossing",
              "Path",
              "Path And Steps",
              "Path On Pipe",
              "Pavement",
              "Pavement And Steps",
              "Pedestrian Crossing",
              "Road",
              "Road Turntable",
              "Roofed Path",
              "Roofed Track",
              "Sand Drag",
              "Shared Use Carriageway",
              "Towing Path",
              "Track",
              "Traffic Calming",
              "Transport Curtilage",
              "Travelling Walkway",
              "Vehicle Dip"
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
          "isobscured": {
            "type": "boolean"
          },
          "istidal": {
            "type": "boolean"
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
            "type": "string"
          },
          "oslandcovertiera": {
            "enum": [
              "Constructed",
              "Made",
              "Mineral",
              "Open Vegetation",
              "Trees",
              "Unmade",
              "Water"
            ],
            "type": "string"
          },
          "oslandcovertierb": {
            "items": {
              "enum": [
                "Bare Earth Or Grass",
                "Coniferous Trees",
                "Heath",
                "Inland Water",
                "Inter Tidal",
                "Made Sealed",
                "Made Unknown",
                "Made Unsealed",
                "Mixed Trees",
                "Non-Coniferous Trees",
                "Rock",
                "Rough Grassland",
                "Sand",
                "Scattered Coniferous Trees",
                "Scattered Mixed Trees",
                "Scattered Non-Coniferous Trees",
                "Scrub",
                "Structure",
                "Tidal Water",
                "Unmade"
              ],
              "maxLength": 125,
              "type": "string"
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
            "type": "string"
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
          "isobscured",
          "istidal",
          "osid",
          "oslandcover_updatedate",
          "oslandcovertiera",
          "oslandcovertierb",
          "oslanduse_updatedate",
          "oslandusetiera",
          "physicallevel",
          "theme",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "378aa1a2f899ef0f1267ad75155e45c6658c725fb308d3c7990adbf6a56e5e74",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Road Track Or Path v1"
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
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/queryables",
      "responseSha256": "eb0bc3ef0320cd437d16a45df87778c28fd683015ae56b180d0d0ef9949f9754",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema",
      "responseSha256": "378aa1a2f899ef0f1267ad75155e45c6658c725fb308d3c7990adbf6a56e5e74",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/associatedstructure",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/capturespecification",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Central Reservation",
            "Cycle Way",
            "Escape Lane",
            "Ford",
            "Lay-by",
            "Level Crossing",
            "Path",
            "Path And Steps",
            "Path On Pipe",
            "Pavement",
            "Pavement And Steps",
            "Pedestrian Crossing",
            "Road",
            "Road Turntable",
            "Roofed Path",
            "Roofed Track",
            "Sand Drag",
            "Shared Use Carriageway",
            "Towing Path",
            "Track",
            "Traffic Calming",
            "Transport Curtilage",
            "Travelling Walkway",
            "Vehicle Dip"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/description_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/description_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/description_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/firstdigitalcapturedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/geometry_area",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/geometry_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/geometry_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/geometry_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/isobscured",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/istidal",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/oslandcover_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/oslandcover_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/oslandcover_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslandcover_updatedate",
      "rdfs:label": "oslandcover_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/oslandcovertiera",
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
            "Trees",
            "Unmade",
            "Water"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/oslandcovertierb",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslandcovertierb",
      "rdfs:label": "oslandcovertierb",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "enum": [
              "Bare Earth Or Grass",
              "Coniferous Trees",
              "Heath",
              "Inland Water",
              "Inter Tidal",
              "Made Sealed",
              "Made Unknown",
              "Made Unsealed",
              "Mixed Trees",
              "Non-Coniferous Trees",
              "Rock",
              "Rough Grassland",
              "Sand",
              "Scattered Coniferous Trees",
              "Scattered Mixed Trees",
              "Scattered Non-Coniferous Trees",
              "Scrub",
              "Structure",
              "Tidal Water",
              "Unmade"
            ],
            "maxLength": 125,
            "type": "string"
          },
          "type": "array"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/oslanduse_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/oslanduse_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/oslanduse_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslanduse_updatedate",
      "rdfs:label": "oslanduse_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/oslandusetiera",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/oslandusetierb",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/physicallevel",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/toid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-roadtrackorpath-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1/schema"
      }
    }
  ]
}
---

# Road Track Or Path v1

Features representing, describing or limiting the extents of roadways, tracks and pathways. A road is a metalled way for vehicles. A track is an unmetalled way that is clearly marked, permanent and used by vehicles. A path is defined as any established way other than a road or track.

Native identifier: `trn-fts-roadtrackorpath-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-roadtrackorpath-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2022-08-27T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
