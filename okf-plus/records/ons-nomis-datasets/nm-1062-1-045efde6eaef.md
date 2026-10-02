---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1062_1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "LC4415EW - Accommodation type by car or van availability by number of usual residents aged 17 or over in household",
  "description": "Nomis dataset definition with native SDMX components.",
  "nativeIdentifier": "NM_1062_1",
  "sourceFamily": "ons-nomis-datasets",
  "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1062_1/def.sdmx.json",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Accommodation type",
    "Cars or Vans",
    "Usual Resident",
    "Household"
  ],
  "sources": [
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json",
      "retrievedAt": "2026-10-02T01:18:03.834666Z",
      "responseSha256": "e782c84721db296c396660a4df4b65fa967b9cbab0b52768e1262659e37e9a54",
      "sourcePointer": "/structure/keyfamilies/keyfamily/639",
      "normalisedSource": "okf-plus/source/ons-nomis-datasets.json",
      "normalisedPointer": "/records/639",
      "normalisedRecordSha256": "8a8bb9678a9cde92cb1bc9ee98a426fe2720cdf7cb9c638b51cbde7aff1c4a48",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1062_1/time.def.sdmx.json",
      "retrievedAt": "2026-10-02T07:42:26.649551Z",
      "responseSha256": "0b862b988226a9fe336ee3cc522fd9fcc714a36a1b8cc90be671411346dd8afb",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-nomis-time-options.json",
      "normalisedPointer": "/records/639",
      "normalisedRecordSha256": "baab68985478d4ed5da77f775e06821b5d1b65c6a1c190eeeae5d1f6817dc0ea",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1062_1/def.sdmx.json"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": 2011,
    "end": 2011,
    "sourceField": "timeMetadata.codes",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "year",
    "derivation": "Nomis-native-integer-year.v1"
  },
  "update": {
    "frequency": {
      "status": "not-evidenced",
      "label": null,
      "iri": null,
      "sourceField": null
    },
    "releaseCatalogue": [
      "https://www.nomisweb.co.uk/releasecalendar.asp"
    ],
    "releaseFeed": [],
    "nextRelease": null,
    "metadataModified": "2014-03-26 09:30:00",
    "releaseVersion": null
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "FREQ denotes statistical observation frequency; it does not establish release cadence.",
    "FirstReleased and LastUpdated describe publication history, not the observation date range.",
    "Time-option extrema describe available native codes; continuity and populated observation cells have not been established."
  ],
  "details": {
    "agencyid": "NOMIS",
    "annotations": {
      "FirstReleased": "2014-03-26 09:30:00",
      "Keywords": "Accommodation type,Cars or Vans,Usual Resident,Household",
      "LastUpdated": "2014-03-26 09:30:00",
      "Mnemonic": "c2011lc4415ew",
      "Status": "Current (being actively updated)",
      "SubDescription": "All households",
      "Units": "Persons"
    },
    "components": {
      "attribute": [
        {
          "assignmentstatus": "Mandatory",
          "attachmentlevel": "Observation",
          "codelist": "CL_OBS_STATUS",
          "conceptref": "OBS_STATUS"
        },
        {
          "assignmentstatus": "Conditional",
          "attachmentlevel": "Observation",
          "codelist": "CL_OBS_CONF",
          "conceptref": "OBS_CONF"
        },
        {
          "assignmentstatus": "Conditional",
          "attachmentlevel": "Observation",
          "codelist": "CL_OBS_ROUND",
          "conceptref": "OBS_ROUND"
        },
        {
          "assignmentstatus": "Conditional",
          "attachmentlevel": "Series",
          "codelist": "CL_UNIT_MULT",
          "conceptref": "UNIT_MULTIPLIER"
        },
        {
          "assignmentstatus": "Mandatory",
          "attachmentlevel": "Series",
          "codelist": "CL_TIME_FORMAT",
          "conceptref": "TIME_FORMAT"
        },
        {
          "assignmentstatus": "Mandatory",
          "attachmentlevel": "Series",
          "codelist": "CL_UNIT",
          "conceptref": "UNIT"
        },
        {
          "assignmentstatus": "Mandatory",
          "attachmentlevel": "Series",
          "conceptref": "TITLE_COMPL"
        }
      ],
      "dimension": [
        {
          "codelist": "CL_1062_1_GEOGRAPHY",
          "conceptref": "GEOGRAPHY"
        },
        {
          "codelist": "CL_1062_1_C_TYPACCOM",
          "conceptref": "C_TYPACCOM"
        },
        {
          "codelist": "CL_1062_1_C_CARSNO",
          "conceptref": "C_CARSNO"
        },
        {
          "codelist": "CL_1062_1_C_P17HUK11",
          "conceptref": "C_P17HUK11"
        },
        {
          "codelist": "CL_1062_1_MEASURES",
          "conceptref": "MEASURES"
        },
        {
          "codelist": "CL_1062_1_FREQ",
          "conceptref": "FREQ",
          "isfrequencydimension": "true"
        }
      ],
      "primarymeasure": {
        "conceptref": "OBS_VALUE"
      },
      "timedimension": {
        "codelist": "CL_1062_1_TIME",
        "conceptref": "TIME"
      }
    },
    "id": "NM_1062_1",
    "name": {
      "lang": "en",
      "value": "LC4415EW - Accommodation type by car or van availability by number of usual residents aged 17 or over in household"
    },
    "uri": "Nm-1062d1",
    "version": 1.0,
    "timeMetadata": {
      "bounds": {
        "basis": "Nomis returned TIME codelist native codes; no observations",
        "comparisonRule": "Nomis-native-integer-year.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": 2011,
        "minimumNative": 2011,
        "status": "known-option-extrema"
      },
      "codeListId": "CL_1062_1_TIME",
      "id": "NM_1062_1",
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T07:42:26.649551Z",
        "sha256": "0b862b988226a9fe336ee3cc522fd9fcc714a36a1b8cc90be671411346dd8afb",
        "status": 200,
        "url": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1062_1/time.def.sdmx.json"
      },
      "metadataStatus": "captured",
      "returnedCodeCount": 1,
      "timeOptionsTable": {
        "encoding": "gis-ai-go.native-time-table.v1",
        "columns": [
          "value",
          "description",
          "revisionMetadata"
        ],
        "revisionColumns": [
          "title",
          "value"
        ],
        "absentDescription": null,
        "rows": [
          [
            2011,
            {
              "lang": "en",
              "value": 2011
            },
            [
              [
                "CurrentRevisionReleased",
                "2014-03-26 09:30:00"
              ],
              [
                "CurrentRevisionStatus",
                "Live"
              ],
              [
                "CurrentRevisionVersion",
                0
              ]
            ]
          ]
        ]
      }
    }
  },
  "qb:structure": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1062_1/structure",
    "@type": "qb:DataStructureDefinition",
    "qb:component": [
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1062_1/dimension/GEOGRAPHY",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "GEOGRAPHY",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1062_1_GEOGRAPHY/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1062_1/dimension/C_TYPACCOM",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "C_TYPACCOM",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1062_1_C_TYPACCOM/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1062_1/dimension/C_CARSNO",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "C_CARSNO",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1062_1_C_CARSNO/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1062_1/dimension/C_P17HUK11",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "C_P17HUK11",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1062_1_C_P17HUK11/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1062_1/dimension/MEASURES",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "MEASURES",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1062_1_MEASURES/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1062_1/dimension/FREQ",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "FREQ",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1062_1_FREQ/def.sdmx.json"
          }
        }
      }
    ]
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "Nomis returned TIME codelist native codes; no observations",
      "comparisonRule": "Nomis-native-integer-year.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": 2011,
      "minimumNative": 2011,
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# LC4415EW - Accommodation type by car or van availability by number of usual residents aged 17 or over in household

Nomis dataset definition with native SDMX components.

Native identifier: `NM_1062_1`.

Source family: `ons-nomis-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.nomisweb.co.uk/api/v01/dataset/NM_1062_1/def.sdmx.json)

Update cadence: not evidenced in captured metadata.
Temporal evidence: normalised-source-options (available-native-period-options); start 2011, end 2011.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.nomisweb.co.uk/releasecalendar.asp)

## Evidence limits

- FREQ denotes statistical observation frequency; it does not establish release cadence.
- FirstReleased and LastUpdated describe publication history, not the observation date range.
- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
