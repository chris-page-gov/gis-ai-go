---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Feconomy%2Fgovernmentpublicsectorandtaxes%2Fpublicsectorfinance%2Ftimeseries%2Fct9g%2Fpusf",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "CG: AS: F424N1 K.7 Nominal holding gains/losses: Student Loan Stock Revaluations",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/ct9g/pusf",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/ct9g/pusf",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=8000",
      "retrievedAt": "2026-10-02T07:59:05.675884Z",
      "responseSha256": "160b0ad7e0528f4ac3ab64af3a3b4ec94a10819372d5f5b143e5494713f3cb89",
      "sourcePointer": "/items/939",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/8939",
      "normalisedRecordSha256": "d71dc32a389d59d244914bf7c46ce68c47ce1e6e2a392b68b4f7f9552df86c15",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/ct9g/pusf"
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
    "cdid": "CT9G",
    "dataset_id": "PUSF",
    "edition": "",
    "id": "/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/ct9g/pusf",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-21T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/ct9g/pusf",
    "sourceEvidence": {
      "pointer": "/items/939",
      "retrievedAt": "2026-10-02T07:59:05.675884Z",
      "sha256": "160b0ad7e0528f4ac3ab64af3a3b4ec94a10819372d5f5b143e5494713f3cb89",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=8000"
    },
    "summary": "",
    "title": "CG: AS: F424N1 K.7 Nominal holding gains/losses: Student Loan Stock Revaluations",
    "topics": [
      "1245",
      "9828",
      "3863"
    ],
    "type": "timeseries",
    "uri": "/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/ct9g/pusf"
  }
}
---

# CG: AS: F424N1 K.7 Nominal holding gains/losses: Student Loan Stock Revaluations

ONS website catalogue metadata.

Native identifier: `/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/ct9g/pusf`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/ct9g/pusf)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
