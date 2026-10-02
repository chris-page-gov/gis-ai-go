---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Femploymentandlabourmarket%2Fpeopleinwork%2Femploymentandemployeetypes%2Fdatasets%2Fpublicsectoremploymentbyindustryemp03",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "EMP03: Public sector employment by industry",
  "description": "Public sector employment by industry, UK, published quarterly, seasonally adjusted.",
  "nativeIdentifier": "/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/publicsectoremploymentbyindustryemp03",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/publicsectoremploymentbyindustryemp03",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "civil service",
    "NHS",
    "police",
    "armed forces",
    "education",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/955",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/955",
      "normalisedRecordSha256": "360053bc7a74640c86569829423d7623d8d80db8bfa872fb8ae9cb8ebfb0c33f",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/publicsectoremploymentbyindustryemp03"
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
    "cdid": "",
    "dataset_id": "",
    "edition": "",
    "id": "/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/publicsectoremploymentbyindustryemp03",
    "keywords": [
      "civil service",
      "NHS",
      "police",
      "armed forces",
      "education"
    ],
    "meta_description": "Public sector employment by industry, UK, published quarterly, seasonally adjusted.",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-14T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/publicsectoremploymentbyindustryemp03",
    "sourceEvidence": {
      "pointer": "/items/955",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Public sector employment by industry, UK, published quarterly, seasonally adjusted.",
    "title": "EMP03: Public sector employment by industry",
    "topics": [
      "5687",
      "2114",
      "9243"
    ],
    "type": "dataset_landing_page",
    "uri": "/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/publicsectoremploymentbyindustryemp03"
  }
}
---

# EMP03: Public sector employment by industry

Public sector employment by industry, UK, published quarterly, seasonally adjusted.

Native identifier: `/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/publicsectoremploymentbyindustryemp03`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/publicsectoremploymentbyindustryemp03)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
