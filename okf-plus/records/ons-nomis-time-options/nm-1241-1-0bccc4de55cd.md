---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-nomis-time-options/NM_1241_1",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Nomis time options: NM_1241_1",
  "description": "Native time code list and selected revision metadata; no observations.",
  "nativeIdentifier": "NM_1241_1",
  "sourceFamily": "ons-nomis-time-options",
  "resource": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1241_1/time.def.sdmx.json",
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
    "@id": "https://www.nomisweb.co.uk/api/v01/dataset/NM_1241_1/time.def.sdmx.json"
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
}
---

# Nomis time options: NM_1241_1

Native time code list and selected revision metadata; no observations.

Native identifier: `NM_1241_1`.

Source family: `ons-nomis-time-options`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.nomisweb.co.uk/api/v01/dataset/NM_1241_1/time.def.sdmx.json)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.nomisweb.co.uk/releasecalendar.asp)

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
