---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Feconomy%2Fnationalaccounts%2Fsatelliteaccounts%2Ftimeseries%2Futjn%2Fct",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "0 Household final consumption expenditure: Domestic concept IDEF SA 2024=100",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/nationalaccounts/satelliteaccounts/timeseries/utjn/ct",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/timeseries/utjn/ct",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "timeseries"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:55.653503Z",
      "responseSha256": "7eadf071c4c9bfe9b9bb13d5b0bb7e96119372e8ee94369458e73a124317fa32",
      "sourcePointer": "/items/108",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/108",
      "normalisedRecordSha256": "4df5a50f2890f05fc6ee9e938790f8219149367ff6f3fdcd5c7ddec86ad73037",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/timeseries/utjn/ct"
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
      "https://www.ons.gov.uk/releasecalendar"
    ],
    "releaseFeed": [
      "https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest"
    ],
    "nextRelease": null,
    "metadataModified": null,
    "releaseVersion": ""
  },
  "rights": {
    "metadata": "Public metadata citation and factual normalisation; source rights retained.",
    "describedData": "Not established by metadata discovery; consult source-specific terms.",
    "retrievalAuthority": "metadata-only",
    "executionAdmitted": false
  },
  "limitations": [
    "Website and API representations are retained separately; matching titles do not prove equivalence.",
    "Release dates do not establish the period covered by statistical observations."
  ],
  "details": {
    "canonical_topic": "",
    "cdid": "UTJN",
    "dataset_id": "CT",
    "edition": "",
    "id": "/economy/nationalaccounts/satelliteaccounts/timeseries/utjn/ct",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-29T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/timeseries/utjn/ct",
    "sourceEvidence": {
      "pointer": "/items/108",
      "retrievedAt": "2026-10-02T07:58:55.653503Z",
      "sha256": "7eadf071c4c9bfe9b9bb13d5b0bb7e96119372e8ee94369458e73a124317fa32",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "",
    "title": "0 Household final consumption expenditure: Domestic concept IDEF SA 2024=100",
    "topics": [
      "1245",
      "2735",
      "4176"
    ],
    "type": "timeseries",
    "uri": "/economy/nationalaccounts/satelliteaccounts/timeseries/utjn/ct"
  }
}
---

# 0 Household final consumption expenditure: Domestic concept IDEF SA 2024=100

ONS website catalogue metadata.

Native identifier: `/economy/nationalaccounts/satelliteaccounts/timeseries/utjn/ct`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/nationalaccounts/satelliteaccounts/timeseries/utjn/ct)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
