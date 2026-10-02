---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Special Designation Area v1",
  "description": "Special Designations are statutory and advisory designations that can be applied to protect a highway when street or road works are to be undertaken. A Special Designation feature will reference back to the Roads product through Network Reference and will reference a Street Feature. Features which are a partial reference will provide a Network Reference Location.",
  "nativeIdentifier": "trn-rami-specialdesignationarea-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1",
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
      "sourcePointer": "/collections/81",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/81",
      "normalisedRecordSha256": "e4fadfb8d7a3b2112d0a0a5c6dc4fcf9ec64fd0a651df7179bc6e12f4b0c386a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1"
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
    "start": "2022-09-08T00:00:00Z",
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
    "description": "Special Designations are statutory and advisory designations that can be applied to protect a highway when street or road works are to be undertaken. A Special Designation feature will reference back to the Roads product through Network Reference and will reference a Street Feature. Features which are a partial reference will provide a Network Reference Location.",
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
            "2022-09-08T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "trn-rami-specialdesignationarea-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1",
        "rel": "self",
        "title": "The 'Special Designation Area v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/items",
        "rel": "items",
        "title": "The features in the 'Special Designation Area v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Special Designation Area v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Special Designation Area v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/queryables",
        "properties": {
          "authorityid": {
            "type": [
              "string"
            ]
          },
          "contactauthority_authorityname": {
            "type": [
              "string",
              "null"
            ]
          },
          "contactauthority_identifier": {
            "type": [
              "string",
              "null"
            ]
          },
          "description": {
            "enum": [
              "Maintenance",
              "Reinstatement",
              "Special Designation"
            ],
            "type": [
              "string"
            ]
          },
          "designation": {
            "enum": [
              "Drainage And Flood Risk",
              "Emergency Services Routes",
              "Environmentally Sensitive Areas",
              "Event Information",
              "HGV Approved Routes",
              "Hazardous Materials",
              "Lane Rental",
              "Level Crossing Safety Zone",
              "Local Considerations",
              "Parking Bays And Restrictions",
              "Pedestrian Crossings, Traffic Signals And Traffic Sensors",
              "Pipelines And Specialist Cables",
              "Priority Lanes",
              "Proposed Special Engineering Difficulty",
              "Protected Street",
              "Road Trees",
              "Service Strips",
              "Special Engineering Difficulty",
              "Special Event",
              "Speed Limits",
              "Strategic Route",
              "Street Lighting",
              "Streets Subject To Early Notification Of Immediate Activities",
              "Structures",
              "Traffic Calming Features",
              "Traffic Sensitive Side Road When Temporary Traffic Control Is Employed",
              "Traffic Sensitive Street",
              "Transport Authority Critical Apparatus",
              "Unusual Traffic Layout",
              "Winter Maintenance Routes"
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
          "usrn": {
            "type": [
              "integer"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "9fa940936f48e35586032868388411750894fa3b7331e0313dc0635b78e4062c",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-rami-specialdesignationarea-1.0",
        "properties": {
          "authorityid": {
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
          "contactauthority_authorityname": {
            "type": [
              "string",
              "null"
            ]
          },
          "contactauthority_identifier": {
            "type": [
              "string",
              "null"
            ]
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
                "specialdesignationid": {
                  "description": "The identifier for the Special Designation feature.",
                  "maxLength": 36,
                  "originalName": "specialDesignationID",
                  "type": "string"
                },
                "specialdesignationversiondate": {
                  "description": "The version date of the Special Designation feature.",
                  "format": "date",
                  "originalName": "specialDesignationVersionDate",
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
              "Maintenance",
              "Reinstatement",
              "Special Designation"
            ],
            "type": "string"
          },
          "designation": {
            "enum": [
              "Drainage And Flood Risk",
              "Emergency Services Routes",
              "Environmentally Sensitive Areas",
              "Event Information",
              "HGV Approved Routes",
              "Hazardous Materials",
              "Lane Rental",
              "Level Crossing Safety Zone",
              "Local Considerations",
              "Parking Bays And Restrictions",
              "Pedestrian Crossings, Traffic Signals And Traffic Sensors",
              "Pipelines And Specialist Cables",
              "Priority Lanes",
              "Proposed Special Engineering Difficulty",
              "Protected Street",
              "Road Trees",
              "Service Strips",
              "Special Engineering Difficulty",
              "Special Event",
              "Speed Limits",
              "Strategic Route",
              "Street Lighting",
              "Streets Subject To Early Notification Of Immediate Activities",
              "Structures",
              "Traffic Calming Features",
              "Traffic Sensitive Side Road When Temporary Traffic Control Is Employed",
              "Traffic Sensitive Street",
              "Transport Authority Critical Apparatus",
              "Unusual Traffic Layout",
              "Winter Maintenance Routes"
            ],
            "type": "string"
          },
          "designationdescription": {
            "type": [
              "string",
              "null"
            ]
          },
          "effectiveenddate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "effectivestartdate": {
            "format": "date",
            "type": "string"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/MultiPolygon.json"
          },
          "geometry_area": {
            "type": "number"
          },
          "locationdescription": {
            "type": [
              "string",
              "null"
            ]
          },
          "osid": {
            "type": "string"
          },
          "partialreference": {
            "type": "boolean"
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
          "usrn": {
            "type": "integer"
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
          "authorityid",
          "changetype",
          "description",
          "designation",
          "effectivestartdate",
          "geometry",
          "geometry_area",
          "osid",
          "partialreference",
          "theme",
          "usrn",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "a6e5d38e70d86afc80f6489ad101c55c04cd0e96f78376bf8d2e96a3f91def2d",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Special Designation Area v1"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2022-09-08T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/queryables",
      "responseSha256": "9fa940936f48e35586032868388411750894fa3b7331e0313dc0635b78e4062c",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema",
      "responseSha256": "a6e5d38e70d86afc80f6489ad101c55c04cd0e96f78376bf8d2e96a3f91def2d",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/authorityid",
      "@type": "rdf:Property",
      "dcterms:identifier": "authorityid",
      "rdfs:label": "authorityid",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/contactauthority_authorityname",
      "@type": "rdf:Property",
      "dcterms:identifier": "contactauthority_authorityname",
      "rdfs:label": "contactauthority_authorityname",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/contactauthority_identifier",
      "@type": "rdf:Property",
      "dcterms:identifier": "contactauthority_identifier",
      "rdfs:label": "contactauthority_identifier",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/datetimequalifier",
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
              "specialdesignationid": {
                "description": "The identifier for the Special Designation feature.",
                "maxLength": 36,
                "originalName": "specialDesignationID",
                "type": "string"
              },
              "specialdesignationversiondate": {
                "description": "The version date of the Special Designation feature.",
                "format": "date",
                "originalName": "specialDesignationVersionDate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Maintenance",
            "Reinstatement",
            "Special Designation"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/designation",
      "@type": "rdf:Property",
      "dcterms:identifier": "designation",
      "rdfs:label": "designation",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Drainage And Flood Risk",
            "Emergency Services Routes",
            "Environmentally Sensitive Areas",
            "Event Information",
            "HGV Approved Routes",
            "Hazardous Materials",
            "Lane Rental",
            "Level Crossing Safety Zone",
            "Local Considerations",
            "Parking Bays And Restrictions",
            "Pedestrian Crossings, Traffic Signals And Traffic Sensors",
            "Pipelines And Specialist Cables",
            "Priority Lanes",
            "Proposed Special Engineering Difficulty",
            "Protected Street",
            "Road Trees",
            "Service Strips",
            "Special Engineering Difficulty",
            "Special Event",
            "Speed Limits",
            "Strategic Route",
            "Street Lighting",
            "Streets Subject To Early Notification Of Immediate Activities",
            "Structures",
            "Traffic Calming Features",
            "Traffic Sensitive Side Road When Temporary Traffic Control Is Employed",
            "Traffic Sensitive Street",
            "Transport Authority Critical Apparatus",
            "Unusual Traffic Layout",
            "Winter Maintenance Routes"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/designationdescription",
      "@type": "rdf:Property",
      "dcterms:identifier": "designationdescription",
      "rdfs:label": "designationdescription",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/effectiveenddate",
      "@type": "rdf:Property",
      "dcterms:identifier": "effectiveenddate",
      "rdfs:label": "effectiveenddate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/effectivestartdate",
      "@type": "rdf:Property",
      "dcterms:identifier": "effectivestartdate",
      "rdfs:label": "effectivestartdate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/geometry",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry",
      "rdfs:label": "geometry",
      "okfp:schemaDefinition": {
        "@value": {
          "$ref": "https://geojson.org/schema/MultiPolygon.json"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/geometry_area",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/locationdescription",
      "@type": "rdf:Property",
      "dcterms:identifier": "locationdescription",
      "rdfs:label": "locationdescription",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/partialreference",
      "@type": "rdf:Property",
      "dcterms:identifier": "partialreference",
      "rdfs:label": "partialreference",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "boolean"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/timeinterval",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/usrn",
      "@type": "rdf:Property",
      "dcterms:identifier": "usrn",
      "rdfs:label": "usrn",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-specialdesignationarea-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1/schema"
      }
    }
  ]
}
---

# Special Designation Area v1

Special Designations are statutory and advisory designations that can be applied to protect a highway when street or road works are to be undertaken. A Special Designation feature will reference back to the Roads product through Network Reference and will reference a Street Feature. Features which are a partial reference will provide a Network Reference Location.

Native identifier: `trn-rami-specialdesignationarea-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-specialdesignationarea-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2022-09-08T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
