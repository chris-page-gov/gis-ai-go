---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Site v2",
  "description": "Polygon feature which represents the recognisable extent of certain types of function or activity. Examples include a caravan site, a university, and a railway centre.",
  "nativeIdentifier": "lus-fts-site-2",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "OS NGD",
    "lus",
    "schema",
    "queryables"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections",
      "retrievedAt": "2026-10-02T01:18:50.822323Z",
      "responseSha256": "cf6f9c7670533ff42c64af98a8f7bb8aa60911463d937623a4fc6f5bb8767de9",
      "sourcePointer": "/collections/22",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/22",
      "normalisedRecordSha256": "4a04b4a52fae25bd3104e6ca02c544a072c2c1f692fd96f166960f9f6e52f1f1",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2"
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
    "start": "2024-09-07T00:00:00Z",
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
    "description": "Polygon feature which represents the recognisable extent of certain types of function or activity. Examples include a caravan site, a university, and a railway centre.",
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
            "2024-09-07T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "lus-fts-site-2",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2",
        "rel": "self",
        "title": "The 'Site v2' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/items",
        "rel": "items",
        "title": "The features in the 'Site v2' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema",
        "rel": "describedby",
        "title": "Schema for the 'Site v2' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Site v2' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/queryables",
        "properties": {
          "description": {
            "enum": [
              "Abattoir",
              "Abbey",
              "Agriculture Services Site",
              "Air Freight Terminal",
              "Air Navigation Beacon",
              "Air Passenger Terminal",
              "Air Quality Monitoring Station",
              "Air Traffic Control Centre",
              "Air Transport Services Site",
              "Aircraft Works",
              "Airfield",
              "Airport With Scheduled Services",
              "Airport Without Scheduled Services",
              "Airstrip",
              "Allotments",
              "Ambulance And Fire Station",
              "Ambulance And Police Station",
              "Ambulance Station",
              "Ambulance, Fire And Police Station",
              "Amenity And Open Space Site",
              "Amphitheatre",
              "Amusement And Show Place Site",
              "Amusement Park",
              "Animal Cemetery",
              "Animal Cemetery And Crematorium",
              "Animal Crematorium",
              "Animal Training Site",
              "Animal Treatment Site",
              "Animal Welfare Site",
              "Aquatic Animal Attraction",
              "Arboretum",
              "Art Gallery",
              "Art Gallery And Library",
              "Art Gallery And Library And Museum",
              "Art Gallery And Museum",
              "Arts Centre",
              "Arts Centre And Museum",
              "Athletics Ground",
              "Athletics Stadium",
              "Attraction Or Leisure Site",
              "Aviary",
              "Balancing Pond",
              "Beach",
              "Biogas Power Station",
              "Boat Building Site",
              "Boat Hire Site",
              "Boat Lift",
              "Boat Maintenance Or Storage Site",
              "Boating Site",
              "Botanical Garden",
              "Bothy",
              "Bowls Site",
              "Brewery",
              "Brick Works",
              "Buddhist Temple",
              "Burial Ground",
              "Bus Depot",
              "Bus Station",
              "Business Or Industrial Park",
              "Cable Terminal Station",
              "Camp Site",
              "Camping And Caravanning Site",
              "Car Cleaning Site",
              "Caravan Site",
              "Castle",
              "Cathedral",
              "Cattery",
              "Cattery And Kennels",
              "Cement Works",
              "Cemetery",
              "Cemetery And Crematorium",
              "Central Government Services",
              "Chapel",
              "Chapel Of Rest",
              "Chemical Works",
              "Children's Centre",
              "Children's Nursery",
              "Church",
              "Cider Factory",
              "Cinema",
              "Cliff Railway",
              "Climbing Hut",
              "Coach And Commercial Vehicle Park",
              "Coach Park",
              "Coach Station",
              "Coastguard Lookout",
              "College",
              "Commercial Fisheries",
              "Commercial Hostel",
              "Commercial Vehicle Park",
              "Commercial Vehicle Service Area",
              "Communal Residential Site",
              "Community Meeting Place",
              "Community Services",
              "Conference Or Exhibition Centre",
              "Construction Site",
              "Consulate",
              "Container Freight Terminal",
              "Cooling Station",
              "Crematorium",
              "Cricket Ground (Participation)",
              "Cricket Ground (Spectating)",
              "Cricket Stadium",
              "Crop Handling And Storage Site",
              "Curling Rink",
              "Customs Post",
              "Cycle Hire Station",
              "Cycling Sports Facility",
              "Dairy Processing Site",
              "Derelict Site",
              "Detention Centre",
              "Distillery",
              "Distribution Or Storage Site",
              "Docks",
              "Dry Dock",
              "Education Support Site",
              "Educational Field Study Centre",
              "Electricity Distribution Site",
              "Electricity Storage Site",
              "Electricity Sub Station",
              "Embassy",
              "Emergency Assistance Or Equipment Site",
              "Equestrian Sports Facility",
              "Farm Site",
              "Ferry Passenger Terminal",
              "Ferry Vehicular Terminal",
              "Ferry Vehicular Terminal (International)",
              "Filling Station",
              "Filling Station And Post Office",
              "Film Studio",
              "Fire Service Training Site",
              "Fire Station",
              "Fire Station And Police Station",
              "Fish Farm",
              "Fish Hatchery",
              "Fishing Lake",
              "Flood Or Water Controlling Site",
              "Flour Mill",
              "Folly",
              "Food Processing Site",
              "Football Ground (Participation)",
              "Football Ground (Spectating)",
              "Football Stadium",
              "Garden Centre",
              "Garden Of Rest",
              "Gas Distribution Or Storage Site",
              "Gas Extraction Site",
              "Gas Governor",
              "Gas Production Site",
              "Glassworks",
              "Gliding Area",
              "Go-Kart Track",
              "Golf Centre",
              "Golf Clubhouse",
              "Golf Course",
              "Golf Driving Range",
              "Greyhound Track Or Stadium",
              "Gurdwara",
              "Health Centre",
              "Heating Plant",
              "Helicopter Station",
              "Heliport",
              "High Commission",
              "Hill Carving",
              "Hindu Temple",
              "HM Coastguard Station",
              "Hockey Ground",
              "Holiday Accommodation",
              "Holiday Centre",
              "Horse Racing Course",
              "Horse Racing Facility",
              "Horse Racing Or Breeding Stables",
              "Horticulture",
              "Hospice",
              "Hospital",
              "Hotel",
              "Hydroelectric Power Generating",
              "Hydrogen Fuel Production And Supply",
              "Ice Rink",
              "Industry And Business Site",
              "Inshore Rescue Boat Station",
              "Kennels",
              "Kingdom Hall",
              "Knackery",
              "Law Court",
              "Leisure Or Sports Centre",
              "Library",
              "Library And Museum",
              "Lifeboat Station",
              "Light Rail Station",
              "Lighthouse",
              "Livestock Market",
              "Local Government Site",
              "Lock",
              "Manufacturing Site",
              "Marina",
              "Maze",
              "Medical Care Accommodation",
              "Medical Care Site",
              "Memorial",
              "Memorial Gardens",
              "Meteorological Station",
              "Military Accommodation Site",
              "Military Airfield",
              "Military Cemetery",
              "Military Docks",
              "Military Range",
              "Military Reserves Site",
              "Military Site",
              "Military Training Area",
              "Mine",
              "Mineral Distribution Or Storage Site",
              "Mineral Processing Site",
              "Minster",
              "Mixed Use Site",
              "Model Aircraft Flying Site",
              "Model Boating Site",
              "Model Car Racing Site",
              "Model Village",
              "Mortuary",
              "Mosque",
              "Motocross Circuit",
              "Motor Sport Site",
              "Multi-Purpose Community Site",
              "Museum",
              "Nautical Fuel Station",
              "Nautical Navigation Beacon",
              "Non Commercial Hostel",
              "Observatory",
              "Observing Station",
              "Oil Distribution Centre",
              "Oil Extraction Site",
              "Oil Refinery",
              "Oil Terminal",
              "Outdoor Activity Centre",
              "Paddling Pool",
              "Paper Mill",
              "Park And Ride Car Park",
              "Peat Cuttings",
              "Picnic Area",
              "Pitch And Putt Course",
              "Place Of Worship",
              "Play Area",
              "Playing Field",
              "Police Headquarters",
              "Police Station",
              "Police Support Site",
              "Post Office",
              "Pottery",
              "Pound",
              "Power Station",
              "Printing Works",
              "Prison",
              "Private Park Or Significant Garden",
              "Private Residential Site",
              "Professional Sports Training Ground",
              "Public Car And Coach Park",
              "Public Car And Commercial Vehicle Park",
              "Public Car Park",
              "Public Convenience",
              "Public House",
              "Public Park Or Garden",
              "Public Recycling Site",
              "Public Waste Disposal Site",
              "Pumping Station",
              "Pupil Referral Site",
              "Putting Green",
              "Quarry",
              "Racquet Sports Club",
              "Radar Station",
              "Rail Freight Transport",
              "Rail Maintenance Site",
              "Railway Station",
              "Railway Station (Not Publicly Accessible)",
              "Railway Station (Preserved Line)",
              "Railway Station (Principal)",
              "Railway Station (Underground System)",
              "Railway Stop (Amusement)",
              "Railway Stop (Funicular)",
              "Recreation Ground",
              "Recreational Or Social Club",
              "Recycling Site",
              "Religious Community Site",
              "Religious Meeting Place",
              "Research Site",
              "Retail Complex",
              "Retail Site",
              "Riding Stables",
              "Road Freight Site",
              "Road Maintenance Site",
              "Rowing Club",
              "Royal Palace",
              "Rugby Ground (Spectating)",
              "Rugby Pitch Or Ground (Participation)",
              "Rugby Stadium",
              "Sailing Centre",
              "Satellite Earth Station",
              "School",
              "Secure Residential Site",
              "Service Area",
              "Sheep Dip",
              "Shinty Site",
              "Ship Passenger Terminal",
              "Shipyard",
              "Shooting Lodge",
              "Shooting Range",
              "Showground",
              "Shrine",
              "Skateboard Park",
              "Ski Centre",
              "Slate Mining",
              "Smallholding",
              "Social Care Services Site",
              "Solar Power Site",
              "Solid Fuel Distribution Or Storage Site",
              "Speedway Track",
              "Sports Ground (Spectating)",
              "Sports Or Exercise Facility",
              "Sports Pavilion",
              "Sports Stadium",
              "Steel Works",
              "Stone Works",
              "Stupa",
              "Sugar Refinery",
              "Swimming Pool",
              "Synagogue",
              "Telecommunications Site",
              "Telephone Exchange",
              "Television Studio",
              "Tennis Site",
              "Tenpin Bowling Centre",
              "Theatre",
              "Tidal Power Station",
              "Timber Distribution Or Storage Site",
              "Timber Mill",
              "Tourist Attraction",
              "Tourist Information Centre",
              "Training Site",
              "Travellers Site",
              "Unclassified Site",
              "University",
              "University College",
              "University Halls Of Residence",
              "University School",
              "University Sports Or Exercise Facility",
              "University Support Site",
              "Vehicle Charging Site",
              "Vehicle Repair Garage",
              "Vehicle Testing Site",
              "Vehicular Rail Terminal",
              "Ventilating Station",
              "Visitor Information Centre",
              "War Memorial",
              "Waste Disposal Site",
              "Waste Incineration Site",
              "Waste Processing Site",
              "Waste Water Treatment Works",
              "Water Distribution Site",
              "Water Monitoring Station",
              "Water Sports Centre",
              "Water Treatment Site",
              "Weighbridge",
              "Wholesale Food Market",
              "Wildlife Observation Site",
              "Wildlife Or Zoological Park",
              "Wind Farm",
              "Winery",
              "Yacht Club",
              "Youth Hostel",
              "Youth Organisation Camp Site",
              "Youth Recreational Or Social Club"
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
          "nlud_code": {
            "type": [
              "string",
              "null"
            ]
          },
          "osid": {
            "format": "uuid",
            "type": [
              "string"
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
          "stakeholder": {
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
          "toid": {
            "type": [
              "string",
              "null"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "6f46eb76cc4c41036e90019a501c65e7c97d24c7de45cee0980bf0be62f2e3d6",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "lus-fts-site-2.3",
        "properties": {
          "address_classificationcode": {
            "type": [
              "string",
              "null"
            ]
          },
          "address_classificationcorrelation": {
            "enum": [
              "Good",
              "Acceptable",
              "Discrepancy"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "address_classificationsource": {
            "enum": [
              "Matched UPRN",
              "Child Address",
              "Multiple Addresses"
            ],
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
          "addresscount_commercial": {
            "type": "integer"
          },
          "addresscount_other": {
            "type": "integer"
          },
          "addresscount_residential": {
            "type": "integer"
          },
          "addresscount_total": {
            "type": "integer"
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
              "Abattoir",
              "Abbey",
              "Agriculture Services Site",
              "Air Freight Terminal",
              "Air Navigation Beacon",
              "Air Passenger Terminal",
              "Air Quality Monitoring Station",
              "Air Traffic Control Centre",
              "Air Transport Services Site",
              "Aircraft Works",
              "Airfield",
              "Airport With Scheduled Services",
              "Airport Without Scheduled Services",
              "Airstrip",
              "Allotments",
              "Ambulance And Fire Station",
              "Ambulance And Police Station",
              "Ambulance Station",
              "Ambulance, Fire And Police Station",
              "Amenity And Open Space Site",
              "Amphitheatre",
              "Amusement And Show Place Site",
              "Amusement Park",
              "Animal Cemetery",
              "Animal Cemetery And Crematorium",
              "Animal Crematorium",
              "Animal Training Site",
              "Animal Treatment Site",
              "Animal Welfare Site",
              "Aquatic Animal Attraction",
              "Arboretum",
              "Art Gallery",
              "Art Gallery And Library",
              "Art Gallery And Library And Museum",
              "Art Gallery And Museum",
              "Arts Centre",
              "Arts Centre And Museum",
              "Athletics Ground",
              "Athletics Stadium",
              "Attraction Or Leisure Site",
              "Aviary",
              "Balancing Pond",
              "Beach",
              "Biogas Power Station",
              "Boat Building Site",
              "Boat Hire Site",
              "Boat Lift",
              "Boat Maintenance Or Storage Site",
              "Boating Site",
              "Botanical Garden",
              "Bothy",
              "Bowls Site",
              "Brewery",
              "Brick Works",
              "Buddhist Temple",
              "Burial Ground",
              "Bus Depot",
              "Bus Station",
              "Business Or Industrial Park",
              "Cable Terminal Station",
              "Camp Site",
              "Camping And Caravanning Site",
              "Car Cleaning Site",
              "Caravan Site",
              "Castle",
              "Cathedral",
              "Cattery",
              "Cattery And Kennels",
              "Cement Works",
              "Cemetery",
              "Cemetery And Crematorium",
              "Central Government Services",
              "Chapel",
              "Chapel Of Rest",
              "Chemical Works",
              "Children's Centre",
              "Children's Nursery",
              "Church",
              "Cider Factory",
              "Cinema",
              "Cliff Railway",
              "Climbing Hut",
              "Coach And Commercial Vehicle Park",
              "Coach Park",
              "Coach Station",
              "Coastguard Lookout",
              "College",
              "Commercial Fisheries",
              "Commercial Hostel",
              "Commercial Vehicle Park",
              "Commercial Vehicle Service Area",
              "Communal Residential Site",
              "Community Meeting Place",
              "Community Services",
              "Conference Or Exhibition Centre",
              "Construction Site",
              "Consulate",
              "Container Freight Terminal",
              "Cooling Station",
              "Crematorium",
              "Cricket Ground (Participation)",
              "Cricket Ground (Spectating)",
              "Cricket Stadium",
              "Crop Handling And Storage Site",
              "Curling Rink",
              "Customs Post",
              "Cycle Hire Station",
              "Cycling Sports Facility",
              "Dairy Processing Site",
              "Derelict Site",
              "Detention Centre",
              "Distillery",
              "Distribution Or Storage Site",
              "Docks",
              "Dry Dock",
              "Education Support Site",
              "Educational Field Study Centre",
              "Electricity Distribution Site",
              "Electricity Storage Site",
              "Electricity Sub Station",
              "Embassy",
              "Emergency Assistance Or Equipment Site",
              "Equestrian Sports Facility",
              "Farm Site",
              "Ferry Passenger Terminal",
              "Ferry Vehicular Terminal",
              "Ferry Vehicular Terminal (International)",
              "Filling Station",
              "Filling Station And Post Office",
              "Film Studio",
              "Fire Service Training Site",
              "Fire Station",
              "Fire Station And Police Station",
              "Fish Farm",
              "Fish Hatchery",
              "Fishing Lake",
              "Flood Or Water Controlling Site",
              "Flour Mill",
              "Folly",
              "Food Processing Site",
              "Football Ground (Participation)",
              "Football Ground (Spectating)",
              "Football Stadium",
              "Garden Centre",
              "Garden Of Rest",
              "Gas Distribution Or Storage Site",
              "Gas Extraction Site",
              "Gas Governor",
              "Gas Production Site",
              "Glassworks",
              "Gliding Area",
              "Go-Kart Track",
              "Golf Centre",
              "Golf Clubhouse",
              "Golf Course",
              "Golf Driving Range",
              "Greyhound Track Or Stadium",
              "Gurdwara",
              "Health Centre",
              "Heating Plant",
              "Helicopter Station",
              "Heliport",
              "High Commission",
              "Hill Carving",
              "Hindu Temple",
              "HM Coastguard Station",
              "Hockey Ground",
              "Holiday Accommodation",
              "Holiday Centre",
              "Horse Racing Course",
              "Horse Racing Facility",
              "Horse Racing Or Breeding Stables",
              "Horticulture",
              "Hospice",
              "Hospital",
              "Hotel",
              "Hydroelectric Power Generating",
              "Hydrogen Fuel Production And Supply",
              "Ice Rink",
              "Industry And Business Site",
              "Inshore Rescue Boat Station",
              "Kennels",
              "Kingdom Hall",
              "Knackery",
              "Law Court",
              "Leisure Or Sports Centre",
              "Library",
              "Library And Museum",
              "Lifeboat Station",
              "Light Rail Station",
              "Lighthouse",
              "Livestock Market",
              "Local Government Site",
              "Lock",
              "Manufacturing Site",
              "Marina",
              "Maze",
              "Medical Care Accommodation",
              "Medical Care Site",
              "Memorial",
              "Memorial Gardens",
              "Meteorological Station",
              "Military Accommodation Site",
              "Military Airfield",
              "Military Cemetery",
              "Military Docks",
              "Military Range",
              "Military Reserves Site",
              "Military Site",
              "Military Training Area",
              "Mine",
              "Mineral Distribution Or Storage Site",
              "Mineral Processing Site",
              "Minster",
              "Mixed Use Site",
              "Model Aircraft Flying Site",
              "Model Boating Site",
              "Model Car Racing Site",
              "Model Village",
              "Mortuary",
              "Mosque",
              "Motocross Circuit",
              "Motor Sport Site",
              "Multi-Purpose Community Site",
              "Museum",
              "Nautical Fuel Station",
              "Nautical Navigation Beacon",
              "Non Commercial Hostel",
              "Observatory",
              "Observing Station",
              "Oil Distribution Centre",
              "Oil Extraction Site",
              "Oil Refinery",
              "Oil Terminal",
              "Outdoor Activity Centre",
              "Paddling Pool",
              "Paper Mill",
              "Park And Ride Car Park",
              "Peat Cuttings",
              "Picnic Area",
              "Pitch And Putt Course",
              "Place Of Worship",
              "Play Area",
              "Playing Field",
              "Police Headquarters",
              "Police Station",
              "Police Support Site",
              "Post Office",
              "Pottery",
              "Pound",
              "Power Station",
              "Printing Works",
              "Prison",
              "Private Park Or Significant Garden",
              "Private Residential Site",
              "Professional Sports Training Ground",
              "Public Car And Coach Park",
              "Public Car And Commercial Vehicle Park",
              "Public Car Park",
              "Public Convenience",
              "Public House",
              "Public Park Or Garden",
              "Public Recycling Site",
              "Public Waste Disposal Site",
              "Pumping Station",
              "Pupil Referral Site",
              "Putting Green",
              "Quarry",
              "Racquet Sports Club",
              "Radar Station",
              "Rail Freight Transport",
              "Rail Maintenance Site",
              "Railway Station",
              "Railway Station (Not Publicly Accessible)",
              "Railway Station (Preserved Line)",
              "Railway Station (Principal)",
              "Railway Station (Underground System)",
              "Railway Stop (Amusement)",
              "Railway Stop (Funicular)",
              "Recreation Ground",
              "Recreational Or Social Club",
              "Recycling Site",
              "Religious Community Site",
              "Religious Meeting Place",
              "Research Site",
              "Retail Complex",
              "Retail Site",
              "Riding Stables",
              "Road Freight Site",
              "Road Maintenance Site",
              "Rowing Club",
              "Royal Palace",
              "Rugby Ground (Spectating)",
              "Rugby Pitch Or Ground (Participation)",
              "Rugby Stadium",
              "Sailing Centre",
              "Satellite Earth Station",
              "School",
              "Secure Residential Site",
              "Service Area",
              "Sheep Dip",
              "Shinty Site",
              "Ship Passenger Terminal",
              "Shipyard",
              "Shooting Lodge",
              "Shooting Range",
              "Showground",
              "Shrine",
              "Skateboard Park",
              "Ski Centre",
              "Slate Mining",
              "Smallholding",
              "Social Care Services Site",
              "Solar Power Site",
              "Solid Fuel Distribution Or Storage Site",
              "Speedway Track",
              "Sports Ground (Spectating)",
              "Sports Or Exercise Facility",
              "Sports Pavilion",
              "Sports Stadium",
              "Steel Works",
              "Stone Works",
              "Stupa",
              "Sugar Refinery",
              "Swimming Pool",
              "Synagogue",
              "Telecommunications Site",
              "Telephone Exchange",
              "Television Studio",
              "Tennis Site",
              "Tenpin Bowling Centre",
              "Theatre",
              "Tidal Power Station",
              "Timber Distribution Or Storage Site",
              "Timber Mill",
              "Tourist Attraction",
              "Tourist Information Centre",
              "Training Site",
              "Travellers Site",
              "Unclassified Site",
              "University",
              "University College",
              "University Halls Of Residence",
              "University School",
              "University Sports Or Exercise Facility",
              "University Support Site",
              "Vehicle Charging Site",
              "Vehicle Repair Garage",
              "Vehicle Testing Site",
              "Vehicular Rail Terminal",
              "Ventilating Station",
              "Visitor Information Centre",
              "War Memorial",
              "Waste Disposal Site",
              "Waste Incineration Site",
              "Waste Processing Site",
              "Waste Water Treatment Works",
              "Water Distribution Site",
              "Water Monitoring Station",
              "Water Sports Centre",
              "Water Treatment Site",
              "Weighbridge",
              "Wholesale Food Market",
              "Wildlife Observation Site",
              "Wildlife Or Zoological Park",
              "Wind Farm",
              "Winery",
              "Yacht Club",
              "Youth Hostel",
              "Youth Organisation Camp Site",
              "Youth Recreational Or Social Club"
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
          "extentdefinition": {
            "enum": [
              "Auto-Defined Complete",
              "Manually Defined Complete",
              "Manually Defined Incomplete"
            ],
            "type": "string"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/MultiPolygon.json",
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
          "mainbuildingid": {
            "type": [
              "string",
              "null"
            ]
          },
          "matcheduprn": {
            "type": [
              "number",
              "null"
            ]
          },
          "matcheduprn_method": {
            "enum": [
              "Matched Using Single Address",
              "Matched Using Single Non-parent Address",
              "Matched Using Classification",
              "Matched Using Hierarchy",
              "Matched Using Override"
            ],
            "type": [
              "string",
              "null"
            ]
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
          "sitetoaddressreference": {
            "items": {
              "properties": {
                "relationshiptype": {
                  "description": "The type of relationship that has been formed between the source and target features, for example, Within or Same As.",
                  "enum": [
                    "Within",
                    "Same As",
                    "Accessed From",
                    "Nearest"
                  ],
                  "maxLength": 30,
                  "originalName": "relationshipType",
                  "type": "string"
                },
                "siteid": {
                  "description": "The identifier for the Site feature.",
                  "format": "uuid",
                  "maxLength": 36,
                  "originalName": "siteID",
                  "type": "string"
                },
                "siteversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "siteVersionDate",
                  "type": "string"
                },
                "uprn": {
                  "description": "Unique Property Reference Number (UPRN) of the Address features that lie within the extent of the Site geometry.",
                  "originalName": "uprn",
                  "type": "number"
                }
              },
              "type": "object"
            },
            "type": "array"
          },
          "stakeholder": {
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
          "oslandusetiera",
          "oslandusetierb",
          "oslanduse_evidencedate",
          "oslanduse_updatedate",
          "oslanduse_capturemethod",
          "stakeholder",
          "name1_text",
          "name1_language",
          "name1_evidencedate",
          "name1_updatedate",
          "name2_text",
          "name2_language",
          "name2_evidencedate",
          "name2_updatedate",
          "extentdefinition",
          "matcheduprn",
          "matcheduprn_method",
          "address_classificationcode",
          "address_classificationcorrelation",
          "address_classificationsource",
          "address_primarydescription",
          "address_secondarydescription",
          "addresscount_total",
          "addresscount_residential",
          "addresscount_commercial",
          "addresscount_other",
          "nlud_code",
          "nlud_orderdescription",
          "nlud_groupdescription",
          "mainbuildingid",
          "status",
          "status_updateDate",
          "sitetoaddressreference"
        ],
        "requiredUndeclared": [
          "status_updateDate"
        ],
        "sha256": "c1cabddc6bc9e073f168979fcc88815b305da71b75db3819a9dd8c0c16af06e5",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Site v2"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2024-09-07T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/queryables",
      "responseSha256": "6f46eb76cc4c41036e90019a501c65e7c97d24c7de45cee0980bf0be62f2e3d6",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema",
      "responseSha256": "c1cabddc6bc9e073f168979fcc88815b305da71b75db3819a9dd8c0c16af06e5",
      "requiredUndeclared": [
        "status_updateDate"
      ]
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/address_classificationcode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/address_classificationcorrelation",
      "@type": "rdf:Property",
      "dcterms:identifier": "address_classificationcorrelation",
      "rdfs:label": "address_classificationcorrelation",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Good",
            "Acceptable",
            "Discrepancy"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/address_classificationsource",
      "@type": "rdf:Property",
      "dcterms:identifier": "address_classificationsource",
      "rdfs:label": "address_classificationsource",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Matched UPRN",
            "Child Address",
            "Multiple Addresses"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/address_primarydescription",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/address_secondarydescription",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/addresscount_commercial",
      "@type": "rdf:Property",
      "dcterms:identifier": "addresscount_commercial",
      "rdfs:label": "addresscount_commercial",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/addresscount_other",
      "@type": "rdf:Property",
      "dcterms:identifier": "addresscount_other",
      "rdfs:label": "addresscount_other",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/addresscount_residential",
      "@type": "rdf:Property",
      "dcterms:identifier": "addresscount_residential",
      "rdfs:label": "addresscount_residential",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/addresscount_total",
      "@type": "rdf:Property",
      "dcterms:identifier": "addresscount_total",
      "rdfs:label": "addresscount_total",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Abattoir",
            "Abbey",
            "Agriculture Services Site",
            "Air Freight Terminal",
            "Air Navigation Beacon",
            "Air Passenger Terminal",
            "Air Quality Monitoring Station",
            "Air Traffic Control Centre",
            "Air Transport Services Site",
            "Aircraft Works",
            "Airfield",
            "Airport With Scheduled Services",
            "Airport Without Scheduled Services",
            "Airstrip",
            "Allotments",
            "Ambulance And Fire Station",
            "Ambulance And Police Station",
            "Ambulance Station",
            "Ambulance, Fire And Police Station",
            "Amenity And Open Space Site",
            "Amphitheatre",
            "Amusement And Show Place Site",
            "Amusement Park",
            "Animal Cemetery",
            "Animal Cemetery And Crematorium",
            "Animal Crematorium",
            "Animal Training Site",
            "Animal Treatment Site",
            "Animal Welfare Site",
            "Aquatic Animal Attraction",
            "Arboretum",
            "Art Gallery",
            "Art Gallery And Library",
            "Art Gallery And Library And Museum",
            "Art Gallery And Museum",
            "Arts Centre",
            "Arts Centre And Museum",
            "Athletics Ground",
            "Athletics Stadium",
            "Attraction Or Leisure Site",
            "Aviary",
            "Balancing Pond",
            "Beach",
            "Biogas Power Station",
            "Boat Building Site",
            "Boat Hire Site",
            "Boat Lift",
            "Boat Maintenance Or Storage Site",
            "Boating Site",
            "Botanical Garden",
            "Bothy",
            "Bowls Site",
            "Brewery",
            "Brick Works",
            "Buddhist Temple",
            "Burial Ground",
            "Bus Depot",
            "Bus Station",
            "Business Or Industrial Park",
            "Cable Terminal Station",
            "Camp Site",
            "Camping And Caravanning Site",
            "Car Cleaning Site",
            "Caravan Site",
            "Castle",
            "Cathedral",
            "Cattery",
            "Cattery And Kennels",
            "Cement Works",
            "Cemetery",
            "Cemetery And Crematorium",
            "Central Government Services",
            "Chapel",
            "Chapel Of Rest",
            "Chemical Works",
            "Children's Centre",
            "Children's Nursery",
            "Church",
            "Cider Factory",
            "Cinema",
            "Cliff Railway",
            "Climbing Hut",
            "Coach And Commercial Vehicle Park",
            "Coach Park",
            "Coach Station",
            "Coastguard Lookout",
            "College",
            "Commercial Fisheries",
            "Commercial Hostel",
            "Commercial Vehicle Park",
            "Commercial Vehicle Service Area",
            "Communal Residential Site",
            "Community Meeting Place",
            "Community Services",
            "Conference Or Exhibition Centre",
            "Construction Site",
            "Consulate",
            "Container Freight Terminal",
            "Cooling Station",
            "Crematorium",
            "Cricket Ground (Participation)",
            "Cricket Ground (Spectating)",
            "Cricket Stadium",
            "Crop Handling And Storage Site",
            "Curling Rink",
            "Customs Post",
            "Cycle Hire Station",
            "Cycling Sports Facility",
            "Dairy Processing Site",
            "Derelict Site",
            "Detention Centre",
            "Distillery",
            "Distribution Or Storage Site",
            "Docks",
            "Dry Dock",
            "Education Support Site",
            "Educational Field Study Centre",
            "Electricity Distribution Site",
            "Electricity Storage Site",
            "Electricity Sub Station",
            "Embassy",
            "Emergency Assistance Or Equipment Site",
            "Equestrian Sports Facility",
            "Farm Site",
            "Ferry Passenger Terminal",
            "Ferry Vehicular Terminal",
            "Ferry Vehicular Terminal (International)",
            "Filling Station",
            "Filling Station And Post Office",
            "Film Studio",
            "Fire Service Training Site",
            "Fire Station",
            "Fire Station And Police Station",
            "Fish Farm",
            "Fish Hatchery",
            "Fishing Lake",
            "Flood Or Water Controlling Site",
            "Flour Mill",
            "Folly",
            "Food Processing Site",
            "Football Ground (Participation)",
            "Football Ground (Spectating)",
            "Football Stadium",
            "Garden Centre",
            "Garden Of Rest",
            "Gas Distribution Or Storage Site",
            "Gas Extraction Site",
            "Gas Governor",
            "Gas Production Site",
            "Glassworks",
            "Gliding Area",
            "Go-Kart Track",
            "Golf Centre",
            "Golf Clubhouse",
            "Golf Course",
            "Golf Driving Range",
            "Greyhound Track Or Stadium",
            "Gurdwara",
            "Health Centre",
            "Heating Plant",
            "Helicopter Station",
            "Heliport",
            "High Commission",
            "Hill Carving",
            "Hindu Temple",
            "HM Coastguard Station",
            "Hockey Ground",
            "Holiday Accommodation",
            "Holiday Centre",
            "Horse Racing Course",
            "Horse Racing Facility",
            "Horse Racing Or Breeding Stables",
            "Horticulture",
            "Hospice",
            "Hospital",
            "Hotel",
            "Hydroelectric Power Generating",
            "Hydrogen Fuel Production And Supply",
            "Ice Rink",
            "Industry And Business Site",
            "Inshore Rescue Boat Station",
            "Kennels",
            "Kingdom Hall",
            "Knackery",
            "Law Court",
            "Leisure Or Sports Centre",
            "Library",
            "Library And Museum",
            "Lifeboat Station",
            "Light Rail Station",
            "Lighthouse",
            "Livestock Market",
            "Local Government Site",
            "Lock",
            "Manufacturing Site",
            "Marina",
            "Maze",
            "Medical Care Accommodation",
            "Medical Care Site",
            "Memorial",
            "Memorial Gardens",
            "Meteorological Station",
            "Military Accommodation Site",
            "Military Airfield",
            "Military Cemetery",
            "Military Docks",
            "Military Range",
            "Military Reserves Site",
            "Military Site",
            "Military Training Area",
            "Mine",
            "Mineral Distribution Or Storage Site",
            "Mineral Processing Site",
            "Minster",
            "Mixed Use Site",
            "Model Aircraft Flying Site",
            "Model Boating Site",
            "Model Car Racing Site",
            "Model Village",
            "Mortuary",
            "Mosque",
            "Motocross Circuit",
            "Motor Sport Site",
            "Multi-Purpose Community Site",
            "Museum",
            "Nautical Fuel Station",
            "Nautical Navigation Beacon",
            "Non Commercial Hostel",
            "Observatory",
            "Observing Station",
            "Oil Distribution Centre",
            "Oil Extraction Site",
            "Oil Refinery",
            "Oil Terminal",
            "Outdoor Activity Centre",
            "Paddling Pool",
            "Paper Mill",
            "Park And Ride Car Park",
            "Peat Cuttings",
            "Picnic Area",
            "Pitch And Putt Course",
            "Place Of Worship",
            "Play Area",
            "Playing Field",
            "Police Headquarters",
            "Police Station",
            "Police Support Site",
            "Post Office",
            "Pottery",
            "Pound",
            "Power Station",
            "Printing Works",
            "Prison",
            "Private Park Or Significant Garden",
            "Private Residential Site",
            "Professional Sports Training Ground",
            "Public Car And Coach Park",
            "Public Car And Commercial Vehicle Park",
            "Public Car Park",
            "Public Convenience",
            "Public House",
            "Public Park Or Garden",
            "Public Recycling Site",
            "Public Waste Disposal Site",
            "Pumping Station",
            "Pupil Referral Site",
            "Putting Green",
            "Quarry",
            "Racquet Sports Club",
            "Radar Station",
            "Rail Freight Transport",
            "Rail Maintenance Site",
            "Railway Station",
            "Railway Station (Not Publicly Accessible)",
            "Railway Station (Preserved Line)",
            "Railway Station (Principal)",
            "Railway Station (Underground System)",
            "Railway Stop (Amusement)",
            "Railway Stop (Funicular)",
            "Recreation Ground",
            "Recreational Or Social Club",
            "Recycling Site",
            "Religious Community Site",
            "Religious Meeting Place",
            "Research Site",
            "Retail Complex",
            "Retail Site",
            "Riding Stables",
            "Road Freight Site",
            "Road Maintenance Site",
            "Rowing Club",
            "Royal Palace",
            "Rugby Ground (Spectating)",
            "Rugby Pitch Or Ground (Participation)",
            "Rugby Stadium",
            "Sailing Centre",
            "Satellite Earth Station",
            "School",
            "Secure Residential Site",
            "Service Area",
            "Sheep Dip",
            "Shinty Site",
            "Ship Passenger Terminal",
            "Shipyard",
            "Shooting Lodge",
            "Shooting Range",
            "Showground",
            "Shrine",
            "Skateboard Park",
            "Ski Centre",
            "Slate Mining",
            "Smallholding",
            "Social Care Services Site",
            "Solar Power Site",
            "Solid Fuel Distribution Or Storage Site",
            "Speedway Track",
            "Sports Ground (Spectating)",
            "Sports Or Exercise Facility",
            "Sports Pavilion",
            "Sports Stadium",
            "Steel Works",
            "Stone Works",
            "Stupa",
            "Sugar Refinery",
            "Swimming Pool",
            "Synagogue",
            "Telecommunications Site",
            "Telephone Exchange",
            "Television Studio",
            "Tennis Site",
            "Tenpin Bowling Centre",
            "Theatre",
            "Tidal Power Station",
            "Timber Distribution Or Storage Site",
            "Timber Mill",
            "Tourist Attraction",
            "Tourist Information Centre",
            "Training Site",
            "Travellers Site",
            "Unclassified Site",
            "University",
            "University College",
            "University Halls Of Residence",
            "University School",
            "University Sports Or Exercise Facility",
            "University Support Site",
            "Vehicle Charging Site",
            "Vehicle Repair Garage",
            "Vehicle Testing Site",
            "Vehicular Rail Terminal",
            "Ventilating Station",
            "Visitor Information Centre",
            "War Memorial",
            "Waste Disposal Site",
            "Waste Incineration Site",
            "Waste Processing Site",
            "Waste Water Treatment Works",
            "Water Distribution Site",
            "Water Monitoring Station",
            "Water Sports Centre",
            "Water Treatment Site",
            "Weighbridge",
            "Wholesale Food Market",
            "Wildlife Observation Site",
            "Wildlife Or Zoological Park",
            "Wind Farm",
            "Winery",
            "Yacht Club",
            "Youth Hostel",
            "Youth Organisation Camp Site",
            "Youth Recreational Or Social Club"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/description_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/description_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/description_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/extentdefinition",
      "@type": "rdf:Property",
      "dcterms:identifier": "extentdefinition",
      "rdfs:label": "extentdefinition",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Auto-Defined Complete",
            "Manually Defined Complete",
            "Manually Defined Incomplete"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/geometry",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry",
      "rdfs:label": "geometry",
      "okfp:schemaDefinition": {
        "@value": {
          "$ref": "https://geojson.org/schema/MultiPolygon.json",
          "type": "object"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/geometry_area_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/geometry_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/geometry_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/geometry_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/mainbuildingid",
      "@type": "rdf:Property",
      "dcterms:identifier": "mainbuildingid",
      "rdfs:label": "mainbuildingid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/matcheduprn",
      "@type": "rdf:Property",
      "dcterms:identifier": "matcheduprn",
      "rdfs:label": "matcheduprn",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/matcheduprn_method",
      "@type": "rdf:Property",
      "dcterms:identifier": "matcheduprn_method",
      "rdfs:label": "matcheduprn_method",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Matched Using Single Address",
            "Matched Using Single Non-parent Address",
            "Matched Using Classification",
            "Matched Using Hierarchy",
            "Matched Using Override"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/name1_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/name1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/name1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/name1_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/name2_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/name2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/name2_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/nlud_code",
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
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/nlud_groupdescription",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/nlud_orderdescription",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/oslanduse_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/oslanduse_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/oslanduse_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/oslandusetiera",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/oslandusetierb",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/sitetoaddressreference",
      "@type": "rdf:Property",
      "dcterms:identifier": "sitetoaddressreference",
      "rdfs:label": "sitetoaddressreference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "relationshiptype": {
                "description": "The type of relationship that has been formed between the source and target features, for example, Within or Same As.",
                "enum": [
                  "Within",
                  "Same As",
                  "Accessed From",
                  "Nearest"
                ],
                "maxLength": 30,
                "originalName": "relationshipType",
                "type": "string"
              },
              "siteid": {
                "description": "The identifier for the Site feature.",
                "format": "uuid",
                "maxLength": 36,
                "originalName": "siteID",
                "type": "string"
              },
              "siteversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "siteVersionDate",
                "type": "string"
              },
              "uprn": {
                "description": "Unique Property Reference Number (UPRN) of the Address features that lie within the extent of the Site geometry.",
                "originalName": "uprn",
                "type": "number"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/stakeholder",
      "@type": "rdf:Property",
      "dcterms:identifier": "stakeholder",
      "rdfs:label": "stakeholder",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/status",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/status_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/toid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/lus-fts-site-2/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2/schema"
      }
    }
  ]
}
---

# Site v2

Polygon feature which represents the recognisable extent of certain types of function or activity. Examples include a caravan site, a university, and a railway centre.

Native identifier: `lus-fts-site-2`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/lus-fts-site-2)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2024-09-07T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
