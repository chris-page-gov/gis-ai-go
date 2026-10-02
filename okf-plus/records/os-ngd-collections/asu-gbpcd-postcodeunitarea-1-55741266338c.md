---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Postcode Unit Area v1",
  "description": "The Postcode Unit Area Feature Type is an area representation of the notional extents of areas containing addresses which share a common postcode unit. Notional extents are designed to enable users to display and analyse any data collected at the postcode unit level. These have been refined to avoid property extents and to follow the path of linear features such as roads, rivers and railways where possible. Polygons within this feature type are derived from georeferenced Royal Mail Postal Address File (PAF) delivery addresses.",
  "nativeIdentifier": "asu-gbpcd-postcodeunitarea-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "OS NGD",
    "asu",
    "schema",
    "queryables"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections",
      "retrievedAt": "2026-10-02T01:18:50.822323Z",
      "responseSha256": "cf6f9c7670533ff42c64af98a8f7bb8aa60911463d937623a4fc6f5bb8767de9",
      "sourcePointer": "/collections/0",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/0",
      "normalisedRecordSha256": "54912dc526bba64f362eb4cce789f5738ee693bd44b0b5206533dd7c09279d62",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1"
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
    "start": "2026-02-10T00:00:00Z",
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
    "description": "The Postcode Unit Area Feature Type is an area representation of the notional extents of areas containing addresses which share a common postcode unit. Notional extents are designed to enable users to display and analyse any data collected at the postcode unit level. These have been refined to avoid property extents and to follow the path of linear features such as roads, rivers and railways where possible. Polygons within this feature type are derived from georeferenced Royal Mail Postal Address File (PAF) delivery addresses.",
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
            "2026-02-10T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "asu-gbpcd-postcodeunitarea-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1",
        "rel": "self",
        "title": "The 'Postcode Unit Area v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/items",
        "rel": "items",
        "title": "The features in the 'Postcode Unit Area v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Postcode Unit Area v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Postcode Unit Area v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/queryables",
        "properties": {
          "featureid": {
            "format": "uuid",
            "type": [
              "string"
            ]
          },
          "postcode": {
            "type": [
              "string"
            ]
          },
          "postcodearea": {
            "type": [
              "string"
            ]
          },
          "postcodedistrict": {
            "type": [
              "string"
            ]
          },
          "postcodesector": {
            "type": [
              "string"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "ee7106654f3b26b19c34ddd64c8a077c8bef66080c323ecb674bb293d22fdf3c",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "asu-gbpcd-postcodeunitarea-1.0",
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
              "Postcode Unit Area"
            ],
            "type": "string"
          },
          "featureid": {
            "format": "uuid",
            "type": "string"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/Polygon.json",
            "type": "object"
          },
          "geometryid": {
            "format": "uuid",
            "type": "string"
          },
          "postcode": {
            "type": "string"
          },
          "postcodearea": {
            "type": "string"
          },
          "postcodedeliverypointcount_matched": {
            "type": "integer"
          },
          "postcodedeliverypointcount_total": {
            "type": "integer"
          },
          "postcodedeliverypointcount_unmatched": {
            "type": "integer"
          },
          "postcodedistrict": {
            "type": "string"
          },
          "postcodenospace": {
            "type": "string"
          },
          "postcodepartcount_coincidentalgeometry": {
            "type": "integer"
          },
          "postcodepartcount_total": {
            "type": "integer"
          },
          "postcodepartdeliverypointcount_commercial": {
            "type": "integer"
          },
          "postcodepartdeliverypointcount_residential": {
            "type": "integer"
          },
          "postcodepartdeliverypointcount_total": {
            "type": "integer"
          },
          "postcodesector": {
            "type": "string"
          },
          "postcodetype": {
            "enum": [
              "Large User",
              "Small User"
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
          "changetype",
          "description",
          "featureid",
          "geometry",
          "geometryid",
          "postcode",
          "postcodearea",
          "postcodedeliverypointcount_matched",
          "postcodedeliverypointcount_total",
          "postcodedeliverypointcount_unmatched",
          "postcodedistrict",
          "postcodenospace",
          "postcodepartcount_coincidentalgeometry",
          "postcodepartcount_total",
          "postcodepartdeliverypointcount_commercial",
          "postcodepartdeliverypointcount_residential",
          "postcodepartdeliverypointcount_total",
          "postcodesector",
          "postcodetype",
          "theme",
          "versionavailablefromdate",
          "versionavailabletodate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "816f5ffb61543323f7110d11ecc77e8b02d6eeefce0c4e6cfcc0fdffd36cb670",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Postcode Unit Area v1"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2026-02-10T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/queryables",
      "responseSha256": "ee7106654f3b26b19c34ddd64c8a077c8bef66080c323ecb674bb293d22fdf3c",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema",
      "responseSha256": "816f5ffb61543323f7110d11ecc77e8b02d6eeefce0c4e6cfcc0fdffd36cb670",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Postcode Unit Area"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/featureid",
      "@type": "rdf:Property",
      "dcterms:identifier": "featureid",
      "rdfs:label": "featureid",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "uuid",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/geometryid",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometryid",
      "rdfs:label": "geometryid",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "uuid",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcode",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcode",
      "rdfs:label": "postcode",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcodearea",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodearea",
      "rdfs:label": "postcodearea",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcodedeliverypointcount_matched",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodedeliverypointcount_matched",
      "rdfs:label": "postcodedeliverypointcount_matched",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcodedeliverypointcount_total",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodedeliverypointcount_total",
      "rdfs:label": "postcodedeliverypointcount_total",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcodedeliverypointcount_unmatched",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodedeliverypointcount_unmatched",
      "rdfs:label": "postcodedeliverypointcount_unmatched",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcodedistrict",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodedistrict",
      "rdfs:label": "postcodedistrict",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcodenospace",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodenospace",
      "rdfs:label": "postcodenospace",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcodepartcount_coincidentalgeometry",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodepartcount_coincidentalgeometry",
      "rdfs:label": "postcodepartcount_coincidentalgeometry",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcodepartcount_total",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodepartcount_total",
      "rdfs:label": "postcodepartcount_total",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcodepartdeliverypointcount_commercial",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodepartdeliverypointcount_commercial",
      "rdfs:label": "postcodepartdeliverypointcount_commercial",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcodepartdeliverypointcount_residential",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodepartdeliverypointcount_residential",
      "rdfs:label": "postcodepartdeliverypointcount_residential",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcodepartdeliverypointcount_total",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodepartdeliverypointcount_total",
      "rdfs:label": "postcodepartdeliverypointcount_total",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcodesector",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodesector",
      "rdfs:label": "postcodesector",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/postcodetype",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodetype",
      "rdfs:label": "postcodetype",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Large User",
            "Small User"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitarea-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1/schema"
      }
    }
  ]
}
---

# Postcode Unit Area v1

The Postcode Unit Area Feature Type is an area representation of the notional extents of areas containing addresses which share a common postcode unit. Notional extents are designed to enable users to display and analyse any data collected at the postcode unit level. These have been refined to avoid property extents and to follow the path of linear features such as roads, rivers and railways where possible. Polygons within this feature type are derived from georeferenced Royal Mail Postal Address File (PAF) delivery addresses.

Native identifier: `asu-gbpcd-postcodeunitarea-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitarea-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2026-02-10T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
