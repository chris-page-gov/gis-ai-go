---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/os-api-contracts/https%3A%2F%2Fdocs.os.uk%2Fos-apis%2Faccessing-os-apis%2Fos-maps-api%2Ftechnical-specification%2Fzxy.md",
  "@type": [
    "dcterms:Standard",
    "okfp:MetadataRecord"
  ],
  "type": "Specification",
  "title": "ZXY",
  "description": "Captured official documentation with extracted API contract fragments.",
  "nativeIdentifier": "https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/zxy.md",
  "sourceFamily": "os-api-contracts",
  "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/zxy.md",
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
      "resource": "https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/zxy.md",
      "retrievedAt": "2026-10-02T07:27:45.012742Z",
      "responseSha256": "dcf4adbcaa5c67a7450e7be1758056012480f30206b21da534c9158b256e0717",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/os-api-contracts.json",
      "normalisedPointer": "/records/91",
      "normalisedRecordSha256": "239b3610430cb837cb5bb116a1d9bbd414180467d31cffe1a822bf00659238db",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/zxy.md"
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
        "fragmentSha256": "95584de19ec805ea27b019eadd75a18adb165a883cf36cdab1d238720620d24b",
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
            "operationId": "getZXYTileData",
            "parameters": [
              {
                "in": "path",
                "name": "layer",
                "required": true,
                "schema": {
                  "enum": [
                    "Road_27700",
                    "Road_3857",
                    "Outdoor_27700",
                    "Outdoor_3857",
                    "Light_27700",
                    "Light_3857",
                    "Leisure_27700"
                  ],
                  "type": "string"
                }
              },
              {
                "in": "path",
                "name": "z",
                "required": true,
                "schema": {
                  "format": "int32",
                  "type": "integer"
                }
              },
              {
                "in": "path",
                "name": "x",
                "required": true,
                "schema": {
                  "format": "int32",
                  "type": "integer"
                }
              },
              {
                "in": "path",
                "name": "y",
                "required": true,
                "schema": {
                  "format": "int32",
                  "type": "integer"
                }
              }
            ],
            "path": "/zxy/{layer}/{z}/{x}/{y}.png",
            "responses": {
              "200": {
                "content": {
                  "image/png": {
                    "schema": {}
                  }
                }
              }
            },
            "securityDeclaration": "root"
          }
        ],
        "schemas": {},
        "securitySchemes": {
          "api-key": {
            "in": "query",
            "name": "key",
            "type": "apiKey"
          }
        },
        "servers": [
          "https://api.os.uk/maps/raster/v1"
        ],
        "title": "OS Maps API",
        "unresolvedComponentClasses": [],
        "validationStatus": "extracted-not-conformance-validated",
        "version": "v1.0"
      }
    ],
    "extractionErrors": [],
    "id": "https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/zxy.md",
    "kind": "documentation-contract",
    "sourceSha256": "dcf4adbcaa5c67a7450e7be1758056012480f30206b21da534c9158b256e0717",
    "title": "ZXY",
    "url": "https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/zxy.md"
  }
}
---

# ZXY

Captured official documentation with extracted API contract fragments.

Native identifier: `https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/zxy.md`.

Source family: `os-api-contracts`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://docs.os.uk/os-apis/accessing-os-apis/os-maps-api/technical-specification/zxy.md)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.


The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
