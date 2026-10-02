---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Road v1",
  "description": "A road feature is a link set which represents a collection of road link features that share the same name (for example, Bilston Road) or classification number (for example, A41), used primarily by motorised vehicles. A road will reference the complete collection of road link features irrespective of which authority boundary it falls within. The feature type will include Motorways, A Roads, B Roads, and Named Thoroughfares (roads). The link set may not be contiguous across junctions or where a classified road consists of separate sections, which may be separated by some considerable distance. In addition, the same road link feature may be referenced by multiple road features.",
  "nativeIdentifier": "trn-ntwk-road-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1",
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
      "sourcePointer": "/collections/60",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/60",
      "normalisedRecordSha256": "e33b9eea10e803dbf8f4ff931a674895c9d5a45ec4f28535641c379decec7eb6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1"
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
    "start": "2022-08-23T00:00:00Z",
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
    "description": "A road feature is a link set which represents a collection of road link features that share the same name (for example, Bilston Road) or classification number (for example, A41), used primarily by motorised vehicles. A road will reference the complete collection of road link features irrespective of which authority boundary it falls within. The feature type will include Motorways, A Roads, B Roads, and Named Thoroughfares (roads). The link set may not be contiguous across junctions or where a classified road consists of separate sections, which may be separated by some considerable distance. In addition, the same road link feature may be referenced by multiple road features.",
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
            "2022-08-23T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "trn-ntwk-road-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1",
        "rel": "self",
        "title": "The 'Road v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/items",
        "rel": "items",
        "title": "The features in the 'Road v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Road v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Road v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/queryables",
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
            "type": [
              "string"
            ]
          },
          "designatedname1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "designatedname2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "geometry_length": {
            "type": [
              "number"
            ]
          },
          "nationalroadcode": {
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
          "roadclassification": {
            "enum": [
              "A Road",
              "B Road",
              "Classified Unnumbered",
              "Motorway",
              "Not Classified",
              "Unclassified",
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
        "sha256": "257fa4a97af5dc5332685cfa3d7dcca71b94adca23d73e06ae67f5634b69b83e",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-ntwk-road-1.1",
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
              "Road"
            ],
            "type": "string"
          },
          "designatedname1_language": {
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
          "designatedname1_responsibleauthorityidentifier": {
            "type": [
              "string",
              "null"
            ]
          },
          "designatedname1_responsibleauthorityname": {
            "type": [
              "string",
              "null"
            ]
          },
          "designatedname1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "designatedname2_language": {
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
          "designatedname2_responsibleauthorityidentifier": {
            "type": [
              "string",
              "null"
            ]
          },
          "designatedname2_responsibleauthorityname": {
            "type": [
              "string",
              "null"
            ]
          },
          "designatedname2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/MultiLineString.json"
          },
          "geometry_length": {
            "type": "number"
          },
          "nationalroadcode": {
            "type": [
              "string",
              "null"
            ]
          },
          "osid": {
            "type": "string"
          },
          "roadclassification": {
            "enum": [
              "A Road",
              "B Road",
              "Classified Unnumbered",
              "Motorway",
              "Not Classified",
              "Unclassified",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "roadlinkreference": {
            "items": {
              "properties": {
                "roadid": {
                  "description": "The identifier for the Road feature.",
                  "maxLength": 36,
                  "originalName": "roadID",
                  "type": "string"
                },
                "roadlinkid": {
                  "description": "The identifier of the road link feature.",
                  "maxLength": 36,
                  "originalName": "roadLinkID",
                  "type": "string"
                },
                "roadversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "roadVersionDate",
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
          "changetype",
          "description",
          "geometry",
          "geometry_length",
          "osid",
          "theme",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "75bfb21e6c284524a87b9cafb00b75137527b155f6e32fe7ac1f0b89db7c6516",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Road v1"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2022-08-23T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/queryables",
      "responseSha256": "257fa4a97af5dc5332685cfa3d7dcca71b94adca23d73e06ae67f5634b69b83e",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema",
      "responseSha256": "75bfb21e6c284524a87b9cafb00b75137527b155f6e32fe7ac1f0b89db7c6516",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/changetype",
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
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Road"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/designatedname1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "designatedname1_language",
      "rdfs:label": "designatedname1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/designatedname1_responsibleauthorityidentifier",
      "@type": "rdf:Property",
      "dcterms:identifier": "designatedname1_responsibleauthorityidentifier",
      "rdfs:label": "designatedname1_responsibleauthorityidentifier",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/designatedname1_responsibleauthorityname",
      "@type": "rdf:Property",
      "dcterms:identifier": "designatedname1_responsibleauthorityname",
      "rdfs:label": "designatedname1_responsibleauthorityname",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/designatedname1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "designatedname1_text",
      "rdfs:label": "designatedname1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/designatedname2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "designatedname2_language",
      "rdfs:label": "designatedname2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/designatedname2_responsibleauthorityidentifier",
      "@type": "rdf:Property",
      "dcterms:identifier": "designatedname2_responsibleauthorityidentifier",
      "rdfs:label": "designatedname2_responsibleauthorityidentifier",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/designatedname2_responsibleauthorityname",
      "@type": "rdf:Property",
      "dcterms:identifier": "designatedname2_responsibleauthorityname",
      "rdfs:label": "designatedname2_responsibleauthorityname",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/designatedname2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "designatedname2_text",
      "rdfs:label": "designatedname2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/geometry_length",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/nationalroadcode",
      "@type": "rdf:Property",
      "dcterms:identifier": "nationalroadcode",
      "rdfs:label": "nationalroadcode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/roadclassification",
      "@type": "rdf:Property",
      "dcterms:identifier": "roadclassification",
      "rdfs:label": "roadclassification",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "A Road",
            "B Road",
            "Classified Unnumbered",
            "Motorway",
            "Not Classified",
            "Unclassified",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/roadlinkreference",
      "@type": "rdf:Property",
      "dcterms:identifier": "roadlinkreference",
      "rdfs:label": "roadlinkreference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "roadid": {
                "description": "The identifier for the Road feature.",
                "maxLength": 36,
                "originalName": "roadID",
                "type": "string"
              },
              "roadlinkid": {
                "description": "The identifier of the road link feature.",
                "maxLength": 36,
                "originalName": "roadLinkID",
                "type": "string"
              },
              "roadversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "roadVersionDate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/toid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-road-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1/schema"
      }
    }
  ]
}
---

# Road v1

A road feature is a link set which represents a collection of road link features that share the same name (for example, Bilston Road) or classification number (for example, A41), used primarily by motorised vehicles. A road will reference the complete collection of road link features irrespective of which authority boundary it falls within. The feature type will include Motorways, A Roads, B Roads, and Named Thoroughfares (roads). The link set may not be contiguous across junctions or where a classified road consists of separate sections, which may be separated by some considerable distance. In addition, the same road link feature may be referenced by multiple road features.

Native identifier: `trn-ntwk-road-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-road-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2022-08-23T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
