---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-releases-published/%2Freleases%2Ffamiliesandhouseholdsintheuk2025",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Families and households in the UK: 2025",
  "description": "Official release catalogue entry.",
  "nativeIdentifier": "/releases/familiesandhouseholdsintheuk2025",
  "sourceFamily": "ons-releases-published",
  "resource": "https://www.ons.gov.uk/releases/familiesandhouseholdsintheuk2025",
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
      "sourcePointer": "/releases/216",
      "normalisedSource": "okf-plus/source/ons-releases-published.json",
      "normalisedPointer": "/records/216",
      "normalisedRecordSha256": "5dbdc5940d542ac9f6b53ff27bb2a82e20d03a1e4930f49d0300ad811d9f35d1",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/releases/familiesandhouseholdsintheuk2025"
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
      "release_date": "2026-04-17T08:30:00.000Z",
      "summary": "Estimates of families (with and without children) and household types, including people living alone in the UK in 2025.",
      "title": "Families and households in the UK: 2025"
    },
    "id": "/releases/familiesandhouseholdsintheuk2025",
    "nativeIdentityField": "uri",
    "releaseTypeFilter": "type-published",
    "resource": "https://www.ons.gov.uk/releases/familiesandhouseholdsintheuk2025",
    "sourceEvidence": {
      "pointer": "/releases/216",
      "retrievedAt": "2026-10-02T07:59:09.079287Z",
      "sha256": "b5781c5d5c5066f546f60df7b788bb21b6590158a060f3e9dfc7e9627a8cc433",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search/releases?sort=release_date_asc&release-type=type-published&highlight=false&fromDate=2026-01-01&toDate=2026-12-31&limit=1000&offset=0"
    },
    "title": "Families and households in the UK: 2025",
    "uri": "/releases/familiesandhouseholdsintheuk2025"
  }
}
---

# Families and households in the UK: 2025

Official release catalogue entry.

Native identifier: `/releases/familiesandhouseholdsintheuk2025`.

Source family: `ons-releases-published`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/releases/familiesandhouseholdsintheuk2025)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
