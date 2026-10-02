---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-time-options/NM_62_1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Nomis time options: NM_62_1",
  "description": "Native time code list and selected revision metadata; no observations.",
  "nativeIdentifier": "NM_62_1",
  "sourceFamily": "ons-nomis-time-options",
  "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_62_1/time.def.sdmx.json",
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
      "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_62_1/time.def.sdmx.json",
      "retrievedAt": "2026-10-02T07:32:55.881788Z",
      "responseSha256": "79ffa7ea592da0364bb15bebfec161cf97a4ea16cca38793c68cdd1f8bf31c1c",
      "sourcePointer": null,
      "normalisedSource": "okf-plus/source/ons-nomis-time-options.json",
      "normalisedPointer": "/records/39",
      "normalisedRecordSha256": "6f8733e2ff3e31d9d8c8f2faa1691aa3dd7d45b54bb92c954313332ca95721d5",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "catalogue-document"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.nomisweb.co.uk/api/v01/dataset/NM_62_1/time.def.sdmx.json"
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
    "codeListId": "CL_62_1_TIME",
    "id": "NM_62_1",
    "metadataEvidence": {
      "retrievedAt": "2026-10-02T07:32:55.881788Z",
      "sha256": "79ffa7ea592da0364bb15bebfec161cf97a4ea16cca38793c68cdd1f8bf31c1c",
      "status": 200,
      "url": "https://www.nomisweb.co.uk/api/v01/dataset/NM_62_1/time.def.sdmx.json"
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
          []
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

# Nomis time options: NM_62_1

Native time code list and selected revision metadata; no observations.

Native identifier: `NM_62_1`.

Source family: `ons-nomis-time-options`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.nomisweb.co.uk/api/v01/dataset/NM_62_1/time.def.sdmx.json)

Update cadence: not evidenced in captured metadata.
Temporal evidence: normalised-source-options (available-native-period-options); start 2001, end 2001.
Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.

[Release catalogue or change-discovery route](https://www.nomisweb.co.uk/releasecalendar.asp)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
