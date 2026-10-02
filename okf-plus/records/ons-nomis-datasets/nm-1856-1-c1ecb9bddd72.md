---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1856_1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "ST056 - Tenure and amenities by household composition",
  "description": "Nomis dataset definition with native SDMX components.",
  "nativeIdentifier": "NM_1856_1",
  "sourceFamily": "ons-nomis-datasets",
  "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1856_1/def.sdmx.json",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Tenure",
    "Shower",
    "Rented",
    "Owned",
    "Pensioner",
    "One person",
    "Dependent child(ren)",
    "Bath",
    "Amenities",
    "Lone parent"
  ],
  "sources": [
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json",
      "retrievedAt": "2026-10-02T01:18:03.834666Z",
      "responseSha256": "e782c84721db296c396660a4df4b65fa967b9cbab0b52768e1262659e37e9a54",
      "sourcePointer": "/structure/keyfamilies/keyfamily/1191",
      "normalisedSource": "okf-plus/source/ons-nomis-datasets.json",
      "normalisedPointer": "/records/1191",
      "normalisedRecordSha256": "39a6e8e501f6f0fa1b7ae414b74fc0504745ca79f49d4d130b76810bae601964",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1856_1/time.def.sdmx.json",
      "retrievedAt": "2026-10-02T07:51:06.624027Z",
      "responseSha256": "7ccbf78273f1078825c2bf436b43b1e85a881c1763ceea679a41a1e711ad369c",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-nomis-time-options.json",
      "normalisedPointer": "/records/1191",
      "normalisedRecordSha256": "b0dd2a70a2c5eb8a57da3318395c92f84c6b6d00baec120d9a5671e61583b5e6",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1856_1/def.sdmx.json"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": 2001,
    "end": 2001,
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
    "metadataModified": "2003-08-30 09:30:00",
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
      "FirstReleased": "2003-08-30 09:30:00",
      "Keywords": "Tenure,Shower,Rented,Owned,Pensioner,One person,Dependent child(ren),Bath,Amenities,Lone parent",
      "LastUpdated": "2003-08-30 09:30:00",
      "Mnemonic": "st056",
      "Status": "Historical (not actively being updated)",
      "SubDescription": "All households",
      "Units": "Households"
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
          "codelist": "CL_1856_1_GEOGRAPHY",
          "conceptref": "GEOGRAPHY"
        },
        {
          "codelist": "CL_1856_1_C_TENHUK11",
          "conceptref": "C_TENHUK11"
        },
        {
          "codelist": "CL_1856_1_C_AMEN",
          "conceptref": "C_AMEN"
        },
        {
          "codelist": "CL_1856_1_C_HEAT",
          "conceptref": "C_HEAT"
        },
        {
          "codelist": "CL_1856_1_C_HHCHUK11",
          "conceptref": "C_HHCHUK11"
        },
        {
          "codelist": "CL_1856_1_MEASURES",
          "conceptref": "MEASURES"
        },
        {
          "codelist": "CL_1856_1_FREQ",
          "conceptref": "FREQ",
          "isfrequencydimension": "true"
        }
      ],
      "primarymeasure": {
        "conceptref": "OBS_VALUE"
      },
      "timedimension": {
        "codelist": "CL_1856_1_TIME",
        "conceptref": "TIME"
      }
    },
    "id": "NM_1856_1",
    "name": {
      "lang": "en",
      "value": "ST056 - Tenure and amenities by household composition"
    },
    "uri": "Nm-1856d1",
    "version": 1.0,
    "timeMetadata": {
      "bounds": {
        "basis": "Nomis returned TIME codelist native codes; no observations",
        "comparisonRule": "Nomis-native-integer-year.v1",
        "continuityEstablished": false,
        "granularity": "year",
        "maximumNative": 2001,
        "minimumNative": 2001,
        "status": "known-option-extrema"
      },
      "codeListId": "CL_1856_1_TIME",
      "id": "NM_1856_1",
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T07:51:06.624027Z",
        "sha256": "7ccbf78273f1078825c2bf436b43b1e85a881c1763ceea679a41a1e711ad369c",
        "status": 200,
        "url": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1856_1/time.def.sdmx.json"
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
            2001,
            {
              "lang": "en",
              "value": 2001
            },
            [
              [
                "CurrentRevisionReleased",
                "2003-08-30 09:30:00"
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
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1856_1/structure",
    "@type": "qb:DataStructureDefinition",
    "qb:component": [
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1856_1/dimension/GEOGRAPHY",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "GEOGRAPHY",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1856_1_GEOGRAPHY/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1856_1/dimension/C_TENHUK11",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "C_TENHUK11",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1856_1_C_TENHUK11/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1856_1/dimension/C_AMEN",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "C_AMEN",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1856_1_C_AMEN/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1856_1/dimension/C_HEAT",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "C_HEAT",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1856_1_C_HEAT/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1856_1/dimension/C_HHCHUK11",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "C_HHCHUK11",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1856_1_C_HHCHUK11/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1856_1/dimension/MEASURES",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "MEASURES",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1856_1_MEASURES/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1856_1/dimension/FREQ",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "FREQ",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1856_1_FREQ/def.sdmx.json"
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
      "maximumNative": 2001,
      "minimumNative": 2001,
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# ST056 - Tenure and amenities by household composition

Nomis dataset definition with native SDMX components.

Native identifier: `NM_1856_1`.

Source family: `ons-nomis-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.nomisweb.co.uk/api/v01/dataset/NM_1856_1/def.sdmx.json)

Update cadence: not evidenced in captured metadata.
Temporal evidence: normalised-source-options (available-native-period-options); start 2001, end 2001.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.nomisweb.co.uk/releasecalendar.asp)

## Evidence limits

- FREQ denotes statistical observation frequency; it does not establish release cadence.
- FirstReleased and LastUpdated describe publication history, not the observation date range.
- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
