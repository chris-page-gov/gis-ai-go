---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Highway Dedication v1",
  "description": "Highway dedication provides an indication of the type of Highway user who has access to that particular section of the Highway. Against every section of geometry supplied by the local highway authority there will be one of eight different types of Highway Dedication defined in the Highways Act 1980 and the Countryside and Rights of Way Act 2000 which determines the Highway user access. There can only be one Highway Dedication type applied to the geometry at any given date or time.",
  "nativeIdentifier": "trn-rami-highwaydedication-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1",
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
      "sourcePointer": "/collections/71",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/71",
      "normalisedRecordSha256": "9c68c8ba71fc61f323a2c87a4957a1d38d3c04a69ab92b4154aa31546faeae10",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1"
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
    "description": "Highway dedication provides an indication of the type of Highway user who has access to that particular section of the Highway.\nAgainst every section of geometry supplied by the local highway authority there will be one of eight different types of Highway Dedication defined in the Highways Act 1980 and the Countryside and Rights of Way Act 2000 which determines the Highway user access.\nThere can only be one Highway Dedication type applied to the geometry at any given date or time.",
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
    "id": "trn-rami-highwaydedication-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1",
        "rel": "self",
        "title": "The 'Highway Dedication v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/items",
        "rel": "items",
        "title": "The features in the 'Highway Dedication v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Highway Dedication v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Highway Dedication v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/queryables",
        "properties": {
          "authorityid": {
            "type": [
              "string"
            ]
          },
          "description": {
            "enum": [
              "All Vehicles",
              "Bridleway",
              "Byway Open To All Traffic",
              "Cycle Track Or Cycle Way",
              "Motorway",
              "No Dedication Or Dedication Unknown",
              "Pedestrian Way Or Footpath",
              "Restricted Byway"
            ],
            "type": [
              "string"
            ]
          },
          "geometry_length": {
            "type": [
              "number"
            ]
          },
          "nationalcycleroute": {
            "type": [
              "boolean"
            ]
          },
          "obstruction": {
            "type": [
              "boolean"
            ]
          },
          "osid": {
            "type": [
              "string"
            ]
          },
          "planningorder": {
            "type": [
              "boolean",
              "null"
            ]
          },
          "publicrightofway": {
            "type": [
              "boolean"
            ]
          },
          "quietroute": {
            "type": [
              "boolean",
              "null"
            ]
          },
          "worksprohibited": {
            "type": [
              "boolean",
              "null"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "e77c241fad56f4dd9356498982c9f341363b6a318167c0f9b456901c865e9ccf",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-rami-highwaydedication-1.0",
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
          "description": {
            "enum": [
              "All Vehicles",
              "Bridleway",
              "Byway Open To All Traffic",
              "Cycle Track Or Cycle Way",
              "Motorway",
              "No Dedication Or Dedication Unknown",
              "Pedestrian Way Or Footpath",
              "Restricted Byway"
            ],
            "type": "string"
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
            "$ref": "https://geojson.org/schema/LineString.json"
          },
          "geometry_length": {
            "type": "number"
          },
          "highwaydedicationnetworkreference": {
            "items": {
              "properties": {
                "highwaydedicationid": {
                  "description": "The identifier of the highway dedication feature.",
                  "maxLength": 36,
                  "originalName": "highwayDedicationID",
                  "type": "string"
                },
                "highwaydedicationversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "highwayDedicationVersionDate",
                  "pattern": "YYYY-MM-DD",
                  "type": "string"
                },
                "networkfeaturetype": {
                  "description": "The type of network feature referenced.",
                  "enum": [
                    "Path Link",
                    "Road Link",
                    "Street"
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
                }
              },
              "type": "object"
            },
            "type": "array"
          },
          "nationalcycleroute": {
            "type": "boolean"
          },
          "obstruction": {
            "type": "boolean"
          },
          "osid": {
            "type": "string"
          },
          "planningorder": {
            "type": [
              "boolean",
              "null"
            ]
          },
          "publicrightofway": {
            "type": "boolean"
          },
          "quietroute": {
            "type": [
              "boolean",
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
          },
          "worksprohibited": {
            "type": [
              "boolean",
              "null"
            ]
          }
        },
        "required": [
          "authorityid",
          "changetype",
          "description",
          "effectivestartdate",
          "geometry",
          "geometry_length",
          "nationalcycleroute",
          "obstruction",
          "osid",
          "publicrightofway",
          "theme",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "949f2eb7b11bbf48de535e503fd4e934c33c4148b382144aea31b55e4b75b64e",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Highway Dedication v1"
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
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/queryables",
      "responseSha256": "e77c241fad56f4dd9356498982c9f341363b6a318167c0f9b456901c865e9ccf",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema",
      "responseSha256": "949f2eb7b11bbf48de535e503fd4e934c33c4148b382144aea31b55e4b75b64e",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/authorityid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "All Vehicles",
            "Bridleway",
            "Byway Open To All Traffic",
            "Cycle Track Or Cycle Way",
            "Motorway",
            "No Dedication Or Dedication Unknown",
            "Pedestrian Way Or Footpath",
            "Restricted Byway"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/effectiveenddate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/effectivestartdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/geometry",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry",
      "rdfs:label": "geometry",
      "okfp:schemaDefinition": {
        "@value": {
          "$ref": "https://geojson.org/schema/LineString.json"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/geometry_length",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/highwaydedicationnetworkreference",
      "@type": "rdf:Property",
      "dcterms:identifier": "highwaydedicationnetworkreference",
      "rdfs:label": "highwaydedicationnetworkreference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "highwaydedicationid": {
                "description": "The identifier of the highway dedication feature.",
                "maxLength": 36,
                "originalName": "highwayDedicationID",
                "type": "string"
              },
              "highwaydedicationversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "highwayDedicationVersionDate",
                "pattern": "YYYY-MM-DD",
                "type": "string"
              },
              "networkfeaturetype": {
                "description": "The type of network feature referenced.",
                "enum": [
                  "Path Link",
                  "Road Link",
                  "Street"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/nationalcycleroute",
      "@type": "rdf:Property",
      "dcterms:identifier": "nationalcycleroute",
      "rdfs:label": "nationalcycleroute",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "boolean"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/obstruction",
      "@type": "rdf:Property",
      "dcterms:identifier": "obstruction",
      "rdfs:label": "obstruction",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "boolean"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/planningorder",
      "@type": "rdf:Property",
      "dcterms:identifier": "planningorder",
      "rdfs:label": "planningorder",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/publicrightofway",
      "@type": "rdf:Property",
      "dcterms:identifier": "publicrightofway",
      "rdfs:label": "publicrightofway",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "boolean"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/quietroute",
      "@type": "rdf:Property",
      "dcterms:identifier": "quietroute",
      "rdfs:label": "quietroute",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-highwaydedication-1/field/worksprohibited",
      "@type": "rdf:Property",
      "dcterms:identifier": "worksprohibited",
      "rdfs:label": "worksprohibited",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1/schema"
      }
    }
  ]
}
---

# Highway Dedication v1

Highway dedication provides an indication of the type of Highway user who has access to that particular section of the Highway. Against every section of geometry supplied by the local highway authority there will be one of eight different types of Highway Dedication defined in the Highways Act 1980 and the Countryside and Rights of Way Act 2000 which determines the Highway user access. There can only be one Highway Dedication type applied to the geometry at any given date or time.

Native identifier: `trn-rami-highwaydedication-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-highwaydedication-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2022-08-24T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
