---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_69_1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "benefit claimants 5% data - working age families",
  "description": "The families dataset enables users to simply identify benefit units which include children. The dataset consists of adults of working age who receive additional allowances for dependent children and is a subset of claimants who appear on the working age client group dataset.",
  "nativeIdentifier": "NM_69_1",
  "sourceFamily": "ons-nomis-datasets",
  "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_69_1/def.sdmx.json",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "DWP benefits",
    "Claimants",
    "Families",
    "Working age"
  ],
  "sources": [
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json",
      "retrievedAt": "2026-10-02T01:18:03.834666Z",
      "responseSha256": "e782c84721db296c396660a4df4b65fa967b9cbab0b52768e1262659e37e9a54",
      "sourcePointer": "/structure/keyfamilies/keyfamily/47",
      "normalisedSource": "okf-plus/source/ons-nomis-datasets.json",
      "normalisedPointer": "/records/47",
      "normalisedRecordSha256": "fd558f65e43516824d997805504a60c96dc8bcee129a27271f91825695191263",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_69_1/time.def.sdmx.json",
      "retrievedAt": "2026-10-02T07:33:03.521148Z",
      "responseSha256": "ffa8ce0b164efb75d84eb839c569177c7025e8e191385739bb1831d8833bb8bc",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-nomis-time-options.json",
      "normalisedPointer": "/records/47",
      "normalisedRecordSha256": "9da2052d3a5716725142c58c714086364add84278593b72c216cc66cfb6cd46f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.nomisweb.co.uk/api/v01/dataset/NM_69_1/def.sdmx.json"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "1995-05",
    "end": "2007-08",
    "sourceField": "timeMetadata.codes",
    "note": "Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.",
    "precision": "month",
    "derivation": "ONS-native-ISO-period-code.v1"
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
    "metadataModified": "2016-11-16 09:30:00",
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
      "FirstReleased": "2005-10-30 09:30:00",
      "Keywords": "DWP benefits,Claimants,Families,Working age",
      "LastUpdated": "2016-11-16 09:30:00",
      "Mnemonic": "bcgwaf",
      "Status": "Current (being actively updated)",
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
          "codelist": "CL_69_1_GEOGRAPHY",
          "conceptref": "GEOGRAPHY"
        },
        {
          "codelist": "CL_69_1_SEX",
          "conceptref": "SEX"
        },
        {
          "codelist": "CL_69_1_AGE",
          "conceptref": "AGE"
        },
        {
          "codelist": "CL_69_1_DURATION",
          "conceptref": "DURATION"
        },
        {
          "codelist": "CL_69_1_FAMILY_TYPE",
          "conceptref": "FAMILY_TYPE"
        },
        {
          "codelist": "CL_69_1_STAT_GROUP",
          "conceptref": "STAT_GROUP"
        },
        {
          "codelist": "CL_69_1_BENEFIT",
          "conceptref": "BENEFIT"
        },
        {
          "codelist": "CL_69_1_MEASURES",
          "conceptref": "MEASURES"
        },
        {
          "codelist": "CL_69_1_FREQ",
          "conceptref": "FREQ",
          "isfrequencydimension": "true"
        }
      ],
      "primarymeasure": {
        "conceptref": "OBS_VALUE"
      },
      "timedimension": {
        "codelist": "CL_69_1_TIME",
        "conceptref": "TIME"
      }
    },
    "description": {
      "lang": "en",
      "value": "The families dataset enables users to simply identify benefit units which include children. The dataset consists of adults of working age who receive additional allowances for dependent children and is a subset of claimants who appear on the working age client group dataset."
    },
    "id": "NM_69_1",
    "name": {
      "lang": "en",
      "value": "benefit claimants 5% data - working age families"
    },
    "uri": "Nm-69d1",
    "version": 1.0,
    "timeMetadata": {
      "bounds": {
        "basis": "Nomis returned TIME codelist native codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "month",
        "maximumNative": "2007-08",
        "minimumNative": "1995-05",
        "status": "known-option-extrema"
      },
      "codeListId": "CL_69_1_TIME",
      "id": "NM_69_1",
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T07:33:03.521148Z",
        "sha256": "ffa8ce0b164efb75d84eb839c569177c7025e8e191385739bb1831d8833bb8bc",
        "status": 200,
        "url": "https://www.nomisweb.co.uk/api/v01/dataset/NM_69_1/time.def.sdmx.json"
      },
      "metadataStatus": "captured",
      "returnedCodeCount": 50,
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
            "1995-05",
            {
              "lang": "en",
              "value": "May 1995"
            },
            []
          ],
          [
            "1995-08",
            {
              "lang": "en",
              "value": "August 1995"
            },
            []
          ],
          [
            "1995-11",
            {
              "lang": "en",
              "value": "November 1995"
            },
            []
          ],
          [
            "1996-02",
            {
              "lang": "en",
              "value": "February 1996"
            },
            []
          ],
          [
            "1996-05",
            {
              "lang": "en",
              "value": "May 1996"
            },
            []
          ],
          [
            "1996-08",
            {
              "lang": "en",
              "value": "August 1996"
            },
            []
          ],
          [
            "1996-11",
            {
              "lang": "en",
              "value": "November 1996"
            },
            []
          ],
          [
            "1997-02",
            {
              "lang": "en",
              "value": "February 1997"
            },
            []
          ],
          [
            "1997-05",
            {
              "lang": "en",
              "value": "May 1997"
            },
            []
          ],
          [
            "1997-08",
            {
              "lang": "en",
              "value": "August 1997"
            },
            []
          ],
          [
            "1997-11",
            {
              "lang": "en",
              "value": "November 1997"
            },
            []
          ],
          [
            "1998-02",
            {
              "lang": "en",
              "value": "February 1998"
            },
            []
          ],
          [
            "1998-05",
            {
              "lang": "en",
              "value": "May 1998"
            },
            []
          ],
          [
            "1998-08",
            {
              "lang": "en",
              "value": "August 1998"
            },
            []
          ],
          [
            "1998-11",
            {
              "lang": "en",
              "value": "November 1998"
            },
            []
          ],
          [
            "1999-02",
            {
              "lang": "en",
              "value": "February 1999"
            },
            []
          ],
          [
            "1999-05",
            {
              "lang": "en",
              "value": "May 1999"
            },
            []
          ],
          [
            "1999-08",
            {
              "lang": "en",
              "value": "August 1999"
            },
            []
          ],
          [
            "1999-11",
            {
              "lang": "en",
              "value": "November 1999"
            },
            []
          ],
          [
            "2000-02",
            {
              "lang": "en",
              "value": "February 2000"
            },
            []
          ],
          [
            "2000-05",
            {
              "lang": "en",
              "value": "May 2000"
            },
            []
          ],
          [
            "2000-08",
            {
              "lang": "en",
              "value": "August 2000"
            },
            []
          ],
          [
            "2000-11",
            {
              "lang": "en",
              "value": "November 2000"
            },
            []
          ],
          [
            "2001-02",
            {
              "lang": "en",
              "value": "February 2001"
            },
            []
          ],
          [
            "2001-05",
            {
              "lang": "en",
              "value": "May 2001"
            },
            []
          ],
          [
            "2001-08",
            {
              "lang": "en",
              "value": "August 2001"
            },
            []
          ],
          [
            "2001-11",
            {
              "lang": "en",
              "value": "November 2001"
            },
            []
          ],
          [
            "2002-02",
            {
              "lang": "en",
              "value": "February 2002"
            },
            []
          ],
          [
            "2002-05",
            {
              "lang": "en",
              "value": "May 2002"
            },
            []
          ],
          [
            "2002-08",
            {
              "lang": "en",
              "value": "August 2002"
            },
            []
          ],
          [
            "2002-11",
            {
              "lang": "en",
              "value": "November 2002"
            },
            []
          ],
          [
            "2003-02",
            {
              "lang": "en",
              "value": "February 2003"
            },
            []
          ],
          [
            "2003-05",
            {
              "lang": "en",
              "value": "May 2003"
            },
            []
          ],
          [
            "2003-08",
            {
              "lang": "en",
              "value": "August 2003"
            },
            []
          ],
          [
            "2003-11",
            {
              "lang": "en",
              "value": "November 2003"
            },
            []
          ],
          [
            "2004-02",
            {
              "lang": "en",
              "value": "February 2004"
            },
            []
          ],
          [
            "2004-05",
            {
              "lang": "en",
              "value": "May 2004"
            },
            []
          ],
          [
            "2004-08",
            {
              "lang": "en",
              "value": "August 2004"
            },
            []
          ],
          [
            "2004-11",
            {
              "lang": "en",
              "value": "November 2004"
            },
            []
          ],
          [
            "2005-02",
            {
              "lang": "en",
              "value": "February 2005"
            },
            []
          ],
          [
            "2005-05",
            {
              "lang": "en",
              "value": "May 2005"
            },
            [
              [
                "taken on",
                "2005-05-01"
              ],
              [
                "CurrentRevisionReleased",
                "2005-10-30 09:30:00"
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
          ],
          [
            "2005-08",
            {
              "lang": "en",
              "value": "August 2005"
            },
            [
              [
                "taken on",
                "2005-08-01"
              ],
              [
                "CurrentRevisionReleased",
                "2006-01-30 09:30:00"
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
          ],
          [
            "2005-11",
            {
              "lang": "en",
              "value": "November 2005"
            },
            [
              [
                "taken on",
                "2005-11-01"
              ],
              [
                "CurrentRevisionReleased",
                "2006-05-09 09:30:00"
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
          ],
          [
            "2006-02",
            {
              "lang": "en",
              "value": "February 2006"
            },
            [
              [
                "taken on",
                "2006-02-28"
              ],
              [
                "CurrentRevisionReleased",
                "2006-08-31 09:30:00"
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
          ],
          [
            "2006-05",
            {
              "lang": "en",
              "value": "May 2006"
            },
            [
              [
                "taken on",
                "2006-05-31"
              ],
              [
                "CurrentRevisionReleased",
                "2006-11-09 09:30:00"
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
          ],
          [
            "2006-08",
            {
              "lang": "en",
              "value": "August 2006"
            },
            [
              [
                "taken on",
                "2006-08-01"
              ],
              [
                "CurrentRevisionReleased",
                "2007-02-14 09:30:00"
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
          ],
          [
            "2006-11",
            {
              "lang": "en",
              "value": "November 2006"
            },
            [
              [
                "taken on",
                "2006-11-01"
              ],
              [
                "CurrentRevisionReleased",
                "2007-05-30 09:30:00"
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
          ],
          [
            "2007-02",
            {
              "lang": "en",
              "value": "February 2007"
            },
            [
              [
                "taken on",
                "2007-02-01"
              ],
              [
                "CurrentRevisionReleased",
                "2007-08-15 09:30:00"
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
          ],
          [
            "2007-05",
            {
              "lang": "en",
              "value": "May 2007"
            },
            [
              [
                "taken on",
                "2007-05-01"
              ],
              [
                "CurrentRevisionReleased",
                "2007-11-14 09:30:00"
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
          ],
          [
            "2007-08",
            {
              "lang": "en",
              "value": "August 2007"
            },
            [
              [
                "taken on",
                "2007-08-01"
              ],
              [
                "CurrentRevisionReleased",
                "2008-06-12 09:30:00"
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
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_69_1/structure",
    "@type": "qb:DataStructureDefinition",
    "qb:component": [
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_69_1/dimension/GEOGRAPHY",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "GEOGRAPHY",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_69_1_GEOGRAPHY/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_69_1/dimension/SEX",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "SEX",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_69_1_SEX/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_69_1/dimension/AGE",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "AGE",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_69_1_AGE/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_69_1/dimension/DURATION",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "DURATION",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_69_1_DURATION/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_69_1/dimension/FAMILY_TYPE",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "FAMILY_TYPE",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_69_1_FAMILY_TYPE/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_69_1/dimension/STAT_GROUP",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "STAT_GROUP",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_69_1_STAT_GROUP/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_69_1/dimension/BENEFIT",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "BENEFIT",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_69_1_BENEFIT/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_69_1/dimension/MEASURES",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "MEASURES",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_69_1_MEASURES/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_69_1/dimension/FREQ",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "FREQ",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_69_1_FREQ/def.sdmx.json"
          }
        }
      }
    ]
  },
  "okfp:nativeTemporalBounds": {
    "@value": {
      "basis": "Nomis returned TIME codelist native codes; no observations",
      "comparisonRule": "ONS-native-ISO-period-code.v1",
      "continuityEstablished": false,
      "granularity": "month",
      "maximumNative": "2007-08",
      "minimumNative": "1995-05",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# benefit claimants 5% data - working age families

The families dataset enables users to simply identify benefit units which include children. The dataset consists of adults of working age who receive additional allowances for dependent children and is a subset of claimants who appear on the working age client group dataset.

Native identifier: `NM_69_1`.

Source family: `ons-nomis-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.nomisweb.co.uk/api/v01/dataset/NM_69_1/def.sdmx.json)

Update cadence: not evidenced in captured metadata.
Temporal evidence: normalised-source-options (available-native-period-options); start 1995-05, end 2007-08.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.nomisweb.co.uk/releasecalendar.asp)

## Evidence limits

- FREQ denotes statistical observation frequency; it does not establish release cadence.
- FirstReleased and LastUpdated describe publication history, not the observation date range.
- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
