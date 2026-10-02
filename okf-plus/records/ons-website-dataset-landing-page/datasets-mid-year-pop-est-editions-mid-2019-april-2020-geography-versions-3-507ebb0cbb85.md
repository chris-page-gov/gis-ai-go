---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Fdatasets%2Fmid-year-pop-est%2Feditions%2Fmid-2019-april-2020-geography%2Fversions%2F3",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Population Estimates for UK, England and Wales, Scotland and Northern Ireland",
  "description": "ONS website catalogue metadata.",
  "nativeIdentifier": "/datasets/mid-year-pop-est/editions/mid-2019-april-2020-geography/versions/3",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/datasets/mid-year-pop-est/editions/mid-2019-april-2020-geography/versions/3",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "Population",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "responseSha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "sourcePointer": "/items/781",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/2781",
      "normalisedRecordSha256": "b2a6ae03f51605021caf7190fb7684929fb8d8a33a87e90895dfa16f12952e23",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/datasets/mid-year-pop-est/editions/mid-2019-april-2020-geography/versions/3"
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
    "releaseVersion": "mid-2019-april-2020-geography"
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
    "cdid": "",
    "dataset_id": "mid-year-pop-est",
    "edition": "mid-2019-april-2020-geography",
    "id": "/datasets/mid-year-pop-est/editions/mid-2019-april-2020-geography/versions/3",
    "keywords": [
      "Population"
    ],
    "meta_description": "",
    "nativeIdentityField": "uri",
    "release_date": "2021-07-07T00:00:00.000Z",
    "resource": "https://www.ons.gov.uk/datasets/mid-year-pop-est/editions/mid-2019-april-2020-geography/versions/3",
    "sourceEvidence": {
      "pointer": "/items/781",
      "retrievedAt": "2026-10-02T07:58:52.295433Z",
      "sha256": "0d79e07b78fab471f1f359097e30515b2bedce7bbd543e7f239a0a7c6f3440c2",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=2000"
    },
    "summary": "Estimates of the usual resident population for the UK as at 30 June of the reference year. Provided by administrative area, single year of age and sex.",
    "title": "Population Estimates for UK, England and Wales, Scotland and Northern Ireland",
    "type": "dataset_landing_page",
    "uri": "/datasets/mid-year-pop-est/editions/mid-2019-april-2020-geography/versions/3"
  }
}
---

# Population Estimates for UK, England and Wales, Scotland and Northern Ireland

ONS website catalogue metadata.

Native identifier: `/datasets/mid-year-pop-est/editions/mid-2019-april-2020-geography/versions/3`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/datasets/mid-year-pop-est/editions/mid-2019-april-2020-geography/versions/3)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
