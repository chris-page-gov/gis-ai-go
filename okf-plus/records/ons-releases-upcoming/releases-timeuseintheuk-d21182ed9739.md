---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-releases-upcoming/%2Freleases%2Ftimeuseintheuk",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Time use in the UK",
  "description": "Official release catalogue entry.",
  "nativeIdentifier": "/releases/timeuseintheuk",
  "sourceFamily": "ons-releases-upcoming",
  "resource": "https://www.ons.gov.uk/releases/timeuseintheuk",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search/releases?sort=release_date_asc&release-type=type-upcoming&highlight=false&fromDate=2026-01-01&toDate=2026-12-31&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:59:10.156842Z",
      "responseSha256": "efe40208494d4c51e7af3768443014ed933f15719ed17d334223cfac56a21292",
      "sourcePointer": "/releases/45",
      "normalisedSource": "okf-plus/source/ons-releases-upcoming.json",
      "normalisedPointer": "/records/45",
      "normalisedRecordSha256": "e840c87dcaf7843610aa6ac6edcc4d46423f91b5e60472a709137109671d49d7",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/releases/timeuseintheuk"
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
      "finalised": false,
      "postponed": false,
      "provisional_date": "October to November 2026",
      "published": false,
      "release_date": "2026-10-22T08:30:00.000Z",
      "summary": "Average daily time spent by adults on activities including paid work, unpaid household work, unpaid care, travel and entertainment. These are official statistics in development. The release contains two datasets: Wave 9 (2025) and Wave 10 (2026).",
      "title": "Time use in the UK"
    },
    "id": "/releases/timeuseintheuk",
    "nativeIdentityField": "uri",
    "releaseTypeFilter": "type-upcoming",
    "resource": "https://www.ons.gov.uk/releases/timeuseintheuk",
    "sourceEvidence": {
      "pointer": "/releases/45",
      "retrievedAt": "2026-10-02T07:59:10.156842Z",
      "sha256": "efe40208494d4c51e7af3768443014ed933f15719ed17d334223cfac56a21292",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search/releases?sort=release_date_asc&release-type=type-upcoming&highlight=false&fromDate=2026-01-01&toDate=2026-12-31&limit=1000&offset=0"
    },
    "title": "Time use in the UK",
    "uri": "/releases/timeuseintheuk"
  }
}
---

# Time use in the UK

Official release catalogue entry.

Native identifier: `/releases/timeuseintheuk`.

Source family: `ons-releases-upcoming`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/releases/timeuseintheuk)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
