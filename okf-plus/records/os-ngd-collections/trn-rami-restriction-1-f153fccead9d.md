---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Restriction v1",
  "description": "Restriction includes turn restrictions, restriction for vehicles, and access restrictions. Turn restrictions are a restriction based upon a vehicle manoeuvre. This type of restriction includes prohibitive driving instructions, mandatory driving instruction and implicit restrictions. Prohibited instructions are indicated by road signs within a red circle, examples include No U Turn, No Right Turn or No Left Turn. These can include exceptions to the instruction and are typically elements like Except for Buses. Mandatory driving instructions indicated by road signs within a blue circle or painted on the roadway such as Turn Right, Ahead Only and Left Turn. Implicit restrictions occur where a turn is not signed as prohibited but would not be a normal manoeuvre. For example, where a road splits around a traffic island or at complex junctions where additional geometry has been captured to reflect the traffic flow. These are not differentiated from actual signed restrictions. Restriction for vehicles are constraints that apply to the vehicles based on their physical characteristics: height, weight, width and length. These are required to protect structures such as bridges and tunnels from damage, or to restrict/prohibit use by vehicle that exceed specific dimensions, usually for environmental reasons. Restriction for vehicles has been extended to support the full definition of height, weight, width and length restrictions as defined in the UK to ensure that they can: Apply to specific vehicle types only Relate to a structure for which the restriction is designed to protect (for example, a Bridge)",
  "nativeIdentifier": "trn-rami-restriction-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1",
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
      "sourcePointer": "/collections/78",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/78",
      "normalisedRecordSha256": "654837ae2ea7e90f8be02094fdcc53c81420cf2cda28179f7355d24a92ffab9c",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1"
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
    "description": "Restriction includes turn restrictions, restriction for vehicles, and access restrictions.\nTurn restrictions are a restriction based upon a vehicle manoeuvre. This type of restriction includes prohibitive driving instructions, mandatory driving instruction and implicit restrictions. Prohibited instructions are indicated by road signs within a red circle, examples include No U Turn, No Right Turn or No Left Turn. These can include exceptions to the instruction and are typically elements like Except for Buses. Mandatory driving instructions indicated by road signs within a blue circle or painted on the roadway such as Turn Right, Ahead Only and Left Turn. Implicit restrictions occur where a turn is not signed as prohibited but would not be a normal manoeuvre. For example, where a road splits around a traffic island or at complex junctions where additional geometry has been captured to reflect the traffic flow. These are not differentiated from actual signed restrictions.\nRestriction for vehicles are constraints that apply to the vehicles based on their physical characteristics: height, weight, width and length. These are required to protect structures such as bridges and tunnels from damage, or to restrict/prohibit use by vehicle that exceed specific dimensions, usually for environmental reasons.\nRestriction for vehicles has been extended to support the full definition of height, weight, width and length restrictions as defined in the UK to ensure that they can:\nApply to specific vehicle types only\nRelate to a structure for which the restriction is designed to protect (for example, a Bridge)",
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
    "id": "trn-rami-restriction-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1",
        "rel": "self",
        "title": "The 'Restriction v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/items",
        "rel": "items",
        "title": "The features in the 'Restriction v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Restriction v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Restriction v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/queryables",
        "properties": {
          "description": {
            "enum": [
              "Access Restriction",
              "One Way",
              "Restriction For Vehicles",
              "Turn Restriction"
            ],
            "type": [
              "string"
            ]
          },
          "exemption": {
            "items": {
              "enum": [
                "Access",
                "All Vehicles",
                "Abnormal Loads",
                "Access To Off Street Premises",
                "Articulated Vehicles",
                "Animal Loads",
                "Authorised Vehicles",
                "Buses",
                "Coaches",
                "Customers",
                "Dangerous Goods",
                "Disabled",
                "Emergency Vehicles",
                "Explosives",
                "Emergency Access",
                "Goods Vehicles",
                "Wide Loads",
                "Escorted Traffic",
                "Goods Vehicles Exceeding 1.5T",
                "Goods Vehicles Exceeding 2T",
                "Goods Vehicles Exceeding 2.5T",
                "Goods Vehicles Exceeding 4T",
                "Goods Vehicles Exceeding 3T",
                "Fuel Tankers",
                "Goods Vehicles Exceeding 3.5T",
                "Goods Vehicles Exceeding 5T",
                "Goods Vehicles Exceeding 7.5T",
                "Guided Buses",
                "Goods Vehicles Exceeding 17T",
                "Loading And Unloading",
                "Goods Vehicles Exceeding 16.5T",
                "Local Buses",
                "Goods Vehicles Exceeding 17.5T",
                "Official Business",
                "Goods Vehicles Exceeding 18T",
                "Paying",
                "Goods Vehicles Exceeding 26T",
                "Pedestrians",
                "Goods Vehicles Exceeding 33T",
                "Permit Holders",
                "Heavy Goods Vehicles",
                "Public Transport",
                "Horse Drawn Vehicles",
                "Residents And Guests",
                "Large Vehicles",
                "School Buses",
                "Long Vehicles",
                "Service Vehicles",
                "Light Goods Vehicles",
                "Taxis",
                "Mopeds",
                "Through Traffic",
                "Motor Cycles",
                "Works Traffic",
                "Motor Vehicles",
                "Pedal Cycles",
                "Pedestrians",
                "Ridden Or Accompanied Horses",
                "Towed Caravans",
                "Tracked Vehicles",
                "Trailers",
                "Tramcars",
                "Guests",
                "Public",
                "Residents",
                "Public Service Vehicles",
                "Vehicles Under 7.5T",
                "Wide Vehicles",
                "Inflammables"
              ],
              "enumeration": true,
              "maxLength": 38,
              "type": [
                "string",
                "null"
              ]
            },
            "type": [
              "array"
            ]
          },
          "geometry_length": {
            "type": [
              "number"
            ]
          },
          "inclusion": {
            "items": {
              "enum": [
                "Access",
                "All Vehicles",
                "Abnormal Loads",
                "Access To Off Street Premises",
                "Articulated Vehicles",
                "Animal Loads",
                "Authorised Vehicles",
                "Buses",
                "Coaches",
                "Customers",
                "Dangerous Goods",
                "Disabled",
                "Emergency Vehicles",
                "Explosives",
                "Emergency Access",
                "Goods Vehicles",
                "Wide Loads",
                "Escorted Traffic",
                "Goods Vehicles Exceeding 1.5T",
                "Goods Vehicles Exceeding 2T",
                "Goods Vehicles Exceeding 2.5T",
                "Goods Vehicles Exceeding 4T",
                "Goods Vehicles Exceeding 3T",
                "Fuel Tankers",
                "Goods Vehicles Exceeding 3.5T",
                "Goods Vehicles Exceeding 5T",
                "Goods Vehicles Exceeding 7.5T",
                "Guided Buses",
                "Goods Vehicles Exceeding 17T",
                "Loading And Unloading",
                "Goods Vehicles Exceeding 16.5T",
                "Local Buses",
                "Goods Vehicles Exceeding 17.5T",
                "Official Business",
                "Goods Vehicles Exceeding 18T",
                "Paying",
                "Goods Vehicles Exceeding 26T",
                "Pedestrians",
                "Goods Vehicles Exceeding 33T",
                "Permit Holders",
                "Heavy Goods Vehicles",
                "Public Transport",
                "Horse Drawn Vehicles",
                "Residents And Guests",
                "Large Vehicles",
                "School Buses",
                "Long Vehicles",
                "Service Vehicles",
                "Light Goods Vehicles",
                "Taxis",
                "Mopeds",
                "Through Traffic",
                "Motor Cycles",
                "Works Traffic",
                "Motor Vehicles",
                "Pedal Cycles",
                "Pedestrians",
                "Ridden Or Accompanied Horses",
                "Towed Caravans",
                "Tracked Vehicles",
                "Trailers",
                "Tramcars",
                "Guests",
                "Public",
                "Residents",
                "Public Service Vehicles",
                "Vehicles Under 7.5T",
                "Wide Vehicles",
                "Inflammables"
              ],
              "enumeration": true,
              "maxLength": 38,
              "type": [
                "string",
                "null"
              ]
            },
            "type": [
              "array"
            ]
          },
          "osid": {
            "type": [
              "string"
            ]
          },
          "restriction": {
            "enum": [
              "Forbidden Legally",
              "Mandatory Turn",
              "Maximum Double Axle Weight",
              "Maximum Height",
              "Maximum Length",
              "Maximum Single Axle Weight",
              "Maximum Total Weight",
              "Maximum Triple Axle Weight",
              "Maximum Unladen Weight",
              "Maximum Width",
              "No Turn",
              "One Way",
              "Physically Impossible",
              "Private"
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
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "dcaf38bd52298430f23326ee60ce116973bc5ac302d7bf6da906bbd98098074f",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-rami-restriction-1.0",
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
          "datetimequalifier": {
            "items": {
              "properties": {
                "datetimequalifierid": {
                  "description": "The OS identifier of the date time qualifier feature.",
                  "maxLength": 36,
                  "originalName": "dateTimeQualifierID",
                  "type": "string"
                },
                "enddate": {
                  "description": "The date at which the restriction applied ends. This date will be in the format YYYY-MM-DD.",
                  "format": "date",
                  "originalName": "endDate",
                  "pattern": "YYYY-MM-DD",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "endmonthday": {
                  "description": "The date at which the restriction applied ends. This date will be in the format MM-DD.",
                  "maxLength": 6,
                  "originalName": "endMonthDay",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "endtime": {
                  "description": "The time the restriction ends.",
                  "maxLength": 8,
                  "originalName": "endTime",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "nameddate": {
                  "description": "The named month or period this time interval applies to.",
                  "enum": [
                    "All Year",
                    "April",
                    "August",
                    "Autumn",
                    "Christmas",
                    "December",
                    "Easter",
                    "February",
                    "January",
                    "July",
                    "June",
                    "March",
                    "May",
                    "November",
                    "October",
                    "September",
                    "Spring",
                    "Summer",
                    "Winter"
                  ],
                  "maxLength": 9,
                  "originalName": "namedDate",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "namedday": {
                  "description": "The named day this restriction applies to.",
                  "enum": [
                    "All Days",
                    "Friday",
                    "Market Days",
                    "Monday",
                    "Public Holidays",
                    "Saturday",
                    "Sunday",
                    "Thursday",
                    "Tuesday",
                    "Wednesday",
                    "Weekdays",
                    "Weekends"
                  ],
                  "maxLength": 15,
                  "originalName": "namedDay",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "namedperiod": {
                  "description": "A specified period in which the restriction applies.",
                  "enum": [
                    "Extreme Weather",
                    "Firing Times",
                    "Local Times Apply",
                    "School Arrival And Departure",
                    "School Holidays",
                    "School Hours",
                    "Special Arrangements",
                    "Term Time"
                  ],
                  "maxLength": 28,
                  "originalName": "namedPeriod",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "namedtime": {
                  "description": "These are named time periods that do not relate to the same time each day.",
                  "enum": [
                    "All Day",
                    "At High Tide",
                    "At Low Tide",
                    "Dawn Till Dusk",
                    "Day",
                    "Dusk Till Dawn",
                    "Evening Rush Hour",
                    "Evenings",
                    "Morning Rush Hour",
                    "Night",
                    "Part Time",
                    "Peak Time"
                  ],
                  "maxLength": 17,
                  "originalName": "namedTime",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "restrictionid": {
                  "description": "The identifier for the Restriction feature.",
                  "maxLength": 36,
                  "originalName": "restrictionID",
                  "type": "string"
                },
                "restrictionversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "restrictionVersionDate",
                  "pattern": "YYYY-MM-DD",
                  "type": "string"
                },
                "startdate": {
                  "description": "The date at which the restriction applied starts. This date will be in the format YYYY-MM-DD.",
                  "format": "date",
                  "originalName": "startDate",
                  "pattern": "YYYY-MM-DD",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "startmonthday": {
                  "description": "The date at which the restriction applied starts. This date will be in the format -MM-DD.",
                  "maxLength": 6,
                  "originalName": "startMonthDay",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "starttime": {
                  "description": "The time the restriction begins.",
                  "maxLength": 8,
                  "originalName": "startTime",
                  "type": [
                    "string",
                    "null"
                  ]
                }
              },
              "type": "object"
            },
            "type": "array"
          },
          "description": {
            "enum": [
              "Access Restriction",
              "One Way",
              "Restriction For Vehicles",
              "Turn Restriction"
            ],
            "type": "string"
          },
          "exemption": {
            "items": {
              "enum": [
                "Access",
                "All Vehicles",
                "Abnormal Loads",
                "Access To Off Street Premises",
                "Articulated Vehicles",
                "Animal Loads",
                "Authorised Vehicles",
                "Buses",
                "Coaches",
                "Customers",
                "Dangerous Goods",
                "Disabled",
                "Emergency Vehicles",
                "Explosives",
                "Emergency Access",
                "Goods Vehicles",
                "Wide Loads",
                "Escorted Traffic",
                "Goods Vehicles Exceeding 1.5T",
                "Goods Vehicles Exceeding 2T",
                "Goods Vehicles Exceeding 2.5T",
                "Goods Vehicles Exceeding 4T",
                "Goods Vehicles Exceeding 3T",
                "Fuel Tankers",
                "Goods Vehicles Exceeding 3.5T",
                "Goods Vehicles Exceeding 5T",
                "Goods Vehicles Exceeding 7.5T",
                "Guided Buses",
                "Goods Vehicles Exceeding 17T",
                "Loading And Unloading",
                "Goods Vehicles Exceeding 16.5T",
                "Local Buses",
                "Goods Vehicles Exceeding 17.5T",
                "Official Business",
                "Goods Vehicles Exceeding 18T",
                "Paying",
                "Goods Vehicles Exceeding 26T",
                "Pedestrians",
                "Goods Vehicles Exceeding 33T",
                "Permit Holders",
                "Heavy Goods Vehicles",
                "Public Transport",
                "Horse Drawn Vehicles",
                "Residents And Guests",
                "Large Vehicles",
                "School Buses",
                "Long Vehicles",
                "Service Vehicles",
                "Light Goods Vehicles",
                "Taxis",
                "Mopeds",
                "Through Traffic",
                "Motor Cycles",
                "Works Traffic",
                "Motor Vehicles",
                "Pedal Cycles",
                "Pedestrians",
                "Ridden Or Accompanied Horses",
                "Towed Caravans",
                "Tracked Vehicles",
                "Trailers",
                "Tramcars",
                "Guests",
                "Public",
                "Residents",
                "Public Service Vehicles",
                "Vehicles Under 7.5T",
                "Wide Vehicles",
                "Inflammables"
              ],
              "maxLength": 38,
              "type": [
                "string",
                "null"
              ]
            },
            "type": "array"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/MultiLineString.json"
          },
          "geometry_length": {
            "type": "number"
          },
          "inclusion": {
            "items": {
              "enum": [
                "Access",
                "All Vehicles",
                "Abnormal Loads",
                "Access To Off Street Premises",
                "Articulated Vehicles",
                "Animal Loads",
                "Authorised Vehicles",
                "Buses",
                "Coaches",
                "Customers",
                "Dangerous Goods",
                "Disabled",
                "Emergency Vehicles",
                "Explosives",
                "Emergency Access",
                "Goods Vehicles",
                "Wide Loads",
                "Escorted Traffic",
                "Goods Vehicles Exceeding 1.5T",
                "Goods Vehicles Exceeding 2T",
                "Goods Vehicles Exceeding 2.5T",
                "Goods Vehicles Exceeding 4T",
                "Goods Vehicles Exceeding 3T",
                "Fuel Tankers",
                "Goods Vehicles Exceeding 3.5T",
                "Goods Vehicles Exceeding 5T",
                "Goods Vehicles Exceeding 7.5T",
                "Guided Buses",
                "Goods Vehicles Exceeding 17T",
                "Loading And Unloading",
                "Goods Vehicles Exceeding 16.5T",
                "Local Buses",
                "Goods Vehicles Exceeding 17.5T",
                "Official Business",
                "Goods Vehicles Exceeding 18T",
                "Paying",
                "Goods Vehicles Exceeding 26T",
                "Pedestrians",
                "Goods Vehicles Exceeding 33T",
                "Permit Holders",
                "Heavy Goods Vehicles",
                "Public Transport",
                "Horse Drawn Vehicles",
                "Residents And Guests",
                "Large Vehicles",
                "School Buses",
                "Long Vehicles",
                "Service Vehicles",
                "Light Goods Vehicles",
                "Taxis",
                "Mopeds",
                "Through Traffic",
                "Motor Cycles",
                "Works Traffic",
                "Motor Vehicles",
                "Pedal Cycles",
                "Pedestrians",
                "Ridden Or Accompanied Horses",
                "Towed Caravans",
                "Tracked Vehicles",
                "Trailers",
                "Tramcars",
                "Guests",
                "Public",
                "Residents",
                "Public Service Vehicles",
                "Vehicles Under 7.5T",
                "Wide Vehicles",
                "Inflammables"
              ],
              "maxLength": 38,
              "type": [
                "string",
                "null"
              ]
            },
            "type": "array"
          },
          "measure1_sourceofmeasure": {
            "enum": [
              "Calculated",
              "External",
              "Signed"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "measure1_unitofmeasure": {
            "type": [
              "string",
              "null"
            ]
          },
          "measure1_value": {
            "type": [
              "number",
              "null"
            ]
          },
          "measure2_sourceofmeasure": {
            "enum": [
              "Calculated",
              "External",
              "Signed"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "measure2_unitofmeasure": {
            "type": [
              "string",
              "null"
            ]
          },
          "measure2_value": {
            "type": [
              "number",
              "null"
            ]
          },
          "osid": {
            "type": "string"
          },
          "restriction": {
            "enum": [
              "Forbidden Legally",
              "Mandatory Turn",
              "Maximum Double Axle Weight",
              "Maximum Height",
              "Maximum Length",
              "Maximum Single Axle Weight",
              "Maximum Total Weight",
              "Maximum Triple Axle Weight",
              "Maximum Unladen Weight",
              "Maximum Width",
              "No Turn",
              "One Way",
              "Physically Impossible",
              "Private"
            ],
            "type": "string"
          },
          "restrictionnetworkreference": {
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
                "restrictionid": {
                  "description": "The identifier for the Restriction feature.",
                  "maxLength": 36,
                  "originalName": "restrictionID",
                  "type": "string"
                },
                "restrictionversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "restrictionVersionDate",
                  "pattern": "YYYY-MM-DD",
                  "type": "string"
                },
                "roadlinkdirection": {
                  "description": "The direction in which the restriction applies in direction of digitisation of the Road Link feature.",
                  "enum": [
                    "Both Directions",
                    "In Direction",
                    "In Opposite Direction"
                  ],
                  "maxLength": 21,
                  "originalName": "roadLinkDirection",
                  "type": "string"
                },
                "roadlinksequence": {
                  "description": "The order in which the restriction applies to the referenced Road Link features.",
                  "maxLength": 2,
                  "originalName": "roadLinkSequence",
                  "type": [
                    "integer",
                    "null"
                  ]
                }
              },
              "type": "object"
            },
            "type": "array"
          },
          "structure": {
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
          "timeinterval": {
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
          },
          "trafficsign1": {
            "type": [
              "string",
              "null"
            ]
          },
          "trafficsign2": {
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
          "restriction",
          "theme",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "d731fe04c07a3c9b8ae6765e09883c024156c8df1361a1a7c016473efb6070fd",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Restriction v1"
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
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/queryables",
      "responseSha256": "dcaf38bd52298430f23326ee60ce116973bc5ac302d7bf6da906bbd98098074f",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema",
      "responseSha256": "d731fe04c07a3c9b8ae6765e09883c024156c8df1361a1a7c016473efb6070fd",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/atpositionxcoordinate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/atpositionycoordinate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/datetimequalifier",
      "@type": "rdf:Property",
      "dcterms:identifier": "datetimequalifier",
      "rdfs:label": "datetimequalifier",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "datetimequalifierid": {
                "description": "The OS identifier of the date time qualifier feature.",
                "maxLength": 36,
                "originalName": "dateTimeQualifierID",
                "type": "string"
              },
              "enddate": {
                "description": "The date at which the restriction applied ends. This date will be in the format YYYY-MM-DD.",
                "format": "date",
                "originalName": "endDate",
                "pattern": "YYYY-MM-DD",
                "type": [
                  "string",
                  "null"
                ]
              },
              "endmonthday": {
                "description": "The date at which the restriction applied ends. This date will be in the format MM-DD.",
                "maxLength": 6,
                "originalName": "endMonthDay",
                "type": [
                  "string",
                  "null"
                ]
              },
              "endtime": {
                "description": "The time the restriction ends.",
                "maxLength": 8,
                "originalName": "endTime",
                "type": [
                  "string",
                  "null"
                ]
              },
              "nameddate": {
                "description": "The named month or period this time interval applies to.",
                "enum": [
                  "All Year",
                  "April",
                  "August",
                  "Autumn",
                  "Christmas",
                  "December",
                  "Easter",
                  "February",
                  "January",
                  "July",
                  "June",
                  "March",
                  "May",
                  "November",
                  "October",
                  "September",
                  "Spring",
                  "Summer",
                  "Winter"
                ],
                "maxLength": 9,
                "originalName": "namedDate",
                "type": [
                  "string",
                  "null"
                ]
              },
              "namedday": {
                "description": "The named day this restriction applies to.",
                "enum": [
                  "All Days",
                  "Friday",
                  "Market Days",
                  "Monday",
                  "Public Holidays",
                  "Saturday",
                  "Sunday",
                  "Thursday",
                  "Tuesday",
                  "Wednesday",
                  "Weekdays",
                  "Weekends"
                ],
                "maxLength": 15,
                "originalName": "namedDay",
                "type": [
                  "string",
                  "null"
                ]
              },
              "namedperiod": {
                "description": "A specified period in which the restriction applies.",
                "enum": [
                  "Extreme Weather",
                  "Firing Times",
                  "Local Times Apply",
                  "School Arrival And Departure",
                  "School Holidays",
                  "School Hours",
                  "Special Arrangements",
                  "Term Time"
                ],
                "maxLength": 28,
                "originalName": "namedPeriod",
                "type": [
                  "string",
                  "null"
                ]
              },
              "namedtime": {
                "description": "These are named time periods that do not relate to the same time each day.",
                "enum": [
                  "All Day",
                  "At High Tide",
                  "At Low Tide",
                  "Dawn Till Dusk",
                  "Day",
                  "Dusk Till Dawn",
                  "Evening Rush Hour",
                  "Evenings",
                  "Morning Rush Hour",
                  "Night",
                  "Part Time",
                  "Peak Time"
                ],
                "maxLength": 17,
                "originalName": "namedTime",
                "type": [
                  "string",
                  "null"
                ]
              },
              "restrictionid": {
                "description": "The identifier for the Restriction feature.",
                "maxLength": 36,
                "originalName": "restrictionID",
                "type": "string"
              },
              "restrictionversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "restrictionVersionDate",
                "pattern": "YYYY-MM-DD",
                "type": "string"
              },
              "startdate": {
                "description": "The date at which the restriction applied starts. This date will be in the format YYYY-MM-DD.",
                "format": "date",
                "originalName": "startDate",
                "pattern": "YYYY-MM-DD",
                "type": [
                  "string",
                  "null"
                ]
              },
              "startmonthday": {
                "description": "The date at which the restriction applied starts. This date will be in the format -MM-DD.",
                "maxLength": 6,
                "originalName": "startMonthDay",
                "type": [
                  "string",
                  "null"
                ]
              },
              "starttime": {
                "description": "The time the restriction begins.",
                "maxLength": 8,
                "originalName": "startTime",
                "type": [
                  "string",
                  "null"
                ]
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Access Restriction",
            "One Way",
            "Restriction For Vehicles",
            "Turn Restriction"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/exemption",
      "@type": "rdf:Property",
      "dcterms:identifier": "exemption",
      "rdfs:label": "exemption",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "enum": [
              "Access",
              "All Vehicles",
              "Abnormal Loads",
              "Access To Off Street Premises",
              "Articulated Vehicles",
              "Animal Loads",
              "Authorised Vehicles",
              "Buses",
              "Coaches",
              "Customers",
              "Dangerous Goods",
              "Disabled",
              "Emergency Vehicles",
              "Explosives",
              "Emergency Access",
              "Goods Vehicles",
              "Wide Loads",
              "Escorted Traffic",
              "Goods Vehicles Exceeding 1.5T",
              "Goods Vehicles Exceeding 2T",
              "Goods Vehicles Exceeding 2.5T",
              "Goods Vehicles Exceeding 4T",
              "Goods Vehicles Exceeding 3T",
              "Fuel Tankers",
              "Goods Vehicles Exceeding 3.5T",
              "Goods Vehicles Exceeding 5T",
              "Goods Vehicles Exceeding 7.5T",
              "Guided Buses",
              "Goods Vehicles Exceeding 17T",
              "Loading And Unloading",
              "Goods Vehicles Exceeding 16.5T",
              "Local Buses",
              "Goods Vehicles Exceeding 17.5T",
              "Official Business",
              "Goods Vehicles Exceeding 18T",
              "Paying",
              "Goods Vehicles Exceeding 26T",
              "Pedestrians",
              "Goods Vehicles Exceeding 33T",
              "Permit Holders",
              "Heavy Goods Vehicles",
              "Public Transport",
              "Horse Drawn Vehicles",
              "Residents And Guests",
              "Large Vehicles",
              "School Buses",
              "Long Vehicles",
              "Service Vehicles",
              "Light Goods Vehicles",
              "Taxis",
              "Mopeds",
              "Through Traffic",
              "Motor Cycles",
              "Works Traffic",
              "Motor Vehicles",
              "Pedal Cycles",
              "Pedestrians",
              "Ridden Or Accompanied Horses",
              "Towed Caravans",
              "Tracked Vehicles",
              "Trailers",
              "Tramcars",
              "Guests",
              "Public",
              "Residents",
              "Public Service Vehicles",
              "Vehicles Under 7.5T",
              "Wide Vehicles",
              "Inflammables"
            ],
            "maxLength": 38,
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/geometry_length",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/inclusion",
      "@type": "rdf:Property",
      "dcterms:identifier": "inclusion",
      "rdfs:label": "inclusion",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "enum": [
              "Access",
              "All Vehicles",
              "Abnormal Loads",
              "Access To Off Street Premises",
              "Articulated Vehicles",
              "Animal Loads",
              "Authorised Vehicles",
              "Buses",
              "Coaches",
              "Customers",
              "Dangerous Goods",
              "Disabled",
              "Emergency Vehicles",
              "Explosives",
              "Emergency Access",
              "Goods Vehicles",
              "Wide Loads",
              "Escorted Traffic",
              "Goods Vehicles Exceeding 1.5T",
              "Goods Vehicles Exceeding 2T",
              "Goods Vehicles Exceeding 2.5T",
              "Goods Vehicles Exceeding 4T",
              "Goods Vehicles Exceeding 3T",
              "Fuel Tankers",
              "Goods Vehicles Exceeding 3.5T",
              "Goods Vehicles Exceeding 5T",
              "Goods Vehicles Exceeding 7.5T",
              "Guided Buses",
              "Goods Vehicles Exceeding 17T",
              "Loading And Unloading",
              "Goods Vehicles Exceeding 16.5T",
              "Local Buses",
              "Goods Vehicles Exceeding 17.5T",
              "Official Business",
              "Goods Vehicles Exceeding 18T",
              "Paying",
              "Goods Vehicles Exceeding 26T",
              "Pedestrians",
              "Goods Vehicles Exceeding 33T",
              "Permit Holders",
              "Heavy Goods Vehicles",
              "Public Transport",
              "Horse Drawn Vehicles",
              "Residents And Guests",
              "Large Vehicles",
              "School Buses",
              "Long Vehicles",
              "Service Vehicles",
              "Light Goods Vehicles",
              "Taxis",
              "Mopeds",
              "Through Traffic",
              "Motor Cycles",
              "Works Traffic",
              "Motor Vehicles",
              "Pedal Cycles",
              "Pedestrians",
              "Ridden Or Accompanied Horses",
              "Towed Caravans",
              "Tracked Vehicles",
              "Trailers",
              "Tramcars",
              "Guests",
              "Public",
              "Residents",
              "Public Service Vehicles",
              "Vehicles Under 7.5T",
              "Wide Vehicles",
              "Inflammables"
            ],
            "maxLength": 38,
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/measure1_sourceofmeasure",
      "@type": "rdf:Property",
      "dcterms:identifier": "measure1_sourceofmeasure",
      "rdfs:label": "measure1_sourceofmeasure",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Calculated",
            "External",
            "Signed"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/measure1_unitofmeasure",
      "@type": "rdf:Property",
      "dcterms:identifier": "measure1_unitofmeasure",
      "rdfs:label": "measure1_unitofmeasure",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/measure1_value",
      "@type": "rdf:Property",
      "dcterms:identifier": "measure1_value",
      "rdfs:label": "measure1_value",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/measure2_sourceofmeasure",
      "@type": "rdf:Property",
      "dcterms:identifier": "measure2_sourceofmeasure",
      "rdfs:label": "measure2_sourceofmeasure",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Calculated",
            "External",
            "Signed"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/measure2_unitofmeasure",
      "@type": "rdf:Property",
      "dcterms:identifier": "measure2_unitofmeasure",
      "rdfs:label": "measure2_unitofmeasure",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/measure2_value",
      "@type": "rdf:Property",
      "dcterms:identifier": "measure2_value",
      "rdfs:label": "measure2_value",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/restriction",
      "@type": "rdf:Property",
      "dcterms:identifier": "restriction",
      "rdfs:label": "restriction",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Forbidden Legally",
            "Mandatory Turn",
            "Maximum Double Axle Weight",
            "Maximum Height",
            "Maximum Length",
            "Maximum Single Axle Weight",
            "Maximum Total Weight",
            "Maximum Triple Axle Weight",
            "Maximum Unladen Weight",
            "Maximum Width",
            "No Turn",
            "One Way",
            "Physically Impossible",
            "Private"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/restrictionnetworkreference",
      "@type": "rdf:Property",
      "dcterms:identifier": "restrictionnetworkreference",
      "rdfs:label": "restrictionnetworkreference",
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
              "restrictionid": {
                "description": "The identifier for the Restriction feature.",
                "maxLength": 36,
                "originalName": "restrictionID",
                "type": "string"
              },
              "restrictionversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "restrictionVersionDate",
                "pattern": "YYYY-MM-DD",
                "type": "string"
              },
              "roadlinkdirection": {
                "description": "The direction in which the restriction applies in direction of digitisation of the Road Link feature.",
                "enum": [
                  "Both Directions",
                  "In Direction",
                  "In Opposite Direction"
                ],
                "maxLength": 21,
                "originalName": "roadLinkDirection",
                "type": "string"
              },
              "roadlinksequence": {
                "description": "The order in which the restriction applies to the referenced Road Link features.",
                "maxLength": 2,
                "originalName": "roadLinkSequence",
                "type": [
                  "integer",
                  "null"
                ]
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/structure",
      "@type": "rdf:Property",
      "dcterms:identifier": "structure",
      "rdfs:label": "structure",
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
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/timeinterval",
      "@type": "rdf:Property",
      "dcterms:identifier": "timeinterval",
      "rdfs:label": "timeinterval",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/toid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/trafficsign1",
      "@type": "rdf:Property",
      "dcterms:identifier": "trafficsign1",
      "rdfs:label": "trafficsign1",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/trafficsign2",
      "@type": "rdf:Property",
      "dcterms:identifier": "trafficsign2",
      "rdfs:label": "trafficsign2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-restriction-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1/schema"
      }
    }
  ]
}
---

# Restriction v1

Restriction includes turn restrictions, restriction for vehicles, and access restrictions. Turn restrictions are a restriction based upon a vehicle manoeuvre. This type of restriction includes prohibitive driving instructions, mandatory driving instruction and implicit restrictions. Prohibited instructions are indicated by road signs within a red circle, examples include No U Turn, No Right Turn or No Left Turn. These can include exceptions to the instruction and are typically elements like Except for Buses. Mandatory driving instructions indicated by road signs within a blue circle or painted on the roadway such as Turn Right, Ahead Only and Left Turn. Implicit restrictions occur where a turn is not signed as prohibited but would not be a normal manoeuvre. For example, where a road splits around a traffic island or at complex junctions where additional geometry has been captured to reflect the traffic flow. These are not differentiated from actual signed restrictions. Restriction for vehicles are constraints that apply to the vehicles based on their physical characteristics: height, weight, width and length. These are required to protect structures such as bridges and tunnels from damage, or to restrict/prohibit use by vehicle that exceed specific dimensions, usually for environmental reasons. Restriction for vehicles has been extended to support the full definition of height, weight, width and length restrictions as defined in the UK to ensure that they can: Apply to specific vehicle types only Relate to a structure for which the restriction is designed to protect (for example, a Bridge)

Native identifier: `trn-rami-restriction-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-restriction-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2022-08-24T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
