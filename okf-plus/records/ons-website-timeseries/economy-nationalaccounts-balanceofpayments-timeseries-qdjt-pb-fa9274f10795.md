---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Feconomy%2Fnationalaccounts%2Fbalanceofpayments%2Ftimeseries%2Fqdjt%2Fpb",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Bop-consistent: Ex: NSA: Portugal",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/economy/nationalaccounts/balanceofpayments/timeseries/qdjt/pb",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/qdjt/pb",
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
      "sourcePointer": "/items/585",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/8585",
      "normalisedRecordSha256": "47ed20cb269c89a4e40a23c5f00eafc0f6a218d82789a4962435fe906dd72fbb",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/qdjt/pb"
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
    "cdid": "QDJT",
    "dataset_id": "PB",
    "edition": "",
    "id": "/economy/nationalaccounts/balanceofpayments/timeseries/qdjt/pb",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2025-10-31T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/qdjt/pb",
    "sourceEvidence": {
      "pointer": "/items/585",
      "retrievedAt": "2026-10-02T07:59:05.675884Z",
      "sha256": "160b0ad7e0528f4ac3ab64af3a3b4ec94a10819372d5f5b143e5494713f3cb89",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=8000"
    },
    "summary": "",
    "title": "Bop-consistent: Ex: NSA: Portugal",
    "topics": [
      "1245",
      "2735",
      "1583"
    ],
    "type": "timeseries",
    "uri": "/economy/nationalaccounts/balanceofpayments/timeseries/qdjt/pb"
  }
}
---

# Bop-consistent: Ex: NSA: Portugal

ONS website catalogue metadata.

Native identifier: `/economy/nationalaccounts/balanceofpayments/timeseries/qdjt/pb`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/qdjt/pb)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
