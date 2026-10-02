---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Collection",
  "title": "Named Point v1",
  "description": "A settlement, locality, geographical feature, or area of water that has a name, represented as a point.",
  "nativeIdentifier": "gnm-fts-namedpoint-1",
  "sourceFamily": "os-ngd-collections",
  "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1",
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
      "sourcePointer": "/collections/12",
      "normalisedSource": "okf-plus/source/os-ngd-collections.json",
      "normalisedPointer": "/records/12",
      "normalisedRecordSha256": "a140b6dbce45d488dcd58c29d6d52acc374a494ebcf21a68347e664f15ab945f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1"
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
    "start": "2022-07-30T00:00:00Z",
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
    "description": "A settlement, locality, geographical feature, or area of water that has a name, represented as a point.",
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
            "2022-07-30T00:00:00Z",
            null
          ]
        ],
        "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
      }
    },
    "id": "gnm-fts-namedpoint-1",
    "itemType": "feature",
    "links": [
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1",
        "rel": "self",
        "title": "The 'Named Point v1' feature collection",
        "type": "application/json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/items",
        "rel": "items",
        "title": "The features in the 'Named Point v1' feature collection as GeoJSON",
        "type": "application/geo+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema",
        "rel": "describedby",
        "title": "Schema for the 'Named Point v1' feature collection",
        "type": "application/schema+json"
      },
      {
        "href": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/queryables",
        "rel": "http://www.opengis.net/def/rel/ogc/1.0/queryables",
        "title": "The queryable attributes for the 'Named Point v1' feature collection",
        "type": "application/schema+json"
      }
    ],
    "schemas": {
      "queryables": {
        "additionalProperties": null,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/queryables",
        "properties": {
          "countrygsscode": {
            "type": [
              "string",
              "null"
            ]
          },
          "description": {
            "enum": [
              "City",
              "Hamlet",
              "Named Area Of Coastal Rock",
              "Named Area Of Railway Land",
              "Named Area Of Sea",
              "Named Area Of Still Water",
              "Named Bay",
              "Named Beach",
              "Named Cirque Or Hollow",
              "Named Cliff Or Slope",
              "Named Coastal Headland",
              "Named Coastal Ravine",
              "Named Estuary",
              "Named Group Of Islands",
              "Named Harbour",
              "Named Hill Or Mountain",
              "Named Inland Water Marsh",
              "Named Island",
              "Named Linear Structure",
              "Named Other Coastal Landform",
              "Named Other Geographic Area",
              "Named Other Land Cover",
              "Named Other Landform",
              "Named Range Of Hills Or Mountains",
              "Named Reservoir",
              "Named Spot Height",
              "Named Stretch Of Inland Water",
              "Named Stretch Of Tidal Water",
              "Named Tidal Land Cover",
              "Named Valley",
              "Named Waterfall",
              "Named Woodland Or Forest",
              "Other Rural Settlement",
              "Other Urban Area",
              "Part Of Settlement",
              "Suburban Area",
              "Town",
              "Village"
            ],
            "type": [
              "string"
            ]
          },
          "descriptiongroup": {
            "enum": [
              "Land Name",
              "Landform Name",
              "Other Name",
              "Settlement",
              "Water Name"
            ],
            "type": [
              "string"
            ]
          },
          "height": {
            "type": [
              "number",
              "null"
            ]
          },
          "lowertierlocalauthoritygsscode": {
            "type": [
              "string",
              "null"
            ]
          },
          "name1_text": {
            "type": [
              "string"
            ]
          },
          "name2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "name3_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "name4_text": {
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
          "regionalauthoritygsscode": {
            "type": [
              "string",
              "null"
            ]
          },
          "regiongsscode": {
            "type": [
              "string",
              "null"
            ]
          },
          "uppertierlocalauthoritygsscode": {
            "type": [
              "string",
              "null"
            ]
          }
        },
        "required": [],
        "requiredUndeclared": [],
        "sha256": "a4d590b62a79d0e70ed9f8ce7c9accaaf8739f038041bdd715b6acacb526ab73",
        "type": "object",
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/queryables"
      },
      "schema": {
        "additionalProperties": false,
        "dialect": "http://json-schema.org/draft-07/schema#",
        "id": "gnm-fts-namedpoint-1.0",
        "properties": {
          "boundedbymaxx": {
            "type": "number"
          },
          "boundedbymaxy": {
            "type": "number"
          },
          "boundedbyminx": {
            "type": "number"
          },
          "boundedbyminy": {
            "type": "number"
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
          "country_name1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "country_name1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "country_name2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "country_name2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "countrygsscode": {
            "type": [
              "string",
              "null"
            ]
          },
          "description": {
            "enum": [
              "City",
              "Hamlet",
              "Named Area Of Coastal Rock",
              "Named Area Of Railway Land",
              "Named Area Of Sea",
              "Named Area Of Still Water",
              "Named Bay",
              "Named Beach",
              "Named Cirque Or Hollow",
              "Named Cliff Or Slope",
              "Named Coastal Headland",
              "Named Coastal Ravine",
              "Named Estuary",
              "Named Group Of Islands",
              "Named Harbour",
              "Named Hill Or Mountain",
              "Named Inland Water Marsh",
              "Named Island",
              "Named Linear Structure",
              "Named Other Coastal Landform",
              "Named Other Geographic Area",
              "Named Other Land Cover",
              "Named Other Landform",
              "Named Range Of Hills Or Mountains",
              "Named Reservoir",
              "Named Spot Height",
              "Named Stretch Of Inland Water",
              "Named Stretch Of Tidal Water",
              "Named Tidal Land Cover",
              "Named Valley",
              "Named Waterfall",
              "Named Woodland Or Forest",
              "Other Rural Settlement",
              "Other Urban Area",
              "Part Of Settlement",
              "Suburban Area",
              "Town",
              "Village"
            ],
            "type": "string"
          },
          "descriptiongroup": {
            "enum": [
              "Land Name",
              "Landform Name",
              "Other Name",
              "Settlement",
              "Water Name"
            ],
            "type": "string"
          },
          "geometry": {
            "$ref": "https://geojson.org/schema/Point.json"
          },
          "height": {
            "type": [
              "number",
              "null"
            ]
          },
          "lowertierlocalauthority_name1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "lowertierlocalauthority_name1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "lowertierlocalauthority_name2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "lowertierlocalauthority_name2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "lowertierlocalauthoritygsscode": {
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
            "type": "string"
          },
          "name1_text": {
            "type": "string"
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
          "name3_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "name3_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "name4_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "name4_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "osid": {
            "type": "string"
          },
          "region_name1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "region_name1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "region_name2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "region_name2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "regionalauthority_name1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "regionalauthority_name1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "regionalauthority_name2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "regionalauthority_name2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "regionalauthoritygsscode": {
            "type": [
              "string",
              "null"
            ]
          },
          "regiongsscode": {
            "type": [
              "string",
              "null"
            ]
          },
          "sameasdbobih": {
            "type": [
              "integer",
              "null"
            ]
          },
          "sameasdbpedia": {
            "type": [
              "string",
              "null"
            ]
          },
          "sameasgeonames": {
            "type": [
              "string",
              "null"
            ]
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
          "uppertierlocalauthority_name1_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "uppertierlocalauthority_name1_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "uppertierlocalauthority_name2_language": {
            "enum": [
              "eng",
              "gla",
              "cym"
            ],
            "type": "string"
          },
          "uppertierlocalauthority_name2_text": {
            "type": [
              "string",
              "null"
            ]
          },
          "uppertierlocalauthoritygsscode": {
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
          "boundedbymaxx",
          "boundedbymaxy",
          "boundedbyminx",
          "boundedbyminy",
          "changetype",
          "description",
          "descriptiongroup",
          "geometry",
          "name1_text",
          "osid",
          "theme",
          "versionavailablefromdate",
          "versiondate"
        ],
        "requiredUndeclared": [],
        "sha256": "c0b8c4a1ac2522b9f26b4b76f674fa4219297e849b8e8ae1e5e65461cd6ef78b",
        "type": null,
        "url": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    "storageCrs": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "title": "Named Point v1"
  },
  "dcterms:temporal": {
    "@type": "dcterms:PeriodOfTime",
    "dcat:startDate": {
      "@value": "2022-07-30T00:00:00Z",
      "@type": "xsd:dateTime"
    }
  },
  "schemaEvidence": {
    "queryables": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/queryables",
      "responseSha256": "a4d590b62a79d0e70ed9f8ce7c9accaaf8739f038041bdd715b6acacb526ab73",
      "requiredUndeclared": []
    },
    "schema": {
      "resource": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema",
      "responseSha256": "c0b8c4a1ac2522b9f26b4b76f674fa4219297e849b8e8ae1e5e65461cd6ef78b",
      "requiredUndeclared": []
    }
  },
  "okfp:field": [
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/boundedbymaxx",
      "@type": "rdf:Property",
      "dcterms:identifier": "boundedbymaxx",
      "rdfs:label": "boundedbymaxx",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/boundedbymaxy",
      "@type": "rdf:Property",
      "dcterms:identifier": "boundedbymaxy",
      "rdfs:label": "boundedbymaxy",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/boundedbyminx",
      "@type": "rdf:Property",
      "dcterms:identifier": "boundedbyminx",
      "rdfs:label": "boundedbyminx",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/boundedbyminy",
      "@type": "rdf:Property",
      "dcterms:identifier": "boundedbyminy",
      "rdfs:label": "boundedbyminy",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "number"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/changetype",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/country_name1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "country_name1_language",
      "rdfs:label": "country_name1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/country_name1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "country_name1_text",
      "rdfs:label": "country_name1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/country_name2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "country_name2_language",
      "rdfs:label": "country_name2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/country_name2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "country_name2_text",
      "rdfs:label": "country_name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/countrygsscode",
      "@type": "rdf:Property",
      "dcterms:identifier": "countrygsscode",
      "rdfs:label": "countrygsscode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/description",
      "@type": "rdf:Property",
      "dcterms:identifier": "description",
      "rdfs:label": "description",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "City",
            "Hamlet",
            "Named Area Of Coastal Rock",
            "Named Area Of Railway Land",
            "Named Area Of Sea",
            "Named Area Of Still Water",
            "Named Bay",
            "Named Beach",
            "Named Cirque Or Hollow",
            "Named Cliff Or Slope",
            "Named Coastal Headland",
            "Named Coastal Ravine",
            "Named Estuary",
            "Named Group Of Islands",
            "Named Harbour",
            "Named Hill Or Mountain",
            "Named Inland Water Marsh",
            "Named Island",
            "Named Linear Structure",
            "Named Other Coastal Landform",
            "Named Other Geographic Area",
            "Named Other Land Cover",
            "Named Other Landform",
            "Named Range Of Hills Or Mountains",
            "Named Reservoir",
            "Named Spot Height",
            "Named Stretch Of Inland Water",
            "Named Stretch Of Tidal Water",
            "Named Tidal Land Cover",
            "Named Valley",
            "Named Waterfall",
            "Named Woodland Or Forest",
            "Other Rural Settlement",
            "Other Urban Area",
            "Part Of Settlement",
            "Suburban Area",
            "Town",
            "Village"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/descriptiongroup",
      "@type": "rdf:Property",
      "dcterms:identifier": "descriptiongroup",
      "rdfs:label": "descriptiongroup",
      "okfp:schemaDefinition": {
        "@value": {
          "enum": [
            "Land Name",
            "Landform Name",
            "Other Name",
            "Settlement",
            "Water Name"
          ],
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/geometry",
      "@type": "rdf:Property",
      "dcterms:identifier": "geometry",
      "rdfs:label": "geometry",
      "okfp:schemaDefinition": {
        "@value": {
          "$ref": "https://geojson.org/schema/Point.json"
        },
        "@type": "@json"
      },
      "okfp:queryable": false,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/height",
      "@type": "rdf:Property",
      "dcterms:identifier": "height",
      "rdfs:label": "height",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/lowertierlocalauthority_name1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "lowertierlocalauthority_name1_language",
      "rdfs:label": "lowertierlocalauthority_name1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/lowertierlocalauthority_name1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "lowertierlocalauthority_name1_text",
      "rdfs:label": "lowertierlocalauthority_name1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/lowertierlocalauthority_name2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "lowertierlocalauthority_name2_language",
      "rdfs:label": "lowertierlocalauthority_name2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/lowertierlocalauthority_name2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "lowertierlocalauthority_name2_text",
      "rdfs:label": "lowertierlocalauthority_name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/lowertierlocalauthoritygsscode",
      "@type": "rdf:Property",
      "dcterms:identifier": "lowertierlocalauthoritygsscode",
      "rdfs:label": "lowertierlocalauthoritygsscode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/name1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/name1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "name1_text",
      "rdfs:label": "name1_text",
      "okfp:schemaDefinition": {
        "@value": {
          "type": "string"
        },
        "@type": "@json"
      },
      "okfp:queryable": true,
      "prov:wasDerivedFrom": {
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/name2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/name3_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "name3_language",
      "rdfs:label": "name3_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/name3_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "name3_text",
      "rdfs:label": "name3_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/name4_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "name4_language",
      "rdfs:label": "name4_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/name4_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "name4_text",
      "rdfs:label": "name4_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/osid",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/region_name1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "region_name1_language",
      "rdfs:label": "region_name1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/region_name1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "region_name1_text",
      "rdfs:label": "region_name1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/region_name2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "region_name2_language",
      "rdfs:label": "region_name2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/region_name2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "region_name2_text",
      "rdfs:label": "region_name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/regionalauthority_name1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "regionalauthority_name1_language",
      "rdfs:label": "regionalauthority_name1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/regionalauthority_name1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "regionalauthority_name1_text",
      "rdfs:label": "regionalauthority_name1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/regionalauthority_name2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "regionalauthority_name2_language",
      "rdfs:label": "regionalauthority_name2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/regionalauthority_name2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "regionalauthority_name2_text",
      "rdfs:label": "regionalauthority_name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/regionalauthoritygsscode",
      "@type": "rdf:Property",
      "dcterms:identifier": "regionalauthoritygsscode",
      "rdfs:label": "regionalauthoritygsscode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/regiongsscode",
      "@type": "rdf:Property",
      "dcterms:identifier": "regiongsscode",
      "rdfs:label": "regiongsscode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/sameasdbobih",
      "@type": "rdf:Property",
      "dcterms:identifier": "sameasdbobih",
      "rdfs:label": "sameasdbobih",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/sameasdbpedia",
      "@type": "rdf:Property",
      "dcterms:identifier": "sameasdbpedia",
      "rdfs:label": "sameasdbpedia",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/sameasgeonames",
      "@type": "rdf:Property",
      "dcterms:identifier": "sameasgeonames",
      "rdfs:label": "sameasgeonames",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/theme",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/uppertierlocalauthority_name1_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "uppertierlocalauthority_name1_language",
      "rdfs:label": "uppertierlocalauthority_name1_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/uppertierlocalauthority_name1_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "uppertierlocalauthority_name1_text",
      "rdfs:label": "uppertierlocalauthority_name1_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/uppertierlocalauthority_name2_language",
      "@type": "rdf:Property",
      "dcterms:identifier": "uppertierlocalauthority_name2_language",
      "rdfs:label": "uppertierlocalauthority_name2_language",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/uppertierlocalauthority_name2_text",
      "@type": "rdf:Property",
      "dcterms:identifier": "uppertierlocalauthority_name2_text",
      "rdfs:label": "uppertierlocalauthority_name2_text",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/uppertierlocalauthoritygsscode",
      "@type": "rdf:Property",
      "dcterms:identifier": "uppertierlocalauthoritygsscode",
      "rdfs:label": "uppertierlocalauthoritygsscode",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/versionavailablefromdate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/versionavailabletodate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    },
    {
      "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-ngd-collections/gnm-fts-namedpoint-1/field/versiondate",
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
        "@id": "https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1/schema"
      }
    }
  ]
}
---

# Named Point v1

A settlement, locality, geographical feature, or area of water that has a name, represented as a point.

Native identifier: `gnm-fts-namedpoint-1`.

Source family: `os-ngd-collections`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://api.os.uk/features/ngd/ofa/v1/collections/gnm-fts-namedpoint-1)

Update cadence: not evidenced in captured metadata.
Temporal evidence: source-stated (advertised-collection-temporal-extent); start 2022-07-30T00:00:00Z, end not stated.
An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.

[Release catalogue or change-discovery route](https://docs.os.uk/osngd/getting-started/os-ngd-release-notes)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
