---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_19_1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "vacancies - seasonally adjusted series",
  "description": "an analysis of seasonally adjusted jobcentre inflows, outflows and placings during the previous accounting period together with the stock of vacancies remaining unfilled on the count date",
  "nativeIdentifier": "NM_19_1",
  "sourceFamily": "ons-nomis-datasets",
  "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_19_1/def.sdmx.json",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [],
  "sources": [
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json",
      "retrievedAt": "2026-10-02T01:18:03.834666Z",
      "responseSha256": "e782c84721db296c396660a4df4b65fa967b9cbab0b52768e1262659e37e9a54",
      "sourcePointer": "/structure/keyfamilies/keyfamily/15",
      "normalisedSource": "okf-plus/source/ons-nomis-datasets.json",
      "normalisedPointer": "/records/15",
      "normalisedRecordSha256": "06812e327d5724851d8fae87de20fc0ca8a6f1d72e90b11d04cebf6981a00fd0",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    },
    {
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_19_1/time.def.sdmx.json",
      "retrievedAt": "2026-10-02T07:32:32.733648Z",
      "responseSha256": "41f74ac436b0305f89421f4de3c0839b73469907d255ee84b0b62f760f322c34",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-nomis-time-options.json",
      "normalisedPointer": "/records/15",
      "normalisedRecordSha256": "5f6f157093a1f5b94973c4c343766a98dfea02f6a31ebacd7dd11264ac0c4a26",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.nomisweb.co.uk/api/v01/dataset/NM_19_1/def.sdmx.json"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": "1980-01",
    "end": "2001-04",
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
      "Mnemonic": "vsa",
      "Status": "Historical (not actively being updated)",
      "SubDescription": "vsa",
      "Units": "JCP Vacancies"
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
          "codelist": "CL_19_1_GEOGRAPHY",
          "conceptref": "GEOGRAPHY"
        },
        {
          "codelist": "CL_19_1_ITEM",
          "conceptref": "ITEM"
        },
        {
          "codelist": "CL_19_1_MEASURES",
          "conceptref": "MEASURES"
        },
        {
          "codelist": "CL_19_1_FREQ",
          "conceptref": "FREQ",
          "isfrequencydimension": "true"
        }
      ],
      "primarymeasure": {
        "conceptref": "OBS_VALUE"
      },
      "timedimension": {
        "codelist": "CL_19_1_TIME",
        "conceptref": "TIME"
      }
    },
    "description": {
      "lang": "en",
      "value": "an analysis of seasonally adjusted jobcentre inflows, outflows and placings during the previous accounting period together with the stock of vacancies remaining unfilled on the count date"
    },
    "id": "NM_19_1",
    "name": {
      "lang": "en",
      "value": "vacancies - seasonally adjusted series"
    },
    "uri": "Nm-19d1",
    "version": 1.0,
    "timeMetadata": {
      "bounds": {
        "basis": "Nomis returned TIME codelist native codes; no observations",
        "comparisonRule": "ONS-native-ISO-period-code.v1",
        "continuityEstablished": false,
        "granularity": "month",
        "maximumNative": "2001-04",
        "minimumNative": "1980-01",
        "status": "known-option-extrema"
      },
      "codeListId": "CL_19_1_TIME",
      "id": "NM_19_1",
      "metadataEvidence": {
        "retrievedAt": "2026-10-02T07:32:32.733648Z",
        "sha256": "41f74ac436b0305f89421f4de3c0839b73469907d255ee84b0b62f760f322c34",
        "status": 200,
        "url": "https://www.nomisweb.co.uk/api/v01/dataset/NM_19_1/time.def.sdmx.json"
      },
      "metadataStatus": "captured",
      "returnedCodeCount": 256,
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
            "1980-01",
            {
              "lang": "en",
              "value": "January 1980"
            },
            []
          ],
          [
            "1980-02",
            {
              "lang": "en",
              "value": "February 1980"
            },
            []
          ],
          [
            "1980-03",
            {
              "lang": "en",
              "value": "March 1980"
            },
            []
          ],
          [
            "1980-04",
            {
              "lang": "en",
              "value": "April 1980"
            },
            []
          ],
          [
            "1980-05",
            {
              "lang": "en",
              "value": "May 1980"
            },
            []
          ],
          [
            "1980-06",
            {
              "lang": "en",
              "value": "June 1980"
            },
            []
          ],
          [
            "1980-07",
            {
              "lang": "en",
              "value": "July 1980"
            },
            []
          ],
          [
            "1980-08",
            {
              "lang": "en",
              "value": "August 1980"
            },
            []
          ],
          [
            "1980-09",
            {
              "lang": "en",
              "value": "September 1980"
            },
            []
          ],
          [
            "1980-10",
            {
              "lang": "en",
              "value": "October 1980"
            },
            []
          ],
          [
            "1980-11",
            {
              "lang": "en",
              "value": "November 1980"
            },
            []
          ],
          [
            "1980-12",
            {
              "lang": "en",
              "value": "December 1980"
            },
            []
          ],
          [
            "1981-01",
            {
              "lang": "en",
              "value": "January 1981"
            },
            []
          ],
          [
            "1981-02",
            {
              "lang": "en",
              "value": "February 1981"
            },
            []
          ],
          [
            "1981-03",
            {
              "lang": "en",
              "value": "March 1981"
            },
            []
          ],
          [
            "1981-04",
            {
              "lang": "en",
              "value": "April 1981"
            },
            []
          ],
          [
            "1981-05",
            {
              "lang": "en",
              "value": "May 1981"
            },
            []
          ],
          [
            "1981-06",
            {
              "lang": "en",
              "value": "June 1981"
            },
            []
          ],
          [
            "1981-07",
            {
              "lang": "en",
              "value": "July 1981"
            },
            []
          ],
          [
            "1981-08",
            {
              "lang": "en",
              "value": "August 1981"
            },
            []
          ],
          [
            "1981-09",
            {
              "lang": "en",
              "value": "September 1981"
            },
            []
          ],
          [
            "1981-10",
            {
              "lang": "en",
              "value": "October 1981"
            },
            []
          ],
          [
            "1981-11",
            {
              "lang": "en",
              "value": "November 1981"
            },
            []
          ],
          [
            "1981-12",
            {
              "lang": "en",
              "value": "December 1981"
            },
            []
          ],
          [
            "1982-01",
            {
              "lang": "en",
              "value": "January 1982"
            },
            []
          ],
          [
            "1982-02",
            {
              "lang": "en",
              "value": "February 1982"
            },
            []
          ],
          [
            "1982-03",
            {
              "lang": "en",
              "value": "March 1982"
            },
            []
          ],
          [
            "1982-04",
            {
              "lang": "en",
              "value": "April 1982"
            },
            []
          ],
          [
            "1982-05",
            {
              "lang": "en",
              "value": "May 1982"
            },
            []
          ],
          [
            "1982-06",
            {
              "lang": "en",
              "value": "June 1982"
            },
            []
          ],
          [
            "1982-07",
            {
              "lang": "en",
              "value": "July 1982"
            },
            []
          ],
          [
            "1982-08",
            {
              "lang": "en",
              "value": "August 1982"
            },
            []
          ],
          [
            "1982-09",
            {
              "lang": "en",
              "value": "September 1982"
            },
            []
          ],
          [
            "1982-10",
            {
              "lang": "en",
              "value": "October 1982"
            },
            []
          ],
          [
            "1982-11",
            {
              "lang": "en",
              "value": "November 1982"
            },
            []
          ],
          [
            "1982-12",
            {
              "lang": "en",
              "value": "December 1982"
            },
            []
          ],
          [
            "1983-01",
            {
              "lang": "en",
              "value": "January 1983"
            },
            []
          ],
          [
            "1983-02",
            {
              "lang": "en",
              "value": "February 1983"
            },
            []
          ],
          [
            "1983-03",
            {
              "lang": "en",
              "value": "March 1983"
            },
            []
          ],
          [
            "1983-04",
            {
              "lang": "en",
              "value": "April 1983"
            },
            []
          ],
          [
            "1983-05",
            {
              "lang": "en",
              "value": "May 1983"
            },
            []
          ],
          [
            "1983-06",
            {
              "lang": "en",
              "value": "June 1983"
            },
            []
          ],
          [
            "1983-07",
            {
              "lang": "en",
              "value": "July 1983"
            },
            []
          ],
          [
            "1983-08",
            {
              "lang": "en",
              "value": "August 1983"
            },
            []
          ],
          [
            "1983-09",
            {
              "lang": "en",
              "value": "September 1983"
            },
            []
          ],
          [
            "1983-10",
            {
              "lang": "en",
              "value": "October 1983"
            },
            []
          ],
          [
            "1983-11",
            {
              "lang": "en",
              "value": "November 1983"
            },
            []
          ],
          [
            "1983-12",
            {
              "lang": "en",
              "value": "December 1983"
            },
            []
          ],
          [
            "1984-01",
            {
              "lang": "en",
              "value": "January 1984"
            },
            []
          ],
          [
            "1984-02",
            {
              "lang": "en",
              "value": "February 1984"
            },
            []
          ],
          [
            "1984-03",
            {
              "lang": "en",
              "value": "March 1984"
            },
            []
          ],
          [
            "1984-04",
            {
              "lang": "en",
              "value": "April 1984"
            },
            []
          ],
          [
            "1984-05",
            {
              "lang": "en",
              "value": "May 1984"
            },
            []
          ],
          [
            "1984-06",
            {
              "lang": "en",
              "value": "June 1984"
            },
            []
          ],
          [
            "1984-07",
            {
              "lang": "en",
              "value": "July 1984"
            },
            []
          ],
          [
            "1984-08",
            {
              "lang": "en",
              "value": "August 1984"
            },
            []
          ],
          [
            "1984-09",
            {
              "lang": "en",
              "value": "September 1984"
            },
            []
          ],
          [
            "1984-10",
            {
              "lang": "en",
              "value": "October 1984"
            },
            []
          ],
          [
            "1984-11",
            {
              "lang": "en",
              "value": "November 1984"
            },
            []
          ],
          [
            "1984-12",
            {
              "lang": "en",
              "value": "December 1984"
            },
            []
          ],
          [
            "1985-01",
            {
              "lang": "en",
              "value": "January 1985"
            },
            []
          ],
          [
            "1985-02",
            {
              "lang": "en",
              "value": "February 1985"
            },
            []
          ],
          [
            "1985-03",
            {
              "lang": "en",
              "value": "March 1985"
            },
            []
          ],
          [
            "1985-04",
            {
              "lang": "en",
              "value": "April 1985"
            },
            []
          ],
          [
            "1985-05",
            {
              "lang": "en",
              "value": "May 1985"
            },
            []
          ],
          [
            "1985-06",
            {
              "lang": "en",
              "value": "June 1985"
            },
            []
          ],
          [
            "1985-07",
            {
              "lang": "en",
              "value": "July 1985"
            },
            []
          ],
          [
            "1985-08",
            {
              "lang": "en",
              "value": "August 1985"
            },
            []
          ],
          [
            "1985-09",
            {
              "lang": "en",
              "value": "September 1985"
            },
            []
          ],
          [
            "1985-10",
            {
              "lang": "en",
              "value": "October 1985"
            },
            []
          ],
          [
            "1985-11",
            {
              "lang": "en",
              "value": "November 1985"
            },
            []
          ],
          [
            "1985-12",
            {
              "lang": "en",
              "value": "December 1985"
            },
            []
          ],
          [
            "1986-01",
            {
              "lang": "en",
              "value": "January 1986"
            },
            []
          ],
          [
            "1986-02",
            {
              "lang": "en",
              "value": "February 1986"
            },
            []
          ],
          [
            "1986-03",
            {
              "lang": "en",
              "value": "March 1986"
            },
            []
          ],
          [
            "1986-04",
            {
              "lang": "en",
              "value": "April 1986"
            },
            []
          ],
          [
            "1986-05",
            {
              "lang": "en",
              "value": "May 1986"
            },
            []
          ],
          [
            "1986-06",
            {
              "lang": "en",
              "value": "June 1986"
            },
            []
          ],
          [
            "1986-07",
            {
              "lang": "en",
              "value": "July 1986"
            },
            []
          ],
          [
            "1986-08",
            {
              "lang": "en",
              "value": "August 1986"
            },
            []
          ],
          [
            "1986-09",
            {
              "lang": "en",
              "value": "September 1986"
            },
            []
          ],
          [
            "1986-10",
            {
              "lang": "en",
              "value": "October 1986"
            },
            []
          ],
          [
            "1986-11",
            {
              "lang": "en",
              "value": "November 1986"
            },
            []
          ],
          [
            "1986-12",
            {
              "lang": "en",
              "value": "December 1986"
            },
            []
          ],
          [
            "1987-01",
            {
              "lang": "en",
              "value": "January 1987"
            },
            []
          ],
          [
            "1987-02",
            {
              "lang": "en",
              "value": "February 1987"
            },
            []
          ],
          [
            "1987-03",
            {
              "lang": "en",
              "value": "March 1987"
            },
            []
          ],
          [
            "1987-04",
            {
              "lang": "en",
              "value": "April 1987"
            },
            []
          ],
          [
            "1987-05",
            {
              "lang": "en",
              "value": "May 1987"
            },
            []
          ],
          [
            "1987-06",
            {
              "lang": "en",
              "value": "June 1987"
            },
            []
          ],
          [
            "1987-07",
            {
              "lang": "en",
              "value": "July 1987"
            },
            []
          ],
          [
            "1987-08",
            {
              "lang": "en",
              "value": "August 1987"
            },
            []
          ],
          [
            "1987-09",
            {
              "lang": "en",
              "value": "September 1987"
            },
            []
          ],
          [
            "1987-10",
            {
              "lang": "en",
              "value": "October 1987"
            },
            []
          ],
          [
            "1987-11",
            {
              "lang": "en",
              "value": "November 1987"
            },
            []
          ],
          [
            "1987-12",
            {
              "lang": "en",
              "value": "December 1987"
            },
            []
          ],
          [
            "1988-01",
            {
              "lang": "en",
              "value": "January 1988"
            },
            []
          ],
          [
            "1988-02",
            {
              "lang": "en",
              "value": "February 1988"
            },
            []
          ],
          [
            "1988-03",
            {
              "lang": "en",
              "value": "March 1988"
            },
            []
          ],
          [
            "1988-04",
            {
              "lang": "en",
              "value": "April 1988"
            },
            []
          ],
          [
            "1988-05",
            {
              "lang": "en",
              "value": "May 1988"
            },
            []
          ],
          [
            "1988-06",
            {
              "lang": "en",
              "value": "June 1988"
            },
            []
          ],
          [
            "1988-07",
            {
              "lang": "en",
              "value": "July 1988"
            },
            []
          ],
          [
            "1988-08",
            {
              "lang": "en",
              "value": "August 1988"
            },
            []
          ],
          [
            "1988-09",
            {
              "lang": "en",
              "value": "September 1988"
            },
            []
          ],
          [
            "1988-10",
            {
              "lang": "en",
              "value": "October 1988"
            },
            []
          ],
          [
            "1988-11",
            {
              "lang": "en",
              "value": "November 1988"
            },
            []
          ],
          [
            "1988-12",
            {
              "lang": "en",
              "value": "December 1988"
            },
            []
          ],
          [
            "1989-01",
            {
              "lang": "en",
              "value": "January 1989"
            },
            []
          ],
          [
            "1989-02",
            {
              "lang": "en",
              "value": "February 1989"
            },
            []
          ],
          [
            "1989-03",
            {
              "lang": "en",
              "value": "March 1989"
            },
            []
          ],
          [
            "1989-04",
            {
              "lang": "en",
              "value": "April 1989"
            },
            []
          ],
          [
            "1989-05",
            {
              "lang": "en",
              "value": "May 1989"
            },
            []
          ],
          [
            "1989-06",
            {
              "lang": "en",
              "value": "June 1989"
            },
            []
          ],
          [
            "1989-07",
            {
              "lang": "en",
              "value": "July 1989"
            },
            []
          ],
          [
            "1989-08",
            {
              "lang": "en",
              "value": "August 1989"
            },
            []
          ],
          [
            "1989-09",
            {
              "lang": "en",
              "value": "September 1989"
            },
            []
          ],
          [
            "1989-10",
            {
              "lang": "en",
              "value": "October 1989"
            },
            []
          ],
          [
            "1989-11",
            {
              "lang": "en",
              "value": "November 1989"
            },
            []
          ],
          [
            "1989-12",
            {
              "lang": "en",
              "value": "December 1989"
            },
            []
          ],
          [
            "1990-01",
            {
              "lang": "en",
              "value": "January 1990"
            },
            []
          ],
          [
            "1990-02",
            {
              "lang": "en",
              "value": "February 1990"
            },
            []
          ],
          [
            "1990-03",
            {
              "lang": "en",
              "value": "March 1990"
            },
            []
          ],
          [
            "1990-04",
            {
              "lang": "en",
              "value": "April 1990"
            },
            []
          ],
          [
            "1990-05",
            {
              "lang": "en",
              "value": "May 1990"
            },
            []
          ],
          [
            "1990-06",
            {
              "lang": "en",
              "value": "June 1990"
            },
            []
          ],
          [
            "1990-07",
            {
              "lang": "en",
              "value": "July 1990"
            },
            []
          ],
          [
            "1990-08",
            {
              "lang": "en",
              "value": "August 1990"
            },
            []
          ],
          [
            "1990-09",
            {
              "lang": "en",
              "value": "September 1990"
            },
            []
          ],
          [
            "1990-10",
            {
              "lang": "en",
              "value": "October 1990"
            },
            []
          ],
          [
            "1990-11",
            {
              "lang": "en",
              "value": "November 1990"
            },
            []
          ],
          [
            "1990-12",
            {
              "lang": "en",
              "value": "December 1990"
            },
            []
          ],
          [
            "1991-01",
            {
              "lang": "en",
              "value": "January 1991"
            },
            []
          ],
          [
            "1991-02",
            {
              "lang": "en",
              "value": "February 1991"
            },
            []
          ],
          [
            "1991-03",
            {
              "lang": "en",
              "value": "March 1991"
            },
            []
          ],
          [
            "1991-04",
            {
              "lang": "en",
              "value": "April 1991"
            },
            []
          ],
          [
            "1991-05",
            {
              "lang": "en",
              "value": "May 1991"
            },
            []
          ],
          [
            "1991-06",
            {
              "lang": "en",
              "value": "June 1991"
            },
            []
          ],
          [
            "1991-07",
            {
              "lang": "en",
              "value": "July 1991"
            },
            []
          ],
          [
            "1991-08",
            {
              "lang": "en",
              "value": "August 1991"
            },
            []
          ],
          [
            "1991-09",
            {
              "lang": "en",
              "value": "September 1991"
            },
            []
          ],
          [
            "1991-10",
            {
              "lang": "en",
              "value": "October 1991"
            },
            []
          ],
          [
            "1991-11",
            {
              "lang": "en",
              "value": "November 1991"
            },
            []
          ],
          [
            "1991-12",
            {
              "lang": "en",
              "value": "December 1991"
            },
            []
          ],
          [
            "1992-01",
            {
              "lang": "en",
              "value": "January 1992"
            },
            []
          ],
          [
            "1992-02",
            {
              "lang": "en",
              "value": "February 1992"
            },
            []
          ],
          [
            "1992-03",
            {
              "lang": "en",
              "value": "March 1992"
            },
            []
          ],
          [
            "1992-04",
            {
              "lang": "en",
              "value": "April 1992"
            },
            []
          ],
          [
            "1992-05",
            {
              "lang": "en",
              "value": "May 1992"
            },
            []
          ],
          [
            "1992-06",
            {
              "lang": "en",
              "value": "June 1992"
            },
            []
          ],
          [
            "1992-07",
            {
              "lang": "en",
              "value": "July 1992"
            },
            []
          ],
          [
            "1992-08",
            {
              "lang": "en",
              "value": "August 1992"
            },
            []
          ],
          [
            "1992-09",
            {
              "lang": "en",
              "value": "September 1992"
            },
            []
          ],
          [
            "1992-10",
            {
              "lang": "en",
              "value": "October 1992"
            },
            []
          ],
          [
            "1992-11",
            {
              "lang": "en",
              "value": "November 1992"
            },
            []
          ],
          [
            "1992-12",
            {
              "lang": "en",
              "value": "December 1992"
            },
            []
          ],
          [
            "1993-01",
            {
              "lang": "en",
              "value": "January 1993"
            },
            []
          ],
          [
            "1993-02",
            {
              "lang": "en",
              "value": "February 1993"
            },
            []
          ],
          [
            "1993-03",
            {
              "lang": "en",
              "value": "March 1993"
            },
            []
          ],
          [
            "1993-04",
            {
              "lang": "en",
              "value": "April 1993"
            },
            []
          ],
          [
            "1993-05",
            {
              "lang": "en",
              "value": "May 1993"
            },
            []
          ],
          [
            "1993-06",
            {
              "lang": "en",
              "value": "June 1993"
            },
            []
          ],
          [
            "1993-07",
            {
              "lang": "en",
              "value": "July 1993"
            },
            []
          ],
          [
            "1993-08",
            {
              "lang": "en",
              "value": "August 1993"
            },
            []
          ],
          [
            "1993-09",
            {
              "lang": "en",
              "value": "September 1993"
            },
            []
          ],
          [
            "1993-10",
            {
              "lang": "en",
              "value": "October 1993"
            },
            []
          ],
          [
            "1993-11",
            {
              "lang": "en",
              "value": "November 1993"
            },
            []
          ],
          [
            "1993-12",
            {
              "lang": "en",
              "value": "December 1993"
            },
            []
          ],
          [
            "1994-01",
            {
              "lang": "en",
              "value": "January 1994"
            },
            []
          ],
          [
            "1994-02",
            {
              "lang": "en",
              "value": "February 1994"
            },
            []
          ],
          [
            "1994-03",
            {
              "lang": "en",
              "value": "March 1994"
            },
            []
          ],
          [
            "1994-04",
            {
              "lang": "en",
              "value": "April 1994"
            },
            []
          ],
          [
            "1994-05",
            {
              "lang": "en",
              "value": "May 1994"
            },
            []
          ],
          [
            "1994-06",
            {
              "lang": "en",
              "value": "June 1994"
            },
            []
          ],
          [
            "1994-07",
            {
              "lang": "en",
              "value": "July 1994"
            },
            []
          ],
          [
            "1994-08",
            {
              "lang": "en",
              "value": "August 1994"
            },
            []
          ],
          [
            "1994-09",
            {
              "lang": "en",
              "value": "September 1994"
            },
            []
          ],
          [
            "1994-10",
            {
              "lang": "en",
              "value": "October 1994"
            },
            []
          ],
          [
            "1994-11",
            {
              "lang": "en",
              "value": "November 1994"
            },
            []
          ],
          [
            "1994-12",
            {
              "lang": "en",
              "value": "December 1994"
            },
            []
          ],
          [
            "1995-01",
            {
              "lang": "en",
              "value": "January 1995"
            },
            []
          ],
          [
            "1995-02",
            {
              "lang": "en",
              "value": "February 1995"
            },
            []
          ],
          [
            "1995-03",
            {
              "lang": "en",
              "value": "March 1995"
            },
            []
          ],
          [
            "1995-04",
            {
              "lang": "en",
              "value": "April 1995"
            },
            []
          ],
          [
            "1995-05",
            {
              "lang": "en",
              "value": "May 1995"
            },
            []
          ],
          [
            "1995-06",
            {
              "lang": "en",
              "value": "June 1995"
            },
            []
          ],
          [
            "1995-07",
            {
              "lang": "en",
              "value": "July 1995"
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
            "1995-09",
            {
              "lang": "en",
              "value": "September 1995"
            },
            []
          ],
          [
            "1995-10",
            {
              "lang": "en",
              "value": "October 1995"
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
            "1995-12",
            {
              "lang": "en",
              "value": "December 1995"
            },
            []
          ],
          [
            "1996-01",
            {
              "lang": "en",
              "value": "January 1996"
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
            "1996-03",
            {
              "lang": "en",
              "value": "March 1996"
            },
            []
          ],
          [
            "1996-04",
            {
              "lang": "en",
              "value": "April 1996"
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
            "1996-06",
            {
              "lang": "en",
              "value": "June 1996"
            },
            []
          ],
          [
            "1996-07",
            {
              "lang": "en",
              "value": "July 1996"
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
            "1996-09",
            {
              "lang": "en",
              "value": "September 1996"
            },
            []
          ],
          [
            "1996-10",
            {
              "lang": "en",
              "value": "October 1996"
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
            "1996-12",
            {
              "lang": "en",
              "value": "December 1996"
            },
            []
          ],
          [
            "1997-01",
            {
              "lang": "en",
              "value": "January 1997"
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
            "1997-03",
            {
              "lang": "en",
              "value": "March 1997"
            },
            []
          ],
          [
            "1997-04",
            {
              "lang": "en",
              "value": "April 1997"
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
            "1997-06",
            {
              "lang": "en",
              "value": "June 1997"
            },
            []
          ],
          [
            "1997-07",
            {
              "lang": "en",
              "value": "July 1997"
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
            "1997-09",
            {
              "lang": "en",
              "value": "September 1997"
            },
            []
          ],
          [
            "1997-10",
            {
              "lang": "en",
              "value": "October 1997"
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
            "1997-12",
            {
              "lang": "en",
              "value": "December 1997"
            },
            []
          ],
          [
            "1998-01",
            {
              "lang": "en",
              "value": "January 1998"
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
            "1998-03",
            {
              "lang": "en",
              "value": "March 1998"
            },
            []
          ],
          [
            "1998-04",
            {
              "lang": "en",
              "value": "April 1998"
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
            "1998-06",
            {
              "lang": "en",
              "value": "June 1998"
            },
            []
          ],
          [
            "1998-07",
            {
              "lang": "en",
              "value": "July 1998"
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
            "1998-09",
            {
              "lang": "en",
              "value": "September 1998"
            },
            []
          ],
          [
            "1998-10",
            {
              "lang": "en",
              "value": "October 1998"
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
            "1998-12",
            {
              "lang": "en",
              "value": "December 1998"
            },
            []
          ],
          [
            "1999-01",
            {
              "lang": "en",
              "value": "January 1999"
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
            "1999-03",
            {
              "lang": "en",
              "value": "March 1999"
            },
            []
          ],
          [
            "1999-04",
            {
              "lang": "en",
              "value": "April 1999"
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
            "1999-06",
            {
              "lang": "en",
              "value": "June 1999"
            },
            []
          ],
          [
            "1999-07",
            {
              "lang": "en",
              "value": "July 1999"
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
            "1999-09",
            {
              "lang": "en",
              "value": "September 1999"
            },
            []
          ],
          [
            "1999-10",
            {
              "lang": "en",
              "value": "October 1999"
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
            "1999-12",
            {
              "lang": "en",
              "value": "December 1999"
            },
            []
          ],
          [
            "2000-01",
            {
              "lang": "en",
              "value": "January 2000"
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
            "2000-03",
            {
              "lang": "en",
              "value": "March 2000"
            },
            []
          ],
          [
            "2000-04",
            {
              "lang": "en",
              "value": "April 2000"
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
            "2000-06",
            {
              "lang": "en",
              "value": "June 2000"
            },
            []
          ],
          [
            "2000-07",
            {
              "lang": "en",
              "value": "July 2000"
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
            "2000-09",
            {
              "lang": "en",
              "value": "September 2000"
            },
            []
          ],
          [
            "2000-10",
            {
              "lang": "en",
              "value": "October 2000"
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
            "2000-12",
            {
              "lang": "en",
              "value": "December 2000"
            },
            []
          ],
          [
            "2001-01",
            {
              "lang": "en",
              "value": "January 2001"
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
            "2001-03",
            {
              "lang": "en",
              "value": "March 2001"
            },
            []
          ],
          [
            "2001-04",
            {
              "lang": "en",
              "value": "April 2001"
            },
            []
          ]
        ]
      }
    }
  },
  "qb:structure": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_19_1/structure",
    "@type": "qb:DataStructureDefinition",
    "qb:component": [
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_19_1/dimension/GEOGRAPHY",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "GEOGRAPHY",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_19_1_GEOGRAPHY/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_19_1/dimension/ITEM",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "ITEM",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_19_1_ITEM/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_19_1/dimension/MEASURES",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "MEASURES",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_19_1_MEASURES/def.sdmx.json"
          }
        }
      },
      {
        "@type": "qb:ComponentSpecification",
        "qb:dimension": {
          "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-datasets/NM_19_1/dimension/FREQ",
          "@type": "qb:DimensionProperty",
          "rdfs:label": "FREQ",
          "qb:codeList": {
            "@id": "https://www.nomisweb.co.uk/api/v01/codelist/CL_19_1_FREQ/def.sdmx.json"
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
      "maximumNative": "2001-04",
      "minimumNative": "1980-01",
      "status": "known-option-extrema"
    },
    "@type": "@json"
  }
}
---

# vacancies - seasonally adjusted series

an analysis of seasonally adjusted jobcentre inflows, outflows and placings during the previous accounting period together with the stock of vacancies remaining unfilled on the count date

Native identifier: `NM_19_1`.

Source family: `ons-nomis-datasets`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.nomisweb.co.uk/api/v01/dataset/NM_19_1/def.sdmx.json)

Update cadence: not evidenced in captured metadata.
Temporal evidence: normalised-source-options (available-native-period-options); start 1980-01, end 2001-04.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.nomisweb.co.uk/releasecalendar.asp)

## Evidence limits

- FREQ denotes statistical observation frequency; it does not establish release cadence.
- FirstReleased and LastUpdated describe publication history, not the observation date range.
- Time-option extrema describe available native codes; continuity and populated observation cells have not been established.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
