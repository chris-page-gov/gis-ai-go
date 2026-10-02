---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-names-api%2Ftechnical-specification%2Ffind.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "Find",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-names-api/technical-specification/find.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-names-api/technical-specification/find.md",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "specification",
    "documentation"
  ],
  "sources": [
    {
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-names-api/technical-specification/find.md",
      "retrievedAt": "2026-10-02T07:28:07.628581Z",
      "responseSha256": "e43dcdbd9791eeef25d5df3ee38b892fdc31c17f7b5c42ebcd6890934c46646f",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/108",
      "normalisedRecordSha256": "15157db77e4dd42779248b17781b58c027e3a9ebfb9535b12974803164f57721",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-names-api/technical-specification/find.md"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "not-applicable",
    "kind": "dataset-reference-period",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "Dataset reference-period extent is not applicable to this record type."
  },
  "update": {
    "frequency": {
      "status": "not-applicable",
      "label": null,
      "iri": null,
      "sourceField": null
    },
    "releaseCatalogue": [],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": null,
    "releaseVersion": null
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [],
  "details": {
    "callable": false,
    "contentCaptured": true,
    "contracts": [
      {
        "componentParameters": {},
        "fragmentSha256": "744674a8eb04f7a2ab28d9ef09661fdeea0992928913ffdba56bd1de91e86bfe",
        "jsonFence": 1,
        "openapi": "3.0.1",
        "operations": [
          {
            "admission": "not-reviewed",
            "callable": false,
            "deprecated": false,
            "documentedSecurity": [
              {
                "api-key": [],
                "api-key-header": [],
                "oauth2": []
              }
            ],
            "httpMethodSemantics": "safe-method",
            "method": "GET",
            "operationId": "findAddress",
            "parameters": [
              {
                "in": "query",
                "name": "query",
                "required": true,
                "schema": {
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "format",
                "schema": {
                  "enum": [
                    "JSON",
                    "XML"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "query",
                "name": "maxresults",
                "schema": {
                  "maximum": 100,
                  "minimum": 1,
                  "type": "integer"
                },
                "style": "form"
              },
              {
                "in": "query",
                "name": "offset",
                "schema": {
                  "minimum": 1,
                  "type": "integer"
                }
              },
              {
                "explode": false,
                "in": "query",
                "name": "bounds",
                "schema": {
                  "items": {
                    "type": "number"
                  },
                  "maxItems": 4,
                  "minItems": 4,
                  "type": "array"
                },
                "style": "form"
              },
              {
                "in": "query",
                "name": "fq",
                "schema": {
                  "enum": [
                    "Airfield",
                    "Airport",
                    "Bay",
                    "Beach",
                    "Bus_Station",
                    "Channel",
                    "Chemical_Works",
                    "Cirque_Or_Hollow",
                    "City",
                    "Cliff_Or_Slope",
                    "Coach_Station",
                    "Coastal_Headland",
                    "Electricity_Distribution",
                    "Electricity_Production",
                    "Estuary",
                    "Further_Education",
                    "Gas_Distribution_or_Storage",
                    "Group_Of_Islands",
                    "Hamlet",
                    "Harbour",
                    "Helicopter_Station",
                    "Heliport",
                    "Higher_or_University_Education",
                    "Hill_Or_Mountain",
                    "Hill_Or_Mountain_Ranges",
                    "Hospice",
                    "Hospital",
                    "Inland_Water",
                    "Island",
                    "Medical_Care_Accommodation",
                    "Named_Road",
                    "Non_State_Primary_Education",
                    "Non_State_Secondary_Education",
                    "Numbered_Road",
                    "Oil_Distribution_or_Storage",
                    "Oil_Refining",
                    "Oil_Terminal",
                    "Other_Coastal_Landform",
                    "Other_Landcover",
                    "Other_Landform",
                    "Other_Settlement",
                    "Passenger_Ferry_Terminal",
                    "Port_Consisting_of_Docks_and_Nautical_Berthing",
                    "Postcode",
                    "Primary_Education",
                    "Railway",
                    "Railway_Station",
                    "Road_User_Services",
                    "Sea",
                    "Secondary_Education",
                    "Section_Of_Named_Road",
                    "Section_Of_Numbered_Road",
                    "Special_Needs_Education",
                    "Spot_Height",
                    "Suburban_Area",
                    "Tidal_Water",
                    "Town",
                    "Tramway",
                    "Urban_Greenspace",
                    "Valley",
                    "Vehicular_Ferry_Terminal",
                    "Vehicular_Rail_Terminal",
                    "Village",
                    "Waterfall",
                    "Wetland",
                    "Woodland_Or_Forest"
                  ],
                  "type": "string"
                }
              }
            ],
            "path": "/find",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/SearchResponse"
                    }
                  },
                  "application/xml": {
                    "schema": {
                      "$ref": "#/components/schemas/SearchResponse"
                    }
                  }
                }
              }
            },
            "securityDeclaration": "root"
          }
        ],
        "schemas": {
          "GazetteerEntry": {
            "properties": {
              "GAZETTEER_ENTRY": {
                "properties": {
                  "COUNTRY": {
                    "type": "string"
                  },
                  "COUNTRY_URI": {
                    "type": "string"
                  },
                  "COUNTY_UNITARY": {
                    "type": "string"
                  },
                  "COUNTY_UNITARY_TYPE": {
                    "type": "string"
                  },
                  "COUNTY_UNITARY_URI": {
                    "type": "string"
                  },
                  "GEOMETRY_X": {
                    "type": "number"
                  },
                  "GEOMETRY_Y": {
                    "type": "number"
                  },
                  "ID": {
                    "type": "string"
                  },
                  "LEAST_DETAIL_VIEW_RES": {
                    "type": "integer"
                  },
                  "LOCAL_TYPE": {
                    "type": "string"
                  },
                  "MBR_XMAX": {
                    "type": "number"
                  },
                  "MBR_XMIN": {
                    "type": "number"
                  },
                  "MBR_YMAX": {
                    "type": "number"
                  },
                  "MBR_YMIN": {
                    "type": "number"
                  },
                  "MOST_DETAIL_VIEW_RES": {
                    "type": "integer"
                  },
                  "NAME1": {
                    "type": "string"
                  },
                  "NAMES_URI": {
                    "type": "string"
                  },
                  "POPULATED_PLACE": {
                    "type": "string"
                  },
                  "POPULATED_PLACE_TYPE": {
                    "type": "string"
                  },
                  "POPULATED_PLACE_URI": {
                    "type": "string"
                  },
                  "POSTCODE_DISTRICT": {
                    "type": "string"
                  },
                  "POSTCODE_DISTRICT_URI": {
                    "type": "string"
                  },
                  "REGION": {
                    "type": "string"
                  },
                  "REGION_URI": {
                    "type": "string"
                  },
                  "TYPE": {
                    "type": "string"
                  }
                },
                "type": "object"
              }
            },
            "type": "object"
          },
          "Header": {
            "properties": {
              "format": {
                "type": "string"
              },
              "maxresults": {
                "type": "integer"
              },
              "offset": {
                "type": "integer"
              },
              "query": {
                "type": "string"
              },
              "totalresults": {
                "type": "integer"
              },
              "uri": {
                "type": "string"
              }
            },
            "type": "object"
          },
          "SearchResponse": {
            "properties": {
              "header": {
                "$ref": "#/components/schemas/Header"
              },
              "results": {
                "items": {
                  "$ref": "#/components/schemas/GazetteerEntry"
                },
                "type": "array"
              }
            },
            "type": "object"
          }
        },
        "securitySchemes": {
          "api-key": {
            "in": "query",
            "name": "key",
            "type": "apiKey"
          }
        },
        "servers": [
          "https://api.os.uk/search/names/v1"
        ],
        "title": "OS Names API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.0"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-names-api/technical-specification/find.md",
    "kind": "documentation-contract",
    "sourceSha256": "e43dcdbd9791eeef25d5df3ee38b892fdc31c17f7b5c42ebcd6890934c46646f",
    "title": "Find",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-names-api/technical-specification/find.md"
  }
}
---

# Find

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-names-api/technical-specification/find.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-names-api/technical-specification/find.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
