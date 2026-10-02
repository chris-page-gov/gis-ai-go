---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Rail v3",
  "description": "Features related to travel by railway or tramway. Features representing, describing or limiting the extents of railways. The Transport Features Collection contains information relating to permanent railways that form the network between two points.",
  "nativeIdentifier": "trn-fts-rail-3",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3",
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
      "sourcePointer": "/collections/38",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/38",
      "normalisedRecordSha256": "2123ef3e88ee0aa6e2893b70fb424139b68b423569d60acb906aa0331213ec70",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3"
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
    "start": "2024-09-24T00:00:00Z",
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
    "description": "Features related to travel by railway or tramway. Features representing, describing or limiting the extents of railways. The Transport Features Collection contains information relating to permanent railways that form the network between two points.",
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
            "2024-09-24T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "trn-fts-rail-3",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3",
        "rel": "self",
        "title": "The 'Rail v3' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/items",
        "rel": "items",
        "title": "The features in the 'Rail v3' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema",
        "rel": "describedby",
        "title": "Schema for the 'Rail v3' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Rail v3' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/queryables",
        "properties": {
          "description": {
            "enum": [
              "Railway Traverse",
              "Made Surface",
              "Sloping Masonry",
              "Transport Curtilage",
              "Turntable"
            ],
            "type": [
              "string"
            ]
          },
          "geometry_area_m2": {
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
          "oslandcovertiera": {
            "enum": [
              "Made",
              "Mineral",
              "Open Vegetation",
              "Trees"
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
                "Scrub"
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
              "Mixed Use",
              "Residential Accommodation",
              "Sports Attraction Or Facility",
              "Temporary Or Holiday Accommodation",
              "Transport: Air",
              "Transport: Rail",
              "Transport: Road, Track Or Path",
              "Transport: Water",
              "Unknown Or Unused Artificial",
              "Unknown Or Unused Natural",
              "Unknown Use",
              "Utility Or Environmental Protection"
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
                "string"
              ]
            },
            "type": [
              "array"
            ]
          },
          "status": {
            "enum": [
              "Active",
              "Derelict",
              "Inactive",
              "Under Construction",
              "Unknown"
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
        "sha256": "c056e2a9af28bb047c40e8363e064752ab3774fdaf99fd1f3d15cbde531d7082",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-fts-rail-3.1",
        "properties": {
          "address_classificationcode": {
            "type": [
              "string",
              "null"
            ]
          },
          "address_primarydescription": {
            "type": [
              "string",
              "null"
            ]
          },
          "address_secondarydescription": {
            "type": [
              "string",
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
          "containingsitecount": {
            "type": "integer"
          },
          "description": {
            "enum": [
              "Railway Traverse",
              "Made Surface",
              "Sloping Masonry",
              "Transport Curtilage",
              "Turntable"
            ],
            "type": "string"
          },
          "description_capturemethod": {
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
          "description_evidencedate": {
            "format": "date",
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
            "$ref": "https://geojson.org/schema/Polygon.json",
            "type": "object"
          },
          "geometry_area_m2": {
            "type": "number"
          },
          "geometry_capturemethod": {
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
          "geometry_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "geometry_updatedate": {
            "format": "date",
            "type": "string"
          },
          "habitatcoveragereference": {
            "items": {
              "properties": {
                "featuretypeversiondate": {
                  "description": "Date of the latest Land feature version.",
                  "format": "date",
                  "originalName": "featureTypeVersionDate",
                  "type": "string"
                },
                "habitatcode": {
                  "description": "Habitat classification code for EUNIS Level 1 and EUNIS Level 2 only, where a direct mapping is possible to the OS Land Cover Tier B classification value. This is blank for OS Land Cover Tier B and UK BAP Broad Habitat.",
                  "maxLength": 5,
                  "originalName": "habitatCode",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "habitatdescription": {
                  "description": "Habitat classification description. EUNIS Level 2 and UK BAP Broad Habitat descriptions are populated where a direct mapping is possible to the OS Land Cover Tier B classification value.",
                  "maxLength": 80,
                  "originalName": "habitatDescription",
                  "type": "string"
                },
                "osid": {
                  "description": "Primary feature identifier of the feature reference.",
                  "format": "uuid",
                  "maxLength": 36,
                  "originalName": "OSID",
                  "type": "string"
                },
                "percentage": {
                  "description": "Numerical value of the calculated percentage of each classification within a single topographic area.",
                  "originalName": "percentage",
                  "type": [
                    "integer",
                    "null"
                  ]
                },
                "percentage_evidencedate": {
                  "description": "The date on which the latest evidence was gathered to make an update to the percentage value, if required.",
                  "format": "date",
                  "originalName": "percentage_evidenceDate",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "percentage_updatedate": {
                  "description": "Date the percentage attribute was last updated.",
                  "format": "date",
                  "originalName": "percentage_updateDate",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "scheme": {
                  "description": "Classification scheme name.",
                  "maxLength": 20,
                  "originalName": "scheme",
                  "type": "string"
                }
              },
              "type": "object"
            },
            "type": "array"
          },
          "isobscured": {
            "type": "boolean"
          },
          "largestsite_landusetiera": {
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
              "Mixed Use",
              "Residential Accommodation",
              "Sports Attraction Or Facility",
              "Temporary Or Holiday Accommodation",
              "Transport: Air",
              "Transport: Rail",
              "Transport: Road, Track Or Path",
              "Transport: Water",
              "Unknown Or Unused Artificial",
              "Unknown Or Unused Natural",
              "Unknown Use",
              "Utility Or Environmental Protection"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "largestsite_landusetierb": {
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
              "type": "string"
            },
            "type": "array"
          },
          "lowertierlocalauthority_count": {
            "type": "integer"
          },
          "lowertierlocalauthority_gsscode": {
            "type": [
              "string",
              "null"
            ]
          },
          "nlud_code": {
            "type": [
              "string",
              "null"
            ]
          },
          "nlud_groupdescription": {
            "type": [
              "string",
              "null"
            ]
          },
          "nlud_orderdescription": {
            "type": [
              "string",
              "null"
            ]
          },
          "osid": {
            "format": "uuid",
            "type": "string"
          },
          "oslandcover_capturemethod": {
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
          "oslandcover_evidencedate": {
            "format": "date",
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
              "Made",
              "Mineral",
              "Open Vegetation",
              "Trees"
            ],
            "type": "string"
          },
          "oslandcovertierb": {
            "items": {
              "enum": [
                "Bare Earth Or Grass",
                "Coniferous Trees",
                "Heath",
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
                "Scrub"
              ],
              "maxLength": 125,
              "type": "string"
            },
            "type": "array"
          },
          "oslanduse_capturemethod": {
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
          "oslanduse_evidencedate": {
            "format": "date",
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
              "Mixed Use",
              "Residential Accommodation",
              "Sports Attraction Or Facility",
              "Temporary Or Holiday Accommodation",
              "Transport: Air",
              "Transport: Rail",
              "Transport: Road, Track Or Path",
              "Transport: Water",
              "Unknown Or Unused Artificial",
              "Unknown Or Unused Natural",
              "Unknown Use",
              "Utility Or Environmental Protection"
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
              "type": "string"
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
          "sitereference": {
            "items": {
              "properties": {
                "railid": {
                  "description": "The identifier for the Rail feature.",
                  "format": "uuid",
                  "maxLength": 36,
                  "originalName": "railID",
                  "type": "string"
                },
                "railversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "railVersionDate",
                  "type": "string"
                },
                "siteid": {
                  "description": "The identifier for the Site feature.",
                  "format": "uuid",
                  "maxLength": 36,
                  "originalName": "siteID",
                  "type": "string"
                }
              },
              "type": "object"
            },
            "type": "array"
          },
          "smallestsite_landusetiera": {
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
              "Mixed Use",
              "Residential Accommodation",
              "Sports Attraction Or Facility",
              "Temporary Or Holiday Accommodation",
              "Transport: Air",
              "Transport: Rail",
              "Transport: Road, Track Or Path",
              "Transport: Water",
              "Unknown Or Unused Artificial",
              "Unknown Or Unused Natural",
              "Unknown Use",
              "Utility Or Environmental Protection"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "smallestsite_landusetierb": {
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
              "type": "string"
            },
            "type": "array"
          },
          "smallestsite_siteid": {
            "type": [
              "string",
              "null"
            ]
          },
          "status": {
            "enum": [
              "Active",
              "Derelict",
              "Inactive",
              "Under Construction",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "status_updatedate": {
            "format": "date",
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
          "firstdigitalcapturedate",
          "changetype",
          "geometry",
          "geometry_area_m2",
          "geometry_evidencedate",
          "geometry_updatedate",
          "geometry_capturemethod",
          "theme",
          "description",
          "description_evidencedate",
          "description_updatedate",
          "description_capturemethod",
          "oslandcovertiera",
          "oslandcovertierb",
          "oslandcover_evidencedate",
          "oslandcover_updatedate",
          "oslandcover_capturemethod",
          "oslandusetiera",
          "oslandusetierb",
          "oslanduse_evidencedate",
          "oslanduse_updatedate",
          "oslanduse_capturemethod",
          "associatedstructure",
          "isobscured",
          "physicallevel",
          "capturespecification",
          "containingsitecount",
          "smallestsite_siteid",
          "smallestsite_landusetiera",
          "smallestsite_landusetierb",
          "largestsite_landusetiera",
          "largestsite_landusetierb",
          "nlud_code",
          "nlud_orderdescription",
          "nlud_groupdescription",
          "address_classificationcode",
          "address_primarydescription",
          "address_secondarydescription",
          "lowertierlocalauthority_gsscode",
          "lowertierlocalauthority_count",
          "status",
          "status_updatedate",
          "habitatcoveragereference",
          "sitereference"
        ],
        "requiredUndeclared": [],
        "sha256": "72fc369be31a247874d41cbb45aacbfe3698d6d65246a381478f0486c2b02f19",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Rail v3"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2024-09-24T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/queryables",
      "responseSha256": "c056e2a9af28bb047c40e8363e064752ab3774fdaf99fd1f3d15cbde531d7082",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema",
      "responseSha256": "72fc369be31a247874d41cbb45aacbfe3698d6d65246a381478f0486c2b02f19",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/address_classificationcode",
      "@type": "rdf:Property",
      "dcterms:identifier": "address_classificationcode",
      "rdfs:label": "address_classificationcode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/address_primarydescription",
      "@type": "rdf:Property",
      "dcterms:identifier": "address_primarydescription",
      "rdfs:label": "address_primarydescription",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/address_secondarydescription",
      "@type": "rdf:Property",
      "dcterms:identifier": "address_secondarydescription",
      "rdfs:label": "address_secondarydescription",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/associatedstructure",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/capturespecification",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/containingsitecount",
      "@type": "rdf:Property",
      "dcterms:identifier": "containingsitecount",
      "rdfs:label": "containingsitecount",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Railway Traverse",
            "Made Surface",
            "Sloping Masonry",
            "Transport Curtilage",
            "Turntable"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/description_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "description_capturemethod",
      "rdfs:label": "description_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/description_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/description_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/firstdigitalcapturedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/geometry",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry",
      "rdfs:label": "geometry",
      "okfp:schemaDefinition": {
        "@value": {
          "$ref": "https://geojson.org/schema/Polygon.json",
          "type": "object"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/geometry_area_m2",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry_area_m2",
      "rdfs:label": "geometry_area_m2",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/geometry_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry_capturemethod",
      "rdfs:label": "geometry_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/geometry_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/geometry_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/habitatcoveragereference",
      "@type": "rdf:Property",
      "dcterms:identifier": "habitatcoveragereference",
      "rdfs:label": "habitatcoveragereference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "featuretypeversiondate": {
                "description": "Date of the latest Land feature version.",
                "format": "date",
                "originalName": "featureTypeVersionDate",
                "type": "string"
              },
              "habitatcode": {
                "description": "Habitat classification code for EUNIS Level 1 and EUNIS Level 2 only, where a direct mapping is possible to the OS Land Cover Tier B classification value. This is blank for OS Land Cover Tier B and UK BAP Broad Habitat.",
                "maxLength": 5,
                "originalName": "habitatCode",
                "type": [
                  "string",
                  "null"
                ]
              },
              "habitatdescription": {
                "description": "Habitat classification description. EUNIS Level 2 and UK BAP Broad Habitat descriptions are populated where a direct mapping is possible to the OS Land Cover Tier B classification value.",
                "maxLength": 80,
                "originalName": "habitatDescription",
                "type": "string"
              },
              "osid": {
                "description": "Primary feature identifier of the feature reference.",
                "format": "uuid",
                "maxLength": 36,
                "originalName": "OSID",
                "type": "string"
              },
              "percentage": {
                "description": "Numerical value of the calculated percentage of each classification within a single topographic area.",
                "originalName": "percentage",
                "type": [
                  "integer",
                  "null"
                ]
              },
              "percentage_evidencedate": {
                "description": "The date on which the latest evidence was gathered to make an update to the percentage value, if required.",
                "format": "date",
                "originalName": "percentage_evidenceDate",
                "type": [
                  "string",
                  "null"
                ]
              },
              "percentage_updatedate": {
                "description": "Date the percentage attribute was last updated.",
                "format": "date",
                "originalName": "percentage_updateDate",
                "type": [
                  "string",
                  "null"
                ]
              },
              "scheme": {
                "description": "Classification scheme name.",
                "maxLength": 20,
                "originalName": "scheme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/isobscured",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/largestsite_landusetiera",
      "@type": "rdf:Property",
      "dcterms:identifier": "largestsite_landusetiera",
      "rdfs:label": "largestsite_landusetiera",
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
            "Mixed Use",
            "Residential Accommodation",
            "Sports Attraction Or Facility",
            "Temporary Or Holiday Accommodation",
            "Transport: Air",
            "Transport: Rail",
            "Transport: Road, Track Or Path",
            "Transport: Water",
            "Unknown Or Unused Artificial",
            "Unknown Or Unused Natural",
            "Unknown Use",
            "Utility Or Environmental Protection"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/largestsite_landusetierb",
      "@type": "rdf:Property",
      "dcterms:identifier": "largestsite_landusetierb",
      "rdfs:label": "largestsite_landusetierb",
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
            "type": "string"
          },
          "type": "array"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/lowertierlocalauthority_count",
      "@type": "rdf:Property",
      "dcterms:identifier": "lowertierlocalauthority_count",
      "rdfs:label": "lowertierlocalauthority_count",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/lowertierlocalauthority_gsscode",
      "@type": "rdf:Property",
      "dcterms:identifier": "lowertierlocalauthority_gsscode",
      "rdfs:label": "lowertierlocalauthority_gsscode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/nlud_code",
      "@type": "rdf:Property",
      "dcterms:identifier": "nlud_code",
      "rdfs:label": "nlud_code",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/nlud_groupdescription",
      "@type": "rdf:Property",
      "dcterms:identifier": "nlud_groupdescription",
      "rdfs:label": "nlud_groupdescription",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/nlud_orderdescription",
      "@type": "rdf:Property",
      "dcterms:identifier": "nlud_orderdescription",
      "rdfs:label": "nlud_orderdescription",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/oslandcover_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslandcover_capturemethod",
      "rdfs:label": "oslandcover_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/oslandcover_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/oslandcover_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/oslandcovertiera",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslandcovertiera",
      "rdfs:label": "oslandcovertiera",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Made",
            "Mineral",
            "Open Vegetation",
            "Trees"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/oslandcovertierb",
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
              "Scrub"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/oslanduse_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "oslanduse_capturemethod",
      "rdfs:label": "oslanduse_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/oslanduse_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/oslanduse_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/oslandusetiera",
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
            "Mixed Use",
            "Residential Accommodation",
            "Sports Attraction Or Facility",
            "Temporary Or Holiday Accommodation",
            "Transport: Air",
            "Transport: Rail",
            "Transport: Road, Track Or Path",
            "Transport: Water",
            "Unknown Or Unused Artificial",
            "Unknown Or Unused Natural",
            "Unknown Use",
            "Utility Or Environmental Protection"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/oslandusetierb",
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
            "type": "string"
          },
          "type": "array"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/physicallevel",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/sitereference",
      "@type": "rdf:Property",
      "dcterms:identifier": "sitereference",
      "rdfs:label": "sitereference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "railid": {
                "description": "The identifier for the Rail feature.",
                "format": "uuid",
                "maxLength": 36,
                "originalName": "railID",
                "type": "string"
              },
              "railversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "railVersionDate",
                "type": "string"
              },
              "siteid": {
                "description": "The identifier for the Site feature.",
                "format": "uuid",
                "maxLength": 36,
                "originalName": "siteID",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/smallestsite_landusetiera",
      "@type": "rdf:Property",
      "dcterms:identifier": "smallestsite_landusetiera",
      "rdfs:label": "smallestsite_landusetiera",
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
            "Mixed Use",
            "Residential Accommodation",
            "Sports Attraction Or Facility",
            "Temporary Or Holiday Accommodation",
            "Transport: Air",
            "Transport: Rail",
            "Transport: Road, Track Or Path",
            "Transport: Water",
            "Unknown Or Unused Artificial",
            "Unknown Or Unused Natural",
            "Unknown Use",
            "Utility Or Environmental Protection"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/smallestsite_landusetierb",
      "@type": "rdf:Property",
      "dcterms:identifier": "smallestsite_landusetierb",
      "rdfs:label": "smallestsite_landusetierb",
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
            "type": "string"
          },
          "type": "array"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/smallestsite_siteid",
      "@type": "rdf:Property",
      "dcterms:identifier": "smallestsite_siteid",
      "rdfs:label": "smallestsite_siteid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/status",
      "@type": "rdf:Property",
      "dcterms:identifier": "status",
      "rdfs:label": "status",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Active",
            "Derelict",
            "Inactive",
            "Under Construction",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/status_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "status_updatedate",
      "rdfs:label": "status_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/toid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-fts-rail-3/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3/schema"
      }
    }
  ]
}
---

# Rail v3

Features related to travel by railway or tramway. Features representing, describing or limiting the extents of railways. The Transport Features Collection contains information relating to permanent railways that form the network between two points.

Native identifier: `trn-fts-rail-3`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-fts-rail-3)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2024-09-24T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
