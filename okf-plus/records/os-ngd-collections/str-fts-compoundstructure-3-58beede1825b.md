---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Compound Structure v3",
  "description": "Polygon feature which encompasses one or more components and represents a manmade construction that has been built for a specific purpose. Examples include a bridge, a dam, and an aqueduct.",
  "nativeIdentifier": "str-fts-compoundstructure-3",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3",
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
      "sourcePointer": "/collections/28",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/28",
      "normalisedRecordSha256": "7503c281fcaffa77bfd08c680ec2924cb6abe8e6564f227f489714ce51e1b446",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3"
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
    "start": "2026-02-19T00:00:00Z",
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
    "description": "Polygon feature which encompasses one or more components and represents a manmade construction that has been built for a specific purpose. Examples include a bridge, a dam, and an aqueduct.",
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
            "2026-02-19T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "str-fts-compoundstructure-3",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3",
        "rel": "self",
        "title": "The 'Compound Structure v3' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/items",
        "rel": "items",
        "title": "The features in the 'Compound Structure v3' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema",
        "rel": "describedby",
        "title": "Schema for the 'Compound Structure v3' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Compound Structure v3' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/queryables",
        "properties": {
          "description": {
            "enum": [
              "Aqueduct",
              "Breakwater",
              "Bridge",
              "Canal Tunnel",
              "Clapper Bridge",
              "Dam",
              "Footbridge",
              "Leisure Pier",
              "Lift Bridge",
              "Natural Subterranean Passage",
              "Pedestrian Tunnel Or Subway",
              "Rail Tunnel",
              "Road Tunnel",
              "Sluice",
              "Swing Bridge",
              "Tanker Berthing",
              "Transporter Bridge",
              "Tube Or Metro Tunnel",
              "Underground Conduit",
              "Underground Flood Relief Channel",
              "Underpass",
              "Viaduct",
              "Watercourse Tunnel"
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
          "name3_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "name4_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "osid": {
            "type": [
              "string"
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
              "string"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "ee9bfaa7e8d41b6413f61137e49dd7ab0670822ad6acfccd05ca13e85b1e1e25",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "str-fts-compoundstructure-3.0",
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
              "Aqueduct",
              "Breakwater",
              "Bridge",
              "Canal Tunnel",
              "Clapper Bridge",
              "Dam",
              "Footbridge",
              "Leisure Pier",
              "Lift Bridge",
              "Natural Subterranean Passage",
              "Pedestrian Tunnel Or Subway",
              "Rail Tunnel",
              "Road Tunnel",
              "Sluice",
              "Swing Bridge",
              "Tanker Berthing",
              "Transporter Bridge",
              "Tube Or Metro Tunnel",
              "Underground Conduit",
              "Underground Flood Relief Channel",
              "Underpass",
              "Viaduct",
              "Watercourse Tunnel"
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
          "name3_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "name3_language": {
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
          "name3_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "name3_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "name4_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "name4_language": {
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
          "name4_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "name4_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "networkover": {
            "enum": [
              "Canal",
              "Multiple",
              "Path",
              "Railway",
              "Road",
              "Water"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "networkunder": {
            "enum": [
              "Canal",
              "Multiple",
              "Path",
              "Railway",
              "Road",
              "Water"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "osid": {
            "type": "string"
          },
          "relatedentity": {
            "items": {
              "properties": {
                "crossreferencefeature": {
                  "description": "Description of the related dataset that the cross reference refers to, for example, 'Third-party Bridge Information'.",
                  "enum": [
                    "Third-party Bridge Information"
                  ],
                  "maxLength": 40,
                  "originalName": "crossReferenceFeature",
                  "type": "string"
                },
                "crossreferenceid": {
                  "description": "Identifier of the related data entity or feature type instance that is the target of the reference or link.",
                  "maxLength": 254,
                  "originalName": "crossReferenceID",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "crossreferencename": {
                  "description": "The bridge name extracted from the third-party bridge information record by OS.",
                  "maxLength": 254,
                  "originalName": "crossReferenceName",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "crossreferencenumber": {
                  "description": "The bridge number extracted from the third-party bridge information record by OS.",
                  "maxLength": 254,
                  "originalName": "crossReferenceNumber",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "crossreferenceprovider": {
                  "description": "The organisation that provided the third-party bridge information record.",
                  "maxLength": 254,
                  "originalName": "crossReferenceProvider",
                  "type": "string"
                },
                "crossreferencetype": {
                  "description": "The bridge type extracted from the third-party bridge information record by OS.",
                  "maxLength": 254,
                  "originalName": "crossReferenceType",
                  "type": [
                    "string",
                    "null"
                  ]
                },
                "featuretypeid": {
                  "description": "OSID assigned by Ordnance Survey to the compound structure as a persistent identifier. This is used along with the Feature Type Version Date attribute to join the component to the Compound Structure Feature Type.",
                  "maxLength": 36,
                  "originalName": "featureTypeID",
                  "type": "string"
                },
                "featuretypeversiondate": {
                  "description": "Date of the feature version to which this related component applies. This is used along with the Feature Type ID attribute to join the component to the Compound Structure Feature Type.",
                  "format": "date",
                  "originalName": "featureTypeVersionDate",
                  "type": "string"
                },
                "relatedentityid": {
                  "description": "Primary key providing a unique row identifier assigned to enable indexing for efficient querying.",
                  "format": "uuid",
                  "maxLength": 36,
                  "originalName": "relatedEntityID",
                  "type": "string"
                },
                "relationshiptype": {
                  "description": "Type of relationship which has been formed between the source and target features, for example, 'Within' or 'Same As'.",
                  "enum": [
                    "Within",
                    "Same As",
                    "Accessed From",
                    "Nearest"
                  ],
                  "maxLength": 30,
                  "originalName": "relationshipType",
                  "type": "string"
                }
              },
              "type": "object"
            },
            "type": "array"
          },
          "status": {
            "enum": [
              "Active",
              "Derelict",
              "Inactive",
              "Under Construction",
              "Unknown"
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
          "geometry_evidencedate",
          "geometry_updatedate",
          "geometry_capturemethod",
          "theme",
          "description",
          "description_evidencedate",
          "description_updatedate",
          "description_capturemethod",
          "name1_text",
          "name1_language",
          "name1_evidencedate",
          "name1_updatedate",
          "name2_text",
          "name2_language",
          "name2_evidencedate",
          "name2_updatedate",
          "name3_text",
          "name3_language",
          "name3_evidencedate",
          "name3_updatedate",
          "name4_text",
          "name4_language",
          "name4_evidencedate",
          "name4_updatedate",
          "status",
          "capturespecification",
          "networkover",
          "networkunder",
          "relatedentity"
        ],
        "requiredUndeclared": [],
        "sha256": "6b69c09f756eb7762e4d1da771b3a6d802ab49c366eb7c229fc4384117042bdf",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Compound Structure v3"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2026-02-19T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/queryables",
      "responseSha256": "ee9bfaa7e8d41b6413f61137e49dd7ab0670822ad6acfccd05ca13e85b1e1e25",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema",
      "responseSha256": "6b69c09f756eb7762e4d1da771b3a6d802ab49c366eb7c229fc4384117042bdf",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/capturespecification",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Aqueduct",
            "Breakwater",
            "Bridge",
            "Canal Tunnel",
            "Clapper Bridge",
            "Dam",
            "Footbridge",
            "Leisure Pier",
            "Lift Bridge",
            "Natural Subterranean Passage",
            "Pedestrian Tunnel Or Subway",
            "Rail Tunnel",
            "Road Tunnel",
            "Sluice",
            "Swing Bridge",
            "Tanker Berthing",
            "Transporter Bridge",
            "Tube Or Metro Tunnel",
            "Underground Conduit",
            "Underground Flood Relief Channel",
            "Underpass",
            "Viaduct",
            "Watercourse Tunnel"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/description_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/description_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/description_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/geometry_area_m2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/geometry_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/geometry_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/geometry_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name1_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name1_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name2_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name2_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name3_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "name3_evidencedate",
      "rdfs:label": "name3_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name3_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "name3_language",
      "rdfs:label": "name3_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name3_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "name3_text",
      "rdfs:label": "name3_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name3_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "name3_updatedate",
      "rdfs:label": "name3_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name4_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "name4_evidencedate",
      "rdfs:label": "name4_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name4_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "name4_language",
      "rdfs:label": "name4_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name4_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "name4_text",
      "rdfs:label": "name4_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/name4_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "name4_updatedate",
      "rdfs:label": "name4_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/networkover",
      "@type": "rdf:Property",
      "dcterms:identifier": "networkover",
      "rdfs:label": "networkover",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Canal",
            "Multiple",
            "Path",
            "Railway",
            "Road",
            "Water"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/networkunder",
      "@type": "rdf:Property",
      "dcterms:identifier": "networkunder",
      "rdfs:label": "networkunder",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Canal",
            "Multiple",
            "Path",
            "Railway",
            "Road",
            "Water"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/relatedentity",
      "@type": "rdf:Property",
      "dcterms:identifier": "relatedentity",
      "rdfs:label": "relatedentity",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "crossreferencefeature": {
                "description": "Description of the related dataset that the cross reference refers to, for example, 'Third-party Bridge Information'.",
                "enum": [
                  "Third-party Bridge Information"
                ],
                "maxLength": 40,
                "originalName": "crossReferenceFeature",
                "type": "string"
              },
              "crossreferenceid": {
                "description": "Identifier of the related data entity or feature type instance that is the target of the reference or link.",
                "maxLength": 254,
                "originalName": "crossReferenceID",
                "type": [
                  "string",
                  "null"
                ]
              },
              "crossreferencename": {
                "description": "The bridge name extracted from the third-party bridge information record by OS.",
                "maxLength": 254,
                "originalName": "crossReferenceName",
                "type": [
                  "string",
                  "null"
                ]
              },
              "crossreferencenumber": {
                "description": "The bridge number extracted from the third-party bridge information record by OS.",
                "maxLength": 254,
                "originalName": "crossReferenceNumber",
                "type": [
                  "string",
                  "null"
                ]
              },
              "crossreferenceprovider": {
                "description": "The organisation that provided the third-party bridge information record.",
                "maxLength": 254,
                "originalName": "crossReferenceProvider",
                "type": "string"
              },
              "crossreferencetype": {
                "description": "The bridge type extracted from the third-party bridge information record by OS.",
                "maxLength": 254,
                "originalName": "crossReferenceType",
                "type": [
                  "string",
                  "null"
                ]
              },
              "featuretypeid": {
                "description": "OSID assigned by Ordnance Survey to the compound structure as a persistent identifier. This is used along with the Feature Type Version Date attribute to join the component to the Compound Structure Feature Type.",
                "maxLength": 36,
                "originalName": "featureTypeID",
                "type": "string"
              },
              "featuretypeversiondate": {
                "description": "Date of the feature version to which this related component applies. This is used along with the Feature Type ID attribute to join the component to the Compound Structure Feature Type.",
                "format": "date",
                "originalName": "featureTypeVersionDate",
                "type": "string"
              },
              "relatedentityid": {
                "description": "Primary key providing a unique row identifier assigned to enable indexing for efficient querying.",
                "format": "uuid",
                "maxLength": 36,
                "originalName": "relatedEntityID",
                "type": "string"
              },
              "relationshiptype": {
                "description": "Type of relationship which has been formed between the source and target features, for example, 'Within' or 'Same As'.",
                "enum": [
                  "Within",
                  "Same As",
                  "Accessed From",
                  "Nearest"
                ],
                "maxLength": 30,
                "originalName": "relationshipType",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/status",
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
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-compoundstructure-3/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3/schema"
      }
    }
  ]
}
---

# Compound Structure v3

Polygon feature which encompasses one or more components and represents a manmade construction that has been built for a specific purpose. Examples include a bridge, a dam, and an aqueduct.

Native identifier: `str-fts-compoundstructure-3`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-compoundstructure-3)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2026-02-19T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
