---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-releases-published/%2Freleases%2Fmaterialfootprintintheuk",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Material footprint in the UK",
  "description": "Official release catalogue entry.",
  "nativeIdentifier": "/releases/materialfootprintintheuk",
  "sourceFamily": "ons-releases-published",
  "resource": "https://www.ons.gov.uk/releases/materialfootprintintheuk",
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
      "sourcePointer": "/releases/259",
      "normalisedSource": "okf-plus/source/ons-releases-published.json",
      "normalisedPointer": "/records/259",
      "normalisedRecordSha256": "7561f4bc04bb2bd00f439924d1a86af6b9b58488b9d8509f2946b38387cd2bc7",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/releases/materialfootprintintheuk"
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
      "release_date": "2026-05-08T08:30:00.000Z",
      "summary": "The UK’s material footprint captures the amount of domestic and foreign extraction of materials needed to produce the goods and services used by households, governments and charities in the UK.",
      "title": "Material footprint in the UK"
    },
    "id": "/releases/materialfootprintintheuk",
    "nativeIdentityField": "uri",
    "releaseTypeFilter": "type-published",
    "resource": "https://www.ons.gov.uk/releases/materialfootprintintheuk",
    "sourceEvidence": {
      "pointer": "/releases/259",
      "retrievedAt": "2026-10-02T07:59:09.079287Z",
      "sha256": "b5781c5d5c5066f546f60df7b788bb21b6590158a060f3e9dfc7e9627a8cc433",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search/releases?sort=release_date_asc&release-type=type-published&highlight=false&fromDate=2026-01-01&toDate=2026-12-31&limit=1000&offset=0"
    },
    "title": "Material footprint in the UK",
    "uri": "/releases/materialfootprintintheuk"
  }
}
---

# Material footprint in the UK

Official release catalogue entry.

Native identifier: `/releases/materialfootprintintheuk`.

Source family: `ons-releases-published`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/releases/materialfootprintintheuk)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
