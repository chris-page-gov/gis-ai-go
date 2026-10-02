---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_2217_1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "RM117 - Religion by accommodation type",
  "description": "Nomis dataset definition with native SDMX components.",
  "nativeIdentifier": "NM_2217_1",
  "sourceFamily": "ons-nomis-datasets",
  "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_2217_1/def.sdmx.json",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Accommodation type",
    "Religion"
  ],
  "sources": [
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json",
      "retrievedAt": "2026-10-02T01:18:03.834666Z",
      "responseSha256": "e782c84721db296c396660a4df4b65fa967b9cbab0b52768e1262659e37e9a54",
      "sourcePointer": "/structure/keyfamilies/keyfamily/1481",
      "normalisedSource": "okf-plus/source/ons-nomis-datasets.json",
      "normalisedPointer": "/records/1481",
      "normalisedRecordSha256": "443ae13416056fadbc961cfc3d31b34407fbf63fa5a9e4f498ed073c9d86e9d7",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_2217_1/time.def.sdmx.json",
      "retrievedAt": "2026-10-02T07:55:37.028166Z",
      "responseSha256": "694eeff7e5678e801205974c86f630f68ed60417a1d2f34bb597be9935461f41",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-nomis-time-options.json",
      "normalisedPointer": "/records/1481",
      "normalisedRecordSha256": "7bcc78af68b4c6fae9233cc03ae7bcef890a0da94d9aa16aa189a938e1a47c81",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.nomisweb.co.uk/api/v01/dataset/NM_2217_1/def.sdmx.json"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": 2021,
    "end": 2021,
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
    "metadataModified": null,
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
      "Keywords": "Accommodation type,Religion",
      "Mnemonic": "c2021rm117",
      "Status": "Current (being actively updated)",
      "SubDescription": "All usual residents in households",
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
          "codelist": "CL_2217_1_GEOGRAPHY",
          "conceptref": "GEOGRAPHY"
        },
        {
          "codelist": "CL_2217_1_C2021_ACCTYPE_6",
          "conceptref": "C2021_ACCTYPE_6"
        },
        {
          "codelist": "CL_2217_1_C2021_RELIGION_10",
          "conceptref": "C2021_RELIGION_10"
        },
        {
          "codelist": "CL_2217_1_MEASURES",
          "conceptref": "MEASURES"
        },
        {
          "codelist": "CL_2217_1_FREQ",
          "conceptref": "FREQ",
          "isfrequencydimension": "true"
        }
      ],
      "primarymeasure": {
        "conceptref": "OBS_VALUE"
      },
      "timedimension": {
        "codelist": "CL_2217_1_TIME",
        "conceptref": "TIME"
      }
    },
    "id": "NM_2217_1",
    "name": {
      "lang": "en",
      "value": "RM117 - Religion by accommodation type"
    },
    "uri": "Nm-2217d1",
    "version": 1.0,
    "timeMetadata": {
      "bounds": {
        "basis": "Nomis returned TIME codelist native codes; no observations",
        "comparisonRule": "Nomis-native-integer-year.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": 2021,
        "minimumNative": 2021,
        "status": "known-option-extrema"
      },
      "codeListId": "CL_2217_1_TIME",
      "id": "NM_2217_1",
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T07:55:37.028166Z",
        "sha256": "694eeff7e5678e801205974c86f630f68ed60417a1d2f34bb597be9935461f41",
        "status": 200,
        "url": "https://www.nomisweb.co.uk/api/v01/dataset/NM_2217_1/time.def.sdmx.json"
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
            2021,
            {
              "lang": "en",
              "value": 2021
            },
            []
          ]
        ]
      }
    }
  },
  "qb:structure": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_2217_1/structure",
    "@type": "qb:DataStructureDefinition",
    "qb:component": [
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_2217_1/dimension/GEOGRAPHY",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "GEOGRAPHY",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_2217_1_GEOGRAPHY/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_2217_1/dimension/C2021_ACCTYPE_6",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "C2021_ACCTYPE_6",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_2217_1_C2021_ACCTYPE_6/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_2217_1/dimension/C2021_RELIGION_10",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "C2021_RELIGION_10",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_2217_1_C2021_RELIGION_10/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_2217_1/dimension/MEASURES",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "MEASURES",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_2217_1_MEASURES/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_2217_1/dimension/FREQ",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "FREQ",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_2217_1_FREQ/def.sdmx.json"
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
      "maximumNative": 2021,
      "minimumNative": 2021,
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# RM117 - Religion by accommodation type

Nomis dataset definition with native SDMX components.

Native identifier: `NM_2217_1`.

Source family: `ons-nomis-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.nomisweb.co.uk/api/v01/dataset/NM_2217_1/def.sdmx.json)

Update cadence: not evidenced in captured metadata.
Temporal evidence: normalised-source-options (available-native-period-options); start 2021, end 2021.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.nomisweb.co.uk/releasecalendar.asp)

## Evidence limits

- FREQ denotes statistical observation frequency; it does not establish release cadence.
- FirstReleased and LastUpdated describe publication history, not the observation date range.
- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
