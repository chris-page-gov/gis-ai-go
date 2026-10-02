---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Field Boundary v1",
  "description": "A line feature representing field boundary features adjacent to, or contained within, areas of agricultural land, trees, rough grassland or heath. Also includes features adjacent to, or contained within, land in the RPA’s Rural Land Register where they are in urban areas in England. Field Boundary features replicate all, or part of, an underlying OS NGD Structure (Built Obstruction) Line and are classified as Tree Canopy, Wooded Strip, Hedge, Wall, Other or Unknown (in hierarchy order).",
  "nativeIdentifier": "str-fts-fieldboundary-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1",
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
      "sourcePointer": "/collections/29",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/29",
      "normalisedRecordSha256": "7b3f3ccb2ee9c9fb1fa7cf46cc84bf5c93d2b044f1b356b6c4628b657056de18",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1"
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
    "start": "2024-03-16T00:00:00Z",
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
    "description": "A line feature representing field boundary features adjacent to, or contained within, areas of agricultural land, trees, rough grassland or heath. Also includes features adjacent to, or contained within, land in the RPA’s Rural Land Register where they are in urban areas in England. Field Boundary features replicate all, or part of, an underlying OS NGD Structure (Built Obstruction) Line and are classified as Tree Canopy, Wooded Strip, Hedge, Wall, Other or Unknown (in hierarchy order).",
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
            "2024-03-16T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "str-fts-fieldboundary-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1",
        "rel": "self",
        "title": "The 'Field Boundary v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/items",
        "rel": "items",
        "title": "The features in the 'Field Boundary v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Field Boundary v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Field Boundary v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/queryables",
        "properties": {
          "averageheight_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagewidth_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "description": {
            "enum": [
              "Hedge",
              "Tree Canopy",
              "Wall",
              "Wooded Strip",
              "Other",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "geometry_length_m": {
            "type": [
              "number"
            ]
          },
          "maximumheight_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "maximumwidth_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "minimumheight_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "minimumwidth_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "osid": {
            "format": "uuid",
            "type": [
              "string"
            ]
          },
          "structureline_osid": {
            "format": "uuid",
            "type": [
              "string"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "5b876e1cc028631db24556aa7eb09026ab84e62a4b7a71288bba8ae98b3dadaa",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "str-fts-fieldboundary-1.0",
        "properties": {
          "averageheight_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagewidth_m": {
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
          "description": {
            "enum": [
              "Hedge",
              "Tree Canopy",
              "Wall",
              "Wooded Strip",
              "Other",
              "Unknown"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/LineString.json"
          },
          "geometry_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "geometry_length_m": {
            "type": "number"
          },
          "geometry_updatedate": {
            "format": "date",
            "type": "string"
          },
          "imagery_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "iswoodlandboundary": {
            "type": "boolean"
          },
          "iswoodlandboundary_evidencedate": {
            "format": "date",
            "type": "string"
          },
          "iswoodlandboundary_updatedate": {
            "format": "date",
            "type": "string"
          },
          "maximumheight_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "maximumwidth_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "minimumheight_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "minimumwidth_m": {
            "type": [
              "number",
              "null"
            ]
          },
          "osid": {
            "format": "uuid",
            "type": "string"
          },
          "structureline_osid": {
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
          "changetype",
          "description",
          "geometry",
          "geometry_length_m",
          "geometry_updatedate",
          "osid",
          "theme",
          "versionavailablefromdate",
          "versiondate",
          "iswoodlandboundary",
          "iswoodlandboundary_evidencedate",
          "isWoodlandboundary_updatedate",
          "builtobstruction_osid"
        ],
        "requiredUndeclared": [
          "builtobstruction_osid",
          "isWoodlandboundary_updatedate"
        ],
        "sha256": "161b768a8a5b363319d9a20c2b40745574c1ada17003c4fba4f213a1701a897b",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Field Boundary v1"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2024-03-16T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/queryables",
      "responseSha256": "5b876e1cc028631db24556aa7eb09026ab84e62a4b7a71288bba8ae98b3dadaa",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema",
      "responseSha256": "161b768a8a5b363319d9a20c2b40745574c1ada17003c4fba4f213a1701a897b",
      "requiredUndeclared": [
        "builtobstruction_osid",
        "isWoodlandboundary_updatedate"
      ]
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/averageheight_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "averageheight_m",
      "rdfs:label": "averageheight_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/averagewidth_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagewidth_m",
      "rdfs:label": "averagewidth_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Hedge",
            "Tree Canopy",
            "Wall",
            "Wooded Strip",
            "Other",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/geometry_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/geometry_length_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/geometry_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/imagery_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "imagery_evidencedate",
      "rdfs:label": "imagery_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/iswoodlandboundary",
      "@type": "rdf:Property",
      "dcterms:identifier": "iswoodlandboundary",
      "rdfs:label": "iswoodlandboundary",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "boolean"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/iswoodlandboundary_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "iswoodlandboundary_evidencedate",
      "rdfs:label": "iswoodlandboundary_evidencedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/iswoodlandboundary_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "iswoodlandboundary_updatedate",
      "rdfs:label": "iswoodlandboundary_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/maximumheight_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "maximumheight_m",
      "rdfs:label": "maximumheight_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/maximumwidth_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "maximumwidth_m",
      "rdfs:label": "maximumwidth_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/minimumheight_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "minimumheight_m",
      "rdfs:label": "minimumheight_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/minimumwidth_m",
      "@type": "rdf:Property",
      "dcterms:identifier": "minimumwidth_m",
      "rdfs:label": "minimumwidth_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/structureline_osid",
      "@type": "rdf:Property",
      "dcterms:identifier": "structureline_osid",
      "rdfs:label": "structureline_osid",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "uuid",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/str-fts-fieldboundary-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1/schema"
      }
    }
  ]
}
---

# Field Boundary v1

A line feature representing field boundary features adjacent to, or contained within, areas of agricultural land, trees, rough grassland or heath. Also includes features adjacent to, or contained within, land in the RPA’s Rural Land Register where they are in urban areas in England. Field Boundary features replicate all, or part of, an underlying OS NGD Structure (Built Obstruction) Line and are classified as Tree Canopy, Wooded Strip, Hedge, Wall, Other or Unknown (in hierarchy order).

Native identifier: `str-fts-fieldboundary-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/str-fts-fieldboundary-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2024-03-16T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
