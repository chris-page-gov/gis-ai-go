---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Postcode Unit Point v1",
  "description": "The Postcode Unit Point Feature Type is a point representation of a postcode, calculated from the average positions of addresses which share a postcode.",
  "nativeIdentifier": "asu-gbpcd-postcodeunitpoint-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1",
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
      "sourcePointer": "/collections/1",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/1",
      "normalisedRecordSha256": "c2ba2a6171c65e178e3b89d9ed860ae0591708660b64d1467447423814cf4f72",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1"
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
    "description": "The Postcode Unit Point Feature Type is a point representation of a postcode, calculated from the average positions of addresses which share a postcode.",
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
    "id": "asu-gbpcd-postcodeunitpoint-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1",
        "rel": "self",
        "title": "The 'Postcode Unit Point v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/items",
        "rel": "items",
        "title": "The features in the 'Postcode Unit Point v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Postcode Unit Point v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Postcode Unit Point v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/queryables",
        "properties": {
          "inputaddressaccuracy": {
            "enum": [
              "All Input Addresses Have High Positional Accuracy",
              "All Input Addresses Have Low Positional Accuracy",
              "All Input Addresses Have Very Low Positional Accuracy",
              "Input Addresses Positioned At Local Delivery Office",
              "Some Input Addresses Have High Positional Accuracy"
            ],
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
        "sha256": "38fe6a6ebe6927f5c6951dc3960853d0291631a15b0b9fc577544ca35c29d238",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "asu-gbpcd-postcodeunitpoint-1.1",
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
              "Postcode Unit Point"
            ],
            "type": "string"
          },
          "easting": {
            "type": "number"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/Point.json",
            "type": "object"
          },
          "inputaddressaccuracy": {
            "enum": [
              "All Input Addresses Have High Positional Accuracy",
              "All Input Addresses Have Low Positional Accuracy",
              "All Input Addresses Have Very Low Positional Accuracy",
              "Input Addresses Positioned At Local Delivery Office",
              "Some Input Addresses Have High Positional Accuracy"
            ],
            "type": "string"
          },
          "ispobox": {
            "enum": [
              "Yes",
              "No"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "latitude": {
            "type": "number"
          },
          "longitude": {
            "type": "number"
          },
          "northing": {
            "type": "number"
          },
          "postcode": {
            "type": "string"
          },
          "postcodearea": {
            "type": "string"
          },
          "postcodedeliverypointcount_commercial": {
            "type": [
              "integer",
              "null"
            ]
          },
          "postcodedeliverypointcount_matched": {
            "type": [
              "integer",
              "null"
            ]
          },
          "postcodedeliverypointcount_residential": {
            "type": [
              "integer",
              "null"
            ]
          },
          "postcodedeliverypointcount_total": {
            "type": [
              "integer",
              "null"
            ]
          },
          "postcodedeliverypointcount_unmatched": {
            "type": [
              "integer",
              "null"
            ]
          },
          "postcodedistrict": {
            "type": "string"
          },
          "postcodenospace": {
            "type": "string"
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
          "relatedentity": {
            "items": {
              "properties": {
                "crossreferencefeature": {
                  "description": "Description of the related dataset that the cross reference refers to, for example, 'Lower Tier Local Authority'.",
                  "enum": [
                    "Country",
                    "County",
                    "Lower Tier Local Authority",
                    "NHS Health Authority",
                    "NHS Regional Health Authority",
                    "Ward"
                  ],
                  "maxLength": 50,
                  "originalName": "crossReferenceFeature",
                  "type": "string"
                },
                "crossreferenceid": {
                  "description": "Identifier of the related data entity or feature type instance that is the target of the reference or link.",
                  "maxLength": 36,
                  "originalName": "crossReferenceID",
                  "type": "string"
                },
                "featuretypeid": {
                  "description": "Postcode assigned by Royal Mail as a persistent identifier. This is used along with the Feature Type Version Date attribute to join the component to the Postcode Unit Point Feature Type.",
                  "maxLength": 36,
                  "originalName": "featureTypeID",
                  "type": "string"
                },
                "featuretypeversiondate": {
                  "description": "Date of the feature version to which this related component applies. This is used along with the Feature Type ID attribute to join the component to the Postcode Unit Point Feature Type.",
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
          "easting",
          "geometry",
          "inputaddressaccuracy",
          "ispobox",
          "latitude",
          "longitude",
          "northing",
          "postcode",
          "postcodearea",
          "postcodedeliverypointcount_commercial",
          "postcodedeliverypointcount_matched",
          "postcodedeliverypointcount_residential",
          "postcodedeliverypointcount_total",
          "postcodedeliverypointcount_unmatched",
          "postcodedistrict",
          "postcodenospace",
          "postcodesector",
          "postcodetype",
          "relatedentity",
          "theme",
          "versionavailablefromdate",
          "versionavailabletodate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "0ee860103642127b54738c4fdde235658cf35d134938c3556652ed54356d386a",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Postcode Unit Point v1"
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
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/queryables",
      "responseSha256": "38fe6a6ebe6927f5c6951dc3960853d0291631a15b0b9fc577544ca35c29d238",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema",
      "responseSha256": "0ee860103642127b54738c4fdde235658cf35d134938c3556652ed54356d386a",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Postcode Unit Point"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/easting",
      "@type": "rdf:Property",
      "dcterms:identifier": "easting",
      "rdfs:label": "easting",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/inputaddressaccuracy",
      "@type": "rdf:Property",
      "dcterms:identifier": "inputaddressaccuracy",
      "rdfs:label": "inputaddressaccuracy",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "All Input Addresses Have High Positional Accuracy",
            "All Input Addresses Have Low Positional Accuracy",
            "All Input Addresses Have Very Low Positional Accuracy",
            "Input Addresses Positioned At Local Delivery Office",
            "Some Input Addresses Have High Positional Accuracy"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/ispobox",
      "@type": "rdf:Property",
      "dcterms:identifier": "ispobox",
      "rdfs:label": "ispobox",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Yes",
            "No"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/latitude",
      "@type": "rdf:Property",
      "dcterms:identifier": "latitude",
      "rdfs:label": "latitude",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/longitude",
      "@type": "rdf:Property",
      "dcterms:identifier": "longitude",
      "rdfs:label": "longitude",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/northing",
      "@type": "rdf:Property",
      "dcterms:identifier": "northing",
      "rdfs:label": "northing",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/postcode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/postcodearea",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/postcodedeliverypointcount_commercial",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodedeliverypointcount_commercial",
      "rdfs:label": "postcodedeliverypointcount_commercial",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "integer",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/postcodedeliverypointcount_matched",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodedeliverypointcount_matched",
      "rdfs:label": "postcodedeliverypointcount_matched",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "integer",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/postcodedeliverypointcount_residential",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodedeliverypointcount_residential",
      "rdfs:label": "postcodedeliverypointcount_residential",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "integer",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/postcodedeliverypointcount_total",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodedeliverypointcount_total",
      "rdfs:label": "postcodedeliverypointcount_total",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "integer",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/postcodedeliverypointcount_unmatched",
      "@type": "rdf:Property",
      "dcterms:identifier": "postcodedeliverypointcount_unmatched",
      "rdfs:label": "postcodedeliverypointcount_unmatched",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "integer",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/postcodedistrict",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/postcodenospace",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/postcodesector",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/postcodetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/relatedentity",
      "@type": "rdf:Property",
      "dcterms:identifier": "relatedentity",
      "rdfs:label": "relatedentity",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "crossreferencefeature": {
                "description": "Description of the related dataset that the cross reference refers to, for example, 'Lower Tier Local Authority'.",
                "enum": [
                  "Country",
                  "County",
                  "Lower Tier Local Authority",
                  "NHS Health Authority",
                  "NHS Regional Health Authority",
                  "Ward"
                ],
                "maxLength": 50,
                "originalName": "crossReferenceFeature",
                "type": "string"
              },
              "crossreferenceid": {
                "description": "Identifier of the related data entity or feature type instance that is the target of the reference or link.",
                "maxLength": 36,
                "originalName": "crossReferenceID",
                "type": "string"
              },
              "featuretypeid": {
                "description": "Postcode assigned by Royal Mail as a persistent identifier. This is used along with the Feature Type Version Date attribute to join the component to the Postcode Unit Point Feature Type.",
                "maxLength": 36,
                "originalName": "featureTypeID",
                "type": "string"
              },
              "featuretypeversiondate": {
                "description": "Date of the feature version to which this related component applies. This is used along with the Feature Type ID attribute to join the component to the Postcode Unit Point Feature Type.",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/asu-gbpcd-postcodeunitpoint-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1/schema"
      }
    }
  ]
}
---

# Postcode Unit Point v1

The Postcode Unit Point Feature Type is a point representation of a postcode, calculated from the average positions of addresses which share a postcode.

Native identifier: `asu-gbpcd-postcodeunitpoint-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/asu-gbpcd-postcodeunitpoint-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2026-02-10T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
