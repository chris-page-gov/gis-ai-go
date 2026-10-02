---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-time-options/NM_1715_1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Nomis time options: NM_1715_1",
  "description": "Native time code list and selected revision metadata; no observations.",
  "nativeIdentifier": "NM_1715_1",
  "sourceFamily": "ons-nomis-time-options",
  "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1715_1/time.def.sdmx.json",
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
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1715_1/time.def.sdmx.json",
      "retrievedAt": "2026-10-02T07:49:03.935488Z",
      "responseSha256": "337518cd8f15fc5ea6429e2461ef702bca243ceb26e6f7888d8ef5868a8ec413",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-nomis-time-options.json",
      "normalisedPointer": "/records/1060",
      "normalisedRecordSha256": "4d3305cb51252a5f9d5bf3fcfb7d51fbbf2277ed1777786179047d47d81e8541",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1715_1/time.def.sdmx.json"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "normalised-source-options",
    "kind": "available-native-period-options",
    "start": 2001,
    "end": 2001,
    "sourceField": "codes",
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
  "limitations": [],
  "details": {
    "bounds": {
      "basis": "Nomis returned TIME codelist native codes; no observations",
      "comparisonRule": "Nomis-native-integer-year.v1",
      "continuityEstablished": false,
      "granularity": "year",
      "maximumNative": 2001,
      "minimumNative": 2001,
      "status": "known-option-extrema"
    },
    "codeListId": "CL_1715_1_TIME",
    "id": "NM_1715_1",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T07:49:03.935488Z",
      "sha256": "337518cd8f15fc5ea6429e2461ef702bca243ceb26e6f7888d8ef5868a8ec413",
      "status": 200,
      "url": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1715_1/time.def.sdmx.json"
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

# Nomis time options: NM_1715_1

Native time code list and selected revision metadata; no observations.

Native identifier: `NM_1715_1`.

Source family: `ons-nomis-time-options`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.nomisweb.co.uk/api/v01/dataset/NM_1715_1/time.def.sdmx.json)

Update cadence: not evidenced in captured metadata.
Temporal evidence: normalised-source-options (available-native-period-options); start 2001, end 2001.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.nomisweb.co.uk/releasecalendar.asp)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
