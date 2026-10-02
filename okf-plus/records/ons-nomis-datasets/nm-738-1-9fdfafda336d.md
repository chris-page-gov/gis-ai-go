---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_738_1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "DC2209EWr - Country of birth by national identity (regional)",
  "description": "Nomis dataset definition with native SDMX components.",
  "nativeIdentifier": "NM_738_1",
  "sourceFamily": "ons-nomis-datasets",
  "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_738_1/def.sdmx.json",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Country of Birth",
    "National Identity"
  ],
  "sources": [
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json",
      "retrievedAt": "2026-10-02T01:18:03.834666Z",
      "responseSha256": "e782c84721db296c396660a4df4b65fa967b9cbab0b52768e1262659e37e9a54",
      "sourcePointer": "/structure/keyfamilies/keyfamily/357",
      "normalisedSource": "okf-plus/source/ons-nomis-datasets.json",
      "normalisedPointer": "/records/357",
      "normalisedRecordSha256": "d439fb076b276cb360849b3654fb53ce0d7c7bae9ce731cb677ee2ff7eec807d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_738_1/time.def.sdmx.json",
      "retrievedAt": "2026-10-02T07:38:01.770944Z",
      "responseSha256": "0599d2cadae466363fff9fb73aef467c99ca7d834e353316e6918e6bb1e4502f",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-nomis-time-options.json",
      "normalisedPointer": "/records/357",
      "normalisedRecordSha256": "4edfcf33efe98dc108396ab4702b43afc28bcf316d562c8d84cc184828c98ed7",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.nomisweb.co.uk/api/v01/dataset/NM_738_1/def.sdmx.json"
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
    "metadataModified": "2013-07-12 09:30:00",
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
      "FirstReleased": "2013-07-12 09:30:00",
      "Keywords": "Country of Birth,National Identity",
      "LastUpdated": "2013-07-12 09:30:00",
      "Mnemonic": "c2011dc2209ewr",
      "Status": "Current (being actively updated)",
      "SubDescription": "All usual residents",
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
          "codelist": "CL_738_1_GEOGRAPHY",
          "conceptref": "GEOGRAPHY"
        },
        {
          "codelist": "CL_738_1_C_COB",
          "conceptref": "C_COB"
        },
        {
          "codelist": "CL_738_1_NATID_ALL",
          "conceptref": "NATID_ALL"
        },
        {
          "codelist": "CL_738_1_MEASURES",
          "conceptref": "MEASURES"
        },
        {
          "codelist": "CL_738_1_FREQ",
          "conceptref": "FREQ",
          "isfrequencydimension": "true"
        }
      ],
      "primarymeasure": {
        "conceptref": "OBS_VALUE"
      },
      "timedimension": {
        "codelist": "CL_738_1_TIME",
        "conceptref": "TIME"
      }
    },
    "id": "NM_738_1",
    "name": {
      "lang": "en",
      "value": "DC2209EWr - Country of birth by national identity (regional)"
    },
    "uri": "Nm-738d1",
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
      "codeListId": "CL_738_1_TIME",
      "id": "NM_738_1",
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T07:38:01.770944Z",
        "sha256": "0599d2cadae466363fff9fb73aef467c99ca7d834e353316e6918e6bb1e4502f",
        "status": 200,
        "url": "https://www.nomisweb.co.uk/api/v01/dataset/NM_738_1/time.def.sdmx.json"
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
                "2013-07-12 09:30:00"
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
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_738_1/structure",
    "@type": "qb:DataStructureDefinition",
    "qb:component": [
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_738_1/dimension/GEOGRAPHY",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "GEOGRAPHY",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_738_1_GEOGRAPHY/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_738_1/dimension/C_COB",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "C_COB",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_738_1_C_COB/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_738_1/dimension/NATID_ALL",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "NATID_ALL",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_738_1_NATID_ALL/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_738_1/dimension/MEASURES",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "MEASURES",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_738_1_MEASURES/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_738_1/dimension/FREQ",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "FREQ",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_738_1_FREQ/def.sdmx.json"
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

# DC2209EWr - Country of birth by national identity (regional)

Nomis dataset definition with native SDMX components.

Native identifier: `NM_738_1`.

Source family: `ons-nomis-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.nomisweb.co.uk/api/v01/dataset/NM_738_1/def.sdmx.json)

Update cadence: not evidenced in captured metadata.
Temporal evidence: normalised-source-options (available-native-period-options); start 2011, end 2011.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.nomisweb.co.uk/releasecalendar.asp)

## Evidence limits

- FREQ denotes statistical observation frequency; it does not establish release cadence.
- FirstReleased and LastUpdated describe publication history, not the observation date range.
- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
