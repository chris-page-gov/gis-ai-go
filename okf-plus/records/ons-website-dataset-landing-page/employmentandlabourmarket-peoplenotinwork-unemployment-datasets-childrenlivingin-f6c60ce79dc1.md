---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/ons-website-dataset-landing-page/%2Femploymentandlabourmarket%2Fpeoplenotinwork%2Funemployment%2Fdatasets%2Fchildrenlivinginlongtermworklesshouseholdsuk",
  "@type": [
    "dcat:Dataset",
    "okfp:MetadataRecord"
  ],
  "type": "Dataset",
  "title": "Children living in long-term workless households, UK",
  "description": "Data are fom the APS household datasets",
  "nativeIdentifier": "/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/childrenlivinginlongtermworklesshouseholdsuk",
  "sourceFamily": "ons-website-dataset-landing-page",
  "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/childrenlivinginlongtermworklesshouseholdsuk",
  "status": "draft",
  "generated": {
    "by": "gis-ai-go OKF+ source producer"
  },
  "okfp:machineImported": true,
  "assertionStatus": "normalised",
  "reviewStatus": "not-human-reviewed",
  "tags": [
    "life chances",
    "inactive",
    "unemployed",
    "dataset_landing_page"
  ],
  "sources": [
    {
      "resource": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "responseSha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "sourcePointer": "/items/489",
      "normalisedSource": "okf-plus/source/ons-website-dataset-landing-page.json",
      "normalisedPointer": "/records/489",
      "normalisedRecordSha256": "61ba3eabd32915d494568a2cfe4d9c429ed605d1ce0ded7600d7636235d5e40d",
      "evidenceKind": "captured-public-metadata",
      "sourcePointerStatus": "exact-native-id-match"
    }
  ],
  "prov:wasDerivedFrom": {
    "@id": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/childrenlivinginlongtermworklesshouseholdsuk"
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
    "id": "/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/childrenlivinginlongtermworklesshouseholdsuk",
    "keywords": [
      "life chances",
      "inactive",
      "unemployed"
    ],
    "meta_description": "Data are fom the APS household datasets",
    "nativeIdentityField": "uri",
    "release_date": "2016-07-03T23:00:00.000Z",
    "resource": "https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/childrenlivinginlongtermworklesshouseholdsuk",
    "sourceEvidence": {
      "pointer": "/items/489",
      "retrievedAt": "2026-10-02T07:58:49.825353Z",
      "sha256": "6d5b0456fe7c708cfbf663f1b34661c9b2a5428f65b9aea3ccba327bf11e3e8f",
      "status": 200,
      "url": "https://api.beta.ons.gov.uk/v1/search?q=&content_type=dataset_landing_page&sort=title&highlight=false&limit=1000&offset=0"
    },
    "summary": "Estimates of children living in workless and long-term workless households",
    "title": "Children living in long-term workless households, UK",
    "topics": [
      "5687",
      "4361",
      "2268"
    ],
    "type": "dataset_landing_page",
    "uri": "/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/childrenlivinginlongtermworklesshouseholdsuk"
  }
}
---

# Children living in long-term workless households, UK

Data are fom the APS household datasets

Native identifier: `/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/childrenlivinginlongtermworklesshouseholdsuk`.

Source family: `ons-website-dataset-landing-page`. Assertion: normalised metadata; independent human review is not recorded.

[Official source](https://www.ons.gov.uk/employmentandlabourmarket/peoplenotinwork/unemployment/datasets/childrenlivinginlongtermworklesshouseholdsuk)

Update cadence: not evidenced in captured metadata.
Temporal evidence: not-evidenced (dataset-reference-period); start not stated, end not stated.
No supported reference-period extent in captured metadata; release and catalogue dates are separate.

[Release catalogue or change-discovery route](https://www.ons.gov.uk/releasecalendar)
[Recent release feed](https://www.ons.gov.uk/releasecalendar?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest)

## Evidence limits

- Website and API representations are retained separately; matching titles do not prove equivalence.
- Release dates do not establish the period covered by statistical observations.

The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.
