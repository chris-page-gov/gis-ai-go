---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Railway Link Set v1",
  "description": "A Railway Link Set depicts the full extent of a named railway as one continuous line.",
  "nativeIdentifier": "trn-ntwk-railwaylinkset-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1",
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
      "sourcePointer": "/collections/58",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/58",
      "normalisedRecordSha256": "ca0eb44de7b9b3be8f6ea7e9f3f750046c67beb597d2f3a94935b9fe907418c9",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1"
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
    "start": "2023-08-22T00:00:00Z",
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
    "description": "A Railway Link Set depicts the full extent of a named railway as one continuous line.",
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
            "2023-08-22T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "trn-ntwk-railwaylinkset-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1",
        "rel": "self",
        "title": "The 'Railway Link Set v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/items",
        "rel": "items",
        "title": "The features in the 'Railway Link Set v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Railway Link Set v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Railway Link Set v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/queryables",
        "properties": {
          "geometry_length_m": {
            "type": [
              "number"
            ]
          },
          "name1_text": {
            "type": [
              "string"
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
            "format": "uuid",
            "type": [
              "string"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "8c7ede79e8e4b4d650384f42096bd8ed0f2be0aafa65fc2dc940aa449af360d3",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-ntwk-railwaylinkset-1.1",
        "properties": {
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
              "Railway Link Set"
            ],
            "type": "string"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/MultiLineString.json"
          },
          "geometry_length_m": {
            "type": "number"
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
            "type": "string"
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
          "osid": {
            "format": "uuid",
            "type": "string"
          },
          "railwaylinkreference": {
            "items": {
              "properties": {
                "railwaylinkid": {
                  "description": "The indentifier for the RailwayLink feature.",
                  "format": "uuid",
                  "maxLength": 36,
                  "originalName": "railwayLinkID",
                  "type": "string"
                },
                "railwaylinksetid": {
                  "description": "The indentifier for the RailwayLinkSet feature.",
                  "format": "uuid",
                  "maxLength": 36,
                  "originalName": "railwayLinkSetID",
                  "type": "string"
                },
                "railwaylinksetversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "railwayLinkSetVersionDate",
                  "pattern": "YYYY-MM-DD",
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
          "geometry_length_m",
          "name1_text",
          "osid",
          "theme",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "bfeeec01652f20232c57ea0a0b0109ed9a85586cde450b9189dfcebb21df08ef",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Railway Link Set v1"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2023-08-22T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/queryables",
      "responseSha256": "8c7ede79e8e4b4d650384f42096bd8ed0f2be0aafa65fc2dc940aa449af360d3",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema",
      "responseSha256": "bfeeec01652f20232c57ea0a0b0109ed9a85586cde450b9189dfcebb21df08ef",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Railway Link Set"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/geometry_length_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry_length_m",
      "rdfs:label": "geometry_length_m",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/name1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/name1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "name1_text",
      "rdfs:label": "name1_text",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/name2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/name3_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/name3_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/name4_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/name4_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/railwaylinkreference",
      "@type": "rdf:Property",
      "dcterms:identifier": "railwaylinkreference",
      "rdfs:label": "railwaylinkreference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "railwaylinkid": {
                "description": "The indentifier for the RailwayLink feature.",
                "format": "uuid",
                "maxLength": 36,
                "originalName": "railwayLinkID",
                "type": "string"
              },
              "railwaylinksetid": {
                "description": "The indentifier for the RailwayLinkSet feature.",
                "format": "uuid",
                "maxLength": 36,
                "originalName": "railwayLinkSetID",
                "type": "string"
              },
              "railwaylinksetversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "railwayLinkSetVersionDate",
                "pattern": "YYYY-MM-DD",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-railwaylinkset-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1/schema"
      }
    }
  ]
}
---

# Railway Link Set v1

A Railway Link Set depicts the full extent of a named railway as one continuous line.

Native identifier: `trn-ntwk-railwaylinkset-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-railwaylinkset-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2023-08-22T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
