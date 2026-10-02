---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-releases-published/%2Freleases%2Fanexplainerofukgovernmentexpenditure",
  "@type": [
    "dcterms:BibliographicResource",
    "okfp:MetadataRecord"
  ],
  "type": "Documentation",
  "title": "Government expenditure in the UK",
  "description": "Official release catalogue entry.",
  "nativeIdentifier": "/releases/anexplainerofukgovernmentexpenditure",
  "sourceFamily": "ons-releases-published",
  "resource": "https://www.ons.gov.uk/releases/anexplainerofukgovernmentexpenditure",
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
      "sourcePointer": "/releases/287",
      "normalisedSource": "okf-plus/source/ons-releases-published.json",
      "normalisedPointer": "/records/287",
      "normalisedRecordSha256": "f9b5228b7bdb871bc447abc6e0ea4ae74807ce756c811c2c676afee1249990f1",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/releases/anexplainerofukgovernmentexpenditure"
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
    "date_changes": [
      {
        "change_notice": "The previously stated release time of 07:00am was incorrect. This was caused by human error and has now been altered to the correct release time of 09:30am.",
        "previous_date": "2026-05-18T06:00:00.000Z"
      }
    ],
    "description": {
      "cancelled": false,
      "census": false,
      "finalised": true,
      "postponed": true,
      "published": true,
      "release_date": "2026-05-18T08:30:00.000Z",
      "summary": "Types of government expenditure and their trends over the last 30 years, including current and capital spending by central and local government.",
      "title": "Government expenditure in the UK"
    },
    "id": "/releases/anexplainerofukgovernmentexpenditure",
    "nativeIdentityField": "uri",
    "releaseTypeFilter": "type-published",
    "resource": "https://www.ons.gov.uk/releases/anexplainerofukgovernmentexpenditure",
    "sourceEvidence": {
      "pointer": "/releases/287",
      "retrievedAt": "2026-10-02T07:59:09.079287Z",
      "sha256": "b5781c5d5c5066f546f60df7b788bb21b6590158a060f3e9dfc7e9627a8cc433",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search/releases?sort=release_date_asc&release-type=type-published&highlight=false&fromDate=2026-01-01&toDate=2026-12-31&limit=1000&offset=0"
    },
    "title": "Government expenditure in the UK",
    "uri": "/releases/anexplainerofukgovernmentexpenditure"
  }
}
---

# Government expenditure in the UK

Official release catalogue entry.

Native identifier: `/releases/anexplainerofukgovernmentexpenditure`.

Source family: `ons-releases-published`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/releases/anexplainerofukgovernmentexpenditure)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-applicable (dataset-reference-period); start not stated, end not stated.
Dataset reference-period extent is not applicable to this record type.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
