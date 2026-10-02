---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Building v4",
  "description": "A new building geometry which represents a single building footprint. This geometry consists of adjoining building parts which have been determined to be part of the same building. When contained in a Land Use Site, adjoining building parts will be represented by a single feature.",
  "nativeIdentifier": "bld-fts-building-4",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "OS NGD",
    "bld",
    "schema",
    "queryables"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections",
      "retrievedAt": "2026-10-02T01:18:50.822323Z",
      "responseSha256": "cf6f9c7670533ff42c64af98a8f7bb8aa60911463d937623a4fc6f5bb8767de9",
      "sourcePointer": "/collections/5",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/5",
      "normalisedRecordSha256": "00f57103edf63547caf4d24c884d0d66f9dbd2264e03ab495584be68a1f8aa00",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4"
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
    "start": "2025-03-12T00:00:00Z",
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
    "description": "A new building geometry which represents a single building footprint. This geometry consists of adjoining building parts which have been determined to be part of the same building. When contained in a Land Use Site, adjoining building parts will be represented by a single feature.",
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
            "2025-03-12T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "bld-fts-building-4",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4",
        "rel": "self",
        "title": "The 'Building v4' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/items",
        "rel": "items",
        "title": "The features in the 'Building v4' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema",
        "rel": "describedby",
        "title": "Schema for the 'Building v4' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Building v4' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/queryables",
        "properties": {
          "basementpresence": {
            "enum": [
              "Present",
              "Not Present",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "basementpresence_selfcontained": {
            "enum": [
              "Present",
              "Not Present",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "buildingage_period": {
            "enum": [
              "Pre-1837",
              "Pre-1919",
              "1837-1869",
              "1870-1918",
              "1919-1944",
              "1945-1959",
              "1960-1979",
              "1980-1989",
              "1990-1999",
              "2000-2009",
              "2010-2019",
              "2020-2029",
              "2030-2039",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "buildingage_year": {
            "type": [
              "integer",
              "null"
            ]
          },
          "buildinguse": {
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
              "Unknown",
              "Unknown Use",
              "Utility Or Environmental Protection"
            ],
            "type": [
              "string"
            ]
          },
          "buildinguse_oslandusetiera": {
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
          "connectivity": {
            "enum": [
              "End-Connected",
              "Multi-Connected",
              "Semi-Connected",
              "Standalone"
            ],
            "type": [
              "string"
            ]
          },
          "constructionmaterial": {
            "enum": [
              "Brick Or Block Or Stone",
              "Concrete",
              "Mixed (Masonry And Metal)",
              "Mixed (Masonry And Timber)",
              "Mixed (Plaster And Timber)",
              "Other Artificial Material (Not Concrete)",
              "Other Non-Standard Or System Build",
              "Static Caravan Or Mobile Home",
              "Metal",
              "Timber Or Wood",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "description": {
            "enum": [
              "Abbey",
              "Agriculture Building",
              "Air Passenger Terminal",
              "Air Quality Monitoring Station",
              "Airport With Scheduled Services",
              "Airport Without Scheduled Services",
              "Ambulance And Fire Station",
              "Ambulance And Police Station",
              "Ambulance Station",
              "Ambulance, Fire And Police Station",
              "Ancillary Building",
              "Art Gallery",
              "Arts Centre",
              "Arts Centre And Museum",
              "Athletics Ground",
              "Athletics Stadium",
              "Attraction Building",
              "Biogas Power Station",
              "Bowls Clubhouse",
              "Buddhist Temple",
              "Building Under Construction",
              "Cable Terminal Station",
              "Cathedral",
              "Central Government Services",
              "Chapel",
              "Children's Nursery",
              "Church",
              "Cinema",
              "Coastguard Lookout",
              "College",
              "Commercial Building",
              "Community Building",
              "Community Meeting Place",
              "Community Services",
              "Construction Building",
              "Crematorium",
              "Cricket Ground (Participation)",
              "Cricket Ground (Spectating)",
              "Cricket Stadium",
              "Curling Rink",
              "Cycling Sports Facility",
              "Defence Building",
              "Detached House",
              "Detention Centre",
              "Domestic Outbuilding",
              "Education Building",
              "Electricity Distribution Facility",
              "Electricity Storage Facility",
              "Electricity Sub Station",
              "Emergency Assistance Or Equipment Facility",
              "End-Of-Terrace House",
              "Ferry Passenger Terminal",
              "Ferry Vehicular Terminal",
              "Ferry Vehicular Terminal (International)",
              "Fire Station",
              "Fire Station And Police Station",
              "Football Ground (Participation)",
              "Football Ground (Spectating)",
              "Football Stadium",
              "Gas Distribution Or Storage Facility",
              "Gas Governor",
              "Gas Production Facility",
              "Golf Centre",
              "Golf Clubhouse",
              "Golf Course",
              "Golf Driving Range",
              "Government Building",
              "Greyhound Track Or Stadium",
              "Gurdwara",
              "Health Centre",
              "Heating Plant",
              "Heliport",
              "Hindu Temple",
              "Historic Building",
              "HM Coastguard Station",
              "Hockey Ground",
              "Horse Racing Course",
              "Hospice",
              "Hospital",
              "Hydroelectric Power Generating",
              "Hydrogen Fuel Production And Supply",
              "Ice Rink",
              "Inshore Rescue Boat Station",
              "Kingdom Hall",
              "Law Court",
              "Leisure Or Sports Centre",
              "Library",
              "Library And Museum",
              "Lifeboat Station",
              "Light Rail Station",
              "Local Government Facility",
              "Medical Building",
              "Medical Care Facility",
              "Mid-Terrace House",
              "Minster",
              "Mixed Use Building",
              "Mosque",
              "Multi-Purpose Community Centre",
              "Multiple Residential Accommodation",
              "Museum",
              "Place Of Worship",
              "Police Headquarters",
              "Police Station",
              "Police Support Facility",
              "Power Station",
              "Prison",
              "Pumping Station",
              "Pupil Referral Centre",
              "Racquet Sports Club",
              "Railway Station",
              "Railway Station (Not Publicly Accessible)",
              "Railway Station (Principal)",
              "Railway Station (Underground System)",
              "Religious Meeting Place",
              "Residential Building",
              "Rowing Club",
              "Rugby Ground (Spectating)",
              "Rugby Pitch Or Ground (Participation)",
              "Rugby Stadium",
              "Sailing Centre",
              "School",
              "Secure Residential Unit",
              "Semi-Detached House",
              "Solar Power Facility",
              "Speedway Track",
              "Sports Building",
              "Sports Ground (Spectating)",
              "Sports Or Exercise Facility",
              "Sports Pavilion",
              "Sports Stadium",
              "Static Caravan Or Mobile Home",
              "Stupa",
              "Swimming Pool",
              "Synagogue",
              "Telecommunications Facility",
              "Telephone Exchange",
              "Temporary Or Holiday Accommodation Building",
              "Tennis Centre",
              "Theatre",
              "Tidal Power Station",
              "Transport Building",
              "University",
              "University College",
              "University School",
              "University Sports Or Exercise Facility",
              "Unknown Building",
              "Utility Building",
              "Waste Water Treatment Works",
              "Water Distribution Facility",
              "Water Sports Centre",
              "Water Treatment Facility",
              "Wildlife Or Zoological Park",
              "Yacht Club"
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
          "height_absolutemax_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "height_absolutemin_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "height_absoluteroofbase_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "height_relativemax_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "height_relativeroofbase_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "mainbuildingid": {
            "type": [
              "string",
              "null"
            ]
          },
          "mainbuildingid_ismainbuilding": {
            "enum": [
              "Yes",
              "No"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "numberoffloors": {
            "type": [
              "integer",
              "null"
            ]
          },
          "osid": {
            "format": "uuid",
            "type": [
              "string"
            ]
          },
          "physicalstate": {
            "enum": [
              "Built",
              "Derelict",
              "Under Construction"
            ],
            "type": [
              "string"
            ]
          },
          "roofmaterial_greenroofpresence": {
            "enum": [
              "Present",
              "Not Present",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roofmaterial_primarymaterial": {
            "enum": [
              "Fabric",
              "Glass Or Polycarbonate",
              "Green Roof",
              "Metal",
              "Mixed",
              "Other",
              "Thatch",
              "Tile Or Stone Or Slate",
              "Unknown",
              "Waterproof Membrane Or Concrete"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roofmaterial_solarpanelpresence": {
            "enum": [
              "Present",
              "Not Present",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roofshapeaspect_shape": {
            "enum": [
              "Flat",
              "Mixed",
              "Pitched",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "1a204d0c47eace06fa87342386ae342777d44afd472bfd1143f53cc20c5e7100",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "bld-fts-building-4.1",
        "properties": {
          "basementpresence": {
            "enum": [
              "Present",
              "Not Present",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "basementpresence_capturemethod": {
            "enum": [
              "Automated Process",
              "Default Value",
              "Desk-Based",
              "Field Survey",
              "Remote Sensing Survey",
              "Sensor Measurement",
              "Third Party Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "basementpresence_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "basementpresence_selfcontained": {
            "enum": [
              "Present",
              "Not Present",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "basementpresence_source": {
            "enum": [
              "Address Authority",
              "Ordnance Survey",
              "Verisk"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "basementpresence_thirdpartyprovenance": {
            "type": [
              "string",
              "null"
            ]
          },
          "basementpresence_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "buildingage_capturemethod": {
            "enum": [
              "Automated Process",
              "Default Value",
              "Desk-Based",
              "Field Survey",
              "Remote Sensing Survey",
              "Sensor Measurement",
              "Third Party Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "buildingage_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "buildingage_period": {
            "enum": [
              "Pre-1837",
              "Pre-1919",
              "1837-1869",
              "1870-1918",
              "1919-1944",
              "1945-1959",
              "1960-1979",
              "1980-1989",
              "1990-1999",
              "2000-2009",
              "2010-2019",
              "2020-2029",
              "2030-2039",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "buildingage_source": {
            "enum": [
              "Ordnance Survey",
              "Verisk"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "buildingage_thirdpartyprovenance": {
            "type": [
              "string",
              "null"
            ]
          },
          "buildingage_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "buildingage_year": {
            "type": [
              "integer",
              "null"
            ]
          },
          "buildingpartcount": {
            "type": "integer"
          },
          "buildingpartreference": {
            "items": {
              "properties": {
                "buildingid": {
                  "description": "The identifier of the Building.",
                  "format": "uuid",
                  "maxLength": 36,
                  "originalName": "buildingID",
                  "type": "string"
                },
                "buildingpartid": {
                  "description": "The identifier of the Building Part the Building is created from.",
                  "format": "uuid",
                  "maxLength": 36,
                  "originalName": "buidingPartID",
                  "type": "string"
                },
                "buildingversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "buildingVersionDate",
                  "type": "string"
                }
              },
              "type": "object"
            },
            "type": "array"
          },
          "buildinguse": {
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
              "Unknown",
              "Unknown Use",
              "Utility Or Environmental Protection"
            ],
            "type": "string"
          },
          "buildinguse_addresscount_commercial": {
            "type": "integer"
          },
          "buildinguse_addresscount_other": {
            "type": "integer"
          },
          "buildinguse_addresscount_residential": {
            "type": "integer"
          },
          "buildinguse_addresscount_total": {
            "type": "integer"
          },
          "buildinguse_oslandusetiera": {
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
          "buildinguse_updatedate": {
            "format": "date",
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
          "connectivity": {
            "enum": [
              "End-Connected",
              "Multi-Connected",
              "Semi-Connected",
              "Standalone"
            ],
            "type": "string"
          },
          "connectivity_count": {
            "type": "integer"
          },
          "connectivity_updatedate": {
            "format": "date",
            "type": "string"
          },
          "constructionmaterial": {
            "enum": [
              "Brick Or Block Or Stone",
              "Concrete",
              "Mixed (Masonry And Metal)",
              "Mixed (Masonry And Timber)",
              "Mixed (Plaster And Timber)",
              "Other Artificial Material (Not Concrete)",
              "Other Non-Standard Or System Build",
              "Static Caravan Or Mobile Home",
              "Metal",
              "Timber Or Wood",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "constructionmaterial_capturemethod": {
            "enum": [
              "Automated Process",
              "Default Value",
              "Desk-Based",
              "Field Survey",
              "Remote Sensing Survey",
              "Sensor Measurement",
              "Third Party Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "constructionmaterial_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "constructionmaterial_source": {
            "enum": [
              "Ordnance Survey",
              "Verisk"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "constructionmaterial_thirdpartyprovenance": {
            "type": [
              "string",
              "null"
            ]
          },
          "constructionmaterial_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "containingsitecount": {
            "type": "integer"
          },
          "description": {
            "enum": [
              "Abbey",
              "Agriculture Building",
              "Air Passenger Terminal",
              "Air Quality Monitoring Station",
              "Airport With Scheduled Services",
              "Airport Without Scheduled Services",
              "Ambulance And Fire Station",
              "Ambulance And Police Station",
              "Ambulance Station",
              "Ambulance, Fire And Police Station",
              "Ancillary Building",
              "Art Gallery",
              "Arts Centre",
              "Arts Centre And Museum",
              "Athletics Ground",
              "Athletics Stadium",
              "Attraction Building",
              "Biogas Power Station",
              "Bowls Clubhouse",
              "Buddhist Temple",
              "Building Under Construction",
              "Cable Terminal Station",
              "Cathedral",
              "Central Government Services",
              "Chapel",
              "Children's Nursery",
              "Church",
              "Cinema",
              "Coastguard Lookout",
              "College",
              "Commercial Building",
              "Community Building",
              "Community Meeting Place",
              "Community Services",
              "Construction Building",
              "Crematorium",
              "Cricket Ground (Participation)",
              "Cricket Ground (Spectating)",
              "Cricket Stadium",
              "Curling Rink",
              "Cycling Sports Facility",
              "Defence Building",
              "Detached House",
              "Detention Centre",
              "Domestic Outbuilding",
              "Education Building",
              "Electricity Distribution Facility",
              "Electricity Storage Facility",
              "Electricity Sub Station",
              "Emergency Assistance Or Equipment Facility",
              "End-Of-Terrace House",
              "Ferry Passenger Terminal",
              "Ferry Vehicular Terminal",
              "Ferry Vehicular Terminal (International)",
              "Fire Station",
              "Fire Station And Police Station",
              "Football Ground (Participation)",
              "Football Ground (Spectating)",
              "Football Stadium",
              "Gas Distribution Or Storage Facility",
              "Gas Governor",
              "Gas Production Facility",
              "Golf Centre",
              "Golf Clubhouse",
              "Golf Course",
              "Golf Driving Range",
              "Government Building",
              "Greyhound Track Or Stadium",
              "Gurdwara",
              "Health Centre",
              "Heating Plant",
              "Heliport",
              "Hindu Temple",
              "Historic Building",
              "HM Coastguard Station",
              "Hockey Ground",
              "Horse Racing Course",
              "Hospice",
              "Hospital",
              "Hydroelectric Power Generating",
              "Hydrogen Fuel Production And Supply",
              "Ice Rink",
              "Inshore Rescue Boat Station",
              "Kingdom Hall",
              "Law Court",
              "Leisure Or Sports Centre",
              "Library",
              "Library And Museum",
              "Lifeboat Station",
              "Light Rail Station",
              "Local Government Facility",
              "Medical Building",
              "Medical Care Facility",
              "Mid-Terrace House",
              "Minster",
              "Mixed Use Building",
              "Mosque",
              "Multi-Purpose Community Centre",
              "Multiple Residential Accommodation",
              "Museum",
              "Place Of Worship",
              "Police Headquarters",
              "Police Station",
              "Police Support Facility",
              "Power Station",
              "Prison",
              "Pumping Station",
              "Pupil Referral Centre",
              "Racquet Sports Club",
              "Railway Station",
              "Railway Station (Not Publicly Accessible)",
              "Railway Station (Principal)",
              "Railway Station (Underground System)",
              "Religious Meeting Place",
              "Residential Building",
              "Rowing Club",
              "Rugby Ground (Spectating)",
              "Rugby Pitch Or Ground (Participation)",
              "Rugby Stadium",
              "Sailing Centre",
              "School",
              "Secure Residential Unit",
              "Semi-Detached House",
              "Solar Power Facility",
              "Speedway Track",
              "Sports Building",
              "Sports Ground (Spectating)",
              "Sports Or Exercise Facility",
              "Sports Pavilion",
              "Sports Stadium",
              "Static Caravan Or Mobile Home",
              "Stupa",
              "Swimming Pool",
              "Synagogue",
              "Telecommunications Facility",
              "Telephone Exchange",
              "Temporary Or Holiday Accommodation Building",
              "Tennis Centre",
              "Theatre",
              "Tidal Power Station",
              "Transport Building",
              "University",
              "University College",
              "University School",
              "University Sports Or Exercise Facility",
              "Unknown Building",
              "Utility Building",
              "Waste Water Treatment Works",
              "Water Distribution Facility",
              "Water Sports Centre",
              "Water Treatment Facility",
              "Wildlife Or Zoological Park",
              "Yacht Club"
            ],
            "type": "string"
          },
          "description_updatedate": {
            "format": "date",
            "type": "string"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/Polygon.json",
            "type": "object"
          },
          "geometry_area_m2": {
            "type": "number"
          },
          "geometry_updatedate": {
            "format": "date",
            "type": "string"
          },
          "height_absolutemax_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "height_absolutemin_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "height_absoluteroofbase_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "height_confidencelevel": {
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
          "height_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "height_relativemax_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "height_relativeroofbase_m": {
            "type": [
              "number",
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
          "isinsite": {
            "type": "boolean"
          },
          "mainbuildingid": {
            "type": [
              "string",
              "null"
            ]
          },
          "mainbuildingid_ismainbuilding": {
            "enum": [
              "Yes",
              "No"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "mainbuildingid_updatedate": {
            "format": "date",
            "type": "string"
          },
          "numberoffloors": {
            "type": [
              "integer",
              "null"
            ]
          },
          "numberoffloors_capturemethod": {
            "enum": [
              "Automated Process",
              "Default Value",
              "Desk-Based",
              "Field Survey",
              "Remote Sensing Survey",
              "Sensor Measurement",
              "Third Party Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "numberoffloors_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "numberoffloors_source": {
            "type": [
              "string",
              "null"
            ]
          },
          "numberoffloors_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "osid": {
            "format": "uuid",
            "type": "string"
          },
          "physicalstate": {
            "enum": [
              "Built",
              "Derelict",
              "Under Construction"
            ],
            "type": "string"
          },
          "physicalstate_updatedate": {
            "format": "date",
            "type": "string"
          },
          "primarysiteid": {
            "type": [
              "string",
              "null"
            ]
          },
          "roofmaterial_capturemethod": {
            "enum": [
              "Automated Process",
              "Default Value",
              "Desk-Based",
              "Field Survey",
              "Remote Sensing Survey",
              "Sensor Measurement",
              "Third Party Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roofmaterial_confidenceindicator": {
            "enum": [
              "Complex Roof",
              "Existing Building Changed Since Imagery Capture",
              "Expected Data Output",
              "Insufficient Building Size",
              "New Building Surveyed After Imagery Capture",
              "Obscured Roof",
              "Uncertain Data Output"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roofmaterial_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "roofmaterial_greenroofpresence": {
            "enum": [
              "Present",
              "Not Present",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roofmaterial_primarymaterial": {
            "enum": [
              "Fabric",
              "Glass Or Polycarbonate",
              "Green Roof",
              "Metal",
              "Mixed",
              "Other",
              "Thatch",
              "Tile Or Stone Or Slate",
              "Unknown",
              "Waterproof Membrane Or Concrete"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roofmaterial_solarpanelpresence": {
            "enum": [
              "Present",
              "Not Present",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roofmaterial_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "roofshapeaspect_areafacingeast_m2": {
            "type": [
              "number",
              "null"
            ]
          },
          "roofshapeaspect_areafacingnorth_m2": {
            "type": [
              "number",
              "null"
            ]
          },
          "roofshapeaspect_areafacingnortheast_m2": {
            "type": [
              "number",
              "null"
            ]
          },
          "roofshapeaspect_areafacingnorthwest_m2": {
            "type": [
              "number",
              "null"
            ]
          },
          "roofshapeaspect_areafacingsouth_m2": {
            "type": [
              "number",
              "null"
            ]
          },
          "roofshapeaspect_areafacingsoutheast_m2": {
            "type": [
              "number",
              "null"
            ]
          },
          "roofshapeaspect_areafacingsouthwest_m2": {
            "type": [
              "number",
              "null"
            ]
          },
          "roofshapeaspect_areafacingwest_m2": {
            "type": [
              "number",
              "null"
            ]
          },
          "roofshapeaspect_areaflat_m2": {
            "type": [
              "number",
              "null"
            ]
          },
          "roofshapeaspect_areaindeterminable_m2": {
            "type": [
              "number",
              "null"
            ]
          },
          "roofshapeaspect_areapitched_m2": {
            "type": [
              "number",
              "null"
            ]
          },
          "roofshapeaspect_areatotal_m2": {
            "type": [
              "number",
              "null"
            ]
          },
          "roofshapeaspect_capturemethod": {
            "enum": [
              "Automated Process",
              "Default Value",
              "Desk-Based",
              "Field Survey",
              "Remote Sensing Survey",
              "Sensor Measurement",
              "Third Party Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roofshapeaspect_confidenceindicator": {
            "enum": [
              "Complex Roof",
              "Existing Building Changed Since Imagery Capture",
              "Expected Data Output",
              "Insufficient Building Size",
              "New Building Surveyed After Imagery Capture",
              "Obscured Roof",
              "Uncertain Data Output"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roofshapeaspect_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "roofshapeaspect_shape": {
            "enum": [
              "Flat",
              "Mixed",
              "Pitched",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roofshapeaspect_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "sitereference": {
            "items": {
              "properties": {
                "buildingid": {
                  "description": "The identifier of the Building.",
                  "format": "uuid",
                  "maxLength": 36,
                  "originalName": "buildingID",
                  "type": "string"
                },
                "buildingversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "buildingVersionDate",
                  "type": "string"
                },
                "siteid": {
                  "description": "The identifier of the site the Building is within.",
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
          "uprnreference": {
            "items": {
              "properties": {
                "buildingid": {
                  "description": "The identifier of the Building.",
                  "format": "uuid",
                  "maxLength": 36,
                  "originalName": "buildingID",
                  "type": "string"
                },
                "buildingversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "buildingVersionDate",
                  "type": "string"
                },
                "uprn": {
                  "description": "The identifier of the addressable feature that is located within the Building.",
                  "originalName": "uprn",
                  "type": "number"
                }
              },
              "type": "object"
            },
            "type": "array"
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
          "versiondate",
          "versionavailablefromdate",
          "versionavailabletodate",
          "changetype",
          "geometry",
          "geometry_area_m2",
          "geometry_updatedate",
          "theme",
          "description",
          "description_updatedate",
          "physicalstate",
          "physicalstate_updatedate",
          "buildingpartcount",
          "isinsite",
          "primarysiteid",
          "containingsitecount",
          "mainbuildingid",
          "mainbuildingid_ismainbuilding",
          "mainbuildingid_updatedate",
          "buildinguse",
          "buildinguse_oslandusetiera",
          "buildinguse_addresscount_total",
          "buildinguse_addresscount_residential",
          "buildinguse_addresscount_commercial",
          "buildinguse_addresscount_other",
          "buildinguse_updatedate",
          "connectivity",
          "connectivity_count",
          "connectivity_updatedate",
          "constructionmaterial",
          "constructionmaterial_evidencedate",
          "constructionmaterial_updatedate",
          "constructionmaterial_source",
          "constructionmaterial_capturemethod",
          "constructionmaterial_thirdpartyprovenance",
          "buildingage_period",
          "buildingage_year",
          "buildingage_evidencedate",
          "buildingage_updatedate",
          "buildingage_source",
          "buildingage_capturemethod",
          "buildingage_thirdpartyprovenance",
          "basementpresence",
          "basementpresence_selfcontained",
          "basementpresence_evidencedate",
          "basementpresence_updatedate",
          "basementpresence_source",
          "basementpresence_capturemethod",
          "basementpresence_thirdpartyprovenance",
          "numberoffloors",
          "numberoffloors_evidencedate",
          "numberoffloors_updatedate",
          "numberoffloors_source",
          "numberoffloors_capturemethod",
          "height_absolutemin_m",
          "height_absoluteroofbase_m",
          "height_absolutemax_m",
          "height_relativeroofbase_m",
          "height_relativemax_m",
          "height_confidencelevel",
          "height_evidencedate",
          "height_updatedate",
          "roofmaterial_primarymaterial",
          "roofmaterial_solarpanelpresence",
          "roofmaterial_greenroofpresence",
          "roofmaterial_confidenceindicator",
          "roofmaterial_evidencedate",
          "roofmaterial_updatedate",
          "roofmaterial_capturemethod",
          "roofshapeaspect_shape",
          "roofshapeaspect_areapitched_m2",
          "roofshapeaspect_areaflat_m2",
          "roofshapeaspect_areafacingnorth_m2",
          "roofshapeaspect_areafacingnortheast_m2",
          "roofshapeaspect_areafacingeast_m2",
          "roofshapeaspect_areafacingsoutheast_m2",
          "roofshapeaspect_areafacingsouth_m2",
          "roofshapeaspect_areafacingsouthwest_m2",
          "roofshapeaspect_areafacingwest_m2",
          "roofshapeaspect_areafacingnorthwest_m2",
          "roofshapeaspect_areaindeterminable_m2",
          "roofshapeaspect_areatotal_m2",
          "roofshapeaspect_confidenceindicator",
          "roofshapeaspect_evidencedate",
          "roofshapeaspect_updatedate",
          "roofshapeaspect_capturemethod",
          "sitereference",
          "buildingpartreference",
          "uprnreference"
        ],
        "requiredUndeclared": [],
        "sha256": "4af10efc7afe8125c2fc9e46d391018faab5a4b9c4f6f3f2d2a67944eb49464e",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Building v4"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2025-03-12T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/queryables",
      "responseSha256": "1a204d0c47eace06fa87342386ae342777d44afd472bfd1143f53cc20c5e7100",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema",
      "responseSha256": "4af10efc7afe8125c2fc9e46d391018faab5a4b9c4f6f3f2d2a67944eb49464e",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/basementpresence",
      "@type": "rdf:Property",
      "dcterms:identifier": "basementpresence",
      "rdfs:label": "basementpresence",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Present",
            "Not Present",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/basementpresence_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "basementpresence_capturemethod",
      "rdfs:label": "basementpresence_capturemethod",
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
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/basementpresence_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "basementpresence_evidencedate",
      "rdfs:label": "basementpresence_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/basementpresence_selfcontained",
      "@type": "rdf:Property",
      "dcterms:identifier": "basementpresence_selfcontained",
      "rdfs:label": "basementpresence_selfcontained",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Present",
            "Not Present",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/basementpresence_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "basementpresence_source",
      "rdfs:label": "basementpresence_source",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Address Authority",
            "Ordnance Survey",
            "Verisk"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/basementpresence_thirdpartyprovenance",
      "@type": "rdf:Property",
      "dcterms:identifier": "basementpresence_thirdpartyprovenance",
      "rdfs:label": "basementpresence_thirdpartyprovenance",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/basementpresence_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "basementpresence_updatedate",
      "rdfs:label": "basementpresence_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildingage_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildingage_capturemethod",
      "rdfs:label": "buildingage_capturemethod",
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
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildingage_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildingage_evidencedate",
      "rdfs:label": "buildingage_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildingage_period",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildingage_period",
      "rdfs:label": "buildingage_period",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Pre-1837",
            "Pre-1919",
            "1837-1869",
            "1870-1918",
            "1919-1944",
            "1945-1959",
            "1960-1979",
            "1980-1989",
            "1990-1999",
            "2000-2009",
            "2010-2019",
            "2020-2029",
            "2030-2039",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildingage_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildingage_source",
      "rdfs:label": "buildingage_source",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Ordnance Survey",
            "Verisk"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildingage_thirdpartyprovenance",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildingage_thirdpartyprovenance",
      "rdfs:label": "buildingage_thirdpartyprovenance",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildingage_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildingage_updatedate",
      "rdfs:label": "buildingage_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildingage_year",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildingage_year",
      "rdfs:label": "buildingage_year",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "integer",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildingpartcount",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildingpartcount",
      "rdfs:label": "buildingpartcount",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildingpartreference",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildingpartreference",
      "rdfs:label": "buildingpartreference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "buildingid": {
                "description": "The identifier of the Building.",
                "format": "uuid",
                "maxLength": 36,
                "originalName": "buildingID",
                "type": "string"
              },
              "buildingpartid": {
                "description": "The identifier of the Building Part the Building is created from.",
                "format": "uuid",
                "maxLength": 36,
                "originalName": "buidingPartID",
                "type": "string"
              },
              "buildingversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "buildingVersionDate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildinguse",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildinguse",
      "rdfs:label": "buildinguse",
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
            "Unknown",
            "Unknown Use",
            "Utility Or Environmental Protection"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildinguse_addresscount_commercial",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildinguse_addresscount_commercial",
      "rdfs:label": "buildinguse_addresscount_commercial",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildinguse_addresscount_other",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildinguse_addresscount_other",
      "rdfs:label": "buildinguse_addresscount_other",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildinguse_addresscount_residential",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildinguse_addresscount_residential",
      "rdfs:label": "buildinguse_addresscount_residential",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildinguse_addresscount_total",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildinguse_addresscount_total",
      "rdfs:label": "buildinguse_addresscount_total",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildinguse_oslandusetiera",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildinguse_oslandusetiera",
      "rdfs:label": "buildinguse_oslandusetiera",
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
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/buildinguse_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "buildinguse_updatedate",
      "rdfs:label": "buildinguse_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/connectivity",
      "@type": "rdf:Property",
      "dcterms:identifier": "connectivity",
      "rdfs:label": "connectivity",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "End-Connected",
            "Multi-Connected",
            "Semi-Connected",
            "Standalone"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/connectivity_count",
      "@type": "rdf:Property",
      "dcterms:identifier": "connectivity_count",
      "rdfs:label": "connectivity_count",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/connectivity_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "connectivity_updatedate",
      "rdfs:label": "connectivity_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/constructionmaterial",
      "@type": "rdf:Property",
      "dcterms:identifier": "constructionmaterial",
      "rdfs:label": "constructionmaterial",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Brick Or Block Or Stone",
            "Concrete",
            "Mixed (Masonry And Metal)",
            "Mixed (Masonry And Timber)",
            "Mixed (Plaster And Timber)",
            "Other Artificial Material (Not Concrete)",
            "Other Non-Standard Or System Build",
            "Static Caravan Or Mobile Home",
            "Metal",
            "Timber Or Wood",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/constructionmaterial_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "constructionmaterial_capturemethod",
      "rdfs:label": "constructionmaterial_capturemethod",
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
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/constructionmaterial_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "constructionmaterial_evidencedate",
      "rdfs:label": "constructionmaterial_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/constructionmaterial_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "constructionmaterial_source",
      "rdfs:label": "constructionmaterial_source",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Ordnance Survey",
            "Verisk"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/constructionmaterial_thirdpartyprovenance",
      "@type": "rdf:Property",
      "dcterms:identifier": "constructionmaterial_thirdpartyprovenance",
      "rdfs:label": "constructionmaterial_thirdpartyprovenance",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/constructionmaterial_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "constructionmaterial_updatedate",
      "rdfs:label": "constructionmaterial_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/containingsitecount",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Abbey",
            "Agriculture Building",
            "Air Passenger Terminal",
            "Air Quality Monitoring Station",
            "Airport With Scheduled Services",
            "Airport Without Scheduled Services",
            "Ambulance And Fire Station",
            "Ambulance And Police Station",
            "Ambulance Station",
            "Ambulance, Fire And Police Station",
            "Ancillary Building",
            "Art Gallery",
            "Arts Centre",
            "Arts Centre And Museum",
            "Athletics Ground",
            "Athletics Stadium",
            "Attraction Building",
            "Biogas Power Station",
            "Bowls Clubhouse",
            "Buddhist Temple",
            "Building Under Construction",
            "Cable Terminal Station",
            "Cathedral",
            "Central Government Services",
            "Chapel",
            "Children's Nursery",
            "Church",
            "Cinema",
            "Coastguard Lookout",
            "College",
            "Commercial Building",
            "Community Building",
            "Community Meeting Place",
            "Community Services",
            "Construction Building",
            "Crematorium",
            "Cricket Ground (Participation)",
            "Cricket Ground (Spectating)",
            "Cricket Stadium",
            "Curling Rink",
            "Cycling Sports Facility",
            "Defence Building",
            "Detached House",
            "Detention Centre",
            "Domestic Outbuilding",
            "Education Building",
            "Electricity Distribution Facility",
            "Electricity Storage Facility",
            "Electricity Sub Station",
            "Emergency Assistance Or Equipment Facility",
            "End-Of-Terrace House",
            "Ferry Passenger Terminal",
            "Ferry Vehicular Terminal",
            "Ferry Vehicular Terminal (International)",
            "Fire Station",
            "Fire Station And Police Station",
            "Football Ground (Participation)",
            "Football Ground (Spectating)",
            "Football Stadium",
            "Gas Distribution Or Storage Facility",
            "Gas Governor",
            "Gas Production Facility",
            "Golf Centre",
            "Golf Clubhouse",
            "Golf Course",
            "Golf Driving Range",
            "Government Building",
            "Greyhound Track Or Stadium",
            "Gurdwara",
            "Health Centre",
            "Heating Plant",
            "Heliport",
            "Hindu Temple",
            "Historic Building",
            "HM Coastguard Station",
            "Hockey Ground",
            "Horse Racing Course",
            "Hospice",
            "Hospital",
            "Hydroelectric Power Generating",
            "Hydrogen Fuel Production And Supply",
            "Ice Rink",
            "Inshore Rescue Boat Station",
            "Kingdom Hall",
            "Law Court",
            "Leisure Or Sports Centre",
            "Library",
            "Library And Museum",
            "Lifeboat Station",
            "Light Rail Station",
            "Local Government Facility",
            "Medical Building",
            "Medical Care Facility",
            "Mid-Terrace House",
            "Minster",
            "Mixed Use Building",
            "Mosque",
            "Multi-Purpose Community Centre",
            "Multiple Residential Accommodation",
            "Museum",
            "Place Of Worship",
            "Police Headquarters",
            "Police Station",
            "Police Support Facility",
            "Power Station",
            "Prison",
            "Pumping Station",
            "Pupil Referral Centre",
            "Racquet Sports Club",
            "Railway Station",
            "Railway Station (Not Publicly Accessible)",
            "Railway Station (Principal)",
            "Railway Station (Underground System)",
            "Religious Meeting Place",
            "Residential Building",
            "Rowing Club",
            "Rugby Ground (Spectating)",
            "Rugby Pitch Or Ground (Participation)",
            "Rugby Stadium",
            "Sailing Centre",
            "School",
            "Secure Residential Unit",
            "Semi-Detached House",
            "Solar Power Facility",
            "Speedway Track",
            "Sports Building",
            "Sports Ground (Spectating)",
            "Sports Or Exercise Facility",
            "Sports Pavilion",
            "Sports Stadium",
            "Static Caravan Or Mobile Home",
            "Stupa",
            "Swimming Pool",
            "Synagogue",
            "Telecommunications Facility",
            "Telephone Exchange",
            "Temporary Or Holiday Accommodation Building",
            "Tennis Centre",
            "Theatre",
            "Tidal Power Station",
            "Transport Building",
            "University",
            "University College",
            "University School",
            "University Sports Or Exercise Facility",
            "Unknown Building",
            "Utility Building",
            "Waste Water Treatment Works",
            "Water Distribution Facility",
            "Water Sports Centre",
            "Water Treatment Facility",
            "Wildlife Or Zoological Park",
            "Yacht Club"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/description_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/geometry_area_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/geometry_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/height_absolutemax_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "height_absolutemax_m",
      "rdfs:label": "height_absolutemax_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/height_absolutemin_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "height_absolutemin_m",
      "rdfs:label": "height_absolutemin_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/height_absoluteroofbase_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "height_absoluteroofbase_m",
      "rdfs:label": "height_absoluteroofbase_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/height_confidencelevel",
      "@type": "rdf:Property",
      "dcterms:identifier": "height_confidencelevel",
      "rdfs:label": "height_confidencelevel",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/height_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/height_relativemax_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "height_relativemax_m",
      "rdfs:label": "height_relativemax_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/height_relativeroofbase_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "height_relativeroofbase_m",
      "rdfs:label": "height_relativeroofbase_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/height_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/isinsite",
      "@type": "rdf:Property",
      "dcterms:identifier": "isinsite",
      "rdfs:label": "isinsite",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "boolean"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/mainbuildingid",
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
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/mainbuildingid_ismainbuilding",
      "@type": "rdf:Property",
      "dcterms:identifier": "mainbuildingid_ismainbuilding",
      "rdfs:label": "mainbuildingid_ismainbuilding",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Yes",
            "No"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/mainbuildingid_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "mainbuildingid_updatedate",
      "rdfs:label": "mainbuildingid_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/numberoffloors",
      "@type": "rdf:Property",
      "dcterms:identifier": "numberoffloors",
      "rdfs:label": "numberoffloors",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "integer",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/numberoffloors_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "numberoffloors_capturemethod",
      "rdfs:label": "numberoffloors_capturemethod",
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
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/numberoffloors_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "numberoffloors_evidencedate",
      "rdfs:label": "numberoffloors_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/numberoffloors_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "numberoffloors_source",
      "rdfs:label": "numberoffloors_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/numberoffloors_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "numberoffloors_updatedate",
      "rdfs:label": "numberoffloors_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/physicalstate",
      "@type": "rdf:Property",
      "dcterms:identifier": "physicalstate",
      "rdfs:label": "physicalstate",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Built",
            "Derelict",
            "Under Construction"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/physicalstate_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "physicalstate_updatedate",
      "rdfs:label": "physicalstate_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/primarysiteid",
      "@type": "rdf:Property",
      "dcterms:identifier": "primarysiteid",
      "rdfs:label": "primarysiteid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofmaterial_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofmaterial_capturemethod",
      "rdfs:label": "roofmaterial_capturemethod",
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
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofmaterial_confidenceindicator",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofmaterial_confidenceindicator",
      "rdfs:label": "roofmaterial_confidenceindicator",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Complex Roof",
            "Existing Building Changed Since Imagery Capture",
            "Expected Data Output",
            "Insufficient Building Size",
            "New Building Surveyed After Imagery Capture",
            "Obscured Roof",
            "Uncertain Data Output"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofmaterial_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofmaterial_evidencedate",
      "rdfs:label": "roofmaterial_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofmaterial_greenroofpresence",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofmaterial_greenroofpresence",
      "rdfs:label": "roofmaterial_greenroofpresence",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Present",
            "Not Present",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofmaterial_primarymaterial",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofmaterial_primarymaterial",
      "rdfs:label": "roofmaterial_primarymaterial",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Fabric",
            "Glass Or Polycarbonate",
            "Green Roof",
            "Metal",
            "Mixed",
            "Other",
            "Thatch",
            "Tile Or Stone Or Slate",
            "Unknown",
            "Waterproof Membrane Or Concrete"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofmaterial_solarpanelpresence",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofmaterial_solarpanelpresence",
      "rdfs:label": "roofmaterial_solarpanelpresence",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Present",
            "Not Present",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofmaterial_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofmaterial_updatedate",
      "rdfs:label": "roofmaterial_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_areafacingeast_m2",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_areafacingeast_m2",
      "rdfs:label": "roofshapeaspect_areafacingeast_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_areafacingnorth_m2",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_areafacingnorth_m2",
      "rdfs:label": "roofshapeaspect_areafacingnorth_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_areafacingnortheast_m2",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_areafacingnortheast_m2",
      "rdfs:label": "roofshapeaspect_areafacingnortheast_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_areafacingnorthwest_m2",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_areafacingnorthwest_m2",
      "rdfs:label": "roofshapeaspect_areafacingnorthwest_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_areafacingsouth_m2",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_areafacingsouth_m2",
      "rdfs:label": "roofshapeaspect_areafacingsouth_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_areafacingsoutheast_m2",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_areafacingsoutheast_m2",
      "rdfs:label": "roofshapeaspect_areafacingsoutheast_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_areafacingsouthwest_m2",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_areafacingsouthwest_m2",
      "rdfs:label": "roofshapeaspect_areafacingsouthwest_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_areafacingwest_m2",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_areafacingwest_m2",
      "rdfs:label": "roofshapeaspect_areafacingwest_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_areaflat_m2",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_areaflat_m2",
      "rdfs:label": "roofshapeaspect_areaflat_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_areaindeterminable_m2",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_areaindeterminable_m2",
      "rdfs:label": "roofshapeaspect_areaindeterminable_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_areapitched_m2",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_areapitched_m2",
      "rdfs:label": "roofshapeaspect_areapitched_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_areatotal_m2",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_areatotal_m2",
      "rdfs:label": "roofshapeaspect_areatotal_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_capturemethod",
      "rdfs:label": "roofshapeaspect_capturemethod",
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
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_confidenceindicator",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_confidenceindicator",
      "rdfs:label": "roofshapeaspect_confidenceindicator",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Complex Roof",
            "Existing Building Changed Since Imagery Capture",
            "Expected Data Output",
            "Insufficient Building Size",
            "New Building Surveyed After Imagery Capture",
            "Obscured Roof",
            "Uncertain Data Output"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_evidencedate",
      "rdfs:label": "roofshapeaspect_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_shape",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_shape",
      "rdfs:label": "roofshapeaspect_shape",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Flat",
            "Mixed",
            "Pitched",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/roofshapeaspect_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "roofshapeaspect_updatedate",
      "rdfs:label": "roofshapeaspect_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/sitereference",
      "@type": "rdf:Property",
      "dcterms:identifier": "sitereference",
      "rdfs:label": "sitereference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "buildingid": {
                "description": "The identifier of the Building.",
                "format": "uuid",
                "maxLength": 36,
                "originalName": "buildingID",
                "type": "string"
              },
              "buildingversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "buildingVersionDate",
                "type": "string"
              },
              "siteid": {
                "description": "The identifier of the site the Building is within.",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/uprnreference",
      "@type": "rdf:Property",
      "dcterms:identifier": "uprnreference",
      "rdfs:label": "uprnreference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "buildingid": {
                "description": "The identifier of the Building.",
                "format": "uuid",
                "maxLength": 36,
                "originalName": "buildingID",
                "type": "string"
              },
              "buildingversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "buildingVersionDate",
                "type": "string"
              },
              "uprn": {
                "description": "The identifier of the addressable feature that is located within the Building.",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-building-4/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema"
      }
    }
  ]
}
---

# Building v4

A new building geometry which represents a single building footprint. This geometry consists of adjoining building parts which have been determined to be part of the same building. When contained in a Land Use Site, adjoining building parts will be represented by a single feature.

Native identifier: `bld-fts-building-4`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2025-03-12T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
