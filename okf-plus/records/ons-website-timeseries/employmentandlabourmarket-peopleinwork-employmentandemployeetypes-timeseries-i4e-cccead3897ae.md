---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-timeseries/%2Femploymentandlabourmarket%2Fpeopleinwork%2Femploymentandemployeetypes%2Ftimeseries%2Fi4ea%2Flms",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "\"LFS: In Employment: Mining, energy, water supply: UK: Women: Aged 16 and over: Thousands: NSA\"",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/i4ea/lms",
  "sourceFamily": "ons-website-timeseries",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/i4ea/lms",
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
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:55.653503Z",
      "responseSha256": "7eadf071c4c9bfe9b9bb13d5b0bb7e96119372e8ee94369458e73a124317fa32",
      "sourcePointer": "/items/35",
      "normalisedSource": "okf-plus/source/ons-website-timeseries.json",
      "normalisedPointer": "/records/35",
      "normalisedRecordSha256": "bb9d963ffc9101da49a0e15043d0c59c283adccb7285acd701820407f9da1b0f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/i4ea/lms"
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
    "cdid": "I4EA",
    "dataset_id": "LMS",
    "edition": "",
    "id": "/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/i4ea/lms",
    "keywords": [],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-14T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/i4ea/lms",
    "sourceEvidence": {
      "pointer": "/items/35",
      "retrievedAt": "2026-10-02T07:58:55.653503Z",
      "sha256": "7eadf071c4c9bfe9b9bb13d5b0bb7e96119372e8ee94369458e73a124317fa32",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=timeseries&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "",
    "title": "\"LFS: In Employment: Mining, energy, water supply: UK: Women: Aged 16 and over: Thousands: NSA\"",
    "topics": [
      "5687",
      "2114",
      "9243"
    ],
    "type": "timeseries",
    "uri": "/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/i4ea/lms"
  }
}
---

# "LFS: In Employment: Mining, energy, water supply: UK: Women: Aged 16 and over: Thousands: NSA"

ONS website catalogue metadata.

Native identifier: `/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/i4ea/lms`.

Source family: `ons-website-timeseries`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/timeseries/i4ea/lms)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
