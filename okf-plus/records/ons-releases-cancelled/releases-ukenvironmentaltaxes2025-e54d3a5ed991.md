---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-releases-cancelled/%2Freleases%2Fukenvironmentaltaxes2025",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "UK environmental taxes: 2025",
  "description": "Official release catalogue entry.",
  "nativeIdentifier": "/releases/ukenvironmentaltaxes2025",
  "sourceFamily": "ons-releases-cancelled",
  "resource": "https://www.ons.gov.uk/releases/ukenvironmentaltaxes2025",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search/releases?sort=release_date_asc&release-type=type-cancelled&highlight=false&fromDate=2026-01-01&toDate=2026-12-31&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:59:11.130083Z",
      "responseSha256": "7a14d3ab6e4347e4678415f67ea769577dc86033d4b4ddbd42c71550c51e8db8",
      "sourcePointer": "/releases/2",
      "normalisedSource": "okf-plus/source/ons-releases-cancelled.json",
      "normalisedPointer": "/records/2",
      "normalisedRecordSha256": "b46baf0768d482d84c8be46bba06e35c5b47f8a5ca91ac366c25579546813441",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/releases/ukenvironmentaltaxes2025"
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
      "cancelled": true,
      "census": false,
      "finalised": false,
      "postponed": false,
      "provisional_date": "May 2026",
      "published": false,
      "release_date": "2026-05-06T08:30:00.000Z",
      "summary": "The value and composition of UK environmental taxes from 1997 to 2025 (where available), by type of tax and economic activity, and comparisons with other European countries.",
      "title": "UK environmental taxes: 2025"
    },
    "id": "/releases/ukenvironmentaltaxes2025",
    "nativeIdentityField": "uri",
    "releaseTypeFilter": "type-cancelled",
    "resource": "https://www.ons.gov.uk/releases/ukenvironmentaltaxes2025",
    "sourceEvidence": {
      "pointer": "/releases/2",
      "retrievedAt": "2026-10-02T07:59:11.130083Z",
      "sha256": "7a14d3ab6e4347e4678415f67ea769577dc86033d4b4ddbd42c71550c51e8db8",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search/releases?sort=release_date_asc&release-type=type-cancelled&highlight=false&fromDate=2026-01-01&toDate=2026-12-31&limit=1000&offset=0"
    },
    "title": "UK environmental taxes: 2025",
    "uri": "/releases/ukenvironmentaltaxes2025"
  }
}
---

# UK environmental taxes: 2025

Official release catalogue entry.

Native identifier: `/releases/ukenvironmentaltaxes2025`.

Source family: `ons-releases-cancelled`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/releases/ukenvironmentaltaxes2025)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
