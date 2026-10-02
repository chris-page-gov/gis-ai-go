---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-releases-published/%2Freleases%2Fdatacentresandtheuknationalaccounts",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Data centres and the UK National Accounts",
  "description": "Official release catalogue entry.",
  "nativeIdentifier": "/releases/datacentresandtheuknationalaccounts",
  "sourceFamily": "ons-releases-published",
  "resource": "https://www.ons.gov.uk/releases/datacentresandtheuknationalaccounts",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "release"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search/releases?sort=release_date_asc&release-type=type-published&highlight=false&fromDate=2026-01-01&toDate=2026-12-31&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:59:09.079287Z",
      "responseSha256": "b5781c5d5c5066f546f60df7b788bb21b6590158a060f3e9dfc7e9627a8cc433",
      "sourcePointer": "/releases/508",
      "normalisedSource": "okf-plus/source/ons-releases-published.json",
      "normalisedPointer": "/records/508",
      "normalisedRecordSha256": "99f3cf2f37510c5dca146530add10e75f4f24d43861cc319bd1a3c782b4bf6bc",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/releases/datacentresandtheuknationalaccounts"
  },
  "dcterms:conformsTo": {
    "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"
  },
  "temporal": {
    "status": "not-applicable",
    "kind": "dataset-reference-period",
    "start": null,
    "end": null,
    "sourceField": null,
    "note": "Dataset reference-period extent is not applicable to this record type."
  },
  "update": {
    "frequency": {
      "status": "not-applicable",
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
    "releaseVersion": null
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
    "date_changes": null,
    "description": {
      "cancelled": false,
      "census": false,
      "finalised": true,
      "postponed": false,
      "published": true,
      "release_date": "2026-08-24T08:30:00.000Z",
      "summary": "This article will describe how data centres affect the UK National Accounts, and where relevant data are seen. It is one of a series of articles to be released by ONS on the digital economy including digital infrastructure and the development of an AI thematic account.",
      "title": "Data centres and the UK National Accounts"
    },
    "id": "/releases/datacentresandtheuknationalaccounts",
    "nativeIdentityField": "uri",
    "releaseTypeFilter": "type-published",
    "resource": "https://www.ons.gov.uk/releases/datacentresandtheuknationalaccounts",
    "sourceEvidence": {
      "pointer": "/releases/508",
      "retrievedAt": "2026-10-02T07:59:09.079287Z",
      "sha256": "b5781c5d5c5066f546f60df7b788bb21b6590158a060f3e9dfc7e9627a8cc433",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search/releases?sort=release_date_asc&release-type=type-published&highlight=false&fromDate=2026-01-01&toDate=2026-12-31&limit=1000&offset=0"
    },
    "title": "Data centres and the UK National Accounts",
    "uri": "/releases/datacentresandtheuknationalaccounts"
  }
}
---

# Data centres and the UK National Accounts

Official release catalogue entry.

Native identifier: `/releases/datacentresandtheuknationalaccounts`.

Source family: `ons-releases-published`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/releases/datacentresandtheuknationalaccounts)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
