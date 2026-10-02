---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Crowd Sourced Name Point v1",
  "description": "A crowd sourced name collated from data submitted to the Vernacular Names Tool in the OS Data Hub, provided as a point feature.",
  "nativeIdentifier": "gnm-fts-crowdsourcednamepoint-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "OS NGD",
    "gnm",
    "schema",
    "queryables"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections",
      "retrievedAt": "2026-10-02T01:18:50.822323Z",
      "responseSha256": "cf6f9c7670533ff42c64af98a8f7bb8aa60911463d937623a4fc6f5bb8767de9",
      "sourcePointer": "/collections/10",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/10",
      "normalisedRecordSha256": "a14a24bb455c37b4b0878f77e3e857914a4ce21c3958015edfbfd714ee17193a",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1"
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
    "start": "2025-03-21T00:00:00Z",
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
    "description": "A crowd sourced name collated from data submitted to the Vernacular Names Tool in the OS Data Hub, provided as a point feature.",
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
            "2025-03-21T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "gnm-fts-crowdsourcednamepoint-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1",
        "rel": "self",
        "title": "The 'Crowd Sourced Name Point v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/items",
        "rel": "items",
        "title": "The features in the 'Crowd Sourced Name Point v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Crowd Sourced Name Point v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Crowd Sourced Name Point v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/queryables",
        "properties": {
          "description": {
            "enum": [
              "Crowd Sourced Name"
            ],
            "type": [
              "string"
            ]
          },
          "name_text": {
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
        "sha256": "e174f780427fb2ac50208c71e085eefaae1fd92bdf8ecff00803186a3cb2f3d2",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "gnm-fts-crowdsourcednamepoint-1.0",
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
              "Crowd Sourced Name"
            ],
            "type": "string"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/Point.json",
            "type": "object"
          },
          "hassimilarosname": {
            "type": "boolean"
          },
          "matchedosid": {
            "format": "uuid",
            "type": [
              "string",
              "null"
            ]
          },
          "matchedosid_featuretype": {
            "enum": [
              "Building Part",
              "Compound Structure",
              "Inter Tidal Line",
              "Land",
              "Landform",
              "Landform Point",
              "Land Point",
              "Named Area",
              "Named Road Junction",
              "Road",
              "Road Node",
              "Road Track Or Path",
              "Site",
              "Street",
              "Structure",
              "Structure Line",
              "Structure Point",
              "Water",
              "Water Link Set",
              "Water Point"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "matchedosid_theme": {
            "enum": [
              "Buildings",
              "Geographical Names",
              "Land",
              "Land Use",
              "Structures",
              "Transport",
              "Water"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "matcheduprn": {
            "type": [
              "long",
              "null"
            ]
          },
          "matchedusrn": {
            "type": [
              "integer",
              "null"
            ]
          },
          "matchtype": {
            "enum": [
              "Alternative Name For Existing Feature",
              "Under Review",
              "Unmatched - Feature Not In Current Specifications Or Scope",
              "Unmatched - Name And Classification Supplied Are Ambiguous",
              "Unmatched - Name Persists For Feature That No Longer Exists"
            ],
            "type": "string"
          },
          "name_evidencedate": {
            "format": "date-time",
            "type": "string"
          },
          "name_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "name_source": {
            "type": "string"
          },
          "name_text": {
            "type": "string"
          },
          "osid": {
            "format": "uuid",
            "type": "string"
          },
          "sourceclassification": {
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
          "hassimilarosname",
          "matchedosid",
          "matchedosid_featuretype",
          "matchedosid_theme",
          "matcheduprn",
          "matchedusrn",
          "matchtype",
          "name_evidencedate",
          "name_language",
          "name_source",
          "name_text",
          "osid",
          "sourceclassification",
          "theme",
          "versionavailablefromdate",
          "versionavailabletodate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "78380e38bb91d8cf1ebc60e3612cc11c8183782dad8e959cfa87532ab2aaa94a",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Crowd Sourced Name Point v1"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2025-03-21T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/queryables",
      "responseSha256": "e174f780427fb2ac50208c71e085eefaae1fd92bdf8ecff00803186a3cb2f3d2",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema",
      "responseSha256": "78380e38bb91d8cf1ebc60e3612cc11c8183782dad8e959cfa87532ab2aaa94a",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Crowd Sourced Name"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/hassimilarosname",
      "@type": "rdf:Property",
      "dcterms:identifier": "hassimilarosname",
      "rdfs:label": "hassimilarosname",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "boolean"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/matchedosid",
      "@type": "rdf:Property",
      "dcterms:identifier": "matchedosid",
      "rdfs:label": "matchedosid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/matchedosid_featuretype",
      "@type": "rdf:Property",
      "dcterms:identifier": "matchedosid_featuretype",
      "rdfs:label": "matchedosid_featuretype",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Building Part",
            "Compound Structure",
            "Inter Tidal Line",
            "Land",
            "Landform",
            "Landform Point",
            "Land Point",
            "Named Area",
            "Named Road Junction",
            "Road",
            "Road Node",
            "Road Track Or Path",
            "Site",
            "Street",
            "Structure",
            "Structure Line",
            "Structure Point",
            "Water",
            "Water Link Set",
            "Water Point"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/matchedosid_theme",
      "@type": "rdf:Property",
      "dcterms:identifier": "matchedosid_theme",
      "rdfs:label": "matchedosid_theme",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Buildings",
            "Geographical Names",
            "Land",
            "Land Use",
            "Structures",
            "Transport",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/matcheduprn",
      "@type": "rdf:Property",
      "dcterms:identifier": "matcheduprn",
      "rdfs:label": "matcheduprn",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "long",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/matchedusrn",
      "@type": "rdf:Property",
      "dcterms:identifier": "matchedusrn",
      "rdfs:label": "matchedusrn",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/matchtype",
      "@type": "rdf:Property",
      "dcterms:identifier": "matchtype",
      "rdfs:label": "matchtype",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Alternative Name For Existing Feature",
            "Under Review",
            "Unmatched - Feature Not In Current Specifications Or Scope",
            "Unmatched - Name And Classification Supplied Are Ambiguous",
            "Unmatched - Name Persists For Feature That No Longer Exists"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/name_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "name_evidencedate",
      "rdfs:label": "name_evidencedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date-time",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/name_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "name_language",
      "rdfs:label": "name_language",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "eng",
            "gla",
            "cym"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/name_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "name_source",
      "rdfs:label": "name_source",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/name_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "name_text",
      "rdfs:label": "name_text",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/sourceclassification",
      "@type": "rdf:Property",
      "dcterms:identifier": "sourceclassification",
      "rdfs:label": "sourceclassification",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-crowdsourcednamepoint-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1/schema"
      }
    }
  ]
}
---

# Crowd Sourced Name Point v1

A crowd sourced name collated from data submitted to the Vernacular Names Tool in the OS Data Hub, provided as a point feature.

Native identifier: `gnm-fts-crowdsourcednamepoint-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-crowdsourcednamepoint-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2025-03-21T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
