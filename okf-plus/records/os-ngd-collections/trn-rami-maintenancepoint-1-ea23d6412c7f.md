---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Maintenance Point v1",
  "description": "A feature which has a point geometry and provides information about whether the road is maintained at public expense by a national or local highway authority, a road authority or is maintained by another responsible organisation (i.e. not maintained at public expense). If a path is prospectively maintainable at public expense, then this is not currently maintained by a road or highway authority, but the responsible organisation has started the process for a highway or road authority to become responsible for the maintenance of the street at public expense.",
  "nativeIdentifier": "trn-rami-maintenancepoint-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1",
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
      "sourcePointer": "/collections/74",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/74",
      "normalisedRecordSha256": "aed0010145b806c85ed2a113e48f5b9613deca1004e64bea7fbe09e42eb71dfb",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1"
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
    "description": "A feature which has a point geometry and provides information about whether the road is maintained at public expense by a national or local highway authority, a road authority or is maintained by another responsible organisation (i.e. not maintained at public expense). If a path is prospectively maintainable at public expense, then this is not currently maintained by a road or highway authority, but the responsible organisation has started the process for a highway or road authority to become responsible for the maintenance of the street at public expense.",
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
    "id": "trn-rami-maintenancepoint-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1",
        "rel": "self",
        "title": "The 'Maintenance Point v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/items",
        "rel": "items",
        "title": "The features in the 'Maintenance Point v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Maintenance Point v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Maintenance Point v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/queryables",
        "properties": {
          "authorityid": {
            "type": [
              "string"
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
          "highwayauthority_authorityname": {
            "type": [
              "string"
            ]
          },
          "highwayauthority_identifier": {
            "type": [
              "string"
            ]
          },
          "maintenanceauthority_authorityname": {
            "type": [
              "string",
              "null"
            ]
          },
          "maintenanceauthority_identifier": {
            "type": [
              "string",
              "null"
            ]
          },
          "maintenanceresponsibility": {
            "enum": [
              "Maintained At Public Expense",
              "Prospectively Maintained At Public Expense",
              "Not Maintained At Public Expense",
              "Maintained At Public Expense By Another Highways Authority",
              "Street Outside Scope Of EToN"
            ],
            "type": [
              "string"
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
        "sha256": "91185dbe147e9ff96a9a449586a4ae7333971bad06e273cfa02c16d48be30067",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-rami-maintenancepoint-1.0",
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
              "Maintenance",
              "Reinstatement",
              "Special Designation"
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
            "$ref": "https://geojson.org/schema/MultiPoint.json"
          },
          "highwayauthority_authorityname": {
            "type": "string"
          },
          "highwayauthority_identifier": {
            "type": "string"
          },
          "locationdescription": {
            "type": [
              "string",
              "null"
            ]
          },
          "maintenanceauthority_authorityname": {
            "type": [
              "string",
              "null"
            ]
          },
          "maintenanceauthority_identifier": {
            "type": [
              "string",
              "null"
            ]
          },
          "maintenanceresponsibility": {
            "enum": [
              "Maintained At Public Expense",
              "Prospectively Maintained At Public Expense",
              "Not Maintained At Public Expense",
              "Maintained At Public Expense By Another Highways Authority",
              "Street Outside Scope Of EToN"
            ],
            "type": "string"
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
          "effectivestartdate",
          "geometry",
          "highwayauthority_authorityname",
          "highwayauthority_identifier",
          "maintenanceresponsibility",
          "osid",
          "partialreference",
          "theme",
          "usrn",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "5ea33a90c7891f3962c409f2350789ac1207114130f3dd24c875c88a245741fb",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Maintenance Point v1"
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
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/queryables",
      "responseSha256": "91185dbe147e9ff96a9a449586a4ae7333971bad06e273cfa02c16d48be30067",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema",
      "responseSha256": "5ea33a90c7891f3962c409f2350789ac1207114130f3dd24c875c88a245741fb",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/authorityid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/description",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/effectiveenddate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/effectivestartdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/geometry",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry",
      "rdfs:label": "geometry",
      "okfp:schemaDefinition": {
        "@value": {
          "$ref": "https://geojson.org/schema/MultiPoint.json"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/highwayauthority_authorityname",
      "@type": "rdf:Property",
      "dcterms:identifier": "highwayauthority_authorityname",
      "rdfs:label": "highwayauthority_authorityname",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/highwayauthority_identifier",
      "@type": "rdf:Property",
      "dcterms:identifier": "highwayauthority_identifier",
      "rdfs:label": "highwayauthority_identifier",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/locationdescription",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/maintenanceauthority_authorityname",
      "@type": "rdf:Property",
      "dcterms:identifier": "maintenanceauthority_authorityname",
      "rdfs:label": "maintenanceauthority_authorityname",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/maintenanceauthority_identifier",
      "@type": "rdf:Property",
      "dcterms:identifier": "maintenanceauthority_identifier",
      "rdfs:label": "maintenanceauthority_identifier",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/maintenanceresponsibility",
      "@type": "rdf:Property",
      "dcterms:identifier": "maintenanceresponsibility",
      "rdfs:label": "maintenanceresponsibility",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Maintained At Public Expense",
            "Prospectively Maintained At Public Expense",
            "Not Maintained At Public Expense",
            "Maintained At Public Expense By Another Highways Authority",
            "Street Outside Scope Of EToN"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/partialreference",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/usrn",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-maintenancepoint-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1/schema"
      }
    }
  ]
}
---

# Maintenance Point v1

A feature which has a point geometry and provides information about whether the road is maintained at public expense by a national or local highway authority, a road authority or is maintained by another responsible organisation (i.e. not maintained at public expense). If a path is prospectively maintainable at public expense, then this is not currently maintained by a road or highway authority, but the responsible organisation has started the process for a highway or road authority to become responsible for the maintenance of the street at public expense.

Native identifier: `trn-rami-maintenancepoint-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-maintenancepoint-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2022-08-24T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
