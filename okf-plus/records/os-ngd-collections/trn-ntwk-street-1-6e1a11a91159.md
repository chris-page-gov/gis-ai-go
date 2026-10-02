---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Street v1",
  "description": "A Street feature is the definition of the street as defined in the National Street Gazetteer. A Street includes aggregated geometry. Where possible, the geometry of streets captured by a Roads or Highway Authority is spatially matched to the geometry of OS Road Links.",
  "nativeIdentifier": "trn-ntwk-street-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1",
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
      "sourcePointer": "/collections/68",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/68",
      "normalisedRecordSha256": "d0a39111e1321ddf3f8b82fad8aff4aafbafe444e831505e2c76a2f1272ccff2",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1"
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
    "description": "A Street feature is the definition of the street as defined in the National Street Gazetteer. A Street includes aggregated geometry. Where possible, the geometry of streets captured by a Roads or Highway Authority is spatially matched to the geometry of OS Road Links.",
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
    "id": "trn-ntwk-street-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1",
        "rel": "self",
        "title": "The 'Street v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/items",
        "rel": "items",
        "title": "The features in the 'Street v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Street v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Street v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/queryables",
        "properties": {
          "administrativearea1_text": {
            "type": [
              "string"
            ]
          },
          "administrativearea2_text": {
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
            "type": [
              "string"
            ]
          },
          "description": {
            "enum": [
              "Designated Street Name",
              "Numbered Street",
              "Officially Described Street",
              "Unofficial Street Name"
            ],
            "type": [
              "string"
            ]
          },
          "descriptor1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "descriptor2_text": {
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
          "gsscode1": {
            "type": [
              "string",
              "null"
            ]
          },
          "gsscode2": {
            "type": [
              "string",
              "null"
            ]
          },
          "locality1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "locality2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "localname1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "localname2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "localroadcode": {
            "type": [
              "string",
              "null"
            ]
          },
          "nationalroadcode": {
            "type": [
              "string",
              "null"
            ]
          },
          "operationalstate": {
            "enum": [
              "Addressing Only",
              "Open",
              "Permanently Closed",
              "Prospective",
              "Temporarily Closed",
              "Under Construction"
            ],
            "type": [
              "string"
            ]
          },
          "responsibleauthority_identifier": {
            "type": [
              "string"
            ]
          },
          "responsibleauthority_name": {
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
          "townname1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "townname2_text": {
            "type": [
              "string",
              "null"
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
        "sha256": "98fd53f15edb1aa902ccc272be7ea368b5817dbda8d1f901755432c300f49006",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-ntwk-street-1.0",
        "properties": {
          "administrativearea1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "administrativearea1_text": {
            "type": "string"
          },
          "administrativearea2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "administrativearea2_text": {
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
              "Designated Street Name",
              "Numbered Street",
              "Officially Described Street",
              "Unofficial Street Name"
            ],
            "type": "string"
          },
          "descriptor1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "descriptor1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "descriptor2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "descriptor2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "designatedname1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
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
            "type": "string"
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
            "$ref": "https://geojson.org/schema/MultiLineString.json"
          },
          "geometry_length": {
            "type": "number"
          },
          "geometry_source": {
            "enum": [
              "Highways England",
              "Local Highway Authority",
              "Ordnance Survey",
              "Transport Scotland",
              "Welsh Government"
            ],
            "type": "string"
          },
          "gsscode1": {
            "type": [
              "string",
              "null"
            ]
          },
          "gsscode2": {
            "type": [
              "string",
              "null"
            ]
          },
          "gsscoderole1": {
            "enum": [
              "Lower Tier Local Authority",
              "Unitary Local Authority",
              "Upper Tier Local Authority"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "gsscoderole2": {
            "enum": [
              "Lower Tier Local Authority",
              "Unitary Local Authority",
              "Upper Tier Local Authority"
            ],
            "type": [
              "string",
              "null"
            ]
          },
          "locality1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "locality1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "locality2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "locality2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "localname1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "localname1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "localname2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "localname2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "localroadcode": {
            "type": [
              "string",
              "null"
            ]
          },
          "nationalroadcode": {
            "type": [
              "string",
              "null"
            ]
          },
          "operationalstate": {
            "enum": [
              "Addressing Only",
              "Open",
              "Permanently Closed",
              "Prospective",
              "Temporarily Closed",
              "Under Construction"
            ],
            "type": "string"
          },
          "operationalstatedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "pathlinkreference": {
            "items": {
              "properties": {
                "pathlinkid": {
                  "description": "The identifiers of the referenced Path Link feature(s).",
                  "maxLength": 36,
                  "originalName": "pathLinkID",
                  "type": "string"
                },
                "streetversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "streetVersionDate",
                  "pattern": "YYYY-MM-DD",
                  "type": "string"
                },
                "usrn": {
                  "description": "The Unique Street Reference Number (USRN), a unique and persistent identifier of a Street assigned by the Road or Highway Authority.",
                  "maxLength": 8,
                  "originalName": "usrn",
                  "type": "integer"
                }
              },
              "type": "object"
            },
            "type": "array"
          },
          "responsibleauthority_identifier": {
            "type": "string"
          },
          "responsibleauthority_name": {
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
                "roadlinkid": {
                  "description": "The identifier of the road link feature.",
                  "maxLength": 36,
                  "originalName": "roadLinkID",
                  "type": "string"
                },
                "streetversiondate": {
                  "description": "The date this version of the feature entered the OS National Geographic Database.",
                  "format": "date",
                  "originalName": "streetVersionDate",
                  "pattern": "YYYY-MM-DD",
                  "type": "string"
                },
                "usrn": {
                  "description": "The Unique Street Reference Number (USRN), a unique and persistent identifier of a Street assigned by the Road or Highway Authority.",
                  "maxLength": 8,
                  "originalName": "usrn",
                  "type": "integer"
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
          "townname1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "townname1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "townname2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "townname2_text": {
            "type": [
              "string",
              "null"
            ]
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
          "administrativearea1_text",
          "changetype",
          "description",
          "effectivestartdate",
          "geometry",
          "geometry_length",
          "geometry_source",
          "responsibleauthority_identifier",
          "responsibleauthority_name",
          "theme",
          "usrn",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "9ae6c9b7a809c45ec98222e580095d86a93fd01e4beb9a7b75c746813d7477af",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Street v1"
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
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/queryables",
      "responseSha256": "98fd53f15edb1aa902ccc272be7ea368b5817dbda8d1f901755432c300f49006",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema",
      "responseSha256": "9ae6c9b7a809c45ec98222e580095d86a93fd01e4beb9a7b75c746813d7477af",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/administrativearea1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "administrativearea1_language",
      "rdfs:label": "administrativearea1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/administrativearea1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "administrativearea1_text",
      "rdfs:label": "administrativearea1_text",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/administrativearea2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "administrativearea2_language",
      "rdfs:label": "administrativearea2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/administrativearea2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "administrativearea2_text",
      "rdfs:label": "administrativearea2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Designated Street Name",
            "Numbered Street",
            "Officially Described Street",
            "Unofficial Street Name"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/descriptor1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "descriptor1_language",
      "rdfs:label": "descriptor1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/descriptor1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "descriptor1_text",
      "rdfs:label": "descriptor1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/descriptor2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "descriptor2_language",
      "rdfs:label": "descriptor2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/descriptor2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "descriptor2_text",
      "rdfs:label": "descriptor2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/designatedname1_language",
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
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/designatedname1_responsibleauthorityidentifier",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/designatedname1_responsibleauthorityname",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/designatedname1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/designatedname2_language",
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
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/designatedname2_responsibleauthorityidentifier",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/designatedname2_responsibleauthorityname",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/designatedname2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/effectiveenddate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/effectivestartdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/geometry_length",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/geometry_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry_source",
      "rdfs:label": "geometry_source",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Highways England",
            "Local Highway Authority",
            "Ordnance Survey",
            "Transport Scotland",
            "Welsh Government"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/gsscode1",
      "@type": "rdf:Property",
      "dcterms:identifier": "gsscode1",
      "rdfs:label": "gsscode1",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/gsscode2",
      "@type": "rdf:Property",
      "dcterms:identifier": "gsscode2",
      "rdfs:label": "gsscode2",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/gsscoderole1",
      "@type": "rdf:Property",
      "dcterms:identifier": "gsscoderole1",
      "rdfs:label": "gsscoderole1",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Lower Tier Local Authority",
            "Unitary Local Authority",
            "Upper Tier Local Authority"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/gsscoderole2",
      "@type": "rdf:Property",
      "dcterms:identifier": "gsscoderole2",
      "rdfs:label": "gsscoderole2",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Lower Tier Local Authority",
            "Unitary Local Authority",
            "Upper Tier Local Authority"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/locality1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "locality1_language",
      "rdfs:label": "locality1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/locality1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "locality1_text",
      "rdfs:label": "locality1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/locality2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "locality2_language",
      "rdfs:label": "locality2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/locality2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "locality2_text",
      "rdfs:label": "locality2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/localname1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "localname1_language",
      "rdfs:label": "localname1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/localname1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "localname1_text",
      "rdfs:label": "localname1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/localname2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "localname2_language",
      "rdfs:label": "localname2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/localname2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "localname2_text",
      "rdfs:label": "localname2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/localroadcode",
      "@type": "rdf:Property",
      "dcterms:identifier": "localroadcode",
      "rdfs:label": "localroadcode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/nationalroadcode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/operationalstate",
      "@type": "rdf:Property",
      "dcterms:identifier": "operationalstate",
      "rdfs:label": "operationalstate",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Addressing Only",
            "Open",
            "Permanently Closed",
            "Prospective",
            "Temporarily Closed",
            "Under Construction"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/operationalstatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "operationalstatedate",
      "rdfs:label": "operationalstatedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/pathlinkreference",
      "@type": "rdf:Property",
      "dcterms:identifier": "pathlinkreference",
      "rdfs:label": "pathlinkreference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "pathlinkid": {
                "description": "The identifiers of the referenced Path Link feature(s).",
                "maxLength": 36,
                "originalName": "pathLinkID",
                "type": "string"
              },
              "streetversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "streetVersionDate",
                "pattern": "YYYY-MM-DD",
                "type": "string"
              },
              "usrn": {
                "description": "The Unique Street Reference Number (USRN), a unique and persistent identifier of a Street assigned by the Road or Highway Authority.",
                "maxLength": 8,
                "originalName": "usrn",
                "type": "integer"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/responsibleauthority_identifier",
      "@type": "rdf:Property",
      "dcterms:identifier": "responsibleauthority_identifier",
      "rdfs:label": "responsibleauthority_identifier",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/responsibleauthority_name",
      "@type": "rdf:Property",
      "dcterms:identifier": "responsibleauthority_name",
      "rdfs:label": "responsibleauthority_name",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/roadclassification",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/roadlinkreference",
      "@type": "rdf:Property",
      "dcterms:identifier": "roadlinkreference",
      "rdfs:label": "roadlinkreference",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "properties": {
              "roadlinkid": {
                "description": "The identifier of the road link feature.",
                "maxLength": 36,
                "originalName": "roadLinkID",
                "type": "string"
              },
              "streetversiondate": {
                "description": "The date this version of the feature entered the OS National Geographic Database.",
                "format": "date",
                "originalName": "streetVersionDate",
                "pattern": "YYYY-MM-DD",
                "type": "string"
              },
              "usrn": {
                "description": "The Unique Street Reference Number (USRN), a unique and persistent identifier of a Street assigned by the Road or Highway Authority.",
                "maxLength": 8,
                "originalName": "usrn",
                "type": "integer"
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/townname1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "townname1_language",
      "rdfs:label": "townname1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/townname1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "townname1_text",
      "rdfs:label": "townname1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/townname2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "townname2_language",
      "rdfs:label": "townname2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/townname2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "townname2_text",
      "rdfs:label": "townname2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/usrn",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-ntwk-street-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1/schema"
      }
    }
  ]
}
---

# Street v1

A Street feature is the definition of the street as defined in the National Street Gazetteer. A Street includes aggregated geometry. Where possible, the geometry of streets captured by a Roads or Highway Authority is spatially matched to the geometry of OS Road Links.

Native identifier: `trn-ntwk-street-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-ntwk-street-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2022-08-23T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
