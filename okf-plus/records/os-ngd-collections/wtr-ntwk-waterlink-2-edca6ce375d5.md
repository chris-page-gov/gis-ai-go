---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Water Link v2",
  "description": "A network representation of the general alignment and connectivity of permanent water, including rivers, lakes, and canals.",
  "nativeIdentifier": "wtr-ntwk-waterlink-2",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "OS NGD",
    "wtr",
    "schema",
    "queryables"
  ],
  "sources": [
    {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections",
      "retrievedAt": "2026-10-02T01:18:50.822323Z",
      "responseSha256": "cf6f9c7670533ff42c64af98a8f7bb8aa60911463d937623a4fc6f5bb8767de9",
      "sourcePointer": "/collections/91",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/91",
      "normalisedRecordSha256": "307cbdb14a3baac385b5463bf3da831b15e8e4b699a1f4d49b37801b17680c96",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2"
  },
  "dcterms:conformsTo": [
    {
      "@id": "http://www.opengis.net/spec/ogcapi-features-1/1.0"
    },
    {
      "@id": "http://www.opengis.net/def/crs/EPSG/0/7405"
    }
  ],
  "temporal": {
    "status": "source-stated",
    "kind": "advertised-collection-temporal-extent",
    "start": "2025-10-11T00:00:00Z",
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
      "http://www.opengis.net/def/crs/EPSG/0/7405",
      "http://www.opengis.net/def/crs/EPSG/0/27700",
      "http://www.opengis.net/def/crs/EPSG/0/3857",
      "http://www.opengis.net/def/crs/EPSG/0/4326",
      "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
    ],
    "description": "A network representation of the general alignment and connectivity of permanent water, including rivers, lakes, and canals.",
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
            "2025-10-11T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "wtr-ntwk-waterlink-2",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2",
        "rel": "self",
        "title": "The 'Water Link v2' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/items",
        "rel": "items",
        "title": "The features in the 'Water Link v2' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema",
        "rel": "describedby",
        "title": "Schema for the 'Water Link v2' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Water Link v2' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/queryables",
        "properties": {
          "catchmentid": {
            "type": [
              "string",
              "null"
            ]
          },
          "catchmentname": {
            "type": [
              "string",
              "null"
            ]
          },
          "description": {
            "enum": [
              "Canal",
              "Canal Feeder",
              "Drain",
              "Foreshore",
              "Leat",
              "Lock",
              "Marsh",
              "Overflow",
              "Reservoir",
              "Sea",
              "Still Water",
              "Watercourse"
            ],
            "type": [
              "string"
            ]
          },
          "geometry_length_m": {
            "type": [
              "number"
            ]
          },
          "gradient": {
            "type": [
              "number",
              "null"
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
          "osid": {
            "type": [
              "string"
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
        "sha256": "8090c890a59f600f58bcc4334603015b8cf04b2a1bf2c4dc44854b20b60b01ee",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "wtr-ntwk-waterlink-2.0",
        "properties": {
          "capturespecification": {
            "enum": [
              "Moorland",
              "Rural",
              "Urban"
            ],
            "type": "string"
          },
          "catchmentid": {
            "type": [
              "string",
              "null"
            ]
          },
          "catchmentname": {
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
              "Canal",
              "Canal Feeder",
              "Drain",
              "Foreshore",
              "Leat",
              "Lock",
              "Marsh",
              "Overflow",
              "Reservoir",
              "Sea",
              "Still Water",
              "Watercourse"
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
          "description_source": {
            "type": [
              "string",
              "null"
            ]
          },
          "description_updatedate": {
            "format": "date",
            "type": "string"
          },
          "endnode": {
            "type": "string"
          },
          "flowdirection": {
            "enum": [
              "In Direction",
              "Unknown"
            ],
            "type": "string"
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
          "geometry_source": {
            "enum": [
              "Local Authority Inferred",
              "Local Authority Surveyed",
              "National Authority Inferred",
              "National Authority Surveyed",
              "Ordnance Survey Area",
              "Ordnance Survey Inferred",
              "Ordnance Survey Line"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "geometry_updatedate": {
            "format": "date",
            "type": "string"
          },
          "gradient": {
            "type": [
              "number",
              "null"
            ]
          },
          "levelofdetail": {
            "enum": [
              "District",
              "Local",
              "National",
              "Regional"
            ],
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
          "nameid": {
            "type": [
              "string",
              "null"
            ]
          },
          "namesecondary1_language": {
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
          "namesecondary1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "namesecondary2_language": {
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
          "namesecondary2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "namesecondaryid": {
            "type": [
              "string",
              "null"
            ]
          },
          "nametertiary1_language": {
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
          "nametertiary1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "nametertiary2_language": {
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
          "nametertiary2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "nametertiaryid": {
            "type": [
              "string",
              "null"
            ]
          },
          "osid": {
            "type": "string"
          },
          "permanence": {
            "enum": [
              "Intermittent",
              "Permanent"
            ],
            "type": "string"
          },
          "physicalcontainment": {
            "enum": [
              "In Culvert",
              "In Natural Subterranean Passage",
              "In Tunnel",
              "Inapplicable"
            ],
            "type": "string"
          },
          "physicallevel": {
            "enum": [
              "Level 1",
              "Level 2",
              "Level 3",
              "Overhead",
              "Surface Level",
              "Underground"
            ],
            "type": "string"
          },
          "primacy": {
            "enum": [
              "1",
              "2"
            ],
            "type": "string"
          },
          "startnode": {
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
          },
          "watertype": {
            "enum": [
              "Inland",
              "Tidal"
            ],
            "type": "string"
          },
          "width_average": {
            "type": [
              "number",
              "null"
            ]
          },
          "width_derivationmethod": {
            "enum": [
              "Calculated From Polygon",
              "Modelled From Network",
              "Default Value For Geographic Region"
            ],
            "type": "string"
          },
          "width_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "width_maximum": {
            "type": [
              "number",
              "null"
            ]
          },
          "width_minimum": {
            "type": [
              "number",
              "null"
            ]
          },
          "width_updatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          }
        },
        "required": [
          "changetype",
          "description",
          "description_updatedate",
          "endnode",
          "flowdirection",
          "geometry",
          "geometry_length",
          "geometry_updatedate",
          "osid",
          "permanence",
          "physicalcontainment",
          "physicallevel",
          "primacy",
          "startnode",
          "theme",
          "versionavailablefromdate",
          "versiondate",
          "watertype"
        ],
        "requiredUndeclared": [
          "geometry_length"
        ],
        "sha256": "3eb1b7ce91fd32aca9c3789a795d3ba9286d2e999a2d48d72ea3fe7bfe55efce",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/7405",
    "title": "Water Link v2"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2025-10-11T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/queryables",
      "responseSha256": "8090c890a59f600f58bcc4334603015b8cf04b2a1bf2c4dc44854b20b60b01ee",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema",
      "responseSha256": "3eb1b7ce91fd32aca9c3789a795d3ba9286d2e999a2d48d72ea3fe7bfe55efce",
      "requiredUndeclared": [
        "geometry_length"
      ]
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/capturespecification",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/catchmentid",
      "@type": "rdf:Property",
      "dcterms:identifier": "catchmentid",
      "rdfs:label": "catchmentid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/catchmentname",
      "@type": "rdf:Property",
      "dcterms:identifier": "catchmentname",
      "rdfs:label": "catchmentname",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Canal",
            "Canal Feeder",
            "Drain",
            "Foreshore",
            "Leat",
            "Lock",
            "Marsh",
            "Overflow",
            "Reservoir",
            "Sea",
            "Still Water",
            "Watercourse"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/description_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/description_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "description_source",
      "rdfs:label": "description_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/description_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/endnode",
      "@type": "rdf:Property",
      "dcterms:identifier": "endnode",
      "rdfs:label": "endnode",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/flowdirection",
      "@type": "rdf:Property",
      "dcterms:identifier": "flowdirection",
      "rdfs:label": "flowdirection",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "In Direction",
            "Unknown"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/geometry_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/geometry_length_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/geometry_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry_source",
      "rdfs:label": "geometry_source",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Local Authority Inferred",
            "Local Authority Surveyed",
            "National Authority Inferred",
            "National Authority Surveyed",
            "Ordnance Survey Area",
            "Ordnance Survey Inferred",
            "Ordnance Survey Line"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/geometry_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/gradient",
      "@type": "rdf:Property",
      "dcterms:identifier": "gradient",
      "rdfs:label": "gradient",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/levelofdetail",
      "@type": "rdf:Property",
      "dcterms:identifier": "levelofdetail",
      "rdfs:label": "levelofdetail",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "District",
            "Local",
            "National",
            "Regional"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/name1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/name1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/name2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/nameid",
      "@type": "rdf:Property",
      "dcterms:identifier": "nameid",
      "rdfs:label": "nameid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/namesecondary1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "namesecondary1_language",
      "rdfs:label": "namesecondary1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/namesecondary1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "namesecondary1_text",
      "rdfs:label": "namesecondary1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/namesecondary2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "namesecondary2_language",
      "rdfs:label": "namesecondary2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/namesecondary2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "namesecondary2_text",
      "rdfs:label": "namesecondary2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/namesecondaryid",
      "@type": "rdf:Property",
      "dcterms:identifier": "namesecondaryid",
      "rdfs:label": "namesecondaryid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/nametertiary1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "nametertiary1_language",
      "rdfs:label": "nametertiary1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/nametertiary1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "nametertiary1_text",
      "rdfs:label": "nametertiary1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/nametertiary2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "nametertiary2_language",
      "rdfs:label": "nametertiary2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/nametertiary2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "nametertiary2_text",
      "rdfs:label": "nametertiary2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/nametertiaryid",
      "@type": "rdf:Property",
      "dcterms:identifier": "nametertiaryid",
      "rdfs:label": "nametertiaryid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/permanence",
      "@type": "rdf:Property",
      "dcterms:identifier": "permanence",
      "rdfs:label": "permanence",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Intermittent",
            "Permanent"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/physicalcontainment",
      "@type": "rdf:Property",
      "dcterms:identifier": "physicalcontainment",
      "rdfs:label": "physicalcontainment",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "In Culvert",
            "In Natural Subterranean Passage",
            "In Tunnel",
            "Inapplicable"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/physicallevel",
      "@type": "rdf:Property",
      "dcterms:identifier": "physicallevel",
      "rdfs:label": "physicallevel",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Level 1",
            "Level 2",
            "Level 3",
            "Overhead",
            "Surface Level",
            "Underground"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/primacy",
      "@type": "rdf:Property",
      "dcterms:identifier": "primacy",
      "rdfs:label": "primacy",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "1",
            "2"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/startnode",
      "@type": "rdf:Property",
      "dcterms:identifier": "startnode",
      "rdfs:label": "startnode",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/toid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/watertype",
      "@type": "rdf:Property",
      "dcterms:identifier": "watertype",
      "rdfs:label": "watertype",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Inland",
            "Tidal"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/width_average",
      "@type": "rdf:Property",
      "dcterms:identifier": "width_average",
      "rdfs:label": "width_average",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "number",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/width_derivationmethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "width_derivationmethod",
      "rdfs:label": "width_derivationmethod",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Calculated From Polygon",
            "Modelled From Network",
            "Default Value For Geographic Region"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/width_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "width_evidencedate",
      "rdfs:label": "width_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/width_maximum",
      "@type": "rdf:Property",
      "dcterms:identifier": "width_maximum",
      "rdfs:label": "width_maximum",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "number",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/width_minimum",
      "@type": "rdf:Property",
      "dcterms:identifier": "width_minimum",
      "rdfs:label": "width_minimum",
      "okfp:schemaDefinition": {
        "@value": {
          "type": [
            "number",
            "null"
          ]
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/wtr-ntwk-waterlink-2/field/width_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "width_updatedate",
      "rdfs:label": "width_updatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2/schema"
      }
    }
  ]
}
---

# Water Link v2

A network representation of the general alignment and connectivity of permanent water, including rivers, lakes, and canals.

Native identifier: `wtr-ntwk-waterlink-2`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/wtr-ntwk-waterlink-2)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2025-10-11T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
