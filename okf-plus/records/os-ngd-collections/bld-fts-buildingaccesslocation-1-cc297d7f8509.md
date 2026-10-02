---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Building Access Location v1",
  "description": "Feature which has a point geometry and represents the locations where pedestrians and / or vehicles can enter or exit a building.",
  "nativeIdentifier": "bld-fts-buildingaccesslocation-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1",
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
      "sourcePointer": "/collections/6",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/6",
      "normalisedRecordSha256": "b90269b0c55de188e53a19a45981b408b64d8b0f2f79eca0d69ab74852bca195",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1"
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
    "start": "2025-03-01T00:00:00Z",
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
    "description": "Feature which has a point geometry and represents the locations where pedestrians and / or vehicles can enter or exit a building.",
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
            "2025-03-01T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "bld-fts-buildingaccesslocation-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1",
        "rel": "self",
        "title": "The 'Building Access Location v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/items",
        "rel": "items",
        "title": "The features in the 'Building Access Location v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Building Access Location v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Building Access Location v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/queryables",
        "properties": {
          "access_level": {
            "enum": [
              "Above Surface Level",
              "Below Surface Level",
              "Surface Level"
            ],
            "type": [
              "string"
            ]
          },
          "access_mode": {
            "enum": [
              "Pedestrian",
              "Pedestrian And Vehicular",
              "Vehicular"
            ],
            "type": [
              "string"
            ]
          },
          "access_obstruction": {
            "items": {
              "enum": [
                "No Obstruction",
                "Other Obstruction",
                "Ramp",
                "Step"
              ],
              "enumeration": true,
              "maxLength": 30,
              "type": [
                "string"
              ]
            },
            "type": [
              "array"
            ]
          },
          "access_purpose": {
            "enum": [
              "Emergency",
              "Primary Public",
              "Private",
              "Public"
            ],
            "type": [
              "string"
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
        "sha256": "8b8a8551e879ed6676a2e93f195a98e7038d26308b7a47ac0296698c3d4688e1",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "bld-fts-buildingaccesslocation-1.1",
        "properties": {
          "access_evidencedate": {
            "format": "date",
            "type": "string"
          },
          "access_level": {
            "enum": [
              "Above Surface Level",
              "Below Surface Level",
              "Surface Level"
            ],
            "type": "string"
          },
          "access_mode": {
            "enum": [
              "Pedestrian",
              "Pedestrian And Vehicular",
              "Vehicular"
            ],
            "type": "string"
          },
          "access_obstruction": {
            "items": {
              "enum": [
                "No Obstruction",
                "Other Obstruction",
                "Ramp",
                "Step"
              ],
              "maxLength": 30,
              "type": "string"
            },
            "type": "array"
          },
          "access_purpose": {
            "enum": [
              "Emergency",
              "Primary Public",
              "Private",
              "Public"
            ],
            "type": "string"
          },
          "access_updatedate": {
            "format": "date",
            "type": "string"
          },
          "accessedbuildingid": {
            "format": "uuid",
            "type": [
              "string",
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
          "description": {
            "enum": [
              "Building Access Location"
            ],
            "type": "string"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/Point.json",
            "type": "object"
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
            "type": "string"
          },
          "geometry_updatedate": {
            "format": "date",
            "type": "string"
          },
          "osid": {
            "format": "uuid",
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
          "geometry_evidencedate",
          "geometry_updatedate",
          "geometry_capturemethod",
          "theme",
          "description",
          "access_mode",
          "access_purpose",
          "access_obstruction",
          "access_level",
          "access_evidencedate",
          "access_updatedate",
          "accessedbuildingid"
        ],
        "requiredUndeclared": [],
        "sha256": "de82cd3d78c51f5b64d283ddf251857c09f0c2eae8f1292213a68eedfef398ff",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Building Access Location v1"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2025-03-01T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/queryables",
      "responseSha256": "8b8a8551e879ed6676a2e93f195a98e7038d26308b7a47ac0296698c3d4688e1",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema",
      "responseSha256": "de82cd3d78c51f5b64d283ddf251857c09f0c2eae8f1292213a68eedfef398ff",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/access_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "access_evidencedate",
      "rdfs:label": "access_evidencedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/access_level",
      "@type": "rdf:Property",
      "dcterms:identifier": "access_level",
      "rdfs:label": "access_level",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Above Surface Level",
            "Below Surface Level",
            "Surface Level"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/access_mode",
      "@type": "rdf:Property",
      "dcterms:identifier": "access_mode",
      "rdfs:label": "access_mode",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Pedestrian",
            "Pedestrian And Vehicular",
            "Vehicular"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/access_obstruction",
      "@type": "rdf:Property",
      "dcterms:identifier": "access_obstruction",
      "rdfs:label": "access_obstruction",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "enum": [
              "No Obstruction",
              "Other Obstruction",
              "Ramp",
              "Step"
            ],
            "maxLength": 30,
            "type": "string"
          },
          "type": "array"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/access_purpose",
      "@type": "rdf:Property",
      "dcterms:identifier": "access_purpose",
      "rdfs:label": "access_purpose",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Emergency",
            "Primary Public",
            "Private",
            "Public"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/access_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "access_updatedate",
      "rdfs:label": "access_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/accessedbuildingid",
      "@type": "rdf:Property",
      "dcterms:identifier": "accessedbuildingid",
      "rdfs:label": "accessedbuildingid",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "uuid",
          "type": [
            "string",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Building Access Location"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/geometry",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry",
      "rdfs:label": "geometry",
      "okfp:schemaDefinition": {
        "@value": {
          "$ref": "https://geojson.org/schema/Point.json",
          "type": "object"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/geometry_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/geometry_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry_evidencedate",
      "rdfs:label": "geometry_evidencedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/geometry_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/bld-fts-buildingaccesslocation-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1/schema"
      }
    }
  ]
}
---

# Building Access Location v1

Feature which has a point geometry and represents the locations where pedestrians and / or vehicles can enter or exit a building.

Native identifier: `bld-fts-buildingaccesslocation-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingaccesslocation-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2025-03-01T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
