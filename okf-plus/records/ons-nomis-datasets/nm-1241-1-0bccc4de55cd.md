---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1241_1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "SH12 - Persons resident outside local authority area [1961 census]",
  "description": "Gives figures by sex of persons with a usual residence outside the Local Authority area of enumeration distinguishing visitors from elsewhere in England and Wales and from outside England and Wales. For Local Authority areas split by New Town or Conurbation Centre boundaries the parts of the local authority area within and outside the New Town or Conurbation Centre are treated as separate Local Authority areas.",
  "nativeIdentifier": "NM_1241_1",
  "sourceFamily": "ons-nomis-datasets",
  "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1241_1/def.sdmx.json",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Persons",
    "Sex",
    "Visitors"
  ],
  "sources": [
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json",
      "retrievedAt": "2026-10-02T01:18:03.834666Z",
      "responseSha256": "e782c84721db296c396660a4df4b65fa967b9cbab0b52768e1262659e37e9a54",
      "sourcePointer": "/structure/keyfamilies/keyfamily/777",
      "normalisedSource": "okf-plus/source/ons-nomis-datasets.json",
      "normalisedPointer": "/records/777",
      "normalisedRecordSha256": "f01e7b4bb1fbf3bdf6e01e9265dbbade5db7981af64b2fc70cc820c7695a9058",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1241_1/time.def.sdmx.json",
      "retrievedAt": "2026-10-02T07:44:38.893219Z",
      "responseSha256": "d7d3c32baa2dd48dc76c20ca7717da4439ad51da5ecab4afdd5348983b3c0029",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-nomis-time-options.json",
      "normalisedPointer": "/records/777",
      "normalisedRecordSha256": "6b96acf6f2dd28b0dab29d0615638612dac62c56ce06a81aac4a822e3c2bd6f3",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1241_1/def.sdmx.json"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "not-evidenced",
    "kind": "dataset-reference-period",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "No supported reference-period extent in captured metadata; release and catalogue dates are separate."
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
    "metadataModified": "2021-01-28 09:30:00",
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
      "FirstReleased": "2021-01-28 09:30:00",
      "Keywords": "Persons,Sex,Visitors",
      "LastUpdated": "2021-01-28 09:30:00",
      "Mnemonic": "c1961sh12",
      "Status": "Historical (not actively being updated)",
      "SubDescription": "Persons with a usual residence outside the local authority area of enumeration",
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
          "codelist": "CL_1241_1_GEOGRAPHY",
          "conceptref": "GEOGRAPHY"
        },
        {
          "codelist": "CL_1241_1_AREA",
          "conceptref": "AREA"
        },
        {
          "codelist": "CL_1241_1_C_SEX",
          "conceptref": "C_SEX"
        },
        {
          "codelist": "CL_1241_1_MEASURES",
          "conceptref": "MEASURES"
        },
        {
          "codelist": "CL_1241_1_FREQ",
          "conceptref": "FREQ",
          "isfrequencydimension": "true"
        }
      ],
      "primarymeasure": {
        "conceptref": "OBS_VALUE"
      },
      "timedimension": {
        "codelist": "CL_1241_1_TIME",
        "conceptref": "TIME"
      }
    },
    "description": {
      "lang": "en",
      "value": "Gives figures by sex of persons with a usual residence outside the Local Authority area of enumeration distinguishing visitors from elsewhere in England and Wales and from outside England and Wales. For Local Authority areas split by New Town or Conurbation Centre boundaries the parts of the local authority area within and outside the New Town or Conurbation Centre are treated as separate Local Authority areas."
    },
    "id": "NM_1241_1",
    "name": {
      "lang": "en",
      "value": "SH12 - Persons resident outside local authority area [1961 census]"
    },
    "uri": "Nm-1241d1",
    "version": 1.0,
    "timeMetadata": {
      "bounds": {
        "basis": "published time-dimension option codes; no observations",
        "continuityEstablished": false,
        "maximumNative": null,
        "minimumNative": null,
        "status": "unknown-incomplete-options"
      },
      "codeListId": "CL_1241_1_TIME",
      "id": "NM_1241_1",
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T07:44:38.893219Z",
        "sha256": "d7d3c32baa2dd48dc76c20ca7717da4439ad51da5ecab4afdd5348983b3c0029",
        "status": 200,
        "url": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1241_1/time.def.sdmx.json"
      },
      "metadataStatus": "no-returned-time-codelist",
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
        "rows": []
      }
    }
  },
  "qb:structure": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1241_1/structure",
    "@type": "qb:DataStructureDefinition",
    "qb:component": [
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1241_1/dimension/GEOGRAPHY",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "GEOGRAPHY",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1241_1_GEOGRAPHY/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1241_1/dimension/AREA",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "AREA",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1241_1_AREA/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1241_1/dimension/C_SEX",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "C_SEX",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1241_1_C_SEX/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1241_1/dimension/MEASURES",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "MEASURES",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1241_1_MEASURES/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_1241_1/dimension/FREQ",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "FREQ",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_1241_1_FREQ/def.sdmx.json"
          }
        }
      }
    ]
  }
}
---

# SH12 - Persons resident outside local authority area [1961 census]

Gives figures by sex of persons with a usual residence outside the Local Authority area of enumeration distinguishing visitors from elsewhere in England and Wales and from outside England and Wales. For Local Authority areas split by New Town or Conurbation Centre boundaries the parts of the local authority area within and outside the New Town or Conurbation Centre are treated as separate Local Authority areas.

Native identifier: `NM_1241_1`.

Source family: `ons-nomis-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.nomisweb.co.uk/api/v01/dataset/NM_1241_1/def.sdmx.json)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.nomisweb.co.uk/releasecalendar.asp)

## Evidence limits

- FREQ denotes statistical observation frequency; it does not establish release cadence.
- FirstReleased and LastUpdated describe publication history, not the observation date range.
- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
