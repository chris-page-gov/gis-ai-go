---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Fbusinessindustryandtrade%2Fretailindustry%2Ftimeseries%2Fn3ds%2Fdrsi",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "AGG 14: Implied Deflator Index: Non store retailing",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/businessindustryandtrade/retailindustry/timeseries/n3ds/drsi",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/timeseries/n3ds/drsi",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:57.811101Z",
      "responseSha256": "22932aba91e4c035fde2020af198daa96c384d76c08d4e23d85ecf4f2d28f649",
      "sourcePointer": "/items/779",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/2779",
      "normalisedRecordSha256": "46f21835e9dd9724f1a33b95e96f219b42439e3cb8e9ffe384478daf0d68ba3b",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/timeseries/n3ds/drsi"
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
    "cdid": "N3DS",
    "dataset_id": "DRSI",
    "edition": "",
    "id": "/businessindustryandtrade/retailindustry/timeseries/n3ds/drsi",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-17T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/timeseries/n3ds/drsi",
    "sourceEvidence": {
      "pointer": "/items/779",
      "retrievedAt": "2026-10-02T07:58:57.811101Z",
      "sha256": "22932aba91e4c035fde2020af198daa96c384d76c08d4e23d85ecf4f2d28f649",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "",
    "title": "AGG 14: Implied Deflator Index: Non store retailing",
    "topics": [
      "9658",
      "3545"
    ],
    "type": "timeseries",
    "uri": "/businessindustryandtrade/retailindustry/timeseries/n3ds/drsi"
  }
}
---

# AGG 14: Implied Deflator Index: Non store retailing

ONS website catalogue metadata.

Native identifier: `/businessindustryandtrade/retailindustry/timeseries/n3ds/drsi`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/retailindustry/timeseries/n3ds/drsi)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
