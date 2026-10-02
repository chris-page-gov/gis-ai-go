---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Femploymentandlabourmarket%2Fpeoplenotinwork%2Fredundancies%2Fdatasets%2Fredundanciesbyindustryagesexandreemploymentratesred02",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "RED02: Redundancies by age, industry and region",
  "description": "Redundancies by industry, region, age group, sex and re-employment rates, not seasonally adjusted.",
  "nativeIdentifier": "/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundanciesbyindustryagesexandreemploymentratesred02",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundanciesbyindustryagesexandreemploymentratesred02",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "responseSha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "sourcePointer": "/items/26",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/3026",
      "normalisedRecordSha256": "070289ba65dda3157b6d7506749152a9307629c8089a20e8494594a4dc6209fd",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundanciesbyindustryagesexandreemploymentratesred02"
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
    "dataset_id": "RED02",
    "edition": "",
    "id": "/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundanciesbyindustryagesexandreemploymentratesred02",
    "keywords": [],
    "meta_description": "Redundancies by industry, region, age group, sex and re-employment rates, not seasonally adjusted.",
    "nativeIdentityField": "uri",
    "release_date": "2026-09-14T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundanciesbyindustryagesexandreemploymentratesred02",
    "sourceEvidence": {
      "pointer": "/items/26",
      "retrievedAt": "2026-10-02T07:58:53.503544Z",
      "sha256": "0ebe824ca624eef0a815aad8798cb1057b61256c539186b17205f7c3368beebc",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=3000"
    },
    "summary": "Redundancies by age, industry, and region, not seasonally adjusted. These estimates are sourced from the Labour Force Survey, a survey of households. These are official statistics.",
    "title": "RED02: Redundancies by age, industry and region",
    "topics": [
      "5687",
      "4361",
      "7583"
    ],
    "type": "dataset_landing_page",
    "uri": "/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundanciesbyindustryagesexandreemploymentratesred02"
  }
}
---

# RED02: Redundancies by age, industry and region

Redundancies by industry, region, age group, sex and re-employment rates, not seasonally adjusted.

Native identifier: `/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundanciesbyindustryagesexandreemploymentratesred02`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/redundancies/datasets/redundanciesbyindustryagesexandreemploymentratesred02)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
