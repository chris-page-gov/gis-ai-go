---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-releases-upcoming/%2Freleases%2Fprovisionalpopulationestimatefortheukmid2026",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Provisional population estimate for the UK: mid-2026",
  "description": "Official release catalogue entry.",
  "nativeIdentifier": "/releases/provisionalpopulationestimatefortheukmid2026",
  "sourceFamily": "ons-releases-upcoming",
  "resource": "https://www.ons.gov.uk/releases/provisionalpopulationestimatefortheukmid2026",
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
      "sourcePointer": "/releases/130",
      "normalisedSource": "okf-plus/source/ons-releases-upcoming.json",
      "normalisedPointer": "/records/130",
      "normalisedRecordSha256": "66f50f2c406c6b5abd97bd9c8802ab0fa1adb8adeb6a34736a468377d80d82e0",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/releases/provisionalpopulationestimatefortheukmid2026"
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
      "provisional_date": "November 2026",
      "published": false,
      "release_date": "2026-11-26T09:30:00.000Z",
      "summary": "Provisional mid-year estimate of the total population of the UK.",
      "title": "Provisional population estimate for the UK: mid-2026"
    },
    "id": "/releases/provisionalpopulationestimatefortheukmid2026",
    "nativeIdentityField": "uri",
    "releaseTypeFilter": "type-upcoming",
    "resource": "https://www.ons.gov.uk/releases/provisionalpopulationestimatefortheukmid2026",
    "sourceEvidence": {
      "pointer": "/releases/130",
      "retrievedAt": "2026-10-02T07:59:10.156842Z",
      "sha256": "efe40208494d4c51e7af3768443014ed933f15719ed17d334223cfac56a21292",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search/releases?sort=release_date_asc&release-type=type-upcoming&highlight=false&fromDate=2026-01-01&toDate=2026-12-31&limit=1000&offset=0"
    },
    "title": "Provisional population estimate for the UK: mid-2026",
    "uri": "/releases/provisionalpopulationestimatefortheukmid2026"
  }
}
---

# Provisional population estimate for the UK: mid-2026

Official release catalogue entry.

Native identifier: `/releases/provisionalpopulationestimatefortheukmid2026`.

Source family: `ons-releases-upcoming`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/releases/provisionalpopulationestimatefortheukmid2026)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
