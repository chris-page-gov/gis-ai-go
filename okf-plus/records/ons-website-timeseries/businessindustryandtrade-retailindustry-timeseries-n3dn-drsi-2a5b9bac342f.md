---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Fbusinessindustryandtrade%2Fretailindustry%2Ftimeseries%2Fn3dn%2Fdrsi",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "AGG 12: Implied Deflator Index:Total Predominantly non-food stores",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/businessindustryandtrade/retailindustry/timeseries/n3dn/drsi",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/timeseries/n3dn/drsi",
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
      "sourcePointer": "/items/777",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/2777",
      "normalisedRecordSha256": "e7d5af8a7a3c3ef6a60c810207e787f58f3f4f8868fde148f75e8d6fe0f8a7f7",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/timeseries/n3dn/drsi"
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
    "cdid": "N3DN",
    "dataset_id": "DRSI",
    "edition": "",
    "id": "/businessindustryandtrade/retailindustry/timeseries/n3dn/drsi",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-17T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/timeseries/n3dn/drsi",
    "sourceEvidence": {
      "pointer": "/items/777",
      "retrievedAt": "2026-10-02T07:58:57.811101Z",
      "sha256": "22932aba91e4c035fde2020af198daa96c384d76c08d4e23d85ecf4f2d28f649",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "",
    "title": "AGG 12: Implied Deflator Index:Total Predominantly non-food stores",
    "topics": [
      "9658",
      "3545"
    ],
    "type": "timeseries",
    "uri": "/businessindustryandtrade/retailindustry/timeseries/n3dn/drsi"
  }
}
---

# AGG 12: Implied Deflator Index:Total Predominantly non-food stores

ONS website catalogue metadata.

Native identifier: `/businessindustryandtrade/retailindustry/timeseries/n3dn/drsi`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/businessindustryandtrade/retailindustry/timeseries/n3dn/drsi)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
