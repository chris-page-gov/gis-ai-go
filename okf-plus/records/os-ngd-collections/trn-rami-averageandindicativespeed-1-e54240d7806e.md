---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Average And Indicative Speed v1",
  "description": "This feature type provides two sets of speed information for all roads in Great Britain. These are: 1. A historic average speed in kilometres per hours (kph). In this context, 'historic' means that the average speed data was collected over a six-month period for the selected road link. Average speeds are provided in different time periods for each road link. A single day (i.e. a 24-hour period) is split into 8 time periods Monday to Friday (MF) and 6 time periods Saturday to Sunday (SS), for example, Monday–Friday (MF) 07:00–09:00, Saturday–Sunday (SS) 14:00–19:00. There’s a separate attribute for each time period. 2. An indicative speed limit. This is an indication of the maximum speed limit for vehicles; the indicative speed limits reference road network data. Indicative speed limit values that apply over the majority of a section of road are provided in both miles per hour (mph) and kilometres per hour (kph).",
  "nativeIdentifier": "trn-rami-averageandindicativespeed-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1",
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
      "sourcePointer": "/collections/70",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/70",
      "normalisedRecordSha256": "0e8be0a4a9d55512c23c82addf881b4edf0fa06f610e8dc65221866bdaf19720",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1"
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
    "start": "2023-02-03T00:00:00Z",
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
    "description": "This feature type provides two sets of speed information for all roads in Great Britain. These are:\n1.\tA historic average speed in kilometres per hours (kph). In this context, 'historic' means that the average speed data was collected over a six-month period for the selected road link. Average speeds are provided in different time periods for each road link. A single day (i.e. a 24-hour period) is split into 8 time periods Monday to Friday (MF) and 6 time periods Saturday to Sunday (SS), for example, Monday–Friday (MF) 07:00–09:00, Saturday–Sunday (SS) 14:00–19:00. There’s a separate attribute for each time period.\n2.\tAn indicative speed limit. This is an indication of the maximum speed limit for vehicles; the indicative speed limits reference road network data. Indicative speed limit values that apply over the majority of a section of road are provided in both miles per hour (mph) and kilometres per hour (kph).",
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
            "2023-02-03T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "trn-rami-averageandindicativespeed-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1",
        "rel": "self",
        "title": "The 'Average And Indicative Speed v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/items",
        "rel": "items",
        "title": "The features in the 'Average And Indicative Speed v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Average And Indicative Speed v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Average And Indicative Speed v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/queryables",
        "properties": {
          "averagespeed_mf12to14againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf12to14indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf14to16againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf14to16indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf16to19againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf16to19indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf19to22againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf19to22indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf22to4againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf22to4indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf4to7againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf4to7indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf7to9againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf7to9indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf9to12againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf9to12indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss10to14againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss10to14indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss14to19againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss14to19indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss19to22againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss19to22indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss22to4againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss22to4indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss4to7againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss4to7indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss7to10againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss7to10indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "geometry_length_m": {
            "type": [
              "number"
            ]
          },
          "indicativespeedlimit_kph": {
            "type": [
              "integer"
            ]
          },
          "indicativespeedlimit_mph": {
            "type": [
              "integer"
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
        "sha256": "f9ceebd782c36886c90dcad661b6a4b381c4dc7791bf79c4014ed6c27603316d",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "trn-rami-averageandindicativespeed-1.0",
        "properties": {
          "alternatename1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "alternatename1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "alternatename2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "alternatename2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "averagespeed_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "averagespeed_mf12to14againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf12to14capturemethod": {
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
          "averagespeed_mf12to14indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf14to16againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf14to16capturemethod": {
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
          "averagespeed_mf14to16indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf16to19againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf16to19capturemethod": {
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
          "averagespeed_mf16to19indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf19to22againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf19to22capturemethod": {
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
          "averagespeed_mf19to22indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf22to4againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf22to4capturemethod": {
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
          "averagespeed_mf22to4indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf4to7againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf4to7capturemethod": {
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
          "averagespeed_mf4to7indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf7to9againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf7to9capturemethod": {
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
          "averagespeed_mf7to9indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf9to12againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_mf9to12capturemethod": {
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
          "averagespeed_mf9to12indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_source": {
            "type": [
              "string",
              "null"
            ]
          },
          "averagespeed_ss10to14againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss10to14capturemethod": {
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
          "averagespeed_ss10to14indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss14to19againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss14to19capturemethod": {
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
          "averagespeed_ss14to19indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss19to22againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss19to22capturemethod": {
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
          "averagespeed_ss19to22indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss22to4againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss22to4capturemethod": {
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
          "averagespeed_ss22to4indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss4to7againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss4to7capturemethod": {
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
          "averagespeed_ss4to7indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss7to10againstdirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_ss7to10capturemethod": {
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
          "averagespeed_ss7to10indirection_kph": {
            "type": [
              "number",
              "null"
            ]
          },
          "averagespeed_updatedate": {
            "format": "date",
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
              "Average And Indicative Speed"
            ],
            "type": "string"
          },
          "formspartofstreet": {
            "items": {
              "type": "integer"
            },
            "type": "array"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/LineString.json"
          },
          "geometry_length_m": {
            "type": "number"
          },
          "indicativespeedlimit_capturemethod": {
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
          "indicativespeedlimit_evidencedate": {
            "format": "date",
            "type": [
              "string",
              "null"
            ]
          },
          "indicativespeedlimit_kph": {
            "type": "integer"
          },
          "indicativespeedlimit_mph": {
            "type": "integer"
          },
          "indicativespeedlimit_source": {
            "type": [
              "string",
              "null"
            ]
          },
          "indicativespeedlimit_updatedate": {
            "format": "date",
            "type": "string"
          },
          "name1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
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
            "type": "string"
          },
          "name2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "osid": {
            "format": "uuid",
            "type": "string"
          },
          "roadclassificationnumber": {
            "type": [
              "string",
              "null"
            ]
          },
          "routehierarchy": {
            "enum": [
              "A Road",
              "A Road Primary",
              "B Road",
              "B Road Primary",
              "Local Access Road",
              "Local Road",
              "Minor Road",
              "Motorway",
              "Restricted Local Access Road",
              "Restricted Secondary Access Road",
              "Secondary Access Road",
              "Shared Use Road"
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
          "averagespeed_mf12to14capturemethod",
          "averagespeed_mf14to16capturemethod",
          "averagespeed_mf16to19capturemethod",
          "averagespeed_mf19to22capturemethod",
          "averagespeed_mf22to4capturemethod",
          "averagespeed_mf4to7capturemethod",
          "averagespeed_mf7to9capturemethod",
          "averagespeed_mf9to12capturemethod",
          "averagespeed_ss10to14capturemethod",
          "averagespeed_ss14to19capturemethod",
          "averagespeed_ss19to22capturemethod",
          "averagespeed_ss22to4capturemethod",
          "averagespeed_ss4to7capturemethod",
          "averagespeed_ss7to10capturemethod",
          "averagespeed_updatedate",
          "changetype",
          "description",
          "geometry",
          "geometry_length_m",
          "indicativespeedlimit_capturemethod",
          "indicativespeedlimit_kph",
          "indicativespeedlimit_mph",
          "indicativespeedlimit_updatedate",
          "osid",
          "routehierarchy",
          "theme",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "561f236e1866e43aa5a9dfebe98dd26c4a8d916ef28821107d82a0b9c2da2b32",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/7405",
    "title": "Average And Indicative Speed v1"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2023-02-03T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/queryables",
      "responseSha256": "f9ceebd782c36886c90dcad661b6a4b381c4dc7791bf79c4014ed6c27603316d",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema",
      "responseSha256": "561f236e1866e43aa5a9dfebe98dd26c4a8d916ef28821107d82a0b9c2da2b32",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/alternatename1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "alternatename1_language",
      "rdfs:label": "alternatename1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/alternatename1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "alternatename1_text",
      "rdfs:label": "alternatename1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/alternatename2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "alternatename2_language",
      "rdfs:label": "alternatename2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/alternatename2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "alternatename2_text",
      "rdfs:label": "alternatename2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_evidencedate",
      "rdfs:label": "averagespeed_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf12to14againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf12to14againstdirection_kph",
      "rdfs:label": "averagespeed_mf12to14againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf12to14capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf12to14capturemethod",
      "rdfs:label": "averagespeed_mf12to14capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf12to14indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf12to14indirection_kph",
      "rdfs:label": "averagespeed_mf12to14indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf14to16againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf14to16againstdirection_kph",
      "rdfs:label": "averagespeed_mf14to16againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf14to16capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf14to16capturemethod",
      "rdfs:label": "averagespeed_mf14to16capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf14to16indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf14to16indirection_kph",
      "rdfs:label": "averagespeed_mf14to16indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf16to19againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf16to19againstdirection_kph",
      "rdfs:label": "averagespeed_mf16to19againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf16to19capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf16to19capturemethod",
      "rdfs:label": "averagespeed_mf16to19capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf16to19indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf16to19indirection_kph",
      "rdfs:label": "averagespeed_mf16to19indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf19to22againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf19to22againstdirection_kph",
      "rdfs:label": "averagespeed_mf19to22againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf19to22capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf19to22capturemethod",
      "rdfs:label": "averagespeed_mf19to22capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf19to22indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf19to22indirection_kph",
      "rdfs:label": "averagespeed_mf19to22indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf22to4againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf22to4againstdirection_kph",
      "rdfs:label": "averagespeed_mf22to4againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf22to4capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf22to4capturemethod",
      "rdfs:label": "averagespeed_mf22to4capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf22to4indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf22to4indirection_kph",
      "rdfs:label": "averagespeed_mf22to4indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf4to7againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf4to7againstdirection_kph",
      "rdfs:label": "averagespeed_mf4to7againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf4to7capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf4to7capturemethod",
      "rdfs:label": "averagespeed_mf4to7capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf4to7indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf4to7indirection_kph",
      "rdfs:label": "averagespeed_mf4to7indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf7to9againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf7to9againstdirection_kph",
      "rdfs:label": "averagespeed_mf7to9againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf7to9capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf7to9capturemethod",
      "rdfs:label": "averagespeed_mf7to9capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf7to9indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf7to9indirection_kph",
      "rdfs:label": "averagespeed_mf7to9indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf9to12againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf9to12againstdirection_kph",
      "rdfs:label": "averagespeed_mf9to12againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf9to12capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf9to12capturemethod",
      "rdfs:label": "averagespeed_mf9to12capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_mf9to12indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_mf9to12indirection_kph",
      "rdfs:label": "averagespeed_mf9to12indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_source",
      "rdfs:label": "averagespeed_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss10to14againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss10to14againstdirection_kph",
      "rdfs:label": "averagespeed_ss10to14againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss10to14capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss10to14capturemethod",
      "rdfs:label": "averagespeed_ss10to14capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss10to14indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss10to14indirection_kph",
      "rdfs:label": "averagespeed_ss10to14indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss14to19againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss14to19againstdirection_kph",
      "rdfs:label": "averagespeed_ss14to19againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss14to19capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss14to19capturemethod",
      "rdfs:label": "averagespeed_ss14to19capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss14to19indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss14to19indirection_kph",
      "rdfs:label": "averagespeed_ss14to19indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss19to22againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss19to22againstdirection_kph",
      "rdfs:label": "averagespeed_ss19to22againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss19to22capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss19to22capturemethod",
      "rdfs:label": "averagespeed_ss19to22capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss19to22indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss19to22indirection_kph",
      "rdfs:label": "averagespeed_ss19to22indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss22to4againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss22to4againstdirection_kph",
      "rdfs:label": "averagespeed_ss22to4againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss22to4capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss22to4capturemethod",
      "rdfs:label": "averagespeed_ss22to4capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss22to4indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss22to4indirection_kph",
      "rdfs:label": "averagespeed_ss22to4indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss4to7againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss4to7againstdirection_kph",
      "rdfs:label": "averagespeed_ss4to7againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss4to7capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss4to7capturemethod",
      "rdfs:label": "averagespeed_ss4to7capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss4to7indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss4to7indirection_kph",
      "rdfs:label": "averagespeed_ss4to7indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss7to10againstdirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss7to10againstdirection_kph",
      "rdfs:label": "averagespeed_ss7to10againstdirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss7to10capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss7to10capturemethod",
      "rdfs:label": "averagespeed_ss7to10capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_ss7to10indirection_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_ss7to10indirection_kph",
      "rdfs:label": "averagespeed_ss7to10indirection_kph",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/averagespeed_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "averagespeed_updatedate",
      "rdfs:label": "averagespeed_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Average And Indicative Speed"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/formspartofstreet",
      "@type": "rdf:Property",
      "dcterms:identifier": "formspartofstreet",
      "rdfs:label": "formspartofstreet",
      "okfp:schemaDefinition": {
        "@value": {
          "items": {
            "type": "integer"
          },
          "type": "array"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/geometry",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/geometry_length_m",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/indicativespeedlimit_capturemethod",
      "@type": "rdf:Property",
      "dcterms:identifier": "indicativespeedlimit_capturemethod",
      "rdfs:label": "indicativespeedlimit_capturemethod",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/indicativespeedlimit_evidencedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "indicativespeedlimit_evidencedate",
      "rdfs:label": "indicativespeedlimit_evidencedate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/indicativespeedlimit_kph",
      "@type": "rdf:Property",
      "dcterms:identifier": "indicativespeedlimit_kph",
      "rdfs:label": "indicativespeedlimit_kph",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/indicativespeedlimit_mph",
      "@type": "rdf:Property",
      "dcterms:identifier": "indicativespeedlimit_mph",
      "rdfs:label": "indicativespeedlimit_mph",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "integer"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/indicativespeedlimit_source",
      "@type": "rdf:Property",
      "dcterms:identifier": "indicativespeedlimit_source",
      "rdfs:label": "indicativespeedlimit_source",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/indicativespeedlimit_updatedate",
      "@type": "rdf:Property",
      "dcterms:identifier": "indicativespeedlimit_updatedate",
      "rdfs:label": "indicativespeedlimit_updatedate",
      "okfp:schemaDefinition": {
        "@value": {
          "format": "date",
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/name1_language",
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
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/name1_text",
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
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/name2_language",
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
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/name2_text",
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
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/roadclassificationnumber",
      "@type": "rdf:Property",
      "dcterms:identifier": "roadclassificationnumber",
      "rdfs:label": "roadclassificationnumber",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/routehierarchy",
      "@type": "rdf:Property",
      "dcterms:identifier": "routehierarchy",
      "rdfs:label": "routehierarchy",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "A Road",
            "A Road Primary",
            "B Road",
            "B Road Primary",
            "Local Access Road",
            "Local Road",
            "Minor Road",
            "Motorway",
            "Restricted Local Access Road",
            "Restricted Secondary Access Road",
            "Secondary Access Road",
            "Shared Use Road"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/trn-rami-averageandindicativespeed-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/schema"
      }
    }
  ]
}
---

# Average And Indicative Speed v1

This feature type provides two sets of speed information for all roads in Great Britain. These are: 1. A historic average speed in kilometres per hours (kph). In this context, 'historic' means that the average speed data was collected over a six-month period for the selected road link. Average speeds are provided in different time periods for each road link. A single day (i.e. a 24-hour period) is split into 8 time periods Monday to Friday (MF) and 6 time periods Saturday to Sunday (SS), for example, Monday–Friday (MF) 07:00–09:00, Saturday–Sunday (SS) 14:00–19:00. There’s a separate attribute for each time period. 2. An indicative speed limit. This is an indication of the maximum speed limit for vehicles; the indicative speed limits reference road network data. Indicative speed limit values that apply over the majority of a section of road are provided in both miles per hour (mph) and kilometres per hour (kph).

Native identifier: `trn-rami-averageandindicativespeed-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2023-02-03T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
